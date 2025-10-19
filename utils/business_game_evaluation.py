"""
Business Games - System Oceny Kontraktów
Obsługuje 3 tryby: Heurystyka, AI, Mistrz Gry
"""

import json
import random
from datetime import datetime
from typing import Dict, Tuple, Optional
import os

from config.business_games_settings import (
    EVALUATION_MODES,
    DEFAULT_EVALUATION_MODE,
    AI_EVALUATION_CONFIG,
    GAME_MASTER_CONFIG,
    # HEURISTIC_CONFIG,  # USUNIĘTA - heurystyka już nie istnieje
    SETTINGS_FILE
)

# =============================================================================
# GŁÓWNA FUNKCJA OCENY
# =============================================================================

def evaluate_contract_solution(
    user_data: Dict,
    contract: Dict,
    solution: str,
    evaluation_mode: Optional[str] = None
) -> Tuple[int, str, Dict]:
    """
    Ocenia rozwiązanie kontraktu według wybranego trybu
    
    Args:
        user_data: Dane użytkownika (potrzebne dla kolejki GM)
        contract: Dane kontraktu do oceny
        solution: Tekst rozwiązania przesłany przez użytkownika
        evaluation_mode: "ai" / "game_master" (None = użyj domyślnego)
    
    Returns:
        Tuple[rating, feedback, details]:
        - rating (int): Ocena 1-5 gwiazdek (0 = pending dla GM)
        - feedback (str): Tekstowy feedback dla użytkownika
        - details (dict): Szczegóły oceny (metoda, statystyki itp.)
    
    Example:
        >>> rating, feedback, details = evaluate_contract_solution(
        ...     user_data, contract, solution, "ai"
        ... )
        >>> print(f"Ocena: {rating}/5")
        >>> print(f"Feedback: {feedback}")
    """
    # DEBUG: Loguj do pliku
    from utils.debug_log import log_debug
    log_debug("="*60)
    log_debug("evaluate_contract_solution() wywołane")
    
    # Pobierz aktywny tryb jeśli nie podano
    if evaluation_mode is None:
        evaluation_mode = get_active_evaluation_mode()
        print(f"🔍 DEBUG: get_active_evaluation_mode() zwróciło: '{evaluation_mode}'")
        log_debug(f"get_active_evaluation_mode() zwróciło: '{evaluation_mode}'")
    
    print(f"🔍 DEBUG: Używam trybu oceny: '{evaluation_mode}'")
    log_debug(f"Używam trybu oceny: '{evaluation_mode}'")
    
    # Walidacja trybu
    if evaluation_mode not in EVALUATION_MODES:
        print(f"⚠️ Nieznany tryb oceny: {evaluation_mode}, używam domyślnego AI")
        log_debug(f"⚠️ Nieznany tryb oceny: {evaluation_mode}, używam domyślnego AI")
        evaluation_mode = "ai"
    
    # Wybór metody oceny
    if evaluation_mode == "ai":
        return evaluate_with_ai(solution, contract, user_data)
    
    elif evaluation_mode == "game_master":
        return queue_for_game_master(user_data, contract, solution)
    
    else:
        # Fallback do AI
        return evaluate_with_ai(solution, contract, user_data)


# =============================================================================
# TRYB 1: HEURYSTYKA (USUNIĘTA - zastąpiona przez Game Master fallback)
# =============================================================================

# FUNKCJA USUNIĘTA - heurystyka była zbyt losowa i bez feedbacku
# Teraz: AI działa → pełny feedback | AI nie działa → kolejka do GM
# 
# def evaluate_heuristic(solution: str, contract: Dict) -> Tuple[int, str, Dict]:
#     """Stara heurystyka - USUNIĘTA"""
#     pass


# =============================================================================
# TRYB 2: OCENA AI (Google Gemini)
# =============================================================================

