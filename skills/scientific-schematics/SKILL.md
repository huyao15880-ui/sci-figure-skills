---
name: scientific-schematics
description: "[阶段1·示意图生成] 投稿级概念图/机理图/流程图：AI 图像生成 + 独立视觉评分迭代环。图是'画的'而非'数据画的'时使用。不做数据面板（sci-figure-plot）或组图（sci-figure-compose）。方法论参考 davila7/claude-code-templates 的 score-loop 思路，本地链路为 GPT 生图（cli-anything-gpt）+ 视觉模型复审。"
version: 1.0.0
domains: [biology, nanomaterials, art-design]
---

# scientific-schematics — AI 示意图生成（评分迭代环）

**核心原则：agent 不硬手画示意图**（matplotlib 盒子画概念图 = 业余感天花板）。
生成交给图像模型，agent 负责规格化 prompt + 独立视觉评分 + 迭代。

## 工作流（评分迭代环）

1. **Prompt 模板**（顺序固定）：类型 + 组件 + 流向 + 标签内容 + 风格约束
   - 必须具体：组件数量、层尺寸、方向（"vertical flow, top to bottom"）
   - 风格自动附加：白底、墨灰细线、无色无纹理（数据图另有色板）、
     无文字或仅英文短标签、Nature schematic 风格、留白充足
2. **生成**：`cli-anything-gpt ask -f prompt.txt --gen-image --output out.png`
   （先 `pool acquire`，逐张跑，完成后 `pool release`）；
   无该工具时用任意图像生成 API（images.generate 等价接口）
3. **独立评分**（视觉模型，五维 × 0–2 = /10）：
   科学准确性 / 清晰层级 / 标签质量 / 布局（无重叠、流向逻辑）/ 专业度
4. **阈值判据**（journal 级 8.5；低于阈值 → 按批评改 prompt 重生成，
   硬上限 2 轮迭代，防无限循环）
5. **像素预检**（评分前）：饱和度 <12（线稿）、四角 >245（白底）、
   尺寸 ≥1000px——风格不符直接重生成，不浪费评分轮
6. **组合**：素材（图标/装置）由 matplotlib 以 letterbox 站格置入 + 矢量
   文字/箭头连接（保持文字为矢量真文本，不烤进位图）

## 关键判据：整幅生成 vs 素材组合

- **多元素整图 → 整幅生成**（让图像模型自己排版）：
  agent imshow 缩放组合必掉精度（降采样模糊/灰底残留/比例失衡），
  素材再好组合也烂（两版实证）
- **单元素素材 → 仅作独立图标时才组合**（站格 letterbox + 矢量文字）
- **风格升级**：纯墨灰线稿性冷淡 → **BioRender 风格**（柔和粉彩填充 +
  统一深灰轮廓 + 扁平现代）——Nature 概念图行业标准，评分 8.8 vs 线稿 8.4

## 实测配方（4/4 过检）

- 素材提示词锁定句式："Minimalist scientific illustration, clean vector
  style, white background, thin ink-grey outlines only (no color, no shading,
  no texture). Subject: ... No text, no labels, no watermark."
- 生图 ~60–90 s/张；饱和度实测 0.1–0.3、四角纯白
- 文字层一律由 matplotlib 后置（Arial 矢量），位图里绝不含字
- 整幅概念图（多元素排版）失败率高：改为**单元素素材 + 代码组合**路线
  （图像模型出零件，agent 管网格与文字——各自干擅长的事）

## 边界
- 数据图 → sci-figure-plot；组图 → sci-figure-compose
- 需要严格几何（晶格/结构式）→ 考虑 schemdraw/NetworkX 代码绘制
- 评分用视觉模型必须真读图（返回"没有图片"= 重试或换 URL 编码）
- 致谢：评分迭代环方法论 adapted from davila7/claude-code-templates
  （scientific-schematics），本地链路与配方为自有实测
