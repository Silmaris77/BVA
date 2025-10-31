# 📚 Przewodnik: Komponenty CSS dla Lekcji
## Executive Pro Design System

### 🎨 Paleta kolorów
- **Navy Blue**: `#1E3A8A` - główny kolor
- **Gold**: `#F59E0B` - akcent
- **Platinum**: `#F3F4F6` - tekst na ciemnym tle
- **Success**: `#22c55e` - sukces/tipy
- **Danger**: `#ef4444` - ostrzeżenia/błędy

---

## 📖 Komponenty

### 1️⃣ Header Główny Sekcji
**Klasa**: `.lesson-header-primary`

```html
<div class="lesson-header-primary">
    <h3>🧠 Neurobiologia Przywództwa</h3>
    <p>W tym module poznasz mechanizmy działania ludzkiego mózgu w kontekście przywództwa.</p>
</div>
```

**Wygląd**: Gradient navy → niebieski, białe litery, zaokrąglone rogi

---

### 2️⃣ Karty Informacyjne

#### Info (niebieska)
**Klasa**: `.lesson-card-info`

```html
<div class="lesson-card-info">
    <h4>💡 Ciekawostka</h4>
    <p>Wiesz, że 90% komunikacji to komunikacja niewerbalna?</p>
</div>
```

#### Success (zielona) 
**Klasa**: `.lesson-card-success`

```html
<div class="lesson-card-success">
    <h4>✅ Tip dnia</h4>
    <p>Zacznij każdą rozmowę od pytania otwartego!</p>
</div>
```

#### Warning (pomarańczowa/złota)
**Klasa**: `.lesson-card-warning`

```html
<div class="lesson-card-warning">
    <h4>⚠️ Uważaj!</h4>
    <p>Unikaj zamykania rozmówcy pytaniami typu tak/nie.</p>
</div>
```

#### Danger (czerwona)
**Klasa**: `.lesson-card-danger`

```html
<div class="lesson-card-danger">
    <h4>🚫 Najczęstszy błąd</h4>
    <p>Przerywanie rozmówcy w połowie zdania niszczy zaufanie!</p>
</div>
```

#### Gold (złota z blaskiem)
**Klasa**: `.lesson-card-gold`

```html
<div class="lesson-card-gold">
    <h4>⭐ Kluczowa Umiejętność</h4>
    <p>Aktywne słuchanie to fundament zaufania w zespole.</p>
</div>
```

---

### 3️⃣ Highlight Box
**Klasa**: `.lesson-highlight`

```html
<div class="lesson-highlight">
    <p><strong>Zapamiętaj:</strong> Każda rozmowa to szansa na budowanie zaufania lub jego niszczenie.</p>
</div>
```

**Wygląd**: Delikatne złote tło, złoty pasek z lewej

---

### 4️⃣ Cytaty
**Klasa**: `.lesson-quote`

```html
<div class="lesson-quote">
    <p>„Leadership is not about being in charge. It's about taking care of those in your charge."</p>
    <div class="lesson-quote-author">— Simon Sinek</div>
</div>
```

**Wygląd**: Elegancki, pochylona czcionka, złoty akcent

---

### 5️⃣ Przykłady
**Klasa**: `.lesson-example`

```html
<div class="lesson-example">
    <div class="lesson-example-title">📌 Przykład praktyczny</div>
    <p><strong>Sytuacja:</strong> Członek zespołu popełnił błąd w raporcie.</p>
    <p><strong>Zła reakcja:</strong> "Dlaczego znowu to zepsułeś?!"</p>
    <p><strong>Dobra reakcja:</strong> "Widzę, że w raporcie są niezgodności. Opowiedz mi, co się stało?"</p>
</div>
```

---

### 6️⃣ Listy
**Klasa**: `.lesson-list`

```html
<div class="lesson-list">
    <ul>
        <li><strong>Aktywne słuchanie</strong> - pokazuje szacunek i buduje zaufanie</li>
        <li><strong>Pytania otwarte</strong> - zachęcają do głębszej refleksji</li>
        <li><strong>Parafraza</strong> - potwierdza zrozumienie</li>
    </ul>
</div>
```

---

### 7️⃣ Kluczowe Wnioski (Key Takeaway)
**Klasa**: `.lesson-takeaway`

```html
<div class="lesson-takeaway">
    <h4>🎯 Kluczowe wnioski z tej sekcji:</h4>
    <ul>
        <li>Zaufanie buduje się przez małe, konsekwentne działania</li>
        <li>Oksytocyna vs. kortyzol - chemia naszego mózgu</li>
        <li>Każda rozmowa ma 4 poziomy komunikacji</li>
    </ul>
</div>
```

**Wygląd**: Navy gradient, białe litery, mocny cień - wyróżnia się na stronie

