"""
🛒 FMCG Industry Module for Business Games

Moduł branży FMCG (Fast-Moving Consumer Goods) - FreshLife Poland
Zawiera wszystkie zakładki i funkcjonalności specyficzne dla FMCG.

Wyekstrahowane z business_games.py (KROK 7 - FMCG separation)
"""

import streamlit as st
from datetime import datetime
from views.business_games_refactored.helpers import get_game_data, save_game_data

# Import nowych modułów rozszerzeń
from utils.fmcg_client_helpers import (
    migrate_fmcg_customers_to_new_structure,
    get_client_by_id,
    get_clients_by_status,
    is_visit_overdue,
    get_reputation_status
)
from utils.fmcg_reputation import (
    update_client_reputation,
    record_visit,
    sign_contract,
    check_overdue_visits
)
from utils.fmcg_products import (
    get_product_info,
    suggest_cross_sell_products,
    get_portfolio_summary,
    FRESHLIFE_PRODUCTS
)

# =============================================================================
# MIGRATION & INITIALIZATION
# =============================================================================

def ensure_fmcg_data_structure(username: str, user_data: dict, bg_data: dict) -> int:
    """
    Sprawdza strukturę danych FMCG i przeprowadza migrację jeśli potrzebna
    
    Args:
        username: Nazwa użytkownika
        user_data: Cały dict user_data
        bg_data: business_games["fmcg"] dict
    
    Returns:
        Liczba zmigrowanych klientów (0 jeśli brak migracji)
    """
    
    customers_data = bg_data.get("customers", {})
    
    # Sprawdź czy już jest nowa struktura
    if "clients" in customers_data:
        # Już zmigrowane
        return 0
    
    # Sprawdź czy są dane do migracji
    if "prospects" not in customers_data and "active_clients" not in customers_data:
        # Nowa instalacja - inicjalizuj pustą strukturę
        customers_data["clients"] = {}
        bg_data["customers"] = customers_data
        return 0
    
    # MIGRACJA
    st.info("🔄 Wykryto starą strukturę danych - przeprowadzam migrację do nowego systemu...")
    
    migrated_data, count = migrate_fmcg_customers_to_new_structure(bg_data)
    
    # Nadpisz bg_data
    bg_data.update(migrated_data)
    
    # Zapisz
    import json
    users_file = "users_data.json"
    with open(users_file, "r", encoding="utf-8") as f:
        all_users = json.load(f)
    all_users[username] = user_data
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(all_users, f, ensure_ascii=False, indent=2)
    
    st.success(f"✅ Zmigrowano {count} klientów do nowego systemu z reputacją i portfolio!")
    
    return count

# =============================================================================
# FMCG TABS
# =============================================================================

def show_fmcg_company_info_tab(username, user_data, industry_id):
    """Zakładka z informacjami o firmie FreshLife Poland i portfolio produktów"""
    from data.industries.fmcg_company import COMPANY_INFO, PRODUCT_PORTFOLIO
    
    # Hero Card - Główna informacja o firmie
    st.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 16px; color: white; margin-bottom: 24px; box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);'>
<div style='font-size: 32px; font-weight: 700; margin-bottom: 12px;'>🛒 FreshLife Poland</div>
<div style='font-size: 18px; opacity: 0.95; line-height: 1.6;'>Wiodący producent i dystrybutor produktów FMCG w Polsce<br><span style='font-size: 14px; opacity: 0.8;'>Część globalnej grupy FreshLife International</span></div>
</div>
""", unsafe_allow_html=True)
    
    # Karty z kluczowymi informacjami (3 kolumny)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
<div style='background: white; padding: 20px; border-radius: 12px; border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
<div style='color: #667eea; font-size: 14px; font-weight: 600; margin-bottom: 8px;'>📅 ROK ZAŁOŻENIA</div>
<div style='font-size: 28px; font-weight: 700; color: #1e293b;'>{COMPANY_INFO['founded']}</div>
<div style='color: #64748b; font-size: 13px; margin-top: 4px;'>{2025 - int(COMPANY_INFO['founded'])} lat doświadczenia</div>
</div>
""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
<div style='background: white; padding: 20px; border-radius: 12px; border-left: 4px solid #10b981; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
<div style='color: #10b981; font-size: 14px; font-weight: 600; margin-bottom: 8px;'>👥 PRACOWNICY</div>
<div style='font-size: 28px; font-weight: 700; color: #1e293b;'>{COMPANY_INFO['employees_poland']}</div>
<div style='color: #64748b; font-size: 13px; margin-top: 4px;'>w całej Polsce</div>
</div>
""", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
<div style='background: white; padding: 20px; border-radius: 12px; border-left: 4px solid #f59e0b; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
<div style='color: #f59e0b; font-size: 14px; font-weight: 600; margin-bottom: 8px;'>📍 SIEDZIBA</div>
<div style='font-size: 20px; font-weight: 700; color: #1e293b;'>{COMPANY_INFO['hq_location']}</div>
<div style='color: #64748b; font-size: 13px; margin-top: 4px;'>+ oddziały w całym kraju</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 24px 0;'></div>", unsafe_allow_html=True)
    
    # Misja i Wartości w jednym rzędzie
    col_mission, col_values = st.columns([1.2, 1.8])
    
    with col_mission:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 24px; border-radius: 12px; color: white; height: 100%; box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);'>
<div style='font-size: 18px; font-weight: 700; margin-bottom: 12px;'>🎯 Nasza Misja</div>
<div style='font-size: 14px; line-height: 1.6; opacity: 0.95;'>{COMPANY_INFO['mission']}</div>
</div>
""", unsafe_allow_html=True)
    
    with col_values:
        st.markdown("**💎 Wartości Firmy**")
        values_cols = st.columns(len(COMPANY_INFO['values']))
        for i, value in enumerate(COMPANY_INFO['values']):
            with values_cols[i]:
                st.markdown(f"""
<div style='background: #f8fafc; padding: 12px; border-radius: 8px; text-align: center; border: 2px solid #e2e8f0;'>
<div style='font-size: 13px; font-weight: 600; color: #475569;'>{value}</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 32px 0;'></div>", unsafe_allow_html=True)
    
    # Szczegółowy opis firmy - karty z gradientami
    st.markdown(f"""
<div style='font-size: 22px; font-weight: 700; color: #1e293b; margin-bottom: 16px;'>
📖 Historia i Filozofia
</div>
""", unsafe_allow_html=True)
    
    col_desc1, col_desc2 = st.columns(2)
    
    with col_desc1:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%); padding: 24px; border-radius: 12px; color: white; height: 100%; box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);'>
<div style='font-size: 18px; font-weight: 700; margin-bottom: 12px;'>📚 Historia Firmy</div>
<div style='font-size: 14px; line-height: 1.6; opacity: 0.95;'>{COMPANY_INFO.get('description', 'FreshLife Poland to jedna z wiodących firm FMCG w Polsce, oferująca szeroki asortyment produktów codziennego użytku.')}</div>
</div>
""", unsafe_allow_html=True)
    
    with col_desc2:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%); padding: 24px; border-radius: 12px; color: white; height: 100%; box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);'>
<div style='font-size: 18px; font-weight: 700; margin-bottom: 12px;'>💡 Nasza Filozofia</div>
<div style='font-size: 14px; line-height: 1.6; opacity: 0.95;'>{COMPANY_INFO.get('philosophy', 'Wierzymy w jakość, innowacyjność i odpowiedzialność społeczną. Każdy nasz produkt jest tworzony z myślą o zadowoleniu klientów i ochronie środowiska.')}</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 32px 0;'></div>", unsafe_allow_html=True)
    
    # Pozycja Rynkowa - Karty z efektami
    st.markdown(f"""
