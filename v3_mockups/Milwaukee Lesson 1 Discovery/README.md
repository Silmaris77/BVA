# Milwaukee Lesson 1: Discovery - Zrozumieć klienta przemysłowego

## 📋 Overview
Interactive HTML mockup for Milwaukee B2B training - complete 10-card lesson focused on industrial customer discovery for Key Account Managers.

## 🎯 Learning Objectives
- Understand 3 customer profiles (mining, automotive, general manufacturing)
- Perform SWOT analysis before meetings
- Map stakeholders by influence × attitude
- Build internal champions (Bob strategy)
- Recognize buying signals and hidden objections
- Master 8 decision-maker types and conversation patterns
- Use practical templates for client work

## 📊 Lesson Structure

### Card 1: Video Introduction (5 XP)
- YouTube video embed
- 3 customer profile overview
- Key insights reflection

### Card 2: Customer Profile Table (0 XP - presentation only)
- 3-column comparison: Kopalnie | Automotive | Produkcja
- KPIs, pain points, decision-makers, buying cycles, arguments, objections
- Tooltips on technical terms (LTIFR, OEE, ATEX)

### Card 3: SWOT Interactive (10 XP)
- Dropdown examples: Mahle, KGHM, Custom
- 4 textareas (Strengths, Weaknesses, Opportunities, Threats)
- Validation: min 3 points per field
- Auto-save + manual save
- Prefilled Mahle example

### Card 4: Stakeholder Matrix (15 XP)
- Interactive table (8+ rows)
- Dropdowns: Influence (1-3), Attitude (-2 to +2)
- Auto-calculate 9 zones (Ambassador, Ally, Hesitant, Opponent, etc.)
- 2D visual matrix with live counters
- Add row functionality
- Validation: min 5 people

### Card 5: Case Study "Bob" (10 XP)
- 7-month timeline (M1-M7)
- Discovery → PoC → ROI → Crisis → Internal Champion → Deal
- 3 reflection questions (min 50 chars each)
- Character counter
- Auto-save

### Card 6: Quiz (15 XP)
- 10 scenario-based questions
- Multiple choice (A/B/C/D)
- Instant visual feedback (green/red)
- Score calculation with interpretation
- 0-5: Need more practice
- 6-8: Good job
- 9-10: Discovery Expert

### Card 7: Flashcards (20 XP)
- 8 decision-maker types:
  - Maintenance Manager
  - Production Manager
  - Procurement Specialist
  - HSE Officer
  - Quality Manager
  - CFO
  - Operator/Technician
  - CEO/Plant Director
- 3D flip animation
- Front: Icon + Title + Influence/Focus
- Back: Language, Pain Point, Argument, Objection, Counter
- Progress tracker (0/8)
- Auto +20 XP when all 8 viewed

### Card 8: Template Download (10 XP)
- 5 Excel sheets:
  - Pre-meeting prep
  - Stakeholder map
  - Discovery questions
  - ROI calculator
  - Next steps tracker
- Commitment checkbox (+10 XP)
- Email reminder

### Card 9: AI Interview Simulation (15 XP)
- 3 rounds with "Bob" (Production Manager, Mahle)
- **Round 1: Discovery**
  - Keywords: rotacja, ergonomia, waga, wibracje, operatorzy, wydajność
  - Score: Max 35 points
- **Round 2: Value Proposition**
  - Keywords: ROI, case study, oszczędność, dowód, liczby, VW, automotive
  - Score: Max 35 points
- **Round 3: Next Steps**
  - Keywords: PoC, pilot, demo, test, próba, data, plan
  - Score: Max 30 points
- Heuristic scoring (0-100)
- Mood tracking based on score:
  - 80+: 😍 Bob impressed
  - 60-79: 😊 Bob interested
  - 40-59: 😐 Bob skeptical
  - <40: 😕 Bob disappointed
- +15 XP if score ≥60

