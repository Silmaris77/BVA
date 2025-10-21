# 🎮 Business Games - Typy Kontraktów - Szczegółowa Specyfikacja

**Data utworzenia:** 21 października 2025  
**Status:** Design Document - Do implementacji Q4 2025

---

## 🎯 Problem do Rozwiązania

**Obecny system kontraktów:**
- Wszystkie kontrakty to "napisz/powiedz rozwiązanie" (Text Contract)
- Monotonność - brak variety w gameplay
- Długi czas wykonania (każdy kontrakt = 5-15 minut pisania)
- Trudność w ocenie jakości (wymaga AI/Mistrz Gry)
- Brak instant gratification

**Cel:**
Wprowadzić 8 różnych typów kontraktów, które:
1. Zwiększą engagement i zabawę
2. Zapewnią różnorodność gameplay
3. Pozwolą na szybsze progresje (quick wins)
4. Zachowają element edukacyjny
5. Umożliwią różne style nauki (visual, interactive, competitive)

---

## 📋 Wszystkie 8 Typów - Overview

| Typ | Trudność Impl. | Priorytet | ETA | Engagement | Edukacja |
|-----|----------------|-----------|-----|------------|----------|
| 1. Text Contract | ✅ Gotowy | - | - | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 2. Quiz Contract | 🟢 Łatwy | #1 | Nov 2025 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 3. Decision Tree | 🟡 Średni | #2 | Dec 2025 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 4. Simulation | 🟡 Średni | #3 | Jan 2026 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 5. Speed Challenge | 🟢 Łatwy | #4 | Jan 2026 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 6. Case Study | 🟢 Łatwy | #5 | Feb 2026 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 7. Collaborative | 🔴 Trudny | #6 | Q3 2026 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 8. Challenge | 🟡 Średni | #7 | Q2 2026 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 1️⃣ Text Contract (Obecny)

### Opis
Klasyczny kontrakt - napisz lub nagraj rozwiązanie problemu klienta.

### Use Case
Głęboka analiza, rozwój umiejętności pisemnej komunikacji, complex problem solving.

### Przykład
```json
{
  "id": "CIQ-TEXT-001",
  "type": "text",
  "title": "Mediacja w konflikcie zespołowym",
  "client": "TechCorp",
  "description": "Zespół projektowy jest podzielony...",
  "task": "Odpowiedz krótko na 3 pytania: ...",
  "min_words": 50,
  "difficulty": 3,
  "reward_base": 650,
  "reward_5star": 1100,
  "time_limit_days": 1
}
```

### Ocena
- Heurystyka (długość tekstu)
- AI (Gemini - merytoryczna ocena)
- Mistrz Gry (ręczna)

### Zalety
✅ Rozwija deep thinking  
✅ Praktyczne umiejętności biznesowe  
✅ Merytoryczna wartość

### Wady
❌ Czasochłonne  
❌ Wymaga motywacji do pisania  
❌ Trudne w ocenie automatycznej

---

## 2️⃣ Quiz Contract 🧠 **[PRIORYTET #1]**

### Opis
Seria 5-10 pytań jednokrotnego lub wielokrotnego wyboru. Instant feedback.

### Use Case
Weryfikacja wiedzy teoretycznej, quick wins, przypomnienie konceptów z lekcji.

### Przykład
```json
{
  "id": "CIQ-QUIZ-001",
  "type": "quiz",
  "title": "Leadership Models - Quick Test",
  "client": "Academy of Management",
  "description": "Przetestuj swoją wiedzę o stylach przywództwa",
  "difficulty": 2,
  "reward_base": 300,
  "reward_5star": 500,
  "time_limit_minutes": 10,
  "questions": [
    {
      "id": "q1",
      "question": "Który styl przywództwa jest najskuteczniejszy w sytuacji kryzysowej?",
      "type": "single_choice",
      "options": [
        "Demokratyczny",
        "Autokratyczny",
        "Laissez-faire",
        "Servant Leadership"
      ],
      "correct": 1,
      "explanation": "W kryzysie potrzebne są szybkie, zdecydowane decyzje, co charakteryzuje styl autokratyczny.",
      "points": 10
    },
    {
      "id": "q2",
      "question": "Jakie cechy charakteryzują Servant Leadership? (zaznacz wszystkie)",
      "type": "multiple_choice",
      "options": [
        "Stawianie potrzeb zespołu na pierwszym miejscu",
        "Centralizacja władzy",
        "Empatia i słuchanie",
        "Mikromanagement"
      ],
      "correct": [0, 2],
      "explanation": "Servant Leadership koncentruje się na wspieraniu i rozwoju zespołu.",
      "points": 15
    },
    {
      "id": "q3",
      "question": "Uzupełnij: Według teorii Herzberga, czynniki ____ zapobiegają niezadowoleniu, ale nie motywują.",
      "type": "fill_blank",
      "correct": "higieniczne",
      "accept_variants": ["higieniczne", "higieny", "hygiene"],
      "points": 10
    }
  ],
  "passing_score": 70,
  "total_points": 100
}
```

