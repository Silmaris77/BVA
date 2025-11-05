# 🎨 BVA Educational Materials - Przewodnik Stylistyczny

## 📋 Spis treści
1. [System kolorów - kiedy używać](#system-kolorów)
2. [Emoji - hierarchia i znaczenie](#emoji-standardy)
3. [Struktura lekcji](#struktura-lekcji)
4. [Przykłady użycia](#przykłady)

---

## 🎨 System kolorów - kiedy używać

### 🔵 **Info Box (Niebieski)** - `.info-box`
**Kiedy:** Teoria, definicje, wyjaśnienia, kontekst biznesowy

**Użyj gdy:**
- Wyjaśniasz pojęcie lub termin
- Dajesz kontekst merytoryczny
- Przedstawiasz ogólną informację
- Opisujesz "jak to działa"

**Przykład:**
```html
<div class="info-box">
    <h3>🎯 Co to jest Food Cost?</h3>
    <p>Food cost to stosunek kosztu surowców do ceny sprzedaży dania...</p>
</div>
```

---

### 🟢 **Success Box (Zielony)** - `.success-box`
**Kiedy:** Dobre praktyki, checklisty, przykłady sukcesu, "tak rób"

**Użyj gdy:**
- Pokazujesz właściwy sposób działania
- Prezentujesz checklistę
- Dajesz pozytywne przykłady
- Podkreślasz korzyści

**Przykład:**
```html
<div class="success-box">
    <h4>✅ Dobra rozmowa z klientem</h4>
    <p>"Heinz ma wyższą cenę, ale niższy koszt porcji - oszczędzasz 20 zł miesięcznie."</p>
</div>
```

---

### 🔴 **Error Box (Czerwony)** - `.error-box`
**Kiedy:** Błędy, pułapki, "tak NIE rób", ostrzeżenia krytyczne

**Użyj gdy:**
- Pokazujesz typowe błędy
- Ostrzegasz przed pułapkami
- Prezenujesz negatywne przykłady
- Wyjaśniasz co unikać

**Przykład:**
```html
<div class="error-box">
    <h4>❌ Zła rozmowa</h4>
    <p>"OK, dam Panu -12% rabatu." → Efekt: zniszczona wartość marki</p>
</div>
```

---

### 🟡 **Warning Box (Żółty)** - `.warning-box`
**Kiedy:** Uwaga, wskazówki, tipy, porady praktyczne

**Użyj gdy:**
- Dajesz praktyczną wskazówkę
- Chcesz zwrócić uwagę na szczegół
- Podajesz "pro tip"
- Sugerujesz uważność

**Przykład:**
```html
<div class="warning-box">
    <h4>💡 Pro tip</h4>
    <p>Aktualizuj tracking cen PRZED spotkaniem z klientem - świeże dane = silniejsza pozycja!</p>
</div>
```

---

### 🟠 **Highlight Box (Pomarańczowy)** - `.highlight-box`
**Kiedy:** Przykłady, case studies, scenariusze praktyczne

**Użyj gdy:**
- Prezentujesz case study
- Pokazujesz praktyczny scenariusz
- Dajesz przykład z życia
- Ilustrujesz teorię praktyką

**Przykład:**
```html
<div class="highlight-box">
    <h4>📋 Case study: Burgerownia</h4>
    <p>Restauracja X zmieniła dostawcę ketchupu i food cost wzrósł o 2%...</p>
</div>
```

---

### 🟣 **Tool Box (Fioletowy)** - `.tool-box`
**Kiedy:** Narzędzia, kalkulatory, elementy interaktywne

**Użyj gdy:**
- Wprowadzasz kalkulator
- Pokazujesz narzędzie (Excel, arkusz)
- Prezentujesz element interaktywny
- Dajesz "narzędzie do użycia"

**Przykład:**
```html
<div class="tool-box">
    <h4>🧮 Kalkulator Food Cost</h4>
    <p>Wpisz koszt składników i cenę sprzedaży, aby obliczyć marżę...</p>
</div>
```

---

## 🎯 Emoji standardy - hierarchia i znaczenie

### **Emoji dla Tabów**
```
📖 Wprowadzenie / Teoria
🎯 Praktyka / Zastosowanie
💬 Komunikacja / Rozmowy
📊 Dane / Analiza / Wykresy
🧮 Kalkulatory / Narzędzia interaktywne
🛠️ Narzędzia praktyczne (Excel, templates)
📈 Tracking / Monitoring
💰 Finanse / Ceny / Rabaty
🏪 Merchandising / Shelf
✅ Podsumowanie / Checklist
```

### **Emoji dla Nagłówków (wewnątrz treści)**
```
🎯 Cel / Główna idea
💡 Wskazówka / Insight
⚠️ Uwaga / Ostrzeżenie
✅ Zalety / Dobre praktyki
❌ Wady / Błędy / Pułapki
📋 Lista / Checklist
🔍 Przykład / Case study
📐 Wzór / Formula
🔹 Punkt kluczowy
💬 Cytat / Dialog
🚀 Action item / Do zrobienia
```

### **Emoji dla Boxów**
```
ℹ️ Info box (niebieski)
✅ Success box (zielony)
❌ Error box (czerwony)
💡 Warning box (żółty)
📋 Highlight box (pomarańczowy)
🧮 Tool box (fioletowy)
```

---

## 📚 Struktura lekcji

### **Typowa struktura (elastyczna - dostosuj do merytoryki)**

```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Tytuł Lekcji</title>
    <link rel="stylesheet" href="bva_educational_styles.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Tytuł Lekcji</h1>
            <p>Krótki opis / subtitle</p>
        </div>
        
        <div class="tabs">
            <button class="tab-button active" onclick="openTab('tab1')">📖 Tab 1</button>
            <button class="tab-button" onclick="openTab('tab2')">🎯 Tab 2</button>
            <!-- więcej tabów według potrzeb -->
        </div>
        
        <div class="content">
            <!-- Treść tabów -->
        </div>
    </div>
    
    <div class="footer">
        <button class="footer-button" onclick="scrollToTop()">
            ⬆️ Powrót na górę
        </button>
        <div style="font-size: 1.2rem; font-weight: 600;">
            BVA Educational Materials
        </div>
        <div style="opacity: 0.9; font-size: 0.95rem;">
            Nazwa lekcji | Data: 2025-11-05 | Wersja: 1.0
        </div>
    </div>
    
    <script src="bva_educational_scripts.js"></script>
</body>
</html>
```

---

## 💡 Przykłady użycia

### **Przykład 1: Teoria + Praktyka**
```html
<!-- TEORIA (niebieski) -->
<div class="info-box">
    <h3>📖 Czym jest merchandising?</h3>
    <p>Merchandising to technika prezentacji produktu...</p>
</div>

<!-- PRAKTYKA (zielony) -->
<div class="success-box">
    <h4>✅ Jak to zrobić w praktyce</h4>
    <ol>
        <li>Umieść produkt na wysokości oczu</li>
        <li>Użyj shelf talkera z ceną</li>
    </ol>
</div>
```

### **Przykład 2: Dobre vs Złe praktyki**
```html
<!-- ZŁE (czerwony) -->
<div class="error-box">
    <h4>❌ Zła praktyka</h4>
    <p>"Dam Panu -15% rabatu" → Zniszczenie wartości marki</p>
</div>

<!-- DOBRE (zielony) -->
<div class="success-box">
    <h4>✅ Dobra praktyka</h4>
    <p>"Zamiast rabatu dam pakiet 4+1 - to 20% oszczędności na porcji"</p>
</div>
```

### **Przykład 3: Wskazówka praktyczna**
```html
<div class="warning-box">
    <h4>💡 Pro tip</h4>
    <p>Przed spotkaniem z klientem sprawdź ceny konkurencji - 
    będziesz mieć silniejszą pozycję negocjacyjną!</p>
</div>
```

### **Przykład 4: Case Study**
```html
<div class="highlight-box">
    <h4>📋 Case study: Burgerownia XYZ</h4>
    <p>Restauracja X zmieniła ketchup z produktu standardowego na Heinz...</p>
    <p><strong>Efekt:</strong> Food cost spadł o 1,5%, goście docenili jakość</p>
</div>
```

### **Przykład 5: Kalkulator**
```html
<div class="tool-box">
    <h4>🧮 Kalkulator interaktywny</h4>
    <div class="calculator">
        <input type="number" id="koszt" placeholder="Koszt składników">
        <input type="number" id="cena" placeholder="Cena sprzedaży">
        <button onclick="calculate()">Oblicz Food Cost</button>
    </div>
</div>
```

---

## ✅ Zasady ogólne

### **DO:**
✅ Używaj kolorów zgodnie z ich znaczeniem  
✅ Konsekwentnie stosuj emoji  
✅ Dopasowuj liczbę tabów do merytoryki (elastycznie)  
✅ Używaj blockquote dla cytatów/motywacyjnych zdań  
✅ Dodawaj stopkę w każdej lekcji  

### **NIE:**
❌ Nie mieszaj znaczeń kolorów (np. niebieski dla błędów)  
❌ Nie używaj więcej niż 1-2 emoji w nagłówku  
❌ Nie zmuszaj treści do 5 tabów "bo standard"  
❌ Nie używaj inline styles (używaj klas z CSS)  

---

## 🔄 Aktualizacje

**Wersja 1.0** (2025-11-05)
- Pierwszy standard kolorystyczny
- Definicje znaczeń emoji
- Przykłady użycia boxów
