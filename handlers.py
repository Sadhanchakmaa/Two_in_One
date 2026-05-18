# handlers.py
import os
import re
import random
import shutil
import openpyxl
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

from config import (
    MAIN_MENU, BACK_FB_MENU, BASE_DIR, COUNTRY_DATA,
    clean_numbers_from_text, get_country_info
)

# Custom Premium Emoji IDs
CUSTOM_EMOJI = {
    "📱": "6210664181943771071",
    "👻": "6069037893056208851",
    "💗": "6213065824576478666",
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
    "🔐": "5472308992514464048"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔥"]}">🔥</tg-emoji> <b>BEST NUMBER TOOL ON TELEGRAM</b> <tg-emoji emoji-id="{CUSTOM_EMOJI["🔥"]}">🔥</tg-emoji>\n\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✅"]}">✅</tg-emoji> Clean 10,000+ numbers in seconds\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✅"]}">✅</tg-emoji> 100% accurate country detection\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✅"]}">✅</tg-emoji> No data stored (except FB manager)\n\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🚀"]}">🚀</tg-emoji> <b>Just send a file & relax!</b>\n\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📞"]}">📞</tg-emoji> <b>{len(COUNTRY_DATA)} countries</b> | <tg-emoji emoji-id="{CUSTOM_EMOJI["📂"]}">📂</tg-emoji> 3 formats',
        parse_mode='HTML',
        reply_markup=MAIN_MENU
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✨"]}">✨</tg-emoji> Cancelled successfully!\n'
        f'No worries — returning to Main Menu <tg-emoji emoji-id="{CUSTOM_EMOJI["🏠"]}">🏠</tg-emoji>',
        parse_mode='HTML',
        reply_markup=MAIN_MENU
    )
    return ConversationHandler.END


def read_txt_content(file_path):
    content = ""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line and re.search(r'\d', line):
                content += line + " "
    return content


def read_xlsx_content(file_path):
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheet = wb.active
    content = ""
    for row in sheet.iter_rows(values_only=True):
        for cell in row:
            if cell is not None:
                cell_str = str(cell).strip()
                if re.search(r'\d{9,}', cell_str):
                    content += cell_str + " "
    return content


def read_csv_content(file_path):
    content = ""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parts = line.replace(',', ' ').split()
            for part in parts:
                if re.search(r'\d{9,}', part):
                    content += part + " "
    return content


def read_file_content(file_path, file_ext):
    if file_ext == '.xlsx':
        return read_xlsx_content(file_path)
    elif file_ext == '.csv':
        return read_csv_content(file_path)
    else:
        return read_txt_content(file_path)


async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()  # 👈 এই লাইন যোগ করুন (একদম প্রথমে)
    
    text = update.message.text
    
    if text == "BACK":
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔙"]}">🔙</tg-emoji> <b>Returning to Main Menu</b>',
            parse_mode='HTML',
            reply_markup=MAIN_MENU
        )
        return
    
    if text == "BACK TO MAIN MENU":
        context.user_data.clear()
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🏠"]}">🏠</tg-emoji> <b>Main Menu</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✅"]}">✅</tg-emoji> Session ended\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["👇"]}">👇</tg-emoji> <b>Choose an option:</b>',
            parse_mode='HTML',
            reply_markup=MAIN_MENU
        )
        return ConversationHandler.END
    
    # Number Converter
    if text == "NUMBER CONVERTER":
        context.user_data.clear()
        context.user_data['mode'] = 'number_converter'
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📎"]}">📎</tg-emoji> <b>FILE UPLOAD REQUIRED</b>\n\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✅"]}">✅</tg-emoji> <b>Supported formats:</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📄"]}">📄</tg-emoji> • .txt\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📄"]}">📄</tg-emoji> • .csv\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📄"]}">📄</tg-emoji> • .xlsx\n\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📥"]}">📥</tg-emoji> <b>Send your file now</b>\n\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔙"]}">🔙</tg-emoji> Press BACK to cancel',
            parse_mode='HTML',
            reply_markup=BACK_FB_MENU
        )
        return
    
    if text == "FILE CHANGE":
        return
    
    if text == "FACEBOOK COOKIES":
        return
    
    if text == "RESET":
        context.user_data.clear()
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🗑️"]}">🗑️</tg-emoji> <b>DATA CLEARED</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✅"]}">✅</tg-emoji> Ready\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🏠"]}">🏠</tg-emoji> Main Menu',
            parse_mode='HTML',
            reply_markup=MAIN_MENU
        )
        return
    
    if text == "HELP":
        help_inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Admin",style="primary", url="https://t.me/Sadhan_chakma", icon_custom_emoji_id=CUSTOM_EMOJI["💗"])],
            [InlineKeyboardButton("Main Channel",style="success", url="https://t.me/Team_X_Run", icon_custom_emoji_id=CUSTOM_EMOJI["👻"])]
        ])
        
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📖"]}">📖</tg-emoji> <b>COMMAND REFERENCE</b>\n\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🌍"]}">🌍</tg-emoji> <b>NUMBER CONVERTER</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎯"]}">🎯</tg-emoji> → Extract + country flag\n\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📂"]}">📂</tg-emoji> <b>FILE CHANGE</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎯"]}">🎯</tg-emoji> → Rename files\n\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📱"]}">📱</tg-emoji> <b>FACEBOOK COOKIES</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎯"]}">🎯</tg-emoji> → Store UID/Pass/Cookies\n\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔄"]}">🔄</tg-emoji> <b>RESET</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎯"]}">🎯</tg-emoji> → Clear temp data\n\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🌍"]}">🌍</tg-emoji> <b>{len(COUNTRY_DATA)} countries supported</b>',
            parse_mode='HTML',
            reply_markup=help_inline_keyboard
        )
        return


