"""
🛒 FMCG Order Realism Module

Funkcje zapewniające realistyczne wielkości zamówień
na podstawie parametrów sklepu (wielkość, kategoria produktów)
"""

from typing import Dict, Tuple


# =============================================================================
# SALES CAPACITY TEMPLATES (bazowane na wielkości sklepu)
# =============================================================================

def generate_sales_capacity(size_sqm: int, client_type: str = "Sklep osiedlowy") -> Dict:
    """
    Generuje sales_capacity dla sklepu na podstawie metrażu
    
    Args:
        size_sqm: Powierzchnia sklepu w m²
        client_type: Typ klienta (dla przyszłych modyfikacji)
    
    Returns:
        Dict z parametrami sprzedaży dla każdej kategorii
    """
    # Określ segment na podstawie metrażu
    if size_sqm < 50:
        segment = "mikro"
    elif size_sqm < 100:
        segment = "maly"
    elif size_sqm < 200:
        segment = "sredni"
    else:
        segment = "duzy"
    
    # Szablony capacity dla segmentów
    templates = {
        "mikro": {
            "Personal Care": {
                "weekly_sales_volume": 80,
                "shelf_space_facings": 8,
                "storage_capacity": 120,
                "rotation_days": 14,
                "max_order_per_sku": 12,
                "avg_products_in_category": 6
            },
            "Food": {
                "weekly_sales_volume": 150,
                "shelf_space_facings": 12,
                "storage_capacity": 250,
                "rotation_days": 7,
                "max_order_per_sku": 24,
                "avg_products_in_category": 10
            },
            "Home Care": {
                "weekly_sales_volume": 40,
                "shelf_space_facings": 6,
                "storage_capacity": 80,
                "rotation_days": 21,
                "max_order_per_sku": 6,
                "avg_products_in_category": 5
            },
            "Snacks": {
                "weekly_sales_volume": 100,
                "shelf_space_facings": 10,
                "storage_capacity": 180,
                "rotation_days": 30,
                "max_order_per_sku": 24,
                "avg_products_in_category": 8
            },
            "Beverages": {
                "weekly_sales_volume": 120,
                "shelf_space_facings": 12,
                "storage_capacity": 200,
                "rotation_days": 14,
                "max_order_per_sku": 24,
                "avg_products_in_category": 7
            }
        },
        "maly": {
            "Personal Care": {
                "weekly_sales_volume": 150,
                "shelf_space_facings": 12,
                "storage_capacity": 200,
                "rotation_days": 14,
                "max_order_per_sku": 24,
                "avg_products_in_category": 8
            },
            "Food": {
                "weekly_sales_volume": 300,
                "shelf_space_facings": 20,
                "storage_capacity": 400,
                "rotation_days": 7,
                "max_order_per_sku": 36,
                "avg_products_in_category": 12
            },
            "Home Care": {
                "weekly_sales_volume": 80,
                "shelf_space_facings": 8,
                "storage_capacity": 150,
                "rotation_days": 21,
                "max_order_per_sku": 12,
                "avg_products_in_category": 6
            },
            "Snacks": {
                "weekly_sales_volume": 200,
                "shelf_space_facings": 15,
                "storage_capacity": 300,
                "rotation_days": 30,
                "max_order_per_sku": 30,
                "avg_products_in_category": 10
            },
            "Beverages": {
                "weekly_sales_volume": 250,
                "shelf_space_facings": 18,
                "storage_capacity": 350,
                "rotation_days": 14,
                "max_order_per_sku": 36,
                "avg_products_in_category": 10
            }
        },
        "sredni": {
            "Personal Care": {
                "weekly_sales_volume": 250,
                "shelf_space_facings": 18,
                "storage_capacity": 350,
                "rotation_days": 14,
                "max_order_per_sku": 36,
                "avg_products_in_category": 12
            },
            "Food": {
                "weekly_sales_volume": 500,
                "shelf_space_facings": 30,
                "storage_capacity": 700,
                "rotation_days": 7,
                "max_order_per_sku": 48,
                "avg_products_in_category": 15
            },
            "Home Care": {
                "weekly_sales_volume": 150,
                "shelf_space_facings": 12,
                "storage_capacity": 250,
                "rotation_days": 21,
                "max_order_per_sku": 24,
                "avg_products_in_category": 8
            },
            "Snacks": {
                "weekly_sales_volume": 350,
                "shelf_space_facings": 22,
                "storage_capacity": 500,
                "rotation_days": 30,
                "max_order_per_sku": 48,
                "avg_products_in_category": 12
            },
            "Beverages": {
                "weekly_sales_volume": 400,
                "shelf_space_facings": 25,
                "storage_capacity": 600,
                "rotation_days": 14,
                "max_order_per_sku": 48,
                "avg_products_in_category": 12
            }
        },
        "duzy": {
            "Personal Care": {
                "weekly_sales_volume": 400,
                "shelf_space_facings": 25,
                "storage_capacity": 600,
                "rotation_days": 14,
                "max_order_per_sku": 48,
                "avg_products_in_category": 15
            },
            "Food": {
                "weekly_sales_volume": 800,
                "shelf_space_facings": 40,
                "storage_capacity": 1200,
                "rotation_days": 7,
                "max_order_per_sku": 72,
                "avg_products_in_category": 20
            },
            "Home Care": {
                "weekly_sales_volume": 250,
                "shelf_space_facings": 18,
                "storage_capacity": 400,
                "rotation_days": 21,
                "max_order_per_sku": 36,
                "avg_products_in_category": 10
            },
            "Snacks": {
                "weekly_sales_volume": 500,
                "shelf_space_facings": 30,
                "storage_capacity": 800,
                "rotation_days": 30,
                "max_order_per_sku": 72,
                "avg_products_in_category": 15
            },
            "Beverages": {
                "weekly_sales_volume": 600,
                "shelf_space_facings": 35,
                "storage_capacity": 1000,
                "rotation_days": 14,
                "max_order_per_sku": 72,
                "avg_products_in_category": 15
            }
        }
    }
    
    return templates.get(segment, templates["maly"])


