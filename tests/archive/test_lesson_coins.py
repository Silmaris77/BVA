"""
Test: Sprawdzenie że monety NIE są dodawane za lekcje
Tylko XP powinno się zwiększać w lekcjach.
"""

import sys
import os

# Dodaj ścieżkę do głównego katalogu projektu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.lesson_progress import award_fragment_xp
from data.users import load_user_data, save_user_data
import streamlit as st

def test_lesson_no_coins():
    """Test: Lekcje dodają XP ale NIE dodają monet"""
    print("\n" + "="*60)
    print("TEST: Lekcje NIE dodają monet (tylko XP)")
    print("="*60)
    
    # Utwórz testowego użytkownika
    test_username = "test_lesson_user"
    users_data = load_user_data()
    
    # Ustaw początkowe wartości
    initial_xp = 100
    initial_coins = 1000
    
    users_data[test_username] = {
        "username": test_username,
        "xp": initial_xp,
        "degencoins": initial_coins,
        "lesson_progress": {}
    }
    save_user_data(users_data)
    
    # Symuluj session_state
    class MockSessionState:
        username = test_username
        user_data = users_data[test_username]
    
    st.session_state = MockSessionState()
    
    print(f"\n📊 Stan początkowy:")
    print(f"   XP: {initial_xp}")
    print(f"   Monety: {initial_coins}")
    
    # Przyznaj XP za fragment lekcji
    xp_to_award = 50
    awarded, xp_amount = award_fragment_xp("lesson_001", "intro", xp_to_award)
    
    # Odczytaj zaktualizowane dane
    users_data = load_user_data()
    user_data = users_data[test_username]
    
    final_xp = user_data.get('xp', 0)
    final_coins = user_data.get('degencoins', 0)
    
    print(f"\n📊 Stan po ukończeniu fragmentu lekcji (50 XP):")
    print(f"   XP: {initial_xp} → {final_xp} ({'+' if final_xp > initial_xp else ''}{final_xp - initial_xp})")
    print(f"   Monety: {initial_coins} → {final_coins} ({'+' if final_coins > initial_coins else ''}{final_coins - initial_coins})")
    
    # Sprawdzenia
    assert awarded, "XP powinno zostać przyznane"
    assert xp_amount == xp_to_award, f"Przyznane XP powinno wynosić {xp_to_award}, jest {xp_amount}"
    
    # KLUCZOWY TEST: XP wzrosło, monety NIE
    assert final_xp == initial_xp + xp_to_award, f"XP powinno wzrosnąć o {xp_to_award}"
    assert final_coins == initial_coins, f"Monety NIE powinny się zmienić! Były: {initial_coins}, są: {final_coins}"
    
    print("\n✅ TEST PRZESZEDŁ!")
    print("   ✓ XP wzrosło o 50")
    print("   ✓ Monety pozostały bez zmian (1000)")
    print("   ✓ System nagród działa poprawnie - lekcje dają tylko XP")
    
    # Cleanup
    del users_data[test_username]
    save_user_data(users_data)
    
    return True

def test_multiple_fragments():
    """Test: Wiele fragmentów lekcji - tylko XP, brak monet"""
    print("\n" + "="*60)
    print("TEST: Wiele fragmentów - tylko XP")
    print("="*60)
    
    test_username = "test_multiple_user"
    users_data = load_user_data()
    
    initial_xp = 0
    initial_coins = 1000
    
    users_data[test_username] = {
        "username": test_username,
        "xp": initial_xp,
        "degencoins": initial_coins,
        "lesson_progress": {}
    }
    save_user_data(users_data)
    
    class MockSessionState:
        username = test_username
        user_data = users_data[test_username]
    
    st.session_state = MockSessionState()
    
    print(f"\n📊 Stan początkowy:")
    print(f"   XP: {initial_xp}")
    print(f"   Monety: {initial_coins}")
    
    # Wykonaj różne fragmenty
    fragments = [
        ("lesson_001", "intro", 5),      # Lesson started
        ("lesson_001", "content", 15),   # Content read
        ("lesson_001", "quiz", 20),      # Quiz completed
        ("lesson_001", "ai_exercise", 15), # AI exercise
        ("lesson_001", "summary", 50),   # Lesson completed
    ]
    
    total_xp_expected = sum(xp for _, _, xp in fragments)
    
    for lesson_id, fragment_type, xp in fragments:
        awarded, _ = award_fragment_xp(lesson_id, fragment_type, xp)
        st.session_state.user_data = load_user_data()[test_username]
    
    # Odczytaj finalne dane
    users_data = load_user_data()
    user_data = users_data[test_username]
    
    final_xp = user_data.get('xp', 0)
    final_coins = user_data.get('degencoins', 0)
    
    print(f"\n📊 Stan po ukończeniu 5 fragmentów:")
    print(f"   XP: {initial_xp} → {final_xp} (+{final_xp - initial_xp})")
    print(f"   Monety: {initial_coins} → {final_coins} ({'+' if final_coins > initial_coins else ''}{final_coins - initial_coins})")
    
    # Sprawdzenia
    assert final_xp == total_xp_expected, f"XP powinno wynosić {total_xp_expected}, jest {final_xp}"
    assert final_coins == initial_coins, f"Monety NIE powinny się zmienić!"
    
    print("\n✅ TEST PRZESZEDŁ!")
    print(f"   ✓ XP wzrosło o {total_xp_expected}")
    print("   ✓ Monety pozostały bez zmian (1000)")
    print("   ✓ System działa poprawnie dla wielu fragmentów")
    
    # Cleanup
    del users_data[test_username]
    save_user_data(users_data)
    
    return True

if __name__ == "__main__":
    print("\n" + "🧪"*30)
    print("TEST SUITE: System monet - tylko Business Games")
    print("🧪"*30)
    
    try:
        test_lesson_no_coins()
        test_multiple_fragments()
        
        print("\n" + "="*60)
        print("🎉 WSZYSTKIE TESTY PRZESZŁY!")
        print("="*60)
        print("\n✨ Potwierdzenie:")
        print("   - Lekcje dodają TYLKO XP")
        print("   - Monety są dostępne TYLKO w Business Games")
        print("   - System walut działa zgodnie z założeniami")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
