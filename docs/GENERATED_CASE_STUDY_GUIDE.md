# Nowy typ ćwiczenia AI: Generated Case Study

## 🎯 Opis funkcjonalności

Nowy typ ćwiczenia `generated_case` automatycznie generuje unikalne case studies z zadaniami dla użytkowników, a następnie ocenia ich odpowiedzi.

## 🚀 Jak używać w lekcjach

### 1. Dodaj do konfiguracji ćwiczenia AI:

```json
{
  "id": "dynamic_case_exercise",
  "title": "Dynamiczne Case Study - C-IQ",
  "description": "AI wygeneruje dla Ciebie unikalny przypadek biznesowy do rozwiązania",
  "type": "ai_exercise",
  "ai_config": {
    "exercise_type": "generated_case",
    "difficulty_level": "medium",
    "generate_new_case": true,
    "max_attempts": 3,
    "feedback_criteria": [
      "Zrozumienie problemu komunikacyjnego",
      "Zastosowanie zasad C-IQ",
      "Praktyczność rozwiązania",
      "Neurobiologiczne uzasadnienie"
    ]
  }
}
```

### 2. Poziomy trudności:

- **"easy"** - Proste konflikty z oczywistymi rozwiązaniami (10-15 min)
- **"medium"** - Przypadki średniej złożoności wymagające analizy (15-20 min)  
- **"hard"** - Złożone scenariusze z wieloma zmiennymi (20-30 min)

### 3. Co generuje AI:

```json
{
  "title": "Nazwa case study",
  "company_context": "Kontekst firmy/działu",
  "situation": "Szczegółowy opis sytuacji",
  "characters": {
    "main_character": {
      "name": "Imię głównej postaci",
      "position": "Stanowisko",
      "challenge": "Główne wyzwanie"
    },
    "other_characters": [...]
  },
  "communication_challenge": "Problem komunikacyjny",
  "c_iq_opportunity": "Możliwości zastosowania C-IQ",
  "task": "Konkretne zadanie dla uczestnika",
  "success_criteria": ["kryterium 1", "kryterium 2"],
  "difficulty": "medium",
  "estimated_time": "15-20 minut"
}
```

### 4. Ocena odpowiedzi zawiera:

- **overall_score** (1-10) - Ogólna ocena
- **case_understanding** (1-10) - Zrozumienie przypadku
- **solution_quality** (1-10) - Jakość rozwiązania
- **c_iq_application** (1-10) - Zastosowanie C-IQ
- **practical_value** (1-10) - Wartość praktyczna
- **feedback** - Szczegółowy feedback
- **strong_points** - Mocne strony odpowiedzi
- **improvement_areas** - Obszary do poprawy
- **c_iq_tips** - Wskazówki dotyczące C-IQ
- **next_steps** - Kolejne kroki rozwoju

## 🔧 Implementacja techniczna

### Metody w AIExerciseEvaluator:

1. **`generate_case_study(lesson_context, difficulty_level)`**
   - Generuje nowy case study
   - Używa AI lub fallback na demo cases
   - Zwraca pełną strukturę case study

2. **`_evaluate_generated_case(config, user_response, context)`**
   - Ocenia odpowiedź na wygenerowany case
   - Wykorzystuje case_data z config['generated_case_data']
   - Zwraca szczegółową ocenę

3. **`_generate_demo_case(difficulty_level)`**
   - Fallback dla przypadków gdy AI nie działa
   - Predefiniowane cases dla każdego poziomu trudności

## 🎲 Przykłady demo cases:

### Easy: "Konflikt o deadline w zespole marketingu"
- Sytuacja: Przesunięty deadline, zestresowany zespół
- Zadanie: Przekazanie trudnej wiadomości z użyciem C-IQ

### Medium: "Kryzys komunikacji po nieudanym projekcie" 
- Sytuacja: Nieudany projekt, wzajemne oskarżenia
- Zadanie: Retrospektywa z zastosowaniem C-IQ

### Hard: "Reorganizacja i opór przed zmianą"
- Sytuacja: Łączenie działów, opory, plotki
- Zadanie: Kompleksowa strategia komunikacyjna

## ✅ Zalety nowego ćwiczenia:

1. **Unikalność** - Każdy użytkownik dostaje inny case
2. **Dostosowanie** - Różne poziomy trudności
3. **Kontekstualność** - Powiązane z treścią lekcji
4. **Szczegółowa ocena** - Wielowymiarowy feedback
5. **Fallback** - Działa nawet gdy AI nie jest dostępne
6. **Realność** - Autentyczne scenariusze biznesowe

## 🔄 Workflow użycia:

1. System generuje case study (AI lub demo)
2. Użytkownik czyta scenariusz i zadanie
3. Użytkownik pisze swoją odpowiedź/rozwiązanie
4. AI ocenia odpowiedź według kryteriów C-IQ
5. Użytkownik otrzymuje szczegółowy feedback
6. Możliwość powtórzenia z nowym case study

Ten typ ćwiczenia idealnie nadaje się do lekcji o Conversational Intelligence, gdzie teoria musi być zastosowana w praktycznych, biznesowych scenariuszach!