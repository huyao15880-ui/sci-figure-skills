# Changelog

本仓库遵循[成长性机制](growth/CONTRIBUTING.md)：配方/教训/数据集形态三通道沉淀。

## [1.0.0] - 2026-08-17

### 初始发布（自研清洗版）

- **skills/**：五个 skill 清洗为自有版本 v1.0.0
  - matplotlib：rcParams 期刊配方、savefig 纪律、U+2212/标记躲让硬规则
  - sci-figure-plot：单面板（DFT PDOS / d-band / POSCAR / CHGDIFF /
    电化学曲线 / 校准统计）+ boride 示例色板
  - sci-figure-compose：mm 精确 PDF-on-PDF 组图五步流水线、四查审计、
    Plotly 字号补偿、短绳执行纪律、教训集
  - sci-figure-toolchain：Origin/MATLAB/COMSOL/Inkscape CLI 配方与
    原生崩溃点绕行
  - scientific-schematics：AI 生图评分迭代环（attribution：davila7
    score-loop 思路）
- **domains/**：三领域适配层（纳米材料 / 生物 / 艺术设计）——数据类型→
  图型→skill 映射、领域规范增量、领域专属坑
- **datasets/**：本地数据集注册规范（数据不进仓库、索引进、冻结纪律）
- **growth/**：成长性机制（配方/教训/数据集三通道沉淀 + 版本规则）
- **docs/**：GAP_ANALYSIS（不足清单）、COMMERCIALIZATION（商业化路线）
- 实战背景：Nature Communications 投稿六图 + SI 三图全流程
  （最终坐标系原则、数值一致性校验、QA 闭环均在该投稿中验证）

### 补充（同日四批）

- **首个 XAFS recipe 落地**：`skills/sci-figure-plot/recipes/xafs_basic_chain_ptfoil.py`
  ——Pt 箔 L3 边 Larch 完整链 + 183mm 三联图（视觉审计 CLEAN）；
  物理验证：|χ(R)| 峰 2.45 Å + 相位修正 = 2.77 Å 与已知 Pt-Pt 键长精确吻合
- xraylarch 2026.3.1 本机安装 + 实跑；透射 XDI 无 mu 列踩坑记录
- SYNCHROTRON_XAFS 笔记增第六节实跑记录，backlog 更新

### 补充（同日三批）

- **docs/SYNCHROTRON_XAFS.md**：同步辐射 XAFS 处理分析学习笔记——工具地图
  （Larch/Larix/Demetter 理念/FEFF/小波三工具）、Larch API 级标准处理链
  （pre_edge→autobk→xftf→feffit + 6 个 worked example）、参数纪律
  （四件套报告/合理域/相位修正通则）、XAFS 绘图五件套规范、本地 Pt
  L3-edge 实战锚（单原子判据等）
- nanomaterials PROFILE 增同步辐射节；CHART_CATALOG 补 XANES/小波图型

### 补充（同日二批）

- **docs/CHART_CATALOG.md**：2D/3D 图型全谱目录（分布/关系/比较/组成/
  不确定性/科研谱图/3D/示意图八大类，含实现栈与配方状态），吸收
  From Data to Viz 决策树体系；3D 技术选型结论（PyVista 主力 +
  OVITO 原子渲染 + Blender headless 艺术渲染）
- GAP_ANALYSIS 增 G9（3D 能力为零——最大增量缺口）
- COMMERCIALIZATION 增竞品格局实证（国内付费网站全为示意图类，
  数据图+审计无直接竞品；3D 封面 ≥500 元/张定价锚）
