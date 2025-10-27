"""
Baza klientów FMCG - Traditional Trade
Sklepy osiedlowe, kioski, małe sieci lokalne
"""

# Segmenty rynku
MARKET_SEGMENTS = {
    "traditional_trade": {
        "name": "Traditional Trade",
        "description": "Sklepy osiedlowe, kioski, małe lokalne sieci",
        "size": "45% rynku detalicznego",
        "difficulty": "łatwy",
        "potential": "średni",
        "typical_order": "2,000 - 8,000 PLN miesięcznie",
        "decision_maker": "Właściciel",
        "key_factors": ["Marża", "Rotacja towaru", "Wsparcie merchandisingowe"]
    },
    "modern_trade": {
        "name": "Modern Trade", 
        "description": "Sieci supermarketów i hipermarketów",
        "size": "40% rynku detalicznego",
        "difficulty": "trudny",
        "potential": "bardzo wysoki",
        "typical_order": "50,000 - 500,000 PLN miesięcznie",
        "decision_maker": "Category Manager, Commercial Director",
        "key_factors": ["Cena", "Wolumen", "Marketing support", "Listing fees"]
    },
    "convenience": {
        "name": "Convenience",
        "description": "Sieci convenience, stacje benzynowe",
        "size": "15% rynku detalicznego",
        "difficulty": "średni",
        "potential": "rosnący",
        "typical_order": "10,000 - 30,000 PLN miesięcznie",
        "decision_maker": "Regional Manager",
        "key_factors": ["Convenience packaging", "Brand recognition", "Impulse"]
    }
}

