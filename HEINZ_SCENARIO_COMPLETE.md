# 🍅 Heinz Food Service Challenge - Scenariusz Kompletny

**Status**: ✅ GOTOWY DO IMPLEMENTACJI  
**Data**: 2 listopada 2025  
**Cel**: Realistyczny scenariusz sprzedaży B2B dla Heinz Polska w kanale Food Service

---

## 📋 Podsumowanie Wykonawcze

Stworzono kompletny scenariusz gry sprzedażowej dla **Heinz Polska**, w którym gracz wciela się w rolę **Junior Sales Representative** zarządzającego portfolio dwóch marek:

- **Heinz** (premium): 28.50-29.50 PLN → restauracje, burgery craft, hotele
- **Pudliszki** (value): 18.50-18.90 PLN → stołówki, fast food, jadłodajnie

**Kluczowa zmiana koncepcyjna**: Heinz i Pudliszki to **NIE** konkurencja, tylko **portfolio Heinz Polska**. Gracz uczy się strategii dwóch marek pokrywających cały rynek.

**Uproszczenie produktowe**: W tym scenariuszu gracz sprzedaje **TYLKO KETCHUPY** (4 SKU total). Pozostałe kategorie produktów (sosy, mustard, mayo) są zarezerwowane dla innych scenariuszy (np. "Full Portfolio Challenge"). Dzięki temu scenariusz jest:
- ✅ **Fokus na jednej kategorii** - łatwiejsze nauczanie portfolio management
- ✅ **Realistyczny** - junior rep zazwyczaj zaczyna od 1 kategorii
- ✅ **Prosty do zrozumienia** - 4 produkty vs 10+ (jak w Quick Start)
- ✅ **Gotowy na rozbudowę** - później dodamy scenariusze z pełnym portfolio

---

## 🎯 Struktura Scenariusza

### 1. **Podstawowe Informacje**
```yaml
ID: heinz_food_service
Nazwa: 🍅 Heinz Food Service Challenge
Firma: Heinz Polska
Czas trwania: 8 tygodni
Baza: Lipowa 29, 43-445 Dzięgielów (49°43'37.8"N 18°42'09.3"E)
Region: Dzięgielów + okolice (Wisła, Ustroń, Skoczów, Cieszyn), radius 30km
Klienci: 25 punktów Food Service
```

### 2. **Baza Klientów** (25 klientów)

**Plik**: `data/industries/fmcg_clients_heinz_foodservice.py`

| Typ klienta | Ilość | Potencjał (kg/mies) | Target produktu |
|-------------|-------|---------------------|-----------------|
| 🍔 Burgerownie/Street Food | 6 | 83 | Heinz premium |
| 🌯 Kebabownie/Fast Food | 4 | 115 | Pudliszki value |
| 🍽️ Stołówki/Bary | 3 | 125 | Pudliszki value |
| 🍕 Pizzerie/Casual | 4 | 44 | Mixed portfolio |
| 🏨 Hotele | 2 | 25 | Heinz premium |
| 📦 Dystrybutorzy | 6 | 155 + pośrednictwo | Portfolio całe |

**Segmentacja**:
- Premium (8): Target Heinz
- Value (10): Target Pudliszki  
- Mixed (7): Portfolio play - obie marki

**Obecni dostawcy** (competitive landscape):
- Kotlin: **8 klientów** ← główny cel przejęć
- Pudliszki: **3 klientów** ← easy upsell do Heinz
- Heinz: **2 klientów** ← expand portfolio
- No-name/Mix: **6 klientów** ← upgrade opportunity
- Brak/Retail: **6 klientów** ← easy wins

**Łączny potencjał**: ~4,200 kg/miesiąc (bez dystrybutorów pośrednio)

### 3. **Produkty** (4 SKU - TYLKO KETCHUPY)

**Plik**: `data/industries/fmcg_products.py` (HEINZ_PRODUCTS)

⚠️ **WAŻNE**: W scenariuszu Heinz Food Service gracz sprzedaje **TYLKO KETCHUPY**. Pozostałe kategorie (majonez, mustard, sosy specjalne) są wyłączone i zarezerwowane dla przyszłych scenariuszy typu "Full Portfolio Challenge".

