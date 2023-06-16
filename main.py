
import json
import lzma
import os
from typing import NamedTuple, Dict, Any, Set

from datetime import datetime

import dateutil.parser as converter
import requests
from bs4 import BeautifulSoup


CWD = os.getcwd()
RESULTS_DIR = os.path.join(CWD, 'data')


class ArticleInfo(NamedTuple):
    title: str
    text: str
    publication_dt: datetime
    parsing_dt: datetime
    html: str
    href: str
    language: str

    def to_dict(self) -> Dict[str, Any]:
        dct = self._asdict()
        dct['publication_dt'] = self.publication_dt.isoformat()
        dct['parsing_dt'] = self.parsing_dt.isoformat()
        return dct


class ParsingError(Exception):
    def __init__(self, message: str, exception: Exception) -> None:
        self.exception = exception
        self.message = message


class RequestError(Exception):
    def __init__(self, message: str, exception: Exception) -> None:
        self.exception = exception
        self.message = message


def get_all_articles__yahoo_finance() -> Set[str]:
    url = 'https://finance.yahoo.com'
    html_ = requests.get(url).content
    soup = BeautifulSoup(html_, 'html.parser')
    links = set()
    for link in soup.find_all('a'):
        l = link.get('href')
        if l != None and l.startswith('https'):
            links.add(l)
    return links


def get_article_id(url: str) -> str:
    j = 1
    ch = str(url)[len(str(url))-j]
    while ch != '/':
        j += 1
        ch = str(url)[len(str(url))-j]
    return str(url)[-(j-1):-5]


def parse_article__yahoo_finance(url: str) -> ArticleInfo:
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.content.decode('utf-8')
    except Exception as e:
        raise RequestError('wrong request', e)

    try:
        soup = BeautifulSoup(html, 'html.parser')
        attribute_ = soup.find("h1").text
        publication_dt_ = converter.parse(soup.find("time").text)
        language_ = 'en'
        content_ = soup.find("div", class_="caas-body").text
        href_ = url
        parsing_dt_ = datetime.now().replace(microsecond=0)
        return ArticleInfo(
            title=attribute_,
            text=content_,
            publication_dt=publication_dt_,
            parsing_dt=parsing_dt_,
            html=html,
            href=href_,
            language=language_,
        )
    except Exception as e:
        raise ParsingError('wrong content of page', e)


def save_to_disk(article_id: str, info: ArticleInfo) -> None:
    os.makedirs(os.path.join(RESULTS_DIR, article_id), exist_ok=True)
    with lzma.open(os.path.join(RESULTS_DIR, article_id, f'{article_id}.xz'), "wt") as file:
        file.write(info.html)
    with lzma.open(os.path.join(RESULTS_DIR, article_id, f'json{article_id}.xz'), "wb") as file:
        file.write(json.dumps(info.to_dict()).encode('utf-8'))


def main() -> None:
    print("start")
    print("getting links")
    links = get_all_articles__yahoo_finance()
    print('\n'.join(links))

    for link in links:
        print(" parsing start " + link)
        print(" getting article_")
        article_id = get_article_id(link)

        print(" getting ArticleInfo")
        info = parse_article__yahoo_finance(link)
        if len(info) == 0:
            continue
        print(" saving file")
        save_to_disk(article_id, info)

        print(" parsing link final")
    print("done")


if __name__ == '__main__':
    main()
