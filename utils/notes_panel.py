"""
Notes Panel Component - Floating notatnik dla gracza podczas rozmowy
Używany w coaching_tool.py i FMCG game
"""

import streamlit as st
from typing import Optional, List, Dict
from repository.notes import NotesRepository


def render_notes_panel(
    user_id: int,
    active_tab: str = "product_card",
    scenario_context: Optional[str] = None,
    client_name: Optional[str] = None,
    key_prefix: str = "notes",
    available_products: Optional[List[Dict]] = None,
    available_clients: Optional[List[Dict]] = None
):
    """
    Renderuje floating panel z notatkami gracza
    
    Args:
        user_id: ID użytkownika
        active_tab: Domyślnie aktywna zakładka
        scenario_context: Opcjonalny kontekst scenariusza (do auto-sugestii)
        client_name: Nazwa klienta (do filtrowania notatek)
        key_prefix: Prefix dla kluczy widgetów (aby uniknąć duplikatów)
        available_products: Lista dostępnych produktów (dla menu rozwijanego)
        available_clients: Lista dostępnych klientów (dla menu rozwijanego)
    """
    
    # Inicjalizacja repository
    repo = NotesRepository()
    
    # Panel header
    st.markdown("### 📔 Notatnik")
    
    # Zakładki - ROZSZERZONE
    tab_mapping = {
        "📦 Produkty": "product_card",
        "🎯 Pitches": "elevator_pitch",
        "👤 Klient": "client_profile",
        "💡 Pomysły": "visit_ideas",
        "📊 Analiza": "market_analysis",
        "🎓 Szkolenie": "training_notes"
    }
    
    selected_tab = st.tabs(list(tab_mapping.keys()))
    
    for i, (tab_name, category) in enumerate(tab_mapping.items()):
        with selected_tab[i]:
            # Pobierz notatki dla tej kategorii
            notes = repo.get_user_notes(user_id, category=category)
            
            if notes:
                # Wyświetl notatki
                for note in notes:
                    _render_note_item(note, repo, user_id, key_prefix)
            else:
                st.info(f"Brak notatek w kategorii **{tab_name}**")
            
            # Przycisk dodawania
            st.markdown("---")
            if st.button(f"➕ Dodaj notatkę", key=f"{key_prefix}_add_note_{category}"):
                st.session_state[f'{key_prefix}_adding_note_{category}'] = True
            
            # Formularz dodawania (jeśli aktywny)
            if st.session_state.get(f'{key_prefix}_adding_note_{category}', False):
                _render_add_note_form(
                    user_id, 
                    category, 
                    repo, 
                    key_prefix,
                    available_products=available_products if category == "product_card" else None,
                    available_clients=available_clients if category == "client_profile" else None
                )


def _render_note_item(note: Dict, repo: NotesRepository, user_id: int, key_prefix: str = "notes"):
    """Renderuje pojedynczą notatkę"""
    
    note_id = note['note_id']
    is_pinned = note['is_pinned']
    
    # Container z notatką
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # Tytuł z ikoną przypięcia
            pin_emoji = "📌 " if is_pinned else ""
            st.markdown(f"**{pin_emoji}{note['title']}**")
        
        with col2:
            # Akcje
            if st.button("📌" if not is_pinned else "✖", 
                        key=f"{key_prefix}_pin_{note_id}", 
                        help="Przypnij/Odepnij"):
                repo.toggle_pin(note_id)
                st.rerun()
        
        # Treść notatki
        content = note['content']
        # Skróć jeśli za długa (bez nested expander)
        if len(content) > 200:
            st.markdown("**Pełna treść:**")
            st.text(content)
        else:
            st.text(content)
        
        # Tagi
        if note['tags']:
            tags_html = " ".join([
                f"<span style='background: #e9ecef; padding: 2px 8px; border-radius: 12px; "
                f"font-size: 11px; color: #495057; margin-right: 4px;'>#{tag}</span>"
                for tag in note['tags']
            ])
            st.markdown(tags_html, unsafe_allow_html=True)
        
        # Metadata
        st.caption(f"🕐 {note['updated_at']}")
        
        st.markdown("---")


