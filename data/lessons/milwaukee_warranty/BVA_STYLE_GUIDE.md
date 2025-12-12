# 🎨 BVA Educational Materials - Style Guide
## Standardy wizualizacji dla lekcji i materiałów szkoleniowych

> **Wersja:** 2.0 (Grudzień 2025)  
> **Autor:** BrainventureAcademy  
> **Zakres:** Lekcje, inspiracje, materiały HTML/JSON

---

## 📌 1. KOLORY SEMANTYCZNE (Info Boxes)

Każdy typ informacji ma przypisany kolor dla spójności i szybkiego rozpoznawania:

### Paleta główna:

| Typ | Kolor | Gradient | Użycie | Emoji |
|-----|-------|----------|--------|-------|
| **Info** 🔵 | `#3b82f6` | `linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%)` | Teoria, definicje, fakty | 📖 |
| **Success** 🟢 | `#10b981` | `linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%)` | Dobre praktyki, porady | ✅ |
| **Warning** 🟡 | `#f59e0b` | `linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)` | Uwagi, wskazówki | ⚠️ |
| **Error** 🔴 | `#ef4444` | `linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)` | Błędy, pułapki, zagrożenia | ❌ |
| **Highlight** 🟠 | `#f97316` | `linear-gradient(135deg, #ffedd5 0%, #fed7aa 100%)` | Case studies, przykłady | 💡 |

### Struktura CSS Box:

```css
.info-box {
    background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
    border-left: 5px solid #3b82f6;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.success-box {
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    border-left: 5px solid #10b981;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

/* ...podobnie dla warning-box, error-box, highlight-box */
```

---

## 🎭 2. EMOJI STANDARDY

Spójne użycie emoji zwiększa czytelność i szybką nawigację:

### Sekcje strukturalne:

| Emoji | Znaczenie | Użycie |
|-------|-----------|--------|
| 📖 | Teoria/Wprowadzenie | Intro, definicje, podstawy |
| 🎯 | Praktyka/Zastosowanie | Przykłady, case studies, ćwiczenia |
| 💬 | Komunikacja/Dialog | Rozmowy z klientem, skrypty sprzedażowe |
| 📊 | Dane/Analiza | Wykresy, statystyki, KPI |
| ✅ | Podsumowanie/Checklist | Wnioski, action items |
| 🔑 | Kluczowe punkty | Najważniejsze informacje |
| 💡 | Insight/Tip | Pro tipy, lifehacki |
| ⚠️ | Ostrzeżenie | Częste błędy, ryzyko |
| 🎓 | Wiedza teoretyczna | Koncepcje, modele, teorie |
| 🏆 | Sukces/Best practice | Wzorce doskonałości |

### Nawigacja (tabs):

```json
{
  "tabs": [
    {"label": "📖 Wprowadzenie", "id": "intro"},
    {"label": "🎯 Praktyka", "id": "practice"},
    {"label": "💬 Case Study", "id": "case"},
    {"label": "📊 Analiza", "id": "analysis"},
    {"label": "✅ Podsumowanie", "id": "summary"}
  ]
}
```

---

## 🏢 3. KOLORY BRANDINGOWE (Grupy użytkowników)

Każda grupa ma dedykowany kolor dla spójności wizualnej:

| Grupa | Kolor | Gradient | Użycie |
|-------|-------|----------|--------|
| **General** | `#6c757d` | `linear-gradient(135deg, #6c757d 0%, #495057 100%)` | Ogólne materiały |
| **Warta** | `#dc3545` | `linear-gradient(135deg, #dc3545 0%, #a02828 100%)` | Ubezpieczenia |
| **Heinz** | `#e74c3c` | `linear-gradient(135deg, #D32F2F 0%, #A02020 100%)` | FMCG/Food Service |
| **Milwaukee** | `#f39c12` | `linear-gradient(135deg, #f39c12 0%, #d68910 100%)` | B2B/narzędzia |
| **Degen** | `#9b59b6` | `linear-gradient(135deg, #9b59b6 0%, #7d3c98 100%)` | Trading/crypto |

### Przykład użycia w lekcji Milwaukee:

```html
<div style="background: linear-gradient(135deg, #f39c12 0%, #d68910 100%); 
            padding: 40px; text-align: center; border-radius: 16px;">
    <h1 style="color: white; margin-bottom: 16px;">
        🔧 Milwaukee - Warunki Gwarancji
    </h1>
    <p style="color: white; font-size: 1.2rem;">
        Profesjonalna obsługa reklamacji i doradzanie klientom
    </p>
</div>
```

---

## 📝 4. TYPOGRAFIA

### Hierarchia nagłówków:

```css
h1 {
    font-size: 2.5rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 10px;
}

h2 {
    font-size: 2rem;
    font-weight: 600;
    color: #334155;
    margin: 30px 0 15px 0;
}

h3 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #475569;
    margin: 25px 0 12px 0;
}

h4 {
    font-size: 1.2rem;
    font-weight: 600;
    color: #64748b;
    margin: 20px 0 10px 0;
}
```

### Tekst body:

```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #1e293b;
    font-size: 1.05rem;
}

.lead-text {
    font-size: 1.2rem;
    line-height: 1.8;
    font-weight: 400;
}

.small-text {
    font-size: 0.9rem;
    color: #64748b;
}
```

---

## 🎨 5. KARTY I KOMPONENTY

### Brand Card (np. dla produktów):

