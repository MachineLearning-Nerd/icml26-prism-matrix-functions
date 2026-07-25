# Claim 5 source audit

Source: arXiv:2601.22137 HTML, retrieved 2026-07-24, SHA-256
`9876b930c97063af87fbfc8eb51e577920d2047d76abd4f71c1f63570b9a4866`.
Anchors: Section 6.2, Figure 6, Appendix E.2.

The disclosed protocol is 10 layers, 16 heads, width 1024, 200M FineWeb
tokens, global batch 32, microbatch 4, and A100-SXM4-80GB hardware. Crucially,
the appendix says PRISM5 used **three** matrix iterations, not five, with
`alpha=29/20` for the initial three.

Missing fields include tokenizer/vocabulary, sequence length, feed-forward
width and remaining architecture, FineWeb snapshot/subset/order, validation
split, learning-rate schedule/warmup, seeds, A100 worker count, executable
revision, checkpoints, and raw trajectories.
