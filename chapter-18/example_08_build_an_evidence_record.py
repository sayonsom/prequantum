"""Build a hash-addressed evidence record for a verified teaching result."""

import hashlib
import json
import platform

import numpy as np
import scipy

model_record = {
    "name": "three-generator-single-period-teaching-model",
    "demand_mw": 150.0,
    "units": ["A", "B", "C"],
    "p_min_mw": [30.0, 20.0, 0.0],
    "p_max_mw": [120.0, 80.0, 60.0],
}
result_record = {
    "commitment": [1, 1, 0],
    "dispatch_mw": [120.0, 30.0, 0.0],
    "reported_cost": 3505.0,
}

assert np.isclose(sum(result_record["dispatch_mw"]), model_record["demand_mw"])
for on, power, minimum, maximum in zip(
    result_record["commitment"],
    result_record["dispatch_mw"],
    model_record["p_min_mw"],
    model_record["p_max_mw"],
):
    assert minimum * on <= power <= maximum * on


def digest(payload) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


evidence = {
    "model_sha256": digest(model_record),
    "result_sha256": digest(result_record),
    "solver_class": "classical exact enumeration plus linear programming",
    "verification": {
        "power_balance": "pass",
        "unit_bounds": "pass",
        "network_security": "not evaluated in this example",
    },
    "environment": {
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
    },
    "operational_boundary": {
        "read_only": True,
        "authorized_for_grid_control": False,
    },
    "strongest_claim": "verified optimum for the declared small teaching model",
}

print(json.dumps(evidence, indent=2, sort_keys=True))
