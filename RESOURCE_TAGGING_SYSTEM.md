# System Tagowania Zasobów i Edycji Użytkowników

**Data utworzenia:** 2025-12-03  
**Wersja:** 1.0

## Przegląd

Nowy system zastępuje sztywne listy ID zasobów w `company_templates.json` elastycznym systemem tagowania, który pozwala przypisywać zasoby do wielu grup jednocześnie.

## Struktura

### 1. Pliki konfiguracyjne

**`config/resource_tags.json`**
- Centralna baza tagów dla wszystkich zasobów
- Struktura:
  ```json
  {
    "companies": [...],  // Lista grup (General, Warta, Heinz, Milwaukee, Degen)
    "lessons": {...},     // Mapa: lesson_id -> [tagi]
    "business_games_scenarios": {...},
    "business_games_types": {...},
    "inspirations_categories": {...}
  }
  ```

### 2. Moduły pomocnicze

**`utils/resource_access.py`**
- Główny moduł zarządzający dostępem do zasobów
- Funkcje:
  - `has_access_to_resource()` - sprawdza dostęp użytkownika do zasobu
  - `get_resource_tags()` - pobiera tagi zasobu
  - `set_resource_tags()` - ustawia tagi zasobu
  - `get_accessible_resources()` - lista zasobów dostępnych dla użytkownika
  - `filter_resources_by_tags()` - filtruje listę zasobów według dostępu

### 3. Panel administracyjny

**Nowa zakładka: "Tagowanie Zasobów"** (`views/admin.py`)
- Wizualny edytor tagów dla zasobów
- Przypisywanie zasobów do grup za pomocą checkboxów
- Podgląd wszystkich tagów

**Rozszerzona zakładka: "Użytkownicy"**
- Pod-zakładka "Edycja użytkownika"
- Zmiana grupy użytkownika (company)
- Edycja custom permissions (JSON)
- Podgląd finalnych uprawnień

## Grupy użytkowników (Companies)

| Kod | Nazwa | Opis | Kolor |
|-----|-------|------|-------|
| `General` | Ogólne | Zasoby dostępne dla wszystkich | #6c757d |
| `Warta` | Warta | Ubezpieczenia | #dc3545 |
| `Heinz` | Heinz | FMCG | #e74c3c |
| `Milwaukee` | Milwaukee | B2B/narzędzia | #f39c12 |
| `Degen` | Degen | Trading/crypto | #9b59b6 |

## Jak działa system tagowania

### Przypisywanie tagów

1. Admin wchodzi do zakładki "Tagowanie Zasobów"
2. Wybiera typ zasobu (lekcje/inspiracje/BG)
3. Wybiera konkretny zasób
4. Zaznacza checkboxy grup, które mają mieć dostęp
5. Zapisuje zmiany

### Sprawdzanie dostępu

System sprawdza dostęp użytkownika w następującej kolejności:

1. **Czy zasób ma tag "General"?** → Dostęp dla wszystkich
2. **Czy użytkownik ma custom permissions?** → Użyj starego systemu (company_templates.json)
3. **Czy zasób ma tag odpowiadający company użytkownika?** → Dostęp

### Przykład

```python
# Lekcja "DEGEN_1_Trading_Psychology" ma tagi: ["Degen"]
# Użytkownik ma company="Degen"

from utils.resource_access import has_access_to_resource

has_access = has_access_to_resource(
    'lessons', 
    'DEGEN_1_Trading_Psychology', 
    user_data
)
# Zwróci: True
```

## Migracja ze starego systemu

### Stary system (company_templates.json)
```json
{
  "Degen": {
    "content": {
      "lessons": ["DEGEN_1_Trading_Psychology"],
      ...
    }
  }
}
```

### Nowy system (resource_tags.json)
```json
{
  "lessons": {
    "DEGEN_1_Trading_Psychology": ["Degen"]
  }
}
```

### Zalety nowego systemu

1. **Wielokrotne przypisanie** - zasób może należeć do wielu grup
   ```json
   "sales": ["General", "Warta", "Milwaukee"]
   ```

