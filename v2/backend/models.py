from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator
from datetime import datetime
import json

from .database import Base

# Custom JSON Type for SQLite using TEXT
class JSONEncoded(TypeDecorator):
    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(128))
    
    # Missing in DB but present in original model - will be added by migration script
    email = Column(String(100), unique=True, index=True)
    full_name = Column(String(100))
    
    # Gamification Stats
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    degencoins = Column(Integer, default=0)
    
    # Profile & Business Data
    degen_type = Column(String(50))
    company = Column(String(100))
    avatar_url = Column(String(255))
    preferences = Column(JSONEncoded) # Settings: { theme: 'glass' | 'minimal', ... }
    permissions = Column(JSONEncoded)
    account_created_by = Column(String(100))
    
    # Dates & Flags
    joined_date = Column(Date, default=datetime.utcnow)
    last_login = Column(DateTime)
    test_taken = Column(Boolean, default=False)
    intro_completed = Column(Boolean, default=False)
    
    # System
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    activities = relationship("ActivityLog", back_populates="user")
    lesson_progress = relationship("LessonProgress", back_populates="user")
    tool_results = relationship("ToolResult", back_populates="user")

class Lesson(Base):
    __tablename__ = "lessons"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, index=True) # e.g. "intro-1"
    title = Column(String)
    description = Column(String)
    category = Column(String)
    video_url = Column(String)
    thumbnail_url = Column(String, nullable=True)
    duration = Column(Integer) # in seconds
    xp_reward = Column(Integer, default=100)
    difficulty = Column(String, default="Beginner")
    order = Column(Integer, default=0)

    progress_entries = relationship("LessonProgress", back_populates="lesson")

class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Changed to Integer ID to match User.id
    lesson_id = Column(String, ForeignKey("lessons.id"))
    completed = Column(Boolean, default=False)
    watched_duration = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="progress_entries")

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False, index=True)
    activity_type = Column(String(50), nullable=False)
    description = Column(String(255))
    metadata_json = Column(JSONEncoded, nullable=True)
    xp_awarded = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activities")

class ToolResult(Base):
    __tablename__ = "tool_results"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False, index=True)
    tool_id = Column(String(50), nullable=False) # e.g. "milwaukee_app_wizard"
    
    input_data = Column(JSONEncoded) # Kontekst i odpowiedzi
    output_data = Column(JSONEncoded) # Wygenerowana rekomendacja
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="tool_results")

# Update User model to include tool_results
# To bedzie wymagalo edycji klasy User wyzej, ale zrobie to w osobnym chunku albo zostawie bez back_populates jesli nie kluczowe.
# Lepiej dodac back_populates dla spojnosci.
