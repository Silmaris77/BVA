# 🔄 Plan Migracji JSON → SQL - Szczegółowy i Bezpieczny

## 📊 Analiza Obecnego Stanu

### Problemy Identyfikowane z Poprzedniej Migracji
1. **Business Games**: Błędy przy włączaniu scenariuszy
2. **Utrata danych**: Brak pełnego backupu przed migracją
3. **Brak warstwy abstrakcji**: Bezpośrednie zależności od JSON
4. **Brak możliwości rollback**: Trudność w cofnięciu zmian

### Struktura Danych do Migracji

#### 1. **users_data.json** (~20K linii!)
```json
{
  "username": {
    "user_id": "uuid",
    "password": "hash",
    "xp": 1634,
    "degencoins": 107407,
    "level": 1,
    "badges": [...],
    "completed_lessons": [...],
    "lesson_progress": {...},
    "inspirations": {
      "read": [...],
      "favorites": [...]
    },
    "recent_activities": [...],
    "badge_data": {...},
    "business_game": {...},      // STARA STRUKTURA
    "business_games": {          // NOWA STRUKTURA
      "consulting": {
        "scenario_id": "...",
        "firm": {...},
        "employees": [...],
        "contracts": {...},
        "stats": {...},
        "ranking": {...},
        "events": {...},
        "money": 0,
        "history": {
          "transactions": [...],
          "level_ups": [...]
        }
      }
    }
  }
}
```

#### 2. **Inne pliki JSON**
- `game_master_queue.json` - kolejka AI dla business games
- `leadership_profiles.json` - profile przywództwa
- `user_status.json` - status użytkowników
- `config/api_limits.json` - limity API
- `config/business_games_active_mode.json` - tryb AI

---

## 🎯 Strategia Migracji - "Stopniowa z Feature Flag"

### Zasady Projektowe
1. ✅ **Zero Downtime** - aplikacja działa przez cały czas
2. ✅ **Dual Write** - zapis do JSON i SQL równolegle
3. ✅ **Feature Flag** - łatwe przełączanie źródła danych
4. ✅ **Pełny Rollback** - możliwość cofnięcia w każdej chwili
5. ✅ **Testowanie na produkcji** - stopniowe włączanie dla użytkowników

---

## 📐 Architektura Docelowa

### Warstwa Abstrakcji (Repository Pattern)

```
┌─────────────────────────────────────────┐
│        Application Layer                │
│  (views/, utils/, main.py)              │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│     Repository Layer (NOWA!)            │
│  - UserRepository                       │
│  - BusinessGameRepository               │
│  - LessonProgressRepository             │
│  - InspirationRepository                │
└───────────────┬─────────────────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
┌──────────────┐  ┌──────────────┐
│ JSON Storage │  │ SQL Storage  │
│ (backward    │  │ (new, SQLite │
│  compat)     │  │  or Postgres)│
└──────────────┘  └──────────────┘
```

### Feature Flag System

```python
# config/migration_config.json
{
  "storage_backend": "json",  # "json" | "sql" | "dual"
  "per_user_backend": {
    "Max": "sql",             # Test user na SQL
    "Admin": "sql",
    "*": "json"               # Wszyscy inni na JSON
  },
  "dual_write_enabled": true,
  "read_from_sql_percentage": 0,  # Stopniowe zwiększanie: 0 → 25 → 50 → 100
  "rollback_enabled": true
}
```

---

## 🗄️ Schema Bazy Danych

### SQLite (Developement) / PostgreSQL (Production)

