# BVA v2 MVP - Roadmap & Checklist Implementacji

**Start:** 6 stycznia 2026  
**Target MVP:** ~6-7 tygodni  
**Status:** 📝 Planning → 🛠️ Development

---

## 📊 Progress Overview

```
[█░░░░░░░░░] 10% - Specyfikacja & Planning (COMPLETED)
[░░░░░░░░░░]  0% - Backend Foundation
[░░░░░░░░░░]  0% - Frontend Core
[░░░░░░░░░░]  0% - Integration & Testing
[░░░░░░░░░░]  0% - Deployment
```

---

## ✅ Faza 0: Planning & Design (DONE)

- [x] Analiza wymagań MVP
- [x] Wybór stack technologicznego
- [x] Projekt architektury systemu
- [x] Schemat bazy danych (ERD)
- [x] API design (endpoints)
- [x] User flows & diagrams
- [x] 3 propozycje layoutu UI/UX
- [ ] **DECYZJA:** Wybór finalnego layoutu ← **TUTAJ JESTEŚMY**

---

## 🏗️ Faza 1: Backend Foundation (Week 1-2)

### Krok 1.1: Project Setup (Dzień 1)
- [ ] Utworzenie struktury folderów (`v2_clean/backend/`)
- [ ] Virtual environment setup
- [ ] Install dependencies (`requirements.txt`)
- [ ] Git init + `.gitignore`
- [ ] Environment variables (`.env`)
- [ ] Basic FastAPI app (`main.py`)
- [ ] CORS configuration
- [ ] Health check endpoint (`/api/health`)

**Verification:** `curl http://localhost:8000/api/health` → `{"status": "ok"}`

---

### Krok 1.2: Database Setup (Dzień 2)
- [ ] SQLAlchemy config (`database.py`)
- [ ] Define models:
  - [ ] User model (`models/user.py`)
  - [ ] Lesson model (`models/lesson.py`)
  - [ ] LessonProgress model (`models/progress.py`)
  - [ ] ActivityLog model (`models/activity.py`)
- [ ] Alembic init (migrations)
- [ ] Create initial migration
- [ ] Apply migration → create tables
- [ ] Test: Insert test data manually via SQL

**Verification:** SQLite browser shows all tables with correct schema

---

### Krok 1.3: Authentication System (Dzień 3-4)
- [ ] Password hashing utilities (`core/security.py`)
- [ ] JWT token generation/verification
- [ ] Pydantic schemas:
  - [ ] `LoginRequest`
  - [ ] `Token`
  - [ ] `UserResponse`
- [ ] Auth router (`api/auth.py`):
  - [ ] `POST /auth/login`
  - [ ] `GET /auth/me`
  - [ ] `POST /auth/logout` (optional)
- [ ] Dependencies (`api/deps.py`):
  - [ ] `get_db()`
  - [ ] `get_current_user()`
- [ ] Test endpoints with Postman/Thunder Client

**Verification:** Login returns JWT, `/auth/me` returns user data

---

### Krok 1.4: User Management (Dzień 5)
- [ ] User service (`services/user_service.py`):
  - [ ] `authenticate(username, password)`
  - [ ] `get_user_stats(user_id)`
  - [ ] `update_profile(user_id, data)`
- [ ] User router (`api/users.py`):
  - [ ] `GET /users/me`
  - [ ] `PUT /users/me`
  - [ ] `GET /users/me/stats`
  - [ ] `GET /users/me/activity`
- [ ] Schemas:
  - [ ] `UserUpdate`
  - [ ] `UserStats`
  - [ ] `ActivityLogResponse`

**Verification:** Can update profile, view stats

---

### Krok 1.5: Lessons System (Dzień 6-7)
- [ ] Lesson service (`services/lesson_service.py`):
  - [ ] `get_all_lessons(user_id, filters)`
  - [ ] `get_lesson_by_id(lesson_id, user_id)`
  - [ ] `get_or_create_progress(user_id, lesson_id)`
