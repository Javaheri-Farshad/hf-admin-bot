import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# 🔹 اطلاعات تو
BOT_TOKEN = "8248572511:AAH14qNEHCFDF9UwT8Fpebfca8Jqkh7Mc1w"
ADMIN_ID = 6143956856  # آیدی عددی خودت

# 🔹 مراحل مکالمه
ASK_TASKS, ASK_DIRECTS, ASK_SALES, ASK_ISSUES = range(4)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 لطفاً کارهای انجام‌شده امروز رو بفرست:")
    return ASK_TASKS

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tasks"] = update.message.text
    await update.message.reply_text("تعداد دایرکت‌های پاسخ داده شده امروز:")
    return ASK_DIRECTS

async def directs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["directs"] = update.message.text
    await update.message.reply_text("تعداد فروش یا سفارش امروز:")
    return ASK_SALES

async def sales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["sales"] = update.message.text
    await update.message.reply_text("مشکلات یا موارد خاص امروز:")
    return ASK_ISSUES

async def issues(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["issues"] = update.message.text

    report = f"""
📅 گزارش روزانه
📝 کارها: {context.user_data['tasks']}
📩 دایرکت‌ها: {context.user_data['directs']}
💰 فروش: {context.user_data['sales']}
⚠️ مشکلات: {context.user_data['issues']}
"""

    # ارسال گزارش به مدیر
    await context.bot.send_message(chat_id=ADMIN_ID, text=report)
    await update.message.reply_text("✅ گزارش شما ارسال شد. ممنون 🙏")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("گزارش‌گیری لغو شد ❌")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_TASKS: [MessageHandler(filters.TEXT & ~filters.COMMAND, tasks)],
            ASK_DIRECTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, directs)],
            ASK_SALES: [MessageHandler(filters.TEXT & ~filters.COMMAND, sales)],
            ASK_ISSUES: [MessageHandler(filters.TEXT & ~filters.COMMAND, issues)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
