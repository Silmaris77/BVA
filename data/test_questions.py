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


TEST_QUESTIONS = [
    {
        "question": "Jak reagujesz, gdy cena aktywa gwałtownie wzrasta?",
        "options": [
            {"text": "Natychmiast kupuję, nie analizując zbyt dużo.", "scores": {"YOLO Degen": 3, "Hype Degen": 1}},
            {"text": "Zastanawiam się, czy to zgodne z moją strategią.", "scores": {"Strategist Degen": 3}},
            {"text": "Czuję euforię i szybko kupuję.", "scores": {"Emo Degen": 3, "YOLO Degen": 1}},
            {"text": "Czekam na spokojniejszy moment na rynku.", "scores": {"Zen Degen": 3}},
            {"text": "Analizuję dane, by przewidzieć kolejny ruch.", "scores": {"Mad Scientist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Sprawdzam dane historyczne i ryzyko.", "scores": {"Spreadsheet Degen": 3, "Strategist Degen": 1}},
            {"text": "Analizuję kontekst i większy trend.", "scores": {"Meta Degen": 3}},
            {"text": "Kupuję, bo widzę, że wszyscy o tym mówią.", "scores": {"Hype Degen": 3, "YOLO Degen": 1}}
        ]
    },
    {
        "question": "Co robisz, gdy rynek zaczyna się zmieniać w sposób nieprzewidywalny?",
        "options": [
            {"text": "Działam natychmiast  instynkt to podstawa.", "scores": {"YOLO Degen": 3, "Emo Degen": 1}},
            {"text": "Analizuję dane, zanim coś zrobię.", "scores": {"Strategist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Wpadam w panikę, sprzedaję wszystko.", "scores": {"Emo Degen": 3}},
            {"text": "Zachowuję spokój, nic nie zmieniam.", "scores": {"Zen Degen": 3}},
            {"text": "Tworzę własny model predykcyjny.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Odświeżam arkusze z analizami.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Szukam głębszego sensu zmian.", "scores": {"Meta Degen": 3}},
            {"text": "Reaguję tak, jak społeczność Twittera.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak często zmieniasz swoje decyzje inwestycyjne?",
        "options": [
            {"text": "Ciągle  każda okazja to nowy ruch.", "scores": {"YOLO Degen": 3, "Hype Degen": 1}},
            {"text": "Tylko gdy plan tego wymaga.", "scores": {"Strategist Degen": 3}},
            {"text": "Za każdym razem, gdy się zestresuję.", "scores": {"Emo Degen": 3}},
            {"text": "Prawie nigdy  spokój to podstawa.", "scores": {"Zen Degen": 3}},
            {"text": "Kiedy dane dają zielone światło.", "scores": {"Mad Scientist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Gdy model pokazuje, że to uzasadnione.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "W rytmie zmian rynkowych i geopolitycznych.", "scores": {"Meta Degen": 3}},
            {"text": "Gdy coś trenduje  wchodzę!", "scores": {"Hype Degen": 3, "YOLO Degen": 1}}
        ]
    },
    {
        "question": "Jak wygląda Twoje poranne podejście do inwestowania?",
        "options": [
            {"text": "Włączam aplikację i kupuję na ślepo.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprawdzam moją strategię i wykonuję plan.", "scores": {"Strategist Degen": 3}},
            {"text": "Sprawdzam nastroje i kieruję się emocjami.", "scores": {"Emo Degen": 3}},
            {"text": "Medytuję, zanim podejmę decyzję.", "scores": {"Zen Degen": 3}},
            {"text": "Odpalam skrypty z analizami.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Aktualizuję swój Excel z danymi.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Przeglądam światowe wydarzenia.", "scores": {"Meta Degen": 3}},
            {"text": "Sprawdzam TikToka i Twittera.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak się czujesz, gdy Twoja inwestycja traci na wartości?",
        "options": [
            {"text": "Trudno, YOLO  lecę dalej.", "scores": {"YOLO Degen": 3}},
            {"text": "To część planu, mam to pod kontrolą.", "scores": {"Strategist Degen": 3}},
            {"text": "Jestem załamany, nie mogę spać.", "scores": {"Emo Degen": 3}},
            {"text": "Akceptuję to. Taki jest rynek.", "scores": {"Zen Degen": 3}},
            {"text": "Analizuję, dlaczego tak się stało.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Aktualizuję plik i zmieniam parametry.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Sprawdzam, czy to nie wynik globalnych trendów.", "scores": {"Meta Degen": 3}},
            {"text": "Obwiniam influencerów z internetu.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak wybierasz projekt lub spółkę do inwestycji?",
        "options": [
            {"text": "Klikam w to, co akurat wygląda fajnie.", "scores": {"YOLO Degen": 3}},
            {"text": "Szukam zgodności z moją strategią.", "scores": {"Strategist Degen": 3}},
            {"text": "Wybieram to, co wzbudza emocje.", "scores": {"Emo Degen": 3}},
            {"text": "Wybieram intuicyjnie, po przemyśleniu.", "scores": {"Zen Degen": 3}},
            {"text": "Patrzę na technologię i innowacyjność.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Analizuję wskaźniki i liczby.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Czytam białą księgę i analizuję ekosystem.", "scores": {"Meta Degen": 3}},
            {"text": "To, co trenduje na socialach.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak planujesz swoje portfolio?",
        "options": [
            {"text": "Nie planuję  pełen spontan.", "scores": {"YOLO Degen": 3}},
            {"text": "Mam rozpisany plan i cel.", "scores": {"Strategist Degen": 3}},
            {"text": "Dodaję i usuwam po impulsie.", "scores": {"Emo Degen": 3}},
            {"text": "Portfolio to droga  zmienia się naturalnie.", "scores": {"Zen Degen": 3}},
            {"text": "Symuluję wiele scenariuszy.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Optymalizuję strukturę w arkuszu kalkulacyjnym.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Układam pod mega trendy i narracje.", "scores": {"Meta Degen": 3}},
            {"text": "Kupuję to, co polecają inni.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz w dniu dużej korekty rynkowej?",
        "options": [
            {"text": "Wchodzę all-in w dołku.", "scores": {"YOLO Degen": 3}},
            {"text": "Trzymam się planu.", "scores": {"Strategist Degen": 3}},
            {"text": "Wpadam w panikę i wyprzedaję.", "scores": {"Emo Degen": 3}},
            {"text": "Obserwuję i nie działam pochopnie.", "scores": {"Zen Degen": 3}},
            {"text": "Weryfikuję modele i dane.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Uaktualniam wyceny i alokację.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Szacuję konsekwencje makroekonomiczne.", "scores": {"Meta Degen": 3}},
            {"text": "Patrzę co robią znani YouTuberzy.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jaki jest Twój ulubiony sposób zdobywania wiedzy o inwestowaniu?",
        "options": [
            {"text": "Z memów i shortów.", "scores": {"YOLO Degen": 3}},
            {"text": "Z książek i analiz.", "scores": {"Strategist Degen": 3}},
            {"text": "Z podcastów o sukcesach i porażkach.", "scores": {"Emo Degen": 3}},
            {"text": "Z doświadczenia i uważności.", "scores": {"Zen Degen": 3}},
            {"text": "Z badań naukowych.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Z raportów i arkuszy.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Z rozmów i debat o przyszłości.", "scores": {"Meta Degen": 3}},
            {"text": "Z komentarzy pod filmami influencerów.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak oceniasz sukces swojej inwestycji?",
        "options": [
            {"text": "Czy zrobiłem szybki zysk?", "scores": {"YOLO Degen": 3}},
            {"text": "Czy osiągnąłem cel zgodnie z planem?", "scores": {"Strategist Degen": 3}},
            {"text": "Czy poczułem się z tym dobrze?", "scores": {"Emo Degen": 3}},
            {"text": "Czy nie cierpiałem w procesie?", "scores": {"Zen Degen": 3}},
            {"text": "Czy moja hipoteza się potwierdziła?", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Czy ROI było zgodne z kalkulacją?", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Czy wpisało się to w większy trend?", "scores": {"Meta Degen": 3}},
            {"text": "Czy znajomi byli pod wrażeniem?", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak podejmujesz decyzję o sprzedaży aktywów?",
        "options": [
            {"text": "Sprzedaję wszystko nagle, gdy tylko czuję się zagrożony.", "scores": {"Emo Degen": 3}},
            {"text": "Sprzedaję tylko wtedy, gdy osiągnę planowany cel.", "scores": {"Strategist Degen": 3}},
            {"text": "Sprzedaję od razu po dużym wzroście  lepiej nie ryzykować.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprzedaję spokojnie i bez emocji, zgodnie z filozofią spokoju.", "scores": {"Zen Degen": 3}},
            {"text": "Tworzę modele ryzyka i podejmuję decyzję na podstawie wyników.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Najpierw aktualizuję dane, potem analizuję.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Próbuję przewidzieć przyszłość rynku i na tej podstawie decyduję.", "scores": {"Meta Degen": 3}},
            {"text": "Sprzedaję, gdy widzę, że wszyscy to robią.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co motywuje Cię najbardziej do inwestowania?",
        "options": [
            {"text": "Możliwość zysku tu i teraz.", "scores": {"YOLO Degen": 3}},
            {"text": "Realizacja długoterminowej strategii.", "scores": {"Strategist Degen": 3}},
            {"text": "Emocje  ekscytacja, adrenalina.", "scores": {"Emo Degen": 3}},
            {"text": "Praktyka spokoju i cierpliwości.", "scores": {"Zen Degen": 3}},
            {"text": "Chęć przetestowania własnych hipotez.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Obliczenia pokazujące potencjalny zwrot.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Wiara w przełomowe technologie.", "scores": {"Meta Degen": 3}},
            {"text": "Trendy, memy, hype i to, co popularne.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz po udanej inwestycji?",
        "options": [
            {"text": "Czuję euforię i szukam kolejnej szansy!", "scores": {"Emo Degen": 3}},
            {"text": "Analizuję, czy było to zgodne z planem.", "scores": {"Strategist Degen": 3}},
            {"text": "Wypłacam zyski i idę dalej  YOLO.", "scores": {"YOLO Degen": 3}},
            {"text": "Praktykuję wdzięczność i pozostaję spokojny.", "scores": {"Zen Degen": 3}},
            {"text": "Zapisuję dane i aktualizuję model.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Zastanawiam się, jak to powtórzyć na poziomie systemowym.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Snuję wizje przyszłości i szukam czegoś jeszcze bardziej innowacyjnego.", "scores": {"Meta Degen": 3}},
            {"text": "Chwalę się znajomym  niech wiedzą!", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz, gdy masz zainwestować większą sumę?",
        "options": [
            {"text": "Wchodzę od razu, bez zastanowienia.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprawdzam, czy to pasuje do mojego planu i alokacji.", "scores": {"Strategist Degen": 3}},
            {"text": "Waham się, analizuję i w końcu nic nie robię.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Medytuję, a potem podejmuję decyzję w zgodzie ze sobą.", "scores": {"Zen Degen": 3}},
            {"text": "Ekscytuję się, ale potem się boję i działam impulsywnie.", "scores": {"Emo Degen": 3}},
            {"text": "Tworzę pełną analizę w Excelu, zanim zrobię cokolwiek.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Zastanawiam się, jak ta inwestycja wpisuje się w przyszłość.", "scores": {"Meta Degen": 3}},
            {"text": "Wpisuję nazwę aktywa w Google Trends i Twittera.", "scores": {"Hype Degen": 3}}
        ]
    }
]
