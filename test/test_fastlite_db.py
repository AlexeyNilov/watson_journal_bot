import pytest
from sqlite_minutils.db import Database
from fastlite import Table

from data.fastlite_db import (
    create_event_table,
    prepare_db,
    recreate_db,
    event_structure,
    EventNotFound,
    TABLES,
)


@pytest.fixture
def mock_db():
    return Database(":memory:")


def test_create_event_table(mock_db):
    event_table = create_event_table(mock_db)
    assert isinstance(event_table, Table)
    assert event_table.name == "event"
    assert [col.name for col in event_table.columns] == list(event_structure.keys())
    assert event_table.columns[0].name == "id"
    assert event_table.columns[0].type == "INTEGER"
    assert event_table.columns[0].is_pk == 1


def test_prepare_db(mock_db):
    prepare_db(mock_db)
    assert "event" in [table.name for table in mock_db.tables]


def test_recreate_db(mock_db):
    # First, create some tables
    prepare_db(mock_db)
    assert len(mock_db.tables) > 0

    # Now recreate the database
    recreate_db(mock_db)

    # Check that all tables were dropped and recreated
    assert len(mock_db.tables) == len(TABLES)
    for table_name in TABLES:
        assert table_name in [table.name for table in mock_db.tables]


def test_event_not_found_exception():
    with pytest.raises(EventNotFound):
        raise EventNotFound("Event not found")


def test_tables_dict():
    assert "event" in TABLES
    assert callable(TABLES["event"])
