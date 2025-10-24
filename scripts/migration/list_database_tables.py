"""
Lista wszystkich tabel w bazie danych i ich struktura
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.connection import get_engine
from sqlalchemy import inspect


def list_all_tables():
    """Wyświetla wszystkie tabele i ich kolumny"""
    engine = get_engine()
    inspector = inspect(engine)
    
    print("="*80)
    print("📋 DATABASE TABLES AND STRUCTURE")
    print("="*80)
    
    tables = inspector.get_table_names()
    
    print(f"\n✅ Total tables: {len(tables)}\n")
    
    for table_name in sorted(tables):
        print(f"\n📊 Table: {table_name}")
        print("-" * 80)
        
        columns = inspector.get_columns(table_name)
        
        # Print column details
        for col in columns:
            col_name = col['name']
            col_type = str(col['type'])
            nullable = "NULL" if col['nullable'] else "NOT NULL"
            primary_key = "🔑 PRIMARY KEY" if col.get('primary_key') else ""
            
            print(f"  {col_name:<30} {col_type:<20} {nullable:<10} {primary_key}")
        
        # Print foreign keys
        fks = inspector.get_foreign_keys(table_name)
        if fks:
            print("\n  Foreign Keys:")
            for fk in fks:
                print(f"    - {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")
        
        # Print indexes
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print("\n  Indexes:")
            for idx in indexes:
                cols = ', '.join(idx['column_names'])
                unique = "UNIQUE" if idx['unique'] else ""
                print(f"    - {idx['name']}: ({cols}) {unique}")
    
    print("\n" + "="*80)
    print("✅ DONE")
    print("="*80)


if __name__ == "__main__":
    list_all_tables()
