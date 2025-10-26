"""
Ustawienia globalne dla aplikacji ZenDegenAcademy
"""

# ⚡ TRYB DEVELOPERSKI - Wyłącza zapisy do JSON dla maksymalnej szybkości
# DEVELOPMENT_MODE = True  -> Brak zapisów, wszystko w pamięci (szybkie!)
# DEVELOPMENT_MODE = False -> Normalne zapisy do plików (produkcja)
DEVELOPMENT_MODE = False  # BETA TESTY - zapisy włączone

# Ścieżka do pliku JSON zawierającego dane wszystkich lekcji
# Upewnij się, że ten plik istnieje i zawiera poprawne dane w formacie:
# {
#   "B1C1L1": {
#     "metadata": {
#       "title": "Pełna Nazwa Lekcji B1C1L1",
#       "description": "Opis lekcji...",
#       "category": "Podstawy"
#     },
#     "content": { ... }
#   },
#   ...
# }
LESSONS_FILE_PATH = "data/lessons.json"

# Inne ustawienia globalne mogą być dodane tutaj
APP_NAME = "ZenDegenAcademy"
APP_VERSION = "1.1.0"

# Upewnij się, że ta linia istnieje, jeśli nie, zostanie dodana.
# Jeśli plik jest pusty, cała zawartość powyżej zostanie dodana.
# Jeśli plik istnieje i zawiera już LESSONS_FILE_PATH, nie zostanie zmieniony.

import streamlit as st

