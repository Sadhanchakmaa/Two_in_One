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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 *BEST NUMBER TOOL ON TELEGRAM* 🔥\n\n"
        "✅ Clean 10,000+ numbers in seconds\n"
        "✅ 100% accurate country detection\n"
        "✅ No data stored (except FB manager)\n\n"
        "🚀 *Just send a file & relax!*\n\n"
        f"📞 *{len(COUNTRY_DATA)} countries* | 📁 3 formats",
        parse_mode="Markdown",
        reply_markup=MAIN_MENU
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "✨ Cancelled successfully!\n"
        "No worries — returning to Main Menu 🏠",
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
    text = update.message.text
    
    if text == "🔙 BACK":
        context.user_data.clear()
        await update.message.reply_text(
            "🔙 *Returning to Main Menu*",
            parse_mode="Markdown",
            reply_markup=MAIN_MENU
        )
        return
    
    if text == "🔙 BACK TO MAIN MENU":
        context.user_data.clear()
        await update.message.reply_text(
            "🏠 *Main Menu*\n━━━━━━━━━━\n✅ Session ended\n👇 Choose an option:",
            parse_mode="Markdown",
            reply_markup=MAIN_MENU
        )
        return ConversationHandler.END
    
    # নাম্বার কনভার্টার
    if text == "🌍 NUMBER CONVERTER":
        context.user_data.clear()
        context.user_data['mode'] = 'number_converter'
        await update.message.reply_text(
            "📎 *FILE UPLOAD REQUIRED*\n\n"
            "┌─────────────────────┐\n│ ✅ Supported formats │\n├─────────────────────┤\n│ • .txt              │\n│ • .csv              │\n│ • .xlsx             │\n└─────────────────────┘\n\n"
            "📤 *Send your file now*\n\n🔙 Press BACK to cancel",
            parse_mode="Markdown",
            reply_markup=BACK_FB_MENU
        )
        return
    
    if text == "📁 FILE CHANGE":
        return
    
    if text == "📱 FACEBOOK COOKIES":
        return
    
    if text == "🔄 RESET":
        context.user_data.clear()
        await update.message.reply_text(
            "┌─────────────────┐\n│ 🗑 DATA CLEARED │\n├─────────────────┤\n│ ✅ Ready        │\n│ 🏠 Main Menu    │\n└─────────────────┘",
            parse_mode="Markdown",
            reply_markup=MAIN_MENU
        )
        return
    
    if text == "ℹ️ HELP":
        await update.message.reply_text(
            f"📖 *COMMAND REFERENCE*\n\n"
            "┌─────────────────────────┐\n│ 🌍 NUMBER CONVERTER     │\n│ → Extract + country flag│\n├─────────────────────────┤\n"
            "│ 📁 FILE CHANGE          │\n│ → Rename files          │\n├─────────────────────────┤\n"
            "│ 📱 FACEBOOK COOKIES     │\n│ → Store UID/Pass/Cookies│\n├─────────────────────────┤\n"
            "│ 🔄 RESET                │\n│ → Clear temp data       │\n└─────────────────────────┘\n\n"
            f"🌍 *{len(COUNTRY_DATA)} countries supported*",
            parse_mode="Markdown",
            reply_markup=MAIN_MENU
        )
        return


