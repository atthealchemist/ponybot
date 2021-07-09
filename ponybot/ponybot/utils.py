from datetime import timedelta


def beat(hours=0, minutes=0, seconds=0):
    return timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds()
