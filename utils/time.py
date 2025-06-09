from datetime import datetime


def format_timestamp(time: float):
    date = datetime.fromtimestamp(time)
    return date.strftime("%H:%M:%S")
