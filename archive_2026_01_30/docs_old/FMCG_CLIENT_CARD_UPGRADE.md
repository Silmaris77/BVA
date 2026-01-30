# 🎴 FMCG: Rozbudowa Karty Klienta - Plan Implementacji

## 📋 AKTUALNY STAN (28.10.2025)

### ✅ Co już działa:
1. **Baza klientów** (`data/industries/fmcg_customers.py`):
   - 6 klientów Traditional Trade z pełnymi profilami
   - Dane: nazwa, właściciel, lokalizacja, opis, personality, pain points
   - `initial_status: "prospect"` (ale brak ACTIVE/LOST)
   - `relationship_score: 0` (ale to NIE jest nasza reputacja)

2. **UI - Lista klientów** (`views/.../fmcg.py :: show_fmcg_customers_tab`):
   - Podział na Prospects / Active
   - Expander z podstawowymi info
   - Przycisk "Umów spotkanie" → AI conversation
   - Historia conversations (liczba spotkań)

3. **AI Conversations**:
   - System rozmów z klientami działa
   - Speech-to-text integration
   - Zapis historii w `user_data["business_games"]["fmcg"]["conversations"]`

### ❌ Czego brakuje (według FMCG_GAME_DESIGN.md):
1. **Parametry ACTIVE klienta:**
   - `status` (PROSPECT/ACTIVE/LOST)
   - `reputation` (-100 do +100)
   - `last_visit_date`
   - `visit_frequency_required` (dni)
   - `products_portfolio` (JSON array)
   - `monthly_value` (PLN)
   - `market_share_vs_competition` (%)
   - `contract_renewal_date`
   - `satisfaction_score` (1-5)

2. **Listing produktów:**
   - Array produktów z FreshMarket u każdego klienta
   - Dane per produkt: volume, market share, shelf placement
   - Możliwość cross-sell (dodawanie nowych produktów)

3. **Timeline eventów:**
   - Historia współpracy (nie tylko conversations)
   - Events: first_visit, contract_signed, regular_visit, cross_sell, late_visit, etc.
   - Zmiany reputacji w czasie

4. **Szczegółowa karta klienta:**
   - Widok reputacji z wizualizacją
   - Lista produktów u klienta
   - Udziały PH vs konkurencja
   - Timeline współpracy
   - Zadania związane z tym klientem
   - Statystyki (dni współpracy, liczba wizyt, avg rating)

---

## 🚀 PLAN IMPLEMENTACJI (3 etapy)

### **ETAP 1: Rozszerzenie struktury danych** 📝 (1-2 dni)

#### 1.1. Definicja nowego modelu klienta w `user_data`

