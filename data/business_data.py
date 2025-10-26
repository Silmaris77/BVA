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
        "zakres_monet": (2000, 5000),
        "max_pracownikow": 2,
        "limit_kontraktow_dzienny": 1,
        "opis": "Mała firma z pierwszymi pracownikami. Czas na rozwój!",
        "ikona": "🏢"
    },
    3: {
        "nazwa": "CIQ Advisory",
        "zakres_monet": (5000, 10000),
        "max_pracownikow": 3,
        "limit_kontraktow_dzienny": 1,
        "opis": "Rozwijająca się firma konsultingowa z rosnącym portfolio",
        "ikona": "🏛️"
    },
    4: {
        "nazwa": "Strategic Partners",
        "zakres_monet": (10000, 20000),
        "max_pracownikow": 5,
        "limit_kontraktow_dzienny": 2,
        "opis": "Firma strategiczna z solidną bazą klientów",
        "ikona": "🎯"
    },
    5: {
        "nazwa": "Elite Consulting Group",
        "zakres_monet": (20000, 35000),
        "max_pracownikow": 7,
        "limit_kontraktow_dzienny": 2,
        "opis": "Elitarna grupa konsultingowa z prestiżowymi kontraktami",
        "ikona": "💎"
    },
    6: {
        "nazwa": "Regional CIQ Leaders",
        "zakres_monet": (35000, 55000),
        "max_pracownikow": 10,
        "limit_kontraktow_dzienny": 2,
        "opis": "Liderzy regionalni z oddziałami w kilku miastach",
        "ikona": "🌆"
    },
    7: {
        "nazwa": "National CIQ Authority",
        "zakres_monet": (55000, 80000),
        "max_pracownikow": 15,
        "limit_kontraktow_dzienny": 3,
        "opis": "Autorytet w skali kraju - znana marka w branży",
        "ikona": "�"
    },
    8: {
        "nazwa": "Global CIQ Partners",
        "zakres_monet": (80000, 120000),
        "max_pracownikow": 20,
        "limit_kontraktow_dzienny": 3,
        "opis": "Międzynarodowa firma z prestiżową klientelą na wielu rynkach",
        "ikona": "🌍"
    },
    9: {
        "nazwa": "Worldwide CIQ Corporation",
        "zakres_monet": (120000, 180000),
        "max_pracownikow": 30,
        "limit_kontraktow_dzienny": 4,
        "opis": "Globalna korporacja konsultingowa z oddziałami na 5 kontynentach",
        "ikona": "🌐"
    },
    10: {
        "nazwa": "CIQ Empire",
        "zakres_monet": (180000, float('inf')),
        "max_pracownikow": 50,
        "limit_kontraktow_dzienny": 5,
        "opis": "Imperium CIQ - absolutny lider rynku, legenda branży!",
        "ikona": "👑"
    }
}

# =============================================================================
# TYPY BIUR
# =============================================================================

OFFICE_TYPES = {
    "home_office": {
        "nazwa": "Home Office",
        "max_pracownikow": 2,
        "koszt_dzienny": 0,
        "koszt_ulepszenia": 0,
        "bonus_reputacji": 0,
        "opis": "Praca z domu - wystarczy na początek",
        "ikona": "🏠"
    },
    "small_office": {
        "nazwa": "Small Office",
        "max_pracownikow": 5,
        "koszt_dzienny": 50,
        "koszt_ulepszenia": 1000,
        "bonus_reputacji": 5,
        "opis": "Małe biuro w centrum miasta",
        "ikona": "🏢"
    },
    "medium_office": {
        "nazwa": "Medium Office",
        "max_pracownikow": 10,
        "koszt_dzienny": 100,
        "koszt_ulepszenia": 3000,
        "bonus_reputacji": 15,
        "opis": "Przestronne biuro z salą konferencyjną",
        "ikona": "🏛️"
    },
    "large_office": {
        "nazwa": "Large Office",
        "max_pracownikow": 20,
        "koszt_dzienny": 200,
        "koszt_ulepszenia": 7000,
        "bonus_reputacji": 30,
        "opis": "Duże biuro z wieloma pokojami",
        "ikona": "🏰"
    },
    "headquarters": {
        "nazwa": "Headquarters",
        "max_pracownikow": 50,
        "koszt_dzienny": 400,
        "koszt_ulepszenia": float('inf'),  # Maksymalny poziom
        "bonus_reputacji": 50,
        "opis": "Prestiżowa siedziba firmy",
        "ikona": "🌆"
    }
}

