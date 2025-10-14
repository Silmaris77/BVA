# 📊 C-IQ Leadership Profile - Przykładowe Dane

## 🎯 Dodane Funkcjonalności

### 1. **Szczegółowe Przykłady w Placeholderach**
- **Rozmowy z zespołem:** Przykład dialog menedżer-pracownik o problemach projektowych
- **Feedback i oceny:** Przykład konstruktywnej rozmowy feedbackowej
- **Sytuacje konfliktowe:** Przykład rozwiązywania konfliktu w zespole
- **Motywowanie zespołu:** Przykład motywującej rozmowy i rozpoznawania potencjału

### 2. **Automatyczne Wypełnienie**
- Przycisk "🎯 Użyj przykładów" - automatycznie wypełnia wszystkie pola przykładowymi danymi
- Przycisk "🧹 Wyczyść pola" - czyści wszystkie pola do stanu początkowego
- Możliwość szybkiego testowania narzędzia bez potrzeby wpisywania własnych danych

### 3. **Inteligentny System Wskazówek**
- **Dobre przykłady:** Co wpisywać (pełne dialogi, rzeczywiste sytuacje)
- **Czego unikać:** Pojedyncze zdania, ogólne opisy, dane osobowe
- **Minimalne wymagania:** 2 pola, po 3-5 zdań, łącznie ~200 słów

### 4. **System Monitorowania Gotowości**
- **Licznik wypełnionych pól** (X/4)
- **Licznik słów** - pokazuje postęp w czasie rzeczywistym
- **Status gotowości:**
  - ✅ "Gotowe do analizy!" - gdy ≥2 pola i ≥150 słów
  - ⏳ "Potrzeba jeszcze X słów" - gdy za mało tekstu
  - 📝 "Wypełnij więcej pól" - gdy za mało pól

### 5. **Inteligentny Przycisk Analizy**
- Automatycznie wyłącza się gdy dane są niewystarczające
- Zapobiega próbom analizy z za małą ilością danych
- Wizualnie wskazuje kiedy analiza jest możliwa

## 📝 Przykładowe Dane Do Testowania

### 🎯 Rozmowy z zespołem
```
Menedżer: Jak się masz Kasia? Jak idzie projekt z klientem ABC?
Pracownik: Mam problem z terminem, klient ciągle zmienia wymagania
Menedżer: Rozumiem. Co byś potrzebowała żeby wrócić na właściwy tor? Może razem znajdziemy rozwiązanie?
Pracownik: Przydałaby się pomoc Tomka z zespołu technicznego
Menedżer: Świetnie, już go informuję. A może też warto ustalić z klientem jasne ramy zmian?
```

### 📈 Feedback i oceny
```
Menedżer: Tomek, chciałbym porozmawiać o Twoich ostatnich wynikach. Zauważyłem że świetnie radzisz sobie z projektami technicznymi
Pracownik: Dziękuję, staram się
Menedżer: Widzę to! Jednocześnie myślę że mógłbyś więcej komunikować się z zespołem podczas pracy. Co o tym sądzisz?
Pracownik: Masz rację, czasami zapominam informować o postępach
Menedżer: To naturalne. Może spróbujemy codziennych 5-minutowych update'ów? Co byś o tym powiedział?
```

### ⚡ Sytuacje konfliktowe
```
Menedżer: Ania, muszę z Tobą porozmawiać o sytuacji z wczoraj
Pracownik: Wiem, przepraszam za wybuch
Menedżer: Rozumiem że byłaś pod presją. Opowiedz mi co się działo
Pracownik: Klient krzyczy, deadline jest niemożliwy, a jeszcze Marek nie przygotował danych
Menedżer: Brzmi jak doskonała burza. Jak mogę Ci pomóc żeby tak się nie powtórzyło?
Pracownik: Może jakieś lepsze planowanie i wsparcie w kontaktach z trudnymi klientami?
```

### 🚀 Motywowanie zespołu
```
Menedżer: Paweł, chciałem Ci powiedzieć że Twój pomysł na automatyzację był strzałem w dziesiątkę
Pracownik: Dziękuję, ale to nic wielkiego
Menedżer: Żartujesz? Zaoszczędziliśmy 15 godzin tygodniowo! Widzę w Tobie ogromny potencjał na lidera technicznego
Pracownik: Naprawdę tak myślisz?
Menedżer: Absolutnie! Masz naturalne spojrzenie na procesy. Może byś pokierował naszym nowym projektem optymalizacji?
```

## 🎨 Korzyści UX

1. **Intuicyjność:** Użytkownicy widzą dokładnie czego oczekuje narzędzie
2. **Testowanie:** Możliwość szybkiego przetestowania bez własnych danych
3. **Weryfikacja:** System pilnuje jakości danych przed analizą
4. **Motywacja:** Liczniki pokazują postęp i zachęcają do kompletowania danych
5. **Przejrzystość:** Jasne wskazówki eliminują niepewność co do wypełniania

## 🔧 Implementacja Techniczna

- **Streamlit session_state** dla zarządzania stanem przykładowych danych
- **Dynamiczne liczniki** z real-time aktualizacją
- **Walidacja danych** przed wysłaniem do AI
- **Responsywny design** z kolumnami i metrykami
- **Fallback handling** dla różnych stanów aplikacji