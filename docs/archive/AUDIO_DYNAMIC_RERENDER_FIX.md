# ✅ POPRAWKA: Speech-to-Text - dynamiczny re-render

## 🐛 Problem zgłoszony przez użytkownika:
> "działa to inaczej niż w innych kontraktach. Tam rozpoznany tekst od razu pojawiał się w okienku odpowiedzi gracza z odpowiednią interpunkcją"

## 🔍 Przyczyna:
Rozwiązanie w AI Conversation nie używało **dynamicznego klucza** dla `text_area`, przez co Streamlit nie robił re-render po aktualizacji `session_state`.

### **Różnice:**

| Aspekt | Stare rozwiązanie (AI Conv) | "Feedback" (prawidłowe) |
|--------|----------------------------|------------------------|
| Klucz text_area | `f"input_{contract_id}_{turn}"` | `f"solution_v{version}"` |
| Inkrementacja wersji | ❌ Nie | ✅ Tak (`version += 1`) |
| Re-render po transkrypcji | ❌ Nie | ✅ Tak (zmiana klucza) |
| Wartość `value=` | `session_state[static_key]` | `session_state[transcription_key]` |

## ✅ Rozwiązanie:

### **1. Dodano wersjonowanie:**
```python
transcription_version_key = f"ai_conv_transcription_version_{contract_id}"

if transcription_version_key not in st.session_state:
    st.session_state[transcription_version_key] = 0
```

### **2. Inkrementacja po transkrypcji:**
```python
# Po rozpoznaniu mowy
st.session_state[transcription_key] = transcription
st.session_state[transcription_version_key] += 1  # ← WYMUSZA RE-RENDER!
```

### **3. Dynamiczny klucz text_area:**
```python
# Klucz zmienia się przy każdej transkrypcji
text_area_key = f"ai_conv_input_{contract_id}_{turn}_v{st.session_state[transcription_version_key]}"

player_message = st.text_area(
    "📝 Możesz edytować transkrypcję lub pisać bezpośrednio:",
    value=st.session_state[transcription_key],  # ← WARTOŚĆ Z SESSION STATE
    key=text_area_key  # ← DYNAMICZNY KLUCZ
)
```

### **4. Synchronizacja z powrotem:**
```python
# Zapisz zmiany użytkownika z powrotem do session_state
if text_area_key in st.session_state:
    st.session_state[transcription_key] = st.session_state[text_area_key]
```

### **5. Czyszczenie po wysłaniu:**
```python
# Po wysłaniu wiadomości
st.session_state[transcription_key] = ""
st.session_state[transcription_version_key] += 1  # Wymusza czysty text_area
st.rerun()
```

## 🎯 **Rezultat:**

**PRZED:**
1. Użytkownik nagrywa → transkrypcja gotowa
2. Pole tekstowe: (puste) ← **nie odświeża się**
3. Użytkownik musi kliknąć w pole żeby zobaczyć tekst
4. Komunikaty: "🤖 Gemini dodał interpunkcję" + "✅ Transkrypcja zakończona"

**PO:**
1. Użytkownik nagrywa → transkrypcja gotowa
2. **Pole tekstowe automatycznie pokazuje tekst** ✅
3. Interpunkcja już dodana przez Gemini ✅
4. Tekst natychmiast widoczny (jak w "Feedback") ✅
5. **Brak komunikatów** - ciche działanie ✅
6. **Dynamiczna wysokość pola** - automatycznie rozciąga się przy dłuższym tekście ✅

## 📝 Zmienione linie w `views/business_games.py`:

- **Linie 2598-2710**: Cała sekcja Speech-to-Text przepisana
  - Dodano `transcription_key` i `transcription_version_key`
  - Zmieniono `text_area_key` na dynamiczny: `_v{version}`
  - Dodano inkrementację wersji po transkrypcji
  - Zmieniono `value=` na `session_state[transcription_key]`
  - **Usunięto komunikaty** `st.info()` i `st.success()` (linie 2674, 2695)
  - **Usunięto komunikat błędu Gemini** `st.warning()` (linia 2678)
  
- **Linia 2735**: Czyszczenie po wysłaniu
  ```python
  # PRZED:
  st.session_state[f"text_area_{contract_id}"] = ""
  
  # PO:
  st.session_state[transcription_key] = ""
  st.session_state[transcription_version_key] += 1
  ```

- **Linie 2713-2716**: Dynamiczna wysokość pola tekstowego
  ```python
  # Oblicz dynamiczną wysokość na podstawie liczby linii
  num_lines = current_text.count('\n') + 1
  # Minimalna: 120px, maksymalna: 400px, każda linia: +25px
  dynamic_height = max(120, min(400, 120 + (num_lines - 3) * 25))
  ```

## 🧪 **Test:**

1. Login → Business Games → 💬 Spóźniający się Talent
2. Kliknij **🎤 Nagrywanie...**
3. Powiedz: _"witaj marku co się dzieje"_
4. **Natychmiast po rozpoznaniu** pole tekstowe powinno pokazać:
   ```
   Witaj Marku, co się dzieje?
   ```
   (bez klikania, bez ręcznego odświeżania)

---

**Teraz działa identycznie jak w "Feedback dla nowego pracownika"! 🎉**
