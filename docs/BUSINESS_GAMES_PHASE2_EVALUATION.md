# 🎯 Business Games - Phase 2: System Oceny Kontraktów

## 📋 Przegląd

Phase 2 wprowadza elastyczny system oceny kontraktów z trzema trybami:
1. **🤖 Ocena AI** - Automatyczna ocena przez model Google Gemini
2. **👨‍💼 Ocena Mistrza Gry** - Ręczna ocena przez Admina
3. **⚡ Heurystyka** - Prosta automatyczna ocena (MVP, obecnie aktywna)

## 🎮 Tryby oceny

### 1️⃣ Ocena AI (🤖)
**Status:** Planowana

**Działanie:**
- Przesłanie treści kontraktu i rozwiązania do Google Gemini
- AI ocenia jakość odpowiedzi według kryteriów kontraktu
- Zwraca ocenę 1-5 gwiazdek + feedback tekstowy
- Automatyczne naliczenie nagrody

**Zalety:**
- ✅ Szczegółowa analiza jakościowa
- ✅ Spersonalizowany feedback
- ✅ Konsystentna ocena według obiektywnych kryteriów
- ✅ Skalowalna (bez limitu użytkowników)

**Wady:**
- ❌ Wymaga API key do Google Gemini
- ❌ Koszt per request (zależny od długości tekstu)
- ❌ Czas odpowiedzi ~3-10 sekund

**Kryteria oceny AI:**
```python
{
    "content_quality": 0-25,      # Merytoryczna wartość treści
    "completeness": 0-25,          # Kompletność odpowiedzi
    "structure": 0-20,             # Struktura i organizacja
    "practicality": 0-20,          # Praktyczne zastosowanie
    "creativity": 0-10             # Innowacyjność rozwiązania
}
# Suma: 0-100 punktów → przeliczenie na 1-5 gwiazdek
```

---

### 2️⃣ Ocena Mistrza Gry (👨‍💼)
**Status:** Planowana

**Działanie:**
- Rozwiązania trafiają do kolejki oczekujących
- Admin loguje się do panelu Business Games Admin
- Przegląda przesłane rozwiązania
- Ocenia według własnej wiedzy i doświadczenia
- Przyznaje 1-5 gwiazdek + opcjonalny komentarz
- System automatycznie nalicza nagrodę

**Zalety:**
- ✅ Pełna kontrola jakości
- ✅ Możliwość edukacyjnego feedbacku
- ✅ Dostosowanie do kontekstu firmy/kursu
- ✅ Brak kosztów API
- ✅ Możliwość oceny niuansów niedostępnych dla AI

**Wady:**
- ❌ Wymaga czasu Admina
- ❌ Opóźnienie w otrzymaniu nagrody
- ❌ Niewykonalne przy dużej liczbie graczy
- ❌ Subiektywność oceny

**Panel Mistrza Gry:**
```
┌─────────────────────────────────────────────┐
│ 📋 Oczekujące Rozwiązania (5)              │
├─────────────────────────────────────────────┤
│ 1. Jan Kowalski - CIQ-KONFLIKT-001         │
│    Przesłane: 2025-10-18 14:30            │
│    [📖 Przejrzyj] [✅ Oceń]                │
├─────────────────────────────────────────────┤
│ 2. Anna Nowak - CIQ-COACHING-001           │
│    Przesłane: 2025-10-18 15:45            │
│    [📖 Przejrzyj] [✅ Oceń]                │
└─────────────────────────────────────────────┘
```

---

### 3️⃣ Heurystyka (⚡)
**Status:** Aktualnie aktywna (MVP)

**Działanie:**
- Prosta ocena oparta na długości tekstu
- Losowy element dla symulacji zmienności
- Instant feedback (bez opóźnień)
- Brak kosztów

**Algorytm:**
```python
def simulate_contract_evaluation(solution, contract):
    word_count = len(solution.split())
    min_words = contract.get("min_slow", 300)
    
    # Bazowa ocena na podstawie długości
    if word_count < min_words * 0.5:
        base_score = 1
    elif word_count < min_words * 0.8:
        base_score = 2
    elif word_count < min_words:
        base_score = 3
    elif word_count < min_words * 1.5:
        base_score = 4
    else:
        base_score = 5
    
    # Dodaj losowość ±1 gwiazdka
    rating = max(1, min(5, base_score + random.randint(-1, 1)))
    return rating
```

