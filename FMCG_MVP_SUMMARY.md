# 🎮 FMCG Game - MVP Summary (Dla Klienta)

**Data:** 28.10.2025  
**Wersja:** 1.0 (po dodaniu Trade Marketing + Balansu)

---

## 🎯 CORE CONCEPT

**"Symulator kariery w sprzedaży FMCG z AI rozmowami handlowymi"**

Gracz zaczyna jako **Junior Sales Rep** w firmie FreshMarket i buduje karierę przez:
- 🗺️ Zarządzanie terytorium (mapa 30km wokół Piaseczna)
- 🤝 Rozmowy handlowe z AI (właściciele sklepów)
- 📈 Zarządzanie relacjami (reputacja -100 do +100)
- 💰 Osiąganie celów sprzedażowych (10k PLN/miesiąc → awans)

---

## 🔑 KLUCZOWE MECHANIKI (MVP)

### 1. **CYKL ŻYCIA KLIENTA** (3 statusy)

```
🔍 PROSPECT → ✅ ACTIVE → ❌ LOST
   (Hunting)   (Farming)   (Win-back)
```

- **PROSPECT:** Szukasz nowych klientów, cold call, trudne przekonanie
- **ACTIVE:** Obsługujesz klientów, regularne wizyty, budowanie reputacji
- **LOST:** Zaniedbałeś klienta, musi go odzyskać (bardzo trudne!)

### 2. **REPUTACJA** (-100 do +100)

**DWA POZIOMY:** 🆕
1. **Reputacja u klienta** (indywidualna dla każdego ACTIVE/LOST)
2. **Reputacja ogólna handlowca** (średnia ważona wszystkich klientów)

**Reputacja u klienta - Rośnie gdy:**
- Odwiedzasz regularnie (+5)
- Dostajesz 5⭐ od AI (+10)
- Sprzedajesz nowy produkt (+15)

**Reputacja u klienta - Maleje gdy:**
- Nie odwiedzasz > 7 dni (-5/dzień)
- Dostajesz 1-2⭐ (-15)
- Nie wykonujesz zadań (-10)

**6 progów u klienta:**
- 80-100: VIP Client 🌟
- 50-79: Happy Client 😊
- 20-49: Neutral 😐
- 0-19: At Risk ⚠️
- -1 to -49: Critical 😞
- <-50: LOST ❌

**Reputacja ogólna handlowca:** 🆕
- Średnia ważona reputacji u wszystkich klientów
- **ACTIVE:** 80% wagi (ważone wartością miesięczną - VIPy liczą się bardziej)
- **LOST:** 20% wagi (kara za utratę klienta)
- **Wzór:** `(sum(rep_active × value) / sum(value)) × 0.8 + (avg(rep_lost)) × 0.2`

**Przykład:**
```
ACTIVE:
- Sklep A: rep=70, 1,000 PLN → waga: 70,000
- Sklep B: rep=60, 500 PLN → waga: 30,000
- Sklep C: rep=80, 1,500 PLN → waga: 120,000
Średnia ACTIVE: 220,000 / 3,000 = 73.3

LOST:
- Sklep D: rep=-30 → średnia: -30

OGÓLNA: 73.3 × 0.8 + (-30) × 0.2 = 58.6 - 6 = 52.6 → 53/100
```

**Progi reputacji ogólnej:**
| Rep | Tytuł | Efekty |
|-----|-------|--------|
| 90-100 | 🏆 Sales Legend | +10% zamówienia, +500 PLN/m bonus |
| 75-89 | 🌟 Top Performer | +5% zamówienia, Premium klienci |
| 60-74 | ✅ Solid Rep | Standard |
| 40-59 | 🟡 Average | Ostrzeżenie szefa |
| 20-39 | ⚠️ Struggling | -10% nowe kontrakty |
| <20 | 🔴 At Risk | -20% kontrakty, Ryzyko zwolnienia |

**Wpływ na gameplay:**
- Nowi PROSPECT: Jeśli rep ≥75 → "Słyszałem dobre rzeczy!" (+10 starting rep)
- Awans Level 2: Wymaga rep ≥60 (nie można z "Average")
- Email od szefa: Jeśli <40 → "30 dni na poprawę lub zwolnienie!"
- Rekomendacje: Jeśli ≥90 → Dostęp do VIP prospectów

