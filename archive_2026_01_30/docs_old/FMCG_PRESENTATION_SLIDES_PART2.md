# FMCG Sales Simulator - Prezentacja CZĘŚĆ 2

## SLAJD 13: PRZYKŁADOWY TYDZIEŃ GRACZA

```
┌─────────────────────────────────────────────────┐
│  📅 TYDZIEŃ W SYMULATORZE                       │
│                                                 │
│  PONIEDZIAŁEK (Gentle Start)                   │
│  9:00  🏪 Sklep ABC - wizyta regularna (4⭐)   │
│  14:00 📦 Kontrola ekspozycji - Dino           │
│  Wynik: +10 PLN/m, +8 rep                      │
│  Czas: 25 min                                   │
│                                                 │
│  WTOREK (Momentum)                             │
│  9:00  🎯 PROSPECT - Żabka Konstancin (cold)   │
│  12:00 📞 Event: Telefon od Kaufland           │
│  14:00 🏪 Dino - cross-sell FreshDish (5⭐)    │
│  Wynik: +400 PLN/m, +20 rep, używam POS (200)  │
│  Czas: 35 min                                   │
│                                                 │
│  ŚRODA (Challenge)                             │
│  9:00  🚨 PILNE: Reklamacja - Sklep ABC        │
│  11:00 Rozwiązanie (5⭐) → +10 rep bonus!      │
│  15:00 🔄 Win-back - Kaufland (LOST)           │
│  Wynik: ABC repair, Kaufland 🤔 (wymaga 2. try)│
│  Czas: 40 min                                   │
│                                                 │
│  CZWARTEK (Routine)                            │
│  9:00  🏪 Żabka - follow-up cold call (4⭐)    │
│  14:00 🏪 Sklep XYZ - regularna                │
│  Wynik: Żabka zainteresowana, +5 rep (XYZ)     │
│  Czas: 30 min                                   │
│                                                 │
│  PIĄTEK (Closing)                              │
│  9:00  🎯 Żabka - KONTRAKT! 🎉 (ACTIVE)        │
│  14:00 📊 Raport tygodniowy                    │
│  Wynik: +1,200 PLN/m nowy kontrakt             │
│  Czas: 20 min                                   │
│                                                 │
│  ───────────────────────────────────────────   │
│  PODSUMOWANIE TYGODNIA:                        │
│  • 12 wizyt / 5 dni                            │
│  • +1,610 PLN/m (1 nowy + 1 cross-sell)        │
│  • Overall reputation: 52 → 58 (+6)            │
│  • Total czas: 2h 30min (~30 min/dzień)       │
└─────────────────────────────────────────────────┘
```

**Insight:**  
Tydzień gry = tydzień pracy (realistyczny timing)  
Ale bez ryzyka prawdziwych klientów!

---

## SLAJD 14: PRZYKŁADOWE WYNIKI ROZMOWY AI

```
┌─────────────────────────────────────────────────┐
│  💬 PRZYKŁAD: COLD CALL (PROSPECT)              │
│                                                 │
│  SCENARIUSZ:                                   │
│  Gracz: Junior handlowiec (Level 1)           │
│  Klient: Sklep ABC (Prospect, interest=60)     │
│  Cel: Podpisać kontrakt na FreshSoap           │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  WERSJA A - SŁABA ROZMOWA (2⭐)                │
│  ────────────────────────────────────────────  │
│  Gracz: "Dzień dobry, mam świetną ofertę!"    │
│  AI: "Nie mam czasu, zajęty jestem"           │
│  Gracz: "Ale naprawdę warto, super ceny!"     │
│  AI: "Mam już dostawcę, dziękuję"             │
│                                                 │
│  WYNIK: 🚫 Odmowa (visits_count = 1)           │
│  FEEDBACK:                                     │
│  ❌ "Zbyt agresywna sprzedaż"                  │
│  ❌ "Nie zapytałeś o potrzeby klienta"         │
│  💡 "Spróbuj zacząć od pytania otwartego"      │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  WERSJA B - DOBRA ROZMOWA (5⭐)                │
│  ────────────────────────────────────────────  │
│  Gracz: "Dzień dobry, widzę że sklep dobrze   │
│          prosperuje. Jakie produkty są u Was  │
│          najlepiej sprzedawane?"               │
│  AI: "Przede wszystkim kosmetyki, ale miejsce │
│       jest ograniczone"                        │
│  Gracz: "Rozumiem. Mamy FreshSoap - kompaktowy│
│          produkt, który nie zajmuje dużo       │
│          miejsca. Mogę zostawić próbkę?"       │
│  AI: "Dobra, chętnie zobaczę"                 │
│                                                 │
│  WYNIK: ✅ KONTRAKT PODPISANY! 🎉              │
│  FEEDBACK:                                     │
│  ✅ "Świetne rozpoznanie potrzeby (miejsce)"   │
│  ✅ "Delikatne podejście, nie presja"          │
│  ✅ "Próbka = smart move"                      │
└─────────────────────────────────────────────────┘
```

