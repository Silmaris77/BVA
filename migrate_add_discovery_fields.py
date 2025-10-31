"""
Migration script: Add discovery fields to existing FMCG clients

Adds:
- discovered_info.sales_capacity_discovered = {} (empty - to be discovered)
- discovered_info.market_share_by_category = {} (all categories at 0%)
- knowledge_level = 0 (if not exists)

Run: python migrate_add_discovery_fields.py
"""

import json
import os
import shutil
from datetime import datetime

def migrate_add_discovery_fields():
    """Add discovery fields to all existing FMCG clients"""
    
    # Path to users_data.json
    users_data_path = "users_data.json"
    
    if not os.path.exists(users_data_path):
        print(f"❌ File not found: {users_data_path}")
        return
    
    # Backup first
    backup_path = f"users_data_backup_discovery_{int(datetime.now().timestamp())}.json"
    shutil.copy(users_data_path, backup_path)
    print(f"✅ Backup created: {backup_path}")
    
    # Load users data
    with open(users_data_path, 'r', encoding='utf-8') as f:
        users_data = json.load(f)
    
    print(f"✅ Loaded {len(users_data)} users")
    
    # Prepare all categories
    all_categories = ["Personal Care", "Food", "Home Care", "Snacks", "Beverages"]
    current_month = datetime.now().strftime("%Y-%m")
    
    # Counters
    users_with_fmcg = 0
    clients_updated = 0
    
    # Iterate through all users
    for username, user_data in users_data.items():
        # Check if user has FMCG game
        if "fmcg_game_state" not in user_data or "fmcg_clients" not in user_data:
            continue
        
        users_with_fmcg += 1
        clients = user_data["fmcg_clients"]
        
        # Iterate through clients
        for client_id, client in clients.items():
            # Initialize discovered_info if not exists
            if "discovered_info" not in client:
                client["discovered_info"] = {}
            
            discovered_info = client["discovered_info"]
            
            # Add sales_capacity_discovered (empty on start)
            if "sales_capacity_discovered" not in discovered_info:
                discovered_info["sales_capacity_discovered"] = {}
                print(f"   → {client.get('name', client_id)}: Added sales_capacity_discovered = {{}}")
            
            # Add market_share_by_category (all categories at 0%)
            if "market_share_by_category" not in discovered_info:
                discovered_info["market_share_by_category"] = {}
                
                for category in all_categories:
                    discovered_info["market_share_by_category"][category] = {
                        "player_share": 0,
                        "competitor_share": 100,
                        "player_volume_weekly": 0,
                        "total_volume_weekly": 0,  # Unknown until discovered
                        "trend": "stable",
                        "trend_percentage": 0,
                        "last_updated": datetime.now().isoformat(),
                        "history": [
                            {
                                "month": current_month,
                                "player_share": 0,
                                "player_volume": 0
                            }
                        ]
                    }
                
                print(f"   → {client.get('name', client_id)}: Added market_share_by_category (5 categories at 0%)")
            
            # Initialize all other discovery fields if missing
            discovery_fields = [
                "personality_description",
                "decision_priorities",
                "main_customers",
                "customer_demographics",
                "competing_brands",
                "shelf_space_constraints",
                "pain_points",
                "business_goals",
                "typical_order_value",
                "preferred_frequency",
                "payment_terms",
                "delivery_preferences",
                "best_selling_categories",
                "seasonal_patterns",
                "trust_level",
                "preferred_communication"
            ]
            
            for field in discovery_fields:
                if field not in discovered_info:
                    discovered_info[field] = None
            
            # Update client
            client["discovered_info"] = discovered_info
            
            # Initialize knowledge_level if not exists
            if "knowledge_level" not in client:
                client["knowledge_level"] = 0
                print(f"   → {client.get('name', client_id)}: Added knowledge_level = 0")
            
            # Initialize discovery_notes if not exists
            if "discovery_notes" not in client:
                client["discovery_notes"] = []
            
            clients_updated += 1
        
        # Update user data
        user_data["fmcg_clients"] = clients
    
    # Save updated data
    with open(users_data_path, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Migration complete!")
    print(f"   Users with FMCG: {users_with_fmcg}")
    print(f"   Clients updated: {clients_updated}")
    print(f"   Backup: {backup_path}")

if __name__ == "__main__":
    migrate_add_discovery_fields()
