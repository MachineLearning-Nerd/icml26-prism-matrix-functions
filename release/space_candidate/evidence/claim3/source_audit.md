# Claim 3 source audit

Theorem 2 (`Thmtheorem2`) prints sketch entries distributed as
`N(1,1/p)` and the dimension threshold constant `27.6`. Appendix B.3
(`A2.SS3`) again prints `N(1,1/p)` but invokes an OSE result only after
changing the dimension constant to `41.4`. These are source-visible
inconsistencies; the verifier uses the theorem statement (`27.6`) and does not
repair the nonzero sketch mean.

The same missing positivity assumption as Theorem 1 remains. The exact
counterexample is stronger than a Monte Carlo objection: for scalar residuals
`R=rI`, every nonzero sketch yields the same optimizer, so the claimed bound
fails with probability one for every allowed `p`.
