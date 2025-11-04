# 📋 System Zadań - Roadmap & Backlog

**Utworzono:** 4 listopada 2025  
**Status:** Phase 1 w implementacji

---

## 🎯 Vision

System zadań ma być **kręgosłupem rozgrywki**, który:
- 🎓 **Uczy** gracza mechanik i best practices sprzedaży
- 📖 **Opowiada historię** scenariusza (story-driven tasks)
- 💰 **Motywuje** poprzez nagrody i progresję
- 🎮 **Jest grywalny** - nie przytłacza, ale angażuje

---

## 📊 Architektura Systemu (3 poziomy)

### **Poziom 1: Onboarding Tasks** ✅ IMPLEMENTED
**Kiedy:** Trial Period (Dzień 1-2)  
**Status:** OBOWIĄZKOWE  
**Nagroda:** Odblokowanie wizyt

```
Tydzień 1, Poniedziałek-Wtorek
├── 📋 Zadanie 1: "Poznaj swoje terytorium" (ABC Segmentation)
├── 🗺️ Zadanie 2: "Zaplanuj pierwszy tydzień" (Routing)
└── 💬 Zadanie 3: "Przygotuj elevator pitch" (Presentation)
```

**✅ Status:** Działa, pozostawiamy bez zmian

---

### **Poziom 2: Weekly Tasks** 🚧 PHASE 1 (w implementacji)
**Kiedy:** Co tydzień (Poniedziałek)  
**Status:** OPCJONALNE  
**Nagroda:** XP + Unlock Tokens + Client Reputation + Company Reputation

```
Tydzień 2: (po trial period)
├── 👋 Pierwsza wizyta (jakość ≥3⭐) → 100 XP + 2 tokens + +5 client rep + +3 company rep
└── 📞 Odwiedź 5 prospectów → 50 XP + 1 token + +3 client rep

Tydzień 3:
├── ✍️ Podpisz pierwszą umowę → 200 XP + 3 tokens + +10 client rep + +5 company rep
└── 📦 Sprzedaj 3 różne kategorie → 100 XP + 2 tokens + +3 company rep

Tydzień 4:
├── 💰 Sprzedaż 5,000 PLN → 200 XP + 3 tokens + +10 company rep
└── ❤️ Reputacja +50 z 3 klientami → 150 XP + 2 tokens + +8 client rep

Tydzień 5+: Dynamic tasks based on scenario + progressive difficulty
```

**💰 System Nagród (FINAL DECISION):**
- ❌ **PLN removed** - nie ma "zarobków" w grze
- ✅ **XP** - career progression, level up (50-300 XP per task)
- ✅ **Unlock Tokens** - "waluta" na premium features (1-3 tokens per task, 5-15 cost per unlock)
- ✅ **Client Reputation** - boost reputacji u klientów (+3 to +10)
- ✅ **Company Reputation** - boost reputacji w firmie (+3 to +10)
- ✅ **Overall Rating** - kombinacja Client (60%) + Company (40%) → Tier progression

**🎯 Implementacja Phase 1:**
- 2-3 zadania tygodniowe
- Deadline: Piątek
- Progress tracking
- Auto-check completion
- Reward payout

---

### **Poziom 3: Milestone Tasks** 📅 PHASE 2
**Kiedy:** Miesięcznie / Event-driven  
**Status:** OPCJONALNE  
**Nagroda:** Duże bonusy + Unlocks + Career progression

```python
MILESTONE_TASKS = {
    "month_1": {
        "establish_presence": {
            "title": "🏆 Osiągnij 10 aktywnych klientów",
            "reward": {
                "cash": 5000,
                "xp": 500,
                "unlock": "territory_expansion",
                "career_level": +1
            },
            "story": "Szef Region: 'Potrzebuję cię na pełnych obrotach. Zbuduj portfolio 10 aktywnych - to otworzy ci drogę do większego terytorium.'"
        }
    },
    
    "heinz_challenge": {
        "beat_kotlin_milestone": {
            "title": "🥊 Kotlin Challenge - Przejmij 6/8",
            "reward": {
                "cash": 10000,
                "xp": 1000,
                "achievement": "Kotlin Slayer",
                "unlock": "exclusive_heinz_products"
            },
            "story": "HQ Challenge: Kotlin dominuje w Dzięgielowie. Szef stawia 10k PLN bonusu za przejęcie 6 lokali. Let's crush them!"
        }
    },
    
    "territory_master": {
        "full_coverage": {
            "title": "🗺️ 100% Coverage - Wszystkie segmenty",
            "description": "Zdobądź min. 1 klienta z każdego typu (Burger, Kebab, Stołówka, Pizza, Hotel, Dystrybutor)",
            "reward": {
                "cash": 8000,
                "achievement": "Segment Master",
                "unlock": "premium_analytics"
            }
        }
    }
}
```

---

## 🎮 Typy Zadań (Catalog)

### **1. Learning Tasks (Edukacyjne)**
**Cel:** Nauczanie mechanik gry i real-world knowledge

