# sample fastText

### Wikipediaデータのダウンロード
https://dumps.wikimedia.org/jawiki/

### WikiExtractor
https://github.com/attardi/wikiextractor
>$ python wikiextractor/WikiExtractor.py -b 500M -o (出力先フォルダ) jawiki-xxxxxxxx-pages-articles-multistream.xml.bz2

### 分かち書き
>$ mecab (対象テキストファイル) -O wakati -o (出力先ファイル)

### 辞書　mecab-neologd
https://github.com/neologd/mecab-ipadic-neologd

### fastText
https://github.com/facebookresearch/fastText
