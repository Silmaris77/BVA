"""
🎓 Sales Conversation Trainer - narzędzie treningowe do ćwiczenia rozmów handlowych

To jest wersja treningowa panelu wizyt - pozwala ćwiczyć rozmowy handlowe
bez wpływu na stan gry (bez kosztu energii, bez zapisywania do SQL).
"""

import streamlit as st
from typing import Dict, List
import time
from datetime import datetime
from utils.fmcg_ai_conversation import conduct_fmcg_conversation
from utils.notes_panel import render_notes_panel
from data.users_new import get_current_user_data
from utils.user_helpers import get_user_sql_id
from utils.fmcg_conviction_ai import evaluate_sales_argument


def render_sales_conversation_trainer(client_id: str, clients: Dict, username: str, 
                                      available_products: List[Dict] = None, 
                                      available_clients: List[Dict] = None):
    """
    Narzędzie treningowe do ćwiczenia rozmów handlowych FMCG
    
    Args:
        client_id: ID klienta do treningu
        clients: Słownik wszystkich klientów
        username: Nazwa użytkownika
        available_products: Lista produktów dla notatnika
        available_clients: Lista klientów dla notatnika
    """
    client = clients.get(client_id, {})
    client_name = client.get('name', client_id)
    
    # Initialize conversation state
    conversation_key = f"trainer_conversation_{client_id}"
    if conversation_key not in st.session_state:
        st.session_state[conversation_key] = {
            "messages": [],
            "training_started": True,
            "training_completed": False,
            "current_turn": 1
        }
    
    conv_state = st.session_state[conversation_key]
    current_turn = conv_state.get("current_turn", 1)
    
    # =================================================================
    # HEADER
    # =================================================================
    
    st.markdown("## 🎓 Sales Conversation Trainer")
    st.info("💡 **Tryb treningowy:** Ta rozmowa nie wpływa na stan gry. Ćwicz bez konsekwencji!")
    
    # Pobierz avatar właściciela
    avatar = client.get("avatar", "👤")
    owner_name = client.get("owner", client.get("owner_name", ""))
    
    st.markdown(f"### 💬 Trening z {client_name}")
    if owner_name:
        st.caption(f"{avatar} Właściciel: **{owner_name}**")
    
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
    
    if not conv_state["training_completed"]:
        # Show conversation history
        for msg in conv_state["messages"]:
            if msg["role"] == "assistant":
                # AI klienta
                timestamp = msg.get("timestamp", "")
                content = msg.get("content", "")
                st.markdown(f"""
                <div style='background: #f8fafc; padding: 16px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid #3b82f6;'>
                    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                        <span style='font-size: 24px; margin-right: 8px;'>{avatar}</span>
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
                            <div style='font-weight: 600; color: #1e293b;'>Ty (trening)</div>
                            <div style='font-size: 11px; color: #64748b;'>{timestamp}</div>
                        </div>
                    </div>
                    <div style='color: #1e3a8a; line-height: 1.6;'>{content}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # =================================================================
        # INPUT GRACZA
        # =================================================================
        
        st.markdown("---")
        
        # Wskazówki kontekstowe - tylko przy pierwszej turze
        if current_turn == 1:
            st.info(f"💡 **Cel treningu:** Przećwicz rozmowę z {client_name}. AI będzie grać klienta i reagować na Twoje argumenty.")
        
        # Klucze dla transkrypcji i wersjonowania
        transcription_key = f"trainer_transcription_{client_id}"
        transcription_version_key = f"trainer_transcription_version_{client_id}"
        last_audio_hash_key = f"trainer_last_audio_hash_{client_id}"
        
        # Inicjalizacja
        st.session_state.setdefault(transcription_key, "")
        st.session_state.setdefault(transcription_version_key, 0)
        st.session_state.setdefault(last_audio_hash_key, None)
        
        # Counter for recorder key to ensure fresh recorder each time
        recorder_counter_key = f"trainer_audio_recorder_counter_{client_id}"
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
            key=f"trainer_audio_recorder_{client_id}_{st.session_state[recorder_counter_key]}"
        )
        
        # Use recorded audio or file upload
        audio_data = None
        if audio_bytes_recorded:
            # Convert bytes to file-like object
            import io
            audio_data = io.BytesIO(audio_bytes_recorded)
            audio_data.name = "recording.wav"
            st.success("✅ Nagranie zakończone! Przetwarzam...")
            # Increment counter so next recorder is fresh
            st.session_state[recorder_counter_key] += 1
        
        # Przetwarzanie nagrania audio
        if audio_data is not None:
            import hashlib
            
            audio_bytes = audio_data.getvalue() if hasattr(audio_data, 'getvalue') else audio_data.read()
            audio_hash = hashlib.md5(audio_bytes).hexdigest()
            
            if audio_hash != st.session_state[last_audio_hash_key]:
                st.session_state[last_audio_hash_key] = audio_hash
                
                import speech_recognition as sr
                import tempfile
                import os
                from pydub import AudioSegment
                
                with st.spinner("🤖 Rozpoznaję mowę..."):
                    try:
                        # Detect file extension
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
                            # Convert to WAV format for speech recognition
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
        text_area_key = f"trainer_input_{client_id}_{current_turn}_v{st.session_state[transcription_version_key]}"
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
            "✍️ Twoja odpowiedź:",
            value=current_text,
            height=dynamic_height,
            key=text_area_key,
            placeholder="Mów przez mikrofon lub pisz tutaj...",
            on_change=sync_textarea_to_state
        )
        
        # Przyciski w jednej linii
        col_send, col_restart, col_end = st.columns(3)
        
        with col_send:
            if st.button("📤 Wyślij", 
                        type="primary", 
                        use_container_width=True,
                        disabled=not player_message.strip(),
                        key=f"send_trainer_{client_id}_{current_turn}"):
                if player_message.strip():
                    with st.spinner("🤖 AI analizuje Twoją odpowiedź i generuje reakcję..."):
                        # Dodaj wiadomość gracza
                        conv_state["messages"].append({
                            "role": "user",
                            "content": player_message,
                            "timestamp": datetime.now().strftime("%H:%M")
                        })
                        
                        # AI generuje odpowiedź klienta
                        try:
                            ai_response, metadata = conduct_fmcg_conversation(
                                client=client,
                                player_message=player_message,
                                conversation_history=[],
                                current_messages=conv_state["messages"]
                            )
                            
                            # Dodaj odpowiedź AI (klient mówi naturalnie)
                            conv_state["messages"].append({
                                "role": "assistant",
                                "content": ai_response,
                                "timestamp": datetime.now().strftime("%H:%M")
                            })
                            
                        except Exception as e:
                            # Zapisz błąd jako wiadomość AI
                            error_msg = f"❌ Przepraszam, wystąpił błąd podczas generowania odpowiedzi.\n\nSzczegóły: {str(e)[:200]}"
                            conv_state["messages"].append({
                                "role": "assistant",
                                "content": error_msg,
                                "timestamp": datetime.now().strftime("%H:%M")
                            })
                        
                        # Inkrementuj turę
                        conv_state["current_turn"] += 1
                        
                        # Wyczyść transkrypcję dla nowej wiadomości
                        st.session_state[transcription_key] = ""
                        st.session_state[transcription_version_key] += 1
                        
                        st.rerun()
        
        with col_restart:
            if st.button("🔄 Od nowa", type="secondary", use_container_width=True, key=f"restart_trainer_{client_id}"):
                # Wyczyść całą rozmowę
                st.session_state[conversation_key] = {
                    "messages": [],
                    "training_started": True,
                    "training_completed": False,
                    "current_turn": 1
                }
                st.session_state[transcription_key] = ""
                st.session_state[transcription_version_key] += 1
                st.rerun()
        
        with col_end:
            # Przycisk zakończenia treningu
            if st.button("🏁 Zakończ trening", type="secondary", use_container_width=True, key=f"end_trainer_{client_id}"):
                # Oznacz trening jako zakończony
                conv_state["training_completed"] = True
                st.rerun()
        
        # Notatnik dostępny w trakcie treningu
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
                        scenario_context=f"Trening z {client_name}",
                        client_name=client_name,
                        key_prefix=f"trainer_{client_id}",
                        available_products=available_products,
                        available_clients=available_clients
                    )
                else:
                    st.warning("⚠️ Notatnik niedostępny - użytkownik nie w bazie SQL")
    
    # =================================================================
    # TRAINING COMPLETED - SHOW SUMMARY
    # =================================================================
    
    else:
        st.success("🎉 Trening zakończony!")
        
        st.markdown("### 📊 Podsumowanie treningu")
        
        # Statystyki rozmowy
        total_turns = len([m for m in conv_state["messages"] if m["role"] == "user"])
        st.metric("Liczba tur rozmowy", total_turns)
        
        # Oceń jakość rozmowy treningowej
        st.markdown("#### 🤖 Ocena AI")
        st.info("🚧 Funkcja oceny rozmowy treningowej - w przygotowaniu")
        
        # TODO: Tutaj może być bardziej szczegółowa ocena niż w normalnej wizycie
        # Np. punkty za:
        # - Odkrywanie potrzeb (Discovery)
        # - Prezentację produktu (Pitch)
        # - Odpowiadanie na obiekcje (Handling Objections)
        # - Zamknięcie rozmowy (Closing)
        
        # Zapisz transkrypt do notatek (opcjonalnie)
        if st.button("📝 Zapisz transkrypt do notatek", type="secondary", use_container_width=True):
            st.info("🚧 Funkcja zapisu transkryptu - w przygotowaniu")
        
        # Restart lub wyjście
        col_restart2, col_exit = st.columns(2)
        
        with col_restart2:
            if st.button("🔄 Nowy trening", type="primary", use_container_width=True, key="restart_training_final"):
                # Wyczyść całą rozmowę
                st.session_state[conversation_key] = {
                    "messages": [],
                    "training_started": True,
                    "training_completed": False,
                    "current_turn": 1
                }
                st.session_state[transcription_key] = ""
                st.session_state[transcription_version_key] += 1
                st.rerun()
        
        with col_exit:
            if st.button("🏠 Wróć do narzędzi", type="secondary", use_container_width=True, key="exit_training"):
                # Wyczyść stan treningu
                if conversation_key in st.session_state:
                    del st.session_state[conversation_key]
                st.rerun()
