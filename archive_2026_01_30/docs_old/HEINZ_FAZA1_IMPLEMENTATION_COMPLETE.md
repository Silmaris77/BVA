# 🍅 HEINZ FOOD SERVICE - FAZA 1 IMPLEMENTATION COMPLETE

## ✅ Data zmian: 2025-01-27

## 📋 Zakres implementacji

### FAZA 1: Struktura danych - "Through Distributor" Model

Zmiana modelu biznesowego z **Direct Sales** na **Through Distributor**:
- Handlowiec (PH) **nie przyjmuje zamówień bezpośrednio**
- PH **przekonuje** szefów kuchni do produktów Heinz
- Restauracje **zamawiają przez dystrybutorów**
- Sukces mierzony przez **pull-through rate** (nie direct orders)

---

## 🗂️ Nowe pliki danych

### 1. `data/fmcg/distributors.json` (5 dystrybutorów HoReCa)

**Dystrybutorzy:**
1. **Farutex** - Premium HoReCa (Kraków & Katowice)
2. **Transgourmet** - Sieci & Stołówki (national chains)
3. **Bidfood** - Nowoczesna gastronomia (fine dining, craft burgers)
4. **Selgros HoReCa** - Cash & Carry Value (bary, fast foody)
5. **Orbico** - Hotele & Wydarzenia (premium catering)

**Struktura danych dystrybutora:**
```json
{
  "id": "farutex",
  "name": "Farutex - Premium HoReCa Distribution",
  "segment": "premium_horeca",
  "description": "...",
  "heinz_stock_level": "wysoki|średni|niski|brak",
  "monthly_heinz_sales_kg": 450,
  "relationship_score": 70,
  "active_customers_using_heinz": 18,
  "pull_through_rate": 32.5,
  "brands_portfolio": ["Heinz", "Hellmann's", "Knorr", ...],
  "contact_person": {
    "name": "Jan Kowalski",
    "role": "Key Account Manager HoReCa",
    "phone": "+48 601 234 567",
    "email": "jan.kowalski@farutex.pl"
  },
  "cooperation_level": "partner|neutral|cold",
  "last_meeting_date": "2025-01-10",
  "next_joint_visit_available": true
}
```

---

### 2. `data/fmcg/heinz_products.json` (6 SKU - FIXED PORTFOLIO)

**Produkty (dokładnie te 6, nie inne!):**

1. **Heinz Ketchup Premium 5kg** - 29.50 PLN
   - Brix 29%, wysoka wydajność, premium positioning
   - Idealny do: burgerów, frytek, hot dogów

2. **Heinz Majonez Delikatny 5kg** - 42.00 PLN
   - Stabilny w temperaturze, baza do sosów
   - Cross-sell: Korean Sauce (fusion mayo)

3. **Heinz BBQ Sauce Original 2.5kg** - 36.00 PLN
   - Upside-down butla, uniwersalny
   - Premium perceived value, marynaty

4. **Heinz Sticky Korean Sauce 2.35kg** - 44.00 PLN
   - Trendowy, azjatycki profil smakowy
   - Innowacja: "Korean Mayo" (z majonezem)

5. **Pudliszki Ketchup Łagodny 5kg** - 18.90 PLN
   - Value segment, polskie pomidory
   - Dla stołówek, fast foodów (pressure na koszt)

6. **Heinz Mayonnaise Professional 10L** - 72.00 PLN
   - Bag-in-box system, wysoka wydajność
   - Dla dużych sieci QSR i cateringu

**Struktura danych produktu:**
```json
{
  "id": "heinz_ketchup_premium_5kg",
  "name": "Heinz Ketchup Premium 5kg",
  "category": "Sosy pomidorowe",
  "brand": "Heinz",
  "format": "Wiadro 5kg",
  "price_distributor": 29.50,
  "food_cost_per_portion_20g": 0.12,
  "portions_per_unit": 250,
  "positioning": "Premium",
  "usp": "Najgęstszy ketchup w segmencie HoReCa (Brix 29%). Wysoka wydajność: o 15% mniejsze zużycie niż tańsze marki.",
  "margin_percent": 35.0,
  "ideal_customer_segments": ["premium", "mixed"],
  "cross_sell_products": ["heinz_majonez_delikatny_5kg", "heinz_bbq_sauce_original_2_5kg"]
}
```

---

### 3. `data/fmcg/clients_heinz.json` (10 przykładowych restauracji)

**Nowe pola klientów:**