- [ ] Lesson router (`api/lessons.py`):
  - [ ] `GET /lessons` (with filters)
  - [ ] `GET /lessons/{id}`
  - [ ] `GET /lessons/{id}/progress`
- [ ] Schemas:
  - [ ] `LessonResponse`
  - [ ] `LessonList`
  - [ ] `ProgressResponse`
- [ ] Seed initial lessons (script)

**Verification:** GET /lessons returns list with progress

---

### Krok 1.6: Progress Tracking (Dzień 8-9)
- [ ] Progress service (`services/progress_service.py`):
  - [ ] `update_progress(user_id, lesson_id, percent, position)`
  - [ ] `complete_lesson(user_id, lesson_id)`
  - [ ] `calculate_xp_reward(lesson)`
  - [ ] `check_level_up(user)`
  - [ ] `log_activity(user_id, action, metadata)`
- [ ] Progress endpoints:
  - [ ] `POST /lessons/{id}/start`
  - [ ] `PUT /lessons/{id}/progress`
  - [ ] `POST /lessons/{id}/complete`
- [ ] Schemas:
  - [ ] `ProgressUpdate`
  - [ ] `CompletionResponse`

**Verification:** Complete lesson → XP increases, level up works

---

### Krok 1.7: Data Migration (Dzień 10)
- [ ] Script: `migrate_users_from_json.py`
  - [ ] Load `users_data.json`
  - [ ] For each user:
    - [ ] Hash password (if plain text)
    - [ ] Insert into `users` table
    - [ ] Preserve XP, level, company, etc.
- [ ] Script: `seed_lessons.py`
  - [ ] Load lessons from `data/lessons/*.json`
  - [ ] Insert into `lessons` table
  - [ ] Map video URLs
- [ ] Backup old data
- [ ] Run migration
- [ ] Verify: All users can log in

**Verification:** Login with existing credentials works

---

### Krok 1.8: Backend Testing (Dzień 11)
- [ ] Setup pytest (`tests/conftest.py`)
- [ ] Test fixtures (test DB, test user)
- [ ] Auth tests (`tests/test_auth.py`):
  - [ ] Test login success
  - [ ] Test login failure
  - [ ] Test protected routes
- [ ] Lesson tests (`tests/test_lessons.py`):
  - [ ] Test get lessons
  - [ ] Test filter lessons
  - [ ] Test lesson details
- [ ] Progress tests (`tests/test_progress.py`):
  - [ ] Test update progress
  - [ ] Test complete lesson
  - [ ] Test XP calculation
- [ ] Run: `pytest -v`

**Verification:** All tests pass ✅

---

## 🎨 Faza 2: Frontend Foundation (Week 3-4)

### Krok 2.1: Next.js Setup (Dzień 12)
- [ ] Create Next.js project: `npx create-next-app@latest`
- [ ] Install dependencies:
  - [ ] `axios`, `lucide-react`, `framer-motion`
  - [ ] `tailwindcss`, `clsx`, `tailwind-merge`
- [ ] Configure Tailwind (chosen layout theme)
- [ ] Setup folder structure (App Router)
- [ ] Create `lib/api.ts` (Axios instance)
- [ ] Create `types/index.ts` (TypeScript types)

**Verification:** `npm run dev` → http://localhost:3000 works

---

### Krok 2.2: Auth Context & Utilities (Dzień 13)
- [ ] Create `context/AuthContext.tsx`
- [ ] Custom hook: `hooks/useAuth.ts`
- [ ] Auth utilities (`lib/auth.ts`):
  - [ ] `getToken()`
  - [ ] `setToken(token)`
  - [ ] `removeToken()`
  - [ ] `isTokenExpired(token)`
- [ ] API client (`lib/api.ts`):
  - [ ] Axios instance with interceptors
  - [ ] Auto-attach Authorization header
  - [ ] Handle 401 (redirect to login)

**Verification:** Context provides auth state

---

