"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.9 From Textbook to Grid: Running QuantumGridOS on Real Hardware
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_18_from_textbook_to_grid_running_quantumgri.py
"""

# qgo's hybrid decomposition for large problems
#
# optimizer_large = qgo.HybridOptimizer(
#     qubo=qubo_large,              # 600-variable QUBO
#     backend='ibm_boston',          # Heron r3
#     qaoa_layers=2,
#     decomposition='time_block',   # split 24 periods into 6 blocks of 4
#     n_restarts=10,
#     resilience_level=1,
# )
#
# result_large = optimizer_large.solve()
# print(f"Decomposition: {result_large.n_subproblems} sub-problems")
# print(f"Each sub-problem: {result_large.sub_qubit_count} qubits")
# print(f"Total hardware calls: {result_large.n_hardware_calls}")
# print(f"Classical stitching time: {result_large.stitch_time:.1f}s")
#
# Typical output:
# Decomposition: 6 sub-problems
# Each sub-problem: 100 qubits
# Total hardware calls: 60 (6 sub-problems × 10 restarts)
# Classical stitching time: 2.3s
