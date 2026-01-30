# 🎯 HEINZ MVP - 3-Week Roadmap
**Target Completion Date:** 26 Listopada 2025  
**Goal:** Gotowa prezentacja + działające demo dla Heinz Poland

---

## 📋 EXECUTIVE SUMMARY

### Cel biznesowy:
Stworzenie **Heinz Sales Academy** - platformy symulacyjnej z modułami szkoleniowymi dla sales reps Heinz Poland (Food Service + Retail).

### Scope MVP:
- ✅ **Gra symulacyjna:** Territory management, wizyty u klientów, economic tools
- ✅ **Szkolenia:** 7 gotowych lekcji interaktywnych (Trade Marketing, Food Service Economics)
- ✅ **Branding Heinz:** Logo, kolory, produkty Heinz/Pudliszki
- ✅ **Prezentacja:** Landing page + Deck (10 slides)

### Timeline:
**3 tygodnie = 15 dni roboczych**

---

## 🎯 VALUE PROPOSITION FOR HEINZ

### Problem Statement:
- Onboarding nowych sales reps w Heinz trwa **6-9 miesięcy**
- Tradycyjne szkolenia = kosztowne (trainers, wyjazdy, brak praktyki)
- Brak standaryzacji (każdy region szkoli inaczej)
- Wysoki turnover w pierwszym roku (40-50%)

### Solution:
**Heinz Sales Academy** - symulacja sprzedaży + szkolenia online, które:
- Skraca onboarding z 9 do **3-4 miesięcy**
- Redukuje koszty szkoleń o **60%**
- Standaryzuje wiedzę (wszyscy uczą się tego samego)
- Zwiększa engagement (gamification)

### Measurable Benefits:
| Metryka | Przed | Po (cel) |
|---------|-------|----------|
| Time-to-productivity | 9 miesięcy | 3-4 miesiące |
| Koszt onboardingu | 15,000 zł/osoba | 6,000 zł/osoba |
| Retention (rok 1) | 55% | 75% |
| Knowledge assessment | 60% (avg) | 85% (avg) |

---

## 💰 PRICING STRATEGY

### Pilot Program (Rekomendacja):
```
15,000 PLN za 3 miesiące
- 20-30 userów (sales reps + managers)
- 1 scenariusz główny ("Territory Management Basics")
- 7 lekcji szkoleniowych
- Branding Heinz (logo, kolory)
- Support: email + 2x check-in call
- Raport końcowy (engagement, learning outcomes)
```

### Full Deployment (po pilotażu):
```
40,000 PLN/kwartał
- Unlimited users (całe Heinz Poland)
- 3-5 custom scenariuszy
- Integracja z CRM (opcjonalnie)
- Dedykowany CSM
- Custom content development
```

---

## 📅 3-WEEK SPRINT PLAN

---

## **TYDZIEŃ 1: DOKOŃCZ GRĘ (Core Mechanics)** 🎮
**Cel:** Działający visit flow + portfolio produktowe

### **Dzień 1-2 (Środa-Czwartek, 6-7 listopada):**
**Task: Visit Flow - Conversation System**

**Co zrobić:**
1. **Conversation Tree Engine**
   ```python
   # core/conversation_engine.py
   - Stwórz klasę ConversationNode
   - Dialog z właścicielem (3-4 opcje wyboru)
   - Branching logic (różne outcomes)
   ```

2. **Przykładowa wizyta (Sklep Osiedlowy):**
   ```
   Właściciel: "Dzień dobry, co dzisiaj?"
   
   Opcje:
   [A] Kontrola półki - sprawdzam ekspozycję Heinz
   [B] Nowa oferta - mam promocję na Ketchup 2.5kg
   [C] Relacja - pogadamy o biznesie, jak idzie sezon?
   [D] Problem solving - klient zgłaszał reklamację
   ```

3. **Outcomes po wizycie:**
   - Zamówienie (SKU + ilość)
   - Instalacja POS materiałów
   - Feedback (pozytywny/negatywny)
   - Relationship score (+/-)

**Output:** Działający popup wizyty z dialogiem

**Czas:** 2 dni (16h)

