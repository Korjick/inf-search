from lxml import html
import requests
import re
from bs4 import BeautifulSoup
import pymorphy2
from natasha import (Doc, MorphVocab, Segmenter, NewsEmbedding, NewsMorphTagger)

if __name__ == '__main__':
    TOTAL_PAGES = 128
    REMOVE_MORPH = ['CONJ', 'INTJ', 'PRCL', 'PREP']
    morph = pymorphy2.MorphAnalyzer()
    segmenter = Segmenter()
    morphVocab = MorphVocab()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)

    final = dict()
    for i in range(TOTAL_PAGES):
        with open('./sites/' + str(i) + '.html', 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.select('.container')[0].get_text(separator='\n')
            text = re.sub(r'[^\w\s]', '', text)
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            text = ' '.join(chunk.lower() for chunk in chunks if morph.parse(chunk)[0].tag.POS not in REMOVE_MORPH and len(chunk) > 0 and not any(char.isdigit() for char in chunk))
            doc = Doc(text)
            doc.segment(segmenter)
            doc.tag_morph(morph_tagger)
            for token in doc.tokens:
                token.lemmatize(morphVocab)
                if token.lemma not in final:
                    final[token.lemma] = set()
                final[token.lemma].add(token.text)

    open('./tokens.txt', 'w').close()
    with open('./tokens.txt', 'a', encoding='utf-8') as file:
        for key, value in final.items():
            for token in value:
                file.write(token + '\n')

    open('./lemmas.txt', 'w').close()
    with open('./lemmas.txt', 'a', encoding='utf-8') as file:
        for key, value in final.items():
            file.write(key + ' ' + ' '.join(value) + '\n')