"""
Moduł do obsługi pytań otwartych z oceną AI w systemie BVA
"""

import streamlit as st
from typing import Dict, List, Tuple
import json
import re

try:
    from openai import OpenAI
    openai_available = True
except ImportError:
    openai_available = False

class AIQuestionEvaluator:
    """Klasa do oceny odpowiedzi na pytania otwarte przy użyciu AI"""
    
    def __init__(self):
        # Sprawdź czy klucz API jest dostępny
        self.api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, 'secrets') else None
        if not self.api_key or not openai_available:
            st.warning("🔑 Klucz API OpenAI nie jest skonfigurowany lub biblioteka OpenAI nie jest zainstalowana. Pytania otwarte będą działać w trybie demo.")
            self.demo_mode = True
        else:
            self.demo_mode = False
            self.client = OpenAI(api_key=self.api_key)
    
    def evaluate_answer(self, question: str, user_answer: str, correct_answer: str, 
                       context: str = "", max_score: int = 10) -> Dict:
        """
        Ocenia odpowiedź użytkownika na pytanie otwarte
        
        Args:
            question: Treść pytania
            user_answer: Odpowiedź użytkownika
            correct_answer: Wzorcowa odpowiedź lub kluczowe punkty
            context: Kontekst lekcji/tematu
            max_score: Maksymalna liczba punktów
            
        Returns:
            Dict z oceną, feedbackiem i szczegółami
        """
        
        if self.demo_mode:
            return self._demo_evaluation(user_answer, max_score)
        
        try:
            prompt = self._create_evaluation_prompt(question, user_answer, correct_answer, context, max_score)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Jesteś ekspertem w dziedzinie neuroprzywództwa i edukatorem. Twoim zadaniem jest sprawiedliwa i konstruktywna ocena odpowiedzi uczniów."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            result = self._parse_ai_response(response.choices[0].message.content, max_score)
            return result
            
        except Exception as e:
            st.error(f"Błąd podczas oceny odpowiedzi: {str(e)}")
            return self._fallback_evaluation(user_answer, max_score)
    
    def _create_evaluation_prompt(self, question: str, user_answer: str, 
                                correct_answer: str, context: str, max_score: int) -> str:
        """Tworzy prompt dla AI do oceny odpowiedzi"""
        
        return f"""
Oceń następującą odpowiedź ucznia na pytanie z zakresu neuroprzywództwa:

KONTEKST LEKCJI: {context}

PYTANIE: {question}

ODPOWIEDŹ UCZNIA: {user_answer}

WZORCOWA ODPOWIEDŹ/KLUCZOWE PUNKTY: {correct_answer}

Oceń odpowiedź w skali 0-{max_score} punktów uwzględniając:
1. Poprawność merytoryczną (50%)
2. Kompletność odpowiedzi (30%) 
3. Zrozumienie konceptów (20%)

Podaj ocenę w formacie JSON:
{{
    "score": [liczba 0-{max_score}],
    "feedback": "[konstruktywny feedback dla ucznia]",
    "strong_points": "[co uczeń zrobił dobrze]",
    "areas_for_improvement": "[co można poprawić]",
    "suggestions": "[konkretne sugestie do dalszej nauki]"
}}

Uwagi:
- Bądź sprawiedliwy ale wymagający
- Doceniaj częściowo poprawne odpowiedzi
- Daj konstruktywny feedback
- Używaj języka polskiego
- Jeśli odpowiedź jest bardzo krótka lub niejasna, wskaż to delikatnie
"""
    
    def _parse_ai_response(self, response: str, max_score: int) -> Dict:
        """Parsuje odpowiedź AI i zwraca ustrukturyzowany wynik"""
        
        try:
            # Spróbuj sparsować JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                
                # Walidacja i normalizacja
                score = min(max(int(result.get('score', 0)), 0), max_score)
                
                return {
                    'score': score,
                    'max_score': max_score,
                    'percentage': (score / max_score) * 100,
                    'feedback': result.get('feedback', 'Brak szczegółowego feedbacku'),
                    'strong_points': result.get('strong_points', ''),
                    'areas_for_improvement': result.get('areas_for_improvement', ''),
                    'suggestions': result.get('suggestions', ''),
                    'passed': score >= (max_score * 0.6)  # 60% to zaliczenie
                }
        except:
            pass
        
        # Fallback parsing jeśli JSON nie działa
        return self._fallback_evaluation(response, max_score)
    
    def _demo_evaluation(self, user_answer: str, max_score: int) -> Dict:
        """Tryb demo - prosta ocena bez AI"""
        
        # Prosta heurystyka na podstawie długości odpowiedzi
        answer_length = len(user_answer.strip())
        
        if answer_length < 10:
            score = 2
            feedback = "Odpowiedź jest bardzo krótka. Spróbuj rozwinąć swoją myśl i podać więcej szczegółów."
        elif answer_length < 50:
            score = 4
            feedback = "Dobry początek! Twoja odpowiedź zawiera podstawowe informacje, ale można ją rozszerzyć o więcej szczegółów."
        elif answer_length < 150:
            score = 7
            feedback = "Bardzo dobra odpowiedź! Wykazujesz zrozumienie tematu. Można by jeszcze dodać przykłady praktyczne."
        else:
            score = 9
            feedback = "Doskonała, szczegółowa odpowiedź! Wykazujesz głębokie zrozumienie zagadnienia."
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': (score / max_score) * 100,
            'feedback': feedback + " (Tryb demo - pełna ocena AI wymaga konfiguracji API)",
            'strong_points': "Dobra struktura odpowiedzi",
            'areas_for_improvement': "Spróbuj dodać więcej przykładów praktycznych",
            'suggestions': "Poszukaj dodatkowych źródeł na temat neuroprzywództwa",
            'passed': score >= (max_score * 0.6)
        }
    
    def _fallback_evaluation(self, text: str, max_score: int) -> Dict:
        """Fallback w przypadku błędu AI"""
        
        score = max_score // 2  # Połowa punktów jako fallback
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': 50.0,
            'feedback': "Dziękujemy za odpowiedź. Ocena automatyczna nie jest obecnie dostępna.",
            'strong_points': "Podjąłeś próbę odpowiedzi",
            'areas_for_improvement': "Sprawdź materiały lekcyjne",
            'suggestions': "Skonsultuj się z instruktorem",
            'passed': True  # W trybie fallback zaliczamy
        }