### Mechanika
1. Gracz wybiera Quiz Contract z listy
2. Rozpoczyna quiz (full screen mode, distraction-free)
3. Odpowiada na pytania sekwencyjnie
4. Po każdej odpowiedzi → instant feedback (correct/incorrect + explanation)
5. Na końcu: podsumowanie (score, prawidłowe odpowiedzi, czas)
6. Auto-grading:
   - 90-100% → 5 stars
   - 80-89% → 4 stars
   - 70-79% → 3 stars
   - 60-69% → 2 stars
   - <60% → 1 star (fail, repeat możliwy)

### Scoring Algorithm
```python
def grade_quiz_contract(answers, questions):
    total_points = sum(q['points'] for q in questions)
    earned_points = 0
    
    for i, answer in enumerate(answers):
        question = questions[i]
        
        if question['type'] == 'single_choice':
            if answer == question['correct']:
                earned_points += question['points']
        
        elif question['type'] == 'multiple_choice':
            # Partial credit
            correct_set = set(question['correct'])
            answer_set = set(answer)
            
            correct_selected = len(correct_set & answer_set)
            incorrect_selected = len(answer_set - correct_set)
            missed = len(correct_set - answer_set)
            
            # Scoring: +1 za correct, -0.5 za incorrect
            score = max(0, correct_selected - 0.5 * incorrect_selected)
            max_score = len(correct_set)
            earned_points += question['points'] * (score / max_score)
        
        elif question['type'] == 'fill_blank':
            normalized_answer = answer.lower().strip()
            if normalized_answer in [v.lower() for v in question['accept_variants']]:
                earned_points += question['points']
    
    percentage = (earned_points / total_points) * 100
    
    # Convert to stars
    if percentage >= 90:
        stars = 5
    elif percentage >= 80:
        stars = 4
    elif percentage >= 70:
        stars = 3
    elif percentage >= 60:
        stars = 2
    else:
        stars = 1
    
    return {
        'stars': stars,
        'percentage': percentage,
        'earned_points': earned_points,
        'total_points': total_points
    }
```

### UI Mockup
```
┌─────────────────────────────────────────────────┐
│ 🧠 Quiz Contract: Leadership Models             │
│ Klient: Academy of Management                   │
│ Pytanie 3 z 10                       ⏱️ 05:42  │
├─────────────────────────────────────────────────┤
│                                                  │
│ Który styl przywództwa jest najskuteczniejszy  │
│ w sytuacji kryzysowej?                          │
│                                                  │
│ ◯ Demokratyczny                                 │
│ ◉ Autokratyczny                                 │
│ ◯ Laissez-faire                                 │
│ ◯ Servant Leadership                            │
│                                                  │
│          [← Poprzednie]    [Dalej →]           │
└─────────────────────────────────────────────────┘
```

### Nagrody
- **Base reward:** 50-70% wartości Text Contract (szybsze wykonanie)
- **Time bonus:** +10% jeśli ukończono w <50% czasu
- **Perfect score bonus:** +20% za 100%

### Zalety
✅ Instant gratification  
✅ Łatwe w tworzeniu (content)  
✅ Auto-grading (zero manual work)  
✅ Weryfikacja wiedzy  
✅ Quick wins dla graczy

### Wady
❌ Powierzchowna nauka (recognition vs recall)  
❌ Można zgadywać  
❌ Mniej kreatywności

### Implementacja - Tech Stack
- **Frontend:** Streamlit radio/checkbox/text_input
- **Backend:** Python function dla grading
- **Storage:** JSON schema w `CONTRACTS_POOL`
- **Session state:** Przechowuje answers podczas quiz