**Zalety:**
- ✅ Natychmiastowy rezultat
- ✅ Brak kosztów
- ✅ Proste w utrzymaniu
- ✅ Dobre dla MVP/testów

**Wady:**
- ❌ Brak merytorycznej oceny
- ❌ Łatwe do "oszukania" długim tekstem
- ❌ Brak edukacyjnego feedbacku

---

## 🔧 Implementacja - Konfiguracja

### Panel Admin - Ustawienia Business Games

```python
# config/business_games_settings.py

EVALUATION_MODES = {
    "heuristic": {
        "name": "⚡ Heurystyka",
        "description": "Prosta automatyczna ocena (szybka, darmowa)",
        "enabled": True,
        "requires": []
    },
    "ai": {
        "name": "🤖 Ocena AI",
        "description": "Szczegółowa ocena przez Google Gemini (wolniejsza, płatna)",
        "enabled": False,
        "requires": ["Google Gemini_API_KEY"]
    },
    "game_master": {
        "name": "👨‍💼 Mistrz Gry",
        "description": "Ręczna ocena przez Admina (najlepsza jakość)",
        "enabled": False,
        "requires": ["admin_availability"]
    }
}

# Domyślny tryb
DEFAULT_EVALUATION_MODE = "heuristic"

# Ustawienia AI
AI_EVALUATION_CONFIG = {
    "model": "Geminio-mini",
    "temperature": 0.3,  # Niska temperatura = bardziej konsystentne oceny
    "max_tokens": 500,
    "prompt_template": """
Jesteś ekspertem od Conversational Intelligence i oceniasz rozwiązanie kontraktu konsultingowego.

KONTRAKT:
Tytuł: {contract_title}
Kategoria: {contract_category}
Trudność: {contract_difficulty}/5
Opis: {contract_description}
Wymagania: {contract_requirements}

ROZWIĄZANIE UCZESTNIKA:
{user_solution}

KRYTERIA OCENY (0-100 punktów):
1. Merytoryczna wartość treści (0-25 pkt)
2. Kompletność odpowiedzi (0-25 pkt)
3. Struktura i organizacja (0-20 pkt)
4. Praktyczne zastosowanie (0-20 pkt)
5. Innowacyjność (0-10 pkt)

Oceń rozwiązanie i zwróć JSON:
{{
  "total_score": 0-100,
  "rating": 1-5,
  "feedback": "szczegółowy komentarz",
  "strengths": ["lista mocnych stron"],
  "improvements": ["lista sugestii"]
}}
"""
}

# Ustawienia Mistrza Gry
GAME_MASTER_CONFIG = {
    "queue_enabled": True,
    "notification_email": True,  # Powiadomienie dla admina
    "max_pending_reviews": 50,
    "review_deadline_hours": 48  # SLA dla oceny
}
```

---

## 🎨 UI - Panel Admina

### Widok: Ustawienia Business Games

