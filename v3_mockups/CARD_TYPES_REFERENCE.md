# 📚 Wzorce Kart Lekcji - BrainVenture Academy

Kompletna dokumentacja wszystkich typów kart używanych w lekcjach HTML mockup-ów.

---

## 1. 🎯 KARTA HERO (Wprowadzenie)

**Kiedy użyć:** Pierwsza karta każdej lekcji

**Elementy:**
- Duża emoji/ikona (80px)
- Cel lekcji
- Lista "Czego się nauczysz?" w `framework-box`
- `key-insight` z kluczową informacją

**Przykład:**
```html
<div class="card active" id="card1">
    <h2>🎯 Witaj w lekcji</h2>
    <div class="hero-image">🪚</div>
    <p>Opis lekcji...</p>

    <div class="framework-box">
        <h4>📚 Czego się nauczysz?</h4>
        <ul>
            <li><strong>Punkt 1</strong> - opis</li>
            <li><strong>Punkt 2</strong> - opis</li>
        </ul>
    </div>

    <div class="key-insight">
        <strong>💡 Kluczowa informacja:</strong> Treść...
    </div>
</div>
```

---

## 2. 📊 KARTA TEORIA/PODSTAWY

**Kiedy użyć:** Wyjaśnienie koncepcji, definicji, parametrów technicznych

**Elementy:**
- `framework-box` (pomarańczowy) - procesy, listy
- `key-insight` (złoty) - ważne wnioski
- `spec-grid` - parametry techniczne

**Przykład:**
```html
<div class="card" id="card2">
    <h2>📊 Specyfikacja Techniczna</h2>

    <div class="spec-grid">
        <div class="spec-item">
            <div class="spec-label">Parametr</div>
            <div class="spec-value">Wartość</div>
        </div>
    </div>

    <div class="key-insight">
        <strong>💡 Przewaga:</strong> Wyjaśnienie...
    </div>
</div>
```

**CSS spec-grid:**
```css
.spec-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin: 16px 0;
}

.spec-item {
    background: rgba(255, 255, 255, 0.05);
    padding: 12px;
    border-radius: 8px;
}
```

---

## 3. 🛡️ KARTA BEZPIECZEŃSTWO

**Kiedy użyć:** Instrukcje bezpieczeństwa, ostrzeżenia, systemy ochrony

**Elementy:**
- `safety-warning` (czerwony) - ostrzeżenia
- `framework-box` - procedury bezpieczeństwa

**Przykład:**
```html
<div class="card" id="card3">
    <h2>🛡️ Systemy Bezpieczeństwa</h2>

    <div class="safety-warning">
        <strong>⚠️ UWAGA:</strong> Krytyczne ostrzeżenie...
    </div>

    <div class="framework-box">
        <h4>Jak działa?</h4>
        <ul>
            <li>Punkt 1</li>
            <li>Punkt 2</li>
        </ul>
    </div>
</div>
```

**CSS safety-warning:**
```css
.safety-warning {
    background: rgba(255, 68, 68, 0.15);
    border-left: 4px solid #ff4444;
    padding: 20px;
    border-radius: 12px;
    margin: 24px 0;
}
```

---

## 4. 🎴 KARTA FISZKI (Flashcards)

**Kiedy użyć:** Zapamiętywanie 8-10 kluczowych faktów/definicji

**Elementy:**
- 10 interaktywnych fiszek z animacją flip 3D
- Nawigacja z przyciskami poprzednia/następna
- Wskaźnik postępu (kropki)
- Pytanie na przodzie, odpowiedź na odwrocie

**Przykład HTML:**
```html
<div class="card" id="card5">
    <h2>🎴 Fiszki: Zapamiętaj Kluczowe Informacje</h2>
    <p>Kliknij fiszkę, aby ją odwrócić i sprawdzić odpowiedź. Przejdź przez wszystkie 10 fiszek!</p>

    <div class="flashcard-container">
        <div class="flashcard" id="flashcard" onclick="flipCard()">
            <div class="flashcard-number" id="flashcardNumber">1/10</div>
            <div class="flashcard-inner" id="flashcardInner">
                <!-- Front -->
                <div class="flashcard-front">
                    <div class="flashcard-question" id="flashcardQuestion">
                        Pytanie?
                    </div>
                    <div class="flashcard-hint">💡 Kliknij, aby zobaczyć odpowiedź</div>
                </div>
                <!-- Back -->
                <div class="flashcard-back">
                    <div class="flashcard-answer" id="flashcardAnswer">
                        <strong>Odpowiedź</strong><br>Wyjaśnienie...
                    </div>
                </div>
            </div>
            <div class="flip-instruction">
                <i data-lucide="repeat" style="width: 14px; height: 14px;"></i>
                Kliknij aby obrócić
            </div>
        </div>
    </div>

    <div class="flashcard-controls">
        <button class="flashcard-btn" id="prevFlashcard" onclick="changeFlashcard(-1)" disabled>
            <i data-lucide="chevron-left" style="width: 16px; height: 16px;"></i>
            Poprzednia
        </button>
        <button class="flashcard-btn primary" id="nextFlashcard" onclick="changeFlashcard(1)">
            Następna
            <i data-lucide="chevron-right" style="width: 16px; height: 16px;"></i>
        </button>
    </div>

    <div class="flashcard-progress">Fiszka <span id="flashcardProgressText">1 z 10</span></div>
    <div class="flashcard-dots" id="flashcardDots"></div>
</div>
```

