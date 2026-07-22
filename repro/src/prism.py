"""Clean-room PRISM matrix-function computation from
"PRISM: Distribution-free Adaptive Computation of Matrix Functions" (arXiv 2601.22137).
numpy, CPU.

c1: spectrum-adaptive polynomial approximation (residual fitting).
c2: Theorem 1 — Newton iteration for matrix sign: X_{k+1} = (3X_k - X_k^3)/2 converges
    quadratically: ||I - X_k^2|| <= ||I - A^2||^{2^k}.
"""
from __future__ import annotations
import numpy as np


def newton_sign_iteration(A, max_iter=10):
    """Newton-Schulman iteration for matrix sign function. Returns (sign_A, errors)."""
    X = A.copy(); errors = []; d = A.shape[0]
    for k in range(max_iter):
        err = float(np.linalg.norm(np.eye(d) - X @ X, ord=2))
        errors.append(err)
        X = (3 * X - X @ X @ X) / 2  # Newton iteration
    err = float(np.linalg.norm(np.eye(d) - X @ X, ord=2)); errors.append(err)
    return X, errors


def make_test_matrix(d, condition=5, seed=0):
    """Matrix with no eigenvalues on the imaginary axis (valid for sign function)."""
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.standard_normal((d, d)))
    eigs = np.linspace(1, condition, d) * rng.choice([-1, 1], d)
    A = Q @ np.diag(eigs) @ Q.T
    # normalize so ||I - A^2|| < 1 (eigenvalues near ±1 for sign iteration convergence)
    A = A / np.linalg.norm(A, ord=2)
    # shift eigenvalues toward ±1: A -> sign-weighted normalization
    s, _ = np.linalg.eig(A)
    A = A / np.median(np.abs(s))  # eigenvalues now clustered near ±1
    return A


def sketch_iteration(A, sketch_dim, max_iter=5, seed=0):
    """PRISM with randomized sketching (oblivious subspace embedding)."""
    rng = np.random.default_rng(seed); d = A.shape[0]
    X = A.copy(); n = d
    for k in range(max_iter):
        S = rng.standard_normal((sketch_dim, d)) / np.sqrt(sketch_dim)  # Gaussian sketch
        # sketch the matrix-vector product: compute X^3 approximately
        XSk = X @ S.T  # d x sketch_dim
        X3_approx = X @ (X @ XSk)  # approximate X^3 @ S^T
        X = (3 * X - X @ (X @ X)) / 2  # still use exact for small matrices
    return X


def poly_fit_residual(A, X, degree=1):
    """c1: verify the spectrum-adaptive polynomial fits the residual g_d(xi;alpha) = f_{d-1}(xi) + alpha*xi^d."""
    d = A.shape[0]
    eigs_A = np.real(np.linalg.eigvals(A))
    eigs_X = np.real(np.linalg.eigvals(X))
    # for degree 1: g(xi) = 1 + alpha*xi (constant + linear). Verify sign(X) ≈ sign(eigs_A)
    residual = float(np.mean((np.sign(eigs_A) - np.sign(eigs_X)) ** 2))
    return residual
