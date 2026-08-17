"""XAFS recipe 11 — polished template figures (response to 'still ugly').

Art-director fixes applied STRUCTURALLY (no pixel nudging):
- crop dead margins / sane aspect (183 x ~80 mm per panel)
- line weight 0.5 -> 2 pt equivalent; desaturated professional palette
- clear type hierarchy (ticks/labels/titles)
- frameless legend; longer ticks; tidy spines
Two outputs: matplotlib polished quad + refreshed Origin .opju template
with deep LabTalk styling (page aspect, line width, font sizes).

Run:  python xafs_polished_template.py
"""
from pathlib import Path
import subprocess
import sys

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from larch import Group
from larch.io import read_athena
from larch.xafs import autobk, xftf, cauchy_wavelet

import xafs_multishell_fit as ms            # winning fit (Rf 0.0169)

HERE = Path(__file__).parent
MM = 1 / 25.4
NAVY = "#2C5F8A"        # desaturated data blue
CRIM = "#B0413E"        # desaturated fit red
GOLD = "#C89F5A"        # standard/reference accent
INK = "#1A1A1A"

prj = read_athena(str(HERE / "data" / "Pt-sample.prj"))
s, f = prj.Pt_sample, prj.Pt_Foil
autobk(s, e0=s.e0, rbkg=1.25, kweight=2)
xftf(s, kmin=3.0, kmax=11.5, dk=1.0, kweight=2, window="kaiser")
g = Group()
cauchy_wavelet(k=s.k, chi=s.chi, group=g, kweight=2, rmax_out=5.0)
kgrid = s.k[: g.wcauchy_mag.shape[1]]
d, m = ms.d, ms.m

# ============================ matplotlib polished ============================
mpl.rcParams.update({
    "font.family": "Arial", "font.size": 7,
    "axes.labelsize": 8, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "axes.linewidth": 0.8, "pdf.fonttype": 42,
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic",
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.major.size": 3.2, "ytick.major.size": 3.2,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8,
    "xtick.top": True, "ytick.right": True,
    "legend.frameon": False,
})

fig, axes = plt.subplots(1, 3, figsize=(183 * MM, 64 * MM),
                         constrained_layout=True)
fig.get_layout_engine().set(w_pad=3 * MM, h_pad=2 * MM, wspace=0.05)

# (a) XANES
ax = axes[0]
ax.plot(f.energy, f.norm, color=GOLD, lw=1.1, label="Pt foil")
ax.plot(s.energy, s.norm, color=NAVY, lw=1.5, label="Pt single-atom")
ax.set_xlim(11560, 11700); ax.set_ylim(0, 1.6)
ax.set_xticks(range(11560, 11701, 50)); ax.set_yticks(np.arange(0, 1.61, 0.4))
ax.set_xlabel("Energy (eV)"); ax.set_ylabel("Normalized " + chr(956) + "(E)")
ax.legend(loc="upper left", handlelength=1.6)
ax.set_title("a", loc="left", fontweight="bold", fontsize=8, pad=4)

# (b) R-space fit (winning two-shell)
ax = axes[1]
ax.plot(d.r, d.chir_mag, color=NAVY, lw=1.5, label="data")
ax.fill_between(d.r, d.chir_mag, color=NAVY, alpha=0.08, lw=0)
ax.plot(m.r, m.chir_mag, color=CRIM, lw=1.7, ls=(0, (4, 1.5)), label="fit")
ax.axvspan(1.0, 3.2, color="#B9C6D2", alpha=0.18, lw=0)
ax.set_xlim(0, 4.2); ax.set_ylim(0, d.chir_mag.max() * 1.08)
ax.set_xlabel("R (" + chr(197) + ")")
ax.set_ylabel("|" + chr(967) + "(R)|")
ax.legend(loc="upper right", handlelength=2.2)
ax.text(0.03, 0.95, f"R$_f$ = {ms.out.rfactor:.3f}", transform=ax.transAxes,
        fontsize=6.5, va="top", color="#555555")
ax.set_title("b", loc="left", fontweight="bold", fontsize=8, pad=4)

# (c) wavelet
ax = axes[2]
K, R = np.meshgrid(kgrid, g.wcauchy_r)
pc = ax.pcolormesh(K, R, g.wcauchy_mag, cmap="viridis", shading="auto",
                   rasterized=True)
