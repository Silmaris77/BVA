# Milwaukee Lesson 1 Discovery - Testing Checklist

## 🧪 Pre-Launch Testing Guide

### File Location
`c:\Users\pksia\Dropbox\BVA\v3_mockups\Milwaukee Lesson 1 Discovery\lesson1_discovery.html`

**Open in browser**: Double-click the file or drag into Chrome/Firefox/Edge

---

## ✅ Basic Functionality Tests

### Navigation
- [ ] Page loads without errors (check browser console: F12)
- [ ] Progress bar displays "Karta 0 z 10" and "⭐ 0 XP"
- [ ] Card 1 is visible on load
- [ ] "← Poprzednia" button is disabled on Card 1
- [ ] "Następna →" button navigates to Card 2
- [ ] Arrow keys work (← goes back, → goes forward)
- [ ] Progress bar updates as you navigate
- [ ] XP badge updates as you earn XP

### Card 1: Video (5 XP)
- [ ] YouTube embed loads (placeholder video)
- [ ] Checkbox: "Obejrzałem całe video"
- [ ] Checking checkbox shows success message
- [ ] XP increases to 5
- [ ] Reflection textarea auto-saves (type, refresh page, check if text persists)
- [ ] Can navigate to Card 2

### Card 2: Profile Table (0 XP)
- [ ] 3-column table displays correctly
- [ ] All 6 rows visible (KPI, Bolączki, Decydenci, etc.)
- [ ] Tooltips show on hover (LTIFR, OEE, ATEX)
- [ ] No XP awarded (presentation only)
- [ ] Can navigate forward/back

### Card 3: SWOT Interactive (10 XP)
- [ ] Dropdown shows 3 options: Mahle, KGHM, Custom
- [ ] Selecting "Mahle" fills all 4 textareas with example
- [ ] Selecting "KGHM" fills with different example
- [ ] Selecting "Custom" clears all fields
- [ ] Typing in textareas auto-saves (check localStorage)
- [ ] "Wyczyść" button asks for confirmation, then clears
- [ ] Validation works:
  - [ ] Try saving with <3 points in one field → error message
  - [ ] Fill all 4 fields with ≥3 points each → success
- [ ] +10 XP awarded on first save
- [ ] Can't earn XP again on second save (check XP stays at 15)

### Card 4: Stakeholder Matrix (15 XP)
- [ ] Table has 8 default rows
- [ ] Dropdowns work: Wpływ (1-3), Postawa (-2 to +2)
- [ ] Zone auto-calculates based on influence + attitude:
  - [ ] Wpływ 3, Postawa +2 → "Ambasador"
  - [ ] Wpływ 1, Postawa -2 → "Przeciwnik niskiego wpływu"
- [ ] "Akcja" column auto-generates strategy
- [ ] 2D Visual Matrix updates live:
  - [ ] Counters show number in each zone
  - [ ] 3×3 grid displays correctly
- [ ] "Dodaj osobę ➕" button adds new row
- [ ] Validation: Try saving with <5 people → error
- [ ] Fill ≥5 people → +15 XP (total now 30)
- [ ] Auto-saves to localStorage

### Card 5: Bob Case Study (10 XP)
- [ ] Timeline shows all 7 months (M1-M7)
- [ ] 3 reflection textareas present
- [ ] Character counter shows "0/50" initially
- [ ] Type <50 chars → counter stays orange
- [ ] Type ≥50 chars → counter turns green "✅ 52 znaków"
- [ ] Auto-saves as you type
- [ ] Validation: Try saving with <50 chars in one field → error
- [ ] Fill all 3 with ≥50 chars → +10 XP (total now 40)

