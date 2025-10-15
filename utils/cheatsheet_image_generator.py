"""
Generator obrazu PNG/JPG z cheatsheet HTML
"""
from html2image import Html2Image
from bs4 import BeautifulSoup
import json

def generate_cheatsheet_image(lesson_title: str, cheatsheet_html: str, format: str = 'png') -> bytes:
    """
    Generuje obraz (PNG lub JPG) z cheatsheet HTML w układzie poziomym (2 kolumny)
    
    Args:
        lesson_title: Tytuł lekcji
        cheatsheet_html: HTML z cheatsheet
        format: 'png' lub 'jpg'
    
    Returns:
        bytes: Dane obrazu
    """
    hti = Html2Image(output_path='temp')
    
    # Parsuj HTML i podziel sekcje na dwie kolumny
    soup = BeautifulSoup(cheatsheet_html, 'html.parser')
    all_divs = soup.find_all('div', recursive=False)
    
    # Header (pierwszy div) idzie na górę
    header = str(all_divs[0]) if all_divs else ''
    
    # Pozostałe sekcje dzielimy na dwie kolumny
    # Lewa kolumna zawsze ma tyle samo lub więcej elementów niż prawa
    sections = all_divs[1:] if len(all_divs) > 1 else []
    mid = (len(sections) + 1) // 2  # Zaokrąglenie w górę dla lewej kolumny
    
    left_column = ''.join(str(div) for div in sections[:mid])
    right_column = ''.join(str(div) for div in sections[mid:])
    
    # Pełny HTML z układem dwukolumnowym
    full_html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
                background: #ffffff;
                padding: 25px;
                width: 1600px;
                color: #424242;
            }}
            
            .two-column-layout {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 25px;
                margin-top: 20px;
            }}
            
            .column {{
                display: flex;
                flex-direction: column;
                gap: 20px;
            }}
            .column {{
                display: flex;
                flex-direction: column;
                gap: 20px;
            }}
            
            /* Style identyczne jak w aplikacji */
            h1, h2, h3, h4, h5, h6 {{
                margin: 0;
                font-weight: 600;
            }}
            
            ul {{
                list-style-type: disc;
            }}
            
            li {{
                margin-bottom: 4px;
            }}
            
            /* Grid layouts */
            [style*="display: grid"] {{
                display: grid !important;
            }}
            
            [style*="grid-template-columns: 1fr 1fr 1fr"] {{
                grid-template-columns: 1fr 1fr 1fr !important;
            }}
            
            [style*="grid-template-columns: 1fr 1fr"] {{
                grid-template-columns: 1fr 1fr !important;
            }}
            
            /* Karty z kolorowymi ramkami */
            [style*="border-left: 5px solid"] {{
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            }}
            
            /* Białe tło wewnętrznych kart */
            [style*="background: white"] {{
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            }}
            
            /* Responsywne marginesy */
            [style*="margin-bottom"] {{
                margin-bottom: var(--margin, 10px);
            }}
            
            /* Zachowaj wszystkie inline style */
            [style] {{
                /* Style inline mają najwyższy priorytet */
            }}
        </style>
    </head>
    <body>
        <!-- Header na górze -->
        {header}
        
        <!-- Dwie kolumny z sekcjami -->
        <div class="two-column-layout">
            <div class="column">
                {left_column}
            </div>
            <div class="column">
                {right_column}
            </div>
        </div>
    </body>
    </html>
    '''
    
    # Generuj obraz - format poziomy: szerokość 1700px, wysokość ~2000px
    screenshot_path = hti.screenshot(
        html_str=full_html,
        save_as=f'cheatsheet.{format}',
        size=(1700, 2000)
    )
    
    # Wczytaj i zwróć jako bytes
    if screenshot_path:
        with open(screenshot_path[0], 'rb') as f:
            return f.read()
    
    return None


# Test
if __name__ == '__main__':
    print("="*70)
    print("TEST GENERATORA OBRAZU")
    print("="*70)
    
    with open('data/lessons/11. Od słów do zaufania - Conversational Intelligence.json', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\nGeneruję PNG...")
    image_data = generate_cheatsheet_image(
        lesson_title=data['title'],
        cheatsheet_html=data['summary']['cheatsheet'],
        format='png'
    )
    
    if image_data:
        with open('test_cheatsheet.png', 'wb') as f:
            f.write(image_data)
        print(f"✅ Zapisano: test_cheatsheet.png ({len(image_data):,} bajtów)")
    else:
        print("❌ Błąd generowania")
    
    print("\n" + "="*70)