---

### 8️⃣ Krok po Kroku
**Klasa**: `.lesson-steps`

```html
<div class="lesson-steps">
    <div class="lesson-step">
        <h5>Zaobserwuj</h5>
        <p>Zwróć uwagę na mowę ciała rozmówcy - czy jest otwarty czy zamknięty?</p>
    </div>
    <div class="lesson-step">
        <h5>Zapytaj</h5>
        <p>Zadaj pytanie otwarte: "Jak się z tym czujesz?"</p>
    </div>
    <div class="lesson-step">
        <h5>Wysłuchaj</h5>
        <p>Pozwól drugiej osobie mówić bez przerywania - pełna uwaga!</p>
    </div>
    <div class="lesson-step">
        <h5>Podsumuj</h5>
        <p>Sparafrazuj to, co usłyszałeś: "Jeśli dobrze rozumiem..."</p>
    </div>
</div>
```

**Wygląd**: Automatyczna numeracja (1, 2, 3...), złote kółka z numerami

---

### 9️⃣ Podsumowanie Sekcji
**Klasa**: `.lesson-summary`

```html
<div class="lesson-summary">
    <h4>📝 Podsumowanie modułu</h4>
    <p>W tym module nauczyłeś się:</p>
    <ul>
        <li>Jak działa neurobiologia zaufania</li>
        <li>Jakie są 4 poziomy Conversational Intelligence</li>
        <li>Jak świadomie budować relacje przez rozmowy</li>
    </ul>
</div>
```

**Wygląd**: Złota ramka, delikatne świecenie, platynowe tło

---

### 🔟 Dwukolumnowy Layout
**Klasa**: `.lesson-two-columns`

```html
<div class="lesson-two-columns">
    <div class="lesson-card-danger">
        <h4>❌ Red Flags</h4>
        <ul>
            <li>Przerywanie</li>
            <li>Osądzanie</li>
            <li>Ignorowanie emocji</li>
        </ul>
    </div>
    <div class="lesson-card-success">
        <h4>✅ Green Flags</h4>
        <ul>
            <li>Aktywne słuchanie</li>
            <li>Empatia</li>
            <li>Otwartość</li>
        </ul>
    </div>
</div>
```

**Responsive**: Na mobile (< 768px) układa się w jedną kolumnę

---

### 1️⃣1️⃣ Callout Boxes
**Klasy**: `.lesson-callout-info`, `.lesson-callout-tip`, `.lesson-callout-warning`

```html
<div class="lesson-callout-tip">
    <span>💡</span>
    <p>Zacznij każdy dzień od krótkiej rozmowy 1-on-1 z kimś z zespołu!</p>
</div>
```

---

### 1️⃣2️⃣ Tabele
**Klasa**: `.lesson-table`

```html
<table class="lesson-table">
    <thead>
        <tr>
            <th>Poziom</th>
            <th>Cecha</th>
            <th>Hormon</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Poziom 1</td>
            <td>Obrona</td>
            <td>Kortyzol</td>
        </tr>
        <tr>
            <td>Poziom 2</td>
            <td>Współpraca</td>
            <td>Oksytocyna</td>
        </tr>
    </tbody>
</table>
```

---

### 1️⃣3️⃣ Video Embed
**Klasa**: `.lesson-video`

```html
<div class="lesson-video">
    <iframe src="https://www.youtube.com/embed/VIDEO_ID" allowfullscreen></iframe>
</div>
```

**Wygląd**: Responsywny 16:9, zaokrąglone rogi

---

### 1️⃣4️⃣ Progress Bar
**Klasa**: `.lesson-progress`

```html
<div class="lesson-progress">
    <div class="lesson-progress-label">
        <span>Twój postęp w module:</span>
        <span>75%</span>
    </div>
    <div class="lesson-progress-bar">
        <div class="lesson-progress-fill" style="width: 75%"></div>
    </div>
</div>
```

**Wygląd**: Złoty gradient, płynna animacja

---

## 🛠️ Utility Classes

### Spacing
```html
<div class="lesson-spacing-sm">  <!-- margin: 12px 0 -->
<div class="lesson-spacing-md">  <!-- margin: 20px 0 -->
<div class="lesson-spacing-lg">  <!-- margin: 32px 0 -->
<div class="lesson-spacing-xl">  <!-- margin: 48px 0 -->
```

---

## ✅ Best Practices

### DO ✅
- Używaj **semantycznych klas** (`.lesson-card-success` zamiast `.green-box`)
- Łącz komponenty (np. `.lesson-card-info` + `.lesson-spacing-lg`)
- Dodawaj emoji w nagłówkach dla wizualnego rozróżnienia
- Używaj `<strong>` dla kluczowych słów w tekście
- Strukturyzuj treść hierarchicznie (header → karty → podsumowanie)

