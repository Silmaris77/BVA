"""
Dashboard - Notes Management Section
Sekcja zarządzania notatkami w dashboard
"""

import streamlit as st
from repository.notes import NotesRepository
from typing import Dict, List


def show_notes_management_section(user_data: Dict):
    """
    Sekcja zarządzania notatkami w dashboard
    
    Args:
        user_data: Dane użytkownika
    """
    
    user_id = user_data.get('user_id', 1)  # Fallback dla testów
    repo = NotesRepository()
    
    st.markdown("---")
    st.markdown("### 📔 Notatnik")
    
    # Statystyki + kontrolki w jednej linii
    stats = repo.get_notes_stats(user_id)
    
    col_stats, col_controls = st.columns([2, 1])
    
    with col_stats:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 15px 20px; border-radius: 12px; color: white;'>
            <div style='font-size: 14px; opacity: 0.9; margin-bottom: 4px;'>📔 Twoje notatki</div>
            <div style='font-size: 28px; font-weight: 600;'>{stats['total']}</div>
            <div style='font-size: 12px; opacity: 0.8; margin-top: 4px;'>
                {stats['product_card']} produktów | {stats['elevator_pitch']} pitches | {stats['client_profile']} klientów
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_controls:
        # Filtr kategorii
        category_options = {
            "🗂️ Wszystkie": None,
            "📦 Produkty": "product_card",
            "🎯 Pitches": "elevator_pitch",
            "🎓 Mentor": "mentor_tip",
            "📊 Manager": "manager_feedback",
            "👤 Klienci": "client_profile",
            "✍️ Własne": "personal"
        }
        
        selected_category_label = st.selectbox(
            "Kategoria",
            options=list(category_options.keys()),
            key="notes_category_filter"
        )
        selected_category = category_options[selected_category_label]
    
    # Wyszukiwarka
    col_search, col_add = st.columns([3, 1])
    
    with col_search:
        search_term = st.text_input(
            "🔍 Szukaj w notatkach",
            placeholder="Wpisz frazę, tag lub słowo kluczowe...",
            key="notes_search_dashboard"
        )
    
    with col_add:
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)  # Spacer
        if st.button("➕ Nowa notatka", key="add_note_dashboard", type="primary", use_container_width=True):
            st.session_state['adding_new_note'] = True
    
    # Formularz dodawania nowej notatki
    if st.session_state.get('adding_new_note', False):
        _render_add_note_modal(user_id, repo)
        return  # Zatrzymaj rendering reszty gdy formularz otwarty
    
    # Pobierz notatki (search lub filter)
    if search_term:
        notes = repo.search_notes(user_id, search_term, category=selected_category)
        st.info(f"🔍 Znaleziono {len(notes)} notatek dla '{search_term}'")
    else:
        notes = repo.get_user_notes(user_id, category=selected_category)
    
    # Wyświetl notatki w grid
    if notes:
        _render_notes_grid(notes, repo, user_id)
    else:
        st.info("📝 Brak notatek w tej kategorii. Dodaj pierwszą notatkę klikając '➕ Nowa notatka'")


def _render_notes_grid(notes: List[Dict], repo: NotesRepository, user_id: int):
    """Renderuje grid z kartami notatek"""
    
    # Grid - 3 kolumny na desktop, 1 na mobile
    num_cols = 3
    cols = st.columns(num_cols)
    
    for idx, note in enumerate(notes):
        col_idx = idx % num_cols
        
        with cols[col_idx]:
            _render_note_card(note, repo, user_id)


def _render_note_card(note: Dict, repo: NotesRepository, user_id: int):
    """Renderuje pojedynczą kartę notatki"""
    
    note_id = note['note_id']
    category = note['category']
    
    # Kategoria badge
    category_config = {
        'product_card': {'emoji': '📦', 'color': '#e3f2fd', 'text_color': '#1976d2', 'label': 'Produkt'},
        'elevator_pitch': {'emoji': '🎯', 'color': '#f3e5f5', 'text_color': '#7b1fa2', 'label': 'Pitch'},
        'mentor_tip': {'emoji': '🎓', 'color': '#fff3e0', 'text_color': '#e65100', 'label': 'Mentor'},
        'manager_feedback': {'emoji': '📊', 'color': '#e8f5e9', 'text_color': '#2e7d32', 'label': 'Manager'},
        'client_profile': {'emoji': '👤', 'color': '#fce4ec', 'text_color': '#c2185b', 'label': 'Klient'},
        'personal': {'emoji': '✍️', 'color': '#f1f8e9', 'text_color': '#558b2f', 'label': 'Osobiste'}
    }
    
    config = category_config.get(category, {'emoji': '📝', 'color': '#f5f5f5', 'text_color': '#666', 'label': 'Inne'})
    
    # Karta
    card_html = f"""
    <div style='background: white; border-radius: 12px; padding: 20px; margin-bottom: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s, box-shadow 0.2s;'
         onmouseover='this.style.transform="translateY(-4px)"; this.style.boxShadow="0 8px 20px rgba(0,0,0,0.15)";'
         onmouseout='this.style.transform="translateY(0)"; this.style.boxShadow="0 2px 8px rgba(0,0,0,0.1)";'>
        
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;'>
            <span style='background: {config['color']}; color: {config['text_color']};
                         padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600;
                         text-transform: uppercase;'>
                {config['emoji']} {config['label']}
            </span>
            <span style='font-size: 20px;'>
                {'📌' if note['is_pinned'] else ''}
            </span>
        </div>
        
        <div style='font-weight: 600; color: #333; margin-bottom: 10px; font-size: 16px;'>
            {note['title']}
        </div>
        
        <div style='color: #666; line-height: 1.6; margin-bottom: 15px; font-size: 14px;
                    max-height: 100px; overflow: hidden;'>
            {note['content'][:150]}{'...' if len(note['content']) > 150 else ''}
        </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Tagi
    if note['tags']:
        tags_html = " ".join([
            f"<span style='background: #e9ecef; padding: 3px 10px; border-radius: 12px; "
            f"font-size: 11px; color: #495057; margin-right: 4px;'>#{tag}</span>"
            for tag in note['tags'][:3]  # Max 3 tagi
        ])
        st.markdown(f"<div style='margin-bottom: 12px;'>{tags_html}</div>", unsafe_allow_html=True)
    
    # Footer
    footer_html = f"""
        <div style='display: flex; justify-content: space-between; align-items: center;
                    padding-top: 12px; border-top: 1px solid #e9ecef;'>
            <span style='color: #999; font-size: 12px;'>
                🕐 {note['updated_at'][:16]}
            </span>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
    
    # Akcje (buttony poniżej karty)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📌" if not note['is_pinned'] else "✖", 
                    key=f"pin_note_{note_id}",
                    help="Przypnij/Odepnij",
                    use_container_width=True):
            repo.toggle_pin(note_id)
            st.rerun()
    
    with col2:
        if st.button("✏️", key=f"edit_note_{note_id}", help="Edytuj", use_container_width=True):
            st.session_state['editing_note_id'] = note_id
            st.rerun()
    
    with col3:
        if st.button("🗑️", key=f"delete_note_{note_id}", help="Usuń", use_container_width=True):
            repo.delete_note(note_id)
            st.success(f"✅ Usunięto notatkę '{note['title']}'")
            st.rerun()
    
    # Modal edycji (jeśli aktywny)
    if st.session_state.get('editing_note_id') == note_id:
        _render_edit_note_modal(note, repo)


