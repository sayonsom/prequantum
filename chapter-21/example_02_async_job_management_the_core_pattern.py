"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 3: The Concept Build > 3.2 Async Job Management: The Core Pattern
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_02_async_job_management_the_core_pattern.py
"""

# quantum_service_async.py
import uuid
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

app = FastAPI(title="Async Quantum Service")

# --- Job state management ---
class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class QuantumJob(BaseModel):
    job_id: str
    status: JobStatus
    created_at: datetime
    result: Optional[dict] = None
    error: Optional[str] = None

# In-memory store (use Redis/PostgreSQL in production)
jobs: dict[str, QuantumJob] = {}

# --- Quantum execution (runs in background) ---
async def execute_quantum_job(job_id: str, n_qubits: int, shots: int):
    """Background task: build circuit, run, store result."""
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator

    jobs[job_id].status = JobStatus.RUNNING
    try:
        qc = QuantumCircuit(n_qubits)
        qc.h(0)
        for i in range(1, n_qubits):
            qc.cx(0, i)
        qc.measure_all()

        # Simulate hardware latency (real QPU would be minutes)
        backend = AerSimulator()
        result = backend.run(qc, shots=shots).result()
        counts = result.get_counts()

        jobs[job_id].status = JobStatus.COMPLETED
        jobs[job_id].result = {"counts": counts, "n_qubits": n_qubits}

    except Exception as e:
        jobs[job_id].status = JobStatus.FAILED
        jobs[job_id].error = str(e)

# --- API endpoints ---
@app.post("/jobs/ghz")
async def submit_ghz(
    n_qubits: int = 5,
    shots: int = 1024,
    background_tasks: BackgroundTasks = None,
):
    """Submit a GHZ job. Returns immediately with job_id."""
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = QuantumJob(
        job_id=job_id,
        status=JobStatus.QUEUED,
        created_at=datetime.now(),
    )
    background_tasks.add_task(execute_quantum_job, job_id, n_qubits, shots)
    return {"job_id": job_id, "status": "queued"}

@app.get("/jobs/{job_id}")
async def get_job(job_id: str):
    """Poll job status and retrieve results."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

# Run: uvicorn quantum_service_async:app --reload
# Submit: curl -X POST "http://localhost:8000/jobs/ghz?n_qubits=5"
# Poll:   curl "http://localhost:8000/jobs/abc12345"
# Expected flow:
# POST /jobs/ghz → {"job_id": "a1b2c3d4", "status": "queued"}
# GET  /jobs/a1b2c3d4 → {"status": "running", ...}
# GET  /jobs/a1b2c3d4 → {"status": "completed", "result": {"counts": ...}}
