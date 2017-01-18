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
print('Done!')

def search(word1, word2):
  search_template =  '-http -https -# -「  min_faves:30'
  txt = word1 + " " + word2 + search_template
  search_result = api.search(q=txt, count=200)
  if search_result == []:
    txt = word2 + search_template
    search_result = api.search(q=txt, count=200)
    if search_result != []:
      result = search_result
    else:
      result = None
  else:
    result = search_result

  if result != None:
    message = result[0].text
    for r in result:
      if "？" in r.text:
        message = r.text
  else:
    message = "ちょっとよくわからないな。"

  #print(api.rate_limit_status()['resources']['search']['/search/tweets'])
  return message

if __name__ == "__main__":
  word1 = input("word 1 >>")
  word2 = input("word 2 >>")
  print(search(word1, word2))
  #for s in search(word1, word2):
    #print(s.text)
