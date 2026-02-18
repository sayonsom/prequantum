"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 3: The Concept Build > 3.9 Qiskit Serverless: Functions as a Service
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_10_qiskit_serverless_functions_as_a_service.py
"""

# serverless_vqe.py -- deployed to IBM Quantum Platform
from qiskit_serverless import QiskitFunction
from qiskit import QuantumCircuit
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import EstimatorV2 as Estimator
import numpy as np

def vqe_workflow(hamiltonian_terms: dict, n_qubits: int, layers: int):
    """
    Complete VQE workflow deployed as a serverless function.
    IBM manages the infrastructure -- you manage the algorithm.
    """
    from scipy.optimize import minimize

    # Build parameterized ansatz
    ansatz = EfficientSU2(n_qubits, reps=layers)
    hamiltonian = SparsePauliOp.from_list([
        (pauli, coeff) for pauli, coeff in hamiltonian_terms.items()
    ])

    # Estimator handles transpilation and error mitigation
    estimator = Estimator(mode=backend)  # backend injected by runtime

    def cost(params):
        bound = ansatz.assign_parameters(params)
        job = estimator.run([(bound, hamiltonian)])
        return job.result()[0].data.evs[0]

    result = minimize(cost, x0=np.random.randn(ansatz.num_parameters),
                      method="COBYLA", options={"maxiter": 200})

    return {
        "ground_energy": float(result.fun),
        "optimal_params": result.x.tolist(),
        "converged": result.success,
    }

# Deploy to IBM Quantum Platform
vqe_function = QiskitFunction(
    title="VQE Solver",
    entrypoint="serverless_vqe:vqe_workflow",
    dependencies=["scipy"],
)

# Call it like any cloud function
# job = vqe_function.run(
#     hamiltonian_terms={"II": -1.053, "IZ": 0.395, "ZI": -0.395,
#                        "ZZ": -0.011, "XX": 0.181},
#     n_qubits=2,
#     layers=2,
# )
# result = job.result()
# print(f"Ground energy: {result['ground_energy']:.4f} Ha")