**Strategiczne dylematy:**
- ❓ Inwestować w małego klienta (rep=45) czy szukać nowych?
- ❓ Odzyskiwać LOST (-30 rep) czy skupić się na ACTIVE?
- ❓ 1 VIP (5k PLN) vs 5 małych (1k każdy) → różny wpływ na avg

### 3. **NARZĘDZIA TRADE MARKETING** 🆕

**Budżet:** 2,000 PLN/miesiąc

**5 narzędzi:**
1. 💰 **Rabat** (0 PLN) - obniża cenę, +5 rep
2. 🎁 **Gratis** (350 PLN) - Kup 10, weź 12, +8 rep
3. 📢 **POS** (200 PLN) - Stojaki/plakaty, +15% sprzedaży przez 30 dni, +5 rep
4. 🎪 **Promocja** (600 PLN) - Konkurs dla klientów końcowych, +30% przez 14 dni, +10 rep
5. 🚚 **Darmowa dostawa** (150 PLN) - Free shipping, +3 rep

**Strategia:** Gracz musi mądrze wydawać budżet (POS = najlepszy ROI)

### 4. **BALANS ROZGRYWKI** 🆕

**System energii:**
- Dzień: 8:00-17:00 (100% energii)
- Wizyta bliska (5-10km): -20% energii
- Wizyta daleka (20-30km): -30% energii
- Zadanie proste: -10%
- Lunch break: +15%

**Wynik:** Max **2-3 wizyty + 2 zadania dziennie**

**Wydarzenia losowe (1-2/dzień):**
- 🎉 30% pozytywne (bonusy, nowi klienci)
- ⚠️ 50% neutralne (wybory gracza)
- 🚨 20% negatywne (awaria auta, konkurencja)

**Rytm:**
- **1 dzień:** 20-30 min gry (2-3 wizyty)
- **1 tydzień:** 1.5-2h gry (12-15 wizyt)
- **1 miesiąc:** 6-8h (osiągnięcie Level 1 targetu)

### 5. **AI CONVERSATIONS**

**Wizyta handlowa = rozmowa z AI (Gemini):**
- Gracz pisze/mówi (speech-to-text)
- AI odpowiada jako właściciel sklepu
- AI ocenia rozmowę (1-5⭐)
- Feedback: "Co poszło dobrze? Co poprawić?"

**Kontekst AI zależy od:**
- Statusu (PROSPECT/ACTIVE/LOST)
- Reputacji (VIP vs At Risk = różne nastroje)
- Historii (ile wizyt, jakie produkty)
- Celu (cold call / check-in / win-back)

### 6. **PRODUKTY U KLIENTA**

**Każdy aktywny klient ma listing produktów:**
```json
{
  "product": "FreshSoap",
  "monthly_volume": 50 sztuk,
  "market_share": 30%,  // vs konkurencja
  "shelf_placement": "prime",  // prime/standard/poor
  "trend": "growing"  // growing/stable/declining
}
```

**Cross-sell:** Gracz może sprzedać więcej produktów → +15 rep, +PLN

---

## 📊 PRZYKŁADOWY FLOW (1 TYDZIEŃ)

**Poniedziałek:**
- 8:00: Start (100% energii)
- 9:00: 🚗 Wizyta u "Sklep U Janusza" (PROSPECT, cold call)
  - AI rozmowa: Przekonywanie do FreshSoap
  - Używam narzędzia: 🎁 Gratis (2 sztuki za darmo)
  - Wynik: ✅ Kontrakt podpisany! 500 PLN/miesiąc, ocena 4⭐
- 11:00: 📋 Zadanie: "Raport tygodniowy" (proste)
- 13:00: ☕ Lunch break (+15% energii)
- 14:00: 🚗 Wizyta u "Biedronka Konstancin" (ACTIVE, check-in)
  - Reputacja: 65/100 (Happy Client)
  - AI rozmowa: Kontrola ekspozycji
  - Wynik: ✅ Wszystko OK, ocena 5⭐ (+10 rep → 75/100)
- 16:00: 🎲 **Wydarzenie:** "Telefon od klienta - chce promocję"
  - Wybór: [Zgoda -500 PLN, +15 rep] → Wybieram
- 17:00: Koniec dnia

**Wynik dnia:**
- 2 wizyty (1 nowy kontrakt + 1 check-in)
- 1 zadanie
- 500 PLN sprzedaży
- 1 PROSPECT → ACTIVE (Sklep U Janusza, rep=50)
- Budżet: 1,650/2,000 PLN (użyłem gratis + promocja)
- **🌟 Reputacja ogólna:** 58/100 → 62/100 🆕
  - ACTIVE (2): Janusz=50, Biedronka=75 → avg=62.5
  - LOST (0): -
  - Wzrost: Nowy klient + poprawa u Biedronki

