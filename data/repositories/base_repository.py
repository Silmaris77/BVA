"""
Base Repository - Abstrakcyjna klasa bazowa dla wszystkich repozytoriów
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import json
from pathlib import Path


class BaseRepository(ABC):
    """
    Abstrakcyjna klasa bazowa dla repozytoriów
    
    Implementuje logikę wyboru backendu (JSON vs SQL) oraz dual-write mode.
    """
    
    def __init__(self, backend: Optional[str] = None):
        """
        Args:
            backend: "json" | "sql" | "dual" | None (auto z config)
        """
        self._load_config()
        self.backend = backend or self.config.get("storage_backend", "json")
    
    def _load_config(self):
        """Ładuje konfigurację migracji"""
        config_path = Path(__file__).parent.parent.parent / "config" / "migration_config.json"
        
        if config_path.exists():
            with open(config_path, encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            # Domyślna konfiguracja
            self.config = {
                "storage_backend": "json",
                "dual_write_enabled": False,
                "per_user_backend": {"*": "json"},
                "feature_flags": {
                    "enable_sql_read": False,
                    "enable_sql_write": False
                }
            }
    
    def _should_use_sql_for_read(self, identifier: Optional[str] = None) -> bool:
        """
        Decyduje czy użyć SQL do odczytu na podstawie konfiguracji
        
        Args:
            identifier: username lub inny identyfikator (dla per-user config)
        
        Returns:
            bool: True jeśli należy użyć SQL
        """
        # Sprawdź global feature flag
        if not self.config.get("feature_flags", {}).get("enable_sql_read", False):
            return False
        
        # Backend ustawiony bezpośrednio
        if self.backend == "sql":
            return True
        elif self.backend == "json":
            return False
        
        # Per-user configuration
        if identifier:
            per_user = self.config.get("per_user_backend", {})
            user_backend = per_user.get(identifier, per_user.get("*", "json"))
            return user_backend == "sql"
        
        # Domyślnie JSON
        return False
    
    def _should_use_sql_for_write(self, identifier: Optional[str] = None) -> bool:
        """
        Decyduje czy użyć SQL do zapisu na podstawie konfiguracji
        
        Args:
            identifier: username lub inny identyfikator (dla per-user config)
        
        Returns:
            bool: True jeśli należy użyć SQL
        """
        # Sprawdź global feature flag
        if not self.config.get("feature_flags", {}).get("enable_sql_write", False):
            return False
        
        # Backend ustawiony bezpośrednio
        if self.backend == "sql":
            return True
        elif self.backend == "json":
            return False
        
        # Per-user configuration
        if identifier:
            per_user = self.config.get("per_user_backend", {})
            user_backend = per_user.get(identifier, per_user.get("*", "json"))
            return user_backend == "sql"
        
        # Domyślnie JSON
        return False
    
    def _is_dual_write_enabled(self) -> bool:
        """Sprawdza czy dual-write jest włączony"""
        return (
            self.config.get("dual_write_enabled", False) or 
            self.config.get("feature_flags", {}).get("enable_dual_write", False)
        )
    
    def _validate_before_save(self) -> bool:
        """Sprawdza czy walidacja jest włączona"""
        return self.config.get("validation", {}).get("validate_before_save", True)
    
    @abstractmethod
    def get(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Pobiera dane
        
        Args:
            identifier: Unikalny identyfikator (np. username)
        
        Returns:
            Dict z danymi lub None jeśli nie znaleziono
        """
        pass
    
    @abstractmethod
    def save(self, identifier: str, data: Dict[str, Any]) -> bool:
        """
        Zapisuje dane
        
        Args:
            identifier: Unikalny identyfikator
            data: Dane do zapisania
        
        Returns:
            bool: True jeśli sukces
        """
        pass
    
    @abstractmethod
    def delete(self, identifier: str) -> bool:
        """
        Usuwa dane
        
        Args:
            identifier: Unikalny identyfikator
        
        Returns:
            bool: True jeśli sukces
        """
        pass
    
    @abstractmethod
    def exists(self, identifier: str) -> bool:
        """
        Sprawdza czy dane istnieją
        
        Args:
            identifier: Unikalny identyfikator
        
        Returns:
            bool: True jeśli istnieje
        """
        pass
    
    def validate_data(self, data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Waliduje dane przed zapisem
        
        Args:
            data: Dane do walidacji
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Bazowa walidacja - override w podklasach dla specyficznej logiki
        if not isinstance(data, dict):
            return False, "Data must be a dictionary"
        
        return True, None
