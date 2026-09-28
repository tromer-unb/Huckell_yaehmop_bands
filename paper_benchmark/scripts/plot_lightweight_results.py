#!/usr/bin/env python3
from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"; OUT = ROOT / "generated_figures"; OUT.mkdir(exist_ok=True)
def read(name):
    with (RES / name).open(newline="") as handle: return list(csv.DictReader(handle))
def vals(rows, key): return np.array([float(r[key]) for r in rows])
c2=read("c2db_ablation.csv"); j3=read("jarvis3d_ablation.csv"); tmd=read("tmd_shared_cv_summary.csv"); stock=read("stock_rmse.csv")
stock2=np.mean([float(r["stock_rmse_eV"]) for r in stock if r["dimension"]=="2D"]); stock3=np.mean([float(r["stock_rmse_eV"]) for r in stock if r["dimension"]=="3D"])
fit2=vals(c2,"constrained_rmse_eV").mean(); fit3=vals(j3,"constrained_rmse_eV").mean()
fig,ax=plt.subplots(figsize=(7.2,5.0)); ax.bar(np.arange(4),[stock2,fit2,stock3,fit3]); ax.set_yscale("log"); ax.set_xticks(np.arange(4),["2D stock","2D fitted","3D stock","3D fitted"]); ax.set_ylabel("Mean validation RMSE (eV, log scale)"); fig.tight_layout(); fig.savefig(OUT/"stock_vs_fitted.pdf"); plt.close(fig)
for name,rows,label in [("2d_ablation",c2,"2D"),("3d_ablation",j3,"3D")]:
    x=vals(rows,"nogap_rmse_eV"); y=vals(rows,"constrained_rmse_eV"); lo=min(x.min(),y.min())*.9; hi=max(x.max(),y.max())*1.06
    fig,ax=plt.subplots(figsize=(6,5)); ax.scatter(x,y); ax.plot([lo,hi],[lo,hi],"--"); ax.set_xlim(lo,hi); ax.set_ylim(lo,hi); ax.set_xlabel("Validation RMSE without gap term (eV)"); ax.set_ylabel("Validation RMSE with gap constraint (eV)"); ax.set_title(label); fig.tight_layout(); fig.savefig(OUT/f"{name}.pdf"); plt.close(fig)
data=[vals(c2,"nogap_rmse_eV"),vals(c2,"constrained_rmse_eV"),vals(j3,"nogap_rmse_eV"),vals(j3,"constrained_rmse_eV")]
fig,ax=plt.subplots(figsize=(7.2,5)); ax.boxplot(data,tick_labels=["2D\nno gap","2D\ngap","3D\nno gap","3D\ngap"],showmeans=True); ax.set_ylabel("Validation RMSE (eV)"); fig.tight_layout(); fig.savefig(OUT/"dimension_summary.pdf"); plt.close(fig)
x=np.arange(len(tmd)); w=.25; fig,ax=plt.subplots(figsize=(8.4,4.8)); ax.bar(x-w,vals(tmd,"individual_rmse_eV"),width=w,label="Individual"); ax.bar(x,vals(tmd,"naive_rmse_eV"),width=w,label="Naive transfer"); ax.bar(x+w,vals(tmd,"shared_rmse_eV"),width=w,label="Shared CV"); ax.set_xticks(x,["MoS2","WS2","MoSe2","WSe2","MoTe2","WTe2"],rotation=25); ax.set_ylabel("Validation RMSE (eV)"); ax.legend(); fig.tight_layout(); fig.savefig(OUT/"tmd_transferability.pdf"); plt.close(fig)
print(f"Wrote lightweight figures to {OUT}")
