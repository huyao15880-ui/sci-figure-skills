# Gap Analysis — 不足清单与解决方案映射

> 2026-08-17 基于 NC 投稿全流程实战 + GitHub 生态调研。
> 每条不足标注：现状证据 → 生态对标 → 解决路径。诚实边界：以下"生态对标"
> 结论来自公开搜索，未逐一复测其功能细节。

## G1 规则是散文，不是代码

**现状**：排版纪律散落在 SKILL.md 文本里，agent 每次现场解释执行——
质量方差存在（skill 已大幅压缩但未消除）；无法脱离 agent 运行。
**对标**：[SciencePlots](https://github.com/garrettj403/SciencePlots)（~7k
stars，`pip install SciencePlots` 后 `plt.style.use(['science','nature'])`）
把样式做成 .mplstyle 分发；但其 2023 年末停更、且只管样式不管审计。
**路径**：把 matplotlib skill 的 rcParams 配方编译成
`styles/nc.mplstyle / nature.mplstyle / ieee.mplstyle` + `scifig` Python
包（样式 + 面板字母/CI 带/浓度色映射等高频函数）。**差异化不在样式**
（红海），样式包只是分发壳。

## G2 四查审计是清单，不是工具（最高优先）

**现状**：页内性/字体白名单/负号审计/字号实测/IoU 复核写成文档，
靠 agent 现场写检查代码——每次实现略异，且无法给外部用户独立使用。
**对标**：调研未发现专门的投稿图 PDF 审计开源工具；生态只有
`pdffonts`（Poppler，仅字体嵌入）、`pikepdf`（底层库，需自写逻辑）。
**这是确认的空白**。
**路径**：`figcheck` CLI——输入 PDF，输出 PASS/FAIL 报告
（页内性/字体白名单/负号/字号实测下限/墨迹边界/MediaBox 裁切风险）。
**它是商业化的核心资产**：免费图到处有，"投稿技术审查预检"没有。

## G3 依赖 agent 会话，无 headless 管线

**现状**：必须开 Claude Code/Codex 会话跑 skill。
**路径**：Agent SDK / CLI headless 封装成服务端 worker（数据 → 队列 →
产物 + figcheck 报告）。MVP 可先用"半自动"：网站收单，本地 agent 执行。

## G4 无交互改图回路

**现状**：改一处 = 重跑脚本，用户（尤其非编程背景的生物/艺术用户）
无法自助微调。
**对标**：BioRender 的拖拽 + 即时预览是用户体验基准。
**路径**：v1 用参数面板（图型/色板/字号/尺寸下拉）+ 重渲染；
v2 才考虑画布级交互。生物/艺术设计两个领域对交互的敏感度高于纳米材料。

## G5 领域模板不均（生物/艺术设计近空白）

**现状**：电化学/DFT 深度实战；生物（生存/剂量响应/热图）与艺术设计
（graphical abstract/海报）只有规范框架，无配方积累。
**对标**：[Bioicons](https://bioicons.com)（2700+ 开源 SVG 图标）、
[SciDraw](https://scidraw.io)（CC-BY + DOI）素材库可直接整合进
scientific-schematics 的组合路线，替代部分 AI 生图（更快且风格稳定）。
**路径**：domains/ 适配层已建（本版本），下一步按领域补 recipes/——
每个领域 3-5 个高频图型配方即可撑起服务菜单。

## G6 CJK（中文期刊）支持未系统化

**现状**：Arial 白名单体系没有中文字体方案；中文图会触发字体回退。
**对标**：社区 skill（scipilot）有 CJK 字体自动配置思路。
**路径**：中文字体白名单（思源黑体/宋体系）+ matplotlib 双字体配置
配方，进 art-design PROFILE 与 figcheck 白名单。

## G7 无基准测试（benchmark）

**现状**："我们比 GPT 直出好"是实战体感，无量化证据。
**路径**：建 20 个跨三领域典型数据集基准 → 同题三跑（我们 / GPT 直出 /
SciencePlots 默认）→ figcheck 通过率 + 编辑修改次数对比。
既是产品验证也是营销素材。

## G8 视觉 QA 依赖多模态模型（贵且慢）

**现状**：重叠/错位检测靠视觉模型审图。
**路径**：确定性检测先行（PDF 文本层 bbox 与数据墨迹 bbox 交集 =
文字-数据重叠；图例框 vs 点群包围盒）——可编码的先编码，视觉模型
只兜底审"美学"维。这直接降服务成本。

---

## 优先级（投入产出排序）

| # | 事项 | 定位 |
|---|---|---|
| P0 | G2 figcheck CLI | 商业核心资产 + 空白确认 |
| P0 | G5 三领域各 3-5 配方 | 服务菜单的最小可售集 |
| P1 | G1 样式包编译 | 分发壳（PyPI 引流） |
| P1 | G8 确定性重叠检测 | 降本（服务毛利） |
| P2 | G3 headless / G4 交互 / G7 基准 | 规模化前置件 |