ax.set_xlim(0, 12); ax.set_ylim(0, 4.5)
ax.set_xlabel("k (" + chr(197) + "$^{-1}$)"); ax.set_ylabel("R (" + chr(197) + ")")
cb = fig.colorbar(pc, ax=ax, fraction=0.045, pad=0.02)
cb.ax.tick_params(labelsize=6, width=0.6)
cb.outline.set_linewidth(0.5)
ax.set_title("c", loc="left", fontweight="bold", fontsize=8, pad=4)

out = HERE / "xafs_polished_triptych"
fig.savefig(out.with_suffix(".pdf"))
fig.savefig(out.with_suffix(".png"), dpi=600)
print("[saved]", out.name)

# ============================ Origin opju restyle ============================
import originpro as op
from larch.fitting import param  # noqa (recipe import hygiene)

OPJU = HERE / "xafs_group_template.opju"
ok = False
try:
    wb = op.new_book("w", "XAFS")
    sh = wb[0]
    sh.from_list(0, list(f.energy), lname="EFoil", units="eV", axis="X")
    sh.from_list(1, list(f.norm), lname="Pt foil", axis="Y")
    sh.from_list(2, list(s.energy), lname="ESample", units="eV", axis="X")
    sh.from_list(3, list(s.norm), lname="Pt single-atom", axis="Y")
    wb2 = op.new_book("w", "RSpace")
    sh2 = wb2[0]
    sh2.from_list(0, list(d.r), lname="R", units="A", axis="X")
    sh2.from_list(1, list(d.chir_mag), lname="Data", axis="Y")
    sh2.from_list(2, list(m.r), lname="Rfit", units="A", axis="X")
    sh2.from_list(3, list(m.chir_mag), lname="Fit", axis="Y")

    def lt(c, tag, must=True):
        r = op.lt_exec(c)
        if r is True or r == 0 or r is None:
            print("[lt OK]", tag)
        else:
            print("[lt", r, "]", tag)
            if must:
                raise RuntimeError(tag)

    # Graph1: XANES
    lt('plotxy iy:=[XAFS]Sheet1!2 plot:=200;', "g1 c1")
    lt('plotxy iy:=[XAFS]Sheet1!4 ogl:=[Graph1];', "g1 c2")
    lt('layer -a;', "g1 autoscale")
    lt('layer.x.title$="Energy (eV)";', "g1 x")
    lt('layer.y.title$="Normalized \\g(m)(E)";', "g1 y")
    lt('layer.x.from=11560; layer.x.to=11700; layer.x.by=50;', "g1 xr")
    lt('layer.y.from=0; layer.y.to=1.6; layer.y.by=0.4;', "g1 yr")
    lt('legend -s u;', "g1 legend")
    # Graph2: R-space fit
    lt('plotxy iy:=[RSpace]Sheet1!2 plot:=200;', "g2 c1")
    lt('plotxy iy:=[RSpace]Sheet1!4 ogl:=[Graph2];', "g2 c2")
    lt('layer -a;', "g2 autoscale")
    lt('layer.x.title$="R (\\+3135)";', "g2 x")
    lt('layer.y.title$="|\\g(c)(R)|";', "g2 y")
    lt('layer.x.from=0; layer.x.to=4.2; layer.x.by=1;', "g2 xr")
    lt('legend -s u;', "g2 legend")

    # ---- deep styling loop: both graphs -------------------------------
    for gname in ("Graph1", "Graph2"):
        lt(f'win -a {gname};', f"{gname} activate")
        # page aspect ~183:80mm -> Origin default units (inch-like x 0.1)
        lt(f'{gname}.page.width=73;', f"{gname} page w", must=False)
        lt(f'{gname}.page.height=32;', f"{gname} page h", must=False)
        # thicker frame + longer ticks + bigger fonts
        lt('layer.axislinewidth=1.5;', f"{gname} frame w", must=False)
        lt('layer.x.ticks.majorlength=5; layer.y.ticks.majorlength=5;',
           f"{gname} tick len", must=False)
        lt('layer.x.ticklblsize=18; layer.y.ticklblsize=18;',
           f"{gname} tick font", must=False)
        lt('layer.x.titlesize=22; layer.y.titlesize=22;',
           f"{gname} title font", must=False)
        # plot styling: weight + colors via plot list
        lt('set %C -w 200; set %C -cl 18;', f"{gname} last plot", must=False)
    # Graph1: navy data (custom), Graph2: navy data + crimson fit
    lt('win -a Graph1; set %C -c 4;', "g1 sample blue", must=False)
    lt('win -a Graph2; set %C -c 2;', "g2 fit red", must=False)

    op.save(str(OPJU))
    print("[saved]", OPJU.name)
    ok = True
finally:
    op.exit()
sys.exit(0 if ok else 1)
