# 🎯 Mechanika vs Content - Analiza i Decyzja

**Data:** 26 października 2025  
**Problem:** Czy rozwijać mechanikę czy tworzyć content dla nowych branż?

---

## 🔍 **PROBLEM: Różne Perspektywy Rozgrywki**

### **Consulting = "Prowadzenie firmy"** 🏢
```
Gracz = Właściciel firmy konsultingowej
- Zatrudnia pracowników
- Zarządza finansami
- Przyjmuje kontrakty
- Rozwija firmę (10 poziomów)
```

### **FMCG = "Bycie Przedstawicielem Handlowym"** 🛒
```
Gracz = Sales Representative lub Regional Manager
- NIE prowadzi własnej firmy
- Pracuje dla firmy X (np. P&G, Unilever)
- Ma cele sprzedażowe
- Zarządza terytorium/klientami/zespołem
```

### **Pharma = Podobna perspektywa** 💊
```
Gracz = Medical Representative
- Pracuje dla firmy farmaceutycznej
- Buduje relacje z lekarzami (KOLs)
- Edukuje o produktach
- Ma targety recepty
```

---

## 🤔 **DWIE DROGI**

### **OPCJA A: Jedna Mechanika = "Prowadzenie Firmy"** (Status Quo)

**Konsekwencje:**
```
✅ PROS:
- Kod już działa (Consulting ready)
- Szybka implementacja (copy-paste scenarios)
- Spójny UX (wszędzie to samo UI)
- Łatwe w utrzymaniu

❌ CONS:
- **Nierealistyczne dla FMCG/Pharma**
  → Sales rep NIE otwiera własnej firmy!
- Mniejsza immersja
- Gorzej sprzeda się B2B (corporate kupuje "real simulation")
- Gracze z branży powiedzą "to nie tak wygląda moja praca"
```

**Przykład absurdu:**
```
FMCG Game:
"Otwórz własną firmę FMCG i zatrudniaj sales repów"
→ To jest biznes developera/CEO, NIE sales repa!

Pharma Game:
"Załóż własną firmę farmaceutyczną i produkuj leki"
→ To wymaga miliardów i 10 lat, NIE jest to symulacja med repa!
```

---

### **OPCJA B: Różne Mechaniki dla Różnych Branż** (Realistyczne)

**Konsekwencje:**
```
✅ PROS:
- **Realistyczne doświadczenie** (gracz czuje się jak real sales rep)
- Większa immersja i engagement
- Lepiej sprzedaje się B2B ("to jest DOKŁADNIE moja praca!")
- Unikalna value proposition (nikt nie ma tego!)
- Każda branża = inny gameplay (replayability)

❌ CONS:
- Więcej pracy (każda branża = nowa mechanika)
- Trudniejsze w utrzymaniu (6 różnych systemów)
- Ryzyko inconsistency
- Dłuższy czas do MVP
```

**Przykład realizmu:**
```
FMCG Game:
"Jesteś Regional Sales Manager dla Unilever
- Zarządzaj 5 sales repami
- Osiągnij target 500k PLN sprzedaży w Q1
- Wynegocjuj listing w Biedronka
- Rozwiąż konflikt w zespole"
→ TO jest realistyczna symulacja!

Pharma Game:
"Jesteś Medical Representative dla GSK
- Zbuduj relacje z 20 lekarzami (KOLs)
- Edukuj o nowym leku
- Osiągnij 300 recept/miesiąc
- Organizuj konferencję medyczną"
→ TO jest realistyczna symulacja!
```

---

## 💡 **MOJA REKOMENDACJA: HYBRID MODEL** ⚡

### **Rozwiązanie: "Career Progression" Framework**

**Koncepcja:**
Każda branża ma **3-etapową karierę** zamiast "prowadzenie firmy":

```
POZIOM 1-3: Individual Contributor (IC)
- Pracujesz solo
- Realizujesz osobiste targety
- Uczysz się branży

POZIOM 4-7: Team Leader / Manager
- Zarządzasz małym zespołem (2-5 osób)
- Deleguj zadania
- Trenujesz juniorów

POZIOM 8-10: Regional Director / VP
- Zarządzasz całym regionem/działem
- Strategiczne decyzje
- Budżety i biznes planning
```

---

## 🛠️ **IMPLEMENTACJA DLA KAŻDEJ BRANŻY**

### **1. FMCG - "Sales Career Path"** 🛒

