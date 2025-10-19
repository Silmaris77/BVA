# 🐛 Bugfix - admin_tabs not defined

## Problem

```
NameError: name 'admin_tabs' is not defined
File "views\admin.py", line 922, in manage_lesson_access
    with admin_tabs[6]:
         ^^^^^^^^^^
```

### Przyczyna

Zakładka Business Games (`admin_tabs[6]`) była **błędnie umieszczona wewnątrz funkcji** `manage_lesson_access()` zamiast w głównej funkcji `show_admin_dashboard()`.

### Struktura przed naprawą (BŁĘDNA):

```python
def show_admin_dashboard():
    admin_tabs = st.tabs([...])  # Definicja admin_tabs
    
    with admin_tabs[0]:
        # Zakładka Przegląd
    
    with admin_tabs[1]:
        # Zakładka Użytkownicy
    
    # ... itd ...
    
    with admin_tabs[5]:
        # Zakładka Zarządzanie
        # ... koniec funkcji show_admin_dashboard()

def manage_lesson_access():  # ← Nowa funkcja (poza show_admin_dashboard)
    # ...
    
    with admin_tabs[6]:  # ← BŁĄD! admin_tabs nie istnieje tutaj!
        show_business_games_admin_panel()

def show_business_games_admin_panel():
    # ...
```

### Problem:
- `admin_tabs` jest zmienną lokalną funkcji `show_admin_dashboard()`
- Funkcja `manage_lesson_access()` jest **poza** `show_admin_dashboard()`
- Próba użycia `admin_tabs[6]` w `manage_lesson_access()` powoduje `NameError`

## ✅ Rozwiązanie

Przeniesiono zakładkę Business Games (`admin_tabs[6]`) do właściwego miejsca - **wewnątrz funkcji** `show_admin_dashboard()`.

### Struktura po naprawie (POPRAWNA):

```python
def show_admin_dashboard():
    admin_tabs = st.tabs([...])  # Definicja admin_tabs
    
    with admin_tabs[0]:
        # Zakładka Przegląd
    
    with admin_tabs[1]:
        # Zakładka Użytkownicy
    
    # ... itd ...
    
    with admin_tabs[5]:
        # Zakładka Zarządzanie
    
    # 7. Zakładka Business Games ← DODANO TUTAJ!
    with admin_tabs[6]:
        show_business_games_admin_panel()  # ✅ Teraz admin_tabs jest dostępne!
    
    # Koniec funkcji show_admin_dashboard()

def manage_lesson_access():  # ← Osobna funkcja pomocnicza
    # Zarządzanie dostępnością lekcji
    # Nie używa już admin_tabs
    pass

def show_business_games_admin_panel():  # ← Osobna funkcja pomocnicza
    # Panel Business Games
    pass
```

## 📝 Zmiany w kodzie

### Plik: `views/admin.py`

**Linia ~806 (przed końcem `show_admin_dashboard()`):**

```python
# DODANO:
    # 7. Zakładka Business Games
    with admin_tabs[6]:
        show_business_games_admin_panel()
```

**Linia ~921 (wewnątrz `manage_lesson_access()`):**

```python
# USUNIĘTO:
    # 7. Zakładka Business Games
    with admin_tabs[6]:
        show_business_games_admin_panel()
```

## 🎯 Kluczowe zasady

### 1. Zakres zmiennych (Variable Scope)
- Zmienne lokalne funkcji są dostępne tylko **wewnątrz tej funkcji**
- `admin_tabs` zdefiniowane w `show_admin_dashboard()` → dostępne tylko tam
- Inne funkcje (np. `manage_lesson_access()`) **nie mają dostępu** do `admin_tabs`

### 2. Struktura tabs w Streamlit
```python
def main_function():
    tabs = st.tabs(["Tab1", "Tab2", "Tab3"])  # Definicja
    
    with tabs[0]:
        # Zawartość Tab1 - MUSI być w tej samej funkcji!
    
    with tabs[1]:
        # Zawartość Tab2 - MUSI być w tej samej funkcji!
        helper_function()  # ✅ Możesz wywoływać inne funkcje
    
    with tabs[2]:
        # Zawartość Tab3
        pass

def helper_function():  # ← Osobna funkcja pomocnicza
    # Logika biznesowa, nie używa tabs
    st.write("Coś")
```

### 3. Funkcje pomocnicze
- `manage_lesson_access()` - pomocnicza funkcja wywoływana z `admin_tabs[3]`
- `show_business_games_admin_panel()` - pomocnicza funkcja wywoływana z `admin_tabs[6]`
- Te funkcje **nie mają** i **nie potrzebują** dostępu do `admin_tabs`
- Są wywoływane **z poziomu** właściwych zakładek

## 🧪 Weryfikacja

Po naprawie:
- ✅ `show_admin_dashboard()` tworzy wszystkie 7 zakładek
- ✅ Każda zakładka ma dostęp do `admin_tabs`
- ✅ Funkcje pomocnicze nie używają `admin_tabs` bezpośrednio
- ✅ Brak błędu `NameError`

## 📚 Lekcja na przyszłość

**Problem:** Przy dodawaniu nowej zakładki (Business Games) kod został błędnie umieszczony w funkcji pomocniczej zamiast w głównej funkcji z tabs.

**Rozwiązanie:** Zawsze sprawdzaj:
1. Gdzie jest `st.tabs()` - to jest główna funkcja
2. Wszystkie `with tabs[x]:` muszą być **w tej samej funkcji**
3. Funkcje pomocnicze są wywoływane **wewnątrz** bloków `with tabs[x]:`

---

**Data naprawy:** 2025-10-19  
**Status:** ✅ Naprawione i przetestowane  
**Plik:** `views/admin.py`  
**Typ błędu:** Błąd zakresu zmiennych (Variable Scope Error)  
**Autor:** GitHub Copilot
