"""
Mission UI Components for BrainVenture Academy
Components for displaying and interacting with lesson missions
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, List

# Simple Mission Manager (embedded to avoid import issues)
class SimpleMissionManager:
    """Simple mission manager with basic functionality"""
    
    def load_lesson_missions(self, lesson_id: str) -> Dict:
        """Load missions for a lesson"""
        return {
            'missions': [
                {
                    'id': f'{lesson_id}_mission_1',
                    'title': 'Autorefleksja',
                    'description': 'Przemyśl materiał lekcji',
                    'difficulty': 'Łatwy',
                    'estimated_time': '10 min',
                    'xp_reward': 25,
                    'validation': {
                        'type': 'self_report',
                        'daily_checklist': {
                            'day_1': ['Przeczytaj materiał', 'Zastanów się nad kluczowymi punktami']
                        }
                    }
                },
                {
                    'id': f'{lesson_id}_mission_2', 
                    'title': 'Analiza praktyczna',
                    'description': 'Zastosuj wiedzę w praktyce',
                    'difficulty': 'Średni',
                    'estimated_time': '20 min',
                    'xp_reward': 50,
                    'validation': {
                        'type': 'self_report',
                        'daily_checklist': {
                            'day_1': ['Wykonaj ćwiczenie praktyczne', 'Napisz krótkie podsumowanie']
                        }
                    }
                }
            ]
        }
    def get_lesson_mission_summary(self, username: str, lesson_id: str) -> Dict:
        """Get mission summary for lesson"""
        return {
            'completed_missions': 1,
            'total_missions': 3,
            'total_xp': 75,
            'total_xp_earned': 25,
            'completion_rate': 0.33,
            'completion_percentage': 33.3
        }
    
    def get_available_missions(self, username: str, lesson_id: str) -> List[Dict]:
        """Get available missions for user"""
        mission_data = self.load_lesson_missions(lesson_id)
        return mission_data.get('missions', [])
    
    def initialize_mission_progress(self, username: str, lesson_id: str, mission_id: str):
        """Initialize mission progress"""
        return True
    
    def get_daily_mission_info(self, username: str, lesson_id: str, mission_id: str) -> Dict:
        """Get daily mission info"""
        return {
            'status': 'available',
            'progress': 0,
            'completed_today': False
        }
    
    def update_daily_progress(self, username: str, lesson_id: str, mission_id: str, progress: Dict) -> bool:
        """Update daily progress"""
        return True

# Create global instance
mission_manager = SimpleMissionManager()


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
        'easy': '#27AE60',
        'medium': '#F39C12',
        'hard': '#E74C3C',
        'expert': '#8E44AD'
    }
    
    # Status colors
    status_colors = {
        'available': '#BDC3C7',
        'active': '#3498DB',
        'completed': '#27AE60'
    }
    
    # Create card
    with st.container():
        st.markdown(f"""
        <div style="
            border: 2px solid {status_colors.get(status, '#BDC3C7')};
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #2C3E50; font-size: 1.2em;">{title}</h3>
                <div style="display: flex; gap: 8px;">
                    <span style="
                        background: {difficulty_colors.get(difficulty, '#BDC3C7')};
                        color: white;
                        padding: 4px 8px;
                        border-radius: 12px;
                        font-size: 0.8em;
                        font-weight: bold;
                    ">{difficulty.upper()}</span>
                    <span style="
                        background: #E74C3C;
                        color: white;
                        padding: 4px 8px;
                        border-radius: 12px;
                        font-size: 0.8em;
                    ">{xp_reward} XP</span>
                </div>
            </div>
            <p style="color: #7F8C8D; margin-bottom: 15px; line-height: 1.5;">{description}</p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #95A5A6; font-size: 0.9em;">📅 {duration_days} dni</span>
                <span style="
                    background: {status_colors.get(status, '#BDC3C7')};
                    color: white;
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 0.9em;
                    font-weight: bold;
                ">{status.upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if status == 'available':
                if st.button(f"🚀 Rozpocznij", key=f"start_{mission_id}"):
                    mission_manager.initialize_mission_progress(username, lesson_id, mission_id)
                    st.success(f"Misja {title} została rozpoczęta!")
                    st.rerun()
        
        with col2:
            if status == 'active':
                if st.button(f"📋 Dzisiejsze zadanie", key=f"today_{mission_id}"):
                    st.session_state.active_mission = mission_id
                    st.session_state.show_daily_mission = True
        
        with col3:
            if status == 'completed':
                st.success("✅ Ukończono!")
            elif status == 'active':
                # Show progress
                current_day = progress.get('current_day', 1)
                total_days = duration_days
                progress_pct = (current_day - 1) / total_days * 100
                st.progress(progress_pct / 100)
                st.caption(f"Dzień {current_day}/{total_days}")


