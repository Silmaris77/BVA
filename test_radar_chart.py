"""
Test wykresu radarowego Profil 360°
"""

from utils.profile_report import create_360_profile_chart, collect_user_profile_data

# Test user z wszystkimi 3 testami
test_user_full = {
    'username': 'test_full',
    'kolb_test': {
        'style': 'Diverging',
        'scores': {
            'CE': 32,
            'RO': 38,
            'AC': 24,
            'AE': 28
        }
    },
    'test_scores': {
        'Neuroempata': 24,
        'Neuroanalityk': 18,
        'Neuroinnowator': 20,
        'Neuroreaktor': 15,
        'Neurobalanser': 19
    },
    'dominant_neuroleader': 'Neuroempata',
    'mi_test': {
        'results': {
            'interpersonal': 85.5,
            'linguistic': 78.2,
            'intrapersonal': 72.8,
            'logical': 65.3,
            'kinesthetic': 58.7,
            'visual': 55.2,
            'musical': 48.9,
            'naturalistic': 45.1
        }
    },
    'progress': {}
}

# Test user tylko z testem Kolba
test_user_kolb_only = {
    'username': 'test_kolb',
    'kolb_test': {
        'style': 'Converging',
        'scores': {
            'CE': 20,
            'RO': 28,
            'AC': 40,
            'AE': 35
        }
    },
    'progress': {}
}

# Test user tylko z MI
test_user_mi_only = {
    'username': 'test_mi',
    'mi_test': {
        'results': {
            'logical': 88.5,
            'linguistic': 75.2,
            'intrapersonal': 68.8,
            'visual': 62.3,
            'interpersonal': 58.7,
            'kinesthetic': 45.2,
            'musical': 38.9,
            'naturalistic': 35.1
        }
    },
    'progress': {}
}

# Test user bez testów
test_user_no_tests = {
    'username': 'test_none',
    'progress': {
        'Przywództwo': 100,
        'Komunikacja': 100,
        'Innowacyjność': 50
    }
}

def test_radar_chart(user_data, description):
    """Test generowania wykresu radarowego"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"{'='*60}")
    
    try:
        profile_data = collect_user_profile_data(user_data)
        
        # Sprawdź zebrane testy
        tests = profile_data['tests']
        print(f"✅ Kolb: {'TAK' if tests['kolb'] else 'NIE'}")
        print(f"✅ Neuroleader: {'TAK' if tests['neuroleader'] else 'NIE'}")
        print(f"✅ MI: {'TAK' if tests['mi'] else 'NIE'}")
        
        # Generuj wykres
        fig = create_360_profile_chart(profile_data)
        
        if fig:
            print(f"\n✅ Wykres radarowy wygenerowany pomyślnie!")
            print(f"   Liczba punktów danych: {len(fig.data)}")
            if len(fig.data) > 0:
                trace = fig.data[0]
                if hasattr(trace, 'theta') and trace.theta:
                    print(f"   Kategorie na wykresie: {len(trace.theta)}")
                    print(f"   Kategorie: {', '.join(trace.theta[:3])}{'...' if len(trace.theta) > 3 else ''}")
        else:
            print(f"⚠️ Wykres nie został wygenerowany")
            
    except Exception as e:
        print(f"❌ BŁĄD: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TEST WYKRESU RADAROWEGO 'PROFIL 360°'")
    print("="*60)
    
    # Test 1: Wszystkie testy
    test_radar_chart(test_user_full, "Użytkownik z wszystkimi testami (Kolb + Neuroleader + MI)")
    
    # Test 2: Tylko Kolb
    test_radar_chart(test_user_kolb_only, "Użytkownik tylko z testem Kolba")
    
    # Test 3: Tylko MI
    test_radar_chart(test_user_mi_only, "Użytkownik tylko z testem MI")
    
    # Test 4: Bez testów
    test_radar_chart(test_user_no_tests, "Użytkownik bez testów diagnostycznych")
    
    print("\n" + "="*60)
    print("✅ WSZYSTKIE TESTY ZAKOŃCZONE")
    print("="*60)
    print("\n💡 Odśwież stronę w przeglądarce i przejdź do:")
    print("   Profil → Raporty → Kim Jestem? → Wygeneruj raport")
    print("\n")
