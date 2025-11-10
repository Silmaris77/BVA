"""
Test prostego scenariusza Heinz
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scenarios.heinz_simple_visit import HeinzSimpleVisitScenario


def test_client_profile():
    """Test tworzenia profilu klienta"""
    print("🧪 Test 1: Tworzenie profilu klienta")
    
    scenario = HeinzSimpleVisitScenario()
    client = scenario.get_client_profile()
    
    assert client['id'] == 'michal_bistro'
    assert client['owner'] == 'Michał Kowalski'
    assert 'personality' in client
    assert 'current_situation' in client
    
    print("✅ Profil klienta OK")
    print(f"   - Klient: {client['name']}")
    print(f"   - Właściciel: {client['owner']}")
    print(f"   - Typ: {client['personality']['type']}")
    print()


def test_start_conversation():
    """Test rozpoczęcia rozmowy"""
    print("🧪 Test 2: Rozpoczęcie rozmowy")
    
    scenario = HeinzSimpleVisitScenario()
    client = scenario.get_client_profile()
    
    greeting = scenario.start_conversation(client)
    
    print("✅ Rozmowa rozpoczęta")
    print(f"   Klient mówi: \"{greeting}\"")
    print()


def test_continue_conversation():
    """Test kontynuacji rozmowy"""
    print("🧪 Test 3: Kontynuacja rozmowy")
    
    scenario = HeinzSimpleVisitScenario()
    client = scenario.get_client_profile()
    
    # Start
    greeting = scenario.start_conversation(client)
    
    conversation_history = [
        {"role": "assistant", "content": greeting},
        {"role": "user", "content": "Dzień dobry! Jestem z Heinz. Czy mogę poświęcić Panu 5 minut?"}
    ]
    
    response = scenario.continue_conversation(
        client=client,
        conversation_history=conversation_history,
        player_message="Dzień dobry! Jestem z Heinz. Czy mogę poświęcić Panu 5 minut?"
    )
    
    print("✅ Klient odpowiedział")
    print(f"   Klient mówi: \"{response}\"")
    print()


def test_evaluate_conversation():
    """Test oceny rozmowy"""
    print("🧪 Test 4: Ocena rozmowy")
    
    scenario = HeinzSimpleVisitScenario()
    client = scenario.get_client_profile()
    
    # Przykładowa rozmowa
    conversation_history = [
        {"role": "assistant", "content": "Dzień dobry. Słucham?"},
        {"role": "user", "content": "Dzień dobry! Jestem z Heinz. Jaki ketchup Pan obecnie używa?"},
        {"role": "assistant", "content": "Mam Pudliszki."},
        {"role": "user", "content": "A czy klienci pytają o inne marki?"},
        {"role": "assistant", "content": "Czasem pytają o Heinz."},
        {"role": "user", "content": "To może warto przetestować? Heinz ma wyższą marżę - 35% vs 25%."},
        {"role": "assistant", "content": "Hmm, to ciekawe. Ile kosztuje?"},
        {"role": "user", "content": "5kg butelka to 42.50 PLN. Czy mogę przygotować testowe zamówienie?"},
        {"role": "assistant", "content": "Dobra, niech będzie jedna butelka na próbę."}
    ]
    
    score, feedback, analysis = scenario.evaluate_conversation(
        client=client,
        conversation_history=conversation_history
    )
    
    print("✅ Rozmowa oceniona")
    print(f"   Wynik: {score}/100")
    print(f"   Breakdown:")
    if 'breakdown' in analysis:
        for key, value in analysis['breakdown'].items():
            print(f"     - {key}: {value}/25")
    print()
    print(f"   Feedback:")
    print(f"   {feedback[:200]}...")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("🎯 TESTY PROSTEGO SCENARIUSZA HEINZ")
    print("=" * 60)
    print()
    
    try:
        test_client_profile()
        test_start_conversation()
        test_continue_conversation()
        test_evaluate_conversation()
        
        print("=" * 60)
        print("✅ WSZYSTKIE TESTY ZAKOŃCZONE SUKCESEM!")
        print("=" * 60)
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ BŁĄD W TESTACH!")
        print("=" * 60)
        print(f"Błąd: {e}")
        import traceback
        traceback.print_exc()