```python
{
    "type": "learning",
    "title": "📚 Przeczytaj artykuł: Kanał Tradycyjny",
    "description": "Zapoznaj się z materiałem o dystrybucji FMCG",
    "action_required": "read_article",
    "reward": {"xp": 50},
    "time_to_complete": "10 min",
    "assigned_by": "Mentor",
    "story": "Mentor: 'Zanim zaczniesz sprzedawać, musisz zrozumieć jak działa kanał. Przeczytaj - potem quizik!'"
}

# Warianty:
- Przeczytaj case study
- Obejrzyj tutorial video
- Ukończ quiz (np. o technikach sprzedażowych)
- Eksploruj Dashboard (tooltips)
```

### **2. Sales Tasks (Sprzedażowe)**
**Cel:** Aktywność sprzedażowa, realizacja celów revenue

```python
{
    "type": "sales",
    "title": "💰 Sprzedaż 5,000 PLN w tym tygodniu",
    "description": "Osiągnij łączną sprzedaż 5k PLN do piątku",
    "action_required": "achieve_sales",
    "target": 5000,
    "reward": {"cash": 1000, "xp": 200, "reputation": +10},
    "assigned_by": "Regional Manager",
    "story": "Szef: 'Headquarters patrzy na liczby. 5k do piątku - pokaż że jesteś warty awansu!'"
}

# Warianty:
- Sprzedaj X jednostek produktu Y
- Osiągnij X% marży
- Zamknij umowę wartości min. X PLN
- Sprzedaj pełną paletę (promocja)
```

### **3. Relationship Tasks (Relacyjne)**
**Cel:** Budowanie długoterminowych relacji z klientami

```python
{
    "type": "relationship",
    "title": "❤️ Zbuduj reputację +50 z 3 klientami",
    "description": "Doprowadź 3 aktywnych klientów do reputacji +50",
    "action_required": "achieve_reputation",
    "target": {"clients": 3, "reputation_threshold": 50},
    "reward": {"cash": 800, "xp": 150, "unlock": "loyalty_program"},
    "assigned_by": "Customer Success Manager",
    "story": "CSM: 'Lojalność = powtarzalne zamówienia. Wybierz 3 klientów i zbuduj relację. Wizyty, telefony, wsparcie!'"
}

# Warianty:
- Odzyskaj klienta ze statusu LOST
- Zrób follow-up call do 5 klientów
- Przeproś klienta za błąd (recovery task)
- Upsell: klient ACTIVE → VIP (3+ produkty)
```

### **4. Strategic Tasks (Strategiczne)**
**Cel:** Długoterminowe planowanie, rozwój terytorium

```python
{
    "type": "strategic",
    "title": "🗺️ Rozszerz terytorium o 5 km",
    "description": "Zdobądź 3 klientów poza obecnym promieniem 15 km",
    "action_required": "territory_expansion",
    "target": {"new_clients": 3, "min_distance": 15},
    "reward": {"cash": 2000, "xp": 300, "territory_radius": +5},
    "assigned_by": "Territory Manager",
    "story": "TM: 'Mamy niezagospodarowany teren 20 km od bazy. Zdobądź 3 sklepy - territory expansion approved!'"
}

# Warianty:
- Otwórz nowy segment (np. HoReCa → Retail)
- Zaplanuj trasę optymalną (min. 8 wizyt, max 50 km)
- Wprowadź nowy produkt do 5 sklepów
- Cross-region cooperation (współpraca z innym repem)
```

### **5. Competitive Tasks (Konkurencyjne)**
**Cel:** Przejmowanie od konkurencji, market share

```python
{
    "type": "competitive",
    "title": "🥊 Przejmij 2 klientów od Dove",
    "description": "Zamień Dove Personal Care na FreshLife w 2 sklepach",
    "action_required": "win_from_competitor",
    "target": {"competitor": "Dove", "wins": 2, "category": "Personal Care"},
    "reward": {"cash": 1500, "xp": 250, "achievement": "Dove Buster"},
    "assigned_by": "Marketing Director",
    "story": "Marketing: 'Dove ma 60% share w Personal Care. Zdobądź 2 przyczółki - to otworzy kampanię regionalną!'"
}

# Warianty:
- Intelligence gathering (odwiedź 3 sklepy z Kotlin, zrób notatki)
- Price war defense (utrzymaj klientów mimo promocji konkurencji)
- Category killer (zdominiej jedną kategorię w regionie)
```

### **6. Operational Tasks (Operacyjne)**
**Cel:** Codzienne czynności, efficiency

```python
{
    "type": "operational",
    "title": "📦 Zrealizuj 10 dostaw terminowo",
    "description": "Wszystkie dostawy w tym tygodniu on-time (0 opóźnień)",
    "action_required": "delivery_performance",
    "target": {"deliveries": 10, "on_time_rate": 100},
    "reward": {"cash": 500, "xp": 100, "reputation": +5},
    "assigned_by": "Logistics Manager",
    "story": "Logistics: 'Klienci narzekają na opóźnienia. 10 dostaw w terminie - pokażmy że możemy!'"
}

# Warianty:
- Zinwentaryzuj magazyn (stock check)
- Zmniejsz straty (breakage <2%)
- Optymalizuj trasę (fuel efficiency)
- Aktualizuj dane klientów (CRM hygiene)
```

