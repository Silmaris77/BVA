"""
Test weryfikujący aktualny tryb oceny Business Games
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.business_game_evaluation import get_active_evaluation_mode
from config.business_games_settings import DEFAULT_EVALUATION_MODE, SETTINGS_FILE

print("="*60)
print("   TEST TRYBU OCENY BUSINESS GAMES")
print("="*60)
print()

# 1. Sprawdź DEFAULT w kodzie
print("1️⃣ Domyślny tryb (hardcoded w config):")
print(f"   DEFAULT_EVALUATION_MODE = '{DEFAULT_EVALUATION_MODE}'")
print()

# 2. Sprawdź plik konfiguracyjny
print("2️⃣ Plik konfiguracyjny:")
print(f"   Lokalizacja: {SETTINGS_FILE}")

if os.path.exists(SETTINGS_FILE):
    import json
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    print(f"   ✅ Plik istnieje")
    print(f"   📄 Zawartość:")
    for key, value in config.items():
        print(f"      {key}: {value}")
else:
    print(f"   ❌ Plik NIE istnieje")
print()

# 3. Sprawdź co zwraca funkcja
print("3️⃣ Aktywny tryb (funkcja get_active_evaluation_mode()):")
active_mode = get_active_evaluation_mode()
print(f"   Zwraca: '{active_mode}'")
print()

# 4. Podsumowanie
print("="*60)
print("📊 PODSUMOWANIE:")
print("="*60)

if active_mode == "ai":
    print("✅ Tryb ustawiony na: AI (Gemini)")
    print("🎉 System będzie używać Google Gemini do oceny kontraktów")
elif active_mode == "heuristic":
    print("⚠️ Tryb ustawiony na: Heurystyka")
    print("🔧 Aby zmienić na AI:")
    print("   1. Uruchom: python set_ai_mode.py")
    print("   2. Zrestartuj aplikację Streamlit")
elif active_mode == "game_master":
    print("👨‍💼 Tryb ustawiony na: Mistrz Gry (ręczna ocena)")
else:
    print(f"❓ Nieznany tryb: {active_mode}")

print()
print("="*60)
print("💡 WAŻNE:")
print("="*60)
print("Po zmianie pliku konfiguracyjnego MUSISZ zrestartować")
print("aplikację Streamlit, aby zmiany zostały załadowane!")
print()
print("Restart:")
print("  1. Ctrl+C w terminalu ze Streamlit")
print("  2. streamlit run main.py")
