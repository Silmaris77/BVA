# Instrukcja Refaktoryzacji: System Layoutu i Motywów (V3)

Poniżej znajduje się szczegółowa dokumentacja zmian w systemie motywów, które ustandaryzowały wygląd aplikacji i umożliwiły łatwe tworzenie nowych skórek (np. Voltage).

---

## 1. Architektura Tokenów (CSS Variables)

Wszystkie kolory i style zostały wyciągnięte z komponentów i przeniesione do `src/app/globals.css`. Dzięki temu komponenty są "ślepe" na konkretne motywy.

### Lista standardowych tokenów:
Zdefiniowane w `:root` (domyślny tryb ciemny) oraz nadpisywane w selektorach motywów.

#### Tokeny podstawowe (wymagane)
| Token | Przeznaczenie |
| :--- | :--- |
| `--t-bg` | Główne tło strony |
| `--t-card-bg` | Tło kart/modułów |
| `--t-card-border` | Kolor obramowania kart |
| `--t-card-radius` | Zaokrąglenie rogów kart |
| `--t-card-shadow` | Cień kart |
| `--t-text` | Główny kolor tekstu |
| `--t-text-muted` | Tekst pomocniczy/wyciszony |
| `--t-accent` | Główny kolor akcentu (np. fiolet/złoto/cyjan) |
| `--t-accent-secondary` | Drugi kolor akcentu |
| `--t-accent-glow` | Poświata akcentu (dla efektów glow) |

#### Tokeny nawigacji
| Token | Przeznaczenie |
| :--- | :--- |
| `--t-nav-bg` | Tło nawigacji (sidebar, bottom nav) |
| `--t-nav-border` | Ramka nawigacji |
| `--t-nav-active` | Kolor aktywnego elementu |

#### Tokeny przycisków
| Token | Przeznaczenie |
| :--- | :--- |
| `--t-button-bg` | Tło przycisków |
| `--t-button-text` | Tekst przycisków |
| `--t-button-shadow` | Cień przycisków (dla efektu 3D) |

#### Tokeny formularzy
| Token | Przeznaczenie |
| :--- | :--- |
| `--t-input-bg` | Tło inputów |
| `--t-input-border` | Ramka inputów |
| `--t-input-focus` | Kolor focus inputów |

#### Tokeny hover (WAŻNE!)
| Token | Przeznaczenie |
| :--- | :--- |
| `--t-hover-transition` | Transition przy najechaniu (np. `all 0.3s ease`) |
| `--t-hover-transform` | Transform przy najechaniu (np. `translateY(-3px)`) |

> [!WARNING]
> **NIE używaj** `--t-hover-anim` z animacjami typu `electricFlicker` - są irytujące!
> Zamiast tego używaj płynnych `transition` + `transform`.

---

## 2. Klasy Utility dla Motywów

Zamiast wszędzie pisać inline styles, zdefiniuj klasy utility w `globals.css`:

```css
/* === THEME UTILITY CLASSES === */
.theme-card {
    background: var(--t-card-bg);
    border: 1px solid var(--t-card-border);
    border-radius: var(--t-card-radius);
    box-shadow: var(--t-card-shadow);
    color: var(--t-text);
    transition: var(--t-hover-transition, all 0.3s ease);
}

.theme-card:hover {
    transform: var(--t-hover-transform, translateY(-2px));
}

.theme-button {
    background: var(--t-button-bg, var(--t-accent));
    color: var(--t-button-text, #000);
    border: none;
    border-radius: 4px;
    box-shadow: var(--t-button-shadow);
    transition: all 0.2s ease;
}

.theme-input {
    background: var(--t-input-bg);
    border: 1px solid var(--t-input-border);
    color: var(--t-text);
    border-radius: 4px;
}

.theme-input:focus {
    border-color: var(--t-input-focus, var(--t-accent));
    outline: none;
}

.theme-text-muted {
    color: var(--t-text-muted);
}

.theme-accent {
    color: var(--t-accent);
}
```

### Użycie w komponentach:
```tsx
// Czysto i prosto!
<div className="theme-card">
  <h3>Tytuł</h3>
  <p className="theme-text-muted">Opis</p>
  <button className="theme-button">Akcja</button>
</div>
```

---

## 3. Refaktoryzacja Komponentów (V3 Standard)

Każdy komponent typu "Karta" (Hub, Lekcje, Statystyki) powinien używać klas utility lub zmiennych.

### Wzorzec A: Klasy utility (preferowany)
```tsx
<div className="theme-card glass-card">
  {content}
</div>
```

