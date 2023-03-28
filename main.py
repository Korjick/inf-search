from lxml import html
import requests
import re
from bs4 import BeautifulSoup
import pymorphy2
from natasha import (Doc, MorphVocab, Segmenter, NewsEmbedding, NewsMorphTagger)

import utils
import json

if __name__ == '__main__':

    # Save our lemmas to json format
    final = utils.html_lemma()
    utils.dict_to_json(final)

    # test = utils.json_to_dict()
    # word = 'напомним'
    # word_doc = utils.word_to_lemmas_doc(word)
    # for token in word_doc.tokens:
    #     print(token.lemma)

