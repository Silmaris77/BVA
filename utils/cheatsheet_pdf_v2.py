"""
Generator PDF dla Cheatsheet v2 - Wierny wygląd aplikacji
Odwzorowuje kolory, layout i style z sekcji Cheatsheet w aplikacji
"""
import io
import os
from typing import Dict, List
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, KeepTogether, Flowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bs4 import BeautifulSoup
import re


# Kolory z aplikacji
COLORS = {
    'primary_gradient_start': HexColor('#667eea'),  # Fiolet
    'primary_gradient_end': HexColor('#764ba2'),    # Ciemniejszy fiolet
    'neurobiologia': HexColor('#667eea'),           # Niebieski-fiolet
    'poziomy': HexColor('#4caf50'),                 # Zielony
    'techniki': HexColor('#ff9800'),                # Pomarańczowy
    'diagnostyka': HexColor('#2196f3'),             # Niebieski
    'zwinnosc': HexColor('#9c27b0'),                # Fioletowy
    'kultura': HexColor('#ff9800'),                 # Pomarańczowy
    'plan': HexColor('#4caf50'),                    # Zielony
    'checklist_gradient': HexColor('#f093fb'),      # Różowy
    'background_light': HexColor('#f8f9fa'),        # Jasne tło
    'card_white': colors.white,                      # Białe karty
    'text_dark': HexColor('#424242'),               # Ciemny tekst
    'text_medium': HexColor('#666666'),             # Średni tekst
    'success': HexColor('#2e7d32'),                 # Zielony sukces
    'error': HexColor('#d32f2f'),                   # Czerwony błąd
}


class ColoredBackground(Flowable):
    """Kolorowe tło dla sekcji (imituje gradient)"""
    
    def __init__(self, width, height, color):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.color = color
    
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)


def register_fonts():
    """Rejestruje czcionki z polskimi znakami"""
    try:
        # Spróbuj Arial Unicode
        arial_unicode = "C:/Windows/Fonts/arialuni.ttf"
        if os.path.exists(arial_unicode):
            pdfmetrics.registerFont(TTFont('ArialUnicode', arial_unicode))
            return 'ArialUnicode'
    except:
        pass
    
    try:
        # Fallback do Arial
        arial = "C:/Windows/Fonts/arial.ttf"
        if os.path.exists(arial):
            pdfmetrics.registerFont(TTFont('Arial', arial))
            return 'Arial'
    except:
        pass
    
    # Ostateczny fallback
    return 'Helvetica'


def create_styles(font_name='ArialUnicode'):
    """Tworzy style dopasowane do wyglądu aplikacji"""
    styles = getSampleStyleSheet()
    
    # Główny tytuł (gradient header)
    styles.add(ParagraphStyle(
        name='HeaderTitle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=24,
        textColor=colors.white,
        alignment=TA_CENTER,
        spaceAfter=6,
        spaceBefore=0,
    ))
    
    # Podtytuł w headerze
    styles.add(ParagraphStyle(
        name='HeaderSubtitle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=12,
        textColor=colors.white,
        alignment=TA_CENTER,
        spaceAfter=0,
    ))
    
    # Tytuł sekcji (h3)
    styles.add(ParagraphStyle(
        name='SectionTitle',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=13,
        textColor=COLORS['primary_gradient_start'],
        spaceBefore=8,
        spaceAfter=8,
        leftIndent=0,
    ))
    
    # Podsekcja (h4)
    styles.add(ParagraphStyle(
        name='SubsectionTitle',
        parent=styles['Heading3'],
        fontName=font_name,
        fontSize=10,
        textColor=COLORS['text_dark'],
        spaceBefore=6,
        spaceAfter=4,
        leftIndent=0,
    ))
    
    # Zwykły tekst
    styles.add(ParagraphStyle(
        name='NormalText',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=9,
        textColor=COLORS['text_dark'],
        leading=12,
        leftIndent=0,
    ))
    
    # Bullet point
    styles.add(ParagraphStyle(
        name='BulletText',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=8,
        textColor=COLORS['text_dark'],
        leading=11,
        leftIndent=15,
        bulletIndent=5,
    ))
    
    # Stopka
    styles.add(ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=8,
        textColor=COLORS['text_medium'],
        alignment=TA_CENTER,
        spaceAfter=0,
    ))
    
    return styles


