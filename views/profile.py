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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Statystyki", "🎒 Ekwipunek", "🏆 Odznaki", "💰 Historia XP", "📈 Raporty"])
    
    # Tab 1: Statistics - podobnie jak w Dashboard
    with tab1:
        scroll_to_top()
        show_profile_stats_section(user_data, device_type)
    
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
    # Tab 3: Badges
    with tab3:
        scroll_to_top()
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        # Use Step 5 badge display system
        show_badges_section()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Tab 4: XP History
    with tab4:
        scroll_to_top()
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        show_xp_history_section()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Tab 5: Reports
    with tab5:
        scroll_to_top()
        st.markdown("<div class='profile-tab-content'>", unsafe_allow_html=True)
        show_reports_section()
        st.markdown("</div>", unsafe_allow_html=True)

def show_xp_history_section():
    """Wyświetla szczegółową historię zdobywania XP"""
    from utils.activity_tracker import get_xp_history
    from data.users import load_user_data
    
    zen_header("💰 Historia Zdobywania XP")
    
    username = st.session_state.username
    users_data = load_user_data()
    user_data = users_data.get(username, {})
    
    # Podsumowanie na górze
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Całkowite XP",
            user_data.get('xp', 0),
            help="Suma wszystkich zdobytych punktów doświadczenia"
        )
    with col2:
        st.metric(
            "Poziom",
            user_data.get('level', 1),
            help="Twój obecny poziom"
        )
    with col3:
        # Oblicz postęp do następnego poziomu
        current_xp = user_data.get('xp', 0)
        current_level = user_data.get('level', 1)
        next_level_xp = current_level * 100  # Uproszczony wzór
        progress = min(100, (current_xp % next_level_xp) / next_level_xp * 100)
        st.metric(
            "Postęp",
            f"{int(progress)}%",
            help=f"Do następnego poziomu: {next_level_xp - (current_xp % next_level_xp)} XP"
        )
    
    st.markdown("---")
    
    # Filtry
    st.markdown("### 🔍 Filtry")
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
    
    # Mapuj okres na dni
    period_days = {
        "Ostatnie 7 dni": 7,
        "Ostatnie 30 dni": 30,
        "Ostatnie 90 dni": 90,
        "Wszystko": 365
    }
    days = period_days[period]
    
    # Pobierz activity_log
    activity_log = user_data.get('activity_log', [])
    
    # Filtruj po dacie
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    
    filtered_activities = []
    for entry in activity_log:
        try:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            if timestamp >= cutoff_date:
                # Filtruj po typie aktywności
                if activity_types[filter_type] is None or entry['type'] in activity_types[filter_type]:
                    # Sprawdź czy ma XP (albo z details, albo domyślne)
                    xp_earned = entry.get('details', {}).get('xp_earned', 0)
                    if xp_earned > 0 or entry['type'] in ['lesson_started', 'lesson_completed', 'quiz_completed', 
                                                            'inspiration_read', 'tool_used', 'ai_exercise', 'test_completed']:
                        filtered_activities.append(entry)
        except:
            continue
    
    # Statystyki przefiltrowanych danych
    st.markdown("---")
    st.markdown(f"### 📊 Statystyki: {period}")
    
    # Oblicz statystyki
    total_xp_period = 0
    activity_breakdown = {}
    
    for entry in filtered_activities:
        # Pobierz XP z details lub użyj domyślnych wartości
        details = entry.get('details', {})
        xp = details.get('xp_earned', 0)
        
        # Fallback dla starych wpisów bez xp_earned
        if xp == 0:
            xp_mapping = {
                'lesson_started': 5,
                'lesson_completed': 50,
                'quiz_completed': 20,
                'ai_exercise': 15,
                'inspiration_read': 1,
                'test_completed': 5,
                'tool_used': 1
            }
            xp = xp_mapping.get(entry['type'], 0)
        
        total_xp_period += xp
        
        # Grupuj po typie
        activity_type = entry['type']
        if activity_type not in activity_breakdown:
            activity_breakdown[activity_type] = {'count': 0, 'xp': 0}
        activity_breakdown[activity_type]['count'] += 1
        activity_breakdown[activity_type]['xp'] += xp
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Zdobyte XP", f"{total_xp_period} XP")
    with col_stat2:
        st.metric("Liczba aktywności", len(filtered_activities))
    with col_stat3:
        avg_xp = total_xp_period / len(filtered_activities) if filtered_activities else 0
        st.metric("Średnio na aktywność", f"{avg_xp:.1f} XP")
    
    # Wykres breakdown po typach
    if activity_breakdown:
        st.markdown("### 📈 Rozkład XP według typu aktywności")
        
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
        
        # Przygotuj dane do wyświetlenia
        breakdown_data = []
        for act_type, stats in activity_breakdown.items():
            breakdown_data.append({
                'Typ': type_names.get(act_type, act_type),
                'Liczba': stats['count'],
                'XP': stats['xp'],
                'Średnio': f"{stats['xp'] / stats['count']:.1f}"
            })
        
        # Sortuj po XP
        breakdown_data.sort(key=lambda x: x['XP'], reverse=True)
        
        # Wyświetl jako DataFrame
        import pandas as pd
        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Szczegółowa tabela aktywności
    st.markdown("### 📜 Szczegółowa Historia")
    
    if not filtered_activities:
        st.info(f"Brak aktywności w wybranym okresie ({period}).")
    else:
        # Przygotuj dane do tabeli
        table_data = []
        
        for entry in sorted(filtered_activities, key=lambda x: x['timestamp'], reverse=True):
            timestamp = datetime.fromisoformat(entry['timestamp'])
            activity_type = entry['type']
            details = entry.get('details', {})
            
            # Pobierz XP
            xp = details.get('xp_earned', 0)
            if xp == 0:
                xp_mapping = {
                    'lesson_started': 5,
                    'lesson_completed': 50,
                    'quiz_completed': 20,
                    'ai_exercise': 15,
                    'inspiration_read': 1,
                    'test_completed': 5,
                    'tool_used': 1
                }
                xp = xp_mapping.get(activity_type, 0)
            
            # Nazwa aktywności
            type_names = {
                'lesson_started': '📖 Rozpoczęcie lekcji',
                'lesson_completed': '✅ Ukończenie lekcji',
                'quiz_completed': '📝 Quiz',
                'inspiration_read': '💡 Przeczytanie inspiracji',
                'tool_used': '🛠️ Użycie narzędzia',
                'ai_exercise': '🤖 Ćwiczenie AI',
                'test_completed': '🎯 Test diagnostyczny'
            }
            activity_name = type_names.get(activity_type, activity_type)
            
            # Dodatkowe szczegóły
            extra_info = ""
            if activity_type == 'quiz_completed':
                score = details.get('score_percentage', 0)
                extra_info = f"Wynik: {score}%"
            elif activity_type == 'test_completed':
                test_name = details.get('test_name', '')
                extra_info = f"{test_name}"
            elif activity_type == 'tool_used':
                tool_name = details.get('tool_name', '')
                extra_info = f"{tool_name}"
            elif activity_type == 'ai_exercise':
                exercise_name = details.get('exercise_name', '')
                extra_info = f"{exercise_name}"
            elif activity_type == 'inspiration_read':
                insp_id = details.get('inspiration_id', '')
                extra_info = f"ID: {insp_id}"
            
            table_data.append({
                'Data': timestamp.strftime('%Y-%m-%d %H:%M'),
                'Aktywność': activity_name,
                'Szczegóły': extra_info,
                'XP': f"+{xp}"
            })
        
        # Wyświetl jako DataFrame z paginacją
        import pandas as pd
        df = pd.DataFrame(table_data)
        
        # Dodaj paginację
        items_per_page = 20
        total_pages = (len(table_data) - 1) // items_per_page + 1
        
        if total_pages > 1:
            page = st.selectbox("Strona", range(1, total_pages + 1), key="xp_history_page")
            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            df_page = df.iloc[start_idx:end_idx]
        else:
            df_page = df
        
        st.dataframe(df_page, use_container_width=True, hide_index=True)
        
        # Statystyka na końcu
        st.caption(f"Wyświetlono {len(df_page)} z {len(table_data)} aktywności")

