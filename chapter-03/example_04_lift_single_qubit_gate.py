import numpy as np


X = np.array([[0, 1], [1, 0]], dtype=complex)
I = np.eye(2, dtype=complex)
zero = np.array([1, 0], dtype=complex)
one = np.array([0, 1], dtype=complex)
labels = ("00", "01", "10", "11")

state_01 = np.kron(zero, one)
x_on_left = np.kron(X, I)
x_on_right = np.kron(I, X)

left_result = x_on_left @ state_01
right_result = x_on_right @ state_01

print("start:", labels[int(np.argmax(abs(state_01)))])
print("X on left:", labels[int(np.argmax(abs(left_result)))])
print("X on right:", labels[int(np.argmax(abs(right_result)))])

# start: 01
# X on left: 11
# X on right: 00
