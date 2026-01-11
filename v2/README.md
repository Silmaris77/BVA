# BrainVentureAcademy v2.0 - Migracja do FastAPI + Next.js

> **Status:** 📝 Planning Phase  
> **Data rozpoczęcia:** 6 stycznia 2026  
> **Target MVP:** ~6-7 tygodni  
> **Scope:** Lekcje + System Progressu (XP, Levels)

---

## 📚 Dokumentacja Projektowa

### 🎯 [START_HERE.md](START_HERE.md) ← **ZACZNIJ TUTAJ!**
Przewodnik wprowadzający - przegląd wszystkich dokumentów, FAQ, quick start

### 📋 Dokumenty Techniczne:
1. **[SPECIFICATION_MVP.md](SPECIFICATION_MVP.md)** - Pełna specyfikacja MVP
   - Architektura systemu
   - Schemat bazy danych
   - API endpoints
   - User flows
   - Stack technologiczny

2. **[LAYOUT_PROPOSALS.md](LAYOUT_PROPOSALS.md)** - 3 Propozycje UI/UX
   - Layout 1: Glassmorphism (modern, premium)
   - Layout 2: Professional (clean, business)
   - Layout 3: Gamified (fun, engaging)
   - Porównanie i rekomendacje

3. **[DIAGRAMS.md](DIAGRAMS.md)** - Diagramy Techniczne
   - Architektura szczegółowa
   - Database ERD
   - Authentication flow
   - Lesson workflow
   - Folder structure
   - Code examples

4. **[ROADMAP.md](ROADMAP.md)** - Plan Implementacji
   - 31 kroków implementacji (checklist)
   - 5 faz: Planning → Deployment
   - Verification criteria
   - Success metrics

---

## 🏗️ Architektura v2

```
┌─────────────────────────────────────┐
│   FRONTEND (Next.js 15 + React)    │
│   • TypeScript                      │
│   • Tailwind CSS                    │
│   • Framer Motion                   │
│   Port: 3000                        │
└──────────────┬──────────────────────┘
               │ REST API (JSON + JWT)
┌──────────────▼──────────────────────┐
│   BACKEND (FastAPI)                 │
│   • Python 3.11+                    │
│   • SQLAlchemy ORM                  │
│   • JWT Authentication              │
│   Port: 8000                        │
└──────────────┬──────────────────────┘
               │ SQL Queries
┌──────────────▼──────────────────────┐
│   DATABASE (SQLite → PostgreSQL)    │
│   • users, lessons                  │
│   • lesson_progress, activity_logs  │
└─────────────────────────────────────┘
```

---

## 🚀 Uruchomienie (Development)

