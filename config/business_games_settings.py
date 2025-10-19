"""
Business Games - Konfiguracja systemu oceny kontraktów
Obsługuje 3 tryby: Heurystyka, AI, Mistrz Gry
"""

# =============================================================================
# TRYBY OCENY
# =============================================================================

EVALUATION_MODES = {
    "heuristic": {
        "name": "⚡ Heurystyka",
        "description": "Prosta automatyczna ocena oparta na długości tekstu",
        "subtitle": "(Szybka, darmowa, dobra dla MVP)",
        "enabled": True,
        "requires": [],
        "instant": True,
        "cost_per_eval": 0,
        "quality": "Podstawowa"
    },
    "ai": {
        "name": "🤖 Ocena AI",
        "description": "Szczegółowa ocena przez model Google Gemini",
        "subtitle": "(Wolniejsza, płatna, wysoka jakość)",
        "enabled": False,
        "requires": ["GOOGLE_API_KEY"],
        "instant": False,
        "cost_per_eval": 0.02,  # średnio $0.01-0.03
        "quality": "Wysoka"
    },
    "game_master": {
        "name": "👨‍💼 Mistrz Gry",
        "description": "Ręczna ocena przez Admina",
        "subtitle": "(Najlepsza jakość, wymaga czasu Admina)",
        "enabled": False,
        "requires": ["admin_availability"],
        "instant": False,
        "cost_per_eval": 0,
        "quality": "Najwyższa"
    }
}

# Domyślny tryb oceny
DEFAULT_EVALUATION_MODE = "ai"  # Zmieniono z "heuristic" na "ai" dla oceny Google Gemini

# =============================================================================
# KONFIGURACJA OCENY AI (Google Gemini)
# =============================================================================

AI_EVALUATION_CONFIG = {
    # Model Google Gemini (zmieniono na gemini-2.5-flash - stabilny, szybki, dostępny)
    "model": "gemini-2.5-flash",  # Stabilna wersja Gemini 2.5 Flash
    "temperature": 0.3,           # Niska temperatura = bardziej konsystentne oceny
    "max_tokens": 800,            # Limit dla odpowiedzi
    
    # System instruction dla Gemini
    "system_instruction": """Jesteś ekspertem od Conversational Intelligence i Business Coaching, 
oceniającym rozwiązania kontraktów konsultingowych. Jesteś obiektywny, konstruktywny i pomocny.
Zwracasz odpowiedzi TYLKO w formacie JSON.""",
    
    # Prompt template
    "prompt_template": """Oceń poniższe rozwiązanie kontraktu konsultingowego.

KONTRAKT DO OCENY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tytuł: {contract_title}
Kategoria: {contract_category}
Poziom trudności: {contract_difficulty}/5 ⭐
Opis: {contract_description}
Minimalne słowa: {min_words}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ROZWIĄZANIE UCZESTNIKA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{user_solution}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KRYTERIA OCENY (0-100 punktów):

1. **Merytoryczna wartość treści** (0-25 pkt)
   - Czy rozwiązanie odnosi się do teorii CIQ?
   - Czy zawiera konkretne techniki konwersacyjne?
   - Czy pokazuje zrozumienie problemu?

2. **Kompletność odpowiedzi** (0-25 pkt)
   - Czy odpowiada na wszystkie aspekty kontraktu?
   - Czy pokrywa wymagane minimum słów?
   - Czy zawiera konkretne przykłady?

3. **Struktura i organizacja** (0-20 pkt)
   - Czy tekst jest logicznie zorganizowany?
   - Czy jest czytelny i zrozumiały?
   - Czy używa odpowiedniego formatowania?

4. **Praktyczne zastosowanie** (0-20 pkt)
   - Czy rozwiązanie jest wykonalne?
   - Czy zawiera konkretne kroki działania?
   - Czy jest przydatne dla klienta?

5. **Innowacyjność** (0-10 pkt)
   - Czy zawiera oryginalne pomysły?
   - Czy wykracza poza standardowe rozwiązania?

INSTRUKCJE:
- Oceń rozwiązanie według powyższych kryteriów
- Suma punktów: 0-100
- Przelicz na gwiazdki: 0-20=1⭐, 21-40=2⭐, 41-60=3⭐, 61-80=4⭐, 81-100=5⭐
- Podaj krótki (2-3 zdania) feedback dla uczestnika
- Wymień 2-3 mocne strony
- Wymień 2-3 sugestie do poprawy

Zwróć odpowiedź TYLKO w formacie JSON (bez markdown, bez ```json):
{{
  "total_score": <0-100>,
  "rating": <1-5>,
  "feedback": "krótki komentarz ogólny",
  "strengths": ["mocna strona 1", "mocna strona 2"],
  "improvements": ["sugestia 1", "sugestia 2"]
}}
""",
    
    # Mapowanie punktów na gwiazdki
    "score_to_rating": {
        (0, 20): 1,
        (21, 40): 2,
        (41, 60): 3,
        (61, 80): 4,
        (81, 100): 5
    },
    
    # Timeout dla API (sekundy)
    "timeout": 30,
    
    # Retry policy
    "max_retries": 2,
    "retry_delay": 2,  # sekundy między próbami
    
    # Generation config dla Gemini
    "generation_config": {
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 2048,  # Zwiększono z 800 na 2048 - JSON był ucinany
    }
}

