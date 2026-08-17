---
name: sci-figure-plot
description: [阶段1·单图] Draw ONE publication panel with matplotlib from prepared CSV (DFT PDOS / charge density / electrochemistry curves). NOT for multi-panel composition or chart-type choice.
---

# Scientific Figure Plotting (DFT / Electrochemistry)

## Overview

A conventions-first approach to generating publication-quality figures with matplotlib. All figures follow a unified style hierarchy so panels can be freely combined into composite figures.

## Directory Structure

```
figure_N/
  data/          ← input: .tif from VESTA, POSCAR, PDOS CSV, CHGDIFF.vasp
  output/        ← generated: individual .tiff panels
  plot_xxx.py    ← one script per panel type
  plot_tot.py    ← combiner: assembles output/ images into final figure
```

Each folder is a self-contained figure. `plot_tot.py` reads from `output/` and writes the final combined `.tiff`.

## Style Constants

```python
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"

DPI = 600
FMT = ".tiff"

# Individual panel size
FIGSIZE_SINGLE = (6.2, 4.8)
# Combined multi-panel
FIGSIZE_WIDE   = (12.5, 7.0)   # adjust height per row count

# Typography
FS_PANEL_LABEL = 22   # panel letters: a, b, c ...
FS_AXIS_LABEL  = 15
FS_TICK        = 13
FS_VALUE_LABEL = 12

# Bar width
BAR_W = 0.42

# Spine / tick styling
def style_ax(ax):
    for sp in ax.spines.values():
        sp.set_linewidth(1.0)
    ax.tick_params(direction="in", labelsize=FS_TICK, width=1.0, length=4)
```

## Color Palette (boride series)

```python
COLORS = {
    "FeCoNiB": "#6F4C9B",
    "FeB":     "#B75828",
    "CoB":     "#224967",
    "NiB":     "#4b7f52",
}
```

## Panel Label Convention

```python
ax.text(0.01, 0.98, "a",
        transform=ax.transAxes,
        fontsize=22, fontweight="bold", color="black",
        ha="left", va="top")
```

## find_image Helper (used in plot_tot.py)

```python
from pathlib import Path

def find_image(name, search_dirs=("output", "data")):
    for folder in search_dirs:
        for ext in [".tif", ".tiff", ".png", ".jpg", ".jpeg"]:
            p = Path(folder) / f"{name}{ext}"
            if p.exists():
                return p
    raise FileNotFoundError(f"Cannot find image: {name}")
```

## PDOS Panel

```python
import pandas as pd
import numpy as np

df = pd.read_csv("data/FeCoNiB_N_metal_vertical_pdos.csv")
E   = df["energy_eV_vs_Ef"].values
dos = df["top_metal_d"].values
eps_d = -2.310   # precomputed d-band center

fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
ax.axvline(eps_d, color="#9E9E9E", ls="--", lw=2.4, label=r"$\varepsilon_d$")
ax.plot(E, dos, color=COLORS["FeCoNiB"], lw=2.3, label="FeCoNiB")
ax.set_xlim(-9, 5)
ax.set_xlabel(r"Energy $-$ $E_F$ (eV)", fontsize=FS_AXIS_LABEL)
ax.set_ylabel(r"PDOS (eV$^{-1}$)",       fontsize=FS_AXIS_LABEL)
style_ax(ax)
plt.tight_layout()
plt.savefig(f"output/FeCoNiB_pdos{FMT}", dpi=DPI, bbox_inches="tight")
```

## d-Band Center Bar Chart

```python
data = {
    "FeCoNiB": (-2.310, COLORS["FeCoNiB"]),
    "FeB":     (-2.192, COLORS["FeB"]),
    "CoB":     (-2.158, COLORS["CoB"]),
    "NiB":     (-2.591, COLORS["NiB"]),
}
items = sorted(data.items(), key=lambda x: x[1][0])
labels, eps, colors = zip(*[(k, v[0], v[1]) for k, v in items])

fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
bars = ax.bar(labels, eps, color=colors, width=BAR_W)
ax.set_ylim(min(eps) - 0.5, 0.0)
ax.set_ylabel(r"d-band center $\varepsilon_d$ (eV)", fontsize=FS_AXIS_LABEL)
for bar, val in zip(bars, eps):
    ax.text(bar.get_x() + bar.get_width()/2, val - 0.05,
            f"{val:.3f}", ha="center", va="top", fontsize=FS_VALUE_LABEL)
style_ax(ax)
plt.tight_layout()
plt.savefig(f"output/epsilon_d_bar_chart{FMT}", dpi=DPI, bbox_inches="tight")
```

## Contact Distance (from POSCAR)

