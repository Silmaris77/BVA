# 🌟 FMCG: Reputacja Ogólna Handlowca - Specyfikacja

**Data:** 28.10.2025  
**Feature:** Overall Reputation Score  
**Priorytet:** MUST HAVE (Core Progression Metric)

---

## 🎯 DLACZEGO TO DODAJEMY?

### **Problem:**
- Gracz ma reputację u każdego klienta (per customer), ale **brak globalnego wskaźnika jakości pracy**
- Nie ma motywacji do dbania o **wszystkich** klientów (może ignorować małych, skupiać się tylko na dużych)
- Brak kary za utratę klientów (LOST) - gracz może myśleć "trudno, znajdę innych"
- Awans do Level 2 bazuje tylko na PLN i liczbie kontraktów - można to osiągnąć przez agresywny hunting bez dbania o relacje

### **Rozwiązanie:**
**Reputacja ogólna handlowca** = Średnia ważona reputacji u wszystkich klientów (ACTIVE + LOST z karą)

---

## 📊 MECHANIKA

### **Wzór kalkulacji:**

```python
def calculate_overall_reputation(user_data):
    """
    Oblicza ogólną reputację handlowca
    """
    clients = user_data["business_games"]["fmcg"]["clients"]
    
    active_clients = [c for c in clients.values() if c["status"] == "ACTIVE"]
    lost_clients = [c for c in clients.values() if c["status"] == "LOST"]
    
    # ACTIVE: 80% wagi (ważone wartością miesięczną)
    if active_clients:
        active_weighted_sum = sum(
            c["reputation"] * c["monthly_value"] 
            for c in active_clients
        )
        active_total_value = sum(c["monthly_value"] for c in active_clients)
        active_avg = active_weighted_sum / active_total_value if active_total_value > 0 else 0
    else:
        active_avg = 0
    
    # LOST: 20% wagi (kara, równo ważone)
    if lost_clients:
        lost_avg = sum(c["last_reputation"] for c in lost_clients) / len(lost_clients)
    else:
        lost_avg = 0
    
    # Finalna reputacja
    overall = active_avg * 0.8 + lost_avg * 0.2
    
    return round(overall)
```

### **Wagi:**
- **ACTIVE:** 80% (ważone wartością miesięczną PLN)
  - Dlaczego? VIP klient (5k PLN) powinien mieć większy wpływ niż mały sklep (500 PLN)
  - Realny model: W prawdziwej sprzedaży ważniejsi klienci liczą się bardziej
- **LOST:** 20% (kara, równo ważone)
  - Dlaczego? Utrata klienta = red flag (nawet jeśli masz innych)
  - Kara motywuje do odzyskiwania (win-back)

### **Przykład kalkulacji:**

**Scenario A: Gracz ma 3 ACTIVE, 0 LOST**
```
ACTIVE:
- Sklep A: rep=70, 1,000 PLN → waga: 70 × 1,000 = 70,000
- Sklep B: rep=60, 500 PLN  → waga: 60 × 500 = 30,000
- Sklep C: rep=80, 1,500 PLN → waga: 80 × 1,500 = 120,000

Suma: 220,000 / 3,000 = 73.3
LOST: 0

OVERALL: 73.3 × 0.8 + 0 × 0.2 = 58.6 → 59/100
```

**Scenario B: Gracz ma 3 ACTIVE, 2 LOST**
```
ACTIVE (jak wyżej): 73.3

LOST:
- Sklep D: last_rep = -30
- Sklep E: last_rep = -20
Średnia: (-30 + -20) / 2 = -25

OVERALL: 73.3 × 0.8 + (-25) × 0.2 = 58.6 - 5 = 53.6 → 54/100
```

**Różnica:** -5 punktów za 2 utraconych klientów (motywacja do win-back!)

---

## 🎯 PROGI REPUTACJI OGÓLNEJ

