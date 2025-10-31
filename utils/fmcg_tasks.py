"""
FMCG Game - System zadań (Onboarding Quests)
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Tuple
import os


def get_gemini_api_key():
    """Pobierz klucz API Gemini z Streamlit secrets lub env variable"""
    # Najpierw sprawdź Streamlit secrets
    try:
        # Próbuj najpierw z sekcji API_KEYS
        if hasattr(st, 'secrets') and 'API_KEYS' in st.secrets and 'GEMINI_API_KEY' in st.secrets['API_KEYS']:
            print("✅ Znaleziono klucz API w st.secrets['API_KEYS']['GEMINI_API_KEY']")
            return st.secrets['API_KEYS']['GEMINI_API_KEY']
        # Fallback do top-level GEMINI_API_KEY
        elif hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
            print("✅ Znaleziono klucz API w st.secrets['GEMINI_API_KEY']")
            return st.secrets['GEMINI_API_KEY']
    except Exception as e:
        print(f"⚠️ Nie można odczytać st.secrets: {e}")
    
    # Fallback do zmiennej środowiskowej
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        print("✅ Znaleziono klucz API w os.environ")
    return env_key


def evaluate_task_with_ai(task_id: str, submission_text: str, task_data: Dict) -> Tuple[str, bool]:
    """
    Ewaluacja zadania przy użyciu Gemini 2.0 Flash
    
    Args:
        task_id: ID zadania
        submission_text: Tekst zgłoszony przez użytkownika
        task_data: Dane zadania z ONBOARDING_TASKS
    
    Returns:
        Tuple (feedback_text, is_accepted)
    """
    print(f"🔍 evaluate_task_with_ai wywołane dla {task_id}")
    print(f"🔍 Submission length: {len(submission_text)} chars")
    
    api_key = get_gemini_api_key()
    print(f"🔍 API key: {'FOUND' if api_key else 'NOT FOUND'}")
    
    if not api_key:
        print("⚠️ Brak klucza API Gemini - używam static feedback")
        # Fallback to static feedback if no API key
        return get_static_feedback(task_id, submission_text), True
    
    print(f"✅ Klucz API Gemini dostępny - używam AI evaluation dla {task_id}")
    
    try:
        print("🔍 Importuję google.generativeai...")
        import google.generativeai as genai
        
        print("🔍 Konfiguruję genai...")
        genai.configure(api_key=api_key)
        
        print("🔍 Tworzę model gemini-2.0-flash-exp...")
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Build evaluation prompt
        prompt = f"""Jesteś mentorem w grze symulacyjnej sprzedaży FMCG. Oceniasz wykonanie zadania przez początkującego handlowca.

**ZADANIE:**
{task_data['title']}

**OPIS ZADANIA:**
{task_data['description']}

**KRYTERIA SUKCESU:**
{chr(10).join(f"- {criterion}" for criterion in task_data['success_criteria'])}

**ZGŁOSZENIE UŻYTKOWNIKA:**
{submission_text}

**INSTRUKCJE OCENY:**
1. Przeanalizuj czy zgłoszenie spełnia wszystkie kryteria sukcesu
2. Oceń jakość, kompletność i praktyczność rozwiązania
3. Sprawdź czy użytkownik zrozumiał cel zadania

**FORMAT FEEDBACKU:**

Jeśli zadanie ZAAKCEPTOWANE (spełnia wszystkie kryteria):
```
ACCEPT
✅ **Świetna robota!**

**Co zrobiłeś dobrze:**
- [konkretne punkty co było OK]
- [użyj emoji ✅]

💡 **Następny krok:**
[co powinien zrobić dalej]

🎯 **Wskazówka praktyczna:**
[praktyczna rada do zastosowania w grze]
```

Jeśli zadanie WYMAGA POPRAWY (nie spełnia kryteriów):
```
REVISE
⚠️ **Dobre rozpoczęcie, ale wymaga poprawek**

**Co jest OK:**
✅ [co było dobre]

**Co wymaga poprawy:**
❌ [konkretne braki - max 3 punkty]
❌ [wskaż co dokładnie poprawić]

💡 **Jak poprawić:**
1. [konkretna instrukcja]
2. [konkretna instrukcja]

🔄 **Możesz poprawić i wysłać ponownie.**
```

