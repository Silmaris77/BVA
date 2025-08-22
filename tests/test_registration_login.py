#!/usr/bin/env python3
"""
Test systemu rejestracji i logowania nowych użytkowników
"""

import os
import sys
import json
import tempfile
import shutil
from datetime import datetime

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def test_registration_and_login():
    """Test rejestracji i ponownego logowania użytkownika"""
    
    print("🧪 Test systemu rejestracji i logowania")
    print("=" * 60)
    
    # Create a temporary copy of users_data.json for testing
    original_users_file = os.path.join(project_root, 'users_data.json')
    backup_users_file = os.path.join(project_root, 'users_data_login_test_backup.json')
    
    try:
        # Backup original file
        shutil.copy2(original_users_file, backup_users_file)
        print("📁 Utworzono kopię zapasową users_data.json")
        
        # Import required modules after setting up the path
        from data.users import register_user, login_user, load_user_data, save_user_data
        
        # Test data
        test_username = "test_nowy_uzytkownik"
        test_password = "test123"
        
        # Cleanup any existing test user
        users_data = load_user_data()
        if test_username in users_data:
            del users_data[test_username]
            save_user_data(users_data)
            print(f"🧹 Usunięto istniejącego użytkownika testowego: {test_username}")
        
        # Test 1: Registration
        print(f"\n📝 Test 1: Rejestracja użytkownika '{test_username}'")
        registration_result = register_user(test_username, test_password, test_password)
        print(f"   Wynik rejestracji: '{registration_result}'")
        
        if registration_result == "Registration successful!":
            print("   ✅ Rejestracja zakończona sukcesem")
        else:
            print(f"   ❌ Rejestracja nie powiodła się: {registration_result}")
            return False
        
        # Test 2: Verify user exists in database
        print(f"\n📊 Test 2: Sprawdzenie czy użytkownik został zapisany")
        users_data = load_user_data()
        if test_username in users_data:
            user_data = users_data[test_username]
            print(f"   ✅ Użytkownik znaleziony w bazie danych")
            print(f"   📋 Dane użytkownika:")
            print(f"      - User ID: {user_data.get('user_id', 'BRAK')}")
            print(f"      - Password: {user_data.get('password', 'BRAK')}")
            print(f"      - Level: {user_data.get('level', 'BRAK')}")
            print(f"      - XP: {user_data.get('xp', 'BRAK')}")
            print(f"      - Inspirations: {user_data.get('inspirations', 'BRAK')}")
            
            # Verify inspirations field
            if 'inspirations' in user_data and isinstance(user_data['inspirations'], dict):
                if 'read' in user_data['inspirations'] and 'favorites' in user_data['inspirations']:
                    print("   ✅ Pole inspirations poprawnie zainicjalizowane")
                else:
                    print("   ⚠️ Pole inspirations nie ma wszystkich wymaganych kluczy")
            else:
                print("   ❌ Brak pola inspirations lub niewłaściwy format")
        else:
            print(f"   ❌ Użytkownik {test_username} nie został znaleziony w bazie danych")
            return False
        
        # Test 3: Login attempt
        print(f"\n🔐 Test 3: Próba logowania użytkownika '{test_username}'")
        login_result = login_user(test_username, test_password)
        
        if login_result:
            print("   ✅ Logowanie zakończone sukcesem")
            print(f"   📋 Zwrócone dane użytkownika:")
            print(f"      - User ID: {login_result.get('user_id', 'BRAK')}")
            print(f"      - Level: {login_result.get('level', 'BRAK')}")
            print(f"      - XP: {login_result.get('xp', 'BRAK')}")
        else:
            print("   ❌ Logowanie nie powiodło się")
            return False
        
        # Test 4: Test wrong password
        print(f"\n🚫 Test 4: Próba logowania z błędnym hasłem")
        wrong_login_result = login_user(test_username, "wrong_password")
        
        if wrong_login_result is None:
            print("   ✅ Logowanie z błędnym hasłem prawidłowo odrzucone")
        else:
            print("   ❌ Logowanie z błędnym hasłem zostało zaakceptowane (błąd bezpieczeństwa!)")
            return False
        
        # Test 5: Test non-existent user
        print(f"\n👻 Test 5: Próba logowania nieistniejącego użytkownika")
        nonexistent_login_result = login_user("nieistniejacy_uzytkownik", "haslo")
        
        if nonexistent_login_result is None:
            print("   ✅ Logowanie nieistniejącego użytkownika prawidłowo odrzucone")
        else:
            print("   ❌ Logowanie nieistniejącego użytkownika zostało zaakceptowane (błąd!)")
            return False
        
        # Cleanup: Remove test user
        print(f"\n🧹 Czyszczenie: Usuwanie użytkownika testowego")
        users_data = load_user_data()
        if test_username in users_data:
            del users_data[test_username]
            save_user_data(users_data)
            print(f"   ✅ Użytkownik {test_username} usunięty")
        
        print("\n" + "=" * 60)
        print("✅ Wszystkie testy przeszły pomyślnie!")
        print("🎉 System rejestracji i logowania działa poprawnie!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test nie powiódł się: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Restore original file if something went wrong
        if os.path.exists(backup_users_file):
            if not os.path.exists(original_users_file):
                shutil.move(backup_users_file, original_users_file)
                print("📁 Przywrócono oryginalny plik users_data.json")
            else:
                os.remove(backup_users_file)
                print("📁 Usunięto plik kopii zapasowej")

if __name__ == "__main__":
    success = test_registration_and_login()
    sys.exit(0 if success else 1)
