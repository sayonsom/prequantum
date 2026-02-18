"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.3 Qiskit V2 Primitives: Sampler and Estimator
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_06_qiskit_v2_primitives_sampler_and_estimat.py
"""

# On real hardware, resilience levels control error mitigation:
#
# from qiskit_ibm_runtime import SamplerV2, EstimatorV2
#
# # resilience_level=0: No mitigation (fastest)
# # resilience_level=1: Twirled readout error extinction (TREX)
# # resilience_level=2: Zero-noise extrapolation (ZNE)
#
# estimator = EstimatorV2(backend)
# estimator.options.resilience_level = 1  # readout mitigation
# estimator.options.default_shots = 4096
#
# # The runtime also supports dynamical decoupling and Pauli twirling
# estimator.options.dynamical_decoupling.enable = True
# estimator.options.twirling.enable_gates = True
#
# # NEW in late 2025: Directed Execution Model via Executor
# # For power users who need control over the mitigation pipeline:
# from qiskit_ibm_runtime import Executor
# executor = Executor(backend)
# # Specify exactly which randomized variants to generate
# # and let the Executor handle generation, execution, and post-processing
