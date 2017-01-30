from gensim.models import word2vec
import sqlite3
import MeCab

dbname = 'database.db'

def getNouns():
  conn = sqlite3.connect(dbname)
  c = conn.cursor()

  select_sql = 'select * from nouns'
  c.execute(select_sql)
  
  rows = c.fetchall()
  conn.close()

  return rows


def getReplies(msg_id):
  conn = sqlite3.connect(dbname)
  c = conn.cursor()

  select_sql = 'select * from templates where id=%s' %(msg_id)
  c.execute(select_sql)
  
  rows = c.fetchall()
  conn.close()

  return rows



def getText(model, word1, word2):
  db_nouns = getNouns()

  similar_db_nouns = []

  for dn in db_nouns:
    try:
      if model.similarity(word1, dn[0]) > 0.5:
        similar_db_nouns.append(dn)
        print(dn)
    except:
      print("モデルに登録されていない文字\t" + dn[0])

  templates = []

  for sdn in similar_db_nouns:
    for r in getReplies(sdn[1]):
      templates.append(r[1])

  return similar_db_nouns, templates

  
def replaceNouns(model, word1, word2):
  result = getText(model, word1, word2)
  words = result[0]
  texts = result[1]

  print (texts)

  m = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

  changed_msg = []
  
  for t in texts:
    t_origin = t.replace(" ", "").replace("\n", "")
    tmp = t_origin
    nouns = []
    lines = m.parse(t).split("EOS")[0].split("\n")[:-1]
    #print("\n" + t)
    for line in lines:
      w = line.split("\t")
      #print(w)
      check = m.parse(w[0]).split("EOS")[0].split("\n")[0].split("\t")
      #print(check)
      if "名詞" in check[3]:
        nouns.append(check[0])
        #print("## checked\t" + check[0])
    
    if len(nouns) != 0:
      w1_nouns_list = []

      try:
        # word1に一番似ている単語を文章中から探す
        for n in nouns:
          w1_nouns_list.append([n, model.similarity(n, word1)])
        w1_nouns_list = sorted(w1_nouns_list, key=lambda x: x[1], reverse=True)
        #print(w1_nouns_list)
      except:
        print("## おそらく登録されていない名詞があります")
  
      try:
        w2_nouns_list = []
        # word2に一番似ている単語を文章中から探す
        for n in nouns:
          w2_nouns_list.append([n, model.similarity(n, word2)])
        w2_nouns_list = sorted(w2_nouns_list, key=lambda x: x[1], reverse=True)
      except:
        print("## おそらく登録されていない名詞があります")

      t_list = []
      if len(w1_nouns_list) != 0:
        word_class = []
        new_word_class = []
        mcb_lines = m.parse(t).split("EOS")[0].split("\n")
        for ml in mcb_lines:
          if ml != "":
            w = ml.split("\t")
            word_class.append([w[0],w[3]])
        
        #print(word_class)
        
        i = 0
        while i < len(word_class):
          tmp_word = word_class[i][0]
          i = i + 1 
          
          while True:
            if i >= len(word_class):
              break
            if "名詞" not in word_class[i][1]:
              break
            tmp_word = tmp_word + word_class[i][0]
            i = i + 1
          
          t_list.append(tmp_word)

        #print(t_list)
        for i in range(0,len(t_list)):
          if w1_nouns_list[0][0] == t_list[i]:
            t_list[i] = word1
          if w2_nouns_list[0][0] != w1_nouns_list[0][0]:
            if w2_nouns_list[0][0] == t_list[i]:
              t_list[i] = word2
          else:
            if len(w2_nouns_list) > 1:
              if w2_nouns_list[1][0] == t_list[i]:
                t_list[i] = word2

        tmp = "".join(t_list)

        print("------------------------------------------------------------")
        print([t_origin])
        print([tmp])

      '''
      if len(w1_nouns_list) != 0:
        tmp.replace(w1_nouns_list[0][0], word1) # word1 と word1に一番似ている単語 を入れ替える

        if w1_nouns_list[0][0] == w2_nouns_list[0][0]:
          if len(w2_nouns_list) != 1:
            tmp.replace(w2_nouns_list[1][0], word2) # word2 と word2に2番目に似ている単語 を入れ替える
        else:
          tmp.replace(w2_nouns_list[0][0], word2) # word2 と word2に一番似ている単語 を入れ替える

        new_noun = None
        print("\n" + t)

        for n in nouns:
          try:
            new_noun = model.most_similar(positive=[word1,n], negative=[w1_nouns_list[0][0]], topn=10)[0][0]
          except:
            print("## おそらく登録されていない名詞があります")
          if new_noun != None:
            try:
              tmp = tmp.replace(n, new_noun)
              print(n + "\t" + new_noun)
              print("#Changed " + tmp)
            except:
              print("## 置き換え済み")
      '''
    if t_origin != tmp:
      changed_msg.append(tmp)

  print("========================================================")
  for c in changed_msg:
    print(c)




if __name__=='__main__':
  file_name = "./MODELS/model_300.vec"
      
  # 学習済みモデルのロード
  model = word2vec.Word2Vec.load_word2vec_format(file_name, binary=False)
 
  word1 = "パソコン"
  word2 = "ディスプレイ"

  replaceNouns(model, word1, word2)
