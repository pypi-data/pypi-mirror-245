#!/usr/bin/env python

from pathlib import Path
from sys import argv

from itaxotools.convphase.phase import phase_mimic_format

if __name__ == "__main__":
    input_path = Path(argv[1])
    output_path = Path(argv[2])

    phase_mimic_format(input_path, output_path)
