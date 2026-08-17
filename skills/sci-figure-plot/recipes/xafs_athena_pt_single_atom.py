"""XAFS recipe 04 — Pt single-atom catalyst from Athena project (Pt-sample.prj).

Reproduces the XANES/EXAFS evidence chain for the Pt single-atom sample:
edge shift vs valence standards (Pt foil / PtO / PtO2), chi(k), R-space
with the single-atom criterion (first shell Pt-C/N near 2 A phase-
corrected; no Pt-Pt metal path at ~2.7 A).

Data: data/Pt-sample.prj (user-provided Athena project; local, not
redistributed beyond this repo owner's machine).
Run:   python xafs_athena_pt_single_atom.py
"""
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from larch.io import read_athena
from larch.xafs import autobk, xftf

HERE = Path(__file__).parent
MM = 1 / 25.4
MINUS = "\u2212"

prj = read_athena(str(HERE / "data" / "Pt-sample.prj"))
groups = {n: getattr(prj, n) for n in ("Pt_sample", "Pt_Foil", "PtO", "PtO2")}

edge_shift = groups["Pt_sample"].e0 - groups["Pt_Foil"].e0
print(f"E0: sample {groups['Pt_sample'].e0:.1f}, foil {groups['Pt_Foil'].e0:.1f}, "
      f"PtO {groups['PtO'].e0:.1f}, PtO2 {groups['PtO2'].e0:.1f} eV")
print(f"edge shift vs Pt foil = {edge_shift:+.1f} eV (positive -> Pt delta+)")

s = groups["Pt_sample"]
autobk(s, e0=s.e0, rbkg=1.0, kweight=2)
xftf(s, kmin=3.0, kmax=11.5, dk=1.0, kweight=2, window="kaiser")
chir_mag = np.hypot(s.chir_re, s.chir_im)

# --- Pt foil control through the IDENTICAL chain: where does Pt-Pt sit? ---
foil = groups["Pt_Foil"]
autobk(foil, e0=foil.e0, rbkg=1.0, kweight=2)
xftf(foil, kmin=3.0, kmax=11.5, dk=1.0, kweight=2, window="kaiser")
foil_mag = np.hypot(foil.chir_re, foil.chir_im)
mf = (foil.r > 1.8) & (foil.r < 3.4)
r_foil_peak = foil.r[mf][np.argmax(foil_mag[mf])]
print(f"P foil Pt-Pt |chi(R)| peak at R = {r_foil_peak:.2f} A (reference)")

mask = (s.r > 1.0) & (s.r < 2.2)
r_first = s.r[mask][np.argmax(chir_mag[mask])]
mask_m = (s.r > 2.2) & (s.r < 3.1)
m_region = s.r[mask_m][np.argmax(chir_mag[mask_m])]
peak_metal = chir_mag[mask_m].max() / chir_mag.max()
print(f"first-shell |chi(R)| peak at R = {r_first:.2f} A "
      f"(+0.3-0.5 A -> ~{r_first + 0.4:.2f} A vs report Pt-C/N 2.02 A)")
print(f"high-shell structure max at R = {m_region:.2f} A "
      f"({peak_metal:.0%} of first shell)")
print(f"Note: foil Pt-Pt sits at {r_foil_peak:.2f} A; sample structure at "
      f"{m_region:.2f} A is {'OFFSET from' if abs(m_region-r_foil_peak)>0.1 else 'coincident with'} "
      f"metallic Pt-Pt position")

# --- XANES LCF (NNLS) with honest interpretation bounds ---------------------
from scipy.optimize import nnls
m = (s.energy > s.e0 - 30) & (s.energy < s.e0 + 80)
E, y = s.energy[m], s.norm[m]
A = np.vstack([np.interp(E, g.energy, g.norm)
               for g in (foil, groups["PtO"], groups["PtO2"])]).T
w, _ = nnls(A, y)
w = w / w.sum()
r_res = y - A @ w
lcf_r2 = 1 - np.sum(r_res**2) / np.sum((y - y.mean())**2)
print(f"LCF(XANES): foil={w[0]:.2f} PtO={w[1]:.2f} PtO2={w[2]:.2f}, R2={lcf_r2:.3f}")
print("LCF bounds: cationic single-atom Pt-C/N borrows PtO weight "
      "(white-line + edge shift co-directional) - do NOT read as literal "
      "phase fractions; quantitative verdict needs feffit.")

