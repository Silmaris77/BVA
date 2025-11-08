# 🎯 Plan Pracy: FMCG Heinz Food Service Game

**Data rozpoczęcia:** 7 Listopada 2025  
**Target prezentacji:** 26 Listopada 2025 (19 dni)  
**Cel:** Gotowa prezentacja + działające demo dla Heinz Poland

---

## 📊 STAN OBECNY (7 listopada 2025)

### ✅ Co już mamy (DONE):

**1. Fundament Techniczny:**
- ✅ Struktura Business Games (consulting + FMCG)
- ✅ System użytkowników (JSON + SQL)
- ✅ Repository pattern (user, business_game, notes)
- ✅ Migracje danych (automatyczne dodawanie pól)

**2. FMCG Core Mechanics:**
- ✅ Territory management (Piaseczno, 25 klientów z lokalizacją GPS)
- ✅ Lifecycle klienta: PROSPECT → ACTIVE → LOST
- ✅ Discovery System (5-star knowledge, stopniowe odkrywanie)
- ✅ Reputation System (0-100, progress bar, 5 poziomów)
- ✅ Energy System (dedukcja per wizyta, dystans + czas)
- ✅ Visit Flow (konwersacje AI, zamówienia, historia)
- ✅ Sales Capacity (realistyczne limity zamówień per kategoria)
- ✅ Market Share tracking (player vs competition per kategoria)
- ✅ Notes System (6 kategorii, dropdown produkty/klienci)

**3. FMCG UI/UX:**
- ✅ Dashboard (4 tabs: Dashboard, Przygotowanie, Wyniki, Alex AI)
- ✅ Client Cards (reputation gauge, discovery progress, timeline)
- ✅ Visit Panel (AI conversation, ordering, podsumowanie)
- ✅ Map View (25 klientów z GPS, dystanse)
- ✅ Discovery Panel (stopniowe odkrywanie informacji)
- ✅ Notes Panel (6 kategorii, integracja z wizytami)
- ✅ Wykresy finansowe (przychody/koszty od daty założenia firmy)
- ✅ Unikalne avatary dla 25 klientów (emoji twarzy)

**4. Dane Heinz:**
- ✅ 25 klientów Piaseczno (Traditional Trade + Modern Trade)
- ✅ Portfolio Heinz/Pudliszki (produkty w JSON)
- ✅ Segmenty rynku (Traditional, Modern, Convenience)

**5. AI & Automacja:**
- ✅ AI Conversations (Gemini, kontekst klienta, historia wizyt)
- ✅ Alex AI Placeholder (struktura competencies, quizy, case studies)

---

## ❌ Co BRAKUJE do MVP Heinz (TO-DO):

### 🚨 CRITICAL (Must-Have dla prezentacji):

**1. Portfolio Heinz/Pudliszki - KOMPLETNY:**
- ❌ Brakuje ~10-15 produktów Heinz (obecnie mamy kilka testowych)
- ❌ Brakuje ceny HoReCa vs Retail
- ❌ Brakuje food cost % (kluczowe dla argumentacji sprzedaży)
- ❌ Brakuje SKU i formatów (500ml retail vs 2.5kg HoReCa)

**2. Economic Tools In-Game:**
- ❌ Food Cost Calculator (popup podczas wizyty)
- ❌ Auto-Pitch Generator (na podstawie kalkulacji)
- ❌ ROI Calculator (porównanie Heinz vs konkurencja)

