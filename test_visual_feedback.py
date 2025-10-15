"""Test wizualnej prezentacji feedbacku"""
import streamlit as st
from utils.ai_exercises import AIExerciseEvaluator, display_ai_feedback

# Konfiguracja strony
st.set_page_config(page_title="Test Feedbacku AI", page_icon="🎯")

st.title("🎯 Test Wizualizacji Feedbacku AI")
st.markdown("---")

# Utwórz evaluator
evaluator = AIExerciseEvaluator()

# Wybór typu ćwiczenia
exercise_type = st.selectbox(
    "Wybierz typ ćwiczenia:",
    ["level_identification", "case_analysis", "self_reflection", "conversation_simulation"]
)

# Przykładowe odpowiedzi
sample_responses = {
    "level_identification": "poziom 3, komunikat my i wzrost adrenaliny",
    "case_analysis": "Menedżer powinien zacząć od aktywnego słuchania i pytań otwartych, aby zespół mógł wyrazić swoje obawy. Następnie wspólnie wypracować rozwiązania wykorzystując język poziomu III - my, razem, wspólnie.",
    "self_reflection": "Zauważyłem, że często przerywam innym i narzucam swoje rozwiązania. Chcę nauczyć się lepiej słuchać i zadawać więcej pytań otwartych.",
    "conversation_simulation": "Rozpocząłbym od uznania emocji zespołu i zbudowania bezpiecznej przestrzeni. Następnie użył pytań otwartych aby wspólnie wypracować rozwiązania."
}

user_response = st.text_area(
    "Twoja odpowiedź:",
    value=sample_responses[exercise_type],
    height=100
)

if st.button("🤖 Otrzymaj feedback AI", type="primary"):
    with st.spinner("AI analizuje Twoją odpowiedź..."):
        ai_config = {
            'exercise_type': exercise_type,
            'feedback_criteria': ['Jakość analizy', 'Zastosowanie C-IQ'],
            'assessment_rubric': {}
        }
        
        result = evaluator.evaluate_exercise(ai_config, user_response, 'Conversational Intelligence')
        
        st.markdown("---")
        st.markdown("## 📊 Feedback AI")
        
        # Wyświetl używając nowej funkcji
        display_ai_feedback(result)

st.markdown("---")
st.caption("💡 Test nowej wizualizacji feedbacku AI - kategorie w tabsach, ładne karty, wypunktowania")
