# 💬 Tooltips w Mapach Myśli - Instrukcja

## 📋 Przegląd

Mapy myśli wspierają teraz wyświetlanie tooltipów (dymków z wyjaśnieniami) po najechaniu myszką na węzeł. To pozwala dodać dodatkowe informacje bez zaśmiecania wizualnej struktury mapy.

## 🎯 Jak dodać tooltip do węzła

W pliku JSON lekcji, w strukturze `mind_map`, możesz dodać pole `description` lub `tooltip` do dowolnego węzła:

### Przykład 1: Tooltip w centralnym węźle

```json
{
  "central_node": {
    "id": "ciq_main",
    "label": "🗣️ Conversational Intelligence",
    "size": 30,
    "color": "#43C6AC",
    "description": "Conversational Intelligence (C-IQ) to umiejętność prowadzenia rozmów, które budują zaufanie, współpracę i innowacyjność w organizacji."
  }
}
```

### Przykład 2: Tooltips w kategoriach

```json
{
  "categories": [
    {
      "id": "neurobiologia",
      "label": "🧠 Neurobiologia rozmów",
      "size": 20,
      "color": "#FF9950",
      "tooltip": "Badania pokazują, że rozmowy aktywują te same obszary mózgu co nagrody i zagrożenia, wpływając na wydzielanie neurotransmiterów.",
      "details": [
        {
          "id": "kortyzol",
          "label": "⚠️ Kortyzol",
          "size": 12,
          "color": "#FFB380",
          "description": "Kortyzol to hormon stresu wydzielany w sytuacjach zagrożenia. W rozmowach wysokie poziomy kortyzolu prowadzą do obronnej postawy i braku otwartości."
        },
        {
          "id": "oksytocyna",
          "label": "❤️ Oksytocyna",
          "size": 12,
          "color": "#FFB380",
          "tooltip": "Oksytocyna to 'hormon więzi' wydzielany podczas pozytywnych interakcji. Zwiększa zaufanie, empatię i chęć współpracy."
        }
      ]
    }
  ]
}
```

### Przykład 3: Tooltips w rozwiązaniach

```json
{
  "solutions": [
    {
      "id": "listening",
      "label": "👂 Aktywne słuchanie",
      "size": 15,
      "color": "#8A9BFF",
      "description": "Technika polegająca na pełnej koncentracji na rozmówcy, parafrazowaniu i zadawaniu pytań pogłębiających. Buduje zaufanie i pokazuje szacunek."
    }
  ]
}
```

## 📝 Wskazówki dotyczące pisania tooltipów

### ✅ Dobre praktyki:

1. **Długość**: 1-3 zdania (50-150 znaków)
2. **Język**: Prosty i zrozumiały
3. **Wartość**: Dodaj kontekst, definicję lub przykład
4. **Szczegółowość**: Więcej szczegółów niż w labelce węzła

### ❌ Czego unikać:

1. Nie powtarzaj dokładnie tego co jest w labelce
2. Nie pisz długich esejów (powyżej 200 znaków)
3. Nie używaj skomplikowanego żargonu bez wyjaśnienia
4. Nie dodawaj tooltipów do każdego węzła (tylko do tych, które wymagają wyjaśnienia)

## 🎨 Przykłady dobrych tooltipów

### Terminy naukowe:
```json
{
  "label": "🧪 Dopamina",
  "description": "Neuroprzekaźnik odpowiedzialny za system nagrody w mózgu. Wydzielany podczas przyjemnych doświadczeń, wzmacnia zachowania prowadzące do nagrody."
}
```

### Koncepcje biznesowe:
```json
{
  "label": "📊 KPI",
  "tooltip": "Key Performance Indicator - mierzalny wskaźnik efektywności używany do oceny sukcesu organizacji w osiąganiu celów biznesowych."
}
```

### Techniki/Narzędzia:
```json
{
  "label": "🎯 SMART Goals",
  "description": "Framework tworzenia celów: Specific (konkretny), Measurable (mierzalny), Achievable (osiągalny), Relevant (istotny), Time-bound (ograniczony czasowo)."
}
```

### Procesy:
```json
{
  "label": "🔄 Feedback Loop",
  "tooltip": "Cykl informacji zwrotnej: działanie → obserwacja → analiza → korekta → działanie. Kluczowy dla ciągłego doskonalenia."
}
```

## 🔧 Gdzie dodawać tooltips?

### Priorytet 1 (WYSOKI):
- ✅ Terminy naukowe (kortyzol, dopamina, neuroplastyczność)
- ✅ Skróty i akronimy (KPI, ROI, OKR, C-IQ)
- ✅ Specjalistyczny żargon

### Priorytet 2 (ŚREDNI):
- ⭐ Złożone koncepcje wymagające wyjaśnienia
- ⭐ Techniki i metodologie
- ⭐ Case study (kontekst przykładu)

### Priorytet 3 (NISKI):
- 💡 Oczywiste pojęcia (można pominąć)
- 💡 Węzły które są samo-wyjaśniające

## 🚀 Jak to działa technicznie?

System automatycznie sprawdza czy węzeł ma pole `description` lub `tooltip` i:
1. Jeśli **TAK** → dodaje parametr `title` do Node (wyświetla się po najechaniu)
2. Jeśli **NIE** → węzeł bez tooltipa (normalny)

Obsługiwane przez:
- `utils/mind_map.py` → funkcja `create_data_driven_mind_map()`
- Biblioteka: `streamlit-agraph` → parametr `title` w Node
- Renderowanie: HTML tooltip natywny przeglądarki

## 📦 Przykład kompletnej struktury z tooltipami

```json
{
  "mind_map": {
    "central_node": {
      "id": "main",
      "label": "🎯 C-IQ Master",
      "description": "Conversational Intelligence dla liderów"
    },
    "categories": [
      {
        "id": "cat1",
        "label": "🧠 Neurobiologia",
        "tooltip": "Jak mózg reaguje na różne typy rozmów",
        "details": [
          {
            "id": "detail1",
            "label": "Kortyzol",
            "description": "Hormon stresu - aktywowany przez zagrożenie w rozmowach"
          }
        ]
      }
    ],
    "solutions": [
      {
        "id": "sol1",
        "label": "👂 Aktywne słuchanie",
        "tooltip": "Pełna koncentracja na rozmówcy z parafrazowaniem"
      }
    ]
  }
}
```

## ✨ Rezultat

Gdy użytkownik najedzie myszką na węzeł:
- 🖱️ Pojawia się dymek z opisem
- 📖 Użytkownik może przeczytać dodatkowy kontekst
- 🎓 Mapa staje się narzędziem edukacyjnym, nie tylko wizualizacją

---

*Aktualizacja: Wsparcie dla tooltipów dodane 2025-10-15*
