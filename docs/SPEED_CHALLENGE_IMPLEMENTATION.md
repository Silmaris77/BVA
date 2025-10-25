# 🚀 Speed Challenge - Nowy Typ Kontraktu

## ✅ Zaimplementowano

### 1. **Engine** (`utils/speed_challenge_engine.py`)
- ⏱️ **Real-time countdown timer** - odliczanie z kolorowaniem (zielony → żółty → czerwony)
- 💨 **Speed bonus system** - im szybciej, tym więcej punktów (do +50%)
- 🎯 **AI evaluation** - Gemini API ocenia jakość odpowiedzi
- 📊 **State management** - pełna obsługa session state
- 🔄 **Fallback mechanism** - jeśli AI nie działa, działa heurystyka

### 2. **Dane** (`data/business_data.py`)
Dodano 2 nowe kontrakty:

**A) `speed_urgent_call`** (90 sekund, medium pressure)
```
⚡ Urgent: Klient dzwoni - natychmiastowa porada!
Anna (CEO) dzwoni z paniki - zaraz pitch przed inwestorami!
Pytanie o CAC/LTV metryki - potrzebuje QUICK SMART ANSWER.
```

**B) `speed_crisis_decision`** (60 sekund, high pressure)
```
⚡ KRYZYS: Decyzja w 60 sekund!
Black Friday - checkout padł, tracimy 10k zł/minutę!
Restart vs przeładowanie? SZYBKA DECYZJA!
```

### 3. **UI Integration** (`views/business_games.py`)
- 🎨 **Renderowanie kontraktu** - `render_speed_challenge_contract()`
- 📱 **Responsive design** - pressure-based colors
- ⏰ **Live timer** - auto-refresh co 0.5s
- 📊 **Results view** - stars, points, feedback, speed bonus breakdown
- 🎁 **Reward calculation** - bonus za szybkość (do +30% reward)

---

## 🎮 Jak Działa

### Faza 1: **Start**
1. Gracz widzi kontekst (klient, urgency reason, problem)
2. Kliknięcie "🚀 START TIMER" → uruchamia countdown
3. Timer zaczyna odliczać z kolorowaniem

### Faza 2: **W Trakcie**
1. Timer odlicza w czasie rzeczywistym
2. Gracz wpisuje odpowiedź w text area
3. Kolory: 🟢 zielony (>50%) → 🟡 żółty (25-50%) → 🔴 czerwony (<25%)
4. Jeśli czas minie → pole blokuje się, "⏰ CZAS MINĄŁ!"

### Faza 3: **Evaluation**
1. Kliknięcie "📤 Wyślij odpowiedź"
2. AI (Gemini) ocenia:
   - ✅ **Clarity** - czy wyjaśnił problem w prostych słowach?
   - 🎯 **Actionable** - czy dał konkretną odpowiedź?
   - 😌 **Calm confidence** - czy uspokoił klienta?
   - 💼 **Business savvy** - czy rozumie metryki?
3. Zwraca: stars (1-5), points (0-100), feedback, strengths, improvements

### Faza 4: **Results**
1. Pokazuje:
   - ⭐ Ocena (1-5 gwiazdek)
   - 🎯 Punkty (z speed bonusem!)
   - ⏱️ Czas (zielony/czerwony)
   - 🏆 Status (SUCCESS/OK/TIMEOUT)
2. Feedback + strengths + improvements
3. Przyciski: "✅ Zamknij i kompletuj" lub "🔄 Spróbuj ponownie"

---

## 🎁 Reward System

### Base Reward
```python
nagroda_base = 400-600 DegenCoins (zależnie od kontraktu)
```

### Rating Multiplier
```
⭐ 1 = 0.5x
⭐⭐ 2 = 0.7x
⭐⭐⭐ 3 = 1.0x
⭐⭐⭐⭐ 4 = 1.3x
⭐⭐⭐⭐⭐ 5 = 1.6x
```

### Speed Bonus
```python
# Obliczany jako: time_taken / time_limit
# Im mniejszy ratio, tym większy bonus

Przykład (90s limit):
- Odpowiedź w 20s → ratio 0.22 → speed_bonus 0.78 (78%)
- Odpowiedź w 45s → ratio 0.50 → speed_bonus 0.50 (50%)
- Odpowiedź w 85s → ratio 0.94 → speed_bonus 0.06 (6%)

Final reward = base * rating_multiplier * (1 + speed_bonus * 0.3)
```

