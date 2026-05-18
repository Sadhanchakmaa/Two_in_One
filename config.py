# config.py
import os
import json
import sys
import re
from telegram import ReplyKeyboardMarkup, KeyboardButton

# ==================== টোকেন ====================
TOKEN = os.environ.get("BOT_TOKEN")
#TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ BOT_TOKEN not found in environment variables!")
    sys.exit(1)
# ==================== পাথ ডিটেক্ট ====================
def get_base_dir():
    if 'com.termux' in os.environ.get('PREFIX', '') or os.path.exists('/sdcard'):
        return "/sdcard/File_conv"
    else:
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

# ==================== কাস্টম ইমোজি (ডিরেক্টলি) ====================
CUSTOM_EMOJI = {
    "📱": "6210664181943771071",
    "📂": "5332586662629227075",
    "🌍": "6188045471118790922",
    "🔄": "5264727218734524899",
    "ℹ️": "5332679880599418983",
    "🔥": "6231224366483384495",
    "✅": "6230828091325818369",
    "🚀": "6147654280112248427",
    "📞": "5467539229468793355",
    "🔙": "6206505206197261313",
    "🏠": "5416041192905265756",
    "📎": "5377844313575150051",
    "✏️": "5395444784611480792",
    "✨": "6232983172770962452",
    "👑": "6233506609025261770",
    "💎": "6230898013393396414",
    "🎯": "5310278924616356636",
    "📊": "6233241506463883080",
    "🔒": "5296369303661067030",
    "📥": "5433811242135331842",
    "⚙️": "5895577117592128901",
    "🗑️": "6233541449799966206",
    "💾": "25431736674147114227",
    "📖": "5226512880362332956",
    "⏳": "6154603635981423575",
    "❌": "6232999605315837644",
    "📝": "5436353008076075648",
    "📌": "5436007417827578363",
    "🟢": "6113685078825505075",
    "🔴": "6233042091132329496",
    "🎲": "5472404950673791399",
    "📋": "5197269100878907942",
    "📄": "5873153278023307367",
    "🏷️": "6066473359493828085",
    "🔑": "5330115548900501467",
    "🍪": "6233183429916107004",
    "🆔": "5841276284155467413",
    "⚠️": "5436034420286960597",
    "👇": "6233121371933646400",
    "⏭️": "6233383992003927192",
    "🔐": "5472308992514464048",
    "💗": "YOUR_HEART_EMOJI_ID",
    "👻": "YOUR_GHOST_EMOJI_ID"
}

# ==================== মেইন মেনু ====================
MAIN_MENU = ReplyKeyboardMarkup([
    [KeyboardButton("FACEBOOK COOKIES", icon_custom_emoji_id=CUSTOM_EMOJI.get("📱"), style="primary")],
    [KeyboardButton("FILE CHANGE", icon_custom_emoji_id=CUSTOM_EMOJI.get("📂"), style="danger")],
    [KeyboardButton("NUMBER CONVERTER", icon_custom_emoji_id=CUSTOM_EMOJI.get("🌍"), style="success")],
    [KeyboardButton("RESET", icon_custom_emoji_id=CUSTOM_EMOJI.get("🔄"), style="danger"), 
     KeyboardButton("HELP", icon_custom_emoji_id=CUSTOM_EMOJI.get("ℹ️"), style="success")]
], resize_keyboard=True)

BACK_FB_MENU = ReplyKeyboardMarkup([
    [KeyboardButton("BACK", icon_custom_emoji_id=CUSTOM_EMOJI.get("🔙"), style="danger")]
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
