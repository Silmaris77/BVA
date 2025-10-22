"""
AI Conversation Engine - Symulacja rozmów z NPC (pracownicy, klienci, partnerzy)
===============================================================================

Ten moduł obsługuje dynamiczne rozmowy AI w kontraktach biznesowych.
Zamiast klikać w gotowe odpowiedzi, gracz pisze swoje własne, a AI:
- Ocenia jakość odpowiedzi (empathy, assertiveness, professionalism)
- Generuje dynamiczną reakcję NPC
- Prowadzi rozmowę dalej w oparciu o kontekst
- Generuje głos dla odpowiedzi NPC (TTS)
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import google.generativeai as genai
import os
import base64
from pathlib import Path

# Dodatkowy import dla TTS
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


def generate_npc_audio(text: str, npc_config: Dict) -> Optional[str]:
    """
    Generuje plik audio z tekstem NPC używając gTTS.
    
    Args:
        text: Tekst do wypowiedzenia
        npc_config: Konfiguracja NPC (dla dostosowania głosu)
        
    Returns:
        Base64 encoded audio data lub None jeśli TTS niedostępne
    """
    if not TTS_AVAILABLE or not text:
        return None
    
    try:
        # Określ język i parametry głosu
        lang = "pl"  # Polski
        slow = False  # Normalna prędkość
        
        # Opcjonalnie: dostosuj parametry na podstawie emocji/roli NPC
        # Dla przykładu - można rozszerzyć o różne głosy/tempo
        
        # Generuj audio
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # Zapisz do tymczasowego pliku
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        
        audio_file = temp_dir / f"npc_audio_{datetime.now().timestamp()}.mp3"
        tts.save(str(audio_file))
        
        # Odczytaj jako base64
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()
        
        # Usuń tymczasowy plik
        try:
            audio_file.unlink()
        except:
            pass
        
        return audio_base64
        
    except Exception as e:
        print(f"TTS Error: {e}")
        return None


def initialize_ai_conversation(contract_id: str, npc_config: Dict, scenario_context: str):
    """
    Inicjalizuje rozmowę AI dla danego kontraktu.
    
    Args:
        contract_id: Unikalny ID kontraktu
        npc_config: Konfiguracja NPC (imię, rola, osobowość, cel)
        scenario_context: Kontekst scenariusza (sytuacja, tło, cel rozmowy)
    """
    # Initialize session state for this conversation
    conv_key = f"ai_conv_{contract_id}"
    
    if conv_key not in st.session_state:
        st.session_state[conv_key] = {
            "messages": [],  # Historia rozmowy: [{role: "npc/player", text: str, timestamp: str, score: int}]
            "current_turn": 0,
            "total_score": 0,
            "metrics": {
                "empathy_score": 0,
                "assertiveness_score": 0,
                "professionalism_score": 0,
                "solution_quality": 0,
                "relationship_health": 50  # Starts neutral (0-100)
            },
            "npc_config": npc_config,
            "scenario_context": scenario_context,
            "conversation_active": True,
            "ending_reached": False,
            "ending_type": None  # "success", "neutral", "failure"
        }
        
        # NPC sends opening message
        opening_message = npc_config.get("opening_message", "Dzień dobry.")
        opening_audio = generate_npc_audio(opening_message, npc_config)
        
        st.session_state[conv_key]["messages"].append({
            "role": "npc",
            "text": opening_message,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "emotion": npc_config.get("initial_emotion", "neutral"),
            "audio": opening_audio
        })


def get_conversation_state(contract_id: str) -> Dict:
    """Pobiera aktualny stan rozmowy"""
    conv_key = f"ai_conv_{contract_id}"
    return st.session_state.get(conv_key, {})


def evaluate_player_response(
    player_message: str,
    conversation_history: List[Dict],
    npc_config: Dict,
    scenario_context: str,
    gemini_api_key: str
) -> Dict:
    """
    Ocenia odpowiedź gracza używając Gemini AI.
    
    Returns:
        Dict: {
            "empathy": int (0-100),
            "assertiveness": int (0-100),
            "professionalism": int (0-100),
            "solution_quality": int (0-100),
            "relationship_impact": int (-30 to +30),
            "feedback": str,
            "points": int (0-20)
        }
    """
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
    
    # Build conversation history for context
    history_text = "\n".join([
        f"{'NPC' if msg['role'] == 'npc' else 'GRACZ'}: {msg['text']}"
        for msg in conversation_history[-5:]  # Last 5 messages for context
    ])
    
    evaluation_prompt = f"""Jesteś ekspertem od analizy rozmów biznesowych i komunikacji interpersonalnej.

