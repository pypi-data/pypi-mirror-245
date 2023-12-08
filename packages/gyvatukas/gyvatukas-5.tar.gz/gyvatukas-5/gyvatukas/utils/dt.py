import datetime


def get_dt_utc_now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)
