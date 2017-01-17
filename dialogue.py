from gensim.models import word2vec

global model

def responce(file_name): 
  # 学習済みモデルのロード
  model = word2vec.Word2Vec.load_word2vec_format(file_name, binary=False)
  start = input("You >>")
  goal = "徳島"
  A = start
  #B = goal

  while True:
    intention_list = []

    # Aの類似語を集める　類似度順にソート
    similar_words = model.most_similar(positive=[A], negative=[], topn=100)
    similar_words.sort(key=lambda x: float(x[1]), reverse=True)
    
    #similar_words = similar_words[:10]

    for s in similar_words:
      # 各類似語とゴールとの類似度の比較
      intention_list.append((s[0],model.similarity(goal,s[0])))
    
    intention_list.sort(key=lambda x: float(x[1]), reverse=True)
    #print(intention_list)
    
    print("\n単語\t" + goal + "との類似度")
    for il in intention_list:
      print(il[0] + "\t" + str(il[1]))
    
    print("=======================================================")
    print("「" + intention_list[0][0] + "」")
    A = input()
  

if __name__=='__main__':
  file_name = "./MODELS/model_300.vec" 
  responce(file_name)
