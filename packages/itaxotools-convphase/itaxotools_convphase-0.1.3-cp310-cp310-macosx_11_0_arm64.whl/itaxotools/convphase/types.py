from __future__ import annotations

from typing import Iterable, NamedTuple

from itaxotools.common.types import Type


class UnphasedSequence(NamedTuple):
    id: str
    data: str


class PhasedSequence(NamedTuple):
    id: str
    data_a: str
    data_b: str


class PhaseWarning(Type):
    def __init__(self, text=""):
        self.text = text

    def __str__(self):
        return self.text

    def __eq__(self, other):
        return type(self) is type(other)

    def __hash__(self):
        return hash(type(self))


class Empty(PhaseWarning):
    def __init__(self):
        text = "Dataset is empty!"
        super().__init__(text)


class Length(PhaseWarning):
    def __init__(self):
        text = "Sequences are not of uniform length!"
        super().__init__(text)


class Missing(PhaseWarning):
    def __init__(self):
        text = "Sequences contain gaps or missing nucleotides!"
        super().__init__(text)


class Duplicate(PhaseWarning):
    def __init__(self):
        text = "Dataset contains duplicate ids!"
        super().__init__(text)


class Phased(PhaseWarning):
    def __init__(self):
        text = "Sequences are already phased!"
        super().__init__(text)


class Ambiguity(PhaseWarning):
    def __init__(self, characters: Iterable[str], identifiers: Iterable[str]):
        self.characters = "".join(c.upper() for c in characters)
        self.identifiers = frozenset(identifiers)

        identifiers_str = ", ".join(repr(id) for id in list(self.identifiers)[:3])
        if len(self.identifiers) > 3:
            identifiers_str += f" and {len(self.identifiers) - 3} more"

        character_s = "s" if len(self.characters) > 1 else ""
        identifier_s = "s" if len(self.identifiers) > 1 else ""

        text = f"Ambiguity code{character_s} detected: {repr(self.characters)} for individual{identifier_s}: {identifiers_str}!"

        super().__init__(text)

    def __eq__(self, other):
        if not isinstance(other, Ambiguity):
            return False
        if set(self.characters) != set(other.characters):
            return False
        if self.identifiers != other.identifiers:
            return False
        return True

    def __hash__(self):
        return hash((type(self), self.characters, self.identifiers))
