"""
Moduł narzędzi AI dla BrainVenture Academy
Zawiera zaawansowane narzędzia do rozwoju umiejętności komunikacyjnych i przywództwa
"""

import streamlit as st
from utils.ai_exercises import AIExerciseEvaluator
from utils.components import zen_header, zen_button, stat_card
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, toggle_device_view
from utils.scroll_utils import scroll_to_top
import json
import os
import math
import re
from datetime import datetime
from typing import Dict, List, Optional
import io
import plotly.graph_objects as go
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from reportlab.pdfbase import pdfutils
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def save_leadership_profile(username: str, profile: Dict, profile_name: Optional[str] = None) -> bool:
    """Zapisuje profil przywódczy użytkownika"""
    try:
        # Ścieżka do pliku profili
        profiles_file = "leadership_profiles.json"
        
        # Wczytaj istniejące profile lub stwórz nowy słownik
        if os.path.exists(profiles_file):
            with open(profiles_file, 'r', encoding='utf-8') as f:
                profiles = json.load(f)
        else:
            profiles = {}
        
        # Migracja starych danych do nowej struktury
        if username in profiles:
            if not isinstance(profiles[username], dict) or "profiles" not in profiles[username]:
                # Stary format - przekształć do nowego
                old_profile = profiles[username] if username in profiles else {}
                profiles[username] = {"profiles": [old_profile] if old_profile else [], "current_profile": 0}
        
        # Struktura: profiles[username] = {"profiles": [lista_profili], "current_profile": index}
        if username not in profiles:
            profiles[username] = {"profiles": [], "current_profile": 0}
        
        # Dodaj metadata do profilu
        profile['created_at'] = datetime.now().isoformat()
        profile['username'] = username
        profile['profile_name'] = profile_name or f"Profil {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Dodaj nowy profil do listy (zawsze dodaj nowy zamiast nadpisywać)
        profiles[username]["profiles"].append(profile)
        profiles[username]["current_profile"] = len(profiles[username]["profiles"]) - 1
        
        # Ogranicz do ostatnich 10 profili
        if len(profiles[username]["profiles"]) > 10:
            profiles[username]["profiles"] = profiles[username]["profiles"][-10:]
            profiles[username]["current_profile"] = 9
        
        # Zapisz do pliku
        with open(profiles_file, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, ensure_ascii=False, indent=2)
            
        return True
    except Exception as e:
        st.error(f"Błąd zapisu profilu: {e}")
        return False

def load_leadership_profile(username: str, profile_index: Optional[int] = None) -> Optional[Dict]:
    """Wczytuje profil przywódczy użytkownika"""
    try:
        profiles_file = "leadership_profiles.json"
        
        if not os.path.exists(profiles_file):
            return None
            
        with open(profiles_file, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            
        user_data = profiles.get(username)
        if not user_data:
            return None
            
        # Obsługa starego formatu (backward compatibility)
        if isinstance(user_data, dict) and 'profiles' not in user_data:
            return user_data
            
        # Nowy format z listą profili
        if profile_index is not None:
            if 0 <= profile_index < len(user_data["profiles"]):
                return user_data["profiles"][profile_index]
        else:
            # Zwróć aktualny profil
            current_idx = user_data.get("current_profile", 0)
            if user_data["profiles"]:
                return user_data["profiles"][current_idx]
                
        return None
    except Exception as e:
        st.error(f"Błąd wczytywania profilu: {e}")
        return None

def get_user_profiles_history(username: str) -> List[Dict]:
    """Pobiera historię wszystkich profili użytkownika"""
    try:
        profiles_file = "leadership_profiles.json"
        
        if not os.path.exists(profiles_file):
            return []
            
        with open(profiles_file, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            
        user_data = profiles.get(username)
        if not user_data:
            return []
            
        # Obsługa starego formatu
        if isinstance(user_data, dict) and 'profiles' not in user_data:
            return [user_data]
            
        # Nowy format - zwróć wszystkie profile
        return user_data.get("profiles", [])
    except Exception:
        return []

def delete_user_profile(username: str, profile_index: Optional[int] = None) -> bool:
    """Usuwa profil użytkownika"""
    try:
        profiles_file = "leadership_profiles.json"
        
        if not os.path.exists(profiles_file):
            return True
            
        with open(profiles_file, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            
        user_data = profiles.get(username)
        if not user_data:
            return True
            
        if profile_index is not None:
            # Usuń konkretny profil
            if isinstance(user_data, dict) and 'profiles' in user_data:
                if 0 <= profile_index < len(user_data["profiles"]):
                    user_data["profiles"].pop(profile_index)
                    # Zaktualizuj current_profile jeśli potrzeba
                    if user_data["current_profile"] >= len(user_data["profiles"]):
                        user_data["current_profile"] = max(0, len(user_data["profiles"]) - 1)
        else:
            # Usuń wszystkie profile użytkownika
            del profiles[username]
            
        # Zapisz zmiany
        with open(profiles_file, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, ensure_ascii=False, indent=2)
            
        return True
    except Exception as e:
        st.error(f"Błąd usuwania profilu: {e}")
        return False

def show_autodiagnosis():
    """Narzędzia autodiagnozy"""
    st.markdown("### 🎯 Autodiagnoza")
    st.markdown("Poznaj swój styl uczenia się, typ neuroleadera i preferowane sposoby rozwoju")
    
    # Wyświetl testy w dwóch kolumnach
    col1, col2 = st.columns(2)
    
    # Karta z testem Neurolidera
    with col1:
        st.markdown("""
        <div style='padding: 20px; border: 2px solid #E91E63; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%);'>
            <h4>🧠 Test typu Neurolidera</h4>
            <p><strong>Odkryj swój unikalny styl przywództwa i maksymalizuj swój potencjał lidera</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>🎯 Kompleksowa analiza stylu przywództwa</li>
                <li>📊 Wykres radarowy kompetencji</li>
                <li>💪 Identyfikacja mocnych stron i wyzwań</li>
                <li>🎓 Spersonalizowane strategie rozwoju</li>
                <li>🧩 Dopasowanie do ról biznesowych</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if zen_button("🧠 Rozpocznij Test Neurolidera", key="neuroleader_test", width='stretch'):
            st.session_state.active_tool = "neuroleader_test"
    
    # Karta z testem Kolba
    with col2:
        st.markdown("""
        <div style='padding: 20px; border: 2px solid #9C27B0; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);'>
            <h4>🔄 Test stylów uczenia się według Kolba</h4>
            <p><strong>Odkryj swój preferowany styl uczenia się i maksymalizuj efektywność rozwoju</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>🔍 12 pytań diagnostycznych</li>
                <li>🎯 Identyfikacja dominującego stylu </li>
                <li>💪 Analiza mocnych stron w uczeniu się</li>
                <li>💡 Spersonalizowane wskazówki rozwojowe</li>
                <li>🔄 Zrozumienie pełnego cyklu uczenia się Kolba</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if zen_button("🔄 Rozpocznij Test Kolba", key="kolb_test", width='stretch'):
            st.session_state.active_tool = "kolb_test"
    
    # Wyświetl odpowiedni test jeśli jest aktywny
    active_tool = st.session_state.get('active_tool')
    
    if active_tool == "neuroleader_test":
        st.markdown("---")
        # Import funkcji z profile.py
        from views.profile import show_neuroleader_test_section
        show_neuroleader_test_section()
    
    elif active_tool == "kolb_test":
        st.markdown("---")
        show_kolb_test()

def show_kolb_test():
    """Wyświetla test stylów uczenia się według Kolba"""
    st.markdown("### 🔄 Kolb Experiential Learning Profile (KELP)")
    
    # Wczytaj zapisane wyniki z bazy danych (jeśli użytkownik zalogowany)
    # ALE TYLKO jeśli użytkownik nie kliknął "Rozpocznij test od nowa"
    if st.session_state.get('logged_in') and st.session_state.get('username'):
        from data.users import load_user_data
        
        users_data = load_user_data()
        username = st.session_state.username
        
        # Sprawdź czy użytkownik nie zresetował testu celowo
        if username in users_data and users_data[username].get('kolb_test'):
            # Jeśli użytkownik ma zapisane wyniki, wczytaj je do session state
            kolb_data = users_data[username]['kolb_test']
            
            # Sprawdź czy session state nie ma już wczytanych wyników
            # ORAZ czy użytkownik nie kliknął "reset" (sprawdzamy flagę kolb_reset)
            if not st.session_state.get('kolb_completed') and not st.session_state.get('kolb_reset'):
                st.session_state.kolb_results = kolb_data.get('scores', {})
                st.session_state.kolb_dimensions = kolb_data.get('dimensions', {})
                st.session_state.kolb_dominant = kolb_data.get('dominant_style')
                st.session_state.kolb_quadrant = kolb_data.get('quadrant')
                st.session_state.kolb_flexibility = kolb_data.get('flexibility', 0)
                st.session_state.kolb_completed = True
                
                # Informacja o wczytaniu zapisanych wyników
                st.info(f"✅ Wczytano Twoje wcześniejsze wyniki testu z dnia: {kolb_data.get('completed_date', 'Nieznana')}")
    
    # Karta z teorią ELT
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                box-shadow: 0 4px 15px rgba(102,126,234,0.4); 
                border-radius: 20px; 
                padding: 30px; 
                margin: 20px 0; 
                color: white;'>
        <div style='font-size: 2.5em; margin-bottom: 15px;'>📚</div>
        <h4 style='color: white; margin: 0 0 20px 0;'>Teoria Uczenia się przez Doświadczenie (ELT)</h4>
        <p style='font-size: 1.1em; line-height: 1.7; margin-bottom: 0;'>
            Teoria Davida Kolba z 1984 roku definiuje uczenie się jako <b>dynamiczny proces</b>, 
            w którym wiedza jest tworzona poprzez <b>transformację doświadczenia</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Karty z czterema fazami cyklu
    st.markdown("<h4 style='margin: 30px 0 20px 0; color: #333;'>🔄 Cykl Uczenia się Kolba - Cztery Fazy:</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%); 
                    box-shadow: 0 3px 10px rgba(231,76,60,0.3); 
                    border-radius: 15px; 
                    padding: 20px; 
                    margin: 10px 0; 
                    color: white;'>
        <div style='font-size: 2.5em; margin-bottom: 15px;'></div>
            <h5 style='color: white; margin: 0 0 10px 0;'>1. Konkretne Doświadczenie (CE)</h5>
            <p style='margin: 0; font-size: 0.95em; line-height: 1.6;'>
                Zetknięcie się z nową sytuacją<br><b>→ Feeling (Odczuwanie)</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%); 
                    box-shadow: 0 3px 10px rgba(155,89,182,0.3); 
                    border-radius: 15px; 
                    padding: 20px; 
                    margin: 10px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'></div>
            <h5 style='color: white; margin: 0 0 10px 0;'>3. Abstrakcyjna Konceptualizacja (AC)</h5>
            <p style='margin: 0; font-size: 0.95em; line-height: 1.6;'>
                Tworzenie teorii i uogólnień<br><b>→ Thinking (Myślenie)</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%); 
                    box-shadow: 0 3px 10px rgba(74,144,226,0.3); 
                    border-radius: 15px; 
                    padding: 20px; 
                    margin: 10px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'></div>
            <h5 style='color: white; margin: 0 0 10px 0;'>2. Refleksyjna Obserwacja (RO)</h5>
            <p style='margin: 0; font-size: 0.95em; line-height: 1.6;'>
                Obserwacja i refleksja<br><b>→ Watching (Obserwowanie)</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%); 
                    box-shadow: 0 3px 10px rgba(46,204,113,0.3); 
                    border-radius: 15px; 
                    padding: 20px; 
                    margin: 10px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'></div>
            <h5 style='color: white; margin: 0 0 10px 0;'>4. Aktywne Eksperymentowanie (AE)</h5>
            <p style='margin: 0; font-size: 0.95em; line-height: 1.6;'>
                Testowanie koncepcji w praktyce<br><b>→ Doing (Działanie)</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Karta z wymiarami biegunowymi
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                box-shadow: 0 3px 12px rgba(240,147,251,0.4); 
                border-radius: 18px; 
                padding: 25px; 
                margin: 25px 0; 
                color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'></div>
        <h5 style='color: white; margin: 0 0 15px 0;'>Wymiary Biegunowe:</h5>
        <ul style='margin: 0; padding-left: 20px; line-height: 2;'>
            <li><b>Oś Postrzegania:</b> Konkretne Przeżycie (CE) ↔ Abstrakcyjna Konceptualizacja (AC)</li>
            <li><b>Oś Przetwarzania:</b> Refleksyjna Obserwacja (RO) ↔ Aktywne Eksperymentowanie (AE)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Karta z celem testu
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); 
                box-shadow: 0 3px 10px rgba(255,234,167,0.3); 
                border-radius: 15px; 
                padding: 20px; 
                margin: 20px 0; 
                color: #222;'>
        <div style='font-size: 2em; margin-bottom: 10px;'></div>
        <h5 style='margin: 0 0 10px 0; color: #e17055;'>Cel testu:</h5>
        <p style='margin: 0; font-size: 1.05em; line-height: 1.7;'>
            Zidentyfikować Twój <b>preferowany styl uczenia się</b> i ocenić <b>elastyczność</b> 
            w przechodzeniu przez pełny cykl Kolba.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicjalizacja state
    if 'kolb_answers' not in st.session_state:
        st.session_state.kolb_answers = {}
    if 'kolb_completed' not in st.session_state:
        st.session_state.kolb_completed = False
    
    # Pytania testowe - 12 pytań z 4 opcjami każde (odpowiadające CE, RO, AC, AE)
    # Format zgodny z LSI: ranking wymuszony wybór
    questions = [
        {
            "id": 1,
            "question": "Kiedy uczę się czegoś nowego, najlepiej mi się pracuje gdy:",
            "options": {
                "CE": "Angażuję się osobiście i uczę się przez doświadczenie",
                "RO": "Mam czas na obserwację i refleksję",
                "AC": "Mogę analizować i tworzyć logiczne teorie",
                "AE": "Mogę aktywnie testować i eksperymentować"
            }
        },
        {
            "id": 2,
            "question": "W procesie uczenia się najbardziej cenię:",
            "options": {
                "CE": "Konkretne przykłady i osobiste doświadczenia",
                "RO": "Możliwość przemyślenia i obserwacji",
                "AC": "Abstrakcyjne koncepcje i modele teoretyczne",
                "AE": "Praktyczne zastosowania i działanie"
            }
        },
        {
            "id": 3,
            "question": "Podczas rozwiązywania problemów:",
            "options": {
                "CE": "Polegam na intuicji i uczuciach",
                "RO": "Słucham różnych perspektyw i zbieramy informacje",
                "AC": "Analizuję logicznie i systematycznie",
                "AE": "Testuję różne rozwiązania w praktyce"
            }
        },
        {
            "id": 4,
            "question": "W zespole najlepiej funkcjonuję jako:",
            "options": {
                "CE": "Osoba, która wnosi osobiste zaangażowanie i empatię",
                "RO": "Obserwator, który dostrzega różne perspektywy",
                "AC": "Analityk, który tworzy strategie i plany",
                "AE": "Praktyk, który wdraża i koordynuje działania"
            }
        },
        {
            "id": 5,
            "question": "Podczas szkolenia/warsztatu najbardziej odpowiada mi:",
            "options": {
                "CE": "Osobiste zaangażowanie i doświadczenie sytuacji",
                "RO": "Czas na dyskusję i przemyślenie tematu",
                "AC": "Solidne podstawy teoretyczne i modele",
                "AE": "Praktyczne ćwiczenia i testowanie umiejętności"
            }
        },
        {
            "id": 6,
            "question": "Podejmuję decyzje głównie na podstawie:",
            "options": {
                "CE": "Osobistych wartości i bezpośredniego doświadczenia",
                "RO": "Obserwacji sytuacji i przemyśleń",
                "AC": "Logicznej analizy i racjonalnych przesłanek",
                "AE": "Praktycznych testów i sprawdzania w działaniu"
            }
        },
        {
            "id": 7,
            "question": "W sytuacji nowej/stresowej:",
            "options": {
                "CE": "Kieruję się emocjami i bezpośrednim odczuciem",
                "RO": "Wycofuję się i najpierw obserwuję",
                "AC": "Szukam racjonalnych wyjaśnień i teorii",
                "AE": "Działam szybko i sprawdzam co zadziała"
            }
        },
        {
            "id": 8,
            "question": "Moja największa mocna strona to:",
            "options": {
                "CE": "Empatia i wrażliwość na ludzi",
                "RO": "Umiejętność słuchania i refleksji",
                "AC": "Zdolności analityczne i logiczne myślenie",
                "AE": "Praktyczność i skuteczność działania"
            }
        },
        {
            "id": 9,
            "question": "Przy nauce nowego narzędzia/programu:",
            "options": {
                "CE": "Eksperymentuję swobodnie i uczę się przez próby",
                "RO": "Obserwuję innych i czytam opinie",
                "AC": "Czytam dokumentację i poznaję strukturę",
                "AE": "Od razu zaczynam używać i testuję funkcje"
            }
        },
        {
            "id": 10,
            "question": "W projektach zawodowych najbardziej lubię:",
            "options": {
                "CE": "Pracę z ludźmi i budowanie relacji",
                "RO": "Analizowanie danych i integrację różnych perspektyw",
                "AC": "Tworzenie strategii i systemów",
                "AE": "Realizację konkretnych zadań i wdrażanie"
            }
        },
        {
            "id": 11,
            "question": "Najlepiej pamiętam, gdy:",
            "options": {
                "CE": "Czuję emocjonalne połączenie z tematem",
                "RO": "Mam czas na obserwację i rozważanie",
                "AC": "Rozumiem logikę i teorię stojącą za tym",
                "AE": "Praktykuję i wielokrotnie testuję"
            }
        },
        {
            "id": 12,
            "question": "Mój naturalny sposób działania to:",
            "options": {
                "CE": "Spontaniczne reagowanie na sytuacje",
                "RO": "Cierpliwe obserwowanie przed działaniem",
                "AC": "Systematyczne planowanie i analizowanie",
                "AE": "Szybkie podejmowanie decyzji i działanie"
            }
        }
    ]
    
    # Wyświetl pytania TYLKO jeśli test nie został ukończony
    if not st.session_state.kolb_completed:
        st.markdown("---")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                    border-radius: 12px; 
                    padding: 15px; 
                    margin: 20px 0; 
                    text-align: center;'>
            <h4 style='margin: 0; color: #2c3e50;'>📝 Odpowiedz na poniższe pytania</h4>
            <p style='margin: 5px 0 0 0; color: #555;'>Wybierz opcję najbardziej do Ciebie pasującą</p>
        </div>
        """, unsafe_allow_html=True)
        
        for q in questions:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                        border-left: 5px solid #3498db; 
                        border-radius: 10px; 
                        padding: 20px; 
                        margin: 15px 0; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h5 style='margin: 0 0 15px 0; color: #2c3e50;'>
                    <span style='background: #3498db; color: white; padding: 5px 12px; border-radius: 50%; margin-right: 10px;'>{q['id']}</span>
                    {q['question']}
                </h5>
            </div>
            """, unsafe_allow_html=True)
            
            answer = st.radio(
                f"Pytanie {q['id']}",
                options=list(q['options'].keys()),
                format_func=lambda x, opts=q['options']: opts[x],
                key=f"kolb_q{q['id']}",
                label_visibility="collapsed"
            )
            st.session_state.kolb_answers[q['id']] = answer
            st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
        
        # Przycisk do obliczenia wyniku
        if st.button("📊 Oblicz mój styl uczenia się", type="primary", use_container_width=True):
            if len(st.session_state.kolb_answers) == len(questions):
                calculate_kolb_results()
                st.session_state.kolb_completed = True
                st.rerun()
            else:
                st.warning("⚠️ Proszę odpowiedzieć na wszystkie pytania")
    
    # Wyświetl wyniki jeśli test został ukończony
    if st.session_state.kolb_completed:
        display_kolb_results()

def generate_kolb_ai_tips(learning_style: str, profession: str):
    """Generuje spersonalizowane wskazówki AI na podstawie stylu uczenia się i zawodu"""
    try:
        import google.generativeai as genai
        
        # Pobierz klucz API z secrets
        api_key = st.secrets.get("GOOGLE_API_KEY")
        
        if not api_key:
            st.error("❌ Klucz API Google Gemini nie jest skonfigurowany. Skontaktuj się z administratorem.")
            return
        
        # Konfiguruj Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            st.secrets.get("AI_SETTINGS", {}).get("gemini_model", "gemini-2.5-flash")
        )
        
        # Mapowanie stylów na opisy (zgodnie z naukową dokumentacją ELT)
        style_descriptions = {
            "Diverging (Wyobraźnia/Imagination)": "osoba ucząca się przez konkretne doświadczenia i refleksyjną obserwację, postrzegająca sytuacje z wielu perspektyw, ceniąca wyobraźnię i emocjonalne zaangażowanie",
            "Assimilating (Teoria/Thinking)": "osoba ucząca się przez abstrakcyjną konceptualizację i refleksyjną obserwację, ceniąca logiczne modele i systematyczne podejście teoretyczne",
            "Converging (Decyzja/Decision)": "osoba ucząca się przez abstrakcyjną konceptualizację i aktywne eksperymentowanie, skupiona na praktycznym zastosowaniu teorii i rozwiązywaniu problemów",
            "Accommodating (Działanie/Action)": "osoba ucząca się przez konkretne doświadczenia i aktywne eksperymentowanie, ceniąca intuicję, elastyczność i praktyczne działanie"
        }
        
        prompt = f"""Jesteś ekspertem od rozwoju zawodowego i stylów uczenia się według teorii Experiential Learning Theory (ELT) Davida Kolba.

Użytkownik to {profession}, którego dominującym stylem uczenia się jest: **{learning_style}**
({style_descriptions.get(learning_style, '')})

Wygeneruj **konkretne, praktyczne wskazówki** dostosowane do tego stylu uczenia się.

KRYTYCZNE WYMAGANIA FORMATOWANIA:

1. Utwórz dokładnie 3 sekcje z nagłówkami:
   **Optymalne warunki dla Twojej nauki:**
   **Jak wzmacniać swoje mocne strony:**
   **Jak rozwijać obszary do rozwoju:**

2. Każdy nagłówek MUSI być w osobnej linii i po nim MUSI być pusta linia

3. Pod każdym nagłówkiem utwórz dokładnie 3 punkty rozpoczynające się od "- "

4. W sekcji "Jak wzmacniać swoje mocne strony" każdy punkt powinien zaczynać się od pogrubionej nazwy mocnej strony, np:
   - **Empatia:** Wykorzystuj swoją wrażliwość do...
   - **Kreatywność:** Twoja wyobraźnia pozwala na...

5. W sekcji "Jak rozwijać obszary do rozwoju" każdy punkt powinien zaczynać się od pogrubionej nazwy obszaru, np:
   - **Podejmowanie decyzji:** Aby szybciej decydować, wypróbuj...
   - **Praktyczne wdrażanie:** Rozwijaj tę umiejętność przez...

TREŚĆ:
- Bardzo konkretne wskazówki możliwe do wdrożenia natychmiast
- Dostosowane do stylu {learning_style} i zawodu {profession}
- Każdy punkt max 2-3 zdania
- W języku polskim
- BEZ formatowania HTML
- NIE używaj zwrotów typu "Warunek 1", "Mocna strona 2", "Obszar rozwoju 3" - pisz bezpośrednio o konkretnej umiejętności/warunku
"""
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            ai_tips = response.text
            st.session_state.kolb_ai_tips = ai_tips
            st.success("✅ Wskazówki zostały wygenerowane!")
        else:
            st.error("❌ Nie otrzymano odpowiedzi od AI")
            st.session_state.kolb_ai_tips = None
        
    except Exception as e:
        st.error(f"❌ Błąd generowania wskazówek: {str(e)}")
        import traceback
        st.error(f"Szczegóły: {traceback.format_exc()}")
        st.session_state.kolb_ai_tips = None

