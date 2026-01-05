"""
Milwaukee Application Engine - After Visit Mode
Feedback loop dla poprawy rekomendacji i skills development
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, List

def show_after_visit_mode():
    """
    Tryb post-wizyta: Feedback na temat faktycznej wizyty
    Pomaga identyfikować luki w discovery i doskonalić podejście
    """
    
    st.header("📋 After Visit Report")
    st.markdown("**Wypełnij ten formularz po wizycie u klienta, aby doskonalić swoje podejście Application First.**")
    st.markdown("---")
    
    # Sprawdź czy mamy zapisaną rekomendację
    if not st.session_state.get('ae_recommendation'):
        st.warning("Brak danych rekomendacji. Wróć do Application Engine i przejdź przez pełny proces najpierw.")
        return
    
    app_id = st.session_state.get('ae_selected_app', '')
    context = st.session_state.get('ae_context', {})
    
    st.subheader(f"Wizyta: {context.get('typ_klienta', 'Klient')}")
    st.caption(f"Aplikacja: {app_id}")
    
    # SEKCJA 1: Co się faktycznie wydarzyło?
    st.markdown("### 1️⃣ Faktyczny przebieg wizyty")
    
    visit_happened = st.radio(
        "Czy wizyta się odbyła?",
        options=["Tak", "Nie - klient odwołał", "Nie - przełożona"],
        key='visit_happened'
    )
    
    if visit_happened == "Tak":
        visit_date = st.date_input("Data wizyty:", datetime.now())
        visit_duration = st.number_input("Czas trwania (min):", min_value=5, max_value=300, value=45)
        
        # SEKCJA 2: Weryfikacja kontekstu
        st.markdown("### 2️⃣ Czy kontekst klienta był trafny?")
        
        context_accurate = st.radio(
            "Czy początkowy kontekst (typ klienta, materiały, skala) był poprawny?",
            options=["Tak, 100%", "Częściowo - były różnice", "Nie - zupełnie inaczej"],
            key='context_accurate'
        )
        
        if context_accurate != "Tak, 100%":
            context_diff = st.text_area(
                "Czym różniła się rzeczywistość od założeń?",
                placeholder="Np. Klient deklarował pracę w betonie, ale 80% to cegła...",
                key='context_diff'
            )
        
        # SEKCJA 3: Aplikacja - trafność
        st.markdown("### 3️⃣ Czy aplikacja była trafiona?")
        
        application_match = st.radio(
            "Czy wybrana aplikacja odpowiadała faktycznym potrzebom klienta?",
            options=["Tak - idealnie", "Tak - w 70-80%", "Częściowo - trzeba było dostosować", "Nie - inna aplikacja była lepsza"],
            key='app_match'
        )
        
        if application_match == "Nie - inna aplikacja była lepsza":
            better_app = st.text_input("Jaka aplikacja byłaby lepsza?", key='better_app')
        
        # SEKCJA 4: Discovery - pytania
        st.markdown("### 4️⃣ Ocena pytań discovery")
        
        st.write("**Które pytania pogłębiające zadałeś?**")
        
        answers = st.session_state.get('ae_answers', {})
        questions_asked = st.multiselect(
            "Zaznacz pytania, które faktycznie zadałeś:",
            options=list(answers.keys()),
            key='questions_asked'
        )
        
        additional_questions = st.text_area(
            "Jakie dodatkowe pytania zadałeś (nie z listy)?",
            placeholder="Np. Pytałem o budżet, o poprzednie doświadczenia z narzędziami...",
            key='additional_questions'
        )
        
        most_valuable_question = st.selectbox(
            "Które pytanie dało najcenniejsze informacje?",
            options=[''] + list(answers.keys()) + ['Moje własne pytanie'],
            key='most_valuable_q'
        )
        
        # SEKCJA 5: Produkty - co faktycznie zaproponowałeś?
        st.markdown("### 5️⃣ Produkty i rekomendacja")
        
        package = st.session_state.get('ae_recommendation', {})
        all_skus = []
        
        for category in ['narzedzia', 'baterie', 'akcesoria', 'organizacja', 'ppe']:
            items = package.get(category, [])
            for item in items:
                all_skus.append(f"{item.get('name', item.get('sku', 'Unknown'))} ({category})")
        
        products_presented = st.multiselect(
            "Które produkty faktycznie zaprezentowałeś?",
            options=all_skus,
            key='products_presented'
        )
        
        products_missing = st.text_area(
            "Jakich produktów brakowało w rekomendacji (które powinny być)?",
            placeholder="Np. Klient potrzebował piły, której nie było w pakiecie...",
            key='products_missing'
        )
        
        products_unnecessary = st.text_area(
            "Które produkty z pakietu były niepotrzebne dla tego klienta?",
            placeholder="Np. PACKOUT był za drogi dla tego typu klienta...",
            key='products_unnecessary'
        )
        
        # SEKCJA 6: Skrypt perswazyjny - co zadziałało?
        st.markdown("### 6️⃣ Skuteczność przekazu")
        
        script_used = st.radio(
            "Czy użyłeś skryptu perswazyjnego z narzędzia?",
            options=["Tak - prawie 1:1", "Częściowo - własnym słowami", "Nie - miałem własne podejście"],
            key='script_used'
        )
        
        if script_used in ["Tak - prawie 1:1", "Częściowo - własnym słowami"]:
            script_effectiveness = st.slider(
                "Jak skuteczny był skrypt? (1-10)",
                min_value=1,
                max_value=10,
                value=7,
                key='script_effectiveness'
            )
            
            script_feedback = st.text_area(
                "Co działało najlepiej? Co zmienić?",
                placeholder="Np. Przekaz o oszczędności czasu zadziałał świetnie, ale klient nie przejmował się ROI...",
                key='script_feedback'
            )
        
        # SEKCJA 7: Obiekcje
        st.markdown("### 7️⃣ Obiekcje klienta")
        
        objections = st.multiselect(
            "Jakie obiekcje zgłosił klient?",
            options=[
                "To jest drogie",
                "Mam już inne narzędzia",
                "Nie potrzebuję tak dużo",
                "Czy M12 wystarczy?",
                "Baterie się rozładują",
                "Wolę pneumatykę",
                "Muszę pomyśleć",
                "Nie mam budżetu",
                "Inne (wpisz poniżej)"
            ],
            key='objections'
        )
        
        if "Inne (wpisz poniżej)" in objections:
            other_objection = st.text_input("Jakie inne obiekcje?", key='other_objection')
        
        objection_handled = st.radio(
            "Czy udało się obsłużyć obiekcje?",
            options=["Tak - wszystkie", "Częściowo", "Nie - klient nie był przekonany"],
            key='objection_handled'
        )
        
        # SEKCJA 8: Rezultat
        st.markdown("### 8️⃣ Rezultat wizyty")
        
        outcome = st.selectbox(
            "Jaki był wynik wizyty?",
            options=[
                "Sprzedaż - zamknięta na miejscu",
                "Oferta wysłana - czekamy na decyzję",
                "Klient zainteresowany - follow-up",
                "Klient musi pomyśleć - brak konkretów",
                "Klient nie był zainteresowany",
                "Wizyta odkryta inne potrzeby - inna oferta"
            ],
            key='outcome'
        )
        
        if outcome in ["Sprzedaż - zamknięta na miejscu", "Oferta wysłana - czekamy na decyzję"]:
            sold_value = st.number_input(
                "Wartość sprzedaży/oferty (PLN):",
                min_value=0,
                step=100,
                key='sold_value'
            )
            
            sold_products = st.text_area(
                "Jakie produkty sprzedano/zaoferowano?",
                placeholder="Lista SKU lub nazw produktów...",
                key='sold_products'
            )
        
        # SEKCJA 9: Samoocena i wnioski
        st.markdown("### 9️⃣ Twoja samoocena")
        
        self_rating = st.slider(
            "Jak oceniasz swoją wizytę? (1-10)",
            min_value=1,
            max_value=10,
            value=7,
            key='self_rating'
        )
        
        what_went_well = st.text_area(
            "Co poszło dobrze?",
            placeholder="Np. Dobrze zidentyfikowałem główny pain point...",
            key='what_went_well'
        )
        
        what_to_improve = st.text_area(
            "Co poprawić na przyszłość?",
            placeholder="Np. Powinienem zadać więcej pytań o budżet...",
            key='what_to_improve'
        )
        
        # SEKCJA 10: System suggestions (auto-generated)
        st.markdown("### 🤖 Sugestie systemowe")
        
        suggestions = generate_suggestions(
            context_accurate,
            application_match,
            script_effectiveness if script_used != "Nie - miałem własne podejście" else None,
            outcome
        )
        
        for suggestion in suggestions:
            st.info(f"💡 {suggestion}")
        
        # Zapisz feedback
        st.markdown("---")
        if st.button("💾 Zapisz feedback", type="primary", use_container_width=True):
            save_after_visit_feedback({
                'visit_happened': visit_happened,
                'visit_date': str(visit_date),
                'visit_duration': visit_duration,
                'context_accurate': context_accurate,
                'context_diff': locals().get('context_diff', ''),
                'application_match': application_match,
                'better_app': locals().get('better_app', ''),
                'questions_asked': questions_asked,
                'additional_questions': additional_questions,
                'most_valuable_question': most_valuable_question,
                'products_presented': products_presented,
                'products_missing': products_missing,
                'products_unnecessary': products_unnecessary,
                'script_used': script_used,
                'script_effectiveness': locals().get('script_effectiveness', None),
                'script_feedback': locals().get('script_feedback', ''),
                'objections': objections,
                'other_objection': locals().get('other_objection', ''),
                'objection_handled': objection_handled,
                'outcome': outcome,
                'sold_value': locals().get('sold_value', 0),
                'sold_products': locals().get('sold_products', ''),
                'self_rating': self_rating,
                'what_went_well': what_went_well,
                'what_to_improve': what_to_improve,
                'suggestions': suggestions
            })


def generate_suggestions(context_accurate, app_match, script_effectiveness, outcome):
    """Generuj automatyczne sugestie na podstawie feedbacku"""
    suggestions = []
    
    # Sugestie dotyczące kontekstu
    if context_accurate == "Nie - zupełnie inaczej":
        suggestions.append("Rozważ dodatkowe pytania pre-wizyta (call/email) aby lepiej zrozumieć kontekst przed spotkaniem.")
    elif context_accurate == "Częściowo - były różnice":
        suggestions.append("Spróbuj zadawać więcej pytań otwartych na początku spotkania, aby zweryfikować założenia.")
    
    # Sugestie dotyczące aplikacji
    if app_match in ["Częściowo - trzeba było dostosować", "Nie - inna aplikacja była lepsza"]:
        suggestions.append("Podczas discovery zadaj pytanie: 'Jakie 3 najczęstsze zadania wykonujesz?' - może to wcześniej wykryć mismatch.")
    
    # Sugestie dotyczące skryptu
    if script_effectiveness and script_effectiveness < 6:
        suggestions.append("Niski rating skryptu - skup się na słuchaniu klienta i dostosuj przekaz do jego języka, nie odwrotnie.")
    
    # Sugestie dotyczące outcome
    if outcome == "Klient nie był zainteresowany":
        suggestions.append("Brak zainteresowania może oznaczać niedopasowanie aplikacji lub brak zidentyfikowania prawdziwego pain point.")
    elif outcome == "Klient musi pomyśleć - brak konkretów":
        suggestions.append("Spróbuj konkretnego CTA: 'Czy chciałby Pan przetestować to narzędzie przez tydzień?' zamiast ogólnej oferty.")
    
    return suggestions if suggestions else ["Świetna robota! Wizyta przebiegła zgodnie z planem."]


def save_after_visit_feedback(feedback_data: Dict):
    """Zapisz feedback do pliku"""
    
    # Dodaj metadata
    feedback_data['timestamp'] = datetime.now().isoformat()
    feedback_data['user'] = st.session_state.get('username', 'Unknown')
    feedback_data['application_id'] = st.session_state.get('ae_selected_app', '')
    feedback_data['original_context'] = st.session_state.get('ae_context', {})
    feedback_data['original_recommendation'] = st.session_state.get('ae_recommendation', {})
    
    # Zapisz do pliku
    feedback_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'data', 'milwaukee', 'feedback'
    )
    os.makedirs(feedback_dir, exist_ok=True)
    
    filename = f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{st.session_state.get('username', 'unknown')}.json"
    filepath = os.path.join(feedback_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, ensure_ascii=False, indent=2)
        
        st.success(f"✅ Feedback zapisany! Plik: {filename}")
        st.info("Twój feedback pomoże nam doskonalić Application Engine i szkolenia.")
        
        # Opcjonalnie - wyświetl podsumowanie
        with st.expander("📊 Podsumowanie feedback"):
            st.json(feedback_data)
    
    except Exception as e:
        st.error(f"Błąd zapisu feedback: {e}")


if __name__ == "__main__":
    show_after_visit_mode()
