"""Example 16.7: wrap the verified polynomial in QuantumGridOS 0.1.9."""

import numpy as np

from quantumgridos.algorithms.qubo import QUBOProblem, solve_qubo_exact


# These coefficients were derived and exhaustively verified in Examples 16.1
# and 16.2. QuantumGridOS uses the same representation: a separate linear
# vector and one copy of each pair coefficient in the upper triangle.
problem = QUBOProblem(
    linear=np.array([-47.0, -76.0, -82.0]),
    quadratic=np.array(
        [
            [0.0, 40.0, 60.0],
            [0.0, 0.0, 120.0],
            [0.0, 0.0, 0.0],
        ]
    ),
    constant=90.0,
    variable_names=["generator_A", "generator_B", "generator_C"],
    metadata={
        "model_scope": "single-period fixed-output commitment candidate",
        "power_unit_mw": 50,
        "demand_units": 3,
    },
)

best = solve_qubo_exact(problem, top_k=2)[0]
print(f"assignment={problem.assignment(best.bitstring)}")
print(f"energy={best.energy:.1f}")
print(f"solver={best.solver}")
print(f"scope={problem.metadata['model_scope']}")

