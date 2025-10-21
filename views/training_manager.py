"""
Narzędzie do zarządzania szkoleniem - Timer, Licytacja, Rankingi
"""

import streamlit as st
from datetime import datetime, timedelta
import time
import pandas as pd

def show_training_manager():
    """Kompleksowe narzędzie do zarządzania szkoleniem"""
    
    st.markdown("## ⏱️ Zarządzanie Szkoleniem")
    st.markdown("**Timer | Licytacja | Rankingi zespołów**")
    
    # Inicjalizacja session_state
    if 'training_teams' not in st.session_state:
        st.session_state.training_teams = [
            {"name": "Zespół 1", "bid": 0, "revenue": [100], "efficiency": [9], 
             "color": "#667eea", "logo": "🏢"},
            {"name": "Zespół 2", "bid": 0, "revenue": [100], "efficiency": [9], 
             "color": "#f093fb", "logo": "🚀"},
            {"name": "Zespół 3", "bid": 0, "revenue": [100], "efficiency": [9], 
             "color": "#4facfe", "logo": "⭐"},
        ]
    
    if 'training_timer_end' not in st.session_state:
        st.session_state.training_timer_end = None
    
    if 'training_current_round' not in st.session_state:
        st.session_state.training_current_round = 0
    
    if 'training_max_rounds' not in st.session_state:
        st.session_state.training_max_rounds = 10
    
    # Główne zakładki
    tab1, tab2, tab3, tab4 = st.tabs(["⏱️ Timer", "💰 Licytacja", "📊 Rankingi & Postępy", "⚙️ Ustawienia"])
    
    # ========== TAB 1: TIMER ==========
    with tab1:
        show_timer_tab()
    
    # ========== TAB 2: LICYTACJA ==========
    with tab2:
        show_auction_tab()
    
    # ========== TAB 3: RANKINGI ==========
    with tab3:
        show_rankings_tab()
    
    # ========== TAB 4: USTAWIENIA ==========
    with tab4:
        show_settings_tab()