def evaluate_with_ai(solution: str, contract: Dict, user_data: Dict = None) -> Tuple[int, str, Dict]:
    """
    Ocena przez model Google Gemini
    
    Wysyła prompt do Gemini z:
    - Opisem kontraktu
    - Rozwiązaniem uczestnika
    - Kryteriami oceny
    
    AI zwraca:
    - Ocenę 0-100 punktów
    - Rating 1-5 gwiazdek
    - Feedback tekstowy
    - Mocne strony
    - Sugestie do poprawy
    
    Args:
        solution: Tekst rozwiązania
        contract: Dane kontraktu
        user_data: Dane użytkownika (dla fallbacku do GM)
    
    Returns:
        (rating, feedback, details)
    """
    from utils.debug_log import log_debug
    
    log_debug("🤖 evaluate_with_ai() ROZPOCZĘTA")
    print("🤖 DEBUG: evaluate_with_ai() rozpoczęta")
    
    try:
        log_debug("Importuję google.generativeai...")
        import google.generativeai as genai
        log_debug("✅ Import google.generativeai OK")
        
        log_debug("Przygotowuję prompt...")
        # Przygotuj prompt
        prompt = AI_EVALUATION_CONFIG["prompt_template"].format(
            contract_title=contract["tytul"],
            contract_category=contract["kategoria"],
            contract_difficulty=contract.get("trudnosc", 3),  # Poprawiono z "poziom_trudnosci" na "trudnosc"
            contract_description=contract["opis"],
            min_words=contract.get("min_slow", 300),
            user_solution=solution
        )
        log_debug(f"✅ Prompt przygotowany (długość: {len(prompt)} znaków)")
        
        log_debug("Pobieram API key...")
        # Pobierz API key (priorytet: secrets > env > plik)
        api_key = None
        
        # 1. Najpierw sprawdź Streamlit secrets (standardowy sposób w aplikacji)
        try:
            import streamlit as st
            api_key = st.secrets["GOOGLE_API_KEY"]
            log_debug("✅ API key pobrane z st.secrets")
        except Exception as e:
            log_debug(f"❌ Nie udało się pobrać z st.secrets: {e}")
            api_key = None
        
        # 2. Jeśli nie ma w secrets, sprawdź zmienną środowiskową
        if not api_key:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                log_debug("✅ API key pobrane z ENV")
        
        # 3. Jeśli nie ma, sprawdź plik konfiguracyjny (backward compatibility)
        if not api_key:
            api_key = load_gemini_api_key()
            if api_key:
                log_debug("✅ API key pobrane z pliku")
        
        if not api_key:
            log_debug("❌ BRAK API KEY! Rzucam wyjątek...")
            raise Exception("Brak klucza API Google Gemini. Fallback do heurystyki.")
        
        log_debug("Konfiguruję genai.configure()...")
        # Skonfiguruj Gemini
        genai.configure(api_key=api_key)
        log_debug("✅ genai.configure() OK")
        
        log_debug("Ustawiam safety_settings...")
        # Safety settings - wyłącz zbyt restrykcyjne blokady dla treści edukacyjnych
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        log_debug("✅ safety_settings ustawione")
        
        log_debug(f"Tworzę model: {AI_EVALUATION_CONFIG['model']}...")
        # Utwórz model
        model = genai.GenerativeModel(
            model_name=AI_EVALUATION_CONFIG["model"],
            generation_config=AI_EVALUATION_CONFIG["generation_config"],
            system_instruction=AI_EVALUATION_CONFIG["system_instruction"],
            safety_settings=safety_settings
        )
        log_debug("✅ Model utworzony")
        
        log_debug("Wywołuję model.generate_content()...")
        # Wywołaj Gemini API
        response = model.generate_content(prompt)
        log_debug("✅ Otrzymano odpowiedź z Gemini")
        
        # Sprawdź czy odpowiedź jest zablokowana przez safety
        if not response.candidates or not response.candidates[0].content.parts:
            log_debug("⚠️ Odpowiedź zablokowana przez safety settings lub pusta")
            # Sprawdź finish_reason
            if response.candidates:
                finish_reason = response.candidates[0].finish_reason
                log_debug(f"finish_reason: {finish_reason}")
            
            # Odpowiedź zablokowana - spróbuj bez safety settings
            log_debug("Próbuję ponownie BEZ safety settings...")
            print("⚠️ Odpowiedź zablokowana przez safety settings, próbuję ponownie bez nich...")
            model_no_safety = genai.GenerativeModel(
                model_name=AI_EVALUATION_CONFIG["model"],
                generation_config=AI_EVALUATION_CONFIG["generation_config"],
                system_instruction=AI_EVALUATION_CONFIG["system_instruction"]
            )
            response = model_no_safety.generate_content(prompt)
            log_debug("✅ Otrzymano odpowiedź z Gemini (bez safety)")
        
        # Parse odpowiedzi JSON
        result_text = ""
        try:
            result_text = response.text.strip()
            log_debug(f"Długość odpowiedzi: {len(result_text)} znaków")
        except Exception as e:
            log_debug(f"❌ Błąd pobierania response.text: {e}")
            # Prawdopodobnie safety block - przekieruj do GM
            log_debug("Fallback do Game Master (safety block)")
            print("⚠️ Ocena AI zablokowana przez safety. Przekierowuję do Mistrza Gry...")
            if user_data:
                return queue_for_game_master(user_data, contract, solution)
            else:
                return 0, "❌ Błąd: Safety block i brak możliwości kolejki GM", {"method": "error", "error": "safety_block"}
        
        # Usuń markdown formatting jeśli jest
        if result_text.startswith("```json"):
            result_text = result_text.replace("```json", "").replace("```", "").strip()
        elif result_text.startswith("```"):
            result_text = result_text.replace("```", "").strip()
        
        # Spróbuj naprawić ucięty JSON (dodaj brakujące zamknięcia)
        if not result_text.endswith("}"):
            log_debug("⚠️ JSON nie kończy się }, próbuję naprawić...")
            
            # Znajdź ostatni kompletny element
            # Jeśli JSON urywa się w środku stringa, obetnij do ostatniego kompletnego
            last_comma_pos = result_text.rfind('",')
            last_bracket_pos = result_text.rfind(']')
            
            # Usuń ucięte fragmenty
            if last_comma_pos > last_bracket_pos:
                # Ucięło w środku obiektu - obetnij do ostatniego kompletnego pola
                result_text = result_text[:last_comma_pos + 1]
            elif last_bracket_pos > 0:
                # Ucięło po tablicy - obetnij do końca tablicy
                result_text = result_text[:last_bracket_pos + 1]
            
            # Policz otwarte/zamknięte nawiasy
            open_braces = result_text.count("{")
            close_braces = result_text.count("}")
            open_brackets = result_text.count("[")
            close_brackets = result_text.count("]")
            
            # Dodaj brakujące zamknięcia
            if open_brackets > close_brackets:
                result_text += "]" * (open_brackets - close_brackets)
            if open_braces > close_braces:
                result_text += "}" * (open_braces - close_braces)
            
            log_debug(f"Naprawiony JSON (ostatnie 200 znaków): ...{result_text[-200:]}")
        
        result = json.loads(result_text)
        log_debug("✅ JSON sparsowany pomyślnie")
        
        # Wyciągnij dane
        rating = result.get("rating", 3)
        total_score = result.get("total_score", 50)
        feedback_text = result.get("feedback", "Brak feedbacku")
        strengths = result.get("strengths", [])
        improvements = result.get("improvements", [])
        
        # Sformatuj feedback jako opinię klienta
        feedback = feedback_text
        
        if strengths:
            feedback += "\n\n**👍 Co nam się podobało:**\n"
            feedback += "\n".join([f"• {s}" for s in strengths])
        
        if improvements:
            feedback += "\n\n**� Co mogłoby być lepsze:**\n"
            feedback += "\n".join([f"• {i}" for i in improvements])

        
        # Szczegóły
        details = {
            "method": "ai",
            "model": AI_EVALUATION_CONFIG["model"],
            "total_score": total_score,
            "rating": rating,
            "strengths": strengths,
            "improvements": improvements,
            "word_count": len(solution.split()),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "provider": "google_gemini"
        }
        
        return rating, feedback, details
        
    except ImportError as e:
        log_debug(f"❌ ImportError: {e}")
        print("⚠️ Brak biblioteki google-generativeai. Przekierowuję do kolejki Mistrza Gry.")
        log_debug("Fallback do Game Master (ImportError)")
        if user_data:
            return queue_for_game_master(user_data, contract, solution)
        else:
            # Jeśli brak user_data, zwróć error
            return 0, "❌ Błąd: Brak biblioteki AI i nie można utworzyć kolejki GM", {"method": "error", "error": "ImportError"}
    
    except json.JSONDecodeError as e:
        log_debug(f"❌ JSONDecodeError: {e}")
        print(f"⚠️ Błąd parsowania JSON z Gemini: {e}")
        try:
            if result_text:  # Sprawdź czy result_text istnieje
                print(f"Odpowiedź: {result_text[:200]}")
                log_debug(f"Odpowiedź Gemini: {result_text[:500]}")
        except:
            print("Odpowiedź: brak")
            log_debug("Odpowiedź Gemini: brak")
        print("⚠️ JSON ucięty/błędny. Przekierowuję do kolejki Mistrza Gry.")
        log_debug("Fallback do Game Master (JSONDecodeError)")
        if user_data:
            return queue_for_game_master(user_data, contract, solution)
        else:
            return 0, "❌ Błąd: JSON ucięty i nie można utworzyć kolejki GM", {"method": "error", "error": "JSONDecodeError"}
    
    except Exception as e:
        # Fallback do Game Master w razie błędu
        log_debug(f"❌ Exception: {type(e).__name__}: {e}")
        print(f"⚠️ Błąd oceny AI: {e}")
        print("⚠️ Przekierowuję do kolejki Mistrza Gry...")
        log_debug("Fallback do Game Master (Exception)")
        if user_data:
            return queue_for_game_master(user_data, contract, solution)
        else:
            return 0, "❌ Błąd AI i nie można utworzyć kolejki GM", {"method": "error", "error": str(e)}