| Reputacja | Tytuł | Badge | Efekty | Odblokowuje |
|-----------|-------|-------|--------|-------------|
| **90-100** | Sales Legend | 🏆 | +10% do zamówień<br>+500 PLN/m bonus | Osiągnięcie<br>VIP prospects |
| **75-89** | Top Performer | 🌟 | +5% do zamówień<br>Priorytet w support | Premium klienci |
| **60-74** | Solid Rep | ✅ | Standard | - |
| **40-59** | Average | 🟡 | Ostrzeżenie szefa | Wymaga poprawy |
| **20-39** | Struggling | ⚠️ | -10% nowe kontrakty | 30 dni na poprawę |
| **< 20** | At Risk | 🔴 | -20% kontrakty<br>Perspektywa zwolnienia | Mission critical |

---

## 🎮 WPŁYW NA GAMEPLAY

### **1. Nowi PROSPECT klienci**

**Mechanika:** Word of mouth - Twoja reputacja poprzedza Cię

```python
def apply_reputation_bonus_to_prospect(prospect, overall_rep):
    """
    Nowi klienci słyszeli o Tobie - wpływa na starting reputation
    """
    if overall_rep >= 75:
        # "Słyszałem dobre rzeczy o Panu!"
        prospect["initial_reputation"] = 10
        prospect["interest_level"] += 2
    elif overall_rep >= 60:
        # Standardowy start
        prospect["initial_reputation"] = 0
    else:
        # "Hmm, nie najlepsze opinie..."
        prospect["initial_reputation"] = -10
        prospect["interest_level"] -= 1
```

**UI (podczas pierwszej wizyty):**
```
┌─ WIZYTA: Sklep "ABC" ──────────────────────┐
│                                             │
│ AI: "Dzień dobry! Słyszałem o Panu dobre   │
│      rzeczy od mojego kolegi ze Sklepu XYZ.│
│      Co Pan ma do zaoferowania?"           │
│                                             │
│ [Bonus: +10 starting reputation] 🌟        │
└─────────────────────────────────────────────┘
```

### **2. Ocena szefa (koniec miesiąca)**

**Email od managera:**

**Jeśli rep ≥90:**
```
📧 EMAIL OD MANAGERA

Temat: Gratulacje! 🎉

Gratulacje! Twoja reputacja (92/100) jest wzorowa!
Klienci są zachwyceni współpracą z Tobą.

BONUS: +500 PLN do wypłaty
ODBLOKOWUJE: Dostęp do VIP prospectów (wartość 10k+/m)

Kontynuuj świetną robotę!
```

**Jeśli rep 60-89:**
```
📧 EMAIL OD MANAGERA

Temat: Miesięczny raport

Dobra robota w tym miesiącu! Twoja reputacja (68/100)
jest solidna. Klienci są zadowoleni.

Kontynuuj w ten sposób i awans jest w zasięgu ręki.
```

**Jeśli rep 40-59:**
```
📧 EMAIL OD MANAGERA

Temat: Ostrzeżenie - wymaga poprawy ⚠️

Widzimy, że Twoja reputacja spadła do 45/100.
To niepokojące. Kilku klientów narzeka na brak wizyt.

WYMAGANA POPRAWA: Podnieś reputację do min. 60/100
w ciągu 30 dni.

Skup się na relacjach z obecnymi klientami!
```

**Jeśli rep <40:**
```
📧 EMAIL OD MANAGERA

Temat: PILNE - Spotkanie dyscyplinarne 🚨

Twoja reputacja (35/100) jest alarmująco niska.
Masz 2 utraconych klientów w tym miesiącu.

ULTIMA RATIO: 30 dni na poprawę do min. 50/100
lub będziemy musieli przedyskutować Twoją przyszłość
w firmie.

MISJA:
- Odzyskaj minimum 1 LOST klienta
- Popraw reputację u min. 3 ACTIVE klientów do 60+

Spotkanie z HR: Piątek 14:00

[Rozumiem, działam!]
```

### **3. Awans do Level 2**

**Dodatkowy warunek:**

