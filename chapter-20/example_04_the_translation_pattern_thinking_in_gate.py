"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.2 The Translation Pattern: Thinking in Gates, Not SDKs
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_04_the_translation_pattern_thinking_in_gate.py
"""

import pennylane as qml
import numpy as np

dev_grad = qml.device('default.qubit', wires=1)

@qml.qnode(dev_grad, diff_method='parameter-shift')
def circuit(theta):
    qml.RY(theta, wires=0)
    return qml.expval(qml.PauliZ(0))

# Evaluate the circuit
theta_val = np.array(0.5, requires_grad=True)
expectation = circuit(theta_val)
print(f"<Z> at theta=0.5: {expectation:.4f}")
# Output: <Z> at theta=0.5: 0.8776

# Compute the gradient -- PennyLane does this automatically!
gradient = qml.grad(circuit)(theta_val)
print(f"d<Z>/dtheta at theta=0.5: {gradient:.4f}")
# Output: d<Z>/dtheta at theta=0.5: -0.4794

# The parameter-shift rule evaluates the circuit at theta +/- pi/2
# then computes [f(theta + pi/2) - f(theta - pi/2)] / 2
# This works on REAL HARDWARE -- no simulator tricks needed!
manual_gradient = (circuit(np.array(0.5 + np.pi/2)) -
                   circuit(np.array(0.5 - np.pi/2))) / 2
print(f"Manual parameter-shift: {manual_gradient:.4f}")
# Output: Manual parameter-shift: -0.4794  (matches!)
