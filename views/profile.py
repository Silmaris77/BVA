import streamlit as st
import pandas as pd
import random
import re
import os
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from data.test_questions import DEGEN_TYPES, TEST_QUESTIONS
from data.users import load_user_data, save_user_data, update_single_user_field, get_current_user_data
from PIL import Image
from utils.components import zen_header, zen_button, notification, tip_block
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, responsive_grid, responsive_container, toggle_device_view, apply_responsive_styles, get_responsive_figure_size

from datetime import datetime, timedelta
import time
from utils.personalization import (
    update_user_avatar,
    update_user_theme,
    get_user_style,
    generate_user_css
)
from utils.goals import (
    add_user_goal,
    update_goal_progress,
    delete_goal,
    get_user_goals,
    calculate_goal_metrics
)
from utils.daily_missions import get_daily_missions_progress
from utils.inventory import (
    activate_item,
    get_user_inventory,
    is_booster_active,
    format_time_remaining
)
from utils.badge_display import BadgeDisplaySystem
from config.settings import USER_AVATARS, THEMES, DEGEN_TYPES, BADGES, BADGE_CATEGORIES
from data.degen_details import degen_details
from utils.xp_system import calculate_xp_progress
from utils.components import zen_header, zen_button, notification, stat_card, xp_level_display, goal_card, badge_card, progress_bar, tip_block, quote_block,  add_animations_css
from utils.user_components import user_stats_panel
from utils.real_time_updates import live_xp_indicator
from utils.achievements import check_achievements
from datetime import datetime, timedelta

def buy_item(item_type, item_id, price, user_data, users_data, username):
    """
    Process the purchase of an item
    
    Parameters:
    - item_type: Type of the item (avatar, background, special_lesson, booster)
    - item_id: Unique identifier of the item
    - price: Cost in DegenCoins
    - user_data: User's data dictionary
    - users_data: All users' data dictionary
    - username: Username of the current user
    
    Returns:
    - (success, message): Tuple with success status and message
    """
    # Sprawdź czy użytkownik ma wystarczającą ilość monet
    if user_data.get('degencoins', 0) < price:
        return False, "Nie masz wystarczającej liczby DegenCoins!"
    
    # Odejmij monety
    user_data['degencoins'] = user_data.get('degencoins', 0) - price
      # Dodaj przedmiot do ekwipunku użytkownika
    if 'inventory' not in user_data:
        user_data['inventory'] = {}
    
    # Map plural to singular for consistency with inventory system
    item_type_mapping = {
        'avatars': 'avatar',
        'backgrounds': 'background', 
        'special_lessons': 'special_lesson',
        'boosters': 'booster'
    }
    
    inventory_key = item_type_mapping.get(item_type, item_type)
    
    if inventory_key not in user_data['inventory']:
        user_data['inventory'][inventory_key] = []
    
    # Dodaj przedmiot do odpowiedniej kategorii (unikaj duplikatów)
    if item_id not in user_data['inventory'][inventory_key]:
        user_data['inventory'][inventory_key].append(item_id)
    
    # Dodaj specjalną obsługę dla boosterów (dodając datę wygaśnięcia)
    if item_type == 'booster':
        if 'active_boosters' not in user_data:
            user_data['active_boosters'] = {}
        
        # Ustawienie czasu wygaśnięcia na 24 godziny od teraz
        expiry_time = datetime.now() + timedelta(hours=24)
        user_data['active_boosters'][item_id] = {
            'expires_at': expiry_time.isoformat(),
            'purchased_at': datetime.now().isoformat()
        }
    
    # Zapisz zaktualizowane dane
    users_data[username] = user_data
    save_user_data(users_data)
    
    return True, f"Pomyślnie zakupiono {item_id.replace('_', ' ').title()}!"

