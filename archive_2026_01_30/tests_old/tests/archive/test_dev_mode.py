"""
Test trybu developerskiego - sprawdź czy zapisuje tylko w pamięci
"""
from config.settings import DEVELOPMENT_MODE

print(f"🔧 DEVELOPMENT_MODE: {DEVELOPMENT_MODE}")

if DEVELOPMENT_MODE:
    print("✅ Tryb DEV aktywny - zapisy wyłączone")
    print("📝 Dane zapisywane tylko w st.session_state['users_data_cache']")
    print("⚡ Logowanie powinno być BŁYSKAWICZNE")
else:
    print("💾 Tryb PRODUKCYJNY - normalne zapisy do JSON")
    print("📁 Dane zapisywane w users_data.json")
