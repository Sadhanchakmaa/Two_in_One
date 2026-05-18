# rename_handler.py
import os
import re
import shutil
from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, filters, CommandHandler, ContextTypes

from config import MAIN_MENU, BACK_FB_MENU, BASE_DIR

WAITING_FOR_RENAME_FILE = 1
WAITING_FOR_NEW_FILENAME = 2


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("✨ Cancelled! Returning to Main Menu 🏠", reply_markup=MAIN_MENU)
    return ConversationHandler.END


async def handle_rename_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🔙 BACK":
        if 'original_file_path' in context.user_data:
            path = context.user_data['original_file_path']
            if os.path.exists(path):
                os.remove(path)
        context.user_data.clear()
        await update.message.reply_text("┌─────────────────────┐\n│  🔙 BACK TO MENU    │\n└─────────────────────┘", parse_mode="Markdown", reply_markup=MAIN_MENU)
        return ConversationHandler.END
    
    if not update.message.document:
        await update.message.reply_text(
            "┌─────────────────────────────┐\n│  ❌ NO FILE DETECTED        │\n├─────────────────────────────┤\n"
            "│  📤 Send a valid file       │\n│  📁 .txt | .csv | .xlsx     │\n├─────────────────────────────┤\n│  🔙 Or press BACK to cancel │\n└─────────────────────────────┘",
            parse_mode="Markdown", reply_markup=BACK_FB_MENU
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
            "┌─────────────────────────────┐\n│  ❌ UNSUPPORTED FORMAT      │\n├─────────────────────────────┤\n"
            "│  ✅ Supported formats:      │\n│  • .txt                     │\n│  • .csv                     │\n│  • .xlsx                    │\n└─────────────────────────────┘",
            parse_mode="Markdown", reply_markup=BACK_FB_MENU
        )
        return WAITING_FOR_RENAME_FILE
    
    original_path = os.path.join(BASE_DIR, f"original_{file.file_id}{file_ext}")
    await file.download_to_drive(original_path)
    
    context.user_data['original_file_path'] = original_path
    context.user_data['original_file_ext'] = file_ext
    context.user_data['original_file_name'] = file_name
    
    await update.message.reply_text(
        f"┌─────────────────────────────┐\n│  📄 FILE RECEIVED           │\n├─────────────────────────────┤\n"
        f"│  📛 Name: `{file_name[:20]}`│\n├─────────────────────────────┤\n│  ✏️ Send new file name      │\n"
        f"│  (without extension)        │\n├─────────────────────────────┤\n│  📝 Example:                │\n│  `my_renamed_file`          │\n"
        f"├─────────────────────────────┤\n│  🔙 Press BACK to cancel    │\n└─────────────────────────────┘",
        parse_mode="Markdown", reply_markup=BACK_FB_MENU
    )
    return WAITING_FOR_NEW_FILENAME


async def handle_new_filename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if text == "🔙 BACK":
        if 'original_file_path' in context.user_data:
            path = context.user_data['original_file_path']
            if os.path.exists(path):
                os.remove(path)
        await update.message.reply_text("┌─────────────────────┐\n│  🔙 BACK TO MENU    │\n└─────────────────────┘", parse_mode="Markdown", reply_markup=MAIN_MENU)
        return ConversationHandler.END
    
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', text).replace(' ', '_')
    
    if not safe_name:
        await update.message.reply_text(
            "┌─────────────────────┐\n│  ❌ INVALID NAME    │\n├─────────────────────┤\n│  ✏️ Try another     │\n│  📝 Use letters &   │\n│     numbers only    │\n└─────────────────────┘",
            parse_mode="Markdown"
        )
        return WAITING_FOR_NEW_FILENAME
    
    original_path = context.user_data.get('original_file_path')
    file_ext = context.user_data.get('original_file_ext', '.txt')
    
    if not original_path or not os.path.exists(original_path):
        await update.message.reply_text(
            "┌─────────────────────┐\n│  ❌ FILE NOT FOUND  │\n├─────────────────────┤\n│  🔄 Please restart  │\n│     the process     │\n└─────────────────────┘",
            parse_mode="Markdown", reply_markup=MAIN_MENU
        )
        return ConversationHandler.END
    
    new_filename = f"{safe_name}{file_ext}"
    new_path = os.path.join(BASE_DIR, new_filename)
    
    shutil.copy2(original_path, new_path)
    
    with open(new_path, "rb") as f:
        await update.message.reply_document(document=f, filename=new_filename,
            caption=f"╔══════════════════════════════════╗\n║     ✅ FILE RENAMED SUCCESSFULLY   ║\n╠══════════════════════════════════╣\n"
                    f"║  📄 Original: `{context.user_data.get('original_file_name', 'Unknown')[:20]}`\n║  📄 New: `{new_filename[:20]}`\n╚══════════════════════════════════╝",
            parse_mode="Markdown")
    
    os.remove(original_path)
    os.remove(new_path)
    
    context.user_data.clear()
    await update.message.reply_text("┌─────────────────────┐\n│  🏠 BACK TO MENU    │\n└─────────────────────┘", parse_mode="Markdown", reply_markup=MAIN_MENU)
    return ConversationHandler.END


def rename_conversation_handler():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📁 FILE CHANGE$"), handle_rename_file)],
        states={
            WAITING_FOR_RENAME_FILE: [MessageHandler(filters.ALL, handle_rename_file)],
            WAITING_FOR_NEW_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_filename)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )