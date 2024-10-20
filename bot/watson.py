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
    ConversationHandler,
)
from data.logger import set_logging
from bot.common import error_handler, cancel
from bot.command import (
    help_command,
    summary_command,
    x_command,
    x_command_end,
    s_command,
    retro_command,
    skippy_command,
    emo_command,
    emo_command_stage_1,
    emo_command_stage_2,
    emo_command_stage_end,
)
from bot.message import parse_message

set_logging()


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    x_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("x", x_command)],
        states={
            0: [
                CallbackQueryHandler(x_command_end),
            ],
        },
        fallbacks=[CommandHandler("cancel", callback=cancel)],
        per_message=False,
    )

    emo_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("emo", emo_command)],
        states={
            0: [
                CallbackQueryHandler(emo_command_stage_1),
            ],
            1: [
                CallbackQueryHandler(emo_command_stage_2),
            ],
            2: [
                CallbackQueryHandler(emo_command_stage_end),
            ],
        },
        fallbacks=[CommandHandler("cancel", callback=cancel)],
        per_message=False,
    )

    application.add_handler(x_conversation_handler)
    application.add_handler(emo_conversation_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("s", s_command))
    application.add_handler(CommandHandler("summary", summary_command))
    application.add_handler(CommandHandler("retro", retro_command))
    application.add_handler(CommandHandler("skippy", skippy_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, parse_message)
    )
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
