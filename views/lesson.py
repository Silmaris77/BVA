import streamlit as st
from data.lessons import load_lessons
from data.users import load_user_data, save_user_data
from utils.components import zen_header, zen_button, notification, content_section, tip_block, quote_block, progress_bar, embed_content, lesson_card
from utils.components import youtube_video  # Osobny import dla youtube_video
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view
from utils.scroll_utils import scroll_to_top
from utils.media_embed import render_embedded_content
from utils.media_embed import render_embedded_content
from utils.lesson_progress import (
    award_fragment_xp, get_lesson_fragment_progress, calculate_lesson_completion,
    is_lesson_fully_completed, get_fragment_xp_breakdown, mark_lesson_as_completed,
    check_and_mark_lesson_completion
)
from utils.real_time_updates import get_live_user_stats, live_xp_indicator, show_xp_notification
from utils.streamlit_compat import tabs_with_fallback, display_compatibility_info
from views.skills_new import show_skill_tree
from views.admin import is_lesson_accessible

def get_difficulty_stars(difficulty):
    """Konwertuje poziom trudności (liczba lub tekst) na odpowiednią liczbę gwiazdek."""
    difficulty_map = {
        "beginner": 1,
        "podstawowy": 1,
        "intermediate": 2,
        "średni": 2,
        "średniozaawansowany": 3,
        "advanced": 4,
        "zaawansowany": 4,
        "expert": 5,
        "ekspercki": 5
    }
    
    if isinstance(difficulty, str):
        difficulty_level = difficulty_map.get(difficulty.lower(), 1)
    else:
        pass
        try:
            difficulty_level = int(difficulty)
        except (ValueError, TypeError):
            difficulty_level = 1
    
    return '⭐' * difficulty_level

def show_lesson():
    """Show lesson view with tabs for lessons and course structure"""
    
    # Przewiń na górę strony
    scroll_to_top()
    
    # Sprawdź czy został zażądany reset stanu lekcji przez kliknięcie "Lekcje" w nawigacji
    if st.session_state.get('lesson_reset_requested', False):
        # Reset lekcji zażądany - wyczyść stan
        st.session_state.current_lesson = None
        if 'lesson_finished' in st.session_state:
            st.session_state.lesson_finished = False
        # Usuń flagę resetu po jednorazowym użyciu
        st.session_state.lesson_reset_requested = False
    
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    zen_header("Lekcje")
    
    # Wyświetl informacje o kompatybilności w trybie dev
    display_compatibility_info()
    
    # Create main tabs with compatibility fallback
    tab1 = st.container()  # Używamy tylko jednego kontenera zamiast tabów
    
    with tab1:
        show_lessons_content()
    
    # with tab2:
    #     show_skill_tree()

def show_lessons_by_category(lessons_by_category, completed_lessons, device_type, accessible=True):
    """Helper function to show lessons grouped by category"""
    for category, category_lessons in lessons_by_category.items():
        # Utwórz kolumny dla responsywnego układu
        # Na urządzeniach mobilnych - 1 kolumna, na desktopie - 2 kolumny
        if device_type == 'mobile':
            columns = st.columns(1)
        else:
            columns = st.columns(1)
        
        # Wyświetlaj lekcje w kolumnach
        for i, (lesson_id, lesson) in enumerate(category_lessons):
            # Sprawdź, czy lekcja jest ukończona
            is_completed = lesson_id in completed_lessons
            
            # Wybierz kolumnę (naprzemiennie dla 2 kolumn, zawsze pierwsza dla 1 kolumny)
            column_index = i % len(columns)
            
            with columns[column_index]:
                if accessible:
                    # Lekcja dostępna - normalne wyświetlanie
                    lesson_card(
                        title=lesson.get('title', 'Lekcja'),
                        description=lesson.get('description', 'Ta lekcja wprowadza podstawowe zasady...'),
                        xp=lesson.get('xp_reward', 30),
                        difficulty=lesson.get('difficulty', 'beginner'),
                        category=lesson.get('tag', category),
                        completed=is_completed,
                        button_text="Powtórz lekcję" if is_completed else "Rozpocznij",
                        button_key=f"start_{lesson_id}",
                        lesson_id=lesson_id,
                        on_click=lambda _, lid=lesson_id: (
                            setattr(st.session_state, 'current_lesson', lid),
                            setattr(st.session_state, 'lesson_step', 'intro'),
                            setattr(st.session_state, 'quiz_score', 0) if 'quiz_score' in st.session_state else None,
                            scroll_to_top(),
                            st.rerun()
                        )
                    )
                else:
                    # Lekcja niedostępna - użyj lesson_card z odpowiednimi parametrami
                    lesson_card(
                        title=f"🔒 {lesson.get('title', 'Lekcja')}",
                        description=lesson.get('description', 'Ta lekcja wprowadza podstawowe zasady...'),
                        xp=lesson.get('xp_reward', 30),
                        difficulty=lesson.get('difficulty', 'beginner'),
                        category=lesson.get('tag', category),
                        completed=False,
                        accessible=False,  # Niedostępna lekcja
                        lesson_id=lesson_id
                    )

