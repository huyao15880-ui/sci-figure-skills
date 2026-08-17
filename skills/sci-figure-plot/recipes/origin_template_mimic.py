"""XAFS recipe 08 — mimic the group's prior-art Origin template.

Reproduces the style spec extracted from data/raw/Figure/*.wmf
(docs/ORIGIN_TEMPLATE_SPEC.md): blue-data / red-fit pairing, 1.5-2 pt
solid lines, four-frame inward-tick axes for fit panels, open frame for
XANES, prior-art axis title wording, jet wavelet (with viridis variant
per colour discipline). Data: our Pt_sample (Pt-sample.prj), fit curve
from the configurable engine - i.e. the mimic is applied to OUR analysis,
proving the template is fully transferable.

Run:  python origin_template_mimic.py
"""
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from larch import Group
from larch.io import read_athena
from larch.xafs import autobk, xftf, cauchy_wavelet

import xafs_feffit_pt_configurable as engine

HERE = Path(__file__).parent
MM = 1 / 25.4
BLUE, RED = "#1F77B4", "#D62728"          # prior-art pairing

prj = read_athena(str(HERE / "data" / "Pt-sample.prj"))
s, f = prj.Pt_sample, prj.Pt_Foil
autobk(s, e0=s.e0, rbkg=1.0, kweight=2)
xftf(s, kmin=3.0, kmax=11.5, dk=1.0, kweight=2, window="kaiser")
chir_mag = np.hypot(s.chir_re, s.chir_im)

res = engine.do_fit(engine.get_args([]))       # fit under report conditions
dm = res["dset"].model

g = Group()
cauchy_wavelet(k=s.k, chi=s.chi, group=g, kweight=2, rmax_out=5.0)
kgrid = s.k[: g.wcauchy_mag.shape[1]]

mpl.rcParams.update({
    "font.family": "Arial", "font.size": 8,
    "axes.labelsize": 9, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.linewidth": 1.0, "pdf.fonttype": 42,
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.top": True, "ytick.right": True,
    "xtick.major.size": 4, "ytick.major.size": 4,
    "xtick.major.width": 1.0, "ytick.major.width": 1.0,
})

fig, axes = plt.subplots(2, 2, figsize=(183 * MM, 130 * MM),
                         constrained_layout=True)
fig.get_layout_engine().set(w_pad=2 * MM, h_pad=2 * MM, wspace=0.08, hspace=0.10)

# (a) XANES - open frame, prior-art wording
ax = axes[0, 0]
ax.spines[:].set_visible(False)
ax.spines["left"].set_visible(True)
ax.spines["bottom"].set_visible(True)
ax.tick_params(top=False, right=False)
ax.plot(f.energy, f.norm, color="#7F7F7F", lw=1.5, label="Pt foil")
ax.plot(s.energy, s.norm, color=BLUE, lw=1.8, label="Pt sample")
ax.set_xlim(11560, 11700)
ax.set_ylim(0, 1.6)
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("Normalized " + chr(956) + "(E)")
ax.legend(loc="upper left", frameon=False, fontsize=7.5)
ax.set_title("a", loc="left", fontweight="bold", fontsize=8, pad=3)

# (b) k-space fit pairing
ax = axes[0, 1]
m = s.k <= 12
ax.plot(s.k[m], s.k[m] ** 2 * s.chi[m], color=BLUE, lw=1.6)
ax.plot(dm.k, dm.k ** 2 * dm.chi, color=RED, lw=1.6)
ax.set_xlim(0, 12.5)
ax.set_xlabel("k (" + chr(197) + "$^{-1}$)")
ax.set_ylabel("k$^2$" + chr(967) + "(k)")
ax.legend(handles=[plt.Line2D([], [], color=BLUE, label="data"),
                   plt.Line2D([], [], color=RED, label="fit")],
          loc="upper right", frameon=False, fontsize=7.5)
ax.set_title("b", loc="left", fontweight="bold", fontsize=8, pad=3)

# (c) R-space fit with prior-art axis wording + annotation box
ax = axes[1, 0]
d_ = res["dset"].data
ax.plot(d_.r, d_.chir_mag, color=BLUE, lw=1.6, label="data")
ax.plot(dm.r, dm.chir_mag, color=RED, lw=1.6, label="fit")
ax.text(0.97, 0.95,
        f"CN = {res['CN']:.1f}\nR = {res['R']:.2f} " + chr(197) +
        f"\nR$_f$ = {res['rfactor']:.3f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=7.5,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#999999", lw=0.6))
ax.set_xlim(0, 4)
ax.set_ylim(0, d_.chir_mag.max() * 1.12)
ax.set_xlabel("R (" + chr(197) + ")")
ax.set_ylabel("|" + chr(967) + "(R)| Fourier Transform Magnitude")
ax.legend(loc="upper right", frameon=False, fontsize=7.5)
ax.set_title("c", loc="left", fontweight="bold", fontsize=8, pad=3)

# (d) wavelet - prior-art jet + discipline viridis twin inset
ax = axes[1, 1]
K, R = np.meshgrid(kgrid, g.wcauchy_r)
pc = ax.pcolormesh(K, R, g.wcauchy_mag, cmap="jet", shading="auto",
                   rasterized=True)
ax.set_xlim(0, 12)
ax.set_ylim(0, 5)
ax.set_xlabel("k (" + chr(197) + "$^{-1}$)")
ax.set_ylabel("R (" + chr(197) + ")")
cb = fig.colorbar(pc, ax=ax, fraction=0.05, pad=0.02)
cb.ax.tick_params(labelsize=7, width=0.8)
cb.set_label("|W(k,R)|", fontsize=8)
ax.set_title("d (jet, prior-art)", loc="center", fontsize=8, pad=3)
ax.set_title("d", loc="left", fontweight="bold", fontsize=8, pad=3)

out = HERE / "xafs_prior_art_template_mimic"
fig.savefig(out.with_suffix(".pdf"))
fig.savefig(out.with_suffix(".png"), dpi=600)
print(f"[saved] {out.name}.pdf/.png  page=183x130 mm  "
      f"(style: docs/ORIGIN_TEMPLATE_SPEC.md)")
