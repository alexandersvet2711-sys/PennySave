from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("8885675155:AAGxMF1htzYDkhUAfeODqVh4P3Eo5i9woaM")
ADMIN_ID = os.getenv("8712902814")

@app.route("/")
def home():
    return "PennySave server is running"

@app.route("/notify", methods=["POST"])
def notify():

    data = request.json or {}

    user_id = data.get("id", "Неизвестно")
    name = data.get("name", "Неизвестно")

    text = (
        f"🟢 Пользователь открыл приложение\n\n"
        f"Имя: {name}\n"
        f"ID: {user_id}"
    )

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": ADMIN_ID,
            "text": text
        }
    )

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)