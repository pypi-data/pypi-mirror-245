#!/usr/bin/env python

from pathlib import Path
from sys import argv

from itaxotools.convphase.phase import iter_phase, set_progress_callback
from itaxotools.taxi2.sequences import SequenceHandler


def progress_callback(value, maximum, text):
    print(f"{text}: {value}/{maximum}")


set_progress_callback(progress_callback)


if __name__ == "__main__":
    input_path = Path(argv[1])

    with SequenceHandler.Fasta(input_path) as file:
        x = [(a.id, a.seq) for a in file]

    for z in x:
        print(z)

    print("#" * 50)
    y = iter_phase(x)
    print("#" * 50)

    for z in y:
        print(z)

    print("Done")
