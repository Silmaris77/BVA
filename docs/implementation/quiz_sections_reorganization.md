# Reorganizacja sekcji wyników quizów autodiagnozy

## Zmiany wprowadzone

Zreorganizowano sekcje wyświetlania wyników quizów autodiagnozy zgodnie z żądaną kolejnością:

### Nowa kolejność elementów:

1. **✅ Ukończyłeś już ten quiz w dniu: [data]**
2. **✅ Dziękujemy za szczerą samorefleksję!** *(nowe)*
3. **🔍 Zobacz swoje poprzednie odpowiedzi** *(expander z wynikami)*
4. **🔄 Przystąp do quizu ponownie** *(przycisk na końcu)*

## Szczegóły implementacji

### 1. Dodano komunikat po ukończeniu - dla już ukończonych quizów
```python
# Dla quizów autodiagnosy dodaj komunikat o samorefleksji
if is_self_diagnostic:
    st.success("✅ Dziękujemy za szczerą samorefleksję!")
```

### 2. Dodano komunikat po pierwszym ukończeniu quizu
```python
# Dla quizów autodiagnosy dodaj komunikat o samorefleksji  
if is_self_diagnostic:
    st.success("✅ Dziękujemy za szczerą samorefleksję!")
```

### 3. Lepsze oddzielenie przycisk "Przystąp ponownie"
```python
# Przycisk ponownego przystąpienia na końcu
st.markdown("---")
if st.button("🔄 Przystąp do quizu ponownie", key=f"{quiz_id}_restart"):
```

## Lokalizacje zmian

- **Linia ~2473**: Dodano komunikat po wyświetleniu daty ukończenia (dla już ukończonych quizów)
- **Linia ~2756**: Dodano komunikat po pierwszym ukończeniu quizu autodiagnozy  
- **Linia ~2530**: Dodano separację przed przyciskiem ponownego przystąpienia

## Dotyczy funkcji
- `display_quiz()` w `views/lesson.py`

## Typ quizów
- Tylko quizy autodiagnozy (`is_self_diagnostic = True`)
- Nie wpływa na standardowe quizy testowe

## Data: 2024-12-22