# 🔍 FMCG Simulator - Pre-Implementation Audit & Refactoring Plan

**Data:** 28 października 2025  
**Cel:** Ocena gotowości projektu do implementacji FMCG + plan refactoringu

---

## 📊 EXECUTIVE SUMMARY

### ✅ DOBRA WIADOMOŚĆ
- **SQL infrastructure GOTOWA!** (models.py, connection.py, repositories)
- **Business Games architecture SOLIDNA** (consulti ng działa, testowane)
- **Hybrydowy system JSON+SQL DZIAŁA** (UserRepository, BusinessGameRepository)
- **Migration scripts KOMPLETNE** (dry-run, rollback, validation)

### ⚠️ DO ZROBIENIA PRZED FMCG
1. **Migracja Business Games → SQL** (consulting obecnie w JSON)
2. **Refactoring game data structure** (niektóre redundancje)
3. **Standaryzacja API** (niektóre funkcje używają JSON bezpośrednio)
4. **Clean up deprecated code** (stare `business_game` vs nowe `business_games`)

### 🎯 REKOMENDACJA
**OPTION A (Bezpieczne):** Zmigruj consulting → SQL PRZED FMCG (2-3 dni)  
**OPTION B (Szybkie):** FMCG bezpośrednio w SQL, consulting migracja równolegle (5 dni)

**Polecam OPTION A** - lepiej mieć solidne fundamenty!

---

## 🗄️ AKTUALNY STAN BAZY DANYCH

### ✅ CO JUŻ MAMY (SQL)

#### 1. **User Model** - PRODUCTION READY ✅
```python
# database/models.py (linia 68-147)
class User(Base):
    __tablename__ = 'users'
    
    # ✅ Wszystkie pola zdefiniowane
    id, user_id, username, password_hash
    degen_type, xp, degencoins, level
    joined_date, last_login, test_taken
    created_at, updated_at
    
    # ✅ Metody konwersji
    to_dict() - SQL → JSON
    from_dict() - JSON → SQL
    update_from_dict() - UPDATE z JSON
```

**Status:** GOTOWY, używany w produkcji

---

#### 2. **BusinessGame Model** - PRODUCTION READY ✅
```python
# database/models.py (linia 245-364)
class BusinessGame(Base):
    __tablename__ = 'business_games'
    
    # ✅ Metadata
    id, user_id, scenario_type, scenario_id
    
    # ✅ Firm data
    firm_name, firm_logo, firm_founded
    firm_level, firm_reputation
    
    # ✅ Office
    office_type, office_upgraded_at
    
    # ✅ Financial
    money, initial_money
    
    # ✅ Scenario config
    scenario_modifiers (JSON)
    scenario_objectives (JSON)
    objectives_completed (JSON)
    
    # ✅ Ranking & Events
    ranking (JSON)
    events (JSON)
    
    # ✅ Timestamps
    created_at, updated_at
    
    # ✅ Relationships
    employees (1:N)
    contracts (1:N)
    transactions (1:N)
    stats (1:1)
```

**Status:** GOTOWY, testowany dla consulting

---

#### 3. **BusinessGameEmployee Model** - PRODUCTION READY ✅
```python
# database/models.py (linia 365-433)
class BusinessGameEmployee(Base):
    __tablename__ = 'business_game_employees'
    
    # ✅ Pola
    id, game_id (FK), employee_type
    hired_at, name
    
    # ✅ Metody
    to_dict() - SQL → JSON
    from_dict() - JSON → SQL
```

**Status:** GOTOWY

---

#### 4. **BusinessGameContract Model** - PRODUCTION READY ✅
```python
# database/models.py (linia 434-582)
class BusinessGameContract(Base):
    __tablename__ = 'business_game_contracts'
    
    # ✅ Metadata
    id, game_id (FK), contract_id, status
    
    # ✅ Contract details (WSZYSTKIE pola z consulting!)
    title, category, client, description, task
    difficulty, base_reward, reward_4star, reward_5star
    reputation, required_knowledge (JSON)
    duration_days, required_level, min_words, emoji
    
    # ✅ Lifecycle
    available_until, completed_at
    
    # ✅ Evaluation
    rating, earned_money, user_response, ai_feedback
    
    # ✅ Extra data (elastyczność!)
    extra_data (JSON) - dla FMCG-specific fields
    
    # ✅ Metody
    to_dict() - SQL → JSON
    from_dict() - JSON → SQL (z handling extra_data!)
```