### DON'T ❌
- **Nigdy** nie używaj inline styles (`style="..."`)
- **Nigdy** nie mieszaj jasnych kolorów tła z jasnymi tekstami
- Nie używaj więcej niż 3-4 różnych typów kart w jednej lekcji
- Nie duplikuj tych samych informacji w różnych komponentach
- Nie przesadzaj z emoji (max 1 na kartę/nagłówek)

---

## 📋 Przykład Kompletnej Lekcji

```html
<!-- HEADER GŁÓWNY -->
<div class="lesson-header-primary">
    <h3>🧠 Neurobiologia Zaufania</h3>
    <p>Odkryj, jak twój mózg buduje lub niszczy zaufanie w każdej rozmowie.</p>
</div>

<!-- WPROWADZENIE -->
<p>Czy wiesz, że każda rozmowa wywołuje reakcję chemiczną w mózgu? Poznajmy mechanizmy...</p>

<!-- KLUCZOWA KONCEPCJA -->
<div class="lesson-card-gold">
    <h4>⭐ Kluczowa koncepcja: Oksytocyna vs. Kortyzol</h4>
    <p>To nie metafora - zaufanie i strach to rzeczywiste substancje chemiczne w naszym mózgu!</p>
</div>

<!-- PRZYKŁAD PRAKTYCZNY -->
<div class="lesson-example">
    <div class="lesson-example-title">📌 Przykład z życia</div>
    <p><strong>Sytuacja:</strong> Pracownik przychodzi z problemem...</p>
    <p><strong>Reakcja typu A (kortyzol):</strong> "Nie mam czasu na to teraz!"</p>
    <p><strong>Reakcja typu B (oksytocyna):</strong> "Usiądź, opowiedz mi o tym."</p>
</div>

<!-- KROKI DO WDROŻENIA -->
<div class="lesson-spacing-lg">
    <h4>Jak to zastosować w praktyce?</h4>
</div>

<div class="lesson-steps">
    <div class="lesson-step">
        <h5>Zauważ moment</h5>
        <p>Gdy ktoś do Ciebie podchodzi - zatrzymaj się na chwilę.</p>
    </div>
    <div class="lesson-step">
        <h5>Skontaktuj wzrokiem</h5>
        <p>Odłóż telefon, odwróć się, nawiąż kontakt wzrokowy.</p>
    </div>
    <div class="lesson-step">
        <h5>Otwórz przestrzeń</h5>
        <p>"Opowiedz mi więcej..." zamiast "Tak, ok, zrobię to."</p>
    </div>
</div>

<!-- TIP -->
<div class="lesson-callout-tip">
    <span>💡</span>
    <p>Wystarczy 2 minuty pełnej uwagi, by wywołać reakcję oksytocyny!</p>
</div>

<!-- PODSUMOWANIE -->
<div class="lesson-summary">
    <h4>📝 Co zapamiętać z tej sekcji?</h4>
    <ul>
        <li>Każda rozmowa = reakcja chemiczna w mózgu</li>
        <li>Oksytocyna = hormon zaufania i więzi</li>
        <li>Kortyzol = hormon stresu i obrony</li>
        <li>Masz wybór: który hormon wywołasz swoją reakcją?</li>
    </ul>
</div>

<!-- KEY TAKEAWAY -->
<div class="lesson-takeaway">
    <h4>🎯 Praktyczne zadanie na dziś:</h4>
    <p>Wybierz JEDNĄ osobę z zespołu i daj jej dzisiaj 5 minut pełnej, nieprzerwanej uwagi. Obserwuj efekt!</p>
</div>
```

---

## 🎨 Paleta Executive Pro w CSS Variables

Możesz też używać zmiennych CSS bezpośrednio:

```css
background: var(--primary-navy);     /* #1E3A8A */
color: var(--accent-gold);           /* #F59E0B */
color: var(--text-primary);          /* #F3F4F6 - jasny tekst */
color: var(--text-secondary);        /* #cbd5e1 - nieco przyciemniony */
background: var(--background-card);  /* ciemne tło karty */
background: var(--surface-elevated); /* nieco jaśniejsze */
```

---

## 🚀 Gotowe do użycia!

System jest już zintegrowany z motywem **Executive Pro**. Wszystkie komponenty:
- ✅ Mają poprawny kontrast (WCAG AA)
- ✅ Są responsywne (mobile-first)
- ✅ Używają spójnej palety Navy/Gold/Platinum
- ✅ Działają w ciemnym motywie
- ✅ Mają płynne animacje i przejścia

**Kopiuj komponenty z tego przewodnika i twórz profesjonalne lekcje! 🎓**
