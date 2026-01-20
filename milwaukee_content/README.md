# Milwaukee Content Source - Struktura i Przewodnik

## 📁 Omówienie Struktury

Ten folder zawiera wszystkie materiały źródłowe użyte do generowania contentu dla Milwaukee Tools w aplikacji BrainVenture Academy.

---

## 🗂️ Organizacja Folderów

### `00_context/` - Ogólny Kontekst i Fundament
**Cel:** Podstawowe informacje o firmie, grupie docelowej i celach edukacyjnych.

**Pliki:**
- `company_info.md` - O Milwaukee: historia, wartości, mission statement
- `target_audience.md` - Profile uczniów: role, poziomy, potrzeby
- `learning_objectives.md` - Cele edukacyjne, KPI, oczekiwane rezultaty
- `branding_guidelines.md` - Kolory, logo, tone of voice, przykłady komunikacji

**Kiedy używać:** Zacznij tutaj! Te pliki definiują "dlaczego" i "dla kogo" tworzysz content.

---

### `01_products/` - Informacje o Produktach
**Cel:** Kompletna baza wiedzy o produktach Milwaukee.

**Pliki:**
- `catalog.json` - Strukturalizowana lista wszystkich produktów
- `competitive_analysis.md` - Milwaukee vs konkurencja (DeWalt, Makita, Bosch)

**Subfolder `categories/`:**
- Osobne pliki `.md` dla każdej kategorii produktów
- Przykłady: `drills.md`, `impact_drivers.md`, `batteries.md`, `chargers.md`

**Format rekomendowany:**
```markdown
# Kategoria: Wiertarki

## Modele
### M18 FUEL™ Hammer Drill/Driver
- SKU: 2804-20
- Moc: 1200 in-lbs
- Prędkość: 0-550 / 0-2,000 RPM
- Cena sugerowana: $XXX
- Kluczowe features: ...
- Use cases: ...
```

---

### `02_lessons/` - Materiały Źródłowe dla Lekcji
**Cel:** Surowe materiały, które zostaną przekonwertowane na lekcje w aplikacji.

**Struktura:**
```
module_X_nazwa/
├── lesson_XX_title.md      # Treść lekcji
├── quiz_questions.json     # Pytania quizowe
├── assets/                 # Media dla tego modułu
│   ├── diagrams/
│   ├── screenshots/
│   └── videos/
└── notes.md               # Notatki i TODO
```

**Moduły (przykładowe):**
- `module_1_foundations` - Podstawy: historia, wartości, portfolio
- `module_2_product_knowledge` - Szczegółowa wiedza produktowa
- `module_3_sales_techniques` - Techniki sprzedaży, negocjacje
- `module_4_advanced` - Zaawansowane: B2B, relationship building

**Format lekcji:**
```markdown
# Tytuł Lekcji

## Metadata
- Kategoria: sales / product / safety
- Difficulty: 1-5
- Estimated Time: 15min
- Prerequisites: [lesson_ids]
- XP Reward: 50

## Karta 1: Hero
**Type:** hero
**Title:** ...
**Content:** ...
**Image:** path/to/image.jpg

## Karta 2: Content
**Type:** content
**Title:** ...
**Content:** ...
**Media Type:** image/video/diagram

## Karta 3: Quiz
**Type:** quiz
**Question:** ...
**Options:**
- A)
- B)
- C)
- D)
**Correct Answer:** B
**Explanation:** ...
```

---

### `03_engrams/` - Definicje Engram'ów
**Cel:** Specyfikacje engram'ów (ulepszeń) dla użytkowników.

**Pliki:**
- `engrams_list.md` - Overview wszystkich engram'ów
- `specs/*.json` - Szczegółowe specyfikacje każdego engramu

**Format JSON:**
```json
{
  "id": "milwaukee_expert",
  "name": "Milwaukee Expert",
  "description": "Deep knowledge of entire product line",
  "category": "learning",
  "xp_cost": 500,
  "level_required": 5,
  "effects": [
    {
      "type": "unlock_content",
      "value": "advanced_products",
      "description": "Access to advanced product specs"
    },
    {
      "type": "xp_multiplier",
      "value": 1.15,
      "description": "+15% XP on product knowledge lessons"
    }
  ],
  "icon": "graduation-cap"
}
```

