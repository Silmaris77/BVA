import streamlit as st
from datetime import datetime
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
    """Konwertuje poziom trudno�ci (liczba lub tekst) na odpowiedni� liczb� gwiazdek."""
    difficulty_map = {
        "beginner": 1,
        "podstawowy": 1,
        "intermediate": 2,
        "�redni": 2,
        "�redniozaawansowany": 3,
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
    
    return '?' * difficulty_level

def show_lesson():
    """Show lesson view with tabs for lessons and course structure"""
    
    # Przewi� na g�r� strony
    scroll_to_top()
    
    # Sprawd� czy zosta� za��dany reset stanu lekcji przez klikni�cie "Lekcje" w nawigacji
    if st.session_state.get('lesson_reset_requested', False):
        # Reset lekcji za��dany - wyczy�� stan
        st.session_state.current_lesson = None
        if 'lesson_finished' in st.session_state:
            st.session_state.lesson_finished = False
        # Usu� flag� resetu po jednorazowym u�yciu
        st.session_state.lesson_reset_requested = False
    
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urz�dzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urz�dzenia
    device_type = get_device_type()
    
    zen_header("Lekcje")
    
    # Wy�wietl informacje o kompatybilno�ci w trybie dev
    display_compatibility_info()
    
    # Create main tabs with compatibility fallback
    tab1 = st.container()  # U�ywamy tylko jednego kontenera zamiast tab�w
    
    with tab1:
        show_lessons_content()
    
    # with tab2:
    #     show_skill_tree()

def show_lessons_by_category(lessons_by_category, completed_lessons, device_type, accessible=True):
    """Helper function to show lessons grouped by category"""
    for category, category_lessons in lessons_by_category.items():
        # Utw�rz kolumny dla responsywnego uk�adu
        # Na urz�dzeniach mobilnych - 1 kolumna, na desktopie - 2 kolumny
        if device_type == 'mobile':
            columns = st.columns(1)
        else:
            columns = st.columns(1)
        
        # Wy�wietlaj lekcje w kolumnach
        for i, (lesson_id, lesson) in enumerate(category_lessons):
            # Sprawd�, czy lekcja jest uko�czona
            is_completed = lesson_id in completed_lessons
            
            # Wybierz kolumn� (naprzemiennie dla 2 kolumn, zawsze pierwsza dla 1 kolumny)
            column_index = i % len(columns)
            
            with columns[column_index]:
                if accessible:
                    # Lekcja dost�pna - normalne wy�wietlanie
                    lesson_card(
                        title=lesson.get('title', 'Lekcja'),
                        description=lesson.get('description', 'Ta lekcja wprowadza podstawowe zasady...'),
                        xp=lesson.get('xp_reward', 30),
                        difficulty=lesson.get('difficulty', 'beginner'),
                        category=lesson.get('tag', category),
                        completed=is_completed,
                        button_text="Powt�rz lekcj�" if is_completed else "Rozpocznij",
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
                    # Lekcja niedost�pna - u�yj lesson_card z odpowiednimi parametrami
                    lesson_card(
                        title=f"?? {lesson.get('title', 'Lekcja')}",
                        description=lesson.get('description', 'Ta lekcja wprowadza podstawowe zasady...'),
                        xp=lesson.get('xp_reward', 30),
                        difficulty=lesson.get('difficulty', 'beginner'),
                        category=lesson.get('tag', category),
                        completed=False,
                        accessible=False,  # Niedost�pna lekcja
                        lesson_id=lesson_id
                    )

def show_lessons_content():
    """Show the lessons content with tabs for available and unavailable lessons"""
    # Pobierz aktualny typ urz�dzenia
    device_type = get_device_type()
    
    lessons = load_lessons()
    
    # Check if we're viewing a specific lesson or the overview
    if 'current_lesson' not in st.session_state or not st.session_state.current_lesson:
        # WIDOK PRZEGL�DU LEKCJI
        # Pobierz dane u�ytkownika dla oznaczenia uko�czonych lekcji
        from data.users import get_current_user_data
        user_data = get_current_user_data(st.session_state.username)
        completed_lessons = user_data.get('completed_lessons', [])
        
        # Sprawd� dost�pno�� lekcji dla u�ytkownika
        username = st.session_state.get('username')
        
        # Podziel lekcje na dost�pne i niedost�pne
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
        
        # Sortuj lekcje w ka�dej kategorii: nieuko�czone najpierw, potem uko�czone
        for category in available_lessons:
            available_lessons[category].sort(key=lambda x: (x[0] in completed_lessons, x[0]))
        
        for category in unavailable_lessons:
            unavailable_lessons[category].sort(key=lambda x: (x[0] in completed_lessons, x[0]))
        
        # Utw�rz tabs dla dost�pnych i niedost�pnych lekcji
        tab_available, tab_unavailable = st.tabs(["?? Lekcje dost�pne", "?? Lekcje niedost�pne"])
        
        with tab_available:
            scroll_to_top()
            st.markdown("### Dost�pne lekcje")
            if available_lessons:
                show_lessons_by_category(available_lessons, completed_lessons, device_type, accessible=True)
            else:
                st.info("Brak dost�pnych lekcji.")
        
        with tab_unavailable:
            scroll_to_top()
            st.markdown("### Niedost�pne lekcje")
            if unavailable_lessons:
                show_lessons_by_category(unavailable_lessons, completed_lessons, device_type, accessible=False)
            else:
                st.info("Wszystkie lekcje s� dost�pne!")

    else:
        # Kod wy�wietlania pojedynczej lekcji
        lessons = load_lessons()  # Dodaj ponowne �adowanie lekcji  
        lesson_id = st.session_state.current_lesson
        if lesson_id not in lessons:
            # Automatycznie wyczy�� nieprawid�owe ID lekcji i wr�� do listy
            st.session_state.current_lesson = None
            st.rerun()
            return
        
        lesson = lessons[lesson_id]

        # Sprawd� dost�pno�� lekcji
        username = st.session_state.get('username')
        if username and not is_lesson_accessible(username, lesson_id):
            st.error("?? **Dost�p do tej lekcji jest ograniczony**")
            st.warning("Ta lekcja nie jest obecnie dost�pna dla Twojego konta. Skontaktuj si� z administratorem, aby uzyska� dost�p.")
            
            # Przycisk powrotu do listy lekcji
            if st.button("?? Wr�� do listy lekcji"):
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
            }# Oblicz ca�kowit� liczb� dost�pnych krok�w w tej lekcji
        available_steps = ['intro', 'content', 'summary']
        if 'sections' in lesson:
            # Usuni�to opening_quiz i closing_quiz z osobnych krok�w - s� teraz zintegrowane w zak�adkach
            if 'practical_exercises' in lesson.get('sections', {}):
                available_steps.append('practical_exercises')
            elif 'reflection' in lesson.get('sections', {}) or 'application' in lesson.get('sections', {}):
                # Backward compatibility dla starszych lekcji
                if 'reflection' in lesson.get('sections', {}):
                    available_steps.append('reflection')
                if 'application' in lesson.get('sections', {}):
                    available_steps.append('application')
          # Ustal kolejno�� krok�w (bez opening_quiz i closing_quiz jako osobnych krok�w)
        step_order = ['intro']
        step_order.extend(['content'])
        
        # Nowa sekcja �wicze� praktycznych zamiast osobnych reflection i application
        # closing_quiz jest teraz zintegrowany w sekcji practical_exercises
        if 'practical_exercises' in available_steps:
            step_order.append('practical_exercises')
        elif 'reflection' in available_steps or 'application' in available_steps:
            # Backward compatibility dla starszych lekcji
            if 'reflection' in available_steps:
                step_order.append('reflection')
            if 'application' in available_steps:
                step_order.append('application')
        
        # closing_quiz usuni�ty jako osobny krok - jest teraz w zak�adce practical_exercises
        step_order.append('summary')
        
        total_steps = len(step_order)
        base_xp = lesson.get('xp_reward', 100)        # Mapowanie krok�w do nazw wy�wietlanych (usuni�to opening_quiz i closing_quiz)
        step_names = {
            'intro': 'Wprowadzenie',
            'content': 'Nauka',
            'practical_exercises': 'Praktyka',
            'reflection': 'Refleksja',  # backward compatibility
            'application': 'Zadania praktyczne',  # backward compatibility
            'summary': 'Podsumowanie'
        }
        
        # Specjalne nazwy dla lekcji "Wprowadzenie do neuroprzyw�dztwa"
        if lesson.get('title') == 'Wprowadzenie do neuroprzyw�dztwa':
            step_names = {
                'intro': 'Wprowadzenie',
                'content': 'Case Study',
                'practical_exercises': 'O CO TU CHODZI',
                'reflection': 'Refleksja',  # backward compatibility
                'application': 'Zadania praktyczne',  # backward compatibility
                'summary': 'AUTODIAGNOZA'
            }# Mapowanie krok�w do warto�ci XP (usuni�to opening_quiz i closing_quiz)
        step_xp_values = {
            'intro': int(base_xp * 0.05),          # 5% ca�kowitego XP
            'content': int(base_xp * 0.30),        # 30% ca�kowitego XP (Merytoryka)
            'practical_exercises': int(base_xp * 0.60),  # 60% ca�kowitego XP (nowa po��czona sekcja z quizem ko�cowym)
            'reflection': int(base_xp * 0.20),     # 20% ca�kowitego XP (backward compatibility)
            'application': int(base_xp * 0.20),    # 20% ca�kowitego XP (backward compatibility)
            'summary': int(base_xp * 0.05)         # 5% ca�kowitego XP
        }
        
        # Oblicz rzeczywiste maksimum XP jako sum� wszystkich dost�pnych krok�w
        max_xp = sum(step_xp_values[step] for step in step_order)
          # Znajd� indeks obecnego kroku i nast�pnego kroku
        current_step_idx = step_order.index(st.session_state.lesson_step) if st.session_state.lesson_step in step_order else 0
        next_step_idx = min(current_step_idx + 1, len(step_order) - 1)
        next_step = step_order[next_step_idx]
        
        # Style dla paska post�pu i interfejsu
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
        }          /* Przyciski "Dalej" o szeroko�ci odpowiadaj�cej przyciskom nawigacji poziomej */
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
        
        /* Zapewnij, �e kontener przycisku ma odpowiedni� szeroko�� */
        .next-button .stButton {
            width: 280px !important;
            max-width: 280px !important;
            margin: 0 auto !important;
            display: block !important;
        }
        
        /* Wymu� szeroko�� na elemencie div zawieraj�cym przycisk */
        .next-button > div {
            width: 280px !important;
            max-width: 280px !important;
            margin: 0 auto !important;
        }
        
        /* Dodatkowe wymuszenie dla wszystkich element�w w kontenerze */
        .next-button * {
            max-width: 280px !important;
        }
        
        /* Style dla expander�w */
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

        /* Specjalne style dla urz�dze� mobilnych */
        @media (max-width: 768px) {
            /* Zwi�ksz szeroko�� g��wnego kontenera */
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
            
            /* Zwi�ksz line-height i zmniejsz font-size dla lepszej czytelno�ci */
            .st-emotion-cache-16idsys p, .stMarkdown p {
                font-size: 0.9rem !important;
                line-height: 1.8 !important;
                margin-bottom: 1rem !important;
            }
            
            /* Specjalne style dla tre�ci w gradientowych divach */
            div[style*="linear-gradient"] {
                margin-left: -10px !important;
                margin-right: -10px !important;
                padding-left: 15px !important;
                padding-right: 15px !important;
            }
            
            /* Zmniejsz padding dla zagnie�d�onych kontener�w */
            div[style*="padding: 25px"] {
                padding: 15px 10px !important;
            }
            
            /* Zwi�ksz szeroko�� tabs na mobile */
            .stTabs [data-baseweb="tab-list"] {
                flex-wrap: nowrap !important;
                overflow-x: auto !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                min-width: auto !important;
                padding: 8px 12px !important;
                font-size: 0.85rem !important;
            }
            
            /* Wi�kszy obszar klikalny dla expander�w */
            .st-expander {
                margin-bottom: 12px;
            }
            
            .st-expander .st-emotion-cache-16idsys p {
                font-size: 0.9rem !important; /* Nieco mniejsza czcionka na ma�ych ekranach */
                line-height: 1.7 !important;
            }
            
            /* Zwi�kszony obszar klikni�cia dla nag��wka expandera */
            .st-expander-header {
                padding: 15px 10px !important;
                font-size: 1.1rem !important;
                font-weight: 600 !important;
                min-height: 50px;
            }
            
            /* Dodaj wska�nik rozwijania */
            .st-expander:not(.st-emotion-cache-xujm5h) .st-expander-header::after {
                content: '�';
                float: right;
                margin-left: 10px;
                transition: transform 0.3s;
            }
            
            .st-expander.st-emotion-cache-xujm5h .st-expander-header::after {
                content: '^';
                float: right;
                margin-left: 10px;
            }        }        </style>
        """, unsafe_allow_html=True)        # Sidebar pozostaje pusty - nawigacja przeniesiona na g��wn� stron�
        with st.sidebar:
            pass

        # Nawigacja pozioma na g��wnej stronie
        def show_horizontal_lesson_navigation():
            """Wy�wietla poziom� nawigacj� lekcji na g��wnej stronie"""
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
            }            /* Zapewnij jednakow� szeroko�� przycisk�w nawigacji lekcji - 280px jak przycisk "Dalej" */
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
            st.markdown('<div class="lesson-nav-title">?? Nawigacja lekcji</div>', unsafe_allow_html=True)
            
            # Stw�rz kolumny dla przycisk�w nawigacji z responsive grid
            available_steps_in_order = [step for step in step_order if step in available_steps]
            
            # U�yj responsive grid: 2 kolumny na desktop i tablet, 1 na mobile
            device_type = get_device_type()
            if device_type == 'mobile':
                cols_per_row = 1
            else:  # desktop i tablet
                cols_per_row = 2
            
            # Podziel przyciski na wiersze
            rows = []
            for i in range(0, len(available_steps_in_order), cols_per_row):
                rows.append(available_steps_in_order[i:i + cols_per_row])
            
            # Wy�wietl ka�dy wiersz osobno
            for row_steps in rows:
                cols = st.columns(cols_per_row)
                for col_index, step in enumerate(row_steps):
                    if col_index < len(cols):  # Sprawd� czy kolumna istnieje
                        with cols[col_index]:
                            step_name = step_names.get(step, step.capitalize())
                            step_number = step_order.index(step) + 1  # Numer kroku w oryginalnej kolejno�ci
                            
                            # Sprawd� status kroku
                            is_completed = st.session_state.lesson_progress.get(step, False)
                            is_current = (step == st.session_state.lesson_step)
                            
                            # Specjalna logika dla sekcji "Podsumowanie" - wymaga zaliczenia quizu ko�cowego
                            if step == 'summary':
                                # Sprawd� czy quiz ko�cowy zosta� zdany z minimum 75%
                                lesson_title = lesson.get("title", "")
                                closing_quiz_key = f"closing_quiz_{lesson_id}"
                                closing_quiz_state = st.session_state.get(closing_quiz_key, {})
                                quiz_passed = closing_quiz_state.get("quiz_passed", False)
                                
                                # Dla lekcji "Wprowadzenie do neuroprzyw�dztwa" nie ma blokowania
                                if lesson_title != "Wprowadzenie do neuroprzyw�dztwa" and not quiz_passed and not is_current:
                                    # Blokuj dost�p do podsumowania je�li quiz nie zosta� zdany
                                    button_text = f"?? {step_number}. {step_name}"
                                    button_type = "secondary"
                                    disabled = True
                                    help_text = "Musisz zaliczy� quiz ko�cowy (min. 75%) w sekcji 'Praktyka', aby odblokowa� podsumowanie"
                                elif is_current:
                                    button_text = f"?? {step_number}. {step_name}"
                                    button_type = "primary"
                                    disabled = False
                                    help_text = f"Przejd� do: {step_name}"
                                elif is_completed:
                                    button_text = f"? {step_number}. {step_name}"
                                    button_type = "secondary"
                                    disabled = False
                                    help_text = f"Przejd� do: {step_name}"
                                else:
                                    button_text = f"{step_number}. {step_name}"
                                    button_type = "secondary"
                                    disabled = True
                                    help_text = f"Uko�cz poprzednie kroki aby odblokowa�: {step_name}"
                            else:
                                # Standardowa logika dla innych krok�w
                                if is_current:
                                    # Aktualny krok - niebieski
                                    button_text = f"?? {step_number}. {step_name}"
                                    button_type = "primary"
                                    disabled = False
                                    help_text = f"Przejd� do: {step_name}"
                                elif is_completed:
                                    # Uko�czony krok - zielony z checkmarkiem
                                    button_text = f"? {step_number}. {step_name}"
                                    button_type = "secondary"
                                    disabled = False
                                    help_text = f"Przejd� do: {step_name}"
                                else:
                                    # Przysz�y krok - szary, zablokowany
                                    button_text = f"{step_number}. {step_name}"
                                    button_type = "secondary"
                                    disabled = True
                                    help_text = f"Uko�cz poprzednie kroki aby odblokowa�: {step_name}"
                            
                            # Wy�wietl przycisk
                            if st.button(
                                button_text, 
                                key=f"nav_step_{step}_{col_index}", 
                                type=button_type,
                                disabled=disabled,
                                width='stretch',
                                help=help_text
                            ):
                                if not is_current:  # Tylko je�li nie jest to aktualny krok
                                    st.session_state.lesson_step = step
                                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Wy�wietl poziom� nawigacj�
        show_horizontal_lesson_navigation()

        # Main content
        st.markdown("<div class='st-bx'>", unsafe_allow_html=True)# Nag��wek sekcji
        current_section_title = step_names.get(st.session_state.lesson_step, st.session_state.lesson_step.capitalize())
        st.markdown(f"<h1>{current_section_title}</h1>", unsafe_allow_html=True)
          # Main content logic for each step
        if st.session_state.lesson_step == 'intro':
            # Sprawd� tytu� lekcji, aby ukry� niekt�re tabs dla konkretnych lekcji
            lesson_title = lesson.get("title", "")
            
            if lesson_title == "Wprowadzenie do neuroprzyw�dztwa":
                # Dla tej lekcji pokazuj tylko zak�adk� "Wprowadzenie"
                intro_tabs = tabs_with_fallback(["Wprowadzenie"])
                
                with intro_tabs[0]:
                    # Wy�wietl g��wne wprowadzenie
                    if isinstance(lesson.get("intro"), dict) and "main" in lesson["intro"]:
                        st.markdown(lesson["intro"]["main"], unsafe_allow_html=True)
                    elif isinstance(lesson.get("intro"), str):
                        st.markdown(lesson["intro"], unsafe_allow_html=True)
                    else:
                        st.warning("Brak tre�ci wprowadzenia.")
            else:
                # Dla wszystkich innych lekcji pokazuj pe�ne tabs
                intro_tabs = tabs_with_fallback(["Wprowadzenie", "Case Study", "?? Quiz Samodiagnozy"])
                
                with intro_tabs[0]:
                    # Wy�wietl g��wne wprowadzenie
                    if isinstance(lesson.get("intro"), dict) and "main" in lesson["intro"]:
                        st.markdown(lesson["intro"]["main"], unsafe_allow_html=True)
                    elif isinstance(lesson.get("intro"), str):
                        st.markdown(lesson["intro"], unsafe_allow_html=True)
                    else:
                        st.warning("Brak tre�ci wprowadzenia.")
            
                with intro_tabs[1]:
                    # Wy�wietl studium przypadku
                    if isinstance(lesson.get("intro"), dict) and "case_study" in lesson["intro"]:
                        st.markdown(lesson["intro"]["case_study"], unsafe_allow_html=True)
                    else:
                        st.warning("Brak studium przypadku w tej lekcji.")
            
                with intro_tabs[2]:
                    # Wy�wietl quiz samodiagnozy
                    if (isinstance(lesson.get("intro"), dict) and 
                        "quiz_samodiagnozy" in lesson["intro"] and 
                        "questions" in lesson["intro"]["quiz_samodiagnozy"]):
                        
                        st.info("?? **Quiz Samodiagnozy** - Ten quiz pomaga Ci lepiej pozna� siebie jako lidera. Nie ma tu dobrych ani z�ych odpowiedzi - chodzi o szczer� autorefleksj�. Twoje odpowiedzi nie wp�ywaj� na post�p w lekcji.")
                        
                        quiz_data = lesson["intro"]["quiz_samodiagnozy"]
                        quiz_complete, _, earned_points = display_quiz(quiz_data)
                        # Oznacz quiz jako uko�czony po wype�nieniu
                        if quiz_complete:
                            quiz_xp_key = f"opening_quiz_xp_{lesson_id}"
                            if not st.session_state.get(quiz_xp_key, False):
                                # Award fragment XP for quiz participation
                                fragment_xp = get_fragment_xp_breakdown(lesson.get('xp_reward', 30))
                                success, earned_xp = award_fragment_xp(lesson_id, 'intro_quiz', fragment_xp['intro'] // 3)  # 1/3 of intro XP
                                st.session_state[quiz_xp_key] = True
                                if success and earned_xp > 0:
                                    show_xp_notification(earned_xp, "za szczer� samorefleksj�")
                        
                            st.success("? Dzi�kujemy za szczer� samorefleksj�!")
                    
                    elif 'sections' in lesson and 'opening_quiz' in lesson.get('sections', {}):
                        # Backward compatibility - stary format
                        st.info("?? **Quiz Samodiagnozy** - Ten quiz pomaga Ci lepiej pozna� siebie jako inwestora. Nie ma tu dobrych ani z�ych odpowiedzi - chodzi o szczer� autorefleksj�. Twoje odpowiedzi nie wp�ywaj� na post�p w lekcji.")
                        
                        quiz_data = lesson['sections']['opening_quiz']
                        quiz_complete, _, earned_points = display_quiz(quiz_data)
                        # Oznacz quiz jako uko�czony po wype�nieniu
                        if quiz_complete:
                            quiz_xp_key = f"opening_quiz_xp_{lesson_id}"
                            if not st.session_state.get(quiz_xp_key, False):
                                # Award fragment XP for quiz participation
                                fragment_xp = get_fragment_xp_breakdown(lesson.get('xp_reward', 30))
                                success, earned_xp = award_fragment_xp(lesson_id, 'intro_quiz', fragment_xp['intro'] // 3)  # 1/3 of intro XP
                                st.session_state[quiz_xp_key] = True
                                if success and earned_xp > 0:
                                    show_xp_notification(earned_xp, "za szczer� samorefleksj�")
                            
                            st.success("? Dzi�kujemy za szczer� samorefleksj�!")
                            
                            # Dodaj przycisk do ponownego przyst�pienia do quizu samodiagnozy
                            st.markdown("---")
                            col1, col2, col3 = st.columns([1, 1, 1])
                            with col2:
                                if st.button("?? Przyst�p ponownie", key=f"retry_self_diagnosis_legacy_{lesson_id}", help="Mo�esz ponownie wype�ni� quiz samodiagnozy aby zaktualizowa� swoj� autorefleksj�", width='stretch'):
                                    # Reset stanu quizu samodiagnozy
                                    quiz_id = f"quiz_{quiz_data.get('title', '').replace(' ', '_').lower()}"
                                    
                                    # Usu� stan g��wny quizu
                                    if quiz_id in st.session_state:
                                        del st.session_state[quiz_id]
                                    
                                    # Usu� wszystkie odpowiedzi na pytania
                                    for i in range(len(quiz_data.get('questions', []))):
                                        question_key = f"{quiz_id}_q{i}_selected"
                                        if question_key in st.session_state:
                                            del st.session_state[question_key]
                                        
                                        # Usu� tak�e klucze suwak�w je�li istniej�
                                        slider_key = f"{quiz_id}_q{i}_slider"
                                        if slider_key in st.session_state:
                                            del st.session_state[slider_key]
                                    
                                    st.rerun()
                    
                    else:
                        st.info("Ten quiz samodiagnozy nie jest dost�pny dla tej lekcji.")
                        
            # Przycisk "Dalej" po wprowadzeniu            
            # U�yj kolumn aby ograniczy� szeroko�� przycisku
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
                        show_xp_notification(xp_awarded, f"Zdoby�e� {xp_awarded} XP za uko�czenie wprowadzenia!")
                        
                        # Refresh user data for real-time updates
                        from utils.real_time_updates import refresh_user_data
                        refresh_user_data()
                        
                        # Sprawd� czy lekcja zosta�a uko�czona
                        check_and_mark_lesson_completion(lesson_id)
                    
                    # Przejd� do nast�pnego kroku
                    st.session_state.lesson_step = next_step
                    scroll_to_top()
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        elif st.session_state.lesson_step == 'content':
            # Sprawd� struktur� learning - obs�uguj zar�wno tabs jak i sections
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'learning' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'learning'!")
            else:
                learning_data = lesson['sections']['learning']
                
                # Nowa struktura z tabs (jak w lekcji 11)
                if 'tabs' in learning_data:
                    st.markdown("### ?? Materia� do nauki")
                    
                    # CSS dla pe�nej szeroko�ci expander�w w tabsie "Tekst"
                    st.markdown("""
                        <style>
                        /* Expander w tabsie "Tekst" wype�nia ca�� szeroko�� */
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
                        
                        /* Zawarto�� expandera r�wnie� pe�na szeroko�� */
                        div[data-testid="stExpander"] .streamlit-expanderContent {
                            width: 100% !important;
                            padding: 0 !important;
                            margin: 0 !important;
                        }
                        
                        /* Nag��wek expandera pe�na szeroko�� */
                        div[data-testid="stExpander"] .streamlit-expanderHeader {
                            width: 100% !important;
                            margin: 0 !important;
                        }
                        
                        /* Karty wewn�trz expandera maj� idealnie dopasowan� szeroko�� */
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown,
                        div[data-testid="stExpander"] .streamlit-expanderContent div[data-testid="column"],
                        div[data-testid="stExpander"] .streamlit-expanderContent div[data-testid="stVerticalBlock"],
                        div[data-testid="stExpander"] .streamlit-expanderContent > div {
                            width: 100% !important;
                            margin: 0 !important;
                            padding: 0 !important;
                            box-sizing: border-box !important;
                        }
                        
                        /* Wszystkie elementy wewn�trz expandera */
                        div[data-testid="stExpander"] .streamlit-expanderContent * {
                            max-width: 100% !important;
                            box-sizing: border-box !important;
                        }
                        
                        /* Konkretnie dla kart z tre�ci� */
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown > div,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown > div > div {
                            width: 100% !important;
                            margin: 0 !important;
                            padding: 1rem !important;
                            border-radius: 8px !important;
                            box-sizing: border-box !important;
                        }
                        
                        /* Wi�ksza czcionka dla tekst�w (nie tytu��w) w expanderach */
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown p,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown li,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown div:not(h1):not(h2):not(h3):not(h4):not(h5):not(h6) {
                            font-size: 1.5rem !important;
                            line-height: 1.6 !important;
                        }
                        
                        /* Bardziej specyficzne selektory dla tekst�w w kartach */
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown > div p,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown > div > div p,
                        div[data-testid="stExpander"] .streamlit-expanderContent .element-container p,
                        div[data-testid="stExpander"] .streamlit-expanderContent [data-testid="stMarkdownContainer"] p {
                            font-size: 1.5rem !important;
                            line-height: 1.6 !important;
                        }
                        
                        /* Uniwersalny selektor dla wszystkich tekst�w w expanderach (opr�cz nag��wk�w) */
                        div[data-testid="stExpander"] .streamlit-expanderContent {
                            font-size: 1.5rem !important;
                            line-height: 1.6 !important;
                        }
                        
                        /* Zachowanie normalnego rozmiaru dla tytu��w */
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h1,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h2,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h3,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h4,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h5,
                        div[data-testid="stExpander"] .streamlit-expanderContent .stMarkdown h6 {
                            font-size: inherit !important;
                        }
                        
                        /* Responsywno�� na urz�dzeniach mobilnych */
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
                    
                    # Utw�rz tabs dla r�nych typ�w tre�ci
                    tab_names = [tab.get('title', f'Tab {i+1}') for i, tab in enumerate(learning_data['tabs'])]
                    tabs = st.tabs(tab_names)
                    
                    for i, (tab_container, tab_data) in enumerate(zip(tabs, learning_data['tabs'])):
                        with tab_container:
                            # Wy�wietl sekcje w tym tab
                            if 'sections' in tab_data:
                                tab_title = tab_data.get('title', '')
                                
                                # Dla tab "Tekst" u�ywaj expander�w
                                if 'Tekst' in tab_title:
                                    for j, section in enumerate(tab_data['sections']):
                                        section_title = section.get('title', f'Sekcja {j+1}')
                                        # Pierwszy expander domy�lnie otwarty
                                        is_expanded = (j == 0)
                                        
                                        with st.expander(section_title, expanded=is_expanded):
                                            # U�yj nowego renderera obs�uguj�cego osadzone media
                                            content = section.get('content', 'Brak tre�ci')
                                            render_embedded_content(content, section)
                                else:
                                    # Dla pozosta�ych tabs (Podcast, Video) standardowe wy�wietlanie
                                    for section in tab_data['sections']:
                                        if 'title' in section:
                                            st.markdown(f"### {section['title']}")
                                        
                                        # U�yj nowego renderera obs�uguj�cego osadzone media
                                        content = section.get('content', 'Brak tre�ci')
                                        render_embedded_content(content, section)
                            else:
                                st.warning(f"Tab '{tab_data.get('title', 'Bez nazwy')}' nie zawiera sekcji.")
                
                # Stara struktura z sections (kompatybilno�� wsteczna)
                elif 'sections' in learning_data:
                    # Sprawd�, czy sekcja learning istnieje i czy zawiera sections
                    for i, section in enumerate(learning_data["sections"]):
                        # Dla lekcji "Wprowadzenie do neuroprzyw�dztwa" pierwszy expander jest otwarty
                        is_expanded = False
                        if lesson.get('title') == 'Wprowadzenie do neuroprzyw�dztwa' and i == 0:
                            is_expanded = True
                        
                        with st.expander(section.get("title", f"Sekcja {i+1}"), expanded=is_expanded):
                            # Wy�wietl tre�� sekcji u�ywaj�c nowego renderera
                            content = section.get("content", "Brak tre�ci")
                            render_embedded_content(content, section)
                            
                            # Sprawd� czy sekcja zawiera film YouTube (pojedynczy)
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
                            
                            # Sprawd� czy sekcja zawiera wiele film�w YouTube (videos)
                            if 'videos' in section and section['videos']:
                                st.markdown("### ?? Materia�y wideo")
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
                                        
                                        # Dodaj separator mi�dzy filmami
                                        if j < len(section['videos']) - 1:
                                            st.markdown("---")
                else:
                    st.error("Sekcja 'learning' nie zawiera ani 'tabs' ani 'sections'!")
                                            # Przycisk "Dalej" po tre�ci lekcji
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
                        show_xp_notification(xp_awarded, f"Zdoby�e� {xp_awarded} XP za zapoznanie si� z materia�em!")
                        
                        # Refresh user data for real-time updates
                        from utils.real_time_updates import refresh_user_data
                        refresh_user_data()
                        
                        # Sprawd� czy lekcja zosta�a uko�czona
                        check_and_mark_lesson_completion(lesson_id)
                    
                    # Przejd� do nast�pnego kroku
                    st.session_state.lesson_step = next_step
                    scroll_to_top()
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.lesson_step == 'practical_exercises':
            # Sekcja �wicze� praktycznych - dla lekcji "Wprowadzenie do neuroprzyw�dztwa" specjalna obs�uga
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'practical_exercises' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'practical_exercises'!")
            else:
                practical_data = lesson['sections']['practical_exercises']
                lesson_title = lesson.get("title", "")
                
                # Specjalna obs�uga dla lekcji "Wprowadzenie do neuroprzyw�dztwa"
                if lesson_title == "Wprowadzenie do neuroprzyw�dztwa" and 'case_study_analysis' in practical_data:
                    case_study_data = practical_data['case_study_analysis']
                    
                    # Wy�wietl tytu� i opis
                    st.markdown(f"### {case_study_data['title']}")
                    st.markdown(case_study_data['description'])
                    st.markdown("---")
                    
                    # Wy�wietl ka�d� cz�� case study
                    for part in case_study_data['parts']:
                        with st.expander(f"**Cz�� {part['id']}: {part['title']}**", expanded=False):
                            # Pole tekstowe z case content
                            st.markdown("#### ?? Opis sytuacji")
                            st.markdown(f"<div style='background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #007bff; margin: 15px 0;'>{part['case_content']}</div>", unsafe_allow_html=True)
                            
                            # Film omawiaj�cy t� cz��
                            st.markdown("#### ?? Analiza neurobiologiczna")
                            
                            # Wy�wietl video je�li URL nie jest placeholder
                            video_url = part['video']['url']
                            if "PLACEHOLDER" not in video_url:
                                from utils.components import youtube_video
                                youtube_video(
                                    video_url,
                                    part['video']['title'],
                                    part['video']['description']
                                )
                            else:
                                st.info(f"?? **{part['video']['title']}**\n\n{part['video']['description']}\n\n*Film b�dzie dost�pny wkr�tce.*")
                            
                            st.markdown("---")
                
                else:
                    # Standardowa obs�uga dla innych lekcji
                    # Przygotuj zak�adki dla r�nych typ�w �wicze�
                    available_tabs = []
                    tab_keys = []
                    sub_tabs_data = {}
                    
                    # Fiszki - sprawdzanie wiedzy (nowa funkcjonalno��)
                    if 'flashcards' in practical_data:
                        available_tabs.append("?? Fiszki")
                        tab_keys.append('flashcards')
                        sub_tabs_data['flashcards'] = practical_data['flashcards']
                    
                    # Nowa struktura z 'exercises' i 'closing_quiz'
                    if 'exercises' in practical_data:
                        available_tabs.append("?? �wiczenia")
                        tab_keys.append('exercises')
                        sub_tabs_data['exercises'] = practical_data['exercises']
                    
                    # Case Studies - interaktywne przypadki do analizy
                    if 'case_studies' in practical_data:
                        available_tabs.append("?? Case Studies")
                        tab_keys.append('case_studies')
                        sub_tabs_data['case_studies'] = practical_data['case_studies']
                    
                    # AI Exercises - interaktywne �wiczenia sprawdzane przez AI
                    if 'ai_exercises' in practical_data:
                        available_tabs.append("?? �wiczenia AI")
                        tab_keys.append('ai_exercises')
                        sub_tabs_data['ai_exercises'] = practical_data['ai_exercises']
                    
                    # Pytania otwarte z ocen� AI
                    if 'ai_questions' in practical_data:
                        available_tabs.append("?? Pytania AI")
                        tab_keys.append('ai_questions')
                        sub_tabs_data['ai_questions'] = practical_data['ai_questions']
                    
                    # Challenge - AI generuje przypadki do rozwi�zania
                    if 'generated_case_studies' in practical_data:
                        available_tabs.append("?? Challenge")
                        tab_keys.append('generated_case_studies')
                        sub_tabs_data['generated_case_studies'] = practical_data['generated_case_studies']
                    
                    if 'closing_quiz' in practical_data:
                        available_tabs.append("?? Quiz ko�cowy")
                        tab_keys.append('closing_quiz')
                        sub_tabs_data['closing_quiz'] = practical_data['closing_quiz']
                    
                    # Backward compatibility - stara struktura bezpo�rednia (reflection, application, closing_quiz)
                    if 'reflection' in practical_data:
                        available_tabs.append("?? Refleksja")
                        tab_keys.append('reflection')
                        sub_tabs_data['reflection'] = practical_data['reflection']
                    
                    if 'application' in practical_data:
                        available_tabs.append("?? Zadania Praktyczne")
                        tab_keys.append('application')
                        sub_tabs_data['application'] = practical_data['application']
                    
                    # Renderuj zak�adki dla nowej struktury (exercises, closing_quiz)  
                    if available_tabs and 'tabs' not in practical_data:
                        # Wy�wietl pod-zak�adki dla nowej struktury
                        tabs = tabs_with_fallback(available_tabs)
                        
                        for i, (tab_key, tab_title) in enumerate(zip(tab_keys, available_tabs)):
                            with tabs[i]:
                                if tab_key == 'closing_quiz':
                                    # Specjalna obs�uga dla quizu ko�cowego
                                    lesson_title = lesson.get("title", "")
                                    if lesson_title == "Wprowadzenie do neuroprzyw�dztwa":
                                        # Dla tej lekcji quiz autodiagnozy bez wymogu 75%
                                        st.info("?? **Quiz autodiagnozy** - Ten quiz pomo�e Ci lepiej pozna� swoje podej�cie do przyw�dztwa. Nie ma tu dobrych ani z�ych odpowiedzi - chodzi o szczer� autorefleksj�.")
                                        
                                        quiz_data = sub_tabs_data['closing_quiz']
                                        quiz_completed, quiz_passed, earned_points = display_quiz(quiz_data, passing_threshold=0)  # Brak wymogu minimum
                                        
                                        # Oznacz quiz jako uko�czony po wype�nieniu
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
                                            # Quiz ko�cowy dostaje 1/3 z XP practical_exercises 
                                            success, earned_xp = award_fragment_xp(lesson_id, 'closing_quiz', step_xp_values['practical_exercises'] // 3)
                                            st.session_state[closing_quiz_xp_key] = True
                                            if success and earned_xp > 0:
                                                show_xp_notification(earned_xp, f"Zdoby�e� {earned_xp} XP za uko�czenie quizu autodiagnozy!")
                                        
                                        st.success("? Dzi�kujemy za szczer� autorefleksj�! Mo�esz teraz przej�� do podsumowania.")
                                        
                                        # Dodaj przycisk do ponownego przyst�pienia do quizu autodiagnozy
                                        st.markdown("---")
                                        col1, col2, col3 = st.columns([1, 1, 1])
                                        with col2:
                                            if st.button("?? Przyst�p ponownie", key=f"retry_autodiag_quiz_{lesson_id}", help="Mo�esz ponownie wype�ni� quiz autodiagnozy aby zaktualizowa� swoj� autorefleksj�", width='stretch'):
                                                # Reset stanu quizu
                                                quiz_id = f"quiz_{quiz_data.get('title', '').replace(' ', '_').lower()}"
                                                closing_quiz_key = f"closing_quiz_{lesson_id}"  # Definiuj tutaj
                                                
                                                # Usu� stan g��wny quizu
                                                if quiz_id in st.session_state:
                                                    del st.session_state[quiz_id]
                                                
                                                # Usu� wszystkie odpowiedzi na pytania
                                                for i in range(len(quiz_data.get('questions', []))):
                                                    question_key = f"{quiz_id}_q{i}_selected"
                                                    if question_key in st.session_state:
                                                        del st.session_state[question_key]
                                                    
                                                    # Usu� tak�e klucze suwak�w je�li istniej�
                                                    slider_key = f"{quiz_id}_q{i}_slider"
                                                    if slider_key in st.session_state:
                                                        del st.session_state[slider_key]
                                                
                                                # Reset stanu zaliczenia
                                                if closing_quiz_key in st.session_state:
                                                    st.session_state[closing_quiz_key]["quiz_completed"] = False
                                                    st.session_state[closing_quiz_key]["quiz_passed"] = False
                                                st.rerun()
                                    else:
                                        # Dla wszystkich innych lekcji standardowy quiz ko�cowy
                                        st.info("?? **Quiz ko�cowy** - Sprawd� swoj� wiedz� z tej lekcji. Musisz uzyska� minimum 75% poprawnych odpowiedzi, aby przej�� dalej.")
                                        
                                        quiz_data = sub_tabs_data['closing_quiz']
                                        quiz_completed, quiz_passed, earned_points = display_quiz(quiz_data, passing_threshold=75)
                                        
                                        # Oznacz quiz jako uko�czony po wype�nieniu
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
                                                # Quiz ko�cowy dostaje 1/3 z XP practical_exercises 
                                                success, earned_xp = award_fragment_xp(lesson_id, 'closing_quiz', step_xp_values['practical_exercises'] // 3)
                                                st.session_state[closing_quiz_xp_key] = True
                                                if success and earned_xp > 0:
                                                    show_xp_notification(earned_xp, f"Zdoby�e� {earned_xp} XP za uko�czenie quizu ko�cowego!")
                                            
                                            if quiz_passed:
                                                st.success("? Gratulacje! Zaliczy�e� quiz ko�cowy! Mo�esz teraz przej�� do podsumowania.")
                                            else:
                                                st.error("? Aby przej�� do podsumowania, musisz uzyska� przynajmniej 75% poprawnych odpowiedzi. Przyst�p do quizu ponownie u�ywaj�c przycisku powy�ej.")
                                elif tab_key == 'exercises':
                                    # Standardowa obs�uga dla zak�adki exercises
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wy�wietl opis zak�adki je�li istnieje
                                    if 'description' in tab_data:
                                        st.info(tab_data['description'])
                                    
                                    # Wy�wietl sekcje w zak�adce
                                    if 'sections' in tab_data:
                                        for section in tab_data['sections']:
                                            st.markdown(f"### {section.get('title', 'Sekcja')}")
                                            st.markdown(section.get('content', 'Brak tre�ci'), unsafe_allow_html=True)
                                    else:
                                        st.warning(f"Zak�adka '{tab_title}' nie zawiera sekcji do wy�wietlenia.")
                                
                                elif tab_key == 'flashcards':
                                    # Obs�uga fiszek
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wy�wietl tytu� i opis sekcji
                                    if 'title' in tab_data:
                                        st.markdown(f"### {tab_data['title']}")
                                    if 'description' in tab_data:
                                        st.info(tab_data['description'])
                                    
                                    # Obs�uga fiszek
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
                                            
                                            # Wy�wietl kart�
                                            if not flashcard_state['show_back']:
                                                # Prz�d karty
                                                st.markdown(f"### ?? Fiszka {flashcard_state['current_card'] + 1}/{total_cards}")
                                                
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
                                                    if st.button("?? Poka� odpowied�", key=f"show_back_{card_id}", type="primary", width="stretch"):
                                                        flashcard_state['show_back'] = True
                                                        st.rerun()
                                            
                                            else:
                                                # Ty� karty
                                                st.markdown(f"### ?? Fiszka {flashcard_state['current_card'] + 1}/{total_cards}")
                                                
                                                # Pytanie (mniejsze)
                                                st.markdown(f"""
                                                <div style='background: #f8f9fa; padding: 15px; border-radius: 10px; 
                                                           border-left: 4px solid #667eea; margin: 15px 0;'>
                                                    <strong>Pytanie:</strong> {current_card['front']}
                                                </div>
                                                """, unsafe_allow_html=True)
                                                
                                                # Odpowied�
                                                st.markdown(f"""
                                                <div style='background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%); 
                                                           padding: 30px; border-radius: 15px; color: white; 
                                                           margin: 20px 0; min-height: 150px;'>
                                                    <h4 style='color: white; margin-bottom: 15px;'>? Odpowied�:</h4>
                                                    <p style='color: white; margin: 0; font-size: 1.1rem; line-height: 1.5;'>
                                                        {current_card['back']}
                                                    </p>
                                                </div>
                                                """, unsafe_allow_html=True)
                                                
                                                # Ocena zrozumienia
                                                st.markdown("#### Jak dobrze zna�e� odpowied�?")
                                                col1, col2, col3 = st.columns(3)
                                                
                                                with col1:
                                                    if st.button("? Nie wiedzia�em", key=f"incorrect_{card_id}", type="secondary", width="stretch"):
                                                        flashcard_state['studied_cards'].add(card_id)
                                                        flashcard_state['incorrect_answers'].add(card_id)
                                                        flashcard_state['correct_answers'].discard(card_id)  # Usu� z poprawnych je�li by�o
                                                        flashcard_state['show_back'] = False
                                                        flashcard_state['current_card'] = (flashcard_state['current_card'] + 1) % total_cards
                                                        st.rerun()
                                                
                                                with col2:
                                                    if st.button("?? Cz�ciowo", key=f"partial_{card_id}", width="stretch"):
                                                        flashcard_state['studied_cards'].add(card_id)
                                                        # Cz�ciowa wiedza = nie dodawaj do �adnej kategorii
                                                        flashcard_state['show_back'] = False
                                                        flashcard_state['current_card'] = (flashcard_state['current_card'] + 1) % total_cards
                                                        st.rerun()
                                                
                                                with col3:
                                                    if st.button("? Wiedzia�em", key=f"correct_{card_id}", type="primary", width="stretch"):
                                                        flashcard_state['studied_cards'].add(card_id)
                                                        flashcard_state['correct_answers'].add(card_id)
                                                        flashcard_state['incorrect_answers'].discard(card_id)  # Usu� z niepoprawnych je�li by�o
                                                        flashcard_state['show_back'] = False
                                                        flashcard_state['current_card'] = (flashcard_state['current_card'] + 1) % total_cards
                                                        st.rerun()
                                            
                                            # Funkcje dodatkowe
                                            st.markdown("---")
                                            col1, col2 = st.columns(2)
                                            
                                            with col1:
                                                if st.button("?? Reset post�pu", key=f"reset_flashcards_{lesson_id}"):
                                                    flashcard_state['current_card'] = 0
                                                    flashcard_state['show_back'] = False
                                                    flashcard_state['studied_cards'] = set()
                                                    flashcard_state['correct_answers'] = set()
                                                    flashcard_state['incorrect_answers'] = set()
                                                    st.success("Reset post�pu fiszek!")
                                                    st.rerun()
                                            
                                            with col2:
                                                if st.button("?? Tylko niepoprawne", key=f"review_incorrect_{lesson_id}", disabled=len(flashcard_state['incorrect_answers']) == 0):
                                                    # Znajd� pierwsz� niepoprawn� kart�
                                                    for i, card in enumerate(cards):
                                                        if card['id'] in flashcard_state['incorrect_answers']:
                                                            flashcard_state['current_card'] = i
                                                            flashcard_state['show_back'] = False
                                                            break
                                                    st.rerun()
                                            
                                            # Statystyki nauki na dole
                                            st.markdown("---")
                                            st.markdown("### ?? Statystyki nauki")
                                            
                                            studied_count = len(flashcard_state['studied_cards'])
                                            correct_count = len(flashcard_state['correct_answers'])
                                            incorrect_count = len(flashcard_state['incorrect_answers'])
                                            
                                            # Wy�wietl post�p
                                            col1, col2, col3, col4 = st.columns(4)
                                            with col1:
                                                st.metric("Przejrzane", f"{studied_count}/{total_cards}")
                                            with col2:
                                                st.metric("Poprawne", correct_count)
                                            with col3:
                                                st.metric("Niepoprawne", incorrect_count)
                                            with col4:
                                                accuracy = (correct_count / max(studied_count, 1)) * 100
                                                st.metric("Skuteczno��", f"{accuracy:.1f}%")
                                            
                                            # Progress bar
                                            progress = studied_count / total_cards
                                            st.progress(progress, text=f"Post�p nauki: {studied_count}/{total_cards} fiszek")
                                            
                                            # Award XP za zako�czenie wszystkich fiszek
                                            if studied_count == total_cards:
                                                flashcards_xp_key = f"flashcards_xp_{lesson_id}"
                                                if not st.session_state.get(flashcards_xp_key, False):
                                                    flashcards_xp = step_xp_values['practical_exercises'] // 6  # 1/6 XP z practical_exercises
                                                    success, earned_xp = award_fragment_xp(lesson_id, 'flashcards', flashcards_xp)
                                                    st.session_state[flashcards_xp_key] = True
                                                    if success and earned_xp > 0:
                                                        st.success(f"?? Przejrza�e� wszystkie fiszki! Zdoby�e� {earned_xp} XP!")
                                        
                                        else:
                                            st.warning("Brak fiszek do wy�wietlenia.")
                                    else:
                                        st.warning("Brak fiszek w tej sekcji.")
                                
                                elif tab_key == 'case_studies':
                                    # Obs�uga Case Studies - interaktywne przypadki do analizy
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wy�wietl tytu� i opis sekcji
                                    if 'title' in tab_data:
                                        st.markdown(f"### {tab_data['title']}")
                                    if 'description' in tab_data:
                                        st.info(tab_data['description'])
                                    
                                    # Obs�uga studies
                                    if 'studies' in tab_data:
                                        studies = tab_data['studies']
                                        
                                        for study in studies:
                                            with st.expander(f"**Case Study {study['id']}: {study['title']}**", expanded=False):
                                                # Opis scenariusza
                                                st.markdown("#### ?? Scenariusz")
                                                st.markdown(study['scenario'], unsafe_allow_html=True)
                                                
                                                # Pytania do przemy�lenia
                                                st.markdown("#### ?? Pytania do przemy�lenia")
                                                for i, question in enumerate(study['questions'], 1):
                                                    st.markdown(f"**{i}.** {question}")
                                                
                                                # Miejsce na odpowied� u�ytkownika
                                                st.markdown(study['user_space'], unsafe_allow_html=True)
                                                
                                                # Rozwijane rozwi�zanie
                                                with st.expander("?? **Poka� przyk�adowe rozwi�zanie**", expanded=False):
                                                    st.markdown(study['solution'], unsafe_allow_html=True)
                                                
                                                st.markdown("---")
                                    else:
                                        st.warning("Brak case studies w tej sekcji.")
                                
                                elif tab_key == 'ai_questions':
                                    # Obs�uga pyta� otwartych z ocen� AI
                                    try:
                                        from utils.ai_questions import display_open_question, load_open_question_styles
                                        load_open_question_styles()
                                        
                                        tab_data = sub_tabs_data[tab_key]
                                        
                                        # Wy�wietl tytu� i opis sekcji
                                        if 'title' in tab_data:
                                            st.markdown(f"### {tab_data['title']}")
                                        if 'description' in tab_data:
                                            st.info(tab_data['description'])
                                        
                                        # Wy�wietl pytania
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
                                            
                                            # Podsumowanie wynik�w
                                            if answered_questions > 0:
                                                st.markdown("### ?? Podsumowanie wynik�w")
                                                percentage = (total_score / max_total_score) * 100 if max_total_score > 0 else 0
                                                
                                                col1, col2, col3 = st.columns(3)
                                                with col1:
                                                    st.metric("Odpowiedziano", f"{answered_questions}/{total_questions}")
                                                with col2:
                                                    st.metric("Punkty", f"{total_score}/{max_total_score}")
                                                with col3:
                                                    st.metric("Wynik", f"{percentage:.1f}%")
                                                
                                                if answered_questions == total_questions:
                                                    # Award XP za uko�czenie wszystkich pyta� AI
                                                    ai_questions_xp_key = f"ai_questions_xp_{lesson_id}"
                                                    if not st.session_state.get(ai_questions_xp_key, False):
                                                        ai_xp = step_xp_values['practical_exercises'] // 4  # 1/4 XP z practical_exercises
                                                        success, earned_xp = award_fragment_xp(lesson_id, 'ai_questions', ai_xp)
                                                        st.session_state[ai_questions_xp_key] = True
                                                        if success and earned_xp > 0:
                                                            st.success(f"?? Uko�czy�e� wszystkie pytania AI! Zdoby�e� {earned_xp} XP!")
                                        else:
                                            st.warning("Brak pyta� do wy�wietlenia.")
                                    
                                    except ImportError:
                                        st.error("Modu� obs�ugi pyta� AI nie jest dost�pny. Skontaktuj si� z administratorem.")
                                    except Exception as e:
                                        st.error(f"B��d podczas �adowania pyta� AI: {str(e)}")
                                
                                elif tab_key == 'ai_exercises':
                                    # Obs�uga �wicze� AI - interaktywne �wiczenia sprawdzane przez AI
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wy�wietl tytu� i opis sekcji
                                    if 'title' in tab_data:
                                        st.markdown(f"### {tab_data['title']}")
                                    if 'description' in tab_data:
                                        st.info(tab_data['description'])
                                    
                                    # Obs�uga �wicze� AI
                                    if 'exercises' in tab_data:
                                        exercises = tab_data['exercises']
                                        
                                        # Wy�wietl konfiguracj� AI je�li istnieje - USUNI�TE (nie potrzebne)
                                        
                                        for exercise in exercises:
                                            exercise_id = exercise.get('id', 'unknown')
                                            exercise_title = exercise.get('title', '�wiczenie')
                                            exercise_type = exercise.get('type', 'standard')
                                            
                                            with st.expander(f"**{exercise_title}**", expanded=True):
                                                # Wy�wietl zawarto�� �wiczenia
                                                if 'content' in exercise:
                                                    content = exercise['content']
                                                    
                                                    # G��wna tre��
                                                    if 'main' in content:
                                                        st.markdown(content['main'], unsafe_allow_html=True)
                                                    
                                                    # Scenariusz (dla symulacji)
                                                    if 'scenario' in content:
                                                        st.markdown(content['scenario'], unsafe_allow_html=True)
                                                    
                                                    # Przypadek do analizy
                                                    if 'case_study' in content:
                                                        st.markdown(content['case_study'], unsafe_allow_html=True)
                                                    
                                                    # Interfejs refleksji
                                                    if 'reflection_interface' in content:
                                                        st.markdown(content['reflection_interface'], unsafe_allow_html=True)
                                                    
                                                    # Prompt do �wiczenia
                                                    if 'exercise_prompt' in content:
                                                        st.markdown(content['exercise_prompt'], unsafe_allow_html=True)
                                                    
                                                    # Prompt do analizy
                                                    if 'analysis_prompt' in content:
                                                        st.markdown(content['analysis_prompt'], unsafe_allow_html=True)
                                                    
                                                    # Interaktywne elementy (quiz wiedzy)
                                                    if 'interactive_elements' in content:
                                                        for element in content['interactive_elements']:
                                                            if element['type'] == 'knowledge_check':
                                                                st.markdown("---")
                                                                question = element['question']
                                                                options = element['options']
                                                                correct = element['correct']
                                                                explanation = element.get('explanation', '')
                                                                
                                                                # Sprawd� czy ju� odpowiedziano
                                                                answer_key = f"knowledge_check_{exercise_id}_{lesson_id}"
                                                                
                                                                st.markdown(f"**Pytanie:** {question}")
                                                                selected = st.radio(
                                                                    "Wybierz odpowied�:",
                                                                    options,
                                                                    key=answer_key,
                                                                    index=None
                                                                )
                                                                
                                                                if selected:
                                                                    selected_index = options.index(selected)
                                                                    if selected_index == correct:
                                                                        st.success(f"? Poprawnie! {explanation}")
                                                                    else:
                                                                        st.error(f"? Niepoprawnie. Prawid�owa odpowied� to: {options[correct]}")
                                                                        st.info(explanation)
                                                
                                                st.markdown("---")
                                                
                                                # Placeholder dla przysz�ej integracji AI
                                                if exercise_type == 'ai_exercise':
                                                    # Importuj i u�yj modu�u AI
                                                    try:
                                                        from utils.ai_exercises import display_ai_exercise_interface
                                                        
                                                        lesson_title = lesson.get("title", "")
                                                        exercise_completed = display_ai_exercise_interface(exercise, lesson_title)
                                                        
                                                        # Je�li �wiczenie uko�czone, zapisz w sesji
                                                        if exercise_completed:
                                                            completed_key = f"ai_exercise_{exercise_id}_{lesson_id}_completed"
                                                            st.session_state[completed_key] = True
                                                    
                                                    except ImportError:
                                                        st.error("Modu� obs�ugi �wicze� AI nie jest dost�pny.")
                                                    except Exception as e:
                                                        st.error(f"B��d podczas �adowania �wiczenia AI: {str(e)}")
                                                        # Fallback - podstawowy interfejs
                                                        st.markdown("### ?? Feedback AI")
                                                        st.info("Funkcjonalno�� oceny AI b�dzie dost�pna wkr�tce. Na razie mo�esz przeanalizowa� swoje odpowiedzi samodzielnie u�ywaj�c wskaz�wek z lekcji.")
                                                        
                                                        # Wy�wietl kryteria oceny je�li dost�pne
                                                        if 'ai_config' in exercise:
                                                            ai_config = exercise['ai_config']
                                                            if 'feedback_criteria' in ai_config:
                                                                st.markdown("**Kryteria oceny AI:**")
                                                                criteria = ai_config['feedback_criteria']
                                                                if isinstance(criteria, list):
                                                                    for criterion in criteria:
                                                                        st.markdown(f"� {criterion}")
                                                                elif isinstance(criteria, dict):
                                                                    for criterion, weight in criteria.items():
                                                                        st.markdown(f"� {criterion}: {weight}%")
                                        
                                        # Podsumowanie �wicze� AI
                                        st.markdown("---")
                                        st.markdown("### ?? Post�p �wicze� AI")
                                        
                                        completed_exercises = 0
                                        # Liczymy tylko prawdziwe �wiczenia AI (z ai_config)
                                        ai_only_exercises = [ex for ex in exercises if 'ai_config' in ex]
                                        total_exercises = len(ai_only_exercises)
                                        
                                        # Sprawd� ile �wicze� zosta�o uko�czonych
                                        for exercise in ai_only_exercises:
                                            exercise_id = exercise.get('id', 'unknown')
                                            completion_key = f"ai_exercise_{exercise_id}_completed"
                                            if st.session_state.get(completion_key, False):
                                                completed_exercises += 1
                                        
                                        # Wy�wietl post�p
                                        progress = completed_exercises / total_exercises if total_exercises > 0 else 0
                                        st.progress(progress, text=f"Uko�czone �wiczenia: {completed_exercises}/{total_exercises}")
                                        
                                        col1, col2, col3 = st.columns(3)
                                        with col1:
                                            st.metric("Uko�czone", f"{completed_exercises}/{total_exercises}")
                                        with col2:
                                            percentage = (completed_exercises / total_exercises * 100) if total_exercises > 0 else 0
                                            st.metric("Post�p", f"{percentage:.0f}%")
                                        with col3:
                                            remaining = total_exercises - completed_exercises
                                            st.metric("Pozosta�o", remaining)
                                        
                                        # Award XP za �wiczenia AI
                                        if completed_exercises == total_exercises and total_exercises > 0:
                                            ai_exercises_xp_key = f"ai_exercises_xp_{lesson_id}"
                                            if not st.session_state.get(ai_exercises_xp_key, False):
                                                ai_xp = step_xp_values['practical_exercises'] // 3  # 1/3 XP z practical_exercises
                                                success, earned_xp = award_fragment_xp(lesson_id, 'ai_exercises', ai_xp)
                                                st.session_state[ai_exercises_xp_key] = True
                                                if success and earned_xp > 0:
                                                    st.balloons()
                                                    st.success(f"?? Gratulacje! Uko�czy�e� wszystkie �wiczenia AI! Zdoby�e� {earned_xp} XP!")
                                        
                                        # Motywuj�ca wiadomo��
                                        if completed_exercises > 0:
                                            if completed_exercises == total_exercises:
                                                st.success("?? Doskonale! Uko�czy�e� wszystkie �wiczenia AI. Twoje umiej�tno�ci C-IQ s� teraz znacznie lepsze!")
                                            else:
                                                st.info(f"?? �wietna robota! Uko�czy�e� ju� {completed_exercises} z {total_exercises} �wicze�. Kontynuuj rozw�j!")
                                        else:
                                            st.info("?? Zacznij od pierwszego �wiczenia, aby rozwija� swoje umiej�tno�ci Conversational Intelligence!")
                                        
                                        # Przycisk resetowania �wicze�
                                        from utils.ai_exercises import display_reset_all_button
                                        display_reset_all_button(lesson_id)
                                    else:
                                        st.warning("Brak �wicze� AI w tej sekcji.")
                                
                                elif tab_key == 'generated_case_studies':
                                    # Obs�uga dynamicznych case studies generowanych przez AI
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wy�wietl tytu� sekcji
                                    if 'title' in tab_data:
                                        st.markdown(f"### {tab_data['title']}")
                                    
                                    # Obs�uga �wicze� z generowanymi case studies
                                    if 'exercises' in tab_data:
                                        exercises = tab_data['exercises']
                                        
                                        # Pobierz pierwsze �wiczenie (u�ywamy go jako szablon)
                                        if exercises:
                                            exercise = exercises[0]
                                            exercise_type = exercise.get('type', 'ai_exercise')
                                            
                                            # Obs�uga �wiczenia AI z dynamicznym generowaniem case studies
                                            if exercise_type == 'ai_exercise' and 'ai_config' in exercise:
                                                try:
                                                    from utils.ai_exercises import display_ai_exercise_interface
                                                    
                                                    lesson_title = lesson.get("title", "")
                                                    exercise_completed = display_ai_exercise_interface(exercise, lesson_title)
                                                    
                                                    # Je�li �wiczenie uko�czone, zapisz w sesji
                                                    if exercise_completed:
                                                        exercise_id = exercise.get('id', 'unknown')
                                                        completed_key = f"generated_case_{exercise_id}_{lesson_id}_completed"
                                                        st.session_state[completed_key] = True
                                                
                                                except ImportError:
                                                    st.error("Modu� obs�ugi �wicze� AI nie jest dost�pny.")
                                                except Exception as e:
                                                    st.error(f"B��d podczas �adowania dynamicznego case study: {str(e)}")
                                                    # Fallback - podstawowy interfejs
                                                    st.markdown("### ?? Challenge")
                                                    st.info("Funkcjonalno�� generowania challenge b�dzie dost�pna wkr�tce.")
                                                    
                                                    # Wy�wietl kryteria oceny je�li dost�pne
                                                    if 'ai_config' in exercise:
                                                        ai_config = exercise['ai_config']
                                                        if 'feedback_criteria' in ai_config:
                                                            st.markdown("**Kryteria oceny AI:**")
                                                            criteria = ai_config['feedback_criteria']
                                                            if isinstance(criteria, list):
                                                                for criterion in criteria:
                                                                    st.markdown(f"� {criterion}")
                                    else:
                                        st.warning("Brak dynamicznych case studies w tej sekcji.")
                                
                                else:
                                    # Standardowa obs�uga dla innych zak�adek
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wy�wietl opis zak�adki je�li istnieje
                                    if 'description' in tab_data:
                                        st.info(tab_data['description'])
                                    
                                    # Wy�wietl sekcje w zak�adce
                                    if 'sections' in tab_data:
                                        for section in tab_data['sections']:
                                            st.markdown(f"### {section.get('title', 'Sekcja')}")
                                            st.markdown(section.get('content', 'Brak tre�ci'), unsafe_allow_html=True)
                                    else:
                                        st.warning(f"Zak�adka '{tab_title}' nie zawiera sekcji do wy�wietlenia.")
                
                # Stara struktura z 'tabs' (backward compatibility)
                if 'tabs' in practical_data:
                    old_tabs = practical_data['tabs']
                    
                    # Inicjalizuj zmienne dla starej struktury
                    available_tabs = []
                    tab_keys = []
                    sub_tabs_data = {}
                    
                    # Sprawd� kt�re zak�adki s� dost�pne i przygotuj je w logicznej kolejno�ci uczenia si�
                    # 1. Autotest - sprawdzenie aktualnego stanu
                    if 'autotest' in old_tabs:
                        available_tabs.append("?? Autotest")
                        tab_keys.append('autotest')
                        sub_tabs_data['autotest'] = old_tabs['autotest']
                    
                    # 2. Refleksja - przemy�lenie w�asnych do�wiadcze�
                    if 'reflection' in old_tabs:
                        available_tabs.append("?? Refleksja")
                        tab_keys.append('reflection')
                        sub_tabs_data['reflection'] = old_tabs['reflection']
                    
                    # 3. Analiza - case studies i scenariusze
                    if 'analysis' in old_tabs:
                        available_tabs.append("?? Analiza")
                        tab_keys.append('analysis')
                        sub_tabs_data['analysis'] = old_tabs['analysis']
                    
                    # 4. Wdro�enie - konkretny plan dzia�ania
                    if 'implementation' in old_tabs:
                        available_tabs.append("?? Wdro�enie")
                        tab_keys.append('implementation')
                        sub_tabs_data['implementation'] = old_tabs['implementation']
                    
                    # 5. Quiz ko�cowy - przeniesiony z osobnego kroku
                    if 'closing_quiz' in lesson.get('sections', {}):
                        # Sprawd� tytu� lekcji dla specjalnej nazwy tabu
                        lesson_title = lesson.get("title", "")
                        if lesson_title == "Wprowadzenie do neuroprzyw�dztwa":
                            available_tabs.append("?? Quiz autodiagnozy")
                        else:
                            available_tabs.append("?? Quiz ko�cowy")
                        tab_keys.append('closing_quiz')
                        sub_tabs_data['closing_quiz'] = lesson['sections']['closing_quiz']
                    
                    if available_tabs:
                        # Wy�wietl pod-zak�adki
                        tabs = tabs_with_fallback(available_tabs)
                        
                        for i, (tab_key, tab_title) in enumerate(zip(tab_keys, available_tabs)):
                            with tabs[i]:
                                if tab_key == 'closing_quiz':
                                    # Specjalna obs�uga dla quizu ko�cowego
                                    lesson_title = lesson.get("title", "")
                                    if lesson_title == "Wprowadzenie do neuroprzyw�dztwa":
                                        # Dla tej lekcji quiz autodiagnozy bez wymogu 75%
                                        st.info("?? **Quiz autodiagnozy** - Ten quiz pomo�e Ci lepiej pozna� swoje podej�cie do przyw�dztwa. Nie ma tu dobrych ani z�ych odpowiedzi - chodzi o szczer� autorefleksj�.")
                                        
                                        quiz_data = sub_tabs_data['closing_quiz']
                                        quiz_completed, quiz_passed, earned_points = display_quiz(quiz_data, passing_threshold=0)  # Brak wymogu minimum
                                        
                                        # Oznacz quiz jako uko�czony po wype�nieniu
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
                                                # Quiz ko�cowy dostaje 1/3 z XP practical_exercises 
                                                success, earned_xp = award_fragment_xp(lesson_id, 'closing_quiz', step_xp_values['practical_exercises'] // 3)
                                                st.session_state[closing_quiz_xp_key] = True
                                                if success and earned_xp > 0:
                                                    show_xp_notification(earned_xp, f"Zdoby�e� {earned_xp} XP za uko�czenie quizu autodiagnozy!")
                                            
                                            st.success("? Dzi�kujemy za szczer� autorefleksj�! Mo�esz teraz przej�� do podsumowania.")
                                            
                                            # Dodaj przycisk do ponownego przyst�pienia do quizu autodiagnozy
                                            st.markdown("---")
                                            col1, col2, col3 = st.columns([1, 1, 1])
                                            with col2:
                                                if st.button("?? Przyst�p ponownie", key=f"retry_autodiag_quiz_practical_{lesson_id}", help="Mo�esz ponownie wype�ni� quiz autodiagnozy aby zaktualizowa� swoj� autorefleksj�", width='stretch'):
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
                                        # Dla wszystkich innych lekcji standardowy quiz ko�cowy
                                        st.info("?? **Quiz ko�cowy** - Sprawd� swoj� wiedz� z tej lekcji. Musisz uzyska� minimum 75% poprawnych odpowiedzi, aby przej�� dalej.")
                                        
                                        quiz_data = sub_tabs_data['closing_quiz']
                                        quiz_completed, quiz_passed, earned_points = display_quiz(quiz_data, passing_threshold=75)
                                          # Oznacz quiz jako uko�czony po wype�nieniu
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
                                                # Quiz ko�cowy dostaje 1/3 z XP practical_exercises 
                                                success, earned_xp = award_fragment_xp(lesson_id, 'closing_quiz', step_xp_values['practical_exercises'] // 3)
                                                st.session_state[closing_quiz_xp_key] = True
                                                if success and earned_xp > 0:
                                                    show_xp_notification(earned_xp, f"Zdoby�e� {earned_xp} XP za uko�czenie quizu ko�cowego!")
                                            
                                            if quiz_passed:
                                                st.success("? Gratulacje! Zaliczy�e� quiz ko�cowy! Mo�esz teraz przej�� do podsumowania.")
                                            else:
                                                st.error("? Aby przej�� do podsumowania, musisz uzyska� przynajmniej 75% poprawnych odpowiedzi. Przyst�p do quizu ponownie u�ywaj�c przycisku powy�ej.")
                                else:
                                    # Standardowa obs�uga dla innych zak�adek
                                    tab_data = sub_tabs_data[tab_key]
                                    
                                    # Wy�wietl opis zak�adki je�li istnieje
                                    if 'description' in tab_data:
                                        st.info(tab_data['description'])
                                    
                                    # Wy�wietl sekcje w zak�adce
                                    if 'sections' in tab_data:
                                        for section in tab_data['sections']:
                                            st.markdown(f"### {section.get('title', 'Sekcja')}")
                                            
                                            # U�yj nowego renderera obs�uguj�cego osadzone media
                                            content = section.get('content', 'Brak tre�ci')
                                            render_embedded_content(content, section)
                                            
                                            # Je�li sekcja wymaga odpowiedzi u�ytkownika
                                            if section.get('interactive', False):
                                                # Generuj klucz dla przechowywania odpowiedzi
                                                section_key = f"practical_{tab_key}_{section.get('title', '').replace(' ', '_').lower()}"
                                                  # U�yj formularza dla lepszego UX
                                                with st.form(key=f"form_{section_key}"):
                                                    # Pobierz istniej�c� odpowied� (je�li jest)
                                                    existing_response = st.session_state.get(section_key, "")
                                                    
                                                    # Wy�wietl pole tekstowe z istniej�c� odpowiedzi�
                                                    user_response = st.text_area(
                                                        "Twoja odpowied�:",
                                                        value=existing_response,
                                                        height=200,
                                                        key=f"input_{section_key}"
                                                    )
                                                      # Przycisk do zapisywania odpowiedzi w formularzu
                                                    submitted = st.form_submit_button("Zapisz odpowied�")
                                                    
                                                    if submitted:
                                                        # Zapisz odpowied� w stanie sesji
                                                        st.session_state[section_key] = user_response
                                                        st.success("Twoja odpowied� zosta�a zapisana!")
                                    else:
                                        st.warning(f"Zak�adka '{tab_title}' nie zawiera sekcji do wy�wietlenia.")
                    else:
                        st.warning("Nie znaleziono dost�pnych pod-zak�adek w sekcji �wicze� praktycznych.")
              # Przycisk "Dalej" po �wiczeniach praktycznych - z kontrol� dost�pu do podsumowania
            st.markdown("<div class='next-button'>", unsafe_allow_html=True)
            
            # Sprawd� czy nast�pny krok to 'summary' i czy quiz ko�cowy zosta� zdany
            if next_step == 'summary':
                lesson_title = lesson.get("title", "")
                closing_quiz_key = f"closing_quiz_{lesson_id}"
                closing_quiz_state = st.session_state.get(closing_quiz_key, {})
                quiz_passed = closing_quiz_state.get("quiz_passed", False)
                
                # Dla lekcji "Wprowadzenie do neuroprzyw�dztwa" nie ma blokowania
                if lesson_title == "Wprowadzenie do neuroprzyw�dztwa" or quiz_passed:                    # Quiz zdany lub brak wymogu dla specjalnej lekcji - normalny przycisk "Dalej"
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
                                show_xp_notification(xp_awarded, f"Zdoby�e� {xp_awarded} XP za uko�czenie �wicze� praktycznych!")
                                
                                # Refresh user data for real-time updates
                                from utils.real_time_updates import refresh_user_data
                                refresh_user_data()
                                
                                # Sprawd� czy lekcja zosta�a uko�czona
                                check_and_mark_lesson_completion(lesson_id)
                            
                            # Przejd� do nast�pnego kroku
                            st.session_state.lesson_step = next_step
                            scroll_to_top()
                            st.rerun()
                else:
                    # Quiz niezdany - zablokowany przycisk z komunikatem
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        zen_button(
                            f"?? Dalej: {step_names.get(next_step, next_step.capitalize())}",
                            disabled=True,
                            width='stretch',
                            help="Musisz zaliczy� quiz ko�cowy (min. 75%) aby przej�� do podsumowania"
                        )
                    st.warning("?? Aby przej�� do podsumowania, musisz najpierw zaliczy� quiz ko�cowy z wynikiem minimum 75%. Przejd� do zak�adki '?? Quiz ko�cowy' powy�ej.")
            else:                # Normalny przycisk dla innych krok�w (nie-summary)
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
                            show_xp_notification(xp_awarded, f"Zdoby�e� {xp_awarded} XP za uko�czenie �wicze� praktycznych!")
                            
                            # Refresh user data for real-time updates
                            from utils.real_time_updates import refresh_user_data
                            refresh_user_data()
                            
                            # Sprawd� czy lekcja zosta�a uko�czona
                            check_and_mark_lesson_completion(lesson_id)
                        
                        # Przejd� do nast�pnego kroku
                        st.session_state.lesson_step = next_step
                        scroll_to_top()
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.lesson_step == 'reflection':
            # Wy�wietl sekcje refleksji
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'reflection' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'reflection'!")
            elif 'sections' not in lesson['sections'].get('reflection', {}):
                st.error("Sekcja 'reflection' nie zawiera klucza 'sections'!")
            else:
                # Wy�wietl sekcje refleksji
                for section in lesson["sections"]["reflection"]["sections"]:
                    st.markdown(f"### {section.get('title', 'Zadanie refleksyjne')}")
                    st.markdown(section.get("content", "Brak tre�ci"), unsafe_allow_html=True)
                    
                    # Generuj klucz dla przechowywania odpowiedzi
                    reflection_key = f"reflection_{section.get('title', '').replace(' ', '_').lower()}"
                    
                    # Generuj INNY klucz dla widgetu tekstowego
                    widget_key = f"input_{reflection_key}"
                    
                    # U�yj formularza, aby unikn�� problem�w z aktualizacj� stanu sesji
                    with st.form(key=f"form_{reflection_key}"):
                        # Pobierz istniej�c� odpowied� (je�li jest)
                        existing_response = st.session_state.get(reflection_key, "")
                        
                        # Wy�wietl pole tekstowe z istniej�c� odpowiedzi�
                        user_reflection = st.text_area(
                            "Twoja odpowied�:",
                            value=existing_response,
                            height=200,
                            key=widget_key
                        )
                        
                        # Przycisk do zapisywania odpowiedzi w formularzu
                        submitted = st.form_submit_button("Zapisz odpowied�")
                        
                        if submitted:
                            # Zapisz odpowied� w stanie sesji
                            st.session_state[reflection_key] = user_reflection
                            st.success("Twoja odpowied� zosta�a zapisana!")              # Przycisk "Dalej" po refleksji
            st.markdown("<div class='next-button'>", unsafe_allow_html=True)
              # Sprawd� czy nast�pny krok to 'summary' i czy quiz ko�cowy zosta� zdany
            if next_step == 'summary':
                lesson_title = lesson.get("title", "")
                closing_quiz_key = f"closing_quiz_{lesson_id}"
                closing_quiz_state = st.session_state.get(closing_quiz_key, {})
                quiz_passed = closing_quiz_state.get("quiz_passed", False)
                
                # Dla lekcji "Wprowadzenie do neuroprzyw�dztwa" nie ma blokowania
                if lesson_title == "Wprowadzenie do neuroprzyw�dztwa" or quiz_passed:
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
                                show_xp_notification(xp_awarded, f"Zdoby�e� {xp_awarded} XP za wykonanie zada� refleksyjnych!")
                                
                                # Refresh user data for real-time updates
                                from utils.real_time_updates import refresh_user_data
                                refresh_user_data()
                            
                            # Przejd� do nast�pnego kroku
                            st.session_state.lesson_step = next_step
                            scroll_to_top()
                            st.rerun()
                else:
                    # Quiz niezdany - zablokowany przycisk z komunikatem
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        zen_button(
                            f"?? Dalej: {step_names.get(next_step, next_step.capitalize())}",
                            disabled=True,
                            width='stretch',
                            help="Musisz zaliczy� quiz ko�cowy (min. 75%) aby przej�� do podsumowania"
                        )
                    st.warning("?? Aby przej�� do podsumowania, musisz najpierw zaliczy� quiz ko�cowy z wynikiem minimum 75%. Quiz znajdziesz w sekcji 'Praktyka' � '?? Quiz ko�cowy'.")
            else:
                # Normalny przycisk dla innych krok�w (nie-summary)
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
                            show_xp_notification(xp_awarded, f"Zdoby�e� {xp_awarded} XP za wykonanie zada� refleksyjnych!")
                            
                            # Refresh user data for real-time updates
                            from utils.real_time_updates import refresh_user_data
                            refresh_user_data()
                        
                        # Przejd� do nast�pnego kroku
                        st.session_state.lesson_step = next_step
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif st.session_state.lesson_step == 'application':
            # Wy�wietl zadania praktyczne
            if 'sections' not in lesson:
                st.error("Lekcja nie zawiera klucza 'sections'!")
            elif 'application' not in lesson.get('sections', {}):
                st.error("Lekcja nie zawiera sekcji 'application'!")
            elif 'sections' not in lesson['sections'].get('application', {}):
                st.error("Sekcja 'application' nie zawiera klucza 'sections'!")
            else:
                # Wy�wietl zadania praktyczne
                for section in lesson["sections"]["application"]["sections"]:
                    st.markdown(f"### {section.get('title', 'Zadanie praktyczne')}")
                    st.markdown(section.get("content", "Brak tre�ci"), unsafe_allow_html=True)
                    
                    # Generuj klucz dla przechowywania odpowiedzi
                    task_key = f"application_{section.get('title', '').replace(' ', '_').lower()}"
                    
                    # U�yj formularza, aby unikn�� problem�w z aktualizacj� stanu sesji
                    with st.form(key=f"form_{task_key}"):
                        # Pobierz istniej�c� odpowied� (je�li jest)
                        existing_solution = st.session_state.get(task_key, "")
                        
                        # Wy�wietl pole tekstowe z istniej�c� odpowiedzi�
                        user_solution = st.text_area(
                            "Twoje rozwi�zanie:",
                            value=existing_solution,
                            height=200,
                            key=f"input_{task_key}"
                        )
                        
                        # Przycisk do zapisywania odpowiedzi w formularzu
                        submitted = st.form_submit_button("Zapisz rozwi�zanie")
                        
                        if submitted:
                            # Zapisz odpowied� w stanie sesji
                            st.session_state[task_key] = user_solution
                            st.success("Twoje rozwi�zanie zosta�a zapisana!")
                            # Dodaj od�wie�enie strony po zapisaniu
                            st.rerun()              # Przycisk "Dalej" po zadaniach praktycznych
            st.markdown("<div class='next-button'>", unsafe_allow_html=True)
            
            # Sprawd� czy nast�pny krok to 'summary' i czy quiz ko�cowy zosta� zdany
            if next_step == 'summary':
                lesson_title = lesson.get("title", "")
                closing_quiz_key = f"closing_quiz_{lesson_id}"
                closing_quiz_state = st.session_state.get(closing_quiz_key, {})
                quiz_passed = closing_quiz_state.get("quiz_passed", False)
                
                # Dla lekcji "Wprowadzenie do neuroprzyw�dztwa" nie ma blokowania
                if lesson_title == "Wprowadzenie do neuroprzyw�dztwa" or quiz_passed:
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
                                show_xp_notification(xp_awarded, f"Zdoby�e� {xp_awarded} XP za wykonanie zada� praktycznych!")
                                
                                # Refresh user data for real-time updates
                                from utils.real_time_updates import refresh_user_data
                                refresh_user_data()
                            
                            # Przejd� do nast�pnego kroku
                            st.session_state.lesson_step = next_step
                            scroll_to_top()
                            st.rerun()
                else:                    # Quiz niezdany - zablokowany przycisk z komunikatem
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        zen_button(
                            f"?? Dalej: {step_names.get(next_step, next_step.capitalize())}",
                            disabled=True,
                            width='stretch',
                            help="Musisz zaliczy� quiz ko�cowy (min. 75%) aby przej�� do podsumowania"
                        )
                    st.warning("?? Aby przej�� do podsumowania, musisz najpierw zaliczy� quiz ko�cowy z wynikiem minimum 75%. Quiz znajdziesz w sekcji 'Praktyka' � '?? Quiz ko�cowy'.")
            else:
                # Normalny przycisk dla innych krok�w (nie-summary)
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
                            show_xp_notification(xp_awarded, f"Zdoby�e� {xp_awarded} XP za wykonanie zada� praktycznych!")
                            
                            # Refresh user data for real-time updates
                            from utils.real_time_updates import refresh_user_data
                            refresh_user_data()
                        
                        # Przejd� do nast�pnego kroku
                        st.session_state.lesson_step = next_step
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        elif st.session_state.lesson_step == 'summary':
            # Wy�wietl podsumowanie lekcji w podziale na zak�adki, podobnie jak wprowadzenie
            if 'summary' in lesson:
                # Sprawd� tytu� lekcji, aby ukry� niekt�re tabs dla konkretnych lekcji
                lesson_title = lesson.get("title", "")
                
                if lesson_title == "Wprowadzenie do neuroprzyw�dztwa":
                    # Dla tej lekcji pokazuj dwie zak�adki: Quiz Autodiagnozy i Podsumowanie
                    summary_tabs = tabs_with_fallback(["?? Quiz Autodiagnozy", "?? Podsumowanie"])
                    
                    with summary_tabs[0]:
                        # Wy�wietl quiz autodiagnozy
                        if 'closing_quiz' in lesson['summary']:
                            quiz_passed, can_continue, score = display_quiz(lesson['summary']['closing_quiz'])
                            
                            # Sprawd� czy quiz zosta� uko�czony
                            if quiz_passed:
                                success, fragment_xp = award_fragment_xp(lesson_id, 'closing_quiz', step_xp_values['summary'])
                                if success and fragment_xp > 0:
                                    st.success(f"? Quiz uko�czony! Zdoby�e� {fragment_xp} XP!")
                        else:
                            st.warning("Brak quizu autodiagnozy.")
                    
                    with summary_tabs[1]:
                        # Wy�wietl g��wne podsumowanie
                        if 'main' in lesson['summary']:
                            st.markdown(lesson['summary']['main'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak g��wnego podsumowania.")
                        
                        # Rekomendacje szkole� (ukryte - mo�liwo�� przywr�cenia w przysz�o�ci)
                        # try:
                        #     from utils.training_recommendations import display_training_recommendations, load_recommendations_styles
                        #     load_recommendations_styles()
                        #     
                        #     # Klucz wynik�w quizu autodiagnozy
                        #     quiz_results_key = "quiz_quiz_autodiagnozy_results"
                        #     display_training_recommendations(lesson_id, quiz_results_key)
                        #     
                        # except ImportError:
                        #     st.error("Modu� rekomendacji szkole� nie jest dost�pny.")
                        # except Exception as e:
                        # except Exception as e:
                        #     st.error(f"B��d podczas �adowania rekomendacji: {str(e)}")
                else:
                    # Dla wszystkich innych lekcji pokazuj pe�ne tabs
                    # Podziel podsumowanie na cztery zak�adki - dodajemy Cheatsheet
                    summary_tabs = tabs_with_fallback(["Podsumowanie", "Case Study", "??? Mapa my�li", "?? Cheatsheet"])
                    
                    with summary_tabs[0]:
                        # Wy�wietl g��wne podsumowanie
                        if 'main' in lesson['summary']:
                            st.markdown(lesson['summary']['main'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak g��wnego podsumowania.")
                    
                    with summary_tabs[1]:
                        # Wy�wietl studium przypadku
                        if 'case_study' in lesson['summary']:
                            st.markdown(lesson['summary']['case_study'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak studium przypadku w podsumowaniu.")
                
                    with summary_tabs[2]:
                        # Wy�wietl interaktywn� map� my�li
                        st.markdown("### ??? Interaktywna mapa my�li")
                        st.markdown("Poni�ej znajdziesz interaktywn� map� my�li podsumowuj�c� kluczowe koncepty z tej lekcji. Mo�esz klika� na w�z�y aby je przesuwa� i lepiej eksplorowa� powi�zania mi�dzy r�nymi tematami.")
                        
                        try:
                            from utils.mind_map import create_lesson_mind_map
                            mind_map_result = create_lesson_mind_map(lesson)
                            
                            if mind_map_result is None:
                                st.info("?? **Mapa my�li w przygotowaniu**\n\nDla tej lekcji przygotowujemy interaktywn� map� my�li, kt�ra pomo�e Ci lepiej zrozumie� powi�zania mi�dzy r�nymi konceptami. Wkr�tce b�dzie dost�pna!")
                        except Exception as e:
                            st.warning("?? Mapa my�li nie jest obecnie dost�pna. Sprawd�, czy wszystkie wymagane biblioteki s� zainstalowane.")
                            st.expander("Szczeg�y b��du (dla deweloper�w)").write(str(e))
                    
                    with summary_tabs[3]:
                        # Wy�wietl cheatsheet
                        if 'cheatsheet' in lesson['summary']:
                            st.markdown(lesson['summary']['cheatsheet'], unsafe_allow_html=True)
                            
                            # Dodaj przycisk do eksportu PDF (jak w Tools)
                            st.markdown("---")
                            
                            col_export, col_info = st.columns([1, 3])
                            with col_export:
                                # Przycisk PDF
                                if zen_button("?? Eksportuj PDF", key="export_cheatsheet_pdf"):
                                    try:
                                        from utils.cheatsheet_pdf_v5 import generate_cheatsheet_pdf
                                        
                                        username = getattr(st.session_state, 'username', 'U�ytkownik')
                                        lesson_title = lesson.get('title', 'Lekcja')
                                        cheatsheet_content = lesson['summary']['cheatsheet']
                                        
                                        # Generuj prawdziwy PDF (jak w Tools)
                                        pdf_data = generate_cheatsheet_pdf(
                                            lesson_title=lesson_title,
                                            cheatsheet_html=cheatsheet_content,
                                            username=username
                                        )
                                        
                                        # Przygotuj nazw� pliku
                                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                        lesson_id = lesson.get('id', 'lesson').replace(' ', '_')
                                        filename = f"cheatsheet_{lesson_id}_{timestamp}.pdf"
                                        
                                        st.download_button(
                                            label="?? Pobierz PDF",
                                            data=pdf_data,
                                            file_name=filename,
                                            mime="application/pdf",
                                            key="download_cheatsheet_pdf"
                                        )
                                        st.success("? Cheatsheet PDF gotowy do pobrania!")
                                        
                                    except Exception as e:
                                        st.error(f"? B��d podczas generowania PDF: {str(e)}")
                                        if st.session_state.get('debug_mode', False):
                                            import traceback
                                            st.expander("Szczeg�y b��du (dla deweloper�w)").code(traceback.format_exc())
                                
                                # Przycisk PNG
                                if zen_button("??? Eksportuj Obraz", key="export_cheatsheet_image"):
                                    try:
                                        from utils.cheatsheet_image_generator import generate_cheatsheet_image
                                        
                                        lesson_title = lesson.get('title', 'Lekcja')
                                        cheatsheet_content = lesson['summary']['cheatsheet']
                                        
                                        # Generuj obraz PNG
                                        image_data = generate_cheatsheet_image(
                                            lesson_title=lesson_title,
                                            cheatsheet_html=cheatsheet_content,
                                            format='png'
                                        )
                                        
                                        if image_data:
                                            # Przygotuj nazw� pliku
                                            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                                            lesson_id = lesson.get('id', 'lesson').replace(' ', '_')
                                            filename = f"cheatsheet_{lesson_id}_{timestamp}.png"
                                            
                                            st.download_button(
                                                label="?? Pobierz PNG",
                                                data=image_data,
                                                file_name=filename,
                                                mime="image/png",
                                                key="download_cheatsheet_image"
                                            )
                                            st.success("? Cheatsheet PNG gotowy do pobrania!")
                                        else:
                                            st.error("? Nie uda�o si� wygenerowa� obrazu")
                                        
                                    except Exception as e:
                                        st.error(f"? B��d podczas generowania obrazu: {str(e)}")
                                        if st.session_state.get('debug_mode', False):
                                            import traceback
                                            st.expander("Szczeg�y b��du (dla deweloper�w)").code(traceback.format_exc())
                            
                            with col_info:
                                st.info("?? Wybierz format: PDF lub Obraz (PNG)")
                        else:
                            st.warning("Brak cheatsheet w podsumowaniu.")

                # Wy�wietl ca�kowit� zdobyt� ilo�� XP
                total_xp = st.session_state.lesson_progress['total_xp_earned']
                # st.success(f"Gratulacje! Uko�czy�e� lekcj� i zdoby�e� ��cznie {total_xp} XP!")
                  # Sprawd� czy lekcja zosta�a ju� zako�czona
                lesson_finished = st.session_state.get('lesson_finished', False)
                
                if not lesson_finished:
                    # Pierwszy etap - przycisk "Zako�cz lekcj�"
                    st.markdown("<div class='next-button'>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if zen_button("?? Zako�cz lekcj�", width='stretch'):
                            # Sprawd� czy XP za podsumowanie ju� zosta�o przyznane
                            progress = get_lesson_fragment_progress(lesson_id)
                            if not progress.get('summary_completed', False):
                                success, xp_awarded = award_fragment_xp(lesson_id, 'summary', step_xp_values['summary'])
                                
                                if success and xp_awarded > 0:
                                    # Update session state for UI compatibility - usuni�to podw�jne ustawienie
                                    # award_fragment_xp ju� ustawia summary_completed
                                    st.session_state.lesson_progress['steps_completed'] += 1
                                    st.session_state.lesson_progress['total_xp_earned'] += xp_awarded
                                    
                                    # Show real-time XP notification
                                    show_xp_notification(xp_awarded, f"Zdoby�e� {xp_awarded} XP za uko�czenie podsumowania!")
                                    
                                    # Refresh user data for real-time updates
                                    from utils.real_time_updates import refresh_user_data
                                    refresh_user_data()
                                    
                                    # Sprawd� czy lekcja zosta�a uko�czona
                                    check_and_mark_lesson_completion(lesson_id)
                            
                            # Oznacz lekcj� jako zako�czon� i zapisz post�p
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
                                
                            # Show completion notification - wy�wietl faktyczne ca�kowite XP
                            final_total_xp = st.session_state.lesson_progress.get('total_xp_earned', 0)
                            show_xp_notification(0, f"?? Gratulacje! Uko�czy�e� ca�� lekcj� i zdoby�e� {final_total_xp} XP!")
                            
                            # Oznacz lekcj� jako zako�czon� w sesji
                            st.session_state.lesson_finished = True
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    # Drugi etap - poka� podsumowanie i przycisk powrotu
                    st.balloons()  # Animacja gratulacji
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                                color: white; padding: 20px; border-radius: 15px; margin: 20px 0;
                                text-align: center; box-shadow: 0 4px 15px rgba(76,175,80,0.3);">
                        <h2 style="margin: 0 0 10px 0;">?? Lekcja uko�czona!</h2>
                        <p style="margin: 0; font-size: 18px;">�wietna robota! Mo�esz teraz przej�� do kolejnych lekcji.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Przycisk powrotu do wszystkich lekcji
                    st.markdown("<div class='next-button'>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if zen_button("?? Wr�� do wszystkich lekcji", width='stretch'):
                            # Wyczy�� stan zako�czenia lekcji
                            st.session_state.lesson_finished = False
                            # Powr�t do przegl�du lekcji
                            st.session_state.current_lesson = None
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            elif 'outro' in lesson:
                # Backward compatibility - obs�uga starszego formatu outro - zakomentowano map� my�li
                lesson_title = lesson.get("title", "")
                
                if lesson_title == "Wprowadzenie do neuroprzyw�dztwa":
                    # Dla tej lekcji pokazuj tylko zak�adk� "Podsumowanie"
                    summary_tabs = tabs_with_fallback(["Podsumowanie"])
                    
                    with summary_tabs[0]:
                        # Wy�wietl g��wne podsumowanie
                        if 'main' in lesson['outro']:
                            st.markdown(lesson['outro']['main'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak g��wnego podsumowania.")
                else:
                    # Dla wszystkich innych lekcji pokazuj pe�ne tabs
                    summary_tabs = tabs_with_fallback(["Podsumowanie", "Case Study", "??? Mapa my�li"])
                    
                    with summary_tabs[0]:
                        # Wy�wietl g��wne podsumowanie
                        if 'main' in lesson['outro']:
                            st.markdown(lesson['outro']['main'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak g��wnego podsumowania.")
                    
                    with summary_tabs[1]:
                        # Wy�wietl studium przypadku
                        if 'case_study' in lesson['outro']:
                            st.markdown(lesson['outro']['case_study'], unsafe_allow_html=True)
                        else:
                            st.warning("Brak studium przypadku w podsumowaniu.")
                
                    with summary_tabs[2]:
                        # Wy�wietl interaktywn� map� my�li
                        st.markdown("### ??? Interaktywna mapa my�li")
                        st.markdown("Poni�ej znajdziesz interaktywn� map� my�li podsumowuj�c� kluczowe koncepty z tej lekcji. Mo�esz klika� na w�z�y aby je przesuwa� i lepiej eksplorowa� powi�zania mi�dzy r�nymi tematami.")
                        
                        try:
                            from utils.mind_map import create_lesson_mind_map
                            mind_map_result = create_lesson_mind_map(lesson)
                            
                            if mind_map_result is None:
                                st.info("?? **Mapa my�li w przygotowaniu**\n\nDla tej lekcji przygotowujemy interaktywn� map� my�li, kt�ra pomo�e Ci lepiej zrozumie� powi�zania mi�dzy r�nymi konceptami. Wkr�tce b�dzie dost�pna!")
                        except Exception as e:
                            st.warning("?? Mapa my�li nie jest obecnie dost�pna. Sprawd�, czy wszystkie wymagane biblioteki s� zainstalowane.")
                            st.expander("Szczeg�y b��du (dla deweloper�w)").write(str(e))
            else:
                # Brak podsumowania w danych lekcji
                st.error("Lekcja nie zawiera podsumowania!")
          # Zamknij div .st-bx
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Add live XP indicator - ZAKOMENTOWANE
        # live_xp_indicator()        # Show lesson progress with current XP system
        # Pobierz aktualne dane fragment�w
        fragment_progress = get_lesson_fragment_progress(lesson_id)
          # Synchronizuj stan sesji z rzeczywistymi danymi fragment�w
        for step in step_order:
            completed_key = f"{step}_completed"
            if completed_key in fragment_progress:
                st.session_state.lesson_progress[step] = fragment_progress[completed_key]
        
        # Oblicz zdobyte XP na podstawie rzeczywistych danych z systemu fragment�w
        current_xp = 0
        for step in step_order:
            step_xp_key = f"{step}_xp"
            if step_xp_key in fragment_progress:
                current_xp += fragment_progress[step_xp_key]
          # Oblicz aktualny post�p na podstawie XP (nie liczby krok�w)
        completion_percent = (current_xp / max_xp) * 100 if max_xp > 0 else 0
          # Przygotuj dane o kluczowych krokach do wy�wietlenia
        key_steps_info = []
        if 'intro' in step_order:
            completed = fragment_progress.get('intro_completed', False)
            key_steps_info.append(f"?? Intro: {step_xp_values['intro']} XP {'?' if completed else ''}")
        
        # opening_quiz usuni�te - jest teraz zintegrowane w zak�adce intro
        
        if 'content' in step_order:
            completed = fragment_progress.get('content_completed', False)
            key_steps_info.append(f"?? Tre��: {step_xp_values['content']} XP {'?' if completed else ''}")
        
        if 'practical_exercises' in step_order:
            completed = fragment_progress.get('practical_exercises_completed', False)
            key_steps_info.append(f"?? �wiczenia praktyczne: {step_xp_values['practical_exercises']} XP {'?' if completed else ''}")
        
        if 'reflection' in step_order:
            completed = fragment_progress.get('reflection_completed', False)
            key_steps_info.append(f"?? Refleksja: {step_xp_values['reflection']} XP {'?' if completed else ''}")
        
        if 'application' in step_order:
            completed = fragment_progress.get('application_completed', False)
            key_steps_info.append(f"?? Zadania: {step_xp_values['application']} XP {'?' if completed else ''}")
        
        if 'summary' in step_order:
            completed = fragment_progress.get('summary_completed', False)
            key_steps_info.append(f"?? Podsumowanie: {step_xp_values['summary']} XP {'?' if completed else ''}")
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; padding: 20px; margin-bottom: 20px; color: white;">
            <h3 style="margin: 0 0 10px 0;">?? {lesson.get('title', 'Lekcja')}</h3>
            <div style="background: rgba(255,255,255,0.2); border-radius: 10px; padding: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: bold;">Post�p lekcji: {completion_percent:.0f}%</span>
                    <span>?? {current_xp}/{max_xp} XP</span>
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
    """Wy�wietla lekcj� z nowymi sekcjami quiz�w"""
    
    # Wy�wietl tytu� lekcji
    st.markdown(f"<h1>{lesson_data['title']}</h1>", unsafe_allow_html=True)
    
    # Wy�wietl wprowadzenie
    if 'intro' in lesson_data:
        st.markdown(lesson_data['intro'], unsafe_allow_html=True)
    
    # Przygotuj dane zak�adek
    tab_data = []    # Dodaj zak�adki w odpowiedniej kolejno�ci (usuni�to opening_quiz - jest teraz w intro)
    
    if 'learning' in lesson_data.get('sections', {}):
        tab_data.append(("Nauka", "learning"))    
    if 'reflection' in lesson_data.get('sections', {}):
        tab_data.append(("Refleksja", "reflection"))
    
    # Wyodr�bnij tytu�y zak�adek
    tab_titles = [title for title, _ in tab_data]
    
    # Wy�wietl zak�adki tylko je�li s� jakie� dane do wy�wietlenia
    if tab_titles:
        tabs = tabs_with_fallback(tab_titles)        # Dla ka�dej zak�adki wy�wietl odpowiedni� zawarto��
        for i, (_, tab_name) in enumerate(tab_data):
            with tabs[i]:
                if tab_name == "learning":
                    display_learning_sections(lesson_data['sections'][tab_name])
                elif tab_name == "reflection":
                    display_reflection_sections(lesson_data['sections'][tab_name])
    else:
        st.warning("Ta lekcja nie zawiera �adnych sekcji do wy�wietlenia.")


# Dodanie brakuj�cych funkcji
def display_learning_sections(learning_data):
    """Wy�wietla sekcje nauki z lekcji"""
    if not learning_data or 'sections' not in learning_data:
        st.warning("Brak tre�ci edukacyjnych w tej lekcji.")
        return
        
    for section in learning_data['sections']:
        content_section(
            section.get("title", "Tytu� sekcji"), 
            section.get("content", "Brak tre�ci"), 
            collapsed=False
        )


def display_reflection_sections(reflection_data):
    """Wy�wietla sekcje refleksji z lekcji"""
    if not reflection_data:
        st.warning("Brak zada� refleksyjnych w tej lekcji.")
        return
        
    # Check if there are sections in the data
    if 'sections' not in reflection_data:
        st.warning("Dane refleksji nie zawieraj� sekcji.")
        return
        
    for section in reflection_data['sections']:
        st.markdown(f"### {section.get('title', 'Zadanie refleksyjne')}")
        st.markdown(section.get("content", "Brak tre�ci"), unsafe_allow_html=True)
        
        # Dodaj pole tekstowe do wprowadzania odpowiedzi
        reflection_key = f"reflection_{section.get('title', '').replace(' ', '_').lower()}"
        user_reflection = st.text_area(
            "Twoja odpowied�:",
            value=st.session_state.get(reflection_key, ""),
            height=200,
            key=reflection_key
        )
        
        # Dodaj przycisk do zapisywania odpowiedzi
        if st.button("Zapisz odpowied�", key=f"save_{reflection_key}"):
            st.session_state[reflection_key] = user_reflection
            st.success("Twoja odpowied� zosta�a zapisana!")

def display_quiz(quiz_data, passing_threshold=60):
    """Wy�wietla quiz z pytaniami i opcjami odpowiedzi. Zwraca True, gdy quiz jest uko�czony."""
    
    # Style CSS TYLKO dla przycisk�w odpowiedzi quiz - nie wp�ywa na nawigacj�
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
        st.warning("Ten quiz nie zawiera �adnych pyta�.")
        return False, False, 0
        
    st.markdown(f"<h2>{quiz_data.get('title', 'Quiz')}</h2>", unsafe_allow_html=True)
    
    if "description" in quiz_data:
        st.markdown(quiz_data['description'])
    
    # Sprawd� czy to quiz samodiagnozy (wszystkie correct_answer s� null)
    is_self_diagnostic = all(q.get('correct_answer') is None for q in quiz_data['questions'])
    
    quiz_id = f"quiz_{quiz_data.get('title', '').replace(' ', '_').lower()}"
    
    # Klucz dla zapisywania wynik�w w danych u�ytkownika
    results_key = f"{quiz_id}_results"
    
    # Sprawd� czy quiz zosta� ju� uko�czony i s� zapisane wyniki
    completed_quiz_data = None
    if 'user_data' in st.session_state and results_key in st.session_state.user_data:
        completed_quiz_data = st.session_state.user_data[results_key]
    
    # Przycisk "Przyst�p ponownie" je�li quiz by� ju� uko�czony
    if completed_quiz_data:
        st.markdown('<div class="quiz-results">', unsafe_allow_html=True)
        st.success(f"? Uko�czy�e� ju� ten quiz w dniu: {completed_quiz_data.get('completion_date', 'nieznana data')}")
        
        # Wy�wietl poprzednie wyniki
        if 'answers' in completed_quiz_data:
            with st.expander("?? Zobacz raport z quizu"):
                quiz_type = quiz_data.get('type', 'buttons')
                
                # Sprawd� czy mamy szczeg�owe wyniki
                if 'question_results' in completed_quiz_data:
                    # Nowy format z szczeg�owymi wynikami
                    question_results = completed_quiz_data['question_results']
                    total_points = completed_quiz_data.get('total_points', 0)
                    correct_answers = completed_quiz_data.get('correct_answers', 0)
                    
                    # Dla quiz�w autodiagnozy - najpierw spersonalizowane wyniki
                    if is_self_diagnostic:
                        quiz_title_lower = quiz_data.get('title', '').lower()
                        current_lesson_id = st.session_state.get('current_lesson', '')
                        
                        # Specjalny raport dla lekcji "Wprowadzenie do neuroprzyw�dztwa"
                        if ('quiz autodiagnozy' in quiz_title_lower and 
                            'wprowadzenie do neuroprzyw�dztwa' in current_lesson_id.lower()):
                            display_neuroleadership_autodiagnosis(quiz_data, completed_quiz_data['answers'])
                        
                        # Raport dla Conversational Intelligence
                        elif any([
                            'conversational intelligence' in quiz_title_lower,
                            'c-iq' in quiz_title_lower,
                            'od s��w do zaufania' in quiz_title_lower,
                            'jak wa�ne mo�e by�' in quiz_title_lower
                        ]):
                            display_self_diagnostic_results(quiz_data, completed_quiz_data['answers'])
                    
                    # Potem szczeg�owe wyniki quizu
                    display_quiz_results(quiz_data, question_results, total_points, correct_answers, is_self_diagnostic, quiz_type)
                
                else:
                    # Stary format - zachowaj kompatybilno��
                    if quiz_type == 'slider':
                        scale = quiz_data.get('scale', {'min': 1, 'max': 5})
                        labels = scale.get('labels', {})
                        
                        total_points = 0
                        for i, (question, answer) in enumerate(zip(quiz_data['questions'], completed_quiz_data['answers'])):
                            st.write(f"**Pytanie {i+1}:** {question['question']}")
                            answer_label = labels.get(str(answer), str(answer))
                            st.write(f"**Odpowied�:** {answer} - {answer_label}")
                            total_points += answer
                            st.markdown("---")
                        
                        st.info(f"**��czna suma punkt�w:** {total_points}/{len(quiz_data['questions']) * scale['max']}")
                    else:
                        # Stary format z opcjami
                        for i, (question, answer) in enumerate(zip(quiz_data['questions'], completed_quiz_data['answers'])):
                            st.write(f"**Pytanie {i+1}:** {question['question']}")
                            if isinstance(answer, int) and answer < len(question.get('options', [])):
                                st.write(f"**Odpowied�:** {question['options'][answer]}")
                            st.markdown("---")
        
        # Przycisk ponownego przyst�pienia na ko�cu
        st.markdown("---")
        help_text = "Mo�esz ponownie wype�ni� quiz aby zaktualizowa� swoj� autorefleksj�" if is_self_diagnostic else "Mo�esz ponownie przyst�pi� do quizu aby poprawi� sw�j wynik"
        if st.button("?? Przyst�p do quizu ponownie", key=f"{quiz_id}_restart", help=help_text):
            # Wyczy�� dane sesji dla tego quizu
            if quiz_id in st.session_state:
                del st.session_state[quiz_id]
            
            # Wyczy�� wszystkie klucze zwi�zane z tym quizem (suwaki, checkboxy, radio)
            keys_to_delete = []
            for key in st.session_state.keys():
                if isinstance(key, str) and key.startswith(f"{quiz_id}_"):
                    keys_to_delete.append(key)
            
            for key in keys_to_delete:
                del st.session_state[key]
            
            # Usu� wyniki z persistent storage
            if 'user_data' in st.session_state and results_key in st.session_state.user_data:
                del st.session_state.user_data[results_key]
            
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sprawd� czy quiz zosta� zdany na podstawie passing_threshold
        if is_self_diagnostic:
            # Quizy autodiagnozy zawsze zaliczone gdy uko�czone
            quiz_passed = True
        else:
            # Dla quiz�w testowych sprawd� wynik
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
        # Sprawd� czy liczba pyta� si� zmieni�a i dostosuj list� odpowiedzi
        expected_length = len(quiz_data['questions'])
        current_length = len(st.session_state[quiz_id]["answers"])
        
        if current_length != expected_length:
            # Dostosuj d�ugo�� listy odpowiedzi
            if current_length < expected_length:
                # Dodaj brakuj�ce None'y
                st.session_state[quiz_id]["answers"].extend([None] * (expected_length - current_length))
            else:
                # Obetnij list� do odpowiedniej d�ugo�ci
                st.session_state[quiz_id]["answers"] = st.session_state[quiz_id]["answers"][:expected_length]
    
    # Wy�wietl wszystkie pytania
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
            
            # Wy�wietl etykiety skali
            if 'labels' in scale:
                labels_html = "<div style='display: flex; justify-content: space-between; margin: 10px 0; font-size: 0.9em; color: #666;'>"
                for value in range(min_val, max_val + 1):
                    label = scale['labels'].get(str(value), str(value))
                    labels_html += f"<span><strong>{value}</strong>: {label}</span>"
                labels_html += "</div>"
                st.markdown(labels_html, unsafe_allow_html=True)
            
            # U�yj poprzedniej odpowiedzi jako warto�� domy�ln�, je�li istnieje
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
                help=f"Przesu� suwak, aby wybra� warto�� od {min_val} do {max_val}"
            )
            
            # Zapisz odpowied� w czasie rzeczywistym
            # Upewnij si�, �e lista jest wystarczaj�co d�uga przed zapisem
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
                
                # Upewnij si�, �e lista jest wystarczaj�co d�uga przed zapisem
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
                    "Wybierz odpowied�:",
                    options=range(len(question['options'])),
                    format_func=lambda x: question['options'][x],
                    index=current_answer if current_answer is not None else None,
                    key=f"{question_id}_radio"
                )
                
                # Upewnij si�, �e lista jest wystarczaj�co d�uga przed zapisem
                if i >= len(st.session_state[quiz_id]["answers"]):
                    st.session_state[quiz_id]["answers"].extend([None] * (i + 1 - len(st.session_state[quiz_id]["answers"])))
                
                st.session_state[quiz_id]["answers"][i] = selected_option
                if selected_option is None:
                    all_answered = False
        
        st.markdown("---")
    
    # Sprawd� czy wszystkie pytania zosta�y odpowiedziane
    for i, answer in enumerate(st.session_state[quiz_id]["answers"]):
        if answer is None or (isinstance(answer, list) and len(answer) == 0):
            all_answered = False
            break
    
    # Przycisk zatwierdzenia wszystkich odpowiedzi
    if all_answered:
        st.markdown('<div style="text-align: center; margin: 30px 0;">', unsafe_allow_html=True)
        if st.button("?? Zatwierd� wszystkie odpowiedzi", key=f"{quiz_id}_submit_all", help="Zatwierd� quiz i zapisz wyniki"):
            # Oblicz wyniki
            total_points = 0
            correct_answers = 0
            question_results = []  # Szczeg�owe wyniki dla ka�dego pytania
            
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
                        # Dla quiz�w autodiagnozy: opcje 0-4 = 1-5 punkt�w
                        if isinstance(answer, list):
                            points = sum(j + 1 for j in answer)
                            question_result['points_earned'] = points
                            total_points += points
                        else:
                            points = answer + 1
                            question_result['points_earned'] = points
                            total_points += points
                    else:
                        # Dla quiz�w testowych
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
            
            # Zapisz wyniki do danych u�ytkownika (persistent storage)
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
                'question_results': question_results  # Dodaj szczeg�owe wyniki
            }
            
            # Oznacz quiz jako uko�czony
            st.session_state[quiz_id]["completed"] = True
            st.session_state[quiz_id]["total_points"] = total_points
            st.session_state[quiz_id]["correct_answers"] = correct_answers  # Dodaj dla sprawdzania zaliczenia
            
            # Zaloguj uko�czenie quizu w systemie activity tracking
            try:
                from utils.activity_tracker import log_activity
                
                # Oblicz procent poprawnych odpowiedzi
                total_questions = len(quiz_data['questions'])
                score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 and not is_self_diagnostic else 0
                
                # Okre�l typ quizu
                if is_self_diagnostic:
                    quiz_category = 'self_diagnostic'
                elif 'opening' in quiz_id.lower() or quiz_id.startswith('opening'):
                    quiz_category = 'opening'
                elif 'closing' in quiz_id.lower() or quiz_id.startswith('closing'):
                    quiz_category = 'closing'
                else:
                    quiz_category = 'practice'
                
                # Sprawd� czy zdany (dla quiz�w testowych)
                passed = score_percentage >= passing_threshold if not is_self_diagnostic else True
                
                log_activity(st.session_state.username, 'quiz_completed', {
                    'quiz_id': quiz_id,
                    'quiz_title': quiz_data.get('title', 'Quiz'),
                    'quiz_category': quiz_category,
                    'total_questions': total_questions,
                    'correct_answers': correct_answers,
                    'score_percentage': round(score_percentage, 1),
                    'total_points': total_points,
                    'passed': passed,
                    'passing_threshold': passing_threshold,
                    'is_self_diagnostic': is_self_diagnostic
                })
            except Exception as e:
                # Nie przerywaj procesu je�li tracking nie dzia�a
                print(f"Warning: Could not log quiz completion: {e}")
            
            st.success(f"? Quiz zosta� uko�czony! Twoje wyniki zosta�y zapisane.")
            
            # Dla quiz�w autodiagnozy wy�wietl spersonalizowane wyniki je�li dost�pne
            if is_self_diagnostic and 'results_interpretation' in quiz_data:
                try:
                    display_self_diagnostic_results(quiz_data, st.session_state[quiz_id]["answers"])
                except Exception as e:
                    st.error(f"B��d podczas wy�wietlania spersonalizowanych wynik�w: {e}")
            
            # Wy�wietl szczeg�owe wyniki quizu
            display_quiz_results(quiz_data, question_results, total_points, correct_answers, is_self_diagnostic, quiz_type)
            
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("?? Odpowiedz na wszystkie pytania, aby m�c zatwierdzi� quiz.")
    
    # Zwr�� status uko�czenia
    quiz_completed = st.session_state[quiz_id].get("completed", False)
    earned_points = st.session_state[quiz_id].get("total_points", 0)
    
    # Sprawd� czy quiz zosta� zdany na podstawie passing_threshold
    if quiz_completed:
        if is_self_diagnostic:
            # Quizy autodiagnozy zawsze zaliczone gdy uko�czone
            quiz_passed = True
        else:
            # Dla quiz�w testowych sprawd� wynik z saved data
            if completed_quiz_data and 'correct_answers' in completed_quiz_data:
                correct = completed_quiz_data['correct_answers']
                total = len(quiz_data['questions'])
                percentage = (correct / total) * 100 if total > 0 else 0
                quiz_passed = percentage >= passing_threshold
            else:
                # Fallback - sprawd� current session state
                correct = st.session_state[quiz_id].get("correct_answers", 0)
                total = st.session_state[quiz_id].get("total_questions", len(quiz_data['questions']))
                percentage = (correct / total) * 100 if total > 0 else 0
                quiz_passed = percentage >= passing_threshold
    else:
        quiz_passed = False
    
    return quiz_completed, quiz_passed, earned_points


def check_lesson_prerequisites(lesson_id, user_progress):
    """
    Sprawdza czy u�ytkownik ma wymagane wyniki z poprzednich lekcji
    """
    # Pobierz ustawienia wymaga� dla lekcji
    lesson_requirements = get_lesson_requirements(lesson_id)
    
    if not lesson_requirements:
        return True  # Brak wymaga� = dost�p dozwolony
    
    for requirement in lesson_requirements:
        required_lesson = requirement.get('lesson')
        required_score = requirement.get('min_score', 0)
        
        # Sprawd� wynik z wymaganej lekcji
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
    # W przysz�o�ci mo�na to przenie�� do pliku konfiguracyjnego
    requirements = {
        "1": [],  # Pierwsza lekcja - brak wymaga�
        "2": [{"lesson": "1", "min_score": 60}],  # Druga lekcja wymaga 60% z pierwszej
        "3": [{"lesson": "2", "min_score": 60}],  # itd.
    }
    
    return requirements.get(lesson_id, [])
    
    # Wy�wietl wszystkie pytania
    for i, question in enumerate(quiz_data['questions']):
        question_id = f"{quiz_id}_q{i}"
        
        # Kontener dla pytania z w�asnymi stylami
        st.markdown(f"""
        <div class="quiz-question">
            <h3>Pytanie {i+1}: {question['question']}</h3>
        </div>
        """, unsafe_allow_html=True)          # Je�li pytanie ju� zosta�o odpowiedziane, poka� wynik
        if i in st.session_state[quiz_id]["answered_questions"]:
            selected = st.session_state.get(f"{question_id}_selected")
            question_type = question.get('type', 'single_choice')
            quiz_type = quiz_data.get('type', 'buttons')
            
            # Obs�uga wy�wietlania odpowiedzi dla suwak�w
            if quiz_type == 'slider' or question_type == 'slider':
                scale = quiz_data.get('scale', {'min': 1, 'max': 5})
                labels = scale.get('labels', {})
                selected_label = labels.get(str(selected), str(selected))
                
                st.markdown(f"? **Twoja odpowied�: {selected} - {selected_label}**")
                
                # Wy�wietl skal� dla kontekstu
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
                # Wy�wietl odpowiedzi z oznaczeniem poprawnej (stary kod)
                for j, option in enumerate(question['options']):
                    # Dla quiz�w samodiagnozy - wszystkie opcje r�wne
                    if is_self_diagnostic:
                        if isinstance(selected, list):
                            # Wielokrotny wyb�r w samodiagnozie (rzadko u�ywane)
                            if j in selected:
                                st.markdown(f"? **{option}** _(Twoja odpowied�)_")
                            else:
                                st.markdown(f"0 {option}")
                        else:
                            # Pojedynczy wyb�r w samodiagnozie
                            if j == selected:
                                st.markdown(f"? **{option}** _(Twoja odpowied�)_")
                            else:
                                st.markdown(f"0 {option}")
                    else:
                        # Dla quiz�w z poprawnymi odpowiedziami
                        if question_type == 'multiple_choice':
                            # Pytania z wielokrotnym wyborem
                            correct_answers = question.get('correct_answers', [])
                            selected_list = selected if isinstance(selected, list) else []
                            
                            if j in correct_answers and j in selected_list:
                                st.markdown(f"? **{option}** _(Poprawna odpowied� - wybrana)_")
                            elif j in correct_answers and j not in selected_list:
                                st.markdown(f"? **{option}** _(Poprawna odpowied� - nie wybrana)_")
                            elif j not in correct_answers and j in selected_list:
                                st.markdown(f"? **{option}** _(Niepoprawna odpowied� - wybrana)_")
                            else:
                                st.markdown(f"0 {option}")
                        else:
                            # Pytania z pojedynczym wyborem
                            correct_answer = question.get('correct_answer')
                            is_correct = correct_answer is not None and selected == correct_answer
                            
                            if correct_answer is not None:
                                if j == correct_answer:
                                    st.markdown(f"? **{option}** _(Poprawna odpowied�)_")
                                elif j == selected and not is_correct:
                                    st.markdown(f"? **{option}** _(Twoja odpowied�)_")
                                else:
                                    st.markdown(f"0 {option}")
                            else:
                                st.markdown(f"0 {option}")
              # Wy�wietl wyja�nienie
            if "explanation" in question:
                st.info(question['explanation'])
            
            st.markdown("---")
        else:
            # Okre�l typ quizu i u�yj odpowiedniej klasy CSS
            quiz_type_class = "self-reflection-quiz" if is_self_diagnostic else "test-quiz"
            
            # Rozpocznij sekcj� przycisk�w odpowiedzi quiz z odpowiedni� klas�
            st.markdown(f'<div class="quiz-answers-section {quiz_type_class}">', unsafe_allow_html=True)
            
            # Sprawd� czy to quiz ze suwakami
            question_type = question.get('type', 'single_choice')
            quiz_type = quiz_data.get('type', 'buttons')
            
            if quiz_type == 'slider' or question_type == 'slider':
                # Quiz ze suwakami
                scale = quiz_data.get('scale', {'min': 1, 'max': 5})
                min_val = scale['min']
                max_val = scale['max']
                default_val = question.get('default', (min_val + max_val) // 2)
                
                # Wy�wietl etykiety skali
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
                    help=f"Przesu� suwak, aby wybra� warto�� od {min_val} do {max_val}"
                )
                
                # Przycisk zatwierdzenia
                if st.button("Zatwierd� odpowied�", key=f"{question_id}_submit_slider"):
                    # Zapisz wybran� warto��
                    st.session_state[f"{question_id}_selected"] = selected_value
                    st.session_state[quiz_id]["answered_questions"].append(i)
                    
                    # Dla quiz�w samodiagnozy - zlicz punkty
                    if "total_points" not in st.session_state[quiz_id]:
                        st.session_state[quiz_id]["total_points"] = 0
                    st.session_state[quiz_id]["total_points"] += selected_value
                    
                    if len(st.session_state[quiz_id]["answered_questions"]) == st.session_state[quiz_id]["total_questions"]:
                        st.session_state[quiz_id]["completed"] = True
                    
                    st.rerun()
                    return False, False, 0
                    
            elif is_self_diagnostic:
                # Quiz autorefleksji - przyciski kr�tkie, dopasowane do tre�ci
                for j, option in enumerate(question['options']):
                    # Ka�dy przycisk w osobnej kolumnie o minimalnej szeroko�ci
                    col1, col2 = st.columns([1, 3])  # Pierwsza kolumna ma�a, druga wi�ksza ale niewykorzystana
                    
                    with col1:
                        if st.button(option, key=f"{question_id}_opt{j}"):
                            # Zapisz wybran� odpowied�
                            st.session_state[f"{question_id}_selected"] = j
                            st.session_state[quiz_id]["answered_questions"].append(i)                            # Dla quiz�w samodiagnozy - zlicz punkty (opcje 1-5 = j+1 punkt�w)
                            points = j + 1
                            if "total_points" not in st.session_state[quiz_id]:
                                st.session_state[quiz_id]["total_points"] = 0
                            st.session_state[quiz_id]["total_points"] += points
                            if len(st.session_state[quiz_id]["answered_questions"]) == st.session_state[quiz_id]["total_questions"]:
                                st.session_state[quiz_id]["completed"] = True
                                # Usuni�to opening_quiz handling - jest teraz zintegrowane w intro
                            st.rerun()
                            return False, False, 0
            else:
                # Quiz testowy - przyciski pe�nej szeroko�ci
                question_type = question.get('type', 'single_choice')
                if question_type == 'multiple_choice':
                    # Pytanie z wielokrotnym wyborem
                    st.write("**Wybierz wszystkie poprawne odpowiedzi:**")
                    
                    # Zbierz aktualny stan checkbox�w
                    for j, option in enumerate(question['options']):
                        checkbox_key = f"{question_id}_opt{j}"
                        st.checkbox(option, key=checkbox_key)
                    
                    # Przycisk do zatwierdzenia odpowiedzi z unikatowym kluczem
                    submit_key = f"{question_id}_submit"
                      # Przycisk do zatwierdzenia odpowiedzi
                    if st.button("Zatwierd� odpowiedzi", key=submit_key):
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
                        st.warning("Wybierz przynajmniej jedn� odpowied� przed zatwierdzeniem.")
                else:
                    # Pytanie z pojedynczym wyborem (domy�lne)
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
    
    # Sprawd� czy quiz jest uko�czony i oblicz punkty
    is_completed = st.session_state[quiz_id].get("completed", False)
    
    if is_completed:
        if is_self_diagnostic:
            # Quiz samodiagnozy - wy�wietl punkty i interpretacj�
            total_points = st.session_state[quiz_id].get("total_points", 0)
            
            # Oblicz maksymalne mo�liwe punkty (liczba pyta� � 5)
            max_possible_points = len(quiz_data['questions']) * 5;
            
            st.markdown(f"""
            <div class="quiz-summary">
                <h3>?? Tw�j wynik: {total_points}/{max_possible_points} punkt�w</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Wy�wietl interpretacj� wynik�w je�li dost�pna
            if 'scoring' in quiz_data and 'interpretation' in quiz_data['scoring']:
                interpretation_found = False
                for score_range, interpretation in quiz_data['scoring']['interpretation'].items():
                    # Parsuj zakres punkt�w (np. "10-20", "21-35", "36-50")
                    if '-' in score_range:
                        min_score, max_score = map(int, score_range.split('-'))
                        if min_score <= total_points <= max_score:
                            st.success(f"?? **Interpretacja wynik�w:**\n\n{interpretation}")
                            interpretation_found = True
                            break
                
                if not interpretation_found:
                    st.info("?? Dzi�kujemy za szczer� samorefleksj�! Twoje odpowiedzi pomog� nam lepiej dopasowa� materia� do Twojego stylu inwestowania.")
            else:
                st.info("?? Dzi�kujemy za szczer� samorefleksj�! Twoje odpowiedzi pomog� nam lepiej dopasowa� materia� do Twojego stylu inwestowania.")
              # Zawsze "zdany" dla quizu samodiagnozy
            return is_completed, True, total_points
            
        else:            # Standardowy quiz z poprawnymi odpowiedziami
            correct = st.session_state[quiz_id]["correct_answers"]
            total = st.session_state[quiz_id]["total_questions"]
            percentage = (correct / total) * 100
            
            # Oblicz punkty - warto�� zale�y od procentu odpowiedzi poprawnych
            quiz_xp_value = 15
            earned_points = int(quiz_xp_value * (percentage / 100))
            
            # Czy quiz zosta� zdany (na podstawie passing_threshold)
            is_passed = percentage >= passing_threshold
            
            st.markdown(f"""
            <div class="quiz-summary">
                <h3>Tw�j wynik: {correct}/{total} ({percentage:.0f}%)</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Wy�wietl interpretacj� wynik�w je�li dost�pna (nowy system)
            if 'result_interpretation' in quiz_data:
                interpretation_found = False
                interpretations = quiz_data['result_interpretation']
                
                # Sprawd� ka�dy pr�g interpretacji od najwy�szego do najni�szego
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
                    # Fallback do standardowych komunikat�w
                    if percentage >= 80:
                        st.success("�wietnie! Doskonale rozumiesz ten temat.")
                    elif percentage >= passing_threshold:
                        if passing_threshold > 60:
                            st.success(f"Bardzo dobrze! Osi�gn��e� wymagany pr�g {passing_threshold}% i mo�esz kontynuowa�.")
                        else:
                            st.success("Bardzo dobrze! Mo�esz kontynuowa� nauk�.")
                    else:
                        if passing_threshold > 60:
                            st.error(f"Aby przej�� dalej, musisz uzyska� przynajmniej {passing_threshold}% poprawnych odpowiedzi. Spr�buj ponownie!")
                        else:
                            st.warning("Spr�buj jeszcze raz - mo�esz to zrobi� lepiej!")
            else:
                # Standardowe komunikaty je�li brak interpretacji
                if percentage >= 80:
                    st.success("�wietnie! Doskonale rozumiesz ten temat.")
                elif percentage >= passing_threshold:
                    if passing_threshold > 60:
                        st.success(f"Bardzo dobrze! Osi�gn��e� wymagany pr�g {passing_threshold}% i mo�esz kontynuowa�.")
                    else:
                        st.success("Bardzo dobrze! Mo�esz kontynuowa� nauk�.")
                else:
                    if passing_threshold > 60:
                        st.error(f"Aby przej�� dalej, musisz uzyska� przynajmniej {passing_threshold}% poprawnych odpowiedzi. Spr�buj ponownie!")
                    else:
                        st.warning("Spr�buj jeszcze raz - mo�esz to zrobi� lepiej!")
            
            return is_completed, is_passed, earned_points
    
    # Quiz nie jest jeszcze uko�czony
    return is_completed, False, 0


def display_neuroleadership_autodiagnosis(quiz_data, answers):
    """Wy�wietla szczeg�owy raport autodiagnozy dla lekcji 'Wprowadzenie do neuroprzyw�dztwa'"""
    
    # Mapowanie pyta� na zagadnienia
    topics = [
        "Kontrola emocji i podejmowanie decyzji",
        "Neurotransmitery i motywacja zespo�u", 
        "Model SCARF - 5 potrzeb m�zgu",
        "Model SEEDS - pozytywne �rodowisko",
        "Zarz�dzanie stresem i odporno��",
        "Podejmowanie decyzji i ryzyko",
        "Koncentracja, pami�� i wydajno��",
        "Zdrowie i kondycja m�zgu",
        "Neuroplastyczno�� i nawyki",
        "Zastosowanie w wyzwaniach mened�erskich"
    ]
    
    # Mapowanie warto�ci na interpretacje
    value_interpretations = {
        5: {"label": "Bardzo wa�ne", "color": "#d32f2f", "priority": "PRIORYTET 1"},
        4: {"label": "Raczej wa�ne", "color": "#f57c00", "priority": "PRIORYTET 2"}, 
        3: {"label": "Trudno powiedzie�", "color": "#616161", "priority": "DO PRZEMY�LENIA"},
        2: {"label": "Raczej niewa�ne", "color": "#388e3c", "priority": "MNIEJSZA WAGA"},
        1: {"label": "W og�le niewa�ne", "color": "#1976d2", "priority": "NISKI PRIORYTET"}
    }
    
    st.markdown("### ?? Tw�j Profil Rozwojowy w Neuroprzyw�dztwie")
    st.markdown("Na podstawie Twoich odpowiedzi przygotowali�my spersonalizowany raport pokazuj�cy, kt�re zagadnienia z neuroprzyw�dztwa s� dla Ciebie najwa�niejsze.")
    
    # Sortuj zagadnienia wed�ug wa�no�ci (od najwy�szej do najni�szej)
    topic_scores = list(zip(topics, answers))
    topic_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Grupuj zagadnienia wed�ug priorytet�w
    priority_groups = {
        "PRIORYTET 1": [],
        "PRIORYTET 2": [],
        "DO PRZEMY�LENIA": [],
        "MNIEJSZA WAGA": [],
        "NISKI PRIORYTET": []
    }
    
    for topic, score in topic_scores:
        priority = value_interpretations[score]["priority"]
        priority_groups[priority].append((topic, score))
    
    # Wy�wietl ka�d� grup� priorytet�w
    for priority_name, group_topics in priority_groups.items():
        if group_topics:  # Tylko je�li grupa nie jest pusta
            if priority_name == "PRIORYTET 1":
                st.markdown(f"#### ?? {priority_name} - Zagadnienia kluczowe dla Twojego rozwoju")
                st.markdown("Te obszary wymagaj� Twojej szczeg�lnej uwagi i mog� przynie�� najwi�ksze korzy�ci w Twojej pracy mened�erskiej.")
            elif priority_name == "PRIORYTET 2":
                st.markdown(f"#### ? {priority_name} - Wa�ne obszary rozwoju")
                st.markdown("Te zagadnienia r�wnie� zas�uguj� na uwag� i mog� znacz�co wp�yn�� na Twoj� skuteczno�� jako lidera.")
            elif priority_name == "DO PRZEMY�LENIA":
                st.markdown(f"#### ?? {priority_name}")
                st.markdown("W tych obszarach warto pog��bi� wiedz�, aby lepiej oceni� ich znaczenie dla Twojej pracy.")
            elif priority_name == "MNIEJSZA WAGA":
                st.markdown(f"#### ? {priority_name}")
                st.markdown("Te zagadnienia mog� by� mniej priorytetowe w Twoim obecnym kontek�cie zawodowym.")
            else:  # NISKI PRIORYTET
                st.markdown(f"#### ?? {priority_name}")
                st.markdown("Te obszary obecnie nie stanowi� dla Ciebie wyzwania.")
            
            for topic, score in group_topics:
                interpretation = value_interpretations[score]
                st.markdown(f"""
                <div style='background: linear-gradient(90deg, {interpretation['color']}15 0%, {interpretation['color']}05 100%); 
                           padding: 15px; border-radius: 8px; margin: 8px 0; 
                           border-left: 4px solid {interpretation['color']};'>
                    <strong style='color: {interpretation['color']};'>{topic}</strong><br>
                    <span style='color: #666; font-size: 0.9rem;'>Ocena: {score}/5 - {interpretation['label']}</span>
                </div>
                """, unsafe_allow_html=True)
    
    # Podsumowanie i rekomendacje
    high_priority_count = len(priority_groups["PRIORYTET 1"]) + len(priority_groups["PRIORYTET 2"])
    
    st.markdown("---")
    st.markdown("### ?? Rekomendacje dla Twojego rozwoju")
    
    if high_priority_count >= 7:
        st.info("""
        ?? **Kompleksowy rozw�j:** Identyfikujesz wiele obszar�w jako wa�ne. Rozwa� systematyczne przej�cie przez ca�y kurs, 
        koncentruj�c si� szczeg�lnie na zagadnieniach oznaczonych jako Priorytet 1.
        """)
    elif high_priority_count >= 4:
        st.info("""
        ? **Ukierunkowany rozw�j:** Masz wyra�nie zdefiniowane priorytety. Skup si� na zagadnieniach z najwy�sz� ocen� 
        i stopniowo rozszerzaj wiedz� o pozosta�e obszary.
        """)
    else:
        st.info("""
        ?? **Selektywny rozw�j:** Identyfikujesz konkretne obszary do rozwoju. To dobra strategia - skup si� na tych 
        zagadnieniach, kt�re s� dla Ciebie najbardziej istotne.
        """)
    
    # Nast�pne kroki
    if priority_groups["PRIORYTET 1"]:
        st.markdown("#### ?? Sugerowane kolejne kroki:")
        st.markdown("1. **Zacznij od zagadnie� Priorytetu 1** - te obszary mog� przynie�� Ci najwi�ksze korzy�ci")
        st.markdown("2. **Przejd� przez odpowiednie lekcje kursu** - ka�de zagadnienie ma dedykowan� lekcj� z praktycznymi �wiczeniami")
        st.markdown("3. **Zastosuj wiedz� w praktyce** - po ka�dej lekcji wypr�buj poznane techniki w swojej pracy")
        st.markdown("4. **Wr�� do autodiagnozy za 3-6 miesi�cy** - sprawd� jak zmieni�a si� Twoja perspektywa")


def display_self_diagnostic_results(quiz_data, answers):
    """Uniwersalna funkcja do wy�wietlania wynik�w quiz�w autodiagnozy na podstawie konfiguracji z JSON"""
    
    if 'results_interpretation' not in quiz_data:
        st.info("Brak konfiguracji wynik�w dla tego quizu samodiagnozy.")
        return
    
    interpretation = quiz_data['results_interpretation']
    
    st.markdown("---")
    st.markdown("## ?? Twoje spersonalizowane wyniki")
    
    # Oblicz wynik na podstawie tej samej metody co g��wny system
    # Opcje 0-4 = 1-5 punkt�w (answer + 1)
    total_score = sum(answer + 1 for answer in answers)
    
    # Znajd� odpowiedni poziom wynik�w
    matching_level = None
    for level in interpretation['levels']:
        if level['min_score'] <= total_score <= level['max_score']:
            matching_level = level
            break
    
    if not matching_level:
        st.error(f"Nie znaleziono odpowiedniego poziomu dla wyniku: {total_score}")
        return
    
    # Okre�l kolor na podstawie nazwy poziomu
    color_map = {
        "Bardzo wysoka": "#e53e3e",  # czerwony
        "Wysoka": "#dd6b20",         # pomara�czowy  
        "�rednia": "#3182ce",        # niebieski
        "Niska": "#38a169"           # zielony
    }
    level_color = color_map.get(matching_level['name'], "#3182ce")
    
    # G��wny wynik
    relevance_icons = {
        "Bardzo wysoka": "??",
        "Wysoka": "?", 
        "�rednia": "??",
        "Niska": "??"
    }
    icon = relevance_icons.get(matching_level['name'], "??")
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {level_color} 0%, {level_color}CC 100%); 
                padding: 25px; border-radius: 15px; margin: 20px 0; color: white; text-align: center;'>
        <h2 style='margin: 0; color: white;'>{icon} ISTOTNO��: {matching_level['name'].upper()}</h2>
        <p style='font-size: 1.2rem; margin: 15px 0; opacity: 0.9;'>
            Wynik: <strong>{total_score}/{len(answers) * 4}</strong> punkt�w
        </p>
        <p style='font-size: 1rem; margin: 0; opacity: 0.8;'>
            Poziom istotno�ci tematyki lekcji dla Twoich potrzeb zawodowych
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Szczeg�owa analiza
    st.markdown(f"### {matching_level['title']}")
    st.markdown(matching_level['description'])
    
    # Kluczowe wnioski
    if 'insights' in matching_level and matching_level['insights']:
        st.markdown("#### ?? Kluczowe wnioski dla Ciebie:")
        for insight in matching_level['insights']:
            st.markdown(f"� {insight}")
    
    # Rekomendacje
    if 'recommendations' in matching_level and matching_level['recommendations']:
        st.markdown("#### ?? Konkretne rekomendacje:")
        for i, recommendation in enumerate(matching_level['recommendations'], 1):
            st.markdown(f"{i}. {recommendation}")
    
    # Nast�pne kroki
    if 'next_steps' in matching_level:
        st.markdown("#### ?? Twoje nast�pne kroki:")
        st.info(matching_level['next_steps'])


def display_conversational_intelligence_results(answers, questions):
    """Wy�wietla spersonalizowane wyniki quizu samodiagnozy dla Conversational Intelligence"""
    
    st.markdown("---")
    st.markdown("## ?? Twoje spersonalizowane wyniki")
    
    # Oblicz punkty dla ka�dej kategorii
    high_relevance_count = sum(1 for answer in answers if answer >= 2)  # odpowiedzi 2 i 3 (indeksy)
    medium_relevance_count = sum(1 for answer in answers if answer == 1)  # odpowied� 1 (indeks)
    low_relevance_count = sum(1 for answer in answers if answer == 0)  # odpowied� 0 (indeks)
    
    total_questions = len(questions)
    high_percentage = (high_relevance_count / total_questions) * 100
    
    # Okre�l poziom relevantno�ci
    if high_percentage >= 75:
        relevance_level = "BARDZO WYSOKA"
        relevance_color = "#d32f2f"
        relevance_icon = "??"
    elif high_percentage >= 50:
        relevance_level = "WYSOKA"
        relevance_color = "#f57c00"
        relevance_icon = "?"
    elif high_percentage >= 25:
        relevance_level = "�REDNIA"
        relevance_color = "#1976d2"
        relevance_icon = "??"
    else:
        relevance_level = "NISKA"
        relevance_color = "#388e3c"
        relevance_icon = "?"
    
    # G��wny wynik
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {relevance_color} 0%, {relevance_color}CC 100%); 
                padding: 25px; border-radius: 15px; margin: 20px 0; color: white; text-align: center;'>
        <h2 style='margin: 0; color: white;'>{relevance_icon} RELEVANTNO��: {relevance_level}</h2>
        <p style='font-size: 1.2rem; margin: 15px 0; opacity: 0.9;'>
            Conversational Intelligence ma dla Ciebie <strong>{relevance_level.lower()}</strong> warto�� praktyczn�
        </p>
        <p style='font-size: 1rem; margin: 0; opacity: 0.8;'>
            {high_relevance_count}/{total_questions} obszar�w wskazuje na wysok� potrzeb� rozwoju C-IQ
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Szczeg�owa analiza na podstawie odpowiedzi
    if high_percentage >= 75:
        st.markdown("""
        ### ?? Conversational Intelligence to dla Ciebie GAME CHANGER!
        
        **Twoja diagnoza pokazuje, �e:**
        - Borykasz si� z wyzwaniami komunikacyjnymi, kt�re wp�ywaj� na Twoje cele zawodowe
        - Umiej�tno�ci C-IQ mog� by� kluczem do prze�omu w Twoim przyw�dztwie
        - Inwestycja w rozw�j inteligencji konwersacyjnej mo�e przynie�� Ci bardzo szybkie i wymierne korzy�ci
        
        **Priorytetowe obszary rozwoju dla Ciebie:**
        ? **Natychmiastowe zastosowanie** - rozpocznij od jednej trudnej rozmowy tygodniowo  
        ? **G��bokie studiowanie** - przeanalizuj wszystkie poziomy rozm�w w praktyce  
        ? **Feedback od zespo�u** - popro� o ocen�, jak zmienia si� atmosfera rozm�w  
        """)
        
    elif high_percentage >= 50:
        st.markdown("""
        ### ? Conversational Intelligence to solidna inwestycja w Tw�j rozw�j
        
        **Twoja diagnoza pokazuje, �e:**
        - Masz kilka obszar�w, gdzie C-IQ mo�e realnie pom�c
        - Widzisz potencja� w lepszych rozmowach dla osi�gni�cia cel�w
        - Rozw�j tych umiej�tno�ci mo�e wzmocni� Twoje mocne strony przyw�dcze
        
        **Rekomendowany plan rozwoju:**
        ? **Stopniowe wdra�anie** - wybierz 2-3 techniki C-IQ do praktykowania  
        ? **Obserwacja rezultat�w** - monitoruj jak zmieniaj� si� Twoje relacje  
        ? **Eksperymentowanie** - testuj r�ne poziomy rozm�w w bezpiecznych sytuacjach  
        """)
        
    elif high_percentage >= 25:
        st.markdown("""
        ### ?? Conversational Intelligence to u�yteczne uzupe�nienie Twoich umiej�tno�ci
        
        **Twoja diagnoza pokazuje, �e:**
        - Masz solidne podstawy komunikacyjne
        - C-IQ mo�e pom�c w kilku konkretnych sytuacjach
        - B�dzie to raczej rozwijanie istniej�cych mocnych stron ni� radykalna zmiana
        
        **Sugerowane podej�cie:**
        ? **Selektywne uczenie** - skup si� na technikach najbardziej przydatnych w Twojej roli  
        ? **Praktyczne zastosowanie** - u�ywaj C-IQ w konkretnych, trudnych sytuacjach  
        ? **Mentoring innych** - przekazuj te umiej�tno�ci cz�onkom zespo�u  
        """)
        
    else:
        st.markdown("""
        ### ? Masz ju� solidne fundamenty - C-IQ to opcjonalne wzbogacenie
        
        **Twoja diagnoza pokazuje, �e:**
        - Prawdopodobnie ju� stosujesz wiele zasad C-IQ intuicyjnie
        - Twoje obecne podej�cie do komunikacji jest skuteczne
        - C-IQ mo�e s�u�y� g��wnie jako systematyzacja wiedzy, kt�r� ju� posiadasz
        
        **Zalecenia:**
        ? **�wiadome stosowanie** - nadaj nazwy temu, co ju� robisz dobrze  
        ? **Dzielenie si� wiedz�** - ucz innych skutecznych wzorc�w komunikacji  
        ? **Ci�g�e doskonalenie** - stosuj C-IQ w wyj�tkowo trudnych sytuacjach  
        """)
    
    # Kluczowe wnioski i nast�pne kroki
    st.markdown("### ?? Twoje nast�pne kroki")
    
    # Analizuj konkretne odpowiedzi i daj spersonalizowane wskaz�wki
    problem_areas = []
    for i, answer in enumerate(answers):
        if answer >= 2:  # Wysokie wskazanie potrzeby
            if i == 0:
                problem_areas.append("**Defensywno�� rozm�wc�w** - ludzie cz�sto si� 'zamykaj�' w rozmowach z Tob�")
            elif i == 1:
                problem_areas.append("**Budowanie zaufania** - Twoje cele zawodowe silnie zale�� od jako�ci relacji")
            elif i == 2:
                problem_areas.append("**Motywowanie zespo�u** - tracisz energi� na napi�cia komunikacyjne")
            elif i == 3:
                problem_areas.append("**Zarz�dzanie konfliktem** - konflikty eskaluj� zamiast si� konstruktywnie rozwi�zywa�")
            elif i == 4:
                problem_areas.append("**Konstruktywny feedback** - Twoje uwagi wywo�uj� op�r zamiast motywowa�")
            elif i == 5:
                problem_areas.append("**Wsp�tworzenie** - widzisz potencja� w przej�ciu od przekonywania do wsp�pracy")
            elif i == 6:
                problem_areas.append("**Kultura zespo�u** - chcesz aktywnie wp�ywa� na atmosfer� przez rozmowy")
            elif i == 7:
                problem_areas.append("**Filozofia 'mikrozmian'** - inspiruje Ci� idea transformacji przez codzienne interakcje")
    
    if problem_areas:
        st.markdown("**Twoje priorytetowe obszary rozwoju:**")
        for area in problem_areas:
            st.markdown(f"� {area}")
    
    # Konkretne rekomendacje akcji
    st.markdown("""
    ### ?? Konkretne akcje na najbli�szy tydzie�:
    
    1. **Jedna �wiadoma rozmowa dziennie** - wybierz jedn� interakcj� i zastosuj zasady Poziomu III (ciekawo�� zamiast oceny)
    2. **Obserwuj neurochemi�** - zwracaj uwag�, kiedy widzisz napi�cie u rozm�wcy i jak mo�esz je roz�adowa�
    3. **Eksperymentuj z pytaniami** - zamiast m�wi� "nie", pytaj "jak mogliby�my to rozwi�za�?"
    
    **Pami�taj:** Wed�ug Judith Glaser, ka�da rozmowa to szansa na mikro-zmian�. Ju� jedna �wiadoma interakcja dziennie mo�e zacz�� transformowa� Twoj� rzeczywisto�� zawodow�! ??
    """)
    
    # Dodaj motywuj�cy cytat
    st.markdown("""
    ---
    > *"Dotarcie do nast�pnego poziomu wielko�ci zale�y od jako�ci kultury, kt�ra zale�y od jako�ci relacji, a te � od jako�ci rozm�w."*  
    > **� Judith Glaser**
    """, unsafe_allow_html=True)


def display_quiz_results(quiz_data, question_results, total_points, correct_answers, is_self_diagnostic, quiz_type):
    """Wy�wietla szczeg�owe wyniki quizu po jego uko�czeniu"""
    
    # Statystyki g��wne
    total_questions = len(question_results)
    
    if not is_self_diagnostic and quiz_type != 'slider':
        # Quiz testowy - pokazuj wynik procentowy
        percentage = (correct_answers / total_questions) * 100
        
        # Okre�l kolor na podstawie wyniku
        if percentage >= 75:
            color = "#4CAF50"  # zielony
            status_icon = "??"
            status_text = "�wietny wynik!"
        elif percentage >= 60:
            color = "#FF9800"  # pomara�czowy
            status_icon = "??"
            status_text = "Dobry wynik!"
        else:
            color = "#f44336"  # czerwony
            status_icon = "??"
            status_text = "Mo�esz lepiej!"
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {color}20 0%, {color}10 100%); 
                    padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 5px solid {color};'>
            <h3 style='color: {color}; margin: 0;'>{status_icon} {status_text}</h3>
            <p style='font-size: 1.2rem; margin: 10px 0; color: #333;'>
                <strong>Wynik: {correct_answers}/{total_questions} ({percentage:.1f}%)</strong>
            </p>
            <p style='margin: 0; color: #666;'>
                Poprawne odpowiedzi: {correct_answers} | B��dne odpowiedzi: {total_questions - correct_answers}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    elif quiz_type == 'slider':
        # Quiz ze sliderami
        max_possible = total_questions * max([q.get('max_value', 5) for q in quiz_data.get('questions', [])])
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #2196F320 0%, #2196F310 100%); 
                    padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 5px solid #2196F3;'>
            <h3 style='color: #2196F3; margin: 0;'>?? ��czna suma punkt�w</h3>
            <p style='font-size: 1.2rem; margin: 10px 0; color: #333;'>
                <strong>{total_points}/{max_possible} punkt�w</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Quiz autodiagnozy - przejd� bezpo�rednio do szczeg��w odpowiedzi
        pass
    
    # Szczeg�owa analiza pyta�
    if not is_self_diagnostic:
        st.markdown("### ?? Analiza odpowiedzi na poszczeg�lne pytania")
        
        for i, result in enumerate(question_results):
            with st.expander(f"Pytanie {i+1}: {result['question'][:60]}..." if len(result['question']) > 60 else f"Pytanie {i+1}: {result['question']}", expanded=False):
                
                # Wy�wietl pytanie
                st.markdown(f"**Pytanie:** {result['question']}")
                
                # Wy�wietl odpowied� u�ytkownika
                question_data = quiz_data['questions'][i]
                user_answer = result['user_answer']
                
                if isinstance(user_answer, list):
                    # Multiple choice
                    user_answer_text = ", ".join([question_data['options'][idx] for idx in user_answer])
                    st.markdown(f"**Twoja odpowied�:** {user_answer_text}")
                    
                    # Poka� poprawne odpowiedzi
                    if 'correct_answers' in result:
                        correct_text = ", ".join([question_data['options'][idx] for idx in result['correct_answers']])
                        st.markdown(f"**Poprawne odpowiedzi:** {correct_text}")
                else:
                    # Single choice
                    if user_answer is not None and user_answer < len(question_data.get('options', [])):
                        user_answer_text = question_data['options'][user_answer]
                        st.markdown(f"**Twoja odpowied�:** {user_answer_text}")
                        
                        # Poka� poprawn� odpowied�
                        if 'correct_answer' in result and result['correct_answer'] is not None:
                            correct_text = question_data['options'][result['correct_answer']]
                            st.markdown(f"**Poprawna odpowied�:** {correct_text}")
                
                # Status odpowiedzi
                if result['is_correct']:
                    st.success("? Odpowied� poprawna!")
                else:
                    st.error("? Odpowied� niepoprawna")
                    
                    # Dodaj wyja�nienie, je�li jest dost�pne
                    if 'explanation' in question_data:
                        st.info(f"?? **Wyja�nienie:** {question_data['explanation']}")
    
    else:
        # Dla quiz�w autodiagnozy - poka� podsumowanie odpowiedzi i spersonalizowane wyniki
        st.markdown("### ?? Twoje odpowiedzi")
        
        with st.expander("Zobacz szczeg�y swoich odpowiedzi", expanded=False):
            # Podstawowe szczeg�y odpowiedzi
            for i, result in enumerate(question_results):
                st.markdown(f"**Pytanie {i+1}:** {result['question']}")
                
                question_data = quiz_data['questions'][i]
                user_answer = result['user_answer']
                quiz_type = quiz_data.get('type', 'buttons')
                
                if quiz_type == 'slider':
                    # Quiz ze sliderami - u�yj labels ze scale
                    scale = quiz_data.get('scale', {})
                    labels = scale.get('labels', {})
                    answer_label = labels.get(str(user_answer), str(user_answer))
                    st.markdown(f"**Odpowied�:** {user_answer}/5 - {answer_label}")
                elif isinstance(user_answer, list):
                    # Multiple choice
                    user_answer_text = ", ".join([question_data['options'][idx] for idx in user_answer])
                    st.markdown(f"**Odpowied�:** {user_answer_text} ({result['points_earned']} pkt)")
                else:
                    # Single choice
                    if user_answer is not None and user_answer < len(question_data.get('options', [])):
                        user_answer_text = question_data['options'][user_answer]
                        st.markdown(f"**Odpowied�:** {user_answer_text} ({result['points_earned']} pkt)")
                
                st.markdown("---")
            
            # Sprawd� czy to quiz Conversational Intelligence - spersonalizowane wyniki s� ju� wy�wietlane wcze�niej
            # wi�c tutaj je pomijamy
            pass
    
    # Wskaz�wki i nast�pne kroki
    if not is_self_diagnostic:
        if correct_answers == total_questions:
            st.balloons()
            st.markdown("""
            ### ?? Gratulacje!
            Uzyska�e�/a� maksymalny wynik! Doskonale opanowa�e�/a� materia� z tej lekcji.
            """)
        elif correct_answers / total_questions >= 0.75:
            st.markdown("""
            ### ?? Bardzo dobry wynik!
            �wietnie radzisz sobie z materia�em. Mo�e warto przejrze� pytania, na kt�re odpowiedzia�e�/a� niepoprawnie.
            """)
        elif correct_answers / total_questions >= 0.5:
            st.markdown("""
            ### ?? Dobra robota!
            Masz solidne podstawy, ale warto jeszcze raz przejrze� materia� lekcji, szczeg�lnie tematy z pyta�, na kt�re odpowiedzia�e�/a� niepoprawnie.
            """)
        else:
            st.markdown("""
            ### ?? Czas na powt�rk�!
            Warto wr�ci� do materia�u lekcji i przejrze� go jeszcze raz. Nie martw si� - uczenie si� to proces!
            """)
    
    # Wskaz�wka o ponownym przyst�pieniu
    st.markdown("---")
    st.markdown("?? **Wskaz�wka:** Mo�esz przyst�pi� do quizu ponownie, klikaj�c przycisk '?? Przyst�p do quizu ponownie'.")
