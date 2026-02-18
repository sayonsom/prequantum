"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 3: The Concept Build > 3.7 The Complete Quantum Microservice Pattern
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_06_the_complete_quantum_microservice_patter.py
"""

# quantum_microservice.py -- production pattern
import uuid
import asyncio
import hashlib
import os
from datetime import datetime
from typing import Optional
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- Configuration ---
USE_REAL_HARDWARE = os.getenv("QUANTUM_BACKEND", "simulator") != "simulator"
IBM_TOKEN = os.getenv("IBM_QUANTUM_TOKEN")
BACKEND_NAME = os.getenv("QUANTUM_BACKEND", "aer_simulator")
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour default

app = FastAPI(
    title="Quantum Microservice",
    description="Production quantum-classical API",
    version="1.0.0",
)

# --- Models ---
class JobStatus(str, Enum):
    QUEUED = "queued"
    TRANSPILING = "transpiling"
    RUNNING = "running"
    POST_PROCESSING = "post_processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobRequest(BaseModel):
    circuit_type: str  # "ghz", "bell", "vqe"
    n_qubits: int = 2
    shots: int = 4096
    error_mitigation: bool = True

class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    backend: str
    created_at: datetime
    result: Optional[dict] = None
    error: Optional[str] = None
    cached: bool = False

# --- State ---
jobs: dict[str, JobResponse] = {}
cache: dict[str, dict] = {}

# --- Backend factory ---
def get_backend():
    if USE_REAL_HARDWARE:
        from qiskit_ibm_runtime import QiskitRuntimeService
        service = QiskitRuntimeService(
            channel="ibm_quantum", token=IBM_TOKEN
        )
        return service.backend(BACKEND_NAME)
    else:
        from qiskit_aer import AerSimulator
        return AerSimulator()

# --- Circuit factory ---
def build_circuit(circuit_type: str, n_qubits: int):
    from qiskit import QuantumCircuit
    if circuit_type == "ghz":
        qc = QuantumCircuit(n_qubits)
        qc.h(0)
        for i in range(1, n_qubits):
            qc.cx(0, i)
        qc.measure_all()
        return qc
    elif circuit_type == "bell":
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()
        return qc
    else:
        raise ValueError(f"Unknown circuit type: {circuit_type}")

# --- Execution engine ---
async def run_job(job_id: str, request: JobRequest):
    job = jobs[job_id]
    try:
        # Check cache first
        cache_key = f"{request.circuit_type}:{request.n_qubits}:{BACKEND_NAME}"
        if cache_key in cache and cache[cache_key]["shots"] >= request.shots:
            job.result = cache[cache_key]["result"]
            job.cached = True
            job.status = JobStatus.COMPLETED
            return

        # Build circuit
        job.status = JobStatus.TRANSPILING
        qc = build_circuit(request.circuit_type, request.n_qubits)

        # Execute
        job.status = JobStatus.RUNNING
        backend = get_backend()
        result = backend.run(qc, shots=request.shots).result()
        counts = result.get_counts()

        # Post-process
        job.status = JobStatus.POST_PROCESSING
        processed = {
            "counts": counts,
            "n_qubits": request.n_qubits,
            "total_shots": sum(counts.values()),
            "dominant_states": {
                k: v for k, v in sorted(
                    counts.items(), key=lambda x: -x[1]
                )[:5]
            },
        }

        # Cache and store
        cache[cache_key] = {"shots": request.shots, "result": processed}
        job.result = processed
        job.status = JobStatus.COMPLETED

    except Exception as e:
        job.status = JobStatus.FAILED
        job.error = str(e)

# --- Endpoints ---
@app.post("/jobs", response_model=dict)
async def submit_job(request: JobRequest):
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = JobResponse(
        job_id=job_id,
        status=JobStatus.QUEUED,
        backend=BACKEND_NAME,
        created_at=datetime.now(),
    )
    asyncio.create_task(run_job(job_id, request))
    return {"job_id": job_id, "status": "queued", "backend": BACKEND_NAME}

@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    return jobs[job_id]

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "backend": BACKEND_NAME,
        "active_jobs": sum(
            1 for j in jobs.values()
            if j.status in (JobStatus.QUEUED, JobStatus.RUNNING)
        ),
        "cache_size": len(cache),
    }

# Run: QUANTUM_BACKEND=simulator uvicorn quantum_microservice:app
# Or:  QUANTUM_BACKEND=ibm_brisbane IBM_QUANTUM_TOKEN=xxx uvicorn quantum_microservice:app
