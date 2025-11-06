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
from utils.user_helpers import get_user_sql_id


def render_visit_panel_advanced(client_id: str, clients: Dict, game_state: Dict, username: str, 
                                available_products: List[Dict] = None, available_clients: List[Dict] = None):
    """
    Panel wizyty FMCG wykorzystujący sprawdzoną logikę z consulting conversation contracts
    
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
        
        # Przyciski w jednej linii
        col_send, col_end = st.columns(2)
        
        with col_send:
            if st.button("📤 Wyślij", 
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
        
        with col_end:
            # Przycisk zakończenia wizyty
            if st.button("🏁 Zakończ wizytę", type="secondary", use_container_width=True, key=f"end_visit_{client_id}"):
                # Oznacz wizytę jako zakończoną
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
                        user_id=sql_user_id,  # INTEGER PRIMARY KEY z tabeli users
                        active_tab="client_profile",
                        scenario_context=f"Wizyta FMCG u {client_name}",
                        client_name=client_name,
                        key_prefix=f"visit_{client_id}",
                        available_products=available_products,
                        available_clients=available_clients
                    )
                else:
                    st.warning("⚠️ Notatnik niedostępny - użytkownik nie w bazie SQL")
    
    # =================================================================
    # VISIT COMPLETED - SAVE RESULTS
    # =================================================================
    
    else:
        st.success("🎉 Wizyta zakończona!")
        
        st.markdown("### 📦 Zamówienie")
        
        # Panel zamówienia - produkty Heinz
        st.markdown("#### Produkty do zamówienia:")
        
        # Produkty Heinz - Ketchup
        heinz_products = {
            "Heinz Ketchup 500ml": {"price": 12.50, "margin": 25},
            "Heinz Ketchup 1kg": {"price": 22.00, "margin": 25},
            "Heinz Ketchup saszetki 100szt": {"price": 45.00, "margin": 20},
            "Heinz BBQ Sauce 500ml": {"price": 15.00, "margin": 25},
            "Heinz Musztarda 500ml": {"price": 11.00, "margin": 25}
        }
        
        # Product selection
        order_items = []
        total_value = 0
        
        for product_name, product_info in heinz_products.items():
            col_prod, col_qty = st.columns([3, 1])
            with col_prod:
                st.markdown(f"**{product_name}** - {product_info['price']:.2f} PLN (marża {product_info['margin']}%)")
            with col_qty:
                qty = st.number_input(
                    "Ilość",
                    min_value=0,
                    max_value=500,
                    value=0,
                    step=1,
                    key=f"qty_{client_id}_{product_name.replace(' ', '_')}",
                    label_visibility="collapsed"
                )
                if qty > 0:
                    item_value = qty * product_info['price']
                    order_items.append({
                        "product": product_name,
                        "quantity": qty,
                        "unit_price": product_info['price'],
                        "total": item_value,
                        "margin_pct": product_info['margin']
                    })
                    total_value += item_value
        
        st.markdown("---")
        
        # Podsumowanie zamówienia
        if total_value > 0:
            st.markdown("#### 💼 Podsumowanie zamówienia:")
            st.metric("**Wartość całkowita**", f"{total_value:,.2f} PLN")
        else:
            st.info("Nie wybrano żadnych produktów do zamówienia")
        
        # Użyte narzędzia (z conversation metadata)
        st.markdown("#### 🛠️ Użyte narzędzia:")
        st.info("🚧 Lista użytych narzędzi sprzedażowych - w przygotowaniu")
        
        # Zapisz wyniki
        if st.button("💾 Zapisz i przejdź dalej", type="primary", use_container_width=True, key=f"save_visit_{client_id}"):
            # Get conversation messages for analysis
            conv_state = st.session_state.get(conversation_key, {})
            messages = conv_state.get("messages", [])
            
            # Update client data
            client["last_visit_day"] = game_state.get("current_day", 0)
            client["last_visit_date"] = datetime.now().isoformat()
            
            # Update client status - PROSPECT becomes ACTIVE after first order
            if client.get("status") == "PROSPECT" and total_value > 0:
                client["status"] = "ACTIVE"
                client["status_since"] = datetime.now().isoformat()
                st.success("🎉 Klient zmienił status: PROSPECT → ACTIVE!")
            
            # Update visits count
            client["visits_count"] = client.get("visits_count", 0) + 1
            
            # Save reputation BEFORE change (for accurate display)
            reputation_before = client.get("reputation", 50)
            
            # Calculate reputation change based on conversation and order
            # Reputacja: skala 0-100, wartość początkowa 50 (neutralna)
            # Budowanie reputacji jest powolne i wymaga wielu wizyt
            reputation_change = 2  # Baza za wizytę (mała zmiana)
            
            if total_value > 0:
                # Bonus based on order value (umiarkowany)
                if total_value >= 500:
                    reputation_change += 5  # Duże zamówienie: razem +7
                elif total_value >= 200:
                    reputation_change += 3  # Średnie zamówienie: razem +5
                else:
                    reputation_change += 1  # Małe zamówienie: razem +3
            
            # Apply reputation change (max 100, min 0)
            client["reputation"] = min(100, max(0, reputation_before + reputation_change))
            
            # ====================================================================
            # EXTRACT DISCOVERED INFO FROM CONVERSATION USING AI
            # ====================================================================
            
            if "discovered_info" not in client:
                client["discovered_info"] = {}
            
            discovered = client["discovered_info"]
            
            # Use AI to extract what client actually said in conversation
            try:
                from utils.fmcg_ai_conversation import extract_discovered_info_from_conversation
                
                st.info("🤖 Analizuję rozmowę i wyciągam informacje o kliencie...")
                
                new_discoveries = extract_discovered_info_from_conversation(
                    conversation_messages=messages,
                    client=client,
                    current_discovered_info=discovered
                )
                
                # DEBUG: Show what AI found
                if new_discoveries:
                    with st.expander("🔍 DEBUG: Co AI znalazło w rozmowie", expanded=False):
                        st.json(new_discoveries)
                
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
                            st.success(f"✅ Odkryto potencjał ketchupowy: {monthly_kg} kg/mies")
                        else:
                            st.info("💡 Potencjał ketchupowy już był znany")
                    else:
                        # Regular discovered_info field
                        if discovered.get(field) is None:  # Only if not discovered yet
                            discovered[field] = value
                            discoveries_count += 1
                            
                            # Show discovery notification
                            field_labels = {
                                "personality_description": "Opis osobowości",
                                "decision_priorities": "Priorytety decyzyjne",
                                "main_customers": "Główni klienci sklepu",
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
                st.warning(f"⚠️ Nie udało się przeanalizować rozmowy: {e}")
                import traceback
                st.code(traceback.format_exc())
            
            # Calculate knowledge level based on discovered fields count
            from utils.fmcg_ai_conversation import calculate_knowledge_level
            client["knowledge_level"] = calculate_knowledge_level(discovered)
            
            # Build conversation transcript for history
            conversation_transcript = "\n\n".join([
                f"{'🎮 Handlowiec' if msg['role'] == 'user' else '🏪 ' + client_name}: {msg['content']}"
                for msg in messages
            ])
            
            # Add to visit history
            if "visit_history" not in client:
                client["visit_history"] = []
            
            visit_record = {
                "day": game_state.get("current_day", 0),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "order_value": total_value,
                "order_items": order_items,
                "reputation_change": reputation_change,
                "reputation_after": client["reputation"],
                "knowledge_level_after": client["knowledge_level"],
                "discoveries_count": discoveries_count if 'discoveries_count' in locals() else 0,
                "new_discoveries": list(new_discoveries.keys()) if 'new_discoveries' in locals() else [],
                "conversation_transcript": conversation_transcript,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            client["visit_history"].append(visit_record)
            
            # Update sales stats
            if total_value > 0:
                game_state["total_sales"] = game_state.get("total_sales", 0) + total_value
                # Calculate weighted margin
                total_margin = sum(item["total"] * item["margin_pct"] / 100 for item in order_items)
                game_state["total_margin"] = game_state.get("total_margin", 0) + total_margin
            
            # Update weekly/monthly stats
            game_state["visits_this_week"] = game_state.get("visits_this_week", 0) + 1
            
            # Calculate and deduct energy cost
            from utils.fmcg_mechanics import calculate_visit_energy_cost
            distance = client.get("distance_from_base", client.get("distance_km", 0))
            energy_cost = calculate_visit_energy_cost(distance, visit_duration_minutes=45)
            
            current_energy = game_state.get("energy", 100)
            new_energy = max(0, current_energy - energy_cost)
            game_state["energy"] = new_energy
            
            # Mark visit as completed
            completed_visits = game_state.get("completed_visits_today", [])
            if client_id not in completed_visits:
                completed_visits.append(client_id)
                game_state["completed_visits_today"] = completed_visits
            
            # IMPORTANT: Also update session_state for route tracking
            if hasattr(st.session_state, 'completed_visits_today'):
                if client_id not in st.session_state.completed_visits_today:
                    st.session_state.completed_visits_today.append(client_id)
            else:
                st.session_state.completed_visits_today = [client_id]
            
            # Update clients dict in game_state
            if "clients" not in game_state:
                game_state["clients"] = {}
            game_state["clients"][client_id] = client
            
            # Save to database (with correct parameters)
            try:
                from utils.fmcg_mechanics import update_fmcg_game_state_sql
                update_fmcg_game_state_sql(username, game_state, game_state["clients"])
                
                # Clear conversation state BEFORE showing success & rerun
                if conversation_key in st.session_state:
                    del st.session_state[conversation_key]
                
                # Clear visit_saved flag (in case it exists from before)
                if f"visit_saved_{client_id}" in st.session_state:
                    del st.session_state[f"visit_saved_{client_id}"]
                
                st.success("✅ Wizyta zapisana!")
                
                # Show summary before continuing
                st.markdown("---")
                st.markdown("### 📊 Podsumowanie wizyty:")
                st.markdown(f"**Reputacja:** {client.get('reputation', 0)}/100 (+{reputation_change})")
                st.markdown(f"**Poziom znajomości:** {client.get('knowledge_level', 0)}⭐ ")
                st.markdown(f"**Status:** {client.get('status', 'PROSPECT')}")
                st.markdown(f"**Energia:** {new_energy}% (-{energy_cost}%) 🔋")
                if total_value > 0:
                    st.markdown(f"**Zamówienie:** {total_value:.2f} PLN")
                st.markdown("---")
                
                # Check if there are more visits on route
                if hasattr(st.session_state, 'planned_route') and st.session_state.planned_route:
                    remaining = [cid for cid in st.session_state.planned_route if cid not in st.session_state.completed_visits_today]
                    if remaining:
                        next_client_name = clients.get(remaining[0], {}).get('name', remaining[0])
                        if st.button("➡️ Przejdź do kolejnej wizyty", type="primary", use_container_width=True):
                            st.rerun()
                    else:
                        st.info("🎉 Wszystkie wizyty na trasie ukończone!")
                        if st.button("🏠 Wróć do listy klientów", type="primary", use_container_width=True):
                            st.rerun()
                else:
                    if st.button("🏠 Wróć do listy klientów", type="primary", use_container_width=True):
                        st.rerun()
            except Exception as e:
                st.error(f"Błąd zapisu: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
