from __future__ import annotations

from typing import Callable, NamedTuple

import pytest

from itaxotools.convphase.scan import scan_input_sequences, scan_output_sequences
from itaxotools.convphase.types import PhaseWarning
from itaxotools.taxi2.sequences import Sequence, Sequences


class ScanInputTest(NamedTuple):
    fixture: Callable[[], Sequences]
    warns: list[PhaseWarning]

    @property
    def sequences(self) -> Sequences:
        return self.fixture()

    def validate(self):
        warns = scan_input_sequences(self.sequences)
        for w in warns:
            assert w in self.warns


class ScanOutputTest(NamedTuple):
    fixture: Callable[[], Sequences]
    warns: list[PhaseWarning]

    @property
    def sequences(self) -> Sequences:
        return self.fixture()

    def validate(self):
        warns = scan_output_sequences(self.sequences)
        for w in warns:
            assert w in self.warns


def good_sequences() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "AAA"),
            Sequence("id2", "GGG"),
        ]
    )


def empty_sequences() -> Sequences:
    return Sequences([])


def missing_sequences_1() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "AAN"),
            Sequence("id2", "GGG"),
        ]
    )


def missing_sequences_2() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "AAA"),
            Sequence("id2", "GGN"),
        ]
    )


def missing_sequences_3() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "AAA"),
            Sequence("id2", "GGn"),
        ]
    )


def missing_sequences_4() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "AAA"),
            Sequence("id2", "GG-"),
        ]
    )


def missing_sequences_5() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "AAA"),
            Sequence("id2", "GG?"),
        ]
    )


def non_uniform_sequences_1() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "AA"),
            Sequence("id2", "GGGG"),
        ]
    )


def non_uniform_sequences_2() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "AAAA"),
            Sequence("id2", "GG"),
        ]
    )


def non_uniform_and_missing_sequences() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "AA--"),
            Sequence("id2", "GGn"),
        ]
    )


def duplicate_id_sequences() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "AAA"),
            Sequence("id1", "GGG"),
        ]
    )


def ambiguous_sequences() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "ASN"),
            Sequence("id2", "wG-"),
        ]
    )


scan_tests = [
    ScanInputTest(good_sequences, []),
    ScanInputTest(empty_sequences, [PhaseWarning.Empty()]),
    ScanInputTest(missing_sequences_1, [PhaseWarning.Missing()]),
    ScanInputTest(missing_sequences_2, [PhaseWarning.Missing()]),
    ScanInputTest(missing_sequences_3, [PhaseWarning.Missing()]),
    ScanInputTest(missing_sequences_4, [PhaseWarning.Missing()]),
    ScanInputTest(missing_sequences_5, [PhaseWarning.Missing()]),
    ScanInputTest(non_uniform_sequences_1, [PhaseWarning.Length()]),
    ScanInputTest(non_uniform_sequences_2, [PhaseWarning.Length()]),
    ScanInputTest(
        non_uniform_and_missing_sequences,
        [PhaseWarning.Length(), PhaseWarning.Missing()],
    ),
    ScanInputTest(duplicate_id_sequences, [PhaseWarning.Duplicate()]),
    ScanOutputTest(good_sequences, []),
    ScanOutputTest(
        ambiguous_sequences, [PhaseWarning.Ambiguity("swn", ["id2", "id1"])]
    ),
]


@pytest.mark.parametrize("test", scan_tests)
def test_scan(test: ScanInputTest | ScanOutputTest) -> None:
    test.validate()
