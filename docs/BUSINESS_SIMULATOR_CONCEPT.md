# Business Conversation Simulator - Koncepcja

## Ogólny Pomysł

Interaktywny symulator rozmów biznesowych wykorzystujący AI do odgrywania różnych ról (szef, pracownik, klient, partner). Użytkownik ćwiczy trudne rozmowy menedżerskie otrzymując w czasie rzeczywistym:
- Ocenę poziomu C-IQ (Conversational Intelligence) swoich wypowiedzi
- Dynamiczne odpowiedzi AI dostosowane do stylu komunikacji użytkownika
- Końcowy raport z analizą całej rozmowy

## 8 Scenariuszy Rozmów

### 1. 💰 Rozmowa o podwyżkę
- **Użytkownik:** Pracownik
- **AI:** Wymagający szef
- **Cel:** Negocjować podwyżkę używając argumentów biznesowych i poziomu III C-IQ

### 2. 📢 Feedback dla pracownika  
- **Użytkownik:** Menedżer
- **AI:** Defensywny pracownik
- **Cel:** Przekazać trudny feedback z empatią i konkretnymi przykładami

### 3. ⚡ Rozwiązanie konfliktu
- **Użytkownik:** Mediator
- **AI:** Sfrustrowany członek zespołu
- **Cel:** Mediować w konflikcie używając technik poziomu III

### 4. 📋 Delegowanie zadania
- **Użytkownik:** Menedżer
- **AI:** Przeciążony pracownik
- **Cel:** Delegować zadanie z empatią i wsparciem

### 5. 🔥 Motywowanie zdemotywowanego
- **Użytkownik:** Menedżer
- **AI:** Wypalony pracownik rozważający odejście
- **Cel:** Odnaleźć motywację używając szczerości i konkretnych zmian

### 6. 🔄 Opór wobec zmian
- **Użytkownik:** Lider zmiany
- **AI:** Sceptyczny członek zespołu
- **Cel:** Przekonać do zmiany adresując obawy

### 7. 😤 Rozmowa z trudnym klientem
- **Użytkownik:** Account Manager
- **AI:** Sfrustrowany klient grożący odejściem
- **Cel:** Uspokoić sytuację i odbudować zaufanie
- **Specjalność:** AI zaczyna rozmowę (klient dzwoni zdenerwowany)

### 8. 💼 Negocjacje warunków
- **Użytkownik:** Negocjator
- **AI:** Twardy partner biznesowy
- **Cel:** Osiągnąć porozumienie win-win

## Mechanika Symulatora

### Wybór Scenariusza
- **Selectbox** z 8 scenariuszami
- Wyświetlenie opisu, ról i kontekstu przed startem
- Przycisk "▶️ Rozpocznij symulację"
- **XP Award:** +1 XP za uruchomienie narzędzia

### Dynamiczne Role - Kto Zaczyna?
Każdy scenariusz ma pole `"initiator"`:
- **`"user"`** - Użytkownik zaczyna rozmowę (większość scenariuszy)
- **`"ai"`** - AI zaczyna (np. klient dzwoni zdenerwowany)

### Generowanie Kontekstu
Przed każdą rozmową AI generuje unikalny kontekst:
- Imiona postaci
- Konkretna sytuacja biznesowa
- Szczegóły zwiększające trudność
- Kontekst emocjonalny

**Przykład:** "Jesteś Senior Developer w TechCorp. Pracujesz od 2 lat bez podwyżki, konkurencja oferuje +30%. Niedawno firma miała rundę zwolnień, ale Ty przynosisz kluczowe rezultaty."

### Analiza C-IQ w Czasie Rzeczywistym

Po każdej wypowiedzi użytkownika:

```python
{
    "level": "Transformacyjny/Pozycyjny/Transakcyjny",
    "score": [1-10],
    "reasoning": "Dlaczego ten poziom",
    "tip": "Jak podnieść poziom",
    "is_appropriate": true/false,  # Czy poziom pasuje do kontekstu
    "color": "green/blue/orange/red"  # Wizualizacja
}
```

