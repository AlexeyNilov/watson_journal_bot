"""
This module contains command handlers for the bot.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.common import authorized_only


@authorized_only
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler."""
    await update.message.reply_text("Welcome to Watson!")
