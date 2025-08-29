"""
Moduł do analizy wyników autodiagnozy i rekomendacji szkoleń w systemie BVA
"""

import streamlit as st
from typing import Dict, List, Tuple
import json

class TrainingRecommendationEngine:
    """Klasa do analizy wyników autodiagnozy i generowania rekomendacji szkoleń"""
    
    def __init__(self):
        # Mapowanie pytań z autodiagnozy na obszary rozwoju i związane z nimi szkolenia
        self.question_mapping = {
            1: {  # Kontrolowanie emocji w stresie
                "area": "Zarządzanie emocjami",
                "key_skills": ["kontrola emocji", "zarządzanie stresem", "podejmowanie decyzji pod presją"],
                "recommended_trainings": [
                    {
                        "title": "Mózg emocjonalny",
                        "lesson_id": "1",
                        "priority": "wysoky",
                        "description": "Poznaj neurobiologię emocji i naucz się efektywnie zarządzać swoimi reakcjami emocjonalnymi",
                        "focus_areas": ["neurobiologia emocji", "techniki kontroli emocjonalnej", "wpływ stresu na decyzje"]
                    },
                    {
                        "title": "Techniki zarządzania stresem w przywództwie",
                        "lesson_id": "advanced_stress",
                        "priority": "średni",
                        "description": "Praktyczne narzędzia do radzenia sobie ze stresem w roli lidera",
                        "focus_areas": ["techniki relaksacyjne", "mindfulness dla liderów", "budowanie odporności"]
                    }
                ]
            },
            2: {  # Rola neurotransmiterów w motywowaniu
                "area": "Chemia motywacji",
                "key_skills": ["neurobiologia motywacji", "budowanie zaangażowania zespołu", "system nagród"],
                "recommended_trainings": [
                    {
                        "title": "Chemia mózgu",
                        "lesson_id": "2",
                        "priority": "wysoki",
                        "description": "Zrozum jak neurotransmitery wpływają na motywację i zaangażowanie pracowników",
                        "focus_areas": ["dopamina i motywacja", "serotonina i zadowolenie", "system nagród mózgu"]
                    },
                    {
                        "title": "Budowanie kultury wysokiego zaangażowania",
                        "lesson_id": "engagement_culture",
                        "priority": "średni",
                        "description": "Praktyczne strategie zwiększania zaangażowania zespołu",
                        "focus_areas": ["psychologia motywacji", "system incentives", "kultura organizacyjna"]
                    }
                ]
            },
            3: {  # Model SCARF - 5 podstawowych potrzeb mózgu
                "area": "Potrzeby społeczne mózgu",
                "key_skills": ["model SCARF", "zarządzanie potrzebami zespołu", "komunikacja świadoma mózgu"],
                "recommended_trainings": [
                    {
                        "title": "Model SCARF",
                        "lesson_id": "3",
                        "priority": "krytyczny",
                        "description": "Opanuj fundamentalny model 5 potrzeb społecznych mózgu: Status, Certainty, Autonomy, Relatedness, Fairness",
                        "focus_areas": ["5 potrzeb SCARF", "praktyczne zastosowania", "komunikacja SCARF-aware"]
                    },
                    {
                        "title": "Komunikacja uwzględniająca potrzeby mózgu",
                        "lesson_id": "brain_aware_communication",
                        "priority": "wysoki",
                        "description": "Naucz się komunikować w sposób, który wspiera a nie zagraża podstawowym potrzebom mózgu",
                        "focus_areas": ["komunikacja bezpieczna dla mózgu", "feedback bez zagrożeń", "budowanie zaufania"]
                    }
                ]
            },
            4: {  # Model SEEDS - pozytywne środowisko pracy
                "area": "Środowisko pracy przyjazne mózgowi",
                "key_skills": ["model SEEDS", "budowanie bezpiecznego środowiska", "kultura psychologicznego bezpieczeństwa"],
                "recommended_trainings": [
                    {
                        "title": "Model SEEDS",
                        "lesson_id": "4",
                        "priority": "wysoki",
                        "description": "Zbuduj pozytywne środowisko pracy wykorzystując model SEEDS: Bezpieczeństwo, Emocje, Eksploracja, Społeczność",
                        "focus_areas": ["bezpieczeństwo psychologiczne", "zarządzanie emocjami zespołu", "kultura innowacji"]
                    },
                    {
                        "title": "Budowanie zespołów wysokiej wydajności",
                        "lesson_id": "high_performance_teams",
                        "priority": "średni",
                        "description": "Praktyczne narzędzia tworzenia zespołów o wysokiej wydajności i zaangażowaniu",
                        "focus_areas": ["dynamika zespołu", "psychological safety", "efektywna współpraca"]
                    }
                ]
            },
            5: {  # Zarządzanie stresem i odporność psychiczna
                "area": "Odporność i zarządzanie stresem",
                "key_skills": ["zarządzanie stresem", "budowanie odporności", "wellbeing zespołu"],
                "recommended_trainings": [
                    {
                        "title": "Neurobiologia stresu i odporności",
                        "lesson_id": "stress_resilience",
                        "priority": "wysoki",
                        "description": "Poznaj mechanizmy stresu w mózgu i naucz się budować odporność psychiczną",
                        "focus_areas": ["fizjologia stresu", "techniki odprężenia", "budowanie rezyliencji"]
                    },
                    {
                        "title": "Wellbeing w miejscu pracy",
                        "lesson_id": "workplace_wellbeing",
                        "priority": "średni",
                        "description": "Strategie tworzenia zdrowszego i bardziej zrównoważonego środowiska pracy",
                        "focus_areas": ["work-life balance", "profilaktyka wypalenia", "zdrowie mentalne"]
                    }
                ]
            },
            6: {  # Procesy podejmowania decyzji
                "area": "Neurobiologia decyzji",
                "key_skills": ["podejmowanie decyzji", "zarządzanie ryzykiem", "myślenie strategiczne"],
                "recommended_trainings": [
                    {
                        "title": "Mózg strategiczny - podejmowanie decyzji",
                        "lesson_id": "strategic_brain",
                        "priority": "wysoki",
                        "description": "Zrozum jak mózg podejmuje decyzje i naucz się optymalizować ten proces",
                        "focus_areas": ["neurobiologia decyzji", "cognitive biases", "analiza ryzyka"]
                    },
                    {
                        "title": "Myślenie krytyczne dla liderów",
                        "lesson_id": "critical_thinking",
                        "priority": "średni",
                        "description": "Rozwiń umiejętności krytycznego myślenia i analizy strategicznej",
                        "focus_areas": ["analiza problemów", "myślenie systemowe", "podejmowanie decyzji grupowych"]
                    }
                ]
            },
            7: {  # Koncentracja, pamięć, zdolności poznawcze
                "area": "Funkcje poznawcze",
                "key_skills": ["koncentracja", "pamięć", "funkcje wykonawcze", "produktywność poznawcza"],
                "recommended_trainings": [
                    {
                        "title": "Optymalizacja funkcji poznawczych",
                        "lesson_id": "cognitive_optimization",
                        "priority": "średni",
                        "description": "Naucz się jak poprawić koncentrację, pamięć i inne funkcje poznawcze",
                        "focus_areas": ["neurobiologia uwagi", "techniki pamięciowe", "zarządzanie energią mentalną"]
                    },
                    {
                        "title": "Produktywność oparta na neuronaukach",
                        "lesson_id": "neuroscience_productivity",
                        "priority": "średni",
                        "description": "Wykorzystaj wiedzę o mózgu do zwiększenia swojej produktywności i efektywności",
                        "focus_areas": ["zarządzanie czasem", "deep work", "optymalizacja wydajności"]
                    }
                ]
            },
            8: {  # Zdrowie i wydajność mózgu
                "area": "Zdrowie mózgu",
                "key_skills": ["neuroplastyczność", "zdrowie mózgu", "lifestyle dla mózgu"],
                "recommended_trainings": [
                    {
                        "title": "Zdrowie mózgu dla liderów",
                        "lesson_id": "brain_health",
                        "priority": "średni",
                        "description": "Poznaj czynniki wpływające na zdrowie i wydajność mózgu",
                        "focus_areas": ["sen i mózg", "nutrition dla mózgu", "aktywność fizyczna"]
                    },
                    {
                        "title": "Neuroplastyczność w praktyce",
                        "lesson_id": "neuroplasticity_practice",
                        "priority": "niski",
                        "description": "Wykorzystaj zdolność mózgu do zmiany dla rozwoju osobistego i zawodowego",
                        "focus_areas": ["nauka przez całe życie", "adaptacja do zmian", "rozwój mózgu"]
                    }
                ]
            },
            9: {  # Neuroplastyczność i zmiana nawyków
                "area": "Zmiana i rozwój",
                "key_skills": ["neuroplastyczność", "zmiana nawyków", "coaching rozwojowy"],
                "recommended_trainings": [
                    {
                        "title": "Neuroplastyczność w praktyce",
                        "lesson_id": "neuroplasticity_practice",
                        "priority": "wysoki",
                        "description": "Wykorzystaj zdolność mózgu do zmiany dla kształtowania nowych nawyków i zachowań",
                        "focus_areas": ["mechanizmy zmiany", "budowanie nawyków", "coaching oparty na neuronaukach"]
                    },
                    {
                        "title": "Coaching neurobiologiczny",
                        "lesson_id": "neurobiological_coaching",
                        "priority": "średni",
                        "description": "Naucz się coachingu opartego na najnowszych odkryciach neuronaukowych",
                        "focus_areas": ["brain-based coaching", "zmiana zachowań", "rozwój potencjału"]
                    }
                ]
            },
            10: {  # Zastosowanie wiedzy o mózgu w kluczowych wyzwaniach
                "area": "Zastosowania praktyczne",
                "key_skills": ["neuroprzywództwo", "zastosowania praktyczne", "integracja wiedzy"],
                "recommended_trainings": [
                    {
                        "title": "Zaawansowane neuroprzywództwo",
                        "lesson_id": "advanced_neuroleadership",
                        "priority": "wysoki",
                        "description": "Zintegruj wiedzę o mózgu w codziennych wyzwaniach menedżerskich",
                        "focus_areas": ["motywowanie zespołu", "zarządzanie zmianą", "rozwój pracowników"]
                    },
                    {
                        "title": "Neuroprzywództwo w praktyce - case studies",
                        "lesson_id": "neuroleadership_cases",
                        "priority": "średni",
                        "description": "Analizuj rzeczywiste przypadki zastosowania neuroprzywództwa w organizacjach",
                        "focus_areas": ["studia przypadków", "best practices", "implementacja w organizacji"]
                    }
                ]
            }
        }
    
    def analyze_autodiagnosis_results(self, quiz_results: Dict) -> Dict:
        """
        Analizuje wyniki autodiagnozy i generuje rekomendacje szkoleń
        
        Args:
            quiz_results: Wyniki quizu autodiagnozy (answers, completion_date, itp.)
            
        Returns:
            Dict z analizą i rekomendacjami
        """
        if 'answers' not in quiz_results:
            return {
                'error': 'Brak danych odpowiedzi w wynikach autodiagnozy',
                'recommendations': []
            }
        
        answers = quiz_results['answers']
        
        # Analizuj odpowiedzi (zakładając skalę 1-5 gdzie 5 = bardzo ważne)
        priority_areas = []
        
        for i, answer in enumerate(answers):
            question_num = i + 1
            score = int(answer) if isinstance(answer, (int, float, str)) else 3
            
            if question_num in self.question_mapping:
                area_data = self.question_mapping[question_num]
                
                # Im wyższy wynik (4-5), tym większy priorytet tego obszaru
                if score >= 4:
                    priority_level = "krytyczny" if score == 5 else "wysoki"
                    priority_areas.append({
                        'question_id': question_num,
                        'score': score,
                        'priority': priority_level,
                        'area': area_data['area'],
                        'key_skills': area_data['key_skills'],
                        'trainings': area_data['recommended_trainings']
                    })
                elif score == 3:
                    priority_areas.append({
                        'question_id': question_num,
                        'score': score,
                        'priority': "średni",
                        'area': area_data['area'],
                        'key_skills': area_data['key_skills'],
                        'trainings': area_data['recommended_trainings']
                    })
        
        # Sortuj według priorytetu (krytyczny > wysoki > średni)
        priority_order = {"krytyczny": 3, "wysoki": 2, "średni": 1, "niski": 0}
        priority_areas.sort(key=lambda x: (priority_order.get(x['priority'], 0), x['score']), reverse=True)
        
        # Generuj rekomendacje
        recommendations = self._generate_training_recommendations(priority_areas)
        
        return {
            'priority_areas': priority_areas,
            'recommendations': recommendations,
            'analysis_summary': self._generate_analysis_summary(priority_areas)
        }
    
    def _generate_training_recommendations(self, priority_areas: List[Dict]) -> List[Dict]:
        """Generuje listę rekomendowanych szkoleń na podstawie analizy priorytetów"""
        
        all_trainings = []
        seen_trainings = set()
        
        for area in priority_areas:
            for training in area['trainings']:
                training_key = training['lesson_id']
                
                if training_key not in seen_trainings:
                    # Dodaj informacje o priorytecie z obszaru
                    enhanced_training = training.copy()
                    enhanced_training['area_priority'] = area['priority']
                    enhanced_training['area_score'] = area['score']
                    enhanced_training['related_area'] = area['area']
                    
                    all_trainings.append(enhanced_training)
                    seen_trainings.add(training_key)
        
        # Sortuj według priorytetu obszaru i własnego priorytetu szkolenia
        priority_order = {"krytyczny": 3, "wysoki": 2, "średni": 1, "niski": 0}
        
        all_trainings.sort(
            key=lambda x: (
                priority_order.get(x['area_priority'], 0),
                priority_order.get(x['priority'], 0),
                x['area_score']
            ),
            reverse=True
        )
        
        return all_trainings
    
    def _generate_analysis_summary(self, priority_areas: List[Dict]) -> Dict:
        """Generuje podsumowanie analizy wyników autodiagnozy"""
        
        total_areas = len(priority_areas)
        critical_areas = len([a for a in priority_areas if a['priority'] == 'krytyczny'])
        high_areas = len([a for a in priority_areas if a['priority'] == 'wysoki'])
        medium_areas = len([a for a in priority_areas if a['priority'] == 'średni'])
        
        # Znajdź obszar z najwyższym priorytetem
        top_area = priority_areas[0] if priority_areas else None
        
        return {
            'total_identified_areas': total_areas,
            'critical_priority_areas': critical_areas,
            'high_priority_areas': high_areas,
            'medium_priority_areas': medium_areas,
            'top_priority_area': top_area['area'] if top_area else None,
            'recommended_focus': self._get_focus_recommendation(critical_areas, high_areas, medium_areas)
        }
    
    def _get_focus_recommendation(self, critical: int, high: int, medium: int) -> str:
        """Generuje rekomendację dotyczącą skupienia się na rozwoju"""
        
        if critical > 0:
            return f"Masz {critical} obszar(ów) krytycznych - skup się najpierw na nich, aby uzyskać największy wpływ na swoją efektywność jako lidera."
        elif high >= 3:
            return f"Masz {high} obszarów wysokiego priorytetu - zalecamy systematyczne podejście, zaczynając od 1-2 obszarów."
        elif high > 0:
            return f"Masz {high} obszar(ów) wysokiego priorytetu - to dobry punkt startowy dla Twojego rozwoju."
        elif medium > 0:
            return f"Masz {medium} obszar(ów) średniego priorytetu - możesz rozwijać się w nich stopniowo, według własnych preferencji."
        else:
            return "Twoje odpowiedzi wskazują na niski priorytet dla wszystkich obszarów neuroprzywództwa. Może warto ponownie przeanalizować swoje potrzeby rozwojowe?"


