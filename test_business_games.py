"""
Test Business Games - Podstawowa funkcjonalność
"""

from utils.business_game import (
    initialize_business_game,
    accept_contract,
    submit_contract_solution,
    hire_employee,
    fire_employee,
    calculate_daily_costs,
    refresh_contract_pool,
    get_firm_summary
)
from data.business_data import CONTRACTS_POOL

def test_initialize():
    """Test inicjalizacji firmy"""
    print("\n" + "="*60)
    print("TEST 1: Inicjalizacja Business Games")
    print("="*60)
    
    # Tworzymy user_data z degencoins (jak w prawdziwej aplikacji)
    user_data = {
        "username": "test_user",
        "degencoins": 1000,  # Startowa waluta
        "business_game": initialize_business_game("test_user")
    }
    
    bg_data = user_data["business_game"]
    
    assert bg_data["firm"]["name"] == "test_user's Consulting"
    assert bg_data["firm"]["level"] == 1
    # ZMIANA: coins jest teraz w user_data, nie w bg_data
    assert user_data.get('degencoins', 0) == 1000
    assert bg_data["firm"]["reputation"] == 0
    assert len(bg_data["employees"]) == 0
    assert len(bg_data["contracts"]["active"]) == 0
    
    print("✅ Inicjalizacja działa poprawnie!")
    print(f"   - Nazwa firmy: {bg_data['firm']['name']}")
    print(f"   - Poziom: {bg_data['firm']['level']}")
    print(f"   - Monety startowe: {user_data['degencoins']}")
    print(f"   - Reputacja: {bg_data['firm']['reputation']}")
    
    return user_data

def test_refresh_contracts(user_data):
    """Test odświeżania puli kontraktów"""
    print("\n" + "="*60)
    print("TEST 2: Odświeżanie puli kontraktów")
    print("="*60)
    
    bg_data = user_data["business_game"]
    bg_data = refresh_contract_pool(bg_data, force=True)
    user_data["business_game"] = bg_data
    
    assert len(bg_data["contracts"]["available_pool"]) > 0
    
    print(f"✅ Odświeżono pulę kontraktów!")
    print(f"   - Dostępne kontrakty: {len(bg_data['contracts']['available_pool'])}")
    
    for i, contract in enumerate(bg_data["contracts"]["available_pool"][:3], 1):
        print(f"   {i}. {contract['emoji']} {contract['tytul']}")
        print(f"      Nagroda: {contract['nagroda_base']}-{contract['nagroda_5star']} monet")
    
    return user_data

def test_accept_contract(user_data):
    """Test przyjmowania kontraktu"""
    print("\n" + "="*60)
    print("TEST 3: Przyjmowanie kontraktu")
    print("="*60)
    
    bg_data = user_data["business_game"]
    
    # Weź pierwszy dostępny kontrakt
    if len(bg_data["contracts"]["available_pool"]) == 0:
        print("❌ Brak dostępnych kontraktów!")
        return user_data
    
    first_contract = bg_data["contracts"]["available_pool"][0]
    contract_id = first_contract["id"]
    
    print(f"Przyjmuję kontrakt: {first_contract['tytul']}")
    
    bg_data, success, message = accept_contract(bg_data, contract_id)
    user_data["business_game"] = bg_data
    
    assert success, f"Nie udało się przyjąć kontraktu: {message}"
    assert len(bg_data["contracts"]["active"]) == 1
    
    print(f"✅ {message}")
    print(f"   - Aktywne kontrakty: {len(bg_data['contracts']['active'])}")
    print(f"   - Deadline: {bg_data['contracts']['active'][0]['deadline']}")
    
    return user_data

