from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = "8885675155:AAGxMF1htzYDkhUAfeODqVh4P3Eo5i9woaM"
ADMIN_ID = "8712902814"


def send_to_admin(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": ADMIN_ID,
            "text": text
        }
    )


@app.route("/")
def home():
    return "Bot is running"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json or {}

    message = data.get("message") or {}

    text = message.get("text", "")
    chat_id = str(message.get("chat", {}).get("id", ""))

    # ==========================
    # ОТВЕТ АДМИНА ПОЛЬЗОВАТЕЛЮ
    # ==========================
    if chat_id == ADMIN_ID:

        reply_to = message.get("reply_to_message")

        if reply_to and text:

            original_text = reply_to.get("text", "")

            if "ID:" in original_text:

                try:
                    target_id = original_text.split("ID:")[1].split("\n")[0].strip()

                    requests.post(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        json={
                            "chat_id": target_id,
                            "text": text
                        }
                    )

                    send_to_admin("✅ Ответ отправлен")

                except Exception as e:
                    send_to_admin(f"❌ Ошибка: {e}")

        return "ok"

    # ==========================
    # ДАННЫЕ ПОЛЬЗОВАТЕЛЯ
    # ==========================
    user = message.get("from") or {}

    user_id = user.get("id")
    username = user.get("username", "no_username")
    first_name = user.get("first_name", "")

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ==========================
    # START
    # ==========================
    if text == "/start":

        send_to_admin(
            f"🟢 Новый пользователь\n\n"
            f"ID: {user_id}\n"
            f"Username: @{username}\n"
            f"Имя: {first_name}\n"
            f"Время: {time_now}"
        )

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": user_id,
                "text": "Добро пожаловать!"
            }
        )

        return "ok"

    # ==========================
    # ЛЮБОЕ СООБЩЕНИЕ
    # ==========================
    if text:

        send_to_admin(
            f"📩 Сообщение от пользователя\n\n"
            f"ID: {user_id}\n"
            f"Username: @{username}\n"
            f"Имя: {first_name}\n\n"
            f"{text}"
        )

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
