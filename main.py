import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
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
from handlers.reroll import reroll
from handlers.cluckonomy import cluckonomy
from handlers.dividends import dividends
from handlers.passive_income import passive_income
from handlers.title import set_title
from handlers.cluck_engagement_features import craft, mission, pet_marketplace
from handlers.cluck_expansion_missions_trading_ui import daily_missions, craft_menu, handle_craft_click, trade
from handlers.loot_features import open_loot, sell_all
from handlers.skin import set_skin
from handlers.loot_addons_clucklair_iteminfo_crates import iteminfo, clucklair, open_common, open_epic

from db.database import upgrade_schema
from handlers.help_command import help_command
from handlers.cluck_pet_system_full import (
    pet, feed, namepet, dresspet, pet_battle,
    pet_leaderboard, pet_marketplace, pet_fusion
)
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
    application.add_handler(CommandHandler("pet", pet))
    application.add_handler(CommandHandler("feed", feed))
    application.add_handler(CommandHandler("namepet", namepet))
    application.add_handler(CommandHandler("dresspet", dresspet))
    application.add_handler(CommandHandler("petbattle", pet_battle))
    application.add_handler(CommandHandler("pet_leaderboard", pet_leaderboard))
    application.add_handler(CommandHandler("pet_marketplace", pet_marketplace))
    application.add_handler(CommandHandler("pet_fusion", pet_fusion))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reroll", reroll))
    application.add_handler(CommandHandler("collection", collection))
    application.add_handler(CommandHandler("iteminfo", iteminfo))
    application.add_handler(CommandHandler("clucklair", clucklair))
    application.add_handler(CommandHandler("open_common", open_common))
    application.add_handler(CommandHandler("open_epic", open_epic))
    application.add_handler(CommandHandler("craft", craft))
    application.add_handler(CommandHandler("mission", mission))
    application.add_handler(CommandHandler("dailymissions", daily_missions))
    application.add_handler(CommandHandler("craftmenu", craft_menu))
    application.add_handler(CallbackQueryHandler(handle_craft_click, pattern="^craft_"))
    application.add_handler(CommandHandler("trade", trade))

    
    application.run_polling()

if __name__ == "__main__":
    main()
