import math


candidate = {
    "one_qubit_gates": 120,
    "two_qubit_gates": 40,
    "one_qubit_error": 0.001,
    "two_qubit_error": 0.01,
    "scheduled_duration": 18e-6,
    "t1": 200e-6,
    "t2": 120e-6,
}

independent_no_event = (
    (1 - candidate["one_qubit_error"]) ** candidate["one_qubit_gates"]
    * (1 - candidate["two_qubit_error"]) ** candidate["two_qubit_gates"]
)
union_bound = min(
    1.0,
    candidate["one_qubit_gates"] * candidate["one_qubit_error"]
    + candidate["two_qubit_gates"] * candidate["two_qubit_error"],
)
relaxation_survival = math.exp(
    -candidate["scheduled_duration"] / candidate["t1"]
)
coherence_factor = math.exp(
    -candidate["scheduled_duration"] / candidate["t2"]
)

print(f"Independent no-error-event heuristic: {independent_no_event:.3f}")
print(f"Union-bound error-event ceiling:       {union_bound:.3f}")
print(f"T1 survival over schedule:             {relaxation_survival:.3f}")
print(f"T2 coherence factor over schedule:     {coherence_factor:.3f}")
print("These are diagnostics, not a prediction of circuit fidelity.")

assert 0 <= independent_no_event <= 1
assert 0 <= union_bound <= 1
