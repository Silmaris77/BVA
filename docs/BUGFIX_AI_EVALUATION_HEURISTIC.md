# 🐛 Bugfix - Ocena AI nie działa (zawsze heuristic)

## Problem

Po włączeniu trybu AI, system nadal używał oceny heurystycznej:
```json
{
  "method": "heuristic",  ← powinno być "ai"
  "word_count": 237,
  "rating": 3
}
```

## 🔍 Przyczyny (5 problemów!)

### 1. ❌ Błędny model Gemini
**Problem:** `gemini-1.5-flash` nie istnieje dla API v1beta
```
404 models/gemini-1.5-flash is not found for API version v1beta
```

**Rozwiązanie:** Zmieniono na `gemini-2.5-flash` (stabilny, dostępny)

### 2. ❌ Safety Settings blokują odpowiedzi
**Problem:** finish_reason=2 (SAFETY) - Gemini blokowało treści edukacyjne
```
Invalid operation: The `response.text` quick accessor requires 
the response to contain a valid `Part`, but none were returned. 
The candidate's [finish_reason] is 2.
```

**Rozwiązanie:** Dodano safety_settings z BLOCK_NONE dla kategorii HARM

### 3. ❌ Błędne pole w kontrakcie
**Problem:** Prompt używał `contract["poziom_trudnosci"]`, ale kontrakty mają pole `"trudnosc"`
```python
# BŁĄD:
contract_difficulty=contract["poziom_trudnosci"]  # KeyError!

# POPRAWKA:
contract_difficulty=contract.get("trudnosc", 3)
```

### 4. ❌ DEFAULT_EVALUATION_MODE = "heuristic"
**Problem:** Domyślna wartość w kodzie była "heuristic" zamiast "ai"

**Rozwiązanie:** Zmieniono na `DEFAULT_EVALUATION_MODE = "ai"`

### 5. ❌ Brak retry logic dla zablokowanych odpowiedzi
**Problem:** Gdy safety blokowała, od razu fallback do heurystyki

**Rozwiązanie:** Dodano retry bez safety_settings

## ✅ Wykonane naprawy

### Plik: `config/business_games_settings.py`

**Linia 44:**
```python
# PRZED:
DEFAULT_EVALUATION_MODE = "heuristic"

# PO:
DEFAULT_EVALUATION_MODE = "ai"
```

**Linia 52:**
```python
# PRZED:
"model": "gemini-1.5-flash",  # Model nie istnieje!

# PO:
"model": "gemini-2.5-flash",  # Stabilny model Gemini 2.5
```

### Plik: `utils/business_game_evaluation.py`

**Linia 182 - Poprawiono pole kontraktu:**
```python
# PRZED:
contract_difficulty=contract["poziom_trudnosci"],  # Błąd!

# PO:
contract_difficulty=contract.get("trudnosc", 3),  # Poprawnie
```

**Linia 210-220 - Dodano safety settings:**
```python
# DODANO:
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name=AI_EVALUATION_CONFIG["model"],
    generation_config=AI_EVALUATION_CONFIG["generation_config"],
    system_instruction=AI_EVALUATION_CONFIG["system_instruction"],
    safety_settings=safety_settings  # ← DODANO
)
```

**Linia 228-240 - Dodano retry logic:**
```python
# DODANO:
if not response.candidates or not response.candidates[0].content.parts:
    # Odpowiedź zablokowana - spróbuj bez safety settings
    print("⚠️ Odpowiedź zablokowana przez safety settings, próbuję ponownie bez nich...")
    model_no_safety = genai.GenerativeModel(
        model_name=AI_EVALUATION_CONFIG["model"],
        generation_config=AI_EVALUATION_CONFIG["generation_config"],
        system_instruction=AI_EVALUATION_CONFIG["system_instruction"]
    )
    response = model_no_safety.generate_content(prompt)
```

### Plik: `config/business_games_active_mode.json`

```json
{
  "evaluation_mode": "ai",
  "updated_at": "2025-10-19 01:23:46"
}
```

## 📊 Test weryfikacyjny

Utworzono `test_ai_evaluation.py` który:
1. ✅ Testuje funkcję `evaluate_with_ai()` bezpośrednio
2. ✅ Pokazuje dokładne błędy (nie tylko fallback)
3. ✅ Weryfikuje API key
4. ✅ Sprawdza import google.generativeai

Utworzono `list_gemini_models.py` który:
1. ✅ Listuje wszystkie dostępne modele Gemini
2. ✅ Pokazuje które wspierają generateContent
3. ✅ Pomaga wybrać właściwy model

## 🎯 Dostępne modele Gemini (stan na 2025-10-19)

**Zalecane do użycia:**
- ✅ **`gemini-2.5-flash`** ← Używamy tego (szybki, stabilny, ekonomiczny)
- ✅ `gemini-2.5-pro` (wolniejszy, droż human, wyższa jakość)
- ✅ `gemini-2.0-flash` (alternatywa)

**NIE używać (przestarzałe):**
- ❌ `gemini-1.5-flash` (404 - nie istnieje dla v1beta)
- ❌ `gemini-pro` (404 - nie istnieje dla v1beta)

## 🚀 Jak przetestować

```powershell
# 1. Test bezpośredni funkcji AI
python test_ai_evaluation.py

# 2. Test trybu w konfiguracji
python test_evaluation_mode.py

# 3. Lista dostępnych modeli
python list_gemini_models.py

# 4. Zmiana trybu na AI
python set_ai_mode.py

# 5. Restart aplikacji
streamlit run main.py
```

## ✅ Oczekiwany wynik

Po wszystkich poprawkach, nowy kontrakt będzie oceniany tak:

```json
{
  "method": "ai",  ← AI zamiast heuristic!
  "model": "gemini-2.5-flash",
  "total_score": 85,
  "rating": 4,
  "strengths": [
    "Świetna analiza problemu",
    "Konkretne przykłady"
  ],
  "improvements": [
    "Można dodać harmonogram",
    "Rozwinąć część o komunikacji"
  ],
  "provider": "google_gemini",
  "timestamp": "2025-10-19 01:45:00"
}
```

## 📝 Checklist napraw

- [x] Zmieniono DEFAULT_EVALUATION_MODE na "ai"
- [x] Zmieniono model z gemini-1.5-flash na gemini-2.5-flash
- [x] Poprawiono pole contract["poziom_trudnosci"] → contract.get("trudnosc", 3)
- [x] Dodano safety_settings do GenerativeModel
- [x] Dodano retry logic dla zablokowanych odpowiedzi
- [x] Utworzono skrypty testowe
- [x] Zaktualizowano dokumentację

## 💡 Lekcje na przyszłość

1. **Zawsze weryfikuj nazwy pól** - `poziom_trudnosci` vs `trudnosc`
2. **Sprawdzaj dostępne modele** - Google często zmienia nazwy/wersje
3. **Safety settings** - dla treści edukacyjnych mogą być zbyt restrykcyjne
4. **Try-except nie wystarczy** - trzeba logować błędy aby je zobaczyć
5. **Testuj bezpośrednio** - nie tylko przez UI, ale też przez skrypty

---

**Data naprawy:** 2025-10-19  
**Status:** ✅ Naprawione (czeka na weryfikację w aplikacji)  
**Pliki zmienione:** 3  
**Skrypty testowe utworzone:** 4  
**Autor:** GitHub Copilot
