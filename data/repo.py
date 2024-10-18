from data.fastlite_db import DB
from sqlite_minutils.db import Database
from datetime import datetime, timezone
from typing import Optional, List, Dict


class ProfileNotFound(Exception):
    pass


def get_current_utc_timestamp() -> str:
    """Returns the current UTC timestamp in ISO 8601 format with timezone awareness."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def save_event(
    text: str, user_id: int, time: Optional[str] = None, db: Database = DB
) -> dict:
    if time is None:
        time = get_current_utc_timestamp()
    return db.t.event.insert(time=time, user_id=user_id, text=text)


def get_events(user_id: int, db: Database = DB) -> list[dict]:
    query = f"SELECT * FROM event WHERE user_id = {user_id};"
    return db.q(query)


def search_events(search_text: str, user_id: int, db: Database = DB) -> List[Dict]:
    query = f"SELECT * FROM event WHERE text LIKE '%{search_text}%' AND user_id = {user_id};"
    return db.q(query)
