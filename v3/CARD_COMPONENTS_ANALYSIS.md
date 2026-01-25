# Analiza Komponentów Kart - OJT Lesson 2

## ✅ Istniejące Komponenty (wszystkie wymagane!)

Świetna wiadomość - **wszystkie potrzebne komponenty już istnieją** w projekcie v3:

1. ✅ **HeroCard.tsx** - dla `type: "hero"`
2. ✅ **DataCard.tsx** - dla `type: "data"`
3. ✅ **ConceptCard.tsx** - dla `type: "content"` (mapowane w CardRenderer)
4. ✅ **StoryCard.tsx** - dla `type: "story"`
5. ✅ **LightbulbCard.tsx** - dla `type: "lightbulb"`
6. ✅ **PracticeCard.tsx** - dla `type: "practice"`
7. ✅ **QuizCard.tsx** - dla `type: "quiz"`
8. ✅ **HabitBuilderCard.tsx** - dla `type: "habit"`
9. ✅ **ChecklistCard.tsx** - dla `type: "checklist"`
10. ✅ **TestCard.tsx** - dla `type: "test"`
11. ✅ **AchievementCard.tsx** - dla `type: "achievement"`
12. ✅ **EndingCard.tsx** - dla `type: "ending"`

---

## ⚠️ Różnice w Interfejsach

Niektóre komponenty mają **inne struktury danych** niż założono w SQL. Wymagają adaptacji SQL lub komponentów:

### 1. StoryCard - WYMAGA ZMIAN W SQL

**Aktualny interface:**
```tsx
interface StoryCardProps {
    icon?: string
    badge?: string
    title: string
    scenario: {         // ❌ W SQL mamy 'scenarios' (array)
        heading: string
        text: string
    }
    consequences: (string | { heading: string; text: string })[]
    lesson: {
        heading: string
        text: string
    }
}
```

**W SQL mamy:**
```json
{
  "type": "story",
  "scenarios": [  // ❌ Array z type: "bad"/"good", dialogue array
    {
      "type": "bad",
      "dialogue": [{"speaker": "...", "text": "..."}],
      "consequences": ["..."]
    }
  ],
  "lesson": "..."  // ❌ String, nie object
}
```

**Rozwiązania:**
- **Opcja A:** Zmodyfikować StoryCard aby obsługiwał scenarios array + dialogue + good/bad types
- **Opcja B:** Zmienić strukturę w SQL aby pasowała do istniejącego StoryCard (prostsze)

---

### 2. PracticeCard - WYMAGA ROZSZERZENIA

**Aktualny interface:**
```tsx
interface PracticeCardProps {
    title: string
    content: string
    keyPoints?: string[]
    actionSteps?: string[]
}
```

**W SQL mamy dodatkowo:**
```json
{
  "scenario": "...",        // ❌ Brak w interface
  "instruction": "...",     // ❌ Brak w interface  
  "inputs": [               // ❌ Brak w interface
    {"label": "...", "placeholder": "..."}
  ],
  "sampleAnswers": {...}    // ❌ Brak w interface
}
```

**Rozwiązanie:**
Rozszerzyć PracticeCard o:
- `scenario?: string` - wyświetlić jako callout box
- `instruction?: string` - wyświetlić przed inputs
- `inputs?: Array<{label, placeholder}>` - textarea/input fields
- `sampleAnswers?: {title, answers, tip}` - collapsible reveal section

---

### 3. LightbulbCard - WYMAGA WERYFIKACJI

**Trzeba sprawdzić czy obsługuje:**
- `comparison` object z headers i rows
- `whenToTell` object z cases array
- `examples` array z type: "wrong"/"correct"
- `insights` array z type: "positive"/"negative"

---

### 4. HabitBuilderCard - WYMAGA ROZSZERZENIA

**Aktualny interface:**
```tsx
interface HabitAction {
    text: string  // ❌ W SQL mamy więcej pól
    id: string
}
```

**W SQL mamy:**
```json
{
  "habits": [
    {
      "id": "habit1",
      "icon": "🗓️",        // ❌ Brak w interface
      "title": "...",      // ❌ Brak w interface (jest tylko 'text')
      "description": "...", // ❌ Brak w interface
      "goal": "..."        // ❌ Brak w interface
    }
  ],
  "tip": "..."  // ❌ Brak w props
}
```

**Rozwiązanie:**
Rozszerzyć HabitBuilderCard o pola: icon, title, description, goal, tip

