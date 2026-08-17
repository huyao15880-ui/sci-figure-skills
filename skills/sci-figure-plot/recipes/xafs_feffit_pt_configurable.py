"""XAFS recipe 06 — configurable feffit engine ("fit as you wish").

Every degree of freedom a reviewer or operator cares about is exposed:

  data layer    --rbkg            background removal radius (A)
  fit window    --kmin --kmax --kweight --rmin --rmax --dk --window
  structural    --shell n4|c4|c2n2 --dist-n --dist-c   (cluster rebuilt,
                 feff6l re-run & cached per geometry)
  param policy  --s02 FIX         fix S02 instead of fitting amp
                 --sig2-max --e0-range --r-range      parameter bounds

Examples
  report conditions (default):
      python xafs_feffit_pt_configurable.py
  shorter k window:
      python xafs_feffit_pt_configurable.py --kmax 10.0
  mixed C/N shell:
      python xafs_feffit_pt_configurable.py --shell c2n2 --dist-n 1.98 --dist-c 2.05
  fixed S02=0.90 (report-style fixed amplitude):
      python xafs_feffit_pt_configurable.py --s02 0.90
  sensitivity sweep over kmax (reviewer defense):
      python xafs_feffit_pt_configurable.py --scan kmax 9.5 10.5 11.5 12.5

Data: data/Pt-sample.prj (user Athena project)
"""
from __future__ import annotations

import argparse
import sys
import hashlib
from pathlib import Path

import numpy as np
from larch import Group
from larch.io import read_athena
from larch.xafs import (autobk, xftf, feffpath, feffit_transform,
                        feffit_dataset, feffit, feffit_report)
from larch.xafs.feffrunner import FeffRunner
from larch.fitting import param, guess

HERE = Path(__file__).parent
DATA = HERE / "data" / "Pt-sample.prj"
CACHE = HERE / "feff_cache"
REPORT_LOCK = {"CN": "4.3±0.5", "R": "2.02±0.01", "sig2": "0.002±0.001",
               "dE0": "-4.4±1.5", "Rf": "0.013"}


# ---------------------------------------------------------------- clusters
def build_cluster(shell: str, d_n: float, d_c: float):
    """Return atom list [(x,y,z,ipot,tag)] for the requested first shell."""
    def ring(distance, ipot, tag, n=4):
        xy = distance / np.sqrt(2)
        pts = [(xy, xy), (-xy, xy), (xy, -xy), (-xy, -xy)]
        k = n // 2 if n == 2 else n
        return [(x, y, 0.0, ipot, tag) for (x, y) in pts[:k]]

    atoms = [(0.0, 0.0, 0.0, 0, "Pt")]
    if shell == "n4":
        atoms += ring(d_n, 1, "N")
    elif shell == "c4":
        atoms += ring(d_c, 2, "C")
    elif shell == "c2n2":
        atoms += ring(d_n, 1, "N", n=2)
        atoms += [(x, -y, 0.0, ip, t) for x, y, z, ip, t in ring(d_c, 2, "C", n=2)]
    else:
        raise ValueError(f"unknown shell {shell}")
    return atoms


def run_feff(shell: str, d_n: float, d_c: float) -> Path:
    """Write feff.inp, run feff6l, return folder (cached by geometry)."""
    key = hashlib.md5(f"{shell}{d_n:.3f}{d_c:.3f}".encode()).hexdigest()[:10]
    work = CACHE / f"{shell}_{key}"
    if list(work.glob("feff*.dat")):
        return work
    work.mkdir(parents=True, exist_ok=True)
    atoms = build_cluster(shell, d_n, d_c)
    used_ipots = sorted({ip for *_, ip, _ in atoms})
    pot_lines = {0: "  0  78", 1: "  1   7", 2: "  2   6"}
    lines = [
        "TITLE configurable Pt single-atom cluster",
        "HOLE 4 1.0",
        "CONTROL 1 1 1 1",
        "PRINT 0 0 0 0",
        "POTENTIALS",
        *[pot_lines[i] for i in used_ipots],
        "ATOMS",
    ]
    lines += [f"{x:10.4f} {y:10.4f} {z:10.4f}   {ip}   {t}"
              for x, y, z, ip, t in atoms]
    (work / "feff.inp").write_text("\n".join(lines) + "\n", encoding="ascii")
    FeffRunner(feffinp="feff.inp", folder=str(work)).run(exe="feff6l")
    return work


