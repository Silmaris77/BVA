"""
Milwaukee Application First™ Tool
4-poziomowy wizard: Kontekst → Pytania → Aplikacja → Rekomendacja
"""

import streamlit as st
import json
import os
from utils.milwaukee_recommender import get_recommender
from datetime import datetime

def milwaukee_application_engine():
    """Główny widok Application Engine"""
    
    st.title("🔴 Milwaukee Application First™ Tool")
    st.markdown("**Sprzedajemy rozwiązania do pracy, nie tylko narzędzia.**")
    st.markdown("---")
    
    # Inicjalizacja session state
    if 'ae_step' not in st.session_state:
        st.session_state.ae_step = 1
    if 'ae_context' not in st.session_state:
        st.session_state.ae_context = {}
    if 'ae_selected_app' not in st.session_state:
        st.session_state.ae_selected_app = None
    if 'ae_answers' not in st.session_state:
        st.session_state.ae_answers = {}
    if 'ae_recommendation' not in st.session_state:
        st.session_state.ae_recommendation = None
    
    recommender = get_recommender()
    
    # Progress bar
    progress_steps = ["Kontekst", "Aplikacja", "Pytania pogłębiające", "Rekomendacja"]
    current_step = st.session_state.ae_step
    
    cols = st.columns(4)
    for idx, step_name in enumerate(progress_steps, 1):
        with cols[idx-1]:
            if idx < current_step:
                st.success(f"✅ {step_name}")
            elif idx == current_step:
                st.info(f"▶️ {step_name}")
            else:
                st.text(f"⏹️ {step_name}")
    
    st.markdown("---")
    
    # POZIOM 1: KONTEKST KLIENTA
    if st.session_state.ae_step == 1:
        show_context_step(recommender)
    
    # POZIOM 2: WYBÓR APLIKACJI
    elif st.session_state.ae_step == 2:
        show_application_selection_step(recommender)
    
    # POZIOM 3: PYTANIA POGŁĘBIAJĄCE
    elif st.session_state.ae_step == 3:
        show_discovery_questions_step(recommender)
    
    # POZIOM 4: REKOMENDACJA + SKRYPT
    elif st.session_state.ae_step == 4:
        show_recommendation_step(recommender)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.ae_step > 1:
            if st.button("⬅️ Wstecz"):
                st.session_state.ae_step -= 1
                st.rerun()
    
    with col3:
        if st.button("🔄 Restart"):
            st.session_state.ae_step = 1
            st.session_state.ae_context = {}
            st.session_state.ae_selected_app = None
            st.session_state.ae_answers = {}
            st.session_state.ae_recommendation = None
            st.rerun()


def show_context_step(recommender):
    """POZIOM 1: Zbieranie kontekstu klienta (4 zmienne)"""
    
    st.header("1️⃣ Kontekst klienta")
    st.markdown("**Nie zaczynamy od produktu. Zaczynamy od zrozumienia pracy klienta.**")
    
    questions_data = recommender.questions.get('context_questions', {})
    
    # Typ klienta
    st.subheader("🎯 " + questions_data['typ_klienta']['question'])
    typ_klienta_options = {opt['value']: f"{opt['label']} - {opt['description']}" 
                           for opt in questions_data['typ_klienta']['options']}
    
    typ_klienta = st.selectbox(
        "Wybierz profil:",
        options=list(typ_klienta_options.keys()),
        format_func=lambda x: typ_klienta_options[x],
        key='typ_klienta_select'
    )
    
    # Typ pracy
    st.subheader("⚙️ " + questions_data['typ_pracy']['question'])
    typ_pracy_options = {opt['value']: f"{opt['label']} - {opt['description']}" 
                         for opt in questions_data['typ_pracy']['options']}
    
    typ_pracy = st.selectbox(
        "Wybierz charakter pracy:",
        options=list(typ_pracy_options.keys()),
        format_func=lambda x: typ_pracy_options[x],
        key='typ_pracy_select'
    )
    
    # Materiały/środowisko (multi-select)
    st.subheader("🔨 " + questions_data['materialy_srodowisko']['question'])
    material_options = {opt['value']: opt['label'] 
                        for opt in questions_data['materialy_srodowisko']['options']}
    
    materialy = st.multiselect(
        "Wybierz materiały/środowisko (możesz wybrać kilka):",
        options=list(material_options.keys()),
        format_func=lambda x: material_options[x],
        key='materialy_select'
    )
    
    # Pokaż implications dla wybranych materiałów
    if materialy:
        st.info("**To oznacza że potrzebne będą:**")
        all_implications = []
        for material in materialy:
            for opt in questions_data['materialy_srodowisko']['options']:
                if opt['value'] == material:
                    all_implications.extend(opt.get('implications', []))
        
        for impl in set(all_implications):
            st.markdown(f"- {impl}")
    
    # Skala działalności
    st.subheader("👥 " + questions_data['skala']['question'])
    skala_options = {opt['value']: f"{opt['label']} - {', '.join(opt.get('implications', []))}" 
                     for opt in questions_data['skala']['options']}
    
    skala = st.selectbox(
        "Wybierz skalę:",
        options=list(skala_options.keys()),
        format_func=lambda x: skala_options[x],
        key='skala_select'
    )
    
    # Zapisz kontekst i przejdź dalej
    if st.button("Dalej ➡️", type="primary", use_container_width=True):
        if not materialy:
            st.error("Wybierz przynajmniej jeden materiał/środowisko!")
        else:
            st.session_state.ae_context = {
                'typ_klienta': typ_klienta,
                'typ_pracy': typ_pracy,
                'materialy_srodowisko': materialy,
                'skala': skala
            }
            st.session_state.ae_step = 2
            st.rerun()


