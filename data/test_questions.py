# Typy neurolider�w - transformacja z degen�w na neurolider�w
NEUROLEADER_TYPES = {
    "Neuroanalityk": {
        "description": "Rozwa�ny, skrupulatny, cz�sto parali�owany nadmiarem analiz. Lider, kt�ry ma trudno�ci z podejmowaniem decyzji.",
        "tagline": "Unikaj�cy Ryzyka",
        "icon": "??",
        "strengths": ["Wyczuwa zagro�enia", "Analizuje scenariusze ryzyka", "Dok�adno�� w analizie", "Ostro�no�� w decyzjach"],
        "challenges": ["Parali� decyzyjny", "Odk�ada decyzje na p�niej", "L�k przed b��dami", "Traci okazje przez zw�ok�"],
        "strategy": "Ustal limity czasowe na analiz�. Stosuj zasad� 'wystarczaj�co dobrej decyzji'. Praktykuj podejmowanie ma�ych decyzji.",
        "color": "#2c3e50",
        "supermoc": "Wyczuwa zagro�enia i analizuje scenariusze ryzyka jak nikt inny",
        "slabo��": "Traci okazje przez zw�ok�"
    },
    "Neuroreaktor": {
        "description": "Lider, kt�ry reaguje impulsywnie na stres i emocje, dzia�a b�yskawicznie i emocjonalnie, cz�sto bez pe�nych danych.",
        "tagline": "Impulsywny Stra�nik", 
        "icon": "??",
        "strengths": ["Szybkie reakcje w kryzysie", "Dzia�anie pod presj�", "Natychmiastowe rozwi�zywanie problem�w", "Energia w trudnych sytuacjach"],
        "challenges": ["Impulsywne decyzje", "Dzia�anie pod wp�ywem emocji", "Brak pe�nej analizy", "Ryzykowne wybory"],
        "strategy": "Techniki oddechowe i mindfulness. Zasada 24 godzin na wa�ne decyzje. Konsultuj decyzje z zaufan� osob�.",
        "color": "#e74c3c",
        "supermoc": "Zdolno�� do dzia�ania w kryzysie",
        "slabo��": "Podejmuje ryzykowne decyzje"
    },
    "Neurobalanser": {
        "description": "Liderzy, kt�rzy potrafi� ��czy� racjonalno�� z empati�, podejmuj�c decyzje w oparciu o dane oraz intuicj�.",
        "tagline": "Zbalansowany Integrator",
        "icon": "??", 
        "strengths": ["Inteligencja emocjonalna", "Logiczne my�lenie", "Elastyczno��", "Zr�wnowa�one podej�cie"],
        "challenges": ["Mo�e zbyt d�ugo analizowa�", "Wahanie w decyzjach", "Potrzeba znalezienia balansu", "Czasem zbyt ostro�ny"],
        "strategy": "Ustal jasne kryteria decyzyjne. Rozwijaj umiej�tno�� facylitacji. Praktykuj podejmowanie decyzji w ograniczonym czasie.",
        "color": "#3498db",
        "supermoc": "Inteligencja emocjonalna + logika",
        "slabo��": "Mo�e zbyt d�ugo si� waha�"
    },
    "Neuroempata": {
        "description": "Lider, kt�ry skupia si� na emocjonalnych potrzebach zespo�u. Ceni zaufanie, dobre relacje i komunikacj� w zespole.",
        "tagline": "Architekt Relacji",
        "icon": "??",
        "strengths": ["Budowanie wi�zi", "Empatia", "Zrozumienie potrzeb zespo�u", "Tworzenie atmosfery zaufania"],
        "challenges": ["Zbyt emocjonalne podej�cie", "Trudno�� z obiektywizmem", "Problem z granicami", "Preferencje osobiste"],
        "strategy": "Rozwijaj umiej�tno�ci analityczne. Ustal jasne granice. Ucz si� asertywno�ci. Korzystaj z zewn�trznych opinii.",
        "color": "#27ae60",
        "supermoc": "Wi�zi emocjonalne i zaanga�owanie zespo�u",
        "slabo��": "Trudno�� z obiektywizmem"
    },
    "Neuroinnowator": {
        "description": "Liderzy, kt�rzy potrafi� dostosowa� swoje podej�cie do zmieniaj�cej si� sytuacji. S� otwarci na nowe rozwi�zania, gotowi do eksperyment�w.",
        "tagline": "Nawigator Zmiany",
        "icon": "??",
        "strengths": ["Adaptacja do zmian", "Innowacyjno��", "Eksperymentowanie", "Elastyczno�� strategii"],
        "challenges": ["Brak stabilno�ci", "Zbyt cz�ste zmiany", "Mo�e frustrowa� zesp�", "Brak konsekwencji"],
        "strategy": "Wprowad� struktur� do swoich innowacji. Rozwijaj umiej�tno�� priorytetyzacji. Komunikuj zmiany efektywnie.",
        "color": "#9b59b6",
        "supermoc": "Adaptacja i innowacyjno��", 
        "slabo��": "Brak konsekwencji i cierpliwo�ci"
    },
    "Neuroinspirator": {
        "description": "Liderzy, kt�rzy potrafi� zmotywowa� innych do dzia�ania dzi�ki swojej osobowo�ci, wizji i entuzjazmowi.",
        "tagline": "Charyzmatyczny Wizjoner",
        "icon": "??",
        "strengths": ["Charyzma", "Motywowanie zespo�u", "Wizja przysz�o�ci", "Energia i entuzjazm"],
        "challenges": ["Mo�e zdominowa� zesp�", "Zale�no�� od charyzmy", "Zaniedbywanie autonomii zespo�u", "Nadmierna pewno�� siebie"],
        "strategy": "Rozwijaj zdolno�� do s�uchania. �wiadomie buduj autonomi� zespo�u. Naucz si� korzysta� z danych w decyzjach.",
        "color": "#f39c12",
        "supermoc": "Wp�yw, energia, wizja",
        "slabo��": "Mo�e zdominowa� zesp�"
    }
}