def show_timer_tab():
    """Zakładka z timerem"""
    st.markdown("### ⏱️ Timer szkoleniowy")
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        minutes = st.number_input("Ustaw czas (minuty):", min_value=0, max_value=180, value=30, key="timer_minutes")
    
    with col2:
        seconds = st.number_input("Sekundy:", min_value=0, max_value=59, value=0, key="timer_seconds")
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 START", type="primary", use_container_width=True):
            total_seconds = minutes * 60 + seconds
            if total_seconds > 0:
                st.session_state.training_timer_end = datetime.now() + timedelta(seconds=total_seconds)
                st.rerun()
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⏹️ STOP", use_container_width=True):
            if st.session_state.training_timer_end:
                st.session_state.training_timer_end = None
                if 'training_timer_total' in st.session_state:
                    del st.session_state.training_timer_total
                st.rerun()
    
    # Wyświetl aktywny timer
    if st.session_state.training_timer_end:
        time_left = st.session_state.training_timer_end - datetime.now()
        
        if time_left.total_seconds() > 0:
            # Timer aktywny
            minutes_left = int(time_left.total_seconds() // 60)
            seconds_left = int(time_left.total_seconds() % 60)
            total_seconds_left = int(time_left.total_seconds())
            
            # Oblicz całkowity czas (do progress bara)
            if 'training_timer_total' not in st.session_state:
                st.session_state.training_timer_total = total_seconds_left
            
            total_seconds_initial = st.session_state.training_timer_total
            
            # Zabezpieczenie przed dzieleniem przez zero
            if total_seconds_initial > 0:
                progress = 1 - (total_seconds_left / total_seconds_initial)
                progress_ratio = total_seconds_left / total_seconds_initial
            else:
                progress = 1.0
                progress_ratio = 1.0
            
            # Użyj HTML + JavaScript do płynnego odliczania z kolorowym progress barem
            st.components.v1.html(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        font-family: 'Inter', sans-serif;
                    }}
                </style>
            </head>
            <body>
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white; padding: 80px 40px; border-radius: 30px; text-align: center;
                        margin: 20px 0; box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                        min-height: 500px; display: flex; flex-direction: column; justify-content: center;'>
                <h1 id="timer" style='font-size: 180px; margin: 0; 
                                      font-family: "Roboto Mono", monospace; font-weight: 700;
                                      text-shadow: 4px 4px 8px rgba(0,0,0,0.3); letter-spacing: 15px;'>
                    {minutes_left:02d}:{seconds_left:02d}
                </h1>
                <p style='font-size: 36px; margin: 30px 0 40px 0; 
                          font-family: "Inter", sans-serif; font-weight: 300; 
                          letter-spacing: 4px; text-transform: uppercase;'>Pozostały czas</p>
                
                <!-- Kolorowy progress bar -->
                <div style='width: 100%; max-width: 900px; margin: 0 auto; background: rgba(255,255,255,0.2); 
                            border-radius: 30px; height: 50px; overflow: hidden;
                            box-shadow: inset 0 4px 8px rgba(0,0,0,0.2);'>
                    <div id="progressBar" 
                         style='height: 100%; width: 0%; 
                                background: hsl(120, 80%, 50%);
                                border-radius: 30px;
                                box-shadow: 0 4px 12px rgba(0,0,0,0.3);'>
                    </div>
                </div>
            </div>
            
            <script>
                let secondsLeft = {total_seconds_left};
                const totalSeconds = {total_seconds_initial};
                const timerElement = document.getElementById('timer');
                const progressBar = document.getElementById('progressBar');
                
                function getProgressColor(ratio) {{
                    let hue;
                    if (ratio > 0.6) {{
                        hue = Math.floor(120 * ratio / 0.6);
                    }} else if (ratio > 0.3) {{
                        hue = Math.floor(120 - (120 - 30) * (0.6 - ratio) / 0.3);
                    }} else {{
                        hue = Math.floor(30 - 30 * (0.3 - ratio) / 0.3);
                    }}
                    return `hsl(${{hue}}, ${{ratio > 0.3 ? 90 : 95}}%, 50%)`;
                }}
                
                function updateDisplay() {{
                    const mins = Math.floor(secondsLeft / 60);
                    const secs = secondsLeft % 60;
                    timerElement.textContent = 
                        String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
                    
                    // Aktualizuj progress bar z kolorem
                    const progressRatio = secondsLeft / totalSeconds;
                    progressBar.style.width = (progressRatio * 100) + '%';
                    progressBar.style.background = getProgressColor(progressRatio);
                }}
                
                // Natychmiastowe ustawienie początkowe (bez transition)
                updateDisplay();
                
                // Dodaj transition dopiero po początkowym ustawieniu
                setTimeout(() => {{
                    progressBar.style.transition = 'width 1s linear, background 1s linear';
                }}, 50);
                
                const interval = setInterval(() => {{
                    if (secondsLeft > 0) {{
                        secondsLeft--;
                        updateDisplay();
                    }} else {{
                        progressBar.style.width = '0%';
                        progressBar.style.background = 'hsl(0, 95%, 50%)';
                        clearInterval(interval);
                        
                        // Wyświetl komunikat CZAS MINĄŁ
                        document.querySelector('div[style*="gradient"]').innerHTML = `
                            <h1 style='font-size: 120px; margin: 0; animation: pulse 1.5s infinite;
                                       font-family: "Inter", sans-serif; font-weight: 600;
                                       text-shadow: 4px 4px 8px rgba(0,0,0,0.3);'>⏰ CZAS MINĄŁ!</h1>
                            <style>
                                @keyframes pulse {{
                                    0%, 100% {{ transform: scale(1); }}
                                    50% {{ transform: scale(1.1); }}
                                }}
                            </style>
                        `;
                        
                        // Odtwórz dźwięk dzwonka
                        const audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3');
                        audio.volume = 0.7;
                        audio.play();
                    }}
                }}, 1000);
            </script>
            </body>
            </html>
            """, height=650)
            
            # Brak reruns - JavaScript sam obsługuje wszystko!
        else:
            # Czas minął!
            st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                        color: white; padding: 60px; border-radius: 20px; text-align: center;
                        margin: 20px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                        animation: pulse 1s infinite;'>
                <h1 style='font-size: 60px; margin: 0;'>⏰ CZAS MINĄŁ!</h1>
            </div>
            <style>
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
            }}
            </style>
            """, unsafe_allow_html=True)
            
            if st.button("🔄 Nowy timer", type="primary", use_container_width=True):
                st.session_state.training_timer_end = None
                st.rerun()


