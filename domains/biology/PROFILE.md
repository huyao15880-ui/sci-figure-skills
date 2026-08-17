# Domain Profile: 生物（Biology / Life Sciences）

生物领域的图件适配档案。skill 通用规则见 `skills/`，本页只放领域增量。

## 数据类型 → 图型 → skill 映射

| 数据类型 | 典型图型 | 主 skill | 备注 |
|---|---|---|---|
| 生存数据 | Kaplan-Meier 曲线 + risk table | sci-figure-plot | log-rank p 进图注 |
| 剂量响应 | 四参数 logistic 拟合 + IC50 | sci-figure-plot | CI 带必带 |
| 组间比较 | 小提琴/箱线 + 散点叠放 | sci-figure-plot | n<8 禁柱状图，见下 |
| 高维矩阵 | 热图 + 层次聚类树 | sci-figure-plot | 色板禁 rainbow（见下） |
| 差异分析 | 火山图 | sci-figure-plot | 显著阈值线标注 |
| 流式/wb 定量 | 配对点图 | sci-figure-plot | 配对标记全水平躲让 |
| 机制/通路示意 | 概念图 | scientific-schematics | BioRender 风格基准 |
| 多面板正文图 | 组图 | sci-figure-compose | 生命科学期刊双栏 ~180mm |

## 领域规范增量

- **小样本纪律**：n<8 的组间比较禁柱状图（均值±SD 遮蔽分布），一律
  散点/小提琴展示每个观测；n 数标注在图内或图注（n=x per group）
- **统计标注**：p 值有效数字（p<0.001 而非 p=0.000）；多重比较注明校正方法；
  error bar 类型（SD/SEM/95%CI）必须在图注声明——不声明 = 不合格
- **色板（色盲安全）**：分类色用 Okabe-Ito；连续色用 viridis/crameri 系；
  红 green 组合（如 heatmap 双向发散）改用 colorbrewer RdBu 或 crameri
  Roma/Berlin；详见 `domains/art-design/PROFILE.md` 色彩章节
- **示意图风格**：机制图/通路图按 BioRender 风格基准（柔和粉彩填充 +
  统一深灰轮廓 + 扁平现代），评分阈值见 scientific-schematics
- **伦理边界**：涉及患者/动物数据的图，脱敏检查进四查审计（图内不得出现
  ID/日期可回溯信息）

## 领域数据集

本地数据集按 `datasets/DATASET_INDEX.md` 规范注册。生物典型形态：
生存长表（time, event, group）、剂量响应（dose, response, replicate）、
表达矩阵（gene × sample，附注释列）。

## 常见坑（领域专属）

- KM 曲线 censoring tick 必须画（|），不画 = 隐瞒删失
- 热图行/列注释条与主热图对齐（共享轴，禁独立缩放）
- 显微图比例尺（scale bar）必须有且单位明确，禁"图中标尺在图注"式偷懒
