# Copilot Instructions - BrainVentureAcademy (BVA)

## Project Overview
Educational gamification platform built with **Streamlit** for personal development, investments, and financial psychology. Combines learning modules with business simulation games.

## Core Architecture

### Application Structure
```
main.py              # Entry point - MUST call st.set_page_config() FIRST
├── views/           # Page modules (dashboard, business_games, profile, etc.)
├── utils/           # Shared components (session, navigation, themes)
├── repository/      # Data access layer (SQL + JSON hybrid)
├── data/            # Static data (lessons, scenarios, business_games/)
└── database/        # SQLite database files
```

### Critical Patterns

**1. Streamlit Configuration Order**
```python
# ALWAYS this order in main.py:
st.set_page_config(**PAGE_CONFIG)  # FIRST!
# Then other imports and logic
```

**2. Data Storage: Dual System**
- **SQLite** (`business_games.db`) - Business games, contracts, events, FMCG scenarios
- **JSON** (`users_data.json`) - User profiles, XP, badges, learning progress
- Repository pattern in `repository/` abstracts database access

**3. Session State Management**
```python
# Initialize in utils/session.py
init_session_state()  # Call at app start
# Key session variables:
st.session_state.logged_in
st.session_state.username
st.session_state.user_data
st.session_state.current_page
```

## Running the Application

### Windows (Primary Platform)
```powershell
python -m streamlit run main.py
```
**Never use**: `streamlit run main.py` - fails on Windows

### Common Ports
- Default: http://localhost:8501
- Fallbacks: 8502, 8503

## Business Games Module

### Architecture
- **Main file**: `views/business_games.py` (orchestrator)
- **Refactored modules**: `views/business_games_refactored/`
  - `components/` - UI cards, charts, headers
  - `fmcg.py` - FMCG scenario logic
  - `helpers.py` - Business logic functions

### Contract Types
1. **Standard** (💼) - Basic contracts
2. **Premium** (⭐) - High-value, reputation-gated
3. **AI Conversation** (💬) - NPC dialogue with TTS (gTTS Polish voice)
4. **Speed Challenge** (⚡) - Timed contracts (coming soon)

### AI Conversation Contracts
- Uses Google Generative AI for NPC responses
- Real-time metrics: empathy, assertiveness, professionalism
- Text-to-Speech with gTTS (Polish male voice)
- Scenarios in `data/business_games/ai_conversation_contracts.json`

### Company Progression System
- **10 levels**: Solo Consultant → CIQ Empire
- Progression based on: cash reserves + reputation
- Employee cost: 500 PLN/person/day
- Daily contracts scale with level (1-5 per day)

### Event System
- 10% chance per day
- Difficulty scales with company level
- Defined in `data/business_games/events.json`

## Development Workflows

### Adding New Features
1. **Views**: Create in `views/` or extend existing
2. **Components**: Reusable UI in `utils/components.py`
3. **Navigation**: Update `utils/new_navigation.py` + `navigation_menu()`
4. **Session state**: Initialize new vars in `utils/session.py`

### Database Migrations
- Pattern: `migrate_*.py` scripts in root (e.g., `migrate_add_discovery_fields.py`)
- Backup before migration: `users_data_backup_*.json`
- Test migrations with `run_migration.py`

### Testing
- Test files archived in `tests/archive/`
- Active tests: `test_*.py` in root
- No automated test runner - manual execution

## Key Conventions

### Import Management
```python
# Always add APP_DIR to path (in main.py pattern)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, APP_DIR)
```

### Error Handling
```python
# Suppress Google Cloud warnings (common pattern)
warnings.filterwarnings('ignore', message='.*ALTS.*')
os.environ['GRPC_VERBOSITY'] = 'ERROR'
```

### UI Styling
- Custom CSS in `static/css/style.css`
- Hides Streamlit deploy button and main menu
- Theme manager in `utils/theme_manager.py`

### Gamification System
- **XP**: Earned from lessons, inspirations, tests
- **Levels**: Progressive thresholds (0-99, 100-299, 300-599...)
- **DegenCoins**: Virtual currency (shop in development)
- **Badges**: Achievement system in `utils/achievements.py`

## External Dependencies

### AI Integration
- **Google Generative AI** - NPC conversations in Business Games
- API key required: Configure in application settings
- Models: Gemini for chat, gTTS for voice

### Data Visualization
- **Plotly** - Interactive charts (Business Games analytics)
- **Altair** - Statistical visualizations
- **Matplotlib** - Basic charts
- **Folium** - Map visualizations (FMCG route planning)

### Audio Processing
- **gTTS** - Text-to-Speech (Polish language)
- **ElevenLabs** - Premium TTS (optional)
- **SpeechRecognition** - Voice input (planned feature)

## Common Pitfalls

1. **Streamlit Config**: Must be called before ANY other Streamlit command
2. **Import Order**: Session init before page rendering
3. **JSON Encoding**: Handle datetime serialization manually
4. **Windows Paths**: Use `os.path.join()`, not hardcoded separators
5. **SQL Transactions**: Always commit after INSERT/UPDATE in repository pattern

## File Naming Patterns

- `fix_*.py` - One-off repair scripts (archived after use)
- `migrate_*.py` - Database migration scripts
- `test_*.py` - Test files (active or in `tests/archive/`)
- `*_backup_*.json` - Automatic backups (timestamped)
- `cleanup_*.py` - Data cleanup utilities

## Documentation

- **README.md** - Comprehensive app documentation
- **CHANGELOG_2025_10_27.md** - Detailed change log
- **FMCG_*.md** - FMCG game design specs
- **BETA_*.md** - Beta testing guides
- Archived docs in `docs/archive/`

## Company-Based Permissions System (Dec 2025)

### Architecture
- **Company Templates**: `config/company_templates.json` - Warta/Heinz/Milwaukee presets
- **User Model**: Extended with `company`, `permissions`, `account_created_by` fields
- **Admin Panel**: Create users with company-specific access (views/admin.py)
- **Permissions Helper**: `utils/permissions.py` - Check access to content/tools

### Usage
```python
from utils.permissions import has_access_to_lesson, get_ranking_scope

# Check access
if has_access_to_lesson('intro_1', user_data):
    show_lesson()

# Get ranking scope
scope = get_ranking_scope(user_data)  # 'none', 'company', or 'global'
```

### Admin Workflow
1. **Admin creates account** → selects company (Warta/Heinz/Milwaukee)
2. **Auto-applies permissions** from company template
3. **Optional customization** for individual users
4. **User logs in** → sees only assigned content/tools

### Integration Points (Completed)
- **views/admin.py**: `is_lesson_accessible()` - replaced old JSON system with SQL permissions
- **views/lesson.py**: Filters lessons by `has_access_to_lesson()`
- **views/business_games.py**: Filters scenarios/types, rankings by company scope
- **views/inspirations.py**: Filters categories by `has_access_to_inspiration_category()`
- **utils/components.py**: `navigation_menu()` - hides tools without access

## Recent Major Changes (Oct 2025)

- Business Games refactored to modular architecture
- AI Conversation contracts with TTS added
- 112 files archived/cleaned (25-30 MB freed)
- Custom CSS simplified (removed 130 lines)
- SQL migration from pure JSON to hybrid system

---

**When making changes**: Prioritize modularity, maintain the repository pattern, and always test with `python -m streamlit run main.py` on Windows.
