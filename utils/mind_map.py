"""
Funkcje do generowania interaktywnych map myśli dla lekcji
"""
import streamlit as st
import re

def create_lesson_mind_map(lesson_data):
    """
    Tworzy interaktywną mapę myśli dla danej lekcji
    Implementuje system skalowalny z trzema trybami:
    1. Data-driven - używa danych z lesson_data['mind_map']
    2. Backward compatibility - dla B1C1L1 (stary hardcoded system)
    3. Auto-generated - automatyczne generowanie dla lekcji bez dedykowanych danych
    
    Args:
        lesson_data (dict): Dane lekcji w formacie JSON
    """
    try:
        # Inteligentna logika decyzyjna
        if 'mind_map' in lesson_data:
            # Tryb 1: Data-driven - używaj danych z JSON
            return create_data_driven_mind_map(lesson_data['mind_map'])
        elif lesson_data.get('id') == 'B1C1L1':
            # Tryb 2: Backward compatibility dla B1C1L1c
            return create_b1c1l1_mind_map()
        else:
            # Tryb 3: Auto-generated dla pozostałych lekcji
            return create_auto_generated_mind_map(lesson_data)
            
    except ImportError:
        # Fallback jeśli streamlit-agraph nie jest dostępne
        st.warning("📋 Mapa myśli nie jest obecnie dostępna. Zainstaluj bibliotekę streamlit-agraph aby włączyć tę funkcję.")
        return None
    except Exception as e:
        st.error(f"Błąd podczas tworzenia mapy myśli: {str(e)}")
        return None