<div style='font-size: 22px; font-weight: 700; color: #1e293b; margin-bottom: 16px;'>
📈 Nasza Pozycja na Rynku
</div>
""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px; border-radius: 16px; color: white; text-align: center; box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3); transition: transform 0.3s ease;'>
<div style='font-size: 36px; margin-bottom: 12px;'>🧴</div>
<div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>Personal Care</div>
<div style='font-size: 32px; font-weight: 700; margin: 12px 0;'>#{COMPANY_INFO['market_position']['personal_care']}</div>
<div style='font-size: 12px; opacity: 0.85; padding: 8px 12px; background: rgba(255,255,255,0.2); border-radius: 20px; display: inline-block;'>TOP 3 w Polsce</div>
</div>
""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 24px; border-radius: 16px; color: white; text-align: center; box-shadow: 0 8px 20px rgba(240, 147, 251, 0.3); transition: transform 0.3s ease;'>
<div style='font-size: 36px; margin-bottom: 12px;'>🍽️</div>
<div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>Food & Beverages</div>
<div style='font-size: 32px; font-weight: 700; margin: 12px 0;'>#{COMPANY_INFO['market_position']['food']}</div>
<div style='font-size: 12px; opacity: 0.85; padding: 8px 12px; background: rgba(255,255,255,0.2); border-radius: 20px; display: inline-block;'>TOP 5 w Polsce</div>
</div>
""", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 24px; border-radius: 16px; color: white; text-align: center; box-shadow: 0 8px 20px rgba(79, 172, 254, 0.3); transition: transform 0.3s ease;'>
<div style='font-size: 36px; margin-bottom: 12px;'>🏠</div>
<div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>Home Care</div>
<div style='font-size: 32px; font-weight: 700; margin: 12px 0;'>#{COMPANY_INFO['market_position']['home_care']}</div>
<div style='font-size: 12px; opacity: 0.85; padding: 8px 12px; background: rgba(255,255,255,0.2); border-radius: 20px; display: inline-block;'>Lider Polski</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
    
    # Portfolio Produktów - Header z CTA
    st.markdown(f"""
<div style='background: linear-gradient(to right, #fbbf24, #f59e0b); padding: 20px 24px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);'>
<div style='display: flex; justify-content: space-between; align-items: center; color: white;'>
<div>
<div style='font-size: 24px; font-weight: 700; margin-bottom: 4px;'>🛍️ Portfolio Produktów</div>
<div style='font-size: 14px; opacity: 0.95;'>Poznaj nasze produkty - klucz do sukcesu w rozmowach z klientami</div>
</div>
<div style='background: rgba(255,255,255,0.25); padding: 12px 20px; border-radius: 20px; font-size: 14px; font-weight: 600;'>💡 Wiedza = Sprzedaż</div>
</div>
</div>
""", unsafe_allow_html=True)
    
    # Zakładki dla kategorii z nowymi ikonami
    tab_pc, tab_food, tab_hc = st.tabs([
        "🧴 Personal Care (TOP 3)", 
        "🍽️ Food & Beverages (TOP 5)", 
        "🏠 Home Care (LIDER)"
    ])
    
    with tab_pc:
        show_product_category(PRODUCT_PORTFOLIO['personal_care'])
    
    with tab_food:
        show_product_category(PRODUCT_PORTFOLIO['food'])
    
    with tab_hc:
        show_product_category(PRODUCT_PORTFOLIO['home_care'])


def show_product_category(category):
    """Wyświetla produkty z danej kategorii w grywalizacyjnym stylu"""
    
    # Header kategorii jako karta
    st.markdown(f"""
<div style='background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 24px; border-radius: 12px; color: white; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);'>
<div style='font-size: 26px; font-weight: 700; margin-bottom: 8px;'>{category['category_name']}</div>
<div style='font-size: 14px; opacity: 0.95; margin-bottom: 12px;'>{category['description']}</div>
<div style='display: inline-block; background: rgba(255,255,255,0.25); padding: 8px 16px; border-radius: 20px; font-size: 14px; font-weight: 600;'>📊 Udział w rynku: {category['market_share']}%</div>
</div>
""", unsafe_allow_html=True)
    
    # Produkty jako karty w grid 2 kolumny
    for idx in range(0, len(category['products']), 2):
        cols = st.columns(2)
        
        for col_idx, col in enumerate(cols):
            if idx + col_idx < len(category['products']):
                product = category['products'][idx + col_idx]
                
                with col:
                    # Określ kolor karty bazując na potencjale wolumenu
                    volume_colors = {
                        'high': ('linear-gradient(135deg, #10b981 0%, #059669 100%)', '#10b981'),
                        'medium': ('linear-gradient(135deg, #f59e0b 0%, #d97706 100%)', '#f59e0b'),
                        'low': ('linear-gradient(135deg, #6b7280 0%, #4b5563 100%)', '#6b7280')
                    }
                    bg_gradient, border_color = volume_colors.get(
                        product['volume_potential'].lower(), 
                        ('linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)', '#6366f1')
                    )
                    
                    # Karta produktu
                    st.markdown(f"""
<div style='background: white; border-radius: 12px; border-left: 4px solid {border_color}; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: transform 0.2s, box-shadow 0.2s;'>
<div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
<div>
<div style='font-size: 18px; font-weight: 700; color: #1e293b; margin-bottom: 4px;'>📦 {product['name']}</div>
<div style='font-size: 13px; color: #64748b; font-weight: 500;'>{product['subcategory']}</div>
</div>
<div style='background: {bg_gradient}; color: white; padding: 6px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; white-space: nowrap;'>{product['volume_potential'].upper()}</div>
</div>
</div>
""", unsafe_allow_html=True)
                    
                    # Expander z detalami
                    with st.expander("🔍 Szczegóły produktu", expanded=False):
                        detail_col1, detail_col2 = st.columns([1.5, 1])
                        
                        with detail_col1:
                            st.markdown(f"""
**💡 USP (Unique Selling Proposition):**  
{product['usp']}

**📦 Warianty:**  
{', '.join(product['variants'])}

**🎯 Grupa docelowa:** {product['target_group']}

**📦 Opakowanie:** {product['packaging']}

**⏰ Termin przydatności:** {product['shelf_life']}
""")
                            
                            if product.get('awards'):
                                st.markdown(f"**🏆 Nagrody:** {', '.join(product['awards'])}")
                        
                        with detail_col2:
                            # Kompaktowy box z danymi - stats card
                            st.markdown(f"""
<div style='background: #f8fafc; padding: 16px; border-radius: 8px; border: 2px solid #e2e8f0;'>
<div style='margin-bottom: 16px;'>
<div style='font-size: 11px; color: #64748b; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px;'>💰 Cena Detaliczna</div>
<div style='font-size: 20px; font-weight: 700; color: #0f172a;'>{product["price_range"]}</div>
</div>
<div style='margin-bottom: 16px;'>
<div style='font-size: 11px; color: #64748b; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px;'>📊 Marża</div>
<div style='font-size: 20px; font-weight: 700; color: #10b981;'>{product["margin_percent"]}%</div>
</div>
<div style='padding: 12px; background: {bg_gradient}; border-radius: 6px; text-align: center;'>
<div style='font-size: 11px; color: white; opacity: 0.9; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px;'>Potencjał Wolumenu</div>
<div style='font-size: 16px; font-weight: 700; color: white;'>{product["volume_potential"].upper()}</div>
</div>
</div>
""", unsafe_allow_html=True)


def show_fmcg_dashboard_tab(username, user_data, industry_id):
    """Dashboard FMCG - przegląd kariery, cele, postępy"""
    bg_data = user_data["business_games"][industry_id]
    
    from data.industries.fmcg import CAREER_LEVELS as FMCG_LEVELS
    from data.scenarios import get_scenario
    
    career = bg_data["career"]
    metrics = bg_data["metrics"]
    level = career["level"]
    scenario_id = bg_data.get("scenario_id")
    
    # 📋 CELE SCENARIUSZA
    st.markdown("### 🎯 Cele Scenariusza")
    
    if scenario_id:
        scenario = get_scenario("fmcg", scenario_id)
        objectives = bg_data.get("scenario_objectives", [])
        completed = bg_data.get("objectives_completed", [])
        
        if objectives:
            for i, obj in enumerate(objectives):
                is_completed = i in completed
                icon = "✅" if is_completed else "⏳"
                progress_color = "#10b981" if is_completed else "#f59e0b"
                
                st.markdown(f"""
                <div style='background: white; padding: 16px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid {progress_color};'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <strong>{icon} {obj['description']}</strong>
                        </div>
                        <div style='color: {progress_color}; font-weight: 700;'>
                            {obj.get('reward_money', 0):,} PLN
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Brak celów dla tego scenariusza.")
    else:
        st.info("Tryb swobodny - brak celów scenariusza.")
    
    st.markdown("---")
    
    # 📊 POSTĘP KARIERY
    st.markdown("### 📈 Postęp Kariery")
    
    level_info = FMCG_LEVELS[level]
    next_level = level + 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        html = f"""<div class='game-card'>
<h4 style='margin-top:0;'>💼 Obecna Pozycja</h4>
<p style='font-size: 18px; font-weight: 700; color: #8b5cf6;'>{career['title']}</p>
<p style='opacity: 0.8;'>Poziom {level}/10</p>
<p style='font-size: 13px; margin-top: 12px;'><strong>Obowiązki:</strong></p>
<ul style='font-size: 12px; opacity: 0.9;'>
{"".join([f"<li>{resp}</li>" for resp in level_info['responsibilities'][:3]])}
</ul>
</div>"""
        st.markdown(html, unsafe_allow_html=True)
    
    with col2:
        if next_level <= 10:
            next_level_info = FMCG_LEVELS[next_level]
            required = next_level_info['required_metrics']
            
            # Oblicz progress
            sales_progress = min(100, (metrics.get('monthly_sales', 0) / required.get('monthly_sales', 1)) * 100) if 'monthly_sales' in required else 0
            share_progress = min(100, (metrics.get('market_share', 0) / required.get('market_share', 1)) * 100) if 'market_share' in required else 0
            csat_progress = min(100, (metrics.get('customer_satisfaction', 0) / required.get('customer_satisfaction', 1)) * 100) if 'customer_satisfaction' in required else 0
            
            # Zbuduj HTML (bez wcięć!)
            html = f"""<div class='game-card'>
<h4 style='margin-top:0;'>🎯 Następny Poziom</h4>
<p style='font-size: 18px; font-weight: 700; color: #10b981;'>{next_level_info['role']}</p>
<p style='opacity: 0.8;'>Poziom {next_level}/10</p>
<p style='font-size: 13px; margin-top: 12px;'><strong>Wymagania:</strong></p>
<div style='margin-top: 8px;'>
<div style='font-size: 12px; margin-bottom: 4px;'>💰 Sprzedaż: {metrics.get('monthly_sales', 0):,.0f} / {required.get('monthly_sales', 0):,.0f} PLN</div>
<div style='background: #e2e8f0; border-radius: 4px; height: 6px;'>
<div style='background: #f59e0b; height: 100%; width: {sales_progress}%; border-radius: 4px;'></div>
</div>
<div style='font-size: 12px; margin-bottom: 4px; margin-top: 8px;'>📊 Market Share: {metrics.get('market_share', 0):.1f}% / {required.get('market_share', 0)}%</div>
<div style='background: #e2e8f0; border-radius: 4px; height: 6px;'>
<div style='background: #8b5cf6; height: 100%; width: {share_progress}%; border-radius: 4px;'></div>
</div>
<div style='font-size: 12px; margin-bottom: 4px; margin-top: 8px;'>⭐ CSAT: {metrics.get('customer_satisfaction', 0)}% / {required.get('customer_satisfaction', 0)}%</div>
<div style='background: #e2e8f0; border-radius: 4px; height: 6px;'>
<div style='background: #10b981; height: 100%; width: {csat_progress}%; border-radius: 4px;'></div>
</div>
</div>
</div>"""
            
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.success("🏆 Osiągnąłeś najwyższy poziom - Chief Sales Officer!")