**Status:** GOTOWY, wspiera rozszerzenia (extra_data)

---

#### 5. **BusinessGameTransaction Model** - PRODUCTION READY ✅
```python
# database/models.py (linia 583-657)
class BusinessGameTransaction(Base):
    __tablename__ = 'business_game_transactions'
    
    # ✅ Pola
    id, game_id (FK)
    transaction_date, transaction_type
    amount, description, balance_after
    
    # ✅ Metody
    to_dict() - SQL → JSON
    from_dict() - JSON → SQL
```

**Status:** GOTOWY

---

#### 6. **BusinessGameStats Model** - PRODUCTION READY ✅
```python
# database/models.py (linia 658-739)
class BusinessGameStats(Base):
    __tablename__ = 'business_game_stats'
    
    # ✅ Pola
    id, game_id (FK)
    total_revenue, total_costs
    contracts_completed, contracts_failed
    avg_rating, days_played
    best_category, worst_category
    current_streak, best_streak
    
    # ✅ Metody
    to_dict() - SQL → JSON
    from_dict() - JSON → SQL
```

**Status:** GOTOWY

---

### 📂 REPOSITORY LAYER - PRODUCTION READY ✅

#### 1. **UserRepository** - data/repositories/user_repository.py
```python
class UserRepository(BaseRepository):
    def __init__(self, backend="json")  # ✅ Hybrydowy!
    
    # ✅ CRUD
    get_user(username) - pobierz z JSON lub SQL
    save_user(username, user_data) - zapisz do JSON lub SQL
    update_user(username, updates) - UPDATE
    delete_user(username) - DELETE
    
    # ✅ Migracja
    _migrate_business_games_data() - fix missing fields
    
    # ✅ Backend switching
    _get_from_json() / _get_from_sql()
    _save_to_json() / _save_to_sql()
```

**Status:** PRODUCTION, używane w całym projekcie

---

#### 2. **BusinessGameRepository** - data/repositories/business_game_repository.py
```python
class BusinessGameRepository(BaseRepository):
    def __init__(self, backend="json")  # ✅ Hybrydowy!
    
    # ✅ CRUD
    get_scenario(username, scenario_type) - pobierz consulting/fmcg/etc
    save_scenario(username, scenario_type, data) - zapisz
    get_all_scenarios(username) - wszystkie scenariusze użytkownika
    delete_scenario(username, scenario_type) - usuń
    
    # ✅ Validation
    _validate_business_game_data() - sprawdź strukturę
    
    # ✅ Backend switching (oba backendy gotowe!)
    _get_from_json() / _get_from_sql()
    _save_to_json() / _save_to_sql()
    _get_all_from_json() / _get_all_from_sql()
```

**Status:** PRODUCTION READY, testowane

---

### 🔄 MIGRATION SCRIPTS - GOTOWE ✅

#### 1. **scripts/migration/migrate_business_games.py**
- Dry-run mode (walidacja bez zapisu)
- Live migration
- Validation
- Użyte na Max (consulting)

#### 2. **scripts/migration/migrate_all_users.py**
- Batch migration wszystkich użytkowników
- Fazy: 5 → 15 → reszta
- Stats tracking
- Rollback support

#### 3. **scripts/migration/test_sql_read.py**
- Test odczytu z SQL
- Weryfikacja danych

---

## 🚨 PROBLEM: CONSULTING W JSON, NIE SQL

### Aktualny Stan
```python
# users_data.json (przykład Max)
{
  "Max": {
    "username": "Max",
    "degencoins": 5420,
    "business_games": {
      "consulting": {   # ❌ TO JEST W JSON!
        "firm": {...},
        "employees": [...],
        "contracts": {
          "active": [...],
          "completed": [...]
        },
        "stats": {...},
        "history": {...}
      }
    }
  }
}
```

### Problem
1. **Consistency:** User data w SQL, business games w JSON = split brain
2. **Performance:** JSON file lock dla wielu userów
3. **Queries:** Nie możemy robić SQL queries po business games (ranking, stats)
4. **Backups:** JSON może się uszkodzić (mieliśmy 4 fix_json*.py!)
5. **FMCG:** Jeśli dodamy FMCG do JSON, problem się pogłębi

