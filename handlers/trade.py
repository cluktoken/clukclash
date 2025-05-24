from telegram import Update
from telegram.ext import ContextTypes
from db.database import trade_token

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Usage: /buy <TOKEN> <AMOUNT>")
        return
    token, amount = args[0].upper(), int(args[1])
    result = trade_token(update.effective_user.id, token, amount, "buy")
    await update.message.reply_text(result)

async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Usage: /sell <TOKEN> <AMOUNT>")
        return
    token, amount = args[0].upper(), int(args[1])
    result = trade_token(update.effective_user.id, token, amount, "sell")
    await update.message.reply_text(result)