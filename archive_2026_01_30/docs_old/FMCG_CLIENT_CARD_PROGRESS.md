# 📋 FMCG Client Card - Realizacja Krok po Kroku

## ✅ UKOŃCZONE (Session 1)

### 1. Helper Functions Module
**Plik:** `utils/fmcg_client_helpers.py`

✅ Utworzono moduł z 10 funkcjami pomocniczymi:
- `create_new_client_entry()` - Tworzy pełną strukturę klienta z nowymi polami
- `migrate_fmcg_customers_to_new_structure()` - Migracjado nowej struktury z backward compatibility
- `get_client_by_id()` - Pobiera klienta z dict
- `get_clients_by_status()` - Filtruje klientów po statusie
- `calculate_next_visit_due()` - Oblicza datę kolejnej wizyty
- `is_visit_overdue()` - Sprawdza opóźnienie wizyty
- `add_product_to_portfolio()` - Dodaje produkt do portfolio (cross-sell)
- `get_reputation_status()` - Zwraca dane dla gauge'a reputacji
- `update_reputation()` - Aktualizuje reputację (wrapper)
- `add_timeline_event()` - Dodaje event do timeline

### 2. Reputation System Module
**Plik:** `utils/fmcg_reputation.py`

✅ Utworzono system reputacji z:
- `REPUTATION_CHANGES` - Dictionary z wartościami zmian dla wszystkich event types
- `update_client_reputation()` - Główna funkcja aktualizacji reputacji
- `get_default_event_description()` - Generuje opisy eventów
- `record_visit()` - Rejestruje wizytę i aktualizuje reputację (z AI quality score)
- `sign_contract()` - Podpisuje kontrakt (PROSPECT → ACTIVE), dodaje +20 rep
- `check_overdue_visits()` - Sprawdza wszystkich klientów pod kątem opóźnionych wizyt

**Event types covered:**
- ✅ Pozytywne: wizyty na czas (+ 5/10), zadania (+3), promocje (+5), cross-sell (+15), przekroczenie planu (+10)
- ❌ Negatywne: wizyta spóźniona (-3/-7/-15), brak wizyty 30 dni (-20), słaba wizyta (-5/-10), brak produktu (-8)

**Auto-detection:**
- Sprawdza `next_visit_due` vs current date
- Automatycznie klasyfikuje wizytę jako spóźnioną (1-7, 8-14, 15+ dni)
- Integruje AI quality score (1-5 stars)
- Auto-trigger LOST status gdy rep <= -50

### 3. Products Management Module
**Plik:** `utils/fmcg_products.py`

✅ Utworzono zarządzanie produktami:
- `FRESHLIFE_PRODUCTS` - Dict z 8 produktami (jogurty, mleko, masło, sery, śmietanka, kefir)
- `get_product_info()` - Zwraca dane produktu
- `get_products_by_category()` - Filtruje po kategorii
- `calculate_monthly_value()` - Oblicza miesięczną wartość sprzedaży
- `suggest_cross_sell_products()` - Sugeruje produkty do cross-sellu (5 strategii)
- `update_product_volume()` - Aktualizuje volume produktu
- `remove_product_from_portfolio()` - Usuwa produkt (-10 rep)
- `get_portfolio_summary()` - Generuje podsumowanie portfolio

**Cross-sell strategies:**
1. Jogurt naturalny → jogurt owocowy
2. Mleko → masło organiczne (wyższa marża)
3. Sery → śmietanka
4. Basic → Premium upsell (kefir probiotyczny)
5. Małe portfolio → Bestsellery (jogurt, mleko)

### 4. Integration Layer
**Plik:** `views/business_games_refactored/industries/fmcg.py`

✅ Dodano:
- Import wszystkich nowych modułów (helpers, reputation, products)
- Funkcja `ensure_fmcg_data_structure()` - wykrywa starą strukturę i wywołuje migrację
- Auto-save po migracji do `users_data.json`

---

## 🔄 W TRAKCIE (Session 1 - COMPLETED ✅)

### 5. Integracja Migracji z Playable UI ✅

**Status:** DONE

**Zmiany:**
1. ✅ Dodano import wszystkich modułów w `fmcg_playable.py`
2. ✅ Dodano auto-migration check przed load_fmcg_game_state_sql()
3. ✅ Naprawiono sygnaturę `migrate_fmcg_customers_to_new_structure()` (bg_data zamiast user_data)
4. ✅ Wszystkie testy backend przeszły pomyślnie

### 6. Client Detail Card UI ✅

**Status:** DONE

