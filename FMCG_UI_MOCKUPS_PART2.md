# FMCG Simulator - UI Mockups CZĘŚĆ 2

## 6. CALENDAR VIEW (Planowanie Tygodnia)

```
╔════════════════════════════════════════════════════════════════════════════╗
║  📅 KALENDARZ - Tydzień 15-21 Listopada 2025        [◀️ Poprzedni] [Następny ▶️] ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬────┐ ║
║  │  PON     │  WT      │  ŚR      │  CZW     │  PT      │  SOB     │ ND │ ║
║  │  15.11   │  16.11   │  17.11   │  18.11   │  19.11   │  20.11   │21  │ ║
║  ├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼────┤ ║
║  │ ⚡ 100% │ ⚡ 85%  │ ⚡ 90%  │ ⚡ 70%  │ ⚡ 80%  │ 🚫 OFF  │🚫 │ ║
║  │          │          │          │          │          │          │    │ ║
║  │ 9:00     │ 9:00     │ 9:00     │ 10:00    │ 9:00     │          │    │ ║
║  │ 🔴 PILNE │ 🟢 Sklep │ 🟡 Dino  │ 🔵 NEW   │ 📊 Raport│          │    │ ║
║  │ Kaufland │   ABC    │ Konstanc.│ Żabka    │ tygodniow│          │    │ ║
║  │ (Rekl.)  │ (Reg.)   │ (Cross)  │ (Cold)   │          │          │    │ ║
║  │          │          │          │          │          │          │    │ ║
║  │ 14:00    │ 14:00    │ 14:00    │ 15:00    │ 14:00    │          │    │ ║
║  │ 🟡 Sklep │ 📦 Kontr │ 🚨 PILNE │ 🟢 Follow│ 🟡 XYZ   │          │    │ ║
║  │   XYZ    │   ekspo  │ Problem  │   up     │ (Reg.)   │          │    │ ║
║  │ (Reg.)   │   Dino   │ Sklep C  │ Kaufland │          │          │    │ ║
║  │          │          │          │          │          │          │    │ ║
║  │ 16:00    │          │          │          │          │          │    │ ║
║  │ 📧 Email │          │          │          │          │          │    │ ║
║  │ (Admin)  │          │          │          │          │          │    │ ║
║  │          │          │          │          │          │          │    │ ║
║  │ ────────│ ────────│ ────────│ ────────│ ────────│          │    │ ║
║  │ Tasks: 3 │ Tasks: 2 │ Tasks: 2 │ Tasks: 2 │ Tasks: 2 │   REST   │REST│ ║
║  │ ⏱️ 40min│ ⏱️ 35min│ ⏱️ 35min│ ⏱️ 30min│ ⏱️ 25min│          │    │ ║
║  └──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴────┘ ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 📋 LEGENDA                                                         │  ║
║  │                                                                    │  ║
║  │ 🔴 PILNE (deadline dziś/jutro)   🟡 ŚREDNIE (deadline 3-7 dni)    │  ║
║  │ 🟢 NISKIE (deadline >7 dni)      🔵 NOWE (świeżo dodane)          │  ║
║  │ 📦 Operacyjne  🚨 Awaryjne  📧 Admin  📊 Raport                   │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🎯 PODSUMOWANIE TYGODNIA                                           │  ║
║  │                                                                    │  ║
║  │ Total zadań: 11                                                    │  ║
║  │ • PILNE: 2  🔴                                                     │  ║
║  │ • Wizyty regularne: 5  🟡                                          │  ║
║  │ • Cross-sell: 1  🟢                                                │  ║
║  │ • Cold call: 1  🔵                                                 │  ║
║  │ • Operacyjne: 1  📦                                                │  ║
║  │ • Admin: 1  📧                                                     │  ║
║  │                                                                    │  ║
║  │ Szacowany czas: 2h 45min (~33 min/dzień)                          │  ║
║  │ Energia potrzebna: 380% (avg 76%/dzień - OK! ✅)                  │  ║
║  │                                                                    │  ║
║  │ ⚠️ UWAGA: Środa jest mocno obciążona (2 pilne!) - rozważ         │  ║
║  │           przesunięcie "Problem Sklep C" na czwartek               │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  [➕ Dodaj zadanie]  [📥 Import z CRM]  [🔀 Reorganizuj]  [🖨️ Drukuj]   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

**Features:**
- **Drag & drop** zadań między dniami (reorganizacja)
- **Color coding** (priorytet wizualny)
- **Energia tracking** (ostrzeżenie gdy przekroczony 100%/dzień)
- **Smart suggestions** (AI podpowiada optymalne rozplanowanie)

---

## 7. CLIENT LIST VIEW (Przegląd Wszystkich Klientów)

```
╔════════════════════════════════════════════════════════════════════════════╗
║  👥 KLIENCI (15 total)              [🔍 Szukaj...] [🗂️ Filtruj] [+ Dodaj]  ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  [Wszyscy] [🟢 ACTIVE: 8] [🔵 PROSPECT: 5] [🔴 LOST: 2]                   ║
║                                                                            ║
║  Sortuj: [💰 PLN/m ▼] [⭐ Reputation] [📅 Ostatnia wizyta] [📍 Dystans]   ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🟢 Sklep ABC                                        💰 1,200 PLN/m │  ║
║  │ ⭐ 80/100 (Top Performer 🎖️)    📍 8km    📅 Ostatnia: 3 dni temu  │  ║
║  │ ────────────────────────────────────────────────────────────────  │  ║
║  │ Produkty: FreshSoap, FreshShampoo (2/12)                          │  ║
║  │ Market share: 30% (+2% vs m-c wcześniej) 📈                       │  ║
║  │ Następna wizyta: Za 11 dni (26.11)                                │  ║
║  │                                                                    │  ║
║  │ [🚗 Wizyta] [📧 Email] [📊 Raport] [📋 Szczegóły]                 │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🟢 Dino Konstancin                                  💰 2,500 PLN/m │  ║
║  │ ⭐ 65/100 (Happy 😊)             📍 12km   📅 Ostatnia: 7 dni temu │  ║
║  │ ────────────────────────────────────────────────────────────────  │  ║
║  │ Produkty: FreshSoap, FreshMilk, FreshYogurt (3/12)               │  ║
║  │ Market share: 22% (-3% vs m-c wcześniej) ⚠️ SPADEK!              │  ║
║  │ Następna wizyta: OVERDUE! (14 dni temu) 🔴                        │  ║
║  │                                                                    │  ║
║  │ ⚠️ ALERT: Brak wizyty >14 dni! Reputation zagrożone (-5 rep/tyg)  │  ║
║  │                                                                    │  ║
║  │ [🚗 PILNA WIZYTA!] [📧 Email] [📊 Raport] [📋 Szczegóły]          │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🔵 Żabka Konstancin (PROSPECT)                      💰 Est. 800 PLN│  ║
║  │ 🎯 Interest: 70/100 (Wysoki!)   📍 5km    📅 Wizyty: 1 (cold call)│  ║
║  │ ────────────────────────────────────────────────────────────────  │  ║
║  │ Ostatnia rozmowa: 12.11 (4⭐) - "Zainteresowany, wymaga 2. wizyty"│  ║
║  │ Sugestia: Użyj Gratis (2+1) w następnej wizycie (+25% szans!) 💡 │  ║
║  │                                                                    │  ║
║  │ [🚗 2. Wizyta] [📧 Follow-up] [📋 Szczegóły]                      │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🔴 Kaufland Piaseczno (LOST)                        💰 Was: 5,000  │  ║
║  │ ⚠️ Rep: -30/100 (Lost)          📍 15km   📅 Utracony: 30 dni temu│  ║
║  │ ────────────────────────────────────────────────────────────────  │  ║
║  │ Powód: "Zaniedbanie - brak wizyt przez 6 tygodni"                 │  ║
║  │ Win-back attempts: 1/3 (ostatnia: 20.11, wynik: 4⭐ "Rozważa")    │  ║
║  │ Difficulty: 8.0/10 (Bardzo trudne) 💀                             │  ║
║  │                                                                    │  ║
║  │ 💡 Sugestia: Poczekaj 14 dni (czas goi rany), użyj Gratis +       │  ║
║  │             Darmowa dostawa w następnej próbie                     │  ║
║  │                                                                    │  ║
║  │ [🔄 Win-back] [❌ Zrezygnuj] [📋 Szczegóły]                        │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ... [Przewiń aby zobaczyć więcej - 11 klientów pozostało]                ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 📊 QUICK STATS                                                     │  ║
║  │                                                                    │  ║
║  │ Total revenue: 12,300 PLN/m                                       │  ║
║  │ Avg reputation: 58/100 (Average ⚠️)                               │  ║
║  │ Market share avg: 26%                                              │  ║
║  │ Klienci z OVERDUE: 1 🔴                                            │  ║
║  │ Win-back opportunities: 2 (wartość: 8,000 PLN/m!)                 │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

