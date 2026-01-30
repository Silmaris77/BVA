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

## 8. 🔢 KARTA RANKING (Drag & Drop Priorytetów)

**Kiedy użyć:** Uporządkowanie elementów według ważności, proces sekwencyjny, hierarchie

**Elementy:**
- Dual-zone layout (pool → ranking list)
- Draggable items z ikonami Lucide
- Auto-numeracja pozycji (1, 2, 3...)
- Przycisk "Sprawdź ranking"
- Feedback z liczbą poprawnych pozycji

**Przykład HTML:**
```html
<div class="card" id="card12">
    <h2>🔢 Priorytetyzacja: Ustaw kolejność działań BHP</h2>
    <p>Przeciągnij elementy z lewej strony na listę po prawej, ustawiając je od najważniejszego (góra) do najmniej ważnego (dół).</p>

    <div class="ranking-container">
        <div class="ranking-pool">
            <h4>Elementy do uporządkowania:</h4>
            <div class="ranking-item" draggable="true" data-priority="1">
                <i data-lucide="shield-check"></i>
                <span>Sprawdzenie osłon przed włączeniem</span>
            </div>
            <div class="ranking-item" draggable="true" data-priority="2">
                <i data-lucide="hard-hat"></i>
                <span>Założenie środków ochrony osobistej</span>
            </div>
            <div class="ranking-item" draggable="true" data-priority="3">
                <i data-lucide="disc"></i>
                <span>Sprawdzenie stanu tarczy tnącej</span>
            </div>
            <!-- więcej elementów -->
        </div>

        <div class="ranking-zone">
            <h4>Twoja kolejność (od najważniejszego):</h4>
            <div class="ranking-list" id="rankingList">
                <!-- Elementy przeciągane tutaj -->
            </div>
        </div>
    </div>

    <button class="check-btn" onclick="checkRanking()" style="display:none;">Sprawdź ranking</button>
    <div class="result-message" id="rankingResult"></div>
</div>
```

**CSS dla Ranking:**
```css
.ranking-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    margin: 24px 0;
}

.ranking-pool,
.ranking-zone {
    background: rgba(255, 255, 255, 0.03);
    padding: 20px;
    border-radius: 12px;
    border: 2px dashed rgba(255, 136, 0, 0.3);
}

.ranking-item {
    background: rgba(255, 136, 0, 0.1);
    border: 2px solid rgba(255, 136, 0, 0.4);
    padding: 16px;
    margin: 12px 0;
    border-radius: 12px;
    cursor: move;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.3s ease;
}

.ranking-item:hover {
    background: rgba(255, 136, 0, 0.2);
    transform: translateX(4px);
}

.ranking-item.dragging {
    opacity: 0.5;
    transform: scale(0.95);
}

.ranking-list {
    min-height: 300px;
    background: rgba(0, 255, 136, 0.05);
    border: 2px solid rgba(0, 255, 136, 0.3);
    border-radius: 12px;
    padding: 16px;
}

.ranking-item .ranking-number {
    background: #ff8800;
    color: #0a0a1a;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    margin-right: 8px;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .ranking-container {
        grid-template-columns: 1fr;
    }
}
```

