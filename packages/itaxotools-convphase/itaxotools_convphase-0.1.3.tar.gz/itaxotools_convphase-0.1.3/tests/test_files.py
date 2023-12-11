from __future__ import annotations

from pathlib import Path
from typing import Callable, NamedTuple

import pytest
from utility import assert_eq_files

from itaxotools.convphase.files import get_handler_from_info, get_info_from_path
from itaxotools.taxi2.file_types import FileFormat
from itaxotools.taxi2.sequences import Sequence, Sequences

TEST_DATA_DIR = Path(__file__).parent / Path(__file__).stem


class HandlerTest(NamedTuple):
    fixture: Callable[[], Sequences]
    file: str

    @property
    def file_path(self) -> Path:
        return TEST_DATA_DIR / self.file

    @property
    def fixed(self) -> Sequences:
        return self.fixture()

    def validate(self, tmp_path: Path) -> None:
        output_path = tmp_path / self.file
        self.validate_write(output_path)
        self.validate_read()

    def validate_write(self, output_path: Path) -> None:
        info = get_info_from_path(self.file_path)
        handler = get_handler_from_info(output_path, "w", info)
        with handler as file:
            for sequence in self.fixed:
                file.write(sequence)
        assert_eq_files(output_path, self.file_path)

    def validate_read(self) -> None:
        info = get_info_from_path(self.file_path)
        handler = get_handler_from_info(self.file_path, "r", info)
        file_sequences = []
        with handler as file:
            for sequence in file:
                file_sequences.append(sequence)
        fixed_list = list(self.fixed)
        assert len(fixed_list) == len(file_sequences)
        for sequence in fixed_list:
            assert sequence in file_sequences


class InfoTest(NamedTuple):
    file: str
    info: dict = {}

    @property
    def file_path(self) -> Path:
        return TEST_DATA_DIR / self.file

    def validate(self, tmp_path: Path) -> None:
        file_info = get_info_from_path(self.file_path)
        for field in self.info:
            print(field, file_info)
            assert hasattr(file_info, field)
            assert getattr(file_info, field) == self.info[field]


def sequences_simple() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "ATC"),
            Sequence("id2", "ATG"),
            Sequence("id3", "ATA"),
        ]
    )


def sequences_organism() -> Sequences:
    return Sequences(
        [
            Sequence("id1", "ATC", {"organism": "X"}),
            Sequence("id2", "ATG", {"organism": "Y"}),
            Sequence("id3", "ATA", {"organism": "Z"}),
        ]
    )


handler_tests = [
    HandlerTest(sequences_simple, "simple.fas"),
    HandlerTest(sequences_organism, "organism.fas"),
    HandlerTest(sequences_organism, "organism.dot.fas"),
    HandlerTest(sequences_simple, "simple.tsv"),
    HandlerTest(sequences_organism, "organism.tsv"),
]


@pytest.mark.parametrize("test", handler_tests)
def test_files(test: HandlerTest, tmp_path: Path) -> None:
    test.validate(tmp_path)


info_tests = [
    InfoTest("simple.tsv", dict(format=FileFormat.Tabfile)),
    InfoTest("simple.fas", dict(format=FileFormat.Fasta)),
]


@pytest.mark.parametrize("test", info_tests)
def test_infos(test: InfoTest, tmp_path: Path) -> None:
    test.validate(tmp_path)


bad_info_tests = [
    InfoTest("empty.tsv"),
    InfoTest("no_headers.tsv"),
]


@pytest.mark.parametrize("test", bad_info_tests)
def test_bad_infos(test: InfoTest, tmp_path: Path) -> None:
    with pytest.raises(Exception):
        test.validate(tmp_path)
