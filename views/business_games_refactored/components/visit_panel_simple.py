"""
🎯 Prosty Panel Wizyty - Naturalna Rozmowa Handlowa

Minimalistyczny interfejs do symulacji rozmowy handlowej:
- Tylko rozmowa (bez wyboru produktów przed wizytą)
- AI gra klienta naturalnie
- Ocena i feedback DOPIERO PO zakończeniu
- Jedna sesja - musi być skończona na raz
"""

import streamlit as st
from datetime import datetime
from typing import Dict, List
from utils.fmcg_ai_conversation import conduct_fmcg_conversation, evaluate_conversation_quality
from utils.fmcg_mechanics import update_fmcg_game_state_sql
from utils.notes_panel import render_notes_panel
from data.users_new import get_current_user_data, save_single_user
from utils.user_helpers import get_user_sql_id


def render_visit_panel_simple(client_id: str, clients: Dict, game_state: Dict, username: str,
                            available_products: List[Dict] = None, available_clients: List[Dict] = None):
    """
    Prosty panel wizyty - naturalna rozmowa bez coaching
    
    Args:
        client_id: ID odwiedzanego klienta
        clients: Słownik wszystkich klientów
        game_state: Stan gry
        username: Nazwa użytkownika
        available_products: Lista produktów dla notatnika
        available_clients: Lista klientów dla notatnika
    """
    client = clients.get(client_id, {})
    client_name = client.get('name', client_id)
    
    # Initialize conversation state
    conversation_key = f"simple_visit_{client_id}"
    if conversation_key not in st.session_state:
        st.session_state[conversation_key] = {
            "messages": [],
            "visit_started": False,
            "visit_completed": False,
            "start_time": None
        }
    
    conv_state = st.session_state[conversation_key]
    
    # =================================================================
    # HEADER
    # =================================================================
    
    avatar = client.get("avatar", "👤")
    owner_name = client.get("chef_name", client.get("owner", client.get("owner_name", "")))
    
    # Fallback jeśli brak imienia właściciela
    if not owner_name:
        owner_name = "Właściciel"
    
    st.markdown(f"### 💬 Wizyta u {client_name}")
    if owner_name and owner_name != "Właściciel":
        st.caption(f"{avatar} Właściciel: **{owner_name}**")
    
    # Cancel button (return to main view)
    if st.button("← Anuluj wizytę", type="secondary", key="cancel_visit_simple"):
        # Clear visit state
        if conversation_key in st.session_state:
            del st.session_state[conversation_key]
        if "current_visit_client_id" in st.session_state:
            del st.session_state["current_visit_client_id"]
        st.rerun()
    
    # Client info (compact)
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        status = client.get('status', 'PROSPECT')
        st.caption(f"Status: **{status}**")
    with col_c2:
        reputation = client.get('reputation', 0)
        st.caption(f"Reputacja: **{reputation}/100**")
    with col_c3:
        segment = client.get('segment', '?')
        st.caption(f"Segment: **{segment}**")
    
    st.markdown("---")
    
    # =================================================================
    # CONVERSATION
    # =================================================================
    
    if not conv_state["visit_completed"]:
        # START VISIT
        if not conv_state["visit_started"]:
            st.markdown("### 👋 Rozpocznij wizytę")
            st.info(f"💡 Prowadź naturalną rozmowę z {owner_name}. AI odpowie jako klient.")
            
            if st.button("🚀 Rozpocznij rozmowę", type="primary", use_container_width=True):
                conv_state["visit_started"] = True
                conv_state["start_time"] = datetime.now().isoformat()
                
                # AI powitanie
                with st.spinner(f"{owner_name} wita..."):
                    try:
                        ai_greeting, _ = conduct_fmcg_conversation(
                            client=client,
                            player_message="[ROZPOCZĘCIE WIZYTY]",
                            conversation_history=[],
                            current_messages=[]
                        )
                    except Exception as e:
                        print(f"❌ Błąd AI greeting: {str(e)}")
                        ai_greeting = f"Dzień dobry! Witam w {client_name}. Słucham?"
                
                conv_state["messages"].append({
                    "role": "assistant",
                    "content": ai_greeting,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
                st.rerun()
        
        # CONVERSATION IN PROGRESS
        else:
            # Display conversation history
            for msg in conv_state["messages"]:
                if msg["role"] == "user":
                    with st.chat_message("user", avatar="🎮"):
                        st.markdown(msg["content"])
                        st.caption(f"🕐 {msg['timestamp']}")
                else:
                    with st.chat_message("assistant", avatar=avatar):
                        st.markdown(f"**{owner_name}:** {msg['content']}")
                        st.caption(f"🕐 {msg['timestamp']}")
            
            # Input area
            st.markdown("---")
            
            # Klucze dla transkrypcji i wersjonowania
            transcription_key = f"simple_visit_transcription_{client_id}"
            transcription_version_key = f"simple_visit_transcription_version_{client_id}"
            last_audio_hash_key = f"simple_visit_last_audio_hash_{client_id}"
            
            # Inicjalizacja
            st.session_state.setdefault(transcription_key, "")
            st.session_state.setdefault(transcription_version_key, 0)
            st.session_state.setdefault(last_audio_hash_key, None)
            
            # Counter for recorder key
            recorder_counter_key = f"simple_audio_recorder_counter_{client_id}"
            st.session_state.setdefault(recorder_counter_key, 0)
            
            # Audio recording with button
            from audio_recorder_streamlit import audio_recorder
            
            # Display audio recorder
            audio_bytes_recorded = audio_recorder(
                text="",
                recording_color="#e74c3c",
                neutral_color="#3498db",
                icon_name="microphone",
                icon_size="2x",
                key=f"simple_audio_recorder_{client_id}_{st.session_state[recorder_counter_key]}"
            )
            
            # Use recorded audio
            audio_data = None
            if audio_bytes_recorded:
                import io
                import hashlib
                
                # Sprawdź czy to nowe nagranie
                audio_hash = hashlib.md5(audio_bytes_recorded).hexdigest()
                
                if audio_hash != st.session_state[last_audio_hash_key]:
                    st.session_state[last_audio_hash_key] = audio_hash
                    audio_data = io.BytesIO(audio_bytes_recorded)
                    audio_data.name = "recording.wav"
                    st.success("✅ Nagranie zakończone! Przetwarzam...")
            
            # Przetwarzanie nagrania audio
            if audio_data is not None:
                import speech_recognition as sr
                import tempfile
                import os
                from pydub import AudioSegment
                
                # Pobierz bajty audio
                audio_bytes = audio_data.getvalue() if hasattr(audio_data, 'getvalue') else audio_data.read()
                
                with st.spinner("🤖 Rozpoznaję mowę..."):
                    try:
                        file_ext = ".webm"
                        if hasattr(audio_data, 'name'):
                            if audio_data.name.endswith('.wav'):
                                file_ext = ".wav"
                            elif audio_data.name.endswith('.mp3'):
                                file_ext = ".mp3"
                            elif audio_data.name.endswith('.m4a'):
                                file_ext = ".m4a"
                            elif audio_data.name.endswith('.ogg'):
                                file_ext = ".ogg"
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                            tmp_file.write(audio_bytes)
                            tmp_path = tmp_file.name
                        
                        wav_path = None
                        try:
                            audio = AudioSegment.from_file(tmp_path)
                            wav_path = tmp_path.replace(file_ext, "_converted.wav")
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
                            # Inkrementuj counter aby zresetować audio_recorder
                            st.session_state[recorder_counter_key] += 1
                            st.success("✅ Transkrypcja ukończona!")
                            
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
            text_area_key = f"simple_visit_input_{client_id}_{len(conv_state['messages'])}_v{st.session_state[transcription_version_key]}"
            current_text = st.session_state.get(transcription_key, "")
            
            # Callback - synchronizuj wartość text_area z transcription_key
            def sync_textarea_to_state():
                if text_area_key in st.session_state:
                    st.session_state[transcription_key] = st.session_state[text_area_key]
            
            # Oblicz dynamiczną wysokość
            num_lines = current_text.count('\n') + 1
            dynamic_height = max(120, min(400, 120 + (num_lines - 3) * 25))
            
            player_message = st.text_area(
                "✍️ Twoja wypowiedź:",
                value=current_text,
                height=dynamic_height,
                key=text_area_key,
                placeholder="Mów przez mikrofon lub pisz tutaj...",
                on_change=sync_textarea_to_state
            )
            
            col_send, col_end = st.columns([3, 1])
            
            with col_send:
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
                        with st.spinner(f"{owner_name} odpowiada..."):
                            try:
                                ai_response, metadata = conduct_fmcg_conversation(
                                    client=client,
                                    player_message=player_message,
                                    conversation_history=[],
                                    current_messages=conv_state["messages"]
                                )
                            except Exception as e:
                                import traceback
                                error_details = traceback.format_exc()
                                print(f"❌ Błąd AI conversation: {error_details}")
                                ai_response = f"Przepraszam, coś poszło nie tak... Błąd: {str(e)}"
                        
                        # Add AI response
                        conv_state["messages"].append({
                            "role": "assistant",
                            "content": ai_response,
                            "timestamp": datetime.now().strftime("%H:%M")
                        })
                        
                        # Wyczyść transkrypcję dla nowej wiadomości
                        st.session_state[transcription_key] = ""
                        st.session_state[transcription_version_key] += 1
                        
                        st.rerun()
            
            with col_end:
                if st.button("🏁 Zakończ\nwizytę", type="secondary", use_container_width=True):
                    conv_state["visit_completed"] = True
                    st.rerun()
            
            # Notatnik dostępny w trakcie wizyty
            st.markdown("---")
            with st.expander("📓 Notatnik", expanded=False):
                user_data = get_current_user_data()
                if user_data:
                    # Get INTEGER user id from SQL (for notes foreign key)
                    sql_user_id = get_user_sql_id(username)
                    
                    if sql_user_id:
                        render_notes_panel(
                            user_id=sql_user_id,
                            active_tab="client_profile",
                            scenario_context=f"Wizyta u {client_name}",
                            client_name=client_name,
                            key_prefix=f"simple_visit_{client_id}",
                            available_products=available_products,
                            available_clients=available_clients
                        )
                    else:
                        st.warning("⚠️ Notatnik niedostępny - użytkownik nie w bazie SQL")
    
    # =================================================================
    # VISIT COMPLETED - EVALUATION
    # =================================================================
    else:
        st.success("✅ Wizyta zakończona!")
        st.markdown("---")
        
        # Evaluate conversation
        st.markdown("### 📊 Ocena Rozmowy")
        
        with st.spinner("🤖 AI analizuje Twoją rozmowę..."):
            try:
                conversation_evaluation = evaluate_conversation_quality(
                    conversation_messages=conv_state["messages"],
                    client=client
                )
            except Exception as e:
                st.error(f"❌ Błąd oceny: {e}")
                conversation_evaluation = {
                    "quality": 3,
                    "order_likely": False,
                    "order_value": 0,
                    "reputation_change": 0,
                    "feedback": "Automatyczna ocena niedostępna"
                }
        
        # Display score
        quality = conversation_evaluation.get("quality", 3)
        feedback = conversation_evaluation.get("feedback", "Brak feedbacku")
        
        # Stars visualization
        stars_filled = quality
        stars = "⭐" * stars_filled + "☆" * (5 - stars_filled)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 30px; border-radius: 15px; text-align: center; color: white;'>
    <div style='font-size: 48px; margin-bottom: 10px;'>{stars}</div>
    <div style='font-size: 24px; font-weight: bold;'>{quality}/5</div>
    <div style='font-size: 14px; opacity: 0.9; margin-top: 10px;'>JAKOŚĆ ROZMOWY</div>
</div>
""", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Feedback
        st.markdown("#### 💬 Feedback AI:")
        st.markdown(f"""
<div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; 
            border-left: 5px solid #667eea;'>
{feedback}
</div>
""", unsafe_allow_html=True)
        
        # Order prediction
        if conversation_evaluation.get("order_likely"):
            order_value = conversation_evaluation.get("order_value", 0)
            st.success(f"🎉 **Prawdopodobne zamówienie:** ~{order_value} PLN")
        else:
            st.info("📝 **Brak zamówienia** - buduj relację w kolejnych wizytach")
        
        # Reputation change
        reputation_change = conversation_evaluation.get("reputation_change", 0)
        if reputation_change != 0:
            sign = "+" if reputation_change > 0 else ""
            st.metric("Zmiana reputacji", f"{sign}{reputation_change}", delta=reputation_change)
        
        st.markdown("---")
        
        # Save results
        if st.button("💾 Zapisz i wyjdź", type="primary", use_container_width=True):
            # ====================================================================
            # EXTRACT DISCOVERED INFO FROM CONVERSATION USING AI
            # ====================================================================
            
            if "discovered_info" not in client:
                client["discovered_info"] = {}
            
            discovered = client["discovered_info"]
            
            # Use AI to extract what client actually said in conversation
            try:
                from utils.fmcg_ai_conversation import extract_discovered_info_from_conversation
                
                st.info("🤖 Analizuję rozmowę i odkrywam informacje o kliencie...")
                
                new_discoveries = extract_discovered_info_from_conversation(
                    conversation_messages=conv_state["messages"],
                    client=client,
                    current_discovered_info=discovered
                )
                
                # Update discovered_info with new discoveries
                discoveries_count = 0
                for field, value in new_discoveries.items():
                    if field == "sales_capacity_discovered_Food":
                        # Special handling for Food category capacity
                        if "sales_capacity_discovered" not in discovered:
                            discovered["sales_capacity_discovered"] = {}
                        if "Food" not in discovered["sales_capacity_discovered"]:
                            discovered["sales_capacity_discovered"]["Food"] = value
                            discoveries_count += 1
                            monthly_kg = value.get('monthly_volume_kg', 0)
                            st.success(f"✅ Odkryto potencjał: {monthly_kg} kg/mies")
                        else:
                            st.info("💡 Potencjał już był znany")
                    else:
                        # Regular discovered_info field
                        if discovered.get(field) is None:  # Only if not discovered yet
                            discovered[field] = value
                            discoveries_count += 1
                            
                            # Show discovery notification
                            field_labels = {
                                "personality_description": "Opis osobowości",
                                "decision_priorities": "Priorytety decyzyjne",
                                "main_customers": "Główni klienci",
                                "pain_points": "Problemy biznesowe",
                                "typical_order_value": "Typowa wartość zamówienia",
                                "preferred_frequency": "Preferowana częstotliwość",
                                "trust_level": "Poziom zaufania"
                            }
                            label = field_labels.get(field, field)
                            st.success(f"✅ Odkryto: {label}")
                
                if discoveries_count > 0:
                    st.success(f"🎉 Odkryto {discoveries_count} nowych informacji o kliencie!")
                else:
                    st.info("💡 Klient nie ujawnił nowych informacji w tej rozmowie")
                    
            except Exception as e:
                st.warning(f"⚠️ Nie udało się przeanalizować discovery: {e}")
            
            # Calculate knowledge level based on discovered fields count
            try:
                from utils.fmcg_ai_conversation import calculate_knowledge_level
                client["knowledge_level"] = calculate_knowledge_level(discovered)
            except:
                pass
            
            # Update client data
            client["last_visit_day"] = game_state.get("current_day", 0)
            client["last_visit_date"] = datetime.now().isoformat()
            client["visits_count"] = client.get("visits_count", 0) + 1
            
            # Update reputation
            reputation_before = client.get("reputation", 50)
            client["reputation"] = min(100, max(0, reputation_before + reputation_change))
            
            # Update status if first order
            if client.get("status") == "PROSPECT" and conversation_evaluation.get("order_likely"):
                client["status"] = "ACTIVE"
                st.success("🎉 Klient zmienił status: PROSPECT → ACTIVE!")
            
            # Add to visit history
            if "visit_history" not in client:
                client["visit_history"] = []
            
            conversation_transcript = "\n\n".join([
                f"{'🎮 Handlowiec' if msg['role'] == 'user' else avatar + ' ' + owner_name}: {msg['content']}"
                for msg in conv_state["messages"]
            ])
            
            visit_record = {
                "day": game_state.get("current_day", 0),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "quality_score": quality,
                "reputation_change": reputation_change,
                "reputation_after": client["reputation"],
                "order_likely": conversation_evaluation.get("order_likely", False),
                "order_value": conversation_evaluation.get("order_value", 0),
                "conversation_transcript": conversation_transcript,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            client["visit_history"].append(visit_record)
            
            # ====================================================================
            # UPDATE CONVICTION DATA (dla scenariusza Heinz)
            # ====================================================================
            
            # Check if Heinz scenario
            scenario_type = game_state.get('scenario', {}).get('model', '')
            is_heinz_scenario = scenario_type == 'through_distributor'
            
            if not is_heinz_scenario and 'heinz' in game_state.get('scenario_id', '').lower():
                is_heinz_scenario = True
            
            if not is_heinz_scenario and client.get('conviction_data'):
                is_heinz_scenario = True
            
            if is_heinz_scenario and client.get('conviction_data'):
                # Update conviction based on conversation quality
                st.info("🤖 Aktualizuję conviction dla produktów Heinz...")
                
                # Map quality score to progress gain
                if quality >= 5:
                    progress_gain = 25  # Excellent conversation
                elif quality >= 4:
                    progress_gain = 15  # Good conversation
                elif quality >= 3:
                    progress_gain = 10  # Decent conversation
                else:
                    progress_gain = 5   # Poor conversation
                
                # Update all products currently in conviction process
                for product_id, conv_info in client["conviction_data"].items():
                    current_progress = conv_info.get('progress', 0)
                    current_stage = conv_info.get('stage', 'discovery')
                    
                    # Only update if not already won
                    if current_stage != 'won' and current_progress < 100:
                        new_progress = min(100, current_progress + progress_gain)
                        
                        # Determine new stage
                        if new_progress >= 67:
                            new_stage = 'convince'
                        elif new_progress >= 34:
                            new_stage = 'pitch'
                        else:
                            new_stage = 'discovery'
                        
                        # Check if won
                        if new_progress >= 100:
                            new_stage = 'won'
                        
                        # Update conviction data
                        client["conviction_data"][product_id]['progress'] = new_progress
                        client["conviction_data"][product_id]['stage'] = new_stage
                        client["conviction_data"][product_id]['last_interaction_date'] = datetime.now().strftime("%Y-%m-%d")
                        
                        # Add to history
                        if 'conversation_history' not in client["conviction_data"][product_id]:
                            client["conviction_data"][product_id]['conversation_history'] = []
                        
                        client["conviction_data"][product_id]['conversation_history'].append({
                            'date': datetime.now().strftime("%Y-%m-%d"),
                            'progress_gain': progress_gain,
                            'progress_after': new_progress,
                            'stage_after': new_stage,
                            'conversation_quality': quality
                        })
                        
                        # Show notification
                        product_name = product_id.replace('_', ' ').title()
                        st.success(f"✅ {product_name}: +{progress_gain}% conviction (→ {new_progress}%, {new_stage.upper()})")
                        
                        # Check if won (100%)
                        if new_stage == 'won' and current_stage != 'won':
                            st.balloons()
                            st.success(f"🎉 **{product_name}** - Klient przekonany! Zamówienie wkrótce.")
                            
                            # Create pending order (delayed order logic)
                            try:
                                from utils.delayed_orders import create_pending_order
                                
                                if 'pending_orders' not in client["conviction_data"][product_id]:
                                    client["conviction_data"][product_id]['pending_orders'] = []
                                
                                # Check if pending order already exists
                                existing_pending = [
                                    o for o in client["conviction_data"][product_id]['pending_orders']
                                    if o['status'] == 'pending'
                                ]
                                
                                if not existing_pending:
                                    pending_order = create_pending_order(
                                        client_id=client_id,
                                        client_name=client.get('name', client.get('chef_name', 'Nieznany')),
                                        product_id=product_id,
                                        date_convinced=datetime.now().strftime("%Y-%m-%d"),
                                        distributor_name="Orbico"
                                    )
                                    
                                    client["conviction_data"][product_id]['pending_orders'].append(pending_order)
                                    
                                    st.info(f"📦 Oczekiwane zamówienie za {pending_order['delay_days']} dni przez dystrybutora")
                            except Exception as e:
                                st.warning(f"⚠️ Nie udało się utworzyć pending order: {e}")
            
            # Calculate energy cost
            from utils.fmcg_mechanics import calculate_visit_energy_cost
            distance = client.get("distance_from_base", client.get("distance_km", 0))
            energy_cost = calculate_visit_energy_cost(distance, visit_duration_minutes=30)
            
            current_energy = game_state.get("energy", 100)
            new_energy = max(0, current_energy - energy_cost)
            game_state["energy"] = new_energy
            
            # Mark visit as completed
            completed_visits = game_state.get("completed_visits_today", [])
            if client_id not in completed_visits:
                completed_visits.append(client_id)
                game_state["completed_visits_today"] = completed_visits
            
            # INCREMENT WEEKLY VISIT COUNTER
            game_state["visits_this_week"] = game_state.get("visits_this_week", 0) + 1
            print(f"\n{'='*80}\n✅ WIZYTA ZAPISANA - visits_this_week: {game_state['visits_this_week']}\n{'='*80}\n")
            
            # Update session state for route tracking
            if hasattr(st.session_state, 'completed_visits_today'):
                if client_id not in st.session_state.completed_visits_today:
                    st.session_state.completed_visits_today.append(client_id)
            else:
                st.session_state.completed_visits_today = [client_id]
            
            # CRITICAL: Explicitly update clients dict (even though client is a reference)
            clients[client_id] = client
            
            # Update clients dict in game_state
            if "clients" not in game_state:
                game_state["clients"] = {}
            game_state["clients"][client_id] = client
            
            # IMPORTANT: Update session state to reflect changes immediately
            if "fmcg_clients" in st.session_state:
                st.session_state["fmcg_clients"][client_id] = client
            if "fmcg_game_state" in st.session_state:
                st.session_state["fmcg_game_state"] = game_state
            
            # DUAL-WRITE MODE: Save to both JSON and SQL
            user_data = get_current_user_data(username)
            if user_data:
                # Update the game_state in user_data structure
                if "business_games" not in user_data:
                    user_data["business_games"] = {}
                if "fmcg" not in user_data["business_games"]:
                    user_data["business_games"]["fmcg"] = {}  # FIX: Create fmcg dict, not overwrite business_games
                
                # Save updated game_state back to structure
                user_data["business_games"]["fmcg"]["game_state"] = game_state
                user_data["business_games"]["fmcg"]["clients"] = clients
                
                # Write to JSON
                save_single_user(username, user_data)
                print(f"\n{'='*80}\n✅ ZAPISANO DO JSON - visits: {game_state.get('visits_this_week', 0)}, clients: {len(clients)}\n{'='*80}\n")
                
                # Write to SQL
                sql_success = update_fmcg_game_state_sql(username, game_state, clients)
                if sql_success:
                    print(f"✅ ZAPISANO DO SQL - visits: {game_state.get('visits_this_week', 0)}")
                else:
                    print(f"⚠️ Zapis do SQL nieudany (user może nie istnieć w SQL)")
            else:
                st.error("❌ Nie znaleziono danych użytkownika!")
            
            st.success("✅ Wizyta zapisana!")
            
            # Summary
            st.markdown("#### 📊 Podsumowanie:")
            st.markdown(f"**Reputacja:** {client['reputation']}/100 ({'+' if reputation_change > 0 else ''}{reputation_change})")
            st.markdown(f"**Energia:** {new_energy}% (-{energy_cost}%)")
            st.markdown(f"**Status:** {client.get('status', 'PROSPECT')}")
            
            st.markdown("---")
            
            # Button to return to main view
            if st.button("🔙 Powrót do gry", type="primary", use_container_width=True):
                # Clear conversation state
                if conversation_key in st.session_state:
                    del st.session_state[conversation_key]
                
                # CRITICAL: Clear current_visit flag to return to main view
                if "current_visit_client_id" in st.session_state:
                    del st.session_state["current_visit_client_id"]
                
                st.rerun()