**JavaScript dla Ranking:**
```javascript
let rankingDraggedElement = null;

function initRanking() {
    const items = document.querySelectorAll('.ranking-item');
    const rankingList = document.getElementById('rankingList');

    items.forEach(item => {
        item.addEventListener('dragstart', (e) => {
            rankingDraggedElement = item;
            item.classList.add('dragging');
        });

        item.addEventListener('dragend', (e) => {
            item.classList.remove('dragging');
        });
    });

    rankingList.addEventListener('dragover', (e) => {
        e.preventDefault();
    });

    rankingList.addEventListener('drop', (e) => {
        e.preventDefault();
        if (rankingDraggedElement) {
            rankingList.appendChild(rankingDraggedElement);
            updateRankingNumbers();
            document.querySelector('.check-btn').style.display = 'inline-block';
        }
    });
}

function updateRankingNumbers() {
    const rankingList = document.getElementById('rankingList');
    const items = rankingList.querySelectorAll('.ranking-item');
    
    items.forEach((item, index) => {
        // Usuń stary numer jeśli istnieje
        const oldNumber = item.querySelector('.ranking-number');
        if (oldNumber) oldNumber.remove();
        
        // Dodaj nowy numer
        const numberSpan = document.createElement('span');
        numberSpan.className = 'ranking-number';
        numberSpan.textContent = index + 1;
        item.insertBefore(numberSpan, item.firstChild);
    });
}

function checkRanking() {
    const rankingList = document.getElementById('rankingList');
    const items = rankingList.querySelectorAll('.ranking-item');
    let correctCount = 0;

    items.forEach((item, index) => {
        const correctPosition = parseInt(item.dataset.priority) - 1;
        if (index === correctPosition) {
            correctCount++;
            item.style.borderColor = '#00ff88';
        } else {
            item.style.borderColor = '#ff4444';
        }
    });

    const result = document.getElementById('rankingResult');
    const total = items.length;
    
    if (correctCount === total) {
        result.innerHTML = `🎯 <strong>Doskonale!</strong> Wszystkie elementy na właściwych pozycjach (${correctCount}/${total})`;
        result.style.color = '#00ff88';
    } else {
        result.innerHTML = `⚠️ <strong>Wynik:</strong> ${correctCount}/${total} poprawnych pozycji. Spróbuj ponownie!`;
        result.style.color = '#ffd700';
    }
}

// Inicjalizacja
window.addEventListener('load', () => {
    initRanking();
    lucide.createIcons();
});
```

**Use Cases:**
- BHP priorities (jak w przykładzie)
- Etapy procesu sprzedaży
- Hierarchia potrzeb
- GTD priorities
- Eisenhower Matrix

---

## 9. 📝 KARTA FILL-IN-THE-BLANKS (Uzupełnij Luki)

**Kiedy użyć:** Memoryzacja parametrów technicznych, vocabulary, formulas

**Elementy:**
- Tekst z lukami (inputs)
- Klikalne opcje słów (word bank)
- Automatyczne wypełnianie luk
- Walidacja z kolorowaniem (zielony/czerwony)
- Wynik liczbowy (X/Y poprawnych)

**Przykład HTML:**
```html
<div class="card" id="card13">
    <h2>📝 Uzupełnij Specyfikację</h2>
    <p>Kliknij słowa poniżej, aby uzupełnić tekst. Każde słowo pasuje tylko do jednej luki.</p>

    <div class="fill-blanks-text">
        <p>
            Milwaukee MX FUEL COS350G2 posiada zabezpieczenie RAPIDSTOP, które zatrzymuje tarczę w mniej niż 
            <input type="text" class="fill-blank" data-answer="3" readonly> sekundy. 
            Maksymalna głębokość cięcia to <input type="text" class="fill-blank" data-answer="125" readonly> mm, 
            a tarcza ma średnicę <input type="text" class="fill-blank" data-answer="350" readonly> mm. 
            Do cięcia betonu zalecana jest tarcza <input type="text" class="fill-blank" data-answer="HUDD" readonly>, 
            natomiast do asfaltu tarcza <input type="text" class="fill-blank" data-answer="CCS" readonly>. 
            Przy długotrwałej pracy warto mieć opcję <input type="text" class="fill-blank" data-answer="SWITCH TANK" readonly>.
        </p>
    </div>

    <div class="word-bank">
        <h4>Dostępne słowa:</h4>
        <div class="word-options">
            <button class="word-option" onclick="fillBlankFromOption(this)">RAPIDSTOP</button>
            <button class="word-option" onclick="fillBlankFromOption(this)">3</button>
            <button class="word-option" onclick="fillBlankFromOption(this)">125</button>
            <button class="word-option" onclick="fillBlankFromOption(this)">350</button>
            <button class="word-option" onclick="fillBlankFromOption(this)">HUDD</button>
            <button class="word-option" onclick="fillBlankFromOption(this)">CCS</button>
            <button class="word-option" onclick="fillBlankFromOption(this)">SWITCH TANK</button>
            <button class="word-option" onclick="fillBlankFromOption(this)">250</button>
            <button class="word-option" onclick="fillBlankFromOption(this)">5</button>
            <button class="word-option" onclick="fillBlankFromOption(this)">DUH</button>
        </div>
    </div>

    <button class="check-btn" onclick="checkAllBlanks()">Sprawdź odpowiedzi</button>
    <div class="result-message" id="blanksResult"></div>
</div>
```