KONTEKST SCENARIUSZA:
{scenario_context}

PROFIL NPC (rozmówcy):
- Imię: {npc_config.get('name', 'Unknown')}
- Rola: {npc_config.get('role', 'Unknown')}
- Osobowość: {npc_config.get('personality', 'neutral')}
- Aktualny stan emocjonalny: {npc_config.get('current_emotion', 'neutral')}
- Cel NPC: {npc_config.get('goal', 'Unknown')}

HISTORIA ROZMOWY (ostatnie 5 wiadomości):
{history_text}

OSTATNIA ODPOWIEDŹ GRACZA:
{player_message}

ZADANIE:
Oceń jakość odpowiedzi gracza w 4 wymiarach (0-100 punktów każdy):

1. EMPATHY (empatia) - Czy gracz rozumie emocje i perspektywę rozmówcy?
2. ASSERTIVENESS (asertywność) - Czy gracz wyraża swoją opinię jasno ale nie agresywnie?
3. PROFESSIONALISM (profesjonalizm) - Czy ton i forma są odpowiednie biznesowo?
4. SOLUTION_QUALITY (jakość rozwiązania) - Czy gracz proponuje konstruktywne rozwiązanie?

Dodatkowo oceń:
- RELATIONSHIP_IMPACT (-30 do +30) - Jak ta wypowiedź wpłynie na relację z rozmówcą?
- POINTS (0-20) - Ogólna jakość tej wypowiedzi (suma powyższych czynników)

Zwróć odpowiedź w DOKŁADNIE tym formacie JSON (tylko JSON, bez markdown, bez dodatkowych komentarzy):
{{
  "empathy": <0-100>,
  "assertiveness": <0-100>,
  "professionalism": <0-100>,
  "solution_quality": <0-100>,
  "relationship_impact": <-30 do +30>,
  "points": <0-20>,
  "feedback": "<krótka (1-2 zdania) informacja zwrotna dla gracza - co zrobił dobrze, co można poprawić>"
}}"""

    try:
        response = model.generate_content(evaluation_prompt)
        result_text = response.text.strip()
        
        # Clean up response (remove markdown code blocks if present)
        if result_text.startswith("```json"):
            result_text = result_text.replace("```json", "").replace("```", "").strip()
        elif result_text.startswith("```"):
            result_text = result_text.replace("```", "").strip()
        
        import json
        evaluation = json.loads(result_text)
        return evaluation
        
    except Exception as e:
        # Fallback evaluation if AI fails
        return {
            "empathy": 50,
            "assertiveness": 50,
            "professionalism": 50,
            "solution_quality": 50,
            "relationship_impact": 0,
            "points": 10,
            "feedback": f"[Błąd oceny AI: {str(e)}] Odpowiedź przyjęta z domyślną oceną."
        }


def generate_npc_reaction(
    player_message: str,
    evaluation: Dict,
    conversation_history: List[Dict],
    npc_config: Dict,
    scenario_context: str,
    current_metrics: Dict,
    gemini_api_key: str
) -> Dict:
    """
    Generuje dynamiczną reakcję NPC na odpowiedź gracza.
    
    Returns:
        Dict: {
            "text": str (reakcja NPC),
            "emotion": str ("happy", "neutral", "sad", "angry", "defensive", "grateful"),
            "conversation_continues": bool,
            "ending_triggered": bool,
            "ending_type": Optional[str] ("success", "neutral", "failure")
        }
    """
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
    
    # Build conversation history
    history_text = "\n".join([
        f"{'NPC' if msg['role'] == 'npc' else 'GRACZ'}: {msg['text']}"
        for msg in conversation_history
    ])
    
    turn_count = len([m for m in conversation_history if m['role'] == 'player'])
    relationship_health = current_metrics.get("relationship_health", 50)
    
    reaction_prompt = f"""Jesteś {npc_config.get('name')} - {npc_config.get('role')}.

TWOJA OSOBOWOŚĆ: {npc_config.get('personality', 'neutral')}
TWÓJ CEL W TEJ ROZMOWIE: {npc_config.get('goal')}

KONTEKST SCENARIUSZA:
{scenario_context}

PEŁNA HISTORIA ROZMOWY:
{history_text}

