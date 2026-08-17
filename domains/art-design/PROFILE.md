# Domain Profile: 艺术设计（Art & Design）

艺术设计向的图件适配档案——服务学术传播场景（graphical abstract、封面设计、
学术海报、数据可视化美学）。skill 通用规则见 `skills/`，本页只放领域增量。

## 场景 → 产出 → skill 映射

| 场景 | 典型产出 | 主 skill | 备注 |
|---|---|---|---|
| Graphical abstract | 单幅 183mm 概念图 | scientific-schematics + toolchain | 文字转曲后投递 |
| 期刊封面候选 | 装置/结构艺术图 | scientific-schematics | 分辨率 ≥300dpi 全幅 |
| 学术海报 | A0/A1 多栏排版 | sci-figure-toolchain（Inkscape） | 矢量优先 |
| 数据可视化美学 | 高质量数据图 | matplotlib + sci-figure-plot | 色彩纪律见下 |
| 信息图/流程图 | 概念图 | scientific-schematics | 评分环阈值可调 8.0 |

## 色彩纪律（本仓库全领域生效，艺术设计领域负责定义）

- **色盲安全**（~8% 男性红绿色盲）：分类色 Okabe-Ito 十色为默认；
  禁 red-green 双色编码关键信息
- **连续色标**：viridis 系（感知均匀）或 crameri scientific colour maps
  （batlow/roma/berlin 等）；禁 rainbow/jet（感知失真 + 色盲不可分）
- **发散色标**：RdBu / crameri Roma，中点必须对应数据中点（0 或中位数），
  两端对称
- **明度层级**：同图内信息层级用明度差（L* 差 ≥25）表达，不只靠色相
- **打印安全**：关键对比在灰度下仍可分（转灰度抽查——CMYK 印刷防线）

## 排版纪律

- **字体层级**：同一交付物 ≤2 字族；标题/正文/标注三级明度+字号区分
- **网格系统**：多元素排版先定网格（海报 12 栏 / abstract 三分法），
  元素对齐网格，禁自由摆放
- **留白**：概念图元素间距 ≥ 元素尺寸 15%；拥挤 = 降级
- **视觉动线**：graphical abstract 读序左→右（或符合语言方向），
  箭头引导，终点放结论
- **文字转曲**：对外交付的 SVG/PDF 一律 `--export-text-to-path`
  （见 toolchain §4），防字体环境缺字

## 领域专属审计增量（并入四查）

- 灰度转换抽查（关键对比仍可分）
- 色相区分抽查（两色在 CIELAB ΔE ≥ 20 或形状/明度辅助编码）
- 图内文字层级 ≤3 级
- 视觉评分环（scientific-schematics 五维）阈值：学术投稿 8.5 / 传播物料 8.0

## 常见坑（领域专属）

- 生图素材风格漂移（同图多元素跨风格）→ prompt 锁风格句式 + 逐张像素预检
- 位图放大失真 → 素材 1:1 置入，需要大图重新生成不插值
- 屏幕好看打印糊 → sRGB → CMYK 关键色打样检查（红/亮蓝最先翻车）
