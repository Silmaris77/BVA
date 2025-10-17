"""
Modu≥ narzÍdzi AI dla BrainVenture Academy
Zawiera zaawansowane narzÍdzia do rozwoju umiejÍtnoúci komunikacyjnych i przywÛdztwa
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
    """Zapisuje profil przywÛdczy uøytkownika"""
    try:
        # åcieøka do pliku profili
        profiles_file = "leadership_profiles.json"
        
        # Wczytaj istniejπce profile lub stwÛrz nowy s≥ownik
        if os.path.exists(profiles_file):
            with open(profiles_file, 'r', encoding='utf-8') as f:
                profiles = json.load(f)
        else:
            profiles = {}
        
        # Migracja starych danych do nowej struktury
        if username in profiles:
            if not isinstance(profiles[username], dict) or "profiles" not in profiles[username]:
                # Stary format - przekszta≥Ê do nowego
                old_profile = profiles[username] if username in profiles else {}
                profiles[username] = {"profiles": [old_profile] if old_profile else [], "current_profile": 0}
        
        # Struktura: profiles[username] = {"profiles": [lista_profili], "current_profile": index}
        if username not in profiles:
            profiles[username] = {"profiles": [], "current_profile": 0}
        
        # Dodaj metadata do profilu
        profile['created_at'] = datetime.now().isoformat()
        profile['username'] = username
        profile['profile_name'] = profile_name or f"Profil {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Dodaj nowy profil do listy (zawsze dodaj nowy zamiast nadpisywaÊ)
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
        st.error(f"B≥πd zapisu profilu: {e}")
        return False

def load_leadership_profile(username: str, profile_index: Optional[int] = None) -> Optional[Dict]:
    """Wczytuje profil przywÛdczy uøytkownika"""
    try:
        profiles_file = "leadership_profiles.json"
        
        if not os.path.exists(profiles_file):
            return None
            
        with open(profiles_file, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            
        user_data = profiles.get(username)
        if not user_data:
            return None
            
        # Obs≥uga starego formatu (backward compatibility)
        if isinstance(user_data, dict) and 'profiles' not in user_data:
            return user_data
            
        # Nowy format z listπ profili
        if profile_index is not None:
            if 0 <= profile_index < len(user_data["profiles"]):
                return user_data["profiles"][profile_index]
        else:
            # ZwrÛÊ aktualny profil
            current_idx = user_data.get("current_profile", 0)
            if user_data["profiles"]:
                return user_data["profiles"][current_idx]
                
        return None
    except Exception as e:
        st.error(f"B≥πd wczytywania profilu: {e}")
        return None

def get_user_profiles_history(username: str) -> List[Dict]:
    """Pobiera historiÍ wszystkich profili uøytkownika"""
    try:
        profiles_file = "leadership_profiles.json"
        
        if not os.path.exists(profiles_file):
            return []
            
        with open(profiles_file, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
            
        user_data = profiles.get(username)
        if not user_data:
            return []
            
        # Obs≥uga starego formatu
        if isinstance(user_data, dict) and 'profiles' not in user_data:
            return [user_data]
            
        # Nowy format - zwrÛÊ wszystkie profile
        return user_data.get("profiles", [])
    except Exception:
        return []

def delete_user_profile(username: str, profile_index: Optional[int] = None) -> bool:
    """Usuwa profil uøytkownika"""
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
            # UsuÒ konkretny profil
            if isinstance(user_data, dict) and 'profiles' in user_data:
                if 0 <= profile_index < len(user_data["profiles"]):
                    user_data["profiles"].pop(profile_index)
                    # Zaktualizuj current_profile jeúli potrzeba
                    if user_data["current_profile"] >= len(user_data["profiles"]):
                        user_data["current_profile"] = max(0, len(user_data["profiles"]) - 1)
        else:
            # UsuÒ wszystkie profile uøytkownika
            del profiles[username]
            
        # Zapisz zmiany
        with open(profiles_file, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, ensure_ascii=False, indent=2)
            
        return True
    except Exception as e:
        st.error(f"B≥πd usuwania profilu: {e}")
        return False

def show_autodiagnosis():
    """NarzÍdzia autodiagnozy"""
    st.markdown("### ?? Autodiagnoza")
    st.markdown("Poznaj swÛj styl uczenia siÍ, typ neuroleadera i preferowane sposoby rozwoju")
    
    # Wyúwietl testy w dwÛch kolumnach
    col1, col2 = st.columns(2)
    
    # Karta z testem Neurolidera
    with col1:
        st.markdown("""
        <div style='padding: 20px; border: 2px solid #E91E63; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%);'>
            <h4>?? Test typu Neurolidera</h4>
            <p><strong>Odkryj swÛj unikalny styl przywÛdztwa i maksymalizuj swÛj potencja≥ lidera</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>?? Kompleksowa analiza stylu przywÛdztwa</li>
                <li>?? Wykres radarowy kompetencji</li>
                <li>?? Identyfikacja mocnych stron i wyzwaÒ</li>
                <li>?? Spersonalizowane strategie rozwoju</li>
                <li>?? Dopasowanie do rÛl biznesowych</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if zen_button("?? Rozpocznij Test Neurolidera", key="neuroleader_test", width='stretch'):
            st.session_state.active_tool = "neuroleader_test"
    
    # Karta z testem Kolba
    with col2:
        st.markdown("""
        <div style='padding: 20px; border: 2px solid #9C27B0; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);'>
            <h4>?? Test stylÛw uczenia siÍ wed≥ug Kolba</h4>
            <p><strong>Odkryj swÛj preferowany styl uczenia siÍ i maksymalizuj efektywnoúÊ rozwoju</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>?? 12 pytaÒ diagnostycznych</li>
                <li>?? Identyfikacja dominujπcego stylu </li>
                <li>?? Analiza mocnych stron w uczeniu siÍ</li>
                <li>?? Spersonalizowane wskazÛwki rozwojowe</li>
                <li>?? Zrozumienie pe≥nego cyklu uczenia siÍ Kolba</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if zen_button("?? Rozpocznij Test Kolba", key="kolb_test", width='stretch'):
            st.session_state.active_tool = "kolb_test"
    
    # Wyúwietl odpowiedni test jeúli jest aktywny
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
    """Wyúwietla test stylÛw uczenia siÍ wed≥ug Kolba"""
    st.markdown("### ?? Kolb Experiential Learning Profile (KELP)")
    
    # Wczytaj zapisane wyniki z bazy danych (jeúli uøytkownik zalogowany)
    # ALE TYLKO jeúli uøytkownik nie kliknπ≥ "Rozpocznij test od nowa"
    if st.session_state.get('logged_in') and st.session_state.get('username'):
        from data.users import load_user_data
        
        users_data = load_user_data()
        username = st.session_state.username
        
        # Sprawdü czy uøytkownik nie zresetowa≥ testu celowo
        if username in users_data and users_data[username].get('kolb_test'):
            # Jeúli uøytkownik ma zapisane wyniki, wczytaj je do session state
            kolb_data = users_data[username]['kolb_test']
            
            # Sprawdü czy session state nie ma juø wczytanych wynikÛw
            # ORAZ czy uøytkownik nie kliknπ≥ "reset" (sprawdzamy flagÍ kolb_reset)
            if not st.session_state.get('kolb_completed') and not st.session_state.get('kolb_reset'):
                st.session_state.kolb_results = kolb_data.get('scores', {})
                st.session_state.kolb_dimensions = kolb_data.get('dimensions', {})
                st.session_state.kolb_dominant = kolb_data.get('dominant_style')
                st.session_state.kolb_quadrant = kolb_data.get('quadrant')
                st.session_state.kolb_flexibility = kolb_data.get('flexibility', 0)
                st.session_state.kolb_completed = True
                
                # Informacja o wczytaniu zapisanych wynikÛw
                st.info(f"? Wczytano Twoje wczeúniejsze wyniki testu z dnia: {kolb_data.get('completed_date', 'Nieznana')}")
    
    # Karta z teoriπ ELT
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                box-shadow: 0 4px 15px rgba(102,126,234,0.4); 
                border-radius: 20px; 
                padding: 30px; 
                margin: 20px 0; 
                color: white;'>
        <div style='font-size: 2.5em; margin-bottom: 15px;'>??</div>
        <h4 style='color: white; margin: 0 0 20px 0;'>Teoria Uczenia siÍ przez Doúwiadczenie (ELT)</h4>
        <p style='font-size: 1.1em; line-height: 1.7; margin-bottom: 0;'>
            Teoria Davida Kolba z 1984 roku definiuje uczenie siÍ jako <b>dynamiczny proces</b>, 
            w ktÛrym wiedza jest tworzona poprzez <b>transformacjÍ doúwiadczenia</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Karty z czterema fazami cyklu
    st.markdown("<h4 style='margin: 30px 0 20px 0; color: #333;'>?? Cykl Uczenia siÍ Kolba - Cztery Fazy:</h4>", unsafe_allow_html=True)
    
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
            <h5 style='color: white; margin: 0 0 10px 0;'>1. Konkretne Doúwiadczenie (CE)</h5>
            <p style='margin: 0; font-size: 0.95em; line-height: 1.6;'>
                ZetkniÍcie siÍ z nowπ sytuacjπ<br><b>õ Feeling (Odczuwanie)</b>
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
                Tworzenie teorii i uogÛlnieÒ<br><b>õ Thinking (Myúlenie)</b>
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
                Obserwacja i refleksja<br><b>õ Watching (Obserwowanie)</b>
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
                Testowanie koncepcji w praktyce<br><b>õ Doing (Dzia≥anie)</b>
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
            <li><b>Oú Postrzegania:</b> Konkretne Przeøycie (CE) - Abstrakcyjna Konceptualizacja (AC)</li>
            <li><b>Oú Przetwarzania:</b> Refleksyjna Obserwacja (RO) - Aktywne Eksperymentowanie (AE)</li>
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
            ZidentyfikowaÊ TwÛj <b>preferowany styl uczenia siÍ</b> i oceniÊ <b>elastycznoúÊ</b> 
            w przechodzeniu przez pe≥ny cykl Kolba.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicjalizacja state
    if 'kolb_answers' not in st.session_state:
        st.session_state.kolb_answers = {}
    if 'kolb_completed' not in st.session_state:
        st.session_state.kolb_completed = False
    
    # Pytania testowe - 12 pytaÒ z 4 opcjami kaøde (odpowiadajπce CE, RO, AC, AE)
    # Format zgodny z LSI: ranking wymuszony wybÛr
    questions = [
        {
            "id": 1,
            "question": "Kiedy uczÍ siÍ czegoú nowego, najlepiej mi siÍ pracuje gdy:",
            "options": {
                "CE": "AngaøujÍ siÍ osobiúcie i uczÍ siÍ przez doúwiadczenie",
                "RO": "Mam czas na obserwacjÍ i refleksjÍ",
                "AC": "MogÍ analizowaÊ i tworzyÊ logiczne teorie",
                "AE": "MogÍ aktywnie testowaÊ i eksperymentowaÊ"
            }
        },
        {
            "id": 2,
            "question": "W procesie uczenia siÍ najbardziej ceniÍ:",
            "options": {
                "CE": "Konkretne przyk≥ady i osobiste doúwiadczenia",
                "RO": "MoøliwoúÊ przemyúlenia i obserwacji",
                "AC": "Abstrakcyjne koncepcje i modele teoretyczne",
                "AE": "Praktyczne zastosowania i dzia≥anie"
            }
        },
        {
            "id": 3,
            "question": "Podczas rozwiπzywania problemÛw:",
            "options": {
                "CE": "Polegam na intuicji i uczuciach",
                "RO": "S≥ucham rÛønych perspektyw i zbieramy informacje",
                "AC": "AnalizujÍ logicznie i systematycznie",
                "AE": "TestujÍ rÛøne rozwiπzania w praktyce"
            }
        },
        {
            "id": 4,
            "question": "W zespole najlepiej funkcjonujÍ jako:",
            "options": {
                "CE": "Osoba, ktÛra wnosi osobiste zaangaøowanie i empatiÍ",
                "RO": "Obserwator, ktÛry dostrzega rÛøne perspektywy",
                "AC": "Analityk, ktÛry tworzy strategie i plany",
                "AE": "Praktyk, ktÛry wdraøa i koordynuje dzia≥ania"
            }
        },
        {
            "id": 5,
            "question": "Podczas szkolenia/warsztatu najbardziej odpowiada mi:",
            "options": {
                "CE": "Osobiste zaangaøowanie i doúwiadczenie sytuacji",
                "RO": "Czas na dyskusjÍ i przemyúlenie tematu",
                "AC": "Solidne podstawy teoretyczne i modele",
                "AE": "Praktyczne Êwiczenia i testowanie umiejÍtnoúci"
            }
        },
        {
            "id": 6,
            "question": "PodejmujÍ decyzje g≥Ûwnie na podstawie:",
            "options": {
                "CE": "Osobistych wartoúci i bezpoúredniego doúwiadczenia",
                "RO": "Obserwacji sytuacji i przemyúleÒ",
                "AC": "Logicznej analizy i racjonalnych przes≥anek",
                "AE": "Praktycznych testÛw i sprawdzania w dzia≥aniu"
            }
        },
        {
            "id": 7,
            "question": "W sytuacji nowej/stresowej:",
            "options": {
                "CE": "KierujÍ siÍ emocjami i bezpoúrednim odczuciem",
                "RO": "WycofujÍ siÍ i najpierw obserwujÍ",
                "AC": "Szukam racjonalnych wyjaúnieÒ i teorii",
                "AE": "Dzia≥am szybko i sprawdzam co zadzia≥a"
            }
        },
        {
            "id": 8,
            "question": "Moja najwiÍksza mocna strona to:",
            "options": {
                "CE": "Empatia i wraøliwoúÊ na ludzi",
                "RO": "UmiejÍtnoúÊ s≥uchania i refleksji",
                "AC": "Zdolnoúci analityczne i logiczne myúlenie",
                "AE": "PraktycznoúÊ i skutecznoúÊ dzia≥ania"
            }
        },
        {
            "id": 9,
            "question": "Przy nauce nowego narzÍdzia/programu:",
            "options": {
                "CE": "EksperymentujÍ swobodnie i uczÍ siÍ przez prÛby",
                "RO": "ObserwujÍ innych i czytam opinie",
                "AC": "Czytam dokumentacjÍ i poznajÍ strukturÍ",
                "AE": "Od razu zaczynam uøywaÊ i testujÍ funkcje"
            }
        },
        {
            "id": 10,
            "question": "W projektach zawodowych najbardziej lubiÍ:",
            "options": {
                "CE": "PracÍ z ludümi i budowanie relacji",
                "RO": "Analizowanie danych i integracjÍ rÛønych perspektyw",
                "AC": "Tworzenie strategii i systemÛw",
                "AE": "RealizacjÍ konkretnych zadaÒ i wdraøanie"
            }
        },
        {
            "id": 11,
            "question": "Najlepiej pamiÍtam, gdy:",
            "options": {
                "CE": "CzujÍ emocjonalne po≥πczenie z tematem",
                "RO": "Mam czas na obserwacjÍ i rozwaøanie",
                "AC": "Rozumiem logikÍ i teoriÍ stojπcπ za tym",
                "AE": "PraktykujÍ i wielokrotnie testujÍ"
            }
        },
        {
            "id": 12,
            "question": "MÛj naturalny sposÛb dzia≥ania to:",
            "options": {
                "CE": "Spontaniczne reagowanie na sytuacje",
                "RO": "Cierpliwe obserwowanie przed dzia≥aniem",
                "AC": "Systematyczne planowanie i analizowanie",
                "AE": "Szybkie podejmowanie decyzji i dzia≥anie"
            }
        }
    ]
    
    # Wyúwietl pytania TYLKO jeúli test nie zosta≥ ukoÒczony
    if not st.session_state.kolb_completed:
        st.markdown("---")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                    border-radius: 12px; 
                    padding: 15px; 
                    margin: 20px 0; 
                    text-align: center;'>
            <h4 style='margin: 0; color: #2c3e50;'>?? Odpowiedz na poniøsze pytania</h4>
            <p style='margin: 5px 0 0 0; color: #555;'>Wybierz opcjÍ najbardziej do Ciebie pasujπcπ</p>
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
        if st.button("?? Oblicz mÛj styl uczenia siÍ", type="primary", width="stretch"):
            if len(st.session_state.kolb_answers) == len(questions):
                calculate_kolb_results()
                st.session_state.kolb_completed = True
                st.rerun()
            else:
                st.warning("?? ProszÍ odpowiedzieÊ na wszystkie pytania")
    
    # Wyúwietl wyniki jeúli test zosta≥ ukoÒczony
    if st.session_state.kolb_completed:
        display_kolb_results()

def generate_kolb_ai_tips(learning_style: str, profession: str):
    """Generuje spersonalizowane wskazÛwki AI na podstawie stylu uczenia siÍ i zawodu"""
    try:
        import google.generativeai as genai
        
        # Pobierz klucz API z secrets
        api_key = st.secrets.get("GOOGLE_API_KEY")
        
        if not api_key:
            st.error("? Klucz API Google Gemini nie jest skonfigurowany. Skontaktuj siÍ z administratorem.")
            return
        
        # Konfiguruj Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            st.secrets.get("AI_SETTINGS", {}).get("gemini_model", "gemini-2.5-flash")
        )
        
        # Mapowanie stylÛw na opisy (zgodnie z naukowπ dokumentacjπ ELT)
        style_descriptions = {
            "Diverging (Wyobraünia/Imagination)": "osoba uczπca siÍ przez konkretne doúwiadczenia i refleksyjnπ obserwacjÍ, postrzegajπca sytuacje z wielu perspektyw, ceniπca wyobraüniÍ i emocjonalne zaangaøowanie",
            "Assimilating (Teoria/Thinking)": "osoba uczπca siÍ przez abstrakcyjnπ konceptualizacjÍ i refleksyjnπ obserwacjÍ, ceniπca logiczne modele i systematyczne podejúcie teoretyczne",
            "Converging (Decyzja/Decision)": "osoba uczπca siÍ przez abstrakcyjnπ konceptualizacjÍ i aktywne eksperymentowanie, skupiona na praktycznym zastosowaniu teorii i rozwiπzywaniu problemÛw",
            "Accommodating (Dzia≥anie/Action)": "osoba uczπca siÍ przez konkretne doúwiadczenia i aktywne eksperymentowanie, ceniπca intuicjÍ, elastycznoúÊ i praktyczne dzia≥anie"
        }
        
        prompt = f"""Jesteú ekspertem od rozwoju zawodowego i stylÛw uczenia siÍ wed≥ug teorii Experiential Learning Theory (ELT) Davida Kolba.

Uøytkownik to {profession}, ktÛrego dominujπcym stylem uczenia siÍ jest: **{learning_style}**
({style_descriptions.get(learning_style, '')})

Wygeneruj **konkretne, praktyczne wskazÛwki** dostosowane do tego stylu uczenia siÍ.

KRYTYCZNE WYMAGANIA FORMATOWANIA:

1. UtwÛrz dok≥adnie 3 sekcje z nag≥Ûwkami:
   **Optymalne warunki dla Twojej nauki:**
   **Jak wzmacniaÊ swoje mocne strony:**
   **Jak rozwijaÊ obszary do rozwoju:**

2. Kaødy nag≥Ûwek MUSI byÊ w osobnej linii i po nim MUSI byÊ pusta linia

3. Pod kaødym nag≥Ûwkiem utwÛrz dok≥adnie 3 punkty rozpoczynajπce siÍ od "- "

4. W sekcji "Jak wzmacniaÊ swoje mocne strony" kaødy punkt powinien zaczynaÊ siÍ od pogrubionej nazwy mocnej strony, np:
   - **Empatia:** Wykorzystuj swojπ wraøliwoúÊ do...
   - **KreatywnoúÊ:** Twoja wyobraünia pozwala na...

5. W sekcji "Jak rozwijaÊ obszary do rozwoju" kaødy punkt powinien zaczynaÊ siÍ od pogrubionej nazwy obszaru, np:
   - **Podejmowanie decyzji:** Aby szybciej decydowaÊ, wyprÛbuj...
   - **Praktyczne wdraøanie:** Rozwijaj tÍ umiejÍtnoúÊ przez...

TREå∆:
- Bardzo konkretne wskazÛwki moøliwe do wdroøenia natychmiast
- Dostosowane do stylu {learning_style} i zawodu {profession}
- Kaødy punkt max 2-3 zdania
- W jÍzyku polskim
- BEZ formatowania HTML
- NIE uøywaj zwrotÛw typu "Warunek 1", "Mocna strona 2", "Obszar rozwoju 3" - pisz bezpoúrednio o konkretnej umiejÍtnoúci/warunku
"""
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            ai_tips = response.text
            st.session_state.kolb_ai_tips = ai_tips
            st.success("? WskazÛwki zosta≥y wygenerowane!")
        else:
            st.error("? Nie otrzymano odpowiedzi od AI")
            st.session_state.kolb_ai_tips = None
        
    except Exception as e:
        st.error(f"? B≥πd generowania wskazÛwek: {str(e)}")
        import traceback
        st.error(f"SzczegÛ≥y: {traceback.format_exc()}")
        st.session_state.kolb_ai_tips = None

def calculate_kolb_results():
    """Oblicza wyniki testu Kolba zgodnie z metodologiπ LSI"""
    answers = st.session_state.kolb_answers
    
    # Liczenie punktÛw dla kaødej zdolnoúci uczenia siÍ
    # CE = Konkretne Doúwiadczenie (Concrete Experience - Feeling)
    # RO = Refleksyjna Obserwacja (Reflective Observation - Watching)
    # AC = Abstrakcyjna Konceptualizacja (Abstract Conceptualization - Thinking)
    # AE = Aktywne Eksperymentowanie (Active Experimentation - Doing)
    
    scores = {"CE": 0, "RO": 0, "AC": 0, "AE": 0}
    
    for answer in answers.values():
        scores[answer] += 1
    
    # Obliczanie wymiarÛw rÛønicowych (zgodnie z metodologiπ LSI)
    # Wymiar Postrzegania (Oú Abstrakcja-Konkret)
    ac_ce = scores["AC"] - scores["CE"]  # Dodatni = preferencja AC, Ujemny = preferencja CE
    
    # Wymiar Przetwarzania (Oú AktywnoúÊ-Refleksja)
    ae_ro = scores["AE"] - scores["RO"]  # Dodatni = preferencja AE, Ujemny = preferencja RO
    
    # Okreúlenie stylu na podstawie wymiarÛw (siatka 2x2)
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
    
    # Obliczenie elastycznoúci uczenia siÍ (odleg≥oúÊ od centrum siatki)
    # Im bliøej centrum (0,0), tym wiÍksza elastycznoúÊ
    distance_from_center = math.sqrt(ac_ce**2 + ae_ro**2)
    max_distance = math.sqrt(12**2 + 12**2)  # Maksymalna odleg≥oúÊ przy 12 pytaniach
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
    
    # Zapisz wyniki do danych uøytkownika (persistent storage)
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
            
            # Zaloguj ukoÒczenie testu i przyznaj XP
            try:
                from data.users import award_xp_for_activity
                award_xp_for_activity(
                    username,
                    'test_completed',
                    5,  # 5 XP za ukoÒczenie testu Kolba
                    {
                        'test_name': 'Kolb Learning Styles',
                        'dominant_style': dominant_style,
                        'quadrant': quadrant
                    }
                )
            except Exception:
                pass
    
    # WyczyúÊ flagÍ reset po zapisaniu nowych wynikÛw (pozwÛl na auto-load przy kolejnym logowaniu)
    st.session_state.kolb_reset = False

def format_ai_tips_compact(ai_tips_text: str) -> str:
    """
    Formatuje tekst AI na kompaktowπ strukturÍ z kategoriami i punktami.
    Wykrywa sekcje i przekszta≥ca je w wizualne boxy.
    Radzi sobie z rÛønymi formatami AI (wieloliniowe i jednoliniowe punkty).
    """
    import re
    
    # Ikony dla rÛønych kategorii
    category_icons = {
        'optymalne warunki': '??',
        'warunki': '??',
        'nauki': '??',
        'mocne strony': '??',
        'wzmacniaÊ': '??',
        'silne': '??',
        'obszary do rozwoju': '??',
        'rozwijaÊ': '??',
        's≥abe': '??',
        'rozwÛj': '??',
        'metody': '??',
        'technik': '??',
        'narzÍdzi': '???',
        'strategi': '??',
        'Êwicz': '??',
        'przyk≥ad': '?',
        'zalec': '??',
        'unikaj': '??',
        'rozwÛj': '??',
        'praktyk': '?',
        'tips': '??',
        'wskazÛwk': '??',
        'zastosow': '??',
        'sposÛb': '??',
        'korzyúÊ': '??'
    }
    
    # Najpierw podziel tekst na sekcje przez nag≥Ûwki **Header**:
    # Uøyj regex aby znaleüÊ sekcje - TYLKO te ktÛre sπ na poczπtku linii i koÒczπ siÍ dwukropkiem + newline
    section_pattern = r'^\*\*(.+?)\*\*:\s*$'
    
    lines = ai_tips_text.strip().split('\n')
    formatted_sections = []
    current_section = None
    current_items = []
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # Sprawdü czy to nag≥Ûwek sekcji (linia zawiera TYLKO **Nag≥Ûwek**: i nic wiÍcej)
        header_match = re.match(section_pattern, line_stripped)
        
        if header_match and len(line_stripped) < 80:  # Nag≥Ûwki sπ krÛtkie (max 80 znakÛw)
            # To jest nag≥Ûwek sekcji
            if current_section and current_items:
                formatted_sections.append((current_section, current_items))
            
            current_section = header_match.group(1).strip()
            current_items = []
        else:
            # To jest zawartoúÊ (moøe zawieraÊ **bold:** wewnπtrz)
            # UsuÒ bullet points z poczπtku
            clean_line = re.sub(r'^[-ï*]+\s*', '', line_stripped)
            clean_line = clean_line.strip()
            
            if clean_line:
                if not current_section:
                    current_section = "WskazÛwki"
                current_items.append(clean_line)
    
    # Dodaj ostatniπ sekcjÍ
    if current_section and current_items:
        formatted_sections.append((current_section, current_items))
    
    # Jeúli nadal nic nie wykryto, fallback
    if not formatted_sections and ai_tips_text.strip():
        # Podziel po kropkach lub nowych liniach
        items = [item.strip() for item in re.split(r'[.\n]+', ai_tips_text) if item.strip()]
        if items:
            formatted_sections.append(("WskazÛwki AI", items))
    
    # Generuj HTML
    html_parts = []
    
    # Filtruj puste sekcje
    formatted_sections = [(title, items) for title, items in formatted_sections if items]
    
    if not formatted_sections:
        # Fallback - surowy tekst
        return f'''
        <div class="ai-tip-box" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 20px; border-radius: 8px;">
            <h3 style="margin: 0 0 10px 0; font-size: 16px; font-weight: bold;">?? WskazÛwki AI</h3>
            <div style="margin: 0; padding-left: 10px;">
                {ai_tips_text.replace(chr(10), '<br>')}
            </div>
        </div>
        '''
    
    for i, (title, items) in enumerate(formatted_sections):
        # UsuÒ emoji z tytu≥u jeúli juø jest
        title = re.sub(r'^[\U0001F300-\U0001F9FF]\s*', '', title)
        
        # Wybierz ikonÍ
        icon = '??'
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
        
        # Box z nag≥Ûwkiem i klasπ CSS - uøywamy div zamiast ul/li dla lepszego renderowania w PDF
        html_parts.append(f'''
        <div class="ai-tip-box" style="background: {bg}; color: {text_color}; padding: 12px 18px; border-radius: 8px; margin-bottom: 15px;">
            <h3 style="margin: 0 0 10px 0; font-size: 16px; font-weight: bold;">{icon} {title}</h3>
            <div style="margin: 0; padding-left: 10px;">
        ''')
        
        for item in items:
            # Sprawdü czy punkt zaczyna siÍ od **Bold tekst:**
            bold_prefix_match = re.match(r'^\*\*(.+?)\*\*:\s*(.+)', item)
            
            if bold_prefix_match:
                # Punkt ma bold prefix
                bold_text = bold_prefix_match.group(1).strip()
                rest_text = bold_prefix_match.group(2).strip()
                clean_item = f'<strong>{bold_text}:</strong> {rest_text}'
            else:
                # Zwyk≥y punkt - usuÒ gwiazdki z tekstu i zamieÒ na <strong>
                clean_item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
            
            # UsuÒ ewentualne podwÛjne spacje
            clean_item = re.sub(r'\s+', ' ', clean_item).strip()
            
            if clean_item:
                # Kaødy punkt jako osobny div z margin-bottom dla separacji
                html_parts.append(f'<div style="margin-bottom: 8px; line-height: 1.6; font-size: 14px;">? {clean_item}</div>')
        
        html_parts.append('</div></div>')
    
    return '\n'.join(html_parts)

def format_ai_tips_for_streamlit(ai_tips_text: str) -> str:
    """
    Formatuje tekst AI dla Streamlit (bez HTML, uøywa markdown i emoji).
    Zwraca czysty tekst z emoji i strukturπ do wyúwietlenia przez st.markdown().
    """
    import re
    
    # Podziel tekst na sekcje - nag≥Ûwki to linie z **Tekst:**
    section_pattern = r'^\*\*(.+?)\*\*:?\s*$'
    
    lines = ai_tips_text.strip().split('\n')
    sections = []
    current_section = None
    current_items = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # PomiÒ puste linie miÍdzy sekcjami
        if not line_stripped:
            continue
        
        # Sprawdü czy to nag≥Ûwek sekcji
        header_match = re.match(section_pattern, line_stripped)
        
        # Nag≥Ûwek = krÛtka linia (max 100 znakÛw) z **Tekst:**
        if header_match and len(line_stripped) < 100:
            # To jest nag≥Ûwek - zapisz poprzedniπ sekcjÍ
            if current_section and current_items:
                sections.append((current_section, current_items))
            
            current_section = header_match.group(1).strip().rstrip(':')
            current_items = []
        else:
            # To jest zawartoúÊ punktu
            # UsuÒ bullet points i spacje
            clean_line = re.sub(r'^[-ï*]\s*', '', line_stripped)
            clean_line = clean_line.strip()
            
            if clean_line:
                if not current_section:
                    # Jeúli nie ma sekcji, utwÛrz domyúlnπ
                    current_section = "WskazÛwki"
                current_items.append(clean_line)
    
    # Dodaj ostatniπ sekcjÍ
    if current_section and current_items:
        sections.append((current_section, current_items))
    
    # Jeúli nie wykryto sekcji, sprÛbuj przetworzyÊ jako jeden blok
    if not sections:
        # SprÛbuj podzieliÊ po pustych liniach i nag≥Ûwkach inline
        fallback_sections = []
        current_section = "WskazÛwki"
        current_items = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Sprawdü czy linia zawiera inline nag≥Ûwek **Tekst:** tekst
            inline_match = re.match(r'^\*\*(.+?)\*\*:\s*(.+)', line)
            if inline_match and len(inline_match.group(1)) < 50:
                if current_items:
                    fallback_sections.append((current_section, current_items))
                current_section = inline_match.group(1).strip()
                current_items = [inline_match.group(2).strip()]
            else:
                clean_line = re.sub(r'^[-ï*]\s*', '', line)
                if clean_line:
                    current_items.append(clean_line)
        
        if current_items:
            fallback_sections.append((current_section, current_items))
        
        sections = fallback_sections if fallback_sections else []
    
    # Jeúli nadal nie ma sekcji, zwrÛÊ surowy tekst
    if not sections:
        return ai_tips_text
    
    # Generuj markdown dla Streamlit
    result_parts = []
    
    for section_title, items in sections:
        # Wybierz emoji na podstawie tytu≥u sekcji
        icon = '??'
        title_lower = section_title.lower()
        if 'warunki' in title_lower or 'optymalne' in title_lower:
            icon = '??'
        elif 'mocn' in title_lower or 'wzmacnia' in title_lower or 'siln' in title_lower:
            icon = '??'
        elif 'rozwÛj' in title_lower or 'rozwija' in title_lower or 's≥ab' in title_lower or 'obszar' in title_lower:
            icon = '??'
        
        # Dodaj nag≥Ûwek sekcji
        result_parts.append(f"\n#### {icon} {section_title}\n")
        
        # Dodaj punkty
        for item in items:
            # Sprawdü czy punkt ma bold prefix **Tekst:**
            bold_prefix_match = re.match(r'^\*\*(.+?)\*\*:\s*(.+)', item)
            
            if bold_prefix_match:
                # Punkt ma bold prefix
                bold_text = bold_prefix_match.group(1).strip()
                rest_text = bold_prefix_match.group(2).strip()
                result_parts.append(f"- **{bold_text}:** {rest_text}")
            else:
                # Zwyk≥y punkt - zostaw **bold** jak jest
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
    username = st.session_state.get('username', 'Uøytkownik')
    
    # Przygotuj dane dla wykresÛw
    ability_info = {
        "CE": {"name": "Konkretne Doúwiadczenie", "emoji": "??", "color": "#E74C3C", "desc": "Feeling"},
        "RO": {"name": "Refleksyjna Obserwacja", "emoji": "???", "color": "#4A90E2", "desc": "Watching"},
        "AC": {"name": "Abstrakcyjna Konceptualizacja", "emoji": "??", "color": "#9B59B6", "desc": "Thinking"},
        "AE": {"name": "Aktywne Eksperymentowanie", "emoji": "??", "color": "#2ECC71", "desc": "Doing"}
    }
    
    # Wygeneruj wykres s≥upkowy jako HTML (Plotly offline)
    abilities_order = ['CE', 'RO', 'AC', 'AE']
    scores = [results[a] for a in abilities_order]
    colors = [ability_info[a]['color'] for a in abilities_order]
    
    # Etykiety w dwÛch liniach dla lepszej czytelnoúci
    labels_multiline = [
        'Konkretne<br>Doúwiadczenie',
        'Refleksyjna<br>Obserwacja',
        'Abstrakcyjna<br>Konceptualizacja',
        'Aktywne<br>Eksperymentowanie'
    ]
    
    # Wykres s≥upkowy
    fig_bar = go.Figure(data=[
        go.Bar(
            x=labels_multiline,  # Etykiety w dwÛch liniach
            y=scores,
            marker=dict(color=colors),
            text=scores,
            textposition='outside',
            textfont=dict(size=16, color='#333')
        )
    ])
    fig_bar.update_layout(
        title='Zdolnoúci Podstawowe w Cyklu Kolba',
        xaxis=dict(tickangle=0, tickfont=dict(size=12)),  # Poziome etykiety
        yaxis=dict(title='Wynik (punkty)', range=[0, 13]),
        width=650,  # Fixed width - bezpieczna szerokoúÊ dla A4
        height=350,  # ZwiÍkszone z 300 dla etykiet X
        margin=dict(t=50, b=80, l=50, r=40),  # Zmniejszony dolny margines (etykiety 2-liniowe)
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Konwertuj wykres do HTML (inline, bez CDN)
    bar_chart_html = fig_bar.to_html(
        include_plotlyjs='inline',  # Osadü plotly.js w HTML
        div_id='bar_chart',
        config={'displayModeBar': False}  # Ukryj toolbar
    )
    
    # Wygeneruj wykres siatki
    x_coord = dimensions['AE-RO']
    y_coord = dimensions['AC-CE']
    
    fig_grid = go.Figure()
    
    # Dodaj t≥o Êwiartek
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
    
    # Dodaj punkt uøytkownika
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
        title='Siatka StylÛw Uczenia siÍ',
        xaxis=dict(title='Przetwarzanie (AE - RO)', range=[-13, 13]),
        yaxis=dict(title='Postrzeganie (AC - CE)', range=[-13, 13]),
        width=650,  # Fixed width - bezpieczna szerokoúÊ dla A4
        height=400,  
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=60, b=60, l=70, r=70)  # WiÍksze boczne marginesy
    )
    
    # Konwertuj wykres siatki do HTML
    grid_chart_html = fig_grid.to_html(
        include_plotlyjs=False,  # Plotly.js juø jest w pierwszym wykresie
        div_id='grid_chart',
        config={'displayModeBar': False, 'responsive': True}  # Responsive
    )
    
    # Opisy stylÛw
    style_descriptions = {
        "Diverging (Dywergent)": {
            "icon": "??",
            "desc": "Uczysz siÍ poprzez obserwacjÍ i refleksjÍ. Preferujesz kreatywne podejúcie i wieloúÊ perspektyw.",
            "strengths": "KreatywnoúÊ, empatia, wyobraünia, generowanie pomys≥Ûw",
            "development": "Praca w grupach, burze mÛzgÛw, case studies, dyskusje"
        },
        "Assimilating (Asymilator)": {
            "icon": "??",
            "desc": "Uczysz siÍ poprzez logiczne myúlenie i teoriÍ. Preferujesz systematyczne podejúcie.",
            "strengths": "Analiza, organizacja informacji, myúlenie konceptualne",
            "development": "Wyk≥ady, czytanie, badania, modele teoretyczne"
        },
        "Converging (Konwergent)": {
            "icon": "??",
            "desc": "Uczysz siÍ poprzez praktyczne zastosowanie teorii. Preferujesz rozwiπzywanie konkretnych problemÛw.",
            "strengths": "Rozwiπzywanie problemÛw, podejmowanie decyzji, praktyczne zastosowania",
            "development": "∆wiczenia praktyczne, symulacje, eksperymenty, projekty"
        },
        "Accommodating (Akomodator)": {
            "icon": "?",
            "desc": "Uczysz siÍ poprzez dzia≥anie i eksperymentowanie. Preferujesz intuicyjne podejúcie.",
            "strengths": "Adaptacja, dzia≥anie, branie ryzyka, realizacja planÛw",
            "development": "Praktyka w terenie, trial-and-error, projekty terenowe"
        }
    }
    
    style_info = style_descriptions.get(dominant, style_descriptions["Diverging (Dywergent)"])
    
    # SzczegÛ≥owe opisy stylÛw (pe≥na wersja dla PDF)
    detailed_style_descriptions = {
        "Diverging (Dywergent)": {
            "icon": "??",
            "quadrant": "CE/RO",
            "description": "£πczysz Konkretne Doúwiadczenie i Refleksyjnπ ObserwacjÍ. Jesteú wraøliwy i potrafisz spojrzeÊ na sytuacje z wielu rÛønych perspektyw. Twoja g≥Ûwna mocna strona to wyobraünia i zdolnoúÊ do generowania wielu pomys≥Ûw.",
            "strengths": ["Wyobraünia i kreatywnoúÊ", "ZdolnoúÊ do widzenia sytuacji z rÛønych perspektyw", "Empatia i wraøliwoúÊ", "Doskona≥oúÊ w burzy mÛzgÛw i generowaniu pomys≥Ûw", "UmiejÍtnoúÊ integracji rÛønych obserwacji"],
            "weaknesses": ["Trudnoúci z podejmowaniem szybkich decyzji", "Problemy z przek≥adaniem teorii na dzia≥anie", "Tendencja do nadmiernego analizowania"],
            "careers": "Doradztwo, sztuka, HR, psychologia, dziennikarstwo",
            "learning_methods": "Studia przypadkÛw, dyskusje grupowe, feedback, introspekcja, obserwacja dzia≥ania innych"
        },
        "Assimilating (Asymilator)": {
            "icon": "??",
            "quadrant": "AC/RO",
            "description": "£πczysz Abstrakcyjnπ KonceptualizacjÍ i Refleksyjnπ ObserwacjÍ. Preferujesz zwiÍz≥e, logiczne i systematyczne podejúcie. Wykazujesz duøπ zdolnoúÊ do tworzenia modeli teoretycznych i scalania licznych obserwacji w zintegrowane wyjaúnienia.",
            "strengths": ["Tworzenie modeli teoretycznych", "Logiczne i systematyczne myúlenie", "Precyzja i spÛjnoúÊ teorii", "ZdolnoúÊ do scalania wielu obserwacji", "Planowanie strategiczne"],
            "weaknesses": ["Mniejsze zainteresowanie problemami praktycznymi", "Trudnoúci w pracy z ludümi", "Preferencja teorii nad zastosowaniem"],
            "careers": "Nauka, informatyka, planowanie strategiczne, badania, matematyka",
            "learning_methods": "Wyk≥ady teoretyczne, modele i schematy, analiza koncepcji, dociekliwe pytania, prace nad systemami"
        },
        "Converging (Konwergent)": {
            "icon": "??",
            "quadrant": "AC/AE",
            "description": "£πczysz Abstrakcyjnπ KonceptualizacjÍ i Aktywne Eksperymentowanie. Doskonale radzisz sobie z praktycznym zastosowaniem teorii do rozwiπzywania konkretnych problemÛw. Skupiasz siÍ na zadaniach i rzeczach, a nie na kwestiach miÍdzyludzkich.",
            "strengths": ["Praktyczne zastosowanie teorii", "EfektywnoúÊ i sprawnoúÊ dzia≥ania", "ZdolnoúÊ do podejmowania decyzji", "UmiejÍtnoúci techniczne", "Rozwiπzywanie konkretnych problemÛw"],
            "weaknesses": ["Mniejsze zainteresowanie relacjami miÍdzyludzkimi", "Skupienie na zadaniach kosztem ludzi", "Preferencja dla jednoznacznych rozwiπzaÒ"],
            "careers": "Inøynieria, technologia, medycyna, ekonomia, zawody techniczne",
            "learning_methods": "∆wiczenia praktyczne, wdroøenia, testowanie umiejÍtnoúci, konkretne przyk≥ady zawodowe, zadania aplikacyjne"
        },
        "Accommodating (Akomodator)": {
            "icon": "?",
            "quadrant": "CE/AE",
            "description": "£πczysz Konkretne Doúwiadczenie i Aktywne Eksperymentowanie. To styl 'hands-on', ktÛry polega na intuicji. Jesteú elastyczny, zdolny do wprowadzania planÛw w øycie, chÍtnie eksperymentujesz i adaptujesz siÍ do nowych warunkÛw.",
            "strengths": ["ElastycznoúÊ i adaptacja", "Podejmowanie ryzyka", "Szybka reakcja na zmiany", "Osobiste zaangaøowanie", "UmiejÍtnoúÊ wprowadzania planÛw w øycie"],
            "weaknesses": ["Tendencja do dzia≥ania bez planu", "NiecierpliwoúÊ wobec teorii", "Ryzyko podejmowania pochopnych decyzji"],
            "careers": "Zarzπdzanie operacyjne, sprzedaø, marketing, przedsiÍbiorczoúÊ",
            "learning_methods": "Gry, symulacje, rÛønorodne Êwiczenia, odgrywanie rÛl, zadania niestandardowe wymagajπce ryzyka"
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
                gap: 15px;  /* Mniejsza przerwa miÍdzy kartami */
                margin-bottom: 30px;
            }}
            
            .ability-card {{
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px 10px;  /* Mniejszy padding dla wÍøszych kart */
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
            
            /* Style dla kompaktowych wskazÛwek AI */
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
            
            /* Style dla wykresÛw Plotly */
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
                
                /* Karty zdolnoúci - kompaktowe w druku */
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
                    max-width: 680px !important;  /* SzerokoúÊ dopasowana do wykresÛw */
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
                
                /* Kontenery wykresÛw */
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
        <button class="print-button" onclick="window.print()">??? Drukuj / Zapisz jako PDF</button>
        
        <div class="header">
            <h1>?? Raport Kolb Learning Style Inventory</h1>
            <p>Uøytkownik: {username}</p>
            <p>Data: {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
        </div>
        
        <div class="section">
            <h2 class="section-title">?? Twoje Zdolnoúci Uczenia siÍ</h2>
            
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
            <h2 class="section-title">?? Wizualizacja WynikÛw</h2>
            <div class="chart-container" style="max-width: 95%; margin: 0 auto;">
                {bar_chart_html}
            </div>
        </div>
        
        <div class="section" style="page-break-before: always;">
            <h2 class="section-title">?? TwÛj Dominujπcy Styl Uczenia siÍ</h2>
            
            <div class="dominant-style">
                <h2>{detailed_style_info['icon']} {dominant}</h2>
                <p><strong>∆wiartka:</strong> {detailed_style_info['quadrant']}</p>
                <p style="margin-top: 15px; font-size: 16px; line-height: 1.8;">{detailed_style_info['description']}</p>
            </div>
            
            <div class="chart-container" style="max-width: 95%; margin: 0 auto;">
                {grid_chart_html}
            </div>
            
            <div class="two-column" style="margin-top: 30px;">
                <div class="info-box" style="border-left-color: #2ECC71; background: linear-gradient(135deg, rgba(46, 204, 113, 0.1) 0%, rgba(39, 174, 96, 0.1) 100%);">
                    <h3 style="color: #2ECC71;">?? Twoje mocne strony:</h3>
                    <ul style="margin: 10px 0; padding-left: 20px; line-height: 1.8;">
                        {''.join([f'<li>{s}</li>' for s in detailed_style_info['strengths']])}
                    </ul>
                </div>
                
                <div class="info-box" style="border-left-color: #E67E22; background: linear-gradient(135deg, rgba(230, 126, 34, 0.1) 0%, rgba(211, 84, 0, 0.1) 100%);">
                    <h3 style="color: #E67E22;">?? Obszary do rozwoju:</h3>
                    <ul style="margin: 10px 0; padding-left: 20px; line-height: 1.8;">
                        {''.join([f'<li>{w}</li>' for w in detailed_style_info['weaknesses']])}
                    </ul>
                </div>
            </div>
            
            <div class="two-column" style="margin-top: 20px;">
                <div class="info-box" style="border-left-color: #3498DB;">
                    <h3 style="color: #3498DB;">?? Typowe zawody:</h3>
                    <p>{detailed_style_info['careers']}</p>
                </div>
                
                <div class="info-box" style="border-left-color: #9B59B6;">
                    <h3 style="color: #9B59B6;">?? Rekomendowane metody uczenia siÍ:</h3>
                    <p>{detailed_style_info['learning_methods']}</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">?? ElastycznoúÊ Uczenia siÍ</h2>
            
            <div class="flexibility-meter">
                <div class="score">{flexibility:.1f}%</div>
                <p>Twoja elastycznoúÊ w uczeniu siÍ</p>
                <p style="color: #666; font-size: 14px;">
                    {"?? Wysoka elastycznoúÊ! Potrafisz ≥πczyÊ rÛøne style uczenia siÍ." if flexibility > 70 
                     else "? Dobra elastycznoúÊ. Masz zrÛwnowaøone podejúcie." if flexibility > 50
                     else "?? Silne preferencje w okreúlonym stylu. Rozwaø rozwijanie innych zdolnoúci."}
                </p>
            </div>
            
            <div class="info-box">
                <h3>?? Twoja pozycja na siatce</h3>
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
            <h2 class="section-title">? Wymiary Liczbowe (LSI Dimensions)</h2>
            
            <div class="abilities-grid" style="grid-template-columns: repeat(3, 1fr);">
                <div class="ability-card" style="border-left: 5px solid #667eea; background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);">
                    <h3>Oú Postrzegania</h3>
                    <div style="color: #666; font-size: 14px; margin: 5px 0;">AC-CE</div>
                    <div class="score" style="color: #667eea">{dimensions['AC-CE']:+d}</div>
                    <div style="color: #666; font-size: 14px;">{'Preferencja: Myúlenie (AC)' if dimensions['AC-CE'] > 0 else 'Preferencja: Czucie (CE)'}</div>
                </div>
                
                <div class="ability-card" style="border-left: 5px solid #f5576c; background: linear-gradient(135deg, rgba(240, 147, 251, 0.1) 0%, rgba(245, 87, 108, 0.1) 100%);">
                    <h3>Oú Przetwarzania</h3>
                    <div style="color: #666; font-size: 14px; margin: 5px 0;">AE-RO</div>
                    <div class="score" style="color: #f5576c">{dimensions['AE-RO']:+d}</div>
                    <div style="color: #666; font-size: 14px;">{'Preferencja: Dzia≥anie (AE)' if dimensions['AE-RO'] > 0 else 'Preferencja: Obserwacja (RO)'}</div>
                </div>
                
                <div class="ability-card" style="border-left: 5px solid #38f9d7; background: linear-gradient(135deg, rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%);">
                    <h3>ElastycznoúÊ</h3>
                    <div style="color: #666; font-size: 14px; margin: 5px 0;">Learning Flexibility</div>
                    <div class="score" style="color: #38f9d7">{flexibility:.0f}%</div>
                    <div style="color: #666; font-size: 14px;">{'Wysoka - ZrÛwnowaøony' if flexibility > 60 else 'årednia - Umiarkowana' if flexibility > 30 else 'Niska - Wyraüna preferencja'}</div>
                </div>
            </div>
            
            <div class="info-box" style="margin-top: 20px;">
                <h3>?? Interpretacja wymiarÛw:</h3>
                <p><strong>AC-CE (Postrzeganie):</strong> Pokazuje jak preferujesz postrzegaÊ informacje - poprzez abstrakcyjne myúlenie (AC) czy konkretne doúwiadczenie (CE).</p>
                <p><strong>AE-RO (Przetwarzanie):</strong> Pokazuje jak preferujesz przetwarzaÊ informacje - poprzez aktywne eksperymentowanie (AE) czy refleksyjnπ obserwacjÍ (RO).</p>
                <p><strong>ElastycznoúÊ:</strong> Im bliøej centrum siatki, tym wiÍksza elastycznoúÊ w prze≥πczaniu miÍdzy stylami uczenia siÍ.</p>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">??? Rekomendacje Rozwojowe</h2>
            
            <div class="info-box" style="border-left-color: #2ECC71;">
                <h3>? Co robiÊ wiÍcej:</h3>
                <p>{style_info['development']}</p>
            </div>
            
            <div class="info-box" style="border-left-color: #E74C3C;">
                <h3>?? Obszary do rozwiniÍcia:</h3>
                <p>Rozwaø Êwiczenie pozosta≥ych stylÛw uczenia siÍ, aby zwiÍkszyÊ swojπ elastycznoúÊ i efektywnoúÊ.</p>
            </div>
        </div>
        """
    
    # Dodaj sekcjÍ AI jeúli jest dostÍpna
    ai_section = ""
    if st.session_state.get('kolb_profession') and st.session_state.get('kolb_ai_tips'):
        profession = st.session_state.kolb_profession
        ai_tips_raw = st.session_state.kolb_ai_tips
        
        # Parsuj wskazÛwki AI na sekcje (taka sama logika jak w Streamlit)
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
                clean_line = re.sub(r'^[-ï*]\s*', '', line_stripped)
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
                icon = '??'
                bg = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                text_color = 'white'
            elif 'mocn' in section_title.lower() or 'wzmacnia' in section_title.lower():
                icon = '??'
                bg = 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
                text_color = 'white'
            elif 'rozwÛj' in section_title.lower() or 'rozwija' in section_title.lower():
                icon = '??'
                bg = 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
                text_color = '#333'
            else:
                icon = '??'
                bg = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
                text_color = 'white'
            
            # Buduj HTML dla punktÛw z numeracjπ
            items_html = "<ol style='margin: 10px 0 0 20px; padding-left: 0;'>"
            for item in items:
                # ZamieÒ **tekst** na <strong>tekst</strong>
                formatted_item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                items_html += f"<li style='margin: 10px 0; line-height: 1.6;'>{formatted_item}</li>"
            items_html += "</ol>"
            
            # Dodaj kartÍ z klasπ dla zachowania kolorÛw w druku
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
            <h2 class="section-title">?? Jak UczyÊ siÍ Efektywnie</h2>
            
            <div class='ai-header-color' style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; 
                        padding: 15px 20px; 
                        border-radius: 10px; 
                        margin-bottom: 20px;
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                        color-adjust: exact;">
                <p style="margin: 0; font-size: 16px;"><strong>?? ZawÛd:</strong> {profession} | <strong>?? Styl uczenia siÍ:</strong> {dominant}</p>
            </div>
            
            {ai_cards_html}
            
            <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; border-radius: 5px; margin-top: 20px;">
                <p style="margin: 0; font-size: 13px; color: #1565c0;"><strong>?? PamiÍtaj:</strong> Te wskazÛwki sπ dopasowane do Twojego stylu uczenia siÍ. Testuj je w praktyce i obserwuj co dzia≥a najlepiej w Twojej sytuacji.</p>
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
    
    # ZwrÛÊ HTML - przeglπdarka uøytkownika wygeneruje PDF
    return html_content

def display_kolb_results():
    """Wyúwietla wyniki testu Kolba zgodnie z metodologiπ ELT"""
    st.markdown("---")
    st.markdown("## ?? Twoje wyniki - Kolb Experiential Learning Profile")
    
    results = st.session_state.kolb_results
    dimensions = st.session_state.kolb_dimensions
    dominant = st.session_state.kolb_dominant
    quadrant = st.session_state.kolb_quadrant
    flexibility = st.session_state.kolb_flexibility
    
    # Wyúwietl wyniki dla czterech zdolnoúci uczenia siÍ
    st.markdown("### ?? Twoje zdolnoúci uczenia siÍ")
    cols = st.columns(4)
    
    ability_info = {
        "CE": {"name": "Konkretne Doúwiadczenie", "emoji": "??", "color": "#E74C3C", "desc": "Feeling"},
        "RO": {"name": "Refleksyjna Obserwacja", "emoji": "???", "color": "#4A90E2", "desc": "Watching"},
        "AC": {"name": "Abstrakcyjna Konceptualizacja", "emoji": "??", "color": "#9B59B6", "desc": "Thinking"},
        "AE": {"name": "Aktywne Eksperymentowanie", "emoji": "??", "color": "#2ECC71", "desc": "Doing"}
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
    
    # Wizualizacja 1: Wykres S≥upkowy dla Zdolnoúci Podstawowych
    st.markdown("---")
    st.markdown("### ?? Wykres Zdolnoúci Podstawowych (Bar Chart)")
    st.markdown("*Twoje preferencje do poszczegÛlnych etapÛw Cyklu Kolba*")
    
    # Przygotuj dane do wykresu s≥upkowego
    abilities_order = ['CE', 'RO', 'AC', 'AE']
    ability_labels = {
        'CE': 'Konkretne Doúwiadczenie<br>(Feeling)',
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
            text='Zdolnoúci Podstawowe w Cyklu Kolba',
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
    
    st.plotly_chart(fig_bar, width="stretch")
    
    # Interpretacja wykresu s≥upkowego
    strongest = max(results.items(), key=lambda x: x[1])
    weakest = min(results.items(), key=lambda x: x[1])
    
    col_int1, col_int2 = st.columns(2)
    with col_int1:
        st.success(f"**?? Twoja najsilniejsza zdolnoúÊ:** {ability_info[strongest[0]]['name']} ({strongest[1]}/12)")
    with col_int2:
        st.warning(f"**?? Obszar do rozwoju:** {ability_info[weakest[0]]['name']} ({weakest[1]}/12)")
    
    # Wizualizacja 2: Siatka StylÛw Uczenia siÍ (Learning Style Grid)
    st.markdown("---")
    st.markdown("### ?? Siatka StylÛw Uczenia siÍ (Learning Style Grid)")
    st.markdown("*Twoja pozycja w matrycy stylÛw ELT - im bliøej úrodka, tym wiÍksza elastycznoúÊ*")
    
    # Pobierz wspÛ≥rzÍdne
    x_coord = dimensions['AE-RO']  # Oú pozioma (Przetwarzanie)
    y_coord = dimensions['AC-CE']  # Oú pionowa (Postrzeganie)
    
    # UtwÛrz wykres siatki
    fig_grid = go.Figure()
    
    # Dodaj t≥o Êwiartek z nazwami stylÛw
    quadrant_info = {
        'Diverging': {'x': [-12, 0], 'y': [-12, 0], 'color': 'rgba(231, 76, 60, 0.15)', 'label_x': -6, 'label_y': -6},
        'Assimilating': {'x': [-12, 0], 'y': [0, 12], 'color': 'rgba(155, 89, 182, 0.15)', 'label_x': -6, 'label_y': 6},
        'Converging': {'x': [0, 12], 'y': [0, 12], 'color': 'rgba(52, 152, 219, 0.15)', 'label_x': 6, 'label_y': 6},
        'Accommodating': {'x': [0, 12], 'y': [-12, 0], 'color': 'rgba(46, 204, 113, 0.15)', 'label_x': 6, 'label_y': -6}
    }
    
    # Rysuj prostokπty Êwiartek
    for style_name, info in quadrant_info.items():
        fig_grid.add_shape(
            type="rect",
            x0=info['x'][0], x1=info['x'][1],
            y0=info['y'][0], y1=info['y'][1],
            fillcolor=info['color'],
            line=dict(width=0)
        )
        
        # Dodaj etykiety stylÛw
        fig_grid.add_annotation(
            x=info['label_x'], y=info['label_y'],
            text=f"<b>{style_name}</b>",
            showarrow=False,
            font=dict(size=14, color='rgba(0,0,0,0.5)', family='Arial Black'),
            xanchor='center',
            yanchor='middle'
        )
    
    # Strefa ZrÛwnowaøonego Uczenia siÍ (centralna)
    balanced_zone_radius = 4
    theta = [i for i in range(0, 361, 10)]
    balanced_x = [balanced_zone_radius * math.cos(math.radians(t)) for t in theta]
    balanced_y = [balanced_zone_radius * math.sin(math.radians(t)) for t in theta]
    
    fig_grid.add_trace(go.Scatter(
        x=balanced_x, y=balanced_y,
        fill='toself',
        fillcolor='rgba(255, 193, 7, 0.2)',
        line=dict(color='rgba(255, 193, 7, 0.6)', width=2, dash='dash'),
        name='Strefa ZrÛwnowaøonego<br>Uczenia siÍ',
        hoverinfo='name',
        showlegend=True
    ))
    
    # Osie
    fig_grid.add_shape(type="line", x0=-12, x1=12, y0=0, y1=0, 
                       line=dict(color="rgba(0,0,0,0.4)", width=2))
    fig_grid.add_shape(type="line", x0=0, x1=0, y0=-12, y1=12, 
                       line=dict(color="rgba(0,0,0,0.4)", width=2))
    
    # Punkt uøytkownika
    fig_grid.add_trace(go.Scatter(
        x=[x_coord], y=[y_coord],
        mode='markers+text',
        marker=dict(
            size=20,
            color='#FF5722',
            line=dict(color='white', width=3),
            symbol='circle'
        ),
        text=['TW”J<br>WYNIK'],
        textposition='top center',
        textfont=dict(size=12, color='#FF5722', family='Arial Black'),
        name='Twoja pozycja',
        hovertemplate=f'<b>Twoja pozycja</b><br>AE-RO: {x_coord:+d}<br>AC-CE: {y_coord:+d}<br>ElastycznoúÊ: {flexibility:.0f}%<extra></extra>'
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
            text=f'TwÛj Styl: {dominant} | ElastycznoúÊ: {flexibility:.0f}%',
            font=dict(size=18, color='#333', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='<b>Oú Przetwarzania (AE-RO)</b>',
            range=[-14, 14],
            zeroline=False,
            gridcolor='rgba(0,0,0,0.1)',
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            title='<b>Oú Postrzegania (AC-CE)</b>',
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
    
    st.plotly_chart(fig_grid, width="stretch")
    
    # Interpretacja siatki
    distance_from_center = math.sqrt(x_coord**2 + y_coord**2)
    
    if distance_from_center <= 4:
        interpretation_color = "success"
        interpretation = f"?? **Gratulacje!** TwÛj wynik znajduje siÍ w **Strefie ZrÛwnowaøonego Uczenia siÍ**. Oznacza to wysokπ elastycznoúÊ i zdolnoúÊ do wykorzystania wszystkich faz cyklu Kolba w zaleønoúci od sytuacji."
    elif distance_from_center <= 8:
        interpretation_color = "info"
        interpretation = f"? **Umiarkowana preferencja** - TwÛj styl jest wyraünie okreúlony ({dominant}), ale zachowujesz dobrπ elastycznoúÊ. Moøesz efektywnie adaptowaÊ siÍ do rÛønych sytuacji uczenia siÍ."
    else:
        interpretation_color = "warning"
        interpretation = f"?? **Silna preferencja** - TwÛj wynik znajduje siÍ daleko od centrum siatki, co wskazuje na wyraünπ tendencjÍ do stylu **{dominant}**. Rozwaø celowe rozwijanie s≥abszych zdolnoúci, aby zwiÍkszyÊ elastycznoúÊ uczenia siÍ."
    
    if interpretation_color == "success":
        st.success(interpretation)
    elif interpretation_color == "info":
        st.info(interpretation)
    else:
        st.warning(interpretation)
    
    # Wymiary liczbowe
    st.markdown("---")
    st.markdown("### ?? Wymiary Liczbowe (LSI Dimensions)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 12px; text-align: center; color: white;'>
            <h4 style='color: white; margin-bottom: 10px;'>Oú Postrzegania</h4>
            <p style='font-size: 0.9em; margin: 5px 0;'>AC-CE</p>
            <div style='font-size: 2em; font-weight: bold; margin: 10px 0;'>{dimensions['AC-CE']:+d}</div>
            <p style='font-size: 0.85em;'>{'Preferencja: Myúlenie (AC)' if dimensions['AC-CE'] > 0 else 'Preferencja: Czucie (CE)'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='padding: 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    border-radius: 12px; text-align: center; color: white;'>
            <h4 style='color: white; margin-bottom: 10px;'>Oú Przetwarzania</h4>
            <p style='font-size: 0.9em; margin: 5px 0;'>AE-RO</p>
            <div style='font-size: 2em; font-weight: bold; margin: 10px 0;'>{dimensions['AE-RO']:+d}</div>
            <p style='font-size: 0.85em;'>{'Preferencja: Dzia≥anie (AE)' if dimensions['AE-RO'] > 0 else 'Preferencja: Obserwacja (RO)'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        flex_color = "#2ECC71" if flexibility > 60 else "#F39C12" if flexibility > 30 else "#E74C3C"
        st.markdown(f"""
        <div style='padding: 20px; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    border-radius: 12px; text-align: center; color: white;'>
            <h4 style='color: white; margin-bottom: 10px;'>ElastycznoúÊ</h4>
            <p style='font-size: 0.9em; margin: 5px 0;'>Learning Flexibility</p>
            <div style='font-size: 2em; font-weight: bold; margin: 10px 0;'>{flexibility:.0f}%</div>
            <p style='font-size: 0.85em;'>{'Wysoka - ZrÛwnowaøony profil' if flexibility > 60 else 'årednia - Umiarkowana' if flexibility > 30 else 'Niska - Wyraüna preferencja'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Wyúwietl dominujπcy styl
    st.markdown("---")
    st.markdown(f"### ? TwÛj dominujπcy styl: **{dominant}**")
    st.markdown(f"**∆wiartka:** {quadrant}")
    
    # Opisy stylÛw zgodnie z dokumentacjπ naukowπ
    style_descriptions = {
        "Diverging (Dywergent)": {
            "quadrant": "CE/RO",
            "description": "£πczysz Konkretne Doúwiadczenie i Refleksyjnπ ObserwacjÍ. Jesteú wraøliwy i potrafisz spojrzeÊ na sytuacje z wielu rÛønych perspektyw. Twoja g≥Ûwna mocna strona to wyobraünia i zdolnoúÊ do generowania wielu pomys≥Ûw.",
            "strengths": [
                "Wyobraünia i kreatywnoúÊ",
                "ZdolnoúÊ do widzenia sytuacji z rÛønych perspektyw",
                "Empatia i wraøliwoúÊ",
                "Doskona≥oúÊ w burzy mÛzgÛw i generowaniu pomys≥Ûw",
                "UmiejÍtnoúÊ integracji rÛønych obserwacji"
            ],
            "weaknesses": [
                "Trudnoúci z podejmowaniem szybkich decyzji",
                "Problemy z przek≥adaniem teorii na dzia≥anie",
                "Tendencja do nadmiernego analizowania"
            ],
            "careers": "Doradztwo, sztuka, HR, psychologia, dziennikarstwo",
            "learning_methods": "Studia przypadkÛw, dyskusje grupowe, feedback, introspekcja, obserwacja dzia≥ania innych"
        },
        "Assimilating (Asymilator)": {
            "quadrant": "AC/RO",
            "description": "£πczysz Abstrakcyjnπ KonceptualizacjÍ i Refleksyjnπ ObserwacjÍ. Preferujesz zwiÍz≥e, logiczne i systematyczne podejúcie. Wykazujesz duøπ zdolnoúÊ do tworzenia modeli teoretycznych i scalania licznych obserwacji w zintegrowane wyjaúnienia.",
            "strengths": [
                "Tworzenie modeli teoretycznych",
                "Logiczne i systematyczne myúlenie",
                "Precyzja i spÛjnoúÊ teorii",
                "ZdolnoúÊ do scalania wielu obserwacji",
                "Planowanie strategiczne"
            ],
            "weaknesses": [
                "Mniejsze zainteresowanie problemami praktycznymi",
                "Trudnoúci w pracy z ludümi",
                "Preferencja teorii nad zastosowaniem"
            ],
            "careers": "Nauka, informatyka, planowanie strategiczne, badania, matematyka",
            "learning_methods": "Wyk≥ady teoretyczne, modele i schematy, analiza koncepcji, dociekliwe pytania, prace nad systemami"
        },
        "Converging (Konwergent)": {
            "quadrant": "AC/AE",
            "description": "£πczysz Abstrakcyjnπ KonceptualizacjÍ i Aktywne Eksperymentowanie. Doskonale radzisz sobie z praktycznym zastosowaniem teorii do rozwiπzywania konkretnych problemÛw. Skupiasz siÍ na zadaniach i rzeczach, a nie na kwestiach miÍdzyludzkich.",
            "strengths": [
                "Praktyczne zastosowanie teorii",
                "EfektywnoúÊ i sprawnoúÊ dzia≥ania",
                "ZdolnoúÊ do podejmowania decyzji",
                "UmiejÍtnoúci techniczne",
                "Rozwiπzywanie konkretnych problemÛw"
            ],
            "weaknesses": [
                "Mniejsze zainteresowanie relacjami miÍdzyludzkimi",
                "Skupienie na zadaniach kosztem ludzi",
                "Preferencja dla jednoznacznych rozwiπzaÒ"
            ],
            "careers": "Inøynieria, technologia, medycyna, ekonomia, zawody techniczne",
            "learning_methods": "∆wiczenia praktyczne, wdroøenia, testowanie umiejÍtnoúci, konkretne przyk≥ady zawodowe, zadania aplikacyjne"
        },
        "Accommodating (Akomodator)": {
            "quadrant": "CE/AE",
            "description": "£πczysz Konkretne Doúwiadczenie i Aktywne Eksperymentowanie. To styl 'hands-on', ktÛry polega na intuicji. Jesteú elastyczny, zdolny do wprowadzania planÛw w øycie, chÍtnie eksperymentujesz i adaptujesz siÍ do nowych warunkÛw.",
            "strengths": [
                "ElastycznoúÊ i adaptacja",
                "Podejmowanie ryzyka",
                "Szybka reakcja na zmiany",
                "Osobiste zaangaøowanie",
                "UmiejÍtnoúÊ wprowadzania planÛw w øycie"
            ],
            "weaknesses": [
                "Tendencja do dzia≥ania bez planu",
                "NiecierpliwoúÊ wobec teorii",
                "Ryzyko podejmowania pochopnych decyzji"
            ],
            "careers": "Zarzπdzanie operacyjne, sprzedaø, marketing, przedsiÍbiorczoúÊ",
            "learning_methods": "Gry, symulacje, rÛønorodne Êwiczenia, odgrywanie rÛl, zadania niestandardowe wymagajπce ryzyka"
        }
    }
    
    desc = style_descriptions[dominant]
    
    # G≥Ûwna karta z opisem stylu
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                box-shadow: 0 4px 15px rgba(102,126,234,0.4); 
                border-radius: 20px; 
                padding: 30px; 
                margin: 25px 0; 
                color: white;'>
        <div style='font-size: 2.5em; margin-bottom: 10px;'>??</div>
        <h4 style='color: white; margin: 0 0 15px 0;'>TwÛj Styl Uczenia siÍ</h4>
        <p style='font-size: 1.15em; line-height: 1.8; margin: 0;'>
            {desc['description']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # SzczegÛ≥owe karty w 2 kolumnach
    col1, col2 = st.columns(2)
    
    with col1:
        # Karta mocnych stron
        strengths_html = "<br>".join([f"? {s}" for s in desc['strengths']])
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
        
        # Karta zawodÛw
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
        # Karta obszarÛw rozwoju
        weaknesses_html = "<br>".join([f"?? {w}" for w in desc['weaknesses']])
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
    
    # Karta ze strategiπ rozwoju elastycznoúci
    st.markdown("---")
    
    # Identyfikacja s≥abych zdolnoúci
    weak_abilities = [ability for ability, score in results.items() if score < 4]
    strong_abilities = [ability for ability, score in results.items() if score > 8]
    
    if weak_abilities:
        weak_abilities_names = ', '.join([ability_info[a]['name'] for a in weak_abilities])
        weak_tips_html = "<br>".join([f"ï Dla <b>{ability_info[a]['name']} ({a})</b>: Êwicz {ability_info[a]['desc'].lower()}" for a in weak_abilities])
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%); 
                    box-shadow: 0 3px 12px rgba(255,234,167,0.3); 
                    border-radius: 18px; 
                    padding: 25px; 
                    margin: 20px 0; 
                    color: #222;'>
            <div style='font-size: 2em; margin-bottom: 10px;'></div>
            <h4 style='margin: 0 0 15px 0; color: #e17055;'>Zdolnoúci do wzmocnienia</h4>
            <p style='margin: 0 0 15px 0; font-size: 1.05em;'>
                Twoje s≥absze zdolnoúci to: <b>{weak_abilities_names}</b>
            </p>
            <div style='background: rgba(255,255,255,0.3); 
                        border-radius: 10px; 
                        padding: 15px; 
                        margin-top: 15px;'>
                <p style='margin: 0 0 10px 0; font-weight: bold;'>?? Zalecenia rozwojowe:</p>
                <p style='margin: 0; line-height: 1.8;'>
                    Celowo angaøuj siÍ w sytuacje, ktÛre wymagajπ uøywania tych zdolnoúci:<br><br>
                    {weak_tips_html}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Karta z pe≥nym cyklem Kolba
    flexibility_message = "Im bliøej centrum siatki, tym wiÍksza zdolnoúÊ adaptacji do rÛønych sytuacji uczenia siÍ." if flexibility > 50 else "Rozwijaj s≥absze zdolnoúci, aby zwiÍkszyÊ elastycznoúÊ i efektywnoúÊ uczenia siÍ w rÛønych kontekstach."
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                box-shadow: 0 4px 15px rgba(102,126,234,0.4); 
                border-radius: 20px; 
                padding: 30px; 
                margin: 20px 0; 
                color: white;'>
        <div style='font-size: 2em; margin-bottom: 10px;'>??</div>
        <h4 style='color: white; margin: 0 0 20px 0;'>Pe≥ny Cykl Uczenia siÍ Kolba (ELT Cycle)</h4>
        <p style='font-size: 1.05em; line-height: 1.7; margin-bottom: 20px;'>
            Najbardziej efektywne uczenie siÍ wykorzystuje <b>wszystkie cztery fazy</b> w cyklu:
        </p>
        <div style='background: rgba(255,255,255,0.15); 
                    border-radius: 12px; 
                    padding: 20px; 
                    margin: 15px 0;'>
            <ol style='margin: 0; padding-left: 20px; line-height: 2;'>
                <li><b>Konkretne Doúwiadczenie (CE)</b> õ ZetkniÍcie siÍ z nowπ sytuacjπ (Feeling)</li>
                <li><b>Refleksyjna Obserwacja (RO)</b> õ Obserwacja i refleksja (Watching)</li>
                <li><b>Abstrakcyjna Konceptualizacja (AC)</b> õ Tworzenie teorii (Thinking)</li>
                <li><b>Aktywne Eksperymentowanie (AE)</b> õ Testowanie w praktyce (Doing)</li>
            </ol>
        </div>
        <div style='background: rgba(255,193,7,0.3); 
                    border-left: 4px solid #FFC107; 
                    border-radius: 8px; 
                    padding: 15px; 
                    margin-top: 20px;'>
            <p style='margin: 0; font-size: 1.05em;'>
                <b>?? Kluczowa wskazÛwka:</b> TwÛj wynik elastycznoúci (<b>{flexibility:.0f}%</b>) pokazuje, 
                jak dobrze potrafisz prze≥πczaÊ siÍ miÍdzy stylami. {flexibility_message}
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sekcja AI - Praktyczne wskazÛwki dla zawodu
    st.markdown("---")
    st.markdown("### ?? AI: WskazÛwki praktyczne dla Twojego zawodu")
    st.markdown("Wybierz swÛj zawÛd, aby otrzymaÊ spersonalizowane wskazÛwki, jak wykorzystaÊ swÛj styl uczenia siÍ w praktyce:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("????? Trener", width="stretch", type="secondary", key="prof_trainer"):
            st.session_state.kolb_profession = "Trener"
            st.session_state.kolb_ai_generated = False
            st.rerun()
    
    with col2:
        if st.button("?? Menedøer", width="stretch", type="secondary", key="prof_manager"):
            st.session_state.kolb_profession = "Menedøer"
            st.session_state.kolb_ai_generated = False
            st.rerun()
    
    with col3:
        if st.button("?? Sprzedawca", width="stretch", type="secondary", key="prof_sales"):
            st.session_state.kolb_profession = "Sprzedawca"
            st.session_state.kolb_ai_generated = False
            st.rerun()
    
    # Wyúwietl wybrany zawÛd i wygeneruj wskazÛwki
    if 'kolb_profession' in st.session_state and st.session_state.kolb_profession:
        st.info(f"? Wybrany zawÛd: **{st.session_state.kolb_profession}**")
        
        # Wyúwietl wygenerowane wskazÛwki lub przycisk do generowania
        if st.session_state.get('kolb_ai_generated') and 'kolb_ai_tips' in st.session_state and st.session_state.kolb_ai_tips:
            st.markdown("---")
            st.markdown(f"### ?? Jak UczyÊ siÍ Efektywnie")
            
            # Header z zawodem i stylem
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; 
                        padding: 20px; 
                        border-radius: 15px; 
                        margin: 20px 0;
                        box-shadow: 0 4px 15px rgba(102,126,234,0.3);'>
                <h4 style='margin: 0; color: white;'>?? ZawÛd: {st.session_state.kolb_profession} | ?? Styl uczenia siÍ: {dominant}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Parsuj wskazÛwki AI na sekcje dla kart
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
                    clean_line = re.sub(r'^[-ï*]\s*', '', line_stripped)
                    clean_line = clean_line.strip()
                    if clean_line:
                        current_items.append(clean_line)
            
            if current_section and current_items:
                sections.append((current_section, current_items))
            
            # Wyúwietl sekcje jako karty
            if sections:
                for idx, (section_title, items) in enumerate(sections):
                    # Automatyczne wybieranie koloru i ikony na podstawie tytu≥u sekcji
                    if 'warunki' in section_title.lower() or 'optymalne' in section_title.lower():
                        icon = '??'
                        bg = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                        text_color = 'white'
                    elif 'mocn' in section_title.lower() or 'wzmacnia' in section_title.lower():
                        icon = '??'
                        bg = 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
                        text_color = 'white'
                    elif 'rozwÛj' in section_title.lower() or 'rozwija' in section_title.lower():
                        icon = '??'
                        bg = 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
                        text_color = '#333'
                    else:
                        icon = '?'
                        bg = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
                        text_color = 'white'
                    
                    # Buduj HTML dla wszystkich punktÛw w jednej karcie z numeracjπ
                    items_html = "<ol style='margin: 10px 0 0 20px; padding-left: 0;'>"
                    for item in items:
                        # PrzetwÛrz tekst aby zamieniÊ **tekst** na <strong>tekst</strong>
                        # Uøyj regex do zamiany wszystkich wystπpieÒ **coú** na <strong>coú</strong>
                        formatted_item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
                        
                        items_html += f"<li style='margin: 10px 0; line-height: 1.6;'>{formatted_item}</li>"
                    
                    items_html += "</ol>"
                    
                    # Jedna karta z nag≥Ûwkiem i wszystkimi punktami
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
                # Fallback - wyúwietl surowy tekst jeúli parsowanie nie zadzia≥a≥o
                st.markdown(ai_tips_text)
            
            # Debug ekspander - pokaø surowy tekst AI
            with st.expander("?? Debug: Zobacz surowy tekst AI"):
                st.code(st.session_state.kolb_ai_tips, language="text")
            
            # Stopka z informacjπ
            st.markdown("""
            <div style='background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                        padding: 20px; 
                        border-radius: 15px; 
                        margin: 20px 0;
                        border-left: 4px solid #667eea;'>
                <p style='margin: 0; color: #2c3e50; font-size: 1.05em;'>
                    ?? <strong>PamiÍtaj:</strong> Te wskazÛwki sπ dopasowane do Twojego stylu uczenia siÍ. 
                    Testuj je w praktyce i obserwuj co dzia≥a najlepiej w Twojej sytuacji.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button("? Wygeneruj wskazÛwki AI", type="primary", width="stretch", key="generate_ai_tips"):
                with st.spinner("?? AI generuje spersonalizowane wskazÛwki..."):
                    generate_kolb_ai_tips(dominant, st.session_state.kolb_profession)
                    st.session_state.kolb_ai_generated = True
                    st.rerun()
    
    # Przyciski akcji na dole
    st.markdown("---")
    col_pdf, col_reset, col_close = st.columns([1, 1, 1])
    
    with col_pdf:
        if st.button("?? Wygeneruj raport PDF", width="stretch", type="primary", key="download_kolb_pdf"):
            try:
                html_content = generate_kolb_html_report()
                
                # Zapisz HTML do pliku tymczasowego
                report_filename = f"Kolb_Raport_{st.session_state.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                report_path = os.path.join("temp", report_filename)
                
                # Upewnij siÍ øe folder temp istnieje
                os.makedirs("temp", exist_ok=True)
                
                with open(report_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                
                # Download button dla HTML
                st.download_button(
                    label="?? Pobierz raport HTML",
                    data=html_content,
                    file_name=report_filename,
                    mime="text/html",
                    width="stretch",
                    key="save_kolb_html"
                )
                
                st.success("? Raport wygenerowany!")
                st.info(
                    "?? **Jak zapisaÊ jako PDF:**\n\n"
                    "1. OtwÛrz pobrany plik HTML w przeglπdarce\n"
                    "2. Naciúnij **Ctrl+P** (Windows) lub **Cmd+P** (Mac)\n"
                    "3. Wybierz **'Zapisz jako PDF'**\n"
                    "4. Kliknij **Zapisz**"
                )
                    
            except Exception as e:
                st.error(f"? B≥πd podczas generowania raportu: {str(e)}")
    
    with col_reset:
        if st.button("?? Rozpocznij test od nowa", width="stretch", key="restart_kolb_test"):
            # Ustaw flagÍ reset, aby zapobiec automatycznemu wczytywaniu wynikÛw z bazy
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
        if st.button("? Zamknij test", width="stretch", key="close_kolb_from_results"):
            st.session_state.active_tool = None
            st.rerun()

def show_tools_page():

    """G≥Ûwna strona narzÍdzi AI"""
    
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urzπdzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urzπdzenia
    device_type = get_device_type()
    
    # PrzewiÒ na gÛrÍ strony
    scroll_to_top()
    
    # Header strony
    zen_header("??? NarzÍdzia AI")
    
    # Sprawdü czy uøytkownik zosta≥ przekierowany z Dashboard do Autodiagnozy
    if st.session_state.get('tools_tab') == 'autodiagnoza':
        st.info("?? Jesteú w zak≥adce **?? Autodiagnoza** - pierwsza zak≥adka poniøej")
        # WyczyúÊ flagÍ po wyúwietleniu
        st.session_state.tools_tab = None
    
    # G≥Ûwne kategorie w tabach
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "?? Autodiagnoza",
        "?? C-IQ Tools", 
        "?? Symulatory",
        "?? KreatywnoúÊ",
        "?? Analityki", 
        "?? AI Asystent"
    ])
    
    with tab1:
        show_autodiagnosis()
    
    with tab2:
        show_ciq_tools()
    
    with tab3:
        show_simulators()
    
    with tab4:
        show_creative_tools()
        
    with tab5:
        show_analytics()
    
    with tab6:
        show_ai_assistant()

def show_ciq_tools():
    """NarzÍdzia Conversational Intelligence"""
    st.markdown("### ?? NarzÍdzia Conversational Intelligence")
    st.markdown("Wykorzystaj moc AI do analizy i doskonalenia komunikacji na poziomach C-IQ")
    
    # Siatka narzÍdzi
    col1, col2 = st.columns(2)
    
    with col1:
        # C-IQ Scanner
        with st.container():
            scanner_html = '''
            <div style='padding: 20px; border: 2px solid #4CAF50; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);'>
                <h4>?? C-IQ Scanner</h4>
                <p><strong>Zeskanuj poziom komunikacji I otrzymaj wersje na wyøszych poziomach C-IQ</strong></p>
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li>?? Szybkie skanowanie poziomÛw komunikacji (I, II, III)</li>
                    <li>? B≥yskawiczna konwersja na wyøsze poziomy</li>
                    <li>?? Analiza wp≥ywu neurobiologicznego</li>
                    <li>?? Gotowe alternatywne wersje do uøycia</li>
                </ul>
            </div>
            '''
            st.markdown(scanner_html, unsafe_allow_html=True)
            
            if zen_button("?? Uruchom C-IQ Scanner", key="level_detector", width='stretch'):
                st.session_state.active_tool = "level_detector"
        
    with col2:
        # Conversation Intelligence Pro
        with st.container():
            pro_html = '''
            <div style='padding: 20px; border: 2px solid #E91E63; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #ffeef8 0%, #f8bbd9 100%);'>
                <h4>?? Conversation Intelligence Pro</h4>
                <p><strong>Zaawansowana analiza rozmÛw biznesowych w czasie rzeczywistym</strong></p>
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li>?? Sentiment i emocje + wp≥yw neurobiologiczny</li>
                    <li>?? Wykrywanie intencji sprzedaøowych i biznesowych</li>
                    <li>?? Ostrzeøenia o eskalacji problemÛw</li>
                    <li>?? Sugestie real-time dla agentÛw</li>
                    <li>?? Automatyczna kategoryzacja problemÛw</li>
                </ul>
            </div>
            '''
            st.markdown(pro_html, unsafe_allow_html=True)
            
            if zen_button("?? Uruchom CI Pro", key="emotion_detector", width='stretch'):
                st.session_state.active_tool = "emotion_detector"
        
        # C-IQ Leadership Profile
        with st.container():
            leadership_html = '''
            <div style='padding: 20px; border: 2px solid #2196F3; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #e3f2fd 0%, #90caf9 100%);'>
                <h4>?? C-IQ Leadership Profile</h4>
                <p><strong>D≥ugoterminowa analiza stylu przywÛdztwa przez pryzmat C-IQ</strong></p>
                <ul style='margin: 10px 0; padding-left: 20px;'>
                    <li>?? Trend rozwoju C-IQ w czasie</li>
                    <li>?? Profil przywÛdczy (dominujπce poziomy)</li>
                    <li>?? Plan rozwoju komunikacyjnego</li>
                    <li>?? Benchmark z innymi liderami</li>
                </ul>
            </div>
            '''
            st.markdown(leadership_html, unsafe_allow_html=True)
            
            if zen_button("?? UtwÛrz Profil Lidera", key="communication_analyzer", width='stretch'):
                st.session_state.active_tool = "communication_analyzer"
    
    # Wyúwietl aktywne narzÍdzie
    active_tool = st.session_state.get('active_tool')
    if active_tool:
        st.markdown("---")
        
        # Przycisk resetowania
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if zen_button("? Zamknij narzÍdzie", key="close_tool", width='stretch'):
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
    """C-IQ Scanner - g≥Ûwna funkcjonalnoúÊ"""
    st.markdown("## ?? C-IQ Scanner")
    st.markdown("**Zeskanuj poziom komunikacji** i **zobacz alternatywne wersje** na wyøszych poziomach Conversational Intelligence")
    
    # Tabs z rÛønymi trybami
    tab1, tab2, tab3 = st.tabs([
        "?? Analiza tekstu", 
        "?? Przyk≥ady poziomÛw", 
        "?? Szablony emaili"
    ])
    
    with tab1:
        st.markdown("#### Wklej dowolny tekst do analizy C-IQ")
        
        # Przyk≥ady do szybkiego testowania
        with st.expander("?? Przyk≥ady do przetestowania", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Poziom I (Transakcyjny):**")
                example_1 = "Wyúlij raport do koÒca dnia. Brak dyskusji."
                if st.button("?? Uøyj przyk≥adu", key="example_1"):
                    st.session_state.level_detector_input = example_1
                
                st.markdown("**Poziom II (Pozycyjny):**") 
                example_2 = "Uwaøam, øe ten pomys≥ nie ma sensu. Moja propozycja jest lepsza bo..."
                if st.button("?? Uøyj przyk≥adu", key="example_2"):
                    st.session_state.level_detector_input = example_2
            
            with col2:
                st.markdown("**Poziom III (Transformacyjny):**")
                example_3 = "Jakie widzisz moøliwoúci w tej sytuacji? Jak moøemy razem wypracowaÊ rozwiπzanie, ktÛre bÍdzie dzia≥aÊ dla wszystkich?"
                if st.button("?? Uøyj przyk≥adu", key="example_3"):
                    st.session_state.level_detector_input = example_3
        
        text_input = st.text_area(
            "Tekst do analizy:",
            value=st.session_state.get('level_detector_input', ''),
            placeholder="Wklej tutaj email, transkrypcjÍ rozmowy, lub planowanπ wypowiedü...",
            height=200,
            key="level_detector_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if zen_button("?? Skanuj poziom C-IQ", key="analyze_level", width='stretch'):
                if text_input and text_input.strip():
                    with st.spinner("?? Scanner analizuje poziom rozmowy..."):
                        result = analyze_conversation_level(text_input)
                        if result:
                            st.session_state.last_analysis_result = result
                            
                            # Przyznaj XP za uøycie narzÍdzia CIQ Scanner
                            try:
                                from data.users import award_xp_for_activity
                                award_xp_for_activity(
                                    st.session_state.username,
                                    'tool_used',
                                    1,  # 1 XP za uøycie narzÍdzia
                                    {
                                        'tool_name': 'CIQ Scanner',
                                        'detected_level': result.get('detected_level', 'unknown'),
                                        'confidence': result.get('confidence', 0)
                                    }
                                )
                                st.success("? Analiza ukoÒczona! +1 XP")
                            except Exception:
                                pass  # Nie przerywaj jeúli tracking siÍ nie powiedzie
                        else:
                            st.error("Nie uda≥o siÍ przeanalizowaÊ tekstu. SprÛbuj ponownie.")
                else:
                    st.warning("?? Wpisz tekst do analizy")
        
        with col2:
            if text_input:
                word_count = len(text_input.split())
                st.metric("S≥owa", word_count)
        
        # Wyúwietl wynik analizy jeúli istnieje
        if 'last_analysis_result' in st.session_state and text_input and text_input.strip():
            st.markdown("---")
            
            if st.session_state.last_analysis_result.get('analyzed_text') != text_input:
                st.warning("?? PokazujÍ wynik dla poprzedniego tekstu. Kliknij 'Analizuj' ponownie.")
                
            display_level_analysis(st.session_state.last_analysis_result)
    
    with tab2:
        show_ciq_examples()
    
    with tab3:
        show_email_templates()

def analyze_conversation_level(text: str) -> Optional[Dict]:
    """Analizuje poziom C-IQ w tekúcie"""
    
    evaluator = AIExerciseEvaluator()
    
    # Sprawdü czy evaluator jest w demo mode
    if hasattr(evaluator, 'demo_mode') and evaluator.demo_mode:
        st.info("?? C-IQ Scanner w trybie demo - uøywam analizy heurystycznej")
        return create_fallback_analysis(text)
    
    prompt = f"""
Jesteú ekspertem w Conversational Intelligence. Przeanalizuj nastÍpujπcy tekst i okreúl jego poziom C-IQ.

TEKST DO ANALIZY:
"{text}"

POZIOMY C-IQ:
- **Poziom I (Transakcyjny)**: Wymiana informacji, fokus na zadania, jÍzyk dyrektywny, brak emocji, jednokierunkowa komunikacja
- **Poziom II (Pozycyjny)**: Obrona stanowisk, argumentowanie, "my vs oni", konfrontacja, przekonywanie, walka o racjÍ  
- **Poziom III (Transformacyjny)**: WspÛ≥tworzenie, pytania otwarte, "wspÛlny cel", budowanie zaufania, jÍzyk partnerski

WAØNE: 
1. Odpowiedz TYLKO w poprawnym formacie JSON, bez dodatkowych komentarzy.
2. MUSISZ wybraÊ JEDEN dominujπcy poziom - nie moøna wykrywaÊ wielu poziomÛw jednoczeúnie:
   - "detected_level" moøe byÊ tylko: "Poziom I" lub "Poziom II" lub "Poziom III"
   - Wybierz poziom ktÛry najlepiej charakteryzuje CA£Oå∆ tekstu
   - Jeúli tekst zawiera elementy rÛønych poziomÛw, wybierz ten ktÛry DOMINUJE
3. W sekcji "alternative_versions" podaj alternatywy TYLKO dla poziomÛw wyøszych niø wykryty:
   - Jeúli wykryjesz Poziom I: podaj wersje dla II i III
   - Jeúli wykryjesz Poziom II: podaj wersjÍ tylko dla III  
   - Jeúli wykryjesz Poziom III: pozostaw alternative_versions puste {{}}

{{
    "detected_level": "Poziom I/II/III",
    "confidence": [1-10],
    "explanation": "SzczegÛ≥owe wyjaúnienie dlaczego to ten poziom - cytuj konkretne fragmenty",
    "key_indicators": ["konkretny wskaünik jÍzykowy 1", "konkretny wskaünik jÍzykowy 2"],
    "neurobiological_impact": "Przewidywany wp≥yw na hormony - czy wzbudza kortyzol (stres) czy oksytocynÍ (zaufanie)",
    "improvement_suggestions": ["jak podnieúÊ na wyøszy poziom - konkretne zmiany"],
    "alternative_versions": {{
        "level_ii": "Jak brzmia≥by ten tekst przepisany na poziom II (tylko jeúli wykryty poziom to I)",
        "level_iii": "Jak brzmia≥by ten tekst przepisany na poziom III (jeúli wykryty poziom to I lub II)"
    }},
    "practical_tips": ["konkretna wskazÛwka komunikacyjna 1", "konkretna wskazÛwka 2"],
    "emotional_tone": "neutralny/pozytywny/negatywny/agresywny/partnerski",
    "trust_building_score": [1-10],
    "language_patterns": ["wzorzec jÍzykowy 1", "wzorzec jÍzykowy 2"]
}}
"""
    
    try:
        # Uøyj bezpoúrednio funkcji z AIExerciseEvaluator
        if hasattr(evaluator, 'gemini_model'):
            response = evaluator.gemini_model.generate_content(prompt)
            
            if response and response.text:
                content = response.text.strip()
                
                # UsuÒ markdown formatowanie jeúli jest
                if content.startswith("```json"):
                    content = content.replace("```json", "").replace("```", "").strip()
                
                # SprÛbuj sparsowaÊ JSON
                import json
                import re
                
                # Znajdü JSON w odpowiedzi
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    
                    try:
                        result = json.loads(json_str)
                        
                        # Sprawdü czy mamy wymagane pola dla detektora C-IQ
                        if 'detected_level' in result and 'confidence' in result:
                            st.success("? Skanowanie C-IQ ukoÒczone!")
                            # Dodaj analizowany tekst do wyniku
                            result['analyzed_text'] = text
                            return result
                        else:
                            st.warning("?? AI zwrÛci≥o niepe≥nπ analizÍ")
                            st.json(result)  # Pokaø co zwrÛci≥o
                            return create_fallback_analysis(text)
                            
                    except json.JSONDecodeError as json_err:
                        st.error(f"? B≥πd parsowania JSON: {str(json_err)}")
                        st.warning("Uøywam analizy backup zamiast niepoprawnego JSON")
                        return create_fallback_analysis(text)
                else:
                    st.warning("?? Nie uda≥o siÍ znaleüÊ JSON w odpowiedzi AI")
                    return create_fallback_analysis(text)
            else:
                st.warning("?? AI nie zwrÛci≥o odpowiedzi")
                return create_fallback_analysis(text)
        else:
            st.warning("?? Model AI niedostÍpny")
            return create_fallback_analysis(text)
            
    except Exception as e:
        st.error(f"? B≥πd podczas analizy: {str(e)}")
        return create_fallback_analysis(text)

def create_fallback_analysis(text: str) -> Dict:
    """Tworzy fallback analizÍ gdy AI nie dzia≥a"""
    
    text_lower = text.lower()
    word_count = len(text.split())
    
    # Prosta heurystyka do okreúlenia poziomu
    level_iii_keywords = ['jak', 'moøemy', 'razem', 'wspÛlnie', 'jakie', 'czy moglibyúmy', 'co myúlisz', 'jak widzisz']
    level_ii_keywords = ['uwaøam', 'myúlÍ øe', 'nie zgadzam siÍ', 'moja propozycja', 'lepiej by by≥o']
    level_i_keywords = ['wyúlij', 'zrÛb', 'musisz', 'wykonaj', 'deadline', 'koniec']
    
    level_iii_score = sum(1 for keyword in level_iii_keywords if keyword in text_lower)
    level_ii_score = sum(1 for keyword in level_ii_keywords if keyword in text_lower)
    level_i_score = sum(1 for keyword in level_i_keywords if keyword in text_lower)
    
    if level_iii_score > max(level_ii_score, level_i_score):
        detected_level = "Poziom III"
        confidence = min(9, 6 + level_iii_score)
        trust_score = min(9, 7 + level_iii_score)
        explanation = "Tekst zawiera elementy wspÛ≥tworzenia i pytania otwarte charakterystyczne dla Poziomu III."
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
    
    # TwÛrz alternatywne wersje zaleønie od wykrytego poziomu
    alternative_versions = {}
    
    if detected_level == "Poziom I":
        alternative_versions = {
            "level_ii": f"Uwaøam, øe ta sytuacja wymaga analizy. Moja perspektywa jest taka, øe...",
            "level_iii": f"Jakie widzimy moøliwoúci w tej sytuacji? Jak moøemy razem wypracowaÊ najlepsze rozwiπzanie?"
        }
    elif detected_level == "Poziom II":
        alternative_versions = {
            "level_iii": f"Jakie widzimy moøliwoúci w tej sytuacji? Jak moøemy razem wypracowaÊ rozwiπzanie, ktÛre bÍdzie dzia≥aÊ dla wszystkich?"
        }
    # Poziom III nie ma alternatyw - to juø najwyøszy poziom
    
    return {
        "analyzed_text": text,
        "detected_level": detected_level,
        "confidence": confidence,
        "explanation": explanation,
        "key_indicators": [f"D≥ugoúÊ tekstu: {word_count} s≥Ûw", "Analiza heurystyczna s≥Ûw kluczowych"],
        "neurobiological_impact": f"Przewidywany wp≥yw odpowiada charakterystyce {detected_level}",
        "improvement_suggestions": ["Dodaj wiÍcej pytaÒ otwartych", "Uøyj jÍzyka wspÛ≥tworzenia"] if detected_level != "Poziom III" else ["Kontynuuj uøywanie transformacyjnego stylu komunikacji"],
        "alternative_versions": alternative_versions,
        "practical_tips": ["Zadawaj wiÍcej pytaÒ otwartych", "Uøywaj jÍzyka 'my' zamiast 'ty'"] if detected_level != "Poziom III" else ["Wykorzystuj moc wspÛ≥tworzenia", "Buduj na osiπgniÍtym wysokim poziomie"],
        "emotional_tone": "neutralny",
        "trust_building_score": trust_score,
        "language_patterns": ["Wykryte wzorce na podstawie analizy s≥Ûw kluczowych"]
    }

def display_level_analysis(result: Dict):
    """Wyúwietla wyniki analizy poziom C-IQ"""
    
    if not result:
        st.error("Brak wynikÛw analizy")
        return
    
    # G≥Ûwny wynik w metrykach
    level = result.get('detected_level', 'Nie okreúlono')
    confidence = result.get('confidence', 0)
    trust_score = result.get('trust_building_score', 0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("?? Wykryty poziom", level)
    with col2:
        st.metric("?? PewnoúÊ analizy", f"{confidence}/10")
    with col3:
        st.metric("?? Budowanie zaufania", f"{trust_score}/10")
    
    # Wizualizacja poziomÛw z kolorami - poprawiona logika wykrywania
    st.markdown("### ?? Analiza poziomÛw C-IQ")
    
    level_info = {
        "Poziom I": {"color": "??", "desc": "Transakcyjny - wymiana informacji", "bg": "#ffebee"},
        "Poziom II": {"color": "??", "desc": "Pozycyjny - obrona stanowisk", "bg": "#fff8e1"}, 
        "Poziom III": {"color": "??", "desc": "Transformacyjny - wspÛ≥tworzenie", "bg": "#e8f5e8"}
    }
    
    # Lepsze wykrywanie dominujπcego poziomu  
    detected_level = result.get('detected_level', '').strip()
    
    for lvl, info in level_info.items():
        # Precyzyjne wykrywanie - tylko jeden poziom moøe byÊ aktywny
        is_detected = False
        
        if "III" in detected_level and lvl == "Poziom III":
            is_detected = True
        elif "II" in detected_level and "III" not in detected_level and lvl == "Poziom II":
            is_detected = True  
        elif "I" in detected_level and "II" not in detected_level and "III" not in detected_level and lvl == "Poziom I":
            is_detected = True
            
        border_style = "border: 2px solid #4CAF50;" if is_detected else "border: 1px solid #ddd;"
        selected_indicator = "<strong>?? WYKRYTO</strong>" if is_detected else ""
        
        st.markdown(f"""
        <div style='padding: 15px; margin: 5px 0; border-radius: 10px; background-color: {info['bg']}; {border_style}'>
            {info['color']} <strong>{lvl}</strong> {selected_indicator}<br>
            <span style='color: #666;'>{info['desc']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # SzczegÛ≥owe wyjaúnienie
    if 'explanation' in result:
        st.markdown("### ?? SzczegÛ≥owa analiza")
        st.info(result['explanation'])
    
    # Wskaüniki w dwÛch kolumnach
    col1, col2 = st.columns(2)
    
    with col1:
        # Wskaüniki kluczowe
        if 'key_indicators' in result:
            st.markdown("### ?? Kluczowe wskaüniki jÍzykowe")
            for indicator in result['key_indicators']:
                st.markdown(f"ï {indicator}")
        
        # Wzorce jÍzykowe
        if 'language_patterns' in result:
            st.markdown("### ?? Wzorce jÍzykowe")
            for pattern in result['language_patterns']:
                st.markdown(f"ï {pattern}")
    
    with col2:
        # Ton emocjonalny
        if 'emotional_tone' in result:
            st.markdown("### ?? Ton emocjonalny")
            tone = result['emotional_tone']
            tone_colors = {
                'pozytywny': '??', 'neutralny': '??', 'negatywny': '??',
                'agresywny': '??', 'partnerski': '??'
            }
            color = tone_colors.get(tone.lower(), '?')
            st.markdown(f"{color} **{tone.title()}**")
        
        # Wp≥yw neurobiologiczny
        if 'neurobiological_impact' in result:
            st.markdown("### ?? Wp≥yw neurobiologiczny")
            st.warning(result['neurobiological_impact'])
    
    # Sugestie poprawy
    if 'improvement_suggestions' in result:
        st.markdown("### ?? Jak podnieúÊ poziom komunikacji")
        for suggestion in result['improvement_suggestions']:
            st.markdown(f"ï {suggestion}")
    
    # Alternatywne wersje w expanderach - pokazuj tylko wyøsze poziomy
    if 'alternative_versions' in result:
        alt_versions = result['alternative_versions']
        detected_level = result.get('detected_level', '')
        
        # Logika: WAØNE - sprawdzaj od najd≥uøszego do najkrÛtszego ciπgu!
        if 'Poziom III' in detected_level:
            # Dla poziomu III: BRAK nag≥Ûwka, tylko gratulacje
            st.success("?? **Gratulacje!** To juø najwyøszy poziom C-IQ - Transformacyjny!")
            st.info("?? **Twoja komunikacja wykorzystuje:**\n"
                   "ï JÍzyk wspÛ≥tworzenia\n"
                   "ï Pytania otwarte\n" 
                   "ï Budowanie wspÛlnych celÛw\n"
                   "ï StymulacjÍ oksytocyny (zaufanie)")
                   
        elif 'Poziom II' in detected_level:
            # Dla poziomu II: pokaø nag≥Ûwek i alternatywÍ III
            st.markdown("### ?? Jak brzmia≥oby na wyøszym poziomie C-IQ")
            
            if 'level_iii' in alt_versions and alt_versions['level_iii']:
                with st.expander("?? Poziom III - Transformacyjny", expanded=False):
                    st.success(alt_versions['level_iii'])
            else:
                st.info("?? To juø wysoki poziom komunikacji! Poziom III to najwyøszy dostÍpny poziom.")
                
        elif 'Poziom I' in detected_level:
            # Dla poziomu I: pokaø nag≥Ûwek i alternatywy II + III
            st.markdown("### ?? Jak brzmia≥oby na wyøszych poziomach C-IQ")
            
            if 'level_ii' in alt_versions and alt_versions['level_ii']:
                with st.expander("?? Poziom II - Pozycyjny", expanded=False):
                    st.success(alt_versions['level_ii'])
            
            if 'level_iii' in alt_versions and alt_versions['level_iii']:
                with st.expander("?? Poziom III - Transformacyjny", expanded=False):
                    st.success(alt_versions['level_iii'])
        else:
            # Fallback dla nieokreúlonych poziomÛw - pokaø nag≥Ûwek
            st.markdown("### ?? Jak brzmia≥oby na wyøszych poziomach C-IQ")
            
            if 'level_ii' in alt_versions and alt_versions['level_ii']:
                with st.expander("?? Poziom II - Pozycyjny", expanded=False):
                    st.success(alt_versions['level_ii'])
            
            if 'level_iii' in alt_versions and alt_versions['level_iii']:
                with st.expander("?? Poziom III - Transformacyjny", expanded=False):
                    st.success(alt_versions['level_iii'])
    
    # Praktyczne wskazÛwki
    if 'practical_tips' in result:
        st.markdown("### ?? Praktyczne wskazÛwki do zastosowania")
        for i, tip in enumerate(result['practical_tips'], 1):
            st.markdown(f"**{i}.** {tip}")

def show_ciq_examples():
    """Pokazuje przyk≥ady rÛønych poziomÛw C-IQ"""
    st.markdown("#### ?? Przyk≥ady poziomÛw C-IQ w praktyce")
    
    examples = [
        {
            "scenario": "Informowanie o problemie w projekcie",
            "level_1": "Projekt siÍ opÛünia. Deadline za tydzieÒ. Pracujcie d≥uøej.",
            "level_2": "Uwaøam, øe zespÛ≥ nie wywiπzuje siÍ z zobowiπzaÒ. To wina s≥abego planowania z waszej strony.",
            "level_3": "WidzÍ, øe projekt moøe siÍ opÛüniÊ. Jakie widzicie przyczyny tej sytuacji? Jak moøemy razem znaleüÊ rozwiπzanie?"
        },
        {
            "scenario": "Feedback dla pracownika",
            "level_1": "TwÛj raport ma b≥Ídy. Popraw i wyúlij ponownie.",
            "level_2": "Nie zgadzam siÍ z Twoim podejúciem. Moja metoda jest lepsza, poniewaø...",
            "level_3": "Zauwaøy≥em kilka obszarÛw w raporcie, ktÛre moøemy razem ulepszyÊ. Co myúlisz o tych aspektach?"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        st.markdown(f"### Przyk≥ad {i}: {example['scenario']}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**?? Poziom I - Transakcyjny**")
            st.text_area(
                "Poziom I",
                value=example['level_1'],
                height=100,
                key=f"example_{i}_1",
                label_visibility="collapsed"
            )
            
        with col2:
            st.markdown("**?? Poziom II - Pozycyjny**")
            st.text_area(
                "Poziom II",
                value=example['level_2'],
                height=100,
                key=f"example_{i}_2",
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown("**?? Poziom III - Transformacyjny**")
            st.text_area(
                "Poziom III",
                value=example['level_3'],
                height=100,
                key=f"example_{i}_3",
                label_visibility="collapsed"
            )

def show_email_templates():
    """Pokazuje szablony emaili na rÛønych poziomach C-IQ"""
    st.markdown("#### ?? Szablony emaili biznesowych")
    st.info("?? Funkcja w przygotowaniu - biblioteka szablonÛw emaili na rÛønych poziomach C-IQ")

def show_emotion_detector():
    """Conversation Intelligence Pro - Analiza rozmÛw menedøerskich"""
    st.markdown("## ?? Conversation Intelligence Pro")
    st.markdown("**Zaawansowana analiza rozmÛw menedøerskich** - C-IQ w kontekúcie przywÛdztwa i zarzπdzania zespo≥em")
    
    # Tabs dla rÛønych funkcji CI w kontekúcie menedøerskim
    tab1, tab2, tab3, tab4 = st.tabs([
        "?? Analiza Rozmowy", 
        "?? Dynamika Zespo≥u", 
        "?? Sygna≥y ProblemÛw", 
        "?? Leadership Coach"
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
    """Analiza rozmÛw menedøerskich"""
    st.markdown("### ?? Analiza Rozmowy Menedøer-Pracownik")
    
    conversation_text = st.text_area(
        "?? Wklej transkrypcjÍ rozmowy menedøerskiej:",
        placeholder="""Przyk≥ad rozmowy menedøer-pracownik:
Menedøer: Chcia≥bym porozmawiaÊ o Twoich ostatnich projektach.
Pracownik: Okej, ale muszÍ powiedzieÊ, øe czujÍ siÍ przeciπøony zadaniami...
Menedøer: Rozumiem, opowiedz mi wiÍcej o tym przeciπøeniu...""",
        height=120,
        key="sentiment_input"
    )
    
    if conversation_text and len(conversation_text) > 10:
        if zen_button("?? Analizuj Sentiment + C-IQ", key="analyze_sentiment", width='stretch'):
            with st.spinner("?? AnalizujÍ sentiment i poziomy C-IQ..."):
                # Analiza C-IQ + sentiment
                result = analyze_conversation_sentiment(conversation_text)
                if result:
                    display_sentiment_results(result)
                    
                    # Przyznaj XP za uøycie narzÍdzia
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
    """Wykrywanie dynamiki zespo≥owej i potrzeb pracownikÛw"""
    st.markdown("### ?? Analiza Dynamiki Zespo≥u i Motywacji")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**?? Wykrywane potrzeby pracownika:**")
        st.markdown("ï ?? Potrzeba jasnych celÛw")
        st.markdown("ï ?? ChÍÊ rozwoju i szkoleÒ") 
        st.markdown("ï ?? Potrzeba wsparcia/mentoringu")
        st.markdown("ï ?? Sygna≥y wypalenia zawodowego")
        st.markdown("ï ?? Ambicje i aspiracje kariery")
        
    with col2:
        st.markdown("**?? Wyniki analizy:**")
        st.markdown("ï Poziom zaangaøowania zespo≥u")
        st.markdown("ï Rekomendowane akcje menedøerskie")  
        st.markdown("ï Optymalne momenty na feedback")
        st.markdown("ï Przewidywane reakcje pracownika")
    
    intent_text = st.text_area(
        "Tekst do analizy dynamiki zespo≥u:",
        placeholder="Wklej fragment rozmowy menedøer-pracownik o zadaniach, celach, problemach...",
        height=100,
        key="intent_input"
    )
    
    if intent_text and len(intent_text) > 10:
        if zen_button("?? Wykryj Intencje", key="detect_intent", width='stretch'):
            result = analyze_business_intent(intent_text)
            if result:
                display_intent_results(result)
                
                # Przyznaj XP za uøycie narzÍdzia
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
    """Monitoring sygna≥Ûw problemÛw w zespole"""
    st.markdown("### ?? Wykrywanie Sygna≥Ûw ProblemÛw Zespo≥owych")
    
    st.info("?? **Early warning system** dla problemÛw zespo≥owych: wypalenie, konflikty, spadek motywacji")
    
    escalation_text = st.text_area(
        "?? Tekst do analizy sygna≥Ûw problemÛw:",
        placeholder="Wklej fragment rozmowy z pracownikiem, ktÛry moøe sygnalizowaÊ problemy zespo≥owe...",
        height=100,
        key="escalation_input"
    )
    
    # Ustawienia czu≥oúci
    sensitivity = st.slider(
        "??? Czu≥oúÊ wykrywania eskalacji:",
        min_value=1, max_value=10, value=5,
        help="1 = tylko oczywiste sygna≥y, 10 = bardzo wyczulone wykrywanie"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**?? Sygna≥y eskalacji:**")
        st.markdown("ï Spadek motywacji i zaangaøowania")
        st.markdown("ï Sygna≥y wypalenia zawodowego") 
        st.markdown("ï Konflikty interpersonalne")
        st.markdown("ï Rozwaøanie zmiany pracy")
        
    with col2:
        st.markdown("**?? Rekomendowane akcje:**")
        st.markdown("ï Rozmowa 1-on-1 z pracownikiem")
        st.markdown("ï Przeglπd obciπøenia i zadaÒ")
        st.markdown("ï Plan rozwoju i wsparcia")
        st.markdown("ï Poprawa warunkÛw pracy")
    
    if escalation_text and len(escalation_text) > 10:
        if zen_button("?? Sprawdü Ryzyko Eskalacji", key="check_escalation", width='stretch'):
            result = analyze_escalation_risk(escalation_text, sensitivity)
            if result:
                display_escalation_results(result)
                
                # Przyznaj XP za uøycie narzÍdzia
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
    """Real-time coach dla menedøerÛw"""
    st.markdown("### ?? Leadership Coach - Wsparcie Real-time")
    
    st.info("?? **Inteligentny coach przywÛdztwa** podpowiadajπcy najlepsze odpowiedzi w trudnych sytuacjach menedøerskich")
    
    # Kontekst rozmowy menedøerskiej
    context = st.selectbox(
        "?? Typ rozmowy menedøerskiej:",
        [
            "?? Ustawienie celÛw i oczekiwaÒ",
            "?? Feedback o wydajnoúci", 
            "?? Rozmowa z demotywowanym pracownikiem",
            "? Zarzπdzanie konfliktem w zespole",
            "?? Rozmowa rozwojowa i kariera",
            "?? Delegowanie zadaÒ i odpowiedzialnoúci",
            "?? Zarzπdzanie zmianπ organizacyjnπ",
            "?? Rozmowa dyscyplinujπca"
        ]
    )
    
    coach_text = st.text_area(
        "?? Ostatnia wypowiedü pracownika:",
        placeholder="Wklej co w≥aúnie powiedzia≥ pracownik, a AI zasugeruje najlepszπ odpowiedü menedøerskπ...",
        height=100,
        key="coach_input"
    )
    
    if coach_text and len(coach_text) > 5:
        if zen_button("?? Podpowiedz Odpowiedü", key="suggest_response", width='stretch'):
            result = get_ai_coaching(coach_text, context)
            if result:
                display_coaching_results(result)
                
                # Przyznaj XP za uøycie narzÍdzia
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
    """C-IQ Leadership Profile - d≥ugoterminowa analiza stylu przywÛdztwa"""
    st.markdown("## ?? C-IQ Leadership Profile")
    st.markdown("**D≥ugoterminowa analiza Twojego stylu przywÛdztwa** przez pryzmat Conversational Intelligence")
    
    st.info("?? **UnikalnoúÊ:** To jedyne narzÍdzie ktÛre analizuje **wzorce d≥ugoterminowe** w Twoim stylu przywÛdztwa, zamiast pojedynczych rozmÛw")
    
    # Auto-wczytywanie zapisanego profilu
    if hasattr(st.session_state, 'username') and st.session_state.username:
        if 'leadership_profile' not in st.session_state:
            saved_profile = load_leadership_profile(st.session_state.username)
            if saved_profile:
                st.session_state['leadership_profile'] = saved_profile
                st.success(f"?? Wczytano TwÛj zapisany profil przywÛdczy z {saved_profile.get('created_at', 'wczeúniej')[:10]}")
    
    # Tabs dla rÛønych aspektÛw profilu
    tab1, tab2, tab3 = st.tabs([
        "?? Upload Danych", 
        "?? Profil PrzywÛdczy", 
        "?? Plan Rozwoju"
    ])
    
    with tab1:
        st.markdown("### ?? Wgraj prÛbki swojej komunikacji")
        st.markdown("Im wiÍcej danych, tym dok≥adniejszy profil przywÛdczy!")
        
        # Opis co bÍdzie w raporcie
        st.markdown("**?? TwÛj raport bÍdzie zawiera≥:**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**?? Poziomy C-IQ**")
            st.markdown("ï Dominujπcy poziom")
            st.markdown("ï Rozk≥ad procentowy")
            st.markdown("ï Rekomendacje")
        
        with col2:
            st.markdown("**?? Neurobiologia**") 
            st.markdown("ï Wp≥yw na kortyzol")
            st.markdown("ï Stymulacja oksytocyny")
            st.markdown("ï BezpieczeÒstwo psychologiczne")
        
        with col3:
            st.markdown("**?? SkutecznoúÊ**")
            st.markdown("ï ClarnoúÊ przekazu")
            st.markdown("ï Potencja≥ zaufania")
            st.markdown("ï Ryzyko konfliktu")
            
        st.markdown("---")
        
        # Przycisk do przyk≥adowych danych
        col_demo, col_info = st.columns([1, 3])
        with col_demo:
            demo_col1, demo_col2 = st.columns(2)
            with demo_col1:
                if zen_button("?? Uøyj przyk≥adÛw", key="fill_demo_data"):
                    # Bezpoúrednio ustawiamy wartoúci w session_state
                    team_conv_text = '''Menedøer: Kasia, muszÍ wiedzieÊ co siÍ dzieje z projektem ABC. Deadline jest za tydzieÒ!
Pracownik: Mam problem z terminem, klient ciπgle zmienia wymagania
Menedøer: To nie jest wymÛwka. Musisz lepiej planowaÊ. Co konkretnie robi≥aú przez ostatnie dni?
Pracownik: PrÛbowa≥am dopasowaÊ siÍ do nowych wymagaÒ, ale...
Menedøer: S≥uchaj, potrzebujÍ rozwiπzaÒ, nie problemÛw. Jak zamierzasz to naprawiÊ?
Pracownik: Moøe gdybym mia≥a wiÍcej wsparcia od zespo≥u?
Menedøer: Dobrze, porozmawiam z Tomkiem øeby ci pomÛg≥. Ale chcÍ codzienne raporty z postÍpÛw.'''
                    st.session_state['team_conv'] = team_conv_text
                    
                    feedback_conv_text = '''Menedøer: Tomek, muszÍ z tobπ porozmawiaÊ o ocenach. Twoje wyniki techniczne sπ ok, ale komunikacja kuleje
Pracownik: Czyli co dok≥adnie robiÍ üle?
Menedøer: Za ma≥o komunikujesz siÍ z zespo≥em. Ludzie nie wiedzπ nad czym pracujesz
Pracownik: Ale skupiam siÍ na pracy, øeby by≥a jakoúÊ...
Menedøer: To nie usprawiedliwia braku komunikacji. Od nastÍpnego tygodnia codzienne updaty na kanale zespo≥owym. Rozumiesz?
Pracownik: Tak, rozumiem
Menedøer: I jeszcze jedno - wiÍcej inicjatywy. Nie czekaj aø ktoú ci kaøe coú zrobiÊ.'''
                    st.session_state['feedback_conv'] = feedback_conv_text
                    
                    conflict_conv_text = '''Menedøer: Ania, s≥ysza≥em øe wczoraj k≥Ûci≥aú siÍ z Markiem o dane do raportu
Pracownik: To by≥ stres, przepraszam. Deadline naciska i...
Menedøer: Nie obchodzπ mnie wymÛwki. W biurze nie krzyczy siÍ na wspÛ≥pracownikÛw. Kropka.
Pracownik: Ale Marek mia≥ dostarczyÊ dane tydzieÒ temu, a...
Menedøer: To nie usprawiedliwia takiego zachowania. NastÍpnym razem przychodzisz do mnie, zamiast robiÊ scenÍ
Pracownik: Dobrze, ale co z tymi danymi?
Menedøer: Porozmawiam z Markiem. A ty przeprosisz go jutro. I øeby wiÍcej takich sytuacji nie by≥o.'''
                    st.session_state['conflict_conv'] = conflict_conv_text
                    
                    motivation_conv_text = '''Menedøer: Pawe≥, dobra robota z tym automatycznym raportem. Dzia≥a jak naleøy
Pracownik: DziÍki, stara≥em siÍ...
Menedøer: No w≥aúnie. Trzeba by≥o tylko trochÍ nacisnπÊ. Widzisz? Jak siÍ chce, to siÍ moøna
Pracownik: Tak, chociaø trochÍ czasu mi to zajÍ≥o
Menedøer: Czas to pieniπdz. NastÍpnym razem rÛb szybciej, ale tak samo dok≥adnie. Moøe dostaniesz wiÍcej takich projektÛw
Pracownik: To brzmi dobrze. Co mam teraz robiÊ?
Menedøer: Sprawdü czy wszystko dzia≥a i zrÛb dokumentacjÍ. Do koÒca tygodnia ma byÊ gotowe.'''
                    st.session_state['motivation_conv'] = motivation_conv_text
                    
                    st.success("? Wype≥niono pola przyk≥adowymi danymi! PrzewiÒ w dÛ≥ øeby zobaczyÊ dane.")
                    
            with demo_col2:
                if zen_button("?? WyczyúÊ pola", key="clear_data"):
                    # Czyúcimy wartoúci w session_state
                    st.session_state['team_conv'] = ""
                    st.session_state['feedback_conv'] = ""
                    st.session_state['conflict_conv'] = ""
                    st.session_state['motivation_conv'] = ""
                    st.success("?? Wyczyszczono wszystkie pola! PrzewiÒ w dÛ≥ øeby sprawdziÊ.")
        
        with col_info:
            st.info("?? **WskazÛwka:** Wklej rzeczywiste fragmenty swoich rozmÛw (minimum 2-3 zdania na pole). Moøesz teø kliknπÊ 'Uøyj przyk≥adÛw' øeby zobaczyÊ jak dzia≥a narzÍdzie.")
            
            # Debug info
            if st.session_state.get('team_conv'):
                st.write(f"?? Debug: team_conv ma {len(st.session_state.get('team_conv', ''))} znakÛw")
        
        # Multiple text areas dla rÛønych sytuacji
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**?? Rozmowy z zespo≥em:**")
            team_conversations = st.text_area(
                "Wklej fragmenty rozmÛw z pracownikami:",
                placeholder="Wklej tutaj rzeczywiste fragmenty swoich rozmÛw z zespo≥em...",
                height=150,
                key="team_conv"
            )
            
            st.markdown("**?? Feedback i oceny:**")
            feedback_conversations = st.text_area(
                "Fragmenty rozmÛw feedbackowych:",
                placeholder="Wklej tutaj fragmenty rozmÛw dotyczπcych ocen i feedbacku...", 
                height=150,
                key="feedback_conv"
            )

        with col2:
            st.markdown("**? Sytuacje konfliktowe:**")
            conflict_conversations = st.text_area(
                "Rozmowy w trudnych sytuacjach:",
                placeholder="Wklej tutaj fragmenty trudnych rozmÛw i rozwiπzywania konfliktÛw...",
                height=150,
                key="conflict_conv"
            )
            
            st.markdown("**?? Motywowanie zespo≥u:**")
            motivation_conversations = st.text_area(
                "Fragmenty motywujπce i inspirujπce:",
                placeholder="Wklej tutaj fragmenty motywujπcych rozmÛw z zespo≥em...",
                height=150,
                key="motivation_conv"
            )
        
        st.markdown("---")
        st.markdown("#### ?? WskazÛwki do wype≥nienia:")
        tip_col1, tip_col2, tip_col3 = st.columns(3)
        
        with tip_col1:
            st.markdown("**? Dobre przyk≥ady:**")
            st.markdown("ï Pe≥ne dialogi (2-6 wymian)")
            st.markdown("ï Rzeczywiste sytuacje")
            st.markdown("ï RÛønorodne scenariusze")
        
        with tip_col2:
            st.markdown("**? Unikaj:**")
            st.markdown("ï Pojedynczych zdaÒ")
            st.markdown("ï Zbyt ogÛlnych opisÛw")
            st.markdown("ï Danych osobowych")
            
        with tip_col3:
            st.markdown("**?? Minimalna iloúÊ:**")
            st.markdown("ï Przynajmniej 2 pola wype≥nione")
            st.markdown("ï Po 3-5 zdaÒ w kaødym")
            st.markdown("ï £πcznie ~200 s≥Ûw")
        
        # Licznik s≥Ûw i status gotowoúci
        all_conversations = [team_conversations, feedback_conversations, conflict_conversations, motivation_conversations]
        filled_fields = sum(1 for conv in all_conversations if conv.strip())
        total_words = sum(len(conv.split()) for conv in all_conversations if conv.strip())
        
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        with col_stats1:
            st.metric("Wype≥nione pola", f"{filled_fields}/4")
        with col_stats2:
            st.metric("£πczna liczba s≥Ûw", total_words)
        with col_stats3:
            if filled_fields >= 2 and total_words >= 150:
                st.success("? Gotowe do analizy!")
            elif total_words < 150:
                st.warning(f"? Potrzeba jeszcze {150-total_words} s≥Ûw")
            else:
                st.info("?? Wype≥nij wiÍcej pÛl")
        
        # Pole na nazwÍ profilu (opcjonalne)
        profile_name = st.text_input(
            "?? Nazwa profilu (opcjonalnie):",
            placeholder="np. 'Paüdziernik 2024' lub 'Po szkoleniu C-IQ'",
            help="Opcjonalna nazwa u≥atwiajπca rozpoznanie profilu w przysz≥oúci"
        )
        
        # Przycisk analizy
        analysis_ready = filled_fields >= 2 and total_words >= 150
        if zen_button("?? Analizuj MÛj Styl PrzywÛdztwa", 
                     key="analyze_leadership", 
                     width='stretch',
                     disabled=not analysis_ready):
            conversations_text = "\n---\n".join([conv for conv in all_conversations if conv.strip()])
            
            if conversations_text:
                with st.spinner("?? TworzÍ TwÛj profil przywÛdczy..."):
                    leadership_profile = create_leadership_profile(conversations_text)
                    if leadership_profile:
                        st.session_state['leadership_profile'] = leadership_profile
                        
                        # Auto-zapis profilu dla zalogowanego uøytkownika
                        if hasattr(st.session_state, 'username') and st.session_state.username:
                            profile_title = profile_name.strip() if (profile_name and profile_name.strip()) else None
                            if save_leadership_profile(st.session_state.username, leadership_profile, profile_title):
                                saved_name = profile_title or f"Profil {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                                st.success(f"? Profil '{saved_name}' gotowy i zapisany! Zobacz zak≥adkÍ 'Profil PrzywÛdczy'")
                            else:
                                st.success("? Profil przywÛdczy gotowy! Zobacz zak≥adkÍ 'Profil PrzywÛdczy'")
                                st.warning("?? Nie uda≥o siÍ zapisaÊ profilu do pliku")
                        else:
                            st.success("? Profil przywÛdczy gotowy! Zobacz zak≥adkÍ 'Profil PrzywÛdczy'")
                            st.info("?? Zaloguj siÍ, aby automatycznie zapisywaÊ swoje profile")
            else:
                st.warning("?? Dodaj przynajmniej jeden fragment rozmowy do analizy")
    
    with tab2:
        # Sekcja zarzπdzania zapisanymi profilami
        if hasattr(st.session_state, 'username') and st.session_state.username:
            st.markdown("### ?? Twoje zapisane profile")
            
            profiles_history = get_user_profiles_history(st.session_state.username)
            if profiles_history:
                st.markdown(f"**?? Masz {len(profiles_history)} zapisanych profili:**")
                
                # Lista profili do wyboru
                for i, profile in enumerate(profiles_history):
                    col_info, col_actions = st.columns([3, 1])
                    
                    with col_info:
                        profile_name = profile.get('profile_name', f'Profil {i+1}')
                        profile_date = profile.get('created_at', 'Nieznana data')[:16].replace('T', ' ')
                        dominant_level = profile.get('dominant_ciq_level', '?')
                        
                        # Sprawdü czy to aktualnie wczytany profil
                        is_current = ('leadership_profile' in st.session_state and 
                                    st.session_state['leadership_profile'].get('created_at') == profile.get('created_at'))
                        
                        if is_current:
                            st.success(f"? **{profile_name}** (aktualnie wczytany)")
                        else:
                            st.info(f"?? **{profile_name}**")
                        
                        st.caption(f"?? {profile_date} | ?? Poziom dominujπcy: {dominant_level}")
                        
                    with col_actions:
                        if not is_current:
                            if zen_button("?? Wczytaj", key=f"load_profile_{i}"):
                                st.session_state['leadership_profile'] = profile
                                st.success(f"? Wczytano profil: {profile_name}")
                                st.rerun()
                        
                        if zen_button("??? UsuÒ", key=f"delete_profile_{i}"):
                            if delete_user_profile(st.session_state.username, i):
                                if is_current:
                                    del st.session_state['leadership_profile']
                                st.success(f"??? UsuniÍto profil: {profile_name}")
                                st.rerun()
                    
                    st.markdown("---")
            else:
                st.info("?? Nie masz jeszcze øadnych zapisanych profili")
                st.markdown("?? Po stworzeniu pierwszego profilu zostanie automatycznie zapisany")
        else:
            st.info("?? Zaloguj siÍ, aby automatycznie zapisywaÊ swoje profile")
            
        st.markdown("---")
        
        if 'leadership_profile' in st.session_state:
            # Przycisk eksportu PDF
            col_export, col_info = st.columns([1, 3])
            with col_export:
                if zen_button("?? Eksportuj PDF", key="export_leadership_pdf"):
                    try:
                        username = getattr(st.session_state, 'username', 'Uøytkownik')
                        pdf_data = generate_leadership_pdf(st.session_state['leadership_profile'], username)
                        
                        # Przygotuj nazwÍ pliku
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"raport_przywodczy_{username}_{timestamp}.pdf"
                        
                        st.download_button(
                            label="?? Pobierz raport",
                            data=pdf_data,
                            file_name=filename,
                            mime="application/pdf",
                            key="download_pdf"
                        )
                        st.success("? Raport PDF gotowy do pobrania!")
                        
                    except Exception as e:
                        st.error(f"? B≥πd podczas generowania PDF: {str(e)}")
            
            with col_info:
                st.info("?? Eksport zawiera pe≥ny raport przywÛdczy + plan rozwoju")
            
            st.markdown("---")
            
            display_leadership_profile(st.session_state['leadership_profile'])
        else:
            st.info("?? Najpierw wgraj dane w zak≥adce 'Upload Danych'")
            
    with tab3:
        if 'leadership_profile' in st.session_state:
            display_leadership_development_plan(st.session_state['leadership_profile'])
        else:
            st.info("?? Profil przywÛdczy jest potrzebny do stworzenia planu rozwoju")

# ===============================================
# BUSINESS CONVERSATION SIMULATOR - TYMCZASOWO WY£•CZONY
# ===============================================
# Funkcje symulatora zosta≥y tymczasowo wy≥πczone z powodu b≥ÍdÛw parsowania.
# Pe≥na dokumentacja koncepcji w: docs/BUSINESS_SIMULATOR_CONCEPT.md
# Kod zostanie przepisany od nowa w osobnym module.
#
# UsuniÍte funkcje (linie 3690-4817):
# - generate_case_context()
# - get_fallback_context()
# - generate_initial_message()
# - get_fallback_initial_message()
# - generate_conversation_report()
# - generate_fallback_report()
# - generate_conversation_transcript()
# - show_conversation_report()
# - show_business_conversation_simulator() [G£”WNA FUNKCJA - 700+ linii]
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
                    temperature=0.8,  # årednia kreatywnoúÊ
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
        # W razie b≥Ídu uøyj fallbacku
        return get_fallback_context(scenario)

def get_fallback_context(scenario):
    """Zwraca predefiniowany kontekst gdy AI nie dzia≥a"""
    fallback_contexts = {
        "salary_raise": "Jesteú Project Managerem w firmie IT. Pracujesz od 18 miesiÍcy bez podwyøki, a niedawno przejπ≥eú dodatkowe obowiπzki po zwolnionym koledze. S≥ysza≥eú, øe firma ma dobry kwarta≥ finansowy.",
        "difficult_feedback": "Marek pracuje jako Junior Developer. Ostatnio jego projekty sπ opÛünione o úrednio 2 tygodnie, a kod wymaga wielu poprawek. Problem trwa od 3 miesiÍcy. Ma potencja≥, ale wydaje siÍ byÊ przyt≥oczony zadaniami.",
        "team_conflict": "Konflikt miÍdzy Aniπ (Senior Designer) a Tomkiem (Frontend Developer). Problem: Ania czuje øe Tomek ignoruje jej wskazÛwki designerskie i samowolnie zmienia projekty. To trwa od 2 miesiÍcy i wp≥ywa na jakoúÊ produktu. Twoja perspektywa (Ania): czujesz siÍ lekcewaøona i sfrustrowana."
    }
    
    scenario_id = None
    for sid, sc in {"salary_raise": {}, "difficult_feedback": {}, "team_conflict": {}}.items():
        if scenario.get('name') == {"salary_raise": "?? Rozmowa o podwyøkÍ", "difficult_feedback": "?? Feedback dla pracownika", "team_conflict": "? Rozwiπzanie konfliktu"}.get(sid):
            scenario_id = sid
            break
    
    if scenario_id:
        return fallback_contexts.get(scenario_id, "Kontekst rozmowy biznesowej.")
    else:
        return "Kontekst rozmowy biznesowej."

def generate_initial_message(scenario, case_context):
    """Generuje pierwszπ wiadomoúÊ AI uwzglÍdniajπcπ kontekst"""
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
        
        prompt = f"""Jesteú {scenario['ai_role']} w symulacji biznesowej.

KONTEKST SYTUACJI:
{case_context}

TWOJA POSTA∆: {scenario['ai_persona']}

Wygeneruj pierwszπ naturalnπ wypowiedü rozpoczynajπcπ tÍ rozmowÍ. 
- 1-2 zdania
- Naturalny ton odpowiedni do roli
- Moøesz nawiπzaÊ do kontekstu jeúli to naturalne

Tylko treúÊ wypowiedzi, bez opisÛw:"""

        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception:
        return get_fallback_initial_message(scenario)

def get_fallback_initial_message(scenario):
    """Zwraca prostπ pierwszπ wiadomoúÊ jako fallback"""
    fallback_messages = {
        "Szef": "DzieÒ dobry. S≥ucham, o co chodzi? Mam tylko 10 minut.",
        "Pracownik": "CzeúÊ! Co tam? Wszystko w porzπdku?",
        "Cz≥onek zespo≥u": "No dobra, to o co w koÒcu chodzi? I tak nikt mnie tu nie s≥ucha..."
    }
    return fallback_messages.get(scenario.get('ai_role'), "DzieÒ dobry, s≥ucham.")

def generate_conversation_report(messages, scenario, case_context):
    """Generuje koÒcowy raport z rozmowy uøywajπc AI"""
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
        
        # Przygotuj historiÍ rozmowy dla AI
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
OceÒ ca≥π rozmowÍ i wygeneruj raport rozwojowy. ZwrÛÊ JSON:

{{
    "outcome": "Pozytywny|CzÍúciowy|Negatywny",
    "outcome_reason": "1-2 zdania dlaczego taki wynik",
    "strengths": ["mocna strona 1 (konkret, nr wymiany)", "mocna strona 2"],
    "improvements": ["obszar rozwoju 1 (konkret, nr wymiany)", "obszar rozwoju 2"],
    "key_moment": "Najbardziej krytyczny moment rozmowy i dlaczego",
    "next_steps": "Co uøytkownik powinien ÊwiczyÊ dalej"
}}

KRYTERIA OCENY:
- Pozytywny: osiπgniÍto porozumienie, zbudowano rapport, konstruktywne rozwiπzanie
- CzÍúciowy: kompromis, nierozstrzygniÍta kwestia, ale bez eskalacji
- Negatywny: konflikt, pat, przerwanie rozmowy, brak postÍpu

WAØNE:
- Bπdü konkretny: "wymiana 3" zamiast "na poczπtku"
- Doceniaj uøycie Transformacyjnego C-IQ
- ZwrÛÊ uwagÍ na progression - czy poziom C-IQ siÍ poprawia≥?
- Max 15 s≥Ûw na punkt

TYLKO JSON:"""

        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # WyczyúÊ JSON
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
    """Prosty raport gdy AI nie dzia≥a"""
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
        'outcome': 'CzÍúciowy',
        'outcome_reason': 'Rozmowa zosta≥a zakoÒczona.',
        'strengths': ['UkoÒczy≥eú scenariusz', 'PrzeÊwiczy≥eú komunikacjÍ C-IQ'],
        'improvements': ['SprÛbuj wiÍcej pytaÒ otwartych', 'Buduj na odpowiedziach rozmÛwcy'],
        'key_moment': 'Ca≥a rozmowa by≥a Êwiczeniem umiejÍtnoúci.',
        'next_steps': 'SprÛbuj innego scenariusza i zwrÛÊ uwagÍ na poziomy C-IQ.',
        'total_turns': total_turns,
        'ciq_stats': ciq_stats
    }

def generate_conversation_transcript(messages, scenario):
    """Generuje transkrypcjÍ rozmowy w formacie tekstowym"""
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
    
    # Historia rozmowy z analizπ C-IQ
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
            
            # Dodaj analizÍ C-IQ
            if msg.get('ciq_level'):
                ciq = msg['ciq_level']
                level = ciq.get('level', 'Brak')
                is_appropriate = ciq.get('is_appropriate', None)
                
                appropriate_text = ""
                if is_appropriate is not None:
                    appropriate_text = " ? (odpowiedni w kontekúcie)" if is_appropriate else " ? (nieodpowiedni)"
                
                transcript_lines.append(f"   L¶ C-IQ: {level}{appropriate_text}")
                
                # Opcjonalnie dodaj feedback
                feedback = ciq.get('feedback', '')
                if feedback:
                    # SkrÛÊ feedback do 100 znakÛw
                    short_feedback = feedback[:100] + "..." if len(feedback) > 100 else feedback
                    transcript_lines.append(f"   L¶ {short_feedback}")
            
            transcript_lines.append("")
            transcript_lines.append("-" * 60)
            transcript_lines.append("")
    
    transcript_lines.append("=" * 60)
    transcript_lines.append("KONIEC TRANSKRYPCJI")
    transcript_lines.append("=" * 60)
    
    return "\n".join(transcript_lines)

def show_conversation_report(report, scenario):
    """Wyúwietla koÒcowy raport z rozmowy"""
    st.markdown("---")
    st.markdown("## ?? PODSUMOWANIE ROZMOWY")
    st.markdown("?????????????????????????????????")
    
    # Wynik rozmowy z emoji
    outcome_emoji = {
        'Pozytywny': '?',
        'CzÍúciowy': '??',
        'Negatywny': '?'
    }
    outcome = report.get('outcome', 'CzÍúciowy')
    emoji = outcome_emoji.get(outcome, '??')
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"### {emoji} Wynik")
        outcome_color = {
            'Pozytywny': 'green',
            'CzÍúciowy': 'orange',
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
        st.markdown("### ?? Dlaczego?")
        st.info(report.get('outcome_reason', 'Brak opisu'))
    
    # Statystyki
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("?? Wymian", report.get('total_turns', 0))
    
    ciq_stats = report.get('ciq_stats', {})
    with col2:
        st.metric("?? Transformacyjny", ciq_stats.get('Transformacyjny', 0))
    with col3:
        st.metric("?? Pozycyjny", ciq_stats.get('Pozycyjny', 0))
    with col4:
        st.metric("?? Transakcyjny", ciq_stats.get('Transakcyjny', 0))
    
    # Mocne strony
    st.markdown("---")
    st.markdown("### ?? Twoje mocne strony")
    strengths = report.get('strengths', [])
    if strengths:
        for strength in strengths:
            st.success(f"? {strength}")
    else:
        st.info("Brak szczegÛ≥Ûw")
    
    # Obszary rozwoju
    st.markdown("### ?? Obszary do rozwoju")
    improvements = report.get('improvements', [])
    if improvements:
        for improvement in improvements:
            st.warning(f"õ {improvement}")
    else:
        st.info("Brak szczegÛ≥Ûw")
    
    # Kluczowy moment
    st.markdown("---")
    st.markdown("### ?? Kluczowy moment rozmowy")
    st.info(report.get('key_moment', 'Brak analizy'))
    
    # NastÍpne kroki
    st.markdown("### ?? Co dalej?")
    st.success(report.get('next_steps', 'Kontynuuj Êwiczenia z innymi scenariuszami'))
    
    st.markdown("---")
    
    # TRANSKRYPCJA ROZMOWY
    st.markdown("### ?? Transkrypcja rozmowy")
    st.caption("Pe≥ny zapis Twojej rozmowy z analizπ poziomÛw C-IQ")
    
    # Generuj transkrypcjÍ
    messages = st.session_state.get('simulator_messages', [])
    transcript = generate_conversation_transcript(messages, scenario)
    
    # Wyúwietl w expander (domyúlnie zwiniÍty)
    with st.expander("?? Zobacz pe≥nπ transkrypcjÍ", expanded=False):
        st.text(transcript)
        
        # Przycisk do pobrania
        st.download_button(
            label="?? Pobierz transkrypcjÍ (.txt)",
            data=transcript,
            file_name=f"transkrypcja_{scenario['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            help="Zapisz transkrypcjÍ na swoim komputerze"
        )
    
    st.markdown("---")

def show_business_conversation_simulator():
    """Symulator rozmÛw biznesowych z analizπ C-IQ"""
    st.markdown("### ?? Symulator RozmÛw Biznesowych")
    
    # DIAGNOSTYKA - ZAWSZE WIDOCZNA
    try:
        api_key = st.secrets.get("API_KEYS", {}).get("gemini")
        if api_key:
            st.success(f"? API OK - Klucz znaleziony ({len(api_key)} znakÛw) - Uøywam prawdziwego AI")
        else:
            st.error("? BRAK KLUCZA API - Dodaj 'gemini' do secrets w [API_KEYS]")
            st.warning("?? Uøywam prostych odpowiedzi fallback zamiast AI")
    except Exception as e:
        st.error(f"? B£•D SECRETS: {type(e).__name__}: {str(e)}")
        st.warning("?? Nie mogÍ odczytaÊ konfiguracji - uøywam fallback")
    
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
        st.session_state.simulator_max_turns = 10  # Maksymalnie 10 wymian (20 wiadomoúci)
    if 'simulator_completed' not in st.session_state:
        st.session_state.simulator_completed = False
    if 'simulator_final_report' not in st.session_state:
        st.session_state.simulator_final_report = None
    
    # Definicja scenariuszy z promptami do generowania kontekstu
    scenarios = {
        "salary_raise": {
            "name": "?? Rozmowa o podwyøkÍ",
            "description": "Prosisz szefa o podwyøkÍ. TwÛj szef jest wymagajπcy i skupiony na wynikach.",
            "ai_persona": "Jesteú wymagajπcym dyrektorem firmy. Cenisz konkretne wyniki i liczby. Jesteú sceptyczny wobec prÛúb o podwyøkÍ, chyba øe rozmÛwca przedstawi mocne argumenty biznesowe. Nie jesteú wrogi, ale wymagasz przekonujπcych dowodÛw wartoúci pracownika.",
            "ai_role": "Szef",
            "user_role": "Pracownik",
            "context_prompt": """Wygeneruj krÛtki (3-4 zdania), konkretny kontekst biznesowy dla rozmowy pracownik-szef o podwyøkÍ:
- Nazwa stanowiska pracownika
- Branøa/firma
- Dlaczego pracownik chce podwyøki (np. rok bez podwyøki, nowe obowiπzki, oferta z innej firmy)
- Dodatkowy szczegÛ≥ zwiÍkszajπcy trudnoúÊ (np. firma ma trudnoúci finansowe, ostatnio by≥o zwolnienie kogoú)

Odpowiedz TYLKO kontekstem, bez dodatkÛw. Format: "Jesteú [stanowisko] w [firma/branøa]. [sytuacja]. [wyzwanie]."
"""
        },
        "difficult_feedback": {
            "name": "?? Feedback dla pracownika",
            "description": "Musisz przekazaÊ trudny feedback pracownikowi, ktÛry nie spe≥nia oczekiwaÒ.",
            "ai_persona": "Jesteú pracownikiem, ktÛry nie zdaje sobie sprawy z problemÛw w swojej pracy. Poczπtkowo moøesz byÊ defensywny, ale jeúli rozmÛwca uøyje empatii i konkretÛw (poziom Transformacyjny C-IQ), stajesz siÍ otwarty na feedback.",
            "ai_role": "Pracownik",
            "user_role": "Menedøer",
            "context_prompt": """Wygeneruj krÛtki (3-4 zdania), konkretny kontekst dla trudnej rozmowy feedbackowej:
- ImiÍ pracownika i stanowisko
- Konkretny problem z wydajnoúciπ (np. spÛünione projekty, konflikty w zespole, b≥Ídy w pracy)
- Jak d≥ugo problem trwa
- Dodatkowy kontekst (np. pracownik ma potencja≥ ale ostatnio siÍ pogubi≥, albo nie przyjmuje feedbacku)

Odpowiedz TYLKO kontekstem. Format: "[ImiÍ] pracuje jako [stanowisko]. Problem: [konkret]. [dodatkowy szczegÛ≥]."
"""
        },
        "team_conflict": {
            "name": "? Rozwiπzanie konfliktu",
            "description": "DwÛch cz≥onkÛw zespo≥u ma konflikt. Musisz pomÛc im siÍ porozumieÊ.",
            "ai_persona": "Jesteú sfrustrowanym cz≥onkiem zespo≥u, ktÛry czuje siÍ niedoceniony. Jesteú lekko agresywny i obwiniasz innych. Moøesz siÍ uspokoiÊ tylko jeúli rozmÛwca wykaøe empatiÍ i pomoøe znaleüÊ wspÛlne rozwiπzanie (C-IQ Transformacyjny).",
            "ai_role": "Cz≥onek zespo≥u",
            "user_role": "Mediator",
            "context_prompt": """Wygeneruj krÛtki (3-4 zdania), konkretny kontekst konfliktu zespo≥owego:
- Imiona dwÛch skonfliktowanych osÛb i ich role
- O co dok≥adnie chodzi w konflikcie (np. podzia≥ zadaÒ, rÛøne style pracy, nieporozumienie)
- Jak d≥ugo to trwa i jaki ma wp≥yw na zespÛ≥
- Perspektywa osoby z ktÛrπ rozmawiasz (czuje siÍ niedoceniona/wykorzystana)

Odpowiedz TYLKO kontekstem. Format: "Konflikt miÍdzy [osoba1] a [osoba2]. Problem: [konkret]. Twoja perspektywa: [uczucia]."
"""
        },
        "delegation": {
            "name": "?? Delegowanie zadania",
            "description": "Delegujesz waøne zadanie pracownikowi, ktÛry ma juø duøe obciπøenie pracπ.",
            "ai_persona": "Jesteú przeciπøonym pracownikiem, ktÛry ma juø pe≥ne rÍce roboty. Czujesz siÍ zmÍczony i obawiasz siÍ, øe kolejne zadanie CiÍ przyt≥oczy. Jesteú otwarty na rozmowÍ, ale potrzebujesz wsparcia i jasnych priorytetÛw.",
            "ai_role": "Pracownik",
            "user_role": "Menedøer",
            "context_prompt": """Wygeneruj krÛtki (3-4 zdania), konkretny kontekst delegowania zadania:
- ImiÍ pracownika i jego stanowisko
- Jakie zadanie chcesz delegowaÊ i dlaczego jest waøne
- Obecne obciπøenie pracownika (np. 3 projekty rÛwnoczeúnie, deadline za tydzieÒ)
- Dodatkowy szczegÛ≥ (np. brak innej osoby do zadania, klient czeka)

Odpowiedz TYLKO kontekstem. Format: "Chcesz delegowaÊ [zadanie] do [imiÍ]. Obecna sytuacja: [obciπøenie]. [wyzwanie]."
"""
        },
        "motivation": {
            "name": "?? Motywowanie zdemotywowanego",
            "description": "Pracownik straci≥ motywacjÍ i rozwaøa zmianÍ pracy. Musisz go zmotywowaÊ.",
            "ai_persona": "Jesteú zdemotywowanym pracownikiem, ktÛry czuje siÍ wypalony i niedoceniany. Praca przesta≥a CiÍ inspirowaÊ. Jesteú otwarty na rozmowÍ, ale potrzebujesz szczeroúci, zrozumienia i konkretnych zmian, nie pustych obietnic.",
            "ai_role": "Pracownik",
            "user_role": "Menedøer",
            "context_prompt": """Wygeneruj krÛtki (3-4 zdania), konkretny kontekst rozmowy motywacyjnej:
- ImiÍ pracownika i stanowisko
- Dlaczego straci≥ motywacjÍ (np. rutyna, brak rozwoju, nieudane projekty)
- Jak d≥ugo to trwa i jakie sπ objawy (np. gorsze wyniki, brak zaangaøowania)
- Dodatkowy kontekst (np. dosta≥ ofertÍ z innej firmy, jest wartoúciowym pracownikiem)

Odpowiedz TYLKO kontekstem. Format: "[ImiÍ] jest [stanowisko]. Problem: [demotywacja]. [sygna≥y i sytuacja]."
"""
        },
        "change_resistance": {
            "name": "?? OpÛr wobec zmian",
            "description": "Przekonujesz zespÛ≥ do duøej zmiany organizacyjnej, na ktÛrπ sπ opory.",
            "ai_persona": "Jesteú sceptycznym cz≥onkiem zespo≥u, ktÛry obawia siÍ zmian. Masz doúwiadczenie z nieudanymi zmianami w przesz≥oúci. Jesteú ostroøny i potrzebujesz przekonujπcych argumentÛw oraz poczucia bezpieczeÒstwa.",
            "ai_role": "Cz≥onek zespo≥u",
            "user_role": "Lider zmiany",
            "context_prompt": """Wygeneruj krÛtki (3-4 zdania), konkretny kontekst wprowadzania zmiany:
- Jaka zmiana jest wprowadzana (np. nowy system, restrukturyzacja, nowa metodologia)
- Dlaczego zespÛ≥ siÍ obawia (np. poprzednie z≥e doúwiadczenia, niepewnoúÊ)
- Jakie sπ realne obawy (np. wiÍcej pracy, utrata kontroli, zwolnienia)
- Twoja perspektywa jako cz≥onka zespo≥u

Odpowiedz TYLKO kontekstem. Format: "Firma wprowadza [zmiana]. Twoje obawy: [konkret]. [dodatkowy kontekst]."
"""
        },
        "difficult_client": {
            "name": "?? Rozmowa z trudnym klientem",
            "description": "Klient jest niezadowolony z realizacji projektu i grozi rezygnacjπ.",
            "ai_persona": "Jesteú sfrustrowanym klientem, ktÛry czuje øe jego projekt jest zaniedbywany. Jesteú niezadowolony z komunikacji i wynikÛw. Moøesz byÊ osch≥y i wymagajπcy, ale jeúli zobaczysz autentycznπ chÍÊ rozwiπzania problemu, stajesz siÍ bardziej otwarty.",
            "ai_role": "Klient",
            "user_role": "Account Manager",
            "context_prompt": """Wygeneruj krÛtki (3-4 zdania), konkretny kontekst rozmowy z trudnym klientem:
- Nazwa klienta/firmy i branøa
- Co posz≥o nie tak w projekcie (np. opÛünienie, b≥Ídy, z≥a komunikacja)
- Jak powaøna jest sytuacja (np. klient grozi odejúciem, z≥e recenzje)
- Dodatkowy kontekst (np. duøy kontrakt, prestiøowy klient)

Odpowiedz TYLKO kontekstem. Format: "Klient [nazwa] z branøy [branøa]. Problem: [konkret]. Sytuacja: [powaga]."
"""
        },
        "negotiation": {
            "name": "?? Negocjacje warunkÛw",
            "description": "Negocjujesz warunki wspÛ≥pracy z wymagajπcym partnerem biznesowym.",
            "ai_persona": "Jesteú twardym negocjatorem, ktÛry zna swojπ wartoúÊ. Chcesz najlepszych warunkÛw i nie boisz siÍ odejúÊ, jeúli oferta nie jest satysfakcjonujπca. Szanujesz profesjonalizm i konkretne argumenty biznesowe.",
            "ai_role": "Partner biznesowy",
            "user_role": "Negocjator",
            "context_prompt": """Wygeneruj krÛtki (3-4 zdania), konkretny kontekst negocjacji biznesowych:
- Kim jest partner (firma, branøa, skala dzia≥alnoúci)
- Co jest przedmiotem negocjacji (np. cena, terminy, zakres wspÛ≥pracy)
- Jakie sπ kluczowe punkty sporne (np. budøet, harmonogram, warunki p≥atnoúci)
- Dodatkowy kontekst (np. partner ma alternatywne oferty, presja czasowa)

Odpowiedz TYLKO kontekstem. Format: "Negocjujesz z [partner] ws. [przedmiot]. Punkt sporny: [konkret]. [sytuacja]."
"""
        }
    }
    
    # WybÛr scenariusza - NOWA KONSTRUKCJA Z SELECTBOX
    if not st.session_state.simulator_started:
        st.markdown("### ?? Wybierz scenariusz rozmowy:")
        
        # Przygotuj opcje dla selectbox
        scenario_options = {scenario['name']: scenario_id for scenario_id, scenario in scenarios.items()}
        
        # Selectbox z opisem wybranego scenariusza
        selected_name = st.selectbox(
            "Scenariusz:",
            options=list(scenario_options.keys()),
            key="scenario_selector",
            help="Wybierz typ rozmowy biznesowej, ktÛrπ chcesz przeÊwiczyÊ"
        )
        
        # Pobierz wybrany scenariusz
        selected_id = scenario_options[selected_name]
        selected_scenario = scenarios[selected_id]
        
        # Wyúwietl szczegÛ≥y wybranego scenariusza
        st.markdown("---")
        with st.container():
            st.markdown(f"#### {selected_scenario['name']}")
            st.info(f"?? **Scenariusz:** {selected_scenario['description']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Twoja rola:** {selected_scenario['user_role']}")
            with col2:
                st.markdown(f"**RozmÛwca:** {selected_scenario['ai_role']}")
            
            st.markdown("")
            if st.button("?? Rozpocznij symulacjÍ", type="primary", width="stretch", key=f"start_{selected_id}"):
                st.session_state.simulator_scenario = selected_id
                st.session_state.simulator_started = True
                st.session_state.simulator_waiting_for_next = False  # Reset flagi
                
                # Zaloguj rozpoczÍcie symulatora i przyznaj XP
                try:
                    from data.users import award_xp_for_activity
                    award_xp_for_activity(
                        st.session_state.username,
                        'tool_used',
                        1,  # 1 XP za uøycie narzÍdzia
                        {
                            'tool_name': 'Business Conversation Simulator',
                            'scenario': selected_id,
                            'scenario_name': selected_scenario['name']
                        }
                    )
                except Exception:
                    pass
                
                # Generuj kontekst case study
                with st.spinner("?? GenerujÍ kontekst scenariusza..."):
                    case_context = generate_case_context(selected_scenario)
                    st.session_state.simulator_case_context = case_context
                    
                    # Wygeneruj pierwszπ wiadomoúÊ AI z kontekstem
                    initial_message = generate_initial_message(selected_scenario, case_context)
                    st.session_state.simulator_messages = [
                        {"role": "ai", "content": initial_message, "ciq_level": None}
                    ]
                
                st.rerun()
        
        # Instrukcja
        st.markdown("---")
        st.markdown("#### ?? Poziomy C-IQ (Conversational Intelligence):")
        
        ciq_col1, ciq_col2, ciq_col3 = st.columns(3)
        
        with ciq_col1:
            st.markdown("""
            **?? Transakcyjny**
            - Wymiana informacji
            - "Ty mÛwisz - ja s≥ucham"
            - Brak g≥Íbszego dialogu
            - Przyk≥ad: _"ChcÍ podwyøki o 20%"_
            """)
        
        with ciq_col2:
            st.markdown("""
            **?? Pozycyjny**
            - Obrona swojej pozycji
            - Walka o racjÍ
            - "Ja vs. Ty"
            - Przyk≥ad: _"Zas≥ugujÍ na wiÍcej, bo inni zarabiajπ wiÍcej"_
            """)
        
        with ciq_col3:
            st.markdown("""
            **?? Transformacyjny**
            - WspÛ≥tworzenie rozwiπzaÒ
            - Empatia i zrozumienie
            - "My razem"
            - Przyk≥ad: _"Jak moøemy wspÛlnie znaleüÊ rozwiπzanie?"_
            """)
        
        return
    
    # Aktywna symulacja
    scenario_id = st.session_state.simulator_scenario
    if not scenario_id:
        return
    scenario = scenarios[scenario_id]
    
    # SPRAWDè CZY ROZMOWA ZAKO—CZONA - jeúli tak, pokaø raport
    if st.session_state.simulator_completed and st.session_state.simulator_final_report:
        show_conversation_report(st.session_state.simulator_final_report, scenario)
        
        # Przyciski: nowy scenariusz lub zamknij
        col1, col2 = st.columns(2)
        with col1:
            if st.button("?? SprÛbuj innego scenariusza", type="primary", width="stretch"):
                st.session_state.simulator_started = False
                st.session_state.simulator_messages = []
                st.session_state.simulator_scenario = None
                st.session_state.simulator_case_context = None
                st.session_state.simulator_waiting_for_next = False
                st.session_state.simulator_completed = False
                st.session_state.simulator_final_report = None
                st.rerun()
        with col2:
            if st.button("? Zamknij", width="stretch"):
                st.session_state.active_simulator = None
                st.session_state.simulator_started = False
                st.session_state.simulator_messages = []
                st.session_state.simulator_scenario = None
                st.session_state.simulator_case_context = None
                st.session_state.simulator_waiting_for_next = False
                st.session_state.simulator_completed = False
                st.session_state.simulator_final_report = None
                st.rerun()
        
        return  # ZakoÒcz funkcjÍ - nie pokazuj reszty interfejsu
    
    # Oblicz liczbÍ wymian (tylko wiadomoúci uøytkownika)
    user_turns = len([m for m in st.session_state.simulator_messages if m['role'] == 'user'])
    max_turns = st.session_state.simulator_max_turns
    
    # Nag≥Ûwek z nazwπ scenariusza i licznikiem
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"#### {scenario['name']}")
        st.caption(scenario['description'])
    with col2:
        # Licznik wymian
        progress = user_turns / max_turns
        if progress < 0.6:
            color = "?"
        elif progress < 0.8:
            color = "??"
        else:
            color = "??"
        st.metric("Wymiana", f"{color} {user_turns}/{max_turns}")
    with col3:
        # Przycisk zakoÒczenia
        if st.button("?? ZakoÒcz", help="ZakoÒcz rozmowÍ i zobacz raport"):
            # Generuj raport
            with st.spinner("?? GenerujÍ raport..."):
                report = generate_conversation_report(
                    st.session_state.simulator_messages,
                    scenario,
                    st.session_state.simulator_case_context
                )
                st.session_state.simulator_final_report = report
                st.session_state.simulator_completed = True
                
                # Zaloguj ukoÒczenie Êwiczenia AI i przyznaj XP
                try:
                    from data.users import award_xp_for_activity
                    award_xp_for_activity(
                        st.session_state.username,
                        'ai_exercise',
                        15,  # 15 XP za ukoÒczenie Êwiczenia AI
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
    
    # Wyúwietl kontekst case study
    if st.session_state.simulator_case_context:
        with st.expander("?? Kontekst scenariusza", expanded=False):
            st.info(st.session_state.simulator_case_context)
    
    st.markdown("---")
    
    # Wyúwietl historiÍ rozmowy
    for idx, msg in enumerate(st.session_state.simulator_messages):
        if msg['role'] == 'ai':
            with st.chat_message("assistant", avatar="??"):
                st.markdown(msg['content'])
        else:
            with st.chat_message("user", avatar="??"):
                st.markdown(msg['content'])
                if msg.get('ciq_level'):
                    # Wyúwietl analizÍ C-IQ z odpowiednim kolorem
                    level_info = msg['ciq_level']
                    color = level_info.get('color', 'blue')
                    is_appropriate = level_info.get('is_appropriate', None)
                    
                    # Wybierz funkcjÍ Streamlit bazujπc na kolorze i kontekúcie
                    feedback_text = f"?? **C-IQ: {level_info['level']}** - {level_info['feedback']}"
                    
                    if color == 'green':
                        st.success(feedback_text)
                    elif color == 'blue':
                        # Niebieski = odpowiedni w kontekúcie
                        st.info(feedback_text)
                    elif color == 'orange':
                        st.warning(feedback_text)
                    else:  # red
                        st.error(feedback_text) if not is_appropriate else st.info(feedback_text)
                    
                    # Jeúli to ostatnia wiadomoúÊ uøytkownika, pokaø przyciski akcji
                    # Sprawdü czy nastÍpna wiadomoúÊ to odpowiedü AI (wtedy moøemy "powtÛrzyÊ")
                    is_last_user_msg = (idx == len(st.session_state.simulator_messages) - 2 
                                       and idx + 1 < len(st.session_state.simulator_messages)
                                       and st.session_state.simulator_messages[idx + 1]['role'] == 'ai')
                    
                    if is_last_user_msg and not st.session_state.get('simulator_waiting_for_next', False):
                        col1, col2, col3 = st.columns([1, 1, 3])
                        with col1:
                            if st.button("?? PowtÛrz", key=f"retry_{idx}", help="UsuÒ tÍ wypowiedü i sprÛbuj ponownie"):
                                # UsuÒ ostatniπ parÍ wiadomoúci (user + AI)
                                st.session_state.simulator_messages = st.session_state.simulator_messages[:-2]
                                st.rerun()
                        with col2:
                            if st.button("? Dalej", key=f"continue_{idx}", help="Kontynuuj konwersacjÍ"):
                                # Oznacz øe uøytkownik zaakceptowa≥ i chce iúÊ dalej
                                st.session_state.simulator_waiting_for_next = True
                                st.rerun()
    
    # Input uøytkownika - dostÍpny tylko gdy:
    # 1. To poczπtek rozmowy (brak wiadomoúci)
    # 2. Ostatnia wiadomoúÊ to AI (user odpowiedzia≥ na feedback i kliknπ≥ "Dalej")
    # 3. User kliknπ≥ "Dalej" (flaga simulator_waiting_for_next)
    can_send_message = (
        len(st.session_state.simulator_messages) == 0 or  # Poczπtek
        st.session_state.simulator_messages[-1]['role'] == 'ai' or  # Ostatnia to AI
        st.session_state.get('simulator_waiting_for_next', False)  # User kliknπ≥ "Dalej"
    )
    
    if can_send_message:
        # Reset flagi
        if st.session_state.get('simulator_waiting_for_next'):
            st.session_state.simulator_waiting_for_next = False
        
        user_input = st.chat_input("Twoja odpowiedü...")
        
        if user_input:
            # Sprawdü czy to bÍdzie ostatnia wymiana (osiπgniÍcie limitu)
            user_turns = len([m for m in st.session_state.simulator_messages if m['role'] == 'user'])
            will_reach_limit = (user_turns + 1) >= st.session_state.simulator_max_turns
            
            # Analiza C-IQ przed dodaniem do historii
            ciq_analysis = analyze_ciq_level(user_input)
            
            # Generuj odpowiedü AI (PRZED dodaniem wiadomoúci uøytkownika do historii)
            ai_response = generate_ai_response(
                user_input, 
                st.session_state.simulator_messages,  # Historia BEZ obecnej wiadomoúci
                scenario,
                ciq_analysis
            )
            
            # Teraz dodaj wiadomoúÊ uøytkownika
            user_message = {"role": "user", "content": user_input, "ciq_level": ciq_analysis}
            st.session_state.simulator_messages.append(user_message)
            
            # Dodaj odpowiedü AI
            st.session_state.simulator_messages.append({
                "role": "ai", 
                "content": ai_response,
                "ciq_level": None
            })
            
            # Jeúli osiπgniÍto limit, automatycznie zakoÒcz i generuj raport
            if will_reach_limit:
                with st.spinner("?? OsiπgniÍto limit wymian. GenerujÍ raport..."):
                    report = generate_conversation_report(
                        st.session_state.simulator_messages,
                        scenario,
                        st.session_state.simulator_case_context
                    )
                    st.session_state.simulator_final_report = report
                    st.session_state.simulator_completed = True
            
            st.rerun()
    else:
        # Uøytkownik musi przeczytaÊ feedback i wybraÊ akcjÍ
        st.info("?? **Przeczytaj feedback powyøej i wybierz:**\n- ?? **PowtÛrz** - sprÛbuj przeformu≥owaÊ swojπ odpowiedü\n- ? **Dalej** - kontynuuj konwersacjÍ")

def analyze_ciq_level(user_message):
    """Analizuje poziom C-IQ w wiadomoúci uøytkownika za pomocπ AI"""
    
    # Sprawdü czy API jest dostÍpne
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
        
        # Pobierz kontekst rozmowy i historiÍ
        conversation_history = st.session_state.get('simulator_messages', [])
        case_context = st.session_state.get('simulator_case_context', '')
        
        # Zbuduj kontekst ostatnich wymian
        recent_context = "\n".join([
            f"{'AI' if msg['role'] == 'ai' else 'Ty'}: {msg['content']}" 
            for msg in conversation_history[-4:]  # Ostatnie 2 wymiany
        ]) if conversation_history else "Poczπtek rozmowy"
        
        prompt = f"""Przeanalizuj tÍ wypowiedü pod kπtem Conversational Intelligence (C-IQ) w kontekúcie trwajπcej rozmowy:

KONTEKST SYTUACJI:
{case_context if case_context else 'Rozmowa biznesowa'}

OSTATNIE WYPOWIEDZI:
{recent_context}

AKTUALNA WYPOWIEDè: "{user_message}"

POZIOMY C-IQ:
?? **Transakcyjny** - wymiana informacji, pytania o fakty, jasne komunikaty ("co/kiedy/ile")
   õ Odpowiedni gdy: ustalamy fakty, planujemy dzia≥ania, wymieniamy dane
   õ Nieodpowiedni gdy: sytuacja wymaga empatii, rozwiπzania konfliktu, budowania relacji

?? **Pozycyjny** - obrona stanowiska, argumentowanie, "ja vs ty" ("zas≥ugujÍ/powinienem")
   õ Czasem potrzebny gdy: musimy byÊ asertywni, broniÊ granic
   õ Problematyczny gdy: eskaluje konflikt, niszczy zaufanie

?? **Transformacyjny** - wspÛ≥tworzenie, empatia, "my/razem" ("jak moøemy/co myúlisz")
   õ Najlepszy gdy: trudne rozmowy, budowanie relacji, rozwiπzywanie problemÛw
   õ Rzadko nieodpowiedni (moøe byÊ postrzegany jako "za miÍkki" w niektÛrych kulturach)

OceÒ:
1. Jaki to poziom?
2. Czy jest odpowiedni do KONTEKSTU rozmowy?
3. Jak moøna poprawiÊ (jeúli warto)?

Odpowiedz w formacie JSON:
{{
    "level": "Transakcyjny|Pozycyjny|Transformacyjny",
    "is_appropriate": true/false,
    "reasoning": "Dlaczego to ten poziom i czy jest OK w tym kontekúcie",
    "tip": "WskazÛwka - jeúli poziom odpowiedni: 'Dobry wybÛr! ...' lub 'OK w tym momencie, ale...' / jeúli nieodpowiedni: 'SprÛbuj...' "
}}

TYLKO JSON:"""

        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # WyczyúÊ JSON z markdown
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0].strip()
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0].strip()
        
        import json
        result = json.loads(result_text)
        
        # Mapuj kolor bazujπc na poziomie I czy jest odpowiedni
        is_appropriate = result.get("is_appropriate", False)
        level = result["level"]
        
        # Logika kolorÛw:
        # - Transformacyjny: zawsze zielony (prawie zawsze dobry)
        # - Transakcyjny/Pozycyjny: niebieski jeúli odpowiedni, czerwony/pomaraÒczowy jeúli nie
        if level == "Transformacyjny":
            color = "green"
        elif is_appropriate:
            color = "blue"  # Niebieski = OK w tym kontekúcie
        else:
            # Standardowe kolory ostrzegawcze
            color = "red" if level == "Transakcyjny" else "orange"
        
        return {
            "level": result["level"],
            "feedback": f"{result['reasoning']} ?? {result['tip']}",
            "color": color,
            "is_appropriate": is_appropriate
        }
        
    except Exception as e:
        # Fallback na prostπ heurystykÍ
        return analyze_ciq_level_fallback(user_message)

def analyze_ciq_level_fallback(user_message):
    """Prosta heurystyka analizy C-IQ gdy AI nie dzia≥a"""
    user_message_lower = user_message.lower()
    
    # S≥owa kluczowe dla kaødego poziomu
    transformational_keywords = [
        'razem', 'wspÛlnie', 'jak moøemy', 'zrozumiem', 'pomÛø mi zrozumieÊ',
        'jakie masz', 'co myúlisz', 'wspÛ≥praca', 'oboje', 'nasz cel',
        's≥ucham', 'rozumiem', 'doceniam', 'ceniÍ'
    ]
    
    positional_keywords = [
        'ale', 'jednak', 'zas≥ugujÍ', 'powinienem', 'musisz', 'masz obowiπzek',
        'to niesprawiedliwe', 'inni majπ', 'dlaczego ja nie', 'to twoja wina'
    ]
    
    transactional_keywords = [
        'chcÍ', 'potrzebujÍ', 'daj mi', 'kiedy', 'ile', 'co dostanÍ'
    ]
    
    # Analiza obecnoúci s≥Ûw kluczowych
    transformational_score = sum(1 for keyword in transformational_keywords if keyword in user_message_lower)
    positional_score = sum(1 for keyword in positional_keywords if keyword in user_message_lower)
    transactional_score = sum(1 for keyword in transactional_keywords if keyword in user_message_lower)
    
    # Dodatkowe wskaüniki
    has_question = '?' in user_message
    has_we_language = any(word in user_message_lower for word in ['my', 'nam', 'nasz', 'wspÛlnie', 'razem'])
    has_i_focus = any(word in user_message_lower.split()[:3] for word in ['ja', 'chcÍ', 'potrzebujÍ', 'muszÍ'])
    
    # Okreúl poziom
    if transformational_score >= 2 or (has_question and has_we_language):
        return {
            "level": "Transformacyjny",
            "feedback": "åwietnie! Budujesz wspÛ≥pracÍ i pokazujesz empatiÍ. To buduje zaufanie.",
            "color": "green"
        }
    elif positional_score >= 2 or (has_i_focus and positional_score >= 1):
        return {
            "level": "Pozycyjny",
            "feedback": "Bronisz swojej pozycji. ?? SprÛbuj skupiÊ siÍ na wspÛlnych celach zamiast 'ja vs. ty'.",
            "color": "orange"
        }
    else:
        return {
            "level": "Transakcyjny",
            "feedback": "Wymieniasz informacje. ?? Moøesz pog≥ÍbiÊ rozmowÍ pytajπc o perspektywÍ drugiej strony.",
            "color": "red"
        }

def generate_ai_response(user_input, conversation_history, scenario, ciq_analysis):
    """Generuje odpowiedü AI na podstawie kontekstu rozmowy"""
    
    # Sprawdü czy API jest dostÍpne (BEZ wyúwietlania komunikatÛw w UI)
    try:
        api_key = st.secrets.get("API_KEYS", {}).get("gemini")
    except Exception:
        api_key = None
    
    if not api_key:
        # Fallback na prostπ odpowiedü bez AI
        if ciq_analysis['level'] == 'Transformacyjny':
            return "Doceniam twoje podejúcie. Zgadzam siÍ, øe warto to omÛwiÊ szczegÛ≥owo. Co proponujesz?"
        elif ciq_analysis['level'] == 'Pozycyjny':
            return "Rozumiem twÛj punkt widzenia, ale muszÍ spojrzeÊ na to szerzej. Czy moøemy porozmawiaÊ o faktach?"
        else:
            return "Okej, s≥ucham. Opowiedz wiÍcej."
        if ciq_analysis['level'] == 'Transformacyjny':
            return "Doceniam twoje podejúcie. Zgadzam siÍ, øe warto to omÛwiÊ szczegÛ≥owo. Co proponujesz?"
        elif ciq_analysis['level'] == 'Pozycyjny':
            return "Rozumiem twÛj punkt widzenia, ale muszÍ spojrzeÊ na to szerzej. Czy moøemy porozmawiaÊ o faktach?"
        else:
            return "Okej, s≥ucham. Opowiedz wiÍcej."
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # SprÛbuj uøyÊ najbardziej dostÍpnego modelu
        try:
            model = genai.GenerativeModel(
                "gemini-2.0-flash-exp",
                generation_config=genai.GenerationConfig(
                    temperature=0.9,  # Wysoka kreatywnoúÊ
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
        
        # Przygotuj historiÍ rozmowy z odpowiednimi rolami
        history_text = "\n".join([
            f"{scenario.get('ai_role', 'AI') if msg['role'] == 'ai' else scenario.get('user_role', 'Ty')}: {msg['content']}" 
            for msg in conversation_history[-8:]  # Ostatnie 4 wymiany
        ])
        
        # Pobierz kontekst case study jeúli istnieje
        case_context = st.session_state.get('simulator_case_context', '')
        
        # Sprawdü liczbÍ wymian - czy zbliøamy siÍ do koÒca?
        user_turns = len([m for m in conversation_history if m['role'] == 'user']) + 1  # +1 bo obecna
        max_turns = st.session_state.get('simulator_max_turns', 10)
        approaching_end = user_turns >= 6  # Po 6 wymianach sugeruj zakoÒczenie
        
        # Prompt dla AI - z kontekstem case study
        end_hint = ""
        if approaching_end:
            end_hint = "\n\nWSKAZ”WKA: To juø wymiana {}/{}. Subtelnie sugeruj zakoÒczenie rozmowy - np. 'MyúlÍ øe ustaliliúmy...', 'Wydaje mi siÍ øe dobrze by≥oby teraz...', itp.".format(user_turns, max_turns)
        
        prompt = f"""Wcielasz siÍ w rolÍ: {scenario.get('ai_role', 'rozmÛwcy')} w symulacji biznesowej.

KONTEKST SYTUACJI:
{case_context}

TWOJA POSTA∆: {scenario['ai_persona']}

DOTYCHCZASOWA ROZMOWA:
{history_text}

{scenario.get('user_role', 'RozmÛwca').upper()} W£AåNIE POWIEDZIA£: "{user_input}"

Odpowiedz jako {scenario.get('ai_role', 'rozmÛwca')} - naturalnie, bezpoúrednio, w 1-2 zdaniach.

WSKAZ”WKI:
- PamiÍtaj o kontekúcie sytuacji i uøywaj go w odpowiedziach gdy to naturalne
- Jeúli rozmÛwca uøywa s≥Ûw "my", "razem", "wspÛlnie" õ bπdü bardziej otwarty i wspÛ≥pracuj
- Jeúli atakuje lub oskarøa õ bπdü defensywny lub zdecydowany  
- Jeúli zadaje pytanie õ odpowiedz konkretnie na nie
- Zachowuj swojπ postaÊ ale reaguj naturalnie na ton rozmÛwcy
- NIE powtarzaj poprzednich odpowiedzi{end_hint}

Odpowiedü ({scenario.get('ai_role', 'AI')}):"""

        response = model.generate_content(prompt)
        ai_text = response.text.strip()
        
        # ZwrÛÊ odpowiedü AI
        if len(ai_text) > 0:
            return ai_text
        else:
            # Pusta odpowiedü - uøyj fallbacku
            raise Exception("AI zwrÛci≥o pustπ odpowiedü")
        
    except Exception as e:
        # Ciche logowanie b≥Ídu (bez wyúwietlania uøytkownikowi)
        # Moøna dodaÊ print(f"AI Error: {e}") do debugowania lokalnie
        
        # Fallback jeúli API zawiedzie - lepsze odpowiedzi bazowane na C-IQ
        if ciq_analysis['level'] == 'Transformacyjny':
            return "NaprawdÍ doceniam twoje podejúcie. ZastanÛwmy siÍ razem, jak to rozwiπzaÊ."
        elif ciq_analysis['level'] == 'Pozycyjny':
            return "Hmm, widzÍ øe masz swoje zdanie. Ale czy moøemy spojrzeÊ na to z innej perspektywy?"
        else:
            return "Dobrze, co jeszcze chcia≥byú powiedzieÊ?"

def show_simulators():
    """Symulatory komunikacyjne"""
    # Wymuú prze≥adowanie modu≥u w trybie dev
    import sys
    if 'views.simulators.business_simulator_v2' in sys.modules:
        import importlib
        importlib.reload(sys.modules['views.simulators.business_simulator_v2'])
    
    from views.simulators.business_simulator_v2 import show_business_simulator
    
    st.markdown("### ?? Symulatory Komunikacyjne")
    st.markdown("Interaktywne symulacje rÛønych scenariuszy komunikacyjnych")
    
    # Siatka symulatorÛw
    col1, col2 = st.columns(2)
    
    with col1:
        business_sim_html = '''
        <div style='padding: 20px; border: 2px solid #9C27B0; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #f3e5f5 0%, #ce93d8 100%);'>
            <h4>?? Symulator RozmÛw Biznesowych v2.0</h4>
            <p><strong>? Nowa wersja z AI-generowanym kontekstem!</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>?? 8 scenariuszy biznesowych</li>
                <li>?? 3 poziomy trudnoúci (≥atwy/úredni/trudny)</li>
                <li>?? AI generuje realistyczny kontekst</li>
                <li>?? Analiza C-IQ + feedback</li>
                <li>?? MoøliwoúÊ poprawiania odpowiedzi</li>
            </ul>
        </div>
        '''
        st.markdown(business_sim_html, unsafe_allow_html=True)
        
        if zen_button("?? Uruchom Symulator v2.0", key="business_simulator", width='stretch'):
            st.session_state.active_simulator = "business_conversation"
    
    with col2:
        negotiation_html = '''
        <div style='padding: 20px; border: 2px solid #795548; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #efebe9 0%, #bcaaa4 100%); opacity: 0.6;'>
            <h4>?? Trener Negocjacji</h4>
            <p><strong>?? W przygotowaniu ??</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>?? Scenariusze negocjacyjne</li>
                <li>?? Techniki C-IQ w negocjacjach</li>
                <li>?? Analiza skutecznoúci</li>
            </ul>
        </div>
        '''
        st.markdown(negotiation_html, unsafe_allow_html=True)
        
        if zen_button("?? Uruchom Trenera", key="negotiation_trainer", width='stretch'):
            st.info("?? W przygotowaniu - trening umiejÍtnoúci negocjacyjnych")
    
    # Wyúwietl aktywny symulator
    active_simulator = st.session_state.get('active_simulator')
    
    if active_simulator == "business_conversation":
        st.markdown("---")
        show_business_simulator()

def show_creative_tools():
    """NarzÍdzia kreatywne i innowacyjne"""
    from views.creative_tools.six_hats_team import show_six_hats_team
    
    st.markdown("### ?? NarzÍdzia Kreatywne")
    st.markdown("Techniki innowacyjnego myúlenia i generowania pomys≥Ûw")
    
    # Siatka narzÍdzi
    col1, col2 = st.columns(2)
    
    with col1:
        six_hats_html = '''
        <div style='padding: 20px; border: 2px solid #FF9800; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #fff3e0 0%, #ffcc80 100%);'>
            <h4>?? Wirtualny ZespÛ≥ Kreatywny</h4>
            <p><strong>6 Kapeluszy de Bono z AI</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>?? Bia≥y - Fakty i dane</li>
                <li>?? Czerwony - Emocje i intuicja</li>
                <li>? Czarny - Ryzyka i problemy</li>
                <li>?? ØÛ≥ty - Szanse i korzyúci</li>
                <li>?? Zielony - Kreatywne pomys≥y</li>
                <li>?? Niebieski - Moderacja i synteza</li>
            </ul>
            <p><strong>? Tryb auto i interaktywny | Konflikty miÍdzy kapeluszami | Portfolio sesji</strong></p>
        </div>
        '''
        st.markdown(six_hats_html, unsafe_allow_html=True)
        
        if zen_button("?? Uruchom ZespÛ≥ Kreatywny", key="six_hats_team", width='stretch'):
            st.session_state.active_creative_tool = "six_hats"
    
    with col2:
        brainstorm_html = '''
        <div style='padding: 20px; border: 2px solid #3F51B5; border-radius: 15px; margin: 10px 0; background: linear-gradient(135deg, #e8eaf6 0%, #9fa8da 100%); opacity: 0.6;'>
            <h4>?? AI Brainstorm Facilitator</h4>
            <p><strong>?? W przygotowaniu ??</strong></p>
            <ul style='margin: 10px 0; padding-left: 20px;'>
                <li>? Facylitacja burzy mÛzgÛw</li>
                <li>?? SCAMPER, Mind Mapping</li>
                <li>?? Generowanie innowacji</li>
            </ul>
        </div>
        '''
        st.markdown(brainstorm_html, unsafe_allow_html=True)
        
        if zen_button("?? Uruchom Brainstorm", key="brainstorm_tool", width='stretch'):
            st.info("?? W przygotowaniu - zaawansowany facylitator burzy mÛzgÛw")
    
    # Wyúwietl aktywne narzÍdzie
    active_tool = st.session_state.get('active_creative_tool')
    
    if active_tool == "six_hats":
        st.markdown("---")
        show_six_hats_team()

def show_analytics():
    """Analityki i tracking postÍpÛw"""
    st.markdown("### ?? Analityki i Tracking")
    st.markdown("Zaawansowane analityki postÍpÛw w rozwoju umiejÍtnoúci komunikacyjnych")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tracker_html = '''
        <div style='padding: 15px; border: 1px solid #4CAF50; border-radius: 10px; background: #f8fff8;'>
            <h4>?? Tracker PostÍpÛw</h4>
            <p>Monitoruj rozwÛj umiejÍtnoúci C-IQ w czasie</p>
        </div>
        '''
        st.markdown(tracker_html, unsafe_allow_html=True)
        
        if zen_button("?? Zobacz PostÍpy", key="progress_tracker", width='stretch'):
            st.info("?? W przygotowaniu - szczegÛ≥owy tracking postÍpÛw w nauce")
    
    with col2:
        goals_html = '''
        <div style='padding: 15px; border: 1px solid #FF9800; border-radius: 10px; background: #fffbf0;'>
            <h4>?? Cele Rozwoju</h4>
            <p>Ustaw i úledü osobiste cele komunikacyjne</p>
        </div>
        '''
        st.markdown(goals_html, unsafe_allow_html=True)
        
        if zen_button("?? Ustaw Cele", key="development_goals", width='stretch'):
            st.info("?? W przygotowaniu - system celÛw rozwojowych")
    
    with col3:
        report_html = '''
        <div style='padding: 15px; border: 1px solid #2196F3; border-radius: 10px; background: #f0f8ff;'>
            <h4>?? Raport UmiejÍtnoúci</h4>
            <p>Kompleksowy raport Twoich kompetencji</p>
        </div>
        '''
        st.markdown(report_html, unsafe_allow_html=True)
        
        if zen_button("?? Zobacz Raport", key="skills_report", width='stretch'):
            st.info("?? W przygotowaniu - szczegÛ≥owy raport umiejÍtnoúci")

def show_ai_assistant():
    """AI Asystent personalny"""
    st.markdown("### ?? AI Asystent Personalny")
    st.markdown("TwÛj osobisty coach AI do rozwoju umiejÍtnoúci komunikacyjnych")
    
    # Placeholder dla chatbota
    st.info("?? **W przygotowaniu** - inteligentny asystent AI dostÍpny 24/7")
    
    # Demo interfejsu chatbota
    st.markdown("#### ?? Przyk≥ad rozmowy z AI Asystenem:")
    
    # Przyk≥adowe wiadomoúci
    with st.chat_message("assistant"):
        st.markdown("CzeúÊ! Jestem Twoim AI Asystenem do rozwoju komunikacji. W czym mogÍ Ci pomÛc?")
    
    with st.chat_message("user"):
        st.markdown("Jak przygotowaÊ siÍ do trudnej rozmowy z szefem?")
    
    with st.chat_message("assistant"):
        ai_response = '''
        åwietne pytanie! Oto moja strategia oparta na C-IQ:
        
        **?? Przygotowanie:**
        1. Zidentyfikuj cel rozmowy (co chcesz osiπgnπÊ)
        2. Przygotuj pytania otwarte zamiast oskarøeÒ
        3. ZastanÛw siÍ nad wspÛlnymi celami
        
        **?? Podczas rozmowy:**
        - Zacznij od poziomu III: "Chcia≥bym porozmawiaÊ o..."
        - Unikaj jÍzyka "ty" na rzecz "my", "nas"
        - Zadawaj pytania: "Jak widzisz tÍ sytuacjÍ?"
        
        Chcesz przeÊwiczyÊ konkretny scenariusz?
        '''
        st.markdown(ai_response)
    
    # Wy≥πczony input
    chat_input = st.chat_input("Napisz wiadomoúÊ do AI Asystenta...", disabled=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**?? Planowane funkcje:**")
        st.markdown("ï Rozmowy w czasie rzeczywistym")
        st.markdown("ï Personalizowane porady")
        st.markdown("ï Analiza postÍpÛw")
        st.markdown("ï Przypomnienia o Êwiczeniach")
    
    with col2:
        st.markdown("**?? Obszary wsparcia:**")
        st.markdown("ï Przygotowanie do trudnych rozmÛw")
        st.markdown("ï Analiza komunikacji")
        st.markdown("ï Strategie C-IQ")
        st.markdown("ï Budowanie pewnoúci siebie")

# ===============================================
# CONVERSATION INTELLIGENCE PRO - FUNKCJE AI
# ===============================================

def analyze_conversation_sentiment(text: str) -> Optional[Dict]:
    """Analizuje sentiment rozmowy menedøer-pracownik + poziomy C-IQ"""
    evaluator = AIExerciseEvaluator()
    
    prompt = f"""
Jesteú ekspertem w Conversational Intelligence i analizie rozmÛw przywÛdczych miÍdzy menedøerem a pracownikiem.
Przeanalizuj nastÍpujπcπ transkrypcjÍ rozmowy menedøerskiej:

TRANSKRYPCJA:
"{text}"

Przeprowadü kompleksowπ analizÍ z perspektywy przywÛdztwa zawierajπcπ:
1. SENTIMENT ANALYSIS - emocje menedøera i pracownika
2. C-IQ LEVELS - poziomy komunikacji przywÛdczej
3. NEUROBIOLOGICAL IMPACT - wp≥yw na kortyzol/oksytocynÍ w kontekúcie zespo≥u
4. LEADERSHIP INSIGHTS - wnioski dla rozwoju przywÛdztwa

Odpowiedz w formacie JSON:
{{
    "overall_sentiment": "pozytywny/neutralny/negatywny",
    "sentiment_score": [1-10],
    "ciq_analysis": {{
        "manager_level": "Poziom I/II/III",
        "employee_level": "Poziom I/II/III", 
        "leadership_effectiveness": "niska/úrednia/wysoka",
        "conversation_flow": "buduje_zaufanie/neutralna/tworzy_napiÍcie"
    }},
    "emotions_detected": {{
        "manager": ["emocja1", "emocja2"],
        "employee": ["emocja1", "emocja2"]
    }},
    "neurobiological_impact": {{
        "cortisol_triggers": ["sytuacja powodujπca stres"],
        "oxytocin_builders": ["sytuacja budujπca zaufanie"]
    }},
    "leadership_insights": {{
        "team_engagement_risk": [1-10],
        "leadership_effectiveness": [1-10],
        "key_moments": ["waøny moment w rozmowie przywÛdczej"],
        "development_opportunities": ["obszar rozwoju przywÛdztwa"]
    }},
    "recommendations": {{
        "immediate_actions": ["natychmiastowe dzia≥anie"],
        "long_term_improvements": ["d≥ugoterminowa poprawa"],
        "coaching_points": ["wskazÛwka dla menedøera"]
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
        st.error(f"? B≥πd analizy sentiment: {str(e)}")
        return create_fallback_sentiment_analysis(text)

def analyze_business_intent(text: str) -> Optional[Dict]:
    """Wykrywa intencje biznesowe w rozmowie"""
    evaluator = AIExerciseEvaluator()
    
    prompt = f"""
Jesteú ekspertem w wykrywaniu intencji biznesowych w rozmowach.
Przeanalizuj nastÍpujπcy tekst pod kπtem potrzeb i motywacji pracownika:

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
    "key_phrases": ["waøna fraza1", "waøna fraza2"]
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
    """Analizuje ryzyko problemÛw zespo≥owych i wypalenia"""
    evaluator = AIExerciseEvaluator()
    
    prompt = f"""
Jesteú ekspertem w wykrywaniu sygna≥Ûw problemÛw zespo≥owych i wypalenia zawodowego w kontekúcie przywÛdztwa.
Czu≥oúÊ wykrywania: {sensitivity}/10 (1=bardzo konserwatywne, 10=bardzo wyczulone)

FRAGMENT ROZMOWY Z PRACOWNIKIEM: "{text}"

Przeanalizuj ryzyko problemÛw zespo≥owych i odpowiedz w JSON:
{{
    "team_problem_risk": [1-10],
    "risk_level": "low/medium/high/critical", 
    "warning_signals": [
        {{
            "signal": "konkretny sygna≥ problemu zespo≥owego",
            "severity": [1-10],
            "fragment": "fragment tekstu pokazujπcy sygna≥"
        }}
    ],
    "employee_state": {{
        "current_emotion": "motywacja/frustracja/wypalenie/zaangaøowanie",
        "engagement_level": [1-10],
        "progression": "improving/stable/deteriorating"
    }},
    "leadership_actions": [
        "rekomendowane dzia≥anie przywÛdcze 1",
        "rekomendowane dzia≥anie przywÛdcze 2"
    ],
    "support_strategies": [
        "strategia wsparcia pracownika 1", 
        "strategia wsparcia pracownika 2"
    ],
    "hr_escalation": {{
        "recommended": true/false,
        "reason": "powÛd przekazania do HR lub wyøszego managementu",
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
    """Generuje coaching przywÛdczy w czasie rzeczywistym dla menedøerÛw"""
    evaluator = AIExerciseEvaluator()
    
    prompt = f"""
Jesteú ekspertem w Conversational Intelligence i coachem przywÛdczym dla menedøerÛw.

TYP ROZMOWY MENEDØERSKIEJ: {context}
OSTATNIA WYPOWIEDè PRACOWNIKA: "{text}"

Zasugeruj najlepszπ odpowiedü menedøerskπ na poziomie III C-IQ (Transformacyjnym), ktÛra buduje zaufanie i zaangaøowanie w zespole.

Odpowiedz w JSON:
{{
    "suggested_responses": [
        {{
            "response": "konkretna sugerowana odpowiedü",
            "ciq_level": "III",
            "rationale": "dlaczego ta odpowiedü jest dobra",
            "expected_outcome": "oczekiwany rezultat"
        }}
    ],
    "alternative_approaches": [
        {{
            "approach": "alternatywne podejúcie",
            "when_to_use": "kiedy uøyÊ tego podejúcia"
        }}
    ],
    "what_to_avoid": [
        "czego unikaÊ w odpowiedzi 1",
        "czego unikaÊ w odpowiedzi 2"
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
        "desired_team_state": "poøπdany stan zespo≥u", 
        "leadership_approach": "jak menedøer moøe wspieraÊ przejúcie do lepszego stanu"
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
# FALLBACK FUNCTIONS (gdy AI nie dzia≥a)
# ===============================================

def create_fallback_sentiment_analysis(text: str) -> Dict:
    """Fallback analiza sentiment gdy AI nie dzia≥a"""
    text_lower = text.lower()
    
    negative_words = ['problem', 'b≥πd', 'nie dzia≥a', 'z≥y', 's≥aby', 'frustracja', 'üle']
    positive_words = ['dobrze', 'super', 'úwietnie', 'dziÍkujÍ', 'pomocy', 'mi≥o']
    
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
            "improvement_opportunities": ["Uøyj wiÍcej pytaÒ otwartych"]
        },
        "recommendations": {
            "immediate_actions": ["Zastosuj techniki C-IQ poziom III"],
            "coaching_points": ["Fokus na wspÛ≥tworzeniu rozwiπzaÒ"]
        }
    }

def create_fallback_intent_analysis(text: str) -> Dict:
    """Fallback analiza intencji"""
    text_lower = text.lower()
    
    development_signals = ['rozwÛj', 'szkolenie', 'nauka', 'kariera', 'awans']
    support_signals = ['pomoc', 'wsparcie', 'trudnoúci', 'przeciπøenie', 'stres']
    
    need = "general_support"
    if any(word in text_lower for word in development_signals):
        need = "development"
    elif any(word in text_lower for word in support_signals):
        need = "support"
        
    return {
        "detected_intents": [{
            "need": need,
            "confidence": 7,
            "evidence": ["Analiza s≥Ûw kluczowych"],
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
    """Fallback analiza problemÛw zespo≥owych"""
    text_lower = text.lower()
    problem_words = ['przeciπøenie', 'stres', 'wypalenie', 'frustracja', 'demotywacja', 'rezygnacja']
    
    problem_count = sum(1 for word in problem_words if word in text_lower)
    risk = min(10, problem_count * sensitivity)
    
    return {
        "team_problem_risk": risk,
        "risk_level": "high" if risk > 7 else "medium" if risk > 4 else "low",
        "warning_signals": [{
            "signal": f"Wykryto {problem_count} sygna≥Ûw problemÛw zespo≥owych",
            "severity": min(8, problem_count * 2)
        }],
        "leadership_actions": [
            "Przeprowadü rozmowÍ 1-on-1 z pracownikiem",
            "Zastosuj techniki C-IQ Poziom III"
        ],
        "support_strategies": [
            "Zaoferuj wsparcie w zarzπdzaniu obciπøeniem",
            "Skup siÍ na wspÛlnych celach zespo≥u"
        ],
        "hr_escalation": {
            "recommended": risk > 8,
            "reason": "Wysokie ryzyko problemÛw zespo≥owych wymagajπcych interwencji HR"
        }
    }

def create_fallback_coaching(context: str) -> Dict:
    """Fallback coaching przywÛdczy"""
    return {
        "suggested_responses": [{
            "response": "Rozumiem Twojπ sytuacjÍ. Jak moøemy wspÛlnie pracowaÊ nad tym wyzwaniem?",
            "ciq_level": "III",
            "rationale": "Pytanie otwarte + jÍzyk wspÛ≥tworzenia + empatia przywÛdcza"
        }],
        "ciq_techniques": [
            "Uøywaj pytaÒ otwartych z pracownikami",
            "JÍzyk 'my' i 'wspÛlnie' zamiast 'ty musisz'",
            "Fokus na wspÛlnych celach zespo≥u"
        ],
        "what_to_avoid": [
            "JÍzyk dyrektywny menedøerski (Poziom I)",
            "Argumentowanie i przekonywanie (Poziom II)"
        ],
        "follow_up_questions": [
            "Co mogÍ zrobiÊ, øeby Ci pomÛc?",
            "Jakie wsparcie by≥oby dla Ciebie najcenniejsze?"
        ],
        "leadership_strategy": {
            "employee_emotion": "analiza w trybie offline",
            "desired_team_state": "zaangaøowany i zmotywowany zespÛ≥",
            "leadership_approach": "coaching i wsparcie zamiast kontroli"
        }
    }

# ===============================================
# LEADERSHIP PROFILE FUNCTIONS
# ===============================================

def create_leadership_profile(conversations_text: str) -> Optional[Dict]:
    """Tworzy d≥ugoterminowy profil przywÛdczy na podstawie wielu rozmÛw"""
    evaluator = AIExerciseEvaluator()
    
    prompt = f"""
Jesteú ekspertem w analizie d≥ugoterminowych wzorcÛw przywÛdczych przez pryzmat Conversational Intelligence.
Przeanalizuj zbiÛr rozmÛw menedøerskich i stwÛrz kompletny profil przywÛdczy.

ZBI”R ROZM”W MENEDØERSKICH:
"{conversations_text}"

StwÛrz d≥ugoterminowy profil przywÛdczy w JSON:
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
        "silna strona przywÛdcza 1",
        "silna strona przywÛdcza 2"
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
    """Fallback profil gdy AI nie dzia≥a - menedøer poziom I-II"""
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
            "language_patterns": ["Polecenia i instrukcje", "Kontrola wykonania", "Wymagania rezultatÛw"],
            "emotional_intelligence": 4
        },
        "neurobiological_impact": {
            "cortisol_triggers": 7,
            "oxytocin_builders": 4,
            "psychological_safety": 4
        },
        "strengths": [
            "Jasne komunikowanie oczekiwaÒ",
            "Zdecydowanie w podejmowaniu decyzji",
            "Orientacja na wyniki",
            "Reagowanie na problemy operacyjne"
        ],
        "development_areas": [
            "Redukcja stylu dyrektywnego (za duøo poziomu I)",
            "Rozwijanie umiejÍtnoúci s≥uchania aktywnego",
            "WiÍcej pytaÒ otwartych zamiast poleceÒ",
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
    """Bezpieczne pobieranie wartoúci liczbowej z domyúlnπ wartoúciπ"""
    value = data.get(key, default)
    return default if value is None else value

def generate_leadership_pdf(profile: Dict, username: str) -> bytes:
    """Generuje raport przywÛdczy w formacie PDF"""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import os
    
    # UtwÛrz buffer dla PDF
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
        print(f"B≥πd ≥adowania fontu: {e}")
        unicode_font = 'Times-Roman'
        unicode_font_bold = 'Times-Bold'
    
    # Konfiguracja dokumentu PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Style tekstu z obs≥ugπ polskich znakÛw
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
    
    # ZawartoúÊ PDF
    story = []
    
    # Upewnij siÍ, øe wszystkie stringi sπ w UTF-8 z polskimi znakami
    def ensure_unicode(text):
        if text is None:
            return ""
        if isinstance(text, (int, float)):
            return str(text)
        
        # Konwertuj na string i zachowaj polskie znaki
        text_str = str(text)
        
        # Upewnij siÍ, øe string jest w UTF-8
        try:
            if isinstance(text_str, bytes):
                text_str = text_str.decode('utf-8', errors='ignore')
            else:
                # Test enkodowania - jeúli siÍ udaje, znaczy øe string jest OK
                text_str.encode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            # Fallback - usuÒ problematyczne znaki
            text_str = str(text).encode('utf-8', errors='ignore').decode('utf-8')
            
        return text_str
    
    # Nag≥Ûwek
    story.append(Paragraph(ensure_unicode("?? Raport PrzywÛdczy C-IQ"), title_style))
    story.append(Paragraph(f"<b>Uøytkownik:</b> {ensure_unicode(username)}", normal_style))
    story.append(Paragraph(f"<b>Data wygenerowania:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
    story.append(Spacer(1, 20))
    
    # Sekcja 1: Dominujπcy poziom
    story.append(Paragraph(ensure_unicode("?? Dominujπcy Poziom C-IQ"), subtitle_style))
    dominant_level = ensure_unicode(profile.get('dominant_ciq_level', 'Brak danych'))
    story.append(Paragraph(f"<b>{dominant_level}</b>", normal_style))
    story.append(Spacer(1, 15))
    
    # Sekcja 2: Rozk≥ad poziomÛw
    story.append(Paragraph(ensure_unicode("?? Rozk≥ad PoziomÛw C-IQ"), subtitle_style))
    distribution = profile.get('ciq_distribution', {})
    
    level_data = [
        [ensure_unicode('Poziom'), ensure_unicode('WartoúÊ')],
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
    story.append(Paragraph(ensure_unicode("?? Wp≥yw Neurobiologiczny"), subtitle_style))
    neurobiological = profile.get('neurobiological_impact', {})
    
    neuro_data = [
        [ensure_unicode('Aspekt'), ensure_unicode('Poziom (1-10)')],
        [ensure_unicode('Wyzwalacze kortyzolu'), str(safe_get_numeric(neurobiological, 'cortisol_triggers', 5))],
        [ensure_unicode('Budowanie oksytocyny'), str(safe_get_numeric(neurobiological, 'oxytocin_builders', 5))],
        [ensure_unicode('BezpieczeÒstwo psychologiczne'), str(safe_get_numeric(neurobiological, 'psychological_safety', 5))]
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
    story.append(Paragraph("?? Mocne Strony", subtitle_style))
    strengths = profile.get('strengths', ['Brak danych'])
    for strength in strengths[:5]:  # Max 5 pozycji
        story.append(Paragraph(f"ï {ensure_unicode(strength)}", normal_style))
    story.append(Spacer(1, 15))
    
    # Sekcja 5: Obszary rozwoju
    story.append(Paragraph(ensure_unicode("?? Obszary Rozwoju"), subtitle_style))
    development_areas = profile.get('development_areas', ['Brak danych'])
    for area in development_areas[:5]:  # Max 5 pozycji  
        story.append(Paragraph(f"ï {ensure_unicode(area)}", normal_style))
    story.append(Spacer(1, 20))
    
    # Nowa strona dla planu rozwoju
    story.append(PageBreak())
    story.append(Paragraph(ensure_unicode("?? Plan Rozwoju PrzywÛdczego"), title_style))
    story.append(Spacer(1, 20))
    
    # Plan rozwoju - cele
    level_iii = safe_get_numeric(profile.get('ciq_distribution', {}), 'level_iii_percentage', 20)
    target_level_iii = min(level_iii + 20, 80)
    
    story.append(Paragraph("?? Cele Rozwojowe", subtitle_style))
    story.append(Paragraph(f"<b>Aktualny poziom transformacyjny:</b> {level_iii}%", normal_style))
    story.append(Paragraph(f"<b>Docelowy poziom transformacyjny:</b> {target_level_iii}%", normal_style))
    story.append(Paragraph(f"<b>Wymagany wzrost:</b> +{target_level_iii - level_iii}%", normal_style))
    story.append(Spacer(1, 15))
    
    # Rekomendacje
    story.append(Paragraph("?? Kluczowe Rekomendacje", subtitle_style))
    
    recommendations = [
        "Praktykuj zadawanie pytaÒ otwartych zamiast zamkniÍtych",
        "Rozwijaj umiejÍtnoúci aktywnego s≥uchania", 
        "Wprowadzaj wiÍcej empatii w codziennej komunikacji",
        "Eksperymentuj z rÛønymi stylami komunikacyjnymi",
        "Regularne sesje feedbacku z zespo≥em"
    ]
    
    for rec in recommendations:
        story.append(Paragraph(f"ï {ensure_unicode(rec)}", normal_style))
    
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
    
    # ZwrÛÊ dane PDF
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def display_leadership_profile(profile: Dict):
    """Wyúwietla profil przywÛdczy"""
    st.markdown("## ?? TwÛj Profil PrzywÛdczy C-IQ")
    
    # G≥Ûwne metryki
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        dominant_level = profile.get('dominant_ciq_level', 'II')
        st.metric("?? Dominujπcy poziom C-IQ", f"Poziom {dominant_level}")
        
    with col2:
        leadership_style = profile.get('leadership_style', {})
        style = leadership_style.get('primary_style', 'collaborative')
        st.metric("?? Styl przywÛdztwa", style.title())
        
    with col3:
        team_impact = profile.get('team_impact', {})
        engagement = team_impact.get('predicted_engagement', 6)
        if engagement is None:
            engagement = 6
        st.metric("?? Wp≥yw na zaangaøowanie", f"{engagement}/10")
        
    with col4:
        trust_building = team_impact.get('trust_building_capability', 6)
        if trust_building is None:
            trust_building = 6
        st.metric("?? Budowanie zaufania", f"{trust_building}/10")
    
    # Rozk≥ad poziomÛw C-IQ
    st.markdown("### ?? Rozk≥ad Twoich poziomÛw C-IQ")
    distribution = profile.get('ciq_distribution', {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        level_i = distribution.get('level_i_percentage', 30)
        if level_i is None:
            level_i = 30
        st.metric("?? Poziom I (Transakcyjny)", f"{level_i}%")
        
    with col2:
        level_ii = distribution.get('level_ii_percentage', 50) 
        if level_ii is None:
            level_ii = 50
        st.metric("?? Poziom II (Pozycyjny)", f"{level_ii}%")
        
    with col3:
        level_iii = distribution.get('level_iii_percentage', 20)
        # Walidacja - upewniamy siÍ øe to liczba
        if level_iii is None:
            level_iii = 20
        st.metric("?? Poziom III (Transformacyjny)", f"{level_iii}%")
        
    # Rekomendacje na podstawie rozk≥adu C-IQ
    st.markdown("#### ?? Rekomendacje na podstawie Twoich poziomÛw C-IQ:")
    
    # Walidacja wszystkich wartoúci przed porÛwnaniem
    level_i = distribution.get('level_i_percentage', 30)
    if level_i is None:
        level_i = 30
    level_ii = distribution.get('level_ii_percentage', 50) 
    if level_ii is None:
        level_ii = 50
    if level_iii is None:
        level_iii = 20
    
    if level_iii < 30:
        st.warning("?? **Prioritet:** ZwiÍksz uøywanie poziomu III - zadawaj wiÍcej pytaÒ otwartych, s≥uchaj aktywnie, wspÛ≥twÛrz rozwiπzania")
    elif level_iii < 50:
        st.info("?? **Kierunek rozwoju:** Kontynuuj pracÍ nad poziomem III - doskona≥ umiejÍtnoúci budowania dialogu")
    else:
        st.success("?? **Gratulacje!** Masz silny poziom III - teraz skup siÍ na konsystentnoúci i rozwijaniu innych")
        
    if level_i > 50:
        st.warning("?? **Uwaga:** Za duøo poziomu I (transakcyjnego) - sprÛbuj wiÍcej s≥uchaÊ niø mÛwiÊ")
        
    if level_ii > 60:
        st.info("?? **WskazÛwka:** Duøo poziomu II - rozwijaj umiejÍtnoúci przejúcia do poziomu III")
    
    # Mocne strony i obszary rozwoju
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ?? Twoje mocne strony przywÛdcze")
        strengths = profile.get('strengths', [])
        for strength in strengths:
            st.markdown(f"? {strength}")
            
    with col2:
        st.markdown("### ?? Obszary do rozwoju")
        development_areas = profile.get('development_areas', [])
        for area in development_areas:
            st.markdown(f"?? {area}")
            
    # Sekcja neurobiologiczna
    st.markdown("### ?? Wp≥yw neurobiologiczny Twojej komunikacji")
    neurobiological = profile.get('neurobiological_impact', {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        cortisol = neurobiological.get('cortisol_triggers', 5)
        if cortisol is None:
            cortisol = 5
        if cortisol <= 3:
            st.success(f"?? **Niski cortyzol** {cortisol}/10")
            st.write("Twoja komunikacja minimalizuje stres")
        elif cortisol <= 7:
            st.warning(f"?? **åredni cortyzol** {cortisol}/10") 
            st.write("Czasami moøesz wywo≥ywaÊ napiÍcie")
        else:
            st.error(f"?? **Wysoki cortyzol** {cortisol}/10")
            st.write("Komunikacja moøe stresowaÊ zespÛ≥")
            
    with col2:
        oxytocin = neurobiological.get('oxytocin_builders', 5)
        if oxytocin is None:
            oxytocin = 5
        if oxytocin >= 7:
            st.success(f"?? **Wysoka oksytocyna** {oxytocin}/10")
            st.write("åwietnie budujesz wiÍzi i zaufanie")
        elif oxytocin >= 4:
            st.info(f"?? **årednia oksytocyna** {oxytocin}/10")
            st.write("Umiarkowanie budujesz relacje") 
        else:
            st.error(f"?? **Niska oksytocyna** {oxytocin}/10")
            st.write("Potrzeba wiÍcej budowania wiÍzi")
            
    with col3:
        safety = neurobiological.get('psychological_safety', 5)
        if safety is None:
            safety = 5
        if safety >= 7:
            st.success(f"?? **Wysokie bezpieczeÒstwo** {safety}/10")
            st.write("ZespÛ≥ czuje siÍ bezpiecznie")
        elif safety >= 4:
            st.info(f"?? **årednie bezpieczeÒstwo** {safety}/10")
            st.write("Jest miejsce na poprawÍ bezpieczeÒstwa")
        else:
            st.error(f"?? **Niskie bezpieczeÒstwo** {safety}/10") 
            st.write("ZespÛ≥ moøe czuÊ siÍ niepewnie")
    
    # Sekcja skutecznoúci komunikacji
    st.markdown("### ?? SkutecznoúÊ Twojej komunikacji")
    
    communication = profile.get('communication_patterns', {})
    team_impact = profile.get('team_impact', {})
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # ClarnoúÊ przekazu - wyliczamy na podstawie poziomu C-IQ
        level_iii = profile.get('ciq_distribution', {}).get('level_iii_percentage', 20)
        if level_iii is None:
            level_iii = 20
        clarity_score = min(10, max(3, int(level_iii / 10 + 3)))
        
        if clarity_score >= 7:
            st.success(f"?? **ClarnoúÊ przekazu** {clarity_score}/10")
            st.write("Komunikujesz jasno i zrozumiale")
        elif clarity_score >= 5:
            st.info(f"?? **ClarnoúÊ przekazu** {clarity_score}/10")
            st.write("Przekaz jest w miarÍ jasny")
        else:
            st.warning(f"?? **ClarnoúÊ przekazu** {clarity_score}/10")
            st.write("Przekaz wymaga uúciúlenia")
            
    with col2:
        trust_potential = team_impact.get('trust_building_capability', 6)
        if trust_potential is None:
            trust_potential = 6
        if trust_potential >= 7:
            st.success(f"?? **Potencja≥ zaufania** {trust_potential}/10")
            st.write("Silnie budujesz zaufanie zespo≥u")
        elif trust_potential >= 5:
            st.info(f"?? **Potencja≥ zaufania** {trust_potential}/10") 
            st.write("Umiarkowanie budujesz zaufanie")
        else:
            st.warning(f"?? **Potencja≥ zaufania** {trust_potential}/10")
            st.write("Zaufanie wymaga wzmocnienia")
            
    with col3:
        # Ryzyko konfliktu - odwrotnoúÊ conflict_resolution
        conflict_resolution = team_impact.get('conflict_resolution', 6)
        if conflict_resolution is None:
            conflict_resolution = 6
        conflict_risk = 10 - conflict_resolution
        
        if conflict_risk <= 3:
            st.success(f"? **Ryzyko konfliktu** {conflict_risk}/10")
            st.write("Bardzo niskie ryzyko konfliktÛw")
        elif conflict_risk <= 6:
            st.info(f"? **Ryzyko konfliktu** {conflict_risk}/10")
            st.write("Umiarkowane ryzyko konfliktÛw") 
        else:
            st.warning(f"? **Ryzyko konfliktu** {conflict_risk}/10")
            st.write("Wysokie ryzyko napiÍÊ w zespole")

def display_leadership_development_plan(profile: Dict):
    """Wyúwietla plan rozwoju przywÛdczego"""
    st.markdown("## ?? TwÛj Plan Rozwoju PrzywÛdczego")
    
    # Analiza obecnego poziomu
    dominant_level = profile.get('dominant_ciq_level', 'II')
    distribution = profile.get('ciq_distribution', {})
    level_iii_percentage = safe_get_numeric(distribution, 'level_iii_percentage', 20)
    
    st.markdown("### ?? Analiza obecnej sytuacji")
    if level_iii_percentage < 30:
        st.warning(f"?? **Poziom III stanowi tylko {level_iii_percentage}%** Twojej komunikacji. To g≥Ûwny obszar rozwoju!")
    elif level_iii_percentage < 50:
        st.info(f"?? **Poziom III: {level_iii_percentage}%** - dobry start, ale jest miejsce na poprawÍ")
    else:
        st.success(f"?? **Poziom III: {level_iii_percentage}%** - úwietny poziom transformacyjnego przywÛdztwa!")
    
    # Plan rozwoju na najbliøsze 3 miesiπce
    st.markdown("### ??? Plan rozwoju - najbliøsze 3 miesiπce")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**?? Cele do osiπgniÍcia:**")
        target_level_iii = min(level_iii_percentage + 20, 80)
        st.markdown(f"ï ZwiÍksz poziom III z {level_iii_percentage}% do {target_level_iii}%")
        st.markdown("ï Stosuj wiÍcej pytaÒ otwartych")
        st.markdown("ï Praktykuj jÍzyk wspÛ≥tworzenia")
        st.markdown("ï Buduj psychologiczne bezpieczeÒstwo")
        
    with col2:
        st.markdown("**?? Konkretne Êwiczenia:**")
        st.markdown("ï **Tygodniowo:** 3 rozmowy 1-on-1 z fokusem na C-IQ III")
        st.markdown("ï **Dziennie:** Zadaj 5+ pytaÒ otwartych zespo≥owi") 
        st.markdown("ï **MiesiÍcznie:** Przeanalizuj swoje rozmowy tym narzÍdziem")
        st.markdown("ï **Kwartalne:** Feedback 360∞ o stylu komunikacji")
    
    # Benchmark z innymi liderami
    st.markdown("### ?? Benchmark z innymi liderami")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**?? Lider Poczπtkujπcy**")
        st.markdown("ï Poziom III: 15-25%")
        st.markdown("ï Fokus na zadania")
        st.markdown("ï Komunikacja dyrektywna")
        
    with col2:
        st.markdown("**?? Lider Doúwiadczony**") 
        st.markdown("ï Poziom III: 40-60%")
        st.markdown("ï Balans zadania-relacje")
        st.markdown("ï RozwÛj zespo≥u")
        
    with col3:
        st.markdown("**?? Lider Transformacyjny**")
        st.markdown("ï Poziom III: 65%+")
        st.markdown("ï Inspiruje i motywuje")
        st.markdown("ï Buduje kultur zaufania")
    
    # Gdzie jesteú
    if level_iii_percentage < 25:
        st.info("?? **Jesteú na poziomie:** Lider Poczπtkujπcy - úwietny moment na rozwÛj!")
    elif level_iii_percentage < 60:
        st.success("?? **Jesteú na poziomie:** Lider Doúwiadczony - bardzo dobry wynik!")
    else:
        st.success("?? **Jesteú na poziomie:** Lider Transformacyjny - gratulacje! ??")

# ===============================================
# DISPLAY FUNCTIONS - WYåWIETLANIE REZULTAT”W  
# ===============================================

def display_sentiment_results(result: Dict):
    """Wyúwietla wyniki analizy sentymentu"""
    st.markdown("## ?? Wyniki Analizy Sentiment + C-IQ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sentiment = result.get('overall_sentiment', 'neutralny')
        score = result.get('sentiment_score', 5)
        
        color = "??" if sentiment == "pozytywny" else "??" if sentiment == "negatywny" else "??"
        st.metric(f"{color} Sentiment ogÛlny", f"{sentiment.title()}", f"Ocena: {score}/10")
        
    with col2:
        ciq = result.get('ciq_analysis', {})
        manager_level = ciq.get('manager_level', 'N/A')
        st.metric("?? Poziom menedøera", manager_level)
        
    with col3:
        business = result.get('business_insights', {})
        escalation = business.get('escalation_risk', 0)
        color = "??" if escalation < 4 else "??" if escalation < 7 else "??"
        st.metric(f"{color} Ryzyko eskalacji", f"{escalation}/10")
    
    # SzczegÛ≥y
    if 'emotions_detected' in result:
        st.markdown("### ?? Wykryte emocje")
        emotions = result['emotions_detected']
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("** Menedøer:**")
            for emotion in emotions.get('manager', []):
                st.markdown(f"ï {emotion}")
                
        with col2:
            st.markdown("**?? Pracownik:**")
            for emotion in emotions.get('employee', []):
                st.markdown(f"ï {emotion}")
    
    # Rekomendacje
    if 'recommendations' in result:
        st.markdown("### ?? Rekomendacje")
        recommendations = result['recommendations']
        
        if 'immediate_actions' in recommendations:
            st.markdown("**?? Natychmiastowe dzia≥ania:**")
            for action in recommendations['immediate_actions']:
                st.markdown(f"ï {action}")
                
        if 'coaching_points' in recommendations:
            st.markdown("**?? WskazÛwki coachingowe:**")
            for point in recommendations['coaching_points']:
                st.markdown(f"ï {point}")

def display_intent_results(result: Dict):
    """Wyúwietla wyniki detekcji intencji"""
    st.markdown("## ?? Wykryte Intencje Biznesowe")
    
    if 'detected_intents' in result:
        for intent_data in result['detected_intents']:
            intent = intent_data.get('intent', 'unknown')
            confidence = intent_data.get('confidence', 0)
            urgency = intent_data.get('urgency', 'medium')
            
            # Kolory dla rÛønych intencji
            intent_colors = {
                'purchase': '??',
                'complaint': '??', 
                'cancellation': '?',
                'upsell_opportunity': '??',
                'feature_request': '??'
            }
            
            color = intent_colors.get(intent, '?')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"{color} Intencja", intent.replace('_', ' ').title())
            with col2:
                st.metric("?? PewnoúÊ", f"{confidence}/10")
            with col3:
                urgency_color = "??" if urgency == "high" else "??" if urgency == "medium" else "??"
                st.metric(f"{urgency_color} PilnoúÊ", urgency.title())
    
    # Rekomendacje biznesowe
    if 'next_best_actions' in result:
        st.markdown("### ?? Rekomendowane dzia≥ania")
        for action in result['next_best_actions']:
            st.markdown(f"ï {action}")

def display_escalation_results(result: Dict):
    """Wyúwietla wyniki analizy problemÛw zespo≥owych"""
    st.markdown("## ?? Analiza ProblemÛw Zespo≥owych")
    
    risk_level = result.get('risk_level', 'medium')
    team_risk = result.get('team_problem_risk', result.get('escalation_risk', 5))
    
    # Kolory dla poziomÛw ryzyka
    risk_colors = {
        'low': '??',
        'medium': '??', 
        'high': '??',
        'critical': '??'
    }
    
    color = risk_colors.get(risk_level, '??')
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"{color} Poziom ryzyka", risk_level.upper(), f"{team_risk}/10")
    
    with col2:
        hr_esc = result.get('hr_escalation', result.get('manager_escalation', {}))
        if hr_esc.get('recommended', False):
            st.error("?? ZALECANE PRZEKAZANIE DO HR/WYØSZEGO MANAGEMENTU")
        else:
            st.success("? Menedøer moøe kontynuowaÊ wsparcie zespo≥u")
    
    # Sygna≥y ostrzegawcze
    if 'warning_signals' in result:
        st.markdown("### ?? Wykryte sygna≥y ostrzegawcze")
        for signal in result['warning_signals']:
            severity = signal.get('severity', 0)
            signal_text = signal.get('signal', '')
            severity_color = "??" if severity > 7 else "??" if severity > 4 else "??"
            st.markdown(f"{severity_color} **{signal_text}** (IntensywnoúÊ: {severity}/10)")
    
    # Strategie wsparcia
    if 'support_strategies' in result:
        st.markdown("### ?? Strategie wsparcia pracownika")
        for strategy in result['support_strategies']:
            st.markdown(f"ï {strategy}")
    
    # Dzia≥ania przywÛdcze
    if 'leadership_actions' in result:
        st.markdown("### ?? Rekomendowane dzia≥ania menedøerskie")
        for action in result['leadership_actions']:
            st.markdown(f"ï {action}")

def display_coaching_results(result: Dict):
    """Wyúwietla wyniki coachingu przywÛdczego"""
    st.markdown("## ?? Leadership Coach - Sugerowane odpowiedzi")
    
    # G≥Ûwne sugestie
    if 'suggested_responses' in result:
        for i, suggestion in enumerate(result['suggested_responses']):
            st.markdown(f"### ?? Sugerowana odpowiedü {i+1}")
            
            response = suggestion.get('response', '')
            rationale = suggestion.get('rationale', '')
            
            st.success(f"**?? Odpowiedü:** {response}")
            st.info(f"**?? Uzasadnienie:** {rationale}")
    
    # Techniki C-IQ
    if 'ciq_techniques' in result:
        st.markdown("### ?? Techniki C-IQ do zastosowania")
        for technique in result['ciq_techniques']:
            st.markdown(f"ï {technique}")
    
    # Czego unikaÊ
    if 'what_to_avoid' in result:
        st.markdown("### ? Czego unikaÊ")
        for avoid in result['what_to_avoid']:
            st.markdown(f"ï {avoid}")
    
    # Pytania otwarte
    if 'follow_up_questions' in result:
        st.markdown("### ? Sugerowane pytania otwarte")
        for question in result['follow_up_questions']:
            st.markdown(f"ï {question}")

if __name__ == "__main__":
    show_tools_page()