### Content Creation - Przykład
```python
# Generator quizów z istniejących lekcji
def generate_quiz_from_lesson(lesson_id):
    lesson = get_lesson(lesson_id)
    
    questions = []
    for concept in lesson['key_concepts']:
        question = {
            'question': f"Co to jest {concept['name']}?",
            'type': 'single_choice',
            'options': generate_distractors(concept['definition'], num=3),
            'correct': 0,  # Correct answer first
            'points': 10
        }
        questions.append(question)
    
    return create_quiz_contract(
        title=f"{lesson['title']} - Quiz",
        questions=questions,
        difficulty=lesson['difficulty']
    )
```

---

## 3️⃣ Decision Tree Contract 🌳 **[PRIORYTET #2]**

### Opis
Interaktywna historia - seria decyzji, każda wpływa na następną scenę. Multiple endings.

### Use Case
Practical decision-making, consequence awareness, storytelling, realistic scenarios.

### Przykład
```json
{
  "id": "CIQ-TREE-001",
  "type": "decision_tree",
  "title": "Navigate Difficult Employee Conversation",
  "client": "HR Solutions Inc",
  "description": "Twój najlepszy programista jest stale spóźniony. Musisz przeprowadzić trudną rozmowę.",
  "difficulty": 3,
  "reward_base": 600,
  "reward_5star": 1000,
  "start_node": "scene_1",
  "nodes": {
    "scene_1": {
      "id": "scene_1",
      "title": "🏢 Poniedziałek, 10:30 - Trzecie spóźnienie w tym tygodniu",
      "text": "Mark wchodzi do biura o 10:30. To już trzecie spóźnienie w tym tygodniu. Pozostali członkowie zespołu wymieniają spojrzenia. Daily standup zaczął się bez niego.",
      "image": "office_late.jpg",
      "choices": [
        {
          "text": "Natychmiast wezwij Marka do swojego biura i zgromij go",
          "next": "scene_2a_confrontation",
          "points": -10,
          "feedback": "❌ Emocjonalna reakcja bez poznania kontekstu"
        },
        {
          "text": "Poczekaj na prywatny moment i zapytaj co się dzieje",
          "next": "scene_2b_empathy",
          "points": 15,
          "feedback": "✅ Empatyczne podejście, prywatność"
        },
        {
          "text": "Zignoruj to - Mark jest zbyt wartościowy aby go stracić",
          "next": "scene_2c_ignore",
          "points": -15,
          "feedback": "❌ Unikanie problemu, niesprawiedliwość wobec zespołu"
        },
        {
          "text": "Wyślij mu maila z zasadami firmy dotyczącymi punktualności",
          "next": "scene_2d_passive",
          "points": -5,
          "feedback": "⚠️ Zbyt formalne, brak dialogu"
        }
      ]
    },
    "scene_2b_empathy": {
      "id": "scene_2b_empathy",
      "title": "☕ W kuchni, po spotkaniu",
      "text": "Podchodzisz do Marka w kuchni. 'Hej Mark, zauważyłem że ostatnio kilka razy się spóźniłeś. Wszystko w porządku?' Mark waha się, ale widać że chce porozmawiać.",
      "choices": [
        {
          "text": "'Moja matka jest chora. Muszę ją wozić na terapie rano.'",
          "next": "scene_3b_family",
          "points": 0,
          "is_revelation": true
        }
      ]
    },
    "scene_3b_family": {
      "id": "scene_3b_family",
      "title": "💬 Szczera rozmowa",
      "text": "Mark wyjaśnia: 'Przepraszam, powinienem powiedzieć wcześniej. Moja mama ma chemo każdy poniedziałek i środę rano. Nie mam nikogo kto mógłby ją zawieźć. Próbuję załatwiać to szybko ale...'",
      "choices": [
        {
          "text": "Zaproponuj elastyczne godziny pracy (10:30-18:30 w te dni)",
          "next": "ending_win_win",
          "points": 25,
          "feedback": "✅ Empathy + Solution-oriented"
        },
        {
          "text": "Pozwól na pracę zdalną w te dni",
          "next": "ending_remote",
          "points": 20,
          "feedback": "✅ Flexible, ale może wpłynąć na team dynamics"
        },
        {
          "text": "Zaproponuj pomoc zespołu (car pooling, coverage)",
          "next": "ending_team_help",
          "points": 30,
          "feedback": "🏆 Exceptional - team building + empathy"
        },
        {
          "text": "Powiedz że rozumiesz, ale zasady są zasadami",
          "next": "ending_by_the_book",
          "points": -10,
          "feedback": "❌ Brak elastyczności, stracisz zaufanie"
        }
      ]
    },
    "ending_team_help": {
      "id": "ending_team_help",
      "title": "🎉 BEST ENDING - Team Support",
      "text": "Organizujesz krótkie spotkanie zespołu. Wyjaśniasz sytuację Marka (za jego zgodą). Zespół spontanicznie oferuje pomoc:\n\n• Sarah: 'Mogę go podwozić, mieszkam blisko'\n• Tom: 'W te dni mogę zaczynać wcześniej i pokryć jego standup'\n• Team: Wszyscy doceniają transparentność\n\nMark jest głęboko poruszony. Produktywność zespołu rośnie. Zbudowałeś kulturę wzajemnego wsparcia.",
      "outcome": {
        "reputation": +50,
        "team_morale": +30,
        "mark_loyalty": 100,
        "points": 100
      },
      "is_ending": true
    },
    "ending_win_win": {
      "id": "ending_win_win",
      "title": "✅ GOOD ENDING - Flexible Hours",
      "text": "Ustalasz z Markiem elastyczne godziny. W poniedziałki i środy pracuje 10:30-18:30. W pozostałe dni normalnie.\n\nMark jest wdzięczny i odwzajemnia się zwiększoną produktywnością. Problem rozwiązany, ale zespół nie wie o sytuacji i może mieć poczucie nierówności.",
      "outcome": {
        "reputation": +30,
        "team_morale": -5,
        "mark_loyalty": 80,
        "points": 75
      },
      "is_ending": true
    },
    "scene_2a_confrontation": {
      "id": "scene_2a_confrontation",
      "title": "😠 W biurze managera - Konfrontacja",
      "text": "Wołasz Marka do biura z widoczną irytacją. 'Mark, to już trzeci raz w tym tygodniu. To nieakceptowalne.' Mark się zamyka, krzyżuje ręce.",
      "choices": [
        {
          "text": "Kontynuuj zgromienie - 'Jesteś przykładem dla innych'",
          "next": "ending_resignation",
          "points": -30,
          "feedback": "❌ Critical failure - stracisz Marka"
        },
        {
          "text": "Zatrzymaj się i zmień ton - 'Przepraszam, zacznijmy od nowa'",
          "next": "scene_3a_recovery",
          "points": 5,
          "feedback": "⚠️ Próba naprawy, ale damage already done"
        }
      ]
    },
    "ending_resignation": {
      "id": "ending_resignation",
      "title": "💔 WORST ENDING - Employee Lost",
      "text": "Mark słucha w milczeniu. Po spotkaniu wraca do biurka, pakuje rzeczy i składa wypowiedzenie. Później dowiadujesz się że jego matka była chora na raka. Zespół traci szacunek do Twojego stylu zarządzania.\n\n2 tygodnie później Mark zaczyna pracę u konkurencji.",
      "outcome": {
        "reputation": -50,
        "team_morale": -40,
        "mark_loyalty": 0,
        "employee_lost": true,
        "points": 0
      },
      "is_ending": true
    }
  },
  "scoring": {
    "points_to_stars": {
      "5": 90,
      "4": 70,
      "3": 50,
      "2": 30,
      "1": 0
    }
  }
}
```

