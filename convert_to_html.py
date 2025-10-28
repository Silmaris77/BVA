"""
FMCG Simulator - Prosty konwerter Markdown → HTML
Generuje HTML z dokumentów (łatwo przekonwertować na PDF z przeglądarki)
"""

from pathlib import Path
import markdown
from datetime import datetime

# Lista plików do konwersji
FILES_TO_CONVERT = [
    {
        'input': 'FMCG_PRESENTATION_SLIDES.md',
        'output': 'FMCG_Presentation_Part1.html',
        'title': 'FMCG Sales Simulator - Prezentacja (Część 1)'
    },
    {
        'input': 'FMCG_PRESENTATION_SLIDES_PART2.md',
        'output': 'FMCG_Presentation_Part2.html',
        'title': 'FMCG Sales Simulator - Prezentacja (Część 2)'
    },
    {
        'input': 'FMCG_MVP_SUMMARY.md',
        'output': 'FMCG_Executive_Summary.html',
        'title': 'FMCG Sales Simulator - Executive Summary'
    },
    {
        'input': 'FMCG_OUTCOMES_SPEC.md',
        'output': 'FMCG_Technical_Spec.html',
        'title': 'FMCG Sales Simulator - Technical Specification'
    },
    {
        'input': 'FMCG_UI_MOCKUPS_PART1.md',
        'output': 'FMCG_UI_Mockups_Part1.html',
        'title': 'FMCG Sales Simulator - UI Mockups (Część 1)'
    },
    {
        'input': 'FMCG_UI_MOCKUPS_PART2.md',
        'output': 'FMCG_UI_Mockups_Part2.html',
        'title': 'FMCG Sales Simulator - UI Mockups (Część 2)'
    },
    {
        'input': 'FMCG_PRESENTATION_PACKAGE_SUMMARY.md',
        'output': 'FMCG_Package_Summary.html',
        'title': 'FMCG Sales Simulator - Package Summary'
    }
]

