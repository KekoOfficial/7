import json
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

from config import TOKEN, LOG_FILE

def save_log(text):
    with open(LOG_FILE, "a") as f:
        f.write(text + "\n")

async def recibir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user = update.effective_user
    msg = update.message.text

    line = f"[USER {user.id}] {user.first_name}: {msg}"
    print(line)

    save_log(line)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir))

    print("🤖 BOT ONLINE")
    app.run_polling()

if __name__ == "__main__":
    main()