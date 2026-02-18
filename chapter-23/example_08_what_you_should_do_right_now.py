"""
Pre Quantum - Chapter 23: Hype vs Reality
Code Example: Beat 3: The Concept Build > 3.7 What You Should Do Right Now
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-23/example_08_what_you_should_do_right_now.py
"""

# What you built across 23 chapters -- a skills inventory
skills_inventory = {
    "Part I: Foundations": [
        "Qubit states as numpy arrays (Ch. 2)",
        "Entanglement and Bell states (Ch. 3)",
        "Linear algebra for quantum computing (Ch. 4)",
        "Quantum gates as matrix transformations (Ch. 5)",
    ],
    "Part II: Toolkit": [
        "Circuit model and simulators (Ch. 6)",
        "Noise models and decoherence (Ch. 7)",
        "Quantum information protocols (Ch. 8)",
        "Vector spaces and operator formalism (Ch. 9)",
    ],
    "Part III: Algorithms": [
        "Oracle algorithms: Deutsch-Jozsa, BV (Ch. 10)",
        "Grover's search and amplitude amplification (Ch. 11)",
        "QFT and Shor's algorithm (Ch. 12)",
        "Variational algorithms: VQE, QAOA (Ch. 13)",
        "Eigenvalues, Hamiltonians, density matrices (Ch. 14)",
    ],
    "Part IV: Applications": [
        "Quantum machine learning (Ch. 15)",
        "Quantum optimization and QUBO (Ch. 16)",
        "Quantum simulation and trotterization (Ch. 17)",
        "Energy grid optimization with QuantumGridOS (Ch. 18)",
        "Quantum cryptography and PQC (Ch. 19)",
    ],
    "Part V: Becoming a Quantum Developer": [
        "Qiskit, Cirq, PennyLane -- SDK fluency (Ch. 20)",
        "Quantum-classical microservices (Ch. 21)",
        "Quantum error correction (Ch. 22)",
        "Evaluating quantum advantage claims (Ch. 23)",
    ],
}

total_skills = 0
for part, skills in skills_inventory.items():
    print(f"\n{part}:")
    for skill in skills:
        print(f"  - {skill}")
        total_skills += 1

print(f"\n{'='*50}")
print(f"Total: {total_skills} core competencies across 23 chapters")
print(f"You are now a quantum-literate developer.")
print(f"That puts you in the top ~0.1% of software engineers worldwide.")
