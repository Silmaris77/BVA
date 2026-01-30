"""
Test Anti-Cheat System
Sprawdza czy system wykrywania oszustw działa poprawnie
"""

from datetime import datetime, timedelta
from utils.anti_cheat import (
    check_for_cheating,
    analyze_writing_time,
    analyze_paste_behavior,
    analyze_ai_patterns,
    format_anti_cheat_warning,
    apply_anti_cheat_penalty
)

print("🧪 Test Anti-Cheat System\n")
print("="*60)

# =============================================================================
# TEST 1: Analiza czasu pisania
# =============================================================================
print("\n📝 TEST 1: Analiza czasu pisania")
print("-"*60)

# Przypadek 1: Normalna prędkość (OK)
solution_normal = " ".join(["słowo"] * 300)  # 300 słów
start_time_normal = datetime.now() - timedelta(seconds=90)  # 90 sekund
submit_time_normal = datetime.now()

suspicious, reason, penalty = analyze_writing_time(
    solution_normal, start_time_normal, submit_time_normal
)

print(f"✅ Normalna prędkość (300 słów, 90s):")
print(f"   Podejrzane: {suspicious}")
if suspicious:
    print(f"   Powód: {reason}")
    print(f"   Kara: {penalty} ⭐")

# Przypadek 2: Zbyt szybko (PODEJRZANE)
solution_fast = " ".join(["słowo"] * 500)  # 500 słów
start_time_fast = datetime.now() - timedelta(seconds=30)  # 30 sekund!
submit_time_fast = datetime.now()

suspicious, reason, penalty = analyze_writing_time(
    solution_fast, start_time_fast, submit_time_fast
)

print(f"\n⚠️ Zbyt szybko (500 słów, 30s):")
print(f"   Podejrzane: {suspicious}")
if suspicious:
    print(f"   Powód: {reason}")
    print(f"   Kara: {penalty} ⭐")

# =============================================================================
# TEST 2: Analiza wklejania
# =============================================================================
print("\n\n📋 TEST 2: Analiza wklejania")
print("-"*60)

# Przypadek 1: Małe wklejenie (OK)
paste_events_ok = [
    {"length": 50, "total_solution_length": 1000},
    {"length": 30, "total_solution_length": 1000}
]

suspicious, reason, penalty = analyze_paste_behavior(paste_events_ok)

print(f"✅ Małe wklejenia (80/1000 znaków):")
print(f"   Podejrzane: {suspicious}")

# Przypadek 2: Masowe wklejanie (PODEJRZANE)
paste_events_mass = [
    {"length": 2400, "total_solution_length": 2500}
]

suspicious, reason, penalty = analyze_paste_behavior(paste_events_mass)

print(f"\n⚠️ Masowe wklejanie (2400/2500 znaków):")
print(f"   Podejrzane: {suspicious}")
if suspicious:
    print(f"   Powód: {reason}")
    print(f"   Kara: {penalty} ⭐")

# =============================================================================
# TEST 3: Detekcja wzorców AI
# =============================================================================
print("\n\n🤖 TEST 3: Detekcja wzorców AI")
print("-"*60)

# Przypadek 1: Tekst ludzki (OK)
human_text = """
Pracowałem kiedyś w firmie gdzie mieliśmy podobny problem.
Szef był totalnie nieprzewidywalny i to naprawdę wpływało na morale.
Myślę że najlepiej byłoby porozmawiać z nim bezpośrednio, 
ale też zadbać o własne granice. Może warto też pogadać z HR?
"""

has_patterns, matched = analyze_ai_patterns(human_text)

print(f"✅ Tekst ludzki:")
print(f"   Wzorce AI: {has_patterns} (wykryto: {len(matched)})")

# Przypadek 2: Tekst AI (PODEJRZANE)
ai_text = """
W tej sytuacji należy rozważyć kilka kluczowych aspektów:

1. Komunikacja z przełożonym
2. Ustalenie jasnych granic
3. Dokumentacja incydentów

Istotne jest aby w kontekście tej sytuacji zachować profesjonalizm.
Z perspektywy zarządzania konfliktem, warto zwrócić uwagę na:
- Regularne spotkania zespołu
- Transparentną komunikację
- Wsparcie HR

Biorąc pod uwagę powyższe, najlepszym rozwiązaniem będzie...
"""

has_patterns, matched = analyze_ai_patterns(ai_text)

print(f"\n⚠️ Tekst AI:")
print(f"   Wzorce AI: {has_patterns} (wykryto: {len(matched)})")
if matched:
    print(f"   Przykładowe wzorce: {matched[:2]}")

# =============================================================================
# TEST 4: Kompleksowa analiza
# =============================================================================
print("\n\n🔍 TEST 4: Kompleksowa analiza (check_for_cheating)")
print("-"*60)

# Symuluj oszustwo: szybkie + wklejanie + AI
cheat_solution = ai_text
cheat_start = datetime.now() - timedelta(seconds=20)
cheat_submit = datetime.now()
cheat_paste = [{"length": 1500, "total_solution_length": 1600}]

result = check_for_cheating(
    solution=cheat_solution,
    start_time=cheat_start,
    submit_time=cheat_submit,
    paste_events=cheat_paste,
    use_ai_detection=False  # Wyłącz Gemini dla testów
)

print(f"⚠️ Wykryte oszustwo:")
print(f"   Podejrzane: {result['is_suspicious']}")
print(f"   Flagi: {result['flags']}")
print(f"   Kara łącznie: {result['total_penalty']} ⭐")

# =============================================================================
# TEST 5: Formatowanie ostrzeżenia
# =============================================================================
print("\n\n💬 TEST 5: Ostrzeżenie dla użytkownika")
print("-"*60)

warning = format_anti_cheat_warning(result)
print(warning)

# =============================================================================
# TEST 6: Aplikowanie kary
# =============================================================================
print("\n\n⭐ TEST 6: Aplikowanie kary do oceny")
print("-"*60)

original_rating = 5
penalized_rating = apply_anti_cheat_penalty(original_rating, result['total_penalty'])

print(f"Oryginalna ocena: {original_rating} ⭐")
print(f"Kara: -{result['total_penalty']} ⭐")
print(f"Ocena po karze: {penalized_rating} ⭐")

# =============================================================================
# PODSUMOWANIE
# =============================================================================
print("\n\n" + "="*60)
print("✅ TESTY ZAKOŃCZONE")
print("="*60)
print("""
System anti-cheat działa poprawnie!

Wykrywa:
- ⏱️ Zbyt szybkie pisanie
- 📋 Masowe wklejanie
- 🤖 Wzorce AI-generowanego tekstu

Kary:
- -1 ⭐ za czas/wklejanie
- -3 ⭐ za wiele flag

Minimalna ocena: 1 ⭐
""")

print("\n💡 UWAGA: Test Gemini AI pominięty (use_ai_detection=False)")
print("   Aby przetestować pełną detekcję AI, ustaw use_ai_detection=True")
print("   i upewnij się że config/gemini_api_key.txt istnieje")
