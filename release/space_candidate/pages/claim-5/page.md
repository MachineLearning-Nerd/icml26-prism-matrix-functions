# Claim 5 — Muon/GPT training losses

## Exact contract and source correction

Section 6.2, Figure 6, and Appendix E.2 report validation losses `5.0251`
(PRISM5), `5.4523` (PolarExpress), and `6.8689` (AdamW) after a 200M-FineWeb-
token run of a 10-layer, 16-head, width-1024 GPT-style model.

The appendix says **PRISM5 used three matrix iterations**, with
`alpha=29/20` for the initial three. The imported five-iteration wording is not
the paper protocol; the negative control requires that mutation to fail.

## Four routes and result

**BLOCKED — LOW confidence.**

1. Source reconstruction found that tokenizer, sequence length, feed-forward
   width, remaining architecture, FineWeb snapshot/order/split, schedule,
   seed, worker topology, and executable are missing.
2. The arXiv archive, modded-nanogpt, and PolarExpress public artifacts contain
   no exact training implementation, raw trajectories, or checkpoint.
3. The fastest optimistic CPU `6NT` bound observed was 7.91 days. It is only a
   feasibility bound and omits missing model/data details.
4. Mandatory falsification rejected any downscaled CPU model because it cannot
   contradict the particular unpublished author run.

The route exits `8`, independent checker `0`, and mutation `9`.

- [Executable four-route verifier](/code/training_claims_closure.py)
- [Independent checker](/code/check_training_claims_closure.py)
- [Contract](/evidence/claim5/claim_contract.json)
- [Raw summary](/evidence/claim5/raw_result.json)
- [Checker output](/evidence/claim5/checker_output.txt)
- [Negative control](/evidence/claim5/negative_control_output.txt)

Unblocker: exact model/training code, FineWeb sample/order/validation split,
seed, schedule, worker topology, checkpoints, and raw trajectories.
