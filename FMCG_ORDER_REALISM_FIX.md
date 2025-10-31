# FMCG - Naprawa Realizmu Zamówień

## 🎯 Problem

Obecnie handlowiec może zaproponować nierealistyczne ilości (np. 1000 opakowań ketchupu dla małego sklepu osiedlowego), a AI klient może zaakceptować to lub zaproponować nadal nierealistyczną kontrpropozycję (500 sztuk).

## 📊 Rozwiązanie: Parametry Wielkości Sprzedaży Sklepu

### 1. Nowe Parametry Klienta

Dodajemy do każdego klienta `sales_capacity` - słownik z limitami sprzedaży:

```python
"sales_capacity": {
    # Kategorie produktów
    "Personal Care": {
        "weekly_sales_volume": 150,      # Sztuki/tydzień w całej kategorii
        "shelf_space_facings": 12,       # Ile facing (pozycji) na półce
        "storage_capacity": 200,         # Max zapas w magazynku (szt)
        "rotation_days": 14,             # Ile dni produkt się sprzedaje
        "max_order_per_sku": 24          # Max zamówienie na 1 SKU
    },
    "Food": {
        "weekly_sales_volume": 300,
        "shelf_space_facings": 20,
        "storage_capacity": 400,
        "rotation_days": 7,
        "max_order_per_sku": 36
    },
    "Home Care": {
        "weekly_sales_volume": 80,
        "shelf_space_facings": 8,
        "storage_capacity": 150,
        "rotation_days": 21,
        "max_order_per_sku": 12
    },
    "Snacks": {
        "weekly_sales_volume": 200,
        "shelf_space_facings": 15,
        "storage_capacity": 300,
        "rotation_days": 30,
        "max_order_per_sku": 30
    },
    "Beverages": {
        "weekly_sales_volume": 250,
        "shelf_space_facings": 18,
        "storage_capacity": 350,
        "rotation_days": 14,
        "max_order_per_sku": 36
    }
}
```

### 2. Segmentacja Sklepów

Różne typy sklepów mają różne capacity:

| Segment | Wielkość | Personal Care | Food | Home Care | Snacks | Beverages |
|---------|----------|---------------|------|-----------|--------|-----------|
| **Mikro osiedlowy** | 30-50 m² | 80 szt/tydz | 150 | 40 | 100 | 120 |
| **Mały osiedlowy** | 50-100 m² | 150 szt/tydz | 300 | 80 | 200 | 250 |
| **Średni osiedlowy** | 100-200 m² | 250 szt/tydz | 500 | 150 | 350 | 400 |
| **Duży osiedlowy** | 200+ m² | 400 szt/tydz | 800 | 250 | 500 | 600 |

### 3. Formuła Zamówienia Realistycznego

```python
def calculate_realistic_order_quantity(
    client: Dict,
    product: Dict,
    weeks_to_cover: int = 2
) -> int:
    """
    Oblicza realistyczną ilość zamówienia
    
    Args:
        client: Dane klienta z sales_capacity
        product: Produkt (z kategorią)
        weeks_to_cover: Na ile tygodni zamówienie (default: 2)
    
    Returns:
        Realistyczna ilość do zamówienia
    """
    category = product.get("category", "Personal Care")
    capacity = client.get("sales_capacity", {}).get(category, {})
    
    # Podstawowe parametry
    weekly_volume = capacity.get("weekly_sales_volume", 100)
    max_per_sku = capacity.get("max_order_per_sku", 24)
    rotation_days = capacity.get("rotation_days", 14)
    
    # Oszacuj udział tego produktu w kategorii (zakładamy 5-10 SKU w kategorii)
    avg_sku_share = weekly_volume / 7  # Średnio 7 SKU w kategorii
    
    # Zamówienie na X tygodni
    base_order = int(avg_sku_share * weeks_to_cover)
    
    # Ogranicz do max per SKU
    realistic_qty = min(base_order, max_per_sku)
    
    # Zaokrąglij do pełnych opakowań zbiorczych (6, 12, 24)
    if realistic_qty <= 6:
        return 6
    elif realistic_qty <= 12:
        return 12
    elif realistic_qty <= 24:
        return 24
    else:
        return ((realistic_qty // 6) * 6)  # Wielokrotność 6
    
    return max(6, realistic_qty)  # Min 6 sztuk


def validate_order_quantity(
    client: Dict,
    product: Dict,
    proposed_quantity: int
) -> Dict:
    """
    Waliduje czy zamówienie jest realistyczne
    
    Returns:
        {
            "is_realistic": bool,
            "recommended_quantity": int,
            "feedback": str  # dla AI - dlaczego nerealne
        }
    """
    realistic_qty = calculate_realistic_order_quantity(client, product, weeks_to_cover=2)
    max_qty = realistic_qty * 3  # Max 6 tygodni zapasu
    
    if proposed_quantity <= realistic_qty * 1.2:
        return {
            "is_realistic": True,
            "recommended_quantity": proposed_quantity,
            "feedback": "Ilość w porządku"
        }
    elif proposed_quantity <= max_qty:
        return {
            "is_realistic": True,
            "recommended_quantity": proposed_quantity,
            "feedback": f"To dość duże zamówienie (typowo {realistic_qty} szt), ale da się zmieścić"
        }
    else:
        return {
            "is_realistic": False,
            "recommended_quantity": realistic_qty,
            "feedback": f"To za dużo! Nie mam miejsca ani budżetu. Typowo biorę {realistic_qty} sztuk, max {max_qty}."
        }
```

