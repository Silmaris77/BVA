"""
Generator PDF dla Cheatsheet v3 - Prosty i skuteczny
Odwzorowuje wygląd aplikacji z prawidłowym formatowaniem
"""
import io
import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bs4 import BeautifulSoup


def register_fonts():
    """Rejestruje czcionki z polskimi znakami"""
    try:
        arial_unicode = "C:/Windows/Fonts/arialuni.ttf"
        if os.path.exists(arial_unicode):
            pdfmetrics.registerFont(TTFont('ArialUnicode', arial_unicode))
            return 'ArialUnicode'
    except:
        pass
    
    try:
        arial = "C:/Windows/Fonts/arial.ttf"
        if os.path.exists(arial):
            pdfmetrics.registerFont(TTFont('Arial', arial))
            return 'Arial'
    except:
        pass
    
    return 'Helvetica'


def create_styles(font_name='ArialUnicode'):
    """Tworzy style dopasowane do aplikacji"""
    styles = getSampleStyleSheet()
    
    # Header title (biały na fioletowym)
    styles.add(ParagraphStyle(
        name='HeaderTitle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=18,
        textColor=colors.white,
        alignment=TA_CENTER,
        spaceAfter=4,
        spaceBefore=8,
        leading=22,
    ))
    
    # Header subtitle
    styles.add(ParagraphStyle(
        name='HeaderSubtitle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=11,
        textColor=colors.white,
        alignment=TA_CENTER,
        spaceAfter=8,
        leading=14,
    ))
    
    # Nagłówek sekcji głównej (h3) - WIĘKSZY
    styles.add(ParagraphStyle(
        name='SectionTitle',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=14,
        spaceBefore=10,
        spaceAfter=8,
        leading=18,
        textColor=HexColor('#1a237e'),
    ))
    
    # Podsekcja (h4) - średni
    styles.add(ParagraphStyle(
        name='SubsectionTitle',
        parent=styles['Heading3'],
        fontName=font_name,
        fontSize=11,
        spaceBefore=6,
        spaceAfter=4,
        leading=14,
        textColor=HexColor('#424242'),
    ))
    
    # Normalny tekst
    styles.add(ParagraphStyle(
        name='CheatsheetBody',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=14,
        textColor=HexColor('#424242'),
        spaceAfter=3,
    ))
    
    # Bullet punkt
    styles.add(ParagraphStyle(
        name='CheatsheetBullet',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=9,
        leading=13,
        textColor=HexColor('#424242'),
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=2,
    ))
    
    # Stopka
    styles.add(ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=8,
        textColor=HexColor('#757575'),
        alignment=TA_CENTER,
    ))
    
    return styles


def clean_html_text(text):
    """Czyści tekst HTML, zachowując <strong> jako <b>"""
    if not text:
        return ""
    
    text = text.strip()
    # Zamień <strong> na <b> (ReportLab rozumie <b>)
    text = text.replace('<strong>', '<b>').replace('</strong>', '</b>')
    # Usuń inne tagi HTML
    text = re.sub(r'<(?!/?b>)[^>]+>', '', text)
    # Napraw cudzysłowy
    text = text.replace('„', '"').replace('"', '"')
    text = text.replace("'", "'").replace("'", "'")
    # Usuń nadmiarowe spacje
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def extract_section_color(section_div):
    """Wyciąga kolor z border-left sekcji"""
    style = section_div.get('style', '')
    
    # Mapowanie kolorów na kolory tytułów
    color_map = {
        '667eea': HexColor('#667eea'),  # Niebieski-fiolet
        '4caf50': HexColor('#4caf50'),  # Zielony
        'ff9800': HexColor('#ff9800'),  # Pomarańczowy
        '2196f3': HexColor('#2196f3'),  # Niebieski
        '9c27b0': HexColor('#9c27b0'),  # Fioletowy
        'e65100': HexColor('#e65100'),  # Ciemny pomarańczowy
        '1565c0': HexColor('#1565c0'),  # Ciemny niebieski
        '7b1fa2': HexColor('#7b1fa2'),  # Ciemny fioletowy
    }
    
    for color_code, color_obj in color_map.items():
        if color_code in style:
            return color_obj
    
    # Domyślny kolor
    return HexColor('#1a237e')


