from datetime import datetime, timedelta, timezone

def resolve_time_keyword(keyword: str):
    now = datetime.now(timezone.utc)

    if keyword.startswith("days_"):
        days = int(keyword.split("_")[1])
        start = now - timedelta(days=days)
        end = now

    elif keyword.startswith("hours_"):
        hours = int(keyword.split("_")[1])
        start = now - timedelta(hours=hours)
        end = now

    elif keyword == "yesterday":
        yesterday = now.date() - timedelta(days=1)
        start = datetime.combine(yesterday, datetime.min.time(), tzinfo=timezone.utc)
        end = datetime.combine(yesterday, datetime.max.time(), tzinfo=timezone.utc)

    else:
        raise ValueError("Unsupported time keyword")

    return start, end