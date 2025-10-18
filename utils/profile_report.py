"""
Generator raportu "Kim Jestem?" - kompleksowa analiza profilu użytkownika
Integruje wyniki testów diagnostycznych i aktywność w aplikacji
"""

from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json


def collect_user_profile_data(user_data: Dict) -> Dict:
    """
    Zbiera wszystkie dane użytkownika potrzebne do raportu
    
    Returns:
        Dict z sekcjami: tests, activity, strengths, patterns
    """
    profile = {
        'tests': collect_test_results(user_data),
        'activity': collect_activity_data(user_data),
        'strengths': [],
        'patterns': {},
        'metadata': {
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'username': user_data.get('username', 'User')
        }
    }
    
    # Analiza mocnych stron
    profile['strengths'] = analyze_strengths(profile['tests'], profile['activity'])
    
    # Wzorce zachowań
    profile['patterns'] = analyze_patterns(profile['activity'])
    
    return profile


def collect_test_results(user_data: Dict) -> Dict:
    """Zbiera wyniki wszystkich testów diagnostycznych"""
    tests = {
        'completed': [],
        'kolb': None,
        'neuroleader': None,
        'mi': None
    }
    
    # Test Kolba
    if 'kolb_test' in user_data and user_data['kolb_test']:
        kolb = user_data['kolb_test']
        tests['kolb'] = {
            'style': kolb.get('dominant_style', 'Unknown'),
            'scores': kolb.get('scores', {}),
            'description': get_kolb_description(kolb.get('dominant_style', ''))
        }
        tests['completed'].append('Kolb')
    
    # Test Neuroleadera
    if 'test_scores' in user_data and user_data['test_scores']:
        scores = user_data['test_scores']
        dominant = max(scores.items(), key=lambda x: x[1])
        tests['neuroleader'] = {
            'type': dominant[0],
            'scores': scores,
            'description': get_neuroleader_description(dominant[0])
        }
        tests['completed'].append('Neuroleader')
    
    # Test MI (Multiple Intelligences)
    if 'mi_test' in user_data and user_data['mi_test']:
        mi = user_data['mi_test']
        tests['mi'] = {
            'top_3': mi.get('top_3', []),
            'all_scores': mi.get('scores', {}),
            'results': mi.get('results', mi.get('scores', {})),  # Obsłuż oba klucze
            'balance': mi.get('balance_score', 0),
            'description': get_mi_description(mi.get('top_3', []))
        }
        tests['completed'].append('MI')
    
    return tests


def collect_activity_data(user_data: Dict) -> Dict:
    """Zbiera dane o aktywności użytkownika"""
    activity = {
        'modules_completed': [],
        'modules_in_progress': [],
        'total_progress': 0,
        'tools_used': [],
        'engagement_score': 0,
        'last_active': None
    }
    
    # Postęp w modułach
    if 'progress' in user_data:
        progress = user_data['progress']
        activity['total_progress'] = progress.get('overall', 0)
        
        # Zbierz ukończone moduły
        for module, data in progress.items():
            if isinstance(data, dict) and data.get('completed', False):
                activity['modules_completed'].append(module)
            elif isinstance(data, dict) and data.get('progress', 0) > 0:
                activity['modules_in_progress'].append(module)
    
    # Użyte narzędzia (jeśli są zapisane)
    if 'tools_usage' in user_data:
        activity['tools_used'] = user_data['tools_usage']
    
    # Ostatnia aktywność
    if 'last_login' in user_data:
        activity['last_active'] = user_data['last_login']
    
    # Oblicz engagement score (0-100)
    activity['engagement_score'] = calculate_engagement_score(user_data)
    
    return activity


