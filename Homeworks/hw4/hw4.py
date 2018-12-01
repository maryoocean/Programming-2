from flask import Flask, url_for, render_template, request, redirect
import os
import csv
import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')


app = Flask(__name__)


filename = '/applications/data.csv'
fn_json = '/applications/data.json'


def add_csv(sex, age, edu_l, en, l, q1, q2, q3, q4, q5, q6, q7):
    if not os.path.exists('/applications/data.csv'):
        with open('/applications/data.csv', "w", encoding="utf-8") as f:
            f.write('sex,age,edu_level,eng,lang,Смеяться,Спрашивать,Школа,(Музыкальный) альбом,Фейсбук,Скучать,Youtube' + '\n')
            row = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'
            f.write(row % (sex, age, edu_l, en, l, q1, q2, q3, q4, q5, q6, \
                           q7) + '\n')
    else:
        with open('/applications/data.csv', "a", encoding="utf-8") as f:
            row = '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s'
            f.write(row % (sex, age, edu_l, en, l, q1, q2, q3, q4, q5, q6, \
                           q7) + '\n')


@app.route('/')
def index():
    if request.args:
        sex = request.args['sex'].lower()
        age = request.args['age'].lower()
        edu_level = request.args['edu_level'].lower()
        eng = request.args['eng'].lower()
        lang = request.args['lang'].lower()
        laugh = request.args['laugh'].split()[0].lower()
        ask = request.args['ask'].lower()
        school = request.args['school'].lower()
        album = request.args['album'].lower()
        FB = request.args['FB'].lower()
        miss = request.args['miss'].split()[0].lower()
        YouTube = request.args['YouTube'].lower()
        add_csv(sex, age, edu_level, eng, lang, laugh, ask, school, album, \
                FB, miss, YouTube)
    urls = {'Статистика ответов': url_for('statistics'),
                'Страница c JSON-данными': url_for('page_json'),
                'Страница поиска': url_for('search')}
    return render_template('index.html', urls=urls)


def my_dict(i, stats):
    my_d = {}
    overall = 0
    for line in stats:
        line = line.split(',')
        if line[i] in my_d:
            my_d[line[i]] += 1
            overall += 1
        else:
            my_d[line[i]] = 1
            overall += 1
    return my_d, overall


def bar_chart(sex, ppl):
    key_m = 'male'
    key_f = 'female'
    if key_m in sex and key_f in sex:
        Xm = [1]
        Xf = [2]
        M = sex[key_m]/ppl*100
        F = sex[key_f]/ppl*100
        plt.bar(Xm, M, color='b', label='мужчины')
        plt.bar(Xf, F, color='r', label='женщины')
    elif key_f not in sex:
        X = [1]
        Y = sex[key_m]/ppl*100
        plt.bar(X, Y, color='b', label='мужчины')
    elif key_m not in sex:
        X = [1]
        Y = sex[key_f]/ppl*100
        plt.bar(X, Y, color='r', label='женщины')
    plt.ylabel('в процентах')
    plt.title('Респонденты, принявшие участие в опросе')
    plt.legend()
    plt.savefig('/applications/static/ppl.jpg', dpi=300)


@app.route('/stats')
def statistics():
    if os.path.exists('/applications/data.csv'):
        with open('/applications/data.csv', 'r', encoding="utf-8") as f:
            stats = f.read().split('\n')[1:-1]
        sex, ppl = my_dict(0, stats)
        laugh, num = my_dict(5, stats)
        ask, num = my_dict(6, stats)
        miss, num = my_dict(10, stats)
        school, num = my_dict(7, stats)
        FB, num = my_dict(9, stats)
        YouTube, num = my_dict(11, stats)
        album, num = my_dict(8, stats)
        # bar_chart(sex, ppl)
        urls = {'Главная (анкета)': url_for('index'),
            'Страница поиска': url_for('search'),
            'Страница c JSON-данными': url_for('page_json')}
        return render_template('statistics.html', ask=ask, laugh=laugh, miss=miss, \
                               school=school, FB=FB, YouTube=YouTube, \
                               album=album, urls=urls)
    else:
        return redirect(url_for('index'))


@app.route('/search')
def search():
    urls = {'Главная (анкета)': url_for('index'),
            'Статистика ответов': url_for('statistics'),
            'Страница c JSON-данными': url_for('page_json')}
    return render_template('search.html', urls=urls)


@app.route('/results')
def results():
    no_res = 'Извините, у нас такого нет!'
    search = request.args['search']
    f = open(filename, 'r', encoding="utf-8")
    stats = f.read().split('\n')[1:-1]
    f.close()
    content = []
    if search == 'Поиск':
        eng_l = request.args['eng_l']
        for line in stats:
            line_spl = line.split(',')
            if eng_l == line_spl[3]:
                content.append(line_spl)
        res = len(content)
    elif search == 'Поиск по предлогу':
        prep = request.args['prep']
        for line in stats:
            line_spl = line.split(',')
            if prep in line_spl[5:12]:
                content.append(line_spl)
        res = len(content)
    urls = {'Главная (анкета)': url_for('index'),
            'Статистика ответов': url_for('statistics'),
            'Страница поиска': url_for('search'),
            'Cтраница с JSON-данными': url_for('page_json')}
    return render_template("results.html", content=content, no_res=no_res, \
                           res=res, urls=urls)


@app.route('/json')
def page_json():
    json_list = []
    i = 0
    f = open('/applications/data.csv', "r", encoding="utf-8")
    for line in csv.DictReader(f, delimiter=","):
        json_list.append((json.dumps(line, ensure_ascii=False, indent=4)))
    f_json = open('/applications/data.json', 'w', encoding="utf-8")
    f_json.write('[')
    for el in json_list:
        if i < len(json_list)-1:
            i += 1
            f_json.write(el + ',\n')
        else:
            f_json.write(el)
    f_json.write(']')
    f_json.close()
    f_json = open('/applications/data.json', 'r', encoding="utf-8")
    content = f_json.read().split('\n')
    f_json.close()
    urls = {'Главная (анкета)': url_for('index'),
            'Статистика ответов': url_for('statistics'),
            'Страница поиска': url_for('search')}
    return render_template("json.html", content=content, urls=urls)


if __name__=='__main__':
    app.run(debug=True)
