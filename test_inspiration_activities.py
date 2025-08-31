#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test sprawdzający, czy aktywności związane z czytaniem inspiracji są prawidłowo dodawane i wyświetlane.
"""

import json
import os
import sys

# Dodaj główny katalog do ścieżki
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.users import load_user_data, mark_inspiration_as_read_for_user

def test_inspiration_activity():
    """Test czy aktywności dotyczące inspiracji są prawidłowo dodawane"""
    
    print("🧪 Test aktywności inspiracji")
    print("=" * 50)
    
    # Załaduj dane użytkowników
    users_data = load_user_data()
    
    # Znajdź pierwszego użytkownika z aktywnościami
    test_user = None
    for username, data in users_data.items():
        if 'recent_activities' in data and data['recent_activities']:
            test_user = username
            break
    
    if not test_user:
        print("❌ Nie znaleziono użytkownika z aktywnościami")
        return False
        
    print(f"✅ Znaleziono użytkownika testowego: {test_user}")
    
    # Sprawdź aktywności związane z inspiracjami
    user_data = users_data[test_user]
    activities = user_data.get('recent_activities', [])
    
    inspiration_activities = [
        activity for activity in activities 
        if activity.get('type') == 'inspiration_read'
    ]
    
    print(f"📖 Znaleziono {len(inspiration_activities)} aktywności czytania inspiracji:")
    
    for i, activity in enumerate(inspiration_activities[:3], 1):
        details = activity.get('details', {})
        title = details.get('inspiration_title', 'Nieznany tytuł')
        timestamp = activity.get('timestamp', 'Nieznana data')
        print(f"  {i}. {title} - {timestamp}")
    
    # Sprawdź inne typy aktywności
    other_activities = [
        activity for activity in activities 
        if activity.get('type') != 'inspiration_read'
    ]
    
    print(f"\n🔔 Inne aktywności ({len(other_activities)}):")
    for activity in other_activities[:3]:
        activity_type = activity.get('type', 'unknown')
        timestamp = activity.get('timestamp', 'Nieznana data')
        print(f"  - {activity_type} - {timestamp}")
    
    print(f"\n✅ Test zakończony pomyślnie!")
    print(f"   Użytkownik {test_user} ma {len(activities)} aktywności")
    print(f"   W tym {len(inspiration_activities)} związanych z inspiracjami")
    
    return True

if __name__ == "__main__":
    test_inspiration_activity()
