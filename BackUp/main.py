# main.py
import os
import sys

# ব্যাকএন্ড ফোল্ডার পাথে যোগ করুন (বর্তমান ডিরেক্টরি থেকে)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# কনফিগারেশন
from config import TOKEN, MAIN_MENU, BACK_FB_MENU, BASE_DIR, COUNTRY_DATA, get_base_dir, load_country_data

# হ্যান্ডলার ইম্পোর্ট
from handlers import (
    start, cancel, handle_menu, handle_number_file,
    toggle_random_callback, num_convert_callback,
    num_convert_plus_callback, num_reset_callback
)

# কনভার্সেশন হ্যান্ডলার ইম্পোর্ট
from rename_handler import rename_conversation_handler
from facebook_handler import facebook_conversation_handler

# টেলিগ্রাম ইম্পোর্ট
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler


def main():
    app = Application.builder().token(TOKEN).build()
    
    # কনভার্সেশন হ্যান্ডলার যোগ করুন
    app.add_handler(rename_conversation_handler())
    app.add_handler(facebook_conversation_handler())
    
    # বেসিক হ্যান্ডলার
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_number_file))
    
    # কলব্যাক হ্যান্ডলার
    app.add_handler(CallbackQueryHandler(toggle_random_callback, pattern='toggle_random'))
    app.add_handler(CallbackQueryHandler(num_convert_callback, pattern='num_convert'))
    app.add_handler(CallbackQueryHandler(num_convert_plus_callback, pattern='num_convert_plus'))
    app.add_handler(CallbackQueryHandler(num_reset_callback, pattern='num_reset'))
    
    print(f"✅ Bot Started! {len(COUNTRY_DATA)} countries!")
    app.run_polling()


if __name__ == "__main__":
    main()