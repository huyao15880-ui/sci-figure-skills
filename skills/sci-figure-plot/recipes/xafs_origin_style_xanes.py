"""XAFS recipe 07 — Origin-style figure via originpro COM (validated route).

The "draw like Origin" route for real: fills a workbook with originpro
(from_list), plots with LabTalk plotxy (add_plot wrapper crashes), styles
with LabTalk, exports with expGraph (save_fig .pdf crashes), then op.exit.

Run:  python xafs_origin_style_xanes.py
Data: data/Pt-sample.prj (Pt_sample + Pt_Foil XANES overlay)
"""
from pathlib import Path
import sys

import originpro as op
from larch.io import read_athena

HERE = Path(__file__).parent
OUTPDF = HERE / "xanes_origin_style"
MM = 1 / 25.4

prj = read_athena(str(HERE / "data" / "Pt-sample.prj"))
s, f = prj.Pt_sample, prj.Pt_Foil

ok = False
try:
    wb = op.new_book("w", "XAFSXanes")
    sh = wb[0]
    sh.from_list(0, list(s.energy), lname="Energy", units="eV", axis="X")
    sh.from_list(1, list(s.norm), lname="Norm sample", axis="Y")
    sh.from_list(2, list(f.energy), lname="EnergyF", units="eV", axis="X")
    sh.from_list(3, list(f.norm), lname="Norm foil", axis="Y")
    print("[book] 4 cols filled:", sh.rows, "rows")

    op.lt_exec('plotxy iy:=[XAFSXanes]Sheet1!2 plot:=200;')
    op.lt_exec('plotxy iy:=[XAFSXanes]Sheet1!4 plot:=200 ogl:=[Graph1];')
    # Origin house styling
    op.lt_exec('layer -a;')
    op.lt_exec('layer.x.title$="Energy (eV)";')
    op.lt_exec('layer.y.title$="Normalized \\g(m)(E)";')
    op.lt_exec('layer.x.from=11560; layer.x.to=11700; layer.x.by=50;')
    op.lt_exec('layer.y.from=0; layer.y.to=1.6; layer.y.by=0.4;')
    op.lt_exec('legend -s u;')            # legend from LName
    # export (expGraph, NOT save_fig) - default page size first
    op.lt_exec(f'expGraph type:=pdf path:="{OUTPDF.parent}" '
               f'filename:="{OUTPDF.name}" overwrite:=replace;')
    op.lt_exec(f'expGraph type:=png path:="{OUTPDF.parent}" '
               f'filename:="{OUTPDF.name}" overwrite:=replace tr1.Unit:=2 '
               'tr1.DPI:=600;')
    ok = True
    print("[export]", OUTPDF.name + ".pdf")
finally:
    op.exit()

# ---- normalize to 183 mm final page (vector 1:1, compose layer) ------------
import fitz
MM = 25.4 / 72
src = fitz.open(str(OUTPDF) + ".pdf" if str(OUTPDF).endswith("") else str(OUTPDF.with_suffix(".pdf")))
page = src[0]
content = page.rect
W = 183.0 / MM                          # final width in pt
H = content.height / content.width * W
doc = fitz.open()
dest = doc.new_page(width=W, height=H)
dest.show_pdf_page(fitz.Rect(0, 0, W, H), src, 0)
norm_tmp = str(OUTPDF.with_suffix(".norm.pdf"))
doc.save(norm_tmp, deflate=True, garbage=3)
doc.close(); src.close()
import os
os.replace(norm_tmp, str(OUTPDF.with_suffix(".pdf")))

chk = fitz.open(str(OUTPDF.with_suffix(".pdf")))
r = chk[0].rect
print(f"[normalized] {r.width*MM:.1f} x {r.height*MM:.1f} mm")
chk[0].get_pixmap(dpi=200).save(str(OUTPDF) + "_preview.png")
chk.close()
sys.exit(0 if ok else 1)
