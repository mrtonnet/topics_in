##### aimldl > documents > surveys > embedding_in_nlp > README.md

## Embedding in Natural Language Processing

### Embedding in Japanese
Google search: japanese embedding

* [Japanese Word2Vec](https://github.com/philipperemy/japanese-words-to-vectors)
* [Word vectors for 157 languages](https://fasttext.cc/docs/en/crawl-vectors.html)
  * Pre-trained word vectors for 157 languages, trained on Common Crawl and Wikipedia using fastText.
  * For example, English. Korean, Japanese, and Chinese are all supported!
  * Tokenization
    * Chinese -> Stanford word segmenter
    * Japanese -> Mecab
    * Vietnamese -> UETsegmenter
    * For languages using the Latin, Cyrillic, Hebrew or Greek scripts -> the tokenizer from the Europarl preprocessing tools
    * For the remaining languages -> ICU tokenizer.
* [IDEA] Embedding with Aozora Bunko wasn't found from my short search result.
  * Google search: japanese embedding aozora

### MultiVec
[Github Repository: eske/multivec](https://github.com/eske/multivec)
* A Multilingual and Multilevel Representation Learning Toolkit for NLP
* C++ implementation of word2vec, bivec, and paragraph vector

## References
[Distributed Representations of Words and Phrases and their Compositionality](http://arxiv.org/abs/1310.4546), Mikolov et al. (2013)

[Distributed Representations of Sentences and Documents](http://arxiv.org/abs/1405.4053), Le and Mikolov (2014)

[Bilingual Word Representations with Monolingual Quality in Mind](http://stanford.edu/~lmthang/bivec/), Luong et al. (2015)

[Learning Distributed Representations for Multilingual Text Sequences](http://www.aclweb.org/anthology/W15-1512), Pham et al. (2015)

[BilBOWA: Fast Bilingual Distributed Representations without Word Alignments](http://arxiv.org/abs/1410.2455), Gouws et al. (2014)