def generate_cheatsheet_pdf(lesson_title: str, cheatsheet_html: str, username: str = "Użytkownik") -> bytes:
    """
    Generuje PDF z cheatsheet
    
    Args:
        lesson_title: Tytuł lekcji
        cheatsheet_html: HTML cheatsheet
        username: Nazwa użytkownika
        
    Returns:
        bytes: Dane PDF
    """
    try:
        # Buffer
        buffer = io.BytesIO()
        
        # Dokument A4
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15*mm,
            leftMargin=15*mm,
            topMargin=15*mm,
            bottomMargin=15*mm
        )
        
        # Czcionki
        font_name = register_fonts()
        
        # Style
        styles = create_styles(font_name)
        
        # Story
        story = []
        
        # === HEADER (fioletowy) ===
        header_data = [
            [Paragraph("📋 Cheatsheet", styles['HeaderTitle'])],
            [Paragraph(lesson_title, styles['HeaderSubtitle'])],
        ]
        
        header_table = Table(header_data, colWidths=[doc.width])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor('#667eea')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BOX', (0, 0), (-1, -1), 0, colors.white),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 8*mm))
        
        # === PARSUJ HTML ===
        soup = BeautifulSoup(cheatsheet_html, 'html.parser')
        
        # Znajdź wszystkie główne sekcje (pomijamy pierwszy div z headerem gradientowym)
        all_divs = soup.find_all('div', recursive=False)
        
        for div_idx, main_div in enumerate(all_divs):
            # Pomiń header (pierwszy div z gradientem)
            div_style = main_div.get('style', '')
            if 'linear-gradient' in div_style and div_idx == 0:
                continue
            
            # Wykryj kolor sekcji
            section_color = extract_section_color(main_div)
            
            # Znajdź h3 (tytuł sekcji)
            h3 = main_div.find('h3')
            if h3:
                title_text = clean_html_text(h3.get_text())
                title_para = Paragraph(
                    f'<font color="{section_color.hexval()}"><b>{title_text}</b></font>',
                    styles['SectionTitle']
                )
                story.append(title_para)
                story.append(Spacer(1, 3*mm))
            
            # Znajdź wszystkie h4 (podsekcje)
            for h4 in main_div.find_all('h4'):
                h4_text = clean_html_text(h4.get_text())
                h4_para = Paragraph(f'<b>{h4_text}</b>', styles['SubsectionTitle'])
                story.append(h4_para)
                
                # Sprawdź czy po h4 jest ul lub p
                next_elem = h4.find_next_sibling()
                if next_elem:
                    if next_elem.name == 'ul':
                        # Lista punktowana
                        for li in next_elem.find_all('li'):
                            li_text = clean_html_text(li.get_text())
                            bullet = Paragraph(f'• {li_text}', styles['CheatsheetBullet'])
                            story.append(bullet)
                        story.append(Spacer(1, 2*mm))
                    elif next_elem.name == 'p':
                        # Paragraf po h4
                        p_text = clean_html_text(next_elem.get_text())
                        if p_text:
                            para = Paragraph(p_text, styles['CheatsheetBody'])
                            story.append(para)
                            story.append(Spacer(1, 2*mm))
            
            # Znajdź ul bez h4 (listy bezpośrednio w sekcji)
            for ul in main_div.find_all('ul', recursive=False):
                parent = ul.find_parent()
                # Sprawdź czy ul nie jest już przetworzony (po h4)
                prev_h4 = ul.find_previous_sibling('h4')
                if not prev_h4:
                    for li in ul.find_all('li'):
                        li_text = clean_html_text(li.get_text())
                        bullet = Paragraph(f'• {li_text}', styles['CheatsheetBullet'])
                        story.append(bullet)
                    story.append(Spacer(1, 2*mm))
            
            # Znajdź paragrafy bezpośrednio w sekcji (nie po h4)
            for p in main_div.find_all('p', recursive=False):
                prev_h4 = p.find_previous_sibling('h4')
                if not prev_h4:
                    p_text = clean_html_text(p.get_text())
                    if p_text and len(p_text) > 3:
                        para = Paragraph(p_text, styles['CheatsheetBody'])
                        story.append(para)
                        story.append(Spacer(1, 2*mm))
            
            # Sprawdź czy są zagnieżdżone divy (grid layout)
            nested_divs = main_div.find_all('div', recursive=False)
            if len(nested_divs) > 1:
                # Jest grid - przetwórz każdy div
                for nested_div in nested_divs:
                    # Znajdź h4 w zagnieżdżonym div
                    for h4 in nested_div.find_all('h4'):
                        h4_text = clean_html_text(h4.get_text())
                        h4_para = Paragraph(f'<b>{h4_text}</b>', styles['SubsectionTitle'])
                        story.append(h4_para)
                        
                        # Lista lub paragraf po h4
                        next_elem = h4.find_next()
                        while next_elem and next_elem.name in ['ul', 'p']:
                            if next_elem.name == 'ul':
                                for li in next_elem.find_all('li'):
                                    li_text = clean_html_text(li.get_text())
                                    bullet = Paragraph(f'• {li_text}', styles['CheatsheetBullet'])
                                    story.append(bullet)
                                break
                            elif next_elem.name == 'p':
                                p_text = clean_html_text(next_elem.get_text())
                                if p_text and len(p_text) > 3:
                                    para = Paragraph(p_text, styles['CheatsheetBody'])
                                    story.append(para)
                                break
                            next_elem = next_elem.find_next_sibling()
                        
                        story.append(Spacer(1, 2*mm))
            
            # Odstęp między sekcjami
            story.append(Spacer(1, 6*mm))
        
        # === STOPKA ===
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
        footer_text = f"Wygenerowano: {timestamp} | {username}"
        story.append(Spacer(1, 5*mm))
        story.append(Paragraph(footer_text, styles['Footer']))
        
        # Zbuduj PDF
        doc.build(story)
        
        # Zwróć dane
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
        
    except Exception as e:
        # Fallback
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        styles = getSampleStyleSheet()
        story = [
            Paragraph(f"📋 Cheatsheet - {lesson_title}", styles['Title']),
            Spacer(1, 0.3*inch),
            Paragraph(f"Wystąpił błąd: {str(e)}", styles['Normal']),
        ]
        
        doc.build(story)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
