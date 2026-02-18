"""
Pre Quantum - Chapter 19: Quantum Cryptography
Code Example: Beat 3: The Concept Build > 3.2 The Shor Threat: What's Actually at Risk
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-19/example_03_the_shor_threat_whats_actually_at_risk.py
"""

import numpy as np

# What Shor's algorithm breaks and the quantum resources needed
# Updated with Gidney (2025) and Pinnacle (2026) estimates
crypto_targets = [
    ("RSA-1024",     "Factoring",       "~1,000 logical",     "Deprecated",    "Already weak classically"),
    ("RSA-2048",     "Factoring",       "~1,730 logical",     "Standard",      "< 1M physical (Gidney 2025)"),
    ("RSA-4096",     "Factoring",       "~3,500 logical",     "High security", "~2M physical (estimated)"),
    ("ECC P-256",    "Discrete log",    "~2,300 logical",     "Standard",      "Similar to RSA-2048"),
    ("ECC P-384",    "Discrete log",    "~3,500 logical",     "High security", "Similar to RSA-4096"),
    ("DH-2048",      "Discrete log",    "~1,730 logical",     "Key exchange",  "Same as RSA-2048"),
    ("AES-128",      "Grover search",   "Reduces to 2^64",    "Symmetric",     "Weakened, not broken"),
    ("AES-256",      "Grover search",   "Reduces to 2^128",   "Symmetric",     "Still secure"),
    ("SHA-256",      "Grover search",   "Reduces to 2^128",   "Hash",          "Still secure"),
]

print(f"{'Algorithm':<14} {'Attack':>14} {'Qubits Needed':>18} {'Current Use':>16} {'Quantum Threat':>26}")
print("-" * 96)
for alg, attack, qubits, use, threat in crypto_targets:
    print(f"{alg:<14} {attack:>14} {qubits:>18} {use:>16} {threat:>26}")

# Key insight: asymmetric crypto is broken, symmetric crypto is only weakened
print("\n--- The Asymmetry ---")
print("Shor's algorithm:  BREAKS public-key crypto (RSA, ECC, DH)")
print("                   These use number-theoretic hardness assumptions")
print("                   that Shor's period-finding destroys.")
print("\nGrover's algorithm: WEAKENS symmetric crypto (AES, SHA)")
print("                   Gives quadratic speedup: 2^n → 2^(n/2)")
print("                   Fix: double the key size (AES-128 → AES-256)")

# Updated timeline with real hardware milestones
print("\n--- Hardware Timeline (Updated Feb 2026) ---")
milestones = [
    (2024, "Google Willow: 105 qubits",     "Below-threshold error correction demonstrated"),
    (2025, "IBM Nighthawk: 120 qubits",     "218 tunable couplers; ~1K gates per qubit"),
    (2026, "IBM Kookaburra: 4,158 qubits",  "3-chip system; target ~7,500 gates"),
    (2028, "IBM Starling: ~10,000 phys.",    "~200 logical qubits; 100M gate circuits"),
    (2029, "IBM fault-tolerant target",      "Goal: practical fault tolerance"),
    (2030, "Multiple vendors: ~1M phys.",    "RSA-2048 at risk if error rates drop"),
    (2033, "IBM Blue Jay: ~100K phys.",      "~2,000 logical qubits; billion-gate programs"),
]
print(f"{'Year':>6}  {'Hardware':>35}  {'Implication'}")
print("-" * 95)
for year, hw, imp in milestones:
    print(f"{year:>6}  {hw:>35}  {imp}")

print(f"\n--- Logical Qubit Estimates for RSA-2048 (Historical) ---")
logical_estimates = [
    (2003, "Beauregard",           "4,099 (2n+3)",        "Minimum qubits, very deep circuit"),
    (2014, "Pavlidis & Gizopoulos","~18,434 (9n+2)",      "Reduced circuit depth"),
    (2019, "Gidney & Ekerå",       "~6,150 (~3n)",        "Optimized time-space tradeoff"),
    (2024, "Chevignard et al.",     "~1,730 (~0.85n)",     "Fewest logical, high gate count"),
]
print(f"{'Year':>6}  {'Authors':<24} {'Logical Qubits':<24} {'Notes'}")
print("-" * 85)
for year, auth, qubits, notes in logical_estimates:
    print(f"{year:>6}  {auth:<24} {qubits:<24} {notes}")
# Output:
# Algorithm            Attack      Qubits Needed      Current Use               Quantum Threat
# ------------------------------------------------------------------------------------------------
# RSA-1024          Factoring      ~1,000 logical       Deprecated      Already weak classically
# RSA-2048          Factoring      ~1,730 logical         Standard  < 1M physical (Gidney 2025)
# RSA-4096          Factoring      ~3,500 logical    High security     ~2M physical (estimated)
# ECC P-256      Discrete log      ~2,300 logical         Standard       Similar to RSA-2048
# ECC P-384      Discrete log      ~3,500 logical    High security       Similar to RSA-4096
# DH-2048        Discrete log      ~1,730 logical     Key exchange         Same as RSA-2048
# AES-128       Grover search   Reduces to 2^64        Symmetric      Weakened, not broken
# AES-256       Grover search  Reduces to 2^128        Symmetric              Still secure
# SHA-256       Grover search  Reduces to 2^128             Hash              Still secure
#
# --- The Asymmetry ---
# Shor's algorithm:  BREAKS public-key crypto (RSA, ECC, DH)
#                    These use number-theoretic hardness assumptions
#                    that Shor's period-finding destroys.
#
# Grover's algorithm: WEAKENS symmetric crypto (AES, SHA)
#                    Gives quadratic speedup: 2^n → 2^(n/2)
#                    Fix: double the key size (AES-128 → AES-256)
#
# --- Hardware Timeline (Updated Feb 2026) ---
#   Year                             Hardware  Implication
# -----------------------------------------------------------------------------------------------
#   2024         Google Willow: 105 qubits  Below-threshold error correction demonstrated
#   2025        IBM Nighthawk: 120 qubits  218 tunable couplers; ~1K gates per qubit
#   2026     IBM Kookaburra: 4,158 qubits  3-chip system; target ~7,500 gates
#   2028     IBM Starling: ~10,000 phys.  ~200 logical qubits; 100M gate circuits
#   2029     IBM fault-tolerant target  Goal: practical fault tolerance
#   2030     Multiple vendors: ~1M phys.  RSA-2048 at risk if error rates drop
#   2033      IBM Blue Jay: ~100K phys.  ~2,000 logical qubits; billion-gate programs
#
# --- Logical Qubit Estimates for RSA-2048 (Historical) ---
#   Year  Authors                  Logical Qubits           Notes
# -------------------------------------------------------------------------------------
#   2003  Beauregard               4,099 (2n+3)             Minimum qubits, very deep circuit
#   2014  Pavlidis & Gizopoulos    ~18,434 (9n+2)           Reduced circuit depth
#   2019  Gidney & Ekerå           ~6,150 (~3n)             Optimized time-space tradeoff
#   2024  Chevignard et al.        ~1,730 (~0.85n)          Fewest logical, high gate count
