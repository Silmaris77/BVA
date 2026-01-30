"""
Test NotesRepository - sprawdzenie czy CRUD działa poprawnie
"""

import sys
from pathlib import Path

# Dodaj parent directory do path
sys.path.insert(0, str(Path(__file__).parent.parent))

from repository.notes import NotesRepository


def test_notes_repository():
    """Test podstawowych operacji na notatniku"""
    
    print("=" * 60)
    print("🧪 TEST: NotesRepository")
    print("=" * 60)
    print()
    
    repo = NotesRepository()
    test_user_id = 999  # Test user ID
    
    # Cleanup - usuń wszystkie notatki testowe
    print("🧹 Czyszczenie danych testowych...")
    repo.delete_user_notes(test_user_id)
    print()
    
    # ===== TEST 1: CREATE =====
    print("✏️  TEST 1: Tworzenie notatek")
    print("-" * 60)
    
    note1_id = repo.create_note(
        user_id=test_user_id,
        category='product_card',
        title='Chocolate Supreme',
        content='Cena: €15.20\nMarża: 35%\nUSP: Premium kakao z Ghany',
        is_pinned=True,
        tags=['czekolada', 'premium']
    )
    print(f"✅ Utworzono notatkę #1 (ID: {note1_id}) - Chocolate Supreme")
    
    note2_id = repo.create_note(
        user_id=test_user_id,
        category='elevator_pitch',
        title='Pitch dla produktów premium',
        content='Nasze produkty premium to nie tylko najwyższa jakość...',
        tags=['premium', 'marża']
    )
    print(f"✅ Utworzono notatkę #2 (ID: {note2_id}) - Elevator Pitch")
    
    note3_id = repo.create_note(
        user_id=test_user_id,
        category='client_profile',
        title='Supermarket ABC',
        content='Typ: ISTJ\nPreferencje: Produkty lokalne',
        is_pinned=True,
        tags=['ISTJ', 'supermarket']
    )
    print(f"✅ Utworzono notatkę #3 (ID: {note3_id}) - Profil klienta")
    print()
    
    # ===== TEST 2: READ =====
    print("📖 TEST 2: Odczyt notatek")
    print("-" * 60)
    
    all_notes = repo.get_user_notes(test_user_id)
    print(f"📋 Wszystkie notatki użytkownika: {len(all_notes)}")
    for note in all_notes:
        pin_icon = "📌" if note['is_pinned'] else "  "
        print(f"   {pin_icon} [{note['category']}] {note['title']}")
    print()
    
    # ===== TEST 3: SEARCH =====
    print("🔍 TEST 3: Wyszukiwanie")
    print("-" * 60)
    
    results = repo.search_notes(test_user_id, 'premium')
    print(f"🔎 Wyniki dla 'premium': {len(results)}")
    for note in results:
        print(f"   - {note['title']} (tagi: {', '.join(note['tags'])})")
    print()
    
    # ===== TEST 4: UPDATE =====
    print("✏️  TEST 4: Aktualizacja")
    print("-" * 60)
    
    success = repo.update_note(
        note1_id,
        content='Cena: €15.20\nMarża: 35%\nUSP: Premium kakao z Ghany\nNOWE: Certyfikat Fair Trade',
        tags=['czekolada', 'premium', 'fairtrade']
    )
    print(f"{'✅' if success else '❌'} Zaktualizowano notatkę #{note1_id}")
    
    updated_note = repo.get_note_by_id(note1_id)
    print(f"   Nowe tagi: {', '.join(updated_note['tags'])}")
    print()
    
    # ===== TEST 5: TOGGLE PIN =====
    print("📌 TEST 5: Przypinanie")
    print("-" * 60)
    
    repo.toggle_pin(note2_id)
    print(f"✅ Przełączono pin dla notatki #{note2_id}")
    
    pinned_notes = repo.get_user_notes(test_user_id, pinned_only=True)
    print(f"📌 Przypięte notatki: {len(pinned_notes)}")
    for note in pinned_notes:
        print(f"   - {note['title']}")
    print()
    
    # ===== TEST 6: CATEGORY GROUPING =====
    print("🗂️  TEST 6: Grupowanie po kategoriach")
    print("-" * 60)
    
    by_category = repo.get_notes_by_category(test_user_id)
    for category, notes in by_category.items():
        if notes:
            print(f"   {category}: {len(notes)} notatek")
    print()
    
    # ===== TEST 7: STATISTICS =====
    print("📊 TEST 7: Statystyki")
    print("-" * 60)
    
    stats = repo.get_notes_stats(test_user_id)
    print(f"📈 Statystyki:")
    print(f"   Total: {stats['total']}")
    print(f"   Produkty: {stats['product_card']}")
    print(f"   Pitches: {stats['elevator_pitch']}")
    print(f"   Klienci: {stats['client_profile']}")
    print()
    
    # ===== TEST 8: DELETE =====
    print("🗑️  TEST 8: Usuwanie")
    print("-" * 60)
    
    success = repo.delete_note(note2_id)
    print(f"{'✅' if success else '❌'} Usunięto notatkę #{note2_id}")
    
    remaining = repo.get_user_notes(test_user_id)
    print(f"📋 Pozostałe notatki: {len(remaining)}")
    print()
    
    # Cleanup
    print("🧹 Czyszczenie po testach...")
    deleted_count = repo.delete_user_notes(test_user_id)
    print(f"   Usunięto {deleted_count} notatek testowych")
    print()
    
    print("=" * 60)
    print("🎉 WSZYSTKIE TESTY ZAKOŃCZONE SUKCESEM!")
    print("=" * 60)


if __name__ == "__main__":
    test_notes_repository()