### Card 6: Quiz (15 XP)
- [ ] 10 questions display
- [ ] Each question has 4 options (A/B/C/D)
- [ ] Click option → background changes (green = correct, red = incorrect)
- [ ] Feedback text shows below option
- [ ] Options disable after selection (can't change answer)
- [ ] After 10 answers → score panel appears
- [ ] Score shows as "X/10"
- [ ] Interpretation message shows based on score
- [ ] +15 XP awarded (total now 55)
- [ ] "Następna →" button appears after scoring

### Card 7: Flashcards (20 XP)
- [ ] 8 flashcards display in grid
- [ ] Click card → 3D flip animation
- [ ] Front shows: Icon + Title + Wpływ/Focus
- [ ] Back shows: 5 fields (Język, Bolączka, Argument, Obiekcja, Counter)
- [ ] Progress tracker shows "Poznane karty: 0/8"
- [ ] Click 1 card → "1/8"
- [ ] Click all 8 → "8/8" + +20 XP (total now 75)
- [ ] "Znam wszystkie" button flips all cards
- [ ] "Przejrzyj ponownie" button unflips all + resets counter
- [ ] Auto-saves progress

### Card 8: Template (10 XP)
- [ ] "Pobierz Template Excel" button shows
- [ ] Click button → alert (mockup message)
- [ ] Checkbox: "Użyję szablonu w ciągu 7 dni"
- [ ] Check checkbox → success message + +10 XP (total now 85)
- [ ] Auto-saves checkbox state

### Card 9: AI Interview (15 XP)
- [ ] 3 conversation rounds display
- [ ] Bob's messages show with yellow border
- [ ] 3 textareas for user responses (round1, round2, round3)
- [ ] Character hints show "Min. 80 znaków (0/80)"
- [ ] Type text → hint updates "X/80" (orange if <80, green if ≥80)
- [ ] Auto-saves responses as you type
- [ ] Try clicking "Oceń" with <80 chars → alert error
- [ ] Fill all 3 with ≥80 chars, click "Oceń moją rozmowę"
- [ ] Score panel appears with:
  - [ ] Score number (0-100)
  - [ ] Mood indicator (emoji + text)
  - [ ] 3 feedback paragraphs (one per round)
- [ ] Test scoring keywords:
  - [ ] Round 1: Include "ergonomia", "pytanie", "potrzeby" → higher score
  - [ ] Round 2: Include "ROI", "case study", "dowód" → higher score
  - [ ] Round 3: Include "PoC", "pilot", "demo" → higher score
- [ ] Score ≥60 → +15 XP (total now 100)
- [ ] Score <60 → no XP
- [ ] Mood changes based on score:
  - [ ] ≥80 → 😍 "Bob jest pod wrażeniem!"
  - [ ] 60-79 → 😊 "Bob jest zainteresowany"
  - [ ] 40-59 → 😐 "Bob jest sceptyczny"
  - [ ] <40 → 😕 "Bob jest rozczarowany"

### Card 10: Summary & Badge (10 XP)
- [ ] "Gratulacje!" header shows
- [ ] 7 learning checklist items display with icons
- [ ] Stats grid shows 3 boxes:
  - [ ] "XP zdobyte" shows current XP (e.g., 100)
  - [ ] "Karty ukończone" shows 10/10
  - [ ] "Czas nauki" shows ~60 min
- [ ] "Przejdź do Lekcji 2" button is disabled
- [ ] "Pokaż mój badge!" button shows
- [ ] Click badge button → popup overlay appears:
  - [ ] 🔍 icon
  - [ ] "Discovery Expert" title
  - [ ] "Milwaukee B2B Academy" subtitle
  - [ ] Stats: XP + Cards
  - [ ] Congratulations message
  - [ ] "Zamknij 🎉" button
- [ ] +10 XP awarded on first badge show (total now 110)
- [ ] Click "Zamknij" → overlay closes
- [ ] Click "Pokaż mój badge!" again → can reopen (no extra XP)

---

## 📱 Mobile Responsive Tests

### Test on different screen sizes:
1. **Desktop** (1920×1080):
   - [ ] All cards display full-width
   - [ ] Stakeholder table has enough space
   - [ ] Flashcards show 2 columns
   - [ ] Stats grid shows 3 columns

2. **Tablet** (768px):
   - [ ] Font sizes scale down
   - [ ] Tables remain readable
   - [ ] Flashcards show 1 column
   - [ ] Stats grid shows 1 column

3. **Mobile** (375px - iPhone SE):
   - [ ] All content fits without horizontal scroll
   - [ ] Buttons are touch-friendly
   - [ ] Textareas are easy to type in
   - [ ] Badge popup scales correctly

**Test method**: Open browser DevTools (F12) → Toggle device toolbar → Select different devices

---

## 💾 LocalStorage Persistence Tests

### Test auto-save:
1. [ ] Fill Card 3 SWOT with data
2. [ ] Navigate to Card 5, fill reflections
3. [ ] Close browser tab completely
4. [ ] Reopen `lesson1_discovery.html`
5. [ ] Navigate to Card 3 → SWOT data still there?
6. [ ] Navigate to Card 5 → Reflections still there?
7. [ ] Check XP badge → XP persists?
8. [ ] Check progress bar → Shows correct card position?

### Test localStorage keys (F12 → Application → Local Storage):
- [ ] `lessonProgress` = JSON with currentCard, earnedXP, completedCards
- [ ] `swot_strengths` = SWOT S field
- [ ] `swot_weaknesses` = SWOT W field
- [ ] `swot_opportunities` = SWOT O field
- [ ] `swot_threats` = SWOT T field
- [ ] `stakeholderData` = JSON array
- [ ] `bobReflections` = JSON object with q1, q2, q3
- [ ] `aiResponses` = JSON with round1, round2, round3
- [ ] `templateCommitment` = "true"/"false"

---

## 🐛 Known Issues to Watch For

### Potential bugs (based on C-IQ lesson fix):
- [ ] Quiz button doesn't change to "Następna →" after scoring
  - **Fix**: Check `showQuizScore()` function updates button text
- [ ] XP awarded multiple times for same card
  - **Fix**: Check `completedCards.has(cardNumber)` before adding XP
- [ ] Progress bar doesn't reach 100% on Card 10
  - **Fix**: Verify calculation includes Card 10
- [ ] Badge popup doesn't center on small screens
  - **Fix**: Check `.badge-overlay` CSS has `justify-content: center`

### Browser compatibility:
- [ ] Chrome (recommended)
- [ ] Firefox
- [ ] Edge
- [ ] Safari (if available)

### Console errors:
- [ ] Open F12 → Console tab
- [ ] Navigate through all 10 cards
- [ ] Check for red error messages
- [ ] Common issues:
  - `Cannot read property 'value' of null` → element ID mismatch
  - `localStorage is not defined` → browser privacy mode
  - CSS not loading → file path issue

---

## 🎯 Success Criteria

✅ **Ready for demo if:**
- All 10 cards load without errors
- Navigation works (prev/next + arrows)
- XP system awards correctly (no duplicates)
- LocalStorage persists all data
- AI Interview scoring works with keywords
- Badge popup displays with correct XP
- Mobile responsive (no horizontal scroll on 375px)
- No console errors

---

## 📊 Final XP Breakdown

| Card | Activity | XP |
|------|----------|-----|
| 1 | Video watched | 5 |
| 2 | Profile table | 0 |
| 3 | SWOT saved | 10 |
| 4 | Stakeholder map | 15 |
| 5 | Bob reflections | 10 |
| 6 | Quiz completed | 15 |
| 7 | All flashcards viewed | 20 |
| 8 | Template commitment | 10 |
| 9 | AI Interview ≥60 | 15 |
| 10 | Completion bonus | 10 |
| **TOTAL** | | **110 XP** |

---

## 🚀 Post-Testing Actions

After testing, document:
1. **Bugs found**: List with steps to reproduce
2. **UX issues**: Confusing interactions, unclear instructions
3. **Performance**: Slow sections, lag on interactions
4. **Suggestions**: Improvements for final BVA integration

**Test completed by**: _________________  
**Date**: _________________  
**Browser**: _________________  
**Result**: ☐ Pass ☐ Fail (with notes)
