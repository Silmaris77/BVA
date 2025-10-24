# ⚙️ Ustawienia Firmy - Nowy Design

## 📋 Przegląd

Wszystkie ustawienia firmy zostały zorganizowane w **3 zakładki** (tabs) w jednym miejscu dla lepszej użyteczności.

---

## 🎨 Struktura UI

### Dashboard → Przewiń w dół → "⚙️ Ustawienia Firmy"

```
┌─────────────────────────────────────────────────────────┐
│  ⚙️ USTAWIENIA FIRMY                                     │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  [✏️ Nazwa i logo] [🔄 Zarządzanie firmą] [📦 Archiwum]  │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📑 Zakładka 1: "✏️ Nazwa i logo"

**Layout:** 2 kolumny (nazwa | logo)

### Lewa kolumna - Nazwa firmy:
```
┌──────────────────────────────┐
│ ✏️ Zmień nazwę firmy          │
├──────────────────────────────┤
│ [Input: "Max's Consulting"]  │
│                               │
│ [💾 Zapisz nazwę]            │
└──────────────────────────────┘
```

### Prawa kolumna - Logo:
```
┌──────────────────────────────┐
│ 🎨 Zmień logo firmy           │
├──────────────────────────────┤
│ Kategoria: [🏢 Budynki ▼]    │
│                               │
│ [🏢] [🏛️] [🏢] [🏭] [🏗️] [🏦]  │
│ [🏪] [🏬] [🏨] [🏫] [🏩] [🏯]  │
│                               │
└──────────────────────────────┘
```

### Podgląd (pełna szerokość):
```
┌────────────────────────────────────────────┐
│         👀 Podgląd                          │
│ ┌────────────────────────────────────────┐ │
│ │                                        │ │
│ │            🏢                          │ │
│ │      Max's Consulting                  │ │
│ │                                        │ │
│ └────────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

---

## 🔄 Zakładka 2: "🔄 Zarządzanie firmą"

**Funkcja:** Rozpoczęcie nowej firmy

```
┌──────────────────────────────────────────────────┐
│ ⚠️ Uwaga: Te akcje mogą zmienić Twoją grę!       │
├──────────────────────────────────────────────────┤
│                                                   │
│ ### 🆕 Rozpocznij nową firmę                     │
│                                                   │
│ ℹ️  Co się stanie:                               │
│    • Obecna firma zostanie zarchiwizowana        │
│    • Stworzysz nową firmę od zera               │
│    • Zachowasz DegenCoins i doświadczenie       │
│    • Możesz wrócić w zakładce "📦 Archiwum"     │
│                                                   │
│            [🚀 Rozpocznij nową firmę]            │
│                                                   │
└──────────────────────────────────────────────────┘
```

**Proces:**
1. Kliknij "🚀 Rozpocznij nową firmę"
2. Obecna firma → `archived_games[industry_id][]`
3. Usunięcie `business_games[industry_id]`
4. Przekierowanie → wybór scenariusza

---

## 📦 Zakładka 3: "📦 Archiwum firm"

**Funkcja:** Przeglądanie i przywracanie zarchiwizowanych firm

### Gdy są zarchiwizowane firmy:

```
┌────────────────────────────────────────────────────────┐
│ ### 📦 Masz 2 zarchiwizowane firmy                     │
├────────────────────────────────────────────────────────┤
│ ℹ️ Możesz przywrócić dowolną firmę                    │
│                                                         │
│ ┌──────────────────────────────────────────────────┐  │
│ │ 🏢  │ Max's Consulting (zarchiwizowana 24.10.25)│  │
│ │     │ 📅 2025-10-24 19:30:00                    │  │
│ │     │ 🏢 Level 3 | ⭐ Reputacja 45              │ [🔄 Przywróć] │
│ └──────────────────────────────────────────────────┘  │
│ ───────────────────────────────────────────────────   │
│ ┌──────────────────────────────────────────────────┐  │
│ │ 💼  │ Elite Consulting (zarchiwizowana 20.10.25)│  │
│ │     │ 📅 2025-10-20 14:15:00                    │  │
│ │     │ 🏢 Level 5 | ⭐ Reputacja 78              │ [🔄 Przywróć] │
│ └──────────────────────────────────────────────────┘  │
│                                                         │
└────────────────────────────────────────────────────────┘
```

### Gdy brak firm:

```
┌────────────────────────────────────────────────────────┐
│ ℹ️ Brak zarchiwizowanych firm                          │
│    Rozpocznij nową firmę w zakładce                    │
│    '🔄 Zarządzanie firmą'                              │
└────────────────────────────────────────────────────────┘
```

---

## 🔄 Przepływ: Przywracanie firmy

**Krok 1:** Użytkownik klika "🔄 Przywróć" przy wybranej firmie

**Krok 2:** System automatycznie:
```python
# 1. Zarchiwizuj obecną firmę
current_game → archived_games[industry_id][]

# 2. Przywróć wybraną firmę
archived_game → business_games[industry_id]

# 3. Usuń z archiwum
archived_games[industry_id].pop(idx)
```

**Krok 3:** Komunikat sukcesu + `st.rerun()`

---

## 💾 Struktura danych

### Aktywna gra:
```json
{
  "business_games": {
    "consulting": {
      "firm": {
        "name": "Max's Consulting",
        "logo": "🏢",
        "level": 3,
        "reputation": 45
      }
    }
  }
}
```

### Archiwum:
```json
{
  "archived_games": {
    "consulting": [
      {
        "firm": {
          "name": "Max's Consulting",
          "archived_name": "Max's Consulting (zarchiwizowana 24.10.2025)",
          "logo": "🏢",
          "level": 3,
          "reputation": 45
        },
        "archived_at": "2025-10-24 19:30:00"
      }
    ]
  }
}
```

---

## ✅ Zalety nowego designu

1. **Wszystko w jednym miejscu** - nie trzeba szukać ustawień w różnych miejscach
2. **Przejrzysta organizacja** - 3 logiczne zakładki (tabs)
3. **Wizualna hierarchia** - łatwo znaleźć to czego potrzebujesz
4. **Bezpieczeństwo** - ostrzeżenia przed nieodwracalnymi akcjami
5. **Podgląd na żywo** - widzisz efekt zmian (logo + nazwa)
6. **Archiwum** - nie tracisz historii firm, możesz wracać

---

## 🎯 User Experience

**Przed:**
- ❌ Ustawienia rozproszone po całym dashboardzie
- ❌ Brak możliwości ponownego rozpoczęcia gry
- ❌ Expandery (trzeba rozwijać)

**Po:**
- ✅ Wszystko w 3 zakładkach w jednym miejscu
- ✅ Możliwość rozpoczęcia nowej firmy z archiwizacją
- ✅ Zakładki (tabs) - bardziej nowoczesne i przejrzyste
- ✅ Podgląd na żywo

---

## 🚀 Zastosowanie

**Lokalizacja w kodzie:** `views/business_games.py` → `show_dashboard_tab()`

**Linijka:** ~1355

**Funkcje:**
- Zmiana nazwy firmy → `save_user_data(username, user_data)`
- Zmiana logo → grid 6 kolumn (max 12 logo)
- Rozpoczęcie nowej firmy → archiwizacja + reset + wybór scenariusza
- Przywracanie firm → swap obecna ↔ archiwalna