OSTATNIA WYPOWIEDŹ GRACZA:
{player_message}

OCENA TEJ WYPOWIEDZI PRZEZ SYSTEM:
- Empatia: {evaluation.get('empathy', 50)}/100
- Asertywność: {evaluation.get('assertiveness', 50)}/100
- Profesjonalizm: {evaluation.get('professionalism', 50)}/100
- Jakość rozwiązania: {evaluation.get('solution_quality', 50)}/100
- Wpływ na relację: {evaluation.get('relationship_impact', 0)}

AKTUALNY STAN RELACJI: {relationship_health}/100
TURA KONWERSACJI: {turn_count}

ZADANIE:
Wygeneruj swoją reakcję jako {npc_config.get('name')}. Bądź naturalny i realistyczny - reaguj na TON i TREŚĆ wypowiedzi gracza.

WAŻNE ZASADY:
1. Jeśli gracz był empatyczny i profesjonalny (oceny >70) - bądź bardziej otwarty i współpracujący
2. Jeśli gracz był agresywny lub nieprofesjonalny (oceny <40) - bądź defensywny lub zdenerwowany
3. Jeśli relationship_health < 30 lub turn_count >= 8 - rozważ zakończenie rozmowy
4. Jeśli wypracowano dobre rozwiązanie (solution_quality > 75 i relationship_health > 60) - zaakceptuj i zakończ pozytywnie
5. Pamiętaj o swojej osobowości - {npc_config.get('personality_notes', 'bądź sobą')}

