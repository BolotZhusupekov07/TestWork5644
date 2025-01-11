from datetime import datetime


def convert_datetime_to_str(date: datetime) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%S.%f")
