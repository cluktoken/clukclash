import os
from telegram.ext import Application, CommandHandler
from handlers.start import start
from handlers.tap import tap
from handlers.trade import buy, sell
from handlers.portfolio import portfolio
from handlers.market import market
from handlers.leaderboard import leaderboard
from db.database import init_db

def main():
    init_db()
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tap", tap))
    application.add_handler(CommandHandler("market", market))
    application.add_handler(CommandHandler("buy", buy))
    application.add_handler(CommandHandler("sell", sell))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("portfolio", portfolio))

    application.run_polling()

if __name__ == "__main__":
    main()
