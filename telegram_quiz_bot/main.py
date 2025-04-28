
from telebot import TeleBot, types
from messages import start_message, help_message
from quiz_data import quiz_data
from random import shuffle


TOKEN = '7957331136:AAFXsZSDRdKuVrw2zOPWi9e_gqnvWvtDu8Q'

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def greetings(message):
    bot.send_message(chat_id=message.chat.id, text=f'{message.from_user.first_name}, {start_message}')


@bot.message_handler(commands=['help'])
def help_information(message):
    bot.send_message(chat_id=message.chat.id, text=help_message)


question_index = 0
current_question = None
user = None
results = {}
correct_answers = 0


@bot.message_handler(commands=['start_quiz'])
def starting_quiz(message):
    bot.send_message(message.chat.id, "START! Время пошло!")
    send_message(message.chat.id)

    global user
    user = (f"{message.from_user.first_name}_{message.from_user.last_name}")
    results[user] = {'correct_answers': correct_answers}
    print(results)


def send_message(chat_id):

    global current_question

    try:
        current_question = quiz_data[question_index]

    except IndexError:
        bot.send_message(chat_id, "END! Викторина окончена!")
        print(results)

    if question_index < len(quiz_data):

        markup = types.InlineKeyboardMarkup(row_width=1)
        buttons = []

        shuffle(current_question['options'])
        for option in current_question['options']:

            btn = types.InlineKeyboardButton(text=option,
                                             callback_data=option
                                             )
            buttons.append(btn)

        markup.add(*buttons)
        bot.send_message(chat_id, current_question['question'], reply_markup=markup)


@bot.callback_query_handler()
def callback_handler(callback):

    if callback.data == current_question['correct_option']:

        results[user]['correct_answers'] += 1

        global correct_answers
        correct_answers += 1
        bot.answer_callback_query(
                    callback.id,
                    text=f"Вы ответили правильно! {results[user]['correct_answers']} из {len(quiz_data)}",
                    show_alert=True
                    )

    else:
        bot.answer_callback_query(
                    callback.id,
                    text=f"Вы ответили неправильно! "
                         f"Правильный ответ - {current_question['correct_option']}",
                    show_alert=True
                    )

    global question_index
    question_index += 1
    send_message(callback.message.chat.id)


bot.infinity_polling()











