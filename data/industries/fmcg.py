"""
FMCG Industry Configuration
Fast-Moving Consumer Goods - Sales Career Path

Career progression from Junior Sales Rep to Chief Sales Officer
"""

# =============================================================================
# INDUSTRY METADATA
# =============================================================================

INDUSTRY_INFO = {
    "id": "fmcg",
    "name": "FMCG Sales",
    "full_name": "Fast-Moving Consumer Goods",
    "icon": "🛒",
    "description": "Zbuduj karierę w sprzedaży FMCG - od Przedstawiciela Handlowego do Chief Sales Officer",
    "company_name": "FreshLife Poland",
    "company_description": "Polski oddział międzynarodowego koncernu FMCG. Lider w kategorii Personal Care, dynamiczny rozwój w Food i Home Care. Portfolio 12 produktów w 3 kategoriach."
}

# =============================================================================
# CAREER LEVELS - 10-poziomowa ścieżka kariery
# =============================================================================

CAREER_LEVELS = {
    1: {
        "role": "Junior Sales Representative",
        "role_short": "Jr Sales Rep",
        "icon": "🎯",
        "team_size": 0,
        "description": "Uczysz się podstaw sprzedaży FMCG. Obsługujesz małe sklepy detaliczne.",
        "responsibilities": [
            "Wizyt w małych sklepach (spożywczaki, kioski)",
            "Realizacja zamówień",
            "Podstawowa ekspozycja produktów",
            "Raportowanie sprzedaży"
        ],
        "required_metrics": {
            "monthly_sales": 10000,      # 10k PLN/miesiąc
            "market_share": 5,           # 5% market share
            "customer_satisfaction": 70  # 70% satisfaction
        }
    },
    2: {
        "role": "Sales Representative",
        "role_short": "Sales Rep",
        "icon": "💼",
        "team_size": 0,
        "description": "Samodzielny przedstawiciel handlowy. Zarządzasz własnym terytorium.",
        "responsibilities": [
            "Wizyt w średnich sklepach (Żabka, ABC, małe sieci)",
            "Negocjacje warunków handlowych",
            "Planowanie trasy i wizyt",
            "Analiza konkurencji"
        ],
        "required_metrics": {
            "monthly_sales": 25000,
            "market_share": 10,
            "customer_satisfaction": 75
        }
    },
    3: {
        "role": "Senior Sales Representative",
        "role_short": "Sr Sales Rep",
        "icon": "⭐",
        "team_size": 0,
        "description": "Ekspert sprzedaży. Obsługujesz kluczowych klientów i mentoruje juniorów.",
        "responsibilities": [
            "Obsługa Key Accounts (małe sieci regionalne)",
            "Wdrażanie promocji i kampanii",
            "Mentoring juniorów (nieformalne)",
            "Optymalizacja dystybucji"
        ],
        "required_metrics": {
            "monthly_sales": 50000,
            "market_share": 15,
            "customer_satisfaction": 80
        }
    },
    4: {
        "role": "Sales Team Leader",
        "role_short": "Team Leader",
        "icon": "👥",
        "team_size": 3,
        "description": "Zarządzasz małym zespołem przedstawicieli. Pierwsza rola managerska.",
        "responsibilities": [
            "Zarządzanie zespołem 3 sales repów",
            "Coaching i rozwój zespołu",
            "Planowanie territory coverage",
            "Realizacja team targets"
        ],
        "required_metrics": {
            "team_sales": 150000,        # Sales całego zespołu
            "market_share": 18,
            "team_satisfaction": 75      # Satysfakcja zespołu
        }
    },
    5: {
        "role": "Area Sales Manager",
        "role_short": "Area Manager",
        "icon": "🗺️",
        "team_size": 5,
        "description": "Zarządzasz obszarem sprzedaży (kilka miast). Średni management.",
        "responsibilities": [
            "Zarządzanie zespołem 5 sales repów",
            "Strategia sprzedaży dla obszaru",
            "Negocjacje z większymi sieciami",
            "Budżet marketingowy dla obszaru"
        ],
        "required_metrics": {
            "team_sales": 300000,
            "market_share": 20,
            "team_satisfaction": 80
        }
    },
    6: {
        "role": "District Sales Manager",
        "role_short": "District Manager",
        "icon": "🏙️",
        "team_size": 8,
        "description": "Zarządzasz dystryktem (województwo). Duże operacje sprzedażowe.",
        "responsibilities": [
            "Zarządzanie zespołem 8 osób (reps + 1 team leader)",
            "Strategia dystrybucji",
            "Obsługa sieci krajowych (Biedronka, Lidl, Kaufland)",
            "Trade marketing i promocje"
        ],
        "required_metrics": {
            "team_sales": 600000,
            "market_share": 22,
            "team_satisfaction": 82
        }
    },
    7: {
        "role": "Regional Sales Manager",
        "role_short": "Regional Manager",
        "icon": "🌍",
        "team_size": 15,
        "description": "Zarządzasz całym regionem (kilka województw). Senior management.",
        "responsibilities": [
            "Zarządzanie regionem (15+ osób)",
            "Strategia wzrostu i ekspansji",
            "Budżet regionalny (sales + marketing)",
            "Partnership z national chains"
        ],
        "required_metrics": {
            "team_sales": 1200000,
            "market_share": 25,
            "team_satisfaction": 85
        }
    },
    8: {
        "role": "Regional Sales Director",
        "role_short": "Regional Director",
        "icon": "💎",
        "team_size": 25,
        "description": "Dyrektor sprzedaży dla dużego regionu. Executive level.",
        "responsibilities": [
            "Strategia sprzedaży dla makro-regionu",
            "Zarządzanie budżetem milionowym",
            "Rekrutacja i rozwój managerów",
            "Board presentations"
        ],
        "required_metrics": {
            "team_sales": 2500000,
            "market_share": 28,
            "team_satisfaction": 87
        }
    },
    9: {
        "role": "Vice President of Sales",
        "role_short": "VP Sales",
        "icon": "👔",
        "team_size": 50,
        "description": "VP Sales dla całego kraju. C-level position.",
        "responsibilities": [
            "Strategia sprzedaży krajowej",
            "Zarządzanie całą strukturą sales (50+ osób)",
            "Alokacja budżetu",
            "M&A i partnerships"
        ],
        "required_metrics": {
            "team_sales": 5000000,
            "market_share": 30,
            "team_satisfaction": 90
        }
    },
    10: {
        "role": "Chief Sales Officer",
        "role_short": "CSO",
        "icon": "👑",
        "team_size": 100,
        "description": "Najwyższe stanowisko sprzedażowe. Członek zarządu.",
        "responsibilities": [
            "Wizja i strategia sales dla firmy",
            "Zarządzanie całą organizacją sprzedaży",
            "Ekspansja międzynarodowa",
            "Revenue growth & profitability"
        ],
        "required_metrics": {
            "team_sales": 10000000,
            "market_share": 35,
            "team_satisfaction": 92
        }
    }
}