def show_fmcg_tasks_tab(username, user_data, industry_id):
    """Zadania - dostępne zadania do wykonania"""
    from data.industries.fmcg_tasks import get_random_tasks, get_task_by_id
    
    bg_data = user_data["business_games"][industry_id]
    career = bg_data["career"]
    metrics = bg_data["metrics"]
    level = career["level"]
    
    # Pobierz zadania
    active_tasks = bg_data.get("tasks", {}).get("active", [])
    available_pool = bg_data.get("tasks", {}).get("available_pool", [])
    
    if not available_pool or len(available_pool) < 5:
        # Wygeneruj 6 losowych zadań dla poziomu
        new_tasks = get_random_tasks(level, count=6)
        
        # Zapisz do bg_data
        if "tasks" not in bg_data:
            bg_data["tasks"] = {"active": [], "completed": [], "available_pool": []}
        bg_data["tasks"]["available_pool"] = new_tasks
        
        # Zapisz do user_data
        from data.users_new import save_single_user
        save_single_user(username, user_data)
        
        # Odśwież available_pool ze zapisanych danych (bez rerun!)
        available_pool = new_tasks
    
    # =============================================================================
    # AKTYWNE ZADANIA
    # =============================================================================
    if active_tasks:
        st.markdown("### ⚡ Aktywne Zadania")
        st.markdown("Twoje bieżące zadania. Kliknij 'Wykonaj' aby je rozwiązać.")
        
        for task_id in active_tasks:
            task = get_task_by_id(task_id)
            if not task:
                continue
            
            # Mapowanie kategorii
            category_config = {
                "field_sales": {"emoji": "🚗", "color": "#3b82f6", "name": "Sprzedaż w Terenie"},
                "key_accounts": {"emoji": "🏢", "color": "#8b5cf6", "name": "Key Accounts"},
                "team_management": {"emoji": "👥", "color": "#10b981", "name": "Zarządzanie Zespołem"},
                "trade_marketing": {"emoji": "📊", "color": "#f59e0b", "name": "Trade Marketing"},
                "strategy": {"emoji": "🎯", "color": "#ec4899", "name": "Strategia"},
                "crisis": {"emoji": "⚠️", "color": "#ef4444", "name": "Kryzys"}
            }
            cat_info = category_config.get(task["category"], {"emoji": "📋", "color": "#64748b", "name": task["category"]})
            
            with st.expander(f"{cat_info['emoji']} **{task['title']}** - {cat_info['name']}", expanded=False):
                st.markdown(f"**Sytuacja:**")
                st.markdown(task['scenario'])
                
                st.markdown("---")
                st.markdown("**💡 Jak chcesz rozwiązać to zadanie?**")
                
                solution = st.text_area(
                    "Twoje rozwiązanie:",
                    placeholder="Opisz swoje podejście do rozwiązania tego zadania (min. 50 znaków)...",
                    key=f"solution_{task_id}",
                    height=150
                )
                
                col_submit, col_cancel = st.columns([1, 1])
                
                with col_submit:
                    if st.button("✅ Wyślij rozwiązanie", key=f"submit_{task_id}", use_container_width=True):
                        if len(solution.strip()) < 50:
                            st.error("⚠️ Rozwiązanie musi mieć co najmniej 50 znaków!")
                        else:
                            # WYKONAJ ZADANIE
                            # Podstawowa ocena jakości (bez AI - na podstawie długości)
                            quality_score = min(1.0, len(solution.strip()) / 200)  # Max 1.0 przy 200+ znakach
                            
                            # Oblicz nagrody z modyfikatorem jakości (FMCG uses direct keys)
                            actual_sales = int(task.get('sales_impact', 0) * quality_score)
                            actual_share = task.get('reputation_impact', 0) * quality_score
                            actual_csat = task.get('satisfaction_impact', 0) * quality_score  # if exists
                            actual_money = int(task.get('base_reward', 0) * quality_score)
                            
                            # Aktualizuj metryki
                            metrics['monthly_sales'] = metrics.get('monthly_sales', 0) + actual_sales
                            metrics['market_share'] = min(100, metrics.get('market_share', 0) + actual_share)
                            if actual_csat > 0:
                                metrics['customer_satisfaction'] = min(100, metrics.get('customer_satisfaction', 0) + actual_csat)
                            
                            # Aktualizuj finanse (jeśli istnieją)
                            if 'finances' in bg_data:
                                bg_data['finances']['cash'] = bg_data['finances'].get('cash', 0) + actual_money
                            
                            # Przenieś zadanie do completed
                            bg_data["tasks"]["active"].remove(task_id)
                            if "completed" not in bg_data["tasks"]:
                                bg_data["tasks"]["completed"] = []
                            bg_data["tasks"]["completed"].append({
                                "task_id": task_id,
                                "solution": solution,
                                "quality_score": quality_score,
                                "rewards_earned": {
                                    "sales": actual_sales,
                                    "market_share": actual_share,
                                    "csat": actual_csat,
                                    "money": actual_money
                                }
                            })
                            
                            # Sprawdź cele scenariusza
                            scenario_id = bg_data.get("scenario_id")
                            if scenario_id:
                                objectives = bg_data.get("scenario_objectives", [])
                                completed_objectives = bg_data.get("objectives_completed", [])
                                
                                for idx, obj in enumerate(objectives):
                                    if idx not in completed_objectives:
                                        # Sprawdź warunki
                                        completed = True
                                        if 'required_sales' in obj and metrics.get('monthly_sales', 0) < obj['required_sales']:
                                            completed = False
                                        if 'required_market_share' in obj and metrics.get('market_share', 0) < obj['required_market_share']:
                                            completed = False
                                        if 'required_tasks' in obj and len(bg_data["tasks"]["completed"]) < obj['required_tasks']:
                                            completed = False
                                        
                                        if completed:
                                            completed_objectives.append(idx)
                                            # Dodaj nagrodę za cel
                                            if 'reward_money' in obj:
                                                if 'finances' in bg_data:
                                                    bg_data['finances']['cash'] = bg_data['finances'].get('cash', 0) + obj['reward_money']
                                
                                bg_data["objectives_completed"] = completed_objectives
                            
                            # Sprawdź awans
                            from data.industries.fmcg import can_advance_to_next_level, get_career_stage, CAREER_LEVELS as FMCG_LEVELS
                            career_stage = get_career_stage(career['level'])
                            can_advance, advance_reason = can_advance_to_next_level(career['level'], metrics, career_stage)
                            
                            # Zapisz BEZPOŚREDNIO do JSON (workaround dla repository bug)
                            import json
                            users_file = "users_data.json"
                            with open(users_file, "r", encoding="utf-8") as f:
                                all_users = json.load(f)
                            all_users[username] = user_data
                            with open(users_file, "w", encoding="utf-8") as f:
                                json.dump(all_users, f, ensure_ascii=False, indent=2)
                            
                            # Pokaż rezultat
                            st.success(f"✅ Zadanie wykonane!")
                            st.balloons()
                            
                            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
                            with col_r1:
                                st.metric("💰 Sprzedaż", f"+{actual_sales:,} PLN")
                            with col_r2:
                                st.metric("📊 Market Share", f"+{actual_share:.1f}%")
                            with col_r3:
                                st.metric("⭐ CSAT", f"+{actual_csat:.0f}%")
                            with col_r4:
                                st.metric("💵 Gotówka", f"+{actual_money:,} PLN")
                            
                            if can_advance:
                                next_level = career['level'] + 1
                                next_role = FMCG_LEVELS[next_level]['role']
                                st.success(f"🎉 Gratulacje! Możesz awansować na: **{next_role}**!")
                            
                            st.rerun()
                
                with col_cancel:
                    if st.button("❌ Anuluj zadanie", key=f"cancel_{task_id}", use_container_width=True):
                        # Usuń z aktywnych, dodaj z powrotem do available_pool
                        bg_data["tasks"]["active"].remove(task_id)
                        
                        # Dodaj pełny obiekt zadania z powrotem do available_pool
                        bg_data["tasks"]["available_pool"].append(task)
                        
                        # Zapisz BEZPOŚREDNIO do JSON (workaround dla repository bug)
                        import json
                        users_file = "users_data.json"
                        with open(users_file, "r", encoding="utf-8") as f:
                            all_users = json.load(f)
                        all_users[username] = user_data
                        with open(users_file, "w", encoding="utf-8") as f:
                            json.dump(all_users, f, ensure_ascii=False, indent=2)
                        
                        st.warning(f"⚠️ Anulowano zadanie: {task['title']}")
                        st.rerun()
        
        st.markdown("---")
    
    # =============================================================================
    # DOSTĘPNE ZADANIA
    # =============================================================================
    st.markdown("### 💼 Dostępne Zadania")
    st.markdown("Wybierz zadanie aby je zaakceptować. Możesz mieć maksymalnie 3 aktywne zadania jednocześnie.")
    
    # Wyświetl ile aktywnych zadań ma użytkownik
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.metric("Aktywne zadania", f"{len(active_tasks)}/3")
    with col_info2:
        st.metric("Dostępne zadania", len(available_pool))
    
    st.markdown("---")
    
    # Mapowanie kategorii i trudności (wspólne dla wszystkich zadań)
    category_config = {
        "field_sales": {"emoji": "🚗", "color": "#3b82f6", "name": "Sprzedaż w Terenie"},
        "key_accounts": {"emoji": "🏢", "color": "#8b5cf6", "name": "Key Accounts"},
        "team_management": {"emoji": "👥", "color": "#10b981", "name": "Zarządzanie Zespołem"},
        "trade_marketing": {"emoji": "📊", "color": "#f59e0b", "name": "Trade Marketing"},
        "strategy": {"emoji": "🎯", "color": "#ec4899", "name": "Strategia"},
        "crisis": {"emoji": "⚠️", "color": "#ef4444", "name": "Kryzys"}
    }
    
    difficulty_config = {
        "easy": {"label": "Łatwe", "color": "#10b981"},
        "medium": {"label": "Średnie", "color": "#f59e0b"},
        "hard": {"label": "Trudne", "color": "#ef4444"}
    }
    
    # Filtruj available_pool - usuń zadania które są już aktywne (fix dla duplikatów)
    available_pool_filtered = [t for t in available_pool if t['id'] not in active_tasks]
    
    # Wyświetl zadania w gridzie 2 kolumny
    for i in range(0, len(available_pool_filtered), 2):
        col1, col2 = st.columns(2)
        
        # Zadanie 1
        with col1:
            if i < len(available_pool_filtered):
                task = available_pool_filtered[i]  # available_pool zawiera pełne obiekty zadań, nie ID!
                
                if task:
                    cat_info = category_config.get(task["category"], {"emoji": "📋", "color": "#64748b", "name": task["category"]})
                    diff_info = difficulty_config.get(task["difficulty"], {"label": "?", "color": "#64748b"})
                    
                    html = f"""<div class='game-card' style='border-left: 4px solid {cat_info['color']}; min-height: 280px;'>
<div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
<div>
<span style='font-size: 20px;'>{cat_info['emoji']}</span>
<span style='font-size: 13px; color: {cat_info['color']}; font-weight: 600; margin-left: 8px;'>{cat_info['name']}</span>
</div>
<span style='background: {diff_info['color']}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 700;'>{diff_info['label']}</span>
</div>
<h4 style='margin: 8px 0; font-size: 16px; line-height: 1.4;'>{task['title']}</h4>
<p style='font-size: 13px; opacity: 0.8; margin: 12px 0; line-height: 1.5;'>{task['scenario'][:120]}...</p>
<div style='margin-top: 16px; padding-top: 12px; border-top: 1px solid #e2e8f0;'>
<div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>
<strong>Nagrody:</strong>
</div>
<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 11px;'>
<div>💰 Sprzedaż: +{task.get('sales_impact', 0):,} PLN</div>
<div>📊 Market Share: +{task.get('reputation_impact', 0)}%</div>
<div>💵 Gotówka: +{task.get('base_reward', 0):,} PLN</div>
<div>⏱️ Czas: {task.get('time_days', 1)} dni</div>
</div>
</div>
</div>"""
                    
                    st.markdown(html, unsafe_allow_html=True)
                    
                    # Przycisk akceptacji
                    can_accept = len(active_tasks) < 3
                    if can_accept:
                        if st.button(f"✅ Akceptuj zadanie", key=f"accept_{task['id']}", use_container_width=True):
                            # Sprawdź czy zadanie już nie jest w active (fix dla duplikatów)
                            if task['id'] not in bg_data["tasks"]["active"]:
                                # Dodaj do aktywnych zadań (tylko ID!)
                                bg_data["tasks"]["active"].append(task['id'])
                                
                                # Usuń z available_pool - znajdź zadanie po ID i usuń
                                bg_data["tasks"]["available_pool"] = [
                                    t for t in bg_data["tasks"]["available_pool"] 
                                    if t['id'] != task['id']
                                ]
                                
                                # Zapisz BEZPOŚREDNIO do JSON (workaround dla repository bug)
                                import json
                                users_file = "users_data.json"
                                with open(users_file, "r", encoding="utf-8") as f:
                                    all_users = json.load(f)
                                all_users[username] = user_data
                                with open(users_file, "w", encoding="utf-8") as f:
                                    json.dump(all_users, f, ensure_ascii=False, indent=2)
                                
                                st.success(f"✅ Zaakceptowano zadanie: {task['title']}")
                            st.rerun()
                    else:
                        st.button("❌ Limit aktywnych zadań (3/3)", key=f"limit_{task['id']}", disabled=True, use_container_width=True)
        
        # Zadanie 2
        with col2:
            if i+1 < len(available_pool_filtered):
                task = available_pool_filtered[i+1]  # available_pool zawiera pełne obiekty zadań, nie ID!
                
                if task:
                    cat_info = category_config.get(task["category"], {"emoji": "📋", "color": "#64748b", "name": task["category"]})
                    diff_info = difficulty_config.get(task["difficulty"], {"label": "?", "color": "#64748b"})
                    
                    html = f"""<div class='game-card' style='border-left: 4px solid {cat_info['color']}; min-height: 280px;'>
<div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
<div>
<span style='font-size: 20px;'>{cat_info['emoji']}</span>
<span style='font-size: 13px; color: {cat_info['color']}; font-weight: 600; margin-left: 8px;'>{cat_info['name']}</span>
</div>
<span style='background: {diff_info['color']}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 700;'>{diff_info['label']}</span>
</div>
<h4 style='margin: 8px 0; font-size: 16px; line-height: 1.4;'>{task['title']}</h4>
<p style='font-size: 13px; opacity: 0.8; margin: 12px 0; line-height: 1.5;'>{task.get('description', task['scenario'][:120])}...</p>
<div style='margin-top: 16px; padding-top: 12px; border-top: 1px solid #e2e8f0;'>
<div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>
<strong>Nagrody:</strong>
</div>
<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 11px;'>
<div>💰 Sprzedaż: +{task.get('sales_impact', 0):,} PLN</div>
<div>📊 Market Share: +{task.get('reputation_impact', 0)}%</div>
<div>💵 Gotówka: +{task.get('base_reward', 0):,} PLN</div>
<div>⏱️ Czas: {task.get('time_days', 1)} dni</div>
</div>
</div>
</div>"""
                    
                    st.markdown(html, unsafe_allow_html=True)
                    
                    can_accept = len(active_tasks) < 3
                    if can_accept:
                        if st.button(f"✅ Akceptuj zadanie", key=f"accept_{task['id']}", use_container_width=True):
                            # Sprawdź czy zadanie już nie jest w active (fix dla duplikatów)
                            if task['id'] not in bg_data["tasks"]["active"]:
                                # Dodaj do aktywnych zadań (tylko ID!)
                                bg_data["tasks"]["active"].append(task['id'])
                                
                                # Usuń z available_pool - znajdź zadanie po ID i usuń
                                bg_data["tasks"]["available_pool"] = [
                                    t for t in bg_data["tasks"]["available_pool"] 
                                    if t['id'] != task['id']
                                ]
                                
                                # Zapisz BEZPOŚREDNIO do JSON (workaround dla repository bug)
                                import json
                                users_file = "users_data.json"
                                with open(users_file, "r", encoding="utf-8") as f:
                                    all_users = json.load(f)
                                all_users[username] = user_data
                                with open(users_file, "w", encoding="utf-8") as f:
                                    json.dump(all_users, f, ensure_ascii=False, indent=2)
                                
                                st.success(f"✅ Zaakceptowano zadanie: {task['title']}")
                            st.rerun()
                            
                            st.success(f"✅ Zaakceptowano zadanie: {task['title']}")
                            st.rerun()
                    else:
                        st.button("❌ Limit aktywnych zadań (3/3)", key=f"limit_{task['id']}", disabled=True, use_container_width=True)


