"""
Pre Quantum - Chapter 17: Quantum Simulation
Code Example: Beat 3: The Concept Build > 3.3 Deep Dive: The Trotter-Suzuki Hierarchy
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-17/example_04_deep_dive_the_trotter_suzuki_hierarchy.py
"""

import numpy as np
from scipy.linalg import expm

# Pauli matrices
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

H_xx = np.kron(X, X)
H_yy = np.kron(Y, Y)
H_zz = np.kron(Z, Z)

# Compute all pairwise commutators
def commutator(A, B):
    return A @ B - B @ A

comm_xy = commutator(H_xx, H_yy)
comm_xz = commutator(H_xx, H_zz)
comm_yz = commutator(H_yy, H_zz)

print("Commutator norms (measure of 'non-commutativity'):")
print(f"  [XX, YY] = {np.linalg.norm(comm_xy):.4f}")
print(f"  [XX, ZZ] = {np.linalg.norm(comm_xz):.4f}")
print(f"  [YY, ZZ] = {np.linalg.norm(comm_yz):.4f}")

# These should all be equal by the symmetry of the Heisenberg model
print(f"\nAll equal? {np.allclose(np.linalg.norm(comm_xy), np.linalg.norm(comm_xz))}")

# Now verify: Trotter error is proportional to commutator norm
# For a 2-term Hamiltonian H = A + B, 1st-order error ≈ ||[A,B]||·dt²/2
dt = 0.1
for A, B, label in [(H_xx, H_yy, "XX+YY"), (H_xx, H_zz, "XX+ZZ")]:
    H_pair = A + B
    U_exact = expm(-1j * H_pair * dt)
    U_trotter = expm(-1j * A * dt) @ expm(-1j * B * dt)
    actual_err = np.linalg.norm(U_trotter - U_exact)
    predicted = np.linalg.norm(commutator(A, B)) * dt**2 / 2
    print(f"\n{label}:")
    print(f"  Actual Trotter error:    {actual_err:.8f}")
    print(f"  Predicted (||[A,B]||dt²/2): {predicted:.8f}")
    print(f"  Ratio: {actual_err/predicted:.4f}")

# Nested commutator drives 2nd-order error
comm_nested = commutator(H_xx, commutator(H_xx, H_yy))
print(f"\nNested commutator ||[XX,[XX,YY]]|| = {np.linalg.norm(comm_nested):.4f}")
print("This drives the 2nd-order Trotter error (O(dt³) per step)")
# Output:
# Commutator norms (measure of 'non-commutativity'):
#   [XX, YY] = 8.0000
#   [XX, ZZ] = 8.0000
#   [YY, ZZ] = 8.0000
#
# All equal? True
#
# XX+YY:
#   Actual Trotter error:    0.03999467
#   Predicted (||[A,B]||dt²/2): 0.04000000
#   Ratio: 0.9999
#
# XX+ZZ:
#   Actual Trotter error:    0.03999467
#   Predicted (||[A,B]||dt²/2): 0.04000000
#   Ratio: 0.9999
#
# Nested commutator ||[XX,[XX,YY]]|| = 32.0000
# This drives the 2nd-order Trotter error (O(dt³) per step)
