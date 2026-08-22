"""Compare quantum and classical kernels on a declared train/test split."""

import numpy as np


X_TRAIN = np.array([
    [0.10, 0.10], [0.20, 0.20], [0.80, 0.80], [0.90, 0.90],
    [0.10, 0.90], [0.20, 0.80], [0.80, 0.20], [0.90, 0.10],
])
Y_TRAIN = np.array([-1, -1, -1, -1, 1, 1, 1, 1])
X_TEST = np.array([
    [0.15, 0.18], [0.75, 0.85], [0.15, 0.82], [0.82, 0.15],
    [0.40, 0.40], [0.60, 0.60], [0.40, 0.60], [0.60, 0.40],
])
Y_TEST = np.array([-1, -1, 1, 1, -1, -1, 1, 1])


def linear_kernel(left, right):
    return 1.0 + left @ right.T


def rbf_kernel(left, right, gamma=8.0):
    differences = left[:, None, :] - right[None, :, :]
    return np.exp(-gamma * np.sum(differences**2, axis=2))


def product_angle_kernel(left, right):
    differences = left[:, None, :] - right[None, :, :]
    return np.prod(np.cos(np.pi * differences / 2) ** 2, axis=2)


def kernel_ridge_predictions(kernel, regularization=0.1):
    train_matrix = kernel(X_TRAIN, X_TRAIN)
    assert np.allclose(train_matrix, train_matrix.T, atol=1e-12)
    assert np.min(np.linalg.eigvalsh(train_matrix)) >= -1e-12
    coefficients = np.linalg.solve(
        train_matrix + regularization * np.eye(len(X_TRAIN)),
        Y_TRAIN,
    )
    scores = kernel(X_TEST, X_TRAIN) @ coefficients
    return np.where(scores >= 0.0, 1, -1), train_matrix


for name, kernel in [
    ("linear", linear_kernel),
    ("rbf", rbf_kernel),
    ("product_angle", product_angle_kernel),
]:
    predictions, train_matrix = kernel_ridge_predictions(kernel)
    correct = int(np.sum(predictions == Y_TEST))
    minimum_eigenvalue = float(np.min(np.linalg.eigvalsh(train_matrix)))
    print(f"{name}: test_correct={correct}/{len(Y_TEST)}, "
          f"minimum_train_eigenvalue={minimum_eigenvalue:.3e}")

print("evidence=the two nonlinear kernels fit this declared split; no advantage claim follows")
