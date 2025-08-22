"""
Narzędzie do zmiany kolorów zakładek w ZenDegenAcademy
"""

def change_tab_colors(inactive_color="#e9ecef", active_color="#ffffff"):
    """
    Zmienia kolory zakładek w aplikacji
    
    Args:
        inactive_color: Kolor nieaktywnych zakładek (hex)
        active_color: Kolor aktywnej zakładki (hex)
    """
    import os
    
    file_path = "utils/material3_components.py"
    
    # Sprawdź czy plik istnieje
    if not os.path.exists(file_path):
        print(f"❌ Nie znaleziono pliku: {file_path}")
        return False
    
    # Wczytaj zawartość pliku
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Znajdź sekcję ze stylami zakładek
    old_pattern = '''    .stTabs [aria-selected="true"] {
        background-color: rgba(33, 150, 243, 0.1) !important;
        font-weight: 500 !important;
        color: #1976D2 !important;
    }
    
    /* Kolory tekstu zakładek */
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important; /* Biały dla nieaktywnych zakładek */
        text-shadow: 0 0 2px rgba(255, 255, 255, 0.6) !important;
        opacity: 0.7 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        opacity: 1 !important;
    }'''
    
    new_pattern = f'''    .stTabs [aria-selected="true"] {{
        background-color: rgba(33, 150, 243, 0.1) !important;
        font-weight: 500 !important;
        color: {active_color} !important;
        text-shadow: 0 0 3px rgba(255, 255, 255, 0.8) !important;
    }}
    
    /* Kolory tekstu zakładek */
    .stTabs [data-baseweb="tab"] {{
        color: {inactive_color} !important; /* Kolor nieaktywnych zakładek */
        text-shadow: 0 0 2px rgba(255, 255, 255, 0.6) !important;
        opacity: 0.7 !important;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        opacity: 1 !important;
    }}'''
    
    # Zastąp stary wzór nowym
    if old_pattern in content:
        new_content = content.replace(old_pattern, new_pattern)
        
        # Zapisz zmieniony plik
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Zaktualizowano kolory zakładek:")
        print(f"   📝 Nieaktywne: {inactive_color}")
        print(f"   ✨ Aktywna: {active_color}")
        return True
    else:
        print("❌ Nie znaleziono sekcji stylów zakładek do zmiany")
        return False

if __name__ == "__main__":
    print("🎨 Narzędzie do zmiany kolorów zakładek")
    print("=" * 40)
    
    # Przykłady użycia
    print("\n📚 Przykłady kolorów:")
    examples = [
        ("Bardzo jasny szary (domyślny)", "#e9ecef", "#ffffff"),
        ("Prawie biały", "#f8f9fa", "#ffffff"),
        ("Jasny szary", "#ced4da", "#ffffff"),
        ("Średnio-jasny szary", "#adb5bd", "#ffffff"),
        ("Jasny niebieski", "#74c0fc", "#ffffff"),
        ("Jasny zielony", "#51cf66", "#ffffff")
    ]
    
    for i, (name, inactive, active) in enumerate(examples, 1):
        print(f"{i}. {name}: nieaktywne={inactive}, aktywne={active}")
    
    print("\n" + "=" * 40)
    print("Aby zmienić kolory, wywołaj:")
    print("change_tab_colors('#twoj-kolor-nieaktywny', '#twoj-kolor-aktywny')")
    print("\nLub użyj jednego z przykładów powyżej.")
