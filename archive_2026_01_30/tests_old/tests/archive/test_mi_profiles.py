"""
Przykładowe profile użytkowników dla testowania MI Test
"""

# PROFIL 1: Linguistic-Interpersonal (Manager/Coach)
profile_1 = {
    "name": "Maria - Manager",
    "answers": {
        # Linguistic - wysokie (4-5)
        "L1": 5, "L2": 5, "L3": 4, "L4": 5, "L5": 4,
        # Logical - średnie (3)
        "M1": 3, "M2": 3, "M3": 3, "M4": 3, "M5": 3,
        # Visual - niskie (2)
        "V1": 2, "V2": 2, "V3": 2, "V4": 2, "V5": 2,
        # Musical - niskie (2)
        "U1": 2, "U2": 2, "U3": 2, "U4": 2, "U5": 2,
        # Kinesthetic - średnie (3)
        "K1": 3, "K2": 3, "K3": 3, "K4": 3, "K5": 3,
        # Interpersonal - wysokie (4-5)
        "P1": 5, "P2": 5, "P3": 4, "P4": 5, "P5": 4,
        # Intrapersonal - średnie (3)
        "I1": 3, "I2": 3, "I3": 3, "I4": 3, "I5": 3,
        # Naturalistic - niskie (2)
        "N1": 2, "N2": 2, "N3": 2, "N4": 2, "N5": 2
    },
    "expected_top_3": ["linguistic", "interpersonal", "logical"],
    "description": "Idealny profil dla managera, coacha, HR"
}

# PROFIL 2: Logical-Visual (Analityk/Developer)
profile_2 = {
    "name": "Tomasz - Analityk",
    "answers": {
        # Linguistic - średnie (3)
        "L1": 3, "L2": 3, "L3": 3, "L4": 3, "L5": 3,
        # Logical - bardzo wysokie (5)
        "M1": 5, "M2": 5, "M3": 5, "M4": 5, "M5": 5,
        # Visual - wysokie (4-5)
        "V1": 5, "V2": 4, "V3": 5, "V4": 4, "V5": 4,
        # Musical - niskie (2)
        "U1": 2, "U2": 2, "U3": 2, "U4": 2, "U5": 2,
        # Kinesthetic - niskie (2)
        "K1": 2, "K2": 2, "K3": 2, "K4": 2, "K5": 2,
        # Interpersonal - średnie (3)
        "P1": 3, "P2": 3, "P3": 3, "P4": 3, "P5": 3,
        # Intrapersonal - wysokie (4)
        "I1": 4, "I2": 4, "I3": 4, "I4": 4, "I5": 4,
        # Naturalistic - niskie (2)
        "N1": 2, "N2": 2, "N3": 2, "N4": 2, "N5": 2
    },
    "expected_top_3": ["logical", "visual", "intrapersonal"],
    "description": "Idealny profil dla analityka, programisty, data scientist"
}

# PROFIL 3: Kinesthetic-Interpersonal (Trener/Instruktor)
profile_3 = {
    "name": "Kasia - Trenerka",
    "answers": {
        # Linguistic - wysokie (4)
        "L1": 4, "L2": 4, "L3": 4, "L4": 4, "L5": 4,
        # Logical - średnie (3)
        "M1": 3, "M2": 3, "M3": 3, "M4": 3, "M5": 3,
        # Visual - średnie (3)
        "V1": 3, "V2": 3, "V3": 3, "V4": 3, "V5": 3,
        # Musical - średnie (3)
        "U1": 3, "U2": 3, "U3": 3, "U4": 3, "U5": 3,
        # Kinesthetic - bardzo wysokie (5)
        "K1": 5, "K2": 5, "K3": 5, "K4": 5, "K5": 5,
        # Interpersonal - wysokie (4-5)
        "P1": 5, "P2": 5, "P3": 4, "P4": 5, "P5": 4,
        # Intrapersonal - średnie (3)
        "I1": 3, "I2": 3, "I3": 3, "I4": 3, "I5": 3,
        # Naturalistic - średnie (3)
        "N1": 3, "N2": 3, "N3": 3, "N4": 3, "N5": 3
    },
    "expected_top_3": ["kinesthetic", "interpersonal", "linguistic"],
    "description": "Idealny profil dla trenera fitness, instruktora, coacha sportowego"
}

# PROFIL 4: Intrapersonal-Naturalistic (Naukowiec/Badacz)
profile_4 = {
    "name": "Piotr - Badacz",
    "answers": {
        # Linguistic - średnie (3)
        "L1": 3, "L2": 3, "L3": 3, "L4": 3, "L5": 3,
        # Logical - wysokie (4)
        "M1": 4, "M2": 4, "M3": 4, "M4": 4, "M5": 4,
        # Visual - średnie (3)
        "V1": 3, "V2": 3, "V3": 3, "V4": 3, "V5": 3,
        # Musical - niskie (2)
        "U1": 2, "U2": 2, "U3": 2, "U4": 2, "U5": 2,
        # Kinesthetic - niskie (2)
        "K1": 2, "K2": 2, "K3": 2, "K4": 2, "K5": 2,
        # Interpersonal - niskie (2)
        "P1": 2, "P2": 2, "P3": 2, "P4": 2, "P5": 2,
        # Intrapersonal - bardzo wysokie (5)
        "I1": 5, "I2": 5, "I3": 5, "I4": 5, "I5": 5,
        # Naturalistic - bardzo wysokie (5)
        "N1": 5, "N2": 5, "N3": 5, "N4": 5, "N5": 5
    },
    "expected_top_3": ["intrapersonal", "naturalistic", "logical"],
    "description": "Idealny profil dla badacza, naukowca, ekologa"
}

