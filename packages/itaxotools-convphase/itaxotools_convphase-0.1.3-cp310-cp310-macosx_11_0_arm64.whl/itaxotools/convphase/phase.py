from __future__ import annotations

from pathlib import Path
from typing import Callable

from itaxotools._convphase import convPhase, iterPhase, setProgressCallback
from itaxotools.taxi2.sequences import Sequence, Sequences

from .files import get_handler_from_info, get_info_from_path
from .types import PhasedSequence, UnphasedSequence


def iter_phase(
    input: iter[UnphasedSequence],
    number_of_iterations: int = 100,
    thinning_interval: int = 1,
    burn_in: int = 100,
    phase_threshold: float = 0.9,
    allele_threshold: float = 0.9,
) -> iter[PhasedSequence]:
    args = []

    args.append(f"-p{phase_threshold}")
    args.append(f"-q{allele_threshold}")

    args.append(str(number_of_iterations))
    args.append(str(thinning_interval))
    args.append(str(burn_in))

    output = iterPhase(input, args)
    return (PhasedSequence(*x) for x in output)


def phase_mimic_format(input_path: Path, output_path: Path, *args, **kwargs):
    info = get_info_from_path(input_path)
    data = Sequences(get_handler_from_info, input_path, "r", info)
    write_handler = get_handler_from_info(output_path, "w", info)

    unphased = (UnphasedSequence(sequence.id, sequence.seq) for sequence in data)
    phased = iter_phase(unphased, *args, **kwargs)

    phased_dict = {line.id: line for line in phased}

    with write_handler as file:
        for sequence in data:
            try:
                # SeqPhase automatically replaces spaces...
                phased_id = sequence.id.replace(" ", "_")
                line = phased_dict[phased_id]
            except KeyError:
                raise Exception(
                    f'Sequence identifier not found in phased data: "{sequence.id}"'
                )
            sequence_a = Sequence(sequence.id + "a", line.data_a, sequence.extras)
            sequence_b = Sequence(sequence.id + "b", line.data_b, sequence.extras)
            file.write(sequence_a)
            file.write(sequence_b)


def direct_phase(
    input: str,
    number_of_iterations: int = 100,
    thinning_interval: int = 1,
    burn_in: int = 100,
    phase_threshold: float = 0.9,
    allele_threshold: float = 0.9,
) -> str:
    """Uses the C++ backend to parse and write data"""

    args = []

    args.append(input)

    args.append(f"-p{phase_threshold}")
    args.append(f"-q{allele_threshold}")

    args.append(str(number_of_iterations))
    args.append(str(thinning_interval))
    args.append(str(burn_in))

    output = convPhase(*args)
    return output


def set_progress_callback(callback: Callable | None):
    setProgressCallback(callback)