Zwróć odpowiedź w DOKŁADNIE tym formacie JSON (tylko JSON, bez markdown):
{{
  "text": "<Twoja reakcja jako {npc_config.get('name')} - 2-4 zdania, naturalnie, z emocjami>",
  "emotion": "<happy|neutral|sad|angry|defensive|grateful|hopeful>",
  "conversation_continues": <true|false - czy rozmowa powinna trwać dalej>,
  "ending_triggered": <true|false - czy to już koniec rozmowy>,
  "ending_type": "<success|neutral|failure - TYLKO jeśli ending_triggered=true, inaczej null>"
}}"""

    try:
        response = model.generate_content(reaction_prompt)
        result_text = response.text.strip()
        
        # Clean up response
        if result_text.startswith("```json"):
            result_text = result_text.replace("```json", "").replace("```", "").strip()
        elif result_text.startswith("```"):
            result_text = result_text.replace("```", "").strip()
        
        import json
        reaction = json.loads(result_text)
        
        # Generate audio for NPC response
        audio_data = generate_npc_audio(reaction.get("text", ""), npc_config)
        reaction["audio"] = audio_data
        return reaction
        
    except Exception as e:
        # Fallback reaction
        return {
            "text": f"Rozumiem. {npc_config.get('fallback_response', 'Dziękuję za rozmowę.')}",
            "emotion": "neutral",
            "conversation_continues": turn_count < 6,
            "ending_triggered": turn_count >= 6,
            "ending_type": "neutral" if turn_count >= 6 else None
        }


def process_player_message(
    contract_id: str,
    player_message: str,
    gemini_api_key: str
) -> Tuple[Dict, Dict]:
    """
    Przetwarza wiadomość gracza - ocenia ją i generuje reakcję NPC.
    
    Returns:
        Tuple[Dict, Dict]: (evaluation, npc_reaction)
    """
    conv_key = f"ai_conv_{contract_id}"
    conv_state = st.session_state.get(conv_key)
    
    if not conv_state:
        raise ValueError(f"Conversation not initialized for contract {contract_id}")
    
    # Evaluate player's message
    evaluation = evaluate_player_response(
        player_message,
        conv_state["messages"],
        conv_state["npc_config"],
        conv_state["scenario_context"],
        gemini_api_key
    )
    
    # Update metrics
    conv_state["metrics"]["empathy_score"] += evaluation.get("empathy", 0)
    conv_state["metrics"]["assertiveness_score"] += evaluation.get("assertiveness", 0)
    conv_state["metrics"]["professionalism_score"] += evaluation.get("professionalism", 0)
    conv_state["metrics"]["solution_quality"] += evaluation.get("solution_quality", 0)
    conv_state["metrics"]["relationship_health"] += evaluation.get("relationship_impact", 0)
    conv_state["metrics"]["relationship_health"] = max(0, min(100, conv_state["metrics"]["relationship_health"]))
    
    conv_state["total_score"] += evaluation.get("points", 0)
    conv_state["current_turn"] += 1
    
    # Add player message to history
    conv_state["messages"].append({
        "role": "player",
        "text": player_message,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "evaluation": evaluation
    })
    
    # Generate NPC reaction
    npc_reaction = generate_npc_reaction(
        player_message,
        evaluation,
        conv_state["messages"],
        conv_state["npc_config"],
        conv_state["scenario_context"],
        conv_state["metrics"],
        gemini_api_key
    )
    
    # Add NPC reaction to history
    conv_state["messages"].append({
        "role": "npc",
        "text": npc_reaction["text"],
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "emotion": npc_reaction["emotion"],
        "audio": npc_reaction.get("audio")  # Dodaj audio do historii
    })
    
    # Check if conversation should end
    if npc_reaction.get("ending_triggered"):
        conv_state["conversation_active"] = False
        conv_state["ending_reached"] = True
        conv_state["ending_type"] = npc_reaction.get("ending_type", "neutral")
    
    st.session_state[conv_key] = conv_state
    
    return evaluation, npc_reaction


def calculate_final_conversation_score(contract_id: str) -> Dict:
    """
    Oblicza finalny wynik rozmowy i konwertuje na gwiazdki.
    
    Returns:
        Dict: {
            "stars": int (1-5),
            "total_points": int,
            "metrics": Dict (empathy, assertiveness, etc.),
            "ending_type": str,
            "turn_count": int,
            "summary": str
        }
    """
    conv_key = f"ai_conv_{contract_id}"
    conv_state = st.session_state.get(conv_key, {})
    
    total_points = conv_state.get("total_score", 0)
    turn_count = conv_state.get("current_turn", 0)
    metrics = conv_state.get("metrics", {})
    ending_type = conv_state.get("ending_type", "neutral")
    
    # Average metrics (divide by turn count)
    if turn_count > 0:
        avg_empathy = metrics.get("empathy_score", 0) / turn_count
        avg_assertiveness = metrics.get("assertiveness_score", 0) / turn_count
        avg_professionalism = metrics.get("professionalism_score", 0) / turn_count
        avg_solution = metrics.get("solution_quality", 0) / turn_count
    else:
        avg_empathy = avg_assertiveness = avg_professionalism = avg_solution = 0
    
    relationship_health = metrics.get("relationship_health", 50)
    
    # Calculate stars based on:
    # - Total points earned
    # - Ending type (success bonus, failure penalty)
    # - Relationship health
    
    base_stars = 3  # Start with 3 stars
    
    # Points factor (+/- 1 star)
    if total_points >= 100:
        base_stars += 1
    elif total_points < 50:
        base_stars -= 1
    
    # Ending type factor (+/- 1 star)
    if ending_type == "success":
        base_stars += 1
    elif ending_type == "failure":
        base_stars -= 1
    
    # Relationship health factor
    if relationship_health >= 70:
        base_stars += 0.5
    elif relationship_health < 30:
        base_stars -= 0.5
    
    # Clamp to 1-5
    stars = int(max(1, min(5, base_stars)))
    
    # Generate summary
    ending_type_display = ending_type.upper() if ending_type else "NEUTRAL"
    summary = f"""
    Rozmowa zakończona po {turn_count} turach.
    
    📊 Średnie oceny:
    - Empatia: {avg_empathy:.0f}/100
    - Asertywność: {avg_assertiveness:.0f}/100
    - Profesjonalizm: {avg_professionalism:.0f}/100
    - Jakość rozwiązań: {avg_solution:.0f}/100
    
    🤝 Zdrowie relacji: {relationship_health}/100
    🎯 Typ zakończenia: {ending_type_display}
    ⭐ Ocena: {stars}/5 gwiazdek
    """
    
    return {
        "stars": stars,
        "total_points": total_points,
        "metrics": {
            "empathy": avg_empathy,
            "assertiveness": avg_assertiveness,
            "professionalism": avg_professionalism,
            "solution_quality": avg_solution,
            "relationship_health": relationship_health
        },
        "ending_type": ending_type,
        "turn_count": turn_count,
        "summary": summary
    }


def reset_conversation(contract_id: str, npc_config: Dict, scenario_context: str):
    """Resetuje rozmowę - pozwala zagrać ponownie"""
    conv_key = f"ai_conv_{contract_id}"
    if conv_key in st.session_state:
        del st.session_state[conv_key]
    initialize_ai_conversation(contract_id, npc_config, scenario_context)
