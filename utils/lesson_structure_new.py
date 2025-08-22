# utils/lesson_structure_new.py
"""
Nowa 6-etapowa struktura lekcji oparta na prototypie:
1. Wstęp
2. Opening Case Study  
3. Quiz Samooceny
4. Materiał
5. Closing Case Study
6. Podsumowanie
"""

import streamlit as st
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from data.lessons import get_lesson_data
from data.users import load_user_data, save_user_data

class LessonStructureNew:
    """Nowa 6-etapowa struktura lekcji"""
    
    def __init__(self):
        self.stages = [
            {
                "id": "intro",
                "name": "🎯 Wstęp", 
                "description": "Wprowadzenie do tematu",
                "type": "content"
            },
            {
                "id": "opening_case",
                "name": "📖 Opening Case Study",
                "description": "Praktyczny przykład na start", 
                "type": "case_study"
            },
            {
                "id": "self_assessment",
                "name": "❓ Quiz Samooceny", 
                "description": "Sprawdź swoją wiedzę",
                "type": "quiz"
            },
            {
                "id": "main_content",
                "name": "📚 Materiał",
                "description": "Główna treść lekcji",
                "type": "content"
            },
            {
                "id": "closing_case", 
                "name": "🔍 Closing Case Study",
                "description": "Zastosowanie w praktyce",
                "type": "case_study"
            },
            {
                "id": "summary",
                "name": "📝 Podsumowanie",
                "description": "Kluczowe wnioski", 
                "type": "summary"
            }
        ]
    
    def render_lesson_progress_stepper(self, lesson_id: str, current_stage: int = 0):
        """Renderuje progress stepper dla lekcji"""
        st.markdown("### 📊 Postęp Lekcji")
        
        # Progress bar
        progress = (current_stage + 1) / len(self.stages)
        st.progress(progress)
        
        # Stage indicators
        cols = st.columns(len(self.stages))
        
        for i, stage in enumerate(self.stages):
            with cols[i]:
                if i < current_stage:
                    # Completed stage
                    st.markdown(
                        f"<div style='text-align: center; color: #27ae60;'>"
                        f"<div style='font-size: 24px;'>✅</div>"
                        f"<div style='font-size: 12px;'>{stage['name']}</div>"
                        f"</div>", 
                        unsafe_allow_html=True
                    )
                elif i == current_stage:
                    # Current stage
                    st.markdown(
                        f"<div style='text-align: center; color: #3498db;'>"
                        f"<div style='font-size: 24px;'>🔄</div>" 
                        f"<div style='font-size: 12px; font-weight: bold;'>{stage['name']}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                else:
                    # Future stage
                    st.markdown(
                        f"<div style='text-align: center; color: #95a5a6;'>"
                        f"<div style='font-size: 24px;'>⭕</div>"
                        f"<div style='font-size: 12px;'>{stage['name']}</div>"
                        f"</div>",
                        unsafe_allow_html=True  
                    )
        
        st.markdown("---")
    
    def get_lesson_progress(self, lesson_id: str) -> int:
        """Zwraca aktualny etap lekcji dla użytkownika"""
        username = st.session_state.get('username', 'default_user')
        users_data = load_user_data()
        user_data = users_data.get(username, {})
        
        lesson_progress = user_data.get('lesson_progress', {})
        return lesson_progress.get(lesson_id, {}).get('current_stage', 0)
    
    def update_lesson_progress(self, lesson_id: str, stage: int):
        """Aktualizuje postęp lekcji użytkownika"""
        username = st.session_state.get('username', 'default_user')
        users_data = load_user_data()
        
        if username not in users_data:
            users_data[username] = {}
        
        if 'lesson_progress' not in users_data[username]:
            users_data[username]['lesson_progress'] = {}
        
        if lesson_id not in users_data[username]['lesson_progress']:
            users_data[username]['lesson_progress'][lesson_id] = {}
        
        users_data[username]['lesson_progress'][lesson_id]['current_stage'] = stage
        users_data[username]['lesson_progress'][lesson_id]['last_updated'] = datetime.now().isoformat()
        
        # If completed all stages, mark as completed
        if stage >= len(self.stages):
            users_data[username]['lesson_progress'][lesson_id]['completed'] = True
            users_data[username]['lesson_progress'][lesson_id]['completed_at'] = datetime.now().isoformat()
            
            # Award XP for lesson completion
            current_xp = users_data[username].get('xp', 0)
            lesson_xp = 100  # Base XP for lesson completion
            users_data[username]['xp'] = current_xp + lesson_xp
        
        save_user_data(users_data)
    
    def render_stage_content(self, lesson_id: str, stage_id: str):
        """Renderuje zawartość konkretnego etapu"""
        stage_info = next((s for s in self.stages if s['id'] == stage_id), None)
        if not stage_info:
            st.error("Nieznany etap lekcji")
            return
        
        st.markdown(f"## {stage_info['name']}")
        st.markdown(f"*{stage_info['description']}*")
        
        if stage_info['type'] == 'content':
            self._render_content_stage(lesson_id, stage_id)
        elif stage_info['type'] == 'case_study':
            self._render_case_study_stage(lesson_id, stage_id)
        elif stage_info['type'] == 'quiz':
            self._render_quiz_stage(lesson_id, stage_id)
        elif stage_info['type'] == 'summary':
            self._render_summary_stage(lesson_id, stage_id)
    
    def _render_content_stage(self, lesson_id: str, stage_id: str):
        """Renderuje etap z treścią"""
        # Load lesson content
        try:
            lesson_data = get_lesson_data(lesson_id)
            
            if stage_id == 'intro':
                content = lesson_data.get('intro', 'Wprowadzenie do lekcji...')
            elif stage_id == 'main_content':
                content = lesson_data.get('content', 'Główna treść lekcji...')
            else:
                content = "Treść w przygotowaniu..."
            
            st.markdown(content)
            
        except Exception as e:
            st.error(f"Błąd ładowania treści: {e}")
            st.markdown("**Przykładowa treść lekcji**")
            st.markdown("""
            To jest przykład nowej struktury lekcji. W tym miejscu będzie:
            - 📖 Szczegółowe wyjaśnienia
            - 💡 Praktyczne wskazówki  
            - 📊 Wykresy i przykłady
            - 🎯 Kluczowe punkty do zapamiętania
            """)
    
    def _render_case_study_stage(self, lesson_id: str, stage_id: str):
        """Renderuje etap case study"""
        st.markdown("**📋 Case Study**")
        
        # Example case study content
        with st.container(border=True):
            st.markdown("#### 🏢 Przykład: Analiza Spółki XYZ")
            
            if stage_id == 'opening_case':
                st.markdown("""
                **Sytuacja:** 
                Spółka XYZ notowana na GPW, sektor technologiczny, ostatni wzrost ceny o 25% w miesiąc.
                
                **Pytanie:** 
                Czy to dobry moment na wejście? Co byś sprawdził jako pierwszy?
                """)
                
                # Interactive element
                user_response = st.text_area(
                    "Twoja pierwsza analiza:",
                    placeholder="Napisz co byś sprawdził w pierwszej kolejności...",
                    key=f"opening_case_{lesson_id}"
                )
                
                if user_response and len(user_response) > 20:
                    st.success("✅ Dobra obserwacja! Sprawdźmy to razem w dalszej części lekcji.")
            
            elif stage_id == 'closing_case':
                st.markdown("""
                **Teraz po przejściu materiału:**
                Mając wiedzę z lekcji, przeanalizuj ponownie spółkę XYZ.
                
                **Zastosuj nauczone koncepty:**
                1. Wskaźniki fundamentalne
                2. Analiza techniczna  
                3. Ocena ryzyka
                """)
                
                # More advanced interactive element
                col1, col2 = st.columns(2)
                with col1:
                    fundamental_score = st.slider("Ocena fundamentalna (1-10)", 1, 10, 5, key=f"fund_{lesson_id}")
                with col2:
                    technical_score = st.slider("Ocena techniczna (1-10)", 1, 10, 5, key=f"tech_{lesson_id}")
                
                final_decision = st.radio(
                    "Twoja decyzja:",
                    ["Kupuję", "Sprzedaję", "Czekam", "Potrzebuję więcej danych"],
                    key=f"decision_{lesson_id}"
                )
                
                if st.button("Sprawdź swoją analizę", key=f"check_analysis_{lesson_id}"):
                    st.info(f"Twoja ocena: Fund={fundamental_score}, Tech={technical_score}, Decyzja={final_decision}")
                    st.success("🎯 Świetnie! Zastosowałeś systematyczne podejście do analizy.")
    
    def _render_quiz_stage(self, lesson_id: str, stage_id: str):
        """Renderuje etap quizu samooceny"""
        st.markdown("**❓ Quiz Samooceny**")
        st.markdown("*Sprawdź swoją obecną wiedzę przed przejściem do materiału*")
        
        # Sample quiz questions
        questions = [
            {
                "question": "Co to jest analiza fundamentalna?",
                "options": [
                    "Analiza wykresów cenowych",
                    "Ocena wartości wewnętrznej spółki",
                    "Śledzenie nastrojów rynku", 
                    "Analiza wolumenów transakcji"
                ],
                "correct": 1,
                "explanation": "Analiza fundamentalna ocenia rzeczywistą wartość spółki na podstawie danych finansowych."
            },
            {
                "question": "Który wskaźnik pokazuje rentowność spółki?",
                "options": [
                    "P/E",
                    "ROE", 
                    "P/B",
                    "Debt/Equity"
                ],
                "correct": 1,
                "explanation": "ROE (Return on Equity) pokazuje jak efektywnie spółka wykorzystuje kapitał własny."
            }
        ]
        
        user_answers = []
        
        for i, q in enumerate(questions):
            st.markdown(f"**Pytanie {i+1}:** {q['question']}")
            
            answer = st.radio(
                f"Wybierz odpowiedź:",
                q['options'],
                key=f"quiz_{lesson_id}_{stage_id}_{i}",
                index=None
            )
            
            user_answers.append(answer)
        
        if st.button("Sprawdź odpowiedzi", key=f"check_quiz_{lesson_id}_{stage_id}"):
            correct_count = 0
            
            for i, (q, user_answer) in enumerate(zip(questions, user_answers)):
                if user_answer is not None:
                    is_correct = q['options'].index(user_answer) == q['correct']
                    if is_correct:
                        correct_count += 1
                        st.success(f"✅ Pytanie {i+1}: {user_answer} - POPRAWNE!")
                    else:
                        correct_answer = q['options'][q['correct']]
                        st.error(f"❌ Pytanie {i+1}: {user_answer} - NIEPOPRAWNE. Poprawna odpowiedź: {correct_answer}")
                    
                    st.info(f"💡 {q['explanation']}")
            
            score = (correct_count / len(questions)) * 100
            st.markdown(f"### 🎯 Twój wynik: {score:.0f}%")
            
            if score >= 70:
                st.success("🎉 Świetnie! Masz dobrą podstawę do tej lekcji.")
            elif score >= 50:
                st.warning("⚠️ Nieźle, ale zwróć uwagę na materiał.")
            else:
                st.info("📚 Nie martw się - po lekcji będziesz ekspertem!")
    
    def _render_summary_stage(self, lesson_id: str, stage_id: str):
        """Renderuje etap podsumowania"""
        st.markdown("**📝 Podsumowanie Lekcji**")
        
        # Key takeaways
        with st.container(border=True):
            st.markdown("#### 🎯 Kluczowe Wnioski")
            st.markdown("""
            1. **Analiza fundamentalna** to ocena rzeczywistej wartości spółki
            2. **Kluczowe wskaźniki** to P/E, ROE, P/B, Debt/Equity
            3. **Systematyczne podejście** daje lepsze rezultaty niż emocjonalne decyzje
            4. **Zawsze** sprawdzaj multiple sources przed podjęciem decyzji
            """)
        
        # Personal notes
        st.markdown("#### 📋 Twoje Notatki")
        personal_notes = st.text_area(
            "Co najbardziej Ci się przydało z tej lekcji?",
            placeholder="Zapisz swoje przemyślenia, pytania lub plany zastosowania...",
            key=f"notes_{lesson_id}"
        )
        
        if personal_notes:
            if st.button("💾 Zapisz notatkę", key=f"save_notes_{lesson_id}"):
                # Save notes to user data
                username = st.session_state.get('username', 'default_user')
                users_data = load_user_data()
                
                if 'lesson_notes' not in users_data[username]:
                    users_data[username]['lesson_notes'] = {}
                
                users_data[username]['lesson_notes'][lesson_id] = {
                    'content': personal_notes,
                    'created_at': datetime.now().isoformat()
                }
                
                save_user_data(users_data)
                st.success("📝 Notatka zapisana!")
        
        # Next steps
        st.markdown("#### 🚀 Następne Kroki")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📚 Następna Lekcja", key=f"next_lesson_{lesson_id}"):
                st.success("Przechodzimy do kolejnej lekcji!")
                # Here you would implement navigation to next lesson
        
        with col2:
            if st.button("⚡ Przejdź do Praktyki", key=f"go_practice_{lesson_id}"):
                st.session_state.current_section = 'practice'
                st.rerun()
    
    def render_complete_lesson(self, lesson_id: str):
        """Renderuje kompletną lekcję z wszystkimi etapami"""
        current_stage = self.get_lesson_progress(lesson_id)
        
        # Render progress stepper
        self.render_lesson_progress_stepper(lesson_id, current_stage)
        
        # Current stage content
        if current_stage < len(self.stages):
            stage = self.stages[current_stage]
            self.render_stage_content(lesson_id, stage['id'])
            
            # Navigation buttons
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if current_stage > 0:
                    if st.button("⬅️ Poprzedni", key=f"prev_{lesson_id}"):
                        self.update_lesson_progress(lesson_id, current_stage - 1)
                        st.rerun()
            
            with col3:
                if current_stage < len(self.stages) - 1:
                    if st.button("Następny ➡️", key=f"next_{lesson_id}"):
                        self.update_lesson_progress(lesson_id, current_stage + 1)
                        st.rerun()
                else:
                    if st.button("🎉 Ukończ Lekcję", key=f"complete_{lesson_id}"):
                        self.update_lesson_progress(lesson_id, len(self.stages))
                        st.success("🎓 Gratulacje! Lekcja ukończona!")
                        st.balloons()
                        st.rerun()
        else:
            # Lesson completed
            st.success("🎓 Lekcja Ukończona!")
            st.markdown("### 🎉 Gratulacje!")
            st.markdown("Ukończyłeś wszystkie etapy tej lekcji. Czas na praktykę!")
            
            if st.button("🚀 Przejdź do Praktyki", key=f"completed_practice_{lesson_id}"):
                st.session_state.current_section = 'practice'
                st.rerun()

# Initialize lesson structure
def get_lesson_structure():
    """Zwraca instancję nowej struktury lekcji"""
    if 'lesson_structure' not in st.session_state:
        st.session_state.lesson_structure = LessonStructureNew()
    return st.session_state.lesson_structure
