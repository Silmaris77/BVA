"""
Komponenty nagłówków dla Business Games
Funkcje renderujące nagłówki dashboard dla różnych branż
"""

import streamlit as st
from data.business_data import FIRM_LEVELS, GAME_CONFIG
from utils.business_game import get_firm_summary, calculate_overall_score


def render_fmcg_header(user_data, bg_data):
    """Renderuje nagłówek dla FMCG Career Model"""
    from data.industries.fmcg import CAREER_LEVELS as FMCG_LEVELS, INDUSTRY_INFO as FMCG_INFO
    
    career = bg_data["career"]
    metrics = bg_data["metrics"]
    level = career["level"]
    level_info = FMCG_LEVELS[level]
    
    # CSS (takie same style jak Consulting)
    st.markdown("""
    <style>
    .game-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        height: 100%;
    }
    .game-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    .firm-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    .firm-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(102, 126, 234, 0.6);
    }
    .stat-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
        border-left: 4px solid;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    }
    .stat-card.gold { border-left-color: #f59e0b; }
    .stat-card.purple { border-left-color: #8b5cf6; }
    .stat-card.blue { border-left-color: #3b82f6; }
    .stat-card.green { border-left-color: #10b981; }
    .stat-value {
        font-size: 28px;
        font-weight: 700;
        margin: 8px 0;
        color: #1e293b;
    }
    .stat-label {
        font-size: 13px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # JEDEN WIERSZ: Career Card | Monthly Sales | Market Share | CSAT
    col_career, col1, col2, col3 = st.columns([1.5, 1, 1, 1])
    
    with col_career:
        team_size = len(bg_data.get("team", []))
        
        # Buduj HTML ręcznie bez f-string w środku
        if team_size > 0:
            team_section = f"<p style='margin:2px 0; opacity:0.85; font-size: 13px;'>👥 Zespół: {team_size} osób</p>"
        else:
            team_section = ""
        
        # Komponuj HTML bez zagnieżdżonych f-stringów
        html_parts = [
            "<div class='firm-card' style='padding: 20px; display: flex; align-items: center; gap: 16px; min-height: 140px; height: 100%;'>",
            f"<div style='font-size: 48px;'>{career['company_logo']}</div>",
            "<div style='flex: 1;'>",
            f"<h2 style='margin:0; font-size: 18px; font-weight: 700;'>{career['title']}</h2>",
            f"<p style='margin:4px 0 0 0; opacity:0.9; font-size: 13px;'>{career['company']}</p>",
            team_section,
            f"<p style='margin:2px 0 0 0; opacity:0.75; font-size: 12px;'>Poziom {level}/10</p>",
            "</div>",
            "</div>"
        ]
        
        html = "".join(html_parts)
        st.markdown(html, unsafe_allow_html=True)
    
    with col1:
        monthly_sales = metrics.get("monthly_sales", 0)
        st.markdown(f"""
        <div class='stat-card gold'>
            <div class='stat-label'>💰 Monthly Sales</div>
            <div class='stat-value'>{monthly_sales:,.0f}</div>
            <div style='font-size: 12px; color: #64748b;'>PLN</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        market_share = metrics.get("market_share", 0)
        # Progress do następnego poziomu
        next_level = level + 1
        progress_info = ""
        if next_level <= 10:
            next_level_info = FMCG_LEVELS[next_level]
            required_share = next_level_info['required_metrics'].get('market_share', 0)
            if required_share > 0:
                progress_pct = min(100, (market_share / required_share) * 100)
                progress_info = f"<div style='margin-top: 8px;'><div style='background: #e2e8f0; border-radius: 4px; height: 4px; overflow: hidden;'><div style='background: #8b5cf6; height: 100%; width: {progress_pct}%;'></div></div><div style='font-size: 10px; color: #64748b; margin-top: 2px;'>Do awansu: {required_share}%</div></div>"
        
        st.markdown(f"""
        <div class='stat-card purple'>
            <div class='stat-label'>📊 Market Share</div>
            <div class='stat-value'>{market_share:.1f}%</div>
            <div style='font-size: 12px; color: #64748b;'>territory</div>
            {progress_info}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        csat = metrics.get("customer_satisfaction", 75)
        st.markdown(f"""
        <div class='stat-card blue'>
            <div class='stat-label'>⭐ Customer Satisfaction</div>
            <div class='stat-value'>{csat:.0f}%</div>
            <div style='font-size: 12px; color: #64748b;'>CSAT score</div>
        </div>
        """, unsafe_allow_html=True)


def render_header(user_data, industry_id="consulting"):
    """Renderuje nagłówek z profesjonalnymi kartami w stylu gamifikacji
    
    OBSŁUGUJE DWA MODELE:
    - Consulting: Firma, Saldo, Reputacja, Rating
    - FMCG: Kariera, Monthly Sales, Market Share, CSAT
    """
    bg_data = user_data["business_games"][industry_id]
    
    # ========== FMCG CAREER MODEL ==========
    if industry_id == "fmcg":
        render_fmcg_header(user_data, bg_data)
        return
    
    # ========== CONSULTING FIRM MODEL ==========
    firm = bg_data["firm"]
    level_info = FIRM_LEVELS[firm["level"]]
    
    # BACKWARD COMPATIBILITY: Dodaj logo jeśli nie istnieje
    if "logo" not in firm:
        firm["logo"] = level_info['ikona']  # Użyj ikony poziomu jako domyślnej
    
    # CSS dla profesjonalnych kart z efektami
    st.markdown("""
    <style>
    .game-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        height: 100%;
    }
    .game-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    .firm-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    .firm-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(102, 126, 234, 0.6);
    }
    .stat-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
        border-left: 4px solid;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    }
    .stat-card.gold { border-left-color: #f59e0b; }
    .stat-card.purple { border-left-color: #8b5cf6; }
    .stat-card.blue { border-left-color: #3b82f6; }
    .stat-card.green { border-left-color: #10b981; }
    .stat-value {
        font-size: 28px;
        font-weight: 700;
        margin: 8px 0;
        color: #1e293b;
    }
    .stat-label {
        font-size: 13px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # JEDEN WIERSZ: Logo+Nazwa | Saldo | Reputacja | Rating
    summary = get_firm_summary(user_data)
    
    col_firm, col1, col2, col3 = st.columns([1.5, 1, 1, 1])
    
    with col_firm:
        st.markdown(f"""
        <div class='firm-card' style='padding: 20px; display: flex; align-items: center; gap: 16px; min-height: 140px; height: 100%;'>
            <div style='font-size: 48px;'>{firm['logo']}</div>
            <div style='flex: 1;'>
                <h2 style='margin:0; font-size: 22px; font-weight: 700;'>{firm['name']}</h2>
                <p style='margin:4px 0 0 0; opacity:0.9; font-size: 14px;'>
                    Poziom {firm['level']}: {level_info['nazwa']}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col1:
        firm_money = bg_data.get('money', 0)
        st.markdown(f"""
        <div class='stat-card gold'>
            <div class='stat-label'>💰 Saldo firmy</div>
            <div class='stat-value'>{firm_money:,}</div>
            <div style='font-size: 12px; color: #64748b;'>PLN</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Oblicz następny próg reputacji
        current_rep = firm['reputation']
        next_level_rep = None
        if firm['level'] == 1:
            next_level_rep = GAME_CONFIG["reputation_to_level_2"]
            next_level_name = "Boutique Consulting"
        elif firm['level'] == 2:
            next_level_rep = GAME_CONFIG["reputation_to_level_3"]
            next_level_name = "CIQ Advisory Group"
        elif firm['level'] == 3:
            next_level_rep = GAME_CONFIG["reputation_to_level_4"]
            next_level_name = "Global CIQ Partners"
        else:
            next_level_rep = None
            next_level_name = "MAX"
        
        progress_info = ""
        if next_level_rep:
            progress_pct = min(100, (current_rep / next_level_rep) * 100)
            progress_info = f"<div style='margin-top: 8px;'><div style='background: #e2e8f0; border-radius: 4px; height: 4px; overflow: hidden;'><div style='background: #8b5cf6; height: 100%; width: {progress_pct}%;'></div></div><div style='font-size: 10px; color: #64748b; margin-top: 2px;'>Do {next_level_name}: {next_level_rep}</div></div>"
        
        st.markdown(f"""
        <div class='stat-card purple'>
            <div class='stat-label'>📈 Reputacja</div>
            <div class='stat-value'>{current_rep}</div>
            <div style='font-size: 12px; color: #64748b;'>punktów</div>
            {progress_info}
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Rating - używamy oficjalnej funkcji z business_game
        overall_score = calculate_overall_score(bg_data)
        st.markdown(f"""
        <div class='stat-card blue'>
            <div class='stat-label'>🏆 Rating</div>
            <div class='stat-value'>{overall_score:,.0f}</div>
            <div style='font-size: 12px; color: #64748b;'>punktów</div>
        </div>
        """, unsafe_allow_html=True)
