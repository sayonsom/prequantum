"""Example 16.8: validate an optimization evidence ledger."""

from pprint import pprint


ledger = {
    "decision": {
        "variables": ["generator_A", "generator_B", "generator_C"],
        "domain": "binary",
        "basis_order": "ABC",
        "power_unit_mw": 50,
    },
    "objective": {
        "sense": "minimize",
        "operating_cost": [3.0, 4.0, 8.0],
        "constant_in_ranking": False,
    },
    "feasibility": {
        "constraint": "x_A + 2*x_B + 3*x_C = 3",
        "penalty": 10.0,
        "strict_penalty_threshold": 3.0,
        "decoded_validation_required": True,
    },
    "solver": {
        "exact_baseline": "enumerate 8 assignments",
        "quantum_experiment": "p=1 statevector QAOA",
        "qaoa_parameter_search": "181x121 deterministic grid",
        "shots": None,
        "hardware": None,
    },
    "evidence": {
        "exact_best": "110",
        "exact_cost": 7.0,
        "qaoa_most_probable": "110",
        "qaoa_probability": 0.247209,
        "advantage_claim": None,
    },
}

required_records = {"decision", "objective", "feasibility", "solver", "evidence"}
assert set(ledger) == required_records
assert ledger["feasibility"]["penalty"] > ledger["feasibility"]["strict_penalty_threshold"]
assert ledger["evidence"]["advantage_claim"] is None

for record in ("decision", "objective", "feasibility", "solver", "evidence"):
    print(f"{record}:")
    pprint(ledger[record], sort_dicts=True)

