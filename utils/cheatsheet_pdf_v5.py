"""
Generator PDF dla Cheatsheet v5 - Z layoutem i kartami
Odwzorowuje layout grid i karty z aplikacji
"""
import io
import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, KeepTogether, Frame, PageTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bs4 import BeautifulSoup
import html


# Kolory z aplikacji
COLOR_PRIMARY = HexColor('#667eea')
COLOR_GREEN = HexColor('#4caf50')
COLOR_ORANGE = HexColor('#ff9800')
COLOR_BLUE = HexColor('#2196f3')
COLOR_PURPLE = HexColor('#9c27b0')
COLOR_DARK_ORANGE = HexColor('#e65100')
COLOR_TEXT = HexColor('#424242')
COLOR_LIGHT = HexColor('#757575')
COLOR_BG_LIGHT = HexColor('#f8f9fa')


def register_fonts():
    """Rejestruje czcionki"""
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
    
    try:
        arial_unicode = "C:/Windows/Fonts/arialuni.ttf"
        if os.path.exists(arial_unicode):
            pdfmetrics.registerFont(TTFont('ArialUnicode', arial_unicode))
            return 'ArialUnicode'
    except:
        pass
    
    return 'Helvetica'


def create_pdf_styles(font_name='Arial'):
    """Tworzy style PDF"""
    styles = getSampleStyleSheet()
    
    # Header
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
    
    # Tytuł sekcji - dla użycia w kartach
    styles.add(ParagraphStyle(
        name='PDFSectionTitle',
        fontName=font_name,
        fontSize=14,
        spaceBefore=4,
        spaceAfter=6,
        leading=18,
    ))
    
    # Podsekcja w karcie (główny tytuł karty)
    styles.add(ParagraphStyle(
        name='PDFCardSubtitle',
        fontName=font_name,
        fontSize=10,
        spaceBefore=4,
        spaceAfter=3,
        leading=13,
        textColor=COLOR_TEXT,
        wordWrap='CJK',
    ))
    
    # H4 w karcie (podtytuł wewnątrz karty)
    styles.add(ParagraphStyle(
        name='PDFCardH4',
        fontName=font_name,
        fontSize=9,
        spaceBefore=3,
        spaceAfter=2,
        leading=11,
        textColor=COLOR_TEXT,
        wordWrap='CJK',
    ))
    
    # Tekst w karcie
    styles.add(ParagraphStyle(
        name='PDFCardText',
        fontName=font_name,
        fontSize=9,
        leading=12,
        textColor=COLOR_TEXT,
        spaceAfter=2,
        wordWrap='CJK',
    ))
    
    # Bullet w karcie
    styles.add(ParagraphStyle(
        name='PDFCardBullet',
        fontName=font_name,
        fontSize=9,
        leading=12,
        textColor=COLOR_TEXT,
        leftIndent=12,
        bulletIndent=6,
        spaceAfter=2,
        wordWrap='CJK',
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
    """Wykrywa kolor sekcji - zwraca string #RRGGBB"""
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['neurobiologia', 'neuro']):
        return '#667eea'
    elif any(word in text_lower for word in ['poziomy', 'poziom', 'rozmów']):
        return '#4caf50'
    elif 'techniki do natychmiastowego' in text_lower or ('techniki' in text_lower and 'natychmiastowego' in text_lower):
        return '#ff9800'
    elif any(word in text_lower for word in ['narzędzia', 'diagnostyczne', 'architektura']):
        return '#2196f3'
    elif any(word in text_lower for word in ['zwinność', 'zwinności', 'konwersacyjnej']) and 'techniki' in text_lower:
        return '#9c27b0'
    elif any(word in text_lower for word in ['kultura', 'budowanie']):
        return '#e65100'
    elif any(word in text_lower for word in ['plan', 'działania', '30 dni']):
        return '#4caf50'
    elif any(word in text_lower for word in ['kontrolna', 'lista', 'szybka']):
        return '#667eea'
    
    # Sprawdź CSS
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
    
    return '#667eea'


def create_card(title, items, color, styles, width=None):
    """
    Tworzy kartę z obramowaniem kolorowym (jak w aplikacji)
    
    Args:
        title: Tytuł karty (h4)
        items: Lista elementów (bullet points lub paragrafy)
        color: Kolor obramowania (#RRGGBB)
        styles: Style dokumentu
        width: Szerokość karty (opcjonalna)
    
    Returns:
        Table: Tabela z kartą
    """
    card_content = []
    
    # Tytuł karty
    if title:
        card_content.append(Paragraph(f'<b>{title}</b>', styles['PDFCardSubtitle']))
    
    # Elementy
    for item in items:
        if item['type'] == 'subtitle':
            # H4 jako mniejszy podtytuł
            card_content.append(Paragraph(f'<b>{item["text"]}</b>', styles['PDFCardH4']))
        elif item['type'] == 'bullet':
            # Użyj &bull; (HTML entity) zamiast • (Unicode)
            card_content.append(Paragraph(f'&bull; {item["text"]}', styles['PDFCardBullet']))
        elif item['type'] == 'text':
            card_content.append(Paragraph(item['text'], styles['PDFCardText']))
    
    # Tabela jako karta - użyj podanej szerokości lub automatycznej
    card_table = Table([[card_content]], colWidths=[width] if width else [None])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 2, HexColor(color)),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    return card_table


