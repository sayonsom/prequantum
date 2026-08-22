"""Classify a small cryptographic inventory without collecting key material."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CryptoAsset:
    asset_id: str
    purpose: str
    primitive: str
    data_lifetime_years: int
    replacement_lead_years: int
    owner: str


QUANTUM_VULNERABLE = {"RSA", "ECDH", "ECDSA", "DH", "DSA"}


def classify(asset: CryptoAsset) -> tuple[str, str]:
    """Return a review priority and a literal reason."""
    if asset.primitive not in QUANTUM_VULNERABLE:
        return "monitor", "not in this simplified public-key risk set"
    if asset.purpose == "confidentiality" and asset.data_lifetime_years > 0:
        return "high", "recorded ciphertext may outlive its key-establishment protection"
    if asset.replacement_lead_years >= 3:
        return "high", "quantum-vulnerable primitive has a long replacement lead time"
    return "planned", "quantum-vulnerable primitive requires an approved migration path"


def main() -> None:
    inventory = (
        CryptoAsset("api-kex", "confidentiality", "ECDH", 7, 1, "platform"),
        CryptoAsset("firmware-signing", "authenticity", "ECDSA", 12, 5, "devices"),
        CryptoAsset("archive-at-rest", "confidentiality", "AES-256", 15, 2, "data"),
        CryptoAsset("admin-ssh", "authentication", "RSA", 0, 1, "operations"),
    )

    print("asset_id purpose primitive priority reason")
    decisions = {}
    for asset in inventory:
        priority, reason = classify(asset)
        decisions[asset.asset_id] = priority
        print(
            f"{asset.asset_id:16} {asset.purpose:15} {asset.primitive:9} "
            f"{priority:8} {reason}"
        )

    assert decisions["api-kex"] == "high"
    assert decisions["firmware-signing"] == "high"
    assert decisions["archive-at-rest"] == "monitor"
    assert decisions["admin-ssh"] == "planned"
    print("Key material collected: no")
    print("Production configuration changed: no")


if __name__ == "__main__":
    main()
