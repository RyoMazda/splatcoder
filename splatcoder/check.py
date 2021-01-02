import os
import subprocess
import sys
from pathlib import Path
from typing import List

from termcolor import cprint

from . import config
from .scraper import SampleCase


def check(file_path: Path, conf: config.Config) -> None:
    file_path = file_path.absolute()
    # Build
    print(f"Start building {file_path}")
    process = subprocess.run(
        conf.build_command.split() + [str(file_path), '-o', 'splat.out'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    # print(process)
    if process.returncode != 0:
        cprint(process.stderr, 'red')
        sys.exit(1)
        return
    cprint("Successfully built!", 'green')
    print(process.stdout)

    # Parse SampleCases
    sample_cases: List[SampleCase] = list()
    with open(file_path) as f:
        lines = f.readlines()
    for i, o, b in zip(
        [i for i, line in enumerate(lines) if line == 'input\n'],
        [i for i, line in enumerate(lines) if line == 'output\n'],
        [i for i, line in enumerate(lines) if line == '\n'],
    ):
        sample_cases.append(SampleCase(
            input_text=''.join(lines[i+1:o]),
            output_text=''.join(lines[o+1:b]),
        ))

    # Execute
    for i, sample in enumerate(sample_cases):
        cprint(f" -- Sample input {i+1} --", 'white')
        cprint(sample.input_text, 'blue', end='')
        cprint(" -- Expected output--", 'white')
        cprint(sample.output_text, 'cyan', end='')
        cprint(" -- Your output --", 'white')
        process = subprocess.run(
            ['./splat.out'],
            input=sample.input_text,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        # print(process)
        cprint(process.stdout, 'magenta')
        cprint(process.stderr, 'red')
        if process.returncode == -11:
            cprint("Segmentation fault: 11", 'red')
            sys.exit(11)
            os.remove('splat.out')
        elif process.returncode != 0:
            cprint("Code exited with some errors!", 'red')
            sys.exit(1)
            os.remove('splat.out')
    os.remove('splat.out')
    cprint("Tested sample inputs successfully!", 'green')
