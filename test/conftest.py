import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlite_minutils.db import Database
from telegram import Update, Chat, Message, User
from telegram.ext import ContextTypes

import os
from datetime import datetime, timezone, timedelta


os.environ["WATSON_DB_PATH"] = "db/test_empty.sqlite"
from data.fastlite_db import recreate_db, DB
from data.repo import save_event


@pytest.fixture
def user_id():
    return 123456789


@pytest.fixture
def authorized_user(user_id) -> User:
    return User(id=user_id, is_bot=False, first_name="TestUser")


@pytest.fixture
def msg() -> MagicMock:
    message = MagicMock(spec=Message)
    message.reply_text = AsyncMock()
    return message


@pytest.fixture
def update(authorized_user, msg) -> MagicMock:
    recreate_db()
    upd = MagicMock(spec=Update)
    upd.message = msg
    upd.effective_message = AsyncMock(spec=Message)
    upd.effective_user = authorized_user
    upd.effective_chat.type = Chat.PRIVATE
    upd.effective_chat.id = 123456
    return upd


@pytest.fixture
def context():
    ctx = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    ctx.job_queue = MagicMock()
    ctx.job_queue.run_once = MagicMock()
    ctx.job_queue.get_jobs_by_name = MagicMock(return_value=[])
    return ctx


@pytest.fixture
def illegal_user():
    return User(id=111111111, is_bot=False, first_name="TestUser")


@pytest.fixture
def illegal_update(illegal_user, msg):
    upd = MagicMock(spec=Update)
    upd.effective_user = illegal_user
    upd.message = msg
    upd.effective_chat.type = Chat.PRIVATE
    return upd


@pytest.fixture
def empty_db() -> Database:
    recreate_db(DB)
    return DB


@pytest.fixture
def db_with_events(empty_db, user_id) -> Database:

    # Create events for yesterday, today, and tomorrow
    yesterday = datetime.now(tz=timezone.utc) - timedelta(days=1)
    tomorrow = datetime.now(tz=timezone.utc) + timedelta(days=1)

    save_event(
        text="Yesterday's event",
        user_id=user_id,
        time=yesterday.isoformat(),
        db=empty_db,
    )
    save_event(text="Today's event 1", user_id=user_id, db=empty_db)
    save_event(text="Today's event 2", user_id=user_id, db=empty_db)
    save_event(
        text="Tomorrow's event", user_id=user_id, time=tomorrow.isoformat(), db=empty_db
    )
    return empty_db
