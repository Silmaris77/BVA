#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Konwerter README.md do PDF
Konwertuje plik README.md na dokument PDF z zachowaniem formatowania
"""

import markdown2
import os
from datetime import datetime

def convert_markdown_to_html():
    """Konwertuje README.md do HTML"""
    
    # Ścieżki plików
    readme_path = "README.md"
    html_path = "README.html"
    
    print("🔄 Konwertuję README.md do HTML...")
    
    try:
        # Wczytaj plik README.md
        with open(readme_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Konwertuj Markdown do HTML
        html_content = markdown2.markdown(
            markdown_content, 
            extras=[
                'fenced-code-blocks',  # Bloki kodu ```
                'tables',              # Tabele
                'task_list',           # Checklisty
                'toc',                 # Spis treści
                'header-ids',          # ID nagłówków
                'metadata',            # Metadane
                'footnotes',           # Przypisy
                'smarty-pants'         # Inteligentna interpunkcja
            ]
        )
        
        # CSS do formatowania
        css_style = """
        <style>
        @media print {
            @page {
                size: A4;
                margin: 2cm;
            }
            body { font-size: 11px; }
        }
        
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        h1 {
            color: #2c3e50;
            font-size: 28px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
            margin-bottom: 20px;
        }
        
        h2 {
            color: #34495e;
            font-size: 22px;
            margin-top: 25px;
            margin-bottom: 15px;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
        }
        
        h3 {
            color: #2c3e50;
            font-size: 18px;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        h4 {
            color: #7f8c8d;
            font-size: 16px;
            margin-top: 15px;
            margin-bottom: 8px;
        }
        
        code {
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            color: #e74c3c;
        }
        
        pre {
            background-color: #f8f9fa;
            border: 1px solid #e1e8ed;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            margin: 16px 0;
        }
        
        pre code {
            background: none;
            padding: 0;
            color: #333;
        }
        
        blockquote {
            border-left: 4px solid #3498db;
            margin: 16px 0;
            padding: 8px 16px;
            background-color: #f8f9fa;
            font-style: italic;
        }
        
        ul, ol {
            margin: 12px 0;
            padding-left: 30px;
        }
        
        li {
            margin: 6px 0;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 10px 12px;
            text-align: left;
        }
        
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        
        a {
            color: #3498db;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        .footer {
            margin-top: 50px;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }
        </style>
        """
        
        # Kompletny HTML z nagłówkiem
        full_html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZenDegenAcademy - Dokumentacja</title>
    {css_style}
</head>
<body>
    {html_content}
    <div class="footer">
        <hr>
        <p>Dokumentacja wygenerowana automatycznie dnia {datetime.now().strftime('%d.%m.%Y o %H:%M')}</p>
        <p><strong>ZenDegenAcademy v1.2.0</strong> | github.com/Silmaris77/BVA</p>
    </div>
</body>
</html>"""
        
        # Zapisz do HTML
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"✅ HTML został utworzony: {html_path}")
        print(f"📄 Rozmiar pliku: {os.path.getsize(html_path) / 1024:.1f} KB")
        
        return html_path
        
    except Exception as e:
        print(f"❌ Błąd podczas konwersji: {str(e)}")
        return None

if __name__ == "__main__":
    print("🎓 ZenDegenAcademy - Konwerter README do HTML")
    print("=" * 50)
    
    html_file = convert_markdown_to_html()
    if html_file:
        print(f"\n🎉 Konwersja zakończona pomyślnie!")
        print(f"📁 Plik HTML dostępny jako: {html_file}")
        print(f"🖨️  Aby uzyskać PDF:")
        print(f"   1. Otwórz plik {html_file} w przeglądarce")
        print(f"   2. Użyj Ctrl+P (Drukuj)")
        print(f"   3. Wybierz 'Zapisz jako PDF'")
        print(f"   4. Ustaw orientację na 'Pionowa' i marginesy na 'Minimum'")
    else:
        print("\n💥 Konwersja nie powiodła się!")