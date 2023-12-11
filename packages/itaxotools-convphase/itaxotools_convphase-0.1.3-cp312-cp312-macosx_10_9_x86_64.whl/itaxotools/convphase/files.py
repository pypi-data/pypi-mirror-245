from pathlib import Path
from typing import Literal

from itaxotools.taxi2.file_types import FileFormat, FileInfo
from itaxotools.taxi2.files import get_info, identify_format
from itaxotools.taxi2.sequences import SequenceHandler

Mode = Literal["r", "w"]


def get_info_from_path(path: Path) -> bool:
    format = identify_format(path)
    if format not in [FileFormat.Fasta, FileFormat.Tabfile]:
        raise Exception("Unsupported format")
    info = get_info(path)
    if format == FileFormat.Tabfile:
        if not info.header_individuals or not info.header_sequences:
            raise Exception("Cannot process tabfile headers")
    return info


def get_handler_from_info(
    path: Path, mode: Mode, info: FileInfo
) -> SequenceHandler | None:
    if info.format == FileFormat.Fasta:
        return _get_handler_from_fasta_info(path, mode, info)
    elif info.format == FileFormat.Tabfile:
        return _get_handler_from_tabfile_info(path, mode, info)
    return None


def _get_handler_from_fasta_info(
    path: Path, mode: Mode, info: FileInfo.Fasta
) -> SequenceHandler:
    kwargs = {}
    if mode == "r":
        kwargs["parse_organism"] = info.has_subsets
    elif mode == "w":
        kwargs["write_organism"] = info.has_subsets

    return SequenceHandler.Fasta(
        path, mode, organism_separator=info.subset_separator, **kwargs
    )


def _get_handler_from_tabfile_info(
    path: Path, mode: Mode, info: FileInfo.Tabfile
) -> SequenceHandler:
    return SequenceHandler.Tabfile(
        path,
        mode,
        idHeader=info.header_individuals,
        seqHeader=info.header_sequences,
    )