**CSS dla Fill Blanks:**
```css
.fill-blanks-text {
    background: rgba(255, 255, 255, 0.03);
    padding: 24px;
    border-radius: 12px;
    margin: 24px 0;
    font-size: 16px;
    line-height: 2;
}

.fill-blank {
    display: inline-block;
    min-width: 100px;
    padding: 4px 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 2px dashed #ff8800;
    border-radius: 8px;
    color: #ffd700;
    font-family: 'Outfit', sans-serif;
    font-size: 16px;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
}

.fill-blank:focus {
    outline: none;
    border-color: #ffd700;
    box-shadow: 0 0 8px rgba(255, 215, 0, 0.5);
}

.fill-blank.filled {
    border-style: solid;
    background: rgba(255, 136, 0, 0.2);
}

.fill-blank.correct {
    border-color: #00ff88;
    background: rgba(0, 255, 136, 0.2);
}

.fill-blank.incorrect {
    border-color: #ff4444;
    background: rgba(255, 68, 68, 0.2);
    animation: shake 0.3s;
}

.word-bank {
    margin: 24px 0;
}

.word-options {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 16px;
}

.word-option {
    padding: 12px 20px;
    background: rgba(255, 136, 0, 0.1);
    border: 2px solid rgba(255, 136, 0, 0.4);
    border-radius: 12px;
    color: white;
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.word-option:hover {
    background: rgba(255, 136, 0, 0.3);
    transform: translateY(-2px);
}

.word-option.used {
    opacity: 0.3;
    cursor: not-allowed;
    pointer-events: none;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}
```

**JavaScript dla Fill Blanks:**
```javascript
let currentBlankIndex = 0;
const blanks = document.querySelectorAll('.fill-blank');

// Focus first blank
if (blanks.length > 0) {
    blanks[0].focus();
}

// Click na blank aby go aktywować
blanks.forEach((blank, index) => {
    blank.addEventListener('click', () => {
        currentBlankIndex = index;
        blanks.forEach(b => b.style.boxShadow = 'none');
        blank.style.boxShadow = '0 0 8px rgba(255, 215, 0, 0.5)';
    });
});

function fillBlankFromOption(button) {
    if (currentBlankIndex >= blanks.length) {
        currentBlankIndex = 0;
    }
    
    const blank = blanks[currentBlankIndex];
    const word = button.textContent;
    
    blank.value = word;
    blank.classList.add('filled');
    button.classList.add('used');
    
    // Przejdź do następnej pustej luki
    currentBlankIndex++;
    while (currentBlankIndex < blanks.length && blanks[currentBlankIndex].value !== '') {
        currentBlankIndex++;
    }
    
    if (currentBlankIndex < blanks.length) {
        blanks[currentBlankIndex].focus();
    }
}

function checkBlank(blank) {
    const userAnswer = blank.value.trim();
    const correctAnswer = blank.dataset.answer;
    
    if (userAnswer === correctAnswer) {
        blank.classList.add('correct');
        blank.classList.remove('incorrect');
        return true;
    } else {
        blank.classList.add('incorrect');
        blank.classList.remove('correct');
        return false;
    }
}

function checkAllBlanks() {
    let correctCount = 0;
    const total = blanks.length;
    
    blanks.forEach(blank => {
        if (checkBlank(blank)) {
            correctCount++;
        }
    });
    
    const result = document.getElementById('blanksResult');
    
    if (correctCount === total) {
        result.innerHTML = `🎯 <strong>Perfekcyjnie!</strong> Wszystkie luki wypełnione poprawnie (${correctCount}/${total})`;
        result.style.color = '#00ff88';
    } else {
        result.innerHTML = `⚠️ <strong>Wynik:</strong> ${correctCount}/${total} poprawnych. Sprawdź czerwone pola.`;
        result.style.color = '#ffd700';
    }
}
```

**Use Cases:**
- Technical specifications
- Vocabulary practice
- Process descriptions
- Formula completion
- Key facts memorization

---

## 10. 🔗 KARTA MATCHING PAIRS (Dopasuj Pary)

