# 🛡️ Anti-Cheat System - Dokumentacja

## Przegląd

System wykrywania oszustw w Business Games chroni przed:
- Copy-paste z ChatGPT i innych AI
- Zbyt szybkim wypełnianiem rozwiązań
- Masowym wklejaniem gotowych tekstów

## Jak działa?

### 1. ⏱️ **Analiza czasu pisania**
System mierzy czas od otwarcia pola tekstowego do wysłania rozwiązania.

**Progi czasowe:**
- 100 słów = minimum 20 sekund
- 300 słów = minimum 60 sekund
- 500 słów = minimum 100 sekund
- 1000 słów = minimum 200 sekund

**Wykrywanie:**
- Jeśli użytkownik pisze 500 słów w 30 sekund → **PODEJRZANE**
- Kara: -1 ⭐

### 2. 📋 **Monitoring wklejania**
JavaScript śledzi zdarzenia `paste` w polu tekstowym.

**Wykrywanie:**
- Jeśli >80% tekstu wklejone → **PODEJRZANE**
- Jeśli pojedyncze wklejenie >500 słów → **PODEJRZANE**
- Kara: -1 ⭐

### 3. 🤖 **Detekcja AI (Pattern Matching)**
System szuka charakterystycznych wzorców AI:

**Polskie frazy:**
- "W tej sytuacji...", "Aby rozwiązać..."
- "należy rozważyć", "istotne jest"
- "w kontekście", "z perspektywy"

**Angielskie frazy:**
- "In this situation...", "To solve..."
- "it is important to", "should consider"

**Struktura:**
- Numerowane listy zaczynające każde zdanie
- Zbyt perfekcyjna struktura bez błędów

**Wykrywanie:**
- Jeśli 3+ wzorce wykryte → Uruchom Gemini AI

### 4. 🧠 **Gemini AI Detection**
Jeśli wykryto podejrzane wzorce, Gemini analizuje tekst:

**Prompt do Gemini:**
```
Jesteś ekspertem od wykrywania tekstów AI.
Przeanalizuj czy tekst został wygenerowany przez AI.
Zwróć JSON: {is_ai_generated, confidence, explanation}
```

**Wykrywanie:**
- Confidence >70% → **AI WYKRYTE**
- Kara: -2 ⭐

### 5. ⚠️ **Wiele flag**
Jeśli użytkownik ma 2+ podejrzane flagi:
- Kara zwiększona do: **-3 ⭐**

## Kary

| Typ oszustwa | Kara | Opis |
|--------------|------|------|
| Zbyt szybkie pisanie | -1 ⭐ | Czas < minimum dla długości |
| Masowe wklejanie | -1 ⭐ | >80% tekstu wklejone |
| AI wykryte | -2 ⭐ | Gemini confidence >70% |
| Wiele flag | -3 ⭐ | 2+ problemy jednocześnie |

**Minimalna ocena:** 1 ⭐ (nawet z karami)

## Komunikaty dla użytkownika

### Przykład 1: Zbyt szybkie
```
⚠️ WYKRYTO PODEJRZANĄ AKTYWNOŚĆ

⚠️ Podejrzanie szybkie wypełnienie: 45s dla 500 słów 
   (oczekiwano min. 100s)

⚠️ KARA: -1 ⭐ do oceny

---

💬 Feedback od klienta:
[normalny feedback...]
```

### Przykład 2: AI + Wklejanie
```
⚠️ WYKRYTO PODEJRZANĄ AKTYWNOŚĆ

⚠️ Wykryto masowe wklejanie: 95% tekstu wklejone (2400/2500 znaków)

🤖 Wykryto AI-generowany tekst (pewność: 85%): 
   Tekst charakteryzuje się typową strukturą AI z formalnymi 
   frazami i brakiem osobistych przykładów.

⚠️ KARA: -3 ⭐ do oceny (wiele flag)

---

💬 Feedback od klienta:
[normalny feedback...]
```

## Implementacja techniczna

### Frontend (JavaScript)
```javascript
textarea.addEventListener('paste', function(e) {
    const pastedText = e.clipboardData.getData('text');
    const event = {
        'length': pastedText.length,
        'total_solution_length': textarea.value.length,
        'timestamp': new Date().toISOString()
    };
    localStorage.setItem('paste_events_X', JSON.stringify(events));
});
```

### Backend (Python)
```python
# W business_game.py
from utils.anti_cheat import check_for_cheating

anti_cheat_result = check_for_cheating(
    solution=solution,
    start_time=start_time,
    submit_time=datetime.now(),
    paste_events=paste_events,
    use_ai_detection=True
)

if anti_cheat_result["is_suspicious"]:
    rating = apply_anti_cheat_penalty(rating, penalty)
```

## Konfiguracja

Edytuj `utils/anti_cheat.py`:

```python
# Zmień progi czasowe
MIN_TIME_THRESHOLDS = {
    100: 30,   # Zwiększ z 20s na 30s
    300: 90,   # Zwiększ z 60s na 90s
}

# Zmień % wklejania
MAX_PASTE_PERCENTAGE = 70  # Zmniejsz z 80% na 70%

# Zmień kary
PENALTIES = {
    "time_suspicious": -2,  # Zwiększ karę
    "ai_detected": -3,      # Zwiększ karę
}
```

## FAQ

**Q: Czy system może dać fałszywe alarmy?**
A: Tak, dlatego kary są umiarkowane (-1 do -3 ⭐) i minimalna ocena to 1 ⭐. Użytkownik zawsze dostaje feedback nawet z karą.

**Q: Co jeśli ktoś pisze szybko?**
A: Progi są konserwatywne (20s/100 słów = 300 słów/minutę). Bardzo szybcy pisarze mogą przekroczyć, ale kara to tylko -1 ⭐.

**Q: Jak wyłączyć AI detection?**
A: W `submit_contract_solution()` ustaw `use_ai_detection=False`

**Q: Czy Gemini kosztuje?**
A: Tak, każda analiza AI to ~500 tokenów. Dlatego uruchamiamy tylko gdy są podejrzane wzorce.

**Q: Jak użytkownik może uniknąć kar?**
A: 
1. Pisz własne rozwiązania od zera
2. Nie kopiuj całych bloków tekstu
3. Dodawaj osobiste przykłady i doświadczenia
4. Poświęć realistyczną ilość czasu

## Statystyki (przykład)

Po 100 kontraktach:
- 🟢 Czyste: 85%
- 🟡 Podejrzany czas: 10% (kara -1 ⭐)
- 🟡 Wklejanie: 3% (kara -1 ⭐)
- 🔴 AI wykryte: 2% (kara -2 do -3 ⭐)

## Roadmap

**Faza 1 (DONE):** ✅
- ⏱️ Tracking czasu
- 📋 Detekcja wklejania
- 🤖 Pattern matching
- 🧠 Gemini AI detection

**Faza 2 (TODO):**
- 📊 Dashboard anti-cheat dla admina
- 🚫 Ban po 5+ wykrytych oszustwach
- 📧 Email powiadomienia dla prowadzącego
- 🏆 Badge "Uczciwy Gracz" dla czystych kont

**Faza 3 (TODO):**
- 🔍 Analiza stylu pisania (fingerprinting)
- 📈 Uczenie maszynowe na własnym datasecie
- 🌐 Integracja z GPTZero/Originality.ai
