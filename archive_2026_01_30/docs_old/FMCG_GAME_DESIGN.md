# 🛒 FMCG Sales Game - Design Document

**Wersja:** 1.0 MVP  
**Data:** 28.10.2025  
**Status:** 🚧 W BUDOWIE - Poziom 1 (Junior Sales Representative)

---

## 🎯 WIZJA GRY

**Elevator Pitch:**  
"Zbuduj karierę w sprzedaży FMCG od Junior Sales Rep do Chief Sales Officer. Prowadź rozmowy handlowe z AI, zarządzaj swoim terytorium i rozwijaj bazę klientów. Awansuj przez 10 poziomów kariery, odblokowując nowe mechaniki: od wizyt w terenie przez zarządzanie zespołem po strategię biznesową."

**Core Loop (Level 1-3):**
```
PROSPECTING (Hunting) → Pierwsza wizyta → Kontrakt → 
FARMING (Obsługa) → Regularne wizyty → Zadania → Reputacja ↑ → 
Rozwój współpracy → Cross-sell → REPEAT

[Jeśli zaniedbasz] → Reputacja ↓ → LOST (Utracony klient) → Back to PROSPECTING
```

**3 Statusy Klienta:**
- 🔓 **PROSPECT** - Potencjalny klient (hunting)
- ✅ **ACTIVE** - Aktywny klient (farming) 
- ❌ **LOST** - Utracony klient (do odzyskania lub replaced)

---

## 📊 MVP SCOPE - POZIOM 1

### ✅ Co MUSI być w MVP:

#### 1. **ONBOARDING** ✅
- [x] Wprowadzenie do firmy FreshLife Poland
- [x] Przypisanie lokalizacji startowej (Piaseczno)
- [x] Tutorial podstaw (produkty, cele)

#### 2. **MAPA TERENU & PROSPECTING** 🚧
- [ ] Mapa Google/OpenStreetMap z pinezkami klientów
- [ ] 20-30 potencjalnych klientów w promieniu 30km od Piaseczna
- [ ] Typy klientów:
  - 🏪 Małe sklepy spożywcze (5-15km)
  - 🛒 Średnie dyskonty (10-25km)  
  - 🏬 Duże sieci lokalne (20-30km)
- [ ] Informacje o kliencie:
  - Nazwa, typ, lokalizacja
  - Dystans od bazy (Piaseczno)
  - Szacowany czas dojazdu (Google Maps API?)
  - Status: 🔓 Nieodwiedzony | ⏳ W trakcie | ✅ Aktywny | ❌ Stracony
  - Potencjał sprzedaży (LOW/MEDIUM/HIGH)

#### 3. **ZARZĄDZANIE CZASEM** 🚧
- [ ] **Kalendarz tygodniowy:**
  - Poniedziałek-Piątek: dni robocze
  - 8:00-17:00: dostępny czas pracy (9h)
  - Sobota opcjonalnie (sklepy otwarte!)
- [ ] **Budżet czasu:**
  - Wizyta u klienta: 30-60 min (zależnie od typu)
  - Dojazd: Google Maps API (realistyczne czasy)
  - Przygotowanie raportu: 15 min
  - Administracja: 30 min dziennie (fixed)
  - **MAX wizyt dziennie:** ~5-7 (realistycznie)
- [ ] **Planner wizyty:**
  - Drag & drop klientów na kalendarz
  - Automatyczne liczenie czasu (dojazd + wizyta)
  - Alert: "Przekroczono limit czasowy!"
  - Podgląd trasy na mapie
- [ ] **Auto-planowanie regularnych wizyt:**
  - Aktywni klienci wymagają wizyt co X dni
  - System podpowiada: "Klient ABC - brak wizyty od 14 dni!"
  - Auto-dodawanie do kalendarza (z potwierdzeniem)

#### 4. **SYSTEM KLIENTA - CYKL ŻYCIA** 🆕 KLUCZOWE!

##### **A. STATUSY KLIENTA:**

**🔓 PROSPECT (Potencjalny klient)**
- **Stan:** Nieodwiedzony lub w trakcie negocjacji
- **Zadania:**
  - 🎯 Pierwsza wizyta (cold call)
  - 📧 Follow-up po pierwszej wizycie
  - 💼 Prezentacja produktów
- **Cel:** Podpisać pierwszy kontrakt
- **Parametry:**
  - `interest_level`: 0-100% (rośnie podczas rozmów)
  - `first_contact_date`: Kiedy pierwszy raz odwiedzony
  - `visits_count`: Ile razy odwiedzony (max 3 przed decyzją)
  - `decision_deadline`: Data decyzji (2 tygodnie od pierwszej wizyty)

**✅ ACTIVE (Aktywny klient - FARMING)**
- **Stan:** Ma podpisany kontrakt
- **Zadania:**
  - 🔄 Regularne wizyty (co 7-14 dni)
  - 📦 Kontrola ekspozycji produktów
  - 🎁 Promocje sezonowe
  - 📊 Przegląd sprzedaży
  - 🆕 Cross-sell (nowe produkty)
- **Cel:** Utrzymać + rozwijać współpracę
- **Parametry:**
  - `reputation`: -100 do +100 (kluczowy wskaźnik!)
  - `last_visit_date`: Kiedy ostatnia wizyta
  - `visit_frequency_required`: Co ile dni trzeba odwiedzić (7/14/30)
  - `products_portfolio`: Lista produktów u klienta
  - `monthly_value`: Wartość miesięczna kontraktu
  - `market_share_vs_competition`: % naszych produktów vs konkurencja
  - `satisfaction_score`: 1-5⭐ (jak bardzo zadowolony)
  - `contract_renewal_date`: Kiedy kontrakt wygasa

**❌ LOST (Utracony klient)**
- **Stan:** Zerwał współpracę
- **Powody:**
  - Reputacja < -50 (zaniedbanie)
  - Nie odwiedzony > 30 dni
  - Konkurencja przejęła klienta
  - Niezadowolenie z produktów/cen
- **Zadania:**
  - 🔄 Win-back (odzyskanie klienta)
  - 📞 Telefon wyjaśniający
  - 🎁 Specjalna oferta
- **Cel:** Przekonać do powrotu (trudne!)
- **Parametry:**
  - `lost_date`: Kiedy utracony
  - `lost_reason`: Dlaczego (np. "no_visits", "competition", "price")
  - `win_back_attempts`: Ile prób odzyskania (max 2)
  - `win_back_difficulty`: ⭐⭐⭐ (3x trudniej niż prospect)

##### **B. SYSTEM REPUTACJI** 🌟

**Reputacja = Kluczowy wskaźnik relacji (-100 do +100)**

**DWA POZIOMY REPUTACJI:**

**1️⃣ Reputacja u klienta** (indywidualna dla każdego ACTIVE/LOST)
**2️⃣ Reputacja ogólna handlowca** 🆕 (średnia ważona wszystkich klientów)

---

#### **1️⃣ REPUTACJA U KLIENTA** (per customer)

**WZROST REPUTACJI (+):**
- ✅ Regularna wizyta w terminie: **+5 pkt**
- ⭐ Wizyta oceniona 5/5 przez AI: **+10 pkt**
- 📦 Wykonanie zadania dodatkowego: **+3-8 pkt**
- 🎁 Dostarczona promocja: **+5 pkt**
- 🆕 Sprzedaż nowego produktu (cross-sell): **+15 pkt**
- 📊 Przekroczenie planu sprzedaży: **+10 pkt**
- 🚚 Terminowa dostawa: **+2 pkt**

**SPADEK REPUTACJI (-):**
- ❌ Brak wizyty > 7 dni po terminie: **-5 pkt/dzień**
- ❌ Niewykonane zadanie: **-10 pkt**
- ❌ Wizyta oceniona 1-2/5: **-15 pkt**
- ❌ Opóźniona dostawa: **-8 pkt**
- ❌ Brak produktów w asortymencie: **-5 pkt**
- ❌ Konkurencja wprowadziła promocję (a my nie): **-10 pkt**
- ❌ Zignorowany email/telefon: **-3 pkt**

