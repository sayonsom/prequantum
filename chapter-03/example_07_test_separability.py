import numpy as np


def validate_two_qubit_pure_state(state: np.ndarray) -> np.ndarray:
    state = np.asarray(state, dtype=complex)
    if state.shape != (4,):
        raise ValueError("expected a four-entry state vector")
    norm = np.linalg.norm(state)
    if not np.isfinite(norm) or norm == 0:
        raise ValueError("state must have a finite nonzero norm")
    return state / norm


def is_separable_pure_state(state: np.ndarray, atol: float = 1e-10) -> bool:
    normalized = validate_two_qubit_pure_state(state)
    coefficient_matrix = normalized.reshape(2, 2)
    return bool(abs(np.linalg.det(coefficient_matrix)) <= atol)


plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
zero = np.array([1, 0], dtype=complex)
product_state = np.kron(plus, zero)
bell_state = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)

print("product separable:", is_separable_pure_state(product_state))
print("Bell separable:", is_separable_pure_state(bell_state))
print("Bell determinant:", np.linalg.det(bell_state.reshape(2, 2)))

# product separable: True
# Bell separable: False
# Bell determinant: (0.4999999999999999+0j)
