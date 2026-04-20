import telebot
from telebot import types

bot = telebot.TeleBot("7905042865:AAEIixNipcHtK4XTd7Uj3tLTnuJNsxI_2yo")

ADMIN_ID = 7659443417

user_map = {}


# --- старт ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("Перейти на наш сайт")
    markup.row("Поддержка", "Профиль")
    markup.add("Донат")

    bot.send_message(
        message.chat.id,
        "Hello! This is store bot 'SkyFly Shops'\nEmail - SkyFLyStorea@gmail.com",
        reply_markup=markup
    )


# --- сайт ---
@bot.message_handler(func=lambda m: m.text == "Перейти на наш сайт")
def site(message):
    bot.send_message(message.chat.id, "https://google.com")


# --- ПОДДЕРЖКА (ТОЛЬКО ВХОД) ---
@bot.message_handler(func=lambda m: m.text == "Поддержка")
def support(message):
    msg = bot.send_message(message.chat.id, "Опишите проблему")
    bot.register_next_step_handler(msg, send_to_admin)


# --- отправка админу ---
def send_to_admin(message):
    sent = bot.send_message(
        ADMIN_ID,
        f"User ID: {message.chat.id}\n"
        f"Username: @{message.from_user.username}\n\n"
        f"{message.text}"
    )

    user_map[sent.message_id] = message.chat.id

    bot.send_message(message.chat.id, "Отправлено в поддержку")


@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.reply_to_message)
def admin_reply(message):
    replied_id = message.reply_to_message.message_id

    if replied_id in user_map:
        user_id = user_map[replied_id]

        bot.send_message(
            user_id,
            f"Поддержка:\n{message.text}"
        )

        bot.send_message(
            ADMIN_ID,
            f"Ваше сообщение:\n{message.text}\nУспешно доставлено!"
        )


bot.infinity_polling()