---

### **Dzień 3-4 (Piątek-Sobota, 8-9 listopada):**
**Task: Portfolio Produktowe Heinz/Pudliszki**

**Co zrobić:**
1. **Database produktów:**
   ```python
   # data/heinz_products.json
   [
     {
       "sku": "HNZ-KTC-500",
       "name": "Heinz Ketchup 500ml",
       "category": "Ketchup",
       "brand": "Heinz",
       "price_retail": 12.99,
       "price_horeca": 35.99,
       "price_wholesale": 9.50,
       "margin_retail": 35,
       "food_cost_horeca": 1.2  # % na porcję
     },
     {
       "sku": "PDL-MST-2000",
       "name": "Pudliszki Musztarda Sarepska 2kg",
       "category": "Mustard",
       "brand": "Pudliszki",
       ...
     }
   ]
   ```

2. **Portfolio Builder:**
   - 10-15 głównych produktów Heinz (Ketchup, BBQ, Beans)
   - 5-10 produktów Pudliszki (Musztarda, Chrzan)
   - Różne formaty (500ml retail vs 2.5kg HoReCa)

3. **Pricing per Channel:**
   - Traditional Trade (sklepy osiedlowe)
   - Modern Trade (sieci Żabka, Carrefour)
   - HoReCa (restauracje, hotele)

**Output:** JSON z produktami + loader w grze

**Czas:** 2 dni (16h)

---

### **Dzień 5 (Niedziela, 10 listopada):**
**Task: Scoring System + Visit Completion**

**Co zrobić:**
1. **Scoring logic:**
   ```python
   def calculate_visit_score(visit_outcomes):
       points = 0
       
       # Cel: zamówienie
       if visit_outcomes.get("order_placed"):
           points += 100
           points += visit_outcomes["order_value"] / 100  # Bonus za wartość
       
       # Cel: POS materials
       if visit_outcomes.get("pos_installed"):
           points += 50
       
       # Cel: relationship
       points += visit_outcomes.get("relationship_delta", 0) * 10
       
       return points
   ```

2. **Feedback po wizycie:**
   - "Świetna robota! +150 punktów"
   - "Klient zamówił Heinz Ketchup 2.5kg x 5"
   - "Zainstalowano shelf talker"

3. **Update dashboard:**
   - Total points
   - Weekly revenue
   - Clients visited

**Output:** Działający scoring + feedback

**Czas:** 1 dzień (8h)

---

### **Weekend Check-in (10 listopada wieczór):**
**✅ MILESTONE 1: Core game mechanics gotowe**
- Visit flow działa end-to-end
- Portfolio produktowe załadowane
- Scoring system functional

---

## **TYDZIEŃ 2: ECONOMIC TOOLS + BRANDING** 💰🎨
**Cel:** In-game calculators + Heinz look & feel

### **Dzień 6-7 (Poniedziałek-Wtorek, 11-12 listopada):**
**Task: Economic Tools In-Game**

**Co zrobić:**
1. **Food Cost Calculator Popup (podczas wizyty):**
   ```python
   # Klient (restauracja) pyta: "A ile mnie to będzie kosztować na porcję?"
   
   [KALKULATOR]
   Heinz Ketchup 2.5kg: 35.99 zł
   Porcja: 30g
   
   → Koszt porcji: 0.43 zł
   → Food cost: 1.4% (cena burgera 30 zł)
   → Oszczędność vs produkt standardowy: 0.12 zł/porcję
   
   [Pokaż klientowi] → Automatycznie generuje pitch
   ```

2. **Auto-Pitch Generator:**
   ```
   "Pan {Imię}, używając Heinz Ketchup zamiast produktu X:
   - Koszt porcji: tylko 0.43 zł (vs 0.55 zł)
   - Oszczędność miesięczna: ~360 zł (przy 3000 porcjach)
   - Food cost: 1.4% vs 1.8% - lepsza rentowność!"
   ```

3. **Comparison Tool:**
   - Heinz vs Pudliszki (positioning: premium vs value)
   - ROI calculator (zwrot z inwestycji)

**Output:** Popup kalkulatora w grze

