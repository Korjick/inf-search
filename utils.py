import simplejson as json
import re
from bs4 import BeautifulSoup
import pymorphy2
from natasha import (Doc, MorphVocab, Segmenter, NewsEmbedding, NewsMorphTagger)

def pure_text_from_html(path):
    remove_morph = ['CONJ', 'INTJ', 'PRCL', 'PREP']
    morph = pymorphy2.MorphAnalyzer()
    with open(path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.select('.container')[0].get_text(separator='\n')
        text = re.sub(r'[^\w\s]', '', text)
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        text = ' '.join(chunk.lower() for chunk in chunks if
                        morph.parse(chunk)[0].tag.POS not in remove_morph and len(chunk) > 0 and not any(
                            char.isdigit() for char in chunk))
        return text

def word_to_lemmas_doc(word, segmenter=Segmenter(), morph_vocab=MorphVocab(), emb=NewsEmbedding()):
    morph_tagger = NewsMorphTagger(emb)
    doc = Doc(word)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    return doc

"""
{
    'lemma': {
        'lemma': 'WORD',
        'find_in_pages': [1, 2, 3],
        'count': 3,
        'raw': {
            'WORD_1': [],
            'WORD_2': []
        }
    },
    ...
}
"""
def html_lemma(total_pages=128, root_path='./sites/'):
    final = dict()
    for i in range(total_pages):
        text = pure_text_from_html(root_path + str(i) + '.html')
        doc = word_to_lemmas_doc(text)
        for token in doc.tokens:
            if token.lemma not in final:
                final[token.lemma] = {
                    'lemma': token.lemma,
                    'find_in_pages': set(),
                    'count': 0,
                    'raw': dict()
                }
            final[token.lemma]['count'] += 1
            final[token.lemma]['find_in_pages'].add(i)
            if token.text not in final[token.lemma]['raw']:
                final[token.lemma]['raw'][token.text] = set()
            final[token.lemma]['raw'][token.text].add(i)

    return final


def dict_to_json(dictionary, output='inverted_index.json'):
    with open(output, 'w') as outfile:
        json.dump(dictionary, outfile, iterable_as_array=True)

def json_to_dict(input='inverted_index.json'):
    with open(input, 'r') as inverted:
        return json.load(inverted)
