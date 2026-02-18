"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 3: The Concept Build > 3.8 QuantumGridOS Architecture: A Case Study
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_08_quantumgridos_architecture_a_case_study.py
"""

# Simplified from qgo's backend routing pattern
class BackendRouter:
    """Route quantum execution to the right SDK."""

    def route(self, backend: str):
        if backend == 'simulator':
            return self._aer_backend()
        elif backend.startswith('ibm_'):
            return self._ibm_backend(backend)
        elif backend.startswith('braket_'):
            return self._braket_backend(backend)
        elif backend.startswith('ionq_'):
            return self._ionq_via_braket(backend)
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def _ibm_backend(self, name):
        from qiskit_ibm_runtime import QiskitRuntimeService
        service = QiskitRuntimeService(channel='ibm_quantum')
        return IBMAdapter(service.backend(name))

    def _braket_backend(self, arn):
        from braket.aws import AwsDevice
        return BraketAdapter(AwsDevice(arn))
