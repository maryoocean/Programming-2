import random
import os
from pymorphy2 import MorphAnalyzer
from w2v_part import w2v
from inflection_part import inflection
from find_words_part import find_words
from agreement_part import check_agreement
from create_corpus import get_text, texts_file, get_urls


def change_sent():
    m = MorphAnalyzer()
    if os.path.exists('chekhov/texts_plain.txt'):
        with open('chekhov/texts_plain.txt', 'r', encoding="utf-8") as f:
            text = f.read()
            f.close()
    else:
        get_urls()
        with open('chekhov/texts_plain.txt', 'r', encoding="utf-8") as f:
            text = f.read()
            f.close()
    sentences = text.split('. ')
    for sent in sentences:
        print(sent)
        try:
            if sent[0] == ' ':
                sent = sent[1:]
            else:
                sent += '.'
        except IndexError:
            continue
        new_sent = ''
        words = sent.split(' ')
        for word_p in words:
            word = word_p.strip(')(,;:.«» ?!')
            # разбираем слово с помощью pymorphy
            if word != '' and word != ' ':
                ana = m.parse(word)
                w = ana[0]
                pos = w.tag.POS
                # выбираем, что будем менять
                if pos == 'NOUN':
                    # тэг для модели word2vec
                    pos = '_S'
                    new_word = find_words(w, pos, word_p)
                    if new_word is None:
                        new_word = word_p
                    new_sent += new_word + ' '
                elif pos == 'ADJF':
                    pos = '_A'
                    new_word = find_words(w, pos, word_p)
                    if new_word is None:
                        new_word = word_p
                    new_sent += new_word + ' '
                elif pos == 'ADVB':
                    pos = '_ADV'
                    new_word = find_words(w, pos, word_p)
                    if new_word == None:
                        new_word = word_p
                    new_sent += new_word + ' '
                # или добавляем слово в предложение, ничего не делая
                else:
                    new_sent += word_p + ' '
        sent2 = check_agreement(new_sent[:-1])
        sent2 = sent2.capitalize()
        # мы могли не найти нового слова – действительно ли мы изменили предложение?
        if sent2[:-1].lower() != sent.lower():
            with open('chekhov/texts_changed.txt', 'a', encoding="utf-8") as f:
                f.write(sent2 + '. ')
                f.close()
        else:
            with open('chekhov/texts_changed.txt', 'a', encoding="utf-8") as f:
                f.write('oops. ')
                f.close()