def show_application_selection_step(recommender):
    """POZIOM 2: Wybór aplikacji na podstawie kontekstu"""
    
    st.header("2️⃣ Dopasowane aplikacje")
    st.markdown("**Na podstawie kontekstu klienta, proponujemy następujące aplikacje:**")
    
    # Pokaż podsumowanie kontekstu
    with st.expander("📋 Podsumowanie kontekstu klienta"):
        ctx = st.session_state.ae_context
        st.write(f"**Typ klienta:** {ctx.get('typ_klienta', 'N/A')}")
        st.write(f"**Typ pracy:** {ctx.get('typ_pracy', 'N/A')}")
        st.write(f"**Materiały/środowisko:** {', '.join(ctx.get('materialy_srodowisko', []))}")
        st.write(f"**Skala:** {ctx.get('skala', 'N/A')}")
    
    # Dopasuj aplikacje
    matches = recommender.match_application(st.session_state.ae_context)
    
    if not matches:
        st.warning("Nie znaleziono dopasowanych aplikacji dla tego kontekstu.")
        st.info("Spróbuj zmienić kryteria lub skontaktuj się z supportem Milwaukee.")
        return
    
    st.success(f"Znaleziono {len(matches)} dopasowanych aplikacji")
    
    # Wyświetl dopasowania jako karty
    for idx, (app_id, score, reason) in enumerate(matches, 1):
        app_data = recommender.get_application_details(app_id)
        
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"{app_data.get('icon', '🔧')} {app_data.get('title', app_id)}")
                st.caption(f"**Dopasowanie:** {score:.0f}%")
                st.write(f"*{reason}*")
                
                # Charakterystyka aplikacji
                st.markdown("**Charakterystyka:**")
                for char in app_data.get('charakterystyka', [])[:3]:  # Pierwsze 3
                    st.markdown(f"- {char}")
            
            with col2:
                if st.button(f"Wybierz", key=f"select_app_{app_id}", use_container_width=True):
                    st.session_state.ae_selected_app = app_id
                    st.session_state.ae_step = 3
                    st.rerun()
            
            st.markdown("---")


