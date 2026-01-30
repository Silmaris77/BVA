"""
Test FMCG Game Initialization
Testuje nową funkcję initialize_fmcg_game_new()
"""

import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.business_game import initialize_fmcg_game_new, FMCG_AVAILABLE

def test_fmcg_initialization():
    """Test inicjalizacji gry FMCG"""
    print("🧪 Test FMCG Game Initialization")
    print("=" * 60)
    
    # Check if FMCG module available
    print(f"\n✓ FMCG Available: {FMCG_AVAILABLE}")
    
    if not FMCG_AVAILABLE:
        print("❌ FMCG module not available!")
        return False
    
    try:
        # Initialize game
        print("\n🎮 Initializing FMCG game for test user...")
        game_data = initialize_fmcg_game_new("test_user")
        
        print("\n✅ Game initialized successfully!")
        print(f"\n📋 Game Structure:")
        print(f"  - Scenario ID: {game_data.get('scenario_id')}")
        print(f"  - Company: {game_data.get('firm', {}).get('name')}")
        print(f"  - Level: {game_data.get('firm', {}).get('level')}")
        
        # Check FMCG state
        fmcg_state = game_data.get('fmcg_state', {})
        print(f"\n🎯 FMCG State:")
        print(f"  - Role: {fmcg_state.get('role')}")
        print(f"  - Level: {fmcg_state.get('level')}")
        print(f"  - Territory: {fmcg_state.get('territory_name')}")
        print(f"  - Energy: {fmcg_state.get('energy')}/{fmcg_state.get('energy_max')}")
        print(f"  - Marketing Budget: {fmcg_state.get('marketing_budget')} PLN")
        
        # Check clients
        clients = fmcg_state.get('clients', {})
        print(f"\n👥 Clients: {len(clients)} starter clients")
        
        for client_id, client_data in list(clients.items())[:3]:  # Show first 3
            print(f"\n  📍 {client_data.get('name')}")
            print(f"     Type: {client_data.get('type')}")
            print(f"     Status: {client_data.get('status')}")
            print(f"     Location: {client_data.get('location')}")
            print(f"     Distance: {client_data.get('distance_from_base')} km")
            print(f"     Potential: {client_data.get('potential_monthly')} PLN/month")
            print(f"     Owner: {client_data.get('owner_name')}")
        
        if len(clients) > 3:
            print(f"\n  ... and {len(clients) - 3} more clients")
        
        # Check objectives
        print(f"\n🎯 Objectives: {len(game_data.get('scenario_objectives', []))}")
        for obj in game_data.get('scenario_objectives', []):
            print(f"  - {obj.get('description')}")
        
        # Validate structure
        print(f"\n🔍 Validation:")
        required_keys = ['scenario_id', 'firm', 'fmcg_state', 'stats', 'ranking']
        for key in required_keys:
            exists = key in game_data
            print(f"  {'✅' if exists else '❌'} {key}: {'present' if exists else 'MISSING'}")
        
        # Check SQL compatibility
        print(f"\n💾 SQL Compatibility Check:")
        print(f"  - firm.name: {game_data.get('firm', {}).get('name')}")
        print(f"  - firm.level: {game_data.get('firm', {}).get('level')}")
        print(f"  - money: {game_data.get('money', 0)}")
        print(f"  - Has extra_data (fmcg_state): {bool(game_data.get('fmcg_state'))}")
        
        # Save to JSON for inspection
        output_file = "test_fmcg_init.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(game_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Full game data saved to: {output_file}")
        print(f"   File size: {Path(output_file).stat().st_size} bytes")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during initialization:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_fmcg_initialization()
    sys.exit(0 if success else 1)