### Wzorzec B: Inline styles z tokenami (gdy potrzeba customizacji)
```tsx
<div 
  className="glass-card"
  style={{
    background: 'var(--t-card-bg)',
    border: '1px solid var(--t-card-border)',
    borderRadius: 'var(--t-card-radius)',
    // Dodatkowe style specyficzne...
  }}
>
  {content}
</div>
```

---

## 4. Motyw Voltage (⚡ Volta Inspired)

To najbardziej zaawansowany motyw, który wprowadza "techniczny" wygląd inżynierski.

### Pełna definicja tokenów:
```css
[data-theme='voltage'] {
    /* Tła */
    --t-bg: #0a0e14;
    --t-bg-gradient: radial-gradient(ellipse at 50% 0%, rgba(40, 60, 85, 0.6) 0%, rgba(26, 38, 54, 1) 70%);
    
    /* Karty */
    --t-card-bg: linear-gradient(180deg, rgba(14, 20, 30, 0.98) 0%, rgba(10, 14, 22, 0.99) 100%);
    --t-card-border: rgba(0, 229, 255, 0.2);
    --t-card-radius: 6px;
    --t-card-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    
    /* Tekst */
    --t-text: #e8eef5;
    --t-text-muted: #8899aa;
    
    /* Akcenty */
    --t-accent: #ffcc00;           /* Hazard Yellow - przyciski */
    --t-accent-secondary: #00e5ff; /* Electric Cyan - ramki */
    --t-accent-glow: rgba(0, 229, 255, 0.6);
    
    /* Nawigacja */
    --t-nav-bg: linear-gradient(180deg, rgba(12, 18, 28, 0.98) 0%, rgba(8, 12, 20, 0.99) 100%);
    --t-nav-border: rgba(0, 229, 255, 0.15);
    --t-nav-active: #00e5ff;
    
    /* Przyciski */
    --t-button-bg: #ffcc00;
    --t-button-text: #000;
    --t-button-shadow: 0 4px 0 #997a00;
    
    /* Inputy */
    --t-input-bg: rgba(10, 14, 20, 0.9);
    --t-input-border: rgba(0, 229, 255, 0.2);
    --t-input-focus: #00e5ff;
    
    /* Hover - BEZ ANIMACJI! */
    --t-hover-transition: all 0.3s ease;
    --t-hover-transform: translateY(-3px);
    
    /* Zmienne specyficzne dla Voltage */
    --voltage-cyan: #00e5ff;
    --voltage-yellow: #ffcc00;
    --font-heading: 'JetBrains Mono', 'Share Tech Mono', monospace;
}
```

### Specyficzne dekoracje dla kart Voltage:
```css
/* Lewa ramka cyan - charakterystyczny element Volta */
html[data-theme='voltage'] .glass-card,
html[data-theme='voltage'] .lesson-card-v3 {
    border-left: 3px solid var(--voltage-cyan) !important;
    position: relative;
    overflow: hidden;
}

/* Techniczne znaczniki w rogach (Blueprint style) */
html[data-theme='voltage'] .glass-card::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 20px; height: 20px;
    border-top: 2px solid rgba(0, 229, 255, 0.5);
    border-right: 2px solid rgba(0, 229, 255, 0.5);
    pointer-events: none;
}

html[data-theme='voltage'] .glass-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 20px; height: 20px;
    border-bottom: 2px solid rgba(0, 229, 255, 0.5);
    border-left: 2px solid rgba(0, 229, 255, 0.5);
    pointer-events: none;
}
```

### Tło z siatką techniczną:
```css
html[data-theme='voltage'] {
    background-color: #1a2636 !important; /* Jaśniejsze niż karty! */
    background-image:
        radial-gradient(circle at center, rgba(0, 229, 255, 0.2) 1.5px, transparent 1.5px),
        linear-gradient(rgba(0, 229, 255, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 229, 255, 0.08) 1px, transparent 1px),
        linear-gradient(rgba(0, 229, 255, 0.12) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 229, 255, 0.12) 1px, transparent 1px),
        var(--t-bg-gradient) !important;
    background-size: 80px 80px, 20px 20px, 20px 20px, 80px 80px, 80px 80px, 100% 100% !important;
    background-attachment: fixed !important;
}
```

> [!IMPORTANT]
> **Kontrast**: Tło główne (`#1a2636`) MUSI być jaśniejsze niż karty (`#0a0e14`), aby karty "wystawały" wizualnie.

---

## 5. Jak stworzyć nowy motyw (Krok po kroku)

### Krok 1: Zdefiniuj paletę kolorów
```css
[data-theme='moj-motyw'] {
    --t-bg: #...;
    --t-card-bg: #...;
    --t-card-border: #...;
    --t-text: #...;
    --t-text-muted: #...;
    --t-accent: #...;
    --t-accent-secondary: #...;
}
```