# =============================================================================
# KONFIGURACJA MISTRZA GRY
# =============================================================================

GAME_MASTER_CONFIG = {
    # Kolejka rozwiązań
    "queue_enabled": True,
    "queue_file": "game_master_queue.json",
    "max_pending_reviews": 100,
    
    # SLA (Service Level Agreement)
    "review_deadline_hours": 48,  # Zalecany czas na ocenę
    "urgent_threshold_hours": 24,  # Po tym czasie = pilne
    
    # Powiadomienia
    "notification_email": False,  # TODO: Implementacja email
    "notification_in_app": True,  # Powiadomienie w aplikacji
    
    # Interfejs oceny
    "show_contract_details": True,
    "show_word_count": True,
    "show_waiting_time": True,
    "allow_skip": True,  # Możliwość pominięcia na później
    
    # Statystyki
    "track_evaluator_stats": True,  # Statystyki Mistrzów Gry
    "show_avg_review_time": True
}

# =============================================================================
# KONFIGURACJA HEURYSTYKI (obecny system)
# =============================================================================

HEURISTIC_CONFIG = {
    # Próg słów dla różnych ocen
    "word_thresholds": {
        "min_multiplier": 0.5,   # 50% min_words = 1 gwiazdka
        "low_multiplier": 0.8,   # 80% min_words = 2 gwiazdki
        "med_multiplier": 1.0,   # 100% min_words = 3 gwiazdki
        "high_multiplier": 1.5,  # 150% min_words = 4 gwiazdki
        # >150% min_words = 5 gwiazdek
    },
    
    # Losowość (±1 gwiazdka)
    "randomness_enabled": True,
    "randomness_range": (-1, 1),
    
    # Feedback automatyczny
    "auto_feedback": True,
    "feedback_template": "Rozwiązanie zawiera {word_count} słów. Automatyczna ocena: {rating}/5 ⭐"
}

# =============================================================================
# PERSISTENCE
# =============================================================================

SETTINGS_FILE = "config/business_games_active_mode.json"

# =============================================================================
# FUNKCJE POMOCNICZE
# =============================================================================

def get_evaluation_mode_info(mode: str) -> dict:
    """Zwraca informacje o trybie oceny"""
    return EVALUATION_MODES.get(mode, EVALUATION_MODES["heuristic"])


def is_mode_available(mode: str) -> bool:
    """Sprawdza czy tryb jest dostępny"""
    mode_info = EVALUATION_MODES.get(mode)
    if not mode_info:
        return False
    return mode_info["enabled"]


def get_mode_requirements(mode: str) -> list:
    """Zwraca wymagania dla trybu"""
    mode_info = EVALUATION_MODES.get(mode, {})
    return mode_info.get("requires", [])


def validate_mode_config(mode: str) -> tuple:
    """
    Sprawdza czy tryb jest poprawnie skonfigurowany
    Returns: (is_valid: bool, error_message: str)
    """
    if mode not in EVALUATION_MODES:
        return False, f"Nieznany tryb oceny: {mode}"
    
    mode_info = EVALUATION_MODES[mode]
    
    if not mode_info["enabled"]:
        return False, f"Tryb {mode_info['name']} jest wyłączony"
    
    # Sprawdź wymagania
    requirements = mode_info["requires"]
    
    if "GOOGLE_API_KEY" in requirements:
        # TODO: Sprawdź czy klucz API jest ustawiony
        pass
    
    if "admin_availability" in requirements:
        # TODO: Sprawdź czy admin jest dostępny
        pass
    
    return True, ""


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [
    'EVALUATION_MODES',
    'DEFAULT_EVALUATION_MODE',
    'AI_EVALUATION_CONFIG',
    'GAME_MASTER_CONFIG',
    'HEURISTIC_CONFIG',
    'SETTINGS_FILE',
    'get_evaluation_mode_info',
    'is_mode_available',
    'get_mode_requirements',
    'validate_mode_config'
]
