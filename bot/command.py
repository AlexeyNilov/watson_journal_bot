"""
This module contains command handlers for the bot.
"""

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, ConversationHandler
from bot.common import authorized_only
from data.repo import search_events, save_event
from service.event import get_events_for_today
from service.llm import get_tweet, get_retrospection, get_summary, ask_skippy
from service.x import post_tweet
from feelings.loader import FEELINGS, get_sub_feelings


@authorized_only
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a list of available commands to the user with a keyboard menu."""
    commands = [
        ["/retro", "/emo"],
        ["/summary", "/help"],
    ]

    keyboard = ReplyKeyboardMarkup(commands, resize_keyboard=True, is_persistent=True)

    message = (
        "Here are the available commands:\n\n"
        "/retro 🧠 - Retrospection\n"
        "/summary 📅 - Summary of today's events\n"
        "/help ❓ - Show this help message\n"
        "/x 📰 - Improve and send to X\n"
        "/s 🔍 - Search events\n"
        "/skippy 🤖 - Ask Skippy\n"
        "/emo 🌈 - Track your feelings\n"
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
        summary = await get_summary(events_text)
        await update.message.reply_html(f"<b>Today's summary:</b>\n{summary}")


@authorized_only
async def retro_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reply with events summary for the current day"""
    events = get_events_for_today(user_id=update.effective_user.id)
    if not events:
        await update.message.reply_html("No events for today.")
    else:
        events_text = "\n".join(f"• {event.text}" for event in events)
        retro_text = await get_retrospection(events_text)
        await update.message.reply_html(f"<b>Retrospection:</b>\n{retro_text}")


@authorized_only
async def x_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("No text provided")
        return
    input_text = " ".join(context.args)
    text = await get_tweet(input_text)
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
    return 0


@authorized_only
async def x_command_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    return ConversationHandler.END


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


@authorized_only
async def skippy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("No text provided")
        return
    input_text = " ".join(context.args)
    response = await ask_skippy(input_text)
    await update.message.reply_text(f"{response}")


def get_keyboard(data: list):
    keyboard = []
    for key in sorted(data):
        keyboard.append([InlineKeyboardButton(key, callback_data=key)])

    return InlineKeyboardMarkup(keyboard)


@authorized_only
async def emo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = get_keyboard(list(FEELINGS.keys()))
    await update.message.reply_text("How do you feel?", reply_markup=reply_markup)
    return 0


@authorized_only
async def emo_command_stage_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feelings_path = list()
    query = update.callback_query
    await query.answer()
    next_feeling = query.data
    feelings_path.append(next_feeling)
    context.user_data["feelings"] = feelings_path
    sub_feelings = get_sub_feelings(name=next_feeling)
    reply_markup = get_keyboard(sub_feelings)
    await query.edit_message_text(text="How do you feel?", reply_markup=reply_markup)
    return 1


@authorized_only
async def emo_command_stage_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feelings_path = context.user_data["feelings"]
    query = update.callback_query
    await query.answer()
    next_feeling = query.data
    feelings_path.append(next_feeling)
    context.user_data["feelings"] = feelings_path
    sub_feelings = get_sub_feelings(name=next_feeling)
    reply_markup = get_keyboard(sub_feelings)
    await query.edit_message_text(text="How do you feel?", reply_markup=reply_markup)
    return 2


@authorized_only
async def emo_command_stage_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feelings_path = context.user_data["feelings"]
    query = update.callback_query
    await query.answer()
    next_feeling = query.data
    feelings_path.append(next_feeling)
    feelings_icon = get_sub_feelings(name=next_feeling)
    feelings_path.append(feelings_icon)
    feelings_text = " -> ".join(feelings_path)
    feelings_text = f"I feel: {feelings_text}"
    await query.edit_message_reply_markup(reply_markup=None)
    await query.edit_message_text(text=feelings_text)
    save_event(text=feelings_text, user_id=update.effective_user.id)
    return ConversationHandler.END
