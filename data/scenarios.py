"""
Definicje scenariuszy dla Business Games Suite

Każda branża może mieć wiele scenariuszy z różnymi warunkami startowymi,
modyfikatorami i celami do osiągnięcia.
"""

# Import klientów dla scenariuszy FMCG
def load_scenario_clients(client_database_id):
    """
    Ładuje bazę klientów dla scenariusza
    
    Args:
        client_database_id: ID bazy klientów (np. 'fmcg_clients_heinz_foodservice')
        
    Returns:
        Dict z klientami lub pusty dict jeśli nie znaleziono
    """
    if client_database_id == "fmcg_clients_heinz_foodservice":
        try:
            from data.industries.fmcg_clients_heinz_foodservice import HEINZ_FOODSERVICE_CLIENTS
            return HEINZ_FOODSERVICE_CLIENTS
        except ImportError:
            print(f"⚠️ Nie można załadować bazy klientów: {client_database_id}")
            return {}
    return {}

SCENARIOS = {
    "consulting": {
        "lifetime": {
            "id": "lifetime",
            "name": "🌟 Lifetime Challenge",
            "description": "Tryb nieskończony bez celów - rywalizuj z innymi graczami o najwyższy wynik! Idealny do długoterminowej zabawy i współzawodnictwa.",
            "icon": "♾️",
            "difficulty": "open",  # Specjalny poziom dla trybu otwartego
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.0,
                "revenue_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "employee_salary_multiplier": 1.0,
                "contract_difficulty_adjustment": 0
            },
            "objectives": [],  # BRAK CELÓW - tryb nieskończony!
            "special_events": [],
            "is_lifetime": True  # Flaga oznaczająca tryb lifetime
        },
        "standard": {
            "id": "standard",
            "name": "Standard Start",
            "description": "Klasyczny start - zrównoważone warunki początkowe dla równej rozgrywki.",
            "icon": "⚖️",
            "difficulty": "medium",
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.0,
                "revenue_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "employee_salary_multiplier": 1.0,
                "contract_difficulty_adjustment": 0
            },
            "objectives": [
                {
                    "type": "revenue_total",
                    "target": 1000000,
                    "description": "Osiągnij łącznie 1M PLN przychodu",
                    "reward_money": 50000
                },
                {
                    "type": "reputation",
                    "target": 80,
                    "description": "Zbuduj reputację na poziomie 80+",
                    "reward_money": 30000
                },
                {
                    "type": "level",
                    "target": 5,
                    "description": "Osiągnij poziom 5",
                    "reward_money": 20000
                }
            ],
            "special_events": []  # Standardowe eventy z random_events.py
        },
        
        "startup_mode": {
            "id": "startup_mode",
            "name": "🚀 Startup Mode",
            "description": "Początek z małym budżetem i zero doświadczenia, ale szybszy wzrost reputacji. Dla ambitnych!",
            "icon": "🚀",
            "difficulty": "hard",
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.5,  # +50% do wzrostu reputacji
                "revenue_multiplier": 0.9,  # -10% do przychodów (mniejsze zlecenia na start)
                "cost_multiplier": 1.2,  # +20% do kosztów (learning curve)
                "employee_salary_multiplier": 1.1,  # +10% wynagrodzenia (trzeba więcej płacić jako startup)
                "contract_difficulty_adjustment": 5  # +5% trudności kontraktów
            },
            "objectives": [
                {
                    "type": "revenue_total",
                    "target": 2000000,
                    "description": "Osiągnij łącznie 2M PLN przychodu mimo trudnego startu",
                    "reward_money": 100000
                },
                {
                    "type": "reputation",
                    "target": 85,
                    "description": "Udowodnij swoją wartość - reputacja 85+",
                    "reward_money": 75000
                },
                {
                    "type": "level",
                    "target": 6,
                    "description": "Osiągnij poziom 6",
                    "reward_money": 50000
                },
                {
                    "type": "employees",
                    "target": 5,
                    "description": "Zbuduj zespół minimum 5 pracowników",
                    "reward_money": 40000
                }
            ],
            "special_events": ["investor_meeting", "startup_competition"]  # TODO: dodać później
        },
        
        "corporate_rescue": {
            "id": "corporate_rescue",
            "name": "💼 Corporate Rescue",
            "description": "Przejmij upadającą firmę z długami, ale doświadczonym zespołem i trwającymi projektami.",
            "icon": "💼",
            "difficulty": "expert",
            "initial_conditions": {
                "money": -30000,  # Start z długiem!
                "reputation": -50,  # Nadszarpnięta reputacja
                "employees": [
                    # TODO: Dodać konkretnych pracowników przy pełnej implementacji
                    # Na razie będzie pusta lista, ale struktura gotowa
                ],
                "office_type": "medium_office",  # Od razu większe biuro
                "contracts_in_progress": []  # TODO: Dodać przejęte kontrakty
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.3,  # +30% - łatwiej odbudować po sukcesach
                "revenue_multiplier": 1.4,  # +40% - doświadczony zespół generuje więcej
                "cost_multiplier": 1.6,  # +60% - wysokie koszty zespołu i biura
                "employee_salary_multiplier": 1.3,  # +30% - seniorzy wymagają więcej
                "contract_difficulty_adjustment": -10  # -10% trudności dzięki doświadczeniu
            },
            "objectives": [
                {
                    "type": "money",
                    "target": 0,
                    "description": "Wyjdź na zero - spłać długi",
                    "reward_money": 50000
                },
                {
                    "type": "reputation",
                    "target": 90,
                    "description": "Odbuduj reputację do poziomu 90+",
                    "reward_money": 100000
                },
                {
                    "type": "revenue_total",
                    "target": 3000000,
                    "description": "Osiągnij łącznie 3M PLN przychodu",
                    "reward_money": 150000
                },
                {
                    "type": "level",
                    "target": 7,
                    "description": "Osiągnij poziom 7",
                    "reward_money": 75000
                }
            ],
            "special_events": ["debt_collection", "team_mutiny"]  # TODO: dodać później
        }
    },
    
    # =========================================================================
    # FMCG - Career Path Scenarios
    # =========================================================================
    "fmcg": {
        "heinz_food_service": {
            "id": "heinz_food_service",
            "name": "🍅 Heinz Food Service Challenge",
            "description": "Zostań Junior Sales Representative w Heinz Polska. Zarządzaj portfolio dwóch marek (Heinz Premium + Pudliszki Value) w kanale Food Service. 8 tygodni intensywnej sprzedaży w regionie Dzięgielów!",
            "icon": "🍅",
            "difficulty": "medium",
            "company": "Heinz Polska",
            "territory": {
                "base_address": "Lipowa 29, 43-445 Dzięgielów",
                "base_lat": 49.7271667,  # 49°43'37.8"N
                "base_lng": 18.7025833,  # 18°42'09.3"E
                "radius_km": 30
            },
            "duration_weeks": 8,
            "client_database": "fmcg_clients_heinz_foodservice",  # Referencja do pliku z klientami
            "total_clients": 25,
            "client_breakdown": {
                "burgerownie_street_food": 6,
                "kebabownie_fast_food": 4,
                "stołówki_bary": 3,
                "pizzerie_casual": 4,
                "hotele": 2,
                "dystrybutorzy": 6
            },
            "initial_conditions": {
                "level": 1,
                "role": "Junior Sales Representative - Heinz Food Service",
                "company": "Heinz Polska",
                "territory_name": "Dzięgielów Food Service",
                "monthly_sales": 0,
                "current_week": 1,
                "energy": 100,
                "clients_total": 25,  # Restauracje, jadłodajnie, foodtrucki, dystrybutorzy
                "clients_active": 0,
                "clients_prospect": 25
            },
            "products": {
                "own": [
                    # HEINZ PREMIUM LINE
                    {
                        "id": "heinz_ketchup_classic",
                        "name": "Heinz Ketchup Klasyczny 875ml",
                        "brand": "Heinz",
                        "tier": "premium",
                        "category": "ketchup",
                        "price_foodservice": 28.50,
                        "margin_pct": 35,
                        "target_segment": "Restauracje premium, burger joints craft, bistro",
                        "usp": "Marka #1 na świecie, najlepsze pomidory, zero konserwantów, Instagram appeal"
                    },
                    {
                        "id": "heinz_ketchup_hot",
                        "name": "Heinz Ketchup Pikantny 875ml",
                        "brand": "Heinz",
                        "tier": "premium",
                        "category": "ketchup",
                        "price_foodservice": 29.50,
                        "margin_pct": 35,
                        "target_segment": "BBQ restaurants, pub food, foodtrucki z ostrymi daniami",
                        "usp": "Premium spicy, naturalna ostrość, upsell opportunity (+2 zł do burgera)"
                    },
                    # PUDLISZKI VALUE LINE
                    {
                        "id": "pudliszki_ketchup_lagodny",
                        "name": "Pudliszki Ketchup Łagodny 980g",
                        "brand": "Pudliszki",
                        "tier": "value",
                        "category": "ketchup",
                        "price_foodservice": 18.50,
                        "margin_pct": 32,
                        "target_segment": "Stołówki, fast food budget, jadłodajnie",
                        "usp": "Polski lider, świetna cena, sprawdzony smak, duża pojemność"
                    },
                    {
                        "id": "pudliszki_ketchup_ostry",
                        "name": "Pudliszki Ketchup Ostry 980g",
                        "brand": "Pudliszki",
                        "tier": "value",
                        "category": "ketchup",
                        "price_foodservice": 18.90,
                        "margin_pct": 32,
                        "target_segment": "Food courts, kebaby, budżetowe restauracje",
                        "usp": "Najlepsza relacja cena/jakość, duża pojemność"
                    }
                ],
                "competition": [
                    {
                        "id": "kotlin_ketchup",
                        "name": "Kotlin Ketchup 900g",
                        "brand": "Kotlin",
                        "category": "ketchup",
                        "price_foodservice": 16.80,
                        "market_share_foodservice": 18,
                        "weaknesses": "Niska узнаваемость marki, zmienność smaku, słabsze wsparcie marketingowe"
                    },
                    {
                        "id": "develey_ketchup",
                        "name": "Develey Ketchup 875ml",
                        "brand": "Develey",
                        "category": "ketchup",
                        "price_foodservice": 24.50,
                        "market_share_foodservice": 8,
                        "weaknesses": "Niemiecka marka, słaba узнаваемость w PL, droższy od Pudliszek a słabszy od Heinza"
                    }
                ]
            },
            "modifiers": {
                "sales_multiplier": 1.0,
                "distribution_gain": 1.2,
                "satisfaction_impact": 1.0,
                "task_difficulty": 0
            },
            "objectives": [
                {
                    "type": "numeric_distribution",
                    "target": 15,
                    "description": "🎯 Zdobądź 15 punktów sprzedaży (60% dystrybucji numerycznej portfolio Heinz)",
                    "reward_money": 3000,
                    "priority": "critical"
                },
                {
                    "type": "monthly_sales",
                    "target": 15000,
                    "description": "💰 Osiągnij 15,000 PLN sprzedaży (Heinz + Pudliszki łącznie)",
                    "reward_money": 2500,
                    "priority": "high"
                },
                {
                    "type": "premium_mix",
                    "target": 40,
                    "description": "⭐ Utrzymaj 40% wartości sprzedaży z linii premium (Heinz)",
                    "reward_money": 2000,
                    "priority": "high"
                },
                {
                    "type": "beat_competition",
                    "target": "kotlin",
                    "target_wins": 6,
                    "description": "🥊 Przejmij 6 klientów od Kotlin (switch na Heinz lub Pudliszki)",
                    "reward_money": 1500,
                    "priority": "medium"
                },
                {
                    "type": "upsell_rate",
                    "target": 30,
                    "description": "📈 Osiągnij 30% upsell rate (klienci Pudliszki kupujący też Heinz)",
                    "reward_money": 1000,
                    "priority": "medium"
                }
            ],
            "kpis": {
                "primary": [
                    "numeric_distribution",
                    "revenue_total",
                    "premium_mix_percent"
                ],
                "secondary": [
                    "heinz_penetration",
                    "pudliszki_volume",
                    "average_basket_value",
                    "upsell_success_rate"
                ]
            },
            "selling_strategy": {
                "premium_clients": "Heinz primary (Pudliszki jako backup/volume option)",
                "value_clients": "Pudliszki primary (Heinz jako upsell/premium option)",
                "portfolio_approach": "Two-brand strategy: pokryj cały rynek od stołówek do fine dining"
            },
            "special_events": [],
            "is_lifetime": False,
            "onboarding_tasks": [
                {
                    "id": "territory_analysis",
                    "name": "Segmentacja Food Service",
                    "description": "Podziel 25 punktów na 3 segmenty: Premium (Heinz focus), Value (Pudliszki focus), Mixed (portfolio approach)"
                },
                {
                    "id": "route_planning",
                    "name": "Plan wizyt tygodniowych",
                    "description": "Zaplanuj trasę wizyt minimalizując koszty dojazdu i maksymalizując coverage"
                },
                {
                    "id": "portfolio_pitch",
                    "name": "Elevator Pitch - Portfolio Heinz",
                    "description": "Przygotuj pitch: 'Heinz Polska oferuje rozwiązania dla każdego segmentu - od Pudliszek do Heinz premium'"
                }
            ]
        },
        
        "lifetime": {
            "id": "lifetime",
            "name": "🌟 Lifetime Challenge",
            "description": "Tryb nieskończony bez celów - buduj karierę w FMCG bez ograniczeń czasowych!",
            "icon": "♾️",
            "difficulty": "open",
            "initial_conditions": {
                "level": 1,
                "role": "Junior Sales Representative",
                "monthly_sales": 0,
                "market_share": 0,
                "customer_satisfaction": 70,
                "team": []
            },
            "modifiers": {
                "sales_multiplier": 1.0,
                "market_share_gain": 1.0,
                "satisfaction_impact": 1.0,
                "task_difficulty": 0
            },
            "objectives": [],
            "special_events": [],
            "is_lifetime": True
        },
        
        "quick_start": {
            "id": "quick_start",
            "name": "🚀 Quick Start - Pierwsza Sprzedaż",
            "description": "Szybki start dla nowych graczy. Osiągnij pierwszy sukces w FMCG!",
            "icon": "🎯",
            "difficulty": "easy",
            "initial_conditions": {
                "level": 1,
                "role": "Junior Sales Representative",
                "monthly_sales": 0,
                "market_share": 0,
                "customer_satisfaction": 70,
                "team": []
            },
            "modifiers": {
                "sales_multiplier": 1.2,        # +20% łatwiejsza sprzedaż
                "market_share_gain": 1.3,       # Szybszy wzrost market share
                "satisfaction_impact": 1.0,
                "task_difficulty": -5           # Łatwiejsze zadania
            },
            "objectives": [
                {
                    "type": "monthly_sales",
                    "target": 15000,
                    "description": "Osiągnij 15k PLN sprzedaży w miesiącu",
                    "reward_money": 5000
                },
                {
                    "type": "market_share",
                    "target": 8,
                    "description": "Zdobądź 8% market share w swoim territory",
                    "reward_money": 3000
                },
                {
                    "type": "level",
                    "target": 2,
                    "description": "Awansuj na Sales Representative",
                    "reward_money": 5000
                }
            ],
            "special_events": []
        },
        
        "territory_master": {
            "id": "territory_master",
            "name": "🗺️ Territory Master",
            "description": "Opanuj swoje territory! Zostań najlepszym rep w regionie.",
            "icon": "👑",
            "difficulty": "medium",
            "initial_conditions": {
                "level": 2,
                "role": "Sales Representative",
                "monthly_sales": 10000,
                "market_share": 8,
                "customer_satisfaction": 75,
                "team": []
            },
            "modifiers": {
                "sales_multiplier": 1.0,
                "market_share_gain": 1.5,       # Łatwiej zdobywać market share
                "satisfaction_impact": 1.2,     # Większy wpływ na CSAT
                "task_difficulty": 0
            },
            "objectives": [
                {
                    "type": "monthly_sales",
                    "target": 60000,
                    "description": "Osiągnij 60k PLN miesięcznej sprzedaży",
                    "reward_money": 15000
                },
                {
                    "type": "market_share",
                    "target": 20,
                    "description": "Zdobądź 20% market share (dominacja!)",
                    "reward_money": 20000
                },
                {
                    "type": "customer_satisfaction",
                    "target": 85,
                    "description": "Osiągnij 85% satysfakcji klientów",
                    "reward_money": 10000
                },
                {
                    "type": "level",
                    "target": 3,
                    "description": "Awansuj na Senior Sales Rep",
                    "reward_money": 15000
                }
            ],
            "special_events": []
        },
        
        "team_builder": {
            "id": "team_builder",
            "name": "👥 Team Builder - Pierwszy Zespół",
            "description": "Zbuduj i prowadź swój pierwszy zespół sprzedażowy!",
            "icon": "🏗️",
            "difficulty": "hard",
            "initial_conditions": {
                "level": 4,
                "role": "Sales Team Leader",
                "monthly_sales": 0,
                "market_share": 12,
                "customer_satisfaction": 78,
                "team": [
                    {"role": "junior_rep", "name": "Ania", "productivity": 8000},
                    {"role": "sales_rep", "name": "Marek", "productivity": 20000},
                    {"role": "sales_rep", "name": "Kasia", "productivity": 22000}
                ]
            },
            "modifiers": {
                "sales_multiplier": 1.0,
                "market_share_gain": 1.0,
                "satisfaction_impact": 1.0,
                "task_difficulty": 5,           # Trudniejsze (management!)
                "team_turnover": 1.5            # Większe ryzyko odejścia ludzi
            },
            "objectives": [
                {
                    "type": "team_sales",
                    "target": 200000,
                    "description": "Zespół osiąga 200k PLN miesięcznej sprzedaży",
                    "reward_money": 30000
                },
                {
                    "type": "team_satisfaction",
                    "target": 80,
                    "description": "Satysfakcja zespołu na poziomie 80%+",
                    "reward_money": 20000
                },
                {
                    "type": "market_share",
                    "target": 18,
                    "description": "Zdobądź 18% market share jako zespół",
                    "reward_money": 25000
                },
                {
                    "type": "level",
                    "target": 5,
                    "description": "Awansuj na Area Sales Manager",
                    "reward_money": 25000
                }
            ],
            "special_events": ["team_conflict", "top_performer_leaving"]
        },
        
        "national_chains": {
            "id": "national_chains",
            "name": "🏢 National Chains Master",
            "description": "Wygraj kontrakty z największymi sieciami handlowymi w Polsce!",
            "icon": "💼",
            "difficulty": "very_hard",
            "initial_conditions": {
                "level": 6,
                "role": "District Sales Manager",
                "monthly_sales": 0,
                "market_share": 20,
                "customer_satisfaction": 82,
                "team": [
                    {"role": "team_leader", "name": "Piotr", "manages": 3},
                    {"role": "senior_rep", "name": "Anna"},
                    {"role": "senior_rep", "name": "Tomasz"},
                    {"role": "sales_rep", "name": "Ewa"},
                    {"role": "sales_rep", "name": "Jacek"},
                    {"role": "sales_rep", "name": "Magda"},
                    {"role": "junior_rep", "name": "Bartek"}
                ]
            },
            "modifiers": {
                "sales_multiplier": 2.0,        # Duże kontrakty = duża sprzedaż
                "market_share_gain": 2.0,       # National chains = massive impact
                "satisfaction_impact": 1.0,
                "task_difficulty": 10,          # Bardzo trudne negocjacje
                "contract_penalty": 1.5         # Wysokie penalties za błędy
            },
            "objectives": [
                {
                    "type": "team_sales",
                    "target": 800000,
                    "description": "Osiągnij 800k PLN miesięcznej sprzedaży zespołu",
                    "reward_money": 100000
                },
                {
                    "type": "market_share",
                    "target": 28,
                    "description": "Zdobądź 28% market share dzięki national chains",
                    "reward_money": 80000
                },
                {
                    "type": "key_account_wins",
                    "target": 3,
                    "description": "Wygraj 3 kontrakty z top national chains (Biedronka, Lidl, Kaufland)",
                    "reward_money": 120000
                },
                {
                    "type": "level",
                    "target": 7,
                    "description": "Awansuj na Regional Sales Manager",
                    "reward_money": 100000
                }
            ],
            "special_events": ["contract_breach", "competitor_poaching"]
        },
        
        "to_the_top": {
            "id": "to_the_top",
            "name": "🚀 To The Top - CSO Challenge",
            "description": "Ultimate challenge: Od Junior Rep do Chief Sales Officer! Najdłuższa ścieżka kariery.",
            "icon": "👑",
            "difficulty": "expert",
            "initial_conditions": {
                "level": 1,
                "role": "Junior Sales Representative",
                "monthly_sales": 0,
                "market_share": 0,
                "customer_satisfaction": 70,
                "team": []
            },
            "modifiers": {
                "sales_multiplier": 0.9,        # Trudniejsza sprzedaż
                "market_share_gain": 0.8,       # Wolniejszy wzrost
                "satisfaction_impact": 1.0,
                "task_difficulty": 15,          # Bardzo trudne zadania
                "advancement_threshold": 1.2    # 120% requirements do awansu
            },
            "objectives": [
                {
                    "type": "level",
                    "target": 10,
                    "description": "Osiągnij poziom 10: Chief Sales Officer!",
                    "reward_money": 500000
                },
                {
                    "type": "team_sales",
                    "target": 10000000,
                    "description": "Zespół osiąga 10M PLN rocznej sprzedaży",
                    "reward_money": 300000
                },
                {
                    "type": "market_share",
                    "target": 35,
                    "description": "Zdominuj rynek - 35% market share",
                    "reward_money": 200000
                },
                {
                    "type": "team_size",
                    "target": 100,
                    "description": "Zbuduj organizację 100+ osób",
                    "reward_money": 250000
                },
                {
                    "type": "customer_satisfaction",
                    "target": 92,
                    "description": "92% satysfakcji klientów (world-class!)",
                    "reward_money": 150000
                },
                {
                    "type": "career_speed",
                    "target": 24,
                    "description": "Osiągnij CSO w mniej niż 24 miesiące (2 lata)",
                    "reward_money": 1000000  # MASSIVE bonus!
                }
            ],
            "special_events": ["market_crash", "acquisition_offer", "board_challenge"]
        },
        "standard": {
            "id": "standard",
            "name": "Standard Start",
            "description": "Klasyczny start w branży FMCG - zrównoważone warunki początkowe.",
            "icon": "⚖️",
            "difficulty": "medium",
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.0,
                "revenue_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "employee_salary_multiplier": 1.0,
                "contract_difficulty_adjustment": 0
            },
            "objectives": [
                {
                    "type": "revenue_total",
                    "target": 1000000,
                    "description": "Osiągnij łącznie 1M PLN przychodu",
                    "reward_money": 50000
                }
            ],
            "special_events": []
        }
    },
    
    "pharma": {
        "lifetime": {
            "id": "lifetime",
            "name": "🌟 Lifetime Challenge",
            "description": "Tryb nieskończony bez celów - rywalizuj z innymi graczami o najwyższy wynik!",
            "icon": "♾️",
            "difficulty": "open",
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.0,
                "revenue_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "employee_salary_multiplier": 1.0,
                "contract_difficulty_adjustment": 0
            },
            "objectives": [],
            "special_events": [],
            "is_lifetime": True
        },
        "standard": {
            "id": "standard",
            "name": "Standard Start",
            "description": "Klasyczny start w branży farmaceutycznej - zrównoważone warunki początkowe.",
            "icon": "⚖️",
            "difficulty": "medium",
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.0,
                "revenue_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "employee_salary_multiplier": 1.0,
                "contract_difficulty_adjustment": 0
            },
            "objectives": [
                {
                    "type": "revenue_total",
                    "target": 1000000,
                    "description": "Osiągnij łącznie 1M PLN przychodu",
                    "reward_money": 50000
                }
            ],
            "special_events": []
        }
    },
    
    "banking": {
        "lifetime": {
            "id": "lifetime",
            "name": "🌟 Lifetime Challenge",
            "description": "Tryb nieskończony bez celów - rywalizuj z innymi graczami o najwyższy wynik!",
            "icon": "♾️",
            "difficulty": "open",
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.0,
                "revenue_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "employee_salary_multiplier": 1.0,
                "contract_difficulty_adjustment": 0
            },
            "objectives": [],
            "special_events": [],
            "is_lifetime": True
        },
        "standard": {
            "id": "standard",
            "name": "Standard Start",
            "description": "Klasyczny start w bankowości - zrównoważone warunki początkowe.",
            "icon": "⚖️",
            "difficulty": "medium",
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.0,
                "revenue_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "employee_salary_multiplier": 1.0,
                "contract_difficulty_adjustment": 0
            },
            "objectives": [
                {
                    "type": "revenue_total",
                    "target": 1000000,
                    "description": "Osiągnij łącznie 1M PLN przychodu",
                    "reward_money": 50000
                }
            ],
            "special_events": []
        }
    },
    
    "insurance": {
        "lifetime": {
            "id": "lifetime",
            "name": "🌟 Lifetime Challenge",
            "description": "Tryb nieskończony bez celów - rywalizuj z innymi graczami o najwyższy wynik!",
            "icon": "♾️",
            "difficulty": "open",
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.0,
                "revenue_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "employee_salary_multiplier": 1.0,
                "contract_difficulty_adjustment": 0
            },
            "objectives": [],
            "special_events": [],
            "is_lifetime": True
        },
        "standard": {
            "id": "standard",
            "name": "Standard Start",
            "description": "Klasyczny start w ubezpieczeniach - zrównoważone warunki początkowe.",
            "icon": "⚖️",
            "difficulty": "medium",
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.0,
                "revenue_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "employee_salary_multiplier": 1.0,
                "contract_difficulty_adjustment": 0
            },
            "objectives": [
                {
                    "type": "revenue_total",
                    "target": 1000000,
                    "description": "Osiągnij łącznie 1M PLN przychodu",
                    "reward_money": 50000
                }
            ],
            "special_events": []
        }
    },
    
    "automotive": {
        "lifetime": {
            "id": "lifetime",
            "name": "🌟 Lifetime Challenge",
            "description": "Tryb nieskończony bez celów - rywalizuj z innymi graczami o najwyższy wynik!",
            "icon": "♾️",
            "difficulty": "open",
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.0,
                "revenue_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "employee_salary_multiplier": 1.0,
                "contract_difficulty_adjustment": 0
            },
            "objectives": [],
            "special_events": [],
            "is_lifetime": True
        },
        "standard": {
            "id": "standard",
            "name": "Standard Start",
            "description": "Klasyczny start w motoryzacji - zrównoważone warunki początkowe.",
            "icon": "⚖️",
            "difficulty": "medium",
            "initial_conditions": {
                "money": 0,
                "reputation": 0,
                "employees": [],
                "office_type": "home_office"
            },
            "modifiers": {
                "reputation_gain_multiplier": 1.0,
                "revenue_multiplier": 1.0,
                "cost_multiplier": 1.0,
                "employee_salary_multiplier": 1.0,
                "contract_difficulty_adjustment": 0
            },
            "objectives": [
                {
                    "type": "revenue_total",
                    "target": 1000000,
                    "description": "Osiągnij łącznie 1M PLN przychodu",
                    "reward_money": 50000
                }
            ],
            "special_events": []
        }
    }
}


def get_scenario(industry_id: str, scenario_id: str) -> dict | None:
    """
    Pobiera dane scenariusza dla danej branży.
    
    Args:
        industry_id: Identyfikator branży (np. "consulting")
        scenario_id: Identyfikator scenariusza (np. "startup_mode")
    
    Returns:
        Słownik z danymi scenariusza lub None jeśli nie znaleziono
    """
    return SCENARIOS.get(industry_id, {}).get(scenario_id)


def get_available_scenarios(industry_id: str) -> dict:
    """
    Pobiera wszystkie dostępne scenariusze dla danej branży.
    
    Args:
        industry_id: Identyfikator branży
    
    Returns:
        Słownik scenariuszy dla branży
    """
    return SCENARIOS.get(industry_id, {})


def get_default_scenario_id(industry_id: str) -> str:
    """
    Zwraca domyślny scenariusz dla branży (dla backward compatibility).
    
    Args:
        industry_id: Identyfikator branży
    
    Returns:
        ID domyślnego scenariusza (zawsze "standard")
    """
    return "standard"
