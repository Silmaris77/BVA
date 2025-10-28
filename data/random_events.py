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
            "min_contracts": 3,
            "has_active_contracts": True
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
    
    "minor_equipment_issue": {
        "type": "negative",
        "emoji": "💸",
        "title": "Drobna Awaria Sprzętu",
        "description": "Twój komputer potrzebuje drobnych napraw. Kosztowało to 300 monet.",
        "flavor_text": "\"Murphy's Law: Wszystko co może się popsuć, popsuje się w najmniej odpowiednim momencie.\"",
        "effects": {
            "coins": -300
        },
        "rarity": "common",
        "conditions": {
            "min_coins": 400
        }
    },
    
    "internet_outage": {
        "type": "negative",
        "emoji": "📡",
        "title": "Awaria Internetu",
        "description": "Twój internet padł na cały dzień. Straciłeś cenny czas i musiałeś pracować z kawiarni.",
        "flavor_text": "\"No signal... Provider nie odbiera telefonu. Świetnie.\"",
        "effects": {
            "coins": -150
        },
        "rarity": "common",
        "conditions": {}
    },
    
    "coffee_spill": {
        "type": "negative",
        "emoji": "☕",
        "title": "Rozlana Kawa na Klawiaturze",
        "description": "Klasyka. Kawa na klawiaturze. Nowa klawiatura to koszt i strata czasu.",
        "flavor_text": "\"Nooo nie... Akurat teraz?!\"",
        "effects": {
            "coins": -200
        },
        "rarity": "common",
        "conditions": {
            "min_coins": 250
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
        "rarity": "uncommon",
        "conditions": {
            "min_available_contracts": 3,
            "min_contracts": 1  # Wymaga przynajmniej 1 ukończonego kontraktu
        }
    },
    
    # =========================================================================
    # NOWE WYDARZENIA - POZYTYWNE
    # =========================================================================
    
    "viral_recommendation": {
        "type": "positive",
        "emoji": "🚀",
        "title": "Viralna Rekomendacja!",
        "description": "Twój post na LinkedIn o jednym z projektów stał się viralem! Setki firm chce z Tobą współpracować.",
        "flavor_text": "\"Ten case study jest genialny! Musimy ich zatrudnić!\" - komentarze w social media",
        "effects": {
            "coins": 800,
            "reputation": 15
        },
        "rarity": "rare",
        "conditions": {
            "min_contracts": 5,
            "min_reputation": 40
        }
    },
    
    "award_nomination": {
        "type": "positive",
        "emoji": "🏆",
        "title": "Nominacja do Nagrody Branżowej",
        "description": "Twoja firma została nominowana do prestiżowej nagrody 'Consulting Firm of the Year'!",
        "flavor_text": "\"W finale 5 najlepszych firm konsultingowych w kraju!\"",
        "effects": {
            "reputation": 20,
            "coins": 300
        },
        "rarity": "rare",
        "conditions": {
            "min_contracts": 10,
            "min_reputation": 60
        }
    },
    
    "talent_acquisition": {
        "type": "positive",
        "emoji": "⭐",
        "title": "Top Talent Chce do Ciebie Dołączyć",
        "description": "Uznany ekspert w branży usłyszał o Twojej firmie i chce u Ciebie pracować. Następny pracownik będzie taniej!",
        "flavor_text": "\"Słyszałem same dobre rzeczy o Waszej kulturze pracy. Chciałbym się przyłączyć!\"",
        "effects": {
            "reputation": 8
        },
        "rarity": "uncommon",
        "conditions": {
            "min_contracts": 5,
            "has_employees": True
        }
    },
    
    "partnership_offer": {
        "type": "positive",
        "emoji": "🤝",
        "title": "Oferta Partnerstwa Strategicznego",
        "description": "Duża firma konsultingowa proponuje partnership. Dostaniesz dostęp do ich sieci klientów!",
        "flavor_text": "\"Możemy razem zrobić wielkie rzeczy. Co powiesz na współpracę?\"",
        "effects": {
            "coins": 1000,
            "reputation": 12
        },
        "rarity": "rare",
        "conditions": {
            "min_contracts": 8,
            "min_reputation": 50
        }
    },
    
    "grant_approved": {
        "type": "positive",
        "emoji": "💎",
        "title": "Grant na Rozwój Otrzymany!",
        "description": "Twój wniosek o grant z programu wspierania innowacyjnych firm został zaakceptowany!",
        "flavor_text": "\"Gratulujemy! Komitet docenił innowacyjność Waszego podejścia.\"",
        "effects": {
            "coins": 1500
        },
        "rarity": "rare",
        "conditions": {
            "min_contracts": 7,
            "min_reputation": 45
        }
    },
    
    "early_completion_bonus": {
        "type": "positive",
        "emoji": "⚡",
        "title": "Bonus za Szybkość",
        "description": "Ukończyłeś projekt wcześniej niż przewidywano. Klient dorzuca bonus i przedłuża deadline wszystkich aktywnych kontraktów!",
        "flavor_text": "\"Niesamowite! Czekaliśmy 2 tygodnie, a Wy skończyliście w 3 dni!\"",
        "effects": {
            "coins": 600,
            "deadline_extension": 2,
            "boost_count": 2
        },
        "rarity": "uncommon",
        "conditions": {
            "has_active_contracts": True,
            "min_avg_rating": 4.0
        }
    },
    
    # =========================================================================
    # NOWE WYDARZENIA - NEUTRALNE (Z WYBORAMI)
    # =========================================================================
    
    "conference_invitation": {
        "type": "neutral",
        "emoji": "🎤",
        "title": "Zaproszenie na Konferencję",
        "description": "Zostałeś zaproszony jako prelegent na dużą konferencję branżową. Co robisz?",
        "flavor_text": "\"Chcielibyśmy, żebyś podzielił się swoimi doświadczeniami z 500 uczestnikami...\"",
        "choices": [
            {
                "text": "Przyjmuję i prezentuję case study",
                "effects": {
                    "reputation": 15,
                    "coins": -200  # Koszt przygotowania
                }
            },
            {
                "text": "Odmawiam - mam zbyt dużo pracy",
                "effects": {
                    "capacity_boost": 1,
                    "duration_days": 3
                }
            },
            {
                "text": "Wysyłam swojego pracownika",
                "effects": {
                    "reputation": 8,
                    "coins": -100
                }
            }
        ],
        "rarity": "uncommon",
        "conditions": {
            "min_contracts": 6,
            "min_reputation": 40
        }
    },
    
    "equity_offer": {
        "type": "neutral",
        "emoji": "📊",
        "title": "Inwestor Chce Kupić Udziały",
        "description": "Angel investor oferuje dużą gotówkę w zamian za 30% udziałów w Twojej firmie. Co decydujesz?",
        "flavor_text": "\"Widzę potencjał. 50,000 zł za 30% firmy. Deal?\"",
        "choices": [
            {
                "text": "Sprzedaję udziały - biorę cash",
                "effects": {
                    "coins": 5000,
                    "reputation": -5  # Niektórzy mówią, że 'wyprzedałeś się'
                }
            },
            {
                "text": "Odmawiam - zachowuję kontrolę",
                "effects": {
                    "reputation": 10  # Szacunek za niezależność
                }
            },
            {
                "text": "Negocjuję lepsze warunki (15%)",
                "effects": {
                    "coins": 2500,
                    "reputation": 5
                }
            }
        ],
        "rarity": "rare",
        "conditions": {
            "min_contracts": 10,
            "min_reputation": 55
        }
    },
    
    "pro_bono_request": {
        "type": "neutral",
        "emoji": "❤️",
        "title": "Prośba o Pro Bono",
        "description": "Lokalna NGO prosi o darmowe wsparcie w reorganizacji. To zajmie czas, ale może być PR-owo cenne.",
        "flavor_text": "\"Nie mamy budżetu, ale naprawdę potrzebujemy pomocy ekspertów...\"",
        "choices": [
            {
                "text": "Pomagam za darmo",
                "effects": {
                    "reputation": 12,
                    "capacity_penalty": 1,
                    "duration_days": 5
                }
            },
            {
                "text": "Odmawiam grzecznie",
                "effects": {
                    "coins": 0  # Neutralne
                }
            },
            {
                "text": "Oferuję rabat 50%",
                "effects": {
                    "coins": 300,
                    "reputation": 6,
                    "capacity_penalty": 1,
                    "duration_days": 3
                }
            }
        ],
        "rarity": "common",
        "conditions": {
            "min_contracts": 3
        }
    },
    
    "merger_proposal": {
        "type": "neutral",
        "emoji": "🔗",
        "title": "Propozycja Fuzji",
        "description": "Podobna firma proponuje połączenie sił. Razem bylibyście silniejsi, ale stracisz część autonomii.",
        "flavor_text": "\"Razem mamy 15 pracowników i moglibyśmy brać większe projekty!\"",
        "choices": [
            {
                "text": "Łączę firmy",
                "effects": {
                    "coins": 2000,
                    "reputation": 15,
                    "capacity_boost": 2,
                    "duration_days": 30
                }
            },
            {
                "text": "Odrzucam ofertę",
                "effects": {
                    "reputation": 5  # Szacunek za pewność siebie
                }
            },
            {
                "text": "Proponuję luźną współpracę zamiast fuzji",
                "effects": {
                    "coins": 800,
                    "reputation": 8,
                    "next_contract_bonus": 1.2
                }
            }
        ],
        "rarity": "rare",
        "conditions": {
            "min_contracts": 12,
            "has_employees": True
        }
    },
    
    # =========================================================================
    # NOWE WYDARZENIA - NEGATYWNE
    # =========================================================================
    
    "employee_burnout": {
        "type": "negative",
        "emoji": "😰",
        "title": "Wypalenie Pracownika",
        "description": "Jeden z Twoich kluczowych pracowników jest wypalony. Potrzebujesz dać mu urlop lub ryzykujesz jego odejście.",
        "flavor_text": "\"Nie mogę już więcej... Albo wezmę tydzień wolnego, albo odchodzę.\"",
        "effects": {
            "capacity_penalty": 1,
            "duration_days": 7,
            "coins": -500  # Koszt zastępstwa/urlopu
        },
        "rarity": "uncommon",
        "conditions": {
            "has_employees": True,
            "has_active_contracts": True
        }
    },
    
    "tax_audit": {
        "type": "negative",
        "emoji": "🔍",
        "title": "Kontrola Skarbowa",
        "description": "Urząd skarbowy przeprowadza kontrolę. Musisz zatrudnić księgowego i poświęcić czas na dokumentację.",
        "flavor_text": "\"Dzień dobry, jesteśmy z Urzędu Skarbowego. Kontrola rutynowa.\"",
        "effects": {
            "coins": -800,
            "capacity_penalty": 1,
            "duration_days": 5
        },
        "rarity": "uncommon",
        "conditions": {
            "min_contracts": 5,
            "min_coins": 1000
        }
    },
    
    "negative_review_online": {
        "type": "negative",
        "emoji": "😡",
        "title": "Negatywna Recenzja Online",
        "description": "Niezadowolony (były) klient napisał ostrą recenzję na Glassdoor. Twoja reputacja oberwała.",
        "flavor_text": "\"1/5 gwiazdek - nie polecam. Nieprofesjonalni i nieskuteczni!\"",
        "effects": {
            "reputation": -15,
            "coins": -300  # Koszt PR crisis management
        },
        "rarity": "uncommon",
        "conditions": {
            "min_contracts": 4,
            "has_low_rated_contract": True
        }
    },
    
    "equipment_failure": {
        "type": "negative",
        "emoji": "💻",
        "title": "Awaria Sprzętu",
        "description": "Twój komputer/serwer padł w najgorszym momencie. Musisz kupić nowy i odzyskać dane. To kosztuje czas i pieniądze.",
        "flavor_text": "\"BSOD... Nie, nie, nie! Backup? Jaki backup?!\"",
        "effects": {
            "coins": -1000,
            "deadline_reduction": -1  # Skrócenie deadline o 1 dzień dla losowego kontraktu
        },
        "rarity": "rare",
        "conditions": {
            "has_active_contracts": True
        }
    },
    
    "client_bankruptcy": {
        "type": "negative",
        "emoji": "💔",
        "title": "Bankructwo Klienta",
        "description": "Firma, z którą właśnie podpisałeś duży kontrakt, ogłosiła bankructwo. Nie dostaniesz zapłaty.",
        "flavor_text": "\"Z przykrością informujemy, że złożyliśmy wniosek o upadłość...\"",
        "effects": {
            "coins": -1200,
            "reputation": -5
        },
        "rarity": "rare",
        "conditions": {
            "has_active_contracts": True,
            "min_contracts": 3
        }
    },
    
    "key_employee_leaves": {
        "type": "negative",
        "emoji": "👋",
        "title": "Odejście Kluczowego Pracownika",
        "description": "Twój najlepszy konsultant dostał ofertę od konkurencji i odchodzi. Tracisz capacity i musisz przeszkolić zastępstwo.",
        "flavor_text": "\"Doceniam wszystko, ale dostałem ofertę której nie mogę odmówić...\"",
        "effects": {
            "capacity_penalty": 2,
            "duration_days": 14,
            "coins": -600,  # Koszt rekrutacji
            "reputation": -8
        },
        "rarity": "rare",
        "conditions": {
            "has_employees": True,
            "min_contracts": 8
        }
    },
    
    "cyber_attack": {
        "type": "negative",
        "emoji": "🔒",
        "title": "Atak Hakerski",
        "description": "Padłeś ofiarą ransomware. Musisz zapłacić za odzyskanie danych lub stracić wszystko i zacząć od nowa.",
        "flavor_text": "\"Your files have been encrypted. Pay 2 BTC to decrypt...\"",
        "effects": {
            "coins": -1500,
            "reputation": -10,
            "capacity_penalty": 2,
            "duration_days": 7
        },
        "rarity": "rare",
        "conditions": {
            "min_contracts": 6,
            "min_coins": 2000
        }
    },
    
    "lawsuit_threat": {
        "type": "negative",
        "emoji": "⚖️",
        "title": "Groźba Pozwu Sądowego",
        "description": "Były klient grozi pozwem, twierdząc że Twoje porady spowodowały straty. Musisz zatrudnić prawnika.",
        "flavor_text": "\"Otrzymacie wezwanie do sądu. Mój prawnik już przygotowuje dokumenty...\"",
        "effects": {
            "coins": -1000,
            "reputation": -12,
            "capacity_penalty": 1,
            "duration_days": 10
        },
        "rarity": "rare",
        "conditions": {
            "min_contracts": 7,
            "min_coins": 1500
        }
    },
    
    # =========================================================================
    # WYDARZENIA DLA POCZĄTKUJĄCYCH (Poziom 1)
    # =========================================================================
    
    "first_client_review": {
        "type": "positive",
        "emoji": "⭐",
        "title": "Pierwsza Świetna Opinia!",
        "description": "Twój pierwszy klient zostawił entuzjastyczną opinię w internecie. Nowi klienci już dzwonią!",
        "flavor_text": "\"Profesjonalizm i zaangażowanie na najwyższym poziomie. Gorąco polecam!\" - ⭐⭐⭐⭐⭐",
        "effects": {
            "reputation": 5,
            "coins": 200
        },
        "rarity": "common",
        "conditions": {
            "max_level": 2,
            "min_contracts": 1,
            "min_avg_rating": 4.0
        }
    },
    
    "beginner_luck": {
        "type": "positive",
        "emoji": "🍀",
        "title": "Szczęście Początkującego",
        "description": "Natrafiłeś na klienta, który akurat pilnie potrzebuje pomocy i jest gotów zapłacić więcej!",
        "flavor_text": "\"Jesteście wolni? Potrzebuję kogoś NATYCHMIAST. Zapłacę 30% więcej!\"",
        "effects": {
            "next_contract_bonus": 1.3,
            "reputation": 2
        },
        "rarity": "uncommon",
        "conditions": {
            "max_level": 2,
            "min_contracts": 0
        }
    },
    
    "mentor_help": {
        "type": "positive",
        "emoji": "👨‍🏫",
        "title": "Nieoczekiwana Pomoc Mentora",
        "description": "Doświadczony konsultant zauważył Twój potencjał i oferuje bezpłatną poradę, która przyspiesza realizację kontraktu.",
        "flavor_text": "\"Pamiętam swoje początki... Pozwól, że ci pokażę kilka trików!\"",
        "effects": {
            "deadline_extension": 2,
            "capacity_boost": 1,
            "duration_days": 2
        },
        "rarity": "uncommon",
        "conditions": {
            "max_level": 2,
            "min_contracts": 2,
            "has_active_contracts": True
        }
    },
    
    "free_coffee": {
        "type": "positive",
        "emoji": "☕",
        "title": "Darmowa Kawa od Klienta",
        "description": "Klient był pod wrażeniem Twojej pracy i wysłał voucher na miesiąc darmowej kawy. Mała rzecz, a cieszy!",
        "flavor_text": "\"Dziękuję za świetną robotę! To małe podziękowan ie od nas.\"",
        "effects": {
            "reputation": 1,
            "coins": 100
        },
        "rarity": "common",
        "conditions": {
            "max_level": 2,
            "min_contracts": 1
        }
    },
    
    "networking_event": {
        "type": "neutral",
        "emoji": "🎤",
        "title": "Zaproszenie na Wydarzenie Networkingowe",
        "description": "Lokalna izba biznesu organizuje wydarzenie networkingowe. Udział kosztuje 150 monet, ale możesz poznać nowych klientów.",
        "flavor_text": "\"W biznesie chodzi o ludzi. Przyjdź, poznaj innych przedsiębiorców!\"",
        "choices": [
            {
                "text": "✅ Idę! Networking to podstawa",
                "effects": {
                    "coins": -150,
                    "reputation": 4,
                    "next_contract_bonus": 1.2
                }
            },
            {
                "text": "❌ Za drogo, skupiam się na pracy",
                "effects": {
                    "capacity_boost": 1,
                    "duration_days": 1
                }
            }
        ],
        "rarity": "common",
        "conditions": {
            "max_level": 2,
            "min_coins": 200,
            "min_contracts": 1
        }
    },
    
    "online_course": {
        "type": "neutral",
        "emoji": "💻",
        "title": "Kurs Online ze Zniżką",
        "description": "Platforma edukacyjna oferuje 50% zniżki na kurs, który może poprawić Twoje umiejętności. Kosztuje 200 monet.",
        "flavor_text": "\"Zainwestuj w siebie - to najlepsza inwestycja!\"",
        "choices": [
            {
                "text": "✅ Kupuję kurs",
                "effects": {
                    "coins": -200,
                    "capacity_boost": 2,
                    "duration_days": 5
                }
            },
            {
                "text": "❌ Nauczę się sam/sama",
                "effects": {
                    "reputation": 1
                }
            }
        ],
        "rarity": "common",
        "conditions": {
            "max_level": 3,
            "min_coins": 250,
            "min_contracts": 2
        }
    },
    
    "computer_slowdown": {
        "type": "negative",
        "emoji": "🐌",
        "title": "Komputer Zwalnia",
        "description": "Twój komputer zaczyna przytykać i wymaga aktualizacji systemu. Tracisz czas na instalację.",
        "flavor_text": "\"Windows Update: Instalowanie 1 z 247 aktualizacji... Nie wyłączaj komputera.\"",
        "effects": {
            "capacity_penalty": -1,
            "duration_days": 1
        },
        "rarity": "common",
        "conditions": {
            "max_level": 3,
            "min_contracts": 1
        }
    },
    
    "client_confusion": {
        "type": "negative",
        "emoji": "❓",
        "title": "Nieporozumienie z Klientem",
        "description": "Klient źle zrozumiał zakres usługi i oczekuje więcej pracy. Musisz poświęcić dodatkowy czas na wyjaśnienia.",
        "flavor_text": "\"Jak to nie wchodzi w cenę?! Myślałem, że wszystko jest zawarte...\"",
        "effects": {
            "capacity_penalty": -1,
            "duration_days": 2,
            "reputation": -2
        },
        "rarity": "common",
        "conditions": {
            "max_level": 2,
            "min_contracts": 1
        }
    },
    
    "invoice_delay": {
        "type": "negative",
        "emoji": "🧾",
        "title": "Opóźniona Płatność",
        "description": "Klient obiecał zapłacić natychmiast, ale faktura \"zaginęła w systemie\". Musisz czekać na pieniądze.",
        "flavor_text": "\"Księgowość mówi, że nie dostali faktury... Możesz wysłać ponownie?\"",
        "effects": {
            "coins": -100,
            "reputation": -1
        },
        "rarity": "common",
        "conditions": {
            "max_level": 3,
            "min_contracts": 2
        }
    },
    
    "imposter_syndrome": {
        "type": "negative",
        "emoji": "😰",
        "title": "Zespół Samozwańczości",
        "description": "Masz wątpliwości czy naprawdę jesteś wystarczająco dobry/a. Potrzebujesz chwili na odzyskanie pewności siebie.",
        "flavor_text": "\"A co jeśli klient odkryje, że tak naprawdę nie wiem co robię...?\"",
        "effects": {
            "capacity_penalty": -1,
            "duration_days": 1
        },
        "rarity": "uncommon",
        "conditions": {
            "max_level": 2,
            "min_contracts": 3,
            "max_avg_rating": 4.5
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

