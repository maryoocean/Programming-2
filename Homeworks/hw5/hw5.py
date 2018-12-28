import sqlite3
import os.path
import re
from flask import Flask
from flask import url_for, render_template, request, redirect


app = Flask(__name__)


def create_db():
    with open('desktop/newspaper/csv-table.csv', encoding='utf-8') as f:
        data = f.read().split('\n')[1:11]
        # в корпусе я оставила всего 10 первыйх статей
    conn = sqlite3.connect('newspaper.db')
    c = conn.cursor()
    # создаём БД
    c.execute("CREATE TABLE IF NOT EXISTS newspaper(header text, \
                source text, plain_text text, mystem_text)")
    # при большем объёме у меня всё очень долго работало
    for row in data[:4]:
        cells = row.split('\\t')
        path_text = 'desktop/' + cells[0]
        # просто текст
        with open(path_text, 'r', encoding="utf-8") as f:
            plain_t = f.read().replace(u'\xa0', u' ')
        # название статьи и ссылка на неё
        regTitle = re.compile('@ti(.*?)\n')
        regLink = re.compile('@url(.*?)\n')
        title = regTitle.findall(plain_t)[0]
        url = regLink.findall(plain_t)[0]
        # путь к файлам, размеченным mystem, отличается только названием папки
        path_mystem = path_text.replace('plain', 'mystem-plain')
        # размеченный текст
        with open(path_mystem, encoding="utf-8") as f:
            mystem_t = f.read().replace(u'\xa0', u' ').replace('\n', '')
        # добавляем всё в БД
        c = conn.cursor()
        c.execute('INSERT INTO newspaper VALUES (?, ?, ?, ?)', \
                  (title, url, plain_t, mystem_t))
        conn.commit()


create_db()


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/results')
def results():
    conn = sqlite3.connect('newspaper.db')
    c = conn.cursor()
    search = request.args['words']
    """ наверное, лемматизация ввода пользователя сделано очень длинно и можно
        было иначе, но я придумала только так """
    with open('desktop/words.txt', 'w', encoding="utf-8") as f:
        f.write(search)
    os.system("/applications/mystem -lcgid --eng-gr \
                desktop/words.txt desktop/words_ms.txt")
    with open('desktop/words_ms.txt', 'r', encoding="utf-8") as f:
        words = f.read().split('} ')
    for word in words:
        # название статьи и ссылку на неё буду складывать в словарь d_meta
        d_meta = {}
        # в словарь text_art положу названи статьи и текст
        text_art = {}
        regGram = re.compile('[а-я]{1,100}=[A-Z]{1,4}')
        req = re.findall(regGram, word)[0]
        search_req = '%' + req + '%'
        conn = sqlite3.connect("newspaper.db")
        c = conn.cursor()
        c.execute("SELECT * FROM newspaper WHERE mystem_text LIKE ?", \
                  [search_req])
        for row in iter(c.fetchone, None):
            ti = row[0].strip()
            link = row[1].strip()
            text = row[2]
            d_meta[ti] = link
            text = str(text).strip('(),\'')
            sentences = text.split('\n')[5:]
            # первые строчки - это метаданные для корпуса, поэтому [5:]
            article = (' '.join(sentences))
            if len(article) >= 100:
                sent = article.split()
                to_print = ''
                i = 0
                while len(to_print) < 100:
                    to_print += sent[i] + ' '
                    i += 1
                    text_art[ti] = to_print
                to_print = to_print.strip()
                to_print += "..."
                text_art[ti] = to_print
            else:
                text_art[ti] = article
            """ в моих словарях ключи -- это названия статей, они уникальны.
                поэтому печатать текст я буду только при совпадении названия"""
        return render_template('results.html', d_meta=d_meta, text_art=text_art)


if __name__=='__main__':
    app.run(debug=False)
