"""
Migracja: Utworzenie tabeli activity_logs w bazie SQL

Ta migracja tworzy nową tabelę activity_logs do przechowywania
aktywności użytkowników (lekcje, narzędzia, quizy itp.)
"""

import sys
import os
from datetime import datetime

# Dodaj ścieżkę do folderu głównego
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)

from database.models import Base, ActivityLog
from database.connection import get_engine, session_scope

def run_migration():
    """Utwórz tabelę activity_logs w bazie danych"""
    
    print("=" * 60)
    print("MIGRACJA: Utworzenie tabeli activity_logs")
    print("=" * 60)
    print()
    
    try:
        # Utwórz tabelę activity_logs (jeśli nie istnieje)
        print("📦 Tworzenie tabeli activity_logs...")
        engine = get_engine()
        Base.metadata.create_all(engine, tables=[ActivityLog.__table__])
        print("✅ Tabela activity_logs utworzona pomyślnie!")
        print()
        
        # Sprawdź czy tabela istnieje
        with session_scope() as session:
            from sqlalchemy import text
            result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='activity_logs'"))
            tables = result.fetchall()
            
            if tables:
                print("✅ Potwierdzenie: Tabela activity_logs istnieje w bazie")
                print()
                
                # Sprawdź strukturę tabeli
                result = session.execute(text("PRAGMA table_info(activity_logs)"))
                columns = result.fetchall()
                
                print("📊 Struktura tabeli activity_logs:")
                print("-" * 60)
                for col in columns:
                    col_id, col_name, col_type, not_null, default, pk = col
                    print(f"  {col_name:20} {col_type:15} {'NOT NULL' if not_null else 'NULL':10} {'PRIMARY KEY' if pk else ''}")
                print()
                
                # Sprawdź indeksy
                result = session.execute(text("PRAGMA index_list(activity_logs)"))
                indexes = result.fetchall()
                
                if indexes:
                    print("🔍 Indeksy:")
                    print("-" * 60)
                    for idx in indexes:
                        idx_seq, idx_name, idx_unique, idx_origin, idx_partial = idx
                        print(f"  {idx_name} {'(UNIQUE)' if idx_unique else ''}")
                    print()
            else:
                print("⚠️  UWAGA: Tabela activity_logs nie została znaleziona!")
                return False
        
        print("=" * 60)
        print("MIGRACJA ZAKOŃCZONA POMYŚLNIE")
        print("=" * 60)
        print()
        print("NASTĘPNE KROKI:")
        print("1. Uruchom aplikację: python -m streamlit run main.py")
        print("2. Zaloguj się i użyj narzędzia lub ukończ lekcję")
        print("3. Sprawdź czy XP się aktualizuje w Dashboard i Profil → Historia XP")
        print()
        print("OPCJONALNIE: Możesz zmigrować stare dane z JSON do SQL")
        print("używając skryptu migrate_activity_log_from_json.py")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ BŁĄD podczas migracji: {e}")
        print()
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_migration()
    
    if success:
        print("✅ Możesz teraz uruchomić aplikację!")
    else:
        print("❌ Migracja nie powiodła się - sprawdź błędy powyżej")
    
    input("\nNaciśnij Enter aby zakończyć...")