def show_lessons_content():
    """Show the lessons content with tabs for available and unavailable lessons"""
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    lessons = load_lessons()
    
    # Check if we're viewing a specific lesson or the overview
    if 'current_lesson' not in st.session_state or not st.session_state.current_lesson:
        # WIDOK PRZEGLĄDU LEKCJI
        # Pobierz dane użytkownika dla oznaczenia ukończonych lekcji
        from data.users import get_current_user_data
        user_data = get_current_user_data(st.session_state.username)
        completed_lessons = user_data.get('completed_lessons', [])
        
        # Sprawdź dostępność lekcji dla użytkownika
        username = st.session_state.get('username')
        
        # Podziel lekcje na dostępne i niedostępne
        available_lessons = {}
        unavailable_lessons = {}
        
        for lesson_id, lesson in lessons.items():
            is_accessible = is_lesson_accessible(username, lesson_id) if username else True
            category = lesson.get("category", "Inne")
            
            if is_accessible:
                if category not in available_lessons:
                    available_lessons[category] = []
                available_lessons[category].append((lesson_id, lesson))
            else:
                if category not in unavailable_lessons:
                    unavailable_lessons[category] = []
                unavailable_lessons[category].append((lesson_id, lesson))
        
        # Sortuj lekcje w każdej kategorii: nieukończone najpierw, potem ukończone
        for category in available_lessons:
            available_lessons[category].sort(key=lambda x: (x[0] in completed_lessons, x[0]))
        
        for category in unavailable_lessons:
            unavailable_lessons[category].sort(key=lambda x: (x[0] in completed_lessons, x[0]))
        
        # Utwórz tabs dla dostępnych i niedostępnych lekcji
        tab_available, tab_unavailable = st.tabs(["📚 Lekcje dostępne", "🔒 Lekcje niedostępne"])
        
        with tab_available:
            scroll_to_top()
            st.markdown("### Dostępne lekcje")
            if available_lessons:
                show_lessons_by_category(available_lessons, completed_lessons, device_type, accessible=True)
            else:
                st.info("Brak dostępnych lekcji.")
        
        with tab_unavailable:
            scroll_to_top()
            st.markdown("### Niedostępne lekcje")
            if unavailable_lessons:
                show_lessons_by_category(unavailable_lessons, completed_lessons, device_type, accessible=False)
            else:
                st.info("Wszystkie lekcje są dostępne!")

    else:
        # Kod wyświetlania pojedynczej lekcji
        lessons = load_lessons()  # Dodaj ponowne ładowanie lekcji  
        lesson_id = st.session_state.current_lesson
        if lesson_id not in lessons:
            # Automatycznie wyczyść nieprawidłowe ID lekcji i wróć do listy
            st.session_state.current_lesson = None
            st.rerun()
            return
        
        lesson = lessons[lesson_id]

        # Sprawdź dostępność lekcji
        username = st.session_state.get('username')
        if username and not is_lesson_accessible(username, lesson_id):
            st.error("🔒 **Dostęp do tej lekcji jest ograniczony**")
            st.warning("Ta lekcja nie jest obecnie dostępna dla Twojego konta. Skontaktuj się z administratorem, aby uzyskać dostęp.")
            
            # Przycisk powrotu do listy lekcji
            if st.button("⬅️ Wróć do listy lekcji"):
                st.session_state.current_lesson = None
                st.rerun()
            return
            
        if 'lesson_step' not in st.session_state:
            st.session_state.lesson_step = 'intro'
        if 'quiz_score' not in st.session_state:
            st.session_state.quiz_score = 0
        # Get current user's lesson progress using the new fragment system
        fragment_progress = get_lesson_fragment_progress(lesson_id)
        # Initialize legacy session progress for UI compatibility
        if 'lesson_progress' not in st.session_state:
            st.session_state.lesson_progress = {
                'intro': fragment_progress.get('intro_completed', False),
                'content': fragment_progress.get('content_completed', False),
                'practical_exercises': fragment_progress.get('practical_exercises_completed', False),
                'reflection': fragment_progress.get('reflection_completed', False),  # backward compatibility
                'application': fragment_progress.get('application_completed', False),  # backward compatibility
                'summary': fragment_progress.get('summary_completed', False),
            'summary': fragment_progress.get('summary_completed', False),
                'total_xp_earned': fragment_progress.get('total_xp_earned', 0),
                'steps_completed': 0,
                'quiz_scores': {},
                'answers': {}
            }# Oblicz całkowitą liczbę dostępnych kroków w tej lekcji
        available_steps = ['intro', 'content', 'summary']
        if 'sections' in lesson:
            # Usunięto opening_quiz i closing_quiz z osobnych kroków - są teraz zintegrowane w zakładkach
            if 'practical_exercises' in lesson.get('sections', {}):
                available_steps.append('practical_exercises')
            elif 'reflection' in lesson.get('sections', {}) or 'application' in lesson.get('sections', {}):
                # Backward compatibility dla starszych lekcji
                if 'reflection' in lesson.get('sections', {}):
                    available_steps.append('reflection')
                if 'application' in lesson.get('sections', {}):
                    available_steps.append('application')
          # Ustal kolejność kroków (bez opening_quiz i closing_quiz jako osobnych kroków)
        step_order = ['intro']
        step_order.extend(['content'])
        
        # Nowa sekcja ćwiczeń praktycznych zamiast osobnych reflection i application
        # closing_quiz jest teraz zintegrowany w sekcji practical_exercises
        if 'practical_exercises' in available_steps:
            step_order.append('practical_exercises')
        elif 'reflection' in available_steps or 'application' in available_steps:
            # Backward compatibility dla starszych lekcji
            if 'reflection' in available_steps:
                step_order.append('reflection')
            if 'application' in available_steps:
                step_order.append('application')
        
        # closing_quiz usunięty jako osobny krok - jest teraz w zakładce practical_exercises
        step_order.append('summary')
        
        total_steps = len(step_order)
        base_xp = lesson.get('xp_reward', 100)        # Mapowanie kroków do nazw wyświetlanych (usunięto opening_quiz i closing_quiz)
        step_names = {
            'intro': 'Wprowadzenie',
            'content': 'Nauka',
            'practical_exercises': 'Praktyka',
            'reflection': 'Refleksja',  # backward compatibility
            'application': 'Zadania praktyczne',  # backward compatibility
            'summary': 'Podsumowanie'
        }
        
        # Specjalne nazwy dla lekcji "Wprowadzenie do neuroprzywództwa"
        if lesson.get('title') == 'Wprowadzenie do neuroprzywództwa':
            step_names = {
                'intro': 'Wprowadzenie',
                'content': 'Case Study',
                'practical_exercises': 'O CO TU CHODZI',
                'reflection': 'Refleksja',  # backward compatibility
                'application': 'Zadania praktyczne',  # backward compatibility
                'summary': 'AUTODIAGNOZA'
            }# Mapowanie kroków do wartości XP (usunięto opening_quiz i closing_quiz)
        step_xp_values = {
            'intro': int(base_xp * 0.05),          # 5% całkowitego XP
            'content': int(base_xp * 0.30),        # 30% całkowitego XP (Merytoryka)
            'practical_exercises': int(base_xp * 0.60),  # 60% całkowitego XP (nowa połączona sekcja z quizem końcowym)
            'reflection': int(base_xp * 0.20),     # 20% całkowitego XP (backward compatibility)
            'application': int(base_xp * 0.20),    # 20% całkowitego XP (backward compatibility)
            'summary': int(base_xp * 0.05)         # 5% całkowitego XP
        }
        
        # Oblicz rzeczywiste maksimum XP jako sumę wszystkich dostępnych kroków
        max_xp = sum(step_xp_values[step] for step in step_order)
          # Znajdź indeks obecnego kroku i następnego kroku
        current_step_idx = step_order.index(st.session_state.lesson_step) if st.session_state.lesson_step in step_order else 0
        next_step_idx = min(current_step_idx + 1, len(step_order) - 1)
        next_step = step_order[next_step_idx]
        
        # Style dla paska postępu i interfejsu
        st.markdown("""
        <style>
        .progress-container {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 10px 15px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .progress-text {
            font-weight: bold;
            font-size: 16px;
        }
        .xp-counter {
            color: #4CAF50;
            font-weight: bold;
            font-size: 18px;
        }
        .stTabs [data-baseweb="tab-panel"] {
            padding: 25px 15px 15px 15px;
        }        .next-button {
            margin-top: 20px;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
        }          /* Przyciski "Dalej" o szerokości odpowiadającej przyciskom nawigacji poziomej */
        .next-button .stButton > button {
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
            height: 48px !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            display: inline-block !important;
            margin: 0 auto !important;
            font-size: 0.9rem !important;
            line-height: 1.2 !important;
        }
        
        /* Zapewnij, że kontener przycisku ma odpowiednią szerokość */
        .next-button .stButton {
            width: 280px !important;
            max-width: 280px !important;
            margin: 0 auto !important;
            display: block !important;
        }
        
        /* Wymuś szerokość na elemencie div zawierającym przycisk */
        .next-button > div {
            width: 280px !important;
            max-width: 280px !important;
            margin: 0 auto !important;
        }
        
        /* Dodatkowe wymuszenie dla wszystkich elementów w kontenerze */
        .next-button * {
            max-width: 280px !important;
        }
        
        /* Style dla expanderów */
        .st-emotion-cache-1oe5cao {
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 16px;
            background-color: rgba(248,249,251,0.8);
        }
        .st-emotion-cache-1oe5cao:hover {
            background-color: rgba(242,244,248,1); 
        }
        .st-emotion-cache-16idsys p {
            font-size: 1rem;
            line-height: 1.6;
        }
        .st-expander {
            border: none !important;
        }

        /* Specjalne style dla urządzeń mobilnych */
        @media (max-width: 768px) {
            /* Zwiększ szerokość głównego kontenera */
            .main .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                max-width: 100% !important;
            }
            
            /* Zmniejsz marginesy i padding dla sekcji tekstowych */
            .stMarkdown, .st-emotion-cache-1oe5cao {
                margin-left: 0 !important;
                margin-right: 0 !important;
                padding-left: 5px !important;
                padding-right: 5px !important;
            }
            
            /* Zwiększ line-height i zmniejsz font-size dla lepszej czytelności */
            .st-emotion-cache-16idsys p, .stMarkdown p {
                font-size: 0.9rem !important;
                line-height: 1.8 !important;
                margin-bottom: 1rem !important;
            }
            
            /* Specjalne style dla treści w gradientowych divach */
            div[style*="linear-gradient"] {
                margin-left: -10px !important;
                margin-right: -10px !important;
                padding-left: 15px !important;
                padding-right: 15px !important;
            }
            
            /* Zmniejsz padding dla zagnieżdżonych kontenerów */
            div[style*="padding: 25px"] {
                padding: 15px 10px !important;
            }
            
            /* Zwiększ szerokość tabs na mobile */
            .stTabs [data-baseweb="tab-list"] {
                flex-wrap: nowrap !important;
                overflow-x: auto !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                min-width: auto !important;
                padding: 8px 12px !important;
                font-size: 0.85rem !important;
            }
            
            /* Większy obszar klikalny dla expanderów */
            .st-expander {
                margin-bottom: 12px;
            }
            
            .st-expander .st-emotion-cache-16idsys p {
                font-size: 0.9rem !important; /* Nieco mniejsza czcionka na małych ekranach */
                line-height: 1.7 !important;
            }
            
            /* Zwiększony obszar kliknięcia dla nagłówka expandera */
            .st-expander-header {
                padding: 15px 10px !important;
                font-size: 1.1rem !important;
                font-weight: 600 !important;
                min-height: 50px;
            }
            
            /* Dodaj wskaźnik rozwijania */
            .st-expander:not(.st-emotion-cache-xujm5h) .st-expander-header::after {
                content: '▼';
                float: right;
                margin-left: 10px;
                transition: transform 0.3s;
            }
            
            .st-expander.st-emotion-cache-xujm5h .st-expander-header::after {
                content: '▲';
                float: right;
                margin-left: 10px;
            }        }        </style>
        """, unsafe_allow_html=True)        # Sidebar pozostaje pusty - nawigacja przeniesiona na główną stronę
        with st.sidebar:
            pass

        # Nawigacja pozioma na głównej stronie
        def show_horizontal_lesson_navigation():
            """Wyświetla poziomą nawigację lekcji na głównej stronie"""
            st.markdown("""
            <style>
            .lesson-nav-container {
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                padding: 1rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .lesson-nav-title {
                text-align: center;
                font-size: 1.1rem;
                font-weight: 600;
                color: #334155;
                margin-bottom: 1rem;
            }            /* Zapewnij jednakową szerokość przycisków nawigacji lekcji - 280px jak przycisk "Dalej" */
            .lesson-nav-container .stButton > button {
                width: 280px !important;
                min-width: 280px !important;
                max-width: 280px !important;
                height: 48px !important;
                white-space: nowrap !important;
                overflow: hidden !important;
                text-overflow: ellipsis !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                font-size: 0.9rem !important;
                line-height: 1.2 !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="lesson-nav-container">', unsafe_allow_html=True)
            st.markdown('<div class="lesson-nav-title">📚 Nawigacja lekcji</div>', unsafe_allow_html=True)
            
            # Stwórz kolumny dla przycisków nawigacji z responsive grid
            available_steps_in_order = [step for step in step_order if step in available_steps]
            
            # Użyj responsive grid: 2 kolumny na desktop i tablet, 1 na mobile
            device_type = get_device_type()
            if device_type == 'mobile':
                cols_per_row = 1
            else:  # desktop i tablet
                cols_per_row = 2
            
            # Podziel przyciski na wiersze
            rows = []
            for i in range(0, len(available_steps_in_order), cols_per_row):
                rows.append(available_steps_in_order[i:i + cols_per_row])
            
            # Wyświetl każdy wiersz osobno
            for row_steps in rows:
                cols = st.columns(cols_per_row)
                for col_index, step in enumerate(row_steps):
                    if col_index < len(cols):  # Sprawdź czy kolumna istnieje
                        with cols[col_index]:
                            step_name = step_names.get(step, step.capitalize())
                            step_number = step_order.index(step) + 1  # Numer kroku w oryginalnej kolejności
                            
                            # Sprawdź status kroku
                            is_completed = st.session_state.lesson_progress.get(step, False)
                            is_current = (step == st.session_state.lesson_step)
                            
                            # Specjalna logika dla sekcji "Podsumowanie" - wymaga zaliczenia quizu końcowego
                            if step == 'summary':
                                # Sprawdź czy quiz końcowy został zdany z minimum 75%
                                lesson_title = lesson.get("title", "")
                                closing_quiz_key = f"closing_quiz_{lesson_id}"
                                closing_quiz_state = st.session_state.get(closing_quiz_key, {})
                                quiz_passed = closing_quiz_state.get("quiz_passed", False)
                                
                                # Dla lekcji "Wprowadzenie do neuroprzywództwa" nie ma blokowania
                                if lesson_title != "Wprowadzenie do neuroprzywództwa" and not quiz_passed and not is_current:
                                    # Blokuj dostęp do podsumowania jeśli quiz nie został zdany
                                    button_text = f"🔒 {step_number}. {step_name}"
                                    button_type = "secondary"
                                    disabled = True
                                    help_text = "Musisz zaliczyć quiz końcowy (min. 75%) w sekcji 'Praktyka', aby odblokować podsumowanie"
                                elif is_current:
                                    button_text = f"👉 {step_number}. {step_name}"
                                    button_type = "primary"
                                    disabled = False
                                    help_text = f"Przejdź do: {step_name}"
                                elif is_completed:
                                    button_text = f"✅ {step_number}. {step_name}"
                                    button_type = "secondary"
                                    disabled = False
                                    help_text = f"Przejdź do: {step_name}"
                                else:
                                    button_text = f"{step_number}. {step_name}"
                                    button_type = "secondary"
                                    disabled = True
                                    help_text = f"Ukończ poprzednie kroki aby odblokować: {step_name}"
                            else:
                                # Standardowa logika dla innych kroków
                                if is_current:
                                    # Aktualny krok - niebieski
                                    button_text = f"👉 {step_number}. {step_name}"
                                    button_type = "primary"
                                    disabled = False
                                    help_text = f"Przejdź do: {step_name}"
                                elif is_completed:
                                    # Ukończony krok - zielony z checkmarkiem
                                    button_text = f"✅ {step_number}. {step_name}"
                                    button_type = "secondary"
                                    disabled = False
                                    help_text = f"Przejdź do: {step_name}"
                                else:
                                    # Przyszły krok - szary, zablokowany
                                    button_text = f"{step_number}. {step_name}"
                                    button_type = "secondary"
                                    disabled = True
                                    help_text = f"Ukończ poprzednie kroki aby odblokować: {step_name}"
                            
                            # Wyświetl przycisk
                            if st.button(
                                button_text, 
                                key=f"nav_step_{step}_{col_index}", 
                                type=button_type,
                                disabled=disabled,
                                width='stretch',
                                help=help_text
                            ):
                                if not is_current:  # Tylko jeśli nie jest to aktualny krok
                                    st.session_state.lesson_step = step
                                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Wyświetl poziomą nawigację
        show_horizontal_lesson_navigation()

        # Main content
        st.markdown("<div class='st-bx'>", unsafe_allow_html=True)# Nagłówek sekcji
        current_section_title = step_names.get(st.session_state.lesson_step, st.session_state.lesson_step.capitalize())
        st.markdown(f"<h1>{current_section_title}</h1>", unsafe_allow_html=True)
          # Main content logic for each step
        if st.session_state.lesson_step == 'intro':
            # Sprawdź tytuł lekcji, aby ukryć niektóre tabs dla konkretnych lekcji
            lesson_title = lesson.get("title", "")
            
            if lesson_title == "Wprowadzenie do neuroprzywództwa":
                # Dla tej lekcji pokazuj tylko zakładkę "Wprowadzenie"
                intro_tabs = tabs_with_fallback(["Wprowadzenie"])
                
                with intro_tabs[0]:
                    # Wyświetl główne wprowadzenie
                    if isinstance(lesson.get("intro"), dict) and "main" in lesson["intro"]:
                        st.markdown(lesson["intro"]["main"], unsafe_allow_html=True)
                    elif isinstance(lesson.get("intro"), str):
                        st.markdown(lesson["intro"], unsafe_allow_html=True)
                    else:
                        st.warning("Brak treści wprowadzenia.")
            else:
                # Dla wszystkich innych lekcji pokazuj pełne tabs
                intro_tabs = tabs_with_fallback(["Wprowadzenie", "Case Study", "🪞 Quiz Samodiagnozy"])
                
                with intro_tabs[0]:
                    # Wyświetl główne wprowadzenie
                    if isinstance(lesson.get("intro"), dict) and "main" in lesson["intro"]:
                        st.markdown(lesson["intro"]["main"], unsafe_allow_html=True)
                    elif isinstance(lesson.get("intro"), str):
                        st.markdown(lesson["intro"], unsafe_allow_html=True)
                    else:
                        st.warning("Brak treści wprowadzenia.")
            
                with intro_tabs[1]:
                    # Wyświetl studium przypadku
                    if isinstance(lesson.get("intro"), dict) and "case_study" in lesson["intro"]:
                        st.markdown(lesson["intro"]["case_study"], unsafe_allow_html=True)
                    else:
                        st.warning("Brak studium przypadku w tej lekcji.")
            
                with intro_tabs[2]:
                    # Wyświetl quiz samodiagnozy
                    if (isinstance(lesson.get("intro"), dict) and 
                        "quiz_samodiagnozy" in lesson["intro"] and 
                        "questions" in lesson["intro"]["quiz_samodiagnozy"]):
                        
                        st.info("🪞 **Quiz Samodiagnozy** - Ten quiz pomaga Ci lepiej poznać siebie jako lidera. Nie ma tu dobrych ani złych odpowiedzi - chodzi o szczerą autorefleksję. Twoje odpowiedzi nie wpływają na postęp w lekcji.")
                        
                        quiz_data = lesson["intro"]["quiz_samodiagnozy"]
                        quiz_complete, _, earned_points = display_quiz(quiz_data)
                        # Oznacz quiz jako ukończony po wypełnieniu
                        if quiz_complete:
                            quiz_xp_key = f"opening_quiz_xp_{lesson_id}"
                            if not st.session_state.get(quiz_xp_key, False):
                                # Award fragment XP for quiz participation
                                fragment_xp = get_fragment_xp_breakdown(lesson.get('xp_reward', 30))
                                success, earned_xp = award_fragment_xp(lesson_id, 'intro_quiz', fragment_xp['intro'] // 3)  # 1/3 of intro XP
                                st.session_state[quiz_xp_key] = True
                                if success and earned_xp > 0:
                                    show_xp_notification(earned_xp, "za szczerą samorefleksję")
                        
                            st.success("✅ Dziękujemy za szczerą samorefleksję!")
                    
                    elif 'sections' in lesson and 'opening_quiz' in lesson.get('sections', {}):
                        # Backward compatibility - stary format
                        st.info("🪞 **Quiz Samodiagnozy** - Ten quiz pomaga Ci lepiej poznać siebie jako inwestora. Nie ma tu dobrych ani złych odpowiedzi - chodzi o szczerą autorefleksję. Twoje odpowiedzi nie wpływają na postęp w lekcji.")
                        
                        quiz_data = lesson['sections']['opening_quiz']
                        quiz_complete, _, earned_points = display_quiz(quiz_data)
                        # Oznacz quiz jako ukończony po wypełnieniu
                        if quiz_complete:
                            quiz_xp_key = f"opening_quiz_xp_{lesson_id}"
                            if not st.session_state.get(quiz_xp_key, False):
                                # Award fragment XP for quiz participation
                                fragment_xp = get_fragment_xp_breakdown(lesson.get('xp_reward', 30))
                                success, earned_xp = award_fragment_xp(lesson_id, 'intro_quiz', fragment_xp['intro'] // 3)  # 1/3 of intro XP
                                st.session_state[quiz_xp_key] = True
                                if success and earned_xp > 0:
                                    show_xp_notification(earned_xp, "za szczerą samorefleksję")
                            
                            st.success("✅ Dziękujemy za szczerą samorefleksję!")
                            
                            # Dodaj przycisk do ponownego przystąpienia do quizu samodiagnozy
                            st.markdown("---")
                            col1, col2, col3 = st.columns([1, 1, 1])
                            with col2:
                                if st.button("🔄 Przystąp ponownie", key=f"retry_self_diagnosis_legacy_{lesson_id}", help="Możesz ponownie wypełnić quiz samodiagnozy aby zaktualizować swoją autorefleksję", width='stretch'):
                                    # Reset stanu quizu samodiagnozy
                                    quiz_id = f"quiz_{quiz_data.get('title', '').replace(' ', '_').lower()}"
                                    
                                    # Usuń stan główny quizu
                                    if quiz_id in st.session_state:
                                        del st.session_state[quiz_id]
                                    
                                    # Usuń wszystkie odpowiedzi na pytania
                                    for i in range(len(quiz_data.get('questions', []))):
                                        question_key = f"{quiz_id}_q{i}_selected"
                                        if question_key in st.session_state:
                                            del st.session_state[question_key]
                                        
                                        # Usuń także klucze suwaków jeśli istnieją
                                        slider_key = f"{quiz_id}_q{i}_slider"
                                        if slider_key in st.session_state:
                                            del st.session_state[slider_key]
                                    
                                    st.rerun()
                    
                    else:
                        st.info("Ten quiz samodiagnozy nie jest dostępny dla tej lekcji.")
                        
            # Przycisk "Dalej" po wprowadzeniu            
            # Użyj kolumn aby ograniczyć szerokość przycisku
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())}", width='stretch'):
                    # Award fragment XP using the new system
                    success, xp_awarded = award_fragment_xp(lesson_id, 'intro', step_xp_values['intro'])
                    
                    if success and xp_awarded > 0:
                        # Update session state for UI compatibility
                        st.session_state.lesson_progress['intro'] = True
                        st.session_state.lesson_progress['steps_completed'] += 1
                        st.session_state.lesson_progress['total_xp_earned'] += xp_awarded
                        # Show real-time XP notification
                        show_xp_notification(xp_awarded, f"Zdobyłeś {xp_awarded} XP za ukończenie wprowadzenia!")
                        
                        # Refresh user data for real-time updates
                        from utils.real_time_updates import refresh_user_data
                        refresh_user_data()
                        
                        # Sprawdź czy lekcja została ukończona
                        check_and_mark_lesson_completion(lesson_id)
                    
                    # Przejdź do następnego kroku
                    st.session_state.lesson_step = next_step
                    scroll_to_top()
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        elif st.session_state.lesson_step == 'content':
            # Sprawdź strukturę learning - obsługuj zarówno tabs jak i sections
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'learning' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'learning'!")
            else:
                learning_data = lesson['sections']['learning']
                
                # Nowa struktura z tabs (jak w lekcji 11)
                if 'tabs' in learning_data:
                    st.markdown("### 📚 Materiał do nauki")
                    
                    # CSS dla pełnej szerokości expanderów w tabsie "Tekst"
                    st.markdown("""
                        <style>
                        /* Expander w tabsie "Tekst" wypełnia całą szerokość */
                        div[data-testid="stExpander"] {
                            width: 100% !important;
                            margin: 0 !important;
                            border-radius: 8px !important;
                            border: 1px solid #e0e0e0 !important;
                            margin-bottom: 0.5rem !important;
                        }
                        
                        div[data-testid="stExpander"] > div {
                            width: 100% !important;
                            margin: 0 !important;
                        }
                        
                        /* Zawartość expandera również pełna szerokość */
                        div[data-testid="stExpander"] .streamlit-expanderContent {
                            width: 100% !important;
                            padding: 0 !important;
                            margin: 0 !important;
                        }
                        
                        /* Nagłówek expandera pełna szerokość */
                        div[data-testid="stExpander"] .streamlit-expanderHeader {
                            width: 100% !important;
                            margin: 0 !important;
                        }
                        
                        /* Karty wewnątrz expandera mają idealnie dopasowaną szerokość */
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown,
                        div[data-testid="stExpander"] .streamlit-expanderContent div[data-testid="column"],
                        div[data-testid="stExpander"] .streamlit-expanderContent div[data-testid="stVerticalBlock"],
                        div[data-testid="stExpander"] .streamlit-expanderContent > div {
                            width: 100% !important;
                            margin: 0 !important;
                            padding: 0 !important;
                            box-sizing: border-box !important;
                        }
                        
                        /* Wszystkie elementy wewnątrz expandera */
                        div[data-testid="stExpander"] .streamlit-expanderContent * {
                            max-width: 100% !important;
                            box-sizing: border-box !important;
                        }
                        
                        /* Konkretnie dla kart z treścią */
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown > div,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown > div > div {
                            width: 100% !important;
                            margin: 0 !important;
                            padding: 1rem !important;
                            border-radius: 8px !important;
                            box-sizing: border-box !important;
                        }
                        
                        /* Większa czcionka dla tekstów (nie tytułów) w expanderach */
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown p,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown li,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown div:not(h1):not(h2):not(h3):not(h4):not(h5):not(h6) {
                            font-size: 1.5rem !important;
                            line-height: 1.6 !important;
                        }
                        
                        /* Bardziej specyficzne selektory dla tekstów w kartach */
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown > div p,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown > div > div p,
                        div[data-testid="stExpander"] .streamlit-expanderContent .element-container p,
                        div[data-testid="stExpander"] .streamlit-expanderContent [data-testid="stMarkdownContainer"] p {
                            font-size: 1.5rem !important;
                            line-height: 1.6 !important;
                        }
                        
                        /* Uniwersalny selektor dla wszystkich tekstów w expanderach (oprócz nagłówków) */
                        div[data-testid="stExpander"] .streamlit-expanderContent {
                            font-size: 1.5rem !important;
                            line-height: 1.6 !important;
                        }
                        
                        /* Zachowanie normalnego rozmiaru dla tytułów */
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h1,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h2,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h3,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h4,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h5,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h6 {
                            font-size: inherit !important;
                        }
                        
                        /* Responsywność na urządzeniach mobilnych */
                        @media (max-width: 768px) {
                            div[data-testid="stExpander"] {
                                width: 100% !important;
                                margin: 0 0 0.5rem 0 !important;
                            }
                            
                            div[data-testid="stExpander"] .streamlit-expanderContent {
                                padding: 0 !important;
                            }
                            
                            div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown > div,
                            div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown > div > div {
                                padding: 0.75rem !important;
                            }
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    
                    # Utwórz tabs dla różnych typów treści
                    tab_names = [tab.get('title', f'Tab {i+1}') for i, tab in enumerate(learning_data['tabs'])]
                    tabs = st.tabs(tab_names)
                    
                    for i, (tab_container, tab_data) in enumerate(zip(tabs, learning_data['tabs'])):
                        with tab_container:
                            # Wyświetl sekcje w tym tab
                            if 'sections' in tab_data:
                                tab_title = tab_data.get('title', '')
                                
                                # Dla tab "Tekst" używaj expanderów
                                if 'Tekst' in tab_title:
                                    for j, section in enumerate(tab_data['sections']):
                                        section_title = section.get('title', f'Sekcja {j+1}')
                                        # Pierwszy expander domyślnie otwarty
                                        is_expanded = (j == 0)
                                        
                                        with st.expander(section_title, expanded=is_expanded):
                                            # Użyj nowego renderera obsługującego osadzone media
                                            content = section.get('content', 'Brak treści')
                                            render_embedded_content(content, section)
                                else:
                                    # Dla pozostałych tabs (Podcast, Video) standardowe wyświetlanie
                                    for section in tab_data['sections']:
                                        if 'title' in section:
                                            st.markdown(f"### {section['title']}")
                                        
                                        # Użyj nowego renderera obsługującego osadzone media
                                        content = section.get('content', 'Brak treści')
                                        render_embedded_content(content, section)
                            else:
                                st.warning(f"Tab '{tab_data.get('title', 'Bez nazwy')}' nie zawiera sekcji.")
                
                # Stara struktura z sections (kompatybilność wsteczna)
                elif 'sections' in learning_data:
                    # Sprawdź, czy sekcja learning istnieje i czy zawiera sections
                    for i, section in enumerate(learning_data["sections"]):
                        # Dla lekcji "Wprowadzenie do neuroprzywództwa" pierwszy expander jest otwarty
                        is_expanded = False
                        if lesson.get('title') == 'Wprowadzenie do neuroprzywództwa' and i == 0:
                            is_expanded = True
                        
                        with st.expander(section.get("title", f"Sekcja {i+1}"), expanded=is_expanded):
                            # Wyświetl treść sekcji używając nowego renderera
                            content = section.get("content", "Brak treści")
                            render_embedded_content(content, section)
                            
                            # Sprawdź czy sekcja zawiera film YouTube (pojedynczy)
                            if 'video' in section and section['video']:
                                video_data = section['video']
                                video_url = video_data.get('url')
                                video_title = video_data.get('title')
                                video_description = video_data.get('description')
                                
                                if video_url:
                                    from utils.components import youtube_video
                                    youtube_video(
                                        video_url=video_url,
                                        title=video_title,
                                        description=video_description
                                    )
                            
                            # Sprawdź czy sekcja zawiera wiele filmów YouTube (videos)
                            if 'videos' in section and section['videos']:
                                st.markdown("### 🎥 Materiały wideo")
                                for j, video_data in enumerate(section['videos']):
                                    video_url = video_data.get('url')
                                    video_title = video_data.get('title', f'Film {j+1}')
                                    video_description = video_data.get('description')
                                    
                                    if video_url:
                                        from utils.components import youtube_video
                                        youtube_video(
                                            video_url=video_url,
                                            title=video_title,
                                            description=video_description
                                        )
                                        
                                        # Dodaj separator między filmami
                                        if j < len(section['videos']) - 1:
                                            st.markdown("---")
                else:
                    st.error("Sekcja 'learning' nie zawiera ani 'tabs' ani 'sections'!")
                                            # Przycisk "Dalej" po treści lekcji
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())}", width='stretch'):
                    # Award fragment XP using the new system
                    success, xp_awarded = award_fragment_xp(lesson_id, 'content', step_xp_values['content'])
                    
                    if success and xp_awarded > 0:
                        # Update session state for UI compatibility
                        st.session_state.lesson_progress['content'] = True
                        st.session_state.lesson_progress['steps_completed'] += 1
                        st.session_state.lesson_progress['total_xp_earned'] += xp_awarded
                          # Show real-time XP notification
                        show_xp_notification(xp_awarded, f"Zdobyłeś {xp_awarded} XP za zapoznanie się z materiałem!")
                        
                        # Refresh user data for real-time updates
                        from utils.real_time_updates import refresh_user_data
                        refresh_user_data()
                        
                        # Sprawdź czy lekcja została ukończona
                        check_and_mark_lesson_completion(lesson_id)
                    
                    # Przejdź do następnego kroku
                    st.session_state.lesson_step = next_step
                    scroll_to_top()
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.lesson_step == 'practical_exercises':
            # Sekcja ćwiczeń praktycznych - dla lekcji "Wprowadzenie do neuroprzywództwa" specjalna obsługa
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'practical_exercises' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'practical_exercises'!")
            else:
                practical_data = lesson['sections']['practical_exercises']
                lesson_title = lesson.get("title", "")
                
                # Specjalna obsługa dla lekcji "Wprowadzenie do neuroprzywództwa"
                if lesson_title == "Wprowadzenie do neuroprzywództwa" and 'case_study_analysis' in practical_data:
                    case_study_data = practical_data['case_study_analysis']
                    
                    # Wyświetl tytuł i opis
                    st.markdown(f"### {case_study_data['title']}")
                    st.markdown(case_study_data['description'])
                    st.markdown("---")
                    
                    # Wyświetl każdą część case study
                    for part in case_study_data['parts']:
                        with st.expander(f"**Część {part['id']}: {part['title']}**", expanded=False):
                            # Pole tekstowe z case content
                            st.markdown("#### 📝 Opis sytuacji")
                            st.markdown(f"<div style='background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #007bff; margin: 15px 0;'>{part['case_content']}</div>", unsafe_allow_html=True)
                            
                            # Film omawiający tę część
                            st.markdown("#### 🎥 Analiza neurobiologiczna")
                            
                            # Wyświetl video jeśli URL nie jest placeholder
                            video_url = part['video']['url']
                            if "PLACEHOLDER" not in video_url:
                                from utils.components import youtube_video
                                youtube_video(
                                    video_url,
                                    part['video']['title'],
                                    part['video']['description']
                                )
                            else:
                                st.info(f"🎬 **{part['video']['title']}**\n\n{part['video']['description']}\n\n*Film będzie dostępny wkrótce.*")
                            
                            st.markdown("---")
                
                else:
                    # Standardowa obsługa dla innych lekcji
                    # Przygotuj zakładki dla różnych typów ćwiczeń
                    available_tabs = []
                    tab_keys = []
                    sub_tabs_data = {}
                    
                    # Fiszki - sprawdzanie wiedzy (nowa funkcjonalność)
                    if 'flashcards' in practical_data:
                        available_tabs.append("🃏 Fiszki")
                        tab_keys.append('flashcards')
                        sub_tabs_data['flashcards'] = practical_data['flashcards']
                    
                    # Nowa struktura z 'exercises' i 'closing_quiz'
                    if 'exercises' in practical_data:
                        available_tabs.append("🎯 Ćwiczenia")
                        tab_keys.append('exercises')
                        sub_tabs_data['exercises'] = practical_data['exercises']
                    
                    # Case Studies - interaktywne przypadki do analizy
                    if 'case_studies' in practical_data:
                        available_tabs.append("🎭 Case Studies")
                        tab_keys.append('case_studies')
                        sub_tabs_data['case_studies'] = practical_data['case_studies']
                    
                    # Pytania otwarte z oceną AI
                    if 'ai_questions' in practical_data:
                        available_tabs.append("🤖 Pytania AI")
                        tab_keys.append('ai_questions')
                        sub_tabs_data['ai_questions'] = practical_data['ai_questions']
                    
                    if 'closing_quiz' in practical_data:
                        available_tabs.append("🎓 Quiz końcowy")
                        tab_keys.append('closing_quiz')
                        sub_tabs_data['closing_quiz'] = practical_data['closing_quiz']
                    
                    # Backward compatibility - stara struktura bezpośrednia (reflection, application, closing_quiz)
                    if 'reflection' in practical_data:
                        available_tabs.append("📝 Refleksja")
                        tab_keys.append('reflection')
                        sub_tabs_data['reflection'] = practical_data['reflection']
                    
                    if 'application' in practical_data:
                        available_tabs.append("🎯 Zadania Praktyczne")
                        tab_keys.append('application')
                        sub_tabs_data['application'] = practical_data['application']
                    
                    # Renderuj zakładki dla nowej struktury (exercises, closing_quiz)  
                    if available_tabs and 'tabs' not in practical_data:
                        # Wyświetl pod-zakładki dla nowej struktury
                        tabs = tabs_with_fallback(available_tabs)
                        
                        for i, (tab_key, tab_title) in enumerate(zip(tab_keys, available_tabs)):
                            with tabs[i]:
                                if tab_key == 'closing_quiz':
                                    # Specjalna obsługa dla quizu końcowego
                                    lesson_title = lesson.get("title", "")
                                    if lesson_title == "Wprowadzenie do neuroprzywództwa":
                                        # Dla tej lekcji quiz autodiagnozy bez wymogu 75%
                                        st.info("🧠 **Quiz autodiagnozy** - Ten quiz pomoże Ci lepiej poznać swoje podejście do przywództwa. Nie ma tu dobrych ani złych odpowiedzi - chodzi o szczerą autorefleksję.")
                                        
                                        quiz_data = sub_tabs_data['closing_quiz']
                                        quiz_completed, quiz_passed, earned_points = display_quiz(quiz_data, passing_threshold=0)  # Brak wymogu minimum
                                        
                                        # Oznacz quiz jako ukończony po wypełnieniu
                                        if quiz_completed:
                                            # Zapisz stan zaliczenia quizu do sprawdzania w nawigacji
                                            closing_quiz_key = f"closing_quiz_{lesson_id}"
                                            if closing_quiz_key not in st.session_state:
                                                st.session_state[closing_quiz_key] = {}
                                            
                                            st.session_state[closing_quiz_key]["quiz_completed"] = True
                                            st.session_state[closing_quiz_key]["quiz_passed"] = True  # Zawsze zdany dla tej lekcji
                                        
                                        closing_quiz_xp_key = f"closing_quiz_xp_{lesson_id}"
                                        if not st.session_state.get(closing_quiz_xp_key, False):
                                            # Award fragment XP for quiz completion
                                            fragment_xp = get_fragment_xp_breakdown(lesson.get('xp_reward', 30))
                                            # Quiz końcowy dostaje 1/3 z XP practical_exercises 
                                            success, earned_xp = award_fragment_xp(lesson_id, 'closing_quiz', step_xp_values['practical_exercises'] // 3)
                                            st.session_state[closing_quiz_xp_key] = True
                                            if success and earned_xp > 0:
                                                show_xp_notification(earned_xp, f"Zdobyłeś {earned_xp} XP za ukończenie quizu autodiagnozy!")
                                        
                                        st.success("✅ Dziękujemy za szczerą autorefleksję! Możesz teraz przejść do podsumowania.")
                                        
                                        # Dodaj przycisk do ponownego przystąpienia do quizu autodiagnozy
                                        st.markdown("---")
                                        col1, col2, col3 = st.columns([1, 1, 1])
                                        with col2:
                                            if st.button("🔄 Przystąp ponownie", key=f"retry_autodiag_quiz_{lesson_id}", help="Możesz ponownie wypełnić quiz autodiagnozy aby zaktualizować swoją autorefleksję", width='stretch'):
                                                # Reset stanu quizu
                                                quiz_id = f"quiz_{quiz_data.get('title', '').replace(' ', '_').lower()}"
                                                closing_quiz_key = f"closing_quiz_{lesson_id}"  # Definiuj tutaj
                                                
                                                # Usuń stan główny quizu
                                                if quiz_id in st.session_state:
                                                    del st.session_state[quiz_id]
                                                
                                                # Usuń wszystkie odpowiedzi na pytania
                                                for i in range(len(quiz_data.get('questions', []))):
                                                    question_key = f"{quiz_id}_q{i}_selected"
                                                    if question_key in st.session_state:
                                                        del st.session_state[question_key]
                                                    
                                                    # Usuń także klucze suwaków jeśli istnieją
                                                    slider_key = f"{quiz_id}_q{i}_slider"
                                                    if slider_key in st.session_state:
                                                        del st.session_state[slider_key]
                                                
                                                # Reset stanu zaliczenia
                                                if closing_quiz_key in st.session_state:
                                                    st.session_state[closing_quiz_key]["quiz_completed"] = False
                                                    st.session_state[closing_quiz_key]["quiz_passed"] = False
                                                st.rerun()
                                    else:
                                        # Dla wszystkich innych lekcji standardowy quiz końcowy
                                        st.info("🎓 **Quiz końcowy** - Sprawdź swoją wiedzę z tej lekcji. Musisz uzyskać minimum 75% poprawnych odpowiedzi, aby przejść dalej.")
                                        
                                        quiz_data = sub_tabs_data['closing_quiz']
                                        quiz_completed, quiz_passed, earned_points = display_quiz(quiz_data, passing_threshold=75)
                                        
                                        # Oznacz quiz jako ukończony po wypełnieniu
                                        if quiz_completed:
                                            # Zapisz stan zaliczenia quizu do sprawdzania w nawigacji
                                            closing_quiz_key = f"closing_quiz_{lesson_id}"
                                            if closing_quiz_key not in st.session_state:
                                                st.session_state[closing_quiz_key] = {}
                                            
                                            st.session_state[closing_quiz_key]["quiz_completed"] = True
                                            st.session_state[closing_quiz_key]["quiz_passed"] = quiz_passed
                                            
                                            closing_quiz_xp_key = f"closing_quiz_xp_{lesson_id}"
                                            if not st.session_state.get(closing_quiz_xp_key, False):
                                                # Award fragment XP for quiz completion
                                                fragment_xp = get_fragment_xp_breakdown(lesson.get('xp_reward', 30))
                                                # Quiz końcowy dostaje 1/3 z XP practical_exercises 
                                                success, earned_xp = award_fragment_xp(lesson_id, 'closing_quiz', step_xp_values['practical_exercises'] // 3)
                                                st.session_state[closing_quiz_xp_key] = True
                                                if success and earned_xp > 0:
                                                    show_xp_notification(earned_xp, f"Zdobyłeś {earned_xp} XP za ukończenie quizu końcowego!")
                                            
                                            if quiz_passed:
                                                st.success("✅ Gratulacje! Zaliczyłeś quiz końcowy! Możesz teraz przejść do podsumowania.")
                                            else:
                                                st.error("❌ Aby przejść do podsumowania, musisz uzyskać przynajmniej 75% poprawnych odpowiedzi. Spróbuj ponownie!")
                                                
                                                # Dodaj przycisk do ponowienia quizu
                                                st.markdown("---")
                                                col1, col2, col3 = st.columns([1, 1, 1])
                                                with col2:
                                                    if st.button("🔄 Spróbuj ponownie", key=f"retry_closing_quiz_{lesson_id}", type="primary", width='stretch'):
                                                        # Reset stanu quizu
                                                        quiz_id = f"quiz_{quiz_data.get('title', '').replace(' ', '_').lower()}"
                                                        if quiz_id in st.session_state:
                                                            del st.session_state[quiz_id]
                                                        # Reset stanu zaliczenia
                                                        if closing_quiz_key in st.session_state:
                                                            st.session_state[closing_quiz_key]["quiz_completed"] = False
                                                            st.session_state[closing_quiz_key]["quiz_passed"] = False
                                                        st.rerun()
                                elif tab_key == 'exercises':
                                    # Standardowa obsługa dla zakładki exercises
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wyświetl opis zakładki jeśli istnieje
                                    if 'description' in tab_data:
                                        st.info(tab_data['description'])
                                    
                                    # Wyświetl sekcje w zakładce
                                    if 'sections' in tab_data:
                                        for section in tab_data['sections']:
                                            st.markdown(f"### {section.get('title', 'Sekcja')}")
                                            st.markdown(section.get('content', 'Brak treści'), unsafe_allow_html=True)
                                    else:
                                        st.warning(f"Zakładka '{tab_title}' nie zawiera sekcji do wyświetlenia.")
                                
                                elif tab_key == 'flashcards':
                                    # Obsługa fiszek
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wyświetl tytuł i opis sekcji
                                    if 'title' in tab_data:
                                        st.markdown(f"### {tab_data['title']}")
                                    if 'description' in tab_data:
                                        st.info(tab_data['description'])
                                    
                                    # Obsługa fiszek
                                    if 'cards' in tab_data:
                                        cards = tab_data['cards']
                                        
                                        # Inicjalizacja stanu fiszek
                                        flashcard_key = f"flashcards_{lesson_id}"
                                        if flashcard_key not in st.session_state:
                                            st.session_state[flashcard_key] = {
                                                'current_card': 0,
                                                'show_back': False,
                                                'studied_cards': set(),
                                                'correct_answers': set(),
                                                'incorrect_answers': set()
                                            }
                                        
                                        flashcard_state = st.session_state[flashcard_key]
                                        total_cards = len(cards)
                                        
                                        if total_cards > 0:
                                            # Aktualna fiszka
                                            current_card = cards[flashcard_state['current_card']]
                                            card_id = current_card['id']
                                            
                                            # Wyświetl kartę
                                            if not flashcard_state['show_back']:
                                                # Przód karty
                                                st.markdown(f"### 🃏 Fiszka {flashcard_state['current_card'] + 1}/{total_cards}")
                                                
                                                # Pytanie
                                                st.markdown(f"""
                                                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                                           padding: 30px; border-radius: 15px; color: white; 
                                                           margin: 20px 0; text-align: center; min-height: 200px; 
                                                           display: flex; align-items: center; justify-content: center;'>
                                                    <h3 style='color: white; margin: 0; font-size: 1.3rem; line-height: 1.4;'>
                                                        {current_card['front']}
                                                    </h3>
                                                </div>
                                                """, unsafe_allow_html=True)
                                                
                                                # Przycisk pokazania odpowiedzi
                                                col1, col2, col3 = st.columns([1, 2, 1])
                                                with col2:
                                                    if st.button("🔄 Pokaż odpowiedź", key=f"show_back_{card_id}", type="primary", width="stretch"):
                                                        flashcard_state['show_back'] = True
                                                        st.rerun()
                                            
                                            else:
                                                # Tył karty
                                                st.markdown(f"### 🃏 Fiszka {flashcard_state['current_card'] + 1}/{total_cards}")
                                                
                                                # Pytanie (mniejsze)
                                                st.markdown(f"""
                                                <div style='background: #f8f9fa; padding: 15px; border-radius: 10px; 
                                                           border-left: 4px solid #667eea; margin: 15px 0;'>
                                                    <strong>Pytanie:</strong> {current_card['front']}
                                                </div>
                                                """, unsafe_allow_html=True)
                                                
                                                # Odpowiedź
                                                st.markdown(f"""
                                                <div style='background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); 
                                                           padding: 30px; border-radius: 15px; color: white; 
                                                           margin: 20px 0; min-height: 150px;'>
                                                    <h4 style='color: white; margin-bottom: 15px;'>✅ Odpowiedź:</h4>
                                                    <p style='color: white; margin: 0; font-size: 1.1rem; line-height: 1.5;'>
                                                        {current_card['back']}
                                                    </p>
                                                </div>
                                                """, unsafe_allow_html=True)
                                                
                                                # Ocena zrozumienia
                                                st.markdown("#### Jak dobrze znałeś odpowiedź?")
                                                col1, col2, col3 = st.columns(3)
                                                
                                                with col1:
                                                    if st.button("❌ Nie wiedziałem", key=f"incorrect_{card_id}", type="secondary", width="stretch"):
                                                        flashcard_state['studied_cards'].add(card_id)
                                                        flashcard_state['incorrect_answers'].add(card_id)
                                                        flashcard_state['correct_answers'].discard(card_id)  # Usuń z poprawnych jeśli było
                                                        flashcard_state['show_back'] = False
                                                        flashcard_state['current_card'] = (flashcard_state['current_card'] + 1) % total_cards
                                                        st.rerun()
                                                
                                                with col2:
                                                    if st.button("🤔 Częściowo", key=f"partial_{card_id}", width="stretch"):
                                                        flashcard_state['studied_cards'].add(card_id)
                                                        # Częściowa wiedza = nie dodawaj do żadnej kategorii
                                                        flashcard_state['show_back'] = False
                                                        flashcard_state['current_card'] = (flashcard_state['current_card'] + 1) % total_cards
                                                        st.rerun()
                                                
                                                with col3:
                                                    if st.button("✅ Wiedziałem", key=f"correct_{card_id}", type="primary", width="stretch"):
                                                        flashcard_state['studied_cards'].add(card_id)
                                                        flashcard_state['correct_answers'].add(card_id)
                                                        flashcard_state['incorrect_answers'].discard(card_id)  # Usuń z niepoprawnych jeśli było
                                                        flashcard_state['show_back'] = False
                                                        flashcard_state['current_card'] = (flashcard_state['current_card'] + 1) % total_cards
                                                        st.rerun()
                                            
                                            # Funkcje dodatkowe
                                            st.markdown("---")
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                if st.button("🔄 Reset postępu", key=f"reset_flashcards_{lesson_id}"):
                                                    flashcard_state['current_card'] = 0
                                                    flashcard_state['show_back'] = False
                                                    flashcard_state['studied_cards'] = set()
                                                    flashcard_state['correct_answers'] = set()
                                                    flashcard_state['incorrect_answers'] = set()
                                                    st.success("Reset postępu fiszek!")
                                                    st.rerun()
                                            
                                            with col2:
                                                if st.button("🎯 Tylko niepoprawne", key=f"review_incorrect_{lesson_id}", disabled=len(flashcard_state['incorrect_answers']) == 0):
                                                    # Znajdź pierwszą niepoprawną kartę
                                                    for i, card in enumerate(cards):
                                                        if card['id'] in flashcard_state['incorrect_answers']:
                                                            flashcard_state['current_card'] = i
                                                            flashcard_state['show_back'] = False
                                                            break
                                                    st.rerun()
                                            
                                            # Statystyki nauki na dole
                                            st.markdown("---")
                                            st.markdown("### 📊 Statystyki nauki")
                                            
                                            studied_count = len(flashcard_state['studied_cards'])
                                            correct_count = len(flashcard_state['correct_answers'])
                                            incorrect_count = len(flashcard_state['incorrect_answers'])
                                            
                                            # Wyświetl postęp
                                            col1, col2, col3, col4 = st.columns(4)
                                            with col1:
                                                st.metric("Przejrzane", f"{studied_count}/{total_cards}")
                                            with col2:
                                                st.metric("Poprawne", correct_count)
                                            with col3:
                                                st.metric("Niepoprawne", incorrect_count)
                                            with col4:
                                                accuracy = (correct_count / max(studied_count, 1)) * 100
                                                st.metric("Skuteczność", f"{accuracy:.1f}%")
                                            
                                            # Progress bar
                                            progress = studied_count / total_cards
                                            st.progress(progress, text=f"Postęp nauki: {studied_count}/{total_cards} fiszek")
                                            
                                            # Award XP za zakończenie wszystkich fiszek
                                            if studied_count == total_cards:
                                                flashcards_xp_key = f"flashcards_xp_{lesson_id}"
                                                if not st.session_state.get(flashcards_xp_key, False):
                                                    flashcards_xp = step_xp_values['practical_exercises'] // 6  # 1/6 XP z practical_exercises
                                                    success, earned_xp = award_fragment_xp(lesson_id, 'flashcards', flashcards_xp)
                                                    st.session_state[flashcards_xp_key] = True
                                                    if success and earned_xp > 0:
                                                        st.success(f"🎉 Przejrzałeś wszystkie fiszki! Zdobyłeś {earned_xp} XP!")
                                        
                                        else:
                                            st.warning("Brak fiszek do wyświetlenia.")
                                    else:
                                        st.warning("Brak fiszek w tej sekcji.")
                                
                                elif tab_key == 'case_studies':
                                    # Obsługa Case Studies - interaktywne przypadki do analizy
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wyświetl tytuł i opis sekcji
                                    if 'title' in tab_data:
                                        st.markdown(f"### {tab_data['title']}")
                                    if 'description' in tab_data:
                                        st.info(tab_data['description'])
                                    
                                    # Obsługa studies
                                    if 'studies' in tab_data:
                                        studies = tab_data['studies']
                                        
                                        for study in studies:
                                            with st.expander(f"**Case Study {study['id']}: {study['title']}**", expanded=False):
                                                # Opis scenariusza
                                                st.markdown("#### 📋 Scenariusz")
                                                st.markdown(study['scenario'], unsafe_allow_html=True)
                                                
                                                # Pytania do przemyślenia
                                                st.markdown("#### 🤔 Pytania do przemyślenia")
                                                for i, question in enumerate(study['questions'], 1):
                                                    st.markdown(f"**{i}.** {question}")
                                                
                                                # Miejsce na odpowiedź użytkownika
                                                st.markdown(study['user_space'], unsafe_allow_html=True)
                                                
                                                # Rozwijane rozwiązanie
                                                with st.expander("💡 **Pokaż przykładowe rozwiązanie**", expanded=False):
                                                    st.markdown(study['solution'], unsafe_allow_html=True)
                                                
                                                st.markdown("---")
                                    else:
                                        st.warning("Brak case studies w tej sekcji.")
                                
                                elif tab_key == 'ai_questions':
                                    # Obsługa pytań otwartych z oceną AI
                                    try:
                                        from utils.ai_questions import display_open_question, load_open_question_styles
                                        load_open_question_styles()
                                        
                                        tab_data = sub_tabs_data[tab_key]
                                        
                                        # Wyświetl tytuł i opis sekcji
                                        if 'title' in tab_data:
                                            st.markdown(f"### {tab_data['title']}")
                                        if 'description' in tab_data:
                                            st.info(tab_data['description'])
                                        
                                        # Wyświetl pytania
                                        if 'questions' in tab_data:
                                            total_questions = len(tab_data['questions'])
                                            answered_questions = 0
                                            total_score = 0
                                            max_total_score = 0
                                            
                                            for question in tab_data['questions']:
                                                question_id = f"ai_q_{lesson_id}_{question.get('id', 'unknown')}"
                                                answered, result = display_open_question(question, question_id)
                                                
                                                if answered:
                                                    answered_questions += 1
                                                    total_score += result.get('score', 0)
                                                
                                                max_total_score += question.get('max_score', 10)
                                                st.markdown("---")
                                            
                                            # Podsumowanie wyników
                                            if answered_questions > 0:
                                                st.markdown("### 📊 Podsumowanie wyników")
                                                percentage = (total_score / max_total_score) * 100 if max_total_score > 0 else 0
                                                
                                                col1, col2, col3 = st.columns(3)
                                                with col1:
                                                    st.metric("Odpowiedziano", f"{answered_questions}/{total_questions}")
                                                with col2:
                                                    st.metric("Punkty", f"{total_score}/{max_total_score}")
                                                with col3:
                                                    st.metric("Wynik", f"{percentage:.1f}%")
                                                
                                                if answered_questions == total_questions:
                                                    # Award XP za ukończenie wszystkich pytań AI
                                                    ai_questions_xp_key = f"ai_questions_xp_{lesson_id}"
                                                    if not st.session_state.get(ai_questions_xp_key, False):
                                                        ai_xp = step_xp_values['practical_exercises'] // 4  # 1/4 XP z practical_exercises
                                                        success, earned_xp = award_fragment_xp(lesson_id, 'ai_questions', ai_xp)
                                                        st.session_state[ai_questions_xp_key] = True
                                                        if success and earned_xp > 0:
                                                            st.success(f"🎉 Ukończyłeś wszystkie pytania AI! Zdobyłeś {earned_xp} XP!")
                                        else:
                                            st.warning("Brak pytań do wyświetlenia.")
                                    
                                    except ImportError:
                                        st.error("Moduł obsługi pytań AI nie jest dostępny. Skontaktuj się z administratorem.")
                                    except Exception as e:
                                        st.error(f"Błąd podczas ładowania pytań AI: {str(e)}")
                                
                                else:
                                    # Standardowa obsługa dla innych zakładek
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wyświetl opis zakładki jeśli istnieje
                                    if 'description' in tab_data:
                                        st.info(tab_data['description'])
                                    
                                    # Wyświetl sekcje w zakładce
                                    if 'sections' in tab_data:
                                        for section in tab_data['sections']:
                                            st.markdown(f"### {section.get('title', 'Sekcja')}")
                                            st.markdown(section.get('content', 'Brak treści'), unsafe_allow_html=True)
                                    else:
                                        st.warning(f"Zakładka '{tab_title}' nie zawiera sekcji do wyświetlenia.")
                
                # Stara struktura z 'tabs' (backward compatibility)
                if 'tabs' in practical_data:
                    old_tabs = practical_data['tabs']
                    
                    # Inicjalizuj zmienne dla starej struktury
                    available_tabs = []
                    tab_keys = []
                    sub_tabs_data = {}
                    
                    # Sprawdź które zakładki są dostępne i przygotuj je w logicznej kolejności uczenia się
                    # 1. Autotest - sprawdzenie aktualnego stanu
                    if 'autotest' in old_tabs:
                        available_tabs.append("🧠 Autotest")
                        tab_keys.append('autotest')
                        sub_tabs_data['autotest'] = old_tabs['autotest']
                    
                    # 2. Refleksja - przemyślenie własnych doświadczeń
                    if 'reflection' in old_tabs:
                        available_tabs.append("📝 Refleksja")
                        tab_keys.append('reflection')
                        sub_tabs_data['reflection'] = old_tabs['reflection']
                    
                    # 3. Analiza - case studies i scenariusze
                    if 'analysis' in old_tabs:
                        available_tabs.append("📊 Analiza")
                        tab_keys.append('analysis')
                        sub_tabs_data['analysis'] = old_tabs['analysis']
                    
                    # 4. Wdrożenie - konkretny plan działania
                    if 'implementation' in old_tabs:
                        available_tabs.append("🎯 Wdrożenie")
                        tab_keys.append('implementation')
                        sub_tabs_data['implementation'] = old_tabs['implementation']
                    
                    # 5. Quiz końcowy - przeniesiony z osobnego kroku
                    if 'closing_quiz' in lesson.get('sections', {}):
                        # Sprawdź tytuł lekcji dla specjalnej nazwy tabu
                        lesson_title = lesson.get("title", "")
                        if lesson_title == "Wprowadzenie do neuroprzywództwa":
                            available_tabs.append("🧠 Quiz autodiagnozy")
                        else:
                            available_tabs.append("🎓 Quiz końcowy")
                        tab_keys.append('closing_quiz')
                        sub_tabs_data['closing_quiz'] = lesson['sections']['closing_quiz']
                    
                    if available_tabs:
                        # Wyświetl pod-zakładki
                        tabs = tabs_with_fallback(available_tabs)
                        
                        for i, (tab_key, tab_title) in enumerate(zip(tab_keys, available_tabs)):
                            with tabs[i]:
                                if tab_key == 'closing_quiz':
                                    # Specjalna obsługa dla quizu końcowego
                                    lesson_title = lesson.get("title", "")
                                    if lesson_title == "Wprowadzenie do neuroprzywództwa":
                                        # Dla tej lekcji quiz autodiagnozy bez wymogu 75%
                                        st.info("🧠 **Quiz autodiagnozy** - Ten quiz pomoże Ci lepiej poznać swoje podejście do przywództwa. Nie ma tu dobrych ani złych odpowiedzi - chodzi o szczerą autorefleksję.")
                                        
                                        quiz_data = sub_tabs_data['closing_quiz']
                                        quiz_completed, quiz_passed, earned_points = display_quiz(quiz_data, passing_threshold=0)  # Brak wymogu minimum
                                        
                                        # Oznacz quiz jako ukończony po wypełnieniu
                                        if quiz_completed:
                                            # Zapisz stan zaliczenia quizu do sprawdzania w nawigacji
                                            closing_quiz_key = f"closing_quiz_{lesson_id}"
                                            if closing_quiz_key not in st.session_state:
                                                st.session_state[closing_quiz_key] = {}
                                            
                                            st.session_state[closing_quiz_key]["quiz_completed"] = True
                                            st.session_state[closing_quiz_key]["quiz_passed"] = True  # Zawsze zdany dla tej lekcji
                                            
                                            closing_quiz_xp_key = f"closing_quiz_xp_{lesson_id}"
                                            if not st.session_state.get(closing_quiz_xp_key, False):
                                                # Award fragment XP for quiz completion
                                                fragment_xp = get_fragment_xp_breakdown(lesson.get('xp_reward', 30))
                                                # Quiz końcowy dostaje 1/3 z XP practical_exercises 
                                                success, earned_xp = award_fragment_xp(lesson_id, 'closing_quiz', step_xp_values['practical_exercises'] // 3)
                                                st.session_state[closing_quiz_xp_key] = True
                                                if success and earned_xp > 0:
                                                    show_xp_notification(earned_xp, f"Zdobyłeś {earned_xp} XP za ukończenie quizu autodiagnozy!")
                                            
                                            st.success("✅ Dziękujemy za szczerą autorefleksję! Możesz teraz przejść do podsumowania.")
                                            
                                            # Dodaj przycisk do ponownego przystąpienia do quizu autodiagnozy
                                            st.markdown("---")
                                            col1, col2, col3 = st.columns([1, 1, 1])
                                            with col2:
                                                if st.button("🔄 Przystąp ponownie", key=f"retry_autodiag_quiz_practical_{lesson_id}", help="Możesz ponownie wypełnić quiz autodiagnozy aby zaktualizować swoją autorefleksję", width='stretch'):
                                                    # Reset stanu quizu autodiagnozy
                                                    quiz_id = f"quiz_{quiz_data.get('title', '').replace(' ', '_').lower()}"
                                                    if quiz_id in st.session_state:
                                                        del st.session_state[quiz_id]
                                                    # Reset stanu zaliczenia
                                                    if closing_quiz_key in st.session_state:
                                                        st.session_state[closing_quiz_key]["quiz_completed"] = False
                                                        st.session_state[closing_quiz_key]["quiz_passed"] = False
                                                    st.rerun()
                                    else:
                                        # Dla wszystkich innych lekcji standardowy quiz końcowy
                                        st.info("🎓 **Quiz końcowy** - Sprawdź swoją wiedzę z tej lekcji. Musisz uzyskać minimum 75% poprawnych odpowiedzi, aby przejść dalej.")
                                        
                                        quiz_data = sub_tabs_data['closing_quiz']
                                        quiz_completed, quiz_passed, earned_points = display_quiz(quiz_data, passing_threshold=75)
                                          # Oznacz quiz jako ukończony po wypełnieniu
                                        if quiz_completed:
                                            # Zapisz stan zaliczenia quizu do sprawdzania w nawigacji
                                            closing_quiz_key = f"closing_quiz_{lesson_id}"
                                            if closing_quiz_key not in st.session_state:
                                                st.session_state[closing_quiz_key] = {}
                                            
                                            st.session_state[closing_quiz_key]["quiz_completed"] = True
                                            st.session_state[closing_quiz_key]["quiz_passed"] = quiz_passed
                                            
                                            closing_quiz_xp_key = f"closing_quiz_xp_{lesson_id}"
                                            if not st.session_state.get(closing_quiz_xp_key, False):
                                                # Award fragment XP for quiz completion
                                                fragment_xp = get_fragment_xp_breakdown(lesson.get('xp_reward', 30))
                                                # Quiz końcowy dostaje 1/3 z XP practical_exercises 
                                                success, earned_xp = award_fragment_xp(lesson_id, 'closing_quiz', step_xp_values['practical_exercises'] // 3)
                                                st.session_state[closing_quiz_xp_key] = True
                                                if success and earned_xp > 0:
                                                    show_xp_notification(earned_xp, f"Zdobyłeś {earned_xp} XP za ukończenie quizu końcowego!")
                                            
                                            if quiz_passed:
                                                st.success("✅ Gratulacje! Zaliczyłeś quiz końcowy! Możesz teraz przejść do podsumowania.")
                                            else:
                                                st.error("❌ Aby przejść do podsumowania, musisz uzyskać przynajmniej 75% poprawnych odpowiedzi. Spróbuj ponownie!")
                                                
                                                # Dodaj przycisk do ponowienia quizu
                                                st.markdown("---")
                                                col1, col2, col3 = st.columns([1, 1, 1])
                                                with col2:
                                                    if st.button("🔄 Spróbuj ponownie", key=f"retry_closing_quiz_practical_{lesson_id}", type="primary", width='stretch'):
                                                        # Reset stanu quizu
                                                        quiz_id = f"quiz_{quiz_data.get('title', '').replace(' ', '_').lower()}"
                                                        if quiz_id in st.session_state:
                                                            del st.session_state[quiz_id]
                                                        # Reset stanu zaliczenia
                                                        if closing_quiz_key in st.session_state:
                                                            st.session_state[closing_quiz_key]["quiz_completed"] = False
                                                            st.session_state[closing_quiz_key]["quiz_passed"] = False
                                                        st.rerun()
                                else:
                                    # Standardowa obsługa dla innych zakładek
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wyświetl opis zakładki jeśli istnieje
                                    if 'description' in tab_data:
                                        st.info(tab_data['description'])
                                    
                                    # Wyświetl sekcje w zakładce
                                    if 'sections' in tab_data:
                                        for section in tab_data['sections']:
                                            st.markdown(f"### {section.get('title', 'Sekcja')}")
                                            
                                            # Użyj nowego renderera obsługującego osadzone media
                                            content = section.get('content', 'Brak treści')
                                            render_embedded_content(content, section)
                                            
                                            # Jeśli sekcja wymaga odpowiedzi użytkownika
                                            if section.get('interactive', False):
                                                # Generuj klucz dla przechowywania odpowiedzi
                                                section_key = f"practical_{tab_key}_{section.get('title', '').replace(' ', '_').lower()}"
                                                  # Użyj formularza dla lepszego UX
                                                with st.form(key=f"form_{section_key}"):
                                                    # Pobierz istniejącą odpowiedź (jeśli jest)
                                                    existing_response = st.session_state.get(section_key, "")
                                                    
                                                    # Wyświetl pole tekstowe z istniejącą odpowiedzią
                                                    user_response = st.text_area(
                                                        "Twoja odpowiedź:",
                                                        value=existing_response,
                                                        height=200,
                                                        key=f"input_{section_key}"
                                                    )
                                                      # Przycisk do zapisywania odpowiedzi w formularzu
                                                    submitted = st.form_submit_button("Zapisz odpowiedź")
                                                    
                                                    if submitted:
                                                        # Zapisz odpowiedź w stanie sesji
                                                        st.session_state[section_key] = user_response
                                                        st.success("Twoja odpowiedź została zapisana!")
                                    else:
                                        st.warning(f"Zakładka '{tab_title}' nie zawiera sekcji do wyświetlenia.")
                    else:
                        st.warning("Nie znaleziono dostępnych pod-zakładek w sekcji ćwiczeń praktycznych.")
              # Przycisk "Dalej" po ćwiczeniach praktycznych - z kontrolą dostępu do podsumowania
            st.markdown("<div class='next-button'>", unsafe_allow_html=True)
            
            # Sprawdź czy następny krok to 'summary' i czy quiz końcowy został zdany
            if next_step == 'summary':
                lesson_title = lesson.get("title", "")
                closing_quiz_key = f"closing_quiz_{lesson_id}"
                closing_quiz_state = st.session_state.get(closing_quiz_key, {})
                quiz_passed = closing_quiz_state.get("quiz_passed", False)
                
                # Dla lekcji "Wprowadzenie do neuroprzywództwa" nie ma blokowania
                if lesson_title == "Wprowadzenie do neuroprzywództwa" or quiz_passed:                    # Quiz zdany lub brak wymogu dla specjalnej lekcji - normalny przycisk "Dalej"
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())}", width='stretch'):
                            # Award fragment XP using the new system
                            success, xp_awarded = award_fragment_xp(lesson_id, 'practical_exercises', step_xp_values['practical_exercises'])
                            
                            if success and xp_awarded > 0:
                                # Update session state for UI compatibility
                                st.session_state.lesson_progress['practical_exercises'] = True
                                st.session_state.lesson_progress['steps_completed'] += 1
                                st.session_state.lesson_progress['total_xp_earned'] += xp_awarded
                                
                                # Show real-time XP notification
                                show_xp_notification(xp_awarded, f"Zdobyłeś {xp_awarded} XP za ukończenie ćwiczeń praktycznych!")
                                
                                # Refresh user data for real-time updates
                                from utils.real_time_updates import refresh_user_data
                                refresh_user_data()
                                
                                # Sprawdź czy lekcja została ukończona
                                check_and_mark_lesson_completion(lesson_id)
                            
                            # Przejdź do następnego kroku
                            st.session_state.lesson_step = next_step
                            scroll_to_top()
                            st.rerun()
                else:
                    # Quiz niezdany - zablokowany przycisk z komunikatem
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        zen_button(
                            f"🔒 Dalej: {step_names.get(next_step, next_step.capitalize())}",
                            disabled=True,
                            width='stretch',
                            help="Musisz zaliczyć quiz końcowy (min. 75%) aby przejść do podsumowania"
                        )
                    st.warning("⚠️ Aby przejść do podsumowania, musisz najpierw zaliczyć quiz końcowy z wynikiem minimum 75%. Przejdź do zakładki '🎓 Quiz końcowy' powyżej.")
            else:                # Normalny przycisk dla innych kroków (nie-summary)
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())}", width='stretch'):
                        # Award fragment XP using the new system
                        success, xp_awarded = award_fragment_xp(lesson_id, 'practical_exercises', step_xp_values['practical_exercises'])
                        
                        if success and xp_awarded > 0:
                            # Update session state for UI compatibility
                            st.session_state.lesson_progress['practical_exercises'] = True
                            st.session_state.lesson_progress['steps_completed'] += 1
                            st.session_state.lesson_progress['total_xp_earned'] += xp_awarded
                            
                            # Show real-time XP notification
                            show_xp_notification(xp_awarded, f"Zdobyłeś {xp_awarded} XP za ukończenie ćwiczeń praktycznych!")
                            
                            # Refresh user data for real-time updates
                            from utils.real_time_updates import refresh_user_data
                            refresh_user_data()
                            
                            # Sprawdź czy lekcja została ukończona
                            check_and_mark_lesson_completion(lesson_id)
                        
                        # Przejdź do następnego kroku
                        st.session_state.lesson_step = next_step
                        scroll_to_top()
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.lesson_step == 'reflection':
            # Wyświetl sekcje refleksji
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'reflection' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'reflection'!")
            elif 'sections' not in lesson['sections'].get('reflection', {}):
                st.error("Sekcja 'reflection' nie zawiera klucza 'sections'!")
            else:
                # Wyświetl sekcje refleksji
                for section in lesson["sections"]["reflection"]["sections"]:
                    st.markdown(f"### {section.get('title', 'Zadanie refleksyjne')}")
                    st.markdown(section.get("content", "Brak treści"), unsafe_allow_html=True)
                    
                    # Generuj klucz dla przechowywania odpowiedzi
                    reflection_key = f"reflection_{section.get('title', '').replace(' ', '_').lower()}"
                    
                    # Generuj INNY klucz dla widgetu tekstowego
                    widget_key = f"input_{reflection_key}"
                    
                    # Użyj formularza, aby uniknąć problemów z aktualizacją stanu sesji
                    with st.form(key=f"form_{reflection_key}"):
                        # Pobierz istniejącą odpowiedź (jeśli jest)
                        existing_response = st.session_state.get(reflection_key, "")
                        
                        # Wyświetl pole tekstowe z istniejącą odpowiedzią
                        user_reflection = st.text_area(
                            "Twoja odpowiedź:",
                            value=existing_response,
                            height=200,
                            key=widget_key
                        )
                        
                        # Przycisk do zapisywania odpowiedzi w formularzu
                        submitted = st.form_submit_button("Zapisz odpowiedź")
                        
                        if submitted:
                            # Zapisz odpowiedź w stanie sesji
                            st.session_state[reflection_key] = user_reflection
                            st.success("Twoja odpowiedź została zapisana!")              # Przycisk "Dalej" po refleksji
            st.markdown("<div class='next-button'>", unsafe_allow_html=True)
              # Sprawdź czy następny krok to 'summary' i czy quiz końcowy został zdany
            if next_step == 'summary':
                lesson_title = lesson.get("title", "")
                closing_quiz_key = f"closing_quiz_{lesson_id}"
                closing_quiz_state = st.session_state.get(closing_quiz_key, {})
                quiz_passed = closing_quiz_state.get("quiz_passed", False)
                
                # Dla lekcji "Wprowadzenie do neuroprzywództwa" nie ma blokowania
                if lesson_title == "Wprowadzenie do neuroprzywództwa" or quiz_passed:
                    # Quiz zdany - normalny przycisk "Dalej"
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())}", width='stretch'):
                            # Award fragment XP using the new system
                            success, xp_awarded = award_fragment_xp(lesson_id, 'reflection', step_xp_values['reflection'])
                            
                            if success and xp_awarded > 0:
                                # Update session state for UI compatibility
                                st.session_state.lesson_progress['reflection'] = True
                                st.session_state.lesson_progress['steps_completed'] += 1
                                st.session_state.lesson_progress['total_xp_earned'] += xp_awarded
                                
                                # Show real-time XP notification
                                show_xp_notification(xp_awarded, f"Zdobyłeś {xp_awarded} XP za wykonanie zadań refleksyjnych!")
                                
                                # Refresh user data for real-time updates
                                from utils.real_time_updates import refresh_user_data
                                refresh_user_data()
                            
                            # Przejdź do następnego kroku
                            st.session_state.lesson_step = next_step
                            scroll_to_top()
                            st.rerun()
                else:
                    # Quiz niezdany - zablokowany przycisk z komunikatem
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        zen_button(
                            f"🔒 Dalej: {step_names.get(next_step, next_step.capitalize())}",
                            disabled=True,
                            width='stretch',
                            help="Musisz zaliczyć quiz końcowy (min. 75%) aby przejść do podsumowania"
                        )
                    st.warning("⚠️ Aby przejść do podsumowania, musisz najpierw zaliczyć quiz końcowy z wynikiem minimum 75%. Quiz znajdziesz w sekcji 'Praktyka' → '🎓 Quiz końcowy'.")
            else:
                # Normalny przycisk dla innych kroków (nie-summary)
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())}", width='stretch'):
                        # Award fragment XP using the new system
                        success, xp_awarded = award_fragment_xp(lesson_id, 'reflection', step_xp_values['reflection'])
                        
                        if success and xp_awarded > 0:
                            # Update session state for UI compatibility
                            st.session_state.lesson_progress['reflection'] = True
                            st.session_state.lesson_progress['steps_completed'] += 1
                            st.session_state.lesson_progress['total_xp_earned'] += xp_awarded
                            
                            # Show real-time XP notification
                            show_xp_notification(xp_awarded, f"Zdobyłeś {xp_awarded} XP za wykonanie zadań refleksyjnych!")
                            
                            # Refresh user data for real-time updates
                            from utils.real_time_updates import refresh_user_data
                            refresh_user_data()
                        
                        # Przejdź do następnego kroku
                        st.session_state.lesson_step = next_step
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.lesson_step == 'application':
            # Wyświetl zadania praktyczne
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'application' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'application'!")
            elif 'sections' not in lesson['sections'].get('application', {}):
                st.error("Sekcja 'application' nie zawiera klucza 'sections'!")
            else:
                # Wyświetl zadania praktyczne
                for section in lesson["sections"]["application"]["sections"]:
                    st.markdown(f"### {section.get('title', 'Zadanie praktyczne')}")
                    st.markdown(section.get("content", "Brak treści"), unsafe_allow_html=True)
                    
                    # Generuj klucz dla przechowywania odpowiedzi
                    task_key = f"application_{section.get('title', '').replace(' ', '_').lower()}"
                    
                    # Użyj formularza, aby uniknąć problemów z aktualizacją stanu sesji
                    with st.form(key=f"form_{task_key}"):
                        # Pobierz istniejącą odpowiedź (jeśli jest)
                        existing_solution = st.session_state.get(task_key, "")
                        
                        # Wyświetl pole tekstowe z istniejącą odpowiedzią
                        user_solution = st.text_area(
                            "Twoje rozwiązanie:",
                            value=existing_solution,
                            height=200,
                            key=f"input_{task_key}"
                        )
                        
                        # Przycisk do zapisywania odpowiedzi w formularzu
                        submitted = st.form_submit_button("Zapisz rozwiązanie")
                        
                        if submitted:
                            # Zapisz odpowiedź w stanie sesji
                            st.session_state[task_key] = user_solution
                            st.success("Twoje rozwiązanie została zapisana!")
                            # Dodaj odświeżenie strony po zapisaniu
                            st.rerun()              # Przycisk "Dalej" po zadaniach praktycznych
            st.markdown("<div class='next-button'>", unsafe_allow_html=True)
            
            # Sprawdź czy następny krok to 'summary' i czy quiz końcowy został zdany
            if next_step == 'summary':
                lesson_title = lesson.get("title", "")
                closing_quiz_key = f"closing_quiz_{lesson_id}"
                closing_quiz_state = st.session_state.get(closing_quiz_key, {})
                quiz_passed = closing_quiz_state.get("quiz_passed", False)
                
                # Dla lekcji "Wprowadzenie do neuroprzywództwa" nie ma blokowania
                if lesson_title == "Wprowadzenie do neuroprzywództwa" or quiz_passed:
                    # Quiz zdany - normalny przycisk "Dalej"
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())}", width='stretch'):
                            # Award fragment XP using the new system
                            success, xp_awarded = award_fragment_xp(lesson_id, 'application', step_xp_values['application'])
                            
                            if success and xp_awarded > 0:
                                # Update session state for UI compatibility
                                st.session_state.lesson_progress['application'] = True
                                st.session_state.lesson_progress['steps_completed'] += 1
                                st.session_state.lesson_progress['total_xp_earned'] += xp_awarded
                                
                                # Show real-time XP notification
                                show_xp_notification(xp_awarded, f"Zdobyłeś {xp_awarded} XP za wykonanie zadań praktycznych!")
                                
                                # Refresh user data for real-time updates
                                from utils.real_time_updates import refresh_user_data
                                refresh_user_data()
                            
                            # Przejdź do następnego kroku
                            st.session_state.lesson_step = next_step
                            scroll_to_top()
                            st.rerun()
                else:                    # Quiz niezdany - zablokowany przycisk z komunikatem
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        zen_button(
                            f"🔒 Dalej: {step_names.get(next_step, next_step.capitalize())}",
                            disabled=True,
                            width='stretch',
                            help="Musisz zaliczyć quiz końcowy (min. 75%) aby przejść do podsumowania"
                        )
                    st.warning("⚠️ Aby przejść do podsumowania, musisz najpierw zaliczyć quiz końcowy z wynikiem minimum 75%. Quiz znajdziesz w sekcji 'Praktyka' → '🎓 Quiz końcowy'.")
            else:
                # Normalny przycisk dla innych kroków (nie-summary)
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if zen_button(f"Dalej: {step_names.get(next_step, next_step.capitalize())}", width='stretch'):
                        # Award fragment XP using the new system
                        success, xp_awarded = award_fragment_xp(lesson_id, 'application', step_xp_values['application'])
                        
                        if success and xp_awarded > 0:
                            # Update session state for UI compatibility
                            st.session_state.lesson_progress['application'] = True
                            st.session_state.lesson_progress['steps_completed'] += 1
                            st.session_state.lesson_progress['total_xp_earned'] += xp_awarded
                            
                            # Show real-time XP notification
                            show_xp_notification(xp_awarded, f"Zdobyłeś {xp_awarded} XP za wykonanie zadań praktycznych!")
                            
                            # Refresh user data for real-time updates
                            from utils.real_time_updates import refresh_user_data
                            refresh_user_data()
                        
                        # Przejdź do następnego kroku
                        st.session_state.lesson_step = next_step
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        elif st.session_state.lesson_step == 'summary':
            # Wyświetl podsumowanie lekcji w podziale na zakładki, podobnie jak wprowadzenie
            if 'summary' in lesson:
                # Sprawdź tytuł lekcji, aby ukryć niektóre tabs dla konkretnych lekcji
                lesson_title = lesson.get("title", "")
                
                if lesson_title == "Wprowadzenie do neuroprzywództwa":
                    # Dla tej lekcji pokazuj dwie zakładki: Quiz Autodiagnozy i Podsumowanie
                    summary_tabs = tabs_with_fallback(["🎯 Quiz Autodiagnozy", "📋 Podsumowanie"])
                    
                    with summary_tabs[0]:
                        # Wyświetl quiz autodiagnozy
                        if 'closing_quiz' in lesson['summary']:
                            quiz_passed, can_continue, score = display_quiz(lesson['summary']['closing_quiz'])
                            
                            # Sprawdź czy quiz został ukończony
                            if quiz_passed:
                                success, fragment_xp = award_fragment_xp(lesson_id, 'closing_quiz', step_xp_values['summary'])
                                if success and fragment_xp > 0:
                                    st.success(f"✅ Quiz ukończony! Zdobyłeś {fragment_xp} XP!")
                        else:
                            st.warning("Brak quizu autodiagnozy.")
                    
                    with summary_tabs[1]:
                        # Wyświetl główne podsumowanie
                        if 'main' in lesson['summary']:
                            st.markdown(lesson['summary']['main'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak głównego podsumowania.")
                        
                        # Rekomendacje szkoleń (ukryte - możliwość przywrócenia w przyszłości)
                        # try:
                        #     from utils.training_recommendations import display_training_recommendations, load_recommendations_styles
                        #     load_recommendations_styles()
                        #     
                        #     # Klucz wyników quizu autodiagnozy
                        #     quiz_results_key = "quiz_quiz_autodiagnozy_results"
                        #     display_training_recommendations(lesson_id, quiz_results_key)
                        #     
                        # except ImportError:
                        #     st.error("Moduł rekomendacji szkoleń nie jest dostępny.")
                        # except Exception as e:
                        # except Exception as e:
                        #     st.error(f"Błąd podczas ładowania rekomendacji: {str(e)}")
                else:
                    # Dla wszystkich innych lekcji pokazuj pełne tabs
                    # Podziel podsumowanie na cztery zakładki - dodajemy Cheatsheet
                    summary_tabs = tabs_with_fallback(["Podsumowanie", "Case Study", "🗺️ Mapa myśli", "📋 Cheatsheet"])
                    
                    with summary_tabs[0]:
                        # Wyświetl główne podsumowanie
                        if 'main' in lesson['summary']:
                            st.markdown(lesson['summary']['main'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak głównego podsumowania.")
                    
                    with summary_tabs[1]:
                        # Wyświetl studium przypadku
                        if 'case_study' in lesson['summary']:
                            st.markdown(lesson['summary']['case_study'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak studium przypadku w podsumowaniu.")
                
                    with summary_tabs[2]:
                        # Wyświetl interaktywną mapę myśli
                        st.markdown("### 🗺️ Interaktywna mapa myśli")
                        st.markdown("Poniżej znajdziesz interaktywną mapę myśli podsumowującą kluczowe koncepty z tej lekcji. Możesz klikać na węzły aby je przesuwać i lepiej eksplorować powiązania między różnymi tematami.")
                        
                        try:
                            from utils.mind_map import create_lesson_mind_map
                            mind_map_result = create_lesson_mind_map(lesson)
                            
                            if mind_map_result is None:
                                st.info("💡 **Mapa myśli w przygotowaniu**\n\nDla tej lekcji przygotowujemy interaktywną mapę myśli, która pomoże Ci lepiej zrozumieć powiązania między różnymi konceptami. Wkrótce będzie dostępna!")
                        except Exception as e:
                            st.warning("⚠️ Mapa myśli nie jest obecnie dostępna. Sprawdź, czy wszystkie wymagane biblioteki są zainstalowane.")
                            st.expander("Szczegóły błędu (dla deweloperów)").write(str(e))
                    
                    with summary_tabs[3]:
                        # Wyświetl cheatsheet
                        if 'cheatsheet' in lesson['summary']:
                            st.markdown(lesson['summary']['cheatsheet'], unsafe_allow_html=True)
                            
                            # Dodaj przycisk do pobierania PDF
                            st.markdown("---")
                            st.markdown("### 📄 Pobierz Cheatsheet jako PDF")
                            
                            try:
                                from utils.pdf_generator import generate_pdf_content, create_simple_download_button, clean_html_for_pdf
                                
                                # Przygotuj zawartość dla PDF
                                lesson_title = lesson.get('title', 'Lekcja')
                                cheatsheet_content = lesson['summary']['cheatsheet']
                                
                                # Wyczyść HTML dla lepszej konwersji do PDF
                                cleaned_content = clean_html_for_pdf(cheatsheet_content)
                                
                                # Generuj kompletny HTML dla PDF
                                pdf_html = generate_pdf_content(
                                    title=f"Cheatsheet: {lesson_title}",
                                    content_html=cleaned_content
                                )
                                
                                # Twórz przycisk do pobrania
                                filename = f"cheatsheet_{lesson.get('id', 'lesson').replace(' ', '_')}.html"
                                create_simple_download_button(pdf_html, filename, "Pobierz Cheatsheet jako PDF")
                                
                            except Exception as e:
                                st.warning("⚠️ Funkcja pobierania PDF nie jest obecnie dostępna.")
                                st.expander("Szczegóły błędu (dla deweloperów)").write(str(e))
                        else:
                            st.warning("Brak cheatsheet w podsumowaniu.")

                # Wyświetl całkowitą zdobytą ilość XP
                total_xp = st.session_state.lesson_progress['total_xp_earned']
                # st.success(f"Gratulacje! Ukończyłeś lekcję i zdobyłeś łącznie {total_xp} XP!")
                  # Sprawdź czy lekcja została już zakończona
                lesson_finished = st.session_state.get('lesson_finished', False)
                
                if not lesson_finished:
                    # Pierwszy etap - przycisk "Zakończ lekcję"
                    st.markdown("<div class='next-button'>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if zen_button("🎉 Zakończ lekcję", width='stretch'):
                            # Sprawdź czy XP za podsumowanie już zostało przyznane
                            progress = get_lesson_fragment_progress(lesson_id)
                            if not progress.get('summary_completed', False):
                                success, xp_awarded = award_fragment_xp(lesson_id, 'summary', step_xp_values['summary'])
                                
                                if success and xp_awarded > 0:
                                    # Update session state for UI compatibility - usunięto podwójne ustawienie
                                    # award_fragment_xp już ustawia summary_completed
                                    st.session_state.lesson_progress['steps_completed'] += 1
                                    st.session_state.lesson_progress['total_xp_earned'] += xp_awarded
                                    
                                    # Show real-time XP notification
                                    show_xp_notification(xp_awarded, f"Zdobyłeś {xp_awarded} XP za ukończenie podsumowania!")
                                    
                                    # Refresh user data for real-time updates
                                    from utils.real_time_updates import refresh_user_data
                                    refresh_user_data()
                                    
                                    # Sprawdź czy lekcja została ukończona
                                    check_and_mark_lesson_completion(lesson_id)
                            
                            # Oznacz lekcję jako zakończoną i zapisz postęp
                            lesson_completed = check_and_mark_lesson_completion(lesson_id)
                            
                            if lesson_completed:
                                # Check for achievements after completing lesson
                                from utils.achievements import check_achievements
                                username = st.session_state.get('username')
                                if username:
                                    check_achievements(username, 'lesson_completion', lesson_id=lesson_id)
                                
                                # Refresh user data for real-time updates
                                from utils.real_time_updates import refresh_user_data
                                refresh_user_data()
                                
                            # Show completion notification - wyświetl faktyczne całkowite XP
                            final_total_xp = st.session_state.lesson_progress.get('total_xp_earned', 0)
                            show_xp_notification(0, f"🎉 Gratulacje! Ukończyłeś całą lekcję i zdobyłeś {final_total_xp} XP!")
                            
                            # Oznacz lekcję jako zakończoną w sesji
                            st.session_state.lesson_finished = True
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    # Drugi etap - pokaż podsumowanie i przycisk powrotu
                    st.balloons()  # Animacja gratulacji
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                                color: white; padding: 20px; border-radius: 15px; margin: 20px 0;
                                text-align: center; box-shadow: 0 4px 15px rgba(76,175,80,0.3);">
                        <h2 style="margin: 0 0 10px 0;">🎓 Lekcja ukończona!</h2>
                        <p style="margin: 0; font-size: 18px;">Świetna robota! Możesz teraz przejść do kolejnych lekcji.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Przycisk powrotu do wszystkich lekcji
                    st.markdown("<div class='next-button'>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if zen_button("📚 Wróć do wszystkich lekcji", width='stretch'):
                            # Wyczyść stan zakończenia lekcji
                            st.session_state.lesson_finished = False
                            # Powrót do przeglądu lekcji
                            st.session_state.current_lesson = None
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            elif 'outro' in lesson:
                # Backward compatibility - obsługa starszego formatu outro - zakomentowano mapę myśli
                lesson_title = lesson.get("title", "")
                
                if lesson_title == "Wprowadzenie do neuroprzywództwa":
                    # Dla tej lekcji pokazuj tylko zakładkę "Podsumowanie"
                    summary_tabs = tabs_with_fallback(["Podsumowanie"])
                    
                    with summary_tabs[0]:
                        # Wyświetl główne podsumowanie
                        if 'main' in lesson['outro']:
                            st.markdown(lesson['outro']['main'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak głównego podsumowania.")
                else:
                    # Dla wszystkich innych lekcji pokazuj pełne tabs
                    summary_tabs = tabs_with_fallback(["Podsumowanie", "Case Study", "🗺️ Mapa myśli"])
                    
                    with summary_tabs[0]:
                        # Wyświetl główne podsumowanie
                        if 'main' in lesson['outro']:
                            st.markdown(lesson['outro']['main'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak głównego podsumowania.")
                    
                    with summary_tabs[1]:
                        # Wyświetl studium przypadku
                        if 'case_study' in lesson['outro']:
                            st.markdown(lesson['outro']['case_study'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak studium przypadku w podsumowaniu.")
                
                    with summary_tabs[2]:
                        # Wyświetl interaktywną mapę myśli
                        st.markdown("### 🗺️ Interaktywna mapa myśli")
                        st.markdown("Poniżej znajdziesz interaktywną mapę myśli podsumowującą kluczowe koncepty z tej lekcji. Możesz klikać na węzły aby je przesuwać i lepiej eksplorować powiązania między różnymi tematami.")
                        
                        try:
                            from utils.mind_map import create_lesson_mind_map
                            mind_map_result = create_lesson_mind_map(lesson)
                            
                            if mind_map_result is None:
                                st.info("💡 **Mapa myśli w przygotowaniu**\n\nDla tej lekcji przygotowujemy interaktywną mapę myśli, która pomoże Ci lepiej zrozumieć powiązania między różnymi konceptami. Wkrótce będzie dostępna!")
                        except Exception as e:
                            st.warning("⚠️ Mapa myśli nie jest obecnie dostępna. Sprawdź, czy wszystkie wymagane biblioteki są zainstalowane.")
                            st.expander("Szczegóły błędu (dla deweloperów)").write(str(e))
            else:
                # Brak podsumowania w danych lekcji
                st.error("Lekcja nie zawiera podsumowania!")
          # Zamknij div .st-bx
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Add live XP indicator - ZAKOMENTOWANE
        # live_xp_indicator()        # Show lesson progress with current XP system
        # Pobierz aktualne dane fragmentów
        fragment_progress = get_lesson_fragment_progress(lesson_id)
          # Synchronizuj stan sesji z rzeczywistymi danymi fragmentów
        for step in step_order:
            completed_key = f"{step}_completed"
            if completed_key in fragment_progress:
                st.session_state.lesson_progress[step] = fragment_progress[completed_key]
        
        # Oblicz zdobyte XP na podstawie rzeczywistych danych z systemu fragmentów
        current_xp = 0
        for step in step_order:
            step_xp_key = f"{step}_xp"
            if step_xp_key in fragment_progress:
                current_xp += fragment_progress[step_xp_key]
          # Oblicz aktualny postęp na podstawie XP (nie liczby kroków)
        completion_percent = (current_xp / max_xp) * 100 if max_xp > 0 else 0
          # Przygotuj dane o kluczowych krokach do wyświetlenia
        key_steps_info = []
        if 'intro' in step_order:
            completed = fragment_progress.get('intro_completed', False)
            key_steps_info.append(f"📖 Intro: {step_xp_values['intro']} XP {'✅' if completed else ''}")
        
        # opening_quiz usunięte - jest teraz zintegrowane w zakładce intro
        
        if 'content' in step_order:
            completed = fragment_progress.get('content_completed', False)
            key_steps_info.append(f"📚 Treść: {step_xp_values['content']} XP {'✅' if completed else ''}")
        
        if 'practical_exercises' in step_order:
            completed = fragment_progress.get('practical_exercises_completed', False)
            key_steps_info.append(f"🎯 Ćwiczenia praktyczne: {step_xp_values['practical_exercises']} XP {'✅' if completed else ''}")
        
        if 'reflection' in step_order:
            completed = fragment_progress.get('reflection_completed', False)
            key_steps_info.append(f"🤔 Refleksja: {step_xp_values['reflection']} XP {'✅' if completed else ''}")
        
        if 'application' in step_order:
            completed = fragment_progress.get('application_completed', False)
            key_steps_info.append(f"💪 Zadania: {step_xp_values['application']} XP {'✅' if completed else ''}")
        
        if 'summary' in step_order:
            completed = fragment_progress.get('summary_completed', False)
            key_steps_info.append(f"📋 Podsumowanie: {step_xp_values['summary']} XP {'✅' if completed else ''}")
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; padding: 20px; margin-bottom: 20px; color: white;">
            <h3 style="margin: 0 0 10px 0;">📚 {lesson.get('title', 'Lekcja')}</h3>
            <div style="background: rgba(255,255,255,0.2); border-radius: 10px; padding: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: bold;">Postęp lekcji: {completion_percent:.0f}%</span>
                    <span>💎 {current_xp}/{max_xp} XP</span>
                </div>
                <div style="background: rgba(255,255,255,0.3); border-radius: 5px; height: 12px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #4caf50, #2196f3); 
                                width: {completion_percent}%; height: 100%; transition: width 0.3s ease;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 12px; flex-wrap: wrap; gap: 5px;">
                    {' '.join([f'<span>{info}</span>' for info in key_steps_info[:3]])}
                </div>
                {f'<div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 12px; flex-wrap: wrap; gap: 5px;">{" ".join([f"<span>{info}</span>" for info in key_steps_info[3:]])}</div>' if len(key_steps_info) > 3 else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)


def display_lesson(lesson_data):
    """Wyświetla lekcję z nowymi sekcjami quizów"""
    
    # Wyświetl tytuł lekcji
    st.markdown(f"<h1>{lesson_data['title']}</h1>", unsafe_allow_html=True)
    
    # Wyświetl wprowadzenie
    if 'intro' in lesson_data:
        st.markdown(lesson_data['intro'], unsafe_allow_html=True)
    
    # Przygotuj dane zakładek
    tab_data = []    # Dodaj zakładki w odpowiedniej kolejności (usunięto opening_quiz - jest teraz w intro)
    
    if 'learning' in lesson_data.get('sections', {}):
        tab_data.append(("Nauka", "learning"))    
    if 'reflection' in lesson_data.get('sections', {}):
        tab_data.append(("Refleksja", "reflection"))
    
    # Wyodrębnij tytuły zakładek
    tab_titles = [title for title, _ in tab_data]
    
    # Wyświetl zakładki tylko jeśli są jakieś dane do wyświetlenia
    if tab_titles:
        tabs = tabs_with_fallback(tab_titles)        # Dla każdej zakładki wyświetl odpowiednią zawartość
        for i, (_, tab_name) in enumerate(tab_data):
            with tabs[i]:
                if tab_name == "learning":
                    display_learning_sections(lesson_data['sections'][tab_name])
                elif tab_name == "reflection":
                    display_reflection_sections(lesson_data['sections'][tab_name])
    else:
        st.warning("Ta lekcja nie zawiera żadnych sekcji do wyświetlenia.")


# Dodanie brakujących funkcji
def display_learning_sections(learning_data):
    """Wyświetla sekcje nauki z lekcji"""
    if not learning_data or 'sections' not in learning_data:
        st.warning("Brak treści edukacyjnych w tej lekcji.")
        return
        
    for section in learning_data['sections']:
        content_section(
            section.get("title", "Tytuł sekcji"), 
            section.get("content", "Brak treści"), 
            collapsed=False
        )


def display_reflection_sections(reflection_data):
    """Wyświetla sekcje refleksji z lekcji"""
    if not reflection_data:
        st.warning("Brak zadań refleksyjnych w tej lekcji.")
        return
        
    # Check if there are sections in the data
    if 'sections' not in reflection_data:
        st.warning("Dane refleksji nie zawierają sekcji.")
        return
        
    for section in reflection_data['sections']:
        st.markdown(f"### {section.get('title', 'Zadanie refleksyjne')}")
        st.markdown(section.get("content", "Brak treści"), unsafe_allow_html=True)
        
        # Dodaj pole tekstowe do wprowadzania odpowiedzi
        reflection_key = f"reflection_{section.get('title', '').replace(' ', '_').lower()}"
        user_reflection = st.text_area(
            "Twoja odpowiedź:",
            value=st.session_state.get(reflection_key, ""),
            height=200,
            key=reflection_key
        )
        
        # Dodaj przycisk do zapisywania odpowiedzi
        if st.button("Zapisz odpowiedź", key=f"save_{reflection_key}"):
            st.session_state[reflection_key] = user_reflection
            st.success("Twoja odpowiedź została zapisana!")

def display_quiz(quiz_data, passing_threshold=60):
    """Wyświetla quiz z pytaniami i opcjami odpowiedzi. Zwraca True, gdy quiz jest ukończony."""
    
    # Style CSS TYLKO dla przycisków odpowiedzi quiz - nie wpływa na nawigację
    st.markdown("""
    <style>
    .quiz-question {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;+
        border-radius: 15px;
        margin: 20px 0;
        border-left: 5px solid #4caf50;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .quiz-question h3 {
        color: #2e7d32;
        margin: 0;
        font-size: 1.2em;
    }
    
    .quiz-final-button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 10px;
        font-size: 1.1em;
        font-weight: bold;
        margin: 20px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    
    .quiz-final-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
    }
    
    .quiz-results {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 5px solid #2196f3;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    if not quiz_data or "questions" not in quiz_data:
        st.warning("Ten quiz nie zawiera żadnych pytań.")
        return False, False, 0
        
    # DEBUG - Wyświetl podstawowe informacje o quizie na początku
    st.warning("🔧 DEBUG: Wewnątrz display_quiz funkcji")
    st.write(f"Quiz title: {quiz_data.get('title', 'No title')}")
    st.write(f"Number of questions: {len(quiz_data.get('questions', []))}")
    
    st.markdown(f"<h2>{quiz_data.get('title', 'Quiz')}</h2>", unsafe_allow_html=True)
    
    if "description" in quiz_data:
        st.markdown(quiz_data['description'])
    
    # Sprawdź czy to quiz samodiagnozy (wszystkie correct_answer są null)
    is_self_diagnostic = all(q.get('correct_answer') is None for q in quiz_data['questions'])
    
    quiz_id = f"quiz_{quiz_data.get('title', '').replace(' ', '_').lower()}"
    
    # Klucz dla zapisywania wyników w danych użytkownika
    results_key = f"{quiz_id}_results"
    
    # Sprawdź czy quiz został już ukończony i są zapisane wyniki
    completed_quiz_data = None
    if 'user_data' in st.session_state and results_key in st.session_state.user_data:
        completed_quiz_data = st.session_state.user_data[results_key]
    
    # Przycisk "Przystąp ponownie" jeśli quiz był już ukończony
    if completed_quiz_data:
        st.markdown('<div class="quiz-results">', unsafe_allow_html=True)
        st.success(f"✅ Ukończyłeś już ten quiz w dniu: {completed_quiz_data.get('completion_date', 'nieznana data')}")
        
        # Wyświetl poprzednie wyniki
        if 'answers' in completed_quiz_data:
            with st.expander("🔍 Zobacz raport z quizu"):
                quiz_type = quiz_data.get('type', 'buttons')
                
                # Sprawdź czy mamy szczegółowe wyniki
                if 'question_results' in completed_quiz_data:
                    # Nowy format z szczegółowymi wynikami
                    question_results = completed_quiz_data['question_results']
                    total_points = completed_quiz_data.get('total_points', 0)
                    correct_answers = completed_quiz_data.get('correct_answers', 0)
                    
                    # Dla quizów autodiagnozy - najpierw spersonalizowane wyniki Conversational Intelligence
                    if is_self_diagnostic:
                        quiz_title_lower = quiz_data.get('title', '').lower()
                        conditions = [
                            'conversational intelligence' in quiz_title_lower,
                            'c-iq' in quiz_title_lower,
                            'od słów do zaufania' in quiz_title_lower,
                            'jak ważne może być' in quiz_title_lower
                        ]
                        
                        if any(conditions):
                            display_self_diagnostic_results(quiz_data, completed_quiz_data['answers'])
                    
                    # Potem szczegółowe wyniki quizu
                    display_quiz_results(quiz_data, question_results, total_points, correct_answers, is_self_diagnostic, quiz_type)
                
                else:
                    # Stary format - zachowaj kompatybilność
                    if quiz_type == 'slider':
                        scale = quiz_data.get('scale', {'min': 1, 'max': 5})
                        labels = scale.get('labels', {})
                        
                        total_points = 0
                        for i, (question, answer) in enumerate(zip(quiz_data['questions'], completed_quiz_data['answers'])):
                            st.write(f"**Pytanie {i+1}:** {question['question']}")
                            answer_label = labels.get(str(answer), str(answer))
                            st.write(f"**Odpowiedź:** {answer} - {answer_label}")
                            total_points += answer
                            st.markdown("---")
                        
                        st.info(f"**Łączna suma punktów:** {total_points}/{len(quiz_data['questions']) * scale['max']}")
                    else:
                        # Stary format z opcjami
                        for i, (question, answer) in enumerate(zip(quiz_data['questions'], completed_quiz_data['answers'])):
                            st.write(f"**Pytanie {i+1}:** {question['question']}")
                            if isinstance(answer, int) and answer < len(question.get('options', [])):
                                st.write(f"**Odpowiedź:** {question['options'][answer]}")
                            st.markdown("---")
        
        # Przycisk ponownego przystąpienia na końcu
        st.markdown("---")
        help_text = "Możesz ponownie wypełnić quiz aby zaktualizować swoją autorefleksję" if is_self_diagnostic else "Możesz ponownie przystąpić do quizu aby poprawić swój wynik"
        if st.button("🔄 Przystąp do quizu ponownie", key=f"{quiz_id}_restart", help=help_text):
            # Wyczyść dane sesji dla tego quizu
            if quiz_id in st.session_state:
                del st.session_state[quiz_id]
            
            # Wyczyść wszystkie klucze związane z tym quizem (suwaki, checkboxy, radio)
            keys_to_delete = []
            for key in st.session_state.keys():
                if isinstance(key, str) and key.startswith(f"{quiz_id}_"):
                    keys_to_delete.append(key)
            
            for key in keys_to_delete:
                del st.session_state[key]
            
            # Usuń wyniki z persistent storage
            if 'user_data' in st.session_state and results_key in st.session_state.user_data:
                del st.session_state.user_data[results_key]
            
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sprawdź czy quiz został zdany na podstawie passing_threshold
        if is_self_diagnostic:
            # Quizy autodiagnozy zawsze zaliczone gdy ukończone
            quiz_passed = True
        else:
            # Dla quizów testowych sprawdź wynik
            correct = completed_quiz_data.get('correct_answers', 0)
            total = len(quiz_data['questions'])
            percentage = (correct / total) * 100 if total > 0 else 0
            quiz_passed = percentage >= passing_threshold
        
        return True, quiz_passed, completed_quiz_data.get('total_points', 0)
    
    # Inicjalizacja stanu quizu
    if quiz_id not in st.session_state:
        st.session_state[quiz_id] = {
            "answers": [None] * len(quiz_data['questions']),
            "completed": False,
            "total_points": 0,
            "correct_answers": 0
        }
    else:
        # Sprawdź czy liczba pytań się zmieniła i dostosuj listę odpowiedzi
        expected_length = len(quiz_data['questions'])
        current_length = len(st.session_state[quiz_id]["answers"])
        
        if current_length != expected_length:
            # Dostosuj długość listy odpowiedzi
            if current_length < expected_length:
                # Dodaj brakujące None'y
                st.session_state[quiz_id]["answers"].extend([None] * (expected_length - current_length))
            else:
                # Obetnij listę do odpowiedniej długości
                st.session_state[quiz_id]["answers"] = st.session_state[quiz_id]["answers"][:expected_length]
    
    # Wyświetl wszystkie pytania
    quiz_type = quiz_data.get('type', 'buttons')
    all_answered = True
    
    for i, question in enumerate(quiz_data['questions']):
        question_id = f"{quiz_id}_q{i}"
        
        # Kontener dla pytania
        st.markdown(f"""
        <div class="quiz-question">
            <h3>Pytanie {i+1}: {question['question']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if quiz_type == 'slider' or question.get('type') == 'slider':
            # Quiz ze suwakami
            scale = quiz_data.get('scale', {'min': 1, 'max': 5})
            min_val = scale['min']
            max_val = scale['max']
            default_val = question.get('default', (min_val + max_val) // 2)
            
            # Wyświetl etykiety skali
            if 'labels' in scale:
                labels_html = "<div style='display: flex; justify-content: space-between; margin: 10px 0; font-size: 0.9em; color: #666;'>"
                for value in range(min_val, max_val + 1):
                    label = scale['labels'].get(str(value), str(value))
                    labels_html += f"<span><strong>{value}</strong>: {label}</span>"
                labels_html += "</div>"
                st.markdown(labels_html, unsafe_allow_html=True)
            
            # Użyj poprzedniej odpowiedzi jako wartość domyślną, jeśli istnieje
            if i < len(st.session_state[quiz_id]["answers"]):
                current_value = st.session_state[quiz_id]["answers"][i]
            else:
                current_value = None
            if current_value is None:
                current_value = default_val
            
            # Suwak
            slider_key = f"{question_id}_slider"
            selected_value = st.slider(
                "Twoja ocena:",
                min_value=min_val,
                max_value=max_val,
                value=current_value,
                key=slider_key,
                help=f"Przesuń suwak, aby wybrać wartość od {min_val} do {max_val}"
            )
            
            # Zapisz odpowiedź w czasie rzeczywistym
            # Upewnij się, że lista jest wystarczająco długa przed zapisem
            if i >= len(st.session_state[quiz_id]["answers"]):
                st.session_state[quiz_id]["answers"].extend([None] * (i + 1 - len(st.session_state[quiz_id]["answers"])))
            
            st.session_state[quiz_id]["answers"][i] = selected_value
            
        else:
            # Stary format z przyciskami/checkboxami
            if question.get('type') == 'multiple_choice':
                st.write("**Wybierz wszystkie poprawne odpowiedzi:**")
                if i < len(st.session_state[quiz_id]["answers"]):
                    current_answers = st.session_state[quiz_id]["answers"][i] or []
                else:
                    current_answers = []
                selected_options = []
                
                for j, option in enumerate(question['options']):
                    checkbox_key = f"{question_id}_opt{j}"
                    checked = j in current_answers
                    if st.checkbox(option, value=checked, key=checkbox_key):
                        selected_options.append(j)
                
                # Upewnij się, że lista jest wystarczająco długa przed zapisem
                if i >= len(st.session_state[quiz_id]["answers"]):
                    st.session_state[quiz_id]["answers"].extend([None] * (i + 1 - len(st.session_state[quiz_id]["answers"])))
                
                st.session_state[quiz_id]["answers"][i] = selected_options
                if not selected_options:
                    all_answered = False
                    
            else:
                # Single choice
                if i < len(st.session_state[quiz_id]["answers"]):
                    current_answer = st.session_state[quiz_id]["answers"][i]
                else:
                    current_answer = None
                selected_option = st.radio(
                    "Wybierz odpowiedź:",
                    options=range(len(question['options'])),
                    format_func=lambda x: question['options'][x],
                    index=current_answer if current_answer is not None else None,
                    key=f"{question_id}_radio"
                )
                
                # Upewnij się, że lista jest wystarczająco długa przed zapisem
                if i >= len(st.session_state[quiz_id]["answers"]):
                    st.session_state[quiz_id]["answers"].extend([None] * (i + 1 - len(st.session_state[quiz_id]["answers"])))
                
                st.session_state[quiz_id]["answers"][i] = selected_option
                if selected_option is None:
                    all_answered = False
        
        st.markdown("---")
    
    # Sprawdź czy wszystkie pytania zostały odpowiedziane
    for i, answer in enumerate(st.session_state[quiz_id]["answers"]):
        if answer is None or (isinstance(answer, list) and len(answer) == 0):
            all_answered = False
            break
    
    # Przycisk zatwierdzenia wszystkich odpowiedzi
    if all_answered:
        st.markdown('<div style="text-align: center; margin: 30px 0;">', unsafe_allow_html=True)
        if st.button("🎯 Zatwierdź wszystkie odpowiedzi", key=f"{quiz_id}_submit_all", help="Zatwierdź quiz i zapisz wyniki"):
            # Oblicz wyniki
            total_points = 0
            correct_answers = 0
            question_results = []  # Szczegółowe wyniki dla każdego pytania
            
            for i, (question, answer) in enumerate(zip(quiz_data['questions'], st.session_state[quiz_id]["answers"])):
                question_result = {
                    'question': question['question'],
                    'user_answer': answer,
                    'is_correct': False,
                    'points_earned': 0
                }
                
                if quiz_type == 'slider':
                    question_result['points_earned'] = answer
                    total_points += answer
                else:
                    if is_self_diagnostic:
                        # Dla quizów autodiagnozy: opcje 0-4 = 1-5 punktów
                        if isinstance(answer, list):
                            points = sum(j + 1 for j in answer)
                            question_result['points_earned'] = points
                            total_points += points
                        else:
                            points = answer + 1
                            question_result['points_earned'] = points
                            total_points += points
                    else:
                        # Dla quizów testowych
                        correct_answer = question.get('correct_answer')
                        if correct_answer is not None:
                            if answer == correct_answer:
                                correct_answers += 1
                                question_result['is_correct'] = True
                                question_result['points_earned'] = 1
                            question_result['correct_answer'] = correct_answer
                        elif question.get('type') == 'multiple_choice':
                            correct_answers_list = question.get('correct_answers', [])
                            if set(answer) == set(correct_answers_list):
                                correct_answers += 1
                                question_result['is_correct'] = True
                                question_result['points_earned'] = 1
                            question_result['correct_answers'] = correct_answers_list
                
                question_results.append(question_result)
            
            # Zapisz wyniki do danych użytkownika (persistent storage)
            if 'user_data' not in st.session_state:
                st.session_state.user_data = {}
            
            from datetime import datetime
            completion_date = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            st.session_state.user_data[results_key] = {
                'answers': st.session_state[quiz_id]["answers"].copy(),
                'total_points': total_points,
                'correct_answers': correct_answers,
                'completion_date': completion_date,
                'quiz_type': quiz_type,
                'question_results': question_results  # Dodaj szczegółowe wyniki
            }
            
            # Oznacz quiz jako ukończony
            st.session_state[quiz_id]["completed"] = True
            st.session_state[quiz_id]["total_points"] = total_points
            st.session_state[quiz_id]["correct_answers"] = correct_answers  # Dodaj dla sprawdzania zaliczenia
            
            st.success(f"✅ Quiz został ukończony! Twoje wyniki zostały zapisane.")
            
            # Dla quizów autodiagnozy wyświetl spersonalizowane wyniki jeśli dostępne
            if is_self_diagnostic and 'results_interpretation' in quiz_data:
                try:
                    display_self_diagnostic_results(quiz_data, st.session_state[quiz_id]["answers"])
                except Exception as e:
                    st.error(f"Błąd podczas wyświetlania spersonalizowanych wyników: {e}")
            
            # Wyświetl szczegółowe wyniki quizu
            display_quiz_results(quiz_data, question_results, total_points, correct_answers, is_self_diagnostic, quiz_type)
            
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Odpowiedz na wszystkie pytania, aby móc zatwierdzić quiz.")
    
    # Zwróć status ukończenia
    quiz_completed = st.session_state[quiz_id].get("completed", False)
    earned_points = st.session_state[quiz_id].get("total_points", 0)
    
    # Sprawdź czy quiz został zdany na podstawie passing_threshold
    if quiz_completed:
        if is_self_diagnostic:
            # Quizy autodiagnozy zawsze zaliczone gdy ukończone
            quiz_passed = True
        else:
            # Dla quizów testowych sprawdź wynik z saved data
            if completed_quiz_data and 'correct_answers' in completed_quiz_data:
                correct = completed_quiz_data['correct_answers']
                total = len(quiz_data['questions'])
                percentage = (correct / total) * 100 if total > 0 else 0
                quiz_passed = percentage >= passing_threshold
            else:
                # Fallback - sprawdź current session state
                correct = st.session_state[quiz_id].get("correct_answers", 0)
                total = st.session_state[quiz_id].get("total_questions", len(quiz_data['questions']))
                percentage = (correct / total) * 100 if total > 0 else 0
                quiz_passed = percentage >= passing_threshold
    else:
        quiz_passed = False
    
    return quiz_completed, quiz_passed, earned_points


def check_lesson_prerequisites(lesson_id, user_progress):
    """
    Sprawdza czy użytkownik ma wymagane wyniki z poprzednich lekcji
    """
    # Pobierz ustawienia wymagań dla lekcji
    lesson_requirements = get_lesson_requirements(lesson_id)
    
    if not lesson_requirements:
        return True  # Brak wymagań = dostęp dozwolony
    
    for requirement in lesson_requirements:
        required_lesson = requirement.get('lesson')
        required_score = requirement.get('min_score', 0)
        
        # Sprawdź wynik z wymaganej lekcji
        if required_lesson not in user_progress:
            return False
        
        lesson_data = user_progress[required_lesson]
        score = lesson_data.get('quiz_score', 0)
        
        if score < required_score:
            return False
    
    return True


def get_lesson_requirements(lesson_id):
    """
    Pobiera wymagania dla danej lekcji
    """
    # W przyszłości można to przenieść do pliku konfiguracyjnego
    requirements = {
        "1": [],  # Pierwsza lekcja - brak wymagań
        "2": [{"lesson": "1", "min_score": 60}],  # Druga lekcja wymaga 60% z pierwszej
        "3": [{"lesson": "2", "min_score": 60}],  # itd.
    }
    
    return requirements.get(lesson_id, [])
    
    # Wyświetl wszystkie pytania
    for i, question in enumerate(quiz_data['questions']):
        question_id = f"{quiz_id}_q{i}"
        
        # Kontener dla pytania z własnymi stylami
        st.markdown(f"""
        <div class="quiz-question">
            <h3>Pytanie {i+1}: {question['question']}</h3>
        </div>
        """, unsafe_allow_html=True)          # Jeśli pytanie już zostało odpowiedziane, pokaż wynik
        if i in st.session_state[quiz_id]["answered_questions"]:
            selected = st.session_state.get(f"{question_id}_selected")
            question_type = question.get('type', 'single_choice')
            quiz_type = quiz_data.get('type', 'buttons')
            
            # Obsługa wyświetlania odpowiedzi dla suwaków
            if quiz_type == 'slider' or question_type == 'slider':
                scale = quiz_data.get('scale', {'min': 1, 'max': 5})
                labels = scale.get('labels', {})
                selected_label = labels.get(str(selected), str(selected))
                
                st.markdown(f"✓ **Twoja odpowiedź: {selected} - {selected_label}**")
                
                # Wyświetl skalę dla kontekstu
                if 'labels' in scale:
                    labels_html = "<div style='background: #f8f9fa; padding: 10px; border-radius: 8px; margin: 10px 0; font-size: 0.9em;'>"
                    labels_html += "<strong>Skala ocen:</strong><br>"
                    for value in range(scale['min'], scale['max'] + 1):
                        label = labels.get(str(value), str(value))
                        style = "background: #4caf50; color: white; padding: 2px 6px; border-radius: 4px;" if value == selected else ""
                        labels_html += f"<span style='{style}'>{value}: {label}</span> "
                    labels_html += "</div>"
                    st.markdown(labels_html, unsafe_allow_html=True)
            else:
                # Wyświetl odpowiedzi z oznaczeniem poprawnej (stary kod)
                for j, option in enumerate(question['options']):
                    # Dla quizów samodiagnozy - wszystkie opcje równe
                    if is_self_diagnostic:
                        if isinstance(selected, list):
                            # Wielokrotny wybór w samodiagnozie (rzadko używane)
                            if j in selected:
                                st.markdown(f"✓ **{option}** _(Twoja odpowiedź)_")
                            else:
                                st.markdown(f"○ {option}")
                        else:
                            # Pojedynczy wybór w samodiagnozie
                            if j == selected:
                                st.markdown(f"✓ **{option}** _(Twoja odpowiedź)_")
                            else:
                                st.markdown(f"○ {option}")
                    else:
                        # Dla quizów z poprawnymi odpowiedziami
                        if question_type == 'multiple_choice':
                            # Pytania z wielokrotnym wyborem
                            correct_answers = question.get('correct_answers', [])
                            selected_list = selected if isinstance(selected, list) else []
                            
                            if j in correct_answers and j in selected_list:
                                st.markdown(f"✅ **{option}** _(Poprawna odpowiedź - wybrana)_")
                            elif j in correct_answers and j not in selected_list:
                                st.markdown(f"✅ **{option}** _(Poprawna odpowiedź - nie wybrana)_")
                            elif j not in correct_answers and j in selected_list:
                                st.markdown(f"❌ **{option}** _(Niepoprawna odpowiedź - wybrana)_")
                            else:
                                st.markdown(f"○ {option}")
                        else:
                            # Pytania z pojedynczym wyborem
                            correct_answer = question.get('correct_answer')
                            is_correct = correct_answer is not None and selected == correct_answer
                            
                            if correct_answer is not None:
                                if j == correct_answer:
                                    st.markdown(f"✅ **{option}** _(Poprawna odpowiedź)_")
                                elif j == selected and not is_correct:
                                    st.markdown(f"❌ **{option}** _(Twoja odpowiedź)_")
                                else:
                                    st.markdown(f"○ {option}")
                            else:
                                st.markdown(f"○ {option}")
              # Wyświetl wyjaśnienie
            if "explanation" in question:
                st.info(question['explanation'])
            
            st.markdown("---")
        else:
            # Określ typ quizu i użyj odpowiedniej klasy CSS
            quiz_type_class = "self-reflection-quiz" if is_self_diagnostic else "test-quiz"
            
            # Rozpocznij sekcję przycisków odpowiedzi quiz z odpowiednią klasą
            st.markdown(f'<div class="quiz-answers-section {quiz_type_class}">', unsafe_allow_html=True)
            
            # Sprawdź czy to quiz ze suwakami
            question_type = question.get('type', 'single_choice')
            quiz_type = quiz_data.get('type', 'buttons')
            
            if quiz_type == 'slider' or question_type == 'slider':
                # Quiz ze suwakami
                scale = quiz_data.get('scale', {'min': 1, 'max': 5})
                min_val = scale['min']
                max_val = scale['max']
                default_val = question.get('default', (min_val + max_val) // 2)
                
                # Wyświetl etykiety skali
                if 'labels' in scale:
                    labels_html = "<div style='display: flex; justify-content: space-between; margin: 10px 0; font-size: 0.9em; color: #666;'>"
                    for value in range(min_val, max_val + 1):
                        label = scale['labels'].get(str(value), str(value))
                        labels_html += f"<span><strong>{value}</strong>: {label}</span>"
                    labels_html += "</div>"
                    st.markdown(labels_html, unsafe_allow_html=True)
                
                # Suwak
                slider_key = f"{question_id}_slider"
                selected_value = st.slider(
                    "Twoja ocena:",
                    min_value=min_val,
                    max_value=max_val,
                    value=default_val,
                    key=slider_key,
                    help=f"Przesuń suwak, aby wybrać wartość od {min_val} do {max_val}"
                )
                
                # Przycisk zatwierdzenia
                if st.button("Zatwierdź odpowiedź", key=f"{question_id}_submit_slider"):
                    # Zapisz wybraną wartość
                    st.session_state[f"{question_id}_selected"] = selected_value
                    st.session_state[quiz_id]["answered_questions"].append(i)
                    
                    # Dla quizów samodiagnozy - zlicz punkty
                    if "total_points" not in st.session_state[quiz_id]:
                        st.session_state[quiz_id]["total_points"] = 0
                    st.session_state[quiz_id]["total_points"] += selected_value
                    
                    if len(st.session_state[quiz_id]["answered_questions"]) == st.session_state[quiz_id]["total_questions"]:
                        st.session_state[quiz_id]["completed"] = True
                    
                    st.rerun()
                    return False, False, 0
                    
            elif is_self_diagnostic:
                # Quiz autorefleksji - przyciski krótkie, dopasowane do treści
                for j, option in enumerate(question['options']):
                    # Każdy przycisk w osobnej kolumnie o minimalnej szerokości
                    col1, col2 = st.columns([1, 3])  # Pierwsza kolumna mała, druga większa ale niewykorzystana
                    
                    with col1:
                        if st.button(option, key=f"{question_id}_opt{j}"):
                            # Zapisz wybraną odpowiedź
                            st.session_state[f"{question_id}_selected"] = j
                            st.session_state[quiz_id]["answered_questions"].append(i)                            # Dla quizów samodiagnozy - zlicz punkty (opcje 1-5 = j+1 punktów)
                            points = j + 1
                            if "total_points" not in st.session_state[quiz_id]:
                                st.session_state[quiz_id]["total_points"] = 0
                            st.session_state[quiz_id]["total_points"] += points
                            if len(st.session_state[quiz_id]["answered_questions"]) == st.session_state[quiz_id]["total_questions"]:
                                st.session_state[quiz_id]["completed"] = True
                                # Usunięto opening_quiz handling - jest teraz zintegrowane w intro
                            st.rerun()
                            return False, False, 0
            else:
                # Quiz testowy - przyciski pełnej szerokości
                question_type = question.get('type', 'single_choice')
                if question_type == 'multiple_choice':
                    # Pytanie z wielokrotnym wyborem
                    st.write("**Wybierz wszystkie poprawne odpowiedzi:**")
                    
                    # Zbierz aktualny stan checkboxów
                    for j, option in enumerate(question['options']):
                        checkbox_key = f"{question_id}_opt{j}"
                        st.checkbox(option, key=checkbox_key)
                    
                    # Przycisk do zatwierdzenia odpowiedzi z unikatowym kluczem
                    submit_key = f"{question_id}_submit"
                      # Przycisk do zatwierdzenia odpowiedzi
                    if st.button("Zatwierdź odpowiedzi", key=submit_key):
                        selected_options = []
                        for j, option in enumerate(question['options']):
                            checkbox_key = f"{question_id}_opt{j}"
                            if st.session_state.get(checkbox_key, False):
                                selected_options.append(j)
                        if selected_options:
                            st.session_state[f"{question_id}_selected"] = selected_options
                            st.session_state[quiz_id]["answered_questions"].append(i)
                            correct_answers = question.get('correct_answers', [])
                            if set(selected_options) == set(correct_answers):
                                st.session_state[quiz_id]["correct_answers"] += 1
                                if "quiz_score" in st.session_state:
                                    st.session_state.quiz_score += 5
                            if len(st.session_state[quiz_id]["answered_questions"]) == st.session_state[quiz_id]["total_questions"]:
                                st.session_state[quiz_id]["completed"] = True
                            st.rerun()
                            return False, False, 0
                    else:
                        st.warning("Wybierz przynajmniej jedną odpowiedź przed zatwierdzeniem.")
                else:
                    # Pytanie z pojedynczym wyborem (domyślne)
                    for j, option in enumerate(question['options']):
                        if st.button(option, key=f"{question_id}_opt{j}"):
                            st.session_state[f"{question_id}_selected"] = j
                            st.session_state[quiz_id]["answered_questions"].append(i)
                            correct_answer = question.get('correct_answer')
                            if correct_answer is not None and j == correct_answer:
                                st.session_state[quiz_id]["correct_answers"] += 1
                                if "quiz_score" in st.session_state:
                                    st.session_state.quiz_score += 5
                            if len(st.session_state[quiz_id]["answered_questions"]) == st.session_state[quiz_id]["total_questions"]:
                                st.session_state[quiz_id]["completed"] = True
                            st.rerun()
                            return False, False, 0
        st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("---")
    
    # Sprawdź czy quiz jest ukończony i oblicz punkty
    is_completed = st.session_state[quiz_id].get("completed", False)
    
    if is_completed:
        if is_self_diagnostic:
            # Quiz samodiagnozy - wyświetl punkty i interpretację
            total_points = st.session_state[quiz_id].get("total_points", 0)
            
            # Oblicz maksymalne możliwe punkty (liczba pytań × 5)
            max_possible_points = len(quiz_data['questions']) * 5;
            
            st.markdown(f"""
            <div class="quiz-summary">
                <h3>📊 Twój wynik: {total_points}/{max_possible_points} punktów</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Wyświetl interpretację wyników jeśli dostępna
            if 'scoring' in quiz_data and 'interpretation' in quiz_data['scoring']:
                interpretation_found = False
                for score_range, interpretation in quiz_data['scoring']['interpretation'].items():
                    # Parsuj zakres punktów (np. "10-20", "21-35", "36-50")
                    if '-' in score_range:
                        min_score, max_score = map(int, score_range.split('-'))
                        if min_score <= total_points <= max_score:
                            st.success(f"🧮 **Interpretacja wyników:**\n\n{interpretation}")
                            interpretation_found = True
                            break
                
                if not interpretation_found:
                    st.info("🪞 Dziękujemy za szczerą samorefleksję! Twoje odpowiedzi pomogą nam lepiej dopasować materiał do Twojego stylu inwestowania.")
            else:
                st.info("🪞 Dziękujemy za szczerą samorefleksję! Twoje odpowiedzi pomogą nam lepiej dopasować materiał do Twojego stylu inwestowania.")
              # Zawsze "zdany" dla quizu samodiagnozy
            return is_completed, True, total_points
            
        else:            # Standardowy quiz z poprawnymi odpowiedziami
            correct = st.session_state[quiz_id]["correct_answers"]
            total = st.session_state[quiz_id]["total_questions"]
            percentage = (correct / total) * 100
            
            # Oblicz punkty - wartość zależy od procentu odpowiedzi poprawnych
            quiz_xp_value = 15
            earned_points = int(quiz_xp_value * (percentage / 100))
            
            # Czy quiz został zdany (na podstawie passing_threshold)
            is_passed = percentage >= passing_threshold
            
            st.markdown(f"""
            <div class="quiz-summary">
                <h3>Twój wynik: {correct}/{total} ({percentage:.0f}%)</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Wyświetl interpretację wyników jeśli dostępna (nowy system)
            if 'result_interpretation' in quiz_data:
                interpretation_found = False
                interpretations = quiz_data['result_interpretation']
                
                # Sprawdź każdy próg interpretacji od najwyższego do najniższego
                for key in ['excellent', 'good', 'needs_improvement', 'poor']:
                    if key in interpretations:
                        threshold = interpretations[key].get('threshold', 0)
                        if percentage >= threshold:
                            title = interpretations[key].get('title', 'Wynik')
                            message = interpretations[key].get('message', 'Brak opisu')
                            st.success(f"**{title}**\n\n{message}")
                            interpretation_found = True
                            break
                
                if not interpretation_found:
                    # Fallback do standardowych komunikatów
                    if percentage >= 80:
                        st.success("Świetnie! Doskonale rozumiesz ten temat.")
                    elif percentage >= passing_threshold:
                        if passing_threshold > 60:
                            st.success(f"Bardzo dobrze! Osiągnąłeś wymagany próg {passing_threshold}% i możesz kontynuować.")
                        else:
                            st.success("Bardzo dobrze! Możesz kontynuować naukę.")
                    else:
                        if passing_threshold > 60:
                            st.error(f"Aby przejść dalej, musisz uzyskać przynajmniej {passing_threshold}% poprawnych odpowiedzi. Spróbuj ponownie!")
                        else:
                            st.warning("Spróbuj jeszcze raz - możesz to zrobić lepiej!")
            else:
                # Standardowe komunikaty jeśli brak interpretacji
                if percentage >= 80:
                    st.success("Świetnie! Doskonale rozumiesz ten temat.")
                elif percentage >= passing_threshold:
                    if passing_threshold > 60:
                        st.success(f"Bardzo dobrze! Osiągnąłeś wymagany próg {passing_threshold}% i możesz kontynuować.")
                    else:
                        st.success("Bardzo dobrze! Możesz kontynuować naukę.")
                else:
                    if passing_threshold > 60:
                        st.error(f"Aby przejść dalej, musisz uzyskać przynajmniej {passing_threshold}% poprawnych odpowiedzi. Spróbuj ponownie!")
                    else:
                        st.warning("Spróbuj jeszcze raz - możesz to zrobić lepiej!")
            
            return is_completed, is_passed, earned_points
    
    # Quiz nie jest jeszcze ukończony
    return is_completed, False, 0


def display_self_diagnostic_results(quiz_data, answers):
    """Uniwersalna funkcja do wyświetlania wyników quizów autodiagnozy na podstawie konfiguracji z JSON"""
    
    if 'results_interpretation' not in quiz_data:
        st.info("Brak konfiguracji wyników dla tego quizu samodiagnozy.")
        return
    
    interpretation = quiz_data['results_interpretation']
    
    st.markdown("---")
    st.markdown("## 🎯 Twoje spersonalizowane wyniki")
    
    # Oblicz wynik na podstawie tej samej metody co główny system
    # Opcje 0-4 = 1-5 punktów (answer + 1)
    total_score = sum(answer + 1 for answer in answers)
    
    # Znajdź odpowiedni poziom wyników
    matching_level = None
    for level in interpretation['levels']:
        if level['min_score'] <= total_score <= level['max_score']:
            matching_level = level
            break
    
    if not matching_level:
        st.error(f"Nie znaleziono odpowiedniego poziomu dla wyniku: {total_score}")
        return
    
    # Określ kolor na podstawie nazwy poziomu
    color_map = {
        "Bardzo wysoka": "#e53e3e",  # czerwony
        "Wysoka": "#dd6b20",         # pomarańczowy  
        "Średnia": "#3182ce",        # niebieski
        "Niska": "#38a169"           # zielony
    }
    level_color = color_map.get(matching_level['name'], "#3182ce")
    
    # Główny wynik
    relevance_icons = {
        "Bardzo wysoka": "🔥",
        "Wysoka": "⭐", 
        "Średnia": "💡",
        "Niska": "🌱"
    }
    icon = relevance_icons.get(matching_level['name'], "🎯")
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {level_color} 0%, {level_color}CC 100%); 
                padding: 25px; border-radius: 15px; margin: 20px 0; color: white; text-align: center;'>
        <h2 style='margin: 0; color: white;'>{icon} ISTOTNOŚĆ: {matching_level['name'].upper()}</h2>
        <p style='font-size: 1.2rem; margin: 15px 0; opacity: 0.9;'>
            Wynik: <strong>{total_score}/{len(answers) * 4}</strong> punktów
        </p>
        <p style='font-size: 1rem; margin: 0; opacity: 0.8;'>
            Poziom istotności tematyki lekcji dla Twoich potrzeb zawodowych
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Szczegółowa analiza
    st.markdown(f"### {matching_level['title']}")
    st.markdown(matching_level['description'])
    
    # Kluczowe wnioski
    if 'insights' in matching_level and matching_level['insights']:
        st.markdown("#### 💡 Kluczowe wnioski dla Ciebie:")
        for insight in matching_level['insights']:
            st.markdown(f"• {insight}")
    
    # Rekomendacje
    if 'recommendations' in matching_level and matching_level['recommendations']:
        st.markdown("#### 🎯 Konkretne rekomendacje:")
        for i, recommendation in enumerate(matching_level['recommendations'], 1):
            st.markdown(f"{i}. {recommendation}")
    
    # Następne kroki
    if 'next_steps' in matching_level:
        st.markdown("#### 🚀 Twoje następne kroki:")
        st.info(matching_level['next_steps'])


def display_conversational_intelligence_results(answers, questions):
    """Wyświetla spersonalizowane wyniki quizu samodiagnozy dla Conversational Intelligence"""
    
    st.markdown("---")
    st.markdown("## 🎯 Twoje spersonalizowane wyniki")
    
    # Oblicz punkty dla każdej kategorii
    high_relevance_count = sum(1 for answer in answers if answer >= 2)  # odpowiedzi 2 i 3 (indeksy)
    medium_relevance_count = sum(1 for answer in answers if answer == 1)  # odpowiedź 1 (indeks)
    low_relevance_count = sum(1 for answer in answers if answer == 0)  # odpowiedź 0 (indeks)
    
    total_questions = len(questions)
    high_percentage = (high_relevance_count / total_questions) * 100
    
    # Określ poziom relevantności
    if high_percentage >= 75:
        relevance_level = "BARDZO WYSOKA"
        relevance_color = "#d32f2f"
        relevance_icon = "🔥"
    elif high_percentage >= 50:
        relevance_level = "WYSOKA"
        relevance_color = "#f57c00"
        relevance_icon = "⭐"
    elif high_percentage >= 25:
        relevance_level = "ŚREDNIA"
        relevance_color = "#1976d2"
        relevance_icon = "💡"
    else:
        relevance_level = "NISKA"
        relevance_color = "#388e3c"
        relevance_icon = "✅"
    
    # Główny wynik
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {relevance_color} 0%, {relevance_color}CC 100%); 
                padding: 25px; border-radius: 15px; margin: 20px 0; color: white; text-align: center;'>
        <h2 style='margin: 0; color: white;'>{relevance_icon} RELEVANTNOŚĆ: {relevance_level}</h2>
        <p style='font-size: 1.2rem; margin: 15px 0; opacity: 0.9;'>
            Conversational Intelligence ma dla Ciebie <strong>{relevance_level.lower()}</strong> wartość praktyczną
        </p>
        <p style='font-size: 1rem; margin: 0; opacity: 0.8;'>
            {high_relevance_count}/{total_questions} obszarów wskazuje na wysoką potrzebę rozwoju C-IQ
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Szczegółowa analiza na podstawie odpowiedzi
    if high_percentage >= 75:
        st.markdown("""
        ### 🔥 Conversational Intelligence to dla Ciebie GAME CHANGER!
        
        **Twoja diagnoza pokazuje, że:**
        - Borykasz się z wyzwaniami komunikacyjnymi, które wpływają na Twoje cele zawodowe
        - Umiejętności C-IQ mogą być kluczem do przełomu w Twoim przywództwie
        - Inwestycja w rozwój inteligencji konwersacyjnej może przynieść Ci bardzo szybkie i wymierne korzyści
        
        **Priorytetowe obszary rozwoju dla Ciebie:**
        ✅ **Natychmiastowe zastosowanie** - rozpocznij od jednej trudnej rozmowy tygodniowo  
        ✅ **Głębokie studiowanie** - przeanalizuj wszystkie poziomy rozmów w praktyce  
        ✅ **Feedback od zespołu** - poproś o ocenę, jak zmienia się atmosfera rozmów  
        """)
        
    elif high_percentage >= 50:
        st.markdown("""
        ### ⭐ Conversational Intelligence to solidna inwestycja w Twój rozwój
        
        **Twoja diagnoza pokazuje, że:**
        - Masz kilka obszarów, gdzie C-IQ może realnie pomóc
        - Widzisz potencjał w lepszych rozmowach dla osiągnięcia celów
        - Rozwój tych umiejętności może wzmocnić Twoje mocne strony przywódcze
        
        **Rekomendowany plan rozwoju:**
        ✅ **Stopniowe wdrażanie** - wybierz 2-3 techniki C-IQ do praktykowania  
        ✅ **Obserwacja rezultatów** - monitoruj jak zmieniają się Twoje relacje  
        ✅ **Eksperymentowanie** - testuj różne poziomy rozmów w bezpiecznych sytuacjach  
        """)
        
    elif high_percentage >= 25:
        st.markdown("""
        ### 💡 Conversational Intelligence to użyteczne uzupełnienie Twoich umiejętności
        
        **Twoja diagnoza pokazuje, że:**
        - Masz solidne podstawy komunikacyjne
        - C-IQ może pomóc w kilku konkretnych sytuacjach
        - Będzie to raczej rozwijanie istniejących mocnych stron niż radykalna zmiana
        
        **Sugerowane podejście:**
        ✅ **Selektywne uczenie** - skup się na technikach najbardziej przydatnych w Twojej roli  
        ✅ **Praktyczne zastosowanie** - używaj C-IQ w konkretnych, trudnych sytuacjach  
        ✅ **Mentoring innych** - przekazuj te umiejętności członkom zespołu  
        """)
        
    else:
        st.markdown("""
        ### ✅ Masz już solidne fundamenty - C-IQ to opcjonalne wzbogacenie
        
        **Twoja diagnoza pokazuje, że:**
        - Prawdopodobnie już stosujesz wiele zasad C-IQ intuicyjnie
        - Twoje obecne podejście do komunikacji jest skuteczne
        - C-IQ może służyć głównie jako systematyzacja wiedzy, którą już posiadasz
        
        **Zalecenia:**
        ✅ **Świadome stosowanie** - nadaj nazwy temu, co już robisz dobrze  
        ✅ **Dzielenie się wiedzą** - ucz innych skutecznych wzorców komunikacji  
        ✅ **Ciągłe doskonalenie** - stosuj C-IQ w wyjątkowo trudnych sytuacjach  
        """)
    
    # Kluczowe wnioski i następne kroki
    st.markdown("### 🎯 Twoje następne kroki")
    
    # Analizuj konkretne odpowiedzi i daj spersonalizowane wskazówki
    problem_areas = []
    for i, answer in enumerate(answers):
        if answer >= 2:  # Wysokie wskazanie potrzeby
            if i == 0:
                problem_areas.append("**Defensywność rozmówców** - ludzie często się 'zamykają' w rozmowach z Tobą")
            elif i == 1:
                problem_areas.append("**Budowanie zaufania** - Twoje cele zawodowe silnie zależą od jakości relacji")
            elif i == 2:
                problem_areas.append("**Motywowanie zespołu** - tracisz energię na napięcia komunikacyjne")
            elif i == 3:
                problem_areas.append("**Zarządzanie konfliktem** - konflikty eskalują zamiast się konstruktywnie rozwiązywać")
            elif i == 4:
                problem_areas.append("**Konstruktywny feedback** - Twoje uwagi wywołują opór zamiast motywować")
            elif i == 5:
                problem_areas.append("**Współtworzenie** - widzisz potencjał w przejściu od przekonywania do współpracy")
            elif i == 6:
                problem_areas.append("**Kultura zespołu** - chcesz aktywnie wpływać na atmosferę przez rozmowy")
            elif i == 7:
                problem_areas.append("**Filozofia 'mikrozmian'** - inspiruje Cię idea transformacji przez codzienne interakcje")
    
    if problem_areas:
        st.markdown("**Twoje priorytetowe obszary rozwoju:**")
        for area in problem_areas:
            st.markdown(f"• {area}")
    
    # Konkretne rekomendacje akcji
    st.markdown("""
    ### 🚀 Konkretne akcje na najbliższy tydzień:
    
    1. **Jedna świadoma rozmowa dziennie** - wybierz jedną interakcję i zastosuj zasady Poziomu III (ciekawość zamiast oceny)
    2. **Obserwuj neurochemię** - zwracaj uwagę, kiedy widzisz napięcie u rozmówcy i jak możesz je rozładować
    3. **Eksperymentuj z pytaniami** - zamiast mówić "nie", pytaj "jak moglibyśmy to rozwiązać?"
    
    **Pamiętaj:** Według Judith Glaser, każda rozmowa to szansa na mikro-zmianę. Już jedna świadoma interakcja dziennie może zacząć transformować Twoją rzeczywistość zawodową! 💪
    """)
    
    # Dodaj motywujący cytat
    st.markdown("""
    ---
    > *"Dotarcie do następnego poziomu wielkości zależy od jakości kultury, która zależy od jakości relacji, a te – od jakości rozmów."*  
    > **— Judith Glaser**
    """, unsafe_allow_html=True)


def display_quiz_results(quiz_data, question_results, total_points, correct_answers, is_self_diagnostic, quiz_type):
    """Wyświetla szczegółowe wyniki quizu po jego ukończeniu"""
    
    # Statystyki główne
    total_questions = len(question_results)
    
    if not is_self_diagnostic and quiz_type != 'slider':
        # Quiz testowy - pokazuj wynik procentowy
        percentage = (correct_answers / total_questions) * 100
        
        # Określ kolor na podstawie wyniku
        if percentage >= 75:
            color = "#4CAF50"  # zielony
            status_icon = "🎉"
            status_text = "Świetny wynik!"
        elif percentage >= 60:
            color = "#FF9800"  # pomarańczowy
            status_icon = "👍"
            status_text = "Dobry wynik!"
        else:
            color = "#f44336"  # czerwony
            status_icon = "💪"
            status_text = "Możesz lepiej!"
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {color}20 0%, {color}10 100%); 
                    padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 5px solid {color};'>
            <h3 style='color: {color}; margin: 0;'>{status_icon} {status_text}</h3>
            <p style='font-size: 1.2rem; margin: 10px 0; color: #333;'>
                <strong>Wynik: {correct_answers}/{total_questions} ({percentage:.1f}%)</strong>
            </p>
            <p style='margin: 0; color: #666;'>
                Poprawne odpowiedzi: {correct_answers} | Błędne odpowiedzi: {total_questions - correct_answers}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    elif quiz_type == 'slider':
        # Quiz ze sliderami
        max_possible = total_questions * max([q.get('max_value', 5) for q in quiz_data.get('questions', [])])
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #2196F320 0%, #2196F310 100%); 
                    padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 5px solid #2196F3;'>
            <h3 style='color: #2196F3; margin: 0;'>📈 Łączna suma punktów</h3>
            <p style='font-size: 1.2rem; margin: 10px 0; color: #333;'>
                <strong>{total_points}/{max_possible} punktów</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Quiz autodiagnozy - przejdź bezpośrednio do szczegółów odpowiedzi
        pass
    
    # Szczegółowa analiza pytań
    if not is_self_diagnostic:
        st.markdown("### 📝 Analiza odpowiedzi na poszczególne pytania")
        
        for i, result in enumerate(question_results):
            with st.expander(f"Pytanie {i+1}: {result['question'][:60]}..." if len(result['question']) > 60 else f"Pytanie {i+1}: {result['question']}", expanded=False):
                
                # Wyświetl pytanie
                st.markdown(f"**Pytanie:** {result['question']}")
                
                # Wyświetl odpowiedź użytkownika
                question_data = quiz_data['questions'][i]
                user_answer = result['user_answer']
                
                if isinstance(user_answer, list):
                    # Multiple choice
                    user_answer_text = ", ".join([question_data['options'][idx] for idx in user_answer])
                    st.markdown(f"**Twoja odpowiedź:** {user_answer_text}")
                    
                    # Pokaż poprawne odpowiedzi
                    if 'correct_answers' in result:
                        correct_text = ", ".join([question_data['options'][idx] for idx in result['correct_answers']])
                        st.markdown(f"**Poprawne odpowiedzi:** {correct_text}")
                else:
                    # Single choice
                    if user_answer is not None and user_answer < len(question_data.get('options', [])):
                        user_answer_text = question_data['options'][user_answer]
                        st.markdown(f"**Twoja odpowiedź:** {user_answer_text}")
                        
                        # Pokaż poprawną odpowiedź
                        if 'correct_answer' in result and result['correct_answer'] is not None:
                            correct_text = question_data['options'][result['correct_answer']]
                            st.markdown(f"**Poprawna odpowiedź:** {correct_text}")
                
                # Status odpowiedzi
                if result['is_correct']:
                    st.success("✅ Odpowiedź poprawna!")
                else:
                    st.error("❌ Odpowiedź niepoprawna")
                    
                    # Dodaj wyjaśnienie, jeśli jest dostępne
                    if 'explanation' in question_data:
                        st.info(f"💡 **Wyjaśnienie:** {question_data['explanation']}")
    
    else:
        # Dla quizów autodiagnozy - pokaż podsumowanie odpowiedzi i spersonalizowane wyniki
        st.markdown("### 🔍 Twoje odpowiedzi")
        
        with st.expander("Zobacz szczegóły swoich odpowiedzi", expanded=False):
            # Podstawowe szczegóły odpowiedzi
            for i, result in enumerate(question_results):
                st.markdown(f"**Pytanie {i+1}:** {result['question']}")
                
                question_data = quiz_data['questions'][i]
                user_answer = result['user_answer']
                
                if isinstance(user_answer, list):
                    # Multiple choice
                    user_answer_text = ", ".join([question_data['options'][idx] for idx in user_answer])
                    st.markdown(f"**Odpowiedź:** {user_answer_text} ({result['points_earned']} pkt)")
                else:
                    # Single choice
                    if user_answer is not None and user_answer < len(question_data.get('options', [])):
                        user_answer_text = question_data['options'][user_answer]
                        st.markdown(f"**Odpowiedź:** {user_answer_text} ({result['points_earned']} pkt)")
                
                st.markdown("---")
            
            # Sprawdź czy to quiz Conversational Intelligence - spersonalizowane wyniki są już wyświetlane wcześniej
            # więc tutaj je pomijamy
            pass
    
    # Wskazówki i następne kroki
    if not is_self_diagnostic:
        if correct_answers == total_questions:
            st.balloons()
            st.markdown("""
            ### 🎉 Gratulacje!
            Uzyskałeś/aś maksymalny wynik! Doskonale opanowałeś/aś materiał z tej lekcji.
            """)
        elif correct_answers / total_questions >= 0.75:
            st.markdown("""
            ### 👏 Bardzo dobry wynik!
            Świetnie radzisz sobie z materiałem. Może warto przejrzeć pytania, na które odpowiedziałeś/aś niepoprawnie.
            """)
        elif correct_answers / total_questions >= 0.5:
            st.markdown("""
            ### 📚 Dobra robota!
            Masz solidne podstawy, ale warto jeszcze raz przejrzeć materiał lekcji, szczególnie tematy z pytań, na które odpowiedziałeś/aś niepoprawnie.
            """)
        else:
            st.markdown("""
            ### 💪 Czas na powtórkę!
            Warto wrócić do materiału lekcji i przejrzeć go jeszcze raz. Nie martw się - uczenie się to proces!
            """)
    
    # Wskazówka o ponownym przystąpieniu
    st.markdown("---")
    st.markdown("💡 **Wskazówka:** Możesz przystąpić do quizu ponownie, klikając przycisk '🔄 Przystąp ponownie' powyżej.")