---

## 🎯 PLAN REFACTORINGU

### FAZA 1: MIGRACJA CONSULTING → SQL (2 dni)

#### Dzień 1: Dry-run & Validation
```bash
# 1. Test migracji użytkownika testowego
python scripts/migration/migrate_business_games.py Max --dry-run

# 2. Jeśli OK, migracja testowa
python scripts/migration/migrate_business_games.py Max --migrate

# 3. Weryfikacja
python scripts/migration/test_sql_read.py Max

# 4. Test funkcjonalności (manual QA)
# - Otwórz Business Games
# - Sprawdź czy dane się wyświetlają
# - Wykonaj kontrakt
# - Zatrudnij pracownika
# - Sprawdź historię

# 5. Jeśli wszystko OK → rollback JSON dla Max (tymczasowo)
```

#### Dzień 2: Batch Migration (wszyscy użytkownicy)
```bash
# 1. Backup users_data.json
cp users_data.json users_data_backup_before_sql_migration_$(date +%Y%m%d).json

# 2. Batch migration (fazy)
python scripts/migration/migrate_all_users.py --phase1  # 5 userów
python scripts/migration/migrate_all_users.py --phase2  # 15 userów
python scripts/migration/migrate_all_users.py --phase3  # reszta

# 3. Verification
python scripts/migration/final_stats.py

# 4. Switch backend w config
# config/settings.py
DATABASE_BACKEND = "sql"  # było "json"

# 5. Restart aplikacji
# Teraz WSZYSCY używają SQL!
```

**Deliverable:** Consulting w SQL, JSON jako backup

---

### FAZA 2: REFACTORING GAME DATA STRUCTURE (1 dzień)

#### Problem: Redundancje
```python
# ❌ TERAZ (redundancja)
user_data = {
    "degencoins": 5000,  # ← Tu są monety
    "business_games": {
        "consulting": {
            "money": 0,  # ← I tu też (DEPRECATED!)
            "firm": {
                "coins": 0  # ← I TU! (stare)
            }
        }
    }
}

# ✅ POWINNO BYĆ (1 źródło prawdy)
user_data = {
    "degencoins": 5000,  # ← TYLKO TU
    "business_games": {
        "consulting": {
            # money USUNIĘTE
            "firm": {
                # coins USUNIĘTE
            }
        }
    }
}
```

#### Akcje
1. **Cleanup migration script**
```python
# scripts/cleanup_deprecated_money_fields.py
def cleanup_user(user_data):
    if "business_games" in user_data:
        for industry, bg_data in user_data["business_games"].items():
            # Usuń money (deprecated)
            if "money" in bg_data:
                del bg_data["money"]
            
            # Usuń firm.coins (stare)
            if "firm" in bg_data and "coins" in bg_data["firm"]:
                del bg_data["firm"]["coins"]
    
    return user_data
```

2. **Update utils/business_game.py**
- Usuń wszystkie `bg_data["money"]` references
- Używaj tylko `user_data["degencoins"]`
- Update docstringi

3. **Update views/business_games.py**
- Zmień wywołania `get_game_data()` → zawsze pobieraj `user_data["degencoins"]`

**Deliverable:** 1 źródło prawdy dla monet (degencoins)

---

### FAZA 3: STANDARYZACJA API (1 dzień)

#### Problem: Mieszane API
```python
# ❌ views/business_games.py (linia 829)
with open('users_data.json', 'r', encoding='utf-8') as f:  # BEZPOŚREDNI JSON!
    all_users = json.load(f)

# ✅ POWINNO BYĆ
from data.repositories import UserRepository
user_repo = UserRepository()  # backend z config
user_data = user_repo.get_user(username)
```

#### Akcje
1. **Find all direct JSON access**
```bash
grep -r "open('users_data.json'" views/
grep -r "json.load" views/
grep -r "json.dump" views/
```

2. **Replace with Repository calls**
```python
# PRZED
with open('users_data.json', 'r') as f:
    users = json.load(f)
user_data = users[username]

# PO
from data.repositories import UserRepository
user_repo = UserRepository()
user_data = user_repo.get_user(username)
```

