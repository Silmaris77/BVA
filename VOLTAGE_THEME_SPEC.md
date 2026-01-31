# ⚡ VOLTAGE Theme Specification
## Motyw dla elektryków/energetyków - inspirowany aplikacją Volta

---

## 1. Paleta Kolorów

### Kolory Główne
| Token | Wartość | Opis |
|-------|---------|------|
| `--voltage-dark` | `#0a0e14` | Ciemne tło kart |
| `--voltage-bg` | `#1a2636` | Jaśniejsze tło główne aplikacji |
| `--voltage-cyan` | `#00e5ff` | Główny kolor akcentu (Electric Cyan) |
| `--voltage-yellow` | `#ffcc00` | Kolor ostrzegawczy/przycisków (Warning Yellow) |
| `--voltage-card` | `#121a26` | Tło kart |

### Kolory Tekstu
| Token | Wartość | Opis |
|-------|---------|------|
| `--t-text` | `#e8eef5` | Główny tekst (jasny) |
| `--t-text-muted` | `#8899aa` | Wyciszony tekst |

### Kolory Statusów
| Status | Kolor | Opis |
|--------|-------|------|
| Active/Online | `#00ff88` | Zielony neonowy |
| Warning | `#ffcc00` | Żółty ostrzegawczy |
| Error/Offline | `#ff4444` | Czerwony błędu |

---

## 2. Tło Główne Aplikacji

### Styl: Siatka techniczna z węzłami
```css
html[data-theme='voltage'] {
    background-color: #1a2636 !important;
    background-image:
        /* Węzły siatki - punkty na przecięciach */
        radial-gradient(circle at center, rgba(0, 229, 255, 0.2) 1.5px, transparent 1.5px),
        /* Mniejsza siatka - subtelna */
        linear-gradient(rgba(0, 229, 255, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 229, 255, 0.08) 1px, transparent 1px),
        /* Większa siatka - bardziej widoczna */
        linear-gradient(rgba(0, 229, 255, 0.12) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 229, 255, 0.12) 1px, transparent 1px),
        /* Gradient bazowy */
        radial-gradient(ellipse at 50% 0%, rgba(40, 60, 85, 0.6) 0%, rgba(26, 38, 54, 1) 70%) !important;
    background-size: 80px 80px, 20px 20px, 20px 20px, 80px 80px, 80px 80px, 100% 100% !important;
    background-attachment: fixed !important;
}
```

---

## 3. Karty (Glass Cards, Lesson Cards)

### Styl: Ciemne panele z lewą cyan ramką (inspiracja Volta)
```css
[data-theme='voltage'] .glass-card,
[data-theme='voltage'] .lesson-card-v3,
[data-theme='voltage'] .mission-item {
    background: linear-gradient(180deg, rgba(14, 20, 30, 0.98) 0%, rgba(10, 14, 22, 0.99) 100%) !important;
    border: 1px solid rgba(0, 229, 255, 0.2) !important;
    border-left: 3px solid #00e5ff !important; /* Charakterystyczna lewa ramka Volta */
    color: #e8eef5 !important;
    border-radius: 6px !important;
    box-shadow: 
        0 4px 20px rgba(0, 0, 0, 0.5),
        inset 0 1px 0 rgba(0, 229, 255, 0.05) !important;
    overflow: hidden;
}
```

### Hover na kartach (bez migotania!)
```css
[data-theme='voltage'] .glass-card:hover,
[data-theme='voltage'] .lesson-card-v3:hover {
    border-color: rgba(0, 229, 255, 0.5) !important;
    border-left-color: #00e5ff !important;
    box-shadow: 
        0 8px 30px rgba(0, 229, 255, 0.15),
        inset 0 1px 0 rgba(0, 229, 255, 0.1) !important;
    transform: translateY(-3px);
    transition: all 0.3s ease !important;
    /* BEZ ANIMACJI - tylko płynne przejście */
}
```

### Znaczniki narożników (Blueprint Style)
```css
html[data-theme='voltage'] .glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 20px;
    height: 20px;
    border-top: 2px solid rgba(0, 229, 255, 0.5);
    border-right: 2px solid rgba(0, 229, 255, 0.5);
    pointer-events: none;
}

html[data-theme='voltage'] .glass-card::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 20px;
    height: 20px;
    border-bottom: 2px solid rgba(0, 229, 255, 0.5);
    border-left: 2px solid rgba(0, 229, 255, 0.5);
    pointer-events: none;
}
```

---

## 4. Typografia

### Fonty
- **Nagłówki**: `'JetBrains Mono', 'Share Tech Mono', 'Consolas', monospace`
- **Body**: Standardowy font aplikacji (Outfit)

### Style nagłówków
```css
html[data-theme='voltage'] h1,
html[data-theme='voltage'] h2,
html[data-theme='voltage'] .page-title h1 {
    font-family: 'JetBrains Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #e8eef5;
    text-shadow: 0 0 12px rgba(0, 229, 255, 0.15);
}
```