**CSS dla fiszek:**
```css
.flashcard-container {
    position: relative;
    min-height: 400px;
    margin: 32px 0;
}

.flashcard {
    background: linear-gradient(135deg, rgba(255, 68, 68, 0.15), rgba(255, 136, 0, 0.15));
    border: 2px solid rgba(255, 136, 0, 0.4);
    border-radius: 16px;
    padding: 40px;
    cursor: pointer;
    min-height: 350px;
    perspective: 1000px;
}

.flashcard-inner {
    position: relative;
    width: 100%;
    transition: transform 0.6s;
    transform-style: preserve-3d;
}

.flashcard.flipped .flashcard-inner {
    transform: rotateY(180deg);
}

.flashcard-front,
.flashcard-back {
    backface-visibility: hidden;
}

.flashcard-back {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    transform: rotateY(180deg);
}
```

**JavaScript dla fiszek:**
```javascript
const flashcards = [
    {
        question: "Pytanie 1?",
        answer: "<strong>Odpowiedź</strong><br>Wyjaśnienie..."
    },
    // ... 9 więcej
];

let currentFlashcard = 0;
let isFlipped = false;

function flipCard() {
    const card = document.getElementById('flashcard');
    isFlipped = !isFlipped;
    if (isFlipped) {
        card.classList.add('flipped');
    } else {
        card.classList.remove('flipped');
    }
}

function changeFlashcard(direction) {
    const nextCard = currentFlashcard + direction;
    if (nextCard < 0 || nextCard >= flashcards.length) return;
    
    currentFlashcard = nextCard;
    updateFlashcard();
}

function updateFlashcard() {
    const card = flashcards[currentFlashcard];
    document.getElementById('flashcard').classList.remove('flipped');
    isFlipped = false;
    document.getElementById('flashcardQuestion').textContent = card.question;
    document.getElementById('flashcardAnswer').innerHTML = card.answer;
    document.getElementById('flashcardNumber').textContent = `${currentFlashcard + 1}/10`;
    
    // Update buttons
    document.getElementById('prevFlashcard').disabled = currentFlashcard === 0;
    const nextBtn = document.getElementById('nextFlashcard');
    if (currentFlashcard === flashcards.length - 1) {
        nextBtn.disabled = true;
    }
    
    lucide.createIcons();
}
```

---

## 5. ❓ KARTA QUIZ (Wielokrotny Wybór)

**Kiedy użyć:** Test wiedzy z 3-5 pytań, niektóre z wieloma poprawnymi odpowiedziami

**WAŻNE:** To quiz z **checkboxami** - użytkownik może zaznaczyć kilka odpowiedzi!

**Elementy:**
- Pytania z checkboxami
- Przycisk "Sprawdź odpowiedź" (pojawia się po zaznaczeniu)
- Kolorowe feedback: zielony (poprawne), czerwony (błędne), żółty (pominięte poprawne)
- Wyjaśnienie po sprawdzeniu