**WAŻNE:**
- Feedback w języku polskim
- Konkretny i merytoryczny (nie ogólniki!)
- Zachęcający (to gra edukacyjna!)
- Pierwsza linia MUSI być: "ACCEPT" lub "REVISE"
- Używaj emoji dla czytelności
- Maksymalnie 150 słów

Wygeneruj feedback:"""

        # Generate feedback
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,  # Balanced creativity
                top_p=0.9,
                top_k=40,
                max_output_tokens=400,
            )
        )
        
        feedback_text = response.text.strip()
        
        # Parse decision (first line)
        first_line = feedback_text.split('\n')[0].strip().upper()
        is_accepted = "ACCEPT" in first_line
        
        print(f"🔍 AI Response first line: {first_line}")
        print(f"🔍 Decision: {'ACCEPTED' if is_accepted else 'REVISE'}")
        
        # Remove decision line from feedback
        feedback_lines = feedback_text.split('\n')[1:]
        clean_feedback = '\n'.join(feedback_lines).strip()
        
        print(f"🔍 Clean feedback length: {len(clean_feedback)} chars")
        
        return clean_feedback, is_accepted
        
    except Exception as e:
        print(f"❌ Błąd AI evaluation: {e}")
        import traceback
        traceback.print_exc()
        # Fallback to static
        return get_static_feedback(task_id, submission_text), True


# Definicja zadań onboardingowych
ONBOARDING_TASKS = {
    "task_001": {
        "id": "task_001",
        "title": "📊 Segmentacja ABC terytorium",
        "description": """
        Przeanalizuj listę klientów i podziel ich na kategorie A/B/C według potencjału sprzedażowego.
        
        **Wytyczne:**
        - **Kategoria A** (Kluczowi): 20% klientów = 80% potencjału (duże sklepy, 80-150 m²)
        - **Kategoria B** (Potencjalni): 30% klientów = 15% potencjału (średnie, 40-80 m²)
        - **Kategoria C** (Małe): 50% klientów = 5% potencjału (małe, 20-40 m²)
        
        **Alokacja czasu:**
        - A: 60% czasu
        - B: 30% czasu
        - C: 10% czasu
        """,
        "required_article": "🗺️ Planowanie terytorium sprzedażowego",
        "order": 1,
        "input_type": "textarea",
        "placeholder": """Przykład:

KATEGORIA A (4 sklepy - 20%):
- Sklep "Osiedlowy" ul. Puławska 120 (150 m²) - duży ruch, wysokie obroty
- Sklep "Centrum" ul. Marszałkowska 80 (120 m²) - lokalizacja premium
...

KATEGORIA B (6 sklepów - 30%):
- Sklep "Wiśniowa" ul. Wiśniowa 5 (60 m²) - stabilny, potencjał wzrostu
...

KATEGORIA C (10 sklepów - 50%):
- Mały sklep ul. Kwiatowa 12 (30 m²) - ograniczony budżet
...

PLAN CZASU:
- Kategoria A: 60% (3-4 wizyty/mies na sklep)
- Kategoria B: 30% (1-2 wizyty/mies)
- Kategoria C: 10% (raz na 2-3 mies)
        """,
        "success_criteria": [
            "Podział na 3 kategorie (A/B/C)",
            "Proporcje zbliżone do 20/30/50",
            "Uwzględnienie wielkości sklepów",
            "Plan alokacji czasu (60/30/10)"
        ]
    },
    
    "task_002": {
        "id": "task_002",
        "title": "🗺️ Plan tygodnia - Routing i klasteryzacja",
        "description": """
        Zaplanuj trasówkę na pierwszy tydzień pracy. Pogrupuj sklepy geograficznie w klastry 
        i przypisz je do konkretnych dni tygodnia.
        
        **Wytyczne:**
        - Sklepy w jednym klastrze powinny być blisko siebie (max 3-5 km)
        - Jeden dzień = jeden klaster (unikaj krzyżowania się po mieście)
        - 5-6 wizyt dziennie (początkujący handlowiec)
        - Zaczynaj od klientów B i C (Quick Wins First!)
        
        **Zasada:** Klasteryzacja > Chaos (oszczędność 100 km dziennie!)
        """,
        "required_article": "🗺️ Planowanie terytorium sprzedażowego",
        "order": 2,
        "input_type": "textarea",
        "placeholder": """Przykład:

