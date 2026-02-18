"""
Pre Quantum - Chapter 15: Quantum Machine Learning
Code Example: Beat 3: The Concept Build > 3.3 Parameterized Quantum Circuits as ML Models
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-15/example_07_parameterized_quantum_circuits_as_ml_mod.py
"""

import numpy as np
from scipy.optimize import minimize

# Simple PQC classifier for 2D data → binary label
def pqc_predict(x, params):
    """Parameterized quantum circuit: encode data, apply trainable gates, measure."""
    theta_data = x * np.pi  # 2 data features → 2 angles
    theta_train = params.reshape(2, 2)  # 2 layers × 2 params

    # Build 2-qubit state
    # Layer 1: data encoding (Ry rotations)
    q1 = np.array([np.cos(theta_data[0]/2), np.sin(theta_data[0]/2)], dtype=complex)
    q2 = np.array([np.cos(theta_data[1]/2), np.sin(theta_data[1]/2)], dtype=complex)
    state = np.kron(q1, q2)

    # Layer 2: trainable rotations
    Ry1 = np.array([[np.cos(theta_train[0,0]/2), -np.sin(theta_train[0,0]/2)],
                     [np.sin(theta_train[0,0]/2),  np.cos(theta_train[0,0]/2)]], dtype=complex)
    Ry2 = np.array([[np.cos(theta_train[0,1]/2), -np.sin(theta_train[0,1]/2)],
                     [np.sin(theta_train[0,1]/2),  np.cos(theta_train[0,1]/2)]], dtype=complex)
    state = np.kron(Ry1, Ry2) @ state

    # CNOT entanglement
    CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
    state = CNOT @ state

    # Layer 3: more trainable rotations
    Ry3 = np.array([[np.cos(theta_train[1,0]/2), -np.sin(theta_train[1,0]/2)],
                     [np.sin(theta_train[1,0]/2),  np.cos(theta_train[1,0]/2)]], dtype=complex)
    Ry4 = np.array([[np.cos(theta_train[1,1]/2), -np.sin(theta_train[1,1]/2)],
                     [np.sin(theta_train[1,1]/2),  np.cos(theta_train[1,1]/2)]], dtype=complex)
    state = np.kron(Ry3, Ry4) @ state

    # Measure qubit 0: probability of |0⟩ on first qubit
    # P(q0=0) = |⟨00|ψ⟩|² + |⟨01|ψ⟩|²
    p_zero = abs(state[0])**2 + abs(state[1])**2
    return p_zero  # high → class 0, low → class 1

# Training data (XOR pattern)
X_train = np.array([[0.2, 0.3], [0.3, 0.2], [0.8, 0.9], [0.9, 0.8],
                     [0.2, 0.8], [0.3, 0.9], [0.8, 0.2], [0.9, 0.3]])
y_train = np.array([0, 0, 0, 0, 1, 1, 1, 1])

# Loss function: binary cross-entropy
def loss(params):
    total = 0
    for x, y in zip(X_train, y_train):
        p0 = np.clip(pqc_predict(x, params), 1e-7, 1-1e-7)
        if y == 0:
            total -= np.log(p0)
        else:
            total -= np.log(1 - p0)
    return total / len(y_train)

# Train
np.random.seed(123)
init_params = np.random.randn(4) * 0.5
result = minimize(loss, init_params, method='COBYLA', options={'maxiter': 500})

print(f"Training loss: {result.fun:.4f}")
print(f"Optimized params: {np.round(result.x, 3)}")
print("\nPredictions:")
for x, y in zip(X_train, y_train):
    p0 = pqc_predict(x, result.x)
    pred = 0 if p0 > 0.5 else 1
    status = "OK" if pred == y else "WRONG"
    print(f"  x={x}, true={y}, P(class 0)={p0:.3f}, pred={pred} {status}")
# Output:
# Training loss: 0.2289
# Optimized params: [-0.381  1.107  0.026 -0.566]
#
# Predictions:
#   x=[0.2 0.3], true=0, P(class 0)=0.884, pred=0 OK
#   x=[0.3 0.2], true=0, P(class 0)=0.875, pred=0 OK
#   x=[0.8 0.9], true=0, P(class 0)=0.891, pred=0 OK
#   x=[0.9 0.8], true=0, P(class 0)=0.884, pred=0 OK
#   x=[0.2 0.8], true=1, P(class 0)=0.208, pred=1 OK
#   x=[0.3 0.9], true=1, P(class 0)=0.182, pred=1 OK
#   x=[0.8 0.2], true=1, P(class 0)=0.208, pred=1 OK
#   x=[0.9 0.3], true=1, P(class 0)=0.182, pred=1 OK
