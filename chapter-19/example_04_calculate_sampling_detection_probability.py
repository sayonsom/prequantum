"""Calculate detection probabilities for sampled BB84 sifted bits."""

from math import comb


def miss_probability_without_replacement(
    sifted_bits: int, erroneous_bits: int, revealed_bits: int
) -> float:
    """Probability that a random revealed sample contains no erroneous bit."""
    if not 0 <= erroneous_bits <= sifted_bits:
        raise ValueError("erroneous_bits must be within the sifted block")
    if not 0 <= revealed_bits <= sifted_bits:
        raise ValueError("revealed_bits must be within the sifted block")
    clean_bits = sifted_bits - erroneous_bits
    if revealed_bits > clean_bits:
        return 0.0
    return comb(clean_bits, revealed_bits) / comb(sifted_bits, revealed_bits)


def main() -> None:
    sifted_bits = 1_000
    erroneous_bits = 250
    print("revealed miss_probability detection_probability")
    previous_detection = -1.0
    for revealed_bits in (1, 5, 10, 20, 40, 80):
        miss = miss_probability_without_replacement(
            sifted_bits, erroneous_bits, revealed_bits
        )
        detection = 1 - miss
        print(f"{revealed_bits:8d} {miss:16.10f} {detection:21.10f}")
        assert detection > previous_detection
        previous_detection = detection

    print("Revealed sample bits cannot remain in the secret key.")
    print("A production protocol also needs a finite-key security proof.")


if __name__ == "__main__":
    main()
