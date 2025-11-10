"""
🎯 Prosty Panel Wizyty - Scenariusz Heinz

Minimalistyczny interfejs do symulacji rozmowy handlowej:
- Tylko rozmowa (bez zbędnych elementów)
- AI gra klienta
- Ocena i feedback na końcu
"""

import streamlit as st
from datetime import datetime
from typing import Optional

from scenarios.heinz_simple_visit import HeinzSimpleVisitScenario


def render_simple_visit_panel(username: str):
    """
    Renderuje prosty panel wizyty handlowej
    
    Args:
        username: Nazwa użytkownika
    """
    st.title("🎯 Wizyta Handlowa - Heinz Ketchup")
    
    # Exit button
    if st.button("← Wróć do wyboru scenariuszy", type="secondary", key="exit_simple_visit"):
        # Clear conversation state
        conv_key_pattern = "simple_visit_conversation_"
        keys_to_delete = [k for k in st.session_state.keys() if k.startswith(conv_key_pattern)]
        for k in keys_to_delete:
            del st.session_state[k]
        
        # Clear scenario
        if 'simple_scenario' in st.session_state:
            del st.session_state['simple_scenario']
        
        # Clear FMCG scenario flags (set by fmcg_playable.py)
        if 'fmcg_scenario' in st.session_state:
            del st.session_state['fmcg_scenario']
        if 'fmcg_game_initialized' in st.session_state:
            del st.session_state['fmcg_game_initialized']
        
        st.rerun()
    
    st.markdown("---")
    
    # Initialize scenario
    if 'simple_scenario' not in st.session_state:
        st.session_state.simple_scenario = HeinzSimpleVisitScenario()
    
    scenario = st.session_state.simple_scenario
    client = scenario.get_client_profile()
    
    # Initialize conversation state
    conv_key = f"simple_visit_conversation_{client['id']}"
    if conv_key not in st.session_state:
        st.session_state[conv_key] = {
            "messages": [],
            "started": False,
            "completed": False,
            "start_time": None
        }
    
    conv_state = st.session_state[conv_key]
    
    # ============================================================================
    # HEADER - Informacje o kliencie
    # ============================================================================
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"<div style='font-size: 80px; text-align: center;'>{client['avatar']}</div>", 
                       unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"### {client['name']}")
            st.markdown(f"**Właściciel:** {client['owner']}")
            st.markdown(f"**Lokalizacja:** {client['location']}")
            st.markdown(f"**Segment:** {client['segment']}")
    
    st.markdown("---")
    
    # ============================================================================
    # ROZMOWA
    # ============================================================================
    
    if not conv_state["completed"]:
        # START ROZMOWY
        if not conv_state["started"]:
            st.markdown("### 👋 Rozpocznij wizytę")
            st.info("💡 **Cel:** Przekonaj właściciela do testowego zamówienia Heinz Ketchup Premium 5kg")
            
            if st.button("🚀 Rozpocznij rozmowę", type="primary", use_container_width=True):
                # Start conversation
                conv_state["started"] = True
                conv_state["start_time"] = datetime.now().isoformat()
                
                # AI starts with greeting
                with st.spinner("Klient wita handlowca..."):
                    ai_greeting = scenario.start_conversation(client)
                
                conv_state["messages"].append({
                    "role": "assistant",
                    "content": ai_greeting,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
                st.rerun()
        
        # ROZMOWA W TOKU
        else:
            st.markdown("### 💬 Rozmowa")
            
            # Display conversation history
            for msg in conv_state["messages"]:
                if msg["role"] == "user":
                    with st.chat_message("user", avatar="🎮"):
                        st.markdown(msg["content"])
                        st.caption(f"🕐 {msg['timestamp']}")
                else:
                    with st.chat_message("assistant", avatar=client['avatar']):
                        st.markdown(f"**{client['owner']}:** {msg['content']}")
                        st.caption(f"🕐 {msg['timestamp']}")
            
            # Input area
            st.markdown("---")
            col_input, col_end = st.columns([4, 1])
            
            with col_input:
                player_message = st.text_area(
                    "Twoja wypowiedź:",
                    height=100,
                    key=f"player_input_{len(conv_state['messages'])}",
                    placeholder="Wpisz co chcesz powiedzieć klientowi..."
                )
                
                if st.button("📤 Wyślij", type="primary", use_container_width=True, 
                           disabled=not player_message.strip()):
                    if player_message.strip():
                        # Add player message
                        conv_state["messages"].append({
                            "role": "user",
                            "content": player_message,
                            "timestamp": datetime.now().strftime("%H:%M")
                        })
                        
                        # Get AI response
                        with st.spinner(f"{client['owner']} odpowiada..."):
                            ai_response = scenario.continue_conversation(
                                client=client,
                                conversation_history=conv_state["messages"],
                                player_message=player_message
                            )
                        
                        # Add AI response
                        conv_state["messages"].append({
                            "role": "assistant",
                            "content": ai_response,
                            "timestamp": datetime.now().strftime("%H:%M")
                        })
                        
                        st.rerun()
            
            with col_end:
                if st.button("🏁 Zakończ\nwizytę", type="secondary", use_container_width=True):
                    conv_state["completed"] = True
                    st.rerun()
    
    # ============================================================================
    # PODSUMOWANIE I OCENA
    # ============================================================================
    else:
        st.success("✅ Wizyta zakończona!")
        st.markdown("---")
        
        # Evaluate conversation
        st.markdown("### 📊 Ocena Rozmowy")
        
        with st.spinner("🤖 AI analizuje Twoją rozmowę..."):
            score, feedback, analysis = scenario.evaluate_conversation(
                client=client,
                conversation_history=conv_state["messages"]
            )
        
        # Display score
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Score visualization
            stars_filled = int(score / 20)  # 0-100 -> 0-5 stars
            stars = "⭐" * stars_filled + "☆" * (5 - stars_filled)
            
            st.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 30px; border-radius: 15px; text-align: center; color: white;'>
    <div style='font-size: 48px; margin-bottom: 10px;'>{stars}</div>
    <div style='font-size: 64px; font-weight: bold;'>{score}/100</div>
    <div style='font-size: 18px; opacity: 0.9; margin-top: 10px;'>WYNIK ROZMOWY</div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Breakdown
        if "breakdown" in analysis:
            st.markdown("#### 📈 Szczegółowa ocena:")
            
            breakdown = analysis["breakdown"]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("🤝 Budowanie relacji", f"{breakdown.get('building_rapport', 0)}/25")
                st.metric("🎯 Dopasowanie argumentów", f"{breakdown.get('argumentation', 0)}/25")
            
            with col2:
                st.metric("🔍 Odkrywanie potrzeb", f"{breakdown.get('discovery', 0)}/25")
                st.metric("✅ Zamknięcie", f"{breakdown.get('closing', 0)}/25")
        
        st.markdown("---")
        
        # Feedback FUKO
        st.markdown("#### 💬 Feedback od eksperta:")
        with st.container():
            st.markdown(f"""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; 
            border-left: 5px solid #667eea;'>
{feedback}
</div>
""", unsafe_allow_html=True)
        
        # Strengths & Weaknesses
        if "strengths" in analysis or "weaknesses" in analysis:
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                if "strengths" in analysis and analysis["strengths"]:
                    st.markdown("#### ✅ Mocne strony:")
                    for strength in analysis["strengths"]:
                        st.success(f"✓ {strength}")
            
            with col2:
                if "weaknesses" in analysis and analysis["weaknesses"]:
                    st.markdown("#### ⚠️ Do poprawy:")
                    for weakness in analysis["weaknesses"]:
                        st.warning(f"→ {weakness}")
        
        # Order prediction
        if "order_likely" in analysis:
            st.markdown("---")
            if analysis["order_likely"]:
                order_size = analysis.get("order_size_kg", 5)
                st.success(f"🎉 **Prawdopodobne zamówienie:** {order_size} kg Heinz Ketchup")
            else:
                st.info("📝 **Brak zamówienia** - kontynuuj budowanie relacji w kolejnych wizytach")
        
        # Next steps
        if "next_steps" in analysis:
            st.markdown("---")
            st.markdown("#### 🎯 Następne kroki:")
            st.info(analysis["next_steps"])
        
        # Conversation transcript
        with st.expander("📜 Zobacz transkrypcję rozmowy"):
            for msg in conv_state["messages"]:
                role_label = "🎮 Handlowiec" if msg["role"] == "user" else f"{client['avatar']} {client['owner']}"
                st.markdown(f"**{role_label}** ({msg['timestamp']}):")
                st.markdown(f"> {msg['content']}")
                st.markdown("")
        
        # Reset button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Spróbuj ponownie", type="primary", use_container_width=True):
                # Reset conversation
                del st.session_state[conv_key]
                st.rerun()


def show_simple_scenario_intro():
    """Pokazuje intro do prostego scenariusza"""
    st.title("🎯 Prosty Scenariusz Wizyty Handlowej")
    
    st.markdown("""
### Czym jest ten scenariusz?

To **najprostsza możliwa symulacja rozmowy handlowej** w food service.

#### 🎮 Jak to działa?

1. **Rozpocznij rozmowę** - AI wciela się w właściciela bistro
2. **Prowadź dialog** - mówisz co chcesz, klient naturalnie odpowiada
3. **Zakończ wizytę** - otrzymasz ocenę i feedback od eksperta

#### 🎯 Cel:

Przekonaj właściciela bistro "U Michała" do testowego zamówienia **Heinz Ketchup Premium 5kg**.

#### 👨‍🍳 Twój klient:

- **Michał Kowalski** - pragmatyczny, liczy każdą złotówkę
- Obecnie używa Pudliszki (zadowolony na 7/10)
- Ma kilku klientów którzy pytają o Heinz
- Budżet ~500 PLN na nowe produkty

#### ⚡ To NIE jest quiz ani test!

- **Brak ocen w trakcie** - AI po prostu gra klienta
- **Prawdziwa rozmowa** - możesz mówić co chcesz
- **Feedback dopiero na końcu** - jak w prawdziwej wizycie handlowej

---

**Gotowy na pierwszą wizytę?**
""")
    
    if st.button("🚀 Rozpocznij scenariusz", type="primary", use_container_width=True):
        st.session_state['simple_scenario_started'] = True
        st.rerun()