# HTML template z professional styling
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @media print {{
            @page {{
                size: A4;
                margin: 2cm 1.5cm;
            }}
            
            h1, h2, h3 {{
                page-break-after: avoid;
            }}
            
            pre, table {{
                page-break-inside: avoid;
            }}
            
            .no-print {{
                display: none !important;
            }}
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #1a5490;
        }}
        
        .header h1 {{
            color: #1a5490;
            font-size: 28pt;
            margin-bottom: 10px;
        }}
        
        .header .meta {{
            color: #666;
            font-size: 10pt;
        }}
        
        h1 {{
            color: #1a5490;
            font-size: 24pt;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            border-bottom: 2px solid #1a5490;
            padding-bottom: 0.3em;
        }}
        
        h2 {{
            color: #2874a6;
            font-size: 18pt;
            margin-top: 1.2em;
            margin-bottom: 0.4em;
        }}
        
        h3 {{
            color: #34495e;
            font-size: 14pt;
            margin-top: 1em;
            margin-bottom: 0.3em;
        }}
        
        h4 {{
            color: #5d6d7e;
            font-size: 12pt;
            margin-top: 0.8em;
            margin-bottom: 0.3em;
        }}
        
        p {{
            margin-bottom: 0.8em;
        }}
        
        pre {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-left: 4px solid #1a5490;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
            margin: 1em 0;
            font-family: 'Courier New', Courier, monospace;
            font-size: 9pt;
            line-height: 1.4;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        
        code {{
            font-family: 'Courier New', Courier, monospace;
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 9pt;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
            font-size: 10pt;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        
        th {{
            background-color: #1a5490;
            color: white;
            font-weight: bold;
        }}
        
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        tr:hover {{
            background-color: #f5f5f5;
        }}
        
        ul, ol {{
            margin-left: 2em;
            margin-bottom: 1em;
        }}
        
        li {{
            margin-bottom: 0.4em;
        }}
        
        blockquote {{
            border-left: 4px solid #1a5490;
            margin-left: 0;
            padding-left: 1em;
            color: #555;
            font-style: italic;
            margin: 1em 0;
        }}
        
        a {{
            color: #1a5490;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 2em 0;
        }}
        
        .toolbar {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
        }}
        
        .toolbar button {{
            background-color: #1a5490;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11pt;
            margin: 5px 0;
            width: 100%;
        }}
        
        .toolbar button:hover {{
            background-color: #2874a6;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 9pt;
        }}
        
        /* Highlight dla ważnych elementów */
        .highlight {{
            background-color: #fff3cd;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        
        /* Badges */
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 9pt;
            font-weight: bold;
            margin: 0 4px;
        }}
        
        .badge-success {{ background-color: #d4edda; color: #155724; }}
        .badge-warning {{ background-color: #fff3cd; color: #856404; }}
        .badge-danger {{ background-color: #f8d7da; color: #721c24; }}
        .badge-info {{ background-color: #d1ecf1; color: #0c5460; }}
    </style>
</head>
<body>
    <div class="toolbar no-print">
        <button onclick="window.print()">🖨️ Drukuj / Zapisz PDF</button>
        <button onclick="window.location.href='index.html'">📂 Wszystkie pliki</button>
    </div>
    
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <div class="meta">
                Wygenerowano: {date}<br>
                Dokument źródłowy: <code>{source_file}</code>
            </div>
        </div>
        
        <div class="content">
            {content}
        </div>
        
        <div class="footer">
            <p>FMCG Sales Simulator &copy; 2025 | Wersja dokumentu: 1.0</p>
            <p style="margin-top: 10px; font-size: 8pt;">
                💡 <strong>Tip:</strong> Użyj Ctrl+P (Cmd+P na Mac) aby zapisać jako PDF<br>
                W opcjach drukowania wybierz "Zapisz jako PDF"
            </p>
        </div>
    </div>
    
    <script>
        // Automatyczne numerowanie nagłówków
        document.querySelectorAll('h2').forEach((h, i) => {{
            if (!h.textContent.match(/^\\d+\\./)) {{
                h.textContent = (i + 1) + '. ' + h.textContent;
            }}
        }});
    </script>
</body>
</html>
"""


def convert_md_to_html(input_file, output_file, title):
    """Konwertuje plik Markdown na HTML"""
    
    print(f"📄 Konwertowanie: {input_file} → {output_file}")
    
    # Wczytaj plik Markdown
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"  ❌ Plik nie znaleziony: {input_file}")
        return False
    
    # Konwertuj Markdown → HTML
    try:
        html_content = markdown.markdown(
            md_content,
            extensions=[
                'tables',
                'fenced_code',
                'codehilite',
                'nl2br',
                'sane_lists',
                'smarty'
            ]
        )
    except Exception as e:
        print(f"  ❌ Błąd konwersji Markdown: {e}")
        return False
    
    # Wygeneruj pełny HTML
    full_html = HTML_TEMPLATE.format(
        title=title,
        date=datetime.now().strftime('%d.%m.%Y %H:%M'),
        source_file=input_file,
        content=html_content
    )
    
    # Zapisz HTML
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"  ✅ Sukces! Utworzono: {output_file}")
        return True
    except Exception as e:
        print(f"  ❌ Błąd zapisu pliku: {e}")
        return False


def create_index():
    """Tworzy stronę główną z linkami do wszystkich dokumentów"""
    
    index_html = """<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FMCG Simulator - Dokumentacja</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        
        h1 {
            color: #1a5490;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
        }
        
        .doc-list {
            list-style: none;
            padding: 0;
        }
        
        .doc-item {
            background: #f8f9fa;
            margin: 15px 0;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #1a5490;
            transition: all 0.3s;
        }
        
        .doc-item:hover {
            background: #e9ecef;
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .doc-item a {
            text-decoration: none;
            color: #1a5490;
            font-size: 16pt;
            font-weight: bold;
            display: block;
            margin-bottom: 8px;
        }
        
        .doc-desc {
            color: #666;
            font-size: 11pt;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 9pt;
            font-weight: bold;
            margin-left: 10px;
        }
        
        .badge-presentation { background-color: #d1ecf1; color: #0c5460; }
        .badge-technical { background-color: #fff3cd; color: #856404; }
        .badge-ui { background-color: #d4edda; color: #155724; }
        
        .instructions {
            background: #fff3cd;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
            border-left: 4px solid #856404;
        }
        
        .instructions h3 {
            color: #856404;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎮 FMCG Sales Simulator</h1>
        <p class="subtitle">Kompletna Dokumentacja Projektu</p>
        
        <ul class="doc-list">
"""
    
    for file_info in FILES_TO_CONVERT:
        # Określ typ dokumentu
        if 'Presentation' in file_info['output']:
            badge = '<span class="badge badge-presentation">Prezentacja</span>'
        elif 'Technical' in file_info['output'] or 'Outcomes' in file_info['output']:
            badge = '<span class="badge badge-technical">Techniczna</span>'
        elif 'UI' in file_info['output']:
            badge = '<span class="badge badge-ui">UI/UX</span>'
        else:
            badge = '<span class="badge badge-technical">Dokumentacja</span>'
        
        index_html += f"""
            <li class="doc-item">
                <a href="{file_info['output']}">{file_info['title']} {badge}</a>
                <div class="doc-desc">Źródło: <code>{file_info['input']}</code></div>
            </li>
"""
    
    index_html += """
        </ul>
        
        <div class="instructions">
            <h3>📥 Jak zapisać jako PDF?</h3>
            <ol>
                <li>Kliknij link do wybranego dokumentu</li>
                <li>Naciśnij <strong>Ctrl+P</strong> (Windows) lub <strong>Cmd+P</strong> (Mac)</li>
                <li>Wybierz "Zapisz jako PDF" jako drukarkę</li>
                <li>Dostosuj ustawienia (orientacja, marginesy)</li>
                <li>Kliknij "Zapisz"</li>
            </ol>
            
            <p style="margin-top: 15px; color: #856404;">
                <strong>💡 Tip:</strong> Dla najlepszej jakości PDF użyj przeglądarki Chrome lub Edge
            </p>
        </div>
        
        <div style="text-align: center; margin-top: 30px; color: #666; font-size: 10pt;">
            <p>Wygenerowano: """ + datetime.now().strftime('%d.%m.%Y %H:%M') + """</p>
            <p>FMCG Sales Simulator © 2025</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print("✅ Utworzono index.html (strona główna)")


def main():
    """Główna funkcja - konwertuje wszystkie pliki"""
    
    print("=" * 70)
    print("  FMCG SIMULATOR - KONWERTER MARKDOWN → HTML → PDF")
    print("=" * 70)
    print()
    print(f"📋 Znaleziono {len(FILES_TO_CONVERT)} plików do konwersji")
    print()
    
    # Konwertuj każdy plik
    success_count = 0
    for file_info in FILES_TO_CONVERT:
        if convert_md_to_html(
            file_info['input'],
            file_info['output'],
            file_info['title']
        ):
            success_count += 1
        print()
    
    # Stwórz index
    print("📂 Tworzenie strony głównej...")
    create_index()
    print()
    
    # Podsumowanie
    print("=" * 70)
    print(f"✅ ZAKOŃCZONO: {success_count}/{len(FILES_TO_CONVERT)} plików przekonwertowanych")
    print("=" * 70)
    
    if success_count > 0:
        print()
        print("📂 Pliki HTML znajdują się w:")
        print(f"   {Path.cwd()}")
        print()
        print("🌐 Otwórz w przeglądarce:")
        print(f"   file:///{Path.cwd()}/index.html")
        print()
        print("📥 Aby zapisać jako PDF:")
        print("   1. Otwórz plik HTML w przeglądarce")
        print("   2. Naciśnij Ctrl+P (Cmd+P na Mac)")
        print("   3. Wybierz 'Zapisz jako PDF'")
        print("   4. Gotowe!")
        print()
        print("📧 HTML można też wysłać bezpośrednio klientowi!")


if __name__ == '__main__':
    main()
