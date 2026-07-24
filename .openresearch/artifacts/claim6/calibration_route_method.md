# Claim 6 calibration route

The paper names HTMP and gives dimensions 8000 by 4000, but does not provide
generator code, a finite-sample algorithm, a seed, or the mapping from its
displayed `kappa` to the cited beta-Laguerre sampler API.

This route tests five defensible mappings without tuning against a single
curve. It uses the cited finite beta-Laguerre construction, the full paper
dimensions, one fixed seed, and two first-hit anchors from each of the three
published iteration panels. A mapping is accepted only if it falls within all
six predeclared marker-width brackets.

The tested mappings are `beta=kappa/m`, `beta=kappa/n`, `beta=2*kappa/m`,
`beta=kappa/sqrt(m)`, and direct `beta=kappa`. The fixed horizon is 32, beyond
all paper first hits but selected independently of PRISM's theorem formulas.

This is a calibration route, not itself a verification of the full robustness
claim. Its verifier exits nonzero when no interpretation matches every panel.
