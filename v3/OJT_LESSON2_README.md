# OJT Lesson 2 - SQL Implementation Guide

## Struktura lekcji

Lekcja "Model OJT - 5 Etapów" składa się z **29 kart** podzielonych na 5 grup dla łatwiejszego testowania i debugowania.

### Podział kart:

**Part 1 (Karty 1-5):** `insert_ojt_lesson2_full.sql`
- 1: Hero - Jak rozwijać pracowników bez odrywania ich od pracy?
- 2: Data - Dlaczego On-the-Job Training działa?
- 3: Content - Czym jest Model Treningu On-the-Job?
- 4: Content - 5 Etapów Cyklu Treningu OJT
- 5: Content - Etap 1: Rozmowa na początku dnia

**Part 2 (Karty 6-10):** `insert_ojt_lesson2_cards_6_10.sql`
- 6: Story - Przykład: Dobry vs Zły Kontrakt
- 7: Lightbulb - Kontrakt = Psychologiczne Bezpieczeństwo
- 8: Content - Etap 2: Odprawa przed rozmową
- 9: Practice - Ćwiczenie: Przygotuj pytania na odprawę
- 10: Story - Przykład: Siła Demonstracji

**Part 3 (Karty 11-15):** `insert_ojt_lesson2_cards_11_15.sql`
- 11: Content - Etap 3: Obserwacja rozmowy z klientem
- 12: Lightbulb - Dlaczego Fakty > Interpretacje?
- 13: Quiz - Sprawdź swoją wiedzę: Obserwacja
- 14: Practice - Ćwiczenie: Przekształć interpretacje w fakty
- 15: Content - Etap 4: Analiza po rozmowie

**Part 4 (Karty 16-20):** `insert_ojt_lesson2_cards_16_20.sql`
- 16: Story - Przykład: Analiza, która zmieniła wszystko
- 17: Lightbulb - Pytaj, nie mów - dlaczego to działa?
- 18: Quiz - Sprawdź swoją wiedzę: Analiza
- 19: Practice - Przekształć krytykę w pytania coachingowe
- 20: Content - Etap 5: Podsumowanie całego dnia

**Part 5 (Karty 21-29):** `insert_ojt_lesson2_cards_21_29.sql`
- 21: Data - Jak często robić trening OJT?
- 22: Story - Dobry vs Zły Plan Wdrożeniowy
- 23: Quiz - Sprawdź wiedzę: Podsumowanie Modelu OJT
- 24: Habit - Zbuduj swoje nawyki trenera OJT
- 25: Checklist - Twoja Checklista Trenera OJT
- 26: Lightbulb - OJT to Inwestycja, nie Koszt
- 27: Test - Test Końcowy: Model Treningu OJT
- 28: Achievement - Certyfikowany Trener OJT!
- 29: Ending - Twoje Następne Kroki

---

## Instrukcja wdrożenia

### Krok 1: Cleanup (opcjonalny)

Jeśli masz wcześniejsze wersje tej lekcji, usuń je przed wstawieniem nowej:

```sql
DELETE FROM lessons WHERE lesson_id LIKE 'ojt_lesson_2%';
```

### Krok 2: Testowanie poszczególnych części

Każdy plik SQL zawiera **tymczasowy `lesson_id`** dla niezależnego testowania:

- `insert_ojt_lesson2_full.sql` → `ojt_lesson_2_model` (5 kart)
- `insert_ojt_lesson2_cards_6_10.sql` → `ojt_lesson_2_model_part2` (5 kart)
- `insert_ojt_lesson2_cards_11_15.sql` → `ojt_lesson_2_model_part3` (5 kart)
- `insert_ojt_lesson2_cards_16_20.sql` → `ojt_lesson_2_model_part4` (5 kart)
- `insert_ojt_lesson2_cards_21_29.sql` → `ojt_lesson_2_model_part5` (9 kart)

**Sposób testowania:**
1. Uruchom jeden plik SQL (np. `insert_ojt_lesson2_full.sql`)
2. Sprawdź w aplikacji czy karty 1-5 wyświetlają się poprawnie
3. Jeśli OK, usuń tę testową lekcję: `DELETE FROM lessons WHERE lesson_id = 'ojt_lesson_2_model';`
4. Przejdź do następnego pliku

### Krok 3: Finalne wdrożenie (wszystkie 29 kart)

Gdy wszystkie części zostały przetestowane, potrzebujesz **jednej pełnej lekcji z wszystkimi kartami**.

Możesz:
- **Opcja A:** Ręcznie połączyć wszystkie 5 tablic `cards` w jeden plik
- **Opcja B:** Użyć narzędzia do mergowania JSON (np. jq)
- **Opcja C:** Poprosić mnie o stworzenie jednego pliku z wszystkimi 29 kartami

---

## Struktura danych kart

### Card Types i ich pola:

**hero:**
```json
{
  "type": "hero",
  "title": "...",
  "content": "...",
  "sections": [
    {"icon": "👥", "title": "Dla kogo", "content": "...", "list": ["..."]}
  ]
}
```

**data:**
```json
{
  "type": "data",
  "title": "...",
  "content": "... (opcjonalny intro)",
  "stats": [{"value": "70%", "label": "..."}],
  "callout": {"type": "info", "title": "...", "text": "..."},
  "sources": "Źródła: ..."
}
```