# Kolejność ulepszeń biura
OFFICE_UPGRADE_PATH = [
    "home_office",
    "small_office", 
    "medium_office",
    "large_office",
    "headquarters"
]

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
    # ===== BARDZO PROSTE KONTRAKTY DLA POCZĄTKUJĄCYCH (TRUDNOŚĆ 1) =====
    
    {
        "id": "CIQ-EASY-001",
        "tytul": "Krótka rozmowa 1:1 z pracownikiem",
        "kategoria": "Leadership",
        "klient": "LocalCafe",
        "opis": """Właściciel małej kawiarni chce porozmawiać z barista, który ostatnio jest spóźniony.""",
        "zadanie": """Odpowiedz BARDZO KRÓTKO:

1. **Jak rozpoczniesz rozmowę?** (1 zdanie)

2. **Jakie 2 pytania zadasz?** (lista)

3. **Jak zakończysz spotkanie?** (1 zdanie)""",
        "wymagana_wiedza": ["Podstawy komunikacji"],
        "trudnosc": 1,
        "nagroda_base": 200,
        "nagroda_4star": 250,
        "nagroda_5star": 350,
        "reputacja": 15,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,
        "min_slow": 20,
        "emoji": "☕"
    },
    {
        "id": "CIQ-EASY-002",
        "tytul": "Feedback dla nowego pracownika",
        "kategoria": "Feedback",
        "klient": "SmallShop",
        "opis": """Nowy pracownik w sklepie dobrze radzi sobie z klientami, ale zapomina o porządkowaniu półek.""",
        "zadanie": """Napisz krótki feedback (3-5 zdań):

- Co robi dobrze?
- Co warto poprawić?
- Jak może to zrobić?""",
        "wymagana_wiedza": ["Podstawy feedbacku"],
        "trudnosc": 1,
        "nagroda_base": 180,
        "nagroda_4star": 230,
        "nagroda_5star": 300,
        "reputacja": 12,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,
        "min_slow": 15,
        "emoji": "🛒"
    },
    {
        "id": "CIQ-EASY-003",
        "tytul": "Rozwiązanie małego konfliktu",
        "kategoria": "Konflikt",
        "klient": "OfficeTeam",
        "opis": """Dwóch pracowników biurowych kłóci się o to, kto ma sprzątać wspólną kuchnię.""",
        "zadanie": """Zaproponuj proste rozwiązanie:

1. **Dlaczego się kłócą?** (1 zdanie)

2. **Twoja propozycja** (2-3 zdania)

3. **Jak to wdrożyć?** (1-2 zdania)""",
        "wymagana_wiedza": ["Podstawy rozwiązywania konfliktów"],
        "trudnosc": 1,
        "nagroda_base": 220,
        "nagroda_4star": 280,
        "nagroda_5star": 380,
        "reputacja": 18,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,
        "min_slow": 20,
        "emoji": "🧹"
    },
    {
        "id": "CIQ-EASY-004",
        "tytul": "Pytania do zespołu na spotkaniu",
        "kategoria": "Leadership",
        "klient": "StartupTeam",
        "opis": """Manager nowego zespołu (5 osób) chce przeprowadzić pierwsze spotkanie i poznać zespół.""",
        "zadanie": """Zaproponuj 5 pytań na spotkanie:

- 3 pytania do poznania zespołu
- 2 pytania o pracę/projekty

(tylko lista pytań)""",
        "wymagana_wiedza": ["Podstawy komunikacji"],
        "trudnosc": 1,
        "nagroda_base": 160,
        "nagroda_4star": 210,
        "nagroda_5star": 280,
        "reputacja": 10,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,
        "min_slow": 15,
        "emoji": "❓"
    },
    {
        "id": "CIQ-EASY-005",
        "tytul": "Pochwała za dobrą robotę",
        "kategoria": "Feedback",
        "klient": "TechStart",
        "opis": """Młody developer wykonał świetną pracę przy trudnym projekcie. Czas na uznanie!""",
        "zadanie": """Napisz krótką wiadomość (3-4 zdania):

- Co konkretnie zrobił dobrze?
- Jaki to miało wpływ?
- Co to dla Ciebie znaczy?""",
        "wymagana_wiedza": ["Pozytywny feedback"],
        "trudnosc": 1,
        "nagroda_base": 150,
        "nagroda_4star": 200,
        "nagroda_5star": 270,
        "reputacja": 8,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,
        "min_slow": 10,
        "emoji": "⭐"
    },
    {
        "id": "CIQ-EASY-006",
        "tytul": "Plan krótkiego spotkania 1:1",
        "kategoria": "Leadership",
        "klient": "RemoteTeam",
        "opis": """Manager zdalnego zespołu chce regularnie spotykać się 1:1 z każdym członkiem zespołu.""",
        "zadanie": """Zaproponuj prosty plan spotkania (15 min):

1. **Początek** - jak zacząć? (1 zdanie)

2. **Środek** - o czym rozmawiać? (3 tematy)

3. **Koniec** - jak zakończyć? (1 zdanie)""",
        "wymagana_wiedza": ["1:1 meetings"],
        "trudnosc": 1,
        "nagroda_base": 190,
        "nagroda_4star": 240,
        "nagroda_5star": 320,
        "reputacja": 14,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,
        "min_slow": 15,
        "emoji": "📅"
    },
    
    # ===== ORYGINALNE KONTRAKTY =====
    
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
    },
    
    # =============================================================================
    # AI CONVERSATION CONTRACTS - Dynamic Simulations
    # =============================================================================
    
    {
        "id": "CIQ-AI-001",
        "tytul": "💬 Rozmowa: Spóźniający się Talent",
        "kategoria": "AI Conversation",
        "klient": "TechVenture Sp. z o.o.",
        "opis": """Twój najlepszy programista Mark jest systematycznie spóźniony - to już trzecie spóźnienie w tym tygodniu. Zespół to zauważa i atmosfera się pogarsza. Musisz przeprowadzić trudną rozmowę.""",
        "zadanie": """🎭 SYMULACJA ROZMOWY Z AI

**Twoja rola:** Lead konsultant HR - klient poprosił Cię o przeprowadzenie trudnej rozmowy z pracownikiem

**Rozmówca:** Mark, senior developer (gra AI)
- Osobowość: introwertyk, defensywny gdy atakowany, otwarty gdy czuje empatię
- Sytuacja: spóźniony po raz trzeci w tym tygodniu
- Ukryty kontekst: ma osobisty problem (AI zareaguje jeśli podejdziesz empatycznie)

**Twoje zadanie:**
1. Przeprowadź profesjonalną rozmowę coachingową
2. Odkryj prawdziwy powód spóźnień
3. Wypracuj rozwiązanie, które zadowoli obie strony
4. Zachowaj dobrą relację z pracownikiem

**AI ocenia Cię na żywo w 4 wymiarach:**
- 🤝 Empatia - czy rozumiesz perspektywę rozmówcy
- 💪 Asertywność - czy jasno stawiasz granice bez agresji
- 👔 Profesjonalizm - ton, forma, struktura rozmowy
- 💡 Jakość rozwiązania - czy propozycje są konstruktywne

**Jak działa:**
- Piszesz swoją wypowiedź → AI ocenia i reaguje jako Mark
- Każda odpowiedź oceniana (0-20 pkt + wpływ na relację)
- Rozmowa kończy się gdy wypracujecie rozwiązanie lub zepsujecie relację
- Różne zakończenia w zależności od Twoich decyzji!

**Wskazówka:** Zastosuj GROW model lub Conversational Intelligence""",
        "wymagana_wiedza": ["Conversational Intelligence", "Empathy", "GROW Model", "Difficult Conversations"],
        "trudnosc": 1,  # Zmienione z 3 na 1 - aby był widoczny od startu
        "nagroda_base": 600,
        "nagroda_4star": 850,
        "nagroda_5star": 1100,
        "reputacja": 40,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,  # Changed from 2 to 1 - dostępny od startu
        "emoji": "💬",
        
        # Conversation specific fields
        "contract_type": "conversation",
        "npc_config": {
            "name": "Mark",
            "role": "Senior Developer",
            "personality": "introwerted, defensive when attacked, opens up with empathy",
            "personality_notes": "Mark is a talented developer who becomes defensive under pressure. He's dealing with a personal crisis (his mother has cancer and needs daily chemo transport), but won't share this unless he feels safe and understood. If approached with empathy and genuine concern, he'll open up. If confronted aggressively, he'll shut down or quit.",
            "initial_emotion": "anxious",
            "current_emotion": "anxious",
            "goal": "Keep his job while managing his mother's medical crisis. Hoping for understanding and flexibility.",
            "opening_message": "Mark siedzi przy biurku, unikając kontaktu wzrokowego. Widzisz jak napina się gdy się zbliżasz.\n\nMark: \"Przepraszam za spóźnienie... Wiem, że to już trzeci raz w tym tygodniu.\"",
            "fallback_response": "Rozumiem. Może... może muszę po prostu być bardziej zdyscyplinowany."
        },
        "scenario_context": """**Kontekst scenariusza:**

Mark jest Twoim najlepszym senior developerem - 5 lat w firmie, kluczowy dla głównego projektu. Ostatnio jest systematycznie spóźniony - to już trzecie spóźnienie w tym tygodniu (poniedziałek, środa, piątek). Zespół to zauważa - Sarah musiała dzisiaj prezentować jego część na daily standup.

**Ukryty kontekst (który Mark może ujawnić jeśli się otworzy):**
Mama Marka ma raka i właśnie zaczęła chemioterapię. Wymaga codziennego transportu do szpitala o 8:00 rano. Mark nie ma rodzeństwa, ojciec zmarł. On jest jedyną osobą która może ją zawieźć. Jest wykończony emocjonalnie i fizycznie, ale boi się o tym mówić bo myśli że zostanie zwolniony lub uznany za niewydajnego.

**Cel rozmowy:**
1. Odkryć prawdziwą przyczynę spóźnień (nie zakładać z góry)
2. Zachować relację i zaufanie
3. Znaleźć rozwiązanie win-win (np. flex hours, remote work, team support)
4. Pokazać empatię bez rezygnacji z standardów zespołowych

**Możliwe zakończenia:**
- SUCCESS: Mark się otwiera, wypracowujecie elastyczne rozwiązanie, zespół wspiera
- NEUTRAL: Problem rozwiązany powierzchownie, ale bez prawdziwego zrozumienia
- FAILURE: Mark się zblokował lub złożył wypowiedzenie, zespół zdemotywowany

**Wskaźniki sukcesu:**
- Relacja Mark-Firma: czy zostanie i będzie zaangażowany
- Morale zespołu: czy rozumieją sytuację i wspierają
- Rozwiązanie: czy jest długofalowe i fair dla wszystkich"""
    },
    

    {
        "id": "CIQ-AI-002",
        "tytul": "💬 Rozmowa: Trudne Negocjacje",
        "kategoria": "AI Conversation",
        "klient": "TechVentures LLC",
        "opis": """Największy klient (40% revenue) grozi odejściem jeśli nie dostanie 40% zniżki. CEO Michael zadzwonił osobiście. Musisz wynegocjować rozwiązanie które uratuje kontrakt BEZ niszczenia marży.""",
        "zadanie": """🎭 SYMULACJA NEGOCJACJI Z AI

**Twoja rola:** Senior Business Consultant - klient poprosił Cię o pomoc w trudnych negocjacjach

**Rozmówca:** Michael (CEO TechVentures) - gra AI
- Osobowość: twardy negocjator, ale otwarty na win-win jeśli pokażesz wartość
- Sytuacja: zarząd wymaga obniżenia kosztów o 40%, konkurencja oferuje tańszą ofertę
- Ukryty kontekst: wie że Twoja firma jest lepsza, ale ma presję zarządu (AI zareaguje jeśli odkryjesz prawdziwą motywację)

**Twoje zadanie:**
1. Wynegocjuj warunki które utrzymają klienta I Twoją marżę
2. Odkryj prawdziwą motywację (czy to tylko cena?)
3. Zaproponuj kreatywne rozwiązanie win-win
4. Zachowaj długoterminową relację biznesową

**AI ocenia Cię na żywo:**
- 🤝 Empatia - czy rozumiesz pozycję klienta
- 💪 Asertywność - czy bronisz swojej wartości bez kapitulacji
- 👔 Profesjonalizm - biznesowy ton i argumentacja
- 💡 Jakość rozwiązania - kreatywność i wykonalność propozycji

**Możliwe zakończenia:**
- WORST: Natychmiastowa kapitulacja (40% zniżka) → stracisz wiarygodność
- BAD: Klient odchodzi → utrata 500k/rok
- MEDIOCRE: 30% zniżka → słaba marża
- GOOD: 10-15% zniżka + coś ekstra (długi kontrakt, dodatkowe usługi)
- GREAT: Win-win bez zniżki (ROI report, tiered services, custom package)
- BEST: Klient podnosi budżet bo widzi dodatkową wartość!

**Wskazówka:** Nie pytaj o zniżkę - pytaj o WARTOŚĆ i CELE biznesowe""",
        "wymagana_wiedza": ["Negotiation", "Value Communication", "Win-Win Thinking", "Business Acumen"],
        "trudnosc": 1,  # Zmienione z 4 na 1 - aby był widoczny od startu
        "nagroda_base": 800,
        "nagroda_4star": 1100,
        "nagroda_5star": 1400,
        "reputacja": 50,
        "czas_realizacji_dni": 1,
        "wymagany_poziom": 1,  # Changed from 3 to 1 - dostępny od startu
        "emoji": "💬",
        
        # Conversation specific fields
        "contract_type": "conversation",
        "npc_config": {
            "name": "Michael",
            "role": "CEO TechVentures LLC",
            "personality": "tough negotiator, ROI-focused, respectful but firm",
            "personality_notes": "Michael is under pressure from his board to cut costs by 40%. He received a competing offer that's 40% cheaper (but lower quality). He KNOWS your service is better (you saved them $880k last year through optimization), but needs to show the board he's fighting for cost reduction. If you demonstrate clear ROI and help him justify the premium to his board, he'll stay. If you just fold on price, he'll lose respect and demand more. If you're too rigid, he'll leave.",
            "initial_emotion": "businesslike",
            "current_emotion": "businesslike",
            "goal": "Get a deal that satisfies the board (cost reduction or proven ROI) while keeping quality service. Ideally: pay same or less but get MORE value.",
            "opening_message": "*Michael dzwoni do Ciebie osobiście - to rzadkość*\n\nMichael: \"Musimy porozmawiać o kontrakcie. Zarząd wymaga 40% cięcia kosztów. Mam ofertę od Twojej konkurencji - 40% taniej. Cenię naszą współpracę, ale biznes to biznes. Co możesz zaproponować?\"",
            "fallback_response": "Rozumiem. Muszę to przemyśleć i przedyskutować z zarządem."
        },
        "scenario_context": """**Kontekst scenariusza:**

TechVentures LLC to Twój największy klient - 500k zł/rok, stanowi 40% Twojego revenue. Współpraca trwa 3 lata, zawsze byli zadowoleni. W zeszłym roku Twoja optymalizacja procesów zaoszczędziła im 880k zł (mierzalne ROI). 

**Ukryty kontekst:**
- Zarząd TechVentures wprowadza policy: wszystkie koszty vendor down 40%
- Michael (CEO) dostał ofertę od tańszej firmy (40% cheaper)
- Michael WIE że jesteś lepszy (proof: 880k savings), ale potrzebuje ammunition do obrony przed zarządem
- Prawdziwy problem: nie cena, ale brak uzasadnienia dla zarządu DLACZEGO premium service is worth it
- Jeśli pomożesz mu zbudować business case dla zarządu → zostaje i może nawet zwiększy budżet
- Jeśli od razu dasz zniżkę → straci szacunek i będzie demand more
- Jeśli będziesz zbyt sztywny bez pokazania wartości → odejdzie bo nie ma choice

**Cel rozmowy:**
1. Odkryć prawdziwą motywację (zarząd, nie Michael)
2. Przypomnieć o wartości (880k ROI)
3. Zaproponować kreatywne rozwiązanie (np. tiered service, ROI-based pricing, long-term contract z bonusami)
4. Pomóc Michaelowi zbudować argument dla zarządu

**Możliwe rozwiązania (od najlepszego):**
- ROI Report dla zarządu (0% zniżka, ale clear justification)
- Custom package (ta sama cena, ale więcej value)
- Tiered service model (basic cheaper, premium upsell)
- Długoterminowy kontrakt (2-3 lata, 10% discount overall)
- Performance-based pricing (pay for results)
- Bundle z innymi usługami (percepcja oszczędności)

**WORST solution:**
- Natychmiastowa kapitulacja (40% zniżka) → Michael traci respect, Ty tracisz margin i credibility"""
    },
    
    # =========================================================================
    # SPEED CHALLENGE CONTRACTS - Kontrakt z limitem czasu
    # =========================================================================
    {
        "id": "speed_urgent_call",
        "tytul": "⚡ Urgent: Klient dzwoni - natychmiastowa porada!",
        "kategoria": "Kryzys",
        "klient": "StartupHub",
        "opis": "Ważny klient dzwoni z pilną kwestią biznesową. Musisz doradzić NA MIEJSCU - nie ma czasu na research!",
        "wymagana_wiedza": ["Business Metrics", "Quick Thinking", "Client Communication"],
        "typ": "pisanie",
        "trudnosc": 1,  # Zmienione na 1 żeby było zawsze widoczne
        "nagroda_base": 400,
        "nagroda_4star": 550,
        "nagroda_5star": 700,
        "reputacja": 30,
        "czas_realizacji_dni": 0,  # Natychmiastowe - nie ma deadline
        "wymagany_poziom": 1,
        "emoji": "⚡",
        
        # Speed Challenge specific fields
        "contract_type": "speed_challenge",
        "time_limit_seconds": 90,  # 1.5 minuty na odpowiedź
        "speed_bonus_multiplier": 1.5,  # Bonus za szybką odpowiedź
        "pressure_level": "medium",  # low/medium/high
        
        "challenge_config": {
            "situation": "urgent_phone_call",
            "client_name": "Anna Kowalska",
            "client_role": "CEO StartupHub",
            "urgency_reason": "Zaraz mam meeting z inwestorem za 10 minut!",
            
            "problem": """Anna (CEO StartupHub) dzwoni do Ciebie w panice:

"Słuchaj, zaraz mam pitch przed inwestorami - za 10 MINUT! Jeden z nich właśnie przysłał email z pytaniem, które totalnie mnie zaskoczyło:

**Pytanie inwestora:**
'Dlaczego wasz CAC (Customer Acquisition Cost) wzrósł z 50 zł do 150 zł w Q2, podczas gdy LTV (Lifetime Value) spadło z 800 zł do 600 zł? To czerwona flaga - lejek się rozpadł czy problem w retencji?'

Kurczę, nie mam czasu na szczegółową analizę! Jak mam na to odpowiedzieć, żeby NIE wyglądać jak idiota? Potrzebuję quick smart answer - CO to znaczy i JAK bronić tych liczb!"

**Twoje zadanie:**
Doradzić Annie w 90 sekund:
1. Co to naprawdę znaczy (w prostych słowach)
2. Jak to interpretation/spin żeby nie brzmiało źle
3. Konkretną odpowiedź którą może użyć NA MIEJSCU""",
            
            "evaluation_criteria": {
                "clarity": "Czy wyjaśniłeś problem w prostych słowach?",
                "actionable": "Czy dałeś konkretną odpowiedź do użycia?",
                "calm_confidence": "Czy uspokoiłeś klienta i dodałeś mu pewności?",
                "business_savvy": "Czy pokazałeś zrozumienie metryki CAC/LTV?"
            },
            
            "ideal_answer_keywords": [
                "CAC wzrósł",
                "LTV spadło",
                "inwestycja w growth",
                "customer quality",
                "cohort analysis",
                "pokazać trend",
                "wyjaśnić kontekst",
                "pivot strategii"
            ]
        }
    },
    {
        "id": "speed_crisis_decision",
        "tytul": "⚡ KRYZYS: Decyzja w 60 sekund!",
        "kategoria": "Kryzys",
        "klient": "TechShop",
        "opis": "Twój klient ma awarię systemu podczas Black Friday. Musisz doradzić NATYCHMIAST - każda sekunda to stracone tysiące złotych!",
        "wymagana_wiedza": ["Crisis Management", "Technical Decision Making", "Damage Control"],
        "typ": "pisanie",
        "trudnosc": 1,  # Zmienione na 1 żeby było zawsze widoczne (można zmienić na 3 później)
        "nagroda_base": 600,
        "nagroda_4star": 850,
        "nagroda_5star": 1100,
        "reputacja": 45,
        "czas_realizacji_dni": 0,
        "wymagany_poziom": 1,  # Zmienione na 1 żeby było dostępne od początku
        "emoji": "⚡",
        
        "contract_type": "speed_challenge",
        "time_limit_seconds": 60,  # Tylko 1 minuta!
        "speed_bonus_multiplier": 2.0,  # Wyższy bonus - wyższy pressure
        "pressure_level": "high",
        
        "challenge_config": {
            "situation": "system_crisis",
            "client_name": "Marek Nowak",
            "client_role": "CTO E-commerce TechShop",
            "urgency_reason": "Black Friday - tracimy 10k zł na minutę!",
            
            "problem": """Marek (CTO TechShop) dzwoni w totalnej panice - słychać chaos w tle:

"ALARM! Mamy BLACK FRIDAY - największy dzień roku! Właśnie padł nam checkout - klienci NIE MOGĄ PŁACIĆ!

**Sytuacja:**
- 15:30 - peak traffic (5000 userów na stronie)
- Checkout page zwraca błąd 503
- Platforma płatności (Stripe) działa OK - problem u NAS
- Dev team krzyczy że to 'database connection pool exhausted'
- Backup developer proponuje 'restart całego systemu' (to zajmie 15 minut downtime)
- Senior dev mówi 'zwiększ connection pool i przeładuj tylko API' (5 minut)
- CEO krzyczy 'NAPRAWCIE TO TERAZ!!!'

**Tracimy 10,000 zł na KAŻDĄ minutę downtime.**

CO MAMY ROBIĆ?! Restart czy przeładowanie?! SZYBKO!"

**Twoje zadanie (60 sekund):**
1. Która opcja (restart vs przeładowanie)?
2. DLACZEGO (quick reasoning)?
3. Co robić PÓKI to się dzieje (minimize damage)?""",
            
            "evaluation_criteria": {
                "decision_speed": "Czy szybko wybrałeś konkretne rozwiązanie?",
                "risk_assessment": "Czy oceniłeś ryzyko obu opcji?",
                "damage_control": "Czy zaproponowałeś plan minimalizacji strat?",
                "clear_communication": "Czy instrukcje są jasne dla zestresowanego klienta?"
            },
            
            "ideal_answer_keywords": [
                "przeładuj API",
                "connection pool",
                "szybsze rozwiązanie",
                "komunikat dla klientów",
                "monitoruj",
                "backup plan",
                "minimize downtime"
            ]
        }
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
    "reputation_to_level_3": 300,
    "reputation_to_level_4": 600,
    "reputation_to_level_5": 1000,
    "reputation_to_level_6": 1500,
    "reputation_to_level_7": 2200,
    "reputation_to_level_8": 3000,
    "reputation_to_level_9": 4000,
    "reputation_to_level_10": 5500,
    
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
        int: Poziom firmy (1-10)
    """
    # Sprawdź poziomy od najwyższego do najniższego
    # Poziom 10: CIQ Empire
    if coins >= 180000 and reputation >= GAME_CONFIG["reputation_to_level_10"]:
        return 10
    
    # Poziom 9: Worldwide CIQ Corporation
    if coins >= 120000 and reputation >= GAME_CONFIG["reputation_to_level_9"]:
        return 9
    
    # Poziom 8: Global CIQ Partners
    if coins >= 80000 and reputation >= GAME_CONFIG["reputation_to_level_8"]:
        return 8
    
    # Poziom 7: National CIQ Authority
    if coins >= 55000 and reputation >= GAME_CONFIG["reputation_to_level_7"]:
        return 7
    
    # Poziom 6: Regional CIQ Leaders
    if coins >= 35000 and reputation >= GAME_CONFIG["reputation_to_level_6"]:
        return 6
    
    # Poziom 5: Elite Consulting Group
    if coins >= 20000 and reputation >= GAME_CONFIG["reputation_to_level_5"]:
        return 5
    
    # Poziom 4: Strategic Partners
    if coins >= 10000 and reputation >= GAME_CONFIG["reputation_to_level_4"]:
        return 4
    
    # Poziom 3: CIQ Advisory  
    if coins >= 5000 and reputation >= GAME_CONFIG["reputation_to_level_3"]:
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

def get_all_ai_contracts():
    """Zwraca wszystkie kontrakty typu 'conversation' dla coaching tool"""
    conversation_contracts = []
    for contract in CONTRACTS_POOL:
        if contract.get("contract_type") == "conversation":
            # Dodaj pola wymagane przez coaching tool
            contract_dict = contract.copy()
            contract_dict["type"] = "conversation"  # Alias dla kompatybilności
            contract_dict["title"] = contract.get("tytul", "Bez tytułu")
            contract_dict["id"] = contract.get("id")
            conversation_contracts.append(contract_dict)
    return conversation_contracts