**Kolory:**
- 🟢 **Zielony:** Poziom III (Transformacyjny) - zawsze dobry
- 🔵 **Niebieski:** Poziom I/II ale odpowiedni w kontekście
- 🟠 **Pomarańczowy:** Poziom II (Pozycyjny) - można lepiej
- 🔴 **Czerwony:** Poziom I (Transakcyjny) - wymaga poprawy

### Dynamiczne Odpowiedzi AI

AI dostosowuje swoje zachowanie do poziomu C-IQ użytkownika:

**Poziom III użytkownika (empatia, pytania otwarte, "my"):**
- AI staje się bardziej otwarty
- Współpracuje w szukaniu rozwiązań
- Obniża defensywność

**Poziom I-II użytkownika (rozkazy, argumenty, "ty"):**
- AI pozostaje defensywny lub oschły
- Kontratakuje lub zamyka się
- Trudniej osiągnąć cel rozmowy

### Licznik Wymian
- **Limit:** 10 wymian (20 wiadomości)
- **Wizualizacja:** 
  - 🟢 0-6 wymian (dużo czasu)
  - 🟡 7-8 wymian (kończy się czas)
  - 🔴 9-10 wymian (ostatnie szanse)

### Zakończenie Rozmowy

**Przycisk "🏁 Zakończ"** w dowolnym momencie lub automatycznie po 10 wymianach.

#### Końcowy Raport AI
```python
{
    "overall_performance": {
        "ciq_average": [1-10],
        "dominant_level": "I/II/III",
        "improvement_trajectory": "improving/stable/declining"
    },
    "key_moments": [
        {
            "turn": 3,
            "highlight": "Świetne pytanie otwarte!",
            "impact": "positive"
        }
    ],
    "strengths": ["Co poszło dobrze"],
    "areas_for_improvement": ["Co można poprawić"],
    "ciq_techniques_used": ["Użyte techniki C-IQ"],
    "outcome_prediction": {
        "goal_achieved": true/false,
        "relationship_impact": "positive/neutral/negative"
    },
    "next_steps": "Rekomendacje dalszego rozwoju"
}
```

**XP Award:** +15 XP za ukończenie symulacji

### Przyciski Po Zakończeniu
- **🎯 Spróbuj innego scenariusza** - reset i wybór nowego
- **❌ Zamknij** - powrót do menu narzędzi

## Techniczne Detale

### Session State
```python
st.session_state.simulator_scenario = None  # ID wybranego scenariusza
st.session_state.simulator_messages = []  # Historia [{role, content, ciq_analysis}]
st.session_state.simulator_started = False
st.session_state.simulator_case_context = None  # Wygenerowany kontekst
st.session_state.simulator_completed = False
st.session_state.simulator_final_report = None
st.session_state.simulator_max_turns = 10
```

### Struktura Scenariusza
```python
{
    "name": "💰 Rozmowa o podwyżkę",
    "description": "Krótki opis",
    "ai_persona": "Szczegółowa persona AI z instrukcjami zachowania",
    "ai_role": "Szef",
    "user_role": "Pracownik",
    "initiator": "user",  # lub "ai"
    "context_prompt": """Prompt dla AI do generowania kontekstu"""
}
```

### Wizualne Elementy Avatarów

Dynamiczne ikony bazujące na rolach:
```python
role_avatars = {
    "Pracownik": "👤",
    "Szef": "💼", 
    "Menedżer": "💼",
    "Mediator": "⚖️",
    "Członek zespołu": "👥",
    "Klient": "😤",
    "Account Manager": "💼",
    "Partner biznesowy": "🤝",
    "Negocjator": "🤝",
    "Lider zmiany": "🔄"
}
```

**Header:** "👤 Ty: **Menedżer** | 🤖 AI: **Pracownik**"

## Poziomy C-IQ - Legenda

Wyświetlana przed rozpoczęciem:

