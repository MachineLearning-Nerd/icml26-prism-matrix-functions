# Claim 2 method

Use the exact real matrix `A = [[0,-1],[1,0]]`. Then `A^T A = I`, so
`||A||_2 = 1`, and `A^2 = -I`, which is symmetric. Thus every printed matrix
assumption holds.

With `R_0 = I-A^2 = 2I`, the degree-one update is
`X_{k+1}=X_k(I+alpha_k R_k)`. For any scalar residual `R_k=rI`, the exact
objective is proportional to
`q(alpha)=1+(r-1)(1+r alpha)^2`; for `r>=1`, `q` is strictly increasing on
`[1/2,1]`, so the unique optimizer is `alpha_k=1/2`. Exact rational arithmetic
then gives residual norms `2, 5, 50, 33125`.

At `k=2`, Theorem 1 claims a bound of `2`, but the exact norm is `50`.
This is a valid assumption-satisfying counterexample, not a failed run or a
tolerance-dependent numerical mismatch.