def analyze_strengths(tests: Dict, activity: Dict) -> List[Dict]:
    """
    Analizuje mocne strony użytkownika na podstawie testów i aktywności
    
    Returns:
        Lista słowników z mocnymi stronami: {name, source, description}
    """
    strengths = []
    
    # Mocne strony z testu Kolba
    if tests['kolb']:
        style = tests['kolb']['style']
        strengths.append({
            'name': f"Styl uczenia: {style.split('(')[0].strip()}",
            'source': 'Test Kolba',
            'description': get_kolb_strength(style),
            'icon': '🔄'
        })
    
    # Mocne strony z testu Neuroleadera
    if tests['neuroleader']:
        nl_type = tests['neuroleader']['type']
        strengths.append({
            'name': f"Typ przywódcy: {nl_type}",
            'source': 'Test Neuroleadera',
            'description': get_neuroleader_strength(nl_type),
            'icon': '🧬'
        })
    
    # Mocne strony z testu MI
    if tests['mi'] and tests['mi']['top_3']:
        for intelligence, score in tests['mi']['top_3'][:3]:
            strengths.append({
                'name': f"Inteligencja: {get_intelligence_name(intelligence)}",
                'source': 'Test MI',
                'description': get_intelligence_strength(intelligence),
                'icon': get_intelligence_icon(intelligence),
                'score': score
            })
    
    # Mocne strony z aktywności
    if len(activity['modules_completed']) >= 5:
        strengths.append({
            'name': 'Konsekwencja w nauce',
            'source': 'Aktywność',
            'description': f"Ukończyłeś {len(activity['modules_completed'])} modułów - pokazujesz silną determinację w rozwoju",
            'icon': '🎯'
        })
    
    if activity['engagement_score'] > 70:
        strengths.append({
            'name': 'Wysokie zaangażowanie',
            'source': 'Aktywność',
            'description': f"Twój wynik zaangażowania: {activity['engagement_score']}/100 - jesteś aktywnym uczestnikiem",
            'icon': '⚡'
        })
    
    return strengths


def analyze_patterns(activity: Dict) -> Dict:
    """Analizuje wzorce w zachowaniu użytkownika"""
    patterns = {
        'learning_pace': 'moderate',
        'consistency': 'regular',
        'preferred_areas': [],
        'insights': []
    }
    
    # Tempo nauki
    completed = len(activity['modules_completed'])
    if completed >= 10:
        patterns['learning_pace'] = 'fast'
        patterns['insights'].append("Uczysz się w szybkim tempie")
    elif completed >= 5:
        patterns['learning_pace'] = 'moderate'
        patterns['insights'].append("Utrzymujesz stabilne tempo nauki")
    else:
        patterns['learning_pace'] = 'exploratory'
        patterns['insights'].append("Eksplorujesz różne obszary")
    
    # Konsystencja
    if activity['engagement_score'] > 60:
        patterns['consistency'] = 'high'
        patterns['insights'].append("Regularnie wracasz do platformy")
    
    # Preferowane obszary (na podstawie ukończonych modułów)
    if activity['modules_completed']:
        # Grupuj moduły po kategoriach
        categories = categorize_modules(activity['modules_completed'])
        patterns['preferred_areas'] = categories[:3]  # Top 3 kategorie
    
    return patterns


def categorize_modules(modules: List[str]) -> List[str]:
    """Kategoryzuje moduły na podstawie ich nazw"""
    categories = {}
    
    category_keywords = {
        'Komunikacja': ['communication', 'rozmowa', 'feedback', 'komunikacja'],
        'Przywództwo': ['leadership', 'leader', 'zarządzanie', 'zespół'],
        'Rozwój osobisty': ['rozwój', 'development', 'mindset', 'motywacja'],
        'Narzędzia': ['narzędzia', 'tools', 'techniki', 'metody'],
        'Inteligencja emocjonalna': ['emocje', 'emotional', 'empatia']
    }
    
    for module in modules:
        module_lower = module.lower()
        for category, keywords in category_keywords.items():
            if any(keyword in module_lower for keyword in keywords):
                categories[category] = categories.get(category, 0) + 1
                break
    
    # Sortuj po liczbie modułów
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    return [cat for cat, _ in sorted_categories]


