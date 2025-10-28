# FMCG Simulator - UI Mockups & Visualizations

**Cel:** Szczegółowe wizualizacje każdego ekranu gry dla designera/developera  
**Format:** ASCII art mockups + opisy funkcjonalności

---

## 1. DASHBOARD (Główny Ekran)

```
╔════════════════════════════════════════════════════════════════════════════╗
║  🎮 FMCG SIMULATOR              [Profil: Jan Kowalski] [⚙️ Settings] [❓]  ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌──────────────────────────────────────┐  ┌──────────────────────────┐  ║
║  │ 👤 LEVEL 1: JUNIOR SALESPERSON       │  │ 📅 DZIŚ: 15.11.2025     │  ║
║  │                                      │  │ ⚡ Energia: ████░░ 60%   │  ║
║  │ Postęp do Level 2:                   │  │ 🌤️ Pogoda: Słonecznie   │  ║
║  │ ████████████████░░░░ 75%             │  └──────────────────────────┘  ║
║  │                                      │                                 ║
║  │ ✅ Sprzedaż: 9,200/10,000 PLN       │  ┌──────────────────────────┐  ║
║  │ ✅ Kontrakty: 12/10 DONE ✨          │  │ 💰 FINANSE (m-c)        │  ║
║  │ ⚠️ Rating: 3.9/4.0                   │  │                          │  ║
║  │ ⚠️ Reputation: 58/60                 │  │ PLN: 9,200 (+12% 📈)    │  ║
║  │                                      │  │ Trade Mkt: 1,400/2,000  │  ║
║  │ [Awans możliwy za ~3 dni!] 🎯       │  │ Savings: 600 PLN        │  ║
║  └──────────────────────────────────────┘  └──────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ ⭐ REPUTACJA OGÓLNA: 58/100 (Average ⚠️)                           │  ║
║  │                                                                    │  ║
║  │  [Wykres Timeline - ostatnie 30 dni]                              │  ║
║  │                                                            ╱       │  ║
║  │  60 ┤                                                  ╱╱╱        │  ║
║  │  55 ┤                                          ╱╱╱╱╱╱╱╱            │  ║
║  │  50 ┤                                  ╱╱╱╱╱╱╱                     │  ║
║  │  45 ┤                          ╱╱╱╱╱╱╱                             │  ║
║  │  40 ┤──────────────────────────                                   │  ║
║  │     └────┬────┬────┬────┬────┬────┬────┬────                      │  ║
║  │        15.10  22    29   5.11  12    15                           │  ║
║  │                                                                    │  ║
║  │  Progi:                                                            │  ║
║  │  🔴 <40: At Risk  🟡 40-59: Average  🟢 60-74: Solid  ⭐ 75+: Top │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 📋 ZADANIA (4 aktywne)                              [+Dodaj nowe]  │  ║
║  │                                                                    │  ║
║  │ 🔴 PILNE: Reklamacja - Kaufland                    ⏰ Za 2h        │  ║
║  │    "Ostatnia dostawa - opakowania uszkodzone"                     │  ║
║  │    [🚗 Jedź teraz] [📞 Zadzwoń] [⏰ Odłóż]                        │  ║
║  │                                                                    │  ║
║  │ 🟡 Wizyta regularna - Dino Konstancin              ⏰ Dziś         │  ║
║  │    "Check-in co 14 dni (ostatnia: 13 dni temu)"                   │  ║
║  │    [🚗 Jedź (30 min, -25% ⚡)]                                     │  ║
║  │                                                                    │  ║
║  │ 🟢 Cross-sell: FreshDish → Sklep ABC              ⏰ 7 dni        │  ║
║  │    "Klient ma już 2 produkty, idealny moment!"                    │  ║
║  │    [📄 Szczegóły]                                                 │  ║
║  │                                                                    │  ║
║  │ 🔵 Win-back: Żabka Piaseczno (LOST)                ⏰ 14 dni      │  ║
║  │    "Utracony 21 dni temu - Powód: Zaniedbanie"                    │  ║
║  │    Difficulty: 7.5/10 ⚠️  [📋 Przygotuj ofertę]                  │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🗺️ MAPA TERRITORY                                  [🔍 Zoom In]   │  ║
║  │                                                                    │  ║
║  │            [FOLIUM MAP - INTERACTIVE]                              │  ║
║  │                                                                    │  ║
║  │      🟢 Dino                    🔵 Żabka (NEW)                    │  ║
║  │         📍                         📍                              │  ║
║  │                  🔴 Kaufland! (PILNE)                             │  ║
║  │                      📍                                            │  ║
║  │    🟢 Sklep ABC                                                   │  ║
║  │       📍                  🔵 Biedronka (Prospect)                 │  ║
║  │                              📍                                    │  ║
║  │                                                                    │  ║
║  │  Legend: 🟢 ACTIVE  🔵 PROSPECT  🔴 LOST  ⚠️ TASK URGENT          │  ║
║  │                                                                    │  ║
║  │  [Kliknięcie pina → Quick Info Card]                              │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  [📊 RAPORTY]  [🛠️ TRADE MARKETING]  [👥 KLIENCI]  [🎯 ZADANIA]        ║
╚════════════════════════════════════════════════════════════════════════════╝
```