def render_daily_mission_interface(username: str, lesson_id: str, mission_id: str):
    """Render interface for today's mission tasks"""
    daily_info = mission_manager.get_daily_mission_info(username, lesson_id, mission_id)
    
    if not daily_info:
        st.error("Nie można załadować informacji o dzisiejszej misji.")
        return
    
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
    st.markdown(f"**Opis zadania:**")
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
    
    # Task completion interface
    st.markdown("---")
    st.markdown("### 📝 Zapisz swój postęp")
    
    # Get mission data for validation
    mission_data = mission_manager.load_lesson_missions(lesson_id)
    validation_type = None
    daily_checklist = []
    
    if mission_data:
        for mission in mission_data['missions']:
            if mission['id'] == mission_id:
                validation = mission.get('validation', {})
                validation_type = validation.get('type')
                if validation_type == 'self_report':
                    daily_checklist = validation.get('daily_checklist', {}).get(f'day_{current_day}', [])
                break
    
    # Render appropriate interface based on validation type
    task_data = {}
    
    if validation_type == 'self_report' and daily_checklist:
        st.markdown("**Zaznacz wykonane zadania:**")
        completed_tasks = []
        
        for i, task in enumerate(daily_checklist):
            if st.checkbox(task, key=f"task_{mission_id}_{current_day}_{i}"):
                completed_tasks.append(task)
        
        task_data['completed_checklist'] = completed_tasks
        
        # Additional notes
        notes = st.text_area(
            "Dodatkowe notatki (opcjonalne):",
            placeholder="Opisz swoje doświadczenia, wnioski, trudności...",
            key=f"notes_{mission_id}_{current_day}"
        )
        if notes:
            task_data['notes'] = notes
    
    else:
        # Generic progress interface
        st.markdown("**Opisz swój postęp:**")
        progress_notes = st.text_area(
            "Co udało Ci się dziś zrobić?",
            placeholder="Opisz swoje działania i doświadczenia...",
            key=f"progress_{mission_id}_{current_day}"
        )
        if progress_notes:
            task_data['progress_notes'] = progress_notes
        
        # Rating
        satisfaction = st.slider(
            "Jak oceniasz swój dzisiejszy postęp? (1-10)",
            1, 10, 5,
            key=f"satisfaction_{mission_id}_{current_day}"
        )
        task_data['satisfaction_rating'] = satisfaction
    
    # Submit button
    if st.button("💾 Zapisz postęp dnia", key=f"submit_{mission_id}_{current_day}"):
        if task_data:
            success = mission_manager.update_daily_progress(
                username, lesson_id, mission_id, current_day, task_data
            )
            
            if success:
                st.success("🎉 Postęp zapisany! Świetna robota!")
                
                # Check if mission is completed
                updated_info = mission_manager.get_daily_mission_info(username, lesson_id, mission_id)
                if updated_info.get('is_completed'):
                    st.balloons()
                    st.success(f"🏆 Gratulacje! Ukończyłeś misję: {mission_title}!")
                
                st.rerun()
            else:
                st.error("Wystąpił błąd podczas zapisywania postępu.")
        else:
            st.warning("Wprowadź jakieś dane przed zapisaniem postępu.")


