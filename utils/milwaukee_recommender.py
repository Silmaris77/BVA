"""
Milwaukee Application Recommender
Logika dopasowania kontekstu klienta do aplikacji i produktów
"""

import json
import os
from typing import Dict, List, Tuple, Any

# Ścieżki do plików danych
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'milwaukee')
APPLICATIONS_FILE = os.path.join(DATA_DIR, 'applications.json')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products_ecosystem.json')
QUESTIONS_FILE = os.path.join(DATA_DIR, 'discovery_questions.json')


class MilwaukeeRecommender:
    """Silnik rekomendacji Application First"""
    
    def __init__(self):
        self.applications = self._load_json(APPLICATIONS_FILE)
        self.products = self._load_json(PRODUCTS_FILE)
        self.questions = self._load_json(QUESTIONS_FILE)
    
    def _load_json(self, filepath: str) -> Dict:
        """Załaduj plik JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return {}
    
    def match_application(self, context: Dict[str, Any]) -> List[Tuple[str, float, str]]:
        """
        Dopasuj aplikacje do kontekstu klienta
        
        Args:
            context: Dict z kluczami: typ_klienta, typ_pracy, materialy_srodowisko, skala
            
        Returns:
            List[(application_id, match_score, reason)]
        """
        matches = []
        
        for app_id, app_data in self.applications.get('applications', {}).items():
            app_context = app_data.get('context', {})
            score = 0.0
            reasons = []
            
            # Matching typ_klienta (40% wagi)
            if context.get('typ_klienta'):
                if context['typ_klienta'].lower() in app_context.get('typ_klienta', '').lower():
                    score += 40
                    reasons.append(f"Profil klienta: {app_context.get('typ_klienta')}")
            
            # Matching typ_pracy (25% wagi)
            if context.get('typ_pracy'):
                if context['typ_pracy'].lower() in app_context.get('typ_pracy', '').lower():
                    score += 25
                    reasons.append(f"Typ pracy: {app_context.get('typ_pracy')}")
            
            # Matching materiały/środowisko (25% wagi)
            if context.get('materialy_srodowisko'):
                context_materials = [m.lower() for m in context['materialy_srodowisko']]
                app_materials = [m.lower() for m in app_context.get('materialy_srodowisko', [])]
                
                overlap = len(set(context_materials) & set(app_materials))
                if overlap > 0:
                    material_score = (overlap / len(context_materials)) * 25
                    score += material_score
                    reasons.append(f"Materiały: {', '.join(app_context.get('materialy_srodowisko', []))}")
            
            # Matching skala (10% wagi)
            if context.get('skala'):
                if context['skala'].lower() in app_context.get('skala', '').lower():
                    score += 10
                    reasons.append(f"Skala: {app_context.get('skala')}")
            
            if score > 30:  # Threshold dla rekomendacji
                matches.append((app_id, score, " | ".join(reasons)))
        
        # Sortuj po score malejąco
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    def get_application_details(self, app_id: str) -> Dict:
        """Pobierz pełne detale aplikacji"""
        return self.applications.get('applications', {}).get(app_id, {})
    
    def get_discovery_questions(self, typ_klienta: str) -> List[Dict]:
        """Pobierz pytania pogłębiające dla danego typu klienta"""
        # Mapowanie typ_klienta na klucze w discovery_questions
        mapping = {
            'hydraulik': 'hydraulik',
            'warsztat': 'warsztat',
            'serwis_mobilny': 'serwis_mobilny',
            'elektryk': 'elektryk',
            'stolarstwo': 'stolarstwo',
            'budowa': 'budowa'
        }
        
        key = mapping.get(typ_klienta.lower().replace(' ', '_').replace('/', '_'), 'hydraulik')
        return self.questions.get('deepening_questions', {}).get(key, [])
    
    def calculate_product_scores(self, answers: Dict[str, str]) -> Dict[str, float]:
        """
        Oblicz scoring produktów na podstawie odpowiedzi
        
        Args:
            answers: Dict {question_id: answer_value}
            
        Returns:
            Dict {product_sku: score}
        """
        scores = {}
        
        # Iteruj po wszystkich odpowiedziach
        for question_id, answer in answers.items():
            # Znajdź pytanie w bazie
            for typ_klienta, questions_list in self.questions.get('deepening_questions', {}).items():
                for q in questions_list:
                    if q.get('id') == question_id:
                        # Pobierz scoring dla tej odpowiedzi
                        question_scoring = q.get('scoring', {})
                        answer_scoring = question_scoring.get(answer, {})
                        
                        # Dodaj punkty do produktów
                        for product_key, points in answer_scoring.items():
                            if product_key not in ['roi_low', 'roi_medium', 'roi_high', 'roi_critical',
                                                   'ergonomia', 'kompakt', 'baterie_extra', 'baterie_count',
                                                   'education', 'planning', 'upgrade', 'upgrade_check',
                                                   'current_setup_good', 'optimization', 'full_ecosystem',
                                                   'productivity_gain', 'backup_tools', 'tools_other']:
                                scores[product_key] = scores.get(product_key, 0) + points
        
        return scores
    
    def build_recommendation_package(self, app_id: str, product_scores: Dict[str, float] = None) -> Dict:
        """
        Zbuduj pakiet rekomendacji dla aplikacji
        
        Args:
            app_id: ID aplikacji
            product_scores: Opcjonalne scoring z pytań pogłębiających
            
        Returns:
            Dict z rekomendacjami (narzędzia, baterie, akcesoria, organizacja, PPE)
        """
        app_data = self.get_application_details(app_id)
        if not app_data:
            return {}
        
        ecosystem = app_data.get('recommended_ecosystem', {})
        products_data = self.products.get('products', {})
        
        package = {
            'narzedzia': [],
            'baterie': [],
            'akcesoria': [],
            'organizacja': [],
            'ppe': [],
            'total_price': 0
        }
        
        # Narzędzia
        for tool in ecosystem.get('narzedzia', []):
            sku = tool.get('sku')
            product_info = products_data.get(sku, {})
            package['narzedzia'].append({
                'sku': sku,
                'name': product_info.get('full_name', sku),
                'price': product_info.get('price_pln', 0),
                'reason': tool.get('reason', ''),
                'priority': tool.get('priority', 999),
                'features': product_info.get('key_features', []),
                'benefits': product_info.get('benefits', [])
            })
            package['total_price'] += product_info.get('price_pln', 0)
        
        # Baterie
        for battery in ecosystem.get('baterie', []):
            sku = battery.get('sku')
            quantity = battery.get('quantity', 1)
            product_info = products_data.get(sku, {})
            price = product_info.get('price_pln', 0) * quantity
            
            package['baterie'].append({
                'sku': sku,
                'name': product_info.get('full_name', sku),
                'price': price,
                'quantity': quantity,
                'reason': battery.get('reason', ''),
                'features': product_info.get('key_features', [])
            })
            package['total_price'] += price
        
        # Akcesoria
        for accessory in ecosystem.get('akcesoria', []):
            sku = accessory.get('sku')
            product_info = products_data.get(sku, {})
            package['akcesoria'].append({
                'sku': sku,
                'name': product_info.get('full_name', sku),
                'price': product_info.get('price_pln', 0),
                'reason': accessory.get('reason', ''),
                'features': product_info.get('key_features', [])
            })
            package['total_price'] += product_info.get('price_pln', 0)
        
        # Organizacja (PACKOUT)
        for org in ecosystem.get('organizacja', []):
            sku = org.get('sku')
            product_info = products_data.get(sku, {})
            package['organizacja'].append({
                'sku': sku,
                'name': product_info.get('full_name', sku),
                'price': product_info.get('price_pln', 0),
                'reason': org.get('reason', ''),
                'features': product_info.get('key_features', [])
            })
            package['total_price'] += product_info.get('price_pln', 0)
        
        # PPE
        for ppe in ecosystem.get('ppe_dodatki', []):
            sku = ppe.get('sku')
            product_info = products_data.get(sku, {})
            package['ppe'].append({
                'sku': sku,
                'name': product_info.get('full_name', sku),
                'price': product_info.get('price_pln', 0),
                'reason': ppe.get('reason', ''),
                'features': product_info.get('key_features', [])
            })
            package['total_price'] += product_info.get('price_pln', 0)
        
        return package
    
    def get_persuasion_script(self, app_id: str) -> Dict:
        """Pobierz skrypt perswazyjny dla aplikacji"""
        app_data = self.get_application_details(app_id)
        return app_data.get('persuasion_script', {})
    
    def get_roi_calculator(self, app_id: str) -> Dict:
        """Pobierz dane do kalkulatora ROI"""
        app_data = self.get_application_details(app_id)
        return app_data.get('roi_calculator', {})
    
    def get_case_studies(self, app_id: str) -> List[Dict]:
        """Pobierz case studies dla aplikacji"""
        app_data = self.get_application_details(app_id)
        return app_data.get('case_studies', [])
    
    def get_bundle_for_application(self, app_id: str) -> Dict:
        """Pobierz gotowy bundle dla aplikacji (jeśli istnieje)"""
        bundles = self.products.get('bundles', {})
        
        for bundle_id, bundle_data in bundles.items():
            if bundle_data.get('target_application') == app_id:
                return bundle_data
        
        return {}


# Singleton instance
_recommender_instance = None

def get_recommender() -> MilwaukeeRecommender:
    """Pobierz singleton instance recommendera"""
    global _recommender_instance
    if _recommender_instance is None:
        _recommender_instance = MilwaukeeRecommender()
    return _recommender_instance