# =============================================================================
# ORDER QUANTITY CALCULATIONS
# =============================================================================

def calculate_realistic_order_quantity(
    client: Dict,
    product: Dict,
    weeks_to_cover: int = 2,
    is_first_order: bool = False
) -> int:
    """
    Oblicza realistyczną ilość zamówienia na podstawie parametrów sklepu
    
    Args:
        client: Dane klienta (musi zawierać sales_capacity)
        product: Dane produktu (musi zawierać category)
        weeks_to_cover: Na ile tygodni zamówienie (default: 2)
        is_first_order: Czy to pierwsze zamówienie (mniejsze ilości)
    
    Returns:
        Realistyczna ilość do zamówienia (int)
    """
    # Pobierz sales_capacity lub wygeneruj jeśli brak
    sales_capacity = client.get("sales_capacity")
    if not sales_capacity:
        size_sqm = client.get("size_sqm", 80)
        sales_capacity = generate_sales_capacity(size_sqm)
    
    # Pobierz parametry dla kategorii produktu
    category = product.get("category", "Personal Care")
    capacity = sales_capacity.get(category, sales_capacity.get("Personal Care", {}))
    
    # Podstawowe parametry
    weekly_volume = capacity.get("weekly_sales_volume", 100)
    max_per_sku = capacity.get("max_order_per_sku", 24)
    avg_products = capacity.get("avg_products_in_category", 8)
    
    # Oszacuj udział tego produktu w kategorii
    # Założenie: nowy produkt dostanie ~10-15% ruchu kategorii
    product_share = 0.12 if is_first_order else 0.15
    weekly_sales_for_product = weekly_volume * product_share
    
    # Zamówienie na X tygodni
    base_order = int(weekly_sales_for_product * weeks_to_cover)
    
    # Dla pierwszego zamówienia - mniej (test)
    if is_first_order:
        base_order = int(base_order * 0.7)  # 30% mniej na próbę
    
    # Ogranicz do max per SKU
    realistic_qty = min(base_order, max_per_sku)
    
    # Zaokrąglij do pełnych opakowań zbiorczych (6, 12, 24)
    if realistic_qty <= 6:
        return 6
    elif realistic_qty <= 12:
        return 12
    elif realistic_qty <= 24:
        return 24
    elif realistic_qty <= 36:
        return 36
    elif realistic_qty <= 48:
        return 48
    else:
        # Zaokrąglij do wielokrotności 6
        return ((realistic_qty // 6) * 6)


def validate_order_quantity(
    client: Dict,
    product: Dict,
    proposed_quantity: int,
    is_first_order: bool = False
) -> Dict:
    """
    Waliduje czy proponowana ilość zamówienia jest realistyczna
    
    Args:
        client: Dane klienta
        product: Dane produktu
        proposed_quantity: Proponowana ilość przez handlowca
        is_first_order: Czy to pierwsze zamówienie
    
    Returns:
        Dict z wynikiem walidacji:
        {
            "is_realistic": bool,
            "realism_level": str,  # "perfect", "acceptable", "too_high", "too_low", "unrealistic"
            "recommended_quantity": int,
            "feedback_for_ai": str,  # Tekst do użycia przez AI w odpowiedzi
            "feedback_for_player": str  # Tekst do pokazania graczowi
        }
    """
    # Oblicz realistyczną ilość
    realistic_qty = calculate_realistic_order_quantity(
        client, product, weeks_to_cover=2, is_first_order=is_first_order
    )
    
    # Pobierz max ilość (6 tygodni zapasu)
    max_realistic = calculate_realistic_order_quantity(
        client, product, weeks_to_cover=6, is_first_order=False
    )
    
    # Minimum sensowne (1 tydzień)
    min_realistic = calculate_realistic_order_quantity(
        client, product, weeks_to_cover=1, is_first_order=is_first_order
    )
    
    # Analiza propozycji
    ratio = proposed_quantity / realistic_qty if realistic_qty > 0 else 999
    
    # Za mało
    if proposed_quantity < min_realistic * 0.8:
        return {
            "is_realistic": False,
            "realism_level": "too_low",
            "recommended_quantity": realistic_qty,
            "feedback_for_ai": f"To za mało! Nie opłaca mi się zamawiać tak małych ilości. Minimalna sensowna ilość to {min_realistic} sztuk, a normalnie biorę {realistic_qty}.",
            "feedback_for_player": f"⚠️ Za mała ilość. Sklep oczekuje min. {min_realistic} szt (typowo {realistic_qty} szt)"
        }
    
    # Idealne (90-110% realistycznej)
    elif 0.9 <= ratio <= 1.1:
        return {
            "is_realistic": True,
            "realism_level": "perfect",
            "recommended_quantity": proposed_quantity,
            "feedback_for_ai": f"Dobra! {proposed_quantity} sztuk to rozsądna ilość. Zgadzam się.",
            "feedback_for_player": f"✅ Doskonała propozycja! Idealna ilość dla tego sklepu."
        }
    
    # Akceptowalne (110-150% realistycznej)
    elif 1.1 < ratio <= 1.5:
        return {
            "is_realistic": True,
            "realism_level": "acceptable",
            "recommended_quantity": proposed_quantity,
            "feedback_for_ai": f"{proposed_quantity} sztuk to trochę więcej niż zwykle ({realistic_qty}), ale mogę spróbować. Jak się dobrze sprzeda, będę zamawiał więcej.",
            "feedback_for_player": f"✅ Akceptowalne (10-50% powyżej typowej ilości {realistic_qty} szt)"
        }
    
    # Za dużo ale jeszcze możliwe (150-250% realistycznej)
    elif 1.5 < ratio <= 2.5:
        counter_offer = min(int(proposed_quantity * 0.6), max_realistic)
        return {
            "is_realistic": False,
            "realism_level": "too_high",
            "recommended_quantity": counter_offer,
            "feedback_for_ai": f"To stanowczo za dużo! Nie mam ani miejsca ani budżetu na {proposed_quantity} sztuk. Typowo zamawiam {realistic_qty}, maksymalnie mógłbym wziąć {counter_offer}. Co powiesz na {counter_offer} sztuk na początek?",
            "feedback_for_player": f"⚠️ Za duża ilość! Sklep zaproponuje kontrę: {counter_offer} szt (typowo {realistic_qty})"
        }
    
    # Kompletnie nierealistyczne (>250%)
    else:
        return {
            "is_realistic": False,
            "realism_level": "unrealistic",
            "recommended_quantity": realistic_qty,
            "feedback_for_ai": f"Czy Pan/Pani żartuje? {proposed_quantity} sztuk?! To absurdalna ilość dla mojego sklepu! Nie mam na to miejsca, budżetu ani popytu. Normalnie zamawiam {realistic_qty} sztuk. Proszę być poważnym - mogę rozważyć {realistic_qty} sztuk, nie więcej.",
            "feedback_for_player": f"❌ Nierealistyczna ilość! Sklep odrzuci. Typowo {realistic_qty} szt (max {max_realistic})"
        }


def get_order_size_recommendation(
    client: Dict,
    product: Dict,
    is_first_order: bool = False
) -> str:
    """
    Zwraca tekst z rekomendacją wielkości zamówienia dla UI
    
    Args:
        client: Dane klienta
        product: Dane produktu
        is_first_order: Czy to pierwsze zamówienie
    
    Returns:
        Sformatowany string HTML/Markdown z rekomendacją
    """
    # Oblicz różne scenariusze
    optimal = calculate_realistic_order_quantity(client, product, weeks_to_cover=2, is_first_order=is_first_order)
    min_qty = calculate_realistic_order_quantity(client, product, weeks_to_cover=1, is_first_order=is_first_order)
    max_qty = calculate_realistic_order_quantity(client, product, weeks_to_cover=6, is_first_order=False)
    
    # Pobierz parametry kategorii
    sales_capacity = client.get("sales_capacity")
    if not sales_capacity:
        sales_capacity = generate_sales_capacity(client.get("size_sqm", 80))
    
    category = product.get("category", "Personal Care")
    capacity = sales_capacity.get(category, {})
    
    weekly_volume = capacity.get("weekly_sales_volume", 100)
    facings = capacity.get("shelf_space_facings", 10)
    
    # Segment sklepu
    size = client.get("size_sqm", 80)
    if size < 50:
        segment_name = "Mikro sklep"
    elif size < 100:
        segment_name = "Mały sklep"
    elif size < 200:
        segment_name = "Średni sklep"
    else:
        segment_name = "Duży sklep"
    
    recommendation = f"""
📊 **Parametry sklepu ({segment_name}, {size} m²)**

**Kategoria {category}:**
- 📈 Sprzedaż tygodniowa całej kategorii: ~{weekly_volume} szt
- 🏪 Miejsce na półce: {facings} pozycji (facings)

**💡 Rekomendowane zamówienie dla tego produktu:**
- ✅ **Optymalne:** {optimal} szt (2 tygodnie)
- 📉 Minimum: {min_qty} szt (1 tydzień)
- 📈 Maximum: {max_qty} szt (6 tygodni - duży zapas)

{"🎯 **Pierwsze zamówienie:** Sklep będzie ostrożny - zaproponuj {optimal} szt jako test." if is_first_order else ""}
    """
    
    return recommendation.strip()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_category_display_name(category_key: str) -> str:
    """Zwraca polską nazwę kategorii"""
    names = {
        "Personal Care": "Higiena osobista",
        "Food": "Artykuły spożywcze",
        "Home Care": "Chemia domowa",
        "Snacks": "Przekąski",
        "Beverages": "Napoje"
    }
    return names.get(category_key, category_key)


def get_segment_name(size_sqm: int) -> str:
    """Zwraca nazwę segmentu na podstawie metrażu"""
    if size_sqm < 50:
        return "Mikro sklep osiedlowy"
    elif size_sqm < 100:
        return "Mały sklep osiedlowy"
    elif size_sqm < 200:
        return "Średni sklep osiedlowy"
    else:
        return "Duży sklep osiedlowy"


def calculate_market_share(client: dict, category: str) -> dict:
    """
    Oblicza market share gracza w kategorii u klienta
    
    Args:
        client: dict - dane klienta (FMCGClientData)
        category: str - nazwa kategorii (np. "Personal Care")
    
    Returns:
        dict - market share data:
        {
            "player_share": 35,  # % market share gracza
            "competitor_share": 65,
            "player_volume_weekly": 53,  # sztuk tygodniowo (produkty gracza)
            "total_volume_weekly": 150,  # całkowita sprzedaż w kategorii
            "trend": "growing",  # "growing", "declining", "stable"
            "trend_percentage": 15,  # +15% vs miesiąc temu
            "last_updated": "2025-10-30T10:00:00",
            "history": [...]  # historia ostatnich miesięcy
        }
    """
    from datetime import datetime
    from data.industries.fmcg_products import FRESHLIFE_PRODUCTS
    
    # Pobierz discovered info
    discovered_info = client.get('discovered_info', {})
    current_market_share = discovered_info.get('market_share_by_category', {}).get(category, {})
    
    # Pobierz sales_capacity dla kategorii (może być odkryta lub nie)
    sales_capacity_discovered = discovered_info.get('sales_capacity_discovered', {})
    is_capacity_discovered = category in sales_capacity_discovered
    
    # Total volume (jeśli odkryte → użyj discovered, jeśli nie → użyj base sales_capacity)
    if is_capacity_discovered:
        total_volume_weekly = sales_capacity_discovered[category].get('weekly_sales_volume', 0)
    else:
        # Nie odkryte → nie znamy total_volume
        total_volume_weekly = 0
    
    # Oblicz player_volume_weekly (ile produktów gracza klient sprzedaje)
    products_portfolio = client.get('products_portfolio', [])
    player_products_in_category = []
    
    for product_id in products_portfolio:
        product = FRESHLIFE_PRODUCTS.get(product_id)
        if product and product.get('category') == category:
            player_products_in_category.append(product)
    
    # Szacuj player_volume (zakładamy że każdy produkt gracza = 1 facing = ~weekly_sales / facings)
    if is_capacity_discovered and total_volume_weekly > 0:
        facings = sales_capacity_discovered[category].get('shelf_space_facings', 10)
        avg_per_facing = total_volume_weekly / facings if facings > 0 else 10
        player_volume_weekly = int(len(player_products_in_category) * avg_per_facing)
    else:
        # Brak danych capacity → estymacja na podstawie liczby produktów
        player_volume_weekly = len(player_products_in_category) * 10  # Rough estimate
    
    # Oblicz %
    if total_volume_weekly > 0:
        player_share = int((player_volume_weekly / total_volume_weekly) * 100)
        player_share = min(player_share, 100)  # Cap at 100%
    else:
        player_share = 0
    
    competitor_share = 100 - player_share
    
    # Oblicz trend (porównaj z poprzednim miesiącem)
    history = current_market_share.get('history', [])
    trend = "stable"
    trend_percentage = 0
    
    if len(history) >= 2:
        prev_month_share = history[-2].get('player_share', 0)
        if player_share > prev_month_share + 5:
            trend = "growing"
            trend_percentage = player_share - prev_month_share
        elif player_share < prev_month_share - 5:
            trend = "declining"
            trend_percentage = player_share - prev_month_share
        else:
            trend = "stable"
            trend_percentage = player_share - prev_month_share
    
    # Aktualizuj historię (dodaj bieżący miesiąc)
    current_month = datetime.now().strftime("%Y-%m")
    
    # Sprawdź czy już jest entry dla bieżącego miesiąca
    if history and history[-1].get('month') == current_month:
        # Aktualizuj ostatni wpis
        history[-1] = {
            "month": current_month,
            "player_share": player_share,
            "player_volume": player_volume_weekly
        }
    else:
        # Dodaj nowy miesiąc
        history.append({
            "month": current_month,
            "player_share": player_share,
            "player_volume": player_volume_weekly
        })
    
    # Ogranicz historię do ostatnich 6 miesięcy
    history = history[-6:]
    
    return {
        "player_share": player_share,
        "competitor_share": competitor_share,
        "player_volume_weekly": player_volume_weekly,
        "total_volume_weekly": total_volume_weekly,
        "trend": trend,
        "trend_percentage": trend_percentage,
        "last_updated": datetime.now().isoformat(),
        "history": history
    }
