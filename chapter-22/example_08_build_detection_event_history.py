"""Distinguish syndrome values from changes called detection events."""

from __future__ import annotations


def parity_syndrome(data: list[int]) -> tuple[int, int]:
    return data[0] ^ data[1], data[1] ^ data[2]


def xor_pair(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] ^ right[0], left[1] ^ right[1]


data = [0, 0, 0]
previous = (0, 0)
records: list[tuple[int, tuple[int, int], tuple[int, int]]] = []

for round_index in range(1, 5):
    if round_index == 1:
        data[1] ^= 1  # persistent data fault

    measured = parity_syndrome(data)
    if round_index == 2:
        measured = (measured[0] ^ 1, measured[1])  # transient readout fault

    event = xor_pair(previous, measured)
    records.append((round_index, measured, event))
    previous = measured

assert records == [
    (1, (1, 1), (1, 1)),
    (2, (0, 1), (1, 0)),
    (3, (1, 1), (1, 0)),
    (4, (1, 1), (0, 0)),
]

for round_index, measured, event in records:
    print(f"round={round_index} syndrome={measured} event={event}")