def show_auction_tab():
    """Zakładka licytacji"""
    st.markdown("### 💰 Licytacja zespołów")
    
    teams = st.session_state.training_teams
    
    # Sortuj po kwotach licytacji
    sorted_teams = sorted(teams, key=lambda x: x['bid'], reverse=True)
    
    # Kompaktowa tabela z edycją
    st.markdown("#### 🏆 Wpisz oferty zespołów:")
    
    # Nagłówek metryki dla najwyższej oferty
    if any(t['bid'] > 0 for t in teams):
        winner = max(teams, key=lambda x: x['bid'])
        st.success(f"� Najwyższa oferta: **{winner['name']}** - **{winner['bid']:,} zł**")
    
    # Kompaktowa tabela do edycji
    cols = st.columns(len(teams))
    bid_updates = {}
    
    for idx, (col, team) in enumerate(zip(cols, teams)):
        with col:
            st.markdown(f"**{team.get('logo', '🏢')} {team['name']}**")
            bid_updates[team['name']] = st.number_input(
                "Oferta (zł):",
                min_value=0,
                max_value=1000000,
                value=team['bid'],
                step=1000,
                key=f"bid_{team['name']}",
                label_visibility="collapsed"
            )
    
    # Przyciski w jednej linii
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("💵 Aktualizuj wszystkie oferty", type="primary", use_container_width=True):
            for team in teams:
                team['bid'] = bid_updates.get(team['name'], 0)
            st.success("✅ Oferty zaktualizowane!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset", type="secondary", use_container_width=True):
            for team in teams:
                team['bid'] = 0
            st.success("Oferty wyzerowane!")
            st.rerun()
    
    # Wykres i timer w jednym wierszu
    st.markdown("---")
    st.markdown("#### 📊 Ranking ofert - Wykres 3D")
    
    chart_col, timer_col = st.columns([2, 1])
    
    with chart_col:
        import plotly.graph_objects as go
        
        # Przygotuj dane
        sorted_for_chart = sorted(teams, key=lambda x: x['bid'], reverse=True)
        team_names = [f"{t.get('logo', '🏢')} {t['name']}" for t in sorted_for_chart]
        bids = [t['bid'] for t in sorted_for_chart]
        colors_list = [t.get('color', '#667eea') for t in sorted_for_chart]
        
        # Oblicz maksymalną wartość osi Y
        max_bid = max(bids) if bids else 0
        if max_bid >= 1000:
            y_axis_max = max_bid + 200
        else:
            y_axis_max = 1000
        
        # Stwórz wykres 3D
        fig = go.Figure(data=[
            go.Bar(
                x=team_names,
                y=bids,
                marker=dict(
                    color=colors_list,
                    line=dict(color='rgba(0,0,0,0.3)', width=2),
                    pattern_shape="",
                ),
                text=[f"{b:,} zł" for b in bids],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Oferta: %{y:,} zł<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=dict(
                text="Porównanie ofert licytacyjnych",
                font=dict(size=20, color='#667eea')
            ),
            xaxis_title="Zespół",
            yaxis_title="Oferta (zł)",
            height=450,
            showlegend=False,
            plot_bgcolor='rgba(240,240,240,0.5)',
            paper_bgcolor='white',
            font=dict(size=14),
            yaxis=dict(
                gridcolor='lightgray',
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='gray',
                range=[0, y_axis_max]
            ),
            xaxis=dict(
                tickangle=-45
            ),
            margin=dict(t=100, b=80, l=60, r=40),
            uniformtext=dict(mode='hide', minsize=10)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with timer_col:
        # Inicjalizuj stan timera dla licytacji
        if 'auction_timer_running' not in st.session_state:
            st.session_state.auction_timer_running = False
        if 'auction_timer_end' not in st.session_state:
            st.session_state.auction_timer_end = None
        
        # Ustawienia czasu w jednym wierszu: sekundy + przyciski
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            seconds = st.number_input("Sekundy:", min_value=0, max_value=300, value=60, key="auction_seconds", label_visibility="collapsed")
        
        with col2:
            if st.button("▶️", key="auction_start", type="primary", use_container_width=True):
                if seconds > 0:
                    st.session_state.auction_timer_running = True
                    st.session_state.auction_timer_end = datetime.now() + timedelta(seconds=seconds)
                    st.rerun()
        
        with col3:
            if st.button("⏹️", key="auction_stop", type="secondary", use_container_width=True):
                st.session_state.auction_timer_running = False
                st.session_state.auction_timer_end = None
                st.rerun()
        
        # Wyświetl timer pod kontrolkami
        if st.session_state.auction_timer_running and st.session_state.auction_timer_end:
            timer_html = f"""
            <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
            <style>
                .auction-timer-container {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 20px;
                    padding: 30px;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    margin-top: 20px;
                }}
                .auction-timer-display {{
                    font-family: 'Roboto Mono', monospace;
                    font-size: 80px;
                    font-weight: 700;
                    color: white;
                    text-shadow: 0 5px 10px rgba(0,0,0,0.3);
                    margin: 20px 0;
                }}
                .auction-timer-label {{
                    font-family: 'Inter', sans-serif;
                    font-size: 18px;
                    color: rgba(255,255,255,0.9);
                    font-weight: 300;
                    letter-spacing: 2px;
                }}
                .auction-progress {{
                    width: 100%;
                    height: 30px;
                    background: rgba(255,255,255,0.2);
                    border-radius: 15px;
                    overflow: hidden;
                    margin-top: 20px;
                }}
                .auction-progress-bar {{
                    height: 100%;
                    transition: width 1s linear, background-color 1s linear;
                    border-radius: 15px;
                }}
            </style>
            <div class="auction-timer-container">
                <div class="auction-timer-label">CZAS LICYTACJI</div>
                <div class="auction-timer-display" id="auctionTimer">--:--</div>
                <div class="auction-progress">
                    <div class="auction-progress-bar" id="auctionProgress"></div>
                </div>
            </div>
            <audio id="auctionGong" src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3"></audio>
            <script>
                const endTime = new Date("{st.session_state.auction_timer_end.isoformat()}").getTime();
                const totalDuration = endTime - Date.now();
                
                function updateAuctionTimer() {{
                    const now = Date.now();
                    const distance = endTime - now;
                    
                    if (distance < 0) {{
                        document.getElementById("auctionTimer").textContent = "00:00";
                        document.getElementById("auctionProgress").style.width = "0%";
                        document.getElementById("auctionGong").play();
                        window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'finished'}}, '*');
                        return;
                    }}
                    
                    const minutes = Math.floor(distance / 60000);
                    const seconds = Math.floor((distance % 60000) / 1000);
                    document.getElementById("auctionTimer").textContent = 
                        String(minutes).padStart(2, '0') + ":" + String(seconds).padStart(2, '0');
                    
                    const ratio = distance / totalDuration;
                    const percentage = ratio * 100;
                    document.getElementById("auctionProgress").style.width = percentage + "%";
                    
                    let hue;
                    if (ratio > 0.6) {{
                        hue = 120 * (ratio / 0.6);
                    }} else if (ratio > 0.3) {{
                        hue = 120 - 90 * ((0.6 - ratio) / 0.3);
                    }} else {{
                        hue = 30 - 30 * ((0.3 - ratio) / 0.3);
                    }}
                    document.getElementById("auctionProgress").style.backgroundColor = 
                        `hsl(${{hue}}, 70%, 50%)`;
                    
                    setTimeout(updateAuctionTimer, 1000);
                }}
                
                updateAuctionTimer();
            </script>
            """
            st.components.v1.html(timer_html, height=320)
            
            # Sprawdź czy timer się skończył
            if datetime.now() >= st.session_state.auction_timer_end:
                st.session_state.auction_timer_running = False
                st.session_state.auction_timer_end = None
                st.success("⏰ Czas licytacji minął!")
                st.balloons()


def show_rankings_tab():
    """Zakładka rankingów i postępów"""
    st.markdown("### 📊 Postępy zespołów")
    
    teams = st.session_state.training_teams
    current_round = st.session_state.training_current_round
    max_rounds = st.session_state.get('training_max_rounds', 10)
    
    # Kontrola rund
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Aktualna runda", f"{current_round} / {max_rounds}")
    with col2:
        progress_pct = (current_round / max_rounds * 100) if max_rounds > 0 else 0
        st.metric("Postęp", f"{progress_pct:.0f}%")
    with col3:
        if st.button("➕ Następna runda", type="primary", disabled=(current_round >= max_rounds)):
            st.session_state.training_current_round += 1
            st.rerun()
    with col4:
        if st.button("🔄 Reset", type="secondary"):
            st.session_state.training_current_round = 0
            for team in teams:
                team['revenue'] = [100]
                team['efficiency'] = [9]
            st.rerun()
    
    # Informacja jeśli osiągnięto max rund
    if current_round >= max_rounds:
        st.info(f"ℹ️ Osiągnięto maksymalną liczbę rund ({max_rounds}). Zmień limit w zakładce Ustawienia.")
    
    st.markdown("---")
    
    # Dwie tabele: Dochód i Efektywność - EDYTOWALNE
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💰 Dochód zespołów - SKUMULOWANY (edytowalna tabela)")
        
        # Przygotuj dane do edycji - używamy current_round + 1 jako max
        revenue_data = []
        max_display_rounds = max(current_round + 1, max(len(t['revenue']) for t in teams))
        
        for team in teams:
            # Upewnij się, że zespół ma wystarczająco dużo rund
            while len(team['revenue']) < max_display_rounds:
                team['revenue'].append(0)
            
            row = {
                'Logo': team.get('logo', '🏢'),
                'Zespół': team['name']
            }
            # Dodaj kolumny SKUMULOWANE dla każdej rundy
            cumulative = 0
            for r in range(max_display_rounds):
                cumulative += team['revenue'][r]
                row[f'R{r}'] = cumulative
            revenue_data.append(row)
        
        df_revenue = pd.DataFrame(revenue_data)
        
        # Konfiguracja kolumn - dynamicznie dla każdej rundy
        column_config = {
            'Logo': st.column_config.TextColumn('', width='small'),
            'Zespół': st.column_config.TextColumn('Zespół', width='medium')
        }
        
        # Dodaj konfigurację dla kolumn rund
        for r in range(max_display_rounds):
            column_config[f'R{r}'] = st.column_config.NumberColumn(
                f'R{r}',
                help=f'Skumulowany dochód do rundy {r}',
                disabled=True,  # Skumulowane są tylko do odczytu
                format='%d zł'
            )
        
        # Tabela tylko do odczytu (skumulowane wartości)
        st.dataframe(
            df_revenue,
            use_container_width=True,
            hide_index=True,
            column_config=column_config
        )
        
        # Pole do wpisania PRZYROSTU w aktualnej rundzie
        st.markdown(f"**Dodaj przychód dla rundy {current_round}:**")
        revenue_increments = {}
        cols = st.columns(len(teams))
        for idx, (col, team) in enumerate(zip(cols, teams)):
            with col:
                revenue_increments[team['name']] = st.number_input(
                    f"{team.get('logo', '🏢')} {team['name']}",
                    min_value=0,
                    max_value=1000000,
                    value=0,
                    step=100,
                    key=f'revenue_inc_{team["name"]}'
                )
        
        if st.button("➕ Dodaj przychody", type="primary", key='add_revenue'):
            for team in teams:
                increment = revenue_increments.get(team['name'], 0)
                if increment > 0:
                    if current_round < len(team['revenue']):
                        team['revenue'][current_round] += increment
                    else:
                        team['revenue'].append(increment)
            st.success("✅ Przychody dodane!")
            st.rerun()
    
    with col2:
        st.markdown("#### ⚡ Efektywność zespołów - SKUMULOWANA (edytowalna tabela)")
        
        # Przygotuj dane do edycji - używamy current_round + 1 jako max
        efficiency_data = []
        max_display_rounds = max(current_round + 1, max(len(t['efficiency']) for t in teams))
        
        for team in teams:
            # Upewnij się, że zespół ma wystarczająco dużo rund
            while len(team['efficiency']) < max_display_rounds:
                team['efficiency'].append(0)
            
            row = {
                'Logo': team.get('logo', '🏢'),
                'Zespół': team['name']
            }
            # Dodaj kolumny SKUMULOWANE dla każdej rundy
            cumulative = 0
            for r in range(max_display_rounds):
                cumulative += team['efficiency'][r]
                row[f'R{r}'] = cumulative
            efficiency_data.append(row)
        
        df_efficiency = pd.DataFrame(efficiency_data)
        
        # Konfiguracja kolumn - dynamicznie dla każdej rundy
        column_config = {
            'Logo': st.column_config.TextColumn('', width='small'),
            'Zespół': st.column_config.TextColumn('Zespół', width='medium')
        }
        
        # Dodaj konfigurację dla kolumn rund
        for r in range(max_display_rounds):
            column_config[f'R{r}'] = st.column_config.NumberColumn(
                f'R{r}',
                help=f'Skumulowana efektywność do rundy {r}',
                disabled=True,  # Skumulowane są tylko do odczytu
                format='%d'
            )
        
        # Tabela tylko do odczytu (skumulowane wartości)
        st.dataframe(
            df_efficiency,
            use_container_width=True,
            hide_index=True,
            column_config=column_config
        )
        
        # Pole do wpisania PRZYROSTU w aktualnej rundzie
        st.markdown(f"**Dodaj efektywność dla rundy {current_round}:**")
        efficiency_increments = {}
        cols = st.columns(len(teams))
        for idx, (col, team) in enumerate(zip(cols, teams)):
            with col:
                efficiency_increments[team['name']] = st.number_input(
                    f"{team.get('logo', '🏢')} {team['name']}",
                    min_value=0,
                    max_value=20,
                    value=0,
                    step=1,
                    key=f'efficiency_inc_{team["name"]}'
                )
        
        if st.button("➕ Dodaj efektywność", type="primary", key='add_efficiency'):
            for team in teams:
                increment = efficiency_increments.get(team['name'], 0)
                if increment > 0:
                    if current_round < len(team['efficiency']):
                        team['efficiency'][current_round] += increment
                    else:
                        team['efficiency'].append(increment)
            st.success("✅ Efektywność dodana!")
            st.rerun()
    
    # Wykresy SKUMULOWANE
    st.markdown("---")
    st.markdown("### 📈 Wykresy skumulowanych postępów")
    
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("💰 Skumulowany dochód", "⚡ Skumulowana efektywność")
    )
    
    for idx, team in enumerate(teams):
        team_color = team.get('color', '#667eea')
        
        # Skumulowany dochód
        cumulative_revenue = []
        total = 0
        for val in team['revenue']:
            total += val
            cumulative_revenue.append(total)
        
        fig.add_trace(
            go.Scatter(
                x=list(range(len(cumulative_revenue))),
                y=cumulative_revenue,
                name=f"{team.get('logo', '🏢')} {team['name']}",
                mode='lines+markers',
                line=dict(color=team_color, width=4),
                marker=dict(size=12, symbol='circle'),
                hovertemplate=f"{team['name']}<br>Runda: %{{x}}<br>Suma: %{{y}} zł<extra></extra>"
            ),
            row=1, col=1
        )
        
        # Skumulowana efektywność
        cumulative_efficiency = []
        total = 0
        for val in team['efficiency']:
            total += val
            cumulative_efficiency.append(total)
        
        fig.add_trace(
            go.Scatter(
                x=list(range(len(cumulative_efficiency))),
                y=cumulative_efficiency,
                name=team['name'],
                mode='lines+markers',
                line=dict(color=team_color, width=4),
                marker=dict(size=12, symbol='square'),
                showlegend=False,
                hovertemplate=f"{team['name']}<br>Runda: %{{x}}<br>Suma: %{{y}}<extra></extra>"
            ),
            row=1, col=2
        )
    
    fig.update_xaxes(title_text="Runda", row=1, col=1, gridcolor='lightgray', dtick=1)
    fig.update_xaxes(title_text="Runda", row=1, col=2, gridcolor='lightgray', dtick=1)
    fig.update_yaxes(title_text="Dochód skumulowany (zł)", row=1, col=1, gridcolor='lightgray')
    fig.update_yaxes(title_text="Efektywność skumulowana", row=1, col=2, gridcolor='lightgray')
    
    fig.update_layout(
        height=500,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified',
        plot_bgcolor='white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Wykres kołowy - Market Share
    st.markdown("---")
    st.markdown("### 📊 Market Share (udział w rynku)")
    
    # Oblicz całkowity skumulowany dochód dla każdego zespołu
    market_share_data = []
    for team in teams:
        total_revenue = sum(team['revenue'])
        if total_revenue > 0:
            market_share_data.append({
                'team': f"{team.get('logo', '🏢')} {team['name']}",
                'revenue': total_revenue,
                'color': team.get('color', '#667eea')
            })
    
    if market_share_data:
        # Sortuj od największego do najmniejszego
        market_share_data.sort(key=lambda x: x['revenue'], reverse=True)
        
        # Oblicz całkowity rynek
        total_market = sum(item['revenue'] for item in market_share_data)
        
        # Stwórz wykres kołowy
        fig_pie = go.Figure(data=[go.Pie(
            labels=[item['team'] for item in market_share_data],
            values=[item['revenue'] for item in market_share_data],
            marker=dict(
                colors=[item['color'] for item in market_share_data],
                line=dict(color='white', width=3)
            ),
            textinfo='label+percent',
            textfont=dict(size=16, color='white'),
            hovertemplate='<b>%{label}</b><br>Dochód: %{value:,} zł<br>Udział: %{percent}<extra></extra>',
            hole=0.4,  # Donut chart
            pull=[0.05 if i == 0 else 0 for i in range(len(market_share_data))]  # Wysunięcie największego kawałka
        )])
        
        # Dodaj tekst w środku
        winner = market_share_data[0]
        fig_pie.add_annotation(
            text=f"<b>Lider:</b><br>{winner['team']}<br>{winner['revenue']:,} zł",
            x=0.5, y=0.5,
            font=dict(size=16, color='#333'),
            showarrow=False
        )
        
        fig_pie.update_layout(
            title=dict(
                text=f"Udział w rynku (całkowity rynek: {total_market:,} zł)",
                font=dict(size=20, color='#667eea'),
                x=0.5,
                xanchor='center'
            ),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            ),
            height=500,
            margin=dict(t=80, b=40, l=40, r=200)
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Tabela z procentami
        st.markdown("#### 📈 Szczegółowy udział w rynku:")
        share_table = []
        for idx, item in enumerate(market_share_data):
            percentage = (item['revenue'] / total_market * 100) if total_market > 0 else 0
            share_table.append({
                'Miejsce': f"#{idx + 1}",
                'Zespół': item['team'],
                'Dochód': f"{item['revenue']:,} zł",
                'Udział': f"{percentage:.1f}%"
            })
        
        df_share = pd.DataFrame(share_table)
        st.dataframe(
            df_share,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Miejsce': st.column_config.TextColumn('🏆', width='small'),
                'Zespół': st.column_config.TextColumn('Zespół', width='medium'),
                'Dochód': st.column_config.TextColumn('Dochód całkowity', width='medium'),
                'Udział': st.column_config.TextColumn('Udział w rynku', width='small')
            }
        )
    else:
        st.info("Brak danych o przychodach. Dodaj dane w powyższych tabelach.")


def show_settings_tab():
    """Zakładka ustawień"""
    st.markdown("### ⚙️ Ustawienia szkolenia")
    
    teams = st.session_state.training_teams
    
    # Ustawienia globalne szkolenia
    st.markdown("#### 🎯 Parametry szkolenia")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'training_max_rounds' not in st.session_state:
            st.session_state.training_max_rounds = 10
        
        max_rounds = st.number_input(
            "Maksymalna liczba rund:",
            min_value=1,
            max_value=50,
            value=st.session_state.training_max_rounds,
            step=1,
            key='max_rounds_input',
            help="Określ ile rund będzie miało szkolenie"
        )
        
        if max_rounds != st.session_state.training_max_rounds:
            st.session_state.training_max_rounds = max_rounds
            st.success(f"✅ Ustawiono {max_rounds} rund")
            st.rerun()
    
    with col2:
        st.metric(
            "Aktualna runda / Max", 
            f"{st.session_state.training_current_round} / {st.session_state.training_max_rounds}",
            delta=f"{st.session_state.training_max_rounds - st.session_state.training_current_round} pozostało"
        )
    
    st.markdown("---")
    
    # Paleta kolorów i emoji
    colors = {
        'Niebieski': '#667eea',
        'Fioletowy': '#764ba2',
        'Różowy': '#f093fb',
        'Cyjan': '#4facfe',
        'Zielony': '#43e97b',
        'Pomarańczowy': '#fa709a',
        'Czerwony': '#ff6b6b',
        'Żółty': '#ffd93d'
    }
    
    logos = ['🏢', '🚀', '⭐', '💎', '🔥', '⚡', '🎯', '🏆', '💪', '🌟', '🦁', '🐉', '🦅', '🐺', '🐯']
    
    # Zarządzanie zespołami
    st.markdown("#### 👥 Zarządzanie zespołami")
    
    # Lista obecnych zespołów
    for idx, team in enumerate(teams):
        # Upewnij się, że zespół ma kolor i logo
        if 'color' not in team:
            team['color'] = list(colors.values())[idx % len(colors)]
        if 'logo' not in team:
            team['logo'] = logos[idx % len(logos)]
        
        with st.expander(f"{team.get('logo', '🏢')} {team['name']}", expanded=True):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                new_name = st.text_input(
                    "Nazwa zespołu:",
                    value=team['name'],
                    key=f"team_name_{idx}",
                    label_visibility="collapsed"
                )
                if new_name != team['name']:
                    team['name'] = new_name
                    st.rerun()
            
            with col2:
                # Wybór logo
                selected_logo = st.selectbox(
                    "Logo:",
                    options=logos,
                    index=logos.index(team.get('logo', '🏢')) if team.get('logo', '🏢') in logos else 0,
                    key=f"team_logo_{idx}"
                )
                if selected_logo != team.get('logo'):
                    team['logo'] = selected_logo
                    st.rerun()
            
            with col3:
                # Wybór koloru z kolorową ikonką
                def format_color_option(color_name):
                    color_hex = colors[color_name]
                    return f'<span style="display:inline-block; width:16px; height:16px; background-color:{color_hex}; border:1px solid #ccc; margin-right:8px; vertical-align:middle;"></span>{color_name}'
                
                selected_color = st.selectbox(
                    "Kolor:",
                    options=list(colors.keys()),
                    index=list(colors.values()).index(team.get('color', list(colors.values())[0])) 
                        if team.get('color') in colors.values() else 0,
                    key=f"team_color_{idx}",
                    format_func=lambda x: f"■ {x}"  # Fallback dla zwykłego tekstu, ale użyjemy HTML poniżej
                )
                
                # Wyświetl podgląd koloru pod selectboxem
                st.markdown(
                    f'<div style="background-color: {colors[selected_color]}; height: 30px; border-radius: 5px; margin-top: -10px;"></div>',
                    unsafe_allow_html=True
                )
                
                if colors[selected_color] != team.get('color'):
                    team['color'] = colors[selected_color]
                    st.rerun()
            
            with col4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"delete_team_{idx}", help="Usuń zespół"):
                    if len(teams) > 2:
                        teams.pop(idx)
                        st.success("✅ Zespół usunięty!")
                        st.rerun()
                    else:
                        st.error("Min. 2 zespoły!")
            
            # Podgląd koloru
            st.markdown(
                f"<div style='background: {team.get('color', '#667eea')}; "
                f"height: 30px; border-radius: 10px; margin-top: 10px;'></div>",
                unsafe_allow_html=True
            )
    
    # Dodaj nowy zespół
    st.markdown("---")
    st.markdown("#### ➕ Dodaj nowy zespół")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        new_team_name = st.text_input(
            "Nazwa nowego zespołu:", 
            placeholder="Wpisz nazwę zespołu...",
            key="new_team_name"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Dodaj", type="primary", use_container_width=True):
            if new_team_name:
                # Użyj następnego koloru i logo w kolejności
                next_idx = len(teams)
                teams.append({
                    "name": new_team_name,
                    "bid": 0,
                    "revenue": [100],
                    "efficiency": [9],
                    "color": list(colors.values())[next_idx % len(colors)],
                    "logo": logos[next_idx % len(logos)]
                })
                st.success(f"✅ Dodano: {new_team_name}")
                st.rerun()
            else:
                st.warning("Wpisz nazwę zespołu!")
    
    # Reset wszystkiego
    st.markdown("---")
    st.markdown("#### 🔄 Reset globalny")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Uwaga:** To usunie wszystkie dane i przywróci ustawienia domyślne.")
    with col2:
        if st.button("🔥 RESET", type="secondary", use_container_width=True):
            st.session_state.training_teams = [
                {"name": "Zespół 1", "bid": 0, "revenue": [100], "efficiency": [9], 
                 "color": "#667eea", "logo": "🏢"},
                {"name": "Zespół 2", "bid": 0, "revenue": [100], "efficiency": [9], 
                 "color": "#f093fb", "logo": "🚀"},
                {"name": "Zespół 3", "bid": 0, "revenue": [100], "efficiency": [9], 
                 "color": "#4facfe", "logo": "⭐"},
            ]
            st.session_state.training_timer_end = None
            st.session_state.training_current_round = 0
            st.success("✅ Wszystko zresetowane!")
            st.rerun()


if __name__ == "__main__":
    show_training_manager()
