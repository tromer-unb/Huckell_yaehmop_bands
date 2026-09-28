# Shared-parameter fitting

`parameter_fitter/fit_shared.py` fits **one common YAeHMOP parameter set** to several band-structure references at the same time.

This is the generic version of the shared-parameter strategy used in the paper's 2H-TMD transferability study. The systems may contain different structures, different numbers of atoms, different band paths, and different subsets of chemical elements. What is shared is the atomic EHT parameter set and a single global `K` value.

For example, a joint fit to MoS2, WS2, and MoTe2 uses one Mo parameter set wherever Mo occurs, one W set, one S set, one Te set, and one shared `K`. The optimizer minimizes the weighted mean loss over the training systems plus regularization.

## Basic command

```bash
python parameter_fitter/fit_shared.py systems.yaml \
  --outdir results_shared \
  --tag family_shared
```

The YAML file describes all systems. `role: train` systems contribute to the objective. `role: test` systems are evaluated only after the shared parameters are frozen, which provides a direct transferability test.

## What is shared

For a graphene-vacancy data set, every system contains only carbon. A single vector such as

```text
C 2s: Hii, zeta
C 2p: Hii, zeta
K: shared
```

is used for pristine graphene, 1-vacancy, 2-vacancy, and 3-vacancy structures. A vacancy is not a special EHT parameter; it is represented by the changed structure and coordination in the CIF.

Each system is run independently through YAeHMOP during every objective evaluation. The per-system losses are combined as a weighted mean, so a larger supercell does not automatically dominate only because it contains more bands or atoms.

Conceptually,

```text
shared C parameters + shared K
        |        |        |
     pristine    1V       2V
        |        |        |
      YAeHMOP  YAeHMOP  YAeHMOP
        \________|________/
                 |
         weighted mean loss
                 |
             optimizer
```

## Graphene-vacancy example

A ready-to-edit template is provided at:

```text
paper_benchmark/examples/graphene_vacancies_shared.yaml
```

The template trains on pristine graphene, 1V, and 2V, and marks 3V as `role: test`. Therefore the 3V bands do not influence the optimization; they are calculated only after the shared C parameters have been fixed.

Check only the YAML schema without running YAeHMOP:

```bash
python parameter_fitter/fit_shared.py \
  paper_benchmark/examples/graphene_vacancies_shared.yaml \
  --validate-only
```

After replacing the placeholder paths with real CIF and band-image files, run:

```bash
python parameter_fitter/fit_shared.py \
  paper_benchmark/examples/graphene_vacancies_shared.yaml \
  --outdir results_graphene_shared \
  --tag graphene_C_shared
```

## YAML fields

Global options live under `shared:`. Important entries are:

- `fit_window: [-2, 2]` — fit only target states inside this energy interval;
- `gap_weight` — explicit gap penalty; use `0.0` for a dispersion-only transferability test;
- `reg_weight` — regularization toward stock YAeHMOP atomic parameters;
- `points_per_line` and `trace_nx` — fitting-grid and image-digitization resolution;
- `seed` and `optimizer` — reproducibility and optimizer budget;
- `initial_results` — optional list of individual `fit_eht_v2.py` JSON results used only to construct the starting guess.

Each entry in `systems:` has its own `structure`, `reference`, image calibration (`emin`, `emax`), reciprocal-space path, labels, `weight`, and `role`.

Different systems do **not** need to use the same reciprocal-space path. This is important for vacancy supercells because band folding changes the Brillouin zone. Use the path appropriate to each supercell rather than copying the primitive-cell path blindly.

A test system may use only elements that appeared in at least one training system. Otherwise those atomic parameters were never learned and the script stops with an error instead of presenting the result as transferability.

## Optional warm start from individual fits

The paper's shared-TMD workflow used the independent fits only as a **starting guess**, not as the final transferable parameter set. You can do the same here:

1. Fit each training system independently with `fit_eht_v2.py`.
2. Add the resulting JSON files under `shared.initial_results` in the YAML.
3. Run `fit_shared.py`.

For every matching variable, the script averages the individual `best_x` values to initialize the shared optimization. It then performs a new simultaneous optimization over all training systems. If `initial_results` is omitted, the fit starts from the stock YAeHMOP table.

## Outputs

For `--tag graphene_C_shared`, the main files are:

```text
results_graphene_shared/
  param_graphene_C_shared.txt
  param_graphene_C_shared_native.dat
  graphene_C_shared.json
  graphene_C_shared_history.csv
  work/
```

The JSON contains final metrics for both training and held-out test systems. `param_graphene_C_shared.txt` is the portable shared parameter file to use with `band_runner/` on another compatible structure without refitting.

## Important physics caveat for graphene vacancies

The current YAeHMOP workflow is spinless and has no explicit SOC. Vacancy defects in graphene can produce localized magnetic states in spin-polarized DFT. A spin-split reference cannot be reproduced state-by-state by the present model.

For a controlled benchmark of the current shared fitter, use a consistent non-spin-polarized/non-SOC reference or explicitly define how the spin channels are reduced before fitting. Do not interpret a spinless fit as a quantitative model of defect magnetism.

For transferability, prefer a held-out test such as:

```text
train: pristine + 1V + 2V
test:  3V
```

or repeat leave-one-structure-out folds. Training and testing on the same structures measures joint calibration quality, not out-of-sample transferability.
