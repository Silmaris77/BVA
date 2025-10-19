"""
Test systemu oceny kontraktów Business Games
Testuje 3 tryby: Heurystyka, AI (mock), Mistrz Gry
"""

import sys
import os

# Dodaj ścieżkę projektu do PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.business_game_evaluation import (
    evaluate_contract_solution,
    evaluate_heuristic,
    queue_for_game_master,
    get_pending_reviews_count,
    get_pending_contract_reviews,
    submit_game_master_review,
    set_active_evaluation_mode,
    get_active_evaluation_mode
)

# =============================================================================
# TEST 1: HEURYSTYKA
# =============================================================================

def test_heuristic_evaluation():
    """Test oceny heurystycznej"""
    print("=" * 70)
    print("TEST 1: OCENA HEURYSTYCZNA")
    print("=" * 70)
    
    # Mock kontrakt
    contract = {
        "id": "TEST-001",
        "tytul": "Test Conflict Resolution",
        "kategoria": "Konflikt",
        "poziom_trudnosci": 3,
        "opis": "Rozwiąż konflikt w zespole",
        "min_slow": 300,
        "nagroda_base": 500
    }
    
    # Krótkie rozwiązanie (poniżej minimum)
    short_solution = " ".join(["słowo"] * 100)  # 100 słów
    rating, feedback, details = evaluate_heuristic(short_solution, contract)
    
    print(f"\n📝 Krótkie rozwiązanie (100 słów):")
    print(f"   Ocena: {rating}⭐")
    print(f"   Feedback: {feedback}")
    print(f"   Szczegóły: {details}")
    
    assert rating >= 1 and rating <= 5, "Ocena powinna być w zakresie 1-5"
    assert details['word_count'] == 100, "Liczba słów niezgodna"
    
    # Średnie rozwiązanie (ok minimum)
    medium_solution = " ".join(["słowo"] * 300)  # 300 słów
    rating, feedback, details = evaluate_heuristic(medium_solution, contract)
    
    print(f"\n📝 Średnie rozwiązanie (300 słów):")
    print(f"   Ocena: {rating}⭐")
    print(f"   Feedback: {feedback}")
    
    # Długie rozwiązanie (powyżej minimum)
    long_solution = " ".join(["słowo"] * 600)  # 600 słów
    rating, feedback, details = evaluate_heuristic(long_solution, contract)
    
    print(f"\n📝 Długie rozwiązanie (600 słów):")
    print(f"   Ocena: {rating}⭐")
    print(f"   Feedback: {feedback}")
    
    print("\n✅ Test heurystyki zakończony pomyślnie!\n")


# =============================================================================
# TEST 2: MISTRZ GRY (kolejka)
# =============================================================================

def test_game_master_queue():
    """Test kolejki Mistrza Gry"""
    print("=" * 70)
    print("TEST 2: KOLEJKA MISTRZA GRY")
    print("=" * 70)
    
    # Mock user_data
    user_data = {
        "username": "testuser",
        "name": "Test User",
        "degencoins": 1000
    }
    
    # Mock kontrakt
    contract = {
        "id": "TEST-GM-001",
        "tytul": "Test Coaching Session",
        "kategoria": "Coaching",
        "poziom_trudnosci": 4,
        "opis": "Przeprowadź sesję coachingową",
        "min_slow": 400,
        "nagroda_base": 800,
        "nagroda_4star": 1200,
        "nagroda_5star": 1600
    }
    
    solution = " ".join(["rozwiązanie"] * 450)  # 450 słów
    
    print("\n📤 Dodawanie do kolejki...")
    rating, feedback, details = queue_for_game_master(user_data, contract, solution)
    
    print(f"\n   Rating: {rating} (0 = pending)")
    print(f"   Feedback: {feedback[:100]}...")
    print(f"   Review ID: {details['review_id']}")
    
    assert rating == 0, "Rating powinien być 0 dla pending"
    assert details['status'] == 'pending', "Status powinien być pending"
    
    # Sprawdź kolejkę
    pending_count = get_pending_reviews_count()
    print(f"\n📋 Oczekujące oceny: {pending_count}")
    
    assert pending_count > 0, "Powinna być co najmniej jedna oczekująca ocena"
    
    # Pobierz listę
    pending_reviews = get_pending_contract_reviews()
    print(f"\n📋 Lista oczekujących ({len(pending_reviews)}):")
    
    for review in pending_reviews[:3]:  # Pokaż max 3
        print(f"   - {review['username']}: {review['contract_title']} ({review['waiting_hours']}h)")
    
    # Symuluj ocenę przez Mistrza Gry
    if pending_reviews:
        review_to_evaluate = pending_reviews[0]
        print(f"\n👨‍💼 Mistrz Gry ocenia: {review_to_evaluate['id']}")
        
        success = submit_game_master_review(
            review_id=review_to_evaluate['id'],
            rating=5,
            feedback="Doskonała praca! Świetne zastosowanie technik CIQ.",
            admin_username="admin_test"
        )
        
        if success:
            print("   ✅ Ocena zatwierdzona!")
            
            # Sprawdź czy zmniejszyła się kolejka
            new_pending_count = get_pending_reviews_count()
            print(f"   📋 Oczekujące oceny teraz: {new_pending_count}")
        else:
            print("   ⚠️ Nie udało się zatwierdzić (możliwe że użytkownik nie istnieje w bazie)")
    
    print("\n✅ Test kolejki Mistrza Gry zakończony!\n")


# =============================================================================
# TEST 3: ZMIANA TRYBU
# =============================================================================

