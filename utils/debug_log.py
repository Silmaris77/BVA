"""
Logowanie debugowania do pliku - aby zobaczyć co się dzieje
"""

import os
from datetime import datetime

LOG_FILE = "business_games_debug.log"

def log_debug(message):
    """Zapisz wiadomość debug do pliku"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

def clear_debug_log():
    """Wyczyść plik loga"""
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        f.write(f"=== DEBUG LOG START: {datetime.now()} ===\n")
