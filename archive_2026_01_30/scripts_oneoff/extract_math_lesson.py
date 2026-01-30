import pdfplumber
import sys

# Fix encoding
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'c:\Users\pksia\Dropbox\BVA\content\Metamatyka\10 LICZBY I DZIALANIA.pdf'

try:
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n\n'
        
        print("EXTRACTION_SUCCESS")
        print(text)
except Exception as e:
    print(f"Error: {e}")
