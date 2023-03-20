import utils

def search(query, search_type='AND'):
    if search_type not in ('AND', 'OR', 'NOT'):
        return []

    lemmas_dict = utils.json_to_dict()

    res = set()
    if search_type == 'NOT':
        for key, value in lemmas_dict.items():
            res = res.union(set(value['find_in_pages']))

    for token in utils.word_to_lemmas_doc(query).tokens:
        if token.lemma in lemmas_dict:
            pages = set(lemmas_dict[token.lemma]['find_in_pages'])
            if len(res) == 0:
                res = pages
            else:
                if search_type == 'AND':
                    res = res.intersection(pages)
                elif search_type == 'OR':
                    res = res.union(pages)
                elif search_type == 'NOT':
                    res = res.difference(pages)
    return list(res)


if __name__ == '__main__':
    query = input('Введите поисковый запрос разделяя слова пробелом: ')
    print(search(query, search_type='NOT'))



