import pytest
from datetime import datetime, timedelta, timezone
from model.event import Event
from data.repo import save_event
from service.event import get_events_for_today


@pytest.fixture
def setup_test_data(empty_db, user_id):

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


def test_get_events_for_today(setup_test_data, user_id):
    events = get_events_for_today(user_id=user_id, db=setup_test_data)

    assert isinstance(events, list)
    assert len(events) == 2  # Only today's events should be returned

    current_date = datetime.now(tz=timezone.utc).date().isoformat()
    for event in events:
        assert isinstance(event, Event)
        assert datetime.fromisoformat(event.time).date().isoformat() == current_date
        assert "Today's event" in event.text
