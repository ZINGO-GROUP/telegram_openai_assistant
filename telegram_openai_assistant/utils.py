# utils.py

import json
from pathlib import Path
import datetime
from .storage import send_to_other_bot  # storage.py dan send_to_other_bot import qilamiz

# Fayl yo'llari
message_count_file = Path("message_count.json")
qa_file = Path("questions_answers.json")

def get_message_count():
    """Joriy xabarlar sonini olish."""
    if not message_count_file.exists():
        return {"date": str(datetime.date.today()), "count": 0}
    with open(message_count_file) as file:
        return json.load(file)

def update_message_count(new_count):
    """Xabarlar sonini yangilash."""
    with open(message_count_file, 'w') as file:
        json.dump({"date": str(datetime.date.today()), "count": new_count}, file)

def save_qa(telegram_id, username, question, answer):
    """Savol va javoblarni saqlash va yuborish."""
    # JSON faylga saqlash
    if not qa_file.exists():
        with open(qa_file, 'w') as file:
            json.dump([], file)
    with open(qa_file, 'r+') as file:
        data = json.load(file)
        data.append({
            "telegram_id": telegram_id,
            "username": username,
            "question": question,
            "answer": answer
        })
        file.seek(0)
        json.dump(data, file, indent=4)
    
    # Ma'lumotlarni boshqa botga yuborish
    message = (
    f"✨ *Yangi savol-javob!* ✨\n\n"
    f"👤 *Foydalanuvchi:* @{username} id: ({telegram_id})\n"
    f"❓ *Savol:* {question}\n"
    f"💬 *Javob:* {answer}\n\n"
)

    send_to_other_bot(message)