### Krok 2.3: Login Page (Dzień 14)
- [ ] Create `app/(auth)/login/page.tsx`
- [ ] Create `components/auth/LoginForm.tsx`
- [ ] Form validation (basic)
- [ ] Connect to API (`POST /auth/login`)
- [ ] Store token in localStorage
- [ ] Redirect to `/dashboard` on success
- [ ] Error handling (show message)
- [ ] Loading state

**Verification:** Can log in, redirects to dashboard

---

### Krok 2.4: Protected Routes (Dzień 14)
- [ ] Create `middleware.ts` (Next.js middleware)
- [ ] Check auth token on protected routes
- [ ] Redirect to `/login` if not authenticated
- [ ] Create dashboard layout group: `app/(dashboard)/layout.tsx`

**Verification:** Cannot access dashboard without login

---

### Krok 2.5: UI Components (Dzień 15-16)
- [ ] `components/ui/Button.tsx`
- [ ] `components/ui/Card.tsx` (Glassmorphism style)
- [ ] `components/ui/Input.tsx`
- [ ] `components/ui/Progress.tsx`
- [ ] `components/ui/Badge.tsx`
- [ ] `components/ui/Avatar.tsx`
- [ ] Test in Storybook (optional) or standalone page

**Verification:** Components look good, match chosen layout

---

### Krok 2.6: Dashboard Layout (Dzień 17)
- [ ] `components/layout/Sidebar.tsx`
  - [ ] Navigation links
  - [ ] User info (avatar, username)
  - [ ] Level progress bar
- [ ] `components/layout/Header.tsx`
  - [ ] Page title
  - [ ] Breadcrumbs
  - [ ] Notifications icon
  - [ ] Logout button
- [ ] `components/layout/MobileNav.tsx`
  - [ ] Hamburger menu
  - [ ] Responsive drawer
- [ ] Implement in `app/(dashboard)/layout.tsx`

**Verification:** Layout displays correctly on desktop & mobile

---

### Krok 2.7: Dashboard Page (Dzień 18)
- [ ] Create `app/(dashboard)/page.tsx`
- [ ] `components/dashboard/StatsCard.tsx`:
  - [ ] XP / Level
  - [ ] Completed lessons
  - [ ] Time spent
  - [ ] Current streak
- [ ] `components/dashboard/LevelProgress.tsx`
  - [ ] Visual progress bar
  - [ ] XP to next level
- [ ] `components/dashboard/ActivityFeed.tsx`
  - [ ] Recent activities list
- [ ] `components/dashboard/QuickActions.tsx`
  - [ ] "Start new lesson" button
  - [ ] "View profile" button
- [ ] Fetch data from API (`GET /users/me`, `/users/me/stats`, `/users/me/activity`)

**Verification:** Dashboard shows live data

---

## 📚 Faza 3: Lessons Feature (Week 5-6)

### Krok 3.1: Lesson List Page (Dzień 19-20)
- [ ] Create `app/(dashboard)/lessons/page.tsx`
- [ ] `components/lessons/LessonCard.tsx`:
  - [ ] Thumbnail
  - [ ] Title, category, difficulty
  - [ ] XP reward
  - [ ] Progress badge (if started)
  - [ ] Hover animations
- [ ] `components/lessons/LessonList.tsx`
  - [ ] Grid layout
  - [ ] Map lessons to cards
- [ ] `components/lessons/LessonFilters.tsx`
  - [ ] Category dropdown
  - [ ] Difficulty dropdown
  - [ ] Status filter (All/In Progress/Completed)
  - [ ] Search input (optional)
- [ ] Custom hook: `hooks/useLessons.ts`
  - [ ] Fetch lessons
  - [ ] Apply filters
  - [ ] Loading/error states
- [ ] Connect to API (`GET /lessons?category=X&difficulty=Y`)

**Verification:** Can browse and filter lessons

---

