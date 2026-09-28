# Using References from Different Electronic-Structure Codes

The current fitter is **image-based**. It does not parse native VASP, Quantum ESPRESSO, or SIESTA band files directly. This makes the current interface broadly code-agnostic: generate a clean band plot from your preferred code, export the plot, and provide the same reciprocal-space path to the fitter.

## VASP

A common DFT workflow is a self-consistent calculation followed by a non-self-consistent band calculation on a line-mode `KPOINTS` path. VASP's official wiki describes this workflow and the use of fixed-charge-density band calculations.

Useful upstream documentation:

- https://vasp.at/wiki/Band-structure_calculation_using_DFT
- https://vasp.at/wiki/Category:Band_structure
- https://vasp.at/wiki/EIGENVAL

For this project, convert/plot the desired VASP eigenvalues using your normal plotting workflow, export a clean image, and pass the path endpoints to `fit_eht_v2.py`. Native `EIGENVAL`, `vasprun.xml`, and `PROCAR` parsing is not implemented here yet.

## Quantum ESPRESSO

Quantum ESPRESSO's `bands.x` post-processing program reads electronic-structure data, reorganizes eigenvalues into bands, and writes a band file that can be converted to a plottable form by `plotband.x`.

Official documentation:

- https://www.quantum-espresso.org/Doc/INPUT_BANDS.html
- https://www.quantum-espresso.org/Doc/user_guide_PDF/pp_user_guide.pdf

Plot/export the no-SOC (or otherwise model-compatible) band structure with known energy limits. The current release does not directly parse `filband` or `plotband.x` numerical output.

## SIESTA

SIESTA supports explicit `BandLines` definitions and writes a `.bands` file. The official tutorials demonstrate plotting via `gnubands`/gnuplot.

Official documentation:

- https://docs.siesta-project.org/projects/siesta/en/5.4/reference/siesta.html#band-structure-analysis
- https://docs.siesta-project.org/projects/siesta/en/5.4/tutorials/basic/electronic-structure-analysis/bands/

Export the plot as a clean raster image and supply the `BandLines` endpoints/labels to this fitter. Direct `.bands` parsing is a planned extension, not a current feature.

## Other codes

The same logic applies to ABINIT, GPAW, WIEN2k, CASTEP, CP2K, Elk, and other codes: the present interface only requires a valid CIF, a compatible band image, and the path coordinates used to construct that image.

## What must be consistent

Regardless of the DFT package:

1. The CIF geometry should correspond to the calculation used for the reference bands.
2. The reciprocal coordinates passed to the fitter must represent the same path and reciprocal basis used in the plot.
3. The energy limits passed as `--emin/--emax` must match the visible plot bounds.
4. The spin/SOC content should be compatible with the spinless YAeHMOP model.
5. Do not compare a path-limited gap to a fully sampled Brillouin-zone indirect gap without explicitly stating the difference.
