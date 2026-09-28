# Troubleshooting

## `YAeHMOP bind not found`

Run repository setup:

```bash
./setup.sh
```

or point the code at an existing installation:

```bash
export YAEHMOP_BIND=/path/to/bind
export YAEHMOP_PARAM_FILE=/path/to/eht_parms.dat
```

## `Could not auto-detect plot frame`

Use a clean image with a full dark rectangular frame. Avoid cropped axes or plots where the spines are completely removed. Automatic arbitrary-image segmentation is still a development area.

## Wrong energies despite a visually correct trace

Check `--emin` and `--emax`. They calibrate the entire visible image; they are not fitting-window controls. Use `--fit-window` to restrict the fit.

## Missing element in YAeHMOP parameter table

The generic fitter starts from YAeHMOP's stock atomic table. If an element is absent there, a custom physically motivated initial parameter table is required; the current CLI does not synthesize unknown atomic parameters.

## Spin-polarized or SOC reference

The current model is spinless/no-SOC. Prefer a compatible reference. Directly fitting visible spin/SOC splitting is outside the present model.

## Optimizer reports `Maximum number of iterations has been exceeded`

This means the local optimizer reached its configured budget; it does not automatically invalidate the best solution found. Inspect the history, metrics, parameter plausibility, and repeat/extend optimization before drawing conclusions.
