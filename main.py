from __future__ import print_function

from lxml import html
import requests
import re


if __name__ == '__main__':
    HEADERS = {"Accept-Language": "ru-RU,ru;q=0.5"}
    DOWNLOAD_URL = 'https://4pda.to/page/'
    PAGE = 1

    urls = set()

    while len(urls) < 10:
        r = requests.get(DOWNLOAD_URL + str(PAGE), headers=HEADERS, timeout=5)
        r.encoding = 'windows-1251'
        res = html.fromstring(r.text)
        for (element, attr, link, position) in html.iterlinks(res):
            if re.match(r'https://4pda\.to/\d', link):
                urls.add(link)
        PAGE += 1

    open('./index.txt', 'w').close()
    with open('./index.txt', 'a') as index:
        for idx, url in enumerate(urls):
            r = requests.get(url, headers=HEADERS, timeout=5)
            r.encoding = 'windows-1251'
            with open('./' + str(idx) + '.html', 'w', encoding='utf-8') as html:
                html.write(r.text)
                index.write(str(idx) + ' - ' + url + '\n')