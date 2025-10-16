"""
Test xhtml2pdf z polskimi znakami
"""

from xhtml2pdf import pisa
import io

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
        .info-box {
            background: #f0f7ff;
            border-left: 4px solid #4A90E2;
            padding: 20px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>Test polskich znaków</h1>
    <p>Ąą, Ćć, Ęę, Łł, Ńń, Óó, Śś, Źź, Żż</p>
    <p>To jest test generowania PDF z polskimi znakami.</p>
    
    <div class="info-box">
        <h2>Sekcja testowa</h2>
        <ul>
            <li>Element 1 - ąćęłńóśźż</li>
            <li>Element 2 - ĄĆĘŁŃÓŚŹŻ</li>
            <li>Element 3 - Test układu</li>
        </ul>
    </div>
    
    <h2>Kolumny</h2>
    <table style="width: 100%;">
        <tr>
            <td style="width: 50%; padding: 10px; border: 1px solid #ddd;">
                <strong>Kolumna 1</strong><br>
                Treść pierwszej kolumny
            </td>
            <td style="width: 50%; padding: 10px; border: 1px solid #ddd;">
                <strong>Kolumna 2</strong><br>
                Treść drugiej kolumny
            </td>
        </tr>
    </table>
</body>
</html>
"""

try:
    print("🔄 Generuję PDF z xhtml2pdf...")
    output = io.BytesIO()
    
    pisa_status = pisa.CreatePDF(
        src=html_content,
        dest=output,
        encoding='utf-8'
    )
    
    if pisa_status.err:
        print(f"❌ Błąd podczas generowania: {pisa_status.err}")
    else:
        pdf_bytes = output.getvalue()
        output.close()
        
        # Zapisz do pliku
        with open("test_xhtml2pdf.pdf", "wb") as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF wygenerowany pomyślnie! Rozmiar: {len(pdf_bytes)} bajtów")
        print("📄 Plik zapisany jako: test_xhtml2pdf.pdf")
        
except Exception as e:
    print(f"❌ Błąd: {str(e)}")
