"""
System fallback dla funkcji AI gdy limity API są przekroczone
"""
import streamlit as st
from typing import Optional, Dict, Any
import json
import random

class AIFallbackSystem:
    def __init__(self):
        self.fallback_responses = self.load_fallback_responses()
    
    def load_fallback_responses(self) -> Dict:
        """Wczytaj przygotowane odpowiedzi fallback"""
        return {
            "quiz_generation": [
                "⚠️ Funkcja generowania quizów jest tymczasowo niedostępna. Skorzystaj z przygotowanych quizów w lekcjach.",
                "🔄 Tryb offline: Quiz AI niedostępny. Przejdź do sekcji 'Praktyka' dla dostępnych ćwiczeń."
            ],
            "content_analysis": [
                "📚 Analiza AI niedostępna. Przeczytaj materiał i skorzystaj z przygotowanych pytań refleksyjnych.",
                "🧠 Tryb samodzielnej nauki: Przeanalizuj treść używając technik z lekcji o krytycznym myśleniu."
            ],
            "personalized_feedback": [
                "💡 Spersonalizowane feedback tymczasowo niedostępne. Skorzystaj z ogólnych wskazówek w sekcji pomocy.",
                "🎯 Oceń swój postęp używając kryteriów samooceny dostępnych w profilu."
            ],
            "investment_analysis": [
                "📊 Analiza inwestycji AI niedostępna. Użyj checklisty analizy fundamentalnej z materiałów lekcji.",
                "🔍 Skorzystaj z narzędzi do samodzielnej analizy dostępnych w sekcji 'Narzędzia'."
            ]
        }
    
    def get_fallback_message(self, feature_type: str) -> str:
        """Pobierz losową wiadomość fallback dla danego typu funkcji"""
        if feature_type in self.fallback_responses:
            return random.choice(self.fallback_responses[feature_type])
        return "⚠️ Ta funkcja jest tymczasowo niedostępna. Spróbuj ponownie później."
    
    def show_limit_reached_page(self):
        """Pokaż stronę informującą o osiągnięciu limitów"""
        st.error("🚫 **Osiągnięto limit premium requestów**")
        
        st.markdown("""
        ### Co to oznacza?
        
        Twoja aplikacja osiągnęła miesięczny limit requestów do AI. To normalne zabezpieczenie kosztów.
        
        ### Co możesz robić dalej?
        
        #### 🔄 **Opcje natychmiastowe:**
        - ✅ Korzystaj ze wszystkich lekcji i materiałów
        - ✅ Rozwiązuj przygotowane quizy i ćwiczenia  
        - ✅ Śledź swój postęp i XP
        - ✅ Przeglądaj inspiracje dnia
        - ✅ Używaj kalkulatorów inwestycyjnych
        
        #### 📅 **Reset limitu:**
        - Limit resetuje się automatycznie **1. dnia każdego miesiąca**
        - Możesz kontynuować naukę używając dostępnych materiałów
        
        #### 💎 **Upgrade do Premium:**
        - Wyższe limity API
        - Dodatkowe funkcje AI
        - Priorytetowe wsparcie
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📚 Kontynuuj naukę", type="primary"):
                st.session_state.fallback_mode = True
                st.rerun()
        
        with col2:
            if st.button("📊 Zobacz statystyki"):
                from utils.api_limits import show_api_dashboard
                show_api_dashboard()
        
        with col3:
            if st.button("💎 Informacje o Premium"):
                st.session_state.show_premium_info = True
                st.rerun()

# Dekoratory do ochrony funkcji AI
def require_api_limit(estimated_tokens: int = 1000, fallback_type: str = "general"):
    """Dekorator sprawdzający limity API przed wywołaniem funkcji"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            from utils.api_limits import check_api_limit
            
            if check_api_limit(estimated_tokens):
                # Limit OK - wykonaj normalnie
                result = func(*args, **kwargs)
                
                # Zapisz wykorzystanie
                from utils.api_limits import record_api_usage
                record_api_usage(estimated_tokens)
                
                return result
            else:
                # Limit przekroczony - pokaż fallback
                fallback_system = AIFallbackSystem()
                st.warning(fallback_system.get_fallback_message(fallback_type))
                return None
        
        return wrapper
    return decorator

def show_premium_upgrade_info():
    """Pokaż informacje o upgrade do Premium"""
    st.markdown("""
    ## 💎 ZenDegenAcademy Premium
    
    ### Korzyści Premium:
    
    #### 🚀 **Wyższe limity API**
    - 10x więcej requestów miesięcznie
    - Dostęp do zaawansowanych funkcji AI
    - Brak ograniczeń w godzinach szczytu
    
    #### 🧠 **Ekskluzywne funkcje AI**
    - Spersonalizowany coach inwestycyjny
    - Analiza portfolio w czasie rzeczywistym
    - Predykcje trendów rynkowych
    - Generowanie custom strategii
    
    #### 📈 **Zaawansowane narzędzia**
    - Backtesting strategii
    - Risk management calculator
    - Portfolio optimizer
    - Market sentiment analysis
    
    #### 👑 **Premium support**
    - Priorytetowe wsparcie techniczne
    - Dostęp do webinarów premium
    - Bezpośredni kontakt z ekspertami
    - Early access do nowych funkcji
    
    ### Cennik:
    - **Miesięczny**: 99 PLN/miesiąc
    - **Roczny**: 999 PLN/rok (2 miesiące gratis!)
    - **Lifetime**: 2999 PLN (jednorazowo)
    
    ---
    
    #### 🎁 **Specjalna oferta dla obecnych użytkowników:**
    **50% zniżki przez pierwsze 3 miesiące!**
    
    Kod: `EARLY2025`
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🛒 Upgrade do Premium", type="primary"):
            st.info("🚧 Panel zakupów w przygotowaniu. Skontaktuj się z obsługą.")
    
    with col2:
        if st.button("📧 Kontakt ws. Premium"):
            st.info("📧 Email: premium@zendegenacademy.com")

# Globalna instancja systemu fallback
fallback_system = AIFallbackSystem()
