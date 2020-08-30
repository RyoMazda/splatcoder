from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Set

import requests
from bs4 import BeautifulSoup

from . import config


@dataclass
class SampleCase:
    input_text: str
    output_text: str

    @property
    def text(self) -> str:
        return f"""input
{self.input_text}
output
{self.output_text}

"""


class Scraper:
    URL_BASE = 'https://atcoder.jp'
    CONTEST_URL_BASE = URL_BASE + '/contests'

    def __init__(self, conf: config.Config) -> None:
        self.config = conf
        self.session = requests.Session()
        self._login()

    def _get_soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(self.session.get(url).text, "html.parser")

    def _login(self) -> None:
        if self.config.username is None or self.config.password is None:
            print("Skip login since username nor password are not set in the config file.")
            return
        url = 'https://atcoder.jp/login'
        csrf_token = self._get_soup(url).find('input', attrs={'name': 'csrf_token'}).get('value')
        resp = self.session.post(
            url,
            data={
                'username': self.config.username,
                "password": self.config.password,
                "csrf_token": csrf_token,
            },
        )
        if resp.text.find('Sign In') == -1:
            print("Successfully logged in.")
            # Just in case
            r = self.session.get('https://atcoder.jp/settings')
            assert(r.text.find(self.config.username) != -1)
        else:
            print("Failed to Log in.")

    def _format_url(self, url: str) -> str:
        if url[:len(self.CONTEST_URL_BASE)] != self.CONTEST_URL_BASE:
            return f'https://atcoder.jp/contests/{url}'
        else:
            return url

    def _generate_sample_cases(self, url: str) -> Iterator[SampleCase]:
        url = self._format_url(url)
        print(f"Parse sample cases for: {url}")
        for h3 in self._get_soup(url).select('h3'):
            if h3.text[:3] == '入力例':
                input_pre = h3.find_next('pre')
                output_h3 = input_pre.find_next('h3')
                assert(output_h3.text[:3] == '出力例')
                output_pre = output_h3.find_next('pre')
                yield SampleCase(
                    input_text=self._strip(input_pre.text),
                    output_text=self._strip(output_pre.text),
                )

    @staticmethod
    def _strip(text: str) -> str:
        return text.strip(' ,　,\n,\r')

    def start_task(self, url: str, output_dir: Path) -> None:
        output_dir = output_dir.absolute()
        print(f"start-task with {url}")
        if not self.config._template_path.exists():
            raise ValueError(
                f"The specified template file {self.config._template_path} does not exist."
                " Please read the document for details.")
        file_name = Path(url).name + '.cpp'
        file_name = file_name.replace(output_dir.name, '')
        if file_name[0] == '_':
            file_name = file_name[1:]
        output_path = output_dir / file_name
        if output_path.exists():
            raise ValueError(f"You already have {output_path}")
        with open(output_path, 'w') as f:
            f.write('/* Generated by splatcoder\n')
            for sample_case in self._generate_sample_cases(url):
                f.write(sample_case.text)
            f.write('*/\n')
            with open(self.config._template_path) as t:
                f.write(t.read())
        print(f"{output_path} was splatted!")

    def _get_task_list_url(self, url: str) -> str:
        if url[:len(self.CONTEST_URL_BASE)] != self.CONTEST_URL_BASE:
            url = f'https://atcoder.jp/contests/{url}'
        if Path(url).name == 'tasks':
            return url
        else:
            if url[-1] == '/':
                url = url[:-1]
            return url + '/tasks'

    def _get_task_urls(self, url: str) -> Set[str]:
        url = self._get_task_list_url(url)
        soup = self._get_soup(url)
        links = [a.get('href') for a in soup.select('a')]
        return {f'{self.URL_BASE}{link}' for link in links if isinstance(link, str) and 'tasks/' in link}

    def start_contest(self, url: str) -> None:
        print(f"Start contest with {url}")
        output_dir = Path('.') / Path(url).name
        output_dir.mkdir(exist_ok=True, parents=True)
        for task_url in self._get_task_urls(url):
            self.start_task(task_url, output_dir)
