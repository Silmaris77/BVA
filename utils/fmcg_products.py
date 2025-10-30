"""
📦 FMCG Products Management
Zarządzanie portfolio produktów u klientów
"""

from typing import Dict, Optional, List
from datetime import datetime


# Portfolio produktów FreshLife Poland
FRESHLIFE_PRODUCTS = {
    "yogurt_natural": {
        "id": "yogurt_natural",
        "name": "Jogurt Naturalny 400g",
        "category": "dairy",
        "brand": "FreshLife",
        "price_wholesale": 3.50,
        "price_retail": 4.99,
        "margin_percent": 42.6,
        "shelf_life_days": 14
    },
    "yogurt_fruit": {
        "id": "yogurt_fruit",
        "name": "Jogurt Owocowy 150g x4",
        "category": "dairy",
        "brand": "FreshLife",
        "price_wholesale": 5.00,
        "price_retail": 6.99,
        "margin_percent": 39.8,
        "shelf_life_days": 14
    },
    "milk_fresh": {
        "id": "milk_fresh",
        "name": "Mleko Świeże 1L",
        "category": "dairy",
        "brand": "FreshLife",
        "price_wholesale": 2.80,
        "price_retail": 3.99,
        "margin_percent": 42.5,
        "shelf_life_days": 7
    },
    "butter_organic": {
        "id": "butter_organic",
        "name": "Masło Organiczne 200g",
        "category": "dairy",
        "brand": "FreshLife Organic",
        "price_wholesale": 6.50,
        "price_retail": 8.99,
        "margin_percent": 38.3,
        "shelf_life_days": 30
    },
    "cheese_mozzarella": {
        "id": "cheese_mozzarella",
        "name": "Mozzarella 125g",
        "category": "dairy",
        "brand": "FreshLife Premium",
        "price_wholesale": 4.20,
        "price_retail": 5.99,
        "margin_percent": 42.6,
        "shelf_life_days": 21
    },
    "cheese_cheddar": {
        "id": "cheese_cheddar",
        "name": "Cheddar Plastry 150g",
        "category": "dairy",
        "brand": "FreshLife",
        "price_wholesale": 5.50,
        "price_retail": 7.49,
        "margin_percent": 36.2,
        "shelf_life_days": 45
    },
    "cream_cooking": {
        "id": "cream_cooking",
        "name": "Śmietanka 18% 500ml",
        "category": "dairy",
        "brand": "FreshLife",
        "price_wholesale": 3.80,
        "price_retail": 5.29,
        "margin_percent": 39.2,
        "shelf_life_days": 14
    },
    "kefir_probiotic": {
        "id": "kefir_probiotic",
        "name": "Kefir Probiotyczny 500ml",
        "category": "dairy",
        "brand": "FreshLife Bio",
        "price_wholesale": 4.00,
        "price_retail": 5.79,
        "margin_percent": 44.7,
        "shelf_life_days": 10
    }
}


def get_product_info(product_id: str) -> Optional[Dict]:
    """Zwraca informacje o produkcie"""
    return FRESHLIFE_PRODUCTS.get(product_id)


def get_products_by_category(category: str) -> List[Dict]:
    """Zwraca listę produktów z danej kategorii"""
    return [
        prod for prod in FRESHLIFE_PRODUCTS.values()
        if prod["category"] == category
    ]


def get_all_categories() -> List[str]:
    """Zwraca listę wszystkich kategorii"""
    categories = set(prod["category"] for prod in FRESHLIFE_PRODUCTS.values())
    return sorted(categories)


def calculate_monthly_value(products_portfolio: List[Dict]) -> float:
    """
    Oblicza miesięczną wartość sprzedaży na podstawie portfolio
    
    Args:
        products_portfolio: Lista produktów z polami volume, market_share
    
    Returns:
        Miesięczna wartość w PLN
    """
    
    total = 0.0
    
    for entry in products_portfolio:
        product_id = entry.get("product_id")
        volume = entry.get("volume", 0)  # Liczba sztuk miesięcznie
        
        product_info = get_product_info(product_id)
        if not product_info:
            continue
        
        price = product_info["price_wholesale"]
        total += volume * price
    
    return round(total, 2)


