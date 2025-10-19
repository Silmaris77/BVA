"""
Anti-Cheat System - Wykrywanie oszustw w Business Games
Wykrywa copy-paste z ChatGPT i innych AI, oraz zbyt szybkie wypełnianie
"""

import re
from datetime import datetime
from typing import Dict, Tuple, List, Optional
import google.generativeai as genai
import os

# =============================================================================
# KONFIGURACJA
# =============================================================================

# Wzorce AI-generowanego tekstu (polskie i angielskie)
AI_PATTERNS = [
    # Polskie typowe rozpoczęcia
    r"^(W tej sytuacji|Aby rozwiązać|W celu|Najlepszym rozwiązaniem|Pierwszym krokiem)",
    r"(należy rozważyć|istotne jest|warto zwrócić uwagę|kluczowe znaczenie)",
    r"(w kontekście|z perspektywy|biorąc pod uwagę)",
    
    # Angielskie frazy (jeśli ktoś użyje ChatGPT po angielsku i przetłumaczy)
    r"(In this situation|To solve|In order to|The best solution)",
    r"(it is important to|should consider|worth noting|key importance)",
    
    # Zbyt formalna struktura
    r"^\d+\.\s+[A-ZĄŻŹĆŁŚÓĘŃ]",  # Numerowane listy zaczynające zdania
    r"^-\s+[A-ZĄŻŹĆŁŚÓĘŃ]",  # Listy z myślnikami
]

# Minimalne czasy dla różnych długości tekstu (sekundy)
MIN_TIME_THRESHOLDS = {
    100: 20,   # 100 słów = min 20 sekund
    200: 40,   # 200 słów = min 40 sekund
    300: 60,   # 300 słów = min 60 sekund
    500: 100,  # 500 słów = min 100 sekund
    1000: 200, # 1000 słów = min 200 sekund
}

# Maksymalny % tekstu wklejonego naraz (jeśli >80% to podejrzane)
MAX_PASTE_PERCENTAGE = 80

# Kary za wykryte oszustwa
PENALTIES = {
    "time_suspicious": -1,      # Zbyt szybkie - obniż o 1 gwiazdkę
    "paste_detected": -1,       # Masowe wklejanie - obniż o 1 gwiazdkę
    "ai_detected": -2,          # AI wykryte - obniż o 2 gwiazdki
    "multiple_flags": -3        # Wiele flag - obniż o 3 gwiazdki
}

# =============================================================================
# ANALIZA CZASOWA
# =============================================================================

def analyze_writing_time(
    solution: str,
    start_time: datetime,
    submit_time: datetime
) -> Tuple[bool, str, int]:
    """
    Analizuje czy czas pisania jest realistyczny
    
    Args:
        solution: Tekst rozwiązania
        start_time: Kiedy użytkownik otworzył pole tekstowe
        submit_time: Kiedy użytkownik wysłał rozwiązanie
    
    Returns:
        (is_suspicious, reason, penalty)
    """
    word_count = len(solution.split())
    time_taken = (submit_time - start_time).total_seconds()
    
    # Znajdź próg dla danej długości
    threshold_words = sorted([w for w in MIN_TIME_THRESHOLDS.keys() if w <= word_count])
    if threshold_words:
        min_expected_time = MIN_TIME_THRESHOLDS[threshold_words[-1]]
    else:
        min_expected_time = MIN_TIME_THRESHOLDS[100]  # Domyślny
    
    # Sprawdź czy czas jest podejrzanie krótki
    if time_taken < min_expected_time:
        reason = f"⚠️ Podejrzanie szybkie wypełnienie: {int(time_taken)}s dla {word_count} słów (oczekiwano min. {min_expected_time}s)"
        return True, reason, PENALTIES["time_suspicious"]
    
    return False, "", 0

# =============================================================================
# DETEKCJA WKLEJANIA
# =============================================================================

