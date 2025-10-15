"""
Generator PDF dla Cheatsheet v4 - FINALNY
Maksymalnie uproszczony, z gwarancją działania kolorów i formatowania
"""
import io
import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bs4 import BeautifulSoup
import html


# Definicje kolorów z aplikacji
COLOR_PRIMARY = HexColor('#667eea')      # Fioletowy główny
COLOR_GREEN = HexColor('#4caf50')        # Zielony
COLOR_ORANGE = HexColor('#ff9800')       # Pomarańczowy
COLOR_BLUE = HexColor('#2196f3')         # Niebieski
COLOR_PURPLE = HexColor('#9c27b0')       # Fioletowy ciemny
COLOR_DARK_ORANGE = HexColor('#e65100')  # Pomarańczowy ciemny
COLOR_TEXT = HexColor('#424242')         # Tekst główny
COLOR_LIGHT = HexColor('#757575')        # Tekst jasny


def register_fonts():
    """Rejestruje czcionki"""
    # Najpierw spróbuj Arial (standardowy, zwykle działa najlepiej)
    try:
        arial = "C:/Windows/Fonts/arial.ttf"
        arial_bold = "C:/Windows/Fonts/arialbd.ttf"
        
        if os.path.exists(arial):
            pdfmetrics.registerFont(TTFont('Arial', arial))
            if os.path.exists(arial_bold):
                pdfmetrics.registerFont(TTFont('Arial-Bold', arial_bold))
            return 'Arial'
    except Exception as e:
        print(f"⚠️ Nie udało się załadować Arial: {e}")
    
    # Spróbuj Arial Unicode (pełne wsparcie Unicode)
    try:
        arial_unicode = "C:/Windows/Fonts/arialuni.ttf"
        if os.path.exists(arial_unicode):
            pdfmetrics.registerFont(TTFont('ArialUnicode', arial_unicode))
            return 'ArialUnicode'
    except Exception as e:
        print(f"⚠️ Nie udało się załadować Arial Unicode: {e}")
    
    # Fallback na wbudowaną czcionkę
    print("⚠️ Używam Helvetica (wbudowana)")
    return 'Helvetica'


def create_pdf_styles(font_name='ArialUnicode'):
    """Tworzy style PDF"""
    styles = getSampleStyleSheet()
    
    # Header - biały tekst
    styles.add(ParagraphStyle(
        name='PDFHeaderTitle',
        fontName=font_name,
        fontSize=20,
        textColor=colors.white,
        alignment=TA_CENTER,
        spaceAfter=6,
        leading=24,
    ))
    
    styles.add(ParagraphStyle(
        name='PDFHeaderSub',
        fontName=font_name,
        fontSize=12,
        textColor=colors.white,
        alignment=TA_CENTER,
        spaceAfter=8,
        leading=16,
    ))
    
    # Tytuły sekcji - DUŻE i kolorowe
    styles.add(ParagraphStyle(
        name='PDFSectionTitle',
        fontName=font_name,
        fontSize=16,
        spaceBefore=12,
        spaceAfter=8,
        leading=20,
    ))
    
    # Podsekcje
    styles.add(ParagraphStyle(
        name='PDFSubsection',
        fontName=font_name,
        fontSize=12,
        spaceBefore=6,
        spaceAfter=4,
        leading=16,
        textColor=COLOR_TEXT,
    ))
    
    # Normalny tekst
    styles.add(ParagraphStyle(
        name='PDFNormal',
        fontName=font_name,
        fontSize=10,
        leading=14,
        textColor=COLOR_TEXT,
        spaceAfter=4,
    ))
    
    # Bullet
    styles.add(ParagraphStyle(
        name='PDFBullet',
        fontName=font_name,
        fontSize=10,
        leading=14,
        textColor=COLOR_TEXT,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=3,
    ))
    
    # Stopka
    styles.add(ParagraphStyle(
        name='PDFFooter',
        fontName=font_name,
        fontSize=9,
        textColor=COLOR_LIGHT,
        alignment=TA_CENTER,
    ))
    
    return styles


def clean_text(text):
    """Czyści tekst z HTML"""
    if not text:
        return ""
    
    text = html.unescape(text)
    text = text.replace('<strong>', '<b>').replace('</strong>', '</b>')
    text = re.sub(r'<(?!/?b>)[^>]+>', '', text)
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def detect_section_color(text, style_attr):
    """Wykrywa kolor sekcji na podstawie HTML - zwraca string #RRGGBB"""
    
    # Mapowanie słów kluczowych na kolory (zwracamy stringi #RRGGBB)
    if any(word in text.lower() for word in ['neurobiologia', 'neuro']):
        return '#667eea'
    elif any(word in text.lower() for word in ['poziomy', 'poziom', 'rozmów']):
        return '#4caf50'
    elif any(word in text.lower() for word in ['techniki do natychmiastowego', 'techniki', 'użycia', 'natychmiastowego']):
        return '#ff9800'
    elif any(word in text.lower() for word in ['narzędzia', 'diagnostyczne', 'architektura']):
        return '#2196f3'
    elif any(word in text.lower() for word in ['zwinność', 'zwinności', 'konwersacyjnej']):
        return '#9c27b0'
    elif any(word in text.lower() for word in ['kultura', 'budowanie']):
        return '#e65100'
    elif any(word in text.lower() for word in ['plan', 'działania', '30 dni']):
        return '#4caf50'
    elif any(word in text.lower() for word in ['kontrolna', 'lista', 'checklist', 'szybka']):
        return '#667eea'
    
    # Sprawdź style CSS
    if style_attr:
        if '667eea' in style_attr:
            return '#667eea'
        elif '4caf50' in style_attr:
            return '#4caf50'
        elif 'ff9800' in style_attr:
            return '#ff9800'
        elif '2196f3' in style_attr:
            return '#2196f3'
        elif '9c27b0' in style_attr or '7b1fa2' in style_attr:
            return '#9c27b0'
        elif 'e65100' in style_attr:
            return '#e65100'
    
    return '#667eea'  # Domyślny