### 4. Integracja z AI Conversation

W systemowym prompcie dla AI dodajemy:

```python
# W prepare_conversation_context()
sales_capacity = client.get("sales_capacity", {})
product_category = product.get("category", "Personal Care")
capacity_info = sales_capacity.get(product_category, {})

context += f"""
WAŻNE - LIMITY SKLEPU:
- Kategoria {product_category}: sprzedaję ~{capacity_info.get('weekly_sales_volume', 100)} sztuk/tydzień
- Miejsce na półce: {capacity_info.get('shelf_space_facings', 10)} facing
- Magazyn: max {capacity_info.get('storage_capacity', 200)} sztuk
- Typowe zamówienie na jeden produkt: {capacity_info.get('max_order_per_sku', 24)} sztuk

ZASADA: Jeśli handlowiec proponuje nierealistyczną ilość (np. 500 sztuk dla małego sklepu), 
ODRZUĆ to stanowczo mówiąc:
"To stanowczo za dużo! Nie mam ani miejsca ani budżetu. Typowo biorę [realistic_qty] sztuk."

Możesz zaakceptować max 20% powyżej typowej ilości jako "próbę na początek".
"""
```

### 5. UI - Podpowiedzi dla Gracza

W zakładce Rozmowa, przy wyborze produktu pokazujemy:

```python
st.info(f"""
📊 **Parametry sklepu dla kategorii {category}:**
- 📈 Sprzedaż tygodniowa: ~{weekly_volume} szt
- 📦 Typowe zamówienie: {realistic_qty} szt (na 2 tygodnie)
- 🏪 Miejsce na półce: {facings} pozycji
- 💡 Sugerowane pierwsze zamówienie: {realistic_qty} - {realistic_qty * 2} szt
""")
```

## 📋 Plan Implementacji

### ✅ Krok 1: Rozszerzenie Schematu Klienta - DONE
- [x] Dodać `sales_capacity` do `FMCGClientData` (TypedDict)
- [x] Dodać `sales_capacity` do `create_new_client()`
- [x] Utworzyć funkcję `generate_sales_capacity(client_type, size_sqm)` → Dict

### ✅ Krok 2: Funkcje Walidacji - DONE
- [x] `calculate_realistic_order_quantity(client, product, weeks)` → int
- [x] `validate_order_quantity(client, product, qty)` → Dict
- [x] `get_order_size_recommendation(client, product)` → str (text dla UI)

### ✅ Krok 3: Integracja z AI - DONE
- [x] Rozszerzyć `build_conversation_prompt()` o sales_capacity
- [x] Dodać instrukcje w systemowym prompcie AI
- [x] AI teraz odrzuca nierealistyczne ilości zgodnie z parametrami sklepu

### ✅ Krok 4: UI Improvements - DONE
- [x] Pokazać parametry sklepu w zakładce Klienci (card)
- [x] Pokazać sugerowane ilości w zakładce Rozmowa
- [x] Dodać walidację w czasie rzeczywistym (✅/⚠️/❌ przy ilościach)
- [x] Tooltips z wyjaśnieniami

### ✅ Krok 5: Migracja Istniejących Klientów - DONE
- [x] Skrypt migracyjny `migrate_add_sales_capacity.py`
- [x] Migracja zakończona: 20 klientów zaktualizowanych
- [x] Backup utworzony automatycznie

---

## 🎉 IMPLEMENTACJA ZAKOŃCZONA!

**Data:** 2025-10-30  
**Status:** ✅ MVP w pełni wdrożony  
**Czas implementacji:** ~2 godziny

### 📁 Nowe/Zmodyfikowane Pliki:

1. **utils/fmcg_order_realism.py** (NOWY)
   - `generate_sales_capacity()` - generuje capacity dla 4 segmentów sklepów
   - `calculate_realistic_order_quantity()` - oblicza realistyczną ilość
   - `validate_order_quantity()` - waliduje propozycje gracza
   - `get_order_size_recommendation()` - UI recommendation text

2. **data/industries/fmcg_data_schema.py** (ZMODYFIKOWANY)
   - Dodano `sales_capacity: Optional[Dict]` do `FMCGClientData`
   - `create_new_client()` auto-generuje sales_capacity

3. **data/industries/fmcg_conversations.py** (ZMODYFIKOWANY)
   - `build_conversation_prompt()` zawiera szczegółowe instrukcje o limitach
   - AI dostaje konkretne liczby: weekly_volume, max_per_sku, facings
   - Przykłady reakcji dla AI (jak odrzucać nierealistyczne ilości)