# =============================================================================
# METRICS CONFIGURATION
# =============================================================================

METRICS_CONFIG = {
    "primary": {
        "name": "Monthly Sales",
        "short_name": "Sales",
        "icon": "💰",
        "unit": "PLN",
        "description": "Twoja/Twojego zespołu miesięczna sprzedaż",
        "display_format": "{:,} PLN",
        "color": "green"
    },
    "secondary": {
        "name": "Market Share",
        "short_name": "Market Share",
        "icon": "📊",
        "unit": "%",
        "description": "Udział w rynku w Twoim obszarze",
        "display_format": "{}%",
        "color": "blue"
    },
    "tertiary": {
        "name": "Customer Satisfaction",
        "short_name": "CSAT",
        "icon": "⭐",
        "unit": "%",
        "description": "Średnia satysfakcja klientów (sklepy, sieci)",
        "display_format": "{}%",
        "color": "yellow"
    },
    "team_metric": {  # Tylko dla poziomów 4+
        "name": "Team Satisfaction",
        "short_name": "Team SAT",
        "icon": "👥",
        "unit": "%",
        "description": "Satysfakcja i zaangażowanie Twojego zespołu",
        "display_format": "{}%",
        "color": "purple"
    }
}

# =============================================================================
# TASK CATEGORIES - Zamiast kontraktów, mamy "zadania zawodowe"
# =============================================================================

TASK_CATEGORIES = {
    "field_sales": {
        "name": "Sprzedaż Terenowa",
        "icon": "🚗",
        "description": "Wizyty w sklepach, negocjacje, zamówienia",
        "levels": [1, 2, 3, 4, 5, 6, 7]  # Dostępne dla tych poziomów
    },
    "key_accounts": {
        "name": "Obsługa Kluczowych Klientów",
        "icon": "🏢",
        "description": "Współpraca z sieciami handlowymi, duże kontrakty",
        "levels": [3, 4, 5, 6, 7, 8, 9, 10]
    },
    "team_management": {
        "name": "Zarządzanie Zespołem",
        "icon": "👥",
        "description": "Coaching, rekrutacja, rozwój zespołu",
        "levels": [4, 5, 6, 7, 8, 9, 10]
    },
    "trade_marketing": {
        "name": "Trade Marketing",
        "icon": "📢",
        "description": "Promocje, kampanie, planowanie merchandisingu",
        "levels": [2, 3, 4, 5, 6, 7, 8]
    },
    "strategy": {
        "name": "Strategia i Planowanie",
        "icon": "🎯",
        "description": "Business planning, budżety, ekspansja",
        "levels": [5, 6, 7, 8, 9, 10]
    },
    "crisis": {
        "name": "Zarządzanie Kryzysowe",
        "icon": "🚨",
        "description": "Product recall, konflikty, problemy operacyjne",
        "levels": [4, 5, 6, 7, 8, 9, 10]
    }
}