**Kiedy użyć:** Kojarzenie pojęć, product-application matching, terminology learning

**Elementy:**
- Two-column layout (items ↔ targets)
- Click-based interaction (nie drag & drop)
- Visual feedback (green = matched, orange = selected)
- State tracking (matched pairs)
- Gratulacje po dopasowaniu wszystkich

**Przykład HTML:**
```html
<div class="card" id="card14">
    <h2>🔗 Dopasuj Pary: Tarcza ↔ Zastosowanie</h2>
    <p>Kliknij tarczę, a następnie jej prawidłowe zastosowanie, aby stworzyć parę.</p>

    <div class="matching-container">
        <div class="matching-column">
            <h4>Tarcze:</h4>
            <div class="matching-item" data-match="concrete" onclick="selectMatch(this)">
                <i data-lucide="disc"></i>
                <div>
                    <strong>HUDD</strong>
                    <div class="item-subtitle">High-performance Universal Diamond Disc</div>
                </div>
            </div>
            <div class="matching-item" data-match="steel" onclick="selectMatch(this)">
                <i data-lucide="disc"></i>
                <div>
                    <strong>STEELHEAD</strong>
                    <div class="item-subtitle">Diamond disc for steel</div>
                </div>
            </div>
            <div class="matching-item" data-match="asphalt" onclick="selectMatch(this)">
                <i data-lucide="disc"></i>
                <div>
                    <strong>CCS</strong>
                    <div class="item-subtitle">Cutting & Coring System</div>
                </div>
            </div>
        </div>

        <div class="matching-column">
            <h4>Zastosowanie:</h4>
            <div class="matching-item" data-match="concrete" onclick="selectMatch(this)">
                <i data-lucide="box"></i>
                <span>Beton / Granit</span>
            </div>
            <div class="matching-item" data-match="steel" onclick="selectMatch(this)">
                <i data-lucide="zap"></i>
                <span>Metal / Stal zbrojeniowa</span>
            </div>
            <div class="matching-item" data-match="asphalt" onclick="selectMatch(this)">
                <i data-lucide="truck"></i>
                <span>Asfalt / Materiały miękkie</span>
            </div>
        </div>
    </div>

    <div class="result-message" id="matchingResult"></div>
</div>
```

**CSS dla Matching:**
```css
.matching-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    margin: 32px 0;
}

.matching-column h4 {
    color: #ffd700;
    margin-bottom: 16px;
    text-align: center;
}

.matching-item {
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.2);
    padding: 16px;
    margin: 12px 0;
    border-radius: 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all 0.3s ease;
}

.matching-item:hover {
    background: rgba(255, 136, 0, 0.1);
    border-color: rgba(255, 136, 0, 0.5);
    transform: translateX(4px);
}

.matching-item.selected {
    background: rgba(255, 136, 0, 0.2);
    border-color: #ff8800;
    border-width: 3px;
}

.matching-item.matched {
    background: rgba(0, 255, 136, 0.2);
    border-color: #00ff88;
    cursor: default;
    pointer-events: none;
}

.matching-item.matched::after {
    content: '✅';
    margin-left: auto;
    font-size: 20px;
}

.item-subtitle {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    margin-top: 4px;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .matching-container {
        grid-template-columns: 1fr;
    }
}
```

**JavaScript dla Matching:**
```javascript
let firstMatch = null;
let matchedPairs = new Set();

function selectMatch(element) {
    // Ignoruj już dopasowane elementy
    if (element.classList.contains('matched')) return;
    
    if (firstMatch === null) {
        // Pierwszy wybór
        firstMatch = element;
        element.classList.add('selected');
    } else {
        // Drugi wybór - sprawdź czy pasuje
        const firstId = firstMatch.dataset.match;
        const secondId = element.dataset.match;
        
        if (firstId === secondId && firstMatch !== element) {
            // Poprawna para!
            firstMatch.classList.remove('selected');
            firstMatch.classList.add('matched');
            element.classList.add('matched');
            matchedPairs.add(firstId);
            
            // Sprawdź czy wszystkie pary dopasowane
            checkAllMatched();
        } else {
            // Niepoprawna para
            element.classList.add('selected');
            setTimeout(() => {
                firstMatch.classList.remove('selected');
                element.classList.remove('selected');
            }, 500);
        }
        
        firstMatch = null;
    }
}

function checkAllMatched() {
    const totalPairs = 3; // liczba par do dopasowania
    
    if (matchedPairs.size === totalPairs) {
        const result = document.getElementById('matchingResult');
        result.innerHTML = '🎯 <strong>Doskonale!</strong> Wszystkie pary poprawnie dopasowane!';
        result.style.color = '#00ff88';
        result.style.fontSize = '18px';
        result.style.marginTop = '24px';
        result.style.textAlign = 'center';
    }
}
```

