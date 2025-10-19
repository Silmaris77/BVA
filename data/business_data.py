"""
Business Games - Dane podstawowe
Kontrakty CIQ, Poziomy Firmy, Pracownicy, Konfiguracja
"""

# =============================================================================
# POZIOMY FIRMY KONSULTINGOWEJ
# =============================================================================

FIRM_LEVELS = {
    1: {
        "nazwa": "Solo Consultant",
        "zakres_monet": (0, 2000),
        "max_pracownikow": 0,
        "limit_kontraktow_dzienny": 1,
        "opis": "Jeden konsultant freelancer - zaczynasz swoją przygodę!",
        "ikona": "👤"
    },
    2: {
        "nazwa": "Boutique Consulting",
        "zakres_monet": (2000, 8000),
        "max_pracownikow": 2,
        "limit_kontraktow_dzienny": 1,  # +1 na pracownika
        "opis": "Mała firma z pierwszymi pracownikami. Czas na rozwój!",
        "ikona": "🏢"
    },
    3: {
        "nazwa": "CIQ Advisory Group",
        "zakres_monet": (8000, 25000),
        "max_pracownikow": 5,
        "limit_kontraktow_dzienny": 1,
        "opis": "Renomowana firma konsultingowa z solidnym portfolio",
        "ikona": "🏛️"
    },
    4: {
        "nazwa": "Global CIQ Partners",
        "zakres_monet": (25000, float('inf')),
        "max_pracownikow": 10,
        "limit_kontraktow_dzienny": 2,
        "opis": "Międzynarodowa firma z prestiżową klientelą",
        "ikona": "🌍"
    }
}

# =============================================================================
# TYPY PRACOWNIKÓW
# =============================================================================

# =============================================================================
# LOGO FIRMY - Dostępne emoji/ikony
# =============================================================================

FIRM_LOGOS = {
    "basic": {
        "free": ["🏢", "🏛️", "🏰", "🏪", "🏬", "🏭", "🏗️", "🏙️"],
        "premium": []  # Na przyszłość - odblokowane za osiągnięcia
    },
    "business": {
        "free": ["💼", "📊", "📈", "💰", "🎯", "🚀", "⚡", "💎"],
        "premium": []
    },
    "creative": {
        "free": ["🎨", "🎭", "🎪", "🎬", "🎮", "🎲", "🎯", "✨"],
        "premium": []
    },
    "nature": {
        "free": ["🌍", "🌟", "⭐", "🌈", "🔥", "💧", "🌊", "🌺"],
        "premium": []
    },
    "tech": {
        "free": ["💻", "🖥️", "📱", "🔧", "⚙️", "🔬", "🛠️", "🤖"],
        "premium": []
    },
    "animals": {
        "free": ["🦁", "🦅", "🐉", "🦄", "🐺", "🦊", "🦈", "🐙"],
        "premium": []
    }
}

# =============================================================================
# TYPY PRACOWNIKÓW
# =============================================================================

