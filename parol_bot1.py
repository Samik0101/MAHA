import telebot
from telebot import types
import random
import time
import threading

# ——— KONFIGURATSIYA ———
TOKEN         = '7746162082:AAHLYTP6PXlVcZ1GBeIOHpMgqUHUtvDj8ls'
PASSWORDS     = ['Samik_1923.', 'Samandar20061917']
CHANNEL_LINK  = 'https://t.me/+0lMkuMQvxpg1MTFi'

bot = telebot.TeleBot(TOKEN)

# Xato xabarlar
ERROR_MESSAGES = [
    "Yo‘q!", "Ket!", "Sen Samandar emassan!", "Xato!",
    "Botdan chiq!", "Bekorchi!", "Hali emas!", "Qayta urinib ko‘r!"
]

# Asosiy menyu
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add("🔐 Kanalga kirish")
    return kb

# Xabarni o'chirish funksiyasi
def safe_delete(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

# /start komandasi
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(
        message.chat.id,
        "👋 Salom! Kanalga kirish uchun parolni kiriting yoki menyudan tanlang:",
        reply_markup=main_menu()
    )

# Kanalga kirish uchun parol so'rash
@bot.message_handler(func=lambda m: m.text == "🔐 Kanalga kirish")
def ask_password(message):
    msg = bot.send_message(
        message.chat.id,
        "🔑 Parolni kiriting:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, check_password)

# Parolni tekshirish
def check_password(message):
    chat_id = message.chat.id
    pwd = message.text.strip()
    # Parolni tekshirib, xabarni o'chiramiz
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass

    if pwd in PASSWORDS:
        # To'g'ri parol: kanal havolasi yuboriladi
        sent = bot.send_message(
            chat_id,
            f"📢 Kanal havolasi:\n{CHANNEL_LINK}",
            reply_markup=main_menu()
        )
        # 1 daqiqadan keyin havolani o'chirish
        threading.Timer(60.0, lambda: safe_delete(chat_id, sent.message_id)).start()
        
    else:
        # Noto‘g‘ri parol: random xato xabarlar yuboriladi
        cnt = random.randint(3, 5)
        sample = random.sample(ERROR_MESSAGES, cnt)
        for err in sample:
            bot.send_chat_action(chat_id, 'typing')
            time.sleep(0.5)
            sent = bot.send_message(chat_id, err)
            # 1 daqiqadan keyin xato xabarni o'chirish
            threading.Timer(60.0, lambda: safe_delete(chat_id, sent.message_id)).start()
        
        # Menyuni qayta tiklash
        bot.send_message(
            chat_id,
            "❗ Parol noto‘g‘ri. Qayta urinib ko‘ring:",
            reply_markup=main_menu()
        )
        # 1 daqiqadan keyin xato xabarni o'chirish
        threading.Timer(60.0, lambda: safe_delete(chat_id, sent.message_id)).start()

if __name__ == '__main__':
    bot.infinity_polling()
