from datetime import datetime


def format_timestamp(time: float):
    date = datetime.fromtimestamp(time)
    print(date)
    return date.strftime("%H:%M:%S")