EMPLOYEE_TYPES = {
    "junior": {
        "nazwa": "Junior Consultant",
        "koszt_dzienny": 50,
        "koszt_zatrudnienia": 500,
        "bonus": "+1 kontrakt/dzień",
        "bonus_type": "capacity",
        "bonus_value": 1,
        "specjalizacja": None,
        "wymagany_poziom": 1,
        "opis": "Świeży absolwent, wymaga nadzoru. Zwiększa pojemność o 1 kontrakt dziennie.",
        "ikona": "👨‍💼"
    },
    "conflict_specialist": {
        "nazwa": "Conflict Resolution Specialist",
        "koszt_dzienny": 120,
        "koszt_zatrudnienia": 1500,
        "bonus": "+25% zarobków: Konflikt",
        "bonus_type": "category_boost",
        "bonus_value": 0.25,
        "specjalizacja": "Konflikt",
        "wymagany_poziom": 2,
        "opis": "Ekspert w mediacjach i negocjacjach. Zwiększa zarobki z kontraktów typu 'Konflikt' o 25%.",
        "ikona": "⚔️"
    },
    "executive_coach": {
        "nazwa": "Executive Coach",
        "koszt_dzienny": 150,
        "koszt_zatrudnienia": 2000,
        "bonus": "+30% zarobków: Coaching",
        "bonus_type": "category_boost",
        "bonus_value": 0.30,
        "specjalizacja": "Coaching",
        "wymagany_poziom": 2,
        "opis": "Certyfikowany coach dla C-level. Zwiększa zarobki z kontraktów typu 'Coaching' o 30%.",
        "ikona": "🎯"
    },
    "culture_lead": {
        "nazwa": "Culture Transformation Lead",
        "koszt_dzienny": 140,
        "koszt_zatrudnienia": 1800,
        "bonus": "+25% zarobków: Kultura",
        "bonus_type": "category_boost",
        "bonus_value": 0.25,
        "specjalizacja": "Kultura",
        "wymagany_poziom": 3,
        "opis": "Specjalista od zmiany organizacyjnej. Zwiększa zarobki z kontraktów typu 'Kultura' o 25%.",
        "ikona": "🛡️"
    },
    "crisis_expert": {
        "nazwa": "Crisis Communication Expert",
        "koszt_dzienny": 180,
        "koszt_zatrudnienia": 2500,
        "bonus": "+35% zarobków: Kryzys",
        "bonus_type": "category_boost",
        "bonus_value": 0.35,
        "specjalizacja": "Kryzys",
        "wymagany_poziom": 3,
        "opis": "Ratuje reputacje w sytuacjach kryzysowych. Zwiększa zarobki z kontraktów typu 'Kryzys' o 35%.",
        "ikona": "🚨"
    },
    "operations_manager": {
        "nazwa": "Operations Manager",
        "koszt_dzienny": 100,
        "koszt_zatrudnienia": 1200,
        "bonus": "-15% kosztów pracowników",
        "bonus_type": "cost_reduction",
        "bonus_value": 0.15,
        "specjalizacja": "Wsparcie",
        "wymagany_poziom": 2,
        "opis": "Optymalizuje procesy firmy. Zmniejsza koszty wszystkich pracowników o 15%.",
        "ikona": "📊"
    }
}

# =============================================================================
# BAZA KONTRAKTÓW CIQ
# =============================================================================