async def handle_number_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "BACK":
        context.user_data.clear()
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔙"]}">🔙</tg-emoji> <b>BACK TO MENU</b>',
            parse_mode='HTML',
            reply_markup=MAIN_MENU
        )
        return
    
    if context.user_data.get('mode') != 'number_converter':
        return
    
    if 'random_mode' not in context.user_data:
        context.user_data['random_mode'] = False
    
    processing_msg = await update.message.reply_text(
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["⏳"]}">⏳</tg-emoji> <b>PROCESSING</b>\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📂"]}">📂</tg-emoji> Please wait...',
        parse_mode='HTML'
    )
    
    file = await update.message.document.get_file()
    file_name = update.message.document.file_name
    
    if file_name.endswith('.xlsx'):
        file_ext = '.xlsx'
    elif file_name.endswith('.csv'):
        file_ext = '.csv'
    else:
        file_ext = '.txt'
    
    file_path = os.path.join(BASE_DIR, f"{file.file_id}{file_ext}")
    await file.download_to_drive(file_path)
    
    try:
        content = read_file_content(file_path, file_ext)
    except Exception as e:
        await processing_msg.edit_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["❌"]}">❌</tg-emoji> <b>ERROR</b>\n'
            f'{str(e)[:50]}',
            parse_mode='HTML'
        )
        os.remove(file_path)
        return
    
    numbers = clean_numbers_from_text(content)
    
    if not numbers:
        await processing_msg.edit_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["❌"]}">❌</tg-emoji> <b>NO VALID NUMBERS FOUND!</b>\n\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📞"]}">📞</tg-emoji> <b>CORRECT FORMAT:</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎯"]}">🎯</tg-emoji> • 965XXXXXXXXX (Kuwait)\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎯"]}">🎯</tg-emoji> • 998XXXXXXXXX (Uzbekistan)\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎯"]}">🎯</tg-emoji> • 93XXXXXXXXX (Afghanistan)\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎯"]}">🎯</tg-emoji> • 01XXXXXXXXX (Bangladesh)\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎯"]}">🎯</tg-emoji> • 98XXXXXXXX (India)',
            parse_mode='HTML'
        )
        os.remove(file_path)
        return
    
    country_info = get_country_info(numbers[0])
    context.user_data['country_info'] = country_info
    main_country = f"{country_info['flag']} {country_info['name_en']} ({country_info['short_code']}) +{country_info['code']}"
    
    context.user_data['numbers'] = numbers
    
    # 🟢 ON / 🔴 OFF - Random mode icon select
    if context.user_data['random_mode']:
        random_mode_status = f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🟢"]}">🟢</tg-emoji> ON'
        random_icon = CUSTOM_EMOJI["🟢"]
    else:
        random_mode_status = f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔴"]}">🔴</tg-emoji> OFF'
        random_icon = CUSTOM_EMOJI["🔴"]
    
    await processing_msg.delete()
    
    # Inline buttons with icon_custom_emoji_id
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Random Mode",style="success", callback_data='toggle_random', icon_custom_emoji_id=random_icon)],
        [InlineKeyboardButton(f"Convert ({len(numbers)})",style="primary", callback_data='num_convert', icon_custom_emoji_id=CUSTOM_EMOJI["✅"]),
         InlineKeyboardButton("Convert with +",style="primary", callback_data='num_convert_plus', icon_custom_emoji_id=CUSTOM_EMOJI["✅"])],
        [InlineKeyboardButton("Reset",style="danger", callback_data='num_reset', icon_custom_emoji_id=CUSTOM_EMOJI["🔄"])]
    ])
    
    await update.message.reply_text(
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📊"]}">📊</tg-emoji> <b>PROCESSING COMPLETE</b>\n\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🌍"]}">🌍</tg-emoji> <b>Country:</b> {main_country}\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📞"]}">📞</tg-emoji> <b>Valid Numbers:</b> {len(numbers)}\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📝"]}">📝</tg-emoji> <b>Sample:</b> <code>{numbers[0]}</code>\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎲"]}">🎲</tg-emoji> <b>Random Mode:</b> {random_mode_status}\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📌"]}">📌</tg-emoji> <b>Output:</b> +{country_info["code"]}XXXXXXXXX',
        reply_markup=inline_keyboard,
        parse_mode='HTML'
    )
    
    os.remove(file_path)

