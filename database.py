import sqlite3
from telegram import Update
from telegram.ext import ContextTypes
DB_PATH = "chatbot.db"

async def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized.")


async def save_message(user_id: int, username: str, message: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (user_id, username, message)
        VALUES (?, ?, ?)
    """, (user_id, username, message))
    conn.commit()
    conn.close()
    print(f"💾 Saved message: {username} ({user_id}) - {message}")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, COUNT(*) FROM messages GROUP BY username ORDER BY COUNT(*) DESC")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        response = "\n".join([f"{username or 'Unknown'}: {count} messages" for username, count in rows])
    else:
        response = "No data yet."

    await update.message.reply_text(response)