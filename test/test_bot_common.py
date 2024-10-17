import pytest
from unittest.mock import AsyncMock, MagicMock
from bot import common
from telegram.constants import ParseMode
from conf.settings import DEVELOPER_CHAT_ID


@pytest.mark.asyncio
async def test_error_handler(update, context):
    context.error = Exception("Test error")
    context.bot.send_message = AsyncMock()

    # Mock the update.to_dict() method to return a serializable object
    update.to_dict = MagicMock(return_value={"update_id": 123456})

    await common.error_handler(update, context)

    context.bot.send_message.assert_called_once()
    args, kwargs = context.bot.send_message.call_args
    assert kwargs["chat_id"] == DEVELOPER_CHAT_ID
    assert "Test error" in kwargs["text"]
    assert kwargs["parse_mode"] == ParseMode.HTML

    # Additional assertions to check for serializable content
    assert "123456" in kwargs["text"]


@pytest.mark.asyncio
async def test_authorized_only_decorator(update, context):
    @common.authorized_only
    async def test_handler(update, context):
        return "Success"

    result = await test_handler(update, context)

    assert result == "Success"


@pytest.mark.asyncio
async def test_authorized_only_decorator_unauthorized(illegal_update, context):
    @common.authorized_only
    async def test_handler(update, context):
        pass

    await test_handler(illegal_update, context)

    illegal_update.message.reply_text.assert_called_once_with(
        "Sorry, you are not authorized to use this bot"
    )


@pytest.mark.asyncio
async def test_authorized_only_decorator_non_private_chat(update, context):
    update.effective_chat.type = "group"

    @common.authorized_only
    async def test_handler(update, context):
        pass

    await test_handler(update, context)

    update.message.reply_text.assert_called_once_with("Please use private chat.")
