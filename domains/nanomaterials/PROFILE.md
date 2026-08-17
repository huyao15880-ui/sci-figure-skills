# Domain Profile: 纳米材料（Nanomaterials）

纳米材料领域的图件适配档案。skill 通用规则见 `skills/`，本页只放领域增量。

## 数据类型 → 图型 → skill 映射

| 数据类型 | 典型图型 | 主 skill | 备注 |
|---|---|---|---|
| DFT 态密度（PDOS CSV） | 曲线 + d 带中心虚线 | sci-figure-plot | ε_d 标注用 mathtext |
| DFT 电荷密度差（CHGDIFF.vasp） | 平面平均曲线 | sci-figure-plot | 见 read_chgcar_planar 配方 |
| 结构文件（POSCAR） | 接触距离/结构参数 | sci-figure-plot | VESTA 截图进 data/ |
| 电化学（CV/DPV/EIS） | 曲线族 + 浓度色映射 | sci-figure-plot + Origin | viridis + 共享 colorbar |
| 校准/定量 | 散点 + OLS + 95% CI 带 + LOD* 注记 | sci-figure-plot | 数值运行时读冻结统计文件 |
| 表征（XRD/EXAFS/XPS/TEM） | 谱图/显微图拼版 | sci-figure-compose | Origin/LabTalk 直读隐藏数据集 |
| 机理/结构示意 | 概念图 | scientific-schematics | 严格几何用 schemdraw |
| 多面板正文图 | 183mm 组图 | sci-figure-compose | 最终坐标系纪律 |

## 领域规范增量

- **单位与轴**：能量 eV（vs E_F 显式标注）、电流 μA、电位 V（vs Ag/AgCl 等
  参比显式）、浓度 μM/mol L⁻¹——轴题必须带单位，参比电极必须写全
- **色板**：材料体系色（boride 实例见 sci-figure-plot）；浓度映射一律
  viridis + colorbar，禁 rainbow
- **统计边界**：单点浓度（无重复）的 LOD 标 LOD* 并在图注声明 exploratory；
  置信带用 t 分布 95%
- **仿真链**：COMSOL 后处理图走 cli-anything-comsol（见 toolchain §3），
  网格/边界条件参数写入图注或 SI

## 领域数据集

本地数据集按 `datasets/DATASET_INDEX.md` 规范注册（数据不进仓库，
索引进）。纳米材料典型数据集形态：PDOS 列式 CSV（energy_eV_vs_Ef,
top_metal_d）、DPV 曲线长表（potential_V, current_uM, concentration_uM,
material）、校准统计冻结表（slope/r2/lod + CI 列）。

## 常见坑（领域专属）

- EXAFS/R² 复算与文献标注值要对账（矢量重建几何保真度验证）
- 电化学窗口标注（如 0.28–0.36 V 操作窗）用 axvspan 灰带，不用箭头
- 表征图源自仪器的位图（TEM/SEM）拼版禁重采样放大——1:1 置入
