"""
Business Games - Konfiguracja systemu oceny kontraktów
Obsługuje 3 tryby: Heurystyka, AI, Mistrz Gry
"""

# =============================================================================
# TRYBY OCENY
# =============================================================================

EVALUATION_MODES = {
    "ai": {
        "name": "🤖 Ocena AI",
        "description": "Szczegółowa ocena przez model Google Gemini",
        "subtitle": "(Automatyczna, płatna, wysoka jakość)",
        "enabled": True,  # Zmieniono na True - AI jest teraz domyślne
        "requires": ["GOOGLE_API_KEY"],
        "instant": True,  # Zmieniono na True - jest wystarczająco szybkie (2-5s)
        "cost_per_eval": 0.02,  # średnio $0.01-0.03
        "quality": "Wysoka"
    },
    "game_master": {
        "name": "👨‍💼 Mistrz Gry",
        "description": "Ręczna ocena przez Admina (fallback gdy AI nie działa)",
        "subtitle": "(Najwyższa jakość, wymaga czasu Admina)",
        "enabled": True,  # Zmieniono na True - używane jako fallback
        "requires": ["admin_availability"],
        "instant": False,
        "cost_per_eval": 0,
        "quality": "Najwyższa"
    }
}

# Domyślny tryb oceny
DEFAULT_EVALUATION_MODE = "ai"  # AI z fallbackiem do Game Master (usunięto heurystykę)

# =============================================================================
# KONFIGURACJA OCENY AI (Google Gemini)
# =============================================================================

AI_EVALUATION_CONFIG = {
    # Model Google Gemini (zmieniono na gemini-2.5-flash - stabilny, szybki, dostępny)
    "model": "gemini-2.5-flash",  # Stabilna wersja Gemini 2.5 Flash
    "temperature": 0.3,           # Niska temperatura = bardziej konsystentne oceny
    "max_tokens": 2000,           # Limit dla odpowiedzi (zwiększono z 800 do 2000)
    
    # System instruction dla Gemini
    "system_instruction": """Jesteś klientem biznesowym, który zlecił wykonanie projektu konsultingowego.
Oceniasz pracę zleceniobiorcy z perspektywy biznesowej - czy rozwiązanie spełnia Twoje oczekiwania,
czy jest praktyczne i czy możesz je wdrożyć w swojej firmie. Jesteś wymagający ale sprawiedliwy.
Zwracasz odpowiedzi TYLKO w formacie JSON.""",
    
    # Prompt template
    "prompt_template": """Jesteś klientem, który zlecił wykonanie projektu. Oceń otrzymaną pracę.

TWOJE ZLECENIE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tytuł kontraktu: {contract_title}
Kategoria: {contract_category}
Poziom skomplikowania: {contract_difficulty}/5 ⭐
Szczegóły zlecenia: {contract_description}
Oczekiwana objętość: min. {min_words} słów
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ROZWIĄZANIE OD ZLECENIOBIORCY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{user_solution}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OCEŃ PRACĘ JAK KLIENT BIZNESOWY (0-100 punktów):

1. **Zrozumienie naszych potrzeb** (0-25 pkt)
   - Czy zleceniobiorca zrozumiał, czego potrzebujemy?
   - Czy rozwiązanie pasuje do naszej sytuacji?
   - Czy uwzględniono kontekst naszego biznesu?

2. **Kompletność realizacji zlecenia** (0-25 pkt)
   - Czy wszystkie punkty zlecenia zostały wykonane?
   - Czy objętość pracy jest zgodna z umową?
   - Czy dostaliśmy konkretne rozwiązania, nie tylko teorię?

3. **Jakość i przejrzystość** (0-20 pkt)
   - Czy praca jest profesjonalnie przygotowana?
   - Czy wszystko jest jasno i zrozumiale opisane?
   - Czy łatwo nam znaleźć kluczowe informacje?

4. **Możliwość wdrożenia** (0-20 pkt)
   - Czy możemy to wdrożyć w naszej firmie?
   - Czy są konkretne kroki działania?
   - Czy rozwiązanie jest realistyczne (czas, budżet, zasoby)?

5. **Wartość dodana** (0-10 pkt)
   - Czy dostaliśmy coś więcej niż podstawy?
   - Czy są ciekawe/innowacyjne pomysły?
   - Czy praca wyróżnia się jakością?

NAPISZ FEEDBACK JAK KLIENT DO ZLECENIOBIORCY:
- Suma punktów: 0-100
- Przelicz na gwiazdki: 0-20=1⭐, 21-40=2⭐, 41-60=3⭐, 61-80=4⭐, 81-100=5⭐
- Feedback ogólny: 2-3 zdania JAK KLIENT ("Dziękujemy za...", "Jesteśmy zadowoleni/niezadowoleni...", "Praca spełnia/nie spełnia...")
- Co nam się podobało: 2-3 konkretne punkty z perspektywy klienta
- Co mogłoby być lepsze: 2-3 konstruktywne uwagi dotyczące tego, czego nam brakowało lub co wymaga dopracowania

Pisz w 1. osobie liczby mnogiej ("nam się podoba", "oczekiwaliśmy", "chcielibyśmy").
Zwróć odpowiedź TYLKO w formacie JSON (bez markdown, bez ```json):
{{
  "total_score": <0-100>,
  "rating": <1-5>,
  "feedback": "Twój komentarz ogólny jako klient (2-3 zdania)",
  "strengths": ["co nam się podobało 1", "co nam się podobało 2"],
  "improvements": ["czego nam brakowało/co poprawić 1", "czego nam brakowało/co poprawić 2"]
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
        "max_output_tokens": 4096,  # Zwiększono z 2048 na 4096 - JSON był nadal ucinany
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
# KONFIGURACJA HEURYSTYKI (USUNIĘTA - zastąpiona przez Game Master fallback)
# =============================================================================

# HEURISTIC_CONFIG = {
#     # USUNIĘTA - heurystyka była zbyt losowa bez feedbacku
#     # Teraz: AI działa → pełny feedback | AI nie działa → kolejka do GM
# }

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
    # 'HEURISTIC_CONFIG',  # USUNIĘTA - heurystyka już nie istnieje
    'SETTINGS_FILE',
    'get_evaluation_mode_info',
    'is_mode_available',
    'get_mode_requirements',
    'validate_mode_config'
]
