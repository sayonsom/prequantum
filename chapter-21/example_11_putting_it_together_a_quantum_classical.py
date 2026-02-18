"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 3: The Concept Build > 3.10 Putting It Together: A Quantum-Classical Pipeline
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_11_putting_it_together_a_quantum_classical.py
"""

# energy_optimization_service.py
# Complete quantum-classical pipeline for grid optimization
import uuid
import asyncio
import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Quantum Grid Optimizer", version="2.0.0")

# --- Models ---
class OptimizationRequest(BaseModel):
    ieee_case: int = 5          # IEEE test case number
    periods: int = 24            # scheduling horizon (hours)
    qaoa_layers: int = 2         # QAOA depth
    backend: str = "simulator"   # or "ibm_brisbane"
    error_mitigation: bool = True

class OptimizationResult(BaseModel):
    job_id: str
    status: str
    ieee_case: Optional[int] = None
    total_cost: Optional[float] = None
    schedule: Optional[list] = None
    feasible: Optional[bool] = None
    solver_used: Optional[str] = None
    execution_time_s: Optional[float] = None
    cached: bool = False

# --- State ---
jobs: dict[str, OptimizationResult] = {}
cache: dict[str, dict] = {}

# --- Quantum execution ---
async def run_optimization(job_id: str, req: OptimizationRequest):
    import time
    start = time.time()
    job = jobs[job_id]

    try:
        # Check cache
        cache_key = f"uc:{req.ieee_case}:{req.periods}:{req.qaoa_layers}:{req.backend}"
        if cache_key in cache:
            cached = cache[cache_key]
            job.total_cost = cached["total_cost"]
            job.schedule = cached["schedule"]
            job.feasible = cached["feasible"]
            job.solver_used = cached["solver_used"]
            job.cached = True
            job.status = "completed"
            return

        import quantumgridos as qgo

        # Domain layer: power system → QUBO
        job.status = "building_model"
        network = qgo.PowerNetwork.from_ieee_case(req.ieee_case)
        uc = qgo.UnitCommitment(
            network=network,
            periods=req.periods,
            reserve_margin=0.15,
        )
        qubo = uc.to_qubo(penalty_weight='auto')

        # Quantum layer: QUBO → optimal bitstring
        job.status = "running_quantum"
        optimizer = qgo.HybridOptimizer(
            qubo=qubo,
            backend=req.backend,
            qaoa_layers=req.qaoa_layers,
            error_mitigation=req.error_mitigation,
        )
        result = optimizer.solve()

        # Verification layer: check physics constraints
        job.status = "verifying"
        verification = network.verify_schedule(
            schedule=result.schedule,
            check_line_limits=True,
            check_ramp_rates=True,
        )

        # Store results
        elapsed = time.time() - start
        job.total_cost = float(result.total_cost)
        job.schedule = result.schedule.tolist()
        job.feasible = result.feasible and verification.n_line_violations == 0
        job.solver_used = result.solver_used
        job.execution_time_s = round(elapsed, 2)
        job.status = "completed"

        # Cache
        cache[cache_key] = {
            "total_cost": job.total_cost,
            "schedule": job.schedule,
            "feasible": job.feasible,
            "solver_used": job.solver_used,
        }

    except Exception as e:
        job.status = "failed"

# --- Endpoints ---
@app.post("/optimize")
async def submit_optimization(req: OptimizationRequest):
    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = OptimizationResult(
        job_id=job_id, status="queued", ieee_case=req.ieee_case
    )
    asyncio.create_task(run_optimization(job_id, req))
    return {"job_id": job_id, "status": "queued"}

@app.get("/optimize/{job_id}", response_model=OptimizationResult)
async def get_result(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "Job not found")
    return jobs[job_id]

@app.get("/health")
async def health():
    return {"status": "healthy", "active_jobs": sum(
        1 for j in jobs.values() if j.status not in ("completed", "failed")
    )}

# Docker:
# docker build -t quantum-grid-optimizer .
# docker run -p 8000:8000 quantum-grid-optimizer
#
# Usage:
# curl -X POST "http://localhost:8000/optimize" \
#   -H "Content-Type: application/json" \
#   -d '{"ieee_case": 5, "periods": 24, "qaoa_layers": 2}'
#
# Expected:
# {"job_id": "f3a1b2c4", "status": "queued"}
#
# After ~30 seconds:
# GET /optimize/f3a1b2c4
# {
#   "job_id": "f3a1b2c4",
#   "status": "completed",
#   "ieee_case": 5,
#   "total_cost": 28450.0,
#   "feasible": true,
#   "solver_used": "qaoa_simulator",
#   "execution_time_s": 27.3,
#   "cached": false
# }
