import gensim
from pymorphy2 import MorphAnalyzer
import urllib.request
import logging

if 'model' not in locals():
    m = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)


def w2v(w, pos):
    w2 = ''
    if w in model:
        for i in model.most_similar(positive=[w], topn=10):
            # нас устроит только слово той же части речи
            if i[0].endswith(pos):
                w2 = i[0].split('_')[0]
                break
    else:
        # если слова нет в модели, и взять нам нечего: новое слово = старое
        w2 = w.split('_')[0]
    return w2