def suggest_cross_sell_products(client_data: Dict, max_suggestions: int = 3) -> List[Dict]:
    """
    Sugeruje produkty do cross-sellu na podstawie aktualnego portfolio klienta
    
    Args:
        client_data: Dane klienta
        max_suggestions: Maksymalna liczba sugestii
    
    Returns:
        Lista dict z produktami i powodem sugestii
    """
    
    current_products = set(
        p["product_id"] for p in client_data.get("products_portfolio", [])
    )
    
    suggestions = []
    
    # Strategia 1: Jeśli klient ma jogurt naturalny, sugeruj jogurt owocowy
    if "yogurt_natural" in current_products and "yogurt_fruit" not in current_products:
        suggestions.append({
            "product": FRESHLIFE_PRODUCTS["yogurt_fruit"],
            "reason": "Klient już kupuje jogurty naturalne - uzupełnienie o wariant owocowy",
            "priority": "high",
            "expected_volume": 80
        })
    
    # Strategia 2: Jeśli klient ma mleko, sugeruj masło
    if "milk_fresh" in current_products and "butter_organic" not in current_products:
        suggestions.append({
            "product": FRESHLIFE_PRODUCTS["butter_organic"],
            "reason": "Rozszerzenie kategorii mlecznej o masło organiczne - wyższa marża",
            "priority": "medium",
            "expected_volume": 40
        })
    
    # Strategia 3: Jeśli klient ma sery, sugeruj śmietankę
    has_cheese = any(p in current_products for p in ["cheese_mozzarella", "cheese_cheddar"])
    if has_cheese and "cream_cooking" not in current_products:
        suggestions.append({
            "product": FRESHLIFE_PRODUCTS["cream_cooking"],
            "reason": "Uzupełnienie oferty produktów mleczarskich",
            "priority": "medium",
            "expected_volume": 60
        })
    
    # Strategia 4: Premium upsell - jeśli klient ma podstawowe produkty, sugeruj premium
    basic_products = ["milk_fresh", "yogurt_natural"]
    if any(p in current_products for p in basic_products):
        if "kefir_probiotic" not in current_products:
            suggestions.append({
                "product": FRESHLIFE_PRODUCTS["kefir_probiotic"],
                "reason": "Premium bio produkt - wyższa marża dla klienta",
                "priority": "low",
                "expected_volume": 30
            })
    
    # Strategia 5: Jeśli portfolio jest małe, sugeruj bestsellery
    if len(current_products) < 2:
        if "yogurt_natural" not in current_products:
            suggestions.append({
                "product": FRESHLIFE_PRODUCTS["yogurt_natural"],
                "reason": "Bestseller kategorii - wysoka rotacja",
                "priority": "high",
                "expected_volume": 100
            })
        
        if "milk_fresh" not in current_products:
            suggestions.append({
                "product": FRESHLIFE_PRODUCTS["milk_fresh"],
                "reason": "Podstawowy produkt nabiałowy - stały popyt",
                "priority": "high",
                "expected_volume": 120
            })
    
    # Sortuj po priorytecie
    priority_order = {"high": 0, "medium": 1, "low": 2}
    suggestions.sort(key=lambda x: priority_order[x["priority"]])
    
    return suggestions[:max_suggestions]


def update_product_volume(
    client_data: Dict,
    product_id: str,
    new_volume: int,
    reason: str = ""
) -> bool:
    """
    Aktualizuje volume produktu w portfolio klienta
    
    Args:
        client_data: Dane klienta (modyfikowany in-place)
        product_id: ID produktu
        new_volume: Nowy volume (sztuki/miesiąc)
        reason: Powód zmiany (opcjonalny)
    
    Returns:
        True jeśli zaktualizowano, False jeśli produkt nie znaleziony
    """
    
    portfolio = client_data.get("products_portfolio", [])
    
    for entry in portfolio:
        if entry["product_id"] == product_id:
            old_volume = entry["volume"]
            entry["volume"] = new_volume
            entry["last_updated"] = datetime.now().isoformat()
            
            # Przelicz monthly_value
            client_data["monthly_value"] = calculate_monthly_value(portfolio)
            
            # Dodaj event do timeline
            product_info = get_product_info(product_id)
            product_name = product_info["name"] if product_info else product_id
            
            change_pct = ((new_volume - old_volume) / old_volume * 100) if old_volume > 0 else 0
            
            desc = f"📊 Zmiana volume: {product_name} ({old_volume} → {new_volume}, {change_pct:+.1f}%)"
            if reason:
                desc += f" - {reason}"
            
            client_data.setdefault("events_timeline", []).append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "volume_change",
                "description": desc,
                "reputation_change": 0,
                "reputation_after": client_data.get("reputation", 0),
                "related_products": [product_id]
            })
            
            return True
    
    return False


def remove_product_from_portfolio(
    client_data: Dict,
    product_id: str,
    reason: str = ""
) -> bool:
    """
    Usuwa produkt z portfolio klienta
    
    Args:
        client_data: Dane klienta (modyfikowany in-place)
        product_id: ID produktu do usunięcia
        reason: Powód usunięcia
    
    Returns:
        True jeśli usunięto, False jeśli produkt nie znaleziony
    """
    
    portfolio = client_data.get("products_portfolio", [])
    
    for i, entry in enumerate(portfolio):
        if entry["product_id"] == product_id:
            # Usuń
            del portfolio[i]
            
            # Przelicz monthly_value
            client_data["monthly_value"] = calculate_monthly_value(portfolio)
            
            # Dodaj event
            product_info = get_product_info(product_id)
            product_name = product_info["name"] if product_info else product_id
            
            desc = f"❌ Wycofano produkt: {product_name}"
            if reason:
                desc += f" - {reason}"
            
            client_data.setdefault("events_timeline", []).append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "product_removed",
                "description": desc,
                "reputation_change": -10,  # Utrata produktu = spadek reputacji
                "reputation_after": client_data.get("reputation", 0),
                "related_products": [product_id]
            })
            
            # Update reputacji
            from utils.fmcg_reputation import update_client_reputation
            update_client_reputation(
                client_data,
                "product_unavailable",
                description=desc,
                related_products=[product_id]
            )
            
            return True
    
    return False


def get_portfolio_summary(client_data: Dict) -> Dict:
    """
    Generuje podsumowanie portfolio klienta
    
    Returns:
        Dict z kluczami: total_products, total_value, categories, top_product
    """
    
    portfolio = client_data.get("products_portfolio", [])
    
    if not portfolio:
        return {
            "total_products": 0,
            "total_value": 0.0,
            "categories": [],
            "top_product": None
        }
    
    # Kategorie
    categories = set()
    max_volume = 0
    top_product = None
    
    for entry in portfolio:
        product_info = get_product_info(entry["product_id"])
        if product_info:
            categories.add(product_info["category"])
            
            if entry["volume"] > max_volume:
                max_volume = entry["volume"]
                top_product = product_info["name"]
    
    return {
        "total_products": len(portfolio),
        "total_value": client_data.get("monthly_value", 0.0),
        "categories": sorted(categories),
        "top_product": top_product
    }
