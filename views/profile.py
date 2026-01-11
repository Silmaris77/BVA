import streamlit as st
import pandas as pd
import random
import re
import os
import numpy as np
import json
from datetime import datetime
from typing import Dict
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from utils.scroll_utils import scroll_to_top
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from data.neuroleader_test_questions import NEUROLEADER_TYPES, TEST_QUESTIONS
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
from config.settings import USER_AVATARS, THEMES, NEUROLEADER_TYPES, BADGES, BADGE_CATEGORIES
from data.neuroleader_details import neuroleader_details
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
    """Sekcja z kartami statystyk użytkownika - identyczna jak w Dashboard"""
    from views.dashboard import save_daily_stats, calculate_stats_changes, format_change_text
    
    # Zapisz dzisiejsze statystyki (jeśli jeszcze nie zostały zapisane)
    save_daily_stats(st.session_state.username)
    
    # Oblicz prawdziwe zmiany statystyk
    current_stats, changes = calculate_stats_changes(st.session_state.username)
    
    # Pobierz podstawowe dane
    xp = current_stats['xp']
    degencoins = current_stats['degencoins']
    completed_lessons = current_stats['completed_lessons']
    level = current_stats['level']
    
    # Formatuj zmiany z odpowiednimi kolorami
    xp_change, xp_color = format_change_text(changes['xp'], use_absolute=True)
    degencoins_change, degencoins_color = format_change_text(changes['degencoins'], use_absolute=True)
    lessons_change, lessons_color = format_change_text(changes['completed_lessons'], use_absolute=True)
    level_change, level_color = format_change_text(changes['level'], use_absolute=True)
    
    # Użyj przekazanego device_type
    if device_type == 'mobile':
        # Mobile - jedna karta z czterema statystykami w środku
        st.markdown("### 📊 Statystyki")
        
        # Stwórz jedną dużą kartę z wewnętrznym gridem 2x2
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 1.5rem;
            color: white;
            box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 1.5rem;
        ">
            <div style="
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-template-rows: 1fr 1fr;
                gap: 1.5rem;
                height: 100%;
            ">
                <div style="
                    text-align: center;
                    padding: 1rem;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                ">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏆</div>
                    <div style="font-size: 1.8rem; font-weight: bold; margin-bottom: 0.3rem;">{xp}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.3rem;">Punkty XP</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: {xp_color};">{xp_change}</div>
                </div>
                <div style="
                    text-align: center;
                    padding: 1rem;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                ">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🪙</div>
                    <div style="font-size: 1.8rem; font-weight: bold; margin-bottom: 0.3rem;">{degencoins}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.3rem;">Monety</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: {degencoins_color};">{degencoins_change}</div>
                </div>
                <div style="
                    text-align: center;
                    padding: 1rem;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                ">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">⭐</div>
                    <div style="font-size: 1.8rem; font-weight: bold; margin-bottom: 0.3rem;">{level}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.3rem;">Poziom</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: {level_color};">{level_change}</div>
                </div>
                <div style="
                    text-align: center;
                    padding: 1rem;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                ">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">📚</div>
                    <div style="font-size: 1.8rem; font-weight: bold; margin-bottom: 0.3rem;">{completed_lessons}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.3rem;">Ukończone lekcje</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: {lessons_color};">{lessons_change}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Desktop i tablet - 4 kolumny
        cols = st.columns(4)
        stats = [
            {"icon": "🏆", "value": f"{xp}", "label": "Punkty XP", "change": xp_change, "color": xp_color},
            {"icon": "🪙", "value": f"{degencoins}", "label": "Monety", "change": degencoins_change, "color": degencoins_color},
            {"icon": "⭐", "value": f"{level}", "label": "Poziom", "change": level_change, "color": level_color},
            {"icon": "📚", "value": f"{completed_lessons}", "label": "Ukończone lekcje", "change": lessons_change, "color": lessons_color}
        ]
        
        # Wygeneruj kartę w każdej kolumnie z gradientowym stylem
        for i, stat in enumerate(stats):
            with cols[i]:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 16px;
                    padding: 0.2rem;
                    text-align: center;
                    color: white;
                    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    min-height: 30px;
                    margin-bottom: 1rem;
                ">
                    <div style="font-size: 2rem; margin-bottom: 0.3rem;">{stat['icon']}</div>
                    <div style="font-size: 1.6rem; font-weight: bold; margin-bottom: 0.2rem;">{stat['value']}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.3rem;">{stat['label']}</div>
                    <div style="font-size: 0.8rem; font-weight: 600; color: {stat['color']};">{stat['change']}</div>
                </div>
                """, unsafe_allow_html=True)


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
      # Use current user data to ensure neuroleader test results are included
    user_data = get_current_user_data(st.session_state.username)
    users_data = load_user_data()  # For shop transactions
    style = get_user_style(st.session_state.username)
    
    # Wyświetl personalizowane style
    st.markdown(generate_user_css(st.session_state.username), unsafe_allow_html=True)
    
    # Add animations and effects using the component
    add_animations_css()

    # Main Profile Tabs - usunięto Personalizację, Eksplorator Typów i Typ Neurolidera
    # Historia XP przeniesiona jako sub-tab w Statystykach
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Statystyki", "🎒 Ekwipunek", "🏆 Odznaki", "📈 Raporty", "⚙️ Ustawienia"])
    
    # Tab 1: Statistics - z sub-tabami
    with tab1:
        scroll_to_top()
        # Sub-taby w Statystykach
        stats_subtab1, stats_subtab2 = st.tabs(["📈 Przegląd", "💰 Historia XP"])
        
        # Sub-tab 1: Przegląd statystyk
        with stats_subtab1:
            show_profile_stats_section(user_data, device_type)
        
        # Sub-tab 2: Historia XP
        with stats_subtab2:
            st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
            show_xp_history_section()
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Tab 2: Inventory/Equipment
    with tab2:
        scroll_to_top()
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        
        # Load user inventory
        inventory = get_user_inventory(st.session_state.username)
          # Create subtabs for different inventory categories
        inv_tabs = st.tabs(["Awatary", "Tła", "Specjalne Lekcje", "Boostery", "🛒 Sklep"])
        
        # Tab for Avatars
        with inv_tabs[0]:
            scroll_to_top()
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
            scroll_to_top()
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
            scroll_to_top()
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
            scroll_to_top()
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
            scroll_to_top()
            st.subheader("🛒 Sklep")            # Display user's DegenCoins
            st.markdown(f"### Twoje DegenCoins: <span style='color: #FFA500;'>🪙 {user_data.get('degencoins', 0)}</span>", unsafe_allow_html=True)
            
            # Shop tabs
            shop_tabs = st.tabs(["Awatary", "Tła", "Specjalne Lekcje", "Boostery"])
            
            # Avatars Shop
            with shop_tabs[0]:
                scroll_to_top()
                st.markdown("#### Awatary Premium 🔗")
                
                # Lista dostępnych awatarów
                avatars = {
                    "diamond_degen": {
                        "name": "💎 Diamond Neuroleader",
                        "price": 500,
                        "description": "Pokazuje twoje zaangażowanie w rozwój jako przywódca."
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
                scroll_to_top()
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
                scroll_to_top()
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
                scroll_to_top()
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
    
    # Tab 3: Badges (poprzednio tab3, bez zmian)
    with tab3:
        scroll_to_top()
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        # Use Step 5 badge display system
        show_badges_section()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Tab 4: Reports (poprzednio tab5, teraz tab4)
    with tab4:
        scroll_to_top()
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        show_reports_section()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Tab 5: Settings - Ustawienia layoutu
    with tab5:
        scroll_to_top()
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        
        zen_header("⚙️ Ustawienia Profilu")
        
        st.markdown("### 🎨 Wybór Layoutu")
        st.markdown("Wybierz styl wizualny aplikacji, który najbardziej Ci odpowiada.")
        
        # Get current theme/layout from user data
        current_layout = user_data.get('layout_preference', 'standard')
        
        # Layout options
        layout_options = {
            "Standard": {
                "value": "standard",
                "description": "Klasyczny layout z niebiesko-zielonymi kolorami",
                "icon": "📘",
                "colors": ["#4A90E2", "#5CB85C", "#2D3748"]
            },
            "Gaming Pro": {
                "value": "gaming-pro",
                "description": "Nowoczesny gaming design z cyber purple i glow effects",
                "icon": "🎮",
                "colors": ["#8B5CF6", "#3B82F6", "#10B981"]
            },
            "Halloween": {
                "value": "halloween",
                "description": "Halloweenowy klimat z dynią i magiczną purpurą",
                "icon": "🎃",
                "colors": ["#FF6B35", "#9D4EDD", "#00FF00"]
            },
            "Executive Pro": {
                "value": "executive-pro",
                "description": "Profesjonalny design dla kadry zarządzającej - Navy, Gold, Platinum",
                "icon": "💼",
                "colors": ["#1E3A8A", "#F59E0B", "#E5E7EB"]
            },
            "Milwaukee": {
                "value": "milwaukee",
                "description": "Heavy Duty Professional - czerwono-czarno-biały branding Milwaukee",
                "icon": "🔴",
                "colors": ["#C8102E", "#1A1A1A", "#FFFFFF"]
            },
            "Glassmorphism": {
                "value": "glassmorphism",
                "description": "Futurystyczny Neon - przeźroczystość, blur i neonowe akcenty",
                "icon": "🔮",
                "colors": ["#667eea", "#0f1219", "#ffffff"]
            }
        }
        
        # Display layout cards
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            # Przygotuj HTML dla kolorów Standard
            standard_colors_html = ''.join([
                f'<div style="width: 40px; height: 40px; border-radius: 50%; background: {color};"></div>'
                for color in layout_options['Standard']['colors']
            ])
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                border-radius: 12px;
                padding: 20px;
                border: {'3px solid #4A90E2' if current_layout == 'standard' else '1px solid #e2e8f0'};
                transition: all 0.3s ease;
                min-height: 200px;
            ">
                <div style="font-size: 48px; text-align: center; margin-bottom: 10px;">
                    {layout_options['Standard']['icon']}
                </div>
                <h3 style="color: #1a202c; text-align: center; margin-bottom: 10px;">
                    Standard
                </h3>
                <p style="color: #4a5568; text-align: center; font-size: 14px; margin-bottom: 15px;">
                    {layout_options['Standard']['description']}
                </p>
                <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                    {standard_colors_html}
                </div>
                {'<div style="text-align: center; margin-top: 15px; color: #4A90E2; font-weight: 600;">✓ Aktywny</div>' 
                 if current_layout == 'standard' else ''}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Wybierz Standard", key="select_standard", use_container_width=True):
                users_data[st.session_state.username]['layout_preference'] = 'standard'
                save_user_data(users_data)
                st.success("✅ Layout zmieniony na Standard!")
                st.info("🔄 Odśwież stronę (F5), aby zobaczyć zmiany")
        
        with col2:
            # Przygotuj HTML dla kolorów Gaming Pro
            gaming_colors_html = ''.join([
                f'<div style="width: 40px; height: 40px; border-radius: 50%; background: {color}; box-shadow: 0 0 10px {color};"></div>'
                for color in layout_options['Gaming Pro']['colors']
            ])
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                border-radius: 12px;
                padding: 20px;
                border: {'3px solid #8B5CF6' if current_layout == 'gaming-pro' else '1px solid #475569'};
                box-shadow: {'0 0 20px rgba(139, 92, 246, 0.6)' if current_layout == 'gaming-pro' else 'none'};
                transition: all 0.3s ease;
                min-height: 200px;
            ">
                <div style="font-size: 48px; text-align: center; margin-bottom: 10px;">
                    {layout_options['Gaming Pro']['icon']}
                </div>
                <h3 style="color: #f8fafc; text-align: center; margin-bottom: 10px;">
                    Gaming Pro
                </h3>
                <p style="color: #cbd5e1; text-align: center; font-size: 14px; margin-bottom: 15px;">
                    {layout_options['Gaming Pro']['description']}
                </p>
                <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                    {gaming_colors_html}
                </div>
                {'<div style="text-align: center; margin-top: 15px; color: #8B5CF6; font-weight: 600; text-shadow: 0 0 10px rgba(139, 92, 246, 0.8);">✓ Aktywny</div>' 
                 if current_layout == 'gaming-pro' else ''}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Wybierz Gaming Pro", key="select_gaming_pro", use_container_width=True):
                users_data[st.session_state.username]['layout_preference'] = 'gaming-pro'
                save_user_data(users_data)
                st.success("✅ Layout zmieniony na Gaming Pro!")
                st.info("🔄 Odśwież stronę (F5), aby zobaczyć zmiany")
        
        with col3:
            # Przygotuj HTML dla kolorów Halloween
            halloween_colors_html = ''.join([
                f'<div style="width: 40px; height: 40px; border-radius: 50%; background: {color}; box-shadow: 0 0 15px {color};"></div>'
                for color in layout_options['Halloween']['colors']
            ])
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1a0b2e 0%, #2d1b3d 100%);
                border-radius: 12px;
                padding: 20px;
                border: {'3px solid #FF6B35' if current_layout == 'halloween' else '1px solid #3d2754'};
                box-shadow: {'0 0 25px rgba(255, 107, 53, 0.8)' if current_layout == 'halloween' else 'none'};
                transition: all 0.3s ease;
                min-height: 200px;
            ">
                <div style="font-size: 48px; text-align: center; margin-bottom: 10px;">
                    {layout_options['Halloween']['icon']}
                </div>
                <h3 style="color: #FFF5E6; text-align: center; margin-bottom: 10px;">
                    Halloween
                </h3>
                <p style="color: #E0D4C8; text-align: center; font-size: 14px; margin-bottom: 15px;">
                    {layout_options['Halloween']['description']}
                </p>
                <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                    {halloween_colors_html}
                </div>
                {'<div style="text-align: center; margin-top: 15px; color: #FF6B35; font-weight: 600; text-shadow: 0 0 15px rgba(255, 107, 53, 0.9);">✓ Aktywny</div>' 
                 if current_layout == 'halloween' else ''}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Wybierz Halloween 🎃", key="select_halloween", use_container_width=True):
                users_data[st.session_state.username]['layout_preference'] = 'halloween'
                save_user_data(users_data)
                st.success("🎃 Layout zmieniony na Halloween!")
                st.info("🔄 Odśwież stronę (F5), aby zobaczyć zmiany")
        
        with col4:
            # Przygotuj HTML dla kolorów Executive Pro
            executive_colors_html = ''.join([
                f'<div style="width: 40px; height: 40px; border-radius: 8px; background: {color}; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);"></div>'
                for color in layout_options['Executive Pro']['colors']
            ])
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
                border-radius: 12px;
                padding: 20px;
                border: {'3px solid #F59E0B' if current_layout == 'executive-pro' else '1px solid #475569'};
                box-shadow: {'0 0 20px rgba(245, 158, 11, 0.5)' if current_layout == 'executive-pro' else 'none'};
                transition: all 0.3s ease;
                min-height: 200px;
            ">
                <div style="font-size: 48px; text-align: center; margin-bottom: 10px;">
                    {layout_options['Executive Pro']['icon']}
                </div>
                <h3 style="color: #F3F4F6; text-align: center; margin-bottom: 10px; font-weight: 600;">
                    Executive Pro
                </h3>
                <p style="color: #D1D5DB; text-align: center; font-size: 14px; margin-bottom: 15px;">
                    {layout_options['Executive Pro']['description']}
                </p>
                <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                    {executive_colors_html}
                </div>
                {'<div style="text-align: center; margin-top: 15px; color: #F59E0B; font-weight: 600; text-shadow: 0 0 10px rgba(245, 158, 11, 0.7);">✓ Aktywny</div>' 
                 if current_layout == 'executive-pro' else ''}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Wybierz Executive Pro 💼", key="select_executive_pro", use_container_width=True):
                users_data[st.session_state.username]['layout_preference'] = 'executive-pro'
                save_user_data(users_data)
                st.success("💼 Layout zmieniony na Executive Pro!")
                st.info("🔄 Odśwież stronę (F5), aby zobaczyć zmiany")
        
        with col5:
            # Przygotuj HTML dla kolorów Milwaukee
            milwaukee_colors_html = ''.join([
                f'<div style="width: 40px; height: 40px; border-radius: 4px; background: {color}; border: 1px solid {"#333" if color == "#FFFFFF" else "transparent"}; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);"></div>'
                for color in layout_options['Milwaukee']['colors']
            ])
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%);
                border-radius: 12px;
                padding: 20px;
                border: {'3px solid #C8102E' if current_layout == 'milwaukee' else '1px solid #4A4A4A'};
                box-shadow: {'0 0 20px rgba(200, 16, 46, 0.6)' if current_layout == 'milwaukee' else 'none'};
                transition: all 0.3s ease;
                min-height: 200px;
            ">
                <div style="font-size: 48px; text-align: center; margin-bottom: 10px;">
                    {layout_options['Milwaukee']['icon']}
                </div>
                <h3 style="color: #FFFFFF; text-align: center; margin-bottom: 10px; font-weight: 700;">
                    Milwaukee
                </h3>
                <p style="color: #E5E5E5; text-align: center; font-size: 14px; margin-bottom: 15px;">
                    {layout_options['Milwaukee']['description']}
                </p>
                <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                    {milwaukee_colors_html}
                </div>
                {'<div style="text-align: center; margin-top: 15px; color: #C8102E; font-weight: 700; text-shadow: 0 0 10px rgba(200, 16, 46, 0.8);">✓ Aktywny</div>' 
                 if current_layout == 'milwaukee' else ''}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Wybierz Milwaukee 🔴", key="select_milwaukee", use_container_width=True):
                users_data[st.session_state.username]['layout_preference'] = 'milwaukee'
                save_user_data(users_data)
                st.success("🔴 Layout zmieniony na Milwaukee!")
                st.info("🔄 Odśwież stronę (F5), aby zobaczyć zmiany")

        with col6:
            # Przygotuj HTML dla kolorów Glassmorphism
            glass_colors_html = ''.join([
                f'<div style="width: 40px; height: 40px; border-radius: 50%; background: {color}; box-shadow: 0 0 10px {color}; border: 1px solid rgba(255,255,255,0.3);"></div>'
                for color in layout_options['Glassmorphism']['colors']
            ])
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border-radius: 12px;
                padding: 20px;
                border: {'3px solid #00f2ff' if current_layout == 'glassmorphism' else '1px solid rgba(255,255,255,0.1)'};
                box-shadow: {'0 0 20px rgba(0, 242, 255, 0.4)' if current_layout == 'glassmorphism' else '0 8px 32px 0 rgba(31, 38, 135, 0.37)'};
                transition: all 0.3s ease;
                min-height: 200px;
            ">
                <div style="font-size: 48px; text-align: center; margin-bottom: 10px;">
                    {layout_options['Glassmorphism']['icon']}
                </div>
                <h3 style="background: linear-gradient(90deg, #00f2ff, #bd00ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 10px; font-weight: 700;">
                    Glassmorphism
                </h3>
                <p style="color: rgba(255,255,255,0.8); text-align: center; font-size: 14px; margin-bottom: 15px;">
                    {layout_options['Glassmorphism']['description']}
                </p>
                <div style="display: flex; justify-content: center; gap: 10px; margin-top: 15px;">
                    {glass_colors_html}
                </div>
                {'<div style="text-align: center; margin-top: 15px; color: #00f2ff; font-weight: 700; text-shadow: 0 0 10px rgba(0, 242, 255, 0.8);">✓ Aktywny</div>' 
                 if current_layout == 'glassmorphism' else ''}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Wybierz Glass 🔮", key="select_glassmorphism", use_container_width=True):
                users_data[st.session_state.username]['layout_preference'] = 'glassmorphism'
                save_user_data(users_data)
                st.success("🔮 Layout zmieniony na Glassmorphism!")
                st.info("🔄 Odśwież stronę (F5), aby zobaczyć zmiany")
        
        st.markdown("---")
        
        # Feature comparison
        st.markdown("### 📋 Porównanie Layoutów")
        
        comparison_data = {
            "Funkcja": [
                "Kolorystyka",
                "Efekty wizualne",
                "Glow effects",
                "Glassmorphism",
                "Animacje hover",
                "Custom scrollbar",
                "Styl",
                "Najlepszy dla"
            ],
            "Standard": [
                "Niebieski + Zielony",
                "Subtelne cienie",
                "❌ Brak",
                "❌ Brak",
                "✅ Podstawowe",
                "❌ Systemowy",
                "Klasyczny, profesjonalny",
                "Praca, nauka"
            ],
            "Gaming Pro": [
                "Cyber Purple + Electric Blue",
                "Mocne cienie + blur",
                "✅ Fioletowa poświata",
                "✅ Semi-transparent + blur",
                "✅ 3D lift + glow",
                "✅ Gradient + glow",
                "Nowoczesny, gamingowy",
                "Gaming, motywacja"
            ],
            "Halloween": [
                "Pumpkin Orange + Magic Purple",
                "Bardzo mocne + blur",
                "✅ Pomarańczowo-fioletowa",
                "✅ Semi-transparent + blur",
                "✅ 3D lift + glow + flame",
                "✅ Gradient + glow + pulse",
                "Halloweenowy, klimatyczny",
                "Halloween, zabawa"
            ],
            "Executive Pro": [
                "Navy Blue + Gold + Platinum",
                "Eleganckie cienie",
                "✅ Złota poświata (subtelna)",
                "✅ Semi-transparent + sharp",
                "✅ Smooth lift + shimmer",
                "✅ Professional gradient",
                "Biznesowy, premium",
                "Kadra zarządzająca, corpo"
            ],
            "Milwaukee": [
                "Milwaukee Red + Black + White",
                "Industrial shadows",
                "✅ Czerwona poświata",
                "❌ Brak (czysty design)",
                "✅ Heavy Duty transitions",
                "✅ Red accent bars",
                "Heavy Duty Professional",
                "Milwaukee, przemysł, branding"
            ]
        }
        
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def show_xp_history_section():
    """Wyświetla szczegółową historię zdobywania XP w profesjonalnym układzie kart"""
    from utils.activity_tracker import get_xp_history
    from data.users import load_user_data
    
    # CSS dla kart
    st.markdown("""
    <style>
    .xp-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08), 0 1px 4px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.06);
    }
    .xp-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.06);
        transform: translateY(-2px);
    }
    .xp-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        height: 100%;
    }
    .xp-metric-value {
        font-size: 42px;
        font-weight: 700;
        line-height: 1;
        margin: 12px 0;
    }
    .xp-metric-label {
        font-size: 13px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 500;
    }
    .xp-metric-help {
        font-size: 12px;
        opacity: 0.8;
        margin-top: 8px;
    }
    .activity-type-card {
        background: white;
        border-radius: 10px;
        padding: 16px;
        margin: 8px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: all 0.2s ease;
    }
    .activity-type-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateX(4px);
    }
    .activity-type-info {
        flex: 1;
    }
    .activity-type-name {
        font-size: 16px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 4px;
    }
    .activity-type-stats {
        font-size: 13px;
        color: #666;
    }
    .activity-type-xp {
        font-size: 24px;
        font-weight: 700;
        color: #667eea;
    }
    .history-row {
        background: #fafafa;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
        display: flex;
        align-items: center;
        gap: 16px;
        transition: all 0.2s ease;
    }
    .history-row:hover {
        background: #f0f0f0;
        transform: translateX(2px);
    }
    .history-icon {
        font-size: 24px;
        min-width: 32px;
    }
    .history-content {
        flex: 1;
    }
    .history-title {
        font-size: 15px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 2px;
    }
    .history-details {
        font-size: 13px;
        color: #666;
    }
    .history-time {
        font-size: 12px;
        color: #999;
        min-width: 120px;
        text-align: right;
    }
    .history-xp {
        font-size: 16px;
        font-weight: 700;
        color: #27ae60;
        min-width: 60px;
        text-align: right;
    }
    .chart-controls {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
    }
    .filter-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    zen_header("💰 Historia Zdobywania XP")
    
    username = st.session_state.username
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    
    # KARTA 1: Główne metryki
    col1, col2, col3 = st.columns(3)
    
    current_xp = user_data.get('xp', 0)
    current_level = user_data.get('level', 1)
    next_level_xp = current_level * 100
    progress = min(100, (current_xp % next_level_xp) / next_level_xp * 100)
    xp_to_next = next_level_xp - (current_xp % next_level_xp)
    
    with col1:
        st.markdown(f"""
        <div class="xp-metric-card">
            <div class="xp-metric-label">Całkowite XP</div>
            <div class="xp-metric-value">{current_xp}</div>
            <div class="xp-metric-help">Suma wszystkich punktów</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="xp-metric-card" style="background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%);">
            <div class="xp-metric-label">Poziom</div>
            <div class="xp-metric-value">{current_level}</div>
            <div class="xp-metric-help">Twój obecny poziom</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="xp-metric-card" style="background: linear-gradient(135deg, #27ae60 0%, #229954 100%);">
            <div class="xp-metric-label">Postęp do {current_level + 1}</div>
            <div class="xp-metric-value">{int(progress)}%</div>
            <div class="xp-metric-help">Brakuje: {xp_to_next} XP</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KARTA 2: Wykres XP
    st.markdown("""
    <div class="xp-card">
        <h3 style="margin-top: 0; color: #1a1a1a;">📊 Wykres Zdobywania XP</h3>
    """, unsafe_allow_html=True)
    
    # Kontrolki wykresu
    st.markdown('<div class="chart-controls">', unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns([3, 1])
    
    with chart_col1:
        chart_period = st.select_slider(
            "Wybierz okres:",
            options=["7 dni", "30 dni", "90 dni", "6 miesięcy", "1 rok", "Wszystko"],
            value="30 dni",
            key="chart_period_slider"
        )
    
    with chart_col2:
        show_cumulative = st.checkbox("Skumulowane", value=False, 
                                      help="Suma narastająca zamiast dziennych przyrostów")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Mapuj okres na dni
    chart_period_days = {
        "7 dni": 7,
        "30 dni": 30,
        "90 dni": 90,
        "6 miesięcy": 180,
        "1 rok": 365,
        "Wszystko": 3650  # ~10 lat
    }
    chart_days = chart_period_days[chart_period]
    
    # Pobierz activity_log z SQL
    from database.models import ActivityLog, User
    from database.connection import session_scope
    from datetime import datetime, timedelta
    import pandas as pd
    
    chart_cutoff_date = datetime.now() - timedelta(days=chart_days)
    
    # Agreguj XP po dniach
    daily_xp = {}
    
    with session_scope() as session:
        # Pobierz użytkownika
        user = session.query(User).filter_by(username=st.session_state.username).first()
        
        if user:
            # Pobierz aktywności z ostatniego okresu
            activities = session.query(ActivityLog)\
                .filter(ActivityLog.user_id == user.user_id)\
                .filter(ActivityLog.timestamp >= chart_cutoff_date)\
                .order_by(ActivityLog.timestamp.asc())\
                .all()
            
            for activity in activities:
                date_key = activity.timestamp.date()
                
                # Pobierz XP z details
                details = activity.details or {}
                xp = details.get('xp_earned', 0)
                
                # Stare wpisy bez xp_earned - przypisz minimalną wartość
                if xp == 0 and activity.activity_type in ['lesson_started', 'lesson_completed', 'quiz_completed', 
                                                           'ai_exercise', 'inspiration_read', 'test_completed', 'tool_used']:
                    xp = 1
                
                if xp > 0:
                    if date_key not in daily_xp:
                        daily_xp[date_key] = 0
                    daily_xp[date_key] += xp
    
    if daily_xp:
        # Stwórz DataFrame z pełnym zakresem dat (wypełnij brakujące dni zerami)
        all_dates = pd.date_range(
            start=chart_cutoff_date.date(),
            end=datetime.now().date(),
            freq='D'
        )
        
        chart_data = pd.DataFrame({
            'Data': all_dates,
            'XP': [daily_xp.get(date.date(), 0) for date in all_dates]
        })
        
        # Jeśli skumulowane, oblicz sumę narastającą
        if show_cumulative:
            chart_data['XP'] = chart_data['XP'].cumsum()
            y_label = "Skumulowane XP"
            chart_title = f"📈 Skumulowane XP w czasie ({chart_period})"
        else:
            y_label = "Dzienne XP"
            chart_title = f"📊 Dzienne zdobywanie XP ({chart_period})"
        
        # Wykres z Plotly dla lepszej interaktywności
        try:
            import plotly.express as px
            
            fig = px.area(
                chart_data,
                x='Data',
                y='XP',
                title=chart_title,
                labels={'XP': y_label, 'Data': 'Data'},
                color_discrete_sequence=['#667eea']
            )
            
            fig.update_traces(
                line=dict(width=2),
                fillcolor='rgba(102, 126, 234, 0.2)',
                hovertemplate='<b>%{x|%Y-%m-%d}</b><br>XP: %{y}<extra></extra>'
            )
            
            fig.update_layout(
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.2)',
                    title_font=dict(size=14)
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.2)',
                    title_font=dict(size=14)
                ),
                title_font=dict(size=18, color='#667eea'),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Statystyki pod wykresem w kartach
            st.markdown("<br>", unsafe_allow_html=True)
            col_chart1, col_chart2, col_chart3, col_chart4 = st.columns(4)
            
            with col_chart1:
                total_chart_xp = chart_data['XP'].sum() if not show_cumulative else chart_data['XP'].iloc[-1]
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e8f5e9, #f1f8f4); 
                            border-radius: 10px; padding: 16px; text-align: center;
                            border-left: 4px solid #4caf50;">
                    <div style="font-size: 12px; color: #666; margin-bottom: 4px;">Łącznie XP</div>
                    <div style="font-size: 28px; font-weight: 700; color: #27ae60;">{int(total_chart_xp)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_chart2:
                try:
                    if not show_cumulative:
                        avg_daily_xp = chart_data['XP'].mean()
                    else:
                        daily_diff = chart_data['XP'].diff()
                        avg_daily_xp = daily_diff[daily_diff.notna()].mean() if len(daily_diff) > 1 else 0
                    avg_val = int(avg_daily_xp) if avg_daily_xp and str(avg_daily_xp) != 'nan' else 0
                except:
                    avg_val = 0
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e3f2fd, #f0f7fc); 
                            border-radius: 10px; padding: 16px; text-align: center;
                            border-left: 4px solid #2196f3;">
                    <div style="font-size: 12px; color: #666; margin-bottom: 4px;">Średnio/dzień</div>
                    <div style="font-size: 28px; font-weight: 700; color: #1976d2;">{avg_val}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_chart3:
                try:
                    if not show_cumulative:
                        max_daily_xp = chart_data['XP'].max()
                    else:
                        daily_diff = chart_data['XP'].diff()
                        max_daily_xp = daily_diff[daily_diff.notna()].max() if len(daily_diff) > 1 else 0
                    max_val = int(max_daily_xp) if max_daily_xp and str(max_daily_xp) != 'nan' else 0
                except:
                    max_val = 0
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fff3e0, #fef7ed); 
                            border-radius: 10px; padding: 16px; text-align: center;
                            border-left: 4px solid #ff9800;">
                    <div style="font-size: 12px; color: #666; margin-bottom: 4px;">Najlepszy dzień</div>
                    <div style="font-size: 28px; font-weight: 700; color: #f57c00;">{max_val}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_chart4:
                days_with_activity = (chart_data['XP'] > 0).sum() if not show_cumulative else None
                if days_with_activity is not None:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f3e5f5, #f8f0fa); 
                                border-radius: 10px; padding: 16px; text-align: center;
                                border-left: 4px solid #9c27b0;">
                        <div style="font-size: 12px; color: #666; margin-bottom: 4px;">Dni aktywnych</div>
                        <div style="font-size: 28px; font-weight: 700; color: #7b1fa2;">{days_with_activity}/{len(chart_data)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    trend_icon = "📈" if chart_data['XP'].iloc[-1] > chart_data['XP'].iloc[0] else "📉"
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f3e5f5, #f8f0fa); 
                                border-radius: 10px; padding: 16px; text-align: center;
                                border-left: 4px solid #9c27b0;">
                        <div style="font-size: 12px; color: #666; margin-bottom: 4px;">Trend</div>
                        <div style="font-size: 28px; font-weight: 700;">{trend_icon}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
        except ImportError:
            # Fallback do prostego wykresu Streamlit
            st.line_chart(chart_data.set_index('Data')['XP'])
    else:
        st.info(f"Brak danych XP w wybranym okresie ({chart_period}). Zacznij zdobywać doświadczenie!")
    
    st.markdown("</div>", unsafe_allow_html=True)  # Zamknięcie xp-card
    
    # KARTA 3: Filtry
    st.markdown("""
    <div class="xp-card">
        <h3 style="margin-top: 0; color: #1a1a1a;">🔍 Filtry i Statystyki</h3>
        <div class="filter-card">
    """, unsafe_allow_html=True)
    
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        period = st.selectbox(
            "Okres",
            ["Ostatnie 7 dni", "Ostatnie 30 dni", "Ostatnie 90 dni", "Wszystko"],
            index=1
        )
    
    with col_filter2:
        activity_types = {
            "Wszystkie": None,
            "Lekcje": ["lesson_started", "lesson_completed"],
            "Quizy": ["quiz_completed"],
            "Inspiracje": ["inspiration_read"],
            "Narzędzia": ["tool_used"],
            "Ćwiczenia AI": ["ai_exercise"],
            "Testy diagnostyczne": ["test_completed"]
        }
        filter_type = st.selectbox("Typ aktywności", list(activity_types.keys()))
    
    st.markdown("</div>", unsafe_allow_html=True)  # Zamknięcie filter-card
    
    # Mapuj okres na dni
    period_days = {
        "Ostatnie 7 dni": 7,
        "Ostatnie 30 dni": 30,
        "Ostatnie 90 dni": 90,
        "Wszystko": 365
    }
    days = period_days[period]
    
    # Pobierz activity_log z SQL
    from database.models import ActivityLog, User
    from database.connection import session_scope
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    
    filtered_activities = []
    
    with session_scope() as session:
        # Pobierz użytkownika
        user = session.query(User).filter_by(username=st.session_state.username).first()
        
        if user:
            # Pobierz aktywności z ostatniego okresu
            activities = session.query(ActivityLog)\
                .filter(ActivityLog.user_id == user.user_id)\
                .filter(ActivityLog.timestamp >= cutoff_date)\
                .order_by(ActivityLog.timestamp.desc())\
                .all()
            
            for activity in activities:
                # Filtruj po typie aktywności
                if activity_types[filter_type] is None or activity.activity_type in activity_types[filter_type]:
                    # Sprawdź czy ma XP (albo z details, albo domyślne)
                    details = activity.details or {}
                    xp_earned = details.get('xp_earned', 0)
                    if xp_earned > 0 or activity.activity_type in ['lesson_started', 'lesson_completed', 'quiz_completed', 
                                                                     'inspiration_read', 'tool_used', 'ai_exercise', 'test_completed']:
                        # Konwertuj do formatu zgodnego z resztą kodu
                        filtered_activities.append({
                            'type': activity.activity_type,
                            'timestamp': activity.timestamp.isoformat(),
                            'details': details
                        })
    
    # Statystyki przefiltrowanych danych
    st.markdown("---")
    st.markdown(f"### 📊 Statystyki: {period}")
    
    # Oblicz statystyki
    total_xp_period = 0
    activity_breakdown = {}
    
    for entry in filtered_activities:
        # Pobierz XP z details (powinno zawsze być dla nowych wpisów)
        details = entry.get('details', {})
        xp = details.get('xp_earned', 0)
        
        # Tylko jeśli brak xp_earned (stare wpisy), pomiń lub użyj wartości domyślnej
        if xp == 0:
            # Dla starych wpisów bez xp_earned - pomiń lub przypisz minimalną wartość
            xp = 1 if entry['type'] in ['lesson_started', 'lesson_completed', 'quiz_completed', 
                                          'ai_exercise', 'inspiration_read', 'test_completed', 'tool_used'] else 0
        
        if xp > 0:
            total_xp_period += xp
        
        # Grupuj po typie
        activity_type = entry['type']
        if activity_type not in activity_breakdown:
            activity_breakdown[activity_type] = {'count': 0, 'xp': 0}
        activity_breakdown[activity_type]['count'] += 1
        activity_breakdown[activity_type]['xp'] += xp
    
    # Statystyki w kartach
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                    border-radius: 10px; padding: 20px; text-align: center; color: white;">
            <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px;">ZDOBYTE XP</div>
            <div style="font-size: 32px; font-weight: 700;">{total_xp_period}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_stat2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f39c12, #e74c3c); 
                    border-radius: 10px; padding: 20px; text-align: center; color: white;">
            <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px;">AKTYWNOŚCI</div>
            <div style="font-size: 32px; font-weight: 700;">{len(filtered_activities)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_stat3:
        avg_xp = total_xp_period / len(filtered_activities) if filtered_activities else 0
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #27ae60, #229954); 
                    border-radius: 10px; padding: 20px; text-align: center; color: white;">
            <div style="font-size: 13px; opacity: 0.9; margin-bottom: 8px;">ŚREDNIO/AKTYWNOŚĆ</div>
            <div style="font-size: 32px; font-weight: 700;">{avg_xp:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Wykres breakdown po typach
    if activity_breakdown:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h4 style="color: #1a1a1a; margin: 20px 0 16px 0;">📈 Rozkład XP według typu aktywności</h4>', unsafe_allow_html=True)
        
        # Mapowanie nazw typów aktywności
        type_names = {
            'lesson_started': '📖 Lekcje rozpoczęte',
            'lesson_completed': '✅ Lekcje ukończone',
            'quiz_completed': '📝 Quizy',
            'inspiration_read': '💡 Inspiracje',
            'tool_used': '🛠️ Narzędzia',
            'ai_exercise': '🤖 Ćwiczenia AI',
            'test_completed': '🎯 Testy diagnostyczne'
        }
        
        # Kolory dla różnych typów
        type_colors = {
            'lesson_started': '#3498db',
            'lesson_completed': '#27ae60',
            'quiz_completed': '#9b59b6',
            'inspiration_read': '#f39c12',
            'tool_used': '#e74c3c',
            'ai_exercise': '#1abc9c',
            'test_completed': '#34495e'
        }
        
        # Sortuj po XP
        sorted_breakdown = sorted(activity_breakdown.items(), key=lambda x: x[1]['xp'], reverse=True)
        
        for act_type, stats in sorted_breakdown:
            color = type_colors.get(act_type, '#667eea')
            name = type_names.get(act_type, act_type)
            count = stats['count']
            xp = stats['xp']
            avg = xp / count
            
            st.markdown(f"""
            <div class="activity-type-card" style="border-left-color: {color};">
                <div class="activity-type-info">
                    <div class="activity-type-name">{name}</div>
                    <div class="activity-type-stats">{count} aktywności • Średnio {avg:.1f} XP</div>
                </div>
                <div class="activity-type-xp" style="color: {color};">{xp} XP</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Zamknięcie xp-card
    
    # KARTA 4: Szczegółowa historia
    st.markdown("""
    <div class="xp-card">
        <h3 style="margin-top: 0; color: #1a1a1a;">📜 Szczegółowa Historia Aktywności</h3>
    """, unsafe_allow_html=True)
    
    if not filtered_activities:
        st.info(f"Brak aktywności w wybranym okresie ({period}).")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Ikony dla typów aktywności
        type_icons = {
            'lesson_started': '📖',
            'lesson_completed': '✅',
            'quiz_completed': '📝',
            'inspiration_read': '💡',
            'tool_used': '🛠️',
            'ai_exercise': '🤖',
            'test_completed': '🎯'
        }
        
        type_names = {
            'lesson_started': 'Rozpoczęcie lekcji',
            'lesson_completed': 'Ukończenie lekcji',
            'quiz_completed': 'Quiz',
            'inspiration_read': 'Przeczytanie inspiracji',
            'tool_used': 'Użycie narzędzia',
            'ai_exercise': 'Ćwiczenie AI',
            'test_completed': 'Test diagnostyczny'
        }
        
        # Sortuj aktywności po czasie (najnowsze pierwsze)
        sorted_activities = sorted(filtered_activities, key=lambda x: x['timestamp'], reverse=True)
        
        # Paginacja
        items_per_page = 15
        total_items = len(sorted_activities)
        total_pages = (total_items - 1) // items_per_page + 1
        
        if total_pages > 1:
            page = st.selectbox("Strona", range(1, total_pages + 1), key="xp_history_page")
            start_idx = (page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_items)
            page_activities = sorted_activities[start_idx:end_idx]
            st.caption(f"Pokazuję {start_idx + 1}-{end_idx} z {total_items} aktywności")
        else:
            page_activities = sorted_activities
        
        # Wyświetl aktywności jako karty
        for entry in page_activities:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            activity_type = entry['type']
            details = entry.get('details', {})
            
            # Pobierz XP z details (powinno zawsze być dla nowych wpisów)
            xp = details.get('xp_earned', 0)
            
            # Stare wpisy bez xp_earned - przypisz minimalną wartość
            if xp == 0 and activity_type in ['lesson_started', 'lesson_completed', 'quiz_completed', 
                                               'ai_exercise', 'inspiration_read', 'test_completed', 'tool_used']:
                xp = 1
            
            # Przygotuj szczegóły
            extra_info = ""
            if activity_type == 'quiz_completed':
                score = details.get('score_percentage', 0)
                extra_info = f"Wynik: {score}%"
            elif activity_type == 'test_completed':
                test_name = details.get('test_name', '')
                extra_info = test_name
            elif activity_type == 'tool_used':
                tool_name = details.get('tool_name', '')
                extra_info = tool_name
            elif activity_type == 'ai_exercise':
                exercise_name = details.get('exercise_name', '')
                extra_info = exercise_name
            elif activity_type == 'inspiration_read':
                insp_id = details.get('inspiration_id', '')
                extra_info = f"ID: {insp_id}" if insp_id else ""
            
            icon = type_icons.get(activity_type, '📌')
            name = type_names.get(activity_type, activity_type)
            time_str = timestamp.strftime('%d.%m.%Y %H:%M')
            
            st.markdown(f"""
            <div class="history-row">
                <div class="history-icon">{icon}</div>
                <div class="history-content">
                    <div class="history-title">{name}</div>
                    <div class="history-details">{extra_info}</div>
                </div>
                <div class="history-time">{time_str}</div>
                <div class="history-xp">+{xp} XP</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)  # Zamknięcie xp-card

def show_reports_section():
    """Wyświetla sekcję raportów rozwojowych użytkownika z pod-tabami"""
    st.header("📈 Twoje Raporty Rozwojowe")
    
    username = st.session_state.username
    
    # Taby dla różnych typów raportów
    tab1, tab2 = st.tabs(["📊 Raporty Tygodniowe", "🪞 Kim Jestem?"])
    
    with tab1:
        show_weekly_reports_tab(username)
    
    with tab2:
        show_who_am_i_report_tab(username)


def show_weekly_reports_tab(username: str):
    """Wyświetla zakładkę z raportami tygodniowymi"""
    from utils.activity_tracker import (
        get_activity_summary,
        get_login_pattern,
        get_lesson_completion_stats,
        get_quiz_performance_stats,
        get_xp_history,
        initialize_activity_tracking
    )
    from utils.report_generator import (
        generate_weekly_report_ai,
        save_report_to_user_profile,
        get_user_reports,
        should_generate_auto_report
    )
    
    # Inicjalizuj tracking jeśli nie istnieje
    initialize_activity_tracking(username)
    
    # Sprawdź czy powinien zostać wygenerowany automatyczny raport
    auto_report_due = should_generate_auto_report(username)
    
    if auto_report_due:
        st.info("📅 **Automatyczny raport tygodniowy** jest gotowy do wygenerowania! Kliknij przycisk poniżej.")
    
    # Przyciski akcji
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("📊 Wygeneruj nowy raport tygodniowy", type="primary", use_container_width=True):
            with st.spinner("🤖 AI analizuje Twoją aktywność..."):
                # Zbierz dane
                activity_summary = get_activity_summary(username, days=7)
                login_pattern = get_login_pattern(username, days=30)
                lesson_stats = get_lesson_completion_stats(username)
                quiz_stats = get_quiz_performance_stats(username, days=30)
                
                # Generuj raport AI
                report = generate_weekly_report_ai(username, activity_summary, login_pattern, lesson_stats, quiz_stats)
                
                # Zapisz do profilu
                save_report_to_user_profile(username, report)
                
                st.success("✅ Raport został wygenerowany!")
                st.rerun()
    
    with col2:
        # Przycisk do pobrania ostatniego raportu
        reports = get_user_reports(username, limit=1)
        if reports:
            latest_report = reports[0]
            report_json = json.dumps(latest_report, indent=2, ensure_ascii=False)
            st.download_button(
                label="💾 Pobierz",
                data=report_json,
                file_name=f"raport_{username}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Pobierz historyczne raporty
    reports = get_user_reports(username, limit=10)
    
    if not reports:
        st.info("📝 Nie masz jeszcze żadnych raportów. Kliknij przycisk powyżej aby wygenerować pierwszy raport tygodniowy!")
        
        # Pokaż przykładowy raport
        with st.expander("🔍 Co zawiera raport rozwojowy?", expanded=True):
            st.markdown("""
            Twój spersonalizowany raport tygodniowy analizuje:
            
            **📊 Twarde dane:**
            - Liczba dni z logowaniem
            - Ukończone i rozpoczęte lekcje
            - Sesje ćwiczeń AI
            - Użycie narzędzi i symulatorów
            - Przeczytane inspiracje
            
            **🧠 Analiza AI:**
            - Ocena zaangażowania (1-10)
            - Wykryte wzorce aktywności
            - Mocne strony w nauce
            - Obszary do poprawy
            
            **🎯 Rekomendacje:**
            - 3-5 spersonalizowanych akcji
            - Priorytety (wysoki/średni/niski)
            - Szacowany czas realizacji
            - Uzasadnienie każdej rekomendacji
            
            **💬 Motywacja:**
            - Osobista wiadomość od AI
            - Dopasowana do Twojego profilu (Kolb/Neuroleader)
            """)
        
        return
    
    # Wyświetl najnowszy raport szczegółowo
    st.markdown("### 📊 Najnowszy raport")
    display_report_detailed(reports[0])
    
    # Historia raportów
    if len(reports) > 1:
        st.markdown("---")
        st.markdown("### 📚 Historia raportów")
        
        for i, report in enumerate(reports[1:], 1):
            with st.expander(
                f"📅 Raport z {datetime.fromisoformat(report['generated_at']).strftime('%d.%m.%Y')} "
                f"- {report.get('engagement_score', 0)}/10 zaangażowania",
                expanded=False
            ):
                display_report_compact(report)


def show_who_am_i_report_tab(username: str):
    """Wyświetla zakładkę z raportem 'Kim Jestem?'"""
    from data.users import load_user_data
    from utils.profile_report import collect_user_profile_data
    
    # Pobierz dane użytkownika
    users_data = load_user_data()
    if username not in users_data:
        st.error("❌ Nie znaleziono danych użytkownika")
        return
    
    user_data = users_data[username]
    user_data['username'] = username
    
    # Sprawdź czy są jakieś testy
    has_tests = any([
        'kolb_test' in user_data and user_data['kolb_test'],
        'test_scores' in user_data and user_data['test_scores'],
        'mi_test' in user_data and user_data['mi_test']
    ])
    
    if not has_tests:
        st.warning("⚠️ Nie wykonałeś jeszcze żadnego testu diagnostycznego. Wykonaj przynajmniej jeden test aby wygenerować raport.")
        st.info("💡 Przejdź do sekcji **Narzędzia → Autodiagnoza** aby wykonać testy.")
        
        # Pokaż podgląd co zawiera raport
        with st.expander("🔍 Co zawiera raport 'Kim Jestem?'", expanded=True):
            st.markdown("""
            Kompleksowy raport tożsamości zawiera:
            
            **🧭 Synteza Osobista:**
            - Twój unikalny profil uczenia się
            - Opis kim jesteś jako lider i uczeń
            - Połączenie wszystkich wyników diagnostycznych
            
            **📊 Wyniki Testów:**
            - Test Kolba (styl uczenia się)
            - Test Neuroleader (typ przywództwa)
            - Test MI (wielorakie inteligencje)
            
            **💪 Mocne Strony:**
            - Top 5 Twoich największych atutów
            - Źródło każdej mocnej strony
            - Konkretne opisy jak je wykorzystać
            
            **📈 Aktywność:**
            - Ukończone i rozpoczęte moduły
            - Postęp w kursie
            - Wynik zaangażowania
            
            **🚀 Rekomendacje:**
            - Top 5 spersonalizowanych następnych kroków
            - Priorytety (wysokie/średnie/niskie)
            - Konkretne akcje do wykonania
            
            **📥 Eksport PDF:**
            - Pobierz kompletny raport
            - Profesjonalne formatowanie
            - Gotowy do wydruku
            """)
        
        return
    
    # Pokaż ile testów ma użytkownik
    tests_count = sum([
        bool('kolb_test' in user_data and user_data['kolb_test']),
        bool('test_scores' in user_data and user_data['test_scores']),
        bool('mi_test' in user_data and user_data['mi_test'])
    ])
    
    # Informacja o testach i przycisk
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"✅ Masz ukończone **{tests_count}/3** testy diagnostyczne. Kliknij przycisk aby wygenerować kompleksowy raport.")
    with col2:
        generate_button = st.button("🔍 Wygeneruj raport", type="primary", use_container_width=True)
    
    # Generuj raport jeśli kliknięto przycisk
    if generate_button:
        st.markdown("---")
        generate_who_am_i_report_ui(username)

def display_xp_chart(username: str):
    """Wyświetla wykres przyrostu XP z ostatnich 30 dni"""
    from utils.activity_tracker import get_xp_history
    import plotly.graph_objects as go
    from datetime import datetime, timedelta
    
    # Pobierz dane XP
    xp_data = get_xp_history(username, days=30)
    
    if not xp_data['daily_xp']:
        st.info("📊 Brak danych o XP z ostatnich 30 dni. Zacznij wykonywać aktywności, aby zobaczyć wykres!")
        return
    
    # Przygotuj dane - uzupełnij brakujące dni zerami
    all_dates = []
    current_date = datetime.now().date()
    for i in range(29, -1, -1):  # 30 dni wstecz
        all_dates.append((current_date - timedelta(days=i)).strftime('%Y-%m-%d'))
    
    # Mapuj XP na wszystkie dni
    xp_dict = dict(xp_data['daily_xp'])
    daily_values = [xp_dict.get(date, 0) for date in all_dates]
    
    # Oblicz skumulowany XP
    cumulative_xp = []
    total = 0
    for xp in daily_values:
        total += xp
        cumulative_xp.append(total)
    
    # Stwórz wykres
    fig = go.Figure()
    
    # Słupki - dzienny XP
    fig.add_trace(go.Bar(
        x=all_dates,
        y=daily_values,
        name='Dzienny XP',
        marker_color='rgba(102, 126, 234, 0.6)',
        hovertemplate='<b>%{x}</b><br>XP zdobyte: %{y}<extra></extra>'
    ))
    
    # Linia - skumulowany XP
    fig.add_trace(go.Scatter(
        x=all_dates,
        y=cumulative_xp,
        name='Łączny XP',
        mode='lines+markers',
        line=dict(color='rgba(118, 75, 162, 0.8)', width=3),
        marker=dict(size=6, color='rgba(118, 75, 162, 1)'),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Łącznie: %{y} XP<extra></extra>'
    ))
    
    # Layout
    fig.update_layout(
        title=None,
        xaxis=dict(
            title='Data',
            tickangle=-45,
            tickmode='array',
            tickvals=all_dates[::5],  # Co 5 dni
            ticktext=[datetime.strptime(d, '%Y-%m-%d').strftime('%d.%m') for d in all_dates[::5]]
        ),
        yaxis=dict(
            title='XP zdobyte dziennie',
            side='left',
            showgrid=True
        ),
        yaxis2=dict(
            title='Łączny XP',
            side='right',
            overlaying='y',
            showgrid=False
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        hovermode='x unified',
        height=400,
        margin=dict(l=50, r=50, t=30, b=80),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statystyki pod wykresem
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Łącznie zdobyte",
            f"{xp_data['total_xp_gained']} XP",
            help="Suma XP zdobytych w ostatnich 30 dniach"
        )
    
    with col2:
        st.metric(
            "Średnio dziennie",
            f"{xp_data['avg_daily_xp']} XP",
            help="Średnia dzienna zdobyta w ostatnich 30 dniach"
        )
    
    with col3:
        most_date, most_xp = xp_data['most_productive_day']
        if most_date:
            formatted_date = datetime.strptime(most_date, '%Y-%m-%d').strftime('%d.%m')
            st.metric(
                "Najlepszy dzień",
                f"{most_xp} XP",
                delta=formatted_date,
                help=f"Najwięcej XP zdobytych w jednym dniu"
            )
        else:
            st.metric("Najlepszy dzień", "—")
    
    with col4:
        st.metric(
            "Obecny poziom",
            f"Level {xp_data['current_level']}",
            delta=f"{xp_data['current_xp']} XP",
            help="Twój aktualny poziom i całkowite XP"
        )

def display_report_detailed(report: Dict):
    """Wyświetla szczegółowy raport w profesjonalnym układzie kart"""
    
    # CSS dla kart Material Design 3
    st.markdown("""
    <style>
    .report-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08), 0 1px 4px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.06);
    }
    .report-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.06);
        transform: translateY(-2px);
    }
    .card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 2px solid #f0f0f0;
    }
    .card-icon {
        font-size: 28px;
        line-height: 1;
    }
    .card-title {
        font-size: 20px;
        font-weight: 600;
        color: #1a1a1a;
        margin: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .metric-value {
        font-size: 48px;
        font-weight: 700;
        line-height: 1;
        margin: 8px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-trend {
        font-size: 16px;
        margin-top: 8px;
        font-weight: 500;
    }
    .strength-item {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8f4 100%);
        border-left: 4px solid #4caf50;
        padding: 16px;
        border-radius: 8px;
        margin: 8px 0;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }
    .concern-item {
        background: linear-gradient(135deg, #fff3e0 0%, #fef7ed 100%);
        border-left: 4px solid #ff9800;
        padding: 16px;
        border-radius: 8px;
        margin: 8px 0;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }
    .insight-item {
        background: linear-gradient(135deg, #e3f2fd 0%, #f0f7fc 100%);
        border-left: 4px solid #2196f3;
        padding: 16px;
        border-radius: 8px;
        margin: 8px 0;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }
    .recommendation-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        border: 2px solid #e0e0e0;
        transition: all 0.2s ease;
    }
    .recommendation-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    .recommendation-card.priority-high {
        border-left: 6px solid #e74c3c;
    }
    .recommendation-card.priority-medium {
        border-left: 6px solid #f39c12;
    }
    .recommendation-card.priority-low {
        border-left: 6px solid #27ae60;
    }
    .rec-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }
    .rec-title {
        font-size: 18px;
        font-weight: 600;
        color: #1a1a1a;
        flex: 1;
    }
    .rec-badge {
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    .rec-badge.high {
        background: #fee;
        color: #e74c3c;
    }
    .rec-badge.medium {
        background: #fff4e6;
        color: #f39c12;
    }
    .rec-badge.low {
        background: #e8f5e9;
        color: #27ae60;
    }
    .rec-why {
        color: #666;
        font-size: 15px;
        line-height: 1.6;
        margin: 8px 0;
    }
    .rec-time {
        color: #999;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 12px;
    }
    .motivational-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 28px;
        color: white;
        margin: 20px 0;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }
    .motivational-card h3 {
        color: white;
        margin-top: 0;
        margin-bottom: 16px;
        font-size: 22px;
    }
    .motivational-card p {
        font-size: 16px;
        line-height: 1.7;
        margin: 0;
        opacity: 0.95;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Nagłówek raportu
    period_start = datetime.fromisoformat(report['period_start']).strftime('%d.%m.%Y')
    period_end = datetime.fromisoformat(report['period_end']).strftime('%d.%m.%Y')
    
    st.markdown(f"""
    <div style="text-align: center; margin: 24px 0 32px 0;">
        <h2 style="margin: 0 0 8px 0; color: #1a1a1a;">{report.get('summary_headline', '📊 Raport Tygodniowy')}</h2>
        <p style="color: #666; font-size: 16px; margin: 0;">📅 {period_start} - {period_end}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KARTA 1: Metryka zaangażowania
    score = report.get('engagement_score', 0)
    trend = report.get('engagement_trend', 'stabilny')
    
    trend_emoji = {
        'rosnący': '📈',
        'stabilny': '➡️',
        'spadający': '📉'
    }
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Twoje zaangażowanie</div>
        <div class="metric-value">{score}<span style="font-size: 28px; opacity: 0.8;">/10</span></div>
        <div class="metric-trend">{trend_emoji.get(trend, '➡️')} {trend.capitalize()}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # KARTA 2: Wykres XP
    st.markdown("""
    <div class="report-card">
        <div class="card-header">
            <div class="card-icon">📈</div>
            <div class="card-title">Przyrost XP w ostatnich 30 dniach</div>
        </div>
    """, unsafe_allow_html=True)
    display_xp_chart(st.session_state.username)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # KARTA 3: Mocne strony
    strengths = report.get('strengths', [])
    if strengths:
        st.markdown("""
        <div class="report-card">
            <div class="card-header">
                <div class="card-icon">💪</div>
                <div class="card-title">Twoje mocne strony</div>
            </div>
        """, unsafe_allow_html=True)
        
        for strength in strengths:
            st.markdown(f"""
            <div class="strength-item">
                <div style="font-size: 20px;">✓</div>
                <div style="flex: 1; line-height: 1.5;">{strength}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # KARTA 4: Obszary do poprawy
    concerns = report.get('concerns', [])
    if concerns:
        st.markdown("""
        <div class="report-card">
            <div class="card-header">
                <div class="card-icon">🎓</div>
                <div class="card-title">Obszary do rozwoju</div>
            </div>
        """, unsafe_allow_html=True)
        
        for concern in concerns:
            st.markdown(f"""
            <div class="concern-item">
                <div style="font-size: 20px;">→</div>
                <div style="flex: 1; line-height: 1.5;">{concern}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # KARTA 5: Wykryte wzorce
    insights = report.get('insights', [])
    if insights:
        st.markdown("""
        <div class="report-card">
            <div class="card-header">
                <div class="card-icon">🔍</div>
                <div class="card-title">Wykryte wzorce</div>
            </div>
        """, unsafe_allow_html=True)
        
        for insight in insights:
            st.markdown(f"""
            <div class="insight-item">
                <div style="font-size: 20px;">💡</div>
                <div style="flex: 1; line-height: 1.5;">{insight}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # KARTA 6: Rekomendacje
    recommendations = report.get('recommendations', [])
    if recommendations:
        st.markdown("""
        <div class="report-card">
            <div class="card-header">
                <div class="card-icon">🎯</div>
                <div class="card-title">Twój plan działania na następny tydzień</div>
            </div>
        """, unsafe_allow_html=True)
        
        priority_map = {
            'wysoki': 'high',
            'średni': 'medium',
            'niski': 'low'
        }
        
        priority_labels = {
            'wysoki': 'Wysoki priorytet',
            'średni': 'Średni priorytet',
            'niski': 'Niski priorytet'
        }
        
        for i, rec in enumerate(recommendations, 1):
            priority = rec.get('priority', 'średni')
            priority_class = priority_map.get(priority, 'medium')
            priority_label = priority_labels.get(priority, 'Średni priorytet')
            action = rec.get('action', '')
            why = rec.get('why', '')
            time = rec.get('estimated_time', '')
            
            st.markdown(f"""
            <div class="recommendation-card priority-{priority_class}">
                <div class="rec-header">
                    <div class="rec-title">{i}. {action}</div>
                    <span class="rec-badge {priority_class}">{priority_label}</span>
                </div>
                <div class="rec-why">{why}</div>
                <div class="rec-time">
                    <span>⏱️</span>
                    <span>Szacowany czas: {time}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # KARTA 7: Wiadomość motywacyjna
    motivational_message = report.get('motivational_message', '')
    if motivational_message:
        st.markdown(f"""
        <div class="motivational-card">
            <h3>💬 Wiadomość dla Ciebie</h3>
            <p>{motivational_message}</p>
        </div>
        """, unsafe_allow_html=True)

def display_report_compact(report: Dict):
    """Wyświetla skróconą wersję raportu w układzie kart"""
    
    # Podstawowe info w kartach
    col1, col2, col3 = st.columns(3)
    
    score = report.get('engagement_score', 0)
    trend = report.get('engagement_trend', 'stabilny')
    recommendations_count = len(report.get('recommendations', []))
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 12px; padding: 20px; color: white; text-align: center;
                    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);">
            <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">ZAANGAŻOWANIE</div>
            <div style="font-size: 36px; font-weight: 700;">{score}/10</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        trend_colors = {
            'rosnący': '#27ae60',
            'stabilny': '#3498db',
            'spadający': '#e74c3c'
        }
        trend_emoji = {
            'rosnący': '📈',
            'stabilny': '➡️',
            'spadający': '📉'
        }
        color = trend_colors.get(trend, '#3498db')
        emoji = trend_emoji.get(trend, '➡️')
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {color}e6, {color}); 
                    border-radius: 12px; padding: 20px; color: white; text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
            <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">TREND</div>
            <div style="font-size: 28px; font-weight: 600;">{emoji} {trend.capitalize()}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f39c12e6, #f39c12); 
                    border-radius: 12px; padding: 20px; color: white; text-align: center;
                    box-shadow: 0 2px 8px rgba(243, 156, 18, 0.3);">
            <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">REKOMENDACJE</div>
            <div style="font-size: 36px; font-weight: 700;">{recommendations_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Top rekomendacja
    recommendations = report.get('recommendations', [])
    high_priority = [r for r in recommendations if r.get('priority') == 'wysoki']
    
    if high_priority:
        action = high_priority[0].get('action', '')
        st.markdown(f"""
        <div style="background: white; border-left: 6px solid #e74c3c; 
                    border-radius: 8px; padding: 16px; margin: 12px 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <div style="color: #e74c3c; font-size: 12px; font-weight: 600; 
                        text-transform: uppercase; margin-bottom: 8px;">🔴 Wysoki priorytet</div>
            <div style="font-size: 16px; font-weight: 500; color: #1a1a1a;">{action}</div>
        </div>
        """, unsafe_allow_html=True)
    elif recommendations:
        action = recommendations[0].get('action', '')
        st.markdown(f"""
        <div style="background: white; border-left: 6px solid #3498db; 
                    border-radius: 8px; padding: 16px; margin: 12px 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <div style="color: #3498db; font-size: 12px; font-weight: 600; 
                        text-transform: uppercase; margin-bottom: 8px;">🎯 Top rekomendacja</div>
            <div style="font-size: 16px; font-weight: 500; color: #1a1a1a;">{action}</div>
        </div>
        """, unsafe_allow_html=True)

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
            - **🔍 Odkrywca Osobowości** - Wykonaj test typu neurolidera (znajdziesz go w zakładce 🛠️ Narzędzia → 🎯 Autodiagnoza)
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
            scroll_to_top()
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
    """Calculate the dominant neuroleader type based on test scores"""
    return max(scores.items(), key=lambda x: x[1])[0]

def show_neuroleader_test_section():
    """Wyświetla sekcję testu neuroleadera w profilu"""
    device_type = get_device_type()
    
    # Sprawdź czy użytkownik ma już zapisane wyniki
    user_data = get_current_user_data(st.session_state.get('username'))
    has_results = user_data.get('neuroleader_type') is not None
    
    # Jeśli użytkownik ma wyniki i nie rozpoczął testu ponownie, pokaż wyniki
    if has_results and 'test_step' not in st.session_state:
        show_current_neuroleader_type()
        return
    
    # Informacja o teście
    if 'show_test_info' not in st.session_state:
        st.session_state.show_test_info = True
    
    if st.session_state.show_test_info:
        st.markdown("""
        ### 🧠 Test typu neuroleadera
        
        Ten test pomoże Ci sprawdzić, **jakim typem neuroleadera** jesteś.
        
        - Każde pytanie ma **6 odpowiedzi** – każda reprezentuje inny styl przywództwa.
        - **Wybierz tę odpowiedź, która najlepiej opisuje Twoje zachowanie lub sposób myślenia.**
        - Po zakończeniu zobaczysz graficzny wynik w postaci wykresu radarowego.
        
        🧩 Gotowy?
        """)
        if zen_button("Rozpocznij test", key="start_neuroleader_test"):
            st.session_state.show_test_info = False
            if 'test_step' not in st.session_state:
                st.session_state.test_step = 0
                st.session_state.test_scores = {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}
            st.rerun()
    
    # Tryb testu    
    elif 'test_step' not in st.session_state:
        st.session_state.test_step = 0
        st.session_state.test_scores = {neuroleader_type: 0 for neuroleader_type in NEUROLEADER_TYPES}
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
                if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", width='stretch'):
                    # Add scores for the answer
                    for neuroleader_type, score in options[i]['scores'].items():
                        st.session_state.test_scores[neuroleader_type] += score
                    
                    st.session_state.test_step += 1
                    st.rerun()
        else:
            # Na tabletach i desktopach użyj dwóch kolumn
            col1, col2 = st.columns(2)
            for i in range(len(options)):
                if i < len(options) // 2:
                    with col1:
                        if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", width='stretch'):
                            # Add scores for the answer
                            for neuroleader_type, score in options[i]['scores'].items():
                                st.session_state.test_scores[neuroleader_type] += score
                            
                            st.session_state.test_step += 1
                            st.rerun()
                else:
                    with col2:
                        if zen_button(f"{options[i]['text']}", key=f"q{st.session_state.test_step}_opt{i}", width='stretch'):
                            # Add scores for the answer
                            for neuroleader_type, score in options[i]['scores'].items():
                                st.session_state.test_scores[neuroleader_type] += score
                            
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
    st.markdown(f"## Twój typ neuroleadera: **{result}**")
    
    if result in NEUROLEADER_TYPES:
        tagline = NEUROLEADER_TYPES[result].get('tagline', 'Unikalny styl przywództwa')
        description = NEUROLEADER_TYPES[result].get('description', 'Opis niedostępny')
        
        st.markdown(f"*{tagline}*")
        st.markdown(description)
        
        # Show radar chart
        st.subheader("Twój profil przywództwa")
        radar_fig = plot_radar_chart(st.session_state.test_scores, device_type=device_type)
        st.pyplot(radar_fig)
        
        # Save results
        if zen_button("Zapisz wyniki", key="save_test_results"):
            users_data = load_user_data()
            if st.session_state.username not in users_data:
                users_data[st.session_state.username] = {}
            
            users_data[st.session_state.username]['neuroleader_type'] = result
            users_data[st.session_state.username]['test_scores'] = st.session_state.test_scores
            users_data[st.session_state.username]['test_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            save_user_data(users_data)
            
            # Add recent activity for neuroleader type discovery
            from data.users_fixed import add_recent_activity
            add_recent_activity(
                st.session_state.username, 
                "neuroleader_type_discovered", 
                {"neuroleader_type": result}
            )
            
            # Przyznaj XP za ukończenie testu Neurolidera
            try:
                from data.users import award_xp_for_activity
                award_xp_for_activity(
                    st.session_state.username,
                    'test_completed',
                    5,  # 5 XP za ukończenie testu Neurolidera
                    {
                        'test_name': 'Neuroleader Type',
                        'result': result
                    }
                )
            except Exception:
                pass
            
            # Check for achievements
            check_achievements(st.session_state.username)
            
            notification("Wyniki testu zostały zapisane!", type="success")
            
            # Reset test state
            for key in ['test_step', 'test_scores', 'show_test_info']:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Przyciski akcji
    col_restart, col_close = st.columns([1, 1])
    
    with col_restart:
        if zen_button("🔄 Wykonaj test ponownie", key="restart_test", width='stretch'):
            for key in ['test_step', 'test_scores', 'show_test_info']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col_close:
        if st.button("❌ Zamknij test", use_container_width=True, key="close_neuroleader_from_results"):
            st.session_state.active_tool = None
            st.rerun()

def show_current_neuroleader_type():
    """Wyświetla informacje o aktualnym typie neurolidera użytkownika"""
    device_type = get_device_type()
    user_data = get_current_user_data(st.session_state.get('username'))
    
    st.markdown("<div class='st-bx'>", unsafe_allow_html=True)
    
    if user_data.get('neuroleader_type'):
        neuroleader_type = user_data['neuroleader_type']
          # Header with neuroleader type
        st.markdown(f"<h2 style='text-align: center;'>{neuroleader_type}</h2>", unsafe_allow_html=True)
        tagline = NEUROLEADER_TYPES.get(neuroleader_type, {}).get("tagline", "Twój unikalny styl przywództwa")
        st.markdown(f"<div style='text-align: center; color: #666; margin-bottom: 20px;'>{tagline}</div>", unsafe_allow_html=True)
        
        if neuroleader_type in NEUROLEADER_TYPES:
            # Description
            with st.expander("📖 Opis", expanded=True):
                description = NEUROLEADER_TYPES[neuroleader_type].get("description", "Opis niedostępny")
                st.markdown(description)
                
            # Radar chart if available
            if 'test_scores' in user_data:
                st.subheader("Twój profil przywódczy")
                
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
                    strengths = NEUROLEADER_TYPES[neuroleader_type].get("strengths", ["Brak danych"])
                    st.markdown("\n".join([f"- ✅ {strength}" for strength in strengths]))
            
            with col2:
                with st.expander("🔍 Wyzwania", expanded=True):
                    challenges = NEUROLEADER_TYPES[neuroleader_type].get("challenges", ["Brak danych"])
                    st.markdown("\n".join([f"- ⚠️ {challenge}" for challenge in challenges]))
            
            # Strategy
            strategy = NEUROLEADER_TYPES[neuroleader_type].get("strategy", "Strategia niedostępna")
            tip_block(
                strategy,
                title="Rekomendowana strategia",
                icon="🎯"
            )
            
            # Detailed description
            if neuroleader_type in neuroleader_details:
                with st.expander("📚 Szczegółowy opis twojego typu neurolidera", expanded=False):
                    st.markdown(neuroleader_details[neuroleader_type])
            else:
                st.warning("Szczegółowy opis dla tego typu neurolidera nie jest jeszcze dostępny.")
                
            # Test info and retake option
            if 'test_date' in user_data:
                st.info(f"📅 Test wykonany: {user_data['test_date']}")
            
            # Przyciski akcji
            col_restart, col_close = st.columns([1, 1])
            
            with col_restart:
                if zen_button("🔄 Wykonaj test ponownie", key="retake_test", width='stretch'):
                    # Reset test state
                    for key in ['test_step', 'test_scores', 'show_test_info']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.session_state.show_test_info = True
                    st.rerun()
            
            with col_close:
                if st.button("❌ Zamknij test", use_container_width=True, key="close_neuroleader_from_type"):
                    st.session_state.active_tool = None
                    st.rerun()
    else:
        notification(
            "Nie określono jeszcze twojego typu neurolidera. Wykonaj test neurolidera w zakładce powyżej, aby odkryć swój unikalny styl przywództwa i dostosowane rekomendacje.",
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
    # Cast to PolarAxes for type checking (ax is PolarAxes when polar=True)
    from typing import cast
    ax = cast(PolarAxes, ax)
    
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
    ax.set_title("Twój profil przywódczy", size=title_size, pad=20)
    
    # Dostosuj siatkę i oś
    ax.grid(True, alpha=grid_alpha)
    
    # Dodaj etykiety z wartościami
    # Dostosuj odległość etykiet od wykresu
    label_pad = max_val * (0.05 if device_type == 'mobile' else 0.1)
    
    # Poprawiona wersja:
    for i, (angle, value) in enumerate(zip(angles_radians, values)):
        color = NEUROLEADER_TYPES[labels[i]].get("color", "#3498db")
        
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


def generate_who_am_i_report_ui(username: str):
    """UI do generowania i wyświetlania raportu 'Kim Jestem?'"""
    from data.users import load_user_data
    from utils.profile_report import (
        collect_user_profile_data, 
        generate_personal_synthesis, 
        generate_recommendations,
        create_kolb_radar_chart,
        create_neuroleader_radar_chart,
        create_mi_radar_chart,
        create_engagement_gauge,
        create_strengths_bars
    )
    from utils.profile_pdf import generate_who_am_i_pdf
    
    # Pobierz dane użytkownika
    users_data = load_user_data()
    if username not in users_data:
        st.error("❌ Nie znaleziono danych użytkownika")
        return
    
    user_data = users_data[username]
    user_data['username'] = username
    
    # Generuj raport
    with st.spinner("🔄 Analizuję Twój profil..."):
        profile_data = collect_user_profile_data(user_data)
    
    # === NAGŁÓWEK RAPORTU ===
    st.success("✅ Raport 'Kim Jestem?' został wygenerowany!")
    
    # Przycisk PDF na górze
    col_left, col_right = st.columns([3, 1])
    with col_right:
        if st.button("📥 Pobierz PDF", type="secondary", use_container_width=True):
            with st.spinner("Generuję PDF..."):
                try:
                    pdf_bytes = generate_who_am_i_pdf(profile_data)
                    st.download_button(
                        label="⬇️ Pobierz PDF",
                        data=pdf_bytes,
                        file_name=f"Kim_Jestem_{username}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Błąd: {str(e)}")
    
    st.markdown("---")
    
    # === TRZY WYKRESY RADAROWE ===
    st.markdown("### 🎯 Twoje Wyniki Diagnostyczne")
    
    # Sprawdź czy są jakiekolwiek testy
    has_any_test = any([
        profile_data['tests']['kolb'],
        profile_data['tests']['neuroleader'],
        profile_data['tests']['mi']
    ])
    
    if has_any_test:
        # Generuj wykresy
        kolb_chart = create_kolb_radar_chart(profile_data)
        neuroleader_chart = create_neuroleader_radar_chart(profile_data)
        mi_chart = create_mi_radar_chart(profile_data)
        
        # Wyświetl w 3 kolumnach
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if kolb_chart:
                st.plotly_chart(kolb_chart, use_container_width=True)
            else:
                st.info("� **Test Kolba**\n\nWykonaj test aby zobaczyć wykres")
        
        with col2:
            if neuroleader_chart:
                st.plotly_chart(neuroleader_chart, use_container_width=True)
            else:
                st.info("� **Neuroleader**\n\nWykonaj test aby zobaczyć wykres")
        
        with col3:
            if mi_chart:
                st.plotly_chart(mi_chart, use_container_width=True)
            else:
                st.info("🧠 **MI Test**\n\nWykonaj test aby zobaczyć wykres")
    else:
        st.info("📊 Wykresy radarowe pojawią się po wykonaniu testów diagnostycznych")
    
    st.markdown("---")
    
    # === GAUGE ZAANGAŻOWANIA + TOP 5 MOCNYCH STRON ===
    col_gauge, col_strengths = st.columns([1, 2])
    
    with col_gauge:
        engagement_gauge = create_engagement_gauge(profile_data)
        st.plotly_chart(engagement_gauge, use_container_width=True)
    
    with col_strengths:
        strengths_bars = create_strengths_bars(profile_data)
        if strengths_bars:
            st.plotly_chart(strengths_bars, use_container_width=True)
        else:
            st.info("💪 **Mocne Strony**\n\nWykonaj testy aby odkryć swoje mocne strony!")
    
    st.markdown("---")
    
    # === SEKCJA 1: SYNTEZA I AKTYWNOŚĆ (2 kolumny) ===
    col_main, col_stats = st.columns([2, 1])
    
    with col_main:
        st.markdown("### 🧭 Kim Jestem?")
        synthesis = generate_personal_synthesis(profile_data)
        st.markdown(synthesis)
    
    with col_stats:
        st.markdown("### 📈 Aktywność")
        activity = profile_data['activity']
        st.metric("Ukończone moduły", len(activity['modules_completed']))
        st.metric("W trakcie", len(activity['modules_in_progress']))
        st.metric("Postęp ogólny", f"{activity['total_progress']}%")
        st.metric("Zaangażowanie", f"{activity['engagement_score']}/100")
    
    st.markdown("---")
    
    # === SEKCJA 2: TESTY (3 kolumny na pełną szerokość) ===
    st.markdown("### 📊 Moje Wyniki Diagnostyczne")
    
    tests = profile_data['tests']
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if tests['kolb']:
            st.markdown("#### 🔄 Test Kolba")
            st.markdown(f"**{tests['kolb']['style']}**")
            with st.expander("📖 Zobacz opis"):
                st.markdown(tests['kolb']['description'])
        else:
            st.markdown("#### 🔄 Test Kolba")
            st.caption("❌ Nie wykonano")
    
    with col2:
        if tests['neuroleader']:
            st.markdown("#### 🧬 Neuroleader")
            st.markdown(f"**{tests['neuroleader']['type']}**")
            with st.expander("📖 Zobacz opis"):
                st.markdown(tests['neuroleader']['description'])
        else:
            st.markdown("#### 🧬 Neuroleader")
            st.caption("❌ Nie wykonano")
    
    with col3:
        if tests['mi']:
            st.markdown("#### 🧠 MI Test")
            from utils.profile_report import get_intelligence_name
            top = tests['mi']['top_3'][0] if tests['mi']['top_3'] else ('unknown', 0)
            st.markdown(f"**{get_intelligence_name(top[0])}**")
            st.caption(f"Wynik: {top[1]:.1f}%")
            if len(tests['mi']['top_3']) > 1:
                with st.expander("📖 Top 3 inteligencje"):
                    for intel, score in tests['mi']['top_3']:
                        st.write(f"• {get_intelligence_name(intel)}: {score:.1f}%")
        else:
            st.markdown("#### 🧠 MI Test")
            st.caption("❌ Nie wykonano")
    
    st.markdown("---")
    
    # === SEKCJA 3: MOCNE STRONY I REKOMENDACJE (2 kolumny) ===
    col_strengths, col_recommendations = st.columns(2)
    
    with col_strengths:
        st.markdown("### 💪 Moje Mocne Strony")
        strengths = profile_data['strengths']
        if strengths:
            for i, strength in enumerate(strengths[:5], 1):  # Top 5
                with st.expander(f"{i}. {strength['icon']} {strength['name']}", expanded=(i==1)):
                    st.markdown(f"**{strength['description']}**")
                    st.caption(f"📌 Źródło: {strength['source']}")
        else:
            st.info("Wykonaj więcej testów aby odkryć swoje mocne strony!")
    
    with col_recommendations:
        st.markdown("### 🚀 Następne Kroki")
        recommendations = generate_recommendations(profile_data)
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                priority_colors = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }
                
                with st.expander(
                    f"{i}. {priority_colors[rec['priority']]} {rec['icon']} {rec['title']}", 
                    expanded=(i==1)
                ):
                    st.markdown(rec['description'])
                    if 'action' in rec:
                        st.caption(f"➡️ {rec['action']}")
