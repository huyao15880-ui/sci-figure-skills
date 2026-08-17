---
name: sci-figure-toolchain
description: "[阶段0/4·科研软件CLI工作链] Inkscape 无头拼版/字体转曲/矢量导出，Origin(COM/LabTalk)/MATLAB(batch)/COMSOL(comsolbatch) 取数与计算 CLI 配方，含各软件原生崩溃点绕行。正文组图请用 sci-figure-compose。"
version: 1.0.0
domains: [nanomaterials, biology, art-design]
---

# sci-figure-toolchain — 科研软件 CLI 工作链（真机实测版）

> 2026-08-15 本机全链路验证。各 CLI 均为「真软件后端」无 mock：调真实的
> Origin / MATLAB / COMSOL / Inkscape 进程。核心纪律：图件证据链完整——
> 源数据 → 脚本 → 产物可一键重建，禁 GUI 手工步骤。

## 0. 工具速查表（先选对工具）

| 需求 | 用哪个 | 入口 |
|---|---|---|
| 电化学/组图风格数据图（校准、柱状图） | **Origin** | `cli-anything-origin` |
| 数值计算、信号处理、快速探索 | **MATLAB** | `cli-anything-matlab` |
| 有限元仿真（电化学、多物理场） | **COMSOL** | `cli-anything-comsol` |
| 拼版、标注、graphical abstract、WMF 转换、字体转曲 | **Inkscape** | `cli-anything-inkscape` |
| 找其他软件的 CLI | cli-hub | `cli-hub search <关键词>` / `cli-hub can <能力>` |

**统一入口路径**（都不在默认 PATH）：
```bash
SCRIPTS="~/AppData/Roaming/Python/Python3XX/Scripts"   # pip --user 安装位
"$SCRIPTS/cli-anything-origin.exe" --json system info
"$SCRIPTS/cli-anything-matlab.exe"  --json eval "1+1"
"$SCRIPTS/cli-anything-comsol.exe"  --json system info
"C:/Program Files/Inkscape/bin/inkscape.exe" --version   # Inkscape 直连
```

**环境变量**：
```bash
export CLI_MATLAB_EXE="D:/Program Files/MATLAB/R20XXx/bin/matlab.exe"  # MATLAB
export CLI_COMSOL_BATCH=...   # 可选，COMSOL 默认自动发现 C:\Program Files\COMSOL
# CLI_MATLAB_EXE 不设时 backend 自动扫 Program Files
```

## 1. Origin（COM/LabTalk 桥，Origin 2021 = 9.80）

全命令 `--json`。

**读数据（含 graph-only OGGU 的隐藏数据集）**
```bash
$O file info -i x.oggu          # 页面/数据集/行界清单
$O data dump -i x.oggu -d Book1_G -d Book1_H -o out.csv   # 全精度，含误差棒
```
- graph-only OGGU 无工作表，但图内 X/Y/误差数据集可直读
  （`get <ds> -e nend` 定界）
- `%C`(doc -e P) 只给 Y 列；X/误差要用 `doc -e D`

**数据→图→导出（验证过的配方）**
```python
op.new_book("w", "name"); sh = wb[0]
sh.from_list(0, x, lname="t", units="s", axis="X")
sh.from_list(1, y, lname="V", units="mV")
op.lt_exec('plotxy iy:=[name]Sheet1!2 plot:=200;')   # 200=线图
op.lt_exec('layer -a;')                               # 自适应量程
op.lt_exec('layer.x.title$ = "Time (s)";')
```
```bash
$O graph export -n Graph1 -o fig.png          # 栅格
$O graph export -n Graph1 -o fig.pdf          # 矢量（内部走 expGraph）
```
- 多面板组图：`win -t plot merge;` 生成合并页
- 线性拟合：激活含 plot 的层后 `lr -2;` → `lr.a / lr.b`

**☠️ 原生崩溃点（禁用，已内置绕行）**
- `save_fig` 传 .pdf/.eps → 进程崩溃（exit 127 且吞缓冲输出）→ 用 expGraph
- originpro 包装层 `GLayer.add_plot(工作表)` → 崩溃 → 用 plotxy