```python
def check_promotion_eligibility(user_data):
    """
    Sprawdza czy gracz może awansować
    """
    overall_rep = calculate_overall_reputation(user_data)
    
    requirements = {
        "sales": user_data["monthly_sales"] >= 10000,
        "contracts": len(active_clients) >= 10,
        "rating": user_data["avg_rating"] >= 4.0,
        "reputation": overall_rep >= 60  # NOWY WARUNEK!
    }
    
    if all(requirements.values()):
        return True, "Gratulacje! Awansujesz do Level 2!"
    elif not requirements["reputation"]:
        return False, f"Reputacja za niska ({overall_rep}/100). Potrzebujesz min. 60!"
    else:
        return False, "Nie spełniasz wszystkich wymagań."
```

**UI (Dashboard - Progres do awansu):**
```
┌─ AWANS DO LEVEL 2 ─────────────────────────┐
│                                             │
│ ✅ Sprzedaż: 12,500 / 10,000 PLN (125%)    │
│ ✅ Kontrakty: 11 / 10 (110%)               │
│ ✅ Ocena wizyt: 4.3 / 4.0 (108%)           │
│ ❌ Reputacja: 58 / 60 (97%) ⚠️             │
│                                             │
│ Status: BLISKO! Popraw reputację o 2 pkt.  │
│                                             │
│ 💡 Tip: Odwiedź klientów neutralnych (45)  │
│    i podnieś ich do 60+ → avg wzrośnie!    │
└─────────────────────────────────────────────┘
```

### **4. Wydarzenia specjalne**

**Przy reputation ≥90:**
```
🎉 WYDARZENIE: "Uznanie w firmie!"

Twoja legendarna reputacja (92/100) dotarła
do centrali! Prezes chce Cię poznać.

ODBLOKOWUJE:
• Dostęp do VIP prospectów (Carrefour, Auchan)
• Możliwość wystąpienia na konferencji sales
• Mentoring Junior Reps (dodatkowe PLN)

[Wow, super!]
```

**Przy reputation <40:**
```
🚨 WYDARZENIE: "Spotkanie z HR"

Twoja reputacja (35/100) wywołała alarm w centrali.
Musisz się stawić na spotkaniu z HR w piątek.

MISJA KRYTYCZNA (14 dni):
• Odzyskaj 1 LOST klienta
• Popraw 3 ACTIVE do rep ≥60

Inaczej... zwolnienie.

[Rozumiem, walczę o pracę!]
```

---

## 📈 UI COMPONENTS

### **Widget w Dashboard (główny):**

```
┌─ TWOJA REPUTACJA ──────────────────────────────┐
│ 🌟 Reputacja ogólna: 68/100 (Solid Rep ✅)    │
│ ████████████████░░░░                           │
│                                                 │
│ Szczegóły:                                     │
│ ✅ ACTIVE (8 klientów): Avg 72/100             │
│    • VIP (2): 85, 90 → 87.5 avg                │
│    • Zadowoleni (4): 60, 65, 70, 75 → 67.5     │
│    • Neutralni (2): 45, 50 → 47.5              │
│                                                 │
│ ❌ LOST (2 klientów): Avg -25/100              │
│    • Sklep D: -30 (zaniedbanie)                │
│    • Sklep E: -20 (konkurencja)                │
│                                                 │
│ 💡 Akcje do poprawy:                           │
│    1. Odwiedź Sklep F (rep=45) → podnieś do 60 │
│    2. Odzyskaj Sklep D (LOST) → usuń karę      │
│    3. Cross-sell u VIP → max reputacja         │
│                                                 │
│ Postęp do Level 2: ❌ Potrzebujesz 60+ (brakuje 8 pkt) │
│                                                 │
│ [📊 Zobacz pełną historię] [💡 Podpowiedzi]   │
└─────────────────────────────────────────────────┘
```

### **Timeline reputacji (wykres):**

