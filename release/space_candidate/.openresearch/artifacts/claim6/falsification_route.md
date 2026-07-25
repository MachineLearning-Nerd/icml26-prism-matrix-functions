# Claim 6 mandatory fourth route: falsification

## Exact statement and quantifier

The source says that adaptation lets PRISM converge fastest “in our
experiments.” This is a report about particular unpublished samples and
timings, not a theorem quantified over every HTMP matrix.

## Candidate and analytical checker

The independently normalized Equation E.5 route supplies a strong candidate:
the 4000 midpoint quantiles at `gamma=0.5`, `kappa=0.1`. Its minimum
eigenvalue is `4.91038285729026e-72`; its maximum is
`52.65631250687386`.

For any singular coordinate with residual in `[0,1]` and
`alpha <= 29/20`, one PRISM step amplifies the coordinate by at most
`1 + 1/2 + 29/20 = 2.95`. The independent checker therefore proves that the
smallest normalized coordinate remains at most `3.17e-22` after 32 steps, so
one residual coordinate remains essentially one. The run indeed had
Frobenius error `9.1957`, not below `1e-2`.

This contradicts a universalized “stable on HTMP matrices” reading. It does
not contradict the exact source statement: the candidate is not the authors'
unpublished random draw and does not reproduce A100 wall-clock timing.

## Result

**BLOCKED**, not FALSIFIED. A valid falsification would require the exact
public generator, seed/raw matrix, and timing protocol, or a source statement
with a universal quantifier. The negative control uses a zero singular value;
it is rejected because HTMP has positive support.
