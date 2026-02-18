"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 3: The Concept Build > 3.3 Result Caching: Don't Run the Same Circuit Twice
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_03_result_caching_dont_run_the_same_circuit.py
"""

import hashlib
import json
from typing import Optional

class QuantumCache:
    """Cache quantum results by circuit fingerprint."""

    def __init__(self, max_entries: int = 1000):
        self._cache: dict[str, dict] = {}
        self._max = max_entries

    def _fingerprint(self, circuit_qasm: str, shots: int) -> str:
        """Hash the circuit + shot count into a cache key."""
        # QASM string uniquely identifies circuit structure
        content = f"{circuit_qasm}:shots>={shots}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get(self, circuit_qasm: str, shots: int) -> Optional[dict]:
        """Return cached result if available with >= requested shots."""
        key = self._fingerprint(circuit_qasm, shots)
        if key in self._cache:
            cached = self._cache[key]
            if cached["shots"] >= shots:
                return cached["result"]
        return None

    def put(self, circuit_qasm: str, shots: int, result: dict):
        """Store result. Overwrites if new run has more shots."""
        key = self._fingerprint(circuit_qasm, shots)
        if len(self._cache) >= self._max:
            # Evict oldest entry (LRU would be better in production)
            oldest = next(iter(self._cache))
            del self._cache[oldest]
        self._cache[key] = {"shots": shots, "result": result}

# Usage in our service:
cache = QuantumCache()

async def execute_with_cache(qc, shots, backend):
    qasm = qc.qasm()
    cached = cache.get(qasm, shots)
    if cached:
        return cached  # saved $$ and minutes of QPU time

    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts()
    cache.put(qasm, shots, counts)
    return counts
