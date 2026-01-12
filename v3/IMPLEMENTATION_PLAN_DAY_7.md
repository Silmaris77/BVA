# 📅 Day 7 Implementation Plan: Mobile & Profile
**Date:** 2026-01-12
**Focus:** Mobile Responsiveness & "Ja" Hub (Profile)

---

## 📱 Goal 1: Mobile-First Responsiveness

TRANSFORM Desktop-only layout into a fully responsive PWA-ready interface.

### 1. Navigation Architecture
According to `v3_app_specification.md`, we need a dual navigation system:
- **Desktop (≥1024px):** Fixed Sidebar using `Navigation` component.
- **Mobile (<768px):** Fixed Bottom Navigation Bar.

#### [NEW] `components/BottomNav.tsx`
- **Fixed Position:** `fixed bottom-0 left-0 w-full`
- **Style:** Glassmorphism background (`backdrop-blur-xl`, `bg-black/40`)
- **Items:** 4 Main Hubs (Hub, Nauka, Praktyka, Ja)
- **Active State:** Neon underline or glow color
- **Z-Index:** High (`z-50`) to sit above content

#### [MODIFY] `components/Navigation.tsx`
- Implement responsive logic (CSS media queries or `hidden md:flex`)
- Hide Sidebar on mobile (`hidden md:flex`)
- Show Sidebar on desktop

#### [MODIFY] `app/layout.tsx`
- Adjust main content margin:
  - **Desktop:** `ml-[240px]` (Sidebar width)
  - **Mobile:** `mb-[80px]` (Bottom Nav height), `ml-0` (No sidebar margin)

### 2. Responsive Grids
Update existing pages to use responsive Tailwind classes.

#### Dashboard (`app/page.tsx`)
- **Stats Grid:** `grid-cols-1 md:grid-cols-2 lg:grid-cols-4`
- **Main Content:** Stack vertically on mobile, side-by-side on desktop.

#### Lesson Browser (`app/lessons/page.tsx`)
- **Lesson Cards:** `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`
- **Tabs:** Scrollable horizontal container on mobile (hide scrollbar)

---

## 👤 Goal 2: "Ja" Hub (Profile Page)

Create the Personal Hub for user stats, settings, and progress tracking.

### 1. Page Structure
**File:** `src/app/profile/page.tsx` (Move from `app/ja` if exists to standarize)
**Route:** `/profile` (Mapped to "Ja" in navigation)

### 2. Tab System
Implement secondary navigation within the Profile page:
1. **Profil**: Avatar, Bio, Key Stats
2. **Postępy**: Detailed XP charts, Skills Radar
3. **Cele**: Active Missions
4. **Ustawienia**: Account preferences

### 3. "Profil" Tab Components
- **Header Card:**
  - Large Avatar (round, bordered)
  - Username & Title (e.g., "Level 5 Strategist")
  - XP Bar (Visual progress)
- **Stats Summary:**
  - 🔥 Current Streak
  - 📚 Lessons Completed
  - 🏆 Total XP
- **Badges Grid:**
  - Display earned badges (placeholders for now)

### 4. "Ustawienia" Tab Components
- **Account:** Email (readonly), Username (editable)
- **Preferences:** Theme toggle, Notifications
- **Actions:** **Sign Out** button (supa.auth.signOut)

---

## 🛠️ Step-by-Step Execution Tasks

### Phase 1: Navigation Refactor (45 min)
- [ ] Create `BottomNav.tsx` with Lucide icons
- [ ] Update `Navigation.tsx` to handle responsive visibility
- [ ] Update root layout margins

### Phase 2: Grid Responsiveness (30 min)
- [ ] Fix Dashboard stats grid
- [ ] Fix Leaderboard responsiveness
- [ ] Fix Lesson Browser grid
- [ ] Test on mobile view (Chrome DevTools)

### Phase 3: Profile Implementation (60 min)
- [ ] Create `app/profile/page.tsx`
- [ ] Build Profile Header with Avatar
- [ ] Implement Stats Cards
- [ ] Add basic Settings section with Logout
- [ ] Connect "Ja" nav item to `/profile`

---

## 🔍 Verification Checklist
- [ ] Bottom Nav appears ONLY on mobile screens
- [ ] Sidebar appears ONLY on desktop screens
- [ ] Content is not obscured by Bottom Nav on mobile
- [ ] Dashboard grids stack correctly (1 col) on mobile
- [ ] Profile page loads user data from Supabase
- [ ] Logout button successfully redirects to Login