def generate_cheatsheet_pdf(lesson_title: str, cheatsheet_html: str, username: str = "Użytkownik") -> bytes:
    """
    Generuje PDF z cheatsheet z layoutem przypominającym aplikację
    """
    try:
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15*mm,
            leftMargin=15*mm,
            topMargin=15*mm,
            bottomMargin=15*mm
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
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 8*mm))
        
        # === PARSUJ HTML ===
        soup = BeautifulSoup(cheatsheet_html, 'html.parser')
        main_divs = soup.find_all('div', recursive=False)
        
        for div in main_divs:
            div_style = div.get('style', '')
            
            # Pomiń gradient header
            if 'linear-gradient' in div_style and '667eea' in div_style:
                continue
            
            # Domyślny kolor sekcji
            section_color = '#667eea'  # fioletowy jako domyślny
            
            # Znajdź H3 - tytuł głównej sekcji
            h3_tags = div.find_all('h3', recursive=False)
            for h3 in h3_tags:
                h3_text = clean_text(h3.get_text())
                if not h3_text:
                    continue
                
                # Wykryj kolor
                h3_style = h3.get('style', '')
                section_color = detect_section_color(h3_text, h3_style + div_style)
                
                # Tytuł sekcji
                title_para = Paragraph(
                    f'<font color="{section_color}"><b>{h3_text}</b></font>',
                    styles['PDFSectionTitle']
                )
                story.append(title_para)
                story.append(Spacer(1, 3*mm))
            
            # Znajdź zagnieżdżone divy (potencjalne karty)
            nested_divs = div.find_all('div', recursive=False)
            
            # KLUCZOWE: Jeśli jakikolwiek zagnieżdżony div ma grid, to szukaj w nim kart!
            for nested_div in nested_divs:
                nested_style = nested_div.get('style', '')
                if 'display: grid' in nested_style or 'grid-template-columns' in nested_style:
                    # To jest wewnętrzny grid! Karty są w nim
                    nested_divs = nested_div.find_all('div', recursive=False)
                    div_style = nested_style  # Użyj stylu wewnętrznego grid
                    break  # Użyj pierwszego znalezionego grid
            
            # Wykryj czy to layout z kartami
            has_nested_content = False
            for nested_div in nested_divs:
                if nested_div.find('h4') or nested_div.find('ul') or nested_div.find('p'):
                    has_nested_content = True
                    break
            
            is_grid = ('display: grid' in div_style or 'grid-template-columns' in div_style) or has_nested_content
            
            # Jeśli to grid, zbierz karty
            if is_grid and nested_divs:
                
                cards = []
                for nested_div in nested_divs:
                    # Zbierz zawartość karty
                    card_items = []
                    card_title = None
                    
                    # Sprawdź czy jest H3 w zagnieżdżonym divie (tytuł sekcji w karcie)
                    inner_h3 = nested_div.find('h3')
                    if inner_h3:
                        card_title = clean_text(inner_h3.get_text())
                    
                    # Zbierz WSZYSTKIE H4 w karcie
                    h4_tags = nested_div.find_all('h4')
                    if h4_tags:
                        # Jeśli nie było H3, użyj pierwszego H4 jako tytułu karty
                        if not card_title:
                            first_h4 = h4_tags[0]
                            card_title = clean_text(first_h4.get_text())
                            
                            # WAŻNE: Zbierz zawartość pierwszego H4 (jeśli jest tylko jeden H4)
                            if len(h4_tags) == 1:
                                # Tylko jeden H4 - jego zawartość idzie do karty (bez subtitle)
                                next_ul = first_h4.find_next_sibling('ul')
                                if next_ul:
                                    for li in next_ul.find_all('li', recursive=False):
                                        li_text = clean_text(li.get_text())
                                        if li_text:
                                            card_items.append({'type': 'bullet', 'text': li_text})
                                
                                next_p = first_h4.find_next_sibling('p')
                                if next_p:
                                    p_text = clean_text(next_p.get_text())
                                    if p_text:
                                        card_items.append({'type': 'text', 'text': p_text})
                            
                            # Pozostałe H4 jako podsekcje
                            h4_tags_to_process = h4_tags[1:]
                        else:
                            # Jeśli był H3, wszystkie H4 są podsekcjami
                            h4_tags_to_process = h4_tags
                        
                        # Dodaj H4 i ich zawartość jako podsekcje (dla wielu H4)
                        for h4 in h4_tags_to_process:
                            h4_text = clean_text(h4.get_text())
                            if h4_text:
                                # H4 jako podtytuł
                                card_items.append({'type': 'subtitle', 'text': h4_text})
                                
                                # UL po H4
                                next_ul = h4.find_next_sibling('ul')
                                if next_ul:
                                    for li in next_ul.find_all('li', recursive=False):
                                        li_text = clean_text(li.get_text())
                                        if li_text:
                                            card_items.append({'type': 'bullet', 'text': li_text})
                                
                                # P po H4
                                next_p = h4.find_next_sibling('p')
                                if next_p:
                                    p_text = clean_text(next_p.get_text())
                                    if p_text:
                                        card_items.append({'type': 'text', 'text': p_text})
                    
                    if card_title or card_items:
                        cards.append((card_title, card_items))
                
                # Ułóż karty w grid lub jako pojedynczą kartę pełnej szerokości
                if cards:
                    # Jeśli tylko 1 karta, pokaż ją pełnej szerokości (bez grid)
                    if len(cards) == 1:
                        card_title, card_items = cards[0]
                        single_card = create_card(card_title, card_items, section_color, styles, width=doc.width)
                        story.append(single_card)
                        story.append(Spacer(1, 6*mm))
                    else:
                        # Wiele kart - użyj grid
                        # Wykryj liczbę kolumn z CSS
                        num_cols = 2
                        if '1fr 1fr 1fr' in div_style:
                            num_cols = 3
                        
                        # Oblicz szerokość kolumny (uwzględnij gap i padding kart)
                        gap = 4*mm
                        card_padding = 20  # 8 left + 8 right + margines
                        col_width = (doc.width - (num_cols - 1) * gap) / num_cols
                        card_width = col_width - card_padding
                        
                        # Podziel karty na wiersze
                        rows = []
                        for i in range(0, len(cards), num_cols):
                            row_cards = cards[i:i+num_cols]
                            row = []
                            
                            for card_title, card_items in row_cards:
                                card = create_card(card_title, card_items, section_color, styles, width=card_width)
                                row.append(card)
                            
                            # Wypełnij wiersz pustymi komórkami jeśli potrzeba
                            while len(row) < num_cols:
                                row.append('')
                            
                            rows.append(row)
                        
                        # Utwórz tabelę z kartami
                        grid_table = Table(rows, colWidths=[col_width] * num_cols)
                        grid_table.setStyle(TableStyle([
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 2),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
                            ('TOPPADDING', (0, 0), (-1, -1), 2),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                        ]))
                        
                        story.append(grid_table)
                        story.append(Spacer(1, 6*mm))
            
            else:
                # Nie grid - standardowa lista
                h4_tags = div.find_all('h4')
                for h4 in h4_tags:
                    h4_text = clean_text(h4.get_text())
                    if not h4_text:
                        continue
                    
                    h4_para = Paragraph(f'<b>{h4_text}</b>', styles['PDFCardSubtitle'])
                    story.append(h4_para)
                    
                    next_ul = h4.find_next_sibling('ul')
                    if next_ul:
                        for li in next_ul.find_all('li', recursive=False):
                            li_text = clean_text(li.get_text())
                            if li_text:
                                # Użyj &bull; zamiast •
                                bullet = Paragraph(f'&bull; {li_text}', styles['PDFCardBullet'])
                                story.append(bullet)
                        story.append(Spacer(1, 3*mm))
                
                story.append(Spacer(1, 6*mm))
        
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
        import traceback
        print(f"BŁĄD W GENERATORZE PDF: {e}")
        traceback.print_exc()
        
        # Fallback
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
