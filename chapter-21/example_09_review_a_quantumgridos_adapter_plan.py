"""Compare a pinned source inspection with a durable service boundary."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceInspection:
    application_commit: str
    companion_commit: str
    observed_modules: tuple[str, ...]
    observed_capabilities: tuple[str, ...]
    implemented_read_only_tools: tuple[str, ...]


REQUIRED_RECORDS = (
    "request record",
    "plan record",
    "durable job record",
    "immutable result record",
    "operations record",
)

READ_ONLY_MCP_TOOLS = (
    "get_request_record",
    "get_execution_plan",
    "get_job_snapshot",
    "get_result_record",
    "get_operations_summary",
)


def review(inspection: SourceInspection) -> dict[str, object]:
    observed = set(inspection.observed_capabilities)
    missing = [record for record in REQUIRED_RECORDS if record not in observed]
    return {
        "application_commit": inspection.application_commit,
        "companion_commit": inspection.companion_commit,
        "observed_modules": list(inspection.observed_modules),
        "missing_service_records": missing,
        "implemented_read_only_tools": list(inspection.implemented_read_only_tools),
        "submission_authority": "separate explicit service",
    }


inspection = SourceInspection(
    application_commit="dff26bed704886e384c5f7df833828c965a7000a",
    companion_commit="2a80e65f8d29d8c5d27385a2816eea7438ebb533",
    observed_modules=(
        "power-system models",
        "algorithm modules",
        "backend integration",
        "asynchronous TCP interface",
    ),
    observed_capabilities=(),
    implemented_read_only_tools=READ_ONLY_MCP_TOOLS,
)
report = review(inspection)
assert len(report["missing_service_records"]) == 5
assert report["implemented_read_only_tools"] == list(READ_ONLY_MCP_TOOLS)
print(report)