async def toggle_random_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    current_mode = context.user_data.get('random_mode', False)
    new_mode = not current_mode
    context.user_data['random_mode'] = new_mode
    
    numbers = context.user_data.get('numbers', [])
    country_info = context.user_data.get('country_info', {'code': '??', 'flag': '🌍', 'name_en': 'Unknown', 'short_code': '??'})
    
    # 🟢 ON / 🔴 OFF - Random mode status
    if new_mode:
        random_mode_status = f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🟢"]}">🟢</tg-emoji> ON'
        random_icon = CUSTOM_EMOJI["🟢"]
    else:
        random_mode_status = f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔴"]}">🔴</tg-emoji> OFF'
        random_icon = CUSTOM_EMOJI["🔴"]
    
    if not numbers:
        await query.edit_message_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["❌"]}">❌</tg-emoji> <b>NO NUMBERS FOUND!</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📥"]}">📥</tg-emoji> Please upload a file first',
            parse_mode='HTML'
        )
        return
    
    # Inline buttons with icon_custom_emoji_id
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Random Mode", style="success", callback_data='toggle_random', icon_custom_emoji_id=random_icon)],
        [InlineKeyboardButton(f"Convert ({len(numbers)})", style="primary", callback_data='num_convert', icon_custom_emoji_id=CUSTOM_EMOJI["✅"]),
         InlineKeyboardButton("Convert with +",style="primary", callback_data='num_convert_plus', icon_custom_emoji_id=CUSTOM_EMOJI["✅"])],
        [InlineKeyboardButton("Reset",style="danger", callback_data='num_reset', icon_custom_emoji_id=CUSTOM_EMOJI["🔄"])]
    ])
    
    main_country = f"{country_info['flag']} {country_info['name_en']} ({country_info['short_code']}) +{country_info['code']}"
    
    await query.edit_message_text(
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📊"]}">📊</tg-emoji> <b>PROCESSING COMPLETE</b>\n\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🌍"]}">🌍</tg-emoji> <b>Country:</b> {main_country}\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📞"]}">📞</tg-emoji> <b>Valid Numbers:</b> {len(numbers)}\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📝"]}">📝</tg-emoji> <b>Sample:</b> <code>{numbers[0]}</code>\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎲"]}">🎲</tg-emoji> <b>Random Mode:</b> {random_mode_status}\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📌"]}">📌</tg-emoji> <b>Output:</b> +{country_info["code"]}XXXXXXXXX\n\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✅"]}">✅</tg-emoji> <b>Mode changed to</b> {random_mode_status}\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["👇"]}">👇</tg-emoji> Press Convert button to save file',
        reply_markup=inline_keyboard,
        parse_mode='HTML'
    )


