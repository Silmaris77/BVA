# Typy neuroliderów - transformacja z degenów na neuroliderów
NEUROLEADER_TYPES = {
    "Neuroanalityk": {
        "description": "Rozwa¿ny, skrupulatny, czêsto parali¿owany nadmiarem analiz. Lider, który ma trudnoœci z podejmowaniem decyzji.",
        "tagline": "Unikaj¹cy Ryzyka",
        "icon": "??",
        "strengths": ["Wyczuwa zagro¿enia", "Analizuje scenariusze ryzyka", "Dok³adnoœæ w analizie", "Ostro¿noœæ w decyzjach"],
        "challenges": ["Parali¿ decyzyjny", "Odk³ada decyzje na póŸniej", "Lêk przed b³êdami", "Traci okazje przez zw³okê"],
        "strategy": "Ustal limity czasowe na analizê. Stosuj zasadê 'wystarczaj¹co dobrej decyzji'. Praktykuj podejmowanie ma³ych decyzji.",
        "color": "#2c3e50",
        "supermoc": "Wyczuwa zagro¿enia i analizuje scenariusze ryzyka jak nikt inny",
        "slaboœæ": "Traci okazje przez zw³okê"
    },
    "Neuroreaktor": {
        "description": "Lider, który reaguje impulsywnie na stres i emocje, dzia³a b³yskawicznie i emocjonalnie, czêsto bez pe³nych danych.",
        "tagline": "Impulsywny Stra¿nik", 
        "icon": "??",
        "strengths": ["Szybkie reakcje w kryzysie", "Dzia³anie pod presj¹", "Natychmiastowe rozwi¹zywanie problemów", "Energia w trudnych sytuacjach"],
        "challenges": ["Impulsywne decyzje", "Dzia³anie pod wp³ywem emocji", "Brak pe³nej analizy", "Ryzykowne wybory"],
        "strategy": "Techniki oddechowe i mindfulness. Zasada 24 godzin na wa¿ne decyzje. Konsultuj decyzje z zaufan¹ osob¹.",
        "color": "#e74c3c",
        "supermoc": "Zdolnoœæ do dzia³ania w kryzysie",
        "slaboœæ": "Podejmuje ryzykowne decyzje"
    },
    "Neurobalanser": {
        "description": "Liderzy, którzy potrafi¹ ³¹czyæ racjonalnoœæ z empati¹, podejmuj¹c decyzje w oparciu o dane oraz intuicjê.",
        "tagline": "Zbalansowany Integrator",
        "icon": "??", 
        "strengths": ["Inteligencja emocjonalna", "Logiczne myœlenie", "Elastycznoœæ", "Zrównowa¿one podejœcie"],
        "challenges": ["Mo¿e zbyt d³ugo analizowaæ", "Wahanie w decyzjach", "Potrzeba znalezienia balansu", "Czasem zbyt ostro¿ny"],
        "strategy": "Ustal jasne kryteria decyzyjne. Rozwijaj umiejêtnoœæ facylitacji. Praktykuj podejmowanie decyzji w ograniczonym czasie.",
        "color": "#3498db",
        "supermoc": "Inteligencja emocjonalna + logika",
        "slaboœæ": "Mo¿e zbyt d³ugo siê wahaæ"
    },
    "Neuroempata": {
        "description": "Lider, który skupia siê na emocjonalnych potrzebach zespo³u. Ceni zaufanie, dobre relacje i komunikacjê w zespole.",
        "tagline": "Architekt Relacji",
        "icon": "??",
        "strengths": ["Budowanie wiêzi", "Empatia", "Zrozumienie potrzeb zespo³u", "Tworzenie atmosfery zaufania"],
        "challenges": ["Zbyt emocjonalne podejœcie", "Trudnoœæ z obiektywizmem", "Problem z granicami", "Preferencje osobiste"],
        "strategy": "Rozwijaj umiejêtnoœci analityczne. Ustal jasne granice. Ucz siê asertywnoœci. Korzystaj z zewnêtrznych opinii.",
        "color": "#27ae60",
        "supermoc": "Wiêzi emocjonalne i zaanga¿owanie zespo³u",
        "slaboœæ": "Trudnoœæ z obiektywizmem"
    },
    "Neuroinnowator": {
        "description": "Liderzy, którzy potrafi¹ dostosowaæ swoje podejœcie do zmieniaj¹cej siê sytuacji. S¹ otwarci na nowe rozwi¹zania, gotowi do eksperymentów.",
        "tagline": "Nawigator Zmiany",
        "icon": "??",
        "strengths": ["Adaptacja do zmian", "Innowacyjnoœæ", "Eksperymentowanie", "Elastycznoœæ strategii"],
        "challenges": ["Brak stabilnoœci", "Zbyt czêste zmiany", "Mo¿e frustrowaæ zespó³", "Brak konsekwencji"],
        "strategy": "WprowadŸ strukturê do swoich innowacji. Rozwijaj umiejêtnoœæ priorytetyzacji. Komunikuj zmiany efektywnie.",
        "color": "#9b59b6",
        "supermoc": "Adaptacja i innowacyjnoœæ", 
        "slaboœæ": "Brak konsekwencji i cierpliwoœci"
    },
    "Neuroinspirator": {
        "description": "Liderzy, którzy potrafi¹ zmotywowaæ innych do dzia³ania dziêki swojej osobowoœci, wizji i entuzjazmowi.",
        "tagline": "Charyzmatyczny Wizjoner",
        "icon": "??",
        "strengths": ["Charyzma", "Motywowanie zespo³u", "Wizja przysz³oœci", "Energia i entuzjazm"],
        "challenges": ["Mo¿e zdominowaæ zespó³", "Zale¿noœæ od charyzmy", "Zaniedbywanie autonomii zespo³u", "Nadmierna pewnoœæ siebie"],
        "strategy": "Rozwijaj zdolnoœæ do s³uchania. Œwiadomie buduj autonomiê zespo³u. Naucz siê korzystaæ z danych w decyzjach.",
        "color": "#f39c12",
        "supermoc": "Wp³yw, energia, wizja",
        "slaboœæ": "Mo¿e zdominowaæ zespó³"
    }
}

