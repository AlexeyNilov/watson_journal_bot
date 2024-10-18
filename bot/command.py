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
from data.repo import search_events
from service.event import get_events_for_today
from service.llm import (
    get_tweet_from_llm,
    get_retrospection_from_llm,
    get_summary_from_llm,
)
from service.x import post_tweet


@authorized_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a list of available commands to the user with a keyboard menu."""
    commands = [
        ["/summary", "/help"],
    ]

    keyboard = ReplyKeyboardMarkup(commands, resize_keyboard=True, is_persistent=True)

    message = (
        "Here are the available commands:\n\n"
        "/retro 🧠 - Retrospection\n"
        "/summary 📅 - Show today's events\n"
        "/help ❓ - Show this help message\n"
        "/x 📰 - Improve and send to X\n"
        "/s 🔍 - Search events\n"
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
        summary = await get_summary_from_llm(events_text)
        await update.message.reply_html(f"<b>Today's summary:</b>\n{summary}")


@authorized_only
async def retro_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with events summary for the current day"""
    events = get_events_for_today(user_id=update.effective_user.id)
    if not events:
        await update.message.reply_html("No events for today.")
    else:
        events_text = "\n".join(f"• {event.text}" for event in events)
        retro_text = await get_retrospection_from_llm(events_text)
        await update.message.reply_html(f"<b>Retrospection:</b>\n{retro_text}")


@authorized_only
async def x_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("No text provided")
        return
    input_text = " ".join(context.args)
    text = await get_tweet_from_llm(input_text)
    text = text[:280]

    # Store the generated tweet in user_data
    context.user_data["pending_tweet"] = text

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
    if query.data == "yes":
        # Retrieve the stored tweet from user_data
        tweet_text = context.user_data.get("pending_tweet")
        if tweet_text:
            await query.edit_message_text(text="Sending to X...")
            await post_tweet(tweet_text)
            # Clear the pending tweet after posting
            del context.user_data["pending_tweet"]
        else:
            await query.edit_message_text(text="Error: No pending tweet found.")
    else:
        await query.edit_message_text(text="Tweet cancelled.")


@authorized_only
async def s_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("No text provided")
        return
    input_text = " ".join(context.args)
    events = search_events(input_text, update.effective_user.id)
    if not events:
        await update.message.reply_text("No events found")
    else:
        events_text = "\n".join(f"• {event['text']}" for event in events)
        await update.message.reply_html(f"<b>Search results:</b>\n{events_text}")
