"""
Test Wielorakich Inteligencji Gardnera
Multiple Intelligences Test based on Howard Gardner's theory
"""

from typing import Dict, List, Tuple
from datetime import datetime

def get_mi_test_questions() -> List[Dict]:
    """Zwraca listę 40 pytań testowych (5 na każdą inteligencję)"""
    
    questions = []
    
    # 1. JĘZYKOWA (Verbal-Linguistic)
    questions.extend([
        {
            "id": "L1",
            "text": "Lubię pisać (emaile, raporty, artykuły, dziennik) i jest mi to łatwe.",
            "category": "linguistic"
        },
        {
            "id": "L2",
            "text": "Łatwo zapamiętuje nowe słowa, cytaty i informacje słowne.",
            "category": "linguistic"
        },
        {
            "id": "L3",
            "text": "Czytanie książek i artykułów to mój ulubiony sposób na naukę.",
            "category": "linguistic"
        },
        {
            "id": "L4",
            "text": "Potrafię przekonująco argumentować i lubię debaty/dyskusje.",
            "category": "linguistic"
        },
        {
            "id": "L5",
            "text": "Gdy wyjaśniam coś innym, używam metafor, historii i analogii.",
            "category": "linguistic"
        }
    ])
    
    # 2. LOGICZNO-MATEMATYCZNA (Logical-Mathematical)
    questions.extend([
        {
            "id": "M1",
            "text": "Lubię rozwiązywać problemy logiczne, łamigłówki i zagadki.",
            "category": "logical"
        },
        {
            "id": "M2",
            "text": "Dobrze radzę sobie z liczbami, statystyką i analizą danych.",
            "category": "logical"
        },
        {
            "id": "M3",
            "text": "Szukam wzorców, sekwencji i logicznych powiązań między faktami.",
            "category": "logical"
        },
        {
            "id": "M4",
            "text": "Preferuję systematyczne, krok-po-kroku podejście do zadań.",
            "category": "logical"
        },
        {
            "id": "M5",
            "text": "Przy podejmowaniu decyzji bazuję na danych i analizie, nie emocjach.",
            "category": "logical"
        }
    ])
    
    # 3. WIZUALNO-PRZESTRZENNA (Visual-Spatial)
    questions.extend([
        {
            "id": "V1",
            "text": "Najlepiej uczę się z diagramów, map, infografik i schematów.",
            "category": "visual"
        },
        {
            "id": "V2",
            "text": "Mam dobry zmysł orientacji i łatwo wyobrażam sobie przestrzenie 3D.",
            "category": "visual"
        },
        {
            "id": "V3",
            "text": "Lubię rysować, szkicować, robić mind maps i wizualne notatki.",
            "category": "visual"
        },
        {
            "id": "V4",
            "text": "Kolory, design i estetyka są dla mnie ważne.",
            "category": "visual"
        },
        {
            "id": "V5",
            "text": "Łatwo zapamiętuje twarze, miejsca i wizualne szczegóły.",
            "category": "visual"
        }
    ])
    
    # 4. MUZYCZNA (Musical-Rhythmic)
    questions.extend([
        {
            "id": "U1",
            "text": "Muzyka pomaga mi się koncentrować lub relaksować.",
            "category": "musical"
        },
        {
            "id": "U2",
            "text": "Łatwo zapamiętuje melodie, rytmy i potrafię je odtworzyć.",
            "category": "musical"
        },
        {
            "id": "U3",
            "text": "Gram na instrumencie lub chciałbym/chciałabym nauczyć się grać.",
            "category": "musical"
        },
        {
            "id": "U4",
            "text": "Zwracam uwagę na intonację, ton głosu i 'muzykalność' mowy.",
            "category": "musical"
        },
        {
            "id": "U5",
            "text": "Często nucę, tupię rytm lub mam 'piosenki w głowie'.",
            "category": "musical"
        }
    ])
    
    # 5. KINESTETYCZNA (Bodily-Kinesthetic)
    questions.extend([
        {
            "id": "K1",
            "text": "Najlepiej uczę się poprzez praktykę, wykonywanie i 'hands-on' doświadczenie.",
            "category": "kinesthetic"
        },
        {
            "id": "K2",
            "text": "Lubię aktywność fizyczną, sport lub pracę manualną.",
            "category": "kinesthetic"
        },
        {
            "id": "K3",
            "text": "Trudno mi siedzieć długo w miejscu - potrzebuję ruchu.",
            "category": "kinesthetic"
        },
        {
            "id": "K4",
            "text": "Mam dobrą koordynację ruchową i sprawność fizyczną.",
            "category": "kinesthetic"
        },
        {
            "id": "K5",
            "text": "Gdy myślę, często gestykuluję lub przemieszczam się.",
            "category": "kinesthetic"
        }
    ])
    
    # 6. INTERPERSONALNA (Interpersonal)
    questions.extend([
        {
            "id": "P1",
            "text": "Dobrze rozumiem emocje, motywacje i perspektywy innych ludzi.",
            "category": "interpersonal"
        },
        {
            "id": "P2",
            "text": "Lubię pracować w zespole i łatwo buduję relacje.",
            "category": "interpersonal"
        },
        {
            "id": "P3",
            "text": "Ludzie często przychodzą do mnie po radę lub wsparcie.",
            "category": "interpersonal"
        },
        {
            "id": "P4",
            "text": "Łatwo rozwiązuję konflikty i medionuję między ludźmi.",
            "category": "interpersonal"
        },
        {
            "id": "P5",
            "text": "Najlepiej uczę się w dyskusjach, grupowych projektach i networkingu.",
            "category": "interpersonal"
        }
    ])
    
    # 7. INTRAPERSONALNA (Intrapersonal)
    questions.extend([
        {
            "id": "I1",
            "text": "Dobrze znam swoje mocne/słabe strony, wartości i emocje.",
            "category": "intrapersonal"
        },
        {
            "id": "I2",
            "text": "Regularnie reflektuję nad sobą (dziennik, medytacja, coaching).",
            "category": "intrapersonal"
        },
        {
            "id": "I3",
            "text": "Potrzebuję czasu sam/sama na regenerację i myślenie.",
            "category": "intrapersonal"
        },
        {
            "id": "I4",
            "text": "Mam jasno określone cele życiowe i planuję swoją przyszłość.",
            "category": "intrapersonal"
        },
        {
            "id": "I5",
            "text": "Najlepiej uczę się w samodzielnej pracy, w swoim tempie.",
            "category": "intrapersonal"
        }
    ])
    
    # 8. PRZYRODNICZA (Naturalistic)
    questions.extend([
        {
            "id": "N1",
            "text": "Czuję się świetnie w naturze (las, góry, nad wodą).",
            "category": "naturalistic"
        },
        {
            "id": "N2",
            "text": "Interesuję się ekologią, biologią, geografią lub ochroną środowiska.",
            "category": "naturalistic"
        },
        {
            "id": "N3",
            "text": "Łatwo rozpoznaję i klasyfikuję rośliny, zwierzęta lub zjawiska przyrodnicze.",
            "category": "naturalistic"
        },
        {
            "id": "N4",
            "text": "Lubię obserwować, eksperymentować i odkrywać wzorce w przyrodzie.",
            "category": "naturalistic"
        },
        {
            "id": "N5",
            "text": "Tematy związane z naturą pomagają mi zrozumieć złożone koncepcje.",
            "category": "naturalistic"
        }
    ])
    
    return questions