#### **Poziomy 1-3: Sales Representative**
```python
ROLE: "Sales Representative"
FIRMA: "GlobalCPG Inc." (fikcyjna, ale realistyczna)

METRYKI:
- 💰 Monthly Sales (zamiast "money")
- 📊 Market Share (zamiast "reputation")
- 🎯 Target Achievement % (nowy metric!)
- ⭐ Customer Satisfaction (5-star reviews od klientów)

KONTRAKTY = ZADANIA SPRZEDAŻOWE:
- "Wynegocjuj listing produktu X w Biedronka"
- "Zrealizuj promocję w 10 sklepach"
- "Rozwiąż reklamację klienta Y"
- "Przeprowadź training dla merchandiserów"

PRACOWNICY = NIE MA (jeszcze solo)

ADVANCEMENT:
- Sales > 50k PLN + Market Share > 10% → Awans na Junior Manager
```

#### **Poziomy 4-7: Sales Team Leader**
```python
ROLE: "Sales Team Leader"

NOWE MECHANIKI:
- 👥 Zarządzasz zespołem 3-5 sales repów
- 📋 Deleguj zadania (AI characters jako Twoi ludzie)
- 🎓 Trening i coaching członków zespołu
- 💰 Team Sales Target (nie tylko Twoje)

KONTRAKTY = ZADANIA MANAGERSKIE:
- "Onboarding nowego sales repa"
- "Coaching 1:1 z underperformerem"
- "Quarterly Business Review z dyrektorem"
- "Zoptymalizuj territory planning"

ADVANCEMENT:
- Team Sales > 200k PLN + Team Satisfaction > 80% → Awans na Regional Manager
```

#### **Poziomy 8-10: Regional Sales Manager**
```python
ROLE: "Regional Sales Manager"

NOWE MECHANIKI:
- 🗺️ Zarządzasz całym regionem (Polska Południowa)
- 💼 Budżet marketingowy (alokuj między kanały)
- 📊 Strategic planning (Q1, Q2, Q3, Q4 targets)
- 🏆 Rekrutacja i zwolnienia managerów

KONTRAKTY = ZADANIA STRATEGICZNE:
- "Launch nowego produktu w regionie"
- "Restructuring zespołu po merger"
- "Negocjacje kontraktu z national chain"
- "Crisis management: product recall"
```

---

### **2. Pharma - "Medical Rep Career Path"** 💊

#### **Poziomy 1-3: Medical Representative**
```python
ROLE: "Medical Representative"
FIRMA: "PharmaGlobal Ltd."

METRYKI:
- 💊 Prescriptions/Month (recepty wystawione przez lekarzy)
- 👨‍⚕️ KOL Relationships (Key Opinion Leaders - 0-100 score)
- 🎯 Territory Coverage (% lekarzy objętych)
- 📚 Product Knowledge Score

KONTRAKTY = ZADANIA MED REPA:
- "Odwiedź 15 lekarzy i edukuj o produkcie X"
- "Zorganizuj lunch & learn dla 8 lekarzy"
- "Zdobądź commitment od KOL na konferencję"
- "Odpowiedz na medical inquiry od lekarza"

PRACOWNICY = NIE MA

ADVANCEMENT:
- Prescriptions > 200/month + KOL Score > 60 → Awans na Senior Rep
```

#### **Poziomy 4-7: Senior Medical Rep / KAM**
```python
ROLE: "Key Account Manager"

NOWE MECHANIKI:
- 🏥 Zarządzasz relacjami z 5 biggest hospitals
- 👥 Mentoring 2-3 junior med reps
- 📊 Tender management (przetargi szpitalne)
- 🎤 Prezentacje na konferencjach medycznych

KONTRAKTY:
- "Wynegocjuj tender w szpitalu wojewódzkim"
- "Coaching med repa który ma słabe wyniki"
- "Organize medical advisory board"
- "Manage adverse event reporting"
```

#### **Poziomy 8-10: Regional Medical Manager**
```python
ROLE: "Regional Medical Manager"

NOWE MECHANIKI:
- 🗺️ Cały region (10-20 med repów)
- 💰 Budget allocation (eventy, konferencje, materiały)
- 📊 Strategic planning (product launches)
- 🎓 Training programs dla zespołu

KONTRAKTY:
- "Launch nowego leku w regionie"
- "Compliance audit preparation"
- "Restructuring territory alignment"
- "KOL engagement strategy dla onkologii"
```

---

### **3. Banking - "Banker Career Path"** 🏦

