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
        
        # Get task assigner info (default to Sales Manager if not specified)
        assigner = task_data.get('assigned_by', {
            'role': 'Sales Manager',
            'name': 'Krzysztof Nowak'
        })
        
        # Build evaluation prompt - role-play as the task assigner
        prompt = f"""Jesteś {assigner['name']}, {assigner['role']} w firmie FreshLife. 
Przydzieliłeś zadanie swojemu nowemu handlowcowi i teraz oceniasz jego wykonanie.

**ZADANIE, KTÓRE PRZYDZIELIŁEŚ:**
{task_data['title']}

**INSTRUKCJE, KTÓRE DAŁEŚ:**
{task_data['description']}

**CZEGO OCZEKIWAŁEŚ (kryteria sukcesu):**
{chr(10).join(f"- {criterion}" for criterion in task_data['success_criteria'])}

**ZGŁOSZENIE OD HANDLOWCA:**
{submission_text}

**TWOJA ROLA:**
Jesteś doświadczonym managerem, który:
- Traktuje handlowca jako część zespołu (zwracaj się przez "Ty")
- Daje konkretny, praktyczny feedback
- Jest wspierający i rozumie, że handlowiec się uczy
- Akceptuje przyzwoite próby (to gra edukacyjna, nie egzamin!)
- Mówi bezpośrednio, bez zbędnych ozdobników
- Używa przykładów z doświadczenia

**FILOZOFIA OCENY:**
🎯 **Domyślnie AKCEPTUJ, jeśli:**
- Handlowiec zrozumiał sens zadania (nawet jeśli wykonanie nie jest idealne)
- Odpowiedź ma podstawowe elementy wymagane w zadaniu
- Widać wysiłek i przemyślenie (nie jest przypadkowa/śmieciowa)
- Da się z tym pracować w terenie (nawet jeśli wymaga dopracowania)

⚠️ **BEZWZGLĘDNIE ODRZUĆ, jeśli:**
- **Ktoś tylko skopiował treść zadania** (to nie jest wykonanie!)
- **Brak konkretnego wykonania** (np. zadanie wymaga planu, a jest "nie wiem co dalej")
- **Wulgaryzmy/chamstwo** (nieakceptowalne w miejscu pracy)
- **Kompletnie nie na temat** (widać, że nie przeczytał zadania)
- **Brak minimalnego wysiłku** (1 zdanie na zadanie wymagające analizy)
- **Nieczytelny bełkot** (nie da się zrozumieć intencji)

⚠️ **ODRZUĆ jeśli:**
- Brakuje kluczowych elementów (np. w elevator pitch nie ma wartości firmy)
- Odpowiedź jest zbyt ogólnikowa bez żadnych konkretów
- Nie spełnia podstawowych kryteriów sukcesu z zadania
- **ZADANIA O OBIEKCJACH/ODPOWIEDZIACH**: jeśli odpowiedź ma mniej niż 3-4 zdania lub brakuje konkretnej argumentacji (samo "warto mieć" to za mało!)

**SPECJALNA UWAGA dla zadań typu "odpowiedź na obiekcję":**
Takie zadania wymagają KOMPLETNEJ odpowiedzi z:
- Akceptacją punktu klienta
- Konkretną argumentacją (nie "warto mieć", ale DLACZEGO i JAK)
- Przykładem zastosowania lub korzyścią
- Pytaniem angażującym
Odpowiedź w stylu "rozumiem, ale warto mieć" to ODRZUĆ - to nie jest profesjonalna obsługa obiekcji!

**FORMAT FEEDBACKU:**

Jeśli AKCEPTUJESZ zadanie (większość przypadków!):
```
ACCEPT
✅ **Dobra robota - puszczam Cię dalej!**

**Co jest OK:**
- [konkretne punkty - co handlowiec zrobił dobrze]
- [oceń pozytywnie wysiłek]

💡 **Co możesz dopracować w praktyce:**
[1-2 konstruktywne wskazówki na przyszłość - NIE wymaga poprawy w zadaniu, tylko rada do zastosowania potem]

🎯 **Z mojego doświadczenia:**
[praktyczna rada z perspektywy managera]
```

Jeśli ODRZUCASZ (rzeczywiście słabe - brak wykonania):
```
REVISE
⚠️ **To nie jest gotowe - musisz wykonać zadanie**

**Problem:**
❌ [konkretnie czego brakuje - np. "To tylko skopiowana treść zadania, nie Twoja praca"]
❌ [co jest źle - np. "Brak konkretnej listy sklepów z przypisaniem do kategorii"]

💡 **Co musisz zrobić:**
1. [konkretna instrukcja - np. "Weź listę 20 sklepów z gry i przypisz każdy do A/B/C"]
2. [przykład dobrego rozwiązania]

🔄 **Poświęć chwilę i zrób to porządnie - wtedy puszczę Cię dalej.**
```

**WAŻNE ZASADY:**
- Piszesz jako {assigner['name']} ({assigner['role']}) - to feedback od managera, nie ocena komputera
- Język polski, forma "Ty" (jak w normalnej rozmowie z podwładnym)
- **BĄŚ WYROZUMIAŁY** - to początkujący handlowiec w grze edukacyjnej!
- Konkretny feedback odnoszący się do tego co napisał
- Pierwsza linia MUSI być: "ACCEPT" lub "REVISE"
- Emoji dla czytelności
- Maksymalnie 150 słów
- Brzmi jak prawdziwa rozmowa w firmie (nie jak AI)

Wygeneruj feedback jako {assigner['name']}:"""

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
        
        print(f"🔍 RAW AI Response:\n{feedback_text[:200]}")
        
        # Remove code block markers if present
        if feedback_text.startswith('```'):
            # Remove opening ```
            lines = feedback_text.split('\n')
            lines = lines[1:]  # Skip first ```
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]  # Skip closing ```
            feedback_text = '\n'.join(lines).strip()
        
        # Parse decision (check entire response for ACCEPT/REVISE)
        is_accepted = False
        decision_line = ""
        
        for line in feedback_text.split('\n'):
            line_upper = line.strip().upper()
            if 'ACCEPT' in line_upper and 'REVISE' not in line_upper:
                is_accepted = True
                decision_line = line
                break
            elif 'REVISE' in line_upper:
                is_accepted = False
                decision_line = line
                break
        
        print(f"🔍 Decision line found: {decision_line}")
        print(f"🔍 Decision: {'ACCEPTED ✅' if is_accepted else 'REVISE ⚠️'}")
        
        # Remove decision line from feedback (keep the rest)
        if decision_line:
            feedback_text = feedback_text.replace(decision_line, '', 1).strip()
        
        # Clean up any remaining code block artifacts
        feedback_text = feedback_text.replace('```', '').strip()
        
        # Remove any stray HTML closing tags that might appear
        import re
        feedback_text = re.sub(r'</?(div|p|span)>', '', feedback_text)
        
        print(f"🔍 Clean feedback length: {len(feedback_text)} chars")
        
        return feedback_text, is_accepted
        
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
        "title": "🎤 Elevator Pitch - Przedstawienie firmy",
        "assigned_by": {
            "role": "Sales Manager",
            "name": "Krzysztof Nowak"
        },
        "description": """
        Napisz krótkie (30 sekund), profesjonalne przedstawienie firmy Heinz Food Service i Twojej oferty.
        
        **Struktura:**
        1. Kim jesteś? (imię, firma)
        2. Co robicie? (branża, specjalizacja - produkty Heinz i Pudliszki dla HoReCa)
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
        "order": 1,
        "input_type": "textarea",
        "placeholder": """Przykład:

"Dzień dobry! Jestem [Twoje imię] z Heinz Food Service. Specjalizujemy się w dostawach produktów premium dla gastronomii - ketchupy Heinz, sosy Pudliszki, produkty convenience.

Naszą mocną stroną jest jakość marki Heinz oraz kompleksowe wsparcie - szkolenia dla kuchni, materiały POS, pomoc w kreowaniu menu.

Obsługujemy ponad 500 restauracji w całej Polsce.

Mogę opowiedzieć jak pomagamy restauracjom zwiększać marże?"

[Twoja wersja tutaj...]
        """,
        "success_criteria": [
            "Odpowiednia długość (60-80 słów)",
            "Zawiera USP (unikalną wartość)",
            "Wspomina social proof (liczby)",
            "Kończy się pytaniem otwartym"
        ]
    },
    
    "task_002": {
        "id": "task_002",
        "title": "❓ Pytania do nowego klienta",
        "assigned_by": {
            "role": "Sales Manager",
            "name": "Krzysztof Nowak"
        },
        "description": """
        Przygotuj listę 3-4 pytań, które zadasz klientowi przy pierwszym kontakcie.
        
        **Cel pytań:**
        - Zrozumieć potrzeby klienta (typ kuchni, profil gości)
        - Poznać obecne rozwiązania (co teraz używa, skąd kupuje)
        - Zidentyfikować problemy/wyzwania (z czym się boryka)
        - Znaleźć punkt zaczepienia dla oferty
        
        **Zasady dobrych pytań:**
        - Pytania OTWARTE (nie tak/nie)
        - Konkretne (nie ogólniki w stylu "jak idą interesy?")
        - Nastawione na klienta (nie na sprzedaż produktu)
        - Logiczna kolejność (od ogółu do szczegółu)
        """,
        "required_article": "🗺️ Planowanie terytorium sprzedażowego",
        "order": 2,
        "input_type": "textarea",
        "placeholder": """Przykład:

