"""
This module contains command handlers for the bot.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.common import authorized_only


@authorized_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler."""
    await update.message.reply_text("Welcome to Watson!")
