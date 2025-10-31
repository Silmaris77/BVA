# 🎨 BVA Educational Materials - Standard Kolorystyczny

**Wersja:** 1.0  
**Data:** 2025-10-30  
**Status:** Zatwierdzony

---

## 📋 Zasada ogólna

**System hybrydowy:** Kolory tematyczne dla kategorii + uniwersalne kolory dla elementów wewnętrznych

---

## 🎨 Kategorie tematyczne (Header/Stopka/Aktywna zakładka)

| Kategoria | Gradient | Użycie | Przykładowe artykuły |
|-----------|----------|--------|---------------------|
| **🏪 Kanał & Dystrybucja** | `#667eea → #764ba2` (fiolet) | Wszystko o kanale tradycyjnym, hurtowniach, cash & carry | "Kanał Tradycyjny" |
| **🎯 Sprzedaż & Negocjacje** | `#f093fb → #f5576c` (różowo-czerwony) | Techniki sprzedaży, sondowanie, negocjacje | "Sondowanie potrzeb klienta" |
| **📊 Merchandising & Shelf** | `#3b82f6 → #1e40af` (niebieski) | Merchandising, facings, planogram | Przyszłe artykuły |
| **💰 Finanse & Marże** | `#f59e0b → #d97706` (złoty/pomarańczowy) | Kalkulacje, marże, rentowność | Przyszłe artykuły |
| **👥 Relacje & Komunikacja** | `#10b981 → #059669` (zielony) | Budowanie relacji, komunikacja | Przyszłe artykuły |

---

## 🔲 Uniwersalne elementy (ZAWSZE te same kolory)

| Element | Kolor | Gradient | Zastosowanie |
|---------|-------|----------|--------------|
| **Success-box** | `#10b981` | `#d1fae5 → #a7f3d0` | ✅ Zalety, dobre praktyki, sukces |
| **Error-box** | `#ef4444` | `#fee2e2 → #fecaca` | ❌ Wady, błędy, ostrzeżenia |
| **Info-box** | `#3b82f6` | `#dbeafe → #bfdbfe` | ℹ️ Informacje, wskazówki |
| **Warning-box** | `#f59e0b` | `#fef3c7 → #fde68a` | ⚠️ Uwagi, ważne informacje |
| **Highlight-box** | `#f97316` | `#ffedd5 → #fed7aa` | 💡 Kluczowe informacje, najważniejsze punkty |

**Badges:**
- Success: `#d1fae5` / `#065f46`
- Error: `#fee2e2` / `#991b1b`
- Info: `#dbeafe` / `#1e40af`
- Warning: `#fef3c7` / `#92400e`

---

## 📐 Struktura kolorystyczna artykułu

```
┌─────────────────────────────────────┐
│  HEADER (kolor kategorii)           │  ← Gradient kategorii
├─────────────────────────────────────┤
│  TABS (neutralne szare)             │  ← Szary, aktywna = kolor kategorii
├─────────────────────────────────────┤
│  CONTENT (białe tło)                │
│  ├─ Success-box (zawsze zielony)    │  ← Uniwersalne
│  ├─ Error-box (zawsze czerwony)     │  ← Uniwersalne
│  ├─ Info-box (zawsze niebieski)     │  ← Uniwersalne
│  └─ Warning-box (zawsze żółty)      │  ← Uniwersalne
├─────────────────────────────────────┤
│  FOOTER (kolor kategorii)           │  ← Gradient kategorii
└─────────────────────────────────────┘
```

---

## 🛠️ Implementacja

### HTML - atrybut data-category

```html
<body data-category="sprzedaz">
    <div class="header" data-category="sprzedaz">
        <!-- Header content -->
    </div>
    
    <div class="tabs">
        <button class="tab active" data-category="sprzedaz">Tab 1</button>
    </div>
    
    <div class="content">
        <div class="success-box">Zalety...</div>
        <div class="error-box">Wady...</div>
        <div class="info-box">Informacja...</div>
    </div>
    
    <div class="footer" data-category="sprzedaz">
        <!-- Footer content -->
    </div>
</body>
```

### CSS - plik `bva_educational_styles.css`

Wszystkie style w jednym wspólnym pliku CSS, który jest ładowany w każdym artykule:

```html
<link rel="stylesheet" href="bva_educational_styles.css">
```

---

## ✅ Zalety tego podejścia

1. **Intuicyjność** - użytkownik od razu wie o jakiej kategorii czyta (kolor header/footer)
2. **Spójność** - wszystkie boksy informacyjne mają te same kolory we wszystkich artykułach
3. **Skalowalność** - łatwo dodać nowy artykuł, wystarczy ustawić `data-category`
4. **Łatwość utrzymania** - jeden plik CSS dla wszystkich artykułów
5. **Czytelność** - uniwersalne znaczenie kolorów (zielony=sukces, czerwony=błąd itd.)

---

## 📝 Checklist dla nowego artykułu

- [ ] Ustaw `data-category` w `<body>`, `<header>`, `<footer>`, `<tab.active>`
- [ ] Dołącz `<link rel="stylesheet" href="bva_educational_styles.css">`
- [ ] Używaj uniwersalnych klas: `.success-box`, `.error-box`, `.info-box`, `.warning-box`, `.highlight-box`
- [ ] Sprawdź czy gradient kategorii działa poprawnie
- [ ] Dodaj stopkę z przyciskiem "Powrót na górę"
- [ ] Sprawdź responsywność (mobile)

---

## 🎯 Przykłady użycia

### Artykuł o Kanale Tradycyjnym (kategoria: kanal)
```html
<body data-category="kanal">
    <div class="header" data-category="kanal">
        <h1>🏪 Kanał Tradycyjny</h1>
    </div>
    <!-- Gradient fioletowy -->
</body>
```

### Artykuł o Sondowaniu (kategoria: sprzedaz)
```html
<body data-category="sprzedaz">
    <div class="header" data-category="sprzedaz">
        <h1>🎯 Sondowanie potrzeb klienta</h1>
    </div>
    <!-- Gradient różowo-czerwony -->
</body>
```

---

## 🚀 Roadmapa kategorii

| Kategoria | Status | Planowane artykuły |
|-----------|--------|-------------------|
| Kanał & Dystrybucja | ✅ Aktywna | "Kanał Tradycyjny", "Hurtownie vs C&C" |
| Sprzedaż & Negocjacje | ✅ Aktywna | "Sondowanie potrzeb", "Zamykanie sprzedaży" |
| Merchandising & Shelf | 📋 Planowana | "Facings 101", "Shelf share vs Market share" |
| Finanse & Marże | 📋 Planowana | "Kalkulacja marży", "ROI w FMCG" |
| Relacje & Komunikacja | 📋 Planowana | "Budowanie zaufania", "Trudne rozmowy" |

---

**Zatwierdził:** GitHub Copilot  
**Data:** 2025-10-30