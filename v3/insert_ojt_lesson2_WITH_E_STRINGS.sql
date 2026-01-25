-- Insert OJT Lesson 2 - Dollar-quoting + \n for newlines
-- Frontend needs preprocessing: content.replace(/\\n/g, '\n') before ReactMarkdown
DELETE FROM lessons WHERE lesson_id = 'ojt_lesson_2_model';

INSERT INTO lessons (
  lesson_id, 
  title, 
  description, 
  category, 
  difficulty, 
  duration_minutes, 
  xp_reward,
  content
)
VALUES (
  'ojt_lesson_2_model',
  'OJT (On-the-Job Training) - Model ASOLA',
  'Praktyczny przewodnik treningu w terenie dla sales managera. Jak rozwijać sprzedawców podczas wspólnych wizyt u klientów?',
  'Praktyka: Sales Management',
  'intermediate',
  25,
  260,
  $${
    "cards": [
      {
        "id": 1,
        "type": "hero",
        "title": "OJT: Trening w Terenie według Modelu ASOLA",
        "subtitle": "Jak przekształcić wspólne wizyty w efektywny rozwój sprzedawców?",
        "content": "Odkryj 5-etapowy model, który zamieni Cię z \"obserwatora\" w skutecznego coacha terenowego. Poznaj konkretne narzędzia do każdego etapu.",
        "theme": {
          "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          "image": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200"
        },
        "estimated_seconds": 30,
        "xp_points": 0
      },
      {
        "id": 2,
        "type": "data",
        "title": "Statystyki: Dlaczego OJT Działa?",
        "stats": [
          {
            "value": "85%",
            "label": "managerów uważa OJT za najskuteczniejszą metodę rozwoju sprzedaży",
            "trend": "up"
          },
          {
            "value": "3x",
            "label": "większa retencja wiedzy przy treningu w praktyce vs. szkolenie teoretyczne",
            "trend": "up"
          },
          {
            "value": "47%",
            "label": "wzrost wyników sprzedawców po wdrożeniu systematycznego OJT (badanie Sales Management Association)",
            "trend": "up"
          }
        ],
        "sources": ["Sales Management Association, 2023", "Corporate Executive Board"],
        "estimated_seconds": 60,
        "xp_points": 10
      },
      {
        "id": 3,
        "type": "content",
        "title": "Model ASOLA: Czym jest?",
        "content": "**ASOLA** to akronim 5-etapowego procesu OJT:\n\n**A**nalyze - analiza potrzeb\n**S**et the scene - kontraktowanie\n**O**bserve - obserwacja\n**L**earn - feedback i nauka\n**A**pply - praktyka\n\nTo NIE jest \"pojedź ze mną do klienta\". To ustrukturyzowana interwencja rozwojowa z jasnym celem, procesem i mierzalnymi rezultatami.\n\n💡 **Kluczowa różnica:**\n- ❌ **Zwykła wizyta:** \"Jade do klienta X, jedź ze mną\"\n- ✅ **OJT:** \"Pracujemy nad Twoim zamykaniem sprzedaży. Obserwuję 3 wizyty, notuję feedback, potem ćwiczymy i testujesz w czwartej\"",
        "callout": {
          "type": "info",
          "text": "🎯 **Cel OJT:** Rozwijać konkretną umiejętność przez praktykę + natychmiastowy feedback w realnym środowisku"
        },
        "estimated_seconds": 120,
        "xp_points": 15
      },
      {
        "id": 4,
        "type": "content",
        "title": "Etap 1: Analyze (Analiza Potrzeb)",
        "content": "**Czas:** 1-2 dni przed wyjazdem\n**Cel:** Zdiagnozować lukę kompetencyjną + wybrać focus area\n\n**Narzędzia:**\n\n1. **Performance data** (liczby z CRM)\n   Gdzie są spadki? (konwersja, średnia wartość zamówienia, liczba wizyt?)\n\n2. **Call review** (nagrania/notatki z rozmów)\n   Co konkretnie nie działa? (discovery, handling objections, closing?)\n\n3. **Rozmowa 1-on-1**\n   \"Nad czym chcesz popracować? Co Ci nie wychodzi?\"\n\n📋 **Output:** Konkretna umiejętność do rozwinięcia (np. \"pytania odkrywające potrzeby\" lub \"reagowanie na obiekcję cenową\")",
        "callout": {
          "type": "warning",
          "text": "⚠️ **Częsty błąd:** Wybranie zbyt szerokiego celu (\"poprawić sprzedaż\"). Wybierz JEDNĄ mikro-umiejętność!"
        },
        "estimated_seconds": 120,
        "xp_points": 15
      },
      {
        "id": 5,
        "type": "content",
        "title": "Etap 2: Set the Scene (Kontraktowanie)",
        "content": "**Czas:** 10-15 minut na początku wspólnego dnia\n**Cel:** Stworzyć fundament zaufania + jasne oczekiwania\n\n**Struktura rozmowy:**\n\n1. **Przypomnienie celu**\n   \"Dzisiaj skupiamy się na Twoich pytaniach odkrywających. Zgoda?\"\n\n2. **Rola managera**\n   \"Będę obserwować i robić notatki. NIE wskakuję do rozmowy, chyba że poprosisz\"\n\n3. **Ustalenie celów rozwojowych**\n   Nad czym będziemy pracować? (1-2 konkretne umiejętności)\n\n4. **Plan dnia**\n   Co konkretnie zrobimy? (lista klientów/zadań, harmonogram)",
        "callout": {
          "type": "warning",
          "text": "⚠️ **Częsty błąd:** Pomijanie kontraktowania i wskakiwanie od razu w obserwację. Bez wyraźnej zgody pracownika i wspólnych celów, trening zamienia się w stresującą kontrolę!"
        },
        "remember": {
          "title": "Pamiętaj:",
          "items": [
            "Cele rozwojowe powinny być powiązane z celami biznesowymi (np. \"poprawić zamykanie sprzedaży\" → zwiększenie konwersji)"
          ]
        },
        "estimated_seconds": 120,
        "xp_points": 10
      }
    ]
  }$$::jsonb
);
