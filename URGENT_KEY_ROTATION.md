# 🚨 PILNE: Rotacja Klucza API

## Google wykrył Twój klucz API w repozytorium GitHub!

### Co musisz NATYCHMIAST zrobić:

### 1️⃣ **WYGENERUJ NOWY KLUCZ API:**
1. Wejdź na: https://makersuite.google.com/app/apikey
2. **USUŃ stary klucz** (ten skompromitowany)
3. **Wygeneruj nowy klucz**
4. Skopiuj nowy klucz

### 2️⃣ **Zaktualizuj lokalnie:**
1. Otwórz `.streamlit/secrets.toml`
2. Zamień stary klucz na nowy
3. Zapisz plik

### 3️⃣ **Zaktualizuj na Streamlit Cloud:**
1. Wejdź na: https://share.streamlit.io
2. Wybierz swoją aplikację
3. Settings → Secrets
4. Zamień `GOOGLE_API_KEY` na nowy klucz
5. Zapisz

### 4️⃣ **Wyczyść historię Git (OPCJONALNE ale zalecane):**

⚠️ **UWAGA:** To usunie cały stary klucz z historii Git!

```powershell
# Usuń plik z historii
git filter-branch --force --index-filter `
  "git rm --cached --ignore-unmatch config/gemini_api_key.txt" `
  --prune-empty --tag-name-filter cat -- --all

# Usuń hardcoded klucz z historii (jeśli był w kodzie)
git filter-branch --force --tree-filter `
  "find . -type f -name '*.py' -exec sed -i 's/AIzaSyDJu4fJoICZCe9O8shCN18SSq9t_gFH8nM/YOUR_NEW_KEY_HERE/g' {} \;" `
  --prune-empty --tag-name-filter cat -- --all

# Force push (⚠️ UWAGA: to nadpisze historię!)
git push origin --force --all
git push origin --force --tags
```

### ✅ **Sprawdź czy działa:**

```python
# Uruchom lokalnie:
streamlit run main.py

# Sprawdź czy klucz się ładuje
import streamlit as st
print(st.secrets.get("GOOGLE_API_KEY"))
```

### 📚 **Więcej info:**
- [Streamlit Secrets](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [GitHub - Remove sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## ⏰ Zrób to TERAZ!

Klucz API jest publiczny = każdy może go używać na Twój koszt!
