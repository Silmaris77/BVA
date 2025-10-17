"""
Szablony problemów dla narzędzia 6 Kapeluszy de Bono
"""

PROBLEM_TEMPLATES = {
    "nowy_produkt": {
        "name": "🚀 Nowy produkt/usługa",
        "description": "Pomysł na nowy produkt lub usługę",
        "example": "Aplikacja mobilna do zarządzania czasem dla freelancerów",
        "prompts": [
            "Jak możemy ulepszyć istniejący produkt?",
            "Jaki produkt rozwiązałby problem naszych klientów?",
            "Co możemy zaoferować, czego nie ma konkurencja?"
        ]
    },
    "rozwiazanie_problemu": {
        "name": "🔧 Rozwiązanie problemu",
        "description": "Szukanie rozwiązania konkretnego problemu biznesowego",
        "example": "Jak zmniejszyć rotację pracowników w firmie?",
        "prompts": [
            "Jak rozwiązać problem spadającej sprzedaży?",
            "Jak poprawić komunikację w zespole?",
            "Jak zwiększyć satysfakcję klientów?"
        ]
    },
    "strategia": {
        "name": "🎯 Strategia biznesowa",
        "description": "Opracowanie strategii lub kierunku rozwoju",
        "example": "Strategia wejścia na nowy rynek zagraniczny",
        "prompts": [
            "Jak rozwijać firmę w kolejnych latach?",
            "Jaką strategię marketingową obrać?",
            "Jak zbudować przewagę konkurencyjną?"
        ]
    },
    "innowacja": {
        "name": "💡 Innowacja w procesach",
        "description": "Innowacyjne podejście do istniejących procesów",
        "example": "Automatyzacja procesów HR w firmie",
        "prompts": [
            "Jak usprawnić proces rekrutacji?",
            "Jak zautomatyzować raportowanie?",
            "Jak zdigitalizować obsługę klienta?"
        ]
    },
    "zmiana": {
        "name": "🔄 Zarządzanie zmianą",
        "description": "Wprowadzenie istotnej zmiany organizacyjnej",
        "example": "Przejście na pracę zdalną/hybrydową",
        "prompts": [
            "Jak wprowadzić nowy system IT?",
            "Jak przekształcić kulturę organizacyjną?",
            "Jak zrestrukturyzować zespoły?"
        ]
    },
    "marketing": {
        "name": "📢 Kampania marketingowa",
        "description": "Koncepcja kampanii lub działań marketingowych",
        "example": "Kampania na social media dla młodych klientów",
        "prompts": [
            "Jak dotrzeć do nowej grupy docelowej?",
            "Jak zwiększyć rozpoznawalność marki?",
            "Jak zaangażować społeczność online?"
        ]
    },
    "efektywnosc": {
        "name": "⚡ Zwiększenie efektywności",
        "description": "Poprawa wydajności lub efektywności",
        "example": "Skrócenie czasu realizacji projektów o 30%",
        "prompts": [
            "Jak przyspieszyć procesy produkcyjne?",
            "Jak zmniejszyć koszty operacyjne?",
            "Jak zwiększyć produktywność zespołu?"
        ]
    },
    "wlasny": {
        "name": "✍️ Własny problem",
        "description": "Opisz swój własny problem lub wyzwanie",
        "example": None,
        "prompts": []
    }
}

