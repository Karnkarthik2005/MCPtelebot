import logging
import sqlite3
from datetime import datetime
from telegram import Update, ChatPermissions, ChatAction
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, CallbackContext, JobQueue
)

# Enable logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token (Replace with your bot's token)
TOKEN = "YOUR_BOT_TOKEN"
DB_PATH = "telegram_user_history.db"

# Storage
user_data_store = {}
group_rules = "Welcome to the group! Follow the rules."
scheduled_messages = []
BAD_WORDS = ["badword1", "badword2", "offensiveword"]


# Initialize Database
def init_db():
    """Create the database table if it does not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        field VARCHAR NOT NULL,
        old_value VARCHAR,
        new_value VARCHAR,
        changed_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()


def store_change(user_id, field, old_value, new_value):
    """Store name changes in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO user_history (user_id, field, old_value, new_value, changed_at)
    VALUES (?, ?, ?, ?, ?);
    """, (user_id, field, old_value, new_value, datetime.now()))
    conn.commit()
    conn.close()


async def track_name_changes(update: Update, context: CallbackContext) -> None:
    """Detect and log name changes."""
    user = update.effective_user
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT new_value FROM user_history WHERE user_id = ? AND field = 'name' ORDER BY changed_at DESC LIMIT 1;", (user.id,))
    result = cursor.fetchone()
    old_name = result[0] if result else None
    new_name = user.full_name

    if old_name and old_name != new_name:
        store_change(user.id, "name", old_name, new_name)
        await update.message.reply_text(f"⚠ **User {old_name} changed their name to {new_name}!**")

    conn.close()


async def get_user_info(update: Update, context: CallbackContext) -> None:
    """Get user info using /info @username"""
    if not context.args:
        await update.message.reply_text("⚠ Usage: `/info @username`")
        return

    username = context.args[0].strip("@")
    try:
        user = await context.bot.get_chat(username)
        message = f"👤 **User Info:**\n🆔 ID: `{user.id}`\n👤 Name: {user.full_name}\n📛 Username: @{user.username}\n"
        await update.message.reply_text(message, parse_mode="Markdown")
    except:
        await update.message.reply_text("⚠ User not found!")


async def get_profile_picture(update: Update, context: CallbackContext) -> None:
    """Fetch user profile picture with /getpfp @username"""
    if not context.args:
        await update.message.reply_text("⚠ Usage: `/getpfp @username`")
        return

    username = context.args[0].strip("@")
    try:
        user = await context.bot.get_chat(username)
        photos = await context.bot.get_user_profile_photos(user.id)
        if photos and photos.total_count > 0:
            await update.message.reply_photo(photo=photos.photos[0][-1].file_id, caption=f"👤 Profile Picture of {user.full_name}")
        else:
            await update.message.reply_text(f"⚠ No profile picture found for {user.full_name}.")
    except:
        await update.message.reply_text("⚠ Could not fetch profile picture.")


async def mention_all(update: Update, context: CallbackContext) -> None:
    """Mentions all members in the group (first 20 to prevent spam)."""
    chat = update.effective_chat
    members = [f"@{member.user.username}" async for member in context.bot.get_chat_members(chat.id) if member.user.username]
    mention_text = "📢 Mentioning All:\n" + " ".join(members[:20])
    await update.message.reply_text(mention_text if members else "⚠ No members found.")


async def set_rules(update: Update, context: CallbackContext) -> None:
    """Admins can set group rules using /setrules [new rules]"""
    global group_rules
    if not context.args:
        await update.message.reply_text("⚠ Usage: `/setrules Your new rules here`")
        return
    group_rules = " ".join(context.args)
    await update.message.reply_text("✅ Group rules updated!")


async def get_rules(update: Update, context: CallbackContext) -> None:
    """Users can view group rules with /rules"""
    await update.message.reply_text(f"📜 **Group Rules:**\n{group_rules}")


async def schedule_message(update: Update, context: CallbackContext) -> None:
    """Schedule a message with /schedule HH:MM Message"""
    if len(context.args) < 2:
        await update.message.reply_text("⚠ Usage: `/schedule HH:MM Your message`")
        return

    time_str = context.args[0]
    message_text = " ".join(context.args[1:])
    try:
        schedule_time = datetime.strptime(time_str, "%H:%M").time()
        scheduled_messages.append((schedule_time, message_text))
        await update.message.reply_text(f"✅ Message scheduled for {time_str}.")
    except ValueError:
        await update.message.reply_text("⚠ Invalid time format! Use HH:MM (24-hour format).")


async def auto_moderation(update: Update, context: CallbackContext) -> None:
    """Detects bad words and deletes the message."""
    text = update.message.text.lower()
    if any(word in text for word in BAD_WORDS):
        await update.message.delete()
        await update.message.reply_text("⚠ **Inappropriate language detected!**")


def main() -> None:
    """Starts the bot."""
    init_db()
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("info", get_user_info))
    app.add_handler(CommandHandler("getpfp", get_profile_picture))
    app.add_handler(CommandHandler("mentionall", mention_all))
    app.add_handler(CommandHandler("rules", get_rules))
    app.add_handler(CommandHandler("setrules", set_rules))
    app.add_handler(CommandHandler("schedule", schedule_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_moderation))

    logger.info("🚀 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