---

### `04_tools/` - Specyfikacje Narzędzi
**Cel:** Interaktywne narzędzia (kalkulatory, selektory) dla użytkowników.

**Pliki:**
- Każde narzędzie = osobny plik `.md` z specyfikacją
- `data/` - JSON files z danymi dla kalkulatorów

**Format specyfikacji:**
```markdown
# Tool: Product Selector

## Description
Helps sales reps choose the right Milwaukee tool based on customer's job requirements.

## Type
selector / calculator / generator

## Inputs
1. Job Type (dropdown: construction, woodworking, metalwork, automotive)
2. Power Source (dropdown: corded, M18, M12)
3. Budget Range (slider: $50-$500)

## Logic
- If job_type = "construction" AND power = "M18" => Recommend M18 FUEL series
- ...

## Output
- List of 3-5 recommended products
- Comparison table
- Link to detailed specs

## Data Source
`data/product_selector_matrix.json`
```

---

### `05_resources/` - Zasoby do Pobrania
**Cel:** Dokumenty, tabele, skrypty które użytkownicy mogą pobrać i używać w pracy.

**Subfolders:**
- `battle_cards/` - Quick comparison Milwaukee vs competition
- `spec_sheets/` - Karty specyfikacji produktów (PDF lub MD)
- `sales_scripts/` - Scenariusze rozmów z klientami
- `templates/` - Formularze, oferty, dokumenty do wypełnienia

**Format Battle Card:**
```markdown
# Milwaukee M18 FUEL vs DeWalt 20V MAX

## Head-to-Head
| Feature | Milwaukee M18 FUEL | DeWalt 20V MAX |
|---------|-------------------|----------------|
| Max Torque | 1,200 in-lbs | 1,000 in-lbs |
| Battery Life | 2x longer | Baseline |
| Warranty | 5 years | 3 years |
| Price | $XXX | $XXX |

## Key Talking Points
- "Milwaukee delivers 20% more torque..."
- "Our battery lasts twice as long..."

## Handling Objections
**Objection:** "DeWalt is cheaper"
**Response:** "Let me show you the total cost of ownership..."
```

---

### `06_drills/` - Ćwiczenia i Quizy
**Cel:** Praktyczne ćwiczenia dla rozwijania umiejętności.

**Typy:**
- Role-play scenarios (symulacje rozmów)
- Flashcards (szybkie powtórki)
- Product identification quizzes
- Troubleshooting challenges

**Format:**
```markdown
# Drill: Cold Call Practice

## Type
roleplay

## Scenario
You're calling a construction company that currently uses DeWalt tools exclusively. Your goal is to book a 15-minute product demo.

## Customer Profile
- Name: John, Procurement Manager
- Company: BuildCo (150 employees)
- Current pain: Battery life issues
- Budget: Medium

## Your Objective
1. Build rapport
2. Identify pain points
3. Position Milwaukee as solution
4. Book demo appointment

## Evaluation Criteria
- Did you ask discovery questions? (Y/N)
- Did you handle objections? (Y/N)
- Did you close for next step? (Y/N)

## Sample Responses
[Provide examples of good/bad approaches]
```

---

### `07_assets/` - Media Assets
**Cel:** Wszystkie obrazy, video, audio używane w contentcie.

**Subfolders:**
- `images/` - Product photos, diagrams, infographics
- `videos/` - Tutorial videos, product demos (or links to them)
- `documents/` - Source PDFs, presentations, datasheets

**Naming Convention:**
- Use descriptive names: `m18_fuel_drill_side_view.jpg`
- Include product SKU if applicable: `2804-20_features.png`
- Dates for versions: `catalog_2024_q1.pdf`

---

## 🔄 Workflow: Od Źródła do Aplikacji

### Krok 1: Zbierz Informacje
1. Wypełnij pliki w `00_context/`
2. Zgromadź dane produktowe w `01_products/`
3. Zbierz media w `07_assets/`

### Krok 2: Planuj Strukturę
1. Określ moduły i lekcje w `02_lessons/`
2. Zaplanuj engramy w `03_engrams/`
3. Zdefiniuj potrzebne narzędzia w `04_tools/`

