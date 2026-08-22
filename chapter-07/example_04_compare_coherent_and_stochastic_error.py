import numpy as np


rng = np.random.default_rng(19)
delta = 0.01
trials = 50_000
cycle_counts = [1, 5, 10, 20, 40]

print("cycles  coherent_error  stochastic_mean_error")

for cycles in cycle_counts:
    coherent_angle = 2 * cycles * delta
    coherent_error = np.sin(coherent_angle / 2) ** 2

    random_signs = rng.choice(
        [-1.0, 1.0], size=(trials, 2 * cycles)
    )
    stochastic_angles = delta * random_signs.sum(axis=1)
    stochastic_error = np.mean(np.sin(stochastic_angles / 2) ** 2)

    print(f"{cycles:6d}  {coherent_error:14.6f}  {stochastic_error:21.6f}")

assert np.sin(20 * delta) ** 2 > 10 * delta**2
