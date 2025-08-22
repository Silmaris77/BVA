# 🔧 INSTRUKCJE TESTOWANIA KART PRAKTYCZNYCH

## 🎯 Cel
Sprawdzić dlaczego karty nie działają w aplikacji głównej, ale działają w demo.

## 📋 Kroki testowania

### Krok 1: Test podstawowy
```bash
streamlit run test_tabs_in_app.py
```
**Oczekiwany rezultat:** Karty powinny działać poprawnie

### Krok 2: Test głównej aplikacji
```bash
streamlit run main.py
```

1. Zaloguj się do aplikacji
2. Przejdź do: **Kurs** → **B1C1L4**: "Emocjonalna zmienność a zmienność rynku"
3. Przejdź przez kroki: **Intro** → **Samorefleksja** → **Materiał**
4. Dotarcie do kroku: **🎯 Ćwiczenia praktyczne**

### Krok 3: Analiza wyników

**Jeśli widzisz debug informacje:**
- ✅ "Witaj w sekcji Ćwiczeń Praktycznych!"
- ✅ "Znaleziono sekcję practical_exercises z kluczami: [...]"
- ✅ "Znaleziono tabs: ['autotest', 'reflection', 'analysis', 'implementation']"
- ✅ "Przygotowano 4 kart: [...]"
- ✅ "Próba użycia st.tabs() z 4 kartami..."
- ✅ "st.tabs() działa poprawnie!"

**I potem widzisz 4 karty:** 🧠 Autotest | 📝 Refleksja | 📊 Analiza | 🎯 Wdrożenie

## 🚨 Możliwe problemy i rozwiązania

### Problem 1: "st.tabs() nie istnieje"
**Rozwiązanie:** Zaktualizuj Streamlit
```bash
pip install streamlit --upgrade
```

### Problem 2: "AttributeError" lub "TypeError"
**Rozwiązanie:** Sprawdź czy używasz fallback (expanders)
- Powinieneś zobaczyć komunikat: "Karty nie są dostępne. Wyświetlam sekcje jako rozwijane panele."

### Problem 3: Nie docierasz do kroku "Ćwiczenia praktyczne"
**Rozwiązanie:** Sprawdź lesson progress
- Upewnij się, że ukończyłeś poprzednie kroki
- Sprawdź session state w debuggerze

### Problem 4: "Lekcja nie zawiera sekcji practical_exercises"
**Rozwiązanie:** Sprawdź plik B1C1L4.json
```bash
# Sprawdź czy plik istnieje i ma poprawną strukturę
cat data/lessons/B1C1L4.json | grep -A 5 "practical_exercises"
```

## 🧪 Debug dodatkowy

Jeśli nadal nie działa, dodaj tymczasowo na początku lesson.py:
```python
st.write("DEBUG: lesson_step =", st.session_state.get('lesson_step', 'brak'))
st.write("DEBUG: lesson_id =", st.session_state.get('current_lesson', 'brak'))
```

## 🎯 Oczekiwany wynik końcowy

Po naprawie powinieneś widzieć:
1. **4 karty działające** w sekcji Ćwiczenia praktyczne
2. **Każda karta zawiera 3 sekcje** z interaktywną zawartością
3. **Formularze działają** - można wpisywać odpowiedzi i je zapisywać
4. **Przełączanie między kartami** działa płynnie
5. **Po ukończeniu** - przyznawane jest 40% XP z lekcji

## 📞 Jeśli nic nie pomaga

Wyślij zrzut ekranu lub tekst błędu z:
1. Wersji Streamlit: `streamlit --version`
2. Komunikatów debug z aplikacji
3. Ewentualnych błędów w konsoli/logach