```html
<div class="brand-card heinz" style="
    background: white;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border-top: 4px solid #dc2626;">
    <h4 style="color: #dc2626; margin-top: 0;">🍅 Heinz Ketchup</h4>
    <p>Wiodąca marka premium w segmencie sosów...</p>
</div>
```

### Strategy Column (porównania):

```html
<div class="strategy-column">
    <h4 style="
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: white;
        padding: 12px;
        border-radius: 8px;
        text-align: center;">
        🔴 Strategia Premium
    </h4>
    <ul class="argument-list">
        <li style="
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 4px solid #dc2626;">
            Argument 1: Jakość i prestiż
        </li>
    </ul>
</div>
```

---

## 📐 6. LAYOUT I SPACING

### Container główny:

```css
.container {
    max-width: 1200px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
```

### Spacing standardy:

- **Margin sekcji**: `30px 0`
- **Padding boxów**: `20px`
- **Gap między kartami**: `15px`
- **Border radius**: `8px` (mały), `12px` (średni), `16px` (duży)

---

## 🎮 7. INTERAKTYWNE ELEMENTY

### Quiz/Questions:

```html
<div class="quiz-question" style="
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
    border: 2px solid #0ea5e9;
    border-radius: 12px;
    padding: 25px;
    margin: 20px 0;">
    
    <h4 style="color: #0369a1; margin-top: 0;">
        ❓ Pytanie 1: Jak długo trwa gwarancja Milwaukee?
    </h4>
    
    <div class="options">
        <button class="option-btn">A) 12 miesięcy</button>
        <button class="option-btn">B) 24 miesiące</button>
        <button class="option-btn">C) 36 miesięcy</button>
    </div>
</div>
```

### Progress Bars:

```html
<div class="progress-container" style="
    background: #e2e8f0;
    border-radius: 10px;
    height: 24px;
    overflow: hidden;">
    
    <div class="progress-bar" style="
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        height: 100%;
        width: 75%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.9rem;">
        75% ukończone
    </div>
</div>
```

---

## 🔧 8. SPECYFICZNE DLA MILWAUKEE

### Hero Section:

```html
<div style="
    background: linear-gradient(135deg, #f39c12 0%, #d68910 100%);
    padding: 60px 40px;
    text-align: center;
    border-radius: 16px;
    margin-bottom: 40px;">
    
    <div style="font-size: 4rem; margin-bottom: 20px;">🔧</div>
    <h1 style="color: white; font-size: 2.8rem; margin-bottom: 16px;">
        Milwaukee - Warunki Gwarancji
    </h1>
    <p style="color: white; font-size: 1.3rem; line-height: 1.6;">
        Poznaj zasady gwarancyjne i procedury reklamacyjne<br>
        produktów Milwaukee Tool
    </p>
</div>
```

### Checklist/Action Items:

```html
<div class="milwaukee-checklist" style="
    background: white;
    border: 2px solid #f39c12;
    border-radius: 12px;
    padding: 25px;">
    
    <h4 style="color: #d68910; margin-top: 0;">
        ✅ Dokumenty wymagane przy reklamacji:
    </h4>
    <ul style="list-style: none; padding-left: 0;">
        <li style="padding: 10px 0; border-bottom: 1px solid #f5f5f5;">
            ☑️ Paragon lub faktura zakupu
        </li>
        <li style="padding: 10px 0; border-bottom: 1px solid #f5f5f5;">
            ☑️ Certyfikat gwarancyjny (jeśli dotyczy)
        </li>
        <li style="padding: 10px 0;">
            ☑️ Opis usterki
        </li>
    </ul>
</div>
```

---

## 📱 9. RESPONSYWNOŚĆ

### Media queries:

```css
@media (max-width: 768px) {
    .container {
        padding: 20px;
        border-radius: 12px;
    }
    
    h1 {
        font-size: 2rem;
    }
    
    h2 {
        font-size: 1.5rem;
    }
    
    .strategy-column {
        margin-bottom: 20px;
    }
}
```

---

## 🎯 10. PRZYKŁAD KOMPLETNEJ LEKCJI (MILWAUKEE)

Patrz: `data/lessons/milwaukee_warranty/przyklad_lekcji.html`

### Struktura:

1. **Hero Section** - Gradient Milwaukee + tytuł + emoji
2. **Intro Box** (🔵 info-box) - Cele nauki
3. **Sekcja 1** (📖 Teoria) - Podstawy gwarancji
4. **Success Box** (🟢) - Dobre praktyki
5. **Warning Box** (🟡) - Częste błędy
6. **Case Study** (🟠 highlight-box) - Przykład z życia
7. **Quiz** (interaktywny) - Test wiedzy
8. **Summary** (✅ checklist) - Kluczowe wnioski

---

## 📚 11. ZAŁĄCZNIKI

- `bva_educational_styles.css` - Kompletny plik CSS
- `milwaukee_lesson_template.html` - Szablon gotowy do użycia
- `emoji_reference.md` - Pełna lista emoji z użyciem

---

## 🔄 12. CHANGELOG

- **v2.0 (Grudzień 2025)** - Dodano standardy Milwaukee, rozszerzono paletę emoji
- **v1.5 (Listopad 2025)** - Standardy Heinz/Pudliszki
- **v1.0 (Październik 2025)** - Wersja bazowa

---

**Ostatnia aktualizacja:** Grudzień 2025  
**Kontakt:** BrainventureAcademy Team
