"""
Mobile Navigation Component for Streamlit
Integrates bottom tab navigation with Streamlit's session state
"""

import streamlit as st
from utils.error_handling import handle_error, safe_execute

@handle_error
def render_mobile_navigation():
    """
    Renderuje mobilną nawigację dolną z automatyczną integracją ze Streamlit
    """
    
    # Load CSS and JS
    load_mobile_navigation_assets()
    
    # Create mobile navigation HTML with Streamlit integration
    mobile_nav_html = f"""
    <div class="mobile-bottom-nav" id="mobile-nav-container">
        <div class="mobile-nav-items">
            <div class="mobile-nav-item {get_active_class('dashboard')}" onclick="navigateToPage('dashboard')">
                <div class="mobile-nav-icon">🏠</div>
                <div class="mobile-nav-label">Start</div>
            </div>
            <div class="mobile-nav-item {get_active_class('lesson')}" onclick="navigateToPage('lesson')">
                <div class="mobile-nav-icon">📚</div>
                <div class="mobile-nav-label">Nauka</div>
            </div>
            <div class="mobile-nav-item {get_active_class('lesson')}" onclick="navigateToPage('lesson', 'skills')">
                <div class="mobile-nav-icon">🌳</div>
                <div class="mobile-nav-label">Mapa</div>
            </div>
            <div class="mobile-nav-item {get_active_class('profile')}" onclick="navigateToPage('profile')">
                <div class="mobile-nav-icon">👤</div>
                <div class="mobile-nav-label">Profil</div>
                {get_notification_badge('profile')}
            </div>
        </div>
    </div>
    
    <script>
    function navigateToPage(page, subpage = null) {{
        // Update Streamlit session state via form submission
        const form = document.createElement('form');
        form.method = 'POST';
        form.style.display = 'none';
        
        // Create hidden input for page
        const pageInput = document.createElement('input');
        pageInput.type = 'hidden';
        pageInput.name = 'mobile_nav_page';
        pageInput.value = page;
        form.appendChild(pageInput);
        
        // Create hidden input for subpage if provided
        if (subpage) {{
            const subpageInput = document.createElement('input');
            subpageInput.type = 'hidden';
            subpageInput.name = 'mobile_nav_subpage';
            subpageInput.value = subpage;
            form.appendChild(subpageInput);
        }}
        
        document.body.appendChild(form);
        
        // Try to use Streamlit's navigation if available
        if (window.parent && window.parent.streamlit) {{
            try {{
                // Set session state through Streamlit
                window.parent.streamlit.setComponentValue({{
                    'mobile_nav_page': page,
                    'mobile_nav_subpage': subpage
                }});
            }} catch (e) {{
                // Fallback to form submission
                form.submit();
            }}
        }} else {{
            // Fallback to clicking existing navigation buttons
            clickStreamlitButton(page);
        }}
        
        // Visual feedback
        updateActiveState(page);
        addPageTransition();
        
        document.body.removeChild(form);
    }}
    
    function clickStreamlitButton(page) {{
        const buttonMappings = {{
            'dashboard': ['.stSidebar button:contains("START")', 'button:contains("🏠")', 'button:contains("Start")'],
            'lesson': ['.stSidebar button:contains("NAUKA")', 'button:contains("📚")', 'button:contains("Nauka")'],
            'profile': ['.stSidebar button:contains("PROFIL")', 'button:contains("👤")', 'button:contains("Profil")']
        }};
        
        const selectors = buttonMappings[page] || [];
        
        for (const selector of selectors) {{
            const button = document.querySelector(selector);
            if (button) {{
                button.click();
                break;
            }}
        }}
    }}
    
    function updateActiveState(activePage) {{
        const navItems = document.querySelectorAll('.mobile-nav-item');
        navItems.forEach(item => {{
            item.classList.remove('active');
        }});
        
        // Add active class to current page
        const activeItems = document.querySelectorAll(`.mobile-nav-item[onclick*="${{activePage}}"]`);
        activeItems.forEach(item => item.classList.add('active'));
    }}
    
    function addPageTransition() {{
        const mainContent = document.querySelector('.main');
        if (mainContent) {{
            mainContent.classList.remove('page-transition');
            setTimeout(() => {{
                mainContent.classList.add('page-transition');
            }}, 10);
        }}
    }}
    
    // Initialize on load
    document.addEventListener('DOMContentLoaded', function() {{
        if (window.innerWidth <= 1024) {{
            updateActiveState('{st.session_state.get('page', 'dashboard')}');
        }}
    }});
    </script>
    """
    
    # Render mobile navigation (only on mobile devices)
    st.markdown(mobile_nav_html, unsafe_allow_html=True)
    
    # Handle mobile navigation input
    handle_mobile_navigation_input()

