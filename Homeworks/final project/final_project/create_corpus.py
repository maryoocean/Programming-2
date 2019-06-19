import re
import os
import urllib.request
from urllib.request import urlopen
import html
import bs4


def get_text(h_text):
    regText = re.compile('<blockquote>(.*?)<p \
align="center"><?s?m?a?l?l?>?<i>.*[0-9]', flags=re.DOTALL)
    text = regText.findall(h_text)[0]
    regTag = re.compile('<.*?>')
    text = str(regTag.sub('', text))
    regNewLine = re.compile('\n')
    text = regNewLine.sub('', text)
    lines = text.split('.')
    text = ''
    punctuation = '!—,=?'
    sentences = []
    for line in lines:
        # убираем реплики из диалогов и выбираем предложения подлиннее
        if len(line) > 50 and line[0] not in punctuation \
           and '!' not in line and '—' not in line and '?' not in line:
            sentences.append(line + '.')
    text = ''.join(sentences)
    return text


def texts_file(text):
    if not os.path.exists('chekhov/'):
            os.makedirs('chekhov')
    p = 'chekhov/texts_plain.txt'
    with open(p, 'a', encoding="utf-8") as f:
        f.write(text)


def get_urls():
    url = 'https://ostrovok.de/old/classics/chekhov/story%s.htm'
    url_page = 'https://ostrovok.de/old/classics/chekhov/'
    page = urlopen(url_page)
    h_page = page.read()
    s_page = str(BeautifulSoup(h_page, 'html5lib'))
    regURLs = re.compile('<a href="story(.*?)\.htm', flags=re.DOTALL)
    nums = sorted(regURLs.findall(s_page))[:40]  # возьмём 40 рассказов
    if len(nums) > 0:
        for num in nums:
            p = urlopen(url % num)
            html_p = p.read()
            s = str(BeautifulSoup(html_p, 'html5lib'))
            text = get_text(s)
            texts_file(text)