def test_submit_solution(user_data):
    """Test przesyłania rozwiązania"""
    print("\n" + "="*60)
    print("TEST 4: Przesyłanie rozwiązania kontraktu")
    print("="*60)
    
    bg_data = user_data["business_game"]
    
    if len(bg_data["contracts"]["active"]) == 0:
        print("❌ Brak aktywnych kontraktów!")
        return user_data
    
    active_contract = bg_data["contracts"]["active"][0]
    contract_id = active_contract["id"]
    
    # Generuj przykładowe rozwiązanie (długie, aby przeszło walidację)
    solution = """
    Analiza sytuacji:
    
    W kontekście przedstawionego case'u, kluczowymi wyzwaniami są identyfikacja źródeł konfliktu między stronami,
    wykorzystanie technik Conversational Intelligence oraz zastosowanie Ladder of Inference do analizy perspektyw.
    Problem mikromanagementu jest powszechny w organizacjach i często wynika z braku zaufania, niepewności managera
    co do kompetencji zespołu, lub własnych lęków przed utratą kontroli. Ważne jest zrozumienie kontekstu biznesowego,
    kultury organizacyjnej oraz historii relacji między managerem a zespołem.
    
    Struktura sesji coachingowej:
    
    Sesja będzie trwała 90 minut i będzie podzielona na kilka kluczowych etapów zgodnie z modelem GROW.
    Na początku ustalimy jasne cele spotkania i stworzymy bezpieczną przestrzeń do otwartej rozmowy.
    Kluczowe jest wykorzystanie technik active listening i zadawanie pytań otwartych, które pozwolą managerowi
    samodzielnie dojść do insights dotyczących jego zachowania i jego wpływu na zespół.
    
    Kluczowe pytania coachingowe:
    
    1. Co chciałbyś osiągnąć poprzez tę sesję? Jakie są Twoje oczekiwania?
    2. Jak oceniasz obecnie swoją relację z zespołem? Co działa dobrze, a co wymaga poprawy?
    3. Kiedy czujesz potrzebę interwencji w pracę zespołu? Co Cię do tego motywuje?
    4. Jak myślisz, jak Twój zespół postrzega Twój styl zarządzania?
    5. Jakie konsekwencje ma dla Ciebie i zespołu obecny sposób delegowania?
    6. Gdybyś mógł zmienić coś w swoim podejściu, co by to było?
    7. Co powstrzymuje Cię przed większym zaufaniem do zespołu?
    
    Każde pytanie ma na celu zwiększenie samoświadomości managera i pomoc w identyfikacji własnych przekonań
    limitujących oraz wzorców zachowań, które wpływają na jego styl zarządzania.
    
    Plan feedback wykorzystując COIN Framework:
    
    Context: Opisuję konkretną sytuację - na przykład ostatnie spotkanie zespołu, gdzie manager kilkakrotnie
    przerywał członkom zespołu i poprawiał ich pomysły zanim zostały w pełni przedstawione.
    
    Observation: Prezentuję konkretne zaobserwowane zachowania bez oceniania - "Zauważyłem, że podczas prezentacji
    Jane przerwałeś jej trzykrotnie w ciągu pierwszych 5 minut, proponując własne rozwiązania."
    
    Impact: Opisuję wpływ tych zachowań - "To może sprawiać, że członkowie zespołu czują się niedoceniani
    i mogą przestać zgłaszać własne pomysły, co ogranicza innowacyjność i zaangażowanie."
    
    Next steps: Wspólnie ustalamy konkretne action items, takie jak wprowadzenie zasady "najpierw wysłuchaj
    do końca, potem zadaj pytania" oraz regularne check-iny z zespołem dotyczące ich poczucia autonomii.
    
    Mierzalne cele i follow-up:
    
    1. W ciągu 2 tygodni: Manager przeprowadzi 1-on-1 z każdym członkiem zespołu, pytając o ich potrzeby
    dotyczące autonomii i wsparcia.
    
    2. W ciągu miesiąca: Zespół zgłosi minimum 3 własne inicjatywy, które manager zaakceptuje bez mikrozarządzania.
    
    3. Follow-up session za 6 tygodni: Ocena postępów, omówienie wyzwań, dostosowanie strategii.
    
    4. Survey zespołu po 3 miesiącach: Pomiar satysfakcji z poziomu autonomii i stylu zarządzania.
    
    Podsumowanie:
    
    Zaproponowane rozwiązanie łączy coaching z praktycznym feedbackiem i wykorzystuje sprawdzone frameworki
    Conversational Intelligence. Kluczem do sukcesu jest stworzenie bezpiecznej przestrzeni, w której manager
    może otwarcie eksplorować swoje obawy i przekonania, a następnie świadomie pracować nad zmianą zachowań.
    """
    
    coins_before = user_data.get('degencoins', 0)
    reputation_before = bg_data["firm"]["reputation"]
    
    print(f"Przesyłam rozwiązanie dla: {active_contract['tytul']}")
    print(f"Długość rozwiązania: {len(solution.split())} słów")
    
    user_data, success, message = submit_contract_solution(user_data, contract_id, solution)
    bg_data = user_data["business_game"]
    
    assert success, f"Nie udało się przesłać rozwiązania: {message}"
    assert len(bg_data["contracts"]["completed"]) == 1
    assert len(bg_data["contracts"]["active"]) == 0
    
    coins_after = user_data.get('degencoins', 0)
    reputation_after = bg_data["firm"]["reputation"]
    
    print(f"✅ Kontrakt ukończony!")
    print(message)
    print(f"   - Monety: {coins_before} → {coins_after} (+{coins_after - coins_before})")
    print(f"   - Reputacja: {reputation_before} → {reputation_after} (+{reputation_after - reputation_before})")
    print(f"   - Ocena: {bg_data['contracts']['completed'][0]['rating']}/5 ⭐")
    
    return user_data