CONTRACTS_POOL = [
    # KATEGORIA: LEADERSHIP & 1:1 (STARTER - TRUDNOŚĆ 1)
    {
        "id": "CIQ-STARTER-001",
        "tytul": "Poprawa komunikacji w zespole 2-osobowym",
        "kategoria": "Leadership",
        "klient": "StartupDuo",
        "opis": """Mały startup (2 osoby) ma problemy z komunikacją. 
Founder i developer nie rozmawiają otwarcie o priorytetach i oczekiwaniach.""",
        "zadanie": """Odpowiedz krótko na 3 pytania:

1. **Jakie mogą być 2 główne problemy w ich komunikacji?** (1-2 zdania)

2. **Zaproponuj 1 prosty ritual komunikacyjny.** (1 zdanie)

3. **Jak sprawdzić, czy komunikacja się poprawia?** (1 zdanie)""",
        "wymagana_wiedza": ["Conversational Intelligence", "Podstawy komunikacji"],
        "trudnosc": 1,
        "nagroda_base": 300,
        "nagroda_4star": 400,
        "nagroda_5star": 500,
        "reputacja": 20,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,
        "min_slow": 30,
        "emoji": "🤝"
    },
    
    # KATEGORIA: KONFLIKT & NEGOCJACJE
    {
        "id": "CIQ-KONFLIKT-001",
        "tytul": "Mediacja w konflikcie zespołowym",
        "kategoria": "Konflikt",
        "klient": "TechCorp",
        "opis": """Zespół projektowy w firmie TechCorp jest podzielony. 
Lider projektu i główny developer mają odmienne wizje dotyczące architektury systemu. 
Napięcie wpływa na terminowość i morale zespołu.""",
        "zadanie": """Odpowiedz krótko:

1. **Co prawdopodobnie jest źródłem konfliktu?** (2-3 zdania)
   
2. **Zaproponuj strukturę spotkania mediacyjnego.** (3-4 punkty, krótko)
   
3. **Jakie 3 kluczowe pytania zadasz obu stronom?** (lista pytań)""",
        "wymagana_wiedza": ["Conversational Intelligence", "Zarządzanie konfliktem", "Ladder of Inference"],
        "trudnosc": 2,
        "nagroda_base": 450,
        "nagroda_4star": 600,
        "nagroda_5star": 750,
        "reputacja": 30,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,
        "min_slow": 50,
        "emoji": "⚔️"
    },
    {
        "id": "CIQ-KONFLIKT-002",
        "tytul": "Negocjacje z trudnym stakeholderem",
        "kategoria": "Konflikt",
        "klient": "FinanceHub",
        "opis": """Kluczowy stakeholder w projekcie blokuje ważne decyzje. 
Ma silne opinie i nie słucha argumentów zespołu. CEO prosi o wsparcie.""",
        "zadanie": """Krótka strategia:

1. **Jakie mogą być jego ukryte motywacje i obawy?** (2-3 zdania)
   
2. **Zaproponuj strukturę rozmowy** (5 kroków, krótko)
   
3. **Wymień 5 kluczowych pytań otwartych do zadania**

4. **Best case i worst case - jak się zachowasz?** (po 1 zdaniu na każdy)""",
        "wymagana_wiedza": ["Conversational Intelligence", "Techniki negocjacyjne", "Active Listening"],
        "trudnosc": 3,
        "nagroda_base": 650,
        "nagroda_4star": 850,
        "nagroda_5star": 1100,
        "reputacja": 45,
        "czas_realizacji_dni": 2,
        "wymagany_poziom": 1,
        "min_slow": 80,
        "emoji": "⚔️"
    },
    
    # KATEGORIA: COACHING & FEEDBACK
    {
        "id": "CIQ-COACHING-001",
        "tytul": "Sesja coachingowa dla middle managera",
        "kategoria": "Coaching",
        "klient": "MarketPro",
        "opis": """Manager w firmie MarketPro ma problemy z delegowaniem zadań. 
Zespół czuje się mikromanagowany, co wpływa na zaangażowanie i autonomię.""",
        "zadanie": """Odpowiedz krótko:

1. **Jaki jest cel tej sesji coachingowej?** (1 zdanie)
   
2. **Wymień 5 kluczowych pytań coachingowych dla tego managera** (lista pytań)
   
3. **Jaki konkretny feedback dasz managerowi?** (2-3 zdania używając COIN)""",
        "wymagana_wiedza": ["Coaching conversations", "GROW Model", "COIN Framework"],
        "trudnosc": 2,
        "nagroda_base": 550,
        "nagroda_4star": 720,
        "nagroda_5star": 900,
        "reputacja": 35,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,
        "min_slow": 50,
        "emoji": "🎯"
    },
    {
        "id": "CIQ-COACHING-002",
        "tytul": "Executive coaching - transformacja lidera",
        "kategoria": "Coaching",
        "klient": "InnovateCorp",
        "opis": """C-level executive ma problemy z komunikacją w stresie. 
Zespół odbiera go jako agresywnego i nieprzewidywalnego. Board chce interwencji.""",
        "zadanie": """Program coachingowy (3 miesiące):

1. **Jakie narzędzia diagnostyczne wykorzystasz?** (wymień 5 + krótko dlaczego każde)
   
2. **Podaj 5 przykładowych pytań z 360-degree feedback**
   
3. **Określ 3 główne cele transformacji** (po 2-3 zdania na każdy)
   
4. **Zaproponuj po 2 konkretne działania na każdy miesiąc** (6 działań total)
   
5. **Jak zmierzysz sukces programu?** (3 KPI + jak je mierzyć)""",
        "wymagana_wiedza": ["Executive Coaching", "Emotional Intelligence", "Leadership Development"],
        "trudnosc": 4,
        "nagroda_base": 1200,
        "nagroda_4star": 1600,
        "nagroda_5star": 2000,
        "reputacja": 70,
        "czas_realizacji_dni": 3,
        "wymagany_poziom": 1,
        "min_slow": 120,
        "emoji": "🎯"
    },
    
    # KATEGORIA: KULTURA ZESPOŁU
    {
        "id": "CIQ-KULTURA-001",
        "tytul": "Audit kultury komunikacji w zespole",
        "kategoria": "Kultura",
        "klient": "DesignHub",
        "opis": """Remote team w firmie DesignHub ma niskie zaangażowanie. 
Ludzie boją się zadawać pytania na spotkaniach. Atmosfera jest sztywna i formalna.""",
        "zadanie": """Krótka analiza:

1. **Wymień 5 pytań diagnostycznych, które zadasz w wywiadach z zespołem**
   
2. **Jakie są 3 główne bariery w psychological safety tego zespołu?** (po 1 zdaniu na każdą)
   
3. **Zaproponuj 3 konkretne inicjatywy (rituały/procesy) do wdrożenia** (po 1-2 zdania na każdą)""",
        "wymagana_wiedza": ["Psychological Safety", "Team Dynamics", "Remote Work Best Practices"],
        "trudnosc": 3,
        "nagroda_base": 750,
        "nagroda_4star": 1000,
        "nagroda_5star": 1300,
        "reputacja": 50,
        "czas_realizacji_dni": 2,
        "wymagany_poziom": 1,
        "min_slow": 80,
        "emoji": "🛡️"
    },
    {
        "id": "CIQ-KULTURA-002",
        "tytul": "Wdrożenie kultury feedbacku",
        "kategoria": "Kultura",
        "klient": "StartupXYZ",
        "opis": """Startup (30 osób) rośnie szybko, ale nie ma kultury feedbacku. 
Ludzie dowiadują się o problemach dopiero na performance review.""",
        "zadanie": """Zaprojektuj prosty system:

1. **Wybierz framework feedbacku (COIN lub SBI) i wyjaśnij dlaczego** (2-3 zdania)
   
2. **Podaj 5 zasad dawania i przyjmowania feedbacku**
   
3. **Zaproponuj plan wdrożenia** (5 kroków, krótko)
   
4. **Jak utrzymać momentum?** (3 konkretne działania)""",
        "wymagana_wiedza": ["Feedback Frameworks", "Psychological Safety", "Change Management"],
        "trudnosc": 3,
        "nagroda_base": 800,
        "nagroda_4star": 1050,
        "nagroda_5star": 1350,
        "reputacja": 55,
        "czas_realizacji_dni": 2,
        "wymagany_poziom": 1,
        "min_slow": 80,
        "emoji": "🛡️"
    },
    
    # KATEGORIA: KRYZYS & TRUDNE ROZMOWY
    {
        "id": "CIQ-KRYZYS-001",
        "tytul": "Komunikacja po błędzie projektowym",
        "kategoria": "Kryzys",
        "klient": "TechStart",
        "opis": """Startup wprowadził feature, który spowodował bug u 30% użytkowników. 
Social media buzują negatywnymi komentarzami. CEO jest w panice.""",
        "zadanie": """Plan komunikacji kryzysowej:

1. **Napisz krótki komunikat do klientów (email)** - max 150 słów
   
2. **Jakie elementy MUSI zawierać komunikat kryzysowy?** (5 elementów)
   
3. **Co powiedzieć zespołowi engineering?** (3-4 zdania)
   
4. **Przygotuj 5 talking points dla CEO na rozmowy z inwestorami**
   
5. **Plan follow-up na 7 dni** (5 kroków)""",
        "wymagana_wiedza": ["Crisis Communication", "Stakeholder Management", "Psychological Safety"],
        "trudnosc": 4,
        "nagroda_base": 950,
        "nagroda_4star": 1250,
        "nagroda_5star": 1600,
        "reputacja": 65,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,
        "min_slow": 120,
        "emoji": "🚨"
    },
    {
        "id": "CIQ-KRYZYS-002",
        "tytul": "Zarządzanie zmianą - zwolnienia grupowe",
        "kategoria": "Kryzys",
        "klient": "CorporateInc",
        "opis": """Firma musi zwolnić 20% pracowników z powodu restrukturyzacji. 
Leadership chce to zrobić z empatią i zachować zaangażowanie pozostałego zespołu.""",
        "zadanie": """Kompleksowy plan komunikacji:

1. **Kto, kiedy i jak powinien się dowiedzieć PIERWSZY?** (timeline - 5 kroków)
   
2. **Agenda szkolenia dla managerów** (10 punktów z krótkimi opisami)
   
3. **Przygotuj listę 15 "anticipated questions" i odpowiedzi na każde**
   
4. **Napisz draft komunikatu od CEO** (max 200 słów)
   
5. **Framework indywidualnych rozmów** (6 kroków, co powiedzieć i czego NIE mówić)
   
6. **Plan wsparcia dla pozostałego zespołu** (survivor guilt - 5 konkretnych działań)
   
7. **Rebuilding trust - plan na 60 dni** (3 fazy po 20 dni, co w każdej)""",
        "wymagana_wiedza": ["Change Management", "Crisis Communication", "Difficult Conversations"],
        "trudnosc": 5,
        "nagroda_base": 1500,
        "nagroda_4star": 2000,
        "nagroda_5star": 2500,
        "reputacja": 90,
        "czas_realizacji_dni": 3,
        "wymagany_poziom": 1,
        "min_slow": 200,
        "emoji": "🚨"
    },
    
    # KATEGORIA: LEADERSHIP & 1:1
    {
        "id": "CIQ-LEADERSHIP-001",
        "tytul": "Framework dla efektywnych 1:1",
        "kategoria": "Leadership",
        "klient": "MarketPro",
        "opis": """Firma MarketPro (50 osób) nie ma struktury 1:1 meetings. 
Leadership chce wprowadzić best practices dla wszystkich managerów.""",
        "zadanie": """Odpowiedz krótko:

1. **Jak często i jak długo powinny trwać 1:1?** (1 zdanie)
   
2. **Wymień 5 tematów, które należy poruszać na 1:1** (lista)
   
3. **Jakie 3 błędy managerowie najczęściej popełniają na 1:1?** (lista)""",
        "wymagana_wiedza": ["1:1 Conversations", "Active Listening", "Coaching"],
        "trudnosc": 2,
        "nagroda_base": 500,
        "nagroda_4star": 650,
        "nagroda_5star": 850,
        "reputacja": 40,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,
        "min_slow": 40,
        "emoji": "🤝"
    },
    {
        "id": "CIQ-LEADERSHIP-002",
        "tytul": "Skip-level meetings strategy",
        "kategoria": "Leadership",
        "klient": "GrowthCorp",
        "opis": """VP Engineering chce wprowadzić skip-level meetings aby lepiej rozumieć 
co się dzieje w zespołach. Nie wie jak to zrobić, żeby nie podważyć autytetu managerów.""",
        "zadanie": """Strategia skip-level:

1. **Jakie są cele skip-level meetings?** (3 cele, po 1 zdaniu)
   
2. **Jak przedstawić to managerom, żeby nie czuli zagrożenia?** (3-4 zdania)
   
3. **Wymień 10 kluczowych pytań do zadania na skip-level**
   
4. **Czego NIE poruszać na skip-level?** (3 tematy z wyjaśnieniem)""",
        "wymagana_wiedza": ["Skip-level meetings", "Leadership", "Trust Building"],
        "trudnosc": 3,
        "nagroda_base": 700,
        "nagroda_4star": 900,
        "nagroda_5star": 1150,
        "reputacja": 50,
        "czas_realizacji_dni": 2,
        "wymagany_poziom": 1,
        "min_slow": 80,
        "emoji": "🤝"
    }
]

