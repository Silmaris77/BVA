# FMCG Simulator - Kompletny Pakiet Prezentacyjny

## 📦 ZAWARTOŚĆ PAKIETU

Przygotowane dokumenty dla klienta - gotowe do prezentacji i implementacji.

---

## 1. DOKUMENTY PROJEKTOWE (Design)

### A. **FMCG_GAME_DESIGN.md** (1,296 linii)
- Master design document
- Pełna specyfikacja mechanik gry
- 12 głównych sekcji:
  * Vision & Core Loop
  * MVP Scope
  * Lifecycle klientów (PROSPECT/ACTIVE/LOST)
  * System reputacji (2-tier)
  * Zadania (5 typów)
  * Wizyty handlowe (AI)
  * Kontrakty & produkty
  * Win-back system
  * **Trade Marketing tools (NEW)**
  * **Game balance (NEW)**
  * Prompt engineering
  * Technology stack
  * Timeline 6 tygodni

**Dla kogo:** Development team, Game designer

---

### B. **FMCG_OUTCOMES_SPEC.md** (NEW - szczegółowa specyfikacja)
- Matryca wyników rozmów handlowych:
  * PROSPECT: 5 poziomów oceny AI → specific outcomes
  * ACTIVE: 5 poziomów → rep changes, market share, problem detection
  * LOST: 5 poziomów → win-back progress
- Matryca efektów realizacji zadań:
  * Wizyty regularne (w terminie / spóźnione / pominięte)
  * Operacyjne (kontrola ekspozycji)
  * Sprzedażowe (cross-sell)
  * Awaryjne (reklamacje)
  * Win-back (strategic)
- Interakcje Trade Marketing × Wyniki (5 narzędzi, 3 scenariusze ROI)
- Edge cases (6 sytuacji specjalnych)
- Parametry techniczne:
  * JSON schemas
  * Python probability formulas
  * AI context generation

**Dla kogo:** Backend developers, AI engineers, QA testers

---

### C. **FMCG_REPUTATION_SYSTEM.md** (Technical spec)
- Problem/Solution (why add overall reputation)
- Mechanics (weighted average formula)
- Example calculations (3 ACTIVE + 2 LOST)
- Reputation thresholds (6 levels: Sales Legend to At Risk)
- Gameplay impact (4 areas: prospects, advancement, boss, events)
- UI components (3 widgets)
- Strategic dilemmas (3 scenarios)
- Implementation checklist (18 tasks)
- Success metrics (4 KPIs)

**Dla kogo:** Feature implementation team

---

## 2. DOKUMENTY PREZENTACYJNE (Client-facing)

### D. **FMCG_MVP_SUMMARY.md** (365 linii)
- Condensed version dla klienta
- 6 kluczowych mechanik
- Przykładowy tydzień (Monday flow)
- Wymagania awansu
- Demo scenario (8 minut)
- Technology table
- Implementation checklists (MUST / SHOULD / COULD)
- "Why unique" section

**Dla kogo:** Client presentation, Stakeholders

---

### E. **FMCG_PRESENTATION_SLIDES.md** (Część 1: slajdy 1-12)
**Format:** ASCII art slide deck (gotowy do przekonwertowania na PowerPoint/PDF)

**Zawartość:**
1. Cover Slide (Tytuł, elevator pitch)
2. Problem (Tradycyjny trening = drogi, rzadki, teoretyczny)
3. Rozwiązanie (Gamifikowany simulator)
4. Core Loop (Przykładowy dzień gracza - 30 min)
5. Mapa (Territory Piaseczno, Folium)
6. Klienci (Lifecycle: PROSPECT → ACTIVE → LOST)
7. Reputacja (2-tier system, formula)
8. Zadania (5 typów)
9. Rozmowy AI (Jak wygląda, ocena 1-5⭐)
10. Trade Marketing Tools (5 narzędzi, budżet 2k PLN)
11. Balans energii (Dlaczego 30 min/dzień)
12. Wydarzenia (1-2/dzień, unpredictability)

**Dla kogo:** Client presentation (20-25 minut)

---

### F. **FMCG_PRESENTATION_SLIDES_PART2.md** (Część 2: slajdy 13-20)

