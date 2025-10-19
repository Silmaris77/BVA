"""
Random Events - Zdarzenia losowe dla Business Games
Dodają nieprzewidywalność i emocje do rozgrywki
"""

RANDOM_EVENTS = {
    # =========================================================================
    # POZYTYWNE ZDARZENIA (40%)
    # =========================================================================
    
    "bonus_payment": {
        "type": "positive",
        "emoji": "💰",
        "title": "Niespodziewana Premia!",
        "description": "Jeden z Twoich wcześniejszych klientów był tak zadowolony z rezultatów, że postanowił wysłać dodatkową premię.",
        "flavor_text": "\"Wasza pomoc przyniosła lepsze rezultaty niż się spodziewaliśmy. To mała rekompensata!\" - CEO TechCorp",
        "effects": {
            "coins": 500,
            "reputation": 2
        },
        "rarity": "common",
        "conditions": {
            "min_contracts": 1,
            "min_reputation": 0
        }
    },
    
    "media_coverage": {
        "type": "positive",
        "emoji": "📰",
        "title": "Artykuł w Prasie Branżowej",
        "description": "Renomowany portal biznesowy napisał pochlebny artykuł o Twojej firmie. To świetna reklama!",
        "flavor_text": "\"Nowa gwiazda na rynku doradztwa - poznaj firmę, która革 zmienia zasady gry.\"",
        "effects": {
            "reputation": 10
        },
        "rarity": "uncommon",
        "conditions": {
            "min_contracts": 3,
            "min_reputation": 20
        }
    },
    
    "referral_bonus": {
        "type": "positive",
        "emoji": "🤝",
        "title": "Polecenie od Klienta",
        "description": "Zadowolony klient polecił Twoją firmę swojemu partnerowi biznesowemu. Następny kontrakt będzie lepiej płatny!",
        "flavor_text": "\"Jeśli szukacie najlepszych - oni są warci każdej złotówki!\"",
        "effects": {
            "next_contract_bonus": 1.5,  # 50% bonus do następnego kontraktu
            "reputation": 3
        },
        "rarity": "common",
        "conditions": {
            "min_contracts": 2,
            "min_avg_rating": 4.0
        }
    },
    
    "free_training": {
        "type": "positive",
        "emoji": "🎓",
        "title": "Darmowe Szkolenie",
        "description": "Twój zespół otrzymał zaproszenie na ekskluzywne, darmowe szkolenie. Produktywność wzrasta!",
        "flavor_text": "\"Inwestycja w ludzi to najlepsza inwestycja.\"",
        "effects": {
            "capacity_boost": 1,  # +1 do pojemności
            "duration_days": 3
        },
        "rarity": "uncommon",
        "conditions": {
            "min_contracts": 5,
            "has_employees": True
        }
    },
    
    "energy_burst": {
        "type": "positive",
        "emoji": "⚡",
        "title": "Burst Energii!",
        "description": "Zespół jest zmotywowany i pełen energii! Następne kontrakty zrealizujecie szybciej.",
        "flavor_text": "\"Czasem wszystko się układa i praca idzie jak z płatka!\"",
        "effects": {
            "deadline_extension": 1,  # +1 dzień na każdy aktywny kontrakt
            "boost_count": 3  # Na następne 3 kontrakty
        },
        "rarity": "rare",
        "conditions": {
            "min_contracts": 3
        }
    },
    
    # =========================================================================
    # NEUTRALNE ZDARZENIA (30%) - Wymagają decyzji gracza
    # =========================================================================
    
    "risky_offer": {
        "type": "neutral",
        "emoji": "🎰",
        "title": "Ryzykowna Oferta",
        "description": "Klient oferuje bardzo trudny kontrakt, ale nagroda jest podwojona. Czy podejmiesz wyzwanie?",
        "flavor_text": "\"To będzie wymagające, ale jeśli dasz radę - zapłacę double.\"",
        "choices": [
            {
                "text": "✅ Przyjmuję wyzwanie!",
                "effects": {
                    "add_risky_contract": True,
                    "reputation": 5
                }
            },
            {
                "text": "❌ Dziękuję, nie tym razem",
                "effects": {
                    "reputation": 1  # Bonus za rozsądną decyzję
                }
            }
        ],
        "rarity": "uncommon",
        "conditions": {
            "min_contracts": 5,
            "min_reputation": 30
        }
    },
    
    "renegotiation": {
        "type": "neutral",
        "emoji": "🔄",
        "title": "Prośba o Renegocjację",
        "description": "Klient z aktywnym kontraktem chce renegocjować warunki: -20% nagrody, ale +3 dni na realizację.",
        "flavor_text": "\"Mamy problem z budżetem, ale możemy dać więcej czasu...\"",
        "choices": [
            {
                "text": "✅ Zgadzam się",
                "effects": {
                    "modify_active_contract": True,
                    "reward_multiplier": 0.8,
                    "time_bonus": 3
                }
            },
            {
                "text": "❌ Trzymam się ustaleń",
                "effects": {
                    "reputation": 2  # Za profesjonalizm
                }
            }
        ],
        "rarity": "common",
        "conditions": {
            "has_active_contracts": True
        }
    },
    
    "audit": {
        "type": "neutral",
        "emoji": "📊",
        "title": "Dobrowolny Audyt",
        "description": "Organizacja branżowa oferuje certyfikujący audyt. Kosztuje 200 monet, ale zwiększy Twoją reputację.",
        "flavor_text": "\"Certyfikat jakości to inwestycja w przyszłość.\"",
        "choices": [
            {
                "text": "✅ Przejdźmy audyt",
                "effects": {
                    "coins": -200,
                    "reputation": 8
                }
            },
            {
                "text": "❌ Nie teraz",
                "effects": None
            }
        ],
        "rarity": "uncommon",
        "conditions": {
            "min_coins": 300,
            "min_contracts": 3
        }
    },
    
    # =========================================================================
    # NEGATYWNE ZDARZENIA (30%)
    # =========================================================================
    
    "sick_employee": {
        "type": "negative",
        "emoji": "🤒",
        "title": "Pracownik Zachorował",
        "description": "Ktoś z Twojego zespołu zachorował i musi zostać w domu. Pojemność dzienną zmniejszona na 2 dni.",
        "flavor_text": "\"Przykro mi, ale czuję się fatalnie... Muszę zostać w łóżku.\"",
        "effects": {
            "capacity_penalty": -1,
            "duration_days": 2
        },
        "rarity": "common",
        "conditions": {
            "has_employees": True
        }
    },
    
    "equipment_failure": {
        "type": "negative",
        "emoji": "💸",
        "title": "Awaria Sprzętu",
        "description": "Twój główny komputer się zepsuł. Naprawy kosztowały 300 monet.",
        "flavor_text": "\"Murphy's Law: Wszystko co może się popsuć, popsuje się w najmniej odpowiednim momencie.\"",
        "effects": {
            "coins": -300
        },
        "rarity": "common",
        "conditions": {
            "min_coins": 400,
            "min_contracts": 2
        }
    },
    
    "bad_review": {
        "type": "negative",
        "emoji": "📉",
        "title": "Negatywna Recenzja",
        "description": "Niezadowolony klient napisał negatywną opinię na forum branżowym. Twoja reputacja ucierpiała.",
        "flavor_text": "\"Nie polecam - przeciętna obsługa, zawyżone ceny...\" [⭐⭐☆☆☆]",
        "effects": {
            "reputation": -5
        },
        "rarity": "uncommon",
        "conditions": {
            "min_contracts": 3,
            "has_low_rated_contract": True  # Jeśli ostatnio dostał ocenę ≤2
        }
    },
    
    "deadline_pressure": {
        "type": "negative",
        "emoji": "⏰",
        "title": "Skrócony Deadline",
        "description": "Klient zmienił plany i potrzebuje rezultatów szybciej. Jeden z aktywnych kontraktów ma -1 dzień na realizację!",
        "flavor_text": "\"Przepraszam, ale mamy nagłą zmianę priorytetów. Potrzebujemy tego ASAP!\"",
        "effects": {
            "deadline_reduction": -1  # -1 dzień od losowego aktywnego kontraktu
        },
        "rarity": "uncommon",
        "conditions": {
            "has_active_contracts": True
        }
    },
    
    "contract_stolen": {
        "type": "negative",
        "emoji": "🚫",
        "title": "Konkurencja Podbiła Ofertę",
        "description": "Inna firma złożyła lepszą ofertę i jeden z dostępnych kontraktów zniknął z puli.",
        "flavor_text": "\"Przepraszamy, ale zdecydowaliśmy się na innego wykonawcę...\"",
        "effects": {
            "remove_contract_from_pool": True
        },
        "rarity": "rare",
        "conditions": {
            "min_available_contracts": 3
        }
    }
}

# Rozkład częstotliwości według typu
EVENT_TYPE_WEIGHTS = {
    "positive": 40,   # 40%
    "neutral": 30,    # 30%
    "negative": 30    # 30%
}

# Rozkład według rzadkości
RARITY_WEIGHTS = {
    "common": 60,      # 60%
    "uncommon": 30,    # 30%
    "rare": 10         # 10%
}