def load_mobile_navigation_assets():
    """Ładuje CSS i JS dla mobilnej nawigacji"""
    
    # Load CSS
    try:
        with open('static/css/mobile-navigation.css', 'r', encoding='utf-8') as f:
            mobile_css = f.read()
        st.markdown(f"<style>{mobile_css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ Nie znaleziono pliku CSS dla mobilnej nawigacji")
    
    # Add responsive behavior CSS
    responsive_css = """
    <style>
    /* Show mobile nav only on mobile/tablet */
    @media (max-width: 1024px) {
        .mobile-bottom-nav {
            display: block !important;
        }
        
        /* Hide Streamlit sidebar on mobile */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Adjust main content */
        .main {
            margin-left: 0 !important;
        }
        
        .main .block-container {
            padding-bottom: 5rem !important;
        }
    }
    
    @media (min-width: 1025px) {
        .mobile-bottom-nav {
            display: none !important;
        }
    }
    </style>
    """
    st.markdown(responsive_css, unsafe_allow_html=True)

def get_active_class(page):
    """Zwraca klasę 'active' jeśli strona jest aktywna"""
    current_page = st.session_state.get('page', 'dashboard')
    return 'active' if current_page == page else ''

def get_notification_badge(page):
    """Zwraca HTML dla badge z powiadomieniami"""
    # Sprawdź czy są powiadomienia dla danej strony
    notifications = st.session_state.get(f'{page}_notifications', 0)
    
    if notifications > 0:
        return f'<div class="mobile-nav-badge">{notifications if notifications < 10 else "9+"}</div>'
    return ''

def handle_mobile_navigation_input():
    """Obsługuje input z mobilnej nawigacji"""
    
    # Check for mobile navigation input
    if 'mobile_nav_page' in st.session_state:
        target_page = st.session_state.mobile_nav_page
        subpage = st.session_state.get('mobile_nav_subpage', None)
        
        # Update session state
        st.session_state.page = target_page
        
        # Handle subpage navigation (like skills in lesson view)
        if subpage == 'skills' and target_page == 'lesson':
            st.session_state.lesson_view = 'skills'
        
        # Clear mobile nav inputs
        if 'mobile_nav_page' in st.session_state:
            del st.session_state.mobile_nav_page
        if 'mobile_nav_subpage' in st.session_state:
            del st.session_state.mobile_nav_subpage
        
        # Trigger rerun to navigate
        st.rerun()

@handle_error
def set_mobile_notification(page, count=1):
    """
    Ustawia liczbę powiadomień dla danej strony
    
    Args:
        page (str): Nazwa strony ('dashboard', 'lesson', 'profile')
        count (int): Liczba powiadomień (0 = ukryj badge)
    """
    st.session_state[f'{page}_notifications'] = max(0, count)

@handle_error
def clear_mobile_notification(page):
    """Usuwa powiadomienia dla danej strony"""
    set_mobile_notification(page, 0)

# Convenience functions for common navigation actions
def show_mobile_nav_if_needed():
    """Pokazuje mobilną nawigację jeśli jesteśmy na urządzeniu mobilnym"""
    if is_mobile_device():
        render_mobile_navigation()

def is_mobile_device():
    """Sprawdza czy urządzenie to mobile/tablet na podstawie user agent lub viewport"""
    # W rzeczywistej implementacji można użyć streamlit-device-detector
    # Na razie zakładamy że mobile = szerokość <= 1024px (CSS handle to)
    return True  # CSS będzie kontrolować wyświetlanie

# Export functions for use in other modules
__all__ = [
    'render_mobile_navigation',
    'set_mobile_notification', 
    'clear_mobile_notification',
    'show_mobile_nav_if_needed',
    'is_mobile_device'
]
