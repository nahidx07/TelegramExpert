from flask import Flask, request
import telebot
import google.generativeai as genai
import os

# API Keys (Vercel Environment Variables থেকে আসবে)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
API_KEY = os.environ.get('GEMINI_KEY')

# AI Setup - 'gemini-1.5-flash-latest' অথবা 'gemini-pro' ব্যবহার করুন
genai.configure(api_key=API_KEY)
# মডেল নাম আপডেট করা হয়েছে
model = genai.GenerativeModel('gemini-1.5-flash-latest')

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN, threaded=False)

@app.route('/')
def home():
    return "Python Expert AI is online!"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Forbidden', 403

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "হ্যালো! আমি Python Expert AI। আপনার পাইথন কোড বা প্রশ্নটি এখানে লিখুন।")

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    chat_id = message.chat.id
    user_text = message.text

    try:
        # AI জেনারেশন
        prompt = f"You are a professional Python expert. Provide solution for: {user_text}"
        response = model.generate_content(prompt)
        
        # 'reply_to' এর বদলে সরাসরি 'send_message' ব্যবহার করা নিরাপদ
        bot.send_message(chat_id, response.text)
        
    except Exception as e:
        print(f"Error: {e}")
        # যদি gemini-1.5-flash কাজ না করে তবে ব্যাকআপ হিসেবে gemini-pro ট্রাই করা
        try:
            backup_model = genai.GenerativeModel('gemini-pro')
            response = backup_model.generate_content(user_text)
            bot.send_message(chat_id, response.text)
        except:
            bot.send_message(chat_id, "দুঃখিত, এআই মডেলটি এই মুহূর্তে রেসপন্স করছে না। দয়া করে আপনার Gemini API Key চেক করুন।")

# Vercel handler
def handler(request):
    return app(request)
    