**3. Heinz Branding:**
- ❌ Logo Heinz w header aplikacji
- ❌ Heinz Red (#D32F2F) jako primary color
- ❌ Welcome screen "Heinz Sales Academy"
- ❌ Produkty z logo Heinz/Pudliszki

**4. Tutorial & Onboarding:**
- ❌ First-time user experience (5-step tutorial)
- ❌ Guided pierwsza wizyta
- ❌ Tooltips (hover explanations)
- ❌ Help section / FAQ

**5. Scenariusz Heinz:**
- ❌ Dedicated Heinz scenario (zamiast generic FMCG)
- ❌ Cele scenariusza (targets: sprzedaż, wizyty, aktywni klienci)
- ❌ Progression (level-up requirements dla Heinz reps)

---

### 🟡 NICE-TO-HAVE (Jeśli zostanie czas):

**1. Alex AI - Rozbudowa:**
- ⚠️ Quizy Trade Marketing (obecnie tylko placeholder)
- ⚠️ Case Studies Food Service (obecnie tylko struktura)
- ⚠️ Autopilot wizyt (AI robi wizyty za gracza)

**2. Advanced Features:**
- ⚠️ Route Planning Optimizer (algorytm shortest path)
- ⚠️ Weekly/Monthly Targets (gamification)
- ⚠️ Leaderboards (ranking sales reps)
- ⚠️ Certyfikaty ukończenia

**3. Content:**
- ⚠️ 7 lekcji Trade Marketing (obecnie ~3-4 gotowe)
- ⚠️ Food Service Economics lessons
- ⚠️ Więcej produktów (pełny katalog Heinz)

---

## 📅 HARMONOGRAM 19 DNI (7-26 listopada)

### **TYDZIEŃ 1: CORE GAME MECHANICS (7-13 listopada, 7 dni)**

**🎯 Cel:** Działający visit flow + portfolio Heinz + economic tools

---

#### **Dzień 1-2 (Czwartek-Piątek, 7-8 listopada)**
**Task: Portfolio Heinz/Pudliszki - Kompletny**

**Co zrobić:**
1. **Stwórz pełny katalog produktów Heinz (15-20 SKU):**
   ```json
   {
     "heinz_ketchup_500ml": {
       "sku": "HNZ-KTC-500",
       "name": "Heinz Ketchup Classic 500ml",
       "brand": "Heinz",
       "category": "Food",
       "subcategory": "Ketchup",
       "format": "500ml",
       "channel": "Retail",
       "price_retail": 12.99,
       "price_horeca": null,
       "margin_retail": 35,
       "logo": "🍅"
     },
     "heinz_ketchup_2500g": {
       "sku": "HNZ-KTC-2.5KG",
       "name": "Heinz Ketchup Classic 2.5kg",
       "brand": "Heinz",
       "category": "Food",
       "subcategory": "Ketchup",
       "format": "2.5kg",
       "channel": "HoReCa",
       "price_horeca": 35.99,
       "portion_size_g": 30,
       "portions_per_unit": 83,
       "food_cost_per_portion": 0.43,
       "food_cost_percent": 1.4,  // % przy cenie burgera 30 zł
       "logo": "🍅"
     }
   }
   ```

2. **Produkty do dodania:**
   - **Heinz Ketchup:** 500ml (retail), 2.5kg (HoReCa), 5kg (HoReCa)
   - **Heinz BBQ Sauce:** 500ml, 2.2kg, 5kg
   - **Heinz Mayonnaise:** 400ml, 2.15kg, 5kg
   - **Heinz Beans:** 415g, 3kg
   - **Pudliszki Musztarda:** 500g (retail), 2kg (HoReCa)
   - **Pudliszki Chrzan:** 190g, 850g
   - **Pudliszki Ketchup:** 480g, 2kg

3. **Dla każdego produktu HoReCa dodaj:**
   - `portion_size_g` (typowa porcja, np. 30g ketchup)
   - `portions_per_unit` (ile porcji z opakowania)
   - `food_cost_per_portion` (koszt 1 porcji)
   - `food_cost_percent` (% przy typowej cenie dania)
   - `savings_vs_standard` (oszczędność vs produkt konkurencji)

**Output:** `data/industries/heinz_products.json` z 15-20 produktami

**Czas:** 2 dni (16h)

---

#### **Dzień 3-4 (Sobota-Niedziela, 9-10 listopada)**
**Task: Economic Tools In-Game**

**Co zrobić:**
1. **Food Cost Calculator Popup:**
   ```python
   # utils/heinz_economic_tools.py
   
   def calculate_food_cost(product_sku, portion_size_g, dish_price_pln):
       """
       Oblicza food cost dla produktu Heinz
       
       Args:
           product_sku: SKU produktu (np. "HNZ-KTC-2.5KG")
           portion_size_g: Wielkość porcji w gramach
           dish_price_pln: Cena dania u klienta
       
       Returns:
           Dict {
               "cost_per_portion": 0.43,
               "food_cost_percent": 1.4,
               "monthly_savings": 360,  # przy 3000 porcjach
               "vs_competitor": {
                   "competitor_cost": 0.55,
                   "savings_per_portion": 0.12
               }
           }
       """
       pass
   ```

2. **Auto-Pitch Generator:**
   ```python
   def generate_pitch(client_name, product, calculation_result):
       """
       Generuje pitch sprzedażowy na podstawie kalkulacji
       
       Returns:
           str: "Pan {client_name}, używając Heinz Ketchup 2.5kg 
                 zamiast produktu X:
                 - Koszt porcji: tylko 0.43 zł (vs 0.55 zł)
                 - Oszczędność miesięczna: ~360 zł (przy 3000 porcjach)
                 - Food cost: 1.4% vs 1.8% - lepsza rentowność!"
       """
       pass
   ```

3. **Integracja z Visit Panel:**
   - Podczas wizyty (tab "Narzędzia") → przycisk "💰 Kalkulator Food Cost"
   - Popup z formularzem:
     - Select Product (dropdown Heinz HoReCa)
     - Input: Wielkość porcji (default 30g)
     - Input: Cena dania (default 30 zł)
     - Button: "Oblicz"
   - Output: Wyniki + Auto-generated pitch
   - Button: "📋 Kopiuj pitch" (copy to clipboard)

**Output:** 
- `utils/heinz_economic_tools.py`
- Popup w Visit Panel
- Auto-pitch w konwersacji

**Czas:** 2 dni (16h)

---

#### **Dzień 5 (Poniedziałek, 11 listopada)**
**Task: Testing & Bug Fixes (Week 1 Core)**

**Co zrobić:**
1. **Test portfolio:**
   - Czy wszystkie produkty ładują się poprawnie?
   - Czy ceny są realistyczne?
   - Czy food cost % się zgadza?

2. **Test economic tools:**
   - Czy kalkulator liczy poprawnie?
   - Czy pitch jest sensowny?
   - Czy kopiowanie działa?

3. **Bug fixes:**
   - Naprawa błędów z visit flow
   - Poprawki UI/UX

**Output:** Stabilna wersja core mechanics

**Czas:** 1 dzień (8h)

---

### **Weekend Check-in (11 listopada wieczór):**
**✅ MILESTONE 1: Core game mechanics gotowe**
- Portfolio Heinz kompletny (15-20 produktów)
- Economic tools działają (kalkulator + pitch generator)
- Visit flow end-to-end stabilny

---

### **TYDZIEŃ 2: BRANDING + TUTORIAL + SCENARIUSZ (12-18 listopada, 7 dni)**

**🎯 Cel:** Heinz look & feel + onboarding + dedicated scenario

---

#### **Dzień 6-7 (Wtorek-Środa, 12-13 listopada)**
**Task: Heinz Branding**

**Co zrobić:**
1. **Visual Identity:**
   ```python
   # config/heinz_theme.py
   
   HEINZ_THEME = {
       "primary_color": "#D32F2F",  # Heinz Red
       "secondary_color": "#FFFFFF",  # White
       "accent_color": "#1A1A1A",    # Dark Gray
       "font_family": "Roboto, sans-serif",
       "logo_url": "/static/heinz_logo.png"  # Jeśli masz logo
   }
   ```

2. **Welcome Screen (landing page gry):**
   ```python
   # views/fmcg_welcome.py
   
   def render_heinz_welcome():
       st.markdown("""
       <div style='background: linear-gradient(135deg, #D32F2F 0%, #A02020 100%); 
                   padding: 60px 40px; text-align: center; border-radius: 16px;'>
           <h1 style='color: white; font-size: 48px; margin-bottom: 16px;'>
               🍅 HEINZ SALES ACADEMY
           </h1>
           <h3 style='color: #FFE0E0; font-size: 24px; margin-bottom: 32px;'>
               Master Food Service Sales Through Practice
           </h3>
           <p style='color: white; font-size: 18px; max-width: 600px; margin: 0 auto 32px;'>
               Witaj w interaktywnej symulacji sprzedaży Heinz Food Service.
               Poznaj klientów, prowadź wizyty, buduj relacje i osiągnij cele sprzedażowe!
           </p>
           <button style='background: white; color: #D32F2F; padding: 16px 32px; 
                          font-size: 18px; font-weight: bold; border: none; 
                          border-radius: 8px; cursor: pointer;'>
               ▶ Rozpocznij grę
           </button>
       </div>
       """, unsafe_allow_html=True)
   ```

3. **Header aplikacji:**
   - Zamień "BrainventureAcademy" → "Heinz Sales Academy"
   - Dodaj logo Heinz (jeśli dostępne) lub emoji 🍅
   - Zmień primary color na Heinz Red

4. **Produkty z branding:**
   - Każdy produkt ma logo emoji (🍅 Heinz, 🌶️ Pudliszki)
   - W visit panel: produkty wyświetlane z logiem

**Output:** 
- Fully branded app (Heinz Red theme)
- Welcome screen
- Header z logo

**Czas:** 2 dni (16h)

---

#### **Dzień 8-9 (Czwartek-Piątek, 14-15 listopada)**
**Task: Tutorial & Onboarding**

**Co zrobić:**
1. **First-Time User Experience (5 kroków):**
   ```python
   # utils/fmcg_tutorial.py
   
   TUTORIAL_STEPS = [
       {
           "step": 1,
           "title": "Witaj w Heinz Sales Academy!",
           "content": "Jesteś Junior Sales Representative w Heinz Food Service. 
                      Twoim celem jest obsłużyć region Piaseczno i zbudować 
                      bazę lojalnych klientów HoReCa.",
           "action": "next"
       },
       {
           "step": 2,
           "title": "Poznaj swoje terytorium",
           "content": "Masz 25 klientów w promieniu 30km. 
                      Każdy ma inne potrzeby i osobowość. 
                      Kliknij 'Mapa', żeby zobaczyć swoich klientów.",
           "highlight": "map_tab",
           "action": "click_map"
       },
       {
           "step": 3,
           "title": "Przeprowadź pierwszą wizytę",
           "content": "Odwiedź 'Sklep U Danusi' - Twojego pierwszego klienta. 
                      Poznaj właścicielkę, zrozum jej potrzeby i zaproponuj produkty.",
           "highlight": "client_pias_001",
           "action": "start_visit"
       },
       {
           "step": 4,
           "title": "Użyj narzędzi ekonomicznych",
           "content": "Podczas wizyty możesz użyć Kalkulatora Food Cost, 
                      żeby pokazać klientowi oszczędności.",
           "highlight": "economic_tools",
           "action": "use_calculator"
       },
       {
           "step": 5,
           "title": "Sprawdź swoje wyniki",
           "content": "Po wizycie zobacz dashboard - przychody, reputację, 
                      aktywnych klientów. Śledź swój postęp!",
           "highlight": "dashboard_tab",
           "action": "complete"
       }
   ]
   ```

2. **Interactive Tooltips:**
   - Hover na mapie: "To Twoi klienci - kliknij, żeby zobaczyć szczegóły"
   - Hover na produktach: "Kliknij, żeby zobaczyć food cost"
   - Hover na energy: "Każda wizyta kosztuje energię - planuj trasę mądrze"

3. **Help Section:**
   - FAQ: "Jak zdobyć punkty?", "Czym jest food cost?", "Jak używać kalkulatora?"
   - Video walkthrough (opcjonalnie - screen recording)

**Output:** 
- Guided tutorial dla nowego usera
- Tooltips w kluczowych miejscach
- Help/FAQ section

**Czas:** 2 dni (16h)

---

#### **Dzień 10 (Sobota, 16 listopada)**
**Task: Scenariusz Heinz Food Service**

**Co zrobić:**
1. **Stwórz dedicated scenario:**
   ```python
   # data/scenarios.py
   
   "fmcg": {
       "heinz_foodservice": {
           "id": "heinz_foodservice",
           "name": "🍅 Heinz Food Service - Piaseczno Territory",
           "description": """
           Zostań Sales Representative Heinz w regionie Piaseczno.
           Twoim celem jest zbudować bazę 10 aktywnych klientów HoReCa
           i osiągnąć miesięczną sprzedaż 50,000 PLN w ciągu 3 miesięcy.
           """,
           "icon": "🍅",
           "difficulty": "medium",
           
           "initial_conditions": {
               "territory": "Piaseczno",
               "starting_clients": 5,  # PROSPECT
               "energy": 100,
               "marketing_budget": 2000
           },
           
           "objectives": [
               {
                   "type": "active_clients",
                   "target": 10,
                   "description": "Zdobądź 10 aktywnych klientów",
                   "reward_money": 0,
                   "reward_xp": 500
               },
               {
                   "type": "monthly_sales",
                   "target": 50000,
                   "description": "Osiągnij 50,000 PLN sprzedaży miesięcznie",
                   "reward_money": 0,
                   "reward_xp": 1000
               },
               {
                   "type": "reputation_avg",
                   "target": 70,
                   "description": "Utrzymuj średnią reputację 70+ u aktywnych klientów",
                   "reward_money": 0,
                   "reward_xp": 300
               },
               {
                   "type": "products_sold",
                   "target": ["HNZ-KTC-2.5KG", "HNZ-BBQ-2.2KG", "HNZ-MAY-2.15KG"],
                   "description": "Sprzedaj wszystkie 3 kluczowe produkty Heinz",
                   "reward_money": 0,
                   "reward_xp": 200
               }
           ],
           
           "progression": {
               "level_1": {
                   "title": "Junior Sales Rep",
                   "weekly_target_sales": 8000,
                   "weekly_target_visits": 6,
                   "unlock": "Podstawowe produkty Heinz"
               },
               "level_2": {
                   "title": "Sales Representative",
                   "weekly_target_sales": 12000,
                   "weekly_target_visits": 8,
                   "unlock": "Food Cost Calculator"
               },
               "level_3": {
                   "title": "Senior Sales Rep",
                   "weekly_target_sales": 18000,
                   "weekly_target_visits": 10,
                   "unlock": "Alex AI Assistant"
               }
           }
       }
   }
   ```

2. **Progress Tracking:**
   - Dashboard pokazuje cele scenariusza
   - Progress bar dla każdego celu
   - Notyfikacje przy ukończeniu celów

**Output:** 
- Heinz scenario definition
- Objectives tracking
- Progression system

**Czas:** 1 dzień (8h)

---

#### **Dzień 11 (Niedziela, 17 listopada)**
**Task: Testing & Polish (Week 2)**

**Co zrobić:**
1. **Beta test z 3 osobami:**
   - Znajomy/rodzina grają pełny scenariusz (2-3h)
   - Zbierz feedback (co niejasne, co buguje)

2. **Bug fixes:**
   - Tutorial flow crashes?
   - Branding się rozjeżdża?
   - Economic tools liczą błędnie?

3. **Performance:**
   - Czy app ładuje się szybko?
   - Czy nie ma memory leaks?

**Output:** Stabilna wersja z branding + tutorial

**Czas:** 1 dzień (8h)

---

### **Weekend Check-in (17 listopada wieczór):**
**✅ MILESTONE 2: Branding + Tutorial + Scenario gotowe**
- Heinz look & feel (red theme, logo, welcome)
- Tutorial działa (5-step onboarding)
- Scenariusz Heinz z celami

---

### **TYDZIEŃ 3: PREZENTACJA + LANDING PAGE + FINAL POLISH (19-26 listopada, 8 dni)**

**🎯 Cel:** Landing page + Pitch Deck + Demo ready

---

#### **Dzień 12-13 (Wtorek-Środa, 19-20 listopada)**
**Task: Landing Page**

**Co zrobić:**
1. **Struktura strony (Streamlit lub HTML):**
   ```html
   <!-- Section 1: Hero -->
   <div class="hero" style="background: linear-gradient(135deg, #D32F2F, #A02020);">
       <h1>🍅 Heinz Sales Academy</h1>
       <h2>Zmniejsz czas onboardingu o 60%. Zwiększ efektywność zespołu.</h2>
       <button>▶ Zobacz Demo</button>
       <button>📞 Umów prezentację</button>
   </div>
   
   <!-- Section 2: Problem/Solution -->
   <div class="problem-solution">
       <h3>Problem</h3>
       <p>Tradycyjne szkolenia sales reps w Heinz:</p>
       <ul>
           <li>⏰ 9 miesięcy do pełnej produktywności</li>
           <li>💰 15,000 zł koszt na osobę</li>
           <li>📚 Brak standaryzacji szkoleń</li>
           <li>📉 45% turnover w pierwszym roku</li>
       </ul>
       
       <h3>Solution: Heinz Sales Academy</h3>
       <ul>
           <li>🎮 Realistyczna symulacja terenu (25 klientów HoReCa)</li>
           <li>💰 Economic tools (Food Cost Calculator)</li>
           <li>📊 Progress tracking & analytics</li>
           <li>🤖 AI-powered conversations</li>
       </ul>
   </div>
   
   <!-- Section 3: Features -->
   <div class="features">
       <h3>Kluczowe Funkcje</h3>
       <div class="feature-grid">
           <div class="feature">
               <h4>🗺️ Territory Management</h4>
               <p>25 klientów w regionie Piaseczno z realistycznymi profilami</p>
           </div>
           <div class="feature">
               <h4>💬 AI Conversations</h4>
               <p>Prowadź wizyty z AI klientami, buduj relacje</p>
           </div>
           <div class="feature">
               <h4>💰 Food Cost Calculator</h4>
               <p>Oblicz oszczędności, generuj pitch sprzedażowy</p>
           </div>
           <div class="feature">
               <h4>📊 Analytics Dashboard</h4>
               <p>Śledź sprzedaż, reputację, market share</p>
           </div>
       </div>
   </div>
   
   <!-- Section 4: Screenshots -->
   <div class="screenshots">
       <h3>Zobacz Demo</h3>
       <img src="screenshot_map.png" alt="Mapa klientów">
       <img src="screenshot_visit.png" alt="Panel wizyty">
       <img src="screenshot_dashboard.png" alt="Dashboard">
   </div>
   
   <!-- Section 5: Pricing -->
   <div class="pricing">
       <h3>Pilot Program</h3>
       <div class="price-card">
           <h4>15,000 PLN / 3 miesiące</h4>
           <ul>
               <li>✅ 20-30 userów (sales reps + managers)</li>
               <li>✅ Scenariusz "Heinz Food Service - Piaseczno"</li>
               <li>✅ Full Heinz branding</li>
               <li>✅ Support: email + 2x check-in call</li>
               <li>✅ Raport końcowy (engagement, learning outcomes)</li>
           </ul>
           <button>Umów demo call</button>
       </div>
   </div>
   
   <!-- Section 6: CTA -->
   <div class="cta">
       <h3>Gotowi na pilotaż?</h3>
       <p>Umów 30-minutowy demo call z naszym zespołem</p>
       <button>📞 Kontakt</button>
   </div>
   ```

2. **Hosting:**
   - Streamlit Cloud (free tier) - prosta opcja
   - Lub statyczny HTML na GitHub Pages
   - Custom domain: `heinz-academy.yourplatform.com`

**Output:** Live landing page

**Czas:** 2 dni (16h)

---

#### **Dzień 14 (Czwartek, 21 listopada)**
**Task: Pitch Deck (10 slajdów)**

**Slajdy:**

**1. Cover:**
```
🍅 HEINZ SALES ACADEMY
Symulacja Sprzedaży Food Service + Interactive Training

[Logo Heinz]
Prezentacja dla: Heinz Poland
Data: Listopad 2025
```

**2. Problem Statement:**
```
Wyzwania onboardingu w Heinz Food Service:

📊 Obecny stan:
• 9 miesięcy do pełnej produktywności
• 15,000 zł koszt szkolenia na osobę
• Brak standaryzacji (każdy region szkoli inaczej)
• 45% turnover w pierwszym roku

💡 Pytanie: Jak przyspieszyć i ustandaryzować onboarding?
```

**3. Solution:**
```
🍅 Heinz Sales Academy - Interaktywna Platforma Szkoleniowa

🎮 Symulacja Sprzedaży:
   • Realistyczne terytorium (25 klientów HoReCa)
   • AI conversations (prowadź wizyty jak w rzeczywistości)
   • Discovery system (poznaj klientów stopniowo)

💰 Economic Tools:
   • Food Cost Calculator
   • Auto-pitch generator
   • ROI comparisons

📊 Analytics & Tracking:
   • Progress dashboard
   • Performance metrics
   • Manager insights
```

**4. How It Works (Screenshot gry):**
```
[Mapa] → [Wizyta] → [Conversation AI] → [Zamówienie] → [Dashboard]

Gracz:
1. Wybiera klienta z mapy (25 HoReCa w Piasecznie)
2. Prowadzi wizytę (AI conversation)
3. Używa narzędzi (Food Cost Calculator)
4. Składa zamówienie (realistyczne portfolio Heinz)
5. Śledzi wyniki (dashboard, market share)
```

**5. Key Features:**
```
✅ 25 Klientów HoReCa (z GPS, profilami, osobowościami)
✅ Portfolio Heinz/Pudliszki (15-20 produktów z cenami)
✅ Food Cost Calculator (oszczędności per porcja)
✅ AI Conversations (kontekst, historia wizyt, pamięć)
✅ Discovery System (5-star knowledge progress)
✅ Reputation Tracking (0-100, 5 poziomów)
✅ Market Share Analytics (player vs competition)
```

**6. Benefits (Measurable):**
```
Metric              | Przed | Po (cel)
--------------------|-------|----------
Time-to-productivity| 9 mies| 3-4 mies
Koszt/osoba         | 15k   | 6k PLN
Retention (rok 1)   | 55%   | 75%
Knowledge score     | 60%   | 85%
Standardization     | 40%   | 95%

ROI: 2.5x w pierwszym roku
```

**7. Pilot Program:**
```
💰 15,000 PLN / 3 miesiące

Zawiera:
✅ 20-30 userów (sales reps + managers)
✅ Scenariusz "Heinz Food Service - Piaseczno"
✅ 25 klientów HoReCa z realistycznymi profilami
✅ Portfolio Heinz/Pudliszki (15+ produktów)
✅ Economic Tools (Food Cost Calculator)
✅ Full Heinz branding (logo, colors, theme)
✅ Support: email + 2x check-in call
✅ Raport końcowy (engagement, sales metrics, learning outcomes)

Możliwość rozszerzenia po pilotażu
```

**8. Roadmap:**
```
Faza 1 (Pilot - Q4 2025):
✅ Scenariusz Piaseczno (25 klientów)
✅ Economic tools
✅ Basic analytics

Faza 2 (Q1 2026):
🔄 Więcej terytoriów (Warszawa, Kraków, Wrocław)
🔄 Custom scenarios (nowe produkty, promocje)
🔄 Advanced Alex AI (autopilot visits)
🔄 Integracja CRM (Salesforce)

Faza 3 (Q2 2026+):
🔄 Mobile app (iOS/Android)
🔄 Multiplayer (rywalizacja między regionami)
🔄 Certyfikaty ukończenia
🔄 Leaderboards (national ranking)
```

**9. Case Study / Social Proof:**
```
📊 Benchmark:

"Companies using sales simulation platforms report:
• 55% reduction in onboarding time
• 40% improvement in first-year retention
• 30% higher quota attainment"

Source: Harvard Business Review, 2024

🎯 Heinz-specific benefits:
• Standaryzacja szkoleń (100% sales reps te same narzędzia)
• Scalability (łatwo dodać nowe produkty/scenariusze)
• Data-driven insights (manager widzi progress każdego repa)
```

**10. Call to Action:**
```
🚀 Gotowi na pilotaż?

Next Steps:
1️⃣ 30-min demo call (live walkthrough gry)
2️⃣ Proposal & timeline (dostosowany do Heinz)
3️⃣ Kickoff pilotu (styczeń 2026)

Kontakt:
[Twoje dane]
[Email]
[Telefon]

[Umów demo call →]
```

**Output:** PDF deck (10 slajdów)

**Czas:** 1 dzień (8h)

---

#### **Dzień 15-16 (Piątek-Sobota, 22-23 listopada)**
**Task: Screenshots & Demo Video**

**Co zrobić:**
1. **Zrób screenshots:**
   - Mapa klientów (25 pinów z GPS)
   - Panel wizyty (AI conversation + ordering)
   - Dashboard (analytics, market share)
   - Food Cost Calculator (popup z wynikami)
   - Discovery Panel (5-star progress)

2. **Nagraj screen recording (5-10 min):**
   - Welcome screen → Start gry
   - Tutorial (pierwsze kroki)
   - Pierwsza wizyta (pełny flow)
   - Food Cost Calculator (użycie narzędzia)
   - Dashboard (wyniki po wizycie)

3. **Upload:**
   - YouTube (unlisted link) - backup podczas demo call
   - Screenshots do landing page i deck

**Output:** 
- 5-10 high-quality screenshots
- 5-10 min demo video

**Czas:** 2 dni (16h)

---

#### **Dzień 17-18 (Niedziela-Poniedziałek, 24-25 listopada)**
**Task: Final Testing & Rehearsal**

**Co zrobić:**
1. **Final testing:**
   - Pełne przejście scenariusza (2-3h)
   - Test wszystkich features (portfolio, tools, tutorial)
   - Check performance (szybkość ładowania)
   - Mobile view (czy działa na telefonie?)

2. **Bug fixes CRITICAL:**
   - Naprawa tylko critical bugs (blokujących demo)
   - Nice-to-have bugs → backlog

3. **Rehearsal prezentacji (3x):**
   - 30-min pitch (z deckiem)
   - 15-min live demo (gra)
   - 15-min Q&A
   - Time yourself!

4. **Przygotuj odpowiedzi na pytania:**
   - "Ile to kosztuje?" → **15k PLN pilot / 40k full**
   - "Jak mierzymy sukces?" → **KPI: time-to-prod, retention, knowledge score**
   - "Co z integracją CRM?" → **Faza 2 (Salesforce API)**
   - "Mobile app?" → **Faza 3 (Q2 2026)**
   - "Ile czasu zajmuje setup?" → **2 tygodnie (scenariusz + branding)**

**Output:** 
- Zero critical bugs
- Smooth demo flow
- Confident pitch

**Czas:** 2 dni (16h)

---

#### **Dzień 19 (Wtorek, 26 listopada)**
**🎯 PREZENTACJA DLA HEINZ**

**Agenda:**
1. **10 min:** Pitch deck (problem → solution → benefits)
2. **15 min:** Live demo (welcome → tutorial → wizyta → dashboard)
3. **5 min:** Roadmap & pricing
4. **10 min:** Q&A

**Przygotowanie:**
- Demo account: `heinz_demo` / hasło: `demo2024`
- Laptop naładowany, internet backup (hotspot telefon)
- Screen recording jako backup (jeśli live demo crashuje)
- Printed deck (backup jeśli projektor nie działa)

---

## 📊 CHECKLIST PRZED PREZENTACJĄ

### **Technical:**
- [ ] Portfolio 15+ produktów Heinz/Pudliszki (z food cost)
- [ ] Food Cost Calculator działa (popup + auto-pitch)
- [ ] Visit flow end-to-end (conversation → ordering → summary)
- [ ] Tutorial (5-step onboarding)
- [ ] Heinz branding (logo, red theme, welcome screen)
- [ ] Dashboard analytics (przychody, market share, reputation)
- [ ] 25 klientów z GPS (unikalne avatary, profile)
- [ ] Scenariusz Heinz (cele, progression, rewards)
- [ ] Zero critical bugs
- [ ] Beta test (3 osoby ukończyły scenariusz)

### **Business:**
- [ ] Landing page live (URL do wysłania przed meetingiem)
- [ ] Pitch deck (10 slajdów PDF)
- [ ] Screenshots (5-10 high-quality)
- [ ] Demo video (YouTube unlisted backup)
- [ ] Pricing defined (15k pilot, 40k full)
- [ ] Email outreach draft (follow-up po prezentacji)
- [ ] Demo account ready (heinz_demo / demo2024)
- [ ] Rehearsal 3x (30-min pitch + demo)

### **Legal/Admin:**
- [ ] NDA template (jeśli Heinz zażąda)
- [ ] Pilot agreement template (3-month contract)
- [ ] Faktura VAT setup (firma/osoba fizyczna?)

---

## 🎯 SUCCESS METRICS - Jak zmierzyć sukces?

### **Przed prezentacją (19-26 listopada):**
- [ ] 3 beta testerów ukończyło scenariusz (avg time: 2-3h)
- [ ] Zero critical bugs (blocking demo)
- [ ] Landing page live + min 50 views (share w LinkedIn)
- [ ] Deck reviewed przez 2 osoby (feedback uwzględniony)

### **Prezentacja (26 listopada):**
- [ ] Heinz pyta o szczegóły techniczne (zainteresowanie!)
- [ ] Umowa na follow-up meeting (albo "wyślij proposal")
- [ ] Pozytywny feedback na demo

### **Po prezentacji (Q4 2025 - Q1 2026):**
- [ ] Proposal wysłany w 48h
- [ ] Follow-up call w 7 dni
- [ ] Decision: TAK/NIE w 14 dni
- [ ] Pilot kickoff: Styczeń 2026

### **Podczas pilotu (3 miesiące):**
- **Engagement:** 70%+ userów ukończy min 1 scenariusz
- **Learning:** Avg quiz score improvement +25%
- **Satisfaction:** NPS > 50
- **Business impact:** Time-to-first-sale (nowi vs starzy reps)

---

## 💰 BUDGET & RESOURCES

### **Time Investment:**
- **Total:** ~140 godzin (19 dni x ~7-8h/dzień)
- **Your time:** 120h (development, testing, prezentacja)
- **External help:** 20h (design, copy review - opcjonalnie)

### **Costs:**
| Item | Cost | Notes |
|------|------|-------|
| Hosting (Streamlit Cloud) | FREE | Na pilot OK, later: AWS $50/mies |
| Domain | $12/rok | heinz-academy.com |
| Gemini API | FREE tier | 15 requests/min (wystarczy na pilot) |
| Design assets | $0-200 | Canva Pro / Fiverr (opcjonalnie) |
| **TOTAL** | **~$12-212** | Minimalny koszt! |

---

## 🚨 RISK MITIGATION

### **Risk 1: Heinz nie odpowie / odmówi**
**Mitigation:**
- **Plan B:** Unilever, Nestle, Mondelez (już research w FMCG_IMPLEMENTATION_PROGRESS.md)
- **Generic version:** Zmień branding z Heinz → "FMCG Sales Academy" (1 dzień pracy)
- **Pivot:** Inne branże (pharma, automotive, banking)

### **Risk 2: Za dużo customizacji (scope creep)**
**Mitigation:**
- **Pilot = fixed scope** (15k PLN, 3 miesiące, 1 scenariusz)
- **Custom features = Phase 2** (dodatkowy budżet 20-40k)
- **NDA + IP protection** (scenariusz Heinz to Twoja własność intelektualna)

### **Risk 3: Technical issues podczas demo**
**Mitigation:**
- **Backup: Screen recording** (YouTube unlisted, 10-min full demo)
- **Local hosting** (nie cloud) na demo call (no internet dependency)
- **Rehearsal 3x** przed live call (muscle memory)
- **Demo account pre-loaded** z przykładową grą (nie empty state)

### **Risk 4: Pricing za niski/wysoki**
**Mitigation:**
- **Research:** Ile Heinz płaci za tradycyjne szkolenia? (zapytaj recruitment/HR Heinz)
- **Benchmark:** Inne platformy B2B (Moodle: 5-10k, Articulate: 20-50k)
- **Flexibility:** "Możemy dostosować zakres do budżetu" (modular pricing)
- **Value-based:** Podkreślaj ROI (60% oszczędność czasu/kosztu)

---

## 🎓 LESSONS LEARNED (dla przyszłych projektów)

### **Co działało dobrze:**
- ✅ Repository pattern (łatwe dodawanie features)
- ✅ Migracje automatyczne (dodawanie pól do istniejących gier)
- ✅ Discovery System (gamification, stopniowe odkrywanie)
- ✅ AI Conversations (Gemini świetnie radzi sobie z kontekstem)

### **Co można poprawić:**
- ⚠️ Wcześniejsze planowanie portfolio (produkty powinny być na początku)
- ⚠️ Więcej testów jednostkowych (niektóre bugi wychodzą późno)
- ⚠️ Dokumentacja API (dla external integrations w Faze 2)

---

## 📞 SALES PROCESS - Next Steps Po MVP

### **Krok 1: Cold Outreach (27 listopada)**
```
Email do:
- Sales Director Heinz Poland
- HR/L&D Manager Heinz
- Field Sales Manager Heinz

Subject: Skrócenie onboardingu sales reps o 60% - 30-min demo?

Body:
"Cześć [Imię],

Stworzyłem Heinz Sales Academy - platformę symulacyjną dla Food Service reps,
która skraca onboarding z 9 do 3-4 miesięcy i redukuje koszty o 60%.

🎮 Live demo (5 min): [link do landing page]
📊 Measurable impact: Time-to-productivity, retention, knowledge scores

Możemy porozmawiać 30 minut? Pokażę live demo z Twoim brandingiem.

Best,
[Ty]

P.S. Załączam 1-pager z wynikami benchmark (Harvard Business Review)"
```

### **Krok 2: Demo Call (1-7 grudnia)**
- **10 min:** Problem statement + pitch deck
- **15 min:** Live demo (gra + economic tools)
- **5 min:** Q&A + next steps

### **Krok 3: Proposal (8-14 grudnia)**
- Formal proposal (PDF, 5 stron)
- Pricing: 15,000 PLN pilot
- Timeline: Kickoff styczeń 2026
- Deliverables: Scenariusz + portfolio + support

### **Krok 4: Pilot Kickoff (Styczeń 2026)**
- 20-30 userów (sales reps + managers)
- 3 miesiące (styczeń-marzec)
- Weekly check-ins (progress, feedback)
- Final report (marzec 2026): engagement, learning outcomes, business impact

### **Krok 5: Expansion (Kwiecień 2026+)**
- Full deployment (wszystkie regiony Heinz Poland)
- Custom scenarios (nowe produkty, promocje sezonowe)
- CRM integration (Salesforce)
- Mobile app (iOS/Android)

---

## 🚀 MOTIVATION

**26 listopada = 19 dni od teraz**

**To jest realny timeline!**

Masz już 70% pracy zrobionej:
- ✅ Core engine (territory, clients, visits, discovery)
- ✅ AI conversations (Gemini, context, memory)
- ✅ Repository pattern (SQL + JSON)
- ✅ Dashboard analytics (charts, metrics)
- ✅ Notes system (6 categories, sync)

Zostaje 30%:
- Portfolio Heinz (2 dni)
- Economic tools (2 dni)
- Branding (2 dni)
- Tutorial (2 dni)
- Scenariusz (1 dzień)
- Prezentacja (3 dni)
- Testing (2 dni)
= 14 dni solidnej pracy + 5 dni buffer

**You got this!** 💪

---

## 📅 DAILY STANDUP TEMPLATE

Kopiuj to codziennie do trackowania:

```
Data: ___________
Dzień sprintu: ___ / 19

✅ Zrobione wczoraj:
- 
- 

🎯 Plan na dziś:
- 
- 

⚠️ Blockersy:
- 

📊 Progress: ___% (0-100%)

🔥 Priorytet dnia: ______________
```

---

## 🎯 FINAL THOUGHTS

**Klucz do sukcesu:**
1. **Focus:** 1 feature per day (nie rozpraszaj się)
2. **MVP mindset:** "Good enough" > "Perfect"
3. **Test early:** Beta test co 3-4 dni (nie czekaj do końca)
4. **Time-box:** Jeśli task trwa >10h, uproszczaj scope

**Mantra:**
> "Make it work, make it right, make it fast"
> 
> Teraz: **Make it work** (dla Heinz demo)
> Potem: **Make it right** (refactoring po pilotażu)
> Później: **Make it fast** (scalability dla wszystkich regionów)

**Gotowy do startu?** 🚀

Powodzenia! Możesz to zrobić w 19 dni. 💪
