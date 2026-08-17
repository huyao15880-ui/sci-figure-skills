# Sci-Figure Skills

**Agent 原生的科研绘图流水线** —— 专为**纳米材料 / 生物 / 艺术设计**三领域适配，从数据到期刊级 mm 精确投稿 PDF，且**随使用成长**的一组 [Claude Code](https://claude.com/claude-code) / Codex / Cursor skills。

An agent-native, domain-adapted (nanomaterials · biology · art & design) pipeline of skills that turns data into publication-grade figures — mm-exact final-size PDFs that survive journal technical screening — with a growth mechanism that makes the repo stronger with every real figure.

## 为什么需要它

通用 AI 对话能产出"能看"的图，但普遍过不了期刊技术审查：字号缩放失真、负号不是 U+2212、字体未嵌入、面板字母随意、组图坐标系不一致、**图上数字与正文对不上**。这套 skill 把这些教训固化为 agent 可执行的硬规则，全部来自真实投稿返工循环。

核心原则（Nature Communications 投稿全流程验证）：

- **最终坐标系原则**：`figsize = 最终mm / 25.4`，禁止中间尺寸制作再缩放；PDF 页面即交付物（实测 183.00 mm 就是 183.00 mm）
- **期刊排版纪律**：Arial + custom mathtext（防 DejaVu 回退）、`pdf.fonttype 42`、U+2212 负号、8 pt 粗体面板字母、mm 级组图拼版
- **数值一致性**：图上注记运行时从冻结数据文件读取，零硬编码，与图注锁定值逐一对账
- **视觉 QA 闭环**：生成 → 视觉审计定位缺陷 → 修复 → 复审 CLEAN 才交付
- **矢量保真**：.ai 衍生物由已验证 PDF 转换生成并 round-trip 复核（IoU ≥ 0.95）

## 仓库结构

```
skills/          5 个 skill（阶段化流水线）
domains/         三领域适配层：纳米材料 / 生物 / 艺术设计
  └─ PROFILE.md  数据类型→图型→skill 映射 + 领域规范增量 + 领域坑
datasets/        本地数据集注册规范（数据不进仓库、索引进、冻结纪律）
growth/          成长性机制：配方/教训/数据集三通道沉淀 + 版本规则
docs/            GAP_ANALYSIS（不足与解决映射）· COMMERCIALIZATION（商业化路线）
```

## Skills 一览

| Skill | 阶段 | 职责 |
|---|---|---|
| `scientific-schematics` | 1 · 示意图 | 概念图/机理图：AI 生图 + 独立视觉评分迭代环 |
| `sci-figure-plot` | 1 · 数据图 | 单面板：DFT PDOS / d-band / POSCAR / CHGDIFF / 电化学曲线 / 校准统计 |
| `matplotlib` | 1 · 引擎 | rcParams 纪律、期刊排版配方、savefig 配方、易错规则 |
| `sci-figure-compose` | 2–4 · 组图 | mm 精确 PDF-on-PDF 拼版、四查审计、短绳纪律、.ai round-trip |
| `sci-figure-toolchain` | 0/4 · 工具链 | Inkscape 矢量导出/字体转曲；Origin/MATLAB/COMSOL CLI 取数 |

推荐搭配（第三方，独立安装）：选型顾问 [Haojae/scipilot-figure-skill](https://github.com/Haojae/scipilot-figure-skill)；示意图素材库 [Bioicons](https://bioicons.com) / [SciDraw](https://scidraw.io)（CC-BY）。

## 三领域适配

| 领域 | 高频场景 | 详见 |
|---|---|---|
| 纳米材料 | DFT/表征/电化学组图、校准统计 | `domains/nanomaterials/PROFILE.md` |
| 生物 | 生存曲线/剂量响应/热图 + BioRender 风格机制图 | `domains/biology/PROFILE.md` |
| 艺术设计 | graphical abstract/封面/海报 + 全域色彩纪律 | `domains/art-design/PROFILE.md` |

## 安装

```bash
git clone https://github.com/huyao15880-ui/sci-figure-skills.git
cp -r sci-figure-skills/skills/* ~/.claude/skills/     # Claude Code
# 或 ~/.zcode/skills/ / ~/.agents/skills/（Codex 等）
```

对 agent 说"用 sci-figure-plot 画这个 CSV"或"用 sci-figure-compose 组这 6 个面板"。

依赖：Python 3.9+、matplotlib、numpy、pandas、scipy；组图与工具链另需 PyMuPDF / Inkscape（可选 Origin/MATLAB/COMSOL CLI）。

## 成长性

本仓库按 [`growth/CONTRIBUTING.md`](growth/CONTRIBUTING.md) 三通道沉淀：**配方**（这次怎么画成的）→ `skills/*/recipes/`；**教训**（错在哪、规则改了什么）→ SKILL.md 规则增量（能写成断言的必须 CODE 形态）；**数据集形态** → `datasets/DATASET_INDEX.md` 注册。每次实战让仓库单调变强。

## figcheck — 投稿就绪审计 CLI（已发布 MVP）

```bash
python code/figcheck/figcheck.py figure.pdf --journal nature --expect "Energy (eV)"
```
六项检查：页内墨迹 / 字体白名单（抓 SimSun·Type3·DejaVu）/ U+2212 负号 /
字号实测下限（Nature 5pt）/ 关键词在场 / 页面物理尺寸。CI 友好退出码。
自测记录：抓到 Origin 导出 SimSun、抓到本仓库自己图的 4.6pt 下标——修复后 ALL PASS。

## 路线图

不足清单见 [`docs/GAP_ANALYSIS.md`](docs/GAP_ANALYSIS.md)（G2 figcheck ✅ 已交付；
P0 剩余：谱图族+生物配方库；P1：3D 最小集 PyVista+OVITO）。图型全谱目录见 [`docs/CHART_CATALOG.md`](docs/CHART_CATALOG.md)。商业化三层路线见 [`docs/COMMERCIALIZATION.md`](docs/COMMERCIALIZATION.md)。

## License

MIT —— 见 [LICENSE](LICENSE)。示意图评分环方法论部分 adapted from [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)。
