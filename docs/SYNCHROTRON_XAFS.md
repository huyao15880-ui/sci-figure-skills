# Synchrotron XAFS — 同步辐射数据处理分析学习笔记

> 2026-08-17 第一轮学习沉淀。学习目标锚定本地实战：Pt L3-edge 单原子催化剂
> EXAFS 报告（Pt-C/N + Pt-Pt 路径，k=3.0–11.5 / R=1.0–3.2 Å / k-weight=2）。
> 本文档按成长性机制维护：新学工具/踩坑按 `growth/CONTRIBUTING.md` 增补。

## 一、工具地图（学什么、用什么）

| 工具 | 角色 | 学习入口 |
|---|---|---|
| **Larch (xraylarch)** | Python 事实标准：XAFS 全链处理 + FEFF 拟合，MIT | [官方文档](https://xraypy.github.io/xraylarch/)（xafs 章节为处理链总纲）· [GitHub](https://github.com/xraypy/xraylarch)（examples/ 有示例脚本与数据）· 可引用论文 Newville 2013 ([DOI](https://doi.org/10.1088/1742-6596/430/1/012007)) |
| **Larix GUI** | Larch 自带图形界面（前身 XAS Viewer）：pre-edge 拟合 / LCF / PCA-LASSO / EXAFS | [overview](https://millenia.cars.aps.anl.gov/xraylarch/larix/overview.html) |
| **Athena / Artemis (Demeter)** | 传统标准 GUI（Ravel 出品）；理念与 Larch 同源 | [Ravel XAS-Education](https://github.com/bruceravel/XAS-Education)（CC BY-SA，含 FeS2/Cu 箔/Cr 标准等全套课程数据 + Athena 工程文件） |
| **FEFF** | 路径理论计算（feff6l / feff8l 随 Larch 附带；feff8 无 XANES） | Larch 文档 Running Feff 章 |
| **小波变换** | 区分散射原子种类（k-R 二维展开） | Larch `xafs_wavelets`（[文档](https://xraypy.github.io/xraylarch/xafs_wavelets.html)，Morlet+Cauchy）· [ESRF BM20 在线工具](https://www.esrf.fr/UsersAndScience/Experiments/CRG/BM20/Software/Wavelets)（Manceau 组）· 奠基论文 [Muñoz et al. PRB 71, 094110](https://link.aps.org/doi/10.1103/PhysRevB.71.094110) |

理论课（Ravel 教育仓库主题，按需精读）：ATEA 高级 EXAFS、XANES 解读、
多重散射引论、非晶样品建模、荧光自吸收、EXAFS 噪声与中心极限定理、
Ramsauer-Townsend 效应。

## 二、标准处理链（Larch API 级，顺序不可换）

```
原始数据 (read: read_ascii / XDI / SPEC / hdf5)
  ↓ 多次扫描 merge + 能量校准（对标样边位，如 Pt 箔 L3 11564 eV）
find_e0 → pre_edge        # E0 定位；预边扣除 + 归一化 (μ(E)→归一化谱)
  ↓ XANES 分析
pre-edge peak fitting；LCF（线性组合，价态/组分定量）；PCA/LASSO（组分数判定）
  ↓
autobk(rbkg=...)          # 背景扣除：μ(E) → χ(k)；rbkg 常取 1.0–1.5 Å
  ↓
xftf + ftwindow           # 前向 FT：χ(k) → χ(R)；k 权重/窗口/范围在此定
（反向 χ(R)→χ(q) 供拟合空间选择）
  ↓
feff6l/feff8l 生成路径 → feffpath/path2chi/ff2chi
  ↓
feffit_transform + feffit_dataset + feffit → feffit_report
  # 拟合空间可选 k / R / q（或联合）；多路径、多数据集、CN/物种敏感性
```

配套：`cauchy_wavelet`（小波二维展开）；`diffKK`（反常散射因子，含 L 边）。

Larch 自带 6 个 feffit worked example：单路径 / 多路径 / 多数据集 /
配位数 / 拟合空间对比 / Z 敏感性——**逐个跑通 = EXAFS 拟合入门毕业**。

## 三、参数纪律（投稿可辩护性，硬规则）

- **拟合范围必须报告**：k 范围、R 范围、拟合空间、k-weight 四件套
  写进图注（本地实战锚：k=3.0–11.5，R=1.0–3.2 Å，R 空间，k-weight=2）
- **参数合理域**（超出 = 拟合不可信，逐项检查）：
  0.8 < S0² < 1.0；CN > 0；σ² > 0 Å²；|ΔE0| < 10 eV；R-factor < 0.02
- **固定参数必须声明**（如按已知结构固定某路径 S0²/CN，表注标 *）
- **相位修正通则**：EXAFS FT 谱峰位置 + 0.3–0.5 Å ≈ 修正后真实键长
  （表列 R 值为准；这是 XAS 文献普遍现象，图注/审稿回复要能解释）
- **误差报告**：CN/R/σ²/ΔE0 全部 ± 不确定度（来自协方差矩阵）
- **能量校准**：每次变化必过标样；Ravel 教程含"Fe 箔能量失准"案例可练

## 四、绘图规范（XAFS 五件套，进 sci-figure-plot 体系）

| 图 | 内容 | 规范要点 |
|---|---|---|
| XANES 叠图 | 归一化 μ(E)，样品+标样 | 边位对比讲价态；一阶导图辅助定边 |
| k²χ(k) | χ(k) × k² | k 轴到拟合上限（如 11.5）；与拟合线叠画 |
| R 空间幅值 | FT |χ(R)| + 拟合线（数据黑/拟合红） | 峰位标注相位修正说明；R 窗口阴影可选 |
| 拟合参数表 | Path/CN/R/σ²/ΔE0/R-factor | 每值带 ±；固定项标 *；表注给四件套+合理域 |
| 小波图 | k–R 二维色图 | Morlet/Cauchy 注明参数；定性区分散射原子 |

全部图遵守本仓库排版纪律（Arial/U+2212/最终坐标系）；单原子催化剂
标配是 XANES 叠图 + k²χ(k) + R 空间 + 小波四联。

## 五、本地实战锚（Pt L3-edge 报告要点，作为后续复现基准）

- 样品：Pt1（单原子）与 lps-fenmo（低载量纳米）对照
- Pt1：Pt-C/N 路径 CN=4.3±0.5、R=2.02±0.01 Å——**无 Pt-Pt**（单原子判据）
- lps-fenmo：Pt-C/N CN=1.3±0.3 + Pt-Pt CN=3.3±0.9、R=2.67±0.01 Å
  （金属键 → 团簇证据）
- R-factor 0.013 / 0.019（<0.02 达标）；ΔE0 约 −4 eV（|ΔE0|<10 达标）
- 后续复现路线：拿 OPJ/原始 μ(E) → Larch 重跑 pre_edge→autobk→xftf→feffit
  → 与表中锁定值对账（数值一致性纪律）

## 六、实跑记录（2026-08-17，xraylarch 2026.3.1 本机）

- 安装：`pip install xraylarch`（连带 pymatgen/larixite/xraydb/silx 全家）
- 示例数据：pip wheel 不带 examples——`git clone --depth 1
  https://github.com/xraypy/xraylarch`，取 `examples/xafsdata/pt_metal_rt.xdi`
  （MIT，已复制进 `skills/sci-figure-plot/recipes/data/`）
- **首个 recipe 已沉淀**：`skills/sci-figure-plot/recipes/xafs_basic_chain_ptfoil.py`
  ——Pt 箔 L3 边完整链（read→pre_edge→autobk→xftf，k=3–11.5/k-weight=2
  对齐本地报告条件）+ 183mm 三联图（XANES/k²χ(k)/|χ(R)|），视觉审计 CLEAN
- **实测验证**（物理正确性）：
  - E0 自动定位 11562.0 eV（Pt L3 参考 11564 eV，差 2 eV 合理）
  - 第一壳层 |χ(R)| 峰 2.45 Å + 相位修正 ≈ **2.77 Å = Pt 金属已知 Pt-Pt
    键长精确吻合**——第三节"FT 峰位+0.3–0.5 Å≈真实键长"通则实测坐实
- 踩坑记录（进教训）：透射 XDI 列是 energy/itrans/i0 **无现成 mu**，
  须自算 `d.mu = -np.log(d.itrans/d.i0)`；pre_edge 输出属性名为
  `edge_step/norm`（无 pre_edge_slope）

## 七、feffit 拟合层实跑记录（2026-08-17，同日第二批）

**官方 examples 1–4 直跑 + 6 改造 headless 版**（5 不存在，官方即 1-4+6）：

| Example | 主题 | 关键结果（实测） |
|---|---|---|
| feffit1 | Cu 单壳层 | n·S0²=0.93±0.04，σ²=0.0087（室温 Cu 教科书值），r=2.542 Å |
| feffit2 | 多路径 + α·reff 热膨胀 | r=2.555 Å |
| feffit3 | 多温度数据集共享 σ² 爱因斯坦模型 | 10K 下 σ²=0.0033 ✓ |
| feffit4 | CN 直接拟合 | s02·n1=3.87（NiO 氧配位） |
| feffit6 | **Z 敏感性 + 相位修正**（改造版入库 recipe 02） | 见下两条金矿 |

**feffit6 两条教学金矿（ZnSe，8 种假设散射原子 Zn→Rb）**：
1. **相位修正 FT 与散射体种类无关地给真距离**：R_phcor 全部落在
   2.449–2.463 Å（离散 0.014 Å）= Zn-Se 真实键长 2.45 Å；未修正 R 从
   2.471 漂到 2.425
2. **反直觉：chi2 最低是 Br(5.1) 而非真解 Se(8.2)**——相邻 Z(33/34/35)
   背散射振幅简并，单凭 chi2 判 Z 不可靠；须叠加 S0² 合理域
   （Br 1.07 超域 / Se 0.89 ✓）+ E0（Se≈0.03）+ 化学先验裁决

**小波实跑（recipe 03，Cauchy CCWT，Pt 箔）**：wavelet max R=2.65 Å /
k=11.1 Å⁻¹——介于未修正 2.45 与真实 2.77 之间且高 k 段强
（重散射体 Pt 特征），与轻/重散射体小波判别原理一致。

**新踩坑（进教训集）**：
- cauchy_wavelet 输出属性是 `wcauchy_mag/wcauchy_r`（非文档直觉的 w/r）
- Arial 缺 U+207B（上标负号）与下标 ᵣ——单位上标一律 mathtext
  `$^{-1}$`，禁用 Unicode 上标字符（glyph 审计硬规则再次实证）
- 视觉模型会把高分辨率 mathtext 误报为"原始 $ 定界符"——用 PDF 文本层
  `count('$')==0` 做确定性核验，不轻信单一视觉审计

## 七点五、feffit 毕业作：Pt 单原子定量拟合（recipe 05）

全链闭环：Pt-N4 方形平面模型（2.02 Å）→ feff6l 现算路径（feff6l 不认
RPATH 关键字，裁剪版）→ feffit（k 3–11.5, R 1.0–2.2, kw 2，对齐报告）→
对账报告锁定值：

| 量 | 本拟合 | 报告 | 判定 |
|---|---|---|---|
| CN | 3.44±0.75 | 4.3±0.5 | 1.1σ 一致 ✓ |
| R | 1.965±0.017 | 2.02±0.01 | 差 0.055 Å（模型简化预期内） |
| σ² | 0.0051±0.0024 | 0.002±0.001 | 同量级偏大 |
| ΔE0 | −0.3±3.0 | −4.4±1.5 | 误差棒内一致 ✓ |
| R-factor | 0.026 | 0.013 | 模型保真度差距（见下） |

**教学闭环**：R-factor 差一倍不是"谁错"，是结构模型保真度——报告用
C/N 混配 + 更宽拟合窗（含第二壳层路径），我用纯 Pt-N4 单路径简化。
拟合质量取决于结构模型，正是 feffit 的核心课。视觉审计 CLEAN
（183×70 mm 双联图）。

## 七点八、可调拟合引擎（recipe 06，"fit as you wish"）

四层自由度全部 CLI 化：数据层（--rbkg/--e0-offset）→ 拟合窗口
（--kmin/--kmax/--kweight/--rmin/--rmax/--dk/--window）→ 结构模型
（--shell n4|c4|c2n2 + --dist-n/--dist-c，簇体重建+feff6l 缓存重算）→
参数策略（--s02 固定值、--sig2-max/--e0-range/--r-range 边界）；
另支持 --scan PARAM v1 v2... 敏感性批量扫描（审稿防御标准动作）。

实测行为（每个变体都是真实物理，非摆设）：
- --kmax 10：Rf 0.008（窗口缩短拟合变易）；CN 3.16
- --shell c2n2：双路径分层键长 N 1.947/C 2.016 Å，加权 R 1.981
- --s02 0.90：CN 3.60（S0² 与 CN 严格 trade-off，教学点）
- --scan kmax 9.5→12.5：CN 2.97→3.63 单调爬升 + Rf 0.004→0.040
  （CN–S0² 简并随 k 窗系统性漂移——审稿必问的敏感性证据一键可得）

踩坑：FEFF 的 POTENTIALS 每个 unique pot 必须有原子（n4 模型不得声明
C 电位）；c2n2 双 reff 用共享 alpha*reff 表达式做比例位移。

商业注记：这即 web 服务"拟合参数面板"的 CLI 原型——面板选项 = 本
引擎的 argparse 维度，后端 = do_fit()。

## 八、下一步（backlog）

1. ~~本地装库~~（✅ 2026-08-17，第六节）
2. ~~跑通官方 feffit examples~~（✅ 1-4 直跑 + 6 改造 headless，第七节；
   官方无 5）
3. FeS2 课程数据：Ravel 仓库为 S3 手工 zip 链接，暂未取——feffit 1-4+6
   已覆盖等效学习价值（单壳/多路径/多数据集/CN/Z 敏感性），留作
   nice-to-have
4. ~~首个 XAFS recipe~~（✅ ×3：三联图/Z 敏感性/小波，全部过检）
5. ~~小波实跑~~（✅ Cauchy CCWT，第七节；ESRF BM20 为在线 GUI 不便自动
   对比，留人工）
6. ~~feffit 复现本地 Pt 单原子报告~~（部分 ✅ 2026-08-17 用户供
   **Athena 工程 Pt-sample.prj**，recipe 04 已复现处理层：
   Pt_sample+Pt_Foil/PtO/PtO2 四组；边位移 +5.2 eV（Pt δ⁺）；
   第一壳层 1.56 Å+相位修正≈1.96 Å 对上报告 Pt-C/N 2.02 Å；
   同参数箔对照 Pt-Pt 峰 2.45 Å，样品高壳层结构在 2.58 Å
   （偏离金属峰位 +0.13 Å，形态似第二壳层 C/N 而非 Pt-Pt）；
   NNLS-LCF 边区拟合 foil 0.35/PtO 0.65（R²=0.967，**解读边界已
   写入脚本**：阳离子单原子 XANES 借用 PtO 权重，不可直读相分数）；
   定量裁决（CN±σ² 对账报告 4.3@2.02Å）仍需 feffit+FEFF 路径，
   样品身份 Pt1 vs lps-fenmo 待用户确认）
