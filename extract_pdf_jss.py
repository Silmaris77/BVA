import pdfplumber
import sys

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'c:\Users\pksia\Dropbox\BVA\data\lessons\milwaukee_warranty\JSS RULES OF ENGAGEMENT (Sell-out) EMEA V4.pdf'

with pdfplumber.open(pdf_path) as pdf:
    text = ''
    for page in pdf.pages:
        text += page.extract_text() + '\n\n'
    
    print(f'Liczba stron: {len(pdf.pages)}')
    print(f'Długość tekstu: {len(text)} znaków')
    print('\n' + '='*80)
    print('PEŁNA TREŚĆ:')
    print('='*80 + '\n')
    print(text)
