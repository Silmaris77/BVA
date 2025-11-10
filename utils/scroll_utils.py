"""
Utilities for handling page scrolling in Streamlit applications.
"""

import streamlit as st
import streamlit.components.v1 as components


def scroll_to_top():
    """
    Przewija stronę na samą górę używając components.html (najbardziej niezawodne).
    """
    components.html(
        """
        <script>
            // Funkcja brutalnie scrollująca wszystko
            function brutalScroll() {
                // Parent window
                try {
                    window.parent.document.documentElement.scrollTop = 0;
                    window.parent.document.body.scrollTop = 0;
                    window.parent.scrollTo(0, 0);
                } catch(e) {}
                
                // Wszystkie kontenery
                const selectors = [
                    'section.main',
                    'section.main > div',
                    '[data-testid="stMain"]',
                    '[data-testid="stAppViewContainer"]',
                    '.main',
                    'body',
                    'html'
                ];
                
                selectors.forEach(sel => {
                    try {
                        const elements = window.parent.document.querySelectorAll(sel);
                        elements.forEach(el => {
                            el.scrollTop = 0;
                            el.scrollTo && el.scrollTo(0, 0);
                        });
                    } catch(e) {}
                });
            }
            
            // Wykonaj natychmiast
            brutalScroll();
            
            // I powtarzaj aż zadziała
            [0, 10, 50, 100, 200, 300, 500, 1000].forEach(delay => {
                setTimeout(brutalScroll, delay);
            });
        </script>
        """,
        height=0
    )


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