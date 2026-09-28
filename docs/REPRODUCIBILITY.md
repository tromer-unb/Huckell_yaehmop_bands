# Reproducibility and Validation

## Pinned engine

The repository builds YAeHMOP at commit:

```text
4ded45bb2bb7a2d38d2527c991debce9226a9066
```

The setup script records the commit in each generated `yaehmop/UPSTREAM_COMMIT` file.

## Deterministic fitting seed

The current staged fitter defaults to seed `20260927`. A fixed seed makes the stochastic differential-evolution stage reproducible for a fixed software stack and platform, although tiny floating-point differences across compilers/BLAS libraries are possible.

## MoS2 controlled image test

The included MoS2 example uses a controlled no-SOC band image and a `Gamma-M-K-Gamma` path. The V2 frontier test (`-2 ... 2 eV`) was validated locally before publication. The regression test intentionally checks tolerances rather than exact byte-for-byte floating-point values.

## Training vs validation

A dense YAeHMOP k-grid is useful for checking interpolation and numerical smoothness, but it is not an independent DFT validation set. For scientific transferability claims, validate fitted parameters against additional DFT structures, distortions/strains, or held-out raw k-points.

## What a low image-fit error means

A low objective means the parameterized EHT model reproduces the chosen image/path/window under the current loss function. It does not prove universal transferability, correct orbital character, SOC physics, magnetism, or accuracy outside the fitted energy range.