### **7. Innovation Tasks (Innowacyjne)**
**Cel:** Testowanie nowych produktów, feedback

```python
{
    "type": "innovation",
    "title": "🧪 Przetestuj nowy produkt w 5 sklepach",
    "description": "Wprowadź 'FreshLife Eco Bottle' do 5 sklepów i zbierz feedback",
    "action_required": "product_launch",
    "target": {"product_id": "freshlife_eco", "test_stores": 5},
    "reward": {"cash": 1200, "xp": 200, "unlock": "product_innovation_program"},
    "assigned_by": "R&D Director",
    "story": "R&D: 'Mamy nowy produkt eco-friendly. Przetestuj w 5 sklepach, zbierz opinie - jeśli działa, full rollout!'"
}

# Warianty:
- A/B test: 2 SKU, który się lepiej sprzedaje?
- Feedback survey (zapytaj 10 klientów o produkt)
- Display test (przetestuj nowe POS materials)
```

---

## 📅 Frequency & Timing

### **Tydzień 1 (Trial + First Active Week)**
```
Poniedziałek:
  🔴 [OBOWIĄZKOWE] 3 zadania onboardingowe
     Deadline: Wtorek EOD
     Reward: Unlock wizyt
  
Środa (po ukończeniu onboarding):
  🟡 [OPCJONALNE] 2 zadania tygodniowe
     - Pierwsza wizyta (deadline: Piątek)
     - 5 prospectów (deadline: Piątek)
     Reward: 800 PLN + 150 XP
  
Piątek EOD:
  ⏰ Auto-check completion
  💰 Wypłata nagród
  📊 Weekly summary
```

### **Tydzień 2-8 (Regular Weeks)**
```
Poniedziałek AM:
  📋 Nowe zadania tygodniowe (2-3 tasks)
     Priority: 1 HIGH + 1-2 MEDIUM
     Deadline: Piątek
  
  💡 Daily challenges (opcjonalne, Phase 3)
     Quick wins: 100-300 PLN
  
Środa:
  🔔 Reminder: 2 dni do deadline
  📈 Progress update w Dashboard
  
Piątek EOD:
  ⏰ Auto-check + rewards
  📊 Week summary + next week preview
  🏆 Milestone progress check
```

### **Koniec Miesiąca**
```
Last Friday:
  🎉 Monthly recap
  🏆 Milestone completion check
  💰 Bonusy miesięczne (5k-10k PLN)
  📈 Career progression (awans/unlock)
  🔓 New features unlock
  📋 Next month objectives
```

---

## 🎬 Story Integration (Heinz Scenario Example)

### **Week 1: Introduction**
```
📞 Telefon od Commercial Director (Paweł)

"Witaj! Jestem Paweł, twój szef z centrali Heinz Polska. 
Widzę że zaczynasz w Dzięgielowie - dobry wybór terenu.

Region ma potencjał 25 punktów sprzedaży, ale Kotlin tam dominuje. 
Mam dla ciebie challenge:

📋 Tydzień 1: Trial period - poznaj rynek
   - Segmentacja ABC (które sklepy są kluczowe?)
   - Routing (jak objechać teren efektywnie?)
   - Pitch (co powiesz przy pierwszej wizycie?)

📋 Tydzień 2: First blood
   - Wykonaj 5 wizyt (poznaj klientów)
   - Podpisz pierwszą umowę (Heinz lub Pudliszki - obojętne)

📋 Tydzień 3-4: Kotlin Hunt
   - Przejmij 2 klientów od Kotlin
   - To będzie twój egzamin na juniora

Powodzenia! Dzwonię w piątek po update. 📞"
```

### **Week 2: After First Contract**
```
📞 Telefon od Pawła

"Słyszałem! Pierwsza umowa podpisana - gratulacje! 🎉

Teraz czas na skalowanie. Marketing przygotował dla ciebie:
- 📦 Starter pack: POS materials (wobblery, plakaty)
- 💰 Promo pricing: Pudliszki -5% na pierwsze zamówienie
- 📊 Competitor intel report: gdzie jest Kotlin silny

📋 Nowe zadanie: Kotlin Intelligence
   - Odwiedź 3 sklepy używające Kotlin
   - Zrób notatki: dlaczego wybrali Kotlin? Jakie pain points?
   - Deadline: Czwartek (potrzebuję na meeting z HQ)

Reward: 800 PLN + access do competitive pricing tools.

Do usłyszenia! 📞"
```

### **Week 3: Kotlin Campaign Launch**
```
📧 Email od Marketing Director

"Dzień dobry,

Twój intel z terenu był bardzo wartościowy. HQ dało zielone światło na:

🥊 KOTLIN CRUSH CAMPAIGN
   
Cel: Przejmij 6 z 8 klientów Kotlin w Dzięgielowie
Nagroda: 10,000 PLN bonus + exclusive Heinz products unlock

Dostępne narzędzia:
- 📉 Competitive pricing (Pudliszki matching Kotlin -2%)
- 🎁 Conversion bundle (ketchup + mustard + mayo = -15%)
- 📦 Free POS materials dla przejętych klientów
- ☎️ Wsparcie Key Account Manager (telefon do trudnych przypadków)

Easy targets (zaczynaj od tych):
1. Kebab Express - narzeka na delivery Kotlin
2. Pizza House - niespójna jakość ketchupów

Hard targets (zostaw na koniec):
3. Burger Station - bardzo price sensitive
4. Stołówka Zakładowa - długi kontrakt z Kotlin

Deadline: Koniec miesiąca (2 tygodnie)

Powodzenia! Headquarters obserwuje tę kampanię.

Pozdrawiam,
Anna Kowalska
Marketing Director, Heinz Polska"
```

