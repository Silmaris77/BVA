import streamlit as st
import os
import sys
import traceback
import warnings

# Ukryj ostrzeżenia Google Cloud (ALTS credentials)
warnings.filterwarnings('ignore', message='.*ALTS.*')
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

# Ścieżka do głównego katalogu aplikacji (dla importów)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# Import konfiguracji (z fallbackiem)
try:
    from config.settings import PAGE_CONFIG
except Exception as e:
    # Fallback PAGE_CONFIG
    PAGE_CONFIG = {
        "page_title": "BrainventureAcademy",
        "page_icon": "🧠",
        "layout": "wide",
        "initial_sidebar_state": "expanded",
        "menu_items": {
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    }

# Ta funkcja musi być wywołana jako pierwsza funkcja Streamlit
st.set_page_config(**PAGE_CONFIG)

# Pozostały import - próbujemy z obsługą błędów
try:
    from utils.session import init_session_state, clear_session
    from utils.components import zen_header, navigation_menu, zen_button
    from utils.theme_manager import ThemeManager
    from views.login import show_login_page
    from views.dashboard import show_dashboard
    from views.lesson import show_lesson
    from views.profile import show_profile
    from views.skills_new import show_skill_tree
    from views.admin import show_admin_dashboard
    from views.inspirations import show_inspirations_page
    from views.tools import show_tools_page
    from views.business_games import show_business_games
    
    # Import shop module is done within the routing section
except Exception as e:
    st.error(f"Błąd podczas importowania modułów: {str(e)}")
    st.code(traceback.format_exc())
    st.stop()  # Stop execution if imports fail

def main():
    # Initialize session state
    init_session_state()
    
    # Aplikuj wszystkie style (base + user theme)
    ThemeManager.apply_all()
    
    # Mobile sidebar helper - widoczny przycisk na górze strony
    if st.session_state.logged_in:
        st.markdown("""
        <style>
        /* Mobile sidebar helper button */
        @media (max-width: 768px) {
            .mobile-sidebar-btn {
                position: fixed;
                top: 10px;
                left: 10px;
                z-index: 9999;
                background: #3498db;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 18px;
                cursor: pointer;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                display: block;
            }
            .mobile-sidebar-btn:hover {
                background: #2980b9;
            }
        }
        @media (min-width: 769px) {
            .mobile-sidebar-btn {
                display: none;
            }
        }
        </style>
        <div class="mobile-sidebar-btn" onclick="
            const sidebar = window.parent.document.querySelector('[data-testid=\\'stSidebar\\']');
            if (sidebar) {
                const isHidden = sidebar.getAttribute('aria-expanded') === 'false';
                sidebar.setAttribute('aria-expanded', isHidden ? 'true' : 'false');
            }
        ">☰ Menu</div>
        """, unsafe_allow_html=True)
    
    # Sidebar for logged-in users
    if st.session_state.logged_in:
        with st.sidebar:
            st.markdown(f"### Witaj, {st.session_state.username}!")
            # Nawigacja
            navigation_menu()
            
            # # ===== QUICK NOTES (always visible) =====
            # st.markdown("---")
            # st.markdown("### 📝 Szybkie notatki")
            
            # # Initialize quick notes in session state
            # if 'quick_notes' not in st.session_state:
            #     st.session_state['quick_notes'] = ""
            
            # quick_note = st.text_area(
            #     "",
            #     value=st.session_state.get('quick_notes', ''),
            #     height=100,
            #     placeholder="Szybka notatka o kliencie, produkcie, zadaniu...",
            #     key="sidebar_quick_note",
            #     help="Notatki są automatycznie zapisywane w sesji"
            # )
            
            # # Auto-save on change
            # if quick_note != st.session_state.get('quick_notes', ''):
            #     st.session_state['quick_notes'] = quick_note
            
            # col_n1, col_n2 = st.columns(2)
            
            # with col_n1:
            #     if st.button("🗑️ Wyczyść", use_container_width=True, help="Wyczyść szybkie notatki", key="clear_quick_notes"):
            #         st.session_state['quick_notes'] = ""
            #         st.rerun()
            
            # with col_n2:
            #     if st.button("📋 Pełny", use_container_width=True, help="Otwórz pełny notatnik", key="open_full_notes"):
            #         st.info("💡 Pełny notatnik: Dashboard → Zadania & Rozwój")
            
            # st.markdown("---")
            
            # Przycisk wylogowania na dole sidebara
            if zen_button("🚪 Wyloguj się", key="logout_button", width='stretch'):
                # JavaScript do zamknięcia sidebar na mobile po wylogowaniu
                st.markdown("""
                <script>
                if (window.innerWidth < 768) {
                    setTimeout(function() {
                        const sidebarCloseButton = parent.document.querySelector('[data-testid="collapsedControl"]');
                        if (sidebarCloseButton) {
                            sidebarCloseButton.click();
                        }
                    }, 100);
                }
                </script>
                """, unsafe_allow_html=True)
                clear_session()
                st.rerun()
    
    # Page routing
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.page == 'dashboard':
            show_dashboard()
        elif st.session_state.page == 'lesson':
            show_lesson()
        elif st.session_state.page == 'tools':
            show_tools_page()
        elif st.session_state.page == 'business_games':
            # Pobierz dane użytkownika
            from data.users_new import load_user_data
            users_data = load_user_data()
            user_data = users_data.get(st.session_state.username, {})
            show_business_games(st.session_state.username, user_data)
        elif st.session_state.page == 'inspirations':
            show_inspirations_page()
        elif st.session_state.page == 'profile':
            show_profile()
        elif st.session_state.get('page') == 'admin':
            show_admin_dashboard()

if __name__ == "__main__":
    main()