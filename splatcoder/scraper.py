from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Set

import requests
from bs4 import BeautifulSoup
from termcolor import cprint

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
            cprint("Successfully logged in.", 'green')
            # Just in case
            r = self.session.get('https://atcoder.jp/settings')
            assert(r.text.find(self.config.username) != -1)
        else:
            cprint("Failed to Log in.", 'yellow')

    def _format_url(self, url: str) -> str:
        if url[:len(self.CONTEST_URL_BASE)] != self.CONTEST_URL_BASE:
            return f'https://atcoder.jp/contests/{url}'
        else:
            return url

    def generate_sample_cases(self, url: str) -> Iterator[SampleCase]:
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
        return text.strip(' ,　,\n,\r').replace('\r\n', '\n')

    def _get_task_list_url(self, url: str) -> str:
        if url[:len(self.CONTEST_URL_BASE)] != self.CONTEST_URL_BASE:
            url = f'https://atcoder.jp/contests/{url}'
        if Path(url).name == 'tasks':
            return url
        else:
            if url[-1] == '/':
                url = url[:-1]
            return url + '/tasks'

    def get_task_urls(self, url: str) -> Set[str]:
        url = self._get_task_list_url(url)
        soup = self._get_soup(url)
        links = [a.get('href') for a in soup.select('a')]
        return {f'{self.URL_BASE}{link}' for link in links if isinstance(link, str) and 'tasks/' in link}
