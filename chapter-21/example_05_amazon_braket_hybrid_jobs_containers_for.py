"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 3: The Concept Build > 3.5 Amazon Braket Hybrid Jobs: Containers for Quantum
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_05_amazon_braket_hybrid_jobs_containers_for.py
"""

# braket_hybrid_job.py
from braket.aws import AwsDevice
from braket.circuits import Circuit
from braket.jobs import hybrid_job, save_job_result
from braket.jobs.metrics import log_metric
import numpy as np

@hybrid_job(device="arn:aws:braket:::device/quantum-simulator/amazon/sv1")
def vqe_optimization():
    """
    Complete VQE loop runs inside a Braket container.
    Classical optimizer + quantum circuit execution co-located.
    """
    device = AwsDevice(
        "arn:aws:braket:::device/quantum-simulator/amazon/sv1"
    )

    # Define ansatz
    def ansatz(params):
        circ = Circuit()
        circ.ry(0, params[0])
        circ.ry(1, params[1])
        circ.cnot(0, 1)
        circ.ry(0, params[2])
        return circ

    # Simple H2 Hamiltonian coefficients (from Ch. 13)
    coefficients = {
        "II": -1.053, "IZ": 0.395,
        "ZI": -0.395, "ZZ": -0.011, "XX": 0.181
    }

    def cost_function(params):
        circuit = ansatz(params)
        task = device.run(circuit, shots=1000)
        result = task.result()
        # Compute expectation value from counts (simplified)
        counts = result.measurement_counts
        energy = estimate_energy(counts, coefficients)
        log_metric(metric_name="energy", value=energy)
        return energy

    # Classical optimization loop
    from scipy.optimize import minimize
    result = minimize(cost_function, x0=np.random.randn(3), method="COBYLA")

    save_job_result({
        "ground_energy": result.fun,
        "optimal_params": result.x.tolist(),
        "n_iterations": result.nfev,
    })

# Submit from your laptop -- execution happens on AWS
# job = vqe_optimization()
# print(job.result())  # blocks until container completes
