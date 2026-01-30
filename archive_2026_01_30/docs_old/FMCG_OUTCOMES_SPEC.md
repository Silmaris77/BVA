# FMCG Simulator - Specyfikacja Efektów i Wyników

**Dokument techniczny:** Pełna matryca wyników rozmów handlowych i realizacji zadań  
**Wersja:** 1.0  
**Data:** 2025-01-XX  
**Cel:** Sformalizować wszystkie możliwe efekty interakcji przed implementacją

---

## SPIS TREŚCI

1. [Matryca Wyników Rozmów Handlowych](#1-matryca-wyników-rozmów-handlowych)
2. [Matryca Efektów Realizacji Zadań](#2-matryca-efektów-realizacji-zadań)
3. [Interakcje: Narzędzia Trade Marketing × Wyniki](#3-interakcje-narzędzia-trade-marketing--wyniki)
4. [Edge Cases i Sytuacje Specjalne](#4-edge-cases-i-sytuacje-specjalne)
5. [Parametry Techniczne](#5-parametry-techniczne)

---

## 1. MATRYCA WYNIKÓW ROZMÓW HANDLOWYCH

### A. PROSPECT (Cold Call / Pierwsza Wizyta)

**CEL:** Przekonać klienta do podpisania pierwszego kontraktu

#### **Ocena AI × Wynik Rozmowy**

| Ocena AI | Wynik | Status Change | Reputation | PLN/miesiąc | Zadania | Timeline Event | Notatki |
|----------|-------|---------------|------------|-------------|---------|----------------|---------|
| **5⭐** | ✅ **KONTRAKT PODPISANY** | PROSPECT → ACTIVE | Start: 50 | +500-2k (zależy od typu) | Auto: "Wizyta regularna za 7 dni" | "✅ Kontrakt podpisany - [produkty]" | Gracz wybiera produkty z portfolio przed rozmową |
| **4⭐** | 🤔 **ZAINTERESOWANY** | PROSPECT (visits_count +1) | - | - | Sugestia: "Druga wizyta za 3-5 dni" | "🤔 Klient zainteresowany - wymaga drugiej wizyty" | Klient chce pomyśleć / zobaczyć ofertę na piśmie |
| **3⭐** | 🤔 **WĄTPLIWOŚCI** | PROSPECT (visits_count +1) | - | - | Sugestia: "Przygotuj lepszą ofertę, wróć za 7 dni" | "😐 Klient ma wątpliwości - [powód]" | AI podaje konkretny powód (cena? konkurencja? brak miejsca?) |
| **2⭐** | ⏸️ **NIE TERAZ** | PROSPECT (visits_count +1) | - | - | Blokada wizyty na 14 dni | "🚫 Klient niezainteresowany - spróbuj później" | Klient nie ma czasu / budżetu / zainteresowania |
| **1⭐** | ❌ **ODRZUCENIE** | PROSPECT (visits_count +1) | - | - | Jeśli visits_count ≥ 3 → USUŃ | "❌ Definitywna odmowa - [powód]" | Spalony kontakt (źle poprowadzona rozmowa, agresywna sprzedaż) |

#### **Mechaniki Dodatkowe (PROSPECT):**

**Multi-visit System:**
- `visits_count` śledzi liczbę prób
- Po **3 nieudanych wizytach** → Prospect znika z listy (nie marnować czasu)
- Każda wizyta wymaga **nowego podejścia** (AI pamięta poprzednie rozmowy)

**Interest Level (parametr Prospect):**
- Wysoki (80-100): 5⭐ = 90% szans na kontrakt, 4⭐ = 70%
- Średni (50-79): 5⭐ = 70% szans, 4⭐ = 40%
- Niski (20-49): 5⭐ = 50% szans, 4⭐ = 20%
- (AI używa tego w logice, gracz tego nie widzi bezpośrednio)

**Wpływ Narzędzi Trade Marketing:**
- **Gratis (2+1):** +20% szans na sukces w 2. wizycie (argument sprzedażowy)
- **Rabat:** +15% szans ale -10% marża (ryzykowne dla Prospect)
- **Materiały POS:** +10% szans (profesjonalny wygląd)

---

### B. ACTIVE (Check-in / Wizyta Kontrolna)

**CEL:** Utrzymanie relacji, kontrola ekspozycji, cross-sell, rozwiązywanie problemów

#### **Ocena AI × Wynik Rozmowy**

| Ocena AI | Wynik | Status Change | Reputation Change | PLN/miesiąc | Zadania Generowane | Timeline Event | Szczegóły Efektu |
|----------|-------|---------------|-------------------|-------------|-------------------|----------------|------------------|
| **5⭐** | ✅ **DOSKONAŁA WIZYTA** | ACTIVE | +10 | - | Losowo (30%): "🆕 Cross-sell opportunity" | "⭐⭐⭐⭐⭐ Wizyta - klient zachwycony" | Klient zadowolony, brak problemów. Market share +2% (lepsze relacje = lepsze miejsce na półce) |
| **4⭐** | ✅ **DOBRA WIZYTA** | ACTIVE | +5 | - | - | "⭐⭐⭐⭐ Wizyta - wszystko OK" | Standardowa wizyta, klient zadowolony. Brak zmian w market share |
| **3⭐** | 😐 **NEUTRALNA WIZYTA** | ACTIVE | +2 | - | Losowo (40%): "📦 Problem do rozwiązania" | "⭐⭐⭐ Wizyta - bez zmian" | Wizyta dla formalności. Klient obojętny. Ryzyko: jeśli będzie więcej takich → spadek rep |
| **2⭐** | ⚠️ **SŁABA WIZYTA** | ACTIVE | -5 | - | Losowo (60%): "🚨 Zadanie naprawcze (deadline: 7 dni)" | "⭐⭐ Wizyta - klient niezadowolony" | Klient narzeka (ekspozycja? dostawa? jakość?). Jeśli nie rozwiążesz problemu → dalszy spadek rep |
| **1⭐** | ❌ **KATASTROFA** | ACTIVE | -15 | - | Obowiązkowe: "🚨 PILNE: Naprawa relacji (deadline: 3 dni)" | "⭐ Wizyta - poważny problem!" | Klient bardzo zły (np. źle obsłużona reklamacja). Jeśli nie naprawisz w 3 dni → reputation -30 dodatkowe |

#### **Mechaniki Dodatkowe (ACTIVE):**

**Problem Detection (ocena ≤3⭐):**
- AI generuje konkretny problem:
  - **Ekspozycja:** "Produkty w magazynie, nie na półce" → Zadanie: kontrola ekspozycji
  - **Jakość:** "Ostatnia dostawa miała uszkodzenia" → Zadanie: rozmowa z magazynem + rekompensata
  - **Konkurencja:** "Palmolive oferuje lepsze warunki" → Zadanie: złóż lepszą ofertę (Trade Marketing)
  - **Sprzedaż:** "Twoje produkty się nie sprzedają" → Zadanie: promocja konsumencka

**Cross-sell Opportunity (ocena ≥4⭐):**
- AI wykrywa moment (30% szans przy 5⭐, 15% przy 4⭐):
  - Przykład: "Widzę, że FreshSoap sprzedaje się świetnie - może zainteresuje Cię FreshDish?"
  - Gracz może zaproponować nowy produkt
  - Ocena drugiej części rozmowy (pitch produktu):
    - **Sukces:** +1 produkt do portfolio, +15 rep, +200-500 PLN/m
    - **Odmowa:** Brak straty (ale nie można spamować - max 1 cross-sell na 14 dni)

**Visit Frequency Tracking:**
- Każdy ACTIVE klient ma `visit_frequency_required` (7/14/30 dni)
- Jeśli gracz **spóźnia się >7 dni** od last_visit:
  - **Automatyczna kara:** -5 rep (zaniedbanie)
  - **Timeline event:** "⏰ Brak wizyty - klient czuje się zaniedbany"
- Jeśli spóźnienie **>14 dni:**
  - **Kara:** -10 rep
  - **Ryzyko:** Jeśli reputation spadnie <-50 → LOST

**Market Share Dynamics:**
- Każda wizyta 5⭐ → **+2% market share** (lepsze relacje = lepsza ekspozycja)
- Każda wizyta 1-2⭐ → **-3% market share** (pogorszenie relacji = gorsze miejsce na półce)
- Market share wpływa na `monthly_value`:
  - Wzrost z 20% → 25% = +10% PLN/miesiąc
  - Spadek z 30% → 20% = -25% PLN/miesiąc

---

### C. LOST (Win-back / Odzyskiwanie Klienta)

**CEL:** Przeprosić, wyjaśnić zmiany, zaoferować coś ekstra, odbudować zaufanie

#### **Ocena AI × Wynik Rozmowy**

| Ocena AI | Wynik | Status Change | Reputation | PLN/miesiąc | Zadania | Timeline Event | Szczegóły |
|----------|-------|---------------|------------|-------------|---------|----------------|-----------|
| **5⭐** | ✅ **ODZYSKANY** | LOST → ACTIVE | Reset do 0 | Powrót do previous_monthly_value × 0.8 | Auto: "Wizyta kontrolna za 7 dni" | "🎉 Klient odzyskany - kontrakt wznowiony" | Klient daje drugą szansę. Produkty: tylko 80% poprzedniego portfolio (musi odbudować zaufanie) |
| **4⭐** | 🤔 **ROZWAŻA** | LOST (win_back_attempts +1) | - | - | Sugestia: "Druga próba za 14 dni" | "🤔 Klient rozważa powrót - wymaga czasu" | Klient widzi starania, ale potrzebuje czasu / lepszej oferty |
| **3⭐** | 😐 **SKEPTYCZNY** | LOST (win_back_attempts +1, difficulty +1) | - | - | Sugestia: "Przygotuj lepszą ofertę, wróć za 21 dni" | "😐 Klient skeptyczny - [konkretny powód]" | AI podaje co nie przekonało (oferta? zaufanie? konkurencja lepsza?) |
| **2⭐** | ⏸️ **NIE TERAZ** | LOST (win_back_attempts +1, difficulty +2) | - | - | Blokada na 30 dni | "🚫 Klient nie chce rozmawiać - spróbuj za miesiąc" | Zbyt świeża rana / już ma nowego dostawcę / nie wierzy w zmiany |
| **1⭐** | ❌ **SPALONY** | LOST (win_back_attempts +1, difficulty +3) | - | - | Jeśli attempts ≥3 → USUŃ (na zawsze) | "❌ Definitywna odmowa - koniec współpracy" | Źle poprowadzona rozmowa pogorszyła sytuację. Klient zamyka drzwi |

#### **Mechaniki Dodatkowe (LOST):**

**Win-back Difficulty System:**
```python
# Bazowa trudność zależna od lost_reason
base_difficulty = {
    "Zaniedbanie": 7.0,                    # Trudne (gracz zawiódł)
    "Koniec kontraktu - brak wznowienia": 5.0,  # Średnie (naturalne wygaśnięcie)
    "Konkurencja": 6.0,                    # Średnie-trudne (mają lepszą ofertę)
    "Reklamacja nierozwiązana": 8.5,       # Bardzo trudne (klient stracił zaufanie)
    "Reputation < -50": 9.0                # Ekstremalnie trudne (katastrofalna relacja)
}

# Modyfikatory
win_back_difficulty = base_difficulty
win_back_difficulty += (win_back_attempts × 2)  # Każda nieudana próba +2
win_back_difficulty -= (days_since_lost / 30)  # Czas goi rany (-1 co miesiąc)
win_back_difficulty += (current_competitor_months × 0.5)  # Jeśli ma nowego dostawcę

# Szansa powodzenia (przy ocenie 5⭐)
success_chance = max(10, 100 - (win_back_difficulty × 8))
# Przykład: difficulty 7.0 → 44% szans nawet przy 5⭐
```

**Required Offer (Trade Marketing):**
- Win-back **WYMAGA** użycia narzędzia Trade Marketing w ofercie:
  - **Gratis (2+1):** +25% szans na sukces (konkretna korzyść)
  - **Rabat 10%:** +20% szans (kompensata)
  - **Darmowa dostawa:** +15% szans (ułatwienie)
  - **Bez oferty ekstra:** -30% szans (dlaczego miałby wrócić?)
- **Koszt:** Narzędzia kosztują z budżetu (2k PLN/miesiąc) - strategiczna decyzja!

**Win-back Attempts Limit:**
- **Max 3 próby** na klienta LOST
- Po 3. nieudanej → klient **USUŃ** (never contact again)
- **Cooldown:** Minimum 7 dni między próbami (nie można spamować)

**Reputation Reset:**
- Jeśli odzyskany → **reputation = 0** (nie 50 jak nowy klient!)
- Powód: Zaufanie zostało nadszarpnięte, trzeba odbudować
- Pierwsze 3 wizyty **krytyczne** - muszą być 4-5⭐

---

## 2. MATRYCA EFEKTÓW REALIZACJI ZADAŃ

### A. ZADANIA REGULARNE (Auto-generowane Wizyty)

**Typ:** 📅 "Wizyta u [Klient]"  
**Deadline:** Zależny od `visit_frequency_required` (7/14/30 dni)  
**Priorytet:** 🔴 Pilne (jeśli overdue) / 🟡 Średnie (w terminie)

#### **Realizacja × Efekty**

| Status | Termin | Reputation | Market Share | Zadania Dodatkowe | Timeline Event | Notatki |
|--------|--------|------------|--------------|-------------------|----------------|---------|
| ✅ **W TERMINIE** | ≤ deadline | +5 | +1% | - | "📅 Wizyta regularna - relacja utrzymana" | Standardowa nagroda za profesjonalizm |
| ⏰ **SPÓŹNIONY (1-3 dni)** | deadline +1-3 | +2 | 0% | - | "⏰ Wizyta spóźniona - klient zauważył" | Zrealizowane ale bez bonusu |
| ⏰ **BARDZO SPÓŹNIONY (4-7 dni)** | deadline +4-7 | -5 | -2% | Auto: "🚨 Napraw relację" | "⚠️ Poważne spóźnienie - klient niezadowolony" | Kara za zaniedbanie |
| ❌ **POMINIĘTY (>7 dni)** | deadline +8+ | -10 | -5% | Auto: "🚨 PILNE: Win-back early stage" | "❌ Brak wizyty - relacja ucierpiała" | Jeśli reputation spadnie <-50 → LOST |

**Automatyczna Blokada:**
- Gracz **NIE MOŻE** pominąć wizyty regularnej
- Jeśli deadline minął → wizyta pozostaje w kalendarzu jako "OVERDUE" (czerwona)
- Każdy dzień opóźnienia → dodatkowa kara -1 rep/dzień
- **Strategia:** Lepiej zrobić kiepską wizytę (2⭐ = -5 rep) niż pominąć całkowicie (-10 rep)

---

### B. ZADANIA OPERACYJNE (Kontrola, Ekspozycja)

**Typ:** 📦 "Kontrola ekspozycji - [Klient]"  
**Deadline:** 3-7 dni  
**Priorytet:** 🟡 Średnie

#### **Realizacja × Efekty**

| Status | Wynik AI (1-5⭐) | Reputation | Market Share | PLN/miesiąc | Timeline Event | Szczegóły |
|--------|-----------------|------------|--------------|-------------|----------------|-----------|
| ✅ **WYKONANE (5⭐)** | Idealnie | +5 | +3% | +5% (przez 30 dni) | "✅ Ekspozycja poprawiona - produkty na prime shelf" | Produkty przeniesione na najlepsze miejsce. Wzrost sprzedaży |
| ✅ **WYKONANE (3-4⭐)** | OK | +3 | +1% | - | "✅ Ekspozycja poprawiona" | Produkty na półce, ale nie idealnie |
| ❌ **NIEWYKONANE** | - | -10 | -5% | -10% (przez 30 dni) | "❌ Ekspozycja zaniedbana - produkty w magazynie" | Klient sam musi zarządzać ekspozycją - zły wpływ na sprzedaż |

**Problem Discovery:**
- Przy wykonaniu zadania (ocena 5⭐) → 20% szans na **wykrycie nowego problemu**:
  - "Konkurencja ma promocję - nasze produkty giną"
  - "Brakuje shelf-talkers (materiały POS)"
  - "Klient wspomniał o zainteresowaniu nowym produktem"
- **Efekt:** Generuje nowe zadanie (szansa na dodatkowy rep/PLN)

---

### C. ZADANIA SPRZEDAŻOWE (Cross-sell, Up-sell)

**Typ:** 🆕 "Cross-sell: [Produkt] → [Klient]"  
**Deadline:** 7-14 dni  
**Priorytet:** 🟢 Niskie (opportunity, nie obowiązek)

#### **Realizacja × Efekty**

| Status | Wynik AI | Reputation | PLN/miesiąc | Produkty | Timeline Event | Szczegóły |
|--------|----------|------------|-------------|----------|----------------|-----------|
| ✅ **SUKCES (5⭐)** | Przekonał | +15 | +200-500 (zależy od produktu) | +1 produkt | "🎉 Cross-sell sukces - [Produkt] dodany" | Idealny pitch. Klient widzi wartość. Wzrost portfolio |
| 🤔 **ZAINTERESOWANIE (4⭐)** | Rozważa | +5 | - | - | "🤔 Klient rozważa [Produkt] - próbka wysłana" | Wymaga próbki/testu. Nowe zadanie za 14 dni: "Czy przyjął produkt?" |
| 😐 **ODMOWA (3⭐)** | Nie teraz | 0 | - | - | "😐 Cross-sell odrzucony - brak miejsca na półce" | Neutralna odmowa. Można spróbować innego produktu za 30 dni |
| ❌ **AGRESYWNA SPRZEDAŻ (1-2⭐)** | Zirytowany | -10 | - | - | "❌ Cross-sell nieudany - klient poczuł presję" | Źle poprowadzone. Klient czuje się napieralny. Kara |
| ⏸️ **POMINIĘTE** | - | 0 | - | - | - | Brak kary (to opportunity, nie obowiązek) |

**Cooldown System:**
- **Max 1 cross-sell na klienta na 14 dni** (nie spamować)
- Jeśli 2 kolejne cross-sell zakończone ≤3⭐ → **blokada cross-sell na 60 dni** (klient nie chce słyszeć o nowych produktach)
- **Strategia:** Wybieraj moment (reputation ≥60 = większa szansa sukcesu)

**Product Fit (szanse sukcesu):**
```python
# AI ocenia dopasowanie produktu do klienta
product_fit_score = 0
product_fit_score += (client_reputation / 100) × 30  # Lepsza relacja = lepsze szanse
product_fit_score += (client_budget / product_price) × 20  # Czy stać klienta?
product_fit_score += similar_products_success × 15  # Jeśli FreshSoap OK → FreshDish łatwiej
product_fit_score += (market_trends) × 10  # Czy produkt w trendzie?

# Przy 5⭐ rozmowie:
success_chance = max(20, min(95, product_fit_score))
```

---

### D. ZADANIA AWARYJNE (Reklamacje, Problemy)

**Typ:** 🚨 "ALERT: [Problem] - [Klient]"  
**Deadline:** NATYCHMIAST (1-3 dni)  
**Priorytet:** 🔴 PILNE

#### **Realizacja × Efekty**

| Status | Rozwiązanie AI | Reputation | PLN/miesiąc | Zadania Kaskadowe | Timeline Event | Szczegóły |
|--------|---------------|------------|-------------|------------------|----------------|-----------|
| ✅ **ROZWIĄZANE BŁYSKAWICZNIE (<24h, 5⭐)** | Doskonałe | +10 | - | - | "⚡ Problem rozwiązany natychmiast - klient pod wrażeniem" | Szybka reakcja buduje zaufanie. Bonus +10 rep (nie tylko uniknięcie kary) |
| ✅ **ROZWIĄZANE W TERMINIE (1-3 dni, 4-5⭐)** | Skutecznie | 0 | - | - | "✅ Problem rozwiązany - klient usatysfakcjonowany" | Uniknięcie kary -30 rep. Brak bonusu (oczekiwane) |
| ⚠️ **ROZWIĄZANE POŁOWICZNIE (3⭐)** | Kompromis | -10 | -5% | Auto: "📞 Follow-up za 7 dni" | "⚠️ Problem częściowo rozwiązany - wymaga monitoringu" | Klient niezadowolony ale daje czas. Musi być follow-up |
| ❌ **NIEROZWIĄZANE / ŹLE (1-2⭐)** | Porażka | -30 | -15% | Auto: "🚨 Naprawa relacji (3 dni)" | "❌ Problem nierozwiązany - klient wściekły" | Pogorszenie relacji. Jeśli nie naprawisz → LOST |
| ⏸️ **ZIGNOROWANE (>3 dni)** | - | -50 | -30% | Auto: LOST (reason: "Problem ignored") | "💀 Problem zignorowany - utrata klienta" | Automatyczny LOST. Win-back difficulty = 9.5 |

**Problem Types (różne wymagania):**

**Reklamacja jakości:**
- Wymaga: przeprosin + wymiany produktu + rekompensaty (Gratis lub Rabat)
- Jeśli rozwiązane dobrze → klient docenia profesjonalizm

**Opóźniona dostawa:**
- Wymaga: wyjaśnienia przyczyny + obietnica poprawy + darmowa dostawa następna
- AI sprawdza czy gracz nie obwinia magazynu / logistyki (to źle!)

**Konflikt osobisty:**
- Najtrudniejszy typ (difficulty +2)
- Wymaga: autentycznych przeprosin, wysłuchania, zaoferowania rozwiązania
- Jeśli gracz próbuje tylko "sprzedać" → automatycznie 1⭐

---

### E. ZADANIA STRATEGICZNE (Win-back)

**Typ:** 🔄 "Win-back: [Klient LOST]"  
**Deadline:** 14 dni (sugestia, można odłożyć)  
**Priorytet:** 🟡 Średnie (zależy od wartości klienta)

#### **Realizacja × Efekty**

| Status | Wynik | Reputation | PLN/miesiąc | Win-back Attempts | Timeline Event | Szczegóły |
|--------|-------|------------|-------------|------------------|----------------|-----------|
| ✅ **SUKCES (5⭐)** | LOST → ACTIVE | Reset do 0 | Powrót ×0.8 | Reset do 0 | "🎉 Klient odzyskany - świeży start" | Patrz sekcja 1.C (LOST Win-back) |
| 🤔 **PROGRESS (4⭐)** | LOST | - | - | +1, difficulty +1 | "🤔 Klient rozważa - daj mu czas" | Wymaga kolejnej wizyty (14-21 dni) |
| ❌ **PORAŻKA (≤3⭐)** | LOST | - | - | +1, difficulty +2-3 | "❌ Win-back nieudany - [powód]" | Jeśli attempts ≥3 → USUŃ |
| ⏸️ **POMINIĘTE** | LOST | - | - | - | - | Brak kary (gracz może zrezygnować z win-back) |

**Strategic Decision:**
- Win-back **kosztuje** (narzędzia Trade Marketing + czas wizyty = -20-30% energii)
- Gracz musi ocenić: **Czy warto?**
  - Klient 5k PLN/miesiąc → TAK (duża wartość)
  - Klient 500 PLN/miesiąc → NIE (lepiej szukać nowego Prospect)
- **ROI win-back:**
  ```
  Koszt: ~600 PLN (narzędzia) + 1-2 wizyty (czas)
  Zysk: monthly_value × 0.8 × 12 miesięcy (jeśli odzyskany)
  Break-even: monthly_value ≥ 1,000 PLN (inaczej nie opłaca się)
  ```

---

## 3. INTERAKCJE: NARZĘDZIA TRADE MARKETING × WYNIKI

### Wpływ Narzędzi na Szanse Sukcesu

**Budżet:** 2,000 PLN/miesiąc (Level 1)

| Narzędzie | Koszt | Najlepsze Użycie | Modyfikator Szans | Dodatkowe Efekty | Strategia |
|-----------|-------|------------------|------------------|------------------|-----------|
| **Rabat cenowy** | 0 PLN | PROSPECT (cold call), Win-back (rekompensata) | +15% szans | -10% marża (trwałe!) | Ryzykowne. Tylko jeśli MUSI być sukces |
| **Gratis (2+1)** | 350 PLN | Win-back (konkretna korzyść), PROSPECT (2. wizyta) | +20-25% szans | +8 rep (klient docenia) | Najbardziej uniwersalne. Szybki efekt |
| **Materiały POS** | 200 PLN | ACTIVE (kontrola ekspozycji), Cross-sell (wsparcie sprzedaży) | +10% szans, +15% sprzedaż (30 dni) | +5 rep | Najlepszy ROI długoterminowy. Buduje markę |
| **Promocja konsumencka** | 600 PLN | ACTIVE (słaba sprzedaż produktu), Cross-sell (nowy produkt) | +30% sprzedaż (14 dni) | +10 rep | Drogi ale efektowny. Jeśli klient skarży się na brak rotacji |
| **Darmowa dostawa** | 150 PLN | Win-back (ułatwienie), ACTIVE (nagłe zamówienie) | +15% szans | +3 rep | Tani "uprzejmość". Buduje goodwill |

### Przykładowe Scenariusze

#### **Scenariusz 1: Cold Call z Gratis**
```
Klient: Sklep ABC (Prospect, interest_level = 60)
Wizyta: Pierwsza (PROSPECT)
Ocena AI: 4⭐ (zainteresowany ale wątpliwości)

BEZ Gratis:
- Wynik: 🤔 ZAINTERESOWANY (wymaga 2. wizyty)
- Szansa na kontrakt w 2. wizycie: 40%

Z Gratis (2+1) - 350 PLN:
- Wynik: ✅ KONTRAKT PODPISANY (Gratis przekonał!)
- Szansa: 40% + 25% = 65% → Sukces
- Koszt: 350 PLN
- Zysk: +1,200 PLN/miesiąc × 12 = 14,400 PLN/rok
- ROI: 14,400 / 350 = 4,100% (świetna inwestycja!)
```

#### **Scenariusz 2: Win-back z Multiple Tools**
```
Klient: Kaufland Piaseczno (LOST, lost_reason = "Zaniedbanie", difficulty = 7.5)
Win-back Attempt: 1
Ocena AI: 5⭐ (doskonała rozmowa)

BEZ narzędzi:
- Szansa sukcesu: 100 - (7.5 × 8) - 30 = 10% (praktycznie niemożliwe)

Z Gratis (350 PLN) + Darmowa dostawa (150 PLN):
- Szansa: 10% + 25% + 15% = 50%
- Koszt: 500 PLN
- Zysk (jeśli sukces): 3,000 PLN/m × 0.8 × 12 = 28,800 PLN/rok
- Expected Value: 28,800 × 0.5 = 14,400 PLN (opłaca się!)

Z Gratis + Darmowa dostawa + Rabat 10%:
- Szansa: 10% + 25% + 15% + 15% = 65%
- Koszt: 500 PLN + (-10% marża na zawsze)
- Ryzyko: Rabat trwały = -3,600 PLN/rok
- Expected Value: (28,800 - 3,600) × 0.65 = 16,380 PLN (wciąż opłaca się, ale mniejszy zysk)
```

#### **Scenariusz 3: Cross-sell z POS**
```
Klient: Dino Konstancin (ACTIVE, reputation = 70, market_share = 25%)
Zadanie: Cross-sell FreshDish
Ocena AI: 4⭐ (zainteresowany, ale obawia się braku miejsca)

BEZ POS:
- Wynik: 🤔 ZAINTERESOWANIE (wymaga próbki, 50% szans w follow-up)
- Czas: 14 dni na follow-up

Z Materiały POS (200 PLN):
- Argument: "Mamy profesjonalne stojaki - nie zajmie Ci miejsca"
- Szansa sukcesu od razu: 50% + 10% = 60%
- Dodatkowy efekt: +15% sprzedaż FreshDish przez 30 dni (lepsze miejsce)
- ROI: Jeśli sukces → +400 PLN/m (FreshDish) + 15% boost = +460 PLN/m
  - 460 × 12 = 5,520 PLN/rok
  - 5,520 / 200 = 2,760% ROI
```

---

## 4. EDGE CASES I SYTUACJE SPECJALNE

### A. Co jeśli energia = 0 podczas wizyty?

**Problem:** Gracz zaczął wizytę z 25% energii, wizyta kosztuje 30%

**Rozwiązanie:**
- Wizyta **może się odbyć** (w końcu umówiona)
- Energia idzie w **minus** (np. -5%)
- **Kara jakości:**
  - Energia <0% → AI automatycznie obniża ocenę o 1⭐
  - Feedback: "Wyglądasz na zmęczonego - klient to zauważył"
- **Blokada:** Jeśli energia <-20% → gracz **nie może** rozpocząć nowej wizyty (musi zakończyć dzień)
- **Strategia:** Planuj wizyty! Energia = zasób

### B. Co jeśli klient ma reputation = -50 ale kontrakt jeszcze aktywny?

**Problem:** Reputation threshold dla LOST = -50, ale co się dzieje po przekroczeniu?

**Rozwiązanie:**
- Przy reputation **= -50** → **Trigger wydarzenia:**
  - 🚨 "OSTRZEŻENIE: Klient [X] rozważa zmianę dostawcy!"
  - Automatyczne zadanie: "Naprawa relacji (deadline: 7 dni)"
- Gracz ma **7 dni** na podniesienie reputation >-40 (wizyta 5⭐ + problem solving)
- **Jeśli nie naprawi w terminie:**
  - Status: ACTIVE → LOST
  - Reason: "Reputation < -50 przez >7 dni"
  - Win-back difficulty = 8.0 (bardzo trudne)
- **Jeśli naprawi:**
  - Reputation >-40 → zadanie zamknięte
  - Bonus: +5 rep (klient docenia wysiłek)

### C. Co jeśli gracz ma 2 zadania pilne tego samego dnia?

**Problem:** 🚨 Reklamacja (deadline: dziś) + 📅 Wizyta regularna overdue (deadline: dziś)

**Rozwiązanie:**
- Gracz **musi wybrać** (energia nie wystarczy na 2 wizyty)
- **Priorytetyzacja AI:**
  1. **Zadania awaryjne (🚨)** → wyższy priorytet (kara -50 rep za ignore)
  2. Wizyty regularne (📅) → można opóźnić o 1 dzień (kara -1 rep/dzień)
- **Feedback:**
  - "Masz 2 pilne zadania - wybierz mądrze!"
  - "Reklamacja: ignore = -50 rep, Wizyta regularna: +1 dzień = -1 rep"
- **Strategiczny wybór:** Zawsze priorytet dla awaryjnych (mniejsza strata)

### D. Co jeśli gracz używa tego samego narzędzia 3 razy z rzędu u tego samego klienta?

**Problem:** Gracz spamuje Gratis (2+1) co wizytę u Sklep ABC

**Rozwiązanie:**
- **Diminishing Returns:**
  - 1. użycie: +8 rep, pełen efekt
  - 2. użycie (w ciągu 30 dni): +4 rep, 50% efektu
  - 3. użycie (w ciągu 30 dni): +1 rep, 10% efektu
  - 4. użycie: 0 rep, AI feedback: "Klient przyzwyczaił się - to już nie działa"
- **Cooldown:** 30 dni między użyciami **tego samego narzędzia** u **tego samego klienta**
- **Strategia:** Rotuj narzędzia (Gratis → POS → Promocja) dla lepszego efektu

### E. Co jeśli cross-sell sukces, ale klient nie ma budżetu na dodatkowy produkt?

**Problem:** AI oceniło rozmowę 5⭐ (świetny pitch), ale klient logicznie nie stać

**Rozwiązanie:**
- AI sprawdza `client_budget` przed finalizacją
- **Jeśli przekroczony:**
  - Wynik: 🤔 "Klient chce, ale nie stać go teraz"
  - Timeline: "😊 Cross-sell odłożony - klient zainteresowany, czeka na budżet"
  - **Auto-zadanie za 90 dni:** "📅 Follow-up: Czy budżet się zwiększył?"
- **Jeśli w budżecie:**
  - Wynik: ✅ Sukces
  - `monthly_value` wzrasta
  - `client_budget` maleje o wartość nowego produktu

### F. Co jeśli gracz odzyskuje klienta LOST, a potem znowu go traci?

**Problem:** Win-back sukces → klient ACTIVE → po 2 miesiącach znowu LOST

**Rozwiązanie:**
- **2. utrata tego samego klienta:**
  - `win_back_difficulty` **nie resetuje się** całkowicie
  - Nowa difficulty = previous_difficulty × 0.5 + new_base_difficulty
  - Przykład: 1. win-back difficulty = 7.0, 2. utrata → difficulty = 7.0 × 0.5 + 7.0 = 10.5
- **Max attempts** również się kumuluje:
  - 1. win-back: 3 próby użyte, odzyskany
  - 2. win-back: tylko **2 próby** dostępne (3 - 1 pozostała z poprzedniego)
- **Feedback:** "Ten klient już raz wrócił i znowu odszedł - ostatnia szansa!"
- **Strategia:** Jeśli odzyskujesz klienta, **musisz** utrzymać reputation >40 (nie powtarzać błędów)

---

## 5. PARAMETRY TECHNICZNE

### A. Zmienne Stanu Klienta (JSON)

```json
{
  "client_id": "sklep_abc_piaseczno",
  "name": "Sklep ABC",
  "status": "ACTIVE",  // PROSPECT | ACTIVE | LOST
  
  // PROSPECT only
  "interest_level": 65,  // 0-100
  "visits_count": 0,     // Ile wizyt już było
  
  // ACTIVE only
  "reputation": 50,                    // -100 to +100
  "monthly_value": 1200,               // PLN
  "visit_frequency_required": 14,      // dni
  "last_visit_date": "2025-01-10",
  "products_portfolio": [...],
  "market_share": 25,                  // %
  "contract_renewal_date": "2025-07-01",
  
  // LOST only
  "lost_date": "2025-01-15",
  "lost_reason": "Zaniedbanie - brak wizyt przez 6 tygodni",
  "last_reputation": -20,
  "win_back_attempts": 0,              // 0-3
  "win_back_difficulty": 7.5,          // 0-10
  "win_back_cooldown_until": "2025-01-22",  // Nie można próbować przed tą datą
  
  // Timeline (wszystkie statusy)
  "timeline": [
    {
      "date": "2025-01-10",
      "type": "visit",              // visit | task | contract | event
      "event": "Wizyta regularna",
      "rating": 4.5,
      "reputation_change": +5,
      "details": "Check-in - wszystko OK"
    },
    {
      "date": "2025-01-15",
      "type": "task",
      "event": "Cross-sell FreshDish",
      "rating": 5.0,
      "reputation_change": +15,
      "pln_change": +400,
      "details": "Produkt dodany do portfolio"
    }
  ]
}
```

### B. Zmienne Stanu Zadania (JSON)

```json
{
  "task_id": "task_12345",
  "type": "regular_visit",  // regular_visit | operational | sales | emergency | win_back
  "client_id": "sklep_abc",
  "title": "Wizyta u Sklep ABC",
  "description": "Kontrola ekspozycji, check-in",
  "priority": "medium",     // low | medium | high | urgent
  "deadline": "2025-01-20",
  "created_date": "2025-01-13",
  "status": "pending",      // pending | in_progress | completed | failed | expired
  
  // Nagrody (jeśli completed)
  "rewards": {
    "reputation": 5,
    "pln_change": 0,
    "market_share": 1
  },
  
  // Kary (jeśli failed/expired)
  "penalties": {
    "reputation": -10,
    "pln_change": 0,
    "market_share": -2
  },
  
  // Metadata
  "energy_cost": 20,        // % energii
  "estimated_time": 30,     // minuty
  "can_skip": false,        // Czy można pominąć bez kary
  "cascades_on_fail": true  // Czy generuje zadanie naprawcze
}
```

### C. Trade Marketing Tool Usage Tracking

```json
{
  "user_id": "player_123",
  "trade_marketing_budget": 2000,  // PLN/month (resetuje co miesiąc)
  "trade_marketing_spent": 850,    // PLN (wydane w tym miesiącu)
  "trade_marketing_history": [
    {
      "date": "2025-01-10",
      "tool": "gratis_2plus1",
      "client_id": "sklep_abc",
      "cost": 350,
      "context": "PROSPECT cold call",
      "result": "success",  // Kontrakt podpisany
      "roi": 4100           // % (calculated post-hoc)
    },
    {
      "date": "2025-01-15",
      "tool": "pos_materials",
      "client_id": "dino_konstancin",
      "cost": 200,
      "context": "Cross-sell FreshDish",
      "result": "success",
      "roi": 2760
    }
  ],
  
  // Cooldowns (per client)
  "tool_cooldowns": {
    "sklep_abc": {
      "gratis_2plus1": "2025-02-10",  // Nie można użyć przed tą datą
      "rabat": null
    }
  }
}
```

### D. AI Conversation Context (Prompt Variables)

```python
# Przykład generowania kontekstu dla AI przy ACTIVE check-in
def generate_ai_context(client, task, player):
    context = f"""
Jesteś właścicielem: {client['name']} ({client['type']})

HISTORIA WSPÓŁPRACY:
- Dni współpracy: {(today - client['contract_date']).days}
- Ostatnia wizyta: {client['last_visit_date']} ({days_since_visit} dni temu)
- Reputacja sprzedawcy: {client['reputation']}/100 ({get_reputation_label(client['reputation'])})
- Produkty w portfolio: {len(client['products_portfolio'])} z 12 dostępnych
- Market share: {client['market_share']}%

OSTATNIE WYDARZENIA:
{client['timeline'][-3:]}  // Ostatnie 3 eventy

AKTUALNY PROBLEM (jeśli jest):
{task['description']}

TWOJA POSTAWA:
{generate_attitude(client['reputation'])}

CEL SPRZEDAWCY (gracz tego nie widzi):
{task['goal']}

ZASADY:
- Reaguj naturalnie
- Jeśli {client['reputation']} ≥70 → jesteś przyjaźnie nastawiony
- Jeśli {client['reputation']} <40 → jesteś krytyczny, wymagający
- Po rozmowie oceń 1-5⭐ i wyjaśnij dlaczego
"""
    return context
```

### E. Success Probability Formulas

```python
# PROSPECT - Szansa na podpisanie kontraktu
def calculate_contract_probability(client, conversation_rating, tools_used):
    base = client['interest_level'] / 100  # 0.0 - 1.0
    
    # Modyfikator z oceny rozmowy
    rating_mod = {
        5: 0.9,
        4: 0.7,
        3: 0.4,
        2: 0.2,
        1: 0.1
    }[conversation_rating]
    
    # Modyfikator z narzędzi
    tools_mod = 0
    if 'gratis_2plus1' in tools_used:
        tools_mod += 0.20
    if 'rabat' in tools_used:
        tools_mod += 0.15
    if 'pos_materials' in tools_used:
        tools_mod += 0.10
    
    probability = min(0.95, base * rating_mod + tools_mod)
    return probability


# ACTIVE - Cross-sell success probability
def calculate_crosssell_probability(client, product, conversation_rating, tools_used):
    base = 0.3  # Bazowo 30%
    
    # Reputacja (klient musi ufać)
    rep_mod = client['reputation'] / 200  # -100..+100 → -0.5..+0.5
    
    # Dopasowanie produktu
    fit_score = calculate_product_fit(client, product)  # 0.0 - 1.0
    
    # Ocena rozmowy (pitch)
    rating_mod = (conversation_rating - 3) * 0.1  # 5⭐ = +0.2, 3⭐ = 0, 1⭐ = -0.2
    
    # Narzędzia
    tools_mod = 0
    if 'pos_materials' in tools_used:
        tools_mod += 0.10
    if 'promocja_konsumencka' in tools_used:
        tools_mod += 0.15
    
    probability = max(0.05, min(0.95, base + rep_mod + fit_score * 0.3 + rating_mod + tools_mod))
    return probability


# LOST - Win-back success probability
def calculate_winback_probability(client, conversation_rating, tools_used):
    base = 1.0 - (client['win_back_difficulty'] / 10)  # difficulty 7.0 → base 0.3
    
    # Ocena rozmowy (kluczowa!)
    rating_mod = (conversation_rating - 3) * 0.15  # 5⭐ = +0.3, 1⭐ = -0.3
    
    # Narzędzia (obowiązkowe dla realnych szans)
    tools_mod = 0
    if 'gratis_2plus1' in tools_used:
        tools_mod += 0.25
    if 'rabat' in tools_used:
        tools_mod += 0.20
    if 'darmowa_dostawa' in tools_used:
        tools_mod += 0.15
    if not tools_used:  # Brak narzędzi = kara
        tools_mod = -0.30
    
    # Czas od utraty (czas goi rany)
    days_since_lost = (today - client['lost_date']).days
    time_mod = min(0.15, days_since_lost / 200)  # Max +0.15 po 200 dniach
    
    probability = max(0.05, min(0.85, base + rating_mod + tools_mod + time_mod))
    return probability
```

---

## PODSUMOWANIE - KLUCZOWE ZASADY

### 1. **Każda rozmowa MA EFEKT** (nie tylko liczba ⭐)
- PROSPECT: Kontrakt / Zainteresowanie / Odmowa / Spalenie
- ACTIVE: Rep + Market share + Problem detection + Cross-sell opportunity
- LOST: Odzyskanie / Progress / Porażka + difficulty increase

### 2. **Zadania mają KASKADOWE EFEKTY**
- Zadanie 2⭐ → generuje zadanie naprawcze
- Cross-sell 5⭐ → możliwość kolejnego za 30 dni (portfolio expansion)
- Problem zignorowany → LOST → Win-back → ...

### 3. **Narzędzia Trade Marketing = STRATEGICZNY ZASÓB**
- Budżet 2k PLN/miesiąc (ograniczony!)
- Każde narzędzie ma cooldown (nie spamować)
- Wybór: Gratis na Prospect (szybki efekt) vs POS na ACTIVE (długoterminowy ROI)

### 4. **Czas ma ZNACZENIE**
- Spóźnienie -1 rep/dzień
- Zadania awaryjne <24h = bonus, >3 dni = LOST
- Win-back po 90 dniach łatwiejszy niż po 7 dniach (klient zapomina)

### 5. **Reputacja = FUNDAMENT**
- <-50 = trigger LOST (7 dni na naprawę)
- <40 = email od szefa (ostrzeżenie)
- ≥60 = wymagane do awansu
- ≥70 = VIP prospects (word of mouth)

---

**GOTOWE DO IMPLEMENTACJI?**

Ten dokument zawiera **wszystkie możliwe wyniki** interakcji w grze.  
AI powinno używać tych formuł do symulacji.  
UI powinno pokazywać te efekty graczowi.  
Testing powinien weryfikować te prawdopodobieństwa.

Następny krok: **Slide deck dla klienta** prezentujący te mechaniki w przystępny sposób.
