import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go
import math
from datetime import datetime, timedelta
from pathlib import Path
import time
import json
import secrets
import string
# Importy są OK tutaj - lazy loading jest w samym users_new
from data.users_sql import load_user_data, save_user_data
from data.lessons import load_lessons
from utils.scroll_utils import scroll_to_top
from data.neuroleader_test_questions import NEUROLEADER_TYPES
from config.settings import XP_LEVELS
from utils.material3_components import apply_material3_theme
from utils.components import zen_header, zen_button, notification, data_chart, stat_card
from utils.layout import get_device_type, responsive_grid, toggle_device_view
from utils.permissions import load_company_templates, get_available_companies

def check_admin_auth():
    """Sprawdza uwierzytelnienie administratora"""

    # Oryginalna kontrola uprawnień (zakomentowana na czas testów)
    if not st.session_state.get('logged_in', False):
        st.error("Musisz być zalogowany, aby uzyskać dostęp do panelu administratora.")
        return False
       
    admin_users = ["admin", "zenmaster", "Anna", "Max"]  # Dodaj swój login
    if st.session_state.get('username') not in admin_users:
        st.error("Nie masz uprawnień do przeglądania panelu administratora.")
        return False
       
    return True

def get_user_activity_data():
    """Pobiera i przetwarza dane o aktywności użytkowników"""
    users_data = load_user_data()
    
    # Przygotuj dane do analizy
    activity_data = []
    for username, data in users_data.items():        activity_data.append({
            'username': username,
            'xp': data.get('xp', 0),
            'level': data.get('level', 1),
            'completed_lessons': len(data.get('completed_lessons', [])),
            'neuroleader_type': data.get('neuroleader_type', 'Nieznany'),
            'registration_date': data.get('joined_date', 'Nieznana'),  # Poprawione: używamy joined_date
            'last_login': data.get('last_login') or 'Nigdy',           # Lepsze formatowanie dla brakujących danych
            'test_taken': data.get('test_taken', False),
            'completed_missions': len(data.get('completed_missions', [])),
            'streak': data.get('streak', 0)
        })
    
    return pd.DataFrame(activity_data)

def get_lessons_stats():
    """Pobiera i analizuje statystyki lekcji"""
    users_data = load_user_data()
    lessons = load_lessons()
    
    # Inicjalizuj liczniki ukończeń dla każdej lekcji
    completion_count = {lesson_id: 0 for lesson_id in lessons.keys()}
    
    # Zlicz ukończenia lekcji
    for username, data in users_data.items():
        completed_lessons = data.get('completed_lessons', [])
        for lesson_id in completed_lessons:
            if lesson_id in completion_count:
                completion_count[lesson_id] += 1
    
    # Utwórz DataFrame ze statystykami lekcji
    lessons_stats = []
    for lesson_id, lesson in lessons.items():
        lessons_stats.append({
            'lesson_id': lesson_id,
            'title': lesson.get('title', 'Brak tytułu'),
            'category': lesson.get('tag', 'Brak kategorii'),
            'difficulty': lesson.get('difficulty', 'intermediate'),
            'completions': completion_count.get(lesson_id, 0),
            'completion_rate': round(completion_count.get(lesson_id, 0) / len(users_data) * 100, 2) if users_data else 0
        })
    
    return pd.DataFrame(lessons_stats)

def get_neuroleader_type_distribution():
    """Analizuje rozkład typów neuroliderów wśród użytkowników"""
    users_data = load_user_data()
    
    # Zlicz wystąpienia każdego typu neurolidera
    neuroleader_counts = {}
    for _, data in users_data.items():
        neuroleader_type = data.get('neuroleader_type', 'Nieznany')
        neuroleader_counts[neuroleader_type] = neuroleader_counts.get(neuroleader_type, 0) + 1
    
    # Utwórz DataFrame dla wizualizacji
    neuroleader_distribution = []
    for neuroleader_type, count in neuroleader_counts.items():
        neuroleader_distribution.append({
            'neuroleader_type': neuroleader_type,
            'count': count,
            'percentage': round(count / len(users_data) * 100, 2) if users_data else 0
        })
    
    return pd.DataFrame(neuroleader_distribution)

def plot_user_activity_over_time():
    """Generuje wykres aktywności użytkowników w czasie na podstawie rzeczywistych danych"""
    users_data = load_user_data()
    
    # Pobierz rzeczywiste daty z ostatnich 30 dni
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    
    # Inicjalizuj liczniki dla rejestracji i logowań
    registrations = {date: 0 for date in dates}
    logins = {date: 0 for date in dates}
    
    # Zlicz rzeczywistą aktywność na podstawie danych użytkowników
    for username, user_data in users_data.items():
        # 1. Zlicz rejestracje w ostatnich 30 dniach
        joined_date = user_data.get('joined_date')
        if joined_date and joined_date in registrations:
            registrations[joined_date] += 1
        
        # 2. Zlicz ostatnie logowania w ostatnich 30 dniach
        last_login = user_data.get('last_login')
        if last_login:
            # Wyciągnij datę z datetime string (format: "2025-06-26 14:30:15")
            try:
                login_date = last_login.split(' ')[0]  # Weź tylko część z datą
                if login_date in logins:
                    logins[login_date] += 1
            except (AttributeError, IndexError, ValueError):
                # Ignoruj nieprawidłowe formaty dat
                pass
    
    # Odwróć daty, aby najnowsze były na końcu
    dates.reverse()
    
    # Utwórz DataFrame z oddzielnymi kolumnami dla rejestracji i logowań
    activity_df = pd.DataFrame({
        'data': dates,
        'rejestracje': [registrations[date] for date in dates],
        'logowania': [logins[date] for date in dates],
        'łącznie': [registrations[date] + logins[date] for date in dates]
    })
    
    return activity_df


def delete_user_completely(username: str) -> bool:
    """
    Usuwa użytkownika całkowicie - z JSON i SQL
    
    Args:
        username: Nazwa użytkownika do usunięcia
        
    Returns:
        bool: True jeśli usunięto z SQL i JSON, False jeśli tylko z JSON
    """
    sql_success = False
    json_success = False
    
    # 1. Usuń z SQL (jeśli dostępny)
    try:
        from database.models import User, BusinessGame
        from database.connection import session_scope
        
        with session_scope() as session:
            # Znajdź użytkownika
            user = session.query(User).filter_by(username=username).first()
            
            if user:
                # CASCADE usuwa automatycznie:
                # - lesson_progress
                # - completed_lessons
                # - lesson_access
                # - business_games (wraz z employees, contracts, transactions, stats)
                session.delete(user)
                session.commit()
                sql_success = True
                print(f"✅ Usunięto użytkownika '{username}' z SQL")
            else:
                print(f"ℹ️  Użytkownik '{username}' nie istnieje w SQL")
                sql_success = True  # Nie ma w SQL = sukces
                
    except Exception as e:
        print(f"⚠️  Nie udało się usunąć z SQL: {e}")
        sql_success = False
    
    # 2. Usuń z JSON
    try:
        users_data = load_user_data()
        
        if username in users_data:
            users_data.pop(username, None)
            save_user_data(users_data)
            json_success = True
            print(f"✅ Usunięto użytkownika '{username}' z JSON")
        else:
            print(f"ℹ️  Użytkownik '{username}' nie istnieje w JSON")
            json_success = True  # Nie ma w JSON = sukces
            
    except Exception as e:
        print(f"❌ Błąd podczas usuwania z JSON: {e}")
        json_success = False
    
    return sql_success and json_success

