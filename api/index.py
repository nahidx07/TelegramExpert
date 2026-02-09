from flask import Flask, request
import telebot
import google.generativeai as genai
import os

# API Keys (Vercel Settings থেকে আসবে)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
API_KEY = os.environ.get('GEMINI_KEY')

# AI Setup - আমরা gemini-pro ব্যবহার করছি যা সব রিজিয়নে কাজ করে
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

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
    bot.send_message(message.chat.id, "হ্যালো! আমি Python Expert AI। আপনার প্রশ্নটি এখানে লিখুন।")

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        # AI জেনারেশন
        prompt = f"You are a professional Python expert. Help the user: {message.text}"
        response = model.generate_content(prompt)
        
        # রিপ্লাই দেওয়ার বদলে সরাসরি মেসেজ পাঠানো (Vercel এর জন্য নিরাপদ)
        bot.send_message(message.chat.id, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "দুঃখিত, আমি বর্তমানে উত্তর দিতে পারছি না। আপনার API Key চেক করুন।")

# Vercel handler
def handler(request):
    return app(request)
    
