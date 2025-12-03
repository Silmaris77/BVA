"""
Migration: Add permissions fields to User table
Adds: company, permissions, account_created_by columns
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from database.connection import get_engine, session_scope
from database.models import Base, User


def run_migration():
    """Add permissions-related columns to users table"""
    
    engine = get_engine()
    
    print("🔧 Migration: Adding permissions fields to User table")
    print("=" * 60)
    
    # Check if columns already exist
    with engine.connect() as conn:
        # Get existing columns
        result = conn.execute(text("PRAGMA table_info(users)"))
        existing_columns = {row[1] for row in result}
        
        print(f"✓ Existing columns: {existing_columns}")
        
        # Add company column
        if 'company' not in existing_columns:
            print("  Adding column: company (String)")
            conn.execute(text("ALTER TABLE users ADD COLUMN company VARCHAR(100)"))
            conn.commit()
            print("  ✓ Column 'company' added")
        else:
            print("  ⊙ Column 'company' already exists")
        
        # Add permissions column (JSON)
        if 'permissions' not in existing_columns:
            print("  Adding column: permissions (JSON)")
            conn.execute(text("ALTER TABLE users ADD COLUMN permissions TEXT"))
            conn.commit()
            print("  ✓ Column 'permissions' added")
        else:
            print("  ⊙ Column 'permissions' already exists")
        
        # Add account_created_by column
        if 'account_created_by' not in existing_columns:
            print("  Adding column: account_created_by (String)")
            conn.execute(text("ALTER TABLE users ADD COLUMN account_created_by VARCHAR(100)"))
            conn.commit()
            print("  ✓ Column 'account_created_by' added")
        else:
            print("  ⊙ Column 'account_created_by' already exists")
    
    print("\n" + "=" * 60)
    print("✅ Migration completed successfully!")
    print("\nNew columns added:")
    print("  - company: VARCHAR(100) - Company name (Warta/Heinz/Milwaukee)")
    print("  - permissions: TEXT (JSON) - Full permissions structure")
    print("  - account_created_by: VARCHAR(100) - Admin who created account")


def verify_migration():
    """Verify the migration was successful"""
    
    engine = get_engine()
    
    print("\n🔍 Verifying migration...")
    print("=" * 60)
    
    with engine.connect() as conn:
        result = conn.execute(text("PRAGMA table_info(users)"))
        columns = [(row[1], row[2]) for row in result]
        
        print("Current users table schema:")
        for col_name, col_type in columns:
            marker = "✓" if col_name in ['company', 'permissions', 'account_created_by'] else " "
            print(f"  {marker} {col_name}: {col_type}")
    
    print("=" * 60)
    print("✅ Verification complete!")


if __name__ == "__main__":
    try:
        run_migration()
        verify_migration()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