# =============================================================================
# KONFIGURACJA GRY
# =============================================================================

GAME_CONFIG = {
    # Początkowe zasoby
    "starting_coins": 1000,
    "starting_level": 1,
    "starting_reputation": 0,
    
    # Limity i mechaniki
    "max_active_contracts": 3,  # Maksymalna liczba aktywnych kontraktów jednocześnie
    "max_daily_contracts": 10,  # Absolutny limit (nawet z pracownikami)
    "contract_pool_refresh_hours": 24,  # Co ile godzin odświeża się pula kontraktów
    "contract_pool_size": 7,  # Ile kontraktów jest dostępnych dziennie
    
    # Koszty
    "daily_employee_cost_multiplier": 1.0,  # Mnożnik kosztów pracowników
    "contract_penalty_incomplete": 0.5,  # 50% kary za nieukończony kontrakt w terminie
    
    # Progresja
    "reputation_to_level_2": 100,
    "reputation_to_level_3": 500,
    "reputation_to_level_4": 1500,
    
    # Rankingi
    "min_contracts_for_ranking": 0,  # Brak bariery - rankingi widoczne od początku
    "ranking_weights": {
        "overall": {
            "revenue": 0.30,
            "avg_rating": 0.25,
            "reputation": 0.20,
            "level": 0.15,
            "contracts": 0.10
        }
    }
}

