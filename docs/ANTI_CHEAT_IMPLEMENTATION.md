# 🛡️ System Anti-Cheat - Implementacja Zakończona

## ✅ Co zostało zaimplementowane?

### 1. Moduł `utils/anti_cheat.py` (400+ linii)
**Funkcje główne:**
- `check_for_cheating()` - kompleksowa analiza oszustw
- `analyze_writing_time()` - detekcja zbyt szybkiego pisania
- `analyze_paste_behavior()` - wykrywanie masowego wklejania
- `analyze_ai_patterns()` - pattern matching typowych fraz AI
- `analyze_with_gemini_ai_detector()` - detekcja AI przez Gemini
- `format_anti_cheat_warning()` - formatowanie ostrzeżeń
- `apply_anti_cheat_penalty()` - aplikowanie kar do oceny

### 2. Integracja z Business Games

**`utils/business_game.py`:**
- Zmodyfikowano `submit_contract_solution()` aby przyjmowała `start_time` i `paste_events`
- Dodano wywołanie `check_for_cheating()` przed oceną
- Dodano aplikowanie kary do ratingu
- Dodano ostrzeżenia anti-cheat do feedbacku

**`views/business_games.py`:**
- Dodano tracking czasu rozpoczęcia pisania (`session_state`)
- Dodano JavaScript monitoring paste events
- Dodano przekazywanie danych anti-cheat do `submit_contract_solution()`
- Dodano czyszczenie tracking data po submit

### 3. Dokumentacja
- `docs/ANTI_CHEAT_SYSTEM.md` - pełna dokumentacja systemu
- `test_anti_cheat.py` - testy jednostkowe

## 🔍 Jak to działa dla użytkownika?

### Scenariusz 1: Użytkownik uczciwy ✅
1. Otwiera kontrakt, zaczyna pisać
2. Pisze 300 słów w 5 minut
3. Wkleja 2-3 małe fragmenty (cytaty, przykłady)
4. Wysyła rozwiązanie

**Wynik:** Brak kar, normalna ocena 1-5 ⭐

### Scenariusz 2: Copy-paste z ChatGPT ⚠️
1. Otwiera kontrakt
2. Kopiuje zadanie do ChatGPT
3. ChatGPT generuje 500 słów w 10 sekund
4. Wkleja całość (2500 znaków) do aplikacji
5. Wysyła po 30 sekundach

**Wykrywanie:**
- ⏱️ Zbyt szybko: 30s dla 500 słów → **-1 ⭐**
- 📋 Wklejanie: 100% tekstu → **-1 ⭐**
- 🤖 Wzorce AI: "W tej sytuacji...", "należy rozważyć" → Uruchom Gemini
- 🧠 Gemini AI: Confidence 92% → **-2 ⭐**
- ⚠️ Wiele flag (3+) → **KARA: -3 ⭐**

**Wynik:** Ocena obniżona o 3 gwiazdki (np. 5→2 ⭐)

**Komunikat:**
```
⚠️ WYKRYTO PODEJRZANĄ AKTYWNOŚĆ

⚠️ Podejrzanie szybkie wypełnienie: 30s dla 500 słów 
   (oczekiwano min. 100s)

⚠️ Wykryto masowe wklejanie: 100% tekstu wklejone (2500/2500 znaków)

🤖 Wykryto AI-generowany tekst (pewność: 92%): 
   Tekst charakteryzuje się typową strukturą AI z formalnymi 
   frazami ("należy rozważyć", "w kontekście") i brakiem 
   osobistych przykładów.

⚠️ KARA: -3 ⭐ do oceny

---

💬 Feedback od klienta:
[normalny feedback, ale z niższą oceną]
```

## 🎯 Parametry systemu

### Progi czasowe
```python
MIN_TIME_THRESHOLDS = {
    100: 20,   # 100 słów = min 20s (300 słów/min)
    200: 40,   # 200 słów = min 40s
    300: 60,   # 300 słów = min 60s (1 min)
    500: 100,  # 500 słów = min 100s (~1.5 min)
    1000: 200, # 1000 słów = min 200s (~3 min)
}
```

### Próg wklejania
```python
MAX_PASTE_PERCENTAGE = 80  # 80% tekstu wklejonego = podejrzane
```

### Kary
```python
PENALTIES = {
    "time_suspicious": -1,   # Zbyt szybko
    "paste_detected": -1,    # Masowe wklejanie
    "ai_detected": -2,       # AI wykryte przez Gemini
    "multiple_flags": -3     # 2+ flagi jednocześnie
}
```

### Wzorce AI (regex)
```python
AI_PATTERNS = [
    r"^(W tej sytuacji|Aby rozwiązać|W celu)",
    r"(należy rozważyć|istotne jest|warto zwrócić uwagę)",
    r"(w kontekście|z perspektywy|biorąc pod uwagę)",
    r"^\d+\.\s+[A-ZĄŻŹĆŁŚÓĘŃ]",  # Numerowane listy
]
```

