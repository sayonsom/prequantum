"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 4: The AI Lab > 🐛 Break This
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_12__break_this.py
"""

from fastapi import FastAPI
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import asyncio

app = FastAPI()
backend = AerSimulator()
results_store = {}

@app.post("/jobs")
async def submit(n_qubits: int = 5, shots: int = 1024):
    import uuid
    job_id = str(uuid.uuid4())[:8]
    results_store[job_id] = {"status": "queued"}

    # Bug 1: blocking call in async handler
    qc = QuantumCircuit(n_qubits)
    qc.h(0)
    for i in range(1, n_qubits):
        qc.cx(0, i)
    qc.measure_all()
    result = backend.run(qc, shots=shots).result()  # blocks event loop!
    results_store[job_id] = {
        "status": "completed",
        "counts": result.get_counts()
    }

    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    # Bug 2: no 404 handling
    return results_store[job_id]

@app.get("/health")
async def health():
    # Bug 3: no memory bounds on results_store
    return {"jobs_stored": len(results_store)}
