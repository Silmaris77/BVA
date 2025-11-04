"""
🤖 AI Task Evaluator
Ocena rozwiązań zadań biznesowych przez Gemini AI
"""

import google.generativeai as genai
import streamlit as st
import os
from typing import Dict, Tuple


def evaluate_task_solution(task: Dict, solution: str) -> Tuple[float, str, Dict]:
    """
    Ocenia rozwiązanie zadania przez AI (Gemini)
    
    Args:
        task: Dict z zadaniem (title, scenario, category, difficulty)
        solution: Rozwiązanie gracza (tekst)
    
    Returns:
        Tuple[quality_score (0-1), feedback (str), detailed_scores (Dict)]
    """
    
    # Pobierz API key
    api_key = None
    try:
        api_key = st.secrets["API_KEYS"]["gemini"]
    except:
        try:
            with open("config/gemini_api_key.txt", "r") as f:
                api_key = f.read().strip()
        except:
            api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        # Fallback - podstawowa ocena bez AI
        basic_score = min(1.0, len(solution.strip()) / 200)
        return (
            basic_score,
            "⚠️ Brak klucza API Gemini - użyto oceny podstawowej na podstawie długości tekstu.",
            {"length": int(basic_score * 100), "relevance": 0, "actionability": 0, "business_impact": 0, "creativity": 0}
        )
    
    # Konfiguruj Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    # Prompt dla AI
    prompt = f"""Jesteś ekspertem od sprzedaży FMCG i oceniasz rozwiązanie zadania biznesowego.

**ZADANIE:**
Tytuł: {task.get('title', 'Brak tytułu')}
Kategoria: {task.get('category', 'Brak kategorii')}
Trudność: {task.get('difficulty', 'Brak trudności')}

Sytuacja:
{task.get('scenario', 'Brak opisu scenariusza')}

**ROZWIĄZANIE GRACZA:**
{solution}

**TWOJA OCENA:**
Oceń rozwiązanie w skali 0-100 w 4 kategoriach:
1. **Relevance (Trafność)**: Czy rozwiązanie odnosi się do problemu opisanego w zadaniu?
2. **Actionability (Wykonalność)**: Czy można to zrealizować w praktyce? Czy są konkretne kroki?
3. **Business Impact (Wpływ biznesowy)**: Czy to przyniesie realne rezultaty biznesowe?
4. **Creativity (Kreatywność)**: Czy jest innowacyjne, przemyślane, wykracza poza oczywiste?

**FORMAT ODPOWIEDZI (DOKŁADNIE TAK - KAŻDA LINIA ZACZYNA SIĘ OD SŁOWA KLUCZOWEGO):**
RELEVANCE: [liczba 0-100]
ACTIONABILITY: [liczba 0-100]
BUSINESS_IMPACT: [liczba 0-100]
CREATIVITY: [liczba 0-100]
OVERALL: [liczba 0-100]

FEEDBACK:
[2-3 zdania konstruktywnego feedbacku - co jest dobre w rozwiązaniu i co można poprawić]

TONE:
[pozytywny/neutralny/krytyczny]

PRZYKŁAD:
RELEVANCE: 85
ACTIONABILITY: 90
BUSINESS_IMPACT: 80
CREATIVITY: 75
OVERALL: 82

FEEDBACK:
Świetne rozwiązanie! Bardzo trafnie zidentyfikowałeś problem i zaproponowałeś konkretne kroki działania. Jedyny mankament - brakuje konkretnego timeframe'u realizacji. Pamiętaj o deadline'ach!

TONE:
pozytywny
"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parsuj odpowiedź
        scores = {}
        feedback = ""
        tone = "neutral"
        
        lines = response_text.split("\n")
        parsing_feedback = False
        feedback_lines = []
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("RELEVANCE:"):
                try:
                    scores["relevance"] = int(line.split(":")[1].strip())
                except:
                    scores["relevance"] = 50
            elif line.startswith("ACTIONABILITY:"):
                try:
                    scores["actionability"] = int(line.split(":")[1].strip())
                except:
                    scores["actionability"] = 50
            elif line.startswith("BUSINESS_IMPACT:"):
                try:
                    scores["business_impact"] = int(line.split(":")[1].strip())
                except:
                    scores["business_impact"] = 50
            elif line.startswith("CREATIVITY:"):
                try:
                    scores["creativity"] = int(line.split(":")[1].strip())
                except:
                    scores["creativity"] = 50
            elif line.startswith("OVERALL:"):
                try:
                    scores["overall"] = int(line.split(":")[1].strip())
                except:
                    scores["overall"] = 50
            elif line.startswith("FEEDBACK:"):
                parsing_feedback = True
            elif line.startswith("TONE:"):
                parsing_feedback = False
                tone = line.split(":")[1].strip().lower()
            elif parsing_feedback and line:
                feedback_lines.append(line)
        
        feedback = " ".join(feedback_lines).strip()
        
        # Oblicz quality_score (0-1)
        overall_score = scores.get("overall", 50)
        quality_score = overall_score / 100.0
        
        # Dodaj emoji do tonu
        tone_emoji = {
            "pozytywny": "😊",
            "neutralny": "🤔",
            "krytyczny": "⚠️"
        }.get(tone, "🤔")
        
        feedback_formatted = f"{tone_emoji} {feedback}" if feedback else f"{tone_emoji} Rozwiązanie wymaga dopracowania."
        
        return (quality_score, feedback_formatted, scores)
        
    except Exception as e:
        # Error handling - fallback do basic score
        basic_score = min(1.0, len(solution.strip()) / 200)
        return (
            basic_score,
            f"❌ Błąd AI: {str(e)[:100]} - użyto oceny podstawowej.",
            {"length": int(basic_score * 100), "relevance": 0, "actionability": 0, "business_impact": 0, "creativity": 0}
        )
