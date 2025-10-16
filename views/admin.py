import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go
import math
from datetime import datetime, timedelta
import time
import json
from data.users import load_user_data, save_user_data
from data.lessons import load_lessons
from utils.scroll_utils import scroll_to_top
from data.neuroleader_test_questions import NEUROLEADER_TYPES
from config.settings import XP_LEVELS
from utils.material3_components import apply_material3_theme
from utils.components import zen_header, zen_button, notification, data_chart, stat_card
from utils.layout import get_device_type, responsive_grid, toggle_device_view

def check_admin_auth():
    """Sprawdza uwierzytelnienie administratora"""

    # Oryginalna kontrola uprawnień (zakomentowana na czas testów)
    if not st.session_state.get('logged_in', False):
        st.error("Musisz być zalogowany, aby uzyskać dostęp do panelu administratora.")
        return False
       
    admin_users = ["admin", "zenmaster", "Anna", "Max"]  # Dodaj swój login
    if st.session_state.get('username') not in admin_users:
        st.error("Nie masz uprawnień do przeglądania panelu administratora.")
        return False
       
    return True

def get_user_activity_data():
    """Pobiera i przetwarza dane o aktywności użytkowników"""
    users_data = load_user_data()
    
    # Przygotuj dane do analizy
    activity_data = []
    for username, data in users_data.items():        activity_data.append({
            'username': username,
            'xp': data.get('xp', 0),
            'level': data.get('level', 1),
            'completed_lessons': len(data.get('completed_lessons', [])),
            'neuroleader_type': data.get('neuroleader_type', 'Nieznany'),
            'registration_date': data.get('joined_date', 'Nieznana'),  # Poprawione: używamy joined_date
            'last_login': data.get('last_login') or 'Nigdy',           # Lepsze formatowanie dla brakujących danych
            'test_taken': data.get('test_taken', False),
            'completed_missions': len(data.get('completed_missions', [])),
            'streak': data.get('streak', 0)
        })
    
    return pd.DataFrame(activity_data)

def get_lessons_stats():
    """Pobiera i analizuje statystyki lekcji"""
    users_data = load_user_data()
    lessons = load_lessons()
    
    # Inicjalizuj liczniki ukończeń dla każdej lekcji
    completion_count = {lesson_id: 0 for lesson_id in lessons.keys()}
    
    # Zlicz ukończenia lekcji
    for username, data in users_data.items():
        completed_lessons = data.get('completed_lessons', [])
        for lesson_id in completed_lessons:
            if lesson_id in completion_count:
                completion_count[lesson_id] += 1
    
    # Utwórz DataFrame ze statystykami lekcji
    lessons_stats = []
    for lesson_id, lesson in lessons.items():
        lessons_stats.append({
            'lesson_id': lesson_id,
            'title': lesson.get('title', 'Brak tytułu'),
            'category': lesson.get('tag', 'Brak kategorii'),
            'difficulty': lesson.get('difficulty', 'intermediate'),
            'completions': completion_count.get(lesson_id, 0),
            'completion_rate': round(completion_count.get(lesson_id, 0) / len(users_data) * 100, 2) if users_data else 0
        })
    
    return pd.DataFrame(lessons_stats)

def get_neuroleader_type_distribution():
    """Analizuje rozkład typów neuroliderów wśród użytkowników"""
    users_data = load_user_data()
    
    # Zlicz wystąpienia każdego typu neurolidera
    neuroleader_counts = {}
    for _, data in users_data.items():
        neuroleader_type = data.get('neuroleader_type', 'Nieznany')
        neuroleader_counts[neuroleader_type] = neuroleader_counts.get(neuroleader_type, 0) + 1
    
    # Utwórz DataFrame dla wizualizacji
    neuroleader_distribution = []
    for neuroleader_type, count in neuroleader_counts.items():
        neuroleader_distribution.append({
            'neuroleader_type': neuroleader_type,
            'count': count,
            'percentage': round(count / len(users_data) * 100, 2) if users_data else 0
        })
    
    return pd.DataFrame(neuroleader_distribution)

