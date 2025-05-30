import os
import asyncio
import nest_asyncio  # 👈 ADD THIS

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from database import init_db, save_message,stats
import openai
from openai import OpenAI
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")
# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm your chat bot. Ask me anything!")


# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Try asking things like:\n- hello\n- how are you?\n- what is your name")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Unknown"

    await save_message(user_id, username, user_message)  # Save to DB

    # Rule-based responses
    if "hello" in user_message:
        reply = "Hi there! 👋"
    elif "how are you" in user_message:
        reply = "I'm doing great! How about you? 😊"
    elif "hi" in user_message:
        reply="Hi dear"
    elif "who are you" in user_message:
        reply="I'm a Elshaday , do you want more information? yes/no"
    elif "yes" in user_message:
        reply="Elshaday is a software engineer working at Berhan Bank as a software developer"
    elif "no" in user_message:
        reply="Thank you dear"
    elif "what is happeninig" in user_message:
        reply="Don't afried just communicate as a friend"
    elif "what is it" in user_message:
        reply="It is chating with a elshaday's telegram bot"
    elif "where are you" in user_message:
        reply="I'm arround you, dont't worry!!!"
    elif "who is elshaday" in user_message:
        reply="He is a software developer woriking Berhan Bank"
    elif "do you say Berhan bank" in user_message:
        reply="Yeah, Berhan bank is one of the bank institute in Ethiopia"
    elif "your role " in user_message:
        reply="I'm a system developer join the team recently"
    elif "your name" in user_message or "who are you" in user_message:
        reply = "I'm a custom Python Telegram bot."
    elif "capital of ethiopia" in user_message:
        reply="The capital of Ethiopia is Addis Ababa!"
    elif "how old are you" in user_message:
        reply="I am 28 years old "
    elif "What do you like" in user_message:
        reply="I like to visit new sites related to technology"
    elif "bye" in user_message:
        reply = "Goodbye! Have a great day! 👋"
    elif "what is it" in user_message:
        reply="These is the the telegram bot created by elshaday "
    else:
        # AI Fallback using OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ AI Error: {str(e)}"

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