def show_discovery_questions_step(recommender):
    """POZIOM 3: Inteligentne pytania pogłębiające"""
    
    st.header("3️⃣ Pytania pogłębiające")
    
    app_id = st.session_state.ae_selected_app
    app_data = recommender.get_application_details(app_id)
    
    st.markdown(f"**Aplikacja:** {app_data.get('icon', '🔧')} {app_data.get('title', app_id)}")
    st.markdown("**Te pytania pomogą doprecyzować rekomendację i zbudować przekaz sprzedażowy.**")
    st.markdown("---")
    
    # Pobierz pytania dla typu klienta
    typ_klienta = st.session_state.ae_context.get('typ_klienta', '')
    questions = recommender.get_discovery_questions(typ_klienta)
    
    if not questions:
        st.warning("Brak pytań pogłębiających dla tego typu klienta.")
        if st.button("Pomiń i przejdź do rekomendacji ➡️", type="primary"):
            st.session_state.ae_step = 4
            st.rerun()
        return
    
    # Wyświetl pytania
    answers = {}
    
    for idx, question in enumerate(questions, 1):
        st.subheader(f"Pytanie {idx}/{len(questions)}")
        st.write(f"**{question.get('question', '')}**")
        st.caption(f"*Cel: {question.get('purpose', '')}*")
        
        q_type = question.get('type', 'choice')
        q_id = question.get('id', f'q_{idx}')
        
        if q_type == 'scale':
            scale_options = question.get('scale', [])
            answer = st.radio(
                "Wybierz odpowiedź:",
                options=scale_options,
                key=f'answer_{q_id}'
            )
            answers[q_id] = answer
        
        elif q_type == 'choice':
            choice_options = question.get('options', [])
            answer = st.selectbox(
                "Wybierz odpowiedź:",
                options=choice_options,
                key=f'answer_{q_id}'
            )
            answers[q_id] = answer
        
        elif q_type == 'multi_choice':
            choice_options = question.get('options', [])
            answer = st.multiselect(
                "Wybierz odpowiedzi (możesz wybrać kilka):",
                options=choice_options,
                key=f'answer_{q_id}'
            )
            answers[q_id] = answer
        
        elif q_type == 'yes_no':
            yes_no_options = question.get('options', ['Tak', 'Nie'])
            answer = st.radio(
                "Wybierz odpowiedź:",
                options=yes_no_options,
                key=f'answer_{q_id}'
            )
            answers[q_id] = answer
        
        elif q_type == 'number':
            answer = st.number_input(
                "Podaj liczbę:",
                min_value=0,
                step=1,
                key=f'answer_{q_id}'
            )
            answers[q_id] = str(answer)
        
        st.markdown("---")
    
    # Zapisz odpowiedzi i przejdź dalej
    if st.button("Generuj rekomendację ➡️", type="primary", use_container_width=True):
        st.session_state.ae_answers = answers
        st.session_state.ae_step = 4
        st.rerun()


def show_recommendation_step(recommender):
    """POZIOM 4: Rekomendacja + Skrypt perswazyjny"""
    
    st.header("4️⃣ Rekomendacja systemowa")
    
    app_id = st.session_state.ae_selected_app
    app_data = recommender.get_application_details(app_id)
    
    st.markdown(f"**Aplikacja:** {app_data.get('icon', '🔧')} {app_data.get('title', app_id)}")
    
    # Oblicz scoring produktów na podstawie odpowiedzi
    product_scores = recommender.calculate_product_scores(st.session_state.ae_answers)
    
    # Zbuduj pakiet rekomendacji
    package = recommender.build_recommendation_package(app_id, product_scores)
    
    st.markdown("---")
    
    # Tabs: Pakiet | Skrypt | ROI | Case Study
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Pakiet produktów", "💬 Skrypt perswazyjny", "💰 Kalkulator ROI", "🏆 Case Studies"])
    
    with tab1:
        show_product_package(package, app_data)
    
    with tab2:
        show_persuasion_script(recommender, app_id, app_data)
    
    with tab3:
        show_roi_calculator(recommender, app_id)
    
    with tab4:
        show_case_studies(recommender, app_id)
    
    # Akcje końcowe
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 After Visit", use_container_width=True):
            st.session_state.ae_show_after_visit = True
            st.rerun()
    
    with col2:
        if st.button("📄 Eksportuj PDF", use_container_width=True):
            st.info("Funkcja eksportu PDF w przygotowaniu...")
    
    with col3:
        if st.button("📧 Wyślij email", use_container_width=True):
            st.info("Funkcja wysyłki email w przygotowaniu...")
    
    with col4:
        if st.button("💾 Zapisz wizytę", use_container_width=True):
            save_visit_record(app_id, package)
    
    # After Visit Mode
    if st.session_state.get('ae_show_after_visit', False):
        st.markdown("---")
        from views.milwaukee_after_visit import show_after_visit_mode
        show_after_visit_mode()
        
        if st.button("⬅️ Powrót do rekomendacji"):
            st.session_state.ae_show_after_visit = False
            st.rerun()