### Card 10: Summary & Badge (10 XP)
- 7-point learning checklist
- Stats display:
  - XP earned
  - Cards completed (10/10)
  - Time spent (~60 min)
- Badge popup: **🔍 Discovery Expert**
- CTA: Lesson 2 (disabled in mockup)
- +10 XP completion bonus

## 💾 Technical Features

### State Management
- LocalStorage persistence for all inputs
- Auto-save on every keystroke
- XP tracking with Set (no duplicates)
- Progress bar calculation
- Card navigation history

### Interactivity
- Keyboard navigation (Arrow keys)
- Prev/Next button management
- Visual feedback (green checkmarks, red errors)
- Instant validation messages
- Dynamic content generation

### Scoring System
- **Total XP possible**: 110 (75 base + 35 bonuses)
- **Card XP values**:
  - Card 1: 5 XP
  - Card 2: 0 XP
  - Card 3: 10 XP
  - Card 4: 15 XP
  - Card 5: 10 XP
  - Card 6: 15 XP
  - Card 7: 20 XP
  - Card 8: 10 XP
  - Card 9: 15 XP (if score ≥60)
  - Card 10: 10 XP

### AI Interview Scoring Logic
```javascript
// Round 1: Discovery (max 35 points)
Keywords: rotacja, ergonomia, waga, wibracje, operatorzy, wydajność, pytanie, potrzeby, bolączki
Score: 4 points per keyword match (max 35)

// Round 2: Value (max 35 points)
Keywords: roi, case study, oszczędność, przykład, dowód, liczby, kalkulator, vw, automotive
Score: 5 points per keyword match (max 35)

// Round 3: Next Steps (max 30 points)
Keywords: poc, pilot, demo, test, próba, linia, data, spotkanie, plan, weekend
Score: 6 points per keyword match (max 30)

Total: 0-100 points
```

### Validation Rules
- **SWOT**: Min 3 points per field (bullets or line breaks)
- **Stakeholders**: Min 5 people filled
- **Bob Reflections**: Min 50 chars per question (×3)
- **AI Interview**: Min 80 chars per round (×3)
- **Quiz**: All 10 questions answered

## 🎨 Design
- **Primary color**: #D32F2F (Milwaukee Red)
- **Secondary**: #212121 (Black)
- **Accent**: #FFC107 (Yellow)
- **Responsive**: Mobile-optimized (@media 768px)
- **Typography**: Clean sans-serif, bold headings
- **Animations**: 
  - 3D card flips (rotateY 180deg)
  - Progress bar transitions
  - Hover effects
  - Gradient backgrounds

## 📱 Responsive Features
- Single-column layout on mobile
- Adjusted table font sizes
- Stackable stats grid
- Touch-friendly buttons
- Optimized textarea heights

## 🚀 Usage
1. Open `lesson1_discovery.html` in any modern browser
2. Navigate through 10 cards (← → or buttons)
3. Complete activities to earn XP
4. Progress auto-saves to localStorage
5. Earn "Discovery Expert" badge at end

## 🔧 File Structure
- **Total lines**: 3908
- **CSS**: ~700 lines (responsive, animations, Milwaukee branding)
- **HTML**: ~850 lines (10 cards + header + badge overlay)
- **JavaScript**: ~2350 lines (navigation, validation, scoring, persistence)

## 📦 Deliverables
- [x] All 10 cards implemented
- [x] XP system working
- [x] LocalStorage persistence
- [x] AI scoring heuristics
- [x] Badge popup
- [x] Mobile responsive
- [x] No external dependencies

## 🎓 Next Steps (Full BVA Integration)
- Replace mockup template download with actual Excel generation
- Add backend XP sync to user profile
- Enable Lesson 2 unlock after completion
- Add analytics tracking
- Implement actual AI conversation (Google Gemini API)
- Add TTS for AI responses (gTTS Polish voice)

---

**Status**: ✅ Complete Mockup (Ready for review)  
**Version**: 1.0  
**Date**: December 2024  
**Target**: Milwaukee B2B Sales Team (KAM Training)
