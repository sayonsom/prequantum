"""Read, compile, and trace the ideal one-signal BB84 circuit.

This program is a circuit unit test, not a secure QKD implementation. It omits
authentication, finite-key analysis, device imperfections, reconciliation,
privacy amplification, secret-key storage, and every production control.
"""

from collections import Counter

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator, Statevector
from qiskit_aer import AerSimulator


BASIS_GATES = ["rz", "sx", "x", "cx"]
BASIS_NAME = {0: "Z", 1: "X"}


def bb84_signal_circuit(
    alice_bit: int,
    alice_basis: int,
    bob_basis: int,
    *,
    measure: bool,
) -> QuantumCircuit:
    """Build X^a, H^alpha, H^beta, then optional Z measurement."""
    if alice_bit not in (0, 1):
        raise ValueError("alice_bit must be 0 or 1")
    if alice_basis not in (0, 1) or bob_basis not in (0, 1):
        raise ValueError("basis values must be 0 for Z or 1 for X")

    circuit = QuantumCircuit(1, 1 if measure else 0)
    if alice_bit:
        circuit.x(0)
    if alice_basis:
        circuit.h(0)
    if bob_basis:
        circuit.h(0)
    if measure:
        circuit.measure(0, 0)
    return circuit


def expected_probabilities(
    alice_bit: int, alice_basis: int, bob_basis: int
) -> np.ndarray:
    """Return ideal probabilities for Bob's displayed classical result."""
    if alice_basis == bob_basis:
        return np.array([1 - alice_bit, alice_bit], dtype=float)
    return np.array([0.5, 0.5], dtype=float)


def sampled_probabilities(counts: Counter | dict[str, int]) -> np.ndarray:
    total = sum(counts.values())
    return np.array([counts.get("0", 0), counts.get("1", 0)]) / total


def main() -> None:
    simulator = AerSimulator()
    shots = 4096
    print("a A_basis B_basis ideal_p0 ideal_p1 sampled_p0 sampled_p1 compiled_ops")

    for alice_bit in (0, 1):
        for alice_basis in (0, 1):
            for bob_basis in (0, 1):
                unitary = bb84_signal_circuit(
                    alice_bit, alice_basis, bob_basis, measure=False
                )
                logical = bb84_signal_circuit(
                    alice_bit, alice_basis, bob_basis, measure=True
                )
                compiled_unitary = transpile(
                    unitary,
                    basis_gates=BASIS_GATES,
                    optimization_level=3,
                    seed_transpiler=1909,
                )
                compiled = transpile(
                    logical,
                    basis_gates=BASIS_GATES,
                    optimization_level=3,
                    seed_transpiler=1909,
                )

                exact = Statevector.from_instruction(unitary).probabilities()
                expected = expected_probabilities(
                    alice_bit, alice_basis, bob_basis
                )
                assert np.allclose(exact, expected, atol=1e-12)
                assert Operator(unitary).equiv(Operator(compiled_unitary))

                result = simulator.run(
                    compiled, shots=shots, seed_simulator=1909
                ).result()
                counts = result.get_counts(compiled)
                sampled = sampled_probabilities(counts)
                if alice_basis == bob_basis:
                    assert sampled[alice_bit] == 1.0
                else:
                    assert np.max(np.abs(sampled - expected)) < 0.04

                operations = ",".join(
                    f"{name}:{count}"
                    for name, count in sorted(compiled.count_ops().items())
                )
                print(
                    f"{alice_bit} {BASIS_NAME[alice_basis]:>7} "
                    f"{BASIS_NAME[bob_basis]:>7} "
                    f"{expected[0]:8.3f} {expected[1]:8.3f} "
                    f"{sampled[0]:10.3f} {sampled[1]:10.3f} {operations}"
                )

    print("Python conditions selected gates before execution: yes")
    print("Dynamic quantum control used: no")
    print("One protocol signal equals one fresh preparation and one measurement.")
    print("Repeated simulator shots here are a probability unit test, not a secret key.")
    print("Security claim: none; this is an ideal circuit contract only.")


if __name__ == "__main__":
    main()
