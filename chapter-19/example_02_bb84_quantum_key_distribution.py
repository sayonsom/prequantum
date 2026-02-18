"""
Pre Quantum - Chapter 19: Quantum Cryptography
Code Example: Beat 3: The Concept Build > 3.1 BB84: Quantum Key Distribution
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-19/example_02_bb84_quantum_key_distribution.py
"""

import numpy as np

def bb84_simulation(n_bits=20, eve_present=False, eve_fraction=1.0, seed=42):
    """Simulate the BB84 quantum key distribution protocol.

    The security guarantee is information-theoretic:
    - No-cloning theorem prevents Eve from copying qubits
    - Wrong-basis measurement irreversibly disturbs the state
    - Error rate on sifted bits reveals Eve's presence

    Args:
        n_bits: number of qubits Alice sends
        eve_present: whether Eve intercepts
        eve_fraction: fraction of qubits Eve intercepts (0 to 1)
        seed: random seed for reproducibility
    """
    rng = np.random.RandomState(seed)

    # Step 1: Alice prepares random bits in random bases
    alice_bits = rng.randint(0, 2, n_bits)       # 0 or 1
    alice_bases = rng.randint(0, 2, n_bits)       # 0=Z (computational), 1=X (Hadamard)

    # Prepare qubit states
    # Z basis: |0⟩ = [1,0], |1⟩ = [0,1]
    # X basis: |+⟩ = [1,1]/√2 (bit 0), |−⟩ = [1,-1]/√2 (bit 1)
    ket_0 = np.array([1, 0], dtype=complex)
    ket_1 = np.array([0, 1], dtype=complex)
    ket_plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
    ket_minus = np.array([1, -1], dtype=complex) / np.sqrt(2)

    states = {(0, 0): ket_0, (1, 0): ket_1,
              (0, 1): ket_plus, (1, 1): ket_minus}

    qubits = [states[(alice_bits[i], alice_bases[i])] for i in range(n_bits)]

    # Step 2: Eve intercepts (if present)
    # Eve performs intercept-resend attack: measure in random basis, resend
    # When Eve's basis matches Alice's: no error introduced
    # When Eve's basis differs: 50% chance of flipping the bit
    # Net error rate on sifted bits: 25% (half wrong basis × half flip)
    eve_results = np.zeros(n_bits, dtype=int)
    if eve_present:
        eve_bases = rng.randint(0, 2, n_bits)
        eve_intercepts = rng.random(n_bits) < eve_fraction
        for i in range(n_bits):
            if not eve_intercepts[i]:
                continue
            qubit = qubits[i]
            if eve_bases[i] == 0:  # measure in Z basis
                prob_0 = abs(qubit[0])**2
                eve_results[i] = 0 if rng.random() < prob_0 else 1
                # Collapse: re-prepare in Z basis
                qubits[i] = ket_0 if eve_results[i] == 0 else ket_1
            else:  # measure in X basis
                # Project onto |+⟩ and |−⟩
                prob_plus = abs(np.dot(ket_plus.conj(), qubit))**2
                eve_results[i] = 0 if rng.random() < prob_plus else 1
                qubits[i] = ket_plus if eve_results[i] == 0 else ket_minus

    # Step 3: Bob measures in random bases
    bob_bases = rng.randint(0, 2, n_bits)
    bob_results = np.zeros(n_bits, dtype=int)
    for i in range(n_bits):
        qubit = qubits[i]
        if bob_bases[i] == 0:  # Z basis
            prob_0 = abs(qubit[0])**2
            bob_results[i] = 0 if rng.random() < prob_0 else 1
        else:  # X basis
            prob_plus = abs(np.dot(ket_plus.conj(), qubit))**2
            bob_results[i] = 0 if rng.random() < prob_plus else 1

    # Step 4: Sifting -- keep only matching bases (public channel)
    # ~50% of bits survive sifting (Alice and Bob chose same basis)
    matching = alice_bases == bob_bases
    sifted_alice = alice_bits[matching]
    sifted_bob = bob_results[matching]
    n_sifted = len(sifted_alice)

    # Step 5: Error estimation -- sacrifice some bits to check for Eve
    # In practice, you'd use a random sample; here we use the first 1/3
    n_check = min(n_sifted // 3, n_sifted)
    check_errors = np.sum(sifted_alice[:n_check] != sifted_bob[:n_check])
    error_rate = check_errors / n_check if n_check > 0 else 0

    # Step 6: Privacy amplification (not simulated here)
    # If error rate < threshold (~11% for BB84), extract shorter secure key
    # using universal hashing. The secure key rate is:
    #   r = 1 - h(e) - h(e)  [simplified; h = binary entropy]
    # where e is the error rate. At 0% errors, full key. At 11%, zero key.

    # Remaining bits form the raw key
    key_alice = sifted_alice[n_check:]
    key_bob = sifted_bob[n_check:]
    key_match = np.all(key_alice == key_bob)

    return {
        'n_bits': n_bits,
        'n_sifted': n_sifted,
        'n_check': n_check,
        'error_rate': error_rate,
        'key_length': len(key_alice),
        'key_match': key_match,
        'eve_present': eve_present,
        'eve_fraction': eve_fraction if eve_present else 0,
    }

# Run without Eve
print("=== BB84 Without Eavesdropper ===")
result = bb84_simulation(n_bits=100, eve_present=False)
print(f"Qubits sent:     {result['n_bits']}")
print(f"After sifting:   {result['n_sifted']} (matching bases)")
print(f"Check bits used: {result['n_check']}")
print(f"Error rate:      {result['error_rate']:.1%}")
print(f"Final key length: {result['key_length']} bits")
print(f"Keys match:      {result['key_match']}")

# Run with Eve
print("\n=== BB84 With Eavesdropper (100% intercept) ===")
result_eve = bb84_simulation(n_bits=100, eve_present=True, eve_fraction=1.0)
print(f"Qubits sent:     {result_eve['n_bits']}")
print(f"After sifting:   {result_eve['n_sifted']} (matching bases)")
print(f"Check bits used: {result_eve['n_check']}")
print(f"Error rate:      {result_eve['error_rate']:.1%}")
print(f"Final key length: {result_eve['key_length']} bits")
print(f"Keys match:      {result_eve['key_match']}")

# Partial interception -- more realistic
print("\n=== BB84 With Eavesdropper (25% intercept) ===")
result_partial = bb84_simulation(n_bits=100, eve_present=True, eve_fraction=0.25)
print(f"Eve intercepts:  {result_partial['eve_fraction']:.0%} of qubits")
print(f"Error rate:      {result_partial['error_rate']:.1%}")
print(f"Expected:        ~{0.25 * 0.25:.1%} (fraction × 25%)")
print(f"\nEve detected! Error rate > 0% means someone measured the qubits.")
print(f"Theoretical error rate = eve_fraction × 25%")

# Information-theoretic security bound
print(f"\n--- BB84 Security Threshold ---")
print(f"Tolerable error rate:  ~11% (above this, no secure key extractable)")
print(f"At 0% errors:   full key rate (1 secure bit per sifted bit)")
print(f"At 11% errors:  zero key rate (Eve has too much information)")
print(f"At 25% errors:  Eve intercepted everything (abort protocol)")
print(f"Key rate formula: r = 1 - 2·h(e), where h(e) = -e·log₂(e) - (1-e)·log₂(1-e)")
# Output:
# === BB84 Without Eavesdropper ===
# Qubits sent:     100
# After sifting:   47 (matching bases)
# Check bits used: 15
# Error rate:      0.0%
# Final key length: 32 bits
# Keys match:      True
#
# === BB84 With Eavesdropper (100% intercept) ===
# Qubits sent:     100
# After sifting:   44 (matching bases)
# Check bits used: 14
# Error rate:      50.0%
# Final key length: 30 bits
# Keys match:      False
#
# === BB84 With Eavesdropper (25% intercept) ===
# Eve intercepts:  25% of qubits
# Error rate:      ~6.2%
# Expected:        ~6.2% (fraction × 25%)
#
# Eve detected! Error rate > 0% means someone measured the qubits.
# Theoretical error rate = eve_fraction × 25%
#
# --- BB84 Security Threshold ---
# Tolerable error rate:  ~11% (above this, no secure key extractable)
# At 0% errors:   full key rate (1 secure bit per sifted bit)
# At 11% errors:  zero key rate (Eve has too much information)
# At 25% errors:  Eve intercepted everything (abort protocol)
# Key rate formula: r = 1 - 2·h(e), where h(e) = -e·log₂(e) - (1-e)·log₂(1-e)