### Krok 3: Twórz Content
1. Wypełnij markdown files dla lekcji
2. Stwórz specyfikacje dla narzędzi
3. Przygotuj zasoby do pobrania

### Krok 4: Konwersja do JSON
**Opcja A:** Ręczna
- Skopiuj content z MD do formularza w Admin Panel

**Opcja B:** Automatyczna (przyszłość)
- Skrypt konwertujący MD → JSON
- Import hurtowy przez API

### Krok 5: Upload do Aplikacji
1. Zaloguj się do Admin Panel
2. Utwórz lekcje/engramy/tools/resources
3. Testuj z perspektywy użytkownika

---

## 📝 Conventions & Best Practices

### Markdown Formatting
- Używaj `#` dla nagłówków (H1 = #, H2 = ##, itd.)
- **Bold** dla kluczowych terminów
- *Italics* dla emfazy
- Bullet lists dla wyliczeń
- Numbered lists dla kroków sekwencyjnych
- Code blocks dla przykładów kodu/formul

### Tone of Voice
- **Dla Pracowników Milwaukee:** Profesjonalny, wspierający, motywujący
- **O Produkcie:** Dumny, pewny, oparty na faktach
- **O Konkurencji:** Obiektywny, fair, oparty na danych
- Unikaj: żargonu bez wyjaśnienia, negatywnego tonu, przesadnych obietnic

### File Naming
- Lowercase z underscores: `product_selector.md`
- Prefix z numerami dla kolejności: `01_history.md`, `02_values.md`
- Daty w formacie ISO: `catalog_2024-01-15.json`

### Version Control
- Ten folder powinien być w git (jeśli używasz)
- Commit po każdej znaczącej zmianie
- Używaj branch'y dla większych zmian
- Tag release'y (np. `v1.0-milwaukee-launch`)

---

## 🆘 FAQ

### "Jak wielki powinien być jeden plik lekcji?"
**Odpowiedź:** 1 lekcja = 1 plik. Lekcja powinna trwać 10-30 minut, czyli 5-15 kart.

### "W jakim formacie trzymać obrazy?"
**Odpowiedź:** JPG dla zdjęć, PNG dla diagramów/screenshots, SVG dla ikon jeśli możliwe.

### "Czy mogę używać zewnętrznych linków do video?"
**Odpowiedź:** Tak! YouTube, Vimeo, Loom - wszystko działa. Zapisz link w pliku MD.

### "Co jeśli produkt się zmieni?"
**Odpowiedź:** Zaktualizuj plik w `01_products/`, potem zaktualizuj dotknięte lekcje. Git history pokaże co się zmieniło.

### "Kto powinien wypełniać ten content?"
**Odpowiedź:**
- `00_context/` - Manager/Training Lead
- `01_products/` - Product Manager/Marketing
- `02_lessons/` - Instructor/SME
- `03_engrams/` - Gamification Designer
- `04_tools/` - Technical Writer
- `05_resources/` - Sales Enablement
- `06_drills/` - Learning Designer

Ale w praktyce: każdy może! Content collaboration encouraged.

---

## 🚀 Quick Start

### Jeśli zaczynasz od zera:
1. Wypełnij `00_context/company_info.md` (10 min)
2. Wypełnij `00_context/target_audience.md` (10 min)
3. Stwórz listę produktów w `01_products/catalog.json` (30 min)
4. Zaplanuj pierwszą lekcję w `02_lessons/module_1_foundations/lesson_01_intro.md` (1h)
5. Review i iteruj

### Jeśli masz istniejące materiały:
1. Przenieś PDFs/PPTs do `07_assets/documents/`
2. Ekstraktuj content do odpowiednich folderów
3. Restrukturyzuj według rekomendowanego formatu
4. Dodaj metadata i quizy

---

## 📞 Support

Masz pytania? Potrzebujesz pomocy z strukturą contentu?

- Discord: [Link do kanału]
- Email: content@brainventure.academy
- Wiki: [Link do wiki z przykładami]

---

**Powodzenia w tworzeniu world-class contentu dla Milwaukee! 🔧⚡**
