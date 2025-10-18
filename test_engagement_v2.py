"""
Test nowego wzoru zaangażowania - Wariant 2
60% Testy + 40% Aktywność
"""

from datetime import datetime, timedelta
from utils.profile_report import calculate_engagement_score

def test_engagement_v2():
    """Test różnych scenariuszy zaangażowania"""
    
    print("\n" + "="*70)
    print("TEST NOWEGO WZORU ZAANGAŻOWANIA (Wariant 2)")
    print("="*70)
    print("📊 60 pkt: Testy diagnostyczne")
    print("⏰ 40 pkt: Ostatnia aktywność")
    print("="*70)
    
    # Scenariusz 1: Super aktywny (3 testy + dzisiaj)
    print("\n🔥 Scenariusz 1: SUPER AKTYWNY")
    user1 = {
        'kolb_test': {'style': 'Diverging'},
        'test_scores': {'Neuroempata': 24},
        'mi_test': {'results': {'interpersonal': 85}},
        'last_login': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    score1 = calculate_engagement_score(user1)
    print(f"   Testy: 3/3 (60 pkt)")
    print(f"   Ostatnie logowanie: DZISIAJ (40 pkt)")
    print(f"   ✅ Wynik: {score1}/100")
    assert score1 == 100, f"Oczekiwano 100, otrzymano {score1}"
    
    # Scenariusz 2: Regularny (3 testy + tydzień temu)
    print("\n⭐ Scenariusz 2: REGULARNY")
    user2 = {
        'kolb_test': {'style': 'Diverging'},
        'test_scores': {'Neuroempata': 24},
        'mi_test': {'results': {'interpersonal': 85}},
        'last_login': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    }
    score2 = calculate_engagement_score(user2)
    print(f"   Testy: 3/3 (60 pkt)")
    print(f"   Ostatnie logowanie: 5 DNI TEMU (30 pkt)")
    print(f"   ✅ Wynik: {score2}/100")
    assert score2 == 90, f"Oczekiwano 90, otrzymano {score2}"
    
    # Scenariusz 3: Nowy użytkownik (1 test + dzisiaj)
    print("\n✅ Scenariusz 3: NOWY UŻYTKOWNIK")
    user3 = {
        'kolb_test': {'style': 'Converging'},
        'last_login': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    score3 = calculate_engagement_score(user3)
    print(f"   Testy: 1/3 (20 pkt)")
    print(f"   Ostatnie logowanie: DZISIAJ (40 pkt)")
    print(f"   ✅ Wynik: {score3}/100")
    assert score3 == 60, f"Oczekiwano 60, otrzymano {score3}"
    
    # Scenariusz 4: Średnio aktywny (2 testy + 2 tygodnie temu)
    print("\n⚠️ Scenariusz 4: ŚREDNIO AKTYWNY")
    user4 = {
        'kolb_test': {'style': 'Diverging'},
        'test_scores': {'Neuroanalityk': 22},
        'last_login': (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S")
    }
    score4 = calculate_engagement_score(user4)
    print(f"   Testy: 2/3 (40 pkt)")
    print(f"   Ostatnie logowanie: 2 TYGODNIE TEMU (15 pkt)")
    print(f"   ✅ Wynik: {score4}/100")
    assert score4 == 55, f"Oczekiwano 55, otrzymano {score4}"
    
    # Scenariusz 5: Starter (1 test + tydzień temu)
    print("\n📊 Scenariusz 5: STARTER")
    user5 = {
        'mi_test': {'results': {'logical': 88}},
        'last_login': (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    }
    score5 = calculate_engagement_score(user5)
    print(f"   Testy: 1/3 (20 pkt)")
    print(f"   Ostatnie logowanie: TYDZIEŃ TEMU (30 pkt)")
    print(f"   ✅ Wynik: {score5}/100")
    assert score5 == 50, f"Oczekiwano 50, otrzymano {score5}"
    
    # Scenariusz 6: Nieaktywny (3 testy + 2 miesiące temu)
    print("\n❌ Scenariusz 6: NIEAKTYWNY")
    user6 = {
        'kolb_test': {'style': 'Diverging'},
        'test_scores': {'Neuroempata': 24},
        'mi_test': {'results': {'interpersonal': 85}},
        'last_login': (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S")
    }
    score6 = calculate_engagement_score(user6)
    print(f"   Testy: 3/3 (60 pkt)")
    print(f"   Ostatnie logowanie: 2 MIESIĄCE TEMU (0 pkt)")
    print(f"   ✅ Wynik: {score6}/100")
    assert score6 == 60, f"Oczekiwano 60, otrzymano {score6}"
    
    # Scenariusz 7: Bez testów, aktywny
    print("\n🆕 Scenariusz 7: BEZ TESTÓW, AKTYWNY")
    user7 = {
        'last_login': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    score7 = calculate_engagement_score(user7)
    print(f"   Testy: 0/3 (0 pkt)")
    print(f"   Ostatnie logowanie: DZISIAJ (40 pkt)")
    print(f"   ✅ Wynik: {score7}/100")
    assert score7 == 40, f"Oczekiwano 40, otrzymano {score7}"
    
    # Scenariusz 8: Format daty bez godziny
    print("\n📅 Scenariusz 8: FORMAT DATY BEZ GODZINY")
    user8 = {
        'kolb_test': {'style': 'Diverging'},
        'test_scores': {'Neuroempata': 24},
        'last_login': datetime.now().strftime("%Y-%m-%d")  # Bez HH:MM:SS
    }
    score8 = calculate_engagement_score(user8)
    print(f"   Testy: 2/3 (40 pkt)")
    print(f"   Ostatnie logowanie: DZISIAJ (format bez godziny) (40 pkt)")
    print(f"   ✅ Wynik: {score8}/100")
    assert score8 == 80, f"Oczekiwano 80, otrzymano {score8}"
    
    print("\n" + "="*70)
    print("✅ WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
    print("="*70)
    
    # Tabela porównawcza
    print("\n📊 TABELA PORÓWNAWCZA:")
    print("-" * 70)
    print(f"{'Scenariusz':<30} {'Testy':<10} {'Aktywność':<20} {'Wynik':>10}")
    print("-" * 70)
    print(f"{'Super aktywny':<30} {'3/3':<10} {'Dzisiaj':<20} {score1:>10}/100")
    print(f"{'Regularny':<30} {'3/3':<10} {'5 dni temu':<20} {score2:>10}/100")
    print(f"{'Nowy użytkownik':<30} {'1/3':<10} {'Dzisiaj':<20} {score3:>10}/100")
    print(f"{'Średnio aktywny':<30} {'2/3':<10} {'2 tygodnie temu':<20} {score4:>10}/100")
    print(f"{'Starter':<30} {'1/3':<10} {'Tydzień temu':<20} {score5:>10}/100")
    print(f"{'Nieaktywny':<30} {'3/3':<10} {'2 miesiące temu':<20} {score6:>10}/100")
    print(f"{'Bez testów':<30} {'0/3':<10} {'Dzisiaj':<20} {score7:>10}/100")
    print("-" * 70)
    
    print("\n💡 WNIOSKI:")
    print("   • Maksymalny wynik (100) = 3 testy + logowanie w ciągu 24h")
    print("   • Wykonanie wszystkich testów = 60% wyniku (główny cel!)")
    print("   • Regularne logowanie = do 40% wyniku (motywacja do powrotu)")
    print("   • Nawet bez testów można mieć 40% (zachęta do rozpoczęcia)")
    print()

if __name__ == "__main__":
    test_engagement_v2()
