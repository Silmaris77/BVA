# 🔐 Konfiguracja Sekretów (API Keys)

## ⚠️ WAŻNE: NIE COMMITUJ KLUCZY API NA GITHUB!

### Lokalna konfiguracja (development):

1. **Utwórz plik `.streamlit/secrets.toml`** w głównym katalogu projektu:
   ```toml
   GOOGLE_API_KEY = "twoj_klucz_api_tutaj"
   ```

2. **Ten plik jest automatycznie ignorowany** przez `.gitignore`

3. **Uzyskaj klucz API Google Gemini:**
   - Wejdź na: https://makersuite.google.com/app/apikey
   - Zaloguj się z kontem Google
   - Kliknij "Create API Key"
   - Skopiuj klucz (zaczyna się od `AIza...`)

### Konfiguracja na Streamlit Cloud (production):

1. **Przejdź do ustawień swojej aplikacji** na Streamlit Cloud
2. **Kliknij "Secrets"** w menu
3. **Dodaj sekret:**
   ```toml
   GOOGLE_API_KEY = "twoj_klucz_api"
   ```
4. **Zapisz** - aplikacja automatycznie się zrestartuje

### Weryfikacja:

Sprawdź czy aplikacja poprawnie czyta klucz:
```python
import streamlit as st
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    print("✅ Klucz API załadowany")
else:
    print("❌ Brak klucza API")
```

### Dodatkowe zmienne środowiskowe:

Możesz też używać zmiennych środowiskowych:
```bash
# Windows PowerShell:
$env:GOOGLE_API_KEY="twoj_klucz"

# Linux/Mac:
export GOOGLE_API_KEY="twoj_klucz"
```

## 🔒 Bezpieczeństwo:

✅ **TAK:**
- Używaj `st.secrets["KEY"]`
- Używaj zmiennych środowiskowych
- Używaj `.streamlit/secrets.toml` (lokalnie)
- Dodaj `.streamlit/` do `.gitignore`

❌ **NIE:**
- Nie hardcoduj kluczy w kodzie
- Nie commituj `secrets.toml` na GitHub
- Nie udostępniaj kluczy publicznie
- Nie zapisuj kluczy w plikach konfiguracyjnych w repo
