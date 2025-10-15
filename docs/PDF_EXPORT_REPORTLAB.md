# Eksport PDF z użyciem ReportLab

## 📋 Przegląd

Zaimplementowano profesjonalny eksport PDF dla Cheatsheet używając biblioteki ReportLab - tej samej technologii co w narzędziu "Profil Przywódczy C-IQ".

## ✨ Zalety nowego rozwiązania

### Poprzednie rozwiązanie (HTML)
- ❌ Generował plik HTML
- ❌ Wymagał 3 kroków: pobierz → otwórz → drukuj do PDF
- ❌ Użytkownik musiał ręcznie konfigurować drukarkę PDF
- ❌ Niejednolity wygląd (zależny od przeglądarki)

### Nowe rozwiązanie (ReportLab)
- ✅ Generuje prawdziwy plik PDF
- ✅ Jeden krok: kliknij i pobierz
- ✅ Profesjonalny wygląd (jak w Tools)
- ✅ Wsparcie dla polskich znaków (Arial Unicode)
- ✅ Jednolite formatowanie

## 🛠️ Implementacja

### 1. Nowy moduł: `utils/cheatsheet_pdf.py`

```python
def generate_cheatsheet_pdf(lesson_title, cheatsheet_html, username) -> bytes
```

**Funkcje:**
- Parsuje HTML cheatsheet z BeautifulSoup
- Ekstrakcja struktury:
  - `<h3>` → Sekcja (np. "🎯 Cele Rozmowy")
  - `<h4>` → Podsekcja (np. "Poziom I")
  - `<ul>/<li>` → Lista punktowa
- Stylizacja ReportLab:
  - `title_style` - Tytuł dokumentu
  - `subtitle_style` - Sekcje (h3)
  - `heading3_style` - Podsekcje (h4)
  - `normal_style` - Tekst punktów
  - `caption_style` - Stopka
- Czcionka: Arial Unicode (wsparcie polskich znaków)
- Format: A4 z marginesami
- Wielostronicowy z automatycznym PageBreak

### 2. Zmiany w `views/lesson.py`

**Import datetime:**
```python
from datetime import datetime
```

**Nowy przycisk eksportu:**
```python
if zen_button("📄 Eksportuj PDF", key="export_cheatsheet_pdf"):
    from utils.cheatsheet_pdf import generate_cheatsheet_pdf
    
    pdf_data = generate_cheatsheet_pdf(
        lesson_title=lesson_title,
        cheatsheet_html=cheatsheet_content,
        username=username
    )
    
    st.download_button(
        label="⬇️ Pobierz PDF",
        data=pdf_data,
        file_name=f"cheatsheet_{lesson_id}_{timestamp}.pdf",
        mime="application/pdf"
    )
```

## 📊 Struktura PDF

```
┌─────────────────────────────────────┐
│  📋 Cheatsheet                      │
│  Lekcja: [Tytuł]                    │
│  ───────────────────────────────    │
│                                     │
│  🎯 Sekcja 1                        │
│    • Punkt 1                        │
│    • Punkt 2                        │
│                                     │
│  🧠 Sekcja 2                        │
│    Podsekcja A                      │
│      • Punkt A1                     │
│      • Punkt A2                     │
│                                     │
│    Podsekcja B                      │
│      • Punkt B1                     │
│                                     │
│  ───────────────────────────────    │
│  Wygenerowano: [data] | [user]      │
└─────────────────────────────────────┘
```

## 🧪 Testowanie

### Test jednostkowy: `test_cheatsheet_pdf.py`

```bash
python test_cheatsheet_pdf.py
```

**Sprawdza:**
- ✅ Import modułu
- ✅ Generowanie PDF z HTML
- ✅ Polskie znaki (ą, ć, ę, ł, ń, ó, ś, ź, ż)
- ✅ Struktura sekcji i podsekcji
- ✅ Listy punktowane
- ✅ Zapis do pliku