### Backend (FastAPI)
```bash
cd v2/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend (Next.js)
```bash
cd v2/frontend
npm install
npm run dev
```

### Dostęp:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🔐 Logowanie (Test)

**Credentials:**
- Username: `admin`
- Password: `admin123`

---

## 📦 Tech Stack

### Backend
- **FastAPI** 0.109.0 - Modern Python web framework
- **SQLAlchemy** 2.0+ - ORM
- **Pydantic** 2.5+ - Data validation
- **python-jose** - JWT tokens
- **bcrypt** - Password hashing
- **Alembic** - Database migrations

### Frontend
- **Next.js** 15.1.1 - React framework (App Router)
- **React** 19.2.3 - UI library
- **TypeScript** 5.3+ - Type safety
- **Tailwind CSS** 3.4+ - Utility-first CSS
- **Framer Motion** 12.24+ - Animations
- **Axios** - HTTP client

---

## 🎯 MVP Scope (v2.0)

### ✅ Included:
- User authentication (JWT)
- Lesson catalog (browse, filter)
- Video player (HTML5)
- Progress tracking (auto-save)
- XP & Level system
- User profile
- Dashboard with stats

### ❌ Not Included (v2.1+):
- Business Games
- Milwaukee Tool
- Admin panel (use SQL directly)
- Fiszki, Inspiracje
- Ranking system

---

## 📊 Progress

### Phase 1: Planning & Design (DONE) ✅
- [x] Specyfikacja MVP
- [x] Database schema
- [x] API design
- [x] UI/UX proposals
- [ ] **Layout selection** ← TUTAJ JESTEŚMY

### Phase 2: Backend Foundation (Week 1-2)
- [ ] Project setup
- [ ] Database models
- [ ] Authentication system
- [ ] Lessons API
- [ ] Progress tracking

### Phase 3: Frontend Core (Week 3-4)
- [ ] Next.js setup
- [ ] Login page
- [ ] Dashboard
- [ ] Lesson list
- [ ] Lesson player

### Phase 4: Integration (Week 5-6)
- [ ] Connect FE ↔ BE
- [ ] Auto-save progress
- [ ] XP & level up
- [ ] Profile page

### Phase 5: Polish & Deploy (Week 7)
- [ ] Testing
- [ ] Bug fixes
- [ ] Performance
- [ ] Deployment

---

## 🚀 Deployment Plan

### Free Tier Options:
- **Frontend:** Vercel (Next.js) - FREE unlimited
- **Backend:** Railway - FREE 500h/month
- **Database:** Neon (PostgreSQL) - FREE 0.5GB

**Total cost:** 0 zł for MVP!

---

## 📖 Development Guide

### Getting Started:
1. Read [START_HERE.md](START_HERE.md)
2. Choose layout from [LAYOUT_PROPOSALS.md](LAYOUT_PROPOSALS.md)
3. Review [SPECIFICATION_MVP.md](SPECIFICATION_MVP.md)
4. Follow [ROADMAP.md](ROADMAP.md) step-by-step

### Code Style:
- Python: PEP 8, type hints
- TypeScript: ESLint + Prettier
- Commits: Conventional Commits (`feat:`, `fix:`, `docs:`)

---

## 🤝 Contributing

This is a migration from Streamlit (v1) to modern stack (v2). 

**Old system:**
- Streamlit monolith
- `users_data.json` + SQLite
- Session state
- Single codebase

**New system:**
- Separated FE/BE
- Pure SQL database
- JWT authentication
- Modern best practices

---

## 📞 Support

**Questions?**
- Check documentation in `v2/*.md`
- Review [DIAGRAMS.md](DIAGRAMS.md) for technical details
- See [ROADMAP.md](ROADMAP.md) for implementation steps

---

## 🎯 Next Steps

1. **Choose UI layout** (Glassmorphism/Professional/Gamified)
2. **Approve specification** (any changes needed?)
3. **Setup dev environment** (Python 3.11+, Node.js 20+)
4. **Start Phase 1** (Backend foundation)

---

## 📄 License

Private project - BrainVentureAcademy

---

## 🔗 Links

- Old Streamlit app: `../main.py`
- Database: `../users.db`
- Lessons data: `../data/lessons/`

---

*Ready to build the future of BVA!* 🚀

---

## 🚀 Uruchomienie Backendu (FastAPI) - Legacy Docs

### Metoda 1: Bat file (Windows)
```cmd
v2\backend\start.bat
```

### Metoda 2: PowerShell
```powershell
cd "C:\Users\pksia\Dropbox\BVA"
python -m uvicorn v2.backend.main:app --host 127.0.0.1 --port 8001 --reload
```

### Metoda 3: Python
```python
cd "C:\Users\pksia\Dropbox\BVA"
python v2/backend/run.py
```

Backend będzie dostępny na: **http://localhost:8001**

## 🔐 Dane Logowania

- **Username:** `admin`
- **Password:** `admin123`

## 📚 Endpointy

- **Health Check:** http://localhost:8001/api/health
- **API Docs (Swagger):** http://localhost:8001/docs
- **API Redoc:** http://localhost:8001/redoc
- **Login:** POST http://localhost:8001/token

## 🧪 Test Logowania

```powershell
# Z katalogu BVA
python v2/scripts/test_login.py
```

Lub ręcznie:
```powershell
curl.exe -X POST "http://localhost:8001/token" `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -d "username=admin&password=admin123"
```

Oczekiwana odpowiedź:
```json
{
  "access_token": "admin",
  "token_type": "bearer"
}
```

## 🎨 Uruchomienie Frontendu (Next.js)

```powershell
cd v2/frontend
npm install          # Tylko przy pierwszym uruchomieniu
npm run dev
```

Frontend będzie dostępny na: **http://localhost:3000**

## 🔧 Troubleshooting

### Port 8001 zajęty
```powershell
# Znajdź i zabij proces
Get-NetTCPConnection -LocalPort 8001 | ForEach-Object { 
  Stop-Process -Id $_.OwningProcess -Force 
}
```

### Baza danych
- Lokalizacja: `C:\Users\pksia\Dropbox\BVA\users.db`
- SQLite browser lub:
```python
python -c "import sqlite3; conn = sqlite3.connect('users.db'); 
           c = conn.cursor(); 
           c.execute('SELECT username, xp, level FROM users'); 
           print(c.fetchall())"
```

### Reset hasła admina
```powershell
python v2/scripts/create_v2_admin.py
```

## 📝 Status

✅ Backend uruchomiony i działa
✅ Logowanie admin/admin123 potwierdzone
✅ Baza danych skonfigurowana (users.db)
✅ Token authentication działa
