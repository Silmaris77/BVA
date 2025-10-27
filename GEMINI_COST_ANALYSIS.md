# 💰 Analiza Kosztów Gemini API dla Aktywnego Gracza

## 📊 Modele Używane w Aplikacji

### 1. **Gemini 2.5 Flash** (główny model) ⭐
Użycie:
- Post-processing transkrypcji audio (dodawanie interpunkcji) - **GŁÓWNE UŻYCIE**
- Większość narzędzi AI (zastępuje 2.0 Flash)
- Najnowszy stabilny model Flash

### 2. **Gemini 2.0 Flash Experimental** (pomocniczy)
Użycie:
- AI Conversation Engine (rozmowy z NPC w kontraktach)
- FMCG rozmowy z klientami
- Speed Challenge
- Niektóre narzędzia AI

### 3. **Gemini 1.5 Flash** (legacy)
Użycie:
- Anti-cheat system
- Niektóre narzędzia (Communication Analyzer, itp.)

### 4. **Gemini 1.5 Pro** (premium)
Użycie:
- Business Game Evaluation (ocena kontraktów)
- Report Generator
- Niektóre zaawansowane narzędzia

---

## 💵 Cennik Gemini API (Październik 2025)

| Model | Input (1M tokens) | Output (1M tokens) | Status |
|-------|-------------------|-------------------|---------|
| **Gemini 2.5 Flash** | $0.075 | $0.30 | ⭐ Główny model |
| **Gemini 2.0 Flash Exp** | $0 (?) | $0 (?) | 🧪 Experimental (może być darmowy) |
| **Gemini 1.5 Flash** | $0.075 | $0.30 | Legacy |
| **Gemini 1.5 Pro** | $1.25 | $5.00 | Premium (oceny) |

**Uwaga:** Gemini 2.0 Flash Experimental może być DARMOWY w okresie testów!

---

## 🎮 Typowe Użycie - Aktywny Gracz (1 Sesja)

### Scenariusz: 2-godzinna sesja gry

#### **1. Kontrakty Conversation (rozmowy AI)**
- **Liczba kontraktów:** 2-3 kontrakty
- **Tury konwersacji:** 5-8 tur na kontrakt
- **Tokeny:**
  - Prompt systemowy: ~800 tokens input
  - Wypowiedź gracza: ~100 tokens input
  - Odpowiedź NPC: ~200 tokens output
  - **Total na turę:** ~900 input + 200 output
  - **Total na kontrakt (6 tur):** ~5,400 input + 1,200 output
  - **Total 3 kontrakty:** ~16,200 input + 3,600 output

**Koszt (Gemini 2.0 Flash Exp - DARMOWY w okresie testów):**
- Input: 16,200 × $0.00 / 1,000,000 = **$0.00**
- Output: 3,600 × $0.00 / 1,000,000 = **$0.00**
- **Subtotal: $0.00** (darmowe! 🎉)

#### **2. Kontrakty Standard (ocena AI)**
- **Liczba kontraktów:** 3-5 kontraktów
- **Tokeny:**
  - Prompt oceny: ~1,200 tokens input
  - Rozwiązanie gracza: ~500 tokens input
  - Ocena AI: ~300 tokens output
  - **Total na kontrakt:** ~1,700 input + 300 output
  - **Total 4 kontrakty:** ~6,800 input + 1,200 output

**Koszt (Gemini 1.5 Pro):**
- Input: 6,800 × $1.25 / 1,000,000 = **$0.0085**
- Output: 1,200 × $5.00 / 1,000,000 = **$0.006**
- **Subtotal: $0.0145** (~1.5 centa)

#### **3. Speech-to-Text Post-Processing (interpunkcja)**
- **Liczba nagrań:** 10-15 nagrań audio
- **Tokeny:**
  - Prompt + surowa transkrypcja: ~150 tokens input
  - Poprawiona transkrypcja: ~120 tokens output
  - **Total 12 nagrań:** ~1,800 input + 1,440 output

**Koszt (Gemini 2.5 Flash):**
- Input: 1,800 × $0.075 / 1,000,000 = **$0.000135**
- Output: 1,440 × $0.30 / 1,000,000 = **$0.000432**
- **Subtotal: $0.000567** (~0.06 centa)

#### **4. FMCG Rozmowy z Klientami**
- **Liczba spotkań:** 2-3 spotkania
- **Tury:** 6-10 tur na spotkanie
- **Tokeny:**
  - Podobne do Conversation contracts
  - **Total 2 spotkania × 8 tur:** ~12,800 input + 3,200 output

**Koszt (Gemini 2.0 Flash Exp - DARMOWY):**
- Input: 12,800 × $0.00 / 1,000,000 = **$0.00**
- Output: 3,200 × $0.00 / 1,000,000 = **$0.00**
- **Subtotal: $0.00** (darmowe! 🎉)