**Wtorek-Piątek:** Podobnie...

**Koniec tygodnia:**
- 12 wizyt (4 nowe kontrakty + 8 check-ins)
- Sprzedaż: 3,500 PLN (cel: 2,500) ✅
- Średnia ocena: 4.3⭐
- **🌟 Reputacja ogólna:** 62 → 68/100 (✅ Solid Rep!)
  - ACTIVE (5): avg=68 (4 zadowolonych + 1 neutralny)
  - LOST (0): Brak
- **Nagroda:** +500 PLN bonus (osiągnięty cel)

---

## 🎯 CEL GRY (MVP = Level 1)

**Awans do Level 2:**
- ✅ Miesięczna sprzedaż: 10,000 PLN
- ✅ Kontrakty: Min. 10 aktywnych klientów
- ✅ Średnia ocena wizyt: 4.0+/5.0
- ✅ **Reputacja ogólna: ≥60** 🆕 (nie można awansować z "Average")
- ✅ Czas: Min. 1 miesiąc (4 tygodnie)

**Po awansie:**
- 🔓 Większe terytorium (40km)
- 🔓 Dostęp do większych klientów (Carrefour, Auchan)
- 💰 Wyższe cele (25,000 PLN/miesiąc)
- 📈 Nowe mechaniki (zespół, strategia)

---

## 🛠️ TECHNOLOGIE

| Komponent | Technologia | Status |
|-----------|-------------|--------|
| **Backend** | Python + Streamlit | ✅ Działa |
| **Mapa** | Folium (leaflet.js) | 🚧 Do dodania |
| **AI** | Google Gemini | ✅ Działa |
| **Speech-to-text** | SpeechRecognition | ✅ Działa |
| **Baza danych** | JSON (user_data) | ✅ Działa |
| **Klienci** | 6 fake klientów | ✅ Gotowe |

---

## 📋 CHECKLISTY IMPLEMENTACJI

### **MUST HAVE (bez tego nie działa):**
- [ ] Mapa z 20+ klientami (pinezki, filtry)
- [ ] Kalendarz wizyt + system energii
- [ ] Narzędzia Trade Marketing (UI + mechanika, budżet 2k)
- [ ] **Reputacja u klienta** (timeline, progi -100 do +100, UI)
- [ ] **Reputacja ogólna handlowca** 🆕 (średnia ważona, widget w Dashboard)
- [ ] Wydarzenia dzienne (popup, historia, 1-2/dzień)
- [ ] Dashboard (cele, KPI, alerty, **widget reputacji ogólnej**)
- [ ] System kontraktów (PROSPECT/ACTIVE/LOST transitions)

### **SHOULD HAVE (ważne, ale może poczekać):**
- [ ] Routing (optymalizacja tras)
- [ ] CRM (szczegółowa karta klienta)
- [ ] Zadania auto-generowane
- [ ] Nagrody tygodniowe
- [ ] **Wykres historii reputacji ogólnej** 🆕 (timeline 4 tygodni)
- [ ] **Email od szefa przy rep <40** 🆕 ("30 dni na poprawę!")
- [ ] Achievements

### **NICE TO HAVE (polish):**
- [ ] Animacje
- [ ] Sound effects
- [ ] Leaderboard
- [ ] Mobile PWA

---

## ⏱️ TIMELINE IMPLEMENTACJI

| Tydzień | Zadania | Deliverable |
|---------|---------|-------------|
| **1** | Mapa + Klienci (30 fake) | Interaktywna mapa z prospektami |
| **2** | Kalendarz + Energia | Planowanie wizyt działa |
| **3** | Narzędzia TM + Budżet | 5 narzędzi dostępnych w UI |
| **4** | Wydarzenia + Dashboard | Eventy losowe + KPI tracking |
| **5** | Reputacja + Timeline | Pełny system relacji |
| **6** | Testing + Polish | **MVP READY!** |

---

## 💡 CO ROBI TĘ GRĘ WYJĄTKOWĄ?

### 1. **AI Conversations = Core Gameplay**
Nie klikasz przycisków - **rozmawiasz** z AI jak prawdziwy handlowiec.