# PROFIL 5: Zrównoważony (Universal)
profile_5 = {
    "name": "Anna - Uniwersalny",
    "answers": {
        # Wszystkie na poziomie 3-4 (zrównoważone)
        "L1": 4, "L2": 3, "L3": 4, "L4": 3, "L5": 4,
        "M1": 3, "M2": 4, "M3": 3, "M4": 4, "M5": 3,
        "V1": 4, "V2": 3, "V3": 4, "V4": 3, "V5": 4,
        "U1": 3, "U2": 4, "U3": 3, "U4": 4, "U5": 3,
        "K1": 4, "K2": 3, "K3": 4, "K4": 3, "K5": 4,
        "P1": 3, "P2": 4, "P3": 3, "P4": 4, "P5": 3,
        "I1": 4, "I2": 3, "I3": 4, "I4": 3, "I5": 4,
        "N1": 3, "N2": 4, "N3": 3, "N4": 4, "N5": 3
    },
    "expected_top_3": ["linguistic", "visual", "kinesthetic"],  # może się różnić
    "description": "Zrównoważony profil - elastyczny learner"
}

# PROFIL 6: Musical-Linguistic (Artysta/Komunikator)
profile_6 = {
    "name": "Jakub - Muzyk",
    "answers": {
        # Linguistic - wysokie (4-5)
        "L1": 5, "L2": 4, "L3": 5, "L4": 4, "L5": 5,
        # Logical - niskie (2)
        "M1": 2, "M2": 2, "M3": 2, "M4": 2, "M5": 2,
        # Visual - średnie (3)
        "V1": 3, "V2": 3, "V3": 3, "V4": 3, "V5": 3,
        # Musical - bardzo wysokie (5)
        "U1": 5, "U2": 5, "U3": 5, "U4": 5, "U5": 5,
        # Kinesthetic - średnie (3)
        "K1": 3, "K2": 3, "K3": 3, "K4": 3, "K5": 3,
        # Interpersonal - wysokie (4)
        "P1": 4, "P2": 4, "P3": 4, "P4": 4, "P5": 4,
        # Intrapersonal - średnie (3)
        "I1": 3, "I2": 3, "I3": 3, "I4": 3, "I5": 3,
        # Naturalistic - niskie (2)
        "N1": 2, "N2": 2, "N3": 2, "N4": 2, "N5": 2
    },
    "expected_top_3": ["musical", "linguistic", "interpersonal"],
    "description": "Idealny profil dla muzyka, artysty, podcaster'a"
}

# PROFILE DO TESTOWANIA
TEST_PROFILES = [
    profile_1,
    profile_2,
    profile_3,
    profile_4,
    profile_5,
    profile_6
]

# Funkcja pomocnicza do testowania
def test_profile(profile_data):
    """Testuje profil i wyświetla wyniki"""
    from utils.mi_test import calculate_mi_scores
    
    print(f"\n{'='*60}")
    print(f"PROFIL: {profile_data['name']}")
    print(f"Opis: {profile_data['description']}")
    print(f"{'='*60}")
    
    result = calculate_mi_scores(profile_data['answers'])
    
    print(f"\n🏆 TOP 3 Inteligencje:")
    for i, (cat, perc) in enumerate(result['top_3'], 1):
        print(f"  #{i} {cat}: {perc:.0f}%")
    
    print(f"\n🌱 BOTTOM 2 Do rozwoju:")
    for i, (cat, perc) in enumerate(result['bottom_2'], 1):
        print(f"  #{i} {cat}: {perc:.0f}%")
    
    print(f"\n📊 Balance Score: {result['balance_score']:.0f}%")
    print(f"📝 Interpretacja: {result['balance_interpretation']}")
    
    # Sprawdź czy top 3 się zgadza z oczekiwanym
    actual_top = [cat for cat, _ in result['top_3']]
    expected = profile_data['expected_top_3']
    
    if set(actual_top) == set(expected):
        print(f"\n✅ TOP 3 zgodne z oczekiwaniami!")
    else:
        print(f"\n⚠️  TOP 3 różni się od oczekiwanego")
        print(f"   Oczekiwane: {expected}")
        print(f"   Otrzymane: {actual_top}")

if __name__ == "__main__":
    print("🧠 TEST WIELORAKICH INTELIGENCJI - PRZYKŁADOWE PROFILE")
    print("="*60)
    
    for profile in TEST_PROFILES:
        test_profile(profile)
    
    print(f"\n{'='*60}")
    print("✅ Wszystkie profile przetestowane!")
    print("="*60)