def analyze_paste_behavior(
    paste_events: List[Dict]
) -> Tuple[bool, str, int]:
    """
    Analizuje wzorce wklejania tekstu
    
    Args:
        paste_events: Lista zdarzeń paste: [{"length": 500, "timestamp": "..."}, ...]
    
    Returns:
        (is_suspicious, reason, penalty)
    """
    if not paste_events:
        return False, "", 0
    
    # Policz całkowitą długość wklejonego tekstu
    total_pasted = sum(event.get("length", 0) for event in paste_events)
    
    # Znajdź największe pojedyncze wklejenie
    max_paste = max([event.get("length", 0) for event in paste_events])
    
    # Oszacuj całkowitą długość tekstu (zakładamy że to ostatnie zdarzenie)
    if paste_events:
        last_event = paste_events[-1]
        total_length = last_event.get("total_solution_length", max_paste)
    else:
        total_length = max_paste
    
    # Sprawdź % wklejonego tekstu
    if total_length > 0:
        paste_percentage = (total_pasted / total_length) * 100
        
        if paste_percentage > MAX_PASTE_PERCENTAGE:
            reason = f"⚠️ Wykryto masowe wklejanie: {paste_percentage:.0f}% tekstu wklejone ({total_pasted}/{total_length} znaków)"
            return True, reason, PENALTIES["paste_detected"]
    
    # Sprawdź czy jedno ogromne wklejenie (>500 słów naraz)
    if max_paste > 2500:  # ~500 słów * 5 znaków
        reason = f"⚠️ Wykryto pojedyncze masowe wklejenie: {max_paste} znaków"
        return True, reason, PENALTIES["paste_detected"]
    
    return False, "", 0

# =============================================================================
# DETEKCJA AI-GENEROWANEGO TEKSTU (PATTERN MATCHING)
# =============================================================================

def analyze_ai_patterns(solution: str) -> Tuple[bool, List[str]]:
    """
    Wykrywa charakterystyczne wzorce AI-generowanego tekstu
    
    Args:
        solution: Tekst rozwiązania
    
    Returns:
        (has_ai_patterns, matched_patterns)
    """
    matched = []
    
    for pattern in AI_PATTERNS:
        if re.search(pattern, solution, re.IGNORECASE | re.MULTILINE):
            matched.append(pattern)
    
    # Jeśli 3+ wzorce = wysoka szansa na AI
    return len(matched) >= 3, matched

# =============================================================================
# DETEKCJA AI (GEMINI API)
# =============================================================================

def analyze_with_gemini_ai_detector(solution: str) -> Tuple[bool, str, float]:
    """
    Używa Gemini do wykrycia czy tekst został wygenerowany przez AI
    
    Args:
        solution: Tekst rozwiązania
    
    Returns:
        (is_ai_generated, explanation, confidence)
    """
    try:
        # Pobierz API key z pliku
        api_key_path = os.path.join("config", "gemini_api_key.txt")
        if os.path.exists(api_key_path):
            with open(api_key_path, 'r') as f:
                api_key = f.read().strip()
        else:
            return False, "Brak klucza API Gemini", 0.0
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""Jesteś ekspertem od wykrywania tekstów wygenerowanych przez AI.

Przeanalizuj poniższy tekst i odpowiedz CZY został wygenerowany przez AI (ChatGPT, Gemini, itp.).

TEKST DO ANALIZY:
\"\"\"
{solution}
\"\"\"

ZWRÓĆ ODPOWIEDŹ W FORMACIE JSON:
{{
    "is_ai_generated": true/false,
    "confidence": 0.0-1.0,
    "explanation": "krótkie wyjaśnienie (2-3 zdania)",
    "indicators": ["lista wskaźników AI jeśli wykryto"]
}}