def calculate_engagement_score(user_data: Dict) -> int:
    """
    Oblicza wynik zaangażowania (0-100) na podstawie różnych metryk
    
    NOWY WZÓR (Wariant 2):
    - 60 pkt: Testy diagnostyczne (główny cel aplikacji)
    - 40 pkt: Ostatnia aktywność (regularność użytkowania)
    
    Przykłady:
    - 3 testy + dzisiaj = 100/100 🔥
    - 3 testy + tydzień temu = 90/100 ⭐
    - 1 test + dzisiaj = 60/100 ✅
    """
    score = 0
    
    # Testy diagnostyczne (60 punktów) - ZWIĘKSZONE z 30 do 60
    tests_completed = 0
    if 'kolb_test' in user_data and user_data['kolb_test']:
        tests_completed += 1
    if 'test_scores' in user_data and user_data['test_scores']:
        tests_completed += 1
    if 'mi_test' in user_data and user_data['mi_test']:
        tests_completed += 1
    
    score += (tests_completed / 3) * 60
    
    # Ostatnia aktywność (40 punktów) - ZWIĘKSZONE z 30 do 40
    if 'last_login' in user_data:
        try:
            # Obsłuż różne formaty daty
            last_login_str = user_data['last_login']
            
            # Spróbuj format z godziną
            try:
                last_login = datetime.strptime(last_login_str, "%Y-%m-%d %H:%M:%S")
            except:
                # Spróbuj format bez godziny
                try:
                    last_login = datetime.strptime(last_login_str, "%Y-%m-%d")
                except:
                    # Jeśli to już datetime object
                    if isinstance(last_login_str, datetime):
                        last_login = last_login_str
                    else:
                        last_login = None
            
            if last_login:
                days_since = (datetime.now() - last_login).days
                
                if days_since <= 1:
                    score += 40  # Bardzo aktywny (dzisiaj/wczoraj)
                elif days_since <= 7:
                    score += 30  # Aktywny (ostatni tydzień)
                elif days_since <= 30:
                    score += 15  # Umiarkowanie aktywny (ostatni miesiąc)
                # > 30 dni = 0 punktów
                
        except Exception as e:
            # Jeśli błąd parsowania, nie dodawaj punktów za aktywność
            pass
    
    return min(int(score), 100)


def generate_personal_synthesis(profile: Dict) -> str:
    """
    Generuje spersonalizowaną syntezę profilu użytkownika
    Zwraca tekst opisujący użytkownika na podstawie wszystkich danych
    """
    tests = profile['tests']
    activity = profile['activity']
    strengths = profile['strengths']
    patterns = profile['patterns']
    
    synthesis_parts = []
    
    # Wprowadzenie
    synthesis_parts.append(
        f"Na podstawie Twoich {len(tests['completed'])} ukończonych testów diagnostycznych "
        f"i aktywności w platformie BrainVenture Academy, oto Twój kompleksowy profil rozwojowy."
    )
    
    # Styl uczenia się
    if tests['kolb']:
        style = tests['kolb']['style'].split('(')[0].strip()
        synthesis_parts.append(
            f"\n\n**Twój styl uczenia się:** {style}. {tests['kolb']['description']}"
        )
    
    # Typ lidera
    if tests['neuroleader']:
        nl_type = tests['neuroleader']['type']
        synthesis_parts.append(
            f"\n\n**Jako lider:** Reprezentujesz typ {nl_type}. {tests['neuroleader']['description']}"
        )
    
    # Inteligencje wielorakie
    if tests['mi'] and tests['mi']['top_3']:
        top_intel = tests['mi']['top_3'][0][0]
        synthesis_parts.append(
            f"\n\n**Twoje dominujące inteligencje:** Wyróżnia Cię przede wszystkim inteligencja "
            f"{get_intelligence_name(top_intel)}, co oznacza że najlepiej uczysz się poprzez "
            f"{get_intelligence_learning_method(top_intel)}."
        )
    
    # Wzorce aktywności
    if patterns['insights']:
        synthesis_parts.append(
            f"\n\n**Twoje wzorce uczenia się:** {'. '.join(patterns['insights'])}."
        )
    
    # Mocne strony
    if len(strengths) > 0:
        top_strength = strengths[0]
        synthesis_parts.append(
            f"\n\n**Twoja największa mocna strona:** {top_strength['name']}. "
            f"{top_strength['description']}"
        )
    
    return "".join(synthesis_parts)