---

## 5. Przyciski

### Styl 3D z żółtym tłem (Warning Style)
```css
html[data-theme='voltage'] button,
html[data-theme='voltage'] .btn-primary {
    background: #ffcc00 !important;
    color: #000 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 900 !important;
    border-radius: 2px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    border: none !important;
    box-shadow: 0 4px 0 #997a00, 0 10px 20px rgba(0, 0, 0, 0.3) !important;
    transition: all 0.1s !important;
}

html[data-theme='voltage'] button:hover {
    background: #ffdb4d !important;
    transform: translateY(-1px);
    box-shadow: 0 5px 0 #997a00, 0 12px 24px rgba(0, 0, 0, 0.4) !important;
}

html[data-theme='voltage'] button:active {
    transform: translateY(3px);
    box-shadow: 0 1px 0 #997a00 !important;
}
```

---

## 6. Nawigacja

### Sidebar
```css
html[data-theme='voltage'] .sidebar,
html[data-theme='voltage'] aside {
    background: linear-gradient(180deg, rgba(12, 18, 28, 0.98) 0%, rgba(8, 12, 20, 0.99) 100%) !important;
    border-right: 1px solid rgba(0, 229, 255, 0.15) !important;
}
```

### Aktywny element nawigacji
```css
html[data-theme='voltage'] .nav-item.active {
    background: rgba(0, 229, 255, 0.05);
    border-left: 4px solid #00e5ff;
    color: #00e5ff;
    text-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
}
```

### Bottom Navigation
```css
html[data-theme='voltage'] .bottom-nav {
    background: linear-gradient(180deg, rgba(12, 18, 28, 0.98) 0%, rgba(8, 12, 20, 0.99) 100%) !important;
    border-top: 1px solid rgba(0, 229, 255, 0.2) !important;
    backdrop-filter: blur(20px) !important;
}

html[data-theme='voltage'] .bottom-nav a.active {
    color: #00e5ff !important;
}

/* Kropka pod aktywną ikoną */
html[data-theme='voltage'] .bottom-nav a.active::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 4px;
    height: 4px;
    background: #00e5ff;
    border-radius: 50%;
    box-shadow: 0 0 8px #00e5ff;
}
```

---

## 7. Formularze (Inputy)

```css
html[data-theme='voltage'] input,
html[data-theme='voltage'] select,
html[data-theme='voltage'] textarea {
    background: rgba(10, 14, 20, 0.9) !important;
    border: 1px solid rgba(0, 229, 255, 0.2) !important;
    color: #e8eef5 !important;
    font-family: 'JetBrains Mono', monospace !important;
    border-radius: 4px !important;
}

html[data-theme='voltage'] input:focus,
html[data-theme='voltage'] select:focus,
html[data-theme='voltage'] textarea:focus {
    border-color: #00e5ff !important;
    box-shadow: 0 0 0 2px rgba(0, 229, 255, 0.1) !important;
    outline: none !important;
}
```

---

## 8. Elementy specjalne

### LCD Display (dla wartości liczbowych)
```css
html[data-theme='voltage'] .lcd-display,
html[data-theme='voltage'] .value-display {
    background: #080a0f !important;
    border: 1px solid rgba(0, 229, 255, 0.3) !important;
    border-radius: 2px !important;
    padding: 8px 12px !important;
    font-family: 'Share Tech Mono', monospace !important;
    color: #00e5ff !important;
    text-shadow: 0 0 10px rgba(0, 229, 255, 0.6) !important;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.6) !important;
}
```

### Stat Cards
```css
html[data-theme='voltage'] .stat-card {
    background: #080a0f !important;
    border: 1px solid #1a1d2d !important;
    box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.8) !important;
}

html[data-theme='voltage'] .stat-value {
    font-family: 'Share Tech Mono', 'JetBrains Mono', monospace !important;
    color: #00e5ff !important;
    text-shadow: 0 0 10px rgba(0, 229, 255, 0.8) !important;
}
```

### Paski ostrzegawcze (Hazard Stripes)
```css
html[data-theme='voltage'] .warning-stripe,
html[data-theme='voltage'] .hazard-bar {
    background: repeating-linear-gradient(
        -45deg,
        #ffcc00 0px,
        #ffcc00 10px,
        #1a1a1a 10px,
        #1a1a1a 20px
    );
    height: 6px;
    width: 100%;
    border-radius: 0;
}
```

### Progress Bar
```css
html[data-theme='voltage'] .progress-fill {
    background: linear-gradient(90deg, #007c91, #00e5ff) !important;
    box-shadow: 0 0 15px rgba(0, 229, 255, 0.5) !important;
}
```

---

## 9. Efekty Overlay (EffectsOverlay.tsx)

