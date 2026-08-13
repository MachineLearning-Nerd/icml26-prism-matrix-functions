# Source manifest

## Paper

- Title: *PRISM: Distribution-free Adaptive Computation of Matrix Functions
  for Accelerating Neural Network Training*
- Authors: Shenghao Yang, Zhichao Wang, Oleg Balabanov, N. Benjamin Erichson,
  and Michael W. Mahoney
- arXiv: [2601.22137v1](https://arxiv.org/abs/2601.22137)
- OpenReview: [hwhvjhXC0m](https://openreview.net/forum?id=hwhvjhXC0m)
- DOI: [10.48550/arXiv.2601.22137](https://doi.org/10.48550/arXiv.2601.22137)
- Source boundary: the claim ledger uses the paper's v1 source and its
  printed assumptions, theorem statements, experimental descriptions, and
  reported numbers. No official author implementation is implied by this
  repository.

## Repository evidence

- Current executable entry point:
  `uv run --frozen --python 3.11 python repro/src/run_reproduction.py`
- Current claim artifacts: `.openresearch/artifacts/claim{1..6}/`
- Evaluator-visible evidence: `release/space_candidate/evidence/`
- Technical narrative: `reports/prism-reproduction/report.md`
- Historical rejected baseline: `repro/src/verify_prism.py` and the copied
  historical Space snapshot. These files are preserved for lineage and are not
  current evidence.

## Citation

```bibtex
@article{yang2026prism,
  title={PRISM: Distribution-free Adaptive Computation of Matrix Functions for Accelerating Neural Network Training},
  author={Yang, Shenghao and Wang, Zhichao and Balabanov, Oleg and Erichson, N. Benjamin and Mahoney, Michael W.},
  journal={arXiv preprint arXiv:2601.22137},
  year={2026},
  doi={10.48550/arXiv.2601.22137}
}
```

## Thank-you note

Thank you to Shenghao Yang, Zhichao Wang, Oleg Balabanov, N. Benjamin
Erichson, and Michael W. Mahoney for making the PRISM paper and its claims
available for independent study. This repository is an independent audit for
reproducibility and does not represent the authors' implementation, approval,
or endorsement.