# Baza klientów - Traditional Trade (5-6 przykładowych)
CUSTOMERS_DATABASE = {
    # ===== TRADITIONAL TRADE =====
    "trad_001": {
        "id": "trad_001",
        "segment": "traditional_trade",
        "name": "Sklep 'U Kowalskich'",
        "type": "Sklep osiedlowy",
        "owner": "Janina Kowalska",
        "location": "Warszawa, Ursynów, Os. Kabaty",
        "size": "80m²",
        "established": 1998,
        
        "description": """
Dobrze prosperujący sklep osiedlowy na dużym osiedlu Kabaty. 
Właścicielka Janina Kowalska (58 lat) prowadzi biznes od ponad 25 lat.
Stali klienci to głównie rodziny z dziećmi i seniorzy z okolicy.
Sklep słynie z dobrej obsługi i 'klimatu małego sklepu'.
""",
        
        "characteristics": {
            "monthly_revenue": "~120,000 PLN",
            "customers_per_day": "150-200",
            "avg_basket": "45 PLN",
            "opening_hours": "6:00-22:00",
            "employees": 3,  # właścicielka + 2 osoby
            "parking": "Brak (osiedle)",
            "competition": "Biedronka 300m, mały Carrefour Express 500m"
        },
        
        "current_suppliers": [
            "Hurtownia Makro (główny)",
            "Eurocash",
            "Lokalni dostawcy pieczywa i nabiału"
        ],
        
        "pain_points": [
            "Konkurencja dyskontów - klienci porównują ceny",
            "Ograniczona przestrzeń magazynowa",
            "Trudno znaleźć nowych dostawców z dobrą marżą",
            "Brak czasu na analizę asortymentu"
        ],
        
        "opportunities": [
            "Stali klienci - potencjał na produkty premium",
            "Brak mocnej konkurencji w kategorii Personal Care",
            "Właścicielka otwarta na nowości jeśli dobra marża"
        ],
        
        "personality": {
            "style": "Tradycyjny, ostrożny",
            "priorities": ["Marża", "Pewność rotacji", "Łatwość współpracy"],
            "concerns": ["Zaleganie towaru", "Skomplikowane warunki", "Zbyt duże zamówienia"],
            "decision_speed": "Powolna - potrzebuje czasu na przemyślenie",
            "negotiation_style": "Twarda na cenę, ale lojalna jak się przekona"
        },
        
        "initial_status": "prospect",  # prospect, active, lost
        "relationship_score": 0,  # 0-100
        "potential_monthly": 3500  # PLN
    },
    
    "trad_002": {
        "id": "trad_002",
        "segment": "traditional_trade",
        "name": "Kiosk 'MaxiPress'",
        "type": "Kiosk z RUCHEM",
        "owner": "Marek Nowak",
        "location": "Kraków, Stare Miasto, ul. Floriańska",
        "size": "12m²",
        "established": 2015,
        
        "description": """
Mały kiosk w centrum Krakowa, blisko Rynku Głównego.
Właściciel Marek Nowak (42 lata) wykupił kiosk z sieci RUCH.
Duży ruch turystyczny i przechodniów. Sprzedaż impulsowa.
Skupia się na drobnych artykułach - napoje, słodycze, drogeria podróżna.
""",
        
        "characteristics": {
            "monthly_revenue": "~65,000 PLN",
            "customers_per_day": "200-300 (wysoki ruch w sezonie)",
            "avg_basket": "18 PLN",
            "opening_hours": "7:00-21:00",
            "employees": 2,
            "parking": "Brak (centrum)",
            "competition": "Dużo konkurencji - Żabka, Carrefour Express w pobliżu"
        },
        
        "current_suppliers": [
            "RUCH (prasa)",
            "Hurtownia ABC",
            "Dostawcy słodyczy i napojów"
        ],
        
        "pain_points": [
            "Bardzo ograniczona przestrzeń - każda półka na wagę złota",
            "Wysokie czynsz i koszty - potrzebuje dobrej marży",
            "Produkty muszą się szybko rotować",
            "Klienci głównie kupują 'na już' - małe opakowania"
        ],
        
        "opportunities": [
            "Duży ruch - potencjał na produkty impulsowe",
            "Turyści kupują bez patrzenia na cenę",
            "Brak Personal Care w małych opakowaniach podróżnych"
        ],
        
        "personality": {
            "style": "Dynamiczny, biznesowy",
            "priorities": ["Marża", "Szybka rotacja", "Małe opakowania"],
            "concerns": ["Zaleganie towaru", "Produkty których nikt nie zna", "Duże MOQ"],
            "decision_speed": "Szybka - jeśli widzi biznes, decyduje od razu",
            "negotiation_style": "Konkretny, transakcyjny - liczy się zysk"
        },
        
        "initial_status": "prospect",
        "relationship_score": 0,
        "potential_monthly": 2000
    },
    
    "trad_003": {
        "id": "trad_003",
        "segment": "traditional_trade",
        "name": "Sieć 'Nasz Sklep' (3 lokalizacje)",
        "type": "Mała sieć lokalna",
        "owner": "Rodzina Wiśniewskich",
        "location": "Poznań i okolice (Jeżyce, Grunwald, Luboń)",
        "size": "3 sklepy × 120m²",
        "established": 2008,
        
        "description": """
Lokalna sieć 3 sklepów prowadzona przez rodzinę Wiśniewskich.
Ojciec Adam (55) i syn Michał (28) - podział ról: ojciec negocjuje, syn zarządza.
Profesjonalne podejście, ambicje rozbudowy o kolejne lokalizacje.
Dobrze zorganizowani, mają wspólny magazyn i system zamówień.
""",
        
        "characteristics": {
            "monthly_revenue": "~450,000 PLN (suma 3 sklepów)",
            "customers_per_day": "400-500 (suma)",
            "avg_basket": "55 PLN",
            "opening_hours": "6:30-22:00",
            "employees": 12,
            "parking": "Tak - przy 2 lokalizacjach",
            "competition": "Biedronka blisko każdej lokalizacji"
        },
        
        "current_suppliers": [
            "Eurocash (główny)",
            "Selgros",
            "Bezpośrednio producenci (nabiał, pieczywo)"
        ],
        
        "pain_points": [
            "Trudno konkurować z dyskontami - potrzebują wyróżników",
            "Chcą unikalnego asortymentu którego nie ma w Biedronce",
            "Logistyka - wolą dostawców z elastycznymi terminami",
            "Syn chce modernizacji, ojciec jest ostrożny"
        ],
        
        "opportunities": [
            "Wolumen - 3 sklepy to spory potencjał",
            "Profesjonalne podejście - łatwiejsza współpraca",
            "Szukają dostawców premium products",
            "Mają ambicje wzrostu - myślą długoterminowo"
        ],
        
        "personality": {
            "style": "Profesjonalny, analityczny",
            "priorities": ["Wyróżniki vs dyskontów", "Wolumen discount", "Wsparcie marketingowe"],
            "concerns": ["Lock-in w umowę", "Zbyt sztywne warunki", "Listing fees"],
            "decision_speed": "Średnia - muszą się naradzić ojciec z synem",
            "negotiation_style": "Merytoryczny - znają rynek, liczą wszystko"
        },
        
        "initial_status": "prospect",
        "relationship_score": 0,
        "potential_monthly": 12000
    },
    
    "trad_004": {
        "id": "trad_004",
        "segment": "traditional_trade",
        "name": "Sklep 'Smaczek'",
        "type": "Sklep spożywczy",
        "owner": "Grażyna Lewandowska",
        "location": "Wrocław, Śródmieście, ul. Odrzańska",
        "size": "60m²",
        "established": 2012,
        
        "description": """
Mały sklep spożywczy w śródmieściu Wrocławia, blisko akademików.
Właścicielka Grażyna (35) skupia się na studentach i młodych profesjonalistach.
Nowoczesne podejście - Instagram, promocje dla stałych klientów.
Stawia na produkty convenience i zdrowe przekąski.
""",
        
        "characteristics": {
            "monthly_revenue": "~85,000 PLN",
            "customers_per_day": "120-180",
            "avg_basket": "28 PLN",
            "opening_hours": "7:00-23:00",
            "employees": 2,
            "parking": "Brak",
            "competition": "Żabka 100m, Carrefour Express 200m"
        },
        
        "current_suppliers": [
            "Makro",
            "Hurtownia ABC", 
            "Lokalni producenci zdrowej żywności"
        ],
        
        "pain_points": [
            "Studenci wrażliwi na cenę - trudna marża",
            "Duża konkurencja convenience stores",
            "Brak unikalnego asortymentu",
            "Młodzi klienci kupują małe porcje, często"
        ],
        
        "opportunities": [
            "Młoda grupa docelowa - potencjał na personal care",
            "Właścicielka otwarta na social media i promocje",
            "Brak dobrych produktów convenience w Food",
            "Klienci kupują impulsowo - dobra ekspozycja = sprzedaż"
        ],
        
        "personality": {
            "style": "Nowoczesny, otwarty na innowacje",
            "priorities": ["Produkty dla młodych", "Social media support", "Małe opakowania"],
            "concerns": ["Produkty 'dla babć'", "Brak wsparcia marketingowego", "Wysokie MOQ"],
            "decision_speed": "Szybka - jeśli pasuje do koncepcji sklepu",
            "negotiation_style": "Partnerska - szuka win-win, długoterminowej współpracy"
        },
        
        "initial_status": "prospect",
        "relationship_score": 0,
        "potential_monthly": 2800
    },
    
    "trad_005": {
        "id": "trad_005",
        "segment": "traditional_trade",
        "name": "Delikatesy 'Pod Lipami'",
        "type": "Sklep premium osiedlowy",
        "owner": "Jan Kowalczyk",
        "location": "Gdańsk, Oliwa, osiedle willowe",
        "size": "95m²",
        "established": 2010,
        
        "description": """
Sklep premium na ekskluzywnym osiedlu w Oliwie.
Właściciel Jan (48) ma doświadczenie w gastronomii.
Klienci zamożni - kupują jakość, nie patrzą na cenę.
Szeroki wybór produktów regionalnych, eko, bio.
""",
        
        "characteristics": {
            "monthly_revenue": "~180,000 PLN",
            "customers_per_day": "80-120",
            "avg_basket": "95 PLN",
            "opening_hours": "8:00-20:00",
            "employees": 4,
            "parking": "Tak - własny parking",
            "competition": "Niewielka - najbliższy sklep 1.5km"
        },
        
        "current_suppliers": [
            "Makro (selektywnie)",
            "Bezpośrednio od producentów premium",
            "Importerzy produktów eko/bio"
        ],
        
        "pain_points": [
            "Trudno znaleźć unikalny asortyment premium",
            "Klienci wymagający - oczekują najwyższej jakości",
            "Przestrzeń ograniczona - tylko najlepsze produkty",
            "Nie chce produktów 'z dyskontu'"
        ],
        
        "opportunities": [
            "Zamożni klienci - mogą płacić więcej",
            "Brak konkurencji w okolicy",
            "Potencjał na produkty eko/premium z FreshLife",
            "Właściciel szuka wyróżników"
        ],
        
        "personality": {
            "style": "Wybredny, nastawiony na jakość",
            "priorities": ["Jakość", "Unikalne produkty", "Historia marki"],
            "concerns": ["Produkty masowe", "Niska jakość", "Brak certyfikatów"],
            "decision_speed": "Powolna - testuje produkty, sprawdza referencje",
            "negotiation_style": "Elitarny - cena mniej ważna niż jakość i exclusivity"
        },
        
        "initial_status": "prospect",
        "relationship_score": 0,
        "potential_monthly": 5500
    },
    
    "trad_006": {
        "id": "trad_006",
        "segment": "traditional_trade",
        "name": "Sklep 'Rodzinny Koszyk'",
        "type": "Sklep osiedlowy",
        "owner": "Teresa i Andrzej Nowakowie",
        "location": "Łódź, Bałuty, os. Teofilów",
        "size": "70m²",
        "established": 2005,
        
        "description": """
Typowy sklep osiedlowy prowadzony przez małżeństwo emerytów.
Teresa (64) i Andrzej (67) prowadzą sklep 'na dorobku' do emerytury.
Stali klienci, atmosfera 'sąsiedzka', długie rozmowy przy kasie.
Niewielka rotacja, ostrożne podejście do nowości.
""",
        
        "characteristics": {
            "monthly_revenue": "~75,000 PLN",
            "customers_per_day": "90-130",
            "avg_basket": "38 PLN",
            "opening_hours": "7:00-20:00",
            "employees": 2,  # właściciele
            "parking": "Brak",
            "competition": "Biedronka 400m, ale klienci lojalni"
        },
        
        "current_suppliers": [
            "Eurocash (główny)",
            "Lokalni dostawcy"
        ],
        
        "pain_points": [
            "Niska rotacja - boją się zalegania towaru",
            "Ograniczony kapitał - małe zamówienia",
            "Brak czasu i chęci na zmiany",
            "Klienci starsi - kupują sprawdzone produkty"
        ],
        
        "opportunities": [
            "Lojalni klienci - łatwo wprowadzić znane marki",
            "Brak konkurencji bezpośredniej w personal care",
            "Właściciele chętni jeśli ktoś im doradzi co brać",
            "Potencjał na podstawowe produkty z dobrą marżą"
        ],
        
        "personality": {
            "style": "Tradycyjny, nieufny do nowości",
            "priorities": ["Bezpieczeństwo", "Znane marki", "Mała ilość na start"],
            "concerns": ["Zaleganie", "Skomplikowane warunki", "Duże zamówienia"],
            "decision_speed": "Bardzo wolna - muszą się naradzić, przemyśleć",
            "negotiation_style": "Ostrożna - potrzebują gwarancji i prostych warunków"
        },
        
        "initial_status": "prospect",
        "relationship_score": 0,
        "potential_monthly": 1800
    }
}

def get_customer_by_id(customer_id):
    """Zwraca klienta po ID"""
    return CUSTOMERS_DATABASE.get(customer_id)

def get_customers_by_segment(segment):
    """Zwraca listę klientów z danego segmentu"""
    return [c for c in CUSTOMERS_DATABASE.values() if c["segment"] == segment]

def get_all_prospects():
    """Zwraca wszystkich prospects (nowych klientów)"""
    return [c for c in CUSTOMERS_DATABASE.values() if c["initial_status"] == "prospect"]

def get_segment_info(segment_key):
    """Zwraca info o segmencie rynku"""
    return MARKET_SEGMENTS.get(segment_key)
