"""
Test AI Conversation Contract Flow (bez UI)
Emuluje pełen cykl życia kontraktu AI Conversation
"""

import streamlit as st
from datetime import datetime
from utils.ai_conversation_engine import (
    initialize_ai_conversation,
    get_conversation_state,
    calculate_final_conversation_score
)
from utils.business_game import submit_contract_ai_conversation
from data.business_data import CONTRACTS_POOL

# Mock session state (Streamlit requirement)
if not hasattr(st, 'session_state'):
    st.session_state = {}

def test_ai_conversation_flow():
    """Test pełnego flow AI Conversation bez rzeczywistego AI"""
    
    print("=" * 80)
    print("TEST: AI Conversation Contract Flow")
    print("=" * 80)
    
    # 1. Znajdź kontrakt AI Conversation
    ai_contracts = [c for c in CONTRACTS_POOL if c.get("contract_type") == "ai_conversation"]
    
    if not ai_contracts:
        print("❌ Brak kontraktów AI Conversation w CONTRACTS_POOL")
        return
    
    contract = ai_contracts[0]
    contract_id = contract["id"]
    
    print(f"\n✅ Znaleziono kontrakt: {contract['tytul']}")
    print(f"   ID: {contract_id}")
    print(f"   NPC: {contract['npc_config']['name']} ({contract['npc_config']['role']})")
    
    # 2. Inicjalizuj konwersację
    print("\n📝 Inicjalizacja konwersacji...")
    npc_config = contract["npc_config"]
    scenario_context = contract["scenario_context"]
    
    initialize_ai_conversation(contract_id, npc_config, scenario_context)
    
    # 3. Sprawdź stan
    conversation = get_conversation_state(contract_id)
    print(f"   Stan: conversation_active = {conversation.get('conversation_active')}")
    print(f"   Wiadomości: {len(conversation.get('messages', []))}")
    print(f"   Tura: {conversation.get('current_turn')}")
    
    # 4. Symuluj zakończenie rozmowy (manual)
    # Ustawimy conversation_active = False i sztuczne punkty
    st.session_state[f"dt_{contract_id}_conversation_active"] = False
    st.session_state[f"dt_{contract_id}_total_score"] = 85  # Symulacja dobrego wyniku
    st.session_state[f"dt_{contract_id}_metrics"] = {
        "empathy": 80,
        "assertiveness": 75,
        "professionalism": 90,
        "solution_quality": 85
    }
    st.session_state[f"dt_{contract_id}_current_turn"] = 5
    
    print("\n🎯 Symulacja zakończenia rozmowy (85 punktów, 5 tur)...")
    
    # 5. Oblicz finalny wynik
    result = calculate_final_conversation_score(contract_id)
    
    print(f"\n📊 Wynik końcowy:")
    print(f"   Gwiazdki: {result['stars']}/5")
    print(f"   Punkty: {result['total_points']}")
    print(f"   Tur: {result['turn_count']}")
    print(f"   Typ zakończenia: {result.get('ending_type', 'N/A')}")
    print(f"\n   Metryki:")
    for key, value in result.get('metrics', {}).items():
        print(f"      - {key}: {value}/100")
    
    # 6. Test submit_contract_ai_conversation
    print("\n💰 Test submit_contract_ai_conversation()...")
    
    # Przygotuj mock user_data
    user_data = {
        "degencoins": 1000,
        "business_game": {
            "firm": {
                "name": "Test Consulting",
                "level": 2,
                "reputation": 50
            },
            "contracts": {
                "active": [contract.copy()],  # Dodaj kontrakt do aktywnych
                "completed": []
            },
            "stats": {
                "contracts_completed": 0,
                "contracts_5star": 0,
                "contracts_4star": 0,
                "contracts_3star": 0,
                "contracts_2star": 0,
                "contracts_1star": 0
            },
            "history": {
                "transactions": []
            }
        }
    }
    
    # Wywołaj submit
    updated_user_data, success, message, _ = submit_contract_ai_conversation(user_data, contract_id)
    
    if success:
        print(f"   ✅ {message}")
        print(f"\n📈 Zmiany w user_data:")
        print(f"   DegenCoins: {user_data['degencoins']} → {updated_user_data['degencoins']} "
              f"(+{updated_user_data['degencoins'] - user_data['degencoins']})")
        print(f"   Reputacja: {user_data['business_game']['firm']['reputation']} → "
              f"{updated_user_data['business_game']['firm']['reputation']} "
              f"(+{updated_user_data['business_game']['firm']['reputation'] - user_data['business_game']['firm']['reputation']})")
        print(f"   Ukończone kontrakty: {len(updated_user_data['business_game']['contracts']['completed'])}")
        print(f"   Aktywne kontrakty: {len(updated_user_data['business_game']['contracts']['active'])}")
        
        # Sprawdź statystyki
        stats = updated_user_data['business_game']['stats']
        print(f"\n📊 Statystyki:")
        print(f"   Total completed: {stats['contracts_completed']}")
        print(f"   Rozkład gwiazdek: 5★={stats['contracts_5star']}, 4★={stats['contracts_4star']}, "
              f"3★={stats['contracts_3star']}, 2★={stats['contracts_2star']}, 1★={stats['contracts_1star']}")
        
    else:
        print(f"   ❌ {message}")
    
    print("\n" + "=" * 80)
    print("✅ TEST ZAKOŃCZONY POMYŚLNIE")
    print("=" * 80)

if __name__ == "__main__":
    test_ai_conversation_flow()
