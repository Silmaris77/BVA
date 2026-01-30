# 🎴 FMCG: Rozbudowa Karty Klienta - Implementacja

**Data rozpoczęcia:** 29.10.2025  
**Status:** 🚧 W TRAKCIE  
**Priorytet:** P1 (Fundament gry)

---

## 📋 PLAN IMPLEMENTACJI

### KROK 1: Rozszerzona Struktura Danych Klienta ✅
**Cel:** Dodać nowe pola do struktury klienta w `user_data`

**Obecna struktura:**
```python
customers_data = {
    "prospects": ["trad_001", "trad_002"],  # Lista ID
    "active_clients": [],
    "lost_clients": []
}
```

**NOWA struktura:**
```python
customers_data = {
    "clients": {
        "trad_001": {
            # === PODSTAWOWE (już są) ===
            "id": "trad_001",
            "status": "prospect",  # prospect | active | lost
            
            # === NOWE: ACTIVE CLIENT DATA ===
            "reputation": 0,  # -100 do +100
            "last_visit_date": None,  # ISO datetime
            "visit_frequency_required": 14,  # dni między wizytami
            "next_visit_due": None,  # ISO datetime (last_visit + frequency)
            
            # === NOWE: PRODUKTY U KLIENTA ===
            "products_portfolio": [
                {
                    "product_id": "pc_shampoo_fresh",
                    "date_listed": "2025-01-15",
                    "monthly_volume": 120,  # sztuk
                    "market_share_category": 35,  # % w kategorii szampony
                    "shelf_placement": "eye_level",  # eye_level | top | bottom
                    "facing_count": 3,  # ile jednostek na półce
                    "stock_days": 14  # ile dni zapasu
                }
            ],
            
            # === NOWE: METRYKI BIZNESOWE ===
            "monthly_value": 0,  # PLN przychód miesięczny
            "contract_start_date": None,  # Kiedy podpisano pierwszy kontrakt
            "contract_renewal_date": None,  # Kiedy renewal (rok później)
            "market_share_vs_competition": 0,  # % półki FreshLife vs ALL
            "satisfaction_score": 3,  # 1-5 gwiazdek
            
            # === NOWE: TIMELINE EVENTS ===
            "events_timeline": [
                {
                    "date": "2025-01-10",
                    "type": "first_visit",  # first_visit | contract_signed | regular_visit | cross_sell | late_visit | complaint | lost
                    "description": "Pierwsza wizyta - prezentacja portfolio",
                    "reputation_change": 0,
                    "related_products": []
                },
                {
                    "date": "2025-01-15",
                    "type": "contract_signed",
                    "description": "Podpisano pierwszy kontrakt - 3 produkty Personal Care",
                    "reputation_change": +20,
                    "related_products": ["pc_shampoo_fresh", "pc_shower_gel", "pc_toothpaste"]
                }
            ],
            
            # === CONVERSATIONS (już działa) ===
            "conversations": [
                {
                    "date": "2025-01-10 14:30",
                    "messages": [...],
                    "evaluation": {
                        "score": 8,
                        "feedback": "..."
                    }
                }
            ]
        }
    }
}
```

---

### KROK 2: Migracja Danych (Backward Compatibility)
**Plik:** `data/industries/fmcg_data_migration.py` (NOWY)

```python
def migrate_fmcg_to_new_structure(user_data):
    """Migracja starej struktury FMCG do nowej z rozszerzonymi klientami"""
    
    bg_data = user_data.get("business_games", {}).get("fmcg", {})
    
    if "customers" not in bg_data:
        return user_data
    
    old_customers = bg_data["customers"]
    
    # Stara struktura: prospects/active_clients/lost_clients (listy ID)
    if "clients" not in old_customers:
        new_clients = {}
        
        # Migruj prospects
        for client_id in old_customers.get("prospects", []):
            new_clients[client_id] = {
                "id": client_id,
                "status": "prospect",
                "reputation": 0,
                "last_visit_date": None,
                "visit_frequency_required": 14,
                "next_visit_due": None,
                "products_portfolio": [],
                "monthly_value": 0,
                "contract_start_date": None,
                "contract_renewal_date": None,
                "market_share_vs_competition": 0,
                "satisfaction_score": 3,
                "events_timeline": [],
                "conversations": old_customers.get("conversations", {}).get(client_id, [])
            }
        
        # Migruj active
        for client_id in old_customers.get("active_clients", []):
            new_clients[client_id] = {
                # ... analogicznie, status="active"
            }
        
        # Zamień strukturę
        bg_data["customers"] = {"clients": new_clients}
    
    return user_data
```

---

### KROK 3: UI - Szczegółowa Karta Klienta
**Plik:** `views/.../fmcg.py`

**Nowa funkcja:** `render_client_detail_card(client_id, client_data, bg_data)`

