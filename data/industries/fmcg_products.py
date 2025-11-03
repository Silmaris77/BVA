"""
Pełny katalog produktów FMCG
- 12 produktów FreshLife (własne)
- 36 produktów konkurencji (dystrybuowane)
"""

# ============================================================================
# FRESHLIFE PRODUCTS (Własne produkty - wyższa marża)
# ============================================================================

FRESHLIFE_PRODUCTS = {
    # PERSONAL CARE
    "pc_001": {
        "id": "pc_001",
        "name": "BodyWash Natural",
        "brand": "FreshLife",
        "category": "Personal Care",
        "subcategory": "Żele pod prysznic",
        "emoji": "🧴",
        "variants": ["Aloe & Green Tea", "Coconut & Shea", "Lavender Calm"],
        "base_variant": "Aloe & Green Tea 250ml",
        
        # PRICING - MODEL REALISTYCZNY (przez hurtownię)
        "price_retail": 12.99,  # Cena w sklepie
        "price_wholesale_eurocash": 10.50,  # Cena hurtowni (Eurocash) dla sklepu
        "price_freshlife_to_eurocash": 7.50,  # Cena producenta dla hurtowni
        "margin_shop_percent": 19,  # Marża sklepu (kupuje od Eurocash)
        "margin_shop_pln": 2.49,  # Ile zarabia sklep na 1 sztuce
        "margin_eurocash_percent": 40,  # Marża hurtowni
        "margin_freshlife_percent": 25,  # Marża producenta (COGS: 6.00 zł)
        
        # DISTRIBUTION MODEL
        "distribution_model": "wholesale",  # wholesale / direct / hybrid
        "available_at": ["Eurocash", "Makro Cash & Carry", "FMCG24"],
        "eurocash_sku": "FL-PC001-250",  # Kod w systemie Eurocash
        
        # ORDERING
        "moq_freshlife": 6,  # MOQ bezpośrednio od FreshLife (dla testów)
        "moq_eurocash": 1,  # MOQ w Eurocash (dla sklepów)
        "payment_terms_eurocash": "Przelew 14 dni",
        "payment_terms_direct": "Przelew 14 dni lub gotówka",
        "delivery_free_threshold": 300,  # Darmowa dostawa od X zł (bezpośrednia)
        
        # LOGISTICS
        "shelf_space_cm": 15,  # Ile cm zajmuje na półce
        "case_size": 12,  # Ile sztuk w kartonie
        "cases_per_pallet": 80,
        "popularity": 72,  # 0-100
        "shelf_life_days": 1080,
        "packaging": "Butelka PET z recyclingu 250ml, pompka",
        
        # STORYTELLING
        "description": "Naturalny żel pod prysznic z ekstraktami z aloesu i zielonej herbaty. Bez parabenów, SLS i barwników. Idealny dla skóry wrażliwej. Piękne, ekologiczne opakowanie z recyclingu.",
        "target_customer": "Kobiety 25-45 lat świadome składu, rodzice szukający bezpiecznych produktów, osoby z wrażliwą skórą, ekologiczni konsumenci",
        "rotation_speed": "Szybka (7-10 dni przy 10 szt) = 3-4 rotacje/mies",
        "rotation_speed_context": "Przy rotacji 3x/mies i marży 2.49 zł = 7.47 zł zysku/mies z 15 cm półki. Dove rotuje 1x/mies przy marży 2.88 zł = 2.88 zł/mies.",
        "suggested_initial_order": "6-10 szt (pierwsze zamówienie testowe bezpośrednio od FreshLife), potem przez Eurocash",
        
        # PRZEWAGI NAD KONKURENCJĄ (BEZ MARŻ KONKURENCJI - realistycznie!)
        "competitors": [
            {
                "brand": "Dove Natural",
                "price_retail": 15.99,
                "price_wholesale_estimated": 13.11,  # Szacowana (nie znamy dokładnie)
                "moq_estimated": 24,
                "shelf_space_cm": 15,
                "rotation_estimated": "Wolna (30 dni)",
                "advantages": [
                    "💰 Tańszy dla klienta: 12.99 zł vs 15.99 zł (oszczędność 3 zł)",
                    "💵 Lepsza marża dla Pana: zarobi Pan 2.49 zł vs ~2.88 zł, ALE rotacja 3x szybsza!",
                    "📦 Niższe MOQ: może Pan zacząć od 6 szt (u nas bezpośrednio) vs 24 szt Dove",
                    "♻️ 97% naturalnych składników vs 85% (Dove)",
                    "🌱 Opakowanie z recyclingu - przyciąga ekologicznych klientów"
                ]
            },
            {
                "brand": "Fa Natural",
                "price_retail": 13.99,
                "price_wholesale_estimated": 11.19,
                "moq_estimated": 12,
                "shelf_space_cm": 15,
                "rotation_estimated": "Średnia (20 dni)",
                "advantages": [
                    "💰 Tańszy dla klienta: 12.99 zł vs 13.99 zł",
                    "♻️ Bardziej naturalny skład: 97% vs 85%",
                    "📦 Podobne MOQ, ale lepsza rotacja (10 dni vs 20 dni)",
                    "🌱 Opakowanie z recyclingu (Fa - plastik pierwotny)"
                ]
            }
        ],
        
        # ARGUMENTY SPRZEDAŻOWE - dostosowane do modelu przez hurtownię
        "sales_arguments": [
            "📦 Nasz produkt jest dostępny w Eurocash pod kodem FL-PC001-250. Może Pan zamówić przez swoje konto online lub zadzwonić do przedstawiciela. Cena 10.50 zł, sprzeda Pan za 12.99 - to 2.49 zł na sztuce.",
            "🔄 Kluczowa sprawa: nasz produkt rotuje w 7-10 dni, Dove w 30. To oznacza że zarobi Pan WIĘCEJ mimo niższej marży jednostkowej: 3 rotacje/mies x 2.49 zł = 7.47 zł vs 1 rotacja Dove x 2.88 zł = 2.88 zł.",
            "💡 Może Pan zacząć testowo - zamówię bezpośrednio 6 sztuk. Jeśli się sprawdzi (a zazwyczaj tak jest), będzie Pan zamawiał przez Eurocash. Małe ryzyko, duży potencjał.",
            "🛒 Klienci szukają oszczędności: 12.99 zł zamiast 15.99 za Dove to argument, który działa. Szczególnie w małych sklepach, gdzie klient liczy każdą złotówkę.",
            "♻️ Naturalny skład i ekologiczne opakowanie - to trend! Młodsi klienci (25-40 lat) coraz częściej patrzą na skład i pochodzenie opakowania."
        ],
        
        "usp": "97% naturalnych składników, 0% parabenów i SLS, opakowanie z recyclingu, szybka rotacja",
        "awards": [],
        "promo_support": True,
        "pos_materials": ["Wobbler", "Shelf strip", "Tester", "Ulotka składnikowa"],
    },
    
    "pc_002": {
        "id": "pc_002",
        "name": "SilkHair",
        "brand": "FreshLife",
        "category": "Personal Care",
        "subcategory": "Szampony",
        "variants": ["Volume", "Repair", "Color Protection", "Anti-Dandruff"],
        "base_variant": "Volume 400ml",
        "price_retail": 18.00,
        "price_wholesale": 10.80,
        "margin_percent": 40,
        "moq": 12,
        "popularity": 68,
        "shelf_life_days": 1080,
        "packaging": "Butelka HDPE 400ml",
        "usp": "Technologia Keratin Complex, efekt salonu w domu",
        "awards": ["Beauty Awards 2024"],
        "promo_support": True,
        "pos_materials": ["Wobbler", "Leaflet"],
    },
    
    "pc_003": {
        "id": "pc_003",
        "name": "DeoActive",
        "brand": "FreshLife",
        "category": "Personal Care",
        "subcategory": "Dezodoranty",
        "variants": ["Men Sport", "Men Classic", "Women Fresh", "Women Sensitive"],
        "base_variant": "Men Sport 150ml",
        "price_retail": 12.00,
        "price_wholesale": 6.96,
        "margin_percent": 42,
        "moq": 24,
        "popularity": 71,
        "shelf_life_days": 900,
        "packaging": "Aerozol 150ml",
        "usp": "48h ochrony, 0% aluminium",
        "awards": [],
        "promo_support": True,
        "pos_materials": ["Counter display", "Tester"],
    },
    
    # FOOD
    "food_001": {
        "id": "food_001",
        "name": "MorningJoy",
        "brand": "FreshLife",
        "category": "Food",
        "subcategory": "Płatki śniadaniowe",
        "variants": ["Chocolate", "Honey", "Fruits", "Fitness"],
        "base_variant": "Chocolate 500g",
        "price_retail": 14.00,
        "price_wholesale": 10.08,
        "margin_percent": 28,
        "moq": 12,
        "popularity": 62,
        "shelf_life_days": 365,
        "packaging": "Karton 500g",
        "usp": "Pełne ziarno, bez cukru dodanego w wersji Fitness",
        "awards": [],
        "promo_support": True,
        "pos_materials": ["Shelf strip", "Recipe cards"],
    },
    
    "food_002": {
        "id": "food_002",
        "name": "QuickSoup",
        "brand": "FreshLife",
        "category": "Food",
        "subcategory": "Zupy instant",
        "variants": ["Rosół", "Pomidorowa", "Grochówka", "Krem z pieczarek"],
        "base_variant": "Rosół",
        "price_retail": 4.00,
        "price_wholesale": 2.72,
        "margin_percent": 32,
        "moq": 24,
        "popularity": 70,
        "shelf_life_days": 540,
        "packaging": "Saszetka 60g",
        "usp": "Gotowa w 3 minuty, bez konserwantów",
        "awards": [],
        "promo_support": True,
        "pos_materials": ["Counter display", "Sampling"],
    },
    
    "food_003": {
        "id": "food_003",
        "name": "TomatoRed",
        "brand": "FreshLife",
        "category": "Food",
        "subcategory": "Ketchupy i sosy",
        "variants": ["Classic", "Pikantny", "Bez cukru", "Kids"],
        "base_variant": "Classic 470g",
        "price_retail": 11.99,
        "price_wholesale": 7.19,
        "margin_percent": 40,
        "moq": 12,
        "popularity": 96,
        "shelf_life_days": 540,
        "packaging": "Butelka szklana 470g",
        "usp": "Kultowy smak, z naturalnych pomidorów",
        "awards": ["Konsumencki Lider Jakości 2024"],
        "promo_support": True,
        "pos_materials": ["Display", "Wobbler", "Shelf strip"],
    },
    
    # HOME CARE
    "hc_001": {
        "id": "hc_001",
        "name": "SparkleClean",
        "brand": "FreshLife",
        "category": "Home Care",
        "subcategory": "Płyny do mycia podłóg",
        "variants": ["Universal", "Wood", "Tiles", "Antibacterial"],
        "base_variant": "Universal 1L",
        "price_retail": 12.50,
        "price_wholesale": 7.75,
        "margin_percent": 38,
        "moq": 12,
        "popularity": 66,
        "shelf_life_days": 730,
        "packaging": "Butelka PET 1L",
        "usp": "Błysk bez smug, biodegradowalna formuła",
        "awards": [],
        "promo_support": True,
        "pos_materials": ["Wobbler", "Demo video"],
    },
    
    "hc_002": {
        "id": "hc_002",
        "name": "DishPro",
        "brand": "FreshLife",
        "category": "Home Care",
        "subcategory": "Płyny do naczyń",
        "variants": ["Lemon", "Apple", "Sensitive", "Power Grease"],
        "base_variant": "Lemon 500ml",
        "price_retail": 7.50,
        "price_wholesale": 4.50,
        "margin_percent": 40,
        "moq": 24,
        "popularity": 73,
        "shelf_life_days": 730,
        "packaging": "Butelka PET 500ml",
        "usp": "Usuwa tłuszcz już w 30°C, łagodny dla rąk",
        "awards": [],
        "promo_support": True,
        "pos_materials": ["Counter display", "Tester"],
    },
    
    "hc_003": {
        "id": "hc_003",
        "name": "FreshAir",
        "brand": "FreshLife",
        "category": "Home Care",
        "subcategory": "Odświeżacze powietrza",
        "variants": ["Lavender", "Ocean", "Forest", "Citrus"],
        "base_variant": "Lavender 300ml",
        "price_retail": 15.00,
        "price_wholesale": 8.25,
        "margin_percent": 45,
        "moq": 12,
        "popularity": 64,
        "shelf_life_days": 900,
        "packaging": "Aerozol 300ml",
        "usp": "Neutralizuje zapachy zamiast maskować",
        "awards": [],
        "promo_support": True,
        "pos_materials": ["Wobbler", "Tester"],
    },
    
    # SNACKS (nowe kategorie FreshLife)
    "snack_001": {
        "id": "snack_001",
        "name": "CrunchBites",
        "brand": "FreshLife",
        "category": "Snacks",
        "subcategory": "Chipsy",
        "variants": ["Paprika", "Sól morska", "Śmietana-cebula", "BBQ"],
        "base_variant": "Paprika 150g",
        "price_retail": 5.50,
        "price_wholesale": 3.85,
        "margin_percent": 30,
        "moq": 24,
        "popularity": 69,
        "shelf_life_days": 180,
        "packaging": "Torebka foliowa 150g",
        "usp": "Pieczone nie smażone, -30% tłuszczu",
        "awards": [],
        "promo_support": True,
        "pos_materials": ["Counter display", "Wobbler"],
    },
    
    "snack_002": {
        "id": "snack_002",
        "name": "NutMix",
        "brand": "FreshLife",
        "category": "Snacks",
        "subcategory": "Orzechy i bakalie",
        "variants": ["Classic Mix", "Sport Mix", "Exotic Mix", "Party Mix"],
        "base_variant": "Classic Mix 200g",
        "price_retail": 12.00,
        "price_wholesale": 8.40,
        "margin_percent": 30,
        "moq": 12,
        "popularity": 61,
        "shelf_life_days": 270,
        "packaging": "Torebka foliowa 200g",
        "usp": "Prażone bez oleju, naturalne smaki",
        "awards": [],
        "promo_support": False,
        "pos_materials": ["Shelf strip"],
    },
    
    "bev_001": {
        "id": "bev_001",
        "name": "FreshTea",
        "brand": "FreshLife",
        "category": "Beverages",
        "subcategory": "Herbaty mrożone",
        "variants": ["Lemon", "Peach", "Forest Fruits", "Green Tea"],
        "base_variant": "Lemon 500ml",
        "price_retail": 3.50,
        "price_wholesale": 2.45,
        "margin_percent": 30,
        "moq": 24,
        "popularity": 72,
        "shelf_life_days": 180,
        "packaging": "Butelka PET 500ml",
        "usp": "Bez cukru, zaparzona na zimno",
        "awards": [],
        "promo_support": True,
        "pos_materials": ["Chłodziarka branded", "Wobbler"],
    },
}


