# Claim 2 source audit

Source: arXiv:2601.22137v1, ar5iv anchor `Thmtheorem1`, HTML SHA-256
`9876b930c97063af87fbfc8eb51e577920d2047d76abd4f71c1f63570b9a4866`.

The theorem quantifies over real square matrices with only
`0 < ||A||_2 <= 1` and symmetric `A^2`. It does **not** state that `A^2` is
positive semidefinite, that `A` has real spectrum, or that `A` has no
eigenvalues on the imaginary axis. Appendix B.2 later infers that the
eigenvalues of `A^2` lie in `[0,1]`; that inference needs an additional
positivity condition and is false under the printed assumptions.

The contract preserves the printed universal domain. It does not silently add
the assumption needed by the proof.
