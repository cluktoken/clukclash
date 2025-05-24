import os
import asyncio
from telegram.ext import Application, CommandHandler
from handlers.start import start
from handlers.tap import tap
from handlers.trade import buy, sell
from handlers.market import market
from handlers.leaderboard import leaderboard
from db.database import init_db

import asyncio

async def main():
    init_db()
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tap", tap))
    application.add_handler(CommandHandler("market", market))
    application.add_handler(CommandHandler("buy", buy))
    application.add_handler(CommandHandler("sell", sell))
    application.add_handler(CommandHandler("leaderboard", leaderboard))

    await application.run_polling()

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()

    asyncio.get_event_loop().run_until_complete(setup_bot())