### **Week 4: Final Push**
```
📞 Telefon od Pawła (pilny)

"Hej! Quick update - świetna robota do tej pory!

Status Kotlin Campaign:
✅ 4/6 przejęte
⏰ 2 zostały (Burger Station, Stołówka)
⏳ 3 dni do deadline

HQ podniosło stawkę: jeśli zamkniesz 6/6 (a nie 6/8), bonus rośnie:
- Standard (6/8): 10,000 PLN ✅
- Excellence (6/6): 15,000 PLN 🏆

Burger Station: użyj FOZ technique, pokaż cost per portion
Stołówka: kontrakt wygasa za tydzień - catch them now!

Dasz radę? Dzwonię w piątek z CEO na linii 😉

Trzymam kciuki! 📞"
```

---

## 🎯 Task Categories & Examples

### **Category: Customer Acquisition**
```
- Zdobądź 5 nowych prospectów (PROSPECT status)
- Podpisz pierwszą umowę (PROSPECT → ACTIVE)
- Reaktywuj 2 utraconych klientów (LOST → ACTIVE)
- Wykonaj cold call do 10 nowych sklepów
```

### **Category: Revenue Growth**
```
- Osiągnij 5k PLN sprzedaży w tym tygodniu
- Zwiększ average order value o 20%
- Sprzedaj 3 palety produktu premium
- Upsell: dodaj +1 SKU do 5 obecnych zamówień
```

### **Category: Portfolio Management**
```
- Sprzedaj produkty z min. 3 kategorii
- Wprowadź nowy produkt do 5 sklepów
- Zrób cross-sell: klient kupuje A → sprzedaj B
- Portfolio balance: 60% value + 40% premium products
```

### **Category: Territory Development**
```
- Rozszerz teren o 5 km (3 nowe sklepy)
- Osiągnij 100% coverage (wszystkie segmenty)
- Zaplanuj optymalną trasę (8 wizyt, <50 km)
- Otwórz nowy kanał (np. e-commerce B2B)
```

### **Category: Competitive**
```
- Przejmij 2 klientów od Kotlin
- Zbadaj ofertę konkurencji (mystery shopping)
- Obróń klienta przed price war (utrzymaj mimo -20% od konkurenta)
- Zdobądź exclusive shelf space (wypierz Dove z półki)
```

### **Category: Relationship**
```
- Zbuduj reputację +50 z 3 klientami
- Zrób follow-up do wszystkich klientów (0 zaniedbanych)
- Przeproś klienta i odzyskaj reputację (recovery)
- Zorganizuj product demo u klienta VIP
```

### **Category: Operational Excellence**
```
- 10 dostaw on-time (100% punctuality)
- Zinwentaryzuj magazyn (stock accuracy >95%)
- Zaktualizuj dane CRM (wszystkie kontakty aktualne)
- Zmniejsz breakage <2% (careful handling)
```

---

## 🔧 Technical Implementation Notes

### **Data Structure**
```python
# Session state storage
st.session_state.tasks = {
    "active": [task1, task2, task3],
    "completed": [task4, task5],
    "failed": [],  # missed deadline
    "available": []  # unlocked but not started
}

# Task object
task = {
    "id": "week2_first_contract",
    "type": "sales",  # learning, sales, relationship, etc.
    "title": "✍️ Podpisz pierwszą umowę",
    "description": "Zmień status klienta z PROSPECT → ACTIVE",
    "assigned_by": "Regional Manager",
    "assigned_date": "2025-11-04",
    "deadline": "2025-11-08",  # Friday
    "priority": "HIGH",  # CRITICAL, HIGH, MEDIUM, LOW
    
    "requirements": {
        "type": "client_status_change",
        "from_status": "PROSPECT",
        "to_status": "ACTIVE",
        "count": 1
    },
    
    "progress": {
        "current": 0,
        "target": 1,
        "percentage": 0
    },
    
    "reward": {
        "cash": 1000,
        "xp": 200,
        "reputation": 10,
        "unlock": None  # or feature name
    },
    
    "story": {
        "intro": "Szef dzwoni: 'Dobra robota z wizytami! Teraz czas na konkret - podpisz umowę do piątku!'",
        "completion": "🎉 Pierwsza umowa! Szef gratuluje i dodaje nowe zadania.",
        "failure": "😞 Nie udało się w tym tygodniu. Próbuj dalej!"
    },
    
    "status": "active",  # active, completed, failed, locked
    "completed_date": None,
    "completion_method": None  # auto or manual
}
```