**Przykład HTML:**
```html
<div class="card" id="card9">
    <h2>❓ Test Wiedzy</h2>
    <p>Sprawdź wiedzę! <strong>Uwaga: niektóre pytania mają więcej niż jedną poprawną odpowiedź.</strong></p>

    <div class="quiz-question">
        <p style="font-weight: 600; margin-bottom: 16px;">1. Pytanie? (Zaznacz wszystkie poprawne)</p>
        <div class="quiz-options">
            <div class="quiz-option" data-question="0" data-option="0">
                <input type="checkbox" id="q0_opt0" onchange="toggleQuizOption(0, 0)">
                <label for="q0_opt0">Opcja A</label>
            </div>
            <div class="quiz-option" data-question="0" data-option="1">
                <input type="checkbox" id="q0_opt1" onchange="toggleQuizOption(0, 1)">
                <label for="q0_opt1">Opcja B</label>
            </div>
            <div class="quiz-option" data-question="0" data-option="2">
                <input type="checkbox" id="q0_opt2" onchange="toggleQuizOption(0, 2)">
                <label for="q0_opt2">Opcja C</label>
            </div>
            <div class="quiz-option" data-question="0" data-option="3">
                <input type="checkbox" id="q0_opt3" onchange="toggleQuizOption(0, 3)">
                <label for="q0_opt3">Opcja D</label>
            </div>
        </div>
        <button class="quiz-check-btn" data-check="0" onclick="checkQuizAnswer(0)">Sprawdź odpowiedź</button>
        <div class="quiz-explanation" data-explanation="0">
            <strong>✅ Prawidłowe odpowiedzi:</strong> A, B<br>
            Wyjaśnienie dlaczego...
        </div>
    </div>
</div>
```

**CSS dla quizu:**
```css
.quiz-question {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
}

.quiz-options {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin: 16px 0;
}

.quiz-option {
    padding: 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 12px;
}

.quiz-option input[type="checkbox"] {
    width: 20px;
    height: 20px;
    cursor: pointer;
}

.quiz-option.selected {
    background: rgba(255, 136, 0, 0.2);
    border-color: #ff8800;
}

.quiz-option.correct {
    background: rgba(0, 255, 136, 0.2);
    border-color: #00ff88;
}

.quiz-option.incorrect {
    background: rgba(255, 68, 68, 0.2);
    border-color: #ff4444;
}

.quiz-option.missed {
    background: rgba(255, 215, 0, 0.2);
    border-color: #ffd700;
}

.quiz-explanation {
    background: rgba(0, 212, 255, 0.1);
    border-left: 4px solid #00d4ff;
    padding: 16px;
    border-radius: 8px;
    margin-top: 16px;
    display: none;
}

.quiz-explanation.show {
    display: block;
}

.quiz-check-btn {
    margin-top: 16px;
    padding: 12px 24px;
    background: linear-gradient(135deg, #ff8800, #ffd700);
    color: #0a0a1a;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    display: none;
}

.quiz-check-btn.show {
    display: inline-block;
}
```

**JavaScript dla quizu:**
```javascript
// Definicja poprawnych odpowiedzi (indeksy 0-3)
const quizAnswers = [
    [0, 1],         // Q1: Opcje A i B są poprawne
    [2],            // Q2: Tylko opcja C jest poprawna
    [0, 1, 2],      // Q3: Opcje A, B i C są poprawne
];
const userAnswers = [[], [], []]; // Odpowiedzi użytkownika

function toggleQuizOption(questionIndex, optionIndex) {
    const checkbox = document.getElementById(`q${questionIndex}_opt${optionIndex}`);
    const option = checkbox.parentElement;
    
    if (checkbox.checked) {
        if (!userAnswers[questionIndex].includes(optionIndex)) {
            userAnswers[questionIndex].push(optionIndex);
        }
        option.classList.add('selected');
    } else {
        userAnswers[questionIndex] = userAnswers[questionIndex].filter(opt => opt !== optionIndex);
        option.classList.remove('selected');
    }

    // Pokaż przycisk jeśli coś zaznaczono
    const checkBtn = document.querySelector(`[data-check="${questionIndex}"]`);
    if (userAnswers[questionIndex].length > 0) {
        checkBtn.classList.add('show');
    } else {
        checkBtn.classList.remove('show');
    }
}

function checkQuizAnswer(questionIndex) {
    if (userAnswers[questionIndex].length === 0) return;

    const correctAnswers = quizAnswers[questionIndex];
    const selectedAnswers = userAnswers[questionIndex];

    // Oznacz każdą opcję
    for (let i = 0; i < 4; i++) {
        const option = document.querySelector(`[data-question="${questionIndex}"][data-option="${i}"]`);
        const checkbox = document.getElementById(`q${questionIndex}_opt${i}`);
        const isCorrectAnswer = correctAnswers.includes(i);
        const isSelected = selectedAnswers.includes(i);

        if (isCorrectAnswer && isSelected) {
            option.classList.add('correct'); // Zielony - dobrze zaznaczone
        } else if (!isCorrectAnswer && isSelected) {
            option.classList.add('incorrect'); // Czerwony - źle zaznaczone
        } else if (isCorrectAnswer && !isSelected) {
            option.classList.add('missed'); // Żółty - pominięte poprawne
        }

        checkbox.disabled = true;
    }

    // Pokaż wyjaśnienie
    const explanation = document.querySelector(`[data-explanation="${questionIndex}"]`);
    explanation.classList.add('show');

    // Ukryj przycisk
    const checkBtn = document.querySelector(`[data-check="${questionIndex}"]`);
    checkBtn.disabled = true;
    checkBtn.style.display = 'none';
}
```

