# MoS2 image-fitting example

This example is a controlled validation case for the image-based fitter.

- Material: monolayer MoS2 (`1MoS2-1` in C2DB)
- Source page: https://c2db.fysik.dtu.dk/material/1MoS2-1
- Structure: C2DB CIF
- Reference: PBE, no SOC
- Path: `Gamma-M-K-Gamma`
- Image energy range: `-15 ... 11 eV`
- Model basis inferred from stock YAeHMOP: 17 spatial orbitals
- Neutral valence-electron count: 18 (9 occupied spatial bands)

`band.png` is a clean raster reference generated for this test from the public C2DB band data. The optimizer receives only the CIF, the image, the image energy scale, and the path coordinates; numerical reference eigenvalues are not supplied to the fitter.

For a frontier-only demonstration, use:

```bash
../../run_example_frontier.sh
```

The `-2 ... 2 eV` window selects reference points near the valence/conduction frontier while retaining an explicit gap term and stronger default parameter regularization.
