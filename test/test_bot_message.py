import pytest
from bot.message import parse_message


@pytest.mark.asyncio
async def test_parse_message(msg, update, context):
    update.message.text = "10"
    await parse_message(update, context)
    update.message.set_reaction.assert_called_with("👍")
