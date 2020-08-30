import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List

from termcolor import cprint

from . import config
from .scraper import SampleCase, Scraper


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
        if process.returncode != 0:
            cprint(process.stderr, 'red')
            sys.exit(1)
            return
        cprint(process.stdout, 'magenta')

    # TODO: should be finally or something
    os.remove('splat.out')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('args', nargs='*')
    args = parser.parse_args()
    conf = config.load()
    if len(args.args) == 1:
        file_path = args.args[0]
        check(Path(file_path), conf=conf)
    elif len(args.args) == 2:
        method = args.args[0]
        url = args.args[1]
        scraper = Scraper(conf)
        if method in ('start-contest', 'sc', 'c'):
            scraper.start_contest(url)
        elif method in ('start-task', 'st', 't'):
            scraper.start_task(url, Path('.'))
        else:
            raise ValueError("Invalid arguments!")
    else:
        raise ValueError("Invalid arguments!")
    return 0


if __name__ == "__main__":
    main()
