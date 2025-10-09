# Reorganizacja sekcji wyników w quizach autodiagnozy

## Problem
W sekcji "🔍 Zobacz swoje poprzednie odpowiedzi" elementy były wyświetlane w nielogicznej kolejności:
1. Szczegóły odpowiedzi (expander "Zobacz szczegóły swoich odpowiedzi")  
2. Spersonalizowane wyniki ("🎯 Twoje spersonalizowane wyniki")

## Rozwiązanie

### Nowa kolejność w sekcji "🔍 Zobacz swoje poprzednie odpowiedzi":
1. **🎯 Twoje spersonalizowane wyniki** *(najpierw)*
2. **Zobacz szczegóły swoich odpowiedzi** *(expander z detalami)*

## Zmiany implementacyjne

### 1. Sekcja dla już ukończonych quizów (linie ~2477-2498)
```python
# Dla quizów autodiagnozy - najpierw spersonalizowane wyniki Conversational Intelligence
if is_self_diagnostic:
    quiz_title_lower = quiz_data.get('title', '').lower()
    conditions = [
        'conversational intelligence' in quiz_title_lower,
        'c-iq' in quiz_title_lower,
        'od słów do zaufania' in quiz_title_lower,
        'jak ważne może być' in quiz_title_lower
    ]
    
    if any(conditions):
        display_self_diagnostic_results(quiz_data, completed_quiz_data['answers'])

# Potem szczegółowe wyniki quizu
display_quiz_results(quiz_data, question_results, total_points, correct_answers, is_self_diagnostic, quiz_type)
```

### 2. Sekcja po pierwszym ukończeniu quizu (linie ~2756-2766)
```python
# Dla quizów autodiagnozy dodaj komunikat o samorefleksji
if is_self_diagnostic:
    st.success("✅ Dziękujemy za szczerą samorefleksję!")
    
    # Najpierw wyświetl spersonalizowane wyniki jeśli dostępne
    if 'results_interpretation' in quiz_data:
        try:
            display_self_diagnostic_results(quiz_data, st.session_state[quiz_id]["answers"])
        except Exception as e:
            st.error(f"Błąd podczas wyświetlania spersonalizowanych wyników: {e}")
```

### 3. Usunięcie duplikacji w display_quiz_results() (linie ~3530-3545)
Usunięto wywołanie `display_self_diagnostic_results()` z funkcji `display_quiz_results()` dla quizów Conversational Intelligence, ponieważ spersonalizowane wyniki są teraz wyświetlane wcześniej.

## Rezultat

### Nowa struktura quizów autodiagnozy:
1. ✅ Ukończyłeś już ten quiz w dniu: [data]
2. ✅ Dziękujemy za szczerą samorefleksję!
3. 🔍 Zobacz swoje poprzednie odpowiedzi:
   - **🎯 Twoje spersonalizowane wyniki** *(od razu widoczne)*
   - **Zobacz szczegóły swoich odpowiedzi** *(expander z detalami)*
4. 🔄 Przystąp do quizu ponownie

## Dotyczy
- Wszystkich quizów autodiagnozy z konfiguracją `results_interpretation`
- Szczególnie quiz "Conversational Intelligence"  
- Zarówno pierwszy raz ukończone jak i wcześniej ukończone quizy

## Pliki zmienione
- `views/lesson.py` - funkcja `display_quiz()` i `display_quiz_results()`

## Data: 2024-12-22