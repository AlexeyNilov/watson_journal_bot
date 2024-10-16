from datetime import datetime, timezone


def get_current_utc_timestamp() -> str:
    """Returns the current UTC timestamp in ISO 8601 format with timezone awareness."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
