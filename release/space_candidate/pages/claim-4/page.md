# Claim 4 — Shampoo/ResNet timing

## Exact contract

Section 6.2, Figure 5, and Appendix E.1 report that five PRISM matrix
iterations match or outperform exact eigendecomposition in first-50-epoch
wall-clock time on the authors' modified stride-one ResNet-20/CIFAR-10 and
ResNet-32/CIFAR-100 Shampoo runs.

Source: arXiv:2601.22137 HTML retrieved 2026-07-24, SHA-256
`9876b930c97063af87fbfc8eb51e577920d2047d76abd4f71c1f63570b9a4866`.

Disclosed fields include Shampoo `p=2`, learning rate `.001`, weight decay
`.0005`, and maximum preconditioner size `2048`. Missing fields include channel
widths, batch/data protocol, schedule, preconditioner update/start frequency,
seeds, executable revision, raw curves, and timing protocol.

## Four routes and result

**BLOCKED — LOW confidence.**

1. Exact source reconstruction enumerated the missing operational fields.
2. Public Shampoo and arXiv artifacts contain no PRISM integration or raw run.
3. Deliberately smaller CPU networks without Shampoo established only optimistic
   feasibility bounds: fastest observed 50-epoch lower bounds were 4.59 h and
   7.61 h. These are not the paper models and are not reproduction evidence.
4. Mandatory falsification rejected the CPU candidate because it violates the
   exact model, optimizer, and timing assumptions.

The route exits `8` for BLOCKED; the independent checker exits `0`; the shared
contract mutation exits `9`.

- [Executable four-route verifier](/code/training_claims_closure.py)
- [Independent checker](/code/check_training_claims_closure.py)
- [Contract](/evidence/claim4/claim_contract.json)
- [Raw summary](/evidence/claim4/raw_result.json)
- [Checker output](/evidence/claim4/checker_output.txt)
- [Negative control](/evidence/claim4/negative_control_output.txt)

Unblocker: exact modified models, PRISM-Shampoo integration, seeds, complete
data protocol, raw accuracy/time trajectories, and original timing protocol.
