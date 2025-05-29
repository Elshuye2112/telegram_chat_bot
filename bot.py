import os
import asyncio
import nest_asyncio  # 👈 ADD THIS

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from database import init_db, save_message,stats

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm your chat bot. Ask me anything!")


# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Try asking things like:\n- hello\n- how are you?\n- what is your name")


# Smart rule-based handler + Save to DB
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Unknown"

    await save_message(user_id, username, user_message)  # 🔁 Save message to DB

    # Rule-based response
    if "hello" in user_message:
        reply = "Hi there! 👋"
    elif "how are you" in user_message:
        reply = "I'm doing great! How about you? 😊"
    elif "your name" in user_message or "who are you" in user_message:
        reply = "I'm a custom Python Telegram bot."
    elif "bye" in user_message:
        reply = "Goodbye! Have a great day! 👋"
    elif "capital of ethiopia" in user_message:
        reply="Addis Ababa"
    elif "what is new" in user_message:
        reply = "🚀 I'm constantly learning new things to help you better!"

    else:
        reply = "🤔 I didn't understand that. Try 'hello', 'who are you', or 'how are you'."

    await update.message.reply_text(reply)


# Main bot startup
async def main():
    await init_db()  # ✅ Initialize DB

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats)) 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    await app.run_polling()


# Safe run with event loop patch
if __name__ == "__main__":
    nest_asyncio.apply()  # ✅ PATCH the running event loop
    asyncio.run(main())
