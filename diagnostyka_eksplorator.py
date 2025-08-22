#!/usr/bin/env python3
"""
DIAGNOSTYKA PROBLEMU Z ZAKŁADKĄ EKSPLORATOR
"""

print("🔍 DIAGNOSTYKA ZAKŁADKI EKSPLORATOR")
print("=" * 50)

# Test 1: Sprawdź menu nawigacji
print("\n1️⃣ SPRAWDZENIE MENU NAWIGACJI")
print("-" * 30)

try:
    import sys
    import os
    
    # Dodaj ścieżkę
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    if APP_DIR not in sys.path:
        sys.path.append(APP_DIR)
    
    from utils.components import navigation_menu
    import inspect
    
    source = inspect.getsource(navigation_menu)
    lines = source.split('\n')
    
    # Znajdź menu_options
    menu_items = []
    in_menu = False
    
    for line in lines:
        if 'menu_options = [' in line:
            in_menu = True
            continue
        if in_menu:
            if ']' in line and '{' not in line:
                break
            if '"id":' in line and '"' in line:
                parts = line.split('"id": "')
                if len(parts) > 1:
                    item_id = parts[1].split('"')[0]
                    menu_items.append(item_id)
    
    print(f"📋 Znalezione zakładki: {menu_items}")
    
    if 'degen_explorer' in menu_items:
        print("❌ BŁĄD: 'degen_explorer' NADAL W MENU!")
        print("   Sprawdź plik utils/components.py linia ~252")
    else:
        print("✅ 'degen_explorer' został usunięty z menu")
        
    expected = ["dashboard", "lesson", "skills", "shop", "profile"]
    if menu_items == expected:
        print("✅ Menu jest poprawne - 5 zakładek")
    else:
        print(f"⚠️  Menu: oczekiwane {expected}, aktualne {menu_items}")

except Exception as e:
    print(f"❌ Błąd: {e}")

# Test 2: Sprawdź session valid_pages
print("\n2️⃣ SPRAWDZENIE VALID_PAGES")
print("-" * 30)

try:
    from utils.session import init_session_state
    import inspect
    
    source = inspect.getsource(init_session_state)
    
    if 'degen_explorer' in source:
        print("❌ BŁĄD: 'degen_explorer' NADAL W valid_pages!")
        print("   Sprawdź plik utils/session.py")
    else:
        print("✅ 'degen_explorer' został usunięty z valid_pages")
        
    # Znajdź valid_pages
    lines = source.split('\n')
    for line in lines:
        if 'valid_pages' in line and '[' in line:
            print(f"📋 Valid pages: {line.strip()}")
            break

except Exception as e:
    print(f"❌ Błąd: {e}")

# Test 3: Instrukcje dla użytkownika
print("\n3️⃣ INSTRUKCJE ROZWIĄZANIA")
print("-" * 30)

print("""
Jeśli nadal widzisz zakładkę Eksplorator, spróbuj:

🔄 RESTART APLIKACJI:
   1. Zatrzymaj aplikację (Ctrl+C)
   2. Uruchom ponownie: streamlit run main.py
   
🧹 WYCZYŚĆ CACHE:
   1. W przeglądarce naciśnij Ctrl+F5 (hard refresh)
   2. Lub wyczyść cache przeglądarki
   3. Zamknij wszystkie karty z aplikacją
   
📁 SPRAWDŹ PLIK:
   1. Upewnij się że uruchamiasz: python main.py
   2. NIE uruchamiaj: main_new.py lub main_new_fixed.py
   
🔍 SPRAWDŹ KOD:
   1. Otwórz utils/components.py linia 252
   2. Sprawdź czy menu_options ma 5 elementów
   3. Sprawdź czy nie ma "degen_explorer"
""")

print("\n" + "=" * 50)
print("Uruchom tę diagnostykę ponownie po każdej zmianie")
