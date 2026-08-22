"""Validate a small registry of published NIST PQC standards.

The values below are transcribed from FIPS 203, FIPS 204, and FIPS 205.
The registry distinguishes a final standard from an algorithm selected for
future standardization.
"""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class StandardRecord:
    identifier: str
    primitive: str
    family: str
    publication_date: date | None
    status: str


STANDARDS = (
    StandardRecord(
        "FIPS 203", "ML-KEM", "key encapsulation",
        date(2024, 8, 13), "final",
    ),
    StandardRecord(
        "FIPS 204", "ML-DSA", "digital signature",
        date(2024, 8, 13), "final",
    ),
    StandardRecord(
        "FIPS 205", "SLH-DSA", "digital signature",
        date(2024, 8, 13), "final",
    ),
    StandardRecord(
        "no final FIPS", "HQC", "key encapsulation",
        None, "selected for standardization",
    ),
)

ML_KEM_BYTE_LENGTHS = {
    "ML-KEM-512": {"encapsulation_key": 800, "decapsulation_key": 1632,
                   "ciphertext": 768, "shared_secret": 32},
    "ML-KEM-768": {"encapsulation_key": 1184, "decapsulation_key": 2400,
                   "ciphertext": 1088, "shared_secret": 32},
    "ML-KEM-1024": {"encapsulation_key": 1568, "decapsulation_key": 3168,
                    "ciphertext": 1568, "shared_secret": 32},
}


def main() -> None:
    identifiers = [record.identifier for record in STANDARDS if record.status == "final"]
    assert identifiers == ["FIPS 203", "FIPS 204", "FIPS 205"]
    assert STANDARDS[-1].publication_date is None

    print("identifier primitive family status publication_date")
    for record in STANDARDS:
        published = record.publication_date.isoformat() if record.publication_date else "none"
        print(
            f"{record.identifier:16} {record.primitive:8} "
            f"{record.family:18} {record.status:28} {published}"
        )

    print("\nML-KEM parameter-set byte lengths")
    print("set          ek    dk ciphertext shared_secret")
    for name, sizes in ML_KEM_BYTE_LENGTHS.items():
        print(
            f"{name:12} {sizes['encapsulation_key']:4d} "
            f"{sizes['decapsulation_key']:5d} {sizes['ciphertext']:10d} "
            f"{sizes['shared_secret']:13d}"
        )


if __name__ == "__main__":
    main()
