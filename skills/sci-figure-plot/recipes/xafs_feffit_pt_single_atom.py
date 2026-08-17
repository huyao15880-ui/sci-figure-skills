"""XAFS recipe 05 — feffit single-shell quantification of Pt single-atom.

Graduation piece of the XAFS learning line: builds a Pt-N4 square-planar
model (2.02 A, report Pt-C/N distance), runs feff6l to generate the Pt-N
single-scattering path, then feff-fit (k 3-11.5, R 1.0-2.2, kweight 2,
mirroring report conditions) and reconciles CN/R/sigma2/dE0/R-factor
against the locked report values (Pt-C/N CN=4.3+/-0.5, R=2.02+/-0.01,
sigma2=0.002, dE0=-4.4, Rf=0.013).

Sample identity assumption: Pt-sample.prj = single-atom sample (evidence:
+5.2 eV edge shift, first shell ~1.96 A, high-shell structure offset from
metallic Pt-Pt). High-shell attribution stays quantitatively open.

Run:  python xafs_feffit_pt_single_atom.py
Data: data/Pt-sample.prj (user Athena project)
"""
from pathlib import Path
import shutil

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from larch import Group
from larch.io import read_athena
from larch.xafs import autobk, xftf, feffpath, feffit_transform, \
    feffit_dataset, feffit, feffit_report
from larch.xafs.feffrunner import FeffRunner
from larch.fitting import param, guess

HERE = Path(__file__).parent
MM = 1 / 25.4
WORK = HERE / "feff_ptn4"
MINUS = "\u2212"

# ---- 1. build Pt-N4 square-planar cluster (2.02 A) -------------------------
d = 2.02
xy = d / np.sqrt(2)
WORK.mkdir(exist_ok=True)
atoms = [
    (0.0, 0.0, 0.0, 0, "Pt"),
    (xy, xy, 0.0, 1, "N"), (-xy, xy, 0.0, 1, "N"),
    (xy, -xy, 0.0, 1, "N"), (-xy, -xy, 0.0, 1, "N"),
    # second-shell C at ~3.0 A to seed paths for the 2.58 A FT structure
    (3.0, 0.0, 0.0, 2, "C"), (0.0, 3.0, 0.0, 2, "C"),
]
lines = [
    "TITLE Pt-N4 square planar single-atom model (Pt L3)",
    "HOLE 4 1.0",
    "* control: mphase mpath mfeff mchi",
    "CONTROL 1 1 1 1",
    "PRINT 0 0 0 0",
    "* RPATH 2.5   (feff6l: keyword unavailable; single-shell path used)",
    "POTENTIALS",
    "* ipot  Z",
    "  0  78",
    "  1   7",
    "  2   6",
    "ATOMS",
    "*   x          y          z   ipot  tag",
]
lines += [f"{x:10.4f} {y:10.4f} {z:10.4f}   {ip}   {tag}"
          for x, y, z, ip, tag in atoms]
(WORK / "feff.inp").write_text("\n".join(lines) + "\n", encoding="ascii")
print(f"[feff.inp] written -> {WORK}")

# ---- 2. run feff6l ----------------------------------------------------------
runner = FeffRunner(feffinp="feff.inp", folder=str(WORK))
runner.run(exe="feff6l")
paths = sorted(WORK.glob("feff*.dat"))
print(f"[feff6l] {len(paths)} path files: {[p.name for p in paths[:6]]}")

# ---- 3. data through the frozen chain ---------------------------------------
prj = read_athena(str(HERE / "data" / "Pt-sample.prj"))
s = prj.Pt_sample
autobk(s, e0=s.e0, rbkg=1.0, kweight=2)

# ---- 4. feffit: single Pt-N path, report conditions -------------------------
ptn = feffpath(str(WORK / "feff0001.dat"),
               s02="amp", e0="del_e0", sigma2="sig2", deltar="del_r")
trans = feffit_transform(kmin=3.0, kmax=11.5, kw=2, dk=1.0,
                         window="kaiser", rmin=1.0, rmax=2.2)
pars = Group(amp=guess(0.8, min=0.4, max=1.6),
             del_e0=guess(0.0, min=-15, max=15),
             sig2=guess(0.003, min=0, max=0.02),
             del_r=guess(0.0, min=-0.1, max=0.1))