**Zmiany:**
1. ✅ Utworzono `views/business_games_refactored/components/client_detail_card.py`
2. ✅ Zaimplementowano:
   - Header z nazwą, statusem, basic info (gradient card)
   - Reputation Gauge z color-coded progress bar
   - Visit Tracker (last visit, next visit, overdue detection)
   - Products Portfolio z summary metrics i tabelą
   - Cross-sell suggestions (expandable)
   - Events Timeline (ostatnie 10, vertical scrollable)
   - Back button
3. ✅ Zintegrowano z `fmcg_playable.py`:
   - Tab "Klienci" pokazuje listę z przyciskami "Szczegóły"
   - Kliknięcie → render_client_detail_card()
   - Grupowanie po statusie (ACTIVE/PROSPECT/LOST)
   - Session state dla show_client_detail

**Test Results:**
```
✅ TEST 1: Create new client entry - PASSED
✅ TEST 2: Reputation status - PASSED (6 reputation levels)
✅ TEST 3: Update reputation - PASSED (+5 for visit)
✅ TEST 4: Add product to portfolio - PASSED (1500 PLN monthly_value)
✅ TEST 5: Cross-sell suggestions - PASSED (3 suggestions)
✅ TEST 6: Migration - PASSED (3 clients, conversations preserved)
```

---

## 📋 TODO (Session 3)

### 6. UI Component - Client Detail Card

**Nowy komponent:** `render_client_detail_card(client_data)`

**Elementy:**
1. **Header** - Nazwa klienta, status badge, basic info
2. **Reputation Gauge** - Używa `get_reputation_status()`:
   ```python
   rep_status = get_reputation_status(client_data)
   # Display: progress bar z kolorami, emoji, label
   ```
3. **Products Portfolio Table**:
   - Kolumny: Product, Volume/month, Market Share, Shelf Placement
   - Użyj `get_portfolio_summary()` i `FRESHLIFE_PRODUCTS`
   - Button: `[+ Add Product]` dla cross-sell
4. **Timeline (vertically scrollable)**:
   - Loop przez `events_timeline` (ostatnie 10)
   - Format: Date | Icon | Description | Rep change
   - Sortowanie: najnowsze na górze
5. **Visit Tracker**:
   - `last_visit_date` vs `next_visit_due`
   - `is_visit_overdue()` → alert jeśli True
   - Przycisk: `[📞 Plan Visit]`

**Gdzie dodać:**
- W `fmcg_playable.py` po kliknięciu klienta na mapie
- Lub w `fmcg.py` w zakładce "Klienci"

---

### 7. Cross-Sell Mechanics UI

**Gdzie:** Modal po kliknięciu `[+ Add Product]` w Client Detail Card

**Zawartość:**
1. Wywołaj `suggest_cross_sell_products(client_data, max_suggestions=3)`
2. Wyświetl karty produktów:
   - Product name, category, margin %
   - Reason (np. "Klient już kupuje jogurty naturalne")
   - Expected volume
   - Button: `[Dodaj do portfolio]`
3. Po kliknięciu:
   - Wywołaj `add_product_to_portfolio(client_data, product_id, initial_volume)`
   - Auto +15 reputation
   - Zaktualizuj `monthly_value`
   - Zapisz do DB

---

### 8. Visit Recording Integration

**Gdzie:** Po zakończeniu AI conversation w `fmcg_playable.py`

**Flow:**
1. User kończy rozmowę z klientem (AI conversation)
2. System dostaje AI evaluation score (1-5 stars)
3. Wywołaj:
   ```python
   change = record_visit(
       client_data,
       visit_quality=ai_score,  # 1-5
       notes="Rozmowa o nowych produktach"
   )
   ```
4. Pokaż toast:
   - Jeśli change > 0: `✅ Wizyta udana! Reputacja +{change}`
   - Jeśli change < 0: `⚠️ Wizyta spóźniona - reputacja {change}`
5. Update `last_visit_date` i `next_visit_due`

---

### 9. Dashboard Enhancements

**Gdzie:** `fmcg_playable.py` dashboard section

**Dodać metryki:**
1. **Overdue Visits Counter:**
   ```python
   overdue_list = check_overdue_visits(clients)
   if overdue_list:
       st.warning(f"⚠️ {len(overdue_list)} klientów czeka na wizytę!")
   ```

2. **Reputation Trend:**
   - Średnia reputacja wszystkich ACTIVE klientów
   - Chart: reputation over time (z timeline)

3. **Cross-sell Opportunities:**
   - Policz klientów z < 2 produktami
   - Alert: "🎯 5 klientów gotowych na cross-sell!"

---

### 10. Contract Signing Flow

**Gdzie:** Modal w `fmcg_playable.py` dla PROSPECT klientów

