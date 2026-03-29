import json
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters, JobQueue

from config import TOKEN, LOG_FILE, QUEUE_FILE

# =========================
# UTIL
# =========================

def save_log(text):
    with open(LOG_FILE, "a") as f:
        f.write(text + "\n")

def load_queue():
    if os.path.exists(QUEUE_FILE):
        try:
            return json.load(open(QUEUE_FILE))
        except:
            return []
    return []

def save_queue(q):
    with open(QUEUE_FILE, "w") as f:
        json.dump(q, f)

# =========================
# RECIBIR MENSAJES
# =========================

async def recibir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user
    msg = update.message.text

    line = f"{user.id}|{user.first_name}: {msg}"
    print("📩", line)

    save_log(line)

# =========================
# WORKER (JOB QUEUE)
# =========================

async def process_queue(context: ContextTypes.DEFAULT_TYPE):
    queue = load_queue()

    if not queue:
        return

    app = context.application

    new_queue = []

    for item in queue:
        try:
            await app.bot.send_message(
                chat_id=int(item["id"]),
                text=item["msg"]
            )
            print("✔ enviado:", item["id"])

        except Exception as e:
            print("❌ error:", e)
            new_queue.append(item)  # si falla, lo mantiene

    save_queue(new_queue)

# =========================
# MAIN
# =========================

def main():
    app = Application.builder().token(TOKEN).build()

    # recibir mensajes
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir))

    # job queue cada 1 segundo
    job_queue = app.job_queue
    job_queue.run_repeating(process_queue, interval=1, first=1)

    print("🤖 BOT ONLINE")

    app.run_polling()

if __name__ == "__main__":
    main()