def generate_cheatsheet_pdf(lesson_title: str, cheatsheet_html: str, username: str = "Użytkownik") -> bytes:
    """
    Generuje PDF z cheatsheet - WERSJA FINALNA
    """
    try:
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )
        
        font_name = register_fonts()
        styles = create_pdf_styles(font_name)
        
        story = []
        
        # === HEADER (FIOLETOWY) ===
        header_data = [
            [Paragraph("📋 Cheatsheet", styles['PDFHeaderTitle'])],
            [Paragraph(lesson_title, styles['PDFHeaderSub'])],
        ]
        
        header_table = Table(header_data, colWidths=[doc.width])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLOR_PRIMARY),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 10*mm))
        
        # === PARSUJ HTML ===
        soup = BeautifulSoup(cheatsheet_html, 'html.parser')
        
        # Znajdź wszystkie główne divy
        main_divs = soup.find_all('div', recursive=False)
        
        for div in main_divs:
            div_style = div.get('style', '')
            
            # Pomiń gradient header
            if 'linear-gradient' in div_style and '667eea' in div_style:
                continue
            
            # Znajdź H3 - tytuł sekcji
            h3_tags = div.find_all('h3')
            for h3 in h3_tags:
                h3_text = clean_text(h3.get_text())
                if not h3_text:
                    continue
                
                # Wykryj kolor (zwraca string #RRGGBB)
                h3_style = h3.get('style', '')
                section_color = detect_section_color(h3_text, h3_style + div_style)
                
                # Dodaj tytuł sekcji z kolorem
                title_para = Paragraph(
                    f'<font color="{section_color}"><b>{h3_text}</b></font>',
                    styles['PDFSectionTitle']
                )
                story.append(title_para)
                story.append(Spacer(1, 4*mm))
            
            # Znajdź H4 - podsekcje
            h4_tags = div.find_all('h4')
            for h4 in h4_tags:
                h4_text = clean_text(h4.get_text())
                if not h4_text:
                    continue
                
                # Podsekcja
                h4_para = Paragraph(f'<b>{h4_text}</b>', styles['PDFSubsection'])
                story.append(h4_para)
                
                # Szukaj UL po H4
                next_ul = h4.find_next_sibling('ul')
                if next_ul:
                    for li in next_ul.find_all('li', recursive=False):
                        li_text = clean_text(li.get_text())
                        if li_text:
                            bullet = Paragraph(f'• {li_text}', styles['PDFBullet'])
                            story.append(bullet)
                    story.append(Spacer(1, 3*mm))
                else:
                    # Szukaj P po H4
                    next_p = h4.find_next_sibling('p')
                    if next_p:
                        p_text = clean_text(next_p.get_text())
                        if p_text and len(p_text) > 3:
                            para = Paragraph(p_text, styles['PDFNormal'])
                            story.append(para)
                            story.append(Spacer(1, 3*mm))
            
            # Znajdź UL bez H4 (listy bezpośrednio)
            for ul in div.find_all('ul', recursive=False):
                for li in ul.find_all('li', recursive=False):
                    li_text = clean_text(li.get_text())
                    if li_text:
                        bullet = Paragraph(f'• {li_text}', styles['PDFBullet'])
                        story.append(bullet)
                story.append(Spacer(1, 3*mm))
            
            # Odstęp między sekcjami
            story.append(Spacer(1, 8*mm))
        
        # === STOPKA ===
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')
        footer = Paragraph(
            f"Wygenerowano: {timestamp} | {username}",
            styles['PDFFooter']
        )
        story.append(Spacer(1, 5*mm))
        story.append(footer)
        
        # Buduj PDF
        doc.build(story)
        
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
        
    except Exception as e:
        # Fallback z błędem
        import traceback
        print(f"BŁĄD W GENERATORZE PDF: {e}")
        traceback.print_exc()
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        
        story = [
            Paragraph(f"📋 Cheatsheet - {lesson_title}", styles['Title']),
            Spacer(1, 0.3*inch),
            Paragraph(f"Błąd: {str(e)}", styles['Normal']),
        ]
        
        doc.build(story)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
