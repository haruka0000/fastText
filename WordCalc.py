from gensim.models import word2vec

def intention_calc(model, array):
  
  threshold = 0.6 #類似度のしきい値

  similar_words = []
  pos_array = array

  # しきい値を超える類似語を10個集める
  while len(similar_words) <= 10:
    for s in model.most_similar(positive=pos_array, negative=[], topn=10):
      if s[1] >= threshold:   # しきい値比較する
        similar_words.append(s)
    if len(pos_array) == 1:   #受け取った単語が残り1個になれば諦めて最も類似する10語を取得
      similar_words = model.most_similar(positive=pos_array, negative=[], topn=10)
      break
    pos_array = pos_array[1:]   # 最も古い単語を配列から除去する

  return similar_words
  


if __name__=='__main__':
  file_name = "./MODELS/model_300.vec"
  
  # 学習済みモデルのロード
  model = word2vec.Word2Vec.load_word2vec_format(file_name, binary=False)
 
  pos_array = []
  
  input_word = input(">>")
    
  pos_array.append(input_word)
 
  while True:
    input_word = input(">>")
    
    pos_array.append(input_word)

    if len(pos_array) > 5:
      pos_array = pos_array[-5:]
    
    print(pos_array)
    print(intention_calc(model, pos_array))
    if len(pos_array) >= 3:
      print(pos_array[-3:])
      print(intention_calc(model, pos_array[-3:]))
    if len(pos_array) >= 2:
      print(pos_array[-2:])
      print(intention_calc(model, pos_array[-2:]))