#### **5. Speed Challenge**
- **Liczba prób:** 1-2 próby
- **Tokeny:**
  - Prompt + odpowiedź: ~800 input + 200 output per try
  - **Total 2 próby:** ~1,600 input + 400 output

**Koszt (Gemini 2.0 Flash Exp - DARMOWY):**
- Input: 1,600 × $0.00 / 1,000,000 = **$0.00**
- Output: 400 × $0.00 / 1,000,000 = **$0.00**
- **Subtotal: $0.00** (darmowe! 🎉)

#### **6. Narzędzia AI (Communication Analyzer, itp.)**
- **Użycie:** Sporadyczne (1-2 razy w sesji)
- **Tokeny:** ~2,000 input + 500 output

**Koszt (Gemini 1.5 Flash):**
- Input: 2,000 × $0.075 / 1,000,000 = **$0.00015**
- Output: 500 × $0.30 / 1,000,000 = **$0.00015**
- **Subtotal: $0.0003** (~0.03 centa)

---

## 📈 PODSUMOWANIE - Koszt 1 Sesji (2h)

### Scenariusz 1: Gemini 2.0 Flash Exp DARMOWY (prawdopodobne)

| Funkcja | Model | Koszt |
|---------|-------|-------|
| Kontrakty Conversation (3) | Gemini 2.0 Flash Exp | $0.00 |
| Kontrakty Standard (4) | Gemini 1.5 Pro | $0.0145 |
| Speech-to-Text (12 nagrań) | Gemini 2.5 Flash | $0.000567 |
| FMCG Rozmowy (2) | Gemini 2.0 Flash Exp | $0.00 |
| Speed Challenge (2) | Gemini 2.0 Flash Exp | $0.00 |
| Narzędzia AI | Gemini 2.5 Flash | $0.0003 |
| **TOTAL** | | **$0.0154** |

### 💰 **Koszt 1 sesji: ~1.5 centa ($0.015)**

---

### Scenariusz 2: Gdyby 2.0 Flash Exp NIE BYŁ darmowy

| Funkcja | Model | Koszt (hipotetyczny) |
|---------|-------|-------|
| Kontrakty Conversation (3) | Gemini 2.5 Flash | $0.00585 |
| Kontrakty Standard (4) | Gemini 1.5 Pro | $0.0145 |
| Speech-to-Text (12 nagrań) | Gemini 2.5 Flash | $0.000567 |
| FMCG Rozmowy (2) | Gemini 2.5 Flash | $0.0039 |
| Speed Challenge (2) | Gemini 2.5 Flash | $0.00048 |
| Narzędzia AI | Gemini 2.5 Flash | $0.0003 |
| **TOTAL** | | **$0.0253** |

**Koszt: ~2.5 centa** (jeśli musiałbyś płacić za wszystko)

---

## 📊 Ekstrapolacja - Koszty Miesięczne

### Aktywny Gracz (15 sesji/miesiąc)
**Scenariusz z darmowym 2.0 Flash Exp:**
- **Koszt/sesja:** $0.015
- **Sesji/miesiąc:** 15
- **TOTAL:** **$0.23/miesiąc** (~0.90 PLN)

**Gdyby 2.0 Flash był płatny:**
- **TOTAL:** **$0.38/miesiąc** (~1.50 PLN)

### Bardzo Aktywny Gracz (30 sesji/miesiąc)
**Scenariusz z darmowym 2.0 Flash Exp:**
- **Koszt/sesja:** $0.015
- **Sesji/miesiąc:** 30
- **TOTAL:** **$0.45/miesiąc** (~1.80 PLN)

**Gdyby 2.0 Flash był płatny:**
- **TOTAL:** **$0.76/miesiąc** (~3.00 PLN)

---

## 🎓 Klasa 25 Uczniów - Miesiąc

### Scenariusz: 25 uczniów × 8 sesji/miesiąc

**Z darmowym Gemini 2.0 Flash Exp:**
- **Koszt/uczeń/sesja:** $0.015
- **Sesji/uczeń/miesiąc:** 8
- **Uczniów:** 25
- **TOTAL:** **$3.00/miesiąc** (~12 PLN)

**Za cały rok szkolny (9 miesięcy):** ~$27 (~108 PLN)

---

**Gdyby 2.0 Flash był płatny:**
- **TOTAL:** **$5.06/miesiąc** (~20 PLN)
- **Rok szkolny:** ~$45 (~180 PLN)

---

## 🚨 UWAGI

### 1. **Gemini 2.0 Flash Experimental = Najprawdopodobniej DARMOWY!**
Modele "experimental" w Google AI są zazwyczaj darmowe w okresie testów.
**Jeśli 2.0 Flash Exp jest darmowy → ~94% kosztów pochodzi TYLKO z oceny kontraktów (Pro)!**

