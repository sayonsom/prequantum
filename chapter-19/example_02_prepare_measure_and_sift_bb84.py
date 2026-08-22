"""Simulate the ideal prepare, measure, and sift portion of BB84.

This is a protocol model, not a secure QKD implementation.  It omits channel
authentication, error correction, privacy amplification, finite-key analysis,
device imperfections, and key use.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Transcript:
    alice_bits: np.ndarray
    alice_bases: np.ndarray
    bob_bases: np.ndarray
    bob_results: np.ndarray
    keep: np.ndarray


def measure(prepared_bit: int, prepared_basis: int, measured_basis: int,
            rng: np.random.Generator) -> int:
    """Return the ideal projective-measurement outcome for a BB84 state."""
    if prepared_basis == measured_basis:
        return prepared_bit
    return int(rng.integers(0, 2))


def run_bb84_transmission(n_signals: int = 32, seed: int = 1902) -> Transcript:
    rng = np.random.default_rng(seed)
    alice_bits = rng.integers(0, 2, n_signals)
    alice_bases = rng.integers(0, 2, n_signals)  # 0=Z, 1=X
    bob_bases = rng.integers(0, 2, n_signals)
    bob_results = np.array(
        [
            measure(bit, basis, bob_basis, rng)
            for bit, basis, bob_basis in zip(alice_bits, alice_bases, bob_bases)
        ],
        dtype=int,
    )
    return Transcript(
        alice_bits=alice_bits,
        alice_bases=alice_bases,
        bob_bases=bob_bases,
        bob_results=bob_results,
        keep=alice_bases == bob_bases,
    )


def main() -> None:
    transcript = run_bb84_transmission()
    alice_sifted = transcript.alice_bits[transcript.keep]
    bob_sifted = transcript.bob_results[transcript.keep]

    print("index A_bit A_basis B_basis B_result keep")
    for index in range(len(transcript.alice_bits)):
        print(
            f"{index:>5} {transcript.alice_bits[index]:>5} "
            f"{transcript.alice_bases[index]:>7} "
            f"{transcript.bob_bases[index]:>7} "
            f"{transcript.bob_results[index]:>8} "
            f"{str(bool(transcript.keep[index])):>4}"
        )
    print(f"Sifted positions: {int(transcript.keep.sum())}")
    print(f"Sifted strings match: {np.array_equal(alice_sifted, bob_sifted)}")

    assert transcript.keep.any()
    assert np.array_equal(alice_sifted, bob_sifted)


if __name__ == "__main__":
    main()
