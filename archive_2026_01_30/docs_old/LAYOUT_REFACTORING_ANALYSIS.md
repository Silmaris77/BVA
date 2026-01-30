# 🎨 Analiza i Refaktoryzacja Systemu Layoutów
**Data:** 31.10.2025  
**Cel:** Uporządkowanie kodu przed dodaniem nowych wariantów layoutów

---

## 📊 OBECNY STAN - Audit

### 1. Struktura plików CSS
```
static/css/
├── core/                           ❌ PUSTY - niewykorzystany
├── themes/
│   ├── standard.css               ✅ Layout Standard (1660 linii)
│   ├── gaming-pro.css             ✅ Layout Gaming Pro
│   ├── halloween.css              ✅ Layout Halloween
│   ├── executive-pro.css          ✅ Layout Executive Pro (565 linii)
│   ├── classic.css                ⚠️  Nieużywany?
│   ├── executive-pro.css.backup   🗑️ Backup do usunięcia
│   └── executive-pro.css.OLD      🗑️ Backup do usunięcia
├── material3_extended.css         ✅ Bazowe style Material 3 (450 linii)
├── style.css                      ⚠️  Rola niejasna
└── mobile-navigation.css          ✅ Nawigacja mobile

assets/css/
└── login.css                      ✅ Style logowania
```

### 2. Kod Python odpowiedzialny za layouty

#### **main.py** (linie 76-106)
```python
def load_css(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        css = f.read()
    return css

def get_user_layout():
    """Pobiera preferencję layoutu użytkownika"""
    if st.session_state.get('logged_in', False):
        try:
            from data.users import load_user_data
            users_data = load_user_data()
            user_data = users_data.get(st.session_state.get('username'), {})
            return user_data.get('layout_preference', 'standard')
        except:
            return 'standard'
    return 'standard'

# Wybierz odpowiedni plik CSS na podstawie preferencji użytkownika
user_layout = get_user_layout()
theme_path = os.path.join(os.path.dirname(__file__), "static", "css", "themes", f"{user_layout}.css")

# Załaduj CSS layoutu
if os.path.exists(theme_path):
    css = load_css(theme_path)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
else:
    # Fallback to standard if theme file doesn't exist
    css_path = os.path.join(os.path.dirname(__file__), "static", "css", "themes", "standard.css")
    css = load_css(css_path)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
```

**❌ PROBLEMY:**
- Funkcja `load_css()` duplikuje się z `css_loader.py`
- Ładowanie CSS bezpośrednio w main.py (powinno być w dedykowanym module)
- Brak cache'owania CSS
- Brak walidacji czy plik istnieje przed próbą czytania

#### **utils/material3_components.py**
```python
def load_extended_material3_css():
    """Ładuje rozszerzony zestaw stylów Material 3"""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "css", "material3_extended.css")
    
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Nie można znaleźć pliku css: {css_path}")

def m3_button_styles():
    """Dodaje style przycisków Material 3 do interfejsu"""
    return st.markdown("""...""", unsafe_allow_html=True)

def m3_lesson_card_styles():
    """Dodaje style kart lekcji Material 3 do interfejsu"""
    return st.markdown("""...""", unsafe_allow_html=True)

def apply_material3_theme():
    """Aplikuje wszystkie style Material 3 w aplikacji"""
    load_extended_material3_css()
    apply_responsive_styles()
    m3_button_styles()
    m3_lesson_card_styles()
    # ... +100 linii inline CSS
```

**❌ PROBLEMY:**
- Duplikacja funkcji `load_css()` (już jest w main.py)
- Inline CSS w Pythonie zamiast w plikach .css
- Funkcja `apply_material3_theme()` ma 180 linii, z czego 150 to inline CSS
- Style Material 3 są "wstrzykiwane" globalnie, niezależnie od wybranego layoutu
- Brak separacji między base styles a theme-specific styles

#### **utils/css_loader.py**
```python
def ensure_css_files():
    """Upewnia się, że wszystkie wymagane katalogi i pliki CSS istnieją"""
    os.makedirs('assets/css', exist_ok=True)
    
    if not os.path.exists('assets/css/login.css'):
        with open('assets/css/login.css', 'w') as f:
            f.write("""...""")

def load_login_css():
    """Ładuje style CSS dla strony logowania"""
    try:
        with open('assets/css/login.css', 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Plik CSS dla logowania nie został znaleziony.")
```

**❌ PROBLEMY:**
- Tworzenie pliku CSS w runtime (powinien być w repo)
- Funkcja `load_login_css()` tylko dla logowania, nie jest uniwersalna
- Brak cache'owania

