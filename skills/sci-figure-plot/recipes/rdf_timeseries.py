"""Recipe 14 — RDF time-series analysis (synchrotron total-scattering line).

The provider's package includes an RDF series (gofr-0..400, step 40;
"1nm" system) — the total-scattering/PDF methodology that complements
XAFS (PDF: all atom pairs; XAFS: absorber-centred). Panels:
  (a) representative g(r) slices + running coordination number CN(r)
  (b) r-vs-t heatmap of g(r) evolution
  (c) first-shell order (peak height) and CN(2.5 A) vs frame index
Frame-index physical meaning (ps? temperature? anneal step) is not
stated by the provider - reported as-is.

Run:  python rdf_timeseries.py
Data: data/rdf_1nm/gofr-*.dat (user-provided)
"""
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
MM = 1 / 25.4
FRAMES = list(range(0, 401, 40))

series = {}
for t in FRAMES:
    d = np.loadtxt(str(HERE / "data" / "rdf_1nm" / f"gofr-{t}.dat"))
    series[t] = d  # columns: r, g(r), CN(r)

r = series[0][:, 0]
G = np.vstack([series[t][:, 1] for t in FRAMES])      # (time, r)
CN = np.vstack([series[t][:, 2] for t in FRAMES])

i25 = np.argmin(np.abs(r - 2.5))
first_peak = G[:, (r > 1.2) & (r < 2.0)].max(axis=1)
r_at_peak = r[(r > 1.2) & (r < 2.0)][np.argmax(G[:, (r > 1.2) & (r < 2.0)],
                                               axis=1)]
print(f"first peak fixed at r = {r_at_peak[0]:.2f} A; "
      f"height {first_peak[0]:.1f} -> {first_peak[-1]:.1f}")
print(f"CN(2.5 A): {CN[0, i25]:.2f} -> {CN[-1, i25]:.2f}")

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
NAVY, CRIM, GOLD = "#2C5F8A", "#B0413E", "#C89F5A"

fig, axes = plt.subplots(1, 3, figsize=(183 * MM, 62 * MM),
                         constrained_layout=True)
fig.get_layout_engine().set(w_pad=3 * MM, h_pad=2 * MM, wspace=0.05)

# (a) slices + CN(r)
ax = axes[0]
for t, c, lw in ((0, NAVY, 1.5), (160, GOLD, 1.2), (400, CRIM, 1.2)):
    ax.plot(r, series[t][:, 1], color=c, lw=lw, label=f"frame {t}")
ax2 = ax.twinx()
ax2.plot(r, series[0][:, 2], color="#7F7F7F", lw=0.9, ls=(0, (4, 2)))
ax2.set_ylabel("CN(r)", color="#7F7F7F", fontsize=8)
ax2.tick_params(labelsize=6.5, colors="#7F7F7F")
ax.set_xlim(0, 6)
ax.set_ylim(0, 12.5)
ax.set_xlabel("r (" + chr(197) + ")")
ax.set_ylabel("g(r)")
ax.legend(loc="upper right", fontsize=7)
ax.set_title("a", loc="left", fontweight="bold", fontsize=8, pad=4)

# (b) heatmap r x t
ax = axes[1]
T, R = np.meshgrid(FRAMES, r)
pc = ax.pcolormesh(T, R, G.T, cmap="viridis", shading="auto",
                   rasterized=True, vmin=0, vmax=G.max())
ax.set_xlim(0, 400)
ax.set_ylim(0, 6)
ax.set_xlabel("frame index")
ax.set_ylabel("r (" + chr(197) + ")")
cb = fig.colorbar(pc, ax=ax, fraction=0.05, pad=0.02)
cb.ax.tick_params(labelsize=6, width=0.6)
cb.set_label("g(r)", fontsize=7.5)
ax.set_title("b", loc="left", fontweight="bold", fontsize=8, pad=4)

# (c) order + CN evolution
ax = axes[2]
ax.plot(FRAMES, first_peak, color=NAVY, lw=1.5, marker="o", ms=3.5,
        label="1st-shell peak g(r)")
ax.set_xlabel("frame index")
ax.set_ylabel("peak g(r)", color=NAVY)
ax.tick_params(axis="y", colors=NAVY)
ax2 = ax.twinx()
ax2.plot(FRAMES, CN[:, i25], color=CRIM, lw=1.5, marker="s", ms=3.5,
         label="CN(2.5 " + chr(197) + ")")
ax2.set_ylabel("CN(2.5 " + chr(197) + ")", color=CRIM)
ax2.tick_params(axis="y", colors=CRIM)
ax.set_title("c", loc="left", fontweight="bold", fontsize=8, pad=4)

out = HERE / "rdf_timeseries"
fig.savefig(out.with_suffix(".pdf"))
fig.savefig(out.with_suffix(".png"), dpi=600)
print(f"[saved] {out.name}.pdf/.png  page=183x62 mm")
