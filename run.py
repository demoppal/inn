import logging
import os
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

# Configuration
BOT_TOKEN = "8706727466:AAEYGFLafGWwfRMIpkWx_8GCUr1zqRBimDU"
WEB_SERVER_PORT = 5000

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Starlink Module ကို ခေါ်ယူ Run မည့်အပိုင်း ---
def run_starlink_in_bot():
    try:
        import starlink
        if hasattr(starlink, 'main'):
            starlink.main()
        elif hasattr(starlink, 'start'):
            starlink.start()
        return True, "Starlink Module ကို အောင်မြင်စွာ စတင်လိုက်ပါပြီ။"
    except ImportError:
        return False, "'starlink' module ဖိုင်ကို ဆာဗာပေါ်မှာ ရှာမတွေ့ပါ။"
    except Exception as e:
        return False, f"Starlink Run ရာတွင် အမှားတက်ခဲပါသည်: {e}"

def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton("🚀 Starlink စတင်ရန်")],
        [KeyboardButton("ℹ️ အကူအညီ")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_text = (
        f"မင်္ဂလာပါ {user.mention_html()} 🙏\n\n"
        "ကျွန်ုပ်တို့၏ အခမဲ့ Bot မှ ကြိုဆိုပါတယ်။\n"
        "အောက်က '🚀 Starlink စတင်ရန်' ခလုတ်ကို နှိပ်ပြီး တိုက်ရိုက် အသုံးပြုနိုင်ပါတယ်။"
    )
    await update.message.reply_text(welcome_text, parse_mode='HTML', reply_markup=get_main_menu_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    
    if text == "🚀 Starlink စတင်ရန်":
        await update.message.reply_text("⏳ Starlink Module ကို စတင်နေပါပြီ၊ ခေတ္တစောင့်ဆိုင်းပေးပါ...")
        
        success, msg = run_starlink_in_bot()
        if success:
            await update.message.reply_text(f"✅ {msg}")
        else:
            await update.message.reply_text(f"❌ {msg}")
            
    elif text == "ℹ️ အကူအညီ":
        help_text = (
            "📖 **အသုံးပြုနည်း**\n\n"
            "• '🚀 Starlink စတင်ရန်' ခလုတ်ကို နှိပ်လိုက်ရုံဖြင့် Bot က လုပ်ငန်းစဉ်ကို တိုက်ရိုက် အလုပ်လုပ်ပေးသွားမှာ ဖြစ်ပါတယ်။\n"
            "• မည်သည့် Key မျှ ထည့်သွင်းပေးရန် မလိုဘဲ အခမဲ့ စမ်းသပ်နိုင်ပါတယ်။"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')

app = Flask(__name__)
@app.route("/", methods=["GET"])
def health_check():
    return "Bot is alive and free!", 200

def run_flask_app():
    port = int(os.environ.get("PORT", WEB_SERVER_PORT))
    app.run(host="0.0.0.0", port=port)

def main() -> None:
    # Flask Web Server ကို သီးသန့် Thread နဲ့ Background မှာ Run ခြင်း
    Thread(target=run_flask_app, daemon=True).start()
    
    # Telegram Application ကို တည်ဆောက်ခြင်း
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers များ ထည့်သွင်းခြင်း
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # v21+ ရေးထုံးအသစ်အတိုင်း String list ဖြင့် စာလုံးအသေး ပြောင်းလဲသတ်မှတ်ထားပါတယ်
    application.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()
    