KLASTER 1: Mokotów Zachód (Poniedziałki)
1. Sklep B1 - ul. Puławska 50
2. Sklep B2 - ul. Wiśniowa 12
3. Sklep C1 - ul. Konstruktorska 8
4. Sklep C2 - ul. Wołoska 15
5. Sklep C3 - ul. Racławicka 22
Dystans: ~20 km | Wizyty: 5

KLASTER 2: Ursynów (Wtorki)
1. Sklep B3 - al. KEN 80
2. Sklep C4 - ul. Hawajska 12
...

STRATEGIA PIERWSZEGO TYGODNIA:
- Poniedziałek-Środa: Klienci B i C (Quick Wins)
- Czwartek-Piątek: Pierwsi klienci A (z referencjami)
        """,
        "success_criteria": [
            "Klastry geograficzne (sklepy blisko siebie)",
            "Plan PN-PT z przypisanymi sklepami",
            "5-6 wizyt dziennie",
            "Strategia Quick Wins First (B/C przed A)"
        ]
    },
    
    "task_003": {
        "id": "task_003",
        "title": "🎤 Elevator Pitch - Przedstawienie firmy",
        "description": """
        Napisz krótkie (30 sekund), profesjonalne przedstawienie firmy FreshLife i Twojej oferty.
        
        **Struktura:**
        1. Kim jesteś? (imię, firma)
        2. Co robicie? (branża, specjalizacja)
        3. Jaka jest wartość? (USP - unique selling proposition)
        4. Social proof (liczby, referencje)
        5. Call to action (pytanie otwarte)
        
        **Wymagania:**
        - Długość: 25-35 sekund (około 60-80 słów)
        - Konkretne korzyści (nie ogólniki!)
        - Kończy się pytaniem otwartym
        - Brzmi naturalnie (nie jak reklama)
        """,
        "required_article": "🗺️ Planowanie terytorium sprzedażowego",
        "order": 3,
        "input_type": "textarea",
        "placeholder": """Przykład:

"Dzień dobry! Jestem [Twoje imię] z FreshLife. Specjalizujemy się w dystrybucji produktów FMCG dla małych i średnich sklepów. 

Naszą mocną stroną jest terminowość dostaw - 98% on-time delivery - oraz elastyczność. Dowozimy już od 10 sztuk, podczas gdy konkurencja wymaga minimum 50. 

Współpracujemy z ponad 120 sklepami w Warszawie. 

Mogę zadać kilka pytań o Pana biznes?"

[Twoja wersja tutaj...]
        """,
        "success_criteria": [
            "Odpowiednia długość (60-80 słów)",
            "Zawiera USP (unikalną wartość)",
            "Wspomina social proof (liczby)",
            "Kończy się pytaniem otwartym"
        ]
    }
}

def get_task_status(session_state, task_id):
    """Sprawdź status zadania"""
    if "completed_tasks" not in session_state:
        session_state.completed_tasks = {}
    
    return session_state.completed_tasks.get(task_id, {
        "status": "not_started",  # not_started, submitted, completed
        "submission": None,
        "feedback": None,
        "submitted_at": None
    })

def submit_task(session_state, task_id, submission_text):
    """Zapisz zgłoszenie zadania"""
    if "completed_tasks" not in session_state:
        session_state.completed_tasks = {}
    
    session_state.completed_tasks[task_id] = {
        "status": "submitted",
        "submission": submission_text,
        "feedback": None,
        "submitted_at": datetime.now().isoformat()
    }

def get_static_feedback(task_id, submission_text):
    """
    Mockup - statyczny feedback (póki co bez AI)
    W przyszłości: OpenAI API z analizą tekstu
    """
    
    feedback_templates = {
        "task_001": {
            "good": """
✅ **Świetna robota!**

**Segmentacja ABC:**
✅ Poprawnie podzieliłeś klientów na 3 kategorie
✅ Proporcje zbliżone do zasady 80/20
✅ Uwzględniłeś wielkość sklepów i potencjał
✅ Plan alokacji czasu zgodny z wytycznymi (60/30/10)

💡 **Następny krok:**
Przejdź do zadania 2: Planowanie trasówki (routing)