Obecny koszt sesji: ~**$0.015** (1.5 centa)

### 2. **Największy Koszt: Gemini 1.5 Pro (94% kosztów)**
Ocena kontraktów standard = $0.0145 z $0.0154 total.
**Optymalizacja:** Zmiana Pro → Flash = oszczędność 97%!

### 3. **Gemini 2.5 Flash = Doskonały Wybór! ⭐**
- Taka sama cena jak 1.5 Flash ($0.075 / $0.30)
- Nowsza technologia
- Lepsza jakość odpowiedzi
- Używasz go do STT i narzędzi - świetnie!

### 4. **Speech-to-Text to tylko 3.7% kosztów**
Bardzo opłacalne dodanie tej funkcjonalności - praktycznie nic nie kosztuje.

### 5. **Porównanie z konkurencją:**
- **OpenAI GPT-4:** ~15x droższy
- **Claude:** ~8x droższy
- **Gemini Flash:** Najtańszy + najszybszy + (częściowo darmowy!)

---

## 💡 Rekomendacje Optymalizacji

### 🔥 **PRIORYTET 1: Gemini 1.5 Flash dla kontraktów standard**
Zmiana z Pro na Flash:
- **Obecny koszt:** $0.0145/kontrakt (94% całości!)
- **Nowy koszt z Flash:** $0.00043/kontrakt
- **Oszczędność:** 97% (!)

**Nowy koszt sesji:** $0.0014 zamiast $0.015 → **$0.0014/sesja (0.14 centa)** 🎉

**Z darmowym 2.0 Flash Exp + Flash dla ocen:**
- **Klasa/miesiąc:** $0.28 (~1.10 PLN) zamiast $3.00
- **To praktycznie ZA DARMO!** ✨

### 🎯 **PRIORYTET 2: Caching dla promptów systemowych**
Gemini API wspiera context caching - powtarzające się długie prompty są prawie darmowe.
- Może obniżyć koszty o dodatkowe 50%

### ⚡ **PRIORYTET 3: Batch processing**
Grupowanie ocen kontraktów → mniejsze koszty API.

### ⭐ **BONUS: Zostań przy Gemini 2.5 Flash!**
Już używasz najlepszego modelu Flash - świetny wybór! 
- Nowocześniejszy niż 1.5
- Ta sama cena
- Lepsza jakość

---

## 🎉 PODSUMOWANIE

### Obecne Koszty (z darmowym 2.0 Flash Exp):
- **Sesja (2h):** $0.015 (~6 groszy PLN)
- **Miesiąc (aktywny gracz, 15 sesji):** $0.23 (~0.90 PLN)
- **Klasa 25 uczniów/miesiąc (8 sesji):** $3.00 (~12 PLN)

### Po Optymalizacji (Flash zamiast Pro):
- **Sesja (2h):** $0.0014 (~0.5 grosza PLN) ⚡
- **Miesiąc (aktywny gracz):** $0.021 (~0.08 PLN)
- **Klasa 25 uczniów/miesiąc:** $0.42 (~1.70 PLN)

### 🚀 **Koszty PRAKTYCZNIE ZEROWE!**

---

### Gdyby 2.0 Flash Exp był płatny (mało prawdopodobne):
- **Sesja:** $0.025 (~10 groszy PLN)
- **Miesiąc (aktywny gracz):** $0.38 (~1.50 PLN)
- **Klasa/miesiąc:** $5.06 (~20 PLN)

Po optymalizacji (Flash dla ocen):
- **Sesja:** $0.006 (~2.5 grosza PLN)
- **Klasa/miesiąc:** $1.20 (~5 PLN)

---

## ✅ WNIOSKI

1. **Gemini 2.0 Flash Experimental prawdopodobnie DARMOWY** 🎁
2. **Gemini 2.5 Flash to świetny wybór** - już go używasz! ⭐
3. **Koszty są ŚMIESZNIE NISKIE** - grosze za sesję
4. **94% kosztów = ocena kontraktów (Pro)** → łatwo zoptymalizować
5. **Gemini API to najtańsza opcja na rynku** (15x taniej niż GPT-4)
6. **Speech-to-Text prawie nic nie kosztuje** (3.7% budżetu)
7. **Po optymalizacji: praktycznie ZA DARMO!** ✨

**REKOMENDACJA:** 
- ✅ Zostań przy Gemini 2.5 Flash (już używasz)
- ✅ Zmień ocenę kontraktów z Pro → 2.5 Flash
- ✅ Koszty spadną do ~$0.001/sesja
- ✅ Aplikacja będzie praktycznie darmowa w utrzymaniu! 🎯