# Alias dla kompatybilno�ci z reszt� aplikacji - b�dzie stopniowo zast�powany
DEGEN_TYPES = NEUROLEADER_TYPES

TEST_QUESTIONS = [
    {
        "question": "Jak podejmujesz wa�ne decyzje w zespole?",
        "options": [
            {"text": "Dzia�am szybko na podstawie intuicji, bez d�ugiej analizy.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizuj� wszystkie mo�liwe scenariusze i ryzyka.", "scores": {"Neuroanalityk": 3}},
            {"text": "��cz� dane z intuicj� i emocjami zespo�u.", "scores": {"Neurobalanser": 3}},
            {"text": "Skupiam si� na tym, jak decyzja wp�ynie na zesp�.", "scores": {"Neuroempata": 3}},
            {"text": "Testuj� r�ne podej�cia i adaptuj� si� do sytuacji.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspiruj� zesp� wizj� i motywuj� do dzia�ania.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak reagujesz w sytuacji kryzysu w zespole?",
        "options": [
            {"text": "Reaguj� natychmiast, dzia�am pod wp�ywem adrenaliny.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizuj� sytuacj�, szukam wszystkich mo�liwych rozwi�za�.", "scores": {"Neuroanalityk": 3}},
            {"text": "Zachowuj� spok�j i ��cz� logik� z empati�.", "scores": {"Neurobalanser": 3}},
            {"text": "Koncentruj� si� na wspieraniu zespo�u emocjonalnie.", "scores": {"Neuroempata": 3}},
            {"text": "Szybko dostosowuj� plan i wprowadzam innowacje.", "scores": {"Neuroinnowator": 3}},
            {"text": "Mobilizuj� zesp� przez inspiracj� i wizj�.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak motywujesz sw�j zesp�?",
        "options": [
            {"text": "Poprzez szybkie dzia�anie i energi� w trudnych momentach.", "scores": {"Neuroreaktor": 3}},
            {"text": "Przez dok�adne planowanie i analiz� zagro�e�.", "scores": {"Neuroanalityk": 3}},
            {"text": "��cz�c logiczne argumenty z emocjonalnym wsparciem.", "scores": {"Neurobalanser": 3}},
            {"text": "Buduj�c silne relacje i atmosfer� zaufania.", "scores": {"Neuroempata": 3}},
            {"text": "Wprowadzaj�c innowacje i nowe sposoby pracy.", "scores": {"Neuroinnowator": 3}},
            {"text": "Poprzez charyzm�, wizj� i inspiruj�ce przem�wienia.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak podchodzisz do zarz�dzania zmianami w organizacji?",
        "options": [
            {"text": "Wprowadzam zmiany szybko, reaguj�c na bie��co.", "scores": {"Neuroreaktor": 3}},
            {"text": "Dok�adnie analizuj� wszystkie ryzyka przed zmian�.", "scores": {"Neuroanalityk": 3}},
            {"text": "Balansuj� mi�dzy potrzeb� zmiany a stabilno�ci�.", "scores": {"Neurobalanser": 3}},
            {"text": "Skupiam si� na tym, jak zmiany wp�yn� na ludzi.", "scores": {"Neuroempata": 3}},
            {"text": "Eksperymentuj� z r�nymi podej�ciami do zmiany.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspiruj� zesp� wizj� przysz�o�ci po zmianie.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jaki jest Tw�j styl komunikacji z zespo�em?",
        "options": [
            {"text": "Bezpo�redni i szybki, szczeg�lnie w sytuacjach kryzysowych.", "scores": {"Neuroreaktor": 3}},
            {"text": "Ostro�ny i przemy�lany, przedstawiam wszystkie fakty.", "scores": {"Neuroanalityk": 3}},
            {"text": "��cz� logiczne argumenty z uwzgl�dnieniem emocji.", "scores": {"Neurobalanser": 3}},
            {"text": "Empatyczny i wspieraj�cy, s�ucham potrzeb zespo�u.", "scores": {"Neuroempata": 3}},
            {"text": "Elastyczny, dostosowuj� styl do sytuacji i osoby.", "scores": {"Neuroinnowator": 3}},
            {"text": "Charyzmatyczny i inspiruj�cy, motywuj� przez wizj�.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak zarz�dzasz konfliktami w zespole?",
        "options": [
            {"text": "Reaguj� natychmiast, chc� szybko rozwi�za� problem.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizuj� przyczyny konfliktu i szukam optymalnego rozwi�zania.", "scores": {"Neuroanalityk": 3}},
            {"text": "Szukam rozwi�za� uwzgl�dniaj�cych zar�wno fakty jak i emocje.", "scores": {"Neurobalanser": 3}},
            {"text": "Koncentruj� si� na budowaniu porozumienia i mediacji.", "scores": {"Neuroempata": 3}},
            {"text": "Testuj� r�ne sposoby rozwi�zania, dostosowuj�c podej�cie.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspiruj� strony do wsp�lnej wizji i cel�w.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak budujemy strategi� zespo�u?",
        "options": [
            {"text": "Szybko reagujemy na sytuacj�, dzia�amy intuicyjnie.", "scores": {"Neuroreaktor": 3}},
            {"text": "Dok�adnie analizujemy wszystkie mo�liwe scenariusze.", "scores": {"Neuroanalityk": 3}},
            {"text": "��czymy analiz� danych z intuicj� i opiniami zespo�u.", "scores": {"Neurobalanser": 3}},
            {"text": "Uwzgl�dniamy potrzeby i mo�liwo�ci ka�dego cz�onka zespo�u.", "scores": {"Neuroempata": 3}},
            {"text": "Pozostajemy elastyczni i gotowi na adaptacj� strategii.", "scores": {"Neuroinnowator": 3}},
            {"text": "Tworzymy inspiruj�c� wizj�, kt�ra motywuje do dzia�ania.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak reagujesz na niepowodzenia zespo�u?",
        "options": [
            {"text": "Dzia�am natychmiast, by jak najszybciej naprawi� sytuacj�.", "scores": {"Neuroreaktor": 3}},
            {"text": "Analizuj� dok�adnie przyczyny niepowodzenia.", "scores": {"Neuroanalityk": 3}},
            {"text": "Wyci�gam wnioski i r�wnowa�� uczenie si� z wsparciem zespo�u.", "scores": {"Neurobalanser": 3}},
            {"text": "Skupiam si� na wspieraniu zespo�u i odbudowie morale.", "scores": {"Neuroempata": 3}},
            {"text": "Traktuj� to jako okazj� do innowacji i zmiany podej�cia.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspiruj� zesp� do wyci�gni�cia wniosk�w i dalszego rozwoju.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak podejmujesz decyzje pod presj� czasu?",
        "options": [
            {"text": "Dzia�am instynktownie i szybko, ufam intuicji.", "scores": {"Neuroreaktor": 3}},
            {"text": "Stresuj� si�, potrzebuj� wi�cej czasu na analiz�.", "scores": {"Neuroanalityk": 3}},
            {"text": "Szybko analizuj� kluczowe fakty i uwzgl�dniam intuicj�.", "scores": {"Neurobalanser": 3}},
            {"text": "Konsultuj� si� z zespo�em, uwzgl�dniam ich opinie.", "scores": {"Neuroempata": 3}},
            {"text": "Testuj� szybkie rozwi�zania i dostosowuj� w locie.", "scores": {"Neuroinnowator": 3}},
            {"text": "Mobilizuj� zesp� energi� i wizj� szybkiego dzia�ania.", "scores": {"Neuroinspirator": 3}}
        ]
    },
    {
        "question": "Jak rozwijasz sw�j zesp�?",
        "options": [
            {"text": "Przez wyzwania i sytuacje kryzysowe, kt�re hartuj�.", "scores": {"Neuroreaktor": 3}},
            {"text": "Poprzez dok�adn� analiz� mocnych stron i planowanie rozwoju.", "scores": {"Neuroanalityk": 3}},
            {"text": "��cz�c rozw�j zawodowy z rozwojem osobistym.", "scores": {"Neurobalanser": 3}},
            {"text": "Buduj�c silne relacje i wspieraj�c indywidualnie.", "scores": {"Neuroempata": 3}},
            {"text": "Wprowadzaj�c innowacyjne metody i eksperymentuj�c.", "scores": {"Neuroinnowator": 3}},
            {"text": "Inspiruj�c do ci�g�ego rozwoju i osi�gania cel�w.", "scores": {"Neuroinspirator": 3}}
        ]
    }
]


TEST_QUESTIONS = [
    {
        "question": "Jak reagujesz, gdy cena aktywa gwa�townie wzrasta?",
        "options": [
            {"text": "Natychmiast kupuj�, nie analizuj�c zbyt du�o.", "scores": {"YOLO Degen": 3, "Hype Degen": 1}},
            {"text": "Zastanawiam si�, czy to zgodne z moj� strategi�.", "scores": {"Strategist Degen": 3}},
            {"text": "Czuj� eufori� i szybko kupuj�.", "scores": {"Emo Degen": 3, "YOLO Degen": 1}},
            {"text": "Czekam na spokojniejszy moment na rynku.", "scores": {"Zen Degen": 3}},
            {"text": "Analizuj� dane, by przewidzie� kolejny ruch.", "scores": {"Mad Scientist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Sprawdzam dane historyczne i ryzyko.", "scores": {"Spreadsheet Degen": 3, "Strategist Degen": 1}},
            {"text": "Analizuj� kontekst i wi�kszy trend.", "scores": {"Meta Degen": 3}},
            {"text": "Kupuj�, bo widz�, �e wszyscy o tym m�wi�.", "scores": {"Hype Degen": 3, "YOLO Degen": 1}}
        ]
    },
    {
        "question": "Co robisz, gdy rynek zaczyna si� zmienia� w spos�b nieprzewidywalny?",
        "options": [
            {"text": "Dzia�am natychmiast  instynkt to podstawa.", "scores": {"YOLO Degen": 3, "Emo Degen": 1}},
            {"text": "Analizuj� dane, zanim co� zrobi�.", "scores": {"Strategist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Wpadam w panik�, sprzedaj� wszystko.", "scores": {"Emo Degen": 3}},
            {"text": "Zachowuj� spok�j, nic nie zmieniam.", "scores": {"Zen Degen": 3}},
            {"text": "Tworz� w�asny model predykcyjny.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Od�wie�am arkusze z analizami.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Szukam g��bszego sensu zmian.", "scores": {"Meta Degen": 3}},
            {"text": "Reaguj� tak, jak spo�eczno�� Twittera.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak cz�sto zmieniasz swoje decyzje inwestycyjne?",
        "options": [
            {"text": "Ci�gle  ka�da okazja to nowy ruch.", "scores": {"YOLO Degen": 3, "Hype Degen": 1}},
            {"text": "Tylko gdy plan tego wymaga.", "scores": {"Strategist Degen": 3}},
            {"text": "Za ka�dym razem, gdy si� zestresuj�.", "scores": {"Emo Degen": 3}},
            {"text": "Prawie nigdy  spok�j to podstawa.", "scores": {"Zen Degen": 3}},
            {"text": "Kiedy dane daj� zielone �wiat�o.", "scores": {"Mad Scientist Degen": 3, "Spreadsheet Degen": 1}},
            {"text": "Gdy model pokazuje, �e to uzasadnione.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "W rytmie zmian rynkowych i geopolitycznych.", "scores": {"Meta Degen": 3}},
            {"text": "Gdy co� trenduje  wchodz�!", "scores": {"Hype Degen": 3, "YOLO Degen": 1}}
        ]
    },
    {
        "question": "Jak wygl�da Twoje poranne podej�cie do inwestowania?",
        "options": [
            {"text": "W��czam aplikacj� i kupuj� na �lepo.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprawdzam moj� strategi� i wykonuj� plan.", "scores": {"Strategist Degen": 3}},
            {"text": "Sprawdzam nastroje i kieruj� si� emocjami.", "scores": {"Emo Degen": 3}},
            {"text": "Medytuj�, zanim podejm� decyzj�.", "scores": {"Zen Degen": 3}},
            {"text": "Odpalam skrypty z analizami.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Aktualizuj� sw�j Excel z danymi.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Przegl�dam �wiatowe wydarzenia.", "scores": {"Meta Degen": 3}},
            {"text": "Sprawdzam TikToka i Twittera.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak si� czujesz, gdy Twoja inwestycja traci na warto�ci?",
        "options": [
            {"text": "Trudno, YOLO  lec� dalej.", "scores": {"YOLO Degen": 3}},
            {"text": "To cz�� planu, mam to pod kontrol�.", "scores": {"Strategist Degen": 3}},
            {"text": "Jestem za�amany, nie mog� spa�.", "scores": {"Emo Degen": 3}},
            {"text": "Akceptuj� to. Taki jest rynek.", "scores": {"Zen Degen": 3}},
            {"text": "Analizuj�, dlaczego tak si� sta�o.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Aktualizuj� plik i zmieniam parametry.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Sprawdzam, czy to nie wynik globalnych trend�w.", "scores": {"Meta Degen": 3}},
            {"text": "Obwiniam influencer�w z internetu.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak wybierasz projekt lub sp�k� do inwestycji?",
        "options": [
            {"text": "Klikam w to, co akurat wygl�da fajnie.", "scores": {"YOLO Degen": 3}},
            {"text": "Szukam zgodno�ci z moj� strategi�.", "scores": {"Strategist Degen": 3}},
            {"text": "Wybieram to, co wzbudza emocje.", "scores": {"Emo Degen": 3}},
            {"text": "Wybieram intuicyjnie, po przemy�leniu.", "scores": {"Zen Degen": 3}},
            {"text": "Patrz� na technologi� i innowacyjno��.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Analizuj� wska�niki i liczby.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Czytam bia�� ksi�g� i analizuj� ekosystem.", "scores": {"Meta Degen": 3}},
            {"text": "To, co trenduje na socialach.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak planujesz swoje portfolio?",
        "options": [
            {"text": "Nie planuj�  pe�en spontan.", "scores": {"YOLO Degen": 3}},
            {"text": "Mam rozpisany plan i cel.", "scores": {"Strategist Degen": 3}},
            {"text": "Dodaj� i usuwam po impulsie.", "scores": {"Emo Degen": 3}},
            {"text": "Portfolio to droga  zmienia si� naturalnie.", "scores": {"Zen Degen": 3}},
            {"text": "Symuluj� wiele scenariuszy.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Optymalizuj� struktur� w arkuszu kalkulacyjnym.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Uk�adam pod mega trendy i narracje.", "scores": {"Meta Degen": 3}},
            {"text": "Kupuj� to, co polecaj� inni.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz w dniu du�ej korekty rynkowej?",
        "options": [
            {"text": "Wchodz� all-in w do�ku.", "scores": {"YOLO Degen": 3}},
            {"text": "Trzymam si� planu.", "scores": {"Strategist Degen": 3}},
            {"text": "Wpadam w panik� i wyprzedaj�.", "scores": {"Emo Degen": 3}},
            {"text": "Obserwuj� i nie dzia�am pochopnie.", "scores": {"Zen Degen": 3}},
            {"text": "Weryfikuj� modele i dane.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Uaktualniam wyceny i alokacj�.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Szacuj� konsekwencje makroekonomiczne.", "scores": {"Meta Degen": 3}},
            {"text": "Patrz� co robi� znani YouTuberzy.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jaki jest Tw�j ulubiony spos�b zdobywania wiedzy o inwestowaniu?",
        "options": [
            {"text": "Z mem�w i short�w.", "scores": {"YOLO Degen": 3}},
            {"text": "Z ksi��ek i analiz.", "scores": {"Strategist Degen": 3}},
            {"text": "Z podcast�w o sukcesach i pora�kach.", "scores": {"Emo Degen": 3}},
            {"text": "Z do�wiadczenia i uwa�no�ci.", "scores": {"Zen Degen": 3}},
            {"text": "Z bada� naukowych.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Z raport�w i arkuszy.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Z rozm�w i debat o przysz�o�ci.", "scores": {"Meta Degen": 3}},
            {"text": "Z komentarzy pod filmami influencer�w.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak oceniasz sukces swojej inwestycji?",
        "options": [
            {"text": "Czy zrobi�em szybki zysk?", "scores": {"YOLO Degen": 3}},
            {"text": "Czy osi�gn��em cel zgodnie z planem?", "scores": {"Strategist Degen": 3}},
            {"text": "Czy poczu�em si� z tym dobrze?", "scores": {"Emo Degen": 3}},
            {"text": "Czy nie cierpia�em w procesie?", "scores": {"Zen Degen": 3}},
            {"text": "Czy moja hipoteza si� potwierdzi�a?", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Czy ROI by�o zgodne z kalkulacj�?", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Czy wpisa�o si� to w wi�kszy trend?", "scores": {"Meta Degen": 3}},
            {"text": "Czy znajomi byli pod wra�eniem?", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Jak podejmujesz decyzj� o sprzeda�y aktyw�w?",
        "options": [
            {"text": "Sprzedaj� wszystko nagle, gdy tylko czuj� si� zagro�ony.", "scores": {"Emo Degen": 3}},
            {"text": "Sprzedaj� tylko wtedy, gdy osi�gn� planowany cel.", "scores": {"Strategist Degen": 3}},
            {"text": "Sprzedaj� od razu po du�ym wzro�cie  lepiej nie ryzykowa�.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprzedaj� spokojnie i bez emocji, zgodnie z filozofi� spokoju.", "scores": {"Zen Degen": 3}},
            {"text": "Tworz� modele ryzyka i podejmuj� decyzj� na podstawie wynik�w.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Najpierw aktualizuj� dane, potem analizuj�.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Pr�buj� przewidzie� przysz�o�� rynku i na tej podstawie decyduj�.", "scores": {"Meta Degen": 3}},
            {"text": "Sprzedaj�, gdy widz�, �e wszyscy to robi�.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co motywuje Ci� najbardziej do inwestowania?",
        "options": [
            {"text": "Mo�liwo�� zysku tu i teraz.", "scores": {"YOLO Degen": 3}},
            {"text": "Realizacja d�ugoterminowej strategii.", "scores": {"Strategist Degen": 3}},
            {"text": "Emocje  ekscytacja, adrenalina.", "scores": {"Emo Degen": 3}},
            {"text": "Praktyka spokoju i cierpliwo�ci.", "scores": {"Zen Degen": 3}},
            {"text": "Ch�� przetestowania w�asnych hipotez.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Obliczenia pokazuj�ce potencjalny zwrot.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Wiara w prze�omowe technologie.", "scores": {"Meta Degen": 3}},
            {"text": "Trendy, memy, hype i to, co popularne.", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz po udanej inwestycji?",
        "options": [
            {"text": "Czuj� eufori� i szukam kolejnej szansy!", "scores": {"Emo Degen": 3}},
            {"text": "Analizuj�, czy by�o to zgodne z planem.", "scores": {"Strategist Degen": 3}},
            {"text": "Wyp�acam zyski i id� dalej  YOLO.", "scores": {"YOLO Degen": 3}},
            {"text": "Praktykuj� wdzi�czno�� i pozostaj� spokojny.", "scores": {"Zen Degen": 3}},
            {"text": "Zapisuj� dane i aktualizuj� model.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Zastanawiam si�, jak to powt�rzy� na poziomie systemowym.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Snuj� wizje przysz�o�ci i szukam czego� jeszcze bardziej innowacyjnego.", "scores": {"Meta Degen": 3}},
            {"text": "Chwal� si� znajomym  niech wiedz�!", "scores": {"Hype Degen": 3}}
        ]
    },
    {
        "question": "Co robisz, gdy masz zainwestowa� wi�ksz� sum�?",
        "options": [
            {"text": "Wchodz� od razu, bez zastanowienia.", "scores": {"YOLO Degen": 3}},
            {"text": "Sprawdzam, czy to pasuje do mojego planu i alokacji.", "scores": {"Strategist Degen": 3}},
            {"text": "Waham si�, analizuj� i w ko�cu nic nie robi�.", "scores": {"Mad Scientist Degen": 3}},
            {"text": "Medytuj�, a potem podejmuj� decyzj� w zgodzie ze sob�.", "scores": {"Zen Degen": 3}},
            {"text": "Ekscytuj� si�, ale potem si� boj� i dzia�am impulsywnie.", "scores": {"Emo Degen": 3}},
            {"text": "Tworz� pe�n� analiz� w Excelu, zanim zrobi� cokolwiek.", "scores": {"Spreadsheet Degen": 3}},
            {"text": "Zastanawiam si�, jak ta inwestycja wpisuje si� w przysz�o��.", "scores": {"Meta Degen": 3}},
            {"text": "Wpisuj� nazw� aktywa w Google Trends i Twittera.", "scores": {"Hype Degen": 3}}
        ]
    }
]