**Use Cases:**
- Product ↔ Application matching
- Concept ↔ Definition
- Person ↔ Quote
- Country ↔ Capital
- Problem ↔ Solution

---

## 11. ❓ KARTA TRUE/FALSE (Prawda/Fałsz)

**Kiedy użyć:** Szybki test wiedzy, weryfikacja faktów, debunking mitów

**Elementy:**
- Statement cards (twierdzenia do oceny)
- Buttons: PRAWDA / FAŁSZ z ikonami
- Natychmiastowy feedback po kliknięciu
- Wyjaśnienie dlaczego odpowiedź jest poprawna/błędna
- Licznik punktów (X/Y poprawnych)

**Przykład HTML:**
```html
<div class="card" id="card11">
    <h2>❓ True/False - Test Szybkiej Wiedzy</h2>
    <p>Odpowiedz Prawda lub Fałsz. Natychmiastowy feedback po każdej odpowiedzi.</p>

    <div class="true-false-container">
        <div class="statement-card">
            <div class="statement-text">
                <strong>1.</strong> Przecinarka MXF COS350 może ciąć beton do głębokości 125mm w jednym przejściu.
            </div>
            <div class="tf-buttons">
                <button class="tf-button true" onclick="checkTrueFalse(1, true, this)">
                    <i data-lucide="check-circle" style="width: 20px; height: 20px;"></i>
                    PRAWDA
                </button>
                <button class="tf-button false" onclick="checkTrueFalse(1, false, this)">
                    <i data-lucide="x-circle" style="width: 20px; height: 20px;"></i>
                    FAŁSZ
                </button>
            </div>
            <div class="tf-feedback" id="feedback1">
                <strong>✅ Prawidłowo!</strong> MXF COS350 z tarczą 350mm może ciąć do głębokości 125mm.
            </div>
        </div>
        <!-- Więcej statement cards... -->
    </div>

    <div class="key-insight">
        <strong>🎓 Wynik końcowy:</strong> <span id="tfScore">0/5</span> poprawnych odpowiedzi
    </div>
</div>
```

**CSS dla True/False:**
```css
.true-false-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin: 24px 0;
}

.statement-card {
    background: rgba(255, 255, 255, 0.03);
    padding: 24px;
    border-radius: 12px;
    border: 2px solid rgba(255, 255, 255, 0.1);
}

.statement-text {
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 16px;
}

.tf-buttons {
    display: flex;
    gap: 12px;
    margin: 16px 0;
}

.tf-button {
    flex: 1;
    padding: 16px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
    color: white;
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all 0.3s ease;
}

.tf-button:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}

.tf-button.true.correct {
    background: rgba(0, 255, 136, 0.2);
    border-color: #00ff88;
}

.tf-button.false.correct {
    background: rgba(0, 255, 136, 0.2);
    border-color: #00ff88;
}

.tf-button.incorrect {
    background: rgba(255, 68, 68, 0.2);
    border-color: #ff4444;
    animation: shake 0.3s;
}

.tf-feedback {
    background: rgba(0, 212, 255, 0.1);
    border-left: 4px solid #00d4ff;
    padding: 16px;
    border-radius: 8px;
    margin-top: 12px;
    display: none;
}

.tf-feedback.show {
    display: block;
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}
```