```sql
-- ============================================
-- 1. USERS (Core User Data)
-- ============================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id UUID UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    degen_type VARCHAR(50),
    xp INTEGER DEFAULT 0,
    degencoins INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    joined_date DATE NOT NULL,
    last_login TIMESTAMP,
    test_taken BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_user_id (user_id)
);

-- ============================================
-- 2. LESSON PROGRESS
-- ============================================
CREATE TABLE lesson_progress (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    lesson_id VARCHAR(255) NOT NULL,
    section_name VARCHAR(100) NOT NULL,  -- 'intro', 'content', 'quiz', etc.
    xp_awarded BOOLEAN DEFAULT FALSE,
    completed BOOLEAN DEFAULT FALSE,
    xp INTEGER DEFAULT 0,
    degencoins INTEGER DEFAULT 0,
    timestamp TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, lesson_id, section_name),
    INDEX idx_user_lesson (user_id, lesson_id)
);

-- ============================================
-- 3. COMPLETED LESSONS (Many-to-Many)
-- ============================================
CREATE TABLE completed_lessons (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    lesson_id VARCHAR(255) NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, lesson_id),
    INDEX idx_user_completed (user_id)
);

-- ============================================
-- 4. BADGES
-- ============================================
CREATE TABLE user_badges (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    badge_id VARCHAR(100) NOT NULL,
    earned_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, badge_id),
    INDEX idx_user_badges (user_id)
);

CREATE TABLE badge_data (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    badge_id VARCHAR(100) NOT NULL,
    earned BOOLEAN DEFAULT FALSE,
    earned_date DATE,
    xp_earned INTEGER DEFAULT 0,
    tier VARCHAR(50),
    progress DECIMAL(5,2) DEFAULT 0,
    conditions_met JSONB,  -- Przechowuj złożone dane jako JSON
    context JSONB,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, badge_id),
    INDEX idx_user_badge_data (user_id)
);

-- ============================================
-- 5. INSPIRATIONS
-- ============================================
CREATE TABLE user_inspirations (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    inspiration_id VARCHAR(100) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    is_favorite BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,
    favorited_at TIMESTAMP,
    UNIQUE(user_id, inspiration_id),
    INDEX idx_user_inspirations (user_id)
);

-- ============================================
-- 6. RECENT ACTIVITIES
-- ============================================
CREATE TABLE recent_activities (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    activity_type VARCHAR(100) NOT NULL,
    details JSONB,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_activities (user_id, timestamp DESC)
);

-- ============================================
-- 7. BUSINESS GAMES - FIRMA
-- ============================================
CREATE TABLE business_games (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    industry_id VARCHAR(50) NOT NULL,  -- 'consulting', 'fmcg', etc.
    
    -- Scenario metadata
    scenario_id VARCHAR(100),
    scenario_modifiers JSONB,
    scenario_objectives JSONB,
    objectives_completed JSONB,
    
    -- Firma
    firm_name VARCHAR(255),
    firm_logo VARCHAR(10),
    firm_founded DATE,
    firm_level INTEGER DEFAULT 1,
    firm_reputation INTEGER DEFAULT 0,
    
    -- Office
    office_type VARCHAR(50) DEFAULT 'home_office',
    office_upgraded_at TIMESTAMP,
    
    -- Money & Stats
    money INTEGER DEFAULT 0,
    initial_money INTEGER DEFAULT 0,
    total_revenue INTEGER DEFAULT 0,
    total_costs INTEGER DEFAULT 0,
    net_profit INTEGER DEFAULT 0,
    
    -- Contract stats
    contracts_completed INTEGER DEFAULT 0,
    contracts_5star INTEGER DEFAULT 0,
    contracts_4star INTEGER DEFAULT 0,
    contracts_3star INTEGER DEFAULT 0,
    contracts_2star INTEGER DEFAULT 0,
    contracts_1star INTEGER DEFAULT 0,
    avg_rating DECIMAL(3,2) DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, industry_id),
    INDEX idx_user_industry (user_id, industry_id)
);

-- ============================================
-- 8. BUSINESS GAMES - PRACOWNICY
-- ============================================
CREATE TABLE business_game_employees (
    id SERIAL PRIMARY KEY,
    game_id INTEGER NOT NULL REFERENCES business_games(id) ON DELETE CASCADE,
    employee_type VARCHAR(50) NOT NULL,
    hired_at TIMESTAMP NOT NULL,
    name VARCHAR(255),
    INDEX idx_game_employees (game_id)
);

-- ============================================
-- 9. BUSINESS GAMES - KONTRAKTY
-- ============================================
CREATE TABLE business_game_contracts (
    id SERIAL PRIMARY KEY,
    game_id INTEGER NOT NULL REFERENCES business_games(id) ON DELETE CASCADE,
    contract_id VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,  -- 'available', 'active', 'completed'
    
    -- Contract details (przechowuj jako JSONB dla elastyczności)
    contract_data JSONB NOT NULL,
    
    -- Timestamps
    accepted_at TIMESTAMP,
    completed_at TIMESTAMP,
    deadline TIMESTAMP,
    
    -- Evaluation (dla completed)
    rating INTEGER,
    evaluation_details JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_game_contracts (game_id, status),
    INDEX idx_contract_status (game_id, status)
);

-- ============================================
-- 10. BUSINESS GAMES - TRANSAKCJE (History)
-- ============================================
CREATE TABLE business_game_transactions (
    id SERIAL PRIMARY KEY,
    game_id INTEGER NOT NULL REFERENCES business_games(id) ON DELETE CASCADE,
    transaction_date TIMESTAMP NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    amount INTEGER NOT NULL,
    description TEXT,
    balance_after INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_game_transactions (game_id, transaction_date DESC)
);

-- ============================================
-- 11. BUSINESS GAMES - WYDARZENIA
-- ============================================
CREATE TABLE business_game_events (
    id SERIAL PRIMARY KEY,
    game_id INTEGER NOT NULL REFERENCES business_games(id) ON DELETE CASCADE,
    event_id VARCHAR(100),
    event_type VARCHAR(50),
    event_data JSONB,
    triggered_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_game_events (game_id, is_active)
);

-- ============================================
-- 12. BUSINESS GAMES - RANKING
-- ============================================
CREATE TABLE business_game_rankings (
    id SERIAL PRIMARY KEY,
    game_id INTEGER NOT NULL REFERENCES business_games(id) ON DELETE CASCADE,
    overall_score DECIMAL(10,2) DEFAULT 0,
    ranking_data JSONB,  -- current_positions, badges, etc.
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(game_id),
    INDEX idx_game_ranking (game_id)
);

-- ============================================
-- 13. BUSINESS GAMES - STATYSTYKI KATEGORII
-- ============================================
CREATE TABLE business_game_category_stats (
    id SERIAL PRIMARY KEY,
    game_id INTEGER NOT NULL REFERENCES business_games(id) ON DELETE CASCADE,
    category VARCHAR(50) NOT NULL,
    contracts_completed INTEGER DEFAULT 0,
    total_earned INTEGER DEFAULT 0,
    avg_rating DECIMAL(3,2) DEFAULT 0,
    UNIQUE(game_id, category),
    INDEX idx_game_category (game_id)
);

-- ============================================
-- 14. MIGRATION STATUS (dla trackingu)
-- ============================================
CREATE TABLE migration_status (
    id SERIAL PRIMARY KEY,
    user_id UUID UNIQUE NOT NULL,
    migrated_to_sql BOOLEAN DEFAULT FALSE,
    migration_date TIMESTAMP,
    last_json_backup TEXT,  -- Path to backup file
    rollback_available BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔧 Implementacja - Krok po Kroku

### FAZA 0: Przygotowanie (Dzień 1-2)

#### 1. Backup System
```bash
# Stwórz automatyczny system backupów
python scripts/create_full_backup.py
```

**File: `scripts/create_full_backup.py`**
```python
import json
import shutil
from datetime import datetime
from pathlib import Path

