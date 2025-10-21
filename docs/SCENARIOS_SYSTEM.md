# System Scenariuszy - Business Games Suite

## 📋 Przegląd

System scenariuszy pozwala na tworzenie różnych wariantów rozgrywki dla każdej branży w Business Games Suite. Każdy scenariusz ma unikalne warunki startowe, modyfikatory rozgrywki i cele do osiągnięcia.

## 🏗️ Architektura

### Struktura Plików

```
data/
  └── scenarios.py          # Definicje wszystkich scenariuszy
utils/
  └── business_game.py      # Logika inicjalizacji i obsługi scenariuszy
views/
  └── business_games.py     # UI wyboru scenariusza i wyświetlania celów
```

### Routing Wielopoziomowy

```
Level 1: Industry Selector
   ↓
Level 2: Scenario Selector (NOWE!)
   ↓
Level 3: Game View
```

## 📊 Struktura Danych Scenariusza

Każdy scenariusz definiowany w `data/scenarios.py` zawiera:

```python
{
    "id": "scenario_id",
    "name": "Nazwa Scenariusza",
    "description": "Opis scenariusza...",
    "icon": "🚀",
    "difficulty": "medium",  # easy/medium/hard/expert
    
    "initial_conditions": {
        "money": 50000,           # Kapitał startowy (może być ujemny!)
        "reputation": 50,
        "employees": [],          # Lista początkowych pracowników
        "office_type": "home_office",
        "contracts_in_progress": []  # Przejęte kontrakty (opcjonalne)
    },
    
    "modifiers": {
        "reputation_gain_multiplier": 1.0,    # Mnożnik wzrostu reputacji
        "revenue_multiplier": 1.0,             # Mnożnik przychodów
        "cost_multiplier": 1.0,                # Mnożnik kosztów
        "employee_salary_multiplier": 1.0,     # Mnożnik wynagrodzeń
        "contract_difficulty_adjustment": 0    # +/- do trudności kontraktów
    },
    
    "objectives": [
        {
            "type": "revenue_total",  # Typ celu
            "target": 1000000,        # Wartość docelowa
            "description": "Osiągnij 1M PLN przychodu",
            "reward_money": 50000     # Nagroda za ukończenie
        },
        # ... więcej celów
    ],
    
    "special_events": []  # Lista ID unikalnych eventów (TODO)
}
```

## 🎮 Implemented Scenarios

### Consulting

#### ⚖️ Standard Start
- **Trudność:** Medium
- **Budżet:** 50,000 PLN
- **Opis:** Klasyczny, zrównoważony start
- **Cele:** 3 cele (revenue, reputation, level)

#### 🚀 Startup Mode
- **Trudność:** Hard
- **Budżet:** 20,000 PLN (60% mniej!)
- **Reputacja:** 30 (40% mniej!)
- **Modyfikatory:**
  - +50% wzrost reputacji
  - -10% przychody
  - +20% koszty
  - +10% wynagrodzenia
- **Cele:** 4 ambitne cele

#### 💼 Corporate Rescue
- **Trudność:** Expert
- **Budżet:** -30,000 PLN (DŁUGI!)
- **Biuro:** Medium office (od razu)
- **Zespół:** Seniorzy (w przyszłości)
- **Modyfikatory:**
  - +30% wzrost reputacji
  - +40% przychody (doświadczony zespół)
  - +60% koszty (drogi zespół + biuro)
  - -10% trudność kontraktów
- **Cele:** 4 cele (wyjść na zero, odbudować reputację, high revenue)

### Pozostałe Branże

Każda branża (FMCG, Pharma, Banking, Insurance, Automotive) ma scenariusz **Standard** jako placeholder. Gotowe do rozbudowy!

## 🔧 Typy Celów

System obsługuje następujące typy celów:

