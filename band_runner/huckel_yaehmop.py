#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, csv, re
import numpy as np
import matplotlib.pyplot as plt
from ase.io import read
from yaehmop_generic import (BandPath, write_periodic_input_generic, run_bind,
    parse_band, normalized_path_coordinate, resolve_yaehmop_assets)

HERE=Path(__file__).resolve().parent

def read_param(path: Path):
    K=1.75; weighted=True; nval={}; clean=[]
    for line in path.read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#') or s.startswith(';'): continue
        m=re.match(r'(?i)^K\s*(?:=|\s)\s*([-+0-9.eE]+)\s*$',s)
        if m: K=float(m.group(1)); continue
        m=re.match(r'(?i)^WEIGHTED_HIJ\s*(?:=|\s)\s*(\S+)\s*$',s)
        if m: weighted=m.group(1).lower() not in ('0','false','no','off'); continue
        if s.upper()=='END': clean.append('END'); continue
        f=s.split()
        if len(f)>=11:
            clean.append(line); nval[f[0].capitalize()]=int(f[2])
    if not clean or clean[-1].strip().upper()!='END': clean.append('END')
    return K,weighted,nval,'\n'.join(clean)+'\n'

def points_from_flat(vals,dim):
    a=np.asarray(vals,float)
    if len(a)%dim: raise SystemExit('The number of coordinates is incompatible with --point-dim.')
    q=a.reshape(-1,dim); out=np.zeros((len(q),3)); out[:,:dim]=q
    if len(out)<2: raise SystemExit('Provide at least two symmetry points.')
    return out

def main():
    ap=argparse.ArgumentParser(description='Calculate Extended-Huckel bands using the original YAeHMOP bind executable.')
    ap.add_argument('cif'); ap.add_argument('--param',default='param.txt')
    ap.add_argument('--symmetry-points','--symetry-points',dest='symmetry',nargs='+',type=float,required=True)
    ap.add_argument('--point-dim',type=int,choices=(1,2,3),default=2)
    ap.add_argument('--labels',nargs='+'); ap.add_argument('--nkpoints',type=int,default=301)
    ap.add_argument('--points-per-line',type=int); ap.add_argument('--electrons',type=int)
    ap.add_argument('--zero',choices=('vbm','none'),default='vbm')
    ap.add_argument('--output',default='results/bands_yaehmop.csv')
    ap.add_argument('--plot',default='results/bands_yaehmop.png')
    ap.add_argument('--ylim',nargs=2,type=float); ap.add_argument('--work-prefix',default='results/work/run')
    args=ap.parse_args()

    cif=Path(args.cif).resolve(); param=Path(args.param).resolve()
    if not cif.is_file(): raise SystemExit(f'CIF not found: {cif}')
    if not param.is_file(): raise SystemExit(f'Parameter file not found: {param}')
    bind,_=resolve_yaehmop_assets()
    atoms=read(cif); K,weighted,nval,clean=read_param(param)
    electrons=args.electrons
    if electrons is None:
        try: electrons=sum(nval[s.capitalize()] for s in atoms.get_chemical_symbols())
        except KeyError as e: raise SystemExit(f'Element {e.args[0]} is not present in the parameter file; use --electrons.')
    nocc=electrons//2
    pts=points_from_flat(args.symmetry,args.point_dim)
    labels=args.labels or [f'K{i}' for i in range(len(pts))]
    if len(labels)!=len(pts): raise SystemExit('--labels must contain one label per symmetry point.')
    nseg=len(pts)-1
    ppl=args.points_per_line or max(1,round((args.nkpoints-1)/nseg))
    path=BandPath(tuple(labels),pts,int(ppl))

    work=Path(args.work_prefix); work=work if work.is_absolute() else HERE/work
    work.parent.mkdir(parents=True,exist_ok=True)
    inp=work.with_suffix('.bind'); par=work.with_suffix('.parms'); log=work.with_suffix('.log')
    par.write_text(clean)
    write_periodic_input_generic(cif,inp,path,K,weighted,electrons)
    run_bind(bind,inp,par,log)
    k,Eraw=parse_band(str(inp)+'.band'); x=normalized_path_coordinate(k,atoms.cell)
    if nocc<=0 or nocc>=Eraw.shape[1]: raise SystemExit('Electron count is incompatible with the orbital basis.')
    vbm=float(Eraw[:,nocc-1].max()); cbm=float(Eraw[:,nocc].min()); gap=cbm-vbm
    E=Eraw-vbm if args.zero=='vbm' else Eraw.copy()

    out=Path(args.output); out=out if out.is_absolute() else HERE/out; out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['k_index','k_path','kx','ky','kz','band','energy_raw_eV','energy_plot_eV'])
        for ik,(xx,kv) in enumerate(zip(x,k)):
            for ib,e in enumerate(E[ik]): w.writerow([ik,xx,*kv,ib,Eraw[ik,ib],e])

    fig,ax=plt.subplots(figsize=(8,6))
    for j in range(E.shape[1]): ax.plot(x,E[:,j],lw=.8)
    tick_idx=[i*int(ppl) for i in range(len(labels)-1)]+[len(x)-1]
    ticks=[x[i] for i in tick_idx]
    for t in ticks: ax.axvline(t,lw=.5,alpha=.35)
    ax.axhline(0,lw=.6,alpha=.5); ax.set_xticks(ticks); ax.set_xticklabels(labels)
    ax.set_xlim(x[0],x[-1]); ax.set_ylabel('Energy (eV)' + (' relative to VBM' if args.zero=='vbm' else ''))
    if args.ylim: ax.set_ylim(*args.ylim)
    ax.set_title(f'YAeHMOP EHT | gap={gap:.6f} eV | K={K:.6f}'); fig.tight_layout()
    plot=Path(args.plot); plot=plot if plot.is_absolute() else HERE/plot; plot.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(plot,dpi=180); plt.close(fig)
    print(f'YAeHMOP: {bind}')
    print(f'K={K:.12g}  electrons={electrons}  orbitals={Eraw.shape[1]}  kpoints={len(k)}')
    print(f'VBM={vbm:.9f} eV  CBM={cbm:.9f} eV  indirect_gap={gap:.9f} eV')
    print(f'CSV: {out}\nPNG: {plot}\nLOG: {log}')

if __name__=='__main__': main()