def create_full_backup():
    """Tworzy pełny backup wszystkich plików JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"backups/pre_migration_{timestamp}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    files_to_backup = [
        "users_data.json",
        "game_master_queue.json",
        "leadership_profiles.json",
        "user_status.json",
        "config/api_limits.json",
        "config/business_games_active_mode.json"
    ]
    
    backup_manifest = {
        "timestamp": timestamp,
        "files": [],
        "checksums": {}
    }
    
    for file in files_to_backup:
        if Path(file).exists():
            dest = backup_dir / file
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest)
            
            # Checksum dla weryfikacji
            import hashlib
            with open(file, 'rb') as f:
                checksum = hashlib.sha256(f.read()).hexdigest()
            
            backup_manifest["files"].append(file)
            backup_manifest["checksums"][file] = checksum
            print(f"✅ Backed up: {file}")
    
    # Zapisz manifest
    with open(backup_dir / "manifest.json", 'w') as f:
        json.dump(backup_manifest, f, indent=2)
    
    print(f"\n🎉 Backup completed: {backup_dir}")
    return str(backup_dir)

if __name__ == "__main__":
    create_full_backup()
```

#### 2. Struktura Projektu
```
BVA/
├── data/
│   ├── users.py (STARY - do refaktoru)
│   └── repositories/  (NOWY)
│       ├── __init__.py
│       ├── base_repository.py
│       ├── user_repository.py
│       ├── business_game_repository.py
│       ├── lesson_progress_repository.py
│       └── inspiration_repository.py
├── database/
│   ├── __init__.py
│   ├── models.py (SQLAlchemy models)
│   ├── connection.py
│   └── migrations/
│       ├── migrate_users.py
│       ├── migrate_business_games.py
│       └── rollback.py
├── config/
│   └── migration_config.json
└── scripts/
    ├── create_full_backup.py
    ├── verify_migration.py
    └── switch_backend.py
```

---

### FAZA 1: Warstwa Abstrakcji (Dzień 3-5)

#### 1. **Base Repository Pattern**

**File: `data/repositories/base_repository.py`**
```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import json
from pathlib import Path

class BaseRepository(ABC):
    """Abstrakcyjna klasa bazowa dla repozytoriów"""
    
    def __init__(self, backend: str = "json"):
        """
        Args:
            backend: "json" | "sql" | "dual"
        """
        self.backend = backend
        self._load_config()
    
    def _load_config(self):
        """Ładuje konfigurację migracji"""
        config_path = Path("config/migration_config.json")
        if config_path.exists():
            with open(config_path) as f:
                self.config = json.load(f)
        else:
            self.config = {"storage_backend": "json"}
    
    def _should_use_sql(self, username: Optional[str] = None) -> bool:
        """Decyduje czy użyć SQL na podstawie konfiguracji"""
        if self.backend == "json":
            return False
        elif self.backend == "sql":
            return True
        elif self.backend == "dual":
            # Per-user configuration
            if username:
                per_user = self.config.get("per_user_backend", {})
                user_backend = per_user.get(username, per_user.get("*", "json"))
                return user_backend == "sql"
            return False
        return False
    
    @abstractmethod
    def get(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Pobiera dane"""
        pass
    
    @abstractmethod
    def save(self, identifier: str, data: Dict[str, Any]) -> bool:
        """Zapisuje dane"""
        pass
    
    @abstractmethod
    def delete(self, identifier: str) -> bool:
        """Usuwa dane"""
        pass