def calculate_kolb_results():
    """Oblicza wyniki testu Kolba zgodnie z metodologią LSI"""
    answers = st.session_state.kolb_answers
    
    # Liczenie punktów dla każdej zdolności uczenia się
    # CE = Konkretne Doświadczenie (Concrete Experience - Feeling)
    # RO = Refleksyjna Obserwacja (Reflective Observation - Watching)
    # AC = Abstrakcyjna Konceptualizacja (Abstract Conceptualization - Thinking)
    # AE = Aktywne Eksperymentowanie (Active Experimentation - Doing)
    
    scores = {"CE": 0, "RO": 0, "AC": 0, "AE": 0}
    
    for answer in answers.values():
        scores[answer] += 1
    
    # Obliczanie wymiarów różnicowych (zgodnie z metodologią LSI)
    # Wymiar Postrzegania (Oś Abstrakcja-Konkret)
    ac_ce = scores["AC"] - scores["CE"]  # Dodatni = preferencja AC, Ujemny = preferencja CE
    
    # Wymiar Przetwarzania (Oś Aktywność-Refleksja)
    ae_ro = scores["AE"] - scores["RO"]  # Dodatni = preferencja AE, Ujemny = preferencja RO
    
    # Określenie stylu na podstawie wymiarów (siatka 2x2)
    if ac_ce > 0 and ae_ro > 0:
        dominant_style = "Converging (Konwergent)"
        quadrant = "AC/AE"
    elif ac_ce > 0 and ae_ro <= 0:
        dominant_style = "Assimilating (Asymilator)"
        quadrant = "AC/RO"
    elif ac_ce <= 0 and ae_ro > 0:
        dominant_style = "Accommodating (Akomodator)"
        quadrant = "CE/AE"
    else:  # ac_ce <= 0 and ae_ro <= 0
        dominant_style = "Diverging (Dywergent)"
        quadrant = "CE/RO"
    
    # Obliczenie elastyczności uczenia się (odległość od centrum siatki)
    # Im bliżej centrum (0,0), tym większa elastyczność
    distance_from_center = math.sqrt(ac_ce**2 + ae_ro**2)
    max_distance = math.sqrt(12**2 + 12**2)  # Maksymalna odległość przy 12 pytaniach
    flexibility_score = 100 - (distance_from_center / max_distance * 100)
    
    # Zapisz wyniki w session state
    st.session_state.kolb_results = scores
    st.session_state.kolb_dimensions = {
        "AC-CE": ac_ce,
        "AE-RO": ae_ro
    }
    st.session_state.kolb_dominant = dominant_style
    st.session_state.kolb_quadrant = quadrant
    st.session_state.kolb_flexibility = flexibility_score
    
    # Zapisz wyniki do danych użytkownika (persistent storage)
    if st.session_state.get('logged_in') and st.session_state.get('username'):
        from data.users import load_user_data, save_user_data
        from datetime import datetime
        
        users_data = load_user_data()
        username = st.session_state.username
        
        if username in users_data:
            # Zapisz wyniki testu Kolba
            users_data[username]['kolb_test'] = {
                'scores': scores,  # CE, RO, AC, AE punkty
                'dimensions': {
                    'AC-CE': ac_ce,
                    'AE-RO': ae_ro
                },
                'dominant_style': dominant_style,
                'quadrant': quadrant,
                'flexibility': round(flexibility_score, 2),
                'completed_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            save_user_data(users_data)
            
            # Zaloguj ukończenie testu i przyznaj XP
            try:
                from data.users import award_xp_for_activity
                award_xp_for_activity(
                    username,
                    'test_completed',
                    5,  # 5 XP za ukończenie testu Kolba
                    {
                        'test_name': 'Kolb Learning Styles',
                        'dominant_style': dominant_style,
                        'quadrant': quadrant
                    }
                )
            except Exception:
                pass
    
    # Wyczyść flagę reset po zapisaniu nowych wyników (pozwól na auto-load przy kolejnym logowaniu)
    st.session_state.kolb_reset = False

def format_ai_tips_compact(ai_tips_text: str) -> str:
    """
    Formatuje tekst AI na kompaktową strukturę z kategoriami i punktami.
    Wykrywa sekcje i przekształca je w wizualne boxy.
    Radzi sobie z różnymi formatami AI (wieloliniowe i jednoliniowe punkty).
    """
    import re
    
    # Ikony dla różnych kategorii
    category_icons = {
        'optymalne warunki': '🌟',
        'warunki': '🌟',
        'nauki': '📖',
        'mocne strony': '💪',
        'wzmacniać': '💪',
        'silne': '💪',
        'obszary do rozwoju': '🚀',
        'rozwijać': '🚀',
        'słabe': '🚀',
        'rozwój': '🚀',
        'metody': '📚',
        'technik': '🔧',
        'narzędzi': '🛠️',
        'strategi': '🎯',
        'ćwicz': '💪',
        'przykład': '✨',
        'zalec': '👍',
        'unikaj': '⚠️',
        'rozwój': '🚀',
        'praktyk': '⚡',
        'tips': '💡',
        'wskazówk': '💡',
        'zastosow': '🔍',
        'sposób': '📋',
        'korzyść': '🌟'
    }
    
    # Najpierw podziel tekst na sekcje przez nagłówki **Header**:
    # Użyj regex aby znaleźć sekcje - TYLKO te które są na początku linii i kończą się dwukropkiem + newline
    section_pattern = r'^\*\*(.+?)\*\*:\s*$'
    
    lines = ai_tips_text.strip().split('\n')
    formatted_sections = []
    current_section = None
    current_items = []
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # Sprawdź czy to nagłówek sekcji (linia zawiera TYLKO **Nagłówek**: i nic więcej)
        header_match = re.match(section_pattern, line_stripped)
        
        if header_match and len(line_stripped) < 80:  # Nagłówki są krótkie (max 80 znaków)
            # To jest nagłówek sekcji
            if current_section and current_items:
                formatted_sections.append((current_section, current_items))
            
            current_section = header_match.group(1).strip()
            current_items = []
        else:
            # To jest zawartość (może zawierać **bold:** wewnątrz)
            # Usuń bullet points z początku
            clean_line = re.sub(r'^[-•*]+\s*', '', line_stripped)
            clean_line = clean_line.strip()
            
            if clean_line:
                if not current_section:
                    current_section = "Wskazówki"
                current_items.append(clean_line)
    
    # Dodaj ostatnią sekcję
    if current_section and current_items:
        formatted_sections.append((current_section, current_items))
    
    # Jeśli nadal nic nie wykryto, fallback
    if not formatted_sections and ai_tips_text.strip():
        # Podziel po kropkach lub nowych liniach
        items = [item.strip() for item in re.split(r'[.\n]+', ai_tips_text) if item.strip()]
        if items:
            formatted_sections.append(("Wskazówki AI", items))
    
    # Generuj HTML
    html_parts = []
    
    # Filtruj puste sekcje
    formatted_sections = [(title, items) for title, items in formatted_sections if items]
    
    if not formatted_sections:
        # Fallback - surowy tekst
        return f'''
        <div class="ai-tip-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 20px; border-radius: 8px;">
            <h3 style="margin: 0 0 10px 0; font-size: 16px; font-weight: bold;">💡 Wskazówki AI</h3>
            <div style="margin: 0; padding-left: 10px;">
                {ai_tips_text.replace(chr(10), '<br>')}
            </div>
        </div>
        '''
    
    for i, (title, items) in enumerate(formatted_sections):
        # Usuń emoji z tytułu jeśli już jest
        title = re.sub(r'^[\U0001F300-\U0001F9FF]\s*', '', title)
        
        # Wybierz ikonę
        icon = '📌'
        title_lower = title.lower()
        for key, emoji in category_icons.items():
            if key in title_lower:
                icon = emoji
                break
        
        # Kolory naprzemienne
        colors = [
            ('linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 'white'),
            ('linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', 'white'),
            ('linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', 'white'),
            ('linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', '#333'),
            ('linear-gradient(135deg, #fa709a 0%, #fee140 100%)', '#333'),
        ]
        bg, text_color = colors[i % len(colors)]
        
        # Box z nagłówkiem i klasą CSS - używamy div zamiast ul/li dla lepszego renderowania w PDF
        html_parts.append(f'''
        <div class="ai-tip-box" style="background: {bg}; color: {text_color}; padding: 12px 18px; border-radius: 8px; margin-bottom: 15px;">
            <h3 style="margin: 0 0 10px 0; font-size: 16px; font-weight: bold;">{icon} {title}</h3>
            <div style="margin: 0; padding-left: 10px;">
        ''')
        
        for item in items:
            # Sprawdź czy punkt zaczyna się od **Bold tekst:**
            bold_prefix_match = re.match(r'^\*\*(.+?)\*\*:\s*(.+)', item)
            
            if bold_prefix_match:
                # Punkt ma bold prefix
                bold_text = bold_prefix_match.group(1).strip()
                rest_text = bold_prefix_match.group(2).strip()
                clean_item = f'<strong>{bold_text}:</strong> {rest_text}'
            else:
                # Zwykły punkt - usuń gwiazdki z tekstu i zamień na <strong>
                clean_item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
            
            # Usuń ewentualne podwójne spacje
            clean_item = re.sub(r'\s+', ' ', clean_item).strip()
            
            if clean_item:
                # Każdy punkt jako osobny div z margin-bottom dla separacji
                html_parts.append(f'<div style="margin-bottom: 8px; line-height: 1.6; font-size: 14px;">▸ {clean_item}</div>')
        
        html_parts.append('</div></div>')
    
    return '\n'.join(html_parts)

def format_ai_tips_for_streamlit(ai_tips_text: str) -> str:
    """
    Formatuje tekst AI dla Streamlit (bez HTML, używa markdown i emoji).
    Zwraca czysty tekst z emoji i strukturą do wyświetlenia przez st.markdown().
    """
    import re
    
    # Podziel tekst na sekcje - nagłówki to linie z **Tekst:**
    section_pattern = r'^\*\*(.+?)\*\*:?\s*$'
    
    lines = ai_tips_text.strip().split('\n')
    sections = []
    current_section = None
    current_items = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Pomiń puste linie między sekcjami
        if not line_stripped:
            continue
        
        # Sprawdź czy to nagłówek sekcji
        header_match = re.match(section_pattern, line_stripped)
        
        # Nagłówek = krótka linia (max 100 znaków) z **Tekst:**
        if header_match and len(line_stripped) < 100:
            # To jest nagłówek - zapisz poprzednią sekcję
            if current_section and current_items:
                sections.append((current_section, current_items))
            
            current_section = header_match.group(1).strip().rstrip(':')
            current_items = []
        else:
            # To jest zawartość punktu
            # Usuń bullet points i spacje
            clean_line = re.sub(r'^[-•*]\s*', '', line_stripped)
            clean_line = clean_line.strip()
            
            if clean_line:
                if not current_section:
                    # Jeśli nie ma sekcji, utwórz domyślną
                    current_section = "Wskazówki"
                current_items.append(clean_line)
    
    # Dodaj ostatnią sekcję
    if current_section and current_items:
        sections.append((current_section, current_items))
    
    # Jeśli nie wykryto sekcji, spróbuj przetworzyć jako jeden blok
    if not sections:
        # Spróbuj podzielić po pustych liniach i nagłówkach inline
        fallback_sections = []
        current_section = "Wskazówki"
        current_items = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Sprawdź czy linia zawiera inline nagłówek **Tekst:** tekst
            inline_match = re.match(r'^\*\*(.+?)\*\*:\s*(.+)', line)
            if inline_match and len(inline_match.group(1)) < 50:
                if current_items:
                    fallback_sections.append((current_section, current_items))
                current_section = inline_match.group(1).strip()
                current_items = [inline_match.group(2).strip()]
            else:
                clean_line = re.sub(r'^[-•*]\s*', '', line)
                if clean_line:
                    current_items.append(clean_line)
        
        if current_items:
            fallback_sections.append((current_section, current_items))
        
        sections = fallback_sections if fallback_sections else []
    
    # Jeśli nadal nie ma sekcji, zwróć surowy tekst
    if not sections:
        return ai_tips_text
    
    # Generuj markdown dla Streamlit
    result_parts = []
    
    for section_title, items in sections:
        # Wybierz emoji na podstawie tytułu sekcji
        icon = '📌'
        title_lower = section_title.lower()
        if 'warunki' in title_lower or 'optymalne' in title_lower:
            icon = '🌟'
        elif 'mocn' in title_lower or 'wzmacnia' in title_lower or 'siln' in title_lower:
            icon = '💪'
        elif 'rozwój' in title_lower or 'rozwija' in title_lower or 'słab' in title_lower or 'obszar' in title_lower:
            icon = '🚀'
        
        # Dodaj nagłówek sekcji
        result_parts.append(f"\n#### {icon} {section_title}\n")
        
        # Dodaj punkty
        for item in items:
            # Sprawdź czy punkt ma bold prefix **Tekst:**
            bold_prefix_match = re.match(r'^\*\*(.+?)\*\*:\s*(.+)', item)
            
            if bold_prefix_match:
                # Punkt ma bold prefix
                bold_text = bold_prefix_match.group(1).strip()
                rest_text = bold_prefix_match.group(2).strip()
                result_parts.append(f"- **{bold_text}:** {rest_text}")
            else:
                # Zwykły punkt - zostaw **bold** jak jest
                result_parts.append(f"- {item}")
        
        result_parts.append("")  # Pusta linia po sekcji
    
    return '\n'.join(result_parts)

def generate_kolb_html_report() -> str:
    """Generuje raport HTML z wynikami testu Kolba - gotowy do druku jako PDF"""
    
    # Pobierz dane z session state
    results = st.session_state.kolb_results
    dimensions = st.session_state.kolb_dimensions
    dominant = st.session_state.kolb_dominant
    quadrant = st.session_state.kolb_quadrant
    flexibility = st.session_state.kolb_flexibility
    username = st.session_state.get('username', 'Użytkownik')
    
    # Przygotuj dane dla wykresów
    ability_info = {
        "CE": {"name": "Konkretne Doświadczenie", "emoji": "❤️", "color": "#E74C3C", "desc": "Feeling"},
        "RO": {"name": "Refleksyjna Obserwacja", "emoji": "👁️", "color": "#4A90E2", "desc": "Watching"},
        "AC": {"name": "Abstrakcyjna Konceptualizacja", "emoji": "🧠", "color": "#9B59B6", "desc": "Thinking"},
        "AE": {"name": "Aktywne Eksperymentowanie", "emoji": "⚙️", "color": "#2ECC71", "desc": "Doing"}
    }
    
    # Wygeneruj wykres słupkowy jako HTML (Plotly offline)
    abilities_order = ['CE', 'RO', 'AC', 'AE']
    scores = [results[a] for a in abilities_order]
    colors = [ability_info[a]['color'] for a in abilities_order]
    
    # Etykiety w dwóch liniach dla lepszej czytelności
    labels_multiline = [
        'Konkretne<br>Doświadczenie',
        'Refleksyjna<br>Obserwacja',
        'Abstrakcyjna<br>Konceptualizacja',
        'Aktywne<br>Eksperymentowanie'
    ]
    
    # Wykres słupkowy
    fig_bar = go.Figure(data=[
        go.Bar(
            x=labels_multiline,  # Etykiety w dwóch liniach
            y=scores,
            marker=dict(color=colors),
            text=scores,
            textposition='outside',
            textfont=dict(size=16, color='#333')
        )
    ])
    fig_bar.update_layout(
        title='Zdolności Podstawowe w Cyklu Kolba',
        xaxis=dict(tickangle=0, tickfont=dict(size=12)),  # Poziome etykiety
        yaxis=dict(title='Wynik (punkty)', range=[0, 13]),
        width=650,  # Fixed width - bezpieczna szerokość dla A4
        height=350,  # Zwiększone z 300 dla etykiet X
        margin=dict(t=50, b=80, l=50, r=40),  # Zmniejszony dolny margines (etykiety 2-liniowe)
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Konwertuj wykres do HTML (inline, bez CDN)
    bar_chart_html = fig_bar.to_html(
        include_plotlyjs='inline',  # Osadź plotly.js w HTML
        div_id='bar_chart',
        config={'displayModeBar': False}  # Ukryj toolbar
    )
    
    # Wygeneruj wykres siatki
    x_coord = dimensions['AE-RO']
    y_coord = dimensions['AC-CE']
    
    fig_grid = go.Figure()
    
    # Dodaj tło ćwiartek
    quadrant_colors = {
        'Diverging': 'rgba(231, 76, 60, 0.15)',
        'Assimilating': 'rgba(155, 89, 182, 0.15)',
        'Converging': 'rgba(52, 152, 219, 0.15)',
        'Accommodating': 'rgba(46, 204, 113, 0.15)'
    }
    
    quadrant_positions = {
        'Diverging': {'x': [-12, 0], 'y': [-12, 0], 'label_x': -6, 'label_y': -6},
        'Assimilating': {'x': [-12, 0], 'y': [0, 12], 'label_x': -6, 'label_y': 6},
        'Converging': {'x': [0, 12], 'y': [0, 12], 'label_x': 6, 'label_y': 6},
        'Accommodating': {'x': [0, 12], 'y': [-12, 0], 'label_x': 6, 'label_y': -6}
    }
    
    for style_name, pos in quadrant_positions.items():
        fig_grid.add_shape(
            type="rect",
            x0=pos['x'][0], x1=pos['x'][1],
            y0=pos['y'][0], y1=pos['y'][1],
            fillcolor=quadrant_colors[style_name],
            line=dict(width=0)
        )
        fig_grid.add_annotation(
            x=pos['label_x'], y=pos['label_y'],
            text=f"<b>{style_name}</b>",
            showarrow=False,
            font=dict(size=12, color='rgba(0,0,0,0.5)')
        )
    
    # Dodaj punkt użytkownika
    fig_grid.add_trace(go.Scatter(
        x=[x_coord], y=[y_coord],
        mode='markers+text',
        marker=dict(size=20, color='red', symbol='star'),
        text=['Ty'],
        textposition='top center',
        name='Twoja pozycja'
    ))
    
    # Dodaj osie
    fig_grid.add_hline(y=0, line_dash="dash", line_color="gray")
    fig_grid.add_vline(x=0, line_dash="dash", line_color="gray")
    
    fig_grid.update_layout(
        title='Siatka Stylów Uczenia się',
        xaxis=dict(title='Przetwarzanie (AE - RO)', range=[-13, 13]),
        yaxis=dict(title='Postrzeganie (AC - CE)', range=[-13, 13]),
        width=650,  # Fixed width - bezpieczna szerokość dla A4
        height=400,  
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=60, b=60, l=70, r=70)  # Większe boczne marginesy
    )
    
    # Konwertuj wykres siatki do HTML
    grid_chart_html = fig_grid.to_html(
        include_plotlyjs=False,  # Plotly.js już jest w pierwszym wykresie
        div_id='grid_chart',
        config={'displayModeBar': False, 'responsive': True}  # Responsive
    )
    
    # Opisy stylów
    style_descriptions = {
        "Diverging (Dywergent)": {
            "icon": "🎨",
            "desc": "Uczysz się poprzez obserwację i refleksję. Preferujesz kreatywne podejście i wielość perspektyw.",
            "strengths": "Kreatywność, empatia, wyobraźnia, generowanie pomysłów",
            "development": "Praca w grupach, burze mózgów, case studies, dyskusje"
        },
        "Assimilating (Asymilator)": {
            "icon": "📚",
            "desc": "Uczysz się poprzez logiczne myślenie i teorię. Preferujesz systematyczne podejście.",
            "strengths": "Analiza, organizacja informacji, myślenie konceptualne",
            "development": "Wykłady, czytanie, badania, modele teoretyczne"
        },
        "Converging (Konwergent)": {
            "icon": "🎯",
            "desc": "Uczysz się poprzez praktyczne zastosowanie teorii. Preferujesz rozwiązywanie konkretnych problemów.",
            "strengths": "Rozwiązywanie problemów, podejmowanie decyzji, praktyczne zastosowania",
            "development": "Ćwiczenia praktyczne, symulacje, eksperymenty, projekty"
        },
        "Accommodating (Akomodator)": {
            "icon": "⚡",
            "desc": "Uczysz się poprzez działanie i eksperymentowanie. Preferujesz intuicyjne podejście.",
            "strengths": "Adaptacja, działanie, branie ryzyka, realizacja planów",
            "development": "Praktyka w terenie, trial-and-error, projekty terenowe"
        }
    }
    
    style_info = style_descriptions.get(dominant, style_descriptions["Diverging (Dywergent)"])
    
    # Szczegółowe opisy stylów (pełna wersja dla PDF)
    detailed_style_descriptions = {
        "Diverging (Dywergent)": {
            "icon": "🎨",
            "quadrant": "CE/RO",
            "description": "Łączysz Konkretne Doświadczenie i Refleksyjną Obserwację. Jesteś wrażliwy i potrafisz spojrzeć na sytuacje z wielu różnych perspektyw. Twoja główna mocna strona to wyobraźnia i zdolność do generowania wielu pomysłów.",
            "strengths": ["Wyobraźnia i kreatywność", "Zdolność do widzenia sytuacji z różnych perspektyw", "Empatia i wrażliwość", "Doskonałość w burzy mózgów i generowaniu pomysłów", "Umiejętność integracji różnych obserwacji"],
            "weaknesses": ["Trudności z podejmowaniem szybkich decyzji", "Problemy z przekładaniem teorii na działanie", "Tendencja do nadmiernego analizowania"],
            "careers": "Doradztwo, sztuka, HR, psychologia, dziennikarstwo",
            "learning_methods": "Studia przypadków, dyskusje grupowe, feedback, introspekcja, obserwacja działania innych"
        },
        "Assimilating (Asymilator)": {
            "icon": "📚",
            "quadrant": "AC/RO",
            "description": "Łączysz Abstrakcyjną Konceptualizację i Refleksyjną Obserwację. Preferujesz zwięzłe, logiczne i systematyczne podejście. Wykazujesz dużą zdolność do tworzenia modeli teoretycznych i scalania licznych obserwacji w zintegrowane wyjaśnienia.",
            "strengths": ["Tworzenie modeli teoretycznych", "Logiczne i systematyczne myślenie", "Precyzja i spójność teorii", "Zdolność do scalania wielu obserwacji", "Planowanie strategiczne"],
            "weaknesses": ["Mniejsze zainteresowanie problemami praktycznymi", "Trudności w pracy z ludźmi", "Preferencja teorii nad zastosowaniem"],
            "careers": "Nauka, informatyka, planowanie strategiczne, badania, matematyka",
            "learning_methods": "Wykłady teoretyczne, modele i schematy, analiza koncepcji, dociekliwe pytania, prace nad systemami"
        },
        "Converging (Konwergent)": {
            "icon": "🎯",
            "quadrant": "AC/AE",
            "description": "Łączysz Abstrakcyjną Konceptualizację i Aktywne Eksperymentowanie. Doskonale radzisz sobie z praktycznym zastosowaniem teorii do rozwiązywania konkretnych problemów. Skupiasz się na zadaniach i rzeczach, a nie na kwestiach międzyludzkich.",
            "strengths": ["Praktyczne zastosowanie teorii", "Efektywność i sprawność działania", "Zdolność do podejmowania decyzji", "Umiejętności techniczne", "Rozwiązywanie konkretnych problemów"],
            "weaknesses": ["Mniejsze zainteresowanie relacjami międzyludzkimi", "Skupienie na zadaniach kosztem ludzi", "Preferencja dla jednoznacznych rozwiązań"],
            "careers": "Inżynieria, technologia, medycyna, ekonomia, zawody techniczne",
            "learning_methods": "Ćwiczenia praktyczne, wdrożenia, testowanie umiejętności, konkretne przykłady zawodowe, zadania aplikacyjne"
        },
        "Accommodating (Akomodator)": {
            "icon": "⚡",
            "quadrant": "CE/AE",
            "description": "Łączysz Konkretne Doświadczenie i Aktywne Eksperymentowanie. To styl 'hands-on', który polega na intuicji. Jesteś elastyczny, zdolny do wprowadzania planów w życie, chętnie eksperymentujesz i adaptujesz się do nowych warunków.",
            "strengths": ["Elastyczność i adaptacja", "Podejmowanie ryzyka", "Szybka reakcja na zmiany", "Osobiste zaangażowanie", "Umiejętność wprowadzania planów w życie"],
            "weaknesses": ["Tendencja do działania bez planu", "Niecierpliwość wobec teorii", "Ryzyko podejmowania pochopnych decyzji"],
            "careers": "Zarządzanie operacyjne, sprzedaż, marketing, przedsiębiorczość",
            "learning_methods": "Gry, symulacje, różnorodne ćwiczenia, odgrywanie ról, zadania niestandardowe wymagające ryzyka"
        }
    }
    
    detailed_style_info = detailed_style_descriptions.get(dominant, detailed_style_descriptions["Diverging (Dywergent)"])
    
    # HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Raport Kolb - {username}</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            
            body {{
                font-family: 'Arial', 'Helvetica', sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            
            .header {{
                text-align: center;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
            }}
            
            .header h1 {{
                margin: 0;
                font-size: 32px;
                font-weight: bold;
            }}
            
            .header p {{
                margin: 10px 0 0 0;
                font-size: 16px;
                opacity: 0.9;
            }}
            
            .section {{
                margin-bottom: 30px;
                page-break-inside: avoid;
            }}
            
            .section-title {{
                font-size: 24px;
                color: #667eea;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            
            .abilities-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);  /* Jeden wiersz, cztery kolumny */
                gap: 15px;  /* Mniejsza przerwa między kartami */
                margin-bottom: 30px;
            }}
            
            .ability-card {{
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px 10px;  /* Mniejszy padding dla węższych kart */
                text-align: center;
                background: #f8f9fa;
            }}
            
            .ability-card h3 {{
                color: #333;
                margin: 8px 0;
                font-size: 14px;  /* Mniejsza czcionka */
                line-height: 1.3;
            }}
            
            .ability-card .score {{
                font-size: 32px;  /* Mniejszy wynik */
                font-weight: bold;
                margin: 8px 0;
            }}
            
            .ability-card .desc {{
                color: #666;
                font-size: 12px;  /* Mniejszy opis */
                line-height: 1.3;
            }}
            
            .chart-container {{
                text-align: center;
                margin: 20px 0;
                page-break-inside: avoid;
                max-width: 100%;
                overflow: hidden;
            }}
            
            .chart-container img {{
                max-width: 100%;
                height: auto;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
            }}
            
            .dominant-style {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 10px;
                margin: 20px 0;
            }}
            
            .dominant-style h2 {{
                margin: 0 0 15px 0;
                font-size: 28px;
            }}
            
            .dominant-style p {{
                margin: 10px 0;
                font-size: 16px;
                line-height: 1.8;
            }}
            
            .info-box {{
                background: #f0f7ff;
                border-left: 4px solid #4A90E2;
                padding: 20px;
                margin: 20px 0;
                border-radius: 5px;
            }}
            
            .info-box h3 {{
                margin: 0 0 10px 0;
                color: #4A90E2;
            }}
            
            .flexibility-meter {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
            }}
            
            .flexibility-meter .score {{
                font-size: 48px;
                font-weight: bold;
                color: #667eea;
            }}
            
            .footer {{
                text-align: center;
                color: #999;
                font-size: 12px;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #e0e0e0;
            }}
            
            .two-column {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 20px 0;
            }}
            
            /* Style dla kompaktowych wskazówek AI */
            .ai-tip-box {{
                page-break-inside: avoid;
                margin-bottom: 15px;
            }}
            
            .ai-tip-box h3 {{
                margin: 0 0 10px 0;
                font-size: 16px;
                font-weight: bold;
            }}
            
            .ai-tip-box > div {{
                margin: 0;
                padding-left: 10px;
            }}
            
            .ai-tip-box > div > div {{
                margin-bottom: 8px;
                font-size: 14px;
                line-height: 1.5;
            }}
            
            /* Style dla wykresów Plotly */
            .plotly, .js-plotly-plot {{
                max-width: 100%;
                overflow: visible;
                margin: 20px auto;
            }}
            
            #bar_chart, #grid_chart {{
                max-width: 100%;
                overflow: visible;
                page-break-inside: avoid;
            }}
            
            .plotly svg {{
                max-width: 100%;
                height: auto;
            }}
            
            /* Media query dla druku */
            @media print {{
                body {{
                    background: white;
                }}
                
                .header, .dominant-style, .ai-card-color, .ai-header-color {{
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    color-adjust: exact !important;
                }}
                
                .section {{
                    page-break-inside: avoid;
                }}
                
                /* Karty zdolności - kompaktowe w druku */
                .abilities-grid {{
                    gap: 10px !important;  /* Mniejsza przerwa */
                }}
                
                .ability-card {{
                    padding: 10px 8px !important;  /* Jeszcze mniejszy padding */
                }}
                
                .ability-card h3 {{
                    font-size: 13px !important;
                }}
                
                .ability-card .score {{
                    font-size: 28px !important;
                }}
                
                .ability-card .desc {{
                    font-size: 11px !important;
                }}
                
                /* Boxy AI - kompaktowe w druku */
                .ai-tip-box {{
                    margin-bottom: 10px !important;
                    padding: 10px 15px !important;
                }}
                
                .ai-tip-box h3 {{
                    font-size: 14px !important;
                    margin-bottom: 8px !important;
                }}
                
                .ai-tip-box > div > div {{
                    font-size: 12px !important;
                    margin-bottom: 5px !important;
                    line-height: 1.4 !important;
                }}
                
                .chart-container {{
                    margin: 15px auto !important;
                    max-width: 680px !important;  /* Szerokość dopasowana do wykresów */
                    overflow: visible !important;
                }}
                
                /* Wykresy Plotly - bez skalowania */
                .plotly {{
                    page-break-inside: avoid !important;
                    max-width: 680px !important;
                    margin: 0 auto !important;
                }}
                
                .js-plotly-plot {{
                    page-break-inside: avoid !important;
                    max-width: 680px !important;
                }}
                
                /* Kontenery wykresów */
                #bar_chart, #grid_chart {{
                    page-break-inside: avoid !important;
                    max-width: 680px !important;
                    overflow: visible !important;
                    margin: 0 auto 15px auto !important;
                }}
                
                /* SVG w wykresach */
                .plotly svg {{
                    max-width: 680px !important;
                }}
                
                @page {{
                    margin: 1.5cm;
                    size: A4;
                }}
            }}
            
            /* Przycisk drukowania */
            .print-button {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: #667eea;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
                z-index: 1000;
            }}
            
            .print-button:hover {{
                background: #5568d3;
            }}
            
            @media print {{
                .print-button {{
                    display: none;
                }}
            }}
        </style>
    </head>
    <body>
        <!-- Przycisk do drukowania -->
        <button class="print-button" onclick="window.print()">🖨️ Drukuj / Zapisz jako PDF</button>
        
        <div class="header">
            <h1>🎓 Raport Kolb Learning Style Inventory</h1>
            <p>Użytkownik: {username}</p>
            <p>Data: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
        </div>
        
        <div class="section">
            <h2 class="section-title">📊 Twoje Zdolności Uczenia się</h2>
            
            <div class="abilities-grid">
                <div class="ability-card" style="border-left: 5px solid {ability_info['CE']['color']}">
                    <div style="font-size: 32px;">{ability_info['CE']['emoji']}</div>
                    <h3>{ability_info['CE']['name']}</h3>
                    <div class="desc">({ability_info['CE']['desc']})</div>
                    <div class="score" style="color: {ability_info['CE']['color']}">{results['CE']}/12</div>
                </div>
                
                <div class="ability-card" style="border-left: 5px solid {ability_info['RO']['color']}">
                    <div style="font-size: 32px;">{ability_info['RO']['emoji']}</div>
                    <h3>{ability_info['RO']['name']}</h3>
                    <div class="desc">({ability_info['RO']['desc']})</div>
                    <div class="score" style="color: {ability_info['RO']['color']}">{results['RO']}/12</div>
                </div>
                
                <div class="ability-card" style="border-left: 5px solid {ability_info['AC']['color']}">
                    <div style="font-size: 32px;">{ability_info['AC']['emoji']}</div>
                    <h3>{ability_info['AC']['name']}</h3>
                    <div class="desc">({ability_info['AC']['desc']})</div>
                    <div class="score" style="color: {ability_info['AC']['color']}">{results['AC']}/12</div>
                </div>
                
                <div class="ability-card" style="border-left: 5px solid {ability_info['AE']['color']}">
                    <div style="font-size: 32px;">{ability_info['AE']['emoji']}</div>
                    <h3>{ability_info['AE']['name']}</h3>
                    <div class="desc">({ability_info['AE']['desc']})</div>
                    <div class="score" style="color: {ability_info['AE']['color']}">{results['AE']}/12</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">📈 Wizualizacja Wyników</h2>
            <div class="chart-container" style="max-width: 95%; margin: 0 auto;">
                {bar_chart_html}
            </div>
        </div>
        
        <div class="section" style="page-break-before: always;">
            <h2 class="section-title">🎯 Twój Dominujący Styl Uczenia się</h2>
            
            <div class="dominant-style">
                <h2>{detailed_style_info['icon']} {dominant}</h2>
                <p><strong>Ćwiartka:</strong> {detailed_style_info['quadrant']}</p>
                <p style="margin-top: 15px; font-size: 16px; line-height: 1.8;">{detailed_style_info['description']}</p>
            </div>
            
            <div class="chart-container" style="max-width: 95%; margin: 0 auto;">
                {grid_chart_html}
            </div>
            
            <div class="two-column" style="margin-top: 30px;">
                <div class="info-box" style="border-left-color: #2ECC71; background: linear-gradient(135deg, rgba(46, 204, 113, 0.1) 0%, rgba(39, 174, 96, 0.1) 100%);">
                    <h3 style="color: #2ECC71;">💪 Twoje mocne strony:</h3>
                    <ul style="margin: 10px 0; padding-left: 20px; line-height: 1.8;">
                        {''.join([f'<li>{s}</li>' for s in detailed_style_info['strengths']])}
                    </ul>
                </div>
                
                <div class="info-box" style="border-left-color: #E67E22; background: linear-gradient(135deg, rgba(230, 126, 34, 0.1) 0%, rgba(211, 84, 0, 0.1) 100%);">
                    <h3 style="color: #E67E22;">🎯 Obszary do rozwoju:</h3>
                    <ul style="margin: 10px 0; padding-left: 20px; line-height: 1.8;">
                        {''.join([f'<li>{w}</li>' for w in detailed_style_info['weaknesses']])}
                    </ul>
                </div>
            </div>
            
            <div class="two-column" style="margin-top: 20px;">
                <div class="info-box" style="border-left-color: #3498DB;">
                    <h3 style="color: #3498DB;">💼 Typowe zawody:</h3>
                    <p>{detailed_style_info['careers']}</p>
                </div>
                
                <div class="info-box" style="border-left-color: #9B59B6;">
                    <h3 style="color: #9B59B6;">📚 Rekomendowane metody uczenia się:</h3>
                    <p>{detailed_style_info['learning_methods']}</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">💫 Elastyczność Uczenia się</h2>
            
            <div class="flexibility-meter">
                <div class="score">{flexibility:.1f}%</div>
                <p>Twoja elastyczność w uczeniu się</p>
                <p style="color: #666; font-size: 14px;">
                    {"🌟 Wysoka elastyczność! Potrafisz łączyć różne style uczenia się." if flexibility > 70 
                     else "⭐ Dobra elastyczność. Masz zrównoważone podejście." if flexibility > 50
                     else "💪 Silne preferencje w określonym stylu. Rozważ rozwijanie innych zdolności."}
                </p>
            </div>
            
            <div class="info-box">
                <h3>📍 Twoja pozycja na siatce</h3>
                <div class="two-column">
                    <div>
                        <strong>Postrzeganie (AC-CE):</strong> {dimensions['AC-CE']:+.1f}
                    </div>
                    <div>
                        <strong>Przetwarzanie (AE-RO):</strong> {dimensions['AE-RO']:+.1f}
                    </div>
                </div>
                <p style="margin-top: 15px;">
                    <strong>Kwadrant:</strong> {quadrant}
                </p>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">� Wymiary Liczbowe (LSI Dimensions)</h2>
            
            <div class="abilities-grid" style="grid-template-columns: repeat(3, 1fr);">
                <div class="ability-card" style="border-left: 5px solid #667eea; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);">
                    <h3>Oś Postrzegania</h3>
                    <div style="color: #666; font-size: 14px; margin: 5px 0;">AC-CE</div>
                    <div class="score" style="color: #667eea">{dimensions['AC-CE']:+d}</div>
                    <div style="color: #666; font-size: 14px;">{'Preferencja: Myślenie (AC)' if dimensions['AC-CE'] > 0 else 'Preferencja: Czucie (CE)'}</div>
                </div>
                
                <div class="ability-card" style="border-left: 5px solid #f5576c; background: linear-gradient(135deg, rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%);">
                    <h3>Oś Przetwarzania</h3>
                    <div style="color: #666; font-size: 14px; margin: 5px 0;">AE-RO</div>
                    <div class="score" style="color: #f5576c">{dimensions['AE-RO']:+d}</div>
                    <div style="color: #666; font-size: 14px;">{'Preferencja: Działanie (AE)' if dimensions['AE-RO'] > 0 else 'Preferencja: Obserwacja (RO)'}</div>
                </div>
                
                <div class="ability-card" style="border-left: 5px solid #38f9d7; background: linear-gradient(135deg, rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%);">
                    <h3>Elastyczność</h3>
                    <div style="color: #666; font-size: 14px; margin: 5px 0;">Learning Flexibility</div>
                    <div class="score" style="color: #38f9d7">{flexibility:.0f}%</div>
                    <div style="color: #666; font-size: 14px;">{'Wysoka - Zrównoważony' if flexibility > 60 else 'Średnia - Umiarkowana' if flexibility > 30 else 'Niska - Wyraźna preferencja'}</div>
                </div>
            </div>
            
            <div class="info-box" style="margin-top: 20px;">
                <h3>📊 Interpretacja wymiarów:</h3>
                <p><strong>AC-CE (Postrzeganie):</strong> Pokazuje jak preferujesz postrzegać informacje - poprzez abstrakcyjne myślenie (AC) czy konkretne doświadczenie (CE).</p>
                <p><strong>AE-RO (Przetwarzanie):</strong> Pokazuje jak preferujesz przetwarzać informacje - poprzez aktywne eksperymentowanie (AE) czy refleksyjną obserwację (RO).</p>
                <p><strong>Elastyczność:</strong> Im bliżej centrum siatki, tym większa elastyczność w przełączaniu między stylami uczenia się.</p>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">�💡 Rekomendacje Rozwojowe</h2>
            
            <div class="info-box" style="border-left-color: #2ECC71;">
                <h3>✅ Co robić więcej:</h3>
                <p>{style_info['development']}</p>
            </div>
            
            <div class="info-box" style="border-left-color: #E74C3C;">
                <h3>🎯 Obszary do rozwinięcia:</h3>
                <p>Rozważ ćwiczenie pozostałych stylów uczenia się, aby zwiększyć swoją elastyczność i efektywność.</p>
            </div>
        </div>
        """
    
    # Dodaj sekcję AI jeśli jest dostępna
    ai_section = ""
    if st.session_state.get('kolb_profession') and st.session_state.get('kolb_ai_tips'):
        profession = st.session_state.kolb_profession
        ai_tips_raw = st.session_state.kolb_ai_tips
        
        # Parsuj wskazówki AI na sekcje (taka sama logika jak w Streamlit)
        section_pattern = r'^\*\*(.+?)\*\*:?\s*$'
        lines = ai_tips_raw.strip().split('\n')
        sections = []
        current_section = None
        current_items = []
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            header_match = re.match(section_pattern, line_stripped)
            
            if header_match and len(line_stripped) < 100:
                if current_section and current_items:
                    sections.append((current_section, current_items))
                current_section = header_match.group(1).strip().rstrip(':')
                current_items = []
            else:
                clean_line = re.sub(r'^[-•*]\s*', '', line_stripped)
                clean_line = clean_line.strip()
                if clean_line:
                    current_items.append(clean_line)
        
        if current_section and current_items:
            sections.append((current_section, current_items))
        
        # Generuj HTML dla sekcji
        ai_cards_html = ""
        for idx, (section_title, items) in enumerate(sections):
            # Automatyczne wybieranie koloru i ikony
            if 'warunki' in section_title.lower() or 'optymalne' in section_title.lower():
                icon = '🌟'
                bg = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                text_color = 'white'
            elif 'mocn' in section_title.lower() or 'wzmacnia' in section_title.lower():
                icon = '💪'
                bg = 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
                text_color = 'white'
            elif 'rozwój' in section_title.lower() or 'rozwija' in section_title.lower():
                icon = '🚀'
                bg = 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
                text_color = '#333'
            else:
                icon = '📌'
                bg = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
                text_color = 'white'
            
            # Buduj HTML dla punktów z numeracją
            items_html = "<ol style='margin: 10px 0 0 20px; padding-left: 0;'>"
            for item in items:
                # Zamień **tekst** na <strong>tekst</strong>
                formatted_item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                items_html += f"<li style='margin: 10px 0; line-height: 1.6;'>{formatted_item}</li>"
            items_html += "</ol>"
            
            # Dodaj kartę z klasą dla zachowania kolorów w druku
            ai_cards_html += f"""
            <div class='ai-card-color' style='background: {bg}; 
                        color: {text_color}; 
                        padding: 25px; 
                        border-radius: 15px; 
                        margin: 15px 0;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                        color-adjust: exact;'>
                <h4 style='margin: 0 0 20px 0; color: {text_color};'>{icon} {section_title}</h4>
                {items_html}
            </div>
            """
        
        ai_section = f"""
        <div class="section" style="page-break-before: always;">
            <h2 class="section-title">🤖 Jak Uczyć się Efektywnie</h2>
            
            <div class='ai-header-color' style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; 
                        padding: 15px 20px; 
                        border-radius: 10px; 
                        margin-bottom: 20px;
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                        color-adjust: exact;">
                <p style="margin: 0; font-size: 16px;"><strong>👔 Zawód:</strong> {profession} | <strong>🎯 Styl uczenia się:</strong> {dominant}</p>
            </div>
            
            {ai_cards_html}
            
            <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <p style="margin: 0; font-size: 13px; color: #1565c0;"><strong>💡 Pamiętaj:</strong> Te wskazówki są dopasowane do Twojego stylu uczenia się. Testuj je w praktyce i obserwuj co działa najlepiej w Twojej sytuacji.</p>
            </div>
        </div>
        """
    
    html_content += ai_section + """
        
        <div class="footer">
            <p>Raport wygenerowany przez BrainVenture Academy</p>
            <p>Test Kolba - Experiential Learning Theory © David A. Kolb</p>
        </div>
    </body>
    </html>
    """
    
    # Zwróć HTML - przeglądarka użytkownika wygeneruje PDF
    return html_content

def display_kolb_results():
    """Wyświetla wyniki testu Kolba zgodnie z metodologią ELT"""
    st.markdown("---")
    st.markdown("## 🎯 Twoje wyniki - Kolb Experiential Learning Profile")
    
    results = st.session_state.kolb_results
    dimensions = st.session_state.kolb_dimensions
    dominant = st.session_state.kolb_dominant
    quadrant = st.session_state.kolb_quadrant
    flexibility = st.session_state.kolb_flexibility
    
    # Wyświetl wyniki dla czterech zdolności uczenia się
    st.markdown("### 📊 Twoje zdolności uczenia się")
    cols = st.columns(4)
    
    ability_info = {
        "CE": {"name": "Konkretne Doświadczenie", "emoji": "❤️", "color": "#E74C3C", "desc": "Feeling"},
        "RO": {"name": "Refleksyjna Obserwacja", "emoji": "👁️", "color": "#4A90E2", "desc": "Watching"},
        "AC": {"name": "Abstrakcyjna Konceptualizacja", "emoji": "🧠", "color": "#9B59B6", "desc": "Thinking"},
        "AE": {"name": "Aktywne Eksperymentowanie", "emoji": "⚙️", "color": "#2ECC71", "desc": "Doing"}
    }
    
    for idx, (ability, score) in enumerate(results.items()):
        with cols[idx]:
            info = ability_info[ability]
            st.markdown(f"""
            <div style='padding: 15px; background: #f8f9fa; border-radius: 12px; text-align: center; 
                        border-left: 4px solid {info['color']};'>
                <div style='font-size: 2em; margin-bottom: 5px;'>{info['emoji']}</div>
                <h5 style='color: {info['color']}; margin: 5px 0; font-size: 0.9em;'>{info['name']}</h5>
                <p style='color: #666; font-size: 0.8em; margin: 3px 0;'>({info['desc']})</p>
                <div style='font-size: 1.8em; font-weight: bold; color: {info['color']};'>{score}/12</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Wizualizacja 1: Wykres Słupkowy dla Zdolności Podstawowych
    st.markdown("---")
    st.markdown("### 📊 Wykres Zdolności Podstawowych (Bar Chart)")
    st.markdown("*Twoje preferencje do poszczególnych etapów Cyklu Kolba*")
    
    # Przygotuj dane do wykresu słupkowego
    abilities_order = ['CE', 'RO', 'AC', 'AE']
    ability_labels = {
        'CE': 'Konkretne Doświadczenie<br>(Feeling)',
        'RO': 'Refleksyjna Obserwacja<br>(Watching)',
        'AC': 'Abstrakcyjna Konceptualizacja<br>(Thinking)',
        'AE': 'Aktywne Eksperymentowanie<br>(Doing)'
    }
    ability_colors = {
        'CE': '#E74C3C',  # Czerwony
        'RO': '#4A90E2',  # Niebieski
        'AC': '#9B59B6',  # Fioletowy
        'AE': '#2ECC71'   # Zielony
    }
    
    scores = [results[a] for a in abilities_order]
    labels = [ability_labels[a] for a in abilities_order]
    colors = [ability_colors[a] for a in abilities_order]
    
    fig_bar = go.Figure(data=[
        go.Bar(
            x=labels,
            y=scores,
            marker=dict(
                color=colors,
                line=dict(color='rgba(0,0,0,0.3)', width=2)
            ),
            text=scores,
            textposition='outside',
            textfont=dict(size=16, color='#333', family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>Wynik: %{y}/12<extra></extra>'
        )
    ])
    
    fig_bar.update_layout(
        title=dict(
            text='Zdolności Podstawowe w Cyklu Kolba',
            font=dict(size=18, color='#333', family='Arial')
        ),
        yaxis=dict(
            title='Wynik (punkty)',
            range=[0, 13],
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=12)
        ),
        xaxis=dict(
            tickfont=dict(size=11)
        ),
        plot_bgcolor='rgba(248,249,250,0.8)',
        paper_bgcolor='white',
        height=400,
        margin=dict(t=60, b=80, l=60, r=40),
        showlegend=False
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Interpretacja wykresu słupkowego
    strongest = max(results.items(), key=lambda x: x[1])
    weakest = min(results.items(), key=lambda x: x[1])
    
    col_int1, col_int2 = st.columns(2)
    with col_int1:
        st.success(f"**💪 Twoja najsilniejsza zdolność:** {ability_info[strongest[0]]['name']} ({strongest[1]}/12)")
    with col_int2:
        st.warning(f"**🎯 Obszar do rozwoju:** {ability_info[weakest[0]]['name']} ({weakest[1]}/12)")
    
    # Wizualizacja 2: Siatka Stylów Uczenia się (Learning Style Grid)
    st.markdown("---")
    st.markdown("### 🎯 Siatka Stylów Uczenia się (Learning Style Grid)")
    st.markdown("*Twoja pozycja w matrycy stylów ELT - im bliżej środka, tym większa elastyczność*")
    
    # Pobierz współrzędne
    x_coord = dimensions['AE-RO']  # Oś pozioma (Przetwarzanie)
    y_coord = dimensions['AC-CE']  # Oś pionowa (Postrzeganie)
    
    # Utwórz wykres siatki
    fig_grid = go.Figure()
    
    # Dodaj tło ćwiartek z nazwami stylów
    quadrant_info = {
        'Diverging': {'x': [-12, 0], 'y': [-12, 0], 'color': 'rgba(231, 76, 60, 0.15)', 'label_x': -6, 'label_y': -6},
        'Assimilating': {'x': [-12, 0], 'y': [0, 12], 'color': 'rgba(155, 89, 182, 0.15)', 'label_x': -6, 'label_y': 6},
        'Converging': {'x': [0, 12], 'y': [0, 12], 'color': 'rgba(52, 152, 219, 0.15)', 'label_x': 6, 'label_y': 6},
        'Accommodating': {'x': [0, 12], 'y': [-12, 0], 'color': 'rgba(46, 204, 113, 0.15)', 'label_x': 6, 'label_y': -6}
    }
    
    # Rysuj prostokąty ćwiartek
    for style_name, info in quadrant_info.items():
        fig_grid.add_shape(
            type="rect",
            x0=info['x'][0], x1=info['x'][1],
            y0=info['y'][0], y1=info['y'][1],
            fillcolor=info['color'],
            line=dict(width=0)
        )
        
        # Dodaj etykiety stylów
        fig_grid.add_annotation(
            x=info['label_x'], y=info['label_y'],
            text=f"<b>{style_name}</b>",
            showarrow=False,
            font=dict(size=14, color='rgba(0,0,0,0.5)', family='Arial Black'),
            xanchor='center',
            yanchor='middle'
        )
    
    # Strefa Zrównoważonego Uczenia się (centralna)
    balanced_zone_radius = 4
    theta = [i for i in range(0, 361, 10)]
    balanced_x = [balanced_zone_radius * math.cos(math.radians(t)) for t in theta]
    balanced_y = [balanced_zone_radius * math.sin(math.radians(t)) for t in theta]
    
    fig_grid.add_trace(go.Scatter(
        x=balanced_x, y=balanced_y,
        fill='toself',
        fillcolor='rgba(255, 193, 7, 0.2)',
        line=dict(color='rgba(255, 193, 7, 0.6)', width=2, dash='dash'),
        name='Strefa Zrównoważonego<br>Uczenia się',
        hoverinfo='name',
        showlegend=True
    ))
    
    # Osie
    fig_grid.add_shape(type="line", x0=-12, x1=12, y0=0, y1=0, 
                       line=dict(color="rgba(0,0,0,0.4)", width=2))
    fig_grid.add_shape(type="line", x0=0, x1=0, y0=-12, y1=12, 
                       line=dict(color="rgba(0,0,0,0.4)", width=2))
    
    # Punkt użytkownika
    fig_grid.add_trace(go.Scatter(
        x=[x_coord], y=[y_coord],
        mode='markers+text',
        marker=dict(
            size=20,
            color='#FF5722',
            line=dict(color='white', width=3),
            symbol='circle'
        ),
        text=['TWÓJ<br>WYNIK'],
        textposition='top center',
        textfont=dict(size=12, color='#FF5722', family='Arial Black'),
        name='Twoja pozycja',
        hovertemplate=f'<b>Twoja pozycja</b><br>AE-RO: {x_coord:+d}<br>AC-CE: {y_coord:+d}<br>Elastyczność: {flexibility:.0f}%<extra></extra>'
    ))
    
    # Etykiety osi
    fig_grid.add_annotation(x=12.5, y=0, text="<b>AE</b><br>(Doing)", showarrow=False, 
                           font=dict(size=11, color='#2ECC71'), xanchor='left')
    fig_grid.add_annotation(x=-12.5, y=0, text="<b>RO</b><br>(Watching)", showarrow=False, 
                           font=dict(size=11, color='#4A90E2'), xanchor='right')
    fig_grid.add_annotation(x=0, y=12.5, text="<b>AC</b><br>(Thinking)", showarrow=False, 
                           font=dict(size=11, color='#9B59B6'), yanchor='bottom')
    fig_grid.add_annotation(x=0, y=-12.5, text="<b>CE</b><br>(Feeling)", showarrow=False, 
                           font=dict(size=11, color='#E74C3C'), yanchor='top')
    
    fig_grid.update_layout(
        title=dict(
            text=f'Twój Styl: {dominant} | Elastyczność: {flexibility:.0f}%',
            font=dict(size=18, color='#333', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='<b>Oś Przetwarzania (AE-RO)</b>',
            range=[-14, 14],
            zeroline=False,
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            title='<b>Oś Postrzegania (AC-CE)</b>',
            range=[-14, 14],
            zeroline=False,
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=10),
            scaleanchor='x',
            scaleratio=1
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=600,
        margin=dict(t=80, b=80, l=80, r=80),
        showlegend=True,
        legend=dict(
            x=1.02,
            y=1,
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig_grid, use_container_width=True)
    
    # Interpretacja siatki
    distance_from_center = math.sqrt(x_coord**2 + y_coord**2)
    
    if distance_from_center <= 4:
        interpretation_color = "success"
        interpretation = f"🎯 **Gratulacje!** Twój wynik znajduje się w **Strefie Zrównoważonego Uczenia się**. Oznacza to wysoką elastyczność i zdolność do wykorzystania wszystkich faz cyklu Kolba w zależności od sytuacji."
    elif distance_from_center <= 8:
        interpretation_color = "info"
        interpretation = f"� **Umiarkowana preferencja** - Twój styl jest wyraźnie określony ({dominant}), ale zachowujesz dobrą elastyczność. Możesz efektywnie adaptować się do różnych sytuacji uczenia się."
    else:
        interpretation_color = "warning"
        interpretation = f"⚠️ **Silna preferencja** - Twój wynik znajduje się daleko od centrum siatki, co wskazuje na wyraźną tendencję do stylu **{dominant}**. Rozważ celowe rozwijanie słabszych zdolności, aby zwiększyć elastyczność uczenia się."
    
    if interpretation_color == "success":
        st.success(interpretation)
    elif interpretation_color == "info":
        st.info(interpretation)
    else:
        st.warning(interpretation)
    
    # Wymiary liczbowe
    st.markdown("---")
    st.markdown("### 📐 Wymiary Liczbowe (LSI Dimensions)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 12px; text-align: center; color: white;'>
            <h4 style='color: white; margin-bottom: 10px;'>Oś Postrzegania</h4>
            <p style='font-size: 0.9em; margin: 5px 0;'>AC-CE</p>
            <div style='font-size: 2em; font-weight: bold; margin: 10px 0;'>{dimensions['AC-CE']:+d}</div>
            <p style='font-size: 0.85em;'>{'Preferencja: Myślenie (AC)' if dimensions['AC-CE'] > 0 else 'Preferencja: Czucie (CE)'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='padding: 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    border-radius: 12px; text-align: center; color: white;'>
            <h4 style='color: white; margin-bottom: 10px;'>Oś Przetwarzania</h4>
            <p style='font-size: 0.9em; margin: 5px 0;'>AE-RO</p>
            <div style='font-size: 2em; font-weight: bold; margin: 10px 0;'>{dimensions['AE-RO']:+d}</div>
            <p style='font-size: 0.85em;'>{'Preferencja: Działanie (AE)' if dimensions['AE-RO'] > 0 else 'Preferencja: Obserwacja (RO)'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        flex_color = "#2ECC71" if flexibility > 60 else "#F39C12" if flexibility > 30 else "#E74C3C"
        st.markdown(f"""
        <div style='padding: 20px; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    border-radius: 12px; text-align: center; color: white;'>
            <h4 style='color: white; margin-bottom: 10px;'>Elastyczność</h4>
            <p style='font-size: 0.9em; margin: 5px 0;'>Learning Flexibility</p>
            <div style='font-size: 2em; font-weight: bold; margin: 10px 0;'>{flexibility:.0f}%</div>
            <p style='font-size: 0.85em;'>{'Wysoka - Zrównoważony profil' if flexibility > 60 else 'Średnia - Umiarkowana' if flexibility > 30 else 'Niska - Wyraźna preferencja'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Wyświetl dominujący styl
    st.markdown("---")
    st.markdown(f"### ⭐ Twój dominujący styl: **{dominant}**")
    st.markdown(f"**Ćwiartka:** {quadrant}")
    
    # Opisy stylów zgodnie z dokumentacją naukową
    style_descriptions = {
        "Diverging (Dywergent)": {
            "quadrant": "CE/RO",
            "description": "Łączysz Konkretne Doświadczenie i Refleksyjną Obserwację. Jesteś wrażliwy i potrafisz spojrzeć na sytuacje z wielu różnych perspektyw. Twoja główna mocna strona to wyobraźnia i zdolność do generowania wielu pomysłów.",
            "strengths": [
                "Wyobraźnia i kreatywność",
                "Zdolność do widzenia sytuacji z różnych perspektyw",
                "Empatia i wrażliwość",
                "Doskonałość w burzy mózgów i generowaniu pomysłów",
                "Umiejętność integracji różnych obserwacji"
            ],
            "weaknesses": [
                "Trudności z podejmowaniem szybkich decyzji",
                "Problemy z przekładaniem teorii na działanie",
                "Tendencja do nadmiernego analizowania"
            ],
            "careers": "Doradztwo, sztuka, HR, psychologia, dziennikarstwo",
            "learning_methods": "Studia przypadków, dyskusje grupowe, feedback, introspekcja, obserwacja działania innych"
        },
        "Assimilating (Asymilator)": {
            "quadrant": "AC/RO",
            "description": "Łączysz Abstrakcyjną Konceptualizację i Refleksyjną Obserwację. Preferujesz zwięzłe, logiczne i systematyczne podejście. Wykazujesz dużą zdolność do tworzenia modeli teoretycznych i scalania licznych obserwacji w zintegrowane wyjaśnienia.",
            "strengths": [
                "Tworzenie modeli teoretycznych",
                "Logiczne i systematyczne myślenie",
                "Precyzja i spójność teorii",
                "Zdolność do scalania wielu obserwacji",
                "Planowanie strategiczne"
            ],
            "weaknesses": [
                "Mniejsze zainteresowanie problemami praktycznymi",
                "Trudności w pracy z ludźmi",
                "Preferencja teorii nad zastosowaniem"
            ],
            "careers": "Nauka, informatyka, planowanie strategiczne, badania, matematyka",
            "learning_methods": "Wykłady teoretyczne, modele i schematy, analiza koncepcji, dociekliwe pytania, prace nad systemami"
        },
        "Converging (Konwergent)": {
            "quadrant": "AC/AE",
            "description": "Łączysz Abstrakcyjną Konceptualizację i Aktywne Eksperymentowanie. Doskonale radzisz sobie z praktycznym zastosowaniem teorii do rozwiązywania konkretnych problemów. Skupiasz się na zadaniach i rzeczach, a nie na kwestiach międzyludzkich.",
            "strengths": [
                "Praktyczne zastosowanie teorii",
                "Efektywność i sprawność działania",
                "Zdolność do podejmowania decyzji",
                "Umiejętności techniczne",
                "Rozwiązywanie konkretnych problemów"
            ],
            "weaknesses": [
                "Mniejsze zainteresowanie relacjami międzyludzkimi",
                "Skupienie na zadaniach kosztem ludzi",
                "Preferencja dla jednoznacznych rozwiązań"
            ],
            "careers": "Inżynieria, technologia, medycyna, ekonomia, zawody techniczne",
            "learning_methods": "Ćwiczenia praktyczne, wdrożenia, testowanie umiejętności, konkretne przykłady zawodowe, zadania aplikacyjne"
        },
        "Accommodating (Akomodator)": {
            "quadrant": "CE/AE",
            "description": "Łączysz Konkretne Doświadczenie i Aktywne Eksperymentowanie. To styl 'hands-on', który polega na intuicji. Jesteś elastyczny, zdolny do wprowadzania planów w życie, chętnie eksperymentujesz i adaptujesz się do nowych warunków.",
            "strengths": [
                "Elastyczność i adaptacja",
                "Podejmowanie ryzyka",
                "Szybka reakcja na zmiany",
                "Osobiste zaangażowanie",
                "Umiejętność wprowadzania planów w życie"
            ],
            "weaknesses": [
                "Tendencja do działania bez planu",
                "Niecierpliwość wobec teorii",
                "Ryzyko podejmowania pochopnych decyzji"
            ],
            "careers": "Zarządzanie operacyjne, sprzedaż, marketing, przedsiębiorczość",
            "learning_methods": "Gry, symulacje, różnorodne ćwiczenia, odgrywanie ról, zadania niestandardowe wymagające ryzyka"
        }
    }
    
    desc = style_descriptions[dominant]
    
    # Główna karta z opisem stylu
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                box-shadow: 0 4px 15px rgba(102,126,234,0.4); 
                border-radius: 20px; 
                padding: 30px; 
                margin: 25px 0; 
                color: white;'>
        <div style='font-size: 2.5em; margin-bottom: 10px;'>🎯</div>
        <h4 style='color: white; margin: 0 0 15px 0;'>Twój Styl Uczenia się</h4>
        <p style='font-size: 1.15em; line-height: 1.8; margin: 0;'>
            {desc['description']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Szczegółowe karty w 2 kolumnach
    col1, col2 = st.columns(2)
    
    with col1:
        # Karta mocnych stron
        strengths_html = "<br>".join([f"✅ {s}" for s in desc['strengths']])
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%); 
                    box-shadow: 0 3px 12px rgba(46,204,113,0.3); 
                    border-radius: 18px; 
                    padding: 25px; 
                    margin: 15px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'></div>
            <h4 style='margin: 0 0 15px 0; color: white;'>Twoje mocne strony</h4>
            <p style='margin: 0; font-size: 1.05em; line-height: 1.8;'>{strengths_html}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Karta zawodów
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                    box-shadow: 0 3px 12px rgba(52,152,219,0.3); 
                    border-radius: 18px; 
                    padding: 25px; 
                    margin: 15px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'></div>
            <h4 style='margin: 0 0 15px 0; color: white;'>Typowe zawody</h4>
            <p style='margin: 0; font-size: 1.05em; line-height: 1.7;'>{desc['careers']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Karta obszarów rozwoju
        weaknesses_html = "<br>".join([f"⚠️ {w}" for w in desc['weaknesses']])
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #e67e22 0%, #d35400 100%); 
                    box-shadow: 0 3px 12px rgba(230,126,34,0.3); 
                    border-radius: 18px; 
                    padding: 25px; 
                    margin: 15px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'></div>
            <h4 style='margin: 0 0 15px 0; color: white;'>Obszary do rozwoju</h4>
            <p style='margin: 0; font-size: 1.05em; line-height: 1.8;'>{weaknesses_html}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Karta metod szkoleniowych
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); 
                    box-shadow: 0 3px 12px rgba(155,89,182,0.3); 
                    border-radius: 18px; 
                    padding: 25px; 
                    margin: 15px 0; 
                    color: white;'>
            <div style='font-size: 2em; margin-bottom: 10px;'></div>
            <h4 style='margin: 0 0 12px 0; color: white;'>Rekomendowane metody szkoleniowe</h4>
            <p style='margin: 0; font-size: 1.05em; line-height: 1.6;'>{desc['learning_methods']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Karta ze strategią rozwoju elastyczności
    st.markdown("---")
    
    # Identyfikacja słabych zdolności
    weak_abilities = [ability for ability, score in results.items() if score < 4]
    strong_abilities = [ability for ability, score in results.items() if score > 8]
    
    if weak_abilities:
        weak_abilities_names = ', '.join([ability_info[a]['name'] for a in weak_abilities])
        weak_tips_html = "<br>".join([f"• Dla <b>{ability_info[a]['name']} ({a})</b>: ćwicz {ability_info[a]['desc'].lower()}" for a in weak_abilities])
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); 
                    box-shadow: 0 3px 12px rgba(255,234,167,0.3); 
                    border-radius: 18px; 
                    padding: 25px; 
                    margin: 20px 0; 
                    color: #222;'>
            <div style='font-size: 2em; margin-bottom: 10px;'></div>
            <h4 style='margin: 0 0 15px 0; color: #e17055;'>Zdolności do wzmocnienia</h4>
            <p style='margin: 0 0 15px 0; font-size: 1.05em;'>
                Twoje słabsze zdolności to: <b>{weak_abilities_names}</b>
            </p>
            <div style='background: rgba(255,255,255,0.3); 
                        border-radius: 10px; 
                        padding: 15px; 
                        margin-top: 15px;'>
                <p style='margin: 0 0 10px 0; font-weight: bold;'>💡 Zalecenia rozwojowe:</p>
                <p style='margin: 0; line-height: 1.8;'>
                    Celowo angażuj się w sytuacje, które wymagają używania tych zdolności:<br><br>
                    {weak_tips_html}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Karta z pełnym cyklem Kolba
    flexibility_message = "Im bliżej centrum siatki, tym większa zdolność adaptacji do różnych sytuacji uczenia się." if flexibility > 50 else "Rozwijaj słabsze zdolności, aby zwiększyć elastyczność i efektywność uczenia się w różnych kontekstach."
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                box-shadow: 0 4px 15px rgba(102,126,234,0.4); 
                border-radius: 20px; 
                padding: 30px; 
                margin: 20px 0; 
                color: white;'>
        <div style='font-size: 2em; margin-bottom: 10px;'>🔄</div>
        <h4 style='color: white; margin: 0 0 20px 0;'>Pełny Cykl Uczenia się Kolba (ELT Cycle)</h4>
        <p style='font-size: 1.05em; line-height: 1.7; margin-bottom: 20px;'>
            Najbardziej efektywne uczenie się wykorzystuje <b>wszystkie cztery fazy</b> w cyklu:
        </p>
        <div style='background: rgba(255,255,255,0.15); 
                    border-radius: 12px; 
                    padding: 20px; 
                    margin: 15px 0;'>
            <ol style='margin: 0; padding-left: 20px; line-height: 2;'>
                <li><b>Konkretne Doświadczenie (CE)</b> → Zetknięcie się z nową sytuacją (Feeling)</li>
                <li><b>Refleksyjna Obserwacja (RO)</b> → Obserwacja i refleksja (Watching)</li>
                <li><b>Abstrakcyjna Konceptualizacja (AC)</b> → Tworzenie teorii (Thinking)</li>
                <li><b>Aktywne Eksperymentowanie (AE)</b> → Testowanie w praktyce (Doing)</li>
            </ol>
        </div>
        <div style='background: rgba(255,193,7,0.3); 
                    border-left: 4px solid #FFC107; 
                    border-radius: 8px; 
                    padding: 15px; 
                    margin-top: 20px;'>
            <p style='margin: 0; font-size: 1.05em;'>
                <b>💡 Kluczowa wskazówka:</b> Twój wynik elastyczności (<b>{flexibility:.0f}%</b>) pokazuje, 
                jak dobrze potrafisz przełączać się między stylami. {flexibility_message}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sekcja AI - Praktyczne wskazówki dla zawodu
    st.markdown("---")
    st.markdown("### 🤖 AI: Wskazówki praktyczne dla Twojego zawodu")
    st.markdown("Wybierz swój zawód, aby otrzymać spersonalizowane wskazówki, jak wykorzystać swój styl uczenia się w praktyce:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👨‍🏫 Trener", use_container_width=True, type="secondary", key="prof_trainer"):
            st.session_state.kolb_profession = "Trener"
            st.session_state.kolb_ai_generated = False
            st.rerun()
    
    with col2:
        if st.button("👔 Menedżer", use_container_width=True, type="secondary", key="prof_manager"):
            st.session_state.kolb_profession = "Menedżer"
            st.session_state.kolb_ai_generated = False
            st.rerun()
    
    with col3:
        if st.button("💼 Sprzedawca", use_container_width=True, type="secondary", key="prof_sales"):
            st.session_state.kolb_profession = "Sprzedawca"
            st.session_state.kolb_ai_generated = False
            st.rerun()
    
    # Wyświetl wybrany zawód i wygeneruj wskazówki
    if 'kolb_profession' in st.session_state and st.session_state.kolb_profession:
        st.info(f"✅ Wybrany zawód: **{st.session_state.kolb_profession}**")
        
        # Wyświetl wygenerowane wskazówki lub przycisk do generowania
        if st.session_state.get('kolb_ai_generated') and 'kolb_ai_tips' in st.session_state and st.session_state.kolb_ai_tips:
            st.markdown("---")
            st.markdown(f"### 🤖 Jak Uczyć się Efektywnie")
            
            # Header z zawodem i stylem
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; 
                        padding: 20px; 
                        border-radius: 15px; 
                        margin: 20px 0;
                        box-shadow: 0 4px 15px rgba(102,126,234,0.3);'>
                <h4 style='margin: 0; color: white;'>👔 Zawód: {st.session_state.kolb_profession} | 🎯 Styl uczenia się: {dominant}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Parsuj wskazówki AI na sekcje dla kart
            ai_tips_text = st.session_state.kolb_ai_tips
            section_pattern = r'^\*\*(.+?)\*\*:?\s*$'
            lines = ai_tips_text.strip().split('\n')
            sections = []
            current_section = None
            current_items = []
            
            for line in lines:
                line_stripped = line.strip()
                if not line_stripped:
                    continue
                
                header_match = re.match(section_pattern, line_stripped)
                
                if header_match and len(line_stripped) < 100:
                    if current_section and current_items:
                        sections.append((current_section, current_items))
                    current_section = header_match.group(1).strip().rstrip(':')
                    current_items = []
                else:
                    clean_line = re.sub(r'^[-•*]\s*', '', line_stripped)
                    clean_line = clean_line.strip()
                    if clean_line:
                        current_items.append(clean_line)
            
            if current_section and current_items:
                sections.append((current_section, current_items))
            
            # Wyświetl sekcje jako karty
            if sections:
                for idx, (section_title, items) in enumerate(sections):
                    # Automatyczne wybieranie koloru i ikony na podstawie tytułu sekcji
                    if 'warunki' in section_title.lower() or 'optymalne' in section_title.lower():
                        icon = '🌟'
                        bg = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                        text_color = 'white'
                    elif 'mocn' in section_title.lower() or 'wzmacnia' in section_title.lower():
                        icon = '💪'
                        bg = 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
                        text_color = 'white'
                    elif 'rozwój' in section_title.lower() or 'rozwija' in section_title.lower():
                        icon = '🚀'
                        bg = 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
                        text_color = '#333'
                    else:
                        icon = '�'
                        bg = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
                        text_color = 'white'
                    
                    # Buduj HTML dla wszystkich punktów w jednej karcie z numeracją
                    items_html = "<ol style='margin: 10px 0 0 20px; padding-left: 0;'>"
                    for item in items:
                        # Przetwórz tekst aby zamienić **tekst** na <strong>tekst</strong>
                        # Użyj regex do zamiany wszystkich wystąpień **coś** na <strong>coś</strong>
                        formatted_item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                        
                        items_html += f"<li style='margin: 10px 0; line-height: 1.6;'>{formatted_item}</li>"
                    
                    items_html += "</ol>"
                    
                    # Jedna karta z nagłówkiem i wszystkimi punktami
                    with st.container():
                        st.markdown(f"""
                        <div style='background: {bg}; 
                                    color: {text_color}; 
                                    padding: 25px; 
                                    border-radius: 15px; 
                                    margin: 15px 0;
                                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                            <h4 style='margin: 0 0 20px 0; color: {text_color};'>{icon} {section_title}</h4>
                            {items_html}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                # Fallback - wyświetl surowy tekst jeśli parsowanie nie zadziałało
                st.markdown(ai_tips_text)
            
            # Debug ekspander - pokaż surowy tekst AI
            with st.expander("🔍 Debug: Zobacz surowy tekst AI"):
                st.code(st.session_state.kolb_ai_tips, language="text")
            
            # Stopka z informacją
            st.markdown("""
            <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                        padding: 20px; 
                        border-radius: 15px; 
                        margin: 20px 0;
                        border-left: 4px solid #667eea;'>
                <p style='margin: 0; color: #2c3e50; font-size: 1.05em;'>
                    💡 <strong>Pamiętaj:</strong> Te wskazówki są dopasowane do Twojego stylu uczenia się. 
                    Testuj je w praktyce i obserwuj co działa najlepiej w Twojej sytuacji.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button("✨ Wygeneruj wskazówki AI", type="primary", use_container_width=True, key="generate_ai_tips"):
                with st.spinner("🤖 AI generuje spersonalizowane wskazówki..."):
                    generate_kolb_ai_tips(dominant, st.session_state.kolb_profession)
                    st.session_state.kolb_ai_generated = True
                    st.rerun()
    
    # Przyciski akcji na dole
    st.markdown("---")
    col_pdf, col_reset, col_close = st.columns([1, 1, 1])
    
    with col_pdf:
        if st.button("📄 Wygeneruj raport PDF", use_container_width=True, type="primary", key="download_kolb_pdf"):
            try:
                html_content = generate_kolb_html_report()
                
                # Zapisz HTML do pliku tymczasowego
                report_filename = f"Kolb_Raport_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                report_path = os.path.join("temp", report_filename)
                
                # Upewnij się że folder temp istnieje
                os.makedirs("temp", exist_ok=True)
                
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                
                # Download button dla HTML
                st.download_button(
                    label="💾 Pobierz raport HTML",
                    data=html_content,
                    file_name=report_filename,
                    mime="text/html",
                    use_container_width=True,
                    key="save_kolb_html"
                )
                
                st.success("✅ Raport wygenerowany!")
                st.info(
                    "📋 **Jak zapisać jako PDF:**\n\n"
                    "1. Otwórz pobrany plik HTML w przeglądarce\n"
                    "2. Naciśnij **Ctrl+P** (Windows) lub **Cmd+P** (Mac)\n"
                    "3. Wybierz **'Zapisz jako PDF'**\n"
                    "4. Kliknij **Zapisz**"
                )
                    
            except Exception as e:
                st.error(f"❌ Błąd podczas generowania raportu: {str(e)}")
    
    with col_reset:
        if st.button("🔄 Rozpocznij test od nowa", use_container_width=True, key="restart_kolb_test"):
            # Ustaw flagę reset, aby zapobiec automatycznemu wczytywaniu wyników z bazy
            st.session_state.kolb_reset = True
            st.session_state.kolb_answers = {}
            st.session_state.kolb_completed = False
            st.session_state.kolb_results = {}
            st.session_state.kolb_dimensions = {}
            st.session_state.kolb_dominant = None
            st.session_state.kolb_quadrant = None
            st.session_state.kolb_flexibility = 0
            st.session_state.kolb_profession = None
            st.session_state.kolb_ai_generated = False
            st.session_state.kolb_ai_tips = None
            st.rerun()
    
    with col_close:
        if st.button("❌ Zamknij test", use_container_width=True, key="close_kolb_from_results"):
            st.session_state.active_tool = None
            st.rerun()

def show_tools_page():

    """Główna strona narzędzi AI"""
    
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Przewiń na górę strony
    scroll_to_top()
    
    # Header strony
    zen_header("🛠️ Narzędzia AI")
    
    # Sprawdź czy użytkownik został przekierowany z Dashboard do Autodiagnozy
    if st.session_state.get('tools_tab') == 'autodiagnoza':
        st.info("💡 Jesteś w zakładce **🎯 Autodiagnoza** - pierwsza zakładka poniżej")
        # Wyczyść flagę po wyświetleniu
        st.session_state.tools_tab = None
    
    # Główne kategorie w tabach
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Autodiagnoza",
        "🧠 C-IQ Tools", 
        "🎭 Symulatory", 
        "📊 Analityki", 
        "🤖 AI Asystent"
    ])
    
    with tab1:
        show_autodiagnosis()
    
    with tab2:
        show_ciq_tools()
    
    with tab3:
        show_simulators()
        
    with tab4:
        show_analytics()
    
    with tab5:
        show_ai_assistant()

def show_ciq_tools():
    """Narzędzia Conversational Intelligence"""
    st.markdown("### 🧠 Narzędzia Conversational Intelligence")
    st.markdown("Wykorzystaj moc AI do analizy i doskonalenia komunikacji na poziomach C-IQ")
    
    # Siatka narzędzi
    col1, col2 = st.columns(2)
    
    with col1:
        # C-IQ Scanner
        with st.container():
            scanner_html = '''
            <div style='padding: 20px; border: 2px solid #4CAF50; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);'>
                <h4>🎯 C-IQ Scanner</h4>
                <p><strong>Zeskanuj poziom komunikacji I otrzymaj wersje na wyższych poziomach C-IQ</strong></p>
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li>📡 Szybkie skanowanie poziomów komunikacji (I, II, III)</li>
                    <li>⚡ Błyskawiczna konwersja na wyższe poziomy</li>
                    <li>🧠 Analiza wpływu neurobiologicznego</li>
                    <li>🎯 Gotowe alternatywne wersje do użycia</li>
                </ul>
            </div>
            '''
            st.markdown(scanner_html, unsafe_allow_html=True)
            
            if zen_button("🎯 Uruchom C-IQ Scanner", key="level_detector", width='stretch'):
                st.session_state.active_tool = "level_detector"
        
    with col2:
        # Conversation Intelligence Pro
        with st.container():
            pro_html = '''
            <div style='padding: 20px; border: 2px solid #E91E63; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #ffeef8 0%, #f8bbd9 100%);'>
                <h4>🧠 Conversation Intelligence Pro</h4>
                <p><strong>Zaawansowana analiza rozmów biznesowych w czasie rzeczywistym</strong></p>
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li>💎 Sentiment i emocje + wpływ neurobiologiczny</li>
                    <li>🎯 Wykrywanie intencji sprzedażowych i biznesowych</li>
                    <li>⚠️ Ostrzeżenia o eskalacji problemów</li>
                    <li>💡 Sugestie real-time dla agentów</li>
                    <li>🔍 Automatyczna kategoryzacja problemów</li>
                </ul>
            </div>
            '''
            st.markdown(pro_html, unsafe_allow_html=True)
            
            if zen_button("🧠 Uruchom CI Pro", key="emotion_detector", width='stretch'):
                st.session_state.active_tool = "emotion_detector"
        
        # C-IQ Leadership Profile
        with st.container():
            leadership_html = '''
            <div style='padding: 20px; border: 2px solid #2196F3; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #e3f2fd 0%, #90caf9 100%);'>
                <h4>💎 C-IQ Leadership Profile</h4>
                <p><strong>Długoterminowa analiza stylu przywództwa przez pryzmat C-IQ</strong></p>
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li>📈 Trend rozwoju C-IQ w czasie</li>
                    <li>🎯 Profil przywódczy (dominujące poziomy)</li>
                    <li>📋 Plan rozwoju komunikacyjnego</li>
                    <li>🏆 Benchmark z innymi liderami</li>
                </ul>
            </div>
            '''
            st.markdown(leadership_html, unsafe_allow_html=True)
            
            if zen_button("💎 Utwórz Profil Lidera", key="communication_analyzer", width='stretch'):
                st.session_state.active_tool = "communication_analyzer"
    
    # Wyświetl aktywne narzędzie
    active_tool = st.session_state.get('active_tool')
    if active_tool:
        st.markdown("---")
        
        # Przycisk resetowania
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if zen_button("❌ Zamknij narzędzie", key="close_tool", width='stretch'):
                del st.session_state.active_tool
                st.rerun()
        
        st.markdown("---")
        
        if active_tool == 'level_detector':
            show_level_detector()
        elif active_tool == 'emotion_detector':
            show_emotion_detector()
        elif active_tool == 'communication_analyzer':
            show_communication_analyzer()

def show_level_detector():
    """C-IQ Scanner - główna funkcjonalność"""
    st.markdown("## 🎯 C-IQ Scanner")
    st.markdown("**Zeskanuj poziom komunikacji** i **zobacz alternatywne wersje** na wyższych poziomach Conversational Intelligence")
    
    # Tabs z różnymi trybami
    tab1, tab2, tab3 = st.tabs([
        "📝 Analiza tekstu", 
        "💬 Przykłady poziomów", 
        "📧 Szablony emaili"
    ])
    
    with tab1:
        st.markdown("#### Wklej dowolny tekst do analizy C-IQ")
        
        # Przykłady do szybkiego testowania
        with st.expander("💡 Przykłady do przetestowania", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Poziom I (Transakcyjny):**")
                example_1 = "Wyślij raport do końca dnia. Brak dyskusji."
                if st.button("📋 Użyj przykładu", key="example_1"):
                    st.session_state.level_detector_input = example_1
                
                st.markdown("**Poziom II (Pozycyjny):**") 
                example_2 = "Uważam, że ten pomysł nie ma sensu. Moja propozycja jest lepsza bo..."
                if st.button("📋 Użyj przykładu", key="example_2"):
                    st.session_state.level_detector_input = example_2
            
            with col2:
                st.markdown("**Poziom III (Transformacyjny):**")
                example_3 = "Jakie widzisz możliwości w tej sytuacji? Jak możemy razem wypracować rozwiązanie, które będzie działać dla wszystkich?"
                if st.button("📋 Użyj przykładu", key="example_3"):
                    st.session_state.level_detector_input = example_3
        
        text_input = st.text_area(
            "Tekst do analizy:",
            value=st.session_state.get('level_detector_input', ''),
            placeholder="Wklej tutaj email, transkrypcję rozmowy, lub planowaną wypowiedź...",
            height=200,
            key="level_detector_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if zen_button("📡 Skanuj poziom C-IQ", key="analyze_level", width='stretch'):
                if text_input and text_input.strip():
                    with st.spinner("🤖 Scanner analizuje poziom rozmowy..."):
                        result = analyze_conversation_level(text_input)
                        if result:
                            st.session_state.last_analysis_result = result
                            
                            # Przyznaj XP za użycie narzędzia CIQ Scanner
                            try:
                                from data.users import award_xp_for_activity
                                award_xp_for_activity(
                                    st.session_state.username,
                                    'tool_used',
                                    1,  # 1 XP za użycie narzędzia
                                    {
                                        'tool_name': 'CIQ Scanner',
                                        'detected_level': result.get('detected_level', 'unknown'),
                                        'confidence': result.get('confidence', 0)
                                    }
                                )
                                st.success("✅ Analiza ukończona! +1 XP")
                            except Exception:
                                pass  # Nie przerywaj jeśli tracking się nie powiedzie
                        else:
                            st.error("Nie udało się przeanalizować tekstu. Spróbuj ponownie.")
                else:
                    st.warning("⚠️ Wpisz tekst do analizy")
        
        with col2:
            if text_input:
                word_count = len(text_input.split())
                st.metric("Słowa", word_count)
        
        # Wyświetl wynik analizy jeśli istnieje
        if 'last_analysis_result' in st.session_state and text_input and text_input.strip():
            st.markdown("---")
            
            if st.session_state.last_analysis_result.get('analyzed_text') != text_input:
                st.warning("⚠️ Pokazuję wynik dla poprzedniego tekstu. Kliknij 'Analizuj' ponownie.")
                
            display_level_analysis(st.session_state.last_analysis_result)
    
    with tab2:
        show_ciq_examples()
    
    with tab3:
        show_email_templates()

def analyze_conversation_level(text: str) -> Optional[Dict]:
    """Analizuje poziom C-IQ w tekście"""
    
    evaluator = AIExerciseEvaluator()
    
    # Sprawdź czy evaluator jest w demo mode
    if hasattr(evaluator, 'demo_mode') and evaluator.demo_mode:
        st.info("ℹ️ C-IQ Scanner w trybie demo - używam analizy heurystycznej")
        return create_fallback_analysis(text)
    
    prompt = f"""
Jesteś ekspertem w Conversational Intelligence. Przeanalizuj następujący tekst i określ jego poziom C-IQ.

TEKST DO ANALIZY:
"{text}"

POZIOMY C-IQ:
- **Poziom I (Transakcyjny)**: Wymiana informacji, fokus na zadania, język dyrektywny, brak emocji, jednokierunkowa komunikacja
- **Poziom II (Pozycyjny)**: Obrona stanowisk, argumentowanie, "my vs oni", konfrontacja, przekonywanie, walka o rację  
- **Poziom III (Transformacyjny)**: Współtworzenie, pytania otwarte, "wspólny cel", budowanie zaufania, język partnerski

WAŻNE: 
1. Odpowiedz TYLKO w poprawnym formacie JSON, bez dodatkowych komentarzy.
2. MUSISZ wybrać JEDEN dominujący poziom - nie można wykrywać wielu poziomów jednocześnie:
   - "detected_level" może być tylko: "Poziom I" lub "Poziom II" lub "Poziom III"
   - Wybierz poziom który najlepiej charakteryzuje CAŁOŚĆ tekstu
   - Jeśli tekst zawiera elementy różnych poziomów, wybierz ten który DOMINUJE
3. W sekcji "alternative_versions" podaj alternatywy TYLKO dla poziomów wyższych niż wykryty:
   - Jeśli wykryjesz Poziom I: podaj wersje dla II i III
   - Jeśli wykryjesz Poziom II: podaj wersję tylko dla III  
   - Jeśli wykryjesz Poziom III: pozostaw alternative_versions puste {{}}

{{
    "detected_level": "Poziom I/II/III",
    "confidence": [1-10],
    "explanation": "Szczegółowe wyjaśnienie dlaczego to ten poziom - cytuj konkretne fragmenty",
    "key_indicators": ["konkretny wskaźnik językowy 1", "konkretny wskaźnik językowy 2"],
    "neurobiological_impact": "Przewidywany wpływ na hormony - czy wzbudza kortyzol (stres) czy oksytocynę (zaufanie)",
    "improvement_suggestions": ["jak podnieść na wyższy poziom - konkretne zmiany"],
    "alternative_versions": {{
        "level_ii": "Jak brzmiałby ten tekst przepisany na poziom II (tylko jeśli wykryty poziom to I)",
        "level_iii": "Jak brzmiałby ten tekst przepisany na poziom III (jeśli wykryty poziom to I lub II)"
    }},
    "practical_tips": ["konkretna wskazówka komunikacyjna 1", "konkretna wskazówka 2"],
    "emotional_tone": "neutralny/pozytywny/negatywny/agresywny/partnerski",
    "trust_building_score": [1-10],
    "language_patterns": ["wzorzec językowy 1", "wzorzec językowy 2"]
}}
"""
    
    try:
        # Użyj bezpośrednio funkcji z AIExerciseEvaluator
        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            
            if response and response.text:
                content = response.text.strip()
                
                # Usuń markdown formatowanie jeśli jest
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                
                # Spróbuj sparsować JSON
                import json
                import re
                
                # Znajdź JSON w odpowiedzi
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    
                    try:
                        result = json.loads(json_str)
                        
                        # Sprawdź czy mamy wymagane pola dla detektora C-IQ
                        if 'detected_level' in result and 'confidence' in result:
                            st.success("✅ Skanowanie C-IQ ukończone!")
                            # Dodaj analizowany tekst do wyniku
                            result['analyzed_text'] = text
                            return result
                        else:
                            st.warning("⚠️ AI zwróciło niepełną analizę")
                            st.json(result)  # Pokaż co zwróciło
                            return create_fallback_analysis(text)
                            
                    except json.JSONDecodeError as json_err:
                        st.error(f"❌ Błąd parsowania JSON: {str(json_err)}")
                        st.warning("Używam analizy backup zamiast niepoprawnego JSON")
                        return create_fallback_analysis(text)
                else:
                    st.warning("⚠️ Nie udało się znaleźć JSON w odpowiedzi AI")
                    return create_fallback_analysis(text)
            else:
                st.warning("⚠️ AI nie zwróciło odpowiedzi")
                return create_fallback_analysis(text)
        else:
            st.warning("⚠️ Model AI niedostępny")
            return create_fallback_analysis(text)
            
    except Exception as e:
        st.error(f"❌ Błąd podczas analizy: {str(e)}")
        return create_fallback_analysis(text)

def create_fallback_analysis(text: str) -> Dict:
    """Tworzy fallback analizę gdy AI nie działa"""
    
    text_lower = text.lower()
    word_count = len(text.split())
    
    # Prosta heurystyka do określenia poziomu
    level_iii_keywords = ['jak', 'możemy', 'razem', 'wspólnie', 'jakie', 'czy moglibyśmy', 'co myślisz', 'jak widzisz']
    level_ii_keywords = ['uważam', 'myślę że', 'nie zgadzam się', 'moja propozycja', 'lepiej by było']
    level_i_keywords = ['wyślij', 'zrób', 'musisz', 'wykonaj', 'deadline', 'koniec']
    
    level_iii_score = sum(1 for keyword in level_iii_keywords if keyword in text_lower)
    level_ii_score = sum(1 for keyword in level_ii_keywords if keyword in text_lower)
    level_i_score = sum(1 for keyword in level_i_keywords if keyword in text_lower)
    
    if level_iii_score > max(level_ii_score, level_i_score):
        detected_level = "Poziom III"
        confidence = min(9, 6 + level_iii_score)
        trust_score = min(9, 7 + level_iii_score)
        explanation = "Tekst zawiera elementy współtworzenia i pytania otwarte charakterystyczne dla Poziomu III."
    elif level_ii_score > level_i_score:
        detected_level = "Poziom II" 
        confidence = min(8, 5 + level_ii_score)
        trust_score = max(3, 6 - level_ii_score)
        explanation = "Tekst zawiera elementy argumentacji i obrony stanowisk charakterystyczne dla Poziomu II."
    else:
        detected_level = "Poziom I"
        confidence = min(8, 5 + level_i_score) 
        trust_score = max(2, 5 - level_i_score)
        explanation = "Tekst ma charakter transakcyjny i dyrektywny charakterystyczny dla Poziomu I."
    
    # Twórz alternatywne wersje zależnie od wykrytego poziomu
    alternative_versions = {}
    
    if detected_level == "Poziom I":
        alternative_versions = {
            "level_ii": f"Uważam, że ta sytuacja wymaga analizy. Moja perspektywa jest taka, że...",
            "level_iii": f"Jakie widzimy możliwości w tej sytuacji? Jak możemy razem wypracować najlepsze rozwiązanie?"
        }
    elif detected_level == "Poziom II":
        alternative_versions = {
            "level_iii": f"Jakie widzimy możliwości w tej sytuacji? Jak możemy razem wypracować rozwiązanie, które będzie działać dla wszystkich?"
        }
    # Poziom III nie ma alternatyw - to już najwyższy poziom
    
    return {
        "analyzed_text": text,
        "detected_level": detected_level,
        "confidence": confidence,
        "explanation": explanation,
        "key_indicators": [f"Długość tekstu: {word_count} słów", "Analiza heurystyczna słów kluczowych"],
        "neurobiological_impact": f"Przewidywany wpływ odpowiada charakterystyce {detected_level}",
        "improvement_suggestions": ["Dodaj więcej pytań otwartych", "Użyj języka współtworzenia"] if detected_level != "Poziom III" else ["Kontynuuj używanie transformacyjnego stylu komunikacji"],
        "alternative_versions": alternative_versions,
        "practical_tips": ["Zadawaj więcej pytań otwartych", "Używaj języka 'my' zamiast 'ty'"] if detected_level != "Poziom III" else ["Wykorzystuj moc współtworzenia", "Buduj na osiągniętym wysokim poziomie"],
        "emotional_tone": "neutralny",
        "trust_building_score": trust_score,
        "language_patterns": ["Wykryte wzorce na podstawie analizy słów kluczowych"]
    }

def display_level_analysis(result: Dict):
    """Wyświetla wyniki analizy poziom C-IQ"""
    
    if not result:
        st.error("Brak wyników analizy")
        return
    
    # Główny wynik w metrykach
    level = result.get('detected_level', 'Nie określono')
    confidence = result.get('confidence', 0)
    trust_score = result.get('trust_building_score', 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Wykryty poziom", level)
    with col2:
        st.metric("🎲 Pewność analizy", f"{confidence}/10")
    with col3:
        st.metric("🤝 Budowanie zaufania", f"{trust_score}/10")
    
    # Wizualizacja poziomów z kolorami - poprawiona logika wykrywania
    st.markdown("### 📊 Analiza poziomów C-IQ")
    
    level_info = {
        "Poziom I": {"color": "🔴", "desc": "Transakcyjny - wymiana informacji", "bg": "#ffebee"},
        "Poziom II": {"color": "🟡", "desc": "Pozycyjny - obrona stanowisk", "bg": "#fff8e1"}, 
        "Poziom III": {"color": "🟢", "desc": "Transformacyjny - współtworzenie", "bg": "#e8f5e8"}
    }
    
    # Lepsze wykrywanie dominującego poziomu  
    detected_level = result.get('detected_level', '').strip()
    
    for lvl, info in level_info.items():
        # Precyzyjne wykrywanie - tylko jeden poziom może być aktywny
        is_detected = False
        
        if "III" in detected_level and lvl == "Poziom III":
            is_detected = True
        elif "II" in detected_level and "III" not in detected_level and lvl == "Poziom II":
            is_detected = True  
        elif "I" in detected_level and "II" not in detected_level and "III" not in detected_level and lvl == "Poziom I":
            is_detected = True
            
        border_style = "border: 2px solid #4CAF50;" if is_detected else "border: 1px solid #ddd;"
        selected_indicator = "<strong>🎯 WYKRYTO</strong>" if is_detected else ""
        
        st.markdown(f"""
        <div style='padding: 15px; margin: 5px 0; border-radius: 10px; background-color: {info['bg']}; {border_style}'>
            {info['color']} <strong>{lvl}</strong> {selected_indicator}<br>
            <span style='color: #666;'>{info['desc']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Szczegółowe wyjaśnienie
    if 'explanation' in result:
        st.markdown("### 💡 Szczegółowa analiza")
        st.info(result['explanation'])
    
    # Wskaźniki w dwóch kolumnach
    col1, col2 = st.columns(2)
    
    with col1:
        # Wskaźniki kluczowe
        if 'key_indicators' in result:
            st.markdown("### 🔍 Kluczowe wskaźniki językowe")
            for indicator in result['key_indicators']:
                st.markdown(f"• {indicator}")
        
        # Wzorce językowe
        if 'language_patterns' in result:
            st.markdown("### 📝 Wzorce językowe")
            for pattern in result['language_patterns']:
                st.markdown(f"• {pattern}")
    
    with col2:
        # Ton emocjonalny
        if 'emotional_tone' in result:
            st.markdown("### 🎭 Ton emocjonalny")
            tone = result['emotional_tone']
            tone_colors = {
                'pozytywny': '🟢', 'neutralny': '🟡', 'negatywny': '🔴',
                'agresywny': '🔴', 'partnerski': '🟢'
            }
            color = tone_colors.get(tone.lower(), '⚪')
            st.markdown(f"{color} **{tone.title()}**")
        
        # Wpływ neurobiologiczny
        if 'neurobiological_impact' in result:
            st.markdown("### 🧠 Wpływ neurobiologiczny")
            st.warning(result['neurobiological_impact'])
    
    # Sugestie poprawy
    if 'improvement_suggestions' in result:
        st.markdown("### 🎯 Jak podnieść poziom komunikacji")
        for suggestion in result['improvement_suggestions']:
            st.markdown(f"• {suggestion}")
    
    # Alternatywne wersje w expanderach - pokazuj tylko wyższe poziomy
    if 'alternative_versions' in result:
        alt_versions = result['alternative_versions']
        detected_level = result.get('detected_level', '')
        
        # Logika: WAŻNE - sprawdzaj od najdłuższego do najkrótszego ciągu!
        if 'Poziom III' in detected_level:
            # Dla poziomu III: BRAK nagłówka, tylko gratulacje
            st.success("🎉 **Gratulacje!** To już najwyższy poziom C-IQ - Transformacyjny!")
            st.info("💡 **Twoja komunikacja wykorzystuje:**\n"
                   "• Język współtworzenia\n"
                   "• Pytania otwarte\n" 
                   "• Budowanie wspólnych celów\n"
                   "• Stymulację oksytocyny (zaufanie)")
                   
        elif 'Poziom II' in detected_level:
            # Dla poziomu II: pokaż nagłówek i alternatywę III
            st.markdown("### 🔄 Jak brzmiałoby na wyższym poziomie C-IQ")
            
            if 'level_iii' in alt_versions and alt_versions['level_iii']:
                with st.expander("🚀 Poziom III - Transformacyjny", expanded=False):
                    st.success(alt_versions['level_iii'])
            else:
                st.info("🎉 To już wysoki poziom komunikacji! Poziom III to najwyższy dostępny poziom.")
                
        elif 'Poziom I' in detected_level:
            # Dla poziomu I: pokaż nagłówek i alternatywy II + III
            st.markdown("### 🔄 Jak brzmiałoby na wyższych poziomach C-IQ")
            
            if 'level_ii' in alt_versions and alt_versions['level_ii']:
                with st.expander("📈 Poziom II - Pozycyjny", expanded=False):
                    st.success(alt_versions['level_ii'])
            
            if 'level_iii' in alt_versions and alt_versions['level_iii']:
                with st.expander("🚀 Poziom III - Transformacyjny", expanded=False):
                    st.success(alt_versions['level_iii'])
        else:
            # Fallback dla nieokreślonych poziomów - pokaż nagłówek
            st.markdown("### 🔄 Jak brzmiałoby na wyższych poziomach C-IQ")
            
            if 'level_ii' in alt_versions and alt_versions['level_ii']:
                with st.expander("📈 Poziom II - Pozycyjny", expanded=False):
                    st.success(alt_versions['level_ii'])
            
            if 'level_iii' in alt_versions and alt_versions['level_iii']:
                with st.expander("🚀 Poziom III - Transformacyjny", expanded=False):
                    st.success(alt_versions['level_iii'])
    
    # Praktyczne wskazówki
    if 'practical_tips' in result:
        st.markdown("### 💡 Praktyczne wskazówki do zastosowania")
        for i, tip in enumerate(result['practical_tips'], 1):
            st.markdown(f"**{i}.** {tip}")

def show_ciq_examples():
    """Pokazuje przykłady różnych poziomów C-IQ"""
    st.markdown("#### 📚 Przykłady poziomów C-IQ w praktyce")
    
    examples = [
        {
            "scenario": "Informowanie o problemie w projekcie",
            "level_1": "Projekt się opóźnia. Deadline za tydzień. Pracujcie dłużej.",
            "level_2": "Uważam, że zespół nie wywiązuje się z zobowiązań. To wina słabego planowania z waszej strony.",
            "level_3": "Widzę, że projekt może się opóźnić. Jakie widzicie przyczyny tej sytuacji? Jak możemy razem znaleźć rozwiązanie?"
        },
        {
            "scenario": "Feedback dla pracownika",
            "level_1": "Twój raport ma błędy. Popraw i wyślij ponownie.",
            "level_2": "Nie zgadzam się z Twoim podejściem. Moja metoda jest lepsza, ponieważ...",
            "level_3": "Zauważyłem kilka obszarów w raporcie, które możemy razem ulepszyć. Co myślisz o tych aspektach?"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        st.markdown(f"### Przykład {i}: {example['scenario']}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🔴 Poziom I - Transakcyjny**")
            st.text_area(
                "Poziom I",
                value=example['level_1'],
                height=100,
                key=f"example_{i}_1",
                label_visibility="collapsed"
            )
            
        with col2:
            st.markdown("**🟡 Poziom II - Pozycyjny**")
            st.text_area(
                "Poziom II",
                value=example['level_2'],
                height=100,
                key=f"example_{i}_2",
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown("**🟢 Poziom III - Transformacyjny**")
            st.text_area(
                "Poziom III",
                value=example['level_3'],
                height=100,
                key=f"example_{i}_3",
                label_visibility="collapsed"
            )

def show_email_templates():
    """Pokazuje szablony emaili na różnych poziomach C-IQ"""
    st.markdown("#### 📧 Szablony emaili biznesowych")
    st.info("🚧 Funkcja w przygotowaniu - biblioteka szablonów emaili na różnych poziomach C-IQ")

def show_emotion_detector():
    """Conversation Intelligence Pro - Analiza rozmów menedżerskich"""
    st.markdown("## 🧠 Conversation Intelligence Pro")
    st.markdown("**Zaawansowana analiza rozmów menedżerskich** - C-IQ w kontekście przywództwa i zarządzania zespołem")
    
    # Tabs dla różnych funkcji CI w kontekście menedżerskim
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Analiza Rozmowy", 
        "🎯 Dynamika Zespołu", 
        "⚠️ Sygnały Problemów", 
        "💡 Leadership Coach"
    ])
    
    with tab1:
        show_sentiment_analysis()
    
    with tab2:
        show_intent_detection()
        
    with tab3:
        show_escalation_monitoring()
        
    with tab4:
        show_ai_coach()

def show_sentiment_analysis():
    """Analiza rozmów menedżerskich"""
    st.markdown("### 📊 Analiza Rozmowy Menedżer-Pracownik")
    
    conversation_text = st.text_area(
        "🎤 Wklej transkrypcję rozmowy menedżerskiej:",
        placeholder="""Przykład rozmowy menedżer-pracownik:
Menedżer: Chciałbym porozmawiać o Twoich ostatnich projektach.
Pracownik: Okej, ale muszę powiedzieć, że czuję się przeciążony zadaniami...
Menedżer: Rozumiem, opowiedz mi więcej o tym przeciążeniu...""",
        height=120,
        key="sentiment_input"
    )
    
    if conversation_text and len(conversation_text) > 10:
        if zen_button("📊 Analizuj Sentiment + C-IQ", key="analyze_sentiment", width='stretch'):
            with st.spinner("🔍 Analizuję sentiment i poziomy C-IQ..."):
                # Analiza C-IQ + sentiment
                result = analyze_conversation_sentiment(conversation_text)
                if result:
                    display_sentiment_results(result)
                    
                    # Przyznaj XP za użycie narzędzia
                    try:
                        from data.users import award_xp_for_activity
                        award_xp_for_activity(
                            st.session_state.username,
                            'tool_used',
                            1,
                            {'tool_name': 'Conversation Intelligence Pro - Sentiment Analysis'}
                        )
                    except Exception:
                        pass

def show_intent_detection():
    """Wykrywanie dynamiki zespołowej i potrzeb pracowników"""
    st.markdown("### 🎯 Analiza Dynamiki Zespołu i Motywacji")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔍 Wykrywane potrzeby pracownika:**")
        st.markdown("• 🎯 Potrzeba jasnych celów")
        st.markdown("• 📚 Chęć rozwoju i szkoleń") 
        st.markdown("• 🤝 Potrzeba wsparcia/mentoringu")
        st.markdown("• ⚖️ Sygnały wypalenia zawodowego")
        st.markdown("• 🚀 Ambicje i aspiracje kariery")
        
    with col2:
        st.markdown("**📈 Wyniki analizy:**")
        st.markdown("• Poziom zaangażowania zespołu")
        st.markdown("• Rekomendowane akcje menedżerskie")  
        st.markdown("• Optymalne momenty na feedback")
        st.markdown("• Przewidywane reakcje pracownika")
    
    intent_text = st.text_area(
        "Tekst do analizy dynamiki zespołu:",
        placeholder="Wklej fragment rozmowy menedżer-pracownik o zadaniach, celach, problemach...",
        height=100,
        key="intent_input"
    )
    
    if intent_text and len(intent_text) > 10:
        if zen_button("🎯 Wykryj Intencje", key="detect_intent", width='stretch'):
            result = analyze_business_intent(intent_text)
            if result:
                display_intent_results(result)
                
                # Przyznaj XP za użycie narzędzia
                try:
                    from data.users import award_xp_for_activity
                    award_xp_for_activity(
                        st.session_state.username,
                        'tool_used',
                        1,
                        {'tool_name': 'Conversation Intelligence Pro - Intent Detection'}
                    )
                except Exception:
                    pass

def show_escalation_monitoring():
    """Monitoring sygnałów problemów w zespole"""
    st.markdown("### ⚠️ Wykrywanie Sygnałów Problemów Zespołowych")
    
    st.info("💡 **Early warning system** dla problemów zespołowych: wypalenie, konflikty, spadek motywacji")
    
    escalation_text = st.text_area(
        "🚨 Tekst do analizy sygnałów problemów:",
        placeholder="Wklej fragment rozmowy z pracownikiem, który może sygnalizować problemy zespołowe...",
        height=100,
        key="escalation_input"
    )
    
    # Ustawienia czułości
    sensitivity = st.slider(
        "🎚️ Czułość wykrywania eskalacji:",
        min_value=1, max_value=10, value=5,
        help="1 = tylko oczywiste sygnały, 10 = bardzo wyczulone wykrywanie"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**⚠️ Sygnały eskalacji:**")
        st.markdown("• Spadek motywacji i zaangażowania")
        st.markdown("• Sygnały wypalenia zawodowego") 
        st.markdown("• Konflikty interpersonalne")
        st.markdown("• Rozważanie zmiany pracy")
        
    with col2:
        st.markdown("**🎯 Rekomendowane akcje:**")
        st.markdown("• Rozmowa 1-on-1 z pracownikiem")
        st.markdown("• Przegląd obciążenia i zadań")
        st.markdown("• Plan rozwoju i wsparcia")
        st.markdown("• Poprawa warunków pracy")
    
    if escalation_text and len(escalation_text) > 10:
        if zen_button("🚨 Sprawdź Ryzyko Eskalacji", key="check_escalation", width='stretch'):
            result = analyze_escalation_risk(escalation_text, sensitivity)
            if result:
                display_escalation_results(result)
                
                # Przyznaj XP za użycie narzędzia
                try:
                    from data.users import award_xp_for_activity
                    award_xp_for_activity(
                        st.session_state.username,
                        'tool_used',
                        1,
                        {'tool_name': 'Conversation Intelligence Pro - Escalation Monitoring'}
                    )
                except Exception:
                    pass

def show_ai_coach():
    """Real-time coach dla menedżerów"""
    st.markdown("### 💡 Leadership Coach - Wsparcie Real-time")
    
    st.info("🎯 **Inteligentny coach przywództwa** podpowiadający najlepsze odpowiedzi w trudnych sytuacjach menedżerskich")
    
    # Kontekst rozmowy menedżerskiej
    context = st.selectbox(
        "🎭 Typ rozmowy menedżerskiej:",
        [
            "🎯 Ustawienie celów i oczekiwań",
            "📈 Feedback o wydajności", 
            "💬 Rozmowa z demotywowanym pracownikiem",
            "⚡ Zarządzanie konfliktem w zespole",
            "🚀 Rozmowa rozwojowa i kariera",
            "📋 Delegowanie zadań i odpowiedzialności",
            "🔄 Zarządzanie zmianą organizacyjną",
            "⚠️ Rozmowa dyscyplinująca"
        ]
    )
    
    coach_text = st.text_area(
        "💬 Ostatnia wypowiedź pracownika:",
        placeholder="Wklej co właśnie powiedział pracownik, a AI zasugeruje najlepszą odpowiedź menedżerską...",
        height=100,
        key="coach_input"
    )
    
    if coach_text and len(coach_text) > 5:
        if zen_button("💡 Podpowiedz Odpowiedź", key="suggest_response", width='stretch'):
            result = get_ai_coaching(coach_text, context)
            if result:
                display_coaching_results(result)
                
                # Przyznaj XP za użycie narzędzia
                try:
                    from data.users import award_xp_for_activity
                    award_xp_for_activity(
                        st.session_state.username,
                        'tool_used',
                        1,
                        {'tool_name': 'Conversation Intelligence Pro - AI Coach'}
                    )
                except Exception:
                    pass


def show_communication_analyzer():
    """C-IQ Leadership Profile - długoterminowa analiza stylu przywództwa"""
    st.markdown("## 💎 C-IQ Leadership Profile")
    st.markdown("**Długoterminowa analiza Twojego stylu przywództwa** przez pryzmat Conversational Intelligence")
    
    st.info("💎 **Unikalność:** To jedyne narzędzie które analizuje **wzorce długoterminowe** w Twoim stylu przywództwa, zamiast pojedynczych rozmów")
    
    # Auto-wczytywanie zapisanego profilu
    if hasattr(st.session_state, 'username') and st.session_state.username:
        if 'leadership_profile' not in st.session_state:
            saved_profile = load_leadership_profile(st.session_state.username)
            if saved_profile:
                st.session_state['leadership_profile'] = saved_profile
                st.success(f"📂 Wczytano Twój zapisany profil przywódczy z {saved_profile.get('created_at', 'wcześniej')[:10]}")
    
    # Tabs dla różnych aspektów profilu
    tab1, tab2, tab3 = st.tabs([
        "📊 Upload Danych", 
        "👤 Profil Przywódczy", 
        "🎯 Plan Rozwoju"
    ])
    
    with tab1:
        st.markdown("### 📊 Wgraj próbki swojej komunikacji")
        st.markdown("Im więcej danych, tym dokładniejszy profil przywódczy!")
        
        # Opis co będzie w raporcie
        st.markdown("**📋 Twój raport będzie zawierał:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🎯 Poziomy C-IQ**")
            st.markdown("• Dominujący poziom")
            st.markdown("• Rozkład procentowy")
            st.markdown("• Rekomendacje")
        
        with col2:
            st.markdown("**🧠 Neurobiologia**") 
            st.markdown("• Wpływ na kortyzol")
            st.markdown("• Stymulacja oksytocyny")
            st.markdown("• Bezpieczeństwo psychologiczne")
        
        with col3:
            st.markdown("**📈 Skuteczność**")
            st.markdown("• Clarność przekazu")
            st.markdown("• Potencjał zaufania")
            st.markdown("• Ryzyko konfliktu")
            
        st.markdown("---")
        
        # Przycisk do przykładowych danych
        col_demo, col_info = st.columns([1, 3])
        with col_demo:
            demo_col1, demo_col2 = st.columns(2)
            with demo_col1:
                if zen_button("🎯 Użyj przykładów", key="fill_demo_data"):
                    # Bezpośrednio ustawiamy wartości w session_state
                    team_conv_text = '''Menedżer: Kasia, muszę wiedzieć co się dzieje z projektem ABC. Deadline jest za tydzień!
Pracownik: Mam problem z terminem, klient ciągle zmienia wymagania
Menedżer: To nie jest wymówka. Musisz lepiej planować. Co konkretnie robiłaś przez ostatnie dni?
Pracownik: Próbowałam dopasować się do nowych wymagań, ale...
Menedżer: Słuchaj, potrzebuję rozwiązań, nie problemów. Jak zamierzasz to naprawić?
Pracownik: Może gdybym miała więcej wsparcia od zespołu?
Menedżer: Dobrze, porozmawiam z Tomkiem żeby ci pomógł. Ale chcę codzienne raporty z postępów.'''
                    st.session_state['team_conv'] = team_conv_text
                    
                    feedback_conv_text = '''Menedżer: Tomek, muszę z tobą porozmawiać o ocenach. Twoje wyniki techniczne są ok, ale komunikacja kuleje
Pracownik: Czyli co dokładnie robię źle?
Menedżer: Za mało komunikujesz się z zespołem. Ludzie nie wiedzą nad czym pracujesz
Pracownik: Ale skupiam się na pracy, żeby była jakość...
Menedżer: To nie usprawiedliwia braku komunikacji. Od następnego tygodnia codzienne updaty na kanale zespołowym. Rozumiesz?
Pracownik: Tak, rozumiem
Menedżer: I jeszcze jedno - więcej inicjatywy. Nie czekaj aż ktoś ci każe coś zrobić.'''
                    st.session_state['feedback_conv'] = feedback_conv_text
                    
                    conflict_conv_text = '''Menedżer: Ania, słyszałem że wczoraj kłóciłaś się z Markiem o dane do raportu
Pracownik: To był stres, przepraszam. Deadline naciska i...
Menedżer: Nie obchodzą mnie wymówki. W biurze nie krzyczy się na współpracowników. Kropka.
Pracownik: Ale Marek miał dostarczyć dane tydzień temu, a...
Menedżer: To nie usprawiedliwia takiego zachowania. Następnym razem przychodzisz do mnie, zamiast robić scenę
Pracownik: Dobrze, ale co z tymi danymi?
Menedżer: Porozmawiam z Markiem. A ty przeprosisz go jutro. I żeby więcej takich sytuacji nie było.'''
                    st.session_state['conflict_conv'] = conflict_conv_text
                    
                    motivation_conv_text = '''Menedżer: Paweł, dobra robota z tym automatycznym raportem. Działa jak należy
Pracownik: Dzięki, starałem się...
Menedżer: No właśnie. Trzeba było tylko trochę nacisnąć. Widzisz? Jak się chce, to się można
Pracownik: Tak, chociaż trochę czasu mi to zajęło
Menedżer: Czas to pieniądz. Następnym razem rób szybciej, ale tak samo dokładnie. Może dostaniesz więcej takich projektów
Pracownik: To brzmi dobrze. Co mam teraz robić?
Menedżer: Sprawdź czy wszystko działa i zrób dokumentację. Do końca tygodnia ma być gotowe.'''
                    st.session_state['motivation_conv'] = motivation_conv_text
                    
                    st.success("✅ Wypełniono pola przykładowymi danymi! Przewiń w dół żeby zobaczyć dane.")
                    
            with demo_col2:
                if zen_button("🧹 Wyczyść pola", key="clear_data"):
                    # Czyścimy wartości w session_state
                    st.session_state['team_conv'] = ""
                    st.session_state['feedback_conv'] = ""
                    st.session_state['conflict_conv'] = ""
                    st.session_state['motivation_conv'] = ""
                    st.success("🧹 Wyczyszczono wszystkie pola! Przewiń w dół żeby sprawdzić.")
        
        with col_info:
            st.info("💡 **Wskazówka:** Wklej rzeczywiste fragmenty swoich rozmów (minimum 2-3 zdania na pole). Możesz też kliknąć 'Użyj przykładów' żeby zobaczyć jak działa narzędzie.")
            
            # Debug info
            if st.session_state.get('team_conv'):
                st.write(f"🔍 Debug: team_conv ma {len(st.session_state.get('team_conv', ''))} znaków")
        
        # Multiple text areas dla różnych sytuacji
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🎯 Rozmowy z zespołem:**")
            team_conversations = st.text_area(
                "Wklej fragmenty rozmów z pracownikami:",
                placeholder="Wklej tutaj rzeczywiste fragmenty swoich rozmów z zespołem...",
                height=150,
                key="team_conv"
            )
            
            st.markdown("**📈 Feedback i oceny:**")
            feedback_conversations = st.text_area(
                "Fragmenty rozmów feedbackowych:",
                placeholder="Wklej tutaj fragmenty rozmów dotyczących ocen i feedbacku...", 
                height=150,
                key="feedback_conv"
            )

        with col2:
            st.markdown("**⚡ Sytuacje konfliktowe:**")
            conflict_conversations = st.text_area(
                "Rozmowy w trudnych sytuacjach:",
                placeholder="Wklej tutaj fragmenty trudnych rozmów i rozwiązywania konfliktów...",
                height=150,
                key="conflict_conv"
            )
            
            st.markdown("**🚀 Motywowanie zespołu:**")
            motivation_conversations = st.text_area(
                "Fragmenty motywujące i inspirujące:",
                placeholder="Wklej tutaj fragmenty motywujących rozmów z zespołem...",
                height=150,
                key="motivation_conv"
            )
        
        st.markdown("---")
        st.markdown("#### 📋 Wskazówki do wypełnienia:")
        tip_col1, tip_col2, tip_col3 = st.columns(3)
        
        with tip_col1:
            st.markdown("**✅ Dobre przykłady:**")
            st.markdown("• Pełne dialogi (2-6 wymian)")
            st.markdown("• Rzeczywiste sytuacje")
            st.markdown("• Różnorodne scenariusze")
        
        with tip_col2:
            st.markdown("**❌ Unikaj:**")
            st.markdown("• Pojedynczych zdań")
            st.markdown("• Zbyt ogólnych opisów")
            st.markdown("• Danych osobowych")
            
        with tip_col3:
            st.markdown("**🎯 Minimalna ilość:**")
            st.markdown("• Przynajmniej 2 pola wypełnione")
            st.markdown("• Po 3-5 zdań w każdym")
            st.markdown("• Łącznie ~200 słów")
        
        # Licznik słów i status gotowości
        all_conversations = [team_conversations, feedback_conversations, conflict_conversations, motivation_conversations]
        filled_fields = sum(1 for conv in all_conversations if conv.strip())
        total_words = sum(len(conv.split()) for conv in all_conversations if conv.strip())
        
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric("Wypełnione pola", f"{filled_fields}/4")
        with col_stats2:
            st.metric("Łączna liczba słów", total_words)
        with col_stats3:
            if filled_fields >= 2 and total_words >= 150:
                st.success("✅ Gotowe do analizy!")
            elif total_words < 150:
                st.warning(f"⏳ Potrzeba jeszcze {150-total_words} słów")
            else:
                st.info("📝 Wypełnij więcej pól")
        
        # Pole na nazwę profilu (opcjonalne)
        profile_name = st.text_input(
            "📝 Nazwa profilu (opcjonalnie):",
            placeholder="np. 'Październik 2024' lub 'Po szkoleniu C-IQ'",
            help="Opcjonalna nazwa ułatwiająca rozpoznanie profilu w przyszłości"
        )
        
        # Przycisk analizy
        analysis_ready = filled_fields >= 2 and total_words >= 150
        if zen_button("🔍 Analizuj Mój Styl Przywództwa", 
                     key="analyze_leadership", 
                     width='stretch',
                     disabled=not analysis_ready):
            conversations_text = "\n---\n".join([conv for conv in all_conversations if conv.strip()])
            
            if conversations_text:
                with st.spinner("🧠 Tworzę Twój profil przywódczy..."):
                    leadership_profile = create_leadership_profile(conversations_text)
                    if leadership_profile:
                        st.session_state['leadership_profile'] = leadership_profile
                        
                        # Auto-zapis profilu dla zalogowanego użytkownika
                        if hasattr(st.session_state, 'username') and st.session_state.username:
                            profile_title = profile_name.strip() if (profile_name and profile_name.strip()) else None
                            if save_leadership_profile(st.session_state.username, leadership_profile, profile_title):
                                saved_name = profile_title or f"Profil {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                                st.success(f"✅ Profil '{saved_name}' gotowy i zapisany! Zobacz zakładkę 'Profil Przywódczy'")
                            else:
                                st.success("✅ Profil przywódczy gotowy! Zobacz zakładkę 'Profil Przywódczy'")
                                st.warning("⚠️ Nie udało się zapisać profilu do pliku")
                        else:
                            st.success("✅ Profil przywódczy gotowy! Zobacz zakładkę 'Profil Przywódczy'")
                            st.info("💡 Zaloguj się, aby automatycznie zapisywać swoje profile")
            else:
                st.warning("⚠️ Dodaj przynajmniej jeden fragment rozmowy do analizy")
    
    with tab2:
        # Sekcja zarządzania zapisanymi profilami
        if hasattr(st.session_state, 'username') and st.session_state.username:
            st.markdown("### 💾 Twoje zapisane profile")
            
            profiles_history = get_user_profiles_history(st.session_state.username)
            if profiles_history:
                st.markdown(f"**📊 Masz {len(profiles_history)} zapisanych profili:**")
                
                # Lista profili do wyboru
                for i, profile in enumerate(profiles_history):
                    col_info, col_actions = st.columns([3, 1])
                    
                    with col_info:
                        profile_name = profile.get('profile_name', f'Profil {i+1}')
                        profile_date = profile.get('created_at', 'Nieznana data')[:16].replace('T', ' ')
                        dominant_level = profile.get('dominant_ciq_level', '?')
                        
                        # Sprawdź czy to aktualnie wczytany profil
                        is_current = ('leadership_profile' in st.session_state and 
                                    st.session_state['leadership_profile'].get('created_at') == profile.get('created_at'))
                        
                        if is_current:
                            st.success(f"✅ **{profile_name}** (aktualnie wczytany)")
                        else:
                            st.info(f"📂 **{profile_name}**")
                        
                        st.caption(f"📅 {profile_date} | 🎯 Poziom dominujący: {dominant_level}")
                        
                    with col_actions:
                        if not is_current:
                            if zen_button("📥 Wczytaj", key=f"load_profile_{i}"):
                                st.session_state['leadership_profile'] = profile
                                st.success(f"✅ Wczytano profil: {profile_name}")
                                st.rerun()
                        
                        if zen_button("🗑️ Usuń", key=f"delete_profile_{i}"):
                            if delete_user_profile(st.session_state.username, i):
                                if is_current:
                                    del st.session_state['leadership_profile']
                                st.success(f"🗑️ Usunięto profil: {profile_name}")
                                st.rerun()
                    
                    st.markdown("---")
            else:
                st.info("📂 Nie masz jeszcze żadnych zapisanych profili")
                st.markdown("💡 Po stworzeniu pierwszego profilu zostanie automatycznie zapisany")
        else:
            st.info("💡 Zaloguj się, aby automatycznie zapisywać swoje profile")
            
        st.markdown("---")
        
        if 'leadership_profile' in st.session_state:
            # Przycisk eksportu PDF
            col_export, col_info = st.columns([1, 3])
            with col_export:
                if zen_button("📄 Eksportuj PDF", key="export_leadership_pdf"):
                    try:
                        username = getattr(st.session_state, 'username', 'Użytkownik')
                        pdf_data = generate_leadership_pdf(st.session_state['leadership_profile'], username)
                        
                        # Przygotuj nazwę pliku
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"raport_przywodczy_{username}_{timestamp}.pdf"
                        
                        st.download_button(
                            label="⬇️ Pobierz raport",
                            data=pdf_data,
                            file_name=filename,
                            mime="application/pdf",
                            key="download_pdf"
                        )
                        st.success("✅ Raport PDF gotowy do pobrania!")
                        
                    except Exception as e:
                        st.error(f"❌ Błąd podczas generowania PDF: {str(e)}")
            
            with col_info:
                st.info("💡 Eksport zawiera pełny raport przywódczy + plan rozwoju")
            
            st.markdown("---")
            
            display_leadership_profile(st.session_state['leadership_profile'])
        else:
            st.info("📊 Najpierw wgraj dane w zakładce 'Upload Danych'")
            
    with tab3:
        if 'leadership_profile' in st.session_state:
            display_leadership_development_plan(st.session_state['leadership_profile'])
        else:
            st.info("🎯 Profil przywódczy jest potrzebny do stworzenia planu rozwoju")

# ===============================================
# BUSINESS CONVERSATION SIMULATOR - TYMCZASOWO WYŁĄCZONY
# ===============================================
# Funkcje symulatora zostały tymczasowo wyłączone z powodu błędów parsowania.
# Pełna dokumentacja koncepcji w: docs/BUSINESS_SIMULATOR_CONCEPT.md
# Kod zostanie przepisany od nowa w osobnym module.
#
# Usunięte funkcje (linie 3690-4817):
# - generate_case_context()
# - get_fallback_context()
# - generate_initial_message()
# - get_fallback_initial_message()
# - generate_conversation_report()
# - generate_fallback_report()
# - generate_conversation_transcript()
# - show_conversation_report()
# - show_business_conversation_simulator() [GŁÓWNA FUNKCJA - 700+ linii]
# - analyze_ciq_level()
# - analyze_ciq_level_fallback()
# - generate_ai_response()
# ===============================================

def show_simulators():
    """Generuje konkretny kontekst case study dla scenariusza"""
    try:
        api_key = st.secrets.get("API_KEYS", {}).get("gemini")
        if not api_key:
            # Fallback - prosty kontekst bez AI
            return get_fallback_context(scenario)
        
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        try:
            model = genai.GenerativeModel(
                "gemini-2.0-flash-exp",
                generation_config=genai.GenerationConfig(
                    temperature=0.8,  # Średnia kreatywność
                    top_p=0.9,
                )
            )
        except:
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config=genai.GenerationConfig(
                    temperature=0.8,
                    top_p=0.9,
                )
            )
        
        response = model.generate_content(scenario['context_prompt'])
        return response.text.strip()
        
    except Exception as e:
        # W razie błędu użyj fallbacku
        return get_fallback_context(scenario)

def get_fallback_context(scenario):
    """Zwraca predefiniowany kontekst gdy AI nie działa"""
    fallback_contexts = {
        "salary_raise": "Jesteś Project Managerem w firmie IT. Pracujesz od 18 miesięcy bez podwyżki, a niedawno przejąłeś dodatkowe obowiązki po zwolnionym koledze. Słyszałeś, że firma ma dobry kwartał finansowy.",
        "difficult_feedback": "Marek pracuje jako Junior Developer. Ostatnio jego projekty są opóźnione o średnio 2 tygodnie, a kod wymaga wielu poprawek. Problem trwa od 3 miesięcy. Ma potencjał, ale wydaje się być przytłoczony zadaniami.",
        "team_conflict": "Konflikt między Anią (Senior Designer) a Tomkiem (Frontend Developer). Problem: Ania czuje że Tomek ignoruje jej wskazówki designerskie i samowolnie zmienia projekty. To trwa od 2 miesięcy i wpływa na jakość produktu. Twoja perspektywa (Ania): czujesz się lekceważona i sfrustrowana."
    }
    
    scenario_id = None
    for sid, sc in {"salary_raise": {}, "difficult_feedback": {}, "team_conflict": {}}.items():
        if scenario.get('name') == {"salary_raise": "💰 Rozmowa o podwyżkę", "difficult_feedback": "📢 Feedback dla pracownika", "team_conflict": "⚡ Rozwiązanie konfliktu"}.get(sid):
            scenario_id = sid
            break
    
    if scenario_id:
        return fallback_contexts.get(scenario_id, "Kontekst rozmowy biznesowej.")
    else:
        return "Kontekst rozmowy biznesowej."

def generate_initial_message(scenario, case_context):
    """Generuje pierwszą wiadomość AI uwzględniającą kontekst"""
    try:
        api_key = st.secrets.get("API_KEYS", {}).get("gemini")
        if not api_key:
            return get_fallback_initial_message(scenario)
        
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        try:
            model = genai.GenerativeModel(
                "gemini-2.0-flash-exp",
                generation_config=genai.GenerationConfig(temperature=0.7)
            )
        except:
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config=genai.GenerationConfig(temperature=0.7)
            )
        
        prompt = f"""Jesteś {scenario['ai_role']} w symulacji biznesowej.

KONTEKST SYTUACJI:
{case_context}

TWOJA POSTAĆ: {scenario['ai_persona']}

Wygeneruj pierwszą naturalną wypowiedź rozpoczynającą tę rozmowę. 
- 1-2 zdania
- Naturalny ton odpowiedni do roli
- Możesz nawiązać do kontekstu jeśli to naturalne

Tylko treść wypowiedzi, bez opisów:"""

        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception:
        return get_fallback_initial_message(scenario)

def get_fallback_initial_message(scenario):
    """Zwraca prostą pierwszą wiadomość jako fallback"""
    fallback_messages = {
        "Szef": "Dzień dobry. Słucham, o co chodzi? Mam tylko 10 minut.",
        "Pracownik": "Cześć! Co tam? Wszystko w porządku?",
        "Członek zespołu": "No dobra, to o co w końcu chodzi? I tak nikt mnie tu nie słucha..."
    }
    return fallback_messages.get(scenario.get('ai_role'), "Dzień dobry, słucham.")

def generate_conversation_report(messages, scenario, case_context):
    """Generuje końcowy raport z rozmowy używając AI"""
    try:
        api_key = st.secrets.get("API_KEYS", {}).get("gemini")
        if not api_key:
            return generate_fallback_report(messages)
        
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        try:
            model = genai.GenerativeModel(
                "gemini-2.0-flash-exp",
                generation_config=genai.GenerationConfig(temperature=0.3)
            )
        except:
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config=genai.GenerationConfig(temperature=0.3)
            )
        
        # Przygotuj historię rozmowy dla AI
        conversation_text = f"SCENARIUSZ: {scenario['name']}\nKONTEKST: {case_context}\n\nROZMOWA:\n"
        user_messages = []
        
        for msg in messages:
            if msg['role'] == 'user':
                ciq = msg.get('ciq_level', {})
                level = ciq.get('level', 'Brak analizy')
                conversation_text += f"\nUSER: {msg['content']} [C-IQ: {level}]\n"
                user_messages.append({
                    'content': msg['content'],
                    'ciq_level': level,
                    'is_appropriate': ciq.get('is_appropriate', False)
                })
            else:
                conversation_text += f"AI: {msg['content']}\n"
        
        # Liczenie statystyk
        total_turns = len([m for m in messages if m['role'] == 'user'])
        ciq_stats = {
            'Transformacyjny': 0,
            'Pozycyjny': 0,
            'Transakcyjny': 0
        }
        for msg in messages:
            if msg['role'] == 'user' and msg.get('ciq_level'):
                level = msg['ciq_level'].get('level', '')
                if level in ciq_stats:
                    ciq_stats[level] += 1
        
        prompt = f"""{conversation_text}

ZADANIE:
Oceń całą rozmowę i wygeneruj raport rozwojowy. Zwróć JSON:

{{
    "outcome": "Pozytywny|Częściowy|Negatywny",
    "outcome_reason": "1-2 zdania dlaczego taki wynik",
    "strengths": ["mocna strona 1 (konkret, nr wymiany)", "mocna strona 2"],
    "improvements": ["obszar rozwoju 1 (konkret, nr wymiany)", "obszar rozwoju 2"],
    "key_moment": "Najbardziej krytyczny moment rozmowy i dlaczego",
    "next_steps": "Co użytkownik powinien ćwiczyć dalej"
}}

KRYTERIA OCENY:
- Pozytywny: osiągnięto porozumienie, zbudowano rapport, konstruktywne rozwiązanie
- Częściowy: kompromis, nierozstrzygnięta kwestia, ale bez eskalacji
- Negatywny: konflikt, pat, przerwanie rozmowy, brak postępu

WAŻNE:
- Bądź konkretny: "wymiana 3" zamiast "na początku"
- Doceniaj użycie Transformacyjnego C-IQ
- Zwróć uwagę na progression - czy poziom C-IQ się poprawiał?
- Max 15 słów na punkt

TYLKO JSON:"""

        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Wyczyść JSON
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        import json
        report = json.loads(result_text)
        
        # Dodaj statystyki
        report['total_turns'] = total_turns
        report['ciq_stats'] = ciq_stats
        
        return report
        
    except Exception as e:
        return generate_fallback_report(messages)

def generate_fallback_report(messages):
    """Prosty raport gdy AI nie działa"""
    total_turns = len([m for m in messages if m['role'] == 'user'])
    ciq_stats = {
        'Transformacyjny': 0,
        'Pozycyjny': 0,
        'Transakcyjny': 0
    }
    for msg in messages:
        if msg['role'] == 'user' and msg.get('ciq_level'):
            level = msg['ciq_level'].get('level', '')
            if level in ciq_stats:
                ciq_stats[level] += 1
    
    return {
        'outcome': 'Częściowy',
        'outcome_reason': 'Rozmowa została zakończona.',
        'strengths': ['Ukończyłeś scenariusz', 'Przećwiczyłeś komunikację C-IQ'],
        'improvements': ['Spróbuj więcej pytań otwartych', 'Buduj na odpowiedziach rozmówcy'],
        'key_moment': 'Cała rozmowa była ćwiczeniem umiejętności.',
        'next_steps': 'Spróbuj innego scenariusza i zwróć uwagę na poziomy C-IQ.',
        'total_turns': total_turns,
        'ciq_stats': ciq_stats
    }

def generate_conversation_transcript(messages, scenario):
    """Generuje transkrypcję rozmowy w formacie tekstowym"""
    transcript_lines = []
    transcript_lines.append("=" * 60)
    transcript_lines.append("TRANSKRYPCJA ROZMOWY")
    transcript_lines.append("=" * 60)
    transcript_lines.append(f"Scenariusz: {scenario['name']}")
    transcript_lines.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    transcript_lines.append("=" * 60)
    transcript_lines.append("")
    
    # Kontekst case study
    case_context = st.session_state.get('simulator_case_context', '')
    if case_context:
        transcript_lines.append("KONTEKST:")
        transcript_lines.append(case_context)
        transcript_lines.append("")
        transcript_lines.append("-" * 60)
        transcript_lines.append("")
    
    # Historia rozmowy z analizą C-IQ
    exchange_num = 0
    for i, msg in enumerate(messages):
        if msg['role'] == 'user':
            exchange_num += 1
            transcript_lines.append(f"[Wymiana {exchange_num}]")
            transcript_lines.append("")
            
        if msg['role'] == 'ai':
            transcript_lines.append(f"{scenario.get('ai_role', 'AI').upper()}:")
            transcript_lines.append(msg['content'])
            transcript_lines.append("")
        else:
            transcript_lines.append(f"{scenario.get('user_role', 'TY').upper()}:")
            transcript_lines.append(msg['content'])
            
            # Dodaj analizę C-IQ
            if msg.get('ciq_level'):
                ciq = msg['ciq_level']
                level = ciq.get('level', 'Brak')
                is_appropriate = ciq.get('is_appropriate', None)
                
                appropriate_text = ""
                if is_appropriate is not None:
                    appropriate_text = " ✓ (odpowiedni w kontekście)" if is_appropriate else " ⚠ (nieodpowiedni)"
                
                transcript_lines.append(f"   └─ C-IQ: {level}{appropriate_text}")
                
                # Opcjonalnie dodaj feedback
                feedback = ciq.get('feedback', '')
                if feedback:
                    # Skróć feedback do 100 znaków
                    short_feedback = feedback[:100] + "..." if len(feedback) > 100 else feedback
                    transcript_lines.append(f"   └─ {short_feedback}")
            
            transcript_lines.append("")
            transcript_lines.append("-" * 60)
            transcript_lines.append("")
    
    transcript_lines.append("=" * 60)
    transcript_lines.append("KONIEC TRANSKRYPCJI")
    transcript_lines.append("=" * 60)
    
    return "\n".join(transcript_lines)

def show_conversation_report(report, scenario):
    """Wyświetla końcowy raport z rozmowy"""
    st.markdown("---")
    st.markdown("## 📊 PODSUMOWANIE ROZMOWY")
    st.markdown("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # Wynik rozmowy z emoji
    outcome_emoji = {
        'Pozytywny': '✅',
        'Częściowy': '🤝',
        'Negatywny': '❌'
    }
    outcome = report.get('outcome', 'Częściowy')
    emoji = outcome_emoji.get(outcome, '🤝')
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"### {emoji} Wynik")
        outcome_color = {
            'Pozytywny': 'green',
            'Częściowy': 'orange',
            'Negatywny': 'red'
        }
        color = outcome_color.get(outcome, 'blue')
        if color == 'green':
            st.success(f"**{outcome}**")
        elif color == 'orange':
            st.warning(f"**{outcome}**")
        else:
            st.error(f"**{outcome}**")
    with col2:
        st.markdown("### 📝 Dlaczego?")
        st.info(report.get('outcome_reason', 'Brak opisu'))
    
    # Statystyki
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⏱️ Wymian", report.get('total_turns', 0))
    
    ciq_stats = report.get('ciq_stats', {})
    with col2:
        st.metric("🟢 Transformacyjny", ciq_stats.get('Transformacyjny', 0))
    with col3:
        st.metric("🟠 Pozycyjny", ciq_stats.get('Pozycyjny', 0))
    with col4:
        st.metric("🔴 Transakcyjny", ciq_stats.get('Transakcyjny', 0))
    
    # Mocne strony
    st.markdown("---")
    st.markdown("### 💪 Twoje mocne strony")
    strengths = report.get('strengths', [])
    if strengths:
        for strength in strengths:
            st.success(f"✓ {strength}")
    else:
        st.info("Brak szczegółów")
    
    # Obszary rozwoju
    st.markdown("### 🎓 Obszary do rozwoju")
    improvements = report.get('improvements', [])
    if improvements:
        for improvement in improvements:
            st.warning(f"→ {improvement}")
    else:
        st.info("Brak szczegółów")
    
    # Kluczowy moment
    st.markdown("---")
    st.markdown("### 🔑 Kluczowy moment rozmowy")
    st.info(report.get('key_moment', 'Brak analizy'))
    
    # Następne kroki
    st.markdown("### 🌟 Co dalej?")
    st.success(report.get('next_steps', 'Kontynuuj ćwiczenia z innymi scenariuszami'))
    
    st.markdown("---")
    
    # TRANSKRYPCJA ROZMOWY
    st.markdown("### 📜 Transkrypcja rozmowy")
    st.caption("Pełny zapis Twojej rozmowy z analizą poziomów C-IQ")
    
    # Generuj transkrypcję
    messages = st.session_state.get('simulator_messages', [])
    transcript = generate_conversation_transcript(messages, scenario)
    
    # Wyświetl w expander (domyślnie zwinięty)
    with st.expander("🔍 Zobacz pełną transkrypcję", expanded=False):
        st.text(transcript)
        
        # Przycisk do pobrania
        st.download_button(
            label="💾 Pobierz transkrypcję (.txt)",
            data=transcript,
            file_name=f"transkrypcja_{scenario['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            help="Zapisz transkrypcję na swoim komputerze"
        )
    
    st.markdown("---")

def show_business_conversation_simulator():
    """Symulator rozmów biznesowych z analizą C-IQ"""
    st.markdown("### 💼 Symulator Rozmów Biznesowych")
    
    # DIAGNOSTYKA - ZAWSZE WIDOCZNA
    try:
        api_key = st.secrets.get("API_KEYS", {}).get("gemini")
        if api_key:
            st.success(f"✅ API OK - Klucz znaleziony ({len(api_key)} znaków) - Używam prawdziwego AI")
        else:
            st.error("❌ BRAK KLUCZA API - Dodaj 'gemini' do secrets w [API_KEYS]")
            st.warning("⚠️ Używam prostych odpowiedzi fallback zamiast AI")
    except Exception as e:
        st.error(f"❌ BŁĄD SECRETS: {type(e).__name__}: {str(e)}")
        st.warning("⚠️ Nie mogę odczytać konfiguracji - używam fallback")
    
    st.markdown("---")
    
    # Inicjalizacja session state
    if 'simulator_scenario' not in st.session_state:
        st.session_state.simulator_scenario = None
    if 'simulator_messages' not in st.session_state:
        st.session_state.simulator_messages = []
    if 'simulator_started' not in st.session_state:
        st.session_state.simulator_started = False
    if 'simulator_case_context' not in st.session_state:
        st.session_state.simulator_case_context = None
    if 'simulator_max_turns' not in st.session_state:
        st.session_state.simulator_max_turns = 10  # Maksymalnie 10 wymian (20 wiadomości)
    if 'simulator_completed' not in st.session_state:
        st.session_state.simulator_completed = False
    if 'simulator_final_report' not in st.session_state:
        st.session_state.simulator_final_report = None
    
    # Definicja scenariuszy z promptami do generowania kontekstu
    scenarios = {
        "salary_raise": {
            "name": "💰 Rozmowa o podwyżkę",
            "description": "Prosisz szefa o podwyżkę. Twój szef jest wymagający i skupiony na wynikach.",
            "ai_persona": "Jesteś wymagającym dyrektorem firmy. Cenisz konkretne wyniki i liczby. Jesteś sceptyczny wobec próśb o podwyżkę, chyba że rozmówca przedstawi mocne argumenty biznesowe. Nie jesteś wrogi, ale wymagasz przekonujących dowodów wartości pracownika.",
            "ai_role": "Szef",
            "user_role": "Pracownik",
            "context_prompt": """Wygeneruj krótki (3-4 zdania), konkretny kontekst biznesowy dla rozmowy pracownik-szef o podwyżkę:
- Nazwa stanowiska pracownika
- Branża/firma
- Dlaczego pracownik chce podwyżki (np. rok bez podwyżki, nowe obowiązki, oferta z innej firmy)
- Dodatkowy szczegół zwiększający trudność (np. firma ma trudności finansowe, ostatnio było zwolnienie kogoś)

Odpowiedz TYLKO kontekstem, bez dodatków. Format: "Jesteś [stanowisko] w [firma/branża]. [sytuacja]. [wyzwanie]."
"""
        },
        "difficult_feedback": {
            "name": "📢 Feedback dla pracownika",
            "description": "Musisz przekazać trudny feedback pracownikowi, który nie spełnia oczekiwań.",
            "ai_persona": "Jesteś pracownikiem, który nie zdaje sobie sprawy z problemów w swojej pracy. Początkowo możesz być defensywny, ale jeśli rozmówca użyje empatii i konkretów (poziom Transformacyjny C-IQ), stajesz się otwarty na feedback.",
            "ai_role": "Pracownik",
            "user_role": "Menedżer",
            "context_prompt": """Wygeneruj krótki (3-4 zdania), konkretny kontekst dla trudnej rozmowy feedbackowej:
- Imię pracownika i stanowisko
- Konkretny problem z wydajnością (np. spóźnione projekty, konflikty w zespole, błędy w pracy)
- Jak długo problem trwa
- Dodatkowy kontekst (np. pracownik ma potencjał ale ostatnio się pogubił, albo nie przyjmuje feedbacku)

Odpowiedz TYLKO kontekstem. Format: "[Imię] pracuje jako [stanowisko]. Problem: [konkret]. [dodatkowy szczegół]."
"""
        },
        "team_conflict": {
            "name": "⚡ Rozwiązanie konfliktu",
            "description": "Dwóch członków zespołu ma konflikt. Musisz pomóc im się porozumieć.",
            "ai_persona": "Jesteś sfrustrowanym członkiem zespołu, który czuje się niedoceniony. Jesteś lekko agresywny i obwiniasz innych. Możesz się uspokoić tylko jeśli rozmówca wykaże empatię i pomoże znaleźć wspólne rozwiązanie (C-IQ Transformacyjny).",
            "ai_role": "Członek zespołu",
            "user_role": "Mediator",
            "context_prompt": """Wygeneruj krótki (3-4 zdania), konkretny kontekst konfliktu zespołowego:
- Imiona dwóch skonfliktowanych osób i ich role
- O co dokładnie chodzi w konflikcie (np. podział zadań, różne style pracy, nieporozumienie)
- Jak długo to trwa i jaki ma wpływ na zespół
- Perspektywa osoby z którą rozmawiasz (czuje się niedoceniona/wykorzystana)

Odpowiedz TYLKO kontekstem. Format: "Konflikt między [osoba1] a [osoba2]. Problem: [konkret]. Twoja perspektywa: [uczucia]."
"""
        },
        "delegation": {
            "name": "📋 Delegowanie zadania",
            "description": "Delegujesz ważne zadanie pracownikowi, który ma już duże obciążenie pracą.",
            "ai_persona": "Jesteś przeciążonym pracownikiem, który ma już pełne ręce roboty. Czujesz się zmęczony i obawiasz się, że kolejne zadanie Cię przytłoczy. Jesteś otwarty na rozmowę, ale potrzebujesz wsparcia i jasnych priorytetów.",
            "ai_role": "Pracownik",
            "user_role": "Menedżer",
            "context_prompt": """Wygeneruj krótki (3-4 zdania), konkretny kontekst delegowania zadania:
- Imię pracownika i jego stanowisko
- Jakie zadanie chcesz delegować i dlaczego jest ważne
- Obecne obciążenie pracownika (np. 3 projekty równocześnie, deadline za tydzień)
- Dodatkowy szczegół (np. brak innej osoby do zadania, klient czeka)

Odpowiedz TYLKO kontekstem. Format: "Chcesz delegować [zadanie] do [imię]. Obecna sytuacja: [obciążenie]. [wyzwanie]."
"""
        },
        "motivation": {
            "name": "🔥 Motywowanie zdemotywowanego",
            "description": "Pracownik stracił motywację i rozważa zmianę pracy. Musisz go zmotywować.",
            "ai_persona": "Jesteś zdemotywowanym pracownikiem, który czuje się wypalony i niedoceniany. Praca przestała Cię inspirować. Jesteś otwarty na rozmowę, ale potrzebujesz szczerości, zrozumienia i konkretnych zmian, nie pustych obietnic.",
            "ai_role": "Pracownik",
            "user_role": "Menedżer",
            "context_prompt": """Wygeneruj krótki (3-4 zdania), konkretny kontekst rozmowy motywacyjnej:
- Imię pracownika i stanowisko
- Dlaczego stracił motywację (np. rutyna, brak rozwoju, nieudane projekty)
- Jak długo to trwa i jakie są objawy (np. gorsze wyniki, brak zaangażowania)
- Dodatkowy kontekst (np. dostał ofertę z innej firmy, jest wartościowym pracownikiem)

Odpowiedz TYLKO kontekstem. Format: "[Imię] jest [stanowisko]. Problem: [demotywacja]. [sygnały i sytuacja]."
"""
        },
        "change_resistance": {
            "name": "🔄 Opór wobec zmian",
            "description": "Przekonujesz zespół do dużej zmiany organizacyjnej, na którą są opory.",
            "ai_persona": "Jesteś sceptycznym członkiem zespołu, który obawia się zmian. Masz doświadczenie z nieudanymi zmianami w przeszłości. Jesteś ostrożny i potrzebujesz przekonujących argumentów oraz poczucia bezpieczeństwa.",
            "ai_role": "Członek zespołu",
            "user_role": "Lider zmiany",
            "context_prompt": """Wygeneruj krótki (3-4 zdania), konkretny kontekst wprowadzania zmiany:
- Jaka zmiana jest wprowadzana (np. nowy system, restrukturyzacja, nowa metodologia)
- Dlaczego zespół się obawia (np. poprzednie złe doświadczenia, niepewność)
- Jakie są realne obawy (np. więcej pracy, utrata kontroli, zwolnienia)
- Twoja perspektywa jako członka zespołu

Odpowiedz TYLKO kontekstem. Format: "Firma wprowadza [zmiana]. Twoje obawy: [konkret]. [dodatkowy kontekst]."
"""
        },
        "difficult_client": {
            "name": "😤 Rozmowa z trudnym klientem",
            "description": "Klient jest niezadowolony z realizacji projektu i grozi rezygnacją.",
            "ai_persona": "Jesteś sfrustrowanym klientem, który czuje że jego projekt jest zaniedbywany. Jesteś niezadowolony z komunikacji i wyników. Możesz być oschły i wymagający, ale jeśli zobaczysz autentyczną chęć rozwiązania problemu, stajesz się bardziej otwarty.",
            "ai_role": "Klient",
            "user_role": "Account Manager",
            "context_prompt": """Wygeneruj krótki (3-4 zdania), konkretny kontekst rozmowy z trudnym klientem:
- Nazwa klienta/firmy i branża
- Co poszło nie tak w projekcie (np. opóźnienie, błędy, zła komunikacja)
- Jak poważna jest sytuacja (np. klient grozi odejściem, złe recenzje)
- Dodatkowy kontekst (np. duży kontrakt, prestiżowy klient)

Odpowiedz TYLKO kontekstem. Format: "Klient [nazwa] z branży [branża]. Problem: [konkret]. Sytuacja: [powaga]."
"""
        },
        "negotiation": {
            "name": "💼 Negocjacje warunków",
            "description": "Negocjujesz warunki współpracy z wymagającym partnerem biznesowym.",
            "ai_persona": "Jesteś twardym negocjatorem, który zna swoją wartość. Chcesz najlepszych warunków i nie boisz się odejść, jeśli oferta nie jest satysfakcjonująca. Szanujesz profesjonalizm i konkretne argumenty biznesowe.",
            "ai_role": "Partner biznesowy",
            "user_role": "Negocjator",
            "context_prompt": """Wygeneruj krótki (3-4 zdania), konkretny kontekst negocjacji biznesowych:
- Kim jest partner (firma, branża, skala działalności)
- Co jest przedmiotem negocjacji (np. cena, terminy, zakres współpracy)
- Jakie są kluczowe punkty sporne (np. budżet, harmonogram, warunki płatności)
- Dodatkowy kontekst (np. partner ma alternatywne oferty, presja czasowa)

Odpowiedz TYLKO kontekstem. Format: "Negocjujesz z [partner] ws. [przedmiot]. Punkt sporny: [konkret]. [sytuacja]."
"""
        }
    }
    
    # Wybór scenariusza - NOWA KONSTRUKCJA Z SELECTBOX
    if not st.session_state.simulator_started:
        st.markdown("### 🎯 Wybierz scenariusz rozmowy:")
        
        # Przygotuj opcje dla selectbox
        scenario_options = {scenario['name']: scenario_id for scenario_id, scenario in scenarios.items()}
        
        # Selectbox z opisem wybranego scenariusza
        selected_name = st.selectbox(
            "Scenariusz:",
            options=list(scenario_options.keys()),
            key="scenario_selector",
            help="Wybierz typ rozmowy biznesowej, którą chcesz przećwiczyć"
        )
        
        # Pobierz wybrany scenariusz
        selected_id = scenario_options[selected_name]
        selected_scenario = scenarios[selected_id]
        
        # Wyświetl szczegóły wybranego scenariusza
        st.markdown("---")
        with st.container():
            st.markdown(f"#### {selected_scenario['name']}")
            st.info(f"📋 **Scenariusz:** {selected_scenario['description']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Twoja rola:** {selected_scenario['user_role']}")
            with col2:
                st.markdown(f"**Rozmówca:** {selected_scenario['ai_role']}")
            
            st.markdown("")
            if st.button("▶️ Rozpocznij symulację", type="primary", use_container_width=True, key=f"start_{selected_id}"):
                st.session_state.simulator_scenario = selected_id
                st.session_state.simulator_started = True
                st.session_state.simulator_waiting_for_next = False  # Reset flagi
                
                # Zaloguj rozpoczęcie symulatora i przyznaj XP
                try:
                    from data.users import award_xp_for_activity
                    award_xp_for_activity(
                        st.session_state.username,
                        'tool_used',
                        1,  # 1 XP za użycie narzędzia
                        {
                            'tool_name': 'Business Conversation Simulator',
                            'scenario': selected_id,
                            'scenario_name': selected_scenario['name']
                        }
                    )
                except Exception:
                    pass
                
                # Generuj kontekst case study
                with st.spinner("🎬 Generuję kontekst scenariusza..."):
                    case_context = generate_case_context(selected_scenario)
                    st.session_state.simulator_case_context = case_context
                    
                    # Wygeneruj pierwszą wiadomość AI z kontekstem
                    initial_message = generate_initial_message(selected_scenario, case_context)
                    st.session_state.simulator_messages = [
                        {"role": "ai", "content": initial_message, "ciq_level": None}
                    ]
                
                st.rerun()
        
        # Instrukcja
        st.markdown("---")
        st.markdown("#### 📚 Poziomy C-IQ (Conversational Intelligence):")
        
        ciq_col1, ciq_col2, ciq_col3 = st.columns(3)
        
        with ciq_col1:
            st.markdown("""
            **🔴 Transakcyjny**
            - Wymiana informacji
            - "Ty mówisz - ja słucham"
            - Brak głębszego dialogu
            - Przykład: _"Chcę podwyżki o 20%"_
            """)
        
        with ciq_col2:
            st.markdown("""
            **🟡 Pozycyjny**
            - Obrona swojej pozycji
            - Walka o rację
            - "Ja vs. Ty"
            - Przykład: _"Zasługuję na więcej, bo inni zarabiają więcej"_
            """)
        
        with ciq_col3:
            st.markdown("""
            **🟢 Transformacyjny**
            - Współtworzenie rozwiązań
            - Empatia i zrozumienie
            - "My razem"
            - Przykład: _"Jak możemy wspólnie znaleźć rozwiązanie?"_
            """)
        
        return
    
    # Aktywna symulacja
    scenario_id = st.session_state.simulator_scenario
    if not scenario_id:
        return
    scenario = scenarios[scenario_id]
    
    # SPRAWDŹ CZY ROZMOWA ZAKOŃCZONA - jeśli tak, pokaż raport
    if st.session_state.simulator_completed and st.session_state.simulator_final_report:
        show_conversation_report(st.session_state.simulator_final_report, scenario)
        
        # Przyciski: nowy scenariusz lub zamknij
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 Spróbuj innego scenariusza", type="primary", use_container_width=True):
                st.session_state.simulator_started = False
                st.session_state.simulator_messages = []
                st.session_state.simulator_scenario = None
                st.session_state.simulator_case_context = None
                st.session_state.simulator_waiting_for_next = False
                st.session_state.simulator_completed = False
                st.session_state.simulator_final_report = None
                st.rerun()
        with col2:
            if st.button("❌ Zamknij", use_container_width=True):
                st.session_state.active_simulator = None
                st.session_state.simulator_started = False
                st.session_state.simulator_messages = []
                st.session_state.simulator_scenario = None
                st.session_state.simulator_case_context = None
                st.session_state.simulator_waiting_for_next = False
                st.session_state.simulator_completed = False
                st.session_state.simulator_final_report = None
                st.rerun()
        
        return  # Zakończ funkcję - nie pokazuj reszty interfejsu
    
    # Oblicz liczbę wymian (tylko wiadomości użytkownika)
    user_turns = len([m for m in st.session_state.simulator_messages if m['role'] == 'user'])
    max_turns = st.session_state.simulator_max_turns
    
    # Nagłówek z nazwą scenariusza i licznikiem
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"#### {scenario['name']}")
        st.caption(scenario['description'])
    with col2:
        # Licznik wymian
        progress = user_turns / max_turns
        if progress < 0.6:
            color = "�"
        elif progress < 0.8:
            color = "🟡"
        else:
            color = "🔴"
        st.metric("Wymiana", f"{color} {user_turns}/{max_turns}")
    with col3:
        # Przycisk zakończenia
        if st.button("🏁 Zakończ", help="Zakończ rozmowę i zobacz raport"):
            # Generuj raport
            with st.spinner("📊 Generuję raport..."):
                report = generate_conversation_report(
                    st.session_state.simulator_messages,
                    scenario,
                    st.session_state.simulator_case_context
                )
                st.session_state.simulator_final_report = report
                st.session_state.simulator_completed = True
                
                # Zaloguj ukończenie ćwiczenia AI i przyznaj XP
                try:
                    from data.users import award_xp_for_activity
                    award_xp_for_activity(
                        st.session_state.username,
                        'ai_exercise',
                        15,  # 15 XP za ukończenie ćwiczenia AI
                        {
                            'exercise_name': 'Business Conversation Simulator',
                            'scenario': st.session_state.simulator_scenario,
                            'turns': len(st.session_state.simulator_messages) // 2,
                            'completed': True
                        }
                    )
                except Exception:
                    pass
            st.rerun()
    
    # Wyświetl kontekst case study
    if st.session_state.simulator_case_context:
        with st.expander("📋 Kontekst scenariusza", expanded=False):
            st.info(st.session_state.simulator_case_context)
    
    st.markdown("---")
    
    # Wyświetl historię rozmowy
    for idx, msg in enumerate(st.session_state.simulator_messages):
        if msg['role'] == 'ai':
            with st.chat_message("assistant", avatar="💼"):
                st.markdown(msg['content'])
        else:
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg['content'])
                if msg.get('ciq_level'):
                    # Wyświetl analizę C-IQ z odpowiednim kolorem
                    level_info = msg['ciq_level']
                    color = level_info.get('color', 'blue')
                    is_appropriate = level_info.get('is_appropriate', None)
                    
                    # Wybierz funkcję Streamlit bazując na kolorze i kontekście
                    feedback_text = f"📊 **C-IQ: {level_info['level']}** - {level_info['feedback']}"
                    
                    if color == 'green':
                        st.success(feedback_text)
                    elif color == 'blue':
                        # Niebieski = odpowiedni w kontekście
                        st.info(feedback_text)
                    elif color == 'orange':
                        st.warning(feedback_text)
                    else:  # red
                        st.error(feedback_text) if not is_appropriate else st.info(feedback_text)
                    
                    # Jeśli to ostatnia wiadomość użytkownika, pokaż przyciski akcji
                    # Sprawdź czy następna wiadomość to odpowiedź AI (wtedy możemy "powtórzyć")
                    is_last_user_msg = (idx == len(st.session_state.simulator_messages) - 2 
                                       and idx + 1 < len(st.session_state.simulator_messages)
                                       and st.session_state.simulator_messages[idx + 1]['role'] == 'ai')
                    
                    if is_last_user_msg and not st.session_state.get('simulator_waiting_for_next', False):
                        col1, col2, col3 = st.columns([1, 1, 3])
                        with col1:
                            if st.button("🔄 Powtórz", key=f"retry_{idx}", help="Usuń tę wypowiedź i spróbuj ponownie"):
                                # Usuń ostatnią parę wiadomości (user + AI)
                                st.session_state.simulator_messages = st.session_state.simulator_messages[:-2]
                                st.rerun()
                        with col2:
                            if st.button("✅ Dalej", key=f"continue_{idx}", help="Kontynuuj konwersację"):
                                # Oznacz że użytkownik zaakceptował i chce iść dalej
                                st.session_state.simulator_waiting_for_next = True
                                st.rerun()
    
    # Input użytkownika - dostępny tylko gdy:
    # 1. To początek rozmowy (brak wiadomości)
    # 2. Ostatnia wiadomość to AI (user odpowiedział na feedback i kliknął "Dalej")
    # 3. User kliknął "Dalej" (flaga simulator_waiting_for_next)
    can_send_message = (
        len(st.session_state.simulator_messages) == 0 or  # Początek
        st.session_state.simulator_messages[-1]['role'] == 'ai' or  # Ostatnia to AI
        st.session_state.get('simulator_waiting_for_next', False)  # User kliknął "Dalej"
    )
    
    if can_send_message:
        # Reset flagi
        if st.session_state.get('simulator_waiting_for_next'):
            st.session_state.simulator_waiting_for_next = False
        
        user_input = st.chat_input("Twoja odpowiedź...")
        
        if user_input:
            # Sprawdź czy to będzie ostatnia wymiana (osiągnięcie limitu)
            user_turns = len([m for m in st.session_state.simulator_messages if m['role'] == 'user'])
            will_reach_limit = (user_turns + 1) >= st.session_state.simulator_max_turns
            
            # Analiza C-IQ przed dodaniem do historii
            ciq_analysis = analyze_ciq_level(user_input)
            
            # Generuj odpowiedź AI (PRZED dodaniem wiadomości użytkownika do historii)
            ai_response = generate_ai_response(
                user_input, 
                st.session_state.simulator_messages,  # Historia BEZ obecnej wiadomości
                scenario,
                ciq_analysis
            )
            
            # Teraz dodaj wiadomość użytkownika
            user_message = {"role": "user", "content": user_input, "ciq_level": ciq_analysis}
            st.session_state.simulator_messages.append(user_message)
            
            # Dodaj odpowiedź AI
            st.session_state.simulator_messages.append({
                "role": "ai", 
                "content": ai_response,
                "ciq_level": None
            })
            
            # Jeśli osiągnięto limit, automatycznie zakończ i generuj raport
            if will_reach_limit:
                with st.spinner("🏁 Osiągnięto limit wymian. Generuję raport..."):
                    report = generate_conversation_report(
                        st.session_state.simulator_messages,
                        scenario,
                        st.session_state.simulator_case_context
                    )
                    st.session_state.simulator_final_report = report
                    st.session_state.simulator_completed = True
            
            st.rerun()
    else:
        # Użytkownik musi przeczytać feedback i wybrać akcję
        st.info("💡 **Przeczytaj feedback powyżej i wybierz:**\n- 🔄 **Powtórz** - spróbuj przeformułować swoją odpowiedź\n- ✅ **Dalej** - kontynuuj konwersację")

def analyze_ciq_level(user_message):
    """Analizuje poziom C-IQ w wiadomości użytkownika za pomocą AI"""
    
    # Sprawdź czy API jest dostępne
    try:
        api_key = st.secrets.get("API_KEYS", {}).get("gemini")
        if not api_key:
            return analyze_ciq_level_fallback(user_message)
        
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        try:
            model = genai.GenerativeModel(
                "gemini-2.0-flash-exp",
                generation_config=genai.GenerationConfig(
                    temperature=0.3,  # Niska temperatura dla konsystentnej analizy
                )
            )
        except:
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config=genai.GenerationConfig(temperature=0.3)
            )
        
        # Pobierz kontekst rozmowy i historię
        conversation_history = st.session_state.get('simulator_messages', [])
        case_context = st.session_state.get('simulator_case_context', '')
        
        # Zbuduj kontekst ostatnich wymian
        recent_context = "\n".join([
            f"{'AI' if msg['role'] == 'ai' else 'Ty'}: {msg['content']}" 
            for msg in conversation_history[-4:]  # Ostatnie 2 wymiany
        ]) if conversation_history else "Początek rozmowy"
        
        prompt = f"""Przeanalizuj tę wypowiedź pod kątem Conversational Intelligence (C-IQ) w kontekście trwającej rozmowy:

KONTEKST SYTUACJI:
{case_context if case_context else 'Rozmowa biznesowa'}

OSTATNIE WYPOWIEDZI:
{recent_context}

AKTUALNA WYPOWIEDŹ: "{user_message}"

POZIOMY C-IQ:
🔴 **Transakcyjny** - wymiana informacji, pytania o fakty, jasne komunikaty ("co/kiedy/ile")
   → Odpowiedni gdy: ustalamy fakty, planujemy działania, wymieniamy dane
   → Nieodpowiedni gdy: sytuacja wymaga empatii, rozwiązania konfliktu, budowania relacji

🟡 **Pozycyjny** - obrona stanowiska, argumentowanie, "ja vs ty" ("zasługuję/powinienem")
   → Czasem potrzebny gdy: musimy być asertywni, bronić granic
   → Problematyczny gdy: eskaluje konflikt, niszczy zaufanie

🟢 **Transformacyjny** - współtworzenie, empatia, "my/razem" ("jak możemy/co myślisz")
   → Najlepszy gdy: trudne rozmowy, budowanie relacji, rozwiązywanie problemów
   → Rzadko nieodpowiedni (może być postrzegany jako "za miękki" w niektórych kulturach)

Oceń:
1. Jaki to poziom?
2. Czy jest odpowiedni do KONTEKSTU rozmowy?
3. Jak można poprawić (jeśli warto)?

Odpowiedz w formacie JSON:
{{
    "level": "Transakcyjny|Pozycyjny|Transformacyjny",
    "is_appropriate": true/false,
    "reasoning": "Dlaczego to ten poziom i czy jest OK w tym kontekście",
    "tip": "Wskazówka - jeśli poziom odpowiedni: 'Dobry wybór! ...' lub 'OK w tym momencie, ale...' / jeśli nieodpowiedni: 'Spróbuj...' "
}}

TYLKO JSON:"""

        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Wyczyść JSON z markdown
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        import json
        result = json.loads(result_text)
        
        # Mapuj kolor bazując na poziomie I czy jest odpowiedni
        is_appropriate = result.get("is_appropriate", False)
        level = result["level"]
        
        # Logika kolorów:
        # - Transformacyjny: zawsze zielony (prawie zawsze dobry)
        # - Transakcyjny/Pozycyjny: niebieski jeśli odpowiedni, czerwony/pomarańczowy jeśli nie
        if level == "Transformacyjny":
            color = "green"
        elif is_appropriate:
            color = "blue"  # Niebieski = OK w tym kontekście
        else:
            # Standardowe kolory ostrzegawcze
            color = "red" if level == "Transakcyjny" else "orange"
        
        return {
            "level": result["level"],
            "feedback": f"{result['reasoning']} 💡 {result['tip']}",
            "color": color,
            "is_appropriate": is_appropriate
        }
        
    except Exception as e:
        # Fallback na prostą heurystykę
        return analyze_ciq_level_fallback(user_message)

def analyze_ciq_level_fallback(user_message):
    """Prosta heurystyka analizy C-IQ gdy AI nie działa"""
    user_message_lower = user_message.lower()
    
    # Słowa kluczowe dla każdego poziomu
    transformational_keywords = [
        'razem', 'wspólnie', 'jak możemy', 'zrozumiem', 'pomóż mi zrozumieć',
        'jakie masz', 'co myślisz', 'współpraca', 'oboje', 'nasz cel',
        'słucham', 'rozumiem', 'doceniam', 'cenię'
    ]
    
    positional_keywords = [
        'ale', 'jednak', 'zasługuję', 'powinienem', 'musisz', 'masz obowiązek',
        'to niesprawiedliwe', 'inni mają', 'dlaczego ja nie', 'to twoja wina'
    ]
    
    transactional_keywords = [
        'chcę', 'potrzebuję', 'daj mi', 'kiedy', 'ile', 'co dostanę'
    ]
    
    # Analiza obecności słów kluczowych
    transformational_score = sum(1 for keyword in transformational_keywords if keyword in user_message_lower)
    positional_score = sum(1 for keyword in positional_keywords if keyword in user_message_lower)
    transactional_score = sum(1 for keyword in transactional_keywords if keyword in user_message_lower)
    
    # Dodatkowe wskaźniki
    has_question = '?' in user_message
    has_we_language = any(word in user_message_lower for word in ['my', 'nam', 'nasz', 'wspólnie', 'razem'])
    has_i_focus = any(word in user_message_lower.split()[:3] for word in ['ja', 'chcę', 'potrzebuję', 'muszę'])
    
    # Określ poziom
    if transformational_score >= 2 or (has_question and has_we_language):
        return {
            "level": "Transformacyjny",
            "feedback": "Świetnie! Budujesz współpracę i pokazujesz empatię. To buduje zaufanie.",
            "color": "green"
        }
    elif positional_score >= 2 or (has_i_focus and positional_score >= 1):
        return {
            "level": "Pozycyjny",
            "feedback": "Bronisz swojej pozycji. 💡 Spróbuj skupić się na wspólnych celach zamiast 'ja vs. ty'.",
            "color": "orange"
        }
    else:
        return {
            "level": "Transakcyjny",
            "feedback": "Wymieniasz informacje. 💡 Możesz pogłębić rozmowę pytając o perspektywę drugiej strony.",
            "color": "red"
        }

def generate_ai_response(user_input, conversation_history, scenario, ciq_analysis):
    """Generuje odpowiedź AI na podstawie kontekstu rozmowy"""
    
    # Sprawdź czy API jest dostępne (BEZ wyświetlania komunikatów w UI)
    try:
        api_key = st.secrets.get("API_KEYS", {}).get("gemini")
    except Exception:
        api_key = None
    
    if not api_key:
        # Fallback na prostą odpowiedź bez AI
        if ciq_analysis['level'] == 'Transformacyjny':
            return "Doceniam twoje podejście. Zgadzam się, że warto to omówić szczegółowo. Co proponujesz?"
        elif ciq_analysis['level'] == 'Pozycyjny':
            return "Rozumiem twój punkt widzenia, ale muszę spojrzeć na to szerzej. Czy możemy porozmawiać o faktach?"
        else:
            return "Okej, słucham. Opowiedz więcej."
        if ciq_analysis['level'] == 'Transformacyjny':
            return "Doceniam twoje podejście. Zgadzam się, że warto to omówić szczegółowo. Co proponujesz?"
        elif ciq_analysis['level'] == 'Pozycyjny':
            return "Rozumiem twój punkt widzenia, ale muszę spojrzeć na to szerzej. Czy możemy porozmawiać o faktach?"
        else:
            return "Okej, słucham. Opowiedz więcej."
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Spróbuj użyć najbardziej dostępnego modelu
        try:
            model = genai.GenerativeModel(
                "gemini-2.0-flash-exp",
                generation_config=genai.GenerationConfig(
                    temperature=0.9,  # Wysoka kreatywność
                    top_p=0.95,
                    top_k=40,
                )
            )
        except:
            # Fallback na stabilny model
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config=genai.GenerationConfig(
                    temperature=0.9,
                    top_p=0.95,
                    top_k=40,
                )
            )
        
        # Przygotuj historię rozmowy z odpowiednimi rolami
        history_text = "\n".join([
            f"{scenario.get('ai_role', 'AI') if msg['role'] == 'ai' else scenario.get('user_role', 'Ty')}: {msg['content']}" 
            for msg in conversation_history[-8:]  # Ostatnie 4 wymiany
        ])
        
        # Pobierz kontekst case study jeśli istnieje
        case_context = st.session_state.get('simulator_case_context', '')
        
        # Sprawdź liczbę wymian - czy zbliżamy się do końca?
        user_turns = len([m for m in conversation_history if m['role'] == 'user']) + 1  # +1 bo obecna
        max_turns = st.session_state.get('simulator_max_turns', 10)
        approaching_end = user_turns >= 6  # Po 6 wymianach sugeruj zakończenie
        
        # Prompt dla AI - z kontekstem case study
        end_hint = ""
        if approaching_end:
            end_hint = "\n\nWSKAZÓWKA: To już wymiana {}/{}. Subtelnie sugeruj zakończenie rozmowy - np. 'Myślę że ustaliliśmy...', 'Wydaje mi się że dobrze byłoby teraz...', itp.".format(user_turns, max_turns)
        
        prompt = f"""Wcielasz się w rolę: {scenario.get('ai_role', 'rozmówcy')} w symulacji biznesowej.

KONTEKST SYTUACJI:
{case_context}

TWOJA POSTAĆ: {scenario['ai_persona']}

DOTYCHCZASOWA ROZMOWA:
{history_text}

{scenario.get('user_role', 'Rozmówca').upper()} WŁAŚNIE POWIEDZIAŁ: "{user_input}"

Odpowiedz jako {scenario.get('ai_role', 'rozmówca')} - naturalnie, bezpośrednio, w 1-2 zdaniach.

WSKAZÓWKI:
- Pamiętaj o kontekście sytuacji i używaj go w odpowiedziach gdy to naturalne
- Jeśli rozmówca używa słów "my", "razem", "wspólnie" → bądź bardziej otwarty i współpracuj
- Jeśli atakuje lub oskarża → bądź defensywny lub zdecydowany  
- Jeśli zadaje pytanie → odpowiedz konkretnie na nie
- Zachowuj swoją postać ale reaguj naturalnie na ton rozmówcy
- NIE powtarzaj poprzednich odpowiedzi{end_hint}

Odpowiedź ({scenario.get('ai_role', 'AI')}):"""

        response = model.generate_content(prompt)
        ai_text = response.text.strip()
        
        # Zwróć odpowiedź AI
        if len(ai_text) > 0:
            return ai_text
        else:
            # Pusta odpowiedź - użyj fallbacku
            raise Exception("AI zwróciło pustą odpowiedź")
        
    except Exception as e:
        # Ciche logowanie błędu (bez wyświetlania użytkownikowi)
        # Można dodać print(f"AI Error: {e}") do debugowania lokalnie
        
        # Fallback jeśli API zawiedzie - lepsze odpowiedzi bazowane na C-IQ
        if ciq_analysis['level'] == 'Transformacyjny':
            return "Naprawdę doceniam twoje podejście. Zastanówmy się razem, jak to rozwiązać."
        elif ciq_analysis['level'] == 'Pozycyjny':
            return "Hmm, widzę że masz swoje zdanie. Ale czy możemy spojrzeć na to z innej perspektywy?"
        else:
            return "Dobrze, co jeszcze chciałbyś powiedzieć?"

def show_simulators():
    """Symulatory komunikacyjne"""
    # Wymuś przeładowanie modułu w trybie dev
    import sys
    if 'views.simulators.business_simulator' in sys.modules:
        import importlib
        importlib.reload(sys.modules['views.simulators.business_simulator'])
    
    from views.simulators.business_simulator import show_business_simulator
    
    st.markdown("### 🎭 Symulatory Komunikacyjne")
    st.markdown("Interaktywne symulacje różnych scenariuszy komunikacyjnych")
    
    # Siatka symulatorów
    col1, col2 = st.columns(2)
    
    with col1:
        business_sim_html = '''
        <div style='padding: 20px; border: 2px solid #9C27B0; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #f3e5f5 0%, #ce93d8 100%);'>
            <h4>💼 Symulator Rozmów Biznesowych</h4>
            <p><strong>Ćwicz trudne rozmowy z AI partnerem</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>🎯 8 różnych scenariuszy biznesowych</li>
                <li>🤖 AI odgrywa różne role</li>
                <li>📊 Analiza C-IQ w czasie rzeczywistym</li>
            </ul>
        </div>
        '''
        st.markdown(business_sim_html, unsafe_allow_html=True)
        
        if zen_button("💼 Uruchom Symulator", key="business_simulator", width='stretch'):
            st.session_state.active_simulator = "business_conversation"
    
    with col2:
        negotiation_html = '''
        <div style='padding: 20px; border: 2px solid #795548; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #efebe9 0%, #bcaaa4 100%); opacity: 0.6;'>
            <h4>🤝 Trener Negocjacji</h4>
            <p><strong>🚧 W przygotowaniu 🚧</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>⚖️ Scenariusze negocjacyjne</li>
                <li>🎯 Techniki C-IQ w negocjacjach</li>
                <li>📈 Analiza skuteczności</li>
            </ul>
        </div>
        '''
        st.markdown(negotiation_html, unsafe_allow_html=True)
        
        if zen_button("🤝 Uruchom Trenera", key="negotiation_trainer", width='stretch'):
            st.info("🚧 W przygotowaniu - trening umiejętności negocjacyjnych")
    
    # Wyświetl aktywny symulator
    active_simulator = st.session_state.get('active_simulator')
    
    if active_simulator == "business_conversation":
        st.markdown("---")
        show_business_simulator()

def show_analytics():
    """Analityki i tracking postępów"""
    st.markdown("### 📊 Analityki i Tracking")
    st.markdown("Zaawansowane analityki postępów w rozwoju umiejętności komunikacyjnych")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tracker_html = '''
        <div style='padding: 15px; border: 1px solid #4CAF50; border-radius: 10px; background: #f8fff8;'>
            <h4>📈 Tracker Postępów</h4>
            <p>Monitoruj rozwój umiejętności C-IQ w czasie</p>
        </div>
        '''
        st.markdown(tracker_html, unsafe_allow_html=True)
        
        if zen_button("📈 Zobacz Postępy", key="progress_tracker", width='stretch'):
            st.info("🚧 W przygotowaniu - szczegółowy tracking postępów w nauce")
    
    with col2:
        goals_html = '''
        <div style='padding: 15px; border: 1px solid #FF9800; border-radius: 10px; background: #fffbf0;'>
            <h4>🎯 Cele Rozwoju</h4>
            <p>Ustaw i śledź osobiste cele komunikacyjne</p>
        </div>
        '''
        st.markdown(goals_html, unsafe_allow_html=True)
        
        if zen_button("🎯 Ustaw Cele", key="development_goals", width='stretch'):
            st.info("🚧 W przygotowaniu - system celów rozwojowych")
    
    with col3:
        report_html = '''
        <div style='padding: 15px; border: 1px solid #2196F3; border-radius: 10px; background: #f0f8ff;'>
            <h4>📋 Raport Umiejętności</h4>
            <p>Kompleksowy raport Twoich kompetencji</p>
        </div>
        '''
        st.markdown(report_html, unsafe_allow_html=True)
        
        if zen_button("📋 Zobacz Raport", key="skills_report", width='stretch'):
            st.info("🚧 W przygotowaniu - szczegółowy raport umiejętności")

def show_ai_assistant():
    """AI Asystent personalny"""
    st.markdown("### 🤖 AI Asystent Personalny")
    st.markdown("Twój osobisty coach AI do rozwoju umiejętności komunikacyjnych")
    
    # Placeholder dla chatbota
    st.info("🚧 **W przygotowaniu** - inteligentny asystent AI dostępny 24/7")
    
    # Demo interfejsu chatbota
    st.markdown("#### 💬 Przykład rozmowy z AI Asystenem:")
    
    # Przykładowe wiadomości
    with st.chat_message("assistant"):
        st.markdown("Cześć! Jestem Twoim AI Asystenem do rozwoju komunikacji. W czym mogę Ci pomóc?")
    
    with st.chat_message("user"):
        st.markdown("Jak przygotować się do trudnej rozmowy z szefem?")
    
    with st.chat_message("assistant"):
        ai_response = '''
        Świetne pytanie! Oto moja strategia oparta na C-IQ:
        
        **🎯 Przygotowanie:**
        1. Zidentyfikuj cel rozmowy (co chcesz osiągnąć)
        2. Przygotuj pytania otwarte zamiast oskarżeń
        3. Zastanów się nad wspólnymi celami
        
        **💭 Podczas rozmowy:**
        - Zacznij od poziomu III: "Chciałbym porozmawiać o..."
        - Unikaj języka "ty" na rzecz "my", "nas"
        - Zadawaj pytania: "Jak widzisz tę sytuację?"
        
        Chcesz przećwiczyć konkretny scenariusz?
        '''
        st.markdown(ai_response)
    
    # Wyłączony input
    chat_input = st.chat_input("Napisz wiadomość do AI Asystenta...", disabled=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔮 Planowane funkcje:**")
        st.markdown("• Rozmowy w czasie rzeczywistym")
        st.markdown("• Personalizowane porady")
        st.markdown("• Analiza postępów")
        st.markdown("• Przypomnienia o ćwiczeniach")
    
    with col2:
        st.markdown("**🎯 Obszary wsparcia:**")
        st.markdown("• Przygotowanie do trudnych rozmów")
        st.markdown("• Analiza komunikacji")
        st.markdown("• Strategie C-IQ")
        st.markdown("• Budowanie pewności siebie")

# ===============================================
# CONVERSATION INTELLIGENCE PRO - FUNKCJE AI
# ===============================================

def analyze_conversation_sentiment(text: str) -> Optional[Dict]:
    """Analizuje sentiment rozmowy menedżer-pracownik + poziomy C-IQ"""
    evaluator = AIExerciseEvaluator()
    
    prompt = f"""
Jesteś ekspertem w Conversational Intelligence i analizie rozmów przywódczych między menedżerem a pracownikiem.
Przeanalizuj następującą transkrypcję rozmowy menedżerskiej:

TRANSKRYPCJA:
"{text}"

Przeprowadź kompleksową analizę z perspektywy przywództwa zawierającą:
1. SENTIMENT ANALYSIS - emocje menedżera i pracownika
2. C-IQ LEVELS - poziomy komunikacji przywódczej
3. NEUROBIOLOGICAL IMPACT - wpływ na kortyzol/oksytocynę w kontekście zespołu
4. LEADERSHIP INSIGHTS - wnioski dla rozwoju przywództwa

Odpowiedz w formacie JSON:
{{
    "overall_sentiment": "pozytywny/neutralny/negatywny",
    "sentiment_score": [1-10],
    "ciq_analysis": {{
        "manager_level": "Poziom I/II/III",
        "employee_level": "Poziom I/II/III", 
        "leadership_effectiveness": "niska/średnia/wysoka",
        "conversation_flow": "buduje_zaufanie/neutralna/tworzy_napięcie"
    }},
    "emotions_detected": {{
        "manager": ["emocja1", "emocja2"],
        "employee": ["emocja1", "emocja2"]
    }},
    "neurobiological_impact": {{
        "cortisol_triggers": ["sytuacja powodująca stres"],
        "oxytocin_builders": ["sytuacja budująca zaufanie"]
    }},
    "leadership_insights": {{
        "team_engagement_risk": [1-10],
        "leadership_effectiveness": [1-10],
        "key_moments": ["ważny moment w rozmowie przywódczej"],
        "development_opportunities": ["obszar rozwoju przywództwa"]
    }},
    "recommendations": {{
        "immediate_actions": ["natychmiastowe działanie"],
        "long_term_improvements": ["długoterminowa poprawa"],
        "coaching_points": ["wskazówka dla menedżera"]
    }}
}}
"""
    
    try:
        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                import json, re
                content = response.text.strip()
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    return result
        
        return create_fallback_sentiment_analysis(text)
    except Exception as e:
        st.error(f"❌ Błąd analizy sentiment: {str(e)}")
        return create_fallback_sentiment_analysis(text)

def analyze_business_intent(text: str) -> Optional[Dict]:
    """Wykrywa intencje biznesowe w rozmowie"""
    evaluator = AIExerciseEvaluator()
    
    prompt = f"""
Jesteś ekspertem w wykrywaniu intencji biznesowych w rozmowach.
Przeanalizuj następujący tekst pod kątem potrzeb i motywacji pracownika:

TEKST: "{text}"

Wykryj i ocen potrzeby pracownika oraz dynamike zespolowa. Odpowiedz w JSON:
{{
    "detected_intents": [
        {{
            "need": "development/support/recognition/autonomy/clear_goals/workload_balance", 
            "confidence": [1-10],
            "evidence": ["konkretny fragment tekstu"],
            "urgency": "low/medium/high"
        }}
    ],
    "team_dynamics": {{
        "engagement_level": [1-10],
        "motivation_level": [1-10],
        "development_readiness": "high/medium/low",
        "leadership_approach": "konkretne podejscie przywodcze"
    }},
    "risk_assessment": {{
        "burnout_risk": [1-10],
        "turnover_likelihood": [1-10],
        "performance_decline": [1-10]
    }},
    "leadership_actions": [
        "konkretne dzialanie menedzerskie 1",
        "konkretne dzialanie menedzerskie 2"
    ],
    "key_phrases": ["ważna fraza1", "ważna fraza2"]
}}
"""
    
    try:
        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                import json, re
                content = response.text.strip()
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
        
        return create_fallback_intent_analysis(text)
    except Exception:
        return create_fallback_intent_analysis(text)

def analyze_escalation_risk(text: str, sensitivity: int) -> Optional[Dict]:
    """Analizuje ryzyko problemów zespołowych i wypalenia"""
    evaluator = AIExerciseEvaluator()
    
    prompt = f"""
Jesteś ekspertem w wykrywaniu sygnałów problemów zespołowych i wypalenia zawodowego w kontekście przywództwa.
Czułość wykrywania: {sensitivity}/10 (1=bardzo konserwatywne, 10=bardzo wyczulone)

FRAGMENT ROZMOWY Z PRACOWNIKIEM: "{text}"

Przeanalizuj ryzyko problemów zespołowych i odpowiedz w JSON:
{{
    "team_problem_risk": [1-10],
    "risk_level": "low/medium/high/critical", 
    "warning_signals": [
        {{
            "signal": "konkretny sygnał problemu zespołowego",
            "severity": [1-10],
            "fragment": "fragment tekstu pokazujący sygnał"
        }}
    ],
    "employee_state": {{
        "current_emotion": "motywacja/frustracja/wypalenie/zaangażowanie",
        "engagement_level": [1-10],
        "progression": "improving/stable/deteriorating"
    }},
    "leadership_actions": [
        "rekomendowane działanie przywódcze 1",
        "rekomendowane działanie przywódcze 2"
    ],
    "support_strategies": [
        "strategia wsparcia pracownika 1", 
        "strategia wsparcia pracownika 2"
    ],
    "hr_escalation": {{
        "recommended": true/false,
        "reason": "powód przekazania do HR lub wyższego managementu",
        "urgency": "immediate/within_week/monitor"
    }}
}}
"""
    
    try:
        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                import json, re
                content = response.text.strip()
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                    
        return create_fallback_escalation_analysis(text, sensitivity)
    except Exception:
        return create_fallback_escalation_analysis(text, sensitivity)

def get_ai_coaching(text: str, context: str) -> Optional[Dict]:
    """Generuje coaching przywódczy w czasie rzeczywistym dla menedżerów"""
    evaluator = AIExerciseEvaluator()
    
    prompt = f"""
Jesteś ekspertem w Conversational Intelligence i coachem przywódczym dla menedżerów.

TYP ROZMOWY MENEDŻERSKIEJ: {context}
OSTATNIA WYPOWIEDŹ PRACOWNIKA: "{text}"

Zasugeruj najlepszą odpowiedź menedżerską na poziomie III C-IQ (Transformacyjnym), która buduje zaufanie i zaangażowanie w zespole.

Odpowiedz w JSON:
{{
    "suggested_responses": [
        {{
            "response": "konkretna sugerowana odpowiedź",
            "ciq_level": "III",
            "rationale": "dlaczego ta odpowiedź jest dobra",
            "expected_outcome": "oczekiwany rezultat"
        }}
    ],
    "alternative_approaches": [
        {{
            "approach": "alternatywne podejście",
            "when_to_use": "kiedy użyć tego podejścia"
        }}
    ],
    "what_to_avoid": [
        "czego unikać w odpowiedzi 1",
        "czego unikać w odpowiedzi 2"
    ],
    "ciq_techniques": [
        "konkretna technika C-IQ do zastosowania",
        "druga technika C-IQ"
    ],
    "follow_up_questions": [
        "pytanie otwarte dla pracownika 1",
        "pytanie otwarte dla pracownika 2"
    ],
    "leadership_strategy": {{
        "employee_emotion": "rozpoznana emocja pracownika",
        "desired_team_state": "pożądany stan zespołu", 
        "leadership_approach": "jak menedżer może wspierać przejście do lepszego stanu"
    }}
}}
"""
    
    try:
        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                import json, re
                content = response.text.strip()
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                    
        return create_fallback_coaching(context)
    except Exception:
        return create_fallback_coaching(context)

# ===============================================
# FALLBACK FUNCTIONS (gdy AI nie działa)
# ===============================================

def create_fallback_sentiment_analysis(text: str) -> Dict:
    """Fallback analiza sentiment gdy AI nie działa"""
    text_lower = text.lower()
    
    negative_words = ['problem', 'błąd', 'nie działa', 'zły', 'słaby', 'frustracja', 'źle']
    positive_words = ['dobrze', 'super', 'świetnie', 'dziękuję', 'pomocy', 'miło']
    
    neg_count = sum(1 for word in negative_words if word in text_lower)
    pos_count = sum(1 for word in positive_words if word in text_lower)
    
    if neg_count > pos_count:
        sentiment = "negatywny"
        score = max(3, 5 - neg_count)
    elif pos_count > neg_count:
        sentiment = "pozytywny" 
        score = min(8, 5 + pos_count)
    else:
        sentiment = "neutralny"
        score = 5
        
    return {
        "overall_sentiment": sentiment,
        "sentiment_score": score,
        "ciq_analysis": {
            "manager_level": "Poziom II",
            "employee_level": "Poziom I", 
            "leadership_effectiveness": "srednia",
            "conversation_flow": "neutralna"
        },
        "business_insights": {
            "escalation_risk": neg_count * 2,
            "satisfaction_prediction": score,
            "key_moments": ["Analiza heurystyczna"],
            "improvement_opportunities": ["Użyj więcej pytań otwartych"]
        },
        "recommendations": {
            "immediate_actions": ["Zastosuj techniki C-IQ poziom III"],
            "coaching_points": ["Fokus na współtworzeniu rozwiązań"]
        }
    }

def create_fallback_intent_analysis(text: str) -> Dict:
    """Fallback analiza intencji"""
    text_lower = text.lower()
    
    development_signals = ['rozwój', 'szkolenie', 'nauka', 'kariera', 'awans']
    support_signals = ['pomoc', 'wsparcie', 'trudności', 'przeciążenie', 'stres']
    
    need = "general_support"
    if any(word in text_lower for word in development_signals):
        need = "development"
    elif any(word in text_lower for word in support_signals):
        need = "support"
        
    return {
        "detected_intents": [{
            "need": need,
            "confidence": 7,
            "evidence": ["Analiza słów kluczowych"],
            "urgency": "medium"
        }],
        "team_dynamics": {
            "engagement_level": 5,
            "development_readiness": "medium"
        },
        "leadership_actions": [
            "Zastosuj techniki C-IQ Poziom III",
            "Zadaj pytania otwarte o potrzeby pracownika"
        ]
    }

def create_fallback_escalation_analysis(text: str, sensitivity: int) -> Dict:
    """Fallback analiza problemów zespołowych"""
    text_lower = text.lower()
    problem_words = ['przeciążenie', 'stres', 'wypalenie', 'frustracja', 'demotywacja', 'rezygnacja']
    
    problem_count = sum(1 for word in problem_words if word in text_lower)
    risk = min(10, problem_count * sensitivity)
    
    return {
        "team_problem_risk": risk,
        "risk_level": "high" if risk > 7 else "medium" if risk > 4 else "low",
        "warning_signals": [{
            "signal": f"Wykryto {problem_count} sygnałów problemów zespołowych",
            "severity": min(8, problem_count * 2)
        }],
        "leadership_actions": [
            "Przeprowadź rozmowę 1-on-1 z pracownikiem",
            "Zastosuj techniki C-IQ Poziom III"
        ],
        "support_strategies": [
            "Zaoferuj wsparcie w zarządzaniu obciążeniem",
            "Skup się na wspólnych celach zespołu"
        ],
        "hr_escalation": {
            "recommended": risk > 8,
            "reason": "Wysokie ryzyko problemów zespołowych wymagających interwencji HR"
        }
    }

def create_fallback_coaching(context: str) -> Dict:
    """Fallback coaching przywódczy"""
    return {
        "suggested_responses": [{
            "response": "Rozumiem Twoją sytuację. Jak możemy wspólnie pracować nad tym wyzwaniem?",
            "ciq_level": "III",
            "rationale": "Pytanie otwarte + język współtworzenia + empatia przywódcza"
        }],
        "ciq_techniques": [
            "Używaj pytań otwartych z pracownikami",
            "Język 'my' i 'wspólnie' zamiast 'ty musisz'",
            "Fokus na wspólnych celach zespołu"
        ],
        "what_to_avoid": [
            "Język dyrektywny menedżerski (Poziom I)",
            "Argumentowanie i przekonywanie (Poziom II)"
        ],
        "follow_up_questions": [
            "Co mogę zrobić, żeby Ci pomóc?",
            "Jakie wsparcie byłoby dla Ciebie najcenniejsze?"
        ],
        "leadership_strategy": {
            "employee_emotion": "analiza w trybie offline",
            "desired_team_state": "zaangażowany i zmotywowany zespół",
            "leadership_approach": "coaching i wsparcie zamiast kontroli"
        }
    }

# ===============================================
# LEADERSHIP PROFILE FUNCTIONS
# ===============================================

def create_leadership_profile(conversations_text: str) -> Optional[Dict]:
    """Tworzy długoterminowy profil przywódczy na podstawie wielu rozmów"""
    evaluator = AIExerciseEvaluator()
    
    prompt = f"""
Jesteś ekspertem w analizie długoterminowych wzorców przywódczych przez pryzmat Conversational Intelligence.
Przeanalizuj zbiór rozmów menedżerskich i stwórz kompletny profil przywódczy.

ZBIÓR ROZMÓW MENEDŻERSKICH:
"{conversations_text}"

Stwórz długoterminowy profil przywódczy w JSON:
{{
    "dominant_ciq_level": "I/II/III",
    "ciq_distribution": {{
        "level_i_percentage": [0-100],
        "level_ii_percentage": [0-100], 
        "level_iii_percentage": [0-100]
    }},
    "leadership_style": {{
        "primary_style": "directive/collaborative/transformational/coaching",
        "flexibility_score": [1-10],
        "adaptability": "low/medium/high"
    }},
    "communication_patterns": {{
        "question_types": "closed/mixed/open_dominant",
        "language_patterns": ["wzorzec 1", "wzorzec 2"],
        "emotional_intelligence": [1-10]
    }},
    "neurobiological_impact": {{
        "cortisol_triggers": [1-10],
        "oxytocin_builders": [1-10],
        "psychological_safety": [1-10]
    }},
    "strengths": [
        "silna strona przywódcza 1",
        "silna strona przywódcza 2"
    ],
    "development_areas": [
        "obszar do rozwoju 1", 
        "obszar do rozwoju 2"
    ],
    "leadership_evolution": {{
        "trajectory": "improving/stable/declining",
        "consistency": [1-10],
        "growth_potential": [1-10]
    }},
    "team_impact": {{
        "predicted_engagement": [1-10],
        "trust_building_capability": [1-10],
        "conflict_resolution": [1-10]
    }}
}}
"""
    
    try:
        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            if response and response.text:
                import json, re
                content = response.text.strip()
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                    
        return create_fallback_leadership_profile()
    except Exception:
        return create_fallback_leadership_profile()

def create_fallback_leadership_profile() -> Dict:
    """Fallback profil gdy AI nie działa - menedżer poziom I-II"""
    return {
        "dominant_ciq_level": "I",
        "ciq_distribution": {
            "level_i_percentage": 55,
            "level_ii_percentage": 35,
            "level_iii_percentage": 10
        },
        "leadership_style": {
            "primary_style": "directive",
            "flexibility_score": 4,
            "adaptability": "low"
        },
        "communication_patterns": {
            "question_types": "closed_dominant",
            "language_patterns": ["Polecenia i instrukcje", "Kontrola wykonania", "Wymagania rezultatów"],
            "emotional_intelligence": 4
        },
        "neurobiological_impact": {
            "cortisol_triggers": 7,
            "oxytocin_builders": 4,
            "psychological_safety": 4
        },
        "strengths": [
            "Jasne komunikowanie oczekiwań",
            "Zdecydowanie w podejmowaniu decyzji",
            "Orientacja na wyniki",
            "Reagowanie na problemy operacyjne"
        ],
        "development_areas": [
            "Redukcja stylu dyrektywnego (za dużo poziomu I)",
            "Rozwijanie umiejętności słuchania aktywnego",
            "Więcej pytań otwartych zamiast poleceń",
            "Budowanie bezpiecznej przestrzeni do dialogu",
            "Mniej presji czasowej w komunikacji"
        ],
        "leadership_evolution": {
            "trajectory": "stable",
            "consistency": 7,
            "growth_potential": 8
        },
        "team_impact": {
            "predicted_engagement": 4,
            "trust_building_capability": 4,
            "conflict_resolution": 5
        }
    }

def safe_get_numeric(data: dict, key: str, default: int) -> int:
    """Bezpieczne pobieranie wartości liczbowej z domyślną wartością"""
    value = data.get(key, default)
    return default if value is None else value

def generate_leadership_pdf(profile: Dict, username: str) -> bytes:
    """Generuje raport przywódczy w formacie PDF"""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import os
    
    # Utwórz buffer dla PDF
    buffer = io.BytesIO()
    
    # Zarejestruj font systemowy Windows z polskim wsparciem
    try:
        arial_path = "C:/Windows/Fonts/arial.ttf"
        if os.path.exists(arial_path):
            pdfmetrics.registerFont(TTFont('ArialUnicode', arial_path))
            unicode_font = "ArialUnicode"
            unicode_font_bold = "ArialUnicode"
        else:
            unicode_font = 'Times-Roman'
            unicode_font_bold = 'Times-Bold'
    except Exception as e:
        print(f"Błąd ładowania fontu: {e}")
        unicode_font = 'Times-Roman'
        unicode_font_bold = 'Times-Bold'
    
    # Konfiguracja dokumentu PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Style tekstu z obsługą polskich znaków
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=unicode_font_bold,
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#2E7D32'),
        alignment=1  # Center
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'], 
        fontName=unicode_font_bold,
        fontSize=16,
        spaceBefore=20,
        spaceAfter=12,
        textColor=HexColor('#1976D2')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName=unicode_font,
        fontSize=11,
        spaceAfter=8
    )
    
    # Zawartość PDF
    story = []
    
    # Upewnij się, że wszystkie stringi są w UTF-8 z polskimi znakami
    def ensure_unicode(text):
        if text is None:
            return ""
        if isinstance(text, (int, float)):
            return str(text)
        
        # Konwertuj na string i zachowaj polskie znaki
        text_str = str(text)
        
        # Upewnij się, że string jest w UTF-8
        try:
            if isinstance(text_str, bytes):
                text_str = text_str.decode('utf-8', errors='ignore')
            else:
                # Test enkodowania - jeśli się udaje, znaczy że string jest OK
                text_str.encode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            # Fallback - usuń problematyczne znaki
            text_str = str(text).encode('utf-8', errors='ignore').decode('utf-8')
            
        return text_str
    
    # Nagłówek
    story.append(Paragraph(ensure_unicode("💎 Raport Przywódczy C-IQ"), title_style))
    story.append(Paragraph(f"<b>Użytkownik:</b> {ensure_unicode(username)}", normal_style))
    story.append(Paragraph(f"<b>Data wygenerowania:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
    story.append(Spacer(1, 20))
    
    # Sekcja 1: Dominujący poziom
    story.append(Paragraph(ensure_unicode("🎯 Dominujący Poziom C-IQ"), subtitle_style))
    dominant_level = ensure_unicode(profile.get('dominant_ciq_level', 'Brak danych'))
    story.append(Paragraph(f"<b>{dominant_level}</b>", normal_style))
    story.append(Spacer(1, 15))
    
    # Sekcja 2: Rozkład poziomów
    story.append(Paragraph(ensure_unicode("📊 Rozkład Poziomów C-IQ"), subtitle_style))
    distribution = profile.get('ciq_distribution', {})
    
    level_data = [
        [ensure_unicode('Poziom'), ensure_unicode('Wartość')],
        [ensure_unicode('Level I (Transakcyjny)'), f"{safe_get_numeric(distribution, 'level_i_percentage', 30)}%"],
        [ensure_unicode('Level II (Pozycyjny)'), f"{safe_get_numeric(distribution, 'level_ii_percentage', 50)}%"], 
        [ensure_unicode('Level III (Transformacyjny)'), f"{safe_get_numeric(distribution, 'level_iii_percentage', 20)}%"]
    ]
    
    level_table = Table(level_data, colWidths=[3*inch, 2*inch])
    level_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), unicode_font_bold),
        ('FONTNAME', (0, 1), (-1, -1), unicode_font),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(level_table)
    story.append(Spacer(1, 20))
    
    # Sekcja 3: Neurobiologia 
    story.append(Paragraph(ensure_unicode("🧠 Wpływ Neurobiologiczny"), subtitle_style))
    neurobiological = profile.get('neurobiological_impact', {})
    
    neuro_data = [
        [ensure_unicode('Aspekt'), ensure_unicode('Poziom (1-10)')],
        [ensure_unicode('Wyzwalacze kortyzolu'), str(safe_get_numeric(neurobiological, 'cortisol_triggers', 5))],
        [ensure_unicode('Budowanie oksytocyny'), str(safe_get_numeric(neurobiological, 'oxytocin_builders', 5))],
        [ensure_unicode('Bezpieczeństwo psychologiczne'), str(safe_get_numeric(neurobiological, 'psychological_safety', 5))]
    ]
    
    neuro_table = Table(neuro_data, colWidths=[3.5*inch, 1.5*inch])
    neuro_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#FFF3E0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), unicode_font_bold),
        ('FONTNAME', (0, 1), (-1, -1), unicode_font),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(neuro_table)
    story.append(Spacer(1, 20))
    
    # Sekcja 4: Mocne strony
    story.append(Paragraph("💪 Mocne Strony", subtitle_style))
    strengths = profile.get('strengths', ['Brak danych'])
    for strength in strengths[:5]:  # Max 5 pozycji
        story.append(Paragraph(f"• {ensure_unicode(strength)}", normal_style))
    story.append(Spacer(1, 15))
    
    # Sekcja 5: Obszary rozwoju
    story.append(Paragraph(ensure_unicode("📈 Obszary Rozwoju"), subtitle_style))
    development_areas = profile.get('development_areas', ['Brak danych'])
    for area in development_areas[:5]:  # Max 5 pozycji  
        story.append(Paragraph(f"• {ensure_unicode(area)}", normal_style))
    story.append(Spacer(1, 20))
    
    # Nowa strona dla planu rozwoju
    story.append(PageBreak())
    story.append(Paragraph(ensure_unicode("🎯 Plan Rozwoju Przywódczego"), title_style))
    story.append(Spacer(1, 20))
    
    # Plan rozwoju - cele
    level_iii = safe_get_numeric(profile.get('ciq_distribution', {}), 'level_iii_percentage', 20)
    target_level_iii = min(level_iii + 20, 80)
    
    story.append(Paragraph("📊 Cele Rozwojowe", subtitle_style))
    story.append(Paragraph(f"<b>Aktualny poziom transformacyjny:</b> {level_iii}%", normal_style))
    story.append(Paragraph(f"<b>Docelowy poziom transformacyjny:</b> {target_level_iii}%", normal_style))
    story.append(Paragraph(f"<b>Wymagany wzrost:</b> +{target_level_iii - level_iii}%", normal_style))
    story.append(Spacer(1, 15))
    
    # Rekomendacje
    story.append(Paragraph("🎯 Kluczowe Rekomendacje", subtitle_style))
    
    recommendations = [
        "Praktykuj zadawanie pytań otwartych zamiast zamkniętych",
        "Rozwijaj umiejętności aktywnego słuchania", 
        "Wprowadzaj więcej empatii w codziennej komunikacji",
        "Eksperymentuj z różnymi stylami komunikacyjnymi",
        "Regularne sesje feedbacku z zespołem"
    ]
    
    for rec in recommendations:
        story.append(Paragraph(f"• {ensure_unicode(rec)}", normal_style))
    
    story.append(Spacer(1, 20))
    
    # Stopka
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontName=unicode_font,
        fontSize=9,
        textColor=colors.grey,
        alignment=1
    )
    
    story.append(Spacer(1, 30))
    story.append(Paragraph("---", footer_style))
    story.append(Paragraph(ensure_unicode("Raport wygenerowany przez BrainVenture Academy"), footer_style))
    story.append(Paragraph(ensure_unicode("System C-IQ Leadership Profile"), footer_style))
    
    # Zbuduj PDF
    doc.build(story)
    
    # Zwróć dane PDF
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def display_leadership_profile(profile: Dict):
    """Wyświetla profil przywódczy"""
    st.markdown("## 📊 Twój Profil Przywódczy C-IQ")
    
    # Główne metryki
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        dominant_level = profile.get('dominant_ciq_level', 'II')
        st.metric("🎯 Dominujący poziom C-IQ", f"Poziom {dominant_level}")
        
    with col2:
        leadership_style = profile.get('leadership_style', {})
        style = leadership_style.get('primary_style', 'collaborative')
        st.metric("👔 Styl przywództwa", style.title())
        
    with col3:
        team_impact = profile.get('team_impact', {})
        engagement = team_impact.get('predicted_engagement', 6)
        if engagement is None:
            engagement = 6
        st.metric("🚀 Wpływ na zaangażowanie", f"{engagement}/10")
        
    with col4:
        trust_building = team_impact.get('trust_building_capability', 6)
        if trust_building is None:
            trust_building = 6
        st.metric("🤝 Budowanie zaufania", f"{trust_building}/10")
    
    # Rozkład poziomów C-IQ
    st.markdown("### 📈 Rozkład Twoich poziomów C-IQ")
    distribution = profile.get('ciq_distribution', {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        level_i = distribution.get('level_i_percentage', 30)
        if level_i is None:
            level_i = 30
        st.metric("🔵 Poziom I (Transakcyjny)", f"{level_i}%")
        
    with col2:
        level_ii = distribution.get('level_ii_percentage', 50) 
        if level_ii is None:
            level_ii = 50
        st.metric("🟡 Poziom II (Pozycyjny)", f"{level_ii}%")
        
    with col3:
        level_iii = distribution.get('level_iii_percentage', 20)
        # Walidacja - upewniamy się że to liczba
        if level_iii is None:
            level_iii = 20
        st.metric("🟢 Poziom III (Transformacyjny)", f"{level_iii}%")
        
    # Rekomendacje na podstawie rozkładu C-IQ
    st.markdown("#### 💡 Rekomendacje na podstawie Twoich poziomów C-IQ:")
    
    # Walidacja wszystkich wartości przed porównaniem
    level_i = distribution.get('level_i_percentage', 30)
    if level_i is None:
        level_i = 30
    level_ii = distribution.get('level_ii_percentage', 50) 
    if level_ii is None:
        level_ii = 50
    if level_iii is None:
        level_iii = 20
    
    if level_iii < 30:
        st.warning("🎯 **Prioritet:** Zwiększ używanie poziomu III - zadawaj więcej pytań otwartych, słuchaj aktywnie, współtwórz rozwiązania")
    elif level_iii < 50:
        st.info("📈 **Kierunek rozwoju:** Kontynuuj pracę nad poziomem III - doskonał umiejętności budowania dialogu")
    else:
        st.success("🎉 **Gratulacje!** Masz silny poziom III - teraz skup się na konsystentności i rozwijaniu innych")
        
    if level_i > 50:
        st.warning("⚠️ **Uwaga:** Za dużo poziomu I (transakcyjnego) - spróbuj więcej słuchać niż mówić")
        
    if level_ii > 60:
        st.info("💡 **Wskazówka:** Dużo poziomu II - rozwijaj umiejętności przejścia do poziomu III")
    
    # Mocne strony i obszary rozwoju
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💪 Twoje mocne strony przywódcze")
        strengths = profile.get('strengths', [])
        for strength in strengths:
            st.markdown(f"✅ {strength}")
            
    with col2:
        st.markdown("### 🎯 Obszary do rozwoju")
        development_areas = profile.get('development_areas', [])
        for area in development_areas:
            st.markdown(f"📈 {area}")
            
    # Sekcja neurobiologiczna
    st.markdown("### 🧠 Wpływ neurobiologiczny Twojej komunikacji")
    neurobiological = profile.get('neurobiological_impact', {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        cortisol = neurobiological.get('cortisol_triggers', 5)
        if cortisol is None:
            cortisol = 5
        if cortisol <= 3:
            st.success(f"🟢 **Niski cortyzol** {cortisol}/10")
            st.write("Twoja komunikacja minimalizuje stres")
        elif cortisol <= 7:
            st.warning(f"🟡 **Średni cortyzol** {cortisol}/10") 
            st.write("Czasami możesz wywoływać napięcie")
        else:
            st.error(f"🔴 **Wysoki cortyzol** {cortisol}/10")
            st.write("Komunikacja może stresować zespół")
            
    with col2:
        oxytocin = neurobiological.get('oxytocin_builders', 5)
        if oxytocin is None:
            oxytocin = 5
        if oxytocin >= 7:
            st.success(f"🟢 **Wysoka oksytocyna** {oxytocin}/10")
            st.write("Świetnie budujesz więzi i zaufanie")
        elif oxytocin >= 4:
            st.info(f"🟡 **Średnia oksytocyna** {oxytocin}/10")
            st.write("Umiarkowanie budujesz relacje") 
        else:
            st.error(f"🔴 **Niska oksytocyna** {oxytocin}/10")
            st.write("Potrzeba więcej budowania więzi")
            
    with col3:
        safety = neurobiological.get('psychological_safety', 5)
        if safety is None:
            safety = 5
        if safety >= 7:
            st.success(f"🟢 **Wysokie bezpieczeństwo** {safety}/10")
            st.write("Zespół czuje się bezpiecznie")
        elif safety >= 4:
            st.info(f"🟡 **Średnie bezpieczeństwo** {safety}/10")
            st.write("Jest miejsce na poprawę bezpieczeństwa")
        else:
            st.error(f"🔴 **Niskie bezpieczeństwo** {safety}/10") 
            st.write("Zespół może czuć się niepewnie")
    
    # Sekcja skuteczności komunikacji
    st.markdown("### 📈 Skuteczność Twojej komunikacji")
    
    communication = profile.get('communication_patterns', {})
    team_impact = profile.get('team_impact', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Clarność przekazu - wyliczamy na podstawie poziomu C-IQ
        level_iii = profile.get('ciq_distribution', {}).get('level_iii_percentage', 20)
        if level_iii is None:
            level_iii = 20
        clarity_score = min(10, max(3, int(level_iii / 10 + 3)))
        
        if clarity_score >= 7:
            st.success(f"🎯 **Clarność przekazu** {clarity_score}/10")
            st.write("Komunikujesz jasno i zrozumiale")
        elif clarity_score >= 5:
            st.info(f"🎯 **Clarność przekazu** {clarity_score}/10")
            st.write("Przekaz jest w miarę jasny")
        else:
            st.warning(f"🎯 **Clarność przekazu** {clarity_score}/10")
            st.write("Przekaz wymaga uściślenia")
            
    with col2:
        trust_potential = team_impact.get('trust_building_capability', 6)
        if trust_potential is None:
            trust_potential = 6
        if trust_potential >= 7:
            st.success(f"🤝 **Potencjał zaufania** {trust_potential}/10")
            st.write("Silnie budujesz zaufanie zespołu")
        elif trust_potential >= 5:
            st.info(f"🤝 **Potencjał zaufania** {trust_potential}/10") 
            st.write("Umiarkowanie budujesz zaufanie")
        else:
            st.warning(f"🤝 **Potencjał zaufania** {trust_potential}/10")
            st.write("Zaufanie wymaga wzmocnienia")
            
    with col3:
        # Ryzyko konfliktu - odwrotność conflict_resolution
        conflict_resolution = team_impact.get('conflict_resolution', 6)
        if conflict_resolution is None:
            conflict_resolution = 6
        conflict_risk = 10 - conflict_resolution
        
        if conflict_risk <= 3:
            st.success(f"⚡ **Ryzyko konfliktu** {conflict_risk}/10")
            st.write("Bardzo niskie ryzyko konfliktów")
        elif conflict_risk <= 6:
            st.info(f"⚡ **Ryzyko konfliktu** {conflict_risk}/10")
            st.write("Umiarkowane ryzyko konfliktów") 
        else:
            st.warning(f"⚡ **Ryzyko konfliktu** {conflict_risk}/10")
            st.write("Wysokie ryzyko napięć w zespole")

def display_leadership_development_plan(profile: Dict):
    """Wyświetla plan rozwoju przywódczego"""
    st.markdown("## 🎯 Twój Plan Rozwoju Przywódczego")
    
    # Analiza obecnego poziomu
    dominant_level = profile.get('dominant_ciq_level', 'II')
    distribution = profile.get('ciq_distribution', {})
    level_iii_percentage = safe_get_numeric(distribution, 'level_iii_percentage', 20)
    
    st.markdown("### 📊 Analiza obecnej sytuacji")
    if level_iii_percentage < 30:
        st.warning(f"⚠️ **Poziom III stanowi tylko {level_iii_percentage}%** Twojej komunikacji. To główny obszar rozwoju!")
    elif level_iii_percentage < 50:
        st.info(f"📈 **Poziom III: {level_iii_percentage}%** - dobry start, ale jest miejsce na poprawę")
    else:
        st.success(f"🎉 **Poziom III: {level_iii_percentage}%** - świetny poziom transformacyjnego przywództwa!")
    
    # Plan rozwoju na najbliższe 3 miesiące
    st.markdown("### 🗓️ Plan rozwoju - najbliższe 3 miesiące")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎯 Cele do osiągnięcia:**")
        target_level_iii = min(level_iii_percentage + 20, 80)
        st.markdown(f"• Zwiększ poziom III z {level_iii_percentage}% do {target_level_iii}%")
        st.markdown("• Stosuj więcej pytań otwartych")
        st.markdown("• Praktykuj język współtworzenia")
        st.markdown("• Buduj psychologiczne bezpieczeństwo")
        
    with col2:
        st.markdown("**📚 Konkretne ćwiczenia:**")
        st.markdown("• **Tygodniowo:** 3 rozmowy 1-on-1 z fokusem na C-IQ III")
        st.markdown("• **Dziennie:** Zadaj 5+ pytań otwartych zespołowi") 
        st.markdown("• **Miesięcznie:** Przeanalizuj swoje rozmowy tym narzędziem")
        st.markdown("• **Kwartalne:** Feedback 360° o stylu komunikacji")
    
    # Benchmark z innymi liderami
    st.markdown("### 🏆 Benchmark z innymi liderami")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🥉 Lider Początkujący**")
        st.markdown("• Poziom III: 15-25%")
        st.markdown("• Fokus na zadania")
        st.markdown("• Komunikacja dyrektywna")
        
    with col2:
        st.markdown("**🥈 Lider Doświadczony**") 
        st.markdown("• Poziom III: 40-60%")
        st.markdown("• Balans zadania-relacje")
        st.markdown("• Rozwój zespołu")
        
    with col3:
        st.markdown("**🥇 Lider Transformacyjny**")
        st.markdown("• Poziom III: 65%+")
        st.markdown("• Inspiruje i motywuje")
        st.markdown("• Buduje kultur zaufania")
    
    # Gdzie jesteś
    if level_iii_percentage < 25:
        st.info("📍 **Jesteś na poziomie:** Lider Początkujący - świetny moment na rozwój!")
    elif level_iii_percentage < 60:
        st.success("📍 **Jesteś na poziomie:** Lider Doświadczony - bardzo dobry wynik!")
    else:
        st.success("📍 **Jesteś na poziomie:** Lider Transformacyjny - gratulacje! 🎉")

# ===============================================
# DISPLAY FUNCTIONS - WYŚWIETLANIE REZULTATÓW  
# ===============================================

def display_sentiment_results(result: Dict):
    """Wyświetla wyniki analizy sentymentu"""
    st.markdown("## 📊 Wyniki Analizy Sentiment + C-IQ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sentiment = result.get('overall_sentiment', 'neutralny')
        score = result.get('sentiment_score', 5)
        
        color = "🟢" if sentiment == "pozytywny" else "🔴" if sentiment == "negatywny" else "🟡"
        st.metric(f"{color} Sentiment ogólny", f"{sentiment.title()}", f"Ocena: {score}/10")
        
    with col2:
        ciq = result.get('ciq_analysis', {})
        manager_level = ciq.get('manager_level', 'N/A')
        st.metric("🎯 Poziom menedżera", manager_level)
        
    with col3:
        business = result.get('business_insights', {})
        escalation = business.get('escalation_risk', 0)
        color = "🟢" if escalation < 4 else "🟡" if escalation < 7 else "🔴"
        st.metric(f"{color} Ryzyko eskalacji", f"{escalation}/10")
    
    # Szczegóły
    if 'emotions_detected' in result:
        st.markdown("### 😊 Wykryte emocje")
        emotions = result['emotions_detected']
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("** Menedżer:**")
            for emotion in emotions.get('manager', []):
                st.markdown(f"• {emotion}")
                
        with col2:
            st.markdown("**👤 Pracownik:**")
            for emotion in emotions.get('employee', []):
                st.markdown(f"• {emotion}")
    
    # Rekomendacje
    if 'recommendations' in result:
        st.markdown("### 💡 Rekomendacje")
        recommendations = result['recommendations']
        
        if 'immediate_actions' in recommendations:
            st.markdown("**🚨 Natychmiastowe działania:**")
            for action in recommendations['immediate_actions']:
                st.markdown(f"• {action}")
                
        if 'coaching_points' in recommendations:
            st.markdown("**🎯 Wskazówki coachingowe:**")
            for point in recommendations['coaching_points']:
                st.markdown(f"• {point}")

def display_intent_results(result: Dict):
    """Wyświetla wyniki detekcji intencji"""
    st.markdown("## 🎯 Wykryte Intencje Biznesowe")
    
    if 'detected_intents' in result:
        for intent_data in result['detected_intents']:
            intent = intent_data.get('intent', 'unknown')
            confidence = intent_data.get('confidence', 0)
            urgency = intent_data.get('urgency', 'medium')
            
            # Kolory dla różnych intencji
            intent_colors = {
                'purchase': '💰',
                'complaint': '🚨', 
                'cancellation': '❌',
                'upsell_opportunity': '📈',
                'feature_request': '💡'
            }
            
            color = intent_colors.get(intent, '❓')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"{color} Intencja", intent.replace('_', ' ').title())
            with col2:
                st.metric("🎯 Pewność", f"{confidence}/10")
            with col3:
                urgency_color = "🔴" if urgency == "high" else "🟡" if urgency == "medium" else "🟢"
                st.metric(f"{urgency_color} Pilność", urgency.title())
    
    # Rekomendacje biznesowe
    if 'next_best_actions' in result:
        st.markdown("### 🎯 Rekomendowane działania")
        for action in result['next_best_actions']:
            st.markdown(f"• {action}")

def display_escalation_results(result: Dict):
    """Wyświetla wyniki analizy problemów zespołowych"""
    st.markdown("## 🚨 Analiza Problemów Zespołowych")
    
    risk_level = result.get('risk_level', 'medium')
    team_risk = result.get('team_problem_risk', result.get('escalation_risk', 5))
    
    # Kolory dla poziomów ryzyka
    risk_colors = {
        'low': '🟢',
        'medium': '🟡', 
        'high': '🟠',
        'critical': '🔴'
    }
    
    color = risk_colors.get(risk_level, '🟡')
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"{color} Poziom ryzyka", risk_level.upper(), f"{team_risk}/10")
    
    with col2:
        hr_esc = result.get('hr_escalation', result.get('manager_escalation', {}))
        if hr_esc.get('recommended', False):
            st.error("🚨 ZALECANE PRZEKAZANIE DO HR/WYŻSZEGO MANAGEMENTU")
        else:
            st.success("✅ Menedżer może kontynuować wsparcie zespołu")
    
    # Sygnały ostrzegawcze
    if 'warning_signals' in result:
        st.markdown("### ⚠️ Wykryte sygnały ostrzegawcze")
        for signal in result['warning_signals']:
            severity = signal.get('severity', 0)
            signal_text = signal.get('signal', '')
            severity_color = "🔴" if severity > 7 else "🟡" if severity > 4 else "🟢"
            st.markdown(f"{severity_color} **{signal_text}** (Intensywność: {severity}/10)")
    
    # Strategie wsparcia
    if 'support_strategies' in result:
        st.markdown("### 🤝 Strategie wsparcia pracownika")
        for strategy in result['support_strategies']:
            st.markdown(f"• {strategy}")
    
    # Działania przywódcze
    if 'leadership_actions' in result:
        st.markdown("### 👔 Rekomendowane działania menedżerskie")
        for action in result['leadership_actions']:
            st.markdown(f"• {action}")

def display_coaching_results(result: Dict):
    """Wyświetla wyniki coachingu przywódczego"""
    st.markdown("## 💡 Leadership Coach - Sugerowane odpowiedzi")
    
    # Główne sugestie
    if 'suggested_responses' in result:
        for i, suggestion in enumerate(result['suggested_responses']):
            st.markdown(f"### 🎯 Sugerowana odpowiedź {i+1}")
            
            response = suggestion.get('response', '')
            rationale = suggestion.get('rationale', '')
            
            st.success(f"**💬 Odpowiedź:** {response}")
            st.info(f"**🧠 Uzasadnienie:** {rationale}")
    
    # Techniki C-IQ
    if 'ciq_techniques' in result:
        st.markdown("### 🎯 Techniki C-IQ do zastosowania")
        for technique in result['ciq_techniques']:
            st.markdown(f"• {technique}")
    
    # Czego unikać
    if 'what_to_avoid' in result:
        st.markdown("### ❌ Czego unikać")
        for avoid in result['what_to_avoid']:
            st.markdown(f"• {avoid}")
    
    # Pytania otwarte
    if 'follow_up_questions' in result:
        st.markdown("### ❓ Sugerowane pytania otwarte")
        for question in result['follow_up_questions']:
            st.markdown(f"• {question}")

if __name__ == "__main__":
    show_tools_page()