**PROGI REPUTACJI U KLIENTA:**

| Reputacja | Status | Opis | Efekty |
|-----------|--------|------|--------|
| **80-100** | 🌟 VIP | Perfekcyjna relacja | +20% do zamówień, polecanie innym |
| **50-79** | ✅ Zadowolony | Dobra współpraca | Stabilne zamówienia |
| **20-49** | 🟡 Neutralny | OK, ale można lepiej | Wymaga uwagi |
| **0-19** | ⚠️ Zagrożony | Niezadowolony | Ryzyko utraty (-5 pkt/tydzień) |
| **-1 do -49** | 🔴 Krytyczny | Bardzo niezadowolony | Ostatnia szansa! |
| **< -50** | ❌ LOST | Zerwana współpraca | Klient utracony |

---

#### **2️⃣ REPUTACJA OGÓLNA HANDLOWCA** 🆕 (Overall Reputation Score)

**Co to jest?**
Średnia ważona reputacji u wszystkich klientów (ACTIVE + LOST z karą).

**Jak obliczamy?**

```python
# Wzór:
reputation_overall = (
    sum(reputation_active * monthly_value) / sum(monthly_value_all_active) * 0.8 +
    sum(reputation_lost * recovery_penalty) / count_lost * 0.2
)

# Przykład:
ACTIVE klienci:
- Sklep A: rep=70, wartość=1,000 PLN → waga: 70 * 1,000 = 70,000
- Sklep B: rep=60, wartość=500 PLN  → waga: 60 * 500 = 30,000
- Sklep C: rep=80, wartość=1,500 PLN → waga: 80 * 1,500 = 120,000
Suma: (70,000 + 30,000 + 120,000) / (1,000 + 500 + 1,500) = 220,000 / 3,000 = 73.3

LOST klienci:
- Sklep D: rep=-30 (przy utracie) → kara: -30 * 0.5 = -15
Średnia LOST: -15

REPUTACJA OGÓLNA:
73.3 * 0.8 + (-15) * 0.2 = 58.6 - 3 = 55.6 → zaokrąglone: 56/100
```

**Wagi:**
- **ACTIVE klienci:** 80% (ważone wartością miesięczną)
- **LOST klienci:** 20% (kara, ważona równo)
- **PROSPECT:** Nie wlicza się (jeszcze nie mamy relacji)

**Dlaczego wartość miesięczna?**
- Klient za 5,000 PLN/miesiąc jest ważniejszy niż za 500 PLN
- Motywacja do dbania o dużych klientów
- Realny model (w prawdziwej sprzedaży VIPy mają większe znaczenie)

**Dlaczego LOST klienci obniżają?**
- Kara za utratę klienta (nawet jeśli masz innych)
- Motywacja do win-back (odzyskanie podnosi ogólną rep)
- Realny model (w CV "utraceni klienci" = red flag)

---

#### **PROGI REPUTACJI OGÓLNEJ** (Overall)

| Reputacja | Tytuł | Efekty | Odblokowuje |
|-----------|-------|--------|-------------|
| **90-100** | 🏆 **Sales Legend** | +10% do wszystkich zamówień, +500 PLN bonus/miesiąc | Osiągnięcie, Uznanie szefa |
| **75-89** | 🌟 **Top Performer** | +5% do zamówień, Priorytet w support | Dostęp do Premium klientów |
| **60-74** | ✅ **Solid Rep** | Standard, bez bonusów | - |
| **40-59** | 🟡 **Average** | Ostrzeżenie od szefa | Wymaga poprawy |
| **20-39** | ⚠️ **Struggling** | -10% do nowych kontraktów (klienci słyszeli o Tobie) | Warning: 30 dni na poprawę |
| **< 20** | 🔴 **At Risk** | -20% do kontraktów, Perspektywa zwolnienia | Mission: Odzyskaj 3 klientów |

---

#### **MECHANIKA W GRZE**

**UI - Dashboard (nowy widget):**
```
┌─ TWOJA REPUTACJA ──────────────────────────────┐
│ 🌟 Reputacja ogólna: 56/100 (Solid Rep)        │
│ ████████████░░░░░░░░                           │
│                                                 │
│ Szczegóły:                                     │
│ ✅ ACTIVE (8 klientów): Avg 68/100             │
│    • VIP (2): 85, 90                           │
│    • Zadowoleni (4): 60, 65, 70, 72            │
│    • Neutralni (2): 45, 50                     │
│                                                 │
│ ❌ LOST (2 klientów): Avg -25/100              │
│    • Sklep D: -30 (zaniedbanie)                │
│    • Sklep E: -20 (konkurencja)                │
│                                                 │
│ 💡 Tip: Odzyskaj LOST klientów → +10 rep!     │
│                                                 │
│ [📊 Zobacz pełną historię]                     │
└─────────────────────────────────────────────────┘
```

**Wpływ na gameplay:**

1. **Nowi PROSPECT klienci:**
   - Reputation ≥75: "Słyszałem o Panu dobre rzeczy!" (+10 starting rep)
   - Reputation 40-74: Standardowy start (0 rep)
   - Reputation <40: "Hmm, nie najlepsze opinie..." (-10 starting rep)

2. **Ocena szefa (koniec miesiąca):**
   - Reputation ≥90: "Jesteś wzorem dla innych!" (+500 PLN bonus)
   - Reputation 60-89: "Dobra robota, kontynuuj!"
   - Reputation 40-59: "Musisz poprawić relacje z klientami."
   - Reputation <40: "Alarmująco dużo utraconych klientów. 30 dni na poprawę!"

3. **Awans do Level 2:**
   - Dodatkowy warunek: **Reputation ≥60** (oprócz sprzedaży i kontraktów)
   - Nie można awansować z "Average" reputacją

4. **Wydarzenia specjalne:**
   ```
   🎉 WYDARZENIE: "Uznanie w firmie"
   
   Twoja reputacja (78/100) zwróciła uwagę managementu!
   Dostałeś dostęp do VIP prospectów (wartość 10k+/miesiąc).
   
   [✅ Super!]
   ```

5. **Email od szefa (jeśli rep <40):**
   ```
   ⚠️ EMAIL OD MANAGERA
   
   Temat: Pilna rozmowa o wynikach
   
   "Widzimy, że Twoja reputacja spadła do 35/100.
   To niepokojące - masz 2 utraconych klientów w tym miesiącu.
   
   MISJA: Odzyskaj minimum 1 klienta w ciągu 14 dni
   lub popraw reputację u obecnych klientów do 50+.
   
   W przeciwnym razie będziemy musieli przedyskutować
   Twoją przyszłość w firmie."
   
   [Rozumiem, działam!]
   ```

---

#### **STRATEGICZNE KONSEKWENCJE**

**Dilema gracza:**

❓ **Co robić z klientem Neutralnym (rep=45)?**
- **Opcja A:** Inwestuję czas (wizyty, promocje) → podnoszę do 60+ → lepszy avg
- **Opcja B:** Ignoruję, szukam nowych → ryzyko LOST → kara do avg
- **Opcja C:** Świadomie rezygnuję (za mały, nie opłaca się) → LOST, ale skupiam się na VIP

❓ **Czy odzyskiwać LOST klientów?**
- **TAK:** Odzyskany klient (z rep=0) lepszy niż LOST (rep=-30) → podnosi avg
- **NIE:** Trudne, czasochłonne, może się nie udać

❓ **Jak balansować portfolio?**
- **1 VIP (rep=90, 5k PLN)** vs **5 małych (rep=60, 1k każdy)**
- VIP ma większą wagę (5k) → większy wpływ na avg
- Ale jeśli stracisz VIP → ogromny spadek avg

---

#### **HISTORIA REPUTACJI OGÓLNEJ** (Timeline)

