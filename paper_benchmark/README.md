# Paper benchmark: 2D and 3D Extended-Hückel calibration

This directory contains the **lightweight, publication-facing analysis artifacts** for the Physical Review Materials manuscript built around this repository.

The benchmark evaluates automated YAeHMOP Extended-Hückel calibration against numerical DFT band structures for:

- **20 two-dimensional materials** from C2DB, using the `PBE no SOC` trace;
- **8 three-dimensional solids** from JARVIS-DFT `OPT-Bandst` calculations;
- a six-member **2H-TMD leave-one-compound-out transferability** test.

Raw database archives, optimizer work directories, and large intermediate arrays are intentionally excluded from GitHub. Source identifiers and compact aggregate results are retained so the published statistics remain traceable.

## Central results

| Protocol | Mean validation RMSE | Gap statistic |
| --- | ---: | ---: |
| 2D, no explicit gap term | 0.516 eV | gap MAE 0.684 eV |
| 2D, gap constrained | 0.716 eV | gap MAE 0.000725 eV |
| 3D, no explicit gap term | 1.031 eV | — |
| 3D, gap constrained | 1.240 eV | median |gap error| 0.000795 eV |
| TMD shared-parameter leave-one-out | 0.716 eV | gap MAE 0.442 eV |

## Directory layout

- `results/` — aggregate CSV/JSON tables, source manifests, and the parameter-bound audit.
- `scripts/plot_lightweight_results.py` regenerates the principal publication-facing summary figures directly from the versioned CSV tables; static figure binaries remain in the submission workspace.
- `representative_parameters/` — fitted parameter files for MoS2, h-BN, Si, and MgO.
- `representative_data/` — the corresponding CIF structures for direct band-runner reproduction.
- `results/tmd_shared_cv_summary.csv` — all six leave-one-out TMD metrics; `results/tmd_shared_mos2_holdout.json` stores one complete held-out shared-parameter example.
- `scripts/` — lightweight integrity checks and figure-regeneration scripts for the published aggregate tables.

## Representative parameter sets

The published examples deliberately span success and failure modes:

- `1MoS2-1`: typical 2D semiconductor;
- `1BN-1`: difficult wide-gap 2D manifold;
- `JVASP-116`: MgO, representative 3D insulating case;
- `JVASP-1002`: Si, retained as a minimal-basis failure case.

Each directory contains both `param_full.txt` (gap-constrained) and `param_nogap.txt` (dispersion-only) parameters. These files can be passed directly to the repository's `band_runner/` together with the matching CIF structure.

Example:

```bash
python band_runner/huckel_yaehmop.py \
  paper_benchmark/representative_data/1MoS2-1/structure.cif \
  --param paper_benchmark/representative_parameters/1MoS2-1/param_full.txt \
  --symmetry-points 0 0  0.5 0  0.3333333333 0.3333333333  0 0 \
  --point-dim 2 --labels G M K G --nkpoints 401
```

## Reproducing the aggregate analysis

The lightweight result tables are sufficient to reproduce the main benchmark statistics and most summary figures without downloading the original DFT archives:

```bash
python paper_benchmark/scripts/check_results.py
python paper_benchmark/scripts/plot_lightweight_results.py
```

Full numerical refitting requires obtaining the original DFT band data from C2DB/JARVIS. Those bulky source archives and database-specific acquisition helpers are not part of this lightweight package; source URLs/IDs needed to reconstruct the inputs are preserved in `results/source_manifest.csv`.

## Interpretation

The sub-meV gap agreement of the gap-constrained fits is **not a blind prediction**: the gap is explicitly present in that objective. The dispersion-only ablation is included to make this trade-off visible.

Likewise, the main 28-system benchmark uses system-specific parameters. Chemical transferability is probed separately by the 2H-TMD leave-one-compound-out experiments. Jointly learned shared parameters outperform naive averaging but do not yet constitute a universal EHT parameter library.

## Data policy

This GitHub repository intentionally omits bulky raw DFT archives and optimizer scratch directories. A versioned archival dataset suitable for DOI deposition should contain the complete numerical reference bands, optimization histories, and raw-source metadata when the manuscript is submitted/published.
