# YAeHMOP Extended-Hückel Band Tools

[![CI](https://github.com/tromer-unb/Huckell_yaehmop_bands/actions/workflows/ci.yml/badge.svg)](https://github.com/tromer-unb/Huckell_yaehmop_bands/actions/workflows/ci.yml)

A reproducible toolkit for **material-specific Extended Hückel Theory (EHT)** calculations using the original **YAeHMOP `bind` executable** as the electronic-structure engine.

The repository contains two complementary tools:

- **`parameter_fitter/`** — fits YAeHMOP EHT parameters to a reference band-structure image.
- **`band_runner/`** — calculates and plots EHT bands from a CIF structure and a fitted parameter file.

The Python code does **not** reimplement the YAeHMOP Hamiltonian. It prepares YAeHMOP inputs, runs the original compiled engine, parses its band output, and performs fitting/post-processing around it.

## Highlights

- Generic element/orbital discovery from YAeHMOP's parameter table.
- CIF input through ASE.
- Raster band-image digitization with continuity-aware reconstruction through crossings and degeneracies.
- Full-spectrum fitting or **frontier-only fitting** with `--fit-window EMIN EMAX`.
- Explicit gap penalty and regularization toward tabulated YAeHMOP atomic parameters.
- Reproducible MoS2 example (`Gamma-M-K-Gamma`).
- Standalone EHT band runner producing CSV and PNG output.
- Pinned YAeHMOP upstream revision and automated build.
- Unit/smoke tests plus an optional optimizer regression test.

## Quick start

```bash
git clone https://github.com/tromer-unb/Huckell_yaehmop_bands.git
cd Huckell_yaehmop_bands
./setup.sh
```

Run the end-to-end MoS2 demonstration:

```bash
./scripts/run_mos2_demo.sh
```

Or run the test suite:

```bash
.venv/bin/pytest -q
RUN_SLOW_FIT=1 .venv/bin/pytest -q tests/test_parameter_fitter_slow.py
```

## Fit only valence/conduction states near the gap

The image calibration and fitting window are deliberately separate. If the image spans `-15 ... 11 eV`, keep that scale:

```bash
--emin -15 --emax 11
```

and select only frontier states for the objective with:

```bash
--fit-window -2 2
```

Example:

```bash
cd parameter_fitter
../.venv/bin/python fit_eht_v2.py examples/mos2/structure.cif examples/mos2/band.png \
  --format image --emin -15 --emax 11 --fit-window -2 2 \
  --symmetry-points 0 0  0.5 0  0.3333333333 0.3333333333  0 0 \
  --point-dim 2 --labels G M K G \
  --points-per-line 30 --trace-nx 401 \
  --outdir results_frontier --tag mos2_frontier
```

`--ymin -2 2` is retained as a compatibility alias for `--fit-window -2 2`.

## Reference data from VASP, Quantum ESPRESSO, SIESTA, or other codes

The current fitter consumes a **band-structure image**, not a native DFT output file. Therefore it is code-agnostic: a plot generated from VASP, Quantum ESPRESSO, SIESTA, ABINIT, GPAW, WIEN2k, or another electronic-structure package can be used provided the image and reciprocal-space path satisfy the input requirements.

See **[DFT software workflows](docs/DFT_SOFTWARE_GUIDE.md)** and **[image requirements](docs/IMAGE_REFERENCE_GUIDE.md)**.

> Native numerical parsers for VASP/QE/SIESTA are not implemented in this release. Do not interpret the image interface as direct support for `EIGENVAL`, `vasprun.xml`, QE `filband`, or SIESTA `.bands` files.

## Documentation

- [Method and objective](docs/METHOD.md)
- [Image reference requirements](docs/IMAGE_REFERENCE_GUIDE.md)
- [VASP / Quantum ESPRESSO / SIESTA workflows](docs/DFT_SOFTWARE_GUIDE.md)
- [Parameter-file format](docs/PARAMETER_FORMAT.md)
- [Reproducibility and validation](docs/REPRODUCIBILITY.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Project roadmap](docs/ROADMAP.md)

## Important scope and limitations

YAeHMOP in this workflow is a **spinless, non-SOC EHT model**. A spin-polarized or SOC-split DFT reference generally cannot be reproduced state-by-state without an explicit reduction policy. For best consistency, use a non-SOC reference when fitting the current model.

Absolute DFT energy zero is arbitrary in this fitting workflow. The comparison applies a rigid energy alignment; band shape, frontier energies, and the gap are the meaningful fitted quantities.

Raster images impose a finite pixel-resolution floor. Numerical eigenvalues are preferable when sub-meV reproduction is required.

## YAeHMOP provenance

The setup scripts build YAeHMOP from:

- upstream: `https://github.com/greglandrum/yaehmop.git`
- pinned commit: `4ded45bb2bb7a2d38d2527c991debce9226a9066`

YAeHMOP remains under its upstream license; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Repository status

This repository is an actively developed research codebase. Reproducibility information and known limitations are documented explicitly so that fitted parameters are not confused with universally transferable atomic parameters.

## Licensing

YAeHMOP is third-party software and remains subject to its upstream license; see `THIRD_PARTY_NOTICES.md` and `LICENSES/YAeHMOP.txt`. This repository does not silently relicense YAeHMOP. A project-wide license for the Python wrapper/tooling has not been selected in this initial release.