#### **utils/layout.py**
```python
def apply_responsive_styles():
    """Dodaje globalne style CSS dla responsywności"""
    st.markdown("""
    <style>
    /* 187 linii inline CSS dla responsive */
    </style>
    """, unsafe_allow_html=True)
```

**❌ PROBLEMY:**
- 187 linii inline CSS w Pythonie
- Powinno być w osobnym pliku responsive.css

### 3. Miejsca wywołań `apply_material3_theme()`
```
views/profile.py:248
views/lesson.py:63
views/login.py:27
views/skills_new.py:16
views/tools.py:2591
```

**❌ PROBLEM:**
- Każdy view musi pamiętać o wywołaniu `apply_material3_theme()`
- Ryzyko niespójności (np. tools.py:2591 - gdzieś głęboko w funkcji)

---

## 🎯 PROPONOWANA REFAKTORYZACJA

### Faza 1: Centralizacja ładowania CSS

#### 1.1 Nowy moduł `utils/theme_manager.py`
```python
"""
Centralny manager motywów/layoutów dla aplikacji.
Odpowiada za ładowanie CSS i aplikowanie stylów.
"""

import streamlit as st
import os
from functools import lru_cache

class ThemeManager:
    """Zarządza motywami i layoutami aplikacji"""
    
    THEMES_DIR = "static/css/themes"
    DEFAULT_THEME = "standard"
    
    # Dostępne motywy
    AVAILABLE_THEMES = {
        'standard': {
            'name': 'Standard',
            'css_file': 'standard.css',
            'description': 'Klasyczny Material Design',
            'icon': '📱'
        },
        'gaming-pro': {
            'name': 'Gaming Pro',
            'css_file': 'gaming-pro.css',
            'description': 'Fioletowo-cyjanowy gaming vibe',
            'icon': '🎮'
        },
        'halloween': {
            'name': 'Halloween',
            'css_file': 'halloween.css',
            'description': 'Halloweenowy klimat',
            'icon': '🎃'
        },
        'executive-pro': {
            'name': 'Executive Pro',
            'css_file': 'executive-pro.css',
            'description': 'Navy & Gold dla kadry zarządzającej',
            'icon': '💼'
        }
    }
    
    @staticmethod
    @lru_cache(maxsize=10)
    def load_css_file(file_path: str) -> str:
        """Ładuje plik CSS z cache'owaniem"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            st.error(f"⚠️ Plik CSS nie znaleziony: {file_path}")
            return ""
    
    @staticmethod
    def get_user_theme() -> str:
        """Pobiera aktywny motyw użytkownika"""
        if not st.session_state.get('logged_in', False):
            return ThemeManager.DEFAULT_THEME
        
        try:
            from data.users import load_user_data
            users_data = load_user_data()
            username = st.session_state.get('username')
            user_data = users_data.get(username, {})
            theme = user_data.get('layout_preference', ThemeManager.DEFAULT_THEME)
            
            # Walidacja czy motyw istnieje
            if theme not in ThemeManager.AVAILABLE_THEMES:
                return ThemeManager.DEFAULT_THEME
            
            return theme
        except Exception as e:
            st.warning(f"Błąd ładowania preferencji motywu: {e}")
            return ThemeManager.DEFAULT_THEME
    
    @staticmethod
    def apply_theme(theme_key: str = None):
        """Aplikuje wybrany motyw"""
        if theme_key is None:
            theme_key = ThemeManager.get_user_theme()
        
        theme_config = ThemeManager.AVAILABLE_THEMES.get(theme_key)
        if not theme_config:
            theme_key = ThemeManager.DEFAULT_THEME
            theme_config = ThemeManager.AVAILABLE_THEMES[theme_key]
        
        css_file = theme_config['css_file']
        css_path = os.path.join(ThemeManager.THEMES_DIR, css_file)
        
        if not os.path.exists(css_path):
            st.error(f"⚠️ Plik motywu nie istnieje: {css_path}")
            return
        
        css = ThemeManager.load_css_file(css_path)
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    @staticmethod
    def apply_base_styles():
        """Aplikuje bazowe style (Material 3, responsive)"""
        # Material 3 extended
        material3_path = "static/css/material3_extended.css"
        if os.path.exists(material3_path):
            css = ThemeManager.load_css_file(material3_path)
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        
        # Mobile navigation
        mobile_nav_path = "static/css/mobile-navigation.css"
        if os.path.exists(mobile_nav_path):
            css = ThemeManager.load_css_file(mobile_nav_path)
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    
    @staticmethod
    def apply_all():
        """Aplikuje wszystkie style: base + theme"""
        ThemeManager.apply_base_styles()
        ThemeManager.apply_theme()
```

