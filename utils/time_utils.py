#!/usr/bin/env python3
"""
Time utility functions for ZenDegenAcademy
Provides Polish relative time calculation and timestamp handling
"""

from datetime import datetime, timezone, timedelta


def get_current_timestamp():
    """
    Get current timestamp in ISO format
    
    Returns:
        str: Current timestamp in 'YYYY-MM-DD HH:MM:SS' format
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def _polish_plural(value, singular, plural, plural_genitive):
    if value == 1:
        return singular
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        return plural
    else:
        return plural_genitive


def calculate_relative_time(timestamp_str: str) -> str:
    final_activity_time: datetime  # Stores the successfully parsed datetime

    try:
        # Attempt to parse with timezone info if present
        if '+' in timestamp_str or 'Z' in timestamp_str.upper():
            _processed_timestamp_str = timestamp_str.upper().replace('Z', '+00:00') if 'Z' in timestamp_str.upper() else timestamp_str
            try:
                final_activity_time = datetime.fromisoformat(_processed_timestamp_str)
            except ValueError:
                final_activity_time = datetime.strptime(_processed_timestamp_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        else:
            # Assume naive datetime is UTC if no timezone info
            try:
                _activity_time_naive = datetime.fromisoformat(timestamp_str)
            except ValueError:
                _activity_time_naive = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
            final_activity_time = _activity_time_naive.replace(tzinfo=timezone.utc)
    except ValueError:
        # Fallback for simpler formats if primary parsing fails
        try:
            _activity_time_naive = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            final_activity_time = _activity_time_naive.replace(tzinfo=timezone.utc)
        except ValueError:
            return "Nieznana data" # All parsing attempts failed

    # If execution reaches here, final_activity_time must have been assigned.

    now = datetime.now(timezone.utc)
    delta = now - final_activity_time
    seconds = delta.total_seconds()

    if seconds < 5:
        return "przed chwilą"
    elif seconds < 60:
        val = int(seconds)
        return f"{val} {_polish_plural(val, 'sekundę', 'sekundy', 'sekund')} temu"
    elif seconds < 3600: # Less than an hour
        val = int(seconds / 60)
        return f"{val} {_polish_plural(val, 'minutę', 'minuty', 'minut')} temu"
    elif seconds < 86400: # Less than a day
        val = int(seconds / 3600)
        return f"{val} {_polish_plural(val, 'godzinę', 'godziny', 'godzin')} temu"
    elif seconds < 604800: # Less than a week
        val = int(seconds / 86400)
        return f"{val} {_polish_plural(val, 'dzień', 'dni', 'dni')} temu"
    elif seconds < 2592000: # Less than a month (approx 30 days)
        val = int(seconds / 604800)
        return f"{val} {_polish_plural(val, 'tydzień', 'tygodnie', 'tygodni')} temu"
    elif seconds < 31536000: # Less than a year (approx 365 days)
        val = int(seconds / 2592000)
        return f"{val} {_polish_plural(val, 'miesiąc', 'miesiące', 'miesięcy')} temu"
    else: # years
        val = int(seconds / 31536000)
        return f"{val} {_polish_plural(val, 'rok', 'lata', 'lat')} temu"


def format_timestamp_display(timestamp_str):
    """
    Format timestamp for display in Polish format
    
    Args:
        timestamp_str (str): Timestamp in 'YYYY-MM-DD HH:MM:SS' format
        
    Returns:
        str: Formatted date string (e.g., "7 grudnia 2024, 15:30")
    """
    if not timestamp_str:
        return "Nieznana data"
    
    try:
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        
        # Polish month names
        months = [
            "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
            "lipca", "sierpnia", "września", "października", "listopada", "grudnia"
        ]
        
        day = timestamp.day
        month = months[timestamp.month - 1]
        year = timestamp.year
        hour = timestamp.hour
        minute = timestamp.minute
        
        return f"{day} {month} {year}, {hour:02d}:{minute:02d}"
        
    except (ValueError, TypeError):
        return "Nieznana data"


def is_recent_timestamp(timestamp_str, hours=1):
    """
    Check if timestamp is recent (within specified hours)
    
    Args:
        timestamp_str (str): Timestamp in 'YYYY-MM-DD HH:MM:SS' format
        hours (int): Number of hours to consider as "recent"
        
    Returns:
        bool: True if timestamp is recent, False otherwise
    """
    if not timestamp_str:
        return False
    
    try:
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        
        diff = now - timestamp
        return diff.total_seconds() <= (hours * 3600)
        
    except (ValueError, TypeError):
        return False


def get_time_of_day():
    """
    Get current time of day in Polish
    
    Returns:
        str: Time of day ("rano", "po południu", "wieczorem", "w nocy")
    """
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        return "rano"
    elif 12 <= current_hour < 18:
        return "po południu"
    elif 18 <= current_hour < 22:
        return "wieczorem"
    else:
        return "w nocy"


if __name__ == '__main__':
    # Test cases
    print(f"UTC Now: {datetime.now(timezone.utc).isoformat()}")
    print(f"5s ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(seconds=5)).isoformat())}")
    print(f"30s ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat())}")
    print(f"1min ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat())}")
    print(f"30min ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat())}")
    print(f"1hr ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(hours=1)).isoformat())}")
    print(f"5hr ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(hours=5)).isoformat())}")
    print(f"1day ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(days=1)).isoformat())}")
    print(f"3days ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(days=3)).isoformat())}")
    print(f"1week ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(weeks=1)).isoformat())}")
    print(f"3weeks ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(weeks=3)).isoformat())}")
    print(f"1month ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(days=35)).isoformat())}") # Approx
    print(f"5months ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(days=150)).isoformat())}") # Approx
    print(f"1year ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(days=370)).isoformat())}") # Approx
    print(f"3years ago: {calculate_relative_time((datetime.now(timezone.utc) - timedelta(days=3*365)).isoformat())}") # Approx
    print(f"Naive time (assumed UTC): {calculate_relative_time('2024-07-20T10:00:00')}")
    print(f"Time with Z: {calculate_relative_time('2024-07-20T10:00:00Z')}")
    print(f"Time with offset: {calculate_relative_time('2024-07-20T12:00:00+02:00')}")
    print(f"Time with microseconds and Z: {calculate_relative_time('2024-07-20T10:00:00.123456Z')}")
    print(f"Time with microseconds and offset: {calculate_relative_time('2024-07-20T12:00:00.123456+02:00')}")
    print(f"Invalid date: {calculate_relative_time('invalid-date-string')}")
