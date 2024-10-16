import pytest
from sqlite_minutils.db import Database
from service.repo import save_event, get_events, ProfileNotFound
from service.util import get_current_utc_timestamp


def test_save_event(empty_db):
    text = "Test event"
    user_id = 123

    result = save_event(text, user_id, db=empty_db)

    assert result["text"] == text
    assert result["user_id"] == user_id
    assert "time" in result
    assert isinstance(result["time"], str)


def test_get_events(empty_db):
    user_id = 456
    empty_db.events = [
        {"time": get_current_utc_timestamp(), "user_id": user_id, "text": "Event 1"},
        {"time": get_current_utc_timestamp(), "user_id": user_id, "text": "Event 2"},
        {"time": get_current_utc_timestamp(), "user_id": 789, "text": "Event 3"},
    ]
    for event in empty_db.events:
        save_event(event["text"], event["user_id"], db=empty_db)

    results = get_events(user_id, db=empty_db)

    assert len(results) == 2
    assert results[0]["text"] == "Event 1"
    assert results[1]["text"] == "Event 2"


def test_get_events_empty(empty_db):
    user_id = 999

    results = get_events(user_id, db=empty_db)

    assert len(results) == 0


# Test for ProfileNotFound exception
def test_profile_not_found_exception():
    with pytest.raises(ProfileNotFound):
        raise ProfileNotFound("Profile not found")