def create_b1c1l1_mind_map():
    """
    Tworzy mapę myśli specjalnie dla lekcji B1C1L1 - Strach przed stratą
    """
    try:
        from streamlit_agraph import agraph, Node, Edge, Config
        
        # Definiuj węzły
        nodes = []
        edges = []
          # Centralny węzeł - kolor z bloku 1 Skills (pomarańczowy-czerwony)
        nodes.append(Node(id="central", 
                         label="💸 STRACH PRZED STRATĄ", 
                         size=30,
                         color="#FF9950",
                         font={"size": 16, "color": "#FF9950"}))
        
        # Główne koncepty - kolory z bloków Skills
        concepts = [
            {"id": "teoria", "label": "📊 Teoria perspektywy", "color": "#43C6AC"},    # Block 2
            {"id": "dyspozycja", "label": "🔄 Efekt dyspozycji", "color": "#667eea"},  # Block 3            {"id": "dopamina", "label": "🧠 Dopamina", "color": "#f093fb"},           # Block 4
            {"id": "framing", "label": "🖼️ Framing", "color": "#4facfe"}              # Block 5
        ]
        
        for concept in concepts:
            nodes.append(Node(id=concept["id"],
                            label=concept["label"],
                            size=20,
                            color=concept["color"],
                            font={"size": 12, "color": concept["color"]}))  # Font color matches node color
            edges.append(Edge(source="central", target=concept["id"]))
        
        # Szczegóły teorii perspektywy
        teoria_details = [
            {"id": "bol_straty", "label": "😢 Ból straty 2-2,5x silniejszy", "parent": "teoria"},
            {"id": "pewnosc", "label": "🛡️ Preferujemy pewność", "parent": "teoria"},
            {"id": "awersja", "label": "⚠️ Awersja do ryzyka", "parent": "teoria"}
        ]
        
        # Szczegóły efektu dyspozycji
        dyspozycja_details = [
            {"id": "sprzedaj_zyski", "label": "💰 Za szybko sprzedajemy zyski", "parent": "dyspozycja"},
            {"id": "trzymaj_straty", "label": "📉 Za długo trzymamy straty", "parent": "dyspozycja"},
            {"id": "get_even", "label": "🎯 Syndrom 'wyjdę na zero'", "parent": "dyspozycja"}
        ]
        
        # Szczegóły dopaminy
        dopamina_details = [
            {"id": "nagroda", "label": "🎉 System nagrody w mózgu", "parent": "dopamina"},
            {"id": "uzaleznienie", "label": "🎰 Uzależnienie od transakcji", "parent": "dopamina"},
            {"id": "euforia", "label": "🚀 Euforia po zyskach", "parent": "dopamina"}
        ]
        
        # Szczegóły framingu
        framing_details = [
            {"id": "prezentacja", "label": "📝 Sposób prezentacji wpływa na decyzje", "parent": "framing"},
            {"id": "pozytywny", "label": "😊 Pozytywne vs negatywne ujęcie", "parent": "framing"},
            {"id": "manipulacja", "label": "🎭 Podatność na manipulację", "parent": "framing"}
        ]
          # Dodaj wszystkie szczegóły - używają jaśniejszych odcieni kolorów z bloków Skills
        all_details = teoria_details + dyspozycja_details + dopamina_details + framing_details
        detail_colors = {
            "teoria": "#67DFD0",    # Jaśniejszy odcień Block 2
            "dyspozycja": "#8A9BFF", # Jaśniejszy odcień Block 3  
            "dopamina": "#F5B6FF",   # Jaśniejszy odcień Block 4
            "framing": "#7DC6FF"     # Jaśniejszy odcień Block 5
        }
        
        for detail in all_details:
            parent_color = detail_colors.get(detail["parent"], "#DDA0DD")
            nodes.append(Node(id=detail["id"],
                            label=detail["label"],
                            size=12,
                            color=parent_color,
                            font={"size": 10, "color": parent_color}))
            edges.append(Edge(source=detail["parent"], target=detail["id"]))
          # Rozwiązania praktyczne - kolor z Block 3 Skills (jaśniejszy odcień)
        solutions = [
            {"id": "zoom_out", "label": "🔍 Zoom out - szeroka perspektywa"},
            {"id": "limit_strat", "label": "🚧 Wyznacz limit strat"},
            {"id": "stop_checking", "label": "📵 Przestań sprawdzać apki"},
            {"id": "plan", "label": "📋 Trzymaj się planu"}
        ]
        
        solution_color = "#8A9BFF"  # Jaśniejszy odcień Block 3 color
        for solution in solutions:
            nodes.append(Node(id=solution["id"],
                            label=solution["label"],
                            size=15,
                            color=solution_color,
                            font={"size": 11, "color": solution_color}))
            edges.append(Edge(source="central", target=solution["id"]))
        
        # Case study - Kuba (kolor z Block 1 Skills)
        case_study_color = "#FF9950"
        nodes.append(Node(id="kuba",
                        label="👨‍💻 Case Study: Kuba i $MOONZ",
                        size=18,
                        color=case_study_color,
                        font={"size": 12, "color": case_study_color}))
        edges.append(Edge(source="central", target="kuba"))
        
        kuba_details = [
            {"id": "fomo", "label": "😱 FOMO na $MOONZ", "parent": "kuba"},
            {"id": "spadek", "label": "📉 -20% w 2 dni", "parent": "kuba"},
            {"id": "panika", "label": "😰 Panika i sprawdzanie co 3 min", "parent": "kuba"}
        ]
        
        kuba_detail_color = "#FFB380"  # Jaśniejszy odcień Block 1 color
        for detail in kuba_details:
            nodes.append(Node(id=detail["id"],
                            label=detail["label"],
                            size=10,
                            color=kuba_detail_color,
                            font={"size": 9, "color": kuba_detail_color}))
            edges.append(Edge(source=detail["parent"], target=detail["id"]))
          # Konfiguracja wyświetlania - highlight color zsynchronizowany z Skills Block 2
        config = Config(width=800, 
                       height=600,
                       directed=False,
                       physics=True,
                       hierarchical=False,
                       nodeHighlightBehavior=True,
                       highlightColor="#43C6AC",  # Block 2 Skills color
                       collapsible=False)
        
        # Wyświetl mapę
        return_value = agraph(nodes=nodes, 
                             edges=edges, 
                             config=config)
        
        return return_value
        
    except ImportError:
        st.error("Nie można załadować biblioteki streamlit-agraph. Zainstaluj ją używając: pip install streamlit-agraph")
        return None
    except Exception as e:
        st.error(f"Błąd podczas tworzenia mapy myśli: {str(e)}")
        return None

def create_generic_mind_map(lesson_data):
    """
    PRZESTARZAŁA: Używaj create_auto_generated_mind_map
    Zachowana dla zgodności wstecznej
    """
    return create_auto_generated_mind_map(lesson_data)