```python
import numpy as np
from pathlib import Path

SURFACE_ELEM   = {"Fe","Co","Ni","B"}
ADSORBATE_ELEM = {"C","H","O"}

def read_poscar(file):
    lines = Path(file).read_text(errors="ignore").splitlines()
    scale   = float(lines[1])
    lattice = np.array([[float(x) for x in lines[i].split()[:3]]
                        for i in range(2,5)]) * scale
    elements = lines[5].split()
    counts   = [int(x) for x in lines[6].split()]
    coord_line = 7
    if lines[coord_line].strip().lower().startswith("s"):
        coord_line += 1
    frac = np.array([[float(x) for x in lines[coord_line+1+i].split()[:3]]
                     for i in range(sum(counts))])
    cart = frac @ lattice
    atoms = [e for e,n in zip(elements,counts) for _ in range(n)]
    return lattice, np.array(atoms), frac, cart

def pbc_dist(f1, f2, lattice):
    df = f1 - f2; df -= np.round(df)
    return np.linalg.norm(df @ lattice)

def contact_distance(poscar):
    lattice, atoms, frac, _ = read_poscar(poscar)
    surf = [i for i,e in enumerate(atoms) if e in SURFACE_ELEM]
    ads  = [i for i,e in enumerate(atoms) if e in ADSORBATE_ELEM]
    return min(pbc_dist(frac[i], frac[j], lattice) for i in surf for j in ads)
```

## Planar-Average Charge Density (CHGDIFF.vasp)

```python
import re, numpy as np

def read_chgcar_planar(file):
    lines = Path(file).read_text(errors="ignore").splitlines()
    scale   = float(lines[1])
    lattice = np.array([[float(x) for x in lines[i].split()[:3]]
                        for i in range(2,5)]) * scale
    volume  = abs(np.linalg.det(lattice))
    c_len   = np.linalg.norm(lattice[2])
    natoms  = sum(int(x) for x in lines[6].split())
    gl = 8 + natoms          # grid line index (adjust for Selective Dynamics)
    nx,ny,nz = map(int, lines[gl].split()[:3])
    vals = [float(x) for x in re.findall(r"[+-]?[\d.]+(?:[Ee][+-]?\d+)?",
                                          "\n".join(lines[gl+1:]))
            ][:nx*ny*nz]
    rho_z = (np.array(vals).reshape(nz,ny,nx)/volume).mean(axis=(1,2))
    return np.linspace(0, c_len, nz, endpoint=False), rho_z
```

## Composite Panel (plot_tot.py pattern)

```python
import matplotlib.pyplot as plt, matplotlib.image as mpimg

fig = plt.figure(figsize=(12.5, 7.0))
gs  = fig.add_gridspec(2, 3, width_ratios=[1,1,1.05], wspace=0.02, hspace=0.02)

layout = {
    "a": gs[0,0], "b": gs[0,1],
    "c": gs[1,0], "d": gs[1,1],
    "e": gs[:,2],
}
for lab, cell in layout.items():
    ax  = fig.add_subplot(cell)
    img = mpimg.imread(find_image(lab_to_name[lab]))
    ax.imshow(img); ax.axis("off")
    ax.text(0.01, 0.98, lab, transform=ax.transAxes,
            fontsize=22, fontweight="bold", color="black", ha="left", va="top")

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
plt.savefig(f"output/Figure_N_combined{FMT}", dpi=DPI, bbox_inches="tight")
```

## Obtain / Loss Arrow Schematic

```python
from matplotlib.patches import Polygon, Rectangle
import numpy as np

yellow, cyan = "#F2F247", "#57d9d9"

def smooth(u): return 6*u**5 - 15*u**4 + 10*u**3

def gradient(ax, x0, x1, y0, y1, c0, c1, n=2000):
    dy = (y1-y0)/n
    for i in range(n):
        t = smooth(i/(n-1))
        ax.add_patch(Rectangle((x0, y0+i*dy), x1-x0, dy*1.08,
                                facecolor=(1-t)*c0+t*c1, edgecolor="none"))
# Draw upward (yellow) and downward (cyan) gradient-tipped arrows
# then label with rotated "Obtain" / "Loss" text at 90°
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| CHGDIFF.vasp has Selective Dynamics → wrong grid line index | Check `lines[7]` starts with `S` and shift `coord_line += 1` |
| `imshow` distorts tif aspect ratio | Never set equal aspect manually; `imshow` handles it |
| Combined tiff too large | Each `.tif` input should be cropped in VESTA before saving |
| Gradient arrow shows banding | Increase `n` to 2000+ and overlap strips by `dy*1.08` |
| Bar value clipped at top | Set `ax.set_ylim(0, max+0.5)` before adding text labels |
