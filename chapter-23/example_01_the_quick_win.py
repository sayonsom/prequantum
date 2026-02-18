"""
Pre Quantum - Chapter 23: Hype vs Reality
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-23/example_01_the_quick_win.py
"""

# quantum_vs_classical_benchmark.py
# pip install qiskit qiskit-aer networkx numpy
import time
import numpy as np
import networkx as nx
from itertools import product

# --- Problem setup: MaxCut on a random graph ---
np.random.seed(42)
n_nodes = 10
G = nx.random_regular_graph(3, n_nodes, seed=42)
edges = list(G.edges())
print(f"MaxCut problem: {n_nodes} nodes, {len(edges)} edges")

# --- Solver 1: Brute Force (classical, exact) ---
t0 = time.time()
best_cut = 0
best_assignment = None
for bits in product([0, 1], repeat=n_nodes):
    cut = sum(1 for i, j in edges if bits[i] != bits[j])
    if cut > best_cut:
        best_cut = cut
        best_assignment = bits
t_brute = time.time() - t0
print(f"\nBrute force:  cut={best_cut}, time={t_brute:.4f}s "
      f"(checked {2**n_nodes:,} assignments)")

# --- Solver 2: Greedy Heuristic (classical, fast) ---
t0 = time.time()
assignment = [0] * n_nodes
for node in range(n_nodes):
    # Try both colors, pick the one that maximizes cut with assigned neighbors
    cuts = [0, 0]
    for color in [0, 1]:
        assignment[node] = color
        for i, j in edges:
            if i == node or j == node:
                if i < n_nodes and j < n_nodes:
                    if assignment[i] != assignment[j]:
                        cuts[color] += 1
    assignment[node] = np.argmax(cuts)
greedy_cut = sum(1 for i, j in edges if assignment[i] != assignment[j])
t_greedy = time.time() - t0
print(f"Greedy:       cut={greedy_cut}, time={t_greedy:.6f}s "
      f"(ratio: {greedy_cut/best_cut:.2%} of optimal)")

# --- Solver 3: QAOA (quantum, simulated) ---
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def qaoa_maxcut(graph, edges, p=2, shots=4096):
    n = graph.number_of_nodes()
    # Optimal-ish parameters (pre-computed for this graph)
    gamma = np.array([0.6, 0.3])[:p]
    beta = np.array([0.4, 0.2])[:p]

    qc = QuantumCircuit(n)
    # Initial superposition
    qc.h(range(n))

    for layer in range(p):
        # Problem unitary: exp(-i * gamma * C)
        for i, j in edges:
            qc.cx(i, j)
            qc.rz(2 * gamma[layer], j)
            qc.cx(i, j)
        # Mixer unitary: exp(-i * beta * B)
        for i in range(n):
            qc.rx(2 * beta[layer], i)

    qc.measure_all()
    backend = AerSimulator()
    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts()

    # Find best bitstring
    best = max(counts, key=counts.get)
    bits = [int(b) for b in reversed(best)]  # qiskit bit ordering
    qaoa_cut = sum(1 for i, j in edges if bits[i] != bits[j])
    return qaoa_cut, counts

t0 = time.time()
qaoa_cut, counts = qaoa_maxcut(G, edges, p=2, shots=4096)
t_qaoa = time.time() - t0
print(f"QAOA (p=2):   cut={qaoa_cut}, time={t_qaoa:.4f}s "
      f"(ratio: {qaoa_cut/best_cut:.2%} of optimal)")

# --- Comparison ---
print(f"\n{'Method':<15} {'Cut':>5} {'Time (s)':>10} {'Optimal%':>10} {'Winner?':>8}")
print("-" * 52)
results = [
    ("Brute force", best_cut, t_brute),
    ("Greedy", greedy_cut, t_greedy),
    ("QAOA (sim)", qaoa_cut, t_qaoa),
]
fastest = min(results, key=lambda r: r[2])
best_result = max(results, key=lambda r: r[1])
for name, cut, t in results:
    pct = f"{cut/best_cut:.0%}"
    win = "FAST" if t == fastest[2] else ("BEST" if cut == best_result[1] else "")
    print(f"{name:<15} {cut:>5} {t:>10.4f} {pct:>10} {win:>8}")

# Expected output (approximate):
# MaxCut problem: 10 nodes, 15 edges
#
# Brute force:  cut=13, time=0.0108s (checked 1,024 assignments)
# Greedy:       cut=11, time=0.0001s (ratio: 84.62% of optimal)
# QAOA (sim):   cut=12, time=0.3842s (ratio: 92.31% of optimal)
#
# Method              Cut   Time (s)   Optimal%  Winner?
# ----------------------------------------------------
# Brute force          13     0.0108       100%     BEST
# Greedy               11     0.0001        85%     FAST
# QAOA (sim)           12     0.3842        92%
