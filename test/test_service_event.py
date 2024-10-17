from datetime import datetime, timezone
from model.event import Event
from service.event import get_events_for_today


def test_get_events_for_today(db_with_events, user_id):
    events = get_events_for_today(user_id=user_id, db=db_with_events)

    assert isinstance(events, list)
    assert len(events) == 2  # Only today's events should be returned

    current_date = datetime.now(tz=timezone.utc).date().isoformat()
    for event in events:
        assert isinstance(event, Event)
        assert datetime.fromisoformat(event.time).date().isoformat() == current_date
        assert "Today's event" in event.text
