---
name: matplotlib
description: "[阶段1·绘图引擎] matplotlib 底层排版纪律：rcParams 期刊配方（Arial mathtext、U+2212 负号、fonttype 42）、savefig 配方、标记躲让规则。上层 skill 需要引擎级细节控制时使用。"
version: 1.0.0
domains: [nanomaterials, biology, art-design]
---

# matplotlib — 投稿级绘图引擎纪律

对每个绘图元素做细粒度控制的底层规范。上层 skill（sci-figure-plot 画面板、
选型顾问定图型）需要引擎级细节时回到这里。全部规则来自真实返工循环验证。

## 期刊排版 rcParams 配方

```python
plt.rcParams.update({
    'font.family': 'Arial', 'font.size': 5.5,        # 刻度；轴题 6，图内 6.5 bold
    'axes.linewidth': 0.35, 'pdf.fonttype': 42,       # TrueType 嵌入，禁 Type3
    'figure.facecolor': 'white',
    'mathtext.fontset': 'custom',                     # 否则回退 DejaVu！
    'mathtext.rm': 'Arial', 'mathtext.it': 'Arial:italic', 'mathtext.bf': 'Arial:bold',
})
```

## savefig 配方

```python
fig.savefig(out, bbox_inches='tight', pad_inches=0.02)  # 默认 pad 0.1in = 四周 2.54mm 白边！
```

最终尺寸作画：`figsize = 目标mm / 25.4`，禁止事后缩放。
（整版组图例外见 sci-figure-compose：页面即交付物时不用 tight。）

## 硬规则（真实返工循环中的违规实录）

- **U+2212 负号**处处生效：f-string 产出 ASCII `-` →
  `s.replace('-', chr(8722))`；刻度标签默认已是 U+2212（`unicode_minus`）
- **配对标记禁垂直堆叠**：每个（组 × 条件）躲让到自己的 x 偏移
- 放文字/图例前**先算包围盒**，留间隙
- 字符审计：Arial 缺很多符号（✓ ≪ …）——用前检查，或回退
  基础形状/Unicode（² ³ · × − →）
- constrained_layout 与 tight_layout 二选一；同行共享轴 `align_ylabels`
- 网格收紧：`set_constrained_layout_pads(hspace=..., wspace=...)`

## 领域适配入口

- 纳米材料：DFT PDOS / 电化学曲线面板配方见 sci-figure-plot
- 生物：统计图（小提琴/生存/森林）同样适用本页全部排版纪律
- 艺术设计：色彩与字体层级规范见 `domains/art-design/PROFILE.md`
