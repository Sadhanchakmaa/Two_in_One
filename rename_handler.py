# rename_handler.py
import os
import re
import shutil
from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, filters, CommandHandler, ContextTypes

from config import MAIN_MENU, BACK_FB_MENU, BASE_DIR

WAITING_FOR_RENAME_FILE = 1
WAITING_FOR_NEW_FILENAME = 2

# Custom Premium Emoji IDs
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
    "🔐": "5472308992514464048"
}


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✨"]}">✨</tg-emoji> Cancelled! Returning to Main Menu <tg-emoji emoji-id="{CUSTOM_EMOJI["🏠"]}">🏠</tg-emoji>',
        parse_mode='HTML',
        reply_markup=MAIN_MENU
    )
    return ConversationHandler.END


async def handle_rename_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "BACK":
        if 'original_file_path' in context.user_data:
            path = context.user_data['original_file_path']
            if os.path.exists(path):
                os.remove(path)
        context.user_data.clear()
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔙"]}">🔙</tg-emoji> <b>BACK TO MENU</b>',
            parse_mode='HTML',
            reply_markup=MAIN_MENU
        )
        return ConversationHandler.END
    
    if not update.message.document:
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["❌"]}">❌</tg-emoji> <b>NO FILE DETECTED</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📥"]}">📥</tg-emoji> Send a valid file\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📂"]}">📂</tg-emoji> .txt | .csv | .xlsx\n\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔙"]}">🔙</tg-emoji> Or press BACK to cancel',
            parse_mode='HTML',
            reply_markup=BACK_FB_MENU
        )
        return WAITING_FOR_RENAME_FILE
    
    file = await update.message.document.get_file()
    file_name = update.message.document.file_name
    
    if file_name.endswith('.xlsx'):
        file_ext = '.xlsx'
    elif file_name.endswith('.csv'):
        file_ext = '.csv'
    elif file_name.endswith('.txt'):
        file_ext = '.txt'
    else:
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["❌"]}">❌</tg-emoji> <b>UNSUPPORTED FORMAT</b>\n\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✅"]}">✅</tg-emoji> <b>Supported formats:</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📄"]}">📄</tg-emoji> • .txt\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📄"]}">📄</tg-emoji> • .csv\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📄"]}">📄</tg-emoji> • .xlsx',
            parse_mode='HTML',
            reply_markup=BACK_FB_MENU
        )
        return WAITING_FOR_RENAME_FILE
    
    original_path = os.path.join(BASE_DIR, f"original_{file.file_id}{file_ext}")
    await file.download_to_drive(original_path)
    
    context.user_data['original_file_path'] = original_path
    context.user_data['original_file_ext'] = file_ext
    context.user_data['original_file_name'] = file_name
    
    await update.message.reply_text(
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📄"]}">📄</tg-emoji> <b>FILE RECEIVED</b>\n\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔥"]}">🔥</tg-emoji> <b>Name:</b> <code>{file_name[:30]}</code>\n\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✏️"]}">✏️</tg-emoji> <b>Send new file name</b>\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🎯"]}">🎯</tg-emoji> (without extension)\n\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📝"]}">📝</tg-emoji> <b>Example:</b> <code>my_renamed_file</code>\n\n'
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔙"]}">🔙</tg-emoji> Press BACK to cancel',
        parse_mode='HTML',
        reply_markup=BACK_FB_MENU
    )
    return WAITING_FOR_NEW_FILENAME


async def handle_new_filename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if text == "BACK":
        if 'original_file_path' in context.user_data:
            path = context.user_data['original_file_path']
            if os.path.exists(path):
                os.remove(path)
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔙"]}">🔙</tg-emoji> <b>BACK TO MENU</b>',
            parse_mode='HTML',
            reply_markup=MAIN_MENU
        )
        return ConversationHandler.END
    
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', text).replace(' ', '_')
    
    if not safe_name:
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["❌"]}">❌</tg-emoji> <b>INVALID NAME</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✏️"]}">✏️</tg-emoji> Try another\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📝"]}">📝</tg-emoji> Use letters & numbers only',
            parse_mode='HTML'
        )
        return WAITING_FOR_NEW_FILENAME
    
    original_path = context.user_data.get('original_file_path')
    file_ext = context.user_data.get('original_file_ext', '.txt')
    
    if not original_path or not os.path.exists(original_path):
        await update.message.reply_text(
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["❌"]}">❌</tg-emoji> <b>FILE NOT FOUND</b>\n'
            f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🔄"]}">🔄</tg-emoji> Please restart the process',
            parse_mode='HTML',
            reply_markup=MAIN_MENU
        )
        return ConversationHandler.END
    
    new_filename = f"{safe_name}{file_ext}"
    new_path = os.path.join(BASE_DIR, new_filename)
    
    shutil.copy2(original_path, new_path)
    
    with open(new_path, "rb") as f:
        await update.message.reply_document(
            document=f, 
            filename=new_filename,
            caption=f'<tg-emoji emoji-id="{CUSTOM_EMOJI["✅"]}">✅</tg-emoji> <b>FILE RENAMED SUCCESSFULLY</b>\n\n'
                    f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📄"]}">📄</tg-emoji> <b>Original:</b> <code>{context.user_data.get("original_file_name", "Unknown")[:30]}</code>\n'
                    f'<tg-emoji emoji-id="{CUSTOM_EMOJI["📄"]}">📄</tg-emoji> <b>New:</b> <code>{new_filename[:30]}</code>',
            parse_mode='HTML'
        )
    
    os.remove(original_path)
    os.remove(new_path)
    
    context.user_data.clear()
    await update.message.reply_text(
        f'<tg-emoji emoji-id="{CUSTOM_EMOJI["🏠"]}">🏠</tg-emoji> <b>BACK TO MENU</b>',
        parse_mode='HTML',
        reply_markup=MAIN_MENU
    )
    return ConversationHandler.END


def rename_conversation_handler():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^FILE CHANGE$"), handle_rename_file)],
        states={
            WAITING_FOR_RENAME_FILE: [MessageHandler(filters.ALL, handle_rename_file)],
            WAITING_FOR_NEW_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_filename)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )