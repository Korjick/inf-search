import math


def calculate_tf(text, vocab):
    words = text.split()
    word_count = len(words)
    tf_dict = {}
    for word in words:
        if word in vocab:
            tf_dict[word] = tf_dict.get(word, 0) + 1
    for word in tf_dict:
        tf_dict[word] = tf_dict[word] / word_count
    return tf_dict


def calculate_idf(texts, word):
    num_texts_containing_word = sum(1 for text in texts if word in text)
    return math.log(len(texts) / num_texts_containing_word)


def calculate_tfidf(text, texts, vocab):
    tf_dict = calculate_tf(text, vocab)
    tfidf_dict = {}
    for word in tf_dict:
        tfidf_dict[word] = tf_dict[word] * calculate_idf(texts, word)
    return tfidf_dict

