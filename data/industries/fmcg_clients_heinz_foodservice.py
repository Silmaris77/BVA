"""
Baza klientów Food Service dla scenariusza Heinz
Baza gracza: Lipowa 29, 43-445 Dzięgielów (49.7271667°N, 18.7025833°E)
Region: Dzięgielów + okolice (Wisła, Ustroń, Skoczów, Cieszyn), promień 30km
25 punktów gastronomicznych
"""

HEINZ_FOODSERVICE_CLIENTS = {
    # ========== BURGEROWNIE / STREET FOOD (6 klientów) ==========
    "client_001": {
        "id": "client_001",
        "name": "Burger Station",
        "type": "burger_joint",
        "owner": "Marek Kowalski",
        "personality": "ISTJ",  # Tradycjonalista, ostrożny
        "address": "Rynek 1, 43-460 Wisła",
        "latitude": 49.6547,
        "longitude": 18.8615,
        "distance_from_base": 15.2,
        
        "segment": "premium",
        "avg_burger_price": 28,
        "monthly_volume_kg": 15,
        "current_supplier": "Kotlin",
        "current_product": "Kotlin Ketchup 900g",
        "pain_points": ["Zmienność smaku Kotlin", "Goście pytają o Heinz"],
        
        "motivators": ["Smak", "Prestiż", "Instagram appeal"],
        "price_sensitivity": "medium",
        "decision_maker": "owner_chef",
        
        "objections": [
            "Heinz jest za drogi, klienci i tak nie widzą różnicy",
            "Kotlin daje mi rabaty i karty podarunkowe"
        ],
        
        "recommended_strategy": "Kompensacja + Test bez zobowiązań",
        "recommended_products": ["heinz_ketchup_classic", "heinz_ketchup_hot"],
        "upsell_potential": "high"
    },
    
    "client_002": {
        "id": "client_002",
        "name": "Street Burger",
        "type": "food_truck",
        "owner": "Anna Wiśniewska",
        "personality": "ENFP",  # Entuzjastka, otwarta na nowości
        "address": "Plac Hoffa, 43-430 Skoczów",
        "latitude": 49.7783,
        "longitude": 18.7894,
        "distance_from_base": 7.8,
        
        "segment": "premium",
        "avg_burger_price": 25,
        "monthly_volume_kg": 12,
        "current_supplier": "Pudliszki (od dystrybutora)",
        "current_product": "Pudliszki Łagodny 980g",
        "pain_points": ["Chce się wyróżnić", "Brand matters dla foodtruck"],
        
        "motivators": ["Instagram", "Wyróżnienie się", "Jakość"],
        "price_sensitivity": "low",
        "decision_maker": "owner_chef",
        
        "objections": [
            "Używam lokalnych sosów, żeby się wyróżnić"
        ],
        
        "recommended_strategy": "Perspektywizacja + Heinz jako część storytellingu",
        "recommended_products": ["heinz_ketchup_classic"],
        "upsell_potential": "very_high"  # Gotowa na upgrade z Pudliszek
    },
    
    "client_003": {
        "id": "client_003",
        "name": "Grill House Premium",
        "type": "burger_joint",
        "owner": "Tomasz Nowak",
        "personality": "ENTJ",  # Biznesmen, liczy ROI
        "address": "Sanatoryjna 7, 43-450 Ustroń",
        "latitude": 49.7167,
        "longitude": 18.8278,
        "distance_from_base": 11.3,
        
        "segment": "premium",
        "avg_burger_price": 32,
        "monthly_volume_kg": 20,
        "current_supplier": "Heinz (już ma!)",
        "current_product": "Heinz Klasyczny 875ml",
        "pain_points": ["Chce pikantną wersję", "Volume discount"],
        
        "motivators": ["ROI", "Marża", "Menu engineering"],
        "price_sensitivity": "low",
        "decision_maker": "owner",
        
        "objections": [],  # Już klient Heinz!
        
        "recommended_strategy": "Upsell Heinz Hot + Volume deal",
        "recommended_products": ["heinz_ketchup_hot"],
        "upsell_potential": "guaranteed"
    },
    
    "client_004": {
        "id": "client_004",
        "name": "Burger Craft",
        "type": "burger_joint",
        "owner": "Piotr Zieliński",
        "personality": "ISTP",  # Praktyk, testuje zanim kupi
        "address": "Zamkowa 4, 43-460 Wisła",
        "latitude": 49.6528,
        "longitude": 18.8572,
        "distance_from_base": 14.8,
        
        "segment": "mixed",
        "avg_burger_price": 22,
        "monthly_volume_kg": 18,
        "current_supplier": "Mix (Pudliszki + Kotlin)",
        "current_product": "Pudliszki dla volume, Kotlin jako backup",
        "pain_points": ["Niespójna jakość", "Chce uprościć logistykę"],
        
        "motivators": ["Prostota", "Jedna marka", "Stabilność"],
        "price_sensitivity": "medium",
        "decision_maker": "owner_chef",
        
        "objections": [
            "Nie chcę się wiązać z jednym dostawcą",
            "Fanex daje mi karty Sodexo i fartuchy"
        ],
        
        "recommended_strategy": "Powrót do potrzeb + Portfolio Heinz (Pudliszki value + Heinz premium)",
        "recommended_products": ["pudliszki_ketchup_lagodny", "heinz_ketchup_classic"],
        "upsell_potential": "medium"
    },
    
    "client_005": {
        "id": "client_005",
        "name": "Hot Dog Heaven",
        "type": "street_food",
        "owner": "Karolina Lewandowska",
        "personality": "ESFJ",  # Społeczna, lubi rekomendacje
        "address": "Beskidzka 18, 43-430 Skoczów",
        "latitude": 49.7812,
        "longitude": 18.7952,
        "distance_from_base": 7.5,
        
        "segment": "value",
        "avg_product_price": 12,
        "monthly_volume_kg": 10,
        "current_supplier": "Kotlin",
        "current_product": "Kotlin 900g",
        "pain_points": ["Niska узнаваемость Kotlin", "Goście pytają o mustard"],
        
        "motivators": ["Prostota", "Znana marka", "Cross-sell"],
        "price_sensitivity": "high",
        "decision_maker": "owner",
        
        "objections": [
            "Ketchup musi być tani, bo klient nie patrzy na markę"
        ],
        
        "recommended_strategy": "FOZ + Pudliszki jako lepszy value vs Kotlin",
        "recommended_products": ["pudliszki_ketchup_lagodny"],
        "upsell_potential": "low"
    },
    
    "client_006": {
        "id": "client_006",
        "name": "Food Truck Smakosze",
        "type": "food_truck",
        "owner": "Michał Krawczyk",
        "personality": "ESTP",  # Spontaniczny, szybkie decyzje
        "address": "Parking Aqua Park, 43-460 Wisła",
        "latitude": 49.6603,
        "longitude": 18.8654,
        "distance_from_base": 14.2,
        
        "segment": "mixed",
        "avg_product_price": 18,
        "monthly_volume_kg": 8,
        "current_supplier": "Brak stałego",
        "current_product": "Kupuje w Cash&Carry co tydzień",
        "pain_points": ["Chaos logistyczny", "Różne ceny co tydzień"],
        
        "motivators": ["Stabilność", "Prostota zamówień", "Czas"],
        "price_sensitivity": "medium",
        "decision_maker": "owner",
        
        "objections": [
            "Nie mam czasu testować",
            "Cash&Carry wygodniejsze"
        ],
        
        "recommended_strategy": "Logistyka + Regularne dostawy",
        "recommended_products": ["pudliszki_ketchup_lagodny"],
        "upsell_potential": "medium"
    },
    
    # ========== KEBABOWNIE / FAST FOOD ETNICZNY (4 klientów) ==========
    "client_007": {
        "id": "client_007",
        "name": "Kebab King",
        "type": "kebab",
        "owner": "Ahmed Ali",
        "personality": "ISTJ",  # Tradycyjny, cena priorytet
        "address": "3 Maja 12, 43-400 Cieszyn",
        "latitude": 49.7493,
        "longitude": 18.6345,
        "distance_from_base": 9.8,
        
        "segment": "value",
        "avg_product_price": 15,
        "monthly_volume_kg": 35,
        "current_supplier": "Kotlin",
        "current_product": "Kotlin 5L wiaderko",
        "pain_points": ["Foodcost 29% (max 27%)", "Volume wysoki"],
        
        "motivators": ["Cena porcji", "Wolumen", "Prostota"],
        "price_sensitivity": "very_high",
        "decision_maker": "owner",
        
        "objections": [
            "Ketchup musi być tani, bo klient nie patrzy na markę",
            "Nie chcę się wiązać, dystrybutor i tak dowozi taniej"
        ],
        
        "recommended_strategy": "FOZ + Promocja 4+1 Pudliszki",
        "recommended_products": ["pudliszki_ketchup_lagodny"],
        "upsell_potential": "low"
    },
    
    "client_008": {
        "id": "client_008",
        "name": "Doner House",
        "type": "kebab",
        "owner": "Kamil Osman",
        "personality": "ENTP",  # Przedsiębiorczy, szuka okazji
        "address": "Głęboka 8, 43-400 Cieszyn",
        "latitude": 49.7456,
        "longitude": 18.6389,
        "distance_from_base": 9.2,
        
        "segment": "value",
        "avg_product_price": 16,
        "monthly_volume_kg": 28,
        "current_supplier": "Dystrybutor lokalny",
        "current_product": "No-name 10kg wiadro",
        "pain_points": ["Jakość niestabilna", "Reklamacje gości"],
        
        "motivators": ["Stabilność", "Mniej reklamacji", "Brand"],
        "price_sensitivity": "high",
        "decision_maker": "owner",
        
        "objections": [
            "Nie mam czasu testować"
        ],
        
        "recommended_strategy": "Sampling + Pudliszki jako upgrade z no-name",
        "recommended_products": ["pudliszki_ketchup_ostry"],
        "upsell_potential": "medium"
    },
    
    "client_009": {
        "id": "client_009",
        "name": "Kebab Express",
        "type": "fast_food_ethnic",
        "owner": "Selim Yilmaz",
        "personality": "ISFJ",  # Lojalny, ceni relacje
        "address": "Dworcowa 1, 43-450 Ustroń",
        "latitude": 49.7142,
        "longitude": 18.8187,
        "distance_from_base": 9.8,
        
        "segment": "value",
        "avg_product_price": 14,
        "monthly_volume_kg": 40,
        "current_supplier": "Kotlin (przez dystrybutora)",
        "current_product": "Kotlin 5L",
        "pain_points": ["Dystrybutor czasem nie ma stanów", "Delivery delays"],
        
        "motivators": ["Pewność dostaw", "Relacja z PH", "Stabilność cen"],
        "price_sensitivity": "very_high",
        "decision_maker": "owner",
        
        "objections": [
            "Dostawca ma tylko trzy Wasze produkty"
        ],
        
        "recommended_strategy": "Powrót do potrzeb + Bezpośrednia dostawa",
        "recommended_products": ["pudliszki_ketchup_lagodny", "pudliszki_ketchup_ostry"],
        "upsell_potential": "medium"
    },
    
    "client_010": {
        "id": "client_010",
        "name": "Falafel & More",
        "type": "fast_food_ethnic",
        "owner": "Sara Khalil",
        "personality": "ENFJ",  # Wizjonerka, brand conscious
        "address": "Mennicza 5, 43-400 Cieszyn",
        "latitude": 49.7512,
        "longitude": 18.6312,
        "distance_from_base": 10.3,
        "distance_from_base": 0.85,
        
        "segment": "mixed",
        "avg_product_price": 20,
        "monthly_volume_kg": 12,
        "current_supplier": "Brak (kupuje retail Heinz w Żabce!)",
        "current_product": "Heinz 500ml z Żabki",
        "pain_points": ["Za drogo kupować retail", "Chce foodservice pricing"],
        
        "motivators": ["Brand Heinz", "Margin improvement", "Profesjonalizacja"],
        "price_sensitivity": "low",
        "decision_maker": "owner",
        
        "objections": [],  # Już przekonana do Heinza!
        
        "recommended_strategy": "Easy win - foodservice switch z retail",
        "recommended_products": ["heinz_ketchup_classic"],
        "upsell_potential": "very_high"
    },
    
    # ========== BARY MLECZNE / STOŁÓWKI (3 klientów) ==========
    "client_011": {
        "id": "client_011",
        "name": "Bar Mleczny Smaczek",
        "type": "bar_mleczny",
        "owner": "Janina Kowalczyk",
        "personality": "ISTJ",  # Konserwatywna, tylko cena
        "address": "Kościelna 22, 43-430 Skoczów",
        "latitude": 49.7795,
        "longitude": 18.7928,
        "distance_from_base": 7.2,
        
        "segment": "value",
        "avg_meal_price": 12,
        "monthly_volume_kg": 45,
        "current_supplier": "Dystrybutor publiczny",
        "current_product": "No-name 10kg wiadro (najtańszy)",
        "pain_points": ["Budget sztywny", "Przetargi publiczne"],
        
        "motivators": ["Cena", "Tylko cena", "Logistyka"],
        "price_sensitivity": "extreme",
        "decision_maker": "kierownik_zaopatrzenia",
        
        "objections": [
            "Heinz jest zbyt drogi",
            "Liczy się tylko cena i dostępność",
            "Nie mamy gdzie tego trzymać"
        ],
        
        "recommended_strategy": "FOZ + Wydajność (mniej strat, czystsze talerze)",
        "recommended_products": ["pudliszki_ketchup_lagodny"],
        "upsell_potential": "very_low"
    },
    
    "client_012": {
        "id": "client_012",
        "name": "Stołówka Szkolna - Gimnazjum",
        "type": "canteen_school",
        "owner": "Dyrektor Maria Wójcik",
        "personality": "ESFJ",  # Troskliwa, jakość dla dzieci
        "address": "Szkolna 5, 43-460 Wisła",
        "latitude": 49.6582,
        "longitude": 18.8698,
        "distance_from_base": 13.8,
        
        "segment": "value",
        "avg_meal_price": 8,
        "monthly_volume_kg": 30,
        "current_supplier": "Przetarg (Kotlin wygrywa)",
        "current_product": "Kotlin 10kg",
        "pain_points": ["Rodzice pytają o jakość", "Chce lepszego image"],
        
        "motivators": ["Jakość dla dzieci", "Mniej chemii", "Image"],
        "price_sensitivity": "very_high",
        "decision_maker": "dyrektor_plus_przetarg",
        
        "objections": [
            "Dostawca ma tylko trzy Wasze produkty",
            "Procedury przetargowe"
        ],
        
        "recommended_strategy": "Perspektywizacja + Pudliszki jako kompromis (Polski, мniej chemii vs no-name)",
        "recommended_products": ["pudliszki_ketchup_lagodny"],
        "upsell_potential": "low"
    },
    
    "client_013": {
        "id": "client_013",
        "name": "Stołówka Zakładowa - Fabryka Mebli",
        "type": "canteen_corporate",
        "owner": "Kierownik Anna Baran",
        "personality": "INTJ",  # Analityk, data-driven
        "address": "Przemysłowa 10, 43-450 Ustroń",
        "latitude": 49.7128,
        "longitude": 18.8234,
        "distance_from_base": 9.2,
        
        "segment": "value",
        "avg_meal_price": 10,
        "monthly_volume_kg": 50,
        "current_supplier": "Kotlin (kontrakt roczny)",
        "current_product": "Kotlin 10kg wiaderka",
        "pain_points": ["Kontrakt wygasa za 3 miesiące", "Szuka oszczędności"],
        
        "motivators": ["Wydajność", "Mniej marnotrawstwa", "Stabilność cen"],
        "price_sensitivity": "very_high",
        "decision_maker": "procurement_manager",
        
        "objections": [
            "Heinz jest zbyt drogi",
            "Nie mam gdzie tego trzymać"
        ],
        
        "recommended_strategy": "Powrót do potrzeb + ROI (wydajność zmniejsza koszty overall)",
        "recommended_products": ["pudliszki_ketchup_lagodny"],
        "upsell_potential": "medium"  # Jeśli ROI przekona
    },
    
    # ========== PIZZERIE / CASUAL DINING (4 klientów) ==========
    "client_014": {
        "id": "client_014",
        "name": "Pizzeria Da Vinci",
        "type": "pizzeria",
        "owner": "Giovanni Rossi",
        "personality": "ISFP",  # Artysta, tradycja
        "address": "Rynek 10, Dzięgielów",
        "latitude": 49.9378,
        "latitude": 49.7523,
        "longitude": 18.6298,
        "distance_from_base": 10.5,
        
        "segment": "premium",
        "avg_pizza_price": 32,
        "monthly_volume_kg": 8,
        "current_supplier": "Włoski dystrybutor (specjalistyczny)",
        "current_product": "Włoski ketchup Mutti",
        "pain_points": ["Ketchup nie jest priorytetem", "Używają мало"],
        
        "motivators": ["Jakość", "Włoski origin (ale Heinz też ok)", "Prostota"],
        "price_sensitivity": "low",
        "decision_maker": "owner_chef",
        
        "objections": [
            "Mamy własną markę sosów, Heinz byłby konkurencją"
        ],
        
        "recommended_strategy": "Nie walcz - Heinz jako backup/side option",
        "recommended_products": ["heinz_ketchup_classic"],
        "upsell_potential": "low"
    },
    
    "client_015": {
        "id": "client_015",
        "name": "Pizza House - Sieć 3 lokale",
        "type": "pizza_chain",
        "owner": "Prezes Andrzej Kubiak",
        "personality": "ESTJ",  # Manager, standaryzacja
        "address": "Beskidzka 45, 43-430 Skoczów",
        "latitude": 49.7768,
        "longitude": 18.7886,
        "distance_from_base": 6.8,
        
        "segment": "mixed",
        "avg_pizza_price": 28,
        "monthly_volume_kg": 25,  # Suma z 3 lokali
        "current_supplier": "Kotlin (centralne zakupy)",
        "current_product": "Kotlin 5L wiaderka",
        "pain_points": ["Niespójna jakość między lokalami", "Chce standardów"],
        
        "motivators": ["Standaryzacja", "Każda porcja taka sama", "Centralizacja"],
        "price_sensitivity": "medium",
        "decision_maker": "centralne_zakupy",
        
        "objections": [
            "Ketchup z butli 5L nie pasuje do naszego systemu",
            "Nie widzę różnicy dla klienta"
        ],
        
        "recommended_strategy": "Powrót do potrzeb + Heinz jako standard (jedna porcja = ta sama jakość w 3 lokalach)",
        "recommended_products": ["heinz_ketchup_classic"],
        "upsell_potential": "high"  # Decyzja strategiczna = cała sieć
    },
    
    "client_016": {
        "id": "client_016",
        "name": "Trattoria Bella Vista",
        "type": "casual_dining",
        "owner": "Paweł Mazur",
        "personality": "ENFP",  # Kreatywny, lubi eksperymenty
        "address": "Widokowa 2, 43-460 Wisła",
        "latitude": 49.6615,
        "longitude": 18.8623,
        "distance_from_base": 13.5,
        
        "segment": "premium",
        "avg_meal_price": 45,
        "monthly_volume_kg": 5,
        "current_supplier": "Brak (używa własnych sosów)",
        "current_product": "Robi własne sosy pomidorowe",
        "pain_points": ["Czasochłonne", "Chce uprościć kuchnię"],
        
        "motivators": ["Czas", "Jakość stabilna", "Mniej pracy"],
        "price_sensitivity": "very_low",
        "decision_maker": "owner_chef",
        
        "objections": [
            "Nie chcemy tego samego, co sieciówki"
        ],
        
        "recommended_strategy": "Perspektywizacja + Heinz jako premium (używany przez fine dining globally)",
        "recommended_products": ["heinz_ketchup_classic"],
        "upsell_potential": "medium"
    },
    
    "client_017": {
        "id": "client_017",
        "name": "Restauracja Pod Świerkami",
        "type": "casual_dining",
        "owner": "Małgorzata Sikora",
        "personality": "INFJ",  # Idealistka, misja
        "address": "Leśna 15, 43-450 Ustroń",
        "latitude": 49.7153,
        "longitude": 18.8201,
        "distance_from_base": 9.5,
        
        "segment": "premium",
        "avg_meal_price": 38,
        "monthly_volume_kg": 6,
        "current_supplier": "Pudliszki (przez Metro)",
        "current_product": "Pudliszki 980g",
        "pain_points": ["Chce premium image", "Goście oczekują lepszego"],
        
        "motivators": ["Image", "Prestiż", "Brand storytelling"],
        "price_sensitivity": "low",
        "decision_maker": "owner",
        
        "objections": [],  # Gotowa na upgrade!
        
        "recommended_strategy": "Easy upsell z Pudliszek do Heinz",
        "recommended_products": ["heinz_ketchup_classic"],
        "upsell_potential": "very_high"
    },
    
    # ========== HOTELE (2 klientów) ==========
    "client_018": {
        "id": "client_018",
        "name": "Hotel Beskidy ***",
        "type": "hotel_3star",
        "owner": "F&B Manager Jacek Czapla",
        "personality": "ISTJ",  # Procedury, bezpieczeństwo
        "address": "Hotelowa 8, 43-460 Wisła",
        "latitude": 49.6591,
        "longitude": 18.8710,
        "distance_from_base": 13.2,
        
        "segment": "premium",
        "avg_breakfast_price": 35,
        "monthly_volume_kg": 10,
        "current_supplier": "Metro C&C",
        "current_product": "Mix produktów (co akurat jest)",
        "pain_points": ["Niespójność dostaw", "Goście pytają o ketchup przy śniadaniach"],
        
        "motivators": ["Stabilność dostaw", "Prestiż", "Terminowość"],
        "price_sensitivity": "low",
        "decision_maker": "fb_manager",
        
        "objections": [
            "Heinz to marka marketowa",
            "Za drogo jak na kuchnię hotelową"
        ],
        
        "recommended_strategy": "Perspektywizacja + Kompensacja (Heinz = globalny standard hotelowy)",
        "recommended_products": ["heinz_ketchup_classic"],
        "upsell_potential": "high"
    },
    
    "client_019": {
        "id": "client_019",
        "name": "Wellness Hotel SPA ****",
        "type": "hotel_4star",
        "owner": "Dyrektor F&B Katarzyna Wojciechowska",
        "personality": "ENTJ",  # Lider, wymagająca
        "address": "Parkowa 1, 43-450 Ustroń",
        "latitude": 49.7176,
        "longitude": 18.8165,
        "distance_from_base": 10.2,
        
        "segment": "premium",
        "avg_meal_price": 60,
        "monthly_volume_kg": 15,
        "current_supplier": "Heinz (już klient!)",
        "current_product": "Heinz Klasyczny 875ml",
        "pain_points": ["Chce volume pricing", "Pytają o mustard i mayo"],
        
        "motivators": ["Brand consistency", "Portfolio expansion", "Volume discount"],
        "price_sensitivity": "very_low",
        "decision_maker": "fb_director",
        
        "objections": [],  # Już lojalni!
        
        "recommended_strategy": "Portfolio sell + Volume deal",
        "recommended_products": ["heinz_ketchup_hot"],  # Cross-sell
        "upsell_potential": "guaranteed"
    },
    
    # ========== DYSTRYBUTORZY / HURT (6 klientów) ==========
    "client_020": {
        "id": "client_020",
        "name": "HoReCa Dystrybucja Śląsk",
        "type": "distributor",
        "owner": "Handlowiec Paweł Lis",
        "personality": "ESTP",  # Sprzedawca, transakcyjny
        "address": "Lipowa 42, 43-445 Dzięgielów",
        "latitude": 49.7245,
        "longitude": 18.7098,
        "distance_from_base": 0.8,
        
        "segment": "distributor",
        "monthly_volume_kg": 120,  # Obsługuje 15 lokali
        "current_portfolio": "Mix (Kotlin, Develey, trochę Pudliszki)",
        "current_heinz_products": "Brak",
        "pain_points": ["Niska marża na ketchupach", "Klienci pytają o Heinz"],
        
        "motivators": ["Marża", "Rotacja", "Popyt klientów"],
        "price_sensitivity": "medium",
        "decision_maker": "sales_manager",
        
        "objections": [
            "Na Heinz mam mniejszą marżę",
            "Cash&Carry i tak sprzedaje Heinz, po co mi to w ofercie?",
            "Konkurencja daje mi gadżety i premie"
        ],
        
        "recommended_strategy": "Powrót do potrzeb + Program wsparcia sprzedaży (promocje 4+1)",
        "recommended_products": ["heinz_ketchup_classic", "heinz_ketchup_hot", "pudliszki_ketchup_lagodny"],
        "upsell_potential": "very_high"  # Klucz do 15 lokali!
    },
    
    "client_021": {
        "id": "client_021",
        "name": "FoodService Plus",
        "type": "distributor",
        "owner": "Właściciel Robert Dąbrowski",
        "personality": "ISTJ",  # Tradycjonalista, relacje długoterminowe
        "address": "Handlowa 12, 43-450 Ustroń",
        "latitude": 49.7161,
        "longitude": 18.8223,
        "distance_from_base": 9.3,
        
        "segment": "distributor",
        "monthly_volume_kg": 180,  # Duży gracz, 25+ lokali
        "current_portfolio": "Kotlin (główny), Pudliszki (mały udział)",
        "current_heinz_products": "Heinz - tylko na zamówienie",
        "pain_points": ["Kotlin niestabilny quality", "Chce premium option"],
        
        "motivators": ["Długoterminowa relacja", "Wsparcie marketingowe", "Stabilność"],
        "price_sensitivity": "low",
        "decision_maker": "owner",
        
        "objections": [
            "Nie macie wszystkiego na stanie"
        ],
        
        "recommended_strategy": "Lista zastrzeżeń + Partnership approach",
        "recommended_products": ["heinz_ketchup_classic", "pudliszki_ketchup_lagodny"],
        "upsell_potential": "very_high"  # Strategic partner potential
    },
    
    "client_022": {
        "id": "client_022",
        "name": "Gastro Hurt Beskidy",
        "type": "distributor_small",
        "owner": "Pani Zofia Król",
        "personality": "ISFJ",  # Pomocna, konserwatywna
        "address": "Składowa 3, 43-460 Wisła",
        "latitude": 49.6568,
        "longitude": 18.8642,
        "distance_from_base": 13.7,
        
        "segment": "distributor",
        "monthly_volume_kg": 60,  # Mały dystrybutor, 8 lokali
        "current_portfolio": "Bardzo szeroki (wszystko po trochu)",
        "current_heinz_products": "Pudliszki (dobra rotacja)",
        "pain_points": ["Chce uprościć portfolio", "Za dużo SKU"],
        
        "motivators": ["Prostota", "Focus", "Mniej SKU = lepsza rotacja"],
        "price_sensitivity": "medium",
        "decision_maker": "owner",
        
        "objections": [
            "Nie mam miejsca w magazynie na kolejne produkty"
        ],
        
        "recommended_strategy": "Powrót do potrzeb + Heinz + Pudliszki = kompletne portfolio w 4 SKU",
        "recommended_products": ["heinz_ketchup_classic", "pudliszki_ketchup_lagodny"],
        "upsell_potential": "medium"
    },
    
    "client_023": {
        "id": "client_023",
        "name": "Metro Cash & Carry - Oddział Bielsko",
        "type": "cash_and_carry",
        "owner": "Category Manager Tomasz Wilk",
        "personality": "INTJ",  # Analityk, data-driven
        "address": "Obwodowa 50, 43-300 Bielsko-Biała",
        "latitude": 49.8224,
        "longitude": 19.0447,
        "distance_from_base": 25.8,
        
        "segment": "distributor",
        "monthly_volume_kg": 300,  # Mega wolumen
        "current_portfolio": "Pełna linia Heinz + Pudliszki + konkurencja",
        "current_heinz_products": "Wszystkie",
        "pain_points": ["Chce lepsze warunki volume", "Promocje dla klientów końcowych"],
        
        "motivators": ["Rotacja", "Margin", "Promocje"],
        "price_sensitivity": "low",
        "decision_maker": "category_manager",
        
        "objections": [],  # Już partner strategiczny
        
        "recommended_strategy": "Partnership deepening + Joint promotions",
        "recommended_products": ["heinz_ketchup_hot"],  # Nowe SKU
        "upsell_potential": "guaranteed"
    },
    
    "client_024": {
        "id": "client_024",
        "name": "Selgros Cash & Carry",
        "type": "cash_and_carry",
        "owner": "Buyer Monika Szymańska",
        "personality": "ESTJ",  # Manager, KPI-driven
        "address": "Katowicka 88, 43-300 Bielsko-Biała",
        "latitude": 49.8178,
        "longitude": 19.0523,
        "distance_from_base": 26.2,
        
        "segment": "distributor",
        "monthly_volume_kg": 250,
        "current_portfolio": "Kotlin (main), Pudliszki (secondary)",
        "current_heinz_products": "Brak Heinza!",
        "pain_points": ["Klienci pytają o Heinz", "Kotlin spadek sprzedaży"],
        
        "motivators": ["Sales volume", "Customer demand", "Listing fees?"],
        "price_sensitivity": "medium",
        "decision_maker": "buyer_plus_category",
        
        "objections": [
            "Potrzebujemy listing fee",
            "Heinz już jest w Metro, po co nam?"
        ],
        
        "recommended_strategy": "Customer demand + Exclusive regional promo",
        "recommended_products": ["heinz_ketchup_classic", "heinz_ketchup_hot"],
        "upsell_potential": "high"  # Strategic win vs Metro
    },
    
    "client_025": {
        "id": "client_025",
        "name": "FoodPartner - Mały Hurt Lokalny",
        "type": "distributor_small",
        "owner": "Pan Jerzy Mazurek",
        "personality": "ESFP",  # Towarzyski, lubi ludzi
        "address": "Słoneczna 7, 43-445 Dzięgielów",
        "latitude": 49.7298,
        "longitude": 18.7112,
        "distance_from_base": 0.5,
        
        "segment": "distributor",
        "monthly_volume_kg": 45,  # Bardzo mały, 5 stałych klientów
        "current_portfolio": "Kotlin + trochę Pudliszek",
        "current_heinz_products": "Brak",
        "pain_points": ["Chce się wyróżnić", "Konkurencja z Metro/Selgros"],
        
        "motivators": ["Unique selling point", "Relacje z klientami", "Wyróżnienie"],
        "price_sensitivity": "medium",
        "decision_maker": "owner",
        
        "objections": [
            "Za mały jestem na Heinz",
            "Konkurencja daje lepsze ceny"
        ],
        
        "recommended_strategy": "Bumerang + Heinz jako USP (obsługujesz premium klientów, których Metro nie ma czasu)",
        "recommended_products": ["heinz_ketchup_classic", "pudliszki_ketchup_lagodny"],
        "upsell_potential": "medium"
    }
}