---

## 6. ✍️ KARTA ĆWICZENIE INTERAKTYWNE

**Kiedy użyć:** Scenariusz biznesowy z odpowiedzią otwartą

**Elementy:**
- Scenariusz w ramce
- `textarea` do wpisania odpowiedzi
- Przykładowa odpowiedź w `framework-box`
- Feedback w `key-insight`

**Przykład:**
```html
<div class="card" id="card4">
    <h2>✍️ Ćwiczenie: Dobór Narzędzia</h2>

    <div style="background: rgba(255, 136, 0, 0.1); padding: 20px; border-radius: 12px;">
        <p><strong>Scenariusz:</strong></p>
        <p style="font-style: italic;">Klient mówi: "Potrzebuję..."</p>
    </div>

    <p><strong>Jakie pytanie zadasz?</strong></p>
    <textarea class="interactive-input" rows="3" placeholder="Twoja odpowiedź..."></textarea>

    <div class="framework-box">
        <h4>💡 Przykładowa odpowiedź:</h4>
        <p>Sugestia...</p>
    </div>

    <div class="key-insight">
        <strong>Feedback:</strong> Wyjaśnienie...
    </div>
</div>
```

---

## 7. 💭 KARTA REFLEKSJA/PODSUMOWANIE

**Kiedy użyć:** Ostatnia karta - podsumowanie i zadania praktyczne

**Elementy:**
- Pytania otwarte z `textarea`
- Lista kluczowych wniosków
- `key-insight` z następnymi krokami

**Przykład:**
```html
<div class="card" id="card10">
    <h2>💭 Refleksja i Zastosowanie</h2>

    <p>Odpowiedz na pytania, aby utrwalić wiedzę:</p>

    <h3>1. Bezpieczeństwo</h3>
    <textarea class="interactive-input" placeholder="Wymień 5 zasad..."></textarea>

    <h3>2. Praktyka</h3>
    <div class="framework-box">
        <h4>Scenariusz:</h4>
        <p>Opis sytuacji...</p>
    </div>
    <textarea class="interactive-input" placeholder="Jak postąpisz?"></textarea>

    <div class="key-insight">
        <strong>🎯 Następne kroki:</strong>
        <ul>
            <li>Engram - utrwalenie</li>
            <li>Zasób - tabela</li>
            <li>Narzędzie - kalkulator</li>
            <li>Drill - quiz</li>
        </ul>
    </div>
</div>
```

---

## 🎨 Wspólne Komponenty CSS

**Framework Box (pomarańczowy):**
```css
.framework-box {
    background: rgba(255, 136, 0, 0.1);
    border-left: 4px solid #ff8800;
    padding: 20px;
    border-radius: 12px;
    margin: 24px 0;
}
```

**Key Insight Box (złoty):**
```css
.key-insight {
    background: rgba(255, 215, 0, 0.15);
    border-left: 4px solid #ffd700;
    padding: 20px;
    border-radius: 12px;
    margin: 24px 0;
}
```

**Interactive Input:**
```css
.interactive-input {
    width: 100%;
    padding: 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    color: white;
    font-family: 'Outfit', sans-serif;
    font-size: 15px;
    margin: 16px 0;
}
```

---

## 📋 Checklist Tworzenia Lekcji

✅ **Card 1**: Hero z celem lekcji  
✅ **Card 2-3**: Teoria/podstawy  
✅ **Card 4**: Ćwiczenie interaktywne (opcjonalne)  
✅ **Card 5**: Fiszki (10 kluczowych faktów)  
✅ **Card 6-8**: Szczegóły, techniki, produkty  
✅ **Card 9**: Quiz wielokrotnego wyboru (3-5 pytań)  
✅ **Card 10**: Refleksja i podsumowanie  

**Pamiętaj:**
- Nawigacja: Przyciski Wstecz/Dalej
- Progress bar: `(currentCard / totalCards) * 100%`
- Lucide icons: `lucide.createIcons()` po każdej zmianie DOM
- Total cards: Zaktualizuj `const totalCards = X` w JavaScript

---

**Autor:** GitHub Copilot  
**Data:** 16 stycznia 2026  
**Wersja:** 1.0
