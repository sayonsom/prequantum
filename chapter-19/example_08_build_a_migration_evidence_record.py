"""Build and verify a hash-addressed cryptographic migration evidence record."""

from dataclasses import asdict, dataclass
from hashlib import sha256
import json


def canonical_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


@dataclass(frozen=True)
class MigrationEvidence:
    asset_id: str
    inventory_hash: str
    target_standard: str
    test_report_hash: str
    interoperability_passed: bool
    rollback_tested: bool
    approval_status: str
    conclusion: str


def main() -> None:
    inventory_entry = {
        "asset_id": "api-kex",
        "purpose": "confidentiality",
        "current_primitive": "ECDH",
        "owner": "platform",
    }
    test_report = {
        "candidate": "approved product profile using ML-KEM",
        "environment": "isolated staging",
        "tests": ["known-answer", "negative-input", "interoperability", "rollback"],
        "passed": True,
    }
    evidence = MigrationEvidence(
        asset_id=inventory_entry["asset_id"],
        inventory_hash=canonical_hash(inventory_entry),
        target_standard="FIPS 203",
        test_report_hash=canonical_hash(test_report),
        interoperability_passed=True,
        rollback_tested=True,
        approval_status="security-review-pending",
        conclusion="staging evidence supports review; production migration is not authorized",
    )

    serialized = asdict(evidence)
    print(json.dumps(serialized, indent=2, sort_keys=True))
    print(f"evidence_record_sha256={canonical_hash(serialized)}")

    assert evidence.inventory_hash == canonical_hash(inventory_entry)
    assert evidence.test_report_hash == canonical_hash(test_report)
    assert evidence.approval_status != "approved"
    assert "not authorized" in evidence.conclusion


if __name__ == "__main__":
    main()