# =============================================================================
# KRYTERIA OCENY AI
# =============================================================================

EVALUATION_CRITERIA = {
    "completeness": {
        "weight": 0.25,
        "description": "Czy odpowiedź zawiera wszystkie wymagane elementy?",
        "thresholds": {
            5: "Wszystkie elementy obecne + dodatkowe insights",
            4: "Wszystkie wymagane elementy obecne",
            3: "Większość elementów, brakuje 1-2",
            2: "Niepełna odpowiedź, brakuje 3+ elementów",
            1: "Bardzo niekompletna odpowiedź"
        }
    },
    "quality": {
        "weight": 0.30,
        "description": "Jakość merytoryczna i głębokość analizy",
        "thresholds": {
            5: "Wyjątkowa jakość, profesjonalne insights",
            4: "Solidna jakość, dobre uzasadnienia",
            3: "Przeciętna jakość, powierzchowna analiza",
            2: "Słaba jakość, mało konkretów",
            1: "Bardzo słaba jakość"
        }
    },
    "practical": {
        "weight": 0.25,
        "description": "Praktyczność i możliwość implementacji",
        "thresholds": {
            5: "Gotowe do użycia, konkretne action items",
            4: "Praktyczne z drobnymi modyfikacjami",
            3: "Częściowo praktyczne",
            2: "Bardzo teoretyczne, mało praktyczne",
            1: "Niepraktyczne rozwiązania"
        }
    },
    "ciq_knowledge": {
        "weight": 0.20,
        "description": "Wykorzystanie wiedzy z lekcji CIQ",
        "thresholds": {
            5: "Doskonałe wykorzystanie frameworks i technik CIQ",
            4: "Dobre wykorzystanie konceptów CIQ",
            3: "Podstawowe odniesienia do CIQ",
            2: "Minimalne wykorzystanie wiedzy CIQ",
            1: "Brak odniesień do CIQ"
        }
    }
}