| Typ | Opis | Przykład |
|-----|------|----------|
| `revenue_total` | Suma wszystkich przychodów | 1,000,000 PLN |
| `reputation` | Poziom reputacji | 80+ |
| `level` | Poziom firmy | Poziom 5 |
| `money` | Obecny stan konta | 0 (wyjść na zero) |
| `employees` | Liczba pracowników | 5 pracowników |

### Dodawanie Nowych Typów

Aby dodać nowy typ celu, zaktualizuj funkcję `check_objective_completion()` w `utils/business_game.py`:

```python
elif obj_type == "nowy_typ":
    current_value = # pobierz wartość
    return current_value >= target
```

I `get_objectives_summary()` dla wyświetlania postępu.

## 🎨 UI Components

### Ekran Wyboru Scenariusza

Funkcja: `show_scenario_selector(username, user_data, industry_id)`

- Grid 2 kolumny
- Karty scenariuszy z:
  - Ikoną i nazwą
  - Badge trudności (z kolorami)
  - Warunkami startowymi
  - Listą celów (max 3 + "... i X więcej")
  - Przyciskiem "Rozpocznij"

### Widget Celów na Dashboardzie

Funkcja: `show_dashboard_tab()` - sekcja "Cele Scenariusza"

- Expander z licznikiem (X/Y)
- Dla każdego celu:
  - Status (✅ ukończony / ⏳ w trakcie)
  - Nazwa i opis
  - Nagroda (jeśli jest)
  - Progress bar
  - Licznik postępu

### Auto-detection Ukończonych Celów

System automatycznie sprawdza cele przy każdym wejściu na Dashboard:
1. `update_objectives_progress()` sprawdza wszystkie cele
2. Nowo ukończone cele triggeru ją:
   - ✅ Success message
   - 💰 Przyznanie nagrody
   - 🎈 Balloons animation
   - 📝 Transakcja w historii

## 🔄 Backward Compatibility

### Migracja Starych Gier

Gry rozpoczęte przed implementacją scenariuszy automatycznie otrzymują scenariusz **"standard"** przy pierwszym załadowaniu:

```python
# W show_business_games() - auto-migration
if game_data and "scenario_id" not in game_data:
    scenario_id = get_default_scenario_id(industry_id)
    scenario = get_scenario(industry_id, scenario_id)
    
    game_data["scenario_id"] = scenario_id
    game_data["scenario_modifiers"] = scenario['modifiers']
    game_data["scenario_objectives"] = scenario['objectives']
    game_data["objectives_completed"] = []
    # ... save
```

### Struktura Danych w user_data

```python
user_data["business_games"]["consulting"] = {
    # METADATA SCENARIUSZA (NOWE)
    "scenario_id": "startup_mode",
    "scenario_modifiers": {...},
    "scenario_objectives": [...],
    "objectives_completed": ["obj_0", "obj_1"],
    "initial_money": 20000,
    
    # RESZTA JAK WCZEŚNIEJ
    "firm": {...},
    "employees": [...],
    # ...
}
```

## 🚀 Jak Dodać Nowy Scenariusz?

### Krok 1: Definicja w scenarios.py

```python
"consulting": {
    # ... istniejące scenariusze
    
    "my_new_scenario": {
        "id": "my_new_scenario",
        "name": "🌟 Mój Scenariusz",
        "description": "Opis...",
        "icon": "🌟",
        "difficulty": "medium",
        
        "initial_conditions": {
            "money": 30000,
            "reputation": 60,
            "employees": [],
            "office_type": "home_office"
        },
        
        "modifiers": {
            "reputation_gain_multiplier": 1.2,
            "revenue_multiplier": 1.0,
            "cost_multiplier": 0.9,
            "employee_salary_multiplier": 1.0,
            "contract_difficulty_adjustment": -5
        },
        
        "objectives": [
            {
                "type": "revenue_total",
                "target": 500000,
                "description": "Osiągnij 500K przychodu",
                "reward_money": 25000
            }
        ],
        
        "special_events": []
    }
}
```

