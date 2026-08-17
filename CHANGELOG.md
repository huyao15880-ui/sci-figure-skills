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

### 补充（08-18 九批）

- **全套同步辐射资产补齐**（用户第三次推动）：微信存储区找到并抢救
  Fe K 边标样套 athena.prj（Fe_foil/FeO/Fe3O4/Fe2O3）+ 委托单；md5
  去重（重复传输件）；资产清单入笔记
- **recipe 13 Fe 方法栈**：四标样 XANES 叠图、边位-价态标定曲线
  （~4.7 eV/价态，R²>0.99）、一阶导叠图、LCF 自一致性验证（合成
  70/30 恢复零误差）；figcheck ALL PASS

### 补充（08-18 八批）

- **figcheck CLI MVP 发布**（GAP G2 P0 清偿）：六项投稿就绪审计
  （页内墨迹/字体白名单/负号/字号实测/关键词/页面尺寸），CI 退出码，
  `--journal nature` 字号下限档位
- 自测双杀：抓 Origin 导出 SimSun（预期）+ 抓到本仓库自己三联图的
  4.6pt mathtext 下标（意外收获——工具审计自己人）；注记升 7.2pt 后
  ALL PASS
- 漏项盘点入册：谱图族/生物配方（P0）、注册表提交（P1）、3D（P1）、
  论文 Fig2 XAFS 升级（待用户决策）、SAXS/原位 XRD（待选）

### 补充（08-18 七批）

- **"什么才是好拟合"完整答案**（用户二次质疑驱动）：三重贴合金标准
  全量化（k 空间 corr 0.99/幅值峰比 1.04/实部 corr 0.994）；三路径
  胜选模型（Pt-N@1.95+Pt-C@2.08 混配+C 第二壳层）Rf=0.0128 优于报告
  0.013；recipe 12 + 三重贴合图（首次含 Re χ(R)）
- **CN 差异的诚实归因**：与报告 4.3±0.5 的差距非 S0² 口径（约束验证），
  是路径简并（单路径误差 ±0.29）；CN 报告纪律 = 模型说明 + 误差棒
- 高 k 段（9–11.5）贴合受限 = 数据 SNR 边界（rms 0.12 弱信号），非模型错

### 补充（08-18 六批）

- **审美返工**（用户"还很丑"）：视觉总监诊断五要素（死留白/细线/小字/
  黑框图例/生硬饱和色）→ matplotlib 精修三联（183×64mm：低饱和海军蓝
  #2C5F8A+绯红#B0413E+金色标样、数据区浅填充、虚线拟合、阴影拟合窗、
  无框图例）——艺术总监复审 **PUBLISHABLE**
- **分工纪律执行**：Origin .opju 的所见即所得样式（页面比例/字体/线宽）
  LabTalk 深度样式实测静默无效 → 按既有纪律停止排版层死磕，opju 美化
  交人工 2 分钟（其本就是客户可编辑源文件）；matplotlib 版是投稿默认
- 新坑：expGraph 需会话内有活动图（空会话导出静默失败）；样式属性
  （page.width/axislinewidth 等）经 lt_exec 返回 OK 但不落地

### 补充（08-18 五批）

- **拟合质量研究闭环**（用户在 Origin 中发现高壳层未拟合）：单壳层全窗
  基线 Rf=0.054 → 双壳层（Pt-N + 第二壳层 C@2.93）→ **rbkg 敏感性扫描
  （1.25 = Athena 默认最优）→ 终局 Rf=0.0169 < 0.02**，壳层残差
  0.5%/4.7%，全范围贴合；CN 2.4+1.3 与报告 4.3±0.5 在 1σ 内
- recipe 10 定稿（rbkg=1.25 + σ²_C 自由）；模板 opju Graph2 已用
  新拟合刷新

### 补充（08-18 四批）

- **Origin 模板工程 .opju 交付定型**（recipe 09）：前人样式内建的双页
  模板（XANES 叠图 + R 空间蓝/红拟合），客户交付物 = 可编辑 .opju 原文件；
  CLI 复开验证（4 pages/2 graphs 各 2 plots）
- 新坑入册：`save -i` 产出 .oggu 非 .opju；LabTalk save 静默失败 →
  一律 `op.save(path)`；expGraph 只导活动图；SimSun 首次交付前人工
  2 分钟统一字体（doc -e LBL 批量替换无效）

### 补充（08-18 三批）

- **前人 Origin 模板提取与复刻**：data/raw/Figure 7 张 WMF 转换 + 4 张
  视觉交叉分析 → docs/ORIGIN_TEMPLATE_SPEC.md（蓝#1F77B4数据/红#D62728
  拟合配对、1.5–2pt 实线、拟合图四边框内向刻度、XANES 开放框、轴题
  照抄文本、小波 jet+colorbar；字体统一 Arial 的融合决策注明）
- recipe 08 复刻图（183×130mm 四联：XANES/k²χ(k)拟合/R空间拟合带注记框/
  jet 小波）——模板应用到我们自己的 Pt_sample 分析，视觉审计 CLEAN

### 补充（08-18 二批）

