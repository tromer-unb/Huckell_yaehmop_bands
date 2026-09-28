# Preparing a Band-Structure Image

The image interface is intentionally simple, but a clean plot matters because the raster is numerical input.

## Recommended image characteristics

- PNG is preferred; high-resolution JPG can also work.
- Use a full rectangular plot frame whenever possible.
- Use thin, high-contrast band lines. Saturated blue is the most reliable with the current mask; dark monochrome lines are the fallback.
- Avoid fat-band marker sizes, projected-color maps, dense legends inside the axes, or text crossing the bands.
- Keep the energy axis linear.
- Know the exact vertical energy limits shown in the image. Pass them as `--emin` and `--emax`.
- Provide the exact reciprocal-space path coordinates and matching labels used to make the plot.

## Critical distinction: image scale vs fitting window

If the plotted image covers `-15 ... 11 eV`, always use:

```bash
--emin -15 --emax 11
```

Even when only frontier bands are of interest. Restrict the optimization separately:

```bash
--fit-window -2 2
```

Changing `--emin/--emax` to `-2/2` for a figure that actually spans `-15/11` would assign the wrong energy to every pixel.

## Spin and SOC

The current YAeHMOP model is spinless and has no SOC. Prefer a non-spin-polarized, no-SOC reference or a carefully constructed center/average representation. A raw SOC-split plot should not be expected to match state-by-state.

## Image-derived uncertainty

The vertical pixel spacing sets a natural energy-resolution floor. If an image of height `H` pixels covers an energy span `Delta E`, one pixel corresponds approximately to `Delta E/(H-1)`. Use numerical eigenvalues rather than raster fitting when the target accuracy approaches this floor.
