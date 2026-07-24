# Claim 6 source audit

PRISM source: arXiv:2601.22137 HTML SHA-256
`9876b930c97063af87fbfc8eb51e577920d2047d76abd4f71c1f63570b9a4866`.
Anchors: Section 6.1, Figures 3-4, Appendix D Figures D.1-D.2, Appendix C.

Exact disclosed conditions:

- Gaussian `A in R^(n x m)`: `(15000,15000)`, `(20000,5000)`,
  `(100000,2000)`, giving `n/m` of 1, 4, and 50.
- HTMP: `A in R^(8000 x 4000)` with `kappa` 0.1, 0.5, and 100.
- float32 on an NVIDIA A100; error `||I-X_k^T X_k||_F`.
- degree-5 Newton-Schulz, PolarExpress, and PRISM are compared.

The text says PRISM converges fastest and calls its speed stable, but provides
no numerical table, seed count, random seeds, practical sketch dimension,
stopping tolerance, or executable code. This reproduction predeclares three
seeds, three RMS thresholds, and a 24-iteration horizon rather than choosing a
threshold after viewing results.

HTMP primary source: Hodgkinson, Wang, and Mahoney, arXiv:2506.03470,
Algorithm 2. Its printed off-diagonal `d_i t_i` is inconsistent with the
printed diagonal and produces an indefinite matrix. The PSD bidiagonal product
uses `d_(i+1) t_i`; this is the reconstructed generator used for evidence. The
literal printed version is retained as a negative control.
