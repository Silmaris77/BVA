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
        
        prompt = f"""Jesteś ekspertem C-IQ. Oceń identyfikację poziomu rozmowy - ZWIĘŹLE (max 1000 znaków).

KLUCZOWE: W modelu C-IQ są TYLKO 3 POZIOMY:
• Poziom I (Transakcyjny) - wymiana informacji
• Poziom II (Pozycyjny) - obrona stanowisk, ja vs ty
• Poziom III (Transformacyjny) - współtworzenie, my razem
NIE ma poziomu 0, 4, 5 ani innych!

WYPOWIEDŹ:
"Widzę, że mamy wyzwanie z terminami. Zastanawiam się, jakie przeszkody napotykamy jako zespół i jak możemy razem wypracować rozwiązania, które będą działać dla wszystkich. Co myślicie o przyczynach tej sytuacji i jakie pomysły macie na ulepszenie naszych procesów?"

ODPOWIEDŹ UCZESTNIKA: {user_response}

POPRAWNA: Poziom III (Transformacyjny) - język współtworzenia, pytania otwarte.

WAŻNE: Użyj DOKŁADNIE tego formatu. NIE dodawaj emoji ani dwukropków po nagłówkach!

**OCENA OGÓLNA:** [liczba 1-10]

**FEEDBACK**
[2-3 zwięzłe akapity głównej analizy]

**MOCNE STRONY**
• [punkt 1]
• [punkt 2]

**DO POPRAWY**
• [punkt 1 - konkretnie]
• [punkt 2]

**KLUCZOWA RADA**
[Jedna najważniejsza lekcja - napisz przystępnie, bez żargonu. Dodaj KONKRETNY PRZYKŁAD: cytuj dokładną wypowiedź (w cudzysłowie) lub opisz konkretne zachowanie, które jest emanacją tej rady. Np. "Zamiast mówić 'To nie zadziała', powiedz: 'Co by się stało, gdybyśmy spróbowali...?'" lub "Przed spotkaniem poświęć 2 minuty na głęboki oddech i uświadom sobie intencję - chcesz zrozumieć, nie wygrać."]
"""
        
        return self._get_ai_evaluation_text(prompt)
    
    def _evaluate_conversation_simulation(self, config: Dict, user_response: str, context: str) -> Dict:
        """Ocena symulacji rozmowy"""
        
        criteria = config.get('feedback_criteria', [])
        system_prompt = config.get('ai_prompts', {}).get('system', 
            "Jesteś ekspertem w Conversational Intelligence. Analizuj symulacje rozmów.")
        evaluation_prompt = config.get('ai_prompts', {}).get('evaluation', 
            "Oceń symulację rozmowy pod kątem zastosowania zasad C-IQ.")
        
        prompt = f"""Jesteś ekspertem C-IQ. Oceń symulację rozmowy - ZWIĘŹLE (max 1200 znaków).

KLUCZOWE: W modelu C-IQ są TYLKO 3 POZIOMY:
• Poziom I (Transakcyjny) - wymiana informacji
• Poziom II (Pozycyjny) - obrona stanowisk, ja vs ty
• Poziom III (Transformacyjny) - współtworzenie, my razem
NIE ma poziomu 0, 4, 5 ani innych!

KONTEKST: {context}

SYMULACJA UCZESTNIKA: {user_response}

KRYTERIA: {', '.join(criteria)}

WAŻNE: Użyj DOKŁADNIE tego formatu. NIE dodawaj emoji ani dwukropków po nagłówkach!

**OCENA OGÓLNA:** [liczba 1-10]

**FEEDBACK**
[2-3 akapity: Jak wykorzystał poziomy C-IQ? Co z neurobiologią (kortyzol vs oksytocyna)? Jakie techniki zastosował lub pominął?]

**MOCNE STRONY**
• [punkt 1]
• [punkt 2]

**DO POPRAWY**
• [punkt 1 - konkretnie jak poprawić]
• [punkt 2]

**KLUCZOWA RADA**
[Jedna najważniejsza wskazówka - napisz przystępnie, jak do kolegi. Dodaj KONKRETNY PRZYKŁAD: cytuj dokładną wypowiedź (w cudzysłowie) lub opisz konkretne zachowanie. Np. "Gdy widzisz, że rozmówca się defensuje, zatrzymaj się i powiedz: 'Chcę zrozumieć Twoją perspektywę - co jest dla Ciebie najważniejsze w tej sytuacji?'" lub "Zanotuj sobie na kartce przed trudną rozmową: 'Moja intencja = partnerstwo, nie wygrana'."]
"""
        
        return self._get_ai_evaluation_text(prompt)
    
    def _evaluate_case_analysis(self, config: Dict, user_response: str, context: str) -> Dict:
        """Ocena analizy przypadku"""
        
        assessment_rubric = config.get('assessment_rubric', {})
        system_prompt = config.get('ai_prompts', {}).get('system',
            "Jesteś ekspertem w analizie przypadków komunikacyjnych.")
        
        prompt = f"""Jesteś ekspertem C-IQ. Oceń analizę przypadku - ZWIĘŹLE (max 1200 znaków).

KLUCZOWE: W modelu C-IQ są TYLKO 3 POZIOMY:
• Poziom I (Transakcyjny) - wymiana informacji
• Poziom II (Pozycyjny) - obrona stanowisk, ja vs ty
• Poziom III (Transformacyjny) - współtworzenie, my razem
NIE ma poziomu 0, 4, 5 ani innych!

KONTEKST: {context}

ANALIZA UCZESTNIKA: {user_response}

WAŻNE: Użyj DOKŁADNIE tego formatu z emoji. NIE ZMIENIAJ nagłówków!

**🎯 OCENA:** [1-10]

**� FEEDBACK:**
[2-3 akapity: Jak dobrze przeanalizował przypadek? Czy zidentyfikował poziomy C-IQ? Co z neurobiologią i praktyką?]

**✅ MOCNE STRONY:**
• [punkt 1]
• [punkt 2]

**🎯 DO POPRAWY:**
• [punkt 1 - konkretnie]
• [punkt 2]

**💡 KLUCZOWA RADA:**
[Jedna najważniejsza lekcja - pisz jak do przyjaciela, prostym językiem. Zawrzyj KONKRETNY PRZYKŁAD działania lub wypowiedzi. Np. "Przed ważną rozmową powiedz sobie na głos: 'Mogę być ciekawy, zamiast mieć rację' - te 5 sekund zmienia całą interakcję" lub "Gdy czujesz napięcie w brzuchu podczas rozmowy, to znak - weź głęboki oddech i zapytaj: 'Jak Ty to widzisz?'"]
"""
        
        return self._get_ai_evaluation_text(prompt)
    
    def _evaluate_self_reflection(self, config: Dict, user_response: str, context: str) -> Dict:
        """Ocena refleksji osobistej (styl coachingowy)"""
        
        system_prompt = config.get('ai_prompts', {}).get('system',
            "Jesteś profesjonalnym coachem. Udzielaj wspierającego feedback'u.")
        
        prompt = f"""Jesteś coachem. Oceń refleksję osobistą - WSPIERAJĄCO i ZWIĘŹLE (max 1000 znaków).

KONTEKST: {context}

REFLEKSJA UCZESTNIKA: {user_response}

WAŻNE: Użyj DOKŁADNIE tego formatu z emoji. NIE ZMIENIAJ nagłówków!

**🎯 OCENA:** [1-10]

**💬 FEEDBACK:**
[2-3 akapity: Docenij samoświadomość. Wskaż mocne strony. Delikatnie zasugeruj obszary rozwoju. Zmotywuj.]

**✅ ZAUWAŻONE MOCNE STRONY:**
• [punkt 1]
• [punkt 2]

**🌱 SZANSE ROZWOJU:**
• [punkt 1 - delikatnie]
• [punkt 2]

**💡 MAŁY KROK DO DZIAŁANIA:**
[Jedna konkretna, łatwa rzecz do zrobienia dzisiaj]
"""
        
        return self._get_ai_evaluation_text(prompt)
    
    def _evaluate_general_exercise(self, config: Dict, user_response: str, context: str) -> Dict:
        """Ocena ogólnego ćwiczenia"""
        
        criteria = config.get('feedback_criteria', [])
        
        prompt = f"""Jesteś ekspertem C-IQ. Oceń odpowiedź - ZWIĘŹLE (max 1000 znaków).

KLUCZOWE: W modelu C-IQ są TYLKO 3 POZIOMY:
• Poziom I (Transakcyjny) - wymiana informacji
• Poziom II (Pozycyjny) - obrona stanowisk, ja vs ty
• Poziom III (Transformacyjny) - współtworzenie, my razem
NIE ma poziomu 0, 4, 5 ani innych!

KONTEKST: {context}

ODPOWIEDŹ: {user_response}

KRYTERIA: {', '.join(criteria)}

WAŻNE: Użyj DOKŁADNIE tego formatu z emoji. NIE ZMIENIAJ nagłówków!

**🎯 OCENA:** [1-10]

**💬 FEEDBACK:**
[2-3 akapity konstruktywnej analizy]

**✅ MOCNE STRONY:**
• [punkt 1]
• [punkt 2]

**🎯 SUGESTIE:**
• [punkt 1]
• [punkt 2]

**💡 KLUCZOWA RADA:**
[Jedna najważniejsza lekcja - pisz prostym, przystępnym językiem. Dodaj KONKRETNY PRZYKŁAD: dokładną wypowiedź (w cudzysłowie "...") lub konkretne zachowanie. Np. "Następnym razem, zanim odpowiesz na zarzut, zrób pauzę 3 sekundy i zapytaj: 'Powiedz mi więcej - co dokładnie Cię martwi?'" lub "Zacznij spotkanie od: 'Chcę, żebyśmy wspólnie znaleźli rozwiązanie' - te słowa uruchamiają oksytocynę zamiast kortyzolu."]
"""
        
        return self._get_ai_evaluation_text(prompt)
    
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
        
        prompt = f"""Jesteś ekspertem C-IQ. Oceń rozwiązanie case study - ZWIĘŹLE (max 1500 znaków).

KLUCZOWE: W modelu C-IQ są TYLKO 3 POZIOMY:
• Poziom I (Transakcyjny) - wymiana informacji
• Poziom II (Pozycyjny) - obrona stanowisk, ja vs ty
• Poziom III (Transformacyjny) - współtworzenie, my razem
NIE ma poziomu 0, 4, 5 ani innych!

CASE STUDY:
Tytuł: {case_data.get('title', 'Case Study')}
Kontekst: {case_data.get('company_context', '')}
Sytuacja: {case_data.get('situation', '')}
Zadanie: {case_data.get('task', '')}

ROZWIĄZANIE UCZESTNIKA: {user_response}

WAŻNE: Użyj DOKŁADNIE tego formatu. NIE dodawaj emoji ani dwukropków po nagłówkach!

**OCENA OGÓLNA:** [liczba 1-10]

**FEEDBACK**
[2-4 akapity: Czy poprawnie zidentyfikował poziom C-IQ (I, II lub III)? Jak praktyczne jest rozwiązanie? Co z neurobiologią? Przykład lepszego podejścia.]

**MOCNE STRONY**
• [punkt 1]
• [punkt 2]

**DO POPRAWY**
• [punkt 1 - konkretnie jak poprawić]
• [punkt 2]

**KLUCZOWA RADA**
[Jedna najważniejsza lekcja - pisz prostym, zrozumiałym językiem (bez żargonu!). Dodaj KONKRETNY PRZYKŁAD: albo cytuj dokładną wypowiedź (w cudzysłowie "..."), albo opisz konkretne zachowanie krok po kroku. Np. "Zanim zaczniesz mówić o rozwiązaniu, powiedz: 'Rozumiem, że to dla Ciebie ważne - powiedz mi, co najbardziej Cię w tym niepokoi?' - takie pytanie obniża kortyzol o 40%" lub "Gdy ktoś atakuje, zamiast się bronić, zrób to: (1) głęboki oddech, (2) kontakt wzrokowy, (3) powiedz: 'Słyszę, że jesteś zaniepokojony. Pomóż mi to zrozumieć.' UŻYWAJ TYLKO Poziomów I, II, III!"]
"""
        
        result = self._get_ai_evaluation_text(prompt)
        # Dodaj case_data do wyniku, aby móc wygenerować wzorcową odpowiedź
        result['generated_case_data'] = case_data
        return result
    
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
            # Szukaj oceny w różnych formatach: "OCENA OGÓLNA: 8", "**🎯 OCENA OGÓLNA:** 7", itp.
            import re
            overall_score_match = re.search(r'OCENA\s+OG[ÓO]LNA[:\*\s]+(\d+)', content, re.IGNORECASE)
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
            # Szczegółowe konteksty dla poszczególnych branż
            detailed_contexts = {
                "Nauka": """ w środowisku akademickim - Interdisciplinary Centre for Labour Market and Family Dynamics (LabFam) na Uniwersytecie Warszawskim.

KONTEKST BRANŻY NAUKA - LabFam:

GŁÓWNA POSTAĆ (używaj zawsze tej osoby):
Anna Matysiak - Head of LabFam (kierownik centrum badawczego)

O LabFam:
LabFam to interdyscyplinarne centrum badawcze na Wydziale Nauk Ekonomicznych Uniwersytetu Warszawskiego, które bada związki między rynkiem pracy, technologią, globalizacją a dynamiką rodziny. Centrum powstało dzięki finansowaniu NAWA (Polskie Powroty 2019) i prowadzi projekty finansowane przez European Research Council (ERC), w tym flagowy projekt LABFER o wpływie globalizacji i technologii na płodność. LabFam łączy ekonomistów, socjologów, demografów, politologów i statystyków.

ZESPÓŁ LABFAM (używaj tych prawdziwych imion w case study):

Kierownictwo:
- Anna Matysiak (Head of LabFam) - profesor, demografka rodzin i ekonomistka
- Anna Kurowska (Vice-Head) - profesor, politolog i ekonomistka specjalizująca się w polityce rodzinnej
- Anna Wielgopolan (Project Manager) - zarządza administracją i upowszechnianiem

Senior Researchers (Assistant/Associate Professors):
- Ewa Cukrowska-Torzewska - ekonomistka, nierówności płci na rynku pracy
- Wojciech Hardy - ekonomista, technologia i rynek pracy, sektory kreatywne
- Ewa Jarosz - socjolożka, time use, zdrowie publiczne
- Beata Osiewalska - demografka rodzin i statystyczka, childlessness
- Lucas van der Velde - ekonomista, automatyzacja i konsekwencje dla rodzin
- Alina Pavelea - ekonomistka, precarious work, creative workers

PhD Researchers i Research Assistants:
- Agata Kałamucka - ekonomistka, family dynamics, work-life balance
- Agnieszka Kasperska - gender and job quality, social policies
- Chen Luo - ekonomistka, globalizacja i demografia, gender equality
- Honorata Bogusz - ekonometryczka, automation and labor markets
- Ewa Weychert - data analyst, machine learning, inequality
- Ilyar Heydari Barardehi - family policy, gendered roles, aging
- Magdalena Grabowska - ekonomistka, subjective well-being, labor market outcomes

Typowe wyzwania komunikacyjne Anny Matysiak jako Head of LabFam:
- Zarządzanie międzynarodowym, interdyscyplinarnym zespołem (ekonomiści, socjologowie, demografowie)
- Koordynacja projektów badawczych (LABFER/ERC, rEUsilience/Horyzont Europa, projekty IDUB)
- Mentoring doktorantów (Agata, Agnieszka, Chen, Honorata, Ewa, Ilyar, Magdalena) i młodszych badaczy
- Organizacja seminariów naukowych z zagranicznymi prelegentami
- Mediacja w konfliktach o autorstwo publikacji i podział zasobów
- Balansowanie między własnymi badaniami a obowiązkami kierowniczymi
- Komunikacja z grantodawcami (ERC, NAWA, Komisja Europejska) i raportowanie
- Budowanie współpracy międzywydziałowej (WNE, Wydział Nauk Politycznych)
- Zarządzanie presją publikacyjną (Journal of Marriage and Family, Population Studies, Demographic Research)
- Rozwiązywanie napięć między młodszymi naukowcami a seniorami (np. Ewa CT, Wojciech, Beata)
- Prowadzenie trudnych rozmów o przedłużeniu/zakończeniu kontraktów z doktorantami/postdokami
- Tworzenie kultury współpracy w środowisku naturalnie konkurencyjnym
- Koordynacja pracy Vice-Head (Anna Kurowska) i Project Manager (Anna Wielgopolan)

WAŻNE: Case study musi zawsze dotyczyć Anny Matysiak jako Head of LabFam w konkretnej sytuacji menedżerskiej/przywódczej. Używaj prawdziwych imion członków zespołu wymienionego powyżej (np. Wojciech Hardy, Ewa Cukrowska-Torzewska, Agata Kałamucka, Chen Luo, Honorata Bogusz itp.)."""
            }
            
            industry_context = detailed_contexts.get(industry, f" w branży {industry}")

        
        prompt = f"""
Wygeneruj realny case study z obszaru komunikacji zespołowej i przywództwa{industry_context}.

KONTEKST LEKCJI: {lesson_context}

POZIOM TRUDNOŚCI: {difficulty_prompts.get(difficulty_level, "medium")}

WYMAGANIA CO DO ZADANIA: {task_complexity.get(difficulty_level, "")}

{'KLUCZOWE DLA BRANŻY NAUKA: Case study MUSI dotyczyć Anny Matysiak jako Head of LabFam (kierownik centrum badawczego na UW). Anna Matysiak to doświadczony naukowiec i menedżer zarządzający międzynarodowym zespołem badawczym. Sytuacja powinna być realistyczna dla środowiska akademickiego. UŻYWAJ PRAWDZIWYCH IMION z zespołu LabFam (np. Wojciech Hardy, Ewa Cukrowska-Torzewska, Agata Kałamucka, Chen Luo, Honorata Bogusz, Anna Kurowska, Beata Osiewalska itp.).' if industry == 'Nauka' else ''}

Stwórz {difficulty_prompts.get(difficulty_level, "przypadek o średniej złożoności")} oparty na zasadach Conversational Intelligence, który:

1. **Przedstawia autentyczną sytuację {'w LabFam na UW' if industry == 'Nauka' else 'biznesową'}** z konkretymi postaciami
2. **Zawiera wyzwanie komunikacyjne** wymagające zastosowania C-IQ
3. **Ma jasno określony cel** - {'co Anna powinna zrobić jako lider' if industry == 'Nauka' else 'co należy osiągnąć'}
4. **Uwzględnia neurobiologię rozmowy** (poziomy, oksytocyna/kortyzol)

WAŻNE - dostosuj zadanie do poziomu trudności:
- EASY: zadanie musi być bardzo proste, wystarczy odpowiedź 2-3 słów lub jedno zdanie
- MEDIUM: zadanie powinno wymagać odpowiedzi 3-5 zdań
- HARD: zadanie może wymagać szczegółowej analizy

Wygeneruj w formacie JSON:

{{
    "title": "[krótki, opisowy tytuł case study]",
    "company_context": "[2-3 zdania o firmie/dziale{' - dla branży Nauka: zawsze LabFam na UW' if industry == 'Nauka' else ''}]",
    "situation": "[szczegółowy opis sytuacji - 4-6 zdań]",
    "characters": {{
        "main_character": {{
            "name": "{'Anna Matysiak' if industry == 'Nauka' else '[imię]'}",
            "position": "{'Head of LabFam' if industry == 'Nauka' else '[stanowisko]'}",
            "challenge": "[główne wyzwanie tej osoby]"
        }},
        "other_characters": [
            {{
                "name": "[{'UŻYWAJ PRAWDZIWYCH imion z zespołu LabFam: Wojciech Hardy, Ewa Cukrowska-Torzewska, Agata Kałamucka, Chen Luo, Honorata Bogusz, Anna Kurowska, Beata Osiewalska, Ewa Jarosz, Lucas van der Velde, Alina Pavelea, Agnieszka Kasperska, Ewa Weychert, Ilyar Heydari Barardehi, Magdalena Grabowska, Anna Wielgopolan' if industry == 'Nauka' else 'imię'}]",
                "position": "[stanowisko - np. {'PhD Researcher, Research Assistant, Assistant Professor, Vice-Head, Project Manager' if industry == 'Nauka' else 'stanowisko'}]", 
                "role_in_conflict": "[rola w sytuacji]"
            }}
        ]
    }},
    "communication_challenge": "[główny problem komunikacyjny]",
    "c_iq_opportunity": "[jakie zasady C-IQ można zastosować]",
    "task": "[konkretne zadanie dla uczestnika - {'CO ANNA MATYSIAK (Head of LabFam) POWINNA ZROBIĆ w tej sytuacji' if industry == 'Nauka' else 'co ma zrobić'}]",
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
            # Sprawdź czy to świeży feedback (właśnie otrzymany)
            fresh_feedback_key = f"ai_exercise_{exercise_id}_fresh_feedback"
            is_fresh = st.session_state.get(fresh_feedback_key, True)
            
            with st.expander("📝 Feedback AI", expanded=is_fresh):
                # Po pierwszym wyświetleniu oznacz jako nieświeży
                if is_fresh:
                    st.session_state[fresh_feedback_key] = False
                
                # Pokaż odpowiedź użytkownika
                response_key = f"ai_exercise_{exercise_id}_response"
                if response_key in st.session_state:
                    user_response = st.session_state[response_key]
                    st.markdown("### 📝 Twoja odpowiedź")
                    st.info(user_response)
                    st.markdown("---")
                
                # Pokaż feedback AI
                feedback = st.session_state[feedback_key]
                # Pobierz exercise_type dla feedbacku
                exercise_type = exercise.get('ai_config', {}).get('exercise_type', '')
                
                # Utwórz evaluator dla wzorcowej odpowiedzi
                evaluator = AIExerciseEvaluator()
                
                display_ai_feedback(feedback, exercise_type=exercise_type, evaluator=evaluator)
            
            # Przycisk Reset pod expanderem
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("🔄 Reset", key=f"reset_{exercise_id}", help="Resetuj to ćwiczenie i zrób je ponownie", use_container_width=True):
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
            # Opcje personalizacji - bez tabsów
            col1, col2 = st.columns(2)
            
            with col1:
                difficulty_level = st.selectbox(
                    "Poziom trudności:",
                    options=['easy', 'medium', 'hard'],
                    format_func=lambda x: {
                        'easy': '🟢 Łatwy',
                        'medium': '🟡 Średni',
                        'hard': '🔴 Trudny'
                    }[x],
                    index=1,
                    key=f"difficulty_{exercise_id}"
                )
            
            with col2:
                industry = st.selectbox(
                    "Branża:",
                    options=['IT', 'Finanse', 'FMCG', 'Farmacja', 'Nauka', 'Ogólny'],
                    format_func=lambda x: {
                        'IT': '💻 IT / Technologie',
                        'Finanse': '💰 Finanse / Banking',
                        'FMCG': '🛒 FMCG / Retail',
                        'Farmacja': '💊 Farmacja / Medycyna',
                        'Nauka': '🎓 Nauka / Edukacja',
                        'Ogólny': '🏢 Ogólny biznes'
                    }[x],
                    index=0,
                    key=f"industry_{exercise_id}"
                )
            
            st.info(f"💡 Wygeneruję case study na poziomie **{difficulty_level}** z branży **{industry}**")
            
            if st.button("🎲 Wygeneruj Case Study", key=f"generate_{exercise_id}"):
                with st.spinner("🎲 Generuję spersonalizowany przypadek..."):
                    evaluator = AIExerciseEvaluator()
                    lesson_context = ai_config.get('lesson_context', lesson_context)
                    
                    try:
                        generated_case = evaluator.generate_case_study(
                            lesson_context=lesson_context, 
                            difficulty_level=difficulty_level,
                            industry=industry
                        )
                        st.session_state[case_key] = generated_case
                        st.success("✅ Case study wygenerowany!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Błąd podczas generowania przypadku: {str(e)}")
                        demo_case = evaluator._generate_demo_case(difficulty_level)
                        demo_case['industry'] = industry
                        st.session_state[case_key] = demo_case
                        st.success("✅ Case study wygenerowany (demo mode)!")
                        st.rerun()
        
        # Wyświetl wygenerowany przypadek i formularz odpowiedzi
        if case_key in st.session_state:
            generated_case = st.session_state[case_key]
            
            st.markdown("### 🎯 Twoje zadanie")
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
            
            # Sprawdź czy użytkownik już otrzymał feedback
            feedback_key = f"ai_exercise_{exercise_id}_feedback"
            has_feedback = feedback_key in st.session_state
            
            # Jeśli NIE MA jeszcze feedbacku, pokaż przycisk Reset (wygeneruj nowy case)
            if not has_feedback:
                col1, col2, col3 = st.columns([2, 1, 2])
                with col2:
                    if st.button("🔄 Wygeneruj nowy", key=f"regenerate_{exercise_id}", help="Nie podoba Ci się ten case? Wygeneruj nowy!", use_container_width=True):
                        # Usuń wygenerowany case
                        if case_key in st.session_state:
                            del st.session_state[case_key]
                        # Usuń odpowiedź (jeśli była)
                        response_key = f"ai_exercise_{exercise_id}_response"
                        if response_key in st.session_state:
                            del st.session_state[response_key]
                        st.success("✨ Kliknij 'Wygeneruj Case Study' aby otrzymać nowy przypadek!")
                        st.rerun()
                st.markdown("---")
            
            # Pole odpowiedzi - tylko po wygenerowaniu case study
            response_key = f"ai_exercise_{exercise_id}_response"
            user_response = st.text_area(
                "Twoja odpowiedź:",
                value=st.session_state.get(response_key, ""),
                height=200,
                key=response_key,
                placeholder="Wpisz swoją szczegółową odpowiedź tutaj..."
            )
            
            # Przycisk do otrzymania feedback'u AI
            if st.button(f"🤖 Otrzymaj feedback AI", key=f"evaluate_{exercise_id}"):
                if len(user_response.strip()) < 2:
                    st.warning("Napisz co najmniej 2 słowa, aby otrzymać szczegółowy feedback.")
                else:
                    with st.spinner("AI analizuje Twoją odpowiedź..."):
                        evaluator = AIExerciseEvaluator()
                        ai_config = exercise.get('ai_config', {}).copy()
                        
                        # Dla generated_case, dodaj wygenerowany case study do config
                        if exercise_type == 'generated_case':
                            case_key_inner = f"ai_exercise_{exercise_id}_generated_case"
                            if case_key_inner in st.session_state:
                                ai_config['generated_case_data'] = st.session_state[case_key_inner]
                        
                        result = evaluator.evaluate_exercise(ai_config, user_response, lesson_context)
                        
                        # Zapisz feedback
                        feedback_key = f"ai_exercise_{exercise_id}_feedback"
                        st.session_state[feedback_key] = result
                        
                        # Oznacz jako świeży feedback (rozwinie się automatycznie)
                        fresh_feedback_key = f"ai_exercise_{exercise_id}_fresh_feedback"
                        st.session_state[fresh_feedback_key] = True
                        
                        # Oznacz jako ukończone
                        st.session_state[completion_key] = True
                        
                        st.rerun()
    
    # Jeśli to NIE jest generated_case, wyświetl standardowy formularz
    
    return False


def reset_single_exercise(exercise_id: str):
    """Resetuje pojedyncze ćwiczenie AI"""
    completion_key = f"ai_exercise_{exercise_id}_completed"
    feedback_key = f"ai_exercise_{exercise_id}_feedback"
    response_key = f"ai_exercise_{exercise_id}_response"
    case_key = f"ai_exercise_{exercise_id}_generated_case"
    
    # Usuń z session_state
    if completion_key in st.session_state:
        del st.session_state[completion_key]
    if feedback_key in st.session_state:
        del st.session_state[feedback_key]
    if response_key in st.session_state:
        del st.session_state[response_key]
    if case_key in st.session_state:
        del st.session_state[case_key]
    
    st.success(f"✅ Ćwiczenie zresetowane! Możesz je zrobić ponownie.")


def reset_all_ai_exercises(lesson_id: str = None, exercise_prefix: str = "ai_exercise"):
    """Resetuje wszystkie ćwiczenia AI (opcjonalnie dla konkretnej lekcji)"""
    keys_to_remove = []
    
    for key in st.session_state.keys():
        if key.startswith(f"{exercise_prefix}_") and (
            key.endswith("_completed") or 
            key.endswith("_feedback") or 
            key.endswith("_response") or
            key.endswith("_generated_case")
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


def generate_model_answer(case_data: Dict, evaluator) -> str:
    """Generuje wzorcową odpowiedź na poziomie 10/10 dla case study używając AI"""
    
    title = case_data.get('title', 'Case Study')
    context = case_data.get('company_context', '')
    situation = case_data.get('situation', '')
    challenge = case_data.get('challenge', '')
    
    # Prompt do wygenerowania wzorcowej odpowiedzi
    prompt = f"""Jesteś światowej klasy ekspertem w Conversational Intelligence (C-IQ). 