### Subtelne schematy elektryczne SVG
```tsx
if (theme === 'voltage') {
    return (
        <div style={{ position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 1, overflow: 'hidden' }}>
            <svg 
                style={{ 
                    position: 'absolute', 
                    inset: 0, 
                    width: '100%', 
                    height: '100%',
                    opacity: 0.08
                }}
                viewBox="0 0 1920 1080"
                preserveAspectRatio="xMidYMid slice"
            >
                {/* Linie obwodów z rezystorami */}
                <path d="M0 200 H400 L420 180 L440 220 L460 180 L480 220 L500 200 H800" 
                      stroke="#00e5ff" strokeWidth="1.5" fill="none" />
                
                {/* Węzły połączeniowe */}
                <circle cx="400" cy="200" r="4" fill="#00e5ff" />
                <circle cx="800" cy="200" r="4" fill="#00e5ff" />
                
                {/* Symbol uziemienia */}
                <g transform="translate(300, 700)">
                    <line x1="0" y1="0" x2="0" y2="20" stroke="#00e5ff" strokeWidth="1.5" />
                    <line x1="-10" y1="20" x2="10" y2="20" stroke="#00e5ff" strokeWidth="1.5" />
                    <line x1="-6" y1="25" x2="6" y2="25" stroke="#00e5ff" strokeWidth="1.5" />
                    <line x1="-2" y1="30" x2="2" y2="30" stroke="#00e5ff" strokeWidth="1.5" />
                </g>
                
                {/* Symbol kondensatora */}
                <g transform="translate(1500, 600)">
                    <line x1="0" y1="0" x2="0" y2="15" stroke="#00e5ff" strokeWidth="1.5" />
                    <line x1="-8" y1="15" x2="8" y2="15" stroke="#00e5ff" strokeWidth="2" />
                    <line x1="-8" y1="22" x2="8" y2="22" stroke="#00e5ff" strokeWidth="2" />
                    <line x1="0" y1="22" x2="0" y2="37" stroke="#00e5ff" strokeWidth="1.5" />
                </g>
            </svg>
            
            {/* Skanująca linia */}
            <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '2px',
                background: 'linear-gradient(90deg, transparent 0%, rgba(0, 229, 255, 0.3) 50%, transparent 100%)',
                animation: 'voltageScan 8s linear infinite',
                opacity: 0.5
            }} />
        </div>
    )
}
```

---

## 10. Orby (tło animowane)

```css
html[data-theme='voltage'] .orb {
    background: #00e5ff;
    filter: blur(150px);
    opacity: 0.03; /* Bardzo subtelne */
}
```

---

## 11. Zmienne CSS (do ThemeContext)

```css
[data-theme='voltage'] {
    --t-bg: #0a0e14;
    --t-bg-gradient: radial-gradient(ellipse at 50% 0%, rgba(20, 30, 45, 0.8) 0%, rgba(10, 14, 20, 1) 70%);
    --t-card-bg: linear-gradient(180deg, rgba(18, 26, 38, 0.98) 0%, rgba(12, 18, 28, 0.99) 100%);
    --t-card-border: rgba(0, 229, 255, 0.25);
    --t-card-radius: 6px;
    --t-text: #e8eef5;
    --t-text-muted: #8899aa;
    --t-accent: #ffcc00;
    --t-accent-secondary: #00e5ff;
    --t-accent-glow: rgba(0, 229, 255, 0.6);
    --t-hover-anim: none; /* BEZ migotania */
    --t-hover-transform: translateY(-3px);
    
    --font-heading: 'JetBrains Mono', 'Share Tech Mono', 'Consolas', monospace;
    --voltage-cyan: #00e5ff;
    --voltage-yellow: #ffcc00;
    --voltage-dark: #0a0e14;
    --voltage-card: #121a26;
}
```

---

## 12. Kluczowe zasady designu

1. **Kontrast**: Tło główne (`#1a2636`) MUSI być jaśniejsze niż karty (`#0a0e14`)
2. **Lewa ramka**: Każda karta ma 3px cyan lewą ramkę - charakterystyczny element Volta
3. **Bez migotania**: Hover używa tylko `transition`, NIE `animation`
4. **Typografia**: Monospace dla nagłówków i wartości liczbowych
5. **Przyciski**: Żółte ostrzegawcze z efektem 3D (box-shadow)
6. **Siatka**: Subtelna siatka techniczna z widocznymi węzłami

---

## 13. Inspiracja: Aplikacja Volta

Kluczowe elementy z Volta:
- Ciemne, industrial tło
- Cyan jako główny kolor akcentu
- Lewa kolorowa ramka na kartach
- Żółto-czarne paski ostrzegawcze (hazard stripes)
- Monospace fonty dla danych technicznych
- LCD-style display dla wartości
- Schematy elektryczne jako dekoracja

---

*Specyfikacja utworzona: 31.01.2026*
*Wersja: 1.0*
