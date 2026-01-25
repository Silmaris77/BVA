# 🧪 Testing Guide - OJT Lesson 2 Card Components

## Plan Testowania Rozszerzonych Komponentów

---

## 🎯 Cel Testów

Upewnić się, że:
1. ✅ Wszystkie 5 rozszerzonych komponentów renderują nowe formaty poprawnie
2. ✅ Backwards compatibility działa (stare lekcje nie zepsute)
3. ✅ Wszystkie 29 kart OJT Lesson 2 wyświetlają się bez błędów
4. ✅ Interaktywne elementy (inputs, checkboxes, collapsible) działają

---

## 📋 Przygotowanie do Testów

### Krok 1: Backup obecnej bazy danych

```sql
-- Jeśli masz istniejące lessons, zrób backup
SELECT * FROM lessons WHERE lesson_id LIKE 'ojt%';
```

### Krok 2: Wyczyść stare wersje OJT Lesson 2 (jeśli istnieją)

```sql
DELETE FROM lessons WHERE lesson_id = 'ojt_lesson_2_model';
```

---

## 🧪 Testy Etap 1: Cards 1-5 (Podstawowe)

### A. Wstaw SQL

```bash
# Uruchom w psql/pgAdmin
psql -U your_user -d your_database -f insert_ojt_lesson2_full.sql
```

Lub w aplikacji database query tool:
```sql
-- Skopiuj całą zawartość insert_ojt_lesson2_full.sql
-- Wykonaj
```

### B. Otwórz lekcję w aplikacji

1. Zaloguj się do BVA v3
2. Przejdź do **Nauka** → Lekcje
3. Znajdź **"Model OJT - 5 Etapów treningu On-the-Job"**
4. Kliknij **Rozpocznij**

### C. Sprawdź każdą kartę

| Card # | Typ | Co sprawdzić | ✅/❌ |
|--------|-----|--------------|-------|
| 1 | Hero | Badge, title, sections[], icon ✨ |  |
| 2 | Data | Stats grid, callout box, sources |  |
| 3 | Content | Content rendering, remember box |  |
| 4 | Content | Elements list, callout |  |
| 5 | Content | Content + remember items |  |

**Oczekiwany wynik:**
- ✅ Badge "HERO" w lewym górnym rogu (Card 1)
- ✅ Stats wyświetlają się jako grid 2x2 (Card 2)
- ✅ Remember/callout boxes mają odpowiednie kolory
- ✅ Wszystkie emoji/ikony wyświetlają się

**Jeśli FAILED:** Zanotuj błąd, przejdź dalej (nie przerywaj)

---

## 🧪 Testy Etap 2: Cards 6-10 (Story + Lightbulb + Practice)

### A. Wstaw SQL

```sql
-- insert_ojt_lesson2_cards_6_10.sql
```

### B. Sprawdź karty

| Card # | Typ | Co sprawdzić | ✅/❌ |
|--------|-----|--------------|-------|
| 6 | **Story** | Bad/Good scenarios rendering, dialogue boxes |  |
| 7 | **Lightbulb** | Comparison table (2 columns), headers red/green |  |
| 8 | Content | Standard content |  |
| 9 | **Practice** | Scenario callout, instruction, 3 inputs (textarea) |  |
| 10 | **Story** | Phases rendering (5 steps), dialogue per phase |  |

**Critical Tests:**

#### Card 6 (Story - Scenarios)
- [ ] Widzisz 2 boxy: "❌ ŹLE" i "✅ DOBRZE"
- [ ] Każdy box ma dialogue (speaker + text)
- [ ] Consequences wyświetlają się jako bullet points
- [ ] Lesson na dole jest czytelny

#### Card 7 (Lightbulb - Comparison)
- [ ] Widzisz tabelę 2-kolumnową
- [ ] Headers: Red background (left) + Green background (right)
- [ ] 4 rows z porównaniem wrong/right
- [ ] Footnote na dole wyświetla się

#### Card 9 (Practice - Inputs)
- [ ] Scenario callout orange z lewym borderem
- [ ] Instruction blue box
- [ ] 3 pola textarea
- [ ] Możesz wpisać tekst (state się zapisuje)
- [ ] Przycisk "Pokaż przykładowe odpowiedzi" działa
- [ ] Collapsible section rozwija się i zawiera 3 sample answers + tip