**Funkcjonalności:**
- **Real-time updates** (energia spada podczas wizyty)
- **Hover tooltips** (np. "Reputation 58 = potrzebujesz +2 do Solid Rep")
- **Click actions** (kliknięcie zadania → szczegóły, kliknięcie pina → client card)
- **Notifications** (🔔 badge gdy nowe zadanie / event)

---

## 2. CLIENT CARD (Szczegóły Klienta)

```
╔════════════════════════════════════════════════════════════════════════════╗
║  👥 KLIENT: Sklep ABC                            [✖️ Zamknij]              ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌──────────────────────────────────────┐  ┌──────────────────────────┐  ║
║  │ 🏪 PODSTAWOWE INFO                   │  │ 📊 QUICK STATS           │  ║
║  │                                      │  │                          │  ║
║  │ Status: 🟢 ACTIVE                    │  │ Revenue: 1,200 PLN/m    │  ║
║  │ Typ: Sklep spożywczy (mały)         │  │ Market Share: 28%       │  ║
║  │ Lokalizacja: Piaseczno, ul. Główna  │  │ Produkty: 2/12          │  ║
║  │ Dystans: 8 km (-20% energia)        │  │ Wizyty: 8 total         │  ║
║  │                                      │  │ Dni współpracy: 45      │  ║
║  │ Właściciel: Pan Kowalski             │  └──────────────────────────┘  ║
║  │ Osobowość: Pragmatyczny, ceni        │                                 ║
║  │             regularność i dobre      │  ┌──────────────────────────┐  ║
║  │             relacje                  │  │ ⭐ REPUTACJA: 70/100    │  ║
║  └──────────────────────────────────────┘  │                          │  ║
║                                             │ Status: Happy Client 😊  │  ║
║  ┌──────────────────────────────────────┐  │                          │  ║
║  │ 📦 PORTFOLIO (2 produkty)            │  │ Trend (30d): +15 pkt 📈 │  ║
║  │                                      │  │                          │  ║
║  │ ✅ FreshSoap                         │  │ Wpływ na Overall:       │  ║
║  │    • Dodany: 01.10.2025              │  │ +0.8 pkt (8% wagi)      │  ║
║  │    • Wolumen: 50 szt/m               │  │                          │  ║
║  │    • Market share: 30%               │  │ [70 = Happy] 😊         │  ║
║  │    • Shelf: Prime (najlepsza)        │  │  ├─ Regularność wizyt  │  ║
║  │                                      │  │  ├─ Szybkie reakcje     │  ║
║  │ ✅ FreshShampoo                      │  │  └─ Cross-sell sukces  │  ║
║  │    • Dodany: 10.10.2025              │  └──────────────────────────┘  ║
║  │    • Wolumen: 30 szt/m               │                                 ║
║  │    • Market share: 25%               │  ┌──────────────────────────┐  ║
║  │    • Shelf: Standard                 │  │ 📅 NASTĘPNA WIZYTA      │  ║
║  │                                      │  │                          │  ║
║  │ [+ Zaproponuj nowy produkt]          │  │ Wymagana: 20.11.2025    │  ║
║  └──────────────────────────────────────┘  │ (za 5 dni)              │  ║
║                                             │                          │  ║
║  ┌──────────────────────────────────────┐  │ [🚗 Umów wizytę teraz]  │  ║
║  │ 📋 TIMELINE (ostatnie 5 eventów)     │  └──────────────────────────┘  ║
║  │                                      │                                 ║
║  │ 📅 12.11.2025                        │  ┌──────────────────────────┐  ║
║  │    ⭐⭐⭐⭐⭐ Wizyta regularna        │  │ 🛠️ DOSTĘPNE AKCJE       │  ║
║  │    +10 rep | "Świetna rozmowa!"     │  │                          │  ║
║  │                                      │  │ [🚗 Wizyta regularna]   │  ║
║  │ 📅 10.11.2025                        │  │ [🆕 Cross-sell]         │  ║
║  │    🆕 Cross-sell FreshShampoo        │  │ [📦 Kontrola ekspozycji]│  ║
║  │    +15 rep | +400 PLN/m              │  │ [📧 Email / SMS]        │  ║
║  │                                      │  │ [📊 Pełny raport]       │  ║
║  │ 📅 05.11.2025                        │  └──────────────────────────┘  ║
║  │    ⭐⭐⭐⭐ Wizyta regularna          │                                 ║
║  │    +5 rep | "Dobra rozmowa"          │                                 ║
║  │                                      │                                 ║
║  │ 📅 01.11.2025                        │                                 ║
║  │    📦 Kontrola ekspozycji            │                                 ║
║  │    +5 rep | Market share +2%         │                                 ║
║  │                                      │                                 ║
║  │ 📅 25.10.2025                        │                                 ║
║  │    ⭐⭐⭐ Wizyta regularna            │                                 ║
║  │    +2 rep | "Neutralna"              │                                 ║
║  │                                      │                                 ║
║  │ [📜 Pokaż pełną historię (45 dni)]   │                                 ║
║  └──────────────────────────────────────┘                                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

**Interakcje:**
- **Hover na produktach** → wykres sprzedaży (30 dni)
- **Kliknięcie timeline event** → pełne detale rozmowy (transkrypt)
- **Drag product** (future) → zmiana kolejności (shelf placement)

---

## 3. AI CONVERSATION SCREEN (Wizyta)

```
╔════════════════════════════════════════════════════════════════════════════╗
║  💬 WIZYTA: Sklep ABC - Wizyta Regularna          ⏱️ 09:23  [⚡ 70% → 50%] ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🏪 Sklep ABC | Pan Kowalski | Reputation: 70/100 (Happy 😊)        │  ║
║  │ Ostatnia wizyta: 10 dni temu (⭐⭐⭐⭐⭐)                           │  ║
║  │                                                                    │  ║
║  │ KONTEKST WIZYTY:                                                   │  ║
║  │ • Cel: Check-in + kontrola ekspozycji FreshSoap                   │  ║
║  │ • Produkty: FreshSoap (50/m), FreshShampoo (30/m)                 │  ║
║  │ • Możliwość: Cross-sell FreshDish (AI podpowie moment)            │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 💬 ROZMOWA                                           [🔇 Mute AI]  │  ║
║  │────────────────────────────────────────────────────────────────────│  ║
║  │                                                                    │  ║
║  │  AI (Pan Kowalski):                                   🕐 09:23    │  ║
║  │  ┌────────────────────────────────────────────────┐               │  ║
║  │  │ Dzień dobry! Miło Pana widzieć ponownie.       │               │  ║
║  │  │ Wszystko w porządku z dostawami?               │               │  ║
║  │  └────────────────────────────────────────────────┘               │  ║
║  │                                                                    │  ║
║  │  TY:                                                  🕐 09:24    │  ║
║  │  ┌────────────────────────────────────────────────┐               │  ║
║  │  │ Dzień dobry! Tak, wszystko OK. Chciałem        │               │  ║
║  │  │ sprawdzić jak sprzedaje się FreshSoap?         │               │  ║
║  │  └────────────────────────────────────────────────┘               │  ║
║  │                                                                    │  ║
║  │  AI (Pan Kowalski):                                   🕐 09:24    │  ║
║  │  ┌────────────────────────────────────────────────┐               │  ║
║  │  │ Całkiem dobrze! Około 50 sztuk miesięcznie.    │               │  ║
║  │  │ Klienci chwalą, ale widzę że Palmolive ma      │               │  ║
║  │  │ promocję - ich sprzedaż wzrosła ostatnio.      │               │  ║
║  │  └────────────────────────────────────────────────┘               │  ║
║  │                                                                    │  ║
║  │  [💡 AI PODPOWIEDŹ: "Konkurencja ma promocję - może zaproponuj    │  ║
║  │      materiały POS lub promocję konsumencką?"]                    │  ║
║  │                                                                    │  ║
║  │  ─────────────────────────────────────────────────────────────    │  ║
║  │                                                                    │  ║
║  │  Twoja odpowiedź:                                                 │  ║
║  │  ┌────────────────────────────────────────────────────────────┐  │  ║
║  │  │ __________________________________________________________  │  │  ║
║  │  │                                                            │  │  ║
║  │  │  [Wpisz swoją odpowiedź...]                               │  │  ║
║  │  │                                                            │  │  ║
║  │  └────────────────────────────────────────────────────────────┘  │  ║
║  │                                                                    │  ║
║  │  [📤 Wyślij (Enter)]  [🛠️ Użyj narzędzia TM]  [📋 Zakończ wizytę] │  ║
║  │                                                                    │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🛠️ TRADE MARKETING TOOLS (Budget: 1,400/2,000 PLN)                │  ║
║  │                                                                    │  ║
║  │ [💰 Rabat -10%] [🎁 Gratis 2+1 - 350 PLN] [📌 POS - 200 PLN]     │  ║
║  │ [🎉 Promocja - 600 PLN] [🚚 Darmowa dostawa - 150 PLN]            │  ║
║  │                                                                    │  ║
║  │ Kliknij aby dodać do oferty (auto-insert do rozmowy)              │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 📊 LIVE SCORING (AI analiza na żywo)                              │  ║
║  │                                                                    │  ║
║  │ Profesjonalizm:        ████████░░ 80%  ✅ Dobry tone              │  ║
║  │ Dopasowanie oferty:    ██████░░░░ 60%  ⚠️ Nie odniosłeś się do   │  ║
║  │                                            konkurencji             │  ║
║  │ Słuchanie klienta:     ██████████ 100% ✅ Świetnie!               │  ║
║  │                                                                    │  ║
║  │ Aktualna prognoza: ⭐⭐⭐⭐ (4/5)                                  │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

**Features:**
- **Real-time AI responses** (streaming like ChatGPT)
- **Live scoring** (aktualizuje się po każdej wiadomości)
- **Contextual hints** (💡 podpowiedzi gdy gracz ugrzęźnie)
- **Tool integration** (kliknięcie narzędzia → auto-insert do tekstu)

---

## 4. VISIT RESULTS SCREEN (Po Rozmowie)

```
╔════════════════════════════════════════════════════════════════════════════╗
║  🎉 WYNIK WIZYTY: Sklep ABC                                                ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║                          ⭐⭐⭐⭐⭐                                         ║
║                                                                            ║
║                   ŚWIETNA WIZYTA! (5/5)                                    ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 📊 FEEDBACK OD AI                                                  │  ║
║  │                                                                    │  ║
║  │ ✅ CO POSZŁO DOBRZE:                                               │  ║
║  │  • Świetnie rozpoznałeś problem z konkurencją                     │  ║
║  │  • Zaproponowałeś materiały POS (konkretne rozwiązanie)           │  ║
║  │  • Ton rozmowy profesjonalny i przyjazny                          │  ║
║  │  • Słuchałeś klienta (pytania otwarte)                            │  ║
║  │                                                                    │  ║
║  │ 💡 CO MOŻNA POPRAWIĆ:                                              │  ║
║  │  • Mógłbyś wcześniej zapytać o konkurencję                        │  ║
║  │  • Cross-sell FreshDish mógł być delikatniejszy (lekka presja)    │  ║
║  │                                                                    │  ║
║  │ 🎯 PODPOWIEDZI NA PRZYSZŁOŚĆ:                                      │  ║
║  │  • Klient wspomniał o "klientach chwalących" - to znak że         │  ║
║  │    możesz śmiało proponować więcej produktów                      │  ║
║  │  • Palmolive to stały konkurent - monitoruj ich promocje          │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🎁 NAGRODY                                                         │  ║
║  │                                                                    │  ║
║  │  💰 PLN/miesiąc:        1,200 PLN (bez zmian)                     │  ║
║  │  ⭐ Reputation:         +10 (70 → 80)  🎉 Happy → Top Performer!  │  ║
║  │  📈 Market Share:       +2% (28% → 30%)                           │  ║
║  │  🆕 Cross-sell sukces:  FreshDish dodany (+400 PLN/m) 💰          │  ║
║  │  🛠️ Trade Marketing:    -200 PLN (POS Materials użyte)            │  ║
║  │                                                                    │  ║
║  │  ───────────────────────────────────────────────────────────────  │  ║
║  │                                                                    │  ║
║  │  BONUS: Klient polecił Cię sąsiadowi! 🎉                          │  ║
║  │  → Nowy PROSPECT: "Sklep XYZ" (interest_level: 70 - warm lead!)  │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 📊 WPŁYW NA OVERALL REPUTATION                                     │  ║
║  │                                                                    │  ║
║  │  Przed wizytą:  58/100 (Average ⚠️)                               │  ║
║  │  Po wizycie:    60/100 (Solid Rep ✅)  🎊 PRÓG PRZEKROCZONY!      │  ║
║  │                                                                    │  ║
║  │  [Wykres animowany: 58 → 60]                                      │  ║
║  │                                                                    │  ║
║  │  🏆 OSIĄGNIĘCIE ODBLOKOWANE:                                       │  ║
║  │     "SOLID REPUTATION" - Możesz teraz awansować do Level 2!       │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 📅 NOWE ZADANIA WYGENEROWANE                                       │  ║
║  │                                                                    │  ║
║  │  ✅ Sklep ABC - Następna wizyta za 14 dni (30.11.2025)            │  ║
║  │  🆕 Sklep XYZ (PROSPECT) - Cold call (polecenie od Sklep ABC)     │  ║
║  │                                                                    │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║               [📊 Zobacz raport]  [🏠 Wróć do Dashboard]                  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

**Animacje:**
- **Stars fly in** (5 gwiazdek pojawiają się jedna po drugiej)
- **Numbers count up** (reputation 70 → 80 animowane)
- **Confetti effect** gdy osiągnięcie odblokowane
- **Sound effects** (ding! dla bonusów)

---

## 5. TRADE MARKETING PANEL

```
╔════════════════════════════════════════════════════════════════════════════╗
║  🛠️ TRADE MARKETING TOOLS                            [✖️ Zamknij]          ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 💰 BUDŻET MIESIĘCZNY                              Reset za: 12 dni │  ║
║  │                                                                    │  ║
║  │  ████████████░░░░░░░░  1,400 / 2,000 PLN (70%)                    │  ║
║  │                                                                    │  ║
║  │  Wydane: 600 PLN  |  Pozostało: 1,400 PLN                         │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🛠️ DOSTĘPNE NARZĘDZIA                                              │  ║
║  │────────────────────────────────────────────────────────────────────│  ║
║  │                                                                    │  ║
║  │  1. 💰 RABAT CENOWY (-10%)                          Koszt: 0 PLN  │  ║
║  │     ┌──────────────────────────────────────────────────────────┐  │  ║
║  │     │ Efekt:   +5 reputation                                   │  │  ║
║  │     │ Marża:   -10% (TRWAŁE!)                                  │  │  ║
║  │     │ Użycie:  Win-back (rekompensata), PROSPECT (last resort) │  │  ║
║  │     │ ROI:     ⚠️ NISKIE (stała strata marży)                  │  │  ║
║  │     │                                                           │  │  ║
║  │     │ Cooldown: Brak (per klient)                              │  │  ║
║  │     │                                                           │  │  ║
║  │     │ [💡 Użyj tylko gdy KONIECZNIE trzeba!]                   │  │  ║
║  │     │ [🚫 NIE polecane dla małych klientów (<1k PLN/m)]        │  │  ║
║  │     └──────────────────────────────────────────────────────────┘  │  ║
║  │     [➕ Użyj dla klienta...]                                       │  ║
║  │                                                                    │  ║
║  │  2. 🎁 GRATIS (2+1)                                 Koszt: 350 PLN │  ║
║  │     ┌──────────────────────────────────────────────────────────┐  │  ║
║  │     │ Efekt:   +8 reputation, +20-25% szans na sukces          │  │  ║
║  │     │ Czas:    Instant (jednorazowy)                           │  │  ║
║  │     │ Użycie:  Win-back, PROSPECT (2. wizyta), Cross-sell      │  │  ║
║  │     │ ROI:     ⭐⭐⭐⭐⭐ WYSOKIE (konkretna korzyść)         │  │  ║
║  │     │                                                           │  │  ║
║  │     │ Cooldown: 30 dni (per klient)                            │  │  ║
║  │     │                                                           │  │  ║
║  │     │ Historia użyć (ostatnie 30 dni):                         │  │  ║
║  │     │ • 05.11 - Sklep ABC (PROSPECT) → SUKCES ✅               │  │  ║
║  │     │ • 12.11 - Kaufland (Win-back) → W TOKU 🔄               │  │  ║
║  │     │                                                           │  │  ║
║  │     │ [✅ Bardzo uniwersalne - świetny wybór!]                 │  │  ║
║  │     └──────────────────────────────────────────────────────────┘  │  ║
║  │     [➕ Użyj dla klienta...]                                       │  ║
║  │                                                                    │  ║
║  │  3. 📌 MATERIAŁY POS                               Koszt: 200 PLN │  ║
║  │     ┌──────────────────────────────────────────────────────────┐  │  ║
║  │     │ Efekt:   +5 reputation, +15% sprzedaż (30 dni)           │  │  ║
║  │     │ Czas:    30 dni (długoterminowy efekt)                   │  │  ║
║  │     │ Użycie:  ACTIVE (kontrola ekspozycji), Cross-sell        │  │  ║
║  │     │ ROI:     ⭐⭐⭐⭐ BARDZO WYSOKIE (najlepszy ROI)        │  │  ║
║  │     │                                                           │  │  ║
║  │     │ Cooldown: 60 dni (per klient - efekt trwa długo)         │  │  ║
║  │     │                                                           │  │  ║
║  │     │ [💡 Best practice: Użyj PRZED cross-sellem!]            │  │  ║
║  │     │ [📈 Boost sprzedaży = lepsze argumenty do rozbudowy]     │  │  ║
║  │     └──────────────────────────────────────────────────────────┘  │  ║
║  │     [➕ Użyj dla klienta...]                                       │  ║
║  │                                                                    │  ║
║  │  4. 🎉 PROMOCJA KONSUMENCKA                        Koszt: 600 PLN │  ║
║  │     ┌──────────────────────────────────────────────────────────┐  │  ║
║  │     │ Efekt:   +10 reputation, +30% sprzedaż (14 dni)          │  │  ║
║  │     │ Czas:    14 dni (krótki burst)                           │  │  ║
║  │     │ Użycie:  ACTIVE (słaba rotacja), Nowy produkt            │  │  ║
║  │     │ ROI:     ⭐⭐⭐ ŚREDNIE (drogi, ale efektowny)          │  │  ║
║  │     │                                                           │  │  ║
║  │     │ Cooldown: 90 dni (per klient - nie spamować!)            │  │  ║
║  │     │                                                           │  │  ║
║  │     │ [⚠️ DROGI! Użyj tylko gdy problem z rotacją]            │  │  ║
║  │     │ [🎯 Idealny dla launch nowego produktu]                 │  │  ║
║  │     └──────────────────────────────────────────────────────────┘  │  ║
║  │     [➕ Użyj dla klienta...]                                       │  ║
║  │                                                                    │  ║
║  │  5. 🚚 DARMOWA DOSTAWA                             Koszt: 150 PLN │  ║
║  │     ┌──────────────────────────────────────────────────────────┐  │  ║
║  │     │ Efekt:   +3 reputation, +15% szans na sukces             │  │  ║
║  │     │ Czas:    Jednorazowy (uprzejmość)                        │  │  ║
║  │     │ Użycie:  Win-back (ułatwienie), ACTIVE (goodwill)        │  │  ║
║  │     │ ROI:     ⭐⭐ NISKIE (ale tani gesture)                  │  │  ║
║  │     │                                                           │  │  ║
║  │     │ Cooldown: 30 dni (per klient)                            │  │  ║
║  │     │                                                           │  │  ║
║  │     │ [💡 Combo z innym narzędziem = lepszy efekt]            │  │  ║
║  │     │ [😊 Buduje goodwill bez dużego kosztu]                  │  │  ║
║  │     └──────────────────────────────────────────────────────────┘  │  ║
║  │     [➕ Użyj dla klienta...]                                       │  ║
║  │                                                                    │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 📊 ANALYTICS (Ten miesiąc)                                         │  ║
║  │                                                                    │  ║
║  │  Narzędzi użytych: 3                                              │  ║
║  │  Wydane: 600 PLN                                                   │  ║
║  │  Średni ROI: 2,100% 🚀                                             │  ║
║  │                                                                    │  ║
║  │  Najlepsze: Gratis (2x sukces)                                    │  ║
║  │  Najsłabsze: Rabat (użyty 0x - DOBRZE!)                           │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

**Interakcje:**
- **Hover na narzędziu** → pełny opis + ROI calculator
- **Kliknięcie "Użyj"** → wybierz klienta z listy
- **Cooldown visualization** → progress bar gdy narzędzie na cooldown

---

[KONTYNUACJA - Część 3: Więcej ekranów (Calendar, Reports, Settings)]