def generate_recommendations(profile: Dict) -> List[Dict]:
    """
    Generuje spersonalizowane rekomendacje następnych kroków
    
    Returns:
        Lista rekomendacji: {title, description, priority, icon}
    """
    recommendations = []
    tests = profile['tests']
    activity = profile['activity']
    
    # Rekomendacje bazujące na brakujących testach
    if 'Kolb' not in tests['completed']:
        recommendations.append({
            'title': 'Poznaj swój styl uczenia się',
            'description': 'Wykonaj Test Kolba aby lepiej zrozumieć jak efektywnie się uczysz',
            'priority': 'high',
            'icon': '🔄',
            'action': 'Przejdź do testu Kolba'
        })
    
    if 'Neuroleader' not in tests['completed']:
        recommendations.append({
            'title': 'Odkryj swój typ lidera',
            'description': 'Test Neuroleadera pokaże Ci jakim jesteś lub możesz być przywódcą',
            'priority': 'high',
            'icon': '🧬',
            'action': 'Przejdź do testu Neuroleadera'
        })
    
    if 'MI' not in tests['completed']:
        recommendations.append({
            'title': 'Sprawdź swoje inteligencje',
            'description': 'Test Wielorakich Inteligencji ujawni Twoje unikalne talenty',
            'priority': 'high',
            'icon': '🧠',
            'action': 'Przejdź do testu MI'
        })
    
    # Rekomendacje bazujące na wynikach testów
    if tests['mi'] and tests['mi']['top_3']:
        top_intelligence = tests['mi']['top_3'][0][0]
        recommended_modules = get_recommended_modules_for_intelligence(top_intelligence)
        if recommended_modules:
            recommendations.append({
                'title': f'Moduły dopasowane do inteligencji {get_intelligence_name(top_intelligence)}',
                'description': f'Polecamy: {", ".join(recommended_modules[:3])}',
                'priority': 'medium',
                'icon': get_intelligence_icon(top_intelligence),
                'action': 'Zobacz polecane moduły'
            })
    
    # Rekomendacje bazujące na aktywności
    if activity['total_progress'] < 30:
        recommendations.append({
            'title': 'Zwiększ aktywność w kursach',
            'description': 'Ukończenie większej liczby modułów pomoże Ci lepiej zrozumieć swój potencjał',
            'priority': 'medium',
            'icon': '📚',
            'action': 'Przeglądaj kursy'
        })
    
    if len(activity['modules_in_progress']) > 3:
        recommendations.append({
            'title': 'Dokończ rozpoczęte moduły',
            'description': f'Masz {len(activity["modules_in_progress"])} modułów w trakcie - dokończenie ich zwiększy Twój postęp',
            'priority': 'high',
            'icon': '✅',
            'action': 'Zobacz rozpoczęte moduły'
        })
    
    # Sortuj po priorytecie
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    recommendations.sort(key=lambda x: priority_order[x['priority']])
    
    return recommendations[:5]  # Top 5 rekomendacji


# ===== FUNKCJE POMOCNICZE - OPISY =====

def get_kolb_description(style: str) -> str:
    """Zwraca opis stylu uczenia się Kolba"""
    descriptions = {
        'Diverging': 'Uczysz się najlepiej poprzez obserwację i refleksję. Potrafisz spojrzeć na sytuacje z różnych perspektyw.',
        'Assimilating': 'Preferujesz logiczne podejście i abstrakcyjne koncepcje. Świetnie organizujesz informacje w spójne modele.',
        'Converging': 'Najlepiej uczysz się przez praktyczne zastosowanie teorii. Lubisz rozwiązywać konkretne problemy.',
        'Accommodating': 'Uczysz się przez działanie i doświadczenie. Jesteś otwarty na nowe wyzwania i elastyczny w podejściu.'
    }
    for key in descriptions:
        if key in style:
            return descriptions[key]
    return 'Masz unikalny styl uczenia się łączący różne podejścia.'


def get_neuroleader_description(nl_type: str) -> str:
    """Zwraca opis typu neuroleadera"""
    from data.neuroleader_test_questions import NEUROLEADER_TYPES
    if nl_type in NEUROLEADER_TYPES:
        return NEUROLEADER_TYPES[nl_type].get('description', '')
    return ''


def get_mi_description(top_3: List[Tuple]) -> str:
    """Zwraca opis na podstawie top 3 inteligencji"""
    if not top_3:
        return ''
    
    top = top_3[0][0] if top_3 else ''
    return f"Twoja dominująca inteligencja to {get_intelligence_name(top)}, co oznacza unikalny sposób poznawania świata."


