"""
Pre Quantum - Chapter 21: The Quantum Classical Stack
Code Example: Beat 3: The Concept Build > 3.8 QuantumGridOS Architecture: A Case Study
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-21/example_07_quantumgridos_architecture_a_case_study.py
"""

# What you've been writing in Chapters 13-20:
import quantumgridos as qgo

network = qgo.PowerNetwork.from_ieee_case(14)
uc = qgo.UnitCommitment(network, periods=24)
optimizer = qgo.HybridOptimizer(uc.to_qubo(), backend='simulator')
result = optimizer.solve()
interface = qgo.QuantumPowerInterface(port=5555)
interface.publish_schedule(result.schedule)