### Penalty za Timeout
```
- Jeśli przekroczono czas: -2 gwiazdki automatycznie
- Minimum 1 gwiazdka (nawet za timeout)
```

---

## 💡 Example Scenario

**Contract:** `speed_urgent_call` (90s limit, 400 base)

**Player performance:**
- Odpowiedział w 35 sekund ✅
- AI ocena: 4 gwiazdki, 85 punktów
- Speed ratio: 35/90 = 0.39 → bonus 0.61 (61%)

**Calculation:**
```
Base reward: 400 DC
Rating multiplier: 1.3x (4⭐)
Speed bonus: +61% * 0.3 = +18.3%

Final = 400 * 1.3 * 1.183 = 615 DC
```

**Plus:**
- Reputacja: 30 * 4/3 = 40 punktów
- Transaction logged
- Contract moved to completed

---

## 🎯 AI Evaluation Prompt

AI dostaje:
- **Sytuację** - pełny kontekst problemu
- **Odpowiedź gracza** - tekst wpisany przez gracza
- **Czas** - czy w limicie, ile zajęło
- **Kryteria** - evaluation_criteria z challenge_config
- **Ideal keywords** - słowa które powinny się pojawić

Zwraca JSON:
```json
{
  "stars": 4,
  "points": 85,
  "feedback": "Świetna zwięzłość...",
  "strengths": ["Konkretne", "Uspokajające"],
  "improvements": ["Więcej kontekstu"],
  "time_pressure_bonus": true
}
```

---

## 🔧 Technical Features

### Auto-Refresh Timer
```python
if not time_out:
    time.sleep(0.5)
    st.rerun()
```
Timer odświeża się co 0.5s dla smooth countdown.

### Lazy AI Import
```python
try:
    import google.generativeai as genai
    # Use Gemini
except:
    # Fallback to heuristic
```

### Session State Management
```python
st.session_state[f"speed_challenge_{contract_id}"] = {
    "started": False,
    "start_time": None,
    "completed": False,
    "evaluation_result": None,
    ...
}
```

---

## 🎮 Player Experience

### Visual Feedback
- 🎨 **Pressure colors** - low (green), medium (orange), high (red)
- ⏰ **Live countdown** - duży, wyraźny timer
- 📊 **Progress indicators** - visual cues
- 🎯 **Clear CTAs** - prominent buttons

### UX Flow
1. **Intrigue** - "Urgent call!" → ciekawość
2. **Preparation** - Czyta problem przed start
3. **Tension** - Timer odlicza, pressure rośnie
4. **Relief** - Wysłanie odpowiedzi
5. **Validation** - AI feedback + rewards

### Replayability
- "🔄 Spróbuj ponownie" - można retry dla lepszego wyniku
- Różne scenariusze - 2 kontrakty, można dodać więcej
- Randomizacja (TODO) - losowe sytuacje

---

## 📈 Future Improvements

### Możliwe rozszerzenia:
1. **Więcej scenariuszy**
   - Crisis management
   - Negotiation under pressure
   - Technical troubleshooting
   
2. **Difficulty levels**
   - Easy: 120s
   - Medium: 90s
   - Hard: 60s
   - Expert: 30s

3. **Multipliers**
   - Streak bonus (3x speed contracts in a row)
   - Perfect score achievements
   - Leaderboard dla fastest responses

4. **Audio effects**
   - Ticking clock sound
   - Alarm when <10s
   - Success chime

5. **Mobile optimization**
   - Thumb-friendly buttons
   - Larger text areas
   - Voice input option

---

## ✅ Testing Checklist

- [x] Engine funkcje (initialize, start, submit, evaluate)
- [x] Timer rendering (colors, countdown, timeout)
- [x] AI evaluation (Gemini API + fallback)
- [x] UI rendering (start → active → results)
- [x] Reward calculation (base * rating * speed)
- [x] Data persistence (save to user_data)
- [x] Error handling (AI failure, timeout, edge cases)
- [ ] **Manual testing** - uruchomić kontrakt end-to-end
- [ ] **Performance** - czy timer nie laguje
- [ ] **Mobile** - czy działa na telefonie

---

## 🚀 Ready to Test!

Wszystko zaimplementowane. Można teraz:
1. Uruchomić aplikację
2. Wejść w Business Games → Consulting
3. Znaleźć "⚡ Urgent: Klient dzwoni..."
4. Zaakceptować kontrakt
5. Przetestować Speed Challenge!

**IMPORTANT:** Wymaga `GOOGLE_API_KEY` w secrets/env dla AI evaluation.