#### **Poziomy 1-3: Personal Banker**
```python
ROLE: "Personal Banker"
FIRMA: "GlobalBank S.A."

METRYKI:
- 💳 Accounts Opened
- 💰 Loan Portfolio Value
- 😊 Customer Satisfaction (NPS)
- 📈 Cross-sell Ratio

KONTRAKTY:
- "Sprzedaj kredyt hipoteczny młodemu małżeństwu"
- "Rozwiąż reklamację klienta VIP"
- "Przeprowadź financial review z klientem"
- "Upsell kartę premium do konta"
```

#### **Poziomy 4-7: Branch Manager**
```python
ROLE: "Branch Manager"

NOWE MECHANIKI:
- 🏢 Zarządzasz oddziałem (5-10 bankowców)
- 💰 Branch P&L (profit & loss)
- 📊 Sales targets dla całego oddziału
- 👥 Rekrutacja i training

KONTRAKTY:
- "Onboarding nowego bankera"
- "Optimize branch operations (reduce wait time)"
- "Monthly business review z dyrektorem regionalnym"
- "Handle difficult customer escalation"
```

#### **Poziomy 8-10: Regional Director**
```python
ROLE: "Regional Director"

NOWE MECHANIKI:
- 🗺️ 10-20 oddziałów w regionie
- 💼 Strategic planning (ekspansja, zamykanie oddziałów)
- 📊 Risk management (NPL portfolio)
- 🎯 Budget allocation
```

---

### **4. Insurance - "Insurance Career Path"** 🛡️

#### **Poziomy 1-3: Insurance Agent**
```python
ROLE: "Insurance Agent"
FIRMA: "SafeLife Insurance"

METRYKI:
- 💰 Gross Written Premium (GWP)
- 📝 Policies Sold
- 🔄 Retention Rate (ile klientów odnawia)
- ⭐ Customer Satisfaction

KONTRAKTY:
- "Sprzedaj polisę życiową młodej rodzinie"
- "Cross-sell auto insurance do klienta"
- "Handle claim from existing customer"
- "Conduct needs analysis dla SME client"
```

#### **Poziomy 4-7: Agency Manager**
```python
ROLE: "Agency Manager"

NOWE MECHANIKI:
- 👥 Zarządzasz 5-10 agentami
- 💰 Agency GWP target
- 📊 Recruiterowanie nowych agentów
- 🎓 Training i certyfikacja

KONTRAKTY:
- "Recruit 3 new agents this quarter"
- "Coach underperformer to improve sales"
- "Launch new product in your agency"
- "Handle complex commercial claim"
```

#### **Poziomy 8-10: Regional Manager**
```python
ROLE: "Regional Manager"

NOWE MECHANIKI:
- 🗺️ 10-20 agencji w regionie
- 💼 Strategic partnerships (brokerzy)
- 📊 Risk underwriting approval
- 🎯 Regional growth strategy
```

---

### **5. Automotive - "Car Sales Career Path"** 🚗

#### **Poziomy 1-3: Sales Consultant**
```python
ROLE: "Sales Consultant"
FIRMA: "PremiumAuto Dealership"

METRYKI:
- 🚗 Units Sold (nowe + używane)
- 💰 Revenue (sales + finance + insurance)
- 😊 Customer Satisfaction (CSI Score)
- 🔄 Repeat & Referral Rate

KONTRAKTY:
- "Sprzedaj nowy SUV młodej rodzinie"
- "Negotiate trade-in value dla używanego auta"
- "Upsell extended warranty i GAP insurance"
- "Follow-up z klientem po test drive"
```

#### **Poziomy 4-7: Sales Manager**
```python
ROLE: "Sales Manager"

NOWE MECHANIKI:
- 👥 Zarządzasz 5-8 sales consultants
- 💰 Dealership monthly targets
- 📊 Inventory management (co zamawiać)
- 🎓 Product training dla zespołu

KONTRAKTY:
- "Onboard new sales consultant"
- "Handle customer escalation (bad review)"
- "Negotiate fleet deal z firmą"
- "Optimize showroom traffic conversion"
```

#### **Poziomy 8-10: General Manager**
```python
ROLE: "General Manager"

NOWE MECHANIKI:
- 🏢 Cały dealership (sales + service + parts)
- 💼 P&L responsibility
- 📊 Expansion planning (nowy oddział?)
- 🎯 Manufacturer relationship management
```

---

### **6. Consulting - "Consultant Career Path"** (KEEP AS IS)

Consulting już działa dobrze jako "prowadzenie firmy" bo:
- ✅ Realistyczne (konsultanci często otwierają własne boutique)
- ✅ Pasuje do gameplay
- ✅ Kod gotowy

