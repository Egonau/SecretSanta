import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import santaData

TELEGRAM_TOKEN = '5063146143:AAGkfGRB4MwOutD7mmyS6RdjWpMsjkHI8n0'
USERS_INFO = {}
USERS_STATUS = {}
USERS_CALLBACK = {}
bot = telebot.TeleBot(TELEGRAM_TOKEN)


def registration_start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Зарегистрироваться", callback_data="cb_register"))
    return markup


def registration_building_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 4
    markup.add(InlineKeyboardButton("Солянка", callback_data="cb_1"),
               InlineKeyboardButton("БХ", callback_data="cb_2"),
               InlineKeyboardButton("Ляля", callback_data="cb_3"),
               InlineKeyboardButton("Колобок", callback_data="cb_4"))
    return markup


def registration_accept_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Подтвердить регистрацию?", callback_data="cb_accept"))
    return markup


def main_menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Инфо", callback_data="cb_info"),
               InlineKeyboardButton("Чат", callback_data="cb_chat"),
               InlineKeyboardButton("Отправить подарок", callback_data="cb_send"))
    return markup


def info_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Назад", callback_data="cb_menu"))
    return markup


def chat_markup():
    markup = ReplyKeyboardMarkup(row_width=1)
    menu = KeyboardButton("Выйти")
    markup.add(menu)
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_register":
        bot.send_message(call.message.chat.id, "В каком здании ты учишься?",
                         reply_markup=registration_building_markup())
    elif call.data == "cb_1":
        bot.send_message(call.message.chat.id, "Далее", reply_markup=registration_accept_markup())
        USERS_INFO["{}".format(call.message.chat.id)]["building"] = "Солянка"
    elif call.data == "cb_2":
        bot.send_message(call.message.chat.id, "Далее", reply_markup=registration_accept_markup())
        USERS_INFO["{}".format(call.message.chat.id)]["building"] = "БХ"
    elif call.data == "cb_3":
        bot.send_message(call.message.chat.id, "Далее", reply_markup=registration_accept_markup())
        USERS_INFO["{}".format(call.message.chat.id)]["building"] = "Ляля"
    elif call.data == "cb_4":
        bot.send_message(call.message.chat.id, "Далее", reply_markup=registration_accept_markup())
        USERS_INFO["{}".format(call.message.chat.id)]["building"] = "Колобок"
    elif call.data == "cb_accept":
        santaData.users.insert_one(USERS_INFO["{}".format(call.message.chat.id)])
        bot.send_message(call.message.chat.id, "Успешно", reply_markup=main_menu_markup())
    elif call.data == "cb_info":
        # надо продумать, что писать
        bot.send_message(call.message.chat.id,
                         santaData.users.find_one({"id": "{}".format(call.message.chat.id)})["partner"],
                         reply_markup=info_markup())
    elif call.data == "cb_menu":
        bot.send_message(call.message.chat.id, "Главное меню", reply_markup=main_menu_markup())
    elif call.data == "cb_send":
        # надо продумать, что писать
        bot.send_message(call.message.chat.id,
                         santaData.users.find_one({"id": "{}".format(call.message.chat.id)})["partner"],
                         reply_markup=info_markup())
    elif call.data == "cb_chat":
        USERS_STATUS["{}".format(call.message.chat.id)]["chatting"] = True
        bot.send_message(call.message.chat.id, "Переписка началась", reply_markup=chat_markup())


@bot.message_handler(commands=['start'])
def message_handler(message):
    USERS_STATUS["{}".format(message.chat.id)] = {}
    USERS_STATUS["{}".format(message.chat.id)]["chatting"] = False
    try:
        bot.send_message(message.chat.id, santaData.users.find({"id": "{}".format(message.chat.id)}))
        bot.send_message(message.chat.id, "Главное меню", reply_markup=main_menu_markup())
    except Exception:
        USERS_INFO["{}".format(message.chat.id)] = {}
        USERS_INFO["{}".format(message.chat.id)]["id"] = "{}".format(message.chat.id)
        USERS_INFO["{}".format(message.chat.id)]["partner"] = "Undefined"
        bot.send_message(message.chat.id, "Участвуешь?", reply_markup=registration_start_markup())


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if USERS_STATUS["{}".format(message.chat.id)]["chatting"]:
        if message.text =="Выйти":
            USERS_STATUS["{}".format(message.chat.id)]["chatting"] = False
            bot.send_message(message.chat.id, "Выход из переписки", reply_markup=main_menu_markup())
        else:
            bot.send_message(santaData.users.find_one({"id": "{}".format(message.chat.id)})["partner"],message.text)



bot.infinity_polling()
