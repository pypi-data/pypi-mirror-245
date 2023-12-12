from datetime import timedelta


def milliseconds(delta: timedelta) -> int:
    return int(delta.total_seconds() * 1000.0)
