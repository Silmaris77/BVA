"""
Speed Challenge Engine
======================
Obsługuje kontrakt z limitem czasu - gracz musi szybko odpowiedzieć na urgent sytuację.

Features:
- Real-time countdown timer
- Speed bonus calculation
- Pressure mechanics
- AI evaluation of quick responses
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import time

# =============================================================================
# STATE MANAGEMENT
# =============================================================================

def initialize_speed_challenge(contract_id: str, challenge_config: Dict[str, Any], time_limit: int):
    """
    Inicjalizuje Speed Challenge
    
    Args:
        contract_id: Unique contract ID
        challenge_config: Configuration with problem, client, etc.
        time_limit: Time limit in seconds
    """
    if f"speed_challenge_{contract_id}" not in st.session_state:
        st.session_state[f"speed_challenge_{contract_id}"] = {
            "started": False,
            "start_time": None,
            "time_limit": time_limit,
            "challenge_config": challenge_config,
            "player_response": "",
            "completed": False,
            "time_taken": None,
            "evaluation_result": None,
            "failed_timeout": False
        }


def get_challenge_state(contract_id: str) -> Optional[Dict[str, Any]]:
    """Pobiera stan Speed Challenge"""
    return st.session_state.get(f"speed_challenge_{contract_id}")


def start_challenge(contract_id: str):
    """Rozpoczyna challenge - uruchamia timer"""
    state = get_challenge_state(contract_id)
    if state and not state["started"]:
        state["started"] = True
        state["start_time"] = time.time()


def submit_response(contract_id: str, response: str) -> Dict[str, Any]:
    """
    Zapisuje odpowiedź gracza i oblicza czas
    
    Returns:
        Dict with time_taken, on_time, speed_bonus
    """
    state = get_challenge_state(contract_id)
    if not state:
        return {"error": "Challenge not initialized"}
    
    current_time = time.time()
    time_taken = current_time - state["start_time"]
    time_limit = state["time_limit"]
    
    # Sprawdź czy w czasie
    on_time = time_taken <= time_limit
    
    # Oblicz speed bonus (im szybciej, tym lepiej)
    if on_time:
        # 100% bonus jeśli w pierwszych 25% czasu
        # 0% bonus jeśli dokładnie na limicie
        time_ratio = time_taken / time_limit
        speed_bonus = max(0, 1 - time_ratio)  # 0.0 do 1.0
    else:
        speed_bonus = 0
        state["failed_timeout"] = True
    
    state["player_response"] = response
    state["time_taken"] = time_taken
    state["completed"] = True
    
    return {
        "time_taken": time_taken,
        "time_limit": time_limit,
        "on_time": on_time,
        "speed_bonus": speed_bonus
    }


def reset_challenge(contract_id: str):
    """Resetuje challenge do stanu początkowego"""
    if f"speed_challenge_{contract_id}" in st.session_state:
        del st.session_state[f"speed_challenge_{contract_id}"]


# =============================================================================
# TIMER RENDERING
# =============================================================================

def get_remaining_time(contract_id: str) -> float:
    """
    Oblicza pozostały czas w sekundach
    
    Returns:
        Float: Remaining seconds (może być ujemne jeśli przekroczono)
    """
    state = get_challenge_state(contract_id)
    if not state or not state["started"]:
        return state["time_limit"] if state else 0
    
    elapsed = time.time() - state["start_time"]
    remaining = state["time_limit"] - elapsed
    return remaining


def render_timer(contract_id: str, placeholder) -> bool:
    """
    Renderuje live countdown timer
    
    Args:
        placeholder: Streamlit placeholder do update
    
    Returns:
        bool: True jeśli czas minął
    """
    state = get_challenge_state(contract_id)
    if not state or not state["started"] or state["completed"]:
        return False
    
    remaining = get_remaining_time(contract_id)
    
    if remaining <= 0:
        # Czas minął!
        placeholder.markdown("""
        <div style='background: #fee; border: 2px solid #f00; 
                    padding: 16px; border-radius: 8px; text-align: center;'>
            <h2 style='color: #c00; margin: 0;'>⏰ CZAS MINĄŁ!</h2>
            <p style='margin: 8px 0 0 0;'>Zbyt późno na odpowiedź...</p>
        </div>
        """, unsafe_allow_html=True)
        return True
    
    # Renderuj timer z kolorami
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    
    # Kolor zależny od pozostałego czasu
    if remaining > state["time_limit"] * 0.5:
        color = "#4ade80"  # Zielony
        bg_color = "#f0fdf4"
    elif remaining > state["time_limit"] * 0.25:
        color = "#fbbf24"  # Żółty
        bg_color = "#fffbeb"
    else:
        color = "#f87171"  # Czerwony
        bg_color = "#fef2f2"
    
    placeholder.markdown(f"""
    <div style='background: {bg_color}; border: 2px solid {color}; 
                padding: 16px; border-radius: 8px; text-align: center;'>
        <h2 style='color: {color}; margin: 0; font-size: 48px; font-family: monospace;'>
            {minutes:02d}:{seconds:02d}
        </h2>
        <p style='margin: 8px 0 0 0; color: #666;'>Pozostały czas</p>
    </div>
    """, unsafe_allow_html=True)
    
    return False


# =============================================================================
# AI EVALUATION
# =============================================================================

def evaluate_speed_response(
    contract_id: str,
    response: str,
    challenge_config: Dict[str, Any],
    time_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Ocenia odpowiedź gracza używając AI
    
    Args:
        contract_id: Contract ID
        response: Player's response
        challenge_config: Challenge configuration
        time_info: Time metrics (time_taken, on_time, speed_bonus)
    
    Returns:
        Dict with evaluation results
    """
    try:
        import google.generativeai as genai
        import os
        
        # Pobierz API key - najpierw Streamlit secrets, potem ENV
        api_key = None
        try:
            api_key = st.secrets["GOOGLE_API_KEY"]
        except:
            api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            raise Exception("Brak klucza API Google Gemini")
        
        # Konfiguruj Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Używamy najnowszego modelu
        
        # Przygotuj prompt dla AI
        evaluation_prompt = f"""
        Oceń odpowiedź konsultanta na PILNĄ sytuację klienta.
        
        **SYTUACJA:**
        {challenge_config.get('problem', '')}
        
        **ODPOWIEDŹ KONSULTANTA:**
        {response}
        
        **LIMIT CZASU:** {time_info['time_limit']} sekund
        **CZAS ODPOWIEDZI:** {time_info['time_taken']:.1f} sekund
        **W CZASIE:** {'TAK ✅' if time_info['on_time'] else 'NIE ❌ - Spóźnienie!'}
        
        **KRYTERIA OCENY:**
        {chr(10).join(f"- {k}: {v}" for k, v in challenge_config.get('evaluation_criteria', {}).items())}
        
        **IDEALNE ELEMENTY (powinny się pojawić):**
        {', '.join(challenge_config.get('ideal_answer_keywords', []))}
        
        Oceń odpowiedź w skali 1-5 gwiazdek:
        
        ⭐ 1 gwiazdka: Słaba odpowiedź - brak konkretów, nie pomaga klientowi
        ⭐⭐ 2 gwiazdki: Poniżej oczekiwań - niektóre elementy OK ale gaps
        ⭐⭐⭐ 3 gwiazdki: Akceptowalne - podstawowe elementy covered
        ⭐⭐⭐⭐ 4 gwiazdki: Dobra odpowiedź - profesjonalna, pomocna
        ⭐⭐⭐⭐⭐ 5 gwiazdek: Doskonała - zwięzła, konkretna, actionable, uspokajająca
        
        {"UWAGA: Klient dostał odpowiedź PO czasie - to automatycznie obniża ocenę o 1-2 gwiazdki!" if not time_info['on_time'] else ""}
        
        Zwróć JSON:
        {{
            "stars": <1-5>,
            "points": <0-100>,
            "feedback": "<2-3 zdania feedback>",
            "strengths": ["<co było dobre>"],
            "improvements": ["<co poprawić>"],
            "time_pressure_bonus": <true/false - czy dobrze radził sobie pod presją czasu>
        }}
        """
        
        # Wywołaj AI
        ai_response = model.generate_content(evaluation_prompt)
        
        # Parse JSON z odpowiedzi
        import json
        import re
        
        # Wyciągnij JSON z odpowiedzi (może być w ```json ... ```)
        response_text = ai_response.text
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(1)
        else:
            # Spróbuj całej odpowiedzi
            json_text = response_text
        
        ai_result = json.loads(json_text)
        
        # Zastosuj speed bonus do punktów
        base_points = ai_result.get("points", 0)
        speed_multiplier = 1 + (time_info["speed_bonus"] * 0.5)  # Do +50% za szybkość
        final_points = int(base_points * speed_multiplier)
        
        # Jeśli przekroczono czas - obniż gwiazdki
        stars = ai_result.get("stars", 3)
        if not time_info["on_time"]:
            stars = max(1, stars - 2)  # -2 gwiazdki za timeout
            ai_result["timeout_penalty"] = "Przekroczono limit czasu - ocena obniżona"
        
        ai_result["points"] = final_points
        ai_result["base_points"] = base_points
        ai_result["speed_bonus_applied"] = time_info["speed_bonus"]
        ai_result["stars"] = stars
        ai_result["time_taken"] = time_info["time_taken"]
        ai_result["on_time"] = time_info["on_time"]
        
        return ai_result
        
    except Exception as e:
        # Fallback jeśli AI nie działa
        print(f"❌ Speed Challenge AI evaluation error: {e}")
        
        # Prosta ocena fallback
        response_length = len(response.strip())
        
        if not time_info["on_time"]:
            stars = 1
            points = 20
        elif response_length < 50:
            stars = 2
            points = 40
        elif response_length < 150:
            stars = 3
            points = 60
        elif response_length < 300:
            stars = 4
            points = 80
        else:
            stars = 5
            points = 100
        
        # Zastosuj speed bonus
        speed_multiplier = 1 + (time_info["speed_bonus"] * 0.5)
        final_points = int(points * speed_multiplier)
        
        return {
            "stars": stars,
            "points": final_points,
            "base_points": points,
            "speed_bonus_applied": time_info["speed_bonus"],
            "feedback": f"Ocena automatyczna (AI error: {str(e)})",
            "strengths": ["Odpowiedź została wysłana"],
            "improvements": ["Spróbuj być bardziej konkretny i actionable"],
            "time_taken": time_info["time_taken"],
            "on_time": time_info["on_time"],
            "fallback_evaluation": True
        }


# =============================================================================
# COMPLETE WORKFLOW
# =============================================================================

def complete_speed_challenge(
    contract_id: str,
    response: str,
    challenge_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Kompletny workflow: submit response → evaluate → return results
    
    Returns:
        Complete evaluation with stars, points, feedback
    """
    # 1. Submit i oblicz czas
    time_info = submit_response(contract_id, response)
    
    # 2. Oceń odpowiedź
    evaluation = evaluate_speed_response(
        contract_id, 
        response, 
        challenge_config, 
        time_info
    )
    
    # 3. Zapisz w state
    state = get_challenge_state(contract_id)
    if state:
        state["evaluation_result"] = evaluation
    
    return evaluation