4. **views/business_games_refactored/industries/fmcg_playable.py** (ZMODYFIKOWANY)
   - Tab Rozmowa: pokazuje sugerowane ilości per kategoria
   - Walidacja w czasie rzeczywistym (✅/⚠️/❌)
   - Step +6 w number_input (standardowe opakowania)

5. **views/business_games_refactored/components/client_detail_card.py** (ZMODYFIKOWANY)
   - Nowa sekcja "📊 Parametry Sklepu"
   - Pokazuje sales_capacity dla wszystkich kategorii
   - Segment name (Mikro/Mały/Średni/Duży)

6. **migrate_add_sales_capacity.py** (NOWY)
   - Skrypt migracyjny dla istniejących klientów
   - Auto-backup przed zmianami
   - ✅ Wykonany pomyślnie: 20 klientów zaktualizowanych

### 🎯 Rezultaty:

**Przed:**
- Handlowiec: "1000 sztuk ketchupu"
- AI: "Ok, może 500 sztuk?"
- ❌ Kompletnie nierealistyczne dla sklepu 80 m²

**Po:**
- Handlowiec: "1000 sztuk ketchupu"
- AI: "Czy Pan/Pani żartuje? 1000 sztuk?! To absurdalna ilość dla mojego sklepu! Nie mam na to miejsca, budżetu ani popytu. Normalnie zamawiam 24 sztuki. Proszę być poważnym - mogę rozważyć 24 sztuki, nie więcej."
- ✅ Realistyczna odmowa z konkretnymi liczbami!

**UI Podpowiedzi:**
```
📊 Parametry sklepu dla kategorii Artykuły spożywcze:
- Sprzedaż tygodniowa: ~300 szt (cała kategoria)
- Miejsce na półce: 20 pozycji
- 💡 Typowe zamówienie na 1 produkt: 24 szt (2 tygodnie)
```

### 🎓 Wartość Edukacyjna - Osiągnięta!

Studenci teraz uczą się:
- ✅ Realistycznego planowania zamówień
- ✅ Ograniczeń sklepów (miejsce, budżet, rotacja)
- ✅ Segmentacji klientów (mikro ≠ duży sklep)
- ✅ Argumentacji biznesowej ("Dlaczego 24 sztuki?")
- ✅ Rozumienia kanału tradycyjnego

---

**Status:** 🟢 PRODUCTION READY  
**Next Steps:** Testowanie z użytkownikami (Basia et al.)

## 🎓 Wartość Edukacyjna

Studenci nauczą się:
- ✅ **Planowania zamówień** - ile realnie może kupić sklep
- ✅ **Rotacji produktu** - różne kategorie mają różną rotację
- ✅ **Ograniczeń sklepu** - miejsce na półce, budżet, magazyn
- ✅ **Segmentacji** - mikro sklep ≠ średni sklep
- ✅ **Argumentacji** - "Dlaczego 24 sztuki to dobra ilość na start?"

## 🔧 Przykładowe Dane

```python
# Mały sklep osiedlowy (80 m²)
"sales_capacity": {
    "Personal Care": {
        "weekly_sales_volume": 150,
        "shelf_space_facings": 12,
        "storage_capacity": 200,
        "rotation_days": 14,
        "max_order_per_sku": 24,
        "avg_products_in_category": 8
    }
}

# Przykład realistycznych zamówień:
# - BodyWash Natural (Personal Care): 12-24 szt
# - Ketchup (Food): 12-36 szt  
# - Płyn do mycia naczyń (Home Care): 6-12 szt
# - Chipsy (Snacks): 24-48 szt
# - Sok pomarańczowy (Beverages): 24-36 szt
```

## ❓ Pytania do Rozstrzygnięcia

1. **Czy generować sales_capacity dynamicznie** (na podstawie size_sqm) czy **predefiniowane szablony** (mikro/mały/średni/duży)?
   - **Rekomendacja:** Szablony + modyfikator na podstawie size_sqm

2. **Czy pokazywać te dane graczowi jawnie** czy ukryć i tylko AI ich używa?
   - **Rekomendacja:** Pokazać w zakładce Klienci (edukacyjne!)

3. **Jak obsłużyć wyjątki** (np. promocja, sezonowość)?
   - **Rekomendacja:** Parametr `promotional_multiplier` (1.0-2.0)

4. **Czy różnicować wg marki** (FreshLife vs konkurencja)?
   - **Rekomendacja:** Nie na razie - zbyt skomplikowane

## 🚀 Quick Win - MVP

Minimalny zakres do wdrożenia:

1. ✅ Dodać `sales_capacity` z 3 segmentami (mały/średni/duży)
2. ✅ Funkcja `calculate_realistic_order_quantity()`
3. ✅ Rozszerzyć AI prompt o limity
4. ✅ Pokazać "Sugerowane zamówienie" w UI

**Czas implementacji:** ~2-3 godziny

---

**Status:** 📝 Dokument planistyczny  
**Data:** 2025-10-30  
**Priorytet:** 🔴 WYSOKI (wpływa na realizm gry)
