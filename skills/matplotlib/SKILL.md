---
name: matplotlib
description: "[阶段1·绘图引擎] Low-level matplotlib control for publication figures: rcParams discipline, journal typography (Arial mathtext, U+2212 minus, tight pad), marker dodge rules, savefig recipe. Use when a panel needs fine-grained plot-element control beyond what higher-level figure skills cover. Rebuilt 2026-08-17 after cleanup (original community copy lost; content includes battle-tested additions)."
---

# matplotlib — publication-grade plotting engine

Fine-grained control for every plot element when higher-level skills
(sci-figure-plot for panels, scipilot for chart advice) need engine-level detail.

## Journal typography recipe (rcParams)

```python
plt.rcParams.update({
    'font.family': 'Arial', 'font.size': 5.5,        # ticks; labels 6, in-plot 6.5 bold
    'axes.linewidth': 0.35, 'pdf.fonttype': 42,       # TrueType embed, no Type3
    'figure.facecolor': 'white',
    'mathtext.fontset': 'custom',                     # else DejaVu fallback!
    'mathtext.rm': 'Arial', 'mathtext.it': 'Arial:italic', 'mathtext.bf': 'Arial:bold',
})
```

## Savefig recipe

```python
fig.savefig(out, bbox_inches='tight', pad_inches=0.02)  # default pad 0.1in = 2.54mm borders!
```

Draw at FINAL size: `figsize = target_mm / 25.4`. Never rescale afterwards.

## Hard rules (violations found in real review loops)

- **U+2212 minus** everywhere: f-strings produce ASCII `-` →
  `s.replace('-', chr(8722))`; tick labels are U+2212 by default (`unicode_minus`)
- **No vertical stacking of paired markers**: dodge every
  (group × condition) to its own x offset
- **Compute bounding boxes** before placing text/legends; leave gaps
- Glyph audit: Arial lacks many symbols (✓ ≪ …) — check before use or fall
  back to shapes/Unicode basics (² ³ · × − →)
- constrained_layout OR tight_layout, never both; `align_ylabels` for shared rows
- `set_constrained_layout_pads(hspace=..., wspace=...)` to tighten grids
