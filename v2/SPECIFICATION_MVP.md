# BVA v2 - Specyfikacja MVP
## Lekcje + System Progressu

**Data:** 6 stycznia 2026  
**Wersja:** 1.0  
**Scope:** Minimum Viable Product - Lekcje i śledzenie postępów

---

## 📋 Spis Treści
1. [Przegląd](#przegląd)
2. [Architektura Systemu](#architektura-systemu)
3. [Schemat Bazy Danych](#schemat-bazy-danych)
4. [API Endpoints](#api-endpoints)
5. [User Flow](#user-flow)
6. [Funkcjonalności](#funkcjonalności)
7. [Technologie](#technologie)

---

## 🎯 Przegląd

### Cele MVP
- ✅ Użytkownik może się zalogować
- ✅ Przeglądać listę dostępnych lekcji
- ✅ Oglądać lekcje video
- ✅ Śledzić swój progres (% ukończenia)
- ✅ Zdobywać XP i poziomy
- ✅ Widzieć swoją statystykę na dashboardzie

### Poza zakresem MVP (v2.0+)
- ❌ Business Games
- ❌ Milwaukee Tool
- ❌ Fiszki
- ❌ Inspiracje
- ❌ System rankingów
- ❌ Admin panel (podstawowe zarządzanie przez SQLite)

---

## 🏗️ Architektura Systemu

```
┌─────────────────────────────────────────────────────────────┐
│                         UŻYTKOWNIK                          │
│                      (Przeglądarka)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP/HTTPS
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   FRONTEND (Next.js 15)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Pages:                                              │  │
│  │  • /login          - Logowanie                       │  │
│  │  • /dashboard      - Dashboard (stats, aktywność)    │  │
│  │  • /lessons        - Lista lekcji                    │  │
│  │  • /lessons/[id]   - Odtwarzacz lekcji              │  │
│  │  • /profile        - Profil użytkownika             │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Services:                                           │  │
│  │  • api.ts          - Axios client + endpoints        │  │
│  │  • auth.ts         - JWT handling, localStorage      │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ REST API (JSON)
                     │ Authorization: Bearer {JWT}
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  BACKEND (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Routers:                                        │  │
│  │  • /auth/*         - Login, register, refresh token  │  │
│  │  • /users/*        - User profile, stats             │  │
│  │  • /lessons/*      - CRUD lekcji, progres            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Middleware:                                         │  │
│  │  • CORS                                              │  │
│  │  • JWT Authentication                                │  │
│  │  • Error handling                                    │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Business Logic:                                     │  │
│  │  • XP calculation                                    │  │
│  │  • Level progression                                 │  │
│  │  • Lesson completion tracking                        │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ SQLAlchemy ORM
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  BAZA DANYCH (SQLite)                       │
│  Tabele:                                                    │
│  • users              - Dane użytkowników                   │
│  • lessons            - Katalog lekcji                      │
│  • lesson_progress    - Progres użytkowników w lekcjach    │
│  • activity_logs      - Historia aktywności                │
└─────────────────────────────────────────────────────────────┘
```

---

## 💾 Schemat Bazy Danych

### Diagram ERD (Entity Relationship Diagram)

```
┌─────────────────────────────────┐
│           USERS                 │
├─────────────────────────────────┤
│ PK  id (INT)                    │
│     user_id (UUID)              │
│ UQ  username (VARCHAR)          │
│     password_hash (VARCHAR)     │
│ UQ  email (VARCHAR)             │
│     full_name (VARCHAR)         │
│     xp (INT) DEFAULT 0          │
│     level (INT) DEFAULT 1       │
│     degencoins (INT) DEFAULT 0  │
│     degen_type (VARCHAR)        │
│     company (VARCHAR)           │
│     avatar_url (VARCHAR)        │
│     joined_date (DATE)          │
│     last_login (DATETIME)       │
│     created_at (DATETIME)       │
│     updated_at (DATETIME)       │
└────────────┬────────────────────┘
             │
             │ 1:N
             │
┌────────────▼────────────────────┐
│      LESSON_PROGRESS            │
├─────────────────────────────────┤
│ PK  id (INT)                    │
│ FK  user_id (INT) → users.id    │
│ FK  lesson_id (STR) → lessons.id│
│     status (ENUM)               │
│       • not_started             │
│       • in_progress             │
│       • completed               │
│     progress_percent (INT)      │
│     time_spent (INT) seconds    │
│     last_position (INT) seconds │
│     completed_at (DATETIME)     │
│     started_at (DATETIME)       │
│     updated_at (DATETIME)       │
└────────────┬────────────────────┘
             │
             │ N:1
             │
┌────────────▼────────────────────┐
│          LESSONS                │
├─────────────────────────────────┤
│ PK  id (VARCHAR) "intro-1"      │
│     title (VARCHAR)             │
│     description (TEXT)          │
│     category (VARCHAR)          │
│     video_url (VARCHAR)         │
│     thumbnail_url (VARCHAR)     │
│     duration (INT) seconds      │
│     xp_reward (INT) DEFAULT 100 │
│     difficulty (ENUM)           │
│       • Beginner                │
│       • Intermediate            │
│       • Advanced                │
│       • Expert                  │
│     order (INT) - kolejność     │
│     is_published (BOOL)         │
│     created_at (DATETIME)       │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│       ACTIVITY_LOGS             │
├─────────────────────────────────┤
│ PK  id (INT)                    │
│ FK  user_id (INT) → users.id    │
│     action_type (VARCHAR)       │
│       • lesson_started          │
│       • lesson_completed        │
│       • xp_gained               │
│       • level_up                │
│     description (TEXT)          │
│     metadata (JSON)             │
│     timestamp (DATETIME)        │
└─────────────────────────────────┘
```

### Relacje:
- **Users 1:N Lesson_Progress** - Użytkownik ma wiele wpisów progresowych
- **Lessons 1:N Lesson_Progress** - Lekcja ma wiele wpisów progresowych (różni użytkownicy)
- **Users 1:N Activity_Logs** - Użytkownik ma wiele logów aktywności

---

## 🔌 API Endpoints

### Autentykacja (`/auth`)

| Method | Endpoint | Opis | Request | Response |
|--------|----------|------|---------|----------|
| POST | `/auth/login` | Logowanie | `{username, password}` | `{access_token, token_type, user}` |
| POST | `/auth/refresh` | Odświeżenie tokenu | `{refresh_token}` | `{access_token}` |
| POST | `/auth/logout` | Wylogowanie | - | `{message}` |
| GET | `/auth/me` | Dane zalogowanego użytkownika | - | `{user}` |

### Użytkownicy (`/users`)

| Method | Endpoint | Opis | Auth | Response |
|--------|----------|------|------|----------|
| GET | `/users/me` | Mój profil | ✅ | `{id, username, email, xp, level, ...}` |
| PUT | `/users/me` | Aktualizuj profil | ✅ | `{updated_user}` |
| GET | `/users/me/stats` | Moje statystyki | ✅ | `{total_lessons, completed, xp, level, ...}` |
| GET | `/users/me/activity` | Moja aktywność | ✅ | `[{action, timestamp, ...}]` |

### Lekcje (`/lessons`)

| Method | Endpoint | Opis | Auth | Response |
|--------|----------|------|------|----------|
| GET | `/lessons` | Lista lekcji | ✅ | `[{id, title, category, ...}]` |
| GET | `/lessons?category=X` | Filtruj po kategorii | ✅ | `[...]` |
| GET | `/lessons/{id}` | Szczegóły lekcji | ✅ | `{id, title, video_url, ...}` |
| GET | `/lessons/{id}/progress` | Mój progres w lekcji | ✅ | `{status, progress_percent, ...}` |
| POST | `/lessons/{id}/start` | Rozpocznij lekcję | ✅ | `{progress_id}` |
| PUT | `/lessons/{id}/progress` | Zaktualizuj progres | ✅ | `{updated_progress}` |
| POST | `/lessons/{id}/complete` | Ukończ lekcję | ✅ | `{xp_gained, new_level, ...}` |

### Przykładowe requesty/responses

**POST /auth/login**
```json
Request:
{
  "username": "admin",
  "password": "admin123"
}

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@bva.pl",
    "xp": 1050,
    "level": 2,
    "avatar_url": null
  }
}
```

**GET /lessons**
```json
Response (200):
[
  {
    "id": "intro-1",
    "title": "Wprowadzenie do Akademii",
    "description": "Poznaj misję BVA...",
    "category": "Onboarding",
    "thumbnail_url": "/images/intro.jpg",
    "duration": 300,
    "xp_reward": 50,
    "difficulty": "Beginner",
    "my_progress": {
      "status": "completed",
      "progress_percent": 100
    }
  },
  {
    "id": "strat-1",
    "title": "Strategia Błękitnego Oceanu",
    "category": "Strategia",
    "duration": 600,
    "xp_reward": 150,
    "difficulty": "Intermediate",
    "my_progress": {
      "status": "in_progress",
      "progress_percent": 45
    }
  }
]
```

**POST /lessons/{id}/complete**
```json
Response (200):
{
  "lesson_id": "intro-1",
  "xp_gained": 50,
  "total_xp": 1100,
  "new_level": 2,
  "leveled_up": false,
  "completed_at": "2026-01-06T17:30:00Z"
}
```

---

## 🔄 User Flow Diagrams

### 1. Login Flow
```
┌──────────┐
│  START   │
└────┬─────┘
     │
     ▼
┌─────────────────┐
│ Otwórz /login   │
└────┬────────────┘
     │
     ▼
┌─────────────────────────┐
│ Wprowadź username/pass  │
└────┬────────────────────┘
     │
     ▼
┌─────────────────────────┐       ┌──────────────┐
│ POST /auth/login        │──────▶│ Backend      │
└────┬────────────────────┘       │ weryfikacja  │
     │                             └──────┬───────┘
     │                                    │
     ▼                                    │
┌─────────────────────────┐              │
│ Otrzymaj JWT token      │◀─────────────┘
└────┬────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ Zapisz w localStorage   │
└────┬────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ Przekieruj na /dashboard│
└────┬────────────────────┘
     │
     ▼
┌──────────┐
│   END    │
└──────────┘
```

### 2. Lesson Viewing Flow
```
┌──────────┐
│  START   │
└────┬─────┘
     │
     ▼
┌─────────────────────────┐
│ Dashboard: Kliknij      │
│ "Przeglądaj lekcje"     │
└────┬────────────────────┘
     │
     ▼
┌─────────────────────────┐       ┌──────────────┐
│ GET /lessons            │──────▶│ Backend      │
└────┬────────────────────┘       │ pobiera dane │
     │                             └──────┬───────┘
     │                                    │
     ▼                                    │
┌─────────────────────────┐              │
│ Wyświetl listę lekcji   │◀─────────────┘
│ (z progressem)          │
└────┬────────────────────┘
     │
     │ Użytkownik wybiera lekcję
     ▼
┌─────────────────────────┐
│ GET /lessons/{id}       │
└────┬────────────────────┘
     │
     ▼
┌─────────────────────────┐
│ Wyświetl odtwarzacz     │
│ • Video player          │
│ • Opis lekcji           │
│ • Progress bar          │
└────┬────────────────────┘
     │
     │ Co 30 sekund podczas oglądania
     ▼
┌─────────────────────────┐
│ PUT /lessons/{id}/progress│
│ {progress_percent: 60}  │
└────┬────────────────────┘
     │
     │ Po ukończeniu (100%)
     ▼
┌─────────────────────────┐       ┌──────────────┐
│ POST /lessons/{id}/complete│───▶│ Backend      │
└────┬────────────────────┘       │ • Doda XP    │
     │                             │ • Check level│
     │                             └──────┬───────┘
     ▼                                    │
┌─────────────────────────┐              │
│ Pokaż gratulacje        │◀─────────────┘
│ +50 XP!                 │
└────┬────────────────────┘
     │
     ▼
┌──────────┐
│   END    │
└──────────┘
```

### 3. Progress Tracking
```
User oglada video
       │
       ▼
┌─────────────────┐
│ Video event:    │
│ timeupdate      │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Każde 30s:      │
│ Oblicz %        │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ PUT progress    │
│ {               │
│   percent: 45,  │
│   position: 270 │
│ }               │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Backend:        │
│ UPDATE DB       │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Jeśli 100%:     │
│ Trigger complete│
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Award XP        │
│ Check level up  │
│ Log activity    │
└─────────────────┘
```

---

## ⚙️ Funkcjonalności MVP

### 1. System Autentykacji
- [x] Logowanie (JWT)
- [x] Wylogowanie
- [x] Automatyczne odświeżanie tokenu
- [x] Protected routes (middleware)
- [ ] Rejestracja (admin tworzy konta przez SQL)
- [ ] Zapomniałem hasła (v2.0)

### 2. Dashboard
- [x] Witaj {username}
- [x] Statystyki:
  - Total XP
  - Current Level
  - Completed Lessons / Total
  - Today's Activity
- [x] Recent Activity Feed (ostatnie 5 akcji)
- [x] Quick Actions (Start lesson, View profile)

### 3. Lekcje - Lista
- [x] Wyświetl wszystkie lekcje
- [x] Filtry:
  - Kategoria
  - Difficulty
  - Status (Ukończone/W trakcie/Nowe)
- [x] Sortowanie (Alfabetycznie, XP, Duration)
- [x] Thumbnail + podstawowe info
- [x] Progress indicator (% badge)

### 4. Lekcje - Odtwarzacz
- [x] Video player (HTML5 lub React Player)
- [x] Automatyczny zapis pozycji co 30s
- [x] Resume z ostatniej pozycji
- [x] Progress bar (wizualny)
- [x] Opis lekcji
- [x] Info: Duration, XP reward, Category
- [x] Przycisk "Oznacz jako ukończone"
- [x] Nawigacja: Poprzednia/Następna lekcja

### 5. Profil
- [x] Wyświetl dane: username, email, level, XP
- [x] Avatar (upload w v2.0, teraz tylko URL)
- [x] Edycja: email, full_name, avatar_url
- [x] Statystyki:
  - Total lessons completed
  - Total time spent
  - Favorite category
  - Join date

### 6. System XP & Levels
- [x] XP za ukończenie lekcji
- [x] Automatyczny level up przy progach:
  - Level 1: 0-99 XP
  - Level 2: 100-299 XP
  - Level 3: 300-599 XP
  - Level 4: 600-999 XP
  - Level 5: 1000-1499 XP
  - ... (geometryczny wzrost)
- [x] Notyfikacja o level up
- [x] Progress bar do next level

---

## 🛠️ Stack Technologiczny

### Backend
```
FastAPI       0.109.0    # Framework
SQLAlchemy    2.0.25     # ORM
Pydantic      2.5.3      # Validation & schemas
python-jose   3.3.0      # JWT handling
passlib       1.7.4      # Password hashing (bcrypt)
python-multipart 0.0.6  # Form data
uvicorn       0.27.0     # ASGI server
alembic       1.13.1     # Database migrations
```

### Frontend
```
Next.js       15.1.1     # React framework
React         19.2.3     # UI library
TypeScript    5.3.3      # Type safety
Tailwind CSS  3.4.1      # Styling
Framer Motion 12.24.0    # Animations
Axios         1.6.5      # HTTP client
lucide-react  0.562.0    # Icons
```

### Database
```
SQLite 3              # Development
PostgreSQL (future)   # Production (opcjonalnie)
```

### Dev Tools
```
Pytest         # Backend testing
Playwright     # E2E testing (future)
ESLint         # Code linting
Prettier       # Code formatting
```

---

## 📊 Metryki Sukcesu MVP

1. **Funkcjonalność:**
   - ✅ Użytkownik może się zalogować
   - ✅ Użytkownik widzi listę lekcji
   - ✅ Użytkownik może obejrzeć lekcję
   - ✅ Progres jest zapisywany
   - ✅ XP i level działają poprawnie

2. **Performance:**
   - API response time < 200ms (avg)
   - Page load time < 2s
   - Video buffering minimal

3. **UX:**
   - Intuicyjna nawigacja
   - Responsywny design (mobile + desktop)
   - Brak crashów/błędów

---

## 🚀 Deployment (Wyjaśnienie)

### Co to jest deployment?
**Deployment** = Uruchomienie aplikacji tak, żeby była dostępna przez internet (nie tylko na Twoim komputerze).

### Opcje:

#### 1. **Localhost (Rozwój)**
- **Co to:** Aplikacja działa tylko na Twoim komputerze
- **Adres:** http://localhost:3000 (tylko Ty widzisz)
- **Koszt:** 0 zł
- **Kiedy:** Teraz, podczas budowy MVP

#### 2. **VPS (Virtual Private Server)**
- **Co to:** Wynajmujesz "komputer w chmurze", instalujesz wszystko sam
- **Przykłady:** DigitalOcean, Hetzner, OVH
- **Adres:** https://twojadomena.pl
- **Koszt:** ~20-50 zł/miesiąc
- **Kiedy:** Gdy chcesz pełną kontrolę
- **Wymaga:** Wiedzy o Linux, Docker, nginx

#### 3. **Cloud Platform (Managed)**
- **Co to:** Platforma robi deployment za Ciebie (git push = deploy)
- **Przykłady:**
  - **Vercel** (frontend Next.js) - FREE dla hobby
  - **Railway** (backend FastAPI) - FREE do 500h/mies
  - **Render** (full-stack) - FREE tier dostępny
- **Adres:** https://twoja-app.vercel.app
- **Koszt:** 0-30 zł/miesiąc na start
- **Kiedy:** Najłatwiejsze dla MVP
- **Wymaga:** Konta GitHub + 5 kliknięć

### Moja rekomendacja dla MVP:
**Frontend (Next.js)** → Vercel (FREE, automatyczny deploy z GitHub)  
**Backend (FastAPI)** → Railway (FREE tier, łatwy setup)  
**Database** → SQLite plik (później PostgreSQL na Railway)

**Total koszt:** 0 zł przez pierwsze 3-6 miesięcy

---

## 📅 Timeline (Realistyczny)

### Tydzień 1-2: Backend Foundation
- [ ] Setup projektu (struktura folderów)
- [ ] Modele SQLAlchemy (Users, Lessons, Progress)
- [ ] Auth endpoints (login, me)
- [ ] Lessons endpoints (CRUD, progress)
- [ ] Migracja danych z users_data.json
- [ ] Testy podstawowe

### Tydzień 3-4: Frontend Core
- [ ] Setup Next.js + Tailwind
- [ ] Layout system (wybierzesz 1 z 3 propozycji)
- [ ] Login page + auth flow
- [ ] Dashboard z statystykami
- [ ] Lista lekcji (grid + filters)

### Tydzień 5-6: Lesson Player & Progress
- [ ] Odtwarzacz video
- [ ] Auto-save progressu
- [ ] Complete lesson flow
- [ ] XP & Level up notifications
- [ ] Profile page

### Tydzień 7: Polish & Testing
- [ ] Bug fixing
- [ ] Responsive design
- [ ] Loading states
- [ ] Error handling
- [ ] Basic E2E tests

**Total: ~6-7 tygodni** (pracując part-time, ~10h/tydzień)

---

## ✅ Next Steps

1. **Zatwierdzenie specyfikacji** ← jesteśmy tutaj
2. **Wybór layoutu** (3 propozycje w osobnym pliku)
3. **Setup projektu** (struktura folderów + dependencies)
4. **Backend implementation**
5. **Frontend implementation**
6. **Integration & testing**
7. **Deployment**

---

*Dokument żywy - będzie aktualizowany w trakcie developmentu*