```
┌─ HISTORIA REPUTACJI (4 tygodnie) ──────────────┐
│                                                 │
│ 100 |                                           │
│  90 |                                           │
│  80 |                                           │
│  70 |           ●━━━●━━━●                       │
│  60 |       ●━━━           ●                    │
│  50 |   ●━━━                 ●                  │
│  40 |                           ●               │
│     └─────────────────────────────              │
│      W1  W2  W3  W4  W5  W6                    │
│                                                 │
│ Kluczowe wydarzenia:                           │
│ • W1 (50): Start - 2 ACTIVE                    │
│ • W2 (60): +3 nowi klienci                     │
│ • W3 (70): Cross-sell u 2 VIP                  │
│ • W4 (70): Stabilny                            │
│ • W5 (55): UTRATA Sklep D 🔴                   │
│ • W6 (65): Odzyskanie + nowy VIP 🟢            │
│                                                 │
│ Trend: 📈 Wzrost +15 pkt w 6 tygodni           │
└─────────────────────────────────────────────────┘
```

### **Karta klienta (impact na overall):**

```
┌─ KLIENT: Sklep "ABC" ──────────────────────────┐
│ Reputacja u klienta: 45/100 (🟡 Neutralny)     │
│ Wartość miesięczna: 1,200 PLN                  │
│                                                 │
│ 💡 WPŁYW NA TWOJĄ REPUTACJĘ OGÓLNĄ:            │
│    Waga: 1,200 PLN × 45 = 54,000               │
│    Udział: 12% całkowitej wartości ACTIVE      │
│                                                 │
│    JEŚLI podniesiesz rep do 60:                │
│    → Twoja overall rep: 68 → 70 (+2 pkt!) ✅   │
│                                                 │
│    JEŚLI stracisz klienta (LOST):              │
│    → Twoja overall rep: 68 → 63 (-5 pkt!) 🔴   │
│                                                 │
│ [📞 Zaplanuj wizytę] [🎁 Użyj promocji]        │
└─────────────────────────────────────────────────┘
```

---

## 🧮 STRATEGICZNE DYLEMATY (Gameplay Depth)

### **Dylemat 1: Portfolio balancing**

**Scenario:**
- Masz 5 małych klientów (500 PLN każdy, rep=60) = 2,500 PLN total
- Dostałeś prospect VIP (5,000 PLN potencjał)

**Pytanie:** Czy ignorować małych i skupić się na VIP?

**Konsekwencje:**
- **TAK (focus VIP):**
  - ✅ Jeśli podpiszesz VIP (rep=70) → overall wzrośnie (większa waga)
  - ❌ Jeśli zaniedbasz małych → LOST (5× kara -20 = -100 w LOST avg)
  - ❌ Jeśli nie podpiszesz VIP → strata czasu
- **NIE (balans):**
  - ✅ Stabilny overall (5× 60 = bezpieczne)
  - ❌ Wolniejszy wzrost (małe wagi)

**Optymalne:** Pozyskaj VIP + utrzymuj małych (ale to wymaga czasu/energii!)

### **Dylemat 2: Win-back vs New hunting**

**Scenario:**
- Masz 2 LOST klientów (rep=-30, -20) → overall penalty: -10 pkt
- Masz 3 nowych prospectów (potencjał 0 rep → 50 po podpisaniu)

**Pytanie:** Czy odzyskiwać LOST czy szukać nowych?

**Konsekwencje:**
- **Win-back:**
  - ✅ Usunięcie kary (-30 → 0 = +30 impact)
  - ✅ Overall +6 pkt (20% wagi LOST)
  - ❌ Trudne (win-back difficulty 7/10)
  - ❌ Czasochłonne (2-3 wizyty)
- **New hunting:**
  - ✅ Łatwiejsze (cold call difficulty 3/10)
  - ✅ Szybsze (1 wizyta = kontrakt)
  - ❌ LOST pozostaje (kara -10 pkt nadal)

**Optymalne:** Win-back jeśli wartość klienta >2k PLN, inaczej new hunting

### **Dylemat 3: VIP retention vs volume growth**

**Scenario:**
- Masz 1 VIP (5k PLN, rep=90) → 50% wagi overall
- Masz 5 małych (1k każdy, rep=60) → 50% wagi

