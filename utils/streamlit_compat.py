# 🔧 STREAMLIT COMPATIBILITY UTILS
# Narzędzia do obsługi kompatybilności różnych wersji Streamlit

import streamlit as st
import sys
from packaging import version

def get_streamlit_version():
    """Pobierz wersję Streamlit"""
    try:
        return version.parse(st.__version__)
    except:
        return version.parse("1.0.0")  # fallback

def tabs_with_fallback(tab_labels, **kwargs):
    """
    Funkcja tworząca tabs z fallback na expanders dla starszych wersji Streamlit
    
    Args:
        tab_labels: Lista nazw zakładek
        **kwargs: Dodatkowe argumenty dla st.tabs()
    
    Returns:
        Lista kontenerów (tabs lub expanders)
    """
    streamlit_version = get_streamlit_version()
    min_tabs_version = version.parse("1.22.0")
    
    try:
        # Sprawdź czy st.tabs() jest dostępne
        if streamlit_version >= min_tabs_version and hasattr(st, 'tabs'):
            # Użyj natywnych tabs
            return st.tabs(tab_labels, **kwargs)
        else:
            # Fallback na expanders
            st.info("📱 **Używasz starszej wersji Streamlit** - wyświetlamy sekcje jako rozwijane panele zamiast zakładek.")
            containers = []
            for label in tab_labels:
                containers.append(st.expander(label, expanded=False))
            return containers
    except Exception as e:
        # Jeśli coś pójdzie nie tak, użyj expanders
        st.warning(f"⚠️ **Problem z wyświetlaniem zakładek** - przełączamy na alternatywny widok: {str(e)}")
        containers = []
        for label in tab_labels:
            containers.append(st.expander(label, expanded=False))
        return containers

def safe_multiselect(label, options, default=None, **kwargs):
    """
    Bezpieczna wersja st.multiselect z obsługą błędów
    """
    try:
        return st.multiselect(label, options, default=default, **kwargs)
    except Exception as e:
        st.error(f"Błąd multiselect: {str(e)}")
        return default or []

def safe_selectbox(label, options, index=0, **kwargs):
    """
    Bezpieczna wersja st.selectbox z obsługą błędów
    """
    try:
        return st.selectbox(label, options, index=index, **kwargs)
    except Exception as e:
        st.error(f"Błąd selectbox: {str(e)}")
        return options[0] if options else None

def check_streamlit_features():
    """
    Sprawdź dostępność funkcji Streamlit i wyświetl raport
    """
    features = {
        "tabs": hasattr(st, 'tabs'),
        "columns": hasattr(st, 'columns'),
        "expander": hasattr(st, 'expander'),
        "sidebar": hasattr(st, 'sidebar'),
        "multiselect": hasattr(st, 'multiselect'),
        "selectbox": hasattr(st, 'selectbox'),
        "button": hasattr(st, 'button'),
        "markdown": hasattr(st, 'markdown'),
    }
    
    return features

def display_compatibility_info():
    """
    Wyświetl informacje o kompatybilności w sidebar (tylko w trybie dev)
    """
    if st.session_state.get('dev_mode', False):
        with st.sidebar:
            with st.expander("🔧 Kompatybilność Streamlit", expanded=False):
                st.write(f"**Wersja**: {st.__version__}")
                features = check_streamlit_features()
                for feature, available in features.items():
                    status = "✅" if available else "❌"
                    st.write(f"{status} `{feature}`")
