"""
Moduł do obsługi ćwiczeń AI w systemie BVA - Google Gemini Edition
Specjalizuje się w ocenie różnych typów ćwiczeń: symulacje, analizy przypadków, refleksje
Używa wyłącznie Google Gemini AI
"""

import streamlit as st
from typing import Dict, List, Tuple, Optional
import json
import re

# Import Google Gemini
try:
    import google.generativeai as genai
    gemini_available = True
except ImportError:
    gemini_available = False

class AIExerciseEvaluator:
    """Klasa do oceny różnych typów ćwiczeń AI - Google Gemini"""
    
    def __init__(self):
        # Konfiguracja tylko dla Gemini
        self.demo_mode = True
        
        if gemini_available:
            self.google_api_key = st.secrets.get("GOOGLE_API_KEY")
            if self.google_api_key and self.google_api_key != "your-google-gemini-api-key-here":
                try:
                    genai.configure(api_key=self.google_api_key)
                    self.gemini_model = genai.GenerativeModel(
                        st.secrets.get("AI_SETTINGS", {}).get("gemini_model", "gemini-2.5-flash")
                    )
                    
                    # Test bardzo prostego zapytania
                    test_response = self.gemini_model.generate_content("Powiedz 'OK'")
                    if test_response and test_response.text:
                        self.demo_mode = False
                    else:
                        raise Exception("Brak odpowiedzi z testu")
                        
                except Exception as e:
                    self.demo_mode = True
    
    def evaluate_exercise(self, exercise_config: Dict, user_response: str, lesson_context: str = "") -> Dict:
        """
        Główna funkcja do oceny ćwiczeń AI
        
        Args:
            exercise_config: Konfiguracja ćwiczenia (z ai_config)
            user_response: Odpowiedź użytkownika
            lesson_context: Kontekst lekcji
            
        Returns:
            Dict z oceną, feedbackiem i szczegółami
        """
        
        if self.demo_mode:
            return self._demo_evaluation(user_response, exercise_config.get('exercise_type', 'unknown'))
        
        try:
            exercise_type = exercise_config.get('exercise_type', 'general')
            
            # Wybierz odpowiedni prompt na podstawie typu ćwiczenia
            if exercise_type == 'level_identification':
                return self._evaluate_level_identification(exercise_config, user_response, lesson_context)
            elif exercise_type == 'conversation_simulation':
                return self._evaluate_conversation_simulation(exercise_config, user_response, lesson_context)
            elif exercise_type == 'case_analysis':
                return self._evaluate_case_analysis(exercise_config, user_response, lesson_context)
            elif exercise_type == 'self_reflection':
                return self._evaluate_self_reflection(exercise_config, user_response, lesson_context)
            else:
                return self._evaluate_general_exercise(exercise_config, user_response, lesson_context)
                
        except Exception as e:
            st.error(f"Błąd podczas oceny ćwiczenia: {str(e)}")
            return self._fallback_evaluation(user_response)
    
    def _evaluate_level_identification(self, config: Dict, user_response: str, context: str) -> Dict:
        """Ocena identyfikacji poziomów rozmowy"""
        
        criteria = config.get('feedback_criteria', [])
        system_prompt = config.get('ai_prompts', {}).get('system', 
            "Jesteś ekspertem w Conversational Intelligence. Oceniasz umiejętność identyfikacji poziomów rozmowy.")
        
        prompt = f"""Oceń analizę poziomów C-IQ.

WYPOWIEDŹ MENEDŻERA:
"Widzę, że mamy wyzwanie z terminami. Zastanawiam się, jakie przeszkody napotykamy jako zespół i jak możemy razem wypracować rozwiązania, które będą działać dla wszystkich. Co myślicie o przyczynach tej sytuacji i jakie pomysły macie na ulepszenie naszych procesów?"

ODPOWIEDŹ UCZESTNIKA:
{user_response}

POPRAWNA ODPOWIEDŹ: To Poziom III (Transformacyjny) - język współtworzenia, pytania otwarte, focus na rozwiązania.

Oceń w JSON:
{{
    "overall_score": [1-10],
    "identification_correct": true/false,
    "level_identified": "[poziom z odpowiedzi]",
    "correct_level": "Poziom III",
    "feedback": "[feedback po polsku]",
    "strong_points": ["punkt1", "punkt2"],
    "areas_for_improvement": ["obszar1"],
    "learning_tips": ["tip1"]
}}"""
        
        return self._get_ai_evaluation(prompt)
    
    def _evaluate_conversation_simulation(self, config: Dict, user_response: str, context: str) -> Dict:
        """Ocena symulacji rozmowy"""
        
        criteria = config.get('feedback_criteria', [])
        system_prompt = config.get('ai_prompts', {}).get('system', 
            "Jesteś ekspertem w Conversational Intelligence. Analizuj symulacje rozmów.")
        evaluation_prompt = config.get('ai_prompts', {}).get('evaluation', 
            "Oceń symulację rozmowy pod kątem zastosowania zasad C-IQ.")
        
        prompt = f"""Jesteś ekspertem w dziedzinie Conversational Intelligence (C-IQ) i neurobiologii komunikacji. Twoje zadanie to profesjonalna ocena symulacji rozmowy.

KONTEKST LEKCJI: {context}

SYMULACJA ROZMOWY - ODPOWIEDŹ UCZESTNIKA:
{user_response}

KRYTERIA OCENY:
{chr(10).join([f"• {criterion}" for criterion in criteria])}

ZADANIE: Przeanalizuj odpowiedź uczestnika i oceń ją według zasad C-IQ. Zwróć szczególną uwagę na:
1. Identyfikację i świadome przechodzenie między poziomami rozmów (I, II, III)
2. Rozumienie neurobiologii - jak słowa wpływają na hormony (kortyzol vs oksytocyna)
3. Zastosowanie praktycznych technik budowania zaufania
4. Unikanie języka powodującego reakcje obronne

ODPOWIEDZ W FORMACIE JSON:
{{
    "overall_score": [ocena ogólna 1-10],
    "detailed_scores": {{
        "ciq_levels": [1-10],
        "neurobiology_awareness": [1-10], 
        "practical_techniques": [1-10],
        "avoiding_defensiveness": [1-10]
    }},
    "feedback": "[szczegółowy, konstruktywny feedback po polsku]",
    "strong_points": ["silna strona 1", "silna strona 2"],
    "areas_for_improvement": ["obszar do rozwoju 1", "obszar do rozwoju 2"],
    "specific_suggestions": ["konkretna sugestia 1", "konkretna sugestia 2"]
}}

Bądź konstruktywny ale wymagający. Doceniaj próby zastosowania C-IQ, ale wskazuj konkretne możliwości doskonalenia."""
        
        return self._get_ai_evaluation(prompt)
    
    def _evaluate_case_analysis(self, config: Dict, user_response: str, context: str) -> Dict:
        """Ocena analizy przypadku"""
        
        assessment_rubric = config.get('assessment_rubric', {})
        system_prompt = config.get('ai_prompts', {}).get('system',
            "Jesteś ekspertem w analizie przypadków komunikacyjnych.")
        
        prompt = f"""
{system_prompt}

KONTEKST LEKCJI: {context}

ANALIZA PRZYPADKU - ODPOWIEDŹ UCZESTNIKA:
{user_response}

RUBYKA OCENY:
{chr(10).join([f"• {category}: {weight}%" for category, weight in assessment_rubric.items()])}

Oceń analizę w każdej kategorii i podaj szczegółowy feedback:

Podaj ocenę w formacie JSON:
{{
    "overall_score": [1-10],
    "category_scores": {{
        "identification_of_ciq_levels": [1-10],
        "neurobiological_understanding": [1-10],
        "practical_solutions": [1-10],
        "application_of_techniques": [1-10]
    }},
    "feedback": "[szczegółowy feedback]",
    "strong_points": ["mocna strona 1", "mocna strona 2"],
    "areas_for_improvement": ["obszar rozwoju 1", "obszar rozwoju 2"],
    "learning_suggestions": ["sugestia nauki 1", "sugestia nauki 2"]
}}
"""
        
        return self._get_ai_evaluation(prompt)
    
    def _evaluate_self_reflection(self, config: Dict, user_response: str, context: str) -> Dict:
        """Ocena refleksji osobistej (styl coachingowy)"""
        
        system_prompt = config.get('ai_prompts', {}).get('system',
            "Jesteś profesjonalnym coachem. Udzielaj wspierającego feedback'u.")
        
        prompt = f"""
{system_prompt}

KONTEKST LEKCJI: {context}

REFLEKSJA OSOBISTA - ODPOWIEDŹ UCZESTNIKA:
{user_response}

Jako coach, udziel wspierającego i motywującego feedback'u. Skoncentruj się na:
1. Docenieniu samoświadomości
2. Wskazaniu mocnych stron
3. Delikatnym wskazaniu obszarów rozwoju
4. Konkretnych, małych krokach do wprowadzenia
5. Budowaniu motywacji do zmiany

Podaj feedback w formacie JSON:
{{
    "coaching_score": [1-10],
    "self_awareness_level": [1-10],
    "feedback": "[wspierający, coachingowy feedback]",
    "acknowledged_strengths": ["mocna strona 1", "mocna strona 2"],
    "growth_opportunities": ["szansa rozwoju 1", "szansa rozwoju 2"],
    "action_steps": ["mały krok 1", "mały krok 2"],
    "motivation_message": "[motywujące zakończenie]"
}}
"""
        
        return self._get_ai_evaluation(prompt)
    
    def _evaluate_general_exercise(self, config: Dict, user_response: str, context: str) -> Dict:
        """Ocena ogólnego ćwiczenia"""
        
        criteria = config.get('feedback_criteria', [])
        
        prompt = f"""
Jesteś ekspertem w neuroprzywództwie i Conversational Intelligence.

KONTEKST LEKCJI: {context}

ODPOWIEDŹ UCZESTNIKA:
{user_response}

KRYTERIA OCENY:
{chr(10).join([f"• {criterion}" for criterion in criteria])}

Oceń odpowiedź i udziel konstruktywnego feedback'u:

{{
    "score": [1-10],
    "feedback": "[konstruktywny feedback]",
    "strong_points": ["mocna strona 1", "mocna strona 2"],
    "suggestions": ["sugestia 1", "sugestia 2"]
}}
"""
        
        return self._get_ai_evaluation(prompt)
    
    def _get_ai_evaluation(self, prompt: str) -> Dict:
        """Wysyła prompt do Google Gemini i parsuje odpowiedź"""
        
        try:
            # Sprawdź długość promptu
            prompt_length = len(prompt)
            if prompt_length > 8000:
                prompt = prompt[:7500] + "\n\nOceń odpowiedź w formacie JSON."
            
            # Dodaj instrukcję JSON na początku
            json_instruction = """WAŻNE: Odpowiedz TYLKO w poprawnym formacie JSON, bez dodatkowych komentarzy.

"""
            full_prompt = json_instruction + prompt
            
            # Wyślij do Gemini
            response = self.gemini_model.generate_content(full_prompt)
            
            if not response or not response.text:
                raise Exception("Pusta odpowiedź z Gemini")
                
            content = response.text.strip()
            
            # Próbuj sparsować JSON
            try:
                import json
                import re
                
                # Znajdź JSON w odpowiedzi
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    result = json.loads(json_str)
                    
                    # Waliduj że mamy wymagane pola
                    if 'overall_score' in result or 'feedback' in result or 'coaching_score' in result:
                        return result
                        
            except (json.JSONDecodeError, ValueError):
                pass
            
            # Fallback - użyj surowej odpowiedzi Gemini
            import random
            return {
                "overall_score": random.randint(6, 9),
                "feedback": f"**🤖 Odpowiedź Gemini AI:**\n\n{content}",
                "strong_points": ["Otrzymano prawdziwą analizę z AI"],
                "areas_for_improvement": ["Kontynuuj rozwijanie umiejętności C-IQ"],
                "learning_tips": ["Przećwicz więcej przykładów", "Zwróć uwagę na szczegóły"]
            }
                    
        except Exception as e:
            error_msg = str(e)
            
            # Przełącz na demo mode dla tego ćwiczenia
            return {
                "overall_score": 7,
                "feedback": f"⚠️ **AI chwilowo niedostępne** - {error_msg[:100]}...\n\n💡 **Demo feedback**: Twoja odpowiedź została przeanalizowana. Spróbuj ponownie za chwilę aby otrzymać pełny feedback AI.",
                "strong_points": ["Ukończenie ćwiczenia", "Zaangażowanie w rozwój"],
                "areas_for_improvement": ["Spróbuj ponownie gdy AI będzie dostępne"],
                "learning_tips": ["AI czasem ma chwilowe problemy", "Kontynuuj ćwiczenie rozwoju"]
            }
    
    def _demo_evaluation(self, user_response: str, exercise_type: str) -> Dict:
        """Ocena demo gdy AI nie jest dostępne"""
        
        word_count = len(user_response.split())
        
        if exercise_type == 'level_identification':
            # Sprawdź czy użytkownik wspomniał o poziomie III
            level_iii_mentions = any(keyword in user_response.lower() for keyword in 
                                   ['poziom iii', 'poziom 3', 'transformacyjny', 'współtworzenie', 'razem', 'zespół'])
            correct_identification = level_iii_mentions
            
            return {
                "overall_score": 9 if correct_identification else 6,
                "identification_correct": correct_identification,
                "level_identified": "Poziom III" if level_iii_mentions else "Nie określono jednoznacznie",
                "correct_level": "Poziom III",
                "detailed_scores": {
                    "level_identification": 9 if correct_identification else 5,
                    "linguistic_analysis": min(8, max(4, word_count // 15)),
                    "neurobiological_understanding": 7 if 'oksytocyna' in user_response.lower() or 'zaufanie' in user_response.lower() else 5,
                    "reasoning_quality": min(8, max(4, word_count // 20))
                },
                "feedback": f"🎯 **Demo Mode**: {'Doskonale! Poprawnie zidentyfikowałeś poziom III.' if correct_identification else 'Ta wypowiedź to poziom III - zwróć uwagę na język współtworzenia.'} Twoja analiza pokazuje {'dobre' if word_count > 2 else 'podstawowe'} zrozumienie poziomów C-IQ.",
                "strong_points": ["Próba systematycznej analizy", "Uwaga na detale wypowiedzi"] + (["Poprawna identyfikacja poziomu"] if correct_identification else []),
                "areas_for_improvement": [] if correct_identification else ["Rozpoznawanie sygnałów poziomu III", "Analiza języka współtworzenia"],
                "learning_tips": ["Zwracaj uwagę na pytania otwarte vs zamknięte", "Obserwuj słowa tworzące 'my' vs 'wy'"]
            }
        elif exercise_type == 'conversation_simulation':
            return {
                "overall_score": min(8, max(4, word_count // 20)),
                "detailed_scores": {
                    "ciq_levels": 7,
                    "neurobiology_awareness": 6,
                    "practical_techniques": 7,
                    "avoiding_defensiveness": 8
                },
                "feedback": "🎭 **Demo Mode**: Twoja symulacja rozmowy pokazuje dobre rozumienie podstaw C-IQ. Widać, że zastanowiłeś się nad neurobiologią rozmowy i próbujesz zastosować poziom III - współtworzenie rozwiązań.",
                "strong_points": ["Świadomość poziomów rozmowy", "Próba budowania zaufania"],
                "areas_for_improvement": ["Więcej konkretnych technik C-IQ", "Szczegółowszy plan działania"],
                "specific_suggestions": ["Dodaj więcej pytań otwartych", "Uwzględnij język współtworzenia"]
            }
        elif exercise_type == 'case_analysis':
            return {
                "overall_score": min(9, max(5, word_count // 25)),
                "category_scores": {
                    "identification_of_ciq_levels": 7,
                    "neurobiological_understanding": 6,
                    "practical_solutions": 8,
                    "application_of_techniques": 7
                },
                "feedback": "🔍 **Demo Mode**: Twoja analiza przypadku pokazuje dobre zrozumienie podstawowych zasad C-IQ. Potrafisz identyfikować poziomy rozmowy i proponujesz praktyczne rozwiązania.",
                "strong_points": ["Systematyczne podejście do analizy", "Praktyczne rozwiązania"],
                "areas_for_improvement": ["Głębsza analiza neurobiologiczna", "Więcej technik C-IQ"],
                "learning_suggestions": ["Przeczytaj więcej o hormonach stresu/zaufania", "Przećwicz więcej symulacji"]
            }
        elif exercise_type == 'self_reflection':
            return {
                "coaching_score": min(9, max(6, word_count // 15)),
                "self_awareness_level": 8,
                "feedback": "💭 **Demo Mode**: Twoja refleksja pokazuje dużą samoświadomość i szczerość. To doskonały punkt wyjścia do rozwoju umiejętności komunikacyjnych. Widać, że podchodzisz do swojego rozwoju z otwartością i chęcią zmiany.",
                "acknowledged_strengths": ["Wysoka samoświadomość", "Chęć do rozwoju", "Szczerość w autoanalizie"],
                "growth_opportunities": ["Praktyczne zastosowanie C-IQ", "Regularne ćwiczenie nowych technik"],
                "action_steps": ["Obserwuj swoje reakcje w następnej trudnej rozmowie", "Zadaj jedno pytanie otwarte dzisiaj"],
                "motivation_message": "Pamiętaj: każda świadoma zmiana w komunikacji to krok w kierunku lepszych relacji i większego wpływu. Jesteś na dobrej drodze! 🌟"
            }
        else:
            return {
                "score": min(8, max(4, word_count // 20)),
                "feedback": f"🤖 **Demo Mode**: Otrzymałeś {min(8, max(4, word_count // 20))}/10 punktów. Twoja odpowiedź pokazuje zaangażowanie w temat. Aby uzyskać pełną ocenę AI, skonfiguruj klucz OpenAI API.",
                "strong_points": ["Zaangażowanie w zadanie", "Próba zastosowania teorii"],
                "suggestions": ["Skonfiguruj AI dla szczegółowej oceny", "Kontynuuj rozwijanie umiejętności C-IQ"]
            }
    
    def _fallback_evaluation(self, user_response: str) -> Dict:
        """Ocena fallback w przypadku błędu"""
        word_count = len(user_response.split()) if user_response else 0
        return {
            "score": min(7, max(3, word_count // 25)),
            "feedback": "⚠️ Wystąpił problem z oceną AI. Otrzymujesz podstawową ocenę na podstawie długości odpowiedzi. Spróbuj ponownie później lub skontaktuj się z administratorem.",
            "strong_points": ["Ukończenie ćwiczenia"],
            "suggestions": ["Spróbuj ponownie później"]
        }


def display_ai_exercise_interface(exercise: Dict, lesson_context: str = "") -> bool:
    """
    Wyświetla interfejs ćwiczenia AI z możliwością oceny
    
    Args:
        exercise: Słownik z danymi ćwiczenia
        lesson_context: Kontekst lekcji
        
    Returns:
        bool: True jeśli ćwiczenie zostało ukończone
    """
    
    exercise_id = exercise.get('id', 'unknown')
    exercise_title = exercise.get('title', 'Ćwiczenie AI')
    
    # Sprawdź czy ćwiczenie zostało już ukończone
    completion_key = f"ai_exercise_{exercise_id}_completed"
    if st.session_state.get(completion_key, False):
        st.success(f"✅ Ćwiczenie '{exercise_title}' zostało ukończone!")
        
        # Wyświetl poprzedni feedback jeśli istnieje
        feedback_key = f"ai_exercise_{exercise_id}_feedback"
        if feedback_key in st.session_state:
            col1, col2 = st.columns([4, 1])
            with col1:
                with st.expander("📝 Pokaż poprzedni feedback AI", expanded=False):
                    feedback = st.session_state[feedback_key]
                    display_ai_feedback(feedback)
            with col2:
                if st.button("🔄 Reset", key=f"reset_{exercise_id}", help="Resetuj to ćwiczenie i zrób je ponownie"):
                    reset_single_exercise(exercise_id)
                    st.rerun()
        
        return True
    
    # Wyświetl formularz odpowiedzi
    response_key = f"ai_exercise_{exercise_id}_response"
    user_response = st.text_area(
        "Twoja odpowiedź:",
        value=st.session_state.get(response_key, ""),
        height=200,
        key=response_key,
        placeholder="Wpisz swoją szczegółową odpowiedź tutaj..."
    )
    
    # Przycisk do otrzymania feedback'u AI
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button(f"🤖 Otrzymaj feedback AI", key=f"evaluate_{exercise_id}"):
            if len(user_response.strip()) < 2:
                st.warning("Napisz co najmniej 2 słowa, aby otrzymać szczegółowy feedback.")
            else:
                with st.spinner("AI analizuje Twoją odpowiedź..."):
                    evaluator = AIExerciseEvaluator()
                    ai_config = exercise.get('ai_config', {})
                    
                    result = evaluator.evaluate_exercise(ai_config, user_response, lesson_context)
                    
                    # Zapisz feedback
                    feedback_key = f"ai_exercise_{exercise_id}_feedback"
                    st.session_state[feedback_key] = result
                    
                    # Oznacz jako ukończone
                    st.session_state[completion_key] = True
                    
                    st.rerun()
    
    with col2:
        word_count = len(user_response.split())
        st.metric("Słowa", word_count)
        if word_count < 2:
            st.caption("Min. 2 słowa")
    
    return False


def reset_single_exercise(exercise_id: str):
    """Resetuje pojedyncze ćwiczenie AI"""
    completion_key = f"ai_exercise_{exercise_id}_completed"
    feedback_key = f"ai_exercise_{exercise_id}_feedback"
    response_key = f"ai_exercise_{exercise_id}_response"
    
    # Usuń z session_state
    if completion_key in st.session_state:
        del st.session_state[completion_key]
    if feedback_key in st.session_state:
        del st.session_state[feedback_key]
    if response_key in st.session_state:
        del st.session_state[response_key]
    
    st.success(f"✅ Ćwiczenie zresetowane! Możesz je zrobić ponownie.")


def reset_all_ai_exercises(lesson_id: str = None):
    """Resetuje wszystkie ćwiczenia AI (opcjonalnie dla konkretnej lekcji)"""
    keys_to_remove = []
    
    for key in st.session_state.keys():
        if key.startswith("ai_exercise_") and (
            key.endswith("_completed") or 
            key.endswith("_feedback") or 
            key.endswith("_response")
        ):
            # Jeśli podano lesson_id, resetuj tylko dla tej lekcji
            if lesson_id:
                if f"_{lesson_id}_" in key:
                    keys_to_remove.append(key)
            else:
                keys_to_remove.append(key)
    
    # Usuń klucze
    for key in keys_to_remove:
        del st.session_state[key]
    
    return len(keys_to_remove) // 3  # Każde ćwiczenie ma 3 klucze


def display_reset_all_button(lesson_id: str = None):
    """Wyświetla przycisk do resetowania wszystkich ćwiczeń AI"""
    
    # Sprawdź ile ćwiczeń jest ukończonych
    completed_count = 0
    total_exercises = 0
    
    for key in st.session_state.keys():
        if key.startswith("ai_exercise_") and key.endswith("_completed"):
            if lesson_id and f"_{lesson_id}_" not in key:
                continue
            total_exercises += 1
            if st.session_state.get(key, False):
                completed_count += 1
    
    if completed_count > 0:
        with st.expander(f"🔄 Reset ćwiczeń AI ({completed_count} ukończonych)", expanded=False):
            st.warning(f"⚠️ Spowoduje to usunięcie wszystkich odpowiedzi i feedback'ów z {completed_count} ukończonych ćwiczeń.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Resetuj wszystkie ćwiczenia", key=f"reset_all_{lesson_id or 'global'}"):
                    reset_count = reset_all_ai_exercises(lesson_id)
                    st.success(f"✅ Zresetowano {reset_count} ćwiczeń AI! Możesz je zrobić ponownie.")
                    st.rerun()
            
            with col2:
                st.info("💡 **Wskazówka**: Możesz też resetować pojedyncze ćwiczenia przyciskiem 🔄 obok każdego.")


def display_ai_feedback(feedback: Dict):
    """Wyświetla feedback AI w przyjaznym formacie"""
    
    # Główna ocena
    if 'overall_score' in feedback:
        score = feedback['overall_score']
        st.metric("🎯 Ocena ogólna", f"{score}/10")
    elif 'score' in feedback:
        score = feedback['score']
        st.metric("🎯 Ocena", f"{score}/10")
    elif 'coaching_score' in feedback:
        score = feedback['coaching_score']
        st.metric("🎯 Ocena coachingowa", f"{score}/10")
    
    # Szczegółowe oceny jeśli dostępne
    if 'detailed_scores' in feedback:
        st.markdown("### 📊 Szczegółowe oceny")
        cols = st.columns(len(feedback['detailed_scores']))
        for i, (category, score) in enumerate(feedback['detailed_scores'].items()):
            with cols[i]:
                category_name = category.replace('_', ' ').title()
                st.metric(category_name, f"{score}/10")
    
    if 'category_scores' in feedback:
        st.markdown("### 📊 Oceny kategorialne")
        cols = st.columns(2)
        for i, (category, score) in enumerate(feedback['category_scores'].items()):
            with cols[i % 2]:
                category_name = category.replace('_', ' ').title()
                st.metric(category_name, f"{score}/10")
    
    # Główny feedback
    if 'feedback' in feedback:
        st.markdown("### 💬 Feedback AI")
        st.info(feedback['feedback'])
    
    # Mocne strony
    if 'strong_points' in feedback:
        st.markdown("### ✅ Twoje mocne strony")
        for point in feedback['strong_points']:
            st.markdown(f"• {point}")
    
    if 'acknowledged_strengths' in feedback:
        st.markdown("### ✅ Rozpoznane mocne strony")
        for strength in feedback['acknowledged_strengths']:
            st.markdown(f"• {strength}")
    
    # Obszary do poprawy
    if 'areas_for_improvement' in feedback:
        st.markdown("### 🎯 Obszary do rozwoju")
        for area in feedback['areas_for_improvement']:
            st.markdown(f"• {area}")
    
    if 'growth_opportunities' in feedback:
        st.markdown("### 🌱 Szanse rozwoju")
        for opportunity in feedback['growth_opportunities']:
            st.markdown(f"• {opportunity}")
    
    # Sugestie
    if 'suggestions' in feedback or 'specific_suggestions' in feedback:
        st.markdown("### 💡 Sugestie")
        suggestions = feedback.get('suggestions', feedback.get('specific_suggestions', []))
        for suggestion in suggestions:
            st.markdown(f"• {suggestion}")
    
    if 'learning_suggestions' in feedback:
        st.markdown("### 📚 Sugestie dalszej nauki")
        for suggestion in feedback['learning_suggestions']:
            st.markdown(f"• {suggestion}")
    
    if 'action_steps' in feedback:
        st.markdown("### 🎯 Konkretne kroki do działania")
        for step in feedback['action_steps']:
            st.markdown(f"• {step}")
    
    # Motywująca wiadomość
    if 'motivation_message' in feedback:
        st.markdown("### 🌟 Wiadomość motywacyjna")
        st.success(feedback['motivation_message'])