```json
{
  "id": "rest_002",
  "name": "Bistro Urban Kitchen",
  "address": "ul. Floriańska 25, Kraków",
  "type": "Bistro modern",
  "segment": "premium",
  
  // ⬇️ NOWE POLA - "Through Distributor" Model
  
  "distributor_id": "bidfood",  // Który dystrybutor obsługuje restaurację
  
  "convinced_products": {  // Produkty, które chef używa (zamawia przez dystrybutora)
    "heinz_ketchup_premium_5kg": {
      "convinced_date": "2025-01-20",
      "ordering_status": "active|trial|paused|stopped",
      "monthly_volume_kg": 10.0,
      "conviction_progress": 100  // 0-100%
    }
  },
  
  "current_competitors": {  // Co używają ZANIM przekonamy do Heinz
    "ketchup": "Heinz (przekonano!)",
    "majonez": "Develey",
    "korean_sauce": "brak (okazja)"
  },
  
  "chef_name": "Anna Nowak",
  "chef_phone": "+48 602 345 678",
  "decision_maker": "Chef",
  "monthly_covers": 950,
  "avg_check": 70.00,
  "relationship_score": 60,
  "last_visit_date": "2025-01-20",
  "visits_count": 3,
  "notes": "Przekonana do Heinz Ketchup Premium. Zainteresowana Korean Sauce do 'fusion burgers'."
}
```

**Stan początkowy (10 klientów):**
- **rest_002** (Bistro Urban Kitchen): ✅ Heinz Ketchup Premium
- **rest_004** (Burger House Premium): ✅✅ Ketchup + Majonez
- **rest_005** (Hotel Wawel): 🧪 Korean Sauce (test, 75% conviction)
- **rest_009** (Smokehouse): ✅ BBQ Sauce
- **rest_010** (Burger King): ✅✅ Mayo 10L + Ketchup (największy klient!)
- **rest_001, rest_003, rest_006, rest_007, rest_008**: Cold leads (0 przekonanych produktów)

---

## 🔧 Zmiany w kodzie

### 1. `utils/business_game.py`

**Nowa funkcja:**
```python
def load_heinz_clients():
    """
    Ładuje klientów z clients_heinz.json dla scenariusza Heinz Food Service
    
    Returns:
        Dict: Słownik klientów {client_id: client_data}
    """
    clients_path = os.path.join("data", "fmcg", "clients_heinz.json")
    
    if not os.path.exists(clients_path):
        return {}
    
    with open(clients_path, 'r', encoding='utf-8') as f:
        clients_data = json.load(f)
    
    return clients_data
```

**Zaktualizowana funkcja `initialize_fmcg_game_new()`:**
```python
elif scenario == "heinz_food_service":
    # Heinz scenario - ładuje klientów z clients_heinz.json
    game_state = initialize_fmcg_game_state(
        territory="Dzięgielów Food Service",
        lat=49.7271667,
        lon=18.7025833
    )
    game_state["company"] = "Heinz Polska"
    
    # ⬇️ NOWE: Załaduj klientów Heinz Food Service
    heinz_clients = load_heinz_clients()
    game_state["clients"] = heinz_clients
    game_state["clients_prospect"] = len([c for c in heinz_clients.values() if not c.get("convinced_products")])
    game_state["clients_active"] = len([c for c in heinz_clients.values() if c.get("convinced_products")])
```

---

### 2. `client_detail_card.py`

**Nowe importy:**
```python
import json
import os
```

**Nowe funkcje pomocnicze:**
```python
def _load_distributors():
    """Ładuje dane dystrybutorów z JSON"""
    distributor_path = os.path.join("data", "fmcg", "distributors.json")
    if os.path.exists(distributor_path):
        with open(distributor_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def _load_heinz_products():
    """Ładuje produkty Heinz z JSON"""
    products_path = os.path.join("data", "fmcg", "heinz_products.json")
    if os.path.exists(products_path):
        with open(products_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
```

**Nowa sekcja UI - SECTION 2A: 🚚 Dystrybutor:**
- Profil dystrybutora (nazwa, segment)
- Stan magazynu Heinz (wysoki/średni/niski/brak)
- Sprzedaż miesięczna dystrybutora (kg)
- Relacja z dystrybutorem (0-100)
- Pull-Through Rate (%)
- Osoba kontaktowa (imię, rola, telefon, email)
- **Akcje współpracy:**
  - 📞 Zadzwoń (5 pkt aktywności)
  - 🤝 Wspólna wizyta (+20% convince chance, raz na 7 dni)
  - 📊 Raport sprzedaży (10 pkt, pull-through report)

**Nowa sekcja UI - SECTION 2B: 🎯 Portfolio produktowe:**
- **Przekonane produkty Heinz** (expandable list):
  - Status: ✅ Active | 🧪 Trial | ⏸️ Paused | ❌ Stopped
  - Data przekonania
  - Wolumen miesięczny (kg)
  - Conviction progress (0-100%)
- **Obecnie używane marki (konkurencja)** (expandable):
  - Lista kategorii → marka
  - Okazje do upsell (jeszcze nieprzekonane)

---

## 🎮 Gameplay Flow (FAZA 1 - current state)

### Przed wizytą:
1. PH widzi profil klienta
2. Sprawdza dystrybutora (stock level, relacja, pull-through)
3. Analizuje convinced_products vs current_competitors
4. Może zadzwonić do dystrybutora (sprawdzić stock)
5. Może zaplanować **wspólną wizytę** z dystrybutorem (+20% convince chance)

### Podczas wizyty (TODO - FAZA 2):
- Discovery → Pitch → Convince (3-etapowy flow)
- Gemini AI ocenia argumenty gracza
- Conviction progress rośnie 0% → 100%
- Nie ma bezpośredniego zamówienia (to nie direct sales!)

