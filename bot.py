import telebot
from telebot import types
import requests

TOKEN = "7903567004:AAEsRrhmP9Vk3oy5Kkv0KNaH4pUrolSkMQM"
CHANNEL = "@Dastyorim_grop"

bot = telebot.TeleBot(TOKEN)

# Har bir foydalanuvchi uchun bir martalik havola yaratish
def create_one_time_link():
    url = f"https://api.telegram.org/bot{TOKEN}/createChatInviteLink"
    data = {
        "chat_id": CHANNEL,
        "member_limit": 1  # bir martalik
    }
    r = requests.post(url, data=data)
    if r.status_code == 200:
        result = r.json()
        return result['result']['invite_link']
    else:
        return None

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton("Obuna bo'lish", callback_data="subscribe")
    btn2 = types.InlineKeyboardButton("Kanal haqida", callback_data="about_channel")
    btn3 = types.InlineKeyboardButton("Boshqa savol", url="https://t.me/Ilyas2002M")

    markup.add(btn1, btn2, btn3)

    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! Sizni nima qiziqtiradi?",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "subscribe":
        link = create_one_time_link()
        if link:
            bot.send_message(
                call.message.chat.id,
                f"Kanalga obuna bo‘lish uchun ushbu bir martalik havolani bosing:\n{link}"
            )
        else:
            bot.send_message(
                call.message.chat.id,
                "Havola yaratilmadi. Bot kanal admini bo‘lishi kerak!"
            )
        bot.answer_callback_query(call.id, "Obuna bo‘limi tanlandi ✅")

    elif call.data == "about_channel":
        bot.send_message(
            call.message.chat.id,
            "Ushbu kanal sizga semirish yoki ozishga yordam beradi ✅"
        )
        # Video yuborish
        try:
            with open("video.mp4", "rb") as video:
                bot.send_video(
                    call.message.chat.id,
                    video,
                    supports_streaming=True
                )
        except Exception as e:
            bot.send_message(call.message.chat.id, f"Video yuborilmadi: {e}")
        bot.answer_callback_query(call.id, "Kanal haqida bo‘limi tanlandi ✅")

bot.polling()
