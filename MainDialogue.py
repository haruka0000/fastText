from gensim.models import word2vec
import Twitter as Tw
import Phrase
from datetime import datetime
import Html
import WordCalc
import Sentence
import random

global model

def responce(file_name, log_name): 
  # 学習済みモデルのロード
  model = word2vec.Word2Vec.load_word2vec_format(file_name, binary=False)
  
  input_text = input("You >>")
  
  f = open(log_name,'w')
  f.write("You,System;\n")
  f.write(input_text + ",")

  input_words = []
  input_words = Phrase.getNoun(input_text)
  
  while input_words == []:
    print("## ! ## 名詞を含む文章を再度入力してください")
    input_text = input("You >>")
    input_words = Phrase.getNoun(input_text)

  count = 0
  while True:
    intention_words = []

    try:
      print("[user]\t" + input_words[0])
      try:
        noun_log = open(log_name+".noun", 'a')
        noun_log.write("user," + input_words[0] + "\n")
        noun_log.close()
      except:
        print("Log Error")
      
      intention_words =  WordCalc.intention_calc(model, [input_words[0]], 0)
      print("[system]\t" + intention_words[0][0])
      try:
        noun_log = open(log_name+".noun", 'a')
        noun_log.write("system," + intention_words[0][0] + "\n")
        noun_log.close()
      except:
        print("Log Error 2")
    except:
      print("## Error ")

    try:
      ### テンプレートから文作成 ###
      pre_output_msgs = Sentence.replaceNouns(model, input_words[0], intention_words[0][0])
      print(pre_output_msgs)
      output_msg = pre_output_msgs[random.randint(0,len(pre_output_msgs))]

    except:
      ### Twitterから文作成 ###
      try:
        resp_msgs = Tw.getList(input_words[0], "")
        print("Got resp_msgs")

        exp_msgs = Tw.getList(intention_words[0][0], input_words[0])
        print("Got exp_msgs")

        #print(type(exp_msgs))
        if isinstance(resp_msgs, str):
          resp_msg = resp_msgs
        else:
          resp_msg = resp_msgs[count]
        if isinstance(exp_msgs, str):
          exp_msg = exp_msgs
        else:
          exp_msg = exp_msgs[count]
        output_msg = resp_msg + "\nそういえば、" + exp_msg

      except:
        output_msg = "それに関しては詳しくないです。今度勉強します。"

    print("\nSystem >>")
    print(output_msg + "\n")
    f.write(output_msg + ";\n")


    input_text = input("You >>")
    f.write(input_text + ",")
      
    input_words = Phrase.getNoun(input_text)
   
    '''
    # メモリに記憶
    for word in input_words:
      words_memory.append(word)

    # メモリにある単語が5を超えると、最新5単語のみ残す
    if len(words_memory) >= 5:
      words_memory = words_memory[-5:]
    '''

    # 終了コード
    if input_text == "さようなら。":
      print("\nSystem >>さようなら。")
      f.write("さようなら。;\n")
      break

  f.close()

  

if __name__=='__main__':
  now_time = datetime.now().strftime('%Y%m%d%H%M%S')
  file_name = "./MODELS/model_300.vec"
  log_name = "./LOG/" + now_time + ".log"
  html_name = "./LOG/design/" + now_time + ".html"
  responce(file_name, log_name)
  Html.LogToHtml(log_name, html_name)
