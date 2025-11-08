import streamlit as st
from data.users import register_user, login_user
from utils.components import zen_header, notification, zen_button, add_animations_css
from utils.material3_components import apply_material3_theme
from utils.css_loader import ensure_css_files, load_login_css
from utils.scroll_utils import scroll_to_top
from config.settings import DEVELOPMENT_MODE
import os
import base64

# Funkcja do konwersji obrazu na Base64
def img_to_base64(img_path):
    try:
        if os.path.exists(img_path):
            with open(img_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        st.error(f"Błąd wczytywania logo: {str(e)}")
    return ""

def show_login_page():
    # Ostrzeżenie o trybie developerskim
    if DEVELOPMENT_MODE:
        st.warning("⚡ **TRYB DEVELOPERSKI AKTYWNY** - Dane nie są zapisywane do plików (tylko w pamięci). Po restarcie aplikacji znikną.")
    
    # Zastosuj Material 3 Theme
    apply_material3_theme()
    
    # Dodaj animacje CSS
    add_animations_css()
    
    # Upewnij się, że pliki CSS istnieją i załaduj je
    ensure_css_files()
    load_login_css()
    
    # Znajdź logo
    logo_path = os.path.join("assets", "images", "Mozg.png")
    
    # NOWOCZESNY LAYOUT - Centrowana karta z gradientowym tłem
    st.markdown("""
    <style>
        /* Pełnoekranowe gradientowe tło */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        
        /* Ukryj header Streamlit */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Centrowanie całego contentu */
        .main .block-container {
            max-width: 1200px !important;
            padding-top: 5vh !important;
            padding-bottom: 3rem !important;
        }
        
        /* Biała karta główna */
        .login-card {
            background: white;
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: fadeInUp 0.6s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Logo centrowanie */
        .logo-container {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .logo-container img {
            max-width: 200px;
            filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.15));
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        /* Tytuł */
        .login-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .login-subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #64748b;
            margin-bottom: 2.5rem;
            line-height: 1.6;
        }
        
        /* Formularz */
        .stTextInput > div > div > input {
            border-radius: 12px !important;
            border: 2px solid #e2e8f0 !important;
            padding: 14px 16px !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        /* Przyciski */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 14px 28px !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px !important;
            background: transparent !important;
            border-bottom: 2px solid #e2e8f0 !important;
            margin-bottom: 2rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #64748b !important;
            font-weight: 500 !important;
            font-size: 16px !important;
            padding: 12px 24px !important;
            border-radius: 8px 8px 0 0 !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-weight: 600 !important;
        }
        
        /* Info box na dole */
        .info-box {
            text-align: center;
            margin-top: 2rem;
            padding: 1.5rem;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border-radius: 12px;
            border-left: 4px solid #667eea;
        }
        
        .info-box h4 {
            color: #1a202c;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        .info-box p {
            color: #475569;
            margin: 0;
            line-height: 1.6;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Główny kontener - centrowana biała karta
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Logo i tytuł
    col_logo, col_spacer, col_logo2 = st.columns([1, 2, 1])
    with col_spacer:
        if os.path.exists(logo_path):
            st.markdown('<div class="logo-container">', unsafe_allow_html=True)
            try:
                st.image(logo_path, use_column_width=True)
            except TypeError:
                # Fallback for older Streamlit versions
                st.image(logo_path, width=300)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h1 class="login-title">BrainVenture Academy</h1>', unsafe_allow_html=True)
    st.markdown('<p class="login-subtitle">Odkryj tajemnice mózgu i wykorzystaj je w zarządzaniu</p>', unsafe_allow_html=True)
    
    # Zakładki Logowanie/Rejestracja
    login_tab, register_tab = st.tabs(["🔐 Logowanie", "✨ Rejestracja"])
    
    # Zakładka logowania
    with login_tab:
        scroll_to_top()
        with st.form("login_form", clear_on_submit=False):
            st.text_input("Nazwa użytkownika", key="login_username", placeholder="Wpisz swoją nazwę użytkownika")
            st.text_input("Hasło", type="password", key="login_password", placeholder="Wpisz swoje hasło")
            
            st.write("")  # Spacing
            submit_login = st.form_submit_button("Zaloguj się", use_container_width=True)
            
            if submit_login:
                username = st.session_state.login_username
                password = st.session_state.login_password
                
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.page = 'dashboard'
                    st.rerun()
                else:
                    st.error("❌ Niepoprawna nazwa użytkownika lub hasło.")
    
    # Zakładka rejestracji
    with register_tab:
        scroll_to_top()
        with st.form("register_form", clear_on_submit=False):
            st.text_input("Nazwa użytkownika", key="reg_username", placeholder="Wybierz unikalną nazwę")
            st.text_input("Hasło", type="password", key="reg_password", placeholder="Minimum 6 znaków")
            st.text_input("Potwierdź hasło", type="password", key="reg_confirm", placeholder="Powtórz hasło")
            
            st.write("")  # Spacing
            submit_register = st.form_submit_button("Utwórz konto", use_container_width=True)
            
            if submit_register:
                new_username = st.session_state.reg_username
                new_password = st.session_state.reg_password
                confirm_password = st.session_state.reg_confirm
                
                if not new_username or not new_password:
                    st.error("❌ Nazwa użytkownika i hasło są wymagane.")
                elif new_password != confirm_password:
                    st.error("❌ Hasła nie pasują do siebie.")
                else:
                    registration_result = register_user(new_username, new_password, confirm_password)
                    
                    if registration_result == "Registration successful!":
                        st.success("✅ Rejestracja udana! Przekierowuję do dashboardu...")
                        # Automatyczne logowanie po rejestracji
                        st.session_state.logged_in = True
                        st.session_state.username = new_username
                        st.session_state.page = 'dashboard'
                        st.rerun()
                    else:
                        st.error(f"❌ {registration_result}")
    
    # Info box na dole
    st.markdown("""
    <div class="info-box">
        <h4>🧠 Co zyskujesz?</h4>
        <p>Dostęp do interaktywnych lekcji, gier biznesowych, testów osobowości i narzędzi rozwojowych opartych na neuronaukach.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
