"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.9 From Textbook to Grid: Running QuantumGridOS on Real Hardware
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_17_from_textbook_to_grid_running_quantumgri.py
"""

# What happens when the problem is too big for NISQ?
# Let's check circuit requirements for larger grids

test_cases = [
    (5,  1,  'IEEE 5-bus, 1 period'),
    (5,  4,  'IEEE 5-bus, 4 periods'),
    (14, 1,  'IEEE 14-bus, 1 period'),
    (14, 4,  'IEEE 14-bus, 4 periods'),
    (14, 24, 'IEEE 14-bus, 24 periods'),
]

print(f"{'Problem':<28} | {'Qubits':>7} | {'Est. CZs':>10} | {'NISQ?':>6}")
print("-" * 62)
for n_bus, periods, label in test_cases:
    net = qgo.PowerNetwork.from_ieee_case(n_bus)
    uc_test = qgo.UnitCommitment(network=net, periods=periods)
    qubo_test = uc_test.to_qubo(penalty_weight='auto')
    n_qubits = qubo_test.n_variables
    # Rough estimate: QAOA with p=2 needs ~4.5 CZs per variable
    est_cz = int(n_qubits * 4.5)
    nisq_ok = "Yes" if n_qubits <= 30 and est_cz <= 200 else "No"
    print(f"{label:<28} | {n_qubits:>7} | {est_cz:>10} | {nisq_ok:>6}")

# Output:
# Problem                      |  Qubits |  Est. CZs |  NISQ?
# --------------------------------------------------------------
# IEEE 5-bus, 1 period         |      10 |        45 |    Yes
# IEEE 5-bus, 4 periods        |      40 |       180 |    No
# IEEE 14-bus, 1 period        |      25 |       112 |    Yes
# IEEE 14-bus, 4 periods       |     100 |       450 |    No
# IEEE 14-bus, 24 periods      |     600 |      2700 |    No