#### Card 10 (Story - Phases)
- [ ] Widzisz 2 sekcje: "Przed wizytą" + "Demonstracja"
- [ ] Każda sekcja ma dialogue
- [ ] Outcome na dole wyświetla się
- [ ] Lesson na dole wyświetla się

**Jeśli FAILED:** Zanotuj błąd + zrób screenshot

---

## 🧪 Testy Etap 3: Cards 11-15 (Quiz + Practice)

### A. Wstaw SQL

```sql
-- insert_ojt_lesson2_cards_11_15.sql
```

### B. Sprawdź karty

| Card # | Typ | Co sprawdzić | ✅/❌ |
|--------|-----|--------------|-------|
| 11 | Content | Comparison table w content |  |
| 12 | Lightbulb | Steps rendering |  |
| 13 | Quiz | 3 questions, timer, scoring |  |
| 14 | **Practice** | Scenario + 4 inputs (różne typy) |  |
| 15 | Content | Standard content |  |

**Critical Tests:**

#### Card 13 (Quiz)
- [ ] Quiz start screen wyświetla się
- [ ] Możesz wybrać odpowiedź (radio buttons)
- [ ] Po submit widzisz wynik
- [ ] Explanation pokazuje się dla każdego pytania
- [ ] Wynik końcowy (%) wyświetla się

#### Card 14 (Practice - Multiple Inputs)
- [ ] Scenario + instruction wyświetlają się
- [ ] 4 pola input/textarea
- [ ] Sample answers collapsible działa
- [ ] Tip w sample answers ma zielony border

---

## 🧪 Testy Etap 4: Cards 16-20 (Story Phases + Lightbulb Advanced)

### A. Wstaw SQL

```sql
-- insert_ojt_lesson2_cards_16_20.sql
```

### B. Sprawdź karty

| Card # | Typ | Co sprawdzić | ✅/❌ |
|--------|-----|--------------|-------|
| 16 | **Story** | 5-phase story z różnymi type labels |  |
| 17 | **Lightbulb** | Comparison + whenToTell section |  |
| 18 | Quiz | 3 questions |  |
| 19 | Practice | Scenario + 3 textarea inputs |  |
| 20 | Content | Elements list |  |

**Critical Tests:**

#### Card 16 (Story - 5 Phases)
- [ ] Widzisz 5 phase boxes
- [ ] Każdy phase ma title + dialogue
- [ ] Type labels (np. "briefing", "observation") wyświetlają się
- [ ] Outcome box na dole jest widoczny

#### Card 17 (Lightbulb - Comparison + When to Tell)
- [ ] Comparison table 2-column wyświetla się
- [ ] Poniżej: "Kiedy MÓWIĆ..." section z bullet points
- [ ] Highlight box (italic quote) na dole
- [ ] Footnote na samym dole

---

## 🧪 Testy Etap 5: Cards 21-29 (Final Cards + Advanced Features)

### A. Wstaw SQL

```sql
-- insert_ojt_lesson2_cards_21_29.sql
```

### B. Sprawdź karty

| Card # | Typ | Co sprawdzić | ✅/❌ |
|--------|-----|--------------|-------|
| 21 | Data | Stats + callout |  |
| 22 | Story | Phases z dialogiem |  |
| 23 | Quiz | 3 questions |  |
| 24 | **HabitBuilder** | Rich habits (icon + title + description + goal) |  |
| 25 | **Checklist** | Sectioned checklist (3 sekcje) |  |
| 26 | **Lightbulb** | Comparison + Case Study + Quote |  |
| 27 | Test | Test quiz with requirements |  |
| 28 | Achievement | Stats + skills unlocked |  |
| 29 | Ending | Final checklist + CTA |  |

**Critical Tests:**

#### Card 24 (HabitBuilder - Rich Format)
- [ ] Widzisz 4 habit cards
- [ ] Każdy ma: emoji icon + bold title + description + 🎯 goal badge
- [ ] Możesz kliknąć checkbox (zmienia kolor + line-through)
- [ ] Tip box na dole (orange) wyświetla się

#### Card 25 (Checklist - Sections)
- [ ] Widzisz 4 sekcje z nagłówkami
- [ ] Każda sekcja ma mini progress bar
- [ ] Items w każdej sekcji mają checkboxy
- [ ] Główny progress bar (top) agreguje wszystkie sekcje
- [ ] Kliknięcie checkbox aktualizuje progress

