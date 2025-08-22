"""
Generator szablonów map myśli dla nowych lekcji
"""
import json

def generate_mind_map_template(lesson_title, main_topics, include_case_study=True):
    """
    Generuje template JSON dla mapy myśli na podstawie tytułu lekcji i głównych tematów
    
    Args:
        lesson_title (str): Tytuł lekcji
        main_topics (list): Lista głównych tematów/kategorii
        include_case_study (bool): Czy dołączyć case study
    
    Returns:
        dict: Template mapy myśli gotowy do dodania do JSON lekcji
    """
    
    # Kolory dla różnych kategorii
    category_colors = [
        "#4ECDC4",  # Morski
        "#45B7D1",  # Niebieski
        "#96CEB4",  # Miętowy
        "#FECA57",  # Żółty
        "#A29BFE",  # Fioletowy
        "#FD79A8",  # Różowy
        "#FDCB6E",  # Pomarańczowy
        "#E17055"   # Koralowy
    ]
    
    template = {
        "mind_map": {
            "central_node": {
                "id": "main_topic",
                "label": f"💡 {lesson_title.upper()}",
                "size": 25,
                "color": "#FF6B6B",
                "font_size": 16
            },
            "categories": [],
            "solutions": [
                {
                    "id": "solution_1",
                    "label": "🔧 Praktyczne zastosowanie",
                    "size": 15,
                    "color": "#90EE90",
                    "font_size": 11
                },
                {
                    "id": "solution_2", 
                    "label": "💡 Kluczowa wskazówka",
                    "size": 15,
                    "color": "#98FB98",
                    "font_size": 11
                }
            ],
            "connections": [],
            "config": {
                "width": 800,
                "height": 600,
                "physics": True,
                "directed": False
            }
        }
    }
    
    # Dodaj kategorie na podstawie głównych tematów
    for i, topic in enumerate(main_topics):
        color = category_colors[i % len(category_colors)]
        
        category = {
            "id": f"category_{i+1}",
            "label": f"🎯 {topic}",
            "size": 20,
            "color": color,
            "font_size": 12,
            "details": [
                {
                    "id": f"detail_{i+1}_1",
                    "label": "Kluczowy punkt 1",
                    "size": 12,
                    "color": "#DDA0DD",
                    "font_size": 10
                },
                {
                    "id": f"detail_{i+1}_2",
                    "label": "Kluczowy punkt 2", 
                    "size": 12,
                    "color": "#DDA0DD",
                    "font_size": 10
                }
            ]
        }
        
        template["mind_map"]["categories"].append(category)
        
        # Dodaj połączenie od centralnego węzła
        template["mind_map"]["connections"].append({
            "from": "main_topic",
            "to": f"category_{i+1}"
        })
    
    # Dodaj case study jeśli wymagane
    if include_case_study:
        template["mind_map"]["case_study"] = {
            "id": "case_main",
            "label": "📱 Studium przypadku",
            "size": 18,
            "color": "#FF8C42",
            "font_size": 12,
            "details": [
                {
                    "id": "case_detail_1",
                    "label": "Problem",
                    "size": 10,
                    "color": "#FFB347",
                    "font_size": 9
                },
                {
                    "id": "case_detail_2",
                    "label": "Rozwiązanie",
                    "size": 10,
                    "color": "#FFB347", 
                    "font_size": 9
                }
            ]
        }
    
    return template

def create_mind_map_for_lesson(lesson_id, lesson_title, categories):
    """
    Tworzy konkretną mapę myśli dla określonej lekcji
    
    Args:
        lesson_id (str): ID lekcji (np. "B1C1L2")
        lesson_title (str): Tytuł lekcji
        categories (list): Lista słowników z kategoriami
        
    Returns:
        dict: Gotowa struktura mind_map
    """
    
    # Przykłady dla różnych typów lekcji
    lesson_templates = {
        "psychology": {
            "icon": "🧠",
            "solutions": [
                "🔍 Zoom out - szeroka perspektywa",
                "📋 Trzymaj się strategii", 
                "⏸️ Zatrzymaj się i przemyśl"
            ]
        },
        "technical": {
            "icon": "⚙️",
            "solutions": [
                "📊 Analiza danych",
                "🛠️ Praktyczne narzędzia",
                "📈 Monitoring wyników"
            ]
        },
        "strategy": {
            "icon": "🎯", 
            "solutions": [
                "📝 Plan działania",
                "⚖️ Zarządzanie ryzykiem",
                "🎪 Dywersyfikacja"
            ]
        }
    }
    
    # Automatycznie rozpoznaj typ lekcji na podstawie tytułu
    lesson_type = "psychology"  # domyślny
    if any(word in lesson_title.lower() for word in ["analiza", "technical", "wskaźnik"]):
        lesson_type = "technical"
    elif any(word in lesson_title.lower() for word in ["strategia", "portfel", "plan"]):
        lesson_type = "strategy"
    
    template_data = lesson_templates[lesson_type]
    
    mind_map = {
        "central_node": {
            "id": "main_topic",
            "label": f"{template_data['icon']} {lesson_title.upper()}",
            "size": 25,
            "color": "#FF6B6B",
            "font_size": 16
        },
        "categories": [],
        "solutions": [],
        "connections": [],
        "config": {
            "width": 800,
            "height": 600,
            "physics": True,
            "directed": False
        }
    }
    
    # Dodaj kategorie
    colors = ["#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57", "#A29BFE"]
    for i, category in enumerate(categories):
        cat_data = {
            "id": f"category_{i+1}",
            "label": category["label"],
            "size": 20,
            "color": colors[i % len(colors)],
            "font_size": 12,
            "details": category.get("details", [])
        }
        mind_map["categories"].append(cat_data)
        mind_map["connections"].append({
            "from": "main_topic",
            "to": f"category_{i+1}"
        })
    
    # Dodaj rozwiązania
    for i, solution in enumerate(template_data["solutions"]):
        mind_map["solutions"].append({
            "id": f"solution_{i+1}",
            "label": solution,
            "size": 15,
            "color": "#90EE90",
            "font_size": 11
        })
    
    return {"mind_map": mind_map}

def save_template_to_file(template, filename):
    """
    Zapisuje template do pliku JSON
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    print(f"✅ Template zapisany do: {filename}")

# Przykłady użycia
if __name__ == "__main__":
    
    # Przykład 1: Podstawowy template
    basic_template = generate_mind_map_template(
        "Podstawy analizy technicznej",
        ["Wskaźniki techniczne", "Formacje cenowe", "Volume analysis", "Support i Resistance"]
    )
    
    # Przykład 2: Template dla konkretnej lekcji
    lesson_template = create_mind_map_for_lesson(
        "B1C1L2",
        "Zarządzanie emocjami",
        [
            {
                "label": "🎭 Rodzaje emocji",
                "details": [
                    {"id": "fear", "label": "😨 Strach", "size": 12, "color": "#DDA0DD", "font_size": 10},
                    {"id": "greed", "label": "🤑 Chciwość", "size": 12, "color": "#DDA0DD", "font_size": 10}
                ]
            },
            {
                "label": "🛠️ Techniki kontroli",
                "details": [
                    {"id": "meditation", "label": "🧘 Medytacja", "size": 12, "color": "#DDA0DD", "font_size": 10},
                    {"id": "planning", "label": "📋 Planowanie", "size": 12, "color": "#DDA0DD", "font_size": 10}
                ]
            }
        ]
    )
    
    print("📋 Przykładowe szablony wygenerowane!")
    print("Użyj funkcji save_template_to_file() aby zapisać template do pliku.")
