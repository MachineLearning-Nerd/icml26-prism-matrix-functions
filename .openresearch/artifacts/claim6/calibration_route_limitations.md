# Calibration route limitations

- Figure D.2 supplies plotted markers rather than machine-readable source data;
  each anchor therefore has a one-marker tolerance bracket.
- The paper does not state the random seed, so exact pointwise equality is not
  expected.
- The finite chi sampler is numerically unstable when its shape approaches
  zero. Zero draws and zero eigenvalues are recorded rather than hidden.
- Passing this calibration would identify a plausible generator mapping. It
  would not by itself verify the complete Claim 6 comparison.