def plot_user_activity_over_time():
    """Generuje wykres aktywności użytkowników w czasie na podstawie rzeczywistych danych"""
    users_data = load_user_data()
    
    # Pobierz rzeczywiste daty z ostatnich 30 dni
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    
    # Inicjalizuj liczniki dla rejestracji i logowań
    registrations = {date: 0 for date in dates}
    logins = {date: 0 for date in dates}
    
    # Zlicz rzeczywistą aktywność na podstawie danych użytkowników
    for username, user_data in users_data.items():
        # 1. Zlicz rejestracje w ostatnich 30 dniach
        joined_date = user_data.get('joined_date')
        if joined_date and joined_date in registrations:
            registrations[joined_date] += 1
        
        # 2. Zlicz ostatnie logowania w ostatnich 30 dniach
        last_login = user_data.get('last_login')
        if last_login:
            # Wyciągnij datę z datetime string (format: "2025-06-26 14:30:15")
            try:
                login_date = last_login.split(' ')[0]  # Weź tylko część z datą
                if login_date in logins:
                    logins[login_date] += 1
            except (AttributeError, IndexError, ValueError):
                # Ignoruj nieprawidłowe formaty dat
                pass
    
    # Odwróć daty, aby najnowsze były na końcu
    dates.reverse()
    
    # Utwórz DataFrame z oddzielnymi kolumnami dla rejestracji i logowań
    activity_df = pd.DataFrame({
        'data': dates,
        'rejestracje': [registrations[date] for date in dates],
        'logowania': [logins[date] for date in dates],
        'łącznie': [registrations[date] + logins[date] for date in dates]
    })
    
    return activity_df

