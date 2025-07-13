import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "8121739214:AAEK80VGwuS09y_exayUS6PRDryAldvbmkg"
DATA_FILE = "users.json"

REQUIRED_CHANNELS = [
    {"name": "Main Channel", "url": "https://t.me/flashpayyofficial"},
    {"name": "Community", "url": "https://t.me/kdfub1QqG79jNDU0"},
    {"name": "Partnership", "url": "https://t.me/Dark_toolz51"},
    {"name": "Withdraw Channel", "url": "https://t.me/flashpayybot"},
]

MIN_WITHDRAW = 20000
MAX_WITHDRAW = 1000000
REQUIRED_REFERRALS = 10

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def init_user(user_id):
    data = load_data()
    if str(user_id) not in data:
        data[str(user_id)] = {"balance": 0, "referrals": [], "invited_by": None}
        save_data(data)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(user_id)
    if context.args:
        ref_id = context.args[0]
        if ref_id != user_id:
            data = load_data()
            if user_id not in data[ref_id]["referrals"]:
                data[ref_id]["referrals"].append(user_id)
                data[ref_id]["balance"] += 3000
                save_data(data)
    buttons = [[InlineKeyboardButton(ch["name"], url=ch["url"])] for ch in REQUIRED_CHANNELS]
    buttons.append([InlineKeyboardButton("✅ I’ve Joined", callback_data="joined")])
    await update.message.reply_text("📢 Please join all the required channels:", reply_markup=InlineKeyboardMarkup(buttons))

async def joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        ["📥Withdraw", "📢Channels"],
        ["🧑‍🤝‍🧑Invite", "💰Balance"],
        ["Earn more ⚡"]
    ]
    await query.message.reply_text("✅ Access granted!", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    init_user(user_id)
    data = load_data()[user_id]
    bal = data["balance"]
    refs = len(data["referrals"])
    await update.message.reply_text(f"💰 Balance: ₦{bal:,}\n👥 Referrals: {refs}")

async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    link = f"https://t.me/{context.bot.username}?start={user_id}"
    await update.message.reply_text(f"👥 Invite Friends with this link:\n{link}")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()
    bal = data[user_id]["balance"]
    refs = len(data[user_id]["referrals"])
    if bal < MIN_WITHDRAW:
        await update.message.reply_text("❌ Minimum withdrawal is ₦20,000.")
    elif bal > MAX_WITHDRAW:
        await update.message.reply_text("❌ Maximum withdrawal is ₦1,000,000.")
    elif refs < REQUIRED_REFERRALS:
        await update.message.reply_text("❌ You need at least 10 referrals to withdraw.")
    else:
        await update.message.reply_text("✅ Withdrawal request sent! Our team will contact you.")

async def channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[InlineKeyboardButton(ch["name"], url=ch["url"])] for ch in REQUIRED_CHANNELS]
    await update.message.reply_text("📢 Join all channels:", reply_markup=InlineKeyboardMarkup(buttons))

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ I didn't understand that. Use the buttons.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(joined, pattern="joined"))
app.add_handler(MessageHandler(filters.Text("💰Balance"), balance))
app.add_handler(MessageHandler(filters.Text("🧑‍🤝‍🧑Invite"), invite))
app.add_handler(MessageHandler(filters.Text("📥Withdraw"), withdraw))
app.add_handler(MessageHandler(filters.Text("📢Channels"), channels))
app.add_handler(MessageHandler(filters.ALL, unknown))

import asyncio

async def main():
    print("✅ Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
