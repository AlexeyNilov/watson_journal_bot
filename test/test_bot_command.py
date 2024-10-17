import pytest
from bot import command


@pytest.mark.asyncio
async def test_help_command(msg, update, context):
    await command.help_command(update, context)
    msg.reply_text.assert_called_once_with("Welcome to Watson!")


@pytest.mark.asyncio
async def test_help_command_fail(msg, illegal_update, context):
    await command.help_command(illegal_update, context)
    msg.reply_text.assert_called_once_with(
        "Sorry, you are not authorized to use this bot"
    )
