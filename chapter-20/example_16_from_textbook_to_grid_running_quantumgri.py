"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.9 From Textbook to Grid: Running QuantumGridOS on Real Hardware
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_16_from_textbook_to_grid_running_quantumgri.py
"""

# Step 4: Solve on SIMULATOR first (always do this!)
# The simulator result is your ground truth
optimizer_sim = qgo.HybridOptimizer(
    qubo=qubo,
    backend='simulator',
    qaoa_layers=2,
    n_restarts=5,
    shots=4096,
)

result_sim = optimizer_sim.solve()
print(f"Simulator result:")
print(f"  Total cost: ${result_sim.total_cost:,.0f}")
print(f"  Feasible: {result_sim.feasible}")
print(f"  Schedule: {result_sim.schedule.flatten()}")
print(f"  Solver: {result_sim.solver_used}")
# Output:
# Simulator result:
#   Total cost: $4,850
#   Feasible: True
#   Schedule: [1 1 0]  (Gen 1: ON, Gen 2: ON, Gen 3: OFF)
#   Solver: qaoa_simulator

# Step 5: Now run on REAL HARDWARE
# Change ONE parameter: backend='simulator' → backend='ibm_boston'
# (ibm_boston is IBM's most performant Heron r3 processor)
#
# optimizer_hw = qgo.HybridOptimizer(
#     qubo=qubo,
#     backend='ibm_boston',            # <-- THE ONLY CHANGE (Heron r3)
#     qaoa_layers=2,
#     n_restarts=5,
#     shots=4096,
#     resilience_level=1,            # enable readout mitigation
#     optimization_level=3,          # max transpiler optimization
# )
#
# result_hw = optimizer_hw.solve()
# print(f"\nHardware result ({optimizer_hw.backend_name}):")
# print(f"  Total cost: ${result_hw.total_cost:,.0f}")
# print(f"  Feasible: {result_hw.feasible}")
# print(f"  Schedule: {result_hw.schedule.flatten()}")
# print(f"  Transpiled depth: {result_hw.transpiled_depth}")
# print(f"  Queue wait: {result_hw.queue_time_seconds:.0f}s")
#
# Typical hardware output:
# Hardware result (ibm_boston):
#   Total cost: $4,850           # same optimal! mitigation worked
#   Feasible: True
#   Schedule: [1 1 0]            # correct schedule recovered
#   Transpiled depth: 94         # inflated from 62 by routing
#   Queue wait: 187s             # ~3 min in queue

# Step 6: Compare -- what did hardware noise actually do?
# Let's simulate the comparison
print("\n--- Simulator vs. Hardware Comparison ---")
print(f"{'Metric':<25} | {'Simulator':>12} | {'Hardware':>12}")
print("-" * 55)

# Simulated comparison data (typical for this circuit size on Heron r3)
comparison = {
    'Optimal cost found':     ('$4,850',    '$4,850'),
    'Correct schedule':       ('Yes',       'Yes'),
    'QAOA cost landscape':    ('smooth',    'noisy but usable'),
    'Convergence iterations': ('12',        '18'),
    'Time to result':         ('0.8s',      '4.2 min'),
    'CZ count (abstract)':    ('45',        '45'),
    'CZ count (transpiled)':  ('45',        '72'),
    'Circuit depth':          ('62',        '94'),
}

for metric, (sim_val, hw_val) in comparison.items():
    print(f"{metric:<25} | {sim_val:>12} | {hw_val:>12}")

# Output:
# --- Simulator vs. Hardware Comparison ---
# Metric                    |    Simulator |     Hardware
# -------------------------------------------------------
# Optimal cost found        |       $4,850 |       $4,850
# Correct schedule          |          Yes |          Yes
# QAOA cost landscape       |       smooth | noisy but usable
# Convergence iterations    |           12 |           18
# Time to result            |         0.8s |     4.2 min
# CZ count (abstract)       |           45 |           45
# CZ count (transpiled)     |           45 |           72
# Circuit depth             |           62 |           94
