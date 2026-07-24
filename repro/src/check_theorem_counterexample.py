"""Independent checker for the theorem counterexample certificate.

This checker deliberately does not import the primary verifier.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


Matrix = list[list[Fraction]]
ROOT = Path(__file__).resolve().parents[2]


def eye(n: int) -> Matrix:
    return [
        [Fraction(int(row == col)) for col in range(n)] for row in range(n)
    ]


def multiply(left: Matrix, right: Matrix) -> Matrix:
    return [
        [
            sum(
                (left[row][idx] * right[idx][col] for idx in range(len(right))),
                Fraction(0),
            )
            for col in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [left[row][col] + right[row][col] for col in range(len(left[0]))]
        for row in range(len(left))
    ]


def subtract(left: Matrix, right: Matrix) -> Matrix:
    return [
        [left[row][col] - right[row][col] for col in range(len(left[0]))]
        for row in range(len(left))
    ]


def scale(value: Fraction, matrix: Matrix) -> Matrix:
    return [[value * item for item in row] for row in matrix]


def transpose(matrix: Matrix) -> Matrix:
    return [list(row) for row in zip(*matrix)]


def scalar_identity_value(matrix: Matrix) -> Fraction | None:
    value = matrix[0][0]
    for row in range(len(matrix)):
        for col in range(len(matrix)):
            expected = value if row == col else Fraction(0)
            if matrix[row][col] != expected:
                return None
    return value


def parse_matrix(raw: list[list[int]]) -> Matrix:
    return [[Fraction(item) for item in row] for row in raw]


def check(path: Path) -> tuple[bool, dict[str, object]]:
    payload = json.loads(path.read_text())
    matrix = parse_matrix(payload["matrix_A"])
    square = multiply(matrix, matrix)
    assumption_a2_symmetric = square == transpose(square)
    gram = multiply(transpose(matrix), matrix)
    assumption_norm_one = gram == eye(2)

    current = matrix
    trajectory: list[int] = []
    for _ in range(4):
        residual = subtract(eye(2), multiply(current, current))
        scalar = scalar_identity_value(residual)
        if scalar is None:
            return False, {"reason": "residual is not scalar identity"}
        trajectory.append(int(scalar))
        current = multiply(
            current, add(eye(2), scale(Fraction(1, 2), residual))
        )

    # At R=rI with r>=1, q(alpha)=1+(r-1)(1+r alpha)^2 and
    # q'(alpha)=2r(r-1)(1+r alpha)>0 on [1/2,1].
    minimizer_proof = all(
        residual >= 1
        and 2 * residual * (residual - 1) * (1 + residual / 2) > 0
        for residual in map(Fraction, trajectory)
    )
    theorem_1_contradiction = trajectory[2] > 2
    theorem_2_contradiction = trajectory[3] > 2
    is_counterexample = (
        assumption_a2_symmetric
        and assumption_norm_one
        and minimizer_proof
        and theorem_1_contradiction
        and theorem_2_contradiction
    )
    return is_counterexample, {
        "A_squared_symmetric": assumption_a2_symmetric,
        "spectral_norm_A": 1 if assumption_norm_one else None,
        "alpha_half_is_unique_minimizer": minimizer_proof,
        "trajectory": trajectory,
        "theorem_1_k2_actual": trajectory[2],
        "theorem_1_k2_bound": 2,
        "theorem_2_k3_actual": trajectory[3],
        "theorem_2_k3_bound": 2,
        "is_counterexample": is_counterexample,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate",
        nargs="?",
        type=Path,
        default=ROOT / ".openresearch/artifacts/claim2/counterexample.json",
    )
    args = parser.parse_args()
    valid, details = check(args.certificate)
    print("INDEPENDENT_CHECK=" + json.dumps(details, sort_keys=True))
    if not valid:
        print("NOT_A_COUNTEREXAMPLE")
        return 5
    print("VALID_STATED_ASSUMPTION_COUNTEREXAMPLE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
