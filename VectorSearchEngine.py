import json
import os
import math


class VectorSearchEngine():
    def __init__(self):
        # Step 1: Load JSON file
        with open('inverted_index.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # Step 2: Load tf-idf scores
        self.tf_idf = {}
        for i in range(128):
            filename = f'tf-idf-lms/tf_idf_lms_{i}.txt'
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                scores = {}
                for line in lines:
                    word, tf, tf_idf_score = line.split()
                    scores[word] = float(tf_idf_score)
                self.tf_idf[str(i)] = scores

        # Step 3: Create vocabulary
        self.vocab = set()
        for d in self.data.keys():
            self.vocab.add(d)

        # Step 4: Calculate IDF
        self.idf = {}
        N = len(self.tf_idf)
        for word in self.vocab:
            count = sum(1 for i in self.tf_idf if word in self.tf_idf[i])
            self.idf[word] = math.log(N / count)

        # Step 5: Load URLS
        self.indexes = []
        with open('index.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.rstrip()
                line = line.split(' - ')
                self.indexes.append(line[1])

    def search(self, query):
        tokens = query.split()
        query_tf_idf = {}
        for word in tokens:
            if word in self.vocab:
                query_tf_idf[word] = self.idf[word] * (tokens.count(word) / len(tokens))

        results = []
        for doc_id in self.tf_idf:
            doc_tf_idf = self.tf_idf[doc_id]
            numerator = sum(doc_tf_idf.get(w, 0) * query_tf_idf.get(w, 0) for w in self.vocab)
            denominator = math.sqrt(sum(v ** 2 for v in doc_tf_idf.values())) * math.sqrt(
                sum(v ** 2 for v in query_tf_idf.values()))
            similarity = numerator / denominator if denominator != 0 else 0
            results.append((doc_id, similarity))

        results.sort(key=lambda x: x[1], reverse=True)
        return [self.indexes[int(x[0])] for x in results]


# Step 6: Search for documents
if __name__ == '__main__':
    query = 'сталкер дубляж'
    vecSearch = VectorSearchEngine()
    result = vecSearch.search(query)
    print(result)