# ============================================================================
# COMPETITOR PRODUCTS (Produkty konkurencji - dystrybuowane, niższa marża)
# ============================================================================

COMPETITOR_PRODUCTS = {
    # PERSONAL CARE - Konkurencja dla CleanFresh (żele)
    "comp_pc_001": {
        "id": "comp_pc_001",
        "name": "Dove Men+Care",
        "brand": "Dove",
        "manufacturer": "Unilever",
        "category": "Personal Care",
        "subcategory": "Żele pod prysznic",
        "base_variant": "Clean Comfort 400ml",
        "price_retail": 14.00,
        "price_wholesale": 11.90,
        "margin_percent": 15,
        "moq": 6,
        "popularity": 92,
        "shelf_life_days": 1080,
        "packaging": "Butelka PET 400ml",
        "usp": "Nawilża i chroni skórę, technologia MicroMoisture",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_pc_002": {
        "id": "comp_pc_002",
        "name": "Nivea Men",
        "brand": "Nivea",
        "manufacturer": "Beiersdorf",
        "category": "Personal Care",
        "subcategory": "Żele pod prysznic",
        "base_variant": "Deep 500ml",
        "price_retail": 12.00,
        "price_wholesale": 10.20,
        "margin_percent": 15,
        "moq": 6,
        "popularity": 89,
        "shelf_life_days": 1080,
        "packaging": "Butelka PET 500ml",
        "usp": "Oczyszcza i odświeża, węgiel aktywny",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_pc_003": {
        "id": "comp_pc_003",
        "name": "Palmolive Men",
        "brand": "Palmolive",
        "manufacturer": "Colgate-Palmolive",
        "category": "Personal Care",
        "subcategory": "Żele pod prysznic",
        "base_variant": "Revitalising Sport 500ml",
        "price_retail": 9.00,
        "price_wholesale": 7.65,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 78,
        "shelf_life_days": 1080,
        "packaging": "Butelka PET 500ml",
        "usp": "Odświeża i energetyzuje",
        "promo_support": False,
        "pos_materials": [],
    },
    
    # PERSONAL CARE - Konkurencja dla SilkHair (szampony)
    "comp_pc_004": {
        "id": "comp_pc_004",
        "name": "L'Oréal Elseve",
        "brand": "L'Oréal Paris",
        "manufacturer": "L'Oréal",
        "category": "Personal Care",
        "subcategory": "Szampony",
        "base_variant": "Full Resist 400ml",
        "price_retail": 22.00,
        "price_wholesale": 18.70,
        "margin_percent": 15,
        "moq": 6,
        "popularity": 94,
        "shelf_life_days": 1080,
        "packaging": "Butelka PET 400ml",
        "usp": "Wzmacnia włosy, zapobiega wypadaniu",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_pc_005": {
        "id": "comp_pc_005",
        "name": "Dove Repair",
        "brand": "Dove",
        "manufacturer": "Unilever",
        "category": "Personal Care",
        "subcategory": "Szampony",
        "base_variant": "Intensive Repair 400ml",
        "price_retail": 18.00,
        "price_wholesale": 15.30,
        "margin_percent": 15,
        "moq": 6,
        "popularity": 91,
        "shelf_life_days": 1080,
        "packaging": "Butelka PET 400ml",
        "usp": "Regeneruje zniszczone włosy od środka",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_pc_006": {
        "id": "comp_pc_006",
        "name": "Head & Shoulders",
        "brand": "Head & Shoulders",
        "manufacturer": "Procter & Gamble",
        "category": "Personal Care",
        "subcategory": "Szampony",
        "base_variant": "Classic Clean 400ml",
        "price_retail": 20.00,
        "price_wholesale": 17.00,
        "margin_percent": 15,
        "moq": 6,
        "popularity": 96,
        "shelf_life_days": 1080,
        "packaging": "Butelka PET 400ml",
        "usp": "Skutecznie zwalcza łupież",
        "promo_support": False,
        "pos_materials": [],
    },
    
    # PERSONAL CARE - Konkurencja dla DeoActive (dezodoranty)
    "comp_pc_007": {
        "id": "comp_pc_007",
        "name": "Rexona Men",
        "brand": "Rexona",
        "manufacturer": "Unilever",
        "category": "Personal Care",
        "subcategory": "Dezodoranty",
        "base_variant": "Sport Defence 150ml",
        "price_retail": 13.00,
        "price_wholesale": 11.05,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 93,
        "shelf_life_days": 900,
        "packaging": "Aerozol 150ml",
        "usp": "Ochrona do 96h, MotionSense",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_pc_008": {
        "id": "comp_pc_008",
        "name": "Nivea Deo",
        "brand": "Nivea",
        "manufacturer": "Beiersdorf",
        "category": "Personal Care",
        "subcategory": "Dezodoranty",
        "base_variant": "Fresh Active 150ml",
        "price_retail": 11.00,
        "price_wholesale": 9.35,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 88,
        "shelf_life_days": 900,
        "packaging": "Aerozol 150ml",
        "usp": "48h ochrony, Ocean Extracts",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_pc_009": {
        "id": "comp_pc_009",
        "name": "Fa Men",
        "brand": "Fa",
        "manufacturer": "Henkel",
        "category": "Personal Care",
        "subcategory": "Dezodoranty",
        "base_variant": "Sport Energy Boost 150ml",
        "price_retail": 9.50,
        "price_wholesale": 8.08,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 82,
        "shelf_life_days": 900,
        "packaging": "Aerozol 150ml",
        "usp": "Ochrona 48h, Guarana extract",
        "promo_support": False,
        "pos_materials": [],
    },
    
    # FOOD - Konkurencja dla MorningJoy (płatki)
    "comp_food_001": {
        "id": "comp_food_001",
        "name": "Nesquik",
        "brand": "Nesquik",
        "manufacturer": "Nestlé",
        "category": "Food",
        "subcategory": "Płatki śniadaniowe",
        "base_variant": "Chocolate 450g",
        "price_retail": 16.00,
        "price_wholesale": 13.60,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 95,
        "shelf_life_days": 365,
        "packaging": "Karton 450g",
        "usp": "Kultowy smak czekolady, bez sztucznych barwników",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_food_002": {
        "id": "comp_food_002",
        "name": "Fitness Nestlé",
        "brand": "Fitness",
        "manufacturer": "Nestlé",
        "category": "Food",
        "subcategory": "Płatki śniadaniowe",
        "base_variant": "Fruits 400g",
        "price_retail": 14.00,
        "price_wholesale": 11.90,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 87,
        "shelf_life_days": 365,
        "packaging": "Karton 400g",
        "usp": "Pełne ziarno, niskokaloryczne",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_food_003": {
        "id": "comp_food_003",
        "name": "Kellogg's Corn Flakes",
        "brand": "Kellogg's",
        "manufacturer": "Kellogg Company",
        "category": "Food",
        "subcategory": "Płatki śniadaniowe",
        "base_variant": "Original 500g",
        "price_retail": 15.00,
        "price_wholesale": 12.75,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 90,
        "shelf_life_days": 365,
        "packaging": "Karton 500g",
        "usp": "Oryginalne płatki kukurydziane od 1906",
        "promo_support": False,
        "pos_materials": [],
    },
    
    # FOOD - Konkurencja dla QuickSoup (zupy)
    "comp_food_004": {
        "id": "comp_food_004",
        "name": "Knorr",
        "brand": "Knorr",
        "manufacturer": "Unilever",
        "category": "Food",
        "subcategory": "Zupy instant",
        "base_variant": "Rosół instant",
        "price_retail": 4.50,
        "price_wholesale": 3.83,
        "margin_percent": 15,
        "moq": 24,
        "popularity": 96,
        "shelf_life_days": 540,
        "packaging": "Saszetka",
        "usp": "Numer 1 w Polsce, naturalny smak",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_food_005": {
        "id": "comp_food_005",
        "name": "Winiary",
        "brand": "Winiary",
        "manufacturer": "Nestlé",
        "category": "Food",
        "subcategory": "Zupy instant",
        "base_variant": "Pomidorowa",
        "price_retail": 4.00,
        "price_wholesale": 3.40,
        "margin_percent": 15,
        "moq": 24,
        "popularity": 93,
        "shelf_life_days": 540,
        "packaging": "Saszetka",
        "usp": "Polska marka, tradycyjny smak",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_food_006": {
        "id": "comp_food_006",
        "name": "Amino",
        "brand": "Amino",
        "manufacturer": "Gellwe",
        "category": "Food",
        "subcategory": "Zupy instant",
        "base_variant": "Grochówka",
        "price_retail": 3.50,
        "price_wholesale": 2.98,
        "margin_percent": 15,
        "moq": 24,
        "popularity": 84,
        "shelf_life_days": 540,
        "packaging": "Saszetka",
        "usp": "Bogata w aminokwasy",
        "promo_support": False,
        "pos_materials": [],
    },
    
    # FOOD - Konkurencja dla TomatoRed (ketchupy)
    "comp_food_007": {
        "id": "comp_food_007",
        "name": "Fanex Ketchup Pomidorowy",
        "brand": "Fanex",
        "manufacturer": "Fanex Foods",
        "category": "Food",
        "subcategory": "Ketchupy i sosy",
        "base_variant": "Classic 480g",
        "price_retail": 10.99,
        "price_wholesale": 9.34,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 92,
        "shelf_life_days": 540,
        "packaging": "Butelka PET 480g",
        "usp": "Gęsty, z naturalnych pomidorów",
        "promo_support": True,
        "pos_materials": ["Display", "Wobbler"],
    },
    
    "comp_food_008": {
        "id": "comp_food_008",
        "name": "Kotlin Ketchup Łagodny",
        "brand": "Kotlin",
        "manufacturer": "Agros-Nova",
        "category": "Food",
        "subcategory": "Ketchupy i sosy",
        "base_variant": "Łagodny 450g",
        "price_retail": 7.99,
        "price_wholesale": 6.79,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 84,
        "shelf_life_days": 540,
        "packaging": "Butelka PET 450g",
        "usp": "Polski produkt, doskonała cena",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_food_009": {
        "id": "comp_food_009",
        "name": "Łowicz Ketchup Pikantny",
        "brand": "Łowicz",
        "manufacturer": "ZPOW Łowicz",
        "category": "Food",
        "subcategory": "Ketchupy i sosy",
        "base_variant": "Pikantny 480g",
        "price_retail": 8.49,
        "price_wholesale": 7.22,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 88,
        "shelf_life_days": 540,
        "packaging": "Butelka PET 480g",
        "usp": "Z polskich pomidorów, pikantna nuta",
        "promo_support": True,
        "pos_materials": ["Shelf strip"],
    },
    
    # HOME CARE - Konkurencja dla SparkleClean (podłogi)
    "comp_hc_001": {
        "id": "comp_hc_001",
        "name": "Domestos",
        "brand": "Domestos",
        "manufacturer": "Unilever",
        "category": "Home Care",
        "subcategory": "Płyny do mycia podłóg",
        "base_variant": "Universal 1L",
        "price_retail": 14.00,
        "price_wholesale": 11.90,
        "margin_percent": 15,
        "moq": 6,
        "popularity": 92,
        "shelf_life_days": 730,
        "packaging": "Butelka PET 1L",
        "usp": "Zabija 99.9% bakterii",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_hc_002": {
        "id": "comp_hc_002",
        "name": "Cillit Bang",
        "brand": "Cillit Bang",
        "manufacturer": "Reckitt Benckiser",
        "category": "Home Care",
        "subcategory": "Płyny do mycia podłóg",
        "base_variant": "Power Cleaner 1L",
        "price_retail": 16.00,
        "price_wholesale": 13.60,
        "margin_percent": 15,
        "moq": 6,
        "popularity": 88,
        "shelf_life_days": 730,
        "packaging": "Butelka PET 1L",
        "usp": "Usuwa tłuszcz i zabrudzenia bez wysiłku",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_hc_003": {
        "id": "comp_hc_003",
        "name": "Ludwik",
        "brand": "Ludwik",
        "manufacturer": "Inco",
        "category": "Home Care",
        "subcategory": "Płyny do mycia podłóg",
        "base_variant": "Universal 1L",
        "price_retail": 9.00,
        "price_wholesale": 7.65,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 86,
        "shelf_life_days": 730,
        "packaging": "Butelka PET 1L",
        "usp": "Polska marka, sprawdzony skład",
        "promo_support": False,
        "pos_materials": [],
    },
    
    # HOME CARE - Konkurencja dla DishPro (naczynia)
    "comp_hc_004": {
        "id": "comp_hc_004",
        "name": "Fairy",
        "brand": "Fairy",
        "manufacturer": "Procter & Gamble",
        "category": "Home Care",
        "subcategory": "Płyny do naczyń",
        "base_variant": "Lemon 500ml",
        "price_retail": 9.00,
        "price_wholesale": 7.65,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 97,
        "shelf_life_days": 730,
        "packaging": "Butelka PET 500ml",
        "usp": "Usuwa tłuszcz już w zimnej wodzie",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_hc_005": {
        "id": "comp_hc_005",
        "name": "Ludwik Naczynia",
        "brand": "Ludwik",
        "manufacturer": "Inco",
        "category": "Home Care",
        "subcategory": "Płyny do naczyń",
        "base_variant": "Aloes 500ml",
        "price_retail": 6.50,
        "price_wholesale": 5.53,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 89,
        "shelf_life_days": 730,
        "packaging": "Butelka PET 500ml",
        "usp": "Skuteczny i delikatny dla rąk",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_hc_006": {
        "id": "comp_hc_006",
        "name": "Persil",
        "brand": "Persil",
        "manufacturer": "Henkel",
        "category": "Home Care",
        "subcategory": "Płyny do naczyń",
        "base_variant": "Green Power 450ml",
        "price_retail": 8.00,
        "price_wholesale": 6.80,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 83,
        "shelf_life_days": 730,
        "packaging": "Butelka PET 450ml",
        "usp": "Skuteczny i ekologiczny",
        "promo_support": False,
        "pos_materials": [],
    },
    
    # HOME CARE - Konkurencja dla FreshAir (odświeżacze)
    "comp_hc_007": {
        "id": "comp_hc_007",
        "name": "Air Wick",
        "brand": "Air Wick",
        "manufacturer": "Reckitt Benckiser",
        "category": "Home Care",
        "subcategory": "Odświeżacze powietrza",
        "base_variant": "Lavender 300ml",
        "price_retail": 16.00,
        "price_wholesale": 13.60,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 94,
        "shelf_life_days": 900,
        "packaging": "Aerozol 300ml",
        "usp": "Naturalne olejki eteryczne",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_hc_008": {
        "id": "comp_hc_008",
        "name": "Glade",
        "brand": "Glade",
        "manufacturer": "SC Johnson",
        "category": "Home Care",
        "subcategory": "Odświeżacze powietrza",
        "base_variant": "Ocean Escape 300ml",
        "price_retail": 14.00,
        "price_wholesale": 11.90,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 91,
        "shelf_life_days": 900,
        "packaging": "Aerozol 300ml",
        "usp": "Długotrwały świeży zapach",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_hc_009": {
        "id": "comp_hc_009",
        "name": "Brise",
        "brand": "Brise",
        "manufacturer": "Henkel",
        "category": "Home Care",
        "subcategory": "Odświeżacze powietrza",
        "base_variant": "Fresh Cotton 300ml",
        "price_retail": 12.00,
        "price_wholesale": 10.20,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 85,
        "shelf_life_days": 900,
        "packaging": "Aerozol 300ml",
        "usp": "Odświeża i neutralizuje",
        "promo_support": False,
        "pos_materials": [],
    },
    
    # SNACKS - Konkurencja dla CrunchBites (chipsy)
    "comp_snack_001": {
        "id": "comp_snack_001",
        "name": "Lay's",
        "brand": "Lay's",
        "manufacturer": "PepsiCo",
        "category": "Snacks",
        "subcategory": "Chipsy",
        "base_variant": "Papryka 140g",
        "price_retail": 6.00,
        "price_wholesale": 5.10,
        "margin_percent": 15,
        "moq": 24,
        "popularity": 98,
        "shelf_life_days": 180,
        "packaging": "Torebka 140g",
        "usp": "Numer 1 na świecie",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_snack_002": {
        "id": "comp_snack_002",
        "name": "Pringles",
        "brand": "Pringles",
        "manufacturer": "Kellogg's",
        "category": "Snacks",
        "subcategory": "Chipsy",
        "base_variant": "Original 165g",
        "price_retail": 8.50,
        "price_wholesale": 7.23,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 95,
        "shelf_life_days": 270,
        "packaging": "Tuba 165g",
        "usp": "Unikalna forma i opakowanie",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_snack_003": {
        "id": "comp_snack_003",
        "name": "Chio Chips",
        "brand": "Chio",
        "manufacturer": "Intersnack",
        "category": "Snacks",
        "subcategory": "Chipsy",
        "base_variant": "Sól 150g",
        "price_retail": 5.50,
        "price_wholesale": 4.68,
        "margin_percent": 15,
        "moq": 24,
        "popularity": 87,
        "shelf_life_days": 180,
        "packaging": "Torebka 150g",
        "usp": "Chrupkie i smaczne",
        "promo_support": False,
        "pos_materials": [],
    },
    
    # SNACKS - Konkurencja dla NutMix (orzechy)
    "comp_snack_004": {
        "id": "comp_snack_004",
        "name": "Helio Mix",
        "brand": "Helio",
        "manufacturer": "Aksam",
        "category": "Snacks",
        "subcategory": "Orzechy i bakalie",
        "base_variant": "Student Mix 200g",
        "price_retail": 13.00,
        "price_wholesale": 11.05,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 82,
        "shelf_life_days": 270,
        "packaging": "Torebka 200g",
        "usp": "Polska marka, naturalne orzechy",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_snack_005": {
        "id": "comp_snack_005",
        "name": "Bakalland Mix",
        "brand": "Bakalland",
        "manufacturer": "Bakalland",
        "category": "Snacks",
        "subcategory": "Orzechy i bakalie",
        "base_variant": "Energy Mix 180g",
        "price_retail": 14.00,
        "price_wholesale": 11.90,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 88,
        "shelf_life_days": 270,
        "packaging": "Torebka 180g",
        "usp": "Wysokiej jakości owoce i orzechy",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_snack_006": {
        "id": "comp_snack_006",
        "name": "Alesto Mix",
        "brand": "Alesto",
        "manufacturer": "Lidl",
        "category": "Snacks",
        "subcategory": "Orzechy i bakalie",
        "base_variant": "Premium Mix 200g",
        "price_retail": 11.00,
        "price_wholesale": 9.35,
        "margin_percent": 15,
        "moq": 12,
        "popularity": 79,
        "shelf_life_days": 270,
        "packaging": "Torebka 200g",
        "usp": "Private label, dobra cena",
        "promo_support": False,
        "pos_materials": [],
    },
    
    # BEVERAGES - Konkurencja dla FreshTea (herbaty mrożone)
    "comp_bev_001": {
        "id": "comp_bev_001",
        "name": "Lipton Ice Tea",
        "brand": "Lipton",
        "manufacturer": "PepsiCo",
        "category": "Beverages",
        "subcategory": "Herbaty mrożone",
        "base_variant": "Lemon 500ml",
        "price_retail": 4.00,
        "price_wholesale": 3.40,
        "margin_percent": 15,
        "moq": 24,
        "popularity": 96,
        "shelf_life_days": 180,
        "packaging": "Butelka PET 500ml",
        "usp": "Numer 1 na świecie",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_bev_002": {
        "id": "comp_bev_002",
        "name": "Fuze Tea",
        "brand": "Fuze Tea",
        "manufacturer": "Coca-Cola",
        "category": "Beverages",
        "subcategory": "Herbaty mrożone",
        "base_variant": "Peach 500ml",
        "price_retail": 3.80,
        "price_wholesale": 3.23,
        "margin_percent": 15,
        "moq": 24,
        "popularity": 92,
        "shelf_life_days": 180,
        "packaging": "Butelka PET 500ml",
        "usp": "Naturalny smak owoców",
        "promo_support": False,
        "pos_materials": [],
    },
    
    "comp_bev_003": {
        "id": "comp_bev_003",
        "name": "Nestea",
        "brand": "Nestea",
        "manufacturer": "Nestlé",
        "category": "Beverages",
        "subcategory": "Herbaty mrożone",
        "base_variant": "Green Tea 500ml",
        "price_retail": 3.50,
        "price_wholesale": 2.98,
        "margin_percent": 15,
        "moq": 24,
        "popularity": 89,
        "shelf_life_days": 180,
        "packaging": "Butelka PET 500ml",
        "usp": "Zielona herbata, antyoksydanty",
        "promo_support": False,
        "pos_materials": [],
    },
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_all_products():
    """Zwraca wszystkie produkty (FreshLife + Heinz + konkurencja)"""
    all_products = {}
    all_products.update(FRESHLIFE_PRODUCTS)
    all_products.update(HEINZ_PRODUCTS)
    all_products.update(COMPETITOR_PRODUCTS)
    return all_products


def get_freshlife_products():
    """Zwraca tylko produkty FreshLife"""
    return FRESHLIFE_PRODUCTS


def get_heinz_products():
    """Zwraca tylko produkty Heinz"""
    return HEINZ_PRODUCTS


def get_competitor_products():
    """Zwraca tylko produkty konkurencji"""
    return COMPETITOR_PRODUCTS


def get_products_by_category(category):
    """Zwraca produkty z danej kategorii (wszystkie)"""
    all_prods = get_all_products()
    return {k: v for k, v in all_prods.items() if v['category'] == category}


def get_product_by_id(product_id):
    """Zwraca produkt po ID"""
    all_prods = get_all_products()
    return all_prods.get(product_id)


def get_competitors_for_product(freshlife_id):
    """
    Znajduje produkty konkurencji w tej samej kategorii co produkt FreshLife
    
    Returns:
        list - IDs produktów konkurencji (max 3)
    """
    fl_product = FRESHLIFE_PRODUCTS.get(freshlife_id)
    if not fl_product:
        return []
    
    category = fl_product["category"]
    
    # Znajdź konkurentów w tej samej kategorii
    competitors = [
        comp_id for comp_id, comp in COMPETITOR_PRODUCTS.items()
        if comp["category"] == category
    ]
    
    # Zwróć max 3
    return competitors[:3]


def compare_products(freshlife_id, competitor_ids):
    """
    Porównuje produkt FreshLife z produktami konkurencji
    
    Returns:
        dict - porównanie: marża, cena, popularność
    """
    fl_product = FRESHLIFE_PRODUCTS.get(freshlife_id)
    if not fl_product:
        return None
    
    comparison = {
        "freshlife": fl_product,
        "competitors": [],
        "advantages": [],
        "disadvantages": []
    }
    
    for comp_id in competitor_ids:
        comp = COMPETITOR_PRODUCTS.get(comp_id)
        if comp:
            comparison["competitors"].append(comp)
            
            # Analiza przewag
            if fl_product["margin_percent"] > comp["margin_percent"]:
                comparison["advantages"].append(f"Wyższa marża niż {comp['name']} (+{fl_product['margin_percent'] - comp['margin_percent']}pp)")
            
            if fl_product["price_retail"] < comp["price_retail"]:
                comparison["advantages"].append(f"Niższa cena niż {comp['name']} ({comp['price_retail'] - fl_product['price_retail']:.2f} PLN taniej)")
            
            if fl_product["popularity"] < comp["popularity"]:
                comparison["disadvantages"].append(f"Mniejsza rozpoznawalność niż {comp['name']} ({comp['popularity'] - fl_product['popularity']} pkt)")
    
    return comparison


# Przykład użycia porównania
def get_sales_pitch(product_id):
    """Generuje sales pitch dla produktu FreshLife"""
    product = FRESHLIFE_PRODUCTS.get(product_id)
    if not product:
        return "Produkt nie znaleziony"
    
    pitch = f"""
🎯 {product['name']} - {product['subcategory']}

💰 KORZYŚCI FINANSOWE:
- Cena detaliczna: {product['price_retail']:.2f} PLN
- Cena hurt: {product['price_wholesale']:.2f} PLN  
- Marża: {product['margin_percent']}% (vs konkurencja 15%)
- MOQ: tylko {product['moq']} szt.

✨ USP: {product['usp']}

📦 WSPARCIE:
"""
    
    if product.get('promo_support'):
        pitch += "- Wsparcie promocyjne\n"
    if product.get('pos_materials'):
        pitch += f"- Materiały POS: {', '.join(product['pos_materials'])}\n"
    
    
    if product.get('awards'):
        pitch += f"\n🏆 NAGRODY:\n"
        for award in product['awards']:
            pitch += f"- {award}\n"
    
    return pitch


# ============================================================================
# HEINZ PRODUCTS (Food Service Channel)
# ============================================================================

HEINZ_PRODUCTS = {
    "heinz_ketchup_classic": {
        "id": "heinz_ketchup_classic",
        "name": "Heinz Ketchup Łagodny",
        "brand": "Heinz",
        "category": "Food Service",
        "subcategory": "Ketchupy",
        "emoji": "🍅",
        "variants": ["875ml Food Service"],
        "base_variant": "875ml Food Service",
        
        # PRICING - FOOD SERVICE MODEL
        "price_foodservice": 28.50,  # Cena dla restauracji/foodtruck
        "price_retail_equivalent": 32.99,  # Gdyby był w retail (dla porównania)
        "margin_foodservice_pct": 35,  # Marża Heinz
        "cost_per_portion": 0.15,  # Koszt porcji 5ml dla restauracji
        
        # DISTRIBUTION MODEL
        "distribution_model": "direct",  # Bezpośrednia sprzedaż do food service
        "available_at": ["Bezpośrednio od Heinz", "Metro Cash & Carry Food Service"],
        "heinz_sku": "HNZ-KCH-875-FS",
        
        # ORDERING
        "moq": 12,  # Minimum 12 butelek (1 karton)
        "payment_terms": "Przelew 30 dni lub gotówka z 2% rabatem",
        "delivery_free_threshold": 500,  # Darmowa dostawa od 500 zł
        
        # LOGISTICS
        "case_size": 12,  # 12 butelek w kartonie
        "cases_per_pallet": 60,
        "shelf_life_days": 540,  # 18 miesięcy
        "packaging": "Butelka plastikowa z flipcap, łatwa do dawkowania",
        "portion_size_ml": 5,
        "portions_per_bottle": 175,
        
        # STORYTELLING
        "description": "Heinz Ketchup Łagodny to klasyczna receptura globalnej marki, z pomidorów zbieranych w słońcu, charakterystycznym aromatem i smakiem rozpoznawalnym od lat. Kultowy smak #1 na świecie.",
        "price_reference_retail": "Około 8,99 zł za 450g w detalu, formaty Food Service znacznie korzystniejsze",
        "target_customer": "Burgerownie, sieciówki QSR, restauracje casual dining, hotele, foodtrucki premium",
        "usage_speed": "Wysoka - restauracja używa 1 butelkę na 3-5 dni (burger joint)",
        "suggested_initial_order": "12 szt (1 karton testowy) - wystarczy na 2 tygodnie w średniej restauracji",
        
        # SALES STORIES FOOD SERVICE
        "sales_stories": [
            "Gdy w menu wpisujesz markę Heinz, komunikujesz klientowi: jakość, globalny standard, pewność smaku. To nie tylko ketchup — to sygnał, że Twój lokal dba o detal.",
            "Formaty HoReCa (np. pojemniki 2,5L) oznaczają niższy koszt porcji – dzięki większej gęstości i niższym stratom.",
            "Heinz jest obecny w burgerowniach, sieciach QSR, stąd Twoi klienci mogą już znać smak — co zmniejsza opór: mniej prób, mniej tłumaczenia.",
            "Choć cena może być nieco wyższa niż lokalnych marek, argumentem jest: mniej potrzeba na porcję, lepsza jakość i stabilność — co przekłada się na mniejszy food-cost i wyższe zadowolenie klienta."
        ],
        
        # PRZEWAGI NAD KONKURENCJĄ
        "competitors": [
            {
                "brand": "Pudliszki Ketchup Łagodny",
                "price_foodservice": 18.50,
                "cost_per_portion": 0.10,
                "market_share_food_service": 45,
                "advantages": [
                    "🏆 Marka premium - klienci znają i lubią Heinz (узнаваемость 94% vs 67% Pudliszki)",
                    "👨‍🍳 Lepszy smak - naturalne pomidory, bez konserwantów (Pudliszki: E211, E202)",
                    "💰 Koszt porcji: tylko 5 gr więcej (0.15 zł vs 0.10 zł), ale wartość dodana!",
                    "📸 Instagram appeal - butelka Heinz na stole = prestiż, klienci robią zdjęcia",
                    "🎯 Premium positioning - jeśli masz burgery za 25 zł, musisz mieć Heinza, nie Pudliszki"
                ]
            },
            {
                "brand": "Kotlin Ketchup",
                "price_foodservice": 16.80,
                "cost_per_portion": 0.09,
                "market_share_food_service": 12,
                "advantages": [
                    "🏆 Brand power - Heinz to synonim ketchupu na świecie (Kotlin: niche brand)",
                    "👨‍🍳 Jakość składników - zero shortcuts, najlepsze pomidory",
                    "💪 Consistency - każda butelka identyczna (Kotlin: zmienność smaku)",
                    "🌍 Globalny standard - serwujesz to co McDonald's, Five Guys, Shake Shack"
                ]
            }
        ],
        
        # ARGUMENTY SPRZEDAŻOWE
        "sales_arguments": [
            "🍔 Jeśli sprzedajesz burgery premium za 25-35 zł, ketchup Heinz to must-have. Klienci oczekują HEINZA przy drogim burgerze - to część doświadczenia premium.",
            "💰 Różnica w koszcie: zaledwie 5 gr na porcję (0.15 zł vs 0.10 zł Pudliszki). Przy burgerze za 28 zł, klient nie zauważy 5 gr różnicy, ale ZAUWAŻY jakość.",
            "📸 Marketing za darmo: klienci robią zdjęcia burgerów z Heinzem i wrzucają na Instagram. Butelka Heinz na stole = signal jakości. To nie działa z Pudliszkami.",
            "🏆 Brand recognition: 94% Polaków zna Heinz, tylko 67% Pudliszki. Heinz to PEWNOŚĆ - klient wie czego się spodziewać.",
            "👨‍🍳 Zero kompromisów: najlepsze pomidory, bez konserwantów (Pudliszki: E211, E202), bez additional sugars. Clean label - co raz ważniejsze dla gości.",
            "💡 試験: weź 12 butelek testowo (500 zł). Postaw przy burgerach przez tydzień i zobacz reakcje gości. Jeśli nie zobaczysz różnicy, wrócimy do Pudliszek. Deal?"
        ],
        
        # OBJECTIONS HANDLING
        "common_objections": {
            "Za drogo": "Rozumiem. Pytanie: czy Twoi goście płacą 15 zł czy 28 zł za burgera? Przy 28 zł dodatkowe 5 gr to 0.2% kosztu. Ale prestiż marki Heinz może zwiększyć postrzeganą wartość o 10-15%. Warto przetestować.",
            "Pudliszki ok": "Pudliszki są OK dla food courtów i budżetówki. Ale Ty robisz coś więcej - craft burgery, jakość. Heinz to część storytellingu: 'używamy najlepszych składników, nawet ketchup'.",
            "Klienci nie zauważą": "Nieprawda. Zrób test: daj 10 osobom Heinza i Pudliszki blind. 8/10 wybierze Heinza. A jak zobaczą butelkę? 10/10 rozpozna Heinza. Brand matters.",
            "Zbyt duże MOQ": "12 butelek to 2100 zł wartości w porcjach (175 x 12 = 2100 porcji x 1 zł markup = 2100 zł przychodu). To się zwróci w 2-3 tygodnie w aktywnej restauracji."
        },
        
        # UPSELL OPPORTUNITIES
        "upsell": {
            "heinz_ketchup_hot": "Masz ostrą wersję? 30% klientów pyta o pikantny ketchup. Heinz Hot to game-changer - możesz podnieść cenę burgera o 2 zł i dać 'premium spicy experience'.",
            "heinz_mustard": "Do kiełbasek i hot-dogów: Heinz Yellow Mustard. Ta sama jakość, ta sama узнаваемość. Postaw Heinz Mustard przy Heinz Ketchup = kompletny premium experience."
        }
    },
    
    "heinz_ketchup_hot": {
        "id": "heinz_ketchup_hot",
        "name": "Heinz Ketchup Pikantny",
        "brand": "Heinz",
        "category": "Food Service",
        "subcategory": "Ketchupy",
        "emoji": "🌶️",
        "variants": ["875ml Food Service"],
        "base_variant": "875ml Food Service",
        
        "price_foodservice": 29.50,
        "margin_foodservice_pct": 35,
        "cost_per_portion": 0.16,
        
        "moq": 12,
        "payment_terms": "Przelew 30 dni lub gotówka z 2% rabatem",
        "delivery_free_threshold": 500,
        
        "description": "Ostra wersja legendarnego Heinz Ketchup. Naturalna ostrość z chili, bez sztucznych dodatków. Perfect match dla burgerów BBQ, frytek i wings.",
        "target_customer": "Burger joints, BBQ restaurants, pub food, foodtrucki z ostrymi daniami",
        
        "sales_arguments": [
            "🌶️ 30% gości pyta 'macie ostry ketchup?' - Heinz Hot to odpowiedź. Możesz podnieść cenę dania o 2 zł za 'spicy upgrade'.",
            "💰 Markup potential: Heinz Hot postrzegany jako premium - możesz sprzedać porcję za 1.50 zł vs 0.50 zł zwykłego ketchupu.",
            "🎯 Menu engineering: postaw 'Spicy Burger with Heinz Hot Ketchup' jako signature dish. Dodatkowo 2-3 zł do ceny = justified premium."
        ]
    },
    
    # ===== PUDLISZKI VALUE LINE (właściciel: Heinz Polska) =====
    "pudliszki_ketchup_lagodny": {
        "id": "pudliszki_ketchup_lagodny",
        "name": "Pudliszki Ketchup Łagodny",
        "brand": "Pudliszki",
        "tier": "value",
        "owner": "Heinz Polska",
        "category": "Food Service",
        "subcategory": "Ketchupy",
        "emoji": "🍅",
        "variants": ["980g Food Service"],
        
        "price_foodservice": 18.50,
        "price_retail_reference": "7,49 zł za 480g (~15,60 zł/kg) lub 11,99 zł za 700g (~17,13 zł/kg) w detalu",
        "margin_foodservice_pct": 32,
        "cost_per_portion": 0.10,
        
        "moq": 12,
        "payment_terms": "Przelew 30 dni",
        
        "description": "Pudliszki Ketchup łagodny to polski klasyk, przygotowany z wysokiej jakości pomidorów, dostępny w różnych wariantach wagowych. Marka dobrze znana konsumentom detalicznym, co może przenosić się na rozpoznawalność w kanale HoReCa.",
        "target_customer": "Stołówki, fast food budget, jadłodajnie, food courts, bary mleczne",
        
        # SALES STORIES FOOD SERVICE
        "sales_stories": [
            "Pudliszki to marka, którą klienci widzą w sklepie — to daje Ci dodatkowy punkt: gdy używasz jej w lokalu, tworzy się poczucie znajomości i komfortu.",
            "Dla lokalu, który nie chce stawiać na ultra-premium, Pudliszki oferuje bardzo dobrą relację jakości do ceny — idealne dla barów, jadłodajni, stołówek.",
            "Możesz podkreślić: 'Polska marka, polskie pomidory, tradycyjny smak' — co w kontrakcie z klientem może być argumentem np. w ofercie lunchowej czy dla klientów rodzinnych.",
            "Jeśli budżet jest napięty, a wolumen spory — wybór Pudliszki może być rozsądnym kompromisem: stabilny smak, dobra dostępność, konkurencyjna cena."
        ],
        
        "sales_arguments": [
            "💰 Najlepsza relacja cena/jakość - 18.50 zł za 980g. Heinz Polska quality w value segmencie.",
            "🇵🇱 Polski lider - 40 lat tradycji, 67% узнаваемость.",
            "📦 Największa pojemność - 980g vs 875ml konkurencja.",
            "🏢 Portfolio Heinz - jeśli klient będzie zadowolony, za rok upgrade do Heinz premium."
        ]
    },
    
    "pudliszki_ketchup_ostry": {
        "id": "pudliszki_ketchup_ostry",
        "name": "Pudliszki Ketchup Ostry",
        "brand": "Pudliszki",
        "tier": "value",
        "owner": "Heinz Polska",
        "category": "Food Service",
        "subcategory": "Ketchupy",
        "emoji": "🌶️",
        "variants": ["980g Food Service"],
        
        "price_foodservice": 18.90,
        "margin_foodservice_pct": 32,
        
        "moq": 12,
        
        "description": "Ostra wersja Pudliszek. Value option dla volume operations.",
        "target_customer": "Kebaby, food trucks budget, fast food chains",
        
        "sales_arguments": [
            "🌶️ Spicy option za value price - 18.90 zł.",
            "💰 Volume play - oszczędności przy wysokich wolumenach."
        ]
    }
}


# Kategorie dla filtrów
CATEGORIES = {
    "Personal Care": "Produkty do pielęgnacji ciała",
    "Food": "Produkty spożywcze",
    "Food Service": "Produkty dla gastronomii",
    "Home Care": "Produkty do czyszczenia",
    "Snacks": "Przekąski",
    "Beverages": "Napoje"
}

SUBCATEGORIES = {
    "Personal Care": ["Żele pod prysznic", "Szampony", "Dezodoranty"],
    "Food": ["Płatki śniadaniowe", "Zupy instant", "Oleje spożywcze"],
    "Food Service": ["Ketchupy", "Musztardy", "Sosy"],
    "Home Care": ["Płyny do mycia podłóg", "Płyny do naczyń", "Odświeżacze powietrza"],
    "Snacks": ["Chipsy", "Orzechy i bakalie"],
    "Beverages": ["Herbaty mrożone"]
}

