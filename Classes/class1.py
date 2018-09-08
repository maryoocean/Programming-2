import random

letters = 'abcdefghijklmnopqrstuvwxyz'
alphabet = [i for i in letters]
letter = random.choice(alphabet)
index = alphabet.index(letter) + 1
while 1:
    a_try = input('Введите строчную букву английского алфавита: ')
    if a_try in alphabet:
        if a_try == letter:
            print('Вы угадали!', letter)
            break
        elif a_try != letter:
            index_try = alphabet.index(a_try) + 1
            if index_try < index:
                print('Загаднная буква находится правее')
                continue
            else:
                print('Загаднная буква находится левее')
                continue
    else:
        print('Это не строчная буква английского алфавита, попробуйте снова')
        continue


