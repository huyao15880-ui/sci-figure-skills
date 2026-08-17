"""Recipe 15 — EIS analysis: Randles circuit closed loop + real-object overlay.

Panel (a): synthetic Randles EIS (Rs + CPE//Rct), Nyquist plot, with a
hand-rolled complex-least-squares fit recovering the circuit parameters
(closed-loop validation, stated synthetic).
Panel (b): Bode magnitude + phase of the same data/fit.
Panel (c): REAL data recovered from the provider's Origin object
(oleObject3, slide 5 panel C, 61 points; column semantics interpreted
as two (Z', -Z'') curves per Nyquist convention - frequency axis not
preserved with the object, stated).

Run:  python eis_nyquist_bode.py
Data: data/obj3_EIS.csv (real, provider Origin object) + synthetic
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

HERE = Path(__file__).parent
MM = 1 / 25.4
MINUS = "\u2212"

# ---- synthetic Randles ground truth + fit ------------------------------------
TRUE = dict(Rs=10.0, Rct=500.0, Q=2e-5, n=0.90)
f = np.logspace(5, -2, 61)
w = 2 * np.pi * f


def randles(w, Rs, Rct, Q, n):
    Zc = 1.0 / (Q * (1j * w) ** n)          # CPE
    return Rs + 1.0 / (1.0 / Rct + 1.0 / Zc)


Z_true = randles(w, **TRUE)
rng = np.random.default_rng(7)
Z_obs = Z_true * (1 + rng.normal(0, 0.008, Z_true.size)
                  + 1j * rng.normal(0, 0.008, Z_true.size))


def resid(p):
    Zm = randles(w, *p)
    d = ((Zm - Z_obs) / np.abs(Z_obs)).view(float)
    return d


fit = least_squares(resid, [5.0, 300.0, 1e-5, 0.8],
                    bounds=([1, 10, 1e-7, 0.5], [100, 5000, 1e-3, 1.0]))
Rs, Rct, Q, n = fit.x
Z_fit = randles(w, *fit.x)
print("Randles recovery (synthetic):")
print(f"  Rs {Rs:.1f} (true 10)  Rct {Rct:.1f} (true 500)  "
      f"Q {Q*1e5:.2f}e-5 (true 2)  n {n:.3f} (true 0.90)")

# ---- real object curves -------------------------------------------------------
df = pd.read_csv(str(HERE / "data" / "obj3_EIS.csv"))
real = [df[["col_1", "col_2"]].to_numpy(), df[["col_3", "col_4"]].to_numpy()]

# ---- figure --------------------------------------------------------------------
mpl.rcParams.update({
    "font.family": "Arial", "font.size": 7,
    "axes.labelsize": 8, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.linewidth": 0.8, "pdf.fonttype": 42,
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.major.size": 3.2, "ytick.major.size": 3.2,
    "xtick.top": True, "ytick.right": True,
    "legend.frameon": False,
})
NAVY, CRIM, GOLD = "#2C5F8A", "#B0413E", "#C89F5A"

fig, axes = plt.subplots(1, 3, figsize=(183 * MM, 62 * MM),
                         constrained_layout=True)
fig.get_layout_engine().set(w_pad=3 * MM, h_pad=2 * MM, wspace=0.08)

ax = axes[0]
ax.plot(Z_obs.real, -Z_obs.imag, "o", color=NAVY, ms=2.6, mfc="none",
        label="data (synthetic)")
ax.plot(Z_fit.real, -Z_fit.imag, color=CRIM, lw=1.3,
        ls=(0, (4, 1.5)), label="Randles fit")
ax.set_xlabel("Z" + chr(8242) + " (" + chr(937) + ")")
ax.set_ylabel(MINUS + "Z" + chr(8243) + " (" + chr(937) + ")")
ax.legend(loc="upper left", fontsize=6.8)
ax.set_title("a", loc="left", fontweight="bold", fontsize=8, pad=4)

ax = axes[1]
mag = np.abs(Z_obs)
ax.loglog(f, mag, "o", color=NAVY, ms=2.6, mfc="none", label="|Z| data")
ax.loglog(f, np.abs(Z_fit), color=CRIM, lw=1.2, label="|Z| fit")
ax.set_xlabel("f (Hz)")
ax.set_ylabel("|Z| (" + chr(937) + ")")
ax2 = ax.twinx()
ph = np.degrees(-np.angle(Z_obs))
ax2.semilogx(f, ph, "^", color=GOLD, ms=2.4, mfc="none")
ax2.set_ylabel(MINUS + "phase (deg)", color=GOLD, fontsize=8)
ax2.tick_params(labelsize=6.5, colors=GOLD)
ax.legend(loc="lower left", fontsize=6.8)
ax.set_title("b", loc="left", fontweight="bold", fontsize=8, pad=4)

ax = axes[2]
ax.plot(real[0][:, 0], real[0][:, 1], "o-", color=NAVY, ms=2.6, lw=0.9,
        label="object curve 1")
ax.plot(real[1][:, 0], real[1][:, 1], "s-", color=GOLD, ms=2.6, lw=0.9,
        label="object curve 2")
ax.set_xlabel("Z" + chr(8242) + " (object units, semantics TBC)")
ax.set_ylabel("imaginary part (object units)")
ax.legend(loc="upper left", fontsize=6.8)
ax.text(0.97, 0.05, "provider Origin object 3\n(slide 5, panel C);\nfrequency axis not preserved",
        transform=ax.transAxes, ha="right", fontsize=6.0, color="#555555")
ax.set_title("c", loc="left", fontweight="bold", fontsize=8, pad=4)

out = HERE / "eis_nyquist_bode"
fig.savefig(out.with_suffix(".pdf"))
fig.savefig(out.with_suffix(".png"), dpi=600)
print(f"[saved] {out.name}.pdf/.png  page=183x62 mm")