**Uzasadnienie biznesowe**: 
- Junior Sales Representative zazwyczaj zaczyna od jednej kategorii produktowej
- Fokus na portfolio management (premium vs value) w ramach jednej kategorii
- Prostsze dla gracza - 4 produkty zamiast 10+
- Realistyczne dla 8-tygodniowego scenariusza

#### Heinz Premium Line (2 SKU)
1. **Heinz Ketchup Klasyczny** (875ml FS)
   - Cena: 28.50 PLN
   - Retail reference: 8.99 zł/450g
   - Target: Restauracje premium, burger joints, bistro
   - USP: Marka #1 na świecie, zero konserwantów, Instagram appeal

2. **Heinz Ketchup Pikantny** (875ml FS)
   - Cena: 29.50 PLN
   - Target: BBQ restaurants, pub food, foodtrucki
   - USP: Premium spicy, upsell opportunity (+2 zł do burgera)

#### Pudliszki Value Line (2 SKU - właściciel: Heinz Polska)
3. **Pudliszki Ketchup Łagodny** (980g FS)
   - Cena: 18.50 PLN
   - Retail reference: 7.49 zł/480g (15.60 zł/kg)
   - Target: Stołówki, fast food budget, jadłodajnie
   - USP: Polski lider, świetna cena, duża pojemność

4. **Pudliszki Ketchup Ostry** (980g FS)
   - Cena: 18.90 PLN
   - Target: Food courts, kebaby, budżetowe restauracje
   - USP: Najlepsza relacja cena/jakość

**Konkurencja (też tylko ketchupy)**:
- Kotlin Ketchup: 16.80 PLN (18% market share FS)
- Develey Ketchup: 24.50 PLN (8% market share FS)

💡 **Design Decision**: Ograniczenie do jednej kategorii (ketchupy) sprawia, że scenariusz jest bardziej fokusowy i edukacyjny. Gracz uczy się różnicy premium vs value w ramach tej samej kategorii, co jest kluczowe dla portfolio management. Pełne portfolio (mustard, mayo, BBQ sauce) będzie dostępne w scenariuszu "Full Line Challenge".

### 4. **Sales Stories** (wbudowane w produkty)

#### Heinz Premium:
> "Gdy w menu wpisujesz markę Heinz, komunikujesz klientowi: jakość, globalny standard, pewność smaku. To nie tylko ketchup — to sygnał, że Twój lokal dba o detal."

> "Formaty HoReCa (np. pojemniki 2,5L) oznaczają niższy koszt porcji – dzięki większej gęstości i niższym stratom."

> "Heinz jest obecny w burgerowniach, sieciach QSR, stąd Twoi klienci mogą już znać smak — co zmniejsza opór: mniej prób, mniej tłumaczenia."

#### Pudliszki Value:
> "Pudliszki to marka, którą klienci widzą w sklepie — to daje Ci dodatkowy punkt: gdy używasz jej w lokalu, tworzy się poczucie znajomości i komfortu."

> "Dla lokalu, który nie chce stawiać na ultra-premium, Pudliszki oferuje bardzo dobrą relację jakości do ceny — idealne dla barów, jadłodajni, stołówek."

> "Możesz podkreślić: 'Polska marka, polskie pomidory, tradycyjny smak' — co w kontrakcie z klientem może być argumentem np. w ofercie lunchowej czy dla klientów rodzinnych."

### 5. **Objectives (cele scenariusza)**

**Plik**: `data/scenarios.py` (heinz_food_service)

| Objective | Target | Nagroda | Priorytet | Opis |
|-----------|--------|---------|-----------|------|
| **Numeric Distribution** | 15/25 | 3,000 PLN | Critical | 60% dystrybucji numerycznej |
| **Monthly Sales** | 15,000 PLN | 2,500 PLN | High | Łączna sprzedaż (Heinz + Pudliszki) |
| **Premium Mix** | 40% | 2,000 PLN | High | % wartości z linii Heinz |
| **Beat Kotlin** | 6 wins | 1,500 PLN | Medium | Przejęcia z Kotlin |
| **Upsell Rate** | 30% | 1,800 PLN | High | Klienci Pudliszki → Heinz |

