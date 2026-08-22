"""Audit selected QuantumGridOS interfaces without importing the package."""

import argparse
import ast
import subprocess
from pathlib import Path

PINNED_COMMIT = "dff26bed704886e384c5f7df833828c965a7000a"


def class_methods(source_path: Path, class_name: str):
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return {
                child.name
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
    raise AssertionError(f"{class_name} not found in {source_path}")


def imported_modules(source_path: Path):
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    modules = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])
    return modules


parser = argparse.ArgumentParser()
parser.add_argument("repo", type=Path, help="local clone of saralsystems/quantumgridos")
args = parser.parse_args()

commit = subprocess.check_output(
    ["git", "-C", str(args.repo), "rev-parse", "HEAD"], text=True
).strip()
if commit != PINNED_COMMIT:
    raise SystemExit(f"expected {PINNED_COMMIT}, found {commit}")

network_source = args.repo / "quantumgridos/power_systems/network.py"
optimization_source = args.repo / "quantumgridos/power_systems/optimizations.py"
qubo_source = args.repo / "quantumgridos/algorithms/qubo.py"
qaoa_source = args.repo / "quantumgridos/algorithms/qaoa.py"

network_methods = class_methods(network_source, "PowerNetwork")
commitment_methods = class_methods(optimization_source, "UnitCommitment")
qubo_text = qubo_source.read_text(encoding="utf-8")
qaoa_text = qaoa_source.read_text(encoding="utf-8")
optimization_imports = imported_modules(optimization_source)

checks = {
    "PowerNetwork.from_ieee_case": "from_ieee_case" in network_methods,
    "UnitCommitment.solve": "solve" in commitment_methods,
    "UnitCommitment.to_scada_format": "to_scada_format" in commitment_methods,
    "to_scada_format imports time": "time" in optimization_imports,
    "QUBO scope caveat present": "binary master problem" in qubo_text,
    "QAOA schedule reports pmax as output": 'output = gen["pmax"]' in qaoa_text,
    "live-control authorization implemented": False,
}

print("repository commit:", commit)
for label, present in checks.items():
    print(f"{label}: {present}")
print("classification: source inspection only; no grid or quantum job was executed")