**Gracz może zobaczyć wykres:**
```
Reputacja w czasie (ostatnie 4 tygodnie):

100 |
 90 |
 80 |
 70 |     ●━━━●━━━━━●
 60 |   ●               ●
 50 | ●                   ●
 40 |
    └─────────────────────────
     W1  W2  W3  W4  W5  W6

Kluczowe wydarzenia:
• W1: Start (50/100)
• W2: +2 klienci ACTIVE (+10 rep → 60)
• W3-W4: Stabilny (60-70)
• W5: UTRATA Sklep D (-15 rep → 55)
• W6: Odzyskanie Sklep D (+20 rep → 75)
```

##### **C. ZADANIA ZWIĄZANE Z KLIENTEM** 📋

**TYPY ZADAŃ:**

**1. Wizyty Regularne (Auto-generowane)**
```
📅 "Wizyta u Sklep ABC"
Priorytet: 🔴 Pilne (ostatnia wizyta: 10 dni temu, max: 7)
Czas: 30 min
Cel: Utrzymanie relacji, kontrola ekspozycji
Nagroda: +5 reputacji
```

**2. Zadania Operacyjne (Generowane przez system)**
```
📦 "Kontrola ekspozycji - Dino Konstancin"
Deadline: 3 dni
Opis: "Sprawdź czy produkty są na półkach, nie w magazynie"
Nagroda: +5 reputacji, +2% market share
```

**3. Zadania Sprzedażowe (Możliwości)**
```
🆕 "Cross-sell: Zaproponuj nowy produkt 'FreshMilk'"
Deadline: 7 dni
Opis: "Klient ma już 3 produkty. Idealny moment na 4-ty!"
Nagroda: +15 reputacji, +500 PLN/miesiąc
```

**4. Zadania Awaryjne (Eventy)**
```
🚨 "ALERT: Reklamacja w Sklep XYZ"
Deadline: NATYCHMIAST
Opis: "Klient narzeka na jakość dostawy. Rozwiąż problem!"
Nagroda: Unikniesz -30 reputacji
```

**5. Zadania Strategiczne (Odzyskiwanie)**
```
🔄 "Win-back: Kaufland Piaseczno"
Deadline: 14 dni
Opis: "Utracony klient. Przygotuj ofertę win-back."
Nagroda: Odzyskanie klienta (3,000 PLN/miesiąc)
```

##### **D. LISTING PRODUKTÓW U KLIENTA** 📦

**Każdy aktywny klient ma:**
```json
{
  "client_id": "sklep_abc",
  "products_portfolio": [
    {
      "product_id": "fresh_soap",
      "date_added": "2025-10-01",
      "monthly_volume": 50,  // sztuk/miesiąc
      "market_share": 30,    // % vs konkurencja
      "shelf_placement": "prime",  // prime/standard/poor
      "last_promotion": "2025-10-15"
    },
    {
      "product_id": "fresh_shampoo",
      "date_added": "2025-10-10",
      "monthly_volume": 30,
      "market_share": 20,
      "shelf_placement": "standard"
    }
  ],
  "competitor_products": [
    {
      "brand": "Palmolive",
      "market_share": 40,
      "price_vs_us": -10  // 10% tańszy
    },
    {
      "brand": "Nivea",
      "market_share": 30,
      "price_vs_us": +5
    }
  ],
  "total_market_share": 25  // 25% półki to nasze produkty
}
```

**METRYKI:**
- **Listing Score:** Ile produktów z naszego portfolio klient ma (0-12)
- **Market Share:** % naszych produktów vs konkurencja (0-100%)
- **Cross-sell Potential:** Ile jeszcze produktów można sprzedać (0-12)

##### **E. HISTORIA WSPÓŁPRACY** 📊

**Timeline klienta (widoczny w CRM):**
```
📅 2025-10-01: Pierwsza wizyta (Prospect)
✅ 2025-10-05: Kontrakt podpisany (Active) - FreshSoap
🎯 2025-10-08: Wizyta regularna (+5 rep, ocena 4.5⭐)
🆕 2025-10-15: Cross-sell - FreshShampoo (+15 rep)
📦 2025-10-20: Zadanie: Kontrola ekspozycji (+5 rep)
⚠️ 2025-10-27: Brak wizyty (-5 rep) - Reputacja: 15 → 10
```

**Statystyki:**
- Dni współpracy: 27
- Liczba wizyt: 3
- Średnia ocena wizyt: 4.3⭐
- Reputacja: 10 (🟡 Neutralny)
- Market share: 25% → 30% (+5% wzrost!)

#### 5. **WIZYTY HANDLOWE (AI Conversations)** ✅ częściowo
- [x] Rozmowa z NPC (właściciel sklepu)
- [x] System promptów dla AI (Gemini)
- [ ] **DO DODANIA:**
  - [ ] **Kontekst wizyty zależny od statusu klienta:**
    - **PROSPECT (Cold Call):**
      - Brak historii → AI musi przedstawić firmę i produkty
      - Cel: Przekonać do pierwszego kontraktu
      - Trudność: Wysoka (klient nie zna firmy, ma swoich dostawców)
    - **ACTIVE (Check-in):**
      - AI ma dostęp do historii (produkty, ostatnia wizyta, reputacja)
      - Cel: Kontrola ekspozycji, cross-sell, rozwiązanie problemów
      - Trudność: Niska-średnia (klient już współpracuje)
    - **LOST (Win-back):**
      - AI wie dlaczego klient odszedł (lost_reason)
      - Cel: Przeprosić, wyjaśnić, zaoferować coś ekstra
      - Trudność: Bardzo wysoka (klient rozczarowany)
  - [ ] **Automatyczna ocena rozmowy przez AI (1-5⭐):**
    - AI ocenia profesjonalizm, dopasowanie oferty, obsługę obiekcji
    - Wynik wpływa na reputację (patrz poniżej)
  - [ ] **Wynik wizyty:**
    - ✅ **Sukces:** Kontrakt podpisany / Zadanie wykonane / Problem rozwiązany
    - 🤔 **Częściowy:** Klient zainteresowany, wymaga kolejnej wizyty
    - ❌ **Porażka:** Odmowa / Pogorszenie relacji
  - [ ] **Wpływ na reputację (dla ACTIVE klientów):**
    - Ocena 5⭐ → +10 rep
    - Ocena 4⭐ → +5 rep
    - Ocena 3⭐ → +2 rep
    - Ocena 2⭐ → -5 rep
    - Ocena 1⭐ → -15 rep
  - [ ] **Zapisywanie w timeline klienta:**
    - Data, typ wizyty (regularna/zadanie/win-back), ocena, zmiana rep
  - [ ] **Feedback dla gracza:**
    - Podsumowanie: "Co poszło dobrze?" / "Co można poprawić?"
    - Podpowiedzi: "Klient wspomniał o problemie X - możesz zaoferować rozwiązanie Y"

#### 6. **SYSTEM KONTRAKTÓW & PRODUKTY** 🆕
- [ ] **Podpisywanie pierwszego kontraktu (Prospect → Active):**
  - Gracz wybiera produkty z portfolio firmy (sekcja "Nasze Produkty")
  - Klient decyduje o przyjęciu na podstawie:
    - `interest_level` (parametr Prospect)
    - Budżet (zależny od typu: sklep = 500-2k, dyskont = 2-8k, sieć = 10-50k PLN/miesiąc)
    - Jakości rozmowy (ocena AI)
  - **Jeśli sukces:**
    - Status: PROSPECT → ACTIVE
    - Zapisanie `products_portfolio` (lista produktów, wolumen, market share)
    - Ustawienie `visit_frequency_required` (np. co 14 dni dla małych sklepów)
    - Generowanie pierwszego zadania regularnego (wizyta za X dni)
    - reputation = 50 (start jako "Happy Client")
  - **Jeśli porażka:**
    - `visits_count += 1`
    - Jeśli `visits_count >= 3` → Prospect znika (nie zainteresowany)
