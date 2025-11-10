"""
Utilities for handling page scrolling in Streamlit applications.
"""

import streamlit as st


def scroll_to_top():
    """
    Przewija stronę na samą górę.
    Funkcja ta wstrzykuje JavaScript, który przewija główny kontener Streamlit do pozycji (0, 0).
    """
    js_code = """
    <script>
        setTimeout(function() {
            // Próbuj różne selektory, żeby znaleźć główny kontener
            const selectors = [
                'section.main > div',
                'section.main',
                '.main > div',
                '.main',
                '[data-testid="stMain"]',
                '.stApp > div'
            ];
            
            for (let selector of selectors) {
                const element = window.parent.document.querySelector(selector);
                if (element) {
                    element.scrollTop = 0;
                    break;
                }
            }
            
            // Fallback - przewiń całe okno
            window.parent.scrollTo(0, 0);
        }, 50);
    </script>
    """
    
    # Używamy st.markdown zamiast components.html aby uniknąć dodatkowej przestrzeni od iframe
    st.markdown(js_code, unsafe_allow_html=True)


def scroll_to_top_with_delay(delay_ms=100):
    """
    Przewija stronę na górę z opcjonalnym opóźnieniem.
    
    Args:
        delay_ms (int): Opóźnienie w milisekundach przed przewinięciem
    """
    js_code = f"""
    <script>
        setTimeout(function() {{
            const selectors = [
                'section.main > div',
                'section.main',
                '.main > div', 
                '.main',
                '[data-testid="stMain"]',
                '.stApp > div'
            ];
            
            for (let selector of selectors) {{
                const element = window.parent.document.querySelector(selector);
                if (element) {{
                    element.scrollTop = 0;
                    break;
                }}
            }}
            
            window.parent.scrollTo(0, 0);
        }}, {delay_ms});
    </script>
    """
    
    # Używamy st.markdown zamiast components.html aby uniknąć dodatkowej przestrzeni od iframe
    st.markdown(js_code, unsafe_allow_html=True)


def scroll_to_top_smooth():
    """
    Przewija stronę na górę z płynną animacją.
    """
    js_code = """
    <script>
        setTimeout(function() {
            const selectors = [
                'section.main > div',
                'section.main',
                '.main > div',
                '.main',
                '[data-testid="stMain"]',
                '.stApp > div'
            ];
            
            for (let selector of selectors) {
                const element = window.parent.document.querySelector(selector);
                if (element) {
                    element.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });
                    break;
                }
            }
            
            // Fallback
            window.parent.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }, 50);
    </script>
    """
    
    # Używamy st.markdown zamiast components.html aby uniknąć dodatkowej przestrzeni od iframe
    st.markdown(js_code, unsafe_allow_html=True)


def auto_scroll_on_tab_change(tab_key=None):
    """
    Automatycznie przewija do góry przy zmianie zakładki.
    Używa session_state do śledzenia aktualnej zakładki.
    
    Args:
        tab_key (str): Klucz identyfikujący zestaw zakładek
    """
    if tab_key is None:
        tab_key = "current_tab"
    
    # Jeśli to pierwsza wizyta, ustaw wartość domyślną
    if tab_key not in st.session_state:
        st.session_state[tab_key] = None
        return
    
    # Sprawdź czy zakładka się zmieniła
    current_tab_state = st.session_state.get(tab_key)
    
    # Wywołaj przewijanie jeśli zakładka została zmieniona
    if current_tab_state is not None:
        scroll_to_top()