**Zawartość:**
13. Przykładowy tydzień gracza (Poniedziałek-Piątek breakdown)
14. Przykładowe wyniki rozmowy AI (Wersja A vs B, feedback)
15. Dashboard (Co widzi gracz - UI overview)
16. Progression (Awans Level 1 → 2 → 3)
17. Technologia (Stack: Streamlit, Gemini, Folium, koszt)
18. Timeline implementacji (6 tygodni, week-by-week plan)
19. Metryki sukcesu (Learning outcomes, Engagement, Business impact, A/B test)
20. Next Steps (Decision → Development → Beta → Launch, Investment 31k PLN)

**+ BACKUP SLIDES (Q&A):**
- B1: Dlaczego nie gotowe platformy? (Trailhead comparison)
- B2: Prywatność danych (GDPR compliance)
- B3: Czy zastąpi tradycyjne szkolenia? (Hybrid model)

**Dla kogo:** Client presentation (kontynuacja)

---

## 3. WIZUALIZACJE UI (Mockups)

### G. **FMCG_UI_MOCKUPS_PART1.md** (Ekrany 1-5)

**Szczegółowe ASCII art mockups:**
1. **DASHBOARD** (Główny ekran)
   - Level progress bar
   - Reputation timeline (wykres)
   - Zadania (4 aktywne z priorytetami)
   - Mapa territory (interactive Folium)
   - Quick stats (PLN, energia, finanse)

2. **CLIENT CARD** (Szczegóły klienta)
   - Podstawowe info (typ, lokalizacja, dystans)
   - Portfolio produktów (listing, market share)
   - Reputation widget (trend 30d)
   - Timeline (ostatnie 5 eventów)
   - Quick actions (wizyta, email, raport)

3. **AI CONVERSATION SCREEN** (Wizyta)
   - Chat interface (AI vs gracz)
   - Kontekst wizyty (cel, produkty, historia)
   - Live scoring (profesjonalizm, dopasowanie, słuchanie)
   - Trade Marketing tools panel (quick access)
   - AI hints (💡 podpowiedzi kontekstowe)

4. **VISIT RESULTS SCREEN** (Po rozmowie)
   - Rating (⭐⭐⭐⭐⭐)
   - AI feedback (co poszło dobrze / co poprawić)
   - Nagrody (PLN, reputation, market share)
   - Wpływ na overall reputation (wykres animowany)
   - Nowe zadania wygenerowane

5. **TRADE MARKETING PANEL**
   - Budżet (progress bar: 1,400/2,000 PLN)
   - 5 narzędzi (opis, koszt, ROI, cooldown)
   - Historia użyć (ostatnie 30 dni)
   - Analytics (avg ROI, najlepsze/najsłabsze)

**Dla kogo:** UI/UX designer, Frontend developer

---

### H. **FMCG_UI_MOCKUPS_PART2.md** (Ekrany 6-10)

**Zawartość:**
6. **CALENDAR VIEW** (Planowanie tygodnia)
   - Tygodniowy widok (Pon-Niedz)
   - Zadania z kolorami (priorytet)
   - Energia tracking (per dzień)
   - Smart suggestions (AI balancing)

7. **CLIENT LIST VIEW** (Przegląd klientów)
   - Filtry (ACTIVE/PROSPECT/LOST)
   - Sortowanie (PLN, reputation, dystans)
   - Quick info cards
   - Alerts (OVERDUE, market share drops)

8. **WEEKLY REPORT** (Podsumowanie)
   - Key metrics (sprzedaż, reputation, completion rate)
   - Wykres reputacji (4 tygodnie)
   - Top performers (klienci)
   - Areas for improvement
   - Rekomendacje AI
   - Email od szefa (feedback)

9. **LEVEL UP SCREEN** (Awans)
   - Achievements (checklisty ✅)
   - Co się zmienia (territory, budget, mechaniki)
   - Nagrody (badge, bonus, unlocks)
   - Email gratulacyjny
   - Cel Level 2 (następny milestone)

10. **TUTORIAL / ONBOARDING** (First-time user)
    - 8-step guided tour
    - Intro (cele, czas)
    - Mapa (territory)
    - Energia (balance)
    - **Praktyczna wizyta** (guided first visit)
    - Tips & tricks

