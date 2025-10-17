"""
Generator raportów rozwojowych użytkownika z analizą AI
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Optional
import json

def generate_weekly_report_ai(username: str, activity_summary: Dict, login_pattern: Dict, lesson_stats: Dict, quiz_stats: Optional[Dict] = None) -> Dict:
    """
    Generuje tygodniowy raport rozwojowy używając AI
    """
    try:
        api_key = st.secrets.get("API_KEYS", {}).get("gemini")
        if not api_key:
            return generate_fallback_report(username, activity_summary, login_pattern, lesson_stats, quiz_stats)
        
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        try:
            model = genai.GenerativeModel(
                "gemini-2.0-flash-exp",
                generation_config=genai.GenerationConfig(temperature=0.7)
            )
        except:
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config=genai.GenerationConfig(temperature=0.7)
            )
        
        # Przygotuj dane dla AI
        user_profile = activity_summary.get('user_profile', {})
        
        # Dodaj dane o quizach do promptu
        quiz_section = ""
        if quiz_stats and quiz_stats.get('total_quizzes', 0) > 0:
            quiz_section = f"""
WYNIKI QUIZÓW (OSTATNIE 30 DNI):
- Ukończone quizy: {quiz_stats.get('total_quizzes', 0)}
- Średni wynik: {quiz_stats.get('avg_score', 0)}%
- Wskaźnik zdawalności: {quiz_stats.get('pass_rate', 0)}%
- Wyniki 100%: {quiz_stats.get('perfect_scores', 0)}
- Trend: {quiz_stats.get('improvement_trend', 'brak danych')}
- Najwyższy wynik: {quiz_stats.get('highest_score', 0)}%
- Najniższy wynik: {quiz_stats.get('lowest_score', 0)}%
- Słabe obszary: {len(quiz_stats.get('weak_areas', []))} quizów poniżej 70%
"""
        
        prompt = f"""Jesteś ekspertem od rozwoju osobistego i analizy danych uczenia się.

DANE UŻYTKOWNIKA ({username}) - OSTATNIE 7 DNI:

AKTYWNOŚĆ:
- Dni z logowaniem: {activity_summary.get('unique_login_days', 0)}/7
- Lekcje rozpoczęte: {activity_summary.get('lessons', {}).get('started', 0)}
- Lekcje ukończone: {activity_summary.get('lessons', {}).get('completed', 0)}
- Sesje ćwiczeń AI: {activity_summary.get('ai_exercises', {}).get('sessions', 0)}
- Przeczytane inspiracje: {activity_summary.get('inspirations_read', 0)}
- Użyte narzędzia: {', '.join(activity_summary.get('tools_used', {}).keys()) or 'Brak'}

WZORZEC LOGOWAŃ:
- Najaktywniejszy dzień: {login_pattern.get('most_active_day_of_week', 'Brak danych')}
- Najaktywniejsza godzina: {login_pattern.get('most_active_hour', 'Brak danych')}
- Aktywność: {login_pattern.get('activity_rate', 0)}% dni

LEKCJE (OGÓŁEM):
- Ukończone: {lesson_stats.get('completed', 0)}/{lesson_stats.get('total_available', 0)}
- W trakcie: {lesson_stats.get('in_progress', 0)}
- Porzucone: {lesson_stats.get('abandoned', 0)}
{quiz_section}
PROFIL:
- Level: {user_profile.get('level', 1)}, XP: {user_profile.get('xp', 0)}
- Test Kolba: {user_profile.get('kolb_test') or 'Nie wykonany'}
- Test Neurolidera: {user_profile.get('neuroleader_test') or 'Nie wykonany'}

ZADANIE:
Wygeneruj **spersonalizowany raport tygodniowy** w formacie JSON:

{{
    "summary_headline": "Krótki, motywujący nagłówek (max 10 słów)",
    "engagement_score": 1-10 (ocena zaangażowania),
    "engagement_trend": "rosnący|stabilny|spadający",
    "strengths": [
        "Mocna strona 1 (konkret z danych)",
        "Mocna strona 2",
        "Mocna strona 3"
    ],
    "concerns": [
        "Obszar do poprawy 1 (konkret z danych)",
        "Obszar do poprawy 2"
    ],
    "insights": [
        "Wzorzec/obserwacja 1",
        "Wzorzec/obserwacja 2"
    ],
    "recommendations": [
        {{
            "priority": "wysoki|średni|niski",
            "action": "Konkretna akcja do wykonania",
            "why": "Uzasadnienie (1 zdanie)",
            "estimated_time": "X minut"
        }},
        {{...}},
        {{...}}
    ],
    "motivational_message": "Osobista wiadomość motywacyjna (2-3 zdania)"
}}

WYTYCZNE:
- Bądź **konkretny** - używaj liczb z danych
- Uwzględnij wyniki quizów w analizie (jeśli dostępne)
- Jeśli quizy słabe - zasugeruj powtórkę materiału
- Jeśli trend poprawy - doceń i zachęć do kontynuacji
- Bądź **motywujący** ale **realistyczny**
- Jeśli aktywność niska → skupij się na małych krokach
- Jeśli aktywność wysoka → doceń i zasugeruj wyzwania
- Uwzględnij profil Kolba/Neuroleadera jeśli dostępny
- Rekomendacje: 3-5 sztuk, od najważniejszej

