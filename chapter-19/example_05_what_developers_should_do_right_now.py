"""
Pre Quantum - Chapter 19: Quantum Cryptography
Code Example: Beat 3: The Concept Build > 3.4 What Developers Should Do Right Now
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-19/example_05_what_developers_should_do_right_now.py
"""

# Migration checklist for developers -- updated February 2026
# This is a reference, not runnable code

migration_steps = [
    {
        'priority': 'URGENT',
        'action': 'Inventory your cryptographic dependencies',
        'details': [
            'Search codebase for: RSA, ECDSA, ECDH, DH, DSA',
            'Check TLS configurations (what key exchange? what cipher suites?)',
            'Identify certificate authorities and signing algorithms',
            'Map data sensitivity × retention period (the "harvest now" window)',
            'Classify: data that must stay secret for 10+ years is at immediate risk',
        ],
        'tools': 'grep -r "RSA\\|ECDSA\\|ECDH" --include="*.py" .',
    },
    {
        'priority': 'HIGH',
        'action': 'Enable hybrid key exchange in TLS',
        'details': [
            'Use X25519MLKEM768 (hybrid: X25519 + ML-KEM-768)',
            'Chrome & Firefox ship this by default since 2024-25',
            'Apple iOS/macOS 26 advertises X25519MLKEM768 in TLS 1.3 ClientHello',
            'Signal uses PQXDH (X25519 + Kyber) for all new sessions',
            'Server-side: OpenSSL 3.5+, BoringSSL, AWS-LC support hybrid',
            'Note: PQ handshake is ~1,216 bytes vs 32 bytes (plan for bandwidth)',
        ],
        'tools': 'openssl s_client -groups X25519MLKEM768',
    },
    {
        'priority': 'HIGH',
        'action': 'Upgrade digital signatures for long-lived artifacts',
        'details': [
            'Code signing, firmware updates, legal documents, certificates',
            'Switch to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)',
            'ML-DSA: faster, smaller — use for most applications',
            'SLH-DSA: hash-based, ultra-conservative — use for highest assurance',
            'PQ certificates expected available 2026; not default until later',
        ],
        'tools': 'pip install pqcrypto  # or liboqs-python, or oqs-provider for OpenSSL',
    },
    {
        'priority': 'MEDIUM',
        'action': 'Double symmetric key sizes where cheap',
        'details': [
            'AES-128 → AES-256 (Grover reduces effective security to 2^128)',
            'SHA-256 stays fine for most uses (Grover → 2^128 preimage)',
            'HMAC-SHA-256 already quantum-resistant',
            'For SCADA/IoT (Chapter 18): evaluate AES-256 performance on constrained devices',
        ],
        'tools': 'Update cipher suite preferences in TLS config',
    },
    {
        'priority': 'PLAN NOW',
        'action': 'Design for crypto agility',
        'details': [
            'Abstract crypto behind interfaces (Strategy pattern)',
            'Store algorithm identifiers with encrypted data (algorithm + version tag)',
            'Plan re-encryption procedures for stored data',
            'Test PQ algorithms for performance impact (ML-KEM: ~150μs overhead per handshake)',
            'Watch HQC standardization (~2027) as lattice backup',
            'Prepare for hybrid → PQ-only transition (NSA recommends eventually)',
        ],
        'tools': 'Design pattern, not a specific tool',
    },
]

print("=== Post-Quantum Migration Checklist (Updated Feb 2026) ===\n")
for step in migration_steps:
    print(f"[{step['priority']:>9}] {step['action']}")
    for detail in step['details']:
        print(f"             - {detail}")
    print(f"             Tool: {step['tools']}")
    print()

# Key size comparison -- PQ keys are MUCH larger
print("--- Key & Signature Size Impact ---")
sizes = [
    ("RSA-2048",      "256 B",      "256 B",      "256 B",     "Classical standard"),
    ("ECC P-256",     "32 B",       "64 B",       "64 B",      "Classical standard"),
    ("ML-KEM-768",    "1,184 B",    "2,400 B",    "1,088 B*",  "FIPS 203 (recommended)"),
    ("ML-KEM-1024",   "1,568 B",    "3,168 B",    "1,568 B*",  "FIPS 203 (high security)"),
    ("ML-DSA-65",     "1,952 B",    "4,032 B",    "3,309 B",   "FIPS 204 (recommended)"),
    ("SLH-DSA-128s",  "32 B",       "64 B",       "7,856 B",   "FIPS 205 (hash-based)"),
    ("FN-DSA-512",    "897 B",      "1,281 B",    "666 B",     "FIPS 206 (draft)"),
]
print(f"{'Algorithm':<16} {'Public Key':>12} {'Private Key':>12} {'Sig/CT':>12} {'Standard'}")
print("-" * 72)
for alg, pub, priv, sig, std in sizes:
    print(f"{alg:<16} {pub:>12} {priv:>12} {sig:>12} {std}")
print("\n* For KEM, 'Sig/CT' column shows ciphertext size, not signature")
print("ML-KEM-768 public keys are ~37x larger than ECC P-256. Plan for bandwidth.")
print("But: ML-KEM key generation is ~20,500x faster than RSA-2048.")

