"""
This module contains utility functions for the bot.
"""

from telegram import Chat, Update
from telegram.ext import ContextTypes, ConversationHandler
from service import repo
from functools import wraps
import logging
from typing import Callable, Any
import traceback
from conf.settings import DEVELOPER_CHAT_ID
import json
import html
from telegram.constants import ParseMode
from conf.settings import AUTHORIZED_IDS


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global error handler to catch exceptions."""
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)
    logging.error(f"Error: {context.error}")
    logging.error(f"{tb_string}")
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        "An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )


def authorized_only(handler: Callable) -> Callable:
    """Decorator to restrict command handlers to authorized users only."""

    @wraps(handler)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        if update.effective_chat.type != Chat.PRIVATE:
            await update.message.reply_text("Please use private chat.")
            return

        if update.effective_user.id not in AUTHORIZED_IDS:
            await update.message.reply_text(
                "Sorry, you are not authorized to use this bot, /join first"
            )
            return

        return await handler(update, context)

    return wrapper