# Page configuration
PAGE_CONFIG = {
    "page_title": "BrainventureAcademy",  # zakładam, że to są aktualne ustawienia
    "page_icon": "🧠",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "menu_items": {
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
}

# XP levels configuration
XP_LEVELS = {
    1: 0,
    2: 100,
    3: 250,
    4: 500,
    5: 1000,
    6: 2000,
    7: 3500,
    8: 5000,
    9: 7500,
    10: 10000
}

# CSS styles moved to static/css/style.css
# This variable is kept for backward compatibility
APP_STYLES = """
<style>
    /* CSS styles are now in static/css/style.css */
    /* This is kept for backward compatibility */
</style>
"""

# Daily missions configuration
DAILY_MISSIONS = [
    {"title": "Medytacja mindfulness", "description": "Wykonaj 10-minutową medytację uważności", "xp": 50, "badge": "🧘‍♂️"},
    {"title": "Analiza rynku", "description": "Przeanalizuj jeden projekt/token przez 30 minut", "xp": 70, "badge": "📊"},
    {"title": "Przegląd portfela", "description": "Dokonaj przeglądu swojego portfela i strategii", "xp": 60, "badge": "💼"},
    {"title": "Dziennik inwestora", "description": "Zapisz swoje decyzje i emocje z dzisiejszego dnia", "xp": 40, "badge": "📓"},
    {"title": "Nowa wiedza", "description": "Przeczytaj artykuł/raport o rynku lub psychologii inwestowania", "xp": 30, "badge": "🧠"}
]

# User avatar options
USER_AVATARS = {
    # Basic avatars (free selection)
    "default": "👤",
    "zen": "🧘‍♂️",
    "yolo": "🚀",
    "emo": "😭",
    "strategist": "🎯",
    "scientist": "🔬",
    "spreadsheet": "📊",
    "meta": "🔄",
    "hype": "📣",
    
    # Premium shop avatars (purchase required)
    "diamond_degen": "💎",
    "crypto_wizard": "🧙",
    "moon_hunter": "🌕"
}

# Theme options
THEMES = {
    "default": {
        "primary": "#2980B9",
        "secondary": "#6DD5FA",
        "accent": "#27ae60",
        "background": "#f7f7f7",
        "card": "#ffffff"
    },
    "dark": {
        "primary": "#3498db",
        "secondary": "#2c3e50",
        "accent": "#e74c3c",
        "background": "#1a1a1a",
        "card": "#2d2d2d"
    },
    "zen": {
        "primary": "#4CAF50",
        "secondary": "#8BC34A",
        "accent": "#009688",
        "background": "#f9f9f9",
        "card": "#ffffff"
    },
    "yolo": {
        "primary": "#FF5722",
        "secondary": "#FF9800",
        "accent": "#FFEB3B",
        "background": "#f5f5f5",
        "card": "#ffffff"
    },
    "emo": {
        "primary": "#9C27B0",
        "secondary": "#673AB7",
        "accent": "#E91E63",
        "background": "#f0f0f0",
        "card": "#ffffff"
    }
}

# Neuroleader types
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

# BADGE SYSTEM - STEP 1: Categories and Structure
# ===================================================

# Badge Categories Configuration
BADGE_CATEGORIES = {
    "getting_started": {
        "name": "Początkujący",
        "description": "Pierwsze kroki w BrainVenture Academy",
        "icon": "🌱",
        "color": "#4CAF50",
        "order": 1
    },
    "learning_progress": {
        "name": "Postęp w Nauce",
        "description": "Osiągnięcia związane z ukończeniem lekcji i kursów",
        "icon": "📚",
        "color": "#2196F3",
        "order": 2
    },
    "engagement": {
        "name": "Zaangażowanie",
        "description": "Regularna aktywność i konsekwencja w nauce",
        "icon": "🔥",
        "color": "#FF5722",
        "order": 3
    },
    "expertise": {
        "name": "Ekspertyza",
        "description": "Mistrzostwo w konkretnych obszarach wiedzy",
        "icon": "🎓",
        "color": "#9C27B0",
        "order": 4
    },
    "neuroleadership_mastery": {
        "name": "Mistrzostwo Neuroprzywództwa",
        "description": "Poznanie i rozwój różnych typów neurolidera",
        "icon": "🧠",
        "color": "#FFC107",
        "order": 5
    },
    "social": {
        "name": "Społeczność",
        "description": "Interakcje społeczne i budowanie społeczności",
        "icon": "🤝",
        "color": "#00BCD4",
        "order": 6
    },
    "achievements": {
        "name": "Osiągnięcia",
        "description": "Meta-osiągnięcia i kolekcjonowanie odznak",
        "icon": "🏆",
        "color": "#795548",
        "order": 7
    },
    "special": {
        "name": "Specjalne",
        "description": "Rzadkie i wyjątkowe osiągnięcia",
        "icon": "✨",
        "color": "#E91E63",
        "order": 8
    }
}

# Badge Tiers/Levels
BADGE_TIERS = {
    "bronze": {"name": "Brązowa", "color": "#CD7F32", "multiplier": 1.0},
    "silver": {"name": "Srebrna", "color": "#C0C0C0", "multiplier": 1.5},
    "gold": {"name": "Złota", "color": "#FFD700", "multiplier": 2.0},
    "platinum": {"name": "Platynowa", "color": "#E5E4E2", "multiplier": 3.0},
    "diamond": {"name": "Diamentowa", "color": "#B9F2FF", "multiplier": 5.0}
}

# Complete Badge System Configuration
BADGES = {
    # ==========================================
    # KATEGORIA: POCZĄTKUJĄCY (getting_started)
    # ==========================================
    "welcome": {
        "name": "Witaj w Akademii",
        "description": "Pierwszy krok w BrainVenture Academy",
        "icon": "👋",
        "category": "getting_started",
        "tier": "bronze",
        "xp_reward": 25,
        "condition": "register_account",
        "requirement": 1,
        "secret": False,
        "stackable": False
    },
    "profile_complete": {
        "name": "Profil Kompletny",
        "description": "Uzupełnij wszystkie informacje w profilu",
        "icon": "📝",
        "category": "getting_started",
        "tier": "bronze",
        "xp_reward": 50,
        "condition": "complete_profile",
        "requirement": 1,
        "secret": False,
        "stackable": False
    },
    "first_neuroleader_test": {
        "name": "Odkrywca Osobowości",
        "description": "Wykonaj pierwszy test typu neurolidera",
        "icon": "🔍",
        "category": "getting_started",
        "tier": "silver",
        "xp_reward": 100,
        "condition": "neuroleader_test_completed",
        "requirement": 1,
        "secret": False,
        "stackable": False
    },
    "first_lesson": {
        "name": "Pierwszy Uczeń",
        "description": "Ukończ pierwszą lekcję w akademii",
        "icon": "🎯",
        "category": "getting_started",
        "tier": "silver",
        "xp_reward": 75,
        "condition": "lesson_completed",
        "requirement": 1,
        "secret": False,
        "stackable": False
    },

    # ==============================================
    # KATEGORIA: POSTĘP W NAUCE (learning_progress)
    # ==============================================
    "lesson_rookie": {
        "name": "Nowicjusz Lekcji",
        "description": "Ukończ 5 lekcji",
        "icon": "📖",
        "category": "learning_progress",
        "tier": "bronze",
        "xp_reward": 100,
        "condition": "lesson_completed",
        "requirement": 5,
        "secret": False,
        "stackable": False
    },
    "lesson_apprentice": {
        "name": "Uczeń Zaawansowany",
        "description": "Ukończ 15 lekcji",
        "icon": "📚",
        "category": "learning_progress",
        "tier": "silver",
        "xp_reward": 200,
        "condition": "lesson_completed",
        "requirement": 15,
        "secret": False,
        "stackable": False
    },
    "lesson_scholar": {
        "name": "Uczony",
        "description": "Ukończ 30 lekcji",
        "icon": "🎓",
        "category": "learning_progress",
        "tier": "gold",
        "xp_reward": 400,
        "condition": "lesson_completed",
        "requirement": 30,
        "secret": False,
        "stackable": False
    },
    "lesson_master": {
        "name": "Mistrz Lekcji",
        "description": "Ukończ 50 lekcji",
        "icon": "👨‍🎓",
        "category": "learning_progress",
        "tier": "platinum",
        "xp_reward": 750,
        "condition": "lesson_completed",
        "requirement": 50,
        "secret": False,
        "stackable": False
    },
    "quiz_perfectionist": {
        "name": "Perfekcjonista",
        "description": "Uzyskaj 100% w quizie",
        "icon": "💯",
        "category": "learning_progress",
        "tier": "gold",
        "xp_reward": 150,
        "condition": "quiz_completed",
        "requirement": {"score": 100},
        "secret": False,
        "stackable": True
    },
    "speed_learner": {
        "name": "Szybki Umysł",
        "description": "Ukończ 3 lekcje w jeden dzień",
        "icon": "⚡",
        "category": "learning_progress",
        "tier": "silver",
        "xp_reward": 200,
        "condition": "lessons_per_day",
        "requirement": 3,
        "secret": False,
        "stackable": False
    },

    # ==========================================
    # KATEGORIA: ZAANGAŻOWANIE (engagement)
    # ==========================================
    "login_streak_3": {
        "name": "Konsekwentny Początek",
        "description": "Zaloguj się 3 dni z rzędu",
        "icon": "📅",
        "category": "engagement",
        "tier": "bronze",
        "xp_reward": 75,
        "condition": "user_login",
        "requirement": {"streak": 3},
        "secret": False,
        "stackable": False
    },
    "login_streak_7": {
        "name": "Tygodniowy Wojownik",
        "description": "Zaloguj się 7 dni z rzędu",
        "icon": "🗓️",
        "category": "engagement",
        "tier": "silver",
        "xp_reward": 150,
        "condition": "user_login",
        "requirement": {"streak": 7},
        "secret": False,
        "stackable": False
    },
    "login_streak_30": {
        "name": "Mistrz Miesiąca",
        "description": "Zaloguj się 30 dni z rzędu",
        "icon": "🔥",
        "category": "engagement",
        "tier": "gold",
        "xp_reward": 500,
        "condition": "user_login",
        "requirement": {"streak": 30},
        "secret": False,
        "stackable": False
    },
    "daily_mission_hero": {
        "name": "Bohater Misji",
        "description": "Ukończ wszystkie misje dzienne w jeden dzień",
        "icon": "⭐",
        "category": "engagement",
        "tier": "silver",
        "xp_reward": 100,
        "condition": "daily_mission_completed",
        "requirement": {"all_in_day": True},
        "secret": False,
        "stackable": True
    },
    "weekend_scholar": {
        "name": "Weekendowy Uczony",
        "description": "Ukończ lekcję w weekend",
        "icon": "📅",
        "category": "engagement",
        "tier": "bronze",
        "xp_reward": 50,
        "condition": "weekend_learning",
        "requirement": 1,
        "secret": False,
        "stackable": True
    },
    "night_owl": {
        "name": "Nocna Sowa",
        "description": "Ukończ lekcję po godzinie 22:00",
        "icon": "🦉",
        "category": "engagement",
        "tier": "bronze",
        "xp_reward": 50,
        "condition": "late_learning",
        "requirement": {"hour": 22},
        "secret": False,
        "stackable": True
    },
    "early_bird": {
        "name": "Ranny Ptaszek",
        "description": "Ukończ lekcję przed godziną 8:00",
        "icon": "🐦",
        "category": "engagement",
        "tier": "bronze",
        "xp_reward": 50,
        "condition": "early_learning",
        "requirement": {"hour": 8},
        "secret": False,
        "stackable": True
    },

    # =====================================
    # KATEGORIA: EKSPERTYZA (expertise)
    # =====================================
    "neuroleadership_master": {
        "name": "Mistrz Neuroprzywództwa",
        "description": "Ukończ wszystkie lekcje z kategorii Neuroprzywództwo",
        "icon": "�",
        "category": "expertise",
        "tier": "gold",
        "xp_reward": 300,
        "condition": "category_completed",
        "requirement": {"category": "neuroleadership"},
        "secret": False,
        "stackable": False
    },
    "mindfulness_expert": {
        "name": "Ekspert Mindfulness",
        "description": "Ukończ wszystkie lekcje z kategorii Mindfulness",
        "icon": "🧘‍♂️",
        "category": "expertise",
        "tier": "gold",
        "xp_reward": 300,
        "condition": "category_completed",
        "requirement": {"category": "mindfulness"},
        "secret": False,
        "stackable": False
    },
    "neuroscience_guru": {
        "name": "Guru Neuronauk",
        "description": "Ukończ wszystkie lekcje z kategorii Neuronauki",
        "icon": "🔬",
        "category": "expertise",
        "tier": "gold",
        "xp_reward": 300,
        "condition": "category_completed",
        "requirement": {"category": "neuroscience"},
        "secret": False,
        "stackable": False
    },
    "psychology_expert": {
        "name": "Ekspert Psychologii",
        "description": "Ukończ wszystkie lekcje z kategorii Psychologia",
        "icon": "🧠",
        "category": "expertise",
        "tier": "gold",
        "xp_reward": 300,
        "condition": "category_completed",
        "requirement": {"category": "psychology"},
        "secret": False,
        "stackable": False
    },
    "stress_management_master": {
        "name": "Mistrz Zarządzania Stresem",
        "description": "Ukończ wszystkie lekcje z kategorii Zarządzanie Stresem",
        "icon": "😌",
        "category": "expertise",
        "tier": "gold",
        "xp_reward": 300,
        "condition": "category_completed",
        "requirement": {"category": "stress_management"},
        "secret": False,
        "stackable": False
    },
    "xp_collector": {
        "name": "Kolekcjoner XP",
        "description": "Zgromadź 1000 punktów doświadczenia",
        "icon": "💎",
        "category": "expertise",
        "tier": "silver",
        "xp_reward": 200,
        "condition": "xp_awarded",
        "requirement": {"total": 1000},
        "secret": False,
        "stackable": False
    },
    "xp_master": {
        "name": "Mistrz Doświadczenia",
        "description": "Zgromadź 5000 punktów doświadczenia",
        "icon": "💠",
        "category": "expertise",
        "tier": "platinum",
        "xp_reward": 500,
        "condition": "xp_awarded",
        "requirement": {"total": 5000},
        "secret": False,
        "stackable": False
    },

    # ======================================================
    # KATEGORIA: MISTRZOSTWO NEUROPRZYWÓDZTWA (neuroleadership_mastery)
    # ======================================================
    "neuroleader_explorer": {
        "name": "Odkrywca Neuroliderów",
        "description": "Poznaj wszystkie typy neuroliderów",
        "icon": "🗺️",
        "category": "neuroleadership_mastery",
        "tier": "silver",
        "xp_reward": 150,
        "condition": "explore_all_neuroleader_types",
        "requirement": 6,
        "secret": False,
        "stackable": False
    },
    "multi_neuroleader": {
        "name": "Wieloaspektowy Neurolidwer",
        "description": "Wykonaj test neurolideara 3 razy z różnymi wynikami",
        "icon": "🎭",
        "category": "neuroleadership_mastery",
        "tier": "gold",
        "xp_reward": 250,
        "condition": "multiple_neuroleader_results",
        "requirement": 3,
        "secret": False,
        "stackable": False
    },
    "self_aware_leader": {
        "name": "Samoświadomy Lider",
        "description": "Potwierdź swój typ neurolidera wykonując test ponownie",
        "icon": "🔮",
        "category": "neuroleadership_mastery",
        "tier": "silver",
        "xp_reward": 100,
        "condition": "confirm_neuroleader_type",
        "requirement": 1,
        "secret": False,
        "stackable": False
    },
    "neuroleadership_king": {
        "name": "Król Neuroprzywództwa",
        "description": "Osiągnij mistrzostwo we wszystkich aspektach neuroprzywództwa",
        "icon": "👑",
        "category": "neuroleadership_mastery",
        "tier": "diamond",
        "xp_reward": 1000,
        "condition": "complete_neuroleadership_mastery",
        "requirement": 1,
        "secret": True,
        "stackable": False
    },
    "stress_master": {
        "name": "Mistrz Stresu",
        "description": "Przeczytaj wszystkie artykuły o zarządzaniu stresem",
        "icon": "😌",
        "category": "neuroleadership_mastery",
        "tier": "gold",
        "xp_reward": 200,
        "condition": "read_stress_articles",
        "requirement": 3,
        "secret": False,
        "stackable": False
    },
    "brain_hacker": {
        "name": "Haker Mózgu",
        "description": "Przeczytaj wszystkie artykuły o neurobiologii",
        "icon": "🧠",
        "category": "neuroleadership_mastery",
        "tier": "gold",
        "xp_reward": 200,
        "condition": "read_neuroscience_articles",
        "requirement": 5,
        "secret": False,
        "stackable": False
    },

    # =======================================
    # KATEGORIA: SPOŁECZNOŚĆ (social)
    # =======================================
    "community_member": {
        "name": "Członek Społeczności",
        "description": "Dołącz do społeczności akademii",
        "icon": "🏘️",
        "category": "social",
        "tier": "bronze",
        "xp_reward": 50,
        "condition": "join_community",
        "requirement": 1,
        "secret": False,
        "stackable": False
    },
    "helpful_friend": {
        "name": "Pomocny Przyjaciel",
        "description": "Pomóż innemu użytkownikowi",
        "icon": "🤗",
        "category": "social",
        "tier": "silver",
        "xp_reward": 100,
        "condition": "help_user",
        "requirement": 1,
        "secret": False,
        "stackable": True
    },
    "mentor": {
        "name": "Mentor",
        "description": "Pomóż 5 różnym użytkownikom",
        "icon": "👨‍🏫",
        "category": "social",
        "tier": "gold",
        "xp_reward": 300,
        "condition": "help_user",
        "requirement": 5,
        "secret": False,
        "stackable": False
    },
    "influencer": {
        "name": "Influencer",
        "description": "Podziel się swoimi osiągnięciami",
        "icon": "📣",
        "category": "social",
        "tier": "silver",
        "xp_reward": 75,
        "condition": "share_achievement",
        "requirement": 1,
        "secret": False,
        "stackable": True
    },

    # ==========================================
    # KATEGORIA: OSIĄGNIĘCIA (achievements)
    # ==========================================
    "first_badge": {
        "name": "Pierwsza Odznaka",
        "description": "Zdobądź swoją pierwszą odznakę",
        "icon": "🏅",
        "category": "achievements",
        "tier": "bronze",
        "xp_reward": 25,
        "condition": "earn_badge",
        "requirement": 1,
        "secret": False,
        "stackable": False
    },
    "badge_collector": {
        "name": "Kolekcjoner Odznak",
        "description": "Zdobądź 10 różnych odznak",
        "icon": "🎖️",
        "category": "achievements",
        "tier": "silver",
        "xp_reward": 200,
        "condition": "earn_badge",
        "requirement": 10,
        "secret": False,
        "stackable": False
    },
    "badge_master": {
        "name": "Mistrz Odznak",
        "description": "Zdobądź 25 różnych odznak",
        "icon": "🏆",
        "category": "achievements",
        "tier": "gold",
        "xp_reward": 500,
        "condition": "earn_badge",
        "requirement": 25,
        "secret": False,
        "stackable": False
    },
    "achievement_hunter": {
        "name": "Łowca Osiągnięć",
        "description": "Zdobądź wszystkie odznaki z jednej kategorii",
        "icon": "🎯",
        "category": "achievements",
        "tier": "platinum",
        "xp_reward": 750,
        "condition": "complete_category",
        "requirement": 1,
        "secret": False,
        "stackable": True
    },

    # ====================================
    # KATEGORIA: SPECJALNE (special)
    # ====================================
    "pioneer": {
        "name": "Pionier",
        "description": "Jeden z pierwszych 100 użytkowników akademii",
        "icon": "🚀",
        "category": "special",
        "tier": "diamond",
        "xp_reward": 500,
        "condition": "early_adopter",
        "requirement": 100,
        "secret": True,
        "stackable": False
    },
    "legend": {
        "name": "Legenda",
        "description": "Osiągnij wszystkie możliwe odznaki",
        "icon": "👑",
        "category": "special",
        "tier": "diamond",
        "xp_reward": 2000,
        "condition": "complete_all_badges",
        "requirement": 1,
        "secret": True,
        "stackable": False
    },
    "dedicated_student": {
        "name": "Oddany Uczeń",
        "description": "Spędź łącznie 50 godzin w akademii",
        "icon": "⏰",
        "category": "special",
        "tier": "platinum",
        "xp_reward": 1000,
        "condition": "total_study_time",
        "requirement": {"hours": 50},
        "secret": False,
        "stackable": False
    },
    "secret_discoverer": {
        "name": "Odkrywca Sekretów",
        "description": "Znajdź ukryty easter egg w aplikacji",
        "icon": "🕵️",
        "category": "special",
        "tier": "gold",
        "xp_reward": 300,
        "condition": "find_easter_egg",
        "requirement": 1,
        "secret": True,
        "stackable": False
    },
    "midnight_learner": {
        "name": "Uczący się o Północy",
        "description": "Ukończ lekcję dokładnie o północy",
        "icon": "🌙",
        "category": "special",
        "tier": "gold",
        "xp_reward": 200,
        "condition": "midnight_learning",
        "requirement": 1,
        "secret": True,
        "stackable": False
    },
    "forrest_gump_fan": {
        "name": "Fan Forresta Gumpa",
        "description": "Przeczytaj artykuł o Forrest Gump i neuroprzywództwie",
        "icon": "🏃‍♂️",
        "category": "special",
        "tier": "silver",
        "xp_reward": 150,
        "condition": "read_forrest_article",
        "requirement": 1,
        "secret": False,
        "stackable": False
    },
    "neuroplasticity_enthusiast": {
        "name": "Entuzjasta Neuroplastyczności",
        "description": "Przeczytaj 5 artykułów o mózgu i neurobiologii",
        "icon": "🔬",
        "category": "special",
        "tier": "gold",
        "xp_reward": 250,
        "condition": "read_brain_articles",
        "requirement": 5,
        "secret": False,
        "stackable": False
    },
    "mindfulness_practitioner": {
        "name": "Praktyk Mindfulness",
        "description": "Ukończ wszystkie ćwiczenia oddechowe",
        "icon": "🧘",
        "category": "special",
        "tier": "platinum",
        "xp_reward": 500,
        "condition": "complete_breathing_exercises",
        "requirement": 1,
        "secret": False,
        "stackable": False
    }
}