"""XAFS recipe 10 — multi-shell fit: fix the 'fit looks bad' problem.

The single Pt-N path fit only covers R 1.0-2.2; the high-shell structure
(~2.58 A unphased) is unmodelled, leaving the red fit flat where data has
structure. This recipe builds a two-shell FEFF cluster (4 N @ 2.02 A +
2 C @ 3.0 A second shell), fits BOTH paths over the report window
(R 1.0-3.2, k 3-11.5, kw 2), and verifies visual contact across the
full R range. Use its output to refresh the .opju template Graph2.

Run:  python xafs_multishell_fit.py
"""
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from larch import Group
from larch.io import read_athena
from larch.xafs import (autobk, xftf, feffpath, feffit_transform,
                        feffit_dataset, feffit, feffit_report)
from larch.xafs.feffrunner import FeffRunner
from larch.fitting import param, guess

HERE = Path(__file__).parent
WORK = HERE / "feff_cache" / "ptn4_c2_second"
MM = 1 / 25.4
MINUS = "\u2212"

# ---- 1. two-shell cluster: 4N@2.02 (square planar) + 2C@3.0 (z-axis) -------
if not list(WORK.glob("feff*.dat")):
    WORK.mkdir(parents=True, exist_ok=True)
    xy = 2.02 / np.sqrt(2)
    atoms = [(0, 0, 0, 0, "Pt"),
             (xy, xy, 0, 1, "N"), (-xy, xy, 0, 1, "N"),
             (xy, -xy, 0, 1, "N"), (-xy, -xy, 0, 1, "N"),
             (0, 0, 3.0, 2, "C"), (0, 0, -3.0, 2, "C")]
    lines = ["TITLE Pt-N4 + second-shell C2", "HOLE 4 1.0",
             "CONTROL 1 1 1 1", "PRINT 0 0 0 0", "POTENTIALS",
             "  0  78", "  1   7", "  2   6", "ATOMS"]
    lines += [f"{x:9.4f} {y:9.4f} {z:9.4f}   {ip}   {t}"
              for x, y, z, ip, t in atoms]
    (WORK / "feff.inp").write_text("\n".join(lines) + "\n", encoding="ascii")
    FeffRunner(feffinp="feff.inp", folder=str(WORK)).run(exe="feff6l")
paths = sorted(WORK.glob("feff*.dat"))
print("feff paths:", [p.name for p in paths])

# ---- 2. data ------------------------------------------------------------------
prj = read_athena(str(HERE / "data" / "Pt-sample.prj"))
s = prj.Pt_sample
# rbkg sensitivity (0.8/1.0/1.25/1.5 swept): 1.25-1.3 optimal (Rf 0.0169);
# 1.25 is the Athena default the original report likely used
autobk(s, e0=s.e0, rbkg=1.25, kweight=2)
xftf(s, kmin=3.0, kmax=11.5, dk=1.0, kweight=2, window="kaiser")

# ---- 3. two-path fit over the REPORT window -----------------------------------
pN = feffpath(str(paths[0]), s02="ampN", e0="del_e0",
              sigma2="sigN", deltar="delrN")      # shortest = N @ 2.02
pC = feffpath(str(paths[1]), s02="ampC", e0="del_e0",
              sigma2="sigC", deltar="alpha*reff")  # second shell C @ 3.0
trans = feffit_transform(kmin=3.0, kmax=11.5, kw=2, dk=1.0,
                         window="kaiser", rmin=1.0, rmax=3.2)
pars = Group(ampN=guess(0.9, min=0.2, max=1.6),
             ampC=guess(0.5, min=0.0, max=1.6),
             del_e0=guess(0.0, min=-15, max=15),
             sigN=guess(0.004, min=0, max=0.02),
             sigC=guess(0.008, min=0, max=0.02),  # free: Rf 0.0169 < 0.02
             delrN=guess(0.0, min=-0.1, max=0.1),
             alpha=guess(0.0, min=-0.04, max=0.04))
