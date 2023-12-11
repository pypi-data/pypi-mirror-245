from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pytest
from utility import assert_eq_files

from itaxotools.convphase.phase import phase_mimic_format

TEST_DATA_DIR = Path(__file__).parent / Path(__file__).stem


class MimicTest(NamedTuple):
    input_file: str
    output_file: str
    kwargs: dict = {}

    @property
    def input_path(self) -> Path:
        return TEST_DATA_DIR / self.file

    @property
    def output_path(self) -> Path:
        return TEST_DATA_DIR / self.file

    def validate(self, tmp_path: Path) -> None:
        input_path = TEST_DATA_DIR / self.input_file
        target_path = TEST_DATA_DIR / self.output_file
        output_path = tmp_path / self.output_file
        phase_mimic_format(input_path, output_path, **self.kwargs)
        assert_eq_files(output_path, target_path)


phase_tests = [
    MimicTest("simple.unphased.fas", "simple.phased.fas"),
    MimicTest("organism.unphased.fas", "organism.phased.fas"),
    MimicTest("organism.dot.unphased.fas", "organism.dot.phased.fas"),
    MimicTest("simple.unphased.tsv", "simple.phased.tsv"),
    MimicTest("organism.unphased.tsv", "organism.phased.tsv"),
    MimicTest("sample.unphased.fas", "sample.phased.fas"),
    MimicTest(
        "sample.unphased.fas", "sample.phased.p03.fas", dict(phase_threshold=0.3)
    ),
]


@pytest.mark.parametrize("test", phase_tests)
def test_mimic(test: MimicTest, tmp_path: Path) -> None:
    test.validate(tmp_path)