def generate_password(length=12):
    """Generuje losowe hasło"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def create_user_form():
    """Formularz tworzenia nowego użytkownika z uprawnieniami"""
    
    # Get available companies
    companies = get_available_companies()
    company_options = [comp['name'] for comp in companies]
    company_codes = {comp['name']: comp['code'] for comp in companies}
    
    # Load templates for preview
    templates = load_company_templates()
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_username = st.text_input("Nazwa użytkownika", key="new_user_username", 
                                     help="Login użytkownika (unikalny)")
        
        # Password generation
        if 'generated_password' not in st.session_state:
            st.session_state.generated_password = generate_password()
        
        password_col1, password_col2 = st.columns([3, 1])
        with password_col1:
            new_password = st.text_input("Hasło", value=st.session_state.generated_password, 
                                        type="password", key="new_user_password")
        with password_col2:
            if st.button("🔄 Generuj", key="regenerate_password"):
                st.session_state.generated_password = generate_password()
                st.rerun()
        
        # Show password checkbox
        if st.checkbox("Pokaż hasło", key="show_password"):
            st.code(new_password)
    
    with col2:
        selected_company_name = st.selectbox("Firma", options=company_options, 
                                             key="new_user_company")
        selected_company_code = company_codes.get(selected_company_name)
        
        # Preview template
        if selected_company_code:
            template = templates.get(selected_company_code, {})
            st.info(f"📋 Szablon: **{selected_company_name}**")
            
            # Show summary
            content = template.get('content', {})
            tools = template.get('tools', {})
            ranking = template.get('ranking', {})
            
            st.caption(f"✓ Lekcje: {len(content.get('lessons', [])) if content.get('lessons') else 'Wszystkie'}")
            st.caption(f"✓ BG Scenariusze: {len(content.get('business_games', {}).get('scenarios', [])) if content.get('business_games', {}).get('scenarios') else 'Wszystkie'}")
            st.caption(f"✓ Ranking: {ranking.get('scope', 'global')}")
    
    # Advanced settings
    with st.expander("⚙️ Zaawansowane ustawienia (opcjonalne)"):
        st.markdown("**Dostosuj uprawnienia** (jeśli puste - użyje szablonu firmy)")
        
        custom_permissions = st.checkbox("Niestandardowe uprawnienia", key="custom_permissions")
        
        if custom_permissions:
            st.warning("⚠️ Włączono tryb niestandardowy - szablon firmy zostanie zignorowany")
            
            # Tools access
            st.markdown("**Dostęp do narzędzi:**")
            tools_cols = st.columns(3)
            
            custom_tools = {}
            tool_list = ['dashboard', 'profile', 'learn', 'inspirations', 'practice', 
                        'business_games', 'shop', 'personality_tests', 'rankings', 'notes']
            
            for idx, tool in enumerate(tool_list):
                with tools_cols[idx % 3]:
                    custom_tools[tool] = st.checkbox(tool.replace('_', ' ').title(), 
                                                     value=True, key=f"tool_{tool}")
            
            # Content access
            st.markdown("**Dostęp do treści:**")
            lessons_input = st.text_area("ID Lekcji (po przecinku)", 
                                        placeholder="intro_1, leadership_2, sales_3",
                                        key="custom_lessons")
            
            scenarios_input = st.text_area("ID Scenariuszy BG (po przecinku)", 
                                          placeholder="consulting_1, fmcg_heinz",
                                          key="custom_scenarios")
            
            # Ranking settings
            st.markdown("**Ustawienia rankingu:**")
            ranking_scope = st.radio("Tryb rankingu", 
                                    options=['none', 'company', 'global'],
                                    key="custom_ranking_scope")
            
            visible_in_global = st.checkbox("Widoczny w globalnym rankingu", 
                                           value=True, key="custom_visible_global")
    
    # Create button
    st.markdown("---")
    if st.button("✅ Utwórz konto", type="primary", use_container_width=True):
        # Validation
        if not new_username:
            st.error("Podaj nazwę użytkownika")
            return
        
        if not new_password or len(new_password) < 6:
            st.error("Hasło musi mieć minimum 6 znaków")
            return
        
        # Check if user exists
        users_data = load_user_data()
        if new_username in users_data:
            st.error(f"Użytkownik '{new_username}' już istnieje")
            return
        
        # Build permissions
        if custom_permissions:
            # Custom permissions
            lessons_list = [l.strip() for l in lessons_input.split(',')] if lessons_input else None
            scenarios_list = [s.strip() for s in scenarios_input.split(',')] if scenarios_input else None
            
            permissions = {
                'content': {
                    'lessons': lessons_list,
                    'tests': None,
                    'business_games': {
                        'scenarios': scenarios_list,
                        'types': None
                    },
                    'inspirations': None
                },
                'tools': custom_tools,
                'ranking': {
                    'scope': ranking_scope,
                    'visible_in_global': visible_in_global
                }
            }
        else:
            # Use company template
            template = templates.get(selected_company_code, templates.get('_default', {}))
            permissions = {
                'content': template.get('content', {}),
                'tools': template.get('tools', {}),
                'ranking': template.get('ranking', {})
            }
        
        # Create new user
        try:
            from database.models import User
            from database.connection import session_scope
            import uuid
            
            # Prepare user data
            user_id = str(uuid.uuid4())
            joined_date = datetime.now()
            
            # Zapisz użytkownika do SQL (jedyne źródło prawdy)
            with session_scope() as session:
                new_user = User(
                    user_id=user_id,
                    username=new_username,
                    password_hash=new_password,  # TODO: Hash password properly
                    company=selected_company_code,
                    permissions=permissions,
                    account_created_by=st.session_state.get('username', 'admin'),
                    xp=0,
                    level=1,
                    degencoins=0,
                    test_taken=False,
                    joined_date=joined_date.date()
                )
                
                session.add(new_user)
                session.commit()
            
            st.info("✓ Użytkownik utworzony w bazie SQL")
            
            st.success(f"✅ Utworzono konto: **{new_username}**")
            st.info(f"🔑 Hasło: `{new_password}` (przekaż użytkownikowi)")
            
            # Reset form
            st.session_state.generated_password = generate_password()
            
            time.sleep(2)
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Błąd podczas tworzenia konta: {e}")
            import traceback
            st.code(traceback.format_exc())


def show_admin_dashboard():
    """Wyświetla panel administratora"""
    
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Przewiń na górę strony
    scroll_to_top()
    
    # Sprawdź uwierzytelnienie admina
    if not check_admin_auth():
        # Jeśli użytkownik nie jest administratorem, wyświetl przycisk powrotu
        if zen_button("Powrót do strony głównej"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return
    
    # Nagłówek panelu administratora
    zen_header("🛡️ Panel Administratora")
    
    # Dodaj informację o ostatnim odświeżeniu
    st.markdown(f"**Ostatnie odświeżenie:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Przycisk do odświeżania danych
    if zen_button("🔄 Odśwież dane"):
        st.rerun()
    
    # Zakładki główne panelu administratora
    admin_tabs = st.tabs(["Przegląd", "Użytkownicy", "Lekcje", "Testy", "Zarządzanie", "Business Games", "Tagowanie Zasobów"])
    
    # 1. Zakładka Przegląd
    with admin_tabs[0]:
        st.subheader("Przegląd statystyk platformy")
        
        # Pobierz dane
        users_data = load_user_data()
        user_df = get_user_activity_data()
        
        # Podstawowe statystyki
        total_users = len(users_data)
        total_lessons_completed = user_df['completed_lessons'].sum()
        avg_xp = int(user_df['xp'].mean()) if not user_df.empty else 0
        tests_taken = user_df['test_taken'].sum()
        
        # Wyświetl statystyki w responsywnym układzie
        stats_cols = responsive_grid(4, 2, 1)
        
        with stats_cols[0]:
            stat_card("Liczba użytkowników", total_users, "👥")
        
        with stats_cols[1]:
            stat_card("Ukończone lekcje", int(total_lessons_completed), "📚")
        
        with stats_cols[2]:
            stat_card("Średnie XP", avg_xp, "⭐")
        
        with stats_cols[3]:
            stat_card("Wykonane testy", int(tests_taken), "📊")
          # Wykresy aktywności
        st.subheader("Aktywność użytkowników")
        
        activity_df = plot_user_activity_over_time()
        
        # Wykres aktywności użytkowników
        chart = alt.Chart(activity_df).mark_line(point=True).encode(
            x=alt.X('data:T', title='Data'),
            y=alt.Y('łącznie:Q', title='Liczba aktywności (rejestracje + logowania)'),
            tooltip=['data', 'rejestracje', 'logowania', 'łącznie']
        ).properties(
            width='container',
            height=350,
            title='Aktywność użytkowników: rejestracje i logowania (ostatnie 30 dni)'
        )
        
        st.altair_chart(chart)
        
        # Rozkład typów neuroliderów
        st.subheader("Rozkład typów neuroliderów")
        
        neuroleader_df = get_neuroleader_type_distribution()
        
        if not neuroleader_df.empty:
            # Wykres kołowy typów neuroleaderów z ulepszoną czytelnością
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Przygotuj dane
            counts = neuroleader_df['count'].tolist()
            labels = neuroleader_df['neuroleader_type'].tolist()
            total = sum(counts)
            
            # Funkcja do wyświetlania procentów tylko dla większych wartości
            def autopct_format(pct):
                return f'{pct:.1f}%' if pct >= 3 else ''
            
            # Stwórz wykres kołowy z automatycznym pozycjonowaniem etykiet
            pie_result = ax.pie(
                counts, 
                labels=labels,
                autopct=autopct_format,
                startangle=90,
                shadow=False,
                pctdistance=0.85,  # Odległość etykiet z procentami od środka
                labeldistance=1.1,  # Odległość nazw od środka
                explode=[0.05 if count/total < 0.05 else 0 for count in counts],  # Wysuń małe segmenty
                textprops={'fontsize': 10}
            )
            
            # Rozpakuj wyniki (może być 2 lub 3 elementy)
            if len(pie_result) == 3:
                wedges, texts, autotexts = pie_result
                # Poprawa czytelności etykiet procentowych
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            else:
                wedges, texts = pie_result
            
            # Dodaj legendę z dokładnymi liczbami
            legend_labels = [f'{label}: {count} ({count/total*100:.1f}%)' 
                           for label, count in zip(labels, counts)]
            ax.legend(wedges, legend_labels, title="Typy neuroleaderów", 
                     loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            ax.axis('equal')  # Zapewnia okrągły kształt
            plt.title('Rozkład typów neuroleaderów', fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            
            st.pyplot(fig)
        else:
            st.info("Brak danych o typach neuroleaderów.")
    
    # 2. Zakładka Użytkownicy
    with admin_tabs[1]:
        # Sub-zakładki: Lista użytkowników / Edycja użytkownika
        user_subtabs = st.tabs(["👥 Lista użytkowników", "✏️ Edycja użytkownika"])
        
        with user_subtabs[0]:
            st.subheader("Szczegóły użytkowników")
            
            # Pobierz dane
            user_df = get_user_activity_data()
            
            # Filtrowanie użytkowników
            filter_cols = st.columns(3)
            with filter_cols[0]:
                min_xp = st.number_input("Min XP", min_value=0, value=0)
            with filter_cols[1]:
                neuroleader_filter = st.selectbox("Filtruj wg typu neuroleader", 
                                           options=["Wszystkie"] + list(user_df['neuroleader_type'].unique()))
            with filter_cols[2]:
                sort_by = st.selectbox("Sortuj wg", 
                                       options=["xp", "level", "completed_lessons", "username"])
            
            # Zastosuj filtry
            filtered_df = user_df
            if min_xp > 0:
                filtered_df = filtered_df[filtered_df['xp'] >= min_xp]
            
            if neuroleader_filter != "Wszystkie":
                filtered_df = filtered_df[filtered_df['neuroleader_type'] == neuroleader_filter]
            
            # Sortuj dane
            filtered_df = filtered_df.sort_values(by=sort_by, ascending=False)
            
            # Wyświetl tabelę użytkowników
            st.dataframe(
                filtered_df,
                column_config={
                    "username": "Nazwa użytkownika",
                    "xp": "XP",
                    "level": "Poziom",
                    "completed_lessons": "Ukończone lekcje",
                    "neuroleader_type": "Typ neuroleader",
                    "registration_date": "Data rejestracji",
                    "last_login": "Ostatnie logowanie",
                    "test_taken": "Test wykonany",
                    "streak": "Seria dni"
                },
                use_container_width=True
            )
        
            # Dodaj opcję eksportu danych
            if zen_button("Eksportuj dane użytkowników do CSV"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Pobierz CSV",
                    data=csv,
                    file_name="users_data.csv",
                    mime="text/csv"
                )
        
        with user_subtabs[1]:
            show_user_edit_panel()
    
    # 3. Zakładka Lekcje
    with admin_tabs[2]:
        st.subheader("Statystyki lekcji")
        
        # Pobierz dane lekcji
        lessons_df = get_lessons_stats()
        
        # Wyświetl tabelę statystyk lekcji
        st.dataframe(
            lessons_df,
            column_config={
                "lesson_id": "ID lekcji",
                "title": "Tytuł",
                "category": "Kategoria",
                "difficulty": st.column_config.SelectboxColumn(
                    "Poziom trudności", 
                    options=["beginner", "intermediate", "advanced"],
                    required=True
                ),
                "completions": "Liczba ukończeń",
                "completion_rate": st.column_config.ProgressColumn(
                    "Wskaźnik ukończenia (%)",
                    min_value=0,
                    max_value=100,
                    format="%{value:.2f}"
                )
            },
            use_container_width=True
        )
        
        # Wykres popularności lekcji (top 10)
        st.subheader("Najpopularniejsze lekcje")
        
        top_lessons = lessons_df.sort_values('completions', ascending=False).head(10)
        
        if not top_lessons.empty:
            chart = alt.Chart(top_lessons).mark_bar().encode(
                x=alt.X('completions:Q', title='Liczba ukończeń'),
                y=alt.Y('title:N', title='Lekcja', sort='-x'),
                color=alt.Color('category:N', title='Kategoria'),
                tooltip=['title', 'category', 'completions', 'completion_rate']
            ).properties(
                width='container',
                height=400,
                title='Top 10 najpopularniejszych lekcji'
            )
            
            st.altair_chart(chart)
        else:
            st.info("Brak danych o ukończonych lekcjach.")
    
    # 4. Zakładka Testy (poprzednio 5)
    with admin_tabs[3]:
        st.subheader("Wyniki testów Neurolidera")
        
        # Pobierz dane o użytkownikach
        users_data = load_user_data()
        
        # Zbierz dane o wynikach testów
        test_results = []
        for username, data in users_data.items():
            if data.get('test_scores'):
                for neuroleader_type, score in data.get('test_scores', {}).items():
                    test_results.append({
                        'username': username,
                        'neuroleader_type': neuroleader_type,
                        'score': score
                    })
        
        test_df = pd.DataFrame(test_results)
        
        if not test_df.empty:
            # Średnie wyniki dla każdego typu neuroleader
            st.subheader("Średnie wyniki dla typów neuroleaderów")
            
            avg_scores = test_df.groupby('neuroleader_type')['score'].mean().reset_index()
            avg_scores['score'] = avg_scores['score'].round(2)
            
            chart = alt.Chart(avg_scores).mark_bar().encode(
                x=alt.X('neuroleader_type:N', title='Typ neuroleader'),
                y=alt.Y('score:Q', title='Średni wynik'),
                color=alt.Color('neuroleader_type:N', title='Typ neuroleader'),
                tooltip=['neuroleader_type', 'score']
            ).properties(
                width='container',
                height=350,
                title='Średnie wyniki testów wg typu neuroleader'
            )
            
            st.altair_chart(chart)
            
            # Tabela z wynikami testów
            st.subheader("Szczegółowe wyniki testów")
            st.dataframe(
                test_df,
                column_config={
                    "username": "Nazwa użytkownika",
                    "neuroleader_type": "Typ neuroleader",
                    "score": "Wynik"
                },
                use_container_width=True
            )
        else:
            st.info("Brak danych o wynikach testów.")
        
        # NOWA SEKCJA: Wyniki testów Kolba Learning Styles
        st.markdown("---")
        st.subheader("🎯 Wyniki testów Stylów Uczenia się Kolba (Learning Styles)")
        
        # Pobierz dane o użytkownikach z wynikami testów Kolba
        kolb_results = []
        for username, data in users_data.items():
            if data.get('kolb_test'):
                kolb_data = data['kolb_test']
                kolb_results.append({
                    'username': username,
                    'dominant_style': kolb_data.get('dominant_style', 'Nieznany'),
                    'AC-CE': kolb_data.get('dimensions', {}).get('AC-CE', 0),
                    'AE-RO': kolb_data.get('dimensions', {}).get('AE-RO', 0),
                    'flexibility': kolb_data.get('flexibility', 0),
                    'completed_date': kolb_data.get('completed_date', 'Nieznana'),
                    'CE': kolb_data.get('scores', {}).get('CE', 0),
                    'RO': kolb_data.get('scores', {}).get('RO', 0),
                    'AC': kolb_data.get('scores', {}).get('AC', 0),
                    'AE': kolb_data.get('scores', {}).get('AE', 0)
                })
        
        if kolb_results:
            kolb_df = pd.DataFrame(kolb_results)
            
            # Statystyki podstawowe
            st.markdown("#### 📊 Statystyki podstawowe")
            
            stats_cols = st.columns(4)
            with stats_cols[0]:
                st.metric("Liczba użytkowników", len(kolb_df))
            with stats_cols[1]:
                st.metric("Średnia elastyczność", f"{kolb_df['flexibility'].mean():.1f}%")
            with stats_cols[2]:
                most_common_style = kolb_df['dominant_style'].mode()[0] if not kolb_df.empty else "Brak"
                st.metric("Najczęstszy styl", most_common_style.split('(')[0].strip())
            with stats_cols[3]:
                st.metric("Najwyższa elastyczność", f"{kolb_df['flexibility'].max():.1f}%")
            
            # Rozkład stylów uczenia się
            st.markdown("---")
            st.markdown("#### 📈 Rozkład stylów uczenia się")
            
            style_counts = kolb_df['dominant_style'].value_counts().reset_index()
            style_counts.columns = ['Styl', 'Liczba']
            
            chart = alt.Chart(style_counts).mark_bar().encode(
                x=alt.X('Liczba:Q', title='Liczba użytkowników'),
                y=alt.Y('Styl:N', title='Styl uczenia się', sort='-x'),
                color=alt.Color('Styl:N', legend=None),
                tooltip=['Styl', 'Liczba']
            ).properties(
                width='container',
                height=300,
                title='Rozkład stylów uczenia się wśród użytkowników'
            )
            
            st.altair_chart(chart, use_container_width=True)
            
            # GŁÓWNA WIZUALIZACJA: Siatka wszystkich użytkowników
            st.markdown("---")
            st.markdown("#### 🗺️ Siatka Stylów Uczenia się - Wszyscy Użytkownicy")
            st.markdown("*Pozycje wszystkich użytkowników w matrycy ELT z etykietami nazw*")
            
            # Utwórz wykres siatki Kolba z wszystkimi użytkownikami
            fig_all = go.Figure()
            
            # Dodaj tło ćwiartek z nazwami stylów
            quadrant_info = {
                'Diverging': {'x': [-12, 0], 'y': [-12, 0], 'color': 'rgba(231, 76, 60, 0.15)', 'label_x': -6, 'label_y': -6},
                'Assimilating': {'x': [-12, 0], 'y': [0, 12], 'color': 'rgba(155, 89, 182, 0.15)', 'label_x': -6, 'label_y': 6},
                'Converging': {'x': [0, 12], 'y': [0, 12], 'color': 'rgba(52, 152, 219, 0.15)', 'label_x': 6, 'label_y': 6},
                'Accommodating': {'x': [0, 12], 'y': [-12, 0], 'color': 'rgba(46, 204, 113, 0.15)', 'label_x': 6, 'label_y': -6}
            }
            
            # Rysuj prostokąty ćwiartek
            for style_name, info in quadrant_info.items():
                fig_all.add_shape(
                    type="rect",
                    x0=info['x'][0], x1=info['x'][1],
                    y0=info['y'][0], y1=info['y'][1],
                    fillcolor=info['color'],
                    line=dict(width=0)
                )
                
                # Dodaj etykiety stylów
                fig_all.add_annotation(
                    x=info['label_x'], y=info['label_y'],
                    text=f"<b>{style_name}</b>",
                    showarrow=False,
                    font=dict(size=14, color='rgba(0,0,0,0.5)', family='Arial Black'),
                    xanchor='center',
                    yanchor='middle'
                )
            
            # Strefa Zrównoważonego Uczenia się (centralna)
            balanced_zone_radius = 4
            theta = [i for i in range(0, 361, 10)]
            balanced_x = [balanced_zone_radius * math.cos(math.radians(t)) for t in theta]
            balanced_y = [balanced_zone_radius * math.sin(math.radians(t)) for t in theta]
            
            fig_all.add_trace(go.Scatter(
                x=balanced_x, y=balanced_y,
                fill='toself',
                fillcolor='rgba(255, 193, 7, 0.2)',
                line=dict(color='rgba(255, 193, 7, 0.6)', width=2, dash='dash'),
                name='Strefa Zrównoważonego<br>Uczenia się',
                hoverinfo='name',
                showlegend=True
            ))
            
            # Osie
            fig_all.add_shape(type="line", x0=-12, x1=12, y0=0, y1=0, 
                              line=dict(color="rgba(0,0,0,0.4)", width=2))
            fig_all.add_shape(type="line", x0=0, x1=0, y0=-12, y1=12, 
                              line=dict(color="rgba(0,0,0,0.4)", width=2))
            
            # Mapowanie kolorów dla stylów
            style_colors = {
                'Diverging (Dywergent)': '#E74C3C',      # Czerwony
                'Assimilating (Asymilator)': '#9B59B6',  # Fioletowy
                'Converging (Konwergent)': '#3498DB',    # Niebieski
                'Accommodating (Akomodator)': '#2ECC71'  # Zielony
            }
            
            # Dodaj punkty użytkowników pogrupowane wg stylu
            for style in kolb_df['dominant_style'].unique():
                style_data = kolb_df[kolb_df['dominant_style'] == style]
                
                # Przygotuj tekst dla hover i etykiety
                hover_texts = []
                for _, row in style_data.iterrows():
                    hover_text = (
                        f"<b>{row['username']}</b><br>"
                        f"Styl: {row['dominant_style']}<br>"
                        f"AE-RO: {row['AE-RO']:+d}<br>"
                        f"AC-CE: {row['AC-CE']:+d}<br>"
                        f"Elastyczność: {row['flexibility']:.1f}%<br>"
                        f"Data: {row['completed_date']}"
                    )
                    hover_texts.append(hover_text)
                
                fig_all.add_trace(go.Scatter(
                    x=style_data['AE-RO'],
                    y=style_data['AC-CE'],
                    mode='markers+text',
                    marker=dict(
                        size=15,
                        color=style_colors.get(style, '#95A5A6'),
                        line=dict(color='white', width=2),
                        symbol='circle'
                    ),
                    text=style_data['username'],
                    textposition='top center',
                    textfont=dict(size=10, color='#2C3E50', family='Arial Black'),
                    name=style.split('(')[0].strip(),  # Skrócona nazwa do legendy
                    hovertemplate='%{customdata}<extra></extra>',
                    customdata=hover_texts
                ))
            
            # Etykiety osi
            fig_all.add_annotation(x=12.5, y=0, text="<b>AE</b><br>(Doing)", showarrow=False, 
                                   font=dict(size=11, color='#2ECC71'), xanchor='left')
            fig_all.add_annotation(x=-12.5, y=0, text="<b>RO</b><br>(Watching)", showarrow=False, 
                                   font=dict(size=11, color='#4A90E2'), xanchor='right')
            fig_all.add_annotation(x=0, y=12.5, text="<b>AC</b><br>(Thinking)", showarrow=False, 
                                   font=dict(size=11, color='#9B59B6'), yanchor='bottom')
            fig_all.add_annotation(x=0, y=-12.5, text="<b>CE</b><br>(Feeling)", showarrow=False, 
                                   font=dict(size=11, color='#E74C3C'), yanchor='top')
            
            fig_all.update_layout(
                title=dict(
                    text=f'Mapa Stylów Uczenia się - {len(kolb_df)} użytkowników',
                    font=dict(size=18, color='#333', family='Arial Black'),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title='<b>Oś Przetwarzania (AE-RO)</b>',
                    range=[-14, 14],
                    zeroline=False,
                    gridcolor='rgba(0,0,0,0.1)',
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    title='<b>Oś Postrzegania (AC-CE)</b>',
                    range=[-14, 14],
                    zeroline=False,
                    gridcolor='rgba(0,0,0,0.1)',
                    tickfont=dict(size=10),
                    scaleanchor='x',
                    scaleratio=1
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=700,
                margin=dict(t=80, b=80, l=80, r=80),
                showlegend=True,
                legend=dict(
                    title="Style uczenia się:",
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='rgba(0,0,0,0.2)',
                    borderwidth=1
                )
            )
            
            st.plotly_chart(fig_all, use_container_width=True)
            
            # Tabela szczegółowa
            st.markdown("---")
            st.markdown("#### 📋 Szczegółowe wyniki użytkowników")
            
            # Formatuj DataFrame do wyświetlenia
            display_df = kolb_df[['username', 'dominant_style', 'CE', 'RO', 'AC', 'AE', 
                                   'AC-CE', 'AE-RO', 'flexibility', 'completed_date']]
            
            st.dataframe(
                display_df,
                column_config={
                    "username": "Użytkownik",
                    "dominant_style": "Dominujący styl",
                    "CE": st.column_config.NumberColumn("CE (Feeling)", format="%d/12"),
                    "RO": st.column_config.NumberColumn("RO (Watching)", format="%d/12"),
                    "AC": st.column_config.NumberColumn("AC (Thinking)", format="%d/12"),
                    "AE": st.column_config.NumberColumn("AE (Doing)", format="%d/12"),
                    "AC-CE": st.column_config.NumberColumn("AC-CE", format="%+d"),
                    "AE-RO": st.column_config.NumberColumn("AE-RO", format="%+d"),
                    "flexibility": st.column_config.ProgressColumn(
                        "Elastyczność (%)",
                        min_value=0,
                        max_value=100,
                        format="%.1f%%"
                    ),
                    "completed_date": "Data ukończenia"
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Opcja eksportu
            if zen_button("📥 Eksportuj wyniki testów Kolba do CSV"):
                csv = display_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="⬇️ Pobierz CSV",
                    data=csv,
                    file_name=f"kolb_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("Brak użytkowników, którzy ukończyli test stylów uczenia się Kolba.")
    
    # 5. Zakładka Zarządzanie (poprzednio 6)
    with admin_tabs[4]:
        st.subheader("Zarządzanie użytkownikami")
        
        # === TWORZENIE NOWEGO UŻYTKOWNIKA ===
        st.markdown("---")
        st.subheader("➕ Utwórz nowe konto użytkownika")
        
        with st.expander("Formularz tworzenia użytkownika", expanded=False):
            create_user_form()
        
        st.markdown("---")
        
        # Pobierz dane
        users_data = load_user_data()
        usernames = list(users_data.keys())
        
        # Wybór użytkownika
        selected_user = st.selectbox("Wybierz użytkownika", options=usernames)
        
        if selected_user:
            user_data = users_data.get(selected_user, {})
            
            # Wyświetl szczegóły użytkownika
            st.json(user_data)
            
            # Akcje zarządzania
            action_cols = st.columns(3)
            
            with action_cols[0]:
                if zen_button("🔄 Reset postępu XP", key="reset_xp"):
                    if st.session_state.get('confirm_reset_xp', False):
                        # Wykonaj reset XP
                        users_data[selected_user]['xp'] = 0
                        users_data[selected_user]['level'] = 1
                        save_user_data(users_data)
                        st.session_state.confirm_reset_xp = False
                        notification("Zresetowano XP użytkownika.", type="success")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.session_state.confirm_reset_xp = True
                        st.warning("Czy na pewno chcesz zresetować XP? Kliknij ponownie, aby potwierdzić.")
            
            with action_cols[1]:
                if zen_button("📚 Reset ukończonych lekcji", key="reset_lessons"):
                    if st.session_state.get('confirm_reset_lessons', False):
                        # Wykonaj reset ukończonych lekcji
                        users_data[selected_user]['completed_lessons'] = []
                        save_user_data(users_data)
                        st.session_state.confirm_reset_lessons = False
                        notification("Zresetowano ukończone lekcje użytkownika.", type="success")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.session_state.confirm_reset_lessons = True
                        st.warning("Czy na pewno chcesz zresetować ukończone lekcje? Kliknij ponownie, aby potwierdzić.")
            
            with action_cols[2]:
                if zen_button("🗑️ Usuń użytkownika", key="delete_user"):
                    if st.session_state.get('confirm_delete', False):
                        # Wykonaj usunięcie użytkownika z JSON i SQL
                        success = delete_user_completely(selected_user)
                        
                        st.session_state.confirm_delete = False
                        
                        if success:
                            notification("Usunięto użytkownika z JSON i SQL.", type="success")
                        else:
                            notification("Usunięto użytkownika z JSON (SQL może być niedostępny).", type="warning")
                        
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.session_state.confirm_delete = True
                        st.warning("Czy na pewno chcesz usunąć tego użytkownika? Ta operacja usunie wszystkie dane (JSON + SQL) i jest nieodwracalna! Kliknij ponownie, aby potwierdzić.")
            
            # Dodatkowe ustawienia użytkownika
            st.subheader("Edycja danych użytkownika")
            
            edit_cols = st.columns(2)
            with edit_cols[0]:
                new_xp = st.number_input("Punkty XP", min_value=0, value=user_data.get('xp', 0))
            
            with edit_cols[1]:
                new_level = st.number_input("Poziom", min_value=1, value=user_data.get('level', 1))
            
            # Admin status
            is_admin = st.checkbox("Administrator", value=selected_user in ["admin", "zenmaster"])
            
            # === ZMIANA HASŁA ===
            st.markdown("---")
            st.subheader("🔐 Zmiana hasła użytkownika")
            
            with st.expander("Zmień hasło", expanded=False):
                new_password = st.text_input(
                    "Nowe hasło:",
                    type="password",
                    key="admin_new_password",
                    help="Wprowadź nowe hasło dla użytkownika (min. 4 znaki)"
                )
                confirm_password = st.text_input(
                    "Potwierdź hasło:",
                    type="password",
                    key="admin_confirm_password"
                )
                
                if zen_button("🔐 Zmień hasło", key="change_password_btn"):
                    if not new_password or len(new_password) < 4:
                        st.error("❌ Hasło musi mieć co najmniej 4 znaki!")
                    elif new_password != confirm_password:
                        st.error("❌ Hasła nie są identyczne!")
                    else:
                        try:
                            import bcrypt
                            from database.connection import session_scope
                            from database.models import User
                            
                            # Hashuj nowe hasło
                            password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                            
                            # Zapisz w bazie SQL
                            with session_scope() as session:
                                user_obj = session.query(User).filter_by(username=selected_user).first()
                                if user_obj:
                                    user_obj.password_hash = password_hash
                                    session.commit()
                                    st.success(f"✅ Hasło użytkownika {selected_user} zostało zmienione!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("❌ Nie znaleziono użytkownika w bazie SQL!")
                        except Exception as e:
                            st.error(f"❌ Błąd podczas zmiany hasła: {e}")
            
            st.markdown("---")
            
            # Zapisz zmiany XP/Level
            if zen_button("Zapisz zmiany XP/Level"):
                users_data[selected_user]['xp'] = new_xp
                users_data[selected_user]['level'] = new_level
                
                # Zapisz dane
                save_user_data(users_data)
                notification("Zapisano zmiany.", type="success")
                time.sleep(1)
                st.rerun()
        
        # Przycisk eksportu kopii zapasowej
        st.subheader("Kopia zapasowa")
        if zen_button("💾 Eksportuj kopię zapasową danych"):
            # Konwertuj dane do formatu JSON
            users_json = json.dumps(users_data, indent=4)
            
            # Oferuj plik do pobrania
            st.download_button(
                label="Pobierz kopię zapasową (JSON)",
                data=users_json,
                file_name=f"neuroleader_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # 6. Zakładka Business Games (poprzednio 7)
    with admin_tabs[5]:
        show_business_games_admin_panel()
    
    # 7. Zakładka Tagowanie Zasobów (poprzednio 8)
    with admin_tabs[6]:
        show_resource_tagging_panel()

def manage_lesson_access():
    """
    DEPRECATED: Stary system zarządzania dostępnością lekcji
    Zastąpiony przez system tagowania zasobów (zakładka "Tagowanie Zasobów")
    """
    st.warning("⚠️ Ta funkcja została zastąpiona przez nowy system tagowania zasobów.")
    st.info("👉 Użyj zakładki **'Tagowanie Zasobów'** do zarządzania dostępem do lekcji.")
    
    if st.button("Przejdź do Tagowania Zasobów"):
        st.rerun()

def show_business_games_admin_panel():
    """Panel administracyjny Business Games"""
    from utils.business_game_evaluation import (
        get_active_evaluation_mode,
        set_active_evaluation_mode,
        get_pending_reviews_count,
        get_pending_contract_reviews,
        submit_game_master_review,
        get_evaluation_stats,
        save_gemini_api_key,
        load_gemini_api_key
    )
    from config.business_games_settings import EVALUATION_MODES
    
    st.subheader("⚙️ Business Games - Panel Administracyjny")
    
    # Sub-tabs dla różnych sekcji
    bg_tabs = st.tabs(["🎯 Ustawienia Oceny", "👨‍💼 Kolejka Mistrza Gry", "📊 Statystyki"])
    
    # --- TAB 1: USTAWIENIA OCENY ---
    with bg_tabs[0]:
        st.markdown("### 🎯 Tryb Oceny Kontraktów")
        
        current_mode = get_active_evaluation_mode()
        
        st.info(f"**Aktualny tryb:** {EVALUATION_MODES[current_mode]['name']}")
        
        # Wybór trybu
        mode_options = {
            "ai": f"{EVALUATION_MODES['ai']['name']} - {EVALUATION_MODES['ai']['subtitle']}",
            "game_master": f"{EVALUATION_MODES['game_master']['name']} - {EVALUATION_MODES['game_master']['subtitle']}"
        }
        
        selected_mode = st.selectbox(
            "Wybierz tryb oceny:",
            options=list(mode_options.keys()),
            format_func=lambda x: mode_options[x],
            index=list(mode_options.keys()).index(current_mode) if current_mode in mode_options else 0
        )
        
        # Info o wybranym trybie
        st.markdown("---")
        
        if selected_mode == "ai":
            st.warning("""
            **🤖 Ocena AI (Google Gemini):**
            - ✅ Szczegółowa analiza merytoryczna
            - ✅ Automatyczny feedback dla uczestników
            - ✅ Ocena według 5 kryteriów
            - ⚠️ Wymaga klucza API Google Gemini
            - ⚠️ Koszt: ~$0.01-0.03 per ocena
            - ⚠️ Czas oceny: 5-10 sekund
            """)
            
            st.markdown("**Konfiguracja API Google Gemini:**")
            
            # Sprawdź klucz w różnych miejscach
            key_in_secrets = False
            key_in_file = False
            
            # 1. Sprawdź Streamlit secrets (preferowany)
            try:
                if st.secrets.get("GOOGLE_API_KEY"):
                    key_in_secrets = True
                    st.success("✅ Klucz API skonfigurowany w Streamlit secrets (preferowany)")
                    st.info("💡 Używasz tego samego klucza co w innych narzędziach AI aplikacji")
            except:
                pass
            
            # 2. Sprawdź plik konfiguracyjny (backward compatibility)
            existing_key = load_gemini_api_key()
            if existing_key:
                key_in_file = True
                st.success("✅ Klucz API skonfigurowany w pliku config/gemini_api_key.txt")
                if st.checkbox("Pokaż klucz z pliku"):
                    st.code(existing_key)
                if st.button("🗑️ Usuń klucz z pliku"):
                    import os
                    try:
                        os.remove("config/gemini_api_key.txt")
                        st.success("Klucz usunięty z pliku")
                        time.sleep(1)
                        st.rerun()
                    except:
                        pass
            
            # 3. Brak klucza
            if not key_in_secrets and not key_in_file:
                st.warning("⚠️ Brak klucza API")
                st.info("""
                **Opcja 1 (Zalecana):** Klucz już jest w `st.secrets["GOOGLE_API_KEY"]`
                - Używany w innych narzędziach AI
                - Wystarczy wybrać tryb AI i zapisać
                
                **Opcja 2:** Dodaj klucz ręcznie poniżej (zostanie zapisany do pliku)
                """)
            
            # Formularz dodawania klucza
            with st.form("api_key_form"):
                api_key_input = st.text_input(
                    "Wpisz klucz API Google Gemini:",
                    type="password",
                    help="Znajdziesz go na: https://aistudio.google.com/app/apikey"
                )
                
                if st.form_submit_button("💾 Zapisz klucz API"):
                    if api_key_input and len(api_key_input) > 10:
                        save_gemini_api_key(api_key_input)
                        st.success("✅ Klucz API zapisany!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Nieprawidłowy format klucza (klucz jest za krótki)")
        
        elif selected_mode == "game_master":
            pending_count = get_pending_reviews_count()
            
            st.info(f"""
            **👨‍💼 Mistrz Gry:**
            - ✅ Pełna kontrola jakości
            - ✅ Spersonalizowany feedback
            - ✅ Najlepsza jakość edukacyjna
            - ⚠️ Wymaga czasu Admina
            - ⚠️ Opóźnienie w otrzymaniu nagrody
            - ⚠️ Zalecane dla małych grup (do 20 osób)
            """)
            
            if pending_count > 0:
                st.warning(f"⏳ **Oczekujące oceny: {pending_count}**")
                if st.button("📋 Przejdź do kolejki ocen"):
                    st.session_state.bg_admin_tab = 1  # Przełącz na zakładkę kolejki
                    st.rerun()
            else:
                st.success("✅ Brak oczekujących rozwiązań")
        
        # Zapisz ustawienia
        st.markdown("---")
        if st.button("💾 Zapisz ustawienia", type="primary", key="save_bg_settings"):
            if set_active_evaluation_mode(selected_mode):
                st.success(f"✅ Tryb oceny zmieniony na: {EVALUATION_MODES[selected_mode]['name']}")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Błąd podczas zapisywania ustawień")
    
    # --- TAB 2: KOLEJKA MISTRZA GRY ---
    with bg_tabs[1]:
        st.markdown("### 👨‍💼 Kolejka Mistrza Gry")
        
        pending_reviews = get_pending_contract_reviews()
        
        if not pending_reviews:
            st.success("🎉 Brak oczekujących rozwiązań do oceny!")
            st.info("Rozwiązania pojawią się tutaj gdy użytkownicy prześlą kontrakty w trybie 'Mistrz Gry'")
            return
        
        st.info(f"📋 Oczekujące rozwiązania: **{len(pending_reviews)}**")
        
        # Filtry
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_category = st.selectbox(
                "Kategoria:",
                ["Wszystkie", "Konflikt", "Coaching", "Leadership", "Zarządzanie", "Strategia"]
            )
        with col2:
            filter_difficulty = st.selectbox("Trudność:", ["Wszystkie", "1⭐", "2⭐", "3⭐", "4⭐", "5⭐"])
        with col3:
            sort_by = st.selectbox("Sortuj:", ["Najstarsze", "Najnowsze", "Trudność", "Pilne"])
        
        # Filtrowanie
        filtered_reviews = pending_reviews.copy()
        
        if filter_category != "Wszystkie":
            filtered_reviews = [r for r in filtered_reviews if r["contract_category"] == filter_category]
        
        if filter_difficulty != "Wszystkie":
            diff_level = int(filter_difficulty[0])
            filtered_reviews = [r for r in filtered_reviews if r["contract_difficulty"] == diff_level]
        
        # Lista rozwiązań
        st.markdown("---")
        
        for idx, review in enumerate(filtered_reviews, 1):
            # Oznaczenie pilności
            urgent_badge = "🔴 PILNE" if review.get("is_urgent", False) else ""
            
            with st.expander(
                f"#{idx} {urgent_badge} {review['username']} - {review['contract_title']} "
                f"({'⭐' * review['contract_difficulty']})",
                expanded=(idx == 1)  # Pierwszy rozwinięty
            ):
                # Informacje podstawowe
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**👤 Użytkownik:** {review['user_display_name']} (@{review['username']})")
                    st.markdown(f"**📝 Kontrakt:** {review['contract_title']}")
                    st.markdown(f"**🏷️ Kategoria:** {review['contract_category']}")
                    st.markdown(f"**⭐ Trudność:** {'⭐' * review['contract_difficulty']}")
                    st.markdown(f"**📅 Przesłano:** {review['submitted_at']}")
                
                with col2:
                    st.metric("📊 Długość", f"{review['word_count']} słów")
                    st.metric("⏱️ Czeka", f"{review['waiting_hours']}h")
                    
                    if review.get("is_urgent"):
                        st.error("🔴 PILNE!")
                
                # Opis kontraktu
                st.markdown("---")
                st.markdown("**📋 Opis Kontraktu:**")
                st.info(review['contract_description'])
                
                # Rozwiązanie uczestnika
                st.markdown("**📝 Rozwiązanie Uczestnika:**")
                st.text_area(
                    "Treść rozwiązania:",
                    value=review['solution'],
                    height=300,
                    disabled=True,
                    key=f"solution_{review['id']}"
                )
                
                # Formularz oceny
                st.markdown("---")
                st.markdown("### ⭐ Twoja Ocena")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    rating = st.slider(
                        "Oceń jakość rozwiązania:",
                        min_value=1,
                        max_value=5,
                        value=3,
                        help="1⭐ = słabe, 5⭐ = doskonałe",
                        key=f"rating_{review['id']}"
                    )
                    
                    st.write(f"**Wybrano: {rating}⭐**")
                
                with col2:
                    feedback = st.text_area(
                        "Komentarz dla uczestnika (opcjonalny):",
                        placeholder="Mocne strony:\n- ...\n\nDo poprawy:\n- ...\n\nPodsumowanie:\n...",
                        height=200,
                        key=f"feedback_{review['id']}"
                    )
                
                # Przyciski akcji
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if st.button(
                        "✅ Zatwierdź ocenę",
                        key=f"approve_{review['id']}",
                        type="primary",
                        use_container_width=True
                    ):
                        admin_username = st.session_state.get('username', 'admin')
                        
                        if submit_game_master_review(
                            review_id=review['id'],
                            rating=rating,
                            feedback=feedback,
                            admin_username=admin_username
                        ):
                            st.success(f"✅ Ocena zatwierdzona! {review['username']} otrzymał {rating}⭐")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Błąd podczas zatwierdzania oceny")
                
                with col2:
                    if st.button(
                        "⏭️ Pomiń na później",
                        key=f"skip_{review['id']}",
                        use_container_width=True
                    ):
                        st.info("Przeskoczono do następnego")
    
    # --- TAB 3: STATYSTYKI ---
    with bg_tabs[2]:
        st.markdown("### 📊 Statystyki Business Games")
        
        stats = get_evaluation_stats()
        
        # Metryki
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            stat_card("Wszystkie oceny", stats['total_reviews'], "📋")
        
        with col2:
            stat_card("Oczekujące", stats['pending'], "⏳")
        
        with col3:
            stat_card("Ocenione", stats['reviewed'], "✅")
        
        with col4:
            avg_rating = round(stats['avg_rating'], 2)
            stat_card("Średnia ocena", f"{avg_rating}⭐", "⭐")
        
        # Aktualny tryb
        st.markdown("---")
        st.markdown("**Aktualny tryb oceny:**")
        current_mode = stats['active_mode']
        st.info(f"{EVALUATION_MODES[current_mode]['name']} - {EVALUATION_MODES[current_mode]['description']}")


def get_lesson_access_status(username, lesson_id):
    """Sprawdź czy użytkownik ma dostęp do lekcji - NOWY SYSTEM tagowania"""
    from utils.resource_access import has_access_to_resource
    from database.connection import session_scope
    
    try:
        from database.models import User
        with session_scope() as session:
            user = session.query(User).filter_by(username=username).first()
            
            if not user:
                return True  # Domyślnie dostępne dla nowych użytkowników
            
            user_data = user.to_dict()
            
            # NOWY SYSTEM: sprawdź tagi zasobu
            return has_access_to_resource('lessons', lesson_id, user_data)
    except Exception as e:
        print(f"Error checking lesson access: {e}")
        return True  # Domyślnie dostępne przy błędzie

def is_lesson_accessible(username, lesson_id):
    """Wrapper function dla łatwiejszego użycia"""
    return get_lesson_access_status(username, lesson_id)

def initialize_lesson_access_for_user(username):
    """
    DEPRECATED: Stary system inicjalizacji dostępu do lekcji
    Zastąpiony przez system tagowania zasobów (resource_tags.json)
    Funkcja zachowana dla kompatybilności wstecznej, ale nie robi nic.
    """
    # Nowy system nie wymaga inicjalizacji - używa tagów z resource_tags.json
    return True


def show_user_edit_panel():
    """Panel edycji użytkowników - zmiana company i custom permissions"""
    st.subheader("✏️ Edycja Użytkowników")
    
    from database.models import User
    from database.connection import session_scope
    from utils.resource_access import get_all_companies
    
    # Pobierz listę użytkowników z SQL
    try:
        with session_scope() as session:
            users = session.query(User).all()
            
            if not users:
                st.info("Brak użytkowników w systemie.")
                return
            
            # Wybór użytkownika
            user_options = {u.username: u for u in users}
            selected_username = st.selectbox(
                "Wybierz użytkownika do edycji:",
                options=list(user_options.keys())
            )
            
            if selected_username:
                user = user_options[selected_username]
                
                st.markdown("---")
                st.markdown(f"### Edycja: **{user.username}**")
                
                # Informacje podstawowe
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("XP", user.xp)
                    st.metric("Level", user.level)
                with col2:
                    st.metric("Utworzone przez", user.account_created_by or "Rejestracja")
                    st.metric("Ostatnie logowanie", user.last_login.strftime("%Y-%m-%d %H:%M") if user.last_login else "Nigdy")
                
                st.markdown("---")
                
                # Edycja company
                st.markdown("#### 🏢 Przypisanie do grupy")
                companies = get_all_companies()
                company_names = {c['display_name']: c['code'] for c in companies}
                current_company_name = next((c['display_name'] for c in companies if c['code'] == user.company), "Ogólne")
                
                new_company_name = st.selectbox(
                    "Grupa użytkownika:",
                    options=list(company_names.keys()),
                    index=list(company_names.keys()).index(current_company_name) if current_company_name in company_names.keys() else 0
                )
                new_company_code = company_names[new_company_name]
                
                st.info("💡 **Motyw lekcji (Layout)** można zmienić w Profilu → Ustawienia")
                
                # Niestandardowe uprawnienia
                st.markdown("#### ⚙️ Niestandardowe uprawnienia (opcjonalne)")
                use_custom_permissions = st.checkbox(
                    "Użyj niestandardowych uprawnień zamiast szablonu grupy",
                    value=bool(user.permissions)
                )
                
                custom_permissions = None
                if use_custom_permissions:
                    st.warning("⚠️ Niestandardowe uprawnienia nadpiszą szablon grupy")
                    
                    # Edytor JSON dla permissions
                    current_permissions = user.permissions or {}
                    permissions_json = st.text_area(
                        "Uprawnienia (JSON):",
                        value=json.dumps(current_permissions, indent=2, ensure_ascii=False),
                        height=300
                    )
                    
                    try:
                        custom_permissions = json.loads(permissions_json)
                    except json.JSONDecodeError as e:
                        st.error(f"Błąd w JSON: {e}")
                        custom_permissions = None
                
                # Przycisk zapisu
                st.markdown("---")
                if st.button("💾 Zapisz zmiany", type="primary", use_container_width=True):
                    try:
                        # Aktualizuj dane użytkownika w SQL
                        user.company = new_company_code
                        if use_custom_permissions and custom_permissions is not None:
                            user.permissions = custom_permissions
                        else:
                            user.permissions = None  # Użyje szablonu grupy
                        
                        session.commit()
                        
                        st.success(f"✅ Zaktualizowano użytkownika {user.username} (company: {new_company_name})")
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        session.rollback()
                        st.error(f"❌ Błąd podczas zapisywania: {e}")
                
                # Podgląd uprawnień
                st.markdown("---")
                st.markdown("#### 👁️ Podgląd uprawnień")
                
                from utils.permissions import get_user_permissions
                final_permissions = get_user_permissions(user.to_dict())
                
                st.json(final_permissions)
                
    except Exception as e:
        st.error(f"Błąd: {e}")


def show_resource_tagging_panel():
    """Panel tagowania zasobów - przypisywanie lekcji/inspiracji/BG do grup"""
    st.subheader("🏷️ Tagowanie Zasobów")
    
    from utils.resource_access import (
        load_resource_tags, save_resource_tags, 
        get_all_companies, get_resource_tags, set_resource_tags,
        clear_resource_tags_cache
    )
    
    # Przycisk do wymuszonego przeładowania cache
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Reload Cache", help="Wymusza ponowne załadowanie tagów z pliku"):
            clear_resource_tags_cache()
            st.success("Cache wyczyszczony!")
            st.rerun()
    from data.lessons import load_lessons
    
    st.markdown("""
    Przypisuj zasoby (lekcje, inspiracje, scenariusze) do grup użytkowników.
    
    - **General** = dostępne dla wszystkich
    - **Warta/Heinz/Milwaukee/Degen** = tylko dla danej grupy
    """)
    
    # Wybór typu zasobu
    resource_type_options = {
        "📚 Lekcje": "lessons",
        "💡 Inspiracje (kategorie)": "inspirations_categories",
        "🎮 Business Games (scenariusze)": "business_games_scenarios",
        "🎯 Business Games (typy)": "business_games_types"
    }
    
    selected_type_name = st.selectbox("Wybierz typ zasobu:", list(resource_type_options.keys()))
    resource_type = resource_type_options[selected_type_name]
    
    # Pobierz listę zasobów
    tags_data = load_resource_tags()
    resources_dict = tags_data.get(resource_type, {})
    
    # Dla lekcji pobierz z plików
    if resource_type == "lessons":
        lessons = load_lessons()
        resource_ids = list(lessons.keys())
        resource_display = {lid: lessons[lid].get('title', lid) for lid in resource_ids}
    else:
        resource_ids = list(resources_dict.keys())
        resource_display = {rid: rid for rid in resource_ids}
    
    if not resource_ids:
        st.info(f"Brak zasobów typu {selected_type_name}")
        
        # Możliwość dodania nowego
        st.markdown("---")
        st.markdown("#### ➕ Dodaj nowy zasób")
        new_resource_id = st.text_input("ID zasobu:")
        if st.button("Dodaj") and new_resource_id:
            if new_resource_id not in resources_dict:
                set_resource_tags(resource_type, new_resource_id, ["General"])
                st.success(f"Dodano: {new_resource_id}")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Ten zasób już istnieje!")
        return
    
    # Wybór zasobu do edycji
    selected_resource = st.selectbox(
        "Wybierz zasób do edycji:",
        options=resource_ids,
        format_func=lambda x: resource_display.get(x, x)
    )
    
    if selected_resource:
        st.markdown("---")
        st.markdown(f"### Edycja tagów: **{resource_display.get(selected_resource, selected_resource)}**")
        
        # Pobierz aktualne tagi
        current_tags = get_resource_tags(resource_type, selected_resource)
        
        # Wyświetl checkboxy dla każdej grupy
        companies = get_all_companies()
        new_tags = []
        
        st.markdown("**Zaznacz grupy, które mają dostęp:**")
        
        cols = st.columns(len(companies))
        for idx, company in enumerate(companies):
            with cols[idx]:
                is_checked = company['code'] in current_tags
                if st.checkbox(
                    company['display_name'],
                    value=is_checked,
                    key=f"tag_{resource_type}_{selected_resource}_{company['code']}"
                ):
                    new_tags.append(company['code'])
        
        # Pokaż aktualny stan
        st.markdown("---")
        st.markdown("**Aktualne tagi:**")
        if current_tags:
            tag_labels = [next((c['display_name'] for c in companies if c['code'] == tag), tag) for tag in current_tags]
            st.info(", ".join(tag_labels))
        else:
            st.warning("Brak tagów (zasób niedostępny dla nikogo!)")
        
        # Przycisk zapisu
        if st.button("💾 Zapisz tagi", type="primary", use_container_width=True):
            if not new_tags:
                st.error("Musisz wybrać przynajmniej jedną grupę!")
            else:
                if set_resource_tags(resource_type, selected_resource, new_tags):
                    st.success(f"✅ Zaktualizowano tagi dla {selected_resource}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Błąd podczas zapisywania tagów")
    
    # Szybki podgląd wszystkich tagów
    st.markdown("---")
    st.markdown("### 📋 Przegląd wszystkich tagów")
    
    if st.checkbox("Pokaż wszystkie tagi"):
        companies = get_all_companies()
        company_display = {c['code']: c['display_name'] for c in companies}
        
        for resource_id in resource_ids:
            tags = get_resource_tags(resource_type, resource_id)
            tag_labels = [company_display.get(tag, tag) for tag in tags]
            st.write(f"**{resource_display.get(resource_id, resource_id)}**: {', '.join(tag_labels)}")