```python
def show_business_games_admin_settings():
    st.header("⚙️ Ustawienia Business Games")
    
    # Sekcja 1: Wybór trybu oceny
    st.subheader("🎯 Tryb Oceny Kontraktów")
    
    current_mode = load_business_settings().get("evaluation_mode", "heuristic")
    
    mode_options = {
        "heuristic": "⚡ Heurystyka (Automatyczna, szybka)",
        "ai": "🤖 Ocena AI (Google Gemini, szczegółowa)",
        "game_master": "👨‍💼 Mistrz Gry (Ręczna ocena przez Admina)"
    }
    
    selected_mode = st.selectbox(
        "Wybierz tryb oceny:",
        options=list(mode_options.keys()),
        format_func=lambda x: mode_options[x],
        index=list(mode_options.keys()).index(current_mode)
    )
    
    # Info o wybranym trybie
    if selected_mode == "heuristic":
        st.info("""
        **⚡ Heurystyka:**
        - Natychmiastowa ocena po przesłaniu
        - Oparta na długości i strukturze tekstu
        - Brak kosztów
        - Dobra dla testów i MVP
        """)
    
    elif selected_mode == "ai":
        st.warning("""
        **🤖 Ocena AI:**
        - Wymaga klucza API Google Gemini
        - Koszt: ~$0.01-0.05 per ocena
        - Czas oceny: 5-10 sekund
        - Szczegółowy feedback dla uczestników
        """)
        
        # Konfiguracja API
        api_key = st.text_input("Google Gemini API Key:", type="password")
        if api_key:
            st.success("✅ Klucz API skonfigurowany")
        
        # Test połączenia
        if st.button("🧪 Testuj połączenie z Google Gemini"):
            try:
                # Test API
                test_ai_connection(api_key)
                st.success("✅ Połączenie działa!")
            except Exception as e:
                st.error(f"❌ Błąd: {e}")
    
    elif selected_mode == "game_master":
        st.success("""
        **👨‍💼 Mistrz Gry:**
        - Pełna kontrola jakości
        - Rozwiązania czekają na Twoją ocenę
        - Możesz dodawać spersonalizowany feedback
        - Zalecane dla małych grup (do 20 osób)
        """)
        
        # Statystyki kolejki
        pending_count = get_pending_reviews_count()
        if pending_count > 0:
            st.warning(f"⏳ Oczekujące oceny: **{pending_count}**")
            if st.button("📋 Przejdź do kolejki ocen"):
                st.session_state.admin_tab = "game_master_queue"
                st.rerun()
    
    # Zapisz ustawienia
    if st.button("💾 Zapisz ustawienia", type="primary"):
        save_business_settings({"evaluation_mode": selected_mode})
        st.success("✅ Ustawienia zapisane!")
        st.rerun()
```

---

### Widok: Kolejka Mistrza Gry

```python
def show_game_master_queue():
    st.header("👨‍💼 Kolejka Ocen - Mistrz Gry")
    
    pending_reviews = get_pending_contract_reviews()
    
    if not pending_reviews:
        st.success("🎉 Brak oczekujących rozwiązań do oceny!")
        return
    
    st.info(f"📋 Oczekujące rozwiązania: **{len(pending_reviews)}**")
    
    # Filtry
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox("Kategoria:", ["Wszystkie", "Konflikt", "Coaching", "Leadership"])
    with col2:
        filter_difficulty = st.selectbox("Trudność:", ["Wszystkie", "1", "2", "3", "4", "5"])
    with col3:
        sort_by = st.selectbox("Sortuj:", ["Najstarsze", "Najnowsze", "Trudność"])
    
    # Lista rozwiązań
    for review in pending_reviews:
        with st.expander(f"📝 {review['username']} - {review['contract_title']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Użytkownik:** {review['username']}")
                st.markdown(f"**Kontrakt:** {review['contract_title']}")
                st.markdown(f"**Kategoria:** {review['contract_category']}")
                st.markdown(f"**Trudność:** {'⭐' * review['contract_difficulty']}")
                st.markdown(f"**Przesłano:** {review['submitted_at']}")
            
            with col2:
                st.metric("Długość", f"{review['word_count']} słów")
                st.metric("Czeka", f"{review['waiting_hours']}h")
            
            # Opis kontraktu
            st.markdown("---")
            st.markdown("**📋 Opis Kontraktu:**")
            st.markdown(review['contract_description'])
            
            # Rozwiązanie uczestnika
            st.markdown("**📝 Rozwiązanie Uczestnika:**")
            st.text_area(
                "Treść rozwiązania:",
                value=review['solution'],
                height=300,
                disabled=True,
                key=f"solution_{review['id']}"
            )
            
            # Formularz oceny
            st.markdown("---")
            st.markdown("### ⭐ Twoja Ocena")
            
            rating = st.slider(
                "Oceń jakość rozwiązania:",
                min_value=1,
                max_value=5,
                value=3,
                key=f"rating_{review['id']}"
            )
            
            feedback = st.text_area(
                "Komentarz dla uczestnika (opcjonalny):",
                placeholder="Mocne strony:\n- ...\n\nDo poprawy:\n- ...",
                height=150,
                key=f"feedback_{review['id']}"
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("✅ Zatwierdź ocenę", key=f"approve_{review['id']}", type="primary"):
                    submit_game_master_review(
                        review_id=review['id'],
                        rating=rating,
                        feedback=feedback,
                        admin_username=st.session_state.username
                    )
                    st.success(f"✅ Ocena zatwierdzona! {review['username']} otrzymał {rating}⭐")
                    st.rerun()
            
            with col2:
                if st.button("⏭️ Pomiń na później", key=f"skip_{review['id']}"):
                    st.info("Przeskoczono do następnego")
                    continue
```