**Zmiana w strukturze:**
```python
# PRZED (aktualnie):
user_data["business_games"]["fmcg"] = {
    "customers": {
        "prospects": ["trad_001", "trad_002"],  # tylko ID
        "active_clients": []                    # tylko ID
    },
    "conversations": {
        "trad_001": [...]
    }
}

# PO (nowa struktura):
user_data["business_games"]["fmcg"] = {
    "clients": {  # NOWA nazwa klucza (clients zamiast customers)
        "trad_001": {  # ID klienta jako klucz
            # === PODSTAWOWE ===
            "status": "ACTIVE",  # PROSPECT / ACTIVE / LOST
            "reputation": 65,    # -100 do +100
            
            # === PROSPECT-specific ===
            "interest_level": 7,      # 0-10 (tylko dla PROSPECT)
            "first_contact_date": "2025-10-01",
            "visits_count": 2,        # ile wizyt jako PROSPECT
            "decision_deadline": "2025-10-30",  # maks data decyzji
            
            # === ACTIVE-specific ===
            "last_visit_date": "2025-10-20",
            "visit_frequency_required": 14,  # dni między wizytami
            "contract_signed_date": "2025-10-05",
            "contract_renewal_date": "2026-04-05",  # +6 miesięcy
            "monthly_value": 3500,    # PLN/miesiąc (suma produktów)
            "satisfaction_score": 4.2,  # 1-5
            
            # === PRODUKTY U KLIENTA ===
            "products_portfolio": [
                {
                    "product_id": "fresh_soap",
                    "product_name": "FreshSoap (250ml)",  # dla UI
                    "category": "Personal Care / Mycie",
                    "date_added": "2025-10-05",
                    "monthly_volume": 50,  # sztuk
                    "unit_price": 12.50,   # PLN
                    "monthly_value": 625,  # 50 × 12.50
                    "market_share": 30,    # % vs konkurencja
                    "shelf_placement": "prime",  # prime/standard/poor
                    "last_promotion": "2025-10-15",
                    "sales_trend": "growing"  # growing/stable/declining
                },
                {
                    "product_id": "fresh_shampoo",
                    "product_name": "FreshShampoo (400ml)",
                    "category": "Personal Care / Włosy",
                    "date_added": "2025-10-12",
                    "monthly_volume": 30,
                    "unit_price": 18.00,
                    "monthly_value": 540,
                    "market_share": 25,
                    "shelf_placement": "standard",
                    "last_promotion": null,
                    "sales_trend": "stable"
                }
            ],
            
            # === TIMELINE EVENTÓW ===
            "timeline": [
                {
                    "date": "2025-10-01",
                    "event_type": "first_visit",
                    "description": "Pierwsze spotkanie (cold call)",
                    "rating": null,
                    "reputation_change": 0,
                    "details": {"conversation_id": "conv_001"}
                },
                {
                    "date": "2025-10-05",
                    "event_type": "contract_signed",
                    "description": "Podpisanie kontraktu - 2 produkty",
                    "rating": 5,
                    "reputation_change": +50,  # start z 50 rep
                    "details": {
                        "products": ["fresh_soap", "fresh_shampoo"],
                        "monthly_value": 1165
                    }
                },
                {
                    "date": "2025-10-08",
                    "event_type": "regular_visit",
                    "description": "Wizyta regularna - kontrola ekspozycji",
                    "rating": 4.5,
                    "reputation_change": +5,
                    "details": {"conversation_id": "conv_002"}
                },
                {
                    "date": "2025-10-12",
                    "event_type": "cross_sell",
                    "description": "Cross-sell: FreshShampoo",
                    "rating": 5,
                    "reputation_change": +15,
                    "details": {"new_product": "fresh_shampoo", "added_value": 540}
                },
                {
                    "date": "2025-10-20",
                    "event_type": "task_completed",
                    "description": "Wykonano: Promocja FreshSoap",
                    "rating": 4,
                    "reputation_change": +5,
                    "details": {"task_id": "task_123"}
                }
            ],
            
            # === LOST-specific (jeśli status=LOST) ===
            "lost_date": null,
            "lost_reason": null,
            "last_reputation": null,  # ostatnia rep przed utratą
            "win_back_attempts": 0,
            "win_back_difficulty": 5.0,
            
            # === STATYSTYKI (wyliczane dynamicznie) ===
            "stats": {
                "days_cooperation": 19,  # od contract_signed_date
                "total_visits": 3,
                "avg_visit_rating": 4.5,
                "total_products": 2,
                "total_monthly_value": 1165,
                "market_share_avg": 27.5  # średnia wszystkich produktów
            }
        },
        
        "trad_002": {
            "status": "PROSPECT",
            "reputation": 0,
            "interest_level": 6,
            "first_contact_date": "2025-10-22",
            "visits_count": 1,
            "decision_deadline": "2025-11-05",
            "products_portfolio": [],  # puste dla PROSPECT
            "timeline": [
                {
                    "date": "2025-10-22",
                    "event_type": "first_visit",
                    "description": "Pierwsze spotkanie - zainteresowany",
                    "rating": null,
                    "reputation_change": 0
                }
            ]
        }
    },
    
    # Zachowujemy conversations (backward compatibility)
    "conversations": {
        "trad_001": [...]
    }
}
```

#### 1.2. Migracja danych (backward compatibility)

**Plik:** `data/industries/fmcg_data_migration.py` (NOWY)