**JavaScript dla True/False:**
```javascript
let tfCorrectAnswers = [true, false, true, true, true]; // Poprawne odpowiedzi
let tfScore = 0;
let tfAnswered = 0;

function checkTrueFalse(questionId, userAnswer, buttonElement) {
    const isCorrect = tfCorrectAnswers[questionId - 1] === userAnswer;
    const parentCard = buttonElement.closest('.statement-card');
    const allButtons = parentCard.querySelectorAll('.tf-button');
    const feedback = parentCard.querySelector('.tf-feedback');
    
    // Disable wszystkie przyciski
    allButtons.forEach(btn => {
        btn.disabled = true;
        btn.style.opacity = '0.6';
    });
    
    if (isCorrect) {
        buttonElement.classList.add('correct');
        tfScore++;
    } else {
        buttonElement.classList.add('incorrect');
        // Highlight poprawnej odpowiedzi
        const correctButton = tfCorrectAnswers[questionId - 1] ? 
            parentCard.querySelector('.tf-button.true') : 
            parentCard.querySelector('.tf-button.false');
        correctButton.classList.add('correct');
    }
    
    // Pokaż feedback
    feedback.classList.add('show');
    
    // Update score
    tfAnswered++;
    document.getElementById('tfScore').textContent = `${tfScore}/${tfAnswered}`;
    
    lucide.createIcons();
}
```

**Use Cases:**
- Fact verification (technical specs)
- Myth busting (common misconceptions)
- Safety knowledge check
- Quick comprehension test
- Pre-test/post-test comparison

---

## 12. ⭐ KARTA RATING SCALE (Skala Oceny)

**Kiedy użyć:** Samoocena wiedzy, ewaluacja confidence, feedback po lekcji

**Elementy:**
- Pytania z 5-punktową skalą Likerta
- Rating points (1-5) z labelkami
- Endpoints (teksty na krańcach skali)
- Agregacja wyników (średnia)
- Wizualizacja postępu

**Przykład HTML:**
```html
<div class="card" id="card15">
    <h2>⭐ Skala Oceny - Ewaluacja Wiedzy</h2>
    <p>Oceń swój poziom znajomości każdego zagadnienia w skali 1-5.</p>

    <div class="rating-container">
        <div class="rating-question">
            <p style="font-weight: 600; margin-bottom: 16px;">
                Jak dobrze rozumiesz działanie systemu RAPIDSTOP™?
            </p>
            <div class="rating-scale">
                <div class="rating-point" onclick="selectRating(1, 1, this)">
                    <div class="rating-number">1</div>
                    <div class="rating-label">Słabo</div>
                </div>
                <div class="rating-point" onclick="selectRating(1, 2, this)">
                    <div class="rating-number">2</div>
                    <div class="rating-label">Podstawy</div>
                </div>
                <div class="rating-point" onclick="selectRating(1, 3, this)">
                    <div class="rating-number">3</div>
                    <div class="rating-label">Dobrze</div>
                </div>
                <div class="rating-point" onclick="selectRating(1, 4, this)">
                    <div class="rating-number">4</div>
                    <div class="rating-label">B. dobrze</div>
                </div>
                <div class="rating-point" onclick="selectRating(1, 5, this)">
                    <div class="rating-number">5</div>
                    <div class="rating-label">Ekspert</div>
                </div>
            </div>
            <div class="rating-endpoints">
                <span>Nie znam tego systemu</span>
                <span>Mogę go wytłumaczyć innym</span>
            </div>
        </div>
        <!-- Więcej pytań... -->
    </div>

    <div class="framework-box">
        <h4>📊 Twoje oceny:</h4>
        <div id="ratingResults">
            <div>RAPIDSTOP™: <span id="rating1">-</span>/5</div>
            <div>Dobór tarcz: <span id="rating2">-</span>/5</div>
            <div>Procedury BHP: <span id="rating3">-</span>/5</div>
            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1);">
                <strong>Średnia:</strong> <span id="ratingAverage">0.0</span>/5
            </div>
        </div>
    </div>
</div>
```

