# Claim 3 method

Use the Claim 2 matrix and `n=2`, `delta=0.1`, `k=3`. The printed threshold is
`p >= 1522`.

For `R=rI`,
`||S h(R,alpha)||_F = |h(r,alpha)| ||S||_F`. A Gaussian `S` is nonzero almost
surely, so sketching cannot change the unique optimizer `alpha=1/2`. The exact
residual at `k=3` is `33125`, while the claimed bound is `2`. Hence failure
probability is one, greater than `delta=0.1`.

This resolves the quadratic-preservation conjunct of the imported claim. The
separate arithmetic-cost observation `O(p n^2)` is not disputed.