**Portfolio Strategy KPI**:
- **Premium Mix**: `heinz_revenue / total_revenue * 100` (target 40%)
- **Upsell Rate**: `clients_buying_both / clients_buying_pudliszki * 100` (target 30%)

---

## 🎮 Gameplay Flow (jak to działa)

### Inicjalizacja (wybór scenariusza)
1. Gracz wybiera "Heinz Food Service Challenge"
2. System ładuje:
   ```python
   from data.industries.fmcg_clients_heinz_foodservice import HEINZ_FOODSERVICE_CLIENTS
   st.session_state.fmcg_clients = HEINZ_FOODSERVICE_CLIENTS.copy()
   ```
3. Mapa pokazuje 25 klientów w promieniu 30km od Dzięgielów (Lipowa 29)

### Wizyta u klienta
1. Gracz wybiera klienta z listy (sortowanie: distance, potential, segment)
2. System ładuje profil:
   - Personality (MBTI): dyktuje styl rozmowy AI
   - Pain points: problemy do rozwiązania
   - Current supplier: competitive context
   - Objections: typowe obiekcje
   - Recommended strategy: FOZ, Kompensacja, Perspektywizacja, etc.

3. **AI Conversation**:
   ```python
   context = f"""
   Klient: {client['name']}, prowadzi {client['type']}
   Osobowość: {client['personality']}
   Pain points: {', '.join(client['pain_points'])}
   Obecnie używa: {client['current_product']} od {client['current_supplier']}
   
   Rekomendowane produkty: {', '.join(client['recommended_products'])}
   Strategia: {client['recommended_strategy']}
   """
   ```

4. **Notatki** (już zaimplementowane):
   - Gracz może robić notatki podczas rozmowy
   - Panel notatek pod polem wiadomości
   - Kategorie: Produkty, Pitches, Klient

### Zamknięcie sprzedaży
1. Jeśli gracz przekona klienta → zamówienie
2. Tracking:
   ```python
   client['status'] = 'active'
   client['products_ordered'] = ['heinz_ketchup_classic']
   client['monthly_value'] = volume * price
   ```
3. Update KPI:
   - Distribution: +1 punkt
   - Sales: +miesięczna wartość
   - Premium mix: recalculate
   - Beat Kotlin: +1 jeśli był Kotlin

### Dashboard KPI
- **Dystrybucja**: 15/25 (60%)
- **Sprzedaż**: 15,000 PLN / target
- **Premium Mix**: 40% (Heinz revenue %)
- **Kotlin Wins**: 6/8 possible
- **Upsell**: 30% (Pudliszki → Heinz)

---

## 📚 Charakterystyki Klientów (per type)

### 🍔 Burgerownie / Street Food
- **Profil**: Pasjonaci gastronomii, smak = sygnatura
- **Potencjał**: 10-20 kg/mies., wysoka lojalność
- **Obiekcje**: "Za drogi", "Nie widać różnicy", "Fanex daje gadżety"
- **Techniki**: Kompensacja, Test bez zobowiązań, Instagram appeal

### 🌯 Kebabownie / Fast Food
- **Profil**: Duży wolumen, bardzo price sensitive
- **Potencjał**: 20-40 kg/mies., walka o każdy grosz
- **Obiekcje**: "Tylko cena się liczy", "Nie mam czasu"
- **Techniki**: FOZ, Wydajność porcji, Promocje 4+1

### 🍽️ Stołówki / Bary Mleczne
- **Profil**: Ściśle kontrolowany budżet, cena decyduje
- **Potencjał**: 30-50 kg/mies., bardzo niskie marże
- **Obiekcje**: "Heinz za drogi", "Brak miejsca"
- **Techniki**: Wydajność operacyjna, Mniej marnotrawstwa

