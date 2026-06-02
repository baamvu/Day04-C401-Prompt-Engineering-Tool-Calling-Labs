from __future__ import annotations

from datetime import datetime, timezone, timedelta


VIETNAM_TZ = timezone(timedelta(hours=7))

WEEKDAY_NAMES = {
    0: "Thứ Hai",
    1: "Thứ Ba",
    2: "Thứ Tư",
    3: "Thứ Năm",
    4: "Thứ Sáu",
    5: "Thứ Bảy",
    6: "Chủ Nhật",
}


def get_datetime_info(timezone_offset: int = 7) -> dict:
    try:
        tz = timezone(timedelta(hours=timezone_offset))
    except Exception:
        tz = VIETNAM_TZ

    now = datetime.now(tz)
    weekday = WEEKDAY_NAMES.get(now.weekday(), "")

    return {
        "tool": "datetime_info",
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "day_of_week": weekday,
        "day": now.day,
        "month": now.month,
        "year": now.year,
        "timestamp": int(now.timestamp()),
        "iso_format": now.isoformat(),
        "timezone_offset": timezone_offset,
    }
