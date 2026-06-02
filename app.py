from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# 🔑 ВСТАВЬ В PYTHONANYWHERE → Web → Environment variables
BOT_TOKEN = "8885675155:AAGxMF1htzYDkhUAfeODqVh4P3Eo5i9woaM"
ADMIN_ID = "8712902814"


# 📩 отправка тебе в Telegram
def send_to_admin(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": ADMIN_ID,
            "text": text
        }
    )


# 🌐 webhook от Telegram
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}

    print("INCOMING:", data)  # 👈 для проверки в логах

    message = data.get("message") or data.get("edited_message") or {}

    text = message.get("text", "")

    user = message.get("from") or {}
    user_id = user.get("id")
    username = user.get("username", "no_username")

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 👇 ловим старт
    if text == "/start":
        send_to_admin(
            f"🟢 Новый пользователь в боте\n\n"
            f"👤 Username: @{username}\n"
            f"🆔 ID: {user_id}\n"
            f"⏰ Время: {time_now}"
        )

    return "ok"


# 🧪 тест чтобы проверить сервер
@app.route("/")
def home():
    return "Bot is running"