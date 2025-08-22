# 🚀 Mind Map System - Quick Start Guide

## Szybki test systemu

### 1. Sprawdź czy system jest gotowy:
```bash
python -c "import json; data=json.load(open('data/lessons/B1C1L1.json', 'r', encoding='utf-8')); print('Mind map ready:', 'mind_map' in data)"
```

### 2. Uruchom aplikację:
```bash
streamlit run main.py
```

### 3. Przejdź do lekcji B1C1L1:
- Zaloguj się do aplikacji
- Wybierz "Lekcje" z menu
- Kliknij na lekcję "Strach przed stratą" (B1C1L1)
- Przejdź do zakładki "Podsumowanie" 
- Kliknij na "🗺️ Interaktywna mapa myśli"

### 4. Co powinieneś zobaczyć:
- Interaktywną mapę z centralnym węzłem "💸 STRACH PRZED STRATĄ"
- 4 główne kategorie (teoria perspektywy, efekt dyspozycji, dopamina, framing)
- 4 praktyczne rozwiązania  
- Case study Kuby i $MOONZ
- Możliwość klikania i przesuwania węzłów

## Dodawanie mind map do nowej lekcji

### 1. Użyj generator szablonów:
```python
from utils.mind_map_template import generate_mind_map_template

template = generate_mind_map_template(
    lesson_title="Nazwa Twojej Lekcji",
    main_topics=["Temat 1", "Temat 2", "Temat 3"],
    include_case_study=True
)

print(template)  # Skopiuj wynik do pliku lekcji
```

### 2. Dodaj do pliku lekcji:
```json
{
  "id": "B1C1L2",
  "title": "Twoja lekcja",
  "sections": { ... },
  "mind_map": {
    // Wklej tutaj wygenerowaną strukturę
  },
  "outro": { ... }
}
```

### 3. Gotowe!
System automatycznie wykryje strukturę mind_map i użyje jej do wyświetlenia.

## Troubleshooting

### Problem: Mind map się nie wyświetla
- Sprawdź czy streamlit-agraph jest zainstalowany: `pip install streamlit-agraph`
- Sprawdź składnię JSON w pliku lekcji
- Sprawdź logi w konsoli Streamlit

### Problem: Błędy w strukturze
- Upewnij się że wszystkie ID są unikalne
- Sprawdź czy connections odwołują się do istniejących ID
- Porównaj ze strukturą w `data/mind_map_examples/B1C1L1_mind_map.json`

## Dokumentacja
📚 Pełna dokumentacja: `MIND_MAP_USER_GUIDE.md`  
📊 Raport implementacji: `MIND_MAP_IMPLEMENTATION_COMPLETE.md`
