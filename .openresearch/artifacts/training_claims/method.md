# Claims 4 and 5: four-route closure

Both training claims remain LOW confidence, so this experiment performs the
required sequence:

1. Reconstruct every stated source setting and enumerate missing operational
   fields.
2. Retrieve the public baseline artifacts and test whether they contain the
   unpublished PRISM integrations or exact paper identifier.
3. Measure CPU dense-GEMM throughput, benchmark deliberately smaller
   stride-one CIFAR networks, and compute an optimistic `6NT` lower bound for
   the 200M-token run. These are feasibility diagnostics, not claim proxies.
4. Seek falsification against the exact source quantifier. A different CPU
   model or run cannot contradict the authors' particular unpublished
   training runs, so both candidates are rejected and both claims are BLOCKED.

The negative control mutates the language-model contract to five PRISM5
iterations. The exact appendix says PRISM5 used three; the mutation must fail.
