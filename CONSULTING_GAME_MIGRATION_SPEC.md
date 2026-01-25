# CONSULTING GAME - Szczegółowa Specyfikacja Migracji (Streamlit → Next.js v3)

## 📋 Spis treści
1. [Przegląd Gry](#przegląd-gry)
2. [Struktura Danych](#struktura-danych)
3. [Mechanika Gry](#mechanika-gry)
4. [System Kontraktów](#system-kontraktów)
5. [System Pracowników](#system-pracowników)
6. [System Biur](#system-biur)
7. [System Wydarzeń](#system-wydarzeń)
8. [System Rankingów](#system-rankingów)
9. [System Finansowy](#system-finansowy)
10. [Pliki do Migracji](#pliki-do-migracji)
11. [Plan Migracji](#plan-migracji)

---

## 📖 Przegląd Gry

### Koncepcja
**Consulting Game** to symulacja prowadzenia firmy konsultingowej w obszarze CIQ (Conflict Resolution, Executive Coaching, Culture Transformation).

### Cel Gracza
- Rozwinąć firmę od Solo Consultanta → CIQ Empire (10 poziomów)
- Realizować kontrakty dla klientów
- Zarządzać pracownikami i biurem
- Zdobywać reputację i budować pozycję w rankingu

### Kluczowe Metryki
- **DegenCoins** (waluta główna) - przechowywana w `user_data['degencoins']`
- **Reputacja** (reputation) - wpływa na dostęp do lepszych kontraktów
- **Poziom Firmy** (1-10) - określa skalę działalności
- **Overall Score** - ranking graczy

### Tryby Gry
- **Career Mode**: Gracz rozwija swoją firmę konsultingową
- **Sandbox**: Wolna gra bez ograniczeń (przyszłość)

---

## 🗄️ Struktura Danych

### Lokalizacja
```python
user_data["business_games"]["consulting"] = {
    # Cała struktura gry Consulting
}
```

### Pełna Struktura JSON

```json
{
  "firm": {
    "name": "Nazwa Firmy",
    "logo": "🏢",
    "founded": "2025-01-15",
    "level": 1,
    "reputation": 50
  },
  
  "employees": [
    {
      "id": "emp_001",
      "type": "junior",
      "hired_at": "2025-01-20 14:30:00",
      "daily_cost": 50
    }
  ],
  
  "office": {
    "type": "home_office",
    "upgraded_at": null
  },
  
  "contracts": {
    "active": [
      {
        "id": "CIQ-EASY-001",
        "accepted_at": "2025-01-25 10:00:00",
        "deadline": "2025-01-26 23:59:59",
        "status": "in_progress"
      }
    ],
    "completed": [
      {
        "id": "CIQ-EASY-002",
        "rating": 5,
        "reward": 350,
        "reputation_gained": 15,
        "completed_at": "2025-01-24 18:30:00",
        "submission": "Treść odpowiedzi gracza..."
      }
    ],
    "available_pool": [
      {
        "id": "CIQ-MEDIUM-010",
        "tytul": "Tytuł kontraktu",
        "kategoria": "Coaching",
        "klient": "TechCorp"
      }
    ],
    "last_refresh": "2025-01-25 09:00:00"
  },
  
  "stats": {
    "total_revenue": 15000,
    "total_costs": 3500,
    "net_profit": 11500,
    "contracts_completed": 24,
    "contracts_5star": 10,
    "contracts_4star": 8,
    "contracts_3star": 4,
    "contracts_2star": 2,
    "contracts_1star": 0,
    "avg_rating": 4.17,
    "category_stats": {
      "Konflikt": {
        "completed": 5,
        "total_earned": 3000,
        "avg_rating": 4.2
      },
      "Coaching": {...},
      "Kultura": {...},
      "Kryzys": {...},
      "Leadership": {...}
    },
    "last_30_days": {
      "revenue": 5000,
      "contracts": 8,
      "avg_rating": 4.5
    },
    "last_7_days": {
      "revenue": 1200,
      "contracts": 2,
      "avg_rating": 5.0
    }
  },
  
  "ranking": {
    "overall_score": 1542.5,
    "current_positions": {
      "overall": 3,
      "revenue": 5,
      "quality": 2,
      "productivity_30d": 4
    },
    "previous_positions": {
      "overall": 4,
      "revenue": 6
    },
    "badges": ["early_adopter", "quality_master"],
    "position_history": [
      {
        "date": "2025-01-20",
        "overall": 8,
        "score": 450.0
      }
    ]
  },
  
  "events": {
    "history": [
      {
        "id": "event_003",
        "type": "positive",
        "title": "Polecenie od klienta",
        "description": "...",
        "effects": {
          "reputation": 10,
          "coins": 500
        },
        "timestamp": "2025-01-23 14:00:00",
        "manual_roll": false
      }
    ],
    "last_auto_event": "2025-01-25 09:00:00",
    "last_manual_roll": "2025-01-24 15:30:00",
    "active_effects": [
      {
        "name": "Boost marketingowy",
        "effect_type": "reputation_boost",
        "value": 0.2,
        "expires_at": "2025-01-27 00:00:00"
      }
    ]
  },
  
  "history": {
    "transactions": [
      {
        "type": "contract_reward",
        "amount": 350,
        "description": "Kontrakt CIQ-EASY-001 (5★)",
        "timestamp": "2025-01-24 18:30:00"
      },
      {
        "type": "daily_costs",
        "amount": -150,
        "description": "Koszty dzienne (1 pracownik + biuro)",
        "timestamp": "2025-01-25 00:00:00"
      }
    ],
    "level_ups": [
      {
        "from_level": 1,
        "to_level": 2,
        "timestamp": "2025-01-22 16:00:00"
      }
    ],
    "employees": [
      {
        "action": "hired",
        "employee_type": "junior",
        "cost": 500,
        "timestamp": "2025-01-20 14:30:00"
      }
    ],
    "offices": [
      {
        "office_type": "Home Office",
        "cost": 0,
        "capacity": 1,
        "date": "2025-01-15 10:00:00"
      }
    ],
    "milestones": [
      {
        "type": "founded",
        "title": "Założenie firmy",
        "description": "🎉 Firma została założona!",
        "date": "2025-01-15 10:00:00"
      }
    ]
  }
}
```

---

## ⚙️ Mechanika Gry

### 1. Inicjalizacja Gry

**Funkcja:** `initialize_business_game(username)`  
**Plik:** `utils/business_game.py` (linia 185)

**Co się dzieje:**
- Tworzy początkową strukturę danych
- Ustawia poziom 1 (Solo Consultant)
- Ustawia startową reputację (50)
- Home Office jako pierwsze biuro
- Puste listy pracowników i kontraktów

**Ważne:**
- Monety (`degencoins`) są w `user_data['degencoins']`, NIE w strukturze gry!
- Każda gra ma własny `industry_id` (tutaj: `"consulting"`)

### 2. Cykl Rozgrywki

```
1. ODŚWIEŻENIE KONTRAKTÓW (refresh_contract_pool)
   ↓
2. WYDARZENIE DZIENNE (20% szansa)
   ↓
3. GRACZ WYBIERA AKCJĘ:
   - Przyjęcie kontraktu
   - Zatrudnienie pracownika
   - Upgrade biura
   - Ręczne losowanie wydarzenia
   ↓
4. REALIZACJA KONTRAKTÓW
   - Submit solution
   - Ocena AI (1-5 gwiazdek)
   - Nagroda + reputacja
   ↓
5. SPRAWDZENIE DEADLINE
   - Kary za spóźnienie (-50% nagrody, -20 reputacji)
   ↓
6. CODZIENNE KOSZTY (00:00)
   - Pracownicy (50-180 zł/dzień każdy)
   - Biuro (0-400 zł/dzień)
   ↓
7. AWANS POZIOMU (jeśli warunki spełnione)
   - Monety + reputacja w zakresie
   ↓
8. AKTUALIZACJA RANKINGU
```

### 3. System Poziomów Firmy

**Źródło:** `FIRM_LEVELS` w `data/business_data.py`

| Poziom | Nazwa | Zakres Monet | Reputacja | Max Pracowników | Kontrakty/Dzień |
|--------|-------|-------------|-----------|----------------|----------------|
| 1 | Solo Consultant | 0-2000 | - | 0 | 1 |
| 2 | Boutique Consulting | 2000-5000 | - | 2 | 1 |
| 3 | CIQ Advisory | 5000-10000 | - | 3 | 1 |
| 4 | Strategic Partners | 10000-20000 | - | 5 | 2 |
| 5 | Elite Consulting Group | 20000-35000 | - | 7 | 2 |
| 6 | Regional CIQ Leaders | 35000-55000 | - | 10 | 2 |
| 7 | National CIQ Authority | 55000-80000 | - | 15 | 3 |
| 8 | Global CIQ Partners | 80000-120000 | - | 20 | 3 |
| 9 | Worldwide CIQ Corporation | 120000-180000 | - | 30 | 4 |
| 10 | CIQ Empire | 180000+ | - | 50 | 5 |

**Warunki Awansu:**
```python
# user_data['degencoins'] + reputation musi być w zakresie poziomu
# Awans jest automatyczny przy spełnieniu warunków
```

### 4. System Ponawiania Kontraktów

**Częstotliwość:** Co 24h od ostatniego odświeżenia

**Algorytm:**
```python
def refresh_contract_pool(bg_data):
    # 1. Usuń przeterminowane oferty (>24h)
    # 2. Dopełnij pulę do 5-8 kontraktów
    # 3. Filtruj kontrakty po poziomie gracza
    # 4. Losowe 50% szans na Premium (jeśli rep >= 80)
    # 5. Zapisz timestamp refresh
```

**Typy kontraktów w puli:**
- **Standard** (💼): Podstawowe kontrakty
- **Premium** (⭐): Wymagają reputacji 80+, lepsze nagrody
- **AI Conversation** (💬): Rozmowy z NPC (TTS)
- **Speed Challenge** (⚡): Czasowe wyzwania

---

## 📋 System Kontraktów

### Kategorie

| Kategoria | Opis | Ikona |
|-----------|------|-------|
| **Leadership** | Coaching menedżerski, rozmowy 1:1 | 👔 |
| **Konflikt** | Mediacje, rozwiązywanie sporów | ⚔️ |
| **Coaching** | Executive coaching, rozwój liderów | 🎯 |
| **Kultura** | Zmiana organizacyjna, wartości | 🛡️ |
| **Kryzys** | Crisis management, reputacja | 🚨 |

### Poziomy Trudności

| Trudność | Min Słów | Czas (dni) | Nagroda Base | Premium Unlock |
|----------|----------|------------|--------------|----------------|
| 1 (Łatwe) | 20-50 | 1 | 200-350 | - |
| 2 (Średnie) | 50-100 | 1-2 | 500-800 | Rep 60+ |
| 3 (Trudne) | 100-200 | 2-3 | 1000-1500 | Rep 70+ |
| 4 (Bardzo Trudne) | 150-300 | 3-4 | 2000-3000 | Rep 80+ |
| 5 (Eksperckie) | 200+ | 4-5 | 3500-5000 | Rep 90+ |

### Struktura Kontraktu (Baza Danych)

```python
{
    "id": "CIQ-EASY-001",
    "tytul": "Krótka rozmowa 1:1 z pracownikiem",
    "kategoria": "Leadership",
    "klient": "LocalCafe",
    "opis": "Opis sytuacji klienta...",
    "zadanie": "Co ma zrobić gracz (markdown)...",
    "wymagana_wiedza": ["Podstawy komunikacji"],
    "trudnosc": 1,
    "nagroda_base": 200,       # 2-3 gwiazdki
    "nagroda_4star": 250,       # 4 gwiazdki
    "nagroda_5star": 350,       # 5 gwiazdek
    "reputacja": 15,            # Bonus reputacji
    "czas_realizacji_dni": 1,
    "wymagany_poziom": 1,
    "min_slow": 20,             # Min słów w odpowiedzi
    "emoji": "☕"
}
```

### Flow Kontraktu

```
1. DOSTĘPNY W PULI
   - Gracz widzi w zakładce "Kontrakty"
   - Może zaakceptować (limit dzienny!)
   ↓
2. AKTYWNY (IN_PROGRESS)
   - accepted_at + deadline
   - Gracz wypełnia formularz rozwiązania
   ↓
3. SUBMIT SOLUTION
   - Walidacja (min_slow słów)
   - Ocena AI (1-5 gwiazdek) lub ręczna
   ↓
4. UKOŃCZONY (COMPLETED)
   - Nagroda monet
   - Nagroda reputacji
   - Aktualizacja statystyk
   - Event log
```

### Algorytm Oceny AI (OpenAI)

**Funkcja:** `evaluate_contract_with_ai(contract, submission, user_data)`

**Kryteria:**
- **Kompletność** (30%): Czy odpowiada na wszystkie pytania
- **Wiedza merytoryczna** (30%): Poprawność rozwiązań
- **Praktyczność** (20%): Wykonalność w realnym biznesie
- **Struktura** (20%): Czytelność, format

**Wynik:**
```json
{
  "rating": 4,  // 1-5 gwiazdek
  "feedback": "Bardzo dobre rozwiązanie! Mocne strony: ..."
}
```

### Deadline & Penalties

```python
# Sprawdzane w show_dashboard_tab()
if datetime.now() > deadline:
    # Kara:
    # - Nagroda * 0.5 (50% mniej)
    # - Reputacja -20
    # - Status: "late"
```

---

## 👥 System Pracowników

### Typy Pracowników

**Źródło:** `EMPLOYEE_TYPES` w `data/business_data.py`

| Typ | Koszt Zatrudnienia | Koszt Dzienny | Bonus | Wymagany Poziom |
|-----|-------------------|---------------|-------|----------------|
| **Junior Consultant** | 500 | 50 | +1 kontrakt/dzień | 1 |
| **Conflict Specialist** | 1500 | 120 | +25% zarobków (Konflikt) | 2 |
| **Executive Coach** | 2000 | 150 | +30% zarobków (Coaching) | 2 |
| **Culture Lead** | 1800 | 140 | +25% zarobków (Kultura) | 3 |
| **Crisis Expert** | 2500 | 180 | +35% zarobków (Kryzys) | 3 |
| **Operations Manager** | 1200 | 100 | -15% kosztów pracowników | 2 |

### Mechanika Zatrudnienia

```python
def hire_employee(bg_data, user_data, employee_type):
    # 1. Sprawdź limit miejsca (biuro + poziom firmy)
    # 2. Sprawdź koszty (user_data['degencoins'])
    # 3. Dodaj do bg_data['employees']
    # 4. Odejmij monety
    # 5. Zapisz event w history
```

### Bonusy Specjalistów

**Category Boost:**
```python
# Przykład: Executive Coach (+30% Coaching)
if employee_type == "executive_coach" and contract_category == "Coaching":
    final_reward = base_reward * 1.30
```

**Cost Reduction:**
```python
# Operations Manager (-15% kosztów pracowników)
total_daily_costs = sum(emp_costs) * 0.85
```

**Capacity Boost:**
```python
# Junior Consultant (+1 kontrakt/dzień)
daily_limit = base_limit + count_juniors
```

### Zwolnienie Pracownika

```python
def fire_employee(bg_data, employee_id):
    # Brak kosztów zwolnienia
    # Natychmiastowe usunięcie z listy
    # Event w history
```

---

## 🏢 System Biur

### Typy Biur

**Źródło:** `OFFICE_TYPES` w `data/business_data.py`

| Typ | Max Pracowników | Koszt Dzienny | Koszt Upgrade | Bonus Reputacji |
|-----|----------------|---------------|---------------|----------------|
| **Home Office** | 2 | 0 | - | 0 |
| **Small Office** | 5 | 50 | 1000 | +5 |
| **Medium Office** | 10 | 100 | 3000 | +15 |
| **Large Office** | 20 | 200 | 7000 | +30 |
| **Headquarters** | 50 | 400 | ∞ (max) | +50 |

### Ścieżka Upgradu

```python
OFFICE_UPGRADE_PATH = [
    "home_office",
    "small_office", 
    "medium_office",
    "large_office",
    "headquarters"
]
```

**Nie można przeskoczyć poziomów!**

### Mechanika Upgradu

```python
def upgrade_office(bg_data, user_data):
    current = bg_data['office']['type']
    current_idx = OFFICE_UPGRADE_PATH.index(current)
    next_office = OFFICE_UPGRADE_PATH[current_idx + 1]
    
    cost = OFFICE_TYPES[next_office]['koszt_ulepszenia']
    
    # Sprawdź monety
    # Odejmij koszt
    # Zmień typ biura
    # Dodaj bonus reputacji
    # Event w history
```

---

## 🎲 System Wydarzeń

### Typy Wydarzeń

**Źródło:** `data/events.json` (lub `utils/business_game_events.py`)

| Typ | Opis | Przykłady |
|-----|------|-----------|
| **Positive** | Korzyści dla firmy | Polecenie klienta (+500 monet), Grant (+1000) |
| **Negative** | Koszty/straty | Awaria IT (-300), Utrata klienta (-500) |
| **Neutral** | Wybór gracza | Inwestycja w marketing vs szkolenie |

### Struktura Wydarzenia

```json
{
  "id": "event_003",
  "type": "positive",
  "title": "Polecenie od zadowolonego klienta",
  "description": "Jeden z klientów polecił...",
  "icon": "🌟",
  "probability": 0.15,  // 15% szansa
  "effects": {
    "coins": 500,
    "reputation": 10
  },
  "choices": null  // Tylko dla neutral
}
```

### Mechanika Losowania

**Automatyczne (raz dziennie):**
```python
# W show_dashboard_tab()
if last_auto_event != today:
    event = get_random_event(bg_data)  # 20% base chance
    if event:
        apply_event_effects(event)
        bg_data['events']['last_auto_event'] = today
```

**Ręczne (cooldown 24h):**
```python
# Przycisk "Losuj Wydarzenie" w Dashboard
if can_manually_roll:
    event = get_random_event(bg_data)
    bg_data['events']['last_manual_roll'] = now
```

### Neutral Events (Wybory)

```json
{
  "type": "neutral",
  "choices": [
    {
      "id": "invest_marketing",
      "label": "Inwestuj w marketing (-1000 monet)",
      "effects": {"coins": -1000, "reputation": 15}
    },
    {
      "id": "invest_training",
      "label": "Szkolenie zespołu (-800 monet)",
      "effects": {"coins": -800, "employee_boost": 0.1}
    }
  ]
}
```

**UI:** Modal z wyborem → `apply_event_effects(event_id, choice_id)`

### Active Effects (Buffs/Debuffs)

```python
# Przykład: Boost marketingowy na 3 dni
{
  "name": "Marketing Boost",
  "effect_type": "reputation_boost",
  "value": 0.2,  // +20% reputacji
  "expires_at": "2025-01-28 00:00:00"
}
```

**Sprawdzanie:**
```python
# Przed każdą operacją
active_effects = [e for e in bg_data['events']['active_effects'] 
                  if datetime.now() < e['expires_at']]
```

---

## 🏆 System Rankingów

### Overall Score Formula

```python
def calculate_overall_score(bg_data, user_data):
    score = 0
    
    # 1. Kapitał (40% wagi)
    score += user_data['degencoins'] * 0.5
    
    # 2. Reputacja (20% wagi)
    score += bg_data['firm']['reputation'] * 2.0
    
    # 3. Jakość pracy (25% wagi)
    avg_rating = bg_data['stats']['avg_rating']
    score += (avg_rating / 5.0) * 500
    
    # 4. Produktywność 30 dni (15% wagi)
    last_30d_revenue = bg_data['stats']['last_30_days']['revenue']
    score += last_30d_revenue * 0.1
    
    return round(score, 2)
```

### Kategorie Rankingu

| Kategoria | Opis | Sortowanie |
|-----------|------|------------|
| **Overall** | Overall Score | DESC |
| **Revenue** | Total Revenue | DESC |
| **Quality** | Avg Rating | DESC |
| **Productivity 30d** | Revenue (30 dni) | DESC |

### Position History

```python
# Zapisywane codziennie (w bg_data['ranking']['position_history'])
{
  "date": "2025-01-25",
  "overall": 5,
  "score": 1200.5
}
```

**Wykresy:**
- Pozycja w czasie (liniowy)
- Zmiana score (area chart)

### Badges (Odznaki)

```python
BADGES = {
    "early_adopter": "🎖️ Wczesny Gracz",
    "quality_master": "⭐ Mistrz Jakości (avg 4.5+)",
    "revenue_king": "💰 Król Przychodów (100k+)",
    "empire_builder": "👑 Budowniczy Imperium (poziom 10)"
}
```

---

## 💰 System Finansowy

### Waluta: DegenCoins

**Lokalizacja:** `user_data['degencoins']` (GLOBALNIE, nie w bg_data!)

**Źródła dochodu:**
- Kontrakty (200-5000 zł zależnie od trudności i oceny)
- Wydarzenia pozytywne (+500-2000)
- Bonusy

**Wydatki:**
- Zatrudnienie pracowników (500-2500 jednorazowo)
- Upgrade biura (1000-7000)
- Koszty dzienne (50-400/dzień)

### Transakcje (History)

```python
bg_data['history']['transactions'] = [
    {
        "type": "contract_reward",
        "amount": 350,
        "description": "Kontrakt CIQ-EASY-001 (5★)",
        "timestamp": "2025-01-24 18:30:00"
    },
    {
        "type": "daily_costs",
        "amount": -150,
        "description": "Pracownicy (1) + Biuro",
        "timestamp": "2025-01-25 00:00:00"
    },
    {
        "type": "employee_hire",
        "amount": -500,
        "description": "Zatrudnienie Junior Consultant",
        "timestamp": "2025-01-20 14:30:00"
    }
]
```

### Koszty Dzienne

**Funkcja:** `calculate_total_daily_costs(bg_data)`

```python
# Pracownicy
employee_costs = sum([emp['daily_cost'] for emp in employees])

# Operations Manager (-15% kosztów)
if has_operations_manager:
    employee_costs *= 0.85

# Biuro
office_cost = OFFICE_TYPES[office_type]['koszt_dzienny']

total = employee_costs + office_cost
```

**Moment naliczania:** Midnight (00:00) - automatycznie w kolejnym wejściu

### Statystyki Finansowe

```python
bg_data['stats'] = {
    "total_revenue": 25000,     # Suma nagród
    "total_costs": 5000,        # Suma wydatków
    "net_profit": 20000,        # revenue - costs
    
    "last_30_days": {
        "revenue": 8000
    },
    "last_7_days": {
        "revenue": 2500
    }
}
```

---

## 📂 Pliki do Migracji

### 1. Backend (Python)

| Plik | Ścieżka | Odpowiedzialność |
|------|---------|------------------|
| **business_data.py** | `data/business_data.py` | Dane statyczne (poziomy, pracownicy, kontrakty) |
| **business_game.py** | `utils/business_game.py` | Logika gry (inicjalizacja, kontrakty, pracownicy) |
| **business_game_events.py** | `utils/business_game_events.py` | System wydarzeń losowych |
| **users_sql.py** | `data/users_sql.py` | Zapis/odczyt user_data |
| **scenarios.py** | `data/scenarios.py` | Scenariusze gier (nie krytyczne dla Consulting) |

### 2. Frontend (Streamlit → Next.js)

| Component | Obecny Plik | Docelowy Komponent (Next.js) |
|-----------|------------|------------------------------|
| **Home** | `views/business_games.py:show_business_games_home()` | `ConsultingHome.tsx` |
| **Dashboard** | `views/business_games.py:show_dashboard_tab()` | `ConsultingDashboard.tsx` |
| **Contracts** | `views/business_games.py:show_contracts_tab()` | `ConsultingContracts.tsx` |
| **Employees** | `views/business_games.py:show_employees_tab()` | `ConsultingEmployees.tsx` |
| **Office** | `views/business_games.py:show_office_tab()` | `ConsultingOffice.tsx` |
| **Rankings** | `views/business_games.py:show_hall_of_fame()` | `ConsultingRankings.tsx` |
| **Financial Reports** | `views/business_games.py:show_financial_reports_tab()` | `ConsultingReports.tsx` |

### 3. Komponenty Refactored (do przeniesienia)

| Component | Plik | Opis |
|-----------|------|------|
| **render_header()** | `views/business_games_refactored/components/headers.py` | Nagłówek z metrykami |
| **render_contract_card()** | `views/business_games_refactored/components/contract_card.py` | Karta kontraktu |
| **render_employee_card()** | `views/business_games_refactored/components/employee_card.py` | Karta pracownika |
| **create_financial_chart()** | `views/business_games_refactored/components/charts.py` | Wykres Plotly |
| **render_active_event_card()** | `views/business_games_refactored/components/event_card.py` | Karta wydarzenia |

### 4. Dane Statyczne (JSON/Const)

```
data/
├── business_games/
│   ├── contracts.json          # Baza kontraktów CIQ
│   ├── events.json              # Wydarzenia losowe
│   ├── firm_levels.json         # Poziomy firmy
│   ├── employee_types.json      # Typy pracowników
│   └── office_types.json        # Typy biur
```

---

## 🚀 Plan Migracji

### Faza 1: Backend API (Python FastAPI)

**Cel:** Przeniesienie logiki biznesowej do Python backend

#### 1.1. Endpoints API

```python
# v3/backend/routers/consulting.py

POST   /api/consulting/initialize          # Nowa gra
GET    /api/consulting/game                # Pobierz dane gry
POST   /api/consulting/contracts/refresh   # Odśwież pulę
POST   /api/consulting/contracts/accept    # Zaakceptuj kontrakt
POST   /api/consulting/contracts/submit    # Submit rozwiązania
POST   /api/consulting/employees/hire      # Zatrudnij pracownika
DELETE /api/consulting/employees/{id}      # Zwolnij pracownika
POST   /api/consulting/office/upgrade      # Upgrade biura
POST   /api/consulting/events/roll         # Ręczne losowanie
GET    /api/consulting/rankings            # Ranking graczy
GET    /api/consulting/stats               # Statystyki firmy
```

#### 1.2. Modele Pydantic

```python
# v3/backend/models/consulting.py

class FirmData(BaseModel):
    name: str
    logo: str
    founded: str
    level: int
    reputation: int

class Employee(BaseModel):
    id: str
    type: str
    hired_at: str
    daily_cost: int

class ContractInPool(BaseModel):
    id: str
    tytul: str
    kategoria: str
    klient: str
    trudnosc: int
    nagroda_base: int
    # ... pełna struktura

class GameState(BaseModel):
    firm: FirmData
    employees: List[Employee]
    office: OfficeData
    contracts: ContractsData
    stats: StatsData
    ranking: RankingData
    events: EventsData
    history: HistoryData
```

#### 1.3. Migracja Funkcji

```python
# Przeniesienie z utils/business_game.py → backend/services/consulting_service.py

def initialize_game(user_id: str) -> GameState
def refresh_contracts(game_state: GameState) -> GameState
def accept_contract(game_state: GameState, contract_id: str) -> GameState
def submit_contract(game_state: GameState, contract_id: str, submission: str) -> dict
def hire_employee(game_state: GameState, employee_type: str) -> GameState
def calculate_daily_costs(game_state: GameState) -> int
def check_level_up(game_state: GameState, user_coins: int) -> GameState
```

### Faza 2: Frontend Components (Next.js/React)

#### 2.1. Struktura Folderów

```
v3/frontend/src/
├── app/
│   └── consulting/
│       ├── page.tsx                    # Routing główny
│       ├── dashboard/page.tsx
│       ├── contracts/page.tsx
│       ├── employees/page.tsx
│       └── rankings/page.tsx
│
├── components/
│   └── consulting/
│       ├── ConsultingHeader.tsx        # Nagłówek z metrykami
│       ├── ContractCard.tsx            # Karta kontraktu
│       ├── ContractSubmitForm.tsx      # Formularz rozwiązania
│       ├── EmployeeCard.tsx            # Karta pracownika
│       ├── EmployeeHireModal.tsx       # Modal zatrudnienia
│       ├── OfficeUpgradePanel.tsx      # Panel upgrade biura
│       ├── EventCard.tsx               # Karta wydarzenia
│       ├── FinancialChart.tsx          # Wykres finansowy (Recharts)
│       ├── RankingTable.tsx            # Tabela rankingu
│       └── StatsPanel.tsx              # Panel statystyk
│
├── hooks/
│   └── consulting/
│       ├── useConsultingGame.ts        # Główny hook gry
│       ├── useContracts.ts             # Hook kontraktów
│       ├── useEmployees.ts             # Hook pracowników
│       └── useRankings.ts              # Hook rankingów
│
├── types/
│   └── consulting.ts                   # TypeScript interfaces
│
└── lib/
    └── api/
        └── consulting.ts               # API client
```

#### 2.2. TypeScript Interfaces

```typescript
// v3/frontend/src/types/consulting.ts

export interface FirmData {
  name: string
  logo: string
  founded: string
  level: number
  reputation: number
}

export interface Employee {
  id: string
  type: string
  hired_at: string
  daily_cost: number
}

export interface Contract {
  id: string
  tytul: string
  kategoria: string
  klient: string
  opis: string
  zadanie: string
  trudnosc: number
  nagroda_base: number
  nagroda_4star: number
  nagroda_5star: number
  reputacja: number
  czas_realizacji_dni: number
  min_slow: number
  emoji: string
}

export interface GameState {
  firm: FirmData
  employees: Employee[]
  office: OfficeData
  contracts: {
    active: ActiveContract[]
    completed: CompletedContract[]
    available_pool: Contract[]
    last_refresh: string
  }
  stats: StatsData
  ranking: RankingData
  events: EventsData
  history: HistoryData
}
```

#### 2.3. API Client

```typescript
// v3/frontend/src/lib/api/consulting.ts

export const consultingApi = {
  async getGame(): Promise<GameState> {
    const res = await fetch('/api/consulting/game')
    return res.json()
  },

  async acceptContract(contractId: string): Promise<GameState> {
    const res = await fetch('/api/consulting/contracts/accept', {
      method: 'POST',
      body: JSON.stringify({ contract_id: contractId })
    })
    return res.json()
  },

  async submitContract(contractId: string, submission: string) {
    const res = await fetch('/api/consulting/contracts/submit', {
      method: 'POST',
      body: JSON.stringify({ contract_id: contractId, submission })
    })
    return res.json()
  },

  // ... inne metody
}
```

#### 2.4. Custom Hooks

```typescript
// v3/frontend/src/hooks/consulting/useConsultingGame.ts

export function useConsultingGame() {
  const [gameState, setGameState] = useState<GameState | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadGame()
  }, [])

  async function loadGame() {
    const data = await consultingApi.getGame()
    setGameState(data)
    setLoading(false)
  }

  async function acceptContract(contractId: string) {
    const updated = await consultingApi.acceptContract(contractId)
    setGameState(updated)
  }

  return {
    gameState,
    loading,
    acceptContract,
    // ... inne metody
  }
}
```

### Faza 3: UI Components

#### 3.1. Dashboard

```tsx
// v3/frontend/src/app/consulting/dashboard/page.tsx

export default function ConsultingDashboard() {
  const { gameState, loading } = useConsultingGame()
  const { latestEvent, rollEvent } = useEvents()

  if (loading) return <LoadingSpinner />

  return (
    <div className="consulting-dashboard">
      <ConsultingHeader firm={gameState.firm} stats={gameState.stats} />
      
      <div className="grid grid-cols-2 gap-4">
        {/* Dzisiejsze Wydarzenie */}
        <EventCard event={latestEvent} type="auto" />
        
        {/* Ręczne Losowanie */}
        <EventRollPanel onRoll={rollEvent} />
      </div>

      {/* Aktywne Kontrakty */}
      <section>
        <h2>Aktywne Kontrakty</h2>
        {gameState.contracts.active.map(contract => (
          <ContractCard key={contract.id} contract={contract} />
        ))}
      </section>

      {/* Wykres Finansowy */}
      <FinancialChart data={gameState.history.transactions} />
    </div>
  )
}
```

#### 3.2. Contract Card

```tsx
// v3/frontend/src/components/consulting/ContractCard.tsx

export function ContractCard({ contract, type }: Props) {
  return (
    <Card className={cn(
      'contract-card',
      contract.kategoria.toLowerCase()
    )}>
      <CardHeader>
        <div className="flex items-center gap-2">
          <span className="text-3xl">{contract.emoji}</span>
          <div>
            <h3>{contract.tytul}</h3>
            <p className="text-sm text-muted">{contract.klient}</p>
          </div>
        </div>
        <Badge>{contract.kategoria}</Badge>
      </CardHeader>

      <CardContent>
        <p>{contract.opis}</p>
        
        <div className="rewards">
          <Coin amount={contract.nagroda_5star} label="5★" />
          <Star amount={contract.reputacja} />
        </div>

        <Progress 
          value={calculateTimeLeft(contract.deadline)} 
          label="Pozostały czas"
        />
      </CardContent>

      <CardFooter>
        {type === 'available' && (
          <Button onClick={() => onAccept(contract.id)}>
            Przyjmij Kontrakt
          </Button>
        )}
        {type === 'active' && (
          <Button variant="primary" onClick={() => onSubmit(contract.id)}>
            Wyślij Rozwiązanie
          </Button>
        )}
      </CardFooter>
    </Card>
  )
}
```

### Faza 4: Migracja Danych

#### 4.1. Struktura Bazy Danych

**PostgreSQL Tables:**

```sql
-- Users (już istnieje)
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username VARCHAR(100) UNIQUE,
  degencoins INT DEFAULT 1000,
  created_at TIMESTAMP
);

-- Consulting Games
CREATE TABLE consulting_games (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  game_data JSONB,  -- Cała struktura GameState
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Consulting Contracts Pool (statyczne)
CREATE TABLE consulting_contracts (
  id VARCHAR(50) PRIMARY KEY,
  data JSONB,  -- Pełna struktura kontraktu
  difficulty INT,
  category VARCHAR(50)
);

-- Ranking Cache (aktualizowany codziennie)
CREATE TABLE consulting_rankings (
  user_id UUID REFERENCES users(id),
  overall_score FLOAT,
  revenue FLOAT,
  quality FLOAT,
  productivity_30d FLOAT,
  updated_at TIMESTAMP
);
```

#### 4.2. Migracja z users_data.json

```python
# Skrypt migracji: migrate_consulting_to_db.py

import json
from v3.backend.database import get_db
from v3.backend.models.consulting import GameState

def migrate_users():
    with open('data/users_data.json') as f:
        users_data = json.load(f)
    
    db = get_db()
    
    for username, user_data in users_data.items():
        if 'business_games' in user_data:
            if 'consulting' in user_data['business_games']:
                consulting_data = user_data['business_games']['consulting']
                
                # Walidacja przez Pydantic
                game_state = GameState(**consulting_data)
                
                # Zapis do PostgreSQL
                db.execute("""
                    INSERT INTO consulting_games (user_id, game_data)
                    VALUES (%s, %s)
                """, (user_data['id'], game_state.dict()))
                
    db.commit()
```

### Faza 5: Testing

#### 5.1. Backend Tests

```python
# v3/backend/tests/test_consulting.py

def test_initialize_game():
    game = initialize_game("test_user")
    assert game.firm.level == 1
    assert game.firm.reputation == 50
    assert len(game.employees) == 0

def test_accept_contract():
    game = create_test_game()
    contract_id = "CIQ-EASY-001"
    
    updated = accept_contract(game, contract_id)
    assert len(updated.contracts.active) == 1
    assert updated.contracts.active[0].id == contract_id

def test_submit_contract():
    game = create_test_game_with_active_contract()
    submission = "Test solution with minimum 20 words..."
    
    result = submit_contract(game, "CIQ-EASY-001", submission)
    assert result['rating'] >= 1
    assert result['rating'] <= 5
```

#### 5.2. Frontend Tests

```typescript
// v3/frontend/src/__tests__/consulting.test.tsx

describe('ConsultingGame', () => {
  it('loads game state on mount', async () => {
    render(<ConsultingDashboard />)
    await waitFor(() => {
      expect(screen.getByText(/Solo Consultant/i)).toBeInTheDocument()
    })
  })

  it('accepts contract', async () => {
    const { user } = renderWithGame()
    const acceptButton = screen.getByText(/Przyjmij Kontrakt/i)
    
    await user.click(acceptButton)
    
    expect(screen.getByText(/Aktywne Kontrakty/i)).toBeInTheDocument()
  })
})
```

---

## 📊 Różnice vs FMCG

| Aspekt | Consulting | FMCG |
|--------|-----------|------|
| **Model gry** | Firma konsultingowa | Kariera w korporacji |
| **Metryki** | Monety + Reputacja | Sales + Market Share + CSAT |
| **Progresja** | 10 poziomów firmy | 10 poziomów kariery |
| **Zadania** | Kontrakty CIQ | Tasks (Field Sales, KAM) |
| **Zespół** | Pracownicy (zatrudnij/zwolnij) | Team (dostaniesz na poziomie 4+) |
| **Biuro** | Home → Headquarters | Nie ma (pracujesz w GlobalCPG) |
| **Wydarzenia** | Losowe (pozytywne/negatywne) | Podobnie |
| **Scenariusze** | Brak (tylko Career) | 3 scenariusze (Quick, Lifetime, Top) |

---

## ✅ Checklist Migracji

### Backend
- [ ] Stworzyć `v3/backend/routers/consulting.py`
- [ ] Przenieść funkcje z `utils/business_game.py`
- [ ] Stworzyć modele Pydantic
- [ ] Zaimplementować endpoints API
- [ ] Stworzyć tabele PostgreSQL
- [ ] Napisać skrypt migracji danych
- [ ] Testy jednostkowe backend

### Frontend
- [ ] Stworzyć TypeScript interfaces
- [ ] Stworzyć API client
- [ ] Zbudować komponenty UI
- [ ] Zaimplementować custom hooks
- [ ] Stworzyć routing (Next.js App Router)
- [ ] Testy komponentów (Vitest/Jest)

### Data
- [ ] Zmigrować kontrakty do PostgreSQL
- [ ] Zmigrować wydarzenia do JSON/DB
- [ ] Przenieść dane użytkowników (user_data.json → PostgreSQL)

### DevOps
- [ ] Deployment backend (Vercel Serverless Functions lub dedykowany serwer)
- [ ] Deployment frontend (Vercel)
- [ ] CI/CD pipeline
- [ ] Monitoring (Sentry, logging)

---

## 🎯 Podsumowanie

**Consulting Game** to kompleksowa symulacja biznesowa z:
- **10-poziomową progresją firmy** (Solo → Empire)
- **Systemem kontraktów CIQ** (5 kategorii, 5 poziomów trudności)
- **Zarządzaniem pracownikami** (6 typów specjalistów)
- **Systemem biur** (5 poziomów + bonusy)
- **Losowymi wydarzeniami** (automatyczne + ręczne)
- **Rankingiem graczy** (4 kategorie + overall score)
- **Rozwiniętą historiografią** (transakcje, level-upy, milestones)

**Główne wyzwanie migracji:**
- Przeniesienie logiki z Streamlit (synchronicznego) do Next.js (asynchronicznego)
- API-first approach (backend Python → frontend React)
- Zachowanie kompatybilności danych użytkowników

**Czas migracji (szacowany):** 3-4 tygodnie (1 dev)

---

**Ostatnia aktualizacja:** 2025-01-25
