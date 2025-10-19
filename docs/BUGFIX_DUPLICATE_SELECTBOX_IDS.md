# 🐛 Bugfix - Duplicate Selectbox IDs

## Problem

Po dodaniu zakładki "📜 Historia" w Business Games, wystąpił błąd:

```
streamlit.errors.StreamlitDuplicateElementId: There are multiple `selectbox` 
elements with the same auto-generated ID.
```

### Przyczyna

Streamlit generuje automatyczne ID dla widgetów na podstawie:
- Typu elementu (np. `selectbox`)
- Parametrów (label, options)
- Pozycji w kodzie

Gdy dwie zakładki mają selectboxy z **identycznymi parametrami**, Streamlit nie może ich rozróżnić.

### Konflikt w kodzie

**Zakładka "💼 Rynek Kontraktów":**
```python
category_filter = st.selectbox(
    "Kategoria:",
    ["Wszystkie", "Konflikt", "Coaching", "Kultura", "Kryzys", "Leadership"]
)
```

**Zakładka "📜 Historia":**
```python
filter_category = st.selectbox(
    "Kategoria:",  # ← Ten sam label!
    ["Wszystkie"] + ["Konflikt", "Coaching", "Kultura", "Kryzys", "Leadership"]  # ← Prawie te same opcje!
)
```

Streamlit traktował je jako **duplikaty** i rzucał błędem.

## ✅ Rozwiązanie

Dodano **unikalne klucze `key`** do wszystkich widgetów w `views/business_games.py`.

### Zmienione elementy

#### 1. Zakładka "💼 Rynek Kontraktów" (linia ~360)
```python
# PRZED:
category_filter = st.selectbox(
    "Kategoria:",
    ["Wszystkie", "Konflikt", "Coaching", "Kultura", "Kryzys", "Leadership"]
)

# PO:
category_filter = st.selectbox(
    "Kategoria:",
    ["Wszystkie", "Konflikt", "Coaching", "Kultura", "Kryzys", "Leadership"],
    key="contracts_filter_category"  # ← DODANO KLUCZ
)
```

Podobnie dla:
- `difficulty_filter` → `key="contracts_filter_difficulty"`
- `sort_by` → `key="contracts_sort_by"`

#### 2. Zakładka "📜 Historia" (linia ~610)
```python
# PRZED:
filter_category = st.selectbox(
    "Kategoria:",
    ["Wszystkie"] + ["Konflikt", "Coaching", "Kultura", "Kryzys", "Leadership"]
)

# PO:
filter_category = st.selectbox(
    "Kategoria:",
    ["Wszystkie"] + ["Konflikt", "Coaching", "Kultura", "Kryzys", "Leadership"],
    key="history_filter_category"  # ← DODANO KLUCZ
)
```

Podobnie dla:
- `filter_rating` → `key="history_filter_rating"`
- `show_count` → `key="history_show_count"`

#### 3. Zakładka "🏆 Rankingi" (linia ~754)
```python
# PRZED:
ranking_type = st.selectbox(
    "Wybierz ranking:",
    ["🏆 Ogólny (Overall Score)", "💰 Przychody", ...]
)

# PO:
ranking_type = st.selectbox(
    "Wybierz ranking:",
    ["🏆 Ogólny (Overall Score)", "💰 Przychody", ...],
    key="rankings_type_selector"  # ← DODANO KLUCZ
)
```

#### 4. Zakładka "🏢 Dashboard" - Ustawienia (linia ~215)
```python
# PRZED:
new_name = st.text_input("Nowa nazwa firmy", value=bg_data["firm"]["name"])
if st.button("💾 Zapisz nazwę"):

# PO:
new_name = st.text_input("Nowa nazwa firmy", value=bg_data["firm"]["name"], 
                        key="dashboard_firm_name_input")  # ← DODANO KLUCZ
if st.button("💾 Zapisz nazwę", key="dashboard_save_firm_name"):  # ← DODANO KLUCZ
```

## 📋 Pełna lista dodanych kluczy

| Widget | Lokalizacja | Klucz |
|--------|-------------|-------|
| selectbox | Rynek Kontraktów - Kategoria | `contracts_filter_category` |
| selectbox | Rynek Kontraktów - Trudność | `contracts_filter_difficulty` |
| selectbox | Rynek Kontraktów - Sortuj | `contracts_sort_by` |
| selectbox | Historia - Kategoria | `history_filter_category` |
| selectbox | Historia - Ocena | `history_filter_rating` |
| selectbox | Historia - Pokaż | `history_show_count` |
| selectbox | Rankingi - Typ rankingu | `rankings_type_selector` |
| text_input | Dashboard - Nazwa firmy | `dashboard_firm_name_input` |
| button | Dashboard - Zapisz nazwę | `dashboard_save_firm_name` |

## 🎯 Best Practices

### Kiedy dodawać `key`?

1. **ZAWSZE** gdy masz podobne widgety w różnych miejscach
2. **ZAWSZE** w aplikacjach z zakładkami/tabs
3. **ZAWSZE** gdy widget jest w pętli lub warunkowym if/else
4. **Zalecane** w expanderach i sidebarach

### Konwencja nazewnictwa kluczy

```python
key="{context}_{widget_type}_{purpose}"

# Przykłady:
key="contracts_filter_category"  # zakładka_typ_cel
key="history_show_count"         # zakładka_cel
key="dashboard_firm_name_input"  # lokalizacja_dane_typ
```

### Dlaczego to ważne?

- ✅ Unikanie konfliktów ID
- ✅ Lepsze debugowanie (widać który widget powoduje problem)
- ✅ Kontrola nad session state
- ✅ Możliwość manualnego dostępu: `st.session_state.contracts_filter_category`

## 🧪 Testowanie

Po dodaniu kluczy, aplikacja działa poprawnie:

1. ✅ Zakładka "💼 Rynek Kontraktów" - filtry działają
2. ✅ Zakładka "📜 Historia" - filtry działają
3. ✅ Zakładka "🏆 Rankingi" - selektor działa
4. ✅ Brak błędów `StreamlitDuplicateElementId`

## 📝 Nauka na przyszłość

**Problem wystąpił przy dodawaniu nowej funkcjonalności** (zakładka Historia).

**Rozwiązanie:** Zawsze dodawać `key` do widgetów w aplikacjach z wieloma zakładkami, nawet jeśli na pierwszy rzut oka wydają się unikalne.

**Prewencja:** 
- Podczas code review sprawdzać czy wszystkie widgety mają klucze
- W testach przełączać się między zakładkami aby wykryć konflikty
- Używać linterów które wykrywają brakujące klucze

---

**Data naprawy:** 2025-10-19  
**Status:** ✅ Naprawione i przetestowane  
**Plik:** `views/business_games.py`  
**Autor:** GitHub Copilot
