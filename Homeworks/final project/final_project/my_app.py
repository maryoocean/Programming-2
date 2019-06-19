import flask
import telebot
import conf
from choose_sent_part import choose_sent
import os


TOKEN = os.environ["TOKEN"]

telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}
bot = telebot.TeleBot(TOKEN, threaded=False)

bot.remove_webhook()
bot.set_webhook(url="https://chekhontetg.herokuapp.com/bot")

app = flask.Flask(__name__)

correct = {}
sent_to_send = choose_sent()


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    user = message.chat.id
    bot.send_message(user, "Привет! Это бот, который предлагает \
угадать, оригинальное ли перед Вами предложение из произведения \
А. П. Чехова. \n\n Чтобы перестать угадывать, введите команду /stop.")
    play(user)


@bot.message_handler(commands=['stop'])
def goodbye(message):
    user = message.chat.id
    bot.send_message(user, 'Увидимся! Чтобы снова начать угадывать, \
воспользуйтесь командой /start.')


def play(user):
    sent_to_send = choose_sent()
    sent = list(sent_to_send.keys())
    c = sent_to_send[sent[0]]
    correct[user] = c
    kb = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Да, это Чехов!",
                                      callback_data="0")
    btn2 = types.InlineKeyboardButton(text="Здесь что-то не так...",
                                      callback_data="1")
    kb.add(btn1)
    kb.add(btn2)
    bot.send_message(user, sent, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def check_answer(call):
    user = call.message.chat.id
    answers(user, call.data, correct)


def answers(user, answer, correct):
    if int(answer) == int(correct[user]):
        bot.send_message(user, "Правильно!")
    else:
        bot.send_message(user, "Ой...")
    play(user)


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    user = message.chat.id
    bot.reply_to(message, "Я такого не знаю, но можно ввести /start \
и начать играть!")


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route('/bot', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
