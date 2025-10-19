# 🎮 Business Games - Dokumentacja Koncepcji

## 📋 Spis treści
1. [Przegląd](#przegląd)
2. [Podstawowa Mechanika](#podstawowa-mechanika)
3. [Poziomy Firmy](#poziomy-firmy)
4. [Kontrakty CIQ](#kontrakty-ciq)
5. [System Pracowników](#system-pracowników)
6. [System Rankingów](#system-rankingów)
7. [Progresja i Gamifikacja](#progresja-i-gamifikacja)
8. [Roadmap Implementacji](#roadmap-implementacji)

---

## 🎯 Przegląd

### Koncepcja
**Business Games** to symulacja rynkowa dla BrainVenture Academy, w której użytkownicy prowadzą firmę konsultingową specjalizującą się w **Conversational Intelligence (CIQ)**. Realizują kontrakty wykorzystując wiedzę z lekcji, zarządzają finansami i zespołem, oraz rywalizują w rankingach.

### Kluczowe Cele
- ✅ **Praktyczne zastosowanie wiedzy** z lekcji CIQ
- ✅ **Gamifikacja** procesu uczenia się
- ✅ **Motywacja** do regularnych powrotów
- ✅ **Społeczność** poprzez rankingi i konkurencję
- ✅ **Progresja** długoterminowa

### Główne Funkcje
1. 🏢 **Zarządzanie firmą konsultingową**
2. 💼 **Rynek kontraktów** (generowany dynamicznie)
3. 👥 **Zatrudnianie specjalistów** (z różnymi bonusami)
4. 🏆 **Rankingi** (Overall, Revenue, Quality, Productivity)
5. 📊 **Finanse** (przychody, koszty, zysk netto)

---

## 🎮 Podstawowa Mechanika

### Start
- Użytkownik rozpoczyna z **firmą poziomu 1** ("Solo Consultant")
- Startowy kapitał: **1,000 monet** 💰
- Reputacja: **0**
- Brak pracowników

### Pętla Rozgrywki

```
┌─────────────────────────────────────────────────┐
│  1. Odśwież pulę kontraktów (co 24h)            │
│       ↓                                          │
│  2. Wybierz i przyjmij kontrakt                 │
│       ↓                                          │
│  3. Napisz rozwiązanie (300-500+ słów)          │
│       ↓                                          │
│  4. Otrzymaj ocenę (1-5⭐) i wypłatę            │
│       ↓                                          │
│  5. Zarabiaj monety i reputację                 │
│       ↓                                          │
│  6. Awansuj poziom firmy                        │
│       ↓                                          │
│  7. Zatrudniaj pracowników                      │
│       ↓                                          │
│  8. Zwiększaj pojemność kontraktów              │
│       ↓                                          │
│  9. Wspinaj się w rankingach                    │
│       ↓                                          │
└─────────────────────────────────────────────────┘
```

### Limity i Ograniczenia
- **Max aktywnych kontraktów:** 3 jednocześnie
- **Dzienny limit:** 1 kontrakt + 1 za każdego pracownika (max 10/dzień)
- **Odświeżanie puli:** Co 24 godziny
- **Deadline kontraktów:** 1-3 dni (zależnie od trudności)

---

## 📈 Poziomy Firmy

### Poziom 1: Solo Consultant 👤
- **Zakres monet:** 0 - 2,000
- **Max pracowników:** 0
- **Limik kontraktów/dzień:** 1
- **Opis:** Jeden konsultant freelancer - zaczynasz swoją przygodę!

### Poziom 2: Boutique Consulting 🏢
- **Zakres monet:** 2,000 - 8,000
- **Max pracowników:** 2
- **Limit kontraktów/dzień:** 1 (+1 za pracownika)
- **Opis:** Mała firma z pierwszymi pracownikami. Czas na rozwój!

### Poziom 3: CIQ Advisory Group 🏛️
- **Zakres monet:** 8,000 - 25,000
- **Max pracowników:** 5
- **Limit kontraktów/dzień:** 1 (+1 za pracownika)
- **Opis:** Renomowana firma konsultingowa z solidnym portfolio

### Poziom 4: Global CIQ Partners 🌍
- **Zakres monet:** 25,000+
- **Max pracowników:** 10
- **Limit kontraktów/dzień:** 2 (+1 za pracownika)
- **Opis:** Międzynarodowa firma z prestiżową klientelą

---

## 💼 Kontrakty CIQ

### Kategorie Kontraktów

#### 1. ⚔️ Konflikt & Negocjacje
**Przykłady:**
- Mediacja w konflikcie zespołowym (450-750 monet)
- Negocjacje z trudnym stakeholderem (650-1,100 monet)

**Wymagana wiedza:**
- Conversational Intelligence
- Zarządzanie konfliktem
- Ladder of Inference
- Techniki negocjacyjne

#### 2. 🎯 Coaching & Feedback
**Przykłady:**
- Sesja coachingowa dla middle managera (550-900 monet)
- Executive coaching - transformacja lidera (1,200-2,000 monet)

**Wymagana wiedza:**
- Coaching conversations
- GROW Model
- COIN Framework
- Emotional Intelligence

#### 3. 🛡️ Kultura Zespołu
**Przykłady:**
- Audit kultury komunikacji w zespole (750-1,300 monet)
- Wdrożenie kultury feedbacku (800-1,350 monet)

**Wymagana wiedza:**
- Psychological Safety
- Team Dynamics
- Change Management

#### 4. 🚨 Kryzys & Trudne Rozmowy
**Przykłady:**
- Komunikacja po błędzie projektowym (950-1,600 monet)
- Zarządzanie zmianą - zwolnienia grupowe (1,500-2,500 monet)

**Wymagana wiedza:**
- Crisis Communication
- Stakeholder Management
- Difficult Conversations

#### 5. 🤝 Leadership & 1:1
**Przykłady:**
- Framework dla efektywnych 1:1 (500-850 monet)
- Skip-level meetings strategy (700-1,150 monet)

**Wymagana wiedza:**
- 1:1 Conversations
- Active Listening
- Leadership Development

### Struktura Kontraktu

```python
{
    "id": "CIQ-COACHING-001",
    "tytul": "Sesja coachingowa dla middle managera",
    "kategoria": "Coaching",
    "klient": "MarketPro",
    "emoji": "🎯",
    
    "opis": "Manager ma problemy z delegowaniem...",
    "zadanie": "Zaprojektuj sesję coachingową...",
    
    "wymagana_wiedza": ["Coaching", "GROW Model", "COIN"],
    "trudnosc": 2,  # 1-5 gwiazdek
    "czas_realizacji_dni": 1,
    "wymagany_poziom": 1,
    "min_slow": 350,  # minimalna liczba słów
    
    "nagroda_base": 550,
    "nagroda_4star": 720,
    "nagroda_5star": 900,
    "reputacja": 35
}
```

### System Oceny (MVP - uproszczony)

**W MVP:** Heurystyka oparta na:
- Długości rozwiązania (słowa)
- Obecności kluczowych słów
- Struktura (paragrafy, punkty)

**Przyszłość:** Ocena AI wykorzystująca:
- Completeness (25%) - czy wszystkie elementy obecne?
- Quality (30%) - jakość merytoryczna
- Practical (25%) - praktyczność rozwiązania
- CIQ Knowledge (20%) - wykorzystanie frameworks CIQ

### Nagrody

| Ocena | Przykład kontraktu (base: 550) | Bonus |
|-------|-------------------------------|-------|
| ⭐ | 550 monet | 0% |
| ⭐⭐ | 550 monet | 0% |
| ⭐⭐⭐ | 550 monet | 0% |
| ⭐⭐⭐⭐ | 720 monet | +31% |
| ⭐⭐⭐⭐⭐ | 900 monet | +64% |

**+ bonusy od pracowników specjalistów** (do +35%)

---

## 👥 System Pracowników

### Typy Pracowników

#### 1. Junior Consultant 👨‍💼
- **Koszt zatrudnienia:** 500 monet
- **Koszt dzienny:** 50 monet/dzień
- **Bonus:** +1 kontrakt/dzień
- **Wymagany poziom:** 1

#### 2. Conflict Resolution Specialist ⚔️
- **Koszt zatrudnienia:** 1,500 monet
- **Koszt dzienny:** 120 monet/dzień
- **Bonus:** +25% do zarobków w kategorii "Konflikt"
- **Wymagany poziom:** 2

#### 3. Executive Coach 🎯
- **Koszt zatrudnienia:** 2,000 monet
- **Koszt dzienny:** 150 monet/dzień
- **Bonus:** +30% do zarobków w kategorii "Coaching"
- **Wymagany poziom:** 2

#### 4. Culture Transformation Lead 🛡️
- **Koszt zatrudnienia:** 1,800 monet
- **Koszt dzienny:** 140 monet/dzień
- **Bonus:** +25% do zarobków w kategorii "Kultura"
- **Wymagany poziom:** 3

#### 5. Crisis Communication Expert 🚨
- **Koszt zatrudnienia:** 2,500 monet
- **Koszt dzienny:** 180 monet/dzień
- **Bonus:** +35% do zarobków w kategorii "Kryzys"
- **Wymagany poziom:** 3

#### 6. Operations Manager 📊
- **Koszt zatrudnienia:** 1,200 monet
- **Koszt dzienny:** 100 monet/dzień
- **Bonus:** -15% do kosztów wszystkich pracowników
- **Wymagany poziom:** 2

### Strategia Zatrudniania

**Early Game (Poziom 1-2):**
- Zatrudnij **Junior Consultant** aby zwiększyć pojemność

**Mid Game (Poziom 2-3):**
- Dodaj **specjalistów** w kategoriach, które preferujesz
- Rozważ **Operations Manager** jeśli masz 3+ pracowników

**Late Game (Poziom 4):**
- Zbuduj **zróżnicowany zespół** pokrywający wszystkie kategorie
- Maksymalizuj **synergię** między specjalistami

---

## 🏆 System Rankingów

### 1. Ranking Ogólny (Overall Score)

**Algorytm:**
```
Overall Score = 
  30% * Total Revenue +
  25% * (Avg Rating * 1000) +
  20% * Reputation +
  15% * (Firm Level * 5000) +
  10% * (Contracts Completed * 100)
```

**Powód:** Balansuje zarobki, jakość, reputację i aktywność

### 2. Ranking Przychodów (Revenue Leaders)
- Top 10 firm z największymi łącznymi przychodami
- Aktualizacja: Real-time po każdym kontrakcie

### 3. Ranking Jakości (Quality Masters)
- Top 10 firm z najwyższą średnią oceną
- **Minimum 20 kontraktów** aby wejść do rankingu
- Powód: Zapobiega "gaming" systemu

### 4. Ranking Produktywności (Most Active)
- Top 10 firm z największą liczbą kontraktów w ostatnich 30 dniach
- Reset: Co miesiąc
- Motywuje do ciągłej aktywności

### 5. Rankingi Specjalistów (Category Leaders)
- Osobny ranking dla każdej kategorii kontraktów
- Pozwala mniejszym firmom wyróżnić się w niszy

### 6. Ranking Wzrostu (Rising Stars)
- Top 10 firm z największym wzrostem w ostatnich 30 dniach
- Tylko firmy młodsze niż 90 dni
- Daje szansę nowym graczom

### 7. Ranking Perfekcjonistów (5-Star Club)
- Firmy z największą liczbą kontraktów ocenionych na 5⭐
- Nagroda za jakość pracy

### Odznaki Rankingowe

| Pozycja | Odznaka | Bonus |
|---------|---------|-------|
| #1 Overall | 👑 Emperor of CIQ | +10% do wszystkich zarobków |
| #2-3 Overall | 💎 Diamond Consultant | +7% do zarobków |
| #4-10 Overall | 🌟 Elite Consultant | +5% do zarobków |
| #1 Quality | 🏆 Quality Champion | Priorytet w prestiżowych kontraktach |
| #1 Productivity | ⚡ Speed Demon | -10% czasu realizacji |
| #1 Specialist | 🎯 Category Master | +20% w specjalizacji |

---

## 🎯 Progresja i Gamifikacja

### Pętla Progresji

```
Ukończ kontrakt
    ↓
Zarobek monet + reputacja
    ↓
Awans poziomu firmy
    ↓
Odblokowanie nowych pracowników
    ↓
Większa pojemność kontraktów
    ↓
Więcej zarobków
    ↓
Wyższe pozycje w rankingach
    ↓
Odznaki i bonusy
    ↓
LOOP
```

### Kamienie Milowe

| Osiągnięcie | Nagroda | Opis |
|-------------|---------|------|
| **Pierwszy Kontrakt** | 100 monet bonus | "Welcome to the business!" |
| **10 Kontraktów** | Badge "Hustler" | Solidny start |
| **50 Kontraktów** | Badge "Veteran" | Doświadczony konsultant |
| **100 Kontraktów** | Badge "Legend" | Ikona branży CIQ |
| **Pierwszy 5⭐** | Badge "Perfectionist" | Jakość się liczy |
| **10x 5⭐** | Badge "Excellence Master" | Mistrz jakości |
| **Milioner** | Badge "Tycoon" | 100,000 monet zarobione |
| **TOP 10 Overall** | Badge "Elite" | Najlepsi z najlepszych |
| **Poziom 4** | Badge "Empire Builder" | Globalna ekspansja |

### Losowe Wydarzenia (Przyszłość)

**Pozytywne:**
- 📈 "Boom gospodarczy" - +50% zarobków przez 3 dni
- 🎁 "Premiera rynkowa" - Darmowy pracownik na miesiąc
- ⭐ "Nagroda branżowa" - +500 reputacji

**Negatywne:**
- 📉 "Kryzys ekonomiczny" - Koszty pracowników +30% przez 2 dni
- 🏢 "Nowy konkurent" - Zmniejszona pula kontraktów
- 💸 "Podatek" - -10% z salda

**Neutralne:**
- 📰 "Artykuł o firmie" - Zwiększona widoczność w rankingach
- 🤝 "Networking event" - Odblokowuje 1 prestiżowy kontrakt

---

## 🚀 Roadmap Implementacji

### ✅ FAZA 1: MVP (COMPLETED)
**Czas: 3-4 dni**

Zrealizowane:
- ✅ Struktura danych (data/business_data.py)
- ✅ Core logic (utils/business_game.py)
- ✅ UI z 4 zakładkami (views/business_games.py)
- ✅ Integracja z main.py i navigation
- ✅ 10 kontraktów CIQ
- ✅ 6 typów pracowników
- ✅ 4 poziomy firmy
- ✅ Podstawowe finanse
- ✅ Testy jednostkowe

Zawiera:
- Dashboard firmy (monety, reputacja, kontrakty)
- Rynek kontraktów (7 dostępnych dziennie)
- Przyjmowanie i realizacja kontraktów
- Uproszczona ocena (heurystyka)
- Zatrudnianie/zwalnianie pracowników
- Podstawowe rankingi (mock data)
- Statystyki i wykresy

### 📋 FAZA 2: Rozbudowa (1-2 tygodnie)

#### 2.1 Ocena AI
- [ ] Integracja z OpenAI/Anthropic API
- [ ] Implementacja kryteriów oceny
- [ ] Detailed feedback dla użytkownika
- [ ] Przykłady i wskazówki poprawy

#### 2.2 Rankingi Live
- [ ] Globalne rankingi wszystkich użytkowników
- [ ] Aktualizacja pozycji co 1h
- [ ] Powiadomienia o zmianach
- [ ] Leaderboard UI z trendami

#### 2.3 Więcej Kontraktów
- [ ] 30+ kontraktów CIQ (po 6 w każdej kategorii)
- [ ] Różne poziomy trudności
- [ ] Projekty wieloetapowe (3-7 dni)
- [ ] Kontrakty sezonowe/tematyczne

#### 2.4 Wydarzenia Rynkowe
- [ ] System losowych wydarzeń
- [ ] Bonus events (boom, nagrody)
- [ ] Challenge events (kryzysy)
- [ ] Notyfikacje o wydarzeniach

### 📋 FAZA 3: Gamifikacja Advanced (2-3 tygodnie)

#### 3.1 Osiągnięcia i Odznaki
- [ ] 30+ achievement badges
- [ ] Tracking progressu
- [ ] Showcase w profilu
- [ ] Bonusy za odznaki

#### 3.2 Konkursy Miesięczne
- [ ] Monthly challenges
- [ ] Quarterly championships
- [ ] Special events
- [ ] Nagrody i trofea

#### 3.3 Portfolio
- [ ] Historia zrealizowanych projektów
- [ ] Oceny i feedback
- [ ] Showcase najlepszych prac
- [ ] Share na social media

#### 3.4 Timeline Rozwoju
- [ ] Wizualizacja progresji w czasie
- [ ] Milestone markers
- [ ] Porównanie now vs. then
- [ ] Export do PDF

### 📋 FAZA 4: Social & Competition (3-4 tygodnie)

#### 4.1 Head-to-Head Challenges
- [ ] Wyzwij innego gracza
- [ ] 1v1 competition
- [ ] Stakes i rewards
- [ ] Leaderboard dla challengers

#### 4.2 Guilds/Alliances
- [ ] Tworzenie gildii (3-10 firm)
- [ ] Wspólne kontrakty
- [ ] Ranking gildii
- [ ] Bonusy dla członków

#### 4.3 Aukcje Kontraktów
- [ ] Prestiżowe kontrakty na aukcji
- [ ] Bidding system
- [ ] Wygrany bierze wszystko
- [ ] Limited time offers

#### 4.4 Mentorship
- [ ] System mentoringu
- [ ] Doświadczeni pomagają nowym
- [ ] Rewards za mentoring
- [ ] Growth tracking

### 📋 FAZA 5: Ekspansja Tematyczna (Przyszłość)

#### 5.1 Nowe Lekcje = Nowe Kontrakty
- [ ] Design Thinking contracts
- [ ] Six Thinking Hats contracts
- [ ] Leadership contracts
- [ ] Innovation contracts

#### 5.2 Multi-domain Firm
- [ ] Rozszerzenie poza CIQ
- [ ] Nowe specjalizacje
- [ ] Cross-domain projects
- [ ] Strategia rozwoju firmy

---

## 📊 Metryki Sukcesu

### KPI - Krótkoterminowe (MVP)
- **Adoption Rate:** % użytkowników, którzy założyli firmę
- **Contract Completion:** Średnia liczba ukończonych kontraktów/użytkownika
- **Daily Active Users:** Użytkownicy aktywni w Business Games dziennie
- **Session Time:** Średni czas spędzony w zakładce

### KPI - Długoterminowe
- **Retention:** % użytkowników wracających po 7/30 dniach
- **Engagement:** Średnia liczba kontraktów/tydzień
- **Quality:** Średnia ocena kontraktów w systemie
- **Competition:** % użytkowników śledzących rankingi

### Cele Biznesowe
- 📈 **Zwiększenie retencji** o 30% (regularne powroty dla kontraktów)
- 🎯 **Completion rate lekcji** +40% (wiedza potrzebna do kontraktów)
- 💎 **Premium conversion** (w przyszłości: advanced features)
- 🌟 **User satisfaction** 4.5+/5.0

---

## 🎨 UI/UX Highlights

### Dashboard Firmy
- Gradient header z nazwą i poziomem
- Metryki finansowe (4 kolumny)
- Aktywne kontrakty (karty z deadline)
- Statystyki (rozkład kategorii)
- Wykres przychodów (ostatnie 7 dni)

### Rynek Kontraktów
- Filtry (kategoria, trudność, sortowanie)
- Karty kontraktów (border #667eea)
- Podgląd szczegółów (expander)
- Przyciski akcji (przyjmij/zobacz)
- Timer do odświeżenia puli

### Pracownicy
- Lista zatrudnionych (z opcją zwolnienia)
- Lista dostępnych (z wymaganiami)
- Ikony i emotikony dla typów
- Koszty dzienne/miesięczne highlighted

### Rankingi
- Highlight pozycji użytkownika (gradient)
- TOP 10 tabela
- Metryki i trendy (⬆️⬇️)
- Filtry czasowe (7d, 30d, all-time)

---

## 🔧 Techniczne

### Stack
- **Backend:** Python 3.x
- **Frontend:** Streamlit
- **Data:** JSON (users_data.json)
- **Charts:** Plotly
- **AI (future):** OpenAI/Anthropic API

### Pliki Kluczowe
```
data/
  └── business_data.py          # Kontrakty, pracownicy, config
utils/
  └── business_game.py          # Core logic (650+ linii)
views/
  └── business_games.py         # UI (650+ linii)
tests/
  └── test_business_games.py    # Test suite
docs/
  └── BUSINESS_GAMES_CONCEPT.md # Ten dokument
```

### Struktura Danych Użytkownika

```json
{
  "business_game": {
    "firm": {
      "name": "CIQ Masters",
      "founded": "2025-10-18",
      "level": 2,
      "coins": 4350,
      "reputation": 450
    },
    "employees": [
      {"type": "junior", "hired_date": "2025-10-18", "id": "EMP-001"}
    ],
    "contracts": {
      "active": [...],
      "completed": [...],
      "available_pool": [...]
    },
    "stats": {
      "total_revenue": 18450,
      "total_costs": 3600,
      "contracts_completed": 23,
      "avg_rating": 4.2,
      "category_stats": {...}
    },
    "ranking": {
      "overall_score": 8542.5,
      "current_positions": {...}
    }
  }
}
```

---

## 🎉 Podsumowanie

**Business Games** to kompleksowy system gamifikacji, który:
- ✅ Łączy naukę z praktyką
- ✅ Motywuje do regularnych powrotów
- ✅ Buduje społeczność (rankingi)
- ✅ Daje poczucie progresji
- ✅ Jest skalowalne (nowe lekcje = nowe kontrakty)

**MVP jest gotowy!** 🚀
Możesz teraz uruchomić aplikację i przetestować pełną funkcjonalność.

```bash
streamlit run main.py
```

Przejdź do zakładki **🎮 Business Games** i zacznij budować swoją firmę konsultingową CIQ!

---

*Dokument stworzony: 18 października 2025*  
*Status: MVP Completed ✅*  
*Next Steps: Phase 2 - AI Evaluation & Live Rankings*
