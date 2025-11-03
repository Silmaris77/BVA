"""
🚀 Panel Wizyt FMCG - oparty na sprawdzonym render_conversation_contract
"""

import streamlit as st
from typing import Dict, List
import time
from datetime import datetime
from utils.fmcg_ai_conversation import conduct_fmcg_conversation
from utils.fmcg_mechanics import update_fmcg_game_state_sql
from utils.notes_panel import render_notes_panel
from data.users_new import get_current_user_data


def render_visit_panel_advanced(client_id: str, clients: Dict, game_state: Dict, username: str):
    """
    Panel wizyty FMCG wykorzystujący sprawdzoną logikę z consulting conversation contracts
    """
    client = clients.get(client_id, {})
    client_name = client.get('name', client_id)
    
    # Initialize conversation state - używamy tego samego klucza co stary kod dla kompatybilności
    conversation_key = f"visit_conversation_{client_id}"
    if conversation_key not in st.session_state:
        st.session_state[conversation_key] = {
            "messages": [],
            "visit_started": True,  # Auto-start wizyta (nie ma wyboru typu)
            "visit_completed": False,
            "current_turn": 1
        }
    
    conv_state = st.session_state[conversation_key]
    
    # Migracja starych stanów konwersacji (dodaj brakujące klucze)
    if "current_turn" not in conv_state:
        conv_state["current_turn"] = 1
    if "visit_completed" not in conv_state:
        conv_state["visit_completed"] = False
    if "visit_started" not in conv_state:
        conv_state["visit_started"] = True
    if "messages" not in conv_state:
        conv_state["messages"] = []
    
    current_turn = conv_state.get("current_turn", 1)
    
    # =================================================================
    # HEADER
    # =================================================================
    
    st.markdown(f"### 💬 Wizyta u {client_name}")
    
    # Client info (compact)
    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    with col_c1:
        status = client.get('status', 'PROSPECT')
        st.caption(f"Status: **{status}**")
    with col_c2:
        reputation = client.get('reputation', 0)
        st.caption(f"Reputacja: **{reputation}/100**")
    with col_c3:
        segment = client.get('segment', '?')
        st.caption(f"Segment: **{segment}**")
    with col_c4:
        last_visit = client.get('last_visit_day', 'Nigdy')
        st.caption(f"Ostatnia: **{last_visit}**")
    
    st.markdown("---")
    
    # =================================================================
    # CONVERSATION HISTORY
    # =================================================================
    
    if not conv_state["visit_completed"]:
        # Show conversation history
        for msg in conv_state["messages"]:
            if msg["role"] == "assistant":
                # AI klienta
                timestamp = msg.get("timestamp", "")
                content = msg.get("content", "")
                st.markdown(f"""
                <div style='background: #f8fafc; padding: 16px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid #3b82f6;'>
                    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                        <span style='font-size: 24px; margin-right: 8px;'>🏪</span>
                        <div>
                            <div style='font-weight: 600; color: #1e293b;'>{client_name}</div>
                            <div style='font-size: 11px; color: #64748b;'>{timestamp}</div>
                        </div>
                    </div>
                    <div style='color: #334155; line-height: 1.6;'>{content}</div>
                </div>
                """, unsafe_allow_html=True)
                
            elif msg["role"] == "user":
                # Gracz
                timestamp = msg.get("timestamp", "")
                content = msg.get("content", "")
                st.markdown(f"""
                <div style='background: #eff6ff; padding: 16px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid #2563eb;'>
                    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                        <span style='font-size: 24px; margin-right: 8px;'>🎮</span>
                        <div>
                            <div style='font-weight: 600; color: #1e293b;'>Ty</div>
                            <div style='font-size: 11px; color: #64748b;'>{timestamp}</div>
                        </div>
                    </div>
                    <div style='color: #1e3a8a; line-height: 1.6;'>{content}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # =================================================================
        # INPUT GRACZA (zgodny z contract_card)
        # =================================================================
        
        st.markdown("---")
        st.markdown("### ✍️ Twoja odpowiedź")
        
        # Wskazówki kontekstowe
        if current_turn == 1:
            st.info(f"💡 **Wskazówka**: {client_name} ma swoje potrzeby i oczekiwania. Spróbuj zrozumieć sytuację z jego punktu widzenia.")
        
        # === SPEECH-TO-TEXT INTERFACE (jak w contract_card) ===
        st.markdown("**🎤 Nagraj** (wielokrotnie, jeśli chcesz) **lub ✍️ pisz bezpośrednio w polu poniżej:**")
        
        # Klucze dla transkrypcji i wersjonowania
        transcription_key = f"fmcg_visit_transcription_{client_id}"
        transcription_version_key = f"fmcg_visit_transcription_version_{client_id}"
        last_audio_hash_key = f"fmcg_visit_last_audio_hash_{client_id}"
        
        # Inicjalizacja
        st.session_state.setdefault(transcription_key, "")
        st.session_state.setdefault(transcription_version_key, 0)
        st.session_state.setdefault(last_audio_hash_key, None)
        
        audio_data = st.audio_input(
            "🎤 Nagrywanie...",
            key=f"audio_input_fmcg_visit_{client_id}"
        )
        
        # Przetwarzanie nagrania audio (tylko jeśli to NOWE nagranie!)
        if audio_data is not None:
            import hashlib
            
            audio_bytes = audio_data.getvalue()
            audio_hash = hashlib.md5(audio_bytes).hexdigest()
            
            if audio_hash != st.session_state[last_audio_hash_key]:
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
                                
                                api_key = st.secrets["API_KEYS"]["gemini"]
                                genai.configure(api_key=api_key)
                                
                                model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
                                prompt = f"""Dodaj interpunkcję (kropki, przecinki, pytajniki, wykrzykniki) do poniższego tekstu.
Nie zmieniaj słów, tylko dodaj znaki interpunkcyjne. Zachowaj strukturę i podział na zdania.
Zwróć tylko poprawiony tekst, bez dodatkowych komentarzy.

Tekst do poprawy:
{transcription}"""
                                response = model.generate_content(prompt)
                                transcription_with_punctuation = response.text.strip()
                                transcription = transcription_with_punctuation
                                
                            except Exception:
                                pass
                            
                            # DOPISZ do istniejącego tekstu
                            existing_text = st.session_state.get(transcription_key, "")
                            
                            if existing_text.strip():
                                st.session_state[transcription_key] = existing_text.rstrip() + "\n\n" + transcription
                            else:
                                st.session_state[transcription_key] = transcription
                            
                            st.session_state[transcription_version_key] += 1
                            
                        except sr.UnknownValueError:
                            st.error("❌ Nie udało się rozpoznać mowy. Spróbuj ponownie lub mów wyraźniej.")
                        except sr.RequestError as e:
                            st.error(f"❌ Błąd połączenia z usługą rozpoznawania mowy: {str(e)}")
                        finally:
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
                            if wav_path and os.path.exists(wav_path):
                                os.unlink(wav_path)
                                
                    except Exception as e:
                        st.error(f"❌ Błąd podczas transkrypcji: {str(e)}")
                        st.info("💡 Możesz wprowadzić tekst ręcznie w polu poniżej.")
        
        # Dynamiczny klucz który zmienia się po transkrypcji
        text_area_key = f"fmcg_visit_input_{client_id}_{current_turn}_v{st.session_state[transcription_version_key]}"
        current_text = st.session_state.get(transcription_key, "")
        
        # Callback - synchronizuj wartość text_area z transcription_key
        def sync_textarea_to_state():
            if text_area_key in st.session_state:
                st.session_state[transcription_key] = st.session_state[text_area_key]
        
        # Oblicz dynamiczną wysokość
        num_lines = current_text.count('\n') + 1
        dynamic_height = max(120, min(400, 120 + (num_lines - 3) * 25))
        
        # Text area dla odpowiedzi
        player_message = st.text_area(
            "📝 Możesz edytować transkrypcję lub pisać bezpośrednio:",
            value=current_text,
            height=dynamic_height,
            key=text_area_key,
            placeholder=f"Wpisz swoją odpowiedź do {client_name}... lub użyj mikrofonu powyżej",
            on_change=sync_textarea_to_state
        )
        
        # Przyciski
        col_send, col_end = st.columns([3, 1])
        
        with col_send:
            if st.button("Wyślij", 
                        type="primary", 
                        use_container_width=True,
                        disabled=not player_message.strip(),
                        key=f"send_msg_fmcg_{client_id}_{current_turn}"):
                if player_message.strip():
                    with st.spinner("🤖 AI analizuje Twoją odpowiedź i generuje reakcję..."):
                        # Dodaj wiadomość gracza
                        conv_state["messages"].append({
                            "role": "user",
                            "content": player_message,
                            "timestamp": datetime.now().strftime("%H:%M")
                        })
                        
                        # Wywołaj AI klienta (używając sprawdzonej funkcji z fmcg_ai_conversation)
                        try:
                            ai_response, metadata = conduct_fmcg_conversation(
                                client=client,
                                player_message=player_message,
                                conversation_history=[],
                                current_messages=conv_state["messages"]
                            )
                            
                            # Dodaj odpowiedź AI
                            conv_state["messages"].append({
                                "role": "assistant",
                                "content": ai_response,
                                "timestamp": datetime.now().strftime("%H:%M")
                            })
                            
                            # Inkrementuj turę
                            conv_state["current_turn"] += 1
                            
                            # Wyczyść transkrypcję dla nowej wiadomości
                            st.session_state[transcription_key] = ""
                            st.session_state[transcription_version_key] += 1
                            
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Błąd AI: {str(e)}")
        
        # Przycisk zakończenia wizyty
        if st.button("Zakończ wizytę", type="primary", use_container_width=True, key=f"end_visit_{client_id}"):
            # Oznacz wizytę jako zakończoną
            conv_state["visit_completed"] = True
            st.rerun()
    
    # =================================================================
    # VISIT COMPLETED - SAVE RESULTS
    # =================================================================
    
    else:
        st.success("🎉 Wizyta zakończona!")
        
        st.markdown("### 📊 Podsumowanie wizyty")
        
        # Ocena jakości
        quality_score = st.slider(
            "⭐ Jak oceniasz jakość tej wizyty?",
            min_value=1,
            max_value=5,
            value=3,
            help="Autorefleksja: Jak dobrze przeprowadziłeś tę wizytę?",
            key=f"quality_{client_id}"
        )
        
        # Wartość zamówienia
        order_value = st.number_input(
            "💰 Wartość zamówienia (PLN)",
            min_value=0,
            max_value=50000,
            value=0,
            step=100,
            key=f"order_{client_id}"
        )
        
        # Marża
        margin_pct = st.number_input(
            "📈 Marża (%)",
            min_value=0,
            max_value=100,
            value=20,
            step=5,
            key=f"margin_{client_id}"
        )
        
        # Notatki
        visit_notes = st.text_area(
            "📝 Notatki z wizyty",
            placeholder="Co ważnego się wydarzyło? Jakie ustalenia?",
            key=f"notes_{client_id}"
        )
        
        # Zapisz wyniki
        if st.button("💾 Zapisz i przejdź dalej", type="primary", use_container_width=True, key=f"save_visit_{client_id}"):
            # Update client data
            client["last_visit_day"] = game_state.get("current_day", 0)
            client["reputation"] = min(100, client.get("reputation", 50) + (quality_score - 3) * 5)
            
            # Add to visit history
            if "visit_history" not in client:
                client["visit_history"] = []
            
            client["visit_history"].append({
                "day": game_state.get("current_day", 0),
                "quality": quality_score,
                "order_value": order_value,
                "margin_pct": margin_pct,
                "notes": visit_notes,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Update sales stats
            if order_value > 0:
                game_state["total_sales"] = game_state.get("total_sales", 0) + order_value
                game_state["total_margin"] = game_state.get("total_margin", 0) + (order_value * margin_pct / 100)
            
            # Mark visit as completed
            completed_visits = game_state.get("completed_visits_today", [])
            if client_id not in completed_visits:
                completed_visits.append(client_id)
                game_state["completed_visits_today"] = completed_visits
            
            # Save to database
            try:
                update_fmcg_game_state_sql(username, game_state)
                st.success("✅ Wizyta zapisana!")
                time.sleep(1)
                
                # Clear conversation state
                del st.session_state[conversation_key]
                
                st.rerun()
            except Exception as e:
                st.error(f"Błąd zapisu: {str(e)}")
        
        # Notatnik w expanderze (na dole)
        with st.expander("📓 Notatnik", expanded=False):
            user_data = get_current_user_data()
            if user_data:
                render_notes_panel(
                    user_id=user_data.get("id"),
                    active_tab="client_profile",
                    scenario_context=f"Wizyta FMCG u {client_name}",
                    client_name=client_name,
                    key_prefix=f"fmcg_visit_{client_id}"
                )
