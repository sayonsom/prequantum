"""
Pre Quantum - Chapter 14: The Math Behind the Magic
Code Example: Beat 3: The Concept Build > 3.4 Quantum Channels: How Noise Acts on Density Matrices
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-14/example_10_quantum_channels_how_noise_acts_on_densi.py
"""

import numpy as np

def apply_channel(rho, kraus_ops):
    """Apply a quantum channel defined by Kraus operators."""
    result = np.zeros_like(rho)
    for K in kraus_ops:
        result += K @ rho @ K.conj().T
    return result

def verify_kraus(kraus_ops):
    """Check completeness: Σ K†K = I"""
    dim = kraus_ops[0].shape[0]
    total = sum(K.conj().T @ K for K in kraus_ops)
    return np.allclose(total, np.eye(dim))

# --- Bit-flip channel (probability p of flipping) ---
def bit_flip_channel(p):
    K0 = np.sqrt(1 - p) * np.eye(2, dtype=complex)
    K1 = np.sqrt(p) * np.array([[0, 1], [1, 0]], dtype=complex)  # sqrt(p) * X
    return [K0, K1]

# --- Phase-flip channel (probability p of phase flip) ---
def phase_flip_channel(p):
    K0 = np.sqrt(1 - p) * np.eye(2, dtype=complex)
    K1 = np.sqrt(p) * np.array([[1, 0], [0, -1]], dtype=complex)  # sqrt(p) * Z
    return [K0, K1]

# --- Depolarizing channel (probability p of replacing with I/2) ---
def depolarizing_channel(p):
    K0 = np.sqrt(1 - 3*p/4) * np.eye(2, dtype=complex)
    K1 = np.sqrt(p/4) * np.array([[0, 1], [1, 0]], dtype=complex)    # X
    K2 = np.sqrt(p/4) * np.array([[0, -1j], [1j, 0]], dtype=complex) # Y
    K3 = np.sqrt(p/4) * np.array([[1, 0], [0, -1]], dtype=complex)   # Z
    return [K0, K1, K2, K3]

# --- Amplitude damping (T₁ decay, probability γ of |1⟩ → |0⟩) ---
def amplitude_damping_channel(gamma):
    K0 = np.array([[1, 0], [0, np.sqrt(1 - gamma)]], dtype=complex)
    K1 = np.array([[0, np.sqrt(gamma)], [0, 0]], dtype=complex)
    return [K0, K1]

# Verify completeness for all channels
for name, channel_fn, param in [
    ("Bit-flip",       bit_flip_channel,       0.1),
    ("Phase-flip",     phase_flip_channel,     0.1),
    ("Depolarizing",   depolarizing_channel,   0.1),
    ("Amp. damping",   amplitude_damping_channel, 0.1),
]:
    kraus = channel_fn(param)
    print(f"{name:16s} | Completeness: {verify_kraus(kraus)}")

# Apply depolarizing noise to |+⟩ at different strengths
plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
rho_plus = np.outer(plus, plus.conj())

print(f"\n{'p':>5} | {'Purity':>8} | {'Entropy':>8} | {'Off-diag |ρ₀₁|':>15}")
print("-" * 48)
for p in [0.0, 0.2, 0.5, 0.8, 1.0]:
    kraus = depolarizing_channel(p)
    rho_noisy = apply_channel(rho_plus, kraus)
    purity = np.trace(rho_noisy @ rho_noisy).real
    evals = np.linalg.eigvalsh(rho_noisy)
    evals = evals[evals > 1e-12]
    entropy = -np.sum(evals * np.log2(evals))
    offdiag = abs(rho_noisy[0, 1])
    print(f"{p:5.1f} | {purity:8.4f} | {entropy:8.4f} | {offdiag:15.4f}")
# At p=0: pure state, zero entropy, full coherence
# At p=1: maximally mixed, 1 bit of entropy, zero coherence
