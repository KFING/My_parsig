# import requests
# import time
# import csv
# import re
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
#
# #if __name__ == "__main__":
#     str = 'https://news.yahoo.com/clarence-thomas-wrote-scathing-nearly-174813305.html'
#     url = urlopen(str)
#     link = url.read().decode('utf-8')
#     soup = BeautifulSoup(link, 'html.parser')
#     print(soup.find_all("h1", class_="caas-title-wrapper") )

##get_all_articles__yahoo_finance(from_dt: Optional[datetime], to_dt: Optional[datetime]) -> Set[str]
##get_article_info(href: str) -> str
##parse_article__yahoo_finance(html: str) -> ArticleInfo
#save_to_disk(file_name: str, article: ArticleInfo) -> None
#https://www.yahoo.com/news/san-francisco-police-9-victims-071629061.html

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import datetime
from langdetect import detect
import dateutil.parser as converter
import lzma
import base64
import lxml
import lxml.html
import time
import requests
class ContentParsingError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

def get_all_articles__yahoo_finance():
    url = 'https://finance.yahoo.com'
    str_ = 'https://finance.yahoo.com/news/'
    html_ = requests.get(url).content
    soup = BeautifulSoup(html_, 'html.parser')
    links = set()
    for link in soup.find_all('a'):
        l = link.get('href')
        if l != None and l.startswith('https'):
            print(l)
            links.add(l)
            # if (len(str(l)) > 31):
            #     if (str_ == str(l)[:31]):
            #         print(l)
            #         links.add(l)
    print("OK")
    return links
#return links

def get_article_info(url):
    # page = urlopen(url)
    # html_ = page.read()
    # html_ = requests.get(url).content
    # soup = BeautifulSoup(html_, 'html.parser')
    # atribute_ = soup.find('article')
    # return atribute_
    j = 1
    ch = str(url)[len(str(url))-j]
    while ch != '/':
        j += 1
        ch = str(url)[len(str(url))-j]
    article_ = str(url)[-(j-1):-5]
    print(" OK")
    return str(url)[-(j-1):-5]
#return article_

def parse_article__yahoo_finance(url):
    # page = urlopen(url)
    # html_ = page.read().decode('utf-8')
    try:
        html_ = requests.get(url).content
        soup = BeautifulSoup(html_, 'html.parser')
        attribute_ = soup.find("h1", class_="").text
        publication_dt_ = converter.parse(soup.find("time").text).isoformat()
        language_ = detect(attribute_)
        content_ = soup.find("div", class_="caas-body").text
        href_ = url
        parsing_dt_ = datetime.datetime.now().replace(microsecond=0).isoformat()
        ArticleInfo = (
            str(attribute_),
            str(content_),
            str(publication_dt_),
            str(parsing_dt_),
            str(soup),
            str(href_),
            str(language_)
        )
    except AttributeError as e:
        print (e)
        return tuple()
    else:
        print(" OK")
        return ArticleInfo
#return ArticleInfo

def save_to_disk(article_, ArticleInfo):
    try:
        os.makedirs('result_parsing/' + article_)
        with lzma.open('result_parsing/' + article_ + '/' + article_ + '.xz', "w") as file:
            file.write(ArticleInfo[4].encode('utf-8'))
            file.close()
        jsonFile = {
            'header': ArticleInfo[0],
            'content': ArticleInfo[1],
            'publication_dt': ArticleInfo[2],
            'parsing_dt': ArticleInfo[3],
            'href': ArticleInfo[5],
            'language': ArticleInfo[6]
        }
        #print(jsonFile)
        with lzma.open('result_parsing/' + article_ + '/' + 'json' + article_ + '.xz', "w") as file:
             file.write(str(jsonFile).encode('utf-8'))
             file.close()
             #print('t')
        print(" OK")
    except FileExistsError:
        # directory already exists
        pass
#save

def main():
    print("start")
    print("getting links")
    links = set()
    links = get_all_articles__yahoo_finance()
    for link in links:
        print (link)

    for link in links:
        print(" parsing start " + link)
        print(" getting article_")
        article_ = get_article_info(link)

        print(" getting ArticleInfo")
        ArticleInfo = parse_article__yahoo_finance(link)
        if (len(ArticleInfo) == 0):continue
        print(" saving file")
        save_to_disk(article_, ArticleInfo)

        print(" parsing link final")
    print("done")
def parser(time):
    while True:
        main()
        time.sleep(3600/time)

main()


# print("start")
# print("getting links")
# print("ok")
# print(" link parsing start")
# # https://finance.yahoo.com/news/federal-reserve-interest-rate-policy-decision-june-14-2023-180115494.html
# # https://news.yahoo.com/inside-hunt-idaho-killer-153751015.html
# link = 'https://finance.yahoo.com/news/federal-reserve-interest-rate-policy-decision-june-14-2023-180115494.html'
# print(link)
# print(" getting atribute_")
# atribute_ = get_article_info(link)
# print(" ok")
# print(atribute_)
# print(" getting ArticleInfo")
# ArticleInfo = parse_article__yahoo_finance(link)
# print(" ok")
# print(ArticleInfo[6])
# print(" saving file")
# save_to_disk(atribute_, ArticleInfo)
# print(" ok")
# print("done")

#link = 'https://www.yahoo.com/news/san-francisco-police-9-victims-071629061.html'
# url = 'https://www.yahoo.com/news/san-francisco-police-9-victims-071629061.html'
# page = urlopen(url)
# html_ = page.read().decode('utf-8')
# soup = BeautifulSoup(html_, 'html.parser')
# atribute_ = soup.find("h1", class_="").text
# publication_dt_ =  converter.parse(soup.find("time").text).isoformat()
# language_ =  detect(atribute_)
# content_ = soup.find("div", class_="caas-body").text
# href_ = url
# parsing_dt_ = datetime.datetime.now().replace(microsecond=0).isoformat()

#print(soup)



# links = set()
# for link in soup.find_all('a'):
#     l = link.get('href')
#     if l != None and l.startswith('https'):
#         links.add(l)
# for link in links:
#     print(link)

