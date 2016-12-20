from gensim.models import word2vec

global model

def makeRoute(start, goal, file_name):
  print("======= ROUTE =======")
  # 学習済みモデルのロード
  model = word2vec.Word2Vec.load_word2vec_format(file_name, binary=False)

  B = goal
  A_list = [start, model.similarity(B,start)]
  while A_list[0]!=B:
    intention_list = []

    # Aの類似語を集める　類似度順にソート
    similar_words = model.most_similar(positive=[A_list[0]], negative=[], topn=500)
    similar_words.sort(key=lambda x: float(x[1]), reverse=True)
    
    similar_words = similar_words[:10]

    for s in similar_words:
      # 各類似語とゴールとの類似度の比較
      intention_list.append((s[0],model.similarity(B,s[0])))
    
    intention_list.sort(key=lambda x: float(x[1]), reverse=True)
    old_A_list = A_list
    A_list = intention_list[0]
    if A_list[0] == old_A_list[0] or A_list[1] <= old_A_list[1]:
      break
    print(A_list)



def responce(goal, file_name):  
  # 学習済みモデルのロード
  model = word2vec.Word2Vec.load_word2vec_format(file_name, binary=False)
  
  A = input()
  B = goal
  while True:
    intention_list = []

    # Aの類似語を集める　類似度順にソート
    similar_words = model.most_similar(positive=[A,"徳島"], negative=[], topn=100)
    similar_words.sort(key=lambda x: float(x[1]), reverse=True)
    
    print(similar_words) 
    print("単語\t" + A + "との類似度")
   
    for s in similar_words:
      print(s[0] + "\t" + str(s[1]))

    similar_words = similar_words[:10]

    for s in similar_words:

      # 各類似語とゴールとの類似度の比較
      intention_list.append((s[0],model.similarity(B,s[0])))
    
    intention_list.sort(key=lambda x: float(x[1]), reverse=True)
    #print(intention_list)
    
    print("\n単語\t" + B + "との類似度")
    for il in intention_list:
      print(il[0] + "\t" + str(il[1]))
    
    print("=======================================================")
    print("「" + intention_list[0][0] + "」")
    A = input()
  

if __name__=='__main__':
  start = input("start >>")
  goal = input("goal >>")
  file_name = "./MODELS/model_300.vec" 
  makeRoute(start, goal, file_name)