def get_kolb_strength(style: str) -> str:
    """Zwraca mocną stronę dla stylu Kolba"""
    strengths = {
        'Diverging': 'Kreatywność i umiejętność spojrzenia na problemy z wielu perspektyw',
        'Assimilating': 'Analityczne myślenie i tworzenie spójnych teorii',
        'Converging': 'Praktyczne rozwiązywanie problemów i podejmowanie decyzji',
        'Accommodating': 'Adaptacja do zmian i uczenie się przez doświadczenie'
    }
    for key in strengths:
        if key in style:
            return strengths[key]
    return 'Elastyczność w uczeniu się'


def get_neuroleader_strength(nl_type: str) -> str:
    """Zwraca mocną stronę dla typu neuroleadera"""
    from data.neuroleader_test_questions import NEUROLEADER_TYPES
    if nl_type in NEUROLEADER_TYPES:
        return NEUROLEADER_TYPES[nl_type].get('supermoc', '')
    return ''


def get_intelligence_name(intelligence: str) -> str:
    """Zwraca polską nazwę inteligencji"""
    names = {
        'linguistic': 'Językowa',
        'logical': 'Logiczno-matematyczna',
        'visual': 'Wizualno-przestrzenna',
        'musical': 'Muzyczna',
        'kinesthetic': 'Kinestetyczna',
        'interpersonal': 'Interpersonalna',
        'intrapersonal': 'Intrapersonalna',
        'naturalistic': 'Przyrodnicza'
    }
    return names.get(intelligence, intelligence.title())


def get_intelligence_icon(intelligence: str) -> str:
    """Zwraca emoji dla inteligencji"""
    icons = {
        'linguistic': '🗣️',
        'logical': '🔢',
        'visual': '🎨',
        'musical': '🎵',
        'kinesthetic': '🤸',
        'interpersonal': '👥',
        'intrapersonal': '🧘',
        'naturalistic': '🌿'
    }
    return icons.get(intelligence, '🧠')


def get_intelligence_strength(intelligence: str) -> str:
    """Zwraca opis mocnej strony dla inteligencji"""
    strengths = {
        'linguistic': 'Wysoka sprawność językowa - komunikacja i pisanie',
        'logical': 'Myślenie analityczne i rozwiązywanie problemów',
        'visual': 'Wyobraźnia przestrzenna i wizualizacja',
        'musical': 'Wrażliwość na dźwięki i rytmy',
        'kinesthetic': 'Koordynacja ciała i uczenie się przez ruch',
        'interpersonal': 'Rozumienie ludzi i praca zespołowa',
        'intrapersonal': 'Samoświadomość i autorefleksja',
        'naturalistic': 'Obserwacja natury i systemowe myślenie'
    }
    return strengths.get(intelligence, 'Unikalna zdolność poznawcza')


def get_intelligence_learning_method(intelligence: str) -> str:
    """Zwraca preferowaną metodę uczenia się dla inteligencji"""
    methods = {
        'linguistic': 'czytanie, pisanie i dyskusje',
        'logical': 'analizę danych i rozwiązywanie zagadek',
        'visual': 'diagramy, wykresy i materiały wizualne',
        'musical': 'rytm, melodie i dźwięki',
        'kinesthetic': 'praktyczne ćwiczenia i ruch',
        'interpersonal': 'pracę grupową i interakcje społeczne',
        'intrapersonal': 'samodzielną pracę i refleksję',
        'naturalistic': 'obserwację wzorców i systemów'
    }
    return methods.get(intelligence, 'praktyczne doświadczenie')


def get_recommended_modules_for_intelligence(intelligence: str) -> List[str]:
    """Zwraca rekomendowane moduły dla danej inteligencji"""
    modules = {
        'linguistic': ['Komunikacja w zespole', 'Storytelling w biznesie', 'Pisanie raportów'],
        'logical': ['Analiza danych', 'Podejmowanie decyzji', 'Strategiczne myślenie'],
        'visual': ['Mind Mapping', 'Design Thinking', 'Prezentacje wizualne'],
        'musical': ['Komunikacja niewerbalna', 'Wystąpienia publiczne', 'Budowanie atmosfery'],
        'kinesthetic': ['Warsztat komunikacyjny', 'Symulacje biznesowe', 'Team building'],
        'interpersonal': ['Przywództwo', 'Coaching', 'Zarządzanie konfliktem'],
        'intrapersonal': ['Mindfulness', 'Self-awareness', 'Osobisty rozwój'],
        'naturalistic': ['Myślenie systemowe', 'Ekologia organizacji', 'Sustainable leadership']
    }
    return modules.get(intelligence, [])


