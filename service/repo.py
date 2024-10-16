from data.fastlite_db import DB
from sqlite_minutils.db import Database
from service.util import get_current_utc_timestamp


class ProfileNotFound(Exception):
    pass


def save_event(text: str, user_id: int, db: Database = DB) -> dict:
    return db.t.event.insert(
        time=get_current_utc_timestamp(), user_id=user_id, text=text
    )


def get_events(user_id: int, db: Database = DB) -> list[dict]:
    return db.t.event.filter(user_id=user_id)

