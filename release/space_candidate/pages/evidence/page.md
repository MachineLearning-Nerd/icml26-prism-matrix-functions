# Evidence

> **ARCHIVED REJECTED BASELINE.** The output below is from the former 6×6
> toy/proxy verifier. It is not the current claim evidence and must not be
> read as full-scale verification. See [Current verification](#/current-verification)
> for the fail-closed claim ledger.


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_33bb14ecd4e2", "created_at": "2026-07-22T03:59:18+00:00", "title": "Verification output (last 40 lines)"}
-->
## Verification output (last 40 lines)

```

==============================================================================
CLAIM 3: randomized sketching reduces cost while maintaining accuracy
==============================================================================
  ||sign_exact - sign_sketch||_F = 0.000000 (< 1.0)
  -> PASS

==============================================================================
CLAIM 4: PRISM in optimizer produces valid preconditioner (proxy for Shampoo)
==============================================================================
  original cond=10.00, preconditioned cond=9.98 (improved)
  (Paper: Shampoo + CIFAR; we verify preconditioner improvement as proxy.)
  -> PASS

==============================================================================
CLAIM 5: PRISM's adaptive degree converges faster than fixed-degree
==============================================================================
  adaptive (Newton) final error: 8.39e-01
  linear final error: 1.36e+10
  adaptive faster: True
  -> PASS

==============================================================================
CLAIM 6: PRISM achieves high accuracy (||I-X^2|| -> 0)
==============================================================================
  final ||I-X^2|| = 2.36e-04 (< 0.01)
  -> PASS

==============================================================================
VERDICT SUMMARY
==============================================================================
  [FAIL] c1_polynomial
  [PASS] c2_quadratic
  [PASS] c3_sketching
  [PASS] c4_shampoo_proxy
  [PASS] c5_adaptive_faster
  [PASS] c6_accuracy

  5/6 claims verified.
  wrote outputs/verdict.json
```
