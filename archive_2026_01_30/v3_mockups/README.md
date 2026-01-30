# 🚀 BrainVenture V3 - Mockupy i Dokumentacja

**Folder:** `v3_mockups`  
**Data utworzenia:** 2026-01-11  
**Status:** Design & Specification Complete

---

## 📋 Zawartość folderu

Ten folder zawiera **kompletną dokumentację projektową** oraz **interaktywne mockupy HTML** dla nowej wersji aplikacji BrainVenture V3.

### 📄 Dokumentacja

#### `v3_app_specification.md`
Kompleksowa specyfikacja aplikacji zawierająca:
- **Architekturę nawigacji** - Model 4-Hub (Hub, Nauka, Praktyka, Ja)
- **Strukturę modułów** - Szczegółowy breakdown każdego hubu
- **Routing Next.js** - Mapa ścieżek i plików
- **System nawigacji** - Desktop sidebar vs Mobile bottom nav
- **User flows** - Diagramy przepływu użytkownika
- **Design system** - Glassmorphism guidelines, kolory, typografia
- **Responsive behavior** - Breakpoints i layout changes
- **Roadmap implementacji** - Plan 4 faz (10 tygodni)

---

### 🎨 Interaktywne Mockupy (HTML)

Wszystkie mockupy mają:
✅ **Desktop/Mobile toggle** (prawy górny róg)  
✅ **Glassmorphism design** z animated orbs  
✅ **Responsywny layout** (sidebar → bottom nav)  
✅ **Lucide icons** + Chart.js (gdzie applicable)  
✅ **Functional navigation** (hover states, active states)

---

#### 1. `v3_homepage_mockup.html` - 🏠 Hub (Dashboard)

**Główna strona aplikacji**

**Zawartość:**
- **Stats Grid:** Total XP, Level, Lekcje ukończone, Streak
- **Aktywne Misje:** 3 karty z progress bars
  - Milwaukee Canvas (w trakcie)
  - Neural Implant activation
  - Tygodniowe wyzwanie
