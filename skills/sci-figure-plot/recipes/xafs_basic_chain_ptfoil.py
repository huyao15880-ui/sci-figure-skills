"""XAFS recipe 01 — Pt foil L3-edge standard chain + publication triptych.

Larch chain: read_ascii -> pre_edge -> autobk -> xftf (k-weight 2,
k 3-11.5, mirroring the Pt L3-edge fitting conditions used for the
single-atom catalyst report). Plot follows repo plotting discipline
(final-coordinate 183 mm page, Arial, U+2212, pdf.fonttype 42).

Run:  python xafs_basic_chain_ptfoil.py
Data: data/pt_metal_rt.xdi (upstream xraylarch examples, MIT)
"""
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from larch.io import read_ascii
from larch.xafs import pre_edge, autobk, xftf

HERE = Path(__file__).parent
MM = 1 / 25.4
MINUS = "\u2212"

# ---- 1. processing chain --------------------------------------------------
d = read_ascii(str(HERE / "data" / "pt_metal_rt.xdi"))
d.mu = -np.log(d.itrans / d.i0)           # transmission: mu = -ln(I/I0)
pre_edge(d, e0=None)                      # auto E0 + normalization
autobk(d, rbkg=1.25, kweight=2)           # mu(E) -> chi(k)
xftf(d, kmin=3.0, kmax=11.5, dk=1.0,
     kweight=2, window="kaiser")          # chi(k) -> chi(R)

print(f"E0 = {d.e0:.1f} eV (Pt L3 reference: 11564 eV)")
print(f"edge step = {d.edge_step:.3f}; norm points = {len(d.norm)}")
print(f"autobk rbkg = 1.25 A; R-grid max = {d.r.max():.2f} A")
# rough first-shell peak from |chi(R)|
mask = (d.r > 1.5) & (d.r < 3.5)
r_peak = d.r[mask][np.argmax(np.hypot(d.chir_re, d.chir_im)[mask])]
print(f"first |chi(R)| peak at R = {r_peak:.2f} A "
      f"(+0.3-0.5 A phase correction -> true Pt-Pt ~ 2.77 A)")

# ---- 2. triptych at final size --------------------------------------------
mpl.rcParams.update({
    "font.family": "Arial", "font.size": 6.0,
    "axes.labelsize": 6.5, "xtick.labelsize": 5.5, "ytick.labelsize": 5.5,
    "axes.linewidth": 0.4, "pdf.fonttype": 42,
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
    "axes.spines.top": False, "axes.spines.right": False,
})

fig, axes = plt.subplots(1, 3, figsize=(183 * MM, 62 * MM),
                         constrained_layout=True)
fig.get_layout_engine().set(w_pad=1.6 * MM, h_pad=1.6 * MM, wspace=0.06)

ax = axes[0]
ax.plot(d.energy, d.norm, color="#0072B2", lw=0.8)
ax.axvline(d.e0, color="#666666", lw=0.6, ls="--")
ax.text(d.e0 + 30, 0.35, f"E$_0$ = {d.e0:.0f} eV", fontsize=5.5)
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("Normalized " + chr(956) + "(E)")
ax.set_xlim(d.e0 - 200, d.e0 + 800)
ax.set_title("a", loc="left", fontweight="bold", fontsize=8, pad=3)
ax.set_title("XANES", loc="center", fontsize=6.5, pad=3)

ax = axes[1]
ax.plot(d.k, d.k**2 * d.chi, color="#D55E00", lw=0.6)
ax.set_xlim(0, 12.5)
ax.set_xlabel("k (" + chr(197) + MINUS + "$^{1}$)")
ax.set_ylabel("k$^2$" + chr(967) + "(k)")
ax.set_title("b", loc="left", fontweight="bold", fontsize=8, pad=3)
ax.set_title("k$^2$-weighted EXAFS", loc="center", fontsize=6.5, pad=3)

ax = axes[2]
chir_mag = np.hypot(d.chir_re, d.chir_im)
ax.plot(d.r, chir_mag, color="#0072B2", lw=0.9, label="|" + chr(967) + "(R)|")
ax.plot(d.r, d.chir_re, color="#D55E00", lw=0.6, alpha=0.8,
        label="Re " + chr(967) + "(R)")
ax.axvspan(1.0, 3.2, color="#999999", alpha=0.10, lw=0)
ax.set_xlim(0, 6)
ax.set_ylim(-6, 10)
ax.set_xlabel("R (" + chr(197) + ")")
ax.set_ylabel("Fourier transform magnitude")
ax.legend(loc="upper right")
ax.set_title("c", loc="left", fontweight="bold", fontsize=8, pad=3)
ax.set_title("|" + chr(967) + "(R)|, k-weight 2, k 3" + MINUS + "11.5",
             loc="center", fontsize=6.5, pad=3)

out = HERE / "xafs_basic_chain_ptfoil"
fig.savefig(out.with_suffix(".pdf"))
fig.savefig(out.with_suffix(".png"), dpi=600)
print(f"[saved] {out.name}.pdf/.png  page=183x62 mm")
