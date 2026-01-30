"""
Test sprawdzający czy weasyprint działa poprawnie
"""

from weasyprint import HTML, CSS

html_content = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Test PDF</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        h1 {
            color: #667eea;
        }
    </style>
</head>
<body>
    <h1>Test polskich znaków</h1>
    <p>Ąą, Ćć, Ęę, Łł, Ńń, Óó, Śś, Źź, Żż</p>
    <p>To jest test generowania PDF z polskimi znakami.</p>
    <h2>Sekcja testowa</h2>
    <ul>
        <li>Element 1 - ąćęłńóśźż</li>
        <li>Element 2 - ĄĆĘŁŃÓŚŹŻ</li>
        <li>Element 3 - ✅ ❌ 🎯 📊</li>
    </ul>
</body>
</html>
"""

try:
    print("🔄 Generuję PDF z weasyprint...")
    pdf_bytes = HTML(string=html_content).write_pdf()
    
    # Zapisz do pliku
    with open("test_weasyprint.pdf", "wb") as f:
        f.write(pdf_bytes)
    
    print(f"✅ PDF wygenerowany pomyślnie! Rozmiar: {len(pdf_bytes)} bajtów")
    print("📄 Plik zapisany jako: test_weasyprint.pdf")
    
except Exception as e:
    print(f"❌ Błąd: {str(e)}")
    print("\nWeasyprint wymaga GTK3 na Windows.")
    print("Alternatywne rozwiązanie: użyj xhtml2pdf lub generuj HTML i drukuj przez przeglądarkę.")