### Krok 3.2: Lesson Player Page (Dzień 21-22)
- [ ] Create `app/(dashboard)/lessons/[id]/page.tsx`
- [ ] `components/lessons/LessonPlayer.tsx`:
  - [ ] Video player (HTML5 `<video>` or `react-player`)
  - [ ] Play/pause controls
  - [ ] Seek bar
  - [ ] Volume control
  - [ ] Fullscreen button
- [ ] `components/lessons/LessonInfo.tsx`:
  - [ ] Title, description
  - [ ] Duration, XP reward, category
  - [ ] Progress percentage
- [ ] `components/lessons/LessonNavigation.tsx`:
  - [ ] Previous/Next lesson buttons
  - [ ] Back to list
- [ ] Auto-resume from last position
- [ ] "Mark as complete" button

**Verification:** Can play video, see lesson details

---

### Krok 3.3: Progress Auto-Save (Dzień 23)
- [ ] Custom hook: `hooks/useProgress.ts`
- [ ] Video `timeupdate` event listener
- [ ] Throttle updates (every 30 seconds)
- [ ] Calculate progress percentage
- [ ] API call: `PUT /lessons/{id}/progress`
- [ ] Update local state optimistically
- [ ] Show "Saving..." indicator
- [ ] Handle errors gracefully

**Verification:** Progress saves automatically, persists on page reload

---

### Krok 3.4: Lesson Completion (Dzień 24)
- [ ] Detect 100% progress
- [ ] "Complete Lesson" button enabled
- [ ] API call: `POST /lessons/{id}/complete`
- [ ] Show celebration modal:
  - [ ] Confetti animation (optional)
  - [ ] "Congratulations!" message
  - [ ] "+X XP" display
  - [ ] Level up notification (if applicable)
  - [ ] "Next lesson" button
- [ ] Update user XP/level in context
- [ ] Redirect or show next lesson

**Verification:** Completing lesson awards XP, level up works

---

### Krok 3.5: Profile Page (Dzień 25)
- [ ] Create `app/(dashboard)/profile/page.tsx`
- [ ] `components/profile/ProfileHeader.tsx`:
  - [ ] Avatar (with upload in v2.0)
  - [ ] Username, email
  - [ ] Level badge
- [ ] `components/profile/ProfileStats.tsx`:
  - [ ] Total lessons completed
  - [ ] Total XP
  - [ ] Total time spent
  - [ ] Join date
  - [ ] Current streak
- [ ] `components/profile/ProfileForm.tsx`:
  - [ ] Edit email
  - [ ] Edit full_name
  - [ ] Edit avatar_url (text input for now)
  - [ ] Save button
- [ ] API call: `PUT /users/me`

**Verification:** Can view and update profile

---

## 🔗 Faza 4: Integration & Polish (Week 7)

### Krok 4.1: End-to-End Testing (Dzień 26-27)
- [ ] Manual testing: Full user journey
  - [ ] Login → Dashboard → Lessons → Watch → Complete → Profile
- [ ] Test filters and search
- [ ] Test edge cases:
  - [ ] Empty lesson list
  - [ ] Network errors
  - [ ] Token expiration
  - [ ] Invalid lesson ID
- [ ] Test on multiple browsers (Chrome, Firefox, Safari)
- [ ] Test on mobile devices
- [ ] Fix bugs

**Verification:** No critical bugs, smooth UX

---

### Krok 4.2: Performance Optimization (Dzień 28)
- [ ] Lazy load images (Next.js Image component)
- [ ] Code splitting (dynamic imports)
- [ ] Optimize API calls (caching, React Query?)
- [ ] Minimize bundle size
- [ ] Lighthouse audit (Performance, Accessibility)
- [ ] Fix performance issues

**Verification:** Lighthouse score > 90

---

### Krok 4.3: Error Handling & Loading States (Dzień 29)
- [ ] Global error boundary
- [ ] Toast notifications (success/error)
- [ ] Loading skeletons for all pages
- [ ] Empty states (no lessons, no activity)
- [ ] 404 page
- [ ] Network error page
- [ ] Retry mechanisms