**Layout:**
```
╔═══════════════════════════════════════════════════════════════╗
║  🏪 Sklep 'U Kowalskich'           [Status: ACTIVE]   [X]     ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  📊 REPUTACJA: ████████░░ 78/100  [+5 last visit]            ║
║  📅 Ostatnia wizyta: 5 dni temu  |  Następna za: 9 dni      ║
║  💰 Wartość miesięczna: 3,500 PLN                            ║
║  ⭐ Zadowolenie: ★★★★☆ (4.2/5)                               ║
║                                                               ║
║  ────────────────────────────────────────────────────────────║
║                                                               ║
║  📦 PRODUKTY U KLIENTA (5)                                   ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ 🧴 FreshMarket Szampon        120 szt/m   35% share    │ ║
║  │ 🧴 FreshMarket Żel pod prysznic  80 szt/m   28% share  │ ║
║  │ 🦷 FreshMarket Pasta do zębów    60 szt/m   40% share  │ ║
║  │ [+ Dodaj nowy produkt]                                  │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                               ║
║  ────────────────────────────────────────────────────────────║
║                                                               ║
║  📜 TIMELINE WSPÓŁPRACY                                      ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ ●─ 15.01.2025 - Podpisano kontrakt (+20 rep)           │ ║
║  │ │                                                        │ ║
║  │ ●─ 22.01.2025 - Regularna wizyta (+5 rep)              │ ║
║  │ │                                                        │ ║
║  │ ●─ 05.02.2025 - Cross-sell: 2 nowe produkty (+15 rep)  │ ║
║  │ │                                                        │ ║
║  │ ●─ 19.02.2025 - Spóźniona wizyta (-10 rep)             │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                               ║
║  [📞 Umów wizytę]  [📊 Raport]  [🎁 Promocja]               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

### KROK 4: System Reputacji - Mechaniki
**Plik:** `utils/fmcg_reputation.py` (NOWY)

```python
def update_client_reputation(client_data, event_type, params=None):
    """
    Aktualizuje reputację klienta na podstawie wydarzenia
    
    Args:
        client_data: Dict z danymi klienta
        event_type: Typ wydarzenia (str)
        params: Dodatkowe parametry (dict)
    
    Returns:
        reputation_change: int (-100 do +100)
    """
    
    REPUTATION_CHANGES = {
        "regular_visit_on_time": +5,
        "visit_excellent_5stars": +10,
        "task_completed": +3,
        "promotion_delivered": +5,
        "cross_sell_success": +15,
        "exceeded_sales_plan": +10,
        
        "visit_late_1_7days": -3,
        "visit_late_8_14days": -7,
        "visit_late_15plus": -15,
        "no_visit_30days": -20,
        "visit_poor_1_2stars": -10,
        "product_unavailable": -8,
        "complaint_unresolved": -12,
        "competitor_won_listing": -20
    }
    
    change = REPUTATION_CHANGES.get(event_type, 0)
    
    # Zastosuj zmianę
    old_rep = client_data.get("reputation", 0)
    new_rep = max(-100, min(100, old_rep + change))
    client_data["reputation"] = new_rep
    
    # Dodaj event do timeline
    event_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": event_type,
        "description": f"Zmiana reputacji: {change:+d}",
        "reputation_change": change,
        "related_products": params.get("products", []) if params else []
    }
    
    client_data.setdefault("events_timeline", []).append(event_entry)
    
    # Sprawdź czy klient został LOST
    if new_rep <= -50 and client_data["status"] == "active":
        client_data["status"] = "lost"
        client_data["lost_date"] = datetime.now().isoformat()
        client_data["lost_reason"] = "reputation_too_low"
    
    return change
```

---

### KROK 5: Cross-sell (Dodawanie Produktów)
**UI Flow:**
1. Kliknij [+ Dodaj produkt] w karcie klienta
2. Modal z listą produktów FreshLife
3. Wybierz produkt → AI negotiation conversation
4. Jeśli sukces → dodaj do `products_portfolio`
5. Update: `monthly_value`, `market_share`, `reputation` (+15)

---

## 🎯 KOLEJNOŚĆ IMPLEMENTACJI (dzisiaj):

1. ✅ **Struktura danych** - nowe pola w client dict
2. ✅ **Migracja** - backward compatibility
3. ✅ **UI - Gauge reputacji** - wizualizacja -100 do +100
4. ✅ **UI - Timeline** - vertical lista eventów
5. ✅ **UI - Produkty** - tabela z portfolio
6. ⏳ **Mechaniki reputacji** - funkcje update
7. ⏳ **Cross-sell flow** - dodawanie produktów

---

## 📝 NOTATKI IMPLEMENTACYJNE:

- **Reputacja**: -100 (lost) → 0 (neutral) → +100 (champion)
- **Kolory gauge**: 
  - -100 to -50: czerwony (💀 LOST)
  - -49 to 0: pomarańczowy (⚠️ AT RISK)
  - 1 to 50: żółty (😐 NEUTRAL)
  - 51 to 80: zielony (😊 GOOD)
  - 81 to 100: niebieski (🏆 CHAMPION)
  
- **Visit frequency**: 
  - Sklepy małe: 14 dni
  - Średnie: 10 dni
  - Duże: 7 dni
  
- **Timeline**: Max 50 ostatnich eventów (starsze archiwizować)
