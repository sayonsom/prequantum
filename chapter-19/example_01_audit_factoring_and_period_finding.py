"""Separate classical factoring, order finding, and Shor post-processing.

This program contains no quantum period-finding circuit.  It uses exhaustive
classical search so that every arithmetic step can be inspected.
"""

from math import gcd


def trial_factor(n: int) -> tuple[int, int] | None:
    """Return a non-trivial factor pair by classical trial division."""
    if n < 4:
        return None
    for candidate in range(2, int(n**0.5) + 1):
        if n % candidate == 0:
            return candidate, n // candidate
    return None


def classical_order(a: int, n: int) -> int:
    """Find the multiplicative order of a modulo n by exhaustive search."""
    if gcd(a, n) != 1:
        raise ValueError("a and n must be coprime")
    value = 1
    for order in range(1, n + 1):
        value = (value * a) % n
        if value == 1:
            return order
    raise RuntimeError("order was not found")


def shor_postprocess(a: int, order: int, n: int) -> tuple[int, int] | None:
    """Try to obtain factors from a measured order."""
    if order % 2:
        return None
    root = pow(a, order // 2, n)
    if root in (1, n - 1):
        return None
    left = gcd(root - 1, n)
    right = gcd(root + 1, n)
    if left in (1, n) or right in (1, n) or left * right != n:
        return None
    return tuple(sorted((left, right)))


def main() -> None:
    n, a = 15, 2
    factors_by_trial = trial_factor(n)
    order = classical_order(a, n)
    factors_from_order = shor_postprocess(a, order, n)

    residues = [pow(a, exponent, n) for exponent in range(2 * order)]
    print(f"N={n}, a={a}")
    print(f"Classical trial division: {factors_by_trial}")
    print(f"Classical exhaustive order: r={order}")
    print(f"Residues for two periods: {residues}")
    print(f"Post-processing from r: {factors_from_order}")
    print("Quantum period finding executed: no")

    assert factors_by_trial == (3, 5)
    assert order == 4
    assert residues[:order] == residues[order:]
    assert factors_from_order == (3, 5)


if __name__ == "__main__":
    main()
