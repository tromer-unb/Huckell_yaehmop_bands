#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse,copy,csv,json,sys,time
import numpy as np
from scipy.optimize import differential_evolution,minimize
from ase.io import read
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from fit_from_image import parse_points,build_specs,apply_x,physical_ok
from yaehmop_generic import *
from image_target import load_band_image,trace_bands
BIND,PARAM_TABLE=resolve_yaehmop_assets()

def main():
    ap=argparse.ArgumentParser(description='Staged generic YAeHMOP fit from a band-structure image.')
    ap.add_argument('cif'); ap.add_argument('image'); ap.add_argument('--emin',type=float,required=True); ap.add_argument('--emax',type=float,required=True)
    ap.add_argument('--symmetry-points','--symetry-points',dest='symmetry_points',type=float,nargs='+',required=True); ap.add_argument('--point-dim',type=int,choices=(1,2,3),default=2); ap.add_argument('--labels',nargs='+',required=True)
    ap.add_argument('--points-per-line',type=int,default=30); ap.add_argument('--trace-nx',type=int,default=401); ap.add_argument('--seed',type=int,default=20260927)
    ap.add_argument('--gap-weight',type=float,default=2.0); ap.add_argument('--reg-weight',type=float,default=.04); ap.add_argument('--outdir',default='.'); ap.add_argument('--tag',default='image_staged')
    args=ap.parse_args(); out=Path(args.outdir); out.mkdir(parents=True,exist_ok=True); work=out/'work'; work.mkdir(exist_ok=True)
    cif=Path(args.cif).resolve(); image=Path(args.image).resolve(); atoms=read(cif); symbols=atoms.get_chemical_symbols(); elements=list(dict.fromkeys(s.capitalize() for s in symbols))
    defaults=subset_for_elements(parse_parameter_table(PARAM_TABLE),elements); norb=orbital_count(defaults,symbols); nelec=valence_electrons(defaults,symbols); nocc=nelec//2
    specs,x0,bounds,scales=build_specs(defaults,elements); names=[f'{a}_{b}_{c}'.strip('_') for a,b,c in specs]
    # Keep Hii in a chemistry-informed +/-5 eV trust region around tabulated YAeHMOP values.
    bounds=list(bounds)
    for i,(_,_,kind) in enumerate(specs):
        if kind=='Hii': bounds[i]=(x0[i]-5.0,x0[i]+5.0)
    points=parse_points(args.symmetry_points,args.point_dim); path=BandPath(tuple(args.labels),points,args.points_per_line)
    target=load_band_image(image,args.emin,args.emax); xtrace,Btrace,counts,seedidx=trace_bands(target,norb,args.trace_nx)
    tv=float(Btrace[:,nocc-1].max()); tc=float(Btrace[:,nocc].min()); tgap=tc-tv; tmid=.5*(tv+tc)
    pts=[]
    for a,b in zip(points[:-1],points[1:]):
        for j in range(args.points_per_line): pts.append(a+(b-a)*(j/args.points_per_line))
    pts.append(points[-1]); xcoord=normalized_path_coordinate(np.asarray(pts),atoms.cell)
    T=np.column_stack([np.interp(xcoord,xtrace,Btrace[:,j]) for j in range(norb)]); centers=np.median(T,axis=0); bw=1+3*np.exp(-(centers/4.0)**2); denom=float(np.sum(np.ones_like(T)*bw[None,:]))
    inp=work/f'{args.tag}.bind'; parm=work/f'{args.tag}.parms'; runlog=work/f'{args.tag}.run.log'; history=[]; neval=0; best=[1e99,None,None]
    def objective(x,record=True,stage=''):
        nonlocal neval,best; neval+=1; p,K=apply_x(defaults,specs,x)
        if not physical_ok(p): return 100.0
        try:
            write_parameter_file(parm,p); write_periodic_input_generic(cif,inp,path,K,True,nelec); run_bind(BIND,inp,parm,runlog); _,M=parse_band(str(inp)+'.band')
            if M.shape!=T.shape or not np.isfinite(M).all(): return 100.0
            mv=float(M[:,nocc-1].max()); mc=float(M[:,nocc].min()); mgap=mc-mv; shift=tmid-.5*(mv+mc); D=M+shift-T
            rmse=float(np.sqrt(np.mean(D*D))); wr=float(np.sqrt(np.sum(D*D*bw[None,:])/denom)); ge=mgap-tgap; reg=float(np.sqrt(np.mean(((np.asarray(x)-x0)/scales)**2)))
            loss=.4*rmse+.6*wr+args.gap_weight*abs(ge)+args.reg_weight*reg
        except Exception: return 100.0
        if record:
            row={'eval':neval,'stage':stage,'loss':loss,'rmse':rmse,'wrmse':wr,'model_gap_eV':mgap,'image_gap_eV':tgap,'gap_error_eV':ge,'shift_eV':shift,'regularization':reg,**{n:float(v) for n,v in zip(names,x)}}; history.append(row)
            if loss<best[0]: best=[loss,np.array(x,float),row.copy()]; print('BEST',json.dumps(row),flush=True)
        return float(loss)
    print(json.dumps({'elements':elements,'basis_orbitals':norb,'valence_electrons':nelec,'nocc':nocc,'n_k_fit':len(xcoord),'trace_nx':len(xtrace),'trace_seed_x':float(xtrace[seedidx]),'trace_count_distribution':{str(int(k)):int(v) for k,v in zip(*np.unique(counts,return_counts=True))},'image_gap_eV':tgap,'variables':names},indent=2),flush=True)
    t0=time.time(); base=objective(x0,True,'baseline'); print('BASE',base,flush=True); xcur=x0.copy(); stage_info=[]
    def optimize_subset(indices,label,maxiter,popsize,localiter):
        nonlocal xcur
        ind=np.array(indices,int); b=[bounds[i] for i in ind]
        def f(y):
            x=xcur.copy(); x[ind]=y; return objective(x,True,label)
        de=differential_evolution(f,b,maxiter=maxiter,popsize=popsize,seed=args.seed+len(stage_info),x0=xcur[ind],polish=False,workers=1,updating='immediate',tol=1e-5)
        loc=minimize(f,de.x,method='Nelder-Mead',bounds=b,options={'maxiter':localiter,'maxfev':max(200,localiter*12),'xatol':1e-5,'fatol':1e-6,'adaptive':True})
        y=loc.x if loc.fun<de.fun else de.x; xcur[ind]=y; val=objective(xcur,True,label+'-final')
        stage_info.append({'stage':label,'indices':ind.tolist(),'de_fun':float(de.fun),'local_fun':float(loc.fun),'final':float(val),'local_success':bool(loc.success),'local_message':str(loc.message)})
    shape_idx=[i for i,s in enumerate(specs) if s[2]!='Hii']; hii_idx=[i for i,s in enumerate(specs) if s[2]=='Hii']
    optimize_subset(shape_idx,'stage1-shape',7,5,130)
    optimize_subset(hii_idx,'stage2-Hii',8,5,160)
    # Conservative joint local refinement from the staged solution.
    loc=minimize(lambda z: objective(z,True,'stage3-joint'),xcur,method='Nelder-Mead',bounds=bounds,options={'maxiter':220,'maxfev':1500,'xatol':1e-5,'fatol':1e-6,'adaptive':True})
    if loc.fun<objective(xcur,False): xcur=loc.x.copy()
    final=objective(xcur,True,'final'); pbest,Kbest=apply_x(defaults,specs,xcur)
    with (out/f'{args.tag}_history.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(history[0])); w.writeheader(); w.writerows(history)
    result={'tag':args.tag,'source_image':str(image),'cif':str(cif),'elements':elements,'basis_orbitals':norb,'valence_electrons':nelec,'occupied_spatial_bands':nocc,'image_bbox':target['bbox'],'image_trace_gap_eV':tgap,'image_trace_VBM_eV':tv,'image_trace_CBM_eV':tc,'trace_nx':len(xtrace),'n_k_fit':len(xcoord),'variables':names,'bounds':bounds,'default_x':{n:float(v) for n,v in zip(names,x0)},'best_x':{n:float(v) for n,v in zip(names,xcur)},'K':float(Kbest),'base_loss':float(base),'final_loss':float(final),'best_seen':best[2],'stages':stage_info,'joint_local':{'fun':float(loc.fun),'success':bool(loc.success),'message':str(loc.message),'nit':int(loc.nit),'nfev':int(loc.nfev)},'evaluations':neval,'elapsed_s':time.time()-t0}
    (out/f'{args.tag}.json').write_text(json.dumps(result,indent=2)+'\n'); native=out/f'param_{args.tag}_native.dat'; write_parameter_file(native,pbest); friendly=out/f'param_{args.tag}.txt'; friendly.write_text(f'# Generic image-fitted YAeHMOP parameters\nK = {Kbest:.14g}\nWEIGHTED_HIJ = true\n\n'+native.read_text())
    np.savez_compressed(out/f'{args.tag}_digitized_target.npz',x=xtrace,bands=Btrace,counts=counts)
    print('FINAL',json.dumps(result,indent=2),flush=True)
if __name__=='__main__': main()
