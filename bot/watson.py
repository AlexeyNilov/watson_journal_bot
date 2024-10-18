"""
This module contains the main bot logic.
"""

from conf.settings import BOT_TOKEN
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from data.logger import set_logging
from bot.common import error_handler
from bot.command import (
    help_command,
    summary_command,
    x_command,
    x_button,
    s_command,
    retro_command,
)
from bot.message import parse_message

set_logging()


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("x", x_command))
    application.add_handler(CommandHandler("s", s_command))
    application.add_handler(CallbackQueryHandler(x_button))
    application.add_handler(CommandHandler("summary", summary_command))
    application.add_handler(CommandHandler("retro", retro_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, parse_message)
    )
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