dset = feffit_dataset(data=s, paths={"PtN": pN, "C2": pC}, transform=trans)
out = feffit(pars, dset)
print(feffit_report(out)[-1500:])

p = out.params
cn_N = p["ampN"].value * pN.degen
cn_C = p["ampC"].value * pC.degen
r_N = pN.reff + p["delrN"].value
r_C = pC.reff * (1 + p["alpha"].value)
print(f"\n==== two-shell result ====")
print(f"shell1 Pt-N: CN={cn_N:.2f}  R={r_N:.3f} A  "
      f"sig2={p['sigN'].value:.4f}")
print(f"shell2 C   : CN={cn_C:.2f}  R={r_C:.3f} A  "
      f"sig2={p['sigC'].value:.4f}")
print(f"dE0={p['del_e0'].value:.1f}  Rf={out.rfactor:.4f} "
      f"(single-shell was 0.0255)")

d, m = dset.data, dset.model
for lo, hi in ((1.0, 2.2), (2.2, 3.2)):
    mm = (d.r >= lo) & (d.r < hi)
    rr = np.sum((d.chir_mag[mm] - m.chir_mag[mm])**2) / np.sum(d.chir_mag[mm]**2)
    print(f"residual R {lo}-{hi}: {rr:.3f}")

# ---- 4. full-range contact figure --------------------------------------------
mpl.rcParams.update({
    "font.family": "Arial", "font.size": 8,
    "axes.labelsize": 9, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.linewidth": 1.0, "pdf.fonttype": 42,
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.top": True, "ytick.right": True,
    "legend.frameon": False,
})
BLUE, RED = "#1F77B4", "#D62728"
fig, axes = plt.subplots(1, 2, figsize=(183 * MM, 75 * MM), constrained_layout=True)
fig.get_layout_engine().set(w_pad=2 * MM, h_pad=2 * MM, wspace=0.06)

ax = axes[0]
ax.plot(s.k, s.k**2 * s.chi, color=BLUE, lw=1.2, label="data")
mmk = s.k <= 12
ax.plot(m.k, m.k**2 * m.chi, color=RED, lw=1.4, label="2-shell fit")
ax.set_xlim(0, 12.5)
ax.set_xlabel("k (" + chr(197) + "$^{-1}$)")
ax.set_ylabel("k$^2$" + chr(967) + "(k)")
ax.legend(loc="upper right")
ax.set_title("a", loc="left", fontweight="bold", fontsize=8, pad=3)

ax = axes[1]
ax.plot(d.r, d.chir_mag, color=BLUE, lw=1.4, label="data")
ax.plot(m.r, m.chir_mag, color=RED, lw=1.4, label="2-shell fit")
ax.axvspan(1.0, 3.2, color="#999999", alpha=0.10, lw=0)
ax.text(3.35, d.chir_mag.max() * 0.95,
        f"Pt-N: CN={cn_N:.1f}, R={r_N:.2f} " + chr(197) + "\n"
        f"C: CN={cn_C:.1f}, R={r_C:.2f} " + chr(197) + "\n"
        f"R$_f$ = {out.rfactor:.3f}", fontsize=7.5, va="top")
ax.set_xlim(0, 4.5)
ax.set_ylim(0, d.chir_mag.max() * 1.1)
ax.set_xlabel("R (" + chr(197) + ")")
ax.set_ylabel("|" + chr(967) + "(R)| Fourier Transform Magnitude")
ax.legend(loc="upper right")
ax.set_title("b", loc="left", fontweight="bold", fontsize=8, pad=3)

outfig = HERE / "xafs_multishell_fit"
fig.savefig(outfig.with_suffix(".pdf"))
fig.savefig(outfig.with_suffix(".png"), dpi=600)
print(f"[saved] {outfig.name}.pdf/.png")
