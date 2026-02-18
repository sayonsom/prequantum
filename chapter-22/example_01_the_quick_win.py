"""
Pre Quantum - Chapter 22: Quantum Error Correction
Code Example: Beat 2: The Quick Win
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-22/example_01_the_quick_win.py
"""

# 3-qubit bit-flip code: encode, corrupt, detect, correct
# pip install qiskit qiskit-aer
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

# Registers
data = QuantumRegister(3, 'data')      # 3 data qubits (encode |0⟩ → |000⟩)
ancilla = QuantumRegister(2, 'anc')    # 2 syndrome qubits
syndrome = ClassicalRegister(2, 'syn') # syndrome measurement results
output = ClassicalRegister(1, 'out')   # final measurement

qc = QuantumCircuit(data, ancilla, syndrome, output)

# Step 1: ENCODE -- spread |0⟩ across 3 qubits: |0⟩ → |000⟩
# (For |1⟩, this would give |111⟩)
# Nothing to do for |0⟩ -- qubits start in |000⟩

# Step 2: ERROR -- flip qubit 1 (simulating a random bit-flip)
qc.x(data[1])  # |000⟩ → |010⟩  (one qubit is wrong!)
qc.barrier()

# Step 3: DETECT -- measure parities without looking at the data
qc.cx(data[0], ancilla[0])  # parity of qubits 0 and 1
qc.cx(data[1], ancilla[0])
qc.cx(data[1], ancilla[1])  # parity of qubits 1 and 2
qc.cx(data[2], ancilla[1])
qc.barrier()

# Step 4: READ syndrome
qc.measure(ancilla[0], syndrome[0])
qc.measure(ancilla[1], syndrome[1])

# Step 5: CORRECT -- use syndrome to fix the error
# syndrome = 11 → qubit 1 flipped, 10 → qubit 0, 01 → qubit 2
qc.x(data[1]).c_if(syndrome, 3)  # syndrome 11 = 3 in binary
qc.x(data[0]).c_if(syndrome, 2)  # syndrome 10 = 2
qc.x(data[2]).c_if(syndrome, 1)  # syndrome 01 = 1

# Step 6: VERIFY -- measure the first data qubit
qc.measure(data[0], output[0])

# Run it
backend = AerSimulator()
result = backend.run(qc, shots=1024).result()
counts = result.get_counts()
print("Results after error + correction:")
for bitstring, count in sorted(counts.items()):
    print(f"  {bitstring}: {count}")

# Expected output:
# Results after error + correction:
#   0 11: 1024
#
# Reading: output=0 (correct!), syndrome=11 (detected error on qubit 1)
# The code detected AND fixed the bit flip!
