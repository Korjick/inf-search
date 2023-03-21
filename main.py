import utils
import tf_idf

if __name__ == '__main__':

    with open('tokens.txt', 'r', encoding='utf-8') as tokens:
        vocabulary = tokens.read().split('\n')

    with open('lemmas.txt', 'r', encoding='utf-8') as tokens:
        vocabulary_lms = tokens.read().split('\n')
        vocabulary_lms = [vcb.split(' ')[0] for vcb in vocabulary_lms]

    texts = []
    lms_texts = []
    for i in range(128):
        text = utils.pure_text_from_html('./sites/' + str(i) + '.html')
        texts.append(text)
        tmp = []
        for token in utils.word_to_lemmas_doc(text).tokens:
            tmp.append(token.lemma)
        lms_texts.append(' '.join(tmp))

    for i, text in enumerate(texts):
        tf_dict = tf_idf.calculate_tf(text, vocabulary)
        tfidf_dict = tf_idf.calculate_tfidf(text, texts, vocabulary)
        with open('tf-idf/tf_idf_' + str(i) + '.txt', 'w', encoding='utf-8') as f:
            for word in tf_dict:
                f.write(f"{word} {tf_dict[word]:.8f} {tfidf_dict[word]:.8f}\n")

    for i, lms_text in enumerate(lms_texts):
        tf_dict = tf_idf.calculate_tf(lms_text, vocabulary_lms)
        tfidf_dict = tf_idf.calculate_tfidf(lms_text, lms_texts, vocabulary_lms)
        with open('tf-idf-lms/tf_idf_lms_' + str(i) + '.txt', 'w', encoding='utf-8') as f:
            for word in tf_dict:
                f.write(f"{word} {tf_dict[word]:.8f} {tfidf_dict[word]:.8f}\n")