```python
"""
Migracja danych FMCG: stara struktura → nowa struktura z clients
"""

def migrate_fmcg_customers_to_clients(user_data):
    """
    Konwertuje starą strukturę (prospects/active_clients jako listy ID)
    na nową strukturę (clients jako dict z pełnymi parametrami)
    """
    from datetime import datetime, timedelta
    
    bg_data = user_data["business_games"].get("fmcg", {})
    
    # Sprawdź czy już zmigrowane
    if "clients" in bg_data:
        return  # Already migrated
    
    # Stare dane
    old_customers = bg_data.get("customers", {})
    prospects_ids = old_customers.get("prospects", [])
    active_ids = old_customers.get("active_clients", [])
    
    # Nowa struktura
    clients = {}
    
    # Migruj PROSPECTS
    for client_id in prospects_ids:
        clients[client_id] = {
            "status": "PROSPECT",
            "reputation": 0,
            "interest_level": 5,  # domyślna wartość
            "first_contact_date": datetime.now().strftime("%Y-%m-%d"),
            "visits_count": 0,
            "decision_deadline": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
            "products_portfolio": [],
            "timeline": []
        }
    
    # Migruj ACTIVE (jeśli były)
    for client_id in active_ids:
        clients[client_id] = {
            "status": "ACTIVE",
            "reputation": 50,  # domyślna wartość startowa
            "last_visit_date": datetime.now().strftime("%Y-%m-%d"),
            "visit_frequency_required": 14,
            "contract_signed_date": datetime.now().strftime("%Y-%m-%d"),
            "contract_renewal_date": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"),
            "monthly_value": 0,  # do wyliczenia z products
            "satisfaction_score": 4.0,
            "products_portfolio": [],  # Trzeba będzie ręcznie dodać
            "timeline": [
                {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "event_type": "migrated",
                    "description": "Dane zmigrowane ze starej struktury",
                    "rating": null,
                    "reputation_change": 0
                }
            ]
        }
    
    # Zapisz nową strukturę
    bg_data["clients"] = clients
    
    # Usuń starą (opcjonalnie - można zachować jako backup)
    # del bg_data["customers"]
    bg_data["customers_OLD_BACKUP"] = bg_data.get("customers")
    if "customers" in bg_data:
        del bg_data["customers"]
    
    return clients
```

#### 1.3. Dodanie produktów FreshMarket do bazy

**Plik:** `data/industries/fmcg_products.py` (NOWY)

```python
"""
Portfolio produktów FreshMarket (nasza firma)
Wykorzystywane przy podpisywaniu kontraktów i cross-sell
"""

FRESHMARKET_PRODUCTS = {
    # === PERSONAL CARE / MYCIE ===
    "fresh_soap": {
        "id": "fresh_soap",
        "name": "FreshSoap",
        "full_name": "FreshSoap - Mydło w płynie (250ml)",
        "category": "Personal Care",
        "subcategory": "Mycie",
        "size": "250ml",
        "unit_price_base": 12.50,  # PLN (cena hurtowa dla klienta)
        "margin_for_client": 35,   # % marża dla sklepu
        "retail_price_recommended": 16.90,  # PLN
        "volume_potential": "high",  # high/medium/low
        "description": "Delikatne mydło w płynie z gliceryną. Bestseller kategorii.",
        "target_segment": ["traditional_trade", "convenience"],
        "competitor_products": ["Palmolive", "Duru", "Dove"],
        "typical_monthly_volume": {
            "small_shop": 50,
            "medium_shop": 100,
            "chain": 500
        }
    },
    
    "fresh_shampoo": {
        "id": "fresh_shampoo",
        "name": "FreshShampoo",
        "full_name": "FreshShampoo - Szampon do włosów (400ml)",
        "category": "Personal Care",
        "subcategory": "Włosy",
        "size": "400ml",
        "unit_price_base": 18.00,
        "margin_for_client": 40,
        "retail_price_recommended": 25.20,
        "volume_potential": "high",
        "description": "Szampon regenerujący z proteinami jedwabiu.",
        "target_segment": ["traditional_trade", "convenience"],
        "competitor_products": ["Head & Shoulders", "Pantene", "Garnier"],
        "typical_monthly_volume": {
            "small_shop": 30,
            "medium_shop": 70,
            "chain": 300
        }
    },
    
    "fresh_dish": {
        "id": "fresh_dish",
        "name": "FreshDish",
        "full_name": "FreshDish - Płyn do naczyń (500ml)",
        "category": "Home Care",
        "subcategory": "Kuchnia",
        "size": "500ml",
        "unit_price_base": 8.50,
        "margin_for_client": 30,
        "retail_price_recommended": 11.05,
        "volume_potential": "medium",
        "description": "Skuteczny płyn do mycia naczyń, zapach cytrynowy.",
        "target_segment": ["traditional_trade"],
        "competitor_products": ["Ludwik", "Fairy", "Persil"],
        "typical_monthly_volume": {
            "small_shop": 40,
            "medium_shop": 80,
            "chain": 400
        }
    },
    
    # ... dodaj więcej produktów (np. 10-15 total)
}

def get_product_by_id(product_id):
    return FRESHMARKET_PRODUCTS.get(product_id)

def get_products_by_category(category):
    return [p for p in FRESHMARKET_PRODUCTS.values() if p["category"] == category]

def get_all_products():
    return list(FRESHMARKET_PRODUCTS.values())

def calculate_monthly_value(product_id, volume):
    """Oblicz wartość miesięczną: volume × unit_price"""
    product = get_product_by_id(product_id)
    if not product:
        return 0
    return volume * product["unit_price_base"]
```

