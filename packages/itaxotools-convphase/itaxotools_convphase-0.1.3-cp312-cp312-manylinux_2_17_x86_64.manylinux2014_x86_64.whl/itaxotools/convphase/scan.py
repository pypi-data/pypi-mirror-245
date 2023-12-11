from __future__ import annotations

from pathlib import Path

from itaxotools.taxi2.sequences import Sequences

from .files import get_handler_from_info, get_info_from_path
from .types import PhaseWarning


def scan_input_sequences(sequences: Sequences) -> list[PhaseWarning]:
    sequences = iter(sequences)
    try:
        first = next(sequences)
    except StopIteration:
        return [PhaseWarning.Empty()]
    length = len(first.seq)
    has_missing = _scan_missing(first.seq)
    ids = set([first.id])
    uniform = True
    duplicates = False
    phased = False
    for sequence in sequences:
        if len(sequence.seq) != length:
            uniform = False
        if not has_missing:
            has_missing = _scan_missing(sequence.seq)
        if not duplicates and sequence.id in ids:
            duplicates = True
        if "allele" in sequence.extras:
            phased = True
        ids.add(sequence.id)
    warns = []
    if not uniform:
        warns.append(PhaseWarning.Length())
    if has_missing:
        warns.append(PhaseWarning.Missing())
    if duplicates:
        warns.append(PhaseWarning.Duplicate())
    if phased:
        warns.append(PhaseWarning.Phased())
    return warns


def scan_input_path(path: Path) -> list[PhaseWarning]:
    info = get_info_from_path(path)
    data = Sequences(get_handler_from_info, path, "r", info)
    return scan_input_sequences(data)


def _scan_missing(seq: str) -> bool:
    for x in "nN?-":
        if x in seq:
            return True
    return False


def scan_output_sequences(sequences: Sequences) -> list[PhaseWarning]:
    ambiguity_characters = set()
    ambiguity_identifiers = set()

    for sequence in sequences:
        ambiguous = False
        for character in sequence.seq:
            character == character.upper()
            if character not in "ACGT-":
                ambiguity_characters.add(character)
                ambiguous = True
        if ambiguous:
            ambiguity_identifiers.add(sequence.id)

    warns = []
    if ambiguity_characters:
        warns.append(
            PhaseWarning.Ambiguity(ambiguity_characters, ambiguity_identifiers)
        )
    return warns


def scan_output_path(path: Path) -> list[PhaseWarning]:
    info = get_info_from_path(path)
    data = Sequences(get_handler_from_info, path, "r", info)
    return scan_output_sequences(data)