- **Leaderboard:** Top 3 + pozycja użytkownika (#8)
- **Mapa Kompetencji:** Radar chart (6 wymiarów)

**Top Bar:**
- Search bar
- Notifications (badge: 3)
- XP counter (2,450 XP)
- Profile avatar

**Nawigacja:**
- Sidebar (desktop): Hub, Nauka, Praktyka, Ja, AI Assistant
- Bottom Nav (mobile): 4 główne ikony

**Kolory:** Neon Blue + Purple

---

#### 2. `v3_nauka_mockup.html` - 📚 Nauka (Learning Hub)

**Katalog lekcji i zasobów edukacyjnych**

**Zawartość:**
- **Tabs:** Lekcje | Implants | Zasoby
- **Filtry:** Wszystkie, Leadership, Communication, Strategy, Sales, W trakcie
- **Lesson Grid:** 6 przykładowych lekcji
  - Milwaukee Canvas (w trakcie - 57%)
  - Milwaukee Care: Gwarancja (nowa)
  - Zmienność Emocjonalna (ukończona ✓)
  - Leadership Fundamentals
  - Conversational Intelligence
  - Negocjacje Win-Win

**Każda karta lekcji pokazuje:**
- Status badge (W trakcie / Nowe / Ukończone)
- Kategoria (kolorowa ikona)
- Czas trwania (~25-50 min)
- Liczba kart
- Wartość XP (+150 do +250)
- Progress bar (jeśli rozpoczęta)

**Kolory:** Neon Blue (główny akcent)

---

#### 3. `v3_praktyka_mockup.html` - 🎮 Praktyka (Practice Hub)

**Narzędzia biznesowe, gry i projekty**

**Zawartość:**
- **Tabs:** Narzędzia | Gry | Inspiracje | Projekty
- **Quick Actions:**
  - Nowy Canvas (green button)
  - Rozpocznij Grę (purple button)
- **Tool Grid:** 6 narzędzi
  - 🎤 AI Sales Assistant
  - 📋 Canvas Generator
  - 📊 Deal Analyzer
  - 💬 Pitch Simulator
  - 👥 Persona Builder
  - 🎯 OKR Tracker
- **Ostatnia Aktywność:** 3 recent items
  - Milwaukee Canvas - wersja 2 (edytowano 2h temu)
  - Symulacja Negocjacji (wynik: 87/100)
  - AI Sales Call Practice (3 dni temu)

**Kolory:** Neon Green (główny akcent)

---

#### 4. `v3_ja_mockup.html` - 📊 Ja (Personal Hub)

**Profil użytkownika, postępy i cele**

**Zawartość:**
- **Tabs:** Profil | Postępy | Cele | Ustawienia
- **Profile Header:**
  - Avatar (gradient, 120px)
  - Imię i nazwisko: Piotr Kowalski
  - Status: Strategist • Członek od stycznia 2024
  - Level badge: Level 8 • 2,450 XP (gold)
- **Stats Row:** 
  - 12 ukończonych lekcji
  - 7 dni streak 🔥
  - 8 zdobytych odznak
  - #8 w rankingu
- **Zdobyte Odznaki:** Grid 8 badges
  - 🎯 First Steps
  - 📚 Knowledge Seeker
  - 🔥 7-Day Streak
  - ⚡ Fast Learner
  - 💎 Premium Member
  - 🎓 Graduate
  - 🚀 Achiever
  - 🌟 All-Star
- **Mapa Kompetencji:** Radar chart (gold theme)
  - Leadership: 85%
  - Communication: 72%
  - Strategy: 90%
  - Negotiation: 65%
  - Sales: 78%
  - Analytics: 88%
- **Aktywne Cele:** 3 goals z progress
  - Ukończ 15 lekcji w styczniu (12/15 - 80%)
  - Osiągnij Level 10 (2,450/3,500 XP - 70%)
  - 30-dniowy streak (7/30 - 23%)

**Kolory:** Neon Gold (główny akcent)

---

## 🎨 Design System

### Glassmorphism Principles

```css
background: rgba(20, 20, 35, 0.4);
backdrop-filter: blur(20px);
border: 1px solid rgba(255, 255, 255, 0.08);
border-radius: 16-24px;
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
```

### Color Palette (Cyberpunk)

- **Background:** `linear-gradient(135deg, #0f0c29, #302b63, #24243e)`
- **Neon Accents:**
  - Purple: `#b000ff`
  - Blue: `#00d4ff`
  - Gold: `#ffd700`
  - Green: `#00ff88`
  - Red: `#ff0055`

### Typography

- **Font:** Outfit (Google Fonts)
- **Weights:** 300, 400, 500, 600, 700, 800
- **Sizes:**
  - H1: 28-32px / 700
  - H2: 24px / 700
  - H3: 16-18px / 600
  - Body: 15px / 400
  - Small: 11-13px

---

## 📱 Responsive Design

### Breakpoints

- **Mobile:** 0-767px
- **Tablet:** 768-1023px
- **Desktop:** 1024px+

### Layout Transitions

| Element | Desktop | Mobile |
|---------|---------|--------|
| **Navigation** | Fixed Sidebar (240px left) | Bottom Nav (fixed bottom) |
| **Content Margin** | margin-left: 240px | margin-bottom: 70px |
| **Grids** | 2-4 columns | 1-2 columns |
| **Search Bar** | 400px max-width | Compact |

---

## 🚀 Jak używać mockupów?

### Krok 1: Otwórz HTML w przeglądarce

```bash
# Windows
start v3_homepage_mockup.html

# Mac/Linux
open v3_homepage_mockup.html
```

### Krok 2: Toggle Desktop/Mobile

Kliknij przycisk **Desktop** lub **Mobile** w prawym górnym rogu każdego mockupu.

### Krok 3: Testuj interakcje

- Hover over navigation items
- Zobacz active states
- Sprawdź progress bars
- Interakcja z Chart.js (hover over radar)

---

## 📊 Tech Stack

**Frontend (docelowy):**
- Next.js 15 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Lucide Icons
- Chart.js

**Backend:**
- FastAPI
- PostgreSQL
- Pydantic

**Mockupy (current):**
- Vanilla HTML/CSS/JS
- Lucide Icons CDN
- Chart.js CDN
- Google Fonts (Outfit)

---

## 🔄 Next Steps - Implementacja

### Faza 1: Core Navigation (2 tygodnie)
- [ ] Layout component z Sidebar + Bottom Nav
- [ ] Routing dla 4 hubów
- [ ] Top Bar component
- [ ] Responsive breakpoints

### Faza 2: Hub Pages (3 tygodnie)
- [ ] Dashboard (Hub) - rozszerzenie current
- [ ] Learning Hub - catalog + filters
- [ ] Practice Hub - tools grid
- [ ] Personal Hub - profile + stats

### Faza 3: Lesson Player (2 tygodnie)
- [ ] HTML → React migration
- [ ] API integration
- [ ] Progress tracking
- [ ] XP system

### Faza 4: Polish (3 tygodnie)
- [ ] Search functionality
- [ ] Notifications
- [ ] AI recommendations
- [ ] PWA setup

---

## 📞 Kontakt

**Projekt:** BrainVenture V3  
**Data:** Styczeń 2026  
**Status:** Design & Specification Phase

---

**🎯 Cel:** Przekształcenie monolitycznej aplikacji Streamlit w nowoczesną platformę EdTech z mobile-first PWA, card-based learning i AI personalization.
