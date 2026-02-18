"""
Pre Quantum - Chapter 18: Quantum for Energy
Code Example: Beat 3: The Concept Build > 3.6 The QuantumGridOS Pipeline
Source: https://github.com/sayonsom/prequantum/tree/main/chapter-18/example_07_the_quantumgridos_pipeline.py
"""

# NOTE: Requires `pip install quantumgridos`
# This block shows the qgo API; raw implementations were in 3.1-3.5
import quantumgridos as qgo

# 1. Load IEEE 14-bus test case
#    14 buses, 20 branches, 5 generators, 11 loads
network = qgo.PowerNetwork.from_ieee_case(14)
print(f"Network: {network.n_bus} buses, {network.n_branch} branches")
print(f"Generators: {network.n_gen}, Total capacity: {network.total_gen_capacity:.0f} MW")
print(f"Total demand: {network.total_load:.0f} MW")

# 2. Run DC power flow (what you built in 3.3, but for 14 buses)
pf_result = network.run_dc_power_flow()
print(f"\nDC Power Flow:")
print(f"  Slack bus generation: {pf_result.slack_power:.1f} MW")
print(f"  Max line loading: {pf_result.max_loading:.1f}%")
print(f"  Congested lines: {pf_result.n_congested}")

# 3. Formulate unit commitment as QUBO
uc = qgo.UnitCommitment(
    network=network,
    periods=24,
    demand_profile='winter_weekday',  # built-in load curves
    reserve_margin=0.15,               # 15% spinning reserve
)

qubo = uc.to_qubo(penalty_weight='auto')  # auto-tunes penalty
print(f"\nUnit Commitment QUBO:")
print(f"  Variables: {qubo.n_variables} (generators x periods)")
print(f"  Non-zero terms: {qubo.n_nonzero}")
print(f"  Estimated qubits needed: {qubo.n_variables}")

# 4. Solve with QAOA (or classical fallback)
optimizer = qgo.HybridOptimizer(
    qubo=qubo,
    backend='simulator',       # or 'ibm_brisbane' for real hardware
    qaoa_layers=3,
    n_restarts=10,
    cost_scaling=True,         # the technique from Ch. 16!
)

result = optimizer.solve()
print(f"\nOptimization Result:")
print(f"  Solver: {result.solver_used}")
print(f"  Total cost: ${result.total_cost:,.0f}")
print(f"  All constraints satisfied: {result.feasible}")
print(f"  Generator schedule shape: {result.schedule.shape}")

# 5. Verify with security-constrained power flow
verification = network.verify_schedule(
    schedule=result.schedule,
    check_line_limits=True,
    check_ramp_rates=True,
)
print(f"\nVerification:")
print(f"  Line limit violations: {verification.n_line_violations}")
print(f"  Ramp rate violations: {verification.n_ramp_violations}")
print(f"  Max line loading: {verification.max_loading:.1f}%")

# 6. Export for SCADA integration
# qgo speaks the protocol that grid control systems understand
interface = qgo.QuantumPowerInterface(port=5555)
interface.publish_schedule(result.schedule)
print(f"\nSchedule published to TCP port {interface.port}")
print(f"SCADA-compatible format: {interface.protocol}")
# Expected output (will vary with qgo version):
# Network: 14 buses, 20 branches
# Generators: 5, Total capacity: 772 MW
# Total demand: 259 MW
#
# DC Power Flow:
#   Slack bus generation: 232.4 MW
#   Max line loading: 83.2%
#   Congested lines: 0
#
# Unit Commitment QUBO:
#   Variables: 120 (generators x periods)
#   Non-zero terms: 4380
#   Estimated qubits needed: 120
#
# Optimization Result:
#   Solver: qaoa_simulator
#   Total cost: $142,560
#   All constraints satisfied: True
#   Generator schedule shape: (5, 24)
#
# Verification:
#   Line limit violations: 0
#   Ramp rate violations: 0
#   Max line loading: 78.5%
#
# Schedule published to TCP port 5555
# SCADA-compatible format: IEEE_CIM_v3
