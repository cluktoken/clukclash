from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🆘 <b>Cluck Clash Help Menu</b>\n\n"
        "• /start – Begin your Cluck Clash journey 🐣\n"
        "• /tap – Tap to earn $BITS and XP 💥\n"
        "• /market – View current token prices 📊\n"
        "• /buy – Buy $BITS using your cash 💰\n"
        "• /sell – Sell $BITS for cash 💵\n"
        "• /daily – Claim your daily $BITS reward 🎁\n"
        "• /leaderboard – See top players by net worth 🏆\n"
        "• /portfolio – View your $BITS and cash balance 💼\n"
        "• /inventory – See your collected loot and items 🎒\n"
        "• /levelup – Spend XP to level up your player 🎖️\n"
        "• /profile – View your full player profile 📇\n"
        "• /cluckonomy – Global economy stats 🌍\n"
        "• /dividends – Earn passive income from holdings 🪙\n"
        "• /passive – Check passive income status 🌱\n"
        "• /title – Set a custom title for your profile 🏷️\n"
        "• /skin – Set a visual profile skin 🎨\n"
        "• /open – Open a loot box 🎲\n"
        "• /sellall – Sell all inventory items for $BITS 🧹\n"
        "• /pet – View your Cluck Pet 🐔\n"
        "• /feed – Feed your pet 50 $BITS 🍗\n"
        "• /namepet – Name your Cluck Pet 🐣\n"
        "• /dresspet – Give your pet a random cosmetic 👗\n"
        "• /petbattle – Battle another user’s pet ⚔️\n"
        "• /pet_leaderboard – Top 5 pets by XP 🏅\n"
        "• /pet_marketplace – Browse pet skins 🛍️\n"
        "• /pet_fusion – Fuse your pet with mutations 🧬\n"
    )
    await update.message.reply_text(text, parse_mode="HTML")