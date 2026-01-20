-- Import Lesson 1.1 v2.0 (Enhanced): Milwaukee Story - Nothing but HEAVY DUTY™
-- Run this in Supabase SQL Editor to import the lesson
-- Version: 2.0 (Enhanced with storytelling, split Core Values, Application First scenario)

-- Milwaukee Company ID: d73705b5-f27d-49f7-a516-63a1158cb75a

INSERT INTO lessons (
  lesson_id,
  title,
  description,
  duration_minutes,
  xp_reward,
  difficulty,
  company_id,
  module,
  track,
  target_roles,
  tags,
  content
) VALUES (
  'lesson-1-1-milwaukee-story',
  'Milwaukee Story - Nothing but HEAVY DUTY™',
  'Poznaj prawdziwą historię Milwaukee: od Hole-Shootera dla Henry''ego Forda (1918), przez Sawzall i US Navy, do dzisiejszych systemów M12/M18/MX FUEL. Zrozum 3 core values z konkretnymi przykładami i filozofię Application First.',
  20,
  75,
  'beginner',
  'd73705b5-f27d-49f7-a516-63a1158cb75a'::uuid,
  'Module 1: Foundations',
  'Foundation Track',
  ARRAY['JSS', 'ASR', 'KAM', 'BDM', 'FME'],
  ARRAY['milwaukee', 'history', 'values', 'onboarding', 'foundation', 'culture', 'storytelling'],
  $$
  {
    "cards": [
      {
        "id": "card-1",
        "type": "hero",
        "title": "Witaj w Milwaukee Family",
        "subtitle": "Nothing but HEAVY DUTY™ - Zero Kompromisów dla Profesjonalistów",
        "content": "Nie jesteś tu po to, by sprzedawać narzędzia. Jesteś tu po to, by zmieniać sposób, w jaki profesjonaliści pracują każdego dnia.\n\nMilwaukee to nie marka. To **ruch** ludzi, którzy nie akceptują kompromisów — w jakości, bezpieczeństwie i wydajności.\n\nTa lekcja to początek drogi. Poznasz historie, które zbudowały Milwaukee: od pierwszego narzędzia stworzonego dla Henry'ego Forda, przez współpracę z US Navy, po filozofię Heavy Duty™, która definiuje markę do dziś. Dowiesz się, dlaczego Milwaukee myśli inaczej — i dlaczego Ty jesteś częścią tej historii."
      },
      {
        "id": "card-2-text",
        "type": "content",
        "title": "Początki: od Hole-Shootera do koncentracji na użytkowniku (1918–lata 30.)",
        "content": "### 🏭 1918 – Geneza: narzędzie dla Henry'ego Forda\n\n**Hole-Shooter** – lekka wiertarka ¼\", zaprojektowana na potrzeby pracy na liniach montażowych Forda.\n\nTo właśnie od tego narzędzia zaczyna się historia Milwaukee.\n\n---\n\n### 🔥 1924 – Narodziny z popiołów\n\n**Albert F. Siebert** przejmuje majątek spółki po pożarze fabryki i zakłada **Milwaukee Electric Tool Corporation**.\n\nCel jest jasny: udoskonalić Hole-Shootera i dostosować go do realiów przemysłu.\n\n---\n\n### 🔧 Lata 20. i 30. – Źródło przewagi Milwaukee\n\nZnacząca część działalności Milwaukee opierała się na **naprawach narzędzi innych producentów**, a nie na własnej produkcji.\n\nDzięki temu firma zyskała coś bezcennego:\n- dogłębną wiedzę o typowych awariach,\n- zrozumienie rzeczywistych problemów użytkowników,\n- doświadczenie, którego konkurencja nie posiadała.\n\n**Efekt:** Hole-Shooter został wzmocniony i udoskonalony w oparciu o te obserwacje, stając się standardem w przemyśle motoryzacyjnym i obróbce metalu.\n\n---\n\n💡 **DNA Milwaukee:** Od samego początku firma uczyła się od użytkowników. Nie była to deklaracja marketingowa, lecz fundament sposobu działania."
      },
      {
        "id": "card-2-timeline",
        "type": "timeline",
        "title": "100 Lat Historii - Oś Czasu",
        "data": {
          "items": [
            {
              "year": "1918",
              "title": "Hole-Shooter & Henry Ford",
              "description": "Pierwsza lekka wiertarka stworzona specjalnie na linie montażowe Forda. Początek legendy.",
              "icon": "factory"
            },
            {
              "year": "1924",
              "title": "Narodziny Marki",
              "description": "Albert F. Siebert zakłada firmę po pożarze fabryki. Cel: Udoskonalić Hole-Shootera.",
              "icon": "fire"
            },
            {
              "year": "1930s",
              "title": "US Navy Standards",
              "description": "Współpraca z marynarką. Narzędzia muszą przetrwać ekstremalne warunki. Tu rodzi się 'Heavy Duty'.",
              "icon": "anchor"
            },
            {
              "year": "1951",
              "title": "SAWZALL® Revolution",
              "description": "Pierwsza piła szablasta. Milwaukee tworzy nową kategorię narzędzi, a nie tylko ulepsza stare.",
              "icon": "saw"
            },
            {
              "year": "1990s",
              "title": "PRO Only Decision",
              "description": "Strategiczna decyzja: Rezygnacja z rynku hobby. 100% fokus na profesjonalistach.",
              "icon": "target"
            },
            {
              "year": "2005",
              "title": "TTI & Innovation Boom",
              "description": "Nowy rozdział. Inwestycje w technologie akumulatorowe. Start ery M12™ i M18™.",
              "icon": "battery"
            },
            {
              "year": "2024+",
              "title": "MX FUEL™ & Ekosystem",
              "description": "Koniec ery spalin. Pełna elektryfikacja ciężkiego sprzętu.",
              "icon": "lightning"
            }
          ]
        }
      },
      {
        "id": "card-3-text",
        "type": "content",
        "title": "Innowacje, które zmieniły rynek (1930–2024)",
        "content": "### ⚓ Około 1930 r. – Współpraca z marynarką wojenną USA\n\nMilwaukee rozpoczyna współpracę z **US Navy**, produkując narzędzia spełniające **rygorystyczne normy wojskowe**.\n\n**Efekt:** ugruntowanie reputacji marki jako synonimu wyjątkowej trwałości w przemyśle ciężkim.\n\n---\n\n### 🔐 1949 – Bezpieczeństwo jako standard\n\nMilwaukee wprowadza rozwiązania, które realnie poprawiają bezpieczeństwo pracy:\n- **sprzęgło sprężynowe**, ograniczające ryzyko odrzutu narzędzia,\n- **wiertarkę kątową ½\"**, umożliwiającą pracę w ciasnych i trudno dostępnych przestrzeniach.\n\n---\n\n### 🏆 1951 – SAWZALL® i narodziny nowej kategorii\n\nMilwaukee wprowadza na rynek pierwszą **przenośną piłę szablastą**.\n\nHasło „cokolwiek i gdziekolwiek” nie było obietnicą marketingową, lecz opisem realnych możliwości narzędzia.\n\nMilwaukee nie ulepszyło istniejącego rozwiązania – **stworzyło zupełnie nową kategorię narzędzi**.\n\n---\n\n### 📈 Lata 60. i 70. – Ekspansja i specjalizacja\n\nFirma dynamicznie się rozwija, uruchamia nowe zakłady produkcyjne i poszerza ofertę.\n\nSymbolem tej epoki staje się **Hole Hawg** – specjalistyczna wiertarka do wykonywania dużych otworów w konstrukcjach drewnianych, zaprojektowana z myślą o konkretnych zastosowaniach.\n\n---\n\n### 🎯 Lata 90. – Decyzja: tylko profesjonaliści\n\nMilwaukee podejmuje świadomą decyzję o **rezygnacji z rynku hobbystycznego**.\n\nFirma koncentruje się wyłącznie na użytkownikach profesjonalnych, stawiając na trwałość, bezpieczeństwo i wydajność. Ten kierunek definiuje markę do dziś.\n\n---\n\n### 🔋 2005–2024 – Era platform systemowych\n\n- **2005 r.** – przejęcie przez **Techtronic Industries (TTI)**, które otwiera drogę do intensywnego rozwoju technologicznego.\n- **Lata 2010–2020** – rozwój platform M12™ i M18™: jedna bateria, setki kompatybilnych narzędzi.\n- **Od 2021 r.** – **MX FUEL™**, czyli wydajne systemy akumulatorowe zastępujące rozwiązania spalinowych.\n\n---\n\n🎯 **Wzorzec działania:** Milwaukee konsekwentnie tworzy i redefiniuje kategorie narzędzi, zamiast jedynie rozwijać pojedyncze produkty."
      },
      {
        "id": "card-3-lightbulb",
        "type": "lightbulb",
        "title": "Dlaczego Milwaukee rozumie użytkownika?",
        "content": "W latach 20. Milwaukee zarabiało głównie na **naprawianiu narzędzi konkurencji**.",
        "insight": "Dzięki temu inżynierowie widzieli dokładnie, co się psuje i dlaczego. To nie był marketing – to była twarda lekcja inżynierii zwrotnej, która zbudowała DNA firmy.",
        "accent_color": "yellow"
      },
      {
        "id": "card-4",
        "type": "interactive",
        "title": "Quick Check - Historia",
        "quiz": {
          "question": "Co dało Milwaukee unikalny wgląd w potrzeby użytkowników w latach 20. i 30.?",
          "options": [
            "Badania marketingowe",
            "Naprawy cudzych narzędzi (większość przychodów)",
            "Testy w US Navy",
            "Współpraca z Henry'm Fordem"
          ],
          "correct": 1,
          "explanation": "W latach 20-30 Milwaukee zarabiało głównie na naprawach cudzych elektronarzędzi. To dało firmie unikalny wgląd w awarie i realne potrzeby użytkowników – wiedza, której konkurencja nie miała. To DNA 'Obsessive Focus on User'."
        }
      },
      {
        "id": "card-5",
        "type": "content",
        "title": "Wartość kluczowa #1: Koncentracja na użytkowniku",
        "content": "### 🔍 Co to oznacza w praktyce?\n\nProdukt nie zaczyna się w laboratorium ani w sali projektowej. Zaczyna się **w miejscu pracy użytkownika** – od obserwacji tego, jak naprawdę wykonuje swoje zadania.\n\nMilwaukee nie projektuje rozwiązań w oderwaniu od rzeczywistości. Punktem wyjścia zawsze jest realna praca i realne warunki.\n\n---\n\n### 📖 Źródło tej filozofii – lata 20. i 30.\n\nPoczątki Milwaukee były silnie związane z **naprawą narzędzi innych producentów**. To doświadczenie dało firmie wyjątkowy wgląd w:\n- rzeczywiste awarie i ograniczenia narzędzi,\n- frustracje użytkowników w codziennej pracy,\n- problemy, które pozostawały niewidoczne dla konkurencji.\n\nTo nie był przypadek, lecz fundament sposobu myślenia, który ukształtował firmę od samego początku.\n\n---\n\n### 💼 Jak wygląda to dziś?\n\nMilwaukee konsekwentnie stosuje tę samą zasadę:\n- **projektowanie wychodzące od zastosowania**, a nie od parametrów technicznych,\n- **obserwację pracy użytkowników w terenie**, zamiast opierania się na założeniach,\n- **ciągłe zbieranie informacji zwrotnej**, w której użytkownicy testują i oceniają rozwiązania.\n\nNie zadajemy pytania: „Jaką technologię zastosować?”.\nZadajemy pytanie: „Gdzie pracujesz i co realnie spowalnia Twoją pracę?”.\n\n---\n\n🎯 **Twoja rola:** Jako przedstawiciel Milwaukee również odpowiadasz za koncentrację na użytkowniku. Obserwuj, zadawaj pytania, słuchaj i wyciągaj wnioski. To od tych rozmów zaczyna się każda dobra decyzja."
      },
      {
        "id": "card-6",
        "type": "content",
        "title": "Wartość kluczowa #2: Innowacje, które mają znaczenie",
        "content": "### 💡 Co to oznacza?\n\nInnowacja w Milwaukee to **realna przewaga w codziennej pracy użytkownika**. Nie chodzi o efektowne dodatki ani rozwiązania tworzone wyłącznie po to, by dobrze wyglądały w katalogu.\n\nLiczy się tylko to, co faktycznie poprawia wydajność, bezpieczeństwo i komfort pracy.\n\n---\n\n### 🏆 Przykład historyczny: SAWZALL® (1951)\n\n**Problem użytkownika:** „Muszę ciąć różne materiały w różnych miejscach. Narzędzia stacjonarne mnie ograniczają.”\n\n**Odpowiedź Milwaukee:** stworzenie pierwszej **przenośnej piły szablastej**, która pozwalała pracować tam, gdzie wcześniej było to niemożliwe.\n\n**Efekt:** powstanie zupełnie nowej kategorii narzędzi. Dziś piły tego typu są standardem, ale to Milwaukee wyznaczyło kierunek.\n\n---\n\n### 🔋 Przykłady współczesne\n\nMilwaukee konsekwentnie rozwija innowacje, które mają praktyczne zastosowanie:\n- **Technologia FUEL™** – wydajne silniki bezszczotkowe, zaawansowana elektronika i trwałe akumulatory,\n- **ONE-KEY™** – narzędzia do zarządzania sprzętem, jego lokalizacji i zabezpieczenia,\n- **MX FUEL™** – zastąpienie rozwiązań spalinowych systemami akumulatorowymi w ciężkich zastosowaniach.\n\nKażda z tych innowacji ma **mierzalny wpływ na produktywność użytkownika**. Nie jest dodatkiem – jest realnym usprawnieniem.\n\n---\n\n### ⚖️ Prosty test innowacji\n\nZawsze zadajemy jedno pytanie:\n\n**Czy to rozwiązanie realnie zwiększa efektywność pracy użytkownika w jego warunkach?**\n\n- jeśli **tak** – mówimy o innowacji, która ma znaczenie,\n- jeśli **nie** – to jedynie zbędny dodatek."
      },
      {
        "id": "card-7",
        "type": "content",
        "title": "Wartość kluczowa #3: Trwałość bez kompromisów (Heavy Duty)",
        "content": "### 💪 Co to oznacza?\n\n**Trwałość, bezpieczeństwo i wydajność – bez kompromisów.**\n\nDla Milwaukee „Heavy Duty” nie jest hasłem reklamowym. To standard, według którego projektowane są wszystkie rozwiązania.\n\n---\n\n### ⚓ Źródło tej filozofii – współpraca z marynarką wojenną USA (ok. 1930 r.)\n\nMilwaukee produkowało narzędzia spełniające **surowe normy amerykańskiej marynarki wojennej**.\n\nWymagania były jednoznaczne:\n- praca w ekstremalnych warunkach (wilgoć, wibracje, ciągłe obciążenie),\n- brak tolerancji dla awarii,\n- długie i przewidywalne cykle życia narzędzi.\n\n**Efekt:** reputacja trwałości i niezawodności, która budowana jest konsekwentnie do dziś.\n\n---\n\n### 🔐 Jak wygląda to w praktyce?\n\nTrwałość Milwaukee to konkretne decyzje projektowe:\n- **testy w skrajnych warunkach**, obejmujące upadki, pył, wodę i skrajne temperatury,\n- **projektowanie na długie lata użytkowania**, a nie na krótki cykl życia produktu,\n- **5-letnia gwarancja**, będąca potwierdzeniem zaufania do własnych rozwiązań,\n- **rozwiązania zwiększające bezpieczeństwo**, takie jak sprzęgła ograniczające ryzyko odrzutu, stosowane już od 1949 roku.\n\n---\n\n### 🎖️ Heavy Duty to nie „ciężkie narzędzie”\n\nNie chodzi o wagę ani masywność. Chodzi o **odpowiedzialność za jakość**, niezawodność i bezpieczeństwo użytkownika.\n\n**Nothing but HEAVY DUTY™** oznacza jedno: brak kompromisów tam, gdzie liczy się profesjonalna praca."
      },
      {
        "id": "card-8",
        "type": "interactive",
        "title": "Która wartość?",
        "quiz": {
          "question": "Milwaukee testuje nowe narzędzie przez 6 miesięcy w warunkach ekstremalnych (kurz, woda, ciągła praca), zanim je wypuści. Która core value?",
          "options": [
            "Obsessive Focus on the User",
            "Innovation That Matters",
            "Heavy Duty Commitment"
          ],
          "correct": 2,
          "explanation": "To doskonały przykład 'Heavy Duty Commitment'. Milwaukee nie kompromisuje trwałości – testy w ekstremalnych warunkach zapewniają że narzędzie przetrwa lata pracy na jobsite. DNA od czasów US Navy (1930)."
        }
      },
      {
        "id": "card-9-text",
        "type": "content",
        "title": "Application First - Filozofia od Lat 20.",
        "content": "Milwaukee **nie sprzedaje narzędzi** – sprzedaje **sposób pracy**.\n\n---\n\n### ❌ Tradycyjne Podejście (Produktowe):\n\n*\"Ile ma obrotów?\"*\n*\"Nowość w ofercie!\"*\n*\"Najmocniejszy silnik!\"*\n\n**Result:** Sprzedaż pudełka, nie rozwiązania.\n\n---\n\n### ✅ Milwaukee Way (Application First):\n\n*\"Gdzie i jak pracujesz?\"*\n*\"Co dziś Cię spowalnia?\"*\n*\"Jakie problemy masz na jobsite?\"*\n\n**Result:** Rozwiązanie problemu, lojalny klient.\n\n---\n\n### 📜 To Nie Nowe – To DNA od Lat 20.\n\n**Lata 20-30:** Milwaukee naprawiało narzędzia → **widziało realne problemy** → projektowało rozwiązania\n\n**Dzisiaj:** Jobsite walks → **widzimy realne aplikacje** → projektujemy systemy\n\n**Ten sam proces, 100 lat później.**\n\n---\n\n### 🎯 Application First = 7 Kroków:\n\n1. **Application** – Gdzie pracujesz?\n2. **Problem** – Co Cię spowalnia?\n3. **Consequences** – Jaki impact?\n4. **Solution (SYSTEM)** – Tool + Platform + Accessory + Protection\n5. **Demo** – Pokaż w akcji\n6. **Value** – Policz ROI\n7. **Next Steps** – Co dalej?\n\n*(Będziesz ćwiczyć to w Module 3)*"
      },
      {
        "id": "card-9-flashcards",
        "type": "flashcards",
        "title": "Mentalność Sprzedawcy: Sprawdź Różnicę",
        "cards": [
          {
            "front": "❌ Podejście Produktowe (Tradycyjne)",
            "back": "Pytania: 'Ile ma watów?', 'Jaka cena?'\nEfekt: Walka na rabaty. Sprzedajesz 'pudełko'."
          },
          {
            "front": "✅ Podejście Application First (Milwaukee)",
            "back": "Pytania: 'Gdzie pracujesz?', 'Co Cię spowalnia?'\nEfekt: Sprzedaż rozwiązania (Systemu). Lojalny klient."
          }
        ]
      },
      {
        "id": "card-10",
        "type": "interactive",
        "title": "Scenario: Application First w Praktyce",
        "quiz": {
          "question": "Klient wchodzi do sklepu i mówi: 'Potrzebuję wiertarkę udarową'. Co robisz PIERWSZY według Application First?",
          "options": [
            "Pokazujesz najnowszy model M18 FUEL",
            "Pytasz: 'Gdzie będziesz pracować i co wiercić?' (APPLICATION)",
            "Dajesz mu spec sheet z parametrami",
            "Oferujesz demo na miejscu"
          ],
          "correct": 1,
          "explanation": "Application First ZAWSZE zaczyna od pytań o aplikację! 'Gdzie pracujesz?' → 'Co wiercisz?' → 'Jak często?' Dopiero wtedy możesz dobrać SYSTEM (narzędzie + bateria + wiertła + ochrony). Klient powiedział 'wiertarka', ale prawdziwe pytanie to 'JAK rozwiązać jego problem?'"
        }
      },
      {
        "id": "card-11",
        "type": "quiz",
        "title": "Sprawdź Wiedzę: Milwaukee DNA",
        "questions": [
          {
            "question": "Dla kogo został stworzony pierwszy Hole-Shooter w 1918 roku?",
            "options": [
              "Dla górników w kopalniach węgla",
              "Dla Henry'ego Forda na linie produkcyjne",
              "Dla Marynarki Wojennej USA",
              "Dla budowniczych wieżowców w Chicago"
            ],
            "correctAnswer": 1,
            "explanation": "Hole-Shooter, pierwsza lekka wiertarka 1/4 cala, powstała specjalnie dla pracowników Henry'ego Forda, którzy potrzebowali lżejszego narzędzia na liniach montażowych."
          },
          {
            "question": "Dlaczego Milwaukee w latach 20. naprawiało narzędzia konkurencji?",
            "options": [
              "Bo nie mieli własnych produktów",
              "Aby zarobić na częściach zamiennych",
              "Aby zrozumieć, dlaczego narzędzia się psują i budować lepsze (Inżynieria Zwrotna)",
              "To był błąd strategiczny"
            ],
            "correctAnswer": 2,
            "explanation": "To była 'lekcja inżynierii'. Naprawiając narzędzia konkurencji, inżynierowie Milwaukee uczyli się o słabych punktach i potrzebach użytkowników, co pozwoliło im budować trwalszy sprzęt."
          },
          {
            "question": "Jaka innowacja z 1951 roku stworzyła zupełnie nową kategorię narzędzi?",
            "options": [
              "Wiertarka udarowa",
              "SAWZALL® (Piła szablasta)",
              "Szlifierka kątowa",
              "Wkrętarka akumulatorowa"
            ],
            "correctAnswer": 1,
            "explanation": "SAWZALL® był pierwszą przenośną piłą szablastą. Zastąpił ręczne piłowanie i pozwolił na pracę 'Cokolwiek, Gdziekolwiek', tworząc nową kategorię."
          },
          {
            "question": "Co oznacza filozofia 'Application First'?",
            "options": [
              "Najpierw sprzedajemy aplikację mobilną",
              "Najpierw pytamy o pracę i problem użytkownika, dopiero potem dobieramy narzędzie",
              "Najpierw pokazujemy najdroższe narzędzie",
              "Najpierw wysyłamy katalog"
            ],
            "correctAnswer": 1,
            "explanation": "Application First oznacza odwrócenie procesu sprzedaży. Zamiast 'mam wiertarkę, kup ją', pytamy 'gdzie pracujesz i co Cię spowalnia?', by dobrać rozwiązanie systemowe."
          },
          {
            "question": "Dlaczego Milwaukee wycofało się z rynku DIY (Hobby) w latach 90.?",
            "options": [
              "Bo rynek był za mały",
              "Aby skupić się w 100% na użytkownikach PROFESJONALNYCH (Heavy Duty)",
              "Bo konkurencja była za silna",
              "Bo marketowi klienci nie lubili koloru czerwonego"
            ],
            "correctAnswer": 1,
            "explanation": "To była kluczowa decyzja strategiczna. Milwaukee postanowiło być marką wyłącznie dla profesjonalistów, co pozwoliło na bezkompromisową jakość (Heavy Duty) bez walki cenowej w marketach."
          }
        ]
      },
      {
        "id": "card-12",
        "type": "content",
        "title": "Jesteś Częścią Milwaukee Family",
        "content": "### 🎯 Co Zapamiętać:\n\n✅ **Historia:** Od Hole-Shootera (1918) → Sawzall (1951) → MX FUEL (2024)\n✅ **Pattern:** Milwaukee **tworzy kategorie**, nie tylko produkty\n✅ **DNA:** User Focus od lat 20. (naprawy!), US Navy quality (1930), Innovation (Sawzall)\n✅ **Wartości:**\n  - 🔍 **Obsessive Focus** → Jobsite walks, nie zgadujemy\n  - 💡 **Innovation** → Realna przewaga, nie gadżety\n  - 💪 **Heavy Duty** → Zero kompromisów (DNA od US Navy)\n✅ **Filozofia:** Application First – od lat 20., nie marketing\n\n---\n\n### 💪 Dlaczego To Ważne:\n\nJesteś ambasadorem marki, która **zmienia** sposób pracy milionów profesjonalistów.\n\n**Każda rzecz którą sprzedajesz** to nie \"pudełko\" – to:\n- ⏱️ Więcej czasu dla usera\n- 💰 Więcej zarobków\n- 🏠 Szybszy powrót do domu\n- 🔐 Większe bezpieczeństwo\n\nTwoja rola to nie \"handlowiec\" – to **doradca**, który pomaga ludziom pracować lepiej, szybciej, bezpieczniej.\n\n**Nothing but HEAVY DUTY™** to Twoja misja. Zero kompromisów.\n\n---\n\n### ➡️ Następny Krok:\n\n**Lesson 1.2:** Portfolio Overview - Ekosystem M12/M18/MX FUEL\n\n*(Poznasz SYSTEMY, nie pojedyncze produkty – bo Milwaukee sprzedaje ekosystemy)*"
      }
    ]
  }
  $$::jsonb
)
ON CONFLICT (lesson_id) DO UPDATE SET
  title = EXCLUDED.title,
  description = EXCLUDED.description,
  duration_minutes = EXCLUDED.duration_minutes,
  xp_reward = EXCLUDED.xp_reward,
  difficulty = EXCLUDED.difficulty,
  company_id = EXCLUDED.company_id,
  module = EXCLUDED.module,
  track = EXCLUDED.track,
  target_roles = EXCLUDED.target_roles,
  tags = EXCLUDED.tags,
  content = EXCLUDED.content,
  updated_at = NOW();


-- Verify import
SELECT 
  lesson_id,
  title,
  difficulty,
  xp_reward,
  duration_minutes,
  module,
  track,
  jsonb_array_length(content->'cards') as num_cards,
  array_length(target_roles, 1) as num_target_roles,
  array_length(tags, 1) as num_tags,
  (SELECT c.name FROM companies c WHERE c.id = lessons.company_id) as company_name
FROM lessons
WHERE lesson_id = 'lesson-1-1-milwaukee-story';

-- Expected result: 1 row showing 15 cards (Includes Final Quiz hybrid), Milwaukee Tools as company
