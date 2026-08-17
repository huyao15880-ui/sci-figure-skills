# Sci-Figure Skills

**Agent 原生的科研绘图流水线** —— 从 CSV 数据到期刊级 183 mm 投稿 PDF 的一组 [Claude Code](https://claude.com/claude-code) / Codex / Cursor skills。

An agent-native pipeline of skills that turns prepared data into publication-grade figures — mm-exact final-size PDFs that survive journal technical screening, produced by your coding agent under strict plotting discipline.

## 为什么需要它

通用 AI 对话能产出"能看"的 matplotlib 代码，但普遍过不了期刊技术审查：字号在缩放后失真、负号不是 U+2212、字体未嵌入、面板字母位置随意、组图各面板坐标系不一致、**图上数字与正文数值对不上**。这套 skill 把这些教训固化为 agent 可执行的硬规则。

核心原则（在真实投稿流程中反复验证）：

- **最终坐标系原则**：`figsize = 最终mm / 25.4`，禁止中间尺寸制作再统一缩放；`savefig` 不做 tight 裁剪，PDF 页面即最终交付物
- **期刊排版纪律**：Arial + custom mathtext（防 DejaVu 回退）、`pdf.fonttype 42`、U+2212 负号、8 pt 粗体面板字母、mm 级组图拼版
- **数值一致性**：图上注记运行时从冻结数据文件读取，零硬编码，打印验证值与图注锁定值逐一对账
- **视觉 QA 闭环**：生成 → 视觉审计定位缺陷 → 修复 → 复审 CLEAN 才交付
- **矢量保真**：.ai 衍生物由已验证主交付物转换生成并 round-trip 复核（IoU ≥ 0.95），不并行独立重建

## Skills 一览

| Skill | 阶段 | 职责 |
|---|---|---|
| [`scipilot-figure-skill`](https://github.com/Haojae/scipilot-figure-skill)* | 0 · 选型 | 画图前先想：图型选择顾问，拦截小样本柱状图、双轴滥用、彩虹色带等经典错误 |
| `scientific-schematics` | 1 · 示意图 | 概念图/机理图/流程图：AI 生图 + 独立视觉评分迭代，BioRender 风格规范 |
| `sci-figure-plot` | 1 · 数据图 | 单面板绘制：DFT PDOS / 电化学曲线等，从 CSV 到单面板矢量 PDF |
| `matplotlib` | 1 · 引擎 | rcParams 纪律、期刊排版配方、savefig 配方、易错规则清单 |
| `sci-figure-compose` | 2–4 · 组图 | 多面板期刊组图：1:1 mm 精确拼版、坐标轴对齐、行基线字母、四查审计、.ai round-trip |
| `sci-figure-toolchain` | 0/4 · 工具链 | Inkscape 拼版、字体转曲、矢量导出；Origin/MATLAB/COMSOL/Illustrator CLI 取数 |
| `scientific-visualization`* | ∞ · 审计 | 已画图的诚实性/可及性审计：色彩对比、缺失数据、元数据 |

\* 推荐搭配的第三方开源 skill（非本仓库内容，各自独立发布）：选型顾问见 [Haojae/scipilot-figure-skill](https://github.com/Haojae/scipilot-figure-skill)，审计思路改编自 [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)。

## 安装

把 `skills/` 下任意目录复制进你的 agent skills 目录：

```bash
git clone https://github.com/huyao15880-ui/sci-figure-skills.git
cp -r sci-figure-skills/skills/* ~/.claude/skills/     # Claude Code
# 或 ~/.zcode/skills/ / ~/.agents/skills/（Codex 等）
```

对 agent 说"用 sci-figure-plot 画这个 CSV"或"用 sci-figure-compose 组这 6 个面板"，skill 自动加载。

依赖：Python 3.9+、matplotlib、numpy、pandas、scipy；组图与工具链另需 PyMuPDF / Inkscape（可选 Origin/MATLAB/COMSOL CLI）。

## 典型工作流

```
冻结 CSV ──► 阶段1 单面板 PDF（最终 mm 规格）
              │
              ├─► 阶段2-4 组图：mm 精确拼版 + 面板字母 + 四查审计 ──► 主图 PDF/.ai
              └─► 视觉 QA 闭环（审计→修复→复审）
```

一个真实产出（Nature Communications 投稿规格，183 mm 双栏，agent 全程自治完成）：

```python
# 最终坐标系：页面即交付物，无事后缩放
fig, axes = plt.subplots(2, 3, figsize=(183/25.4, 120/25.4), constrained_layout=True)
# 字体/负号/嵌入全部锁定
mpl.rcParams.update({"font.family": "Arial", "pdf.fonttype": 42,
                     "mathtext.fontset": "custom", "mathtext.rm": "Arial"})
fig.savefig(out)   # 无 bbox_inches="tight" —— 183.00 mm 就是 183.00 mm
```

## License

MIT —— 见 [LICENSE](LICENSE)。
