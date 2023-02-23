from __future__ import print_function

from lxml import html
import requests
import csv


if __name__ == '__main__':
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    with open("./builtwith-top1m-20230221.csv", 'r') as file:
        with open('./index.txt', 'w') as index:
            csvreader = csv.reader(file)
            i = 1
            final_output = ''
            for row in csvreader:
                try:
                    if i > 100:
                        break
                    url = 'https://' + row[1]
                    r = requests.get(url, headers=headers, timeout=5)
                    r.encoding = 'utf-8'

                    if r.status_code != 200:
                        continue

                    if len(html.fromstring(r.text).text_content()) < 1000:
                        continue

                    with open('./' + str(i) + '.html', 'w') as htmtext:
                        htmtext.write(r.text)
                        final_output += str(i) + ' - ' + url + '\n'
                        i += 1
                except:
                    continue
            index.write(final_output)