**Verification:** All states handled gracefully

---

### Krok 4.4: Accessibility (Dzień 30)
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] ARIA labels on interactive elements
- [ ] Alt text on images
- [ ] Color contrast WCAG AA
- [ ] Screen reader tested (optional)

**Verification:** Accessibility audit passes

---

### Krok 4.5: Documentation (Dzień 31)
- [ ] Update README.md (setup instructions)
- [ ] API documentation (Swagger auto-generated)
- [ ] Frontend documentation (component usage)
- [ ] Deployment guide
- [ ] Troubleshooting guide

**Verification:** New developer can setup project

---

## 🚀 Faza 5: Deployment (Week 7+)

### Krok 5.1: Backend Deployment (Railway)
- [ ] Create Railway account
- [ ] Create new project
- [ ] Connect GitHub repo (backend)
- [ ] Set environment variables:
  - [ ] `DATABASE_URL` (PostgreSQL or keep SQLite)
  - [ ] `SECRET_KEY`
  - [ ] `CORS_ORIGINS`
- [ ] Deploy
- [ ] Test API endpoints

**URL:** https://bva-backend.railway.app

---

### Krok 5.2: Frontend Deployment (Vercel)
- [ ] Create Vercel account
- [ ] Import GitHub repo (frontend)
- [ ] Set environment variables:
  - [ ] `NEXT_PUBLIC_API_URL` (Railway backend URL)
- [ ] Deploy
- [ ] Test app

**URL:** https://bva.vercel.app

---

### Krok 5.3: Database Migration (Optional)
- [ ] If using PostgreSQL on Railway:
  - [ ] Export SQLite data
  - [ ] Import to PostgreSQL
  - [ ] Update connection string
  - [ ] Test migrations

---

### Krok 5.4: Custom Domain (Optional)
- [ ] Purchase domain (e.g., brainventure.pl)
- [ ] Configure DNS
- [ ] Add to Vercel
- [ ] SSL certificate (auto)

**URL:** https://app.brainventure.pl

---

## 📊 Success Metrics

### Functional Requirements ✅
- [ ] User can log in with existing credentials
- [ ] User can view list of lessons
- [ ] User can watch lesson video
- [ ] Progress is automatically saved
- [ ] User can complete lesson and earn XP
- [ ] Level up works correctly
- [ ] User can view and edit profile

### Technical Requirements ✅
- [ ] API response time < 200ms (avg)
- [ ] Frontend page load < 2s
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Accessible (WCAG AA)
- [ ] Secure (HTTPS, JWT, password hashing)

### UX Requirements ✅
- [ ] Intuitive navigation
- [ ] Clear feedback on actions
- [ ] Smooth animations
- [ ] Professional design (chosen layout)
- [ ] No broken links or dead ends

---

## 🎯 Next Immediate Steps

### Co robić teraz:
1. **Wybierz layout** (Glassmorphism, Professional, lub Gamified)
2. **Zatwierdź specyfikację** (review dokumentów)
3. **Setup development environment:**
   - [ ] Install Python 3.11+
   - [ ] Install Node.js 20+
   - [ ] Install VS Code + extensions
   - [ ] Install Git
4. **Rozpocznij Faza 1, Krok 1.1** (Backend project setup)

---

## 📞 Wsparcie

**Gdy utkniesz:**
- Sprawdź dokumentację: `SPECIFICATION_MVP.md`, `DIAGRAMS.md`
- GitHub Copilot (AI assistant w VS Code)
- Stack Overflow
- FastAPI docs: https://fastapi.tiangolo.com
- Next.js docs: https://nextjs.org/docs

**Pytania do omówienia:**
- Deployment strategy (Railway vs inne)
- PostgreSQL vs SQLite dla produkcji
- Authentication: JWT vs Sessions
- State management: Context vs React Query

---

*Checklist będzie aktualizowana w miarę postępów*  
*Ostatnia aktualizacja: 6 stycznia 2026*
