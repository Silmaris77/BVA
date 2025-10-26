"""
Coaching on-the-job - Narzędzie treningowe z live feedbackiem AI
Oddzielne od Business Games - służy tylko do nauki
"""

import streamlit as st
from utils.ai_conversation_engine import (
    initialize_ai_conversation,
    get_conversation_state,
    process_player_message,
    reset_conversation
)
from data.business_data import get_all_ai_contracts


def show_coaching_on_the_job():
    """Narzędzie Coaching on-the-job - trening komunikacji z live feedbackiem"""
    st.markdown("### 🎓 Coaching on-the-job")
    st.markdown("""
    **Trenuj umiejętności komunikacyjne z natychmiastowym feedbackiem trenera AI**
    
    To narzędzie **nie wpływa na grę** - służy wyłącznie do nauki i doskonalenia umiejętności.
    Każda Twoja wypowiedź jest analizowana przez AI, które daje Ci konkretne wskazówki jak się poprawić.
    """)
    
    # Pobierz scenariusze
    ai_contracts = get_all_ai_contracts()
    
    # Filtruj tylko Conversation
    conversation_contracts = [c for c in ai_contracts if c.get("type") == "conversation"]
    
    if not conversation_contracts:
        st.warning("❌ Brak dostępnych scenariuszy treningowych.")
        return
    
    # Wybór scenariusza
    st.markdown("#### 📋 Wybierz scenariusz treningowy")
    
    scenario_options = {c["title"]: c for c in conversation_contracts}
    selected_title = st.selectbox(
        "Scenariusz:",
        options=list(scenario_options.keys()),
        key="coaching_scenario_select"
    )
    
    selected_contract = scenario_options[selected_title]
    contract_id = f"coaching_{selected_contract['id']}"  # Osobny ID dla coachingu
    npc_config = selected_contract.get("npc_config", {})
    scenario_context = selected_contract.get("scenario_context", "")
    
    # Informacja o scenariuszu
    with st.expander("📖 Kontekst sytuacji", expanded=False):
        st.markdown(scenario_context)
    
    # Inicjalizacja konwersacji (bez username - coaching nie zapisuje się do gry)
    conversation = get_conversation_state(contract_id, username="coaching_temp")
    if not conversation:
        initialize_ai_conversation(contract_id, npc_config, scenario_context, username="coaching_temp")
        conversation = get_conversation_state(contract_id, username="coaching_temp")
    
    current_turn = conversation.get("current_turn", 1)
    
    # === SIDEBAR Z LIVE METRYKAMI ===
    with st.sidebar:
        st.markdown("### 📊 Live Feedback - Coaching")
        st.info("🎓 **Tryb treningowy** - nie wpływa na grę")
        
        total_score = conversation.get("total_score", 0)
        relationship_health = conversation.get("relationship_health", 100)
        
        st.metric("Tura", f"{current_turn}")
        st.metric("Punkty", f"{total_score}")
        
        # Relationship health bar
        health_color = "#10b981" if relationship_health >= 70 else "#f59e0b" if relationship_health >= 40 else "#ef4444"
        st.markdown(f"""
        <div style='margin: 12px 0;'>
            <div style='font-size: 14px; color: #475569; margin-bottom: 4px;'>
                ❤️ Relacja z {npc_config.get('name', 'NPC')}
            </div>
            <div style='background: #e2e8f0; height: 12px; border-radius: 6px; overflow: hidden;'>
                <div style='background: {health_color}; width: {relationship_health}%; 
                            height: 100%; transition: width 0.3s;'></div>
            </div>
            <div style='font-size: 12px; color: #64748b; margin-top: 4px;'>
                {relationship_health}/100
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Metryki szczegółowe
        metrics = conversation.get("metrics", {})
        if metrics:
            st.markdown("#### 🎯 Twoje kompetencje")
            for metric_key, metric_value in metrics.items():
                metric_label = {
                    'empathy': '🤝 Empatia',
                    'assertiveness': '💪 Asertywność',
                    'professionalism': '👔 Profesjonalizm',
                    'solution_quality': '💡 Rozwiązania'
                }.get(metric_key, metric_key.capitalize())
                
                # Progress bar dla każdej metryki
                color = "#10b981" if metric_value >= 70 else "#f59e0b" if metric_value >= 40 else "#ef4444"
                st.markdown(f"""
                <div style='margin: 8px 0;'>
                    <div style='font-size: 12px; color: #475569; margin-bottom: 2px;'>
                        {metric_label}
                    </div>
                    <div style='background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden;'>
                        <div style='background: {color}; width: {metric_value}%; 
                                    height: 100%; transition: width 0.3s;'></div>
                    </div>
                    <div style='font-size: 11px; color: #64748b; margin-top: 2px;'>
                        {metric_value}/100
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # === HISTORIA KONWERSACJI ===
    st.markdown("### 💬 Rozmowa")
    
    messages = conversation.get("messages", [])
    
    chat_container = st.container()
    with chat_container:
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("text", msg.get("content", ""))
            timestamp = msg.get("timestamp", "")
            emotion = msg.get("emotion", "neutral")
            
            if role == "npc":
                emotion_emoji = {
                    "happy": "😊", "concerned": "😟", "frustrated": "😤",
                    "neutral": "😐", "thoughtful": "🤔", "relieved": "😌",
                    "angry": "😠", "satisfied": "😌"
                }.get(emotion, "😐")
                
                st.markdown(f"""
                <div style='background: #f1f5f9; padding: 16px; border-radius: 12px; 
                            margin: 12px 0; border-left: 4px solid #667eea;'>
                    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                        <span style='font-size: 24px; margin-right: 8px;'>{emotion_emoji}</span>
                        <div>
                            <div style='font-weight: 600; color: #1e293b;'>
                                {npc_config.get('name', 'NPC')} <span style='color: #64748b; font-size: 12px;'>({npc_config.get('role', 'Rozmówca')})</span>
                            </div>
                            <div style='font-size: 11px; color: #94a3b8;'>{timestamp}</div>
                        </div>
                    </div>
                    <div style='color: #334155; line-height: 1.6;'>{content}</div>
                </div>
                """, unsafe_allow_html=True)
                
            elif role == "player":
                st.markdown(f"""
                <div style='background: #dbeafe; padding: 16px; border-radius: 12px; 
                            margin: 12px 0; border-left: 4px solid #3b82f6;'>
                    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                        <span style='font-size: 24px; margin-right: 8px;'>🎓</span>
                        <div>
                            <div style='font-weight: 600; color: #1e293b;'>Ty (Trening)</div>
                            <div style='font-size: 11px; color: #64748b;'>{timestamp}</div>
                        </div>
                    </div>
                    <div style='color: #1e3a8a; line-height: 1.6;'>{content}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # POKAŻ FEEDBACK AI (coaching!)
                evaluation = msg.get("evaluation")
                if evaluation:
                    feedback_text = evaluation.get("feedback", "")
                    points = evaluation.get("points", 0)
                    empathy = evaluation.get("empathy", 0)
                    assertiveness = evaluation.get("assertiveness", 0)
                    professionalism = evaluation.get("professionalism", 0)
                    solution = evaluation.get("solution_quality", 0)
                    
                    st.markdown(f"""
                    <div style='background: #fef3c7; padding: 12px; border-radius: 8px; 
                                margin: 8px 0 16px 0; border-left: 4px solid #f59e0b;'>
                        <div style='font-size: 12px; font-weight: 600; color: #92400e; margin-bottom: 6px;'>
                            🎯 Feedback Trenera AI (+{points} pkt)
                        </div>
                        <div style='color: #78350f; font-size: 13px; margin-bottom: 8px;'>{feedback_text}</div>
                        <div style='display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; font-size: 11px;'>
                            <div style='background: rgba(255,255,255,0.5); padding: 4px 8px; border-radius: 4px;'>
                                🤝 {empathy}/100
                            </div>
                            <div style='background: rgba(255,255,255,0.5); padding: 4px 8px; border-radius: 4px;'>
                                💪 {assertiveness}/100
                            </div>
                            <div style='background: rgba(255,255,255,0.5); padding: 4px 8px; border-radius: 4px;'>
                                👔 {professionalism}/100
                            </div>
                            <div style='background: rgba(255,255,255,0.5); padding: 4px 8px; border-radius: 4px;'>
                                💡 {solution}/100
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # === INPUT GRACZA ===
    st.markdown("---")
    st.markdown("### ✍️ Twoja odpowiedź treningowa")
    
    if current_turn == 1:
        st.info(f"💡 **Wskazówka**: To tryb treningowy - otrzymasz feedback po każdej wypowiedzi. Eksperymentuj i ucz się!")
    
    # Prosty text area (bez audio - dla uproszczenia)
    player_message = st.text_area(
        "Co powiesz?",
        height=150,
        placeholder=f"Wpisz swoją odpowiedź do {npc_config.get('name', 'rozmówcy')}...",
        key=f"coaching_input_{contract_id}_{current_turn}"
    )
    
    # Przyciski
    col_send, col_reset = st.columns([3, 1])
    
    with col_send:
        if st.button("📤 Wyślij (i zobacz feedback)", type="primary", use_container_width=True,
                    disabled=not player_message or not player_message.strip()):
            if player_message and player_message.strip():
                with st.spinner("🤖 Trener AI analizuje Twoją odpowiedź..."):
                    api_key = st.secrets.get("API_KEYS", {}).get("gemini", "")
                    if not api_key:
                        st.error("❌ Brak klucza API Gemini.")
                    else:
                        try:
                            evaluation, npc_reaction = process_player_message(
                                contract_id,
                                player_message,
                                api_key,
                                username="coaching_temp"
                            )
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Błąd: {str(e)}")
    
    with col_reset:
        if st.button("🔄 Reset", use_container_width=True):
            reset_conversation(contract_id, npc_config, scenario_context, username="coaching_temp")
            st.rerun()