---

### 5. ChecklistCard - WYMAGA ROZSZERZENIA

**Aktualny interface:**
```tsx
interface ChecklistCardProps {
    title: string
    description?: string
    items: ChecklistItem[]  // ❌ Płaska lista
}
```

**W SQL mamy:**
```json
{
  "sections": [  // ❌ Multi-section structure
    {
      "id": "before",
      "title": "📋 Przed wspólnym dniem:",
      "items": [{"id": "check1", "text": "..."}]
    }
  ]
}
```

**Rozwiązanie:**
Rozszerzyć ChecklistCard aby obsługiwał `sections` zamiast płaskich `items`

---

### 6. EndingCard - WYMAGA WERYFIKACJI

**Trzeba sprawdzić czy obsługuje:**
- `implementationPlan` object ze steps array
- `resources` array z icon/title/description
- `finalQuote` object z text/author
- `closing` i `community` strings

---

### 7. TestCard - WYMAGA WERYFIKACJI

**Trzeba sprawdzić czy obsługuje:**
- `requirements` object (questions, time, passing_score)
- `note` string
- `description` string
- `icon` property

---

### 8. AchievementCard - WYMAGA WERYFIKACJI

**Trzeba sprawdzić czy obsługuje:**
- `skillsUnlocked` array
- `badge_name` string
- `description` vs `content`

---

## 📋 Plan Działania

### Wariant A: Modyfikacja SQL (SZYBSZE - REKOMENDOWANE)

Dostosować struktury JSON w plikach SQL aby pasowały do istniejących komponentów:

**Do zmiany:**
1. **StoryCard** - zmienić `scenarios` array na pojedynczy `scenario` object
2. **PracticeCard** - przenieść `scenario`, `instruction`, `inputs` do `content` jako markdown
3. **HabitBuilderCard** - połączyć `icon + title + description + goal` w jedno pole `text`
4. **ChecklistCard** - spłaszczyć `sections` do jednej listy `items`
5. Pozostałe - sprawdzić czy aktualne props działają

**Czas realizacji:** 2-3 godziny

---

### Wariant B: Modyfikacja Komponentów (DOKŁADNIEJSZE)

Rozszerzyć komponenty aby obsługiwały wszystkie pola z SQL:

**Do zmiany:**
1. **StoryCard.tsx** - dodać support dla scenarios array, dialogue, good/bad types
2. **PracticeCard.tsx** - dodać inputs, scenario, instruction, sampleAnswers
3. **HabitBuilderCard.tsx** - rozszerzyć interface o icon, title, description, goal, tip
4. **ChecklistCard.tsx** - dodać support dla sections
5. **LightbulbCard.tsx** - sprawdzić/dodać comparison, whenToTell, examples, insights
6. **EndingCard.tsx** - sprawdzić/dodać implementationPlan, resources, finalQuote
7. **TestCard.tsx** - sprawdzić/dodać requirements, note, description, icon
8. **AchievementCard.tsx** - sprawdzić/dodać skillsUnlocked, badge_name

**Czas realizacji:** 6-8 godzin

---

## 🎯 Rekomendacja

**Wariant A (Modyfikacja SQL)** - bo:
- Komponenty już działają i są przetestowane
- Szybsze wdrożenie
- Mniej ryzyka błędów
- SQL łatwiej zmienić niż komponenty
- Możemy przetestować każdą kartę osobno

**Następne kroki:**
1. Sprawdzić dokładnie interfejsy wszystkich 12 komponentów
2. Dostosować struktury JSON w SQL do istniejących props
3. Przetestować każdą grupę kart (1-5, 6-10, etc.)
4. Połączyć w finalny SQL z wszystkimi 29 kartami

---

## 🔍 Potrzebne Weryfikacje

Czy mogę przeczytać pełne interfejsy tych komponentów aby dokładnie dostosować SQL?

1. LightbulbCard.tsx - czy obsługuje comparison tables?
2. EndingCard.tsx - jaki dokładnie interface?
3. TestCard.tsx - jaki dokładny interface?
4. AchievementCard.tsx - jaki dokładny interface?
5. DataCard.tsx - czy już ma content i sources? (chyba tak, bo modyfikowaliśmy)

Odpowiedz czy mam:
- **A) Przeczytać te komponenty i dostosować SQL**
- **B) Rozszerzyć komponenty aby obsługiwały bogatsze struktury**
