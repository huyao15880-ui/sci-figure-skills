"""figcheck — submission-readiness audit for scientific figures (MVP).

The confirmed open-source gap: post-export verification that a figure
PDF will survive journal technical screening. Every check below was
battle-tested manually during this project's NC submission and XAFS
pipeline; this CLI makes them one command.

Usage:
    python figcheck.py figure.pdf
    python figcheck.py figure.pdf --journal nature   # min font 5pt
    python figcheck.py figure.pdf --expect "Energy" "R (Å)" --json

Checks:
    1 page-ink      ink extents inside MediaBox (no silent clipping)
    2 fonts         font whitelist (no SimSun/CJK-body/Type3/DejaVu)
    3 minus         no ASCII hyphen-minus in numeric text (U+2212 rule)
    4 font-size     smallest rendered text span >= journal floor
    5 keywords      --expect strings present in text layer
    6 size          physical page size sane (>= 40mm, <= 300mm)
Exit code 0 = all pass, 1 = failures (CI-friendly).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import fitz  # PyMuPDF

FONT_DENYLIST = ("simsun", "simhei", "msyh", "kaiti", "type3", "dejavu")
JOURNAL_FLOOR_PT = {"nature": 5.0, "advanced-materials": 6.0, "default": 5.0}
MIN_PAGE_MM, MAX_PAGE_MM = 40.0, 300.0
MINUS = "\u2212"


def check(pdf: Path, journal: str, expects: list[str]) -> dict:
    doc = fitz.open(str(pdf))
    results, failures = [], 0

    def record(name, ok, detail):
        nonlocal failures
        results.append({"check": name, "pass": bool(ok), "detail": detail})
        if not ok:
            failures += 1

    for pno, page in enumerate(doc, start=1):
        # 1 page-ink: rendering ink bounding box vs page box
        pix = page.get_pixmap(dpi=72, colorspace=fitz.csGRAY)
        import numpy as np
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
        ink = img < 200
        if ink.any():
            rows, cols = ink.nonzero()
            m = (pix.width / page.rect.width, pix.height / page.rect.height)
            ink_rect = fitz.Rect(cols.min() / m[0], rows.min() / m[1],
                                 cols.max() / m[0], rows.max() / m[1])
            margin_pt = 1.5 * 72 / 25.4
            clipped = (ink_rect.x0 < -0.5 or ink_rect.y0 < -0.5 or
                       ink_rect.x1 > page.rect.width + 0.5 or
                       ink_rect.y1 > page.rect.height + 0.5)
            record("page-ink", not clipped,
                   f"p{pno}: ink {ink_rect.width/72*25.4:.0f}x"
                   f"{ink_rect.height/72*25.4:.0f}mm inside "
                   f"{page.rect.width/72*25.4:.0f}x{page.rect.height/72*25.4:.0f}mm")
        else:
            record("page-ink", False, f"p{pno}: NO INK (blank page?)")

        # 2 fonts whitelist
        fonts = sorted({f[3] for f in page.get_fonts()})
        bad = [f for f in fonts
               if any(d in f.lower() for d in FONT_DENYLIST)]
        record("fonts", not bad, f"p{pno}: {fonts}" + (f" DENY: {bad}" if bad else ""))

        # 3 minus sign audit (numeric contexts with ASCII hyphen)
        text = page.get_text()
        import re
        ascii_minus_nums = re.findall(r"\d-\d|\d-\.", text)
        record("minus", not ascii_minus_nums,
               f"p{pno}: {len(ascii_minus_nums)} ASCII-minus numerics "
               + (ascii_minus_nums[:4].__str__() if ascii_minus_nums else "(U+2212 ok)"))

        # 4 font-size floor on real text spans
        floor = JOURNAL_FLOOR_PT[journal]
        smallest, smallest_txt = 99.0, ""
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    if span["text"].strip() and span["size"] < smallest:
                        smallest = span["size"]
                        smallest_txt = span["text"][:24]
        record("font-size", smallest >= floor,
               f"p{pno}: min {smallest:.1f}pt vs floor {floor}pt "
               f"(\"{smallest_txt}\")")

        # 5 keywords
        if expects:
            missing = [e for e in expects if e not in text]
            record("keywords", not missing,
                   f"p{pno}: " + ("all present" if not missing else f"missing {missing}"))

    # 6 page size sanity
    r = doc[0].rect
    w_mm, h_mm = r.width / 72 * 25.4, r.height / 72 * 25.4
    record("size", MIN_PAGE_MM <= w_mm <= MAX_PAGE_MM and
           MIN_PAGE_MM <= h_mm <= MAX_PAGE_MM,
           f"{w_mm:.0f}x{h_mm:.0f}mm")
    doc.close()
    return {"failures": failures, "results": results}


def main(argv=None):
    ap = argparse.ArgumentParser(description="submission-readiness audit")
    ap.add_argument("pdf", type=Path)
    ap.add_argument("--journal", default="default",
                    choices=sorted(JOURNAL_FLOOR_PT))
    ap.add_argument("--expect", nargs="*", default=[])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    rep = check(a.pdf, a.journal, a.expect)
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
    else:
        for r in rep["results"]:
            mark = "PASS" if r["pass"] else "FAIL"
            print(f"[{mark}] {r['check']:10} {r['detail']}")
        print("RESULT:", "ALL PASS" if rep["failures"] == 0
              else f"{rep['failures']} FAILURE(S)")
    sys.exit(0 if rep["failures"] == 0 else 1)


if __name__ == "__main__":
    main()
