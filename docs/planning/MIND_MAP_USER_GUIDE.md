# Przewodnik po skalowalnym systemie Mind Map

## 🎯 Przegląd systemu

System mind map dla BrainVenture Academy został przeprojektowany tak, aby umożliwić łatwe dodawanie interaktywnych map myśli do lekcji przez twórców treści. System obsługuje trzy tryby:

1. **Data-driven maps** - Mapy oparte na danych JSON w pliku lekcji
2. **Backward compatibility** - Zachowanie istniejącej mapy B1C1L1 
3. **Auto-generated maps** - Automatyczne generowanie map z struktury lekcji

## 📁 Struktura plików

```
utils/
├── mind_map.py              # Główny moduł systemu mind map
└── mind_map_template.py     # Generator szablonów dla nowych lekcji

data/
├── lessons/
│   └── B1C1L1.json         # Przykład lekcji z mind_map
└── mind_map_examples/
    └── B1C1L1_mind_map.json # Przykład struktury mind_map
```

## 🔧 Jak dodać mind map do lekcji

### Krok 1: Dodaj sekcję `mind_map` do pliku JSON lekcji

```json
{
  "id": "B1C1L1",
  "title": "Strach przed stratą",
  "mind_map": {
    "central_node": {
      "id": "main_topic",
      "label": "💸 GŁÓWNY TEMAT",
      "size": 30,
      "color": "#FF6B6B",
      "font_size": 16
    },
    "categories": [...],
    "solutions": [...],
    "case_study": {...},
    "connections": [...],
    "config": {...}
  },
  "outro": {...}
}
```

### Krok 2: Zdefiniuj strukturę mind_map

Kompletna struktura zawiera:

#### Central Node (węzeł centralny)
```json
"central_node": {
  "id": "main_topic",           // Unikalny ID
  "label": "💸 GŁÓWNY TEMAT",   // Tekst wyświetlany (emoji + tekst)
  "size": 30,                   // Rozmiar węzła
  "color": "#FF6B6B",           // Kolor tła węzła
  "font_size": 16               // Rozmiar czcionki
}
```

#### Categories (kategorie główne)
```json
"categories": [
  {
    "id": "kategoria_1",
    "label": "📊 Nazwa kategorii",
    "size": 20,
    "color": "#4ECDC4",
    "font_size": 12,
    "details": [                // Szczegóły kategorii
      {
        "id": "szczegol_1",
        "label": "💡 Szczegół",
        "size": 12,
        "color": "#DDA0DD",
        "font_size": 10
      }
    ]
  }
]
```

#### Solutions (rozwiązania praktyczne)
```json
"solutions": [
  {
    "id": "rozwiazanie_1",
    "label": "🔧 Praktyczne rozwiązanie",
    "size": 15,
    "color": "#90EE90",
    "font_size": 11
  }
]
```

#### Case Study (studium przypadku)
```json
"case_study": {
  "id": "case_study",
  "label": "👨‍💻 Case Study: Nazwa",
  "size": 18,
  "color": "#FF8C42",
  "font_size": 12,
  "details": [
    {
      "id": "case_detail_1",
      "label": "📊 Szczegół case study",
      "size": 10,
      "color": "#FFB347",
      "font_size": 9
    }
  ]
}
```

#### Connections (połączenia)
```json
"connections": [
  {
    "from": "main_topic",      // ID węzła źródłowego
    "to": "kategoria_1"        // ID węzła docelowego
  }
]
```

#### Config (konfiguracja wyświetlania)
```json
"config": {
  "width": 800,              // Szerokość mapy
  "height": 600,             // Wysokość mapy
  "physics": true,           // Fizyka animacji
  "directed": false,         // Czy graf skierowany
  "hierarchical": false      // Czy układ hierarchiczny
}
```

## 🎨 Paleta kolorów

### Kolory węzłów głównych
- `#FF6B6B` - Czerwony (centralny węzeł)
- `#4ECDC4` - Morski (kategorie)
- `#45B7D1` - Niebieski (kategorie)
- `#96CEB4` - Miętowy (kategorie)
- `#FECA57` - Żółty (kategorie)