WSKAŹNIKI AI:
- Zbyt formalna/perfekcyjna struktura
- Brak błędów językowych
- Typowe frazy AI ("należy rozważyć", "istotne jest", "w kontekście")
- Listy punktowane bez osobistego kontekstu
- Brak osobistych doświadczeń/przykładów
- Jednolity, "sztuczny" styl pisania"""

        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Parse JSON response
        import json
        # Usuń markdown code blocks jeśli są
        result_text = result_text.replace("```json", "").replace("```", "").strip()
        result = json.loads(result_text)
        
        is_ai = result.get("is_ai_generated", False)
        confidence = result.get("confidence", 0.0)
        explanation = result.get("explanation", "Brak wyjaśnienia")
        
        return is_ai, explanation, confidence
        
    except Exception as e:
        print(f"❌ Błąd w Gemini AI Detection: {e}")
        return False, f"Błąd detekcji: {str(e)}", 0.0

# =============================================================================
# GŁÓWNA FUNKCJA ANALIZY
# =============================================================================

def check_for_cheating(
    solution: str,
    start_time: datetime,
    submit_time: datetime,
    paste_events: Optional[List[Dict]] = None,
    use_ai_detection: bool = True
) -> Dict:
    """
    Kompleksowa analiza oszustw
    
    Args:
        solution: Tekst rozwiązania
        start_time: Kiedy otworzono pole tekstowe
        submit_time: Kiedy wysłano rozwiązanie
        paste_events: Lista zdarzeń paste (opcjonalnie)
        use_ai_detection: Czy użyć Gemini do detekcji AI
    
    Returns:
        {
            "is_suspicious": bool,
            "flags": [lista wykrytych problemów],
            "total_penalty": int,  # Ile gwiazdek odjąć
            "details": {szczegóły każdej analizy},
            "ai_detection": {wynik detekcji AI}
        }
    """
    flags = []
    total_penalty = 0
    details = {}
    
    # 1. Analiza czasu
    time_suspicious, time_reason, time_penalty = analyze_writing_time(
        solution, start_time, submit_time
    )
    if time_suspicious:
        flags.append("time_suspicious")
        total_penalty += time_penalty
        details["time_analysis"] = {
            "suspicious": True,
            "reason": time_reason,
            "penalty": time_penalty
        }
    
    # 2. Analiza wklejania
    paste_suspicious = False  # Inicjalizuj przed użyciem
    if paste_events:
        paste_suspicious, paste_reason, paste_penalty = analyze_paste_behavior(paste_events)
        if paste_suspicious:
            flags.append("paste_detected")
            total_penalty += paste_penalty
            details["paste_analysis"] = {
                "suspicious": True,
                "reason": paste_reason,
                "penalty": paste_penalty
            }
    
    # 3. Analiza wzorców AI (pattern matching)
    has_ai_patterns, matched_patterns = analyze_ai_patterns(solution)
    if has_ai_patterns:
        details["pattern_analysis"] = {
            "ai_patterns_detected": True,
            "matched_count": len(matched_patterns),
            "patterns": matched_patterns[:3]  # Pokaż pierwsze 3
        }
    
    # 4. Analiza AI (Gemini) - tylko jeśli są podejrzane wzorce lub czas/paste
    ai_detection_result = None
    if use_ai_detection and (has_ai_patterns or time_suspicious or (paste_events and paste_suspicious)):
        is_ai, explanation, confidence = analyze_with_gemini_ai_detector(solution)
        
        ai_detection_result = {
            "is_ai_generated": is_ai,
            "confidence": confidence,
            "explanation": explanation
        }
        
        # Jeśli AI wykryte z wysoką pewnością (>70%)
        if is_ai and confidence > 0.7:
            flags.append("ai_detected")
            total_penalty += PENALTIES["ai_detected"]
            details["ai_detection"] = ai_detection_result
    
    # 5. Kara za wiele flag (jeśli 2+ flagi)
    if len(flags) >= 2:
        flags.append("multiple_flags")
        # Zastąp karę na wyższą dla wielu flag
        total_penalty = PENALTIES["multiple_flags"]
    
    # Wynik końcowy
    return {
        "is_suspicious": len(flags) > 0,
        "flags": flags,
        "total_penalty": total_penalty,
        "details": details,
        "ai_detection": ai_detection_result
    }

# =============================================================================
# FUNKCJE POMOCNICZE
# =============================================================================

def format_anti_cheat_warning(check_result: Dict) -> str:
    """
    Formatuje ostrzeżenie dla użytkownika o wykrytych problemach
    
    Args:
        check_result: Wynik z check_for_cheating()
    
    Returns:
        Sformatowany tekst ostrzeżenia
    """
    if not check_result["is_suspicious"]:
        return ""
    
    warnings = []
    
    # Czas
    if "time_suspicious" in check_result["flags"]:
        warnings.append(check_result["details"]["time_analysis"]["reason"])
    
    # Paste
    if "paste_detected" in check_result["flags"]:
        warnings.append(check_result["details"]["paste_analysis"]["reason"])
    
    # AI
    if "ai_detected" in check_result["flags"] and check_result["ai_detection"]:
        ai_result = check_result["ai_detection"]
        warnings.append(f"🤖 Wykryto AI-generowany tekst (pewność: {ai_result['confidence']*100:.0f}%): {ai_result['explanation']}")
    
    # Penalty
    penalty_text = f"\n\n⚠️ **KARA: -{check_result['total_penalty']} ⭐ do oceny**"
    
    return "\n".join(warnings) + penalty_text

def apply_anti_cheat_penalty(original_rating: int, penalty: int) -> int:
    """
    Aplikuje karę do oceny (minimum 1 gwiazdka)
    
    Args:
        original_rating: Oryginalna ocena (1-5)
        penalty: Kara do odjęcia
    
    Returns:
        Nowa ocena (min 1)
    """
    return max(1, original_rating - penalty)