3. **Update utils/achievements.py** (linia 369)
```python
# PRZED
def load_user_data(username: str) -> Dict[str, Any]:
    users_file = "users_data.json"
    with open(users_file, 'r', encoding='utf-8') as f:
        users = json.load(f)
    return users.get(username, {})

# PO
def load_user_data(username: str) -> Dict[str, Any]:
    from data.repositories import UserRepository
    user_repo = UserRepository()
    return user_repo.get_user(username) or {}
```

**Deliverable:** Cały projekt używa Repository API

---

### FAZA 4: CLEANUP DEPRECATED CODE (pół dnia)

#### Problem: Stare struktury
```python
# ❌ STARE (deprecated)
user_data["business_game"]  # Singular!

# ✅ NOWE
user_data["business_games"]["consulting"]  # Plural, multi-industry
```

#### Akcje
1. **Find deprecated references**
```bash
grep -r "business_game\"" --include="*.py" | grep -v "business_games"
```

2. **Migration cleanup** (views/business_games.py linia 58)
```python
# ❌ USUNĄĆ (backward compatibility już niepotrzebna)
if "business_game" in user_data and "business_games" not in user_data:
    user_data["business_games"] = {
        "consulting": user_data["business_game"]
    }
    save_user_data(username, user_data)

# ✅ GDY WSZYSCY SĄ W SQL, TO NIE JEST POTRZEBNE
```

3. **Update documentation**
- README.md - update data structure
- MIGRATION_PLAN.md - mark as complete

**Deliverable:** Clean codebase bez deprecated paths

---

## 🏗️ FMCG IMPLEMENTATION READINESS

### Po refactoringu będziemy mieć:

#### ✅ SOLID FOUNDATIONS
```python
# 1. SQL Models gotowe
BusinessGame (scenario_type="fmcg")
BusinessGameContract (extra_data dla FMCG fields)
BusinessGameEmployee (może być reużyte dla sales reps)
BusinessGameTransaction (historia finansowa)
BusinessGameStats (tracking performance)

# 2. Repository gotowy
bg_repo = BusinessGameRepository(backend="sql")
bg_repo.save_scenario(username, "fmcg", fmcg_data)

# 3. Consistent API
wszystkie operacje przez Repository
brak bezpośredniego JSON access

# 4. Single source of truth
user_data["degencoins"] - tylko tu monety
user_data["business_games"]["fmcg"] - nowy scenariusz
```

---

### 🎮 FMCG-Specific Extensions Needed

#### 1. **New Contract Fields** (używamy extra_data!)
```python
# W BusinessGameContract.extra_data będzie:
{
  "client_type": "PROSPECT|ACTIVE|LOST",
  "client_status": "new|interested|signed|angry",
  "client_reputation": 0-100,  # Per-client!
  "client_monthly_value": 500-50000,
  "visit_count": 0,
  "last_visit": "2025-11-15",
  "products": ["FreshSoap", "FreshMilk"],
  "market_share": 25,  # %
  "contract_type": "regular_visit|operational|sales|emergency",
  "location": {"lat": 52.xxx, "lng": 21.xxx},
  "distance_km": 8
}
```

**✅ NIE TRZEBA ZMIENIAĆ SCHEMA!** `extra_data` (JSON) wspiera to wszystko!

---

#### 2. **New Stats Fields** (rozszerzenie BusinessGameStats)
```python
# Możemy dodać nowe kolumny DO ISTNIEJĄCEJ TABELI:
ALTER TABLE business_game_stats ADD COLUMN overall_reputation INTEGER DEFAULT 0;
ALTER TABLE business_game_stats ADD COLUMN prospects_count INTEGER DEFAULT 0;
ALTER TABLE business_game_stats ADD COLUMN active_count INTEGER DEFAULT 0;
ALTER TABLE business_game_stats ADD COLUMN lost_count INTEGER DEFAULT 0;
ALTER TABLE business_game_stats ADD COLUMN total_visits INTEGER DEFAULT 0;
ALTER TABLE business_game_stats ADD COLUMN avg_ai_rating DECIMAL(3,2) DEFAULT 0;

# LUB używamy extra_data (elastyczniej)
stats.extra_data = {
  "fmcg_specific": {
    "overall_reputation": 58,
    "client_distribution": {"PROSPECT": 5, "ACTIVE": 8, "LOST": 2},
    "territory_coverage": 65  # %
  }
}
```

