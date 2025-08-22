# utils/mission_components_fixed.py
"""
Mission UI Components for ZenDegenAcademy - Fixed Version
Simple, stable mission system
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SimpleMissionManager:
    """Simple mission manager with basic functionality"""
    
    def load_lesson_missions(self, lesson_id: str) -> List[Dict]:
        """Load missions for a lesson"""
        return [
            {
                'id': 'market_analysis',
                'title': '📊 Market Analysis',
                'description': 'Analyze current market trends',
                'difficulty': 'medium',
                'xp_reward': 75,
                'duration_days': 1,
                'status': 'available'
            },
            {
                'id': 'portfolio_review', 
                'title': '💼 Portfolio Review',
                'description': 'Review your investment portfolio',
                'difficulty': 'easy',
                'xp_reward': 50,
                'duration_days': 1,
                'status': 'available'
            },
            {
                'id': 'risk_assessment',
                'title': '⚖️ Risk Assessment', 
                'description': 'Assess risk levels for potential investments',
                'difficulty': 'hard',
                'xp_reward': 100,
                'duration_days': 1,
                'status': 'available'
            }
        ]
    
    def get_lesson_mission_summary(self, username: str, lesson_id: str) -> Dict:
        """Get summary of lesson missions"""
        return {
            'total_missions': 3,
            'completed_missions': 1,
            'total_xp': 75,
            'completion_rate': 0.33
        }
    
    def get_available_missions(self, username: str, lesson_id: str) -> List[Dict]:
        """Get available missions for user"""
        return self.load_lesson_missions(lesson_id)

# Create global instance
mission_manager = SimpleMissionManager()

def render_mission_card(mission: Dict, username: str, lesson_id: str):
    """Render a single mission card"""
    with st.container(border=True):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {mission['title']}")
            st.markdown(mission['description'])
            st.markdown(f"**Trudność:** {mission['difficulty']}")
        
        with col2:
            st.markdown(f"**🎯 {mission['xp_reward']} XP**")
            st.markdown(f"**⏱️ {mission['duration_days']} dni**")
            
            if mission['status'] == 'available':
                if st.button("🚀 Rozpocznij", key=f"start_{mission['id']}"):
                    st.success(f"Misja {mission['title']} rozpoczęta!")
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
        st.info("System misji jest tymczasowo niedostępny.")

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
                        st.success(f"Misja {mission['title']} ukończona!")
                        st.rerun()
                else:
                    st.markdown(f"**+{mission['xp']} XP**")
