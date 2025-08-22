# BADGE SYSTEM - STEP 4: Enhanced Badge Display System
# =====================================================

import streamlit as st
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from config.settings import BADGES, BADGE_CATEGORIES, BADGE_TIERS
from utils.badge_tracking import BadgeTracker
from utils.achievements import load_user_data

class BadgeDisplaySystem:
    """
    Enhanced badge display system with progress visualization and interactive elements
    """
    
    def __init__(self):
        self.tracker = BadgeTracker()
    
    def render_enhanced_badge_section(self, username: str):
        """
        Renderuj główną sekcję odznak z ulepszonymi komponentami
        """
        # Pobierz dane użytkownika z BadgeTracker
        badge_data = self.tracker.get_user_badge_data(username)
        badge_stats = self.tracker.get_badge_statistics(username)
        
        # Header z ogólnymi statystykami
        self._render_badge_header(badge_stats)
        
        # Dashboard postępu
        self._render_progress_dashboard(badge_data, badge_stats)
        
        # Kategorie odznak z ulepszonymi kartami
        self._render_badge_categories(username, badge_data)
    
    def _render_badge_header(self, badge_stats: Dict[str, Any]):
        """Renderuj header z ogólnymi statystykami odznak"""
        st.markdown("""
        <div class="badge-header">
            <h1 class="badge-title">🏆 Twoje Odznaki</h1>
            <p class="badge-subtitle">Śledź swój postęp i odkrywaj nowe osiągnięcia</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Statystyki w jednym wierszu
        stats_cols = st.columns(4)
        
        with stats_cols[0]:
            self._render_stat_card(
                "🏅", 
                str(badge_stats.get('total_earned', 0)), 
                "Zdobyte odznaki",
                change=badge_stats.get('recent_badges_count', 0),
                change_type="positive" if badge_stats.get('recent_badges_count', 0) > 0 else None
            )
        
        with stats_cols[1]:
            total_categories = len(BADGE_CATEGORIES)
            completed_categories = len(badge_stats.get('categories_completed', []))
            self._render_stat_card(
                "📋", 
                f"{completed_categories}/{total_categories}", 
                "Kategorie ukończone",
                progress=int((completed_categories / total_categories) * 100) if total_categories > 0 else 0
            )
        
        with stats_cols[2]:
            total_xp = badge_stats.get('total_badge_xp', 0)
            self._render_stat_card(
                "⭐", 
                str(total_xp), 
                "XP z odznak",
                change=badge_stats.get('recent_xp_gain', 0),
                change_type="positive" if badge_stats.get('recent_xp_gain', 0) > 0 else None
            )
        
        with stats_cols[3]:
            highest_tier = badge_stats.get('highest_tier_earned', 'bronze')
            tier_name = BADGE_TIERS.get(highest_tier, {}).get('name', 'Brązowa')
            self._render_stat_card(
                "💎", 
                tier_name, 
                "Najwyższy tier",
                tier_color=BADGE_TIERS.get(highest_tier, {}).get('color', '#CD7F32')
            )
    
    def _render_stat_card(self, icon: str, value: str, label: str, 
                         change: Optional[int] = None, change_type: Optional[str] = None,
                         progress: Optional[int] = None, tier_color: Optional[str] = None):
        """Renderuj kartę statystyki z animacjami"""
        change_html = ""
        if change is not None and change != 0:
            change_class = f"stat-change {change_type}" if change_type else "stat-change"
            change_symbol = "+" if change > 0 else ""
            change_html = f'<div class="{change_class}">{change_symbol}{change}</div>'
        
        progress_html = ""
        if progress is not None:
            progress_html = f"""
            <div class="mini-progress-bar">
                <div class="mini-progress-fill" style="width: {progress}%;"></div>
            </div>
            """
        
        tier_style = ""
        if tier_color:
            tier_style = f"color: {tier_color}; font-weight: bold;"
        
        st.markdown(f"""
        <div class="enhanced-stat-card">
            <div class="stat-icon">{icon}</div>
            <div class="stat-value" style="{tier_style}">{value}</div>
            <div class="stat-label">{label}</div>
            {change_html}
            {progress_html}        </div>
        """, unsafe_allow_html=True)
    
    def _render_progress_dashboard(self, badge_data: Dict[str, Any], badge_stats: Dict[str, Any]):
        """Renderuj dashboard postępu"""
        st.markdown("### 📊 Twój postęp")
        
        # Rekomendacje następnych odznak
        recommendations = self.tracker.get_recommended_badges(st.session_state.username)
        
        if recommendations:
            st.markdown("#### 🎯 Sugerowane następne odznaki")
            rec_cols = st.columns(min(len(recommendations), 3))
            
            for i, recommendation in enumerate(recommendations):
                if i < 3:  # Maksymalnie 3 rekomendacje
                    with rec_cols[i]:
                        badge_id = recommendation.get('badge_id')
                        if badge_id:
                            self._render_recommendation_card(badge_id, recommendation)
    
    def _render_recommendation_card(self, badge_id: str, recommendation: Dict[str, Any]):
        """Renderuj kartę rekomendowanej odznaki"""
        badge_info = BADGES.get(badge_id, {})
        progress = recommendation.get('progress', 0)
        
        # Próbuj pobrać szczegółowe informacje o postępie z trackera
        try:
            detailed_progress = self.tracker.get_badge_progress_detailed(st.session_state.username, badge_id)
            conditions_status = detailed_progress.get('conditions_status', {})
            next_steps = detailed_progress.get('next_steps', [])
        except:
            conditions_status = {}
            next_steps = ["Sprawdź wymagania odznaki"]
        
        # Oblicz brakujące kroki jako fallback
        if not next_steps:
            missing_steps = []
            for condition, status in conditions_status.items():
                if not status:
                    missing_steps.append(condition)
            next_steps = missing_steps[:2]  # Maksymalnie 2 kroki
        
        if not next_steps:
            next_steps = ["Ukończ pozostałe wymagania"]
        
        st.markdown(f"""
        <div class="recommendation-card">
            <div class="rec-header">
                <div class="rec-icon">{badge_info.get('icon', '🏆')}</div>
                <div class="rec-title">{badge_info.get('name', 'Nieznana odznaka')}</div>
            </div>
            <div class="rec-progress-container">
                <div class="rec-progress-bar">
                    <div class="rec-progress-fill" style="width: {progress}%;"></div>
                </div>
                <div class="rec-progress-text">{progress}% ukończone</div>
            </div>
            <div class="rec-description">{badge_info.get('description', '')}</div>
            <div class="rec-next-steps">
                <strong>Następne kroki:</strong>
                <ul>
                    {"".join([f"<li>{step}</li>" for step in next_steps[:2]])}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_badge_categories(self, username: str, badge_data: Dict[str, Any]):
        """Renderuj kategorie odznak z ulepszonymi kartami"""
        st.markdown("### 🗂️ Kategorie odznak")
        
        # Pogrupuj odznaki według kategorii
        category_badges = {}
        for category_id, category_info in BADGE_CATEGORIES.items():
            category_badges[category_id] = []
            
            for badge_id in BADGES:
                if BADGES[badge_id].get('category') == category_id:
                    category_badges[category_id].append(badge_id)
        
        # Twórz taby dla kategorii
        category_tabs = st.tabs([info['name'] for info in BADGE_CATEGORIES.values()])
        
        for i, (category_id, category_info) in enumerate(BADGE_CATEGORIES.items()):
            with category_tabs[i]:
                self._render_category_content(username, category_id, category_info, 
                                            category_badges[category_id], badge_data)
    
    def _render_category_content(self, username: str, category_id: str, category_info: Dict[str, Any],
                                badge_ids: List[str], badge_data: Dict[str, Any]):
        """Renderuj zawartość kategorii z postępem i odznkami"""
        
        # Header kategorii z postępem
        earned_in_category = sum(1 for badge_id in badge_ids 
                                if badge_data.get('badges', {}).get(badge_id, {}).get('earned', False))
        total_in_category = len(badge_ids)
        category_progress = int((earned_in_category / total_in_category) * 100) if total_in_category > 0 else 0
        
        st.markdown(f"""
        <div class="category-header">
            <div class="category-icon">{category_info.get('icon', '📋')}</div>
            <div class="category-info">
                <h3>{category_info['name']}</h3>
                <p>{category_info['description']}</p>
                <div class="category-progress">
                    <div class="category-progress-bar">
                        <div class="category-progress-fill" style="width: {category_progress}%; background-color: {category_info.get('color', '#2196F3')};"></div>
                    </div>
                    <div class="category-progress-text">{earned_in_category}/{total_in_category} odznak ({category_progress}%)</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sortuj odznaki: zdobyte najpierw, potem według postępu
        sorted_badges = self._sort_badges_for_display(badge_ids, badge_data)
        
        # Wyświetl odznaki w siatce
        badge_cols = st.columns(3)
        for i, badge_id in enumerate(sorted_badges):
            with badge_cols[i % 3]:
                self._render_enhanced_badge_card(username, badge_id, badge_data)
    
    def _sort_badges_for_display(self, badge_ids: List[str], badge_data: Dict[str, Any]) -> List[str]:
        """Sortuj odznaki dla lepszego wyświetlania"""
        def sort_key(badge_id):
            badge_info = badge_data.get('badges', {}).get(badge_id, {})
            progress_info = badge_data.get('badge_progress', {}).get(badge_id, {})
            
            if badge_info.get('earned', False):
                # Zdobyte odznaki - sortuj według daty zdobycia
                earned_date = badge_info.get('earned_date', '1970-01-01')
                return (0, earned_date)  # 0 dla najwyższego priorytetu
            else:
                # Niezdobyte - sortuj według postępu (malejąco)
                progress = progress_info.get('progress', 0)
                return (1, -progress)  # 1 dla niższego priorytetu, ujemny progress dla malejącej kolejności
        
        return sorted(badge_ids, key=sort_key)
    
    def _render_enhanced_badge_card(self, username: str, badge_id: str, badge_data: Dict[str, Any]):
        """Renderuj ulepszoną kartę odznaki z interaktywnymi elementami"""
        badge_info = BADGES.get(badge_id, {})
        user_badge_data = badge_data.get('badges', {}).get(badge_id, {})
        progress_data = badge_data.get('badge_progress', {}).get(badge_id, {})
        
        is_earned = user_badge_data.get('earned', False)
        progress = progress_data.get('progress', 0) if not is_earned else 100
        
        # Ustal styl karty
        card_class = "enhanced-badge-card"
        if is_earned:
            card_class += " earned"
            tier = user_badge_data.get('tier', 'bronze')
            tier_color = BADGE_TIERS.get(tier, {}).get('color', '#CD7F32')
        else:
            card_class += " locked"
            tier_color = "#cccccc"
        
        # Renderuj kartę
        card_html = f"""
        <div class="{card_class}" data-badge-id="{badge_id}">
            <div class="badge-card-header">
                <div class="badge-icon-container">
                    <div class="badge-icon" style="background: linear-gradient(135deg, {tier_color}, {tier_color}aa);">
                        {badge_info.get('icon', '🔒') if is_earned else '🔒'}
                    </div>
                    {self._get_tier_indicator(user_badge_data.get('tier', 'bronze')) if is_earned else ''}
                </div>
                <div class="badge-status">
                    {'✅ Zdobyta' if is_earned else f'🔄 {progress}%'}
                </div>
            </div>
            
            <div class="badge-card-body">
                <h4 class="badge-name">{badge_info.get('name', 'Nieznana odznaka')}</h4>
                <p class="badge-description">{badge_info.get('description', '')}</p>
                
                {self._get_progress_section(progress, is_earned, progress_data)}
                {self._get_earned_info(user_badge_data) if is_earned else ''}
            </div>
            
            <div class="badge-card-footer">
                {self._get_badge_actions(badge_id, is_earned, progress_data)}
            </div>
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Dodaj tooltip z dodatkowymi informacjami
        if st.button("ℹ️", key=f"badge_info_{badge_id}", help="Więcej informacji"):
            self._show_badge_details_modal(badge_id, user_badge_data, progress_data)
    
    def _get_tier_indicator(self, tier: str) -> str:
        """Pobierz wskaźnik tier"""
        tier_info = BADGE_TIERS.get(tier, {})
        tier_color = tier_info.get('color', '#CD7F32')
        tier_name = tier_info.get('name', 'Brązowa')
        
        return f"""
        <div class="tier-indicator" style="background-color: {tier_color};">
            {tier_name}
        </div>
        """
    
    def _get_progress_section(self, progress: int, is_earned: bool, progress_data: Dict[str, Any]) -> str:
        """Pobierz sekcję postępu"""
        if is_earned:
            return '<div class="progress-section earned-badge">Odznaka zdobyta! 🎉</div>'
        
        if progress == 0:
            return '<div class="progress-section not-started">Nie rozpoczęto</div>'
        
        # Następne kroki
        next_steps = []
        conditions_status = progress_data.get('conditions_status', {})
        for condition, status in conditions_status.items():
            if not status:
                next_steps.append(condition)
        
        next_step = next_steps[0] if next_steps else "Ukończ pozostałe wymagania"
        
        return f"""
        <div class="progress-section in-progress">
            <div class="progress-bar-container">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%;"></div>
                </div>
                <span class="progress-text">{progress}%</span>
            </div>
            <div class="next-step">
                <strong>Następny krok:</strong> {next_step}
            </div>
        </div>
        """
    
    def _get_earned_info(self, user_badge_data: Dict[str, Any]) -> str:
        """Pobierz informacje o zdobytej odznace"""
        earned_date = user_badge_data.get('earned_date', '')
        xp_earned = user_badge_data.get('xp_earned', 0)
        
        if earned_date:
            try:
                date_obj = datetime.fromisoformat(earned_date.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%d.%m.%Y')
            except:
                formatted_date = earned_date
        else:
            formatted_date = "Nieznana data"
        
        return f"""
        <div class="earned-info">
            <div class="earned-date">📅 Zdobyta: {formatted_date}</div>
            <div class="earned-xp">⭐ XP: +{xp_earned}</div>
        </div>
        """
    
    def _get_badge_actions(self, badge_id: str, is_earned: bool, progress_data: Dict[str, Any]) -> str:
        """Pobierz akcje dla odznaki"""
        if is_earned:
            return '<button class="badge-action-btn earned">🏆 Zdobyta</button>'
        
        progress = progress_data.get('progress', 0)
        if progress > 0:
            return '<button class="badge-action-btn in-progress">📈 W trakcie</button>'
        else:
            return '<button class="badge-action-btn locked">🔒 Zablokowana</button>'
    
    def _show_badge_details_modal(self, badge_id: str, user_badge_data: Dict[str, Any], 
                                 progress_data: Dict[str, Any]):
        """Pokaż modal z szczegółami odznaki"""
        badge_info = BADGES.get(badge_id, {})
        
        with st.expander(f"📋 Szczegóły: {badge_info.get('name', 'Nieznana odznaka')}", expanded=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 64px; margin: 20px 0;">
                        {badge_info.get('icon', '🏆')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                **Nazwa:** {badge_info.get('name', 'Nieznana odznaka')}
                
                **Opis:** {badge_info.get('description', 'Brak opisu')}
                
                **Kategoria:** {BADGE_CATEGORIES.get(badge_info.get('category', 'other'), {}).get('name', 'Inne')}
                
                **XP:** {badge_info.get('xp', 0)}
                """)
                
                # Warunki zdobycia
                if 'conditions' in badge_info:
                    st.markdown("**Warunki zdobycia:**")
                    conditions = badge_info['conditions']
                    conditions_status = progress_data.get('conditions_status', {})
                    
                    for condition_key, condition_desc in conditions.items():
                        status = conditions_status.get(condition_key, False)
                        status_icon = "✅" if status else "❌"
                        st.markdown(f"- {status_icon} {condition_desc}")
    
    def add_enhanced_badge_styles(self):
        """Dodaj ulepszone style CSS dla systemu odznak"""
        st.markdown("""
        <style>
        /* Badge Header */
        .badge-header {
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            border-radius: 20px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .badge-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0 0 10px 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .badge-subtitle {
            font-size: 1.2rem;
            margin: 0;
            opacity: 0.9;
        }
        
        /* Enhanced Stat Cards */
        .enhanced-stat-card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 1px solid #f0f0f0;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .enhanced-stat-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        }
        
        .enhanced-stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .enhanced-stat-card .stat-icon {
            font-size: 32px;
            margin-bottom: 12px;
            display: block;
        }
        
        .enhanced-stat-card .stat-value {
            font-size: 28px;
            font-weight: 700;
            color: #333;
            margin-bottom: 8px;
        }
        
        .enhanced-stat-card .stat-label {
            font-size: 14px;
            color: #666;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stat-change {
            margin-top: 8px;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .stat-change.positive {
            background: rgba(39, 174, 96, 0.1);
            color: #27ae60;
        }
        
        .mini-progress-bar {
            width: 100%;
            height: 4px;
            background: #f0f0f0;
            border-radius: 2px;
            margin-top: 8px;
            overflow: hidden;
        }
        
        .mini-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 2px;
            transition: width 0.8s ease;
        }
        
        /* Recommendation Cards */
        .recommendation-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 2px solid #e3f2fd;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .recommendation-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            border-color: #2196F3;
        }
        
        .rec-header {
            display: flex;
            align-items: center;
            margin-bottom: 16px;
        }
        
        .rec-icon {
            font-size: 32px;
            margin-right: 12px;
        }
        
        .rec-title {
            font-weight: 600;
            color: #333;
            font-size: 16px;
        }
        
        .rec-progress-container {
            margin: 16px 0;
        }
        
        .rec-progress-bar {
            width: 100%;
            height: 8px;
            background: #f0f0f0;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 8px;
        }
        
        .rec-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #2196F3, #64B5F6);
            border-radius: 4px;
            transition: width 0.8s ease;
        }
        
        .rec-progress-text {
            font-size: 12px;
            color: #666;
            text-align: right;
        }
        
        .rec-description {
            color: #666;
            font-size: 14px;
            margin-bottom: 16px;
            line-height: 1.4;
        }
        
        .rec-next-steps {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            font-size: 13px;
        }
        
        .rec-next-steps ul {
            margin: 8px 0 0 0;
            padding-left: 16px;
        }
        
        .rec-next-steps li {
            margin: 4px 0;
            color: #555;
        }
        
        /* Category Headers */
        .category-header {
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 1px solid #f0f0f0;
            display: flex;
            align-items: center;
        }
        
        .category-icon {
            font-size: 48px;
            margin-right: 20px;
        }
        
        .category-info {
            flex: 1;
        }
        
        .category-info h3 {
            margin: 0 0 8px 0;
            color: #333;
            font-size: 24px;
            font-weight: 600;
        }
        
        .category-info p {
            margin: 0 0 16px 0;
            color: #666;
            font-size: 16px;
        }
        
        .category-progress-bar {
            width: 100%;
            height: 8px;
            background: #f0f0f0;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 8px;
        }
        
        .category-progress-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.8s ease;
        }
        
        .category-progress-text {
            font-size: 14px;
            color: #666;
            font-weight: 500;
        }
        
        /* Enhanced Badge Cards */
        .enhanced-badge-card {
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 2px solid #f0f0f0;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .enhanced-badge-card.earned {
            border-color: #4CAF50;
            background: linear-gradient(135deg, #ffffff 0%, #f8fff8 100%);
        }
        
        .enhanced-badge-card.locked {
            border-color: #ddd;
            background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 100%);
            opacity: 0.8;
        }
        
        .enhanced-badge-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        }
        
        .badge-card-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }
        
        .badge-icon-container {
            position: relative;
        }
        
        .badge-icon {
            font-size: 48px;
            width: 64px;
            height: 64px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 3px solid white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        .tier-indicator {
            position: absolute;
            bottom: -8px;
            right: -8px;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: 600;
            color: white;
            text-transform: uppercase;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        
        .badge-status {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            background: #e3f2fd;
            color: #1976d2;
        }
        
        .enhanced-badge-card.earned .badge-status {
            background: #e8f5e8;
            color: #2e7d32;
        }
        
        .badge-name {
            margin: 0 0 8px 0;
            color: #333;
            font-size: 18px;
            font-weight: 600;
        }
        
        .badge-description {
            margin: 0 0 16px 0;
            color: #666;
            font-size: 14px;
            line-height: 1.4;
        }
        
        /* Progress Sections */
        .progress-section {
            margin: 16px 0;
            padding: 12px;
            border-radius: 8px;
        }
        
        .progress-section.earned-badge {
            background: #e8f5e8;
            color: #2e7d32;
            text-align: center;
            font-weight: 600;
        }
        
        .progress-section.not-started {
            background: #fafafa;
            color: #666;
            text-align: center;
        }
        
        .progress-section.in-progress {
            background: #f3f4f6;
        }
        
        .progress-bar-container {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        }
        
        .progress-bar {
            flex: 1;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #2196F3, #64B5F6);
            border-radius: 4px;
            transition: width 0.8s ease;
        }
        
        .progress-text {
            font-size: 12px;
            font-weight: 600;
            color: #333;
            min-width: 40px;
        }
        
        .next-step {
            font-size: 12px;
            color: #555;
        }
        
        .earned-info {
            background: #f8f9fa;
            padding: 12px;
            border-radius: 8px;
            margin: 16px 0;
        }
        
        .earned-date, .earned-xp {
            font-size: 12px;
            color: #666;
            margin: 4px 0;
        }
        
        /* Badge Actions */
        .badge-card-footer {
            margin-top: 16px;
            text-align: center;
        }
        
        .badge-action-btn {
            padding: 8px 16px;
            border: none;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .badge-action-btn.earned {
            background: #4CAF50;
            color: white;
        }
        
        .badge-action-btn.in-progress {
            background: #2196F3;
            color: white;
        }
        
        .badge-action-btn.locked {
            background: #ccc;
            color: #666;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .badge-header {
                padding: 24px 16px;
            }
            
            .badge-title {
                font-size: 2rem;
            }
            
            .category-header {
                flex-direction: column;
                text-align: center;
            }
            
            .category-icon {
                margin: 0 0 16px 0;
            }
            
            .enhanced-badge-card {
                padding: 16px;
            }
            
            .badge-icon {
                font-size: 40px;
                width: 56px;
                height: 56px;
            }
        }
        </style>
        """, unsafe_allow_html=True)


# Globalna instancja systemu wyświetlania odznak
badge_display = BadgeDisplaySystem()

def render_enhanced_badges(username: str):
    """
    Funkcja pomocnicza do renderowania ulepszonego systemu odznak
    """
    badge_display.add_enhanced_badge_styles()
    badge_display.render_enhanced_badge_section(username)
