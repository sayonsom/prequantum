import numpy as np


def partial_trace_b(rho_ab, dim_a=2, dim_b=2):
    tensor = rho_ab.reshape(dim_a, dim_b, dim_a, dim_b)
    return np.trace(tensor, axis1=1, axis2=3)


def entropy(rho, tolerance=1e-12):
    values = np.linalg.eigvalsh(rho)
    values = values[values > tolerance]
    return float(-np.sum(values * np.log2(values)))


def pure_state_report(state):
    rho_ab = np.outer(state, state.conj())
    rho_a = partial_trace_b(rho_ab)
    singular_values = np.linalg.svd(state.reshape(2, 2), compute_uv=False)
    weights = singular_values**2
    return {
        "rho_a": rho_a,
        "schmidt_weights": weights[weights > 1e-12],
        "schmidt_rank": int(np.sum(weights > 1e-12)),
        "entanglement_entropy_bits": entropy(rho_a),
    }


product = np.array([1, 1, 0, 0], dtype=complex) / np.sqrt(2)  # |0> tensor |+>
bell = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
partial = np.array([np.sqrt(0.8), 0, 0, np.sqrt(0.2)], dtype=complex)

for name, state in {"product": product, "bell": bell, "partial": partial}.items():
    report = pure_state_report(state)
    print(
        f"{name}: weights={np.round(report['schmidt_weights'], 6)}, "
        f"rank={report['schmidt_rank']}, entropy={report['entanglement_entropy_bits']:.6f}, "
        f"rho_a={np.round(report['rho_a'], 6)}"
    )

assert pure_state_report(product)["schmidt_rank"] == 1
assert np.isclose(pure_state_report(bell)["entanglement_entropy_bits"], 1.0)

# A separable mixed state can also have a maximally mixed reduced state.
ket_00 = np.array([1, 0, 0, 0], dtype=complex)
ket_11 = np.array([0, 0, 0, 1], dtype=complex)
separable_mixed = 0.5 * np.outer(ket_00, ket_00) + 0.5 * np.outer(ket_11, ket_11)
reduced_separable = partial_trace_b(separable_mixed)
assert np.allclose(reduced_separable, np.eye(2) / 2)
print(f"separable_mixed_reduced_state={reduced_separable}")
print("boundary=reduced-state entropy is an entanglement measure here only when the joint state is pure")
