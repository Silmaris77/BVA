"""
Final database statistics after migration
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import session_scope
from database.models import User, BusinessGame, BusinessGameContract, BusinessGameStats, BusinessGameTransaction
from sqlalchemy import func

print("="*80)
print("📊 FINAL DATABASE STATISTICS")
print("="*80)

with session_scope() as session:
    # Users
    total_users = session.query(func.count(User.id)).scalar()
    print(f"\n👥 Users: {total_users}")
    
    # Business Games
    total_games = session.query(func.count(BusinessGame.id)).scalar()
    print(f"🎮 Business Games: {total_games}")
    
    # Contracts
    total_contracts = session.query(func.count(BusinessGameContract.id)).scalar()
    contracts_by_status = session.query(
        BusinessGameContract.status,
        func.count(BusinessGameContract.id)
    ).group_by(BusinessGameContract.status).all()
    
    print(f"📄 Contracts: {total_contracts}")
    for status, count in contracts_by_status:
        print(f"   - {status}: {count}")
    
    # Stats
    total_stats = session.query(func.count(BusinessGameStats.id)).scalar()
    print(f"📈 Stats Records: {total_stats}")
    
    # Transactions
    total_transactions = session.query(func.count(BusinessGameTransaction.id)).scalar()
    print(f"💰 Transactions: {total_transactions}")
    
    # Top users by XP
    print(f"\n🏆 Top 5 Users by XP:")
    top_users = session.query(User).order_by(User.xp.desc()).limit(5).all()
    for idx, user in enumerate(top_users, 1):
        print(f"   {idx}. {user.username:<15} XP: {user.xp:>6}  Coins: {user.degencoins:>8}")
    
    # Business games by scenario
    print(f"\n🎮 Business Games by Scenario:")
    games_by_scenario = session.query(
        BusinessGame.scenario_type,
        func.count(BusinessGame.id)
    ).group_by(BusinessGame.scenario_type).all()
    
    for scenario, count in games_by_scenario:
        print(f"   - {scenario}: {count}")

print("\n" + "="*80)
print("✅ MIGRATION COMPLETE - ALL DATA IN SQL")
print("="*80)
