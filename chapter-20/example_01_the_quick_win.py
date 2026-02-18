"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_01_the_quick_win.py
"""

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

# Build a Bell state circuit
qc = QuantumCircuit(2, 2)
qc.h(0)          # superposition on qubit 0
qc.cx(0, 1)      # entangle qubit 1 with qubit 0
qc.measure([0, 1], [0, 1])

# --- Simulator (what we've been doing) ---
sim = AerSimulator()
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
pm = generate_preset_pass_manager(optimization_level=1, backend=sim)
sim_circuit = pm.run(qc)

from qiskit.primitives import StatevectorSampler
sampler_sim = StatevectorSampler()
job_sim = sampler_sim.run([qc], shots=1024)
result_sim = job_sim.result()
counts_sim = result_sim[0].data.meas.get_counts()
print("Simulator:", counts_sim)
# Simulator: {'00': 512, '11': 512}  (perfect, every time)

# --- Real hardware (what quantum computing actually looks like) ---
# Uncomment below if you have an IBM Quantum account:
# service = QiskitRuntimeService(channel="ibm_quantum")
# backend = service.least_busy(operational=True, simulator=False)
# print(f"Running on: {backend.name}")
# pm_hw = generate_preset_pass_manager(optimization_level=1, backend=backend)
# hw_circuit = pm_hw.run(qc)
# sampler_hw = SamplerV2(backend)
# job_hw = sampler_hw.run([hw_circuit], shots=1024)
# result_hw = job_hw.result()
# counts_hw = result_hw[0].data.meas.get_counts()
# print("Hardware:", counts_hw)
# Hardware: {'00': 441, '11': 389, '01': 122, '10': 72}  (typical)

# Here's what typical real hardware results look like:
counts_hw_typical = {'00': 441, '11': 389, '01': 122, '10': 72}
total = sum(counts_hw_typical.values())
print("\n--- Simulator vs. Hardware ---")
for state in ['00', '11', '01', '10']:
    sim_pct = counts_sim.get(state, 0) / 1024 * 100
    hw_pct = counts_hw_typical.get(state, 0) / total * 100
    print(f"|{state}>: Simulator {sim_pct:5.1f}%  |  Hardware {hw_pct:5.1f}%")
# |00>: Simulator  50.0%  |  Hardware  43.1%
# |11>: Simulator  50.0%  |  Hardware  38.0%
# |01>: Simulator   0.0%  |  Hardware  11.9%
# |10>: Simulator   0.0%  |  Hardware   7.0%
