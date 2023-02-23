from __future__ import print_function

from lxml import html
import requests


def get_a_nofollow_lxml(url="https://sites.google.com/site/top1000gou/"):
    r = requests.get(url)
    html_source = r.text
    root_element = html.fromstring(html_source)
    return root_element.find_rel_links("nofollow")


def try_download_and_save_pages(urls, limit=100):
    with open('./index.txt', 'w') as file:
        i = 1
        final_output = ''
        for idx, url in enumerate(urls):
            if try_download_and_save_page(url, i):
                final_output += str(i) + ' - ' + url + '\n'
                i += 1
            if i > limit:
                break
        file.write(final_output)


def try_download_and_save_page(url, i):
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    try:
        r = requests.get(url, headers=headers)
        if len(html.fromstring(r.text).text_content()) < 1000:
            return False
        with open('./' + str(i) + '.html', 'w') as file:
            file.write(r.text)
        return True
    except:
        return False


if __name__ == '__main__':
    a_nofollow = get_a_nofollow_lxml()
    urls = []
    for element in a_nofollow:
        urls.append(element.get('href'))
    try_download_and_save_pages(urls, limit=5)