**CSS dla Rating Scale:**
```css
.rating-container {
    display: flex;
    flex-direction: column;
    gap: 32px;
    margin: 24px 0;
}

.rating-question {
    background: rgba(255, 255, 255, 0.03);
    padding: 24px;
    border-radius: 12px;
}

.rating-scale {
    display: flex;
    gap: 12px;
    margin: 20px 0;
    justify-content: center;
}

.rating-point {
    flex: 1;
    max-width: 100px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.rating-number {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: 700;
    margin: 0 auto 8px;
    transition: all 0.3s ease;
}

.rating-label {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
}

.rating-point:hover .rating-number {
    background: rgba(255, 136, 0, 0.2);
    border-color: #ff8800;
    transform: scale(1.1);
}

.rating-point.selected .rating-number {
    background: linear-gradient(135deg, #ff8800, #ffd700);
    border-color: #ffd700;
    color: #0a0a1a;
    transform: scale(1.15);
}

.rating-endpoints {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    color: rgba(255, 255, 255, 0.6);
    margin-top: 8px;
}

/* Mobile */
@media (max-width: 768px) {
    .rating-scale {
        flex-direction: column;
    }
    
    .rating-point {
        max-width: 100%;
    }
}
```

**JavaScript dla Rating Scale:**
```javascript
let ratings = [null, null, null]; // Oceny użytkownika dla 3 pytań

function selectRating(questionId, value, element) {
    // Usuń previous selection
    const scale = element.parentElement;
    scale.querySelectorAll('.rating-point').forEach(point => {
        point.classList.remove('selected');
    });
    
    // Zaznacz wybraną
    element.classList.add('selected');
    
    // Zapisz ocenę
    ratings[questionId - 1] = value;
    
    // Update display
    document.getElementById(`rating${questionId}`).textContent = value;
    
    // Oblicz średnią
    const validRatings = ratings.filter(r => r !== null);
    if (validRatings.length > 0) {
        const average = validRatings.reduce((a, b) => a + b, 0) / validRatings.length;
        document.getElementById('ratingAverage').textContent = average.toFixed(1);
    }
}
```

**Use Cases:**
- Self-assessment (confidence levels)
- Pre-test / Post-test comparison
- Lesson feedback collection
- Knowledge gap identification
- Progress tracking over time

**Analytics Value:**
- Identify weak topics (low average ratings)
- Personalize content recommendations
- Track confidence growth
- A/B test lesson effectiveness

---

## 13. 💻 KARTA CODE SNIPPET (Fragment Kodu)

**Kiedy użyć:** Technical documentation, API specs, JSON configuration examples

**Elementy:**
- Code container z syntax highlighting
- Line numbers
- Language badge (JSON, Python, JavaScript, etc.)
- Copy button (one-click clipboard)
- Colored syntax (keywords, strings, numbers, comments)

**Przykład HTML:**
```html
<div class="card" id="card16">
    <h2>💻 Code Snippet - Specyfikacja Techniczna</h2>
    <p>Format JSON ze szczegółową specyfikacją produktu. Skopiuj do dokumentacji technicznej.</p>

    <div class="code-container">
        <div class="code-header">
            <span class="code-lang">JSON - Specyfikacja MXF COS350</span>
            <button class="code-copy-btn" onclick="copyCode()">
                <i data-lucide="copy" style="width: 14px; height: 14px;"></i>
                Kopiuj kod
            </button>
        </div>
        <div class="code-content" id="codeContent">
            <div class="code-line">
                <span class="line-number">1</span>
                <span class="code-text">{</span>
            </div>
            <div class="code-line">
                <span class="line-number">2</span>
                <span class="code-text">  <span class="code-keyword">"productId"</span>: <span class="code-string">"MXF COS350-0"</span>,</span>
            </div>
            <div class="code-line">
                <span class="line-number">3</span>
                <span class="code-text">  <span class="code-keyword">"name"</span>: <span class="code-string">"MX FUEL Cut-Off Saw 350mm"</span>,</span>
            </div>
            <div class="code-line">
                <span class="line-number">4</span>
                <span class="code-text">  <span class="code-keyword">"specifications"</span>: {</span>
            </div>
            <div class="code-line">
                <span class="line-number">5</span>
                <span class="code-text">    <span class="code-keyword">"bladeDiameter"</span>: <span class="code-number">350</span>, <span class="code-comment">// mm</span></span>
            </div>
            <!-- Więcej linii... -->
        </div>
    </div>
</div>
```

