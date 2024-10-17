"""
This module contains command handlers for the bot.
"""

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes
from bot.common import authorized_only
from service.event import get_events_for_today
from service.llm import get_tweet_from_llm_mock


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


@authorized_only
async def x_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = await get_tweet_from_llm_mock("test")
    await update.message.reply_text(text)
    keyboard = [
        [
            InlineKeyboardButton("yes", callback_data="yes"),
            InlineKeyboardButton("no", callback_data="no"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Send to X?", reply_markup=reply_markup)


@authorized_only
async def x_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")