2. **Centralizacja** - wszystkie tagi w jednym miejscu

3. **Łatwiejsza edycja** - wizualny interfejs w panelu admina

4. **Backwards compatible** - stary system (custom permissions) nadal działa

## Integracja z istniejącym kodem

### views/lesson.py
```python
from utils.resource_access import has_access_to_resource

# Filtrowanie lekcji
accessible_lessons = [
    lesson for lesson in all_lessons
    if has_access_to_resource('lessons', lesson['id'], user_data)
]
```

### views/business_games.py
```python
from utils.resource_access import has_access_to_resource

# Sprawdzenie dostępu do scenariusza
if has_access_to_resource('business_games_scenarios', scenario_id, user_data):
    # Pokaż scenariusz
```

### views/inspirations.py
```python
from utils.resource_access import has_access_to_resource

# Filtrowanie kategorii inspiracji
accessible_categories = [
    cat for cat in categories
    if has_access_to_resource('inspirations_categories', cat, user_data)
]
```

## Workflow admina

### Utworzenie nowego użytkownika

1. Admin wchodzi do zakładki "Zarządzanie"
2. Tworzy nowe konto i wybiera grupę (np. Degen)
3. Użytkownik jest zapisywany z `company="Degen"`
4. System automatycznie filtruje zasoby według tagów

### Edycja istniejącego użytkownika

1. Admin wchodzi do zakładki "Użytkownicy" → "Edycja użytkownika"
2. Wybiera użytkownika z listy
3. Zmienia grupę lub dodaje custom permissions
4. Zapisuje zmiany
5. Użytkownik natychmiast widzi nowe zasoby

### Tagowanie nowej lekcji

1. Admin dodaje nowy plik lekcji do `data/lessons/`
2. Wchodzi do "Tagowanie Zasobów" → "Lekcje"
3. Wybiera nową lekcję
4. Zaznacza grupy (np. "Degen")
5. Zapisuje - lekcja jest dostępna tylko dla Degen

## FAQ

### Q: Co jeśli zasób nie ma żadnych tagów?
A: Domyślnie zasób dostaje tag `["General"]` przy pierwszym zapisie.

### Q: Czy mogę przypisać zasób do kilku grup?
A: Tak! Wystarczy zaznaczyć kilka checkboxów w panelu tagowania.

### Q: Co się stanie ze starymi użytkownikami z custom permissions?
A: System najpierw sprawdza custom permissions, więc stare ustawienia będą działać.

### Q: Jak oznaczyć zasób jako dostępny dla wszystkich?
A: Dodaj tag "General" lub dodaj tagi wszystkich grup.

### Q: Czy mogę edytować tagi bez restartowania aplikacji?
A: Tak, zmiany są natychmiastowe. Wystarczy odświeżyć stronę.

## Roadmap

### Planowane funkcje:

- [ ] Bulk tagging - przypisanie wielu zasobów na raz
- [ ] Import/export tagów do CSV
- [ ] Historia zmian tagów
- [ ] Automatyczne sugestie tagów na podstawie nazwy zasobu
- [ ] Kopiowanie tagów między zasobami
- [ ] Walidacja tagów przed zapisem
- [ ] Powiadomienia dla użytkowników o nowych zasobach

## Troubleshooting

### Problem: Użytkownik nie widzi lekcji mimo prawidłowej grupy
**Rozwiązanie:** Sprawdź w panelu "Tagowanie Zasobów" czy lekcja ma odpowiedni tag.

### Problem: Cache nie odświeża się
**Rozwiązanie:** Restart Streamlit lub wymuś reload przez `st.cache_data.clear()`.

### Problem: Błąd JSON w custom permissions
**Rozwiązanie:** Użyj walidatora JSON online przed zapisem.

---

**Kontakt:** Admin Panel → Zakładka "Tagowanie Zasobów"  
**Dokumentacja API:** `utils/resource_access.py` (docstringi)
