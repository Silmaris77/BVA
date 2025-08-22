# Typy neuroliderów - transformacja z degenów na neuroliderów
NEUROLEADER_TYPES = {
    "Neuroanalityk": {
        "description": "Rozważny, skrupulatny, często paraliżowany nadmiarem analiz. Lider, który ma trudności z podejmowaniem decyzji.",
        "tagline": "Unikający Ryzyka",
        "icon": "🧠",
        "strengths": ["Wyczuwa zagrożenia", "Analizuje scenariusze ryzyka", "Dokładność w analizie", "Ostrożność w decyzjach"],
        "challenges": ["Paraliż decyzyjny", "Odkłada decyzje na później", "Lęk przed błędami", "Traci okazje przez zwłokę"],
        "strategy": "Ustal limity czasowe na analizę. Stosuj zasadę 'wystarczająco dobrej decyzji'. Praktykuj podejmowanie małych decyzji.",
        "color": "#2c3e50",
        "supermoc": "Wyczuwa zagrożenia i analizuje scenariusze ryzyka jak nikt inny",
        "slabość": "Traci okazje przez zwłokę"
    },
    "Neuroreaktor": {
        "description": "Lider, który reaguje impulsywnie na stres i emocje, działa błyskawicznie i emocjonalnie, często bez pełnych danych.",
        "tagline": "Impulsywny Strażnik", 
        "icon": "🔥",
        "strengths": ["Szybkie reakcje w kryzysie", "Działanie pod presją", "Natychmiastowe rozwiązywanie problemów", "Energia w trudnych sytuacjach"],
        "challenges": ["Impulsywne decyzje", "Działanie pod wpływem emocji", "Brak pełnej analizy", "Ryzykowne wybory"],
        "strategy": "Techniki oddechowe i mindfulness. Zasada 24 godzin na ważne decyzje. Konsultuj decyzje z zaufaną osobą.",
        "color": "#e74c3c",
        "supermoc": "Zdolność do działania w kryzysie",
        "slabość": "Podejmuje ryzykowne decyzje"
    },
    "Neurobalanser": {
        "description": "Liderzy, którzy potrafią łączyć racjonalność z empatią, podejmując decyzje w oparciu o dane oraz intuicję.",
        "tagline": "Zbalansowany Integrator",
        "icon": "⚖️", 
        "strengths": ["Inteligencja emocjonalna", "Logiczne myślenie", "Elastyczność", "Zrównoważone podejście"],
        "challenges": ["Może zbyt długo analizować", "Wahanie w decyzjach", "Potrzeba znalezienia balansu", "Czasem zbyt ostrożny"],
        "strategy": "Ustal jasne kryteria decyzyjne. Rozwijaj umiejętność facylitacji. Praktykuj podejmowanie decyzji w ograniczonym czasie.",
        "color": "#3498db",
        "supermoc": "Inteligencja emocjonalna + logika",
        "slabość": "Może zbyt długo się wahać"
    },
    "Neuroempata": {
        "description": "Lider, który skupia się na emocjonalnych potrzebach zespołu. Ceni zaufanie, dobre relacje i komunikację w zespole.",
        "tagline": "Architekt Relacji",
        "icon": "🌱",
        "strengths": ["Budowanie więzi", "Empatia", "Zrozumienie potrzeb zespołu", "Tworzenie atmosfery zaufania"],
        "challenges": ["Zbyt emocjonalne podejście", "Trudność z obiektywizmem", "Problem z granicami", "Preferencje osobiste"],
        "strategy": "Rozwijaj umiejętności analityczne. Ustal jasne granice. Ucz się asertywności. Korzystaj z zewnętrznych opinii.",
        "color": "#27ae60",
        "supermoc": "Więzi emocjonalne i zaangażowanie zespołu",
        "slabość": "Trudność z obiektywizmem"
    },
    "Neuroinnowator": {
        "description": "Liderzy, którzy potrafią dostosować swoje podejście do zmieniającej się sytuacji. Są otwarci na nowe rozwiązania, gotowi do eksperymentów.",
        "tagline": "Nawigator Zmiany",
        "icon": "🌊",
        "strengths": ["Adaptacja do zmian", "Innowacyjność", "Eksperymentowanie", "Elastyczność strategii"],
        "challenges": ["Brak stabilności", "Zbyt częste zmiany", "Może frustrować zespół", "Brak konsekwencji"],
        "strategy": "Wprowadź strukturę do swoich innowacji. Rozwijaj umiejętność priorytetyzacji. Komunikuj zmiany efektywnie.",
        "color": "#9b59b6",
        "supermoc": "Adaptacja i innowacyjność", 
        "slabość": "Brak konsekwencji i cierpliwości"
    },
    "Neuroinspirator": {
        "description": "Liderzy, którzy potrafią zmotywować innych do działania dzięki swojej osobowości, wizji i entuzjazmowi.",
        "tagline": "Charyzmatyczny Wizjoner",
        "icon": "🌟",
        "strengths": ["Charyzma", "Motywowanie zespołu", "Wizja przyszłości", "Energia i entuzjazm"],
        "challenges": ["Może zdominować zespół", "Zależność od charyzmy", "Zaniedbywanie autonomii zespołu", "Nadmierna pewność siebie"],
        "strategy": "Rozwijaj zdolność do słuchania. Świadomie buduj autonomię zespołu. Naucz się korzystać z danych w decyzjach.",
        "color": "#f39c12",
        "supermoc": "Wpływ, energia, wizja",
        "slabość": "Może zdominować zespół"
    }
}

