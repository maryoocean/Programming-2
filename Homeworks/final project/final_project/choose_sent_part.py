import os
import random
from change_sent_part import change_sent


def choose_sent():
    sent_to_send = {}
    modify = ['0', '1']
    mod = random.choice(modify)
    if mod == 0:
        if os.path.exists('chekhov/texts_plain.txt'):
            with open('chekhov/texts_plain.txt', 'r', encoding="utf-8") as f:
                text_original = f.read()
                f.close()
        else:
            change_sent()
            with open('chekhov/texts_plain.txt', 'r', encoding="utf-8") as f:
                text_original = f.read()
                f.close()
        sentences = text_original.split('. ')
        sent = random.choice(sentences)
        sent += '.'
        sent_to_send[sent] = mod
    else:
        if os.path.exists('chekhov/texts_changed.txt'):
            with open('chekhov/texts_changed.txt', 'r', encoding="utf-8") as f:
                text_changed = f.read()
                f.close()
        else:
            change_sent()
            with open('chekhov/texts_changed.txt', 'r', encoding="utf-8") as f:
                text_original = f.read()
                f.close()
        sentences = text_changed.split('. ')
        sent = random.choice(sentences)
        sent += '.'
        sent_to_send[sent] = mod
    return sent_to_send
