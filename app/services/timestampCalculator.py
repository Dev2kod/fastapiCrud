from datetime import datetime, timedelta
import re

# time returned as today, yesterday, last_7_days, last_3_months, last_1_year, 3_days_ago, 2_months_ago, 1_year_ago, last_30_minutes, last_2_hours, 15_minutes_ago, 1_hour_ago
# end time is always 23:59:59 of the day or current time for minutes/hours 
# start time is always 00:00:00 of the day
def calculate_time_range(time_str):
    now = datetime.now()
    end_time = now.replace(hour=23, minute=59, second=59, microsecond=0)
    
    if time_str == "today":
        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0) 
    elif time_str == "yesterday":
        start_time = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = (now - timedelta(days=1)).replace(hour=23, minute=59, second=59, microsecond=0)
    elif time_str.startswith("last_") and time_str.endswith("_days"):
        days = int(time_str.split("_")[1])
        start_time = (now - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)    
    elif time_str.startswith("last_") and time_str.endswith("_months"):
        months = int(time_str.split("_")[1])
        start_time = (now - timedelta(days=30*months)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_str.startswith("last_") and time_str.endswith("_years"):
        years = int(time_str.split("_")[1])
        start_time = (now - timedelta(days=365*years)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif time_str.startswith("last_") and time_str.endswith("_minutes"):
        minutes = int(time_str.split("_")[1])
        start_time = now - timedelta(minutes=minutes)
        end_time = now
    elif time_str.startswith("last_") and time_str.endswith("_hours"):
        hours = int(time_str.split("_")[1])
        start_time = now - timedelta(hours=hours)
        end_time = now
    
    elif time_str.endswith("_days_ago"):
        days = int(time_str.split("_")[0])
        start_time = (now - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = (now - timedelta(days=days)).replace(hour=23, minute=59, second=59, microsecond=0)
    elif time_str.endswith("_months_ago"):
        months = int(time_str.split("_")[0])
        start_time = (now - timedelta(days=30*months)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = (now - timedelta(days=30*months)).replace(hour=23, minute=59, second=59, microsecond=0)
    elif time_str.endswith("_years_ago"):
        years = int(time_str.split("_")[0])
        start_time = (now - timedelta(days=365*years)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = (now - timedelta(days=365*years)).replace(hour=23, minute=59, second=59, microsecond=0)
    elif time_str.endswith("_minutes_ago"):
        minutes = int(time_str.split("_")[0])
        start_time = now - timedelta(minutes=minutes)
        end_time = now
    elif time_str.endswith("_hours_ago"):
        hours = int(time_str.split("_")[0])
        start_time = now - timedelta(hours=hours)
        end_time = now  
    else:
        start_time = None
        end_time = None

    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")

    if(start_time and end_time):
        time_range = {
            "start_time": start_time,
            "end_time": end_time
        }
    
    return time_range