#### 1.2 Uproszczenie `main.py`
```python
# Zamiast 30+ linii kodu CSS loading:

from utils.theme_manager import ThemeManager

def main():
    init_session_state()
    
    # Aplikuj style (base + user theme)
    ThemeManager.apply_all()
    
    # ... reszta kodu
```

#### 1.3 Usunięcie wywołań z views
```python
# views/profile.py, lesson.py, login.py, skills_new.py, tools.py
# USUŃ: apply_material3_theme()
# Style są już załadowane w main.py przez ThemeManager.apply_all()
```

### Faza 2: Przeniesienie inline CSS do plików

#### 2.1 Wydzielenie `static/css/core/base.css`
```css
/* Bazowe style Material 3 - używane przez wszystkie motywy */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

/* Typography */
html, body, [class*="css"] {
    font-family: 'Roboto', sans-serif;
}

h1, h2, h3 {
    color: #1A237E;
    font-weight: 500;
}

/* Material 3 ripple animation */
@keyframes m3-ripple {
    0% { transform: scale(0); opacity: 1; }
    100% { transform: scale(2); opacity: 0; }
}

/* ... pozostałe 150 linii z apply_material3_theme() */
```

#### 2.2 Wydzielenie `static/css/core/components.css`
```css
/* Material 3 Components - Buttons, Cards, Forms */

/* Button Styles */
.stButton button {
    background-color: #2196F3 !important;
    color: white !important;
    /* ... */
}

/* Lesson Cards */
.m3-lesson-card {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 20%, #dee2e6 50%, #ced4da 80%, #adb5bd 100%);
    /* ... */
}

/* ... pozostałe komponenty z m3_button_styles() i m3_lesson_card_styles() */
```

#### 2.3 Wydzielenie `static/css/core/responsive.css`
```css
/* Responsive styles - z layout.py apply_responsive_styles() */

@media (max-width: 640px) {
    .hide-mobile { display: none !important; }
    /* ... 187 linii */
}
```

#### 2.4 Aktualizacja `material3_extended.css`
```css
/* Material 3 Extended - imports core files */
@import url('core/base.css');
@import url('core/components.css');
@import url('core/responsive.css');

/* Pozostałe style specyficzne dla Material 3 Extended */
:root {
  --md-primary: #2196F3;
  /* ... zmienne */
}

/* Ripple effect */
.ripple { /* ... */ }
```

#### 2.5 Uproszczenie `utils/material3_components.py`
```python
# PO REFAKTORYZACJI - tylko 10 linii!

from utils.theme_manager import ThemeManager

def apply_material3_theme():
    """Legacy function - używaj ThemeManager.apply_all() zamiast tego"""
    ThemeManager.apply_all()

# Usunięte:
# - load_extended_material3_css() → ThemeManager.apply_base_styles()
# - m3_button_styles() → static/css/core/components.css
# - m3_lesson_card_styles() → static/css/core/components.css
# - 180 linii inline CSS → pliki .css
```

#### 2.6 Uproszczenie `utils/layout.py`
```python
# Usunięte apply_responsive_styles() - przeniesione do CSS

# Zachowane:
# - get_device_type()
# - responsive_grid()
# - get_responsive_figure_size()
# - toggle_device_view()
```

### Faza 3: Czyszczenie i organizacja

#### 3.1 Usunięcie duplikatów
```bash
# Usuń:
static/css/themes/executive-pro.css.backup
static/css/themes/executive-pro.css.OLD

# Sprawdź czy używany, jeśli nie - usuń:
static/css/themes/classic.css
static/css/style.css
```

#### 3.2 Struktura po refaktoryzacji
```
static/css/
├── core/
│   ├── base.css              ✨ NOWY - bazowe style M3
│   ├── components.css        ✨ NOWY - komponenty (buttons, cards)
│   └── responsive.css        ✨ NOWY - media queries
├── themes/
│   ├── standard.css          ✅ Uproszczony
│   ├── gaming-pro.css        ✅ Bez zmian
│   ├── halloween.css         ✅ Bez zmian
│   └── executive-pro.css     ✅ Bez zmian
├── material3_extended.css    ♻️  Zrefaktoryzowany (imports z core/)
└── mobile-navigation.css     ✅ Bez zmian

utils/
├── theme_manager.py          ✨ NOWY - centralny manager
├── material3_components.py   ♻️  Tylko legacy wrapper (10 linii)
├── layout.py                 ♻️  Bez inline CSS (100 linii)
└── css_loader.py             🗑️ DO USUNIĘCIA (funkcjonalność w ThemeManager)
```

---

## 📈 KORZYŚCI Z REFAKTORYZACJI

### 1. Czytelność i utrzymanie
✅ **Przed:** 400+ linii inline CSS w Pythonie  
✅ **Po:** Cały CSS w plikach .css (łatwiejszy do edycji, formatowania, lintingu)

