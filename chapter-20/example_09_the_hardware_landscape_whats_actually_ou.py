"""
Pre Quantum - Chapter 20: SDKs and Real Hardware
Code Example: Beat 3: The Concept Build > 3.5 The Hardware Landscape: What's Actually Out There (2025-2026)
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-20/example_09_the_hardware_landscape_whats_actually_ou.py
"""

# Cost estimation: running a 100-shot Bell state on different platforms
# (Approximate pricing as of early 2026)

platforms = {
    'IBM Quantum (free tier)': {
        'model': '10 min/month free',
        'cost_per_shot': 0.0,
        'notes': 'Queue can be hours; Heron r3 devices'
    },
    'Amazon Braket + IonQ Forte': {
        'model': '$0.30/task + $0.03/shot',
        'cost_100_shots': 0.30 + 100 * 0.03,
        'notes': '$3.30 for 100 shots; 36 algorithmic qubits'
    },
    'Amazon Braket + IonQ Aria': {
        'model': '$0.30/task + $0.03/shot (min 2,500 shots w/ mitigation)',
        'cost_100_shots': 0.30 + 2500 * 0.03,
        'notes': '$75.30 minimum with error mitigation'
    },
    'Azure Quantum + Quantinuum Helios': {
        'model': 'Token-based (HQC)',
        'cost_100_shots': '~$50-200 depending on circuit',
        'notes': 'Most expensive, highest fidelity; 98 Ba+ qubits'
    },
    'Azure Quantum + IonQ Forte': {
        'model': 'Token-based (AQT)',
        'cost_100_shots': '~$15-100 depending on gates',
        'notes': '$1 minimum per job'
    }
}

print("Cloud Quantum Platform Pricing (early 2026):")
print("-" * 55)
for name, info in platforms.items():
    print(f"\n{name}:")
    print(f"  Model: {info['model']}")
    if isinstance(info.get('cost_100_shots'), (int, float)):
        print(f"  100-shot Bell state: ${info['cost_100_shots']:.2f}")
    else:
        print(f"  100-shot Bell state: {info.get('cost_100_shots', 'N/A')}")
    print(f"  Note: {info['notes']}")
