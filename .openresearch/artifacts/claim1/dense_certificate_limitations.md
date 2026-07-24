# Dense certificate limitations

- Direct dense matrix products are run at reduced dimensions to keep a
  CPU-only check bounded. The separate spectral-coordinate route uses the
  paper's full dimensions.
- Controlled power-law spectra test qualitatively heavy tails without claiming
  to reproduce the paper's underspecified HTMP generator.
- This route verifies the adaptive polynomial mechanism, not GPU wall-clock
  acceleration or the randomized sketching theorem.
