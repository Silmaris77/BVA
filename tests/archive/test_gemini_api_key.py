"""
Test sprawdzający dostęp do Google Gemini API Key
"""

import os

print("🔍 Sprawdzanie klucza API Google Gemini...\n")

# 1. Sprawdź Streamlit secrets
print("1️⃣ Streamlit secrets:")
try:
    import streamlit as st
    key = st.secrets.get("GOOGLE_API_KEY")
    if key:
        print(f"   ✅ Znaleziono w st.secrets: {key[:10]}...{key[-5:]}")
    else:
        print("   ❌ Brak w st.secrets")
except Exception as e:
    print(f"   ❌ Błąd: {e}")

# 2. Sprawdź zmienną środowiskową
print("\n2️⃣ Zmienna środowiskowa:")
key = os.getenv("GOOGLE_API_KEY")
if key:
    print(f"   ✅ Znaleziono: {key[:10]}...{key[-5:]}")
else:
    print("   ❌ Brak zmiennej GOOGLE_API_KEY")

# 3. Sprawdź plik config
print("\n3️⃣ Plik konfiguracyjny:")
config_file = "config/gemini_api_key.txt"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        key = f.read().strip()
        if key:
            print(f"   ✅ Znaleziono w pliku: {key[:10]}...{key[-5:]}")
        else:
            print("   ⚠️ Plik istnieje ale jest pusty")
else:
    print(f"   ❌ Brak pliku {config_file}")

print("\n" + "="*60)
print("📝 PODSUMOWANIE:")
print("="*60)

# Sprawdź w kolejności priorytetu
api_key = None
source = None

try:
    import streamlit as st
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if api_key:
        source = "Streamlit secrets (PRIORYTET 1)"
except:
    pass

if not api_key:
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        source = "Zmienna środowiskowa (PRIORYTET 2)"

if not api_key and os.path.exists(config_file):
    with open(config_file, 'r') as f:
        api_key = f.read().strip()
        if api_key:
            source = "Plik konfiguracyjny (PRIORYTET 3)"

if api_key:
    print(f"✅ Klucz API znaleziony!")
    print(f"📍 Źródło: {source}")
    print(f"🔑 Klucz: {api_key[:15]}...{api_key[-10:]}")
    print("\n🎉 System oceny AI (Gemini) jest gotowy do użycia!")
else:
    print("❌ Brak klucza API!")
    print("\n📖 Jak dodać klucz:")
    print("   1. Uzyskaj klucz: https://aistudio.google.com/app/apikey")
    print("   2. Dodaj do .streamlit/secrets.toml:")
    print('      GOOGLE_API_KEY = "twoj_klucz_tutaj"')
    print("   3. Uruchom ponownie aplikację")