dset = feffit_dataset(data=s, paths={"PtN": ptn}, transform=trans)
out = feffit(pars, dset)
print(feffit_report(out))

p = out.params
fit_r = ptn.reff + p["del_r"].value
fit_cn = p["amp"].value * ptn.degen
rows = [
    ("CN (n*S0²*degen)", fit_cn, p["amp"].stderr * ptn.degen, "4.3 ± 0.5"),
    ("R (Å)", fit_r, p["del_r"].stderr, "2.02 ± 0.01"),
    ("σ² (Å²)", p["sig2"].value, p["sig2"].stderr, "0.002 ± 0.001"),
    ("ΔE0 (eV)", p["del_e0"].value, p["del_e0"].stderr, "-4.4 ± 1.5"),
    ("R-factor", out.rfactor, None, "0.013"),
]
print("\n==== reconciliation vs locked report (Pt-C/N path) ====")
print(f"{'quantity':<18}{'fit':>12}{'±':>10}   report")
for name, v, e, rep in rows:
    err = f"± {e:.3f}" if e is not None else ""
    print(f"{name:<18}{v:>12.3f}{err:>10}   {rep}")

# ---- 5. figure: R-space fit overlay -----------------------------------------
mpl.rcParams.update({
    "font.family": "Arial", "font.size": 6.0,
    "axes.labelsize": 6.5, "xtick.labelsize": 5.5, "ytick.labelsize": 5.5,
    "axes.linewidth": 0.4, "pdf.fonttype": 42,
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False,
})
fig, axes = plt.subplots(1, 2, figsize=(183 * MM, 70 * MM),
                         constrained_layout=True)
fig.get_layout_engine().set(w_pad=1.6 * MM, h_pad=1.6 * MM, wspace=0.06)

ax = axes[0]
m = s.k <= 12
ax.plot(s.k[m], s.k[m]**2 * s.chi[m], color="#0072B2", lw=0.6, label="data")
ax.plot(dset.model.k, dset.model.k**2 * dset.model.chi,
        color="#D55E00", lw=0.7, label="Pt-N fit")
ax.set_xlim(2, 12)
ax.set_xlabel("k (" + chr(197) + "$^{-1}$)")
ax.set_ylabel("k$^2$" + chr(967) + "(k)")
ax.legend(loc="upper right")
ax.set_title("a", loc="left", fontweight="bold", fontsize=8, pad=3)
ax.set_title("k$^2$" + chr(967) + "(k), k 3" + MINUS + "11.5", loc="center",
             fontsize=6.5, pad=3)

ax = axes[1]
dm, mm_ = dset.model, dset.data
ax.plot(mm_.r, mm_.chir_mag, color="#0072B2", lw=0.9, label="data |" + chr(967) + "(R)|")
ax.plot(dm.r, dm.chir_mag, color="#D55E00", lw=0.9, label="fit |" + chr(967) + "(R)|")
ax.axvspan(1.0, 2.2, color="#999999", alpha=0.10, lw=0)
ax.text(0.35, mm_.chir_mag.max() * 0.92,
        f"CN = {fit_cn:.1f}\nR = {fit_r:.2f} " + chr(197) + "\n"
        f"σ² = {p['sig2'].value*1000:.1f}×10" + "$^{-3}$ " + chr(197) + "²\n"
        f"R$_f$ = {out.rfactor:.3f}", fontsize=5.5, va="top")
ax.set_xlim(0, 5)
ax.set_ylim(0, mm_.chir_mag.max() * 1.1)
ax.set_xlabel("R (" + chr(197) + ")")
ax.set_ylabel("|" + chr(967) + "(R)|")
ax.legend(loc="upper right")
ax.set_title("b", loc="left", fontweight="bold", fontsize=8, pad=3)
ax.set_title("|" + chr(967) + "(R)| fit, Pt-N path", loc="center",
             fontsize=6.5, pad=3)

outfig = HERE / "xafs_feffit_pt_single_atom"
fig.savefig(outfig.with_suffix(".pdf"))
fig.savefig(outfig.with_suffix(".png"), dpi=600)
print(f"[saved] {outfig.name}.pdf/.png  page=183x70 mm")