### **Auto-Check Logic**
```python
def check_task_completion(task, game_state, clients):
    """Auto-check if task requirements are met"""
    
    req_type = task["requirements"]["type"]
    
    if req_type == "client_status_change":
        # Count clients that changed status
        changed = count_status_changes(
            clients, 
            from_status=task["requirements"]["from_status"],
            to_status=task["requirements"]["to_status"],
            since=task["assigned_date"]
        )
        task["progress"]["current"] = changed
        
        if changed >= task["requirements"]["count"]:
            complete_task(task)
    
    elif req_type == "sales_target":
        # Check revenue
        sales = game_state.get("weekly_sales", 0)
        task["progress"]["current"] = sales
        
        if sales >= task["requirements"]["target"]:
            complete_task(task)
    
    # ... more check types
```

### **Reward Payout**
```python
def complete_task(task):
    """Mark task as completed and give rewards"""
    task["status"] = "completed"
    task["completed_date"] = datetime.now()
    
    # Payout rewards
    reward = task["reward"]
    
    if reward.get("cash"):
        game_state["money"] += reward["cash"]
        st.success(f"💰 +{reward['cash']} PLN")
    
    if reward.get("xp"):
        game_state["xp"] += reward["xp"]
        check_level_up(game_state)
    
    if reward.get("reputation"):
        # Reputation boost to all active clients
        boost_all_reputation(clients, reward["reputation"])
    
    if reward.get("unlock"):
        unlock_feature(reward["unlock"])
    
    # Show story completion message
    if task["story"].get("completion"):
        st.info(task["story"]["completion"])
    
    # Move to completed list
    st.session_state.tasks["completed"].append(task)
    st.session_state.tasks["active"].remove(task)
```

---

## 🚀 Implementation Phases

### **✅ PHASE 0: Current State**
- 3 onboarding tasks (trial period)
- Basic task UI in Dashboard → Zadania
- Manual completion (no auto-check)
- Static tasks (nie zmieniają się tygodniowo)

### **🚧 PHASE 1: Weekly Tasks (MVP)** ← CURRENT FOCUS
**Scope:**
- 2-3 zadania tygodniowe (auto-assign w poniedziałek)
- Auto-check completion (sales, status changes)
- Automatic reward payout
- Progress tracking w Dashboard
- Deadline reminder (środa, piątek)

**Files to modify:**
- `data/tasks.py` - task definitions
- `fmcg_playable.py` - UI rendering, auto-check logic
- `game_state` - task tracking storage

**Estimated time:** 4-6 hours

### **📅 PHASE 2: Story Integration + Milestones**
**Scope:**
- Story-driven task assignment (telefony, emaile od NPCs)
- Milestone tasks (miesięczne cele)
- Achievement system (badges)
- Task unlocks (complete A to unlock B)
- Scenario-specific tasks (Heinz vs Quick Start)

**Estimated time:** 8-10 hours

### **🎮 PHASE 3: Advanced Features**
**Scope:**
- Daily challenges (opcjonalne mini-tasks)
- Dynamic task generation (AI-based, react to player behavior)
- Task chains (A → B → C quest lines)
- Competitive tasks (leaderboards)
- Team tasks (współpraca z innymi repami, multiplayer prep)

**Estimated time:** 12-15 hours

---

## 📊 Success Metrics

**KPIs do trackowania:**
- Task completion rate (% ukończonych)
- Average tasks per week
- Preferred task types (które gracze lubią?)
- Task impact on retention (czy zadania trzymają graczy?)
- Reward effectiveness (które nagrody motywują?)

**Target metrics (Phase 2):**
- 70%+ completion rate for HIGH priority
- 50%+ completion rate for MEDIUM priority
- Avg 2-3 tasks completed per week
- 80%+ players complete onboarding

---

## 💡 Future Ideas (Backlog)

### **Social/Multiplayer Tasks**
```
- Współpraca: 2 repów wspólnie obsługują dużego klienta
- Konkurencja: kto szybciej zdobędzie 10 aktywnych?
- Mentoring: senior rep daje zadania juniorowi
- Team challenge: całe terytorium vs inny region
```

### **Seasonal/Event Tasks**
```
- Black Friday Campaign (tydzień mega sprzedaży)
- Holiday Season (grudzień: double rewards)
- New Product Launch Event (2-tygodniowa kampania)
- End-of-Quarter Push (ostatni tydzień kwartału)
```

### **Gamification Enhancements**
```
- Streaks (7 dni pod rząd = bonus)
- Combo system (3 zadania tego samego typu = 2x reward)
- Hidden tasks (Easter eggs, discover by exploration)
- Challenge mode (hard difficulty, 3x reward)
```

### **AI-Driven Tasks**
```python
# System analizuje zachowanie gracza i dostosowuje zadania
if player_weak_in_category("relationship"):
    assign_task("relationship_building_focus")

if player_ignoring_segment("HoReCa"):
    assign_task("explore_horeca_segment")

if player_losing_to_competitor("Kotlin"):
    assign_task("competitive_defense_training")
```

---

## � Reputation System (Replacement for Money)

### **🎯 Problem Statement**
FMCG game nie ma tradycyjnych "zarobków" - gracz nie dostaje pensji ani prowizji w PLN.  
**Potrzebujemy systemu nagród opartego na REPUTATION + UNLOCKS zamiast pieniędzy.**

### **🏗️ Architecture: 3-Level Reputation System**