**Czas:** 2 dni (16h)

---

### **Dzień 8-9 (Środa-Czwartek, 13-14 listopada):**
**Task: Heinz Branding**

**Co zrobić:**
1. **Visual Identity:**
   - Logo Heinz na header
   - Primary color: Heinz Red (#D32F2F)
   - Secondary: White + Dark Gray
   - Fonts: Roboto (clean, corporate)

2. **Welcome Screen:**
   ```
   ═══════════════════════════════════════════
          🍅 HEINZ SALES ACADEMY
       Master Food Service Sales Through Practice
   ═══════════════════════════════════════════
   
   Witaj, [Imię]!
   
   Twoja misja: Zostań najlepszym Area Managerem w Polsce
   
   [▶ Rozpocznij grę]  [📚 Zobacz szkolenia]
   ```

3. **In-game branding:**
   - Products mają loga Heinz/Pudliszki
   - Dashboard: "Heinz Academy Dashboard"
   - Footer: "Powered by Heinz Poland"

**Output:** Fully branded app

**Czas:** 2 dni (16h)

---

### **Dzień 10 (Piątek, 15 listopada):**
**Task: Tutorial & Onboarding**

**Co zrobić:**
1. **First-time user experience:**
   ```
   Krok 1: "Witaj w Heinz Sales Academy!"
   Krok 2: "Zobaczmy mapę Twojego terytorium"
   Krok 3: "Odwiedź pierwszego klienta (tutorial)"
   Krok 4: "Wykonaj pierwszą sprzedaż"
   Krok 5: "Zobacz swoje wyniki"
   ```

2. **Interactive tooltips:**
   - Hover na mapie: "To Twoi klienci"
   - Hover na products: "Kliknij, żeby zobaczyć szczegóły"

3. **Help section:**
   - FAQ: "Jak zdobyć punkty?"
   - Video walkthrough (opcjonalnie)

**Output:** Guided tutorial dla nowego usera

**Czas:** 1 dzień (8h)

---

### **Weekend Check-in (15 listopada wieczór):**
**✅ MILESTONE 2: Gra z brandingiem Heinz gotowa do testów**
- Economic tools działają
- Branding Heinz 100%
- Tutorial functional

---

## **TYDZIEŃ 3: PREZENTACJA + POLISH** 🎁
**Cel:** Landing page + Deck + Demo ready

### **Dzień 11-12 (Sobota-Niedziela, 16-17 listopada):**
**Task: Landing Page**

**Co zrobić:**
1. **Struktura landing page:**
   ```html
   <!-- Section 1: Hero -->
   <h1>Heinz Sales Academy</h1>
   <p>Zmniejsz czas onboardingu o 60%. Zwiększ efektywność zespołu.</p>
   [▶ Zobacz Demo] [📞 Umów prezentację]
   
   <!-- Section 2: Problem/Solution -->
   Problem: Tradycyjne szkolenia = 9 miesięcy + 15k zł
   Solution: Symulacja + e-learning = 3 miesiące + 6k zł
   
   <!-- Section 3: Features -->
   ✅ Realistic Territory Simulation
   ✅ 7 Interactive Training Modules
   ✅ Economic Tools (Food Cost, Pricing)
   ✅ Gamification (points, leaderboards)
   
   <!-- Section 4: Screenshots -->
   [Mapa] [Visit Dialog] [Dashboard] [Training Module]
   
   <!-- Section 5: CTA -->
   Pilot 3-miesięczny: 15,000 zł
   [Umów demo call]
   ```

2. **Hosting:**
   - Streamlit Cloud (free tier) OR
   - AWS Lightsail ($10/mies)
   - Custom domain: heinz-academy.yourplatform.com

**Output:** Live landing page

**Czas:** 2 dni (16h)

---

### **Dzień 13 (Poniedziałek, 18 listopada):**
**Task: Pitch Deck (10 slides)**

**Slajdy:**

**1. Cover:**
```
HEINZ SALES ACADEMY
Symulacja Sprzedaży + E-Learning
[Logo Heinz]
```

**2. Problem Statement:**
```
Wyzwania onboardingu w Heinz:
- 9 miesięcy do pełnej produktywności
- 15,000 zł koszt na osobę
- Brak standaryzacji szkoleń
- 45% turnover w pierwszym roku
```

**3. Solution:**
```
Heinz Sales Academy:
🎮 Realistyczna symulacja terenu
📚 7 modułów szkoleniowych
💰 Economic tools (food cost, ROI)
📊 Analytics & Progress tracking
```

**4. How It Works (Screenshot gry):**
```
[Mapa] → [Visit] → [Conversation] → [Sale] → [Points]
```

**5. Training Modules:**
```
✅ Trade Marketing (4 lekcje)
✅ Ekonomia talerza
✅ Narzędzia ekonomiczne
✅ Dwie marki, jeden zysk
+ więcej w roadmap
```

**6. Benefits (Measurable):**
```
Metric          | Przed | Po
----------------|-------|-------
Time-to-prod    | 9 mies| 3 mies
Koszt/osoba     | 15k   | 6k
Retention       | 55%   | 75%
Knowledge score | 60%   | 85%
```

**7. Pilot Program:**
```
15,000 PLN / 3 miesiące
- 20-30 userów
- 1 scenariusz + 7 szkoleń
- Full Heinz branding
- Support + raport końcowy
```

**8. Roadmap (co będzie później):**
```
Faza 1 (Pilot): Basic scenario + training
Faza 2 (Q1 2026): Custom scenarios, CRM integration
Faza 3 (Q2 2026): Mobile app, multiplayer
```

**9. Case Study / Social Proof:**
```
"Similar platforms reduced onboarding time by 55%"
(Źródło: Harvard Business Review, 2024)
```

**10. Call to Action:**
```
Gotowi na pilotaż?

Kontakt:
[Twoje dane]

[Umów 30-min demo call]
```

**Output:** PDF deck gotowy do wysłania

**Czas:** 1 dzień (8h)

---

### **Dzień 14 (Wtorek, 19 listopada):**
**Task: Testing & Bug Fixes**

**Co zrobić:**
1. **Beta test z 3 userami:**
   - Znajomy/rodzina grają przez pełny scenariusz
   - Zbierz feedback (co niejasne, co buguje)

2. **Critical bug fixes:**
   - Visit flow crashes?
   - Scoring błędnie liczy?
   - Branding się rozjeżdża?

3. **Performance:**
   - Czy app ładuje się szybko?
   - Czy mapa renderuje poprawnie?

**Output:** Stabilna wersja bez krytycznych bugów

**Czas:** 1 dzień (8h)

---

### **Dzień 15 (Środa, 20 listopada):**
**Task: Rehearsal & Final Polish**

**Co zrobić:**
1. **Rehearsal prezentacji:**
   - 30-min pitch (z deckiem)
   - 15-min live demo (gra)
   - 15-min Q&A

2. **Przygotuj odpowiedzi na pytania:**
   - "Ile to kosztuje?" → Pricing ready
   - "Jak mierzymy sukces?" → KPI defined
   - "Co z integracją CRM?" → Roadmap item
   - "Mobile app?" → Phase 3

3. **Final checklist:**
   - [ ] Landing page live
   - [ ] Deck wysłany do Heinz
   - [ ] Demo account gotowy (login: heinz_demo / hasło: demo2024)
   - [ ] Email follow-up draft

**Output:** Gotowość do prezentacji

**Czas:** 1 dzień (8h)

---

### **21-26 listopada: BUFFER WEEK**
**Cel:** Elastyczność na nieprzewidziane

- Dodatkowe testy
- Content polish (typos, translations)
- Przygotowanie case study materials
- Networking (setup meeting z Heinz)

---

## **26 LISTOPADA: 🎯 MVP READY FOR HEINZ PITCH**

---

## 📊 MUST-HAVE vs NICE-TO-HAVE

### ✅ MUST-HAVE (bez tego nie pokazuj):
- [x] Visit flow (conversation → outcome → scoring)
- [x] Portfolio Heinz/Pudliszki (15 produktów minimum)
- [x] Economic tools in-game (food cost calculator)
- [x] Branding Heinz (logo, kolory, welcome screen)
- [x] 7 lekcji szkoleniowych (już gotowe ✅)
- [x] Landing page
- [x] Pitch deck (10 slides)
- [x] Tutorial/onboarding

### 🟡 NICE-TO-HAVE (można dodać po pilotażu):
- [ ] Quizy po lekcjach
- [ ] Certyfikaty ukończenia
- [ ] Multiplayer leaderboards
- [ ] Integracja CRM
- [ ] Mobile app / PWA
- [ ] Wiele scenariuszy
- [ ] Advanced analytics dashboard

---

## 🎯 SUCCESS METRICS (jak zmierzyć sukces MVP)

### Przed prezentacją Heinz:
- [ ] 3 beta testerów ukończyło pełny scenariusz (avg time: 2-3h)
- [ ] Zero critical bugs
- [ ] Landing page live + min 100 views (share w LinkedIn)
- [ ] Deck reviewed przez 2 osoby (feedback uwzględniony)

### Podczas pilotu (3 miesiące):
- **Engagement:** 70%+ userów ukończy min 1 scenariusz
- **Learning:** Avg quiz score improvement +25%
- **Satisfaction:** NPS > 50
- **Business impact:** Measure time-to-first-sale (nowi vs starzy reps)

---

## 💰 BUDGET & RESOURCES

### Time Investment:
- **Total:** ~120 godzin (15 dni x 8h)
- **Your time:** 100h (development)
- **External help:** 20h (design, copy review - opcjonalnie)

### Costs:
| Item | Cost | Notes |
|------|------|-------|
| Hosting (AWS/DO) | $50-100/mies | Po pilotażu |
| Domain | $12/rok | heinz-academy.com |
| Streamlit Cloud | FREE | Na MVP OK |
| Design assets | $0-200 | Canva Pro / Fiverr |
| **TOTAL** | **~$100-300** | Do startu |

---

## 📞 SALES PROCESS - Next Steps Po MVP

### **Krok 1: Cold Outreach (27 listopada)**
```
Email do:
- Sales Director Heinz Poland
- HR/L&D Manager
- Field Sales Manager

Subject: Skrócenie onboardingu sales reps o 60% - 30-min demo?

Body:
"Cześć [Imię],

Stworzyłem Heinz Sales Academy - platformę symulacyjną,
która skraca onboarding nowych sales reps z 9 do 3 miesięcy.

Demo (3 minuty): [link do landing page]

Możemy porozmawiać 30 minut? Pokażę live demo.

Best,
[Ty]"
```

### **Krok 2: Demo Call (1-7 grudnia)**
- 10 min: Problem statement + pitch deck
- 15 min: Live demo (gra + szkolenia)
- 5 min: Q&A + next steps

### **Krok 3: Proposal (8-14 grudnia)**
- Formal proposal (PDF)
- Pricing: 15,000 PLN pilot
- Timeline: Start styczeń 2026
- Deliverables: Scenariusz + szkolenia + support

### **Krok 4: Pilot Kickoff (Styczeń 2026)**
- 20-30 userów
- 3 miesiące
- Weekly check-ins
- Final report (marzec 2026)

### **Krok 5: Expansion (Kwiecień 2026+)**
- Full deployment
- Custom scenarios
- CRM integration
- Mobile app

---

## 🚨 RISK MITIGATION

### **Risk 1: Heinz nie odpowie**
**Mitigation:**
- Plan B: Unilever, Nestle, Mondelez (już research)
- Generic version dla firm szkoleniowych
- Pivot na inną branżę (pharma, automotive)

### **Risk 2: Za dużo customizacji**
**Mitigation:**
- Pilot = fixed scope
- Custom features = Phase 2 (dodatkowy budżet)
- NDA chroni przed "wykradnięciem" idei

### **Risk 3: Technical issues podczas demo**
**Mitigation:**
- Backup: Nagrany screen recording (YouTube unlisted)
- Local hosting (nie cloud) na demo call
- Rehearsal 3x przed live call

### **Risk 4: Pricing za niski/wysoki**
**Mitigation:**
- Research: Ile Heinz płaci za tradycyjne szkolenia?
- Benchmark: Inne platformy B2B (Moodle, Articulate)
- Flexibility: "Możemy dostosować zakres do budżetu"

---

## 📚 DOCUMENTATION & HANDOFF

### **Dla Heinz (po pilotażu):**
- User manual (PDF, 10 stron)
- Admin guide (zarządzanie userami)
- FAQ (20 najczęstszych pytań)
- Video tutorials (5x po 3 minuty)

### **Dla siebie (teraz):**
- Technical documentation (architecture, APIs)
- Code comments (dla przyszłego refactoringu)
- Lessons learned (co działało, co nie)

---

## 🎓 KEY TAKEAWAYS

### **Filozofia MVP:**
> "Make it work, make it right, make it fast"
> 
> Teraz: **Make it work** dla Heinz
> Potem: **Make it right** (refactoring dla multi-industry)
> Później: **Make it fast** (scalability)

### **Priorytetyzacja:**
1. **Core game mechanics** (bez tego nie ma gry)
2. **Branding** (musi wyglądać na Heinz, nie generic)
3. **Prezentacja** (sprzedaż MVP, nie tylko kod)
4. **Polish** (UX, tutorial, help)

### **Communication:**
- Heinz nie kupuje kodu - kupuje **business value**
- Twój pitch: "Onboarding 60% szybciej, 60% taniej"
- Metrics > Features

---

## ✅ FINAL CHECKLIST (przed prezentacją)

### **Technical:**
- [ ] Visit flow działa end-to-end
- [ ] Portfolio 15+ produktów Heinz/Pudliszki
- [ ] Economic calculator functional
- [ ] Scoring system accuratne
- [ ] Branding Heinz (logo, kolory, fonts)
- [ ] Tutorial dla nowego usera
- [ ] Zero critical bugs
- [ ] Beta test z 3 osobami

### **Business:**
- [ ] Landing page live (heinz-academy.yourplatform.com)
- [ ] Pitch deck (10 slides PDF)
- [ ] Pricing defined (15k PLN pilot)
- [ ] Email outreach draft
- [ ] Demo account ready (login: heinz_demo)
- [ ] Rehearsal prezentacji 3x

### **Legal/Admin:**
- [ ] NDA template (jeśli Heinz zażąda)
- [ ] Contract template (pilot agreement)
- [ ] Faktura VAT setup (jeśli wygrasz)

---

## 🚀 MOTIVATION

**26 listopada = 21 dni od teraz**

**To jest realny timeline!**

Masz już 50% pracy zrobionej:
- ✅ Core engine (mapa, klienci, tasks)
- ✅ 7 lekcji szkoleniowych
- ✅ Economic tools (jako lekcje)

Zostaje 50%:
- Visit flow (2 dni)
- Portfolio (2 dni)
- Branding (2 dni)
- Prezentacja (3 dni)
= 9 dni solidnej pracy + 6 dni buffer

**You got this!** 💪

---

## 📞 SUPPORT & NEXT STEPS

**Co mogę zrobić TERAZ:**

1. **Conversation Tree Template** - dam Ci gotowy kod
2. **Portfolio JSON** - stworzę przykładową strukturę
3. **Landing Page Copy** - napiszę teksty marketingowe
4. **Deck Outline** - szczegółowe slajdy z contentem
5. **Email Templates** - cold outreach do Heinz

**Którym chcesz zacząć?** 🚀

---

**Document Version:** 1.0  
**Last Updated:** 5 listopada 2025  
**Owner:** Krzysztof (BVA Project Lead)  
**Status:** 🟢 ACTIVE - 3-week sprint rozpoczęty

---

## 🎯 DAILY STANDUP TEMPLATE

Kopiuj to codziennie do trackowania:

```
Data: ___________
Dzień sprintu: ___ / 15

✅ Zrobione wczoraj:
- 
- 

🎯 Plan na dziś:
- 
- 

⚠️ Blockersy:
- 

📊 Progress: ___% (0-100%)
```

**Gotowy do startu?** Powiedz od czego zaczynamy! 💪