TYLKO JSON:"""

        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Wyczyść JSON
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        report = json.loads(result_text)
        
        # Dodaj metadata
        report['generated_at'] = datetime.now().isoformat()
        report['period_start'] = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        report['period_end'] = datetime.now().strftime('%Y-%m-%d')
        report['report_type'] = 'weekly'
        report['username'] = username
        
        return report
        
    except Exception as e:
        st.error(f"Błąd generowania raportu AI: {e}")
        return generate_fallback_report(username, activity_summary, login_pattern, lesson_stats, quiz_stats)

def generate_fallback_report(username: str, activity_summary: Dict, login_pattern: Dict, lesson_stats: Dict, quiz_stats: Optional[Dict] = None) -> Dict:
    """
    Prosty raport gdy AI nie działa
    """
    engagement_score = calculate_engagement_score(activity_summary, login_pattern, quiz_stats)
    
    strengths = [
        f"Zalogowałeś się {activity_summary.get('unique_login_days', 0)} razy w tym tygodniu",
        f"Ukończone {activity_summary.get('lessons', {}).get('completed', 0)} lekcje"
    ]
    
    # Dodaj informacje o quizach jeśli dostępne
    if quiz_stats and quiz_stats.get('total_quizzes', 0) > 0:
        avg_score = quiz_stats.get('avg_score', 0)
        if avg_score >= 80:
            strengths.append(f"Świetne wyniki w quizach - średnia {avg_score}%!")
        elif avg_score >= 70:
            strengths.append(f"Solidne wyniki w quizach - średnia {avg_score}%")
    
    concerns = []
    if quiz_stats and quiz_stats.get('total_quizzes', 0) > 0:
        avg_score = quiz_stats.get('avg_score', 0)
        if avg_score < 70:
            concerns.append(f"Średnia w quizach {avg_score}% - warto powtórzyć materiał")
        if quiz_stats.get('weak_areas', []):
            concerns.append(f"Wykryto {len(quiz_stats.get('weak_areas', []))} słabe obszary w quizach")
    
    if not concerns:
        concerns = [
            "Zbyt mało danych aby określić obszary do poprawy",
            "Spróbuj być bardziej aktywny w kolejnym tygodniu"
        ]
    
    return {
        'generated_at': datetime.now().isoformat(),
        'period_start': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
        'period_end': datetime.now().strftime('%Y-%m-%d'),
        'report_type': 'weekly',
        'username': username,
        'summary_headline': f"Twój tydzień w BVA - {engagement_score}/10 zaangażowania",
        'engagement_score': engagement_score,
        'engagement_trend': 'stabilny',
        'strengths': strengths,
        'concerns': concerns,
        'insights': [
            "System jeszcze zbiera dane o Twoich wzorcach uczenia się",
            "Kontynuuj regularne logowanie aby otrzymać lepsze insighty"
        ],
        'recommendations': [
            {
                'priority': 'wysoki',
                'action': 'Zaloguj się codziennie przez następne 7 dni',
                'why': 'Regularność jest kluczem do postępu',
                'estimated_time': '15 minut dziennie'
            },
            {
                'priority': 'średni',
                'action': 'Ukończ jedną lekcję w tym tygodniu',
                'why': 'Małe kroki prowadzą do dużych zmian',
                'estimated_time': '30 minut'
            }
        ],
        'motivational_message': 'Każdy dzień to nowa szansa na rozwój. Kontynuuj swoją przygodę z BVA!'
    }

def calculate_engagement_score(activity_summary: Dict, login_pattern: Dict, quiz_stats: Optional[Dict] = None) -> int:
    """
    Oblicza score zaangażowania (1-10) na podstawie aktywności
    """
    score = 0
    
    # Logowania (max 3 punkty)
    login_days = activity_summary.get('unique_login_days', 0)
    if login_days >= 6:
        score += 3
    elif login_days >= 4:
        score += 2
    elif login_days >= 2:
        score += 1
    
    # Lekcje (max 2 punkty)
    lessons_completed = activity_summary.get('lessons', {}).get('completed', 0)
    if lessons_completed >= 3:
        score += 2
    elif lessons_completed >= 1:
        score += 1
    
    # Quizy (max 2 punkty) - NOWE
    if quiz_stats and quiz_stats.get('total_quizzes', 0) > 0:
        avg_score = quiz_stats.get('avg_score', 0)
        if avg_score >= 80:
            score += 2
        elif avg_score >= 70:
            score += 1
    
    # Różnorodność aktywności (max 2 punkty)
    ai_exercises = activity_summary.get('ai_exercises', {}).get('sessions', 0)
    tools_used = len(activity_summary.get('tools_used', {}))
    inspirations = activity_summary.get('inspirations_read', 0)
    
    diverse_score = min(ai_exercises, 1) + min(tools_used, 1) + min(inspirations, 1)
    score += min(diverse_score, 2)
    
    # Regularność (max 1 punkt)
    activity_rate = login_pattern.get('activity_rate', 0)
    if activity_rate >= 80:
        score += 1
    
    return max(1, min(score, 10))  # Ograniczenie 1-10

def save_report_to_user_profile(username: str, report: Dict) -> bool:
    """
    Zapisuje raport do profilu użytkownika
    """
    from data.users import load_user_data, save_user_data
    
    users_data = load_user_data()
    if username not in users_data:
        return False
    
    # Inicjalizuj reports jeśli nie istnieje
    if 'reports' not in users_data[username]:
        users_data[username]['reports'] = []
    
    users_data[username]['reports'].append(report)
    
    # Zachowaj tylko ostatnie 12 raportów (3 miesiące tygodniowych)
    if len(users_data[username]['reports']) > 12:
        users_data[username]['reports'] = users_data[username]['reports'][-12:]
    
    save_user_data(users_data)
    return True

def get_user_reports(username: str, limit: int = 10) -> list:
    """
    Pobiera historyczne raporty użytkownika
    """
    from data.users import load_user_data
    
    users_data = load_user_data()
    if username not in users_data:
        return []
    
    reports = users_data[username].get('reports', [])
    return sorted(reports, key=lambda x: x.get('generated_at', ''), reverse=True)[:limit]

def should_generate_auto_report(username: str) -> bool:
    """
    Sprawdza czy powinien zostać wygenerowany automatyczny raport tygodniowy
    """
    reports = get_user_reports(username, limit=1)
    
    if not reports:
        return True  # Pierwszy raport
    
    last_report_date = datetime.fromisoformat(reports[0].get('generated_at', ''))
    days_since_last = (datetime.now() - last_report_date).days
    
    return days_since_last >= 7  # Raport co 7 dni
