import pytest
from data.repo import (
    save_event,
    get_events,
    search_events,
    ProfileNotFound,
    get_current_utc_timestamp,
)


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


def test_search_events(empty_db, user_id):
    events = [
        {
            "time": get_current_utc_timestamp(),
            "user_id": user_id,
            "text": "Hello world",
        },
        {
            "time": get_current_utc_timestamp(),
            "user_id": user_id,
            "text": "Python is awesome",
        },
        {
            "time": get_current_utc_timestamp(),
            "user_id": user_id,
            "text": "Testing is important",
        },
        {
            "time": get_current_utc_timestamp(),
            "user_id": 789,
            "text": "This should not be found",
        },
    ]
    for event in events:
        save_event(event["text"], event["user_id"], db=empty_db)

    # Test searching for a specific word
    results = search_events("Python", user_id, db=empty_db)
    assert len(results) == 1
    assert results[0]["text"] == "Python is awesome"

    # Test searching for a partial match
    results = search_events("is", user_id, db=empty_db)
    assert len(results) == 2
    assert set(result["text"] for result in results) == {
        "Python is awesome",
        "Testing is important",
    }

    # Test case-insensitive search
    results = search_events("HELLO", user_id, db=empty_db)
    assert len(results) == 1
    assert results[0]["text"] == "Hello world"

    # Test search with no results
    results = search_events("nonexistent", user_id, db=empty_db)
    assert len(results) == 0


def test_search_events_empty_db(empty_db):
    results = search_events("test", 1, db=empty_db)
    assert len(results) == 0