---

## 🔌 Backend - Funkcje oceny

### Struktura plików

```
utils/
  business_game_evaluation.py  # Nowy moduł oceny
  business_game.py              # Istniejący moduł (dodane wywołania)
  
config/
  business_games_settings.py   # Konfiguracja trybów oceny
  
views/
  admin_business_games.py       # Nowy panel admina
```

### Kod: business_game_evaluation.py

```python
"""
Business Games - System Oceny Kontraktów
Obsługuje 3 tryby: Heurystyka, AI, Mistrz Gry
"""

import json
import random
from datetime import datetime
from typing import Dict, Tuple
import Google Gemini

from config.business_games_settings import (
    EVALUATION_MODES, 
    AI_EVALUATION_CONFIG,
    DEFAULT_EVALUATION_MODE
)

# =============================================================================
# GŁÓWNA FUNKCJA OCENY
# =============================================================================

def evaluate_contract_solution(
    user_data: Dict,
    contract: Dict,
    solution: str,
    evaluation_mode: str = None
) -> Tuple[int, str, Dict]:
    """
    Ocenia rozwiązanie kontraktu według wybranego trybu
    
    Args:
        user_data: Dane użytkownika
        contract: Dane kontraktu
        solution: Tekst rozwiązania
        evaluation_mode: "heuristic" / "ai" / "game_master"
    
    Returns:
        (rating: 1-5, feedback: str, details: dict)
    """
    if evaluation_mode is None:
        evaluation_mode = get_active_evaluation_mode()
    
    if evaluation_mode == "heuristic":
        return evaluate_heuristic(solution, contract)
    
    elif evaluation_mode == "ai":
        return evaluate_with_ai(solution, contract)
    
    elif evaluation_mode == "game_master":
        return queue_for_game_master(user_data, contract, solution)
    
    else:
        # Fallback do heurystyki
        return evaluate_heuristic(solution, contract)


# =============================================================================
# TRYB 1: HEURYSTYKA (obecny system)
# =============================================================================

def evaluate_heuristic(solution: str, contract: Dict) -> Tuple[int, str, Dict]:
    """Prosta ocena oparta na długości tekstu"""
    word_count = len(solution.split())
    min_words = contract.get("min_slow", 300)
    
    # Bazowa ocena
    if word_count < min_words * 0.5:
        base_score = 1
    elif word_count < min_words * 0.8:
        base_score = 2
    elif word_count < min_words:
        base_score = 3
    elif word_count < min_words * 1.5:
        base_score = 4
    else:
        base_score = 5
    
    # Losowość
    rating = max(1, min(5, base_score + random.randint(-1, 1)))
    
    feedback = f"Rozwiązanie zawiera {word_count} słów. Automatyczna ocena: {rating}/5 ⭐"
    
    details = {
        "method": "heuristic",
        "word_count": word_count,
        "base_score": base_score,
        "final_rating": rating
    }
    
    return rating, feedback, details


# =============================================================================
# TRYB 2: OCENA AI
# =============================================================================

def evaluate_with_ai(solution: str, contract: Dict) -> Tuple[int, str, Dict]:
    """Ocena przez Google Gemini"""
    try:
        # Przygotuj prompt
        prompt = AI_EVALUATION_CONFIG["prompt_template"].format(
            contract_title=contract["tytul"],
            contract_category=contract["kategoria"],
            contract_difficulty=contract["poziom_trudnosci"],
            contract_description=contract["opis"],
            contract_requirements=contract.get("wymagania", ""),
            user_solution=solution
        )
        
        # Wywołaj Google Gemini
        response = Google Gemini.ChatCompletion.create(
            model=AI_EVALUATION_CONFIG["model"],
            messages=[
                {"role": "system", "content": "Jesteś ekspertem od Conversational Intelligence oceniającym kontrakty konsultingowe."},
                {"role": "user", "content": prompt}
            ],
            temperature=AI_EVALUATION_CONFIG["temperature"],
            max_tokens=AI_EVALUATION_CONFIG["max_tokens"]
        )
        
        # Parse odpowiedzi
        result = json.loads(response.choices[0].message.content)
        
        rating = result["rating"]
        feedback = result["feedback"]
        details = {
            "method": "ai",
            "total_score": result["total_score"],
            "strengths": result.get("strengths", []),
            "improvements": result.get("improvements", []),
            "ai_model": AI_EVALUATION_CONFIG["model"]
        }
        
        return rating, feedback, details
        
    except Exception as e:
        # Fallback do heurystyki w razie błędu
        print(f"AI Evaluation Error: {e}")
        return evaluate_heuristic(solution, contract)


# =============================================================================
# TRYB 3: MISTRZ GRY (kolejka oczekujących)
# =============================================================================

def queue_for_game_master(
    user_data: Dict,
    contract: Dict,
    solution: str
) -> Tuple[int, str, Dict]:
    """
    Dodaje rozwiązanie do kolejki oczekujących na ocenę Mistrza Gry
    Zwraca tymczasową ocenę "pending"
    """
    from data.users import load_user_data, save_user_data
    
    review_id = f"review_{user_data['username']}_{contract['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Dodaj do kolejki
    pending_review = {
        "id": review_id,
        "username": user_data["username"],
        "contract_id": contract["id"],
        "contract_title": contract["tytul"],
        "contract_category": contract["kategoria"],
        "contract_difficulty": contract["poziom_trudnosci"],
        "contract_description": contract["opis"],
        "solution": solution,
        "word_count": len(solution.split()),
        "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "pending",
        "rating": None,
        "feedback": None,
        "reviewed_by": None,
        "reviewed_at": None
    }
    
    # Zapisz do pliku game_master_queue.json
    queue_file = "game_master_queue.json"
    try:
        with open(queue_file, 'r') as f:
            queue = json.load(f)
    except FileNotFoundError:
        queue = []
    
    queue.append(pending_review)
    
    with open(queue_file, 'w') as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    
    feedback = "✅ Rozwiązanie przesłane! Oczekuje na ocenę Mistrza Gry. Otrzymasz powiadomienie gdy zostanie ocenione."
    
    details = {
        "method": "game_master",
        "review_id": review_id,
        "status": "pending"
    }
    
    return 0, feedback, details  # rating=0 oznacza "pending"


def submit_game_master_review(
    review_id: str,
    rating: int,
    feedback: str,
    admin_username: str
) -> bool:
    """Admin zatwierdza ocenę"""
    queue_file = "game_master_queue.json"
    
    try:
        with open(queue_file, 'r') as f:
            queue = json.load(f)
    except FileNotFoundError:
        return False
    
    # Znajdź review
    for review in queue:
        if review["id"] == review_id and review["status"] == "pending":
            # Zaktualizuj status
            review["status"] = "reviewed"
            review["rating"] = rating
            review["feedback"] = feedback
            review["reviewed_by"] = admin_username
            review["reviewed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Zapisz kolejkę
            with open(queue_file, 'w') as f:
                json.dump(queue, f, indent=2, ensure_ascii=False)
            
            # Finalizuj kontrakt użytkownika
            finalize_game_master_contract(review)
            
            return True
    
    return False


def finalize_game_master_contract(review: Dict):
    """
    Finalizuje kontrakt po ocenie Mistrza Gry
    Dodaje monety i reputację użytkownikowi
    """
    from data.users import load_user_data, save_user_data
    from utils.business_game import calculate_contract_reward
    
    users_data = load_user_data()
    username = review["username"]
    
    if username not in users_data:
        return
    
    user_data = users_data[username]
    business_data = user_data.get("business_game", {})
    
    # Znajdź aktywny kontrakt
    for contract in business_data["contracts"]["active"]:
        if contract["id"] == review["contract_id"]:
            # Oblicz nagrodę
            reward = calculate_contract_reward(contract, review["rating"], business_data)
            
            # Dodaj monety i reputację
            user_data['degencoins'] = user_data.get('degencoins', 0) + reward["coins"]
            business_data["firm"]["reputation"] += reward["reputation"]
            business_data["stats"]["total_revenue"] += reward["coins"]
            
            # Przenieś do completed
            completed_contract = contract.copy()
            completed_contract["solution"] = review["solution"]
            completed_contract["rating"] = review["rating"]
            completed_contract["feedback"] = review["feedback"]
            completed_contract["reward"] = reward
            completed_contract["completed_date"] = review["reviewed_at"]
            completed_contract["evaluated_by"] = review["reviewed_by"]
            completed_contract["evaluation_method"] = "game_master"
            
            business_data["contracts"]["completed"].append(completed_contract)
            business_data["contracts"]["active"].remove(contract)
            
            # Zapisz
            user_data["business_game"] = business_data
            users_data[username] = user_data
            save_user_data(users_data)
            
            break


# =============================================================================
# FUNKCJE POMOCNICZE
# =============================================================================

def get_active_evaluation_mode() -> str:
    """Pobiera aktualny tryb oceny z konfiguracji"""
    try:
        with open("config/business_games_active_mode.json", 'r') as f:
            config = json.load(f)
            return config.get("evaluation_mode", DEFAULT_EVALUATION_MODE)
    except FileNotFoundError:
        return DEFAULT_EVALUATION_MODE


def get_pending_reviews_count() -> int:
    """Liczba oczekujących ocen"""
    try:
        with open("game_master_queue.json", 'r') as f:
            queue = json.load(f)
            return len([r for r in queue if r["status"] == "pending"])
    except FileNotFoundError:
        return 0


def get_pending_contract_reviews() -> list:
    """Pobiera listę oczekujących rozwiązań"""
    try:
        with open("game_master_queue.json", 'r') as f:
            queue = json.load(f)
            pending = [r for r in queue if r["status"] == "pending"]
            
            # Dodaj waiting_hours
            for review in pending:
                submitted = datetime.strptime(review["submitted_at"], "%Y-%m-%d %H:%M:%S")
                waiting_hours = (datetime.now() - submitted).total_seconds() / 3600
                review["waiting_hours"] = int(waiting_hours)
            
            return pending
    except FileNotFoundError:
        return []
```