# Statystyki klientów dla dashboardu
def get_client_stats():
    """Zwraca statystyki klientów dla dashboard"""
    total = len(HEINZ_FOODSERVICE_CLIENTS)
    
    by_type = {}
    by_segment = {}
    by_current_supplier = {}
    total_potential_volume = 0
    
    for client in HEINZ_FOODSERVICE_CLIENTS.values():
        # By type
        client_type = client["type"]
        by_type[client_type] = by_type.get(client_type, 0) + 1
        
        # By segment
        segment = client["segment"]
        by_segment[segment] = by_segment.get(segment, 0) + 1
        
        # By current supplier
        supplier = client.get("current_supplier", "Brak")
        by_current_supplier[supplier] = by_current_supplier.get(supplier, 0) + 1
        
        # Total volume
        total_potential_volume += client.get("monthly_volume_kg", 0)
    
    return {
        "total_clients": total,
        "by_type": by_type,
        "by_segment": by_segment,
        "by_current_supplier": by_current_supplier,
        "total_potential_volume_kg": total_potential_volume,
        "avg_volume_per_client": total_potential_volume / total if total > 0 else 0
    }


def get_clients_by_segment(segment):
    """Zwraca listę klientów z danego segmentu"""
    return [c for c in HEINZ_FOODSERVICE_CLIENTS.values() if c.get("segment") == segment]


