"""Diagnostic: Check lesson visibility for mil2"""
import streamlit as st
from data.lessons import load_lessons
from data.users_sql import get_current_user_data
from utils.resource_access import get_resource_tags

st.title("🔍 Diagnostyka widoczności lekcji Milwaukee Canvas")

# Sprawdź czy użytkownik jest zalogowany
if 'username' not in st.session_state:
    st.error("Musisz być zalogowany jako mil2")
    st.stop()

username = st.session_state.username
st.write(f"**Zalogowany użytkownik:** {username}")

# Pobierz dane użytkownika
user_data = get_current_user_data(username)
st.write("### Dane użytkownika z SQL:")
st.json({
    'company': user_data.get('company', 'BRAK'),
    'xp': user_data.get('xp'),
    'level': user_data.get('level')
})

# Załaduj lekcje
lessons = load_lessons()
canvas_id = "MILWAUKEE_Application_First_Canvas"

st.write(f"### Sprawdzenie lekcji `{canvas_id}`:")

if canvas_id in lessons:
    st.success(f"✅ Lekcja ZNALEZIONA w load_lessons() ({len(lessons)} lekcji załadowanych)")
    canvas = lessons[canvas_id]
    st.write(f"**Tytuł:** {canvas.get('lesson', {}).get('title', 'BRAK')}")
    st.write(f"**Kategoria:** {canvas.get('metadata', {}).get('category', 'BRAK')}")
else:
    st.error(f"❌ Lekcja NIE ZNALEZIONA w load_lessons()")
    st.write(f"Dostępne lekcje Milwaukee:")
    mil_lessons = [k for k in lessons.keys() if 'MILWAUKEE' in k.upper()]
    st.write(mil_lessons)
    st.stop()

# Sprawdź tagi
tags = get_resource_tags('lessons', canvas_id)
st.write(f"**Tagi lekcji:** {tags}")

# Sprawdź logikę filtrowania
user_company = user_data.get('company', 'General')
st.write("### Logika filtrowania:")
st.write(f"- `user_company`: **{user_company}**")
st.write(f"- `'{user_company}' in tags`: **{'Milwaukee' in tags}**")
st.write(f"- `'General' in tags`: **{'General' in tags}**")

should_be_visible = user_company in tags or 'General' in tags
if should_be_visible:
    st.success(f"✅ Lekcja **POWINNA BYĆ WIDOCZNA** dla {username}")
else:
    st.error(f"❌ Lekcja **NIE POWINNA BYĆ WIDOCZNA** dla {username}")

st.write("---")
st.write("### Akcje naprawcze:")
st.write("1. Kliknij **Clear cache** w menu Streamlit (⋮ → Clear cache)")
st.write("2. Odśwież stronę (Ctrl+Shift+R)")
st.write("3. Wyloguj się i zaloguj ponownie")
