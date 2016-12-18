from gensim.models import word2vec

model = word2vec.Word2Vec.load_word2vec_format("./model_300.vec", binary=False)

def getSimilarWords(q):
  similar_words = model.most_similar(positive=[q], negative=[])
  print(similar_words)


if __name__ == '__main__':
  getSimilarWords("井上麻里奈")
