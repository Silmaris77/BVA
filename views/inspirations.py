import streamlit as st
import random
from utils.components import zen_header, zen_button
from utils.material3_components import apply_material3_theme
from utils.layout import get_device_type, toggle_device_view
from utils.inspirations_loader import (
    load_inspirations_data, get_categories,
    get_inspirations_by_category, search_inspirations, get_inspiration_by_id,
    load_inspiration_content, increment_inspiration_views,
    mark_inspiration_as_favorite, unmark_inspiration_as_favorite, 
    toggle_inspiration_favorite,  # Add toggle function
    is_inspiration_favorite, get_favorite_inspirations,
    get_random_inspiration, get_all_inspirations,
    mark_inspiration_as_read, is_inspiration_read, get_read_inspirations
)

def show_inspirations_page():
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Używamy naszego komponentu nagłówka
    zen_header("Inspiracje")
    
    # Initialize session state for inspirations
    if 'inspiration_view_mode' not in st.session_state:
        st.session_state.inspiration_view_mode = 'overview'
    if 'current_inspiration' not in st.session_state:
        st.session_state.current_inspiration = None
    if 'favorite_inspirations' not in st.session_state:
        st.session_state.favorite_inspirations = []
    
    # Add basic styles
    add_inspirations_styles()
    
    # Main navigation
    show_navigation()
      # Content based on current view mode
    if st.session_state.inspiration_view_mode == 'overview':
        show_overview()
    elif st.session_state.inspiration_view_mode == 'categories':
        show_categories_view()
    elif st.session_state.inspiration_view_mode == 'search':
        show_search_view()
    elif st.session_state.inspiration_view_mode == 'favorites':
        show_favorites_view()
    elif st.session_state.inspiration_view_mode == 'read':
        show_read_view()
    elif st.session_state.inspiration_view_mode == 'detail':
        show_inspiration_detail()

