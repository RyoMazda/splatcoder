import argparse
from pathlib import Path

from . import config
from . import checker
from .scraper import Scraper


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('args', nargs='*')
    args = parser.parse_args()
    conf = config.load()
    if len(args.args) == 1:
        file_path = args.args[0]
        c = checker.load(file_path=Path(file_path), conf=conf)
        c.run()
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


if __name__ == "__main__":
    main()