def _render_add_note_form(user_id: int, category: str, repo: NotesRepository, key_prefix: str = "notes", 
                          available_products=None, available_clients=None):
    """Renderuje formularz dodawania notatki z opcjonalnymi menu rozwijalnymi"""
    
    with st.form(key=f"{key_prefix}_add_note_form_{category}"):
        st.markdown("**➕ Nowa notatka**")
        
        title = st.text_input("Tytuł", key=f"{key_prefix}_note_title_{category}")
        
        # Menu rozwijane dla produktów
        selected_product_id = None
        if category == "product_card" and available_products:
            product_options = {f"{p.get('name', 'Nieznany')} ({p.get('sku', '')})" : p.get('id') for p in available_products}
            product_options = {"-- Wybierz produkt (opcjonalnie) --": None, **product_options}
            
            selected_product_name = st.selectbox(
                "Produkt",
                options=list(product_options.keys()),
                key=f"{key_prefix}_note_product_{category}",
                help="Powiąż notatkę z konkretnym produktem"
            )
            selected_product_id = product_options.get(selected_product_name)
        
        # Menu rozwijane dla klientów
        selected_client_id = None
        if category == "client_profile" and available_clients:
            client_options = {f"{c.get('name', 'Nieznany')} ({c.get('id', '')})" : c.get('id') for c in available_clients}
            client_options = {"-- Wybierz klienta (opcjonalnie) --": None, **client_options}
            
            selected_client_name = st.selectbox(
                "Klient",
                options=list(client_options.keys()),
                key=f"{key_prefix}_note_client_{category}",
                help="Powiąż notatkę z konkretnym klientem"
            )
            selected_client_id = client_options.get(selected_client_name)
        
        content = st.text_area("Treść", key=f"{key_prefix}_note_content_{category}", height=100)
        
        tags_input = st.text_input(
            "Tagi (oddzielone przecinkami)", 
            key=f"{key_prefix}_note_tags_{category}",
            placeholder="np. premium, czekolada, marża"
        )
        
        is_pinned = st.checkbox("📌 Przypnij notatkę", key=f"{key_prefix}_note_pin_{category}")
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 Zapisz", type="primary")
        with col2:
            cancelled = st.form_submit_button("❌ Anuluj")
        
        if submitted and title and content:
            # Parsuj tagi
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            
            # Utwórz notatkę z powiązaniami
            repo.create_note(
                user_id=user_id,
                category=category,
                title=title,
                content=content,
                related_product_id=selected_product_id,  # NOWE!
                related_client_id=selected_client_id,    # NOWE!
                is_pinned=is_pinned,
                tags=tags if tags else None
            )
            
            st.success(f"✅ Notatka '{title}' została dodana!")
            st.session_state[f'{key_prefix}_adding_note_{category}'] = False
            st.rerun()
        
        if cancelled:
            st.session_state[f'{key_prefix}_adding_note_{category}'] = False
            st.rerun()


def render_notes_panel_compact(user_id: int, search_enabled: bool = True):
    """
    Kompaktowa wersja panelu notatek (dla mobile/tablet)
    
    Args:
        user_id: ID użytkownika
        search_enabled: Czy pokazać wyszukiwarkę
    """
    
    repo = NotesRepository()
    
    st.markdown("### 📔 Szybki dostęp - Notatki")
    
    # Wyszukiwarka
    if search_enabled:
        search_term = st.text_input(
            "🔍 Szukaj w notatkach",
            placeholder="Wpisz frazę...",
            key="notes_search"
        )
        
        if search_term:
            results = repo.search_notes(user_id, search_term)
            st.markdown(f"**Wyniki wyszukiwania ({len(results)}):**")
            
            for note in results[:5]:  # Max 5 wyników
                with st.expander(f"{'📌 ' if note['is_pinned'] else ''}{note['title']}"):
                    st.text(note['content'])
                    if note['tags']:
                        st.caption(f"Tagi: {', '.join([f'#{t}' for t in note['tags']])}")
            
            return
    
    # Przypięte notatki
    pinned_notes = repo.get_user_notes(user_id, pinned_only=True)
    
    if pinned_notes:
        st.markdown("**📌 Przypięte notatki:**")
        
        for note in pinned_notes[:5]:  # Max 5 przypiętych
            category_emoji = {
                'product_card': '📦',
                'elevator_pitch': '🎯',
                'mentor_tip': '🎓',
                'manager_feedback': '📊',
                'client_profile': '👤',
                'personal': '✍️'
            }.get(note['category'], '📝')
            
            with st.expander(f"{category_emoji} {note['title']}", expanded=False):
                st.text(note['content'][:200] + "..." if len(note['content']) > 200 else note['content'])
                
                if st.button("👁️ Zobacz pełną", key=f"view_full_{note['note_id']}"):
                    st.session_state[f'viewing_note_{note["note_id"]}'] = True
    else:
        st.info("Brak przypiętych notatek. Dodaj notatki w Dashboard!")


def get_notes_stats_widget(user_id: int):
    """
    Widget ze statystykami notatek (dla dashboard)
    
    Returns:
        HTML string z kartą statystyk
    """
    
    repo = NotesRepository()
    stats = repo.get_notes_stats(user_id)
    
    total = stats['total']
    
    return f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px; border-radius: 12px; color: white;'>
        <div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>📔 Notatnik</div>
        <div style='font-size: 32px; font-weight: 600; margin-bottom: 4px;'>{total}</div>
        <div style='font-size: 12px; opacity: 0.8;'>
            {stats['product_card']} produktów | {stats['elevator_pitch']} pitches | {stats['client_profile']} klientów
        </div>
    </div>
    """