**进程纪律**：每次 CLI 命令自动关自己的 COM 实例；长脚本结束必须 `op.exit()`；
跑前先清僵尸 Origin 进程（僵尸会致 `LT_execute 无效指针`；崩溃恢复弹窗会
堵死 COM——backend 已用 `set_show(False)` 隐藏防护）。

**探测经验**：COM 脚本每条 print 必须 `flush=True`——原生崩溃吞未刷新 stdout，
把崩溃伪装成"零输出"。

## 2. MATLAB（R20XXa，matlab -batch 硬依赖）

```bash
$M --json exec code "x=linspace(0,2*pi);y=sin(x);disp(max(y))"
$M --json eval "sin(pi/4)"
$M --json plot create "plot(linspace(0,2*pi),sin(linspace(0,2*pi)))" -o sine.png
$M --json system toolboxes
$M exec script analysis.m        # 跑脚本文件
$M repl                          # 交互模式
```
- 每次调用付 MATLAB 启动 ~15–60 s；批量工作写成 .m 一次跑
- 许可证 banner 噪音会混进 stdout，解析时取末行/JSON 段
- 上游：matlab CLI 基于开源 cli-anything-matlab（MIT）封装，本 skill 只收录
  验证过的用法

## 3. COMSOL 6.x（comsolbatch，本地许可）

```bash
$C --json system info                        # 版本/许可
$C model new -o m.java --param L=1[m]        # 脚手架（自动写成 .java！）
$C --json model verify m.java
$C --json model run -i m.java --study std1 --np 8
$C --json demo                               # 冒烟：13 s 全链路
```
- **管线真相**：`.java → comsolcompile → .class → comsolbatch → .mph`
  （comsolbatch 只认 .mph/.class；comsolcompile 对坏输入静默返回 0——
  backend 只信 .class 产物存在，不信退出码）
- Java 模板要点：完整类结构 + `run() throws java.io.IOException`
- 控制台输出 GBK，backend 已解码；`model run` 返回产物 diff

## 4. Inkscape 1.4+（无头组图/矢量转换）

```bash
INK="C:/Program Files/Inkscape/bin/inkscape.exe"
# WMF/EMF → 矢量
$INK asset.wmf --export-type=svg --export-filename=out.svg --export-area-drawing
# 拼版导出（文字转曲=投稿硬要求）
$INK composite.svg --export-type=pdf --export-filename=out.pdf \
    --export-text-to-path --export-area-drawing
```
- 组图流程：Python 生成组合 SVG（栅格 PNG 用 `file:///` 绝对路径引用、矢量
  SVG 可嵌套 `<svg>` 置入、`<text>` 做面板标签 a/b 和标注）→ 上面一条命令出稿
- 验证产物：`%PDF-` 魔数 + `b'/Font' not in pdf_bytes`（零内嵌字体=已转曲）

## 5. 端到端组图工作流（论文级）

```
源数据(CSV/提取)
  ├─ Origin plotxy → expGraph PDF   （组里风格的数据面板）
  ├─ MATLAB exportgraphics PNG      （探索性/统计面板）
  └─ Inkscape WMF 转换 → SVG        （表征资产面板）
        ↓
Python 组合 SVG（180 mm 画布、a/b/c 标签、图注）
        ↓
inkscape --export-text-to-path → 投稿 PDF（矢量、无内嵌字体）
```

## 6. 一键自检（换机器/怀疑环境时跑）

```bash
$O --json system info     # Origin 连通
"$CLI_MATLAB_EXE" -batch "disp(version)"
$C --json system version  # COMSOL 版本
$INK --version            # Inkscape 版本
```

## 7. 组件与来源

| 组件 | 角色 | 验证状态 |
|---|---|---|
| cli-anything-origin | Origin COM/LabTalk 桥（自研） | 18/18 测试过 |
| cli-anything-comsol | COMSOL batch 引擎（自研） | 20/20 含真机 E2E |
| cli-anything-matlab | MATLAB batch 桥（上游开源 MIT，本地封装） | 26 进程内 E2E 过 |
| cli-anything-inkscape | Inkscape 直连 harness | 链路实测 |