**ZMIANA:** Dodaj option "Employee Track":
```
Choice na starcie:
1. "Załóż własną firmę" (obecny system)
2. "Pracuj dla McKinsey/BCG" (nowy track - career progression)
```

---

## 🎯 **WSPÓLNY FRAMEWORK: "Career Progression System"**

### **Uniwersalne mechaniki dla wszystkich 6 branż:**

```python
CAREER_LEVELS = {
    1-3: "Individual Contributor",
    4-7: "Team Leader / Manager", 
    8-10: "Director / VP"
}

METRICS (customized per industry):
- Primary KPI (sales, prescriptions, accounts, etc.)
- Secondary KPI (satisfaction, market share, etc.)
- Team Performance (if manager)
- Strategic Impact (if director)

CONTRACTS = TASKS:
- IC level: Hands-on work (sales calls, client meetings)
- Manager level: Delegation, coaching, planning
- Director level: Strategy, budget, restructuring

PROGRESSION:
- Hit targets → Unlock next level
- Get promoted → New challenges & responsibilities
- Hall of Fame: "Started as Sales Rep → became VP in 18 months!"
```

---

## 🚧 **IMPLEMENTATION PLAN**

### **Faza 1: Refactor Core System (2 tygodnie)**

**Obecny kod:**
```python
# views/business_games.py
bg_data = {
    "firm": {...},  # Consulting-specific
    "money": 0,
    "employees": []
}
```

**Nowy kod (uniwersalny):**
```python
bg_data = {
    "role": "Sales Representative",  # Industry-specific role
    "company": "GlobalCPG Inc.",     # Employer (nie Twoja firma!)
    
    # Uniwersalne metryki
    "level": 1,
    "career_stage": "individual_contributor",  # IC, manager, director
    
    # Industry-specific metrics
    "metrics": {
        "primary_kpi": 0,      # Sales/Prescriptions/Accounts/etc
        "secondary_kpi": 0,    # Market Share/KOL Score/NPS/etc
        "satisfaction": 0       # Customer/Team/Stakeholder
    },
    
    # Zespół (tylko od poziomu 4+)
    "team": [],  # Puste na start, wypełnia się jak awansujesz
    
    # Kontrakty = Zadania zawodowe
    "tasks": {
        "active": [],
        "completed": []
    }
}
```

---

### **Faza 2: Industry Templates (1 tydzień per branża)**

**Create `data/industries/fmcg.py`:**
```python
FMCG_CONFIG = {
    "industry_name": "FMCG Sales",
    "company_name": "GlobalCPG Inc.",
    
    "career_levels": {
        1: {"role": "Junior Sales Rep", "team_size": 0},
        2: {"role": "Sales Representative", "team_size": 0},
        3: {"role": "Senior Sales Rep", "team_size": 0},
        4: {"role": "Sales Team Leader", "team_size": 3},
        5: {"role": "Area Sales Manager", "team_size": 5},
        6: {"role": "District Manager", "team_size": 8},
        7: {"role": "Regional Manager", "team_size": 12},
        8: {"role": "Regional Director", "team_size": 20},
        9: {"role": "VP Sales", "team_size": 50},
        10: {"role": "Chief Sales Officer", "team_size": 100}
    },
    
    "metrics": {
        "primary": {
            "name": "Monthly Sales",
            "unit": "PLN",
            "targets": [5000, 10000, 20000, 50000, ...]  # Per level
        },
        "secondary": {
            "name": "Market Share",
            "unit": "%",
            "targets": [5, 10, 15, 20, ...]
        }
    },
    
    "tasks_pool": [
        # Import from fmcg_tasks.py (kontrakty)
    ]
}
```

---

### **Faza 3: UI Adaptation (3 dni)**

**Dashboard pokazuje:**
```python
# Zamiast "Twoja firma: XYZ Consulting"
st.subheader(f"🎯 {bg_data['role']} @ {bg_data['company']}")

# Zamiast "Money: 5000 PLN"
st.metric("💰 Monthly Sales", f"{bg_data['metrics']['primary_kpi']:,} PLN")

# Zamiast "Reputation: 50"
st.metric("📊 Market Share", f"{bg_data['metrics']['secondary_kpi']}%")

# Nowy panel: Career Progress
st.progress(level / 10)
st.caption(f"Level {level}/10: {role_name}")
```

---

## ⏱️ **TIMELINE COMPARISON**

