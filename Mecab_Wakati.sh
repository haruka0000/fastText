#!/bin/sh

mecab -d /usr/lib/mecab/dic/mecab-ipadic-neologd -b 81920 -Owakati $1 -o $2
