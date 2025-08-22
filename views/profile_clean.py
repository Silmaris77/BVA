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

def clean_html(text):
    """Czyści HTML z tekstu"""
    clean = re.compile('<.*?>')
    normalized_text = re.sub(clean, '', text)
    # Normalizuj białe znaki 
    normalized_text = re.sub(r'\s+', ' ', normalized_text)
    return normalized_text.strip()

def calculate_test_results(scores):
    """Calculate the dominant degen type based on test scores"""
    return max(scores.items(), key=lambda x: x[1])[0]

def show_profile():
    """Główna funkcja profilu z czterema zakładkami"""
    
    # Pobranie danych użytkownika
    user_data = get_current_user_data()
    if not user_data:
        st.error("Nie można załadować danych użytkownika")
        return
    
    device_type = get_device_type()
    
    # Nagłówek profilu
    st.markdown("# 👤 Profil użytkownika")
    
    # Podstawowe informacje o użytkowniku
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"### Witaj, {user_data.get('username', 'Użytkowniku')}! 🎉")
        
        # Avatar
        avatar = user_data.get('avatar', 'default')
        if avatar in USER_AVATARS:
            st.markdown(f"<div style='text-align: center; font-size: 4rem;'>{USER_AVATARS[avatar]}</div>", 
                       unsafe_allow_html=True)
    
    # Zakładki profilu
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Statystyki", 
        "🏆 Odznaki", 
        "🔍 Diagnostyka", 
        "🎒 Ekwipunek"
    ])
    
    with tab1:
        show_profile_stats_section(user_data, device_type)
    
    with tab2:
        show_badges_section(user_data, device_type)
    
    with tab3:
        show_diagnostics_section(user_data)
    
    with tab4:
        show_equipment_section(user_data, device_type)

def show_profile_stats_section(user_data, device_type):
    """Wyświetla sekcję statystyk użytkownika"""
    st.markdown("### 📊 Twoje statystyki")
    
    # Oblicz statystyki
    completed_lessons = user_data.get('completed_lessons', [])
    total_lessons_completed = len(completed_lessons)
    
    degen_coins = user_data.get('degen_coins', 0)
    current_streak = user_data.get('current_streak', 0)
    max_streak = user_data.get('max_streak', 0)
    
    total_quiz_score = user_data.get('total_quiz_score', 0)
    quizzes_completed = user_data.get('quizzes_completed', 0)
    avg_quiz_score = (total_quiz_score / quizzes_completed) if quizzes_completed > 0 else 0
    
    # Progress calculation
    total_lessons = 50  # Założona liczba wszystkich lekcji
    progress_percentage = min((total_lessons_completed / total_lessons) * 100, 100)
    
    # XP system
    total_xp = user_data.get('total_xp', 0)
    level, xp_progress = calculate_xp_progress(total_xp)
    
    # Karty statystyk - responsywne
    if device_type == 'mobile':
        # Na mobile 2 kolumny
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="🎓 Ukończone lekcje",
                value=f"{total_lessons_completed}/{total_lessons}",
                delta=f"{progress_percentage:.1f}%"
            )
            
            st.metric(
                label="🔥 Aktualny streak",
                value=f"{current_streak} dni",
                delta=f"Max: {max_streak}"
            )
        
        with col2:
            st.metric(
                label="💰 DegenCoins",
                value=degen_coins,
                delta="+" + str(user_data.get('coins_earned_today', 0)) + " dziś"
            )
            
            st.metric(
                label="📈 Średni wynik quiz",
                value=f"{avg_quiz_score:.1f}%",
                delta=f"{quizzes_completed} ukończone"
            )
        
        # Druga linia dla mobile
        col3, col4 = st.columns(2)
        
        with col3:
            st.metric(
                label="⭐ Poziom",
                value=f"Level {level}",
                delta=f"{xp_progress:.0f}% do następnego"
            )
        
        with col4:
            st.metric(
                label="🏆 Łączne XP",
                value=total_xp,
                delta="+" + str(user_data.get('xp_earned_today', 0)) + " dziś"
            )
    
    else:
        # Na desktop/tablet 3 kolumny
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="🎓 Ukończone lekcje",
                value=f"{total_lessons_completed}/{total_lessons}",
                delta=f"{progress_percentage:.1f}%"
            )
            
            st.metric(
                label="💰 DegenCoins",
                value=degen_coins,
                delta="+" + str(user_data.get('coins_earned_today', 0)) + " dziś"
            )
        
        with col2:
            st.metric(
                label="🔥 Aktualny streak",
                value=f"{current_streak} dni",
                delta=f"Max: {max_streak}"
            )
            
            st.metric(
                label="📈 Średni wynik quiz",
                value=f"{avg_quiz_score:.1f}%",
                delta=f"{quizzes_completed} ukończone"
            )
        
        with col3:
            st.metric(
                label="⭐ Poziom",
                value=f"Level {level}",
                delta=f"{xp_progress:.0f}% do następnego"
            )
            
            st.metric(
                label="🏆 Łączne XP",
                value=total_xp,
                delta="+" + str(user_data.get('xp_earned_today', 0)) + " dziś"
            )
    
    # Progress bar
    st.markdown("---")
    st.markdown("### 📈 Postęp w kursie")
    progress_bar = st.progress(progress_percentage / 100)
    st.caption(f"Ukończono {total_lessons_completed} z {total_lessons} lekcji ({progress_percentage:.1f}%)")
    
    # Wykres aktywności (przykład)
    if st.checkbox("📊 Pokaż wykres aktywności"):
        # Symulacja danych aktywności z ostatnich 30 dni
        import pandas as pd
        import datetime
        
        dates = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(30)]
        activity = [random.randint(0, 5) for _ in range(30)]  # Symulacja aktywności
        
        df = pd.DataFrame({
            'Data': dates,
            'Aktywność': activity
        })
        
        st.line_chart(df.set_index('Data'))
        st.caption("Wykres pokazuje Twoją aktywność w ciągu ostatnich 30 dni")