- [ ] **Wznowienie kontraktu (Contract Renewal):**
  - Każdy kontrakt ma `contract_renewal_date` (np. co 6 miesięcy)
  - **30 dni przed końcem** → automatyczne zadanie ⚠️ "Negocjacje wznowienia: Klient XYZ"
  - **Wynik zależny od reputacji:**
    - ≥70 rep → **Automatyczne wznowienie** (klient zadowolony, nie wymaga wizyty)
    - 50-69 rep → **Wymaga wizyty** (check-in, czy wszystko OK)
    - 20-49 rep → **Trudne negocjacje** (AI stawia warunki: rabat, lepszy serwis, więcej wizyt)
    - <20 rep → **Prawie niemożliwe** (klient rozważa zmianę dostawcy)
  - **Jeśli nie wznowiono do `contract_renewal_date`:**
    - Status: ACTIVE → LOST
    - `lost_reason = "Koniec kontraktu - brak wznowienia"`
    - `win_back_difficulty = 5.0` (średnia trudność)
- [ ] **Modyfikacja kontraktu (Cross-sell / Up-sell):**
  - Podczas wizyty gracz może zaproponować nowe produkty
  - **Szansa sukcesu zależna od:**
    - Reputacji (≥60 → łatwiej przekonać)
    - Historii sprzedaży (jeśli `FreshMilk` dobrze się sprzedaje → łatwiej sprzedać `FreshYogurt`)
    - Budżetu klienta (czy stać go na więcej?)
    - Jakości pitcha (ocena AI)
  - **Jeśli sukces:**
    - Dodanie produktu do `products_portfolio`
    - +15 rep (klient docenia nowe możliwości)
    - +X PLN/miesiąc do `monthly_value`
  - **Jeśli odmowa:**
    - Brak straty (próba nie kosztuje, ale nie można spamować)
    - AI wyjaśnia powód: "Nie mamy miejsca na półce" / "Za drogo" / "Nie pasuje do naszych klientów"

#### 7. **SYSTEM ODZYSKIWANIA KLIENTÓW (Win-back)** 🆕
- [ ] **Jak klient przechodzi do LOST:**
  - **Opcja 1:** Zaniedbanie (reputation < -50)
  - **Opcja 2:** Nieudane wznowienie kontraktu (patrz wyżej)
  - **Opcja 3:** Katastrofalny błąd (np. źle rozwiązana reklamacja → -50 rep w jednej wizycie)
- [ ] **Parametry LOST klienta:**
  ```json
  {
    "status": "LOST",
    "lost_date": "2024-05-15",
    "lost_reason": "Zaniedbanie - brak wizyt przez 6 tygodni",
    "last_reputation": -20,  // ostatnia reputacja przed utratą
    "win_back_attempts": 0,
    "win_back_difficulty": 7.5  // 0-10, rośnie z każdą próbą
  }
  ```
- [ ] **Próba odzyskania (Win-back Task):**
  - Gracz musi **aktywnie zainicjować** zadanie "🔄 Odzyskaj klienta: XYZ" (nie auto-generuje się)
  - **AI rozmowa z trudniejszym promptem:**
    - Klient jest rozczarowany/zły/obojętny (zależy od `lost_reason`)
    - Gracz musi:
      - Przeprosić (jeśli było zaniedbanie)
      - Wyjaśnić (co się zmieniło, dlaczego teraz będzie lepiej)
      - Zaoferować coś ekstra (rabat, darmowa dostawa, lepsze warunki)
  - **Szansa powodzenia zależna od:**
    - `last_reputation` (jeśli było 40 → łatwiej niż -30)
    - `lost_reason` (konkurencja → łatwiej niż zaniedbanie)
    - `win_back_difficulty` (rośnie z każdą nieudaną próbą)
    - Jakości rozmowy (ocena AI)
  - **Jeśli SUKCES:**
    - Status: LOST → ACTIVE
    - reputation = 0 (trzeba odbudować zaufanie od zera)
    - `win_back_attempts` resetuje się do 0
    - `win_back_difficulty` resetuje się do 5.0
    - Gracz dostaje osiągnięcie 🏆 "Drugie szanse"
  - **Jeśli PORAŻKA:**
    - `win_back_attempts += 1`
    - `win_back_difficulty += 2` (każda nieudana próba zwiększa trudność)
    - Klient pozostaje LOST, można spróbować ponownie po ≥7 dniach
  - **Limit:** Jeśli `win_back_attempts >= 3` → klient **na zawsze LOST** (usunięcie z listy)

#### 8. **GENEROWANIE KONTEKSTU DLA AI (Prompt Engineering)** 🆕
- [ ] **System musi automatycznie tworzyć prompt dla AI na podstawie:**
  - **Dane klienta:**
    - Nazwa, typ (sklep/dyskont/sieć)
    - Status (PROSPECT/ACTIVE/LOST)
    - Reputacja (jeśli ACTIVE)
    - Produkty w portfolio (jeśli ACTIVE)
    - Historia wizyt (ostatnie 3-5 eventów z timeline)
    - Powód wizyty (regularna/zadanie/win-back)
  - **Dane gracza:**
    - Poziom kariery (Junior/Mid/Senior → wpływa na umiejętności)
    - Historia z tym klientem (ile wizyt, średnia ocena)
  - **Cel wizyty:**
    - PROSPECT: "Przekonaj do podpisania kontraktu na produkty: [lista]"
    - ACTIVE (regularna): "Sprawdź ekspozycję, zapytaj o problemy, zaproponuj [nowy produkt]"
    - ACTIVE (zadanie): "Rozwiąż problem: [opis zadania]"
    - LOST (win-back): "Odzyskaj klienta - wyjaśnij [lost_reason], zaoferuj [coś ekstra]"
- [ ] **Przykładowy prompt dla AI:**
  ```
  Jesteś właścicielem sklepu "ABC Market" w Piasecznie (mały sklep spożywczy).
  
  KONTEKST:
  - Współpracujesz z firmą FreshMarket od 45 dni
  - Aktualnie masz 2 produkty: FreshSoap, FreshShampoo
  - Ostatnia wizyta: 10 dni temu (ocena 4.5⭐)
  - Reputacja sprzedawcy u Ciebie: 65/100 (Happy Client 😊)
  - Problem: FreshSoap sprzedaje się słabo (tylko 20 sztuk/miesiąc)
  
  TWOJA POSTAWA:
  - Jesteś zadowolony z współpracy, ale masz obawy o FreshSoap
  - Jesteś otwarty na sugestie, ale nie lubisz agresywnej sprzedaży
  - Cenisz sobie regularność wizyt i dobre relacje
  
  CEL SPRZEDAWCY (gracz tego nie widzi):
  - Zadanie: "Sprawdź ekspozycję FreshSoap i zaproponuj promocję"
  - Możliwy cross-sell: FreshDish (płyn do naczyń)
  
  ZASADY ROZMOWY:
  - Reaguj naturalnie na propozycje sprzedawcy
  - Jeśli gracz dobrze rozpozna problem → chętnie przyjmiesz pomoc
  - Jeśli gracz tylko naciska na sprzedaż → odrzuć
  - Po rozmowie oceń profesjonalizm gracza (1-5⭐) i wyjaśnij ocenę
  ```