- **Origin 出图全链打通**（recipe 07）：originpro from_list 填数 →
  plotxy 双曲线 → LabTalk 样式 → expGraph 导出 → PyMuPDF 183mm 规格化，
  PDF 183×140mm 内容完整（XANES 双曲线+图例+轴题+Origin 四边框内向刻度）
- **matplotlib 仿 Origin 主题**对比版（183×130mm，四边框/内向刻度/
  框图例/Arial）——无 Origin 环境的可规模化路线
- **字体审计关键发现**：中文版 Origin 导出 PDF 字体 = SimSun（投稿
  不合格）→ 投稿走 matplotlib 主题版或 Origin 模板层改字体
- 坑册沉淀进 sci-figure-toolchain（会话寿命/impASC 分块/plotxy 语法/
  page 尺寸 0.4mm 空页/SimSun 字体五坑全记录）

### 补充（08-18 一批）

- **XAFS 期刊风格交付报告**（xafs_report_builder.py）：Athena 工程 →
  Word 报告一键生成——双图（XANES 四联证据图 + EXAFS 拟合图）、
  Table 1 拟合参数对账表（vs 报告锁定值）、Table 2 处理参数复现表、
  三条边界声明（LCF 解读/高壳层归属/样品身份假设）、复现命令清单；
  全部拟合数值运行时从可调引擎拉取（零硬编码），自检 2图2表图注
  计数通过，Word 渲染 QA 2 页无溢出。产品形态：客户 .prj → 本报告

### 补充（同日八批）

- **可调拟合引擎**（recipe 06 xafs_feffit_pt_configurable.py）：四层自由度
  CLI 化（数据层 rbkg / 拟合窗口 k·R·kw·dk·window / 结构模型
  n4|c4|c2n2+键长 / 参数策略 S0² 固定·边界），feff6l 按几何哈希缓存；
  --scan 敏感性批量扫描。实测四变体全部给出真实物理行为（kmax 敏感性
  CN 2.97→3.63 单调漂移 = CN-S0² 简并的审稿级证据）
- 新坑：FEFF POTENTIALS 每 unique pot 必须有原子；双 reff 路径用共享
  alpha*reff 比例位移

### 补充（同日七批）

- **feffit 毕业作**（recipe 05）：Pt-N4 方形平面模型（2.02 Å）→ feff6l
  现算路径（踩坑：feff6l 裁剪版不认 RPATH）→ feffit 报告条件拟合 →
  对账锁定值：CN 3.44±0.75 vs 4.3±0.5（1.1σ 一致）、ΔE0 误差棒内一致；
  R/σ²/R-factor 差距定位为模型保真度（纯 N 单路径 vs C/N 混配+宽窗）
- 183×70 mm 双联拟合图（k 空间+R 空间叠图带统计框），视觉审计 CLEAN
- XAFS 学习线至此全链毕业：读谱→归一化→背景→FT→LCF→小波→FEFF→feffit

### 补充（同日六批）

- **Pt 单原子真实数据复现**（用户供 Athena 工程 Pt-sample.prj，recipe 04）：
  四组（Pt_sample/Pt_Foil/PtO/PtO2）；边位移 +5.2 eV（Pt δ⁺ 判据）；
  第一壳层 1.56 Å + 相位修正 ≈1.96 Å 对上报告 Pt-C/N 2.02 Å；
  同参数箔对照：Pt-Pt 峰 2.45 Å vs 样品高壳层结构 2.58 Å（偏离
  +0.13 Å，非典型金属位）；NNLS-LCF foil 0.35/PtO 0.65（R²=0.967，
  单原子借用 PtO 权重的解读边界已写入脚本注释）
- 183×120 mm 四联图（XANES 叠图/边区放大/k²χ(k)/R 空间+Pt-Pt 区标注）
- 待办：feffit 定量（CN±σ² 对账 4.3@2.02Å）需 FEFF 路径 + 样品身份确认

### 补充（同日五批）

- **feffit 拟合层全实跑**：官方 examples 1-4 直跑（Cu 单壳/多路径热膨胀/
  多温度共享 σ²/CN 拟合）+ feffit6 改造 headless 版入库（recipe 02，
  ZnSe 八散射原子 Z 敏感性，2x4 面板图 183mm，视觉审计 CLEAN）
- **两条教学金矿**：相位修正 FT 在全部 8 种假设下收敛 2.449-2.463 Å
  精确锁死 Zn-Se 2.45 Å；chi2 最低是 Br 而非真解 Se（相邻 Z 简并）——
  判散射原子须 chi2 + S0² 合理域 + 化学先验三重裁决
- **recipe 03**：Cauchy 小波（Pt 箔，max R=2.65 Å/k=11.1，重散射体
  高 k 特征），单栏 89mm 色图，glyph 审计零警告
- 新踩坑入库：cauchy_wavelet 输出属性名、Arial 缺 U+207B/ᵣ（单位上标
  一律 mathtext）、视觉模型误报 mathtext 用 PDF 文本层核验
- Pt 单原子复现确认待数据（无 OPJ/原始 μ(E)）；FeS2 课程数据留
  nice-to-have（S3 手工链接）

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