**Pytanie:** Na czym się skupić?

**Konsekwencje:**
- **Utrata VIP:**
  - 🔴 Overall: 75 → 60 (-15 pkt!) = KATASTROFA
  - 🔴 Wymaga 3 nowych klientów żeby zrekompensować
- **Utrata 1 małego:**
  - 🟡 Overall: 75 → 73 (-2 pkt) = do zniesienia

**Wnioski:**
- VIPy wymagają więcej uwagi (wizyt częściej)
- Jeden VIP > 5 małych (waga!)
- Ale dywersyfikacja = bezpieczeństwo (jeśli stracisz VIP)

---

## 📝 IMPLEMENTATION CHECKLIST

### **Backend (Python):**
- [ ] Funkcja `calculate_overall_reputation(user_data)`
- [ ] Funkcja `get_reputation_breakdown(user_data)` (szczegóły ACTIVE/LOST)
- [ ] Funkcja `calculate_reputation_impact(client_id, new_rep)` (symulacja "co jeśli")
- [ ] Auto-update overall rep po każdej zmianie client reputation
- [ ] Timeline historii (array z datami i wartościami)

### **UI (Streamlit):**
- [ ] Widget "Reputacja ogólna" w Dashboard
- [ ] Breakdown (lista ACTIVE/LOST z rep)
- [ ] Progress bar do Level 2 (4 metrics: PLN, contracts, rating, **reputation**)
- [ ] Wykres timeline (matplotlib/plotly)
- [ ] Karta klienta: "Wpływ na overall reputation"
- [ ] Tooltips/tips: "Podnieś Sklep X do 60 → overall +2 pkt"

### **Events/Email system:**
- [ ] Email przy rep ≥90 ("Gratulacje!")
- [ ] Email przy rep 60-89 ("Dobra robota")
- [ ] Email przy rep 40-59 ("Ostrzeżenie")
- [ ] Email przy rep <40 ("30 dni na poprawę")
- [ ] Event "Uznanie w firmie" (rep ≥90)
- [ ] Event "Spotkanie z HR" (rep <40)

### **Awans system:**
- [ ] Dodać warunek: `overall_reputation >= 60`
- [ ] UI: Show blocked reason ("Reputacja za niska: 58/60")
- [ ] Podpowiedzi: "Odwiedź klientów neutralnych → wzrost overall"

---

## 🎯 SUCCESS METRICS

**Jak zmierzymy sukces tej feature?**

1. **Engagement:**
   - % graczy sprawdzających widget reputacji >3x/tydzień
   - Czas spędzony na widoku breakdown (szczegóły ACTIVE/LOST)

2. **Behavior change:**
   - % graczy wykonujących win-back (przed: 10% → po: 40%?)
   - Średnia liczba LOST klientów (przed: 3-4 → po: 1-2?)

3. **Progression:**
   - % graczy zablokowanych na awansie przez reputation (<60)
   - Średnia reputation na Level 1 (target: 65-70)

4. **Strategic decisions:**
   - % graczy z portfolio balanced (mix małych + VIP)
   - vs % graczy all-in VIP hunting

---

## 💡 FUTURE ENHANCEMENTS (Post-MVP)

- [ ] **Porównanie z innymi graczami:** "Twoja rep: 68, Średnia: 55 (jesteś w top 20%!)"
- [ ] **Achievements:** "Legendary Rep" (90+ przez 3 miesiące), "Comeback Kid" (z 30 do 80 w 1 miesiącu)
- [ ] **Reputation decay:** Rep ≥80 wymaga utrzymania (regularne wizyty VIP), inaczej powolny spadek
- [ ] **Client referrals:** Jeśli rep ≥85 u klienta → może polecić Cię kolegom (nowi prospects z +10 starting rep)
- [ ] **Industry reputation:** Ogólna rep wpływa na cenę (hurtownia daje lepsze warunki jeśli słyszeli o Tobie)

---

**Autor:** AI Assistant  
**Status:** ✅ READY FOR IMPLEMENTATION
