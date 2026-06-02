from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("8885675155:AAGxMF1htzYDkhUAfeODqVh4P3Eo5i9woaM")
ADMIN_ID = os.getenv("8712902814")


def send_to_admin(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": ADMIN_ID,
            "text": text
        }
    )


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    message = data.get("message", {})
    text = message.get("text", "")

    user = message.get("from", {})
    user_id = user.get("id")
    username = user.get("username", "no_username")

    # 👇 ловим START
    if text == "/start":
        send_to_admin(
            f"🟢 Новый пользователь нажал START\n\n"
            f"ID: {user_id}\n"
            f"Username: @{username}"
        )

    return "ok"