#!/usr/bin/env python3
"""
Test admin panel data display for registration_date and last_login
"""

import os
import sys
import json

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def test_admin_data_display():
    """Test prawidłowego wyświetlania dat w panelu administratora"""
    
    print("🧪 Test wyświetlania dat w panelu administratora")
    print("=" * 60)
    
    try:
        # Import after setting up the path
        from views.admin import get_user_activity_data
        from data.users import load_user_data
        
        # Test 1: Load user data directly
        print("\n📊 Test 1: Sprawdzenie danych użytkowników z pliku")
        users_data = load_user_data()
        
        sample_users = list(users_data.keys())[:3]  # Pierwszych 3 użytkowników
        print(f"   Testujemy użytkowników: {sample_users}")
        
        for username in sample_users:
            user_data = users_data[username]
            joined_date = user_data.get('joined_date', 'BRAK')
            last_login = user_data.get('last_login', 'BRAK')
            
            print(f"\n   👤 Użytkownik: {username}")
            print(f"      joined_date: {joined_date}")
            print(f"      last_login: {last_login}")
            
            # Sprawdź czy joined_date nie jest domyślną datą
            if joined_date == '2023-01-01':
                print("      ⚠️ UWAGA: joined_date ma domyślną wartość 2023-01-01")
            elif joined_date and joined_date != 'BRAK':
                print("      ✅ joined_date wygląda poprawnie")
            else:
                print("      ❌ joined_date jest pusty/nieprawidłowy")
        
        # Test 2: Test admin function
        print(f"\n📋 Test 2: Sprawdzenie funkcji get_user_activity_data()")
        activity_df = get_user_activity_data()
        
        print(f"   Znaleziono {len(activity_df)} użytkowników w DataFrame")
        print(f"   Kolumny: {list(activity_df.columns)}")
        
        # Sprawdź kilku pierwszych użytkowników
        for i, row in activity_df.head(3).iterrows():
            username = row['username']
            reg_date = row['registration_date']
            last_login = row['last_login']
            
            print(f"\n   👤 Użytkownik: {username}")
            print(f"      registration_date: {reg_date}")
            print(f"      last_login: {last_login}")
            
            # Sprawdź czy registration_date nie jest domyślną datą
            if reg_date == '2023-01-01':
                print("      ❌ BŁĄD: registration_date nadal ma domyślną wartość 2023-01-01")
            elif reg_date == 'Nieznana':
                print("      ⚠️ registration_date jest 'Nieznana' - może brakować joined_date")
            else:
                print("      ✅ registration_date wygląda poprawnie")
            
            # Sprawdź last_login
            if last_login == '2023-01-01':
                print("      ❌ BŁĄD: last_login nadal ma domyślną wartość 2023-01-01")
            elif last_login in ['Nigdy', 'Brak danych']:
                print("      ✅ last_login prawidłowo pokazuje brak danych")
            elif last_login and last_login not in ['null', None]:
                print("      ✅ last_login ma wartość")
            else:
                print("      ℹ️ last_login jest pusty (OK dla nowych użytkowników)")
        
        # Test 3: Sprawdź konkretne problematyczne przypadki
        print(f"\n🔍 Test 3: Szukanie użytkowników z problematycznymi datami")
        
        problematic_reg_count = len(activity_df[activity_df['registration_date'] == '2023-01-01'])
        problematic_login_count = len(activity_df[activity_df['last_login'] == '2023-01-01'])
        
        print(f"   Użytkownicy z registration_date = '2023-01-01': {problematic_reg_count}")
        print(f"   Użytkownicy z last_login = '2023-01-01': {problematic_login_count}")
        
        if problematic_reg_count == 0 and problematic_login_count == 0:
            print("   ✅ Brak problematycznych dat 2023-01-01!")
        else:
            print("   ❌ Wciąż są problematyczne daty!")
            
            if problematic_reg_count > 0:
                print("      Problematyczne registration_date:")
                problematic_users = activity_df[activity_df['registration_date'] == '2023-01-01']['username'].tolist()
                print(f"      {problematic_users[:5]}")  # Pokaż pierwszych 5
            
            if problematic_login_count > 0:
                print("      Problematyczne last_login:")
                problematic_users = activity_df[activity_df['last_login'] == '2023-01-01']['username'].tolist()
                print(f"      {problematic_users[:5]}")  # Pokaż pierwszych 5
        
        print("\n" + "=" * 60)
        if problematic_reg_count == 0 and problematic_login_count == 0:
            print("✅ Test zakończony sukcesem! Daty wyświetlają się poprawnie.")
            return True
        else:
            print("⚠️ Test wykazał problemy z datami w panelu administratora.")
            return False
        
    except Exception as e:
        print(f"\n❌ Test nie powiódł się: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_admin_data_display()
    sys.exit(0 if success else 1)
