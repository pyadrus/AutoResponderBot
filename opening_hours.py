import datetime
import pytz


def check_opening_hours(opening_hours: dict):
    # Используем get для получения значения по ключу
    time_zone_name = opening_hours.get("time_zone_name")
    print(f"Временная зона: {time_zone_name}")
    if not time_zone_name:
        raise ValueError("Не указано поле 'time_zone_name' в данных о часах работы.")

    tz = pytz.timezone(time_zone_name)
    print(tz)
    now = datetime.datetime.now(tz)
    print(now)
    monday_start = now - datetime.timedelta(
        days=now.weekday(),
        hours=now.hour,
        minutes=now.minute,
        seconds=now.second,
        microseconds=now.microsecond,
    )
    print(monday_start)
    minutes_since_monday = (now - monday_start).total_seconds() / 60
    print(minutes_since_monday)
    for day in opening_hours.get("opening_hours", []):
        opening_minute = day.get("opening_minute")
        closing_minute = day.get("closing_minute")
        if opening_minute is not None and closing_minute is not None:
            if opening_minute <= minutes_since_monday <= closing_minute:
                return False

    return True
