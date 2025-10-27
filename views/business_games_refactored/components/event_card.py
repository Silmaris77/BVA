"""
Komponenty kart wydarzeń dla Business Games
Funkcje renderujące karty wydarzeń i ich efekty
"""

import streamlit as st


def render_active_effects_badge(active_effects: list):
    """Renderuje badge z aktywnymi efektami wydarzeń"""
    
    from datetime import datetime
    
    st.markdown("### ✨ Aktywne Efekty Wydarzenia")
    
    for effect in active_effects:
        effect_type = effect.get("type")
        expires = effect.get("expires")
        hours_left = 0
        
        # Oblicz pozostały czas
        if expires:
            expires_dt = datetime.strptime(expires, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            time_left = expires_dt - now
            hours_left = int(time_left.total_seconds() / 3600)
            
            if hours_left < 0:
                continue  # Pomiń wygasłe
        
        # Ustal emoji i opis w zależności od typu
        if effect_type == "capacity_boost":
            emoji = "🎓"
            title = f"+{effect['value']} pojemności"
            bg_color = "#f0fdf4"
            border_color = "#10b981"
            time_text = f"Wygasa za: {hours_left}h"
        elif effect_type == "capacity_penalty":
            emoji = "🤒"
            title = f"{effect['value']} pojemności"
            bg_color = "#fef2f2"
            border_color = "#ef4444"
            time_text = f"Wygasa za: {hours_left}h"
        elif effect_type == "next_contract_bonus":
            emoji = "🤝"
            title = f"+{int((effect['multiplier'] - 1) * 100)}% nagrody za następny kontrakt"
            bg_color = "#fffbeb"
            border_color = "#f59e0b"
            time_text = "Jednorazowy bonus"
        else:
            continue
        
        st.markdown(f"""
        <div style='border-left: 5px solid {border_color}; 
                    background: {bg_color};
                    padding: 12px; 
                    margin: 8px 0; 
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    gap: 12px;'>
            <span style='font-size: 24px;'>{emoji}</span>
            <div style='flex: 1;'>
                <strong>{title}</strong><br>
                <small style='color: #666;'>{time_text}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_latest_event_card(event: dict):
    """Renderuje małą kartę z najnowszym zdarzeniem na Dashboard (stara wersja)"""
    
    # Kolor w zależności od typu
    if event["type"] == "positive":
        border_color = "#10b981"
        bg_color = "#f0fdf4"
    elif event["type"] == "negative":
        border_color = "#ef4444"
        bg_color = "#fef2f2"
    else:  # neutral
        border_color = "#f59e0b"
        bg_color = "#fffbeb"
    
    st.markdown(f"""
    <div style='border-left: 5px solid {border_color}; 
                background: {bg_color};
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 8px;'>
        <div style='display: flex; align-items: center; gap: 10px;'>
            <span style='font-size: 32px;'>{event['emoji']}</span>
            <div>
                <h4 style='margin: 0;'>Ostatnie Zdarzenie: {event['title']}</h4>
                <p style='margin: 5px 0 0 0; color: #666; font-size: 14px;'>{event['timestamp']}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"💬 {event['description']}")
    
    # Dodaj informację o dotkniętym kontrakcie
    if event.get("affected_contract"):
        st.caption(f"⚠️ Dotknięty kontrakt: **{event['affected_contract']}**")
    
    # Dodaj informację o przedłużonych kontraktach
    if event.get("affected_contracts_extended"):
        contracts_list = ", ".join(event["affected_contracts_extended"])
        st.caption(f"✨ Przedłużone kontrakty: **{contracts_list}**")


def show_active_event_card(event: dict):
    """Wyświetla aktywne wydarzenie jako wyróżnioną kartę (Material Design)
    
    Args:
        event: Słownik z danymi wydarzenia (latest_event)
    """
    from utils.business_game_events import get_active_effects
    
    # Kolory w zależności od typu
    if event["type"] == "positive":
        gradient_start = "#10b981"
        gradient_end = "#059669"
        emoji_bg = "rgba(255,255,255,0.2)"
        icon = "✨"
    elif event["type"] == "negative":
        gradient_start = "#ef4444"
        gradient_end = "#dc2626"
        emoji_bg = "rgba(255,255,255,0.2)"
        icon = "⚠️"
    else:  # neutral
        gradient_start = "#f59e0b"
        gradient_end = "#d97706"
        emoji_bg = "rgba(255,255,255,0.2)"
        icon = "⚖️"
    
    # Buduj HTML z efektami
    effects_html = ""
    if event.get("effects"):
        effects = event["effects"]
        effects_items = []
        
        # Monety (SALDO FIRMY!)
        if effects.get("coins"):
            coin_value = effects["coins"]
            if coin_value > 0:
                effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>💰</span><div><strong>+{coin_value:,} PLN</strong><br><span style='font-size: 11px; opacity: 0.9;'>saldo firmy</span></div></div>")
            else:
                effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>💸</span><div><strong>{coin_value:,} PLN</strong><br><span style='font-size: 11px; opacity: 0.9;'>saldo firmy</span></div></div>")
        
        # Reputacja
        if effects.get("reputation"):
            rep_value = effects["reputation"]
            if rep_value > 0:
                effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>⭐</span><div><strong>+{rep_value}</strong><br><span style='font-size: 11px; opacity: 0.9;'>reputacji</span></div></div>")
            else:
                effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>📉</span><div><strong>{rep_value}</strong><br><span style='font-size: 11px; opacity: 0.9;'>reputacji</span></div></div>")
        
        # Bonus do kontraktu
        if effects.get("next_contract_bonus"):
            bonus_pct = int((effects["next_contract_bonus"] - 1) * 100)
            effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>🎁</span><div><strong>+{bonus_pct}%</strong><br><span style='font-size: 11px; opacity: 0.9;'>bonus nagrody</span></div></div>")
        
        # Przedłużenie deadline
        if effects.get("deadline_extension"):
            ext_hours = effects["deadline_extension"]
            effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>⏰</span><div><strong>+{ext_hours}h</strong><br><span style='font-size: 11px; opacity: 0.9;'>dodatkowy czas</span></div></div>")
        
        # Boost pojemności
        if effects.get("capacity_boost"):
            boost = effects["capacity_boost"]
            duration = effects.get("duration_days", "?")
            effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>📈</span><div><strong>+{boost}</strong><br><span style='font-size: 11px; opacity: 0.9;'>pojemność ({duration}d)</span></div></div>")
        
        # Skrócenie deadline (negatywne)
        if effects.get("deadline_reduction"):
            red_hours = effects["deadline_reduction"]
            effects_items.append(f"<div style='background: {emoji_bg}; padding: 10px 16px; border-radius: 8px; display: flex; align-items: center; gap: 8px;'><span style='font-size: 20px;'>⏱️</span><div><strong>-{red_hours}h</strong><br><span style='font-size: 11px; opacity: 0.9;'>mniej czasu</span></div></div>")
        
        if effects_items:
            effects_html = f"<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-top: 16px;'>{''.join(effects_items)}</div>"
    
    # Flavor text (jeśli istnieje)
    flavor_html = ""
    if event.get("flavor_text"):
        flavor_html = f"""<div style='background: rgba(0,0,0,0.15); border-left: 3px solid rgba(255,255,255,0.5); padding: 12px 16px; border-radius: 8px; margin-top: 16px; font-style: italic; font-size: 13px; line-height: 1.5;'>
"{event['flavor_text']}"
</div>"""
    
    # Wyświetl kartę
    event_card_html = f"""<div style="background: linear-gradient(135deg, {gradient_start} 0%, {gradient_end} 100%); color: white; border-radius: 20px; padding: 24px; margin-bottom: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);">
<div style="display: flex; align-items: start; gap: 20px; margin-bottom: 12px;">
<div style="font-size: 56px; line-height: 1;">{event['emoji']}</div>
<div>
<div style="font-size: 14px; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">{icon} Wydarzenie dnia</div>
<div style="font-size: 22px; font-weight: 700;">{event['title']}</div>
</div>
</div>
<div style="font-size: 15px; opacity: 0.95; line-height: 1.7;">{event['description']}</div>
{flavor_html}
{effects_html}
</div>"""
    
    st.markdown(event_card_html, unsafe_allow_html=True)