---

### **ETAP 2: Rozbudowa UI - Szczegółowa karta klienta** 🎨 (2-3 dni)

#### 2.1. Nowa funkcja: `show_client_card_detailed(client_id, user_data)`

**Gdzie:** `views/business_games_refactored/industries/fmcg.py`

**Design:**

```
┌─────────────────────────────────────────────────────────────┐
│ 🏪 Sklep 'U Kowalskich' - Janina Kowalska                  │
│ 📍 Warszawa, Ursynów, Os. Kabaty                            │
│                                                              │
│ Status: 🟢 AKTYWNY | Reputacja: 65/100 (😊 Happy Client)   │
│ Współpraca: 19 dni | Ostatnia wizyta: 2 dni temu           │
└─────────────────────────────────────────────────────────────┘

┌─ METRYKI ────────────────────────────────────────────────────┐
│ 💰 Wartość miesięczna: 1,165 PLN                            │
│ 📦 Produkty: 2                                              │
│ ⭐ Średnia ocena wizyt: 4.5/5                               │
│ 🎯 Udziały PH: 27.5% (średnia wszystkich produktów)        │
└───────────────────────────────────────────────────────────────┘

┌─ PRODUKTY U KLIENTA ────────────────────────────────────────┐
│                                                              │
│ [Karta produktu 1: FreshSoap]                               │
│ ┌────────────────────────────────────────────────┐          │
│ │ 🧴 FreshSoap (250ml) - Personal Care / Mycie  │          │
│ │                                                │          │
│ │ Volume: 50 szt/miesiąc | Wartość: 625 PLN     │          │
│ │ Market share: 30% 🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜           │          │
│ │ Shelf: 🌟 Prime | Trend: 📈 Rosnący           │          │
│ │ Dodano: 2025-10-05 | Ostatnia promocja: 15.10 │          │
│ └────────────────────────────────────────────────┘          │
│                                                              │
│ [Karta produktu 2: FreshShampoo]                            │
│ ...                                                          │
│                                                              │
│ [➕ Zaproponuj nowy produkt (Cross-sell)]                   │
└───────────────────────────────────────────────────────────────┘

┌─ TIMELINE WSPÓŁPRACY ───────────────────────────────────────┐
│                                                              │
│ 📅 2025-10-20 | 🎯 Wizyta regularna (+5 rep) ⭐⭐⭐⭐⭐    │
│ "Kontrola ekspozycji - wszystko OK"                         │
│                                                              │
│ 📅 2025-10-12 | 🆕 Cross-sell (+15 rep) ⭐⭐⭐⭐⭐         │
│ "Dodano: FreshShampoo (400ml) - +540 PLN/m"                 │
│                                                              │
│ 📅 2025-10-08 | 🎯 Wizyta regularna (+5 rep) ⭐⭐⭐⭐       │
│ "Omówienie rotacji towaru"                                  │
│                                                              │
│ 📅 2025-10-05 | ✅ Kontrakt podpisany (+50 rep) ⭐⭐⭐⭐⭐  │
│ "Pierwsze produkty: FreshSoap, FreshDish - 1,165 PLN/m"    │
│                                                              │
│ 📅 2025-10-01 | 🔍 Pierwsze spotkanie                       │
│ "Cold call - prezentacja FreshMarket"                       │
└───────────────────────────────────────────────────────────────┘

┌─ ZADANIA DLA TEGO KLIENTA ─────────────────────────────────┐
│ 🟢 Wizyta regularna za 12 dni (2025-11-01)                 │
│ 🟡 Renewal kontraktu za 168 dni (2026-04-05)              │
└───────────────────────────────────────────────────────────────┘

┌─ AKCJE ─────────────────────────────────────────────────────┐
│ [📞 Zaplanuj wizytę] [🆕 Cross-sell] [📝 Dodaj notatkę]   │
└───────────────────────────────────────────────────────────────┘
```

#### 2.2. Zmiana w `show_fmcg_customers_tab()`