## 📊 Wyniki testów

```
✅ TEST 1: Analiza czasu pisania
   - Normalna prędkość (300 słów, 90s): ✅ OK
   - Zbyt szybko (500 słów, 30s): ⚠️ WYKRYTO (-1 ⭐)

✅ TEST 2: Analiza wklejania
   - Małe wklejenia (80/1000 znaków): ✅ OK
   - Masowe wklejanie (2400/2500 znaków): ⚠️ WYKRYTO (-1 ⭐)

✅ TEST 3: Detekcja wzorców AI
   - Tekst ludzki: ✅ 0 wzorców
   - Tekst AI: ⚠️ 5 wzorców wykrytych

✅ TEST 4-6: Kompleksowa analiza + ostrzeżenia + kary
   - Wszystkie funkcje działają poprawnie
```

## 🚀 Jak używać?

### Dla użytkowników (automatyczne)
System działa automatycznie w tle. Użytkownik nie musi nic robić.
Jeśli zostanie wykryte oszustwo, dostanie ostrzeżenie w feedbacku.

### Dla administratorów

**1. Włącz/wyłącz AI detection:**
```python
# W utils/business_game.py, funkcja submit_contract_solution()
use_ai_detection=True  # Włącz Gemini (kosztuje API)
use_ai_detection=False # Wyłącz (tylko pattern matching)
```

**2. Dostosuj progi:**
Edytuj `utils/anti_cheat.py`:
- `MIN_TIME_THRESHOLDS` - zmień wymagany czas
- `MAX_PASTE_PERCENTAGE` - zmień % wklejania
- `PENALTIES` - zmień wysokość kar
- `AI_PATTERNS` - dodaj/usuń wzorce

**3. Uruchom testy:**
```bash
python test_anti_cheat.py
```

## 💡 Zalecenia

### Dla prowadzących kurs:
1. **Komunikuj zasady**: Powiedz uczniom że system anty-oszukiwania jest aktywny
2. **Edukuj**: Wyjaśnij jak pisać własne rozwiązania (osobiste przykłady, doświadczenia)
3. **Monitoruj**: Sprawdzaj kontrakty z flagami anti-cheat w historii
4. **Dostosuj progi**: Jeśli za dużo fałszywych alarmów, zwiększ `MIN_TIME_THRESHOLDS`

### Dla uczestników:
1. **Pisz od zera**: Nie kopiuj całych tekstów z AI
2. **Dodawaj osobiste konteksty**: "W mojej firmie...", "Kiedyś pracowałem..."
3. **Poświęć czas**: 300 słów to ~5 minut minimum
4. **Używaj AI jako inspiracji**: OK jest przeczytać AI odpowiedź, potem napisać własną

## 🔮 Przyszłe ulepszenia (opcjonalnie)

### Faza 2:
- 📊 Dashboard anti-cheat dla admina (statystyki wykryć)
- 🚫 Automatyczny ban po 5+ wykrytych oszustwach
- 📧 Email powiadomienia dla prowadzącego
- 🏆 Badge "Uczciwy Gracz" dla czystych kont

### Faza 3:
- 🔍 Fingerprinting stylu pisania (każdy pisze inaczej)
- 📈 Machine Learning na własnym datasecie
- 🌐 Integracja z GPTZero / Originality.ai
- 🎯 Personalizowane pytania kontrolne po submit

## ❓ FAQ

**Q: Czy mogę dostać karę przez przypadek?**
A: Tak, możliwe są fałszywe alarmy. Dlatego kary są umiarkowane (-1 do -3 ⭐) i minimalna ocena to 1 ⭐.

**Q: Jak sprawdzić czy moje rozwiązanie będzie flagowane?**
A: Pisz własny tekst od zera, dodawaj osobiste przykłady, poświęć min. 5 minut na 300 słów.

**Q: Co jeśli Gemini się myli?**
A: Gemini uruchamia się tylko gdy są inne podejrzane sygnały (czas + wklejanie). Sam AI detection nie karze.

**Q: Czy mogę używać AI jako pomocy?**
A: Tak! Możesz przeczytać AI odpowiedź dla inspiracji, ale napisz własne rozwiązanie własnymi słowami.

**Q: Ile kosztuje Gemini AI detection?**
A: ~500 tokenów per analiza. Przy 100 kontraktach z 10% flagami = ~5000 tokenów = ~$0.01

## ✅ Gotowe do produkcji!

System jest w pełni funkcjonalny i gotowy do użycia.
Wszystkie testy przechodzą, dokumentacja kompletna.

**Uruchom aplikację i przetestuj:**
```bash
streamlit run main.py
```

Przejdź do Business Games → Kontrakt → Spróbuj wkleić tekst z ChatGPT 😈