---

## 📊 Porównanie trybów

| Cecha | Heurystyka ⚡ | AI 🤖 | Mistrz Gry 👨‍💼 |
|-------|--------------|--------|-----------------|
| **Czas oceny** | Instant | 5-10s | 1-48h |
| **Koszt** | Darmowe | $0.01-0.05 | Czas admina |
| **Jakość** | Niska | Wysoka | Najwyższa |
| **Feedback** | Brak | Szczegółowy | Spersonalizowany |
| **Skalowalność** | ∞ | ∞ | ~20 osób |
| **Wymaga** | - | API key | Admin availability |

---

## 🚀 Plan wdrożenia

### Faza 1: Przygotowanie (1 tydzień)
- [ ] Stworzenie modułu `business_game_evaluation.py`
- [ ] Konfiguracja `business_games_settings.py`
- [ ] Panel admina - wybór trybu
- [ ] Plik kolejki `game_master_queue.json`

### Faza 2: Implementacja AI (1 tydzień)
- [ ] Integracja z Google Gemini API
- [ ] Optymalizacja promptu oceny
- [ ] Testy jakości ocen AI
- [ ] Obsługa błędów i fallback

### Faza 3: Panel Mistrza Gry (1 tydzień)
- [ ] Widok kolejki rozwiązań
- [ ] Formularz oceny
- [ ] Finalizacja kontraktu po ocenie
- [ ] Powiadomienia email