**Learning:**  
AI uczy **soft skills** (słuchanie, empatia, dopasowanie)  
nie tylko product knowledge!

---

## SLAJD 15: DASHBOARD - Co widzi gracz?

```
┌─────────────────────────────────────────────────┐
│  📊 GAME DASHBOARD                              │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ 👤 GRACZ: Jan Kowalski (Level 1)         │ │
│  │                                           │ │
│  │ POSTĘP DO LEVEL 2:                        │ │
│  │ ████████████░░░░░░░░ 65%                  │ │
│  │                                           │ │
│  │ ✅ Sprzedaż: 8,500 / 10,000 PLN ✅        │ │
│  │ ✅ Kontrakty: 12 / 10 ✅                  │ │
│  │ ⚠️ Rating: 3.8 / 4.0 (0.2 do celu)       │ │
│  │ ⚠️ Reputation: 58 / 60 (2 pkt do celu)   │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ 💰 FINANSE                                │ │
│  │ ├─ Miesięczna sprzedaż: 8,500 PLN        │ │
│  │ ├─ Trade Marketing: 1,200 / 2,000 PLN    │ │
│  │ └─ Trend: +15% vs poprzedni tydzień 📈   │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ ⭐ REPUTACJA                              │ │
│  │                                           │ │
│  │ Ogólna: 58/100 (Average ⚠️)              │ │
│  │ ████████████░░░░░░░░                      │ │
│  │                                           │ │
│  │ Timeline (ostatnie 7 dni):               │ │
│  │   52 ━━ 54 ━━ 56 ━━ 58 📈               │ │
│  │                                           │ │
│  │ Top klienci (reputation):                │ │
│  │ 🥇 Dino: 85/100 (Top Performer)          │ │
│  │ 🥈 Sklep ABC: 70/100 (Happy)             │ │
│  │ 🥉 Żabka: 50/100 (Neutral - NEW)         │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ 📅 ZADANIA (dzisiaj)                      │ │
│  │                                           │ │
│  │ 🔴 PILNE: Reklamacja - Kaufland (3h)     │ │
│  │ 🟡 Wizyta regularna - Dino (dziś)        │ │
│  │ 🟢 Cross-sell - Sklep XYZ (7 dni)        │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │ 🗺️ MAPA (15 klientów w territory)        │ │
│  │                                           │ │
│  │     [Mini-map z pinami]                  │ │
│  │                                           │ │
│  │ 🟢 ACTIVE: 8    🔴 LOST: 2              │ │
│  │ 🔵 PROSPECT: 5                            │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

**UI Philosophy:**  
Game-like = motivating  
Dashboard = sales CRM + RPG stats

---

## SLAJD 16: PROGRESSION - Awans Level 1 → 2

```
┌─────────────────────────────────────────────────┐
│  🎯 AWANS: JUNIOR → MID SALESPERSON             │
│                                                 │
│  WYMAGANIA (Level 2):                          │
│  ────────────────────────────────────────────  │
│  ✅ Sprzedaż miesięczna: ≥ 10,000 PLN         │
│  ✅ Kontrakty aktywne: ≥ 10                    │
│  ✅ Średnia ocena wizyt: ≥ 4.0⭐               │
│  ✅ Reputacja ogólna: ≥ 60/100                │
│                                                 │
│  Czas: ~4 tygodnie (MVP)                       │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  CO SIĘ ZMIENIA NA LEVEL 2?                    │
│  ────────────────────────────────────────────  │
│                                                 │
│  📈 Większe możliwości:                        │
│  • Territory: 15 → 25 klientów                │
│  • Portfolio: 6 → 12 produktów                │
│  • Budget TM: 2,000 → 3,500 PLN/m             │
│                                                 │
│  🎯 Trudniejsze wyzwania:                      │
│  • Sieci handlowe (Kaufland, Tesco)           │
│  • Konkurencja aktywna (Palmolive walczy!)    │
│  • Seasonal trends (lato/zima)                │
│                                                 │
│  💡 Nowe mechaniki:                            │
│  • Zespół (zarządzanie juniorami)             │
│  • Targety regionalne (KPI szefa)             │
│  • Eventy branżowe (targi, konferencje)       │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  ROADMAP (3 poziomy):                          │
│                                                 │
│  Level 1: JUNIOR (4 tygodnie)                 │
│    ├─ Piaseczno (15 klientów)                 │
│    └─ Podstawowe narzędzia                     │
│         ↓                                      │
│  Level 2: MID (8 tygodni)                     │
│    ├─ Region (25 klientów)                    │
│    ├─ Konkurencja                              │
│    └─ Seasonal trends                          │
│         ↓                                      │
│  Level 3: SENIOR (12 tygodni)                 │
│    ├─ Multi-region (50 klientów)              │
│    ├─ Team management (3 juniorów)            │
│    └─ Strategic planning                       │
└─────────────────────────────────────────────────┘
```

**Progression = Retention!**  
Gracz widzi path do mastery (nie tylko "ukończone")

---

## SLAJD 17: TECHNOLOGIA - Stack

```
┌─────────────────────────────────────────────────┐
│  🔧 TECHNOLOGY STACK                            │
│                                                 │
│  FRONTEND:                                     │
│  ────────────────────────────────────────────  │
│  🐍 Streamlit (Python web framework)           │
│    • Szybki development                        │
│    • Natywna integracja z Python               │
│    • Built-in widgets (sliders, charts)        │
│                                                 │
│  📊 Plotly (Interactive charts)                │
│    • Reputation timeline (line chart)          │
│    • Portfolio breakdown (pie chart)           │
│    • Market share evolution (area chart)       │
│                                                 │
│  🗺️ Folium (Maps)                              │
│    • OpenStreetMap integration                 │
│    • Custom markers (ACTIVE/PROSPECT/LOST)     │
│    • Distance calculation (energia)            │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  BACKEND:                                      │
│  ────────────────────────────────────────────  │
│  🤖 Google Gemini API                          │
│    • Conversation simulation                   │
│    • Context-aware responses                   │
│    • 1-5⭐ rating with explanations            │
│                                                 │
│  💾 JSON (Data storage - MVP)                  │
│    • users_data.json (game state)             │
│    • Fast prototyping                          │
│    • Easy debugging                            │
│                                                 │
│  📅 Python datetime                            │
│    • Task deadlines                            │
│    • Visit frequency tracking                  │
│    • Weekly/monthly rhythms                    │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  DEPLOYMENT:                                   │
│  ────────────────────────────────────────────  │
│  ☁️ Streamlit Cloud (MVP)                      │
│    • Free tier: 1GB RAM, 1 CPU                │
│    • Auto-deployment from GitHub               │
│    • SSL included                              │
│                                                 │
│  🚀 Future: Custom hosting                     │
│    • PostgreSQL (scale)                        │
│    • Redis (caching)                           │
│    • Docker (isolation)                        │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  KOSZT (MVP):                                  │
│  • Streamlit Cloud: 0 PLN (free tier)         │
│  • Gemini API: ~50 PLN/m (100 users)          │
│  • Domain: 50 PLN/rok                          │
│  ──────────────                                │
│  TOTAL: ~100 PLN/miesiąc (start)               │
└─────────────────────────────────────────────────┘
```

**Why this stack?**  
Szybkość MVP > Perfect architecture  
Streamlit = 6 tyg implementacji vs 6 m-cy React

---

## SLAJD 18: TIMELINE IMPLEMENTACJI

```
┌─────────────────────────────────────────────────┐
│  📅 6-WEEK IMPLEMENTATION PLAN                  │
│                                                 │
│  WEEK 1: DATA STRUCTURES & MAP                │
│  ────────────────────────────────────────────  │
│  • Client data model (JSON schema)             │
│  • Task system (5 types)                       │
│  • Folium map (Piaseczno area)                 │
│  • 15 fake clients (realistic data)            │
│  Deliverable: Interactive map with pins       │
│                                                 │
│  WEEK 2: CALENDAR & TASK MANAGEMENT            │
│  ────────────────────────────────────────────  │
│  • Calendar UI (Streamlit)                     │
│  • Task auto-generation (wizyty regularne)     │
│  • Deadline tracking                           │
│  • Energy system (100% daily)                  │
│  Deliverable: Functional calendar             │
│                                                 │
│  WEEK 3: AI CONVERSATIONS                      │
│  ────────────────────────────────────────────  │
│  • Gemini API integration                      │
│  • Prompt engineering (PROSPECT/ACTIVE/LOST)   │
│  • Context generation (client history)         │
│  • 1-5⭐ rating system                         │
│  Deliverable: Working AI chat (3 scenarios)   │
│                                                 │
│  WEEK 4: OUTCOMES & EFFECTS                    │
│  ────────────────────────────────────────────  │
│  • Conversation outcomes matrix                │
│  • Task completion effects                     │
│  • Reputation calculations (2-tier)            │
│  • Client status transitions (PROSPECT→ACTIVE) │
│  Deliverable: Full game loop works            │
│                                                 │
│  WEEK 5: TRADE MARKETING & EVENTS              │
│  ────────────────────────────────────────────  │
│  • 5 narzędzi TM (budget tracking)            │
│  • Event system (1-2/day, % distribution)      │
│  • Tool cooldowns                              │
│  • ROI calculations                            │
│  Deliverable: Strategic depth added           │
│                                                 │
│  WEEK 6: POLISH & BALANCE TESTING              │
│  ────────────────────────────────────────────  │
│  • Dashboard UI (charts, stats)                │
│  • Tutorial (onboarding nowych graczy)         │
│  • Balance tuning (probabilities)              │
│  • Bug fixing                                  │
│  Deliverable: MVP ready for beta testers      │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  POST-LAUNCH (Week 7-12):                      │
│  • Beta testing (10-20 handlowców)            │
│  • Feedback collection                         │
│  • Iteracja mechanik                           │
│  • Content expansion (więcej klientów)         │
│                                                 │
│  FULL LAUNCH: Week 13                          │
└─────────────────────────────────────────────────┘
```

**Team:**  
1 dev (Python/Streamlit) + 1 game designer (balance)  
= **6 tygodni do MVP**

---

## SLAJD 19: METRYKI SUKCESU - Jak zmierzymy efekt?

```
┌─────────────────────────────────────────────────┐
│  📊 SUCCESS METRICS                             │
│                                                 │
│  LEARNING OUTCOMES:                            │
│  ────────────────────────────────────────────  │
│  🎯 Avg rating w real cold calls               │
│     Baseline: 2.5⭐ (juniorzy bez treningu)    │
│     Target: 3.5⭐+ (po 20h gry)                │
│     Measure: CRM data (Salesforce/HubSpot)     │
│                                                 │
│  🎯 Time to first contract (juniorzy)          │
│     Baseline: 90-120 dni                       │
│     Target: 60 dni (33% szybciej!)             │
│     Measure: HR onboarding tracking            │
│                                                 │
│  🎯 Win-back success rate                      │
│     Baseline: 15-20% (industry avg)            │
│     Target: 25-30%                             │
│     Measure: CRM LOST→ACTIVE transitions       │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  ENGAGEMENT METRICS:                           │
│  ────────────────────────────────────────────  │
│  📈 Daily Active Users (DAU)                   │
│     Target: 70% graczy loguje się 5+ dni/tyg  │
│                                                 │
│  📈 Session length                             │
│     Target: 25-35 min (sweet spot)             │
│                                                 │
│  📈 Retention (30 dni)                         │
│     Target: 60%+ (benchmark: Duolingo 55%)     │
│                                                 │
│  📈 Level 2 completion rate                    │
│     Target: 40% graczy kończy Level 1 (4 tyg)  │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  BUSINESS IMPACT:                              │
│  ────────────────────────────────────────────  │
│  💰 Koszt treningu / handlowiec                │
│     Traditional: 5,000 PLN (2-day workshop)    │
│     Simulator: 500 PLN (licencja + hosting)    │
│     Savings: 90% 🎉                            │
│                                                 │
│  💰 Onboarding cost reduction                  │
│     Faster to productivity = -30% cost         │
│                                                 │
│  💰 ROI                                        │
│     1 kontrakt extra (junior) = 12k PLN/rok    │
│     Break-even: 1 miesiąc!                     │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  A/B TEST (6 miesięcy):                        │
│  Grupa A: Tradycyjny trening (20 osób)        │
│  Grupa B: Simulator (20 osób)                 │
│                                                 │
│  Measure:                                      │
│  • Sales performance (PLN/miesiąc)             │
│  • Client retention rate                       │
│  • Cold call success rate                      │
│  • Manager satisfaction (1-10)                 │
└─────────────────────────────────────────────────┘
```

---

## SLAJD 20: NEXT STEPS - Co teraz?

```
┌─────────────────────────────────────────────────┐
│  🚀 NASTĘPNE KROKI                              │
│                                                 │
│  PHASE 1: DECISION (2 tygodnie)                │
│  ────────────────────────────────────────────  │
│  ✅ Prezentacja dla stakeholders               │
│  ✅ Q&A session (odpowiedzi na pytania)        │
│  ✅ Budget approval                            │
│  ✅ Wybór beta testerów (10-20 handlowców)     │
│                                                 │
│  PHASE 2: DEVELOPMENT (6 tygodni)              │
│  ────────────────────────────────────────────  │
│  Week 1-2: Core mechanics (map, calendar, AI)  │
│  Week 3-4: Game loop (outcomes, reputation)    │
│  Week 5-6: Polish (UI, balance, tutorial)      │
│                                                 │
│  PHASE 3: BETA TESTING (6 tygodni)             │
│  ────────────────────────────────────────────  │
│  • 10-20 handlowców (mix junior/mid)          │
│  • Weekly feedback sessions                    │
│  • Iteracja mechanik                           │
│  • Content expansion                           │
│                                                 │
│  PHASE 4: LAUNCH (Week 13+)                    │
│  ────────────────────────────────────────────  │
│  • Rollout do całego zespołu                   │
│  • Onboarding nowych graczy                    │
│  • Monitoring metryk                           │
│  • Continuous improvement                      │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  INVESTMENT:                                   │
│  ────────────────────────────────────────────  │
│  Development (6 tyg):       20,000 PLN        │
│  Beta testing (6 tyg):       5,000 PLN        │
│  Hosting (1 rok):            1,200 PLN        │
│  Contingency (20%):          5,000 PLN        │
│  ──────────────────────────────────────        │
│  TOTAL:                     31,200 PLN        │
│                                                 │
│  Expected ROI (Year 1):                        │
│  • 50 handlowców × 4,500 PLN savings          │
│  • = 225,000 PLN saved                         │
│  • ROI: 720% 🚀                                │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│  📞 CONTACT:                                   │
│  [TWOJE DANE]                                  │
│                                                 │
│  📧 Email: [EMAIL]                             │
│  🌐 Demo: [LINK DO PROTOTYPU]                 │
│                                                 │
│  ───────────────────────────────────────────   │
│                                                 │
│         DZIĘKUJEMY ZA UWAGĘ! 🎉                │
│                                                 │
│     Pytania? Otwarte na dyskusję! 💬           │
└─────────────────────────────────────────────────┘
```

---

## BACKUP SLIDES (Q&A)

### B1: Dlaczego nie gotowe platformy (Salesforce Trailhead)?

```
┌─────────────────────────────────────────────────┐
│  Trailhead / LinkedIn Learning:                │
│  ❌ Generic (nie FMCG-specific)                │
│  ❌ Teoretyczne (brak praktyki rozmów)         │
│  ❌ Brak AI conversations                      │
│  ❌ Brak gamifikacji (nudne)                   │
│                                                 │
│  Nasz Simulator:                               │
│  ✅ Custom (Twoje produkty, Twoi klienci)     │
│  ✅ Praktyczny (rozmowy AI, real scenarios)    │
│  ✅ Engaging (30 min/dzień, nie 3h kursu)      │
│  ✅ Mierzalny (postępy widoczne real-time)     │
└─────────────────────────────────────────────────┘
```

### B2: Co z prywatnością danych (AI)?

```
┌─────────────────────────────────────────────────┐
│  GDPR COMPLIANCE:                              │
│  ✅ AI NIE widzi prawdziwych klientów         │
│  ✅ Fake data (generated clients)              │
│  ✅ Gracz może usunąć dane (GDPR right)        │
│  ✅ Gemini API: no training on customer data   │
│                                                 │
│  Wszystkie rozmowy = synthetic scenarios       │
│  (bazowane na realizmie, nie real clients)     │
└─────────────────────────────────────────────────┘
```

### B3: Czy to zastąpi tradycyjne szkolenia?

```
┌─────────────────────────────────────────────────┐
│  NIE - TO SUPLEMENT, NIE REPLACEMENT!          │
│                                                 │
│  Simulator:                                    │
│  • Ongoing practice (30 min/dzień)            │
│  • Soft skills (rozmowy, negocjacje)          │
│  • Individual learning pace                    │
│                                                 │
│  Traditional training:                         │
│  • Product deep-dives (specjaliści)           │
│  • Team building                               │
│  • Strategy sessions                           │
│                                                 │
│  HYBRID MODEL = BEST RESULTS 🎯                │
└─────────────────────────────────────────────────┘
```

---

**KONIEC PREZENTACJI**

**Następny krok:** Wizualizacje (screenshots mockupów UI)