**Trigger:** Po successful visit z PROSPECT (AI score >= 4)

**UI:**
1. Pokaż modal: "🎉 Klient gotowy podpisać kontrakt!"
2. Multi-select: "Wybierz produkty do kontraktu"
   - Lista z `FRESHLIFE_PRODUCTS`
   - Min 1, recommended 2-3
3. Button: `[📝 Podpisz kontrakt]`
4. Wywołaj:
   ```python
   sign_contract(client_data, products=["yogurt_natural", "milk_fresh"])
   # Auto: status → ACTIVE, +20 rep, contract_start_date
   ```
5. Show celebration: "✅ Pierwszy kontrakt podpisany! +20 reputation"

---

## 🎯 Priority Order

**HIGH PRIORITY (Session 2):**
1. ✅ Integracja migracji w `fmcg_playable.py` (5 min)
2. ✅ Client Detail Card UI (30 min)
3. ✅ Visit Recording Integration (15 min)

**MEDIUM PRIORITY (Session 3):**
4. Cross-Sell Mechanics UI (20 min)
5. Contract Signing Flow (25 min)
6. Dashboard Enhancements (20 min)

**LOW PRIORITY (Session 4):**
7. Timeline visualization improvements
8. Reputation trend chart
9. Advanced filters (by reputation, overdue status)

---

## 🔧 Technical Notes

### Data Structure Migration

**Stara struktura:**
```json
{
  "customers": {
    "prospects": ["trad_001", "trad_002"],
    "active_clients": ["trad_003"],
    "lost_clients": []
  },
  "conversations": {
    "trad_001": [...]
  }
}
```

**Nowa struktura:**
```json
{
  "customers": {
    "clients": {
      "trad_001": {
        "id": "trad_001",
        "status": "prospect",
        "reputation": 0,
        "products_portfolio": [],
        "events_timeline": [],
        "last_visit_date": null,
        "next_visit_due": "2025-01-25",
        "visit_frequency_required": 14,
        "monthly_value": 0.0,
        "market_share": 0.0,
        "satisfaction_score": 50,
        "conversations": [...]  // Preserved from old structure
      }
    }
  }
}
```

### Backward Compatibility

`migrate_fmcg_customers_to_new_structure()` zapewnia:
- ✅ Zachowanie conversations
- ✅ Mapowanie status (prospect/active/lost)
- ✅ Domyślne wartości dla nowych pól
- ✅ Brak duplikatów

### Save Strategy

- Helper functions modyfikują `client_data` **in-place**
- Po każdej zmianie wywołaj `update_fmcg_game_state_sql()` lub bezpośredni zapis do JSON
- Dla playable UI: auto-save po każdej wizycie/akcji

---

## 📚 Files Modified

| File | Status | Purpose |
|------|--------|---------|
| `utils/fmcg_client_helpers.py` | ✅ Created | Client management & migration |
| `utils/fmcg_reputation.py` | ✅ Created | Reputation system & visit recording |
| `utils/fmcg_products.py` | ✅ Created | Product management & cross-sell |
| `views/.../fmcg.py` | ✅ Updated | Added imports & migration check |
| `views/.../fmcg_playable.py` | 🔄 TODO | Integrate migration & UI components |
| `FMCG_CLIENT_CARD_IMPLEMENTATION.md` | ✅ Created | Original implementation plan |

---

## 🎮 Testing Checklist

### After Session 2:
- [ ] Load existing FMCG game → auto-migration works
- [ ] Create new FMCG game → new structure from start
- [ ] Client Detail Card shows all fields
- [ ] Reputation gauge displays correct colors
- [ ] Timeline shows last events
- [ ] Visit recording updates reputation correctly

### After Session 3:
- [ ] Cross-sell suggestions appear
- [ ] Add product updates portfolio & monthly_value
- [ ] Contract signing changes PROSPECT → ACTIVE
- [ ] Overdue visits show in dashboard
- [ ] Auto-detect late visits (reputation penalty)

---

## 💡 Future Enhancements (Post-MVP)

1. **Reputation Decay**: -1 rep per week for ACTIVE clients without visit
2. **Product Performance Tracking**: Track sales trend per product
3. **Competitor Events**: Random events where competitor wins listing
4. **Client Personality Impact**: Reputation changes vary by client personality
5. **Multi-product Cross-sell**: Bundle offers (jogurt + mleko = -5% price)
6. **Seasonal Campaigns**: Special promotions impact reputation & volume
7. **Client Referrals**: High reputation clients recommend new prospects

---

**Last Updated:** 2025-01-20
**Author:** GitHub Copilot + User pksia
**Status:** Session 1 Complete ✅ | Session 2 Ready 🚀