### Faza 4: Testy i optymalizacja (3 dni)
- [ ] Testy wszystkich trybów
- [ ] Porównanie jakości ocen
- [ ] Optymalizacja UX
- [ ] Dokumentacja użytkownika

---

## 💡 Przyszłe możliwości

1. **Hybrydowy tryb:** AI + Mistrz Gry (AI ocenia, Admin weryfikuje)
2. **Multi-evaluator:** Kilku oceniających (średnia ocen)
3. **Peer review:** Uczestnicy oceniają nawzajem
4. **Ranking oceniających:** Statystyki Mistrzów Gry
5. **AI training:** Użyj ocen Mistrza Gry do trenowania AI

---

## 📝 Notatki implementacyjne

**Priorytet:** Średni (Phase 2 - po stabilizacji MVP)

**Estymacja:** ~3 tygodnie pracy

**Zależności:**
- Google Gemini API key (dla trybu AI)
- Panel admina (częściowo istniejący)
- System powiadomień (opcjonalny)

**Ryzyka:**
- Koszt API przy dużej liczbie kontraktów
- Opóźnienia w ocenie przez Mistrza Gry
- Niezgodność ocen między trybami

---

## ✅ Status Implementacji

**Status:** ✅ **ZAIMPLEMENTOWANE!**  
**Data utworzenia:** 18 października 2025  
**Data implementacji:** 19 października 2025  
**Ostatnia aktualizacja:** 19 października 2025