🎯 **Wskazówka praktyczna:**
W grze możesz teraz zobaczyć swoich klientów w Dashboard → Analiza terytorium. 
Zastosuj swoją segmentację ABC w praktyce!
            """,
            "medium": """
✅ **Dobry start, ale można poprawić:**

**Co jest OK:**
✅ Podział na 3 kategorie
✅ Uwzględniłeś niektóre kryteria

⚠️ **Co wymaga poprawy:**
❌ Proporcje nie zgadzają się z zasadą 80/20
   - Kategoria A powinna być ~20% klientów (nie więcej!)
   - Kategoria C powinna być ~50% klientów

💡 **Wskazówka:**
Przeczytaj ponownie sekcję "Segmentacja ABC" w artykule. 
Pamiętaj: 20% największych sklepów = 80% Twoich przyszłych obrotów!

🔄 **Możesz poprawić i wysłać ponownie.**
            """,
            "poor": """
⚠️ **Wymaga znacznych poprawek**

❌ **Główne problemy:**
- Brak wyraźnego podziału na kategorie A/B/C
- Nie uwzględniono wielkości sklepów
- Brak planu alokacji czasu

💡 **Jak poprawić:**
1. Przeczytaj artykuł "Planowanie terytorium sprzedażowego" (sekcja Analiza)
2. Podziel klientów według wielkości i potencjału:
   - A: duże sklepy (80-150 m²) = 20% klientów
   - B: średnie (40-80 m²) = 30% klientów
   - C: małe (20-40 m²) = 50% klientów
3. Zaplanuj czas: 60% na A, 30% na B, 10% na C

🔄 **Spróbuj ponownie - to podstawa skutecznej sprzedaży!**
            """
        },
        
        "task_002": {
            "good": """
✅ **Doskonały plan trasówki!**

**Routing i klasteryzacja:**
✅ Sklepy pogrupowane geograficznie
✅ Jeden dzień = jeden klaster (oszczędność czasu i paliwa!)
✅ 5-6 wizyt dziennie (realistyczny plan)
✅ Strategia Quick Wins First - zaczynasz od B i C

💡 **Przewaga:**
Dzięki klasteryzacji oszczędzasz ~100 km i 3 godziny dziennie vs chaotyczne jeżdżenie!

🎯 **Następny krok:**
Zadanie 3: Przygotuj elevator pitch

⚡ **W grze:**
Możesz teraz planować wizyty w Dashboard → Zaplanuj tydzień
            """,
            "medium": """
✅ **Dobry kierunek, drobne poprawki:**

**Co jest OK:**
✅ Próba grupowania geograficznego
✅ Przypisanie sklepów do dni

⚠️ **Co poprawić:**
❌ Niektóre klastry są zbyt rozproszone (sklepy po różnych dzielnicach)
❌ Za dużo/mało wizyt dziennie (cel: 5-6 dla początkującego)

💡 **Wskazówka:**
Sklepy w jednym klastrze powinny być w promieniu 3-5 km. 
Sprawdź lokalizacje i zgrupuj ponownie.

🔄 **Popraw klasteryzację i wyślij ponownie.**
            """,
            "poor": """
⚠️ **Plan wymaga przebudowy**

❌ **Główne problemy:**
- Brak klasteryzacji geograficznej (chaos!)
- Sklepy z różnych dzielnic w jednym dniu
- Brak strategii Quick Wins First

💡 **Jak poprawić:**
1. Przeczytaj sekcję "Routing" w artykule
2. Pogrupuj sklepy według dzielnicy/rejonu
3. Przypisz jeden klaster = jeden dzień
4. Zaczynaj od klientów B i C (nie A!)

🎯 **Przykład:**
Poniedziałek = Mokotów (5 sklepów w promieniu 3 km)
Wtorek = Ursynów (5 sklepów w promieniu 3 km)

🔄 **Spróbuj ponownie z klasteryzacją!**
            """
        },
        
        "task_003": {
            "good": """
✅ **Profesjonalny elevator pitch!**

**Struktura:**
✅ Przedstawienie (imię, firma)
✅ Wartość (USP - unikalna propozycja)
✅ Social proof (liczby, referencje)
✅ Kończy się pytaniem otwartym

💡 **Mocne strony:**
- Naturalny, nie brzmi jak reklama
- Konkretne korzyści (nie ogólniki!)
- Odpowiednia długość (~30 sek)