def create_data_driven_mind_map(mind_map_data):
    """
    Tworzy mapę myśli z danych strukturalnych JSON
    
    Args:
        mind_map_data (dict): Struktura mind_map z pliku JSON lekcji
    """
    try:
        from streamlit_agraph import agraph, Node, Edge, Config
        
        nodes = []
        edges = []
          # Centralny węzeł - domyślnie używa koloru z Bloku 2 Skills
        central = mind_map_data.get('central_node', {})
        central_color = central.get('color', '#43C6AC')  # Block 2 color as default
        nodes.append(Node(
            id=central.get('id', 'main_topic'),
            label=central.get('label', '🎯 GŁÓWNY TEMAT'),
            size=central.get('size', 30),
            color=central_color,
            font={"size": central.get('font_size', 16), "color": central_color}
        ))
        
        # Kategorie główne
        for category in mind_map_data.get('categories', []):
            nodes.append(Node(
                id=category.get('id', 'category'),
                label=category.get('label', 'Kategoria'),
                size=category.get('size', 20),
                color=category.get('color', '#43C6AC'),  # Skills Block 2 color as default
                font={"size": category.get('font_size', 12), "color": "white"}
            ))
            edges.append(Edge(source=central.get('id', 'main_topic'), target=category.get('id', 'category')))
            
            # Szczegóły kategorii
            for detail in category.get('details', []):
                nodes.append(Node(
                    id=detail.get('id', 'detail'),
                    label=detail.get('label', 'Szczegół'),
                    size=detail.get('size', 12),
                    color=detail.get('color', '#DDA0DD'),
                    font={"size": detail.get('font_size', 10), "color": "black"}
                ))
                edges.append(Edge(source=category.get('id', 'category'), target=detail.get('id', 'detail')))
        
        # Rozwiązania praktyczne
        for solution in mind_map_data.get('solutions', []):
            nodes.append(Node(
                id=solution.get('id', 'solution'),
                label=solution.get('label', 'Rozwiązanie'),
                size=solution.get('size', 15),
                color=solution.get('color', '#90EE90'),
                font={"size": solution.get('font_size', 11), "color": "black"}
            ))
            edges.append(Edge(source=central.get('id', 'main_topic'), target=solution.get('id', 'solution')))
        
        # Case study
        case_study = mind_map_data.get('case_study', {})
        if case_study:
            nodes.append(Node(
                id=case_study.get('id', 'case_study'),
                label=case_study.get('label', '📱 Case Study'),
                size=case_study.get('size', 18),
                color=case_study.get('color', '#FF8C42'),
                font={"size": case_study.get('font_size', 12), "color": "white"}
            ))
            edges.append(Edge(source=central.get('id', 'main_topic'), target=case_study.get('id', 'case_study')))
            
            # Szczegóły case study
            for detail in case_study.get('details', []):
                nodes.append(Node(
                    id=detail.get('id', 'case_detail'),
                    label=detail.get('label', 'Szczegół'),
                    size=detail.get('size', 10),
                    color=detail.get('color', '#FFB347'),
                    font={"size": detail.get('font_size', 9), "color": "black"}
                ))
                edges.append(Edge(source=case_study.get('id', 'case_study'), target=detail.get('id', 'case_detail')))
        
        # Dodatkowe połączenia
        for connection in mind_map_data.get('connections', []):
            edges.append(Edge(source=connection.get('from'), target=connection.get('to')))
          # Konfiguracja
        config_data = mind_map_data.get('config', {})
        config = Config(
            width=config_data.get('width', 800),
            height=config_data.get('height', 600),
            directed=config_data.get('directed', False),
            physics=config_data.get('physics', True),
            hierarchical=config_data.get('hierarchical', False),
            nodeHighlightBehavior=True,
            highlightColor="#43C6AC",  # Zsynchronizowany z Skills Block 2
            collapsible=False
        )
        
        return agraph(nodes=nodes, edges=edges, config=config)
        
    except ImportError:
        st.error("Nie można załadować biblioteki streamlit-agraph. Zainstaluj ją używając: pip install streamlit-agraph")
        return None
    except Exception as e:
        st.error(f"Błąd podczas tworzenia data-driven mapy myśli: {str(e)}")
        return None