```
┌─────────────────────────────────────────────────────────┐
│                  OVERALL RATING ⭐                      │
│         (wyświetlane w Hero Section + Dashboard)        │
│                                                          │
│   Formula: (Client Rep × 60%) + (Company Rep × 40%)    │
│                                                          │
│   Przykład: (85 × 0.6) + (72 × 0.4) = 79.8/100        │
│             ⭐⭐⭐⭐ Senior Representative                │
└─────────────────────────────────────────────────────────┘
              ▲                            ▲
              │                            │
              │                            │
    ┌─────────┴──────────┐      ┌─────────┴──────────┐
    │  CLIENT REPUTATION │      │ COMPANY REPUTATION │
    │       (60%)        │      │       (40%)        │
    └────────────────────┘      └────────────────────┘
```

---

### **📊 Component 1: Client Reputation (60% weight)**

**Źródła:**
```python
client_reputation = average([
    client_1_reputation,  # np. Biedronka: 85/100
    client_2_reputation,  # np. Żabka: 72/100
    client_3_reputation,  # np. Carrefour: 90/100
    # ... wszystkie aktywni klienci
])
```

**Jak klient ocenia przedstawiciela:**
- ✅ **Visit Quality** (40%) - średnia jakość wizyt (1-5⭐)
- ✅ **Relationship Level** (30%) - obecny poziom relacji (0-100)
- ✅ **Contract Performance** (20%) - terminowość dostaw, brak reklamacji
- ✅ **Product Mix Success** (10%) - diversyfikacja zakupów (czy kupują różne kategorie)

**Przykład:**
```
Biedronka:
  - Visit Quality: 4.2⭐ / 5⭐ = 84%
  - Relationship: 75/100
  - Contract Performance: 90% (9/10 dostaw on-time)
  - Product Mix: 60% (3/5 kategorii kupowanych)
  
  → Biedronka Reputation = (84×0.4) + (75×0.3) + (90×0.2) + (60×0.1) = 79.1/100
```

---

### **📊 Component 2: Company Reputation (40% weight)**

**Źródła:**
```python
company_reputation = (
    task_performance × 0.30 +      # Czy wykonujesz zadania tygodniowe?
    sales_performance × 0.40 +     # Czy osiągasz cele sprzedażowe?
    professionalism × 0.30         # Jakość pracy, brak błędów
)
```

**Breakdown:**

#### **2a. Task Performance (30%)**
```python
task_performance = completed_tasks / assigned_tasks × 100

# Przykład:
# Tydzień 2: 2/2 zadania = 100%
# Tydzień 3: 1/2 zadania = 50%
# Tydzień 4: 2/2 zadania = 100%
# → Average: 83.3%
```

#### **2b. Sales Performance (40%)**
```python
sales_performance = (
    scenario_goal_progress × 0.60 +  # Czy osiągasz cele scenariusza?
    weekly_sales_trend × 0.40        # Czy sprzedaż rośnie?
)

# Przykład:
# Cel: 15,000 PLN monthly sales
# Aktualnie: 8,500 PLN (56.7% celu)
# Trend: +15% vs poprzedni tydzień
# → Sales Performance = (56.7 × 0.6) + (115 × 0.4) = 80%
```

#### **2c. Professionalism (30%)**
```python
professionalism = 100 - penalties

# Penalties:
# - Spóźniona dostawa: -5 points
# - Zła jakość wizyty (<2⭐): -3 points
# - Przekroczenie budżetu paliwa: -2 points
# - Niezrealizowane obietnice: -10 points

# Przykład:
# Start: 100
# - 1 spóźniona dostawa: -5
# - 1 słaba wizyta: -3
# → Professionalism = 92/100
```

---

### **🎖️ Tier System (6 Levels)**

```
┌──────────────────────────────────────────────────────────────┐
│ TIER         │ OVERALL RATING │ UNLOCKS                      │
├──────────────────────────────────────────────────────────────┤
│ 🟤 Trainee   │    0-40        │ Basic features only          │
│ 🔵 Junior    │   41-55        │ + Route planner              │
│ 🟢 Regular   │   56-70        │ + Client insights            │
│ 🟡 Senior    │   71-85        │ + Advanced analytics         │
│ 🟠 Expert    │   86-95        │ + Mentor mode                │
│ 🔴 Master    │   96-100       │ + All premium features       │
└──────────────────────────────────────────────────────────────┘
```

**Progression Speed:**  
Target: **1 tier per week** (achievable with consistent task completion)

**Przykładowa trajektoria:**
```
Tydzień 1 (Trial): 35 → 🟤 Trainee
Tydzień 2: 45 → 🔵 Junior (wykonane 2/2 zadania + 3 dobre wizyty)
Tydzień 3: 58 → 🟢 Regular (podpisana pierwsza umowa)
Tydzień 4: 68 → 🟢 Regular (stabilizacja)
Tydzień 5: 73 → 🟡 Senior (breakthrough w sprzedaży)
Tydzień 6: 78 → 🟡 Senior (konsolidacja)
Tydzień 7: 82 → 🟡 Senior (dobre performance)
Tydzień 8: 87 → 🟠 Expert (osiągnięcie głównego celu scenariusza)
```