def show_fmcg_onboarding(username, user_data, industry_id):
    """Onboarding FMCG - prezentacja firmy i wybór klientów docelowych"""
    from data.industries.fmcg_company import COMPANY_INFO, PRODUCT_PORTFOLIO, get_company_pitch
    from data.industries.fmcg_customers import get_customers_by_segment, get_segment_info
    
    bg_data = user_data["business_games"][industry_id]
    
    st.markdown("# 🎯 Witaj w FreshLife Poland!")
    
    st.markdown(f"""
### Gratulacje! Zaczynasz karierę jako **{bg_data['career']['title']}**

Przed Tobą długa droga od przedstawiciela handlowego do Chief Sales Officer.
Ale najpierw - poznaj firmę i wybierz swoich pierwszych klientów!
""")
    
    # KROK 1: Poznaj FreshLife
    st.markdown("---")
    st.markdown("## 📋 Krok 1: Poznaj FreshLife Poland")
    
    with st.expander("🏢 O firmie", expanded=True):
        st.markdown(f"""
**{COMPANY_INFO['full_name']}**
        
{COMPANY_INFO['description']}

**Nasza misja:** {COMPANY_INFO['mission']}

**Wartości:**
""")
        for value in COMPANY_INFO['values']:
            st.markdown(f"• {value}")
        
        st.markdown(f"""
**Pozycja rynkowa:**
• Personal Care: {COMPANY_INFO['market_position']['personal_care']}
• Food: {COMPANY_INFO['market_position']['food']}
• Home Care: {COMPANY_INFO['market_position']['home_care']}
""")
    
    # KROK 2: Portfolio produktów
    st.markdown("## 📦 Krok 2: Poznaj nasze produkty")
    
    tab_pc, tab_food, tab_hc = st.tabs(["🧴 Personal Care", "🍽️ Food", "🏠 Home Care"])
    
    with tab_pc:
        category = PRODUCT_PORTFOLIO['personal_care']
        st.markdown(f"**{category['category_name']}** - {category['description']}")
        st.markdown(f"*Market share: {category['market_share']}%*")
        
        for product in category['products']:
            with st.expander(f"{product['name']} - {product['subcategory']}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**USP:** {product['usp']}")
                    st.markdown(f"**Warianty:** {', '.join(product['variants'])}")
                    st.markdown(f"**Target:** {product['target_group']}")
                with col2:
                    st.metric("Cena", product['price_range'])
                    st.metric("Marża", f"{product['margin_percent']}%")
                    st.metric("Potencjał", product['volume_potential'])
    
    with tab_food:
        category = PRODUCT_PORTFOLIO['food']
        st.markdown(f"**{category['category_name']}** - {category['description']}")
        st.markdown(f"*Market share: {category['market_share']}%*")
        
        for product in category['products']:
            with st.expander(f"{product['name']} - {product['subcategory']}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**USP:** {product['usp']}")
                    st.markdown(f"**Warianty:** {', '.join(product['variants'])}")
                with col2:
                    st.metric("Cena", product['price_range'])
                    st.metric("Marża", f"{product['margin_percent']}%")
    
    with tab_hc:
        category = PRODUCT_PORTFOLIO['home_care']
        st.markdown(f"**{category['category_name']}** - {category['description']}")
        st.markdown(f"*Market share: {category['market_share']}%*")
        
        for product in category['products']:
            with st.expander(f"{product['name']} - {product['subcategory']}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**USP:** {product['usp']}")
                    st.markdown(f"**Warianty:** {', '.join(product['variants'])}")
                with col2:
                    st.metric("Cena", product['price_range'])
                    st.metric("Marża", f"{product['margin_percent']}%")
    
    # KROK 3: Wybór targetu
    st.markdown("---")
    st.markdown("## 🎯 Krok 3: Wybierz swoich pierwszych klientów")
    
    st.info("""
💡 **Ważne:** Na początek skup się na **Traditional Trade** (sklepy osiedlowe, kioski).
To najłatwiejszy segment do zdobycia pierwszych klientów.

Wybierz **2-3 sklepy** które chcesz pozyskać jako pierwsze.
""")
    
    # Lista klientów Traditional Trade
    customers = get_customers_by_segment("traditional_trade")
    
    st.markdown("### Dostępni klienci:")
    
    # Session state dla wyborów
    if 'selected_customers' not in st.session_state:
        st.session_state.selected_customers = []
    
    for customer in customers:
        with st.expander(f"🏪 {customer['name']} - {customer['location']} (Potencjał: {customer['potential_monthly']:,} PLN/mies)"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(customer['description'])
                
                st.markdown(f"""
**Charakterystyka:**
• Obrót: {customer['characteristics']['monthly_revenue']}
• Klienci/dzień: {customer['characteristics']['customers_per_day']}
• Konkurencja: {customer['characteristics']['competition']}

**Co ich boli:**
""")
                for pain in customer['pain_points']:
                    st.markdown(f"• {pain}")
                
                st.markdown("**Szanse:**")
                for opp in customer['opportunities']:
                    st.markdown(f"• {opp}")
            
            with col2:
                # Checkbox do wyboru
                is_selected = customer['id'] in st.session_state.selected_customers
                if st.checkbox(
                    "Wybierz",
                    value=is_selected,
                    key=f"select_{customer['id']}"
                ):
                    if customer['id'] not in st.session_state.selected_customers:
                        st.session_state.selected_customers.append(customer['id'])
                else:
                    if customer['id'] in st.session_state.selected_customers:
                        st.session_state.selected_customers.remove(customer['id'])
    
    # Przycisk zakończenia onboardingu
    st.markdown("---")
    
    selected_count = len(st.session_state.selected_customers)
    
    if selected_count < 2:
        st.warning(f"⚠️ Wybierz przynajmniej 2 klientów ({selected_count}/2)")
    elif selected_count > 3:
        st.warning(f"⚠️ Na początek maksymalnie 3 klientów ({selected_count}/3)")
    else:
        st.success(f"✅ Wybrano {selected_count} klientów. Możesz rozpocząć!")
        
        if st.button("🚀 Rozpocznij pracę z wybranymi klientami", type="primary", use_container_width=True):
            # Zapisz wybór i oznacz onboarding jako ukończony
            bg_data["customers"]["selected_targets"] = st.session_state.selected_customers
            bg_data["customers"]["prospects"] = st.session_state.selected_customers.copy()
            bg_data["customers"]["onboarding_completed"] = True
            
            # Inicjalizuj conversation history dla każdego klienta
            for customer_id in st.session_state.selected_customers:
                bg_data["conversations"][customer_id] = []
            
            # Zapisz
            import json
            users_file = "users_data.json"
            with open(users_file, "r", encoding="utf-8") as f:
                all_users = json.load(f)
            all_users[username] = user_data
            with open(users_file, "w", encoding="utf-8") as f:
                json.dump(all_users, f, ensure_ascii=False, indent=2)
            
            st.success("✅ Świetnie! Przekierowuję do panelu klientów...")
            st.rerun()


def show_fmcg_customers_tab(username, user_data, industry_id):
    """Tab Klienci - lista klientów, umów spotkania, historia"""
    from data.industries.fmcg_customers import get_customer_by_id
    
    bg_data = user_data["business_games"][industry_id]
    customers_data = bg_data.get("customers", {})
    
    # Sprawdź czy jest aktywna rozmowa
    if st.session_state.get('fmcg_conversation_active', False):
        customer_id = st.session_state.get('fmcg_conversation_customer')
        customer = get_customer_by_id(customer_id)
        
        if customer:
            render_fmcg_customer_conversation(customer, username, user_data, bg_data, industry_id)
            return
        else:
            # Błąd - reset
            st.session_state.fmcg_conversation_active = False
            st.rerun()
    
    st.markdown("# 👥 Moi Klienci")
    
    # Podsumowanie
    prospects = customers_data.get("prospects", [])
    active = customers_data.get("active_clients", [])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Prospects", len(prospects))
    with col2:
        st.metric("✅ Aktywni", len(active))
    with col3:
        total_potential = sum(
            get_customer_by_id(c_id).get('potential_monthly', 0) 
            for c_id in prospects + active
        )
        st.metric("💰 Potencjał", f"{total_potential:,} PLN/mies")
    
    st.markdown("---")
    
    # Lista prospects
    if prospects:
        st.markdown("## 🎯 Prospects (w trakcie pozyskiwania)")
        
        for customer_id in prospects:
            customer = get_customer_by_id(customer_id)
            if not customer:
                continue
            
            with st.expander(f"🏪 {customer['name']} - {customer['location']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Właściciel:** {customer['owner']}")
                    st.markdown(f"**Typ:** {customer['type']}")
                    st.markdown(f"**Potencjał:** {customer['potential_monthly']:,} PLN/miesiąc")
                    
                    # Historia rozmów
                    conversations = bg_data.get("conversations", {}).get(customer_id, [])
                    if conversations:
                        st.markdown(f"**Spotkań:** {len(conversations)}")
                        last_conv = conversations[-1]
                        st.markdown(f"**Ostatnie:** {last_conv.get('date', 'brak daty')}")
                
                with col2:
                    st.markdown("###")
                    if st.button("📞 Umów spotkanie", key=f"meeting_{customer_id}", use_container_width=True):
                        # Otwórz conversation
                        st.session_state.fmcg_conversation_customer = customer_id
                        st.session_state.fmcg_conversation_active = True
                        st.rerun()
    
    # Lista aktywnych
    if active:
        st.markdown("## ✅ Aktywni Klienci")
        st.info("🚧 Lista aktywnych klientów - wkrótce!")
    
    # Jeśli brak klientów
    if not prospects and not active:
        st.warning("Nie masz jeszcze żadnych klientów. Wróć do onboardingu i wybierz klientów!")


def render_fmcg_customer_conversation(customer, username, user_data, bg_data, industry_id):
    """Renderuje rozmowę z klientem FMCG - wykorzystuje AI Conversation Engine"""
    from data.industries.fmcg_conversations import build_conversation_prompt
    from datetime import datetime
    import google.generativeai as genai
    import os
    
    customer_id = customer['id']
    
    # Nagłówek
    st.markdown(f"""
<div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
            color: white; padding: 24px; border-radius: 16px; margin-bottom: 24px;'>
    <h2 style='margin: 0 0 8px 0;'>🏪 Spotkanie: {customer['name']}</h2>
    <p style='margin: 0; opacity: 0.9; font-size: 14px;'>Właściciel: {customer['owner']} | {customer['location']}</p>
</div>
""", unsafe_allow_html=True)
    
    # Pobierz historię rozmów
    conversation_history = bg_data.get("conversations", {}).get(customer_id, [])
    
    # Informacja o historii
    if conversation_history:
        st.info(f"📋 Spotkanie #{len(conversation_history) + 1} z {customer['owner']}")
    else:
        st.info(f"🆕 Pierwsze spotkanie z {customer['owner']} - czas na prospecting!")
    
    # Historia wiadomości (przechowujemy w session_state)
    if f'fmcg_conv_messages_{customer_id}' not in st.session_state:
        st.session_state[f'fmcg_conv_messages_{customer_id}'] = []
    
    messages = st.session_state[f'fmcg_conv_messages_{customer_id}']
    
    # Current turn - liczba wiadomości gracza (do klucza text_area)
    player_messages_count = len([m for m in messages if m['role'] == 'player'])
    current_turn = player_messages_count + 1
    
    # Wyświetl historię rozmowy
    st.markdown("### 💬 Rozmowa")
    
    for msg in messages:
        if msg['role'] == 'player':
            st.markdown(f"""
<div style='background: #e0f2fe; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #0284c7;'>
    <strong>🎯 Ty:</strong><br>{msg['content']}
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div style='background: #f3f4f6; padding: 12px; border-radius: 8px; margin: 8px 0; border-left: 4px solid #6b7280;'>
    <strong>🏪 {customer['owner']}:</strong><br>{msg['content']}
</div>
""", unsafe_allow_html=True)
    
    # Pole wpisywania wiadomości
    st.markdown("---")
    
    # === SPEECH-TO-TEXT INTERFACE (jak w kontraktach conversation) ===
    st.markdown("**🎤 Nagraj** (wielokrotnie, jeśli chcesz) **lub ✍️ pisz bezpośrednio w polu poniżej:**")
    
    # Klucze dla transkrypcji i wersjonowania
    transcription_key = f"fmcg_transcription_{customer_id}"
    transcription_version_key = f"fmcg_transcription_version_{customer_id}"
    last_audio_hash_key = f"fmcg_last_audio_hash_{customer_id}"
    
    # Inicjalizacja (setdefault nie powoduje re-render jeśli klucz już istnieje!)
    st.session_state.setdefault(transcription_key, "")
    st.session_state.setdefault(transcription_version_key, 0)
    st.session_state.setdefault(last_audio_hash_key, None)
    
    audio_data = st.audio_input(
        "🎤 Nagrywanie...",
        key=f"audio_input_fmcg_{customer_id}_{current_turn}"
    )
    
    # Przetwarzanie nagrania audio (tylko jeśli to NOWE nagranie!)
    if audio_data is not None:
        import hashlib
        
        # Oblicz hash audio aby wykryć duplikaty
        audio_bytes = audio_data.getvalue()
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        
        # Sprawdź czy to to samo nagranie co poprzednio
        if audio_hash != st.session_state[last_audio_hash_key]:
            # NOWE nagranie - przetwarzaj!
            st.session_state[last_audio_hash_key] = audio_hash
            
            import speech_recognition as sr
            import tempfile
            import os
            from pydub import AudioSegment
            
            with st.spinner("🤖 Rozpoznaję mowę..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        tmp_file.write(audio_bytes)
                        tmp_path = tmp_file.name
                    
                    wav_path = None
                    try:
                        audio = AudioSegment.from_file(tmp_path)
                        wav_path = tmp_path.replace(".wav", "_converted.wav")
                        audio.export(wav_path, format="wav")
                        
                        recognizer = sr.Recognizer()
                        with sr.AudioFile(wav_path) as source:
                            audio_data_sr = recognizer.record(source)
                            
                        transcription = recognizer.recognize_google(audio_data_sr, language="pl-PL")
                        
                        # Post-processing: Dodaj interpunkcję przez Gemini
                        try:
                            import google.generativeai as genai
                            
                            # Pobierz API key
                            api_key = None
                            try:
                                api_key = st.secrets["API_KEYS"]["gemini"]
                            except:
                                try:
                                    with open("config/gemini_api_key.txt", "r") as f:
                                        api_key = f.read().strip()
                                except:
                                    api_key = os.getenv("GEMINI_API_KEY")
                            
                            if api_key:
                                genai.configure(api_key=api_key)
                                model = genai.GenerativeModel("models/gemini-2.5-flash")
                                prompt = f"""Dodaj interpunkcję (kropki, przecinki, pytajniki, wykrzykniki) do poniższego tekstu.
Nie zmieniaj słów, tylko dodaj znaki interpunkcyjne. Zachowaj strukturę i podział na zdania.
Zwróć tylko poprawiony tekst, bez dodatkowych komentarzy.

Tekst do poprawy:
{transcription}"""
                                response = model.generate_content(prompt)
                                transcription_with_punctuation = response.text.strip()
                                transcription = transcription_with_punctuation
                                
                        except Exception as gemini_error:
                            # Błąd Gemini - cicho kontynuuj z surową transkrypcją
                            pass
                        
                        # DOPISZ do istniejącego tekstu (z session_state)
                        # Pobierz aktualną wartość z transcription_key (tam zapisujemy wartości)
                        existing_text = st.session_state.get(transcription_key, "")
                        
                        if existing_text.strip():
                            st.session_state[transcription_key] = existing_text.rstrip() + "\n\n" + transcription
                        else:
                            st.session_state[transcription_key] = transcription
                        
                        # Inkrementuj wersję - to wymusi re-render text_area z nową wartością!
                        st.session_state[transcription_version_key] += 1
                        
                        # Ciche działanie - brak st.info() przed rerun!
                        st.rerun()
                        
                    finally:
                        # Cleanup temp files
                        try:
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
                            if wav_path and os.path.exists(wav_path):
                                os.unlink(wav_path)
                        except:
                            pass
                            
                except sr.UnknownValueError:
                    st.session_state.fmcg_stt_error = "🎤 Nie rozpoznano mowy. Spróbuj ponownie (mów wyraźniej, bliżej mikrofonu)."
                    st.rerun()
                except sr.RequestError as e:
                    st.session_state.fmcg_stt_error = f"❌ Błąd usługi rozpoznawania mowy: {e}"
                    st.rerun()
                except Exception as e:
                    st.session_state.fmcg_stt_error = f"❌ Błąd podczas transkrypcji: {str(e)}"
                    st.rerun()
    
    # Wyświetl błędy STT (jeśli są)
    if "fmcg_stt_error" in st.session_state:
        st.warning(st.session_state.fmcg_stt_error)
        del st.session_state.fmcg_stt_error
    
    col_input, col_btn = st.columns([4, 1])
    
    with col_input:
        # Callback - synchronizuj wartość text_area z transcription_key
        def sync_textarea_to_state():
            textarea_key = f"msg_input_{customer_id}_{current_turn}_{st.session_state.get(transcription_version_key, 0)}"
            if textarea_key in st.session_state:
                st.session_state[transcription_key] = st.session_state[textarea_key]
        
        # Użyj wartości z transkrypcji jako value (+ wersja w kluczu wymusza re-render)
        player_message = st.text_area(
            "Twoja wiadomość:",
            value=st.session_state.get(transcription_key, ""),
            placeholder="Napisz co chcesz powiedzieć klientowi...",
            height=100,
            key=f"msg_input_{customer_id}_{current_turn}_{st.session_state.get(transcription_version_key, 0)}",
            on_change=sync_textarea_to_state
        )
    
    with col_btn:
        st.markdown("###")
        send_clicked = st.button("📤 Wyślij", use_container_width=True, type="primary")
        
        st.markdown("###")
        if st.button("🚪 Zakończ spotkanie", use_container_width=True):
            # Zapisz conversation do historii
            if messages:
                conversation_record = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "messages": messages.copy(),
                    "topic": "Prospecting" if not conversation_history else "Follow-up",
                    "customer_impression": "neutral"  # TODO: AI evaluation
                }
                
                if customer_id not in bg_data["conversations"]:
                    bg_data["conversations"][customer_id] = []
                bg_data["conversations"][customer_id].append(conversation_record)
                
                # Zapisz
                import json
                users_file = "users_data.json"
                with open(users_file, "r", encoding="utf-8") as f:
                    all_users = json.load(f)
                all_users[username] = user_data
                with open(users_file, "w", encoding="utf-8") as f:
                    json.dump(all_users, f, ensure_ascii=False, indent=2)
            
            # Wyczyść session state
            st.session_state.fmcg_conversation_active = False
            if f'fmcg_conv_messages_{customer_id}' in st.session_state:
                del st.session_state[f'fmcg_conv_messages_{customer_id}']
            
            # Wyczyść transkrypcję
            if transcription_key in st.session_state:
                del st.session_state[transcription_key]
            if transcription_version_key in st.session_state:
                del st.session_state[transcription_version_key]
            if last_audio_hash_key in st.session_state:
                del st.session_state[last_audio_hash_key]
            
            st.success("✅ Spotkanie zakończone!")
            st.rerun()
    
    # Wyślij wiadomość
    if send_clicked and player_message and player_message.strip():
        st.write(f"🔍 DEBUG START - player_message: {player_message[:50]}...")
        st.write(f"🔍 DEBUG - messages przed append: {len(messages)}")
        
        # Wyczyść transkrypcję po wysłaniu (jak w kontraktach conversation)
        st.session_state[transcription_key] = ""
        st.session_state[transcription_version_key] += 1
        
        # Dodaj wiadomość gracza
        messages.append({
            "role": "player",
            "content": player_message
        })
        
        
        st.write(f"🔍 DEBUG - messages po append gracza: {len(messages)}")
        
        # Przygotuj kontekst dla AI
        context = {
            "relationship_status": "prospect",  # TODO: dynamicznie
            "products_sold": [],
            "relationship_score": 0
        }
        
        # Zbuduj prompt
        prompt = build_conversation_prompt(
            customer=customer,
            conversation_history=conversation_history,
            player_message=player_message,
            context=context,
            current_messages=messages  # Przekaż bieżącą historię rozmowy
        )
        
        # Wywołaj AI
        try:
            # Konfiguracja Gemini - czytaj z secrets.toml
            api_key = None
            try:
                # Najpierw próbuj secrets.toml (bezpieczne)
                api_key = st.secrets["API_KEYS"]["GEMINI_API_KEY"]
            except:
                # Fallback - plik (deprecated)
                try:
                    with open("config/gemini_api_key.txt", "r") as f:
                        api_key = f.read().strip()
                except:
                    api_key = os.getenv("GEMINI_API_KEY")
            
            if not api_key:
                st.error("❌ Brak klucza API Gemini! Dodaj do .streamlit/secrets.toml w sekcji [API_KEYS]")
                return
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            with st.spinner(f"{customer['owner']} myśli..."):
                response = model.generate_content(prompt)
                npc_response = response.text
                
                # Dodaj odpowiedź NPC
                messages.append({
                    "role": "npc",
                    "content": npc_response
                })
                
                st.write(f"🔍 DEBUG - messages po append NPC: {len(messages)}")
                st.write(f"🔍 DEBUG - npc_response: {npc_response[:100]}...")
                st.write("🔍 DEBUG - przed rerun")
                
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Błąd AI: {str(e)}")




def show_fmcg_career_stats_tab(username, user_data, industry_id):
    """📊 Statystyki Kariery - ścieżka rozwoju, osiągnięcia, metryki"""
    from data.industries.fmcg import CAREER_LEVELS
    
    bg_data = user_data["business_games"][industry_id]
    career = bg_data["career"]
    metrics = bg_data["metrics"]
    
    current_level = career["level"]
    current_role = CAREER_LEVELS[current_level]
    next_level = current_level + 1 if current_level < len(CAREER_LEVELS) else None
    
    # Hero Card - Obecny poziom
    st.markdown(f"""
<div style='background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 30px; border-radius: 16px; color: white; margin-bottom: 24px; box-shadow: 0 10px 25px rgba(99, 102, 241, 0.3);'>
<div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>TWOJA OBECNA POZYCJA</div>
<div style='font-size: 32px; font-weight: 700; margin-bottom: 8px;'>{current_role['icon']} {current_role['role']}</div>
<div style='font-size: 16px; opacity: 0.95;'>Poziom {current_level} z {len(CAREER_LEVELS)}</div>
</div>
""", unsafe_allow_html=True)
    
    # Kluczowe metryki - 4 karty
    st.markdown(f"""
<div style='font-size: 22px; font-weight: 700; color: #1e293b; margin-bottom: 16px;'>
📈 Kluczowe Metryki
</div>
""", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_visits = len(bg_data.get("conversation_history", []))
    total_sales = metrics.get("total_sales", 0)
    avg_rating = metrics.get("average_rating", 0)
    win_rate = (metrics.get("successful_visits", 0) / max(total_visits, 1)) * 100
    
    with col1:
        st.markdown(f"""
<div style='background: white; padding: 20px; border-radius: 12px; border-left: 4px solid #10b981; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
<div style='color: #10b981; font-size: 12px; font-weight: 600; margin-bottom: 8px;'>💰 CAŁKOWITA SPRZEDAŻ</div>
<div style='font-size: 28px; font-weight: 700; color: #1e293b;'>{total_sales:,} PLN</div>
<div style='color: #64748b; font-size: 12px; margin-top: 4px;'>Łączna wartość</div>
</div>
""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
<div style='background: white; padding: 20px; border-radius: 12px; border-left: 4px solid #3b82f6; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
<div style='color: #3b82f6; font-size: 12px; font-weight: 600; margin-bottom: 8px;'>🎯 LICZBA WIZYT</div>
<div style='font-size: 28px; font-weight: 700; color: #1e293b;'>{total_visits}</div>
<div style='color: #64748b; font-size: 12px; margin-top: 4px;'>Wszystkie wizyty</div>
</div>
""", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
<div style='background: white; padding: 20px; border-radius: 12px; border-left: 4px solid #f59e0b; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
<div style='color: #f59e0b; font-size: 12px; font-weight: 600; margin-bottom: 8px;'>⭐ ŚREDNIA OCENA</div>
<div style='font-size: 28px; font-weight: 700; color: #1e293b;'>{avg_rating:.1f}/5.0</div>
<div style='color: #64748b; font-size: 12px; margin-top: 4px;'>Od klientów</div>
</div>
""", unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
<div style='background: white; padding: 20px; border-radius: 12px; border-left: 4px solid #ec4899; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
<div style='color: #ec4899; font-size: 12px; font-weight: 600; margin-bottom: 8px;'>🏆 SKUTECZNOŚĆ</div>
<div style='font-size: 28px; font-weight: 700; color: #1e293b;'>{win_rate:.0f}%</div>
<div style='color: #64748b; font-size: 12px; margin-top: 4px;'>Win rate</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 32px 0;'></div>", unsafe_allow_html=True)
    
    # Ścieżka rozwoju kariery
    st.markdown(f"""
<div style='font-size: 22px; font-weight: 700; color: #1e293b; margin-bottom: 16px;'>
🎯 Ścieżka Rozwoju Kariery
</div>
""", unsafe_allow_html=True)
    
    if next_level and next_level in CAREER_LEVELS:
        next_role = CAREER_LEVELS[next_level]
        
        # Karta następnego poziomu
        col_current, col_arrow, col_next = st.columns([2, 0.5, 2])
        
        with col_current:
            st.markdown(f"""
<div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 24px; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);'>
<div style='font-size: 12px; opacity: 0.9; margin-bottom: 8px;'>OBECNA POZYCJA ✓</div>
<div style='font-size: 24px; font-weight: 700; margin-bottom: 4px;'>{current_role['icon']} {current_role['role_short']}</div>
<div style='font-size: 13px; opacity: 0.95;'>Poziom {current_level}</div>
</div>
""", unsafe_allow_html=True)
        
        with col_arrow:
            st.markdown("""
<div style='text-align: center; padding-top: 40px;'>
<div style='font-size: 32px;'>→</div>
</div>
""", unsafe_allow_html=True)
        
        with col_next:
            st.markdown(f"""
<div style='background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 24px; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);'>
<div style='font-size: 12px; opacity: 0.9; margin-bottom: 8px;'>NASTĘPNY POZIOM 🎯</div>
<div style='font-size: 24px; font-weight: 700; margin-bottom: 4px;'>{next_role['icon']} {next_role['role_short']}</div>
<div style='font-size: 13px; opacity: 0.95;'>Poziom {next_level}</div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
        
        # Wymagania do awansu
        st.markdown("**� Wymagania do awansu:**")
        
        req_cols = st.columns(3)
        required = next_role.get("required_metrics", {})
        
        # Miesięczna sprzedaż
        monthly_sales_required = required.get("monthly_sales", 0)
        monthly_sales_current = metrics.get("monthly_sales", 0)
        monthly_progress = min((monthly_sales_current / max(monthly_sales_required, 1)) * 100, 100)
        
        with req_cols[0]:
            st.markdown(f"""
<div style='background: #f8fafc; padding: 16px; border-radius: 8px; border: 2px solid #e2e8f0;'>
<div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>💰 Miesięczna sprzedaż</div>
<div style='font-size: 20px; font-weight: 700; color: #1e293b;'>{monthly_sales_current:,} / {monthly_sales_required:,} PLN</div>
<div style='background: #e2e8f0; height: 8px; border-radius: 4px; margin-top: 8px; overflow: hidden;'>
<div style='background: linear-gradient(to right, #10b981, #059669); height: 100%; width: {monthly_progress}%;'></div>
</div>
<div style='font-size: 11px; color: #64748b; margin-top: 4px;'>{monthly_progress:.0f}% ukończone</div>
</div>
""", unsafe_allow_html=True)
        
        # Market share
        market_share_required = required.get("market_share", 0)
        market_share_current = metrics.get("market_share", 0)
        market_progress = min((market_share_current / max(market_share_required, 1)) * 100, 100)
        
        with req_cols[1]:
            st.markdown(f"""
<div style='background: #f8fafc; padding: 16px; border-radius: 8px; border: 2px solid #e2e8f0;'>
<div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>📊 Udział w rynku</div>
<div style='font-size: 20px; font-weight: 700; color: #1e293b;'>{market_share_current}% / {market_share_required}%</div>
<div style='background: #e2e8f0; height: 8px; border-radius: 4px; margin-top: 8px; overflow: hidden;'>
<div style='background: linear-gradient(to right, #3b82f6, #2563eb); height: 100%; width: {market_progress}%;'></div>
</div>
<div style='font-size: 11px; color: #64748b; margin-top: 4px;'>{market_progress:.0f}% ukończone</div>
</div>
""", unsafe_allow_html=True)
        
        # Satysfakcja klientów
        satisfaction_required = required.get("customer_satisfaction", 0)
        satisfaction_current = metrics.get("customer_satisfaction", 0)
        satisfaction_progress = min((satisfaction_current / max(satisfaction_required, 1)) * 100, 100)
        
        with req_cols[2]:
            st.markdown(f"""
<div style='background: #f8fafc; padding: 16px; border-radius: 8px; border: 2px solid #e2e8f0;'>
<div style='font-size: 12px; color: #64748b; margin-bottom: 8px;'>⭐ Satysfakcja klientów</div>
<div style='font-size: 20px; font-weight: 700; color: #1e293b;'>{satisfaction_current}% / {satisfaction_required}%</div>
<div style='background: #e2e8f0; height: 8px; border-radius: 4px; margin-top: 8px; overflow: hidden;'>
<div style='background: linear-gradient(to right, #f59e0b, #d97706); height: 100%; width: {satisfaction_progress}%;'></div>
</div>
<div style='font-size: 11px; color: #64748b; margin-top: 4px;'>{satisfaction_progress:.0f}% ukończone</div>
</div>
""", unsafe_allow_html=True)
    
    else:
        st.success("🎉 Gratulacje! Osiągnąłeś najwyższy poziom kariery!")
    
    st.markdown("<div style='margin: 32px 0;'></div>", unsafe_allow_html=True)
    
    # Wszystkie poziomy kariery - Timeline
    st.markdown(f"""
<div style='font-size: 22px; font-weight: 700; color: #1e293b; margin-bottom: 16px;'>
🏆 Wszystkie Poziomy Kariery
</div>
""", unsafe_allow_html=True)
    
    for level_num in range(1, len(CAREER_LEVELS) + 1):
        level_info = CAREER_LEVELS[level_num]
        is_current = (level_num == current_level)
        is_unlocked = (level_num <= current_level)
        
        if is_current:
            bg_color = "linear-gradient(135deg, #10b981 0%, #059669 100%)"
            text_color = "white"
            border = "none"
            opacity = "1"
        elif is_unlocked:
            bg_color = "#f8fafc"
            text_color = "#1e293b"
            border = "2px solid #10b981"
            opacity = "0.8"
        else:
            bg_color = "#f8fafc"
            text_color = "#64748b"
            border = "2px solid #e2e8f0"
            opacity = "0.6"
        
        badge = "✓ ODBLOKOWANE" if is_unlocked else "🔒 ZABLOKOWANE"
        badge_bg = "rgba(255,255,255,0.2)" if is_unlocked else "rgba(100,116,139,0.2)"
        
        st.markdown(f"""
<div style='background: {bg_color}; padding: 20px; border-radius: 12px; margin-bottom: 12px; border: {border}; opacity: {opacity};'>
<div style='display: flex; justify-content: space-between; align-items: center;'>
<div>
<div style='font-size: 24px; font-weight: 700; color: {text_color}; margin-bottom: 4px;'>{level_info['icon']} {level_info['role']}</div>
<div style='font-size: 14px; color: {text_color}; opacity: 0.9;'>{level_info['description']}</div>
</div>
<div style='background: {badge_bg}; padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; color: {text_color};'>
{badge}
</div>
</div>
</div>
""", unsafe_allow_html=True)