def display_open_question(question_data: Dict, question_id: str) -> Tuple[bool, Dict]:
    """
    Wyświetla pytanie otwarte z oceną AI
    
    Args:
        question_data: Dane pytania (question, correct_answer, context, itp.)
        question_id: Unikalny identyfikator pytania
        
    Returns:
        Tuple (czy odpowiedziano, wynik oceny)
    """
    
    st.markdown(f"""
    <div class="open-question-container">
        <h4>💭 {question_data.get('question', 'Pytanie')}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Sprawdź czy pytanie już zostało odpowiedziane
    result_key = f"{question_id}_result"
    answer_key = f"{question_id}_answer"
    
    if result_key in st.session_state:
        # Wyświetl poprzedni wynik
        result = st.session_state[result_key]
        prev_answer = st.session_state.get(answer_key, "")
        
        st.markdown('<div class="question-completed">', unsafe_allow_html=True)
        st.success(f"✅ Pytanie zostało już odpowiedziane! Otrzymałeś {result['score']}/{result['max_score']} punktów ({result['percentage']:.1f}%)")
        
        with st.expander("🔍 Zobacz swoją odpowiedź i ocenę"):
            st.markdown("**Twoja odpowiedź:**")
            st.info(prev_answer)
            
            st.markdown("**Feedback:**")
            st.markdown(result['feedback'])
            
            if result['strong_points']:
                st.markdown("**✅ Mocne strony:**")
                st.markdown(result['strong_points'])
            
            if result['areas_for_improvement']:
                st.markdown("**🎯 Obszary do poprawy:**")
                st.markdown(result['areas_for_improvement'])
            
            if result['suggestions']:
                st.markdown("**💡 Sugestie:**")
                st.markdown(result['suggestions'])
        
        # Przycisk ponownej próby
        if st.button("🔄 Spróbuj ponownie", key=f"{question_id}_retry"):
            del st.session_state[result_key]
            if answer_key in st.session_state:
                del st.session_state[answer_key]
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        return True, result
    
    # Wyświetl pole do wprowadzenia odpowiedzi
    if question_data.get('context'):
        st.markdown(f"**Kontekst:** {question_data['context']}")
    
    if question_data.get('hints'):
        with st.expander("💡 Wskazówki"):
            for hint in question_data['hints']:
                st.markdown(f"• {hint}")
    
    user_answer = st.text_area(
        "Twoja odpowiedź:",
        height=150,
        placeholder="Napisz swoją odpowiedź tutaj...",
        key=f"{question_id}_input",
        help="Postaraj się odpowiedzieć szczegółowo i podać przykłady jeśli to możliwe."
    )
    
    # Przycisk wysłania odpowiedzi
    if st.button("📤 Wyślij odpowiedź", key=f"{question_id}_submit", disabled=not user_answer.strip()):
        if user_answer.strip():
            # Oceń odpowiedź
            evaluator = AIQuestionEvaluator()
            
            with st.spinner("🤖 AI analizuje Twoją odpowiedź..."):
                result = evaluator.evaluate_answer(
                    question=question_data.get('question', ''),
                    user_answer=user_answer,
                    correct_answer=question_data.get('correct_answer', ''),
                    context=question_data.get('context', ''),
                    max_score=question_data.get('max_score', 10)
                )
            
            # Zapisz wynik
            st.session_state[result_key] = result
            st.session_state[answer_key] = user_answer
            
            st.rerun()
        else:
            st.warning("Proszę napisać odpowiedź przed wysłaniem.")
    
    return False, {}


# Style CSS dla pytań otwartych
def load_open_question_styles():
    """Ładuje style CSS dla pytań otwartych"""
    
    st.markdown("""
    <style>
    .open-question-container {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 5px solid #4A90E2;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.1);
    }
    
    .open-question-container h4 {
        color: #2c5aa0;
        margin: 0;
        font-size: 1.3em;
    }
    
    .question-completed {
        background: linear-gradient(135deg, #f0fff0 0%, #e6ffe6 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.1);
    }
    
    .stTextArea textarea {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 15px;
    }
    
    .stTextArea textarea:focus {
        border-color: #4A90E2;
        box-shadow: 0 0 10px rgba(74, 144, 226, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)