---

### **💰 Multi-Currency Reward System**

**5 walut w grze:**

#### **1. XP (Experience Points)**
- **Cel:** Career progression, level up
- **Źródła:** Zadania, wizyty, kontrakty, milestone achievements
- **Range:** 50-300 XP per task
- **Unlock:** Nowe umiejętności, tytuły, achievements

#### **2. Client Reputation Points**
- **Cel:** Boost reputacji u konkretnych klientów
- **Źródła:** Quality visits, relationship tasks, successful upsells
- **Range:** +3 to +10 per task
- **Impact:** Lepsza pozycja u klienta → większe zamówienia

#### **3. Company Reputation Points**
- **Cel:** Boost reputacji w firmie
- **Źródła:** Task completion, sales targets, professionalism
- **Range:** +3 to +10 per task
- **Impact:** Overall Rating tier progression → unlocks

#### **4. Unlock Tokens** 🎟️
- **Cel:** "Waluta" na premium features
- **Źródła:** Weekly tasks (głównie)
- **Earning:** 1-3 tokens per weekly task
- **Spending:** 5-15 tokens per feature unlock
- **Przykłady:**
  ```
  - Route Optimizer: 5 tokens
  - Advanced Analytics: 10 tokens
  - Client Insights (競合情報): 8 tokens
  - Mentor AI Assistant: 15 tokens
  - Custom Reports: 12 tokens
  ```

#### **5. Training Credits** 📚
- **Cel:** Skill development, learning modules
- **Źródła:** Milestone tasks, achievements
- **Spending:** Unlock training courses (SPIN Selling, Negotiation, etc.)
- **System:** 1 credit = 1 kurs

---

### **🎁 Task Reward Structure (FINAL)**

```python
# Weekly Task Rewards (standard difficulty):
{
    "xp": 100,                    # Career progression
    "unlock_tokens": 2,           # Premium features
    "client_reputation": +5,      # Boost u klientów
    "company_reputation": +3,     # Boost w firmie
    "training_credits": 0         # Tylko milestone tasks
}

# Harder tasks (competitive, territorial):
{
    "xp": 200,
    "unlock_tokens": 3,
    "client_reputation": +8,
    "company_reputation": +5,
    "training_credits": 0
}

# Milestone tasks:
{
    "xp": 500,
    "unlock_tokens": 5,
    "client_reputation": +15,
    "company_reputation": +10,
    "training_credits": 1         # Bonus!
}
```

---

### **📱 UI/UX Design**

#### **Hero Section (Top Bar)**
```
┌────────────────────────────────────────────────────────┐
│  ⭐ OVERALL RATING: 73/100 (🟡 Senior Representative) │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│  Progress to Expert: 13 points needed                  │
│  🎟️ Unlock Tokens: 12  |  📚 Training Credits: 2     │
└────────────────────────────────────────────────────────┘
```

#### **Dashboard → Statystyki**
```
┌─── REPUTATION BREAKDOWN ───────────────────────────────┐
│                                                         │
│  👥 CLIENT REPUTATION (60% weight): 85/100             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│                                                         │
│  Top Clients:                                           │
│    🟢 Biedronka: 90/100 (Visit Quality: 4.5⭐)         │
│    🟢 Carrefour: 88/100 (Relationship: 85)             │
│    🟡 Żabka: 72/100 (Contract Performance: 65%)        │
│                                                         │
│  📊 Average across 8 active clients                     │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🏢 COMPANY REPUTATION (40% weight): 72/100            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│                                                         │
│  Components:                                            │
│    📋 Task Performance: 83% (5/6 zadań wykonanych)     │
│    💰 Sales Performance: 68% (10,200 / 15,000 PLN)    │
│    💼 Professionalism: 92% (-8 penalty points)         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### **Task Completion Popup**
```
┌─── ZADANIE UKOŃCZONE! ─────────────────────────────────┐
│                                                         │
│  ✅ "Pierwsza wizyta (jakość ≥3⭐)"                    │
│                                                         │
│  NAGRODY:                                               │
│  🔹 +100 XP                                            │
│  🔹 +2 Unlock Tokens 🎟️                               │
│  🔹 +5 Client Reputation (Biedronka: 72 → 77)         │
│  🔹 +3 Company Reputation (Task Performance: 80→83%)   │
│                                                         │
│  ⭐ OVERALL RATING: 68 → 71 (🟡 Senior unlocked!)     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### **🔧 Implementation Phases**

#### **Phase 1: Core Reputation System** ⏱️ 3 days
1. Extend `game_state` with reputation tracking:
   ```python
   "reputation": {
       "clients": {
           "client_id_1": 75,
           "client_id_2": 82,
           # ...
       },
       "company": {
           "task_performance": 83,
           "sales_performance": 68,
           "professionalism": 92
       },
       "overall_rating": 73,
       "tier": "Senior",
       "unlock_tokens": 12,
       "training_credits": 2
   }
   ```

2. Create calculation functions:
   ```python
   def calculate_client_reputation(client_id, game_state):
       # Visit quality + Relationship + Contract + Product mix
       pass
   
   def calculate_company_reputation(game_state):
       # Task + Sales + Professionalism
       pass
   
   def calculate_overall_rating(game_state):
       # (Client × 0.6) + (Company × 0.4)
       pass
   
   def get_tier(overall_rating):
       # Map rating → tier name
       pass
   ```

