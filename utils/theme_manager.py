"""
Theme Manager - Centralny zarządca motywów/layoutów dla aplikacji BVA
Odpowiada za ładowanie CSS i aplikowanie stylów.

Data: 2025-10-31
Autor: Refaktoryzacja systemu layoutów
"""

import streamlit as st
import os
from functools import lru_cache
from typing import Dict, Optional


class ThemeManager:
    """Zarządca motywów i layoutów aplikacji"""
    
    # Ścieżki
    THEMES_DIR = os.path.join("static", "css", "themes")
    STATIC_CSS_DIR = os.path.join("static", "css")
    DEFAULT_THEME = "standard"
    
    # Dostępne motywy
    AVAILABLE_THEMES = {
        'standard': {
            'name': 'Standard',
            'css_file': 'standard.css',
            'description': 'Klasyczny Material Design - jasny, czysty, profesjonalny',
            'icon': '📱',
            'colors': ['#2196F3', '#FFFFFF', '#F5F5F5']
        },
        'gaming-pro': {
            'name': 'Gaming Pro',
            'css_file': 'gaming-pro.css',
            'description': 'Fioletowo-cyjanowa kolorystyka z neonowymi efektami',
            'icon': '🎮',
            'colors': ['#8B5CF6', '#3B82F6', '#10B981']
        },
        'halloween': {
            'name': 'Halloween',
            'css_file': 'halloween.css',
            'description': 'Halloweenowy klimat z dynią i magiczną purpurą',
            'icon': '🎃',
            'colors': ['#FF6B35', '#9D4EDD', '#00FF00']
        },
        'executive-pro': {
            'name': 'Executive Pro',
            'css_file': 'executive-pro.css',
            'description': 'Navy & Gold dla kadry zarządzającej - elegancja i prestiż',
            'icon': '💼',
            'colors': ['#1E3A8A', '#F59E0B', '#E5E7EB']
        }
    }
    
    @staticmethod
    @lru_cache(maxsize=20)
    def load_css_file(file_path: str) -> str:
        """
        Ładuje plik CSS z cache'owaniem dla lepszej wydajności
        
        Args:
            file_path: Ścieżka do pliku CSS
            
        Returns:
            str: Zawartość pliku CSS lub pusty string w przypadku błędu
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            st.error(f"⚠️ Plik CSS nie znaleziony: {file_path}")
            return ""
        except Exception as e:
            st.error(f"⚠️ Błąd ładowania CSS: {e}")
            return ""
    
    @staticmethod
    def get_user_theme() -> str:
        """
        Pobiera aktywny motyw użytkownika z danych użytkownika
        
        Returns:
            str: Klucz motywu (np. 'standard', 'gaming-pro')
        """
        # Jeśli użytkownik nie jest zalogowany, zwróć domyślny motyw
        if not st.session_state.get('logged_in', False):
            return ThemeManager.DEFAULT_THEME
        
        try:
            from data.users import load_user_data
            users_data = load_user_data()
            username = st.session_state.get('username')
            user_data = users_data.get(username, {})
            theme = user_data.get('layout_preference', ThemeManager.DEFAULT_THEME)
            
            # Walidacja czy motyw istnieje w dostępnych motywach
            if theme not in ThemeManager.AVAILABLE_THEMES:
                st.warning(f"⚠️ Nieznany motyw '{theme}', używam domyślnego")
                return ThemeManager.DEFAULT_THEME
            
            return theme
        except Exception as e:
            # W przypadku błędu zwróć domyślny motyw
            # Nie wyświetlaj błędu - może to być normalna sytuacja przy pierwszym logowaniu
            return ThemeManager.DEFAULT_THEME
    
    @staticmethod
    def apply_theme(theme_key: Optional[str] = None):
        """
        Aplikuje wybrany motyw CSS
        
        Args:
            theme_key: Klucz motywu (np. 'standard'). Jeśli None, pobiera z danych użytkownika
        """
        # Jeśli nie podano motywu, pobierz z preferencji użytkownika
        if theme_key is None:
            theme_key = ThemeManager.get_user_theme()
        
        # Pobierz konfigurację motywu
        theme_config = ThemeManager.AVAILABLE_THEMES.get(theme_key)
        if not theme_config:
            st.warning(f"⚠️ Nieznany motyw '{theme_key}', używam domyślnego")
            theme_key = ThemeManager.DEFAULT_THEME
            theme_config = ThemeManager.AVAILABLE_THEMES[theme_key]
        
        # Ścieżka do pliku CSS motywu
        css_file = theme_config['css_file']
        css_path = os.path.join(ThemeManager.THEMES_DIR, css_file)
        
        # Sprawdź czy plik istnieje
        if not os.path.exists(css_path):
            st.error(f"⚠️ Plik motywu nie istnieje: {css_path}")
            return
        
        # Załaduj i aplikuj CSS
        css = ThemeManager.load_css_file(css_path)
        if css:  # Tylko jeśli udało się załadować
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    @staticmethod
    def apply_base_styles():
        """
        Aplikuje bazowe style (Material 3, mobile navigation)
        Te style są wspólne dla wszystkich motywów
        """
        # Material 3 Extended (zawiera importy z core/)
        material3_path = os.path.join(ThemeManager.STATIC_CSS_DIR, "material3_extended.css")
        if os.path.exists(material3_path):
            css = ThemeManager.load_css_file(material3_path)
            if css:
                st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        
        # Mobile Navigation
        mobile_nav_path = os.path.join(ThemeManager.STATIC_CSS_DIR, "mobile-navigation.css")
        if os.path.exists(mobile_nav_path):
            css = ThemeManager.load_css_file(mobile_nav_path)
            if css:
                st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    @staticmethod
    def apply_all():
        """
        Aplikuje wszystkie style: base styles + wybrany motyw użytkownika
        To jest główna funkcja która powinna być wywołana w main.py
        """
        ThemeManager.apply_base_styles()
        ThemeManager.apply_theme()
        
        # Mobile sidebar fix - wymuszenie działania przycisku
        mobile_sidebar_fix = """
        <style>
        /* Zwiększona szerokość sidebar */
        [data-testid="stSidebar"] {
            min-width: 280px !important;
            width: 280px !important;
        }
        
        /* Szersze przyciski w sidebar */
        [data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            white-space: normal !important;
            word-wrap: break-word !important;
            min-height: 3rem !important;
            padding: 0.5rem 1rem !important;
        }
        
        /* Ensure sidebar toggle works on mobile */
        @media (max-width: 768px) {
            /* Make sidebar toggle button always visible and clickable */
            [data-testid="collapsedControl"] {
                display: flex !important;
                pointer-events: auto !important;
                cursor: pointer !important;
                z-index: 9999 !important;
                position: fixed !important;
                top: 1rem !important;
                left: 1rem !important;
            }
            
            /* Ensure sidebar can be opened */
            [data-testid="stSidebar"] {
                transition: transform 0.3s ease-in-out !important;
            }
            
            /* When sidebar is expanded */
            [data-testid="stSidebar"][aria-expanded="true"] {
                transform: translateX(0) !important;
                display: block !important;
            }
            
            /* When sidebar is collapsed */
            [data-testid="stSidebar"][aria-expanded="false"] {
                transform: translateX(-100%) !important;
            }
        }
        </style>
        """
        st.markdown(mobile_sidebar_fix, unsafe_allow_html=True)
    
    @staticmethod
    def get_theme_info(theme_key: str) -> Optional[Dict]:
        """
        Zwraca informacje o motywie
        
        Args:
            theme_key: Klucz motywu
            
        Returns:
            Dict z informacjami o motywie lub None jeśli nie istnieje
        """
        return ThemeManager.AVAILABLE_THEMES.get(theme_key)
    
    @staticmethod
    def list_available_themes() -> Dict[str, Dict]:
        """
        Zwraca słownik wszystkich dostępnych motywów
        
        Returns:
            Dict z dostępnymi motywami
        """
        return ThemeManager.AVAILABLE_THEMES.copy()
    
    @staticmethod
    def clear_cache():
        """
        Czyści cache załadowanych plików CSS
        Przydatne podczas developmentu gdy modyfikujesz pliki CSS
        """
        ThemeManager.load_css_file.cache_clear()


# Legacy compatibility - dla backwards compatibility z starym kodem
def get_user_layout() -> str:
    """
    DEPRECATED: Użyj ThemeManager.get_user_theme() zamiast tego
    
    Legacy function dla kompatybilności wstecznej
    """
    return ThemeManager.get_user_theme()


def load_css(css_file: str) -> str:
    """
    DEPRECATED: Użyj ThemeManager.load_css_file() zamiast tego
    
    Legacy function dla kompatybilności wstecznej
    """
    return ThemeManager.load_css_file(css_file)