### Mechanika
1. Gracz rozpoczyna od `start_node`
2. Czyta scenę (text + optional image)
3. Wybiera jedną z opcji (2-4 choices)
4. System:
   - Dodaje punkty za wybór
   - Pokazuje feedback
   - Przechodzi do `next` node
5. Powtarza aż osiągnie `is_ending: true`
6. Finalne podsumowanie:
   - Suma punktów → stars
   - Outcome metrics (reputation, morale, etc.)
   - Nagroda

### Scoring
```python
def score_decision_tree(path, nodes):
    """
    path: lista wyborów gracza
    nodes: definicja drzewa
    """
    total_points = 0
    outcomes = {}
    
    for choice in path:
        total_points += choice['points']
    
    # Final node zawiera outcome
    final_node = nodes[path[-1]['next']]
    if 'outcome' in final_node:
        outcomes = final_node['outcome']
    
    # Convert points to stars
    stars = points_to_stars(total_points, scoring_table)
    
    return {
        'stars': stars,
        'points': total_points,
        'ending': final_node['title'],
        'outcomes': outcomes
    }
```

### UI Flow
```
[Start] → [Scene 1] → [Choice 1-4] → [Scene 2x] → ... → [Ending]
                ↓ points              ↓ points           ↓ final score
```

### Nagrody
- **Variable:** W zależności od punktów (best ending = 100%, worst = 30%)
- **Replay value:** Można powtórzyć dla innych ścieżek
- **Achievement:** "Saw all endings" bonus