def display_training_recommendations(lesson_id: str, quiz_results_key: str):
    """
    Wyświetla rekomendacje szkoleń na podstawie wyników autodiagnozy
    
    Args:
        lesson_id: ID lekcji
        quiz_results_key: Klucz do wyników quizu w session_state.user_data
    """
    
    st.markdown("### 🎯 Spersonalizowane rekomendacje szkoleń")
    
    # Sprawdź czy są dostępne wyniki autodiagnozy
    if 'user_data' not in st.session_state or quiz_results_key not in st.session_state.user_data:
        st.warning("❗ Aby otrzymać spersonalizowane rekomendacje szkoleń, najpierw ukończ quiz autodiagnozy.")
        return
    
    quiz_results = st.session_state.user_data[quiz_results_key]
    
    # Inicjalizuj engine rekomendacji
    recommendation_engine = TrainingRecommendationEngine()
    
    # Analizuj wyniki
    with st.spinner("🤖 Analizuję Twoje wyniki i przygotowuję spersonalizowane rekomendacje..."):
        analysis = recommendation_engine.analyze_autodiagnosis_results(quiz_results)
    
    if 'error' in analysis:
        st.error(f"Błąd podczas analizy: {analysis['error']}")
        return
    
    # Wyświetl podsumowanie analizy
    summary = analysis['analysis_summary']
    
    st.markdown("#### 📊 Podsumowanie Twojego profilu rozwojowego")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Zidentyfikowane obszary", summary['total_identified_areas'])
    with col2:
        st.metric("Priorytet krytyczny", summary['critical_priority_areas'])
    with col3:
        st.metric("Priorytet wysoki", summary['high_priority_areas'])
    with col4:
        st.metric("Priorytet średni", summary['medium_priority_areas'])
    
    if summary['top_priority_area']:
        st.info(f"🎯 **Twój główny obszar rozwoju:** {summary['top_priority_area']}")
    
    if summary['recommended_focus']:
        st.markdown(f"**💡 Rekomendacja:** {summary['recommended_focus']}")
    
    st.markdown("---")
    
    # Wyświetl rekomendowane szkolenia
    recommendations = analysis['recommendations']
    
    if not recommendations:
        st.info("Na podstawie Twoich odpowiedzi nie zidentyfikowaliśmy obszarów wymagających natychmiastowego rozwoju. To świetnie! Możesz kontynuować naukę według własnych zainteresowań.")
        return
    
    st.markdown("#### 🎓 Rekomendowane szkolenia (uporządkowane według priorytetów)")
    
    for i, training in enumerate(recommendations[:8], 1):  # Pokaż maksymalnie 8 najważniejszych
        priority_color = {
            "krytyczny": "🔴",
            "wysoki": "🟠", 
            "średni": "🟡",
            "niski": "🟢"
        }
        
        color = priority_color.get(training['priority'], "⚪")
        
        with st.expander(f"{color} **{i}. {training['title']}** (Priorytet: {training['priority']})", expanded=i <= 3):
            st.markdown(f"**Obszar rozwoju:** {training['related_area']}")
            st.markdown(f"**Opis:** {training['description']}")
            
            st.markdown("**Główne tematy:**")
            for focus_area in training['focus_areas']:
                st.markdown(f"• {focus_area}")
            
            # Sprawdź czy szkolenie jest dostępne
            available_lessons = ["1", "2", "3", "4", "5"]  # ID dostępnych lekcji
            
            if training['lesson_id'] in available_lessons:
                st.success("✅ Szkolenie dostępne w systemie")
                if st.button(f"📚 Przejdź do szkolenia: {training['title']}", key=f"goto_training_{training['lesson_id']}"):
                    # Przekieruj do odpowiedniej lekcji
                    st.session_state.current_lesson_id = training['lesson_id']
                    st.session_state.lesson_step = 'intro'
                    st.rerun()
            else:
                st.info("⏳ Szkolenie w przygotowaniu - będzie dostępne wkrótce")
    
    # Pokaż szczegóły analizy obszarów
    if st.checkbox("🔍 Pokaż szczegółową analizę obszarów rozwoju"):
        st.markdown("#### 📈 Szczegółowa analiza Twoich obszarów rozwoju")
        
        for area in analysis['priority_areas']:
            priority_emoji = {"krytyczny": "🔴", "wysoki": "🟠", "średni": "🟡"}
            emoji = priority_emoji.get(area['priority'], "⚪")
            
            st.markdown(f"**{emoji} {area['area']}** (Twoja ocena: {area['score']}/5)")
            st.markdown(f"*Kluczowe umiejętności:* {', '.join(area['key_skills'])}")
            st.markdown("---")
    
    # Zapisz rekomendacje w session_state dla przyszłego użytku
    recommendations_key = f"training_recommendations_{lesson_id}"
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    st.session_state.user_data[recommendations_key] = {
        'analysis': analysis,
        'generated_date': quiz_results.get('completion_date', 'unknown'),
        'based_on_quiz': quiz_results_key
    }


# Style CSS dla rekomendacji
def load_recommendations_styles():
    """Ładuje style CSS dla sekcji rekomendacji"""
    
    st.markdown("""
    <style>
    .recommendation-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 5px solid #28a745;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.1);
    }
    
    .priority-critical {
        border-left-color: #dc3545 !important;
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
    }
    
    .priority-high {
        border-left-color: #fd7e14 !important;
        background: linear-gradient(135deg, #fff8f0 0%, #feebc8 100%);
    }
    
    .priority-medium {
        border-left-color: #ffc107 !important;
        background: linear-gradient(135deg, #fffbf0 0%, #fef5e7 100%);
    }
    
    .training-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #007bff;
    }
    </style>
    """, unsafe_allow_html=True)
