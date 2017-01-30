import sqlite3
import MeCab

dbname = 'database.db'

def insertTemplates(one_set_messages):
  conn = sqlite3.connect(dbname)
  c = conn.cursor()

  # テキストから１文毎に分割
  messages = one_set_messages.split(";\n")[:-1]
  messages = list(set(messages))  # 文の被りを無くす
  try:
    # executeメソッドでSQL文を実行する
    create_table = '''create table templates (id int primary key, msg text primaty key)'''
    c.execute(create_table)
  except:
    print("has table")

  select_sql = 'select * from templates'
  c.execute(select_sql)
  rows = c.fetchall()
  t_amount = len(rows)
  
  for i in range(0,len(messages)):
    try:
      sql = 'insert into templates (id, msg) values (?,?)'
      template = (i + t_amount + 1, messages[i])
      c.execute(sql, template)
      conn.commit()
      print(messages[i])
    except:
      print("おそらく既に登録されています！！")

  conn.close

def pickUpNouns():
  conn = sqlite3.connect(dbname)
  c = conn.cursor()

  # ipadicより精度の高いneologdを使うため辞書を指定
  m = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

  try:
    # executeメソッドでSQL文を実行する
    create_table = '''create table nouns (noun text, msg_id int)'''
    c.execute(create_table)
  except:
    print("has table")

  select_sql = 'select * from templates'
  c.execute(select_sql)
  rows = c.fetchall()
  for row in rows:
    lines = m.parse(row[1]).split("\n")[:-2]  # EOS と \n を省く
    for l in lines:
      w = l.split("\t")
      if "名詞" in w[3] and "記号" not in w[3]:
        try:
          sql = 'insert into nouns (noun, msg_id) values (?,?)'
          data = (w[0], row[0])
          c.execute(sql, data)
          conn.commit()
          print(w[0])
        except:
          print("ERROR")
    print(row[1])
  
  conn.close()


def deleteSigns():
  conn = sqlite3.connect(dbname)
  c = conn.cursor()

  m = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

  select_sql = 'select * from nouns'
  c.execute(select_sql)
  rows = c.fetchall()

  for row in rows:
    line = m.parse(row[0]).split("\n")[:-2]  # EOS と \n を省く
    w = line[0].split('\t')
    #print(w)
    if "名詞" not in w[3]:
      print(w)
      delete_sql = 'delete from nouns where noun="%s"' %(row[0])
      c.execute(delete_sql)
      conn.commit()

  conn.close()

if __name__=='__main__':

  f = open("replies.txt", "r")
  text = f.read()
  f.close
  insertTemplates(text)
  
  pickUpNouns()

  deleteSigns()