**Dla kogo:** UI/UX designer, Frontend developer

---

## 4. PLAYER JOURNEY DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FMCG SIMULATOR - PLAYER JOURNEY                      │
│                         (Start → Level 2)                               │
└─────────────────────────────────────────────────────────────────────────┘

DAY 1-2: ONBOARDING
├─ Tutorial (8 kroków, 15 min)
├─ Pierwsza wizyta (PROSPECT guided - Sklep ABC)
│  └─ Wynik: 4⭐ → "Zainteresowany, wymaga 2. wizyty"
├─ Dashboard tour (gdzie co jest)
└─ Cel: Zrozumieć podstawowe mechaniki

      ↓

DAY 3-7: TYDZIEŃ 1 - LEARNING BASICS
├─ 2. wizyta Sklep ABC → 5⭐ → KONTRAKT! 🎉 (+1,200 PLN/m)
├─ Cold call: Dino Konstancin (PROSPECT) → 4⭐ → "Rozważa"
├─ 2 wizyty regularne (nowi klienci ACTIVE)
├─ 1 zadanie operacyjne (kontrola ekspozycji)
├─ Event: Telefon od klienta (neutral, flavor)
└─ Wyniki tygodnia:
   • Sprzedaż: 3,500 PLN/m (z 5 klientów)
   • Reputation: 45 → 52 (+7)
   • Avg rating: 3.8⭐
   • Czas gry: ~35 min/dzień (uczenie się interfejsu)

      ↓

DAY 8-14: TYDZIEŃ 2 - BUILDING MOMENTUM
├─ Dino: 2. wizyta → 5⭐ → KONTRAKT (+2,500 PLN/m)
├─ Cross-sell sukces: Sklep ABC → FreshShampoo (+400 PLN/m)
├─ Trade Marketing: Użycie POS (200 PLN) dla Dino
├─ Event: Rekomendacja! Nowy PROSPECT (Żabka) z high interest
├─ Pierwsze wyzwanie: Reklamacja (PILNE) → Rozwiązane 5⭐ (+10 rep bonus)
└─ Wyniki tygodnia:
   • Sprzedaż: 6,600 PLN/m (+3,100)
   • Reputation: 52 → 56 (+4)
   • Avg rating: 4.0⭐ ✅ TARGET!
   • Czas gry: ~30 min/dzień (efficiency improved)

      ↓

DAY 15-21: TYDZIEŃ 3 - ADVANCED TACTICS
├─ Żabka: Cold call z Gratis (350 PLN) → 5⭐ → KONTRAKT (+800 PLN/m)
├─ 2× Cross-sell attempts (1 sukces, 1 odmowa)
├─ Event: Awaria samochodu (-1 wizyta, learning to adapt)
├─ Kaufland (duży klient): Cold call → 3⭐ → "Wątpliwości"
│  └─ 2. próba z POS + Gratis → 4⭐ → "Rozważa"
├─ Problem: Sklep XYZ market share drop → Zadanie ekspozycji
└─ Wyniki tygodnia:
   • Sprzedaż: 9,100 PLN/m (+2,500)
   • Reputation: 56 → 59 (+3, blisko Solid Rep!)
   • Avg rating: 4.1⭐
   • Strategic thinking: Balancing budget TM (1,600/2,000 used)

      ↓

DAY 22-28: TYDZIEŃ 4 - FINAL PUSH
├─ Kaufland: 3. wizyta z WSZYSTKIMI narzędziami
│  └─ Gratis + POS + Darmowa dostawa (700 PLN) → 5⭐ → KONTRAKT! 🎉
│  └─ +5,000 PLN/m (BIGGEST CLIENT!)
├─ Overall reputation: 59 → 62 (Solid Rep!) ✅
│  └─ Unlock: "SOLID REPUTATION" achievement
│  └─ Feedback od szefa: "Gratulacje, możesz awansować!"
├─ Sprzedaż total: 10,200 PLN/m ✅ (target: 10,000)
├─ Kontrakty: 12 aktywne ✅ (target: 10)
├─ Avg rating: 4.1⭐ ✅ (target: 4.0)
└─ Wyniki miesiąca:
   • 52 wizyty total (avg 13/tydzień)
   • Success rate: 78% (very good!)
   • Trade Marketing ROI: 2,300% (świetne decyzje!)
   • Czas gry: 28 dni × 30 min = 14h total

      ↓

