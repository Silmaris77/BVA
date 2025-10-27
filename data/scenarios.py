"""
Definicje scenariuszy dla Business Games Suite

Każda branża może mieć wiele scenariuszy z różnymi warunkami startowymi,
modyfikatorami i celami do osiągnięcia.
"""

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
