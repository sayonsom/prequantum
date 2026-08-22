import numpy as np

labels = ("|0>", "|1>")
ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)
ket_plus = (ket_0 + ket_1) / np.sqrt(2)

state_record = {
    "notation": "|+>",
    "basis_order": labels,
    "coordinates": ket_plus,
}

print(state_record["notation"])
print(state_record["basis_order"])
print(np.round(np.real_if_close(state_record["coordinates"]), 4))
print(np.round(np.abs(state_record["coordinates"]) ** 2, 4))
print(np.isclose(np.vdot(ket_plus, ket_plus), 1.0))

# |+>
# ('|0>', '|1>')
# [0.7071 0.7071]
# [0.5 0.5]
# True