async def num_convert_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    numbers = context.user_data.get('numbers', [])
    random_mode = context.user_data.get('random_mode', False)
    country_info = context.user_data.get('country_info', {'name_en': 'Unknown', 'code': '??'})
    
    if not numbers:
        await query.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["❌"]}">❌</tg-emoji> <b>NO NUMBERS FOUND!</b>',
            parse_mode='HTML'
        )
        return
    
    if random_mode:
        shuffled_numbers = numbers.copy()
        random.shuffle(shuffled_numbers)
        output = "\n".join(shuffled_numbers)
        mode_text = f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎲"]}">🎲</tg-emoji> Random Order'
    else:
        def get_full_number(num):
            clean_num = num.lstrip('+')
            return int(clean_num)
        
        sorted_numbers = sorted(numbers, key=get_full_number)
        output = "\n".join(sorted_numbers)
        mode_text = f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📊"]}">📊</tg-emoji> Numerical Order (Full Number)'
    
    filename = f"{country_info['name_en']}_Numbers.txt"
    filepath = os.path.join(BASE_DIR, filename)
    
    with open(filepath, "w") as f:
        f.write(output)
    
    with open(filepath, "rb") as f:
        await query.message.reply_document(
            document=f, 
            filename=filename,
            caption=f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✅"]}">✅</tg-emoji> <b>CONVERSION COMPLETE</b>\n\n'
                    f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📞"]}">📞</tg-emoji> <b>Numbers:</b> {len(numbers)}\n'
                    f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎲"]}">🎲</tg-emoji> <b>Mode:</b> {mode_text}\n'
                    f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📌"]}">📌</tg-emoji> <b>Format:</b> +{country_info["code"]}XXXXXXXXX',
            parse_mode='HTML'
        )
    
    os.remove(filepath)


async def num_convert_plus_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    numbers = context.user_data.get('numbers', [])
    random_mode = context.user_data.get('random_mode', False)
    country_info = context.user_data.get('country_info', {'name_en': 'Unknown', 'code': '??'})
    
    if not numbers:
        await query.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["❌"]}">❌</tg-emoji> <b>NO NUMBERS FOUND!</b>',
            parse_mode='HTML'
        )
        return
    
    if random_mode:
        shuffled_numbers = numbers.copy()
        random.shuffle(shuffled_numbers)
        output = "\n".join([f"+{num}" if not num.startswith('+') else num for num in shuffled_numbers])
        mode_text = f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎲"]}">🎲</tg-emoji> Random Order'
    else:
        def get_full_number(num):
            clean_num = num.lstrip('+')
            return int(clean_num)
        
        sorted_numbers = sorted(numbers, key=get_full_number)
        output = "\n".join([f"+{num}" if not num.startswith('+') else num for num in sorted_numbers])
        mode_text = f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📊"]}">📊</tg-emoji> Numerical Order (Full Number)'
    
    filename = f"{country_info['name_en']}_Numbers_With_Plus.txt"
    filepath = os.path.join(BASE_DIR, filename)
    
    with open(filepath, "w") as f:
        f.write(output)
    
    with open(filepath, "rb") as f:
        await query.message.reply_document(
            document=f, 
            filename=filename,
            caption=f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✅"]}">✅</tg-emoji> <b>CONVERSION (+ FORMAT)</b>\n\n'
                    f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📞"]}">📞</tg-emoji> <b>Numbers:</b> {len(numbers)}\n'
                    f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎲"]}">🎲</tg-emoji> <b>Mode:</b> {mode_text}\n'
                    f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📌"]}">📌</tg-emoji> <b>Format:</b> +{country_info["code"]}XXXXXXXXX',
            parse_mode='HTML'
        )
    
    os.remove(filepath)


async def num_reset_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    context.user_data.pop('numbers', None)
    context.user_data.pop('random_mode', None)
    context.user_data.pop('country_info', None)
    
    await query.message.reply_text(
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔄"]}">🔄</tg-emoji> <b>RESET DONE</b>\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🗑️"]}">🗑️</tg-emoji> Data cleared\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📂"]}">📂</tg-emoji> Ready for new\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📥"]}">📥</tg-emoji> Send file now',
        parse_mode='HTML',
        reply_markup=MAIN_MENU
    )