def show_badges_section(user_data, device_type):
    """Wyświetla sekcję odznak i osiągnięć"""
    st.markdown("### 🏆 Odznaki i osiągnięcia")
    
    # Sprawdź postęp użytkownika
    user_progress = user_data.get('progress', {})
    user_badges = user_data.get('badges', [])
    
    # Definicja odznak
    available_badges = {
        "🚀 Pierwszy krok": {
            "description": "Ukończ pierwszą lekcję",
            "requirement": "completed_lessons",
            "threshold": 1,
            "category": "Postęp"
        },
        "📚 Pilny uczeń": {
            "description": "Ukończ 5 lekcji",
            "requirement": "completed_lessons", 
            "threshold": 5,
            "category": "Postęp"
        },
        "🎓 Ekspert": {
            "description": "Ukończ 10 lekcji",
            "requirement": "completed_lessons",
            "threshold": 10,
            "category": "Postęp"
        },
        "🧠 Quiz master": {
            "description": "Ukończ 3 quizy",
            "requirement": "completed_quizzes",
            "threshold": 3,
            "category": "Wiedza"
        },
        "💎 Degen wojownik": {
            "description": "Ukończ test degena",
            "requirement": "degen_test_completed",
            "threshold": 1,
            "category": "Osiągnięcia"
        },
        "🔥 Streak mistrz": {
            "description": "7 dni nauki pod rząd",
            "requirement": "max_streak",
            "threshold": 7,
            "category": "Konsekwencja"
        },
        "⭐ Kolekcjoner": {
            "description": "Zdobądź 5 odznak",
            "requirement": "total_badges",
            "threshold": 5,
            "category": "Meta"
        }
    }
    
    # Pokaż odznaki według kategorii
    categories = ["Postęp", "Wiedza", "Osiągnięcia", "Konsekwencja", "Meta"]
    
    for category in categories:
        st.markdown(f"#### 🏷️ {category}")
        
        category_badges = {k: v for k, v in available_badges.items() 
                          if v["category"] == category}
        
        if not category_badges:
            continue
            
        cols = st.columns(2 if device_type == 'mobile' else 3)
        
        for i, (badge_name, badge_info) in enumerate(category_badges.items()):
            with cols[i % (2 if device_type == 'mobile' else 3)]:
                # Sprawdź czy odznaka jest zdobyta
                requirement = badge_info["requirement"]
                threshold = badge_info["threshold"]
                
                # Sprawdź postęp
                if requirement == "total_badges":
                    current_value = len(user_badges)
                elif requirement == "degen_test_completed":
                    current_value = 1 if user_data.get('degen_test_result') else 0
                elif requirement == "completed_lessons":
                    current_value = len(user_data.get('completed_lessons', []))
                elif requirement == "completed_quizzes":
                    current_value = user_data.get('quizzes_completed', 0)
                else:
                    current_value = user_progress.get(requirement, 0)
                
                is_earned = current_value >= threshold
                
                # Style dla odznaki
                if is_earned:
                    badge_style = """
                    background: linear-gradient(135deg, #FFD700, #FFA500);
                    border: 2px solid #FFD700;
                    color: #000;
                    """
                    badge_emoji = "🏆"
                else:
                    badge_style = """
                    background: linear-gradient(135deg, #9E9E9E, #757575);
                    border: 2px solid #9E9E9E;
                    color: #FFFFFF;
                    """
                    badge_emoji = "🔒"
                
                # Wyświetl odznakę
                st.markdown(f"""
                <div style="{badge_style}
                            border-radius: 15px;
                            padding: 15px;
                            text-align: center;
                            margin: 10px 0;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <div style="font-size: 2em; margin-bottom: 10px;">
                        {badge_emoji}
                    </div>
                    <div style="font-weight: bold; margin-bottom: 5px;">
                        {badge_name.split(' ', 1)[1]}
                    </div>
                    <div style="font-size: 0.9em; opacity: 0.8;">
                        {badge_info['description']}
                    </div>
                    <div style="margin-top: 10px; font-size: 0.8em;">
                        Postęp: {current_value}/{threshold}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Dodaj odznakę do listy jeśli została zdobyta ale nie jest zapisana
                if is_earned and badge_name not in user_badges:
                    user_badges.append(badge_name)
                    user_data['badges'] = user_badges
                    save_user_data(user_data)
                    st.success(f"🎉 Zdobyłeś odznakę: {badge_name}!")
        
        st.markdown("---")
    
    # Statystyki odznak
    total_badges = len(available_badges)
    earned_badges = len(user_badges)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏆 Zdobyte odznaki", f"{earned_badges}/{total_badges}")
    with col2:
        completion_rate = (earned_badges / total_badges * 100) if total_badges > 0 else 0
        st.metric("📊 Ukończenie", f"{completion_rate:.1f}%")
    with col3:
        next_badge = total_badges - earned_badges
        st.metric("🎯 Do zdobycia", next_badge)

def show_diagnostics_section(user_data):
    """Wyświetla sekcję diagnostyki profilu użytkownika"""
    st.markdown("### 🔍 Diagnostyka profilu")
    
    # Analiza stylu uczenia
    st.markdown("#### 📊 Analiza stylu uczenia")
    
    completed_lessons = user_data.get('completed_lessons', [])
    quiz_scores = user_data.get('quiz_scores', {})
    
    if len(completed_lessons) > 0:
        # Analiza częstotliwości nauki
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Częstotliwość nauki:**")
            current_streak = user_data.get('current_streak', 0)
            max_streak = user_data.get('max_streak', 0)
            
            if current_streak >= 7:
                st.success("🔥 Bardzo regularna nauka!")
            elif current_streak >= 3:
                st.info("📈 Dobra regularność")
            else:
                st.warning("⚠️ Spróbuj być bardziej regularny")
            
            st.caption(f"Aktualny streak: {current_streak} dni")
            st.caption(f"Najdłuższy streak: {max_streak} dni")
        
        with col2:
            st.markdown("**Wydajność quizów:**")
            total_quiz_score = user_data.get('total_quiz_score', 0)
            quizzes_completed = user_data.get('quizzes_completed', 0)
            
            if quizzes_completed > 0:
                avg_score = total_quiz_score / quizzes_completed
                if avg_score >= 80:
                    st.success("🎯 Świetne wyniki!")
                elif avg_score >= 60:
                    st.info("📚 Dobre zrozumienie")
                else:
                    st.warning("🔄 Warto powtórzyć materiał")
                
                st.caption(f"Średnia: {avg_score:.1f}%")
            else:
                st.info("Brak ukończonych quizów")
    
    else:
        st.info("Ukończ kilka lekcji, aby zobaczyć analizę")
    
    # Rekomendacje
    st.markdown("---")
    st.markdown("#### 💡 Rekomendacje")
    
    recommendations = []
    
    # Rekomendacje na podstawie streaku
    current_streak = user_data.get('current_streak', 0)
    if current_streak == 0:
        recommendations.append("🎯 Zacznij regularną naukę - nawet 10 minut dziennie robi różnicę!")
    elif current_streak < 7:
        recommendations.append("🔥 Kontynuuj streak! Staraj się uczyć codziennie.")
    
    # Rekomendacje na podstawie postępu
    total_lessons_completed = len(completed_lessons)
    if total_lessons_completed < 5:
        recommendations.append("📚 Ukończ więcej lekcji podstawowych, aby zbudować solidne fundamenty.")
    
    # Rekomendacje na podstawie wyników quizów
    if user_data.get('quizzes_completed', 0) > 0:
        avg_quiz_score = user_data.get('total_quiz_score', 0) / user_data.get('quizzes_completed', 1)
        if avg_quiz_score < 70:
            recommendations.append("🔄 Wróć do trudniejszych lekcji i powtórz materiał.")
    
    # Rekomendacje na podstawie typu degena
    if user_data.get('degen_test_result'):
        degen_type = user_data['degen_test_result']
        if degen_type in DEGEN_TYPES:
            degen_info = DEGEN_TYPES[degen_type]
            if 'recommendation' in degen_info:
                recommendations.append(f"🎭 Jako {degen_type}: {degen_info['recommendation']}")
    
    if recommendations:
        for rec in recommendations:
            st.info(rec)
    else:
        st.success("🎉 Świetna robota! Kontynuuj w tym tempie!")
    
    # Cele osobiste
    st.markdown("---")
    st.markdown("#### 🎯 Cele osobiste")
    
    user_goals = user_data.get('goals', [])
    if user_goals:
        for i, goal in enumerate(user_goals):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"📌 {goal.get('title', 'Cel bez nazwy')}")
            with col2:
                progress = goal.get('progress', 0)
                target = goal.get('target', 100)
                st.write(f"{progress}/{target}")
            with col3:
                if st.button("❌", key=f"delete_goal_{i}"):
                    user_goals.remove(goal)
                    user_data['goals'] = user_goals
                    save_user_data(user_data)
                    st.rerun()
    else:
        st.info("Nie masz jeszcze żadnych celów. Dodaj swój pierwszy cel!")
    
    # Dodaj nowy cel
    with st.expander("➕ Dodaj nowy cel"):
        goal_title = st.text_input("Nazwa celu:")
        goal_target = st.number_input("Cel (liczba):", min_value=1, value=10)
        
        if st.button("Dodaj cel"):
            if goal_title:
                new_goal = {
                    'title': goal_title,
                    'target': goal_target,
                    'progress': 0,
                    'created_date': datetime.now().isoformat()
                }
                if 'goals' not in user_data:
                    user_data['goals'] = []
                user_data['goals'].append(new_goal)
                save_user_data(user_data)
                st.success(f"Dodano cel: {goal_title}")
                st.rerun()

def show_equipment_section(user_data, device_type):
    """Wyświetla sekcję ekwipunku"""
    st.markdown("### 🎒 Ekwipunek")
    
    # Sprawdź czy użytkownik ma zapisany ekwipunek
    user_equipment = user_data.get('equipment', {})
    
    # Przykładowy ekwipunek
    equipment = {
        "Główny ekwipunek": {
            "📚 Książka o tradingu": "Zwiększa wiedzę o analizie technicznej",
            "🔍 Lupa analityczna": "Pomaga w badaniu projektów",
            "💎 Diamentowe ręce": "Zwiększa odporność na FUD"
        },
        "Narzędzia badawcze": {
            "📊 Kalkulator zysków": "Oblicza potencjalne zyski/straty",
            "🎯 Radar okazji": "Wykrywa nowe możliwości inwestycyjne",
            "🛡️ Tarcza ryzyka": "Chroni przed złymi decyzjami"
        },
        "Przedmioty specjalne": {
            "🚀 Rakieta na księżyc": "Dla najodważniejszych inwestycji",
            "🔮 Kryształowa kula": "Przepowiada trendy rynkowe",
            "💰 Worek złota": "Zwiększa starting capital"
        }
    }
    
    for category, items in equipment.items():
        with st.expander(f"🎒 {category}", expanded=True):
            for item, description in items.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{item}**")
                    st.caption(description)
                with col2:
                    # Sprawdź czy przedmiot jest posiadany
                    item_key = f"{category}_{item}"
                    owned = user_equipment.get(item_key, False)
                    
                    if st.checkbox("Posiadane", value=owned, key=f"item_{item_key}"):
                        if not owned:  # Tylko jeśli się zmieniło na True
                            user_equipment[item_key] = True
                            user_data['equipment'] = user_equipment
                            save_user_data(user_data)
                            st.success(f"Dodano {item} do ekwipunku!")
                    else:
                        if owned:  # Tylko jeśli się zmieniło na False
                            user_equipment[item_key] = False
                            user_data['equipment'] = user_equipment
                            save_user_data(user_data)
                            st.info(f"Usunięto {item} z ekwipunku")

    # Sekcja statystyk ekwipunku
    st.markdown("---")
    st.markdown("### 📈 Statystyki ekwipunku")
    
    # Policz posiadane przedmioty
    total_items = sum(len(items) for items in equipment.values())
    owned_items = len([k for k, v in user_equipment.items() if v])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="📦 Przedmioty",
            value=f"{owned_items}/{total_items}",
            delta=f"{owned_items} posiadane"
        )
    with col2:
        # Oblicz rzadkość na podstawie ilości przedmiotów
        if owned_items >= 8:
            rarity = "Legendary"
            rarity_emoji = "🌟"
        elif owned_items >= 5:
            rarity = "Epic"
            rarity_emoji = "💜"
        elif owned_items >= 3:
            rarity = "Rare"
            rarity_emoji = "💙"
        else:
            rarity = "Common"
            rarity_emoji = "⚪"
            
        st.metric(
            label="⭐ Rzadkość",
            value=f"{rarity_emoji} {rarity}",
            delta=f"Level {min(owned_items, 10)}"
        )
    with col3:
        # Oblicz bonus na podstawie przedmiotów
        bonus = owned_items * 2  # 2% za każdy przedmiot
        st.metric(
            label="💪 Bonus",
            value=f"+{bonus}%",
            delta=f"+{owned_items*2}% XP"
        )

    # Przewodnik po ekwipunku 
    with st.expander("ℹ️ Jak zdobyć więcej przedmiotów?"):
        st.markdown("""
        ### 🎯 Sposoby zdobywania ekwipunku:
        
        1. **Ukończenie lekcji** - Każda ukończona lekcja daje przedmioty
        2. **Osiągnięcia** - Specjalne nagrody za określone cele
        3. **Quizy** - Prawidłowe odpowiedzi = lepszy ekwipunek
        4. **Streaki** - Regularna nauka zwiększa jakość nagród
        5. **Eventy specjalne** - Ograniczone czasowo przedmioty
        
        ### 💡 Wskazówki:
        - Przedmioty Epic i Legendary mają specjalne bonusy
        - Niektóre kombinacje przedmiotów dają dodatkowe efekty
        - Ekwipunek wpływa na postęp w nauce
        - Im więcej przedmiotów, tym większy bonus XP
        
        ### 🏆 Cele ekwipunku:
        - **3 przedmioty**: Odblokowanie rangi Rare
        - **5 przedmiotów**: Odblokowanie rangi Epic  
        - **8 przedmiotów**: Odblokowanie rangi Legendary
        - **10+ przedmiotów**: Maksymalny bonus i prestiż
        """)

    # Sekcja wyboru awatara
    st.markdown("---")
    st.markdown("### 🎭 Wybór awatara")
    
    # Lista dostępnych awatarów
    avatars = {
        "biker": "👨‍🚀 Biker", 
        "degen-wojak": "🤖 Degen Wojak",
        "hacker": "👨‍💻 Hacker",
        "chad": "💪 Chad",
        "coomer": "😎 Coomer",
        "pepe": "🐸 Pepe"
    }
    
    # Grid z awatarami
    if device_type == 'mobile':
        cols = st.columns(2)
    else:
        cols = st.columns(3)
        
    for i, (avatar_key, avatar_name) in enumerate(avatars.items()):
        with cols[i % (2 if device_type == 'mobile' else 3)]:
            if st.button(avatar_name, key=f"avatar_{avatar_key}", use_container_width=True):
                user_data['avatar'] = avatar_key
                save_user_data(user_data)
                st.rerun()
            
            # Pokaż checkmark jeśli to aktualny awatar
            if user_data.get('avatar') == avatar_key:
                st.markdown("✅ *Aktualny awatar*")
    
    # Informacje o awatarach
    with st.expander("ℹ️ O awatarach"):
        st.markdown("""
        ### 🎭 Wybierz swojego awatara
        
        Awatar to Twoja wizualna reprezentacja w ZenDegen Academy. Każdy awatar ma swoją unikalną 
        osobowość i styl, który może odzwierciedlać Twoje podejście do inwestowania:
        
        - **👨‍🚀 Biker**: Dla odważnych i niezależnych inwestorów
        - **🤖 Degen Wojak**: Klasyczny wybór dla prawdziwych degenów
        - **👨‍💻 Hacker**: Dla technicznych analityków i miłośników blockchain
        - **💪 Chad**: Dla pewnych siebie i zdecydowanych traderów
        - **😎 Coomer**: Dla spokojnych i wyważonych inwestorów
        - **🐸 Pepe**: Dla miłośników memów i kultury crypto
        """)

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
