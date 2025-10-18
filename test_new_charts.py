"""
Test nowych wykresów: 3 radary + gauge + mocne strony
"""

from utils.profile_report import (
    collect_user_profile_data,
    create_kolb_radar_chart,
    create_neuroleader_radar_chart,
    create_mi_radar_chart,
    create_engagement_gauge,
    create_strengths_bars
)

# Test user z wszystkimi 3 testami
test_user_full = {
    'username': 'test_full',
    'kolb_test': {
        'dominant_style': 'Diverging',
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
        },
        'top_3': [
            ('interpersonal', 85.5),
            ('linguistic', 78.2),
            ('intrapersonal', 72.8)
        ]
    },
    'progress': {
        'Przywództwo': {'completed': True, 'progress': 100},
        'Komunikacja': {'completed': True, 'progress': 100},
        'Innowacyjność': {'completed': False, 'progress': 50}
    },
    'last_login': '2025-10-18'
}

def test_charts(user_data, description):
    """Test generowania wszystkich wykresów"""
    print(f"\n{'='*70}")
    print(f"TEST: {description}")
    print(f"{'='*70}")
    
    try:
        # Zbierz dane profilu
        profile_data = collect_user_profile_data(user_data)
        
        print(f"\n📊 Zebrane dane:")
        print(f"   - Testy: {', '.join(profile_data['tests']['completed'])}")
        print(f"   - Mocne strony: {len(profile_data['strengths'])}")
        print(f"   - Zaangażowanie: {profile_data['activity']['engagement_score']}/100")
        
        # Test 1: Kolb radar
        print(f"\n🔄 Test wykresu Kolba...")
        kolb_chart = create_kolb_radar_chart(profile_data)
        if kolb_chart:
            print(f"   ✅ Wykres Kolba wygenerowany: {len(kolb_chart.data)} trace(s)")
        else:
            print(f"   ⚠️ Brak testu Kolba")
        
        # Test 2: Neuroleader radar
        print(f"\n🧬 Test wykresu Neuroleader...")
        neuroleader_chart = create_neuroleader_radar_chart(profile_data)
        if neuroleader_chart:
            print(f"   ✅ Wykres Neuroleader wygenerowany: {len(neuroleader_chart.data)} trace(s)")
        else:
            print(f"   ⚠️ Brak testu Neuroleader")
        
        # Test 3: MI radar
        print(f"\n🧠 Test wykresu MI...")
        mi_chart = create_mi_radar_chart(profile_data)
        if mi_chart:
            print(f"   ✅ Wykres MI wygenerowany: {len(mi_chart.data)} trace(s)")
            if hasattr(mi_chart.data[0], 'theta'):
                print(f"   📌 Inteligencje: {len(mi_chart.data[0].theta)}")
        else:
            print(f"   ⚠️ Brak testu MI")
        
        # Test 4: Gauge zaangażowania
        print(f"\n⚡ Test gauge zaangażowania...")
        gauge_chart = create_engagement_gauge(profile_data)
        if gauge_chart:
            print(f"   ✅ Gauge wygenerowany: {gauge_chart.data[0].value}/100")
        else:
            print(f"   ❌ Błąd generowania gauge")
        
        # Test 5: Paski mocnych stron
        print(f"\n💪 Test pasków mocnych stron...")
        strengths_bars = create_strengths_bars(profile_data)
        if strengths_bars:
            print(f"   ✅ Paski wygenerowane: {len(strengths_bars.data[0].y)} mocnych stron")
            print(f"   📌 Top 3: {', '.join(strengths_bars.data[0].y[-3:][::-1])}")
        else:
            print(f"   ⚠️ Brak mocnych stron")
        
        print(f"\n✅ Test zakończony sukcesem!")
        
    except Exception as e:
        print(f"\n❌ BŁĄD: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TEST NOWYCH WYKRESÓW - OPCJA 1")
    print("="*70)
    print("🎯 3 Radary + Gauge + Top 5 Mocnych Stron")
    
    # Test z pełnym profilem
    test_charts(test_user_full, "Użytkownik z wszystkimi testami")
    
    # Test tylko z Kolbem
    test_user_kolb = {
        'username': 'test_kolb',
        'kolb_test': {
            'dominant_style': 'Converging',
            'scores': {'CE': 20, 'RO': 28, 'AC': 40, 'AE': 35}
        },
        'progress': {}
    }
    test_charts(test_user_kolb, "Użytkownik tylko z testem Kolba")
    
    # Test bez testów
    test_user_none = {
        'username': 'test_none',
        'progress': {
            'Przywództwo': {'completed': True, 'progress': 100}
        }
    }
    test_charts(test_user_none, "Użytkownik bez testów diagnostycznych")
    
    print("\n" + "="*70)
    print("✅ WSZYSTKIE TESTY ZAKOŃCZONE")
    print("="*70)
    print("\n💡 Odśwież przeglądarkę i zobacz nowe wykresy!")
    print("   Profil → Raporty → Kim Jestem? → Wygeneruj raport\n")