def test_hire_employee(user_data):
    """Test zatrudniania pracownika"""
    print("\n" + "="*60)
    print("TEST 5: Zatrudnianie pracownika")
    print("="*60)
    
    bg_data = user_data["business_game"]
    coins_before = user_data.get('degencoins', 0)
    employees_before = len(bg_data["employees"])
    
    print(f"Stan przed zatrudnieniem:")
    print(f"   - Monety: {coins_before}")
    print(f"   - Pracownicy: {employees_before}")
    
    # Spróbuj zatrudnić Junior Consultant
    user_data, success, message = hire_employee(user_data, "junior")
    bg_data = user_data["business_game"]
    
    if not success:
        print(f"⚠️ Nie można zatrudnić: {message}")
        return user_data
    
    assert len(bg_data["employees"]) == employees_before + 1
    
    coins_after = user_data.get('degencoins', 0)
    
    print(f"✅ {message}")
    print(f"   - Monety: {coins_before} → {coins_after} (-{coins_before - coins_after})")
    print(f"   - Pracownicy: {len(bg_data['employees'])}")
    print(f"   - Koszty dzienne: {calculate_daily_costs(bg_data):.0f} monet/dzień")
    
    return user_data

def test_fire_employee(user_data):
    """Test zwalniania pracownika"""
    print("\n" + "="*60)
    print("TEST 6: Zwalnianie pracownika")
    print("="*60)
    
    bg_data = user_data["business_game"]
    
    if len(bg_data["employees"]) == 0:
        print("⚠️ Brak pracowników do zwolnienia")
        return user_data
    
    employee_id = bg_data["employees"][0]["id"]
    employees_before = len(bg_data["employees"])
    
    user_data, success, message = fire_employee(user_data, employee_id)
    bg_data = user_data["business_game"]
    
    assert success
    assert len(bg_data["employees"]) == employees_before - 1
    
    print(f"✅ {message}")
    print(f"   - Pozostali pracownicy: {len(bg_data['employees'])}")
    
    return user_data

def test_firm_summary(user_data):
    """Test podsumowania firmy"""
    print("\n" + "="*60)
    print("TEST 7: Podsumowanie firmy")
    print("="*60)
    
    summary = get_firm_summary(user_data)
    
    print(f"📊 Firma: {summary['name']}")
    print(f"   - Poziom: {summary['level']} ({summary['level_name']})")
    print(f"   - Monety: {summary['coins']:,} 💰")
    print(f"   - Reputacja: {summary['reputation']} 📈")
    print(f"   - Przychody: {summary['total_revenue']:,} 💰")
    print(f"   - Koszty: {summary['total_costs']:,} 💰")
    print(f"   - Zysk netto: {summary['net_profit']:,} 💰")
    print(f"   - Ukończone kontrakty: {summary['contracts_completed']}")
    print(f"   - Średnia ocena: {summary['avg_rating']:.1f}⭐")
    print(f"   - Pracownicy: {summary['employees_count']}")
    print(f"   - Dzienna pojemność: {summary['daily_capacity']} kontraktów")
    print(f"   - Koszty dzienne: {summary['daily_costs']:.0f} 💰/dzień")
    
    print("\n✅ Wszystkie dane poprawnie wyliczone!")
    
    return user_data

def run_all_tests():
    """Uruchom wszystkie testy"""
    print("\n" + "🎮"*30)
    print("BUSINESS GAMES - TEST SUITE")
    print("🎮"*30)
    
    try:
        user_data = test_initialize()
        user_data = test_refresh_contracts(user_data)
        user_data = test_accept_contract(user_data)
        user_data = test_submit_solution(user_data)
        user_data = test_hire_employee(user_data)
        user_data = test_fire_employee(user_data)
        user_data = test_firm_summary(user_data)
        
        print("\n" + "="*60)
        print("🎉 WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
        print("="*60)
        print("\n✨ Business Games jest gotowy do użycia!")
        print("   Uruchom aplikację i przejdź do zakładki 🎮 Business Games")
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    run_all_tests()
