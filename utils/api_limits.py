"""
System monitorowania i zarządzania limitami API
"""
import json
import datetime
from typing import Dict, Optional, Tuple
import streamlit as st

class APILimitManager:
    def __init__(self, config_file: str = "config/api_limits.json"):
        self.config_file = config_file
        self.limits = self.load_limits()
    
    def load_limits(self) -> Dict:
        """Wczytaj konfigurację limitów z pliku"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Domyślna konfiguracja
            default_config = {
                "monthly_limit": 1000000,  # 1M tokenów miesięcznie
                "daily_limit": 50000,      # 50k tokenów dziennie
                "current_usage": {
                    "monthly": 0,
                    "daily": 0,
                    "last_reset_monthly": datetime.datetime.now().strftime("%Y-%m"),
                    "last_reset_daily": datetime.datetime.now().strftime("%Y-%m-%d")
                },
                "fallback_enabled": True,
                "warning_thresholds": {
                    "daily": 0.8,    # 80%
                    "monthly": 0.9   # 90%
                }
            }
            self.save_limits(default_config)
            return default_config
    
    def save_limits(self, limits: Dict):
        """Zapisz konfigurację limitów do pliku"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(limits, f, indent=2, ensure_ascii=False)
            self.limits = limits
        except Exception as e:
            st.error(f"Błąd zapisu limitów: {e}")
    
    def check_and_reset_limits(self):
        """Sprawdź i zresetuj limity jeśli potrzeba"""
        now = datetime.datetime.now()
        current_month = now.strftime("%Y-%m")
        current_day = now.strftime("%Y-%m-%d")
        
        # Reset miesięczny
        if self.limits["current_usage"]["last_reset_monthly"] != current_month:
            self.limits["current_usage"]["monthly"] = 0
            self.limits["current_usage"]["last_reset_monthly"] = current_month
        
        # Reset dzienny
        if self.limits["current_usage"]["last_reset_daily"] != current_day:
            self.limits["current_usage"]["daily"] = 0
            self.limits["current_usage"]["last_reset_daily"] = current_day
        
        self.save_limits(self.limits)
    
    def can_make_request(self, estimated_tokens: int = 1000) -> Tuple[bool, str]:
        """Sprawdź czy można wykonać żądanie API"""
        self.check_and_reset_limits()
        
        daily_after = self.limits["current_usage"]["daily"] + estimated_tokens
        monthly_after = self.limits["current_usage"]["monthly"] + estimated_tokens
        
        # Sprawdź limity
        if daily_after > self.limits["daily_limit"]:
            return False, "Osiągnięto dzienny limit API"
        
        if monthly_after > self.limits["monthly_limit"]:
            return False, "Osiągnięto miesięczny limit API"
        
        return True, "OK"
    
    def record_usage(self, tokens_used: int):
        """Zapisz wykorzystanie tokenów"""
        self.check_and_reset_limits()
        self.limits["current_usage"]["daily"] += tokens_used
        self.limits["current_usage"]["monthly"] += tokens_used
        self.save_limits(self.limits)
    
    def get_usage_stats(self) -> Dict:
        """Pobierz statystyki wykorzystania"""
        self.check_and_reset_limits()
        
        daily_usage = self.limits["current_usage"]["daily"]
        monthly_usage = self.limits["current_usage"]["monthly"]
        
        return {
            "daily": {
                "used": daily_usage,
                "limit": self.limits["daily_limit"],
                "percentage": (daily_usage / self.limits["daily_limit"]) * 100,
                "remaining": self.limits["daily_limit"] - daily_usage
            },
            "monthly": {
                "used": monthly_usage,
                "limit": self.limits["monthly_limit"],
                "percentage": (monthly_usage / self.limits["monthly_limit"]) * 100,
                "remaining": self.limits["monthly_limit"] - monthly_usage
            }
        }
    
    def show_usage_warning(self):
        """Pokaż ostrzeżenie o wykorzystaniu"""
        stats = self.get_usage_stats()
        
        # Ostrzeżenie dzienne
        if stats["daily"]["percentage"] >= self.limits["warning_thresholds"]["daily"] * 100:
            st.warning(f"⚠️ Wykorzystano {stats['daily']['percentage']:.1f}% dziennego limitu API")
        
        # Ostrzeżenie miesięczne
        if stats["monthly"]["percentage"] >= self.limits["warning_thresholds"]["monthly"] * 100:
            st.warning(f"⚠️ Wykorzystano {stats['monthly']['percentage']:.1f}% miesięcznego limitu API")

# Globalna instancja managera
api_limit_manager = APILimitManager()

def check_api_limit(estimated_tokens: int = 1000) -> bool:
    """Szybka funkcja sprawdzania limitu"""
    can_proceed, message = api_limit_manager.can_make_request(estimated_tokens)
    if not can_proceed:
        st.error(f"🚫 {message}")
        return False
    return True

def record_api_usage(tokens_used: int):
    """Szybka funkcja zapisywania użycia"""
    api_limit_manager.record_usage(tokens_used)

def show_api_dashboard():
    """Dashboard limitów API dla administratorów"""
    st.subheader("📊 Dashboard limitów API")
    
    stats = api_limit_manager.get_usage_stats()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Dzienny limit",
            f"{stats['daily']['used']:,} / {stats['daily']['limit']:,}",
            f"{stats['daily']['remaining']:,} pozostało"
        )
        st.progress(stats['daily']['percentage'] / 100)
    
    with col2:
        st.metric(
            "Miesięczny limit", 
            f"{stats['monthly']['used']:,} / {stats['monthly']['limit']:,}",
            f"{stats['monthly']['remaining']:,} pozostało"
        )
        st.progress(stats['monthly']['percentage'] / 100)
    
    # Ustawienia limitów (tylko dla adminów)
    if st.session_state.get('is_admin', False):
        with st.expander("⚙️ Ustawienia limitów"):
            new_daily = st.number_input("Dzienny limit", value=api_limit_manager.limits["daily_limit"])
            new_monthly = st.number_input("Miesięczny limit", value=api_limit_manager.limits["monthly_limit"])
            
            if st.button("Zapisz nowe limity"):
                api_limit_manager.limits["daily_limit"] = new_daily
                api_limit_manager.limits["monthly_limit"] = new_monthly
                api_limit_manager.save_limits(api_limit_manager.limits)
                st.success("✅ Limity zostały zaktualizowane")
                st.rerun()