### 2. **Długoterminowe relacje**
To nie "sprzedaj i zapomnij" - musisz **utrzymywać** klientów (wizyty regularne, reputacja).

### 3. **Strategiczne decyzje** 🆕
- Budżet 2k PLN - wydasz na gratisy czy POS?
- Odwiedzisz 3 małych (rep=60) czy 1 VIP (rep=90)?
- **Reputacja ogólna:** 1 VIP za 5k ma większą wagę niż 5 małych po 1k!
- Czy odzyskiwać LOST (-30 rep) czy szukać nowych (0 rep)?

### 4. **Emergent gameplay**
Każda rozgrywka inna (losowi klienci, eventy, różne AI responses).

### 5. **Realistic simulation**
Bazuje na prawdziwym FMCG (trade marketing, market share, shelf placement, **portfolio management**).

### 6. **Progresja i sens achievement** 🆕
- Awansowanie wymaga **reputation ≥60** (nie można z "Average")
- Reputation ≥90 = Sales Legend (+500 PLN/m, dostęp do VIP)
- Reputation <40 = Email od szefa: "30 dni na poprawę lub zwolnienie!"

---

## 🎬 DEMO SCENARIO (Dla pokazania klientowi)

**Setup:**
- Gracz = Junior Sales Rep, dzień 1
- Mapa: 20 prospectów w promieniu 30km
- Budżet: 2,000 PLN
- Cel miesiąca: 10,000 PLN

**Pokazujemy:**

1. **Mapa** (30 sec)
   - Pinezki różne kolory
   - Klik → Info o kliencie
   - "Zaplanuj wizytę" → Kalendarz

2. **Kalendarz** (30 sec)
   - Wybór dnia/godziny
   - Energia: 100% → 80% po wizycie
   - Max 3 wizyty/dzień

3. **Wizyta AI** (3 min) ⭐ GŁÓWNA ATRAKCJA
   - Cold call u "Sklep U Janusza"
   - Gracz mówi: "Dzień dobry, jestem z FreshMarket..."
   - AI odpowiada: "Czym się różnicie od konkurencji?"
   - Gracz oferuje: 🎁 Gratis (2 sztuki za darmo)
   - AI: "OK, wezmę 10 sztuk na próbę"
   - **Wynik:** ✅ Kontrakt, 4⭐, +500 PLN

4. **Reputacja** (1 min)
   - Timeline: "2025-10-28: Pierwsza wizyta, +50 rep"
   - Progi: Neutral → Happy (≥50)
   - Za tydzień: Regularna wizyta (+5 rep)

5. **Wydarzenie** (1 min)
   - Popup: "Telefon od klienta - chce promocję"
   - Wybór: Zgoda/Odmowa
   - Konsekwencje: +15 rep lub -5 rep

6. **Dashboard** (1 min)
   - Sprzedaż: 500/10,000 PLN (5%)
   - Kontrakty: 1/10
   - Budżet: 1,650/2,000 PLN
   - **🌟 Reputacja ogólna: 50/100** 🆕 (1 ACTIVE = Janusz rep=50)
   - Alert: "Brawo! Pierwszy kontrakt!"

7. **Reputacja widget** (1 min) 🆕 ⭐ NOWA FUNKCJA
   - Widget: "Twoja reputacja: 50/100 (Solid Rep)"
   - Szczegóły:
     * ACTIVE (1): Janusz = 50/100
     * LOST (0): Brak
   - Tip: "Pozyskaj więcej klientów → wyższa reputacja!"
   - Postęp do awansu: "Potrzebujesz ≥60 do Level 2"

**Total demo:** **8 minut** (idealny pitch!)

---

## 🚀 NEXT STEPS

1. ✅ **Design doc gotowy** (FMCG_GAME_DESIGN.md)
2. ✅ **Plan implementacji** (FMCG_CLIENT_CARD_UPGRADE.md)
3. 🔄 **Teraz:** Zatwierdzenie z klientem
4. ⏳ **Potem:** 6 tygodni implementacji
5. 🎉 **Wynik:** MVP gotowy do beta testów

---

**Pytania do klienta:**

1. Czy balans (2-3 wizyty/dzień, 6-8h/miesiąc) jest OK?
2. Czy narzędzia Trade Marketing są jasne i użyteczne?
3. Czy wydarzenia losowe dodają frajdy czy denerwują?
4. Czy 6 tygodni timeline jest akceptowalne?

**Kontakt:** [Twój email/telefon]
