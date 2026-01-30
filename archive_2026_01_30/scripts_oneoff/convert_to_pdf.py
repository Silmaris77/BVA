"""
FMCG Simulator - Konwerter Markdown → PDF
Generuje PDF z dokumentów prezentacyjnych
"""

from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from datetime import datetime

# Lista plików do konwersji
FILES_TO_CONVERT = [
    {
        'input': 'FMCG_PRESENTATION_SLIDES.md',
        'output': 'FMCG_Presentation_Part1.pdf',
        'title': 'FMCG Sales Simulator - Prezentacja (Część 1)'
    },
    {
        'input': 'FMCG_PRESENTATION_SLIDES_PART2.md',
        'output': 'FMCG_Presentation_Part2.pdf',
        'title': 'FMCG Sales Simulator - Prezentacja (Część 2)'
    },
    {
        'input': 'FMCG_MVP_SUMMARY.md',
        'output': 'FMCG_Executive_Summary.pdf',
        'title': 'FMCG Sales Simulator - Executive Summary'
    },
    {
        'input': 'FMCG_OUTCOMES_SPEC.md',
        'output': 'FMCG_Technical_Spec.pdf',
        'title': 'FMCG Sales Simulator - Technical Specification'
    },
    {
        'input': 'FMCG_UI_MOCKUPS_PART1.md',
        'output': 'FMCG_UI_Mockups_Part1.pdf',
        'title': 'FMCG Sales Simulator - UI Mockups (Część 1)'
    },
    {
        'input': 'FMCG_UI_MOCKUPS_PART2.md',
        'output': 'FMCG_UI_Mockups_Part2.pdf',
        'title': 'FMCG Sales Simulator - UI Mockups (Część 2)'
    },
    {
        'input': 'FMCG_PRESENTATION_PACKAGE_SUMMARY.md',
        'output': 'FMCG_Package_Summary.pdf',
        'title': 'FMCG Sales Simulator - Package Summary'
    }
]

# CSS dla PDF (professional styling)
PDF_CSS = """
@page {
    size: A4;
    margin: 2cm 1.5cm;
    @bottom-right {
        content: counter(page) " / " counter(pages);
        font-size: 10pt;
        color: #666;
    }
}

body {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
    max-width: 100%;
}

h1 {
    color: #1a5490;
    font-size: 24pt;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    border-bottom: 3px solid #1a5490;
    padding-bottom: 0.3em;
    page-break-after: avoid;
}

h2 {
    color: #2874a6;
    font-size: 18pt;
    margin-top: 1.2em;
    margin-bottom: 0.4em;
    page-break-after: avoid;
}

h3 {
    color: #34495e;
    font-size: 14pt;
    margin-top: 1em;
    margin-bottom: 0.3em;
    page-break-after: avoid;
}

pre, code {
    font-family: 'Courier New', monospace;
    background-color: #f4f4f4;
    border: 1px solid #ddd;
    border-radius: 3px;
    padding: 0.2em 0.4em;
    font-size: 9pt;
    page-break-inside: avoid;
}

pre {
    padding: 1em;
    overflow-x: auto;
    white-space: pre-wrap;
    word-wrap: break-word;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
    font-size: 10pt;
    page-break-inside: avoid;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #1a5490;
    color: white;
    font-weight: bold;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

ul, ol {
    margin-left: 1.5em;
}

li {
    margin-bottom: 0.3em;
}

blockquote {
    border-left: 4px solid #1a5490;
    margin-left: 0;
    padding-left: 1em;
    color: #555;
    font-style: italic;
}

a {
    color: #1a5490;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.page-break {
    page-break-before: always;
}

/* Emoji i symbole - zachowaj czytność */
.emoji {
    font-size: 1.2em;
}

/* ASCII art boxes */
pre.ascii-box {
    background-color: #fff;
    border: 2px solid #1a5490;
    padding: 1em;
    line-height: 1.2;
}
"""

def convert_md_to_pdf(input_file, output_file, title):
    """Konwertuje plik Markdown na PDF"""
    
    print(f"📄 Konwertowanie: {input_file} → {output_file}")
    
    # Wczytaj plik Markdown
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"  ❌ Plik nie znaleziony: {input_file}")
        return False
    
    # Konwertuj Markdown → HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite', 'nl2br']
    )
    
    # Dodaj header i styling
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
    </head>
    <body>
        <h1 style="text-align: center; color: #1a5490; border-bottom: none;">
            {title}
        </h1>
        <p style="text-align: center; color: #666; font-size: 10pt; margin-bottom: 2em;">
            Wygenerowano: {datetime.now().strftime('%d.%m.%Y %H:%M')}
        </p>
        <hr style="border: 1px solid #ddd; margin: 2em 0;">
        {html_content}
    </body>
    </html>
    """
    
    # Generuj PDF
    try:
        HTML(string=full_html).write_pdf(
            output_file,
            stylesheets=[CSS(string=PDF_CSS)]
        )
        print(f"  ✅ Sukces! Utworzono: {output_file}")
        return True
    except Exception as e:
        print(f"  ❌ Błąd podczas konwersji: {e}")
        return False


def main():
    """Główna funkcja - konwertuje wszystkie pliki"""
    
    print("=" * 70)
    print("  FMCG SIMULATOR - KONWERTER MARKDOWN → PDF")
    print("=" * 70)
    print()
    
    # Sprawdź czy weasyprint jest zainstalowany
    try:
        import weasyprint
        print("✅ WeasyPrint zainstalowany")
    except ImportError:
        print("❌ WeasyPrint nie jest zainstalowany!")
        print()
        print("Zainstaluj używając:")
        print("  pip install weasyprint markdown")
        print()
        print("UWAGA: WeasyPrint wymaga GTK3 (Windows):")
        print("  1. Pobierz: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases")
        print("  2. Zainstaluj GTK3 Runtime")
        print("  3. Uruchom ponownie skrypt")
        return
    
    print()
    print(f"📋 Znaleziono {len(FILES_TO_CONVERT)} plików do konwersji")
    print()
    
    # Konwertuj każdy plik
    success_count = 0
    for file_info in FILES_TO_CONVERT:
        if convert_md_to_pdf(
            file_info['input'],
            file_info['output'],
            file_info['title']
        ):
            success_count += 1
        print()
    
    # Podsumowanie
    print("=" * 70)
    print(f"✅ ZAKOŃCZONO: {success_count}/{len(FILES_TO_CONVERT)} plików przekonwertowanych")
    print("=" * 70)
    
    if success_count > 0:
        print()
        print("📂 Pliki PDF znajdują się w:")
        print(f"   {Path.cwd()}")
        print()
        print("📧 Gotowe do wysłania klientowi!")


if __name__ == '__main__':
    main()
