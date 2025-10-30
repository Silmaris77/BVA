"""
Migrate database schema - dodaj tabele dla lekcji
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from database.connection import get_engine
from database.models import Base, LessonProgress, CompletedLesson, LessonAccess

print("="*60)
print("🔄 MIGRATING DATABASE SCHEMA")
print("="*60)

# Get engine
engine = get_engine()

# Utwórz nowe tabele (istniejące zostaną pominięte)
Base.metadata.create_all(engine)

print("\n✅ Schema migration complete!")
print("   Created tables:")
print("   - lesson_progress")
print("   - completed_lessons")
print("   - lesson_access")