**CSS dla Code Snippet:**
```css
.code-container {
    background: #1a1a2e;
    border-radius: 12px;
    overflow: hidden;
    margin: 24px 0;
    border: 2px solid rgba(255, 136, 0, 0.3);
}

.code-header {
    background: rgba(255, 136, 0, 0.1);
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.code-lang {
    font-size: 13px;
    color: #ffd700;
    font-weight: 600;
}

.code-copy-btn {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 6px 12px;
    border-radius: 6px;
    color: white;
    font-size: 13px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.3s ease;
}

.code-copy-btn:hover {
    background: rgba(255, 136, 0, 0.3);
    border-color: #ff8800;
}

.code-content {
    padding: 20px;
    font-family: 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.8;
    overflow-x: auto;
}

.code-line {
    display: flex;
    gap: 16px;
}

.line-number {
    color: rgba(255, 255, 255, 0.3);
    min-width: 30px;
    text-align: right;
    user-select: none;
}

.code-text {
    color: #e0e0e0;
}

.code-keyword {
    color: #00d4ff; /* Cyan dla keys */
}

.code-string {
    color: #00ff88; /* Zielony dla strings */
}

.code-number {
    color: #ffd700; /* Złoty dla numbers */
}

.code-comment {
    color: rgba(255, 255, 255, 0.4); /* Szary dla komentarzy */
    font-style: italic;
}
```

**JavaScript dla Code Snippet:**
```javascript
function copyCode() {
    const codeContent = document.getElementById('codeContent');
    const lines = codeContent.querySelectorAll('.code-text');
    const codeText = Array.from(lines).map(line => line.textContent).join('\n');
    
    navigator.clipboard.writeText(codeText).then(() => {
        const btn = document.querySelector('.code-copy-btn');
        const originalText = btn.innerHTML;
        
        btn.innerHTML = '<i data-lucide="check" style="width: 14px; height: 14px;"></i> Skopiowano!';
        btn.style.background = 'rgba(0, 255, 136, 0.3)';
        
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '';
            lucide.createIcons();
        }, 2000);
    });
}
```

**Use Cases:**
- API documentation
- Configuration examples
- Technical specifications (JSON/YAML)
- Code templates for integration
- Database schemas
- Command-line examples

**Variants:**
- **Language support:** JSON, JavaScript, Python, SQL, YAML, Bash
- **Theme:** Dark mode (current) or light code theme
- **Features:** Line highlighting, diff view (+/-), collapsible sections

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

**Nowe typy interaktywne (opcjonalne):**
✅ **Ranking Card** (8): Drag & drop priorytetyzacja (BHP, procesy)  
✅ **Fill Blanks Card** (9): Uzupełnianie luk w tekście (specs, vocabulary)  
✅ **Matching Pairs Card** (10): Kojarzenie par (produkt↔zastosowanie)  
✅ **True/False Card** (11): Szybki test faktów z natychmiastowym feedbackiem  
✅ **Rating Scale Card** (12): Samoocena wiedzy (skala 1-5)  
✅ **Code Snippet Card** (13): Fragmenty kodu z syntax highlighting  

**Kompletna lista z advanced_card_types_mockup.html:**
1. Drag & Drop (kategorie narzędzi)
2. Calculator (moment obrotowy)
3. Comparison Table (porównanie produktów)
4. Video (embedded player)
5. Role-Play (symulacja rozmowy z klientem)
6. Branching Scenario (wybory → konsekwencje)
7. Timeline/Process (wizualizacja procesu)
8. Before/After Slider (porównanie obrazów)
9. Hotspot Image (klikalne punkty na obrazie)
10. Checklist (task list z progressem)
11. True/False ✅
12. Ranking/Sorting ✅
13. Fill in the Blanks ✅
14. Matching Pairs ✅
15. Rating Scale ✅
16. Code Snippet ✅

**Pamiętaj:**
- Nawigacja: Przyciski Wstecz/Dalej
- Progress bar: `(currentCard / totalCards) * 100%`
- Lucide icons: `lucide.createIcons()` po każdej zmianie DOM
- Total cards: Zaktualizuj `const totalCards = X` w JavaScript
- Drag & Drop: Tylko desktop (mobile: użyj click-based alternatives)

---

**Autor:** GitHub Copilot  
**Data:** 17 stycznia 2026  
**Wersja:** 1.2 (dodano True/False, Rating Scale, Code Snippet - komplet 13 typów kart)
