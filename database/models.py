"""
SQLAlchemy Models
Modele bazy danych dla systemu BVA
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, Date, DateTime, 
    DECIMAL, Text, ForeignKey, Index, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator, VARCHAR
from datetime import datetime
import json
import uuid

Base = declarative_base()


# Custom type for UUID (compatible with SQLite)
class GUID(TypeDecorator):
    """Platform-independent GUID type"""
    impl = VARCHAR
    cache_ok = True
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)
    
    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            else:
                return value


# Custom type for JSON (compatible with SQLite)
class JSONEncoded(TypeDecorator):
    """JSON type that works with SQLite and PostgreSQL"""
    impl = Text
    cache_ok = True
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value, ensure_ascii=False)
        return None
    
    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None


# =============================================================================
# USER MODEL
# =============================================================================
class User(Base):
    __tablename__ = 'users'
    
    # Primary fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(GUID(), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    degen_type = Column(String(50))
    xp = Column(Integer, default=0)
    degencoins = Column(Integer, default=0)
    level = Column(Integer, default=1)
    
    # Timestamps
    joined_date = Column(Date, nullable=False, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Flags
    test_taken = Column(Boolean, default=False)
    
    # System
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lesson_progress = relationship("LessonProgress", back_populates="user", cascade="all, delete-orphan")
    completed_lessons = relationship("CompletedLesson", back_populates="user", cascade="all, delete-orphan")
    lesson_access = relationship("LessonAccess", back_populates="user", cascade="all, delete-orphan")
    # badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    
    def to_dict(self, include_relations=False):
        """
        Konwertuje model do dict (kompatybilny z formatem JSON)
        
        Args:
            include_relations: Czy dołączyć powiązane dane (lessons, badges, etc.)
        
        Returns:
            dict: Dane użytkownika w formacie JSON
        """
        result = {
            "user_id": str(self.user_id),
            "password": self.password_hash,
            "degen_type": self.degen_type,
            "xp": self.xp,
            "degencoins": self.degencoins,
            "level": self.level,
            "joined_date": self.joined_date.strftime("%Y-%m-%d") if self.joined_date else None,
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S") if self.last_login else None,
            "test_taken": self.test_taken,
        }
        
        # Add relations when requested
        if include_relations:
            result["completed_lessons"] = [cl.lesson_id for cl in self.completed_lessons]
            result["lesson_access"] = {la.lesson_id: la.has_access for la in self.lesson_access}
            result["lesson_progress"] = {}
            for lp in self.lesson_progress:
                if lp.lesson_id not in result["lesson_progress"]:
                    result["lesson_progress"][lp.lesson_id] = {}
                result["lesson_progress"][lp.lesson_id][f"{lp.section_name}_xp_awarded"] = lp.xp_awarded
                result["lesson_progress"][lp.lesson_id][f"{lp.section_name}_completed"] = lp.completed
                result["lesson_progress"][lp.lesson_id][f"{lp.section_name}_xp"] = lp.xp
                result["lesson_progress"][lp.lesson_id][f"{lp.section_name}_degencoins"] = lp.degencoins
                if lp.timestamp:
                    result["lesson_progress"][lp.lesson_id][f"{lp.section_name}_timestamp"] = lp.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            # result["badges"] = [b.badge_id for b in self.badges]
        
        return result
    
    @classmethod
    def from_dict(cls, username, data):
        """
        Tworzy model User z dict (z formatu JSON)
        
        Args:
            username: Nazwa użytkownika
            data: Dict z danymi użytkownika (format JSON)
        
        Returns:
            User: Nowa instancja modelu
        """
        # Parse user_id
        user_id_str = data.get("user_id")
        if user_id_str:
            try:
                user_id = uuid.UUID(user_id_str)
            except (ValueError, AttributeError):
                user_id = uuid.uuid4()
        else:
            user_id = uuid.uuid4()
        
        # Parse dates
        joined_date = None
        if data.get("joined_date"):
            try:
                joined_date = datetime.strptime(data["joined_date"], "%Y-%m-%d").date()
            except (ValueError, TypeError):
                joined_date = datetime.utcnow().date()
        else:
            joined_date = datetime.utcnow().date()
        
        last_login = None
        if data.get("last_login"):
            try:
                last_login = datetime.strptime(data["last_login"], "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                pass
        
        return cls(
            user_id=user_id,
            username=username,
            password_hash=data.get("password", ""),
            degen_type=data.get("degen_type"),
            xp=data.get("xp", 0),
            degencoins=data.get("degencoins", 0),
            level=data.get("level", 1),
            joined_date=joined_date,
            last_login=last_login,
            test_taken=data.get("test_taken", False)
        )
    
    def update_from_dict(self, data):
        """
        Aktualizuje model z dict (z formatu JSON)
        
        Args:
            data: Dict z danymi użytkownika (format JSON)
        """
        # Update basic fields
        if "password" in data:
            self.password_hash = data["password"]
        if "degen_type" in data:
            self.degen_type = data["degen_type"]
        if "xp" in data:
            self.xp = data["xp"]
        if "degencoins" in data:
            self.degencoins = data["degencoins"]
        if "level" in data:
            self.level = data["level"]
        if "test_taken" in data:
            self.test_taken = data["test_taken"]
        
        # Update dates
        if "last_login" in data and data["last_login"]:
            try:
                self.last_login = datetime.strptime(data["last_login"], "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                pass
        
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<User(username='{self.username}', level={self.level}, xp={self.xp})>"


# =============================================================================
# LESSON MODELS
# =============================================================================

class LessonProgress(Base):
    """Model dla postępu w lekcjach (intro, content, quiz, etc.)"""
    __tablename__ = 'lesson_progress'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(GUID(), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    lesson_id = Column(String(255), nullable=False)
    section_name = Column(String(100), nullable=False)  # intro, content, practical_exercises, summary
    
    xp_awarded = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
    xp = Column(Integer, default=0)
    degencoins = Column(Integer, default=0)
    timestamp = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="lesson_progress")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'lesson_id', 'section_name', name='uix_user_lesson_section'),
        Index('idx_user_lesson', 'user_id', 'lesson_id'),
    )
    
    def to_dict(self):
        """Konwertuje do formatu JSON"""
        return {
            f"{self.section_name}_xp_awarded": self.xp_awarded,
            f"{self.section_name}_completed": self.completed,
            f"{self.section_name}_xp": self.xp,
            f"{self.section_name}_degencoins": self.degencoins,
            f"{self.section_name}_timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S") if self.timestamp else None
        }
    
    @staticmethod
    def from_dict(user_id: uuid.UUID, lesson_id: str, section_name: str, data: dict):
        """Tworzy model z formatu JSON"""
        timestamp = None
        timestamp_str = data.get(f"{section_name}_timestamp")
        if timestamp_str:
            try:
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                pass
        
        return LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            section_name=section_name,
            xp_awarded=data.get(f"{section_name}_xp_awarded", False),
            completed=data.get(f"{section_name}_completed", False),
            xp=data.get(f"{section_name}_xp", 0),
            degencoins=data.get(f"{section_name}_degencoins", 0),
            timestamp=timestamp
        )


class CompletedLesson(Base):
    """Model dla ukończonych lekcji"""
    __tablename__ = 'completed_lessons'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(GUID(), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    lesson_id = Column(String(255), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="completed_lessons")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'lesson_id', name='uix_user_completed_lesson'),
        Index('idx_user_completed', 'user_id'),
    )


class LessonAccess(Base):
    """Model dla dostępu do lekcji"""
    __tablename__ = 'lesson_access'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(GUID(), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    lesson_id = Column(String(255), nullable=False)
    has_access = Column(Boolean, default=False)
    granted_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="lesson_access")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'lesson_id', name='uix_user_lesson_access'),
        Index('idx_user_access', 'user_id'),
    )


# =============================================================================
# BUSINESS GAMES MODELS
# =============================================================================

class BusinessGame(Base):
    """
    Model dla business games - główna tabela scenariuszy
    Obsługuje różne typy scenariuszy: consulting, marketing, hr, etc.
    """
    __tablename__ = 'business_games'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(GUID(), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    scenario_type = Column(String(50), nullable=False, index=True)  # consulting, marketing, hr, etc.
    scenario_id = Column(String(50))  # lifetime, challenge_30days, etc.
    
    # Firm data
    firm_name = Column(String(200))
    firm_logo = Column(String(10))
    firm_founded = Column(Date)
    firm_level = Column(Integer, default=1)
    firm_reputation = Column(Integer, default=0)
    
    # Office data
    office_type = Column(String(50), default='home_office')
    office_upgraded_at = Column(DateTime)
    
    # Financial data
    money = Column(Integer, default=0)
    initial_money = Column(Integer, default=0)
    
    # Scenario configuration
    scenario_modifiers = Column(JSONEncoded)  # Modyfikatory scenariusza
    scenario_objectives = Column(JSONEncoded)  # Cele scenariusza
    objectives_completed = Column(JSONEncoded)  # Ukończone cele
    
    # Ranking & Events
    ranking = Column(JSONEncoded)
    events = Column(JSONEncoded)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref="business_games")
    employees = relationship("BusinessGameEmployee", back_populates="game", cascade="all, delete-orphan")
    contracts = relationship("BusinessGameContract", back_populates="game", cascade="all, delete-orphan")
    transactions = relationship("BusinessGameTransaction", back_populates="game", cascade="all, delete-orphan")
    stats = relationship("BusinessGameStats", back_populates="game", uselist=False, cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'scenario_type', name='uix_user_scenario_type'),
        Index('idx_user_scenario', 'user_id', 'scenario_type'),
    )
    
    def to_dict(self):
        """Konwertuje model SQL do formatu JSON używanego w aplikacji"""
        return {
            'scenario_id': self.scenario_id,
            'scenario_modifiers': self.scenario_modifiers or {},
            'scenario_objectives': self.scenario_objectives or [],
            'objectives_completed': self.objectives_completed or [],
            'firm': {
                'name': self.firm_name,
                'logo': self.firm_logo,
                'founded': self.firm_founded.strftime('%Y-%m-%d') if self.firm_founded else None,
                'level': self.firm_level,
                'reputation': self.firm_reputation
            },
            'employees': [emp.to_dict() for emp in self.employees],
            'office': {
                'type': self.office_type,
                'upgraded_at': self.office_upgraded_at.strftime('%Y-%m-%d %H:%M:%S') if self.office_upgraded_at else None
            },
            'contracts': {
                'active': [c.to_dict() for c in self.contracts if c.status == 'active'],
                'completed': [c.to_dict() for c in self.contracts if c.status == 'completed'],
                'failed': [c.to_dict() for c in self.contracts if c.status == 'failed'],
                'available_pool': [c.to_dict() for c in self.contracts if c.status == 'available']
            },
            'stats': self.stats.to_dict() if self.stats else {},
            'ranking': self.ranking or {},
            'events': self.events or {},
            'money': self.money,
            'history': {
                'transactions': [t.to_dict() for t in self.transactions],
                'level_ups': []  # TODO: implementować jeśli potrzebne
            },
            'initial_money': self.initial_money
        }
    
    @staticmethod
    def from_dict(user_id: str, scenario_type: str, data: dict):
        """Tworzy model SQL z formatu JSON używanego w aplikacji"""
        firm = data.get('firm', {})
        office = data.get('office', {})
        
        game = BusinessGame(
            user_id=user_id,
            scenario_type=scenario_type,
            scenario_id=data.get('scenario_id'),
            firm_name=firm.get('name'),
            firm_logo=firm.get('logo'),
            firm_founded=datetime.strptime(firm.get('founded'), '%Y-%m-%d').date() if firm.get('founded') else None,
            firm_level=firm.get('level', 1),
            firm_reputation=firm.get('reputation', 0),
            office_type=office.get('type', 'home_office'),
            office_upgraded_at=datetime.strptime(office.get('upgraded_at'), '%Y-%m-%d %H:%M:%S') if office.get('upgraded_at') else None,
            money=data.get('money', 0),
            initial_money=data.get('initial_money', 0),
            scenario_modifiers=data.get('scenario_modifiers', {}),
            scenario_objectives=data.get('scenario_objectives', []),
            objectives_completed=data.get('objectives_completed', []),
            ranking=data.get('ranking', {}),
            events=data.get('events', {})
        )
        
        return game
    
    def __repr__(self):
        return f"<BusinessGame(user_id='{self.user_id}', scenario='{self.scenario_type}', level={self.firm_level})>"


class BusinessGameEmployee(Base):
    """Model dla pracowników w business game"""
    __tablename__ = 'business_game_employees'
    
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('business_games.id', ondelete='CASCADE'), nullable=False, index=True)
    
    employee_id = Column(String(50), nullable=False)
    name = Column(String(200))
    role = Column(String(100))
    hired_date = Column(Date)
    salary = Column(Integer)
    
    # Skills & Stats
    skills = Column(JSONEncoded)  # Dictionary of skills
    performance = Column(Integer)
    satisfaction = Column(Integer)
    
    # Additional data
    extra_data = Column(JSONEncoded)  # Any other employee-specific data
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    game = relationship("BusinessGame", back_populates="employees")
    
    __table_args__ = (
        Index('idx_game_employee', 'game_id', 'employee_id'),
    )
    
    def to_dict(self):
        """Konwertuje model SQL do formatu JSON"""
        base_dict = {
            'id': self.employee_id,
            'name': self.name,
            'role': self.role,
            'hired_date': self.hired_date.strftime('%Y-%m-%d') if self.hired_date else None,
            'salary': self.salary,
            'skills': self.skills or {},
            'performance': self.performance,
            'satisfaction': self.satisfaction
        }
        
        # Add extra data if present
        if self.extra_data:
            base_dict.update(self.extra_data)
        
        return base_dict
    
    @staticmethod
    def from_dict(game_id: int, data: dict):
        """Tworzy model SQL z formatu JSON"""
        # Separate known fields from extra fields
        known_fields = {'id', 'name', 'role', 'hired_date', 'salary', 'skills', 'performance', 'satisfaction'}
        extra_data = {k: v for k, v in data.items() if k not in known_fields}
        
        return BusinessGameEmployee(
            game_id=game_id,
            employee_id=data.get('id'),
            name=data.get('name'),
            role=data.get('role'),
            hired_date=datetime.strptime(data.get('hired_date'), '%Y-%m-%d').date() if data.get('hired_date') else None,
            salary=data.get('salary'),
            skills=data.get('skills', {}),
            performance=data.get('performance'),
            satisfaction=data.get('satisfaction'),
            extra_data=extra_data if extra_data else None
        )


class BusinessGameContract(Base):
    """Model dla kontraktów w business game"""
    __tablename__ = 'business_game_contracts'
    
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('business_games.id', ondelete='CASCADE'), nullable=False, index=True)
    
    contract_id = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, index=True)  # active, completed, failed, available
    
    # Contract details
    title = Column(String(500))  # tytul
    category = Column(String(100))  # kategoria
    client = Column(String(200))  # klient
    description = Column(Text)  # opis
    task = Column(Text)  # zadanie
    
    # Difficulty & Rewards
    difficulty = Column(Integer)  # trudnosc
    base_reward = Column(Integer)  # nagroda_base
    reward_4star = Column(Integer)  # nagroda_4star
    reward_5star = Column(Integer)  # nagroda_5star
    reputation = Column(Integer)  # reputacja
    
    # Requirements & Time
    required_knowledge = Column(JSONEncoded)  # wymagana_wiedza
    duration_days = Column(Integer)  # czas_realizacji_dni
    required_level = Column(Integer)  # wymagany_poziom
    min_words = Column(Integer)  # min_slow
    
    # Metadata
    emoji = Column(String(10))
    available_until = Column(DateTime)
    
    # Completion data (for completed/failed contracts)
    completed_at = Column(DateTime)
    rating = Column(Integer)  # 1-5 stars
    earned_money = Column(Integer)
    user_response = Column(Text)  # Odpowiedź użytkownika
    ai_feedback = Column(Text)  # Feedback od AI
    
    # Additional contract-specific data
    extra_data = Column(JSONEncoded)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    game = relationship("BusinessGame", back_populates="contracts")
    
    __table_args__ = (
        Index('idx_game_contract', 'game_id', 'contract_id'),
        Index('idx_game_status', 'game_id', 'status'),
    )
    
    def to_dict(self):
        """Konwertuje model SQL do formatu JSON"""
        base_dict = {
            'id': self.contract_id,
            'tytul': self.title,
            'kategoria': self.category,
            'klient': self.client,
            'opis': self.description,
            'zadanie': self.task,
            'trudnosc': self.difficulty,
            'nagroda_base': self.base_reward,
            'nagroda_4star': self.reward_4star,
            'nagroda_5star': self.reward_5star,
            'reputacja': self.reputation,
            'wymagana_wiedza': self.required_knowledge or [],
            'czas_realizacji_dni': self.duration_days,
            'wymagany_poziom': self.required_level,
            'min_slow': self.min_words,
            'emoji': self.emoji,
            'available_until': self.available_until.strftime('%Y-%m-%d %H:%M:%S') if self.available_until else None
        }
        
        # Add completion data if applicable
        if self.status in ['completed', 'failed']:
            base_dict.update({
                'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None,
                'rating': self.rating,
                'earned_money': self.earned_money,
                'user_response': self.user_response,
                'ai_feedback': self.ai_feedback
            })
        
        # Add extra data if present
        if self.extra_data:
            base_dict.update(self.extra_data)
        
        return base_dict
    
    @staticmethod
    def from_dict(game_id: int, status: str, data: dict):
        """Tworzy model SQL z formatu JSON"""
        # Parse available_until if present
        available_until = None
        if data.get('available_until'):
            try:
                available_until = datetime.strptime(data['available_until'], '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                pass
        
        # Parse completed_at if present
        completed_at = None
        if data.get('completed_at'):
            try:
                completed_at = datetime.strptime(data['completed_at'], '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                pass
        
        # Known fields
        known_fields = {
            'id', 'tytul', 'kategoria', 'klient', 'opis', 'zadanie',
            'trudnosc', 'nagroda_base', 'nagroda_4star', 'nagroda_5star',
            'reputacja', 'wymagana_wiedza', 'czas_realizacji_dni',
            'wymagany_poziom', 'min_slow', 'emoji', 'available_until',
            'completed_at', 'rating', 'earned_money', 'user_response', 'ai_feedback'
        }
        extra_data = {k: v for k, v in data.items() if k not in known_fields}
        
        return BusinessGameContract(
            game_id=game_id,
            contract_id=data.get('id'),
            status=status,
            title=data.get('tytul'),
            category=data.get('kategoria'),
            client=data.get('klient'),
            description=data.get('opis'),
            task=data.get('zadanie'),
            difficulty=data.get('trudnosc'),
            base_reward=data.get('nagroda_base'),
            reward_4star=data.get('nagroda_4star'),
            reward_5star=data.get('nagroda_5star'),
            reputation=data.get('reputacja'),
            required_knowledge=data.get('wymagana_wiedza', []),
            duration_days=data.get('czas_realizacji_dni'),
            required_level=data.get('wymagany_poziom'),
            min_words=data.get('min_slow'),
            emoji=data.get('emoji'),
            available_until=available_until,
            completed_at=completed_at,
            rating=data.get('rating'),
            earned_money=data.get('earned_money'),
            user_response=data.get('user_response'),
            ai_feedback=data.get('ai_feedback'),
            extra_data=extra_data if extra_data else None
        )


class BusinessGameTransaction(Base):
    """Model dla transakcji finansowych w business game"""
    __tablename__ = 'business_game_transactions'
    
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('business_games.id', ondelete='CASCADE'), nullable=False, index=True)
    
    transaction_type = Column(String(50))  # salary, contract_payment, office_upgrade, etc.
    amount = Column(Integer)
    description = Column(String(500))
    
    # Metadata
    related_contract_id = Column(String(50))  # If related to a contract
    related_employee_id = Column(String(50))  # If related to an employee
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Additional transaction data
    extra_data = Column(JSONEncoded)
    
    game = relationship("BusinessGame", back_populates="transactions")
    
    __table_args__ = (
        Index('idx_game_transaction', 'game_id', 'timestamp'),
    )
    
    def to_dict(self):
        """Konwertuje model SQL do formatu JSON"""
        base_dict = {
            'type': self.transaction_type,
            'amount': self.amount,
            'description': self.description,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S') if self.timestamp else None
        }
        
        if self.related_contract_id:
            base_dict['contract_id'] = self.related_contract_id
        if self.related_employee_id:
            base_dict['employee_id'] = self.related_employee_id
        
        # Add extra data if present
        if self.extra_data:
            base_dict.update(self.extra_data)
        
        return base_dict
    
    @staticmethod
    def from_dict(game_id: int, data: dict):
        """Tworzy model SQL z formatu JSON"""
        # Parse timestamp if present
        timestamp = None
        if data.get('timestamp'):
            try:
                timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                timestamp = datetime.utcnow()
        else:
            timestamp = datetime.utcnow()
        
        # Known fields
        known_fields = {'type', 'amount', 'description', 'timestamp', 'contract_id', 'employee_id'}
        extra_data = {k: v for k, v in data.items() if k not in known_fields}
        
        return BusinessGameTransaction(
            game_id=game_id,
            transaction_type=data.get('type'),
            amount=data.get('amount'),
            description=data.get('description'),
            related_contract_id=data.get('contract_id'),
            related_employee_id=data.get('employee_id'),
            timestamp=timestamp,
            extra_data=extra_data if extra_data else None
        )


class BusinessGameStats(Base):
    """Model dla statystyk business game"""
    __tablename__ = 'business_game_stats'
    
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('business_games.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    
    # Overall stats
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
    avg_rating = Column(DECIMAL(3, 2), default=0.0)
    
    # Category stats and time-based stats (stored as JSON)
    category_stats = Column(JSONEncoded)  # Stats per category
    last_30_days = Column(JSONEncoded)  # Last 30 days stats
    last_7_days = Column(JSONEncoded)  # Last 7 days stats
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    game = relationship("BusinessGame", back_populates="stats")
    
    def to_dict(self):
        """Konwertuje model SQL do formatu JSON"""
        return {
            'total_revenue': self.total_revenue,
            'total_costs': self.total_costs,
            'net_profit': self.net_profit,
            'contracts_completed': self.contracts_completed,
            'contracts_5star': self.contracts_5star,
            'contracts_4star': self.contracts_4star,
            'contracts_3star': self.contracts_3star,
            'contracts_2star': self.contracts_2star,
            'contracts_1star': self.contracts_1star,
            'avg_rating': float(self.avg_rating) if self.avg_rating else 0.0,
            'category_stats': self.category_stats or {},
            'last_30_days': self.last_30_days or {},
            'last_7_days': self.last_7_days or {}
        }
    
    @staticmethod
    def from_dict(game_id: int, data: dict):
        """Tworzy model SQL z formatu JSON"""
        return BusinessGameStats(
            game_id=game_id,
            total_revenue=data.get('total_revenue', 0),
            total_costs=data.get('total_costs', 0),
            net_profit=data.get('net_profit', 0),
            contracts_completed=data.get('contracts_completed', 0),
            contracts_5star=data.get('contracts_5star', 0),
            contracts_4star=data.get('contracts_4star', 0),
            contracts_3star=data.get('contracts_3star', 0),
            contracts_2star=data.get('contracts_2star', 0),
            contracts_1star=data.get('contracts_1star', 0),
            avg_rating=data.get('avg_rating', 0.0),
            category_stats=data.get('category_stats', {}),
            last_30_days=data.get('last_30_days', {}),
            last_7_days=data.get('last_7_days', {})
        )


# =============================================================================
# Helper Functions
# =============================================================================

def create_all_tables(engine):
    """Tworzy wszystkie tabele w bazie danych"""
    Base.metadata.create_all(bind=engine)


def drop_all_tables(engine):
    """Usuwa wszystkie tabele z bazy danych"""
    Base.metadata.drop_all(bind=engine)
