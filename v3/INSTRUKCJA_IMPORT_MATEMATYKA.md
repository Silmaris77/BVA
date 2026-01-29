# Instrukcja importu lekcji matematyki do Supabase

## 🎯 Cel
Zaimportować 4 lekcje matematyki (Moduł 1: Liczby i Działania) do bazy Supabase.

## 📋 Przygotowane pliki

- **cleanup_math_lessons.sql** - Usuwa stare dane (duplikaty)
- **insert_math_path.sql** - Kompletny import (moduł + 4 lekcje + learning path)

## ⚠️ WAŻNE: Usunięte pliki
- ~~insert_math_lesson3.sql~~ - ZDUPLIKOWANY (Lekcja 3 już jest w insert_math_path.sql)
- ~~insert_math_lesson4.sql~~ - NIEPOTRZEBNY (Lekcja 4 też jest w insert_math_path.sql)

## 🚀 Kroki wykonania w Supabase

### 1️⃣ Wyczyść starą bazę (jeśli była)

W **Supabase → SQL Editor** uruchom:

```sql
-- v3/cleanup_math_lessons.sql
DELETE FROM lessons WHERE lesson_id IN (
    'math-g7-l1',
    'math-g7-l2', 
    'math-g7-l3',
    'math-g7-l4'
);

DELETE FROM learning_paths WHERE path_slug = 'math-grade-7';
```

### 2️⃣ Zaimportuj wszystko (1 plik!)

W **Supabase → SQL Editor** uruchom **CAŁY PLIK**:

```
v3/insert_math_path.sql
```

**Zawiera:**
- ✅ Moduł "Matematyka: Liczby i Działania"
- ✅ Lekcja 1: Liczby (math-g7-l1) - 16 kart
- ✅ Lekcja 2: Rozwinięcia dziesiętne (math-g7-l2) - 10 kart
- ✅ Lekcja 3: Zaokrąglanie i szacowanie (math-g7-l3) - 15 kart
- ✅ Lekcja 4: Dodawanie i odejmowanie (math-g7-l4) - 16 kart
- ✅ Learning Path "Matematyka - 7 klasa"

### 3️⃣ Weryfikacja

Sprawdź w Supabase Table Editor:

**Tabela `lessons`:**
```sql
SELECT lesson_id, title, duration_minutes, xp_reward 
FROM lessons 
WHERE lesson_id LIKE 'math-g7%'
ORDER BY lesson_id;
```

Powinieneś zobaczyć **4 rekordy**:
- math-g7-l1 | Liczby | 20 min | 100 XP
- math-g7-l2 | Rozwinięcia dziesiętne | 20 min | 100 XP
- math-g7-l3 | Zaokrąglanie i szacowanie | 25 min | 100 XP
- math-g7-l4 | Dodawanie i odejmowanie | 30 min | 120 XP

**Tabela `learning_paths`:**
```sql
SELECT path_slug, title, lesson_sequence 
FROM learning_paths 
WHERE path_slug = 'math-grade-7';
```

Powinieneś zobaczyć:
- path_slug: `math-grade-7`
- title: `Matematyka - 7 klasa`
- lesson_sequence: JSON z 4 lekcjami

## ✅ Gotowe!

Po wykonaniu tych kroków:
- Brak duplikatów ✓
- Wszystkie 4 lekcje w bazie ✓
- Learning path z poprawną kolejnością ✓

## 🐛 Troubleshooting

**Problem: "duplicate key value violates unique constraint"**
- Rozwiązanie: Uruchom ponownie `cleanup_math_lessons.sql`

**Problem: "Encountered two children with same key math-g7-l3"**
- Przyczyna: Duplikat w bazie
- Rozwiązanie: Cleanup → Re-import

**Problem: Lekcje nie widać w aplikacji**
- Sprawdź: `SELECT * FROM lessons WHERE lesson_id LIKE 'math%'`
- Upewnij się, że `module_id` = `d290f1ee-6c54-4b01-90e6-d701748f0851`