# ---- figure: 2x2 final-size -------------------------------------------------
mpl.rcParams.update({
    "font.family": "Arial", "font.size": 6.0,
    "axes.labelsize": 6.5, "xtick.labelsize": 5.5, "ytick.labelsize": 5.5,
    "axes.linewidth": 0.4, "pdf.fonttype": 42,
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False,
})

STYLES = {
    "Pt_sample": ("#D55E00", 1.0, "Pt single-atom sample"),
    "Pt_Foil":   ("#0072B2", 0.7, "Pt foil (Pt" + chr(8304) + ")"),
    "PtO":       ("#009E73", 0.7, "PtO (Pt" + chr(178) + "+)"),
    "PtO2":      ("#5F6368", 0.7, "PtO" + chr(8322) + " (Pt" + chr(8308) + "+)"),
}

fig, axes = plt.subplots(2, 2, figsize=(183 * MM, 120 * MM), constrained_layout=True)
fig.get_layout_engine().set(w_pad=1.6 * MM, h_pad=1.6 * MM, wspace=0.06, hspace=0.10)

ax = axes[0, 0]
for name, (c, lw, lab) in STYLES.items():
    g = groups[name]
    ax.plot(g.energy, g.norm, color=c, lw=lw, label=lab)
ax.set_xlim(11560, 11700)
ax.set_ylim(0, 1.6)
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("Normalized " + chr(956) + "(E)")
ax.legend(loc="upper right", fontsize=5.0)
ax.set_title("a", loc="left", fontweight="bold", fontsize=8, pad=3)
ax.set_title("XANES, Pt L$_3$ edge", loc="center", fontsize=6.5, pad=3)

ax = axes[0, 1]
for name in ("Pt_sample", "Pt_Foil", "PtO", "PtO2"):
    g = groups[name]
    c, lw, _ = STYLES[name]
    m = (g.energy > g.e0 - 20) & (g.energy < g.e0 + 30)
    ax.plot(g.energy[m], g.norm[m], color=c, lw=lw + 0.2)
    ax.axvline(g.e0, color=c, lw=0.5, ls=":")
ax.set_xlabel("Energy (eV)")
ax.set_ylabel("Normalized " + chr(956) + "(E)")
ax.set_title("b", loc="left", fontweight="bold", fontsize=8, pad=3)
ax.set_title(f"edge region (E$_0$ shift {MINUS}{edge_shift:+.1f} eV vs foil)",
             loc="center", fontsize=6.5, pad=3)

ax = axes[1, 0]
ax.plot(s.k, s.k**2 * s.chi, color="#D55E00", lw=0.6)
ax.set_xlim(0, 12.5)
ax.set_xlabel("k (" + chr(197) + "$^{-1}$)")
ax.set_ylabel("k$^2$" + chr(967) + "(k)")
ax.set_title("c", loc="left", fontweight="bold", fontsize=8, pad=3)
ax.set_title("k$^2$-weighted EXAFS", loc="center", fontsize=6.5, pad=3)

ax = axes[1, 1]
ax.plot(s.r, chir_mag, color="#D55E00", lw=0.9)
ax.axvspan(2.2, 3.1, color="#999999", alpha=0.12, lw=0)
ax.annotate("Pt-Pt region\n(no metal path)", xy=(2.65, chir_mag.max() * 0.45),
            xytext=(3.4, chir_mag.max() * 0.6), fontsize=5.5,
            arrowprops=dict(arrowstyle="->", lw=0.5, color="#555555"))
ax.set_xlim(0, 5)
ax.set_ylim(0, chir_mag.max() * 1.15)
ax.set_xlabel("R (" + chr(197) + ")")
ax.set_ylabel("|" + chr(967) + "(R)|")
ax.set_title("d", loc="left", fontweight="bold", fontsize=8, pad=3)
ax.set_title("|" + chr(967) + "(R)|, k-weight 2, k 3" + MINUS + "11.5",
             loc="center", fontsize=6.5, pad=3)

out = HERE / "xafs_athena_pt_single_atom"
fig.savefig(out.with_suffix(".pdf"))
fig.savefig(out.with_suffix(".png"), dpi=600)
print(f"[saved] {out.name}.pdf/.png  page=183x120 mm")
