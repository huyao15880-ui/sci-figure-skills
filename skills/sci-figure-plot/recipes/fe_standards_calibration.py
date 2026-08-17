"""XAFS recipe 13 — Fe K-edge standards suite (the other half of the work).

The provider's full package includes an Fe-line Athena project
(Fe_foil / FeO / Fe3O4 / Fe2O3) alongside the Pt one. This recipe covers
the Fe-line method stack we had not practised:
  (a) standards XANES overlay + edge zoom with E0 markers
  (b) edge-energy vs valence calibration curve (Fe0 7112.0 ->
      Fe2+ 7119.5 -> Fe3O4 7124.0 -> Fe3+ 7126.0)
  (c) first-derivative overlay (white-line/edge shapes)
  (d) LCF self-consistency check: synthesize 70% FeO + 30% Fe2O3, NNLS
      must recover the mix (math validation, stated as synthetic)

Run:  python fe_standards_calibration.py
Data: data/fe_standards.prj (user-provided Athena project)
"""
from pathlib import Path

import numpy as np
from scipy.optimize import nnls
import matplotlib as mpl
import matplotlib.pyplot as plt
from larch.io import read_athena

HERE = Path(__file__).parent
MM = 1 / 25.4
MINUS = "\u2212"

prj = read_athena(str(HERE / "data" / "fe_standards.prj"))
SUITE = ["Fe_foil", "FeO", "Fe3O4", "Fe2O3"]
VALENCE = {"Fe_foil": 0, "FeO": 2, "Fe3O4": 8 / 3, "Fe2O3": 3}
LABEL = {"Fe_foil": "Fe foil (Fe" + chr(8304) + ")",
         "FeO": "FeO (Fe" + chr(178) + "+)",
         "Fe3O4": "Fe" + chr(8323) + "O" + chr(8324) + " (Fe" + chr(178) + "+/Fe" + chr(179) + "+)",
         "Fe2O3": "Fe" + chr(8322) + "O" + chr(8323) + " (Fe" + chr(179) + "+)"}
COLORS = {"Fe_foil": "#5F6368", "FeO": "#2C5F8A", "Fe3O4": "#C89F5A",
          "Fe2O3": "#B0413E"}

groups = {n: getattr(prj, n) for n in SUITE}
for n, g in groups.items():
    print(f"{n}: E0={g.e0:.1f} eV, valence {VALENCE[n]:.2f}")

# ---- (d) LCF self-consistency on synthetic mix ------------------------------
q = groups["FeO"]
m = (q.energy > q.e0 - 30) & (q.energy < q.e0 + 80)
E = q.energy[m]
A = np.vstack([np.interp(E, groups[k].energy, groups[k].norm)
               for k in SUITE]).T
true_w = np.array([0.0, 0.70, 0.0, 0.30])
y = A @ true_w
w, _ = nnls(A, y)
print("LCF recovery (synthetic 70% FeO + 30% Fe2O3):",
      {k: round(v, 3) for k, v in zip(SUITE, w)})

# ---- figure -------------------------------------------------------------------
mpl.rcParams.update({
    "font.family": "Arial", "font.size": 7,
    "axes.labelsize": 8, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "axes.linewidth": 0.8, "pdf.fonttype": 42,
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.major.size": 3.2, "ytick.major.size": 3.2,
    "xtick.top": True, "ytick.right": True,
    "legend.frameon": False,
})

fig, axes = plt.subplots(1, 3, figsize=(183 * MM, 62 * MM),
                         constrained_layout=True)
fig.get_layout_engine().set(w_pad=3 * MM, h_pad=2 * MM, wspace=0.05)

# (a) XANES overlay + edge zoom inset
ax = axes[0]
for n in SUITE:
    g = groups[n]
    ax.plot(g.energy, g.norm, color=COLORS[n], lw=1.4, label=LABEL[n])
ax.set_xlim(7100, 7250)
ax.set_ylim(0, 1.9)
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("Normalized " + chr(956) + "(E)")
ax.legend(loc="upper right", fontsize=6.2, handlelength=1.5)
ax.set_title("a", loc="left", fontweight="bold", fontsize=8, pad=4)

# (b) edge shift vs valence calibration
ax = axes[1]
vx = [VALENCE[n] for n in SUITE]
ey = [groups[n].e0 for n in SUITE]
coef = np.polyfit(vx, ey, 1)
xx = np.linspace(-0.1, 3.2, 50)
for n in SUITE:
    ax.scatter(VALENCE[n], groups[n].e0, color=COLORS[n], s=26, zorder=3,
               edgecolor="white", linewidth=0.5)
ax.plot(xx, np.polyval(coef, xx), color="#7F7F7F", lw=0.9, ls=(0, (4, 2)))
ax.text(0.05, 0.08,
        f"{coef[0]:.1f} eV per valence unit\n"
        f"R² = {np.corrcoef(vx, ey)[0,1]**2:.3f}",
        transform=ax.transAxes, fontsize=7, va="bottom")
ax.set_xlim(-0.2, 3.3)
ax.set_xlabel("Fe oxidation state")
ax.set_ylabel("E$_0$ (eV)")
ax.set_title("b", loc="left", fontweight="bold", fontsize=8, pad=4)

# (c) first derivatives
ax = axes[2]
for n in SUITE:
    g = groups[n]
    d = np.gradient(g.norm, g.energy)
    ax.plot(g.energy, d, color=COLORS[n], lw=1.1, label=LABEL[n])
ax.set_xlim(7108, 7140)
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("d" + chr(956) + "/dE (eV" + MINUS + "$^{1}$)")
ax.legend(loc="upper right", fontsize=6.2, handlelength=1.5)
ax.set_title("c", loc="left", fontweight="bold", fontsize=8, pad=4)

out = HERE / "fe_standards_calibration"
fig.savefig(out.with_suffix(".pdf"))
fig.savefig(out.with_suffix(".png"), dpi=600)
print(f"[saved] {out.name}.pdf/.png  page=183x62 mm")
