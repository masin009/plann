# ==================== bot.py ====================
# این کد را در ربات تلگرام خود بگذارید
# ربات روی سرورهای تلگرام اجرا می‌شود، نیازی به سرور شما ندارد

import telebot
import random
import time

# توکن ربات خود را اینجا بگذارید
TOKEN = "8503188089:AAFUFcjoblYGMOso3YGZ8Tdu1daaFxQqk7M"
bot = telebot.TeleBot(TOKEN)

# کانال مورد نظر
CHANNEL_USERNAME = "@konkorkhabar"

# دیکشنری برای ذخیره کدها
codes = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_name = message.from_user.first_name
    
    # تولید کد 6 رقمی
    code = str(random.randint(100000, 999999))
    
    # ذخیره کد با timestamp
    codes[user_id] = {
        'code': code,
        'time': time.time(),
        'user': user_name
    }
    
    # پیام خوشامدگویی
    welcome_text = f"""
👋 سلام {user_name} عزیز
به ربات تأیید عضویت خوش آمدید

🔐 کد تأیید شما: {code}

📌 این کد را در برنامه وارد کنید
⏱ مدت اعتبار: 10 دقیقه

🆔 آیدی شما: {user_id}
    """
    
    bot.reply_to(message, welcome_text)
    
    # پیام به ادمین (اختیاری)
    print(f"کاربر جدید: {user_name} - کد: {code}")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
🤖 راهنمای استفاده:
برای دریافت کد تأیید، /start را بزنید

📌 کانال ما: @konkorkhabar
📌 برنامه: https://masin009.github.io/planb/

اگر مشکل دارید به ادمین پیام دهید
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['code'])
def send_code(message):
    # ارسال مجدد کد
    user_id = message.chat.id
    
    if user_id in codes:
        code_data = codes[user_id]
        # بررسی انقضا
        if time.time() - code_data['time'] < 600:  # 10 دقیقه
            bot.reply_to(message, f"🔐 کد شما: {code_data['code']}")
        else:
            # کد منقضی شده، کد جدید بده
            new_code = str(random.randint(100000, 999999))
            codes[user_id] = {
                'code': new_code,
                'time': time.time(),
                'user': message.from_user.first_name
            }
            bot.reply_to(message, f"🔄 کد جدید: {new_code}")
    else:
        bot.reply_to(message, "لطفاً اول /start را بزنید")

@bot.message_handler(func=lambda message: True)
def check_message(message):
    # بررسی اینکه آیا کاربر کد ارسال کرده؟
    text = message.text.strip()
    
    if len(text) == 6 and text.isdigit():
        user_id = message.chat.id
        
        if user_id in codes:
            saved_code = codes[user_id]['code']
            
            if text == saved_code:
                bot.reply_to(message, "✅ کد صحیح است! می‌توانید وارد برنامه شوید.")
                
                # اینجا می‌توانید کد را در دیتابیس ذخیره کنید
                print(f"✅ کاربر {user_id} با کد {text} تأیید شد")
            else:
                bot.reply_to(message, "❌ کد اشتباه است")
        else:
            bot.reply_to(message, "❌ ابتدا /start را بزنید")
    else:
        bot.reply_to(message, "لطفاً از دستورات استفاده کنید:\n/start - دریافت کد\n/help - راهنما")

# اجرای ربات
print("🤖 ربات در حال اجراست...")
bot.polling()