def _render_add_note_modal(user_id: int, repo: NotesRepository):
    """Modal dodawania nowej notatki"""
    
    st.markdown("---")
    st.markdown("### ➕ Nowa notatka")
    
    with st.form(key="add_note_form_dashboard"):
        # Kategoria
        category_options = {
            "📦 Produkt": "product_card",
            "🎯 Elevator Pitch": "elevator_pitch",
            "🎓 Wskazówka Mentora": "mentor_tip",
            "📊 Feedback Menedżera": "manager_feedback",
            "👤 Profil Klienta": "client_profile",
            "✍️ Notatka osobista": "personal"
        }
        
        selected_cat_label = st.selectbox("Kategoria", options=list(category_options.keys()))
        category = category_options[selected_cat_label]
        
        # Tytuł
        title = st.text_input("Tytuł notatki", placeholder="np. Chocolate Supreme")
        
        # Treść
        content = st.text_area(
            "Treść", 
            height=150,
            placeholder="np. Cena: €15.20\nMarża: 35%\nUSP: Premium kakao z Ghany"
        )
        
        # Tagi
        tags_input = st.text_input(
            "Tagi (oddzielone przecinkami)",
            placeholder="np. czekolada, premium, fairtrade"
        )
        
        # Przypnij
        is_pinned = st.checkbox("📌 Przypnij notatkę (będzie na górze listy)")
        
        # Buttony
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 Zapisz", type="primary", use_container_width=True)
        with col2:
            cancelled = st.form_submit_button("❌ Anuluj", use_container_width=True)
        
        if submitted and title and content:
            # Parsuj tagi
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            
            # Utwórz notatkę
            repo.create_note(
                user_id=user_id,
                category=category,
                title=title,
                content=content,
                is_pinned=is_pinned,
                tags=tags if tags else None
            )
            
            st.success(f"✅ Notatka '{title}' została dodana!")
            st.session_state['adding_new_note'] = False
            st.rerun()
        
        if cancelled:
            st.session_state['adding_new_note'] = False
            st.rerun()


def _render_edit_note_modal(note: Dict, repo: NotesRepository):
    """Modal edycji notatki"""
    
    note_id = note['note_id']
    
    st.markdown("---")
    st.markdown(f"### ✏️ Edycja: {note['title']}")
    
    with st.form(key=f"edit_note_form_{note_id}"):
        # Tytuł
        new_title = st.text_input("Tytuł", value=note['title'])
        
        # Treść
        new_content = st.text_area("Treść", value=note['content'], height=150)
        
        # Tagi
        current_tags = ", ".join(note['tags']) if note['tags'] else ""
        new_tags_input = st.text_input("Tagi (oddzielone przecinkami)", value=current_tags)
        
        # Przypnij
        new_is_pinned = st.checkbox("📌 Przypnij notatkę", value=note['is_pinned'])
        
        # Buttony
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 Zapisz zmiany", type="primary", use_container_width=True)
        with col2:
            cancelled = st.form_submit_button("❌ Anuluj", use_container_width=True)
        
        if submitted:
            # Parsuj tagi
            new_tags = [tag.strip() for tag in new_tags_input.split(",") if tag.strip()]
            
            # Aktualizuj
            repo.update_note(
                note_id=note_id,
                title=new_title,
                content=new_content,
                is_pinned=new_is_pinned,
                tags=new_tags if new_tags else None
            )
            
            st.success(f"✅ Zaktualizowano notatkę!")
            st.session_state['editing_note_id'] = None
            st.rerun()
        
        if cancelled:
            st.session_state['editing_note_id'] = None
            st.rerun()
