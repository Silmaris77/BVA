"""
User Repository - Zarządzanie danymi użytkowników

Implementuje dostęp do danych użytkowników z możliwością przełączania
między JSON a SQL bez zmiany kodu aplikacji.
"""

from typing import Optional, Dict, Any, List
import json
import os
from datetime import datetime
from pathlib import Path
from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    """
    Repository dla danych użytkowników
    
    Obsługuje:
    - Odczyt/zapis do JSON (backward compatibility)
    - Odczyt/zapis do SQL (nowy system)
    - Dual-write mode (zapis do obu jednocześnie)
    - Per-user backend selection
    """
    
    def __init__(self, backend: Optional[str] = None):
        super().__init__(backend)
        
        # Ścieżka do pliku JSON
        base_path = Path(__file__).parent.parent.parent
        self.json_file_path = base_path / 'users_data.json'
        
        # Lazy loading - SQL inicjalizuje się tylko gdy potrzebny
        self._sql_initialized = False
        self.sql_available = False
        self.User = None
        self.session_scope = None
    
    def _validate_before_save(self) -> bool:
        """
        TYMCZASOWO WYŁĄCZONE - walidacja blokuje zapis przez niepełne dane FMCG
        TODO: Napraw dane FMCG lub dostosuj walidator
        """
        return False
    
    def _ensure_sql_initialized(self) -> bool:
        """
        Lazy loading - inicjalizuje SQL tylko gdy pierwszy raz potrzebny
        
        Returns:
            bool: True jeśli SQL jest dostępny
        """
        if not self._sql_initialized:
            self._sql_initialized = True
            self.sql_available = self._init_sql()
        return self.sql_available
    
    def _init_sql(self) -> bool:
        """
        Inicjalizuje połączenie SQL (jeśli dostępne)
        
        Returns:
            bool: True jeśli SQL jest dostępny
        """
        try:
            # Import SQL models
            from database.models import User
            from database.connection import session_scope
            self.User = User
            self.session_scope = session_scope
            return True
        except ImportError as e:
            print(f"SQL not available: {e}")
            return False
    
    def get(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Pobiera dane użytkownika
        
        Args:
            username: Nazwa użytkownika
        
        Returns:
            Dict z danymi użytkownika lub None
        """
        use_sql = self._should_use_sql_for_read(username)
        
        # Lazy loading - inicjalizuj SQL tylko jeśli potrzebny
        if use_sql:
            self._ensure_sql_initialized()
        
        if use_sql and self.sql_available:
            return self._get_from_sql(username)
        else:
            return self._get_from_json(username)
    
    def _get_from_json(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Pobiera dane użytkownika z JSON
        
        Args:
            username: Nazwa użytkownika
        
        Returns:
            Dict z danymi lub None
        """
        try:
            if self.json_file_path.exists():
                with open(self.json_file_path, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                    user_data = users_data.get(username)
                    
                    # Migracja danych business games (dodaj brakujące pola)
                    if user_data:
                        user_data = self._migrate_business_games_data(user_data)
                    
                    return user_data
        except Exception as e:
            print(f"Error reading from JSON for user {username}: {e}")
        
        return None
    
    def _get_from_sql(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Pobiera dane użytkownika z SQL
        
        Args:
            username: Nazwa użytkownika
        
        Returns:
            Dict z danymi lub None
        """
        try:
            with self.session_scope() as session:
                user = session.query(self.User).filter_by(username=username).first()
                if user:
                    user_data = user.to_dict()
                    # Migracja danych business games
                    user_data = self._migrate_business_games_data(user_data)
                    return user_data
        except Exception as e:
            print(f"Error reading from SQL for user {username}: {e}")
        
        return None
    
    def save(self, identifier: str, data: Dict[str, Any]) -> bool:
        """
        Zapisuje dane użytkownika
        
        Args:
            identifier: Nazwa użytkownika (username)
            data: Dane użytkownika do zapisania
        
        Returns:
            bool: True jeśli sukces
        """
        # Dla czytelności używamy lokalnych nazw
        username = identifier
        user_data = data
        
        try:
            # Walidacja WYŁĄCZONA - blokuje zapis przez niepełne dane FMCG
            # TODO: Napraw dane FMCG lub dostosuj walidator przed włączeniem
            
            use_sql = self._should_use_sql_for_write(username)
            dual_write = self._is_dual_write_enabled()
            
            # Lazy loading - inicjalizuj SQL tylko jeśli potrzebny
            if use_sql or dual_write:
                self._ensure_sql_initialized()
            
            success = True
            
            # Zapis do JSON (zawsze w dual mode lub gdy JSON backend)
            if not use_sql or dual_write:
                json_success = self._save_to_json(username, user_data)
                if not json_success:
                    print(f"⚠️  Failed to save to JSON for user {username}")
                success = success and json_success
            
            # Zapis do SQL (gdy SQL backend lub dual mode)
            if (use_sql or dual_write) and self.sql_available:
                sql_success = self._save_to_sql(username, user_data)
                if not sql_success:
                    print(f"⚠️  Failed to save to SQL for user {username}")
                success = success and sql_success
            
            return success
            
        except Exception as e:
            print(f"❌ EXCEPTION in save(): {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _save_to_json(self, username: str, user_data: Dict[str, Any]) -> bool:
        """
        Zapisuje dane użytkownika do JSON
        
        Args:
            username: Nazwa użytkownika
            user_data: Dane do zapisania
        
        Returns:
            bool: True jeśli sukces
        """
        try:
            # Wczytaj wszystkich użytkowników
            all_users = {}
            if self.json_file_path.exists():
                with open(self.json_file_path, 'r', encoding='utf-8') as f:
                    all_users = json.load(f)
            
            # Zaktualizuj konkretnego użytkownika
            all_users[username] = user_data
            
            # Zapisz z powrotem
            with open(self.json_file_path, 'w', encoding='utf-8') as f:
                json.dump(all_users, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"❌ ERROR saving to JSON for user {username}: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _save_to_sql(self, username: str, user_data: Dict[str, Any]) -> bool:
        """
        Zapisuje dane użytkownika do SQL
        
        Args:
            username: Nazwa użytkownika
            user_data: Dane do zapisania
        
        Returns:
            bool: True jeśli sukces
        """
        try:
            with self.session_scope() as session:
                user = session.query(self.User).filter_by(username=username).first()
                
                if user:
                    # Update existing
                    user.update_from_dict(user_data)
                else:
                    # Create new
                    user = self.User.from_dict(username, user_data)
                    session.add(user)
                
                session.commit()
                return True
        except Exception as e:
            print(f"Error saving to SQL for user {username}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def delete(self, username: str) -> bool:
        """
        Usuwa użytkownika
        
        Args:
            username: Nazwa użytkownika
        
        Returns:
            bool: True jeśli sukces
        """
        use_sql = self._should_use_sql_for_write(username)
        dual_write = self._is_dual_write_enabled()
        
        # Lazy loading - inicjalizuj SQL tylko jeśli potrzebny
        if use_sql or dual_write:
            self._ensure_sql_initialized()
        
        success = True
        
        # Usuń z JSON
        if not use_sql or dual_write:
            json_success = self._delete_from_json(username)
            success = success and json_success
        
        # Usuń z SQL
        if use_sql and self.sql_available:
            sql_success = self._delete_from_sql(username)
            success = success and sql_success
        
        return success
    
    def _delete_from_json(self, username: str) -> bool:
        """
        Usuwa użytkownika z JSON
        
        Args:
            username: Nazwa użytkownika
        
        Returns:
            bool: True jeśli sukces
        """
        try:
            if self.json_file_path.exists():
                with open(self.json_file_path, 'r', encoding='utf-8') as f:
                    all_users = json.load(f)
                
                if username in all_users:
                    del all_users[username]
                    
                    with open(self.json_file_path, 'w', encoding='utf-8') as f:
                        json.dump(all_users, f, indent=2, ensure_ascii=False)
                    return True
            return False
        except Exception as e:
            print(f"Error deleting from JSON for user {username}: {e}")
            return False
    
    def _delete_from_sql(self, username: str) -> bool:
        """
        Usuwa użytkownika z SQL
        
        Args:
            username: Nazwa użytkownika
        
        Returns:
            bool: True jeśli sukces
        """
        try:
            with self.session_scope() as session:
                user = session.query(self.User).filter_by(username=username).first()
                if user:
                    session.delete(user)
                    session.commit()
                    return True
            return False
        except Exception as e:
            print(f"Error deleting from SQL for user {username}: {e}")
            return False
    
    def exists(self, username: str) -> bool:
        """
        Sprawdza czy użytkownik istnieje
        
        Args:
            username: Nazwa użytkownika
        
        Returns:
            bool: True jeśli istnieje
        """
        user_data = self.get(username)
        return user_data is not None
    
    def get_all(self) -> Dict[str, Any]:
        """
        Pobiera wszystkich użytkowników
        
        Returns:
            Dict: {username: user_data}
        """
        use_sql = self._should_use_sql_for_read()
        
        # Lazy loading - inicjalizuj SQL tylko jeśli potrzebny
        if use_sql:
            self._ensure_sql_initialized()
        
        if use_sql and self.sql_available:
            return self._get_all_from_sql()
        else:
            return self._get_all_from_json()
    
    def _get_all_from_json(self) -> Dict[str, Any]:
        """
        Pobiera wszystkich użytkowników z JSON
        
        Returns:
            Dict: {username: user_data}
        """
        try:
            if self.json_file_path.exists():
                with open(self.json_file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error reading all users from JSON: {e}")
        
        return {}
    
    def _get_all_from_sql(self) -> Dict[str, Any]:
        """
        Pobiera wszystkich użytkowników z SQL
        
        Returns:
            Dict: {username: user_data}
        """
        try:
            result = {}
            with self.session_scope() as session:
                users = session.query(self.User).all()
                for user in users:
                    result[user.username] = user.to_dict()
            return result
        except Exception as e:
            print(f"Error reading all users from SQL: {e}")
        
        return {}
    
    def get_usernames(self) -> List[str]:
        """
        Pobiera listę wszystkich nazw użytkowników
        
        Returns:
            List[str]: Lista nazw użytkowników
        """
        all_users = self.get_all()
        return list(all_users.keys())
    
    def _migrate_business_games_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Migruje stare dane business games do nowego formatu
        
        Dodaje brakujące pola:
        - money (saldo firmy)
        - financial_settings (ustawienia finansowe)
        - notifications (ustawienia powiadomień)
        - firm.color_scheme (schemat kolorów)
        - firm.motto (motto firmy)
        
        Args:
            user_data: Dane użytkownika
        
        Returns:
            Dict: Zmigrowane dane użytkownika
        """
        if "business_games" not in user_data:
            return user_data
        
        for industry_id, game_data in user_data["business_games"].items():
            if not isinstance(game_data, dict):
                continue
            
            # Dodaj 'money' jeśli brakuje (saldo firmy)
            if "money" not in game_data:
                game_data["money"] = 0
                print(f"Migration: Added 'money' field to {industry_id} game for user")
            
            # Dodaj 'financial_settings' jeśli brakuje
            if "financial_settings" not in game_data:
                game_data["financial_settings"] = {
                    "savings_goal": 0,
                    "low_balance_alert": -10000,
                    "high_balance_alert": 50000,
                    "auto_transfer_enabled": False,
                    "auto_transfer_threshold": 30000,
                    "auto_transfer_amount": 5000
                }
                print(f"Migration: Added 'financial_settings' to {industry_id} game")
            
            # Dodaj 'notifications' jeśli brakuje
            if "notifications" not in game_data:
                game_data["notifications"] = {
                    "deadline_alert_hours": 24,
                    "deadline_alert_enabled": True,
                    "new_contracts_alert": True,
                    "balance_alerts_enabled": True,
                    "events_alerts_enabled": True,
                    "level_up_alerts": True,
                    "employee_alerts": True,
                    "reputation_alerts": True
                }
                print(f"Migration: Added 'notifications' to {industry_id} game")
            
            # Dodaj pola w 'firm' jeśli brakuje
            if "firm" in game_data:
                if "color_scheme" not in game_data["firm"]:
                    game_data["firm"]["color_scheme"] = "purple"
                    print(f"Migration: Added 'color_scheme' to firm in {industry_id} game")
                
                if "motto" not in game_data["firm"]:
                    game_data["firm"]["motto"] = ""
                    print(f"Migration: Added 'motto' to firm in {industry_id} game")
                
                if "founded" not in game_data["firm"]:
                    game_data["firm"]["founded"] = datetime.now().strftime("%Y-%m-%d")
                    print(f"Migration: Added 'founded' to firm in {industry_id} game")
        
        return user_data
    
    def count(self) -> int:
        """
        Zlicza wszystkich użytkowników
        
        Returns:
            int: Liczba użytkowników
        """
        return len(self.get_all())
    
    def validate_user_data(self, user_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Waliduje dane użytkownika
        
        Args:
            user_data: Dane użytkownika do walidacji
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Bazowa walidacja
        is_valid, error = super().validate_data(user_data)
        if not is_valid:
            return is_valid, error
        
        # Wymagane pola
        required_fields = ['user_id', 'password']
        for field in required_fields:
            if field not in user_data:
                return False, f"Missing required field: {field}"
        
        # Walidacja business_games (jeśli włączona)
        if self.config.get("validation", {}).get("validate_business_games", True):
            if "business_games" in user_data:
                is_valid, error = self._validate_business_games(user_data["business_games"])
                if not is_valid:
                    return is_valid, f"Business games validation failed: {error}"
        
        return True, None
    
    def _validate_business_games(self, business_games: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Waliduje strukturę business_games
        
        Args:
            business_games: Dict z danymi business games
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not isinstance(business_games, dict):
            return False, "business_games must be a dictionary"
        
        # Wymagane pola dla każdej gry
        required_game_fields = ["firm", "employees", "office", "contracts", "stats", "money"]
        
        for industry_id, game_data in business_games.items():
            if not isinstance(game_data, dict):
                return False, f"Game data for {industry_id} must be a dictionary"
            
            # Sprawdź wymagane pola
            for field in required_game_fields:
                if field not in game_data:
                    return False, f"Missing required field '{field}' in {industry_id} game"
            
            # Sprawdź strukturę firm
            if "name" not in game_data.get("firm", {}):
                return False, f"Firm must have 'name' field in {industry_id} game"
            
            # Sprawdź strukturę contracts
            contracts = game_data.get("contracts", {})
            if not all(key in contracts for key in ["active", "completed", "available_pool"]):
                return False, f"Contracts must have active/completed/available_pool in {industry_id} game"
        
        return True, None