# Definicje kapeluszy
HATS_DEFINITIONS = {
    "white": {
        "name": "🤍 Biały Kapelusz",
        "role": "Analityk",
        "description": "Fakty, dane, liczby, obiektywna informacja",
        "focus": [
            "Jakie mamy fakty?",
            "Co wiemy na pewno?",
            "Jakie dane są dostępne?",
            "Czego nie wiemy?"
        ],
        "traits": "neutralny, obiektywny, konkretny, oparty na danych",
        "avoid": "spekulacje, opinie, emocje"
    },
    "red": {
        "name": "🔴 Czerwony Kapelusz",
        "role": "Emocjonalista",
        "description": "Emocje, intuicja, przeczucia, uczucia",
        "focus": [
            "Jak się z tym czuję?",
            "Co mówi mi intuicja?",
            "Jakie są moje odczucia?",
            "Co czuje w brzuchu?"
        ],
        "traits": "emocjonalny, intuicyjny, spontaniczny, subiektywny",
        "avoid": "uzasadnianie emocji, analizowanie uczuć"
    },
    "black": {
        "name": "⚫ Czarny Kapelusz",
        "role": "Krytyk",
        "description": "Ryzyka, problemy, słabe punkty, ostrożność",
        "focus": [
            "Co może pójść nie tak?",
            "Jakie są zagrożenia?",
            "Gdzie są pułapki?",
            "Co jest wątpliwe?"
        ],
        "traits": "ostrożny, sceptyczny, realistyczny, krytyczny",
        "avoid": "przesadny pesymizm bez argumentów"
    },
    "yellow": {
        "name": "🟡 Żółty Kapelusz",
        "role": "Optymista",
        "description": "Korzyści, szanse, możliwości, pozytywne aspekty",
        "focus": [
            "Jakie są plusy?",
            "Co możemy zyskać?",
            "Jakie są szanse?",
            "Co może się udać?"
        ],
        "traits": "pozytywny, entuzjastyczny, widzący możliwości, konstruktywny",
        "avoid": "naiwny optymizm bez podstaw"
    },
    "green": {
        "name": "🟢 Zielony Kapelusz",
        "role": "Kreatywny",
        "description": "Nowe pomysły, alternatywy, twórcze rozwiązania",
        "focus": [
            "A gdyby tak...?",
            "Co jeszcze możemy wymyślić?",
            "Jakie są alternatywy?",
            "Jak to zrobić inaczej?"
        ],
        "traits": "kreatywny, otwarty, nieszablonowy, generujący pomysły",
        "avoid": "ocenianie pomysłów, krytyka"
    },
    "blue": {
        "name": "🔵 Niebieski Kapelusz",
        "role": "Moderator",
        "description": "Organizacja procesu, podsumowania, kontrola",
        "focus": [
            "Gdzie jesteśmy?",
            "Co dalej?",
            "Jaki jest plan?",
            "Co już ustaliliśmy?"
        ],
        "traits": "organizujący, syntetyzujący, strukturalny, kontrolujący proces",
        "avoid": "dominowanie dyskusją, narzucanie opinii"
    }
}

# Kolejność kapeluszy w sesji
HATS_ORDER = ["blue", "white", "red", "black", "yellow", "green", "blue"]

# Możliwe konflikty między kapeluszami
HATS_CONFLICTS = [
    {
        "hats": ["black", "yellow"],
        "probability": 0.4,
        "examples": [
            "Czarny: To zbyt ryzykowne!\nŻółty: Ale pomyśl o potencjale!",
            "Żółty: Widzisz same problemy!\nCzarny: A ty ignorujesz realia!",
            "Czarny: To się nie uda.\nŻółty: Z takim podejściem na pewno nie!"
        ]
    },
    {
        "hats": ["white", "red"],
        "probability": 0.3,
        "examples": [
            "Biały: Pokaż mi dane.\nCzerwony: Nie wszystko da się zmierzyć!",
            "Czerwony: Po prostu to czuję.\nBiały: To nie jest argument.",
            "Biały: Fakty nie kłamią.\nCzerwony: A emocje też mają znaczenie!"
        ]
    },
    {
        "hats": ["green", "black"],
        "probability": 0.35,
        "examples": [
            "Zielony: A gdyby tak...\nCzarny: To nie zadziała, bo...",
            "Czarny: Zbyt wiele niewiadomych.\nZielony: Właśnie dlatego trzeba spróbować!",
            "Zielony: Bądź bardziej otwarty!\nCzarny: Bądź bardziej realistyczny!"
        ]
    }
]