# Alias dla kompatybilnoœci z reszt¹ aplikacji - bêdzie stopniowo zastêpowany
DEGEN_TYPES = NEUROLEADER_TYPES

TEST_QUESTIONS = [
    {
        "question": "Jak podejmujesz wa¿ne decyzje w zespole?",
        "options": [
            {"text": "Dzia³am szybko na podstawie intuicji, bez d³ugiej analizy.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizujê wszystkie mo¿liwe scenariusze i ryzyka.", "scores": {"Neuroanalityk": 3}},
            {"text": "£¹czê dane z intuicj¹ i emocjami zespo³u.", "scores": {"Neurobalanser": 3}},
            {"text": "Skupiam siê na tym, jak decyzja wp³ynie na zespó³.", "scores": {"Neuroempata": 3}},
            {"text": "Testujê ró¿ne podejœcia i adaptujê siê do sytuacji.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspirujê zespó³ wizj¹ i motywujê do dzia³ania.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak reagujesz w sytuacji kryzysu w zespole?",
        "options": [
            {"text": "Reagujê natychmiast, dzia³am pod wp³ywem adrenaliny.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizujê sytuacjê, szukam wszystkich mo¿liwych rozwi¹zañ.", "scores": {"Neuroanalityk": 3}},
            {"text": "Zachowujê spokój i ³¹czê logikê z empati¹.", "scores": {"Neurobalanser": 3}},
            {"text": "Koncentrujê siê na wspieraniu zespo³u emocjonalnie.", "scores": {"Neuroempata": 3}},
            {"text": "Szybko dostosowujê plan i wprowadzam innowacje.", "scores": {"Neuroinnowator": 3}},
            {"text": "Mobilizujê zespó³ przez inspiracjê i wizjê.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak motywujesz swój zespó³?",
        "options": [
            {"text": "Poprzez szybkie dzia³anie i energiê w trudnych momentach.", "scores": {"Neuroreaktor": 3}},
            {"text": "Przez dok³adne planowanie i analizê zagro¿eñ.", "scores": {"Neuroanalityk": 3}},
            {"text": "£¹cz¹c logiczne argumenty z emocjonalnym wsparciem.", "scores": {"Neurobalanser": 3}},
            {"text": "Buduj¹c silne relacje i atmosferê zaufania.", "scores": {"Neuroempata": 3}},
            {"text": "Wprowadzaj¹c innowacje i nowe sposoby pracy.", "scores": {"Neuroinnowator": 3}},
            {"text": "Poprzez charyzmê, wizjê i inspiruj¹ce przemówienia.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak podchodzisz do zarz¹dzania zmianami w organizacji?",
        "options": [
            {"text": "Wprowadzam zmiany szybko, reaguj¹c na bie¿¹co.", "scores": {"Neuroreaktor": 3}},
            {"text": "Dok³adnie analizujê wszystkie ryzyka przed zmian¹.", "scores": {"Neuroanalityk": 3}},
            {"text": "Balansujê miêdzy potrzeb¹ zmiany a stabilnoœci¹.", "scores": {"Neurobalanser": 3}},
            {"text": "Skupiam siê na tym, jak zmiany wp³yn¹ na ludzi.", "scores": {"Neuroempata": 3}},
            {"text": "Eksperymentujê z ró¿nymi podejœciami do zmiany.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspirujê zespó³ wizj¹ przysz³oœci po zmianie.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jaki jest Twój styl komunikacji z zespo³em?",
        "options": [
            {"text": "Bezpoœredni i szybki, szczególnie w sytuacjach kryzysowych.", "scores": {"Neuroreaktor": 3}},
            {"text": "Ostro¿ny i przemyœlany, przedstawiam wszystkie fakty.", "scores": {"Neuroanalityk": 3}},
            {"text": "£¹czê logiczne argumenty z uwzglêdnieniem emocji.", "scores": {"Neurobalanser": 3}},
            {"text": "Empatyczny i wspieraj¹cy, s³ucham potrzeb zespo³u.", "scores": {"Neuroempata": 3}},
            {"text": "Elastyczny, dostosowujê styl do sytuacji i osoby.", "scores": {"Neuroinnowator": 3}},
            {"text": "Charyzmatyczny i inspiruj¹cy, motywujê przez wizjê.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak zarz¹dzasz konfliktami w zespole?",
        "options": [
            {"text": "Reagujê natychmiast, chcê szybko rozwi¹zaæ problem.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizujê przyczyny konfliktu i szukam optymalnego rozwi¹zania.", "scores": {"Neuroanalityk": 3}},
            {"text": "Szukam rozwi¹zañ uwzglêdniaj¹cych zarówno fakty jak i emocje.", "scores": {"Neurobalanser": 3}},
            {"text": "Koncentrujê siê na budowaniu porozumienia i mediacji.", "scores": {"Neuroempata": 3}},
            {"text": "Testujê ró¿ne sposoby rozwi¹zania, dostosowuj¹c podejœcie.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspirujê strony do wspólnej wizji i celów.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak budujemy strategiê zespo³u?",
        "options": [
            {"text": "Szybko reagujemy na sytuacjê, dzia³amy intuicyjnie.", "scores": {"Neuroreaktor": 3}},
            {"text": "Dok³adnie analizujemy wszystkie mo¿liwe scenariusze.", "scores": {"Neuroanalityk": 3}},
            {"text": "£¹czymy analizê danych z intuicj¹ i opiniami zespo³u.", "scores": {"Neurobalanser": 3}},
            {"text": "Uwzglêdniamy potrzeby i mo¿liwoœci ka¿dego cz³onka zespo³u.", "scores": {"Neuroempata": 3}},
            {"text": "Pozostajemy elastyczni i gotowi na adaptacjê strategii.", "scores": {"Neuroinnowator": 3}},
            {"text": "Tworzymy inspiruj¹c¹ wizjê, która motywuje do dzia³ania.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak reagujesz na niepowodzenia zespo³u?",
        "options": [
            {"text": "Dzia³am natychmiast, by jak najszybciej naprawiæ sytuacjê.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizujê dok³adnie przyczyny niepowodzenia.", "scores": {"Neuroanalityk": 3}},
            {"text": "Wyci¹gam wnioski i równowa¿ê uczenie siê z wsparciem zespo³u.", "scores": {"Neurobalanser": 3}},
            {"text": "Skupiam siê na wspieraniu zespo³u i odbudowie morale.", "scores": {"Neuroempata": 3}},
            {"text": "Traktujê to jako okazjê do innowacji i zmiany podejœcia.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspirujê zespó³ do wyci¹gniêcia wniosków i dalszego rozwoju.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak podejmujesz decyzje pod presj¹ czasu?",
        "options": [
            {"text": "Dzia³am instynktownie i szybko, ufam intuicji.", "scores": {"Neuroreaktor": 3}},
            {"text": "Stresujê siê, potrzebujê wiêcej czasu na analizê.", "scores": {"Neuroanalityk": 3}},
            {"text": "Szybko analizujê kluczowe fakty i uwzglêdniam intuicjê.", "scores": {"Neurobalanser": 3}},
            {"text": "Konsultujê siê z zespo³em, uwzglêdniam ich opinie.", "scores": {"Neuroempata": 3}},
            {"text": "Testujê szybkie rozwi¹zania i dostosowujê w locie.", "scores": {"Neuroinnowator": 3}},
            {"text": "Mobilizujê zespó³ energi¹ i wizj¹ szybkiego dzia³ania.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak rozwijasz swój zespó³?",
        "options": [
            {"text": "Przez wyzwania i sytuacje kryzysowe, które hartuj¹.", "scores": {"Neuroreaktor": 3}},
            {"text": "Poprzez dok³adn¹ analizê mocnych stron i planowanie rozwoju.", "scores": {"Neuroanalityk": 3}},
            {"text": "£¹cz¹c rozwój zawodowy z rozwojem osobistym.", "scores": {"Neurobalanser": 3}},
            {"text": "Buduj¹c silne relacje i wspieraj¹c indywidualnie.", "scores": {"Neuroempata": 3}},
            {"text": "Wprowadzaj¹c innowacyjne metody i eksperymentuj¹c.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspiruj¹c do ci¹g³ego rozwoju i osi¹gania celów.", "scores": {"Neuroinspirator": 3}}
        ]
    }
]


TEST_QUESTIONS = [
    {
        "question": "Jak reagujesz, gdy cena aktywa gwa³townie wzrasta?",
        "options": [
            {"text": "Natychmiast kupujê, nie analizuj¹c zbyt du¿o.", "scores": {"YOLO Degen": 3, "Hype Degen": 1}},
            {"text": "Zastanawiam siê, czy to zgodne z moj¹ strategi¹.", "scores": {"Strategist Degen": 3}},
            {"text": "Czujê euforiê i szybko kupujê.", "scores": {"Emo Degen": 3, "YOLO Degen": 1}},
            {"text": "Czekam na spokojniejszy moment na rynku.", "scores": {"Zen Degen": 3}},
            {"text": "Analizujê dane, by przewidzieæ kolejny ruch.", "scores": {"Mad Scientist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Sprawdzam dane historyczne i ryzyko.", "scores": {"Spreadsheet Degen": 3, "Strategist Degen": 1}},
            {"text": "Analizujê kontekst i wiêkszy trend.", "scores": {"Meta Degen": 3}},
            {"text": "Kupujê, bo widzê, ¿e wszyscy o tym mówi¹.", "scores": {"Hype Degen": 3, "YOLO Degen": 1}}
        ]
    },
    {
        "question": "Co robisz, gdy rynek zaczyna siê zmieniaæ w sposób nieprzewidywalny?",
        "options": [
            {"text": "Dzia³am natychmiast  instynkt to podstawa.", "scores": {"YOLO Degen": 3, "Emo Degen": 1}},
            {"text": "Analizujê dane, zanim coœ zrobiê.", "scores": {"Strategist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Wpadam w panikê, sprzedajê wszystko.", "scores": {"Emo Degen": 3}},
            {"text": "Zachowujê spokój, nic nie zmieniam.", "scores": {"Zen Degen": 3}},
            {"text": "Tworzê w³asny model predykcyjny.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Odœwie¿am arkusze z analizami.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Szukam g³êbszego sensu zmian.", "scores": {"Meta Degen": 3}},
            {"text": "Reagujê tak, jak spo³ecznoœæ Twittera.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak czêsto zmieniasz swoje decyzje inwestycyjne?",
        "options": [
            {"text": "Ci¹gle  ka¿da okazja to nowy ruch.", "scores": {"YOLO Degen": 3, "Hype Degen": 1}},
            {"text": "Tylko gdy plan tego wymaga.", "scores": {"Strategist Degen": 3}},
            {"text": "Za ka¿dym razem, gdy siê zestresujê.", "scores": {"Emo Degen": 3}},
            {"text": "Prawie nigdy  spokój to podstawa.", "scores": {"Zen Degen": 3}},
            {"text": "Kiedy dane daj¹ zielone œwiat³o.", "scores": {"Mad Scientist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Gdy model pokazuje, ¿e to uzasadnione.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "W rytmie zmian rynkowych i geopolitycznych.", "scores": {"Meta Degen": 3}},
            {"text": "Gdy coœ trenduje  wchodzê!", "scores": {"Hype Degen": 3, "YOLO Degen": 1}}
        ]
    },
    {
        "question": "Jak wygl¹da Twoje poranne podejœcie do inwestowania?",
        "options": [
            {"text": "W³¹czam aplikacjê i kupujê na œlepo.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprawdzam moj¹ strategiê i wykonujê plan.", "scores": {"Strategist Degen": 3}},
            {"text": "Sprawdzam nastroje i kierujê siê emocjami.", "scores": {"Emo Degen": 3}},
            {"text": "Medytujê, zanim podejmê decyzjê.", "scores": {"Zen Degen": 3}},
            {"text": "Odpalam skrypty z analizami.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Aktualizujê swój Excel z danymi.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Przegl¹dam œwiatowe wydarzenia.", "scores": {"Meta Degen": 3}},
            {"text": "Sprawdzam TikToka i Twittera.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak siê czujesz, gdy Twoja inwestycja traci na wartoœci?",
        "options": [
            {"text": "Trudno, YOLO  lecê dalej.", "scores": {"YOLO Degen": 3}},
            {"text": "To czêœæ planu, mam to pod kontrol¹.", "scores": {"Strategist Degen": 3}},
            {"text": "Jestem za³amany, nie mogê spaæ.", "scores": {"Emo Degen": 3}},
            {"text": "Akceptujê to. Taki jest rynek.", "scores": {"Zen Degen": 3}},
            {"text": "Analizujê, dlaczego tak siê sta³o.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Aktualizujê plik i zmieniam parametry.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Sprawdzam, czy to nie wynik globalnych trendów.", "scores": {"Meta Degen": 3}},
            {"text": "Obwiniam influencerów z internetu.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak wybierasz projekt lub spó³kê do inwestycji?",
        "options": [
            {"text": "Klikam w to, co akurat wygl¹da fajnie.", "scores": {"YOLO Degen": 3}},
            {"text": "Szukam zgodnoœci z moj¹ strategi¹.", "scores": {"Strategist Degen": 3}},
            {"text": "Wybieram to, co wzbudza emocje.", "scores": {"Emo Degen": 3}},
            {"text": "Wybieram intuicyjnie, po przemyœleniu.", "scores": {"Zen Degen": 3}},
            {"text": "Patrzê na technologiê i innowacyjnoœæ.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Analizujê wskaŸniki i liczby.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Czytam bia³¹ ksiêgê i analizujê ekosystem.", "scores": {"Meta Degen": 3}},
            {"text": "To, co trenduje na socialach.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak planujesz swoje portfolio?",
        "options": [
            {"text": "Nie planujê  pe³en spontan.", "scores": {"YOLO Degen": 3}},
            {"text": "Mam rozpisany plan i cel.", "scores": {"Strategist Degen": 3}},
            {"text": "Dodajê i usuwam po impulsie.", "scores": {"Emo Degen": 3}},
            {"text": "Portfolio to droga  zmienia siê naturalnie.", "scores": {"Zen Degen": 3}},
            {"text": "Symulujê wiele scenariuszy.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Optymalizujê strukturê w arkuszu kalkulacyjnym.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Uk³adam pod mega trendy i narracje.", "scores": {"Meta Degen": 3}},
            {"text": "Kupujê to, co polecaj¹ inni.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz w dniu du¿ej korekty rynkowej?",
        "options": [
            {"text": "Wchodzê all-in w do³ku.", "scores": {"YOLO Degen": 3}},
            {"text": "Trzymam siê planu.", "scores": {"Strategist Degen": 3}},
            {"text": "Wpadam w panikê i wyprzedajê.", "scores": {"Emo Degen": 3}},
            {"text": "Obserwujê i nie dzia³am pochopnie.", "scores": {"Zen Degen": 3}},
            {"text": "Weryfikujê modele i dane.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Uaktualniam wyceny i alokacjê.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Szacujê konsekwencje makroekonomiczne.", "scores": {"Meta Degen": 3}},
            {"text": "Patrzê co robi¹ znani YouTuberzy.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jaki jest Twój ulubiony sposób zdobywania wiedzy o inwestowaniu?",
        "options": [
            {"text": "Z memów i shortów.", "scores": {"YOLO Degen": 3}},
            {"text": "Z ksi¹¿ek i analiz.", "scores": {"Strategist Degen": 3}},
            {"text": "Z podcastów o sukcesach i pora¿kach.", "scores": {"Emo Degen": 3}},
            {"text": "Z doœwiadczenia i uwa¿noœci.", "scores": {"Zen Degen": 3}},
            {"text": "Z badañ naukowych.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Z raportów i arkuszy.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Z rozmów i debat o przysz³oœci.", "scores": {"Meta Degen": 3}},
            {"text": "Z komentarzy pod filmami influencerów.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak oceniasz sukces swojej inwestycji?",
        "options": [
            {"text": "Czy zrobi³em szybki zysk?", "scores": {"YOLO Degen": 3}},
            {"text": "Czy osi¹gn¹³em cel zgodnie z planem?", "scores": {"Strategist Degen": 3}},
            {"text": "Czy poczu³em siê z tym dobrze?", "scores": {"Emo Degen": 3}},
            {"text": "Czy nie cierpia³em w procesie?", "scores": {"Zen Degen": 3}},
            {"text": "Czy moja hipoteza siê potwierdzi³a?", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Czy ROI by³o zgodne z kalkulacj¹?", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Czy wpisa³o siê to w wiêkszy trend?", "scores": {"Meta Degen": 3}},
            {"text": "Czy znajomi byli pod wra¿eniem?", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak podejmujesz decyzjê o sprzeda¿y aktywów?",
        "options": [
            {"text": "Sprzedajê wszystko nagle, gdy tylko czujê siê zagro¿ony.", "scores": {"Emo Degen": 3}},
            {"text": "Sprzedajê tylko wtedy, gdy osi¹gnê planowany cel.", "scores": {"Strategist Degen": 3}},
            {"text": "Sprzedajê od razu po du¿ym wzroœcie  lepiej nie ryzykowaæ.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprzedajê spokojnie i bez emocji, zgodnie z filozofi¹ spokoju.", "scores": {"Zen Degen": 3}},
            {"text": "Tworzê modele ryzyka i podejmujê decyzjê na podstawie wyników.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Najpierw aktualizujê dane, potem analizujê.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Próbujê przewidzieæ przysz³oœæ rynku i na tej podstawie decydujê.", "scores": {"Meta Degen": 3}},
            {"text": "Sprzedajê, gdy widzê, ¿e wszyscy to robi¹.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co motywuje Ciê najbardziej do inwestowania?",
        "options": [
            {"text": "Mo¿liwoœæ zysku tu i teraz.", "scores": {"YOLO Degen": 3}},
            {"text": "Realizacja d³ugoterminowej strategii.", "scores": {"Strategist Degen": 3}},
            {"text": "Emocje  ekscytacja, adrenalina.", "scores": {"Emo Degen": 3}},
            {"text": "Praktyka spokoju i cierpliwoœci.", "scores": {"Zen Degen": 3}},
            {"text": "Chêæ przetestowania w³asnych hipotez.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Obliczenia pokazuj¹ce potencjalny zwrot.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Wiara w prze³omowe technologie.", "scores": {"Meta Degen": 3}},
            {"text": "Trendy, memy, hype i to, co popularne.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz po udanej inwestycji?",
        "options": [
            {"text": "Czujê euforiê i szukam kolejnej szansy!", "scores": {"Emo Degen": 3}},
            {"text": "Analizujê, czy by³o to zgodne z planem.", "scores": {"Strategist Degen": 3}},
            {"text": "Wyp³acam zyski i idê dalej  YOLO.", "scores": {"YOLO Degen": 3}},
            {"text": "Praktykujê wdziêcznoœæ i pozostajê spokojny.", "scores": {"Zen Degen": 3}},
            {"text": "Zapisujê dane i aktualizujê model.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Zastanawiam siê, jak to powtórzyæ na poziomie systemowym.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Snujê wizje przysz³oœci i szukam czegoœ jeszcze bardziej innowacyjnego.", "scores": {"Meta Degen": 3}},
            {"text": "Chwalê siê znajomym  niech wiedz¹!", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz, gdy masz zainwestowaæ wiêksz¹ sumê?",
        "options": [
            {"text": "Wchodzê od razu, bez zastanowienia.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprawdzam, czy to pasuje do mojego planu i alokacji.", "scores": {"Strategist Degen": 3}},
            {"text": "Waham siê, analizujê i w koñcu nic nie robiê.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Medytujê, a potem podejmujê decyzjê w zgodzie ze sob¹.", "scores": {"Zen Degen": 3}},
            {"text": "Ekscytujê siê, ale potem siê bojê i dzia³am impulsywnie.", "scores": {"Emo Degen": 3}},
            {"text": "Tworzê pe³n¹ analizê w Excelu, zanim zrobiê cokolwiek.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Zastanawiam siê, jak ta inwestycja wpisuje siê w przysz³oœæ.", "scores": {"Meta Degen": 3}},
            {"text": "Wpisujê nazwê aktywa w Google Trends i Twittera.", "scores": {"Hype Degen": 3}}
        ]
    }
]