🎯 **Jesteś gotowy do pierwszych wizyt!**

⚡ **Praktyka:**
Przećwicz pitch przed lustrem 10 razy, żeby brzmiał naturalnie.
W grze użyjesz go podczas pierwszych rozmów z klientami!

🎉 **Wszystkie zadania onboardingowe ukończone! Możesz rozpocząć wizyty.**
            """,
            "medium": """
✅ **Dobry pitch, drobne poprawki:**

**Co jest OK:**
✅ Przedstawienie firmy
✅ Pewne elementy wartości

⚠️ **Co poprawić:**
❌ Zbyt długi/krótki (cel: 25-35 sekund)
❌ Brak konkretnych liczb (social proof)
❌ Nie kończy się pytaniem otwartym

💡 **Wskazówka:**
Dodaj konkretne liczby: "Współpracujemy z 120 sklepami..."
Zakończ pytaniem: "Mogę zadać kilka pytań o Pana biznes?"

🔄 **Popraw i wyślij ponownie.**
            """,
            "poor": """
⚠️ **Wymaga przepisania**

❌ **Główne problemy:**
- Brak struktury (USP, social proof)
- Za ogólny (mogłoby być o każdej firmie)
- Nie kończy się pytaniem

💡 **Jak poprawić:**
1. Przeczytaj przykład w artykule (sekcja "Przygotowanie")
2. Użyj struktury:
   - Kim jesteś?
   - Co robicie? (konkretnie!)
   - Jaka wartość? (USP)
   - Social proof (liczby)
   - Pytanie otwarte

🎯 **Pamiętaj:** Pitch to 30 sekund, które otwierają drzwi!

🔄 **Spróbuj ponownie ze strukturą.**
            """
        }
    }
    
    # Mockup - prosta heurystyka (później zastąpi AI)
    text_length = len(submission_text.split())
    
    if task_id == "task_001":
        has_abc = "kategoria a" in submission_text.lower() or "kategoria b" in submission_text.lower()
        has_percentages = "60" in submission_text or "30" in submission_text or "10" in submission_text
        
        if has_abc and has_percentages and text_length > 50:
            return feedback_templates[task_id]["good"]
        elif has_abc or text_length > 30:
            return feedback_templates[task_id]["medium"]
        else:
            return feedback_templates[task_id]["poor"]
    
    elif task_id == "task_002":
        has_clusters = "klaster" in submission_text.lower() or "cluster" in submission_text.lower()
        has_days = any(day in submission_text.lower() for day in ["poniedziałek", "wtorek", "środa"])
        
        if has_clusters and has_days and text_length > 50:
            return feedback_templates[task_id]["good"]
        elif has_clusters or has_days:
            return feedback_templates[task_id]["medium"]
        else:
            return feedback_templates[task_id]["poor"]
    
    elif task_id == "task_003":
        has_company = "freshlife" in submission_text.lower()
        has_question = "?" in submission_text
        word_count = len(submission_text.split())
        
        if has_company and has_question and 50 < word_count < 100:
            return feedback_templates[task_id]["good"]
        elif has_company or has_question:
            return feedback_templates[task_id]["medium"]
        else:
            return feedback_templates[task_id]["poor"]
    
    return "Feedback nierozpoznany."

def complete_task(session_state, task_id, feedback):
    """Oznacz zadanie jako ukończone"""
    if "completed_tasks" not in session_state:
        session_state.completed_tasks = {}
    
    if task_id in session_state.completed_tasks:
        session_state.completed_tasks[task_id]["status"] = "completed"
        session_state.completed_tasks[task_id]["feedback"] = feedback

def all_tasks_completed(session_state):
    """Sprawdź czy wszystkie zadania ukończone"""
    if "completed_tasks" not in session_state:
        return False
    
    for task_id in ONBOARDING_TASKS.keys():
        status = get_task_status(session_state, task_id)
        if status["status"] != "completed":
            return False
    
    return True

def get_pending_tasks_count(session_state):
    """Liczba zadań do ukończenia"""
    count = 0
    for task_id in ONBOARDING_TASKS.keys():
        status = get_task_status(session_state, task_id)
        if status["status"] != "completed":
            count += 1
    return count