def show_product_package(package, app_data):
    """Wyświetl pakiet produktów"""
    
    st.subheader(f"🎯 {app_data.get('persuasion_script', {}).get('headline', 'Kompletne rozwiązanie')}")
    
    # Narzędzia
    if package.get('narzedzia'):
        st.markdown("### 🔧 Narzędzia główne")
        for tool in sorted(package['narzedzia'], key=lambda x: x.get('priority', 999)):
            with st.expander(f"**{tool['name']}** - {tool['price']} PLN"):
                st.write(f"**Dlaczego:** {tool['reason']}")
                st.write("**Cechy:**")
                for feature in tool.get('features', [])[:3]:
                    st.markdown(f"- {feature}")
                st.write("**Korzyści:**")
                for benefit in tool.get('benefits', []):
                    st.markdown(f"✅ {benefit}")
    
    # Baterie
    if package.get('baterie'):
        st.markdown("### 🔋 Baterie")
        for battery in package['baterie']:
            st.write(f"**{battery['name']}** x {battery['quantity']} = {battery['price']} PLN")
            st.caption(f"↳ {battery['reason']}")
    
    # Akcesoria
    if package.get('akcesoria'):
        st.markdown("### 🛠️ Akcesoria")
        for acc in package['akcesoria']:
            st.write(f"**{acc['name']}** - {acc['price']} PLN")
            st.caption(f"↳ {acc['reason']}")
    
    # Organizacja
    if package.get('organizacja'):
        st.markdown("### 📦 Organizacja (PACKOUT)")
        for org in package['organizacja']:
            st.write(f"**{org['name']}** - {org['price']} PLN")
            st.caption(f"↳ {org['reason']}")
    
    # PPE
    if package.get('ppe'):
        st.markdown("### 🦺 PPE / Dodatki")
        for ppe in package['ppe']:
            st.write(f"**{ppe['name']}** - {ppe['price']} PLN")
            st.caption(f"↳ {ppe['reason']}")
    
    # Podsumowanie cenowe
    st.markdown("---")
    total = package.get('total_price', 0)
    st.metric("💵 Wartość pakietu", f"{total:,} PLN".replace(',', ' '))
    
    # Check if bundle exists
    from utils.milwaukee_recommender import get_recommender
    bundle = get_recommender().get_bundle_for_application(st.session_state.ae_selected_app)
    if bundle:
        savings = bundle.get('savings_pln', 0)
        bundle_price = bundle.get('bundle_price_pln', 0)
        st.success(f"🎁 **Zestaw promocyjny:** {bundle_price:,} PLN (oszczędność {savings} PLN)".replace(',', ' '))


def show_persuasion_script(recommender, app_id, app_data):
    """Wyświetl skrypt perswazyjny"""
    
    script = recommender.get_persuasion_script(app_id)
    
    if not script:
        st.info("Brak skryptu perswazyjnego dla tej aplikacji.")
        return
    
    st.subheader("💬 Struktura rozmowy sprzedażowej")
    
    # Headline
    st.markdown(f"### 🎯 Przekaz główny")
    st.info(f"**\"{script.get('headline', '')}\"**")
    
    # Problem
    st.markdown("### ❌ Problem (język klienta)")
    st.write(script.get('problem', ''))
    
    # Consequence
    st.markdown("### ⚠️ Konsekwencja")
    st.write(script.get('consequence', ''))
    
    # Solution
    st.markdown("### ✅ Rozwiązanie")
    st.write(script.get('solution', ''))
    
    # Benefits
    st.markdown("### 🎁 Korzyści operacyjne")
    for benefit in script.get('benefits', []):
        st.markdown(f"- **{benefit}**")
    
    # Proof
    st.markdown("### 📊 Dowód / Case")
    st.success(script.get('proof', ''))
    
    # Objection handling
    if script.get('objection_handling'):
        st.markdown("### 🛡️ Obsługa obiekcji")
        objections = script.get('objection_handling', {})
        
        for objection, response in objections.items():
            with st.expander(f"Obiekcja: \"{objection}\""):
                st.write(f"**Odpowiedź:** {response}")
    
    # Next step
    st.markdown("### 🎯 Następny krok (Call to Action)")
    st.info(f"**\"{script.get('next_step', '')}\"**")


