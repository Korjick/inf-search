import re
from bs4 import BeautifulSoup
import pymorphy2
from natasha import (Doc, MorphVocab, Segmenter, NewsEmbedding, NewsMorphTagger)


def html_lemma(total_pages=128, root_path='./sites/'):
    remove_morph = ['PREP', 'CONJ', 'PRCL', 'INTJ']
    morph = pymorphy2.MorphAnalyzer()
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)

    final = dict()
    for i in range(total_pages):
        with open(root_path + str(i) + '.html', 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text(separator='\n')
            text = re.sub(r'[^\w\s]', '', text)
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            text = ' '.join(chunk.lower() for chunk in chunks if
                            morph.parse(chunk)[0].tag.POS not in remove_morph and len(chunk) > 0 and not any(
                                char.isdigit() for char in chunk))
            doc = Doc(text)
            doc.segment(segmenter)
            doc.tag_morph(morph_tagger)
            for token in doc.tokens:
                token.lemmatize(morph_vocab)
                if token.lemma not in final:
                    final[token.lemma] = set()
                final[token.lemma].add(token.text)

    return final