### 2. Performance
✅ **Cache'owanie:** `@lru_cache` na ładowaniu plików CSS  
✅ **Mniej duplikacji:** DRY principle

### 3. Dodawanie nowych motywów
✅ **Przed:** Dodaj CSS do themes/ + zaktualizuj profile.py  
✅ **Po:** Dodaj CSS do themes/ + wpis w `ThemeManager.AVAILABLE_THEMES`

### 4. Konsystencja
✅ **Jeden punkt wejścia:** `ThemeManager.apply_all()` w main.py  
✅ **Brak ryzyka:** Views nie muszą pamiętać o `apply_material3_theme()`

### 5. Testowanie
✅ **Łatwiejsze:** Można testować ThemeManager w izolacji  
✅ **Mock'owanie:** Łatwe podmienienie preferencji użytkownika

---

## 🚀 PLAN IMPLEMENTACJI

### Krok 1: Przygotowanie (5 min)
- [ ] Stwórz folder `static/css/core/`
- [ ] Backup aktualnych plików: `material3_components.py`, `layout.py`

### Krok 2: Wydzielenie CSS (15 min)
- [ ] Stwórz `static/css/core/base.css` (z `apply_material3_theme()`)
- [ ] Stwórz `static/css/core/components.css` (z `m3_button_styles()`, `m3_lesson_card_styles()`)
- [ ] Stwórz `static/css/core/responsive.css` (z `apply_responsive_styles()`)
- [ ] Zaktualizuj `material3_extended.css` (dodaj imports)

### Krok 3: Theme Manager (10 min)
- [ ] Stwórz `utils/theme_manager.py`
- [ ] Przetestuj `ThemeManager.apply_all()` w izolacji

### Krok 4: Integracja w main.py (5 min)
- [ ] Zastąp 30 linii kodu przez `ThemeManager.apply_all()`
- [ ] Przetestuj czy motywy ładują się poprawnie

### Krok 5: Czyszczenie views (10 min)
- [ ] Usuń `apply_material3_theme()` z `profile.py`
- [ ] Usuń `apply_material3_theme()` z `lesson.py`
- [ ] Usuń `apply_material3_theme()` z `login.py`
- [ ] Usuń `apply_material3_theme()` z `skills_new.py`
- [ ] Usuń `apply_material3_theme()` z `tools.py`

### Krok 6: Uproszczenie utils (5 min)
- [ ] Zredukuj `material3_components.py` do legacy wrappera
- [ ] Usuń `apply_responsive_styles()` z `layout.py`
- [ ] Usuń `css_loader.py` (jeśli nieużywany nigdzie indziej)

### Krok 7: Testowanie (10 min)
- [ ] Test: Layout Standard
- [ ] Test: Layout Gaming Pro
- [ ] Test: Layout Halloween
- [ ] Test: Layout Executive Pro
- [ ] Test: Responsive na mobile
- [ ] Test: Przełączanie między layoutami

### Krok 8: Cleanup (5 min)
- [ ] Usuń `executive-pro.css.backup`
- [ ] Usuń `executive-pro.css.OLD`
- [ ] Sprawdź czy `classic.css` i `style.css` są używane
- [ ] Commit zmian

**CAŁKOWITY CZAS:** ~60 minut

---

## ⚠️ RYZYKA I MITYGACJA

### Ryzyko 1:破Breaking zmiana w istniejących layoutach
**Mitygacja:** Krok po kroku, testy po każdym kroku

### Ryzyko 2: CSS nie ładuje się z powodu błędnych ścieżek
**Mitygacja:** Użycie `os.path.join()`, walidacja plików przed ładowaniem

### Ryzyko 3: Cache'owanie powoduje nieświeże style podczas developmentu
**Mitygacja:** `lru_cache` można wyczyścić, lub disable w dev mode

### Ryzyko 4: Coś wykorzystuje `apply_material3_theme()` poza views
**Mitygacja:** Zachowaj jako legacy wrapper z deprecation warning

---

## 📝 NOTATKI

### Pytania do usera:
1. Czy `static/css/style.css` jest używany? (może legacy)
2. Czy `static/css/themes/classic.css` jest używany?
3. Czy chcesz zachować backupy executive-pro.css czy usunąć?

### Przyszłe usprawnienia (poza scope):
- [ ] Hot reload CSS w dev mode (bez restartu Streamlit)
- [ ] Theme preview w profilu (podgląd przed zmianą)
- [ ] User-customizable colors (color picker w profilu)
- [ ] Dark/Light mode toggle dla każdego motywu
- [ ] Export/Import custom themes

---

**Status:** ✅ Gotowe do implementacji  
**Następny krok:** Decyzja usera czy implementować całość czy tylko część
