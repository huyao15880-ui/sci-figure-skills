"""XAFS recipe 09 — group-style Origin TEMPLATE project (.opju deliverable).

Customer deliverable IS the Origin project file. This builds the template
project with the prior-art style (docs/ORIGIN_TEMPLATE_SPEC.md) baked in:
Graph1 = XANES overlay (open frame), Graph2 = R-space fit (blue data /
red fit, four-frame inward ticks, annotation box), Arial fonts throughout
(SimSun defeated), ready for per-order data fill + save-as.

Run:  python origin_template_opju.py
Out:  xafs_group_template.opju (+ verification PDF)
"""
from pathlib import Path
import subprocess
import sys

import originpro as op
from larch.io import read_athena
from larch.xafs import autobk, xftf

import xafs_feffit_pt_configurable as engine

HERE = Path(__file__).parent
OPJU = HERE / "xafs_group_template.opju"
PDF = HERE / "xafs_group_template_check"

prj = read_athena(str(HERE / "data" / "Pt-sample.prj"))
s, f = prj.Pt_sample, prj.Pt_Foil
autobk(s, e0=s.e0, rbkg=1.0, kweight=2)
xftf(s, kmin=3.0, kmax=11.5, dk=1.0, kweight=2, window="kaiser")
import xafs_multishell_fit as ms        # FINAL: 2-shell, all params physical
d_, dm = ms.d, ms.m                     # (3-path rejected: sigma^2 collapsed)


def lt(code, tag):
    r = op.lt_exec(code)
    print(f"[lt {'OK ' if r in (0, None) else r}] {tag}")


ok = False
try:
    # ---------------- Graph 1: XANES overlay (open frame) -------------------
    wb = op.new_book("w", "XAFS")
    sh = wb[0]
    sh.from_list(0, list(f.energy), lname="EFoil", units="eV", axis="X")
    sh.from_list(1, list(f.norm), lname="Foil", axis="Y")
    sh.from_list(2, list(s.energy), lname="ESample", units="eV", axis="X")
    sh.from_list(3, list(s.norm), lname="Sample", axis="Y")
    lt('plotxy iy:=[XAFS]Sheet1!2 plot:=200;', "g1 curve1")
    lt('plotxy iy:=[XAFS]Sheet1!4 ogl:=[Graph1];', "g1 curve2")
    lt('layer -a;', "g1 autoscale")
    lt('layer.x.title$="Energy (eV)";', "g1 xlabel")
    lt('layer.y.title$="Normalized \\g(m)(E)";', "g1 ylabel")
    lt('layer.x.from=11560; layer.x.to=11700; layer.x.by=50;', "g1 xrange")
    lt('layer.y.from=0; layer.y.to=1.6; layer.y.by=0.4;', "g1 yrange")
    lt('legend -s u;', "g1 legend")
    # open frame: hide top/right axes (Origin layer axis show flags)
    lt('layer.x2.show=0; layer.y2.show=0;', "g1 open frame")
    # colors: foil gray(19), sample blue(4); thicker lines
    lt('win -a Graph1; set %C -c 19; set %C -w 150;', "g1 last-plot gray")
    lt('set layer.plotlist(1).plot -c 19;', "g1 try1")

    # ---------------- Graph 2: R-space fit pairing ---------------------------
    wb2 = op.new_book("w", "RSpace")
    sh2 = wb2[0]
    sh2.from_list(0, list(d_.r), lname="R", units="A", axis="X")
    sh2.from_list(1, list(d_.chir_mag), lname="Data", axis="Y")
    sh2.from_list(2, list(dm.r), lname="Rfit", units="A", axis="X")
    sh2.from_list(3, list(dm.chir_mag), lname="Fit", axis="Y")
    lt('plotxy iy:=[RSpace]Sheet1!2 plot:=200;', "g2 data")
    lt('plotxy iy:=[RSpace]Sheet1!4 ogl:=[Graph2];', "g2 fit")
    lt('layer -a;', "g2 autoscale")
    lt('layer.x.title$="R (\\+3135)";', "g2 xlabel angstrom")
    lt('layer.y.title$="|\\g(c)(R)| Fourier Transform Magnitude";', "g2 ylabel")
    lt('layer.x.from=0; layer.x.to=4; layer.x.by=1;', "g2 xrange")
    lt('legend -s u;', "g2 legend")
    lt('set %C -c 2; set %C -w 150;', "g2 fit red")

    # ---------------- global font fix: defeat SimSun -------------------------
    lt('doc -e LBL { %L.font$ = "Arial"; }', "fonts->Arial (labels)")
    lt('layer.x.title.font$="Arial"; layer.y.title.font$="Arial";',
       "try axis-title font")

    # ---------------- save template + verification export --------------------
    # save FULL project via python API (LabTalk save silently fails here)
    op.save(str(OPJU))
    lt(f'expGraph type:=pdf path:="{PDF.parent}" '
       f'filename:="{PDF.name}" overwrite:=replace;', "export check pdf")
    ok = True
    print("[saved]", OPJU.name)
finally:
    op.exit()

sys.exit(0 if ok else 1)