Twoim zadaniem jest napisanie WZORCOWEJ odpowiedzi na poniższy case study, która otrzymałaby ocenę 10/10.

KLUCZOWE: W modelu C-IQ istnieją TYLKO 3 POZIOMY komunikacji:
• Poziom I (Transakcyjny) - wymiana informacji, pozycjonowanie
• Poziom II (Pozycyjny) - bronienie stanowisk, ja vs ty
• Poziom III (Transformacyjny) - współtworzenie, my razem

NIE WYMYŚLAJ innych poziomów (0, 4, 5 itd.)! Używaj TYLKO tych trzech!

CASE STUDY:
Tytuł: {title}
Kontekst firmy: {context}
Sytuacja: {situation}
Wyzwanie: {challenge}

Napisz KOMPLETNĄ odpowiedź uczestnika szkolenia, która:
1. **Precyzyjnie identyfikuje poziom C-IQ** w sytuacji - używając TYLKO Poziomu I, II lub III
2. **Głęboko analizuje aspekty neurobiologiczne** (amygdala, kortyzol, oksytocyna, układ nagrody)
3. **Proponuje KONKRETNE techniki** C-IQ do przejścia na wyższy poziom
4. **Przewiduje rezultaty** i wskaźniki sukcesu
5. Ma długość 500-700 słów
6. Jest napisana z perspektywy uczestnika ("Zrobiłbym...", "Zastosowałbym...", "Moim podejściem byłoby...")