def create_auto_generated_mind_map(lesson_data):
    """
    Automatycznie generuje mapę myśli na podstawie struktury lekcji
    Używana dla lekcji, które nie mają dedykowanej struktury mind_map
    
    Args:
        lesson_data (dict): Dane lekcji w formacie JSON
    """
    try:
        from streamlit_agraph import agraph, Node, Edge, Config
        
        nodes = []
        edges = []
        
        # Informacja o automatycznym generowaniu
        st.info("🤖 Ta mapa myśli została wygenerowana automatycznie na podstawie struktury lekcji. "
               "Aby dodać dedykowaną mapę myśli, dodaj sekcję 'mind_map' do pliku JSON lekcji.")
          # Centralny węzeł z tytułem lekcji - kolor z bloku 2 Skills (morski)
        title = lesson_data.get('title', 'Lekcja')
        nodes.append(Node(id="central", 
                         label=f"📚 {title}", 
                         size=25,
                         color="#43C6AC",
                         font={"size": 14, "color": "#43C6AC"}))
          # Dodaj sekcje lekcji jako węzły - używa kolorów zsynchronizowanych z blokami Skills
        if 'sections' in lesson_data:
            sections = lesson_data['sections']
              # Kolory zsynchronizowane z Skills section blocks (pierwsze kolory gradientów)
            section_colors = [
                "#FF9950",  # Block 1: Emocje & Mózg (pomarańczowy-czerwony)
                "#43C6AC",  # Block 2: Wewnętrzny Kompas (morski-zielony)
                "#667eea",  # Block 3: Świadomość Działania (niebieski-fioletowy)
                "#f093fb",  # Block 4: Elastyczność & Testowanie (różowy-magenta)
                "#4facfe",  # Block 5: Mistrzostwo & Wspólnota (niebieski-cyan)
                "#FF9950",  # Cycle back to Block 1 for additional sections
                "#43C6AC",  # Block 2 repeated
                "#667eea",  # Block 3 repeated
                "#f093fb",  # Block 4 repeated
                "#4facfe"   # Block 5 repeated
            ]
            
            if 'learning' in sections and 'sections' in sections['learning']:
                for i, section in enumerate(sections['learning']['sections']):
                    section_id = f"section_{i}"
                    section_title = section.get('title', f'Sekcja {i+1}')
                    # Usuń emoji z początku tytułu
                    section_title = re.sub(r'^[^\w\s]+\s*', '', section_title)
                    # Skróć tytuł jeśli jest za długi
                    if len(section_title) > 60:
                        section_title = section_title[:57] + "..."
                    
                    # Użyj koloru z palety zsynchronizowanej z blokami Skills
                    color = section_colors[i % len(section_colors)]
                    
                    nodes.append(Node(id=section_id,
                                    label=section_title,
                                    size=15,
                                    color=color,
                                    font={"size": 10, "color": color}))
                    edges.append(Edge(source="central", target=section_id))
        
        # Dodaj elementy standardowe lekcji
        standard_elements = []
          # Quiz jeśli istnieje - kolor z bloku 4 (różowy)
        if lesson_data.get('sections', {}).get('opening_quiz'):
            standard_elements.append({"id": "quiz", "label": "🧠 Quiz", "color": "#f093fb"})
        
        # Refleksja jeśli istnieje - kolor z bloku 5 (niebieski-cyan)
        if lesson_data.get('sections', {}).get('reflection'):
            standard_elements.append({"id": "reflection", "label": "🤔 Refleksja", "color": "#4facfe"})
          # XP Reward - kolor z bloku 1 (pomarańczowy)
        if lesson_data.get('xp_reward'):
            xp = lesson_data.get('xp_reward', 0)
            standard_elements.append({"id": "xp", "label": f"⭐ {xp} XP", "color": "#FF9950"})
        
        # Dodaj inne elementy - kolory zsynchronizowane z blokami Skills
        standard_elements.extend([
            {"id": "summary", "label": "📝 Podsumowanie", "color": "#667eea"},  # Block 3 color
            {"id": "practice", "label": "💪 Ćwiczenia", "color": "#f093fb"}     # Block 4 color
        ])
        
        for element in standard_elements:
            nodes.append(Node(id=element["id"],
                            label=element["label"],
                            size=12,
                            color=element["color"],
                            font={"size": 10, "color": element["color"]}))
            edges.append(Edge(source="central", target=element["id"]))
        
        config = Config(width=700, 
                       height=500,
                       directed=False,
                       physics=True,
                       hierarchical=False,
                       nodeHighlightBehavior=True,
                       highlightColor="#43C6AC")  # Zsynchronizowany z Skills Block 2
        
        return agraph(nodes=nodes, edges=edges, config=config)
        
    except ImportError:
        st.error("Nie można załadować biblioteki streamlit-agraph. Zainstaluj ją używając: pip install streamlit-agraph")
        return None
    except Exception as e:
        st.error(f"Błąd podczas tworzenia auto-generated mapy myśli: {str(e)}")
        return None
