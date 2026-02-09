from flask import Flask, request
import telebot
import google.generativeai as genai
import os

# আপনার API Key গুলো এখানে দিন (অথবা Vercel Environment Variables এ সেট করুন)
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GEMINI_KEY = "YOUR_GEMINI_API_KEY"

# AI কনফিগারেশন
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Python Expert Bot is Running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Invalid Request', 403

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! আমি Python Expert AI। আপনার কোডিং সমস্যাটি এখানে লিখুন।")

@bot.message_handler(func=lambda message: True)
def handle_ai_request(message):
    user_query = message.text
    try:
        # AI জেনারেশন
        prompt = f"You are a Python Expert. Professional coding assistant. Query: {user_query}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, "দুঃখিত, একটু সমস্যা হয়েছে। আবার চেষ্টা করুন।")

# Vercel এর জন্য অ্যাপ এক্সপোর্ট
def handler(request):
    return app(request)
    
