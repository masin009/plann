# ==================== کد ربات (کاملاً آماده) ====================
import telebot
import random
import time

# توکن ربات خودت رو اینجا بذار
TOKEN = "8503188089:AAFUFcjoblYGMOso3YGZ8Tdu1daaFxQqk7M"  # این توکن توئه

bot = telebot.TeleBot(TOKEN)

# دیکشنری برای ذخیره کدها
user_codes = {}

@bot.message_handler(commands=['start'])
def send_code(message):
    user_id = message.chat.id
    user_name = message.from_user.first_name
    
    # تولید کد ۶ رقمی
    code = str(random.randint(100000, 999999))
    
    # ذخیره کد
    user_codes[user_id] = {
        'code': code,
        'time': time.time()
    }
    
    # پیام به کاربر
    bot.reply_to(message, f"""
✅ سلام {user_name} عزیز

🔐 کد تأیید شما: {code}

📌 این کد را در برنامه وارد کن
⏱ مدت اعتبار: ۱۰ دقیقه

@konkorkhabar
    """)

@bot.message_handler(func=lambda message: True)
def check_message(message):
    text = message.text
    
    # اگر کاربر کد فرستاد
    if len(text) == 6 and text.isdigit():
        user_id = message.chat.id
        
        if user_id in user_codes:
            saved_code = user_codes[user_id]['code']
            
            if text == saved_code:
                bot.reply_to(message, "✅ کد صحیح است! به برنامه خوش آمدید")
            else:
                bot.reply_to(message, "❌ کد اشتباه است")
        else:
            bot.reply_to(message, "❌ ابتدا /start را بزن")
    else:
        bot.reply_to(message, "برای دریافت کد /start را بزن")

print("🤖 ربات روشن شد...")
bot.polling()