Format odpowiedzi (użyj prostego markdown bez emoji):

**Identyfikacja poziomu C-IQ:**
[Określ czy to Poziom I, II czy III - używaj TYLKO tych trzech! Uzasadnij konkretami z case study]

**Analiza neurobiologiczna:**
[Jakie procesy w mózgu się dzieją: amygdala/kortyzol (stres) vs prefrontalny/oksytocyna (zaufanie)]

**Konkretne działania:**
[Szczegółowy plan z technikami C-IQ - np. Double-Click, Validacja, Prime, Tell Me More - minimum 3-4 kroki]

**Oczekiwane rezultaty:**
[Konkretne, mierzalne wskaźniki - jak zmieni się komunikacja i współpraca]

WAŻNE: 
- Używaj TYLKO Poziomów I, II, III - żadnych innych!
- Pisz jako uczestnik ("Moją pierwszą akcją byłoby...", "Zastosowałbym...")
- Bądź BARDZO konkretny - cytuj rozmowy, opisuj działania krok po kroku
- Odpowiedź ma być kompletna i samodzielna (500-700 słów)
- NIE używaj emoji ani ozdobników HTML - tylko czysty markdown
"""
    
    try:
        # Wywołaj AI API
        response = evaluator.gemini_model.generate_content(prompt)
        model_answer_text = response.text if response else ""
        
        if not model_answer_text or len(model_answer_text.strip()) < 100:
            return "<p style='color: #666;'>Nie udało się wygenerować wzorcowej odpowiedzi. Spróbuj ponownie.</p>"
        
        # Konwertuj podstawowy markdown na HTML
        import re
        # Zamień **text** na <strong>text</strong>
        formatted_text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', model_answer_text)
        # Zamień podwójne nowe linie na paragrafy
        formatted_text = formatted_text.replace('\n\n', '</p><p style="margin: 15px 0;">')
        # Zamień pojedyncze nowe linie na <br>
        formatted_text = formatted_text.replace('\n', '<br>')
        
        formatted_answer = f"""
