"""
Generator PDF dla materiałów edukacyjnych
Umożliwia generowanie PDF z cheatsheetów i innych materiałów
"""

import streamlit as st
import base64
from io import BytesIO
import html

def generate_pdf_content(title, content_html):
    """
    Generuje kompletny HTML który może być łatwo konwertowany do PDF
    
    Args:
        title (str): Tytuł dokumentu
        content_html (str): Zawartość HTML
    
    Returns:
        str: Kompletny HTML do konwersji PDF
    """
    
    # CSS specjalnie dostosowany do druku PDF
    css_styles = """
    <style>
        @page {
            size: A4;
            margin: 1.5cm;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Arial', sans-serif;
            font-size: 11px;
            line-height: 1.4;
            color: #333;
            max-width: 100%;
            margin: 0;
            padding: 0;
        }
        
        h1, h2, h3, h4, h5 {
            color: #2c3e50;
            margin-top: 1em;
            margin-bottom: 0.5em;
            page-break-after: avoid;
        }
        
        h1 { font-size: 20px; }
        h2 { font-size: 16px; }
        h3 { font-size: 14px; }
        h4 { font-size: 12px; }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #667eea;
        }
        
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            background: #f8f9fa;
            page-break-inside: avoid;
        }
        
        .card h3, .card h4 {
            margin-top: 0;
            color: #667eea;
        }
        
        ul, ol {
            margin: 0.5em 0;
            padding-left: 20px;
        }
        
        li {
            margin-bottom: 0.3em;
        }
        
        .highlight {
            background: #fff3cd;
            padding: 10px;
            border-left: 4px solid #ffc107;
            margin: 10px 0;
        }
        
        .success {
            background: #d4edda;
            padding: 10px;
            border-left: 4px solid #28a745;
            margin: 10px 0;
        }
        
        .info {
            background: #d1ecf1;
            padding: 10px;
            border-left: 4px solid #17a2b8;
            margin: 10px 0;
        }
        
        .footer {
            position: fixed;
            bottom: 1cm;
            right: 1cm;
            font-size: 9px;
            color: #666;
        }
        
        @media print {
            .no-print {
                display: none !important;
            }
        }
    </style>
    """
    
    # Generuj kompletny HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{html.escape(title)}</title>
        {css_styles}
    </head>
    <body>
        <div class="header">
            <h1>{html.escape(title)}</h1>
            <p>Business Value Academy - Materiały edukacyjne</p>
        </div>
        
        <div class="content">
            {content_html}
        </div>
        
        <div class="footer">
            Wygenerowano: {html.escape(str(__import__('datetime').datetime.now().strftime('%d.%m.%Y %H:%M')))}
        </div>
    </body>
    </html>
    """
    
    return html_content

def create_download_link(html_content, filename):
    """
    Tworzy link do pobrania HTML który można otworzyć w przeglądarce i zapisać jako PDF
    
    Args:
        html_content (str): Zawartość HTML
        filename (str): Nazwa pliku
    
    Returns:
        None: Wyświetla przycisk download w Streamlit
    """
    
    # Koduj HTML do base64
    b64_html = base64.b64encode(html_content.encode('utf-8')).decode()
    
    # Twórz link do pobrania
    href = f'data:text/html;base64,{b64_html}'
    
    # Wyświetl przycisk download
    st.markdown(
        f"""
        <div style="text-align: center; margin: 20px 0;">
            <a href="{href}" download="{filename}" 
               style="display: inline-block; padding: 10px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">
                📄 Pobierz HTML (otwórz i zapisz jako PDF)
            </a>
        </div>
        <div style="text-align: center; font-size: 0.9em; color: #666; margin-bottom: 20px;">
            💡 <strong>Instrukcja:</strong> Kliknij link → Otwórz w przeglądarce → Ctrl+P → "Zapisz jako PDF"
        </div>
        """, 
        unsafe_allow_html=True
    )

def clean_html_for_pdf(html_content):
    """
    Czyści HTML usuwając style inline które mogą przeszkadzać w PDF
    
    Args:
        html_content (str): Oryginalny HTML
    
    Returns:
        str: Wyczyszczony HTML
    """
    import re
    
    # Usuń inline styles - zastąp klasami CSS
    # Zachowaj structure ale usuń konfliktujące style
    
    # Zamień gradienty na solidne kolory
    html_content = re.sub(
        r'background: linear-gradient\([^)]+\)',
        'background: #667eea; color: white;',
        html_content
    )
    
    # Usuń bardzo specyficzne style które mogą konfliktować z PDF
    html_content = re.sub(r'style="[^"]*display:\s*grid[^"]*"', 'class="grid"', html_content)
    html_content = re.sub(r'style="[^"]*grid-template-columns[^"]*"', '', html_content)
    
    # Zamień niektóre inline style na klasy
    html_content = re.sub(
        r'style="[^"]*background:\s*#f8f9fa[^"]*"',
        'class="card"',
        html_content
    )
    
    # Uprosć style padding i margin
    html_content = re.sub(r'padding:\s*\d+px;?', 'padding: 10px;', html_content)
    html_content = re.sub(r'margin:\s*[^;]+;', 'margin: 10px 0;', html_content)
    
    return html_content

def create_simple_download_button(html_content, filename, title="Pobierz PDF"):
    """
    Tworzy prosty przycisk do pobrania z lepszą instrukcją
    
    Args:
        html_content (str): Zawartość HTML
        filename (str): Nazwa pliku
        title (str): Tekst przycisku
    
    Returns:
        None: Wyświetla przycisk download w Streamlit
    """
    import streamlit as st
    import base64
    
    # Koduj HTML do base64
    b64_html = base64.b64encode(html_content.encode('utf-8')).decode()
    
    # Utwórz kolumny dla wycentrowania
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Wyświetl przycisk download
        st.markdown(
            f"""
            <div style="text-align: center; margin: 20px 0;">
                <a href="data:text/html;base64,{b64_html}" download="{filename}" 
                   style="display: inline-block; padding: 12px 24px; 
                          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; text-decoration: none; border-radius: 8px; 
                          font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                          transition: transform 0.2s;">
                    📄 {title}
                </a>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Instrukcja
        st.info(
            "💡 **Jak zapisać jako PDF:**\n"
            "1. Kliknij przycisk powyżej\n"
            "2. Otwórz pobrany plik HTML w przeglądarce\n"
            "3. Naciśnij Ctrl+P (lub Cmd+P na Mac)\n"
            "4. Wybierz 'Zapisz jako PDF'\n"
            "5. Kliknij 'Zapisz'"
        )