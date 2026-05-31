import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, WEBAPP_URL, EGA_ID
from database import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════
# COMMAND: /start
# ═══════════════════════════════════════════
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - show main menu"""
    user = update.effective_user
    user_id = user.id
    
    # Get user role
    role = db.get_user_role(user_id)
    
    welcome_text = f"""
🎉 *Ayron Savdo* ga xush kelibsiz!

👤 Siz: {user.first_name} ({role.upper()})
ID: `{user_id}`

Quyidagi tugmalardan foydalaning:
"""
    
    keyboard = []
    
    # WebApp button - always available
    webapp_button = InlineKeyboardButton(
        text="📊 DASHBOARD OCHISH",
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    keyboard.append([webapp_button])
    
    # Role-based buttons
    if role == 'ega':
        keyboard.append([
            InlineKeyboardButton("📋 HISOBOT", callback_data="hisobot"),
            InlineKeyboardButton("🏆 TOP", callback_data="top")
        ])
        keyboard.append([
            InlineKeyboardButton("👷 ISHCHILAR", callback_data="ishchilar"),
            InlineKeyboardButton("🛍 MAHSULOTLAR", callback_data="mahsulotlar")
        ])
    elif role == 'hisobchi':
        keyboard.append([
            InlineKeyboardButton("📋 HISOBOT", callback_data="hisobot"),
            InlineKeyboardButton("🛒 SOTUV", callback_data="sotuv")
        ])
    elif role == 'ishchi':
        keyboard.append([
            InlineKeyboardButton("🛒 SOTUV", callback_data="sotuv"),
            InlineKeyboardButton("🎯 MENING TARGET", callback_data="target")
        ])
    
    keyboard.append([InlineKeyboardButton("ℹ️ INFO", callback_data="info")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# ═══════════════════════════════════════════
# COMMAND: /sotuv
# ═══════════════════════════════════════════
async def sotuv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show sales summary"""
    from datetime import datetime
    
    today = datetime.now().strftime('%Y-%m-%d')
    sotuvlar = [s for s in db.data['sotuvlar'] if s['sana'].startswith(today)]
    
    total = sum(s.get('summa', 0) for s in sotuvlar)
    count = len(sotuvlar)
    
    text = f"""
🛒 *BUGUNGI SOTUVLAR*

📊 Jami: {count} ta
💰 Summa: {total:,} so'm

Batafsil: Dashboard-dan ko'ring
"""
    
    await update.message.reply_text(text, parse_mode='Markdown')

# ═══════════════════════════════════════════
# COMMAND: /hisobot
# ═══════════════════════════════════════════
async def hisobot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show today's report"""
    from datetime import datetime
    
    today = datetime.now().strftime('%Y-%m-%d')
    sotuvlar = [s for s in db.data['sotuvlar'] if s['sana'].startswith(today)]
    rasxodlar = [r for r in db.data['rasxodlar'] if r['sana'].startswith(today)]
    
    total_sotuv = sum(s.get('summa', 0) for s in sotuvlar)
    total_rasxod = sum(r.get('summa', 0) for r in rasxodlar)
    foyda = total_sotuv - total_rasxod
    
    text = f"""
📋 *BUGUNGI HISOBOT*

🛒 Sotuvlar: {total_sotuv:,} so'm
💸 Rasxodlar: {total_rasxod:,} so'm
💹 Foyda: {foyda:,} so'm

📊 Batafsil dashboard-dan ko'ring
"""
    
    await update.message.reply_text(text, parse_mode='Markdown')

# ═══════════════════════════════════════════
# COMMAND: /menu
# ═══════════════════════════════════════════
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show menu"""
    await start(update, context)

# ═══════════════════════════════════════════
# CALLBACK QUERIES
# ═══════════════════════════════════════════
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "info":
        text = """
*Ayron Savdo v5* 🚀

📱 Web App + Bot integratsiyasi
🐍 Python + Flask Backend
💾 JSON Database

Ishchilar, hisobchilar va EGA uchun to'liq hisobot tizimi.

👨‍💼 Barcha sotuvlar real-time kuzatiladi
📊 Kunlik/oylik hisobotlar
🎯 Target va performance tracking

Qo'shimcha savol uchun: @milkmanu
"""
        await query.edit_message_text(text, parse_mode='Markdown')

# ═══════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════
def main():
    """Start the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sotuv", sotuv))
    application.add_handler(CommandHandler("hisobot", hisobot))
    application.add_handler(CommandHandler("menu", menu))
    
    # Callbacks
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 Bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    main()
