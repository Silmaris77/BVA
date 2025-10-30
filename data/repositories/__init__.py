"""
Repository Layer - Warstwa abstrakcji dostępu do danych

Ten moduł implementuje Repository Pattern, który umożliwia:
- Przełączanie między JSON a SQL bez zmiany kodu aplikacji
- Dual-write mode (zapis do obu źródeł jednocześnie)
- Stopniowe migrowanie użytkowników
- Łatwy rollback w razie problemów
"""

from .base_repository import BaseRepository
from .user_repository import UserRepository
from .business_game_repository import BusinessGameRepository
from .lesson_repository import LessonRepository

__all__ = [
    'BaseRepository',
    'UserRepository',
    'BusinessGameRepository',
    'LessonRepository',
]