async def handle_number_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🔙 BACK":
        context.user_data.clear()
        await update.message.reply_text("┌─────────────────────┐\n│  🔙 BACK TO MENU    │\n└─────────────────────┘", parse_mode="Markdown", reply_markup=MAIN_MENU)
        return
    
    if context.user_data.get('mode') != 'number_converter':
        return
    
    if 'random_mode' not in context.user_data:
        context.user_data['random_mode'] = False
    
    processing_msg = await update.message.reply_text(
        "┌─────────────────────┐\n│  ⏳ PROCESSING      │\n│  📁 Please wait...  │\n└─────────────────────┘",
        parse_mode="Markdown"
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
        await processing_msg.edit_text(f"┌─────────────────────┐\n│  ❌ ERROR           │\n│  {str(e)[:20]}│\n└─────────────────────┘", parse_mode="Markdown")
        os.remove(file_path)
        return
    
    numbers = clean_numbers_from_text(content)
    
    if not numbers:
        await processing_msg.edit_text(
            "┌─────────────────────────────────┐\n│  ❌ NO VALID NUMBERS FOUND!     │\n├─────────────────────────────────┤\n"
            "│  📞 CORRECT FORMAT:              │\n│  • 965XXXXXXXXX (Kuwait)        │\n│  • 998XXXXXXXXX (Uzbekistan)    │\n"
            "│  • 93XXXXXXXXX (Afghanistan)    │\n│  • 01XXXXXXXXX (Bangladesh)     │\n│  • 98XXXXXXXX (India)           │\n└─────────────────────────────────┘",
            parse_mode="Markdown"
        )
        os.remove(file_path)
        return
    
    country_info = get_country_info(numbers[0])
    context.user_data['country_info'] = country_info
    main_country = f"{country_info['flag']} {country_info['name_en']} ({country_info['short_code']}) +{country_info['code']}"
    
    context.user_data['numbers'] = numbers
    random_mode_status = "🟢 ON" if context.user_data['random_mode'] else "🔴 OFF"
    
    await processing_msg.delete()
    
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎲 Random Mode: {random_mode_status}", callback_data='toggle_random')],
        [InlineKeyboardButton(f"✅ Convert ({len(numbers)})", callback_data='num_convert'),
         InlineKeyboardButton(f"➕ Convert with +", callback_data='num_convert_plus')],
        [InlineKeyboardButton(f"🔄 Reset", callback_data='num_reset')]
    ])
    
    await update.message.reply_text(
        f"╔══════════════════════════════╗\n║     📊 PROCESSING COMPLETE    ║\n╠══════════════════════════════╣\n"
        f"║  🌍 Country: {main_country[:25]}\n║  🔢 Valid Numbers: {len(numbers)}\n║  📝 Sample: `{numbers[0]}`\n"
        f"║  🎲 Random Mode: {random_mode_status}\n║  📌 Output: +{country_info['code']}XXXXXXXXX\n╚══════════════════════════════╝",
        reply_markup=inline_keyboard,
        parse_mode="Markdown"
    )
    
    os.remove(file_path)


async def toggle_random_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    current_mode = context.user_data.get('random_mode', False)
    new_mode = not current_mode
    context.user_data['random_mode'] = new_mode
    
    # ডিবাগ প্রিন্ট (Termux-এ দেখাবে)
    
    numbers = context.user_data.get('numbers', [])
    country_info = context.user_data.get('country_info', {'code': '??', 'flag': '🌍', 'name_en': 'Unknown', 'short_code': '??'})
    random_mode_status = "🟢 ON" if new_mode else "🔴 OFF"
    
    if not numbers:
        await query.edit_message_text(
            "┌─────────────────────────────────┐\n"
            "│  ❌ NO NUMBERS FOUND!           │\n"
            "├─────────────────────────────────┤\n"
            "│  📤 Please upload a file first  │\n"
            "└─────────────────────────────────┘",
            parse_mode="Markdown"
        )
        return
    
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🎲 Random Mode: {random_mode_status}", callback_data='toggle_random')],
        [InlineKeyboardButton(f"✅ Convert ({len(numbers)})", callback_data='num_convert'),
         InlineKeyboardButton(f"➕ Convert with +", callback_data='num_convert_plus')],
        [InlineKeyboardButton(f"🔄 Reset", callback_data='num_reset')]
    ])
    
    main_country = f"{country_info['flag']} {country_info['name_en']} ({country_info['short_code']}) +{country_info['code']}"
    
    await query.edit_message_text(
        f"╔══════════════════════════════╗\n"
        f"║     📊 PROCESSING COMPLETE    ║\n"
        f"╠══════════════════════════════╣\n"
        f"║  🌍 Country: {main_country[:25]}\n"
        f"║  🔢 Valid Numbers: {len(numbers)}\n"
        f"║  📝 Sample: `{numbers[0]}`\n"
        f"║  🎲 Random Mode: {random_mode_status}\n"
        f"║  📌 Output: +{country_info['code']}XXXXXXXXX\n"
        f"╚══════════════════════════════╝\n\n"
        f"✅ Mode changed to {random_mode_status}\n👇 Press Convert button to save file",
        reply_markup=inline_keyboard,
        parse_mode="Markdown"
    )


