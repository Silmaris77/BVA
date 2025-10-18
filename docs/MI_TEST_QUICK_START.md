# 🧠 Test Wielorakich Inteligencji - Quick Start

## 🚀 Jak uruchomić test?

### Dla użytkownika:

1. Zaloguj się do aplikacji BVA
2. Przejdź do **Narzędzia** → **Autodiagnoza**
3. Kliknij **"Rozpocznij Test MI"**
4. Odpowiedz na 40 pytań (10-15 min)
5. Zobacz swój profil i rekomendacje!

## 📁 Struktura plików

```
utils/mi_test.py           # Logika testu
views/tools.py             # UI (funkcje show_mi_*)
docs/MULTIPLE_INTELLIGENCES_TEST.md  # Pełna dokumentacja
```

## 🔧 Kluczowe funkcje

### `utils/mi_test.py`:
- `get_mi_test_questions()` - 40 pytań
- `calculate_mi_scores(answers)` - kalkulacja
- `get_bva_recommendations(top_intelligences)` - personalizacja

### `views/tools.py`:
- `show_mi_test()` - główny widok
- `show_mi_results()` - raport
- `generate_mi_pdf_report()` - export PDF

## 💡 Przykład użycia w kodzie

```python
# Rozpocznij test
st.session_state.active_tool = "mi_test"

# Pokaż test
show_mi_test()

# Dostęp do wyników
if 'mi_results' in st.session_state:
    results = st.session_state.mi_results
    top_3 = results['top_3']  # [(category, percentage), ...]
    
# Rekomendacje
from utils.mi_test import get_bva_recommendations
top_intelligences = [cat for cat, _ in results['top_3']]
recs = get_bva_recommendations(top_intelligences)
```

## 📊 Format wyników

```python
results = {
    'scores': {
        'linguistic': 23,
        'logical': 20,
        # ... pozostałe
    },
    'percentages': {
        'linguistic': 92.0,
        'logical': 80.0,
        # ... pozostałe
    },
    'top_3': [
        ('linguistic', 92.0),
        ('interpersonal', 88.0),
        ('logical', 80.0)
    ],
    'bottom_2': [
        ('musical', 48.0),
        ('naturalistic', 52.0)
    ],
    'balance_score': 44.0,
    'balance_interpretation': "Umiarkowanie wyspecjalizowany...",
    'timestamp': "2025-10-18 14:30:00"
}
```

## 🎯 Personalizacja BVA

Po zastosowaniu rekomendacji, profil użytkownika zawiera:

```python
user['mi_profile'] = {
    'top_intelligences': ['linguistic', 'interpersonal', 'logical'],
    'preferred_content_types': ['text', 'discussions', 'data'],
    'recommended_modules': ['Email Templates', 'CIQ Examples', ...],
    'recommended_tools': ['AI Coach', 'Conversation Analyzer', ...],
    'learning_tips': ['Rób notatki tekstowe', 'Ucz się w grupach', ...]
}
```

## 🐛 Troubleshooting

### Test nie zapisuje wyników
→ Sprawdź czy użytkownik jest zalogowany (`st.session_state.logged_in`)

### PDF nie generuje się
→ Sprawdź czy istnieje `assets/fonts/DejaVuSans.ttf`

### Wyniki się nie wyświetlają
→ Sprawdź czy `st.session_state.mi_completed == True`

## 📚 Więcej informacji

Pełna dokumentacja: `docs/MULTIPLE_INTELLIGENCES_TEST.md`