**PRZED:**
```python
# Lista w expanderach (mało info)
for customer_id in active:
    customer = get_customer_by_id(customer_id)
    with st.expander(f"🏪 {customer['name']}"):
        st.markdown(f"**Potencjał:** {customer['potential_monthly']:,} PLN")
```

**PO:**
```python
# Lista + przyciski "Zobacz kartę"
for client_id in active_clients_ids:
    client_data = clients[client_id]  # z user_data
    base_info = get_customer_by_id(client_id)  # z bazy
    
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        st.markdown(f"### 🏪 {base_info['name']}")
        st.caption(f"{base_info['owner']} | {base_info['location']}")
    
    with col2:
        # Reputacja
        rep = client_data['reputation']
        rep_emoji = "😊" if rep >= 50 else "😐" if rep >= 0 else "😞"
        st.metric("Reputacja", f"{rep}/100 {rep_emoji}")
    
    with col3:
        # Wartość miesięczna
        st.metric("💰 Wartość", f"{client_data['monthly_value']:,} PLN")
    
    with col4:
        if st.button("📋 Karta", key=f"card_{client_id}"):
            st.session_state.fmcg_selected_client = client_id
            st.rerun()
```

---

### **ETAP 3: Integracja z AI Conversations** 🤖 (1 dzień)

#### 3.1. Aktualizacja reputacji po wizycie

**Gdzie:** `render_fmcg_customer_conversation()` - po zakończeniu rozmowy

**Dodać:**
```python
# Po ocenie AI (rating 1-5⭐)
def update_reputation_after_visit(client_id, rating, visit_type, user_data):
    """
    Aktualizuj reputację klienta po wizycie
    """
    clients = user_data["business_games"]["fmcg"]["clients"]
    client = clients[client_id]
    
    # Mapowanie rating → zmiana reputacji
    reputation_map = {
        5: +10,
        4: +5,
        3: +2,
        2: -5,
        1: -15
    }
    
    rep_change = reputation_map.get(rating, 0)
    old_rep = client['reputation']
    new_rep = max(-100, min(100, old_rep + rep_change))  # clamp -100..100
    
    client['reputation'] = new_rep
    
    # Dodaj event do timeline
    from datetime import datetime
    client['timeline'].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "event_type": visit_type,  # "regular_visit", "first_visit", etc.
        "description": f"Wizyta - ocena {rating}⭐",
        "rating": rating,
        "reputation_change": rep_change,
        "details": {"old_rep": old_rep, "new_rep": new_rep}
    })
    
    # Aktualizuj last_visit_date
    if client['status'] == 'ACTIVE':
        client['last_visit_date'] = datetime.now().strftime("%Y-%m-%d")
    
    return rep_change
```

#### 3.2. Generowanie kontekstu dla AI (z karty klienta)

**Gdzie:** `data/industries/fmcg_conversations.py :: build_conversation_prompt()`

