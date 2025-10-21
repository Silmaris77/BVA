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
    
    # Placeholdery dla pozostałych branż - wypełnisz jak będziesz je implementować
    "fmcg": {
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