def get_intelligence_descriptions() -> Dict:
    """Zwraca szczegółowe opisy każdej inteligencji"""
    
    return {
        "linguistic": {
            "name": "Językowa (Verbal-Linguistic)",
            "icon": "🗣️",
            "short_desc": "Umiejętność posługiwania się słowem mówionym i pisanym",
            "strengths": [
                "Świetna komunikacja werbalna i pisemna",
                "Łatwość w uczeniu się języków",
                "Umiejętność przekonującego argumentowania",
                "Kreatywne pisanie i storytelling",
                "Pamięć do słów i cytatów"
            ],
            "careers": "Pisarz, dziennikarz, prawnik, nauczyciel, copywriter, tłumacz, poeta, redaktor",
            "learning": "Czytaj książki, słuchaj podcastów, pisz notatki, dyskutuj, ucz się przez storytelling",
            "famous": "William Shakespeare, Maya Angelou, Barack Obama, J.K. Rowling"
        },
        "logical": {
            "name": "Logiczno-matematyczna",
            "icon": "🔢",
            "short_desc": "Zdolność do logicznego myślenia i rozumowania matematycznego",
            "strengths": [
                "Analityczne myślenie i rozwiązywanie problemów",
                "Umiejętność pracy z danymi i liczbami",
                "Rozpoznawanie wzorców i sekwencji",
                "Systematyczne podejście do zadań",
                "Zdolności dedukc i indukcyjne"
            ],
            "careers": "Analityk, programista, inżynier, naukowiec, ekonomista, matematyk, statystyk",
            "learning": "Rozwiązuj zagadki, analizuj dane, twórz modele, eksperymentuj, klasyfikuj",
            "famous": "Albert Einstein, Marie Curie, Stephen Hawking, Ada Lovelace"
        },
        "visual": {
            "name": "Wizualno-przestrzenna",
            "icon": "🎨",
            "short_desc": "Zdolność do myślenia obrazami i wizualizacji przestrzennej",
            "strengths": [
                "Myślenie obrazami i przestrzenne",
                "Umiejętność wizualizacji i projektowania",
                "Dobry zmysł estetyczny",
                "Pamięć wzrokowa",
                "Wyczucie proporcji i układu"
            ],
            "careers": "Designer, architekt, artysta, fotograf, pilot, chirurg, grafik, animator",
            "learning": "Twórz mind maps, używaj infografik, szkicuj, wizualizuj, koloruj notatki",
            "famous": "Leonardo da Vinci, Pablo Picasso, Frank Lloyd Wright, Steve Jobs"
        },
        "musical": {
            "name": "Muzyczna (Musical-Rhythmic)",
            "icon": "🎵",
            "short_desc": "Wrażliwość na rytm, melodię i struktury dźwiękowe",
            "strengths": [
                "Wyczucie rytmu i melodii",
                "Wrażliwość na dźwięki i intonację",
                "Umiejętność kompozycji",
                "Dobra pamięć słuchowa",
                "Rozpoznawanie struktur muzycznych"
            ],
            "careers": "Muzyk, kompozytor, producent muzyczny, sound designer, terapeuta muzyczny, DJ",
            "learning": "Słuchaj muzyki podczas nauki, twórz jingles, używaj rytmu, nucąc materiał",
            "famous": "Mozart, Beethoven, Beyoncé, Hans Zimmer"
        },
        "kinesthetic": {
            "name": "Kinestetyczna (Bodily-Kinesthetic)",
            "icon": "🤸",
            "short_desc": "Umiejętność kontroli ciała i manualnej sprawności",
            "strengths": [
                "Doskonała koordynacja i sprawność",
                "Uczenie się przez działanie",
                "Umiejętności manualne",
                "Świadomość ciała",
                "Pamięć mięśniowa"
            ],
            "careers": "Sportowiec, tancerz, chirurg, rzemieślnik, instruktor fitness, aktor, fizjoterapeuta",
            "learning": "Praktykuj hands-on, rób przerwy na ruch, gestykuluj, używaj manipulatywów",
            "famous": "Michael Jordan, Simone Biles, Charlie Chaplin, Martha Graham"
        },
        "interpersonal": {
            "name": "Interpersonalna",
            "icon": "👥",
            "short_desc": "Zdolność do rozumienia i skutecznej komunikacji z innymi",
            "strengths": [
                "Empatia i rozumienie innych",
                "Świetna komunikacja i przywództwo",
                "Umiejętność pracy w zespole",
                "Rozwiązywanie konfliktów",
                "Odczytywanie emocji i intencji"
            ],
            "careers": "Manager, coach, psycholog, sprzedawca, HR, polityk, nauczyciel, mediator",
            "learning": "Ucz się w grupach, dyskutuj, ucz innych, networkuj, role-play",
            "famous": "Oprah Winfrey, Nelson Mandela, Mahatma Gandhi, Dale Carnegie"
        },
        "intrapersonal": {
            "name": "Intrapersonalna",
            "icon": "🧘",
            "short_desc": "Głęboka samoświadomość i zdolność do autorefleksji",
            "strengths": [
                "Wysoka samoświadomość",
                "Umiejętność autorefleksji",
                "Samodzielność w działaniu",
                "Jasne cele i wartości",
                "Inteligencja emocjonalna (wobec siebie)"
            ],
            "careers": "Przedsiębiorca, filozof, pisarz, psycholog, life coach, terapeuta, badacz",
            "learning": "Ucz się samodzielnie, reflektuj, prowadź dziennik, medytuj, ustal cele",
            "famous": "Sigmund Freud, Viktor Frankl, Dalai Lama, Carl Jung"
        },
        "naturalistic": {
            "name": "Przyrodnicza (Naturalistic)",
            "icon": "🌿",
            "short_desc": "Wrażliwość na przyrodę i umiejętność klasyfikacji",
            "strengths": [
                "Wrażliwość na przyrodę",
                "Umiejętność obserwacji i klasyfikacji",
                "Zrozumienie ekosystemów",
                "Holistyczne myślenie",
                "Rozpoznawanie wzorców naturalnych"
            ],
            "careers": "Biolog, ekolog, weterynarz, farmer, geolog, ranger, botanik, zoolog",
            "learning": "Ucz się outdoors, używaj analogii z natury, obserwuj, klasyfikuj, eksperymentuj",
            "famous": "Charles Darwin, Jane Goodall, David Attenborough, Rachel Carson"
        }
    }


