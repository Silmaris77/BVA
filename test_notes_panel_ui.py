"""
Test - Notes Panel Component standalone
"""

import streamlit as st
import sys
from pathlib import Path

# Dodaj parent directory
sys.path.insert(0, str(Path(__file__).parent))

from utils.notes_panel import render_notes_panel, render_notes_panel_compact

st.set_page_config(page_title="Test Notatnika", layout="wide")

st.title("🧪 Test Panelu Notatek")

# Test user ID
test_user_id = st.number_input("User ID", value=1, min_value=1)

st.markdown("---")

# Test layout z 2 kolumnami
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Główna treść (symulacja rozmowy)")
    st.info("Tutaj byłaby rozmowa z klientem...")
    
    for i in range(3):
        st.markdown(f"""
        <div style='background: #f1f5f9; padding: 16px; border-radius: 12px; margin: 12px 0;'>
            <strong>Klient:</strong> Wiadomość testowa {i+1}
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📔 Panel Notatek")
    render_notes_panel(
        user_id=test_user_id,
        active_tab="product_card"
    )

st.markdown("---")
st.markdown("### 📱 Wersja kompaktowa")
render_notes_panel_compact(test_user_id)
