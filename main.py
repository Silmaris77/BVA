import streamlit as st
import os
import sys
import traceback
from config.settings import PAGE_CONFIG

# Ta funkcja musi być wywołana jako pierwsza funkcja Streamlit
st.set_page_config(**PAGE_CONFIG)

# Ścieżka do głównego katalogu aplikacji (dla importów)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

# Pozostały import - próbujemy z obsługą błędów
try:
    from utils.session import init_session_state, clear_session
    from utils.components import zen_header, navigation_menu, zen_button
    from views.login import show_login_page
    from views.dashboard import show_dashboard
    from views.lesson import show_lesson
    from views.profile import show_profile
    from views.skills_new import show_skill_tree
    from views.admin import show_admin_dashboard
    from views.inspirations import show_inspirations_page
    
    # Import shop module is done within the routing section
except Exception as e:
    st.error(f"Błąd podczas importowania modułów: {str(e)}")
    st.code(traceback.format_exc())
    st.stop()  # Stop execution if imports fail

# Załaduj pliki CSS
def load_css(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()
    return css

# Ścieżka do głównego pliku CSS
css_path = os.path.join(os.path.dirname(__file__), "static", "css", "style.css")
css = load_css(css_path)
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def main():
    # Initialize session state
    init_session_state()
    
    # Sidebar for logged-in users
    if st.session_state.logged_in:
        with st.sidebar:
            st.markdown(f"### Witaj, {st.session_state.username}!")
            # Nawigacja
            navigation_menu()
              # Przycisk wylogowania na dole sidebara
            if zen_button("🚪 Wyloguj się", key="logout_button", use_container_width=True):
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
        elif st.session_state.page == 'inspirations':
            show_inspirations_page()
        elif st.session_state.page == 'profile':
            show_profile()
        elif st.session_state.get('page') == 'admin':
            show_admin_dashboard()

if __name__ == "__main__":
    main()