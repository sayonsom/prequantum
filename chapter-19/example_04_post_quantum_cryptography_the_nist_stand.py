"""
Pre Quantum - Chapter 19: Quantum Cryptography
Code Example: Beat 3: The Concept Build > 3.3 Post-Quantum Cryptography: The NIST Standards
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-19/example_04_post_quantum_cryptography_the_nist_stand.py
"""

import numpy as np

def lwe_keygen(n=8, q=97, seed=42):
    """Generate LWE public/private key pair.

    The Learning With Errors problem:
    Given A (random matrix) and b = A·s + e (mod q),
    find secret vector s.

    Without noise e: trivial (solve linear system).
    With noise e: reduces to Shortest Vector Problem (SVP)
    in a lattice of dimension n. No known quantum speedup
    beyond polynomial for SVP.

    n: lattice dimension, q: modulus (prime)
    Real ML-KEM uses n=256 (per module), q=3329, k=2,3,4 modules.
    """
    rng = np.random.RandomState(seed)

    # Private key: small random vector (coefficients in {-1, 0, 1})
    # In ML-KEM, coefficients are sampled from centered binomial distribution
    s = rng.randint(-1, 2, size=n)

    # Public key: (A, b = A·s + e mod q)
    m = n + 4  # number of equations (slightly more than n for overdetermined system)
    A = rng.randint(0, q, size=(m, n))
    e = rng.randint(-1, 2, size=m)  # small error vector
    b = (A @ s + e) % q

    return {'public': (A, b, q), 'private': s}

def lwe_encrypt(public_key, bit):
    """Encrypt a single bit using LWE.

    The encryption "hides" the bit in the noise of a random
    linear combination of public-key rows. The q//2 offset
    for bit=1 is large enough to survive the accumulated noise
    but small enough that an attacker can't distinguish it
    without knowing s.
    """
    A, b, q = public_key
    m = A.shape[0]

    # Pick random subset of rows (simulates random linear combination)
    rng = np.random.RandomState(bit * 17 + 7)  # deterministic for demo
    subset = rng.choice(m, size=m//2, replace=False)

    # Ciphertext: sum selected rows of A and corresponding b values
    u = np.sum(A[subset], axis=0) % q
    v = (np.sum(b[subset]) + bit * (q // 2)) % q

    return u, v

def lwe_decrypt(private_key, ciphertext, q):
    """Decrypt using private key.

    Computes v - u·s mod q. The noise terms cancel (approximately),
    leaving either ~0 (bit was 0) or ~q/2 (bit was 1).

    Why this works:
    v = Σ b_i + bit·(q/2)  = Σ (a_i·s + e_i) + bit·(q/2)
    u = Σ a_i
    v - u·s = Σ e_i + bit·(q/2)  mod q
    Since |Σ e_i| << q/4, we can distinguish 0 from q/2.
    """
    u, v = ciphertext
    s = private_key

    # Compute v - u·s mod q
    result = (v - u @ s) % q

    # If close to 0: bit was 0. If close to q/2: bit was 1.
    if result < q // 4 or result > 3 * q // 4:
        return 0
    else:
        return 1

# Demo: encrypt and decrypt
keys = lwe_keygen(n=8, q=97)
print("=== LWE Encryption (Lattice-Based) ===")
print(f"Lattice dimension: n=8, modulus: q=97")
print(f"Private key s: {keys['private']}")
print(f"Public key A shape: {keys['public'][0].shape}")

# Encrypt both bits
for bit in [0, 1]:
    ct = lwe_encrypt(keys['public'], bit)
    decrypted = lwe_decrypt(keys['private'], ct, 97)
    print(f"\nEncrypt bit={bit}:")
    print(f"  Ciphertext u (dim {len(ct[0])}): {ct[0]}")
    print(f"  Ciphertext v: {ct[1]}")
    print(f"  Decrypted: {decrypted}  {'CORRECT' if decrypted == bit else 'ERROR'}")

# Why is this quantum-resistant? -- deeper explanation
print("\n--- Why Lattice Crypto Resists Quantum Attack ---")
print("RSA hardness:     Factor N = p × q")
print("  → Shor's finds period of a^x mod N via QFT")
print("  → Period-finding has hidden subgroup structure → exponential speedup")
print("  → BROKEN")
print("\nLWE hardness:     Given A and b = A·s + e (mod q), find s")
print("  → Noise vector e hides s in the linear system")
print("  → Reduces to Shortest Vector Problem (SVP) in lattice")
print("  → SVP has NO hidden subgroup structure")
print("  → Best quantum attacks: 2^(c·n) — same exponent as classical")
print("  → Only known quantum speedup: polynomial (not exponential)")
print("  → Security scales with lattice dimension n")

# Real ML-KEM parameters vs our toy example
print("\n--- ML-KEM (FIPS 203) vs Our Toy Example ---")
params = [
    ("Our demo",     "n=8",     "q=97",     "~8B pub",     "toy only"),
    ("ML-KEM-512",   "k=2, n=256", "q=3329", "800B pub",   "NIST Level 1 (≈AES-128)"),
    ("ML-KEM-768",   "k=3, n=256", "q=3329", "1,184B pub", "NIST Level 3 (≈AES-192) — RECOMMENDED"),
    ("ML-KEM-1024",  "k=4, n=256", "q=3329", "1,568B pub", "NIST Level 5 (≈AES-256)"),
]
print(f"{'Scheme':<16} {'Dimension':<14} {'Modulus':<10} {'Key Size':<14} {'Security'}")
print("-" * 80)
for scheme, dim, mod, size, sec in params:
    print(f"{scheme:<16} {dim:<14} {mod:<10} {size:<14} {sec}")
# Output:
# === LWE Encryption (Lattice-Based) ===
# Lattice dimension: n=8, modulus: q=97
# Private key s: [ 1 -1  1  1 -1 -1  1  0]
# Public key A shape: (12, 8)
#
# Encrypt bit=0:
#   Ciphertext u (dim 8): [70 18  3 94 20 50 52 25]
#   Ciphertext v: 34
#   Decrypted: 0  CORRECT
#
# Encrypt bit=1:
#   Ciphertext u (dim 8): [23 18 15 11 42  3 85 16]
#   Ciphertext v: 22
#   Decrypted: 1  CORRECT
#
# --- Why Lattice Crypto Resists Quantum Attack ---
# RSA hardness:     Factor N = p × q
#   → Shor's finds period of a^x mod N via QFT
#   → Period-finding has hidden subgroup structure → exponential speedup
#   → BROKEN
#
# LWE hardness:     Given A and b = A·s + e (mod q), find s
#   → Noise vector e hides s in the linear system
#   → Reduces to Shortest Vector Problem (SVP) in lattice
#   → SVP has NO hidden subgroup structure
#   → Best quantum attacks: 2^(c·n) — same exponent as classical
#   → Only known quantum speedup: polynomial (not exponential)
#   → Security scales with lattice dimension n
#
# --- ML-KEM (FIPS 203) vs Our Toy Example ---
# Scheme           Dimension      Modulus    Key Size       Security
# --------------------------------------------------------------------------------
# Our demo         n=8            q=97       ~8B pub        toy only
# ML-KEM-512       k=2, n=256     q=3329     800B pub       NIST Level 1 (≈AES-128)
# ML-KEM-768       k=3, n=256     q=3329     1,184B pub     NIST Level 3 (≈AES-192) — RECOMMENDED
# ML-KEM-1024      k=4, n=256     q=3329     1,568B pub     NIST Level 5 (≈AES-256)