**content:**
```json
{
  "type": "content",
  "title": "...",
  "content": "...",
  "remember": {"title": "Pamiętaj:", "items": ["..."]},
  "callout": {"type": "warning", "text": "..."}
}
```

**story:**
```json
{
  "type": "story",
  "title": "...",
  "scenarios": [
    {
      "type": "bad",
      "title": "❌ ŹLE",
      "dialogue": [{"speaker": "...", "text": "..."}],
      "consequences": ["..."]
    }
  ],
  "lesson": "Kluczowa lekcja: ..."
}
```

**lightbulb:**
```json
{
  "type": "lightbulb",
  "icon": "💡",
  "title": "...",
  "content": "...",
  "comparison": {
    "headers": ["...", "..."],
    "rows": [{"wrong": "❌ ...", "right": "✅ ..."}]
  }
}
```

**practice:**
```json
{
  "type": "practice",
  "title": "...",
  "scenario": "...",
  "instruction": "...",
  "inputs": [{"label": "...", "placeholder": "..."}],
  "sampleAnswers": {"title": "...", "answers": ["..."]}
}
```

**quiz:**
```json
{
  "type": "quiz",
  "title": "...",
  "questions": [
    {
      "id": 1,
      "text": "...",
      "options": [
        {"letter": "A", "text": "...", "correct": false}
      ],
      "explanation": "..."
    }
  ]
}
```

**habit:**
```json
{
  "type": "habit",
  "title": "...",
  "instruction": "...",
  "habits": [
    {"id": "habit1", "icon": "🗓️", "title": "...", "description": "...", "goal": "..."}
  ],
  "tip": "..."
}
```

**checklist:**
```json
{
  "type": "checklist",
  "title": "...",
  "instruction": "...",
  "sections": [
    {
      "id": "before",
      "title": "📋 Przed:",
      "items": [{"id": "check1", "text": "..."}]
    }
  ]
}
```

**test:**
```json
{
  "type": "test",
  "icon": "🏆",
  "title": "...",
  "description": "...",
  "requirements": {"questions": 10, "time": "2:30", "passing_score": "80%"}
}
```

**achievement:**
```json
{
  "type": "achievement",
  "badge": "🏆",
  "title": "...",
  "description": "...",
  "skillsUnlocked": ["..."],
  "xp": 300,
  "badge_name": "..."
}
```

**ending:**
```json
{
  "type": "ending",
  "title": "...",
  "introduction": "...",
  "implementationPlan": {...},
  "resources": [...],
  "finalQuote": {"text": "...", "author": "..."}
}
```

---

## Znane problemy i rozwiązania

### Problem 1: Escape characters w JSON
**Symptom:** `\"` pojawia się w tekście zamiast cudzysłowów  
**Rozwiązanie:** W PostgreSQL JSONB automatycznie parsuje escape characters - to jest OK

### Problem 2: Badge type nie istnieje
**Symptom:** `Cannot read properties of undefined (reading 'bg')`  
**Rozwiązanie:** Sprawdź czy `callout.type` to jeden z: `warning`, `success`, `info`

### Problem 3: Comparison table nie renderuje się
**Symptom:** Tabela porównawcza pusta  
**Rozwiązanie:** Sprawdź czy komponent obsługuje `comparison` field (ConceptCard, LightbulbCard)

### Problem 4: Practice inputs nie działają
**Symptom:** Pola tekstowe nie przyjmują inputu  
**Rozwiązanie:** Sprawdź czy PracticeCard ma state management dla input values

---

## TODO: Komponenty do aktualizacji

Niektóre typy kart mogą wymagać aktualizacji komponentów v3 BVA:

### Komponenty prawdopodobnie wymagające zmian:

**HabitCard.tsx** - nowy typ karty
- Nie istnieje w obecnej wersji
- Potrzebuje checkbox state management
- UI: lista nawyków z checkboxami + tip box

**ChecklistCard.tsx** - nowy typ karty
- Nie istnieje w obecnej wersji
- Potrzebuje multi-section layout z checkboxami
- State: zaznaczone items per section

**TestCard.tsx** - nowy typ karty
- Może istnieć jako QuizCard z timerem
- Potrzebuje timer countdown i passing score logic
- Start test button + time limit enforcement

**AchievementCard.tsx** - nowy typ karty
- Prawdopodobnie nie istnieje
- UI: duży badge + lista unlocked skills + XP indicator
- Animacje confetti/celebration (opcjonalnie)

**EndingCard.tsx** - nowy typ karty
- Może być standardowy ContentCard
- Potrzebuje layout dla: timeline steps + resource list + quote
- Download/print resources functionality (opcjonalnie)

### Komponenty prawdopodobnie działające:

- **HeroCard.tsx** - używa sections array
- **DataCard.tsx** - zaktualizowany (content, sources, callout.title)
- **ContentCard.tsx** - standardowy, obsługuje remember/callout
- **StoryCard.tsx** - obsługuje scenarios array z dialogue
- **LightbulbCard.tsx** - obsługuje comparison tables
- **PracticeCard.tsx** - obsługuje inputs i sampleAnswers
- **QuizCard.tsx** - obsługuje questions array

---

## Kontakt

Jeśli napotkasz problemy podczas wdrażania, sprawdź:
1. Console errors w DevTools
2. Czy wszystkie komponenty kart istnieją w `v3/src/components/lesson/cards/`
3. Czy CardRenderer.tsx mapuje wszystkie typy kart
4. Logi Supabase czy INSERT się powiódł

**Powodzenia! 🚀**