### Po wizycie (TODO - FAZA 2):
- Jeśli convinced=True: Chef dzwoni do dystrybutora (background)
- Zamówienie pojawia się w **miesięcznym raporcie** (nie natychmiast!)
- Gracz może zadzwonić do dystrybutora: "📞 Call Distributor" → check order status

### Dashboard KPI (TODO - FAZA 3):
- **Sell-Out Volume** (40%) - ile kg sprzedał dystrybutor restauracjom
- **Active Clients** (30%) - ile restauracji regularnie zamawia
- **Pull-Through Rate** (20%) - % Heinz stock → sprzedaż
- **Relationship Index** (10%) - średnia relacja z klientami + dystrybutorami

**Quarterly goal:**
- 1200 kg total sales (sell-out volume)
- 15 active clients
- 35% penetration rate

---

## 🔮 Następne kroki (FAZA 2-4)

### FAZA 2: Convince Mechanics (TODO)
- [ ] Zmienić visit goal: "order" → "convince"
- [ ] 3-etapowy flow: Discovery → Pitch → Convince
- [ ] AI (Gemini) ocenia argumenty gracza
- [ ] Conviction progress bar (0-100%)
- [ ] Delayed order simulation (background call to distributor)
- [ ] "📞 Call Distributor" action (check order status)

### FAZA 3: Dashboard & KPI (TODO)
- [ ] Monthly reports (Sell-Out Volume, Active Clients, Pull-Through, Relationship)
- [ ] Quarterly goals dashboard
- [ ] Distributor dashboard (stock levels, heinz sales, pull-through %)

### FAZA 4: Full Client Detail Card Integration (TODO)
- [ ] Joint Visit mechanics (+20% convince, costs points)
- [ ] Trade Promotion mechanics (30 pts, boost distributor stock)
- [ ] Call Distributor mechanics (5 pts, instant stock check)
- [ ] Sales Report mechanics (10 pts, detailed pull-through analysis)

---

## 📊 Business Model Comparison

| Aspekt | OLD (Direct Sales) | NEW (Through Distributor) |
|--------|-------------------|---------------------------|
| **Visit Goal** | Złóż zamówienie | Przekonaj szefa kuchni |
| **Order Flow** | PH → Direct Order → Revenue | PH → Convince Chef → Chef calls Distributor → Monthly Report |
| **Success Metric** | Revenue (PLN) | Pull-Through Rate (%) |
| **KPI** | Sales Volume | Sell-Out Volume, Active Clients, Pull-Through, Relationship |
| **Visit Result** | Order (immediate) | Conviction (delayed order) |
| **Key Action** | "Złóż zamówienie" | "Przekonaj do Heinz" |
| **Portfolio** | Unlimited products | Fixed 6 SKU |
| **Channel Partner** | None | 5 Distributors |

---

## ✅ Status: FAZA 1 COMPLETE

**Zaimplementowane:**
- ✅ Distributors data structure (5 distributors)
- ✅ Heinz products catalog (6 SKU fixed)
- ✅ Clients with distributor model (10 example restaurants)
- ✅ Client detail card UI (Distributor section + Portfolio section)
- ✅ Backend integration (load_heinz_clients, initialize_fmcg_game_new)

**Gotowe do testowania:**
- Wybierz scenariusz "🍅 Heinz Food Service Challenge - Dzięgielów"
- Aplikacja załaduje 10 klientów z `clients_heinz.json`
- W karcie klienta zobaczysz:
  - 🚚 Dystrybutor (profil, stock, akcje)
  - 🎯 Portfolio produktowe (przekonane produkty + konkurencja)

**Następny krok:** Implementacja FAZA 2 (Convince Mechanics)

---

## 🧪 Test Scenarios

### Test 1: Cold Lead (rest_001 - Karczma u Bazyla)
- Dystrybutor: Farutex
- Convinced products: 0
- Current competitors: Pudliszki (ketchup), Winiary (mayo)
- **Okazja:** Premium products (chef zainteresowany)

### Test 2: Active Client (rest_004 - Burger House Premium)
- Dystrybutor: Transgourmet
- Convinced products: 2 (Ketchup 25kg/mies, Mayo 15kg/mies)
- **Okazja:** BBQ Sauce (używają Develey)

### Test 3: Trial Client (rest_005 - Hotel Wawel)
- Dystrybutor: Orbico
- Convinced products: 1 (Korean Sauce - 🧪 TRIAL, 75% conviction)
- **Okazja:** Przekonać do whole portfolio (relacja 70/100!)

### Test 4: Key Account (rest_010 - Burger King)
- Dystrybutor: Transgourmet
- Convinced products: 2 (Mayo 10L - 80kg/mies!, Ketchup - 60kg/mies)
- **Status:** Klient modelowy, utrzymać relację!

---

**Data implementacji:** 2025-01-27  
**Autor:** GitHub Copilot + pksia  
**Wersja:** FAZA 1 - Data Structure Complete