def show_profile_stats_section(user_data, device_type):
    """Sekcja z kartami statystyk użytkownika - na wzór Dashboard"""
    st.markdown("### 📊 Twoje statystyki")
    
    # Oblicz dane statystyk
    xp = user_data.get('xp', 0)
    degencoins = user_data.get('degencoins', 0)
    completed_lessons = len(user_data.get('completed_lessons', []))
    missions_progress = get_daily_missions_progress(st.session_state.username)
    streak = missions_progress['streak']
    level = user_data.get('level', 1)
    
    # Oblicz trend (przykładowe wartości)
    xp_change = "+15%"
    degencoins_change = "+10%"
    lessons_change = f"+{min(3, completed_lessons)}"
    streak_change = f"+{min(1, streak)}"
    level_change = f"+{max(0, level - 1)}"
    
    # Responsywny układ kolumn
    if device_type == 'mobile':
        # Na mobile: 2 kolumny, 3 wiersze
        cols1 = st.columns(2)
        cols2 = st.columns(2) 
        cols3 = st.columns(1)  # Ostatnia statystyka na środku
        all_cols = list(cols1) + list(cols2) + list(cols3)
    else:
        # Na desktop: 5 kolumn w jednym wierszu
        all_cols = st.columns(5)
    
    # 5 kart statystyk
    stats = [
        {"icon": "🏆", "value": f"{xp}", "label": "Punkty XP", "change": xp_change},
        {"icon": "🪙", "value": f"{degencoins}", "label": "DegenCoins", "change": degencoins_change},
        {"icon": "⭐", "value": f"{level}", "label": "Poziom", "change": level_change},
        {"icon": "📚", "value": f"{completed_lessons}", "label": "Ukończone lekcje", "change": lessons_change},
        {"icon": "🔥", "value": f"{streak}", "label": "Aktualna passa", "change": streak_change}
    ]
    
    # Wygeneruj kartę w każdej kolumnie
    for i, stat in enumerate(stats):
        with all_cols[i]:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{stat['icon']}</div>
                <div class="stat-value">{stat['value']}</div>
                <div class="stat-label">{stat['label']}</div>
                <div class="stat-change positive">{stat['change']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Dodatkowe informacje w expanderze
    with st.expander("📈 Szczegółowe statystyki"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🎯 Średnia punktów za lekcję", 
                     f"{int(xp/max(1, completed_lessons))}", 
                     help="Średnia liczba punktów XP za ukończoną lekcję")
            
            total_quiz_score = user_data.get('total_quiz_score', 0)
            quizzes_completed = user_data.get('quizzes_completed', 0)
            avg_quiz_score = (total_quiz_score / quizzes_completed) if quizzes_completed > 0 else 0
            st.metric("📝 Średni wynik quiz", f"{avg_quiz_score:.1f}%")
        
        with col2:
            max_streak = user_data.get('max_streak', 0)
            st.metric("🔥 Najdłuższa passa", f"{max_streak} dni")
            
            badges_count = len(user_data.get('badges', []))
            st.metric("🏆 Zdobyte odznaki", badges_count)

def show_profile():
    # Zastosuj style Material 3 (tak jak w dashboard)
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Używamy naszego komponentu nagłówka - tak jak w dashboard
    zen_header("Profil")
      # Add live XP indicator - ZAKOMENTOWANE
    # live_xp_indicator()
      # Use current user data to ensure degen test results are included
    user_data = get_current_user_data(st.session_state.username)
    users_data = load_user_data()  # For shop transactions
    style = get_user_style(st.session_state.username)
    
    # Wyświetl personalizowane style
    st.markdown(generate_user_css(st.session_state.username), unsafe_allow_html=True)
    
    # Add animations and effects using the component
    add_animations_css()

    # Main Profile Tabs - usunięto Personalizację i Eksplorator Typów
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Statystyki", "🎒 Ekwipunek", "🏆 Odznaki", "🧬 Typ Degena"])
    
    # Tab 1: Statistics - podobnie jak w Dashboard
    with tab1:
        show_profile_stats_section(user_data, device_type)
    
    # Tab 2: Inventory/Equipment
    with tab2:
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        
        # Load user inventory
        inventory = get_user_inventory(st.session_state.username)
          # Create subtabs for different inventory categories
        inv_tabs = st.tabs(["Awatary", "Tła", "Specjalne Lekcje", "Boostery", "🛒 Sklep"])
        
        # Tab for Avatars
        with inv_tabs[0]:
            st.subheader("Twoje Awatary")
            
            if inventory['avatars']:
                # Create a grid of avatars
                avatar_cols = st.columns(4)
                
                for i, avatar_id in enumerate(inventory['avatars']):
                    if avatar_id in USER_AVATARS:
                        with avatar_cols[i % 4]:
                            st.markdown(f"""
                            <div style="text-align: center; padding: 10px;">
                                <div style="font-size: 3rem; margin-bottom: 5px;">{USER_AVATARS[avatar_id]}</div>
                                <div style="font-size: 0.9rem;">{avatar_id.replace('_', ' ').title()}</div>
                            </div>
                            """, unsafe_allow_html=True)
                              # Add a button to activate this avatar
                            if st.button(f"Aktywuj {avatar_id.title()}", key=f"activate_avatar_{avatar_id}"):
                                success, message = activate_item(st.session_state.username, 'avatar', avatar_id)
                                if success:
                                    notification(message, type="success")
                                    st.rerun()
                                else:
                                    notification(message, type="error")
            else:
                st.info("Nie posiadasz żadnych awatarów. Sprawdź zakładkę Sklep!")
        
        # Tab for Backgrounds
        with inv_tabs[1]:
            st.subheader("Twoje Tła")
            
            if inventory['backgrounds']:
                # Create a grid of backgrounds
                bg_cols = st.columns(2)
                
                for i, bg_id in enumerate(inventory['backgrounds']):
                    with bg_cols[i % 2]:
                        st.markdown(f"""
                        <div style="text-align: center; padding: 10px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 10px;">
                            <div style="font-size: 2rem; margin-bottom: 5px;">🖼️</div>
                            <div style="font-size: 1rem; font-weight: bold;">{bg_id.replace('_', ' ').title()}</div>
                        </div>
                        """, unsafe_allow_html=True)
                          # Add a button to activate this background
                        if st.button(f"Aktywuj {bg_id.title()}", key=f"activate_bg_{bg_id}"):
                            success, message = activate_item(st.session_state.username, 'background', bg_id)
                            if success:
                                notification(message, type="success")
                                st.rerun()
                            else:
                                notification(message, type="error")
            else:
                st.info("Nie posiadasz żadnych teł. Sprawdź zakładkę Sklep!")
        
        # Tab for Special Lessons
        with inv_tabs[2]:
            st.subheader("Twoje Specjalne Lekcje")
            
            if inventory['special_lessons']:
                # Display special lessons
                for lesson_id in inventory['special_lessons']:
                    with st.container():
                        st.markdown(f"""
                        <div style="padding: 15px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 15px;">
                            <div style="display: flex; align-items: center;">
                                <div style="font-size: 2rem; margin-right: 15px;">📚</div>
                                <div>
                                    <div style="font-size: 1.2rem; font-weight: bold;">{lesson_id.replace('_', ' ').title()}</div>
                                    <div style="font-size: 0.9rem; color: #666;">Specjalna lekcja dostępna do odblokowania</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                          # Add a button to unlock this special lesson
                        if st.button(f"Odblokuj lekcję", key=f"unlock_lesson_{lesson_id}"):
                            success, message = activate_item(st.session_state.username, 'special_lesson', lesson_id)
                            if success:
                                notification(message, type="success")
                                st.rerun()
                            else:
                                notification(message, type="error")
            else:
                st.info("Nie posiadasz żadnych specjalnych lekcji. Sprawdź zakładkę Sklep!")
        
        # Tab for Boosters
        with inv_tabs[3]:
            st.subheader("Twoje Boostery")
            
            if inventory['boosters']:
                # Display active boosters
                for booster_id, booster_data in inventory['boosters'].items():
                    is_active, expiration = is_booster_active(st.session_state.username, booster_id)
                    status = "Aktywny" if is_active else "Nieaktywny"
                    status_color = "#4CAF50" if is_active else "#F44336"
                    
                    # Format time remaining
                    time_remaining = format_time_remaining(expiration) if is_active else "Wygasł"
                    
                    st.markdown(f"""
                    <div style="padding: 15px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 15px;">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <div style="display: flex; align-items: center;">
                                <div style="font-size: 2rem; margin-right: 15px;">⚡</div>
                                <div>
                                    <div style="font-size: 1.2rem; font-weight: bold;">{booster_id.replace('_', ' ').title()}</div>
                                    <div style="font-size: 0.9rem; color: #666;">{time_remaining}</div>
                                </div>
                            </div>
                            <div style="font-size: 0.9rem; font-weight: bold; color: {status_color};">{status}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                      # Add button to reactivate if not active
                    if not is_active:
                        if st.button(f"Reaktywuj {booster_id.replace('_', ' ').title()}", key=f"reactivate_booster_{booster_id}"):
                            success, message = activate_item(st.session_state.username, 'booster', booster_id)
                            if success:
                                notification(message, type="success")
                                st.rerun()
                            else:
                                notification(message, type="error")
            else:
                st.info("Nie posiadasz żadnych boosterów. Kup je w poniższej zakładce Sklep!")
        
        # Tab 5: Shop
        with inv_tabs[4]:
            st.subheader("🛒 Sklep")            # Display user's DegenCoins
            st.markdown(f"### Twoje DegenCoins: <span style='color: #FFA500;'>🪙 {user_data.get('degencoins', 0)}</span>", unsafe_allow_html=True)
            
            # Shop tabs
            shop_tabs = st.tabs(["Awatary", "Tła", "Specjalne Lekcje", "Boostery"])
            
            # Avatars Shop
            with shop_tabs[0]:
                st.markdown("#### Awatary Premium 🔗")
                
                # Lista dostępnych awatarów
                avatars = {
                    "diamond_degen": {
                        "name": "💎 Diamond Degen",
                        "price": 500,
                        "description": "Pokazuje twoje zaangażowanie w rozwój jako inwestor."
                    },
                    "crypto_wizard": {
                        "name": "🧙 Crypto Wizard",
                        "price": 750,
                        "description": "Awatar dla tych, którzy mistrzowsko opanowali sztukę inwestowania."
                    },                    "moon_hunter": {
                        "name": "🌕 Moon Hunter",
                        "price": 1000,
                        "description": "Dla tych, którzy zawsze celują wysoko."
                    }
                }
                
                # Wyświetl dostępne awatary w trzech kolumnach
                cols = st.columns(3)
                
                for i, (avatar_id, avatar) in enumerate(avatars.items()):
                    with cols[i % 3]:
                        st.markdown(f"**{avatar['name']}**")
                        st.markdown(f"Cena: 🪙 {avatar['price']}")
                        st.markdown(f"*{avatar['description']}*")
                          # Sprawdź czy użytkownik posiada już ten awatar
                        user_has_item = 'inventory' in user_data and 'avatar' in user_data.get('inventory', {}) and avatar_id in user_data['inventory']['avatar']
                        
                        if user_has_item:
                            st.success("✅ Posiadasz")
                        else:
                            # Przycisk do zakupu
                            if st.button(f"Kup {avatar['name']}", key=f"buy_avatar_{avatar_id}"):
                                success, message = buy_item('avatars', avatar_id, avatar['price'], user_data, users_data, st.session_state.username)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
            
            # Backgrounds Shop
            with shop_tabs[1]:
                st.markdown("#### Tła Premium 🖼️")
                
                # Lista dostępnych teł
                backgrounds = {
                    "crypto_city": {
                        "name": "🏙️ Crypto City",
                        "price": 300,
                        "description": "Nowoczesne miasto przyszłości."
                    },
                    "zen_garden": {
                        "name": "🌿 Zen Garden",
                        "price": 400,
                        "description": "Spokojny ogród dla zrównoważonych inwestorów."
                    },
                    "space_station": {
                        "name": "🚀 Space Station",
                        "price": 600,
                        "description": "Dla inwestorów, którzy sięgają gwiazd."
                    }
                }
                
                # Wyświetl dostępne tła w trzech kolumnach
                cols = st.columns(3)
                
                for i, (bg_id, bg) in enumerate(backgrounds.items()):
                    with cols[i % 3]:
                        st.markdown(f"**{bg['name']}**")
                        st.markdown(f"Cena: 🪙 {bg['price']}")
                        st.markdown(f"*{bg['description']}*")
                          # Sprawdź czy użytkownik posiada już to tło
                        user_has_item = 'inventory' in user_data and 'background' in user_data.get('inventory', {}) and bg_id in user_data['inventory']['background']
                        
                        if user_has_item:
                            st.success("✅ Posiadasz")
                        else:
                            # Przycisk do zakupu
                            if st.button(f"Kup {bg['name']}", key=f"buy_bg_{bg_id}"):
                                success, message = buy_item('backgrounds', bg_id, bg['price'], user_data, users_data, st.session_state.username)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
            
            # Special Lessons Shop
            with shop_tabs[2]:
                st.markdown("#### Specjalne Lekcje 📚")
                
                # Lista dostępnych specjalnych lekcji
                special_lessons = {
                    "market_psychology": {
                        "name": "📊 Psychologia Rynku Zaawansowana",
                        "price": 800,
                        "description": "Zaawansowane techniki psychologii rynku."
                    },
                    "risk_management": {
                        "name": "🛡️ Zarządzanie Ryzykiem Pro",
                        "price": 700,
                        "description": "Profesjonalne techniki zarządzania ryzykiem."
                    },
                    "trading_mastery": {
                        "name": "🧠 Mistrzostwo Tradingowe",
                        "price": 1200,
                        "description": "Odkryj sekrety mistrzów tradingu."
                    }
                }
                
                # Wyświetl dostępne lekcje w trzech kolumnach
                cols = st.columns(3)
                
                for i, (lesson_id, lesson) in enumerate(special_lessons.items()):
                    with cols[i % 3]:
                        st.markdown(f"**{lesson['name']}**")
                        st.markdown(f"Cena: 🪙 {lesson['price']}")
                        st.markdown(f"*{lesson['description']}*")
                          # Sprawdź czy użytkownik posiada już tę lekcję
                        user_has_item = 'inventory' in user_data and 'special_lesson' in user_data.get('inventory', {}) and lesson_id in user_data['inventory']['special_lesson']
                        
                        if user_has_item:
                            st.success("✅ Posiadasz")
                            if st.button(f"Rozpocznij lekcję", key=f"start_{lesson_id}"):
                                st.session_state.page = 'lesson'
                                st.session_state.lesson_id = f"special_{lesson_id}"
                                st.rerun()
                        else:
                            # Przycisk do zakupu
                            if st.button(f"Kup {lesson['name']}", key=f"buy_lesson_{lesson_id}"):
                                success, message = buy_item('special_lessons', lesson_id, lesson['price'], user_data, users_data, st.session_state.username)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
            
            # Boosters Shop
            with shop_tabs[3]:
                st.markdown("#### Boostery ⚡")
                
                # Lista dostępnych boosterów
                boosters = {
                    "xp_boost": {
                        "name": "⚡ XP Boost",
                        "price": 200,
                        "description": "Zwiększa ilość zdobywanego XP o 50% przez 24 godziny."
                    },
                    "coin_boost": {
                        "name": "🪙 Coin Boost",
                        "price": 300,
                        "description": "Zwiększa ilość zdobywanych monet o 50% przez 24 godziny."
                    },
                    "focus_boost": {
                        "name": "🎯 Focus Boost",
                        "price": 250,
                        "description": "Zwiększa szybkość ukończenia lekcji o 30% przez 24 godziny."
                    }
                }
                
                # Wyświetl dostępne boostery w trzech kolumnach
                cols = st.columns(3)
                
                for i, (booster_id, booster) in enumerate(boosters.items()):
                    with cols[i % 3]:
                        st.markdown(f"**{booster['name']}**")
                        st.markdown(f"Cena: 🪙 {booster['price']}")
                        st.markdown(f"*{booster['description']}*")
                        
                        # Sprawdź czy booster jest aktywny
                        is_active = False
                        remaining_time = None
                        
                        if 'active_boosters' in user_data and booster_id in user_data.get('active_boosters', {}):
                            booster_data = user_data['active_boosters'][booster_id]
                            
                            # Handle both old format (string) and new format (object with expires_at)
                            if isinstance(booster_data, str):
                                expiry_time = datetime.fromisoformat(booster_data)
                            elif isinstance(booster_data, dict) and 'expires_at' in booster_data:
                                expiry_time = datetime.fromisoformat(booster_data['expires_at'])
                            else:
                                continue  # Skip invalid booster data
                            
                            now = datetime.now()
                            
                            if expiry_time > now:
                                is_active = True
                                remaining_seconds = (expiry_time - now).total_seconds()
                                remaining_hours = int(remaining_seconds // 3600)
                                remaining_minutes = int((remaining_seconds % 3600) // 60)
                                remaining_time = f"{remaining_hours}h {remaining_minutes}m"
                        
                        if is_active:
                            st.success(f"Aktywny! Pozostały czas: {remaining_time}")
                        else:
                            # Przycisk do zakupu
                            if st.button(f"Kup {booster['name']}", key=f"buy_booster_{booster_id}"):
                                success, message = buy_item('boosters', booster_id, booster['price'], user_data, users_data, st.session_state.username)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
        
        st.markdown("</div>", unsafe_allow_html=True)
    # Tab 3: Badges
    with tab3:
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        # Use Step 5 badge display system
        show_badges_section()
        st.markdown("</div>", unsafe_allow_html=True)
      # Tab 4: Degen Type with Test
    with tab4:
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        
        # Sub-tabs within Typ Degena
        degen_subtab1, degen_subtab2 = st.tabs(["🧠 Test Degena", "� Mój Typ"])
        
        with degen_subtab1:
            # Show Degen Test (imported functionality from degen_explorer)
            show_degen_test_section()
        
        with degen_subtab2:
            # Show current degen type info
            show_current_degen_type()
            
        st.markdown("</div>", unsafe_allow_html=True)

def show_badges_section():
    """Wyświetl sekcję odznak w profilu - Step 5 Implementation"""
    st.header("🏆 Twoje Odznaki - FIXED VERSION")
    
    # Pobierz dane użytkownika
    users_data = load_user_data()
    user_data = users_data.get(st.session_state.username, {})
    user_badges = set(user_data.get('badges', []))
    
    # CSS dla odznak
    st.markdown("""
    <style>
    .badge-unlocked {
        background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
        border: 2px solid #27ae60;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.2);
        transition: transform 0.2s ease;
    }
    .badge-unlocked:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(39, 174, 96, 0.3);
    }
    .badge-locked {
        background: #f5f5f5;
        border: 2px solid #bdc3c7;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
        opacity: 0.6;
        box-shadow: 0 2px 8px rgba(189, 195, 199, 0.2);
    }
    .badge-icon {
        font-size: 2.5em;
        margin-bottom: 8px;
        display: block;
    }
    .badge-name {
        font-weight: bold;
        margin: 8px 0 4px 0;
        color: #2c3e50;
    }
    .badge-description {
        font-size: 0.85em;
        color: #7f8c8d;
        line-height: 1.3;
    }
    .badge-status {
        font-size: 1.2em;
        margin-right: 5px;
    }
    .category-stats {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 4px solid #3498db;
    }
    .category-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 8px;
    }
    .category-description {
        color: #7f8c8d;
        font-size: 0.9em;
        margin-bottom: 10px;
    }
    .category-progress {
        font-size: 0.85em;
        color: #3498db;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
      # Pokaż pomocne wskazówki dla użytkowników bez odznak
    if not user_badges:
        st.info("🌟 Jeszcze nie masz żadnych odznak. Przeglądaj poniższe kategorie, aby zobaczyć jakie odznaki możesz zdobyć!")
        with st.expander("🎯 Jak zdobyć pierwsze odznaki:", expanded=False):
            st.markdown("""
            - **👋 Witaj w Akademii** - Automatycznie po rejestracji
            - **🎯 Pierwszy Uczeń** - Ukończ pierwszą lekcję
            - **🔍 Odkrywca Osobowości** - Wykonaj test typu degena
            - **📝 Profil Kompletny** - Uzupełnij informacje w profilu
            """)
        st.markdown("---")
      # Wyświetl ogólne statystyki
    total_badges = len(BADGES)
    earned_badges = len(user_badges)
    completion_percent = (earned_badges / total_badges) * 100 if total_badges > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Zdobyte odznaki", f"{earned_badges}/{total_badges}", f"{completion_percent:.1f}%")
    with col2:
        if user_badges:
            latest_badge = max(user_badges, key=lambda x: user_data.get('badge_earned_dates', {}).get(x, ''), default=None)
            if latest_badge and latest_badge in BADGES:
                st.metric("Ostatnia odznaka", BADGES[latest_badge]['name'][:20])
            else:
                st.metric("Ostatnia odznaka", "Brak")
        else:
            st.metric("Ostatnia odznaka", "Brak")
    with col3:
        xp_from_badges = sum(BADGES[badge_id].get('xp_reward', 0) for badge_id in user_badges if badge_id in BADGES)
        st.metric("XP z odznak", xp_from_badges)
    
    st.markdown("---")
    
    # Zakładki dla kategorii
    category_names = [info['name'] for info in sorted(BADGE_CATEGORIES.values(), key=lambda x: x['order'])]
    tabs = st.tabs(category_names)
    
    for i, (category_id, category_info) in enumerate(sorted(BADGE_CATEGORIES.items(), key=lambda x: x[1]['order'])):
        with tabs[i]:
            # Nagłówek kategorii
            st.markdown(f"""
            <div class="category-stats">
                <div class="category-title">{category_info['icon']} {category_info['name']}</div>
                <div class="category-description">{category_info['description']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Odznaki w kategorii
            category_badges = [b_id for b_id, b_info in BADGES.items() 
                             if b_info.get('category') == category_id]
            
            if not category_badges:
                st.info(f"Brak odznak w kategorii {category_info['name']}")
                continue
            
            # Statystyki kategorii
            earned_in_category = len([b for b in category_badges if b in user_badges])
            total_in_category = len(category_badges)
            category_completion = (earned_in_category / total_in_category) * 100
            
            st.markdown(f"""
            <div class="category-progress">
                📊 Postęp w kategorii: {earned_in_category}/{total_in_category} ({category_completion:.1f}%)
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Wyświetl odznaki w dwóch kolumnach
            cols = st.columns(2)
            
            # Sortuj odznaki: zdobyte najpierw, potem pozostałe
            earned_badges_in_category = [b for b in category_badges if b in user_badges]
            locked_badges_in_category = [b for b in category_badges if b not in user_badges]
            sorted_badges = earned_badges_in_category + locked_badges_in_category
            
            for j, badge_id in enumerate(sorted_badges):
                if badge_id not in BADGES:
                    continue
                    
                badge_info = BADGES[badge_id]
                is_unlocked = badge_id in user_badges
                
                with cols[j % 2]:
                    css_class = "badge-unlocked" if is_unlocked else "badge-locked"
                    status = "✅" if is_unlocked else "🔒"
                    
                    # Dodaj informacje o tierze i XP
                    tier_name = badge_info.get('tier', 'bronze')
                    xp_reward = badge_info.get('xp_reward', 0)
                    
                    tier_colors = {
                        'bronze': '#CD7F32',
                        'silver': '#C0C0C0', 
                        'gold': '#FFD700',
                        'platinum': '#E5E4E2',
                        'diamond': '#B9F2FF'
                    }
                    tier_color = tier_colors.get(tier_name, '#CD7F32')
                    
                    st.markdown(f"""
                    <div class="{css_class}">
                        <div class="badge-icon">{badge_info.get('icon', '🏆')}</div>
                        <div class="badge-name">
                            <span class="badge-status">{status}</span>
                            {badge_info['name']}
                        </div>
                        <div class="badge-description">{badge_info['description']}</div>
                        <div style="margin-top: 8px; font-size: 0.75em;">
                            <span style="color: {tier_color}; font-weight: bold;">
                                {tier_name.upper()}
                            </span>
                            {' • ' + str(xp_reward) + ' XP' if xp_reward > 0 else ''}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# Helper functions imported from degen_explorer
def clean_html(text):
    """Usuwa wszystkie tagi HTML z tekstu i normalizuje białe znaki"""
    text_without_tags = re.sub(r'<.*?>', '', text)
    normalized_text = re.sub(r'\s+', ' ', text_without_tags)
    return normalized_text.strip()

def calculate_test_results(scores):
    """Calculate the dominant degen type based on test scores"""
    return max(scores.items(), key=lambda x: x[1])[0]

def show_degen_test_section():
    """Wyświetla sekcję testu degena w profilu"""
    device_type = get_device_type()
    
    # Informacja o teście
    if 'show_test_info' not in st.session_state:
        st.session_state.show_test_info = True
    
    if st.session_state.show_test_info:
        st.markdown("""
        ### 🧠 Test typu degena
        
        Ten test pomoże Ci sprawdzić, **jakim typem inwestora (degena)** jesteś.
        
        - Każde pytanie ma **8 odpowiedzi** – każda reprezentuje inny styl inwestycyjny.
        - **Wybierz tę odpowiedź, która najlepiej opisuje Twoje zachowanie lub sposób myślenia.**
        - Po zakończeniu zobaczysz graficzny wynik w postaci wykresu radarowego.
        
        🧩 Gotowy?
        """)
        if zen_button("Rozpocznij test", key="start_degen_test"):
            st.session_state.show_test_info = False
            if 'test_step' not in st.session_state:
                st.session_state.test_step = 0
                st.session_state.test_scores = {degen_type: 0 for degen_type in DEGEN_TYPES}
            st.rerun()
    
    # Tryb testu    
    elif 'test_step' not in st.session_state:
        st.session_state.test_step = 0
        st.session_state.test_scores = {degen_type: 0 for degen_type in DEGEN_TYPES}
        st.rerun()
    
    elif st.session_state.test_step < len(TEST_QUESTIONS):
        # Display current question
        question = TEST_QUESTIONS[st.session_state.test_step]
        
        st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
        st.subheader(f"Pytanie {st.session_state.test_step + 1} z {len(TEST_QUESTIONS)}")
        st.markdown(f"### {question['question']}")
        
        # Render options
        options = question['options']
        
        # Użyj responsywnego układu w zależności od typu urządzenia
        if device_type == 'mobile':
            # Na telefonach wyświetl opcje jedna pod drugą
            for i in range(len(options)):
                if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", use_container_width=True):
                    # Add scores for the answer
                    for degen_type, score in options[i]['scores'].items():
                        st.session_state.test_scores[degen_type] += score
                    
                    st.session_state.test_step += 1
                    st.rerun()
        else:
            # Na tabletach i desktopach użyj dwóch kolumn
            col1, col2 = st.columns(2)
            for i in range(len(options)):
                if i < len(options) // 2:
                    with col1:
                        if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", use_container_width=True):
                            # Add scores for the answer
                            for degen_type, score in options[i]['scores'].items():
                                st.session_state.test_scores[degen_type] += score
                            
                            st.session_state.test_step += 1
                            st.rerun()
                else:
                    with col2:
                        if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", use_container_width=True):
                            # Add scores for the answer
                            for degen_type, score in options[i]['scores'].items():
                                st.session_state.test_scores[degen_type] += score
                            
                            st.session_state.test_step += 1
                            st.rerun()
        
        # Progress bar
        progress_value = st.session_state.test_step / len(TEST_QUESTIONS)
        progress_bar(progress=progress_value, color="#4CAF50")
        st.markdown(f"**Postęp testu: {int(progress_value * 100)}%**")
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        # Show test results
        show_test_results()

def show_test_results():
    """Wyświetla wyniki testu degena"""
    device_type = get_device_type()
    
    # Calculate result
    result = calculate_test_results(st.session_state.test_scores)
    
    st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
    st.success("🎉 Test zakończony!")
    st.markdown(f"## Twój typ degena: **{result}**")
    
    if result in DEGEN_TYPES:
        tagline = DEGEN_TYPES[result].get('tagline', 'Unikalny styl inwestowania')
        description = DEGEN_TYPES[result].get('description', 'Opis niedostępny')
        
        st.markdown(f"*{tagline}*")
        st.markdown(description)
        
        # Show radar chart
        st.subheader("Twój profil inwestycyjny")
        radar_fig = plot_radar_chart(st.session_state.test_scores, device_type=device_type)
        st.pyplot(radar_fig)
        
        # Save results
        if zen_button("Zapisz wyniki", key="save_test_results"):
            users_data = load_user_data()
            if st.session_state.username not in users_data:
                users_data[st.session_state.username] = {}
            
            users_data[st.session_state.username]['degen_type'] = result
            users_data[st.session_state.username]['test_scores'] = st.session_state.test_scores
            users_data[st.session_state.username]['test_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            save_user_data(users_data)
            
            # Add recent activity for degen type discovery
            from data.users_fixed import add_recent_activity
            add_recent_activity(
                st.session_state.username, 
                "degen_type_discovered", 
                {"degen_type": result}
            )
            
            # Check for achievements
            check_achievements(st.session_state.username)
            
            notification("Wyniki testu zostały zapisane!", type="success")
            
            # Reset test state
            for key in ['test_step', 'test_scores', 'show_test_info']:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Option to restart test
    if zen_button("Wykonaj test ponownie", key="restart_test"):
        for key in ['test_step', 'test_scores', 'show_test_info']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def show_current_degen_type():
    """Wyświetla informacje o aktualnym typie degena użytkownika"""
    device_type = get_device_type()
    user_data = get_current_user_data()
    
    st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
    
    if user_data.get('degen_type'):
        degen_type = user_data['degen_type']
          # Header with degen type
        st.markdown(f"<h2 style='text-align: center;'>{degen_type}</h2>", unsafe_allow_html=True)
        tagline = DEGEN_TYPES.get(degen_type, {}).get("tagline", "Twój unikalny styl inwestowania")
        st.markdown(f"<div style='text-align: center; color: #666; margin-bottom: 20px;'>{tagline}</div>", unsafe_allow_html=True)
        
        if degen_type in DEGEN_TYPES:
            # Description
            with st.expander("📖 Opis", expanded=True):
                description = DEGEN_TYPES[degen_type].get("description", "Opis niedostępny")
                st.markdown(description)
                
            # Radar chart if available
            if 'test_scores' in user_data:
                st.subheader("Twój profil inwestycyjny")
                
                radar_fig = plot_radar_chart(user_data['test_scores'], device_type=device_type)
                
                # Add mobile-specific styles for the chart container
                if device_type == 'mobile':
                    st.markdown("""
                    <style>
                    .radar-chart-container {
                        margin: 0 -20px;
                        padding-bottom: 15px;
                    }
                    </style>
                    <div class="radar-chart-container">
                    """, unsafe_allow_html=True)
                    
                st.pyplot(radar_fig)
                
                if device_type == 'mobile':
                    st.markdown("</div>", unsafe_allow_html=True)
              # Strengths and challenges in two columns
            col1, col2 = st.columns(2)
            
            with col1:
                with st.expander("💪 Mocne strony", expanded=True):
                    strengths = DEGEN_TYPES[degen_type].get("strengths", ["Brak danych"])
                    st.markdown("\n".join([f"- ✅ {strength}" for strength in strengths]))
            
            with col2:
                with st.expander("🔍 Wyzwania", expanded=True):
                    challenges = DEGEN_TYPES[degen_type].get("challenges", ["Brak danych"])
                    st.markdown("\n".join([f"- ⚠️ {challenge}" for challenge in challenges]))
            
            # Strategy
            strategy = DEGEN_TYPES[degen_type].get("strategy", "Strategia niedostępna")
            tip_block(
                strategy,
                title="Rekomendowana strategia",
                icon="🎯"
            )
            
            # Detailed description
            if degen_type in degen_details:
                with st.expander("📚 Szczegółowy opis twojego typu degena", expanded=False):
                    st.markdown(degen_details[degen_type])
            else:
                st.warning("Szczegółowy opis dla tego typu degena nie jest jeszcze dostępny.")
                
            # Test info and retake option
            if 'test_date' in user_data:
                st.info(f"📅 Test wykonany: {user_data['test_date']}")
            
            if zen_button("Wykonaj test ponownie", key="retake_test"):
                # Reset test state
                for key in ['test_step', 'test_scores', 'show_test_info']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.show_test_info = True
                st.rerun()
    else:
        notification(
            "Nie określono jeszcze twojego typu degena. Wykonaj test degena w zakładce powyżej, aby odkryć swój unikalny styl inwestowania i dostosowane rekomendacje.",
            type="info"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

def plot_radar_chart(scores, device_type=None):
    """Generate a radar chart for test results
    
    Args:
        scores: Dictionary of degen types and their scores
        device_type: Device type ('mobile', 'tablet', or 'desktop')
    """
    # Jeśli device_type nie został przekazany, pobierz go
    if device_type is None:
        device_type = get_device_type()
        
    # Upewnij się, że labels i values są listami o tym samym rozmiarze
    labels = list(scores.keys())
    values = [float(v) for v in scores.values()]
    
    # Utwórz kąty i od razu skonwertuj na stopnie
    num_vars = len(labels)
    angles_degrees = np.linspace(0, 360, num_vars, endpoint=False)
    angles_radians = np.radians(angles_degrees)
    
    # Tworzenie zamkniętych list bez używania wycinków [:-1]
    values_closed = np.concatenate((values, [values[0]]))
    angles_radians_closed = np.concatenate((angles_radians, [angles_radians[0]]))
    
    # Użyj funkcji helper do ustalenia rozmiaru wykresu
    fig_size = get_responsive_figure_size(device_type)
    
    # Dostosuj pozostałe parametry w zależności od urządzenia
    if device_type == 'mobile':
        title_size = 14
        font_size = 6.5
        grid_alpha = 0.3
        line_width = 1.5
        marker_size = 4
    elif device_type == 'tablet':
        title_size = 16
        font_size = 8
        grid_alpha = 0.4
        line_width = 2
        marker_size = 5
    else:  # desktop
        title_size = 18
        font_size = 9
        grid_alpha = 0.5
        line_width = 2.5
        marker_size = 6
    
    # Tworzenie i konfiguracja wykresu
    fig, ax = plt.subplots(figsize=fig_size, subplot_kw=dict(polar=True))
    
    # Dodaj przezroczyste tło za etykietami dla lepszej czytelności
    ax.set_facecolor('white')
    if device_type == 'mobile':
        # Na telefonach zwiększ kontrast
        ax.set_facecolor('#f8f8f8')
    
    # Plot the radar chart with marker size adjusted for device
    ax.plot(angles_radians_closed, values_closed, 'o-', linewidth=line_width, markersize=marker_size)
    ax.fill(angles_radians_closed, values_closed, alpha=0.25)
    
    # Ensure we have a valid limit
    max_val = max(values) if max(values) > 0 else 1
    y_max = max_val * 1.2  # Add some padding at the top
    ax.set_ylim(0, y_max)
    
    # Adjust label positions and appearance for better device compatibility
    # For mobile, rotate labels to fit better on small screens
    if device_type == 'mobile':
        # Use shorter labels on mobile
        ax.set_thetagrids(angles_degrees, labels, fontsize=font_size-1)
        plt.setp(ax.get_xticklabels(), rotation=67.5)  # Rotate labels for better fit
    else:
        ax.set_thetagrids(angles_degrees, labels, fontsize=font_size)
    
    # Set title with responsive size
    ax.set_title("Twój profil inwestycyjny", size=title_size, pad=20)
    
    # Dostosuj siatkę i oś
    ax.grid(True, alpha=grid_alpha)
    
    # Dodaj etykiety z wartościami
    # Dostosuj odległość etykiet od wykresu
    label_pad = max_val * (0.05 if device_type == 'mobile' else 0.1)
    
    # Poprawiona wersja:
    for i, (angle, value) in enumerate(zip(angles_radians, values)):
        color = DEGEN_TYPES[labels[i]].get("color", "#3498db")
        
        # Na telefonach wyświetl tylko nazwę typu bez wyniku
        if device_type == 'mobile':
            display_text = f"{labels[i].split()[0]}"  # Use only the first word
        else:
            display_text = f"{labels[i]}\n({value})"
            
        # Add text labels with background for better visibility
        ax.text(angle, value + label_pad, display_text, 
                horizontalalignment='center', verticalalignment='center',
                fontsize=font_size, color=color, fontweight='bold',
                bbox=dict(facecolor='white', alpha=0.7, pad=1.5, edgecolor='none'))
    
    # Optimize layout
    plt.tight_layout(pad=1.0 if device_type == 'mobile' else 1.5)
    
    # Use high DPI for better rendering on high-resolution displays
    fig.set_dpi(120 if device_type == 'mobile' else 100)
    
    return fig