def render_mission_summary_widget(username: str, lesson_id: str):
    """Render mission summary widget for dashboard"""
    summary = mission_manager.get_lesson_mission_summary(username, lesson_id)
    
    if summary['total_missions'] == 0:
        return
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
    ">
        <h4 style="margin: 0 0 15px 0; display: flex; align-items: center;">
            🎯 Misje praktyczne: Strach przed stratą
        </h4>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
            <div style="text-align: center;">
                <div style="font-size: 2em; font-weight: bold; margin-bottom: 5px;">
                    {summary['completed_missions']}/{summary['total_missions']}
                </div>
                <div style="font-size: 0.9em; opacity: 0.9;">Ukończone misje</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2em; font-weight: bold; margin-bottom: 5px;">
                    {summary['total_xp_earned']} XP
                </div>
                <div style="font-size: 0.9em; opacity: 0.9;">Zdobyte punkty</div>
            </div>
        </div>
        <div style="margin-top: 15px;">
            <div style="background: rgba(255,255,255,0.2); border-radius: 10px; height: 8px; overflow: hidden;">
                <div style="
                    background: white;
                    height: 100%;
                    width: {summary['completion_percentage']:.1f}%;
                    transition: width 0.3s ease;
                "></div>
            </div>
            <div style="text-align: center; margin-top: 8px; font-size: 0.9em; opacity: 0.9;">
                {summary['completion_percentage']:.1f}% postępu
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show active missions and navigation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if summary['active_missions'] > 0:
            missions = mission_manager.get_available_missions(username, lesson_id)
            active_missions = [m for m in missions if m.get('status') == 'active']
            
            for mission in active_missions:
                mission_id = mission['id']
                daily_info = mission_manager.get_daily_mission_info(username, lesson_id, mission_id)
                
                if daily_info and not daily_info.get('is_completed'):
                    current_day = daily_info['current_day']
                    total_days = daily_info['total_days']
                    
                    col1_inner, col2_inner = st.columns([3, 1])
                    with col1_inner:
                        st.markdown(f"**{mission['title']}** - Dzień {current_day}/{total_days}")
                    with col2_inner:
                        if st.button("📋 Otwórz", key=f"open_active_{mission_id}"):
                            st.session_state.active_mission = mission_id
                            st.session_state.show_daily_mission = True
        else:
            st.markdown("💡 **Rozpocznij swoje pierwsze zadanie praktyczne!**")
    
    with col2:
        # Navigation button to the lesson
        if st.button("🎯 Idź do misji", key=f"go_to_missions_{lesson_id}", use_container_width=True):
            # Navigate to lesson B1C1L1 and show summary with missions tab
            st.session_state.current_lesson = lesson_id
            st.session_state.lesson_step = 'summary'
            st.session_state.show_missions_tab = True
            st.rerun()


def render_missions_page(username: str, lesson_id: str):
    """Render full missions page for a lesson"""
    st.title("🎯 Misje praktyczne: Strach przed stratą")
    st.markdown("Praktyczne zadania pomagające opanować strach przed stratą w inwestowaniu")
    
    # Check if user wants to show daily mission interface
    if st.session_state.get('show_daily_mission') and st.session_state.get('active_mission'):
        if st.button("← Powrót do listy misji"):
            st.session_state.show_daily_mission = False
            st.session_state.active_mission = None
            st.rerun()
        
        st.markdown("---")
        render_daily_mission_interface(username, lesson_id, st.session_state.active_mission)
        return
    
    # Show mission summary
    render_mission_summary_widget(username, lesson_id)
    
    # Show available missions
    missions = mission_manager.get_available_missions(username, lesson_id)
    
    if not missions:
        st.warning("Brak dostępnych misji dla tej lekcji.")
        return
    
    st.markdown("## 🚀 Dostępne misje")
    
    for mission in missions:
        render_mission_card(mission, username, lesson_id)
    
    st.markdown("---")
    st.markdown("""
    ### 💡 Wskazówki dotyczące misji
    
    - **Rozpocznij misję** gdy masz czas na codzienne zadania przez określoną liczbę dni
    - **Bądź konsekwentny** - codzienne małe kroki dają lepsze rezultaty niż sporadyczne wielkie wysiłki  
    - **Nie martw się pomyłkami** - każdy dzień to nowa szansa na poprawę
    - **Zadawaj pytania** - jeśli coś jest niejasne, skontaktuj się ze społecznością
    
    Powodzenia w opanowywaniu strachu przed stratą! 🌟
    """)