# =============================================================================
# FUNKCJE POMOCNICZE
# =============================================================================

def get_firm_level(coins, reputation):
    """Określa poziom firmy na podstawie monet i reputacji
    
    Aby awansować na wyższy poziom, musisz spełnić OBA warunki:
    1. Mieć wystarczającą ilość monet (zakres_monet)
    2. Zdobyć wymaganą reputację (reputation_to_level_X)
    
    Args:
        coins: Liczba monet użytkownika
        reputation: Punkty reputacji użytkownika
        
    Returns:
        int: Poziom firmy (1-4)
    """
    # Sprawdź poziomy od najwyższego do najniższego
    # Poziom 4: Global CIQ Partners
    if coins >= 25000 and reputation >= GAME_CONFIG["reputation_to_level_4"]:
        return 4
    
    # Poziom 3: CIQ Advisory Group  
    if coins >= 8000 and reputation >= GAME_CONFIG["reputation_to_level_3"]:
        return 3
    
    # Poziom 2: Boutique Consulting
    if coins >= 2000 and reputation >= GAME_CONFIG["reputation_to_level_2"]:
        return 2
    
    # Poziom 1: Solo Consultant (domyślny)
    return 1

def get_available_contracts(user_level, completed_lessons):
    """Zwraca kontrakty dostępne dla użytkownika"""
    available = []
    for contract in CONTRACTS_POOL:
        if contract["wymagany_poziom"] <= user_level:
            # Sprawdź czy użytkownik ma wymagane lekcje (uproszczone dla MVP)
            contract_copy = contract.copy()
            contract_copy["locked"] = False
            available.append(contract_copy)
    return available

def calculate_daily_capacity(firm_level, employees):
    """Oblicza dzienną pojemność kontraktów"""
    base = FIRM_LEVELS[firm_level]["limit_kontraktow_dzienny"]
    for emp in employees:
        emp_type = EMPLOYEE_TYPES.get(emp["type"])
        if emp_type and emp_type["bonus_type"] == "capacity":
            base += emp_type["bonus_value"]
    return int(base)

def calculate_employee_costs(employees):
    """Oblicza dzienny koszt pracowników"""
    total = 0
    has_ops_manager = any(emp["type"] == "operations_manager" for emp in employees)
    discount = 0.15 if has_ops_manager else 0
    
    for emp in employees:
        emp_type = EMPLOYEE_TYPES.get(emp["type"])
        if emp_type:
            cost = emp_type["koszt_dzienny"]
            if emp["type"] != "operations_manager":  # Ops manager nie dostaje własnego rabatu
                cost *= (1 - discount)
            total += cost
    
    return round(total, 2)

def get_contract_by_id(contract_id):
    """Pobiera kontrakt po ID"""
    for contract in CONTRACTS_POOL:
        if contract["id"] == contract_id:
            return contract
    return None
