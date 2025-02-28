import telebot
import json
import os
import flask
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
app = flask.Flask(__name__)

# Baca dataset
DATASET_FILE = "dataset.json"
if not os.path.exists(DATASET_FILE):
    with open(DATASET_FILE, "w") as f:
        json.dump({}, f)

# Fungsi untuk membaca jadwal dari dataset
def load_schedule():
    with open(DATASET_FILE, "r") as f:
        return json.load(f)

# Fungsi untuk menyimpan jadwal ke dataset
def save_schedule(data):
    with open(DATASET_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Handle /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Sayangkuu. Gunakan /jadwal untuk melihat jadwal -- Gunakan /tambah untuk menambah jadwal.")

# Handle /jadwal
@bot.message_handler(commands=["jadwal"])
def get_schedule(message):
    data = load_schedule()
    day = message.text.split(" ", 1)[-1].capitalize()

    if day in data:
        jadwal = "\n".join(data[day]) if data[day] else "Tidak ada jadwal hari ini."
        bot.reply_to(message, f"Jadwal hari {day}:\n{jadwal}")
    else:
        bot.reply_to(message, "Format salah. Gunakan /jadwal [hari]")

# Handle tambah jadwal
@bot.message_handler(commands=["tambah"])
def add_schedule(message):
    try:
        _, day, time, subject = message.text.split(" ", 3)
        day = day.capitalize()
        data = load_schedule()

        if day not in data:
            data[day] = []
        data[day].append(f"{time} - {subject}")

        save_schedule(data)
        bot.reply_to(message, f"Jadwal {subject} pada {day} jam {time} telah ditambahkan!")
    except:
        bot.reply_to(message, "Format salah. Gunakan: /tambah [hari] [jam] [mata kuliah]")

# Handle webhook
@app.route("/", methods=["POST"])
def webhook():
    update = flask.request.get_data().decode("utf-8")
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://aed6-2001-448a-1090-ba1-90ca-3096-7c9d-2bce.ngrok-free.app")
    app.run(host="0.0.0.0", port=5000)
