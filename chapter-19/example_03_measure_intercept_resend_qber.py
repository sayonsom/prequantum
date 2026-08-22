"""Estimate sifted-key QBER for ideal BB84 intercept-resend attacks."""

from statistics import NormalDist

import numpy as np


def one_trial(n_signals: int, intercept_fraction: float,
              rng: np.random.Generator) -> tuple[int, int]:
    alice_bits = rng.integers(0, 2, n_signals)
    alice_bases = rng.integers(0, 2, n_signals)
    bob_bases = rng.integers(0, 2, n_signals)
    intercepted = rng.random(n_signals) < intercept_fraction
    eve_bases = rng.integers(0, 2, n_signals)

    eve_bits = np.where(
        eve_bases == alice_bases,
        alice_bits,
        rng.integers(0, 2, n_signals),
    )
    delivered_bits = np.where(intercepted, eve_bits, alice_bits)
    delivered_bases = np.where(intercepted, eve_bases, alice_bases)
    bob_bits = np.where(
        bob_bases == delivered_bases,
        delivered_bits,
        rng.integers(0, 2, n_signals),
    )

    keep = alice_bases == bob_bases
    errors = int(np.count_nonzero(alice_bits[keep] != bob_bits[keep]))
    return errors, int(np.count_nonzero(keep))


def wilson_interval(errors: int, observations: int,
                    confidence: float = 0.95) -> tuple[float, float]:
    """Return a Wilson score interval for a binomial proportion."""
    z = NormalDist().inv_cdf(0.5 + confidence / 2)
    p_hat = errors / observations
    denominator = 1 + z**2 / observations
    center = (p_hat + z**2 / (2 * observations)) / denominator
    radius = (
        z
        * np.sqrt(
            p_hat * (1 - p_hat) / observations
            + z**2 / (4 * observations**2)
        )
        / denominator
    )
    return float(center - radius), float(center + radius)


def main() -> None:
    rng = np.random.default_rng(1903)
    print("intercept expected observed 95%_interval sifted")
    for fraction in (0.0, 0.25, 0.50, 0.75, 1.0):
        errors, sifted = one_trial(200_000, fraction, rng)
        observed = errors / sifted
        lower, upper = wilson_interval(errors, sifted)
        expected = fraction / 4
        print(
            f"{fraction:9.2f} {expected:8.4f} {observed:8.4f} "
            f"[{lower:.4f}, {upper:.4f}] {sifted:6d}"
        )
        assert abs(observed - expected) < 0.01

    print("Model scope: ideal single-photon BB84 with full random-basis intercept-resend")


if __name__ == "__main__":
    main()
