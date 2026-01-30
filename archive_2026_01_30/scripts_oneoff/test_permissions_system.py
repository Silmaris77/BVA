"""
Test script for permissions system
Creates test users for each company and verifies permissions
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from database.models import User
from database.connection import session_scope
from utils.permissions import (
    get_user_permissions, has_access_to_lesson, 
    has_access_to_tool, get_ranking_scope
)
import uuid
from datetime import datetime


def create_test_users():
    """Create test users for each company"""
    
    print("🧪 Creating test users...")
    print("=" * 60)
    
    test_users = [
        {
            'username': 'test_warta',
            'password': 'test123',
            'company': 'Warta'
        },
        {
            'username': 'test_heinz',
            'password': 'test123',
            'company': 'Heinz'
        },
        {
            'username': 'test_milwaukee',
            'password': 'test123',
            'company': 'Milwaukee'
        }
    ]
    
    with session_scope() as session:
        for user_data in test_users:
            # Check if user exists
            existing = session.query(User).filter_by(username=user_data['username']).first()
            if existing:
                print(f"  ⊙ User '{user_data['username']}' already exists - skipping")
                continue
            
            # Create user
            new_user = User(
                user_id=str(uuid.uuid4()),
                username=user_data['username'],
                password_hash=user_data['password'],
                company=user_data['company'],
                permissions=None,  # Will use company template
                account_created_by='test_script',
                xp=0,
                level=1,
                degencoins=0,
                test_taken=False,
                joined_date=datetime.now().date()
            )
            
            session.add(new_user)
            print(f"  ✓ Created user: {user_data['username']} ({user_data['company']})")
        
        session.commit()
    
    print("=" * 60)
    print("✅ Test users created successfully!\n")


def test_permissions():
    """Test permissions for each user"""
    
    print("🔍 Testing permissions...")
    print("=" * 60)
    
    with session_scope() as session:
        test_users = session.query(User).filter(
            User.username.in_(['test_warta', 'test_heinz', 'test_milwaukee'])
        ).all()
        
        for user in test_users:
            user_dict = user.to_dict(include_relations=False)
            
            print(f"\n👤 User: {user.username} (Company: {user.company})")
            print("-" * 60)
            
            # Get permissions
            permissions = get_user_permissions(user_dict)
            
            # Test tools access
            print("  Tools Access:")
            tools = ['dashboard', 'learn', 'business_games', 'shop', 'admin_panel']
            for tool in tools:
                has_access = has_access_to_tool(tool, user_dict)
                status = "✓" if has_access else "✗"
                print(f"    {status} {tool}: {has_access}")
            
            # Test content access
            print("\n  Content Access:")
            lessons = permissions.get('content', {}).get('lessons')
            if lessons:
                print(f"    Lessons: {', '.join(lessons[:3])}... ({len(lessons)} total)")
            else:
                print(f"    Lessons: ALL")
            
            bg_scenarios = permissions.get('content', {}).get('business_games', {}).get('scenarios')
            if bg_scenarios:
                print(f"    BG Scenarios: {', '.join(bg_scenarios[:2])}... ({len(bg_scenarios)} total)")
            else:
                print(f"    BG Scenarios: ALL")
            
            # Test ranking
            print("\n  Ranking:")
            scope = get_ranking_scope(user_dict)
            print(f"    Scope: {scope}")
            
            # Test specific access
            print("\n  Specific Access Tests:")
            print(f"    insurance_basics lesson: {has_access_to_lesson('insurance_basics', user_dict)}")
            print(f"    fmcg_intro lesson: {has_access_to_lesson('fmcg_intro', user_dict)}")
    
    print("\n" + "=" * 60)
    print("✅ Permission tests complete!\n")


def cleanup_test_users():
    """Remove test users"""
    
    response = input("Do you want to cleanup test users? (y/n): ")
    if response.lower() != 'y':
        print("Skipping cleanup.")
        return
    
    print("\n🧹 Cleaning up test users...")
    print("=" * 60)
    
    with session_scope() as session:
        deleted = session.query(User).filter(
            User.username.in_(['test_warta', 'test_heinz', 'test_milwaukee'])
        ).delete()
        
        session.commit()
        print(f"  ✓ Deleted {deleted} test users")
    
    print("=" * 60)
    print("✅ Cleanup complete!\n")


if __name__ == "__main__":
    try:
        create_test_users()
        test_permissions()
        cleanup_test_users()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
