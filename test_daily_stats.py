#!/usr/bin/env python
"""
Test skrypt do testowania funkcji śledzenia dziennych statystyk
"""

import sys
import os

# Dodaj główny katalog do path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

from datetime import datetime, timedelta
from data.users import load_user_data, save_user_data, get_current_user_data
from views.dashboard import save_daily_stats, calculate_stats_changes, format_change_text

def test_daily_stats():
    """Test funkcji dziennych statystyk"""
    
    print("🧪 Test funkcji śledzenia dziennych statystyk")
    print("=" * 50)
    
    # Test dla użytkownika Max
    username = "Max"
    user_data = get_current_user_data(username)
    
    if not user_data:
        print("❌ Użytkownik Max nie istnieje")
        return
    
    print(f"👤 Testujemy dla użytkownika: {username}")
    print(f"📊 Obecne statystyki:")
    print(f"   XP: {user_data.get('xp', 0)}")
    print(f"   Monety: {user_data.get('degencoins', 0)}")
    print(f"   Poziom: {user_data.get('level', 1)}")
    print(f"   Ukończone lekcje: {len(user_data.get('completed_lessons', []))}")
    
    # Sprawdź obecne daily_stats
    daily_stats = user_data.get('daily_stats', {})
    print(f"\n📅 Zapisane dzienne statystyki ({len(daily_stats)} dni):")
    for date, stats in sorted(daily_stats.items()):
        print(f"   {date}: XP={stats['xp']}, Monety={stats['degencoins']}, Poziom={stats['level']}, Lekcje={stats['completed_lessons']}")
    
    # Zapisz dzisiejsze statystyki
    print(f"\n💾 Zapisuję dzisiejsze statystyki...")
    save_daily_stats(username)
    
    # Dodaj sztuczne dane z wczoraj dla testu
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Wczytaj ponownie użytkownika po zapisie
    user_data = get_current_user_data(username)
    
    # Dodaj wczorajsze statystyki (niższe niż dzisiejsze)
    if 'daily_stats' not in user_data:
        user_data['daily_stats'] = {}
    
    user_data['daily_stats'][yesterday] = {
        'xp': max(0, user_data.get('xp', 0) - 50),  # -50 XP wczoraj
        'degencoins': max(0, user_data.get('degencoins', 0) - 50),  # -50 monet wczoraj  
        'level': max(1, user_data.get('level', 1)),  # ten sam poziom
        'completed_lessons': max(0, len(user_data.get('completed_lessons', [])) - 1)  # -1 lekcja wczoraj
    }
    
    # Zapisz zmodyfikowane dane
    users_data = load_user_data()
    users_data[username] = user_data
    save_user_data(users_data)
    
    print(f"🔧 Dodano sztuczne dane z wczoraj: {yesterday}")
    
    # Oblicz zmiany
    current_stats, changes = calculate_stats_changes(username)
    
    print(f"\n📈 Obliczone zmiany w stosunku do wczoraj:")
    for stat_name, change_data in changes.items():
        # Dla XP i monet używamy liczb całkowitych
        if stat_name in ['xp', 'degencoins']:
            change_text, color = format_change_text(change_data, use_absolute=True)
        else:
            change_text, color = format_change_text(change_data, use_absolute=True)
        
        print(f"   {stat_name}: {change_text} (kolor: {color})")
        print(f"     - Zmiana bezwzględna: {change_data['absolute']}")
        print(f"     - Zmiana procentowa: {change_data['percentage']:.1f}%")
    
    print(f"\n✅ Test zakończony pomyślnie!")

if __name__ == "__main__":
    test_daily_stats()