"""
Generator PDF dla raportu "Kim Jestem?"
Tworzy profesjonalnie wyglądający raport w formacie PDF
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import io
from typing import Dict
from datetime import datetime


def register_fonts():
    """Rejestruje fonty obsługujące polskie znaki"""
    try:
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
        return True
    except:
        return False


def generate_who_am_i_pdf(profile_data: Dict) -> bytes:
    """
    Generuje raport PDF "Kim Jestem?"
    
    Args:
        profile_data: Słownik z danymi profilu z utils.profile_report.collect_user_profile_data()
    
    Returns:
        bytes: Zawartość pliku PDF
    """
    buffer = io.BytesIO()
    
    # Ustawienia dokumentu
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    # Rejestracja fontów
    fonts_registered = register_fonts()
    
    # Style
    styles = getSampleStyleSheet()
    
    # Własne style
    if fonts_registered:
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName='DejaVuSans-Bold',
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontName='DejaVuSans-Bold',
            fontSize=16,
            textColor=colors.HexColor('#3498db'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontName='DejaVuSans-Bold',
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=8,
            spaceBefore=12
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontName='DejaVuSans',
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=8
        )
        
        small_style = ParagraphStyle(
            'CustomSmall',
            parent=styles['Normal'],
            fontName='DejaVuSans',
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
    else:
        # Fallback do domyślnych fontów
        title_style = styles['Title']
        heading_style = styles['Heading2']
        subheading_style = styles['Heading3']
        body_style = styles['Normal']
        small_style = styles['Normal']
    
    # Elementy dokumentu
    story = []
    
    # === STRONA TYTUŁOWA ===
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("🧭 RAPORT ROZWOJOWY", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph('"Kim Jestem?"', heading_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(
        f"Kompleksowa analiza profilu rozwojowego",
        body_style
    ))
    story.append(Spacer(1, 0.5*inch))
    
    # Metadata
    metadata = profile_data['metadata']
    story.append(Paragraph(f"Użytkownik: <b>{metadata['username']}</b>", body_style))
    story.append(Paragraph(f"Data wygenerowania: {metadata['generated_at']}", small_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Linia
    story.append(Spacer(1, 0.2*inch))
    story.append(Table([['']], colWidths=[6.5*inch], style=TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 2, colors.HexColor('#3498db'))
    ])))
    story.append(Spacer(1, 0.3*inch))
    
    # Podsumowanie testów
    tests = profile_data['tests']
    story.append(Paragraph(f"📊 Wykonane testy diagnostyczne: <b>{len(tests['completed'])}/3</b>", body_style))
    story.append(Spacer(1, 0.1*inch))
    for test in tests['completed']:
        story.append(Paragraph(f"✅ {test}", body_style))
    
    story.append(PageBreak())
    
    # === SEKCJA 1: KIM JESTEM ===
    story.append(Paragraph("1. KIM JESTEM? 🎯", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Synteza profilu
    from utils.profile_report import generate_personal_synthesis
    synthesis = generate_personal_synthesis(profile_data)
    for paragraph in synthesis.split('\n\n'):
        if paragraph.strip():
            story.append(Paragraph(paragraph.strip(), body_style))
            story.append(Spacer(1, 0.15*inch))
    
    story.append(Spacer(1, 0.3*inch))
    
    # === SEKCJA 2: WYNIKI TESTÓW ===
    story.append(Paragraph("2. MOJE WYNIKI DIAGNOSTYCZNE 📋", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Test Kolba
    if tests['kolb']:
        story.append(Paragraph("🔄 Test Kolba - Styl Uczenia Się", subheading_style))
        kolb = tests['kolb']
        story.append(Paragraph(f"<b>Dominujący styl:</b> {kolb['style']}", body_style))
        story.append(Paragraph(kolb['description'], body_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Test Neuroleadera
    if tests['neuroleader']:
        story.append(Paragraph("🧬 Test Neuroleadera - Typ Przywódcy", subheading_style))
        nl = tests['neuroleader']
        story.append(Paragraph(f"<b>Typ neuroleadera:</b> {nl['type']}", body_style))
        story.append(Paragraph(nl['description'], body_style))
        
        # Tabela wyników
        if nl['scores']:
            story.append(Spacer(1, 0.1*inch))
            scores_data = [['Typ', 'Wynik']]
            for nl_type, score in sorted(nl['scores'].items(), key=lambda x: x[1], reverse=True):
                scores_data.append([nl_type, f"{score}%"])
            
            scores_table = Table(scores_data, colWidths=[3*inch, 1.5*inch])
            scores_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'DejaVuSans-Bold' if fonts_registered else 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 10),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('FONTNAME', (0,1), (-1,-1), 'DejaVuSans' if fonts_registered else 'Helvetica'),
            ]))
            story.append(scores_table)
        story.append(Spacer(1, 0.2*inch))
    
    # Test MI
    if tests['mi']:
        story.append(Paragraph("🧠 Test Wielorakich Inteligencji", subheading_style))
        mi = tests['mi']
        
        story.append(Paragraph("<b>Twoje TOP 3 inteligencje:</b>", body_style))
        story.append(Spacer(1, 0.1*inch))
        
        for i, (intelligence, score) in enumerate(mi['top_3'], 1):
            from utils.profile_report import get_intelligence_name, get_intelligence_icon
            name = get_intelligence_name(intelligence)
            icon = get_intelligence_icon(intelligence)
            story.append(Paragraph(
                f"{i}. {icon} <b>{name}</b> - {score:.1f}%",
                body_style
            ))
        
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(
            f"<b>Balans profilu:</b> {mi['balance']:.1f}% (0% = uniwersalny, 100% = wyspecjalizowany)",
            body_style
        ))
        story.append(Spacer(1, 0.2*inch))
    
    story.append(PageBreak())
    
    # === SEKCJA 3: MOJE MOCNE STRONY ===
    story.append(Paragraph("3. MOJE MOCNE STRONY 💪", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    strengths = profile_data['strengths']
    if strengths:
        for i, strength in enumerate(strengths, 1):
            story.append(Paragraph(
                f"{strength['icon']} <b>{strength['name']}</b>",
                subheading_style
            ))
            story.append(Paragraph(strength['description'], body_style))
            story.append(Paragraph(
                f"<i>Źródło: {strength['source']}</i>",
                small_style
            ))
            story.append(Spacer(1, 0.15*inch))
    else:
        story.append(Paragraph(
            "Wykonaj więcej testów diagnostycznych aby odkryć swoje mocne strony!",
            body_style
        ))
    
    story.append(Spacer(1, 0.3*inch))
    
    # === SEKCJA 4: AKTYWNOŚĆ ===
    story.append(Paragraph("4. MOJA AKTYWNOŚĆ W BVA 📈", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    activity = profile_data['activity']
    
    # Statystyki w tabeli
    activity_data = [
        ['Metryka', 'Wartość'],
        ['Ukończone moduły', str(len(activity['modules_completed']))],
        ['Moduły w trakcie', str(len(activity['modules_in_progress']))],
        ['Ogólny postęp', f"{activity['total_progress']}%"],
        ['Wynik zaangażowania', f"{activity['engagement_score']}/100"],
    ]
    
    activity_table = Table(activity_data, colWidths=[3*inch, 2*inch])
    activity_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'DejaVuSans-Bold' if fonts_registered else 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,1), (-1,-1), 'DejaVuSans' if fonts_registered else 'Helvetica'),
    ]))
    story.append(activity_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Wzorce
    patterns = profile_data['patterns']
    if patterns['insights']:
        story.append(Paragraph("<b>📊 Twoje wzorce uczenia się:</b>", subheading_style))
        for insight in patterns['insights']:
            story.append(Paragraph(f"• {insight}", body_style))
        story.append(Spacer(1, 0.2*inch))
    
    if patterns['preferred_areas']:
        story.append(Paragraph("<b>🎯 Preferowane obszary:</b>", subheading_style))
        for area in patterns['preferred_areas']:
            story.append(Paragraph(f"• {area}", body_style))
    
    story.append(PageBreak())
    
    # === SEKCJA 5: REKOMENDACJE ===
    story.append(Paragraph("5. TWOJE NASTĘPNE KROKI 🚀", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    from utils.profile_report import generate_recommendations
    recommendations = generate_recommendations(profile_data)
    
    if recommendations:
        story.append(Paragraph(
            "Na podstawie Twojego profilu rekomendujemy następujące działania:",
            body_style
        ))
        story.append(Spacer(1, 0.2*inch))
        
        for i, rec in enumerate(recommendations, 1):
            # Priorytet z kolorami
            priority_colors = {
                'high': colors.HexColor('#e74c3c'),
                'medium': colors.HexColor('#f39c12'),
                'low': colors.HexColor('#95a5a6')
            }
            priority_labels = {
                'high': 'WYSOKI PRIORYTET',
                'medium': 'ŚREDNI PRIORYTET',
                'low': 'NISKI PRIORYTET'
            }
            
            story.append(Paragraph(
                f"{rec['icon']} <b>{rec['title']}</b>",
                subheading_style
            ))
            story.append(Paragraph(rec['description'], body_style))
            story.append(Paragraph(
                f"<i>Priorytet: {priority_labels[rec['priority']]}</i>",
                ParagraphStyle(
                    'Priority',
                    parent=small_style,
                    textColor=priority_colors[rec['priority']],
                    alignment=TA_LEFT
                )
            ))
            story.append(Spacer(1, 0.15*inch))
    else:
        story.append(Paragraph(
            "Kontynuuj swoją doskonałą pracę! Wykonaj więcej testów aby otrzymać spersonalizowane rekomendacje.",
            body_style
        ))
    
    story.append(Spacer(1, 0.5*inch))
    
    # === STOPKA ===
    story.append(Spacer(1, 1*inch))
    story.append(Table([['']], colWidths=[6.5*inch], style=TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1, colors.grey)
    ])))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "Ten raport został wygenerowany automatycznie przez system BrainVenture Academy.",
        small_style
    ))
    story.append(Paragraph(
        "Jest to narzędzie rozwojowe i nie stanowi profesjonalnej diagnozy psychologicznej.",
        small_style
    ))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(
        "© 2025 BrainVenture Academy. Wszystkie prawa zastrzeżone.",
        small_style
    ))
    
    # Generuj PDF
    doc.build(story)
    
    # Pobierz bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
