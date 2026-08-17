# Chart Catalog — 2D/3D 图型全谱目录（学习地图 + 配方 backlog）

> 2026-08-17。图型组织体系吸收 [From Data to Viz](https://www.data-to-viz.com/)
> （按数据结构选图决策树）+ [Python Graph Gallery](https://python-graph-gallery.com/)
> （400+ 实例、40 分类）+ 各领域期刊实战。
> 状态标记：✅ 已有配方 · 🔜 backlog（下批补）· ⬜ 空白（待学习）。
> 每条给实现栈；新配方按 `growth/CONTRIBUTING.md` 流程沉淀到
> `skills/sci-figure-plot/recipes/`。

## 一、2D 通用图型（按数据结构）

### 分布（distribution）
| 图型 | 数据形态 | 实现栈 | 状态 |
|---|---|---|---|
| 直方图 + KDE | 单变量数值 | matplotlib | ✅ |
| 小提琴/箱线 + 散点 | 组 × 数值 | matplotlib | ✅（bio PROFILE） |
| 山脊图（joyplot） | 组 × 分布 | joypython/matplotlib | 🔜 |
| 雨云图（raincloud） | 组 × 数值 | ptitprince/matplotlib | 🔜（生物高频） |
| 2D 密度/hexbin | 双数值 大 n | matplotlib | 🔜 |

### 关系（correlation）
| 散点 + 拟合带 | 双数值 | matplotlib（CI 带配方✅） | ✅ |
| 气泡图 | 三变量 | matplotlib | 🔜 |
| 配对连接图 | 前后/配对 | matplotlib（躲让规则✅） | ✅ |
| 相关矩阵 | 多变量 | seaborn clustermap | 🔜 |

### 比较（comparison）
| 柱状 + 误差 | 组 × 均值 | matplotlib/Origin | ✅ |
| 点图（dot plot，n<8 纪律） | 组 × 观测 | matplotlib | ✅ |
| 热图 + 注释条 | 矩阵 | matplotlib | 🔜 |
| 斜率图 | 两时点 × 组 | matplotlib | ⬜ |

### 组成（composition）
| 堆叠柱/面积 | 部分 × 整体 | matplotlib | 🔜 |
| 树图/旭日 | 层级占比 | squarify/plotly | ⬜ |
| 桑基图 | 流向 | plotly | ⬜ |
| 瀑布图 | 增减分解 | matplotlib | ⬜ |

### 时间/趋势
| 折线 + 置信带 | 时序 | matplotlib | ✅ |
| 事件注记时间线 | 时序+事件 | matplotlib | 🔜 |

### 不确定性（科研刚需）
| 森林图 | 效应量 × CI | matplotlib | 🔜（生物/meta 高频） |
| 误差棒总览 | 任意×误差 | matplotlib | ✅ |
| p 值显著性标注 | 组间比较 | statannotations | 🔜 |

### 网络/层级
| 网络图 | 节点边 | networkx | ⬜ |
| 和弦图 | 关联矩阵 | plotly/chord | ⬜ |
| 树状图 | 层级 | scipy+matplotlib | ⬜ |

## 二、科研专用谱图（纳米材料主场）

| 图型 | 数据形态 | 实现栈 | 状态 |
|---|---|---|---|
| XRD 谱叠图 + PDF 卡片棒 | 2θ × 强度 | matplotlib | 🔜 |
| 拉曼/IR 谱 | 波数 × 强度 | matplotlib | 🔜 |
| XPS 分峰拟合 | 结合能 × 计数 + 分峰 | matplotlib（填峰） | 🔜 |
| CV 循环伏安 | E × I 环路 | matplotlib | ✅ |
| DPV/SWV | E × I 峰 | matplotlib（浓度色映射✅） | ✅ |
| EIS Nyquist + Bode + 拟合电路 | Z' × −Z'' | matplotlib/等效电路 | 🔜 |
| Tafel / 活化过电位 | log j × η | matplotlib | 🔜 |
| EXAFS k²χ(k)/R 空间拟合 | k/R × 信号 | matplotlib + Larch | 🔜 |
| XANES 叠图/LCF | E × μ(E) | matplotlib + Larch | 🔜 |
| EXAFS 小波图 | k–R 二维 | Larch xafs_wavelets / ESRF BM20 | ⬜ |
| 等温线/吸附模型 | p/p₀ × 量 + 模型 | matplotlib | ⬜ |
| PL/UV-Vis + Tauc | 波长 × 吸收 + 带隙 | matplotlib | 🔜 |
| DFT PDOS/d 带（见 skill） | E × DOS | matplotlib | ✅ |
| 差分电荷/平面平均 | z × ρ | matplotlib | ✅ |
| Arrhenius / van't Hoff | 1/T × log k | matplotlib | 🔜 |

## 三、3D 图型（本仓库当前空白区，最大增量方向）

| 图型 | 数据形态 | 实现栈 | 状态 |
|---|---|---|---|
| 3D 曲面/等高线投影 | 网格双自变量 | matplotlib(mplot3d)/plotly | 🔜 |
| 等值面（isosurface） | 体数据 | **PyVista**（VTK 现代封装，可复现出版图） | ⬜ |
| 体渲染/切片 | 3D 场 | PyVista | ⬜ |
| 矢量场/流线 | 3D 矢量 | PyVista/Mayavi | ⬜ |
| 晶体结构/原子团簇 | POSCAR/lammps dump | **OVITO**（原子模拟标准）/ ASE | ⬜ |
| 分子结构/蛋白 | pdb/mol | PyMOL / rdkit | ⬜（生物） |
| 表面形貌 3D（AFM） | 高度矩阵 | PyVista/matplotlib | ⬜ |
| 地图/地理分布 | 坐标+值 | cartopy | ⬜ |
| 3D 艺术封面渲染 | 场景 | Blender(headless)/C4D | ⬜（艺术设计，千元级服务） |

3D 技术选型结论（调研 2026-08）：**PyVista**（活跃维护、脚本化可复现，
mesh/volume 出版图首选）为主力；**OVITO** 独占原子/晶体模拟渲染
（LAMMPS/VASP 生态）；Mayavi 有可引用论文但维护弱于 PyVista；
Blender headless 覆盖封面艺术渲染高价区间。

## 四、示意图/版式（scientific-schematics + toolchain 域）

| 类型 | 实现栈 | 状态 |
|---|---|---|
| 机制图/通路图（BioRender 风） | AI 生图评分环 + bioicons/SciDraw 素材 | ✅ |
| 流程图/示意图 | AI 生图 / graphviz | ✅/🔜 |
| graphical abstract/TOC | schematics + Inkscape 转曲 | ✅ |
| 学术海报 A0 | Inkscape 矢量拼版 | 🔜 |
| 封面候选（比稿多版） | schematics + Blender(3D) | ⬜ |

## 五、学习路线（backlog 排序）

1. **P0 谱图族**（XRD/XPS/EIS/UV-Vis/Tafel）：纳米材料服务菜单核心，
   全部 matplotlib 2D，复用现有纪律，成本低
2. **P0 雨云图/森林图**：生物服务菜单核心
3. **P1 PyVista 入门**（曲面/等值面/切片）：3D 数据图最小集
4. **P1 OVITO 晶体渲染**：纳米材料 3D 刚需（POSCAR → 出版图管线）
5. **P2 Blender headless**：封面艺术渲染（千元级定价区间）
6. 学习材料：Python Graph Gallery 逐类过（按 data-to-viz 决策树索引）、
   PyVista 官方 examples、OVITO manual；PMC 同行评审综述
   （Mastering data viz with Python, 2023）作规范引用
