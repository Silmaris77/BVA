"""
Analizuje strukturę business_games z users_data.json
"""

import json
from pathlib import Path


def analyze_business_games():
    """Analizuje strukturę business_games"""
    
    # Load users data
    users_file = Path(__file__).parent.parent.parent / "users_data.json"
    
    with open(users_file, 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    print("="*80)
    print("📊 BUSINESS GAMES STRUCTURE ANALYSIS")
    print("="*80)
    
    # Find users with business_games
    users_with_games = []
    
    for username, user_data in users.items():
        if 'business_games' in user_data and user_data['business_games']:
            users_with_games.append(username)
    
    print(f"\n✅ Users with business_games: {len(users_with_games)}")
    print(f"   Users: {', '.join(users_with_games)}\n")
    
    # Analyze structure for first user
    if users_with_games:
        first_user = users_with_games[0]
        bg_data = users[first_user]['business_games']
        
        print(f"📋 Analyzing structure for user: {first_user}")
        print(f"   Scenarios: {list(bg_data.keys())}\n")
        
        # Analyze first scenario
        for scenario_name, scenario_data in bg_data.items():
            print(f"\n🎮 Scenario: {scenario_name}")
            print(f"   Keys: {list(scenario_data.keys())}")
            
            # Firm structure
            if 'firm' in scenario_data:
                firm = scenario_data['firm']
                print(f"\n   📊 Firm:")
                print(f"      - name: {firm.get('name')}")
                print(f"      - level: {firm.get('level')}")
                print(f"      - keys: {list(firm.keys())}")
            
            # Employees
            if 'employees' in scenario_data:
                employees = scenario_data['employees']
                print(f"\n   👥 Employees: {len(employees)}")
                if employees:
                    first_emp = employees[0]
                    print(f"      First employee keys: {list(first_emp.keys())}")
                    print(f"      Example: {first_emp.get('name')} - {first_emp.get('role')}")
            
            # Office
            if 'office' in scenario_data:
                office = scenario_data['office']
                print(f"\n   🏢 Office:")
                print(f"      - location: {office.get('location')}")
                print(f"      - keys: {list(office.keys())}")
            
            # Contracts
            if 'contracts' in scenario_data:
                contracts = scenario_data['contracts']
                print(f"\n   📄 Contracts:")
                print(f"      - active: {len(contracts.get('active', []))}")
                print(f"      - completed: {len(contracts.get('completed', []))}")
                print(f"      - failed: {len(contracts.get('failed', []))}")
                if contracts.get('active'):
                    first_contract = contracts['active'][0]
                    print(f"      First active contract keys: {list(first_contract.keys())}")
            
            # Stats
            if 'stats' in scenario_data:
                stats = scenario_data['stats']
                print(f"\n   📈 Stats:")
                print(f"      Keys: {list(stats.keys())}")
                for key, value in stats.items():
                    print(f"      - {key}: {value}")
            
            # Money
            if 'money' in scenario_data:
                print(f"\n   💰 Money: {scenario_data['money']}")
            
            # History
            if 'history' in scenario_data:
                history = scenario_data['history']
                print(f"\n   📜 History:")
                print(f"      Keys: {list(history.keys())}")
                if 'transactions' in history:
                    print(f"      - transactions: {len(history['transactions'])}")
                if 'level_ups' in history:
                    print(f"      - level_ups: {len(history['level_ups'])}")
            
            # Other fields
            other_keys = [k for k in scenario_data.keys() 
                         if k not in ['firm', 'employees', 'office', 'contracts', 'stats', 'money', 'history']]
            if other_keys:
                print(f"\n   ℹ️  Other keys: {other_keys}")
            
            # Save full structure to JSON for reference
            output_file = Path(__file__).parent / f"business_games_structure_{scenario_name}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(scenario_data, f, indent=2, ensure_ascii=False)
            print(f"\n   💾 Full structure saved to: {output_file.name}")
            
            break  # Only analyze first scenario
        
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)


if __name__ == "__main__":
    analyze_business_games()
