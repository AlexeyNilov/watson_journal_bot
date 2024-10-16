"""
This module contains message handlers for the bot.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.common import authorized_only
from service import repo


@authorized_only
async def parse_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message.text:
        return

    repo.save_event(text=update.message.text, user_id=update.effective_user.id)
    await update.message.set_reaction("👍")