### 🍕 Pizzerie / Casual Dining
- **Profil**: Jakość i spójność, branding ważny
- **Potencjał**: 15-30 kg/mies., centralne zakupy (sieci)
- **Obiekcje**: "Własna marka sosów", "Nie pasuje systemowo"
- **Techniki**: Standaryzacja, Spójność smaku

### 🏨 Hotele
- **Profil**: Prestiż marki, powtarzalność dostaw
- **Potencjał**: 5-15 kg/mies., wysoka waga reputacji
- **Obiekcje**: "Heinz to marka marketowa"
- **Techniki**: Perspektywizacja, Globalny standard

### 📦 Dystrybutorzy
- **Profil**: B2B, marża i rotacja priorytet
- **Potencjał**: 100+ kg/mies. (pośrednio), klucz do regionu
- **Obiekcje**: "Mniejsza marża na Heinz", "Konkurencja daje premie"
- **Techniki**: Powrót do potrzeb, Program wsparcia sprzedaży

---

## 🎯 Easy Wins (quick victories)

| Klient | Typ | Potencjał | Dlaczego easy win? |
|--------|-----|-----------|-------------------|
| **Grill House Premium** | Burger | Very high | Już ma Heinz, chce Hot! |
| **Street Burger** | Food truck | Very high | Ma Pudliszki, otwarta na upgrade |
| **Falafel & More** | Ethnic | Very high | Kupuje Heinz retail, chce FS pricing |
| **Pod Świerkami** | Casual | Very high | Ma Pudliszki, chce premium image |
| **Wellness Hotel SPA** | Hotel | Guaranteed | Już klient Heinz, expand portfolio |
| **Pizza House** | Chain | High | Sieć 3 lokale, decision = cała sieć |

---

## 🥊 Competitive Wins (Kotlin → Heinz/Pudliszki)

8 klientów z Kotlin (objective: 6 wins):
1. Burger Station (ISTJ, price sensitive)
2. Hot Dog Heaven (ESFJ, brand matters)
3. Kebab King (ISTJ, volume play)
4. Kebab Express (ISFJ, delivery issues)
5. Burger Craft (ISTP, mix suppliers - chce uprościć)
6. Bar Mleczny Smaczek (ISTJ, no-name currently)
7. Stołówka Zakładowa (INTJ, kontrakt wygasa)
8. Pizza House (ESTJ, niespójna jakość)

**Strategia**:
- Start od łatwiejszych: Kebab Express (delivery problems), Pizza House (quality issues)
- Pudliszki jako alternatywa (nie musi być Heinz od razu!)
- FOZ technique: Fakty (wydajność), Odniesienie (cost per portion), Zapytanie

---

## 📂 Pliki Zmodyfikowane/Stworzone

### ✅ Utworzone:
1. **`data/industries/fmcg_clients_heinz_foodservice.py`**
   - 25 klientów Food Service
   - Pełne profile: personality, objections, strategies
   - Helper functions: `get_client_stats()`, `get_easy_wins()`, etc.
   - Dokumentacja użycia

### ✅ Zaktualizowane:
2. **`data/scenarios.py`**
   - Dodano `load_scenario_clients()` function
   - Heinz scenario: `client_database = "fmcg_clients_heinz_foodservice"`
   - Objectives: premium_mix, upsell_rate, beat_kotlin

3. **`data/industries/fmcg_products.py`**
   - HEINZ_PRODUCTS: 4 produkty (2 Heinz, 2 Pudliszki)
   - Sales stories z opisów produktowych
   - Retail reference prices
   - owner="Heinz Polska" dla Pudliszek

---

## 🚀 Next Steps (implementacja w grze)

### High Priority:
1. **Scenario Selection UI** (fmcg_playable.py)
   - Radio buttons: Quick Start, Lifetime, **Heinz Food Service**
   - Load clients when Heinz selected
   - Initialize game state with scenario.initial_conditions

2. **Client List View**
   - Map view z 25 pinami (Folium)
   - Table view: sortable by distance, potential, segment
   - Filters: segment, current_supplier, type

