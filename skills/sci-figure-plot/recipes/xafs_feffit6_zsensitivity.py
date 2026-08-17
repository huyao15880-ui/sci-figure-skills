"""XAFS recipe 02 — Z-sensitivity of backscatterer (ZnSe, headless feffit6).

Adapted from upstream xraylarch examples/feffit/doc_feffit6.py (MIT):
wxmplot GUI calls replaced by a matplotlib 2x4 panel figure. One dataset
(Zn K-edge ZnSe) is fitted eight times, once per hypothesised
backscatterer (Zn..Rb); the correct scatterer (Se) should win on
chi2_reduced and phase-corrected R (~2.45 A, Zn-Se bond).

Run:  python xafs_feffit6_zsensitivity.py
Data: data/znse_zn_xafs.001 + data/Feff_ZnSe/feff_zn*.dat (upstream, MIT)
"""
from pathlib import Path

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from larch import Group
from larch.io import read_ascii
from larch.math import interp
from larch.fitting import param, guess, param_group
from larch.xafs import (autobk, feffpath, feffit_transform,
                        feffit_dataset, feffit, xftf_fast)

HERE = Path(__file__).parent
MM = 1 / 25.4

dat = read_ascii(str(HERE / "data" / "znse_zn_xafs.001"),
                 labels="energy dwelltime i0 i1")
dat.mu = -np.log(dat.i1 / dat.i0)
autobk(dat, e0=9666.0, rbkg=1.25, kweight=2)

pathargs = dict(degen=4.0, s02="amp", e0="del_e0", sigma2="sig2", deltar="del_r")
SCATTERERS = ("Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb")
paths = {z: feffpath(str(HERE / "data" / "Feff_ZnSe" / f"feff_zn{z.lower()}.dat"),
                     **pathargs) for z in SCATTERERS}

trans = feffit_transform(rmin=1.5, rmax=3.0, kmin=3, kmax=13,
                         kw=2, dk=4, window="kaiser")


def phase_correct(dset):
    """Phase-corrected FT; returns R at Im[chi_pc(R)]=0 near the peak."""
    nrpts = len(dset.model.r)
    path1 = list(dset.paths.items())[0][1]
    feff_pha = interp(path1._feffdat.k, path1._feffdat.pha, dset.model.k)
    chir_pha = xftf_fast(dset.data.chi * np.exp(0 - 1j * feff_pha)
                         * dset.data.kwin * dset.data.k**2)[:nrpts]
    mag = np.sqrt(chir_pha.real**2 + chir_pha.imag**2)
    dset.model.chir_phcor = chir_pha
    irmax = int(np.where(mag == max(mag))[0][0])
    y = dset.model.chir_im[irmax - 1: irmax + 2]
    x = dset.model.r[irmax - 1: irmax + 2]
    return x[0] - y[0] * (x[1] - x[0]) / (y[1] - y[0])


print("|Scatt|RedChi2|   S02    |  sigma2  |   E0    |    R     | R_phcor |")
rows = []
for z in SCATTERERS:
    dset = feffit_dataset(data=dat, paths={z: paths[z]}, transform=trans)
    pars = Group(amp=guess(1.0),
                 del_e0=guess(0.1, min=-20, max=20),
                 sig2=param(0.006, vary=True, min=0),
                 del_r=guess(0.0))
    out = feffit(pars, dset)
    p1 = out.datasets[0].paths[z]
    scatt = p1._feffdat.geom[1][0]
    r_phcor = phase_correct(out.datasets[0])
    rows.append(dict(z=scatt, dset=out.datasets[0],
                     chi2=out.chi2_reduced,
                     s02=out.params["amp"].value, s02e=out.params["amp"].stderr,
                     ss=out.params["sig2"].value,
                     e0=out.params["del_e0"].value,
                     r=p1.reff + out.params["del_r"].value,
                     rpc=r_phcor))
    print(f"| {scatt:>2s}  | {out.chi2_reduced:5.1f} | {out.params['amp'].value:5.2f}"
          f"({out.params['amp'].stderr:.2f}) | {out.params['sig2'].value:.4f}  "
          f"| {out.params['del_e0'].value:6.2f} | {p1.reff + out.params['del_r'].value:6.3f} "
          f"| {r_phcor:7.3f} |")

best = min(rows, key=lambda r: r["chi2"])
print(f"\nBest scatterer by chi2: {best['z']} (Zn-Se expected; "
      f"phase-corrected R = {best['rpc']:.3f} A vs Zn-Se 2.45 A)")

# ---- figure: 2x4 R-space overlays, final-size discipline --------------
mpl.rcParams.update({
    "font.family": "Arial", "font.size": 6.0,
    "axes.labelsize": 6.5, "xtick.labelsize": 5.5, "ytick.labelsize": 5.5,
    "axes.linewidth": 0.4, "pdf.fonttype": 42,
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
    "axes.spines.top": False, "axes.spines.right": False,
})

fig, axes = plt.subplots(2, 4, figsize=(183 * MM, 100 * MM),
                         constrained_layout=True, sharex=True, sharey=True)
fig.get_layout_engine().set(w_pad=1.4 * MM, h_pad=1.4 * MM, wspace=0.03, hspace=0.06)

for i, row in enumerate(rows):
    ax = axes.flat[i]
    d = row["dset"]
    m = d.model
    mag_pc = np.sqrt(m.chir_phcor.real**2 + m.chir_phcor.imag**2)
    ax.plot(d.data.r, d.data.chir_mag, color="#0072B2", lw=0.8, label="data")
    ax.plot(m.r, m.chir_mag, color="#D55E00", lw=0.8, label="Feff path")
    ax.plot(m.r, mag_pc, color="#009E73", lw=0.8, ls="--",
            label="phase-corrected")
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 5.5)
    star = " *" if row is best else ""
    ax.set_title(f"{row['z']}{star}  $\\chi^2_r$={row['chi2']:.0f}",
                 loc="center", fontsize=6.0, pad=3)
    ax.set_title("abcdefgh"[i], loc="left", fontweight="bold", fontsize=8, pad=3)
    if i % 4 == 0:
        ax.set_ylabel("|" + chr(967) + "(R)|")
    if i >= 4:
        ax.set_xlabel("R (" + chr(197) + ")")

handles, labels = axes.flat[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="outside lower center", ncol=3, fontsize=6.0)
out_pdf = HERE / "xafs_feffit6_zsensitivity"
fig.savefig(out_pdf.with_suffix(".pdf"))
fig.savefig(out_pdf.with_suffix(".png"), dpi=600)
print(f"[saved] {out_pdf.name}.pdf/.png  page=183x100 mm")
