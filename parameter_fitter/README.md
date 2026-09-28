# EHT Parameter Fitter

Fit material-specific YAeHMOP Extended-Hückel parameters from a CIF structure and a raster band-structure image.

## Recommended interface

Use `fit_eht_v2.py`. V1 files are kept for reproducibility.

```bash
python fit_eht_v2.py structure.cif band.png \
  --format image \
  --emin -15 --emax 11 \
  --symmetry-points 0 0  0.5 0  0.3333333333 0.3333333333  0 0 \
  --point-dim 2 --labels G M K G \
  --points-per-line 30 --trace-nx 401 \
  --outdir results --tag my_fit
```

## Frontier-only fit

```bash
--fit-window -2 2
```

This masks the reference point-by-point: only portions of the reconstructed reference bands whose energies lie inside the selected window contribute to the RMSE terms. The explicit gap term remains active.

When a fit window is active, V2 increases the default parameter regularization from `0.04` to `0.20` to reduce unphysical drift in spectral regions that are no longer constrained. Override this with `--reg-weight VALUE` if needed.

## Output

The main parameter file is `param_<tag>.txt`. The fitter also writes JSON metrics, an optimization-history CSV, the digitized target bands, and YAeHMOP work files.

See the repository-level documentation for image preparation, DFT-code workflows, model assumptions, and validation guidance.