def show_roi_calculator(recommender, app_id):
    """Wyświetl kalkulator ROI"""
    
    roi_data = recommender.get_roi_calculator(app_id)
    
    if not roi_data:
        st.info("Kalkulator ROI w przygotowaniu dla tej aplikacji.")
        return
    
    st.subheader("💰 Zwrot z inwestycji (ROI)")
    
    # Podstawowe dane
    time_savings = roi_data.get('time_savings_per_job', 0)
    time_unit = roi_data.get('time_unit', 'minut')
    jobs_increase = roi_data.get('jobs_per_week_increase', 0)
    avg_job_value = roi_data.get('avg_job_value', 0)
    investment = roi_data.get('investment', 0)
    payback_months = roi_data.get('payback_months', 0)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Oszczędność czasu/zlecenie", f"{time_savings} {time_unit}")
    
    with col2:
        st.metric("Dodatkowe zlecenia/tydzień", f"+{jobs_increase}")
    
    with col3:
        st.metric("Zwrot inwestycji", f"{payback_months} miesięcy")
    
    st.markdown("---")
    
    # Interaktywny kalkulator
    st.markdown("### 🧮 Dostosuj do swojego klienta")
    
    custom_job_value = st.number_input(
        "Średnia wartość zlecenia (PLN):",
        min_value=100,
        max_value=10000,
        value=avg_job_value,
        step=100
    )
    
    custom_jobs_increase = st.slider(
        "Dodatkowe zlecenia miesięcznie:",
        min_value=0,
        max_value=20,
        value=int(jobs_increase * 4)
    )
    
    # Oblicz ROI
    monthly_revenue_increase = custom_job_value * custom_jobs_increase
    calculated_payback = investment / monthly_revenue_increase if monthly_revenue_increase > 0 else 999
    
    st.markdown("### 📈 Wynik")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Dodatkowy przychód/mc", f"{monthly_revenue_increase:,} PLN".replace(',', ' '))
    
    with col2:
        st.metric("Dodatkowy przychód/rok", f"{monthly_revenue_increase * 12:,} PLN".replace(',', ' '))
    
    with col3:
        st.metric("Zwrot inwestycji", f"{calculated_payback:.1f} miesięcy")
    
    if calculated_payback < 6:
        st.success("✅ Bardzo dobry ROI - inwestycja zwróci się w mniej niż 6 miesięcy!")
    elif calculated_payback < 12:
        st.info("ℹ️ Dobry ROI - zwrot w ciągu roku")
    else:
        st.warning("⚠️ Długi okres zwrotu - może warto dostosować ofertę?")


def show_case_studies(recommender, app_id):
    """Wyświetl case studies"""
    
    case_studies = recommender.get_case_studies(app_id)
    
    if not case_studies:
        st.info("Case studies w przygotowaniu dla tej aplikacji.")
        return
    
    st.subheader("🏆 Prawdziwe przykłady z rynku")
    
    for idx, case in enumerate(case_studies, 1):
        with st.container():
            st.markdown(f"### Case Study #{idx}: {case.get('customer', 'Klient')}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**❌ Problem:**")
                st.write(case.get('problem', ''))
                
                st.markdown("**✅ Rozwiązanie:**")
                st.write(case.get('solution', ''))
            
            with col2:
                st.markdown("**📊 Rezultaty:**")
                st.success(case.get('results', ''))
                
                st.markdown("**💬 Cytat:**")
                st.info(f'"{case.get("quote", "")}"')
            
            st.markdown("---")


def save_visit_record(app_id, package):
    """Zapisz rekord wizyty do historii"""
    
    # Struktura zapisu wizyty
    visit_record = {
        'timestamp': datetime.now().isoformat(),
        'user': st.session_state.get('username', 'Unknown'),
        'application_id': app_id,
        'context': st.session_state.ae_context,
        'answers': st.session_state.ae_answers,
        'recommended_package': package,
        'total_value': package.get('total_price', 0)
    }
    
    # Zapisz do pliku (tutaj można rozszerzyć o bazę danych)
    visits_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'milwaukee', 'visits')
    os.makedirs(visits_dir, exist_ok=True)
    
    filename = f"visit_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{st.session_state.get('username', 'unknown')}.json"
    filepath = os.path.join(visits_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(visit_record, f, ensure_ascii=False, indent=2)
        
        st.success(f"✅ Wizyta zapisana! Plik: {filename}")
        st.info("Możesz teraz użyć tego rekordu do analizy lub follow-up z klientem.")
    except Exception as e:
        st.error(f"Błąd zapisu: {e}")


if __name__ == "__main__":
    milwaukee_application_engine()
