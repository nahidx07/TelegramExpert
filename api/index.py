from flask import Flask, request
import telebot
import google.generativeai as genai
import os

# API Keys
# মনে করে Vercel Settings > Environment Variables এ এগুলো দিয়ে দেবেন
TOKEN = os.environ.get('TELEGRAM_TOKEN', 'YOUR_TOKEN_HERE')
API_KEY = os.environ.get('GEMINI_KEY', 'YOUR_KEY_HERE')

# AI Setup
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN, threaded=False)

@app.route('/')
def home():
    return "Python Expert AI is running!"

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
    bot.reply_to(message, "হ্যালো! আমি Python Expert AI। আপনার কোড বা প্রশ্নটি এখানে লিখুন।")

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        response = model.generate_content(f"You are a Python expert. Answer this: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "দুঃখিত, এখন উত্তর দিতে পারছি না।")

# Vercel এর জন্য একদম সঠিক হ্যান্ডেলার পদ্ধতি
# এই অংশটুকু কোনো ফংশনের ভেতরে দেবেন না, একদম নিচে থাকবে।
app.debug = False
