import os
from telegram.ext import Application, CommandHandler
from handlers.start import start
from handlers.tap import tap
from handlers.trade import buy, sell
from handlers.daily import daily
from handlers.portfolio import portfolio
from handlers.market import market
from handlers.leaderboard import leaderboard
from db.database import init_db, get_user_portfolio, get_price
from handlers.inventory import inventory
from handlers.levelup import levelup
from handlers.profile import profile
from handlers.cluckonomy import cluckonomy
from handlers.dividends import dividends
from handlers.passive_income import passive_income
from handlers.title import set_title
from handlers.loot_features import open_loot, sell_all
from handlers.skin import set_skin
from db.database import upgrade_schema
upgrade_schema()


DB_PATH = "/data/crypto_game.db"


def main():
    init_db()
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tap", tap))
    application.add_handler(CommandHandler("market", market))
    application.add_handler(CommandHandler("buy", buy))
    application.add_handler(CommandHandler("sell", sell))
    application.add_handler(CommandHandler("daily", daily))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("portfolio", portfolio))
    application.add_handler(CommandHandler("inventory", inventory))
    application.add_handler(CommandHandler("levelup", levelup))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("cluckonomy", cluckonomy))
    application.add_handler(CommandHandler("dividends", dividends))
    application.add_handler(CommandHandler("passive", passive_income))
    application.add_handler(CommandHandler("title", set_title))
    application.add_handler(CommandHandler("skin", set_skin))
    application.add_handler(CommandHandler("open", open_loot))
    application.add_handler(CommandHandler("sellall", sell_all))



    
    application.run_polling()

if __name__ == "__main__":
    main()
