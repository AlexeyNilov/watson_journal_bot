"""
This module contains command handlers for the bot.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.common import authorized_only
from service.event import get_events_for_today


@authorized_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler."""
    await update.message.reply_text("Welcome to Watson!")


@authorized_only
async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with events summary for the current day"""
    events = get_events_for_today(user_id=update.effective_user.id)
    if not events:
        await update.message.reply_html("No events for today.")
    else:
        events_text = "\n".join(f"• {event.text}" for event in events)
        await update.message.reply_html(f"<b>Today's events:</b>\n{events_text}")