def create_kolb_radar_chart(profile_data: Dict):
    """
    Tworzy wykres radarowy dla Testu Kolba
    
    Args:
        profile_data: Pełne dane profilu z collect_user_profile_data()
    
    Returns:
        plotly Figure object lub None jeśli brak testu
    """
    import plotly.graph_objects as go
    
    tests = profile_data['tests']
    
    if not tests['kolb']:
        return None
    
    kolb_scores = tests['kolb'].get('scores', {})
    
    # Wymiary Kolba z polskimi skrótami
    categories = [
        'Konkretne<br>doświadczenie (CE)',
        'Refleksyjna<br>obserwacja (RO)',
        'Abstrakcyjna<br>konceptualizacja (AC)',
        'Aktywne<br>eksperymentowanie (AE)'
    ]
    
    # Normalizacja wyników (0-48 → 0-100)
    max_kolb = 48
    values = [
        (kolb_scores.get('CE', 0) / max_kolb) * 100,
        (kolb_scores.get('RO', 0) / max_kolb) * 100,
        (kolb_scores.get('AC', 0) / max_kolb) * 100,
        (kolb_scores.get('AE', 0) / max_kolb) * 100
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='rgba(102, 126, 234, 0.8)', width=3),
        marker=dict(size=10, color='#667eea'),
        hovertemplate='<b>%{theta}</b><br>Wynik: %{r:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(255, 255, 255, 0.95)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='rgba(102, 126, 234, 0.3)',
                tickvals=[25, 50, 75, 100],
                ticktext=['25%', '50%', '75%', '100%']
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color='#2c3e50'),
                gridcolor='rgba(102, 126, 234, 0.3)'
            )
        ),
        showlegend=False,
        title=dict(
            text=f'🔄 Test Kolba: {tests["kolb"]["style"]}',
            font=dict(size=16, color='#667eea', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        height=400,
        margin=dict(l=60, r=60, t=80, b=60),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig


def create_neuroleader_radar_chart(profile_data: Dict):
    """
    Tworzy wykres radarowy dla Testu Neuroleader
    
    Args:
        profile_data: Pełne dane profilu z collect_user_profile_data()
    
    Returns:
        plotly Figure object lub None jeśli brak testu
    """
    import plotly.graph_objects as go
    
    tests = profile_data['tests']
    
    if not tests['neuroleader']:
        return None
    
    neuroleader_scores = tests['neuroleader'].get('scores', {})
    
    # 5 typów Neuroleadera
    categories = ['Neuroanalityk', 'Neuroreaktor', 'Neurobalanser', 'Neuroempata', 'Neuroinnowator']
    
    # Normalizacja wyników (0-30 → 0-100)
    max_neuroleader = 30
    values = [
        (neuroleader_scores.get('Neuroanalityk', 0) / max_neuroleader) * 100,
        (neuroleader_scores.get('Neuroreaktor', 0) / max_neuroleader) * 100,
        (neuroleader_scores.get('Neurobalanser', 0) / max_neuroleader) * 100,
        (neuroleader_scores.get('Neuroempata', 0) / max_neuroleader) * 100,
        (neuroleader_scores.get('Neuroinnowator', 0) / max_neuroleader) * 100
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(240, 147, 251, 0.3)',
        line=dict(color='rgba(240, 147, 251, 0.8)', width=3),
        marker=dict(size=10, color='#f093fb'),
        hovertemplate='<b>%{theta}</b><br>Wynik: %{r:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(255, 255, 255, 0.95)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='rgba(240, 147, 251, 0.3)',
                tickvals=[25, 50, 75, 100],
                ticktext=['25%', '50%', '75%', '100%']
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color='#2c3e50'),
                gridcolor='rgba(240, 147, 251, 0.3)'
            )
        ),
        showlegend=False,
        title=dict(
            text=f'🧬 Neuroleader: {tests["neuroleader"]["type"]}',
            font=dict(size=16, color='#f093fb', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        height=400,
        margin=dict(l=60, r=60, t=80, b=60),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig


def create_mi_radar_chart(profile_data: Dict):
    """
    Tworzy wykres radarowy dla Testu MI (wszystkie 8 inteligencji)
    
    Args:
        profile_data: Pełne dane profilu z collect_user_profile_data()
    
    Returns:
        plotly Figure object lub None jeśli brak testu
    """
    import plotly.graph_objects as go
    
    tests = profile_data['tests']
    
    if not tests['mi']:
        return None
    
    # Obsłuż różne struktury danych MI testu
    mi_results = tests['mi'].get('results', tests['mi'].get('all_scores', {}))
    
    if not mi_results:
        # Jeśli brak results/all_scores, spróbuj zbudować z top_3
        top_3 = tests['mi'].get('top_3', [])
        if top_3:
            mi_results = {intel: score for intel, score in top_3}
    
    if not mi_results:
        return None
    
    # Wszystkie 8 inteligencji w określonej kolejności
    intelligence_order = ['linguistic', 'logical', 'visual', 'musical', 
                          'kinesthetic', 'interpersonal', 'intrapersonal', 'naturalistic']
    
    categories = [get_intelligence_name(intel) for intel in intelligence_order if intel in mi_results]
    values = [mi_results.get(intel, 0) for intel in intelligence_order if intel in mi_results]
    
    # Znajdź top inteligencję
    top_intel = max(mi_results.items(), key=lambda x: x[1])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(79, 172, 254, 0.3)',
        line=dict(color='rgba(79, 172, 254, 0.8)', width=3),
        marker=dict(size=10, color='#4facfe'),
        hovertemplate='<b>%{theta}</b><br>Wynik: %{r:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(255, 255, 255, 0.95)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='rgba(79, 172, 254, 0.3)',
                tickvals=[25, 50, 75, 100],
                ticktext=['25%', '50%', '75%', '100%']
            ),
            angularaxis=dict(
                tickfont=dict(size=10, color='#2c3e50'),
                gridcolor='rgba(79, 172, 254, 0.3)'
            )
        ),
        showlegend=False,
        title=dict(
            text=f'🧠 MI Test: {get_intelligence_name(top_intel[0])}',
            font=dict(size=16, color='#4facfe', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        height=400,
        margin=dict(l=60, r=60, t=80, b=60),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    
    return fig


def create_intelligence_bars(profile_data: Dict):
    """
    Tworzy poziome paski postępu dla top inteligencji MI
    
    Args:
        profile_data: Pełne dane profilu
    
    Returns:
        plotly Figure object z wykresem słupkowym
    """
    import plotly.graph_objects as go
    
    tests = profile_data['tests']
    
    if not tests['mi']:
        return None
    
    # Obsłuż różne struktury danych MI testu
    mi_results = tests['mi'].get('results', tests['mi'].get('all_scores', {}))
    
    if not mi_results:
        # Jeśli brak results/all_scores, spróbuj zbudować z top_3
        top_3 = tests['mi'].get('top_3', [])
        if top_3:
            mi_results = {intel: score for intel, score in top_3}
    
    if not mi_results:
        return None
    
    # Sortuj i weź top 5
    sorted_mi = sorted(mi_results.items(), key=lambda x: x[1], reverse=True)[:5]
    
    intelligences = [get_intelligence_name(intel) for intel, _ in sorted_mi]
    scores = [score for _, score in sorted_mi]
    
    # Kolory gradientowe
    colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=intelligences[::-1],  # Odwróć kolejność dla lepszej wizualizacji
        x=scores[::-1],
        orientation='h',
        marker=dict(
            color=colors[::-1],
            line=dict(color='white', width=2)
        ),
        text=[f'{s:.1f}%' for s in scores[::-1]],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Arial Black'),
        hovertemplate='<b>%{y}</b><br>Wynik: %{x:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='💪 Top 5 Wielorakich Inteligencji',
            font=dict(size=16, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Wynik (%)',
            range=[0, 100],
            gridcolor='rgba(200, 200, 200, 0.3)',
            showgrid=True
        ),
        yaxis=dict(
            title='',
            tickfont=dict(size=12)
        ),
        height=350,
        margin=dict(l=200, r=50, t=60, b=50),
        paper_bgcolor='white',
        plot_bgcolor='rgba(240, 240, 240, 0.5)',
        showlegend=False
    )
    
    return fig


def create_engagement_gauge(profile_data: Dict):
    """
    Tworzy gauge chart (wskaźnik półkolowy) dla zaangażowania
    
    Args:
        profile_data: Pełne dane profilu z collect_user_profile_data()
    
    Returns:
        plotly Figure object z gauge chart
    """
    import plotly.graph_objects as go
    
    engagement_score = profile_data['activity']['engagement_score']
    
    # Określ kolor na podstawie wyniku
    if engagement_score >= 75:
        color = '#2ecc71'  # Zielony - wysoki
        status = 'Wysoki'
    elif engagement_score >= 50:
        color = '#f39c12'  # Pomarańczowy - średni
        status = 'Średni'
    elif engagement_score >= 25:
        color = '#e67e22'  # Pomarańczowy ciemny - niski
        status = 'Niski'
    else:
        color = '#e74c3c'  # Czerwony - bardzo niski
        status = 'Rozpoczynający'
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=engagement_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"<b>Zaangażowanie</b><br><span style='font-size:0.8em; color:gray'>{status}</span>", 
               'font': {'size': 18, 'family': 'Arial Black'}},
        number={'suffix': "/100", 'font': {'size': 40, 'color': color}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': color},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 25], 'color': 'rgba(231, 76, 60, 0.15)'},
                {'range': [25, 50], 'color': 'rgba(230, 126, 34, 0.15)'},
                {'range': [50, 75], 'color': 'rgba(243, 156, 18, 0.15)'},
                {'range': [75, 100], 'color': 'rgba(46, 204, 113, 0.15)'}
            ],
            'threshold': {
                'line': {'color': color, 'width': 4},
                'thickness': 0.75,
                'value': engagement_score
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor='white',
        font={'family': 'Arial'}
    )
    
    return fig


