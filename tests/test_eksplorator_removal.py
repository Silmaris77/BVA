#!/usr/bin/env python3
"""
Test sprawdzający czy zakładka Eksplorator została usunięta z nawigacji
"""

import sys
import os

# Dodaj ścieżkę do aplikacji
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

def test_navigation_menu():
    """Test menu nawigacji - sprawdza czy eksplorator został usunięty"""
    try:
        # Import funkcji nawigacji
        from utils.components import navigation_menu
        
        # Sprawdź definicję menu w kodzie źródłowym
        import inspect
        source_code = inspect.getsource(navigation_menu)
        
        print("=== ANALIZA MENU NAWIGACJI ===")
        print(f"Funkcja navigation_menu znaleziona: ✅")
        
        # Sprawdź czy w kodzie jest degen_explorer
        if "degen_explorer" in source_code:
            print(f"❌ BŁĄD: 'degen_explorer' nadal znajduje się w kodzie!")
            print("Fragmenty kodu zawierające 'degen_explorer':")
            lines = source_code.split('\n')
            for i, line in enumerate(lines):
                if 'degen_explorer' in line:
                    print(f"  Linia {i+1}: {line.strip()}")
            return False
        else:
            print(f"✅ 'degen_explorer' został usunięty z kodu nawigacji")
        
        # Sprawdź czy w kodzie jest "Eksplorator"
        if "Eksplorator" in source_code:
            print(f"❌ BŁĄD: 'Eksplorator' nadal znajduje się w kodzie!")
            print("Fragmenty kodu zawierające 'Eksplorator':")
            lines = source_code.split('\n')
            for i, line in enumerate(lines):
                if 'Eksplorator' in line:
                    print(f"  Linia {i+1}: {line.strip()}")
            return False
        else:
            print(f"✅ 'Eksplorator' został usunięty z kodu nawigacji")
        
        # Sprawdź opcje menu
        print("\n=== ANALIZA OPCJI MENU ===")
        if "menu_options" in source_code:
            print("Znalezione opcje menu:")
            lines = source_code.split('\n')
            in_menu_options = False
            for line in lines:
                if 'menu_options = [' in line:
                    in_menu_options = True
                    continue
                if in_menu_options:
                    if ']' in line and '{' not in line:
                        break
                    if '{"id"' in line or '"name"' in line:
                        print(f"  {line.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ BŁĄD podczas testowania: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_session_valid_pages():
    """Test sprawdzający valid_pages w session.py"""
    try:
        print("\n=== ANALIZA VALID_PAGES ===")
        from utils.session import init_session_state
        
        import inspect
        source_code = inspect.getsource(init_session_state)
        
        if "degen_explorer" in source_code:
            print(f"❌ BŁĄD: 'degen_explorer' nadal w valid_pages!")
            return False
        else:
            print(f"✅ 'degen_explorer' został usunięty z valid_pages")
        
        # Znajdź valid_pages
        if "valid_pages" in source_code:
            lines = source_code.split('\n')
            for line in lines:
                if 'valid_pages' in line and '[' in line:
                    print(f"Valid pages: {line.strip()}")
                    break
        
        return True
        
    except Exception as e:
        print(f"❌ BŁĄD podczas testowania session: {e}")
        return False

if __name__ == "__main__":
    print("🔍 TESTOWANIE USUNIĘCIA ZAKŁADKI EKSPLORATOR")
    print("=" * 50)
    
    test1 = test_navigation_menu()
    test2 = test_session_valid_pages()
    
    print("\n" + "=" * 50)
    if test1 and test2:
        print("🎉 SUKCES: Zakładka Eksplorator została poprawnie usunięta!")
        print("📋 Aplikacja powinna teraz wyświetlać tylko 5 zakładek:")
        print("   1. 🏠 Dashboard")
        print("   2. 📚 Lekcje") 
        print("   3. 🌳 Umiejętności")
        print("   4. 🛒 Sklep")
        print("   5. 👤 Profil")
    else:
        print("❌ BŁĄD: Nadal znajdują się referencje do Eksploratora!")
        print("Sprawdź pliki i popraw błędy wskazane powyżej.")