async def num_convert_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    numbers = context.user_data.get('numbers', [])
    random_mode = context.user_data.get('random_mode', False)
    country_info = context.user_data.get('country_info', {'name_en': 'Unknown', 'code': '??'})
    
    if not numbers:
        await query.message.reply_text("❌ NO NUMBERS FOUND!", parse_mode="Markdown")
        return
    
    if random_mode:
        shuffled_numbers = numbers.copy()
        random.shuffle(shuffled_numbers)
        output = "\n".join(shuffled_numbers)
        mode_text = "🎲 Random Order"
    else:
        # সম্পূর্ণ নম্বর অনুযায়ী সাজানো (পুরো ডিজিট)
        # + সাইন থাকলে বাদ দিয়ে integer হিসেবে সাজানো
        def get_full_number(num):
            # + সাইন বাদ দিন
            clean_num = num.lstrip('+')
            # integer তে কনভার্ট করুন
            return int(clean_num)
        
        sorted_numbers = sorted(numbers, key=get_full_number)
        output = "\n".join(sorted_numbers)
        mode_text = "📊 Numerical Order (Full Number)"
    
    filename = f"{country_info['name_en']}_Numbers.txt"
    filepath = os.path.join(BASE_DIR, filename)
    
    with open(filepath, "w") as f:
        f.write(output)
    
    with open(filepath, "rb") as f:
        await query.message.reply_document(
            document=f, 
            filename=filename,
            caption=f"╔══════════════════════════════╗\n"
                    f"║     ✅ CONVERSION COMPLETE    ║\n"
                    f"╠══════════════════════════════╣\n"
                    f"║  🔢 Numbers: {len(numbers)}\n"
                    f"║  🎲 Mode: {mode_text}\n"
                    f"║  📌 Format: +{country_info['code']}XXXXXXXXX\n"
                    f"╚══════════════════════════════╝"
        )
    
    os.remove(filepath)


async def num_convert_plus_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    numbers = context.user_data.get('numbers', [])
    random_mode = context.user_data.get('random_mode', False)
    country_info = context.user_data.get('country_info', {'name_en': 'Unknown', 'code': '??'})
    
    if not numbers:
        await query.message.reply_text("❌ NO NUMBERS FOUND!", parse_mode="Markdown")
        return
    
    if random_mode:
        shuffled_numbers = numbers.copy()
        random.shuffle(shuffled_numbers)
        output = "\n".join([f"+{num}" if not num.startswith('+') else num for num in shuffled_numbers])
        mode_text = "🎲 Random Order"
    else:
        # সম্পূর্ণ নম্বর অনুযায়ী সাজানো (পুরো ডিজিট)
        def get_full_number(num):
            clean_num = num.lstrip('+')
            return int(clean_num)
        
        sorted_numbers = sorted(numbers, key=get_full_number)
        # + সাইন确保 সব নম্বরের শুরুতে + আছে
        output = "\n".join([f"+{num}" if not num.startswith('+') else num for num in sorted_numbers])
        mode_text = "📊 Numerical Order (Full Number)"
    
    filename = f"{country_info['name_en']}_Numbers_With_Plus.txt"
    filepath = os.path.join(BASE_DIR, filename)
    
    with open(filepath, "w") as f:
        f.write(output)
    
    with open(filepath, "rb") as f:
        await query.message.reply_document(
            document=f, 
            filename=filename,
            caption=f"╔══════════════════════════════╗\n"
                    f"║  ✅ CONVERSION (+ FORMAT)    ║\n"
                    f"╠══════════════════════════════╣\n"
                    f"║  🔢 Numbers: {len(numbers)}\n"
                    f"║  🎲 Mode: {mode_text}\n"
                    f"║  📌 Format: +{country_info['code']}XXXXXXXXX\n"
                    f"╚══════════════════════════════╝"
        )
    
    os.remove(filepath)


async def num_reset_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    context.user_data.pop('numbers', None)
    context.user_data.pop('random_mode', None)
    context.user_data.pop('country_info', None)
    
    await query.message.reply_text(
        "┌─────────────────────┐\n│  🔄 RESET DONE      │\n├─────────────────────┤\n│  🗑 Data cleared    │\n│  📁 Ready for new   │\n│  📤 Send file now   │\n└─────────────────────┘",
        parse_mode="Markdown",
        reply_markup=MAIN_MENU
    )