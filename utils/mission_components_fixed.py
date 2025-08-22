# utils/mission_components_fixed.py
"""
Mission UI Components for ZenDegenAcademy - Fixed Version
Components for displaying and interacting with lesson missions
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Simple fallback functions
def get_daily_missions_status():
    """Get status of daily missions"""
    return {
        'completed': 2,
        'total': 3,
        'missions': [
            {'id': 'market_check', 'title': 'Market Check', 'completed': True, 'xp': 75},
            {'id': 'portfolio_review', 'title': 'Portfolio Review', 'completed': True, 'xp': 50},
            {'id': 'risk_analysis', 'title': 'Risk Analysis', 'completed': False, 'xp': 100}
        ],
        'progress': 0.67
    }

def complete_mission_simple(mission_id: str) -> bool:
    """Simple mission completion"""
    st.success(f"Misja {mission_id} ukończona!")
    return True

def render_missions_widget():
    """Render missions widget"""
    st.markdown("### 🎯 Misje Dnia")
    
    status = get_daily_missions_status()
    missions = status['missions']
    
    for mission in missions:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                icon = "✅" if mission['completed'] else "🔄"
                st.markdown(f"{icon} **{mission['title']}**")
            with col2:
                if not mission['completed']:
                    if st.button("START", key=f"start_{mission['id']}"):
                        complete_mission_simple(mission['id'])
                        st.rerun()
                else:
                    st.markdown(f"**+{mission['xp']} XP**")

class MissionManagerFixed:
    """Fixed mission manager with proper structure"""
    
    def load_lesson_missions(self, lesson_id: str) -> Dict:
        """Load missions for a lesson"""
        missions_list = [
            {
                'id': 'market_analysis',
                'title': '📊 Market Analysis',
                'description': 'Analyze current market trends',
                'difficulty': 'medium',
                'xp_reward': 75,
                'duration_days': 1,
                'status': 'available',
                'validation': {
                    'type': 'self_report',
                    'daily_checklist': {
                        'day_1': ['Sprawdź główne indeksy', 'Przeanalizuj 3 spółki']
                    }
                }
            },
            {
                'id': 'portfolio_review', 
                'title': '💼 Portfolio Review',
                'description': 'Review your investment portfolio',
                'difficulty': 'easy',
                'xp_reward': 50,
                'duration_days': 1,
                'status': 'available',
                'validation': {
                    'type': 'self_report',
                    'daily_checklist': {
                        'day_1': ['Oceń każdą pozycję', 'Sprawdź dywersyfikację']
                    }
                }
            },
            {
                'id': 'risk_assessment',
                'title': '⚖️ Risk Assessment', 
                'description': 'Assess risk levels for potential investments',
                'difficulty': 'hard',
                'xp_reward': 100,
                'duration_days': 1,
                'status': 'available',
                'validation': {
                    'type': 'self_report',
                    'daily_checklist': {
                        'day_1': ['Oblicz VaR', 'Sprawdź korelacje', 'Oceń ekspozycję']
                    }
                }
            }
        ]
        
        return {
            'missions': missions_list,
            'lesson_id': lesson_id,
            'total_missions': len(missions_list)
        }
    
    def get_lesson_mission_summary(self, username: str, lesson_id: str) -> Dict:
        """Get summary of lesson missions"""
        return {
            'total_missions': 3,
            'completed_missions': 1,
            'total_xp': 75,
            'completion_rate': 0.33
        }
    
    def initialize_mission_progress(self, username: str, lesson_id: str, mission_id: str) -> bool:
        """Initialize mission progress"""
        return True
    
    def get_daily_mission_info(self, username: str, lesson_id: str, mission_id: str) -> Dict:
        """Get daily mission info"""
        return {
            'mission_title': 'Market Analysis',
            'current_day': 1,
            'total_days': 1,
            'completed_today': False,
            'can_do_today': True,
            'next_available': datetime.now(),
            'is_completed': False,
            'day_info': {
                'title': 'Analiza rynku',
                'description': 'Sprawdź aktualne trendy rynkowe',
                'tasks': ['Sprawdź główne indeksy', 'Przeanalizuj 3 spółki'],
                'target': 'Zrozumienie aktualnej sytuacji rynkowej',
                'tips': ['Użyj wykresów dziennych', 'Sprawdź wolumen transakcji']
            }
        }
    
    def update_daily_progress(self, username: str, lesson_id: str, mission_id: str, day: int, points: int) -> bool:
        """Update daily progress"""
        return True
    
    def get_available_missions(self, username: str, lesson_id: str) -> List:
        """Get available missions"""
        mission_data = self.load_lesson_missions(lesson_id)
        return mission_data.get('missions', [])

# Create global mission manager instance
mission_manager = MissionManagerFixed()

def render_mission_card(mission: Dict, username: str, lesson_id: str):
    """Render a mission card with progress and actions"""
    mission_id = mission['id']
    title = mission['title']
    description = mission['description']
    difficulty = mission.get('difficulty', 'medium')
    xp_reward = mission.get('xp_reward', 0)
    duration_days = mission.get('duration_days', 1)
    status = mission.get('status', 'available')
    progress = mission.get('progress', {})
    
    # Difficulty colors
    difficulty_colors = {
        'easy': '#27ae60',
        'medium': '#f39c12',
        'hard': '#e74c3c'
    }
    
    difficulty_color = difficulty_colors.get(difficulty, '#3498db')
    
    # Status icons
    status_icons = {
        'available': '⭕',
        'active': '🔄', 
        'completed': '✅',
        'locked': '🔒'
    }
    
    status_icon = status_icons.get(status, '⭕')
    
    with st.container(border=True):
        # Header row
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"### {status_icon} {title}")
            st.markdown(f"*{description}*")
            st.markdown(f"**Trudność:** <span style='color: {difficulty_color}'>{difficulty.title()}</span>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**🎯 {xp_reward} XP**")
            st.markdown(f"**⏱️ {duration_days} dni**")
        
        with col3:
            if status == 'available':
                if st.button(f"🚀 Rozpocznij", key=f"start_{mission_id}"):
                    mission_manager.initialize_mission_progress(username, lesson_id, mission_id)
                    st.success(f"Misja {title} została rozpoczęta!")
                    st.rerun()
            elif status == 'active':
                if st.button(f"📋 Dzisiejsze zadanie", key=f"today_{mission_id}"):
                    st.session_state.active_mission = mission_id
                    st.session_state.show_daily_mission = True
            elif status == 'completed':
                st.success("✅ Ukończono!")

def render_daily_mission_interface(username: str, lesson_id: str, mission_id: str):
    """Render the daily mission interface"""
    daily_info = mission_manager.get_daily_mission_info(username, lesson_id, mission_id)
    
    current_day = daily_info['current_day']
    total_days = daily_info['total_days']
    day_info = daily_info['day_info']
    mission_title = daily_info['mission_title']
    is_completed = daily_info['is_completed']
    
    if is_completed:
        st.success("🎉 Ta misja została już ukończona!")
        return
    
    # Header
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
    ">
        <h2 style="margin: 0; font-size: 1.5em;">{mission_title}</h2>
        <h3 style="margin: 10px 0 0 0; font-size: 1.2em;">{day_info['title']}</h3>
        <p style="margin: 5px 0 0 0; font-size: 0.9em; opacity: 0.9;">Dzień {current_day} z {total_days}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress_pct = (current_day - 1) / total_days
    st.progress(progress_pct)
    
    # Day description
    st.markdown("**Opis zadania:**")
    st.markdown(day_info['description'])
    
    # Tasks
    st.markdown("**Zadania do wykonania:**")
    tasks = day_info.get('tasks', [])
    for i, task in enumerate(tasks, 1):
        st.markdown(f"{i}. {task}")
    
    # Target
    if 'target' in day_info:
        st.info(f"🎯 **Cel dnia:** {day_info['target']}")
    
    # Tips
    if 'tips' in day_info:
        with st.expander("💡 Wskazówki"):
            for tip in day_info['tips']:
                st.markdown(f"• {tip}")
    
    # Validation interface
    st.markdown("---")
    st.markdown("### ✅ Potwierdzenie wykonania")
    
    # Simple task completion
    completed_tasks = []
    for i, task in enumerate(tasks):
        if st.checkbox(f"Wykonałem: {task}", key=f"task_{mission_id}_{i}"):
            completed_tasks.append(i)
    
    # Completion button
    if len(completed_tasks) == len(tasks):
        if st.button("🎉 Ukończ dzisiejsze zadanie", key=f"complete_{mission_id}"):
            success = mission_manager.update_daily_progress(username, lesson_id, mission_id, current_day, len(tasks))
            if success:
                st.success("🎊 Gratulacje! Dzisiejsze zadanie ukończone!")
                st.session_state.show_daily_mission = False
                st.rerun()
    else:
        st.info("Zaznacz wszystkie zadania, aby ukończyć dzisiejsze wyzwanie.")
    
    # Back button
    if st.button("⬅️ Powrót do listy misji", key=f"back_{mission_id}"):
        st.session_state.show_daily_mission = False
        st.rerun()

def render_missions_page():
    """Render the main missions page"""
    st.title("🎯 Misje Praktyczne")
    st.markdown("*Zastosuj wiedzę w rzeczywistych wyzwaniach*")
    
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        st.warning("⚠️ Musisz być zalogowany, aby uzyskać dostęp do misji.")
        return
    
    username = st.session_state.get('username', 'default_user')
    lesson_id = st.session_state.get('current_lesson', 'B1C1L1')
    
    # Check if showing daily mission interface
    if st.session_state.get('show_daily_mission') and st.session_state.get('active_mission'):
        render_daily_mission_interface(username, lesson_id, st.session_state.active_mission)
        return
    
    # Mission summary
    summary = mission_manager.get_lesson_mission_summary(username, lesson_id)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Wszystkie misje", summary['total_missions'])
    with col2:
        st.metric("Ukończone", summary['completed_missions'])
    with col3:
        st.metric("Zdobyte XP", summary['total_xp'])
    with col4:
        completion_rate = int(summary['completion_rate'] * 100)
        st.metric("Postęp", f"{completion_rate}%")
    
    st.markdown("---")
    
    # Load and display missions
    try:
        missions = mission_manager.get_available_missions(username, lesson_id)
        
        if missions:
            st.markdown("### 📋 Dostępne Misje")
            for mission in missions:
                render_mission_card(mission, username, lesson_id)
        else:
            st.info("🎯 Brak dostępnych misji dla tej lekcji.")
            
    except Exception as e:
        st.error(f"Błąd ładowania misji: {e}")
        st.info("Używam przykładowych misji...")
        
        # Fallback missions
        example_missions = [
            {
                'id': 'example_1',
                'title': '📊 Analiza Rynku',
                'description': 'Przeanalizuj aktualne trendy rynkowe',
                'difficulty': 'medium',
                'xp_reward': 75,
                'duration_days': 1,
                'status': 'available'
            }
        ]
        
        for mission in example_missions:
            render_mission_card(mission, username, lesson_id)