### Test integracyjny (w aplikacji)

1. Uruchom aplikację: `streamlit run main.py`
2. Przejdź do lekcji C-IQ
3. Kliknij zakładkę "📋 Cheatsheet"
4. Kliknij przycisk "📄 Eksportuj PDF"
5. Kliknij "⬇️ Pobierz PDF"
6. Otwórz plik - powinien wyświetlić się w przeglądarce/czytniku PDF

## 🔧 Zależności

**Biblioteki Python:**
```txt
reportlab>=3.6.12
beautifulsoup4>=4.12.0
```

**Czcionki systemowe:**
- Arial Unicode MS (`C:/Windows/Fonts/arialuni.ttf`)
- Fallback: Arial (`C:/Windows/Fonts/arial.ttf`)
- Fallback: Helvetica (wbudowana w ReportLab)

## 📝 Konfiguracja

### Rozmiar strony
```python
doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                       topMargin=72, bottomMargin=18)
```

### Style tekstu
```python
title_style = ParagraphStyle(
    'Title',
    parent=styles['Title'],
    fontName='ArialUnicode',
    fontSize=18,
    textColor=colors.HexColor('#1a237e'),
    spaceAfter=12
)
```

## 🐛 Obsługa błędów

**Jeśli generowanie PDF nie powiedzie się:**
1. Wyświetla komunikat błędu użytkownikowi
2. W trybie debug pokazuje pełny traceback
3. Nie przerywa działania aplikacji
4. Użytkownik może spróbować ponownie

**Fallback w kodzie:**
```python
try:
    # Normalne generowanie PDF
    pdf_data = generate_cheatsheet_pdf(...)
except Exception as e:
    st.error(f"❌ Błąd podczas generowania PDF: {str(e)}")
    if st.session_state.get('debug_mode'):
        st.expander("Szczegóły błędu").code(traceback.format_exc())
```

## 🎯 Przyszłe usprawnienia

### Możliwe rozszerzenia:
- [ ] Dodatkowe style (ramki, tła)
- [ ] Opcje eksportu (z/bez ikon emoji)
- [ ] Wybór czcionki przez użytkownika
- [ ] Export wielu cheatsheets jako jeden PDF
- [ ] Watermark z logo/nazwą kursu
- [ ] Spis treści dla długich cheatsheets
- [ ] Opcja druku (A4 vs Letter)

### Inspiracja z innych narzędzi:
- ✅ **Profil Przywódczy C-IQ** - bazowy generator (tools.py)
- 🔄 **Mapy myśli** - może też używać ReportLab?
- 🔄 **Statystyki użytkownika** - raport PDF?

## 📚 Powiązane pliki

### Utworzone/Zmodyfikowane:
- ✅ `utils/cheatsheet_pdf.py` - Nowy generator PDF
- ✅ `views/lesson.py` - Integracja eksportu
- ✅ `test_cheatsheet_pdf.py` - Test jednostkowy
- ✅ `docs/PDF_EXPORT_REPORTLAB.md` - Ta dokumentacja

### Wcześniejsze (do ewentualnego usunięcia):
- ⚠️ `utils/pdf_generator.py` - Stary generator HTML
- ⚠️ `docs/PDF_DOWNLOAD_SIMPLIFICATION.md` - Poprzednia wersja

### Wzorcowe (inspiracja):
- 📖 `views/tools.py` (linie 1860-2080) - `generate_leadership_pdf()`

## ✅ Status

**Data wdrożenia:** 2025-01-XX
**Wersja:** 1.0
**Status:** ✅ Zaimplementowane i przetestowane
**Tester:** Agent AI + testy automatyczne

---

**Wnioski:**
Implementacja ReportLab dla eksportu PDF znacznie poprawia UX - użytkownik otrzymuje profesjonalny PDF jednym kliknięciem, bez potrzeby używania funkcji drukowania przeglądarki. Rozwiązanie jest spójne z innymi narzędziami w aplikacji (Tools).