### Kolory funkcjonalne
- `#90EE90` - Zielony jasny (rozwiązania)
- `#98FB98` - Zielony miętowy (rozwiązania)
- `#FF8C42` - Pomarańczowy (case study)
- `#FFB347` - Pomarańczowy jasny (detale case study)
- `#DDA0DD` - Fioletowy jasny (szczegóły)

## 🚀 Generator szablonów

### Automatyczne generowanie szablonu

```python
from utils.mind_map_template import generate_mind_map_template

template = generate_mind_map_template(
    lesson_title="Nazwa lekcji",
    main_topics=["Temat 1", "Temat 2", "Temat 3"],
    include_case_study=True
)

# Wynik: kompletna struktura mind_map gotowa do wklejenia
```

### Dostępne funkcje generatora

- `generate_mind_map_template()` - Podstawowy generator
- `create_mind_map_for_lesson()` - Generator z autodetekcją typu lekcji
- `create_psychology_mind_map()` - Specjalny dla lekcji psychologii
- `create_technical_mind_map()` - Specjalny dla lekcji technicznych
- `create_strategy_mind_map()` - Specjalny dla lekcji strategicznych

## 📊 Przykład kompletnej struktury

Zobacz plik `data/mind_map_examples/B1C1L1_mind_map.json` dla pełnego przykładu.

## 🔄 Logika systemu

### Algorytm decyzyjny
```
1. Czy lekcja ma sekcję 'mind_map'?
   ✅ TAK → Użyj create_data_driven_mind_map()
   
2. Czy to lekcja B1C1L1?
   ✅ TAK → Użyj create_b1c1l1_mind_map() (backward compatibility)
   
3. W przeciwnym razie:
   📊 Użyj create_auto_generated_mind_map()
```

### Fallback behavior
- Jeśli `streamlit-agraph` nie jest dostępne → wyświetl ostrzeżenie
- Jeśli błąd w danych → wyświetl komunikat o błędzie
- Dla lekcji bez `mind_map` → automatyczne generowanie z informacją

## 🧪 Testowanie

### Test podstawowy
```bash
python -c "import json; data=json.load(open('data/lessons/B1C1L1.json', 'r', encoding='utf-8')); print('Mind map present:', 'mind_map' in data)"
```

### Uruchomienie aplikacji
```bash
streamlit run main.py
```

Następnie przejdź do lekcji B1C1L1 aby zobaczyć mind map w akcji.

## 📝 Best Practices

### Do's ✅
- Używaj emoji w labelach dla lepszej wizualizacji
- Zachowaj spójność kolorów w ramach lekcji
- Ogranicz liczbę głównych kategorii do 4-6
- Dodaj szczegóły tylko do najważniejszych kategorii
- Używaj case study dla praktycznych przykładów

### Don'ts ❌
- Nie twórz zbyt wielu szczegółów (max 3-4 na kategorię)
- Nie używaj za długich tekstów w labelach
- Nie mieszaj stylów kolorów między lekcjami
- Nie zapomnij o connections dla central node

## 🔧 Rozwiązywanie problemów

### Problem: Mind map się nie wyświetla
- Sprawdź czy `streamlit-agraph` jest zainstalowane
- Sprawdź składnię JSON w pliku lekcji
- Sprawdź czy wszystkie wymagane pola są obecne

### Problem: Błędy w strukturze
- Sprawdź czy wszystkie ID są unikalne
- Sprawdź czy connections odwołują się do istniejących ID
- Sprawdź czy struktura JSON jest poprawna

### Problem: Złe wyświetlanie
- Dostosuj rozmiary węzłów (size)
- Zmień kolory dla lepszego kontrastu
- Dostosuj konfigurację physics/hierarchical

## 🎯 Następne kroki

1. **Migracja istniejących lekcji** - Dodanie mind_map do innych lekcji
2. **Rozszerzenie szablonów** - Tworzenie specjalistycznych szablonów
3. **Integracja z AI** - Automatyczne generowanie na podstawie treści lekcji
4. **Analytics** - Śledzenie interakcji z mind maps

---

**Utworzono:** 29 maja 2025  
**Status:** ✅ Kompletne i gotowe do użycia  
**Następna aktualizacja:** Po dodaniu nowych funkcji