DAY 29: LEVEL UP! 🎊
├─ Awans: Junior → Mid Salesperson
├─ Nagrody:
│  ├─ Badge: "MID SALESPERSON"
│  ├─ Bonus: +500 PLN (budget TM)
│  ├─ Nowy samochód (-5% energia)
│  ├─ Unlock: Advanced reports
│  └─ Territory expansion (+10 klientów)
├─ Nowe wyzwania:
│  ├─ Sieci handlowe (Tesco, Carrefour)
│  ├─ Konkurencja aktywna
│  ├─ Seasonal trends
│  └─ Targety kwartalne (25k PLN/m)
└─ Email od szefa: "Świetna robota, teraz prawdziwe wyzwania!"

      ↓

LEVEL 2: MID SALESPERSON (8 tygodni)
├─ Territory: 25 klientów (was: 15)
├─ Portfolio: 12 produktów (was: 6)
├─ Budget TM: 3,500 PLN/m (was: 2,000)
├─ Target: 25,000 PLN/m sprzedaży
└─ Nowe mechaniki:
   ├─ Key Account Management
   ├─ Competitor tracking
   ├─ Seasonal events (targi)
   └─ Team collaboration (future: zarządzanie juniorami)

      ↓

[LEVEL 3: SENIOR - Future expansion]
```

---

## 5. KLUCZOWE INSIGHTS DLA KLIENTA

### 💡 DLACZEGO TO DZIAŁA?

**1. Engagement = Mobile Game Model**
- 30 min/dzień (jak Candy Crush)
- Daily rhythm (morning routine)
- Clear goals (Level up progress bar)
- **Result:** 70% DAU (Daily Active Users) możliwe

**2. Learning = Safe Practice Space**
- AI feedback natychmiastowy
- Błąd NIE = utracony klient
- Repetition bez konsekwencji
- **Result:** 4 tygodnie gry = 14h treningu (vs 16h rocznie tradycyjnie)

**3. Motivation = Gamification**
- Achievements (badges)
- Leaderboards (future: compare with peers)
- Progression (Level 1 → 2 → 3)
- **Result:** 60% retention (30 dni) - benchmark Duolingo 55%

**4. Realism = Transfer do prawdziwej pracy**
- AI conversations (soft skills)
- Territory management (planning)
- Budget constraints (trade-offs)
- **Result:** Junior do 1. kontraktu: 60 dni (was: 90-120)

**5. Mierzalność = ROI Proof**
- Every action tracked
- Progress visible real-time
- A/B testing możliwe
- **Result:** ROI 720% Year 1 (31k investment → 225k savings)

---

## 6. IMPLEMENTATION ROADMAP

```
WEEK 1-2: CORE
├─ Data structures (clients, tasks, user state)
├─ Folium map (15 fake clients, Piaseczno)
├─ Calendar UI (Streamlit)
└─ Deliverable: Interactive map + calendar

WEEK 3-4: AI & GAME LOOP
├─ Gemini API integration
├─ Prompt engineering (3 scenarios: PROSPECT/ACTIVE/LOST)
├─ Conversation outcomes (matryca z FMCG_OUTCOMES_SPEC.md)
├─ Reputation calculations (2-tier system)
└─ Deliverable: Working AI chat + full game loop

WEEK 5: TRADE MARKETING & EVENTS
├─ 5 narzędzi TM (budget, cooldowns, ROI tracking)
├─ Event system (1-2/day, % distribution)
├─ Energy system (100% daily, visit costs)
└─ Deliverable: Strategic depth added

WEEK 6: POLISH & TESTING
├─ Dashboard UI (charts: Plotly)
├─ Tutorial (8-step onboarding)
├─ Balance tuning (probabilities testing)
├─ Bug fixing
└─ Deliverable: MVP ready for beta

