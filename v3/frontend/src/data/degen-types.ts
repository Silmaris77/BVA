export type DegenTypeKey =
    | "Zen Degen"
    | "YOLO Degen"
    | "Emo Degen"
    | "Strategist Degen"
    | "Mad Scientist Degen"
    | "Spreadsheet Degen"
    | "Meta Degen"
    | "Hype Degen";

export interface DegenTypeDetails {
    description: string;
    strengths: string[];
    challenges: string[];
    strategy: string;
    color: string;
    icon: string;
}

export const DEGEN_TYPES: Record<DegenTypeKey, DegenTypeDetails> = {
    "Zen Degen": {
        description: "Balansujący emocje i strategie, inwestujesz ze spokojem i uważnością. Dążysz do równowagi, unikając impulsywnych reakcji na wahania rynku.",
        strengths: ["Zrównoważone podejście", "Kontrola emocji", "Długoterminowa wizja", "Odporność na stres"],
        challenges: ["Czasem zbyt ostrożny", "Może przegapiać okazje wymagające szybkiej decyzji"],
        strategy: "Połącz medytację z analizą techniczną. Twórz zrównoważone portfolio z elementami wysokiego ryzyka (np. 5%), aby ćwiczyć wychodzenie ze strefy komfortu.",
        color: "#3498db",
        icon: "🧘"
    },
    "YOLO Degen": {
        description: "Stawiasz wszystko na jedną kartę, podejmując decyzje bez zastanowienia. Traktujesz inwestowanie jak grę, często kierując się FOMO lub euforią.",
        strengths: ["Szybkie działanie", "Odwaga i spontaniczność", "Wykorzystywanie okazji", "Wysoka tolerancja ryzyka"],
        challenges: ["Nadmierna impulsywność", "Ignorowanie ryzyka", "Brak długoterminowego planu", "Podatność na straty"],
        strategy: "Ustal sztywne limity ryzyka (np. max 10% portfolio na ryzykowne ruchy). Zanim klikniesz 'Kup', weź 3 głębokie oddechy.",
        color: "#e74c3c",
        icon: "🚀"
    },
    "Emo Degen": {
        description: "Działasz pod wpływem silnych emocji takich jak strach, euforia czy panika. Twoje decyzje są często reaktywne na bieżące nastroje rynku.",
        strengths: ["Wrażliwość na nastroje rynku", "Intuicja", "Zaangażowanie emocjonalne"],
        challenges: ["Panika przy spadkach", "Kupowanie na szczytach (FOMO)", "Brak kontroli nad emocjami", "Niestabilność decyzyjna"],
        strategy: "Prowadź dziennik emocji inwestora. Wprowadź zasadę 24h oczekiwania ('cooling-off period') przed każdą ważną decyzją.",
        color: "#f39c12",
        icon: "🌪️"
    },
    "Strategist Degen": {
        description: "Działasz według ściśle określonego planu i strategii. Decyzje podejmujesz po analizie, trzymając się ustalonych zasad niezależnie od emocji.",
        strengths: ["Zorganizowanie", "Konsekwencja", "Długoterminowa wizja", "Dyscyplina"],
        challenges: ["Mniejsza elastyczność", "Trudność w adaptacji do nagłych zmian", "Czasem zbyt zachowawczy"],
        strategy: "Regularnie (np. kwartalnie) weryfikuj swoje założenia. Zarezerwuj małą część portfolio na eksperymenty, aby nie popaść w rutynę.",
        color: "#27ae60",
        icon: "📅"
    },
    "Mad Scientist Degen": {
        description: "Eksperymentator. Testujesz innowacyjne podejścia, tworzysz skomplikowane modele i teorie, czasem zapominając o praktyce.",
        strengths: ["Kreatywność", "Innowacyjność", "Analityczne myślenie", "Szukanie nieszablonowych rozwiązań"],
        challenges: ["Paraliż analityczny", "Nadmierne teoretyzowanie", "Trudności w realizacji prostych strategii"],
        strategy: "Ustal sztywny czas na analizę (time-boxing) i moment decyzji. Testuj hipotezy małym kapitałem, zamiast tylko teoretyzować.",
        color: "#9b59b6",
        icon: "🧠"
    },
    "Spreadsheet Degen": {
        description: "Analityk danych. Kochasz liczby, wskaźniki i arkusze kalkulacyjne. Decyzję podejmujesz dopiero, gdy 'liczby się zgadzają'.",
        strengths: ["Dokładność", "Metodyczność", "Działanie oparte na twardych danych", "Minimalizacja błędów poznawczych"],
        challenges: ["Przeciążenie danymi (Analysis Paralysis)", "Ignorowanie intuicji i czynnika ludzkiego", "Powolne reagowanie"],
        strategy: "Pamiętaj, że rynek to nie tylko matematyka, ale też psychologia. Uprość swoje modele do kluczowych wskaźników.",
        color: "#2980b9",
        icon: "📊"
    },
    "Meta Degen": {
        description: "Wizjoner. Analizujesz szeroki kontekst, makroekonomię, trendy globalne i powiązania między rynkami (od krypto po rynek sztuki).",
        strengths: ["Szerokie horyzonty", "Rozumienie globalnych zależności", "Długoterminowa predykcja", "Łączenie kropek"],
        challenges: ["Pomijanie szczegółów", "Trudność w wyczuciu krótkiego terminu", "Zbyt abstrakcyjne podejście"],
        strategy: "Połącz analizę makro z konkretnymi sygnałami mikro. Weryfikuj swoje wielkie wizje w zderzeniu z twardymi danymi tu i teraz.",
        color: "#16a085",
        icon: "🎭"
    },
    "Hype Degen": {
        description: "Social Trader. Śledzisz trendy, Twittera i to, o czym jest głośno. Inwestujesz tam, gdzie skupia się uwaga tłumu.",
        strengths: ["Szybkie wychwytywanie trendów", "Refleks", "Rozumienie psychologii tłumu", "Elastyczność"],
        challenges: ["Podążanie za owczym pędem", "Inwestowanie na szczytach bańki", "Brak własnej analizy fundamentalnej"],
        strategy: "Weryfikuj trendy własnym riserczem. Ustal zasadę, by nie wchodzić w aktywa, o których 'wszyscy już mówią' (często jest za późno).",
        color: "#e67e22",
        icon: "🔥"
    }
};
