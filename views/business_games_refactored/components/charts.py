"""
Wykresy i wizualizacje dla Business Games
Zawiera funkcje tworzące wykresy finansowe i analityczne
"""

from datetime import datetime, timedelta
import plotly.graph_objects as go


def create_financial_chart(bg_data, period=7, cumulative=False):
    """Tworzy wykres finansowy z przychodami, kosztami i zyskiem
    
    Args:
        bg_data: business_game data
        period: liczba dni do wyświetlenia (7, 14, 30)
        cumulative: czy pokazać wartości skumulowane
    
    Returns:
        Plotly figure object
    """
    # Pobierz transakcje
    transactions = bg_data.get("history", {}).get("transactions", [])
    
    if not transactions:
        # Pusty wykres jeśli brak danych - gamifikowany styl
        fig = go.Figure()
        fig.add_annotation(
            text="🎮 Brak danych finansowych<br><span style='font-size: 14px;'>Ukończ pierwszy kontrakt aby zobaczyć wykres!</span>",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color="#64748b", family="Arial")
        )
        fig.update_layout(
            height=400,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='#f8fafc',
            paper_bgcolor='white',
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
    
    # Przygotuj dane dzienne
    daily_data = {}
    for trans in transactions:
        try:
            if "timestamp" not in trans:
                continue  # Pomiń transakcje bez timestamp
            date = trans["timestamp"][:10]  # YYYY-MM-DD
            if date not in daily_data:
                daily_data[date] = {"revenue": 0, "costs": 0}
            
            trans_type = trans.get("type", "")
            amount = trans.get("amount", 0)  # Bezpieczne pobieranie amount
            
            if trans_type in ["contract_reward", "event_reward"]:
                # Przychody z kontraktów i pozytywnych wydarzeń
                daily_data[date]["revenue"] += amount
            elif trans_type in ["daily_costs", "employee_hired", "employee_hire", "event_cost", "office_rent", "office_upgrade"]:
                # Koszty: pracownicy + biuro + negatywne wydarzenia
                daily_data[date]["costs"] += abs(amount)
            # employee_fired nie wpływa na wykres (amount = 0), ale jest w historii
        except Exception as e:
            continue
    
    # Pobierz datę założenia firmy (founded) jako punkt startowy
    firm_founded_str = bg_data.get("firm", {}).get("founded")
    
    if firm_founded_str:
        try:
            # Firma ma datę założenia - użyj jej jako start
            firm_founded = datetime.strptime(firm_founded_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            # Jeśli format niepoprawny, użyj pierwszej transakcji lub dzisiaj
            firm_founded = None
    else:
        firm_founded = None
    
    # Jeśli brak daty założenia, użyj pierwszej transakcji
    if not firm_founded and daily_data:
        sorted_dates = sorted(daily_data.keys())
        if sorted_dates:
            firm_founded = datetime.strptime(sorted_dates[0], "%Y-%m-%d")
    
    # Jeśli wciąż brak daty, użyj dzisiaj
    if not firm_founded:
        firm_founded = datetime.now()
    
    # Określ zakres wyświetlania
    end_date = datetime.now()
    
    # Start = data założenia firmy (ale nie więcej niż 'period' dni wstecz)
    max_start_date = end_date - timedelta(days=period - 1)
    
    if firm_founded < max_start_date:
        # Firma jest starsza niż okres wyświetlania - pokaż tylko ostatnie X dni
        start_date = max_start_date
    else:
        # Firma jest młodsza - pokaż od daty założenia
        start_date = firm_founded
    
    dates = []
    revenues = []
    costs = []
    
    # Oblicz liczbę dni do wyświetlenia
    days_to_show = (end_date - start_date).days + 1
    
    for i in range(days_to_show):
        date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        dates.append(date)
        
        # Pobierz dane lub użyj 0 (pokazujemy wszystkie dni, nawet puste)
        day_data = daily_data.get(date, {"revenue": 0, "costs": 0})
        revenues.append(day_data["revenue"])
        costs.append(day_data["costs"])
    
    # Oblicz zysk
    profits = [r - c for r, c in zip(revenues, costs)]
    
    # Jeśli cumulative, oblicz wartości narastające
    if cumulative:
        revenues_cum = []
        costs_cum = []
        profits_cum = []
        
        rev_sum = 0
        cost_sum = 0
        
        for r, c in zip(revenues, costs):
            rev_sum += r
            cost_sum += c
            revenues_cum.append(rev_sum)
            costs_cum.append(cost_sum)
            profits_cum.append(rev_sum - cost_sum)
        
        revenues = revenues_cum
        costs = costs_cum
        profits = profits_cum
    
    # Formatuj daty na osi X (format: DD.MM np. 06.11)
    if not dates:
        # Zabezpieczenie - jeśli brak dat, zwróć pusty wykres
        dates_formatted = []
    else:
        dates_formatted = []
        for d in dates:
            try:
                date_obj = datetime.strptime(d, "%Y-%m-%d")
                dates_formatted.append(date_obj.strftime("%d.%m"))
            except (ValueError, TypeError):
                dates_formatted.append(d)  # Fallback - użyj oryginalnej wartości
    
    # Twórz wykres - GRYWALIZACYJNY STYL
    fig = go.Figure()
    
    # Trace 1: PRZYCHODY (zielony gradient)
    fig.add_trace(go.Scatter(
        x=dates_formatted,
        y=revenues,
        name='💰 Przychody',
        mode='lines+markers',
        line=dict(color='#10b981', width=4, shape='spline'),
        marker=dict(
            size=10,
            color='#10b981',
            line=dict(color='white', width=2),
            symbol='circle'
        ),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.15)',
        hovertemplate='<b>%{x}</b><br>Przychody: %{y:,.0f} 💰<extra></extra>'
    ))
    
    # Trace 2: KOSZTY (czerwony gradient)
    fig.add_trace(go.Scatter(
        x=dates_formatted,
        y=costs,
        name='💸 Koszty',
        mode='lines+markers',
        line=dict(color='#ef4444', width=4, shape='spline'),
        marker=dict(
            size=10,
            color='#ef4444',
            line=dict(color='white', width=2),
            symbol='circle'
        ),
        fill='tozeroy',
        fillcolor='rgba(239, 68, 68, 0.15)',
        hovertemplate='<b>%{x}</b><br>Koszty: %{y:,.0f} 💸<extra></extra>'
    ))
    
    # Trace 3: ZYSK (fioletowy, grubsza linia)
    profit_colors = ['#10b981' if p > 0 else '#ef4444' if p < 0 else '#94a3b8' for p in profits]
    
    fig.add_trace(go.Scatter(
        x=dates_formatted,
        y=profits,
        name='💎 Zysk',
        mode='lines+markers',
        line=dict(color='#8b5cf6', width=5, shape='spline'),
        marker=dict(
            size=12,
            color=profit_colors,
            line=dict(color='white', width=3),
            symbol='diamond'
        ),
        hovertemplate='<b>%{x}</b><br>Zysk: %{y:,.0f} 💎<extra></extra>'
    ))
    
    # Layout - PROFESJONALNY I GRYWALIZACYJNY
    # Stwórz tytuł z rzeczywistym zakresem dat
    if dates_formatted:
        date_range = f"({dates_formatted[0]} - {dates_formatted[-1]})"
    else:
        date_range = ""
    
    title_text = f"{'📈 Wartości Skumulowane' if cumulative else '📊 Przychody i Koszty'} {date_range}"
    
    fig.update_layout(
        title=dict(
            text=title_text,
            font=dict(size=18, color='#1e293b', family='Arial Black', weight='bold'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Data",
            type='category',  # Traktuj etykiety jako kategorie (tekst), nie liczby
            showgrid=True,
            gridcolor='#e2e8f0',
            gridwidth=1,
            showline=True,
            linecolor='#cbd5e1',
            linewidth=2,
            tickfont=dict(size=11, color='#64748b', family='Arial'),
            tickangle=-45,  # Obróć etykiety dla lepszej czytelności
            tickmode='linear'  # Pokaż wszystkie etykiety
        ),
        yaxis=dict(
            title="",
            showgrid=True,
            gridcolor='#e2e8f0',
            gridwidth=1,
            showline=True,
            linecolor='#cbd5e1',
            linewidth=2,
            tickfont=dict(size=12, color='#64748b', family='Arial'),
            tickformat=',',
            ticksuffix=' 💰'
        ),
        height=400,
        hovermode='x unified',
        plot_bgcolor='#f8fafc',
        paper_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='#e2e8f0',
            borderwidth=2,
            font=dict(size=13, family='Arial', weight='bold')
        ),
        margin=dict(l=60, r=40, t=80, b=50),
        font=dict(family='Arial'),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Arial",
            bordercolor='#cbd5e1'
        )
    )
    
    # Dodaj linię zerową dla zysku (wizualna pomoc)
    fig.add_hline(
        y=0, 
        line_dash="dash", 
        line_color="#94a3b8", 
        line_width=2,
        opacity=0.5,
        annotation_text="",
    )
    
    return fig
