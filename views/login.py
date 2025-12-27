import streamlit as st
from data.users_sql import register_user, login_user
from utils.css_loader import ensure_css_files, load_login_css
from utils.scroll_utils import scroll_to_top
from utils.activity_tracker import initialize_activity_tracking
from config.settings import DEVELOPMENT_MODE

def show_login_page():
    # Ostrzeżenie o trybie developerskim
    if DEVELOPMENT_MODE:
        st.warning("⚡ **TRYB DEVELOPERSKI AKTYWNY** - Dane nie są zapisywane do plików (tylko w pamięci). Po restarcie aplikacji znikną.")
    
    # NIE UŻYWAMY apply_material3_theme() i add_animations_css() 
    # bo wstrzykują duże bloki CSS które zajmują miejsce na górze strony
    
    # Upewnij się, że pliki CSS istnieją i załaduj je
    ensure_css_files()
    load_login_css()
    
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
            max-width: 450px !important;
            padding-top: 0 !important;
            padding-bottom: 0.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            margin: 0 auto !important;
        }
        
        /* Biała karta główna */
        .main .block-container > div:first-child {
            background: white;
            border-radius: 20px;
            padding: 1.5rem 2rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
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
        
        /* Tytuł */
        .login-title {
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            color: #1a202c;
            margin-top: 0;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Formularz */
        .stTextInput > div > div > input {
            border-radius: 12px !important;
            border: 2px solid #e2e8f0 !important;
            padding: 12px 14px !important;
            font-size: 15px !important;
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
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 15px !important;
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
            margin-bottom: 1.5rem !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #64748b !important;
            font-weight: 500 !important;
            font-size: 15px !important;
            padding: 10px 20px !important;
            border-radius: 8px 8px 0 0 !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-weight: 600 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Tytuł (bez logo i motto) - na całą szerokość
    st.markdown('<h1 class="login-title">BrainVenture Academy</h1>', unsafe_allow_html=True)
    
    # Utwórz 3 kolumny: lewa pusta, środkowa z formularzem, prawa pusta
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
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
                        # Załaduj pełne dane użytkownika
                        from data.users import load_user_data
                        users_data = load_user_data()
                        
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_data = users_data.get(username, {})
                        st.session_state.page = 'dashboard'
                        
                        # Inicjalizuj activity tracking dla użytkownika
                        initialize_activity_tracking(username)
                        
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
                        # Rejestracja - nowa funkcja SQL zwraca True/False
                        success = register_user(new_username, new_password)
                        
                        if success:
                            # Załaduj pełne dane nowo utworzonego użytkownika
                            from data.users import load_user_data
                            users_data = load_user_data()
                            
                            st.success("✅ Rejestracja udana! Przekierowuję do dashboardu...")
                            # Automatyczne logowanie po rejestracji
                            st.session_state.logged_in = True
                            st.session_state.username = new_username
                            st.session_state.user_data = users_data.get(new_username, {})
                            st.session_state.page = 'dashboard'
                            
                            # Inicjalizuj activity tracking dla nowego użytkownika
                            initialize_activity_tracking(new_username)
                            
                            st.rerun()
                        else:
                            st.error("❌ Użytkownik już istnieje lub wystąpił błąd")
