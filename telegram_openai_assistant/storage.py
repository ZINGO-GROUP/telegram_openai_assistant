# storage.py

import json
import requests
from .config import second_bot_token, send_chat_id
from pathlib import Path

qa_file = Path("questions_answers.json")

# Boshqa botning API tokeni va chat ID'si
OTHER_BOT_TOKEN = second_bot_token
OTHER_BOT_CHAT_ID = send_chat_id

# Faylni yaratish
if not qa_file.exists():
    with open(qa_file, "w") as file:
        json.dump([], file)

def send_to_other_bot(message):
    """Ma'lumotni boshqa botga yuboradi."""
    url = f"https://api.telegram.org/bot{OTHER_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": OTHER_BOT_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Xatolik: {response.content.decode()}")
    except Exception as e:
        print(f"Xabar yuborishda xato: {e}")


def save_qa(telegram_id, username, question, answer):
    """Savol va javoblarni faylga saqlaydi va boshqa botga yuboradi."""
    # Faylga saqlash
    with open(qa_file, "r+") as file:
        data = json.load(file)
        entry = {
            "telegram_id": telegram_id,
            "username": username,
            "question": question,
            "answer": answer
        }
        data.append(entry)
        file.seek(0)
        json.dump(data, file, indent=4)
    
    # Yangi ma'lumotni boshqa botga yuborish
    message = (
    f"✨ *Yangi savol-javob!* ✨\n\n"
    f"👤 *Foydalanuvchi:* @{username} id: ({telegram_id})\n"
    f"❓ *Savol:* {question}\n"
    f"💬 *Javob:* {answer}\n\n"
    f"🔄 *Yana savollar kutib qolamiz!* 🚀"
)

    send_to_other_bot(message)