1. "Jaki typ kuchni Państwo prowadzicie i kto jest Waszym głównym gościem?"
   [Cel: zrozumieć profil - burger bar vs fine dining vs food truck]

2. "Z jakimi produktami w kategorii sosów i ketchupów pracujecie teraz?"
   [Cel: poznać konkurencję, poziom jakości, cenę]

3. "Jakie są Wasze największe wyzwania jeśli chodzi o koszty w kuchni?"
   [Cel: znaleźć pain point - marnotrawstwo, jakość, standaryzacja]

4. "Jak podejmujecie decyzje o zmianie dostawcy lub wypróbowaniu nowych produktów?"
   [Cel: zrozumieć proces decyzyjny, kto ma głos]

[Twoja lista pytań tutaj...]
        """,
        "success_criteria": [
            "3-4 pytania otwarte",
            "Pytania konkretne (nie ogólniki)",
            "Nastawione na poznanie klienta (nie na sprzedaż)",
            "Logiczna kolejność"
        ]
    },
    
    "task_003": {
        "id": "task_003",
        "title": "💬 Odpowiedź na obiekcję: 'Mam już Heinz'",
        "assigned_by": {
            "role": "Sales Manager",
            "name": "Krzysztof Nowak"
        },
        "description": """
        Klient mówi: "Skoro już mam ketchup Heinz, to po co mi Pudliszki?"
        
        Przygotuj swoją odpowiedź na tę obiekcję.
        
        **Struktura dobrej odpowiedzi:**
        1. **Akceptacja** - przyznaj rację ("Faktycznie, Heinz to świetny wybór...")
        2. **Uzupełnienie** - pokaż wartość dodatkową Pudliszek ("Pudliszki to coś innego...")
        3. **Korzyść konkretna** - co klient zyska ("Dzięki temu możesz...")
        4. **Przykład/dowód** - konkretna sytuacja lub zastosowanie
        5. **Pytanie/CTA** - zaangażuj ("Czy Wasz profil gości...?")
        
        **Wskazówki:**
        - Nie atakuj Heinza (to też nasz produkt!)
        - Pokaż komplementarność: Heinz = premium/międzynarodowe, Pudliszki = tradycja/polska kuchnia
        - Konkretne przykłady zastosowań (nie ogólniki!)
        - Minimum 4-5 zdań rozbudowanej argumentacji
        """,
        "required_article": "🗺️ Planowanie terytorium sprzedażowego",
        "order": 3,
        "input_type": "textarea",
        "placeholder": """Przykład:

"Świetnie, że macie Heinz - to najlepsza jakość premium! 

Pudliszki to segment complementary - bardziej tradycyjny, polski smak, który pasuje do zupełnie innych dań. Heinz idealnie sprawdza się przy burgerach i steakach, ale Pudliszki lepiej komponuje się z polską kuchnią - żeberkami, schabowym, pierogami.

Dzięki obu markom możecie dopasować sos do profilu dania i gościa - turysta zagraniczny dostaje Heinz przy burgerze, polski klient biznesowy Pudliszki do tradycyjnego obiadu.

W Restauracji 'Polskie Smaki' używają Heinza w menu premium, a Pudliszek w menu dnia - i obie marki się uzupełniają.

Czy w Waszym menu są dania, gdzie polski, tradycyjny smak sosu byłby lepszym dopasowaniem?"

[Twoja odpowiedź tutaj...]
        """,
        "success_criteria": [
            "Akceptacja obiekcji (nie atak na Heinz)",
            "Wyjaśnienie komplementarności (Heinz vs Pudliszki - różne zastosowania)",
            "Konkretne korzyści dla klienta (nie ogólniki!)",
            "Przykład lub konkretne zastosowanie",
            "Pytanie angażujące na koniec",
            "Odpowiedź ma minimum 4-5 rozbudowanych zdań"
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
    """Oznacz zadanie jako ukończone i zapisz historię"""
    if "completed_tasks" not in session_state:
        session_state.completed_tasks = {}
    
    if task_id in session_state.completed_tasks:
        session_state.completed_tasks[task_id]["status"] = "completed"
        session_state.completed_tasks[task_id]["feedback"] = feedback
        session_state.completed_tasks[task_id]["completed_at"] = datetime.now().isoformat()
    else:
        # Jeśli nie było submitted, utwórz nowy wpis
        session_state.completed_tasks[task_id] = {
            "status": "completed",
            "submission": "",
            "feedback": feedback,
            "submitted_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat()
        }

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