# ------------------------------------------------------------------- fit
def do_fit(cfg) -> dict:
    work = run_feff(cfg.shell, cfg.dist_n, cfg.dist_c)
    pathfiles = sorted(work.glob("feff*.dat"))

    prj = read_athena(str(DATA))
    s = prj.Pt_sample
    autobk(s, e0=s.e0 + cfg.e0_offset, rbkg=cfg.rbkg, kweight=cfg.kweight)

    shared = dict(s02="amp", e0="del_e0", sigma2="sig2")
    paths = {}
    if len(pathfiles) == 1 or cfg.shell in ("n4", "c4"):
        pf = pathfiles[0]
        paths[pf.stem] = feffpath(str(pf), **shared, deltar="del_r")
    else:  # mixed shell: two reffs -> shared fractional shift alpha*reff
        for pf in pathfiles[:2]:
            paths[pf.stem] = feffpath(str(pf), **shared, deltar="alpha*reff")

    trans = feffit_transform(kmin=cfg.kmin, kmax=cfg.kmax, kw=cfg.kweight,
                             dk=cfg.dk, window=cfg.window,
                             rmin=cfg.rmin, rmax=cfg.rmax)
    amp = (param(cfg.s02, vary=False) if cfg.s02
           else guess(0.9, min=0.4, max=1.6))
    pars = Group(amp=amp,
                 del_e0=guess(0.0, min=-cfg.e0_range, max=cfg.e0_range),
                 sig2=guess(0.003, min=0, max=cfg.sig2_max))
    if len(paths) == 1:
        pars.del_r = guess(0.0, min=-cfg.r_range, max=cfg.r_range)
    else:
        pars.del_r = param(0.0, vary=False)          # unused, keep group
        pars.alpha = guess(0.0, min=-0.05, max=0.05)  # r = reff*(1+alpha)

    dset = feffit_dataset(data=s, paths=paths, transform=trans)
    out = feffit(pars, dset)
    p = out.params

    cn, r_eff, r_wsum = 0.0, [], 0.0
    wsum = 0.0
    for name, fp in paths.items():
        ampv = p["amp"].value
        if len(paths) == 1:
            rr = fp.reff + p["del_r"].value
            shift = "del_r"
        else:
            al = p["alpha"].value
            rr = fp.reff * (1 + al)
            shift = "alpha*reff"
        w = ampv * fp.degen
        cn += w
        r_eff.append((name, fp._feffdat.geom[1][0], rr, w))
        r_wsum += rr * w
        wsum += w

    res = dict(
        cfg=cfg, shell=cfg.shell,
        n_paths=len(paths), paths=r_eff,
        CN=cn, R=r_wsum / wsum,
        sig2=p["sig2"].value, sig2_e=p["sig2"].stderr,
        dE0=p["del_e0"].value, dE0_e=p["del_e0"].stderr,
        rfactor=out.rfactor, chi2r=out.chi2_reduced,
        dset=dset, sample=s, s02_mode=("fixed %.2f" % cfg.s02) if cfg.s02
        else "fitted %.2f" % p["amp"].value,
    )
    return res


def report(res: dict, label: str = ""):
    print(f"\n--- fit [{label or res['shell']}] "
          f"s02({res['s02_mode']}) paths={res['n_paths']} ---")
    for name, tag, rr, w in res["paths"]:
        print(f"    {name}: scatterer {tag}, R={rr:.3f} A, "
              f"amp*degen={w:.2f}")
    print(f"  CN={res['CN']:.2f}   R(w)={res['R']:.3f} A   "
          f"sig2={res['sig2']:.4f}   dE0={res['dE0']:.1f}   "
          f"Rf={res['rfactor']:.4f}")
    print(f"  report lock: CN {REPORT_LOCK['CN']}  R {REPORT_LOCK['R']}  "
          f"sig2 {REPORT_LOCK['sig2']}  dE0 {REPORT_LOCK['dE0']}  "
          f"Rf {REPORT_LOCK['Rf']}")


# ------------------------------------------------------------------- CLI
def get_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_argument_group("data layer")
    g.add_argument("--rbkg", type=float, default=1.0)
    g.add_argument("--e0-offset", type=float, default=0.0)
    g = ap.add_argument_group("fit window")
    g.add_argument("--kmin", type=float, default=3.0)
    g.add_argument("--kmax", type=float, default=11.5)
    g.add_argument("--kweight", type=int, default=2)
    g.add_argument("--rmin", type=float, default=1.0)
    g.add_argument("--rmax", type=float, default=2.2)
    g.add_argument("--dk", type=float, default=1.0)
    g.add_argument("--window", default="kaiser")
    g = ap.add_argument_group("structural model")
    g.add_argument("--shell", choices=["n4", "c4", "c2n2"], default="n4")
    g.add_argument("--dist-n", type=float, default=2.02)
    g.add_argument("--dist-c", type=float, default=2.05)
    g = ap.add_argument_group("parameter policy")
    g.add_argument("--s02", type=float, default=None,
                   help="fix S02 to this value (default: fit amp)")
    g.add_argument("--sig2-max", type=float, default=0.02)
    g.add_argument("--e0-range", type=float, default=15.0)
    g.add_argument("--r-range", type=float, default=0.10)
    g = ap.add_argument_group("sweep")
    ap.add_argument("--scan", nargs="+", metavar=("PARAM", "VALUES"),
                    help="e.g. --scan kmax 9.5 10.5 11.5 12.5")
    return ap.parse_args(argv)


def main(argv=None):
    cfg = get_args(argv)
    if cfg.scan:
        pname, values = cfg.scan[0], cfg.scan[1:]
        base = list(sys.argv[1:]) if argv is None else list(argv)
        print(f"=== sensitivity sweep over {pname} ===")
        for v in values:
            c = get_args(base + [f"--{pname}", v])
            report(do_fit(c), label=f"{pname}={v}")
        return
    report(do_fit(cfg))


if __name__ == "__main__":
    main()