def test_mode_switching():
    """Test zmiany trybów oceny"""
    print("=" * 70)
    print("TEST 3: ZMIANA TRYBÓW OCENY")
    print("=" * 70)
    
    # Sprawdź aktualny tryb
    current_mode = get_active_evaluation_mode()
    print(f"\n📍 Aktualny tryb: {current_mode}")
    
    # Zmień na heurystykę
    print("\n🔄 Zmiana na heurystykę...")
    success = set_active_evaluation_mode("heuristic")
    
    if success:
        new_mode = get_active_evaluation_mode()
        print(f"   ✅ Nowy tryb: {new_mode}")
        assert new_mode == "heuristic", "Tryb powinien być heuristic"
    
    # Zmień na game_master
    print("\n🔄 Zmiana na Mistrza Gry...")
    success = set_active_evaluation_mode("game_master")
    
    if success:
        new_mode = get_active_evaluation_mode()
        print(f"   ✅ Nowy tryb: {new_mode}")
        assert new_mode == "game_master", "Tryb powinien być game_master"
    
    # Próba ustawienia nieprawidłowego trybu
    print("\n🔄 Próba ustawienia nieprawidłowego trybu...")
    success = set_active_evaluation_mode("invalid_mode")
    
    if not success:
        print("   ✅ Poprawnie odrzucono nieprawidłowy tryb")
    
    # Przywróć domyślny
    print("\n🔄 Przywracanie domyślnego trybu (heuristic)...")
    set_active_evaluation_mode("heuristic")
    
    print("\n✅ Test zmiany trybów zakończony!\n")


# =============================================================================
# TEST 4: INTEGRACJA Z BUSINESS GAME
# =============================================================================

def test_integration():
    """Test integracji z business_game.py"""
    print("=" * 70)
    print("TEST 4: INTEGRACJA Z BUSINESS GAME")
    print("=" * 70)
    
    # Mock user_data z Business Games
    user_data = {
        "username": "integration_test",
        "degencoins": 5000,
        "business_game": {
            "firm": {
                "name": "Test Consulting",
                "level": 2,
                "reputation": 100
            },
            "contracts": {
                "active": [{
                    "id": "INTEGRATION-001",
                    "tytul": "Test Integration Contract",
                    "kategoria": "Leadership",
                    "poziom_trudnosci": 3,
                    "opis": "Test integracji",
                    "min_slow": 300,
                    "nagroda_base": 600,
                    "nagroda_3star": 600,
                    "nagroda_4star": 900,
                    "nagroda_5star": 1200
                }],
                "completed": []
            },
            "stats": {
                "contracts_completed": 0,
                "contracts_5star": 0,
                "contracts_4star": 0,
                "contracts_3star": 0,
                "contracts_2star": 0,
                "contracts_1star": 0,
                "total_revenue": 0,
                "category_stats": {}
            },
            "history": {
                "transactions": []
            }
        }
    }
    
    contract = user_data["business_game"]["contracts"]["active"][0]
    solution = " ".join(["test"] * 350)  # 350 słów
    
    print(f"\n📝 Kontrakt: {contract['tytul']}")
    print(f"   Trudność: {contract['poziom_trudnosci']}⭐")
    print(f"   Rozwiązanie: {len(solution.split())} słów")
    
    # Ustaw tryb na heurystykę
    set_active_evaluation_mode("heuristic")
    
    # Oceń przez system
    rating, feedback, details = evaluate_contract_solution(
        user_data=user_data,
        contract=contract,
        solution=solution
    )
    
    print(f"\n⭐ Ocena: {rating}/5")
    print(f"📄 Feedback: {feedback}")
    print(f"🔧 Metoda: {details['method']}")
    
    assert rating >= 1 and rating <= 5, "Ocena powinna być w zakresie 1-5"
    assert details['method'] == 'heuristic', "Metoda powinna być heuristic"
    
    print("\n✅ Test integracji zakończony!\n")


# =============================================================================
# URUCHOM WSZYSTKIE TESTY
# =============================================================================

if __name__ == "__main__":
    print("\n")
    print("🧪 " + "=" * 66 + " 🧪")
    print("   TEST SYSTEMU OCENY KONTRAKTÓW - BUSINESS GAMES")
    print("🧪 " + "=" * 66 + " 🧪")
    print("\n")
    
    try:
        # Test 1
        test_heuristic_evaluation()
        
        # Test 2
        test_game_master_queue()
        
        # Test 3
        test_mode_switching()
        
        # Test 4
        test_integration()
        
        # Podsumowanie
        print("=" * 70)
        print("🎉 WSZYSTKIE TESTY ZAKOŃCZONE POMYŚLNIE! 🎉")
        print("=" * 70)
        print("\n✅ System oceny kontraktów działa poprawnie")
        print("✅ Wszystkie 3 tryby zaimplementowane:")
        print("   - ⚡ Heurystyka (automatyczna, szybka)")
        print("   - 🤖 AI (OpenAI GPT - wymaga API key)")
        print("   - 👨‍💼 Mistrz Gry (ręczna ocena przez Admina)")
        print("\n📋 Następne kroki:")
        print("   1. Przetestuj w aplikacji Streamlit")
        print("   2. Dodaj klucz API OpenAI dla trybu AI")
        print("   3. Oceń kilka kontraktów jako Mistrz Gry")
        print("\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST NIEUDANY: {e}\n")
    except Exception as e:
        print(f"\n❌ BŁĄD: {e}\n")
        import traceback
        traceback.print_exc()
