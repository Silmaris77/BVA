# Config package for BrainventureAcademy

# Zapewniamy, że moduł config jest rozpoznawany jako package
__all__ = ['settings']

# Bezpieczny import - nie rzucamy błędów jeśli import nie działa
try:
    from .settings import PAGE_CONFIG, XP_LEVELS, LESSONS_FILE_PATH
except Exception:
    # Fallback w przypadku problemów z importem
    PAGE_CONFIG = {
        "page_title": "BrainventureAcademy",
        "page_icon": "🧠",
        "layout": "wide",
        "initial_sidebar_state": "expanded",
        "menu_items": {
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    }
    XP_LEVELS = {1: 0, 2: 100, 3: 250, 4: 500, 5: 1000}
    LESSONS_FILE_PATH = "data/lessons.json"