#### 5. **WIZYTY HANDLOWE (AI Conversations)** ✅ częściowo
- [x] Rozmowa z NPC (właściciel sklepu)
- [x] System promptów dla AI (Gemini)
- [ ] **DO DODANIA:**
  - [ ] Kontekst wizyty (Prospect vs Active):
    - **Prospect:** Cold call, prezentacja firmy i produktów
    - **Active:** Check-in, kontrola, cross-sell, problem solving
  - [ ] Automatyczna ocena rozmowy przez AI (1-5⭐)
  - [ ] Wynik wizyty:
    - ✅ **Prospect:** Kontrakt podpisany (jakie produkty, kwota)
    - ✅ **Active:** Zadania wykonane, problemy rozwiązane, cross-sell
    - 🤔 Do przemyślenia (kolejna wizyta)
    - ❌ Odmowa / Problem
  - [ ] **Wpływ na reputację:**
    - Ocena 5⭐ → +10 rep
    - Ocena 4⭐ → +5 rep
    - Ocena 3⭐ → +2 rep
    - Ocena 1-2⭐ → -15 rep
  - [ ] Zapisywanie historii rozmów w timeline klienta
  - [ ] Feedback dla gracza (co poszło dobrze/źle, podpowiedzi)

#### 6. **SYSTEM KONTRAKTÓW & PRODUKTY** 🆕
- [ ] **Kontrakt zawiera:**
  - Klient (nazwa, typ)
  - Produkty (lista z PORTFOLIO)
  - Wartość miesięczna (PLN)
  - Warunki (terminy dostaw, rabaty)
  - Data podpisania
  - Status: Aktywny / Zawieszony / Anulowany
- [ ] **Zarządzanie kontraktami:**
  - Lista wszystkich kontraktów
  - Suma miesięcznej wartości
  - Alarmy: "Kontrakt wygasa za 7 dni!"
  - Możliwość renegocjacji (nowa wizyta)

#### 6. **NARZĘDZIA TRADE MARKETING** 🆕
**Problem:** Gracz potrzebuje "broni" do przekonywania klientów  
**Rozwiązanie:** Budżet marketingowy + 5 typów narzędzi sprzedażowych

- [ ] **Budżet marketingowy:** 2,000 PLN/miesiąc (Level 1)
- [ ] **5 typów narzędzi:**

  **💰 RABAT CENOWY** (Trade Discount)
  - Koszt: 0 PLN (ale obniża marżę -5% do -20%)
  - Efekt: Łatwiej przekonać klienta
  - Kiedy: PROSPECT (pierwszy kontrakt), Obrona przed konkurencją, Win-back
  - Reputacja: +5
  - Ryzyko: Klient przyzwyczai się (trudno wrócić do pełnej ceny)
  - Limit: 1x na klienta co 3 miesiące

  **🎁 GRATIS** (Free Goods)
  - Koszt: 200-500 PLN
  - Efekt: Kup 10, weź 12 (+20% volume gratis)
  - Kiedy: Test produktu, Motywacja do większego zamówienia, Cross-sell boost
  - Reputacja: +8 (klient bardzo lubi gratisy!)
  - Limit: 3x/miesiąc (budżet 1,500 PLN)

  **📢 MATERIAŁY POS** (Point of Sale)
  - Koszt: 150-300 PLN (stojaki, plakaty, wobblery)
  - Efekt: +15% sprzedaży przez 30 dni, shelf_placement: poor → standard/prime
  - Kiedy: Poprawa ekspozycji, Launch nowego produktu
  - Reputacja: +5
  - Trwałość: 30 dni
  - Limit: 2x/miesiąc (budżet 600 PLN)

  **🎪 PROMOCJA KONSUMENCKA** (Consumer Promo)
  - Koszt: 500-800 PLN (konkursy, loterie, nagrody)
  - Efekt: +30% sprzedaży przez 14 dni, +5% market share
  - Kiedy: Boost przed końcem miesiąca, Launch produktu, Reaktywacja kategorii
  - Przykład: "Kup 2 FreshSoap, wygraj 500 PLN"
  - Reputacja: +10
  - Limit: 1x/miesiąc (budżet 800 PLN)

  **🚚 DARMOWA DOSTAWA** (Free Delivery)
  - Koszt: 100-200 PLN
  - Efekt: Brak opłaty za transport (normalnie 50 PLN/dostawa)
  - Kiedy: Małe sklepy z małym zamówieniem, Klient narzeka na koszty
  - Reputacja: +3
  - Limit: 5x/miesiąc (budżet 1,000 PLN)

- [ ] **UI - Wybór narzędzia podczas wizyty:**
  ```
  ┌─ TWOJE NARZĘDZIA ──────────────────────────────────┐
  │ Budżet: 1,200 / 2,000 PLN (60%)                    │
  │                                                     │
  │ [💰 Rabat 10%]  [🎁 Gratis]  [📢 POS]            │
  │  Koszt: 0 PLN   Koszt: 350    Koszt: 200          │
  │  ✅ Dostępny     ⚠️ 2/3 użyte  ✅ 0/2              │
  └─────────────────────────────────────────────────────┘
  ```

- [ ] **Mechanika w AI conversation:**
  - Gracz może zaproponować narzędzie podczas rozmowy
  - AI reaguje na podstawie typu klienta i reputacji
  - Koszt odejmowany po akceptacji

- [ ] **Strategia:**
  - POS = najlepszy ROI (+15% przez 30 dni)
  - Gratisy = skuteczne, ale drogie
  - Rabaty = ostateczność (przyzwyczajają klienta)
  - Promocje = tylko przed końcem miesiąca (boost targetu)

#### 7. **BALANS ROZGRYWKI** 🆕
**Problem:** Nieograniczone wizyty → gracz przejdzie grę w 1 dzień  
**Rozwiązanie:** System energii + wydarzenia losowe

##### **A. DZIENNY LIMIT AKCJI**

**System czasu pracy:**
- Dzień roboczy: 8:00 - 17:00 (9 godzin)
- Energia: 100% (odnawia się codziennie o 8:00)

**Koszt akcji:**
| Akcja | Czas | Energia |
|-------|------|---------|
| 🚗 Wizyta bliska (5-10km) | 1h | -20% |
| 🚗 Wizyta daleka (20-30km) | 2h | -30% |
| 📋 Zadanie proste | 30 min | -10% |
| 📋 Zadanie trudne | 1.5h | -25% |
| ☕ Lunch break | 30 min | +15% |
| 📞 Telefon | 15 min | -5% |

**Przykładowy dzień (Level 1):**
```
8:00  | 100% | Start
8:30  | 80%  | Wizyta 1 (blisko)
10:00 | 70%  | Zadanie proste
11:00 | 40%  | Wizyta 2 (daleko)
13:00 | 55%  | LUNCH (+15%)
14:00 | 45%  | Zadanie średnie
15:00 | 30%  | 3x telefon
16:00 | 10%  | Wizyta 3 (blisko)
17:00 | KONIEC (za mało na 4. wizytę)
```

**Wynik:** Max **2-3 wizyty + 2 zadania dziennie**

**Progresja:**
- Level 1: 2-3 wizyty/dzień
- Level 2-3: 3-4 wizyty/dzień (+10% efektywność)
- Level 4+: Delegowanie (podwładni robią wizyty)

**Penalty:** Energia <20% → Ryzyko złej oceny (-1⭐)

##### **B. WYDARZENIA DZIENNE** 🎲

**System losowych eventów (1-2/dzień):**
- 🎉 Pozytywne (30%): Bonusy, nowi klienci, gratisy
- ⚠️ Neutralne (50%): Wybory gracza (małe konsekwencje)
- 🚨 Negatywne (20%): Wyzwania, konkurencja, awarie

**Przykłady:**

🎉 **Pozytywne:**
- "Rekomendacja od klienta" → +1 prospect na mapie, +10 rep u nowego
- "Znalazłeś gratis w bagażniku" → +300 PLN budżetu
- "Artykuł w gazecie o firmie" → Wszyscy klienci +2 rep

⚠️ **Neutralne/Wybory:**
- "Telefon: Klient chce promocję" → [Zgoda -500 PLN, +15 rep] / [Odmowa -5 rep]
- "Email od szefa: Raport do końca dnia" → [Teraz -20% energii] / [Jutro -5 rep]
- "Klient prosi o dłuższy termin płatności" → [30 dni +10 rep] / [14 dni bez zmian]

