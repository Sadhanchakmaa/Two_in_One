# config.py
import os
import json
import re
from telegram import ReplyKeyboardMarkup, KeyboardButton

# ==================== টোকেন ====================
TOKEN = os.environ.get("BOT_TOKEN", "8998576452:AAGGOkH4LfgLkw-DpqvhqLTAhlbaGtQPyK4")

# ==================== পাথ ডিটেক্ট ====================
def get_base_dir():
    # Railway এর জন্য
    if 'com.termux' in os.environ.get('PREFIX', '') or os.path.exists('/sdcard'):
        return "/sdcard/File_conv"
    else:
        # Railway তে এই পাথে ফাইল সেভ হবে
        return os.path.join(os.getcwd(), "bot_files")

BASE_DIR = get_base_dir()
os.makedirs(BASE_DIR, exist_ok=True)

# ==================== কান্ট্রি ডাটা ====================
def load_country_data():
    try:
        with open('countries.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

COUNTRY_DATA = load_country_data()

# ==================== মেইন মেনু ====================
MAIN_MENU = ReplyKeyboardMarkup([
    [KeyboardButton("📱 FACEBOOK COOKIES", style="primary")],
    [KeyboardButton("📁 FILE CHANGE", style="danger")],
    [KeyboardButton("🌍 NUMBER CONVERTER", style="success")],
    [KeyboardButton("🔄 RESET", style="danger"), KeyboardButton("ℹ️ HELP", style="success")]
], resize_keyboard=True)

BACK_FB_MENU = ReplyKeyboardMarkup([
    [KeyboardButton("🔙 BACK", style="danger")]
], resize_keyboard=True)

# ==================== ইউটিলিটি ফাংশন ====================
def clean_numbers_from_text(text):
    raw_numbers = re.findall(r'\b\d{9,15}\b', text)
    clean = []
    
    for num in raw_numbers:
        if len(num) == 10:
            if num.startswith('01'):
                num = '+880' + num[1:]
            else:
                num = '+91' + num
        elif len(num) == 11:
            code = num[:2]
            if code in COUNTRY_DATA:
                num = '+' + num
            else:
                code = num[:3]
                if code in COUNTRY_DATA:
                    num = '+' + num
                else:
                    num = '+' + num
        elif len(num) == 12:
            code = num[:3]
            if code in COUNTRY_DATA:
                num = '+' + num
            else:
                code = num[:2]
                if code in COUNTRY_DATA:
                    num = '+' + num
                else:
                    num = '+' + num
        elif len(num) == 13:
            code = num[:3]
            if code in COUNTRY_DATA:
                num = '+' + num
            else:
                num = '+' + num
        elif 11 <= len(num) <= 15:
            for code_len in [3, 2]:
                if len(num) > code_len:
                    code = num[:code_len]
                    if code in COUNTRY_DATA:
                        num = '+' + num
                        break
        
        if num.startswith('+') and num not in clean:
            clean.append(num)
    
    return clean

def get_country_info(number):
    for code, info in COUNTRY_DATA.items():
        if number.startswith('+' + code):
            return {
                'code': code,
                'short_code': info.get('code', '??'),
                'flag': info['flag'],
                'name_en': info['name_en']
            }
    return {'code': '??', 'short_code': '??', 'flag': '🌍', 'name_en': 'Unknown'}