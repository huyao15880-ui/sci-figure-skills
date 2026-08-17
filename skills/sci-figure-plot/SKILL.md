---
name: sci-figure-plot
description: "[阶段1·单图] 从准备好的 CSV 绘制单个投稿级面板（DFT PDOS / 电荷密度 / 电化学曲线 / 校准统计）。约定优先：统一样式层级使面板可自由进组图。不做多面板组图（用 sci-figure-compose）或图型选择（用选型顾问）。"
version: 1.0.0
domains: [nanomaterials, biology]
---

# sci-figure-plot — 单面板科研绘图（DFT / 电化学 / 校准统计）

约定优先（conventions-first）：所有图遵循统一样式层级，面板可自由组合进组图。

## 何时使用
- 画**一个**投稿级数据面板（CSV/计算输出 → 单面板矢量图）
- 面板将进入组图（输出规格必须与组图规划一致，先读 sci-figure-compose 的版式）

## 目录结构（每图一个自包含文件夹）

```
figure_N/
  data/          ← 输入：VESTA 的 .tif、POSCAR、PDOS CSV、CHGDIFF.vasp
  output/        ← 产出：单个面板文件
  plot_xxx.py    ← 每种面板一个脚本
  plot_tot.py    ← 组合器：把 output/ 的面板拼成最终图
```

## 样式常量

```python
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Arial"

DPI = 600
FMT = ".tiff"

# 单面板尺寸（进组图时以组图规划的目标 mm 为准，figsize = mm/25.4）
FIGSIZE_SINGLE = (6.2, 4.8)
FIGSIZE_WIDE   = (12.5, 7.0)   # 行数多时调高度

# 字号（最终物理尺寸下的 pt 值）
FS_PANEL_LABEL = 22   # 面板字母 a, b, c ...（独立预览尺寸时）
FS_AXIS_LABEL  = 15
FS_TICK        = 13
FS_VALUE_LABEL = 12

BAR_W = 0.42

def style_ax(ax):
    for sp in ax.spines.values():
        sp.set_linewidth(1.0)
    ax.tick_params(direction="in", labelsize=FS_TICK, width=1.0, length=4)
```

> 注意：上表字号是「独立大图预览」体系；**进组图/期刊交付时**一切以
> sci-figure-compose 的最终坐标系规格表为准（刻度 5.5pt / 轴题 6pt 一类），
> 两套体系禁止混用在同一交付物内。

## 材料系列色板（boride 体系实例，可按体系替换）

```python
COLORS = {
    "FeCoNiB": "#6F4C9B",
    "FeB":     "#B75828",
    "CoB":     "#224967",
    "NiB":     "#4b7f52",
}
```

替换原则：同体系内保持等明度差、色盲可分（Okabe-Ito 或
`domains/art-design/PROFILE.md` 的色板规范）。

## 面板字母约定

```python
ax.text(0.01, 0.98, "a", transform=ax.transAxes,
        fontsize=22, fontweight="bold", color="black", ha="left", va="top")
```

（组图时字母由组图层统一放置，单面板不预置——见 compose 规则。）

## find_image 辅助（plot_tot.py 用）

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

## PDOS 面板（DFT 态密度）

```python
import pandas as pd
import numpy as np

df = pd.read_csv("data/FeCoNiB_N_metal_vertical_pdos.csv")
E   = df["energy_eV_vs_Ef"].values
dos = df["top_metal_d"].values
eps_d = -2.310   # 预计算的 d 带中心

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

## d 带中心柱状图

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

## 接触距离（从 POSCAR）

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

## 平面平均电荷密度（CHGDIFF.vasp）

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
    gl = 8 + natoms          # 网格行索引（有 Selective Dynamics 时调整）
    nx,ny,nz = map(int, lines[gl].split()[:3])
    vals = [float(x) for x in re.findall(r"[+-]?[\d.]+(?:[Ee][+-]?\d+)?",
                                          "\n".join(lines[gl+1:]))
            ][:nx*ny*nz]
    rho_z = (np.array(vals).reshape(nz,ny,nx)/volume).mean(axis=(1,2))
    return np.linspace(0, c_len, nz, endpoint=False), rho_z
```

## 组合面板（plot_tot.py 模式）

```python
import matplotlib.pyplot as plt, matplotlib.image as mpimg

fig = plt.figure(figsize=(12.5, 7.0))
gs  = fig.add_gridspec(2, 3, width_ratios=[1,1,1.05], wspace=0.02, hspace=0.02)

layout = {"a": gs[0,0], "b": gs[0,1], "c": gs[1,0], "d": gs[1,1], "e": gs[:,2]}
for lab, cell in layout.items():
    ax  = fig.add_subplot(cell)
    img = mpimg.imread(find_image(lab_to_name[lab]))
    ax.imshow(img); ax.axis("off")
    ax.text(0.01, 0.98, lab, transform=ax.transAxes,
            fontsize=22, fontweight="bold", color="black", ha="left", va="top")

plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
plt.savefig(f"output/Figure_N_combined{FMT}", dpi=DPI, bbox_inches="tight")
```

（投稿级正式组图不走 imshow 栅格拼装——矢量 1:1 拼版见 sci-figure-compose。）

## 电化学/校准面板要点（DPV / CV / 校准统计）

- 曲线族色 = 浓度映射用 `viridis` + 共享 colorbar（Normalize 到全浓度域）
- 校准图：散点 + OLS 拟合线 + 95% 置信带（t 分布）+ 注记 m/R²/LOD*
- 注记数值**运行时从冻结统计文件读取**，禁止硬编码；LOD* 等探索性估计
  必须带 * 号并在图注声明边界
- 参考 `datasets/DATASET_INDEX.md` 中电化学数据集的字段约定

## 常见错误

| 错误 | 修正 |
|---|---|
| CHGCAR 有 Selective Dynamics → 网格行索引错 | 检查 `lines[7]` 是否以 S 开头并 `coord_line += 1` |
| imshow 拉伸 tif 长宽比 | 不要手动设 equal aspect；imshow 自己处理 |
| 组合 tiff 过大 | 每个 .tif 输入先在 VESTA 里裁剪再保存 |
| 渐变箭头出现色带 | n 提到 2000+ 并用 `dy*1.08` 重叠条带 |
| 柱顶数值被裁 | 放文字前 `ax.set_ylim(0, max+0.5)` |
