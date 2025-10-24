"""
Quick check what's in the SQL database for business games
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import session_scope
from database.models import BusinessGame, BusinessGameContract, BusinessGameStats, BusinessGameTransaction
from sqlalchemy import func

with session_scope() as session:
    # Count business games
    games_count = session.query(func.count(BusinessGame.id)).scalar()
    print(f"📊 Total Business Games: {games_count}\n")
    
    if games_count > 0:
        # Get first game
        game = session.query(BusinessGame).first()
        
        print(f"🎮 First Game:")
        print(f"   - Scenario: {game.scenario_type}")
        print(f"   - Firm: {game.firm_name}")
        print(f"   - Level: {game.firm_level}")
        print(f"   - Money: {game.money}")
        print(f"   - Reputation: {game.firm_reputation}")
        
        # Count related data
        contracts = session.query(func.count(BusinessGameContract.id)).filter_by(game_id=game.id).scalar()
        stats = session.query(func.count(BusinessGameStats.id)).filter_by(game_id=game.id).scalar()
        transactions = session.query(func.count(BusinessGameTransaction.id)).filter_by(game_id=game.id).scalar()
        
        print(f"\n   📄 Contracts: {contracts}")
        print(f"   📈 Stats: {stats}")
        print(f"   💰 Transactions: {transactions}")
        
        # Show contract breakdown
        active = session.query(func.count(BusinessGameContract.id)).filter_by(game_id=game.id, status='active').scalar()
        completed = session.query(func.count(BusinessGameContract.id)).filter_by(game_id=game.id, status='completed').scalar()
        failed = session.query(func.count(BusinessGameContract.id)).filter_by(game_id=game.id, status='failed').scalar()
        available = session.query(func.count(BusinessGameContract.id)).filter_by(game_id=game.id, status='available').scalar()
        
        print(f"\n   Contract breakdown:")
        print(f"      - Active: {active}")
        print(f"      - Completed: {completed}")
        print(f"      - Failed: {failed}")
        print(f"      - Available: {available}")