🚨 **Negatywne:**
- "Awaria samochodu" → Dziś -50% energii (max 1 wizyta)
- "Konkurencja: Promocja -30%" → 3 klientów rozważa odejście (zadanie: odwiedź w 3 dni)
- "Product recall" → Musisz zadzwonić do wszystkich klientów (-2h, ale +5 rep za profesjonalizm)

**Mechanika:**
- 70% bez wpływu (flavor: "Pada deszcz", "Ulubiona piosenka w radiu")
- 30% wymaga reakcji (wybór gracza)
- Historia eventów w timeline

##### **C. RYTM TYGODNIA**

**5 dni roboczych:**
| Dzień | Wizyty | Zadania | Wydarzenia | Vibe |
|-------|--------|---------|------------|------|
| PON | 2-3 | 2 proste | Pozytywne | Spokojny start |
| WT | 3 | 1 średnie | Neutralne | Momentum |
| ŚR | 2 | 2 trudne | Wybór | Środek tygodnia |
| CZW | 3-4 | 1 proste | Negatywne | Push |
| PT | 2 | Raport | Pozytywne | Podsumowanie |

**Tydzień w liczbach:**
- 12-15 wizyt (średnio 3/dzień)
- 6-8 zadań
- 5-7 wydarzeń
- Cel: 2,500 PLN/tydzień (10k/miesiąc ÷ 4)

**Nagrody tygodniowe:**
- Cel sprzedaży: +500 PLN
- Wszystkie zadania: +200 PLN
- 0 utraconych klientów: +100 PLN
- Perfekcja: +1,000 PLN + Osiągnięcie 🏆

##### **D. RYTM MIESIĄCA**

**4 tygodnie:**
| Tydzień | Focus | Difficulty |
|---------|-------|------------|
| **1** | 🎯 Prospecting | Łatwy |
| **2** | 🤝 Relationship | Średni |
| **3** | 💰 Cross-sell | Trudny |
| **4** | 📊 Closing | HARD |

**Koniec miesiąca:**
- Raport miesięczny (PLN, klienci, avg rep)
- Ocena szefa: 1-5⭐
- Progres do awansu
- Reset: Nowe zadania, nowi prospects

**Czas gry (estimate):**
- 1 wizyta: 5-10 min
- 1 zadanie: 3-5 min
- 1 dzień w grze: 20-30 min real time
- 1 tydzień: 1.5-2h
- 1 miesiąc (Level 1): 6-8h

**Sweet spot:** **30 min/dzień** = zaangażowanie jak daily mobile game 📱

#### 8. **DASHBOARD** 🚧
- [ ] **KPI Miesiąca:**
  - 💰 Cel sprzedaży: 10,000 PLN
  - 📊 Aktualny stan: X PLN (Y%)
  - 🎯 Liczba kontraktów: X/5 (cel: min 5)
  - ⭐ Średnia ocena wizyt: 4.2/5.0
- [ ] **Calendar widget:**
  - Zaplanowane wizyty na tydzień
  - Liczba wizyt w tym tygodniu
- [ ] **Top alerts:**
  - "Kontrakt XYZ wygasa!"
  - "Nowy prospect dostępny!"
  - "Cel miesiąca: 60% osiągnięty"

#### 7. **KLIENCI (Baza CRM)** 🚧
- [ ] **Lista wszystkich klientów:**
  - Filtry: Status, Typ, Dystans, Potencjał
  - Sortowanie: Nazwa, Data ostatniej wizyty, Wartość
- [ ] **Karta klienta:**
  - Dane podstawowe
  - Historia wizyt (timeline)
  - Aktualne kontrakty
  - Notatki (edytowalne przez gracza)
  - Akcje: "Zaplanuj wizytę", "Dodaj notatkę"

#### 8. **ZADANIA (To-Do List)** 🚧
- [ ] **Auto-generowane zadania:**
  - "Odwiedź 3 nowych prospectów"
  - "Renegocjuj kontrakt z Sklep ABC"
  - "Osiągnij 10k PLN sprzedaży"
- [ ] **Manualne zadania:**
  - Gracz może dodać własne
- [ ] **Priorytety:** 🔴 Pilne | 🟡 Ważne | 🟢 Normalne

#### 9. **STATYSTYKI KARIERY** ✅
- [x] Obecny poziom i postęp
- [x] Wymagania do awansu
- [x] Kluczowe metryki
- [x] Timeline poziomów

#### 10. **MOJA FIRMA** ✅
- [x] Informacje o FreshLife Poland
- [x] Portfolio produktów
- [x] Misja i wartości

---

## 🗺️ MECHANIKA GEOGRAFICZNA (Szczegóły)

### **Lokalizacja Startowa: Piaseczno**
- Centrum: ul. Puławska (lub inna centralna)
- Promień działania: 30 km
- **Obszar pokrycia:**
  - Warszawa Południe (Ursynów, Mokotów, Wilanów)
  - Piaseczno i okolice
  - Konstancin-Jeziorna
  - Góra Kalwaria
  - Tarczyn
  - Fragment Pruszków/Raszyn

### **Typy Klientów:**

#### 🏪 **Małe sklepy (Tier 3)**
- **Przykłady:** "Sklep u Janusza", "Spożywczak Kasia", "Osiedlowy Mini Market"
- **Lokalizacja:** 5-15 km od bazy
- **Potencjał:** 500-1,500 PLN/miesiąc (LOW)
- **Czas wizyty:** 30 min
- **Poziom trudności:** ⭐ (łatwy - prosty właściciel)
- **Liczba:** ~15 prospectów

#### 🛒 **Dyskonty (Tier 2)**
- **Przykłady:** "Dino Konstancin", "Biedronka Piaseczno Centralna", "Lewiatan Góra Kalwaria"
- **Lokalizacja:** 10-25 km
- **Potencjał:** 2,000-5,000 PLN/miesiąc (MEDIUM)
- **Czas wizyty:** 45 min
- **Poziom trudności:** ⭐⭐ (kierownik - bardziej wymagający)
- **Liczba:** ~10 prospectów

#### 🏬 **Sieci lokalne (Tier 1)**
- **Przykłady:** "Kaufland Piaseczno", "Carrefour Ursynów", "Auchan Janki"
- **Lokalizacja:** 15-30 km
- **Potencjał:** 5,000-15,000 PLN/miesiąc (HIGH)
- **Czas wizyty:** 60 min
- **Poziom trudności:** ⭐⭐⭐ (Category Manager - expert)
- **Liczba:** ~5 prospectów

### **Koszty Dojazdu:**
- **Czas:** Google Maps API (realistyczny)
- **Pieniądze:** 0.50 PLN/km (koszt samochodu służbowego - widoczne w raporcie)
- **Reputacja:** Spóźnienie = -1⭐ w ocenie wizyty

### **Optymalizacja Trasy:**
- Gracz może planować "okrężną" trasę (2-3 klientów tego samego dnia)
- System podpowiada optymalną kolejność
- Bonus: "Efficient Route Planner" (+10% czasu zaoszczędzonego)

---

## 🎮 GAMEPLAY FLOW - TYDZIEŃ PRACY

### **Poniedziałek rano (8:00):**
1. Gracz loguje się do Dashboard
2. Widzi cele na tydzień:
   - 🎯 Zdobądź 3 nowe kontrakty
   - 💰 Wartość sprzedaży: 3,000 PLN (tydzień 1/4 miesiąca)
3. Otwiera **Tab "Mapa Terenu"**
4. Przegląda prospectów:
   - "Sklep u Janusza" (8 km, LOW, 30 min)
   - "Dino Konstancin" (12 km, MEDIUM, 45 min)
   - "Kaufland Piaseczno" (5 km, HIGH, 60 min)

### **Planowanie (Drag & Drop):**
1. Gracz przeciąga "Sklep u Janusza" na Poniedziałek 9:00
2. System liczy:
   - Dojazd: 8 km = ~15 min
   - Wizyta: 30 min
   - Powrót: 15 min
   - **TOTAL: 1h** (Koniec: 10:00)
