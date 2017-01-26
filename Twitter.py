import tweepy
import json
import datetime

# OAuth2.0用のキーを取得する
with open("secret.json") as f:
  secretjson = json.load(f)

# 各種キーをセット
CONSUMER_KEY = secretjson["consumer_key"]
CONSUMER_SECRET = secretjson["consumer_secret"]
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = secretjson["access_token"]
ACCESS_SECRET = secretjson["access_token_secret"]
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#APIインスタンスを作成
api = tweepy.API(auth)

# Twitter APIをPythonから操作するための準備完了
# print('Done!')

def search(word1, word2, option):
  search_template =  ' -https -http -rt -bot  min_faves:40'
  if option == 1:
    search_template =  ' -rt -bot  min_faves:30'
  if option == 2:
    search_template =  ' -rt -bot  min_faves:20'

  txt = word1 + " " + word2 + search_template
  search_result = api.search(q=txt, lang="ja", count=10)
  # いいね数の多い順にソート
  search_result = sorted(search_result, key=lambda t: t.favorite_count, reverse=True)
  
  print(api.rate_limit_status()['resources']['search']['/search/tweets'])

  return search_result

def getList(word1, word2):

  result = []
  for c in range(0,2):
    result = search(word1, word2, c)
    if result != []:
      break
  for c in range(0,2):
    print("１語検索中・・・")
    result = search(word1, "", c)
    if result != []:
      break

  if result != []:
    messages = []
    for r in result:
      # リンク・ハッシュタグ除去
      tmp_msg = r.text.split("http://")[0].split("https://")[0].split("#")[0]
      # リプライ除去
      if "@" in tmp_msg:
        tmp_msg = tmp_msg.split(" ")[1:]
      messages.append(tmp_msg)
  else:
    messages = "あまり詳しくない。"
  
  #print(api.rate_limit_status()['resources']['search']['/search/tweets'])
  
  return messages

if __name__ == "__main__":
  word1 = input("word 1 >>")
  word2 = input("word 2 >>")
  print(getList(word1, word2))
