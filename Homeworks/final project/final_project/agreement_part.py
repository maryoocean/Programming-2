def check_agreement(new_sent):
    m = MorphAnalyzer()
    punctuation = ')(,;:.«» ?!'
    words = new_sent[:-1].split(' ')
    for word_p in words:
        i = words.index(word_p)
        word = word_p.strip(')(,;:.«» ?!')
        if word != ' ' and word != '':
            ana = m.parse(word)
            w = ana[0]
            pos = w.tag.POS
            gender = w.tag.gender
            number = w.tag.number
            case = w.tag.case
            if pos == 'ADJF' or pos == 'ADJS':
                for k in range(i-1, i+2, 2):
                    try:
                        word_around = words[k]
                        word2 = word_around.strip(')(,;:.«» ?!')
                        ana_w2 = m.parse(word2)
                        w2 = ana_w2[0]
                        pos2 = w2.tag.POS
                        if pos2 == 'NOUN':
                            gender2 = w2.tag.gender
                            number2 = w2.tag.number
                            case2 = w2.tag.case
                            if number != number2 or gender2 != gender \
                               or case2 != case:
                                if gender2 is not None and number2 \
                                   is not None and case2 is not None:
                                    try:
                                        ana = m.parse(word)
                                        w = ana[0]
                                        w = w.inflect({gender2})
                                        w = str(w.word)
                                        w = m.parse(w)[0]
                                        w_number = w.inflect({number2})
                                        w = str(w_number.word)
                                        w_c = m.parse(w)[0]
                                        w_case = w_c.inflect({case2})
                                        w = str(w_case.word)
                                    except AttributeError:
                                        w = word
                                        continue
                                else:
                                    w = word
                                last_symbol = str(word_p[-1])
                                if last_symbol in punctuation:
                                    w += last_symbol
                                words.insert(i, w)
                                words.pop(i+1)
                    except IndexError:
                        continue
    sent = ' '.join(words)
    return sent