3. Dodaje "Dino Konstancin" na 10:30
   - Dojazd z poprzedniej lokalizacji: ~10 min
   - Wizyta: 45 min
   - **TOTAL: 55 min** (Koniec: 11:25)
4. Wraca do biura: 12:00 (lunch break)
5. Po południu: "Kaufland" 14:00-16:00

### **Wizyta (AI Conversation):**
1. Gracz klika "Rozpocznij wizytę" o 9:00
2. System ładuje kartę klienta: "Sklep u Janusza"
3. Wyświetla kontekst:
   - Typ: Mały sklep
   - Profil właściciela: "Janusz, 55 lat, konserwatywny, lubi tradycję"
   - Potrzeby: Szuka dostawcy produktów śniadaniowych
4. Rozmowa AI startuje (jak obecny system)
5. Po rozmowie: AI ocenia (1-5⭐) + wynik:
   - ✅ "Janusz zainteresowany! Chce zamówienie próbne (500 PLN/miesiąc)"
   - 🎉 +1 kontrakt, +500 PLN do celu

### **Koniec dnia:**
- Gracz wraca do bazy (17:00)
- Dashboard update:
  - 🎯 Nowe kontrakty: 1/3 ✅
  - 💰 Wartość: 500/3,000 PLN (17%)
  - ⭐ Średnia ocena: 4.5/5.0
- System zapisuje progres

### **Wtorek-Piątek:**
- Repeat: planowanie → wizyty → ocena → progres
- Gracz stopniowo wypełnia kalendarz
- Optymalizuje trasy (mniej dojazdu = więcej wizyt)

### **Koniec Tygodnia (Piątek 17:00):**
- Podsumowanie:
  - 🎯 Kontrakty: 4/3 ✅ (EXCEEDED!)
  - 💰 Wartość: 3,500/3,000 PLN ✅
  - ⭐ Ocena: 4.3/5.0
  - 🚗 Dystans: 350 km (koszt: 175 PLN)
- Feedback: "Świetna robota! Przekroczyłeś cel o 17%!"

---

## 📈 PROGRESJA (Level 1 → Level 2)

### **Wymagania Awansu:**
```
✅ Miesięczna sprzedaż: 10,000+ PLN
✅ Min. liczba kontraktów: 10
✅ Średnia ocena wizyt: 4.0+/5.0
✅ Czas w poziomie: min. 1 miesiąc (4 tygodnie)
```

### **Po Awansie:**
- 🎉 Gratulacje! Jesteś teraz **Sales Representative**
- 🔓 Unlock:
  - Większe terytorium (40 km)
  - Dostęp do większych klientów (Carrefour, Auchan)
  - Wyższe cele (15,000 PLN/miesiąc)
- 💰 Podwyżka (wyższa prowizja)

---

## 🛠️ TECHNOLOGIE & INTEGRACJE

### **Mapa:**
- **Opcja A:** Streamlit + Folium (leaflet.js)
  - ✅ Proste, darmowe
  - ✅ Interaktywne pinezki
  - ❌ Brak routingu (trzeba dodać)
- **Opcja B:** Google Maps API
  - ✅ Profesjonalne
  - ✅ Routing wbudowany
  - ❌ Kosztowne (API calls)
- **Rekomendacja:** Start z Folium, później upgrade do Google Maps

### **Dane Klientów:**
- Fake data (generated names, addresses w okolicy Piaseczna)
- JSON file lub DB (SQLite)
- Atrybuty:
  ```json
  {
    "id": "client_001",
    "name": "Sklep u Janusza",
    "type": "small_shop",
    "lat": 52.0814,
    "lon": 21.0276,
    "address": "ul. Puławska 123, Piaseczno",
    "distance_from_base": 8.5,
    "potential": "LOW",
    "owner_profile": "conservative, traditional",
    "status": "prospect",
    "notes": []
  }
  ```

### **Time Management:**
- Python datetime
- Slot booking system (calendar grid)
- Walidacja kolizji ("Wizyta nachodzi na inną!")

### **AI Conversations:**
- Gemini API ✅ (już działa)
- Dodać: evaluation prompt (ocena rozmowy)

---

## 🎨 UI/UX MOCKUP

### **Tab: Mapa Terenu**
```
┌─────────────────────────────────────────────┐
│  🗺️ TWOJE TERYTORIUM - PIASECZNO (30km)    │
├─────────────────────────────────────────────┤
│                                             │
│  [Mapa z pinezkami]                         │
│   📍 Baza: Piaseczno                        │
│   🏪 Zielone: Nieodwiedzeni                 │
│   🟡 Żółte: W trakcie                       │
│   ✅ Niebieskie: Aktywni                    │
│   ❌ Czerwone: Straceni                     │
│                                             │
├─────────────────────────────────────────────┤
│  FILTRY:                                    │
│  [x] Tier 1  [x] Tier 2  [x] Tier 3        │
│  [x] LOW  [x] MEDIUM  [x] HIGH              │
│  Dystans: [0] ━━━●━━━ [30] km              │
├─────────────────────────────────────────────┤
│  LISTA PROSPECTÓW (15):                     │
│  🏪 Sklep u Janusza | 8km | LOW | 🔓       │
│     [Więcej info] [Zaplanuj wizytę]        │
│  🛒 Dino Konstancin | 12km | MED | 🔓      │
│     [Więcej info] [Zaplanuj wizytę]        │
└─────────────────────────────────────────────┘
```

### **Tab: Dashboard**
```
┌─────────────────────────────────────────────┐
│  🏢 DASHBOARD - TYDZIEŃ 1/4                 │
├─────────────────────────────────────────────┤
│  💰 CEL MIESIĄCA: 10,000 PLN               │
│  ████████░░░░░░░ 3,500 PLN (35%)           │
│                                             │
│  🎯 KONTRAKTY: 4/10                         │
│  ⭐ OCENA: 4.3/5.0                          │
│  🚗 DYSTANS: 350 km                         │
├─────────────────────────────────────────────┤
│  📅 TEN TYDZIEŃ:                            │
│  ✅ Pon: 3 wizyty (500+800+1200 PLN)       │
│  ✅ Wt:  2 wizyty (600+400 PLN)            │
│  ⏳ Śr:  Zaplanowane (2 wizyty)            │
│  🔓 Czw: Wolne                              │
│  🔓 Pt:  Wolne                              │
├─────────────────────────────────────────────┤
│  🚨 ALERTY:                                 │
│  • Kontrakt "Sklep ABC" wygasa za 5 dni!   │
│  • Nowy prospect dostępny: "Biedronka XYZ" │
└─────────────────────────────────────────────┘
```

---

## 📋 BACKLOG (Post-MVP)

### **PHASE 2 (Level 2-3):**
- [x] ✅ **System promocji** → DODANE w sekcji 6 (Narzędzia Trade Marketing)
- [x] ✅ **Eventy losowe** → DODANE w sekcji 7B (Wydarzenia dzienne)
- [ ] Konkurencja (inne firmy walczą o tych samych klientów)
- [ ] Seasonal trends (więcej sprzedaży przed świętami)
- [ ] Weather system (pogoda wpływa na sprzedaż i wizyty)
- [ ] Achievements/Badges ("Pierwszy milion", "100 wizyt", etc.)

### **PHASE 3 (Level 4+):**
- [ ] Zarządzanie zespołem (delegowanie wizyt)
- [ ] Rekrutacja Junior Reps
- [ ] Coaching i rozwój podwładnych
- [ ] Team conflicts (AI conversations między członkami zespołu)
- [ ] Performance reviews (ocena podwładnych)

### **PHASE 4 (Level 7+):**
- [ ] Strategia regionalna
- [ ] Budżety i planowanie
- [ ] Board meetings (AI prezentacje)
- [ ] M&A (przejęcia konkurencji)
- [ ] Launch nowych produktów (R&D decisions)