def show_admin_dashboard():
    """Wyświetla panel administratora"""
    
    # Zastosuj style Material 3
    apply_material3_theme()
    
    # Opcja wyboru urządzenia w trybie deweloperskim
    if st.session_state.get('dev_mode', False):
        toggle_device_view()
    
    # Pobierz aktualny typ urządzenia
    device_type = get_device_type()
    
    # Przewiń na górę strony
    scroll_to_top()
    
    # Sprawdź uwierzytelnienie admina
    if not check_admin_auth():
        # Jeśli użytkownik nie jest administratorem, wyświetl przycisk powrotu
        if zen_button("Powrót do strony głównej"):
            st.session_state.page = 'dashboard'
            st.rerun()
        return
    
    # Nagłówek panelu administratora
    zen_header("🛡️ Panel Administratora")
    
    # Dodaj informację o ostatnim odświeżeniu
    st.markdown(f"**Ostatnie odświeżenie:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Przycisk do odświeżania danych
    if zen_button("🔄 Odśwież dane"):
        st.rerun()
    
    # Zakładki główne panelu administratora
    admin_tabs = st.tabs(["Przegląd", "Użytkownicy", "Lekcje", "Dostępność", "Testy", "Zarządzanie"])
    
    # 1. Zakładka Przegląd
    with admin_tabs[0]:
        st.subheader("Przegląd statystyk platformy")
        
        # Pobierz dane
        users_data = load_user_data()
        user_df = get_user_activity_data()
        
        # Podstawowe statystyki
        total_users = len(users_data)
        total_lessons_completed = user_df['completed_lessons'].sum()
        avg_xp = int(user_df['xp'].mean()) if not user_df.empty else 0
        tests_taken = user_df['test_taken'].sum()
        
        # Wyświetl statystyki w responsywnym układzie
        stats_cols = responsive_grid(4, 2, 1)
        
        with stats_cols[0]:
            stat_card("Liczba użytkowników", total_users, "👥")
        
        with stats_cols[1]:
            stat_card("Ukończone lekcje", int(total_lessons_completed), "📚")
        
        with stats_cols[2]:
            stat_card("Średnie XP", avg_xp, "⭐")
        
        with stats_cols[3]:
            stat_card("Wykonane testy", int(tests_taken), "📊")
          # Wykresy aktywności
        st.subheader("Aktywność użytkowników")
        
        activity_df = plot_user_activity_over_time()
        
        # Wykres aktywności użytkowników
        chart = alt.Chart(activity_df).mark_line(point=True).encode(
            x=alt.X('data:T', title='Data'),
            y=alt.Y('łącznie:Q', title='Liczba aktywności (rejestracje + logowania)'),
            tooltip=['data', 'rejestracje', 'logowania', 'łącznie']
        ).properties(
            width='container',
            height=350,
            title='Aktywność użytkowników: rejestracje i logowania (ostatnie 30 dni)'
        )
        
        st.altair_chart(chart)
        
        # Rozkład typów neuroliderów
        st.subheader("Rozkład typów neuroliderów")
        
        neuroleader_df = get_neuroleader_type_distribution()
        
        if not neuroleader_df.empty:
            # Wykres kołowy typów neuroleaderów z ulepszoną czytelnością
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Przygotuj dane
            counts = neuroleader_df['count'].tolist()
            labels = neuroleader_df['neuroleader_type'].tolist()
            total = sum(counts)
            
            # Funkcja do wyświetlania procentów tylko dla większych wartości
            def autopct_format(pct):
                return f'{pct:.1f}%' if pct >= 3 else ''
            
            # Stwórz wykres kołowy z automatycznym pozycjonowaniem etykiet
            pie_result = ax.pie(
                counts, 
                labels=labels,
                autopct=autopct_format,
                startangle=90,
                shadow=False,
                pctdistance=0.85,  # Odległość etykiet z procentami od środka
                labeldistance=1.1,  # Odległość nazw od środka
                explode=[0.05 if count/total < 0.05 else 0 for count in counts],  # Wysuń małe segmenty
                textprops={'fontsize': 10}
            )
            
            # Rozpakuj wyniki (może być 2 lub 3 elementy)
            if len(pie_result) == 3:
                wedges, texts, autotexts = pie_result
                # Poprawa czytelności etykiet procentowych
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
            else:
                wedges, texts = pie_result
            
            # Dodaj legendę z dokładnymi liczbami
            legend_labels = [f'{label}: {count} ({count/total*100:.1f}%)' 
                           for label, count in zip(labels, counts)]
            ax.legend(wedges, legend_labels, title="Typy neuroleaderów", 
                     loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            
            ax.axis('equal')  # Zapewnia okrągły kształt
            plt.title('Rozkład typów neuroleaderów', fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            
            st.pyplot(fig)
        else:
            st.info("Brak danych o typach neuroleaderów.")
    
    # 2. Zakładka Użytkownicy
    with admin_tabs[1]:
        st.subheader("Szczegóły użytkowników")
        
        # Pobierz dane
        user_df = get_user_activity_data()
        
        # Filtrowanie użytkowników
        filter_cols = st.columns(3)
        with filter_cols[0]:
            min_xp = st.number_input("Min XP", min_value=0, value=0)
        with filter_cols[1]:
            neuroleader_filter = st.selectbox("Filtruj wg typu neuroleader", 
                                       options=["Wszystkie"] + list(user_df['neuroleader_type'].unique()))
        with filter_cols[2]:
            sort_by = st.selectbox("Sortuj wg", 
                                   options=["xp", "level", "completed_lessons", "username"])
        
        # Zastosuj filtry
        filtered_df = user_df
        if min_xp > 0:
            filtered_df = filtered_df[filtered_df['xp'] >= min_xp]
        
        if neuroleader_filter != "Wszystkie":
            filtered_df = filtered_df[filtered_df['neuroleader_type'] == neuroleader_filter]
        
        # Sortuj dane
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=False)
          # Wyświetl tabelę użytkowników
        st.dataframe(
            filtered_df,
            column_config={
                "username": "Nazwa użytkownika",
                "xp": "XP",
                "level": "Poziom",
                "completed_lessons": "Ukończone lekcje",
                "neuroleader_type": "Typ neuroleader",
                "registration_date": "Data rejestracji",
                "last_login": "Ostatnie logowanie",
                "test_taken": "Test wykonany",
                "streak": "Seria dni"
            },
            width='stretch'
        )
        
        # Dodaj opcję eksportu danych
        if zen_button("Eksportuj dane użytkowników do CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Pobierz CSV",
                data=csv,
                file_name="users_data.csv",
                mime="text/csv"
            )
    
    # 3. Zakładka Lekcje
    with admin_tabs[2]:
        st.subheader("Statystyki lekcji")
        
        # Pobierz dane lekcji
        lessons_df = get_lessons_stats()
        
        # Wyświetl tabelę statystyk lekcji
        st.dataframe(
            lessons_df,
            column_config={
                "lesson_id": "ID lekcji",
                "title": "Tytuł",
                "category": "Kategoria",
                "difficulty": st.column_config.SelectboxColumn(
                    "Poziom trudności", 
                    options=["beginner", "intermediate", "advanced"],
                    required=True
                ),
                "completions": "Liczba ukończeń",
                "completion_rate": st.column_config.ProgressColumn(
                    "Wskaźnik ukończenia (%)",
                    min_value=0,
                    max_value=100,
                    format="%{value:.2f}"
                )
            },
            width='stretch'
        )
        
        # Wykres popularności lekcji (top 10)
        st.subheader("Najpopularniejsze lekcje")
        
        top_lessons = lessons_df.sort_values('completions', ascending=False).head(10)
        
        if not top_lessons.empty:
            chart = alt.Chart(top_lessons).mark_bar().encode(
                x=alt.X('completions:Q', title='Liczba ukończeń'),
                y=alt.Y('title:N', title='Lekcja', sort='-x'),
                color=alt.Color('category:N', title='Kategoria'),
                tooltip=['title', 'category', 'completions', 'completion_rate']
            ).properties(
                width='container',
                height=400,
                title='Top 10 najpopularniejszych lekcji'
            )
            
            st.altair_chart(chart)
        else:
            st.info("Brak danych o ukończonych lekcjach.")
    
    # 4. Zakładka Dostępność lekcji
    with admin_tabs[3]:
        manage_lesson_access()
    
    # 5. Zakładka Testy
    with admin_tabs[4]:
        st.subheader("Wyniki testów Neurolidera")
        
        # Pobierz dane o użytkownikach
        users_data = load_user_data()
        
        # Zbierz dane o wynikach testów
        test_results = []
        for username, data in users_data.items():
            if data.get('test_scores'):
                for neuroleader_type, score in data.get('test_scores', {}).items():
                    test_results.append({
                        'username': username,
                        'neuroleader_type': neuroleader_type,
                        'score': score
                    })
        
        test_df = pd.DataFrame(test_results)
        
        if not test_df.empty:
            # Średnie wyniki dla każdego typu neuroleader
            st.subheader("Średnie wyniki dla typów neuroleaderów")
            
            avg_scores = test_df.groupby('neuroleader_type')['score'].mean().reset_index()
            avg_scores['score'] = avg_scores['score'].round(2)
            
            chart = alt.Chart(avg_scores).mark_bar().encode(
                x=alt.X('neuroleader_type:N', title='Typ neuroleader'),
                y=alt.Y('score:Q', title='Średni wynik'),
                color=alt.Color('neuroleader_type:N', title='Typ neuroleader'),
                tooltip=['neuroleader_type', 'score']
            ).properties(
                width='container',
                height=350,
                title='Średnie wyniki testów wg typu neuroleader'
            )
            
            st.altair_chart(chart)
            
            # Tabela z wynikami testów
            st.subheader("Szczegółowe wyniki testów")
            st.dataframe(
                test_df,
                column_config={
                    "username": "Nazwa użytkownika",
                    "neuroleader_type": "Typ neuroleader",
                    "score": "Wynik"
                },
                width='stretch'
            )
        else:
            st.info("Brak danych o wynikach testów.")
        
        # NOWA SEKCJA: Wyniki testów Kolba Learning Styles
        st.markdown("---")
        st.subheader("🎯 Wyniki testów Stylów Uczenia się Kolba (Learning Styles)")
        
        # Pobierz dane o użytkownikach z wynikami testów Kolba
        kolb_results = []
        for username, data in users_data.items():
            if data.get('kolb_test'):
                kolb_data = data['kolb_test']
                kolb_results.append({
                    'username': username,
                    'dominant_style': kolb_data.get('dominant_style', 'Nieznany'),
                    'AC-CE': kolb_data.get('dimensions', {}).get('AC-CE', 0),
                    'AE-RO': kolb_data.get('dimensions', {}).get('AE-RO', 0),
                    'flexibility': kolb_data.get('flexibility', 0),
                    'completed_date': kolb_data.get('completed_date', 'Nieznana'),
                    'CE': kolb_data.get('scores', {}).get('CE', 0),
                    'RO': kolb_data.get('scores', {}).get('RO', 0),
                    'AC': kolb_data.get('scores', {}).get('AC', 0),
                    'AE': kolb_data.get('scores', {}).get('AE', 0)
                })
        
        if kolb_results:
            kolb_df = pd.DataFrame(kolb_results)
            
            # Statystyki podstawowe
            st.markdown("#### 📊 Statystyki podstawowe")
            
            stats_cols = st.columns(4)
            with stats_cols[0]:
                st.metric("Liczba użytkowników", len(kolb_df))
            with stats_cols[1]:
                st.metric("Średnia elastyczność", f"{kolb_df['flexibility'].mean():.1f}%")
            with stats_cols[2]:
                most_common_style = kolb_df['dominant_style'].mode()[0] if not kolb_df.empty else "Brak"
                st.metric("Najczęstszy styl", most_common_style.split('(')[0].strip())
            with stats_cols[3]:
                st.metric("Najwyższa elastyczność", f"{kolb_df['flexibility'].max():.1f}%")
            
            # Rozkład stylów uczenia się
            st.markdown("---")
            st.markdown("#### 📈 Rozkład stylów uczenia się")
            
            style_counts = kolb_df['dominant_style'].value_counts().reset_index()
            style_counts.columns = ['Styl', 'Liczba']
            
            chart = alt.Chart(style_counts).mark_bar().encode(
                x=alt.X('Liczba:Q', title='Liczba użytkowników'),
                y=alt.Y('Styl:N', title='Styl uczenia się', sort='-x'),
                color=alt.Color('Styl:N', legend=None),
                tooltip=['Styl', 'Liczba']
            ).properties(
                width='container',
                height=300,
                title='Rozkład stylów uczenia się wśród użytkowników'
            )
            
            st.altair_chart(chart, use_container_width=True)
            
            # GŁÓWNA WIZUALIZACJA: Siatka wszystkich użytkowników
            st.markdown("---")
            st.markdown("#### 🗺️ Siatka Stylów Uczenia się - Wszyscy Użytkownicy")
            st.markdown("*Pozycje wszystkich użytkowników w matrycy ELT z etykietami nazw*")
            
            # Utwórz wykres siatki Kolba z wszystkimi użytkownikami
            fig_all = go.Figure()
            
            # Dodaj tło ćwiartek z nazwami stylów
            quadrant_info = {
                'Diverging': {'x': [-12, 0], 'y': [-12, 0], 'color': 'rgba(231, 76, 60, 0.15)', 'label_x': -6, 'label_y': -6},
                'Assimilating': {'x': [-12, 0], 'y': [0, 12], 'color': 'rgba(155, 89, 182, 0.15)', 'label_x': -6, 'label_y': 6},
                'Converging': {'x': [0, 12], 'y': [0, 12], 'color': 'rgba(52, 152, 219, 0.15)', 'label_x': 6, 'label_y': 6},
                'Accommodating': {'x': [0, 12], 'y': [-12, 0], 'color': 'rgba(46, 204, 113, 0.15)', 'label_x': 6, 'label_y': -6}
            }
            
            # Rysuj prostokąty ćwiartek
            for style_name, info in quadrant_info.items():
                fig_all.add_shape(
                    type="rect",
                    x0=info['x'][0], x1=info['x'][1],
                    y0=info['y'][0], y1=info['y'][1],
                    fillcolor=info['color'],
                    line=dict(width=0)
                )
                
                # Dodaj etykiety stylów
                fig_all.add_annotation(
                    x=info['label_x'], y=info['label_y'],
                    text=f"<b>{style_name}</b>",
                    showarrow=False,
                    font=dict(size=14, color='rgba(0,0,0,0.5)', family='Arial Black'),
                    xanchor='center',
                    yanchor='middle'
                )
            
            # Strefa Zrównoważonego Uczenia się (centralna)
            balanced_zone_radius = 4
            theta = [i for i in range(0, 361, 10)]
            balanced_x = [balanced_zone_radius * math.cos(math.radians(t)) for t in theta]
            balanced_y = [balanced_zone_radius * math.sin(math.radians(t)) for t in theta]
            
            fig_all.add_trace(go.Scatter(
                x=balanced_x, y=balanced_y,
                fill='toself',
                fillcolor='rgba(255, 193, 7, 0.2)',
                line=dict(color='rgba(255, 193, 7, 0.6)', width=2, dash='dash'),
                name='Strefa Zrównoważonego<br>Uczenia się',
                hoverinfo='name',
                showlegend=True
            ))
            
            # Osie
            fig_all.add_shape(type="line", x0=-12, x1=12, y0=0, y1=0, 
                              line=dict(color="rgba(0,0,0,0.4)", width=2))
            fig_all.add_shape(type="line", x0=0, x1=0, y0=-12, y1=12, 
                              line=dict(color="rgba(0,0,0,0.4)", width=2))
            
            # Mapowanie kolorów dla stylów
            style_colors = {
                'Diverging (Dywergent)': '#E74C3C',      # Czerwony
                'Assimilating (Asymilator)': '#9B59B6',  # Fioletowy
                'Converging (Konwergent)': '#3498DB',    # Niebieski
                'Accommodating (Akomodator)': '#2ECC71'  # Zielony
            }
            
            # Dodaj punkty użytkowników pogrupowane wg stylu
            for style in kolb_df['dominant_style'].unique():
                style_data = kolb_df[kolb_df['dominant_style'] == style]
                
                # Przygotuj tekst dla hover i etykiety
                hover_texts = []
                for _, row in style_data.iterrows():
                    hover_text = (
                        f"<b>{row['username']}</b><br>"
                        f"Styl: {row['dominant_style']}<br>"
                        f"AE-RO: {row['AE-RO']:+d}<br>"
                        f"AC-CE: {row['AC-CE']:+d}<br>"
                        f"Elastyczność: {row['flexibility']:.1f}%<br>"
                        f"Data: {row['completed_date']}"
                    )
                    hover_texts.append(hover_text)
                
                fig_all.add_trace(go.Scatter(
                    x=style_data['AE-RO'],
                    y=style_data['AC-CE'],
                    mode='markers+text',
                    marker=dict(
                        size=15,
                        color=style_colors.get(style, '#95A5A6'),
                        line=dict(color='white', width=2),
                        symbol='circle'
                    ),
                    text=style_data['username'],
                    textposition='top center',
                    textfont=dict(size=10, color='#2C3E50', family='Arial Black'),
                    name=style.split('(')[0].strip(),  # Skrócona nazwa do legendy
                    hovertemplate='%{customdata}<extra></extra>',
                    customdata=hover_texts
                ))
            
            # Etykiety osi
            fig_all.add_annotation(x=12.5, y=0, text="<b>AE</b><br>(Doing)", showarrow=False, 
                                   font=dict(size=11, color='#2ECC71'), xanchor='left')
            fig_all.add_annotation(x=-12.5, y=0, text="<b>RO</b><br>(Watching)", showarrow=False, 
                                   font=dict(size=11, color='#4A90E2'), xanchor='right')
            fig_all.add_annotation(x=0, y=12.5, text="<b>AC</b><br>(Thinking)", showarrow=False, 
                                   font=dict(size=11, color='#9B59B6'), yanchor='bottom')
            fig_all.add_annotation(x=0, y=-12.5, text="<b>CE</b><br>(Feeling)", showarrow=False, 
                                   font=dict(size=11, color='#E74C3C'), yanchor='top')
            
            fig_all.update_layout(
                title=dict(
                    text=f'Mapa Stylów Uczenia się - {len(kolb_df)} użytkowników',
                    font=dict(size=18, color='#333', family='Arial Black'),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title='<b>Oś Przetwarzania (AE-RO)</b>',
                    range=[-14, 14],
                    zeroline=False,
                    gridcolor='rgba(0,0,0,0.1)',
                    tickfont=dict(size=10)
                ),
                yaxis=dict(
                    title='<b>Oś Postrzegania (AC-CE)</b>',
                    range=[-14, 14],
                    zeroline=False,
                    gridcolor='rgba(0,0,0,0.1)',
                    tickfont=dict(size=10),
                    scaleanchor='x',
                    scaleratio=1
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=700,
                margin=dict(t=80, b=80, l=80, r=80),
                showlegend=True,
                legend=dict(
                    title="Style uczenia się:",
                    x=1.02,
                    y=1,
                    xanchor='left',
                    yanchor='top',
                    bgcolor='rgba(255,255,255,0.9)',
                    bordercolor='rgba(0,0,0,0.2)',
                    borderwidth=1
                )
            )
            
            st.plotly_chart(fig_all, use_container_width=True)
            
            # Tabela szczegółowa
            st.markdown("---")
            st.markdown("#### 📋 Szczegółowe wyniki użytkowników")
            
            # Formatuj DataFrame do wyświetlenia
            display_df = kolb_df[['username', 'dominant_style', 'CE', 'RO', 'AC', 'AE', 
                                   'AC-CE', 'AE-RO', 'flexibility', 'completed_date']]
            
            st.dataframe(
                display_df,
                column_config={
                    "username": "Użytkownik",
                    "dominant_style": "Dominujący styl",
                    "CE": st.column_config.NumberColumn("CE (Feeling)", format="%d/12"),
                    "RO": st.column_config.NumberColumn("RO (Watching)", format="%d/12"),
                    "AC": st.column_config.NumberColumn("AC (Thinking)", format="%d/12"),
                    "AE": st.column_config.NumberColumn("AE (Doing)", format="%d/12"),
                    "AC-CE": st.column_config.NumberColumn("AC-CE", format="%+d"),
                    "AE-RO": st.column_config.NumberColumn("AE-RO", format="%+d"),
                    "flexibility": st.column_config.ProgressColumn(
                        "Elastyczność (%)",
                        min_value=0,
                        max_value=100,
                        format="%.1f%%"
                    ),
                    "completed_date": "Data ukończenia"
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Opcja eksportu
            if zen_button("📥 Eksportuj wyniki testów Kolba do CSV"):
                csv = display_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="⬇️ Pobierz CSV",
                    data=csv,
                    file_name=f"kolb_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("Brak użytkowników, którzy ukończyli test stylów uczenia się Kolba.")
    
    # 6. Zakładka Zarządzanie
    with admin_tabs[5]:
        st.subheader("Zarządzanie użytkownikami")
        
        # Pobierz dane
        users_data = load_user_data()
        usernames = list(users_data.keys())
        
        # Wybór użytkownika
        selected_user = st.selectbox("Wybierz użytkownika", options=usernames)
        
        if selected_user:
            user_data = users_data.get(selected_user, {})
            
            # Wyświetl szczegóły użytkownika
            st.json(user_data)
            
            # Akcje zarządzania
            action_cols = st.columns(3)
            
            with action_cols[0]:
                if zen_button("🔄 Reset postępu XP", key="reset_xp"):
                    if st.session_state.get('confirm_reset_xp', False):
                        # Wykonaj reset XP
                        users_data[selected_user]['xp'] = 0
                        users_data[selected_user]['level'] = 1
                        save_user_data(users_data)
                        st.session_state.confirm_reset_xp = False
                        notification("Zresetowano XP użytkownika.", type="success")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.session_state.confirm_reset_xp = True
                        st.warning("Czy na pewno chcesz zresetować XP? Kliknij ponownie, aby potwierdzić.")
            
            with action_cols[1]:
                if zen_button("📚 Reset ukończonych lekcji", key="reset_lessons"):
                    if st.session_state.get('confirm_reset_lessons', False):
                        # Wykonaj reset ukończonych lekcji
                        users_data[selected_user]['completed_lessons'] = []
                        save_user_data(users_data)
                        st.session_state.confirm_reset_lessons = False
                        notification("Zresetowano ukończone lekcje użytkownika.", type="success")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.session_state.confirm_reset_lessons = True
                        st.warning("Czy na pewno chcesz zresetować ukończone lekcje? Kliknij ponownie, aby potwierdzić.")
            
            with action_cols[2]:
                if zen_button("🗑️ Usuń użytkownika", key="delete_user"):
                    if st.session_state.get('confirm_delete', False):
                        # Wykonaj usunięcie użytkownika
                        users_data.pop(selected_user, None)
                        save_user_data(users_data)
                        st.session_state.confirm_delete = False
                        notification("Usunięto użytkownika.", type="success")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.session_state.confirm_delete = True
                        st.warning("Czy na pewno chcesz usunąć tego użytkownika? Ta operacja jest nieodwracalna! Kliknij ponownie, aby potwierdzić.")
            
            # Dodatkowe ustawienia użytkownika
            st.subheader("Edycja danych użytkownika")
            
            edit_cols = st.columns(2)
            with edit_cols[0]:
                new_xp = st.number_input("Punkty XP", min_value=0, value=user_data.get('xp', 0))
            
            with edit_cols[1]:
                new_level = st.number_input("Poziom", min_value=1, value=user_data.get('level', 1))
            
            # Admin status
            is_admin = st.checkbox("Administrator", value=selected_user in ["admin", "zenmaster"])
            
            # Zapisz zmiany
            if zen_button("Zapisz zmiany"):
                users_data[selected_user]['xp'] = new_xp
                users_data[selected_user]['level'] = new_level
                
                # Zapisz dane
                save_user_data(users_data)
                notification("Zapisano zmiany.", type="success")
                time.sleep(1)
                st.rerun()
        
        # Przycisk eksportu kopii zapasowej
        st.subheader("Kopia zapasowa")
        if zen_button("💾 Eksportuj kopię zapasową danych"):
            # Konwertuj dane do formatu JSON
            users_json = json.dumps(users_data, indent=4)
            
            # Oferuj plik do pobrania
            st.download_button(
                label="Pobierz kopię zapasową (JSON)",
                data=users_json,
                file_name=f"neuroleader_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def manage_lesson_access():
    """Panel zarządzania dostępnością lekcji dla użytkowników"""
    st.subheader("🔐 Zarządzanie dostępnością lekcji")
    
    users_data = load_user_data()
    lessons = load_lessons()
    
    if not users_data:
        st.warning("Brak danych użytkowników.")
        return
    
    if not lessons:
        st.warning("Brak danych lekcji.")
        return
    
    # Wybór użytkownika
    usernames = list(users_data.keys())
    selected_user = st.selectbox("Wybierz użytkownika:", usernames)
    
    if selected_user:
        st.write(f"**Zarządzanie dostępem dla: {selected_user}**")
        
        # Sprawdź czy użytkownik ma już dane o dostępności lekcji
        if 'lesson_access' not in users_data[selected_user]:
            users_data[selected_user]['lesson_access'] = {}
        
        lesson_access = users_data[selected_user]['lesson_access']
        
        # Wyświetl wszystkie lekcje z checkboxami
        st.write("**Dostępne lekcje:**")
        
        changes_made = False
        
        # Utwórz kolumny dla lepszego układu
        col1, col2 = st.columns([3, 1])
        
        for lesson_id, lesson_data in lessons.items():
            lesson_title = lesson_data.get('title', lesson_id)
            
            with col1:
                st.write(f"📚 {lesson_title}")
            
            with col2:
                # Sprawdź aktualny status (domyślnie True jeśli nie ustawiono)
                current_status = lesson_access.get(lesson_id, True)
                
                # Checkbox do zmiany statusu
                new_status = st.checkbox(
                    "Dostępna", 
                    value=current_status,
                    key=f"lesson_access_{selected_user}_{lesson_id}"
                )
                
                # Sprawdź czy nastąpiła zmiana
                if new_status != current_status:
                    lesson_access[lesson_id] = new_status
                    changes_made = True
        
        # Przycisk zapisywania zmian
        if changes_made:
            st.warning("⚠️ Masz niezapisane zmiany!")
        
        if st.button("💾 Zapisz zmiany dostępności", type="primary"):
            try:
                users_data[selected_user]['lesson_access'] = lesson_access
                save_user_data(users_data)
                st.success(f"✅ Zapisano zmiany dostępności lekcji dla użytkownika {selected_user}")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Błąd podczas zapisywania: {str(e)}")
        
        # Pokaż aktualny status dostępności
        st.write("**Aktualny status dostępności:**")
        accessible_lessons = [lesson_id for lesson_id, access in lesson_access.items() if access]
        blocked_lessons = [lesson_id for lesson_id, access in lesson_access.items() if not access]
        
        if accessible_lessons:
            st.write("✅ **Dostępne lekcje:**")
            for lesson_id in accessible_lessons:
                lesson_title = lessons.get(lesson_id, {}).get('title', lesson_id)
                st.write(f"  • {lesson_title}")
        
        if blocked_lessons:
            st.write("🔒 **Zablokowane lekcje:**")
            for lesson_id in blocked_lessons:
                lesson_title = lessons.get(lesson_id, {}).get('title', lesson_id)
                st.write(f"  • {lesson_title}")
        
        # Szybkie akcje
        st.write("**Szybkie akcje:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔓 Odblokuj wszystkie lekcje"):
                for lesson_id in lessons.keys():
                    lesson_access[lesson_id] = True
                users_data[selected_user]['lesson_access'] = lesson_access
                save_user_data(users_data)
                st.success("Odblokowano wszystkie lekcje!")
                time.sleep(1)
                st.rerun()
        
        with col2:
            if st.button("🔒 Zablokuj wszystkie lekcje"):
                for lesson_id in lessons.keys():
                    lesson_access[lesson_id] = False
                users_data[selected_user]['lesson_access'] = lesson_access
                save_user_data(users_data)
                st.success("Zablokowano wszystkie lekcje!")
                time.sleep(1)
                st.rerun()

def get_lesson_access_status(username, lesson_id):
    """Sprawdź czy użytkownik ma dostęp do lekcji"""
    users_data = load_user_data()
    
    if username not in users_data:
        return True  # Domyślnie dostępne dla nowych użytkowników
    
    lesson_access = users_data[username].get('lesson_access', {})
    return lesson_access.get(lesson_id, True)  # Domyślnie dostępne jeśli nie ustawiono

def is_lesson_accessible(username, lesson_id):
    """Wrapper function dla łatwiejszego użycia"""
    return get_lesson_access_status(username, lesson_id)

def initialize_lesson_access_for_user(username):
    """Zainicjalizuj domyślny dostęp do lekcji dla nowego użytkownika"""
    users_data = load_user_data()
    
    if username not in users_data:
        return False
    
    if 'lesson_access' not in users_data[username]:
        lessons = load_lessons()
        users_data[username]['lesson_access'] = {}
        
        # Domyślnie wszystkie lekcje dostępne, ale można to zmienić
        for lesson_id in lessons.keys():
            # Specjalne reguły: np. "Wprowadzenie" dostępne zawsze, reszta może być zablokowana
            if "Wprowadzenie" in lesson_id or "wprowadzenie" in lesson_id.lower():
                users_data[username]['lesson_access'][lesson_id] = True
            else:
                # Dla przykładu: blokuj "Mózg emocjonalny" domyślnie
                if "Mózg emocjonalny" in lesson_id:
                    users_data[username]['lesson_access'][lesson_id] = False
                else:
                    users_data[username]['lesson_access'][lesson_id] = True
        
        save_user_data(users_data)
        return True
    
    return False