def get_clients_by_supplier(supplier):
    """Zwraca listę klientów z danym dostawcą"""
    return [c for c in HEINZ_FOODSERVICE_CLIENTS.values() if c.get("current_supplier") == supplier]


def get_high_potential_clients(min_volume=15):
    """Zwraca klientów z wysokim potencjałem (volume)"""
    return [c for c in HEINZ_FOODSERVICE_CLIENTS.values() 
            if c.get("monthly_volume_kg", 0) >= min_volume]


def get_easy_wins():
    """Zwraca klientów z wysokim potencjałem konwersji (very_high, guaranteed)"""
    return [c for c in HEINZ_FOODSERVICE_CLIENTS.values() 
            if c.get("upsell_potential") in ["very_high", "guaranteed"]]


# ============================================================================
# USAGE DOCUMENTATION
# ============================================================================
"""
JAK UŻYWAĆ TEJ BAZY KLIENTÓW W GRE:

1. ŁADOWANIE KLIENTÓW DO SCENARIUSZA:
   from data.industries.fmcg_clients_heinz_foodservice import HEINZ_FOODSERVICE_CLIENTS
   
2. INICJALIZACJA GRY (gdy gracz wybiera Heinz Food Service scenario):
   clients = HEINZ_FOODSERVICE_CLIENTS.copy()
   st.session_state.fmcg_clients = clients
   st.session_state.visited_clients = []
   st.session_state.active_clients = []
   
3. WYŚWIETLANIE LISTY KLIENTÓW DO ODWIEDZIN:
   for client_id, client in clients.items():
       st.write(f"{client['name']} - {client['type']}")
       st.write(f"📍 {client['address']} ({client['distance_from_base']} km)")
       st.write(f"💰 Potencjał: {client['monthly_volume_kg']} kg/mies.")
       
4. ROZPOCZĘCIE ROZMOWY Z KLIENTEM:
   selected_client = clients[client_id]
   st.session_state.current_client = selected_client
   st.session_state.current_personality = selected_client['personality']
   st.session_state.current_objections = selected_client['objections']
   
5. AI CONVERSATION CONTEXT:
   context = f\"\"\"
   Klient: {client['name']}, prowadzi {client['type']}
   Osobowość: {client['personality']}
   Pain points: {', '.join(client['pain_points'])}
   Obecnie używa: {client['current_product']} od {client['current_supplier']}
   Motywatory: {', '.join(client['motivators'])}
   
   Rekomendowane produkty: {', '.join(client['recommended_products'])}
   Strategia: {client['recommended_strategy']}
   \"\"\"
   
6. TRACKING SPRZEDAŻY:
   if sale_successful:
       client['status'] = 'active'
       client['products_ordered'] = ['heinz_ketchup_classic']
       client['monthly_value'] = client['monthly_volume_kg'] * 28.50
       st.session_state.active_clients.append(client_id)
       
7. PORTFOLIO MANAGEMENT KPI:
   heinz_revenue = sum(c['heinz_sales'] for c in active_clients)
   pudliszki_revenue = sum(c['pudliszki_sales'] for c in active_clients)
   premium_mix = heinz_revenue / (heinz_revenue + pudliszki_revenue) * 100
   
8. UPSELL TRACKING:
   clients_with_pudliszki = [c for c in active if 'pudliszki' in c['products']]
   upsold = [c for c in clients_with_pudliszki if 'heinz' in c['products']]
   upsell_rate = len(upsold) / len(clients_with_pudliszki) * 100

PRZYKŁADOWE SCENARIUSZE UŻYCIA:

A) EASY WINS - Start od klientów gotowych na konwersję:
   easy_wins = get_easy_wins()
   # client_003 (Grill House - już ma Heinz, chce Hot)
   # client_010 (Falafel - kupuje retail, chce foodservice pricing)
   # client_017 (Pod Świerkami - ma Pudliszki, chce upgrade)
   
B) COMPETITIVE WINS - Przejmowanie z Kotlin:
   kotlin_clients = get_clients_by_supplier("Kotlin")
   # 8 klientów do przejęcia (objective: beat_kotlin = 6)
   
C) PORTFOLIO PLAY - Sprzedaż obu marek:
   mixed_segment = get_clients_by_segment("mixed")
   # 7 klientów, którzy mogą kupić Heinz + Pudliszki
   
D) STRATEGIC ACCOUNTS - Dystrybutorzy (klucze do całego rynku):
   distributors = [c for c in clients.values() if 'distributor' in c['type']]
   # 6 dystrybutorów = dostęp do 100+ lokali pośrednio

SALES TECHNIQUES MAPPING:

- FOZ (Fakty-Odniesienie-Zapytanie): kebabownie, stołówki (price sensitive)
- Kompensacja: burgerownie premium (justify higher price)
- Perspektywizacja: hotele, casual dining (reframe premium)
- Powrót do potrzeb: dystrybutorzy (long-term partnership)
- Bumerang: objection flip (np. "za drogi" → "właśnie dlatego...")
- Lista zastrzeżeń: duzi dystrybutorzy (complex sales)
"""
