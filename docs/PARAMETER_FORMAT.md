# Parameter File Format

A fitted `param_<tag>.txt` contains global YAeHMOP controls followed by an EHT parameter table.

Example:

```text
K = 1.75
WEIGHTED_HIJ = true

MO    42     6     1     5  s  -8.340000   1.960000   0.000000   1.000000   0.000000
MO    42     6     1     5  p  -5.240000   1.900000   0.000000   1.000000   0.000000
MO    42     6     2     4  d -10.500000   4.540000   1.900000   1.000000   1.000000
END
```

Columns after the element symbol are:

1. atomic number,
2. nominal valence-electron count used by YAeHMOP,
3. number of zeta functions (`1` or `2`),
4. principal quantum number,
5. orbital type (`s`, `p`, `d`, `f`),
6. `Hii` on-site energy (eV),
7. `zeta1`,
8. `zeta2`,
9. coefficient `c1`,
10. coefficient `c2`.

The fitter stores a raw double-zeta coefficient ratio by writing `c1 = 1` and `c2 = ratio`; YAeHMOP performs its internal normalization.

`K` is written as `THE CONST` in the generated YAeHMOP input. `WEIGHTED_HIJ = true` uses YAeHMOP's weighted off-diagonal Hamiltonian prescription.