WEEK 7-12: BETA TESTING
├─ 10-20 handlowców (mix junior/mid)
├─ Weekly feedback sessions
├─ Iteracja mechanik (balance tweaks)
└─ Content expansion (więcej klientów, produktów)

WEEK 13+: LAUNCH
└─ Rollout do całego zespołu
```

---

## 7. PYTANIA DO KLIENTA (Przygotuj odpowiedzi)

**Strategiczne:**
1. Ile handlowców obecnie w zespole? (określi skalę)
2. Jaki jest avg czas onboardingu juniora? (benchmark przed/po)
3. Czy macie CRM? (integracja możliwa)
4. Jaki budżet na training obecnie? (pokazać savings)

**Techniczne:**
5. Czy można użyć prawdziwych nazw produktów? (lub fake names)
6. Czy można użyć prawdziwego territory? (lub synthetic data)
7. Kto będzie product ownerem? (feedback loop ważny)

**Organizacyjne:**
8. Beta testerzy - kto? (mix junior/mid dla balanced feedback)
9. Success metrics - jak mierzymy? (CRM data access?)
10. Timeline - kiedy chcecie launch? (Q1? Q2?)

---

## 8. NEXT STEPS (Po Prezentacji)

**IMMEDIATE (Tydzień 1-2):**
- [ ] Prezentacja stakeholderom
- [ ] Q&A session (2h, deep dive)
- [ ] Budget approval (31,200 PLN)
- [ ] Wybór beta testerów (10-20 osób)
- [ ] Kickoff meeting (dev team)

**SHORT-TERM (Tydzień 3-8):**
- [ ] Development (6 tygodni)
- [ ] Weekly demos (pokazuj progress)
- [ ] Beta recruitment (onboarding materials)

**MID-TERM (Tydzień 9-14):**
- [ ] Beta testing (6 tygodni)
- [ ] Feedback collection (weekly surveys)
- [ ] Iteracja (balance, content)

**LONG-TERM (Tydzień 15+):**
- [ ] Launch (rollout plan)
- [ ] Monitoring (dashboards, analytics)
- [ ] Continuous improvement (content updates)
- [ ] Expansion (Level 3, multiplayer?, VR?)

---

## 9. PLIKI DO PRZESŁANIA KLIENTOWI

**Package zawiera:**
1. ✅ FMCG_PRESENTATION_SLIDES.md (Część 1)
2. ✅ FMCG_PRESENTATION_SLIDES_PART2.md (Część 2)
3. ✅ FMCG_MVP_SUMMARY.md (Executive summary)
4. ✅ FMCG_GAME_DESIGN.md (Full design doc)
5. ✅ FMCG_OUTCOMES_SPEC.md (Technical spec)
6. ✅ FMCG_REPUTATION_SYSTEM.md (Feature spec)
7. ✅ FMCG_UI_MOCKUPS_PART1.md (Screens 1-5)
8. ✅ FMCG_UI_MOCKUPS_PART2.md (Screens 6-10)
9. ✅ FMCG_PRESENTATION_PACKAGE_SUMMARY.md (Ten plik)

**Format:** Markdown (łatwo przekonwertować na PDF/PowerPoint)

**Konwersja na PowerPoint:**
```powershell
# Użyj Pandoc (jeśli zainstalowany)
pandoc FMCG_PRESENTATION_SLIDES.md -o FMCG_Presentation.pptx
pandoc FMCG_MVP_SUMMARY.md -o FMCG_Executive_Summary.pdf
```

Lub skopiuj ASCII art do slajdów ręcznie (zachowaj monospace font: Courier New)

---

## 10. CONTACT & SUPPORT

**Pytania? Uwagi? Potrzebujesz zmian?**

📧 Email: [TWÓJ EMAIL]  
📞 Phone: [TWÓJ TELEFON]  
🌐 Demo: [LINK DO PROTOTYPU - jeśli istnieje]  
💬 Slack: [KANAŁ - jeśli istnieje]

**Dostępność:**
- Pon-Pt: 9:00-17:00
- Response time: <24h

---

**GOTOWE DO PREZENTACJI! 🎉**

Powodzenia w przekonaniu klienta! 🚀