def calculate_mi_scores(answers: Dict[str, int]) -> Dict:
    """
    Oblicza wyniki testu na podstawie odpowiedzi
    
    Args:
        answers: Dict z kluczami będącymi ID pytań (L1, M1, etc.) i wartościami 1-5
    
    Returns:
        Dict z wynikami, procentami, top 3 i bottom 2 inteligencjami
    """
    
    # Inicjalizacja scores
    scores = {
        "linguistic": 0,
        "logical": 0,
        "visual": 0,
        "musical": 0,
        "kinesthetic": 0,
        "interpersonal": 0,
        "intrapersonal": 0,
        "naturalistic": 0
    }
    
    # Mapowanie ID pytań na kategorie
    question_categories = {
        "L1": "linguistic", "L2": "linguistic", "L3": "linguistic", "L4": "linguistic", "L5": "linguistic",
        "M1": "logical", "M2": "logical", "M3": "logical", "M4": "logical", "M5": "logical",
        "V1": "visual", "V2": "visual", "V3": "visual", "V4": "visual", "V5": "visual",
        "U1": "musical", "U2": "musical", "U3": "musical", "U4": "musical", "U5": "musical",
        "K1": "kinesthetic", "K2": "kinesthetic", "K3": "kinesthetic", "K4": "kinesthetic", "K5": "kinesthetic",
        "P1": "interpersonal", "P2": "interpersonal", "P3": "interpersonal", "P4": "interpersonal", "P5": "interpersonal",
        "I1": "intrapersonal", "I2": "intrapersonal", "I3": "intrapersonal", "I4": "intrapersonal", "I5": "intrapersonal",
        "N1": "naturalistic", "N2": "naturalistic", "N3": "naturalistic", "N4": "naturalistic", "N5": "naturalistic"
    }
    
    # Suma punktów dla każdej kategorii
    for question_id, answer_value in answers.items():
        if question_id in question_categories:
            category = question_categories[question_id]
            scores[category] += answer_value
    
    # Oblicz procenty (max 25 punktów = 5 pytań × 5 punktów)
    max_score = 25
    percentages = {
        category: (score / max_score) * 100
        for category, score in scores.items()
    }
    
    # Identyfikuj top 3 i bottom 2
    sorted_scores = sorted(percentages.items(), key=lambda x: x[1], reverse=True)
    top_3 = sorted_scores[:3]
    bottom_2 = sorted_scores[-2:]
    
    # Oblicz profil balance (różnica między najwyższym a najniższym)
    balance_score = top_3[0][1] - bottom_2[-1][1]
    
    # Interpretacja balance
    if balance_score < 30:
        balance_interpretation = "Zrównoważony - masz dobrze rozwinięte różne inteligencje"
    elif balance_score < 50:
        balance_interpretation = "Umiarkowanie wyspecjalizowany - wyraźne preferencje z dobrą elastycznością"
    else:
        balance_interpretation = "Wyspecjalizowany - silne dominujące inteligencje"
    
    return {
        "scores": scores,
        "percentages": percentages,
        "top_3": top_3,
        "bottom_2": bottom_2,
        "balance_score": balance_score,
        "balance_interpretation": balance_interpretation,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def get_bva_recommendations(top_intelligences: List[str]) -> Dict:
    """
    Zwraca spersonalizowane rekomendacje dla BVA na podstawie profilu inteligencji
    
    Args:
        top_intelligences: Lista nazw dominujących inteligencji (np. ['linguistic', 'interpersonal'])
    
    Returns:
        Dict z rekomendacjami modułów, narzędzi i wskazówek
    """
    
    recommendations_map = {
        "linguistic": {
            "modules": ["📝 Email Templates", "🗣️ CIQ Examples", "📚 Case Studies", "📖 Artykuły i e-booki"],
            "tools": ["AI Coach (tekstowy feedback)", "Conversation Analyzer (analiza słów)", "Transkrypcje rozmów"],
            "tips": [
                "Rób notatki tekstowe podczas ćwiczeń",
                "Czytaj transkrypcje rozmów biznesowych",
                "Pisz refleksje w dzienniku rozwoju",
                "Uczestniczy w dyskusjach na forum",
                "Twórz własne storytelling z case studies"
            ],
            "content_preference": ["text", "articles", "ebooks", "discussions"]
        },
        "logical": {
            "modules": ["📊 Analytics & Metrics", "🎯 Level Detector", "📈 Progress Tracking", "🔢 Dashboard"],
            "tools": ["Sentiment Analysis (dane liczbowe)", "Escalation Monitoring (wskaźniki)", "Statystyki CIQ"],
            "tips": [
                "Śledź swoje statystyki i wykresy postępów",
                "Analizuj wzorce w swoich rozmowach",
                "Twórz własne systemy oceny skuteczności",
                "Eksperymentuj z parametrami AI",
                "Buduj modele predykcyjne swoich wyników"
            ],
            "content_preference": ["data", "charts", "analytics", "models"]
        },
        "visual": {
            "modules": ["🎨 Infografiki CIQ", "🗺️ Mind Maps", "📊 Dashboard wizualny", "🖼️ Schematy"],
            "tools": ["Wykresy radarowe", "Color-coded feedback", "Wizualne raporty PDF", "Diagramy poziomów"],
            "tips": [
                "Używaj kolorowych notatek i highlightów",
                "Twórz schematy i flowcharty rozmów",
                "Wizualizuj swoje cele rozwojowe",
                "Zapisuj screenshoty kluczowych postępów",
                "Projektuj własne dashboardy"
            ],
            "content_preference": ["infographics", "videos", "diagrams", "mindmaps"]
        },
        "musical": {
            "modules": ["🎵 Audiobooki", "🎧 Podcasty o przywództwie", "🔊 Nagrania rozmów"],
            "tools": ["Analiza tonu głosu", "Rytm konwersacji", "Intonacja w CIQ", "Audio feedback"],
            "tips": [
                "Słuchaj nagrań przykładowych rozmów",
                "Zwracaj uwagę na ton i intonację w symulacjach",
                "Nagraj własne odpowiedzi i odsłuchaj je",
                "Ucz się z muzyką w tle (jeśli pomaga)",
                "Analizuj 'melodię' skutecznej komunikacji"
            ],
            "content_preference": ["audio", "podcasts", "recordings", "voice_analysis"]
        },
        "kinesthetic": {
            "modules": ["🎮 Business Simulator", "🤝 Role-play exercises", "🏃 Action Challenges", "💼 Praktyczne scenariusze"],
            "tools": ["Interaktywny symulator", "Praktyczne ćwiczenia", "Real-time practice", "Hands-on tasks"],
            "tips": [
                "Rób symulacje stojąc lub chodząc",
                "Gestykuluj podczas przećwiczywania odpowiedzi",
                "Praktykuj od razu w rzeczywistych sytuacjach",
                "Rób krótkie przerwy na ruch co 20 minut",
                "Fizycznie odgrywaj trudne rozmowy"
            ],
            "content_preference": ["simulations", "exercises", "practice", "interactive"]
        },
        "interpersonal": {
            "modules": ["👥 Team Scenarios", "🤝 Conflict Resolution", "💬 Group Discussions", "🎭 Role-playing"],
            "tools": ["Emotion Detector", "Intent Analysis", "AI Coach (empatia)", "Feedback od innych"],
            "tips": [
                "Ucz się z innymi użytkownikami (study groups)",
                "Dziel się swoimi casami na forum",
                "Analizuj emocje i motywacje rozmówców",
                "Praktykuj z partnerem treningowym",
                "Zbieraj feedback od zespołu"
            ],
            "content_preference": ["discussions", "case_studies", "group_work", "networking"]
        },
        "intrapersonal": {
            "modules": ["🧘 Self-reflection Tools", "📔 Development Journal", "🎯 Personal Goals", "🪞 Autoewaluacja"],
            "tools": ["Leadership Profile", "Self-assessment quizy", "Progress tracking", "Dziennik rozwoju"],
            "tips": [
                "Prowadź regularny dziennik rozwoju",
                "Rób cotygodniową autorefleksję",
                "Ucz się w swoim własnym tempie",
                "Medytuj przed trudnymi rozmowami",
                "Ustalaj osobiste cele i mierz je"
            ],
            "content_preference": ["self_reflection", "journaling", "solo_practice", "goals"]
        },
        "naturalistic": {
            "modules": ["🌿 Analogie z natury", "🔄 Systemy i wzorce", "🌍 Holistyczne myślenie", "📊 Ekosystemy"],
            "tools": ["Pattern recognition", "System dynamics", "Ecosystem thinking", "Wzorce behawioralne"],
            "tips": [
                "Ucz się outdoors gdy to możliwe",
                "Szukaj wzorców w zachowaniach ludzi",
                "Myśl o zespole jako o ekosystemie",
                "Używaj metafor przyrodniczych w komunikacji",
                "Obserwuj 'naturalne cykle' w biznesie"
            ],
            "content_preference": ["patterns", "systems", "metaphors", "holistic"]
        }
    }
    
    # Zbierz rekomendacje dla top inteligencji
    all_modules = []
    all_tools = []
    all_tips = []
    content_types = []
    
    for intelligence in top_intelligences:
        if intelligence in recommendations_map:
            recs = recommendations_map[intelligence]
            all_modules.extend(recs["modules"])
            all_tools.extend(recs["tools"])
            all_tips.extend(recs["tips"])
            content_types.extend(recs["content_preference"])
    
    # Usuń duplikaty zachowując kolejność
    all_modules = list(dict.fromkeys(all_modules))
    all_tools = list(dict.fromkeys(all_tools))
    all_tips = list(dict.fromkeys(all_tips))
    content_types = list(dict.fromkeys(content_types))
    
    return {
        "modules": all_modules,
        "tools": all_tools,
        "tips": all_tips,
        "content_types": content_types,
        "detailed_recommendations": {
            intel: recommendations_map[intel] 
            for intel in top_intelligences 
            if intel in recommendations_map
        }
    }
