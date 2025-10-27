"""
🛒 FMCG Industry Module for Business Games

Moduł branży FMCG (Fast-Moving Consumer Goods) - FreshLife Poland
Zawiera wszystkie zakładki i funkcjonalności specyficzne dla FMCG.

Wyekstrahowane z business_games.py (KROK 7 - FMCG separation)
"""

import streamlit as st
from datetime import datetime
from views.business_games_refactored.helpers import get_game_data, save_game_data

# =============================================================================
# FMCG TABS
# =============================================================================

def show_fmcg_company_info_tab(username, user_data, industry_id):
    """Zakładka z informacjami o firmie FreshLife Poland i portfolio produktów"""
    from data.industries.fmcg_company import COMPANY_INFO, PRODUCT_PORTFOLIO
    
    # Sekcja O Firmie (bez dużego nagłówka - oszczędność miejsca)
    st.markdown("## 📋 O Firmie")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
**{COMPANY_INFO['full_name']}**

{COMPANY_INFO['description']}

**Misja:** {COMPANY_INFO['mission']}
""")
    
    with col2:
        st.markdown(f"""
**📊 Dane Podstawowe**
- **Rok założenia:** {COMPANY_INFO['founded']}
- **Firma matka:** {COMPANY_INFO['parent_company']}
- **Pracownicy:** {COMPANY_INFO['employees_poland']}
- **Siedziba:** {COMPANY_INFO['hq_location']}
""")
    
    # Wartości firmy
    st.markdown("### 💎 Nasze Wartości")
    cols = st.columns(len(COMPANY_INFO['values']))
    for i, value in enumerate(COMPANY_INFO['values']):
        with cols[i]:
            st.info(f"**{value}**")
    
    # Pozycja rynkowa
    st.markdown("### 📈 Pozycja Rynkowa")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;'>
    <div style='font-size: 24px; margin-bottom: 8px;'>🧴</div>
    <div style='font-size: 14px; opacity: 0.9;'>Personal Care</div>
    <div style='font-size: 20px; font-weight: 700; margin-top: 8px;'>{COMPANY_INFO['market_position']['personal_care']}</div>
</div>
""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;'>
    <div style='font-size: 24px; margin-bottom: 8px;'>🍽️</div>
    <div style='font-size: 14px; opacity: 0.9;'>Food & Beverages</div>
    <div style='font-size: 20px; font-weight: 700; margin-top: 8px;'>{COMPANY_INFO['market_position']['food']}</div>
</div>
""", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
<div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 12px; color: white; text-align: center;'>
    <div style='font-size: 24px; margin-bottom: 8px;'>🏠</div>
    <div style='font-size: 14px; opacity: 0.9;'>Home Care</div>
    <div style='font-size: 20px; font-weight: 700; margin-top: 8px;'>{COMPANY_INFO['market_position']['home_care']}</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Portfolio Produktów
    st.markdown("## 🛍️ Portfolio Produktów")
    st.info("💡 **Wskazówka:** Zapoznaj się z naszymi produktami - przydadzą Ci się w rozmowach z klientami!")
    
    # Zakładki dla kategorii
    tab_pc, tab_food, tab_hc = st.tabs(["🧴 Personal Care", "🍽️ Food & Beverages", "🏠 Home Care"])
    
    with tab_pc:
        show_product_category(PRODUCT_PORTFOLIO['personal_care'])
    
    with tab_food:
        show_product_category(PRODUCT_PORTFOLIO['food'])
    
    with tab_hc:
        show_product_category(PRODUCT_PORTFOLIO['home_care'])


def show_product_category(category):
    """Wyświetla produkty z danej kategorii"""
    st.markdown(f"### {category['category_name']}")
    st.markdown(f"*{category['description']}*")
    st.markdown(f"**Udział w rynku:** {category['market_share']}%")
    
    st.markdown("---")
    
    for product in category['products']:
        with st.expander(f"📦 **{product['name']}** - {product['subcategory']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
**USP (Unique Selling Proposition):**  
{product['usp']}

**Warianty:**  
{', '.join(product['variants'])}

**Grupa docelowa:** {product['target_group']}

**Opakowanie:** {product['packaging']}

**Termin przydatności:** {product['shelf_life']}
""")
                
                if product.get('awards'):
                    st.markdown(f"**🏆 Nagrody:** {', '.join(product['awards'])}")
            
            with col2:
                # Kompaktowy box z danymi cenowymi - UWAGA: HTML bez wcięć!
                price_box_html = f"""<div style='background: #f8fafc; padding: 16px; border-radius: 8px; border: 2px solid #e2e8f0;'>
<div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'>Cena detaliczna</div>
<div style='font-size: 18px; font-weight: 700; color: #0f172a;'>{product["price_range"]}</div>

<div style='font-size: 12px; color: #64748b; margin-top: 12px; margin-bottom: 4px;'>Marża</div>
<div style='font-size: 18px; font-weight: 700; color: #10b981;'>{product["margin_percent"]}%</div>

<div style='font-size: 12px; color: #64748b; margin-top: 12px; margin-bottom: 4px;'>Potencjał wolumenu</div>
<div style='font-size: 16px; font-weight: 600; color: #8b5cf6;'>{product["volume_potential"].upper()}</div>
</div>"""
                st.markdown(price_box_html, unsafe_allow_html=True)


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


def show_fmcg_stats_tab(username, user_data, industry_id):
    """Statystyki Kariery - wykresy, historia, osiągnięcia"""
    st.info("🚧 Statystyki Kariery - w budowie! 🚧")
    st.write("Tutaj będą statystyki i wykresy.")