# Alias dla kompatybilności z resztą aplikacji - będzie stopniowo zastępowany
DEGEN_TYPES = NEUROLEADER_TYPES

TEST_QUESTIONS = [
    {
        "question": "Jak podejmujesz ważne decyzje w zespole?",
        "options": [
            {"text": "Działam szybko na podstawie intuicji, bez długiej analizy.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizuję wszystkie możliwe scenariusze i ryzyka.", "scores": {"Neuroanalityk": 3}},
            {"text": "Łączę dane z intuicją i emocjami zespołu.", "scores": {"Neurobalanser": 3}},
            {"text": "Skupiam się na tym, jak decyzja wpłynie na zespół.", "scores": {"Neuroempata": 3}},
            {"text": "Testuję różne podejścia i adaptuję się do sytuacji.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspiruję zespół wizją i motywuję do działania.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak reagujesz w sytuacji kryzysu w zespole?",
        "options": [
            {"text": "Reaguję natychmiast, działam pod wpływem adrenaliny.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizuję sytuację, szukam wszystkich możliwych rozwiązań.", "scores": {"Neuroanalityk": 3}},
            {"text": "Zachowuję spokój i łączę logikę z empatią.", "scores": {"Neurobalanser": 3}},
            {"text": "Koncentruję się na wspieraniu zespołu emocjonalnie.", "scores": {"Neuroempata": 3}},
            {"text": "Szybko dostosowuję plan i wprowadzam innowacje.", "scores": {"Neuroinnowator": 3}},
            {"text": "Mobilizuję zespół przez inspirację i wizję.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak motywujesz swój zespół?",
        "options": [
            {"text": "Poprzez szybkie działanie i energię w trudnych momentach.", "scores": {"Neuroreaktor": 3}},
            {"text": "Przez dokładne planowanie i analizę zagrożeń.", "scores": {"Neuroanalityk": 3}},
            {"text": "Łącząc logiczne argumenty z emocjonalnym wsparciem.", "scores": {"Neurobalanser": 3}},
            {"text": "Budując silne relacje i atmosferę zaufania.", "scores": {"Neuroempata": 3}},
            {"text": "Wprowadzając innowacje i nowe sposoby pracy.", "scores": {"Neuroinnowator": 3}},
            {"text": "Poprzez charyzmę, wizję i inspirujące przemówienia.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak podchodzisz do zarządzania zmianami w organizacji?",
        "options": [
            {"text": "Wprowadzam zmiany szybko, reagując na bieżąco.", "scores": {"Neuroreaktor": 3}},
            {"text": "Dokładnie analizuję wszystkie ryzyka przed zmianą.", "scores": {"Neuroanalityk": 3}},
            {"text": "Balansuję między potrzebą zmiany a stabilnością.", "scores": {"Neurobalanser": 3}},
            {"text": "Skupiam się na tym, jak zmiany wpłyną na ludzi.", "scores": {"Neuroempata": 3}},
            {"text": "Eksperymentuję z różnymi podejściami do zmiany.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspiruję zespół wizją przyszłości po zmianie.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jaki jest Twój styl komunikacji z zespołem?",
        "options": [
            {"text": "Bezpośredni i szybki, szczególnie w sytuacjach kryzysowych.", "scores": {"Neuroreaktor": 3}},
            {"text": "Ostrożny i przemyślany, przedstawiam wszystkie fakty.", "scores": {"Neuroanalityk": 3}},
            {"text": "Łączę logiczne argumenty z uwzględnieniem emocji.", "scores": {"Neurobalanser": 3}},
            {"text": "Empatyczny i wspierający, słucham potrzeb zespołu.", "scores": {"Neuroempata": 3}},
            {"text": "Elastyczny, dostosowuję styl do sytuacji i osoby.", "scores": {"Neuroinnowator": 3}},
            {"text": "Charyzmatyczny i inspirujący, motywuję przez wizję.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak zarządzasz konfliktami w zespole?",
        "options": [
            {"text": "Reaguję natychmiast, chcę szybko rozwiązać problem.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizuję przyczyny konfliktu i szukam optymalnego rozwiązania.", "scores": {"Neuroanalityk": 3}},
            {"text": "Szukam rozwiązań uwzględniających zarówno fakty jak i emocje.", "scores": {"Neurobalanser": 3}},
            {"text": "Koncentruję się na budowaniu porozumienia i mediacji.", "scores": {"Neuroempata": 3}},
            {"text": "Testuję różne sposoby rozwiązania, dostosowując podejście.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspiruję strony do wspólnej wizji i celów.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak budujemy strategię zespołu?",
        "options": [
            {"text": "Szybko reagujemy na sytuację, działamy intuicyjnie.", "scores": {"Neuroreaktor": 3}},
            {"text": "Dokładnie analizujemy wszystkie możliwe scenariusze.", "scores": {"Neuroanalityk": 3}},
            {"text": "Łączymy analizę danych z intuicją i opiniami zespołu.", "scores": {"Neurobalanser": 3}},
            {"text": "Uwzględniamy potrzeby i możliwości każdego członka zespołu.", "scores": {"Neuroempata": 3}},
            {"text": "Pozostajemy elastyczni i gotowi na adaptację strategii.", "scores": {"Neuroinnowator": 3}},
            {"text": "Tworzymy inspirującą wizję, która motywuje do działania.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak reagujesz na niepowodzenia zespołu?",
        "options": [
            {"text": "Działam natychmiast, by jak najszybciej naprawić sytuację.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizuję dokładnie przyczyny niepowodzenia.", "scores": {"Neuroanalityk": 3}},
            {"text": "Wyciągam wnioski i równoważę uczenie się z wsparciem zespołu.", "scores": {"Neurobalanser": 3}},
            {"text": "Skupiam się na wspieraniu zespołu i odbudowie morale.", "scores": {"Neuroempata": 3}},
            {"text": "Traktuję to jako okazję do innowacji i zmiany podejścia.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspiruję zespół do wyciągnięcia wniosków i dalszego rozwoju.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak podejmujesz decyzje pod presją czasu?",
        "options": [
            {"text": "Działam instynktownie i szybko, ufam intuicji.", "scores": {"Neuroreaktor": 3}},
            {"text": "Stresuję się, potrzebuję więcej czasu na analizę.", "scores": {"Neuroanalityk": 3}},
            {"text": "Szybko analizuję kluczowe fakty i uwzględniam intuicję.", "scores": {"Neurobalanser": 3}},
            {"text": "Konsultuję się z zespołem, uwzględniam ich opinie.", "scores": {"Neuroempata": 3}},
            {"text": "Testuję szybkie rozwiązania i dostosowuję w locie.", "scores": {"Neuroinnowator": 3}},
            {"text": "Mobilizuję zespół energią i wizją szybkiego działania.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak rozwijasz swój zespół?",
        "options": [
            {"text": "Przez wyzwania i sytuacje kryzysowe, które hartują.", "scores": {"Neuroreaktor": 3}},
            {"text": "Poprzez dokładną analizę mocnych stron i planowanie rozwoju.", "scores": {"Neuroanalityk": 3}},
            {"text": "Łącząc rozwój zawodowy z rozwojem osobistym.", "scores": {"Neurobalanser": 3}},
            {"text": "Budując silne relacje i wspierając indywidualnie.", "scores": {"Neuroempata": 3}},
            {"text": "Wprowadzając innowacyjne metody i eksperymentując.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspirując do ciągłego rozwoju i osiągania celów.", "scores": {"Neuroinspirator": 3}}
        ]
    }
]
