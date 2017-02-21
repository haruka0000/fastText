import MeCab
import sys

def getNoun(s):
  # ipadicより精度の高いneologdを使うため辞書を指定
  m = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")
  
  # 改行コード毎に文字列を分割
  # EOSと最終行の改行を除去[:-2]
  lines = m.parse(s).split("\n")[:-2]
  words_dict = {}

  # タブ毎（名詞と品詞）に分割
  for l in lines:
    tmp = l.split("\t")
    words_dict[tmp[0]] = tmp[3]
  #print(words_dict)

  nouns_dict = {}
  # 名詞のみ抽出
  for word,word_class in words_dict.items():
    if "名詞" in word_class:
      nouns_dict[word] = word_class
  print(nouns_dict)
  if nouns_dict != {}:
    proper_nouns_dict = {}
    for noun,noun_detail in nouns_dict.items():
      if "固有名詞" in noun_detail:
        proper_nouns_dict[noun] = noun_detail
    print(proper_nouns_dict)
  
    input_nouns = []
    if proper_nouns_dict!= {}:
      input_nouns = list(proper_nouns_dict.keys())
    else:
      input_nouns = list(nouns_dict.keys())[::-1]
  else:
    input_nouns = []
  return input_nouns

if __name__ == '__main__':
  q = "本研究は話題の誘導に関する研究である。高橋が研究している。"
  print(q)
  print(getNoun(q))



