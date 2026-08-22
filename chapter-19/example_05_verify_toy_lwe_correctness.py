"""Verify the correctness margin of a deliberately insecure toy LWE scheme.

The arithmetic illustrates modular noise and decoding.  The parameters,
samplers, and construction are unsuitable for protecting any real data, and
the program is not an implementation of ML-KEM.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ToyPublicKey:
    matrix: np.ndarray
    noisy_product: np.ndarray
    modulus: int


def centered(value: int, modulus: int) -> int:
    """Map a residue to a representative near zero."""
    return int((value + modulus // 2) % modulus - modulus // 2)


def keygen(rng: np.random.Generator, n: int = 8, m: int = 12,
           modulus: int = 257) -> tuple[ToyPublicKey, np.ndarray]:
    secret = rng.integers(-1, 2, n)
    matrix = rng.integers(0, modulus, (m, n))
    error = rng.integers(-1, 2, m)
    noisy_product = (matrix @ secret + error) % modulus
    return ToyPublicKey(matrix, noisy_product, modulus), secret


def encrypt(public_key: ToyPublicKey, bit: int,
            rng: np.random.Generator) -> tuple[np.ndarray, int]:
    if bit not in (0, 1):
        raise ValueError("the toy encoder accepts one bit")
    selector = rng.integers(0, 2, len(public_key.noisy_product))
    u = (public_key.matrix.T @ selector) % public_key.modulus
    v = int(
        (
            public_key.noisy_product @ selector
            + bit * (public_key.modulus // 2)
        )
        % public_key.modulus
    )
    return u, v


def decrypt(secret: np.ndarray, ciphertext: tuple[np.ndarray, int],
            modulus: int) -> tuple[int, int]:
    u, v = ciphertext
    residual = centered(int(v - u @ secret), modulus)
    distance_to_zero = abs(residual)
    distance_to_one = min(
        abs(residual - modulus // 2), abs(residual + modulus // 2)
    )
    return int(distance_to_one < distance_to_zero), residual


def main() -> None:
    rng = np.random.default_rng(1905)
    public_key, secret = keygen(rng)
    print("trial bit decoded centered_residual")
    for trial in range(20):
        bit = trial % 2
        decoded, residual = decrypt(
            secret, encrypt(public_key, bit, rng), public_key.modulus
        )
        print(f"{trial:5d} {bit:3d} {decoded:7d} {residual:17d}")
        assert decoded == bit

    print("All toy correctness checks passed.")
    print("Security claim: none; use a reviewed standards-conforming library.")


if __name__ == "__main__":
    main()
