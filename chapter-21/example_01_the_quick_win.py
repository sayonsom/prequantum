"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_01_the_quick_win.py
"""

# quantum_service.py
# pip install fastapi uvicorn qiskit qiskit-aer
from fastapi import FastAPI
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

app = FastAPI(title="Quantum GHZ Service")
backend = AerSimulator()

@app.get("/ghz/{n_qubits}")
async def create_ghz(n_qubits: int, shots: int = 1024):
    """Create and measure a GHZ state."""
    # Build circuit
    qc = QuantumCircuit(n_qubits)
    qc.h(0)
    for i in range(1, n_qubits):
        qc.cx(0, i)
    qc.measure_all()

    # Run on simulator
    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts()

    return {
        "n_qubits": n_qubits,
        "shots": shots,
        "counts": counts,
        "top_state": max(counts, key=counts.get),
    }

# Run with: uvicorn quantum_service:app --reload
# Then visit: http://localhost:8000/ghz/5?shots=4096
# Expected output:
# {
#   "n_qubits": 5,
#   "shots": 4096,
#   "counts": {"00000": 2038, "11111": 2058},
#   "top_state": "11111"
# }