---

## ✅ MVP CHECKLIST (ZAKTUALIZOWANE)

### **Must Have (bez tego MVP nie działa):**
- [ ] Mapa z 20+ klientami (Folium)
- [ ] System planowania wizyt (kalendarz + energia)
- [ ] **System energii (100% dziennie, -20%/-30% za wizytę)** 🆕
- [ ] AI rozmowy handlowe (Gemini)
- [ ] Ocena rozmów + feedback (1-5⭐ + wyjaśnienie)
- [ ] **Narzędzia Trade Marketing (5 typów, budżet 2k)** 🆕
- [ ] System kontraktów (PROSPECT → ACTIVE → LOST)
- [ ] **Reputacja (-100 do +100, progi, timeline)** 🆕
- [ ] Dashboard z celami i KPI
- [ ] Progres do awansu (Level 1→2)

### **Should Have (ważne, ale można dodać później):**
- [ ] **Wydarzenia dzienne (1-2/dzień, 70% flavor)** 🆕
- [ ] Routing optimization (podpowiedzi tras)
- [ ] CRM szczegółowy (notatki, historia, stats)
- [ ] Zadania auto-generowane (regularne wizyty)
- [ ] Alerty (wygasające kontrakty, niskie rep)
- [ ] **Nagrody tygodniowe (+500 PLN za cel)** 🆕

### **Nice to Have (polish):**
- [ ] Animacje przejść (mapa → wizyta)
- [ ] Sound effects (dzwonek, sukces, porażka)
- [ ] **Achievements ("Perfekcyjny tydzień", "Win-back master")** 🆕
- [ ] Leaderboard (multiplayer - porównanie z innymi graczami)
- [ ] Mobile app (PWA)
- [ ] Dark mode
- [ ] Alerty (wygasające kontrakty)

### **Nice to Have (polish):**
- [ ] Animacje przejść
- [ ] Sound effects
- [ ] Achievements/Badges
- [ ] Leaderboard (multiplayer)

---

## 📋 PODSUMOWANIE SYSTEMU KLIENTA

### **Cykl życia klienta w pigułce:**

```
🔍 PROSPECT (Hunting)
├─ 3 wizyty max
├─ Cel: Podpisać pierwszy kontrakt
├─ Trudność: Wysoka (cold call)
└─ Wynik: ACTIVE ✅ lub znika ❌

😊 ACTIVE (Farming)
├─ Regularne wizyty (co X dni)
├─ Reputacja -100 do +100
├─ Zadania auto-generowane
├─ Cross-sell opportunities
├─ Renewal co 6 miesięcy
└─ Jeśli zaniedbany → LOST ⚠️

🔄 LOST (Win-back)
├─ Klient odszedł (zaniedbanie/koniec kontraktu/błąd)
├─ Win-back difficulty: 0-10 (rośnie z próbami)
├─ Max 3 próby odzyskania
└─ Wynik: ACTIVE ✅ lub trwałe LOST ❌
```

### **Kluczowe mechaniki:**

| Mechanika | Cel | Wpływ na gameplay |
|-----------|-----|-------------------|
| **Reputacja** | Mierzy jakość relacji | Decyduje o trudności renewal, cross-sell, win-back |
| **Wizyty regularne** | Wymuszają zaangażowanie | Brak wizyty → -5 rep/dzień → ryzyko LOST |
| **Zadania** | Dają cele krótkoterminowe | Auto-generują się → gracz zawsze ma "co robić" |
| **Produkty u klienta** | Budują wartość klienta | Cross-sell zwiększa monthly_value → wyższe prowizje |
| **Timeline klienta** | Historia współpracy | Gracz widzi postęp/błędy → uczy się z doświadczenia |
| **Contract Renewal** | Długoterminowe planowanie | Wymaga utrzymania rep ≥50 przez 6 miesięcy |
| **Win-back** | Second chance | Ryzyko vs reward (trudne, ale wartościowe) |

### **Przykładowy flow gracza (pierwszy miesiąc):**

**Tydzień 1:**
- Start: 0 klientów, 3 PROSPECTS na mapie
- Dzień 1-2: Odwiedzam Prospect A, B (cold calls)
- Wynik: A → kontrakt ✅ (2 produkty, 1,500 PLN/miesiąc), B → "może później"
- Status: 1 ACTIVE (rep=50), 1 PROSPECT (visits=1)

**Tydzień 2:**
- Zadanie auto: "Wizyta regularna u A (za 14 dni od kontraktu)"
- Odwiedzam Prospect B ponownie → kontrakt ✅ (1 produkt, 800 PLN/miesiąc)
- Pojawia się Prospect C (nowy na mapie)
- Status: 2 ACTIVE (rep=50 każdy), 1 PROSPECT

**Tydzień 3:**
- Wizyta regularna u A → ocena 4⭐ (+5 rep) → rep=55
- Zadanie: "Cross-sell: Zaproponuj FreshYogurt klientowi A"
- Próba cross-sell → sukces ✅ (+15 rep, +400 PLN/miesiąc)
- Status: A (rep=70, 1,900 PLN/m), B (rep=50, 800 PLN/m)

**Tydzień 4:**
- Wizyta u B zaplanowana, ale ZANIEDBANA (zapomniałem!)
- B: reputation 50 → 40 (-2 dni x -5 rep)
- Alert: "⚠️ Klient B niezadowolony - zaplanuj wizytę ASAP!"
- Odwiedzam B → ocena 5⭐ (+10 rep) → rep=50 (odbudowane)

**Koniec miesiąca:**
- **Sprzedaż:** 2,700 PLN/miesiąc (2 active × ~1,300 avg)
- **Kontrakty:** 2/5 (cel Level 1: min 5)
- **Rating:** 4.5⭐ średnia (4+5)/2
- **Status:** Trzeba pozyskać 3 więcej klientów w miesiącu 2!

### **Co robi ten system wyjątkowym?**

✅ **Nie jest "wygrywamy wszystko"** - Można stracić klientów przez zaniedbanie  
✅ **Długoterminowe planowanie** - Trzeba myśleć 6 miesięcy do przodu (renewals)  
✅ **Ryzyko vs reward** - Win-back trudny, ale wartościowy (cross-sell łatwiejszy)  
✅ **Emergent gameplay** - Gracz tworzy własne strategie (farming vs hunting balance)  
✅ **Learning curve** - Błędy w miesiącu 1 uczą jak grać w miesiącu 2  
✅ **Repeatability** - Każda rozgrywka inna (różni klienci, różne AI responses)

---

## 🎯 DEFINITION OF DONE (MVP)

**Gracz może:**
1. ✅ Zalogować się jako Junior Sales Rep
2. ✅ Zobaczyć mapę z prospectami w okolicy Piaseczna
3. ✅ Wybrać klienta i zaplanować wizytę na konkretny dzień/godzinę
4. ✅ Przeprowadzić rozmowę handlową z AI (NPC)
5. ✅ Otrzymać ocenę rozmowy (1-5⭐) i wynik (kontrakt/brak)
6. ✅ Zobaczyć postęp w Dashboard (ile PLN, ile kontraktów)
7. ✅ Po miesiącu awansować do Level 2 (jeśli spełnia wymagania)

**Jeśli powyższe działa = MVP READY! 🚀**

---

## 🚀 NEXT STEPS

1. **Tydzień 1:** Mapa + System klientów
2. **Tydzień 2:** Kalendarz + Planowanie wizyt
3. **Tydzień 3:** Integracja AI (ocena + feedback)
4. **Tydzień 4:** Dashboard + System kontraktów
5. **Tydzień 5:** Testing + Bug fixes
6. **Tydzień 6:** BETA LAUNCH! 🎉

---

**Autor:** AI Assistant + User  
**Ostatnia aktualizacja:** 28.10.2025  
**Kontakt:** [Dodaj swój email/Discord]
