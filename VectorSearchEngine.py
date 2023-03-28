import json
import numpy as np
import os


# define function to vectorize a query
def vectorize_query(query):
    vector = np.zeros(len(vocabulary))
    for word in query.split():
        if word in vocabulary:
            vector[list(vocabulary).index(word)] += 1
    return vector / np.linalg.norm(vector)


# define function to rank documents based on cosine similarity
def rank_documents(query_vector):
    scores = matrix_norm.dot(query_vector)
    ranked_indices = np.argsort(scores)[::-1]
    return ranked_indices


if __name__ == '__main__':
    # load json file containing word/page metadata into Python object
    with open('inverted_index.json', 'r', encoding='utf-8') as f:
        word_metadata = json.load(f)
    word_metadata = list(word_metadata.values())

    # load list of files with TF-IDF scores
    tfidf_files = ['tf-idf-lms/tf_idf_lms_{}.txt'.format(i) for i in range(100)]
    tfidf_lists = []
    for filename in tfidf_files:
        with open(filename, 'r', encoding='utf-8') as f:
            tfidf_list = []
            for line in f:
                word, tf_score, tf_idf_score = line.strip().split()
                tfidf_list.append(float(tf_idf_score))
            tfidf_lists.append(tfidf_list)

    # create vocabulary list
    vocabulary = set()
    for tfidf_list in tfidf_lists:
        for i, score in enumerate(tfidf_list):
            if score > 0:
                word = word_metadata[i]["lemma"]
                vocabulary.add(word)

    # create matrix of TF-IDF weights
    matrix = np.zeros((len(tfidf_lists), len(vocabulary)))
    for i, tfidf_list in enumerate(tfidf_lists):
        for j, score in enumerate(tfidf_list):
            if score > 0:
                word = word_metadata[j]["lemma"]
                matrix[i, list(vocabulary).index(word)] = score

    # normalize rows of matrix to have unit length
    norms = np.linalg.norm(matrix, axis=1)
    norms[norms == 0] = 1
    matrix_norm = matrix / norms[:, np.newaxis]

    # given a query, vectorize it and rank the documents
    query = "microsoft"
    query_vector = vectorize_query(query)
    ranked_indices = rank_documents(query_vector)

    indexes = {}
    with open('index.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip().split(' - ')
            indexes[int(line[0])] = line[1]

    # print the top 10 results
    for i in range(10):
        filename = indexes[ranked_indices[i]]
        print("Rank {}: {}".format(i+1, os.path.splitext(filename)[0]))