**✅ Obie opcje działają!** Kolumny = szybsze queries, JSON = elastyczność

---

#### 3. **New Transaction Types**
```python
# Już wspierane! transaction_type jest VARCHAR(50)
TransactionType.VISIT_REWARD = "visit_reward"
TransactionType.TASK_REWARD = "task_reward"
TransactionType.TRADE_MARKETING = "trade_marketing_cost"
TransactionType.ENERGY_COST = "energy_cost"  # Opcjonalne, jeśli płatne
TransactionType.LEVEL_BONUS = "level_bonus"
```

**✅ Działa out-of-the-box!**

---

#### 4. **New Game Data Fields** (BusinessGame)
```python
# Używamy istniejących pól + JSON extensions:

# scenario_modifiers (JSON):
{
  "energy_system": True,
  "starting_energy": 100,
  "energy_regen_per_day": 100,
  "trade_marketing_budget": 2000,
  "max_clients": 15
}

# scenario_objectives (JSON):
[
  {"type": "revenue", "target": 10000, "current": 2500},
  {"type": "contracts", "target": 10, "current": 3},
  {"type": "reputation", "target": 60, "current": 45}
]

# events (JSON) - już używane dla consulting!
[
  {
    "id": "weather_rain_2025_11_15",
    "type": "weather",
    "effect": {"energy_cost_multiplier": 1.2},
    "expires_at": "2025-11-15 23:59:59"
  }
]
```

**✅ Wszystko już wspierane!**

---

## 📋 TIMELINE & PRIORITIES

### PRIORYTET 1 (CRITICAL) - 2 dni
**Migracja Consulting → SQL**
- [ ] Dzień 1: Test migration (Max) + validation
- [ ] Dzień 2: Batch migration (wszyscy) + switch backend

**Dlaczego krytyczne:**
- Fundament dla FMCG
- Eliminuje JSON split-brain
- Umożliwia SQL queries (ranking, stats)

---

### PRIORYTET 2 (HIGH) - 1 dzień
**Refactoring data structure**
- [ ] Cleanup money/coins redundancja
- [ ] 1 źródło prawdy (degencoins)
- [ ] Update dokumentacji

**Dlaczego ważne:**
- Unikniemy bugów (2 różne salda)
- Czysty kod dla FMCG
- Konsystencja

---

### PRIORYTET 3 (MEDIUM) - 1 dzień
**Standaryzacja API**
- [ ] Replace all direct JSON access → Repository
- [ ] Update utils/achievements.py
- [ ] Update views/business_games.py

**Dlaczego przydatne:**
- Backend-agnostic kod
- Łatwiejsze testy
- Przyszłościowe (PostgreSQL later)

---

### PRIORYTET 4 (LOW) - pół dnia
**Cleanup deprecated**
- [ ] Remove backward compatibility code
- [ ] Remove old `business_game` references
- [ ] Update docs

**Dlaczego opcjonalne:**
- Nie blokuje FMCG
- Techniczna czystość

---

## 🚀 REKOMENDOWANA ŚCIEŻKA

### OPTION A: BEZPIECZNA (5 dni total)
```
Dzień 1-2: Migracja Consulting → SQL
Dzień 3:   Refactoring data structure
Dzień 4:   Standaryzacja API
Dzień 5:   Cleanup + testy

→ Dzień 6+: Start FMCG implementation
```

**Zalety:**
- ✅ Solidne fundamenty
- ✅ Wszystko w SQL
- ✅ Czysty kod
- ✅ Łatwe debugging

**Wady:**
- ⏱️ 5 dni delay przed FMCG

---

### OPTION B: SZYBKA (3 dni total + równolegle)
```
Dzień 1:   Refactoring data structure + API standaryzacja
Dzień 2-3: FMCG implementation (bezpośrednio w SQL!)

Równolegle (background):
- Migracja consulting → SQL (nie blokuje FMCG)
```

**Zalety:**
- ✅ Szybki start FMCG
- ✅ Consulting migracja nie blokuje