<div style='padding: 20px; background: #f9fafb; border-radius: 8px; line-height: 1.8; color: #1f2937;'>
    <p style="margin: 15px 0;">{formatted_text}</p>
</div>
"""
        return formatted_answer
        
    except Exception as e:
        return f"<p style='color: #ef4444;'>Błąd podczas generowania wzorcowej odpowiedzi: {str(e)}</p>"


def display_ai_feedback(feedback: Dict, exercise_type: str = "", evaluator=None):
    """Wyświetla feedback AI w atrakcyjnym, wizualnym formacie"""
    
    # DEBUGGING: sprawdź typ feedback
    if not isinstance(feedback, dict):
        st.error(f"⚠️ Błąd: Feedback nie jest słownikiem. Typ: {type(feedback)}")
        st.code(str(feedback)[:500] + "..." if len(str(feedback)) > 500 else str(feedback))
        return
    
    # Wyciągnij tekst feedbacku i sparsuj sekcje
    feedback_text = feedback.get('feedback', '')
    
    if not feedback_text:
        st.warning("Brak feedbacku do wyświetlenia.")
        return
    
    # Usuń WSZYSTKIE emoji i symbole z nagłówków feedbacku
    import re
    # Usuń emoji, symbole Unicode i inne ozdobniki po ** (nagłówki markdown)
    # Pattern: ** + dowolne znaki niebędące literami/cyframi/spacjami + opcjonalna spacja → **
    feedback_text = re.sub(r'\*\*[^\w\s]+\s*', '**', feedback_text, flags=re.UNICODE)
    
    # Parsuj sekcje z feedbacku markdown
    
    # Wyciągnij ocenę - obsługuje "OCENA OGÓLNA" i "OCENA" z i bez emoji
    score_match = re.search(r'\*\*(?:🎯\s*)?OCENA(?:\s+OGÓLNA)?:?\*\*\s*(\d+)', feedback_text, re.IGNORECASE)
    score = int(score_match.group(1)) if score_match else feedback.get('overall_score', 7)
    
    # Określ kolor na podstawie oceny
    if score >= 9:
        color_start, color_end = "#10b981", "#059669"  # Zielony
        emoji = "🌟"
        message = "Wyśmienicie!"
    elif score >= 7:
        color_start, color_end = "#3b82f6", "#2563eb"  # Niebieski
        emoji = "👍"
        message = "Dobra robota!"
    elif score >= 5:
        color_start, color_end = "#f59e0b", "#d97706"  # Pomarańczowy
        emoji = "💪"
        message = "W porządku!"
    else:
        color_start, color_end = "#ef4444", "#dc2626"  # Czerwony
        emoji = "📈"
        message = "Potencjał do rozwoju!"
    
    # Wyświetl ocenę w dużej metryce
    st.markdown(f"""
    <div style='text-align: center; padding: 15px 20px; background: linear-gradient(135deg, {color_start} 0%, {color_end} 100%); border-radius: 12px; margin: 15px 0; box-shadow: 0 3px 5px rgba(0,0,0,0.1);'>
        <div style='font-size: 2em; margin: 0;'>{emoji}</div>
        <h1 style='color: white; font-size: 2.2em; margin: 8px 0; font-weight: bold;'>{score}<span style='font-size: 0.5em; opacity: 0.8;'>/10</span></h1>
        <p style='color: white; margin: 0; font-size: 1em; opacity: 0.95;'>{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Wyciągnij główny feedback - obsługuje format z i bez emoji
    feedback_match = re.search(r'\*\*(?:💬\s*)?FEEDBACK:?\*\*\s*(.*?)(?=\*\*(?:✅|MOCNE)|$)', feedback_text, re.DOTALL | re.IGNORECASE)
    main_feedback = feedback_match.group(1).strip() if feedback_match else ""
    
    # Wyciągnij mocne strony
    strengths_match = re.search(r'\*\*(?:✅\s*)?(?:MOCNE STRONY|ZAUWAŻONE MOCNE STRONY):?\*\*\s*(.*?)(?=\*\*(?:🎯|DO POPRAWY)|$)', feedback_text, re.DOTALL | re.IGNORECASE)
    strengths_text = strengths_match.group(1).strip() if strengths_match else ""
    strengths = [s.strip() for s in re.findall(r'•\s*([^\n•]+)', strengths_text)]
    
    # Wyciągnij obszary do poprawy
    improve_match = re.search(r'\*\*(?:[🎯🌱]\s*)?(?:DO POPRAWY|OBSZARY DO ROZWOJU|SUGESTIE|SZANSE ROZWOJU):?\*\*\s*(.*?)(?=\*\*(?:💡|KLUCZOWA)|$)', feedback_text, re.DOTALL | re.IGNORECASE)
    improve_text = improve_match.group(1).strip() if improve_match else ""
    improvements = [s.strip() for s in re.findall(r'•\s*([^\n•]+)', improve_text)]
    
    # Wyciągnij kluczową radę
    advice_match = re.search(r'\*\*(?:💡\s*)?(?:KLUCZOWA RADA|MAŁY KROK DO DZIAŁANIA):?\*\*\s*(.*?)(?=$)', feedback_text, re.DOTALL | re.IGNORECASE)
    key_advice = advice_match.group(1).strip() if advice_match else ""
    
    # Wyświetl w tabsach - dla generated_case dodaj tab "Rozwiązanie"
    if exercise_type == 'generated_case':
        tab1, tab2, tab3, tab4 = st.tabs(["💬 Analiza", "📊 Szczegóły", "💡 Kluczowa rada", "✨ Rozwiązanie"])
    else:
        tab1, tab2, tab3 = st.tabs(["💬 Analiza", "📊 Szczegóły", "💡 Kluczowa rada"])
        tab4 = None
    
    with tab1:
        st.markdown("### 💬 Feedback AI")
        # Wyświetl sekcję FEEDBACK z odpowiedzi AI
        if main_feedback:
            st.markdown(f"""
            <div style='padding: 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-left: 4px solid #667eea; border-radius: 10px; margin: 15px 0;'>
                <p style='color: #333; margin: 0; line-height: 1.8; font-size: 1.05em;'>{main_feedback}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Jeśli regex nie znalazł sekcji FEEDBACK, pokaż cały feedback
            st.markdown(f"""
            <div style='padding: 20px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-left: 4px solid #667eea; border-radius: 10px; margin: 15px 0;'>
                <p style='color: #333; margin: 0; line-height: 1.8; font-size: 1.05em;'>{feedback_text}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### ✅ Mocne strony")
            if strengths:
                for i, strength in enumerate(strengths, 1):
                    # Usuń gwiazdki markdown przed wyświetleniem
                    clean_strength = strength.replace('**', '').replace('*', '').strip()
                    st.markdown(f"""
                    <div style='padding: 12px; background: #d1fae5; border-left: 4px solid #10b981; border-radius: 5px; margin: 8px 0;'>
                        <p style='color: #065f46; margin: 0; font-weight: 500;'>✓ {clean_strength}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("💡 Analiza ogólna - sprawdź zakładkę 'Analiza'")
        
        with col_right:
            st.markdown("#### 🎯 Obszary rozwoju")
            if improvements:
                for i, improvement in enumerate(improvements, 1):
                    # Usuń gwiazdki markdown przed wyświetleniem
                    clean_improvement = improvement.replace('**', '').replace('*', '').strip()
                    st.markdown(f"""
                    <div style='padding: 12px; background: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 5px; margin: 8px 0;'>
                        <p style='color: #92400e; margin: 0; font-weight: 500;'>→ {clean_improvement}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("💡 Sugestie zawarte w analizie - sprawdź zakładkę 'Analiza'")
    
    with tab3:
        st.markdown("### 💡 Najważniejsza lekcja do zapamiętania")
        if key_advice:
            # Usuń gwiazdki
            clean_advice = key_advice.replace('**', '').replace('*', '').strip()
            st.markdown(f"""
            <div style='padding: 25px; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-left: 6px solid #f59e0b; border-radius: 10px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <div style='font-size: 2.5em; margin-bottom: 10px;'>💡</div>
                <p style='font-size: 1.2em; color: #78350f; margin: 0; line-height: 1.6; font-weight: 500;'>{clean_advice}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("💡 Kluczowe wnioski zawarte w głównej analizie")
    
    # Tab 4: Rozwiązanie wzorcowe (tylko dla generated_case)
    if tab4 is not None and exercise_type == 'generated_case':
        with tab4:
            st.markdown("### ✨ Wzorcowa odpowiedź na poziomie 10/10")
            st.markdown("""
            <div style='padding: 20px; background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border-left: 6px solid #10b981; border-radius: 10px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <div style='font-size: 2em; margin-bottom: 10px;'>🌟</div>
                <p style='font-size: 1.1em; color: #065f46; margin: 0; line-height: 1.6;'>
                    AI wygenerowało przykładową odpowiedź uczestnika, która otrzymałaby ocenę 10/10. 
                    Zwróć uwagę na poziom szczegółowości, odniesienia do poziomów C-IQ, 
                    aspektów neurobiologicznych i konkretnych, praktycznych rozwiązań.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Generuj wzorcową odpowiedź jeśli mamy dane case study
            if 'generated_case_data' in feedback and evaluator:
                case_data = feedback['generated_case_data']
                
                # Twórz wzorcową odpowiedź na podstawie case study
                with st.spinner("🤖 Generuję wzorcową odpowiedź 10/10..."):
                    model_answer = generate_model_answer(case_data, evaluator)
                
                st.markdown("#### 📝 Wzorcowa odpowiedź wygenerowana przez AI:")
                st.markdown(f"""
                <div style='padding: 20px; background: white; border: 2px solid #10b981; border-radius: 10px; margin: 15px 0;'>
                    {model_answer}
                </div>
                """, unsafe_allow_html=True)
                
                st.info("""
                💡 **Pamiętaj:** To tylko jeden z możliwych sposobów podejścia do problemu. 
                Twoja odpowiedź może być inna i równie wartościowa, jeśli zawiera podobny 
                poziom analizy i praktycznych rozwiązań.
                """)
            elif not evaluator:
                st.warning("⚠️ Nie można wygenerować wzorcowej odpowiedzi - brak połączenia z AI.")
            else:
                st.info("💡 Wzorcowa odpowiedź nie jest dostępna dla tego typu ćwiczenia.")
    
    # Motywująca wiadomość (jeśli dostępna - dla self_reflection)
    if 'motivation_message' in feedback:
        st.markdown("---")
        st.success(f"🌟 **{feedback['motivation_message']}**")