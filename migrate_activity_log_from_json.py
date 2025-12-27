"""
Migracja: Przeniesienie activity_log z JSON do SQL (OPCJONALNE)

Ten skrypt przenosi istniejące wpisy activity_log z pliku users_data.json
do tabeli activity_logs w bazie SQL.

UWAGA: To jest opcjonalne - nowi użytkownicy będą mieli aktywności
automatycznie zapisywane w SQL.
"""

import sys
import os
from datetime import datetime

# Dodaj ścieżkę do folderu głównego
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)

from database.models import ActivityLog, User
from database.connection import session_scope
from data.users import load_user_data
import json

def migrate_activity_log_from_json():
    """Przenieś activity_log z JSON do SQL"""
    
    print("=" * 70)
    print("MIGRACJA: Przenoszenie activity_log z JSON do SQL")
    print("=" * 70)
    print()
    print("⚠️  UWAGA: Ta migracja jest OPCJONALNA")
    print("   Służy do przeniesienia historycznych danych aktywności")
    print("   z pliku users_data.json do bazy SQL.")
    print()
    
    response = input("Czy chcesz kontynuować? (tak/nie): ").strip().lower()
    if response not in ['tak', 't', 'yes', 'y']:
        print("\n❌ Migracja anulowana przez użytkownika")
        return False
    
    print()
    print("📂 Ładowanie danych z users_data.json...")
    
    try:
        users_data = load_user_data()
        print(f"✅ Załadowano dane dla {len(users_data)} użytkowników")
        print()
        
        total_activities = 0
        migrated_users = 0
        skipped_users = 0
        errors = []
        
        with session_scope() as session:
            for username, user_data in users_data.items():
                activity_log = user_data.get('activity_log', [])
                
                if not activity_log:
                    print(f"⏭️  {username}: Brak aktywności do migracji")
                    skipped_users += 1
                    continue
                
                # Znajdź użytkownika w SQL
                user = session.query(User).filter_by(username=username).first()
                
                if not user:
                    print(f"⚠️  {username}: Nie znaleziono w bazie SQL - pomijam")
                    skipped_users += 1
                    continue
                
                print(f"📝 {username}: Migracja {len(activity_log)} aktywności...")
                
                migrated_count = 0
                
                for entry in activity_log:
                    try:
                        # Konwertuj timestamp
                        if isinstance(entry['timestamp'], str):
                            timestamp = datetime.fromisoformat(entry['timestamp'])
                        else:
                            timestamp = entry['timestamp']
                        
                        # Sprawdź czy już nie istnieje (na podstawie user_id, type, timestamp)
                        existing = session.query(ActivityLog)\
                            .filter(ActivityLog.user_id == user.user_id)\
                            .filter(ActivityLog.activity_type == entry['type'])\
                            .filter(ActivityLog.timestamp == timestamp)\
                            .first()
                        
                        if existing:
                            continue  # Pomiń duplikaty
                        
                        # Utwórz nowy wpis
                        activity = ActivityLog(
                            user_id=user.user_id,
                            activity_type=entry['type'],
                            details=entry.get('details', {}),
                            timestamp=timestamp
                        )
                        
                        session.add(activity)
                        migrated_count += 1
                        
                    except Exception as e:
                        error_msg = f"Błąd dla {username}, wpis {entry.get('type', 'unknown')}: {e}"
                        errors.append(error_msg)
                        continue
                
                if migrated_count > 0:
                    session.commit()
                    print(f"✅ {username}: Zmigrowano {migrated_count} aktywności")
                    total_activities += migrated_count
                    migrated_users += 1
                else:
                    print(f"⏭️  {username}: Wszystkie aktywności już istnieją w SQL")
                    skipped_users += 1
        
        print()
        print("=" * 70)
        print("PODSUMOWANIE MIGRACJI")
        print("=" * 70)
        print(f"✅ Użytkowników zmigrowanych: {migrated_users}")
        print(f"⏭️  Użytkowników pominiętych: {skipped_users}")
        print(f"📊 Łącznie aktywności zmigrowanych: {total_activities}")
        
        if errors:
            print()
            print("⚠️  BŁĘDY PODCZAS MIGRACJI:")
            for error in errors[:10]:  # Pokaż pierwsze 10 błędów
                print(f"   - {error}")
            if len(errors) > 10:
                print(f"   ... i {len(errors) - 10} więcej")
        
        print()
        print("=" * 70)
        print("MIGRACJA ZAKOŃCZONA")
        print("=" * 70)
        print()
        print("NASTĘPNE KROKI:")
        print("1. Uruchom aplikację: python -m streamlit run main.py")
        print("2. Sprawdź zakładkę Profil → Historia XP")
        print("3. Powinieneś zobaczyć pełną historię aktywności")
        print()
        
        return True
        
    except Exception as e:
        print(f"\n❌ BŁĄD: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = migrate_activity_log_from_json()
    
    if success:
        print("✅ Dane historyczne zostały przeniesione do SQL")
    else:
        print("❌ Migracja nie powiodła się")
    
    input("\nNaciśnij Enter aby zakończyć...")
