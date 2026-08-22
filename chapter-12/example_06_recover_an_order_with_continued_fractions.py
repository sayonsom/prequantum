from fractions import Fraction
from math import lcm


def denominator_candidate(outcome, counting_width, modulus):
    if outcome == 0:
        return None
    estimate = Fraction(outcome, 2**counting_width)
    return estimate.limit_denominator(modulus)


def validate_order_candidate(base, modulus, candidate):
    return candidate > 0 and pow(base, candidate, modulus) == 1


modulus = 21
base = 2
true_order = 6
counting_width = 10

# These are the nearest counting-register labels to s/r for s = 1, 2, and 5.
outcomes = [round((2**counting_width) * s / true_order) for s in (1, 2, 5)]
fractions = [denominator_candidate(y, counting_width, modulus) for y in outcomes]
denominators = [fraction.denominator for fraction in fractions if fraction is not None]
combined_candidate = lcm(*denominators)

assert fractions == [Fraction(1, 6), Fraction(1, 3), Fraction(5, 6)]
assert denominators == [6, 3, 6]
assert not validate_order_candidate(base, modulus, denominators[1])
assert validate_order_candidate(base, modulus, combined_candidate)
assert combined_candidate == true_order

print(f"outcomes={outcomes}")
print(f"continued_fraction_results={[str(value) for value in fractions]}")
print(f"denominators={denominators}")
print("single_denominator_3_is_complete_order=False")
print(f"validated_lcm_order={combined_candidate}")