```

#### 2. **User Repository**

**File: `data/repositories/user_repository.py`**
```python
from typing import Optional, Dict, Any
import json
import os
from datetime import datetime
from .base_repository import BaseRepository

# SQL imports (conditional)
try:
    from database.models import User, session_scope
    from database.connection import get_session
    SQL_AVAILABLE = True
except ImportError:
    SQL_AVAILABLE = False

class UserRepository(BaseRepository):
    """Repository dla danych użytkowników"""
    
    def __init__(self, backend: str = "json"):
        super().__init__(backend)
        self.json_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            'users_data.json'
        )
    
    def get(self, username: str) -> Optional[Dict[str, Any]]:
        """Pobiera dane użytkownika"""
        use_sql = self._should_use_sql(username)
        
        if use_sql and SQL_AVAILABLE:
            return self._get_from_sql(username)
        else:
            return self._get_from_json(username)
    
    def _get_from_json(self, username: str) -> Optional[Dict[str, Any]]:
        """Pobiera z JSON (stara metoda)"""
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
                return users_data.get(username)
        return None
    
    def _get_from_sql(self, username: str) -> Optional[Dict[str, Any]]:
        """Pobiera z SQL (nowa metoda)"""
        with session_scope() as session:
            user = session.query(User).filter_by(username=username).first()
            if user:
                return user.to_dict()
        return None
    
    def save(self, username: str, user_data: Dict[str, Any]) -> bool:
        """Zapisuje dane użytkownika"""
        use_sql = self._should_use_sql(username)
        dual_write = self.config.get("dual_write_enabled", False)
        
        success = True
        
        # JSON write (zawsze w dual mode lub gdy JSON backend)
        if not use_sql or dual_write:
            success = success and self._save_to_json(username, user_data)
        
        # SQL write (gdy SQL backend lub dual mode)
        if use_sql and SQL_AVAILABLE:
            success = success and self._save_to_sql(username, user_data)
        
        return success
    
    def _save_to_json(self, username: str, user_data: Dict[str, Any]) -> bool:
        """Zapisuje do JSON"""
        try:
            # Load all users
            all_users = {}
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, 'r', encoding='utf-8') as f:
                    all_users = json.load(f)
            
            # Update specific user
            all_users[username] = user_data
            
            # Save back
            with open(self.json_file_path, 'w', encoding='utf-8') as f:
                json.dump(all_users, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving to JSON: {e}")
            return False
    
    def _save_to_sql(self, username: str, user_data: Dict[str, Any]) -> bool:
        """Zapisuje do SQL"""
        try:
            with session_scope() as session:
                user = session.query(User).filter_by(username=username).first()
                
                if user:
                    # Update existing
                    user.update_from_dict(user_data)
                else:
                    # Create new
                    user = User.from_dict(username, user_data)
                    session.add(user)
                
                session.commit()
                return True
        except Exception as e:
            print(f"Error saving to SQL: {e}")
            return False
    
    def delete(self, username: str) -> bool:
        """Usuwa użytkownika"""
        use_sql = self._should_use_sql(username)
        
        success = True
        
        # Delete from JSON
        if not use_sql or self.config.get("dual_write_enabled", False):
            success = success and self._delete_from_json(username)
        
        # Delete from SQL
        if use_sql and SQL_AVAILABLE:
            success = success and self._delete_from_sql(username)
        
        return success
    
    def _delete_from_json(self, username: str) -> bool:
        """Usuwa z JSON"""
        try:
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, 'r', encoding='utf-8') as f:
                    all_users = json.load(f)
                
                if username in all_users:
                    del all_users[username]
                    
                    with open(self.json_file_path, 'w', encoding='utf-8') as f:
                        json.dump(all_users, f, indent=2, ensure_ascii=False)
                    return True
            return False
        except Exception as e:
            print(f"Error deleting from JSON: {e}")
            return False
    
    def _delete_from_sql(self, username: str) -> bool:
        """Usuwa z SQL"""
        try:
            with session_scope() as session:
                user = session.query(User).filter_by(username=username).first()
                if user:
                    session.delete(user)
                    session.commit()
                    return True
            return False
        except Exception as e:
            print(f"Error deleting from SQL: {e}")
            return False
    
    def get_all(self) -> Dict[str, Any]:
        """Pobiera wszystkich użytkowników"""
        use_sql = self._should_use_sql()
        
        if use_sql and SQL_AVAILABLE:
            return self._get_all_from_sql()
        else:
            return self._get_all_from_json()
    
    def _get_all_from_json(self) -> Dict[str, Any]:
        """Pobiera wszystkich z JSON"""
        if os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _get_all_from_sql(self) -> Dict[str, Any]:
        """Pobiera wszystkich z SQL"""
        result = {}
        with session_scope() as session:
            users = session.query(User).all()
            for user in users:
                result[user.username] = user.to_dict()
        return result
