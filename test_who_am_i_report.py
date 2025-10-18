"""
Test generowania raportu 'Kim Jestem?'
"""

from utils.profile_report import (
    collect_user_profile_data,
    generate_personal_synthesis,
    generate_recommendations,
    calculate_engagement_score
)

# Test data - użytkownik który wykonał wszystkie testy
test_user_full = {
    'username': 'test_user_full',
    'kolb_test': {
        'dominant_style': 'Diverging (Obserwator-Refleksyjny)',
        'scores': {
            'CE': 85,
            'RO': 90,
            'AC': 60,
            'AE': 55
        }
    },
    'test_scores': {
        'Neuroanalityk': 45,
        'Neuroreaktor': 30,
        'Neurobalanser': 25,
        'Neuroempata': 80,
        'Neuroinnowator': 60
    },
    'mi_test': {
        'top_3': [
            ('interpersonal', 95.0),
            ('linguistic', 85.0),
            ('intrapersonal', 75.0)
        ],
        'scores': {
            'interpersonal': 95.0,
            'linguistic': 85.0,
            'intrapersonal': 75.0,
            'logical': 60.0,
            'visual': 50.0,
            'kinesthetic': 45.0,
            'musical': 40.0,
            'naturalistic': 35.0
        },
        'balance_score': 60.0
    },
    'progress': {
        'overall': 65,
        'komunikacja': {'completed': True, 'progress': 100},
        'przywodztwo': {'completed': False, 'progress': 45},
        'narzedzia': {'completed': True, 'progress': 100}
    },
    'last_login': '2025-10-18 10:30:00'
}

# Test data - użytkownik który wykonał tylko 1 test
test_user_minimal = {
    'username': 'test_user_minimal',
    'kolb_test': {
        'dominant_style': 'Converging (Praktyk)',
        'scores': {
            'CE': 50,
            'RO': 55,
            'AC': 85,
            'AE': 90
        }
    },
    'progress': {
        'overall': 15
    },
    'last_login': '2025-10-10 14:20:00'
}

# Test data - użytkownik bez testów, ale aktywny
test_user_active_no_tests = {
    'username': 'test_user_active',
    'progress': {
        'overall': 80,
        'komunikacja': {'completed': True, 'progress': 100},
        'przywodztwo': {'completed': True, 'progress': 100},
        'narzedzia': {'completed': True, 'progress': 100},
        'rozwoj': {'completed': False, 'progress': 60}
    },
    'last_login': '2025-10-18 09:00:00'
}


def test_full_profile():
    """Test dla użytkownika z pełnym profilem"""
    print("\n" + "="*80)
    print("TEST 1: Użytkownik z pełnym profilem (wszystkie testy + aktywność)")
    print("="*80)
    
    profile_data = collect_user_profile_data(test_user_full)
    
    print(f"\n✅ Ukończone testy: {len(profile_data['tests']['completed'])}/3")
    print(f"   {', '.join(profile_data['tests']['completed'])}")
    
    print(f"\n✅ Mocne strony: {len(profile_data['strengths'])}")
    for i, strength in enumerate(profile_data['strengths'][:5], 1):
        print(f"   {i}. {strength['icon']} {strength['name']}")
    
    print(f"\n✅ Aktywność:")
    print(f"   - Ukończone moduły: {len(profile_data['activity']['modules_completed'])}")
    print(f"   - W trakcie: {len(profile_data['activity']['modules_in_progress'])}")
    print(f"   - Postęp: {profile_data['activity']['total_progress']}%")
    print(f"   - Zaangażowanie: {profile_data['activity']['engagement_score']}/100")
    
    print(f"\n✅ Synteza profilu:")
    synthesis = generate_personal_synthesis(profile_data)
    print(f"   {synthesis[:200]}...")
    
    print(f"\n✅ Rekomendacje:")
    recommendations = generate_recommendations(profile_data)
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. [{rec['priority'].upper()}] {rec['title']}")


def test_minimal_profile():
    """Test dla użytkownika z minimalnym profilem"""
    print("\n" + "="*80)
    print("TEST 2: Użytkownik z minimalnym profilem (1 test, niska aktywność)")
    print("="*80)
    
    profile_data = collect_user_profile_data(test_user_minimal)
    
    print(f"\n✅ Ukończone testy: {len(profile_data['tests']['completed'])}/3")
    print(f"   {', '.join(profile_data['tests']['completed'])}")
    
    print(f"\n✅ Mocne strony: {len(profile_data['strengths'])}")
    for i, strength in enumerate(profile_data['strengths'], 1):
        print(f"   {i}. {strength['icon']} {strength['name']}")
    
    print(f"\n✅ Aktywność:")
    print(f"   - Postęp: {profile_data['activity']['total_progress']}%")
    print(f"   - Zaangażowanie: {profile_data['activity']['engagement_score']}/100")
    
    print(f"\n✅ Rekomendacje:")
    recommendations = generate_recommendations(profile_data)
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"   {i}. [{rec['priority'].upper()}] {rec['title']}")


def test_active_no_tests():
    """Test dla aktywnego użytkownika bez testów"""
    print("\n" + "="*80)
    print("TEST 3: Użytkownik aktywny, ale bez testów diagnostycznych")
    print("="*80)
    
    profile_data = collect_user_profile_data(test_user_active_no_tests)
    
    print(f"\n✅ Ukończone testy: {len(profile_data['tests']['completed'])}/3")
    if not profile_data['tests']['completed']:
        print(f"   ⚠️ Brak testów diagnostycznych!")
    
    print(f"\n✅ Mocne strony: {len(profile_data['strengths'])}")
    for i, strength in enumerate(profile_data['strengths'], 1):
        print(f"   {i}. {strength['icon']} {strength['name']}")
    
    print(f"\n✅ Aktywność:")
    print(f"   - Ukończone moduły: {len(profile_data['activity']['modules_completed'])}")
    print(f"   - Postęp: {profile_data['activity']['total_progress']}%")
    print(f"   - Zaangażowanie: {profile_data['activity']['engagement_score']}/100")
    
    print(f"\n✅ Rekomendacje:")
    recommendations = generate_recommendations(profile_data)
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"   {i}. [{rec['priority'].upper()}] {rec['title']}")


def test_engagement_scoring():
    """Test obliczeń wyniku zaangażowania"""
    print("\n" + "="*80)
    print("TEST 4: Obliczanie wyniku zaangażowania")
    print("="*80)
    
    score1 = calculate_engagement_score(test_user_full)
    score2 = calculate_engagement_score(test_user_minimal)
    score3 = calculate_engagement_score(test_user_active_no_tests)
    
    print(f"\n✅ Użytkownik pełny profil: {score1}/100")
    print(f"✅ Użytkownik minimalny: {score2}/100")
    print(f"✅ Użytkownik aktywny bez testów: {score3}/100")
    
    assert score1 > score2, "Pełny profil powinien mieć wyższy wynik niż minimalny"
    assert score3 > score2, "Aktywny użytkownik powinien mieć wyższy wynik niż nieaktywny"
    print(f"\n✅ Wszystkie asercje przeszły pomyślnie!")


if __name__ == "__main__":
    print("\n" + "#"*80)
    print("# TEST RAPORTU 'KIM JESTEM?'")
    print("#"*80)
    
    try:
        test_full_profile()
        test_minimal_profile()
        test_active_no_tests()
        test_engagement_scoring()
        
        print("\n" + "="*80)
        print("✅ WSZYSTKIE TESTY ZAKOŃCZONE SUKCESEM!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ BŁĄD: {str(e)}")
        import traceback
        traceback.print_exc()