### Zalety
✅ Bardzo engaging (storytelling)  
✅ Pokazuje konsekwencje decyzji  
✅ Replay value (multiple endings)  
✅ Practical scenarios  
✅ Emocjonalny impact

### Wady
❌ Czasochłonne w tworzeniu (writing)  
❌ Ograniczona skalowalność (każdy node = manual work)  
❌ Trudne w balance (punktacja)

### Implementacja
- **Storage:** Nested JSON structure
- **UI:** Streamlit buttons dla choices
- **State:** Session state przechowuje `current_node` + `path`
- **Rendering:** Markdown dla text, optional st.image()

---

## 4️⃣ Simulation Contract 🎯

### Opis
Mini-game symulujący realną sytuację biznesową. Interaktywne widgety (sliders, drag-drop).

### Przykłady

**A) Prioritization Simulator**
```json
{
  "type": "simulation_priority",
  "title": "Task Prioritization Challenge",
  "tasks": [
    {
      "id": "t1",
      "name": "Fix critical bug",
      "urgency": 5,
      "importance": 5,
      "time_hours": 2
    },
    {
      "id": "t2",
      "name": "Strategic planning meeting",
      "urgency": 2,
      "importance": 5,
      "time_hours": 3
    }
    // ... 10 tasks total
  ],
  "constraints": {
    "available_hours": 8,
    "must_complete_today": ["t1", "t5"]
  },
  "scoring": "eisenhower_matrix"
}
```

Gracz:
1. Widzi listę 10 zadań
2. Drag & drop do kolejności wykonania
3. Lub: assigns priority score (1-10) każdemu
4. System ocenia według Eisenhower Matrix:
   - Urgent + Important → top priority
   - Important not urgent → schedule
   - Urgent not important → delegate
   - Neither → eliminate

**B) Budget Allocation**
```json
{
  "type": "simulation_budget",
  "title": "Department Budget Allocation",
  "total_budget": 100000,
  "departments": [
    {"id": "rd", "name": "R&D", "min": 20, "max": 50},
    {"id": "marketing", "name": "Marketing", "min": 10, "max": 40},
    {"id": "sales", "name": "Sales", "min": 15, "max": 45},
    {"id": "ops", "name": "Operations", "min": 10, "max": 30},
    {"id": "hr", "name": "HR", "min": 5, "max": 20}
  ],
  "company_stage": "growth",
  "optimal_allocation": {
    "rd": 35,
    "marketing": 25,
    "sales": 25,
    "ops": 10,
    "hr": 5
  }
}
```

Gracz:
1. Widzi 5 sliderów (jeden per department)
2. Suma musi = 100%
3. Każdy slider ma min/max constraints
4. System porównuje z `optimal_allocation`:
   - Odchylenie 0-5% → perfect
   - 5-10% → good
   - 10-20% → acceptable
   - >20% → poor

### Scoring
```python
def score_budget_simulation(player_allocation, optimal, tolerance=0.05):
    score = 100
    
    for dept, optimal_pct in optimal.items():
        player_pct = player_allocation[dept]
        deviation = abs(player_pct - optimal_pct) / 100
        
        if deviation <= tolerance:
            penalty = 0
        elif deviation <= 0.10:
            penalty = 10
        elif deviation <= 0.20:
            penalty = 25
        else:
            penalty = 40
        
        score -= penalty
    
    return max(0, score)
```

### UI - Streamlit Widgets
```python
st.subheader("💰 Budget Allocation Simulator")
st.write(f"Total Budget: ${total_budget:,}")

allocations = {}
for dept in departments:
    allocations[dept['id']] = st.slider(
        f"{dept['name']} (%)",
        min_value=dept['min'],
        max_value=dept['max'],
        value=20,  # default
        step=1
    )

# Validation
total_allocated = sum(allocations.values())
if total_allocated != 100:
    st.error(f"Total must equal 100%. Currently: {total_allocated}%")
else:
    if st.button("Submit Allocation"):
        score = score_budget_simulation(allocations, optimal)
        st.success(f"Score: {score}/100")
```

### Zalety
✅ Bardzo interaktywne  
✅ Praktyczne umiejętności  
✅ Visual/kinesthetic learners  
✅ Instant feedback

### Wady
❌ Wymaga custom widgets  
❌ Trudne w content creation (definicja optimal)  
❌ Mobile-unfriendly (sliders)

---

## 5️⃣ Speed Challenge Contract ⚡

### Opis
Seria szybkich mikro-zadań pod presją czasu. Accuracy + speed bonus.