# =============================================================================
# TEAM MEMBERS - Dla poziomów 4+ (Team Leader i wyżej)
# =============================================================================

TEAM_MEMBER_TYPES = {
    "junior_rep": {
        "role": "Junior Sales Rep",
        "icon": "🎯",
        "base_salary": 4000,  # PLN/miesiąc
        "productivity": 8000,  # Średnia sprzedaż/miesiąc
        "skill_level": "beginner",
        "requires_coaching": True
    },
    "sales_rep": {
        "role": "Sales Representative",
        "icon": "💼",
        "base_salary": 5500,
        "productivity": 20000,
        "skill_level": "intermediate",
        "requires_coaching": False
    },
    "senior_rep": {
        "role": "Senior Sales Rep",
        "icon": "⭐",
        "base_salary": 7000,
        "productivity": 40000,
        "skill_level": "advanced",
        "requires_coaching": False
    },
    "team_leader": {
        "role": "Team Leader",
        "icon": "👥",
        "base_salary": 9000,
        "productivity": 0,  # Manager, nie sprzedaje sam
        "skill_level": "management",
        "manages_team": True
    }
}

# =============================================================================
# ADVANCEMENT FORMULA
# =============================================================================

def can_advance_to_next_level(current_level: int, metrics: dict, career_stage: str) -> tuple[bool, str]:
    """
    Sprawdza czy gracz może awansować na następny poziom
    
    Args:
        current_level: Obecny poziom (1-10)
        metrics: Dict z aktualnymi metrykami gracza
        career_stage: "ic", "manager", "director"
    
    Returns:
        (can_advance, reason)
    """
    if current_level >= 10:
        return False, "Osiągnąłeś najwyższy poziom!"
    
    next_level = current_level + 1
    requirements = CAREER_LEVELS[next_level]["required_metrics"]
    
    # Sprawdź metryki w zależności od career stage
    if career_stage in ["ic"]:  # Individual Contributor (1-3)
        checks = [
            (metrics.get("monthly_sales", 0) >= requirements["monthly_sales"], 
             f"Monthly Sales: {metrics.get('monthly_sales', 0):,} / {requirements['monthly_sales']:,} PLN"),
            (metrics.get("market_share", 0) >= requirements["market_share"],
             f"Market Share: {metrics.get('market_share', 0)}% / {requirements['market_share']}%"),
            (metrics.get("customer_satisfaction", 0) >= requirements["customer_satisfaction"],
             f"Customer Satisfaction: {metrics.get('customer_satisfaction', 0)}% / {requirements['customer_satisfaction']}%")
        ]
    else:  # Manager/Director (4+)
        checks = [
            (metrics.get("team_sales", 0) >= requirements["team_sales"],
             f"Team Sales: {metrics.get('team_sales', 0):,} / {requirements['team_sales']:,} PLN"),
            (metrics.get("market_share", 0) >= requirements["market_share"],
             f"Market Share: {metrics.get('market_share', 0)}% / {requirements['market_share']}%"),
            (metrics.get("team_satisfaction", 0) >= requirements.get("team_satisfaction", 0),
             f"Team Satisfaction: {metrics.get('team_satisfaction', 0)}% / {requirements.get('team_satisfaction', 0)}%")
        ]
    
    # Sprawdź wszystkie wymagania
    failed_checks = [reason for passed, reason in checks if not passed]
    
    if failed_checks:
        return False, "Wymagania do awansu:\n" + "\n".join(f"❌ {r}" for r in failed_checks)
    
    return True, f"Gratulacje! Spełniasz wymagania na poziom {next_level}: {CAREER_LEVELS[next_level]['role']}! 🎉"

# =============================================================================
# CAREER STAGE HELPER
# =============================================================================

def get_career_stage(level: int) -> str:
    """Zwraca career stage na podstawie poziomu"""
    if level <= 3:
        return "ic"  # Individual Contributor
    elif level <= 7:
        return "manager"
    else:
        return "director"

# =============================================================================
# GAME CONFIG
# =============================================================================

FMCG_GAME_CONFIG = {
    "starting_level": 1,
    "starting_role": "Junior Sales Representative",
    "max_level": 10,
    "tasks_per_day": {
        1: 1,   # Level 1: 1 zadanie/dzień
        2: 1,
        3: 2,   # Level 3: 2 zadania/dzień (bardziej doświadczony)
        4: 2,   # Team Leader: mniej hands-on
        5: 2,
        6: 3,
        7: 3,
        8: 3,
        9: 4,
        10: 5
    },
    "currency": "PLN",
    "performance_review_frequency": "quarterly",  # Co 3 miesiące review
    "bonus_multipliers": {
        "exceeds_target": 1.5,      # 150% bonusu jeśli przekroczysz target
        "meets_target": 1.0,        # 100% bonusu
        "below_target": 0.5         # 50% bonusu
    }
}
