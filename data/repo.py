from data.fastlite_db import DB
from sqlite_minutils.db import Database
from datetime import datetime, timezone


class ProfileNotFound(Exception):
    pass


def get_current_utc_timestamp() -> str:
    """Returns the current UTC timestamp in ISO 8601 format with timezone awareness."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_event(text: str, user_id: int, db: Database = DB) -> dict:
    return db.t.event.insert(
        time=get_current_utc_timestamp(), user_id=user_id, text=text
    )


def get_events(user_id: int, db: Database = DB) -> list[dict]:
    query = f"SELECT * FROM event WHERE user_id = {user_id};"
    return db.q(query)
