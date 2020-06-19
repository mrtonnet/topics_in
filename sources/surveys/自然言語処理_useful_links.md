

## 自然言語処理 Useful Links
Resources for Japanese, https://aclweb.org/aclwiki/Resources_for_Japanese
National Institute for Japanese Language and Linguistics > Databases > Corpora
https://www.ninjal.ac.jp/english/database/type/corpora/

[Python による日本語自然言語処理](http://www.nltk.org/book-jp/ch12.html)

[自然言語処理における前処理の種類とその威力](https://qiita.com/Hironsan/items/2466fe0f344115aff177)
- This web article explains the preprocessing of NLP.
- It's worth spending time to read it to learn about preprocessing in Japanese.

[自然言語処理の前処理・素性いろいろ](http://yukinoi.hatenablog.com/entry/2018/05/29/120000)
- 前処理, 素性にするための処理, Python codes are summarized.
- This link is well-worth revisiting & studying.


### Google search
* 自然言語処理 python expand 短縮
* 自然言語処理 python contractions
  * -> 自然言語処理 python 縮約を 拡大する
  * -> 自然言語処理 python 縮約 拡大

[nlp - Pythonでの英語の縮約の拡大](https://tutorialmore.com/questions-742007.htm)

* 自然言語処理 python punctuations
  * いろいろな種類の句読点
* [自然言語（前）処理](https://qiita.com/dcm_sawayama/items/406408e8bda0840a8106)


[はじめての自然言語処理](https://www.ogis-ri.co.jp/otc/hiroba/technical/similar-document-search/part4.html)
第4回 spaCy/GiNZA を用いた自然言語処理
技術部 アドバンストテクノロジセンター 鵜野 和也 2019年8月27日

前回は BERT についてその概要と使い方を紹介しました。今回は自然言語処理ライブラリである spaCy と spaCy をフロントエンドとする日本語NLPライブラリの GiNZA について紹介します。

[文章データの単語数カウントやベクトル化の前処理の形態素解析／Python](https://arakan-pgm-ai.hatenablog.com/entry/2018/08/06/090000)

* python 日本語 句読点

[Python:日本語の句読点をトリガーにして改行コードを挿入する](https://www.amelt.net/imc/programming/python/5000/)
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# 句読点に、改行コードを追加
text = u"ハロー。ワールド。Pythonで句読点を扱う。"
text = text.encode('utf-8')
text = text.replace("。", "。" + os.linesep)
print text
"""
```

[文章を句点で分割する](https://teratail.com/questions/108738)
* 発生している問題・エラーメッセージ
* txt = '「君も車屋の猫だけに大分強そうだ。車屋にいると御馳走が食えると見えるね」'
sen = re.findall(r'.+?(?<=[。？])', txt)
print(sen) #-> ['「君も車屋の猫だけに大分強そうだ。']

となり、文末の一文を取りこぼしてしまいます。
自分が期待しているのは
['「君も車屋の猫だけに大分強そうだ。', '車屋にいると御馳走が食えると見えるね」']
です。
* No solution is suggested, but it's worth refering to this article.

[Pythonで文字列から全角や半角の記号を全て取り除く](http://naomichi-dev.hatenablog.com/entry/2017/11/21/215430)

```python
import unicode_script_map as usm
from unicode_script import ScriptType

test_str = "今日はボーリングに行ったー（＾∀＾）"
removed_str = "".join([c for c in test_str if usm.get_script_type(c) != ScriptType.U_Common or c == "\u30fc"])
print(removed_str)

#今日はボーリングに行ったー
```
