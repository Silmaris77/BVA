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
        self.demo_mode = False  # Wymuszenie pełnego trybu dla testów
        
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
                    st.warning(f"Problem z Google Gemini API: {str(e)}")
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
            elif exercise_type == 'generated_case':
                return self._evaluate_generated_case(exercise_config, user_response, lesson_context)
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
    
    def _evaluate_generated_case(self, config: Dict, user_response: str, context: str) -> Dict:
        """Ocena odpowiedzi na wygenerowany case study"""
        
        # Sprawdź czy mamy wygenerowany case w konfiguracji
        if 'generated_case_data' not in config:
            return {
                "overall_score": 5,
                "feedback": "⚠️ Błąd: Brak wygenerowanego case study. Skontaktuj się z administratorem.",
                "case_understanding": 5,
                "solution_quality": 5,
                "c_iq_application": 5,
                "practical_value": 5
            }
        
        case_data = config['generated_case_data']
        
        prompt = f"""
Jesteś ekspertem w Conversational Intelligence i neuroprzywództwie.

WYGENEROWANY CASE STUDY:
Tytuł: {case_data.get('title', 'Case Study')}
Kontekst firmy: {case_data.get('company_context', '')}
Sytuacja: {case_data.get('situation', '')}

ZADANIE DLA UCZESTNIKA:
{case_data.get('task', '')}

ODPOWIEDŹ UCZESTNIKA:
{user_response}

KONTEKST LEKCJI: {context}

WAŻNE: Odpowiedz w ZWYKŁYM TEKŚCIE, NIE w JSON! Użyj formatowania markdown.

Oceń odpowiedź uczestnika według następujących kryteriów (1-10):

**🎯 OCENA OGÓLNA:** [podaj ocenę 1-10]

**📊 SZCZEGÓŁOWE OCENY:**
- **Zrozumienie przypadku:** [1-10] - Czy uczestnik prawidłowo zidentyfikował kluczowe wyzwania?
- **Jakość rozwiązania:** [1-10] - Czy proponowane rozwiązanie jest praktyczne i wykonalne?
- **Zastosowanie C-IQ:** [1-10] - Czy wykorzystał zasady Conversational Intelligence?
- **Wartość praktyczna:** [1-10] - Czy rozwiązanie można wdrożyć w rzeczywistości?

**💬 SZCZEGÓŁOWY FEEDBACK:**
[Napisz konstruktywny, szczegółowy feedback z konkretnymi wskazówkami]

**✅ MOCNE STRONY:**
- [mocny punkt 1]
- [mocny punkt 2]

**🎯 OBSZARY DO ROZWOJU:**
- [obszar poprawy 1]
- [obszar poprawy 2]

**💡 WSKAZÓWKI C-IQ:**
- [wskazówka C-IQ 1]
- [wskazówka C-IQ 2]

**📋 NASTĘPNE KROKI:**
- [następny krok 1]
- [następny krok 2]

**🏆 WZORCOWA ODPOWIEDŹ (10/10):**
[Napisz przykładową wzorcową odpowiedź eksperta C-IQ, która otrzymałaby maksymalną ocenę. Powinna zawierać analizę sytuacji z perspektywy C-IQ, konkretne techniki komunikacyjne, praktyczne kroki i uzasadnienie neurobiologiczne (kortyzol vs oksytocyna)]
"""
        
        return self._get_ai_evaluation_text(prompt)
    
    def _get_ai_evaluation_text(self, prompt: str) -> Dict:
        """Wysyła prompt do Google Gemini i parsuje odpowiedź jako zwykły tekst (nie JSON)"""
        
        try:
            # Sprawdź długość promptu
            prompt_length = len(prompt)
            if prompt_length > 8000:
                prompt = prompt[:7500] + "\n\nOceń odpowiedź w formacie markdown."
            
            # Wyślij do Gemini
            response = self.gemini_model.generate_content(prompt)
            content = response.text if response else ""
            
            if not content or len(content.strip()) < 10:
                return {
                    "overall_score": 5,
                    "feedback": "AI nie zwróciło odpowiedzi. Spróbuj ponownie.",
                    "strong_points": ["Podjęłeś próbę rozwiązania zadania"],
                    "areas_for_improvement": ["Spróbuj ponownie przesłać odpowiedź"],
                    "learning_tips": ["Sprawdź połączenie internetowe", "Spróbuj w innym czasie"]
                }
            
            # Parsuj zwykły tekst - wyciągnij ocenę ogólną
            import re
            overall_score_match = re.search(r'OCENA OGÓLNA.*?(\d+)', content, re.IGNORECASE)
            overall_score = int(overall_score_match.group(1)) if overall_score_match else 7
            
            return {
                "overall_score": overall_score,
                "feedback": content,  # Cały tekst jako feedback
                "strong_points": ["Otrzymano szczegółową analizę z AI"],
                "areas_for_improvement": ["Przeanalizuj feedback AI i zastosuj wskazówki"],
                "learning_tips": ["Kontynuuj rozwijanie umiejętności C-IQ"]
            }
                    
        except Exception as e:
            error_msg = str(e)
            return {
                "overall_score": 5,
                "feedback": f"Wystąpił błąd podczas komunikacji z AI: {error_msg}",
                "strong_points": ["Podjęłeś próbę wykonania zadania"],
                "areas_for_improvement": ["Spróbuj ponownie za chwilę"],
                "learning_tips": ["Sprawdź połączenie internetowe"]
            }
    
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
                
                # Usunię znaczniki markdown jeśli są
                content_clean = content
                if content_clean.startswith("```json"):
                    content_clean = content_clean.replace("```json", "").replace("```", "").strip()
                elif content_clean.startswith("```"):
                    content_clean = content_clean.replace("```", "").strip()
                
                # Próbuj najpierw parsować całą odpowiedź jako JSON
                try:
                    result = json.loads(content_clean)
                    if 'overall_score' in result or 'feedback' in result or 'coaching_score' in result:
                        return result
                except json.JSONDecodeError:
                    pass
                
                # Jeśli nie udało się, znajdź JSON w odpowiedzi
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    result = json.loads(json_str)
                    
                    # Waliduj że mamy wymagane pola
                    if 'overall_score' in result or 'feedback' in result or 'coaching_score' in result:
                        return result
                        
            except (json.JSONDecodeError, ValueError) as json_error:
                # ZAWSZE zastąp content przyjaznym komunikatem gdy JSON się nie parsuje
                content = f"""Przepraszamy, AI napotkało problem techniczny podczas generowania feedback'u. 

**Co się stało:** Odpowiedź zawierała nieprawidłowe znaki lub format.

**Co możesz zrobić:**
• Spróbuj ponownie przesłać swoją odpowiedź  
• Jeśli problem się powtarza, skontaktuj się z administratorem

*Szczegóły techniczne: {str(json_error)[:100]}...*"""
            
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
        elif exercise_type == 'generated_case':
            return {
                "overall_score": min(8, max(5, word_count // 20)),
                "feedback": "🎯 **Demo Mode**: Twoja analiza wygenerowanego case study pokazuje dobre zrozumienie zasad C-IQ. Widzę, że potrafiłeś zidentyfikować kluczowe wyzwania komunikacyjne i zaproponować praktyczne rozwiązania.",
                "case_understanding": min(8, max(6, word_count // 25)),
                "solution_quality": min(9, max(5, word_count // 30)),
                "c_iq_application": min(7, max(5, word_count // 35)),
                "practical_value": min(8, max(6, word_count // 20)),
                "strong_points": ["Analiza sytuacji", "Praktyczne podejście", "Zastosowanie teorii C-IQ"],
                "improvement_areas": ["Głębsza analiza neurobiologiczna", "Więcej konkretnych technik"],
                "c_iq_tips": ["Zwróć uwagę na różnicę między poziomami I, II i III", "Pomyśl o hormonach: kortyzol vs oksytocyna"],
                "next_steps": ["Przetestuj rozwiązania w prawdziwej sytuacji", "Obserwuj reakcje innych na twoje podejście"],
                "exemplary_response": "Analizując tę sytuację przez pryzmat Conversational Intelligence, identyfikuję główne wyzwanie: przekształcenie atmosfery wzajemnych oskarżeń (Poziom I) w konstruktywną naukę zespołową (Poziom III).\n\n**Moja strategia jako Project Manager:**\n\n1. **Przygotowanie neurobiologiczne**: Zacznę od uspokojenia atmosfery, aby obniżyć poziom kortyzolu. Użyję spokojnego tonu głosu i wolniejszego tempa mowy.\n\n2. **Otwarcie retrospektywy**: 'Wszyscy czujemy frustrację po tym projekcie. To naturalne. Naszym wspólnym celem jest wyciągnięcie nauki, która pomoże nam w przyszłości.' - używam języka 'my' zamiast 'wy'.\n\n3. **Przejście na Poziom III**: Zadam pytania otwarte: 'Jakie widzicie systemowe przyczyny tego co się stało?' zamiast szukania winnych.\n\n4. **Budowanie bezpieczeństwa**: Ustanowię zasadę: 'Skupiamy się na procesach i systemach, nie na osobach'.\n\n5. **Współtworzenie rozwiązań**: 'Jak możemy razem zaprojektować lepsze procesy komunikacji między zespołami?'\n\nTa strategia wykorzystuje neurobiologię zaufania do przekształcenia konfliktu w okazję do rozwoju zespołu."
            }
        else:
            return {
                "score": min(8, max(4, word_count // 20)),
                "feedback": f"🤖 **Demo Mode**: Otrzymałeś {min(8, max(4, word_count // 20))}/10 punktów. Twoja odpowiedź pokazuje zaangażowanie w temat. Aby uzyskać pełną ocenę AI, skonfiguruj klucz OpenAI API.",
                "strong_points": ["Zaangażowanie w zadanie", "Próba zastosowania teorii"],
                "suggestions": ["Skonfiguruj AI dla szczegółowej oceny", "Kontynuuj rozwijanie umiejętności C-IQ"]
            }
    
    def generate_case_study(self, lesson_context: str = "", difficulty_level: str = "medium", industry: str = "Ogólny") -> Dict:
        """
        Generuje nowy case study z zadaniem dla użytkownika
        
        Args:
            lesson_context: Kontekst lekcji
            difficulty_level: "easy", "medium", "hard"
            
        Returns:
            Dict z wygenerowanym case study, zadaniem i metadanymi
        """
        
        if self.demo_mode:
            return self._generate_demo_case(difficulty_level)
        
        difficulty_prompts = {
            "easy": "bardzo prosty przypadek wymagający odpowiedzi 2-3 słów lub jednego zdania",
            "medium": "przypadek o średniej złożoności wymagający odpowiedzi 3-5 zdań", 
            "hard": "złożony przypadek wymagający szczegółowej analizy i długiej odpowiedzi"
        }
        
        task_complexity = {
            "easy": "Zadanie powinno być bardzo proste - wystarczy krótka odpowiedź (2-3 słowa lub jedno zdanie). Przykład: 'Jak Anna powinna zacząć rozmowę?' lub 'Jakie pierwsze słowa powinna wypowiedzieć?'",
            "medium": "Zadanie powinno wymagać odpowiedzi 3-5 zdań. Przykład: 'Opisz strategię komunikacyjną' lub 'Zaproponuj scenariusz rozmowy'",
            "hard": "Zadanie powinno wymagać szczegółowej analizy i długiej odpowiedzi. Przykład: 'Opracuj kompleksową strategię komunikacyjną z wieloma etapami'"
        }
        
        industry_context = ""
        if industry != "Ogólny":
            industry_context = f" w branży {industry}"
        
        prompt = f"""
Wygeneruj realny case study z obszaru komunikacji zespołowej i przywództwa{industry_context}.

KONTEKST LEKCJI: {lesson_context}

POZIOM TRUDNOŚCI: {difficulty_prompts.get(difficulty_level, "medium")}

WYMAGANIA CO DO ZADANIA: {task_complexity.get(difficulty_level, "")}

Stwórz {difficulty_prompts.get(difficulty_level, "przypadek o średniej złożoności")} oparty na zasadach Conversational Intelligence, który:

1. **Przedstawia autentyczną sytuację biznesową** z konkretymi postaciami
2. **Zawiera wyzwanie komunikacyjne** wymagające zastosowania C-IQ
3. **Ma jasno określony cel** - co należy osiągnąć
4. **Uwzględnia neurobiologię rozmowy** (poziomy, oksytocyna/kortyzol)

WAŻNE - dostosuj zadanie do poziomu trudności:
- EASY: zadanie musi być bardzo proste, wystarczy odpowiedź 2-3 słów lub jedno zdanie
- MEDIUM: zadanie powinno wymagać odpowiedzi 3-5 zdań
- HARD: zadanie może wymagać szczegółowej analizy

Wygeneruj w formacie JSON:

{{
    "title": "[krótki, opisowy tytuł case study]",
    "company_context": "[2-3 zdania o firmie/dziale]",
    "situation": "[szczegółowy opis sytuacji - 4-6 zdań]",
    "characters": {{
        "main_character": {{
            "name": "[imię]",
            "position": "[stanowisko]",
            "challenge": "[główne wyzwanie tej osoby]"
        }},
        "other_characters": [
            {{
                "name": "[imię]",
                "position": "[stanowisko]", 
                "role_in_conflict": "[rola w sytuacji]"
            }}
        ]
    }},
    "communication_challenge": "[główny problem komunikacyjny]",
    "c_iq_opportunity": "[jakie zasady C-IQ można zastosować]",
    "task": "[konkretne zadanie dla uczestnika - co ma zrobić]",
    "success_criteria": ["kryterium 1", "kryterium 2", "kryterium 3"],
    "difficulty": "{difficulty_level}",
    "estimated_time": "[czas w minutach]"
}}
"""
        
        try:
            result = self._get_case_study_from_ai(prompt)
            # Sprawdź czy otrzymaliśmy poprawny case study
            if result is not None and isinstance(result, dict) and 'title' in result:
                result['generated_at'] = "dynamically_generated"
                result['lesson_context'] = lesson_context
                return result
            else:
                # Jeśli AI nie zwróciło poprawnego case study, użyj demo case
                return self._generate_demo_case(difficulty_level)
        except Exception as e:
            st.error(f"Błąd podczas generowania case study: {str(e)}")
            return self._generate_demo_case(difficulty_level)
    
    def _get_case_study_from_ai(self, prompt: str) -> Dict:
        """Wysyła prompt do Google Gemini i parsuje odpowiedź jako case study"""
        
        try:
            # Sprawdź długość promptu
            prompt_length = len(prompt)
            if prompt_length > 8000:
                prompt = prompt[:7500] + "\n\nWygeneruj case study w formacie JSON."
            
            # Dodaj instrukcję JSON na początku
            json_instruction = """WAŻNE: Odpowiedz TYLKO w poprawnym formacie JSON dla case study, bez dodatkowych komentarzy.

"""
            full_prompt = json_instruction + prompt
            
            # Wyślij do Gemini
            response = self.gemini_model.generate_content(full_prompt)
            
            if not response or not response.text:
                raise Exception("Pusta odpowiedź z Gemini")
                
            content = response.text.strip()
            
            # Usuń markdown formatowanie jeśli jest
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "").strip()
            
            # Próbuj sparsować JSON
            try:
                import json
                import re
                
                # Znajdź JSON w odpowiedzi
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    result = json.loads(json_str)
                    
                    # Waliduj że mamy wymagane pola dla case study
                    required_fields = ['title', 'situation', 'task']
                    if any(field in result for field in required_fields):
                        return result
                        
            except (json.JSONDecodeError, ValueError) as parse_error:
                st.warning(f"JSON parsing error: {str(parse_error)}")
                # Wyświetl surową odpowiedź dla debugowania
                st.info(f"Surowa odpowiedź AI (pierwsze 500 znaków): {content[:500]}...")
            
            # Fallback - jeśli nie można sparsować JSON, zwróć None aby użyć demo case
            st.warning("Nie udało się sparsować JSON case study z AI, używam demo case")
            return None
                    
        except Exception as e:
            st.error(f"Błąd komunikacji z AI: {str(e)}")
            return None

    def _generate_demo_case(self, difficulty_level: str) -> Dict:
        """Generuje demo case study gdy AI nie jest dostępne"""
        
        demo_cases = {
            "easy": {
                "title": "Pierwsze słowa w trudnej rozmowie",
                "company_context": "Małe biuro rachunkowe. Anna musi przekazać współpracownikowi Tomkowi niepopularną informację.",
                "situation": "Anna, kierownik, dowiedziała się że musi poprosić Tomka o zostanie po godzinach. Wie, że Tomek ma dziś ważne plany rodzinne. Stoi przed jego biurkiem i zastanawia się jak zacząć rozmowę.",
                "characters": {
                    "main_character": {
                        "name": "Anna",
                        "position": "Kierownik",
                        "challenge": "Jak zacząć trudną rozmowę"
                    },
                    "other_characters": [
                        {"name": "Tomek", "position": "Księgowy", "role_in_conflict": "Ma ważne plany rodzinne"}
                    ]
                },
                "communication_challenge": "Pierwsze słowa w trudnej rozmowie",
                "c_iq_opportunity": "Zastosowanie empatycznego otwarcia zamiast bezpośredniego polecenia",
                "task": "Jakie pierwsze słowa powinna wypowiedzieć Anna?",
                "success_criteria": ["Empatyczne podejście", "Respekt dla sytuacji Tomka"],
                "difficulty": "easy",
                "estimated_time": "2-3 minuty"
            },
            "medium": {
                "title": "Konflikt między zespołami",
                "company_context": "Średnia firma IT. Zespół programistów i zespół testowy mają konflikt o jakość deliverów.",
                "situation": "Ostatnio programiści oddają kod z wieloma błędami. Testerzy są sfrustrowani, bo muszą znajdować podstawowe problemy zamiast skupić się na zaawansowanych testach. Programiści czują się atakowani i twierdzą, że testerzy są zbyt wymagający. Marcin, project manager, musi przeprowadzić spotkanie mediacyjne.",
                "characters": {
                    "main_character": {
                        "name": "Marcin", 
                        "position": "Project Manager",
                        "challenge": "Mediacja między skonfliktowanymi zespołami"
                    },
                    "other_characters": [
                        {"name": "Zespół Dev", "position": "Programiści", "role_in_conflict": "Czują się atakowani"},
                        {"name": "Zespół QA", "position": "Testerzy", "role_in_conflict": "Frustracja jakością kodu"}
                    ]
                },
                "communication_challenge": "Przeprowadzenie mediacji między zespołami",
                "c_iq_opportunity": "Przejście z wzajemnych oskarżeń na współtworzenie rozwiązań",
                "task": "Opisz strategię Marcina na spotkanie mediacyjne. Jak powinien prowadzić rozmowę aby oba zespoły poczuły się wysłuchane?",
                "success_criteria": ["Wyciszenie oskarżeń", "Znalezienie wspólnych rozwiązań", "Odbudowa współpracy"],
                "difficulty": "medium", 
                "estimated_time": "10-15 minut"
            },
            "hard": {
                "title": "Reorganizacja i opór przed zmianą",
                "company_context": "GlobalCorp przechodzi reorganizację. Trzy działy (IT, Marketing, Sprzedaż) mają zostać połączone w jeden cross-funkcyjny zespół produktowy.",
                "situation": "Dyrektor ds. produktu, Katarzyna, ma wdrożyć nową strukturę organizacyjną. Każdy dział ma swoje obawy: IT boi się utraty autonomii technicznej, Marketing obawia się że ich kreatywność zostanie ograniczona przez 'technicznych', Sprzedaż uważa że stracą bezpośredni kontakt z klientami. Dodatkowo, wszyscy liderzy działów bronią swoich ludzi przed 'potencjalnymi zwolnieniami'. W firmie krążą plotki, a atmosfera jest bardzo napięta. Zarząd oczekuje od Katarzyny szybkiego wdrożenia zmian.",
                "characters": {
                    "main_character": {
                        "name": "Katarzyna",
                        "position": "Dyrektor ds. Produktu", 
                        "challenge": "Przełamanie oporu przed zmianą i zbudowanie jedności w nowej strukturze"
                    },
                    "other_characters": [
                        {"name": "Liderzy IT", "position": "Head of IT", "role_in_conflict": "Bronią autonomii technicznej"},
                        {"name": "Liderzy Marketing", "position": "Marketing Manager", "role_in_conflict": "Obawy o kreatywność"},
                        {"name": "Liderzy Sprzedaży", "position": "Sales Director", "role_in_conflict": "Strach przed utratą kontaktu z klientami"}
                    ]
                },
                "communication_challenge": "Przekształcenie strachu przed zmianą w entuzjazm do współpracy cross-funkcyjnej",
                "c_iq_opportunity": "Wykorzystanie neurobiologii zaufania do budowy nowej tożsamości zespołowej",
                "task": "Opracuj kompleksową strategię komunikacyjną dla Katarzyny. Uwzględnij: 1) Spotkania one-on-one z liderami, 2) Warsztat zespołowy z wszystkimi działami, 3) Plan komunikacji długoterminowej. Użyj zaawansowanych technik C-IQ do przełamania oporów i stworzenia nowej kultury współpracy.",
                "success_criteria": ["Przełamanie oporów liderów", "Stworzenie wspólnej wizji", "Wypracowanie nowych rytów współpracy", "Zbudowanie entuzjazmu do zmian", "Opracowanie planu monitorowania postępów"],
                "difficulty": "hard",
                "estimated_time": "20-30 minut"
            }
        }
        
        case = demo_cases.get(difficulty_level, demo_cases["medium"])
        case['generated_at'] = "demo_mode"
        return case
    
    def _fallback_evaluation(self, user_response: str) -> Dict:
        """Ocena fallback w przypadku błędu"""
        word_count = len(user_response.split()) if user_response else 0
        return {
            "score": min(7, max(3, word_count // 25)),
            "feedback": "⚠️ Wystąpił problem z oceną AI. Otrzymujesz podstawową ocenę na podstawie długości odpowiedzi. Spróbuj ponownie później lub skontaktuj się z administratorem.",
            "strong_points": ["Ukończenie ćwiczenia"],
            "suggestions": ["Spróbuj ponownie później"]
        }
    
    def get_ai_evaluation_direct(self, prompt: str) -> Dict:
        """
        Publiczna funkcja do bezpośredniego wywołania AI dla narzędzi
        Wrapper na prywatną funkcję _get_ai_evaluation
        """
        return self._get_ai_evaluation(prompt)


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
                    # Pokaż odpowiedź użytkownika
                    response_key = f"ai_exercise_{exercise_id}_response"
                    if response_key in st.session_state:
                        user_response = st.session_state[response_key]
                        st.markdown("### 📝 Twoja odpowiedź")
                        st.info(user_response)
                        st.markdown("---")
                    
                    # Pokaż feedback AI
                    feedback = st.session_state[feedback_key]
                    display_ai_feedback(feedback)
            with col2:
                if st.button("🔄 Reset", key=f"reset_{exercise_id}", help="Resetuj to ćwiczenie i zrób je ponownie"):
                    reset_single_exercise(exercise_id)
                    st.rerun()
        
        return True
    
    # Wyświetl formularz odpowiedzi
    
    # Specjalna obsługa dla generated_case - najpierw wygeneruj i wyświetl przypadek
    ai_config = exercise.get('ai_config', {})
    exercise_type = ai_config.get('exercise_type', '')
    
    if exercise_type == 'generated_case':
        # Sprawdź czy przypadek już został wygenerowany
        case_key = f"ai_exercise_{exercise_id}_generated_case"
        
        if case_key not in st.session_state:
            # Wyświetl opcje personalizacji case study
            st.markdown("### 🎯 Personalizuj swój case study")
            st.markdown("Wybierz parametry, aby otrzymać case study dostosowany do Twoich potrzeb:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Stopień trudności:**")
                difficulty_level = st.radio(
                    "Wybierz poziom:",
                    options=['easy', 'medium', 'hard'],
                    format_func=lambda x: {
                        'easy': '🟢 Łatwy (2-3 słowa odpowiedzi)',
                        'medium': '🟡 Średni (3-5 zdań)',
                        'hard': '🔴 Trudny (szczegółowa analiza)'
                    }[x],
                    index=1,  # medium jako domyślny
                    key=f"difficulty_{exercise_id}"
                )
            
            with col2:
                st.markdown("**🏢 Branża:**")
                industry = st.selectbox(
                    "Wybierz sektor:",
                    options=['IT', 'Finanse', 'FMCG', 'Farmacja', 'Nauka', 'Ogólny'],
                    format_func=lambda x: {
                        'IT': '💻 IT / Technologie',
                        'Finanse': '💰 Finanse / Banking',
                        'FMCG': '🛒 FMCG / Retail',
                        'Farmacja': '💊 Farmacja / Medycyna',
                        'Nauka': '🎓 Nauka / Edukacja',
                        'Ogólny': '🏢 Ogólny biznes'
                    }[x],
                    index=0,  # IT jako domyślny
                    key=f"industry_{exercise_id}"
                )
            
            # Wyświetl opis wybranej konfiguracji
            difficulty_names = {'easy': 'Łatwy', 'medium': 'Średni', 'hard': 'Trudny'}
            industry_names = {'IT': 'IT/Technologie', 'Finanse': 'Finanse/Banking', 'FMCG': 'FMCG/Retail', 'Farmacja': 'Farmacja/Medycyna', 'Nauka': 'Nauka/Edukacja', 'Ogólny': 'Ogólny biznes'}
            
            st.info(f"""
**Twoje ustawienia:**
- **Poziom:** {difficulty_names[difficulty_level]}
- **Branża:** {industry_names[industry]}

Case study będzie dostosowany do wybranej branży z odpowiednim poziomem złożoności.
            """)
            
            # Przycisk generowania
            if st.button("🎲 Wygeneruj spersonalizowany case study", key=f"generate_{exercise_id}"):
                with st.spinner("🎲 Generuję spersonalizowany przypadek komunikacyjny..."):
                    evaluator = AIExerciseEvaluator()
                    lesson_context = ai_config.get('lesson_context', lesson_context)
                    
                    try:
                        generated_case = evaluator.generate_case_study(
                            lesson_context=lesson_context, 
                            difficulty_level=difficulty_level,
                            industry=industry
                        )
                        st.session_state[case_key] = generated_case
                        st.rerun()
                    except Exception as e:
                        st.error(f"Błąd podczas generowania przypadku: {str(e)}")
                        # Fallback - użyj demo przypadku z wybranymi parametrami
                        demo_case = evaluator._generate_demo_case(difficulty_level)
                        demo_case['industry'] = industry  # Dodaj informację o branży
                        st.session_state[case_key] = demo_case
                        st.rerun()
        
        # Wyświetl wygenerowany przypadek
        if case_key in st.session_state:
            generated_case = st.session_state[case_key]
            
            st.markdown("### 🎯 Twoje zadanie")
            
            # Wyświetl przypadek w ładnym formacie
            st.markdown(f"""
<div style='background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #007bff; margin: 15px 0;'>
<h4 style='color: #0066cc; margin-top: 0;'>📋 {generated_case.get('title', 'Przypadek komunikacyjny')}</h4>
<p style='line-height: 1.6; margin-bottom: 10px;'><strong>Kontekst:</strong> {generated_case.get('company_context', '')}</p>
<p style='line-height: 1.6; margin-bottom: 15px;'><strong>Sytuacja:</strong> {generated_case.get('situation', '')}</p>
<div style='background: #fff; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6;'>
<strong>🎯 Zadanie:</strong><br>
{generated_case.get('task', 'Przeanalizuj sytuację i zaproponuj rozwiązanie.')}
</div>
</div>
""", unsafe_allow_html=True)
            
            # Dodaj przycisk do wygenerowania nowego przypadku
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button("🔄 Nowy przypadek", key=f"new_case_{exercise_id}", help="Wygeneruj nowy przypadek"):
                    del st.session_state[case_key]
                    st.rerun()
    
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
                    ai_config = exercise.get('ai_config', {}).copy()  # Kopia żeby nie modyfikować oryginału
                    
                    # Dla generated_case, dodaj wygenerowany case study do config
                    if exercise_type == 'generated_case':
                        case_key = f"ai_exercise_{exercise_id}_generated_case"
                        if case_key in st.session_state:
                            ai_config['generated_case_data'] = st.session_state[case_key]
                    
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


def reset_all_ai_exercises(lesson_id: str = None, exercise_prefix: str = "ai_exercise"):
    """Resetuje wszystkie ćwiczenia AI (opcjonalnie dla konkretnej lekcji)"""
    keys_to_remove = []
    
    for key in st.session_state.keys():
        if key.startswith(f"{exercise_prefix}_") and (
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


def display_reset_all_button(lesson_id: str = None, exercise_prefix: str = "ai_exercise"):
    """Wyświetla przycisk do resetowania wszystkich ćwiczeń AI"""
    
    # Sprawdź ile ćwiczeń jest ukończonych
    completed_count = 0
    total_exercises = 0
    
    for key in st.session_state.keys():
        if key.startswith(f"{exercise_prefix}_") and key.endswith("_completed"):
            if lesson_id and f"_{lesson_id}_" not in key:
                continue
            total_exercises += 1
            if st.session_state.get(key, False):
                completed_count += 1
    
    if completed_count > 0:
        with st.expander(f"🔄 Reset ćwiczeń {exercise_prefix.replace('_', ' ').title()} ({completed_count} ukończonych)", expanded=False):
            st.warning(f"⚠️ Spowoduje to usunięcie wszystkich odpowiedzi i feedback'ów z {completed_count} ukończonych ćwiczeń.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Resetuj wszystkie ćwiczenia", key=f"reset_all_{exercise_prefix}_{lesson_id or 'global'}"):
                    reset_count = reset_all_ai_exercises(lesson_id, exercise_prefix)
                    st.success(f"✅ Zresetowano {reset_count} ćwiczeń {exercise_prefix.replace('_', ' ').title()}! Możesz je zrobić ponownie.")
                    st.rerun()
            
            with col2:
                st.info("💡 **Wskazówka**: Możesz też resetować pojedyncze ćwiczenia przyciskiem 🔄 obok każdego.")


def display_ai_feedback(feedback: Dict):
    """Wyświetla feedback AI w przyjaznym formacie"""
    
    # DEBUGGING: sprawdź typ feedback
    if not isinstance(feedback, dict):
        st.error(f"⚠️ Błąd: Feedback nie jest słownikiem. Typ: {type(feedback)}")
        st.code(str(feedback)[:500] + "..." if len(str(feedback)) > 500 else str(feedback))
        return
    
    # Główny feedback - AI już generuje wszystko w tekście z własnymi nagłówkami
    if 'feedback' in feedback:
        st.markdown(feedback['feedback'], unsafe_allow_html=True)
    
    # Motywująca wiadomość (jeśli dostępna)
    if 'motivation_message' in feedback:
        st.markdown("### 🌟 Wiadomość motywacyjna")
        st.success(feedback['motivation_message'])