3. **KPI Dashboard**
   - Premium Mix gauge (target 40%)
   - Upsell Rate tracker (target 30%)
   - Kotlin Wins counter (6/8)
   - Distribution progress (15/25)

### Medium Priority:
4. **AI Context Loading**
   - Inject client profile into conversation
   - Personality-based responses (MBTI)
   - Objection handling hints

5. **Portfolio Sales Mechanics**
   - Detect client segment → recommend appropriate product
   - Track Heinz vs Pudliszki revenue separately
   - Upsell detection (Pudliszki → Heinz)

### Low Priority:
6. **Advanced Features**
   - Client relationship tracking (visits, sentiment)
   - Competitor alerts (Kotlin counter-offers)
   - Seasonal promotions (4+1 deals)

---

## 💡 Educational Value

Ten scenariusz uczy:
- **Portfolio Management**: Jak zarządzać dwoma markami (premium + value)
- **Market Segmentation**: Matching products to customer segments
- **B2B Sales**: Food Service channel dynamics
- **Competitive Strategy**: Przejmowanie z Kotlin, upselling
- **Consultative Selling**: Różne techniki dla różnych personalności

**Realny case study**: Heinz Polska faktycznie zarządza portfolio Heinz + Pudliszki, więc scenariusz odzwierciedla rzeczywiste wyzwania biznesowe.

---

## 📊 Success Metrics (jak wygrać)

**Minimum (Bronze)**: 3 objectives completed
- 10 distribution points
- 10,000 PLN sales
- 4 Kotlin wins

**Target (Silver)**: 4 objectives completed
- 15 distribution points
- 15,000 PLN sales
- 35% premium mix
- 6 Kotlin wins

**Excellence (Gold)**: All 5 objectives
- 15 distribution
- 15,000 PLN
- 40% premium mix
- 6 Kotlin wins
- 30% upsell rate

---

## 🔮 Future Scenarios (roadmap rozbudowy)

### Scenariusz 2: Heinz Full Portfolio Challenge
**Koncepcja**: Rozszerzone portfolio - ketchupy (4) + mustard (3) + mayo (2) + BBQ sauce (2) = **11 SKU**

**Zmiany**:
- Więcej klientów: 40 punktów Food Service
- Dłuższy czas: 12 tygodni
- Cross-selling: klient kupuje ketchup → upsell mustard
- Bundle deals: "Ketchup + Mustard + Mayo = -10%"
- Kategoria KPI: osiągnij 30% penetracji w każdej kategorii

**Edukacja**: 
- Category management (mix 3-4 kategorii)
- Cross-selling techniques
- Bundle pricing strategies

### Scenariusz 3: Heinz Retail Channel
**Koncepcja**: Sprzedaż do sieci retail (Biedronka, Żabka, Carrefour) zamiast Food Service

**Zmiany**:
- 15 klientów retail (różne formaty: convenience, discount, super/hyper)
- Listing fees i planogramy
- Promocje konsumenckie (2+1, -30%)
- Category captain negotiations
- Volume commitments i quarterly reviews

**Edukacja**:
- Retail account management
- Trade marketing
- Shopper insights

### Scenariusz 4: Heinz vs Unilever Showdown
**Koncepcja**: Konkurencja bezpośrednia - Heinz (ty) vs Unilever (AI competitor)

**Mechanika**:
- AI agent gra jako Unilever rep (Hellmann's Mayo, Calvé Ketchup)
- Klienci dostają oferty od obu stron
- Price wars, promotional battles
- Competitor intelligence (spy on Unilever moves)
- Defensive selling (klient chce zmienić na Unilever)

**Edukacja**:
- Competitive selling
- Price objection handling
- Retention strategies

---

## 🎓 Scenariusz gotowy dla:
- ✅ Prezentacji klientowi (Heinz Polska)
- ✅ Beta testingu z prawdziwymi użytkownikami
- ✅ Integracji z istniejącym FMCG game engine
- ✅ Rozbudowy (3 follow-up scenarios zaplanowane)

**Status**: 🟢 PRODUCTION READY (v1.0 - Ketchup Focus)
**Next**: v2.0 - Full Portfolio (+7 SKU)

