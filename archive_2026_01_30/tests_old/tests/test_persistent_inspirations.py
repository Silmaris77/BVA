#!/usr/bin/env python3
"""
Test persistent inspirations system for logged users
"""

import os
import sys
import json
import tempfile
import shutil
from unittest.mock import patch

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

def test_persistent_inspirations():
    """Test inspirations persistence for logged users"""
    
    print("🧪 Test systemu trwałego zapamiętywania inspiracji")
    print("=" * 60)
    
    # Create a temporary copy of users_data.json for testing
    original_users_file = os.path.join(project_root, 'users_data.json')
    temp_users_file = os.path.join(project_root, 'users_data_test_backup.json')
    
    try:
        # Backup original file
        shutil.copy2(original_users_file, temp_users_file)
        print("📁 Utworzono kopię zapasową users_data.json")
        
        # Import required modules after setting up the path
        from data.users import (
            load_user_data, save_user_data, register_user,
            mark_inspiration_as_read_for_user, toggle_inspiration_favorite_for_user,
            is_inspiration_read_by_user, is_inspiration_favorite_by_user,
            get_user_read_inspirations, get_user_favorite_inspirations
        )
        
        # Test 1: Create a test user
        print("\n📝 Test 1: Rejestracja użytkownika testowego")
        result = register_user("test_user_inspirations", "test123", "test123")
        print(f"   Wynik: {result}")
        assert result == "Registration successful!", f"Rejestracja nie powiodła się: {result}"
        print("   ✅ Użytkownik zarejestrowany pomyślnie")
        
        # Test 2: Mark inspiration as read
        print("\n📖 Test 2: Oznaczanie inspiracji jako przeczytane")
        test_inspiration_id = "test_inspiration_123"
        success = mark_inspiration_as_read_for_user(test_inspiration_id, "test_user_inspirations")
        print(f"   Wynik zapisu: {success}")
        assert success == True, "Nie udało się oznaczyć inspiracji jako przeczytanej"
        
        # Check if it's marked as read
        is_read = is_inspiration_read_by_user(test_inspiration_id, "test_user_inspirations")
        print(f"   Czy jest oznaczona jako przeczytana: {is_read}")
        assert is_read == True, "Inspiracja nie została oznaczona jako przeczytana"
        print("   ✅ Inspiracja poprawnie oznaczona jako przeczytana")
        
        # Test 3: Toggle inspiration as favorite
        print("\n❤️ Test 3: Dodawanie inspiracji do ulubionych")
        success = toggle_inspiration_favorite_for_user(test_inspiration_id, "test_user_inspirations")
        print(f"   Wynik toggleowania (dodanie): {success}")
        assert success == True, "Nie udało się dodać inspiracji do ulubionych"
        
        # Check if it's favorite
        is_fav = is_inspiration_favorite_by_user(test_inspiration_id, "test_user_inspirations")
        print(f"   Czy jest ulubiona: {is_fav}")
        assert is_fav == True, "Inspiracja nie została dodana do ulubionych"
        print("   ✅ Inspiracja poprawnie dodana do ulubionych")
        
        # Test 4: Toggle inspiration favorite again (remove)
        print("\n💔 Test 4: Usuwanie inspiracji z ulubionych")
        success = toggle_inspiration_favorite_for_user(test_inspiration_id, "test_user_inspirations")
        print(f"   Wynik toggleowania (usunięcie): {success}")
        assert success == True, "Nie udało się usunąć inspiracji z ulubionych"
        
        # Check if it's no longer favorite
        is_fav = is_inspiration_favorite_by_user(test_inspiration_id, "test_user_inspirations")
        print(f"   Czy nadal jest ulubiona: {is_fav}")
        assert is_fav == False, "Inspiracja nadal jest w ulubionych"
        print("   ✅ Inspiracja poprawnie usunięta z ulubionych")
        
        # Test 5: Check persistence (reload data and verify)
        print("\n💾 Test 5: Sprawdzanie trwałości danych")
        
        # Add multiple inspirations
        test_inspirations = ["insp_1", "insp_2", "insp_3"]
        for insp_id in test_inspirations:
            mark_inspiration_as_read_for_user(insp_id, "test_user_inspirations")
            if insp_id in ["insp_1", "insp_3"]:  # Make 1 and 3 favorite
                toggle_inspiration_favorite_for_user(insp_id, "test_user_inspirations")
        
        # Get lists
        read_list = get_user_read_inspirations("test_user_inspirations")
        fav_list = get_user_favorite_inspirations("test_user_inspirations")
        
        print(f"   Przeczytane inspiracje: {read_list}")
        print(f"   Ulubione inspiracje: {fav_list}")
        
        expected_read = ["test_inspiration_123"] + test_inspirations
        expected_fav = ["insp_1", "insp_3"]
        
        assert set(read_list) == set(expected_read), f"Nieoczekiwana lista przeczytanych: {read_list}"
        assert set(fav_list) == set(expected_fav), f"Nieoczekiwana lista ulubionych: {fav_list}"
        print("   ✅ Dane zostały poprawnie zapisane i odczytane")
        
        # Test 6: Verify data persists in JSON file
        print("\n📄 Test 6: Weryfikacja zapisu w pliku JSON")
        users_data = load_user_data()
        user_data = users_data.get("test_user_inspirations", {})
        inspirations_data = user_data.get("inspirations", {})
        
        file_read = inspirations_data.get("read", [])
        file_fav = inspirations_data.get("favorites", [])
        
        print(f"   Przeczytane w pliku: {file_read}")
        print(f"   Ulubione w pliku: {file_fav}")
        
        assert set(file_read) == set(expected_read), f"Dane w pliku nie są zgodne z oczekiwanymi"
        assert set(file_fav) == set(expected_fav), f"Dane ulubionych w pliku nie są zgodne"
        print("   ✅ Dane zostały poprawnie zapisane w pliku JSON")
        
        # Cleanup: Remove test user
        print("\n🧹 Czyszczenie: Usuwanie użytkownika testowego")
        users_data = load_user_data()
        if "test_user_inspirations" in users_data:
            del users_data["test_user_inspirations"]
            save_user_data(users_data)
            print("   ✅ Użytkownik testowy usunięty")
        
        print("\n" + "=" * 60)
        print("✅ Wszystkie testy przeszły pomyślnie!")
        print("🎉 System trwałego zapamiętywania inspiracji działa poprawnie!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test nie powiódł się: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Restore original file if something went wrong
        if os.path.exists(temp_users_file):
            if not os.path.exists(original_users_file):
                shutil.move(temp_users_file, original_users_file)
                print("📁 Przywrócono oryginalny plik users_data.json")
            else:
                os.remove(temp_users_file)
                print("📁 Usunięto plik kopii zapasowej")

if __name__ == "__main__":
    success = test_persistent_inspirations()
    sys.exit(0 if success else 1)