def create_strengths_bars(profile_data: Dict):
    """
    Tworzy poziome paski dla Top 5 Mocnych Stron
    
    Args:
        profile_data: Pełne dane profilu z collect_user_profile_data()
    
    Returns:
        plotly Figure object z poziomymi paskami
    """
    import plotly.graph_objects as go
    
    strengths = profile_data['strengths'][:5]  # Top 5
    
    if not strengths:
        return None
    
    # Przygotuj dane
    names = [f"{s['icon']} {s['name']}" for s in strengths]
    # Symulujemy "siłę" jako 100 - każda mocna strona jest równie ważna
    # Ale możemy użyć różnych kolorów dla źródła
    values = [100 - (i * 5) for i in range(len(strengths))]  # 100, 95, 90, 85, 80
    
    # Kolory według źródła
    colors = []
    for strength in strengths:
        source = strength['source']
        if 'Kolb' in source:
            colors.append('#667eea')
        elif 'Neuroleader' in source:
            colors.append('#f093fb')
        elif 'MI' in source or 'Inteligencja' in source:
            colors.append('#4facfe')
        else:
            colors.append('#95a5a6')  # Szary dla aktywności
    
    fig = go.Figure()
    
    # Przygotuj customdata dla hover (źródła odwrócone)
    sources_reversed = [strengths[i]['source'] for i in range(len(strengths)-1, -1, -1)]
    
    fig.add_trace(go.Bar(
        y=names[::-1],  # Odwróć kolejność (najlepszy na górze)
        x=values[::-1],
        orientation='h',
        marker=dict(
            color=colors[::-1],
            line=dict(color='white', width=2)
        ),
        text=[f'#{i+1}' for i in range(len(strengths)-1, -1, -1)],
        textposition='inside',
        textfont=dict(color='white', size=16, family='Arial Black'),
        customdata=sources_reversed,
        hovertemplate='<b>%{y}</b><br>Źródło: %{customdata}<extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        title=dict(
            text='💪 Top 5 Mocnych Stron',
            font=dict(size=18, color='#2c3e50', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[0, 105]
        ),
        yaxis=dict(
            tickfont=dict(size=13, family='Arial')
        ),
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='white',
        plot_bgcolor='rgba(240, 240, 240, 0.3)'
    )
    
    return fig