**Wady:**
- ⚠️ FMCG w SQL, consulting wciąż w JSON (tymczasowo)
- ⚠️ Mixed backend przez 2-3 tygodnie

---

### OPTION C: HYBRYDOWA (4 dni total)
```
Dzień 1-2: Migracja Consulting → SQL (MUST HAVE)
Dzień 3:   Refactoring data structure (MUST HAVE)
Dzień 4+:  FMCG implementation (clean start!)

SKIP (na później):
- Standaryzacja API (nice-to-have)
- Cleanup deprecated (nice-to-have)
```

**Zalety:**
- ✅ Solidne fundamenty (SQL + clean data)
- ✅ Relatywnie szybki start (4 dni)
- ✅ Optymalizacja później (nie blokuje)

**Wady:**
- ⏱️ 4 dni delay (ale worth it!)

---

## 🎯 MOJA REKOMENDACJA: **OPTION C (Hybrydowa)**

### Dlaczego?
1. **Consulting → SQL = MUST** (eliminuje split-brain, wspiera queries)
2. **Data cleanup = MUST** (unikniemy bugów z money/coins)
3. **API standaryzacja = nice-to-have** (można refactorować równolegle z FMCG)
4. **Deprecated cleanup = nice-to-have** (techniczna czystość, niepilne)

### Co robimy:
```
📅 DZIEŃ 1-2 (Ty + ja):
Migration consulting → SQL
- Test na Max (dry-run)
- Batch migration (wszyscy)
- Verification
- Switch backend to "sql"

📅 DZIEŃ 3 (ja):
Refactoring data structure
- Cleanup money/coins
- 1 source of truth
- Update business_game.py

📅 DZIEŃ 4+ (ja + Ty review):
FMCG Implementation starts!
- Clean codebase
- SQL backend
- Repository API
- Extra_data dla FMCG fields
```

---

## ✅ CHECKLIST PRZED FMCG

### Przed startem implementacji FMCG, upewnij się że:

- [ ] **SQL Migration Complete**
  - [ ] Consulting w SQL (nie JSON)
  - [ ] Verification passed (test_sql_read.py)
  - [ ] Backend = "sql" w config
  - [ ] Manual QA (business games działa)

- [ ] **Data Structure Clean**
  - [ ] Tylko `user_data["degencoins"]` (nie money/coins)
  - [ ] Tests passed
  - [ ] No console errors

- [ ] **Repository API Works**
  - [ ] `UserRepository` tested
  - [ ] `BusinessGameRepository` tested
  - [ ] Backend switching działa

- [ ] **Documentation Updated**
  - [ ] README.md - nowa struktura
  - [ ] MIGRATION_PLAN.md - status

---

## 🛠️ DODATKOWE NARZĘDZIA DO STWORZENIA

### 1. **Validation Script**
```python
# scripts/validate_data_integrity.py
def validate_user_data(username):
    """Sprawdź czy user data jest spójna"""
    user_repo = UserRepository(backend="sql")
    user_data = user_repo.get_user(username)
    
    issues = []
    
    # Check 1: Tylko degencoins (nie money/coins)
    if "business_games" in user_data:
        for industry, bg_data in user_data["business_games"].items():
            if "money" in bg_data:
                issues.append(f"{industry}: deprecated 'money' field found")
            if "firm" in bg_data and "coins" in bg_data["firm"]:
                issues.append(f"{industry}: deprecated 'coins' field found")
    
    # Check 2: SQL vs JSON consistency
    bg_repo = BusinessGameRepository(backend="sql")
    for industry in ["consulting", "fmcg"]:
        sql_data = bg_repo._get_from_sql(username, industry)
        json_data = bg_repo._get_from_json(username, industry)
        
        if sql_data and json_data:
            # Oba istnieją = problem!
            issues.append(f"{industry}: exists in BOTH SQL and JSON")
        
        if not sql_data and not json_data:
            # Żaden nie istnieje = OK (user nie gra)
            pass
    
    return issues

# Usage
issues = validate_user_data("Max")
if issues:
    print("❌ Issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✅ Data integrity OK!")
```

---

