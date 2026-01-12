-- ========================================
-- SQL INSERT: Podstawy Zarządzania Czasem
-- ========================================
-- Instrukcja:
-- 1. Otwórz Supabase Dashboard → SQL Editor
-- 2. Wklej całą zawartość tego pliku
-- 3. Kliknij "Run"
-- ========================================

INSERT INTO lessons (
  id,
  title,
  description,
  category,
  difficulty,
  duration_minutes,
  xp_reward,
  card_count,
  target_roles,
  is_public,
  content_json,
  created_at,
  updated_at
)
VALUES (
  gen_random_uuid(),
  'Podstawy Zarządzania Czasem',
  'Efektywne planowanie i priorytetyzacja zadań. Poznaj sprawdzone metody jak Matrix Eisenhowera, Pomodoro i Getting Things Done.',
  'Produktywność',
  'beginner',
  15,
  60,
  8,
  ARRAY['manager', 'salesperson', 'consultant'],
  true,
  $$
{
  "cards": [
    {
      "id": 1,
      "type": "intro",
      "title": "Witaj w lekcji o zarządzaniu czasem! ⏰",
      "content": "Czy kiedykolwiek czułeś, że dzień powinien mieć więcej niż 24 godziny? Nie jesteś sam. Większość menedżerów zmaga się z nadmiarem zadań i brakiem czasu.\n\n**W tej lekcji poznasz:**\n\n✅ Matrix Eisenhowera - jak rozróżnić ważne od pilnego\n✅ Technikę Pomodoro - jak pracować w skupieniu\n✅ Getting Things Done (GTD) - system zarządzania wszystkim\n\n**Rezultat:** Więcej czasu na to, co naprawdę ważne.",
      "icon": "⏰",
      "estimated_seconds": 60
    },
    {
      "id": 2,
      "type": "concept",
      "title": "Problem: Tyrania Pilności 🔥",
      "content": "**Typowy dzień menedżera:**\n\n8:00 - Zaplanowałeś pracę nad strategią (WAŻNE)\n8:05 - Email: \"Pilne! Klient czeka!\"\n8:30 - Telefon: \"Szef chce raport dziś!\"\n9:00 - Slack: \"Urgentny problem!\"\n12:00 - Realizacja: Zero czasu na strategię\n\n**Diagnoza:** Żyjesz w trybie reaktywnym, nie proaktywnym.\n\n**Skutek:** Robisz TO, CO PILNE, zamiast TO, CO WAŻNE.\n\n**Rozwiązanie:** Matrix Eisenhowera",
      "examples": [
        "Manager spędza 80% czasu na emailach zamiast na rozwoju zespołu",
        "CEO cały dzień w spotkaniach - brak czasu na myślenie strategiczne",
        "Handlowiec obsługuje kryzys zamiast dzwonić do nowych klientów"
      ],
      "estimated_seconds": 120,
      "xp_points": 10
    },
    {
      "id": 3,
      "type": "concept",
      "title": "Matrix Eisenhowera - 4 Kwadranty 📊",
      "content": "**Dwight Eisenhower (prezydent USA, generał):**\n\"To, co jest ważne, rzadko jest pilne. To, co jest pilne, rzadko jest ważne.\"\n\n**4 Kwadranty:**\n\n**I. Pilne i Ważne** (Kryzys)\n- Deadline jutro\n- Awaria systemu\n- Nagły wypadek\n→ **RÓB NATYCHMIAST**\n\n**II. Ważne, ale NIE Pilne** (Strategia)\n- Planowanie długoterminowe\n- Rozwój zespołu\n- Nauka, zdrowie\n→ **ZAPLANUJ I RÓB REGULARNIE** ⭐\n\n**III. Pilne, ale NIE Ważne** (Dystrakcje)\n- Większość emaili\n- Część spotkań\n- Telefony od innych\n→ **DELEGUJ lub OGRANICZ**\n\n**IV. NIE Pilne i NIE Ważne** (Strata czasu)\n- Social media bez celu\n- Netflix w pracy\n- Pusta gadanina\n→ **ELIMINUJ**",
      "data": {
        "framework": "eisenhower_matrix",
        "quadrants": {
          "q1": {
            "name": "Kryzys",
            "attributes": ["pilne", "ważne"],
            "action": "Rób natychmiast",
            "target_time": "0-25%"
          },
          "q2": {
            "name": "Strategia",
            "attributes": ["nie_pilne", "ważne"],
            "action": "Zaplanuj i rób regularnie",
            "target_time": "50-75%"
          },
          "q3": {
            "name": "Dystrakcje",
            "attributes": ["pilne", "nie_ważne"],
            "action": "Deleguj lub ogranicz",
            "target_time": "0-15%"
          },
          "q4": {
            "name": "Strata czasu",
            "attributes": ["nie_pilne", "nie_ważne"],
            "action": "Eliminuj",
            "target_time": "0%"
          }
        }
      },
      "estimated_seconds": 180,
      "xp_points": 15
    },
    {
      "id": 4,
      "type": "question",
      "question": "Które zadanie należy do Kwadrantu II (Ważne, ale NIE Pilne)?",
      "options": [
        "Spotkanie z klientem za 30 minut (deadline)",
        "Nauka nowego języka programowania",
        "Przeglądanie LinkedIn bez celu",
        "Kolega prosi o pomoc w jego zadaniu"
      ],
      "correctAnswer": 1,
      "explanation": "**Nauka nowego języka** to klasyczny Kwadrant II - ważne dla rozwoju, ale nie pilne.\n\n**Pozostałe:**\n- Spotkanie za 30 min → Kwadrant I (pilne + ważne)\n- LinkedIn bez celu → Kwadrant IV (strata czasu)\n- Pomoc koledze → Kwadrant III (pilne dla niego, nie dla Ciebie)",
      "estimated_seconds": 120,
      "xp_points": 15
    },
    {
      "id": 5,
      "type": "concept",
      "title": "Technika Pomodoro 🍅",
      "content": "**Francesco Cirillo, lata 80.:**\nUżywał kuchennego timera w kształcie pomidora (pomodoro) do nauki.\n\n**Zasada:** Praca w blokach 25 minut z przerwami\n\n**Jak działa:**\n\n1. **Wybierz 1 zadanie** (tylko jedno!)\n2. **Timer 25 minut** - pełne skupienie\n3. **5 min przerwy** - wstań, rozciągnij się\n4. **Powtórz** 4x\n5. **Dłuższa przerwa** (15-30 min)\n\n**Dlaczego działa:**\n\n✅ **Flow state** - 25 min = sweet spot skupienia\n✅ **Deadline effect** - czasowy presja motywuje\n✅ **Przerwy** - mózg potrzebuje regeneracji\n✅ **Mierzalność** - 8 pomidorów = pełny dzień pracy\n\n**Pro tip:** 1 pomidor = 1 zadanie. Nie multitasking!",
      "data": {
        "technique": "pomodoro",
        "work_duration": 25,
        "short_break": 5,
        "long_break": 20,
        "cycles_before_long_break": 4
      },
      "estimated_seconds": 150,
      "xp_points": 10
    },
    {
      "id": 6,
      "type": "concept",
      "title": "Getting Things Done (GTD) - System 🧠",
      "content": "**David Allen - autor Getting Things Done:**\n\"Twój mózg jest do myślenia, nie do pamiętania.\"\n\n**5 kroków GTD:**\n\n**1. CAPTURE (Zbieraj)**\n- Zapisuj WSZYSTKO (zadania, pomysły, zobowiązania)\n- Używaj: notatnik, aplikacja, email do siebie\n- Cel: Opróżnij głowę\n\n**2. CLARIFY (Wyjaśniaj)**\n- Czy to wymaga działania?\n- Jeśli TAK: Co konkretnie trzeba zrobić?\n- Jeśli NIE: Usuń, archiwizuj lub coś na później\n\n**3. ORGANIZE (Organizuj)**\n- Listy kontekstowe: @komputer, @telefon, @spotkanie\n- Projekty (>1 zadanie)\n- Kalendarz (sztywne deadlines)\n\n**4. REFLECT (Przeglądaj)**\n- Co tydzień: Review wszystkich list\n- Co dzień: Sprawdź co dziś\n\n**5. ENGAGE (Działaj)**\n- Wybierz zadanie na podstawie:\n  - Kontekst (gdzie jesteś?)\n  - Energia (ile masz siły?)\n  - Czas (ile masz czasu?)\n  - Priorytet (co najważniejsze?)",
      "data": {
        "system": "GTD",
        "steps": ["Capture", "Clarify", "Organize", "Reflect", "Engage"],
        "tools": ["Inbox", "Project lists", "Context lists", "Calendar", "Someday/Maybe"]
      },
      "estimated_seconds": 180,
      "xp_points": 15
    },
    {
      "id": 7,
      "type": "practice",
      "title": "Twój Plan Działania 📋",
      "content": "**Zastosuj to jutro:**\n\n**RANO (10 minut):**\n1. Wypisz wszystkie zadania na dziś\n2. Zaklasyfikuj je do Matrix Eisenhowera\n3. Zaplanuj 2-3 bloki Pomodoro na zadania Kwadrant II\n\n**W CIĄGU DNIA:**\n- Używaj Pomodoro do zadań wymagających skupienia\n- Gdy pojawi się \"pilne\" - zapytaj: \"Czy to naprawdę Kwadrant I?\"\n- Deleguj Kwadrant III\n\n**WIECZOREM (5 minut):**\n- GTD Review: Co nie zostało zrobione?\n- Przenieś na jutro lub usuń\n- Zaplanuj główne zadania na jutro\n\n**PRO TIPS:**\n\n✅ Blokuj Kwadrant II w kalendarzu (np. 9-11 = praca strategiczna)\n✅ Wyłącz notyfikacje podczas Pomodoro\n✅ Jeden inbox (email/notatki) - przeglądaj 2x dziennie",
      "actionSteps": [
        "Wybierz 1 narzędzie do GTD (Todoist, Notion, papier)",
        "Zaplanuj pierwszy blok Pomodoro na jutro rano",
        "Zidentyfikuj swoje główne zadanie Kwadrant II na ten tydzień"
      ],
      "estimated_seconds": 120,
      "xp_points": 10
    },
    {
      "id": 8,
      "type": "summary",
      "title": "Podsumowanie - Zostań Panem Czasu ⏰",
      "content": "**Gratulacje! Ukończyłeś lekcję! 🎉**\n\n**Co wyniosłeś:**\n\n✅ **Matrix Eisenhowera** - Rozróżniasz ważne od pilnego\n✅ **Pomodoro** - Potrafisz pracować w głębokim skupieniu\n✅ **GTD** - Masz system zarządzania wszystkim\n\n**Kluczowe insights:**\n\n💡 80% rezultatów pochodzi z 20% działań (Kwadrant II)\n💡 Przerwy zwiększają produktywność (Pomodoro)\n💡 Mózg do myślenia, nie pamiętania (GTD)\n\n**Następne kroki:**\n\n1. **Dziś:** Zaklasyfikuj swoje zadania do Matrix\n2. **Jutro:** Wypróbuj pierwszy Pomodoro\n3. **Ten tydzień:** Zrób GTD Weekly Review\n\n**Polecane zasoby:**\n- Książka: Getting Things Done - David Allen\n- Aplikacje: Todoist, Notion, Forest (Pomodoro)\n- Film: Eat That Frog - Brian Tracy\n\n**Pamiętaj:** Zarządzanie czasem to zarządzanie priorytetami. Wybieraj mądrze! 🎯",
      "keyPoints": [
        "Kwadrant II to klucz do długoterminowego sukcesu",
        "Pomodoro = 25 min skupienia + 5 min przerwy",
        "GTD: Capture → Clarify → Organize → Reflect → Engage"
      ],
      "estimated_seconds": 90,
      "xp_points": 5
    }
  ]
}
$$::jsonb,
  NOW(),
  NOW()
);

-- ========================================
-- Weryfikacja wstawienia:
-- ========================================
-- SELECT * FROM lessons WHERE title = 'Podstawy Zarządzania Czasem';
