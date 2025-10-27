"""
FMCG Tasks Pool
Zadania zawodowe dla wszystkich 10 poziomów kariery w FMCG

Kategorie:
- field_sales: Sprzedaż terenowa
- key_accounts: Kluczowi klienci
- team_management: Zarządzanie zespołem
- trade_marketing: Trade marketing i promocje
- strategy: Strategia i planowanie
- crisis: Zarządzanie kryzysowe
"""

# =============================================================================
# POZIOM 1-3: INDIVIDUAL CONTRIBUTOR
# =============================================================================

FMCG_TASKS = [
    
    # =========================================================================
    # LEVEL 1: Junior Sales Representative
    # =========================================================================
    
    {
        "id": "FMCG-FIELD-001",
        "title": "Pierwsza wizyta w sklepie",
        "category": "field_sales",
        "level_required": 1,
        "difficulty": 1,
        "icon": "🏪",
        "description": "Odwiedź sklep spożywczy 'U Janka' i przedstaw ofertę produktów GlobalCPG.",
        "scenario": """
**Klient:** Sklep osiedlowy 'U Janka' (właściciel: Jan Kowalski)
**Sytuacja:** Pierwszy kontakt z tym sklepem. Jan prowadzi mały sklep spożywczy od 15 lat.

**Twoje zadanie:**
1. Przedstaw się i firmę GlobalCPG
2. Zaprezentuj 3 produkty flagowe (Napój GlobalFresh, Czekolada ChocoDelight, Chemia CleanPro)
3. Wynegocjuj pierwsze zamówienie
4. Zaproponuj optymalne miejsce ekspozycji

**Kluczowe informacje:**
- Jan jest sceptyczny wobec nowych dostawców
- Ma już 3 konkurencyjnych dostawców
- Ceni sobie szybką dostawę i dobre warunki płatności
- Sklep ma ~30m² powierzchni sprzedaży

**Co napisać:**
- Jak się prezentujesz i budujesz relację?
- Jakie argumenty użyjesz na rzecz GlobalCPG?
- Jakie warunki handlowe zaproponujesz? (cena, marża, płatność, dostawa)
- Gdzie umieścić produkty w sklepie?
""",
        "task_type": "text",
        "expected_elements": [
            "Przedstawienie siebie i firmy",
            "Value proposition dla sklepu",
            "Konkretna oferta handlowa",
            "Propozycja ekspozycji",
            "Budowanie relacji z Janem"
        ],
        "base_reward": 500,
        "reward_4star": 700,
        "reward_5star": 1000,
        "sales_impact": 5000,      # +5000 PLN do monthly sales jeśli sukces
        "reputation_impact": 10,   # +10 do market share
        "time_days": 1
    },
    
    {
        "id": "FMCG-FIELD-002",
        "title": "Realizacja zamówienia w Żabce",
        "category": "field_sales",
        "level_required": 1,
        "difficulty": 2,
        "icon": "🛒",
        "description": "Zrealizuj zamówienie w sklepie Żabka i zapewnij prawidłową ekspozycję.",
        "scenario": """
**Klient:** Żabka (sklep franczyzowy, manager: Kasia)
**Sytuacja:** Żabka już kupuje od GlobalCPG, ale masz zadanie zwiększyć zamówienie o 30%.

**Twoje zadanie:**
1. Dostarczyć zamówienie (10 kartonów GlobalFresh, 15 kartonów ChocoDelight)
2. Upsell: Dodatkowe 5 kartonów nowego produktu 'EnergyBoost'
3. Zoptymalizować ekspozycję (shelf space)
4. Zrobić zdjęcie ekspozycji do raportu

**Wyzwania:**
- Kasia mówi że nie ma miejsca na półkach
- Konkurencja (RedBull) zajmuje prime location
- Żabka ma policy: max 3 SKU per dostawca na prominent shelf
- Nowy produkt EnergyBoost to nieznana marka

**Co napisać:**
- Jak przekonasz Kasię do EnergyBoost?
- Gdzie umieścisz produkty? (top shelf, eye level, bottom, przy kasie?)
- Jaką promocję zaproponujesz na start?
- Jak wygrasz z konkurencją o shelf space?
""",
        "task_type": "text",
        "expected_elements": [
            "Argumenty za EnergyBoost (upsell)",
            "Merchandising strategy",
            "Negocjacje shelf space",
            "Promocja na start (np. buy 10 get 1 free)"
        ],
        "base_reward": 600,
        "reward_4star": 850,
        "reward_5star": 1200,
        "sales_impact": 8000,
        "reputation_impact": 15,
        "time_days": 1
    },
    
    {
        "id": "FMCG-FIELD-003",
        "title": "Obsługa reklamacji klienta",
        "category": "field_sales",
        "level_required": 1,
        "difficulty": 2,
        "icon": "⚠️",
        "description": "Sklep ABC zgłosił problem z jakością produktu. Rozwiąż reklamację.",
        "scenario": """
**Klient:** Sklep ABC (właściciel: Piotr)
**Problem:** Piotr twierdzi że 5 butelek GlobalFresh miało niewłaściwy smak (kwaśne).

**Sytuacja:**
- Piotr jest zły i grozi że przeniesie zamówienia do konkurencji
- To Twój drugi najważniejszy klient (zamówienia ~15k PLN/miesiąc)
- Inne sklepy NIE zgłaszały podobnych problemów
- Procedura: Możesz wymienić produkt lub zaoferować credit note

**Twoje zadanie:**
1. Zbadaj sytuację (zadaj pytania - która partia, kiedy kupione, jak przechowywane)
2. Zaproponuj rozwiązanie
3. Odzyskaj zaufanie Piotra
4. Upewnij się że nie straci zamówień

**Co napisać:**
- Jakie pytania zadasz Piotrowi?
- Jak zareagujesz na jego złość? (empathy, apology, action)
- Jakie rozwiązanie zaproponujesz?
- Jak zapewnisz że to się nie powtórzy?
""",
        "task_type": "text",
        "expected_elements": [
            "Root cause analysis (pytania)",
            "Empatia i przeprosiny",
            "Konkretne rozwiązanie (wymiana, credit)",
            "Follow-up plan",
            "Retention strategy"
        ],
        "base_reward": 400,
        "reward_4star": 600,
        "reward_5star": 900,
        "sales_impact": -2000,   # Negatywny impact jeśli źle obsłużysz
        "reputation_impact": -10,
        "time_days": 1
    },
    
    # =========================================================================
    # LEVEL 2-3: Sales Representative / Senior Sales Rep
    # =========================================================================
    
    {
        "id": "FMCG-KEY-001",
        "title": "Negocjacje z siecią Lewiatan",
        "category": "key_accounts",
        "level_required": 2,
        "difficulty": 3,
        "icon": "🏢",
        "description": "Wynegocjuj listing 3 produktów w 20 sklepach Lewiatan (sieć regionalna).",
        "scenario": """
**Klient:** Lewiatan (regional chain manager: Tomasz Nowak)
**Cel:** Uzyskać listing w 20 sklepach na 3 produkty GlobalCPG

**Sytuacja:**
- Lewiatan ma 20 sklepów w Twoim regionie (Małopolska)
- Obecnie GlobalCPG NIE jest listowany
- Konkurencja (PepsiCo, Unilever) ma już dobre pozycje
- Tomasz chce: 45 dni płatności, 35% marży, quarterly rebate 3%

**Twoje limity (od managera):**
- Max 30 dni płatności
- Min 28% marży dla sieci
- Rebate: max 2% quarterly

**Twoje zadanie:**
1. Wynegocjuj warunki w ramach limitów
2. Zaproponuj launch promotion
3. Zapewnij support merchandisingowy
4. Podpisz umowę

**Co napisać:**
- Jak otworzysz negocjacje?
- Jaką wartość zaoferujesz Tomaszowi? (poza ceną)
- Jak wynegocjujesz lepsze warunki niż jego initial ask?
- Jaka będzie launch promotion? (BOGOF, 20% off, gift with purchase?)
""",
        "task_type": "text",
        "expected_elements": [
            "Opening strategy (value, not price)",
            "Trade-offs i concessions",
            "Launch promotion plan",
            "Merchandising support",
            "Win-win outcome"
        ],
        "base_reward": 1200,
        "reward_4star": 1800,
        "reward_5star": 2500,
        "sales_impact": 30000,  # Duży impact - 20 sklepów!
        "reputation_impact": 25,
        "time_days": 2
    },
    
    {
        "id": "FMCG-MARKETING-001",
        "title": "Realizacja kampanii 'Letnia Promocja'",
        "category": "trade_marketing",
        "level_required": 2,
        "difficulty": 2,
        "icon": "📢",
        "description": "Wdróż kampanię promocyjną w 15 sklepach. Budget: 5000 PLN.",
        "scenario": """
**Kampania:** Letnia Promocja GlobalFresh
**Cel:** +40% sprzedaży GlobalFresh w lipcu
**Budget:** 5000 PLN
**Sklepy:** 15 sklepów w Twoim territory

**Materiały od firmy:**
- 500 plakatów A3
- 200 wobblerów (shelf talkers)
- 1000 ulotek
- Budget na dodatkowe materiały

**Twoje zadanie:**
1. Zaplanuj dystrybucję materiałów (które sklepy, ile)
2. Zapewnij prime location ekspozycji
3. Zorganizuj sampling w 3 największych sklepach (weekend)
4. Zmierz rezultaty (przed/po)

**Wyzwania:**
- Sklepy nie chcą wielkich plakatów (brak miejsca)
- Sampling wymaga coordinacji z właścicielami
- Konkurencja też robi promocje w lipcu

**Co napisać:**
- Jak rozdysponujesz budget 5000 PLN?
- Którym sklepom dasz więcej materiałów? (segmentacja)
- Jak zorganizujesz sampling? (kto, kiedy, jak mierzyć efekt)
- Jak będziesz monitorować sukces kampanii?
""",
        "task_type": "text",
        "expected_elements": [
            "Budget allocation plan",
            "Segmentacja sklepów (A, B, C class)",
            "Sampling execution plan",
            "KPIs i measurement"
        ],
        "base_reward": 800,
        "reward_4star": 1200,
        "reward_5star": 1600,
        "sales_impact": 20000,
        "reputation_impact": 20,
        "time_days": 3
    },
    
    {
        "id": "FMCG-AI-001",
        "title": "💬 Rozmowa: Trudny klient grozi odejściem",
        "category": "field_sales",
        "level_required": 2,
        "difficulty": 4,
        "icon": "💬",
        "description": "Właściciel sklepu Maximus (Twój TOP klient) grozi przejściem do konkurencji.",
        "task_type": "ai_conversation",
        "npc_config": {
            "name": "Robert",
            "role": "Właściciel sklepu Maximus (TOP 1 klient - 25k PLN/miesiąc)",
            "personality": "frustrated, disappointed, open to solutions but firm",
            "context": """
Robert prowadzi sklep Maximus od 10 lat. Jest Twoim największym klientem (25k PLN sprzedaży/miesiąc).
            
PROBLEM:
- Konkurencja (firma ACME) zaoferowała mu lepsze warunki: 60 dni płatności (Ty dajesz 30), 5% wyższa marża, dedicated merchandiser
- Robert czuje się niedoceniony - "kupuję za 25k/miesiąc a traktujecie mnie jak małego klienta"
- Rozważa przejście do ACME od przyszłego miesiąca
- Jest otwarty na rozmowę, ale musi zobaczyć konkretną ofertę

UKRYTY KONTEKST (NPC wie, gracz odkryje):
- Robert ma sentyment do GlobalCPG (współpraca 5 lat)
- Jego klienci lubią GlobalFresh (brand loyalty)
- ACME ma gorszy service (dłuższe dostawy, częste braki)
- Robert NIE chce zmian, jeśli nie musi

TWOJE LIMITY:
- Max 45 dni płatności (wymagasz aprobaty managera)
- Możesz dać +3% marży
- Możesz zaoferować merchandising support (1 wizyta/tydzień)
- Możesz zaproponować quarterly business review

CEL ROZMOWY:
- Zatrzymać Roberta
- Wynegocjować win-win deal
- Pokazać wartość GlobalCPG (poza ceną)
""",
            "voice_config": {
                "voice_id": "onwK4e9ZLuTAKqWW03F9",  # ElevenLabs - polski mężczyzna
                "stability": 0.5,
                "similarity_boost": 0.75
            },
            "evaluation_criteria": {
                "empathy": {
                    "weight": 0.25,
                    "description": "Czy pokazałeś zrozumienie dla frustracji Roberta?"
                },
                "value_communication": {
                    "weight": 0.30,
                    "description": "Czy podkreśliłeś wartość GlobalCPG (poza ceną)?"
                },
                "negotiation": {
                    "weight": 0.25,
                    "description": "Czy wynegocjowałeś deal w ramach limitów?"
                },
                "relationship": {
                    "weight": 0.20,
                    "description": "Czy zachowałeś długoterminową relację?"
                }
            },
            "success_threshold": 75  # 75%+ overall score = success
        },
        "base_reward": 1500,
        "reward_4star": 2200,
        "reward_5star": 3000,
        "sales_impact": 25000,   # Zatrzymanie TOP klienta!
        "reputation_impact": 30,
        "time_days": 1
    },
    
    # =========================================================================
    # LEVEL 4-7: TEAM MANAGEMENT
    # =========================================================================
    
    {
        "id": "FMCG-TEAM-001",
        "title": "Onboarding nowego sales repa",
        "category": "team_management",
        "level_required": 4,
        "difficulty": 3,
        "icon": "🎓",
        "description": "Wdrożenie nowego członka zespołu (junior rep) do produktywnej pracy.",
        "scenario": """
**Nowa osoba:** Ania - Junior Sales Rep (pierwszy miesiąc)
**Twoja rola:** Sales Team Leader (zarządzasz Anią + 2 innych repów)

**Sytuacja:**
- Ania ukończyła corporate training (1 tydzień)
- Teraz przechodzi do Twojego zespołu (field training)
- Dostała territory: 20 małych sklepów (detalicznych)
- Target: 10k PLN sprzedaży w pierwszym miesiącu

**Twoje zadanie:**
1. Zaplanuj 2-tygodniowy onboarding
2. Określ KPIs dla Ani (realistyczne!)
3. Zorganizuj joint visits (ile, z kim, gdzie?)
4. Przygotuj checklistę i materiały

**Co napisać:**
- Jak wygląda plan onboardingowy? (dzień po dniu, tydzień 1-2)
- Jakie KPIs ustawisz dla Ani? (calls per day, orders, revenue)
- Jak będziesz monitorować progress?
- Kiedy i jak dasz feedback?
""",
        "task_type": "text",
        "expected_elements": [
            "2-week onboarding plan",
            "KPIs dla new hire",
            "Joint visit strategy",
            "Coaching i feedback schedule"
        ],
        "base_reward": 1000,
        "reward_4star": 1500,
        "reward_5star": 2000,
        "sales_impact": 10000,  # Jeśli dobrze wdrożysz, Ania osiągnie target
        "reputation_impact": 15,
        "time_days": 2
    },
    
    {
        "id": "FMCG-TEAM-002",
        "title": "Coaching underperformera",
        "category": "team_management",
        "level_required": 4,
        "difficulty": 4,
        "icon": "📊",
        "description": "Twój sales rep (Marek) nie osiąga targetów już 2 miesiące. Coaching session.",
        "scenario": """
**Członek zespołu:** Marek - Sales Rep (2 lata w firmie)
**Problem:** Target: 25k PLN/miesiąc | Actual: 18k (lipiec), 16k (sierpień)

**Analiza:**
- Marek ma 30 sklepów w swoim territory
- Call frequency spadła: 4 wizyty/dzień (target: 6)
- Conversion rate: 40% (target: 60%)
- Marek twierdzi że "konkurencja jest zbyt agresywna"

**Dodatkowe informacje:**
- Marek ostatnio rozwiódł się (problemy osobiste?)
- Inni repowie osiągają target bez problemu
- Marek był top performerem rok temu

**Twoje zadanie (coaching session):**
1. Zidentyfikuj root cause (co się naprawdę dzieje?)
2. Stwórz action plan (konkretne kroki)
3. Ustaw follow-up (kiedy, jak często?)
4. Zdecyduj: Czy Marek dostaje drugą szansę, czy PIP (Performance Improvement Plan)?

**Co napisać:**
- Jak poprowadzisz coaching session? (GROW model? Inne?)
- Jakie pytania zadasz Markowi?
- Jaki action plan zaproponujesz?
- Jak będziesz monitorować improvement?
""",
        "task_type": "text",
        "expected_elements": [
            "Coaching approach (GROW, SBI, etc.)",
            "Root cause analysis",
            "Action plan z konkretnymi krokami",
            "Follow-up schedule",
            "Decision: Second chance vs PIP"
        ],
        "base_reward": 800,
        "reward_4star": 1200,
        "reward_5star": 1800,
        "sales_impact": 7000,   # Jeśli Marek się poprawi
        "reputation_impact": 10,
        "time_days": 1
    },
    
    # =========================================================================
    # LEVEL 5-7: AREA/DISTRICT/REGIONAL MANAGER
    # =========================================================================
    
    {
        "id": "FMCG-STRATEGY-001",
        "title": "Quarterly Business Planning",
        "category": "strategy",
        "level_required": 5,
        "difficulty": 4,
        "icon": "📈",
        "description": "Zaplanuj Q4 dla swojego obszaru. Target: +25% YoY wzrost.",
        "scenario": """
**Twoja rola:** Area Sales Manager
**Obszar:** 5 miast w Małopolsce (Kraków, Tarnów, Nowy Sącz, Oświęcim, Zakopane)
**Zespół:** 5 sales repów
**Q3 Results:** 280k PLN sprzedaży
**Q4 Target:** 350k PLN (+25% YoY)

**Dostępne zasoby:**
- Trade marketing budget: 15k PLN
- Możliwość zatrudnienia 1 dodatkowego repa (koszt: 6k PLN/miesiąc)
- Nowy produkt launch: 'WinterWarm' (hot beverages)

**Wyzwania:**
- Q4 = święta (duża konkurencja)
- Zakopane = seasonal (turystyka zimowa - potencjał!)
- Kraków = nasycony rynek (trudno rosnąć)
- Budget limited (15k to niewiele)

**Twoje zadanie:**
1. Zaplanuj Q4 strategy (gdzie skupić effort?)
2. Alokuj budget 15k PLN (marketing, promo, incentives)
3. Zdecyduj: Zatrudnić nowego repa czy nie?
4. Launch plan dla WinterWarm
5. Ustaw KPIs dla zespołu

**Co napisać:**
- Jaka jest Twoja Q4 strategy? (geo focus, product mix, channels)
- Jak wydasz 15k PLN budgetu?
- Czy zatrudnisz nowego repa? Dlaczego tak/nie?
- Jak będziesz mierzyć sukces?
""",
        "task_type": "text",
        "expected_elements": [
            "Q4 strategy (geographic/product focus)",
            "Budget allocation plan",
            "Hiring decision + rationale",
            "WinterWarm launch plan",
            "Team KPIs"
        ],
        "base_reward": 2000,
        "reward_4star": 3000,
        "reward_5star": 4500,
        "sales_impact": 70000,  # Jeśli dobrze zaplanujesz, osiągniesz target
        "reputation_impact": 40,
        "time_days": 3
    },
    
    {
        "id": "FMCG-KEY-002",
        "title": "Negocjacje z Biedronką (National Chain)",
        "category": "key_accounts",
        "level_required": 6,
        "difficulty": 5,
        "icon": "🏢",
        "description": "Wynegocjuj listing w 50 sklepach Biedronka. High stakes!",
        "scenario": """
**Klient:** Biedronka (Category Manager: Katarzyna Wiśniewska)
**Cel:** Listing 5 produktów GlobalCPG w 50 sklepach (pilot program)

**Sytuacja:**
- Biedronka = największa sieć w Polsce (3000+ sklepów)
- Sukces pilotu → expansion do 500+ sklepów
- Konkurencja (Unilever, PepsiCo) już listowane
- Katarzyna: tough negotiator, data-driven, no-nonsense

**Wymagania Biedronki:**
- 60 dni płatności
- 40% marża dla sieci
- Quarterly rebate 5%
- Marketing support: 50k PLN/rok
- Penalty clauses za out-of-stock (OOS)

**Twoje limity:**
- Max 45 dni płatności (wymaga board approval)
- Min 32% marża
- Max 3% rebate
- Marketing budget: 30k PLN/rok
- OOS tolerance: 5% (industry standard)

**Twoje zadanie:**
1. Przygotuj negotiation strategy
2. Wynegocjuj deal w ramach limitów
3. Minimalizuj risk (penalty clauses!)
4. Zaplanuj pilot execution

**Co napisać:**
- Jak przygotowujesz się do rozmowy? (research, data, BATNA)
- Jaka jest Twoja opening offer?
- Jak wynegocjujesz lepsze warunki?
- Co zrobisz z penalty clauses?
- Jak zapewnisz sukces pilotu?
""",
        "task_type": "text",
        "expected_elements": [
            "Negotiation prep (BATNA, data, value prop)",
            "Trade-offs strategy",
            "Risk mitigation (penalties, OOS)",
            "Pilot execution plan",
            "Success metrics"
        ],
        "base_reward": 5000,
        "reward_4star": 7500,
        "reward_5star": 10000,
        "sales_impact": 200000,  # MASSIVE impact jeśli sukces!
        "reputation_impact": 50,
        "time_days": 5
    },
    
    # =========================================================================
    # LEVEL 8-10: DIRECTOR / VP / CSO
    # =========================================================================
    
    {
        "id": "FMCG-CRISIS-001",
        "title": "Product Recall Crisis Management",
        "category": "crisis",
        "level_required": 8,
        "difficulty": 5,
        "icon": "🚨",
        "description": "KRYZYS: GlobalFresh wykryto śladowe ilości szkodliwej substancji. Product recall!",
        "scenario": """
**Sytuacja:** KRYZYS - Product Recall
**Produkt:** GlobalFresh (flagship product, 40% revenue)
**Problem:** Badania laboratoryjne wykryły śladowe ilości benzoesanu sodu (powyżej normy EU)

**Skala:**
- 500,000 butelek na rynku (wartość: 2M PLN)
- 2000+ sklepów (cała Polska)
- Media już informują (Twitter, Facebook)
- Sanepid wymaga natychmiastowego recall

**Twoja rola:** Regional Sales Director
**Odpowiedzialność:** Recall w Twoim regionie (500 sklepów, ~100k butelek)

**Zadania:**
1. Communication plan (kto, kiedy, jak komunikuje?)
   - Zespół sales (50 osób)
   - Sklepy (500 klientów)
   - Konsumenci
   - Media
   
2. Logistics plan (jak zbieramy produkt?)
   - Kto zbiera? (team, external contractors?)
   - Transport i magazynowanie
   - Verification (jak sprawdzamy że wszystko zebrane?)
   
3. Compensation plan
   - Sklepy (lost margin, shelf space)
   - Konsumenci (refunds, goodwill)
   - Team (overtime, stress)
   
4. Reputation recovery
   - Jak odbudować trust?
   - Komunikaty PR
   - Future prevention

**Timeline:** 48 godzin na pełen recall!

**Co napisać:**
- Jak poprowadzisz crisis management? (krok po kroku)
- Communication plan (internal + external)
- Logistics (jak zbierzesz 100k butelek w 48h?)
- Jak minimalizujesz damage (finansowy + reputacyjny)?
- Long-term recovery plan
""",
        "task_type": "text",
        "expected_elements": [
            "Crisis management framework",
            "Communication plan (stakeholder matrix)",
            "Logistics execution plan",
            "Compensation strategy",
            "Reputation recovery roadmap"
        ],
        "base_reward": 3000,
        "reward_4star": 5000,
        "reward_5star": 8000,
        "sales_impact": -100000,  # Massive loss jeśli źle obsłużysz
        "reputation_impact": -50,
        "time_days": 2
    },
    
    {
        "id": "FMCG-STRATEGY-002",
        "title": "Annual Strategic Plan (VP Level)",
        "category": "strategy",
        "level_required": 9,
        "difficulty": 5,
        "icon": "📊",
        "description": "Stwórz roczny plan strategiczny dla całego kraju. Board presentation.",
        "scenario": """
**Twoja rola:** Vice President of Sales (cała Polska)
**Zespół:** 50+ sales reps, 10 area managers, 3 regional directors
**Current year results:** 10M PLN revenue
**Board target:** 15M PLN (+50% YoY) - AGGRESSIVE!

**Dostępne zasoby:**
- Budget: 500k PLN (marketing + expansion)
- Możliwość expansion do nowych kanałów (e-commerce, horeca)
- 2 new product launches (premium segment)
- Hiring budget: 10 new people

**Market context:**
- Retail: Mature, high competition (Unilever, PepsiCo dominują)
- E-commerce: Growing 30% YoY (Twoja obecność: 5%)
- Horeca: Underpenetrated (Twoja obecność: 10%)
- Premium segment: Growing trend

**Board expectations:**
1. Clear strategy (where to play, how to win)
2. Financial projections (revenue, margin, ROI)
3. Org structure (hiring, roles, reporting)
4. Risk assessment
5. Quarterly milestones

**Twoje zadanie:**
Przygotuj 1-page strategic plan:
1. Vision & Mission
2. Strategic priorities (top 3)
3. Channel strategy (retail vs e-commerce vs horeca)
4. Product portfolio strategy
5. Org & talent plan
6. Budget allocation
7. KPIs & milestones
8. Risk mitigation

**Co napisać:**
- Jaka jest Twoja strategic vision?
- Gdzie skupisz effort? (retail, e-commerce, horeca, premium?)
- Jak wydasz 500k PLN?
- Jak osiągniesz +50% wzrost? (realistyczne?)
- Quarterly milestones
""",
        "task_type": "text",
        "expected_elements": [
            "Strategic vision & priorities",
            "Channel strategy + rationale",
            "Budget allocation plan",
            "Org & hiring plan",
            "Financial projections",
            "Quarterly milestones",
            "Risk assessment"
        ],
        "base_reward": 10000,
        "reward_4star": 15000,
        "reward_5star": 20000,
        "sales_impact": 5000000,  # Jeśli strategia się powiedzie!
        "reputation_impact": 100,
        "time_days": 7
    }
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_tasks_for_level(level: int, category: str = None) -> list:
    """
    Zwraca zadania dostępne dla danego poziomu
    
    Args:
        level: Poziom gracza (1-10)
        category: Opcjonalna kategoria (field_sales, key_accounts, etc.)
    
    Returns:
        Lista zadań
    """
    tasks = [t for t in FMCG_TASKS if t["level_required"] <= level]
    
    if category:
        tasks = [t for t in tasks if t["category"] == category]
    
    return tasks

def get_task_by_id(task_id: str) -> dict:
    """Zwraca zadanie po ID"""
    for task in FMCG_TASKS:
        if task["id"] == task_id:
            return task
    return None

def get_random_tasks(level: int, count: int = 3) -> list:
    """Zwraca losowe zadania dla poziomu"""
    import random
    available = get_tasks_for_level(level)
    return random.sample(available, min(count, len(available)))
