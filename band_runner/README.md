# EHT Band Runner

Calculate Extended-Hückel bands with the original YAeHMOP engine from:

1. a crystal structure (`.cif`), and
2. a YAeHMOP-style parameter file (`param.txt`).

## Setup

From the repository root, `./setup.sh` installs all dependencies and YAeHMOP. Alternatively:

```bash
cd band_runner
./setup.sh
```

## MoS2 example

```bash
./run_example.sh
```

Outputs are written under `results/` as a CSV table, a PNG band plot, and YAeHMOP work/log files.

## General command

```bash
python huckel_yaehmop.py structure.cif \
  --param param.txt \
  --symmetry-points k1x k1y k2x k2y ... \
  --point-dim 2 \
  --labels G M K G \
  --points-per-line 100
```

Use `--zero vbm` (default) to shift the plotted energy zero to the valence-band maximum, or `--zero none` to keep raw YAeHMOP eigenvalues.

The historical misspelling `--symetry-points` is accepted as an alias for compatibility.
