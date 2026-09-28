# Method

## Electronic-structure engine

All Hamiltonian, overlap, periodic-boundary, and generalized-eigenvalue calculations are performed by the original YAeHMOP `bind` executable. The Python layer writes YAeHMOP inputs and parameter tables, executes `bind`, parses `.band` output, and optimizes the parameter vector.

## Parameter vector

For every element/orbital available in YAeHMOP's atomic table, the generic fitter can vary:

- orbital on-site energy `Hii`,
- first Slater exponent `zeta1`,
- second Slater exponent `zeta2` for double-zeta shells,
- double-zeta coefficient ratio,
- global Wolfsberg-Helmholtz-like `K` (`THE CONST` in YAeHMOP).

A physical constraint requires `zeta1 > zeta2 + 0.12` for double-zeta shells.

## Image digitization

The image reader detects a dark rectangular plotting frame, maps pixel rows to energy using `--emin/--emax`, extracts colored (preferred blue) or dark band pixels, then reconstructs the expected number of ordered bands. A monotone dynamic-programming assignment preserves multiplicity when several degenerate states appear as one raster curve.

## Energy alignment

The EHT and reference spectra are aligned by their mid-gap energy before the RMSE is evaluated. This removes an arbitrary global energy-zero offset.

## Objective

For V2 the objective is conceptually

```text
loss = 0.4 * RMSE
     + 0.6 * weighted_RMSE
     + gap_weight * |Egap_model - Egap_reference|
     + reg_weight * parameter_regularization
```

The near-frontier weighting is determined from reference-band energy centers. If `--fit-window EMIN EMAX` is supplied, the RMSE terms are evaluated only on reference points inside the window, while the gap term stays explicit.

The regularization measures parameter displacement from the tabulated YAeHMOP starting point in scaled parameter coordinates. It is intentionally stronger by default for a restricted energy-window fit because unconstrained deep/high states otherwise allow large parameter excursions.

## Optimizer

The staged fitter uses:

1. differential evolution + Nelder-Mead for exponents/mixing/K,
2. differential evolution + Nelder-Mead for `Hii`,
3. conservative joint Nelder-Mead refinement.

An optimizer reaching its iteration budget is not equivalent to a mathematical proof of convergence. Inspect the history file and repeat with alternative settings/seeds for publication-grade parameter sets.
