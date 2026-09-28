# MoS2 band-runner example

This directory demonstrates calculation of YAeHMOP EHT bands from a CIF and an already fitted parameter file.

- Material: monolayer MoS2 (`1MoS2-1` in C2DB)
- Path used by `run_example.sh`: `Gamma-M-K-Gamma`
- `param.txt`: the stable full-spectrum image-fit parameter set retained as a deterministic band-runner example.

The end-to-end repository demo does not rely on this pre-fitted file: `scripts/run_mos2_demo.sh` first performs a new frontier fit, copies the newly fitted parameter file to the band-runner workflow, and then recalculates the bands.
