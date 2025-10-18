"""Test modułu mi_test"""
from utils.mi_test import calculate_mi_scores, get_mi_test_questions, get_bva_recommendations

# Test 1: Liczba pytań
questions = get_mi_test_questions()
print(f"✅ Test 1: Liczba pytań = {len(questions)} (oczekiwano: 40)")
assert len(questions) == 40, "Powinno być 40 pytań!"

# Test 2: Kalkulacja wyników
# Symuluj odpowiedzi: linguistic=100%, visual=20%, reszta=60%
answers = {}
for i in range(1, 6):
    answers[f'L{i}'] = 5  # Linguistic: 5x5 = 25 (100%)
    answers[f'M{i}'] = 3  # Logical: 5x3 = 15 (60%)
    answers[f'V{i}'] = 1  # Visual: 5x1 = 5 (20%)
    answers[f'U{i}'] = 3  # Musical: 15 (60%)
    answers[f'K{i}'] = 3  # Kinesthetic: 15 (60%)
    answers[f'P{i}'] = 3  # Interpersonal: 15 (60%)
    answers[f'I{i}'] = 3  # Intrapersonal: 15 (60%)
    answers[f'N{i}'] = 3  # Naturalistic: 15 (60%)

result = calculate_mi_scores(answers)

print(f"✅ Test 2: Kalkulacja wyników")
print(f"   Top 3: {result['top_3']}")
print(f"   Bottom 2: {result['bottom_2']}")
print(f"   Balance: {result['balance_score']:.1f}%")

assert result['top_3'][0][0] == 'linguistic', "Linguistic powinno być na 1 miejscu!"
assert result['top_3'][0][1] == 100.0, "Linguistic powinno mieć 100%!"
assert result['bottom_2'][-1][0] == 'visual', "Visual powinno być najniższe!"
assert result['bottom_2'][-1][1] == 20.0, "Visual powinno mieć 20%!"

# Test 3: Rekomendacje
top_intelligences = ['linguistic', 'interpersonal', 'logical']
recs = get_bva_recommendations(top_intelligences)

print(f"✅ Test 3: Rekomendacje BVA")
print(f"   Liczba modułów: {len(recs['modules'])}")
print(f"   Liczba narzędzi: {len(recs['tools'])}")
print(f"   Preferowane formaty: {len(recs['content_types'])}")

assert len(recs['modules']) > 0, "Powinny być rekomendowane moduły!"
assert len(recs['tools']) > 0, "Powinny być rekomendowane narzędzia!"
assert 'text' in recs['content_types'], "Dla linguistic powinien być 'text'!"

print("\n🎉 Wszystkie testy przeszły pomyślnie!")
print("\n📊 Przykładowy profil:")
print(f"   Top 1: {result['top_3'][0][0]} ({result['top_3'][0][1]:.0f}%)")
print(f"   Top 2: {result['top_3'][1][0]} ({result['top_3'][1][1]:.0f}%)")
print(f"   Top 3: {result['top_3'][2][0]} ({result['top_3'][2][1]:.0f}%)")
print(f"\n   Interpretacja: {result['balance_interpretation']}")