**Rozbudować:**
```python
def build_conversation_prompt(customer_id, user_data):
    """
    Generuje prompt dla AI na podstawie:
    - Danych bazowych klienta (fmcg_customers.py)
    - Danych live klienta (user_data["clients"][customer_id])
    """
    from data.industries.fmcg_customers import get_customer_by_id
    from data.industries.fmcg_products import get_product_by_id
    
    base_customer = get_customer_by_id(customer_id)
    clients = user_data["business_games"]["fmcg"].get("clients", {})
    client_live = clients.get(customer_id, {})
    
    status = client_live.get("status", "PROSPECT")
    
    # PROSPECT prompt
    if status == "PROSPECT":
        visits_count = client_live.get("visits_count", 0)
        interest = client_live.get("interest_level", 5)
        
        prompt = f"""
Jesteś {base_customer['owner']}, właścicielem {base_customer['name']}.

STATUS: To {visits_count + 1}. spotkanie z przedstawicielem FreshMarket.

TWOJA POSTAWA:
- Zainteresowanie: {interest}/10 {"(wysoko zainteresowany)" if interest >= 7 else "(średnio zainteresowany)" if interest >= 4 else "(niskie zainteresowanie)"}
- Priorytet: {base_customer['personality']['priorities'][0]}
- Obawy: {base_customer['pain_points'][0]}

CELE:
- Gracz chce Cię przekonać do podpisania kontraktu
- Pytaj o: marżę, warunki dostawy, wsparcie merchandisingowe
- Decyduj na podstawie jakości pitcha (profesjonalizm, odpowiedzi na Twoje pytania)

Po rozmowie oceń gracza 1-5⭐ i wyjaśnij dlaczego.
"""
    
    # ACTIVE prompt
    elif status == "ACTIVE":
        reputation = client_live.get("reputation", 0)
        products = client_live.get("products_portfolio", [])
        
        products_str = ", ".join([get_product_by_id(p['product_id'])['name'] for p in products])
        
        # Określ nastrój na podstawie reputacji
        if reputation >= 70:
            mood = "bardzo zadowolony 😊"
        elif reputation >= 50:
            mood = "zadowolony 🙂"
        elif reputation >= 20:
            mood = "neutralny 😐"
        elif reputation >= 0:
            mood = "lekko niezadowolony 😕"
        else:
            mood = "niezadowolony 😞"
        
        prompt = f"""
Jesteś {base_customer['owner']}, właścicielem {base_customer['name']}.

STATUS: Współpracujesz z FreshMarket od {client_live.get('stats', {}).get('days_cooperation', 0)} dni.

AKTUALNE PRODUKTY:
{products_str}

TWOJA REPUTACJA DO SPRZEDAWCY: {reputation}/100 ({mood})

NASTRÓJ:
{f"Jesteś bardzo zadowolony. Chętnie porozmawiasz o nowych produktach." if reputation >= 70 else ""}
{f"Jesteś OK. Jeśli sprzedawca ma coś ciekawego, wysłuchasz." if 50 <= reputation < 70 else ""}
{f"Masz pewne zastrzeżenia. Sprzedawca musi pokazać wartość." if 0 <= reputation < 50 else ""}
{f"Jesteś rozczarowany. Może rozważasz zmianę dostawcy." if reputation < 0 else ""}

CEL WIZYTY:
- To wizyta regularna (check-in)
- Gracz może chcieć: sprawdzić ekspozycję, zaproponować nowy produkt, rozwiązać problem

Reaguj naturalnie na propozycje. Oceń wizytę 1-5⭐.
"""
    
    return prompt
```

---

## 📊 PODSUMOWANIE - Co dostaniesz po implementacji:

### ✅ Dane:
- Pełny model klienta z 20+ parametrami
- Listing produktów u każdego klienta (volume, market share, shelf)
- Timeline eventów (każda wizyta, cross-sell, zmiana reputacji)
- Backward compatibility (migracja starych danych)

### ✅ UI:
- **Szczegółowa karta klienta** z:
  - Reputacją (liczba + emoji + opis)
  - Listą produktów (volume, wartość, udziały, trend)
  - Timeline współpracy (wszystkie eventy)
  - Zadaniami dla tego klienta
  - Akcjami (wizyta, cross-sell, notatki)
- **Lista klientów** z metrykami (rep, wartość, ostatnia wizyta)
- **Możliwość cross-sell** (dodawanie produktów z UI)

### ✅ Integracja AI:
- Prompt uwzględnia stan klienta (reputacja, produkty, historia)
- Auto-aktualizacja reputacji po wizycie (rating → rep change)
- Timeline automatycznie zapisuje eventy
- Różne nastroje AI w zależności od reputacji

---

## ⏱️ TIMELINE:

| Dzień | Zadania | Output |
|-------|---------|--------|
| **Dzień 1** | Struktura danych + migracja | Nowy model `clients` w user_data |
| **Dzień 2** | Produkty FreshMarket + testy | 10-15 produktów z cenami/marżami |
| **Dzień 3** | UI - karta klienta (hero, metryki) | Widok podstawowych info |
| **Dzień 4** | UI - produkty + timeline | Pełna karta z wszystkimi sekcjami |
| **Dzień 5** | Integracja AI (prompts, reputation) | Działające auto-update po wizytach |
| **Dzień 6** | Testing + polish | Gotowe do pokazania klientowi! |

---

## 🎯 DEFINICJA SUKCESU:

Po implementacji możesz pokazać klientowi:

1. **Karta klienta** z reputacją 65/100 😊
2. **Listing 2-3 produktów** z udziałami (np. FreshSoap: 30% market share)
3. **Timeline** pokazujący historię 5 wizyt z ocenami i zmianami reputacji
4. **Cross-sell w akcji**: Dodanie nowego produktu → zmiana wartości miesięcznej z 1,165 → 1,705 PLN
5. **Zmiana nastroju AI**: Klient z rep=20 (neutralny) vs rep=80 (VIP) - różne odpowiedzi

---

**Czy mam zacząć od ETAPU 1 (struktura danych)?** 🚀