def add_inspirations_styles():
    """Dodaje podstawowe style dla Inspiracji"""
    st.markdown("""
    <style>
    /* Podstawowe style */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Nawigacja */
    .inspirations-nav-bar {
        background: rgba(255,255,255,0.95);
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .inspirations-nav-bar [data-testid="stButton"] button {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
        border: 1px solid #cbd5e1 !important;
        color: #475569 !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
        margin: 0 0.25rem !important;
    }
    
    .inspirations-nav-bar [data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%) !important;
        border-color: #94a3b8 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
      /* Podstawowe hover dla przycisków */
    .stButton button {
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
      /* Style dla kart inspiracji - wyrównanie przycisków */
    .inspiration-card-buttons {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        gap: 0.75rem !important;
        margin-top: 1rem !important;
    }
    
    .inspiration-card-buttons .stButton:first-child button {
        margin-right: auto !important;
        justify-content: flex-start !important;
    }
    
    .inspiration-card-buttons .stButton:last-child button {
        margin-left: auto !important;
        justify-content: flex-end !important;
    }
    
    /* Lepsze wyrównanie przycisków w kartach */
    [data-testid="column"]:nth-child(1) [data-testid="stButton"] button {
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }
    
    [data-testid="column"]:nth-child(2) [data-testid="stButton"] button {
        width: 100% !important;
        text-align: right !important;
        justify-content: flex-end !important;
    }
    
    /* Mobile */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Na mobile przyciski zajmują całą szerokość */
        [data-testid="column"] [data-testid="stButton"] button {
            width: 100% !important;
            text-align: center !important;
            justify-content: center !important;
        }
    }
    
    /* Srebrne karty inspiracji */
    .inspiration-card-silver {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
        border: 1px solid #94a3b8;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .inspiration-card-silver:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15), 0 3px 10px rgba(0, 0, 0, 0.1);
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 50%, #94a3b8 100%);
    }
    
    .inspiration-card-silver::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #64748b, #94a3b8, #cbd5e1);
    }
    
    .inspiration-content {
        position: relative;
        z-index: 1;
    }
    
    .inspiration-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }
    
    .inspiration-title {
        color: #1e293b;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        line-height: 1.3;
    }
    
    .inspiration-description {
        color: #475569;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0 0 1rem 0;
    }
    
    .inspiration-meta {
        display: flex;
        align-items: center;
        gap: 1rem;
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 1rem;
    }
    
    .reading-time {
        background: rgba(100, 116, 139, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-weight: 500;
    }
    
    .tags {
        background: rgba(100, 116, 139, 0.1);
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-weight: 500;
        flex: 1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    @media (max-width: 768px) {
        .inspiration-meta {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
        }
        
        .tags {
            white-space: normal;
            flex: none;
            width: 100%;
        }
    }
    
    /* Karta inspiracji z zintegrowanymi przyciskami */
    .inspiration-card-with-buttons {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e1 100%);
        border: 1px solid #94a3b8;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    
    .inspiration-card-with-buttons:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15), 0 3px 10px rgba(0, 0, 0, 0.1);
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 50%, #94a3b8 100%);
    }
    
    .inspiration-card-with-buttons::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #64748b, #94a3b8, #cbd5e1);
    }
    
    .inspiration-card-with-buttons .inspiration-content {
        padding: 1.5rem;
        flex: 1;
    }
    
    /* Wiersz z przyciskami zintegrowany z kartą */
    .inspiration-button-row {
        display: flex;
        background: rgba(100, 116, 139, 0.08);
        border-top: 1px solid rgba(100, 116, 139, 0.15);
    }
    
    .inspiration-button-wrapper {
        flex: 1;
        position: relative;
    }
    
    .inspiration-button-wrapper:first-child::after {
        content: '';
        position: absolute;
        right: 0;
        top: 10%;
        bottom: 10%;
        width: 1px;
        background: rgba(100, 116, 139, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def show_navigation():
    """Wyświetla nawigację między sekcjami inspiracji"""
    st.markdown('<div class="inspirations-nav-bar">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Przegląd", key="nav_overview"):
            st.session_state.inspiration_view_mode = 'overview'
            st.rerun()
    
    with col2:
        if st.button("📂 Kategorie", key="nav_categories"):
            st.session_state.inspiration_view_mode = 'categories'
            st.rerun()
    
    with col3:
        if st.button("🔍 Szukaj", key="nav_search"):
            st.session_state.inspiration_view_mode = 'search'
            st.rerun()
    
    with col4:
        if st.button("⭐ Ulubione", key="nav_favorites"):
            st.session_state.inspiration_view_mode = 'favorites'
            st.rerun()
    
    with col5:
        if st.button("✅ Przeczytane", key="nav_read"):
            st.session_state.inspiration_view_mode = 'read'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_overview():
    """Strona główna inspiracji - wszystkie artykuły"""
    
    # Wszystkie inspiracje
    st.subheader("📚 Wszystkie Inspiracje")
    all_inspirations = get_all_inspirations()
    
    if all_inspirations:
        st.info(f"📖 Dostępnych jest **{len(all_inspirations)}** inspiracji do przeczytania!")
        display_inspirations_grid(all_inspirations, featured=False)
    else:
        st.info("Brak dostępnych inspiracji")

def show_categories_view():
    """Widok kategorii inspiracji"""
    st.subheader("📂 Przeglądaj po kategoriach")
    
    categories = get_categories()
    
    # Upewnij się, że categories to lista
    if isinstance(categories, dict):
        category_list = list(categories.keys())
    elif isinstance(categories, (list, tuple)):
        category_list = list(categories)
    else:
        category_list = list(categories) if categories else []
    
    # Category selector
    category_options = ["Wszystkie"] + category_list
    selected_category = st.selectbox("Wybierz kategorię:", category_options, key="category_selector")
    
    if selected_category == "Wszystkie":
        inspirations = get_all_inspirations()
    else:
        inspirations = get_inspirations_by_category(selected_category)
    
    if inspirations:
        display_inspirations_grid(inspirations)
    else:
        st.info(f"Brak inspiracji w kategorii: {selected_category}")

def show_search_view():
    """Widok wyszukiwania inspiracji"""
    st.subheader("🔍 Szukaj inspiracji")
    
    # Search input
    search_query = st.text_input("Wpisz frazę do wyszukania:", key="search_input")
    
    if search_query:
        results = search_inspirations(search_query)
        
        if results:
            st.write(f"Znaleziono {len(results)} wyników dla: **{search_query}**")
            display_inspirations_grid(results)
        else:
            st.info(f"Brak wyników dla: {search_query}")
    else:
        st.info("Wprowadź frazę do wyszukania")

def show_favorites_view():
    """Widok ulubionych inspiracji"""
    st.subheader("⭐ Twoje ulubione inspiracje")
    
    favorites = get_favorite_inspirations()
    
    if favorites:
        display_inspirations_grid(favorites)
    else:
        st.info("Nie masz jeszcze ulubionych inspiracji. Dodaj je klikając ⭐ na kartach inspiracji.")

def show_read_view():
    """Widok przeczytanych inspiracji"""
    st.subheader("✅ Przeczytane inspiracje")
    
    read_inspirations = get_read_inspirations()
    
    if read_inspirations:
        st.info(f"📖 Przeczytałeś już **{len(read_inspirations)}** inspiracji!")
        display_inspirations_grid(read_inspirations)
    else:
        st.info("Nie przeczytałeś jeszcze żadnej inspiracji. Rozpocznij czytanie w sekcji Przegląd!")

def display_inspirations_grid(inspirations, featured=False):
    """Wyświetla siatkę inspiracji w kolumnach"""
    
    # Podziel inspiracje na grupy po 2 dla dwóch kolumn
    for i in range(0, len(inspirations), 2):
        col1, col2 = st.columns(2, gap="large")
        
        # Pierwsza karta
        with col1:
            if i < len(inspirations):
                show_single_inspiration_card(inspirations[i], featured, i % 4)
        
        # Druga karta (jeśli istnieje)
        with col2:
            if i + 1 < len(inspirations):
                show_single_inspiration_card(inspirations[i + 1], featured, (i + 1) % 4)
            else:
                # Pusta kolumna dla symetrii
                st.empty()

def show_single_inspiration_card(inspiration, featured=False, card_index=0):
    """Wyświetla pojedynczą kartę inspiracji z zintegrowanymi przyciskami"""
    
    # Przygotuj dane
    reading_time = inspiration.get('reading_time', 5)
    is_fav = is_inspiration_favorite(inspiration['id'])
    is_read = is_inspiration_read(inspiration['id'])
    fav_icon = "⭐" if is_fav else "☆"
    
    # Przygotuj tagi
    tags = inspiration.get('tags', [])
    if tags and isinstance(tags, (list, tuple)):
        # Pokaż maksymalnie 3 tagi
        display_tags = tags[:3] if len(tags) > 3 else tags
        tags_text = " • ".join(display_tags)
    else:
        tags_text = ""
    
    # Sprawdź czy artykuł został przeczytany i dostosuj tekst przycisku
    if is_read:
        button_text = "✅ PRZECZYTANE"
        button_class = "read-button"
    else:
        button_text = "📖 CZYTAJ"
        button_class = "unread-button"
    
    # Karta inspiracji z przyciskami zintegrowanymi
    with st.container():
        # Główna karta
        st.markdown(f"""
        <div class="inspiration-card-integrated">
            <div class="inspiration-content">
                <div class="inspiration-icon">💡</div>
                <h3 class="inspiration-title">{inspiration['title']}</h3>
                <p class="inspiration-description">{inspiration['description']}</p>
                <div class="inspiration-meta">
                    <span class="reading-time">📖 {reading_time} min</span>
                    {f'<span class="tags">🏷️ {tags_text}</span>' if tags_text else ''}
                </div>
            </div>
            <div class="inspiration-buttons">
        """, unsafe_allow_html=True)
        
        # Przyciski Streamlit wewnątrz karty
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"{fav_icon} Ulubione", key=f"fav_{inspiration['id']}_{card_index}", use_container_width=True):
                toggle_inspiration_favorite(inspiration['id'])
                st.rerun()
        with col2:
            if st.button(button_text, key=f"read_{inspiration['id']}_{card_index}", use_container_width=True):
                st.session_state.current_inspiration = inspiration['id']
                st.session_state.inspiration_view_mode = 'detail'
                increment_inspiration_views(inspiration['id'])
                st.rerun()
        
        # Zamknięcie karty
        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_inspiration_detail():
    """Wyświetla szczegóły inspiracji"""
    inspiration_id = st.session_state.current_inspiration
    inspiration = get_inspiration_by_id(inspiration_id)
    
    if not inspiration:
        st.error("Nie znaleziono inspiracji")
        if st.button("← Powrót do przeglądu"):
            st.session_state.inspiration_view_mode = 'overview'
            st.rerun()
        return
    
    # Back button
    if st.button("← Powrót", key="back_to_overview"):
        st.session_state.inspiration_view_mode = 'overview'
        st.rerun()
        
    # Reading time and tags info
    reading_time = inspiration.get('reading_time', 5)
    st.write(f"📖 **Czas czytania:** {reading_time} min")
    
    # Tags
    tags = inspiration.get('tags', [])
    if tags and isinstance(tags, (list, tuple)):
        formatted_tags = [f"*{tag}*" for tag in tags]
        st.write("**Tagi:** " + " • ".join(formatted_tags))
      # Content
    st.markdown("---")
    content = load_inspiration_content(inspiration['content_path'])
    if content:
        st.markdown(content)
        # Oznacz inspirację jako przeczytaną gdy treść zostanie wyświetlona
        mark_inspiration_as_read(inspiration['id'])
    else:
        st.info("Zawartość inspiracji będzie dostępna wkrótce...")
    
    # Favorite button
    is_fav = is_inspiration_favorite(inspiration['id'])
    fav_text = "Usuń z ulubionych ⭐" if is_fav else "Dodaj do ulubionych ☆"
    
    if st.button(fav_text, key="detail_favorite", type="secondary"):
        if is_fav:
            unmark_inspiration_as_favorite(inspiration['id'])
        else:
            mark_inspiration_as_favorite(inspiration['id'])
        st.rerun()
    
    # Random inspiration suggestion
    st.markdown("---")
    if st.button("🎲 Losowa inspiracja", key="random_inspiration"):
        random_insp = get_random_inspiration()
        if random_insp:
            st.session_state.current_inspiration = random_insp['id']
            increment_inspiration_views(random_insp['id'])
            st.rerun()
