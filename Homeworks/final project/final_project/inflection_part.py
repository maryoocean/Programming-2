from w2v_part import w2v
import pymorphy2
from pymorphy2 import MorphAnalyzer


def inflection(w, pos):
    m = MorphAnalyzer()
    lex = str(w.normal_form)
    """ Запоминаем, какие тэги были у исходного слова.
    Берём тэги после пробела, потому что до пробела пишется род,
    а рода исходного слова и близкого ему могут не совпадать."""
    if pos != "_ADV":
        tags = str(w.tag).split(' ')[1]
    else:
        tags = str(w.tag)
    w = lex + pos
    # ищем близкое слово с помощью word2vec
    w2 = w2v(w, pos)
    w2 = m.parse(w2)[0]
    # достаем все форма нашего нового слова
    all_lex = w2.lexeme
    for l in all_lex:
        # пробуем найти такуюже форму слова
        try:
            if pos != "_ADV":
                tags_l = str(l.tag).split(' ')[1]
            else:
                tags_l = str(l.tag)
            if tags == tags_l:
                w2 = str(l.word)
                break
        # например, у слова нет формы множественного числа
            else:
                w2 = None
        # если pymorphy не умеет склонять слово
        except IndexError:
            w2 = None
    return w2