### 2. **Performance Monitoring**
```python
# utils/performance.py
import time
from functools import wraps

def monitor_performance(func):
    """Decorator do monitorowania czasu wykonania"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        
        if elapsed > 1.0:  # >1s = warning
            print(f"⚠️ SLOW: {func.__name__} took {elapsed:.2f}s")
        
        return result
    return wrapper

# Usage
@monitor_performance
def get_business_game_data(username, industry):
    # ... existing code
```

---

### 3. **SQL Query Logger** (debug)
```python
# utils/sql_logger.py
import logging
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if "business_game" in statement:  # Log tylko business game queries
        logging.info(f"SQL: {statement[:100]}...")

# Enable w development
if DEBUG:
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

---

## 📊 EXPECTED RESULTS

### Po zakończeniu refactoringu:

#### ✅ **Performance**
- JSON file lock: **ELIMINATED** (SQL concurrent access)
- Query speed: **10x faster** (indexed SQL vs full JSON scan)
- Backup corruption: **ELIMINATED** (SQL transactions)

#### ✅ **Developer Experience**
- 1 API dla wszystkich operacji (Repository)
- Type safety (SQLAlchemy models)
- Debugowanie łatwiejsze (SQL queries visible)

#### ✅ **Code Quality**
- Eliminated redundancy (money/coins → degencoins)
- Consistent patterns (Repository everywhere)
- Clean architecture (separation of concerns)

#### ✅ **FMCG Ready**
- SQL models support FMCG (extra_data)
- Repository API ready
- No technical debt blocking

---

## 🚨 RISKS & MITIGATION

### Risk 1: Migration Data Loss
**Mitigation:**
- Backup users_data.json PRZED migracją
- Dry-run ZAWSZE najpierw
- Verification script PO migracji
- Rollback plan (restore JSON, switch backend back)

### Risk 2: Downtime During Migration
**Mitigation:**
- Migration poza peak hours (3-6 AM)
- Phased approach (5 → 15 → reszta)
- Fast rollback (<5 min)

### Risk 3: Hidden Dependencies on JSON
**Mitigation:**
- Grep all "users_data.json" references
- Replace with Repository calls
- Integration tests

### Risk 4: Performance Regression
**Mitigation:**
- Monitor query times (@monitor_performance)
- SQL indexes (już są!)
- Connection pooling (SQLAlchemy default)

---

## 📞 DECISION TIME

**Pytanie do Ciebie:**

1. **Którą opcję wybieramy?**
   - [ ] OPTION A - Bezpieczna (5 dni, full refactor)
   - [ ] OPTION B - Szybka (3 dni, FMCG w SQL natychmiast)
   - [ ] OPTION C - Hybrydowa (4 dni, migracja + cleanup) **← RECOMMENDED**

2. **Kiedy startujemy?**
   - [ ] Dzisiaj (28.10)
   - [ ] Jutro (29.10)
   - [ ] Inny termin: __________

3. **Kto robi co?**
   - [ ] Ja robię wszystko (Ty review + QA)
   - [ ] Ty robisz migrację, ja refactoring
   - [ ] Razem pair programming

4. **Testing approach?**
   - [ ] Manual QA (Ty testujesz)
   - [ ] Automated tests (ja piszę)
   - [ ] Obie

**Odpowiedz, a startujemy! 🚀**

---

## 📚 APPENDIX: Useful Commands

### Backup
```bash
# Full backup
cp users_data.json users_data_backup_$(date +%Y%m%d_%H%M%S).json

# Database dump (jeśli PostgreSQL later)
pg_dump bva_db > backup_$(date +%Y%m%d).sql
```

### Migration
```bash
# Dry-run
python scripts/migration/migrate_business_games.py Max --dry-run

# Live migration
python scripts/migration/migrate_business_games.py Max --migrate

# Batch
python scripts/migration/migrate_all_users.py
```

### Verification
```bash
# Check SQL data
python scripts/migration/test_sql_read.py Max

# Stats
python scripts/migration/final_stats.py

# Integrity check
python scripts/validate_data_integrity.py
```

### Rollback
```bash
# Restore JSON
cp users_data_backup_YYYYMMDD.json users_data.json

# Switch backend
# config/settings.py
DATABASE_BACKEND = "json"

# Restart
streamlit run main.py
```

---

**KONIEC AUDYTU**

Gotowy do implementacji? Daj znać którą opcję wybieramy! 💪
