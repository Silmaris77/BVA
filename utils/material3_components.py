import streamlit as st
from utils.theme_manager import ThemeManager

def load_extended_material3_css():
    """Ładuje rozszerzony zestaw stylów Material 3 przez ThemeManager"""
    ThemeManager.apply_base_styles()

def m3_button_styles():
    """Style przycisków są teraz w static/css/core/components.css"""
    pass

def m3_lesson_card_styles():
    """Style kart są teraz w static/css/core/components.css"""
    pass

def apply_material3_theme():
    """Aplikuje wszystkie style Material 3 przez ThemeManager"""
    ThemeManager.apply_all()


# ========================================
# FUNKCJE HELPER (zachowane dla kompatybilności)
# ========================================

def m3_card(title, content, badge=None, icon=None):
    """Renderuje prostą kartę w stylu Material 3"""
    icon_html = f'<span style="font-size: 24px; margin-right: 12px;">{icon}</span>' if icon else ""
    badge_html = f'<div class="m3-badge" style="background-color: #673AB7; margin-left: auto;">{badge}</div>' if badge else ""
    
    card_html = f"""
    <div class="m3-lesson-card">
        <div class="m3-card-content">
            <div style="display: flex; align-items: center;">
                {icon_html}
                <h3 style="margin: 0; flex-grow: 1;">{title}</h3>
                {badge_html}
            </div>
            <p class="m3-description">{content}</p>
        </div>
    </div>
    """
    
    m3_lesson_card_styles()  # Upewnij się, że style są załadowane
    return st.markdown(card_html, unsafe_allow_html=True)

def m3_chip(label, icon=None, is_selected=False, color="#E0E0E0", text_color="#000000"):
    """Renderuje chip w stylu Material 3"""
    icon_html = f'<span style="margin-right: 6px;">{icon}</span>' if icon else ""
    selected_class = "m3-chip-selected" if is_selected else ""
    
    chip_html = f"""
    <style>
    .m3-chip {{
        display: inline-flex;
        align-items: center;
        height: 32px;
        padding: 0 12px;
        border-radius: 16px;
        background-color: {color};
        color: {text_color};
        font-size: 13px;
        font-weight: 500;
        margin: 4px;
        transition: background-color 0.3s;
    }}
    
    .m3-chip:hover {{
        filter: brightness(0.95);
    }}
    
    .m3-chip-selected {{
        background-color: #2196F3;
        color: white;
    }}
    </style>
    
    <span class="m3-chip {selected_class}">
        {icon_html}
        {label}
    </span>
    """
    
    return st.markdown(chip_html, unsafe_allow_html=True)

def m3_segmented_button(options, callback=None):
    """Tworzy przycisk segmentowany w stylu Material 3"""
    if "m3_segmented_selected" not in st.session_state:
        st.session_state.m3_segmented_selected = 0
    
    st.markdown("""
    <style>
    .m3-segmented-container {
        display: flex;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        margin: 8px 0;
    }
    
    .m3-segment {
        flex: 1;
        text-align: center;
        padding: 8px 12px;
        background-color: white;
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s;
        border-right: 1px solid rgba(0,0,0,0.1);
        font-family: 'Roboto', sans-serif;
        font-size: 14px;
    }
    
    .m3-segment:last-child {
        border-right: none;
    }
    
    .m3-segment:hover {
        background-color: rgba(33, 150, 243, 0.1);
    }
    
    .m3-segment-selected {
        background-color: #2196F3 !important;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(len(options))
    for i, (col, option) in enumerate(zip(cols, options)):
        with col:
            button_key = f"m3_segment_{i}"
            selected_class = "m3-segment-selected" if st.session_state.m3_segmented_selected == i else ""
            
            if st.button(option, key=button_key):
                st.session_state.m3_segmented_selected = i
                if callback:
                    callback(i)
            
            # Dodaj klasę stylu do przycisku
            st.markdown(f"""
            <script>
                const button = document.querySelector('button[kind="secondary"][data-testid="{button_key}"]');
                if (button) {{
                    button.classList.add('m3-segment');
                    button.classList.add('{selected_class}');
                }}
            </script>
            """, unsafe_allow_html=True)
    
    return st.session_state.m3_segmented_selected

def m3_text_field(label, value="", key=None, type="text", help=None):
    """Renderuje pole tekstowe w stylu Material 3"""
    field_key = key or f"m3_text_field_{label}"
    
    st.markdown(f"""
    <style>
    .m3-text-field {{
        position: relative;
        margin-bottom: 16px;
        padding-top: 16px;
    }}
    
    .m3-text-field input {{
        width: 100%;
        padding: 12px 16px;
        font-size: 16px;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        background-color: transparent;
        transition: border-color 0.3s, box-shadow 0.3s;
    }}
    
    .m3-text-field input:focus {{
        outline: none;
        border-color: #2196F3;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
    }}
    
    .m3-text-field label {{
        position: absolute;
        left: 16px;
        top: 0;
        font-size: 12px;
        color: #757575;
    }}
    
    .m3-text-field-help {{
        font-size: 12px;
        color: #757575;
        margin-top: 4px;
    }}
    </style>
    
    <div class="m3-text-field">
        <label for="{field_key}">{label}</label>
    </div>
    """, unsafe_allow_html=True)
    
    if type == "password":
        result = st.text_input("", key=field_key, type="password")
    else:
        result = st.text_input("", key=field_key)

    if value:  # Jeśli wartość jest określona, ustaw ją po inicjalizacji
        st.session_state[field_key] = value
    
    if help:
        st.markdown(f'<div class="m3-text-field-help">{help}</div>', unsafe_allow_html=True)
    
    return result

def m3_avatar(image_url=None, text=None, size=40, bg_color="#2196F3"):
    """Renderuje awatar w stylu Material 3"""
    if not image_url and not text:
        text = "U"
    
    if text and len(text) > 2:
        text = text[:2]
    
    avatar_html = f"""
    <style>
    .m3-avatar {{
        width: {size}px;
        height: {size}px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: {size//2.5}px;
        font-weight: 500;
        color: white;
        background-color: {bg_color};
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    </style>
    
    <div class="m3-avatar">
    """
    
    if image_url:
        avatar_html += f'<img src="{image_url}" width="{size}" height="{size}" style="object-fit: cover;">'
    else:
        avatar_html += f'{text}'
    
    avatar_html += "</div>"
    
    return st.markdown(avatar_html, unsafe_allow_html=True)
