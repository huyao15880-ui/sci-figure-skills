"""XAFS recipe 03 — Cauchy continuous wavelet transform (Pt foil L3-edge).

Cauchy CCWT after Munoz, Argoul & Farges: expands chi(k) in the (k, R)
plane so backscatterer signatures separate. For Pt metal the wavelet
should peak at the Pt-Pt distance (phase-corrected ~2.77 A; raw FT
peak ~2.45 A).

Run:  python xafs_wavelet_ptfoil.py
Data: data/pt_metal_rt.xdi (upstream xraylarch examples, MIT)
"""
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from larch import Group
from larch.io import read_ascii
from larch.xafs import pre_edge, autobk, cauchy_wavelet

HERE = Path(__file__).parent
MM = 1 / 25.4

d = read_ascii(str(HERE / "data" / "pt_metal_rt.xdi"))
d.mu = -np.log(d.itrans / d.i0)
pre_edge(d, e0=None)
autobk(d, rbkg=1.25, kweight=2)

g = Group()
cauchy_wavelet(k=d.k, chi=d.chi, group=g, kweight=2, rmax_out=6.0)

kgrid = d.k[: g.wcauchy_mag.shape[1]]      # columns follow input k
K, R = np.meshgrid(kgrid, g.wcauchy_r)
W = g.wcauchy_mag

ir, ik = np.unravel_index(np.nanargmax(W), W.shape)
print(f"wavelet max at R = {g.wcauchy_r[ir]:.2f} A, k = {kgrid[ik]:.1f} A^-1")
print(f"raw FT first-shell peak ~2.45 A; phase-corrected Pt-Pt = 2.77 A")

mpl.rcParams.update({
    "font.family": "Arial", "font.size": 6.0,
    "axes.labelsize": 6.5, "xtick.labelsize": 5.5, "ytick.labelsize": 5.5,
    "axes.linewidth": 0.4, "pdf.fonttype": 42,
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
    "axes.spines.top": False, "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(89 * MM, 78 * MM), constrained_layout=True)
pc = ax.pcolormesh(K, R, W, cmap="viridis", shading="auto",
                   rasterized=True)
ax.set_xlim(0, 12)
ax.set_ylim(0, 6)
ax.set_xlabel("k (" + chr(197) + "$^{-1}$)")
ax.set_ylabel("R (" + chr(197) + ")")
ax.set_title("Cauchy wavelet |W(k,R)|, Pt foil L$_3$",
             loc="center", fontsize=6.5, pad=3)
cb = fig.colorbar(pc, ax=ax, fraction=0.05, pad=0.02)
cb.set_label("|W(k,R)|", fontsize=6.0)
cb.ax.tick_params(labelsize=5.5, width=0.4, length=2.0)
cb.outline.set_linewidth(0.4)

out = HERE / "xafs_wavelet_ptfoil"
fig.savefig(out.with_suffix(".pdf"))
fig.savefig(out.with_suffix(".png"), dpi=600)
print(f"[saved] {out.name}.pdf/.png  page=89x78 mm (single column)")
