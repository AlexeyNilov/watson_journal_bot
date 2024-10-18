import pytest
from telegram import KeyboardButton
from bot import command


@pytest.mark.asyncio
async def test_help_command(msg, update, context):
    await command.help_command(update, context)
    msg.reply_text.assert_called_once()
    call_args = msg.reply_text.call_args[0][0]
    assert "Here are the available commands:" in call_args

    keyboard = msg.reply_text.call_args[1]["reply_markup"]
    assert keyboard.resize_keyboard is True
    assert keyboard.is_persistent is True
    assert keyboard.keyboard[-1] == (
        KeyboardButton(text="/summary"),
        KeyboardButton(text="/help"),
    )


@pytest.mark.asyncio
async def test_help_command_fail(msg, illegal_update, context):
    await command.help_command(illegal_update, context)
    msg.reply_text.assert_called_once_with(
        "Sorry, you are not authorized to use this bot"
    )


# @pytest.mark.asyncio
# async def test_summary_command_empty(msg, update, context):
#     await command.summary_command(update, context)
#     msg.reply_html.assert_called_once_with("No events for today.")


# @pytest.mark.asyncio
# async def test_summary_command_with_events(msg, update, context, db_with_events):
#     await command.summary_command(update, context)
#     msg.reply_html.assert_called_once()
#     call_args = msg.reply_html.call_args[0][0]
#     assert "<b>Today's summary:</b>" in call_args
#     assert "• Today's event 1" in call_args
#     assert "• Today's event 2" in call_args
#     assert "Yesterday's event" not in call_args
#     assert "Tomorrow's event" not in call_args


@pytest.mark.asyncio
async def test_s_command_no_args(update, context):
    context.args = []
    await command.s_command(update, context)
    update.message.reply_text.assert_called_once_with("No text provided")


@pytest.mark.asyncio
async def test_s_command_no_events(update, context, mocker):
    context.args = ["search", "term"]
    mocker.patch("bot.command.search_events", return_value=[])
    await command.s_command(update, context)
    update.message.reply_text.assert_called_once_with("No events found")


@pytest.mark.asyncio
async def test_s_command_with_events(update, context, mocker):
    context.args = ["search", "term"]
    mock_events = [
        {"id": 1, "text": "Event 1", "user_id": update.effective_user.id},
        {"id": 2, "text": "Event 2", "user_id": update.effective_user.id},
    ]
    mocker.patch("bot.command.search_events", return_value=mock_events)

    await command.s_command(update, context)

    expected_response = "<b>Search results:</b>\n• Event 1\n• Event 2"
    update.message.reply_html.assert_called_once_with(expected_response)


@pytest.mark.asyncio
async def test_s_command_search_events_called_correctly(update, context, mocker):
    context.args = ["search", "term"]
    mock_search_events = mocker.patch("bot.command.search_events", return_value=[])

    await command.s_command(update, context)

    mock_search_events.assert_called_once_with("search term", update.effective_user.id)
