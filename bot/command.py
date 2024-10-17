"""
This module contains command handlers for the bot.
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from bot.common import authorized_only
from service.event import get_events_for_today


@authorized_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a list of available commands to the user with a keyboard menu."""
    commands = [
        ["/summary", "/help"],
    ]

    keyboard = ReplyKeyboardMarkup(commands, resize_keyboard=True, is_persistent=True)

    message = (
        "Here are the available commands:\n\n"
        "/summary 📅 - Show today's events\n"
        "/help ❓ - Show this help message\n"
    )

    await update.message.reply_text(message, reply_markup=keyboard)


@authorized_only
async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with events summary for the current day"""
    events = get_events_for_today(user_id=update.effective_user.id)
    if not events:
        await update.message.reply_html("No events for today.")
    else:
        events_text = "\n".join(f"• {event.text}" for event in events)
        await update.message.reply_html(f"<b>Today's events:</b>\n{events_text}")
