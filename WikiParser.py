import urllib.request

import sys
from bs4 import BeautifulSoup


def get_page(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    return html


def make_soup(page):
    soup = BeautifulSoup(page, 'lxml')
    return soup


if __name__ == '__main__':
    str_url_page = 'https://en.wikipedia.org/wiki/2018_inter-Korean_summit'
    soup_page = make_soup(get_page(str_url_page))
    title_page = soup_page.title.string
    print(soup_page.p)