**Features:**
- **Real-time alerts** (OVERDUE wizyty czerwone)
- **Smart suggestions** (AI podpowiada narzędzia TM)
- **Quick actions** (Wizyta / Email bez otwierania szczegółów)
- **Batch operations** (future: wybierz 5 klientów → wyślij email)

---

## 8. WEEKLY REPORT (Podsumowanie Tygodnia)

```
╔════════════════════════════════════════════════════════════════════════════╗
║  📊 RAPORT TYGODNIOWY - 15-21 Listopada 2025                               ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🎯 KLUCZOWE METRYKI                                                │  ║
║  │                                                                    │  ║
║  │  💰 Sprzedaż:           +1,600 PLN/m (nowy kontrakt + cross-sell) │  ║
║  │  ⭐ Reputation ogólna:  58 → 62 (+4 pkt) 📈 SOLID REP! ✅         │  ║
║  │  📅 Wizyt wykonanych:   12 / 12 (100% completion!) 🎉            │  ║
║  │  🏆 Średnia ocena:      4.2⭐ (wyżej niż target 4.0!)             │  ║
║  │  🛠️ Budget TM:          Wykorzystane: 750/2,000 PLN (38%)         │  ║
║  │                                                                    │  ║
║  │  ───────────────────────────────────────────────────────────────  │  ║
║  │                                                                    │  ║
║  │  🎊 OSIĄGNIĘCIA:                                                   │  ║
║  │  ✅ "SOLID REPUTATION" - Reputation ≥60!                          │  ║
║  │  ✅ "PERFECT WEEK" - Wszystkie zadania wykonane!                  │  ║
║  │  ✅ "TOP PERFORMER" - 3 wizyty 5⭐ pod rząd!                       │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 📈 WYKRES REPUTACJI (ostatnie 4 tygodnie)                          │  ║
║  │                                                                    │  ║
║  │  70 ┤                                                      ╱       │  ║
║  │  65 ┤                                              ╱╱╱╱╱╱╱        │  ║
║  │  60 ┤                                      ╱╱╱╱╱╱╱ ← SOLID REP    │  ║
║  │  55 ┤                              ╱╱╱╱╱╱╱                         │  ║
║  │  50 ┤                      ╱╱╱╱╱╱╱                                 │  ║
║  │  45 ┤──────────────────────                                       │  ║
║  │     └────┬────┬────┬────┬────┬────                                │  ║
║  │       Tydz.1  2    3    4(teraz)                                  │  ║
║  │                                                                    │  ║
║  │  Trend: +17 pkt w 4 tygodnie 🚀 (Excellent progress!)             │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🏆 TOP PERFORMERS (Klienci)                                        │  ║
║  │                                                                    │  ║
║  │  🥇 Sklep ABC - 80/100 rep (+10 ten tydzień) - Cross-sell sukces! │  ║
║  │  🥈 Dino Konstancin - 65/100 rep (+5) - Dobra współpraca          │  ║
║  │  🥉 Żabka Konstancin - NOWY KONTRAKT! 🎉 50/100 rep (start)       │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ ⚠️ AREAS FOR IMPROVEMENT                                           │  ║
║  │                                                                    │  ║
║  │  🔴 Kaufland (LOST) - 2. próba win-back nieudana (3⭐)             │  ║
║  │     → Sugestia: Poczekaj 30 dni, przygotuj lepszą ofertę          │  ║
║  │                                                                    │  ║
║  │  🟡 Biedronka (PROSPECT) - 3. wizyta, ciągle brak kontraktu (2⭐)  │  ║
║  │     → Sugestia: Może nie warto dalej próbować? (3/3 wizyty)       │  ║
║  │                                                                    │  ║
║  │  🟡 Sklep XYZ - Spadek market share 28% → 25% (-3%)                │  ║
║  │     → Sugestia: Kontrola ekspozycji + materiały POS                │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 💡 REKOMENDACJE NA NASTĘPNY TYDZIEŃ                                │  ║
║  │                                                                    │  ║
║  │  1. Focus na Sklep XYZ (kontrola ekspozycji - pilne!)             │  ║
║  │  2. Win-back Kaufland - ostatnia próba (3/3) - użyj WSZYSTKICH    │  ║
║  │     narzędzi TM (Gratis + Darmowa dostawa + Rabat jeśli trzeba)   │  ║
║  │  3. Cross-sell u Dino - reputation 65 = dobry moment               │  ║
║  │  4. Cold call nowi PROSPECT (2 nowych w territory)                │  ║
║  │  5. Utrzymaj tempo - 12 wizyt/tydzień = świetny rhythm!           │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 📧 EMAIL OD SZEFA                                                  │  ║
║  │                                                                    │  ║
║  │  Od: Marek Kowalski (Regional Manager)                            │  ║
║  │  Temat: Świetny tydzień! 🎉                                        │  ║
║  │                                                                    │  ║
║  │  "Jan, widzę że osiągnąłeś Solid Reputation (62/100) - gratuluję!│  ║
║  │   Nowy kontrakt z Żabką to dobry ruch. Zwróć uwagę na Sklep XYZ  │  ║
║  │   - spadek market share może oznaczać problem. Trzymaj tempo!"    │  ║
║  │                                                                    │  ║
║  │  [📧 Odpowiedz]                                                    │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  [🖨️ Drukuj]  [📧 Wyślij do managera]  [💾 Zapisz PDF]  [🏠 Dashboard]  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

**Features:**
- **Automated insights** (AI analizuje trendy, podaje rekomendacje)
- **Manager feedback** (symulowany email od szefa - realistic!)
- **Achievements** (gamification - badges za milestones)
- **Comparative charts** (tydzień vs tydzień, miesiąc vs miesiąc)

---

## 9. LEVEL UP SCREEN (Awans)

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                                                                            ║
║                         🎊🎊🎊🎊🎊🎊🎊                                    ║
║                                                                            ║
║                    GRATULACJE! AWANSOWAŁEŚ!                               ║
║                                                                            ║
║                     LEVEL 1 ──────────▶ LEVEL 2                           ║
║                   (Junior)            (Mid Salesperson)                    ║
║                                                                            ║
║                         🎊🎊🎊🎊🎊🎊🎊                                    ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🏆 OSIĄGNIĘCIA (LEVEL 1)                                           │  ║
║  │                                                                    │  ║
║  │  ✅ Sprzedaż:      10,200 / 10,000 PLN ✨                          │  ║
║  │  ✅ Kontrakty:     12 / 10 ✨                                      │  ║
║  │  ✅ Avg rating:    4.1 / 4.0 ✨                                    │  ║
║  │  ✅ Reputation:    62 / 60 ✨                                      │  ║
║  │                                                                    │  ║
║  │  Czas gry: 28 dni (4 tygodnie)                                    │  ║
║  │  Total wizyt: 52                                                   │  ║
║  │  Success rate: 78% (bardzo dobry wynik!)                          │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🆙 CO SIĘ ZMIENIA NA LEVEL 2?                                      │  ║
║  │                                                                    │  ║
║  │  📈 WIĘKSZE MOŻLIWOŚCI:                                            │  ║
║  │  • Territory: 15 → 25 klientów 🗺️                                 │  ║
║  │  • Portfolio: 6 → 12 produktów 📦                                 │  ║
║  │  • Budget TM: 2,000 → 3,500 PLN/m 💰                              │  ║
║  │  • Max task queue: 5 → 10 zadań 📋                                │  ║
║  │                                                                    │  ║
║  │  🎯 NOWE WYZWANIA:                                                 │  ║
║  │  • Sieci handlowe (Kaufland, Tesco, Carrefour)                    │  ║
║  │  • Konkurencja aktywna (Palmolive, Nivea walczą o klientów!)      │  ║
║  │  • Seasonal trends (lato/zima wpływają na sprzedaż)               │  ║
║  │  • Targety kwartalne (Boss oczekuje wyników!)                     │  ║
║  │                                                                    │  ║
║  │  💡 NOWE MECHANIKI:                                                │  ║
║  │  • Key Account Management (VIP klienci, specjalne traktowanie)    │  ║
║  │  • Competitor analysis (śledź co robi konkurencja)                │  ║
║  │  • Seasonal events (targi branżowe, konferencje)                  │  ║
║  │  • Advanced analytics (predykcje, forecasting)                    │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🎁 NAGRODY ZA AWANS                                                │  ║
║  │                                                                    │  ║
║  │  🏅 Badge: "MID SALESPERSON" (visible on profile)                 │  ║
║  │  💰 Bonus: +500 PLN do budżetu TM (jednorazowy)                   │  ║
║  │  🚗 Nowy samochód: -5% koszt energii (szybszy, nowszy model!)     │  ║
║  │  📊 Unlock: Advanced reports (predykcje, trend analysis)          │  ║
║  │  🎯 Unlock: 10 nowych klientów PROSPECT (większy territory)       │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 📧 EMAIL OD SZEFA                                                  │  ║
║  │                                                                    │  ║
║  │  Od: Marek Kowalski (Regional Manager)                            │  ║
║  │  Temat: AWANS! 🎉                                                  │  ║
║  │                                                                    │  ║
║  │  "Jan, świetna robota w ostatnim miesiącu! Awans na Level 2       │  ║
║  │   w 4 tygodnie to doskonały wynik. Nowe wyzwania czekają -        │  ║
║  │   sieci handlowe są trudniejsze, ale Ty sobie poradzisz.          │  ║
║  │   Target na Q1: 25,000 PLN/m sprzedaży. Powodzenia!"              │  ║
║  │                                                                    │  ║
║  │  - Marek                                                           │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ 🎯 CEL LEVEL 2 (MID → SENIOR)                                      │  ║
║  │                                                                    │  ║
║  │  Wymagania:                                                        │  ║
║  │  • Sprzedaż:      25,000 PLN/m                                     │  ║
║  │  • Kontrakty:     20 aktywnych                                     │  ║
║  │  • Avg rating:    4.3⭐                                            │  ║
║  │  • Reputation:    70/100 (Happy Client avg)                       │  ║
║  │  • Key Accounts:  3 sieci handlowe (>5k PLN/m każda)              │  ║
║  │                                                                    │  ║
║  │  Szacowany czas: 8 tygodni                                         │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
║           [🎊 KONTYNUUJ GRĘ]           [📊 Zobacz statystyki]             ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
```