### 🎯 Co zostało zaimplementowane:

✅ **Moduł konfiguracji** (`config/business_games_settings.py`)
- Definicje 3 trybów oceny
- Konfiguracja AI (Google Gemini)
- Ustawienia kolejki Mistrza Gry
- Parametry heurystyki

✅ **Moduł oceny** (`utils/business_game_evaluation.py`)
- `evaluate_contract_solution()` - główna funkcja
- `evaluate_heuristic()` - ocena automatyczna
- `evaluate_with_ai()` - ocena przez Google Gemini (wymaga API key)
- `queue_for_game_master()` - dodawanie do kolejki
- `submit_game_master_review()` - zatwierdzanie oceny przez Admina
- Funkcje pomocnicze dla kolejki i konfiguracji

✅ **Integracja z Business Game** (`utils/business_game.py`)
- `submit_contract_solution()` zaktualizowane
- Obsługa pending_review dla trybu Mistrza Gry
- Zapisywanie feedback i szczegółów oceny

✅ **Panel Administracyjny** (`views/admin.py`)
- Nowa zakładka "Business Games" w panelu admina
- **Tab 1: Ustawienia Oceny**
  - Wybór trybu (Heurystyka/AI/Mistrz Gry)
  - Konfiguracja API Google Gemini
  - Status i statystyki
- **Tab 2: Kolejka Mistrza Gry**
  - Lista oczekujących rozwiązań
  - Formularz oceny (gwiazdki + feedback)
  - Filtry i sortowanie
- **Tab 3: Statystyki**
  - Liczba ocen (wszystkie/pending/reviewed)
  - Średnia ocena
  - Aktualny tryb

✅ **Testy** (`test_evaluation_system.py`)
- Test 1: Heurystyka ✅
- Test 2: Kolejka Mistrza Gry ✅
- Test 3: Zmiana trybów ✅
- Test 4: Integracja ✅

### 📋 Instrukcja użycia:

1. **Logowanie jako Admin:**
   - Zaloguj się jako użytkownik z uprawnieniami admina
   - Przejdź do panelu administratora
   - Wybierz zakładkę "Business Games"

2. **Wybór trybu oceny:**
   - Tab "🎯 Ustawienia Oceny"
   - Wybierz jeden z 3 trybów
   - Zapisz ustawienia

3. **Tryb Heurystyka (domyślny):**
   - Automatycznie aktywny
   - Nie wymaga konfiguracji
   - Natychmiastowa ocena

4. **Tryb AI:**
   - Dodaj klucz API Google Gemini w panelu admina
   - Zapisz klucz
   - Zmień tryb na "AI"
   - Kontrakty będą oceniane przez Gemini

5. **Tryb Mistrz Gry:**
   - Zmień tryb na "Mistrz Gry"
   - Użytkownicy przesyłają rozwiązania → trafiają do kolejki
   - Admin przegląda w Tab "👨‍💼 Kolejka Mistrza Gry"
   - Oceń każde rozwiązanie (1-5⭐ + feedback)
   - Po zatwierdzeniu użytkownik dostaje monety i reputację

### 🔧 Pliki do wdrożenia:

```
BVA/
├── config/
│   └── business_games_settings.py      [NOWY]
├── utils/
│   └── business_game_evaluation.py     [NOWY]
│   └── business_game.py                [ZMODYFIKOWANY]
├── views/
│   └── admin.py                        [ZMODYFIKOWANY]
├── docs/
│   └── BUSINESS_GAMES_PHASE2_EVALUATION.md
└── test_evaluation_system.py           [NOWY - opcjonalny]
```

### ⚠️ Wymagania:

- **Dla trybu AI:** `pip install Google Gemini` + klucz API Google Gemini
- **Dla trybu Mistrz Gry:** Admin musi regularnie sprawdzać kolejkę
- **Ogólne:** Python 3.8+, Streamlit, wszystkie inne zależności projektu

---