# =============================================================================
# TRYB 3: MISTRZ GRY (kolejka oczekujących)
# =============================================================================

def queue_for_game_master(
    user_data: Dict,
    contract: Dict,
    solution: str
) -> Tuple[int, str, Dict]:
    """
    Dodaje rozwiązanie do kolejki oczekujących na ocenę Mistrza Gry
    
    Rozwiązanie nie jest od razu oceniane - trafia do kolejki.
    Admin zaloguje się później i przejrzy wszystkie oczekujące.
    Po ocenie przez Admina kontrakt zostanie sfinalizowany.
    
    Args:
        user_data: Dane użytkownika (username, degencoins itp.)
        contract: Dane kontraktu
        solution: Tekst rozwiązania
    
    Returns:
        (0, feedback, details) - rating=0 oznacza "pending"
    """
    username = user_data.get("username", "unknown")
    review_id = f"review_{username}_{contract['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Przygotuj rekord do kolejki
    pending_review = {
        "id": review_id,
        "username": username,
        "user_display_name": user_data.get("name", username),
        "contract_id": contract["id"],
        "contract_title": contract["tytul"],
        "contract_category": contract["kategoria"],
        "contract_difficulty": contract["poziom_trudnosci"],
        "contract_description": contract["opis"],
        "contract_min_words": contract.get("min_slow", 300),
        "solution": solution,
        "word_count": len(solution.split()),
        "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending",
        "rating": None,
        "feedback": None,
        "reviewed_by": None,
        "reviewed_at": None
    }
    
    # Załaduj kolejkę
    queue = load_game_master_queue()
    
    # Sprawdź limit
    max_pending = GAME_MASTER_CONFIG["max_pending_reviews"]
    pending_count = len([r for r in queue if r["status"] == "pending"])
    
    if pending_count >= max_pending:
        # Kolejka pełna - zwróć tymczasową ocenę i zaloguj ostrzeżenie
        print(f"⚠️ Kolejka Mistrza Gry pełna ({pending_count}/{max_pending}). Rozwiązanie zostanie ocenione później.")
        # Zwróć neutralną ocenę 3/5 z informacją o kolejce
        return 3, f"⏳ Rozwiązanie dodane do kolejki (pozycja {pending_count+1}). Ocena zostanie przeprowadzona przez Mistrza Gry.", {
            "method": "queued_full",
            "queue_position": pending_count + 1,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    # Dodaj do kolejki
    queue.append(pending_review)
    
    # Zapisz
    save_game_master_queue(queue)
    
    # Feedback dla użytkownika
    feedback = f"""✅ **Rozwiązanie przesłane!**

Twoje rozwiązanie oczekuje na ocenę przez Mistrza Gry.
Otrzymasz powiadomienie gdy zostanie ocenione.

⏱️ Szacowany czas oceny: {GAME_MASTER_CONFIG['review_deadline_hours']}h
📊 Liczba słów: {pending_review['word_count']}
"""
    
    # Szczegóły
    details = {
        "method": "game_master",
        "review_id": review_id,
        "status": "pending",
        "word_count": pending_review['word_count'],
        "queue_position": pending_count + 1,
        "timestamp": pending_review["submitted_at"]
    }
    
    return 0, feedback, details  # rating=0 oznacza "pending"


def submit_game_master_review(
    review_id: str,
    rating: int,
    feedback: str,
    admin_username: str
) -> bool:
    """
    Admin zatwierdza ocenę rozwiązania
    
    Wywoływane z panelu admina gdy Mistrz Gry oceni rozwiązanie.
    Aktualizuje status w kolejce i finalizuje kontrakt użytkownika.
    
    Args:
        review_id: ID rekordu z kolejki
        rating: Ocena 1-5 gwiazdek
        feedback: Komentarz od Admina
        admin_username: Username Mistrza Gry
    
    Returns:
        True jeśli sukces, False jeśli błąd
    """
    queue = load_game_master_queue()
    
    # Znajdź review
    for review in queue:
        if review["id"] == review_id and review["status"] == "pending":
            # Zaktualizuj status
            review["status"] = "reviewed"
            review["rating"] = rating
            review["feedback"] = feedback
            review["reviewed_by"] = admin_username
            review["reviewed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Zapisz kolejkę
            save_game_master_queue(queue)
            
            # Finalizuj kontrakt użytkownika
            success = finalize_game_master_contract(review)
            
            return success
    
    return False


def finalize_game_master_contract(review: Dict) -> bool:
    """
    Finalizuje kontrakt po ocenie przez Mistrza Gry
    
    Dodaje monety i reputację użytkownikowi, przenosi kontrakt do completed.
    
    Args:
        review: Rekord z kolejki z oceną
    
    Returns:
        True jeśli sukces
    """
    try:
        from data.users import load_user_data, save_user_data
        from utils.business_game import calculate_contract_reward
        
        users_data = load_user_data()
        username = review["username"]
        
        if username not in users_data:
            print(f"⚠️ Nie znaleziono użytkownika: {username}")
            return False
        
        user_data = users_data[username]
        business_data = user_data.get("business_game", {})
        
        if not business_data:
            print(f"⚠️ Użytkownik {username} nie ma Business Games")
            return False
        
        # Znajdź aktywny kontrakt
        active_contracts = business_data.get("contracts", {}).get("active", [])
        contract_found = None
        
        for contract in active_contracts:
            if contract["id"] == review["contract_id"]:
                contract_found = contract
                break
        
        if not contract_found:
            print(f"⚠️ Nie znaleziono aktywnego kontraktu {review['contract_id']}")
            return False
        
        # Oblicz nagrodę
        reward = calculate_contract_reward(contract_found, review["rating"], business_data)
        
        # Dodaj monety i reputację
        user_data['degencoins'] = user_data.get('degencoins', 0) + reward["coins"]
        business_data["firm"]["reputation"] += reward["reputation"]
        business_data["stats"]["total_revenue"] += reward["coins"]
        
        # Zaktualizuj statystyki ocen
        rating_key = f"contracts_{review['rating']}star"
        business_data["stats"][rating_key] = business_data["stats"].get(rating_key, 0) + 1
        business_data["stats"]["contracts_completed"] = business_data["stats"].get("contracts_completed", 0) + 1
        
        # Przenieś do completed
        completed_contract = contract_found.copy()
        completed_contract["solution"] = review["solution"]
        completed_contract["rating"] = review["rating"]
        completed_contract["feedback"] = review["feedback"]
        completed_contract["reward"] = reward
        completed_contract["completed_date"] = review["reviewed_at"]
        completed_contract["evaluated_by"] = review["reviewed_by"]
        completed_contract["evaluation_method"] = "game_master"
        
        business_data["contracts"]["completed"].append(completed_contract)
        business_data["contracts"]["active"].remove(contract_found)
        
        # Zapisz
        user_data["business_game"] = business_data
        users_data[username] = user_data
        save_user_data(users_data)
        
        print(f"✅ Kontrakt sfinalizowany dla {username}: +{reward['coins']} monet, +{reward['reputation']} reputacji")
        return True
        
    except Exception as e:
        print(f"❌ Błąd finalizacji kontraktu: {e}")
        import traceback
        traceback.print_exc()
        return False


# =============================================================================
# FUNKCJE POMOCNICZE - KONFIGURACJA
# =============================================================================

def get_active_evaluation_mode() -> str:
    """Pobiera aktualny tryb oceny z pliku konfiguracyjnego"""
    from utils.debug_log import log_debug
    
    print(f"🔍 DEBUG: get_active_evaluation_mode() wywoła się...")
    print(f"🔍 DEBUG: SETTINGS_FILE = {SETTINGS_FILE}")
    print(f"🔍 DEBUG: DEFAULT_EVALUATION_MODE = {DEFAULT_EVALUATION_MODE}")
    
    log_debug("get_active_evaluation_mode() wywołane")
    log_debug(f"SETTINGS_FILE = {SETTINGS_FILE}")
    log_debug(f"DEFAULT_EVALUATION_MODE = {DEFAULT_EVALUATION_MODE}")
    
    try:
        if os.path.exists(SETTINGS_FILE):
            print(f"🔍 DEBUG: Plik {SETTINGS_FILE} istnieje")
            log_debug(f"Plik {SETTINGS_FILE} istnieje")
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                mode = config.get("evaluation_mode", DEFAULT_EVALUATION_MODE)
                print(f"🔍 DEBUG: Z pliku odczytano tryb: '{mode}'")
                log_debug(f"Z pliku odczytano tryb: '{mode}'")
                return mode
        else:
            print(f"🔍 DEBUG: Plik {SETTINGS_FILE} NIE istnieje, użyję domyślnego")
            log_debug(f"Plik {SETTINGS_FILE} NIE istnieje")
    except Exception as e:
        print(f"⚠️ Błąd wczytywania trybu oceny: {e}")
        log_debug(f"⚠️ Błąd: {e}")
    
    print(f"🔍 DEBUG: Zwracam DEFAULT: '{DEFAULT_EVALUATION_MODE}'")
    log_debug(f"Zwracam DEFAULT: '{DEFAULT_EVALUATION_MODE}'")
    return DEFAULT_EVALUATION_MODE


def set_active_evaluation_mode(mode: str) -> bool:
    """Ustawia aktywny tryb oceny"""
    try:
        if mode not in EVALUATION_MODES:
            print(f"⚠️ Nieznany tryb: {mode}")
            return False
        
        config = {"evaluation_mode": mode, "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Tryb oceny zmieniony na: {EVALUATION_MODES[mode]['name']}")
        return True
        
    except Exception as e:
        print(f"❌ Błąd zapisywania trybu: {e}")
        return False


def load_gemini_api_key() -> Optional[str]:
    """Ładuje klucz API Google Gemini z pliku konfiguracyjnego"""
    try:
        api_key_file = "config/gemini_api_key.txt"
        if os.path.exists(api_key_file):
            with open(api_key_file, 'r') as f:
                return f.read().strip()
    except Exception as e:
        print(f"⚠️ Błąd wczytywania API key: {e}")
    
    return None


def save_gemini_api_key(api_key: str) -> bool:
    """Zapisuje klucz API Google Gemini do pliku"""
    try:
        api_key_file = "config/gemini_api_key.txt"
        os.makedirs(os.path.dirname(api_key_file), exist_ok=True)
        
        with open(api_key_file, 'w') as f:
            f.write(api_key.strip())
        
        print("✅ Klucz API Gemini zapisany")
        return True
        
    except Exception as e:
        print(f"❌ Błąd zapisywania API key: {e}")
        return False


# =============================================================================
# FUNKCJE POMOCNICZE - KOLEJKA MISTRZA GRY
# =============================================================================

def load_game_master_queue() -> list:
    """Ładuje kolejkę oczekujących rozwiązań"""
    queue_file = GAME_MASTER_CONFIG["queue_file"]
    
    try:
        if os.path.exists(queue_file):
            with open(queue_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Błąd wczytywania kolejki: {e}")
    
    return []


def save_game_master_queue(queue: list) -> bool:
    """Zapisuje kolejkę"""
    queue_file = GAME_MASTER_CONFIG["queue_file"]
    
    try:
        with open(queue_file, 'w', encoding='utf-8') as f:
            json.dump(queue, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Błąd zapisywania kolejki: {e}")
        return False


def get_pending_reviews_count() -> int:
    """Liczba oczekujących ocen"""
    queue = load_game_master_queue()
    return len([r for r in queue if r["status"] == "pending"])


def get_pending_contract_reviews() -> list:
    """
    Pobiera listę oczekujących rozwiązań z dodatkowymi informacjami
    
    Returns:
        Lista recenzji z dodanym polem 'waiting_hours'
    """
    queue = load_game_master_queue()
    pending = [r for r in queue if r["status"] == "pending"]
    
    # Dodaj waiting_hours i urgency flag
    for review in pending:
        try:
            submitted = datetime.strptime(review["submitted_at"], "%Y-%m-%d %H:%M:%S")
            waiting_hours = (datetime.now() - submitted).total_seconds() / 3600
            review["waiting_hours"] = int(waiting_hours)
            review["is_urgent"] = waiting_hours >= GAME_MASTER_CONFIG["urgent_threshold_hours"]
        except Exception:
            review["waiting_hours"] = 0
            review["is_urgent"] = False
    
    # Sortuj: pilne na górze, potem od najstarszych
    pending.sort(key=lambda x: (-x["is_urgent"], -x["waiting_hours"]))
    
    return pending


def get_reviewed_contracts(limit: int = 20) -> list:
    """Pobiera ostatnio ocenione kontrakty"""
    queue = load_game_master_queue()
    reviewed = [r for r in queue if r["status"] == "reviewed"]
    
    # Sortuj od najnowszych
    reviewed.sort(key=lambda x: x.get("reviewed_at", ""), reverse=True)
    
    return reviewed[:limit]


# =============================================================================
# STATYSTYKI
# =============================================================================

def get_evaluation_stats() -> dict:
    """Zwraca statystyki systemu oceny"""
    queue = load_game_master_queue()
    
    pending = [r for r in queue if r["status"] == "pending"]
    reviewed = [r for r in queue if r["status"] == "reviewed"]
    
    stats = {
        "total_reviews": len(queue),
        "pending": len(pending),
        "reviewed": len(reviewed),
        "avg_rating": sum(r["rating"] for r in reviewed) / len(reviewed) if reviewed else 0,
        "active_mode": get_active_evaluation_mode()
    }
    
    return stats


# =============================================================================
# EXPORT
# =============================================================================

__all__ = [
    'evaluate_contract_solution',
    # 'evaluate_heuristic',  # USUNIĘTA - zastąpiona przez Game Master fallback
    'evaluate_with_ai',
    'queue_for_game_master',
    'submit_game_master_review',
    'get_active_evaluation_mode',
    'set_active_evaluation_mode',
    'get_pending_reviews_count',
    'get_pending_contract_reviews',
    'get_reviewed_contracts',
    'get_evaluation_stats',
    'save_gemini_api_key',
    'load_gemini_api_key'
]