### **Opcja A: "Copy-Paste" Consulting → FMCG** (SZYBKIE)
```
Tydzień 1: Skopiuj kod → zmień nazwy → 10 kontraktów
Tydzień 2: Testing
= 2 TYGODNIE per branża
= 10 TYGODNI dla 5 branż (FMCG, Pharma, Banking, Insurance, Auto)
```

**PROS:** Szybko, działa, kod ready  
**CONS:** Nierealistyczne, mała immersja, trudniej sprzedać B2B

---

### **Opcja B: Career Progression Framework** (WOLNIEJSZE, ALE LEPSZE)
```
Tydzień 1-2: Refactor core system (1x robota)
Tydzień 3: FMCG template + 15 tasks
Tydzień 4: Testing FMCG
Tydzień 5: Pharma template + 15 tasks
Tydzień 6: Testing Pharma
...
= 4 TYGODNIE pierwsza branża (FMCG)
= 2 TYGODNIE każda kolejna (reuse framework)
= 12 TYGODNI dla 5 branż
```

**PROS:** Realistyczne, wysoka immersja, łatwiej sprzedać B2B, unique selling point  
**CONS:** +2 tygodnie więcej, więcej kodu do maintain

---

## 💡 **MOJA OSTATECZNA REKOMENDACJA**

### **GO WITH OPTION B - Career Progression**

**Dlaczego?**

1. **B2B sprzedaż wymaga realizmu**
   - Corporate kupuje "real simulation of our jobs"
   - "Open your own pharma company" = instant rejection
   - "Be a med rep and grow to manager" = instant buy!

2. **Unique Value Proposition**
   - Nikt nie ma multi-industry career simulators
   - Każda branża = inny gameplay (6x replayability)
   - "Practice your actual job" vs "pretend you're CEO"

3. **User feedback będzie lepszy**
   - Beta testerzy z FMCG powiedzą "WOW, to jest DOKŁADNIE moja praca!"
   - Zamiast "hmm, ciekawe, ale to nie jest realistyczne"

4. **+2 tygodnie teraz = -6 miesięcy później**
   - Jeśli zrobisz copy-paste, i tak będziesz musiał przerabiać później
   - Lepiej zrobić dobrze od razu

5. **Content > Mechanika (na razie)**
   - Quiz/Decision Tree Contracts możesz dodać później
   - Najpierw zrób 3-4 branże z Career Progression
   - Potem dodasz nowe typy kontraktów (działają na każdej branży!)

---

## 🎯 **NEXT STEPS - CO ZROBIĆ W TYM TYGODNIU**

### **Dzień 1-2: Design Career Framework**
1. Stwórz `data/industries/base.py` - uniwersalny szablon
2. Zdefiniuj 10 poziomów kariery dla FMCG
3. Wymyśl metryki (Monthly Sales, Market Share, Customer Sat)

### **Dzień 3-4: Refactor Core**
1. Zmień `bg_data` struktura (zamiast "firm" → "role", "company", "metrics")
2. Update UI (Dashboard pokazuje nowe metryki)
3. Testing (czy Consulting dalej działa?)

### **Dzień 5-7: Pierwsze 5 zadań FMCG**
1. Napisz 5 kontraktów dla Sales Rep (poziom 1-3)
   - "Wynegocjuj listing w Żabka"
   - "Zrealizuj promocję w 5 sklepach"
   - "Rozwiąż reklamację klienta"
   - "Training dla merchandisera"
   - "Quarterly business review z managerem"
2. Testing

---

## 📝 **TL;DR**

**Pytanie:** Mechanika czy Content?  
**Odpowiedź:** **MECHANIKA NAJPIERW!**

**Powód:** 
- FMCG/Pharma ≠ "prowadzenie firmy"
- Career Progression = realistyczna symulacja
- +2 tygodnie teraz, ale -6 miesięcy później
- Lepiej sprzeda się B2B
- Unique value prop

**Action:** 
Poświęć 2 tygodnie na Career Progression framework, potem content leci szybko (2 tygodnie/branża).

**Timeline:**
- Tydzień 1-2: Career Framework + FMCG template
- Tydzień 3: FMCG content (15 zadań)
- Tydzień 4: Pharma template + content
- Tydzień 5: Banking template + content
- Grudzień: Testing + beta

**Rezultat:** 
3-4 branże gotowe z realistyczną mechaniką → Launch w styczniu!

---

**Chcesz żebym pomógł Ci zaprojektować Career Framework i FMCG template?** 🚀
