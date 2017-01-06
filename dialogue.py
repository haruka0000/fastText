from gensim.models import word2vec
import GetTweets as gt

global model

def makeRoute(model, start, goal):
  print("======= ROUTE =======")
  # 学習済みモデルのロード
  #model = word2vec.Word2Vec.load_word2vec_format(file_name, binary=False)

  B = goal
  A_list = [start, model.similarity(B,start)]
  route = []
  route.append(A_list)
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
    route.append(A_list)
    if A_list[0] == old_A_list[0] or A_list[1] <= old_A_list[1]:
      route.append((B,model.similarity(B,B)))
      break
    print(A_list)
  return route



def responce(file_name): 
  # 学習済みモデルのロード
  model = word2vec.Word2Vec.load_word2vec_format(file_name, binary=False)
  start = input("You >>")
  goal = "徳島"
  #route = makeRoute(model, start, goal) 
  A = start
  #B = goal
  #words = []
  #for r in route[1:]:
  #  words.append(r[0])

  #for word in words:
  while True:
    intention_list = []

    # Aの類似語を集める　類似度順にソート
    similar_words = model.most_similar(positive=[A], negative=[], topn=100)
    similar_words.sort(key=lambda x: float(x[1]), reverse=True)
    
    #print(similar_words) 
    #print("単語\t" + A + "との類似度")
   
    #for s in similar_words:
    #  print(s[0] + "\t" + str(s[1]))

    similar_words = similar_words[:10]

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
    tweets = gt.search(A, intention_list[0][0])   ## A,Bを含むTweetの取得
    print(type(tweets))
    if len(tweets) == 0:
      print(A + "といえば、" + intention_list[0][0] + "についてどう思う？")
    else:
      twt_text = tweets[0].text
      print(twt_text)
    A = input()
  

if __name__=='__main__':
  file_name = "./MODELS/model_300.vec" 
  responce(file_name)
