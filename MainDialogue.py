from gensim.models import word2vec
import GetTweets as GT
import TextDivider as TD
from datetime import datetime
import MakeHtml as MH

global model

def responce(file_name, log_name): 
  # 学習済みモデルのロード
  model = word2vec.Word2Vec.load_word2vec_format(file_name, binary=False)
  
  input_text = input("You >>")
  
  f = open(log_name,'w')
  f.write("You,System;\n")
  f.write(input_text + ",")

  start = TD.getNoun(input_text)
  A = start
  goal = "徳島"
  #B = goal

  while True:
    intention_list = []

    # Aの類似語を集める　類似度順にソート
    similar_words = model.most_similar(positive=A, negative=[], topn=100)
    similar_words.sort(key=lambda x: float(x[1]), reverse=True)
    
    #similar_words = similar_words[:10]

    for s in similar_words:
      # 各類似語とゴールとの類似度の比較
      intention_list.append((s[0],model.similarity(goal,s[0])))
    
    intention_list.sort(key=lambda x: float(x[1]), reverse=True)
    #print(intention_list)
    
    '''
    print("\n単語\t" + goal + "との類似度")
    for il in intention_list:
      print(il[0] + "\t" + str(il[1]))
    
    print("=======================================================")
    print("「" + intention_list[0][0] + "」")
    '''
    tweet_text = GT.search(A[0], " ")
    print("\nSystem >>")
    tweet_text = tweet_text + "\nそういえば、" + GT.search(A[0], intention_list[0][0])
    print(tweet_text + "\n")
    f.write(tweet_text + ";\n")

    input_text = input("You >>")
    f.write(input_text + ",")

    if input_text == "さようなら":
      print("\nSystem >>さようなら")
      f.write("さようなら;\n")
      break
    
    A = TD.getNoun(input_text)
  f.close()

  

if __name__=='__main__':
  now_time = datetime.now().strftime('%Y%m%d%H%M%S')
  file_name = "./MODELS/model_300.vec"
  log_name = "./LOG/" + now_time + ".log"
  html_name = "./LOG/design/" + now_time + ".html"
  responce(file_name, log_name)
  MH.LogToHtml(log_name, html_name)
