"""
Baza klientów FMCG dla regionu Piaseczno
Traditional Trade: sklepy osiedlowe, kioski, małe sieci lokalne
Modern Trade: dyskonty, supermarkety
"""

# Unikalne twarze (avatary) dla każdego klienta - 25 różnych emoji
CLIENT_AVATARS = {
    "pias_001": "👩",  # Danuta Kowalska
    "pias_002": "👨",  # Marek Wiśniewski
    "pias_003": "👴",  # Pan Stanisław
    "pias_004": "👩‍🦰",  # Katarzyna
    "pias_005": "🧔",  # Tomasz
    "pias_006": "👨‍🦳",  # Pan Henryk
    "pias_007": "👩‍🦱",  # Pani Zofia
    "pias_008": "🧑",  # Manager
    "pias_009": "👨‍💼",  # Dyrektor
    "pias_010": "👩‍💼",  # Kierowniczka
    "pias_011": "👱‍♂️",  # Młody właściciel
    "pias_012": "👱‍♀️",  # Młoda właścicielka
    "pias_013": "🧓",  # Senior
    "pias_014": "👵",  # Pani Senior
    "pias_015": "👨‍🦲",  # Łysy pan
    "pias_016": "🧑‍🦰",  # Rudy właściciel
    "pias_017": "🧑‍🦱",  # Kręcone włosy
    "pias_018": "👩‍🦳",  # Siwa pani
    "pias_019": "🧑‍💼",  # Biznesmen
    "pias_020": "👨‍🍳",  # Szef kuchni
    "pias_021": "👩‍🔧",  # Właścicielka praktyczna
    "pias_022": "🧑‍🏫",  # Wykształcony właściciel
    "pias_023": "👨‍⚕️",  # Pan doktor (były)
    "pias_024": "👩‍⚖️",  # Pani prawniczka (była)
    "pias_025": "🧑‍🎓"   # Młody absolwent
}

# Współrzędne geograficzne Piaseczna
PIASECZNO_BASE = {
    "name": "Piaseczno - Biuro Regionalne FreshLife",
    "latitude": 52.0846,
    "longitude": 21.0250,
    "address": "ul. Puławska 50, Piaseczno"
}

