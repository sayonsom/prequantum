"""Build a typed evidence ledger for a bounded QML comparison."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class QMLEvidence:
    data_record: str
    feature_record: str
    learning_record: str
    evidence_record: str
    execution_record: str
    supported_conclusion: str


train_samples = 8
test_samples = 8
train_kernel_pairs = train_samples * (train_samples + 1) // 2
test_kernel_pairs = train_samples * test_samples
shots_per_pair = 1024
total_repetitions = (train_kernel_pairs + test_kernel_pairs) * shots_per_pair

ledger = QMLEvidence(
    data_record=(
        "synthetic two-feature XOR-like data; fixed 8/8 train/test split; "
        "features already scaled to [0,1]"
    ),
    feature_record=(
        "product Ry(pi*x_j) state map; squared state overlap kernel; "
        "exact classical product-cosine formula known"
    ),
    learning_record=(
        "kernel ridge classifier; regularization=0.1; no hyperparameter search"
    ),
    evidence_record=(
        "test correct: linear 4/8, RBF 8/8, product-angle 8/8; "
        "exact statevector calculations"
    ),
    execution_record=(
        f"hypothetical finite-shot estimate: {train_kernel_pairs} train pairs + "
        f"{test_kernel_pairs} test pairs at {shots_per_pair} shots = "
        f"{total_repetitions} circuit repetitions, excluding compilation and retries"
    ),
    supported_conclusion=(
        "two nonlinear kernels fit this declared split; the product-angle kernel "
        "has no demonstrated computational or predictive advantage"
    ),
)

for field, value in asdict(ledger).items():
    print(f"{field}={value}")

quantumgridos_contracts = {
    "get_qml_data_contract": "return split, preprocessing, labels, and leakage checks",
    "get_qml_model_ledger": "return encoding, circuit, observable, optimizer, and costs",
    "get_qml_evidence_report": "return baselines, metrics, uncertainty, resources, and claim",
    "availability": "proposed companion interfaces; not executed by this example",
}
print(f"quantumgridos_contracts={quantumgridos_contracts}")