### Przykład
```json
{
  "type": "speed_challenge",
  "title": "Leadership Quick Wins - 60 seconds",
  "time_limit_seconds": 60,
  "questions": [
    {
      "type": "quick_choice",
      "question": "Best response to angry customer?",
      "options": ["Apologize", "Explain policy", "Escalate", "Ignore"],
      "correct": 0,
      "time_seconds": 6,
      "points": 10
    },
    {
      "type": "yes_no",
      "question": "Should you micromanage experienced employees?",
      "correct": false,
      "time_seconds": 4,
      "points": 5
    },
    {
      "type": "drag_priority",
      "question": "Order these: A) Email, B) Fire, C) Call, D) Report",
      "correct_order": ["B", "C", "A", "D"],
      "time_seconds": 10,
      "points": 15
    }
  ]
}
```

### Mechanika
1. Countdown timer starts
2. Pytanie pojawia się full screen
3. Gracz odpowiada ASAP
4. Auto-submit jeśli czas up
5. Immediate feedback (green/red flash)
6. Next question
7. Final score: (correct answers × points) × speed_multiplier

### Speed Multiplier
```python
def calculate_speed_bonus(time_used, time_allowed):
    if time_used <= time_allowed * 0.5:
        return 1.5  # 50% bonus
    elif time_used <= time_allowed * 0.75:
        return 1.25  # 25% bonus
    elif time_used <= time_allowed:
        return 1.0  # no bonus
    else:
        return 0.75  # penalty for timeout
```

### UI
```
╔════════════════════════════════════╗
║  ⚡ SPEED CHALLENGE ⚡             ║
║  Question 5/10      ⏱️ 42s left   ║
╠════════════════════════════════════╣
║                                    ║
║  Best response to angry customer?  ║
║                                    ║
║  [  Apologize  ]  [ Explain  ]    ║
║  [ Escalate ]     [  Ignore  ]    ║
║                                    ║
╚════════════════════════════════════╝
```

### Zalety
✅ Adrenaline rush  
✅ Casual gaming vibe  
✅ Quick to complete  
✅ Addictive (one more try)

### Wady
❌ Stresujące dla niektórych  
❌ Faworyzuje szybkość > accuracy  
❌ Może prowadzić do burnout

---

## 6️⃣ Case Study Contract 📚

### Opis
Długi case study (500-1000 słów) → przeczytaj → odpowiedz na mix quiz + short text.

### Struktura
```json
{
  "type": "case_study",
  "title": "Google's 20% Time Policy - Success or Failure?",
  "case_text": "In 2004, Google introduced... [800 words]",
  "estimated_reading_time": 5,
  "questions": [
    {
      "type": "quiz",
      "question": "What was the primary goal of 20% time?",
      "options": ["Innovation", "Retention", "Cost savings", "PR"],
      "correct": 0
    },
    {
      "type": "short_text",
      "question": "Identify 2 pros and 2 cons of this policy (50 words max)",
      "max_words": 50,
      "rubric": {
        "pros": ["innovation", "motivation", "gmail/adsense"],
        "cons": ["productivity loss", "inequality", "abandonment"]
      }
    },
    {
      "type": "text",
      "question": "Would you implement this in your company? Why? (100 words)",
      "max_words": 100
    }
  ]
}
```

### Ocena
- Quiz questions: auto-graded
- Short text: keyword matching (partial)
- Long text: AI evaluation

### Scoring
```python
def score_case_study(answers, questions):
    quiz_score = grade_quiz_questions(answers[:3])
    text_score = grade_text_questions_ai(answers[3:])
    
    final_score = (quiz_score * 0.4) + (text_score * 0.6)
    return final_score
```

### Zalety
✅ Deep learning  
✅ Real-world scenarios  
✅ Analytical thinking  
✅ Balanced assessment

