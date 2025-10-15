"""Test układu feedbacku - expander pełnej szerokości"""
import streamlit as st

st.set_page_config(page_title="Test Layout", layout="wide")

st.title("Test nowego układu")

# Symulacja feedbacku
st.success("✅ Ćwiczenie 'Identyfikacja poziomów rozmowy' zostało ukończone!")

with st.expander("📝 Feedback AI", expanded=True):
    st.markdown("### 📝 Twoja odpowiedź")
    st.info("poziom 3, komunikat my i wzrost adrenaliny")
    st.markdown("---")
    
    # Symulacja feedbacku
    st.markdown("""
    <div style='text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 15px; margin: 20px 0;'>
        <div style='font-size: 4em;'>👍</div>
        <h1 style='color: white; font-size: 3.5em; margin: 10px 0;'>7<span style='font-size: 0.5em; opacity: 0.8;'>/10</span></h1>
        <p style='color: white; margin: 0; font-size: 1.3em;'>Dobra robota!</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["💬 Analiza", "📊 Szczegóły", "💡 Kluczowa rada"])
    
    with tab1:
        st.markdown("### 💬 Szczegółowa analiza AI")
        st.markdown("""
        <div style='padding: 15px; background: #f8f9fa; border-left: 4px solid #667eea; border-radius: 5px; margin: 10px 0;'>
            <p style='color: #333; margin: 0;'>Świetnie zidentyfikowałeś Poziom III!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### ✅ Mocne strony")
            st.markdown("""
            <div style='padding: 12px; background: #d1fae5; border-left: 4px solid #10b981; border-radius: 5px;'>
                <p style='color: #065f46; margin: 0;'>✓ Poprawna identyfikacja</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("#### 🎯 Obszary rozwoju")
            st.markdown("""
            <div style='padding: 12px; background: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 5px;'>
                <p style='color: #92400e; margin: 0;'>→ Neurobiologia</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 💡 Najważniejsza lekcja")
        st.info("Poziom III buduje zaufanie!")

# Przycisk Reset pod expanderem - wyśrodkowany
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    st.button("🔄 Reset ćwiczenia", use_container_width=True)

st.markdown("---")
st.caption("✅ Expander teraz wykorzystuje pełną szerokość! Przycisk Reset jest pod expanderem, wyśrodkowany.")
