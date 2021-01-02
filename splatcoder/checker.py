from abc import ABC, abstractmethod
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterator

from termcolor import cprint

from . import config
from .scraper import SampleCase


class Checker(ABC):
    def __init__(
        self,
        file_path: Path,
        conf: config.Config,
    ) -> None:
        self.file_path = file_path.absolute()
        self.conf = conf

    def run(self) -> None:
        """Checks code with sample cases.
        Using Template pattern.
        """
        try:
            print(f"Start building {self.file_path}")
            self._build()
            cprint("Successfully built!", 'green')
            for i, sample in enumerate(self._sample_cases()):
                cprint(f" -- Sample input {i+1} --", 'white')
                cprint(sample.input_text, 'blue', end='')
                cprint(" -- Expected output--", 'white')
                cprint(sample.output_text, 'cyan', end='')
                cprint(" -- Your output --", 'white')
                self._execute(sample)
            cprint("Tested sample inputs successfully!", 'green')
        except Exception as e:
            cprint(str(e), 'red')
        finally:
            self._clean_up()

    def _sample_cases(self) -> Iterator[SampleCase]:
        with open(self.file_path) as f:
            lines = f.readlines()
        for i, o, b in zip(
            [i for i, line in enumerate(lines) if line == 'input\n'],
            [i for i, line in enumerate(lines) if line == 'output\n'],
            [i for i, line in enumerate(lines) if line == '\n'],
        ):
            yield SampleCase(
                input_text=''.join(lines[i+1:o]),
                output_text=''.join(lines[o+1:b]),
            )

    @abstractmethod
    def _build(self) -> None:
        pass

    @abstractmethod
    def _execute(self, sample: SampleCase) -> None:
        pass

    @abstractmethod
    def _clean_up(self) -> None:
        pass


class CppChecker(Checker):
    COMPILED_FILE_NAME = 'splat.out'

    def __init__(
        self,
        file_path: Path,
        conf: config.Config,
    ) -> None:
        super().__init__(file_path, conf)

    def _build(self) -> None:
        process = subprocess.run(
            self.conf.build_command.split() + [
                str(self.file_path),
                '-o', self.COMPILED_FILE_NAME],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        # print(process)
        if process.returncode != 0:
            cprint(process.stderr, 'red')
            sys.exit(1)
            return
        print(process.stdout)

    def _execute(self, sample: SampleCase) -> None:
        process = subprocess.run(
            [f'./{self.COMPILED_FILE_NAME}'],
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
        elif process.returncode != 0:
            cprint("Code exited with some errors!", 'red')
            sys.exit(1)

    def _clean_up(self) -> None:
        os.remove(self.COMPILED_FILE_NAME)


def load(file_path: Path, conf: config.Config) -> Checker:
    return CppChecker(file_path, conf)
