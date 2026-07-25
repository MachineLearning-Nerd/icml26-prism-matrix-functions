# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_ba611c2a9883", "created_at": "2026-07-22T03:59:17+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. PRISM reformulates iterative matrix-function algorithms as spectrum-adaptive polynomial approximation, fitting g_d(ξ;α)=f_{d-1}(ξ)+αξ^d to residual-matrix eigenvalues without requiring explicit spectral or singular-value bounds (Section 4.1).
2. Theorem 1 proves that for degree d=1 with α∈[1/2,1], PRISM's iterates converge quadratically, with error bound ||I−X_k^2||_2 ≤ ||I−A^2||_2^{2^{k-2}} (Section 4, Theorem 1).
3. PRISM uses randomized (oblivious subspace embedding) sketching with p ≥ 48(log n + log(1/δ) + log k + 27.6) Gaussian entries to reduce the per-iteration cost from O(n^3) to O(n^2 log n) while preserving a worst-case quadratic convergence rate (Section 4.2, Theorem 2).
4. When integrated into the Shampoo optimizer for ResNet-20 on CIFAR-10 and ResNet-32 on CIFAR-100, PRISM with 5 iterations matches or outperforms exact eigendecomposition in wall-clock time (Section 6.2, Figure 5).
5. When integrated into the Muon optimizer for a 10-layer, 1024-dimension GPT-2-Large model trained on 200M FineWeb tokens, PRISM-5 achieves a validation loss of 5.0251, versus 5.4523 for PolarExpress and 6.8689 for AdamW (Section 6.2, Figure 6).
6. On Gaussian random matrices with aspect ratios γ=n/m ∈ {1,4,50} and heavy-tailed Marchenko–Pastur matrices with condition numbers κ ∈ {0.1,0.5,100}, PRISM maintains stable convergence speed where the PolarExpress baseline degrades (Section 6.1, Figures 3-4).
