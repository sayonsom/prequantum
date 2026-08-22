from math import gcd


def multiplicative_order(base, modulus):
    if gcd(base, modulus) != 1:
        raise ValueError("the order is defined here only for an invertible base")
    value = 1
    for order in range(1, modulus + 1):
        value = (value * base) % modulus
        if value == 1:
            return order
    raise AssertionError("an order should exist for an invertible residue")


def reduction_result(base, modulus):
    common = gcd(base, modulus)
    if common > 1:
        return "classical_gcd", (common, modulus // common)

    order = multiplicative_order(base, modulus)
    if order % 2 == 1:
        return "retry_odd_order", order

    half_power = pow(base, order // 2, modulus)
    factors = tuple(sorted((gcd(half_power - 1, modulus),
                            gcd(half_power + 1, modulus))))
    if 1 in factors or modulus in factors:
        return "retry_trivial_gcd", (order, half_power, factors)
    return "factors", (order, factors)


modulus = 21
cases = {base: reduction_result(base, modulus) for base in (2, 3, 4, 5, 8, 20)}

assert cases[2] == ("factors", (6, (3, 7)))
assert cases[3] == ("classical_gcd", (3, 7))
assert cases[4] == ("retry_odd_order", 3)
assert cases[5][0] == "retry_trivial_gcd"
assert cases[8] == ("factors", (2, (3, 7)))
assert cases[20][0] == "retry_trivial_gcd"

for base, result in cases.items():
    print(f"base={base:2d} result={result}")
