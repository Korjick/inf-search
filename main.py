from lxml import html
import requests
import re
from bs4 import BeautifulSoup
import pymorphy2
from natasha import (Doc, MorphVocab, Segmenter, NewsEmbedding, NewsMorphTagger)

import utils

if __name__ == '__main__':
    final = utils.html_lemma()



    open('./lemmas.txt', 'w').close()
    with open('./lemmas.txt', 'a', encoding='utf-8') as file:
        for key, value in final.items():
            file.write(key + ' ' + ' '.join(value) + '\n')