### Wady
❌ Długi czas wykonania  
❌ Wymaga czytania (not everyone's forte)  
❌ Trudne w tworzeniu content

---

## 7️⃣ Collaborative Contract 👥 (Multiplayer)

### Opis
2-4 graczy współpracują aby ukończyć projekt. Group rating + individual contribution.

### Przykład
```json
{
  "type": "collaborative",
  "title": "Workshop Facilitation - Team of 4",
  "min_players": 2,
  "max_players": 4,
  "roles": [
    {
      "id": "facilitator",
      "name": "Facilitator",
      "task": "Prepare workshop agenda (100 words)",
      "deliverable_type": "text",
      "weight": 30
    },
    {
      "id": "icebreaker",
      "name": "Icebreaker Designer",
      "task": "Design opening activity (quiz or decision tree)",
      "deliverable_type": "mini_contract",
      "weight": 20
    },
    {
      "id": "moderator",
      "name": "Q&A Moderator",
      "task": "Handle 5 participant questions (simulation)",
      "deliverable_type": "simulation",
      "weight": 25
    },
    {
      "id": "summarizer",
      "name": "Summarizer",
      "task": "Write workshop summary (50 words)",
      "deliverable_type": "text",
      "weight": 25
    }
  ],
  "team_bonus": 20
}
```

### Flow
1. Contract otwiera się dla aplikacji (jak job posting)
2. Gracze aplikują + wybierają role
3. Matching algorithm łączy team
4. Każdy gracz wykonuje swoją część
5. Team chat/comments dla koordynacji
6. Po wszystkich submission → AI ocenia całość
7. Nagroda dzielona:
   - 80% proporcjonalnie do weight + quality
   - 20% team bonus (równo)

### Matching Algorithm
```python
def match_collaborative_contract(applicants, contract):
    # Factors:
    # - Skill level (podobny = lepszy team)
    # - Time zone (overlap dla koordynacji)
    # - Previous collaboration history
    # - Role preferences
    
    teams = []
    for combo in combinations(applicants, contract.max_players):
        score = calculate_team_compatibility(combo)
        teams.append((score, combo))
    
    return max(teams, key=lambda x: x[0])[1]
```

### Zalety
✅ Social experience  
✅ Networking  
✅ Realistic teamwork  
✅ Higher engagement

### Wady
❌ Wymaga multiplayer infrastructure  
❌ Coordination overhead  
❌ Free-rider problem  
❌ Time zone issues

---

## 8️⃣ Challenge Contract 🏆 (Competitive)

### Opis
Limitowana liczba miejsc, ranking graczy. Najlepsi dostają najwięcej.

### Przykład
```json
{
  "type": "challenge",
  "title": "Leadership Tournament - Weekend Event",
  "max_participants": 50,
  "start_date": "2025-11-15 18:00",
  "end_date": "2025-11-17 23:59",
  "task": {
    "type": "case_study",
    "case": "Tesla's Leadership Crisis 2018",
    "questions": [...]
  },
  "reward_tiers": [
    {"rank": "1-10", "reward_multiplier": 3.0, "badge": "🥇 Gold"},
    {"rank": "11-25", "reward_multiplier": 1.5, "badge": "🥈 Silver"},
    {"rank": "26-50", "reward_multiplier": 0.7, "badge": "🥉 Bronze"}
  ]
}
```

### Flow
1. Event announcement 1 week before
2. Registration opens (limit 50)
3. Start: wszyscy dostają dostęp do zadania
4. 48h window na submission
5. AI grades all submissions
6. Ranking publikowany
7. Rewards według tiers

### Leaderboard
```
╔═══════════════════════════════════════════════╗
║ 🏆 Leadership Tournament - LIVE LEADERBOARD  ║
╠═══════════════════════════════════════════════╣
║ #1  🥇 Alice Chen        98.5  →  $3000      ║
║ #2  🥇 Bob Smith         97.2  →  $3000      ║
║ #3  🥇 Carol Wu          96.8  →  $3000      ║
║ ... ║
║ #15 🥈 You (David)       89.3  →  $1500      ║
║ ... ║
║ #47 🥉 Zara Ali          76.1  →  $700       ║
╚═══════════════════════════════════════════════╝
```

### Zalety
✅ Competitive spirit  
✅ Prestige  
✅ FOMO → high participation  
✅ Marketing opportunity

### Wady
❌ Wymaga cron jobs  
❌ Fairness concerns (time zones)  
❌ Pressure → cheating risk  
❌ Losers may feel demotivated

---

## 🎮 Balans Gry - Rekomendacje

### Dystrybucja w Puli Kontraktów
- **40% Text Contracts** - Core learning, deep thinking
- **30% Quiz Contracts** - Quick wins, knowledge verification
- **15% Decision Tree** - Interactive storytelling
- **7% Simulation** - Practical skills
- **5% Speed Challenge** - Fun, adrenaline
- **2% Case Study** - Premium content
- **1% Challenge** - Special events (monthly)
- **0.5% Collaborative** - Advanced players only

### Progression Path
**Level 1-2 (Beginner):**
- 60% Quiz, 30% Text, 10% Speed

**Level 3-4 (Intermediate):**
- 40% Text, 30% Quiz, 20% Decision Tree, 10% Simulation

**Level 5+ (Advanced):**
- 50% Text, 20% Decision Tree, 15% Case Study, 10% Challenge, 5% Collaborative

### Daily Mix Recommendation
Gracz powinien w ciągu tygodnia mieć dostęp do:
- 3-5 Quiz Contracts (quick daily practice)
- 2-3 Text Contracts (deep work)
- 1-2 Decision Tree (storytelling engagement)
- 1 Simulation lub Speed (variety)

---

## 📊 Metryki Sukcesu Per Type

| Metric | Quiz | Tree | Simulation | Speed | Case | Collab | Challenge |
|--------|------|------|------------|-------|------|--------|-----------|
| Completion Rate | >80% | >60% | >50% | >70% | >40% | >30% | >25% |
| Replay Rate | 20% | 40% | 30% | 60% | 10% | 5% | 50% |
| Avg Time (min) | 5-10 | 10-15 | 8-12 | 2-5 | 20-30 | 40-60 | 30-45 |
| Player Rating | 4.0+ | 4.5+ | 4.2+ | 4.3+ | 4.4+ | 3.8+ | 4.5+ |

---

## 🛠️ Implementation Priority & Timeline

### Phase 1: Q4 2025 (Nov-Dec)
**Target:** Quiz + Decision Tree

**Sprint 1 (Nov 1-15):**
- [ ] Schema definition dla Quiz
- [ ] Auto-grading engine
- [ ] UI components (radio, checkbox, fill-in)
- [ ] 10 Quiz Contracts created

**Sprint 2 (Nov 16-30):**
- [ ] Testing Quiz Contracts
- [ ] Schema definition dla Decision Tree
- [ ] Node traversal engine
- [ ] UI dla story + choices

**Sprint 3 (Dec 1-15):**
- [ ] 5 Decision Tree Contracts created (storytelling)
- [ ] Testing & bug fixes
- [ ] Player feedback gathering

**Sprint 4 (Dec 16-31):**
- [ ] Holiday themed contracts (Quiz + Tree)
- [ ] Balancing rewards
- [ ] Documentation update

### Phase 2: Q1 2026 (Jan-Mar)
**Target:** Simulation + Speed Challenge

**Sprint 5-6 (Jan):**
- [ ] Streamlit-sortables integration
- [ ] Priority Simulation created
- [ ] Budget Simulation created
- [ ] Speed Challenge timer system

**Sprint 7-8 (Feb-Mar):**
- [ ] 5 Simulation Contracts
- [ ] 10 Speed Challenges
- [ ] Testing & iteration

### Phase 3: Q2 2026 (Apr-Jun)
**Target:** Case Study + Challenge

### Phase 4: Q3 2026 (Jul-Sep)
**Target:** Collaborative

---

## 📝 Content Creation Guidelines

### Quiz Contract
**Time to create:** 30-45 minutes  
**Template:** 
1. Choose topic from lesson
2. Write 10 questions
3. Add distractors (wrong answers)
4. Write explanations
5. Test difficulty

### Decision Tree
**Time to create:** 3-5 hours  
**Template:**
1. Choose realistic scenario
2. Map decision tree (on paper first)
3. Write engaging narrative
4. Balance points
5. Test all paths

### Simulation
**Time to create:** 4-6 hours  
**Template:**
1. Define problem (prioritization, budget, etc.)
2. Create parameters
3. Define optimal solution
4. Build scoring algorithm
5. Test edge cases

---

## 🎯 Success Criteria

**Launch success if:**
- [ ] 80% completion rate dla Quiz
- [ ] 60% completion rate dla Decision Tree
- [ ] Average player rating 4.0+ dla nowych typów
- [ ] 50% graczy próbuje 3+ różnych typów w miesiącu
- [ ] Session time increases o 20% (więcej variety = więcej gry)
- [ ] Feedback: "less boring", "more fun", "addictive"

**Long-term success if:**
- [ ] Content creators mogą łatwo tworzyć nowe kontrakty
- [ ] Balans między edukacją a zabawą zachowany
- [ ] Retencja graczy rośnie (D7, D30)
- [ ] Gracze wracają dla różnych typów (not just one favorite)

---

**Wersja dokumentu:** 1.0  
**Autor:** Business Games Team  
**Ostatnia aktualizacja:** 21 października 2025  
**Status:** Ready for implementation  
**Następny review:** Po implementacji Quiz + Decision Tree (styczeń 2026)