| Poziom | Charakterystyka | Przykład |
|--------|----------------|----------|
| 🔴 **Transakcyjny** | Wymiana informacji, "ty mówisz - ja słucham" | "Chcę podwyżki o 20%" |
| 🟡 **Pozycyjny** | Obrona pozycji, "ja vs ty" | "Zasługuję na więcej, bo inni zarabiają więcej" |
| 🟢 **Transformacyjny** | Współtworzenie, empatia, "my razem" | "Jak możemy wspólnie znaleźć rozwiązanie?" |

## Integracja z Systemem XP

### Punkty Doświadczenia
- **+1 XP** - Uruchomienie symulatora (tool_used)
- **+15 XP** - Ukończenie symulacji (ai_exercise)

### Tracking Aktywności
```python
award_xp_for_activity(
    username,
    'ai_exercise',
    15,
    {
        'exercise_name': 'Business Conversation Simulator',
        'scenario': 'delegation',
        'turns': 8,
        'completed': True
    }
)
```

## Przyszłe Rozszerzenia

### Poziomy Trudności
Dla każdego scenariusza 3 poziomy:
- **Łatwy:** AI bardziej współpracujący, wyraźne wskazówki
- **Średni:** Standardowa trudność
- **Trudny:** AI bardzo defensywny, presja czasowa, dodatkowe komplikacje

### Modyfikatory Trudności
- ⏰ **Presja czasowa:** "Spotkanie za 5 minut"
- 😢 **Emocjonalny kontekst:** "Pracownik płacze"
- 📉 **Poprzednia porażka:** "Ostatnia rozmowa źle się skończyła"
- 💰 **Wysokie stawki:** "Kontrakt wart milion"

### Kategorie Scenariuszy
- 👤 **Rozwój Pracowników:** feedback, delegowanie, motywowanie
- ⚔️ **Konflikty:** mediacja, trudne rozmowy
- 💼 **Negocjacje:** warunki, podwyżka, kontrakty
- 🔄 **Change Management:** opór wobec zmian

### Raport PDF
Eksport końcowego raportu do PDF z:
- Transkrypcją rozmowy
- Analizą C-IQ dla każdej wypowiedzi
- Wykresami progresji
- Szczegółowymi rekomendacjami

## Najczęstsze Błędy (Napotkane)

### KeyError: None
**Przyczyna:** Python niepoprawnie parsuje plik gdy jest uszkodzona struktura (niezamknięte stringi, błędy indentacji)

**Rozwiązanie:** 
- Wydzielić symulator do osobnego pliku `views/business_simulator.py`
- Używać prostych struktur danych zamiast gigantycznych zagnieżdżonych dict
- Testować każdą funkcję osobno

### Traceback wskazuje na linię wewnątrz stringa
**Przyczyna:** Niezamknięty `"""` string literal

**Rozwiązanie:**
- Sprawdzić parzystość `"""` w całym pliku
- Użyć syntax checker: `python -m py_compile file.py`

### AI nie generuje odpowiedzi
**Fallback:** Każda funkcja AI ma prostą heurystyczną wersję gdy API nie działa

## Implementacja - Kroki

1. ✅ **Zdefiniować 8 scenariuszy** z pełnymi personami
2. ✅ **Session state management** dla stanu symulatora
3. ✅ **Selectbox UI** do wyboru scenariusza
4. ✅ **Generowanie kontekstu** przez AI
5. ✅ **Analiza C-IQ w czasie rzeczywistym**
6. ✅ **Dynamiczne odpowiedzi AI** reagujące na poziom użytkownika
7. ✅ **Końcowy raport** z podsumowaniem
8. ✅ **XP integration** - nagrody za aktywność
9. ✅ **Dynamiczne avatary** bazujące na rolach
10. ✅ **Kto zaczyna rozmowę** (user vs AI initiator)

## Status: 🔴 Tymczasowo Wyłączony

Plik źródłowy był uszkodzony (KeyError: None przy parsowaniu).
Kod zostanie przepisany od nowa w osobnym module.