```

---

### FAZA 2: SQLAlchemy Models (Dzień 6-7)

**File: `database/models.py`** (fragment dla Users i Business Games)

```python
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Date, 
    DateTime, DECIMAL, JSON, ForeignKey, Index, UniqueConstraint, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

Base = declarative_base()

# ============================================
# USER MODEL
# ============================================
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    degen_type = Column(String(50))
    xp = Column(Integer, default=0)
    degencoins = Column(Integer, default=0)
    level = Column(Integer, default=1)
    joined_date = Column(Date, nullable=False)
    last_login = Column(DateTime)
    test_taken = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lesson_progress = relationship("LessonProgress", back_populates="user", cascade="all, delete-orphan")
    completed_lessons = relationship("CompletedLesson", back_populates="user", cascade="all, delete-orphan")
    badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    inspirations = relationship("UserInspiration", back_populates="user", cascade="all, delete-orphan")
    activities = relationship("RecentActivity", back_populates="user", cascade="all, delete-orphan")
    business_games = relationship("BusinessGame", back_populates="user", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Konwertuje model do dict (kompatybilny z JSON)"""
        return {
            "user_id": str(self.user_id),
            "password": self.password_hash,
            "degen_type": self.degen_type,
            "xp": self.xp,
            "degencoins": self.degencoins,
            "level": self.level,
            "joined_date": self.joined_date.strftime("%Y-%m-%d") if self.joined_date else None,
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S") if self.last_login else None,
            "test_taken": self.test_taken,
            "completed_lessons": [cl.lesson_id for cl in self.completed_lessons],
            "badges": [b.badge_id for b in self.badges],
            # ... więcej pól
        }
    
    @classmethod
    def from_dict(cls, username, data):
        """Tworzy model z dict (z JSON)"""
        return cls(
            user_id=uuid.UUID(data.get("user_id")) if data.get("user_id") else uuid.uuid4(),
            username=username,
            password_hash=data.get("password", ""),
            degen_type=data.get("degen_type"),
            xp=data.get("xp", 0),
            degencoins=data.get("degencoins", 0),
            level=data.get("level", 1),
            joined_date=datetime.strptime(data.get("joined_date"), "%Y-%m-%d").date() if data.get("joined_date") else datetime.utcnow().date(),
            last_login=datetime.strptime(data.get("last_login"), "%Y-%m-%d %H:%M:%S") if data.get("last_login") else None,
            test_taken=data.get("test_taken", False)
        )

# ============================================
# BUSINESS GAME MODEL
# ============================================
class BusinessGame(Base):
    __tablename__ = 'business_games'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    industry_id = Column(String(50), nullable=False)
    
    # Scenario
    scenario_id = Column(String(100))
    scenario_modifiers = Column(JSON)
    scenario_objectives = Column(JSON)
    objectives_completed = Column(JSON)
    
    # Firma
    firm_name = Column(String(255))
    firm_logo = Column(String(10))
    firm_founded = Column(Date)
    firm_level = Column(Integer, default=1)
    firm_reputation = Column(Integer, default=0)
    
    # Office
    office_type = Column(String(50), default='home_office')
    office_upgraded_at = Column(DateTime)
    
    # Money & Stats
    money = Column(Integer, default=0)
    initial_money = Column(Integer, default=0)
    total_revenue = Column(Integer, default=0)
    total_costs = Column(Integer, default=0)
    net_profit = Column(Integer, default=0)
    
    # Contract stats
    contracts_completed = Column(Integer, default=0)
    contracts_5star = Column(Integer, default=0)
    contracts_4star = Column(Integer, default=0)
    contracts_3star = Column(Integer, default=0)
    contracts_2star = Column(Integer, default=0)
    contracts_1star = Column(Integer, default=0)
    avg_rating = Column(DECIMAL(3,2), default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="business_games")
    employees = relationship("BusinessGameEmployee", back_populates="game", cascade="all, delete-orphan")
    contracts = relationship("BusinessGameContract", back_populates="game", cascade="all, delete-orphan")
    transactions = relationship("BusinessGameTransaction", back_populates="game", cascade="all, delete-orphan")
    events = relationship("BusinessGameEvent", back_populates="game", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'industry_id', name='uix_user_industry'),
        Index('idx_user_industry', 'user_id', 'industry_id'),
    )
    
    def to_dict(self):
        """Konwertuje do dict (format JSON)"""
        return {
            "scenario_id": self.scenario_id,
            "scenario_modifiers": self.scenario_modifiers or {},
            "scenario_objectives": self.scenario_objectives or [],
            "objectives_completed": self.objectives_completed or [],
            "firm": {
                "name": self.firm_name,
                "logo": self.firm_logo,
                "founded": self.firm_founded.strftime("%Y-%m-%d") if self.firm_founded else None,
                "level": self.firm_level,
                "reputation": self.firm_reputation
            },
            "office": {
                "type": self.office_type,
                "upgraded_at": self.office_upgraded_at.strftime("%Y-%m-%d") if self.office_upgraded_at else None
            },
            "employees": [e.to_dict() for e in self.employees],
            "contracts": {
                "active": [c.to_dict() for c in self.contracts if c.status == 'active'],
                "completed": [c.to_dict() for c in self.contracts if c.status == 'completed'],
                "available_pool": [c.to_dict() for c in self.contracts if c.status == 'available']
            },
            "stats": {
                "total_revenue": self.total_revenue,
                "total_costs": self.total_costs,
                "net_profit": self.net_profit,
                "contracts_completed": self.contracts_completed,
                # ... więcej stats
            },
            "money": self.money,
            "history": {
                "transactions": [t.to_dict() for t in self.transactions],
                "level_ups": []  # TODO: add level_ups table
            }
        }

# ... więcej modeli (Employee, Contract, Transaction, etc.)
```

---

### FAZA 3: Migracja Danych (Dzień 8-9)

**File: `database/migrations/migrate_users.py`**

```python
import json
from pathlib import Path
from database.models import Base, User, session_scope
from database.connection import get_engine
from datetime import datetime
import sys

def migrate_all_users(dry_run=True):
    """
    Migruje wszystkich użytkowników z JSON do SQL
    
    Args:
        dry_run: Jeśli True, tylko symuluje migrację bez zapisu
    """
    # Load JSON data
    json_path = Path("users_data.json")
    if not json_path.exists():
        print("❌ users_data.json not found!")
        return False
    
    with open(json_path, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    print(f"📊 Found {len(users_data)} users to migrate")
    
    # Statystyki
    stats = {
        "total": len(users_data),
        "migrated": 0,
        "failed": 0,
        "errors": []
    }
    
    # Create tables if not exists
    engine = get_engine()
    if not dry_run:
        Base.metadata.create_all(engine)
        print("✅ Database tables created/verified")
    
    # Migrate each user
    for username, user_data in users_data.items():
        try:
            if dry_run:
                print(f"[DRY RUN] Would migrate user: {username}")
                stats["migrated"] += 1
            else:
                migrate_single_user(username, user_data)
                print(f"✅ Migrated: {username}")
                stats["migrated"] += 1
        except Exception as e:
            print(f"❌ Failed to migrate {username}: {e}")
            stats["failed"] += 1
            stats["errors"].append({
                "username": username,
                "error": str(e)
            })
    
    # Podsumowanie
    print("\n" + "="*50)
    print("📊 MIGRATION SUMMARY")
    print("="*50)
    print(f"Total users: {stats['total']}")
    print(f"Migrated: {stats['migrated']}")
    print(f"Failed: {stats['failed']}")
    
    if stats["errors"]:
        print("\n❌ ERRORS:")
        for error in stats["errors"]:
            print(f"  - {error['username']}: {error['error']}")
    
    return stats["failed"] == 0

def migrate_single_user(username, user_data):
    """Migruje pojedynczego użytkownika"""
    with session_scope() as session:
        # Check if user already exists
        existing = session.query(User).filter_by(username=username).first()
        if existing:
            print(f"  ⚠️  User {username} already exists, updating...")
            existing.update_from_dict(user_data)
        else:
            user = User.from_dict(username, user_data)
            session.add(user)
        
        session.commit()

if __name__ == "__main__":
    # Argumenty: --dry-run lub --migrate
    dry_run = "--migrate" not in sys.argv
    
    if dry_run:
        print("🔍 RUNNING IN DRY-RUN MODE")
        print("Use --migrate flag to actually migrate data\n")
    else:
        print("⚠️  LIVE MIGRATION MODE")
        print("This will modify the database!\n")
        confirm = input("Are you sure you want to continue? (yes/no): ")
        if confirm.lower() != "yes":
            print("Migration cancelled.")
            sys.exit(0)
    
    success = migrate_all_users(dry_run=dry_run)
    
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration completed with errors!")
        sys.exit(1)
```

---

### FAZA 4: Rollback Strategy (Dzień 10)

**File: `database/migrations/rollback.py`**

```python
import json
import shutil
from pathlib import Path
from datetime import datetime
from database.models import User, session_scope
from database.connection import get_session

def rollback_to_json(backup_dir: str):
    """
    Przywraca dane z backupu JSON
    
    Args:
        backup_dir: Ścieżka do katalogu z backupem
    """
    backup_path = Path(backup_dir)
    
    if not backup_path.exists():
        print(f"❌ Backup directory not found: {backup_dir}")
        return False
    
    # Verify manifest
    manifest_path = backup_path / "manifest.json"
    if not manifest_path.exists():
        print("❌ Backup manifest not found!")
        return False
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    print(f"📦 Restoring from backup: {manifest['timestamp']}")
    print(f"Files to restore: {len(manifest['files'])}")
    
    # Restore each file
    for file in manifest["files"]:
        source = backup_path / file
        dest = Path(file)
        
        if source.exists():
            # Create backup of current file first
            if dest.exists():
                current_backup = dest.parent / f"{dest.name}.before_rollback"
                shutil.copy2(dest, current_backup)
                print(f"  📋 Backed up current: {current_backup}")
            
            # Restore from backup
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            print(f"  ✅ Restored: {file}")
        else:
            print(f"  ⚠️  File not in backup: {file}")
    
    print("\n✅ Rollback completed!")
    print("⚠️  Remember to update migration_config.json to use 'json' backend")
    
    return True

def export_sql_to_json(output_file: str = "users_data_from_sql.json"):
    """
    Eksportuje dane z SQL z powrotem do JSON (dla bezpieczeństwa)
    """
    output_path = Path(output_file)
    
    print("📤 Exporting SQL data to JSON...")
    
    users_dict = {}
    with session_scope() as session:
        users = session.query(User).all()
        for user in users:
            users_dict[user.username] = user.to_dict()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(users_dict, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported {len(users_dict)} users to {output_file}")
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python rollback.py <backup_dir>  - Restore from backup")
        print("  python rollback.py --export      - Export SQL to JSON")
        sys.exit(1)
    
    if sys.argv[1] == "--export":
        export_sql_to_json()
    else:
        backup_dir = sys.argv[1]
        rollback_to_json(backup_dir)
```

---

## 📋 CHECKLIST WDROŻENIA

### Przed Migracją
- [ ] Backup wszystkich plików JSON
- [ ] Testy wszystkich krytycznych funkcji (business games!)
- [ ] Dokumentacja obecnej struktury danych
- [ ] Plan komunikacji z użytkownikami
- [ ] Przygotowanie środowiska testowego

### Podczas Migracji
- [ ] Migracja w trybie "dual write" (minimum 1 tydzień)
- [ ] Monitoring błędów w logach
- [ ] Stopniowe włączanie SQL dla użytkowników (5% → 25% → 50% → 100%)
- [ ] Weryfikacja integralności danych
- [ ] Testy wydajnościowe

### Po Migracji
- [ ] Weryfikacja wszystkich funkcji
- [ ] Testy business games (scenariusze, kontrakty)
- [ ] Monitoring przez minimum 2 tygodnie
- [ ] Archiwizacja starych plików JSON (nie usuwać!)
- [ ] Dokumentacja nowej architektury

---

## 🚨 CRITICAL: Business Games Specific Concerns

### Problem z Poprzedniej Migracji
> "poprzednio były problemy z danymi z business games i był kłopot z włączaniem scenariuszu"

### Rozwiązanie

1. **Separate Business Game Repository**
   - Dedykowany `BusinessGameRepository` z specjalną obsługą
   - Atomowe transakcje dla inicjalizacji scenariusza
   - Walidacja przed zapisem

2. **Scenario Initialization Protection**
```python
def initialize_scenario_safely(username, industry_id, scenario_id):
    """Bezpieczna inicjalizacja scenariusza z rollback"""
    # 1. Backup current state
    current_state = get_business_game_data(username, industry_id)
    
    try:
        # 2. Initialize new scenario
        new_state = initialize_business_game_with_scenario(
            username, industry_id, scenario_id
        )
        
        # 3. Validate
        if not validate_business_game_state(new_state):
            raise ValueError("Invalid game state after initialization")
        
        # 4. Save
        save_business_game_data(username, industry_id, new_state)
        
        return True
    except Exception as e:
        # ROLLBACK
        if current_state:
            save_business_game_data(username, industry_id, current_state)
        raise e
```

3. **Validation Schema**
```python
BUSINESS_GAME_REQUIRED_FIELDS = {
    "scenario_id",
    "firm",
    "employees",
    "office",
    "contracts",
    "stats",
    "money",
    "history"
}

def validate_business_game_state(bg_data):
    """Waliduje czy stan gry jest poprawny"""
    # Check required fields
    for field in BUSINESS_GAME_REQUIRED_FIELDS:
        if field not in bg_data:
            return False
    
    # Check firma
    if "name" not in bg_data["firm"]:
        return False
    
    # Check contracts structure
    if "active" not in bg_data["contracts"]:
        return False
    
    return True
```

---

## 📈 Timeline

| Faza | Czas | Status |
|------|------|--------|
| Faza 0: Backup & Przygotowanie | 2 dni | ⏳ |
| Faza 1: Warstwa Abstrakcji | 3 dni | ⏳ |
| Faza 2: SQL Models | 2 dni | ⏳ |
| Faza 3: Migracja Testowa | 2 dni | ⏳ |
| Faza 4: Dual-Write Mode | 7 dni | ⏳ |
| Faza 5: Stopniowe Przejście na SQL | 7 dni | ⏳ |
| Faza 6: Monitoring & Stabilizacja | 14 dni | ⏳ |
| **TOTAL** | **~5 tygodni** | |

---

## 🎯 Następne Kroki

**Co robić teraz?**

1. **Przejrzyj ten dokument** i zdecyduj czy zgadzasz się z podejściem
2. **Zdecyduj o bazie danych**: SQLite (prosty start) vs PostgreSQL (production-ready)
3. **Stwórz backup** używając `scripts/create_full_backup.py`
4. **Rozpocznij implementację** od Fazy 1 (Repository Pattern)

**Czy mam przystąpić do implementacji?**
- Option A: Rozpocznij od backupu i Base Repository
- Option B: Najpierw przetestuj migrację tylko użytkowników (bez business_games)
- Option C: Chcesz jeszcze coś zmienić w planie?
