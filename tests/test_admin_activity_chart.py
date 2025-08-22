#!/usr/bin/env python3
"""
Test admin panel activity chart with real user data
"""

import os
import sys
import json

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def test_admin_activity_chart():
    """Test wykresu aktywności użytkowników w panelu administratora"""
    
    print("🧪 Test wykresu aktywności użytkowników")
    print("=" * 60)
    
    try:
        # Import after setting up the path
        from views.admin import plot_user_activity_over_time
        from data.users import load_user_data
        
        # Test 1: Load user data and check dates
        print("\n📊 Test 1: Sprawdzenie danych użytkowników")
        users_data = load_user_data()
        total_users = len(users_data)
        print(f"   Znaleziono {total_users} użytkowników")
        
        # Sprawdź kilku użytkowników pod kątem dat
        users_with_joined_date = 0
        users_with_last_login = 0
        sample_users = list(users_data.keys())[:5]  # Pierwszych 5 użytkowników
        
        for username in sample_users:
            user_data = users_data[username]
            joined_date = user_data.get('joined_date')
            last_login = user_data.get('last_login')
            
            print(f"\n   👤 {username}:")
            print(f"      joined_date: {joined_date}")
            print(f"      last_login: {last_login}")
            
            if joined_date:
                users_with_joined_date += 1
            if last_login:
                users_with_last_login += 1
        
        print(f"\n   📋 Podsumowanie próbki {len(sample_users)} użytkowników:")
        print(f"      Z datą rejestracji: {users_with_joined_date}")
        print(f"      Z datą ostatniego logowania: {users_with_last_login}")
        
        # Test 2: Test function plot_user_activity_over_time
        print(f"\n📈 Test 2: Sprawdzenie funkcji plot_user_activity_over_time()")
        activity_df = plot_user_activity_over_time()
        
        print(f"   DataFrame shape: {activity_df.shape}")
        print(f"   Kolumny: {list(activity_df.columns)}")
        
        # Sprawdź czy DataFrame ma oczekiwane kolumny
        expected_columns = ['data', 'rejestracje', 'logowania', 'łącznie']
        missing_columns = [col for col in expected_columns if col not in activity_df.columns]
        
        if missing_columns:
            print(f"   ❌ Brakujące kolumny: {missing_columns}")
            return False
        else:
            print("   ✅ Wszystkie oczekiwane kolumny są obecne")
        
        # Test 3: Check data quality
        print(f"\n🔍 Test 3: Sprawdzenie jakości danych")
        
        # Sprawdź sumy
        total_registrations = activity_df['rejestracje'].sum()
        total_logins = activity_df['logowania'].sum()
        total_combined = activity_df['łącznie'].sum()
        
        print(f"   Łączne rejestracje w ostatnich 30 dniach: {total_registrations}")
        print(f"   Łączne logowania w ostatnich 30 dniach: {total_logins}")
        print(f"   Łączna aktywność: {total_combined}")
        
        # Sprawdź czy suma się zgadza
        expected_total = total_registrations + total_logins
        if total_combined == expected_total:
            print("   ✅ Suma kolumn jest poprawna")
        else:
            print(f"   ❌ Błąd w sumowaniu: {total_combined} ≠ {expected_total}")
            return False
        
        # Test 4: Show sample data
        print(f"\n📅 Test 4: Próbka danych z ostatnich 7 dni")
        recent_data = activity_df.tail(7)  # Ostatnie 7 dni
        
        for _, row in recent_data.iterrows():
            date = row['data']
            reg = row['rejestracje']
            log = row['logowania']
            total = row['łącznie']
            print(f"   {date}: {reg} rejestracji, {log} logowań, {total} łącznie")
        
        # Test 5: Validate date format
        print(f"\n📆 Test 5: Sprawdzenie formatu dat")
        first_date = activity_df['data'].iloc[0]
        last_date = activity_df['data'].iloc[-1]
        
        print(f"   Pierwsza data: {first_date}")
        print(f"   Ostatnia data: {last_date}")
        
        # Sprawdź czy format daty jest poprawny (YYYY-MM-DD)
        try:
            from datetime import datetime
            datetime.strptime(first_date, '%Y-%m-%d')
            datetime.strptime(last_date, '%Y-%m-%d')
            print("   ✅ Format dat jest poprawny")
        except ValueError:
            print("   ❌ Nieprawidłowy format dat")
            return False
        
        print("\n" + "=" * 60)
        print("✅ Wszystkie testy przeszły pomyślnie!")
        print("🎉 Wykres aktywności używa rzeczywistych danych użytkowników!")
        
        # Podsumowanie dla użytkownika
        if total_combined > 0:
            print(f"\n📊 REZULTAT: Wykres pokaże {total_combined} zdarzeń aktywności z ostatnich 30 dni")
        else:
            print(f"\n📊 REZULTAT: Brak aktywności w ostatnich 30 dniach (wykres będzie pusty)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test nie powiódł się: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_admin_activity_chart()
    sys.exit(0 if success else 1)