3. Add UI components:
   - Hero Section: Overall Rating card
   - Dashboard → Statystyki: Reputation breakdown
   - Task completion: Reward popup

#### **Phase 2: Task Reward System** ⏱️ 2 days
1. Update task definitions in `data/tasks.py`:
   ```python
   "reward": {
       "xp": 100,
       "unlock_tokens": 2,
       "client_reputation": 5,
       "company_reputation": 3,
       "training_credits": 0
   }
   ```

2. Implement reward distribution:
   ```python
   def award_task_reward(task_id, game_state):
       reward = tasks[task_id]["reward"]
       game_state["xp"] += reward["xp"]
       game_state["reputation"]["unlock_tokens"] += reward["unlock_tokens"]
       # ... update reputation components
       recalculate_overall_rating(game_state)
   ```

3. Show reward popup in UI

#### **Phase 3: Tracking Integration** ⏱️ 2 days
1. Hook into visit execution:
   ```python
   # After visit completes:
   update_client_reputation(client_id, visit_quality)
   update_professionalism(penalties)
   ```

2. Hook into contract signing:
   ```python
   # After contract signed:
   update_company_reputation("sales_performance", +5)
   ```

3. Hook into task completion:
   ```python
   # After task completed:
   update_company_reputation("task_performance", +1)
   award_task_reward(task_id)
   ```

4. Weekly recalculation trigger:
   ```python
   # Każdy Poniedziałek:
   recalculate_all_reputation_components()
   check_tier_progression()
   ```

#### **Phase 4: Unlock System** ⏱️ 3 days
1. Define unlockable features:
   ```python
   UNLOCKS = {
       "route_optimizer": {"cost": 5, "tier_required": "Junior"},
       "client_insights": {"cost": 8, "tier_required": "Regular"},
       "advanced_analytics": {"cost": 10, "tier_required": "Senior"},
       # ...
   }
   ```

2. Create unlock UI in Settings:
   ```
   ┌─── PREMIUM FEATURES ───────────────────────┐
   │ 🎟️ Your Tokens: 12                        │
   │                                             │
   │ ✅ Route Optimizer (5 tokens) - UNLOCKED   │
   │ 🔒 Client Insights (8 tokens) - UNLOCK?   │
   │ 🔒 Advanced Analytics (10 tokens)          │
   │    (Requires: 🟡 Senior tier)              │
   └─────────────────────────────────────────────┘
   ```

3. Implement spending logic:
   ```python
   def unlock_feature(feature_id, game_state):
       cost = UNLOCKS[feature_id]["cost"]
       if game_state["reputation"]["unlock_tokens"] >= cost:
           game_state["reputation"]["unlock_tokens"] -= cost
           game_state["unlocked_features"].append(feature_id)
   ```

---

### **🎯 Key Design Decisions (APPROVED)**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Client vs Company Weight** | 60% / 40% | Client satisfaction is primary, but company needs matter too |
| **Tokens per Weekly Task** | 2 tokens | Consistent progress without grind (3 tasks = 6 tokens/week) |
| **Unlock Feature Cost** | 5-15 tokens | 2-5 weeks of effort per unlock (meaningful progression) |
| **Company Rep Components** | 3 (no Innovation) | Keep it simple: Tasks + Sales + Professionalism |
| **Tier Names** | Trainee → Junior → Regular → Senior → Expert → Master | Clear career progression narrative |
| **Progression Speed** | 1 tier/week target | Achievable with consistent play, not too fast/slow |
| **Number of Tiers** | 6 | Enough for 8-week scenario + room for overachievers |

---

## �📚 Resources & References

**Game design patterns:**
- Quest systems (World of Warcraft, Skyrim)
- Daily challenges (mobile games: Candy Crush, Clash of Clans)
- Achievement hunting (Steam, Xbox)
- Progress tracking (Duolingo, Habitica)

**Sales training integration:**
- SPIN Selling tasks
- Challenger Sale exercises
- Consultative selling practice
- Objection handling drills

**Real-world inspiration:**
- Sales contests (real companies do this!)
- Territory management KPIs
- CRM task management (Salesforce, HubSpot)
- Field sales apps (Repsly, RepSpark)

---

## 🎯 Next Actions

**Immediate (Phase 1):**
1. ✅ Create `data/tasks.py` with weekly task definitions
2. ✅ Implement auto-check logic in `fmcg_playable.py`
3. ✅ Build task progress UI in Dashboard → Zadania
4. ✅ Test task assignment and completion flow
5. ✅ Add reward payout system

**Short-term (Phase 2 prep):**
- Design story arc for Heinz scenario (4 chapters)
- Create NPC system (Paweł, Anna, Mentor)
- Plan milestone task progression
- Design achievement badges

**Long-term (Phase 3+):**
- Research AI task generation
- Prototype multiplayer tasks
- Design event calendar system
- Build analytics dashboard

---

**Status:** 🟢 Active development  
**Last updated:** 4 listopada 2025  
**Next review:** Po implementacji Phase 1