### Krok 2: Dodaj tło HTML
```css
html[data-theme='moj-motyw'] {
    background: var(--t-bg) !important;
    /* Opcjonalnie: gradienty, siatki, wzory */
}
```

### Krok 3: Dostosuj orby (jeśli używasz)
```css
html[data-theme='moj-motyw'] .orb {
    background: var(--t-accent);
    opacity: 0.3; /* lub 0 żeby ukryć */
}
```

### Krok 4: Dodaj specyficzne style (opcjonalne)
```css
/* Przyciski, karty, nawigacja - tylko jeśli różnią się od domyślnych */
html[data-theme='moj-motyw'] button { ... }
html[data-theme='moj-motyw'] .glass-card { ... }
```

### Krok 5: Zarejestruj w ThemeSelector
```tsx
// src/components/profile/ThemeSelector.tsx
const themes = [
    // ...
    { id: 'moj-motyw', name: '🎨 Mój Motyw', color: '#...' },
]
```

### Krok 6: Dodaj do typu Theme
```tsx
// src/contexts/ThemeContext.tsx
export type Theme = '...' | 'moj-motyw'
```

---

## 6. Standaryzacja Danych Hub'a

Podczas refaktoryzacji naprawiono również błędy logiczne w widoku Hub:

1.  **Licznik kart (0 kart fix):** W `app/api/lessons/route.ts` wprowadzono wyliczanie `card_count` na podstawie pola `content.cards.length`.
2.  **Etykiety Tracków:** Zmieniono sztywne "0" lub "undefined" na czytelne nazwy (np. "Matematyka") poprzez mapowanie w komponencie głównym.

---

## 7. Integracja Lekcji Matematyki (Lokalne Pliki)

Lekcje matematyki są ładowane dynamicznie z plików JSON w `src/data/math/grade7`.

*   **API Route (`api/lessons`):** Skanuje katalog, parsuje pliki i wstrzykuje je do listy lekcji.
*   **Track Label:** Wymusza etykietę `"Matematyka"` dla wszystkich lekcji o ID zaczynającym się od `math-`.
*   **Fix Ścieżek:** Upewnij się, że używasz `path.join(process.cwd(), 'src/data/math/grade7')`, aby ścieżki działały poprawnie na różnych systemach (Windows/Linux).

---

## 8. Jak przywrócić zmiany po Rollbacku?

Jeśli przywrócisz starszą wersję kodu, wykonaj te kroki, aby odzyskać nowy wygląd:

1.  **CSS:** Skopiuj sekcję `:root` oraz `[data-theme='voltage']` do `src/app/globals.css`.
2.  **Komponenty Hub:** Znajdź komponenty w `src/components/hub/` (DailyTip, NewsFeed, ResumeLessonCard) i podmień ich inline style na zmienne `var(--t-...)` lub klasy `theme-*`.
3.  **API:** Upewnij się, że `src/app/api/lessons/route.ts` parsuje JSON z bazy/plików i dodaje pole `card_count`.

> [!IMPORTANT]
> Przy refaktoryzacji API używaj statycznych importów (`import fs from 'fs'`), ponieważ Turbopack w Next.js 15+ miewa problemy z dynamicznymi `await import('fs')` wewnątrz funkcji.

---

## 9. Checklist przed wdrożeniem nowego motywu

- [ ] Zdefiniowano wszystkie wymagane tokeny w `globals.css`
- [ ] Dodano `html[data-theme='...']` dla tła
- [ ] Przetestowano kontrast tekstu (WCAG AA minimum)
- [ ] Sprawdzono hover na kartach (płynne, bez migotania)
- [ ] Przetestowano na mobile (bottom nav, karty)
- [ ] Dodano do `ThemeContext.tsx` (typ Theme)
- [ ] Dodano do `ThemeSelector.tsx` (lista motywów)
- [ ] Przetestowano w trybie ciemnym i jasnym (jeśli dotyczy)

---

## 10. Znane problemy i rozwiązania

| Problem | Rozwiązanie |
| :--- | :--- |
| Karty nie różnią się od tła | Użyj jaśniejszego tła głównego lub ciemniejszych kart |
| Hover migocze/irytuje | Usuń `animation`, użyj tylko `transition` |
| Tekst nieczytelny | Sprawdź kontrast, użyj `text-shadow` dla glow |
| Przyciski niewidoczne | Dodaj `box-shadow` dla efektu 3D |
| Nawigacja zlewa się z tłem | Dodaj `border` lub inny `background` |

---

*Ostatnia aktualizacja: 31.01.2026*
*Wersja: 2.0*