def show_reports_section():
    """Wyświetla sekcję raportów rozwojowych użytkownika"""
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
    
    st.header("📈 Twoje Raporty Rozwojowe")
    
    username = st.session_state.username
    
    # Inicjalizuj tracking jeśli nie istnieje
    initialize_activity_tracking(username)
    
    # Sprawdź czy powinien zostać wygenerowany automatyczny raport
    auto_report_due = should_generate_auto_report(username)
    
    if auto_report_due:
        st.info("📅 **Automatyczny raport tygodniowy** jest gotowy do wygenerowania! Kliknij przycisk poniżej.")
    
    # Przyciski akcji
    col1, col2 = st.columns([2, 1])
    
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
                label="💾 Pobierz JSON",
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
    """Wyświetla szczegółowy raport"""
    
    # Nagłówek
    st.markdown(f"### {report.get('summary_headline', 'Raport tygodniowy')}")
    
    period_start = datetime.fromisoformat(report['period_start']).strftime('%d.%m.%Y')
    period_end = datetime.fromisoformat(report['period_end']).strftime('%d.%m.%Y')
    st.caption(f"Okres: {period_start} - {period_end}")
    
    # Engagement score
    score = report.get('engagement_score', 0)
    trend = report.get('engagement_trend', 'stabilny')
    
    trend_emoji = {
        'rosnący': '📈',
        'stabilny': '➡️',
        'spadający': '📉'
    }
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(
            "Zaangażowanie",
            f"{score}/10",
            f"{trend_emoji.get(trend, '➡️')} {trend}"
        )
    with col2:
        # Progress bar
        progress_html = f"""
        <div style="background: #e0e0e0; border-radius: 10px; height: 25px; margin-top: 10px;">
            <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                        width: {score * 10}%; 
                        height: 100%; 
                        border-radius: 10px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-weight: bold;">
                {score}/10
            </div>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Wykres przyrostu XP
    st.markdown("### 📈 Przyrost XP w ostatnich 30 dniach")
    display_xp_chart(st.session_state.username)
    
    st.markdown("---")
    
    # Mocne strony
    st.markdown("### 💪 Twoje mocne strony")
    strengths = report.get('strengths', [])
    if strengths:
        for strength in strengths:
            st.success(f"✓ {strength}")
    else:
        st.info("Brak danych")
    
    # Obszary do poprawy
    st.markdown("### 🎓 Obszary do poprawy")
    concerns = report.get('concerns', [])
    if concerns:
        for concern in concerns:
            st.warning(f"→ {concern}")
    else:
        st.info("Świetnie! Nie wykryto istotnych obszarów do poprawy.")
    
    # Insights
    insights = report.get('insights', [])
    if insights:
        st.markdown("### 🔍 Wykryte wzorce")
        for insight in insights:
            st.info(f"💡 {insight}")
    
    # Rekomendacje
    st.markdown("### 🎯 Twój plan działania na następny tydzień")
    recommendations = report.get('recommendations', [])
    
    if recommendations:
        priority_colors = {
            'wysoki': '🔴',
            'średni': '🟡',
            'niski': '🟢'
        }
        
        for i, rec in enumerate(recommendations, 1):
            priority = rec.get('priority', 'średni')
            action = rec.get('action', '')
            why = rec.get('why', '')
            time = rec.get('estimated_time', '')
            
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0; 
                        border-left: 4px solid {'#e74c3c' if priority == 'wysoki' else '#f39c12' if priority == 'średni' else '#27ae60'};">
                <div style="font-weight: bold; margin-bottom: 5px;">
                    {priority_colors.get(priority, '🟡')} {i}. {action}
                </div>
                <div style="font-size: 0.9em; color: #7f8c8d; margin-bottom: 3px;">
                    <strong>Dlaczego:</strong> {why}
                </div>
                <div style="font-size: 0.85em; color: #95a5a6;">
                    ⏱️ Szacowany czas: {time}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Brak rekomendacji")
    
    # Wiadomość motywacyjna
    motivational_message = report.get('motivational_message', '')
    if motivational_message:
        st.markdown("---")
        st.markdown("### 💬 Wiadomość dla Ciebie")
        st.success(motivational_message)

def display_report_compact(report: Dict):
    """Wyświetla skróconą wersję raportu"""
    
    # Podstawowe info
    score = report.get('engagement_score', 0)
    trend = report.get('engagement_trend', 'stabilny')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Zaangażowanie", f"{score}/10")
    with col2:
        st.metric("Trend", trend)
    with col3:
        recommendations_count = len(report.get('recommendations', []))
        st.metric("Rekomendacje", recommendations_count)
    
    # Najważniejsza rekomendacja
    recommendations = report.get('recommendations', [])
    if recommendations:
        high_priority = [r for r in recommendations if r.get('priority') == 'wysoki']
        if high_priority:
            st.info(f"🎯 Priorytet: {high_priority[0].get('action', '')}")

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
