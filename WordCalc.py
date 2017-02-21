from gensim.models import word2vec

def intention_calc(model, array, option):
  target = "釣り"
  if option==0:
    return naturalCalc(model, array, target)
  else:
    return forceCalc(model, array, target)


def naturalCalc(model, pos_array, target):
  print(pos_array)
  words = model.most_similar(positive=pos_array, negative=[], topn=100)

  compared_words = []
  for w in words:
    compared_words.append([w[0], model.similarity(w[0], target)])
  return sorted(compared_words, key=lambda x: x[1], reverse=True)[:10]


def forceCalc(model, pos_array, target):
  similar_words = []
  pos_array.append(target)
  print(pos_array)
  words = model.most_similar(positive=pos_array, negative=[], topn=100)
 
  threshold = 0.6 #類似度のしきい値
  
  for w in words:
    if w[1] >= threshold:   # しきい値比較する
      similar_words.append(w)
  if similar_words == []:
    similar_words=words[:10]
  return similar_words
  


if __name__=='__main__':
  file_name = "./MODELS/model_300.vec"
  
  # 学習済みモデルのロード
  model = word2vec.Word2Vec.load_word2vec_format(file_name, binary=False)
 
  while True:
    input_word = input(">>")
    
    print(intention_calc(model, [input_word], option=0))






