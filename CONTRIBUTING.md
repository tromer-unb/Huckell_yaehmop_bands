# Contributing

Contributions that improve reproducibility, numerical validation, documentation, or support for additional reference formats are welcome.

Before submitting changes:

1. keep YAeHMOP as the underlying EHT engine rather than silently replacing its formalism,
2. add or update tests for behavior changes,
3. distinguish implemented features from roadmap ideas,
4. document spin/SOC assumptions and energy-zero conventions,
5. avoid committing generated optimization work directories or virtual environments,
6. run `pytest -q` and, for optimizer changes, `RUN_SLOW_FIT=1 pytest -q tests/test_parameter_fitter_slow.py`.

For numerical-format adapters, preserve the raw reference energies and metadata before applying any alignment/reduction policy.