# Baza 25 klientów w promieniu 30km od Piaseczna
PIASECZNO_CUSTOMERS = {
    
    # ===== TRADITIONAL TRADE - MAŁE SKLEPY (5-10 km) =====
    
    "pias_001": {
        "id": "pias_001",
        "segment": "traditional_trade",
        "name": "Sklep 'U Danusi'",
        "type": "Sklep osiedlowy",
        "owner": "Danuta Kowalska",
        "location": "Piaseczno Centrum, Os. Warszawskie",
        "address": "ul. Kościuszki 15, Piaseczno",
        "latitude": 52.0832,
        "longitude": 21.0267,
        "distance_km": 0.3,
        "size_sqm": 65,
        "established": 2005,
        
        "description": """
Niewielki sklep osiedlowy w centrum Piaseczna, tuż przy stacji PKP.
Właścicielka Danuta Kowalska (52 lata) prowadzi biznes od prawie 20 lat.
Główni klienci to mieszkańcy pobliskich bloków i ludzie w drodze do pracy.
Znana z dobrej obsługi i 'pamiętania' stałych klientów.
""",
        
        "owner_profile": {
            "name": "Danuta Kowalska",
            "age": 52,
            "experience_years": 18,
            "personality": "Tradycyjna, ostrożna, ale lojalna",
            "priorities": ["Marża", "Stali klienci", "Prosta współpraca"],
            "concerns": ["Zaleganie towaru", "Konkurencja Biedronki", "Skomplikowane warunki"]
        },
        
        "characteristics": {
            "monthly_revenue": 95000,
            "customers_per_day": 140,
            "avg_basket": 42,
            "opening_hours": "6:00-22:00",
            "employees": 2,
            "parking": False,
            "competition": "Biedronka 200m, Żabka 150m"
        },
        
        "potential_monthly": 3200,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_002": {
        "id": "pias_002",
        "segment": "traditional_trade",
        "name": "Kiosk 'MaxiPress Piaseczno'",
        "type": "Kiosk przy stacji PKP",
        "owner": "Marek Wiśniewski",
        "location": "Piaseczno - dworzec PKP",
        "address": "Plac Piłsudskiego 1, Piaseczno",
        "latitude": 52.0845,
        "longitude": 21.0240,
        "distance_km": 0.2,
        "size_sqm": 15,
        "established": 2018,
        
        "description": """
Mały kiosk przy głównym dworcu PKP w Piasecznie.
Właściciel Marek (38) skupia się na dojazdówce - sprzedaż impulsowa.
Duży ruch rano (6-9) i wieczorem (16-19). Produkty convenience.
""",
        
        "owner_profile": {
            "name": "Marek Wiśniewski",
            "age": 38,
            "experience_years": 6,
            "personality": "Dynamiczny, biznesowy, konkretny",
            "priorities": ["Marża", "Szybka rotacja", "Małe opakowania"],
            "concerns": ["Przestrzeń", "Produkty wolno rotujące", "Duże MOQ"]
        },
        
        "characteristics": {
            "monthly_revenue": 45000,
            "customers_per_day": 280,
            "avg_basket": 12,
            "opening_hours": "5:30-22:00",
            "employees": 2,
            "parking": False,
            "competition": "Żabka w dworcu, automaty"
        },
        
        "potential_monthly": 1500,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_003": {
        "id": "pias_003",
        "segment": "traditional_trade",
        "name": "Sklep 'ABC Górki'",
        "type": "Sklep osiedlowy",
        "owner": "Piotr Zieliński",
        "location": "Piaseczno-Górki",
        "address": "ul. Armii Krajowej 24, Piaseczno",
        "latitude": 52.0912,
        "longitude": 21.0180,
        "distance_km": 1.2,
        "size_sqm": 85,
        "established": 2012,
        
        "description": """
Dobrze prosperujący sklep na osiedlu Górki w Piasecznie.
Właściciel Piotr (44) ma doświadczenie w handlu. Nowoczesne podejście.
Główni klienci to rodziny z dziećmi - nowe osiedle domków jednorodzinnych.
""",
        
        "owner_profile": {
            "name": "Piotr Zieliński",
            "age": 44,
            "experience_years": 11,
            "personality": "Profesjonalny, otwarty na nowości",
            "priorities": ["Wyróżniki", "Jakość", "Wsparcie merchandisingowe"],
            "concerns": ["Produkty masowe", "Brak wsparcia", "Złe warunki płatności"]
        },
        
        "characteristics": {
            "monthly_revenue": 135000,
            "customers_per_day": 165,
            "avg_basket": 52,
            "opening_hours": "6:30-22:00",
            "employees": 3,
            "parking": True,
            "competition": "Biedronka 800m, sklepy osiedlowe"
        },
        
        "potential_monthly": 4800,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_004": {
        "id": "pias_004",
        "segment": "traditional_trade",
        "name": "Delikatesy 'Julka'",
        "type": "Sklep premium",
        "owner": "Julia Kamińska",
        "location": "Konstancin-Jeziorna",
        "address": "ul. Warszawska 12, Konstancin-Jeziorna",
        "latitude": 52.0846,
        "longitude": 21.1145,
        "distance_km": 7.2,
        "size_sqm": 110,
        "established": 2015,
        
        "description": """
Ekskluzywny sklep w zamożnym Konstancinie-Jeziornie.
Właścicielka Julia (39) stawia na produkty premium i eko.
Klienci zamożni - kupują jakość, nie cenę. Atmosfera butiku.
""",
        
        "owner_profile": {
            "name": "Julia Kamińska",
            "age": 39,
            "experience_years": 8,
            "personality": "Wybredna, nastawiona na jakość i image",
            "priorities": ["Jakość", "Produkty eko/bio", "Exclusivity"],
            "concerns": ["Produkty masowe", "Brak certyfikatów", "Produkty 'z dyskontu'"]
        },
        
        "characteristics": {
            "monthly_revenue": 220000,
            "customers_per_day": 95,
            "avg_basket": 115,
            "opening_hours": "8:00-20:00",
            "employees": 4,
            "parking": True,
            "competition": "Niewielka - najbliższy premium 3km"
        },
        
        "potential_monthly": 8500,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_005": {
        "id": "pias_005",
        "segment": "traditional_trade",
        "name": "Sklep 'Osiedlowy Plus'",
        "type": "Sklep osiedlowy",
        "owner": "Tomasz i Anna Kowalczykowie",
        "location": "Józefosław",
        "address": "ul. Spacerowa 8, Józefosław",
        "latitude": 52.0612,
        "longitude": 21.0389,
        "distance_km": 3.1,
        "size_sqm": 95,
        "established": 2010,
        
        "description": """
Sklep prowadzony przez młode małżeństwo na rozwijającym się osiedlu.
Tomasz (35) i Anna (33) mają ambicje - chcą rozwinąć biznes.
Mieszkańcy to głównie młode rodziny - duże koszyki zakupowe.
""",
        
        "owner_profile": {
            "name": "Tomasz i Anna Kowalczykowie",
            "age": 35,
            "experience_years": 13,
            "personality": "Ambitni, partnerzy, długoterminowo nastawieni",
            "priorities": ["Rozwój", "Stali klienci", "Nowoczesny asortyment"],
            "concerns": ["Lock-in w umowy", "Brak elastyczności", "Wysokie wymogi"]
        },
        
        "characteristics": {
            "monthly_revenue": 145000,
            "customers_per_day": 180,
            "avg_basket": 58,
            "opening_hours": "6:00-22:00",
            "employees": 4,
            "parking": True,
            "competition": "Biedronka w budowie (za 6 mies.)"
        },
        
        "potential_monthly": 5200,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    # ===== TRADITIONAL TRADE - ŚREDNIA ODLEGŁOŚĆ (10-20 km) =====
    
    "pias_006": {
        "id": "pias_006",
        "segment": "traditional_trade",
        "name": "Sieć 'Nasz Sklep' (4 lokalizacje)",
        "type": "Mała sieć lokalna",
        "owner": "Adam Wiśniewski",
        "location": "Piaseczno region (4 sklepy)",
        "address": "ul. Julianowska 32, Piaseczno (centrala)",
        "latitude": 52.0723,
        "longitude": 21.0312,
        "distance_km": 1.8,
        "size_sqm": 450,  # suma 4 sklepów
        "established": 2008,
        
        "description": """
Lokalna sieć 4 sklepów w regionie Piaseczna (Piaseczno, Julianów, Złotokłos, Lesznowola).
Właściciel Adam (51) to doświadczony biznesmen. Profesjonalna organizacja.
Wspólny magazyn, system zamówień, planują 5-ty sklep w 2026.
""",
        
        "owner_profile": {
            "name": "Adam Wiśniewski",
            "age": 51,
            "experience_years": 16,
            "personality": "Profesjonalny, analityczny, długoterminowy",
            "priorities": ["Wolumen discount", "Wsparcie marketingowe", "Exclusivity regionalna"],
            "concerns": ["Listing fees", "Sztywne warunki", "Konkurencja dyskontów"]
        },
        
        "characteristics": {
            "monthly_revenue": 580000,
            "customers_per_day": 450,
            "avg_basket": 62,
            "opening_hours": "6:00-23:00",
            "employees": 18,
            "parking": True,
            "competition": "Biedronka, Lidl we wszystkich lokalizacjach"
        },
        
        "potential_monthly": 18000,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_007": {
        "id": "pias_007",
        "segment": "convenience",
        "name": "Żabka - Piaseczno Dworzec",
        "type": "Franchise - Żabka",
        "owner": "Franchise (franczyzobiorca lokalny)",
        "location": "Piaseczno - przy dworcu",
        "address": "ul. Dworcowa 3, Piaseczno",
        "latitude": 52.0851,
        "longitude": 21.0235,
        "distance_km": 0.25,
        "size_sqm": 60,
        "established": 2019,
        
        "description": """
Żabka w strategicznej lokalizacji przy dworcu PKP.
Franczyzobiorca musi kupować przez Żabka Polska, ale ma autonomię w promocjach lokalnych.
Duży ruch - głównie produkty convenience i impulsowe.
""",
        
        "owner_profile": {
            "name": "Franchise Żabka",
            "age": 40,
            "experience_years": 4,
            "personality": "Profesjonalny, z procedurami Żabki",
            "priorities": ["Promocje Żabka", "Produkty convenience", "Szybka rotacja"],
            "concerns": ["Musi przez Żabka Polska", "Ograniczona autonomia", "KPIs Żabki"]
        },
        
        "characteristics": {
            "monthly_revenue": 185000,
            "customers_per_day": 320,
            "avg_basket": 28,
            "opening_hours": "24/7",
            "employees": 6,
            "parking": False,
            "competition": "Inne kioski przy dworcu"
        },
        
        "potential_monthly": 3500,  # Ograniczone - musi przez Żabka Polska
        "initial_status": "prospect",
        "relationship_score": 0,
        "note": "⚠️ Decyzja kategorijna na poziomie Żabka Polska - lokalnie tylko promocje"
    },
    
    "pias_008": {
        "id": "pias_008",
        "segment": "traditional_trade",
        "name": "Sklep 'Groszek'",
        "type": "Sklep osiedlowy",
        "owner": "Ewa Lewandowska",
        "location": "Magdalenka",
        "address": "ul. Leszczynowa 5, Magdalenka",
        "latitude": 52.0534,
        "longitude": 21.0689,
        "distance_km": 5.4,
        "size_sqm": 55,
        "established": 2016,
        
        "description": """
Mały sklep na wiejskiej okolicy Magdalenki.
Właścicielka Ewa (47) prowadzi sklep 'z doskoku' - ma inną pracę.
Klienci to głównie mieszkańcy okolicznych domów - mała społeczność.
""",
        
        "owner_profile": {
            "name": "Ewa Lewandowska",
            "age": 47,
            "experience_years": 7,
            "personality": "Spokojna, bez presji wzrostu, stabilna",
            "priorities": ["Proste warunki", "Małe zamówienia", "Sprawdzone produkty"],
            "concerns": ["Zaleganie", "Komplikacje", "Duże MOQ"]
        },
        
        "characteristics": {
            "monthly_revenue": 52000,
            "customers_per_day": 70,
            "avg_basket": 38,
            "opening_hours": "7:00-20:00",
            "employees": 1,
            "parking": True,
            "competition": "Biedronka 4km (Piaseczno)"
        },
        
        "potential_monthly": 1400,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_009": {
        "id": "pias_009",
        "segment": "traditional_trade",
        "name": "Sklep 'Smaki Południa'",
        "type": "Sklep osiedlowy",
        "owner": "Grzegorz Nowak",
        "location": "Góra Kalwaria",
        "address": "ul. Warszawska 78, Góra Kalwaria",
        "latitude": 51.9789,
        "longitude": 21.2056,
        "distance_km": 18.5,
        "size_sqm": 72,
        "established": 2011,
        
        "description": """
Sklep w mniejszym mieście Góra Kalwaria, ok. 19km od Piaseczna.
Właściciel Grzegorz (53) to doświadczony handlowiec.
Klienci lojalni - mały rynek, wszyscy się znają.
""",
        
        "owner_profile": {
            "name": "Grzegorz Nowak",
            "age": 53,
            "experience_years": 12,
            "personality": "Tradycyjny, stabilny, lojalny",
            "priorities": ["Relacje", "Sprawdzone marki", "Dobra marża"],
            "concerns": ["Nowości bez reputacji", "Daleki dojazd dostawców", "Minimalne zamówienia"]
        },
        
        "characteristics": {
            "monthly_revenue": 88000,
            "customers_per_day": 110,
            "avg_basket": 44,
            "opening_hours": "6:30-21:00",
            "employees": 2,
            "parking": True,
            "competition": "Biedronka w centrum, ale klienci lojalni"
        },
        
        "potential_monthly": 2800,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_010": {
        "id": "pias_010",
        "segment": "traditional_trade",
        "name": "Sklep 'Rodzinny Koszyk'",
        "type": "Sklep osiedlowy",
        "owner": "Maria Kowalczyk",
        "location": "Lesznowola",
        "address": "ul. Główna 15, Lesznowola",
        "latitude": 52.0512,
        "longitude": 21.0012,
        "distance_km": 4.8,
        "size_sqm": 68,
        "established": 2013,
        
        "description": """
Typowy sklep osiedlowy w Lesznowoli.
Właścicielka Maria (58) prowadzi sklep spokojnie, bez ambicji ekspansji.
Stali klienci, atmosfera sąsiedzka.
""",
        
        "owner_profile": {
            "name": "Maria Kowalczyk",
            "age": 58,
            "experience_years": 10,
            "personality": "Tradycyjna, ostrożna, potrzebuje doradztwa",
            "priorities": ["Bezpieczeństwo", "Znane marki", "Mała ilość na start"],
            "concerns": ["Ryzyko", "Zaleganie", "Skomplikowane warunki"]
        },
        
        "characteristics": {
            "monthly_revenue": 72000,
            "customers_per_day": 95,
            "avg_basket": 40,
            "opening_hours": "7:00-20:00",
            "employees": 2,
            "parking": False,
            "competition": "Niewielka - osiedle bez Biedronki"
        },
        
        "potential_monthly": 2000,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    # ===== CONVENIENCE & MODERN TRADE (15-30 km) =====
    
    "pias_011": {
        "id": "pias_011",
        "segment": "modern_trade",
        "name": "Carrefour Express - Wilanów",
        "type": "Supermarket - Carrefour Express",
        "owner": "Carrefour Polska S.A.",
        "location": "Warszawa - Wilanów",
        "address": "ul. Klimczaka 1, Warszawa",
        "latitude": 52.1678,
        "longitude": 21.0445,
        "distance_km": 13.2,
        "size_sqm": 280,
        "established": 2017,
        
        "description": """
Carrefour Express w ekskluzywnej dzielnicy Wilanów.
Decyzje kategorialne na poziomie Carrefour Polska.
Lokalny manager ma niewielką autonomię - głównie wykonawstwo.
""",
        
        "owner_profile": {
            "name": "Carrefour Polska - Regional Manager",
            "age": 0,
            "experience_years": 0,
            "personality": "Korporacyjny - procedury, KPIs",
            "priorities": ["Realizacja planogramów", "Promocje Carrefour", "Wolumen"],
            "concerns": ["Decyzje centralne", "Listing fees", "Planogramy"]
        },
        
        "characteristics": {
            "monthly_revenue": 450000,
            "customers_per_day": 280,
            "avg_basket": 85,
            "opening_hours": "6:00-23:00",
            "employees": 12,
            "parking": True,
            "competition": "Biedronka, Lidl, Auchan w okolicy"
        },
        
        "potential_monthly": 12000,  # Wymaga listing agreements
        "initial_status": "prospect",
        "relationship_score": 0,
        "note": "⚠️ Wymaga umowy listing na poziomie Carrefour Polska HQ - długi proces"
    },
    
    "pias_012": {
        "id": "pias_012",
        "segment": "convenience",
        "name": "Circle K - Wilanów",
        "type": "Stacja benzynowa - convenience",
        "owner": "Circle K Polska",
        "location": "Warszawa - Wilanów, S2",
        "address": "Al. Wilanowska 360, Warszawa",
        "latitude": 52.1523,
        "longitude": 21.0389,
        "distance_km": 11.5,
        "size_sqm": 95,
        "established": 2020,
        
        "description": """
Nowoczesna stacja Circle K przy trasie S2 w kierunku Wilanowa.
Duży ruch - zarówno tankujący jak i klienci convenience.
Manager stacji ma autonomię w lokalnych promocjach.
""",
        
        "owner_profile": {
            "name": "Circle K - Station Manager",
            "age": 35,
            "experience_years": 8,
            "personality": "Dynamiczny, nastawiony na convenience i impulse",
            "priorities": ["Produkty convenience", "Impulse purchase", "Szybka rotacja"],
            "concerns": ["Produkty wolno rotujące", "Procedury Circle K", "Planogramy"]
        },
        
        "characteristics": {
            "monthly_revenue": 320000,
            "customers_per_day": 420,
            "avg_basket": 35,
            "opening_hours": "24/7",
            "employees": 10,
            "parking": True,
            "competition": "Orlen, Shell w pobliżu"
        },
        
        "potential_monthly": 5500,
        "initial_status": "prospect",
        "relationship_score": 0,
        "note": "✅ Manager ma autonomię w promocjach lokalnych - dobry target!"
    },
    
    # Dodatkowi klienci - małe sklepy lokalne
    
    "pias_013": {
        "id": "pias_013",
        "segment": "traditional_trade",
        "name": "Sklep 'Centrum'",
        "type": "Sklep osiedlowy",
        "owner": "Krzysztof Mazur",
        "location": "Piaseczno - Zalesie Dolne",
        "address": "ul. Poznańska 12, Zalesie Dolne",
        "latitude": 52.0678,
        "longitude": 21.0478,
        "distance_km": 2.8,
        "size_sqm": 78,
        "established": 2014,
        
        "owner_profile": {
            "name": "Krzysztof Mazur",
            "age": 45,
            "experience_years": 9,
            "personality": "Pragmatyczny, biznesowy",
            "priorities": ["Marża", "Szybka rotacja", "Dobre warunki płatności"],
            "concerns": ["Konkurencja", "Zaleganie", "Słabe wsparcie"]
        },
        
        "characteristics": {
            "monthly_revenue": 98000,
            "customers_per_day": 125,
            "avg_basket": 46,
            "opening_hours": "6:30-21:30",
            "employees": 3,
            "parking": True,
            "competition": "Biedronka 600m"
        },
        
        "potential_monthly": 3100,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_014": {
        "id": "pias_014",
        "segment": "traditional_trade",
        "name": "Sklep 'Przystanek'",
        "type": "Sklep przy przystanku",
        "owner": "Andrzej Sikora",
        "location": "Piaseczno - Kamionka",
        "address": "ul. Julianowska 88, Kamionka",
        "latitude": 52.0589,
        "longitude": 21.0234,
        "distance_km": 3.2,
        "size_sqm": 48,
        "established": 2017,
        
        "owner_profile": {
            "name": "Andrzej Sikora",
            "age": 42,
            "experience_years": 6,
            "personality": "Spokojny, stability-seeking",
            "priorities": ["Proste warunki", "Stali dostawcy", "Niewielkie zamówienia"],
            "concerns": ["Komplikacje", "Duże MOQ", "Nowi dostawcy"]
        },
        
        "characteristics": {
            "monthly_revenue": 56000,
            "customers_per_day": 85,
            "avg_basket": 35,
            "opening_hours": "6:00-21:00",
            "employees": 2,
            "parking": False,
            "competition": "Niewielka - przystanek autobusowy"
        },
        
        "potential_monthly": 1600,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_015": {
        "id": "pias_015",
        "segment": "traditional_trade",
        "name": "Sklep 'Smakosz'",
        "type": "Sklep spożywczy",
        "owner": "Barbara Wójcik",
        "location": "Konstancin - Obory",
        "address": "ul. Łąkowa 3, Obory",
        "latitude": 52.0756,
        "longitude": 21.1234,
        "distance_km": 8.9,
        "size_sqm": 92,
        "established": 2010,
        
        "owner_profile": {
            "name": "Barbara Wójcik",
            "age": 49,
            "experience_years": 13,
            "personality": "Doświadczona, relationship-driven",
            "priorities": ["Długoterminowa współpraca", "Wsparcie", "Jakość produktów"],
            "concerns": ["Brak follow-up", "Słabe wsparcie", "Niestabilni dostawcy"]
        },
        
        "characteristics": {
            "monthly_revenue": 118000,
            "customers_per_day": 140,
            "avg_basket": 52,
            "opening_hours": "7:00-21:00",
            "employees": 3,
            "parking": True,
            "competition": "Biedronka 1.2km"
        },
        
        "potential_monthly": 3900,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_016": {
        "id": "pias_016",
        "segment": "traditional_trade",
        "name": "Sklep 'Dzielnicowy'",
        "type": "Sklep osiedlowy",
        "owner": "Paweł Adamczyk",
        "location": "Chylice",
        "address": "ul. Warszawska 45, Chylice",
        "latitude": 52.1012,
        "longitude": 21.1034,
        "distance_km": 9.2,
        "size_sqm": 64,
        "established": 2016,
        
        "owner_profile": {
            "name": "Paweł Adamczyk",
            "age": 38,
            "experience_years": 7,
            "personality": "Młody, nowoczesny, otwarty",
            "priorities": ["Social media", "Młodzi klienci", "Produkty convenience"],
            "concerns": ["Produkty 'starej daty'", "Brak wsparcia digital", "Sztywne warunki"]
        },
        
        "characteristics": {
            "monthly_revenue": 82000,
            "customers_per_day": 105,
            "avg_basket": 42,
            "opening_hours": "6:00-22:00",
            "employees": 2,
            "parking": True,
            "competition": "Biedronka 1.5km"
        },
        
        "potential_monthly": 2600,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_017": {
        "id": "pias_017",
        "segment": "traditional_trade",
        "name": "Sklep 'Pod Lipami'",
        "type": "Sklep osiedlowy",
        "owner": "Halina Nowakowa",
        "location": "Jazgarzew",
        "address": "ul. Spacerowa 7, Jazgarzew",
        "latitude": 52.0234,
        "longitude": 21.0567,
        "distance_km": 7.8,
        "size_sqm": 58,
        "established": 2008,
        
        "owner_profile": {
            "name": "Halina Nowakowa",
            "age": 62,
            "experience_years": 15,
            "personality": "Tradycyjna, stabilna, potrzebuje wsparcia",
            "priorities": ["Sprawdzone marki", "Proste warunki", "Osobisty kontakt"],
            "concerns": ["Nowości", "Komplikacje", "Brak regularnego kontaktu"]
        },
        
        "characteristics": {
            "monthly_revenue": 48000,
            "customers_per_day": 65,
            "avg_basket": 36,
            "opening_hours": "7:00-19:00",
            "employees": 1,
            "parking": False,
            "competition": "Niewielka"
        },
        
        "potential_monthly": 1200,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_018": {
        "id": "pias_018",
        "segment": "traditional_trade",
        "name": "Mini Market 'Express'",
        "type": "Sklep convenience",
        "owner": "Robert Zalewski",
        "location": "Piaseczno - Julianów",
        "address": "ul. Julianowska 156, Julianów",
        "latitude": 52.0645,
        "longitude": 21.0289,
        "distance_km": 2.5,
        "size_sqm": 75,
        "established": 2019,
        
        "owner_profile": {
            "name": "Robert Zalewski",
            "age": 33,
            "experience_years": 4,
            "personality": "Młody, energiczny, wzrostowy",
            "priorities": ["Szybka rotacja", "Produkty convenience", "Nowoczesny image"],
            "concerns": ["Produkty wolno rotujące", "Stary asortyment", "Brak wsparcia POS"]
        },
        
        "characteristics": {
            "monthly_revenue": 105000,
            "customers_per_day": 155,
            "avg_basket": 38,
            "opening_hours": "6:00-23:00",
            "employees": 3,
            "parking": True,
            "competition": "Żabka 300m"
        },
        
        "potential_monthly": 3400,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_019": {
        "id": "pias_019",
        "segment": "traditional_trade",
        "name": "Sklep 'Przy Rondzie'",
        "type": "Sklep osiedlowy",
        "owner": "Zofia Kowalska",
        "location": "Piaseczno - Os. Henryka",
        "address": "Al. Róż 28, Piaseczno",
        "latitude": 52.0878,
        "longitude": 21.0198,
        "distance_km": 0.8,
        "size_sqm": 82,
        "established": 2015,
        
        "owner_profile": {
            "name": "Zofia Kowalska",
            "age": 51,
            "experience_years": 8,
            "personality": "Pracowita, reliability-focused",
            "priorities": ["Stabilność", "Dobre relacje", "Wsparcie merchandisingowe"],
            "concerns": ["Nowi dostawcy bez referencji", "Brak follow-up", "Problemy z dostawami"]
        },
        
        "characteristics": {
            "monthly_revenue": 108000,
            "customers_per_day": 145,
            "avg_basket": 48,
            "opening_hours": "6:30-21:00",
            "employees": 3,
            "parking": True,
            "competition": "Biedronka 500m"
        },
        
        "potential_monthly": 3600,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_020": {
        "id": "pias_020",
        "segment": "traditional_trade",
        "name": "Delikatesy 'Natura'",
        "type": "Sklep eko/bio",
        "owner": "Katarzyna Zielińska",
        "location": "Konstancin-Jeziorna - centrum",
        "address": "ul. Bielawska 22, Konstancin",
        "latitude": 52.0823,
        "longitude": 21.1178,
        "distance_km": 7.8,
        "size_sqm": 98,
        "established": 2018,
        
        "owner_profile": {
            "name": "Katarzyna Zielińska",
            "age": 36,
            "experience_years": 5,
            "personality": "Eko-świadoma, quality-driven, wymagająca",
            "priorities": ["Produkty eko/bio", "Certyfikaty", "Transparentność składu"],
            "concerns": ["Produkty konwencjonalne", "Brak certyfikatów", "Greenwashing"]
        },
        
        "characteristics": {
            "monthly_revenue": 165000,
            "customers_per_day": 88,
            "avg_basket": 98,
            "opening_hours": "8:00-20:00",
            "employees": 3,
            "parking": True,
            "competition": "Niewielka - niszowy segment"
        },
        
        "potential_monthly": 6500,
        "initial_status": "prospect",
        "relationship_score": 0,
        "note": "🌱 Wymaga produktów z certyfikatami eko/bio - tylko premium linia FreshLife"
    },
    
    "pias_021": {
        "id": "pias_021",
        "segment": "traditional_trade",
        "name": "Sklep 'Sąsiedzki'",
        "type": "Sklep osiedlowy",
        "owner": "Jan Wiśniewski",
        "location": "Łazy",
        "address": "ul. Graniczna 11, Łazy",
        "latitude": 52.0412,
        "longitude": 20.9834,
        "distance_km": 6.2,
        "size_sqm": 62,
        "established": 2013,
        
        "owner_profile": {
            "name": "Jan Wiśniewski",
            "age": 56,
            "experience_years": 10,
            "personality": "Tradycyjny, lojaly, relationship-driven",
            "priorities": ["Długoterminowa współpraca", "Osobisty kontakt", "Stabilność"],
            "concerns": ["Niestabilni dostawcy", "Zmiany warunków", "Brak wsparcia"]
        },
        
        "characteristics": {
            "monthly_revenue": 69000,
            "customers_per_day": 92,
            "avg_basket": 41,
            "opening_hours": "7:00-20:00",
            "employees": 2,
            "parking": False,
            "competition": "Niewielka"
        },
        
        "potential_monthly": 2100,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_022": {
        "id": "pias_022",
        "segment": "convenience",
        "name": "Orlen - Piaseczno Puławska",
        "type": "Stacja benzynowa",
        "owner": "Orlen Polska (franchise)",
        "location": "Piaseczno - trasa Puławska",
        "address": "ul. Puławska 142, Piaseczno",
        "latitude": 52.0789,
        "longitude": 21.0267,
        "distance_km": 0.9,
        "size_sqm": 110,
        "established": 2016,
        
        "owner_profile": {
            "name": "Orlen - Manager Stacji",
            "age": 41,
            "experience_years": 12,
            "personality": "Profesjonalny, KPI-driven, autonomiczny",
            "priorities": ["Marża na convenience", "Produkty impulse", "Szybka rotacja"],
            "concerns": ["Wolno rotujące", "Procedury Orlenu", "Planogramy"]
        },
        
        "characteristics": {
            "monthly_revenue": 385000,
            "customers_per_day": 460,
            "avg_basket": 42,
            "opening_hours": "24/7",
            "employees": 11,
            "parking": True,
            "competition": "Circle K, Shell w regionie"
        },
        
        "potential_monthly": 6200,
        "initial_status": "prospect",
        "relationship_score": 0,
        "note": "✅ Manager ma autonomię w lokalnych promocjach convenience"
    },
    
    "pias_023": {
        "id": "pias_023",
        "segment": "traditional_trade",
        "name": "Sklep 'Pogodny'",
        "type": "Sklep osiedlowy",
        "owner": "Beata Mazurek",
        "location": "Wolica",
        "address": "ul. Centralna 9, Wolica",
        "latitude": 52.0534,
        "longitude": 21.0712,
        "distance_km": 5.9,
        "size_sqm": 71,
        "established": 2011,
        
        "owner_profile": {
            "name": "Beata Mazurek",
            "age": 48,
            "experience_years": 12,
            "personality": "Przyjazna, customer-focused, stabilna",
            "priorities": ["Zadowolenie klientów", "Dobra marża", "Wsparcie"],
            "concerns": ["Niezadowoleni klienci", "Zaleganie", "Słabe produkty"]
        },
        
        "characteristics": {
            "monthly_revenue": 79000,
            "customers_per_day": 102,
            "avg_basket": 43,
            "opening_hours": "6:30-21:00",
            "employees": 2,
            "parking": True,
            "competition": "Biedronka 2km"
        },
        
        "potential_monthly": 2400,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_024": {
        "id": "pias_024",
        "segment": "traditional_trade",
        "name": "Mini Market 'Błysk'",
        "type": "Sklep convenience",
        "owner": "Michał Kowalski",
        "location": "Piaseczno - Głosków",
        "address": "ul. Głoskowska 34, Głosków",
        "latitude": 52.0689,
        "longitude": 21.0456,
        "distance_km": 2.3,
        "size_sqm": 68,
        "established": 2020,
        
        "owner_profile": {
            "name": "Michał Kowalski",
            "age": 29,
            "experience_years": 3,
            "personality": "Młody, ambitny, tech-savvy",
            "priorities": ["Nowoczesne produkty", "Digital marketing", "Impulse purchase"],
            "concerns": ["Stary asortyment", "Brak wsparcia digital", "Długie terminy"]
        },
        
        "characteristics": {
            "monthly_revenue": 92000,
            "customers_per_day": 135,
            "avg_basket": 36,
            "opening_hours": "6:00-23:00",
            "employees": 3,
            "parking": True,
            "competition": "Żabka planowana za rok"
        },
        
        "potential_monthly": 3000,
        "initial_status": "prospect",
        "relationship_score": 0
    },
    
    "pias_025": {
        "id": "pias_025",
        "segment": "traditional_trade",
        "name": "Sklep 'U Ryśka'",
        "type": "Sklep wiejski",
        "owner": "Ryszard Nowak",
        "location": "Wola Prażmowska",
        "address": "ul. Polna 2, Wola Prażmowska",
        "latitude": 51.9912,
        "longitude": 21.0423,
        "distance_km": 12.4,
        "size_sqm": 52,
        "established": 2009,
        
        "owner_profile": {
            "name": "Ryszard Nowak",
            "age": 59,
            "experience_years": 14,
            "personality": "Wiejski, prostolinijny, lojalny",
            "priorities": ["Proste warunki", "Regularność", "Dobra marża"],
            "concerns": ["Komplikacje", "Daleki dojazd dostawców", "Wysokie MOQ"]
        },
        
        "characteristics": {
            "monthly_revenue": 44000,
            "customers_per_day": 58,
            "avg_basket": 38,
            "opening_hours": "7:00-19:00",
            "employees": 1,
            "parking": True,
            "competition": "Brak - jedyny sklep w okolicy"
        },
        
        "potential_monthly": 1100,
        "initial_status": "prospect",
        "relationship_score": 0
    }
}


def get_piaseczno_customers_by_distance(max_distance_km=30):
    """Zwraca klientów w promieniu X km od Piaseczna"""
    return {
        cid: customer for cid, customer in PIASECZNO_CUSTOMERS.items()
        if customer.get("distance_km", 0) <= max_distance_km
    }


def get_piaseczno_customers_by_segment(segment):
    """Zwraca klientów z danego segmentu"""
    return {
        cid: customer for cid, customer in PIASECZNO_CUSTOMERS.items()
        if customer.get("segment") == segment
    }


def get_starter_clients(count=5):
    """
    Zwraca 5 najlepszych klientów PROSPECT na start (Level 1)
    Kryteria: blisko (< 5km), średni potencjał, łatwa osobowość
    """
    candidates = [
        ("pias_001", 5),  # U Danusi - blisko, tradycyjna, dobry start
        ("pias_002", 4),  # MaxiPress - bardzo blisko, biznesowy
        ("pias_003", 5),  # ABC Górki - profesjonalny, otwarty
        ("pias_005", 4),  # Osiedlowy Plus - ambitni, partnerzy
        ("pias_008", 3),  # Groszek - mały, prosty, spokojny
        ("pias_010", 3),  # Rodzinny Koszyk - tradycyjna, potrzebuje pomocy
    ]
    
    # Sortuj po score i weź top 5
    sorted_candidates = sorted(candidates, key=lambda x: x[1], reverse=True)[:count]
    
    return {
        cid: PIASECZNO_CUSTOMERS[cid]
        for cid, _ in sorted_candidates
    }


def calculate_distance(lat1, lon1, lat2, lon2):
    """Oblicza odległość w km między dwoma punktami (haversine formula)"""
    from math import radians, cos, sin, asin, sqrt
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    
    return round(km, 1)