#### Card 26 (Lightbulb - Case Study)
- [ ] Comparison table na górze
- [ ] Case study box z:
  - [ ] Company description (italic)
  - [ ] Investment list (orange label)
  - [ ] Results list (green label)
  - [ ] ROI box (highlighted)
- [ ] Quote block z autorem na dole

#### Card 27 (Test)
- [ ] Requirements box wyświetla się przed startem
- [ ] Test działa jak zwykły quiz
- [ ] Timer (jeśli jest) działa
- [ ] Note wyświetla się

#### Card 28 (Achievement)
- [ ] Stats grid wyświetla się
- [ ] Confetti animation (jeśli jest w komponencie)
- [ ] Skills unlocked list (jeśli rozszerzyłeś)
- [ ] Badge name (jeśli rozszerzyłeś)

#### Card 29 (Ending)
- [ ] Checklist items wyświetlają się
- [ ] Tagline/CTA wyświetla się
- [ ] Next steps (jeśli są)

---

## 🧪 Testy Backwards Compatibility

### Cel: Upewnić się, że stare lekcje nie są zepsute

1. Otwórz dowolną **starą lekcję** (np. z category "Investments", "DEGEN", "Personal Development")
2. Przejdź przez wszystkie karty
3. Sprawdź:
   - [ ] Story cards (old format) renderują się poprawnie
   - [ ] Practice cards (bez inputs) renderują się
   - [ ] Lightbulb cards (bez comparison) renderują się
   - [ ] Habit cards (tylko text) renderują się
   - [ ] Checklist (flat items) renderuje się

**Oczekiwany wynik:**
- ✅ ZERO błędów renderowania
- ✅ Wszystkie stare karty wyglądają tak samo jak wcześniej

**Jeśli FAILED:**
- ❌ CRITICAL BUG - backwards compatibility zepsuta
- Sprawdź czy wszystkie stare pola są opcjonalne (`?`)
- Sprawdź czy fallback na stary format działa

---

## 📊 Podsumowanie Testów

### Checklist Końcowy

- [ ] Cards 1-5: Podstawowe karty działają
- [ ] Cards 6-10: Story scenarios + Lightbulb comparison + Practice inputs działają
- [ ] Cards 11-15: Quiz + Practice multiple inputs działają
- [ ] Cards 16-20: Story phases + Lightbulb advanced działają
- [ ] Cards 21-29: All advanced features działają (Habit, Checklist, Case Study)
- [ ] Backwards compatibility: Stare lekcje nie zepsute

### Raport Błędów (Template)

```markdown
## Znalezione Błędy

### Błąd 1: [Tytuł]
- **Card:** #X (Type: X)
- **Problem:** [Opis]
- **Oczekiwane:** [Co powinno być]
- **Screenshot:** [Jeśli możliwe]
- **Priorytet:** 🔴 Critical / 🟡 Medium / 🟢 Low

### Błąd 2: ...
```

---

## 🚀 Po Testach: Merge SQL Files

Jeśli wszystkie testy przeszły:

1. **Połącz 5 SQL plików** w jeden:
   ```sql
   -- insert_ojt_lesson2_COMPLETE.sql
   -- Skopiuj wszystkie cards z 5 plików (1-29)
   -- Sprawdź JSON syntax (przecinki, brackets)
   ```

2. **Final test:**
   ```sql
   DELETE FROM lessons WHERE lesson_id = 'ojt_lesson_2_model';
   -- Run insert_ojt_lesson2_COMPLETE.sql
   ```

3. **Przejdź całą lekcję** od początku do końca (29 kart)

4. **Zapisz wynik XP** - sprawdź czy się nalicza

---

## 🎯 Success Criteria

✅ **SUKCES jeśli:**
- Wszystkie 29 kart renderują się bez błędów
- Interaktywne elementy (inputs, checkboxes) działają
- Backwards compatibility zachowana
- Żadne regressions w starych lekcjach

🔴 **FAILED jeśli:**
- >2 karty mają błędy renderowania
- Stare lekcje są zepsute
- Komponenty crashują aplikację

---

**Dokument stworzony:** Po rozszerzeniu wszystkich 5 komponentów  
**Cel:** Systematyczne przetestowanie OJT Lesson 2 przed production
