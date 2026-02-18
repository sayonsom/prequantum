"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.9 From Textbook to Grid: Running QuantumGridOS on Real Hardware
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_15_from_textbook_to_grid_running_quantumgri.py
"""

import quantumgridos as qgo
import numpy as np

# Step 1: Build a small power network
# 5 buses, 3 generators, sized for NISQ hardware
network = qgo.PowerNetwork.from_ieee_case(5)
print(f"Network: {network.n_bus} buses, {network.n_gen} generators")
print(f"Total capacity: {network.total_gen_capacity:.0f} MW")
print(f"Total demand: {network.total_load:.0f} MW")
# Output:
# Network: 5 buses, 3 generators
# Total capacity: 310 MW
# Total demand: 195 MW

# Step 2: Formulate as QUBO (same API as Chapter 18)
uc = qgo.UnitCommitment(
    network=network,
    periods=1,                      # single time period for hardware demo
    reserve_margin=0.10,
)
qubo = uc.to_qubo(penalty_weight='auto')
print(f"\nQUBO: {qubo.n_variables} variables, {qubo.n_nonzero} non-zero terms")
print(f"Qubits needed: {qubo.n_variables}")
# Output:
# QUBO: 10 variables, 38 non-zero terms
# Qubits needed: 10

# Step 3: Inspect the QAOA circuit BEFORE sending to hardware
# This is the critical step most tutorials skip
circuit_info = qgo.HybridOptimizer.preview_circuit(
    qubo=qubo,
    qaoa_layers=2,
    backend='simulator',
)
print(f"\nQAOA circuit preview:")
print(f"  Qubits: {circuit_info.n_qubits}")
print(f"  CZ count: {circuit_info.n_cz}")
print(f"  Circuit depth: {circuit_info.depth}")
print(f"  Parameters: {circuit_info.n_params}")
# Output:
# QAOA circuit preview:
#   Qubits: 10
#   CZ count: 45
#   Circuit depth: 62
#   Parameters: 4