### Krok 2: Test

1. Uruchom aplikację
2. Przejdź do Business Games
3. Wybierz branżę
4. Sprawdź czy nowy scenariusz pojawia się na liście
5. Rozpocznij grę i zweryfikuj warunki startowe

### Krok 3: Balancing

- Testuj trudność
- Dostosuj modyfikatory
- Upewnij się, że cele są osiągalne
- Zbieraj feedback

## 🎯 Możliwości Rozbudowy

### 1. Unikalne Wydarzenia dla Scenariuszy

```python
# W random_events.py
SCENARIO_EVENTS = {
    "startup_mode": [
        {
            "id": "investor_meeting",
            "title": "🤝 Spotkanie z Inwestorem",
            # ...
        }
    ]
}
```

### 2. Specjalne Mechaniki per Scenariusz

```python
# Np. dla "Corporate Rescue" - spłata długu w ratach
if scenario_id == "corporate_rescue":
    monthly_debt_payment = 5000
    # ... logika
```

### 3. Nagrody za Scenariusz

```python
# Odznaka za ukończenie wszystkich celów
if all_objectives_completed:
    unlock_badge(f"master_{scenario_id}")
    unlock_achievement(f"completed_{scenario_id}")
```

### 4. Scenariusze Sezonowe

```python
# Np. Świąteczny scenariusz w grudniu
"christmas_rush": {
    "available_from": "2025-12-01",
    "available_to": "2025-12-31",
    # ...
}
```

### 5. Difficulty Tiers

```python
# Odblokowywanie trudniejszych scenariuszy
if user_completed_scenario("standard"):
    unlock_scenario("startup_mode")
if user_completed_scenario("startup_mode"):
    unlock_scenario("corporate_rescue")
```

## 📝 TODO / Przyszłe Ulepszenia

- [ ] Unikalne wydarzenia dla każdego scenariusza
- [ ] System osiągnięć za ukończenie scenariuszy
- [ ] Leaderboard per scenariusz
- [ ] "New Game+" - restart z bonusami
- [ ] Scenariusze społecznościowe (community-created)
- [ ] Sandbox mode (custom scenario builder)
- [ ] Story mode z progresją scenariuszy
- [ ] Co-op scenarios (multiplayer)

## 🐛 Known Issues

- Brak walidacji czy cele są osiągalne
- Modyfikatory nie są jeszcze aplikowane do wszystkich mechanik (TODO: integrate with contract rewards, employee costs, etc.)
- Brak preview modyfikatorów na karcie scenariusza

## 📚 API Reference

### Funkcje w utils/business_game.py

```python
initialize_business_game_with_scenario(username, industry_id, scenario_id) -> Dict
apply_scenario_modifier(base_value, modifier_type, game_data) -> float
get_scenario_info(game_data) -> Optional[Dict]
check_objective_completion(game_data, user_data, objective) -> bool
update_objectives_progress(game_data, user_data) -> List[Dict]
get_objectives_summary(game_data, user_data) -> Dict
```

### Funkcje w data/scenarios.py

```python
get_scenario(industry_id, scenario_id) -> dict | None
get_available_scenarios(industry_id) -> dict
get_default_scenario_id(industry_id) -> str
```

## 💡 Tips for Game Designers

1. **Balance is Key:** Modyfikatory powinny się równoważyć (wyższe koszty = wyższe przychody)
2. **Clear Goals:** Cele powinny być konkretne i mierzalne
3. **Progressive Difficulty:** Łatwe cele na początku, trudniejsze na końcu
4. **Meaningful Rewards:** Nagrody powinny być proporcjonalne do trudności
5. **Narrative:** Każdy scenariusz powinien opowiadać historię

---

**Status:** ✅ Implementacja szkieletu ukończona (2025-01-21)
**Autor:** GitHub Copilot + pksia
**Wersja:** 1.0