def parse_html_to_sections(html_content: str) -> List[Dict]:
    """
    Parsuje HTML cheatsheet do struktury sekcji
    Rozpoznaje layout grid i kolorystykę
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    sections = []
    
    # Znajdź wszystkie główne kontenery sekcji
    section_divs = soup.find_all('div', recursive=False)
    
    for div in section_divs:
        # Sprawdź czy to header (gradient background)
        style = div.get('style', '')
        if 'linear-gradient' in style and '667eea' in style:
            # To jest header - pomijamy, dodamy go osobno
            continue
        
        # Sprawdź czy to grid container
        if 'display: grid' in style or 'grid-template-columns' in style:
            # Grid layout - przetwórz kolumny
            grid_items = div.find_all('div', recursive=False)
            for item in grid_items:
                section = parse_section_item(item)
                if section:
                    sections.append(section)
        else:
            # Pojedyncza sekcja (nie grid)
            section = parse_section_item(div)
            if section:
                sections.append(section)
    
    return sections


def parse_section_item(div) -> Dict:
    """Parsuje pojedynczy element sekcji"""
    section = {
        'title': '',
        'color': COLORS['primary_gradient_start'],
        'items': []
    }
    
    # Wykryj kolor z border-left
    style = div.get('style', '')
    if 'border-left' in style:
        if '#667eea' in style or '667eea' in style:
            section['color'] = COLORS['neurobiologia']
        elif '#4caf50' in style or '4caf50' in style:
            section['color'] = COLORS['poziomy']
        elif '#ff9800' in style or 'ff9800' in style:
            section['color'] = COLORS['techniki']
        elif '#2196f3' in style or '2196f3' in style:
            section['color'] = COLORS['diagnostyka']
        elif '#9c27b0' in style or '9c27b0' in style:
            section['color'] = COLORS['zwinnosc']
    
    # Znajdź tytuł sekcji (h3)
    h3 = div.find('h3')
    if h3:
        section['title'] = h3.get_text(strip=True)
    
    # Znajdź wszystkie podsekcje i listy
    for elem in div.find_all(['h4', 'ul', 'p', 'div']):
        if elem.name == 'h4':
            # Podsekcja
            section['items'].append({
                'type': 'subsection',
                'text': elem.get_text(strip=True)
            })
        elif elem.name == 'ul':
            # Lista punktowana
            items = []
            for li in elem.find_all('li'):
                items.append(li.get_text(strip=True))
            if items:
                section['items'].append({
                    'type': 'list',
                    'items': items
                })
        elif elem.name == 'p' and elem.get_text(strip=True):
            # Paragraf
            section['items'].append({
                'type': 'paragraph',
                'text': elem.get_text(strip=True)
            })
    
    return section if section['title'] else None


def create_section_card(section: Dict, styles, available_width) -> List:
    """
    Tworzy kartę sekcji z kolorowym obramowaniem (jak w aplikacji)
    """
    story = []
    
    # Nagłówek sekcji z kolorem
    title_para = Paragraph(
        f"<font color='{section['color'].hexval()}'><b>{section['title']}</b></font>",
        styles['SectionTitle']
    )
    story.append(title_para)
    story.append(Spacer(1, 4*mm))
    
    # Zawartość sekcji
    for item in section['items']:
        if item['type'] == 'subsection':
            # Podsekcja
            subsection_para = Paragraph(
                f"<b>{item['text']}</b>",
                styles['SubsectionTitle']
            )
            story.append(subsection_para)
            story.append(Spacer(1, 2*mm))
            
        elif item['type'] == 'list':
            # Lista punktowana
            for bullet_text in item['items']:
                # Usuń znaczniki HTML, zachowaj <strong>
                clean_text = bullet_text.replace('<strong>', '<b>').replace('</strong>', '</b>')
                bullet_para = Paragraph(
                    f"• {clean_text}",
                    styles['BulletText']
                )
                story.append(bullet_para)
                story.append(Spacer(1, 1*mm))
            story.append(Spacer(1, 2*mm))
            
        elif item['type'] == 'paragraph':
            # Paragraf
            clean_text = item['text'].replace('<strong>', '<b>').replace('</strong>', '</b>')
            para = Paragraph(clean_text, styles['NormalText'])
            story.append(para)
            story.append(Spacer(1, 2*mm))
    
    story.append(Spacer(1, 5*mm))
    return story


def generate_cheatsheet_pdf(lesson_title: str, cheatsheet_html: str, username: str = "Użytkownik") -> bytes:
    """
    Generuje PDF z cheatsheet dopasowany wizualnie do aplikacji
    
    Args:
        lesson_title: Tytuł lekcji
        cheatsheet_html: HTML cheatsheet
        username: Nazwa użytkownika
        
    Returns:
        bytes: Dane PDF
    """
    try:
        # Przygotuj buffer
        buffer = io.BytesIO()
        
        # Utwórz dokument
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=15*mm
        )
        
        # Rejestruj czcionki
        font_name = register_fonts()
        
        # Utwórz style
        styles = create_styles(font_name)
        
        # Story - zawartość PDF
        story = []
        
        # === HEADER Z GRADIENTEM (imitacja) ===
        # Tło - użyjemy tabeli z kolorowym tłem
        header_data = [
            [Paragraph("📋 Cheatsheet", styles['HeaderTitle'])],
            [Paragraph(f"{lesson_title}", styles['HeaderSubtitle'])],
            [Spacer(1, 2*mm)]
        ]
        
        header_table = Table(header_data, colWidths=[doc.width])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLORS['primary_gradient_start']),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 8*mm))
        
        # === PARSUJ I DODAJ SEKCJE ===
        sections = parse_html_to_sections(cheatsheet_html)
        
        for section in sections:
            # Utwórz kartę sekcji
            section_content = create_section_card(section, styles, doc.width)
            
            # Opakuj w KeepTogether jeśli możliwe
            try:
                story.append(KeepTogether(section_content))
            except:
                # Jeśli sekcja jest za duża, dodaj bez KeepTogether
                story.extend(section_content)
        
        # === STOPKA ===
        story.append(Spacer(1, 10*mm))
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
        footer_text = f"Wygenerowano: {timestamp} | Użytkownik: {username}"
        story.append(Paragraph(footer_text, styles['Footer']))
        
        # Zbuduj PDF
        doc.build(story)
        
        # Zwróć dane
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
        
    except Exception as e:
        # Fallback - prosty PDF z błędem
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        styles = getSampleStyleSheet()
        story = [
            Paragraph(f"📋 Cheatsheet - {lesson_title}", styles['Title']),
            Spacer(1, 0.3*inch),
            Paragraph(f"Wystąpił błąd podczas generowania PDF: {str(e)}", styles['Normal']),
            Spacer(1, 0.2*inch),
            Paragraph("Spróbuj ponownie lub skontaktuj się z administratorem.", styles['Normal']),
        ]
        
        doc.build(story)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
