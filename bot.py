# bot.py - این فایل را در botfather ندهید، فقط برای راهنمایی است
import telebot
import random
import time

TOKEN = "8503188089:AAFUFcjoblYGMOso3YGZ8Tdu1daaFxQqk7M"
bot = telebot.TeleBot(TOKEN)

# دیکشنری برای ذخیره کدها
codes = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # تولید کد 6 رقمی
    code = str(random.randint(100000, 999999))
    
    # ذخیره کد با timestamp
    codes[message.chat.id] = {
        'code': code,
        'time': time.time()
    }
    
    # ارسال کد به کاربر
    bot.reply_to(message, f"🔐 کد تأیید شما: {code}\n\n"
                          f"این کد را در برنامه وارد کنید.\n"
                          f"⚠️ کد تا 10 دقیقه معتبر است.")

@bot.message_handler(func=lambda m: True)
def check_code(message):
    # اینجا می‌توانید کدهای ارسالی را بررسی کنید
    pass

# اجرای ربات
bot.polling()
