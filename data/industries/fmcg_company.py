"""
FreshLife Poland - Fikcyjna firma FMCG (wzorowana na Unilever)
Definicja firmy, portfolio produktów, positioning
"""

COMPANY_INFO = {
    "name": "FreshLife Poland",
    "full_name": "FreshLife Consumer Products Poland Sp. z o.o.",
    "founded": 2005,
    "parent_company": "FreshLife International (UK)",
    "employees_poland": 450,
    "hq_location": "Warszawa, Wilanów",
    
    "mission": "Dostarczamy produkty, które codziennie poprawiają jakość życia Polaków",
    
    "description": """
FreshLife Poland to polski oddział międzynarodowego koncernu FMCG z ponad 50-letnią historią. 
Jesteśmy liderem w kategorii Personal Care i dynamicznie rozwijamy się w segmentach Food i Home Care.

Nasza filozofia opiera się na trzech filarach:
• Innowacyjność - każdego roku wprowadzamy 10+ nowych produktów
• Jakość - certyfikaty ISO, nagrody konsumenckie
• Zrównoważony rozwój - 80% opakowań z recyklingu do 2025

W Polsce jesteśmy w TOP 3 w kategorii Personal Care z udziałem rynkowym 18%.
Współpracujemy z ponad 15,000 punktów sprzedaży detalicznej i hurtowej.
""",
    
    "market_position": {
        "personal_care": "TOP 3 (18% udziału rynku)",
        "food": "TOP 10 (5% udziału rynku)",
        "home_care": "TOP 5 (12% udziału rynku)"
    },
    
    "values": [
        "Innowacyjność",
        "Jakość bez kompromisów",
        "Odpowiedzialność społeczna",
        "Partnerstwo z klientami"
    ]
}

# Portfolio produktów podzielone na 3 kategorie
PRODUCT_PORTFOLIO = {
    "personal_care": {
        "category_name": "Personal Care",
        "description": "Produkty do pielęgnacji ciała i włosów",
        "market_share": 18,
        "products": [
            {
                "id": "pc_001",
                "name": "CleanFresh",
                "subcategory": "Żele pod prysznic",
                "variants": ["Classic", "Sport", "Sensitive", "Fresh Mint"],
                "price_range": "8-12 PLN / 500ml",
                "margin_percent": 35,
                "volume_potential": "wysoki",
                "usp": "Formuła z naturalnym aloesem, 0% parabenów",
                "target_group": "Kobiety i mężczyźni 18-45",
                "shelf_life": "36 miesięcy",
                "packaging": "Butelka PET 100% z recyklingu",
                "awards": ["Konsumencki Lider Jakości 2024"]
            },
            {
                "id": "pc_002",
                "name": "SilkHair",
                "subcategory": "Szampony i odżywki",
                "variants": ["Volume", "Repair", "Color Protection", "Anti-Dandruff"],
                "price_range": "15-22 PLN / 400ml",
                "margin_percent": 40,
                "volume_potential": "średni",
                "usp": "Technologia Keratin Complex, efekt salonu w domu",
                "target_group": "Kobiety 25-55",
                "shelf_life": "36 miesięcy",
                "packaging": "Butelka HDPE",
                "awards": ["Beauty Awards 2024"]
            },
            {
                "id": "pc_003",
                "name": "DeoActive",
                "subcategory": "Dezodoranty",
                "variants": ["Men Sport", "Men Classic", "Women Fresh", "Women Sensitive"],
                "price_range": "9-14 PLN / 150ml spray",
                "margin_percent": 42,
                "volume_potential": "wysoki",
                "usp": "48h ochrony, 0% aluminium",
                "target_group": "Kobiety i mężczyźni 16-50",
                "shelf_life": "30 miesięcy",
                "packaging": "Aerozol aluminiowy",
                "awards": []
            }
        ]
    },
    
    "food": {
        "category_name": "Food & Beverages",
        "description": "Produkty spożywcze i napoje",
        "market_share": 5,
        "products": [
            {
                "id": "food_001",
                "name": "MorningJoy",
                "subcategory": "Płatki śniadaniowe",
                "variants": ["Chocolate", "Honey", "Fruits", "Fitness"],
                "price_range": "12-16 PLN / 500g",
                "margin_percent": 28,
                "volume_potential": "średni",
                "usp": "Pełne ziarno, bez cukru dodanego w wersji Fitness",
                "target_group": "Rodziny z dziećmi, osoby aktywne",
                "shelf_life": "12 miesięcy",
                "packaging": "Karton z okienkiem",
                "awards": []
            },
            {
                "id": "food_002",
                "name": "QuickSoup",
                "subcategory": "Zupy instant",
                "variants": ["Rosół", "Pomidorowa", "Grochówka", "Krem z pieczarek"],
                "price_range": "3-5 PLN / porcja",
                "margin_percent": 32,
                "volume_potential": "wysoki",
                "usp": "Gotowa w 3 minuty, bez konserwantów",
                "target_group": "Młodzi profesjonaliści, studenci",
                "shelf_life": "18 miesięcy",
                "packaging": "Saszetka foliowa",
                "awards": []
            },
            {
                "id": "food_003",
                "name": "PureOil",
                "subcategory": "Oleje spożywcze",
                "variants": ["Rzepakowy", "Słonecznikowy", "Lniany", "Mix omega 3-6-9"],
                "price_range": "8-18 PLN / 500ml",
                "margin_percent": 25,
                "volume_potential": "średni",
                "usp": "Tłoczenie na zimno, bez rafinacji",
                "target_group": "Kobiety 30-60, świadome zdrowie",
                "shelf_life": "12 miesięcy",
                "packaging": "Butelka szklana ciemna",
                "awards": ["Zdrowy Produkt Roku 2023"]
            }
        ]
    },
    
    "home_care": {
        "category_name": "Home Care",
        "description": "Produkty do czyszczenia i pielęgnacji domu",
        "market_share": 12,
        "products": [
            {
                "id": "hc_001",
                "name": "SparkleClean",
                "subcategory": "Płyny do mycia podłóg",
                "variants": ["Universal", "Wood", "Tiles", "Antibacterial"],
                "price_range": "10-15 PLN / 1L",
                "margin_percent": 38,
                "volume_potential": "wysoki",
                "usp": "Błysk bez smug, biodegradowalna formuła",
                "target_group": "Gospodarstwa domowe",
                "shelf_life": "24 miesiące",
                "packaging": "Butelka PET",
                "awards": []
            },
            {
                "id": "hc_002",
                "name": "DishPro",
                "subcategory": "Płyny do naczyń",
                "variants": ["Lemon", "Apple", "Sensitive", "Power Grease"],
                "price_range": "6-9 PLN / 500ml",
                "margin_percent": 40,
                "volume_potential": "bardzo wysoki",
                "usp": "Usuwa tłuszcz już w 30°C, łagodny dla rąk",
                "target_group": "Gospodarstwa domowe",
                "shelf_life": "24 miesiące",
                "packaging": "Butelka PET z pompką",
                "awards": []
            },
            {
                "id": "hc_003",
                "name": "FreshAir",
                "subcategory": "Odświeżacze powietrza",
                "variants": ["Lavender", "Ocean", "Forest", "Citrus"],
                "price_range": "12-18 PLN / 300ml spray",
                "margin_percent": 45,
                "volume_potential": "średni",
                "usp": "Neutralizuje zapachy zamiast maskować",
                "target_group": "Gospodarstwa domowe, biura",
                "shelf_life": "30 miesięcy",
                "packaging": "Aerozol aluminiowy",
                "awards": []
            }
        ]
    }
}

