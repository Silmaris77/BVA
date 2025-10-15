"""
Generator PDF dla Cheatsheet
Wykorzystuje ReportLab do generowania profesjonalnych PDF
"""
import io
from typing import Dict
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from bs4 import BeautifulSoup
import re


def generate_cheatsheet_pdf(lesson_title: str, cheatsheet_html: str, username: str = "Użytkownik") -> bytes:
    """
    Generuje PDF z cheatsheet używając ReportLab
    
    Args:
        lesson_title: Tytuł lekcji
        cheatsheet_html: HTML cheatsheet do konwersji
        username: Nazwa użytkownika
        
    Returns:
        bytes: Dane PDF gotowe do pobrania
    """
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import os
    
    # Utwórz buffer dla PDF
    buffer = io.BytesIO()
    
    # Zarejestruj font z polskim wsparciem
    try:
        arial_path = "C:/Windows/Fonts/arial.ttf"
        arial_bold_path = "C:/Windows/Fonts/arialbd.ttf"
        
        if os.path.exists(arial_path):
            pdfmetrics.registerFont(TTFont('ArialUnicode', arial_path))
            unicode_font = "ArialUnicode"
        else:
            unicode_font = 'Helvetica'
            
        if os.path.exists(arial_bold_path):
            pdfmetrics.registerFont(TTFont('ArialBold', arial_bold_path))
            unicode_font_bold = "ArialBold"
        else:
            unicode_font_bold = 'Helvetica-Bold'
    except Exception as e:
        print(f"Błąd ładowania fontu: {e}")
        unicode_font = 'Helvetica'
        unicode_font_bold = 'Helvetica-Bold'
    
    # Konfiguracja dokumentu
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=30
    )
    
    # Style
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=unicode_font_bold,
        fontSize=20,
        spaceAfter=10,
        textColor=HexColor('#667eea'),
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontName=unicode_font_bold,
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
        textColor=HexColor('#2c3e50')
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontName=unicode_font_bold,
        fontSize=11,
        spaceBefore=8,
        spaceAfter=4,
        textColor=HexColor('#667eea')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName=unicode_font,
        fontSize=9,
        spaceAfter=4,
        leading=12
    )
    
    caption_style = ParagraphStyle(
        'CustomCaption',
        parent=styles['Normal'],
        fontName=unicode_font,
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    
    # Parsuj HTML do tekstu
    soup = BeautifulSoup(cheatsheet_html, 'html.parser')
    
    # Funkcja pomocnicza do czyszczenia tekstu
    def clean_text(text):
        if not text:
            return ""
        text = str(text)
        # Zamień HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&#8203;', '')
        # Usuń nadmiarowe spacje
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    # Zawartość PDF
    story = []
    
    # Nagłówek
    story.append(Paragraph("📋 Cheatsheet", title_style))
    story.append(Paragraph(clean_text(lesson_title), subtitle_style))
    story.append(Spacer(1, 5))
    story.append(Paragraph(f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M')}", caption_style))
    story.append(Paragraph(f"Dla: {clean_text(username)}", caption_style))
    story.append(Spacer(1, 20))
    
    # Przetwórz sekcje z HTML
    # Znajdź wszystkie główne sekcje (div z h3)
    sections = soup.find_all('div', style=lambda x: x and 'background' in x and 'padding' in x)
    
    for section in sections:
        # Znajdź nagłówek sekcji (h3)
        h3 = section.find('h3')
        if h3:
            section_title = clean_text(h3.get_text())
            story.append(Paragraph(section_title, subtitle_style))
        
        # Znajdź pod-sekcje (h4)
        subsections = section.find_all('h4')
        for h4 in subsections:
            subsection_title = clean_text(h4.get_text())
            story.append(Paragraph(subsection_title, heading3_style))
            
            # Znajdź zawartość po h4
            next_elem = h4.find_next_sibling()
            while next_elem and next_elem.name != 'h4':
                if next_elem.name == 'ul':
                    # Lista punktowana
                    for li in next_elem.find_all('li', recursive=False):
                        text = clean_text(li.get_text())
                        story.append(Paragraph(f"• {text}", normal_style))
                elif next_elem.name == 'p':
                    text = clean_text(next_elem.get_text())
                    if text and text not in ['', ' ']:
                        story.append(Paragraph(text, normal_style))
                
                next_elem = next_elem.find_next_sibling()
        
        story.append(Spacer(1, 10))
    
    # Jeśli nie znaleziono struktury, spróbuj prostego parsowania
    if len(story) <= 7:  # Tylko nagłówek
        # Fallback - wyciągnij cały tekst
        all_text = soup.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]
        
        for line in lines[:50]:  # Max 50 linii w fallback
            if len(line) > 5:  # Pomijaj bardzo krótkie linie
                story.append(Paragraph(clean_text(line), normal_style))
    
    # Stopka
    story.append(Spacer(1, 30))
    story.append(Paragraph("─" * 50, caption_style))
    story.append(Paragraph("Wygenerowano przez BrainVenture Academy", caption_style))
    story.append(Paragraph("System edukacyjny Conversational Intelligence", caption_style))
    
    # Zbuduj PDF
    try:
        doc.build(story)
    except Exception as e:
        print(f"Błąd budowania PDF: {e}")
        # Spróbuj z prostszą zawartością
        simple_story = [
            Paragraph("📋 Cheatsheet", title_style),
            Paragraph(clean_text(lesson_title), subtitle_style),
            Spacer(1, 20),
            Paragraph("Treść cheatsheet została przygotowana w formacie PDF.", normal_style),
            Paragraph(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style)
        ]
        doc.build(simple_story)
    
    # Zwróć dane PDF
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data