**Animacje:**
- **Confetti explosion** (particles falling)
- **Level badge fly-in** (smooth animation)
- **Numbers count-up** (10,200 liczy się od 0)
- **Sound:** Triumphant music clip (opt-in)

---

## 10. TUTORIAL / ONBOARDING (First-Time User)

```
╔════════════════════════════════════════════════════════════════════════════╗
║  🎓 TUTORIAL - WITAMY W FMCG SIMULATOR!                  [⏭️ Pomiń] (1/8)  ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │                                                                    │  ║
║  │                  👋 WITAJ, JAN KOWALSKI!                           │  ║
║  │                                                                    │  ║
║  │  Jesteś nowym handlowcem w firmie FreshMarket.                    │  ║
║  │  Twoje zadanie: Zbudować silne portfolio klientów w regionie      │  ║
║  │  Piaseczno i awansować do pozycji Mid Salesperson!                │  ║
║  │                                                                    │  ║
║  │  ───────────────────────────────────────────────────────────────  │  ║
║  │                                                                    │  ║
║  │  🎯 CEL (Level 1 → Level 2):                                       │  ║
║  │  • Osiągnij 10,000 PLN/m sprzedaży                                │  ║
║  │  • Podpisz 10 kontraktów                                           │  ║
║  │  • Utrzymaj średnią ocenę 4.0⭐                                    │  ║
║  │  • Zbuduj reputację ≥60/100                                        │  ║
║  │                                                                    │  ║
║  │  Szacowany czas: ~4 tygodnie (30 min/dzień)                       │  ║
║  │                                                                    │  ║
║  │  [NASTĘPNY KROK ▶️]                                                │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

──────────────────────────────────────────────────────────────────────────────

╔════════════════════════════════════════════════════════════════════════════╗
║  🎓 TUTORIAL - MAPA TERRITORY                            [⏭️ Pomiń] (2/8)  ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  🗺️ TWOJE TERRITORY: PIASECZNO                                     │  ║
║  │                                                                    │  ║
║  │        [MAPA z pinami - HIGHLIGHTED]                               │  ║
║  │                                                                    │  ║
║  │            🟢 ← To są Twoi klienci ACTIVE                         │  ║
║  │            🔵 ← To są PROSPECT (potencjalni klienci)              │  ║
║  │            🔴 ← To są LOST (utraceni, do odzyskania)              │  ║
║  │                                                                    │  ║
║  │  ───────────────────────────────────────────────────────────────  │  ║
║  │                                                                    │  ║
║  │  💡 TIP: Kliknij pin aby zobaczyć szczegóły klienta                │  ║
║  │          Dystans wpływa na koszt energii (dalej = drożej!)        │  ║
║  │                                                                    │  ║
║  │  [◀️ POPRZEDNI]  [NASTĘPNY ▶️]                                     │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

──────────────────────────────────────────────────────────────────────────────

╔════════════════════════════════════════════════════════════════════════════╗
║  🎓 TUTORIAL - ENERGIA & WIZYTY                          [⏭️ Pomiń] (3/8)  ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  ⚡ SYSTEM ENERGII                                                  │  ║
║  │                                                                    │  ║
║  │  Każdy dzień masz 100% energii                                     │  ║
║  │  ████████████████████ 100%                                         │  ║
║  │                                                                    │  ║
║  │  Wizyty kosztują energię:                                          │  ║
║  │  • Bliska wizyta (5-10km):  -20% ⚡                                │  ║
║  │  • Daleka wizyta (20-30km): -30% ⚡                                │  ║
║  │  • Lunch break:             +15% ⚡                                │  ║
║  │                                                                    │  ║
║  │  ───────────────────────────────────────────────────────────────  │  ║
║  │                                                                    │  ║
║  │  Wynik: Możesz zrobić 2-3 wizyty dziennie + kilka małych zadań    │  ║
║  │                                                                    │  ║
║  │  💡 TIP: Planuj wizyty mądrze! Grupuj bliskie klienty razem       │  ║
║  │                                                                    │  ║
║  │  [◀️ POPRZEDNI]  [NASTĘPNY ▶️]                                     │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

──────────────────────────────────────────────────────────────────────────────

╔════════════════════════════════════════════════════════════════════════════╗
║  🎓 TUTORIAL - TWOJA PIERWSZA WIZYTA!                    [⏭️ Pomiń] (4/8)  ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │  🚗 CZAS NA PRAKTYKĘ!                                              │  ║
║  │                                                                    │  ║
║  │  Zrobimy teraz symulowaną wizytę u klienta PROSPECT:              │  ║
║  │  "Sklep ABC" (Pan Kowalski)                                       │  ║
║  │                                                                    │  ║
║  │  Cel: Podpisać pierwszy kontrakt na FreshSoap                     │  ║
║  │                                                                    │  ║
║  │  ───────────────────────────────────────────────────────────────  │  ║
║  │                                                                    │  ║
║  │  💡 TIPS:                                                          │  ║
║  │  • Zacznij od pytania otwartego (nie od sprzedaży!)               │  ║
║  │  • Słuchaj klienta - AI podpowie co jest ważne                    │  ║
║  │  • Dopasuj ofertę do potrzeb                                       │  ║
║  │  • Nie bój się błędów - to trening! 😊                            │  ║
║  │                                                                    │  ║
║  │  [🚗 ROZPOCZNIJ WIZYTĘ]                                            │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

... [Dalsze kroki: Reputacja, Trade Marketing, Wydarzenia, Zakończenie]
```

**Tutorial flow:**
1. Intro (cele, czas gry)
2. Mapa (territory, piny)
3. Energia (balance, planowanie)
4. **PRAKTYKA** - Pierwsza wizyta (guided)
5. Wynik wizyty (feedback, rewards)
6. Reputacja (2-tier system)
7. Trade Marketing (narzędzia)
8. Dashboard tour (gdzie co jest)

---

**KONIEC WIZUALIZACJI UI**

Łącznie stworzyłem **10 szczegółowych mockupów** ekranów:
1. ✅ Dashboard (główny ekran)
2. ✅ Client Card (szczegóły klienta)
3. ✅ AI Conversation (wizyta)
4. ✅ Visit Results (podsumowanie)
5. ✅ Trade Marketing Panel
6. ✅ Calendar View
7. ✅ Client List
8. ✅ Weekly Report
9. ✅ Level Up Screen
10. ✅ Tutorial/Onboarding

**Następny krok:** Diagram flow gry (journey gracza od start do Level 2)
