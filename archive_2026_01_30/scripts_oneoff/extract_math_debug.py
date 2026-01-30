import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'c:\Users\pksia\Dropbox\BVA\content\Metamatyka\10 LICZBY I DZIALANIA.pdf'

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Number of pages: {len(pdf.pages)}")
        full_text = ""
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text += text + "\n"
                print(f"Page {i+1} text length: {len(text)}")
            else:
                print(f"Page {i+1} has no text.")
        
        if not full_text.strip():
            print("WARNING: No text extracted. PDF might be scanned images.")
        else:
            print("EXTRACTION_SUCCESS")
            print(full_text[:500]) # Print first 500 chars to verify
except Exception as e:
    print(f"Error: {e}")
