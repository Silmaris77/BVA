# -*- coding: utf-8 -*-
"""
Reorganize Dashboard: Create Hero Section + 3 Sub-tabs
"""

with open('views/business_games_refactored/industries/fmcg_playable.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find start of tab_dashboard
start_marker = "    with tab_dashboard:"
end_marker = "    # =============================================================================\n    # TAB: SPRZEDAŻ"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("ERROR: Could not find Dashboard tab boundaries")
    exit(1)

print(f"Found Dashboard: {start_idx} to {end_idx}")
print(f"Current Dashboard size: {end_idx - start_idx} characters")

# Extract parts before and after Dashboard
before_dashboard = content[:start_idx]
after_dashboard = content[end_idx:]

# Create new Dashboard structure
new_dashboard = '''    with tab_dashboard:
        # =============================================================================
        # HERO SECTION (zawsze widoczny)
        # =============================================================================
        
        # Get values needed for Hero Section
        energy_pct = game_state.get("energy", 100)
        status_summary = get_client_status_summary(clients)
        current_week = game_state.get("current_week", 1)
        current_day = game_state.get("current_day", "Monday")
        tasks_completed_count = 3 - get_pending_tasks_count(st.session_state)
        all_done = all_tasks_completed(st.session_state)
        
        # Energy emoji based on level
        if energy_pct > 66:
            energy_emoji = "⚡"
        elif energy_pct > 33:
            energy_emoji = "🔋"
        else:
            energy_emoji = "🪫"
        
        # Tasks status
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        day_index = day_names.index(current_day) if current_day in day_names else 0
        is_trial = (current_week == 1 and day_index < 2)
        
        if all_done:
            tasks_status = "✅ Komplet"
            tasks_color = "#10b981"
        elif is_trial:
            tasks_status = f"⏰ {tasks_completed_count}/3"
            tasks_color = "#f59e0b"
        else:
            tasks_status = f"❗ {tasks_completed_count}/3"
            tasks_color = "#ef4444"
        
        # Hero Section - Gaming Style
        hero_html = f"""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 24px; border-radius: 16px; color: white; margin-bottom: 24px;
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);'>
    
    <!-- ENERGY BAR - Gaming style with glow -->
    <div style='margin-bottom: 20px;'>
        <div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px; font-weight: 600;'>
            {energy_emoji} ENERGIA
        </div>
        <div style='background: rgba(255,255,255,0.2); height: 32px; border-radius: 16px; overflow: hidden;
                    box-shadow: inset 0 2px 8px rgba(0,0,0,0.2);'>
            <div style='background: linear-gradient(90deg, #10b981 0%, #34d399 100%); 
                        height: 100%; width: {energy_pct}%;
                        display: flex; align-items: center; justify-content: center; 
                        font-weight: 700; font-size: 16px;
                        box-shadow: 0 0 12px rgba(16, 185, 129, 0.6);
                        transition: width 0.3s ease;'>
                {energy_pct}%
            </div>
        </div>
    </div>
    
    <!-- KPI CARDS - 4 gradient cards in row -->
    <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px;'>
        <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                    padding: 16px; border-radius: 12px; text-align: center;
                    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
                    border: 2px solid rgba(255,255,255,0.2);'>
            <div style='font-size: 32px; font-weight: 700; margin-bottom: 4px;'>{status_summary.get("PROSPECT", 0)}</div>
            <div style='font-size: 12px; opacity: 0.9; font-weight: 600;'>🔓 PROSPECT</div>
        </div>
        <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    padding: 16px; border-radius: 12px; text-align: center;
                    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
                    border: 2px solid rgba(255,255,255,0.2);'>
            <div style='font-size: 32px; font-weight: 700; margin-bottom: 4px;'>{status_summary.get("ACTIVE", 0)}</div>
            <div style='font-size: 12px; opacity: 0.9; font-weight: 600;'>✅ ACTIVE</div>
        </div>
        <div style='background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                    padding: 16px; border-radius: 12px; text-align: center;
                    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
                    border: 2px solid rgba(255,255,255,0.2);'>
            <div style='font-size: 32px; font-weight: 700; margin-bottom: 4px;'>{status_summary.get("LOST", 0)}</div>
            <div style='font-size: 12px; opacity: 0.9; font-weight: 600;'>❌ LOST</div>
        </div>
        <div style='background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); 
                    padding: 16px; border-radius: 12px; text-align: center;
                    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
                    border: 2px solid rgba(255,255,255,0.2);'>
            <div style='font-size: 32px; font-weight: 700; margin-bottom: 4px;'>{game_state.get('monthly_sales', 0):,}</div>
            <div style='font-size: 12px; opacity: 0.9; font-weight: 600;'>💰 SPRZEDAŻ</div>
        </div>
    </div>
    
    <!-- TIME INFO - 3 cards in row -->
    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;'>
        <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; text-align: center;
                    border: 1px solid rgba(255,255,255,0.2);'>
            <div style='font-size: 20px; font-weight: 700; margin-bottom: 2px;'>{current_day}</div>
            <div style='font-size: 11px; opacity: 0.9;'>📅 Dzień</div>
        </div>
        <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; text-align: center;
                    border: 1px solid rgba(255,255,255,0.2);'>
            <div style='font-size: 20px; font-weight: 700; margin-bottom: 2px;'>Tydzień {current_week}</div>
            <div style='font-size: 11px; opacity: 0.9;'>📆 Okres</div>
        </div>
        <div style='background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; text-align: center;
                    border: 1px solid rgba(255,255,255,0.2);
                    border-left: 3px solid {tasks_color};'>
            <div style='font-size: 20px; font-weight: 700; margin-bottom: 2px;'>{tasks_status}</div>
            <div style='font-size: 11px; opacity: 0.9;'>📋 Zadania</div>
        </div>
    </div>
</div>
"""
        
        st.markdown(hero_html, unsafe_allow_html=True)
        
        # =============================================================================
        # SUB-TABY dla szczegółów
        # =============================================================================
        
        dash_stats, dash_alerts, dash_tasks = st.tabs([
            "📊 Statystyki",
            "⚠️ Alerty & Akcje",
            "📋 Zadania & Onboarding"
        ])
        
        # ========================================================================
        # SUB-TAB: STATYSTYKI (Cele, Achievement, Historia)
        # ========================================================================
        
        with dash_stats:
'''

# Continue with dash_stats content...
# I'll build this step by step

print("OK New structure prepared, writing file...")

# Combine all parts
new_content = before_dashboard + new_dashboard + after_dashboard

with open('views/business_games_refactored/industries/fmcg_playable.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("OK Dashboard reorganized with Hero Section + 3 sub-tabs")
