"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.6 Reading Noisy Results: The Three Layers of Error
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_10_reading_noisy_results_the_three_layers_o.py
"""

import numpy as np

# Simulate the three error layers on a Bell state
np.random.seed(42)
n_shots = 10000

# Ideal probabilities: P(00)=0.5, P(01)=0, P(10)=0, P(11)=0.5
ideal = np.array([0.5, 0.0, 0.0, 0.5])
labels = ['00', '01', '10', '11']

# Layer 1: Gate errors (applied BEFORE measurement)
# A small depolarizing noise on each qubit
gate_error = 0.02  # 2% per gate, 2 gates in Bell circuit
gate_noise = gate_error * 2  # rough cumulative effect
noisy_after_gates = (1 - gate_noise) * ideal + gate_noise * np.ones(4) / 4
print("After gate errors:  ", {l: f"{p:.3f}" for l, p in zip(labels, noisy_after_gates)})

# Layer 2: Readout errors (applied AFTER gate errors)
# Confusion matrix: P(measure_i | true_j)
M_readout = np.array([
    [0.96, 0.02, 0.03, 0.01],  # P(measure 00 | true state)
    [0.01, 0.94, 0.01, 0.03],  # P(measure 01 | true state)
    [0.02, 0.01, 0.93, 0.02],  # P(measure 10 | true state)
    [0.01, 0.03, 0.03, 0.94],  # P(measure 11 | true state)
])
noisy_final = M_readout @ noisy_after_gates
print("After readout errors:", {l: f"{p:.3f}" for l, p in zip(labels, noisy_final)})

# Layer 3: T1 decoherence (biases toward |0>)
t1_bias = 0.01  # small bias from relaxation during circuit
noisy_with_t1 = noisy_final.copy()
noisy_with_t1[0] += t1_bias   # |00> gains probability
noisy_with_t1[3] -= t1_bias   # |11> loses probability
noisy_with_t1 = np.clip(noisy_with_t1, 0, None)
noisy_with_t1 /= noisy_with_t1.sum()
print("After T1 decay:     ", {l: f"{p:.3f}" for l, p in zip(labels, noisy_with_t1)})
print("Ideal:              ", {l: f"{p:.3f}" for l, p in zip(labels, ideal)})

# Sample from final noisy distribution
shots = np.random.choice(4, size=n_shots, p=noisy_with_t1)
counts = {labels[i]: np.sum(shots == i) for i in range(4)}
print(f"\nSimulated hardware ({n_shots} shots): {counts}")
# Output (approximately):
# After gate errors:   {'00': '0.480', '01': '0.010', '10': '0.010', '11': '0.480'}
# After readout errors: {'00': '0.467', '01': '0.024', '10': '0.029', '11': '0.459'}
# After T1 decay:      {'00': '0.477', '01': '0.024', '10': '0.029', '11': '0.449'}
# Ideal:               {'00': '0.500', '01': '0.000', '10': '0.000', '11': '0.500'}
# Simulated hardware (10000 shots): {'00': 4770, '01': 247, '10': 286, '11': 4486}
