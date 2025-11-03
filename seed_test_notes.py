"""
Seed test notes - dodaje przykładowe notatki do bazy
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from repository.notes import NotesRepository


def seed_test_notes():
    """Dodaje przykładowe notatki dla user_id=1"""
    
    repo = NotesRepository()
    user_id = 1
    
    print("🌱 Seedowanie przykładowych notatek...")
    print()
    
    # Cleanup - usuń stare notatki testowe
    repo.delete_user_notes(user_id)
    
    # === PRODUKTY ===
    repo.create_note(
        user_id=user_id,
        category='product_card',
        title='Chocolate Supreme',
        content='''Cena hurtowa: €15.20 (sugerowana detaliczna: €17.99)
Marża dla detalu: 35%
USP: Premium kakao z Ghany, certyfikat Fair Trade
Konkurencja: Tańszy o €2 od Brand X, lepsza jakość
Dostępność: Stały stan magazynowy''',
        is_pinned=True,
        tags=['czekolada', 'premium', 'fairtrade']
    )
    print("✅ Dodano: Chocolate Supreme (produkt)")
    
    repo.create_note(
        user_id=user_id,
        category='product_card',
        title='Coffee Delight Premium',
        content='''Cena: €12.50
Marża: 30%
USP: 100% arabica, opakowanie ECO
Konkurencja: Podobna cena jak Brand Y, lepsze opakowanie
Nowość: Właśnie wprowadziliśmy do oferty''',
        tags=['kawa', 'premium', 'eco']
    )
    print("✅ Dodano: Coffee Delight Premium (produkt)")
    
    # === ELEVATOR PITCHES ===
    repo.create_note(
        user_id=user_id,
        category='elevator_pitch',
        title='Pitch dla produktów premium',
        content='''Nasze produkty premium to nie tylko najwyższa jakość składników, ale przede wszystkim marża 30-35% i lojalność klientów. 

W podobnych sklepach sprzedaż wzrosła o 40% po wprowadzeniu naszej linii premium. 

Dlaczego? Bo klienci szukają nie tylko ceny, ale też doświadczenia i wartości. Nasze produkty dają im to wszystko.''',
        is_pinned=True,
        tags=['premium', 'marża', 'wartość']
    )
    print("✅ Dodano: Pitch dla produktów premium")
    
    repo.create_note(
        user_id=user_id,
        category='elevator_pitch',
        title='Opening dla nowych klientów',
        content='''Dzień dobry! Wiem, że Państwa czas jest cenny, więc od razu przejdę do sedna.

Współpracujemy z 200+ sklepami w regionie i mamy produkty, które zwiększają marżę o średnio 25% przy zachowaniu konkurencyjnych cen.

Co by Pan powiedział na 15 minut rozmowy o tym, jak możemy pomóc zwiększyć Pana sprzedaż w kategorii [kategoria]?''',
        tags=['opening', 'nowi klienci', 'cold call']
    )
    print("✅ Dodano: Opening dla nowych klientów")
    
    # === PROFILE KLIENTÓW ===
    repo.create_note(
        user_id=user_id,
        category='client_profile',
        title='Supermarket ABC - Pan Kowalski',
        content='''Typ osobowości: ISTJ (faktyczny, systematyczny)
Preferencje: Produkty lokalne, certyfikaty BIO
Pain points: Ostatnio problemy z dostawami od poprzedniego dostawcy
Historia: Zamówił 3x produkty premium w Q3 2025
Relacja: 65% - dobra, ale ostrożny w decyzjach
Best practice: Zawsze podawać konkretne liczby i fakty''',
        is_pinned=True,
        tags=['supermarket', 'ISTJ', 'lojalny']
    )
    print("✅ Dodano: Profil Supermarket ABC")
    
    repo.create_note(
        user_id=user_id,
        category='client_profile',
        title='Sklep Osiedlowy XYZ - Pani Nowak',
        content='''Typ osobowości: ESFP (towarzyski, spontaniczny)
Preferencje: Nowości, produkty sezonowe
Pain points: Trudności z rotacją produktów premium
Historia: Nowy klient, 2 zamówienia testowe
Relacja: 50% - budujemy zaufanie
Best practice: Pokazać benefity wizualnie, być energicznym''',
        tags=['sklep osiedlowy', 'ESFP', 'nowy']
    )
    print("✅ Dodano: Profil Sklep Osiedlowy XYZ")
    
    # === WSKAZÓWKI MENTORA ===
    repo.create_note(
        user_id=user_id,
        category='mentor_tip',
        title='Technika dla klientów ISTJ',
        content='''Klienci typu ISTJ cenią sobie fakty i konkretne liczby. 

✅ RÓB:
- Podawaj dokładne daty dostaw
- Używaj porównań z konkurencją (liczby!)
- Pokazuj case studies z innymi klientami
- Mów o gwarancjach i procedurach

❌ UNIKAJ:
- Ogólników typu "świetna jakość"
- Presji czasowej
- Zmian w ustaleniach

Przykład dobrej frazy: "Nasza marża to 35%, czyli o 5 punktów procentowych więcej niż przy Brand X"''',
        tags=['ISTJ', 'technika', 'empatia']
    )
    print("✅ Dodano: Technika dla klientów ISTJ")
    
    # === FEEDBACK MENEDŻERA ===
    repo.create_note(
        user_id=user_id,
        category='manager_feedback',
        title='Feedback po Turze 3 - Supermarket ABC',
        content='''✅ Co poszło dobrze:
- Świetne otwarcie rozmowy (+15% Relacja)
- Dobra znajomość produktu
- Profesjonalne zachowanie

⚠️ Do poprawy:
- Za szybko przeszedłeś do ceny - najpierw buduj wartość
- Nie zapytałeś o problemy klienta przed propozycją
- Brak follow-up po prezentacji

💡 Na następny raz:
Zastosuj technikę SPIN: Situation → Problem → Implication → Need-Payoff
Najpierw pytaj, potem proponuj rozwiązania.''',
        tags=['feedback', 'asertywność', 'do-poprawy']
    )
    print("✅ Dodano: Feedback po Turze 3")
    
    # === NOTATKI WŁASNE ===
    repo.create_note(
        user_id=user_id,
        category='personal',
        title='Strategia na Q4 2025',
        content='''Cel: +20% sprzedaży vs Q3

Plan działania:
1. Focus na klientów premium (wyższa marża)
2. Budować relacje z 5 kluczowymi klientami
3. Testować nowe produkty sezonowe (świąteczne)
4. Miesięczne follow-upy z top 10 klientami

KPI do śledzenia:
- Liczba wizyt/tydzień: min. 15
- Conversion rate: target 60%
- Średnia wartość zamówienia: €500+

Deadline: 31.12.2025''',
        tags=['strategia', 'Q4', 'cele']
    )
    print("✅ Dodano: Strategia na Q4 2025")
    
    print()
    print("=" * 60)
    print("🎉 Seedowanie zakończone!")
    print()
    
    # Statystyki
    stats = repo.get_notes_stats(user_id)
    print(f"📊 Dodano {stats['total']} notatek:")
    print(f"   📦 Produkty: {stats['product_card']}")
    print(f"   🎯 Pitches: {stats['elevator_pitch']}")
    print(f"   👤 Klienci: {stats['client_profile']}")
    print(f"   🎓 Mentor: {stats['mentor_tip']}")
    print(f"   📊 Manager: {stats['manager_feedback']}")
    print(f"   ✍️ Osobiste: {stats['personal']}")
    print("=" * 60)


if __name__ == "__main__":
    seed_test_notes()
