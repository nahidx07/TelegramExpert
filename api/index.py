from flask import Flask, request
import telebot
import google.generativeai as genai
import os

# API Keys (Vercel Settings থেকে দেওয়া ভালো, অথবা এখানে সরাসরি দিন)
TELEGRAM_TOKEN = "8440131215:AAGSVHHWs25sehMnz7fyh8PCbVfAdRkBSdk"
GEMINI_KEY = "AIzaSyBRf9gTZzt6W4R9GNfc6NU91NpNnCaVVyE"

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Python Expert Bot is Alive!"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        # এখানে আপডেট হ্যান্ডেল করা হচ্ছে
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        return 'Invalid Request', 403

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! আমি Python Expert AI। আপনার কোড বা প্রশ্নটি লিখুন।")

@bot.message_handler(func=lambda message: True)
def handle_ai_request(message):
    try:
        prompt = f"You are a professional Python expert. Provide clean code or explanation for: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "AI এখন উত্তর দিতে পারছে না। পরে চেষ্টা করুন।")

# Vercel এর জন্য এক্সপোর্ট
def handler(request):
    return app(request)
    
