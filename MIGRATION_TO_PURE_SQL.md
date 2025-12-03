# Migracja na Pure SQL - 3 grudnia 2025

## Podsumowanie

Usunięto dual-system JSON+SQL i przejście na **czysty SQL** jako jedyne źródło prawdy dla danych użytkowników.

## Zmiany

### Nowy moduł: `data/users_sql.py`
- **Pure SQL** - bez żadnych operacji na JSON
- Pełna kompatybilność API z poprzednimi `data.users` i `data.users_new`
- Funkcje:
  - `login_user(username, password)` - logowanie z SQL
  - `register_user(username, password, **kwargs)` - rejestracja do SQL
  - `load_user_data()` - load wszystkich użytkowników z SQL
  - `save_user_data(users_data)` - save wszystkich (deprecated)
  - `save_single_user(username, user_data)` - save pojedynczego
  - `get_current_user_data(username)` - pobierz dane użytkownika
  - `update_user_xp(username, xp_amount)` - aktualizuj XP

### Zaktualizowane pliki

1. **views/login.py**
   - `from data.users import` → `from data.users_sql import`
   - Login i rejestracja teraz z SQL

2. **views/lesson.py**
   - `from data.users import` → `from data.users_sql import`
   - Lekcje czytają/zapisują do SQL

3. **views/admin.py**
   - `from data.users_new import` → `from data.users_sql import`
   - Tworzenie użytkowników **tylko w SQL**
   - Usunięto zapis do JSON

4. **views/business_games.py**
   - Wszystkie `from data.users_new import` → `from data.users_sql import`
   - Business Games czytają/zapisują do SQL

5. **main.py**
   - `from data.users_new import` → `from data.users_sql import`

## Co zostało usunięte

- ❌ Zapis do `users_data.json` przy tworzeniu użytkownika
- ❌ Dual-write logic w repository
- ❌ Dependency na `data.users_new` (adapter nad repository)

## Co pozostało (do przyszłej migracji)

- `data/users.py` - stary moduł (używany tylko w testach)
- `data/users_new.py` - adapter (można usunąć w przyszłości)
- `data/repositories/user_repository.py` - skomplikowana logika dual-write
- `users_data.json` - plik pozostaje jako backup, ale nie jest używany

## Korzyści

✅ **Jednoznaczne źródło prawdy** - tylko SQL
✅ **Brak konfliktów** - nie ma już problemów z synchronizacją JSON↔SQL
✅ **Prostszy kod** - mniej warstw abstrakcji
✅ **Lepsza wydajność** - brak podwójnego zapisu
✅ **Łatwiejsze debugowanie** - jedno miejsce do sprawdzenia danych

## Migracja danych

Jeśli masz użytkowników w `users_data.json`, którzy nie są w SQL:

```python
# Jednorazowy skrypt migracji
import json
from database.models import User
from database.connection import session_scope
import uuid

with open('users_data.json', 'r', encoding='utf-8') as f:
    users_data = json.load(f)

with session_scope() as session:
    for username, data in users_data.items():
        # Sprawdź czy istnieje
        existing = session.query(User).filter_by(username=username).first()
        if not existing:
            # Migruj
            user = User.from_dict(username, data)
            session.add(user)
    
    session.commit()
    print(f"Zmigrowano {len(users_data)} użytkowników")
```

## Testing

1. ✅ Logowanie działa
2. ✅ Tworzenie konta przez admin działa
3. ✅ Lekcje zapisują postęp
4. ✅ Business Games zapisują dane
5. ✅ System uprawnień działa (Warta/Heinz/Milwaukee)

## Następne kroki (opcjonalne)

1. Usuń `data/users_new.py` (jeśli nic go nie używa)
2. Usuń `data/users.py` (stary moduł)
3. Zmień testy żeby używały `data.users_sql`
4. Usuń `data/repositories/user_repository.py` (już niepotrzebny)
5. Zarchiwizuj `users_data.json` jako backup

## Rollback (jeśli potrzebny)

Jeśli coś pójdzie nie tak, przywróć poprzedni stan:

```bash
git checkout views/login.py views/lesson.py views/admin.py views/business_games.py main.py
```

I usuń `data/users_sql.py`.