# Konkurencja
COMPETITORS = {
    "direct": [
        {
            "name": "PureBeauty Corp",
            "strength": "Personal Care, wysoka rozpoznawalność marki",
            "weakness": "Wysokie ceny, ograniczona dystrybucja w small trade"
        },
        {
            "name": "HomeEssentials",
            "strength": "Home Care, agresywna polityka cenowa",
            "weakness": "Niższa jakość postrzegana, mało innowacji"
        },
        {
            "name": "NatureFirst",
            "strength": "Produkty eko, silna w segmencie premium",
            "weakness": "Wąskie portfolio, niszowa"
        }
    ],
    "indirect": [
        "Private labels sieci handlowych",
        "Małe lokalne marki"
    ]
}

def get_product_by_id(product_id):
    """Zwraca produkt po ID"""
    for category in PRODUCT_PORTFOLIO.values():
        for product in category["products"]:
            if product["id"] == product_id:
                return product
    return None

def get_products_by_category(category_key):
    """Zwraca wszystkie produkty z danej kategorii"""
    if category_key in PRODUCT_PORTFOLIO:
        return PRODUCT_PORTFOLIO[category_key]["products"]
    return []

def get_all_products():
    """Zwraca listę wszystkich produktów"""
    all_products = []
    for category in PRODUCT_PORTFOLIO.values():
        all_products.extend(category["products"])
    return all_products

def get_company_pitch():
    """Zwraca krótki pitch firmy dla klienta"""
    return f"""
{COMPANY_INFO['name']} to lider rynku FMCG z portfolio 12 uznanych marek.
Współpracujemy z ponad 15,000 punktami sprzedaży w Polsce.

Oferujemy:
✓ Produkty nagrodzone i docenione przez konsumentów
✓ Konkurencyjne marże (25-45% w zależności od kategorii)
✓ Wsparcie marketingowe i merchandising
✓ Elastyczne warunki płatności
✓ Gwarancję jakości i terminowych dostaw

Dołącz do grona naszych partnerów i rozwijaj sprzedaż razem z FreshLife!
"""