# Real-world deployment status
print("\n--- Who's Already Deployed PQ (as of Feb 2026) ---")
deployments = [
    ("Chrome/Chromium",  "X25519MLKEM768 in TLS 1.3", "Default since ~Chrome 131"),
    ("Firefox",          "X25519MLKEM768 in TLS 1.3", "Default since ~Firefox 135"),
    ("Signal",           "PQXDH (X25519 + Kyber)",    "All new sessions since Sep 2023"),
    ("Apple iMessage",   "PQ3 (ECC + ML-KEM)",        "Since iOS 17.4 (Mar 2024)"),
    ("Apple TLS",        "X25519MLKEM768",             "Default in iOS/macOS 26 (2025)"),
    ("AWS KMS",          "ML-KEM hybrid",              "< 0.05% throughput impact"),
    ("Cloudflare",       "ML-KEM hybrid",              "Default for all connections"),
    ("Google Cloud",     "ML-KEM hybrid TLS",          "Internal and external APIs"),
]
print(f"{'Platform':<18} {'Algorithm':>28} {'Status'}")
print("-" * 80)
for platform, algo, status in deployments:
    print(f"{platform:<18} {algo:>28} {status}")
# Output:
# === Post-Quantum Migration Checklist (Updated Feb 2026) ===
#
# [   URGENT] Inventory your cryptographic dependencies
#              - Search codebase for: RSA, ECDSA, ECDH, DH, DSA
#              - Check TLS configurations (what key exchange? what cipher suites?)
#              - Identify certificate authorities and signing algorithms
#              - Map data sensitivity × retention period (the "harvest now" window)
#              - Classify: data that must stay secret for 10+ years is at immediate risk
#              Tool: grep -r "RSA\|ECDSA\|ECDH" --include="*.py" .
#
# [     HIGH] Enable hybrid key exchange in TLS
#              - Use X25519MLKEM768 (hybrid: X25519 + ML-KEM-768)
#              - Chrome & Firefox ship this by default since 2024-25
#              - Apple iOS/macOS 26 advertises X25519MLKEM768 in TLS 1.3 ClientHello
#              - Signal uses PQXDH (X25519 + Kyber) for all new sessions
#              - Server-side: OpenSSL 3.5+, BoringSSL, AWS-LC support hybrid
#              - Note: PQ handshake is ~1,216 bytes vs 32 bytes (plan for bandwidth)
#              Tool: openssl s_client -groups X25519MLKEM768
#
# [     HIGH] Upgrade digital signatures for long-lived artifacts
#              - Code signing, firmware updates, legal documents, certificates
#              - Switch to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205)
#              - ML-DSA: faster, smaller — use for most applications
#              - SLH-DSA: hash-based, ultra-conservative — use for highest assurance
#              - PQ certificates expected available 2026; not default until later
#              Tool: pip install pqcrypto  # or liboqs-python, or oqs-provider for OpenSSL
#
# [   MEDIUM] Double symmetric key sizes where cheap
#              - AES-128 → AES-256 (Grover reduces effective security to 2^128)
#              - SHA-256 stays fine for most uses (Grover → 2^128 preimage)
#              - HMAC-SHA-256 already quantum-resistant
#              - For SCADA/IoT (Chapter 18): evaluate AES-256 performance on constrained devices
#              Tool: Update cipher suite preferences in TLS config
#
# [PLAN NOW] Design for crypto agility
#              - Abstract crypto behind interfaces (Strategy pattern)
#              - Store algorithm identifiers with encrypted data (algorithm + version tag)
#              - Plan re-encryption procedures for stored data
#              - Test PQ algorithms for performance impact (ML-KEM: ~150μs overhead per handshake)
#              - Watch HQC standardization (~2027) as lattice backup
#              - Prepare for hybrid → PQ-only transition (NSA recommends eventually)
#              Tool: Design pattern, not a specific tool
#
# --- Key & Signature Size Impact ---
# Algorithm        Public Key  Private Key       Sig/CT Standard
# ------------------------------------------------------------------------
# RSA-2048            256 B        256 B        256 B Classical standard
# ECC P-256            32 B         64 B         64 B Classical standard
# ML-KEM-768        1,184 B      2,400 B      1,088 B* FIPS 203 (recommended)
# ML-KEM-1024       1,568 B      3,168 B      1,568 B* FIPS 203 (high security)
# ML-DSA-65         1,952 B      4,032 B      3,309 B FIPS 204 (recommended)
# SLH-DSA-128s         32 B         64 B      7,856 B FIPS 205 (hash-based)
# FN-DSA-512          897 B      1,281 B        666 B FIPS 206 (draft)
#
# * For KEM, 'Sig/CT' column shows ciphertext size, not signature
# ML-KEM-768 public keys are ~37x larger than ECC P-256. Plan for bandwidth.
# But: ML-KEM key generation is ~20,500x faster than RSA-2048.
#
# --- Who's Already Deployed PQ (as of Feb 2026) ---
# Platform           Algorithm                            Status
# --------------------------------------------------------------------------------
# Chrome/Chromium    X25519MLKEM768 in TLS 1.3            Default since ~Chrome 131
# Firefox            X25519MLKEM768 in TLS 1.3            Default since ~Firefox 135
# Signal             PQXDH (X25519 + Kyber)               All new sessions since Sep 2023
# Apple iMessage     PQ3 (ECC + ML-KEM)                   Since iOS 17.4 (Mar 2024)
# Apple TLS          X25519MLKEM768                        Default in iOS/macOS 26 (2025)
# AWS KMS            ML-KEM hybrid                         < 0.05% throughput impact
# Cloudflare         ML-KEM hybrid                         Default for all connections
# Google Cloud       ML-KEM hybrid TLS                     Internal and external APIs
