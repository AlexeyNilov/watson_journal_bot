from datetime import datetime, timezone
from model.event import Event
from data.repo import DB, Database


def get_events_for_today(user_id: int, db: Database = DB) -> list[Event]:
    """Get events for the current day"""
    current_date = datetime.now(tz=timezone.utc).date().isoformat()

    sql = f"""
    SELECT * FROM event
    WHERE user_id = {user_id}
    AND date(time) = date('{current_date}')
    ORDER BY time ASC;
    """

    events = db.q(sql)
    return [Event(**event) for event in events]
