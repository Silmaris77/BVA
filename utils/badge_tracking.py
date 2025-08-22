# BADGE SYSTEM - STEP 3: Comprehensive User Badge Tracking and Progress Storage
# ================================================================================

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union, Tuple
from config.settings import BADGES, BADGE_CATEGORIES, BADGE_TIERS, XP_LEVELS
from utils.achievements import check_badge_condition, load_user_data, save_user_data

class BadgeTracker:
    """
    Comprehensive badge tracking and progress management system
    """
    
    def __init__(self):
        self.cache = {}
        self.performance_stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'updates_processed': 0
        }
    
    # ==========================================
    # CORE BADGE TRACKING FUNCTIONS
    # ==========================================
    
    def get_user_badge_data(self, username: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Pobierz pełne dane odznak użytkownika z cache'em dla wydajności
        
        Args:
            username: Nazwa użytkownika
            use_cache: Czy używać cache (domyślnie True)
        
        Returns:
            Dict zawierający pełne dane odznak użytkownika
        """
        cache_key = f"badge_data_{username}"
        
        if use_cache and cache_key in self.cache:
            self.performance_stats['cache_hits'] += 1
            return self.cache[cache_key]
        
        self.performance_stats['cache_misses'] += 1
        user_data = load_user_data(username)
        
        if not user_data:
            return self._get_empty_badge_data()
        
        # Migruj stare dane jeśli potrzebne
        badge_data = self._migrate_badge_data(user_data)
        
        # Cache'uj wyniki
        if use_cache:
            self.cache[cache_key] = badge_data
        
        return badge_data
    
    def update_badge_progress(self, username: str, context: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Aktualizuj postęp wszystkich odznak użytkownika
        
        Args:
            username: Nazwa użytkownika
            context: Kontekst wywołania
            **kwargs: Dodatkowe dane kontekstowe
        
        Returns:
            Dict z informacjami o aktualizacji
        """
        self.performance_stats['updates_processed'] += 1
        user_data = load_user_data(username)
        
        if not user_data:
            return {'error': 'User not found'}
        
        # Pobierz aktualne dane odznak
        badge_data = self.get_user_badge_data(username, use_cache=False)
        
        # Aktualizuj postęp dla wszystkich odznak
        progress_updates = {}
        new_badges = []
        context_data = context or {}
        context_data.update(kwargs)
        
        for badge_id, badge_info in BADGES.items():
            if not badge_data['badges'].get(badge_id, {}).get('earned', False):
                # Sprawdź postęp odznaki
                progress_info = self._calculate_badge_progress(badge_id, user_data, context_data)
                
                # Aktualizuj dane postępu
                badge_data['badge_progress'][badge_id] = progress_info
                
                # Sprawdź czy odznaka została zdobyta
                if progress_info['progress'] >= 100:
                    new_badge_data = self._award_badge(badge_id, user_data, context_data, progress_info)
                    badge_data['badges'][badge_id] = new_badge_data
                    new_badges.append(badge_id)
                    
                    # Usuń z postępu (już zdobyte)
                    del badge_data['badge_progress'][badge_id]
                
                progress_updates[badge_id] = progress_info
        
        # Aktualizuj statystyki
        badge_data['badge_stats'] = self._calculate_badge_stats(badge_data)
        
        # Zapisz zmiany
        self._save_badge_data(username, user_data, badge_data)
        
        # Wyczyść cache dla tego użytkownika
        self._clear_user_cache(username)
        
        return {
            'new_badges': new_badges,
            'progress_updates': progress_updates,
            'stats': badge_data['badge_stats'],
            'timestamp': datetime.now().isoformat()
        }
    
    def get_badge_progress_detailed(self, username: str, badge_id: str) -> Dict[str, Any]:
        """
        Pobierz szczegółowy postęp dla konkretnej odznaki
        
        Args:
            username: Nazwa użytkownika
            badge_id: ID odznaki
        
        Returns:
            Dict ze szczegółowym postępem odznaki
        """
        if badge_id not in BADGES:
            return {'error': 'Badge not found'}
        
        user_data = load_user_data(username)
        if not user_data:
            return {'error': 'User not found'}
        
        badge_data = self.get_user_badge_data(username)
        
        # Sprawdź czy odznaka już zdobyta
        if badge_data['badges'].get(badge_id, {}).get('earned', False):
            return {
                'badge_id': badge_id,
                'status': 'earned',
                'earned_data': badge_data['badges'][badge_id],
                'progress': 100
            }
        
        # Oblicz aktualny postęp
        progress_info = self._calculate_badge_progress(badge_id, user_data, {})
        
        return {
            'badge_id': badge_id,
            'status': 'in_progress',
            'progress': progress_info['progress'],
            'conditions_status': progress_info['conditions_status'],
            'next_steps': progress_info.get('next_steps', []),
            'estimated_completion': progress_info.get('estimated_completion'),
            'tips': self._get_badge_tips(badge_id, progress_info)
        }
    
    def get_recommended_badges(self, username: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Pobierz rekomendowane odznaki dla użytkownika
        
        Args:
            username: Nazwa użytkownika
            limit: Maksymalna liczba rekomendacji
        
        Returns:
            Lista rekomendowanych odznak
        """
        user_data = load_user_data(username)
        if not user_data:
            return []
        
        badge_data = self.get_user_badge_data(username)
        recommendations = []
        
        # Zbierz odznaki w toku i ich postęp
        progress_badges = []
        for badge_id, progress_info in badge_data['badge_progress'].items():
            if progress_info['progress'] > 0:
                badge_info = BADGES[badge_id].copy()
                badge_info['badge_id'] = badge_id
                badge_info['progress'] = progress_info['progress']
                badge_info['priority_score'] = self._calculate_priority_score(badge_id, progress_info, user_data)
                progress_badges.append(badge_info)
        
        # Sortuj po wyniku priorytetowym
        progress_badges.sort(key=lambda x: x['priority_score'], reverse=True)
        
        # Dodaj najlepsze odznaki w toku
        recommendations.extend(progress_badges[:limit])
        
        # Jeśli potrzeba więcej, dodaj łatwe do zdobycia
        if len(recommendations) < limit:
            easy_badges = self._find_easy_badges(username, user_data, limit - len(recommendations))
            recommendations.extend(easy_badges)
        
        return recommendations[:limit]
    
    def get_badge_roadmap(self, username: str, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Wygeneruj mapę drogową odznak dla użytkownika
        
        Args:
            username: Nazwa użytkownika
            category: Opcjonalna kategoria do filtrowania
        
        Returns:
            Dict z mapą drogową odznak
        """
        user_data = load_user_data(username)
        if not user_data:
            return {'error': 'User not found'}
        
        badge_data = self.get_user_badge_data(username)
        
        # Filtruj odznaki według kategorii jeśli podana
        target_badges = BADGES
        if category and category in BADGE_CATEGORIES:
            target_badges = {
                badge_id: badge_info for badge_id, badge_info in BADGES.items()
                if badge_info.get('category') == category
            }
        
        roadmap = {
            'categories': {},
            'timeline': [],
            'milestones': [],
            'total_progress': 0
        }
        
        for category_id, category_info in BADGE_CATEGORIES.items():
            if category and category != category_id:
                continue
                
            category_badges = [
                badge_id for badge_id, badge_info in target_badges.items()
                if badge_info.get('category') == category_id
            ]
            
            category_progress = self._calculate_category_progress(category_badges, badge_data)
            
            roadmap['categories'][category_id] = {
                'name': category_info['name'],
                'description': category_info['description'],
                'total_badges': len(category_badges),
                'earned_badges': category_progress['earned'],
                'progress_percentage': category_progress['percentage'],
                'next_badge': category_progress.get('next_badge'),
                'badges': category_progress['badges']
            }
        
        # Oblicz ogólny postęp
        total_badges = len(target_badges)
        earned_badges = len([b for b in badge_data['badges'].values() if b.get('earned', False)])
        roadmap['total_progress'] = (earned_badges / total_badges * 100) if total_badges > 0 else 0
        
        return roadmap
    
    # ==========================================
    # STATISTYKI I ANALYTICS
    # ==========================================
    
    def get_badge_statistics(self, username: str) -> Dict[str, Any]:
        """
        Pobierz szczegółowe statystyki odznak użytkownika
        
        Args:
            username: Nazwa użytkownika
        
        Returns:
            Dict ze szczegółowymi statystykami
        """
        badge_data = self.get_user_badge_data(username)
        user_data = load_user_data(username)
        
        if not user_data:
            return {'error': 'User not found'}
        
        stats = {
            'overview': badge_data['badge_stats'],
            'earning_timeline': self._generate_earning_timeline(badge_data),
            'category_breakdown': self._generate_category_breakdown(badge_data),
            'tier_distribution': self._generate_tier_distribution(badge_data),
            'recent_activity': self._generate_recent_badge_activity(badge_data),
            'achievements': self._generate_achievement_insights(badge_data, user_data),
            'performance_metrics': self._generate_performance_metrics(badge_data, user_data)
        }
        
        return stats
    
    def get_badge_leaderboard(self, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Pobierz ranking użytkowników według odznak
        
        Args:
            category: Opcjonalna kategoria do filtrowania
            limit: Maksymalna liczba pozycji
        
        Returns:
            Lista użytkowników w rankingu
        """
        try:
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users_data.json')
            with open(file_path, 'r', encoding='utf-8') as f:
                all_users_data = json.load(f)
        except:
            return []
        
        leaderboard = []
        
        for username, user_data in all_users_data.items():
            user_score = self._calculate_leaderboard_score(username, user_data, category)
            if user_score['total_score'] > 0:
                leaderboard.append({
                    'username': username,
                    'total_badges': user_score['total_badges'],
                    'badge_xp': user_score['badge_xp'],
                    'total_score': user_score['total_score'],
                    'highest_tier': user_score['highest_tier'],
                    'categories_completed': user_score['categories_completed'],
                    'recent_badges': user_score['recent_badges']
                })
        
        # Sortuj według wyniku
        leaderboard.sort(key=lambda x: x['total_score'], reverse=True)
        
        return leaderboard[:limit]
    
    # ==========================================
    # FUNKCJE POMOCNICZE
    # ==========================================
    
    def _get_empty_badge_data(self) -> Dict[str, Any]:
        """Zwróć pustą strukturę danych odznak"""
        return {
            'badges': {},
            'badge_progress': {},
            'badge_stats': {
                'total_earned': 0,
                'categories_completed': [],
                'current_streak': 0,
                'highest_tier_earned': None,
                'total_badge_xp': 0,
                'last_badge_earned': None,
                'earning_rate': 0.0
            }
        }
    
    def _migrate_badge_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Migruj stare dane odznak do nowego formatu
        
        Args:
            user_data: Dane użytkownika
        
        Returns:
            Zmigrowane dane odznak
        """
        # Rozpocznij z pustą strukturą
        badge_data = self._get_empty_badge_data()
        
        # Migruj istniejące odznaki ze starego formatu
        old_badges = user_data.get('badges', [])
        
        for badge_id in old_badges:
            if badge_id in BADGES:
                badge_info = BADGES[badge_id]
                badge_data['badges'][badge_id] = {
                    'earned': True,
                    'earned_date': user_data.get('joined_date', datetime.now().strftime('%Y-%m-%d')),
                    'xp_earned': badge_info.get('xp_reward', 0),
                    'tier': badge_info.get('tier', 'bronze'),
                    'conditions_met': ['migrated'],
                    'progress_when_earned': 100,
                    'context': {'migrated': True}
                }
        
        # Oblicz postęp dla nie-zdobytych odznak
        for badge_id in BADGES.keys():
            if badge_id not in badge_data['badges']:
                progress_info = self._calculate_badge_progress(badge_id, user_data, {})
                if progress_info['progress'] > 0:
                    badge_data['badge_progress'][badge_id] = progress_info
        
        # Oblicz statystyki
        badge_data['badge_stats'] = self._calculate_badge_stats(badge_data)
        
        return badge_data
    
    def _calculate_badge_progress(self, badge_id: str, user_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Oblicz postęp dla konkretnej odznaki
        
        Args:
            badge_id: ID odznaki
            user_data: Dane użytkownika
            context: Kontekst wywołania
        
        Returns:
            Dict z informacjami o postępie
        """
        if badge_id not in BADGES:
            return {'progress': 0, 'conditions_status': {}}
        
        badge_info = BADGES[badge_id]
        
        # Sprawdź czy warunki są spełnione
        conditions_met = check_badge_condition(badge_id, user_data, context)
        
        if conditions_met:
            return {
                'progress': 100,
                'conditions_status': {'main_condition': True},
                'last_updated': datetime.now().isoformat(),
                'ready_to_claim': True
            }
        
        # Oblicz częściowy postęp dla złożonych odznak
        progress_info = self._calculate_partial_progress(badge_id, badge_info, user_data)
        
        return {
            'progress': progress_info['percentage'],
            'conditions_status': progress_info['conditions'],
            'last_updated': datetime.now().isoformat(),
            'next_steps': progress_info.get('next_steps', []),
            'estimated_completion': progress_info.get('estimated_completion')
        }
    
    def _calculate_partial_progress(self, badge_id: str, badge_info: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Oblicz częściowy postęp dla złożonych odznak
        
        Args:
            badge_id: ID odznaki
            badge_info: Informacje o odznace
            user_data: Dane użytkownika
        
        Returns:
            Dict z informacjami o częściowym postępie
        """
        category = badge_info.get('category', '')
        condition = badge_info.get('condition', '')
        requirement = badge_info.get('requirement', 1)
        
        progress = {'percentage': 0, 'conditions': {}, 'next_steps': []}
        
        # Logika dla różnych typów odznak
        if 'lesson' in badge_id and isinstance(requirement, int):
            # Odznaki za lekcje
            completed_lessons = len(user_data.get('completed_lessons', []))
            progress['percentage'] = min(100, (completed_lessons / requirement) * 100)
            progress['conditions']['lessons_completed'] = f"{completed_lessons}/{requirement}"
            if completed_lessons < requirement:
                progress['next_steps'].append(f"Ukończ jeszcze {requirement - completed_lessons} lekcji")
        
        elif 'xp' in badge_id:
            # Odznaki za XP
            current_xp = user_data.get('xp', 0)
            if badge_id == 'xp_collector':
                target_xp = 1000
            elif badge_id == 'xp_master':
                target_xp = 5000
            else:
                target_xp = requirement if isinstance(requirement, int) else 1000
            
            progress['percentage'] = min(100, (current_xp / target_xp) * 100)
            progress['conditions']['xp_progress'] = f"{current_xp}/{target_xp}"
            if current_xp < target_xp:
                progress['next_steps'].append(f"Zdobądź jeszcze {target_xp - current_xp} XP")
        
        elif 'login_streak' in badge_id:
            # Odznaki za streak logowania
            current_streak = user_data.get('login_streak', 0)
            target_streak = requirement if isinstance(requirement, int) else 3
            
            progress['percentage'] = min(100, (current_streak / target_streak) * 100)
            progress['conditions']['streak_progress'] = f"{current_streak}/{target_streak}"
            if current_streak < target_streak:
                progress['next_steps'].append(f"Kontynuuj streak przez {target_streak - current_streak} dni")
        
        elif badge_id == 'profile_complete':
            # Kompletność profilu
            required_fields = ['degen_type', 'avatar', 'theme']
            completed_fields = sum(1 for field in required_fields if user_data.get(field))
            progress['percentage'] = (completed_fields / len(required_fields)) * 100
            
            for field in required_fields:
                progress['conditions'][field] = bool(user_data.get(field))
            
            missing_fields = [field for field in required_fields if not user_data.get(field)]
            if missing_fields:
                progress['next_steps'].append(f"Uzupełnij: {', '.join(missing_fields)}")
        
        elif badge_id == 'badge_collector':
            # Kolekcjonowanie odznak
            current_badges = len(user_data.get('badges', []))
            target_badges = 10
            progress['percentage'] = min(100, (current_badges / target_badges) * 100)
            progress['conditions']['badges_collected'] = f"{current_badges}/{target_badges}"
            if current_badges < target_badges:
                progress['next_steps'].append(f"Zdobądź jeszcze {target_badges - current_badges} odznak")
        
        # Domyślna logika dla prostych warunków
        else:
            # Sprawdź podstawowe warunki
            basic_conditions = self._check_basic_conditions(badge_id, user_data)
            progress['percentage'] = 50 if any(basic_conditions.values()) else 0
            progress['conditions'] = basic_conditions
        
        return progress
    
    def _check_basic_conditions(self, badge_id: str, user_data: Dict[str, Any]) -> Dict[str, bool]:
        """
        Sprawdź podstawowe warunki dla odznaki
        
        Args:
            badge_id: ID odznaki
            user_data: Dane użytkownika
        
        Returns:
            Dict z wynikami podstawowych sprawdzeń
        """
        conditions = {}
        
        # Podstawowe sprawdzenia dla różnych odznak
        if badge_id == 'welcome':
            conditions['account_registered'] = bool(user_data.get('user_id'))
        
        elif badge_id == 'first_degen_test':
            conditions['test_taken'] = user_data.get('test_taken', False)
            conditions['has_degen_type'] = bool(user_data.get('degen_type'))
        
        elif badge_id == 'first_lesson':
            conditions['has_completed_lessons'] = len(user_data.get('completed_lessons', [])) > 0
        
        elif badge_id == 'community_member':
            conditions['community_joined'] = user_data.get('community_joined', False)
        
        # Dodaj więcej sprawdzeń według potrzeb
        
        return conditions
    
    def _award_badge(self, badge_id: str, user_data: Dict[str, Any], context: Dict[str, Any], progress_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Przyznaj odznakę użytkownikowi
        
        Args:
            badge_id: ID odznaki
            user_data: Dane użytkownika
            context: Kontekst przyznania
            progress_info: Informacje o postępie
        
        Returns:
            Dict z danymi przyznania odznaki
        """
        badge_info = BADGES[badge_id]
        
        # Oblicz XP z mnożnikiem tier
        base_xp = badge_info.get('xp_reward', 0)
        tier = badge_info.get('tier', 'bronze')
        multiplier = BADGE_TIERS.get(tier, {}).get('multiplier', 1.0)
        xp_earned = int(base_xp * multiplier)
        
        return {
            'earned': True,
            'earned_date': datetime.now().isoformat(),
            'xp_earned': xp_earned,
            'tier': tier,
            'conditions_met': list(progress_info.get('conditions_status', {}).keys()),
            'progress_when_earned': 100,
            'context': context
        }
    
    def _calculate_badge_stats(self, badge_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Oblicz statystyki odznak użytkownika
        
        Args:
            badge_data: Dane odznak użytkownika
        
        Returns:
            Dict ze statystykami
        """
        earned_badges = badge_data['badges']
        
        stats = {
            'total_earned': len(earned_badges),
            'categories_completed': [],
            'current_streak': 0,
            'highest_tier_earned': None,
            'total_badge_xp': 0,
            'last_badge_earned': None,
            'earning_rate': 0.0
        }
        
        if not earned_badges:
            return stats
        
        # Oblicz całkowite XP z odznak
        stats['total_badge_xp'] = sum(badge.get('xp_earned', 0) for badge in earned_badges.values())
        
        # Znajdź najwyższy tier
        tiers = [badge.get('tier', 'bronze') for badge in earned_badges.values()]
        tier_order = ['bronze', 'silver', 'gold', 'platinum', 'diamond']
        highest_tier_index = max((tier_order.index(tier) for tier in tiers if tier in tier_order), default=0)
        stats['highest_tier_earned'] = tier_order[highest_tier_index]
        
        # Ostatnia zdobyta odznaka
        recent_badges = sorted(
            earned_badges.items(),
            key=lambda x: x[1].get('earned_date', ''),
            reverse=True
        )
        if recent_badges:
            stats['last_badge_earned'] = {
                'badge_id': recent_badges[0][0],
                'earned_date': recent_badges[0][1].get('earned_date')
            }
        
        # Sprawdź ukończone kategorie
        for category_id in BADGE_CATEGORIES.keys():
            category_badges = [badge_id for badge_id, badge_info in BADGES.items() 
                             if badge_info.get('category') == category_id]
            earned_in_category = [badge_id for badge_id in category_badges if badge_id in earned_badges]
            
            if len(earned_in_category) == len(category_badges):
                stats['categories_completed'].append(category_id)
        
        return stats
    
    def _save_badge_data(self, username: str, user_data: Dict[str, Any], badge_data: Dict[str, Any]):
        """
        Zapisz dane odznak użytkownika
        
        Args:
            username: Nazwa użytkownika
            user_data: Dane użytkownika
            badge_data: Dane odznak do zapisania
        """
        # Aktualizuj główne dane użytkownika
        user_data['badge_data'] = badge_data
        
        # Zsynchronizuj z starym formatem dla kompatybilności
        user_data['badges'] = list(badge_data['badges'].keys())
        
        # Zaktualizuj XP użytkownika
        total_badge_xp = badge_data['badge_stats']['total_badge_xp']
        # Note: W rzeczywistej implementacji trzeba uważać na duplikowanie XP
        
        # Zapisz dane
        save_user_data(username, user_data)
    
    def _clear_user_cache(self, username: str):
        """Wyczyść cache dla użytkownika"""
        cache_key = f"badge_data_{username}"
        if cache_key in self.cache:
            del self.cache[cache_key]
    
    # ==========================================
    # DODATKOWE FUNKCJE ANALITYCZNE
    # ==========================================
    
    def _calculate_priority_score(self, badge_id: str, progress_info: Dict[str, Any], user_data: Dict[str, Any]) -> float:
        """Oblicz wynik priorytetowy dla rekomendacji odznaki"""
        badge_info = BADGES[badge_id]
        
        score = 0.0
        
        # Wyższy priorytet dla odznak z większym postępem
        score += progress_info['progress'] * 0.4
        
        # Wyższy priorytet dla odznak z wyższym XP
        score += badge_info.get('xp_reward', 0) * 0.1
        
        # Wyższy priorytet dla wyższych tier
        tier_multipliers = {'bronze': 1.0, 'silver': 1.2, 'gold': 1.5, 'platinum': 2.0, 'diamond': 3.0}
        tier = badge_info.get('tier', 'bronze')
        score *= tier_multipliers.get(tier, 1.0)
        
        # Wyższy priorytet dla kategorii gdzie użytkownik ma już odznaki
        user_badges = user_data.get('badges', [])
        category = badge_info.get('category', '')
        category_badges = [bid for bid, binfo in BADGES.items() if binfo.get('category') == category]
        category_progress = len([bid for bid in category_badges if bid in user_badges]) / len(category_badges)
        score += category_progress * 20
        
        return score
    
    def _find_easy_badges(self, username: str, user_data: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
        """Znajdź łatwe do zdobycia odznaki"""
        easy_badges = []
        
        # Sprawdź odznaki które są blisko ukończenia
        for badge_id, badge_info in BADGES.items():
            if badge_id not in user_data.get('badges', []):
                progress_info = self._calculate_badge_progress(badge_id, user_data, {})
                
                if progress_info['progress'] >= 70:  # Przynajmniej 70% postępu
                    badge_copy = badge_info.copy()
                    badge_copy['badge_id'] = badge_id
                    badge_copy['progress'] = progress_info['progress']
                    badge_copy['priority_score'] = progress_info['progress']
                    easy_badges.append(badge_copy)
        
        # Sortuj według postępu
        easy_badges.sort(key=lambda x: x['progress'], reverse=True)
        
        return easy_badges[:limit]
    
    def _calculate_category_progress(self, category_badges: List[str], badge_data: Dict[str, Any]) -> Dict[str, Any]:
        """Oblicz postęp w kategorii"""
        earned_in_category = [badge_id for badge_id in category_badges 
                             if badge_data['badges'].get(badge_id, {}).get('earned', False)]
        
        progress_percentage = (len(earned_in_category) / len(category_badges) * 100) if category_badges else 0
        
        # Znajdź następną odznakę do zdobycia
        next_badge = None
        for badge_id in category_badges:
            if badge_id not in earned_in_category:
                progress_info = badge_data['badge_progress'].get(badge_id, {})
                if progress_info.get('progress', 0) > 0:
                    next_badge = {
                        'badge_id': badge_id,
                        'name': BADGES[badge_id]['name'],
                        'progress': progress_info['progress']
                    }
                    break
        
        # Jeśli brak w toku, weź pierwszą dostępną
        if not next_badge and len(earned_in_category) < len(category_badges):
            remaining_badges = [bid for bid in category_badges if bid not in earned_in_category]
            if remaining_badges:
                badge_id = remaining_badges[0]
                next_badge = {
                    'badge_id': badge_id,
                    'name': BADGES[badge_id]['name'],
                    'progress': 0
                }
        
        return {
            'earned': len(earned_in_category),
            'total': len(category_badges),
            'percentage': progress_percentage,
            'next_badge': next_badge,
            'badges': {
                'earned': earned_in_category,
                'remaining': [bid for bid in category_badges if bid not in earned_in_category]
            }
        }
    
    def _generate_earning_timeline(self, badge_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Wygeneruj timeline zdobytych odznak"""
        earned_badges = badge_data['badges']
        
        timeline = []
        for badge_id, badge_info in earned_badges.items():
            if badge_info.get('earned', False):
                timeline.append({
                    'badge_id': badge_id,
                    'name': BADGES[badge_id]['name'],
                    'tier': badge_info.get('tier', 'bronze'),
                    'xp_earned': badge_info.get('xp_earned', 0),
                    'earned_date': badge_info.get('earned_date'),
                    'category': BADGES[badge_id].get('category', 'unknown')
                })
        
        # Sortuj według daty zdobycia
        timeline.sort(key=lambda x: x['earned_date'] or '', reverse=True)
        
        return timeline[:10]  # Ostatnie 10
    
    def _generate_category_breakdown(self, badge_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Wygeneruj rozbicie według kategorii"""
        breakdown = {}
        
        for category_id, category_info in BADGE_CATEGORIES.items():
            category_badges = [badge_id for badge_id, badge_info in BADGES.items() 
                             if badge_info.get('category') == category_id]
            
            earned_in_category = [badge_id for badge_id in category_badges 
                                if badge_data['badges'].get(badge_id, {}).get('earned', False)]
            
            breakdown[category_id] = {
                'name': category_info['name'],
                'total_badges': len(category_badges),
                'earned_badges': len(earned_in_category),
                'completion_percentage': (len(earned_in_category) / len(category_badges) * 100) if category_badges else 0,
                'total_xp': sum(badge_data['badges'][bid].get('xp_earned', 0) for bid in earned_in_category),
                'badges': earned_in_category
            }
        
        return breakdown
    
    def _generate_tier_distribution(self, badge_data: Dict[str, Any]) -> Dict[str, int]:
        """Wygeneruj rozkład według tier"""
        distribution = {tier: 0 for tier in ['bronze', 'silver', 'gold', 'platinum', 'diamond']}
        
        for badge_info in badge_data['badges'].values():
            if badge_info.get('earned', False):
                tier = badge_info.get('tier', 'bronze')
                distribution[tier] = distribution.get(tier, 0) + 1
        
        return distribution
    
    def _generate_recent_badge_activity(self, badge_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Wygeneruj ostatnią aktywność odznak"""
        recent_activity = []
        
        # Ostatnio zdobyte odznaki
        earned_badges = [(badge_id, badge_info) for badge_id, badge_info in badge_data['badges'].items()
                        if badge_info.get('earned', False)]
        
        earned_badges.sort(key=lambda x: x[1].get('earned_date', ''), reverse=True)
        
        for badge_id, badge_info in earned_badges[:5]:
            recent_activity.append({
                'type': 'earned',
                'badge_id': badge_id,
                'name': BADGES[badge_id]['name'],
                'date': badge_info.get('earned_date'),
                'xp_earned': badge_info.get('xp_earned', 0)
            })
        
        return recent_activity
    
    def _generate_achievement_insights(self, badge_data: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Wygeneruj insights o osiągnięciach"""
        insights = {
            'completion_rate': 0,
            'favorite_category': None,
            'strongest_area': None,
            'improvement_suggestions': []
        }
        
        total_badges = len(BADGES)
        earned_badges = len(badge_data['badges'])
        insights['completion_rate'] = (earned_badges / total_badges * 100) if total_badges > 0 else 0
        
        # Znajdź ulubioną kategorię
        category_counts = {}
        for badge_id in badge_data['badges'].keys():
            category = BADGES[badge_id].get('category', 'unknown')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        if category_counts:
            insights['favorite_category'] = max(category_counts, key=category_counts.get)
        
        # Sugestie poprawy
        if insights['completion_rate'] < 25:
            insights['improvement_suggestions'].append("Skoncentruj się na podstawowych odznakach")
        elif insights['completion_rate'] < 50:
            insights['improvement_suggestions'].append("Spróbuj ukończyć całą kategorię")
        else:
            insights['improvement_suggestions'].append("Idź po najwyższe tier!")
        
        return insights
    
    def _generate_performance_metrics(self, badge_data: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Wygeneruj metryki wydajności"""
        joined_date = user_data.get('joined_date')
        if not joined_date:
            return {}
        
        try:
            join_date = datetime.strptime(joined_date, '%Y-%m-%d')
            days_since_join = (datetime.now() - join_date).days
            
            earned_badges = len(badge_data['badges'])
            earning_rate = earned_badges / max(days_since_join, 1)
            
            return {
                'days_since_join': days_since_join,
                'badges_per_day': round(earning_rate, 2),
                'total_badge_xp': badge_data['badge_stats']['total_badge_xp'],
                'average_xp_per_badge': round(badge_data['badge_stats']['total_badge_xp'] / max(earned_badges, 1), 1)
            }
        except:
            return {}
    
    def _calculate_leaderboard_score(self, username: str, user_data: Dict[str, Any], category: Optional[str]) -> Dict[str, Any]:
        """Oblicz wynik dla leaderboard"""
        badge_data = self.get_user_badge_data(username)
        
        # Filtruj według kategorii jeśli podana
        if category:
            relevant_badges = {badge_id: badge_info for badge_id, badge_info in badge_data['badges'].items()
                             if BADGES.get(badge_id, {}).get('category') == category}
        else:
            relevant_badges = badge_data['badges']
        
        total_badges = len(relevant_badges)
        badge_xp = sum(badge.get('xp_earned', 0) for badge in relevant_badges.values())
        
        # Oblicz wynik łączny (XP + bonus za liczbę odznak)
        total_score = badge_xp + (total_badges * 10)
        
        # Znajdź najwyższy tier
        tiers = [badge.get('tier', 'bronze') for badge in relevant_badges.values()]
        tier_order = ['bronze', 'silver', 'gold', 'platinum', 'diamond']
        highest_tier_index = max((tier_order.index(tier) for tier in tiers if tier in tier_order), default=0)
        highest_tier = tier_order[highest_tier_index] if tiers else 'none'
        
        # Ukończone kategorie
        completed_categories = badge_data['badge_stats']['categories_completed']
        if category:
            completed_categories = [cat for cat in completed_categories if cat == category]
        
        # Ostatnie odznaki
        recent_badges = sorted(
            relevant_badges.items(),
            key=lambda x: x[1].get('earned_date', ''),
            reverse=True
        )[:3]
        
        return {
            'total_badges': total_badges,
            'badge_xp': badge_xp,
            'total_score': total_score,
            'highest_tier': highest_tier,
            'categories_completed': len(completed_categories),
            'recent_badges': [{'badge_id': bid, 'name': BADGES[bid]['name']} 
                            for bid, _ in recent_badges]
        }
    
    def _get_badge_tips(self, badge_id: str, progress_info: Dict[str, Any]) -> List[str]:
        """Pobierz wskazówki dla konkretnej odznaki"""
        tips = []
        
        badge_info = BADGES.get(badge_id, {})
        category = badge_info.get('category', '')
        
        # Ogólne wskazówki według kategorii
        if category == 'getting_started':
            tips.append("Te odznaki są podstawą - skup się na ukończeniu profilu i pierwszych krokach")
        elif category == 'learning_progress':
            tips.append("Regularnie ukończaj lekcje aby zdobywać odznaki z tej kategorii")
        elif category == 'engagement':
            tips.append("Bądź aktywny codziennie - loguj się regularnie i wykonuj zadania")
        elif category == 'expertise':
            tips.append("Pogłębiaj wiedzę w konkretnych obszarach dla specjalistycznych odznak")
        
        # Specyficzne wskazówki dla konkretnych odznak
        if badge_id == 'speed_learner':
            tips.append("Spróbuj ukończyć 3 lekcje w jeden dzień")
        elif badge_id == 'night_owl':
            tips.append("Ucz się po godzinie 22:00 aby zdobyć tę odznakę")
        elif badge_id == 'weekend_scholar':
            tips.append("Znajdź czas na naukę w weekend")
        elif 'quiz' in badge_id:
            tips.append("Skoncentruj się na dokładnych odpowiedziach w quizach")
        
        return tips

# ==========================================
# GLOBALNA INSTANCJA
# ==========================================

# Utworz globalną instancję dla łatwego dostępu
badge_tracker = BadgeTracker()

# ==========================================
# FUNKCJE KOMPATYBILNOŚCI
# ==========================================

def track_badge_progress(username: str, context: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
    """
    Funkcja kompatybilności dla śledzenia postępu odznak
    
    Args:
        username: Nazwa użytkownika
        context: Kontekst wywołania
        **kwargs: Dodatkowe dane kontekstowe
    
    Returns:
        Dict z informacjami o aktualizacji
    """
    return badge_tracker.update_badge_progress(username, context, **kwargs)

def get_user_badges(username: str) -> Dict[str, Any]:
    """
    Funkcja kompatybilności dla pobierania odznak użytkownika
    
    Args:
        username: Nazwa użytkownika
    
    Returns:
        Dict z danymi odznak użytkownika
    """
    return badge_tracker.get_user_badge_data(username)

def get_badge_recommendations(username: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Funkcja kompatybilności dla rekomendacji odznak
    
    Args:
        username: Nazwa użytkownika
        limit: Maksymalna liczba rekomendacji
    
    Returns:
        Lista rekomendowanych odznak
    """
    return badge_tracker.get_recommended_badges(username, limit)
