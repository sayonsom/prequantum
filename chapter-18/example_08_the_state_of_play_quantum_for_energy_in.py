"""
Pre Quantum - Chapter 18: Quantum for Energy
Code Example: Beat 3: The Concept Build > 3.7 The State of Play: Quantum for Energy in 2025-26
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-18/example_08_the_state_of_play_quantum_for_energy_in.py
"""

import numpy as np

# Hardware landscape as of early 2026
hardware_state = [
    ("IBM Nighthawk",    "Superconducting", 120,  "5,000 2Q gates",   "Nov 2025"),
    ("IBM Kookaburra",   "Superconducting", 1386, "qLDPC QEC module", "2026 target"),
    ("Google Willow",    "Superconducting", 105,  "Below QEC threshold", "Dec 2024"),
    ("Quantinuum Helios","Trapped ion",      98,  "99.92% 2Q fidelity", "Late 2025"),
    ("Infleqtion",       "Neutral atom",    1600, "ARPA-E grid program", "Feb 2026"),
    ("D-Wave Advantage", "Annealer",        5000, "~180 fully connected","Available"),
]

print(f"{'System':<22} {'Type':<18} {'Qubits':>7} {'Key Metric':<25} {'Date':<12}")
print("-" * 90)
for name, qtype, qubits, metric, date in hardware_state:
    print(f"{name:<22} {qtype:<18} {qubits:>7} {metric:<25} {date:<12}")

print()

# Energy-specific quantum programs
energy_programs = [
    ("IonQ + ORNL/DOE",       "Hybrid UC on trapped ions",     "100-200 qubit target by 2026"),
    ("Infleqtion ENCODE",     "ARPA-E grid optimization",      "$6.2M with ComEd, EPRI, Argonne"),
    ("D-Wave + utilities",    "Stochastic UC (annealing)",     "15,000-scenario chance-constrained"),
    ("PNNL review",           "QC for power systems survey",   "OPF, UC, topology optimization"),
]

print(f"\n{'Program':<25} {'Focus':<35} {'Scale/Detail':<40}")
print("-" * 100)
for prog, focus, scale in energy_programs:
    print(f"{prog:<25} {focus:<35} {scale:<40}")

print()

# Updated quantum advantage thresholds
thresholds = [
    ("Current NISQ (2025-26)",  "~100-120 physical",  "Sub-problem decomposition only",
     "IonQ/ORNL demo, Infleqtion ENCODE"),
    ("Near-term (2027-28)",     "~200-500 physical",  "Microgrid-scale UC (10-20 gens)",
     "IBM Cockatoo, Quantinuum Apollo precursor"),
    ("Early fault-tolerant",    "~50 logical",        "Distribution-scale UC with N-1",
     "IBM Starling (2029), Quantinuum Apollo (2029)"),
    ("Full fault-tolerant",     "200+ logical",       "Regional/national grid optimization",
     "IBM Blue Jay (~2033), DARPA Lumos benchmark"),
]
print(f"{'Era':<25} {'Qubits':<22} {'Energy Application':<38} {'Hardware Milestone':<40}")
print("-" * 125)
for era, qubits, app, hw in thresholds:
    print(f"{era:<25} {qubits:<22} {app:<38} {hw:<40}")
# Output:
# System                 Type                Qubits Key Metric                Date
# ------------------------------------------------------------------------------------------
# IBM Nighthawk          Superconducting        120 5,000 2Q gates            Nov 2025
# IBM Kookaburra         Superconducting       1386 qLDPC QEC module         2026 target
# Google Willow          Superconducting        105 Below QEC threshold       Dec 2024
# Quantinuum Helios      Trapped ion             98 99.92% 2Q fidelity       Late 2025
# Infleqtion             Neutral atom           1600 ARPA-E grid program      Feb 2026
# D-Wave Advantage       Annealer              5000 ~180 fully connected     Available
#
# Program                  Focus                              Scale/Detail
# ----------------------------------------------------------------------------------------------------
# IonQ + ORNL/DOE          Hybrid UC on trapped ions          100-200 qubit target by 2026
# Infleqtion ENCODE        ARPA-E grid optimization           $6.2M with ComEd, EPRI, Argonne
# D-Wave + utilities       Stochastic UC (annealing)          15,000-scenario chance-constrained
# PNNL review              QC for power systems survey        OPF, UC, topology optimization
#
# Era                      Qubits                 Energy Application                     Hardware Milestone
# -----------------------------------------------------------------------------------------------------------------------------
# Current NISQ (2025-26)   ~100-120 physical      Sub-problem decomposition only         IonQ/ORNL demo, Infleqtion ENCODE
# Near-term (2027-28)      ~200-500 physical      Microgrid-scale UC (10-20 gens)        IBM Cockatoo, Quantinuum Apollo precursor
# Early fault-tolerant     ~50 logical            Distribution-scale UC with N-1         IBM Starling (2029), Quantinuum Apollo (2029)
# Full fault-tolerant      200+ logical           Regional/national grid optimization    IBM Blue Jay (~2033), DARPA Lumos benchmark
