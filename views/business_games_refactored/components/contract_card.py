"""
📋 CONTRACT CARD COMPONENTS

Moduł zawierający komponenty kart kontraktów dla Business Games.
Wyekstrahowane z business_games.py (KROK 4).

Funkcje:
- render_active_contract_card - Renderuje kartę aktywnego kontraktu
- render_decision_tree_contract - Interaktywny kontrakt drzewa decyzji
- render_conversation_contract - Kontrakt rozmowy z AI
- render_speed_challenge_contract - Kontrakt z limitem czasu
- render_contract_card - Renderuje kartę dostępnego kontraktu do przyjęcia
- render_completed_contract_card - Renderuje kartę ukończonego kontraktu
"""

import streamlit as st
from datetime import datetime, timedelta
import time

from views.business_games_refactored.helpers import (
    get_contract_reward_coins,
    get_contract_reward_reputation
)


def render_active_contract_card(contract, username, user_data, bg_data, contract_index=0):
    """Renderuje profesjonalną kartę aktywnego kontraktu w stylu game UI"""
    
    contract_id = contract.get('id', 'UNKNOWN')
    print(f"DEBUG render_active_contract_card: WEJŚCIE - contract_id={contract_id}, index={contract_index}")
    
    if not contract_id or contract_id == 'UNKNOWN':
        st.error(f"⚠️ BŁĄD: Kontrakt bez ID! Index: {contract_index}, Dane: {contract}")
        return
    
    # Backward compatibility: ai_conversation → conversation
    contract_type = contract.get("contract_type")
    if contract_type == "ai_conversation":
        contract_type = "conversation"
    
    # Sprawdź czy to Decision Tree Contract
    if contract_type == "decision_tree":
        industry_id = bg_data.get("industry", "consulting")
        render_decision_tree_contract(contract, username, user_data, bg_data, industry_id, contract_index=contract_index)
        return
    
    # Sprawdź czy to Conversation Contract
    if contract_type == "conversation":
        industry_id = bg_data.get("industry", "consulting")
        render_conversation_contract(contract, username, user_data, bg_data, industry_id, contract_index=contract_index)
        return
    
    # Sprawdź czy to Speed Challenge Contract
    if contract_type == "speed_challenge":
        industry_id = bg_data.get("industry", "consulting")
        render_speed_challenge_contract(contract, username, user_data, bg_data, industry_id, contract_index=contract_index)
        return
    
    # Dla standardowych kontraktów - inicjalizuj wersję transkrypcji (do śledzenia zmian)
    transcription_version_key = f"transcription_version_{contract_id}"
    if transcription_version_key not in st.session_state:
        st.session_state[transcription_version_key] = 0
    
    # Standardowy kontrakt (pisanie/mówienie)
    with st.container():
        # Oblicz pozostały czas
        deadline = datetime.strptime(contract["deadline"], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        time_left = deadline - now
        hours_left = int(time_left.total_seconds() / 3600)
        
        # Kolory i ikony dla deadline
        if hours_left > 24:
            deadline_status = "✅ Na czasie"
            deadline_bg = "linear-gradient(135deg, #10b981 0%, #059669 100%)"
        elif hours_left > 6:
            deadline_status = "🟡 Kończy się"
            deadline_bg = "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)"
        else:
            deadline_status = "🔴 Pilne!"
            deadline_bg = "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"
        
        # Sprawdź czy kontrakt był dotknięty zdarzeniem
        event_affected = contract.get("affected_by_event")
        
        # Ustal kolor akcent na podstawie typu zdarzenia
        if event_affected:
            if event_affected.get("type") == "deadline_reduction":
                accent_color = "#ef4444"
                glow = "0 0 20px rgba(239, 68, 68, 0.4)"
            elif event_affected.get("type") == "deadline_extension":
                accent_color = "#10b981"
                glow = "0 0 20px rgba(16, 185, 129, 0.4)"
            else:
                accent_color = "#667eea"
                glow = "0 0 20px rgba(102, 126, 234, 0.3)"
        else:
            accent_color = "#667eea"
            glow = "0 0 20px rgba(102, 126, 234, 0.3)"
        
        # Karta kontraktu - profesjonalny design
        difficulty_stars = "🔥" * contract['trudnosc']
        reward_min = contract['nagroda_base']
        reward_max = contract['nagroda_5star']
        
        # Render HTML card
        # Przygotuj HTML dla alertu wydarzenia (jeśli jest)
        event_alert_html = ""
        if event_affected:
            if event_affected.get("type") == "deadline_reduction":
                alert_bg = "#fef2f2"
                alert_border = "#ef4444"
                alert_icon = "⚠️"
                alert_text = f"<strong>Zdarzenie: {event_affected.get('event_title')}</strong><br>Deadline skrócony o {event_affected.get('days_reduced')} dzień!"
            elif event_affected.get("type") == "deadline_extension":
                alert_bg = "#f0fdf4"
                alert_border = "#10b981"
                alert_icon = "✨"
                alert_text = f"<strong>Zdarzenie: {event_affected.get('event_title')}</strong><br>Deadline przedłużony o {event_affected.get('days_added')} dzień!"
            elif event_affected.get("type") == "deadline_boost":
                alert_bg = "#f0f9ff"
                alert_border = "#3b82f6"
                alert_icon = "⚡"
                alert_text = f"<strong>Boost Energii: {event_affected.get('event_title')}</strong><br>Bonus +{event_affected.get('days_added')} dni do realizacji!"
            elif event_affected.get("type") == "renegotiation":
                alert_bg = "#eff6ff"
                alert_border = "#3b82f6"
                alert_icon = "🔄"
                reward_change = int((event_affected.get('reward_multiplier', 1.0) - 1) * 100)
                time_bonus = event_affected.get('time_bonus', 0)
                if reward_change < 0 and time_bonus > 0:
                    alert_text = f"<strong>Renegocjacja: {event_affected.get('event_title')}</strong><br>Nagroda {reward_change}%, ale +{time_bonus} dni na realizację!"
                else:
                    alert_text = f"<strong>Renegocjacja: {event_affected.get('event_title')}</strong><br>Zmieniono warunki kontraktu"
            else:
                alert_bg = "#f9fafb"
                alert_border = "#9ca3af"
                alert_icon = "ℹ️"
                alert_text = f"<strong>Wydarzenie aktywne</strong>"
            
            event_alert_html = f"""<div style="background: {alert_bg}; border-left: 4px solid {alert_border}; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px; display: flex; align-items: center; gap: 12px;"><div style="font-size: 24px;">{alert_icon}</div><div style="font-size: 13px; color: #1e293b; line-height: 1.4;">{alert_text}</div></div>"""
        
        html_content = f"""<div style="background: white; border-radius: 20px; padding: 24px; margin: 16px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.1), {glow}; border-left: 6px solid {accent_color}; transition: all 0.3s ease;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
<div style="flex: 1;">
<div style="font-size: 32px; margin-bottom: 8px;">{contract['emoji']}</div>
<h3 style="margin: 0; color: #1e293b; font-size: 20px; font-weight: 700;">{contract['tytul']}</h3>
<p style="margin: 4px 0 0 0; color: #64748b; font-size: 14px;">Klient: <strong>{contract['klient']}</strong> • {contract['kategoria']}</p>
</div>
<div style="background: {deadline_bg}; color: white; padding: 12px 20px; border-radius: 12px; text-align: center; min-width: 120px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
<div style="font-size: 24px; font-weight: 700; margin-bottom: 4px;">{hours_left}h</div>
<div style="font-size: 11px; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">{deadline_status}</div>
</div>
</div>
<div style="background: #f8f9fa; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
<div style="color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; font-weight: 600;">📝 Opis sytuacji</div>
<div style="color: #334155; font-size: 14px; line-height: 1.6;">{contract['opis']}</div>
</div>
{event_alert_html}
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 16px; padding-top: 16px; border-top: 1px solid #e2e8f0;">
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Nagroda</div>
<div style="color: #f59e0b; font-size: 20px; font-weight: 700;">💰 {reward_min}-{reward_max}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Trudność</div>
<div style="font-size: 20px;">{difficulty_stars}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Reputacja</div>
<div style="color: #8b5cf6; font-size: 20px; font-weight: 700;">⭐ +{contract['reputacja']}</div>
</div>
</div>
</div>"""
        
        st.markdown(html_content, unsafe_allow_html=True)
        
        # ROZWIĄZANIE - expander (domyślnie zwinięty dla kompaktowego widoku)
        with st.expander("✍️ Pracuj nad rozwiązaniem", expanded=False):
            # Wyświetl zadanie na górze
            st.markdown("### 🎯 Zadanie")
            st.markdown(contract['zadanie'])
            st.markdown("---")
            
            # ANTI-CHEAT: Zapisz czas rozpoczęcia pisania
            solution_start_key = f"solution_start_{contract['id']}"
            if solution_start_key not in st.session_state:
                st.session_state[solution_start_key] = datetime.now()
            
            # ANTI-CHEAT: Tracking paste events
            paste_events_key = f"paste_events_{contract['id']}"
            if paste_events_key not in st.session_state:
                st.session_state[paste_events_key] = []
            
            # Wprowadzanie rozwiązania - mówienie + pisanie
            st.markdown("### 📝 Twoje rozwiązanie")
            
            solution_key = f"solution_{contract['id']}"
            
            # Inicjalizuj tylko transcription_key (version_key jest już zainicjalizowany wyżej)
            transcription_key = f"transcription_{contract['id']}"
            if transcription_key not in st.session_state:
                st.session_state[transcription_key] = ""
            
            st.markdown("**🎤 Nagraj** (wielokrotnie, jeśli chcesz) **lub ✍️ pisz bezpośrednio w polu poniżej:**")
            
            # Wyświetl komunikat sukcesu jeśli był (po rerun)
            success_key = f"transcription_success_{contract_id}"
            if st.session_state.get(success_key, False):
                st.success("✅ Transkrypcja zakończona! Tekst pojawił się w polu poniżej.")
                del st.session_state[success_key]  # Usuń flagę aby nie pokazywać ponownie
            
            # Klucz musi być UNIKALNY - dodajmy render_id aby zapobiec duplikacji
            # Jeśli render_id nie istnieje dla tego kontraktu, stwórz nowy
            render_id_key = f"render_id_{contract_id}_{contract_index}"
            if render_id_key not in st.session_state:
                import random
                st.session_state[render_id_key] = random.randint(100000, 999999)
            
            render_id = st.session_state[render_id_key]
            audio_key = f"audio_{contract_id}_{contract_index}_{render_id}"
            
            # Klucz do śledzenia ostatnio przetworzonego audio (hash)
            last_audio_hash_key = f"last_audio_hash_{contract_id}"
            if last_audio_hash_key not in st.session_state:
                st.session_state[last_audio_hash_key] = None
            
            audio_data = st.audio_input(
                "🎤 Nagrywanie...",
                key=audio_key
            )
            
            # Przetwarzaj TYLKO jeśli to NOWE audio (nie było jeszcze przetworzone)
            if audio_data is not None:
                import hashlib
                
                # Oblicz hash audio
                audio_bytes = audio_data.getvalue()
                current_audio_hash = hashlib.md5(audio_bytes).hexdigest()
                
                # Sprawdź czy to nowe audio (inny hash niż ostatnio)
                if current_audio_hash != st.session_state[last_audio_hash_key]:
                    # NOWE audio - przetwarzaj!
                    st.session_state[last_audio_hash_key] = current_audio_hash
                    
                    import speech_recognition as sr
                    import tempfile
                    import os
                    from pydub import AudioSegment
                    
                    with st.spinner("🤖 Rozpoznaję mowę..."):
                        try:
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                                tmp_file.write(audio_data.getvalue())
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
                                    
                                    # Konfiguracja Gemini (z secrets.toml)
                                    api_key = st.secrets["API_KEYS"]["gemini"]
                                    genai.configure(api_key=api_key)
                                    
                                    # Dodaj interpunkcję - użyj najnowszego stabilnego modelu
                                    model = genai.GenerativeModel("models/gemini-2.5-flash")
                                    prompt = f"""Dodaj interpunkcję (kropki, przecinki, pytajniki, wykrzykniki) do poniższego tekstu.
Nie zmieniaj słów, tylko dodaj znaki interpunkcyjne. Zachowaj strukturę i podział na zdania.
Zwróć tylko poprawiony tekst, bez dodatkowych komentarzy.

Tekst do poprawy:
{transcription}"""
                                    
                                    response = model.generate_content(prompt)
                                    transcription_with_punctuation = response.text.strip()
                                    
                                    # Nie wyświetlaj komunikatu tutaj - będzie w session_state
                                    transcription = transcription_with_punctuation
                                    
                                except Exception as gemini_error:
                                    # Nie wyświetlaj ostrzeżenia - kontynuuj z podstawową transkrypcją
                                    pass
                                
                                # DOPISZ do istniejącego tekstu (zamiast nadpisywać)
                                existing_text = st.session_state.get(transcription_key, "")
                                if existing_text.strip():
                                    # Jeśli jest już jakiś tekst, dodaj nową linię i dopisz
                                    st.session_state[transcription_key] = existing_text.rstrip() + "\n\n" + transcription
                                else:
                                    # Jeśli to pierwsze nagranie, po prostu zapisz
                                    st.session_state[transcription_key] = transcription
                                
                                st.session_state[transcription_version_key] += 1
                                
                                # Ustaw flagę sukcesu (wyświetlimy komunikat po rerun)
                                st.session_state[f"transcription_success_{contract_id}"] = True
                                
                                # NIE kasuj flagi rendered_ - po prostu zrób rerun
                                # text_area zostanie zaktualizowany dzięki zmianie klucza (wersja)
                                st.rerun()
                            
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
            
            current_text = st.session_state.get(transcription_key, contract.get("solution", ""))
            
            # Klucz musi zawierać render_id aby zapobiec duplikacji
            # oraz wersję transkrypcji aby wymusić odświeżenie po nagraniu
            text_area_key = f"solution_{contract_id}_{contract_index}_{render_id}_v{st.session_state[transcription_version_key]}"
            
            solution = st.text_area(
                "📝 Możesz edytować transkrypcję lub pisać bezpośrednio:",
                value=current_text,
                height=400,
                key=text_area_key,
                placeholder="Nagrywaj wielokrotnie lub pisz bezpośrednio tutaj..."
            )
            
            # Zapisz aktualną wartość solution do session_state
            st.session_state[transcription_key] = solution
            
            # ANTI-CHEAT: Dodaj JavaScript do śledzenia wklejania
            st.markdown(f"""
            <script>
            (function() {{
                const textarea = document.querySelector('textarea[aria-label="📝 Możesz edytować transkrypcję lub pisać bezpośrednio:"]');
                if (textarea) {{
                    textarea.addEventListener('paste', function(e) {{
                        const pastedText = (e.clipboardData || window.clipboardData).getData('text');
                        const pasteLength = pastedText.length;
                        const totalLength = textarea.value.length + pasteLength;
                        
                        // Wyślij event do Streamlit (przez hidden input)
                        const event = {{
                            'length': pasteLength,
                            'total_solution_length': totalLength,
                            'timestamp': new Date().toISOString()
                        }};
                        
                        console.log('Paste detected:', event);
                        
                        // Zapisz w localStorage (Streamlit może to odczytać)
                        const existingEvents = JSON.parse(localStorage.getItem('paste_events_{contract['id']}') || '[]');
                        existingEvents.push(event);
                        localStorage.setItem('paste_events_{contract['id']}', JSON.stringify(existingEvents));
                    }});
                }}
            }})();
            </script>
            """, unsafe_allow_html=True)
            
            if solution is None:
                solution = ""
            
            word_count = len(solution.split())
            min_words = contract.get('min_slow', 300)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                progress = min(100, int((word_count / min_words) * 100))
                st.progress(progress / 100)
                st.caption(f"Liczba słów: {word_count}/{min_words} ({progress}%)")
            
            # Import funkcji z business_game
            from utils.business_game import submit_contract_solution
            from data.users_new import save_user_data
            from views.business_games_refactored.helpers import play_coin_sound
            
            with col2:
                if st.button("✅ Prześlij rozwiązanie", key=f"submit_{contract_id}_{contract_index}", type="primary"):
                    if word_count < min_words:
                        st.error(f"Rozwiązanie zbyt krótkie! Minimum: {min_words} słów")
                    else:
                        # Pobierz dane anti-cheat
                        start_time = st.session_state.get(solution_start_key)
                        paste_events = st.session_state.get(paste_events_key, [])
                        
                        # Prześlij rozwiązanie z danymi anti-cheat
                        updated_user_data, success, message, _ = submit_contract_solution(
                            user_data, contract['id'], solution,
                            start_time=start_time,
                            paste_events=paste_events if paste_events else None
                        )
                        
                        if success:
                            user_data.update(updated_user_data)
                            save_user_data(username, user_data)
                            
                            # Wyczyść tracking anti-cheat
                            if solution_start_key in st.session_state:
                                del st.session_state[solution_start_key]
                            if paste_events_key in st.session_state:
                                del st.session_state[paste_events_key]
                            
                            # 💰 Odtwórz dźwięk monet!
                            play_coin_sound()
                            
                            st.success(message)
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(message)


def render_decision_tree_contract(contract, username, user_data, bg_data, industry_id="consulting", contract_index=0):
    """Renderuje interaktywny Decision Tree Contract"""
    from utils.decision_tree_engine import (
        initialize_decision_tree_state,
        get_current_node,
        make_choice,
        calculate_final_score,
        reset_decision_tree,
        get_decision_tree_summary,
        calculate_replay_value
    )
    from utils.business_game import complete_contract_decision_tree
    from views.business_games_refactored.helpers import save_game_data
    from data.users_new import save_user_data
    
    contract_id = contract["id"]
    nodes = contract.get("nodes", {})
    start_node_id = contract.get("start_node", "scene_1")
    scoring_config = contract.get("scoring", {})
    
    # Initialize state
    initialize_decision_tree_state(contract_id, start_node_id)
    
    # Check if completed
    is_completed = st.session_state.get(f"dt_{contract_id}_completed", False)
    
    if is_completed:
        # Show final results
        final_results = calculate_final_score(contract_id, nodes, scoring_config)
        replay_info = calculate_replay_value(contract_id, nodes)
        
        st.success(f"🎉 **Ukończono Decision Tree Contract!**")
        
        # Beautiful results card
        ending_node = nodes.get(final_results["ending_id"])
        outcome = final_results.get("outcome", {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⭐ Gwiazdki", f"{final_results['stars']}/5")
        with col2:
            st.metric("🎯 Punkty", final_results['total_points'])
        with col3:
            st.metric("🛤️ Długość ścieżki", final_results['path_length'])
        
        # Ending card
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 24px; border-radius: 16px; margin: 16px 0;'>
            <h2 style='margin: 0 0 12px 0;'>{final_results['ending_title']}</h2>
            <p style='margin: 0; font-size: 14px; line-height: 1.6; opacity: 0.95;'>
                {ending_node.get('text', '') if ending_node else ''}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Outcome details
        if outcome:
            st.markdown("### 📊 Konsekwencje Twoich Decyzji")
            outcome_cols = st.columns(3)
            col_idx = 0
            for key, value in outcome.items():
                if key not in ['points', 'rating']:
                    with outcome_cols[col_idx % 3]:
                        if isinstance(value, (int, float)):
                            st.metric(key.replace('_', ' ').title(), f"{value:+,}" if value != 0 else str(value))
                        else:
                            st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
                        col_idx += 1
        
        # Journey summary
        with st.expander("🗺️ Zobacz swoją ścieżkę decyzji"):
            summary = get_decision_tree_summary(contract_id)
            st.text(summary)
        
        # Replay value
        if replay_info['replay_recommended']:
            st.info(f"""
            🔄 **Warto zagrać ponownie!**
            
            - Odkryłeś **1** z **{replay_info['total_endings']}** zakończeń
            - To {'nie było najlepsze zakończenie' if not replay_info['is_best_ending'] else 'było najlepsze zakończenie! 🏆'}
            - Pozostało **{replay_info['undiscovered_endings']}** innych zakończeń do odkrycia
            
            Każda ścieżka uczy innych lekcji przywództwa!
            """)
        else:
            st.success(f"""
            🏆 **Gratulacje! Osiągnąłeś najlepsze zakończenie!**
            
            Możesz zagrać ponownie aby odkryć {replay_info['undiscovered_endings']} innych zakończeń.
            """)
        
        # Action buttons
        col_action1, col_action2, col_action3 = st.columns(3)
        
        with col_action1:
            if st.button("🔄 Zagraj ponownie", use_container_width=True, key=f"replay_{contract_id}_{contract_index}"):
                reset_decision_tree(contract_id, start_node_id)
                st.rerun()
        
        with col_action2:
            if st.button("✅ Prześlij wynik", type="primary", use_container_width=True, key=f"submit_dt_{contract_id}_{contract_index}"):
                # Calculate reward based on stars
                base_reward = contract.get("nagroda_base", 500)
                reward_5star = contract.get("nagroda_5star", 1000)
                
                stars = final_results['stars']
                if stars == 5:
                    reward = reward_5star
                elif stars == 4:
                    reward = contract.get("nagroda_4star", int((base_reward + reward_5star) / 2))
                elif stars == 3:
                    reward = int((base_reward + reward_5star) / 2 * 0.8)
                elif stars == 2:
                    reward = int(base_reward * 0.8)
                else:
                    reward = base_reward
                
                # Mark contract as completed in bg_data
                updated_bg, success, message = complete_contract_decision_tree(
                    bg_data, 
                    contract_id, 
                    stars, 
                    reward, 
                    contract.get("reputacja", 20),
                    final_results,
                    user_data
                )
                
                if success:
                    save_game_data(user_data, updated_bg, industry_id)
                    save_user_data(username, user_data)
                    st.success(f"{message} 💰 +{reward} monet | ⭐ +{contract.get('reputacja', 20)} reputacji")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(message)
        
        with col_action3:
            if st.button("← Powrót", use_container_width=True, key=f"back_{contract_id}_{contract_index}"):
                st.session_state["view_contract"] = None
                st.rerun()
    
    else:
        # Show current scene
        current_node = get_current_node(contract_id, nodes)
        
        if not current_node:
            st.error("❌ Błąd: Nie znaleziono węzła w drzewie decyzji")
            return
        
        # Progress indicator
        path = st.session_state.get(f"dt_{contract_id}_path", [])
        current_points = st.session_state.get(f"dt_{contract_id}_points", 0)
        
        col_prog1, col_prog2 = st.columns([3, 1])
        with col_prog1:
            st.progress(min(len(path) / 10, 1.0), text=f"Scena {len(path) + 1}")
        with col_prog2:
            st.metric("Punkty", current_points)
        
        # Scene card
        st.markdown(f"""
        <div style='background: white; border-radius: 20px; padding: 32px; margin: 24px 0; 
                    box-shadow: 0 8px 32px rgba(0,0,0,0.12); border-left: 6px solid #667eea;'>
            <h2 style='margin: 0 0 16px 0; color: #1e293b; font-size: 24px;'>
                {current_node.get('title', 'Scena')}
            </h2>
            <div style='color: #475569; font-size: 16px; line-height: 1.8; white-space: pre-wrap;'>
                {current_node.get('text', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Choices
        if current_node.get('is_revelation'):
            # Auto-advance for revelation nodes
            st.info("ℹ️ *Mark się otwiera...*")
            time.sleep(1)
            choice = current_node['choices'][0]
            make_choice(contract_id, choice, nodes)
            st.rerun()
        else:
            st.markdown("### 🤔 Twój wybór:")
            
            for i, choice in enumerate(current_node.get('choices', [])):
                choice_text = choice['text']
                
                # Button dla każdego wyboru
                if st.button(
                    choice_text, 
                    key=f"{contract_id}_choice_{i}_{contract_index}",
                    use_container_width=True,
                    type="secondary"
                ):
                    # Make choice
                    make_choice(contract_id, choice, nodes)
                    
                    # Show immediate feedback
                    feedback = choice.get('feedback', '')
                    if feedback:
                        if '✅' in feedback or '🏆' in feedback:
                            st.success(feedback)
                        elif '❌' in feedback:
                            st.error(feedback)
                        else:
                            st.info(feedback)
                        time.sleep(1.5)
                    
                    st.rerun()
                
                st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
        
        # Show path so far
        if len(path) > 0:
            with st.expander(f"📜 Twoja dotychczasowa ścieżka ({len(path)} decyzji)"):
                for i, step in enumerate(path, 1):
                    points_color = "green" if step['points'] > 0 else "red" if step['points'] < 0 else "gray"
                    st.markdown(f"""
                    **{i}.** {step['choice_text']}  
                    <span style='color: {points_color}; font-weight: bold;'>
                        {'+' if step['points'] > 0 else ''}{step['points']} pkt
                    </span>
                    """, unsafe_allow_html=True)
                    if step.get('feedback'):
                        st.caption(step['feedback'])


def render_conversation_contract(contract, username, user_data, bg_data, industry_id="consulting", contract_index=0):
    """Renderuje interaktywny Conversation Contract - dynamiczna rozmowa z NPC"""
    
    from utils.ai_conversation_engine import (
        initialize_ai_conversation,
        get_conversation_state,
        process_player_message,
        calculate_final_conversation_score,
        reset_conversation
    )
    from views.business_games_refactored.helpers import save_game_data
    from data.users_new import save_user_data
    
    contract_id = contract["id"]
    npc_config = contract.get("npc_config", {})
    scenario_context = contract.get("scenario_context", "")
    
    # Inicjalizacja (per user!)
    conversation = get_conversation_state(contract_id, username)
    if not conversation:
        initialize_ai_conversation(contract_id, npc_config, scenario_context, username)
        conversation = get_conversation_state(contract_id, username)
    
    # Sprawdź czy zakończono
    is_completed = not conversation.get("conversation_active", True)
    
    # Sprawdź czy TTS jest dostępne
    from utils.ai_conversation_engine import TTS_AVAILABLE
    if not TTS_AVAILABLE:
        st.warning("🔇 Text-to-Speech niedostępne. Zainstaluj gTTS: `pip install gTTS`")
    
    # === NAGŁÓWEK KONTRAKTU ===
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 24px; border-radius: 16px; margin-bottom: 24px;'>
        <h2 style='margin: 0 0 8px 0;'>💬 {contract['tytul']}</h2>
        <p style='margin: 0; opacity: 0.9; font-size: 14px;'>{contract['opis']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if is_completed:
        # === WIDOK ZAKOŃCZENIA ===
        final_results = calculate_final_conversation_score(contract_id, username)
        
        st.success(f"🎉 **Rozmowa zakończona!**")
        
        # Metryki w kompaktowej karcie (jak inne kontrakty)
        stars = final_results.get('stars', 1)
        total_points = final_results.get('total_points', 0)
        
        # Oblicz nagrodę dla wyświetlenia
        reward_base = contract.get("nagroda_base", 500)
        reward_5star = contract.get("nagroda_5star", reward_base * 2)
        reward = int(reward_base + ((stars - 1) / 4.0) * (reward_5star - reward_base))
        rep_change = int(contract.get("reputacja", 20) * stars / 3)
        rep_display = f"+{rep_change}" if rep_change >= 0 else str(rep_change)
        
        st.markdown(f"""
        <div style='background: linear-gradient(to right, #f8fafc, #f1f5f9); 
                    border-left: 4px solid #3b82f6; 
                    border-radius: 8px; 
                    padding: 16px; 
                    margin: 16px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
            <div style='display: flex; justify-content: space-around; text-align: center;'>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>⭐</div>
                    <div style='font-weight: 600; color: #1e293b;'>{stars}/5</div>
                    <div style='font-size: 12px; color: #64748b;'>Ocena</div>
                </div>
                <div style='border-left: 2px solid #e2e8f0; height: 60px;'></div>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>💰</div>
                    <div style='font-weight: 600; color: #1e293b;'>{reward:,}</div>
                    <div style='font-size: 12px; color: #64748b;'>Zarobiono</div>
                </div>
                <div style='border-left: 2px solid #e2e8f0; height: 60px;'></div>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>📈</div>
                    <div style='font-weight: 600; color: #1e293b;'>{rep_display}</div>
                    <div style='font-size: 12px; color: #64748b;'>Reputacja</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Feedback od klienta (jak w innych kontraktach)
        st.markdown("---")
        st.subheader("💬 Feedback od klienta")
        
        # Buduj feedback z evaluacji (tak samo jak przy zapisywaniu kontraktu)
        messages = conversation.get("messages", [])
        all_positive = []
        all_improvements = []
        
        for msg in messages:
            if msg.get("role") == "player":
                evaluation = msg.get("evaluation", {})
                all_positive.extend(evaluation.get("positive_aspects", []))
                all_improvements.extend(evaluation.get("improvement_suggestions", []))
        
        # Sformatuj feedback jak w business_game_evaluation.py (z perspektywy NPC)
        npc_name = contract.get("npc_name", "Klient")
        feedback = f"**{npc_name}:** Dziękuję za poświęcony czas na rozmowę."
        
        if all_positive:
            feedback += "\n\n**👍 Co mi się podobało:**\n"
            feedback += "\n".join([f"• {s}" for s in all_positive[:5]])  # Top 5
        
        if all_improvements:
            feedback += "\n\n**⚠️ Co mogłoby być lepsze:**\n"
            feedback += "\n".join([f"• {i}" for i in all_improvements[:5]])  # Top 5
        
        st.info(feedback)
        
        # Link do pełnej historii
        st.info("📜 Pełne szczegóły rozmowy znajdziesz w zakładce **'📜 Historia & Wydarzenia'**")
        
        st.markdown("---")
        
        # Historia rozmowy
        with st.expander("💬 Zobacz całą rozmowę"):
            messages = conversation.get("messages", [])
            for msg in messages:
                role = msg.get("role", "")
                content = msg.get("text", msg.get("content", ""))  # Obsługa obu kluczy
                timestamp = msg.get("timestamp", "")
                audio_data = msg.get("audio")
                
                if role == "npc":
                    st.markdown(f"""
                    <div style='background: #f1f5f9; padding: 12px; border-radius: 8px; 
                                margin: 8px 0; border-left: 4px solid #667eea;'>
                        <div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'>
                            👤 <strong>{npc_config.get('name', 'NPC')}</strong> · {timestamp}
                        </div>
                        <div style='color: #1e293b;'>{content}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Odtwórz audio jeśli dostępne
                    if audio_data:
                        import base64
                        audio_bytes = base64.b64decode(audio_data)
                        st.audio(audio_bytes, format="audio/mp3")
                        
                elif role == "player":
                    content_text = msg.get("text", msg.get("content", ""))
                    st.markdown(f"""
                    <div style='background: #dbeafe; padding: 12px; border-radius: 8px; 
                                margin: 8px 0; border-left: 4px solid #3b82f6;'>
                        <div style='font-size: 12px; color: #64748b; margin-bottom: 4px;'>
                            🎮 <strong>Ty</strong> · {timestamp}
                        </div>
                        <div style='color: #1e293b;'>{content_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Przyciski akcji
        col_replay, col_submit = st.columns(2)
        with col_replay:
            if st.button("🔄 Zagraj ponownie", key=f"replay_{contract_id}_{contract_index}", use_container_width=True):
                reset_conversation(contract_id, npc_config, scenario_context, username)
                st.rerun()
        
        with col_submit:
            if st.button("✅ Zakończ kontrakt", key=f"submit_conv_{contract_id}_{contract_index}", 
                        type="primary", use_container_width=True):
                # Import funkcji calculate_final_conversation_score
                from utils.ai_conversation_engine import calculate_final_conversation_score
                
                # Znajdź kontrakt
                contract_found = next((c for c in bg_data["contracts"]["active"] if c["id"] == contract_id), None)
                if not contract_found:
                    st.error("Kontrakt nie znaleziony w aktywnych")
                else:
                    try:
                        # Pobierz wynik z engine (per user!)
                        result = calculate_final_conversation_score(contract_id, username)
                        stars = result.get("stars", 1)
                        total_points = result.get("total_points", 0)
                        metrics = result.get("metrics", {})
                        
                        # Buduj feedback jak w kontraktach standard (z 👍/⚠️)
                        conv_key = f"ai_conv_{username}_{contract_id}"
                        conv_state = st.session_state.get(conv_key, {})
                        messages = conv_state.get("messages", [])
                        
                        # Zbierz wszystkie pozytywne aspekty i sugestie z całej rozmowy
                        all_positive = []
                        all_improvements = []
                        for msg in messages:
                            if msg.get("role") == "player":
                                evaluation = msg.get("evaluation", {})
                                all_positive.extend(evaluation.get("positive_aspects", []))
                                all_improvements.extend(evaluation.get("improvement_suggestions", []))
                        
                        # Sformatuj feedback jak w business_game_evaluation.py (z perspektywy NPC)
                        npc_name = contract_found.get("npc_name", "Klient")
                        feedback_summary = f"**{npc_name}:** Dziękuję za poświęcony czas na rozmowę."
                        
                        if all_positive:
                            feedback_summary += "\n\n**👍 Co mi się podobało:**\n"
                            feedback_summary += "\n".join([f"• {s}" for s in all_positive[:5]])  # Top 5
                        
                        if all_improvements:
                            feedback_summary += "\n\n**⚠️ Co mogłoby być lepsze:**\n"
                            feedback_summary += "\n".join([f"• {i}" for i in all_improvements[:5]])  # Top 5
                        
                        # Oblicz nagrodę
                        reward_base = contract_found.get("nagroda_base", 500)
                        reward_5star = contract_found.get("nagroda_5star", reward_base * 2)
                        reward = int(reward_base + ((stars - 1) / 4.0) * (reward_5star - reward_base))
                        
                        # KRYTYCZNE: Dodaj do SALDA FIRMY (bg_data["money"]), NIE do DegenCoins!
                        bg_data["money"] = bg_data.get("money", 0) + reward
                        bg_data["firm"]["reputation"] += contract_found.get("reputacja", 20) * stars / 3
                        bg_data["stats"]["total_revenue"] += reward
                        
                        # Przenieś do completed
                        completed_contract = contract_found.copy()
                        completed_contract["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        completed_contract["rating"] = stars  # Używamy "rating" jak inne kontrakty
                        completed_contract["stars"] = stars  # Dla kompatybilności
                        completed_contract["points"] = total_points
                        completed_contract["reward"] = reward
                        completed_contract["metrics"] = metrics
                        completed_contract["feedback"] = feedback_summary
                        completed_contract["status"] = "completed"
                        
                        bg_data["contracts"]["completed"].append(completed_contract)
                        bg_data["contracts"]["active"] = [c for c in bg_data["contracts"]["active"] if c["id"] != contract_id]
                        
                        # Zaktualizuj statystyki
                        bg_data["stats"]["contracts_completed"] = bg_data["stats"].get("contracts_completed", 0) + 1
                        rating_key = f"contracts_{stars}star"
                        bg_data["stats"][rating_key] = bg_data["stats"].get(rating_key, 0) + 1
                        
                        # Dodaj transakcję
                        if "history" not in bg_data:
                            bg_data["history"] = {"transactions": [], "level_ups": []}
                        if "transactions" not in bg_data["history"]:
                            bg_data["history"]["transactions"] = []
                        
                        bg_data["history"]["transactions"].append({
                            "type": "contract_reward",
                            "amount": reward,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "description": f"Conversation: {contract_found['tytul']} ({stars}⭐)"
                        })
                        
                        # Zapisz dane
                        save_game_data(user_data, bg_data, industry_id)
                        save_user_data(username, user_data)
                        
                        st.success(f"✅ Zakończono! 💰 +{reward:,} PLN | ⭐ {stars}/5")
                        time.sleep(1)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Błąd przy zakończeniu kontraktu: {e}")
    
    else:
        # === WIDOK AKTYWNEJ ROZMOWY ===
        
        # Informacja o scenariuszu
        with st.expander("📖 Kontekst sytuacji", expanded=False):
            st.markdown(scenario_context)
        
        # Pobierz current_turn (potrzebny w logice, ale bez wyświetlania)
        current_turn = conversation.get("current_turn", 1)
        
        # === HISTORIA KONWERSACJI ===
        st.markdown("### 💬 Rozmowa")
        
        messages = conversation.get("messages", [])
        
        # Container dla wiadomości
        chat_container = st.container()
        with chat_container:
            for msg in messages:
                role = msg.get("role", "")
                content = msg.get("text", msg.get("content", ""))  # Obsługa obu kluczy
                timestamp = msg.get("timestamp", "")
                emotion = msg.get("emotion", "neutral")
                
                if role == "npc":
                    # Emotikon dla emocji NPC
                    emotion_emoji = {
                        "happy": "😊", "concerned": "😟", "frustrated": "😤",
                        "neutral": "😐", "thoughtful": "🤔", "relieved": "😌",
                        "angry": "😠", "satisfied": "😌"
                    }.get(emotion, "😐")
                    
                    st.markdown(f"""
                    <div style='background: #f1f5f9; padding: 16px; border-radius: 12px; 
                                margin: 12px 0; border-left: 4px solid #667eea; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
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
                    
                    # Odtwórz audio jeśli dostępne
                    audio_data = msg.get("audio")
                    if audio_data:
                        # Dekoduj base64 i wyświetl odtwarzacz
                        import base64
                        audio_bytes = base64.b64decode(audio_data)
                        st.audio(audio_bytes, format="audio/mp3")
                    
                elif role == "player":
                    st.markdown(f"""
                    <div style='background: #dbeafe; padding: 16px; border-radius: 12px; 
                                margin: 12px 0; border-left: 4px solid #3b82f6; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
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
                    
                    # Feedback AI usunięty - realistyczna rozmowa bez "ściąg"
                
                elif role == "evaluation":
                    # Feedback od AI - również usunięty (był duplikat)
                    pass
        
        # === INPUT GRACZA ===
        st.markdown("---")
        st.markdown("### ✍️ Twoja odpowiedź")
        
        # Wskazówki kontekstowe
        if current_turn == 1:
            st.info(f"💡 **Wskazówka**: {npc_config.get('name', 'Rozmówca')} ma swoją perspektywę i cele. Spróbuj zrozumieć sytuację z jego punktu widzenia.")
        
        # === SPEECH-TO-TEXT INTERFACE (jak w "Feedback dla nowego pracownika") ===
        st.markdown("**🎤 Nagraj** (wielokrotnie, jeśli chcesz) **lub ✍️ pisz bezpośrednio w polu poniżej:**")
        
        # Klucze dla transkrypcji i wersjonowania
        transcription_key = f"ai_conv_transcription_{contract_id}"
        transcription_version_key = f"ai_conv_transcription_version_{contract_id}"
        last_audio_hash_key = f"ai_conv_last_audio_hash_{contract_id}"
        
        # Render ID - zapobiega duplikatom gdy kontrakt jest w dashboardzie i zakładce jednocześnie
        render_id_key = f"ai_conv_render_id_{contract_id}_{contract_index}"
        if render_id_key not in st.session_state:
            import random
            st.session_state[render_id_key] = random.randint(100000, 999999)
        render_id = st.session_state[render_id_key]
        
        # Inicjalizacja (setdefault nie powoduje re-render jeśli klucz już istnieje!)
        st.session_state.setdefault(transcription_key, "")
        st.session_state.setdefault(transcription_version_key, 0)
        st.session_state.setdefault(last_audio_hash_key, None)
        
        audio_data = st.audio_input(
            "🎤 Nagrywanie...",
            key=f"audio_input_ai_conv_{contract_id}_{contract_index}_{render_id}"
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
                                
                                api_key = st.secrets["API_KEYS"]["gemini"]
                                genai.configure(api_key=api_key)
                                
                                model = genai.GenerativeModel("models/gemini-2.5-flash")
                                prompt = f"""Dodaj interpunkcję (kropki, przecinki, pytajniki, wykrzykniki) do poniższego tekstu.
Nie zmieniaj słów, tylko dodaj znaki interpunkcyjne. Zachowaj strukturę i podział na zdania.
Zwróć tylko poprawiony tekst, bez dodatkowych komentarzy.

Tekst do poprawy:
{transcription}"""
                                response = model.generate_content(prompt)
                                transcription_with_punctuation = response.text.strip()
                                
                                # Komunikat usunięty - ciche działanie
                                transcription = transcription_with_punctuation
                                
                            except Exception as gemini_error:
                                # Błąd Gemini - cicho kontynuuj z surową transkrypcją
                                pass
                            
                            # DOPISZ do istniejącego tekstu (z session_state)
                            # Pobierz aktualną wartość z transcription_key (tam zapisujemy wartości)
                            existing_text = st.session_state.get(transcription_key, "")
                            
                            if existing_text.strip():
                                # Jeśli jest już jakiś tekst, dodaj nową linię i dopisz
                                st.session_state[transcription_key] = existing_text.rstrip() + "\n\n" + transcription
                            else:
                                # Jeśli to pierwsze nagranie, po prostu zapisz
                                st.session_state[transcription_key] = transcription
                            
                            # Inkrementuj wersję - to wymusi re-render text_area z nową wartością!
                            st.session_state[transcription_version_key] += 1
                            
                            # Komunikat usunięty - ciche działanie
                            
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
        
        # Dynamiczny klucz który zmienia się po transkrypcji (wymusza re-render)
        #WAŻNE: Dodaj render_id aby zapobiec duplikatom między dashboardem a zakładką
        text_area_key = f"ai_conv_input_{contract_id}_{current_turn}_{render_id}_v{st.session_state[transcription_version_key]}"
        current_text = st.session_state.get(transcription_key, "")
        
        # Callback - synchronizuj wartość text_area z transcription_key
        def sync_conv_textarea_to_state():
            if text_area_key in st.session_state:
                st.session_state[transcription_key] = st.session_state[text_area_key]
        
        # Oblicz dynamiczną wysokość na podstawie liczby linii
        num_lines = current_text.count('\n') + 1
        # Minimalna wysokość: 120px, każda linia dodatkowa to ~25px
        dynamic_height = max(120, min(400, 120 + (num_lines - 3) * 25))
        
        # Text area dla odpowiedzi
        player_message = st.text_area(
            "📝 Możesz edytować transkrypcję lub pisać bezpośrednio:",
            value=current_text,
            height=dynamic_height,
            key=text_area_key,
            placeholder=f"Wpisz swoją odpowiedź do {npc_config.get('name', 'rozmówcy')}... lub użyj mikrofonu powyżej",
            on_change=sync_conv_textarea_to_state
        )
        
        # Synchronizacja już jest w callback on_change, nie trzeba tu duplikować
        
        # Przyciski
        col_send, col_end = st.columns([3, 1])
        
        with col_send:
            if st.button("📤 Wyślij wiadomość", 
                        type="primary", 
                        use_container_width=True,
                        disabled=not player_message.strip(),
                        key=f"send_msg_{contract_id}_{current_turn}_{render_id}"):
                if player_message.strip():
                    with st.spinner("🤖 AI analizuje Twoją odpowiedź i generuje reakcję..."):
                        # Get Gemini API key
                        api_key = st.secrets.get("API_KEYS", {}).get("gemini", "")
                        if not api_key:
                            st.error("❌ Brak klucza API Gemini. Skonfiguruj secrets.")
                        else:
                            try:
                                # Process message through AI engine (per user!)
                                evaluation, npc_reaction = process_player_message(
                                    contract_id, 
                                    player_message, 
                                    api_key,
                                    username
                                )
                                
                                # Wyczyść pole tekstowe po wysłaniu (NOWY klucz!)
                                st.session_state[transcription_key] = ""
                                st.session_state[transcription_version_key] += 1  # Wymusza re-render
                                
                                # Success - rerun to show new messages
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Błąd podczas przetwarzania: {str(e)}")
        
        with col_end:
            if st.button("🏁 Zakończ", 
                        use_container_width=True,
                        key=f"end_conv_{contract_id}_{current_turn}_{render_id}"):
                # Zakończ i od razu przenieś do completed (jak "Zakończ kontrakt")
                from utils.ai_conversation_engine import calculate_final_conversation_score
                
                # Znajdź kontrakt
                contract_found = next((c for c in bg_data["contracts"]["active"] if c["id"] == contract_id), None)
                if not contract_found:
                    st.error("Kontrakt nie znaleziony w aktywnych")
                else:
                    try:
                        # Pobierz wynik z engine (per user!)
                        result = calculate_final_conversation_score(contract_id, username)
                        stars = result.get("stars", 1)
                        total_points = result.get("total_points", 0)
                        metrics = result.get("metrics", {})
                        
                        # Buduj feedback jak w kontraktach standard (z 👍/⚠️)
                        conv_key = f"ai_conv_{username}_{contract_id}"
                        conv_state = st.session_state.get(conv_key, {})
                        messages = conv_state.get("messages", [])
                        
                        # Zbierz wszystkie pozytywne aspekty i sugestie z całej rozmowy
                        all_positive = []
                        all_improvements = []
                        for msg in messages:
                            if msg.get("role") == "player":
                                evaluation = msg.get("evaluation", {})
                                all_positive.extend(evaluation.get("positive_aspects", []))
                                all_improvements.extend(evaluation.get("improvement_suggestions", []))
                        
                        # Sformatuj feedback jak w business_game_evaluation.py (z perspektywy NPC)
                        npc_name = contract_found.get("npc_name", "Klient")
                        feedback_summary = f"**{npc_name}:** Dziękuję za poświęcony czas na rozmowę."
                        
                        if all_positive:
                            feedback_summary += "\n\n**👍 Co mi się podobało:**\n"
                            feedback_summary += "\n".join([f"• {s}" for s in all_positive[:5]])  # Top 5
                        
                        if all_improvements:
                            feedback_summary += "\n\n**⚠️ Co mogłoby być lepsze:**\n"
                            feedback_summary += "\n".join([f"• {i}" for i in all_improvements[:5]])  # Top 5
                        
                        # Oblicz nagrodę
                        reward_base = contract_found.get("nagroda_base", 500)
                        reward_5star = contract_found.get("nagroda_5star", reward_base * 2)
                        reward = int(reward_base + ((stars - 1) / 4.0) * (reward_5star - reward_base))
                        
                        # KRYTYCZNE: Dodaj do SALDA FIRMY (bg_data["money"]), NIE do DegenCoins!
                        bg_data["money"] = bg_data.get("money", 0) + reward
                        bg_data["firm"]["reputation"] += contract_found.get("reputacja", 20) * stars / 3
                        bg_data["stats"]["total_revenue"] += reward
                        
                        # Przenieś do completed
                        completed_contract = contract_found.copy()
                        completed_contract["completed_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        completed_contract["rating"] = stars  # Używamy "rating" jak inne kontrakty
                        completed_contract["stars"] = stars  # Dla kompatybilności
                        completed_contract["points"] = total_points
                        completed_contract["reward"] = reward
                        completed_contract["metrics"] = metrics
                        completed_contract["feedback"] = feedback_summary
                        completed_contract["status"] = "completed"
                        
                        bg_data["contracts"]["completed"].append(completed_contract)
                        bg_data["contracts"]["active"] = [c for c in bg_data["contracts"]["active"] if c["id"] != contract_id]
                        
                        # Zaktualizuj statystyki
                        bg_data["stats"]["contracts_completed"] = bg_data["stats"].get("contracts_completed", 0) + 1
                        rating_key = f"contracts_{stars}star"
                        bg_data["stats"][rating_key] = bg_data["stats"].get(rating_key, 0) + 1
                        
                        # Dodaj transakcję
                        if "history" not in bg_data:
                            bg_data["history"] = {"transactions": [], "level_ups": []}
                        if "transactions" not in bg_data["history"]:
                            bg_data["history"]["transactions"] = []
                        
                        bg_data["history"]["transactions"].append({
                            "type": "contract_reward",
                            "amount": reward,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "description": f"Conversation: {contract_found['tytul']} ({stars}⭐)"
                        })
                        
                        # Zapisz dane
                        save_game_data(user_data, bg_data, industry_id)
                        save_user_data(username, user_data)
                        
                        # Wyczyść stan konwersacji
                        conv_key = f"ai_conv_{username}_{contract_id}"
                        if conv_key in st.session_state:
                            del st.session_state[conv_key]
                        
                        st.success(f"✅ Zakończono! 💰 +{reward:,} PLN | ⭐ {stars}/5")
                        time.sleep(1)
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Błąd przy zakończeniu kontraktu: {e}")
def render_speed_challenge_contract(contract, username, user_data, bg_data, industry_id="consulting", contract_index=0):
    """Renderuje Speed Challenge Contract - kontrakt z limitem czasu"""
    from utils.speed_challenge_engine import (
        initialize_speed_challenge,
        get_challenge_state,
        start_challenge,
        get_remaining_time,
        render_timer,
        complete_speed_challenge,
        reset_challenge
    )
    
    contract_id = contract["id"]
    challenge_config = contract.get("challenge_config", {})
    time_limit = contract.get("time_limit_seconds", 60)
    speed_bonus_multiplier = contract.get("speed_bonus_multiplier", 1.5)
    pressure_level = contract.get("pressure_level", "medium")
    
    # Inicjalizacja
    initialize_speed_challenge(contract_id, challenge_config, time_limit)
    state = get_challenge_state(contract_id)
    
    is_completed = state.get("completed", False)
    
    # === NAGŁÓWEK KONTRAKTU ===
    pressure_colors = {
        "low": ("#10b981", "#d1fae5"),
        "medium": ("#f59e0b", "#fef3c7"),
        "high": ("#ef4444", "#fee2e2")
    }
    pressure_color, pressure_bg = pressure_colors.get(pressure_level, pressure_colors["medium"])
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, {pressure_color} 0%, {pressure_color}dd 100%); 
                color: white; padding: 24px; border-radius: 16px; margin-bottom: 24px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
        <div style='display: flex; align-items: center; justify-content: space-between;'>
            <div>
                <h2 style='margin: 0 0 8px 0; font-size: 24px;'>⚡ {contract['tytul']}</h2>
                <p style='margin: 0; opacity: 0.95; font-size: 14px;'>{contract['opis']}</p>
            </div>
            <div style='background: rgba(255,255,255,0.2); padding: 12px 20px; border-radius: 8px;'>
                <div style='font-size: 32px; font-weight: bold; margin: 0;'>{time_limit}s</div>
                <div style='font-size: 12px; opacity: 0.9; margin-top: 4px;'>LIMIT CZASU</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if is_completed:
        # === WIDOK ZAKOŃCZENIA ===
        evaluation = state.get("evaluation_result", {})
        
        stars = evaluation.get("stars", 3)
        points = evaluation.get("points", 0)
        base_points = evaluation.get("base_points", 0)
        speed_bonus = evaluation.get("speed_bonus_applied", 0)
        time_taken = evaluation.get("time_taken", 0)
        on_time = evaluation.get("on_time", True)
        
        # Pokaż wyniki
        st.success("🎉 **Challenge zakończony!**" if on_time else "⏰ **Challenge zakończony (po czasie)**")
        
        st.markdown("---")
        
        # Metryki
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("### ⭐")
            st.markdown(f"**Ocena:** {stars}/5")
        
        with col2:
            st.markdown("### 🎯")
            if speed_bonus > 0:
                st.markdown(f"**Punkty:** ~~{base_points}~~ **{points}**")
                st.caption(f"💨 Speed bonus: +{int(speed_bonus * 100)}%")
            else:
                st.markdown(f"**Punkty:** {points}")
        
        with col3:
            st.markdown("### ⏱️")
            time_color = "green" if on_time else "red"
            st.markdown(f"**Czas:** :{time_color}[{time_taken:.1f}s]")
            st.caption(f"Limit: {time_limit}s")
        
        with col4:
            result_emoji = "🏆" if stars >= 4 and on_time else ("🤝" if on_time else "⏰")
            st.markdown(f"### {result_emoji}")
            st.markdown(f"**{'SUCCESS' if stars >= 4 and on_time else ('OK' if on_time else 'TIMEOUT')}**")
        
        st.markdown("---")
        
        # Feedback
        feedback_text = evaluation.get("feedback", "Brak szczegółowego feedbacku")
        st.markdown(f"""
        <div style='background: {pressure_bg}; border-left: 4px solid {pressure_color}; 
                    padding: 16px; border-radius: 8px; margin: 16px 0;'>
            <h4 style='margin: 0 0 8px 0; color: #1f2937;'>💭 Feedback</h4>
            <p style='margin: 0; color: #4b5563;'>{feedback_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Strengths & Improvements
        col_str, col_imp = st.columns(2)
        
        with col_str:
            st.markdown("#### ✅ Mocne strony")
            strengths = evaluation.get("strengths", [])
            if strengths:
                for strength in strengths:
                    st.markdown(f"- {strength}")
            else:
                st.caption("Brak szczegółów")
        
        with col_imp:
            st.markdown("#### 🎯 Do poprawy")
            improvements = evaluation.get("improvements", [])
            if improvements:
                for improvement in improvements:
                    st.markdown(f"- {improvement}")
            else:
                st.caption("Świetna robota!")
        
        st.markdown("---")
        
        # Twoja odpowiedź
        with st.expander("📝 Twoja odpowiedź", expanded=False):
            st.markdown(state.get("player_response", ""))
        
        # Kontekst problemu
        with st.expander("📋 Problem do rozwiązania"):
            st.markdown(challenge_config.get("problem", "Brak opisu"))
        
        st.markdown("---")
        
        # Przyciski akcji
        col_close, col_retry = st.columns(2)
        
        with col_close:
            if st.button("✅ Zamknij i kompletuj", use_container_width=True, type="primary"):
                # Zapisz wyniki do kontraktu
                final_reward = 0  # Initialize
                
                # Aktualizuj kontrakt
                for i, c in enumerate(bg_data["contracts"]["active"]):
                    if c["id"] == contract_id:
                        bg_data["contracts"]["active"][i].update({
                            "status": "completed",
                            "rating": stars,
                            "completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "speed_challenge_results": {
                                "time_taken": time_taken,
                                "time_limit": time_limit,
                                "on_time": on_time,
                                "speed_bonus": speed_bonus,
                                "pressure_level": pressure_level
                            }
                        })
                        
                        # Przenieś do completed
                        completed_contract = bg_data["contracts"]["active"].pop(i)
                        bg_data["contracts"]["completed"].append(completed_contract)
                        
                        # Dodaj nagrody
                        reward_multiplier = {1: 0.5, 2: 0.7, 3: 1.0, 4: 1.3, 5: 1.6}.get(stars, 1.0)
                        base_reward = contract.get("nagroda_base", 500)
                        final_reward = int(base_reward * reward_multiplier * (1 + speed_bonus * 0.3))
                        
                        # KRYTYCZNE: Dodaj do SALDA FIRMY (bg_data["money"]), NIE do DegenCoins!
                        bg_data["money"] = bg_data.get("money", 0) + final_reward
                        bg_data["stats"]["total_revenue"] += final_reward
                        bg_data["firm"]["reputation"] += contract.get("reputacja", 20) * stars / 3
                        
                        # Dodaj transakcję
                        if "history" not in bg_data:
                            bg_data["history"] = {"transactions": [], "level_ups": []}
                        if "transactions" not in bg_data["history"]:
                            bg_data["history"]["transactions"] = []
                        
                        bg_data["history"]["transactions"].append({
                            "type": "contract_reward",
                            "amount": final_reward,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "description": f"Speed Challenge: {contract['tytul']} ({stars}⭐)"
                        })
                        
                        break
                
                # Zapisz i resetuj
                save_game_data(user_data, bg_data, industry_id)
                save_user_data(username, user_data)
                reset_challenge(contract_id)
                st.success(f"💰 Otrzymujesz {final_reward:,} PLN!")
                st.rerun()
        
        with col_retry:
            if st.button("🔄 Spróbuj ponownie", use_container_width=True):
                reset_challenge(contract_id)
                st.rerun()
    
    else:
        # === WIDOK GRY ===
        
        # Kontekst challenge
        client_name = challenge_config.get("client_name", "Klient")
        client_role = challenge_config.get("client_role", "")
        urgency_reason = challenge_config.get("urgency_reason", "Pilna sprawa!")
        
        st.markdown(f"""
        <div style='background: #f8fafc; padding: 16px; border-radius: 12px; margin-bottom: 20px;
                    border: 2px solid {pressure_color};'>
            <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 12px;'>
                <div style='background: {pressure_color}; color: white; 
                            padding: 8px 16px; border-radius: 20px; font-weight: bold;'>
                    {client_name}
                </div>
                <div style='color: #64748b; font-size: 14px;'>{client_role}</div>
            </div>
            <div style='background: {pressure_bg}; padding: 12px; border-radius: 8px;
                        border-left: 4px solid {pressure_color};'>
                <div style='font-weight: bold; color: {pressure_color}; margin-bottom: 8px;'>
                    ⚡ {urgency_reason}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Problem do rozwiązania
        problem = challenge_config.get("problem", "Brak opisu problemu")
        
        # Konwertuj Markdown na HTML
        import re
        problem_html = problem.replace(chr(10), '<br>')
        problem_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', problem_html)  # **bold**
        problem_html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', problem_html)  # *italic*
        
        st.markdown(f"""
        <div style='background: white; padding: 20px; border-radius: 12px; 
                    border: 1px solid #e5e7eb; margin-bottom: 24px;
                    line-height: 1.6; color: #1f2937;'>
            {problem_html}
        </div>
        """, unsafe_allow_html=True)
        
        
        # Start button lub timer
        if not state.get("started", False):
            st.markdown("---")
            st.markdown(f"""
            <div style='background: {pressure_bg}; padding: 20px; border-radius: 12px; text-align: center;'>
                <h3 style='color: {pressure_color}; margin: 0 0 12px 0;'>⏱️ Gotowy na challenge?</h3>
                <p style='margin: 0; color: #64748b;'>
                    Masz **{time_limit} sekund** na odpowiedź.<br>
                    Im szybciej odpowiesz, tym większy bonus! 💨
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("")
            
            if st.button("🚀 START TIMER", use_container_width=True, type="primary"):
                start_challenge(contract_id)
                st.rerun()
        
        else:
            # Timer aktywny - JavaScript countdown (bez reruns!)
            remaining = get_remaining_time(contract_id)
            time_out = remaining <= 0
            
            # JavaScript timer
            timer_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                    }}
                    @keyframes pulse {{
                        0%, 100% {{ transform: scale(1); }}
                        50% {{ transform: scale(1.05); }}
                    }}
                </style>
            </head>
            <body>
                <div id="timer-container"></div>
                <script>
                (function() {{
                    const container = document.getElementById('timer-container');
                    let secondsLeft = {max(0, int(remaining))};
                    const totalSeconds = {time_limit};
                    
                    function updateTimer() {{
                        const minutes = Math.floor(secondsLeft / 60);
                        const seconds = secondsLeft % 60;
                        const percentage = (secondsLeft / totalSeconds) * 100;
                        
                        let color, bgColor;
                        if (percentage > 50) {{
                            color = '#4ade80';
                            bgColor = '#f0fdf4';
                        }} else if (percentage > 25) {{
                            color = '#fbbf24';
                            bgColor = '#fffbeb';
                        }} else {{
                            color = '#f87171';
                            bgColor = '#fef2f2';
                        }}
                        
                        if (secondsLeft <= 0) {{
                            container.innerHTML = '<div style="background: #fee; border: 2px solid #f00; padding: 16px; border-radius: 8px; text-align: center; animation: pulse 1s infinite;"><h2 style="color: #c00; margin: 0; font-size: 32px;">⏰ CZAS MINĄŁ!</h2><p style="margin: 8px 0 0 0; color: #666;">Zbyt późno na odpowiedź...</p></div>';
                        }} else {{
                            const minutesStr = String(minutes).padStart(2, '0');
                            const secondsStr = String(seconds).padStart(2, '0');
                            
                            container.innerHTML = '<div style="background: ' + bgColor + '; border: 2px solid ' + color + '; padding: 16px; border-radius: 8px; text-align: center;"><h2 style="color: ' + color + '; margin: 0; font-size: 48px; font-family: monospace; font-weight: bold;">' + minutesStr + ':' + secondsStr + '</h2><p style="margin: 8px 0 0 0; color: #666; font-size: 14px;">Pozostały czas</p></div>';
                            
                            secondsLeft--;
                            setTimeout(updateTimer, 1000);
                        }}
                    }}
                    
                    updateTimer();
                }})();
                </script>
            </body>
            </html>
            """
            
            st.components.v1.html(timer_html, height=120)
            
            st.markdown("---")
            
            # Pole odpowiedzi
            st.markdown("### ✍️ Twoja odpowiedź")
            
            response = st.text_area(
                "Wpisz swoją poradę dla klienta:",
                height=200,
                placeholder="Bądź konkretny, zwięzły i actionable...",
                key=f"speed_response_{contract_id}_{contract_index}",
                disabled=time_out
            )
            
            st.markdown("")
            
            # Przyciski
            col_submit, col_cancel = st.columns([3, 1])
            
            with col_submit:
                submit_disabled = not response.strip() or time_out
                if st.button(
                    "📤 Wyślij odpowiedź" if not time_out else "⏰ Czas minął",
                    use_container_width=True,
                    type="primary",
                    disabled=submit_disabled
                ):
                    # Oceń odpowiedź
                    with st.spinner("🤖 AI ocenia twoją odpowiedź..."):
                        evaluation = complete_speed_challenge(
                            contract_id,
                            response,
                            challenge_config
                        )
                    
                    st.rerun()
            
            with col_cancel:
                if st.button("❌ Anuluj", use_container_width=True):
                    reset_challenge(contract_id)
                    st.rerun()


def render_contract_card(contract, username, user_data, bg_data, can_accept_new, industry_id="consulting"):
    """Renderuje profesjonalną kartę dostępnego kontraktu - taki sam layout jak aktywne"""
    
    # Sprawdź czy jest aktywny bonus next_contract
    from utils.business_game_events import get_active_effects
    active_effects = get_active_effects(bg_data)
    has_bonus = any(e.get("type") == "next_contract_bonus" for e in active_effects)
    bonus_multiplier = 1.0
    
    if has_bonus:
        bonus_effect = next((e for e in active_effects if e.get("type") == "next_contract_bonus"), None)
        if bonus_effect:
            bonus_multiplier = bonus_effect.get("multiplier", 1.0)
    
    with st.container():
        # Kolory i style - jednolite jak aktywne kontrakty
        if has_bonus:
            accent_color = "#fbbf24"
            glow = "0 0 24px rgba(251, 191, 36, 0.5)"
        else:
            accent_color = "#667eea"
            glow = "0 0 20px rgba(102, 126, 234, 0.3)"
        
        # Oblicz nagrody z bonusem
        reward_min = int(contract['nagroda_base'] * bonus_multiplier) if has_bonus else contract['nagroda_base']
        reward_max = int(contract['nagroda_5star'] * bonus_multiplier) if has_bonus else contract['nagroda_5star']
        
        # Difficulty
        difficulty_stars = "🔥" * contract['trudnosc']
        
        # Czas realizacji jako "deadline badge"
        deadline_days = contract['czas_realizacji_dni']
        deadline_bg = "linear-gradient(135deg, #10b981 0%, #059669 100%)"  # Zielony dla dostępnych
        
        # Alert bonusu (jeśli aktywny)
        bonus_alert_html = ""
        if has_bonus:
            bonus_percent = int((bonus_multiplier - 1) * 100)
            bonus_alert_html = f"""<div style="background: #fef3c7; border-left: 4px solid #fbbf24; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px; display: flex; align-items: center; gap: 12px;"><div style="font-size: 24px;">🌟</div><div style="font-size: 13px; color: #1e293b; line-height: 1.4;"><strong>BONUS AKTYWNY: +{bonus_percent}%!</strong><br>Zwiększona nagroda za ten kontrakt</div></div>"""
        
        # Karta kontraktu - IDENTYCZNY LAYOUT jak aktywne
        html_content = f"""<div style="background: white; border-radius: 20px; padding: 24px; margin: 16px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.1), {glow}; border-left: 6px solid {accent_color}; transition: all 0.3s ease;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
<div style="flex: 1;">
<div style="font-size: 32px; margin-bottom: 8px;">{contract['emoji']}</div>
<h3 style="margin: 0; color: #1e293b; font-size: 20px; font-weight: 700;">{contract['tytul']}</h3>
<p style="margin: 4px 0 0 0; color: #64748b; font-size: 14px;">Klient: <strong>{contract['klient']}</strong> • {contract['kategoria']}</p>
</div>
<div style="background: {deadline_bg}; color: white; padding: 12px 20px; border-radius: 12px; text-align: center; min-width: 120px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
<div style="font-size: 24px; font-weight: 700; margin-bottom: 4px;">{deadline_days}d</div>
<div style="font-size: 11px; opacity: 0.9; text-transform: uppercase; letter-spacing: 0.5px;">Czas realizacji</div>
</div>
</div>
<div style="background: #f8f9fa; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
<div style="color: #64748b; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; font-weight: 600;">📝 Opis sytuacji</div>
<div style="color: #334155; font-size: 14px; line-height: 1.6;">{contract['opis']}</div>
</div>
{bonus_alert_html}
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 16px; padding-top: 16px; border-top: 1px solid #e2e8f0;">
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Nagroda</div>
<div style="color: #f59e0b; font-size: 20px; font-weight: 700;">💰 {reward_min}-{reward_max}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Trudność</div>
<div style="font-size: 20px;">{difficulty_stars}</div>
</div>
<div style="text-align: center;">
<div style="color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Reputacja</div>
<div style="color: #8b5cf6; font-size: 20px; font-weight: 700;">⭐ +{contract['reputacja']}</div>
</div>
</div>
</div>"""
        
        st.markdown(html_content, unsafe_allow_html=True)
        
        # Expander ze szczegółami zadania - kompaktowy layout z kartami
        with st.expander("👁️ Zobacz szczegóły zadania", expanded=False):
            # Zadanie w karcie (opcjonalne - dla standardowych kontraktów)
            if 'zadanie' in contract:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                            border-left: 4px solid #667eea; 
                            border-radius: 12px; 
                            padding: 16px 20px; 
                            margin-bottom: 16px;'>
                    <div style='color: #667eea; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 8px;'>
                        🎯 ZADANIE DO WYKONANIA
                    </div>
                    <div style='color: #334155; font-size: 14px; line-height: 1.6;'>
                        {contract['zadanie']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Wymagana wiedza w karcie (opcjonalne)
            if 'wymagana_wiedza' in contract and contract['wymagana_wiedza']:
                knowledge_items = "".join([f"<div style='padding: 6px 12px; background: white; border-radius: 6px; margin-bottom: 6px; color: #475569; font-size: 13px;'>✓ {req}</div>" for req in contract['wymagana_wiedza']])
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #10b98115 0%, #05966915 100%); 
                            border-left: 4px solid #10b981; 
                            border-radius: 12px; 
                            padding: 16px 20px; 
                            margin-bottom: 16px;'>
                    <div style='color: #10b981; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; margin-bottom: 12px;'>
                        📚 WYMAGANA WIEDZA
                    </div>
                    {knowledge_items}
                </div>
                """, unsafe_allow_html=True)
            
            # Dodatkowe info w kompaktowej formie
            st.markdown(f"""
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 12px;'>
                <div style='background: #f8fafc; border-radius: 8px; padding: 12px; text-align: center;'>
                    <div style='color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;'>Wymagany poziom</div>
                    <div style='color: #1e293b; font-size: 18px; font-weight: 700;'>🏆 {contract['wymagany_poziom']}</div>
                </div>
                <div style='background: #f8fafc; border-radius: 8px; padding: 12px; text-align: center;'>
                    <div style='color: #94a3b8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;'>Kategoria</div>
                    <div style='color: #1e293b; font-size: 18px; font-weight: 700;'>📂 {contract['kategoria']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Przycisk przyjęcia - szerszy dla lepszej czytelności na laptopach
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col2:
            # Sprawdź możliwość przyjęcia
            if not can_accept_new:
                st.button("❌ Brak miejsca", key=f"no_space_{contract['id']}", disabled=True, use_container_width=True)
            else:
                if st.button("✅ Przyjmij kontrakt", key=f"accept_{contract['id']}", type="primary", use_container_width=True):
                    updated_bg, success, message, _ = accept_contract(bg_data, contract['id'], user_data)
                    
                    if success:
                        from data.users_new import save_single_user
                        user_data = save_game_data(user_data, updated_bg, industry_id)
                        save_single_user(username, user_data)
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

# =============================================================================
# TAB 3: PRACOWNICY
# =============================================================================

# =============================================================================
# TAB 3A: BIURO
# =============================================================================

def show_office_tab(username, user_data, industry_id="consulting"):
    """Zakładka Biuro - zarządzanie przestrzenią"""
    from datetime import datetime
    
    bg_data = get_game_data(user_data, industry_id)
    
    # Inicjalizacja biura jeśli nie istnieje (dla starych zapisów)
    if "office" not in bg_data:
        bg_data["office"] = {
            "type": "home_office",
            "upgraded_at": None
        }
        save_game_data(user_data, bg_data, industry_id)
        save_user_data(username, user_data)
    
    st.subheader("🏢 Twoje Biuro")
    
    office_type = bg_data["office"]["type"]
    office_info = OFFICE_TYPES[office_type]
    
    # Kompaktowa karta informacyjna o biurze
    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); 
                    padding: 20px; border-radius: 12px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 48px;">{office_info['ikona']}</div>
                <div style="flex: 1;">
                    <h3 style="margin: 0; color: #1a1a1a;">{office_info['nazwa']}</h3>
                    <p style="margin: 5px 0; color: #2a2a2a; font-size: 14px;">{office_info['opis']}</p>
                    <div style="display: flex; gap: 20px; margin-top: 10px; font-size: 13px; color: #333;">
                        <span>👥 Max: {office_info['max_pracownikow']} pracowników</span>
                        <span>💰 Koszt: {office_info['koszt_dzienny']} zł/dzień</span>
                        <span>⭐ Reputacja: +{office_info['bonus_reputacji']}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Przycisk ulepszenia (jeśli dostępny)
    current_index = OFFICE_UPGRADE_PATH.index(office_type)
    if current_index < len(OFFICE_UPGRADE_PATH) - 1:
        next_office_type = OFFICE_UPGRADE_PATH[current_index + 1]
        next_office = OFFICE_TYPES[next_office_type]
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.write(f"💡 **Dostępne ulepszenie:** {next_office['ikona']} {next_office['nazwa']}")
        with col2:
            st.write(f"💰 Koszt: **{next_office['koszt_ulepszenia']} PLN**")
        with col3:
            # Pobierz saldo firmy (nie osobiste DegenCoins!)
            current_money = bg_data.get('money', 0)
            
            if current_money >= next_office['koszt_ulepszenia']:
                if st.button("⬆️ Ulepsz biuro", type="primary", use_container_width=True):
                    # Ulepsz biuro - płacimy Z FIRMY!
                    bg_data["money"] = current_money - next_office['koszt_ulepszenia']
                    bg_data["office"]["type"] = next_office_type
                    bg_data["office"]["upgraded_at"] = datetime.now().isoformat()
                    bg_data["stats"]["total_costs"] += next_office['koszt_ulepszenia']
                    
                    # Dodaj transakcję
                    if "transactions" not in bg_data.get("history", {}):
                        if "history" not in bg_data:
                            bg_data["history"] = {}
                        bg_data["history"]["transactions"] = []
                    
                    bg_data["history"]["transactions"].append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "type": "office_upgrade",
                        "description": f"Ulepszenie biura: {next_office['nazwa']}",
                        "amount": -next_office['koszt_ulepszenia']
                    })
                    
                    save_game_data(user_data, bg_data, industry_id)
                    save_user_data(username, user_data)
                    st.success(f"🎉 Biuro ulepszone do: {next_office['nazwa']}!")
                    st.balloons()
                    st.rerun()
            else:
                st.button("⬆️ Ulepsz biuro", disabled=True, use_container_width=True)
                st.caption(f"Potrzebujesz: {next_office['koszt_ulepszenia'] - current_money:.0f} PLN więcej")
    else:
        st.success("🌟 Posiadasz najlepsze możliwe biuro!")

# =============================================================================
# TAB 4A: USTAWIENIA FIRMY
# =============================================================================

def show_firm_settings_tab(username, user_data, industry_id="consulting"):
    """Ustawienia firmy - nazwa, logo, archiwum firm"""
    bg_data = get_game_data(user_data, industry_id)
    
    # Wszystkie ustawienia w jednym miejscu z tabami
    settings_tab1, settings_tab2, settings_tab3, settings_tab4, settings_tab5, settings_tab6 = st.tabs([
        "✏️ Nazwa i logo",
        "� Informacje",
        "🎨 Personalizacja",
        "💰 Cele finansowe",
        "🔔 Powiadomienia",
        "� Zarządzanie firmą"
    ])
    
    # TAB 1: Nazwa i logo
    with settings_tab1:
        col_name, col_logo = st.columns([1, 1])
        
        with col_name:
            st.markdown("### ✏️ Zmień nazwę firmy")
            new_name = st.text_input(
                "Nowa nazwa firmy", 
                value=bg_data["firm"]["name"], 
                key="settings_firm_name_input"
            )
            if st.button("💾 Zapisz nazwę", key="settings_save_firm_name", type="primary"):
                bg_data["firm"]["name"] = new_name
                save_game_data(user_data, bg_data, industry_id)
                save_user_data(username, user_data)
                st.success("✅ Nazwa firmy zaktualizowana!")
                st.rerun()
        
        with col_logo:
            st.markdown("### 🎨 Zmień logo firmy")
            
            # Kategorie logo
            categories = list(FIRM_LOGOS.keys())
            category_names = {
                "basic": "🏢 Budynki",
                "business": "💼 Biznes",
                "creative": "🎨 Kreatywne",
                "nature": "🌍 Natura",
                "tech": "💻 Technologia",
                "animals": "🦁 Zwierzęta"
            }
            
            selected_category = st.selectbox(
                "Kategoria:",
                categories,
                format_func=lambda x: category_names.get(x, x),
                key="settings_logo_category"
            )
            
            # Grid logo (mniejszy - 6 kolumn)
            available_logos = FIRM_LOGOS[selected_category]["free"]
            cols = st.columns(6)
            for idx, logo in enumerate(available_logos[:12]):  # Max 12 logo
                with cols[idx % 6]:
                    if st.button(
                        logo,
                        key=f"settings_logo_{selected_category}_{idx}",
                        help=f"Wybierz {logo}"
                    ):
                        bg_data["firm"]["logo"] = logo
                        save_game_data(user_data, bg_data, industry_id)
                        save_user_data(username, user_data)
                        st.success(f"✅ Logo: {logo}")
                        st.rerun()
        
        # Podgląd na całej szerokości
        st.markdown("---")
        st.markdown("### 👀 Podgląd")
        current_logo = bg_data["firm"].get("logo", "🏢")
        current_name = bg_data["firm"]["name"]
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; color: white;'>
            <div style='font-size: 72px; margin-bottom: 12px;'>{current_logo}</div>
            <h2 style='margin: 0; color: white;'>{current_name}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # TAB 2: Informacje o firmie
    with settings_tab2:
        st.markdown("### 📊 Informacje o firmie")
        
        # Pobierz dane
        founded_date = bg_data["firm"].get("founded", datetime.now().strftime("%Y-%m-%d"))
        founded_dt = datetime.strptime(founded_date, "%Y-%m-%d")
        days_active = (datetime.now() - founded_dt).days
        
        # Grid z informacjami
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 20px; border-radius: 12px; text-align: center; color: white;'>
                <div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>📅 Data założenia</div>
                <div style='font-size: 24px; font-weight: 700;'>{}</div>
            </div>
            """.format(founded_dt.strftime("%d.%m.%Y")), unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 12px; text-align: center; color: white;'>
                <div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>⏱️ Dni działalności</div>
                <div style='font-size: 24px; font-weight: 700;'>{days_active}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            level = bg_data["firm"].get("level", 1)
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 20px; border-radius: 12px; text-align: center; color: white;'>
                <div style='font-size: 14px; opacity: 0.9; margin-bottom: 8px;'>🏆 Poziom firmy</div>
                <div style='font-size: 24px; font-weight: 700;'>Level {level}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Slogan/Motto
        st.markdown("### 💬 Motto firmy")
        current_motto = bg_data["firm"].get("motto", "")
        new_motto = st.text_area(
            "Motto lub slogan Twojej firmy:",
            value=current_motto,
            max_chars=200,
            height=80,
            placeholder="Np. 'Jakość przede wszystkim' lub 'Innowacje dla ludzi'",
            key="firm_motto"
        )
        
        if new_motto != current_motto:
            if st.button("💾 Zapisz motto", type="primary", key="save_motto"):
                bg_data["firm"]["motto"] = new_motto
                save_game_data(user_data, bg_data, industry_id)
                save_user_data(username, user_data)
                st.success("✅ Motto zaktualizowane!")
                st.rerun()
        
        st.markdown("---")
        
        # Dodatkowe informacje
        st.markdown("### 📋 Szczegóły")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.info(f"""
            **🏢 Branża:** {industry_id.capitalize()}  
            **📊 Scenariusz:** {bg_data.get('scenario_id', 'N/A')}  
            **⭐ Reputacja:** {bg_data['firm'].get('reputation', 0)}  
            """)
        
        with info_col2:
            total_employees = len(bg_data.get("employees", []))
            total_completed = len(bg_data.get("contracts", {}).get("completed", []))
            total_revenue = bg_data.get("stats", {}).get("total_revenue", 0)
            
            st.success(f"""
            **👥 Pracownicy:** {total_employees}  
            **✅ Ukończone kontrakty:** {total_completed}  
            **💰 Łączny przychód:** {total_revenue:,} PLN  
            """)
    
    # TAB 3: Personalizacja
    with settings_tab3:
        st.markdown("### 🎨 Schemat kolorów firmy")
        st.info("💡 Wybierz schemat kolorów, który będzie reprezentował Twoją firmę w interfejsie")
        
        # Dostępne schematy kolorów
        color_schemes = {
            "purple": {"name": "🟣 Fioletowy (Classic)", "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "primary": "#667eea"},
            "blue": {"name": "🔵 Niebieski (Professional)", "gradient": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", "primary": "#3b82f6"},
            "green": {"name": "🟢 Zielony (Growth)", "gradient": "linear-gradient(135deg, #10b981 0%, #059669 100%)", "primary": "#10b981"},
            "orange": {"name": "🟠 Pomarańczowy (Energy)", "gradient": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)", "primary": "#f59e0b"},
            "red": {"name": "🔴 Czerwony (Bold)", "gradient": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)", "primary": "#ef4444"},
            "pink": {"name": "🌸 Różowy (Creative)", "gradient": "linear-gradient(135deg, #ec4899 0%, #db2777 100%)", "primary": "#ec4899"},
            "teal": {"name": "💎 Turkusowy (Innovation)", "gradient": "linear-gradient(135deg, #14b8a6 0%, #0d9488 100%)", "primary": "#14b8a6"},
            "indigo": {"name": "💜 Indygo (Premium)", "gradient": "linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)", "primary": "#6366f1"}
        }
        
        # Obecny schemat
        current_scheme = bg_data["firm"].get("color_scheme", "purple")
        
        # Grid z podglądem schematów
        cols = st.columns(4)
        for idx, (scheme_id, scheme_data) in enumerate(color_schemes.items()):
            with cols[idx % 4]:
                is_current = scheme_id == current_scheme
                border = "4px solid #10b981" if is_current else "2px solid #e5e7eb"
                
                st.markdown(f"""
                <div style='border: {border}; border-radius: 12px; padding: 12px; margin-bottom: 12px; background: white;'>
                    <div style='background: {scheme_data["gradient"]}; height: 80px; border-radius: 8px; margin-bottom: 8px;'></div>
                    <div style='font-size: 12px; text-align: center; color: #64748b;'>{scheme_data["name"]}</div>
                    {"<div style='text-align: center; color: #10b981; font-size: 11px; margin-top: 4px;'>✓ Aktywny</div>" if is_current else ""}
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Wybierz", key=f"color_{scheme_id}", disabled=is_current, use_container_width=True):
                    bg_data["firm"]["color_scheme"] = scheme_id
                    save_game_data(user_data, bg_data, industry_id)
                    save_user_data(username, user_data)
                    st.success(f"✅ Zmieniono na {scheme_data['name']}")
                    st.rerun()
        
        st.markdown("---")
        
        # Podgląd wizytówki w rankingach
        st.markdown("### 👀 Podgląd wizytówki")
        current_logo = bg_data["firm"].get("logo", "🏢")
        current_name = bg_data["firm"]["name"]
        current_gradient = color_schemes[current_scheme]["gradient"]
        
        st.markdown(f"""
        <div style='background: {current_gradient}; padding: 24px; border-radius: 16px; color: white; margin: 16px 0;'>
            <div style='display: flex; align-items: center; gap: 20px;'>
                <div style='font-size: 64px;'>{current_logo}</div>
                <div style='flex: 1;'>
                    <h2 style='margin: 0; color: white; font-size: 28px;'>{current_name}</h2>
                    <div style='opacity: 0.9; margin-top: 8px;'>Level {bg_data["firm"].get("level", 1)} • {industry_id.capitalize()}</div>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 32px; font-weight: 700;'>#{1}</div>
                    <div style='opacity: 0.9; font-size: 14px;'>w rankingu</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # TAB 4: Cele finansowe
    with settings_tab4:
        st.markdown("### 💰 Zarządzanie celami finansowymi")
        
        # Inicjalizuj ustawienia finansowe jeśli nie istnieją
        if "financial_settings" not in bg_data:
            bg_data["financial_settings"] = {
                "savings_goal": 0,
                "low_balance_alert": -10000,
                "high_balance_alert": 50000,
                "auto_transfer_enabled": False,
                "auto_transfer_threshold": 30000,
                "auto_transfer_amount": 5000
            }
        
        fin_settings = bg_data["financial_settings"]
        current_balance = bg_data.get("money", 0)
        
        # Obecne saldo
        balance_color = "#10b981" if current_balance >= 0 else "#ef4444"
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 24px; border-radius: 16px; color: white; margin-bottom: 24px;'>
            <div style='font-size: 14px; opacity: 0.8; margin-bottom: 8px;'>💰 Obecne saldo firmy</div>
            <div style='font-size: 42px; font-weight: 700; color: {balance_color};'>{current_balance:,} PLN</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Cel oszczędnościowy
        st.markdown("### 🎯 Cel oszczędnościowy")
        st.caption("Ustaw minimalną kwotę, którą chcesz utrzymać jako bufor bezpieczeństwa")
        
        savings_goal = st.number_input(
            "Cel oszczędnościowy (PLN):",
            min_value=0,
            max_value=1000000,
            value=fin_settings.get("savings_goal", 0),
            step=5000,
            key="savings_goal_input"
        )
        
        if current_balance >= savings_goal and savings_goal > 0:
            st.success(f"✅ Cel osiągnięty! Masz {current_balance - savings_goal:,} PLN powyżej celu")
        elif savings_goal > 0:
            deficit = savings_goal - current_balance
            st.warning(f"⚠️ Brakuje {deficit:,} PLN do osiągnięcia celu")
        
        st.markdown("---")
        
        # Alerty salda
        st.markdown("### 🔔 Alerty salda")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⚠️ Alert niskiego salda")
            low_alert = st.number_input(
                "Powiadom gdy saldo spadnie poniżej:",
                min_value=-100000,
                max_value=0,
                value=fin_settings.get("low_balance_alert", -10000),
                step=1000,
                key="low_alert_input"
            )
            
            if current_balance < low_alert:
                st.error(f"🚨 ALERT! Saldo poniżej progu: {current_balance:,} PLN < {low_alert:,} PLN")
        
        with col2:
            st.markdown("#### 🎉 Alert wysokiego salda")
            high_alert = st.number_input(
                "Powiadom gdy saldo przekroczy:",
                min_value=0,
                max_value=1000000,
                value=fin_settings.get("high_balance_alert", 50000),
                step=5000,
                key="high_alert_input"
            )
            
            if current_balance > high_alert:
                st.success(f"🎉 Gratulacje! Saldo powyżej progu: {current_balance:,} PLN > {high_alert:,} PLN")
        
        st.markdown("---")
        
        # Auto-transfer do DegenCoins
        st.markdown("### 💎 Automatyczny transfer zysków")
        st.caption("Automatycznie przenoś nadwyżki do swojego portfela DegenCoins")
        
        auto_transfer = st.checkbox(
            "Włącz automatyczny transfer",
            value=fin_settings.get("auto_transfer_enabled", False),
            key="auto_transfer_enabled"
        )
        
        if auto_transfer:
            col1, col2 = st.columns(2)
            with col1:
                transfer_threshold = st.number_input(
                    "Transfer gdy saldo przekroczy:",
                    min_value=0,
                    max_value=1000000,
                    value=fin_settings.get("auto_transfer_threshold", 30000),
                    step=5000,
                    key="transfer_threshold"
                )
            with col2:
                transfer_amount = st.number_input(
                    "Kwota transferu:",
                    min_value=1000,
                    max_value=100000,
                    value=fin_settings.get("auto_transfer_amount", 5000),
                    step=1000,
                    key="transfer_amount"
                )
            
            st.info(f"💡 Gdy saldo firmy przekroczy {transfer_threshold:,} PLN, automatycznie przelej {transfer_amount:,} PLN do DegenCoins")
        
        # Zapisz ustawienia
        if st.button("💾 Zapisz ustawienia finansowe", type="primary", key="save_financial_settings"):
            bg_data["financial_settings"] = {
                "savings_goal": savings_goal,
                "low_balance_alert": low_alert,
                "high_balance_alert": high_alert,
                "auto_transfer_enabled": auto_transfer,
                "auto_transfer_threshold": transfer_threshold if auto_transfer else fin_settings.get("auto_transfer_threshold", 30000),
                "auto_transfer_amount": transfer_amount if auto_transfer else fin_settings.get("auto_transfer_amount", 5000)
            }
            save_game_data(user_data, bg_data, industry_id)
            save_user_data(username, user_data)
            st.success("✅ Ustawienia finansowe zapisane!")
            st.rerun()
    
    # TAB 5: Powiadomienia
    with settings_tab5:
        st.markdown("### 🔔 Centrum powiadomień")
        
        # Inicjalizuj ustawienia powiadomień
        if "notifications" not in bg_data:
            bg_data["notifications"] = {
                "deadline_alert_hours": 24,
                "deadline_alert_enabled": True,
                "new_contracts_alert": True,
                "balance_alerts_enabled": True,
                "events_alerts_enabled": True,
                "level_up_alerts": True,
                "employee_alerts": True
            }
        
        notif_settings = bg_data["notifications"]
        
        # Alerty deadline
        st.markdown("### ⏰ Alerty deadline kontraktów")
        deadline_enabled = st.checkbox(
            "Powiadamiaj o zbliżających się deadline'ach",
            value=notif_settings.get("deadline_alert_enabled", True),
            key="deadline_alert_enabled"
        )
        
        if deadline_enabled:
            deadline_hours = st.slider(
                "Powiadom X godzin przed deadline:",
                min_value=1,
                max_value=72,
                value=notif_settings.get("deadline_alert_hours", 24),
                step=1,
                key="deadline_hours"
            )
            st.caption(f"💡 Otrzymasz powiadomienie {deadline_hours}h przed upływem terminu każdego kontraktu")
        
        st.markdown("---")
        
        # Pozostałe powiadomienia
        st.markdown("### 📬 Inne powiadomienia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_contracts = st.checkbox(
                "📋 Nowe kontrakty w puli",
                value=notif_settings.get("new_contracts_alert", True),
                key="new_contracts_alert"
            )
            
            balance_alerts = st.checkbox(
                "💰 Alerty salda",
                value=notif_settings.get("balance_alerts_enabled", True),
                key="balance_alerts"
            )
            
            events_alerts = st.checkbox(
                "🎲 Wydarzenia losowe",
                value=notif_settings.get("events_alerts_enabled", True),
                key="events_alerts"
            )
        
        with col2:
            level_up = st.checkbox(
                "🏆 Awanse poziomów",
                value=notif_settings.get("level_up_alerts", True),
                key="level_up_alerts"
            )
            
            employee_alerts = st.checkbox(
                "👥 Zmiany w zespole",
                value=notif_settings.get("employee_alerts", True),
                key="employee_alerts"
            )
            
            reputation_alerts = st.checkbox(
                "⭐ Zmiany reputacji",
                value=notif_settings.get("reputation_alerts", True),
                key="reputation_alerts"
            )
        
        st.markdown("---")
        
        # Podsumowanie aktywnych alertów
        active_alerts = sum([
            deadline_enabled,
            new_contracts,
            balance_alerts,
            events_alerts,
            level_up,
            employee_alerts,
            reputation_alerts
        ])
        
        st.info(f"📊 Aktywnych alertów: **{active_alerts}**/7")
        
        # Zapisz ustawienia
        if st.button("💾 Zapisz ustawienia powiadomień", type="primary", key="save_notifications"):
            bg_data["notifications"] = {
                "deadline_alert_hours": deadline_hours if deadline_enabled else notif_settings.get("deadline_alert_hours", 24),
                "deadline_alert_enabled": deadline_enabled,
                "new_contracts_alert": new_contracts,
                "balance_alerts_enabled": balance_alerts,
                "events_alerts_enabled": events_alerts,
                "level_up_alerts": level_up,
                "employee_alerts": employee_alerts,
                "reputation_alerts": reputation_alerts
            }
            save_game_data(user_data, bg_data, industry_id)
            save_user_data(username, user_data)
            st.success("✅ Ustawienia powiadomień zapisane!")
            st.rerun()
    
    # TAB 6: Zarządzanie firmą
    with settings_tab6:
        # Sub-taby w zarządzaniu
        manage_tab1, manage_tab2 = st.tabs(["🆕 Nowa firma", "📦 Archiwum"])
        
        # Sub-tab: Nowa firma
        with manage_tab1:
            st.warning("⚠️ **Uwaga:** Te akcje mogą zmienić Twoją grę!")
            
            st.markdown("### 🆕 Rozpocznij nową firmę")
            st.info("""
            **Co się stanie:**
            - Obecna firma zostanie zarchiwizowana (dane nie zostaną utracone)
            - Stworzysz nową firmę od zera z nowym scenariuszem
            - Zachowasz swoje DegenCoins i doświadczenie
            - Będziesz mógł wrócić do poprzedniej firmy w zakładce "📦 Archiwum"
            """)
            
            if st.button("🚀 Rozpocznij nową firmę", type="primary", key="start_new_company"):
                # Zarchiwizuj obecną firmę
                if "archived_games" not in user_data:
                    user_data["archived_games"] = {}
                if industry_id not in user_data["archived_games"]:
                    user_data["archived_games"][industry_id] = []
                
                # Dodaj timestamp do archiwalnej gry
                archived_game = bg_data.copy()
                archived_game["archived_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                archived_game["firm"]["archived_name"] = f"{bg_data['firm']['name']} (zarchiwizowana {datetime.now().strftime('%d.%m.%Y')})"
                
                user_data["archived_games"][industry_id].append(archived_game)
                
                # Usuń obecną grę
                del user_data["business_games"][industry_id]
                
                # Zapisz zmiany
                save_user_data(username, user_data)
                
                # Resetuj session state
                st.session_state["selected_industry"] = industry_id
                
                st.success("✅ Firma zarchiwizowana! Przekierowuję do wyboru scenariusza...")
                time.sleep(1)
                st.rerun()
        
        # Sub-tab: Archiwum
        with manage_tab2:
            if "archived_games" in user_data and industry_id in user_data["archived_games"]:
                archived_count = len(user_data["archived_games"][industry_id])
                
                if archived_count > 0:
                    st.markdown(f"### 📦 Masz {archived_count} zarchiwizowanych firm")
                    st.info("💡 Możesz przywrócić dowolną firmę - obecna zostanie zarchiwizowana automatycznie")
                    
                    for idx, archived_game in enumerate(user_data["archived_games"][industry_id]):
                        firm_name = archived_game["firm"].get("archived_name", archived_game["firm"]["name"])
                        archived_at = archived_game.get("archived_at", "N/A")
                        level = archived_game["firm"].get("level", 1)
                        reputation = archived_game["firm"].get("reputation", 0)
                        logo = archived_game["firm"].get("logo", "🏢")
                        
                        # Karta firmy
                        with st.container():
                            col_logo, col_info, col_action = st.columns([1, 4, 2])
                            
                            with col_logo:
                                st.markdown(f"""
                                <div style='text-align: center; font-size: 48px; padding: 10px;'>
                                    {logo}
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col_info:
                                st.markdown(f"**{firm_name}**")
                                st.caption(f"📅 Zarchiwizowana: {archived_at}")
                                st.caption(f"🏢 Level {level} | ⭐ Reputacja {reputation}")
                            
                            with col_action:
                                if st.button("🔄 Przywróć", key=f"restore_game_{idx}", type="secondary"):
                                    # Zarchiwizuj obecną firmę jeśli istnieje
                                    if industry_id in user_data["business_games"]:
                                        current_game = user_data["business_games"][industry_id].copy()
                                        current_game["archived_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                        current_game["firm"]["archived_name"] = f"{current_game['firm']['name']} (zarchiwizowana {datetime.now().strftime('%d.%m.%Y')})"
                                        user_data["archived_games"][industry_id].append(current_game)
                                    
                                    # Przywróć wybraną firmę
                                    restored_game = archived_game.copy()
                                    # Usuń metadane archiwum
                                    if "archived_at" in restored_game:
                                        del restored_game["archived_at"]
                                    if "archived_name" in restored_game["firm"]:
                                        del restored_game["firm"]["archived_name"]
                                    
                                    user_data["business_games"][industry_id] = restored_game
                                    
                                    # Usuń z archiwum
                                    user_data["archived_games"][industry_id].pop(idx)
                                    
                                    # Zapisz
                                    save_user_data(username, user_data)
                                    
                                    st.success(f"✅ Przywrócono firmę: {firm_name}")
                                    time.sleep(1)
                                    st.rerun()
                            
                            st.markdown("---")
                else:
                    st.info("📭 Brak zarchiwizowanych firm. Rozpocznij nową firmę w zakładce '🆕 Nowa firma'")
            else:
                st.info("📭 Brak zarchiwizowanych firm. Rozpocznij nową firmę w zakładce '🆕 Nowa firma'")

# =============================================================================
# TAB 4B: ZARZĄDZANIE GRĄ
# =============================================================================

def show_game_management_tab(username, user_data, industry_id="consulting"):
    """Zarządzanie grą - zmiana branży, reset, zamknięcie firmy"""
    import time
    from data.scenarios import get_scenario
    
    bg_data = get_game_data(user_data, industry_id)
    
    st.subheader("⚙️ Zarządzanie Grą")
    
    # Sprawdź czy to tryb lifetime
    is_lifetime = bg_data.get("scenario_id") == "lifetime"
    
    if is_lifetime:
        st.markdown("### ♾️ Tryb Lifetime Challenge")
        st.info("💡 Grasz w trybie nieskończonym! Rywalizuj z innymi w rankingu i buduj swoją firmę bez ograniczeń.")
        st.markdown("---")
    
    # Będzie reszta zawartości z expandera...
    st.info("🚧 Funkcje zarządzania grą wkrótce dostępne tutaj.")

# =============================================================================
# TAB 3B: PRACOWNICY
# =============================================================================

def show_employees_tab(username, user_data, industry_id="consulting"):
    """Zakładka Biuro i Pracownicy"""
    bg_data = get_game_data(user_data, industry_id)
    
    # Inicjalizacja biura jeśli nie istnieje (dla starych zapisów)
    if "office" not in bg_data:
        bg_data["office"] = {
            "type": "home_office",
            "upgraded_at": None
        }
        save_game_data(user_data, bg_data, industry_id)
        save_user_data(username, user_data)
    
    # =============================================================================
    # SEKCJA PRACOWNIKÓW
    # =============================================================================
    
    st.subheader("👥 Zarządzanie Zespołem")
    
    # Pobierz informacje o biurze (potrzebne do limitu pracowników)
    office_type = bg_data["office"]["type"]
    office_info = OFFICE_TYPES[office_type]
    
    max_employees = office_info['max_pracownikow']
    current_count = len(bg_data["employees"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("👥 Zespół", f"{current_count}/{max_employees}")
    with col2:
        daily_cost = calculate_daily_costs(bg_data)
        st.metric("💸 Koszty dzienne (pracownicy)", f"{daily_cost:.0f} 💰")
    with col3:
        total_daily = daily_cost + office_info['koszt_dzienny']
        st.metric("� Łączne koszty dzienne", f"{total_daily:.0f} 💰")
    
    st.markdown("---")
    
    # SEKCJA 1: Obecnie zatrudnieni (2 kolumny)
    st.subheader("🏢 Obecnie zatrudnieni")
    
    if len(bg_data["employees"]) == 0:
        st.info("Nie masz jeszcze pracowników. Zatrudnij kogoś z sekcji poniżej!")
    else:
        # Wyświetl zatrudnionych w 2 kolumnach
        cols = st.columns(2)
        for idx, employee in enumerate(bg_data["employees"]):
            with cols[idx % 2]:
                render_employee_card(employee, username, user_data, bg_data, industry_id)
    
    st.markdown("---")
    
    # SEKCJA 2: Dostępni do zatrudnienia (2 kolumny)
    st.subheader("💼 Dostępni do zatrudnienia")
    
    if current_count >= max_employees:
        st.warning(f"⚠️ Osiągnięto limit pracowników: {max_employees}")
    
    # Wyświetl dostępnych w 2 kolumnach
    available_employees = [emp_type for emp_type in EMPLOYEE_TYPES.keys() 
                          if not any(e["type"] == emp_type for e in bg_data["employees"])]
    
    if available_employees:
        cols = st.columns(2)
        for idx, emp_type in enumerate(available_employees):
            with cols[idx % 2]:
                render_hire_card(emp_type, EMPLOYEE_TYPES[emp_type], username, user_data, bg_data, industry_id)
    else:
        st.success("✅ Wszystkie dostępne typy pracowników są już zatrudnione!")

def render_employee_card(employee, username, user_data, bg_data, industry_id="consulting"):
    """Renderuje kartę zatrudnionego pracownika - kompaktowa"""
    
    emp_data = EMPLOYEE_TYPES[employee["type"]]
    
    # Kompaktowa karta
    with st.container():
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 15px; border-radius: 10px; margin-bottom: 10px; color: white;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 18px; font-weight: bold;">{emp_data['ikona']} {emp_data['nazwa']}</div>
                    <div style="font-size: 12px; opacity: 0.9; margin-top: 4px;">{emp_data['bonus']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 14px; font-weight: bold;">{emp_data['koszt_dzienny']} 💰/dzień</div>
                    <div style="font-size: 11px; opacity: 0.8;">od {employee['hired_date']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Przycisk zwolnienia
        if st.button("🗑️ Zwolnij", key=f"fire_{employee['id']}", type="secondary", width="stretch"):
            updated_user_data, success, message = fire_employee(user_data, employee['id'], industry_id)
            if success:
                user_data.update(updated_user_data)
                save_user_data(username, user_data)
                st.success(message)
                st.rerun()
            else:
                st.error(message)

def render_hire_card(emp_type, emp_data, username, user_data, bg_data, industry_id="consulting"):
    """Renderuje kartę dostępnego pracownika - kompaktowa"""
    
    can_hire, reason = can_hire_employee(user_data, emp_type, industry_id)
    
    with st.container():
        # Kompaktowa karta z gradientem (szary)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e0e0e0 0%, #bdbdbd 100%); 
                    padding: 15px; border-radius: 10px; margin-bottom: 10px; color: #424242;">
            <div style="font-size: 18px; font-weight: bold; margin-bottom: 8px;">
                {emp_data['ikona']} {emp_data['nazwa']}
            </div>
            <div style="font-size: 12px; opacity: 0.8; margin-bottom: 8px;">
                {emp_data['bonus']}
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 13px;">
                <div>💰 Zatrudnienie: <strong>{emp_data['koszt_zatrudnienia']}</strong></div>
                <div>📅 Dzienny: <strong>{emp_data['koszt_dzienny']}</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Przycisk zatrudnienia
        if not can_hire:
            st.button("🔒 Niedostępny", key=f"hire_{emp_type}_locked", disabled=True, 
                     help=reason, width="stretch")
        else:
            if st.button("✅ Zatrudnij", key=f"hire_{emp_type}", type="primary", width="stretch"):
                updated_user_data, success, message = hire_employee(user_data, emp_type, industry_id)
                if success:
                    user_data.update(updated_user_data)
                    save_user_data(username, user_data)
                    st.success(message)
                    st.rerun()
                else:
                        st.error(message)
        
        st.markdown("---")

# =============================================================================
# TAB 4: RAPORTY FINANSOWE
# =============================================================================

def show_financial_reports_tab(username, user_data, industry_id="consulting"):
    """Zakładka Raporty Finansowe - zaawansowana analiza P&L i KPI"""
    bg_data = get_game_data(user_data, industry_id)
    
    st.subheader("📊 Raporty Finansowe")
    st.markdown("Zaawansowana analiza wyników finansowych Twojej firmy")
    
    # Wybór okresu analizy
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        period_type = st.selectbox(
            "Okres analizy:",
            ["Ostatni dzień", "Ostatnie 7 dni", "Ostatnie 14 dni", "Ostatnie 30 dni", "Ostatnie 90 dni", "Cały czas"],
            index=1,  # Domyślnie "Ostatnie 7 dni"
            key="financial_period"
        )

    
    with col2:
        comparison = st.checkbox("Porównaj z poprzednim okresem", value=True, key="financial_compare")
    
    with col3:
        if st.button("🔄 Odśwież", key="refresh_reports"):
            st.rerun()
    
    # Mapowanie okresu na dni
    period_days = {
        "Ostatni dzień": 1,
        "Ostatnie 7 dni": 7,
        "Ostatnie 14 dni": 14,
        "Ostatnie 30 dni": 30,
        "Ostatnie 90 dni": 90,
        "Cały czas": 9999
    }
    days = period_days[period_type]
    
    # Pobierz dane finansowe
    financial_data = calculate_financial_data(bg_data, days, comparison)
    
    st.markdown("---")
    
    # Sub-tabs w raportach
    report_tabs = st.tabs(["📈 KPI Dashboard", "📋 P&L Statement", "💰 Analiza Rentowności", "👥 ROI Pracowników", "📊 Analiza Kategorii"])
    
    with report_tabs[0]:
        show_kpi_dashboard(financial_data, bg_data)
    
    with report_tabs[1]:
        show_pl_statement(financial_data, period_type, comparison)
    
    with report_tabs[2]:
        show_profitability_analysis(financial_data, bg_data)
    
    with report_tabs[3]:
        show_employee_roi_analysis(financial_data, bg_data)
    
    with report_tabs[4]:
        show_category_analysis(financial_data, bg_data)


def calculate_financial_data(bg_data, days, include_comparison=False):
    """Oblicza wszystkie dane finansowe dla raportów"""
    from datetime import datetime, timedelta
    
    transactions = bg_data.get("history", {}).get("transactions", [])
    completed_contracts = bg_data.get("contracts", {}).get("completed", [])
    
    # Daty
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days) if days < 9999 else datetime(2000, 1, 1)
    
    # Filtruj transakcje w okresie (z obsługą brakującego timestamp)
    current_transactions = []
    for t in transactions:
        if "timestamp" not in t:
            continue  # Pomiń transakcje bez timestamp
        try:
            if datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S") >= start_date:
                current_transactions.append(t)
        except (ValueError, KeyError):
            continue  # Pomiń transakcje z niepoprawnym formatem
    
    # Filtruj kontrakty w okresie (obsługa różnych formatów daty)
    current_contracts = []
    for c in completed_contracts:
        completed_date_str = c.get("completed_date", "2000-01-01")
        try:
            # Spróbuj format z czasem
            contract_date = datetime.strptime(completed_date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                # Spróbuj format tylko data
                contract_date = datetime.strptime(completed_date_str, "%Y-%m-%d")
            except ValueError:
                # Jeśli niepoprawny format, pomiń
                continue
        
        if contract_date >= start_date:
            current_contracts.append(c)
    
    # CURRENT PERIOD
    # Przychody: kontrakty + pozytywne wydarzenia
    contract_revenue = sum(t.get("amount", 0) for t in current_transactions if t.get("type") == "contract_reward")
    event_revenue = sum(t.get("amount", 0) for t in current_transactions if t.get("type") == "event_reward")
    revenue = contract_revenue + event_revenue
    
    # Koszty: pracownicy + biuro + negatywne wydarzenia
    employee_hire_costs = sum(abs(t.get("amount", 0)) for t in current_transactions if t.get("type") in ["employee_hired", "employee_hire"])
    daily_costs = sum(abs(t.get("amount", 0)) for t in current_transactions if t.get("type") == "daily_costs")
    office_costs = sum(abs(t.get("amount", 0)) for t in current_transactions if t.get("type") in ["office_rent", "office_upgrade"])
    event_costs = sum(abs(t.get("amount", 0)) for t in current_transactions if t.get("type") == "event_cost")
    total_costs = employee_hire_costs + daily_costs + office_costs + event_costs
    profit = revenue - total_costs
    
    # Kontrakty
    num_contracts = len(current_contracts)
    avg_contract_value = revenue / num_contracts if num_contracts > 0 else 0
    avg_rating = sum(c.get("rating", 0) for c in current_contracts) / num_contracts if num_contracts > 0 else 0
    
    # Pracownicy
    num_employees = len(bg_data.get("employees", []))
    revenue_per_employee = revenue / num_employees if num_employees > 0 else 0
    
    # Marże
    profit_margin = (profit / revenue * 100) if revenue > 0 else 0
    cost_to_revenue_ratio = (total_costs / revenue * 100) if revenue > 0 else 0
    
    result = {
        "period": {
            "revenue": revenue,
            "revenue_breakdown": {
                "contracts": contract_revenue,
                "events": event_revenue
            },
            "costs": {
                "employee_hire": employee_hire_costs,
                "daily_costs": daily_costs,
                "office": office_costs,
                "events": event_costs,
                "total": total_costs
            },
            "profit": profit,
            "contracts": {
                "count": num_contracts,
                "avg_value": avg_contract_value,
                "avg_rating": avg_rating
            },
            "employees": {
                "count": num_employees,
                "revenue_per_employee": revenue_per_employee
            },
            "metrics": {
                "profit_margin": profit_margin,
                "cost_to_revenue_ratio": cost_to_revenue_ratio
            }
        }
    }
    
    # PREVIOUS PERIOD (dla porównania)
    if include_comparison and days < 9999:
        prev_end = start_date
        prev_start = prev_end - timedelta(days=days)
        
        # Filtruj transakcje z poprzedniego okresu (z obsługą brakującego timestamp)
        prev_transactions = []
        for t in transactions:
            if "timestamp" not in t:
                continue
            try:
                if prev_start <= datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S") < prev_end:
                    prev_transactions.append(t)
            except (ValueError, KeyError):
                continue
        
        # Filtruj kontrakty z poprzedniego okresu (obsługa różnych formatów daty)
        prev_contracts = []
        for c in completed_contracts:
            completed_date_str = c.get("completed_date", "2000-01-01")
            try:
                # Spróbuj format z czasem
                contract_date = datetime.strptime(completed_date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    # Spróbuj format tylko data
                    contract_date = datetime.strptime(completed_date_str, "%Y-%m-%d")
                except ValueError:
                    # Jeśli niepoprawny format, pomiń
                    continue
            
            if prev_start <= contract_date < prev_end:
                prev_contracts.append(c)
        
        # Przychody: kontrakty + wydarzenia
        prev_contract_revenue = sum(t.get("amount", 0) for t in prev_transactions if t.get("type") == "contract_reward")
        prev_event_revenue = sum(t.get("amount", 0) for t in prev_transactions if t.get("type") == "event_reward")
        prev_revenue = prev_contract_revenue + prev_event_revenue
        
        # Koszty: pracownicy + biuro + wydarzenia
        prev_costs = sum(abs(t.get("amount", 0)) for t in prev_transactions if t.get("type") in ["employee_hired", "employee_hire", "daily_costs", "office_rent", "office_upgrade", "event_cost"])
        prev_profit = prev_revenue - prev_costs
        prev_num_contracts = len(prev_contracts)
        
        result["previous"] = {
            "revenue": prev_revenue,
            "costs": prev_costs,
            "profit": prev_profit,
            "contracts": prev_num_contracts
        }
    
    return result


def show_kpi_dashboard(financial_data, bg_data):
    """Wyświetla dashboard z kluczowymi KPI"""
    st.markdown("### 🎯 Kluczowe Wskaźniki Wydajności")
    
    period = financial_data["period"]
    has_prev = "previous" in financial_data
    
    # Główne KPI w 3 kolumnach
    col1, col2, col3 = st.columns(3)
    
    with col1:
        revenue = period["revenue"]
        revenue_change = 0
        if has_prev and financial_data["previous"]["revenue"] > 0:
            revenue_change = ((revenue - financial_data["previous"]["revenue"]) / financial_data["previous"]["revenue"]) * 100
        
        render_kpi_card(
            "💰 Przychody",
            f"{revenue:,.0f} 💰",
            revenue_change if has_prev else None,
            "positive"
        )
    
    with col2:
        profit = period["profit"]
        profit_change = 0
        if has_prev and financial_data["previous"]["profit"] != 0:
            profit_change = ((profit - financial_data["previous"]["profit"]) / abs(financial_data["previous"]["profit"])) * 100
        
        render_kpi_card(
            "💎 Zysk Netto",
            f"{profit:,.0f} 💰",
            profit_change if has_prev else None,
            "positive" if profit >= 0 else "negative"
        )
    
    with col3:
        margin = period["metrics"]["profit_margin"]
        render_kpi_card(
            "📊 Marża Zysku",
            f"{margin:.1f}%",
            None,
            "positive" if margin >= 20 else "neutral" if margin >= 10 else "negative"
        )
    
    st.markdown("---")
    
    # Dodatkowe KPI w 4 kolumnach
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_kpi_card(
            "📝 Kontrakty",
            f"{period['contracts']['count']}",
            None,
            "neutral"
        )
    
    with col2:
        render_kpi_card(
            "⭐ Śr. Ocena",
            f"{period['contracts']['avg_rating']:.2f}",
            None,
            "positive" if period['contracts']['avg_rating'] >= 4 else "neutral"
        )
    
    with col3:
        render_kpi_card(
            "👥 Pracownicy",
            f"{period['employees']['count']}",
            None,
            "neutral"
        )
    
    with col4:
        rpe = period['employees']['revenue_per_employee']
        render_kpi_card(
            "💼 Rev/Employee",
            f"{rpe:,.0f} 💰",
            None,
            "positive" if rpe > 1000 else "neutral"
        )


def render_kpi_card(title, value, change_percent=None, sentiment="neutral"):
    """Renderuje kartę KPI z opcjonalnym trendem"""
    
    # Kolory na podstawie sentymentu
    colors = {
        "positive": {"bg": "#f0fdf4", "border": "#10b981", "text": "#065f46"},
        "negative": {"bg": "#fef2f2", "border": "#ef4444", "text": "#991b1b"},
        "neutral": {"bg": "#f8f9fa", "border": "#94a3b8", "text": "#475569"}
    }
    
    color = colors.get(sentiment, colors["neutral"])
    
    # Strzałka trendu
    trend_html = ""
    if change_percent is not None:
        if change_percent > 0:
            trend_html = f"<div style='color: #10b981; font-size: 14px;'>▲ +{change_percent:.1f}%</div>"
        elif change_percent < 0:
            trend_html = f"<div style='color: #ef4444; font-size: 14px;'>▼ {change_percent:.1f}%</div>"
        else:
            trend_html = f"<div style='color: #94a3b8; font-size: 14px;'>➡ 0%</div>"
    
    st.markdown(f"""
    <div style="background: {color['bg']}; 
                border-left: 4px solid {color['border']}; 
                padding: 16px; 
                border-radius: 8px;
                height: 100%;">
        <div style="color: {color['text']}; font-size: 12px; font-weight: 600; margin-bottom: 8px;">
            {title}
        </div>
        <div style="font-size: 24px; font-weight: bold; color: {color['text']}; margin-bottom: 4px;">
            {value}
        </div>
        {trend_html}
    </div>
    """, unsafe_allow_html=True)


def show_pl_statement(financial_data, period_type, show_comparison):
    """Wyświetla rachunek zysków i strat (P&L Statement)"""
    st.markdown("### 📋 Rachunek Zysków i Strat (P&L)")
    st.markdown(f"**Okres:** {period_type}")
    
    period = financial_data["period"]
    has_prev = "previous" in financial_data and show_comparison
    
    # Tworzenie tabeli P&L
    import pandas as pd
    
    pl_data = {
        "Pozycja": [
            "PRZYCHODY OPERACYJNE",
            "  Przychody z kontraktów",
            "  Przychody z wydarzeń",
            "  RAZEM PRZYCHODY",
            "",
            "KOSZTY OPERACYJNE",
            "  Koszty zatrudnienia (jednorazowe)",
            "  Koszty pracowników (dzienne)",
            "  Koszty biura (wynajem + ulepszenia)",
            "  Koszty z wydarzeń",
            "  RAZEM KOSZTY",
            "",
            "ZYSK/STRATA OPERACYJNA",
            "",
            "WSKAŹNIKI",
            "  Marża zysku",
            "  Stosunek kosztów do przychodów"
        ],
        "Bieżący okres": [
            "",
            f"{period['revenue_breakdown']['contracts']:,.0f} 💰",
            f"{period['revenue_breakdown']['events']:,.0f} 💰",
            f"{period['revenue']:,.0f} 💰",
            "",
            "",
            f"-{period['costs']['employee_hire']:,.0f} 💰",
            f"-{period['costs']['daily_costs']:,.0f} 💰",
            f"-{period['costs']['office']:,.0f} 💰",
            f"-{period['costs']['events']:,.0f} 💰",
            f"-{period['costs']['total']:,.0f} 💰",
            "",
            f"{period['profit']:,.0f} 💰",
            "",
            "",
            f"{period['metrics']['profit_margin']:.1f}%",
            f"{period['metrics']['cost_to_revenue_ratio']:.1f}%"
        ]
    }
    
    if has_prev:
        prev = financial_data["previous"]
        pl_data["Poprzedni okres"] = [
            "",
            "-",  # Rozbicie przychodów niedostępne dla poprzedniego okresu
            "-",
            f"{prev['revenue']:,.0f} 💰",
            "",
            "",
            "-",  # Rozbicie kosztów niedostępne
            "-",
            "-",
            "-",
            f"-{prev['costs']:,.0f} 💰",
            "",
            f"{prev['profit']:,.0f} 💰",
            "",
            "",
            "-",
            "-"
        ]
        
        # Zmiana
        rev_change = period['revenue'] - prev['revenue']
        profit_change = period['profit'] - prev['profit']
        cost_change = period['costs']['total'] - prev['costs']
        
        pl_data["Zmiana"] = [
            "",
            "-",
            "-",
            f"{rev_change:+,.0f} 💰",
            "",
            "",
            "-",
            "-",
            "-",
            "-",
            f"{-cost_change:+,.0f} 💰",
            "",
            f"{profit_change:+,.0f} 💰",
            "",
            "",
            "-",
            "-"
        ]
    
    df = pd.DataFrame(pl_data)
    
    # Stylowanie tabeli
    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        height=500
    )
    
    # Waterfall chart
    st.markdown("#### 💧 Analiza Waterfall (Przepływ Środków)")
    
    import plotly.graph_objects as go
    
    # Buduj waterfall dynamicznie (tylko niezerowe pozycje)
    x_labels = ["Przychody"]
    y_values = [period['revenue']]
    measures = ["relative"]
    texts = [f"{period['revenue']:,.0f}"]
    
    if period['costs']['employee_hire'] > 0:
        x_labels.append("Koszty<br>zatrudnienia")
        y_values.append(-period['costs']['employee_hire'])
        measures.append("relative")
        texts.append(f"-{period['costs']['employee_hire']:,.0f}")
    
    if period['costs']['daily_costs'] > 0:
        x_labels.append("Koszty<br>pracowników")
        y_values.append(-period['costs']['daily_costs'])
        measures.append("relative")
        texts.append(f"-{period['costs']['daily_costs']:,.0f}")
    
    if period['costs']['office'] > 0:
        x_labels.append("Koszty<br>biura")
        y_values.append(-period['costs']['office'])
        measures.append("relative")
        texts.append(f"-{period['costs']['office']:,.0f}")
    
    if period['costs']['events'] > 0:
        x_labels.append("Koszty<br>wydarzeń")
        y_values.append(-period['costs']['events'])
        measures.append("relative")
        texts.append(f"-{period['costs']['events']:,.0f}")
    
    x_labels.append("Zysk Netto")
    y_values.append(period['profit'])
    measures.append("total")
    texts.append(f"{period['profit']:,.0f}")
    
    fig = go.Figure(go.Waterfall(
        x = x_labels,
        y = y_values,
        measure = measures,
        text = texts,
        textposition = "outside",
        connector = {"line": {"color": "#cbd5e1"}},
        decreasing = {"marker": {"color": "#ef4444"}},
        increasing = {"marker": {"color": "#10b981"}},
        totals = {"marker": {"color": "#8b5cf6"}}
    ))
    
    fig.update_layout(
        title="Przepływ środków: Od przychodów do zysku",
        showlegend=False,
        height=400,
        yaxis_title="Monety 💰",
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def show_profitability_analysis(financial_data, bg_data):
    """Analiza rentowności"""
    st.markdown("### 💰 Analiza Rentowności")
    
    period = financial_data["period"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Wskaźniki Rentowności")
        
        # Gross Profit Margin
        st.metric(
            "Marża Zysku Brutto",
            f"{period['metrics']['profit_margin']:.1f}%",
            help="Zysk / Przychody * 100"
        )
        
        # Cost Efficiency
        efficiency = 100 - period['metrics']['cost_to_revenue_ratio']
        st.metric(
            "Efektywność Kosztowa",
            f"{efficiency:.1f}%",
            help="Im wyższa, tym lepiej zarządzasz kosztami"
        )
        
        # Average Contract Profitability
        avg_profit_per_contract = period['profit'] / period['contracts']['count'] if period['contracts']['count'] > 0 else 0
        st.metric(
            "Średni Zysk na Kontrakt",
            f"{avg_profit_per_contract:,.0f} 💰"
        )
        
        # Break-even point
        if period['costs']['daily_costs'] > 0:
            contracts_completed = period['contracts']['count']
            days_in_period = 7  # Można dynamicznie obliczyć
            daily_revenue = period['revenue'] / days_in_period if days_in_period > 0 else 0
            daily_op_costs = period['costs']['daily_costs'] / days_in_period if days_in_period > 0 else 0
            
            st.metric(
                "Dzienny Przychód",
                f"{daily_revenue:,.0f} 💰"
            )
            st.metric(
                "Dzienny Koszt Operacyjny",
                f"{daily_op_costs:,.0f} 💰"
            )
    
    with col2:
        st.markdown("#### 📈 Benchmark")
        
        # Porównanie z celami
        targets = {
            "Marża zysku": {"current": period['metrics']['profit_margin'], "target": 30, "unit": "%"},
            "Ocena klientów": {"current": period['contracts']['avg_rating'], "target": 4.5, "unit": "⭐"},
            "Rev per Employee": {"current": period['employees']['revenue_per_employee'], "target": 2000, "unit": "💰"}
        }
        
        for name, data in targets.items():
            current = data["current"]
            target = data["target"]
            # Ogranicz progress do zakresu 0-100 (obsługa wartości ujemnych)
            progress = max(0, min((current / target) * 100, 100)) if target > 0 else 0
            
            st.markdown(f"**{name}**")
            st.progress(progress / 100)
            st.markdown(f"{current:.1f}{data['unit']} / {target}{data['unit']}")
            st.markdown("")


def show_employee_roi_analysis(financial_data, bg_data):
    """Analiza ROI pracowników"""
    st.markdown("### 👥 ROI Pracowników")
    
    from data.business_data import EMPLOYEE_TYPES
    
    employees = bg_data.get("employees", [])
    period = financial_data["period"]
    
    if not employees:
        st.info("📭 Nie masz jeszcze pracowników. Zatrudnij kogoś, aby zobaczyć analizę ROI!")
        return
    
    st.markdown(f"""
    **Analiza:** Czy Twoi pracownicy generują wystarczające przychody, aby pokryć swoje koszty?
    
    - **Przychody w okresie:** {period['revenue']:,.0f} 💰
    - **Liczba pracowników:** {len(employees)}
    - **Przychód na pracownika:** {period['employees']['revenue_per_employee']:,.0f} 💰
    """)
    
    st.markdown("---")
    
    # Analiza per typ pracownika
    st.markdown("#### 📊 Analiza per typ pracownika")
    
    employee_stats = {}
    for emp in employees:
        emp_type = emp["type"]
        if emp_type not in employee_stats:
            employee_stats[emp_type] = {
                "count": 0,
                "daily_cost": EMPLOYEE_TYPES[emp_type]["koszt_dzienny"],
                "hire_cost": EMPLOYEE_TYPES[emp_type]["koszt_zatrudnienia"],
                "bonus": EMPLOYEE_TYPES[emp_type]["bonus"]
            }
        employee_stats[emp_type]["count"] += 1
    
    # Tabela ROI
    import pandas as pd
    
    roi_data = []
    for emp_type, stats in employee_stats.items():
        emp_data = EMPLOYEE_TYPES[emp_type]
        total_daily_cost = stats["daily_cost"] * stats["count"] * 7  # Zakładając 7 dni
        roi_data.append({
            "Typ": f"{emp_data['ikona']} {emp_data['nazwa']}",
            "Ilość": stats["count"],
            "Koszt/dzień": f"{stats['daily_cost']} 💰",
            "Koszt tygodniowy": f"{total_daily_cost:,.0f} 💰",
            "Bonus": stats["bonus"]
        })
    
    df = pd.DataFrame(roi_data)
    st.dataframe(df, width="stretch", hide_index=True)
    
    # Wykres kosztów pracowników
    if employee_stats:
        import plotly.graph_objects as go
        
        labels = [f"{EMPLOYEE_TYPES[t]['ikona']} {EMPLOYEE_TYPES[t]['nazwa']}" for t in employee_stats.keys()]
        values = [s['count'] * s['daily_cost'] * 7 for s in employee_stats.values()]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#f5576c'])
        )])
        
        fig.update_layout(
            title="Rozkład kosztów tygodniowych pracowników",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)


def show_category_analysis(financial_data, bg_data):
    """Analiza wydajności kategorii kontraktów"""
    st.markdown("### 📊 Analiza Kategorii Kontraktów")
    
    completed = bg_data.get("contracts", {}).get("completed", [])
    
    if not completed:
        st.info("📭 Brak ukończonych kontraktów do analizy.")
        return
    
    # Grupuj po kategoriach
    import pandas as pd
    
    category_stats = {}
    
    for contract in completed:
        category = contract.get("kategoria", "other")
        
        # Obsługa różnych formatów reward (dict lub int)
        reward_data = contract.get("reward", 0)
        if isinstance(reward_data, dict):
            reward = reward_data.get("coins", 0)
        else:
            reward = reward_data  # Stary format - reward jako int
        
        rating = contract.get("rating", 0)
        
        if category not in category_stats:
            category_stats[category] = {"count": 0, "total_reward": 0, "total_rating": 0, "contracts": []}
        
        category_stats[category]["count"] += 1
        category_stats[category]["total_reward"] += reward
        category_stats[category]["total_rating"] += rating
        category_stats[category]["contracts"].append(contract)
    
    # Przygotuj dane do tabeli
    table_data = []
    for category, stats in category_stats.items():
        count = stats["count"]
        avg_reward = stats["total_reward"] / count if count > 0 else 0
        avg_rating = stats["total_rating"] / count if count > 0 else 0
        
        table_data.append({
            "Kategoria": category.upper(),
            "Liczba kontraktów": count,
            "Łączny przychód": f"{stats['total_reward']:,.0f} 💰",
            "Średni przychód": f"{avg_reward:,.0f} 💰",
            "Średnia ocena": f"{avg_rating:.2f} ⭐"
        })
    
    # Sortuj po przychodzie
    table_data.sort(key=lambda x: float(x["Średni przychód"].replace(" 💰", "").replace(",", "")), reverse=True)
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, width="stretch", hide_index=True)
    
    # Wykres słupkowy - przychody per kategoria
    import plotly.graph_objects as go
    
    categories = [d["Kategoria"] for d in table_data]
    revenues = [float(d["Łączny przychód"].replace(" 💰", "").replace(",", "")) for d in table_data]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=revenues,
            marker_color='#667eea',
            text=revenues,
            texttemplate='%{text:,.0f} 💰',
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Łączne przychody per kategoria",
        xaxis_title="Kategoria",
        yaxis_title="Przychód (💰)",
        height=400,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top kontrakty
    st.markdown("#### 🏆 Top 5 Najbardziej Dochodowych Kontraktów")
    
    all_contracts = []
    for category, stats in category_stats.items():
        all_contracts.extend(stats["contracts"])
    
    top_contracts = sorted(all_contracts, key=lambda x: get_contract_reward_coins(x), reverse=True)[:5]
    
    for i, contract in enumerate(top_contracts, 1):
        reward = get_contract_reward_coins(contract)
        rating = contract.get("rating", 0)
        st.markdown(f"""
        **{i}. {contract.get('emoji', '📋')} {contract.get('tytul', 'Nieznany')}**  
        💰 {reward:,} monet | ⭐ {rating}/5 | 🏢 {contract.get('klient', 'Nieznany klient')}
        """)

# =============================================================================
# TAB 5: HISTORIA KONTRAKTÓW
# =============================================================================

def show_history_tab(username, user_data, industry_id="consulting"):
    """Zakładka Historia & Wydarzenia - chronologiczna oś czasu"""
    bg_data = get_game_data(user_data, industry_id)
    
    st.subheader("📜 Historia & Wydarzenia Firmy")
    
    # Sekcja losowania wydarzeń na górze
    st.markdown("### 🎲 Losowanie Wydarzenia")
    
    # BACKWARD COMPATIBILITY: Zainicjalizuj events jeśli nie istnieje
    if "events" not in bg_data:
        bg_data["events"] = {
            "history": [],
            "last_roll": None,
            "active_effects": []
        }
        save_game_data(user_data, bg_data, industry_id)
        save_user_data(username, user_data)
    
    from utils.business_game_events import should_trigger_event, get_random_event, apply_event_effects
    from datetime import datetime, timedelta
    
    # Sprawdź cooldown
    last_roll = bg_data.get("events", {}).get("last_roll")
    can_roll = True
    hours_left = 0
    minutes_left = 0
    
    if last_roll:
        last_dt = datetime.strptime(last_roll, "%Y-%m-%d %H:%M:%S")
        next_roll = last_dt + timedelta(hours=24)
        now = datetime.now()
        
        if now < next_roll:
            can_roll = False
            time_until_next = next_roll - now
            hours_left = int(time_until_next.total_seconds() / 3600)
            minutes_left = int((time_until_next.total_seconds() % 3600) / 60)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if can_roll:
            st.success("✅ **Możesz wylosować zdarzenie!** (Szansa: 20%)")
        else:
            st.warning(f"⏰ Następne losowanie za: **{hours_left}h {minutes_left}min**")
    
    with col2:
        if st.button("🎲 LOSUJ!", disabled=not can_roll, type="primary", key="roll_event"):
            # Losuj zdarzenie
            event_result = get_random_event(bg_data, user_data.get("degencoins", 0))
            
            if event_result:
                event_id, event_data = event_result
                
                # Sprawdź czy wymaga wyboru
                if event_data["type"] == "neutral" and "choices" in event_data:
                    # Zapisz zdarzenie tymczasowo w session_state
                    st.session_state["pending_event"] = (event_id, event_data)
                    st.rerun()
                else:
                    # Bezpośrednio aplikuj
                    user_data = apply_event_effects(event_id, event_data, None, user_data, industry_id)
                    save_user_data(username, user_data)
                    st.success(f"{event_data['emoji']} **{event_data['title']}**")
                    st.balloons() if event_data["type"] == "positive" else None
                    st.rerun()
            else:
                # Brak zdarzenia (80% przypadków)
                bg_data.setdefault("events", {})["last_roll"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_game_data(user_data, bg_data, industry_id)
                save_user_data(username, user_data)
                st.info("😐 Tym razem nic się nie wydarzyło. Spokojny dzień!")
                st.rerun()
    
    # Pending event (jeśli neutralne wymaga wyboru)
    if "pending_event" in st.session_state:
        event_id, event_data = st.session_state["pending_event"]
        render_event_choice_modal(event_id, event_data, username, user_data, context="history")
    
    st.markdown("---")
    
    # Zbierz wszystkie zdarzenia (kontrakty + wydarzenia)
    timeline_items = []
    
    # Dodaj ukończone kontrakty
    completed = bg_data["contracts"]["completed"]
    for contract in completed:
        timeline_items.append({
            "type": "contract",
            "date": contract.get("completed_date", ""),
            "data": contract
        })
    
    # Dodaj wydarzenia
    events_history = bg_data.get("events", {}).get("history", [])
    for event in events_history:
        timeline_items.append({
            "type": "event",
            "date": event.get("date", ""),
            "data": event
        })
    
    # Sortuj chronologicznie (najnowsze najpierw)
    timeline_items.sort(key=lambda x: x["date"], reverse=True)
    
    if not timeline_items:
        st.info("📭 Brak historii. Wykonuj kontrakty i losuj wydarzenia, aby wypełnić oś czasu!")
        return
    
    # Filtry
    st.markdown("### 🔍 Filtry")
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox(
            "Typ:",
            ["Wszystko", "Tylko kontrakty", "Tylko wydarzenia"],
            key="history_filter_type"
        )
    with col2:
        show_count = st.selectbox(
            "Pokaż:",
            [10, 25, 50, "Wszystko"],
            key="history_show_count"
        )
    with col3:
        # Dodatkowy filtr dla kontraktów
        filter_rating = st.selectbox(
            "Ocena kontraktów:",
            ["Wszystkie", "⭐⭐⭐⭐⭐ (5)", "⭐⭐⭐⭐ (4+)", "⭐⭐⭐ (3+)"],
            key="history_filter_rating"
        )
    
    # Filtrowanie
    filtered = timeline_items
    
    if filter_type == "Tylko kontrakty":
        filtered = [item for item in filtered if item["type"] == "contract"]
    elif filter_type == "Tylko wydarzenia":
        filtered = [item for item in filtered if item["type"] == "event"]
    
    if filter_rating != "Wszystkie":
        if filter_rating == "⭐⭐⭐⭐⭐ (5)":
            filtered = [item for item in filtered if item["type"] != "contract" or item["data"].get("rating", 0) == 5]
        elif filter_rating == "⭐⭐⭐⭐ (4+)":
            filtered = [item for item in filtered if item["type"] != "contract" or item["data"].get("rating", 0) >= 4]
        elif filter_rating == "⭐⭐⭐ (3+)":
            filtered = [item for item in filtered if item["type"] != "contract" or item["data"].get("rating", 0) >= 3]
    
    # Limit
    if show_count != "Wszystko":
        filtered = filtered[:show_count]
    
    st.markdown("---")
    st.markdown(f"**Znaleziono:** {len(filtered)} pozycji")
    st.markdown("---")
    
    # Wyświetl chronologiczną oś czasu
    st.markdown("### ⏰ Oś Czasu")
    
    for item in filtered:
        if item["type"] == "contract":
            render_completed_contract_card(item["data"])
        else:  # event
            render_event_history_card(item["data"])


def render_completed_contract_card(contract):
    """Renderuje kartę ukończonego kontraktu w expanderze (jak wydarzenia)"""
    
    rating = contract.get("rating", 0)
    feedback = contract.get("feedback", "Brak feedbacku")
    completed_date = contract.get("completed_date", "Nieznana data")
    reward_coins = get_contract_reward_coins(contract)
    
    # Status koloru na podstawie oceny
    if rating >= 4:
        border_color = "#10b981"  # zielony
        icon = "✅"
    elif rating >= 3:
        border_color = "#f59e0b"  # pomarańczowy
        icon = "⭐"
    else:
        border_color = "#ef4444"  # czerwony
        icon = "❌"
    
    # Tytuł expandera z metrykami
    rep_change = get_contract_reward_reputation(contract)
    rep_display = f"+{rep_change}" if rep_change >= 0 else str(rep_change)
    
    expander_title = f"{icon} {contract['emoji']} **{contract['tytul']}** - {contract['klient']} | ⭐ {rating}/5 | 💰 {reward_coins:,} | 📈 {rep_display} | 📅 {completed_date}"
    
    with st.expander(expander_title, expanded=False):
        # Metryki w karcie
        st.markdown(f"""
        <div style='background: linear-gradient(to right, #f8fafc, #f1f5f9); 
                    border-left: 4px solid {border_color}; 
                    border-radius: 8px; 
                    padding: 16px; 
                    margin: 16px 0;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
            <div style='display: flex; justify-content: space-around; text-align: center;'>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>⭐</div>
                    <div style='font-weight: 600; color: #1e293b;'>{rating}/5</div>
                    <div style='font-size: 12px; color: #64748b;'>Ocena</div>
                </div>
                <div style='border-left: 2px solid #e2e8f0; height: 60px;'></div>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>💰</div>
                    <div style='font-weight: 600; color: #1e293b;'>{reward_coins:,}</div>
                    <div style='font-size: 12px; color: #64748b;'>Zarobiono</div>
                </div>
                <div style='border-left: 2px solid #e2e8f0; height: 60px;'></div>
                <div>
                    <div style='font-size: 24px; margin-bottom: 4px;'>📈</div>
                    <div style='font-weight: 600; color: #1e293b;'>{rep_display}</div>
                    <div style='font-size: 12px; color: #64748b;'>Reputacja</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Feedback od klienta
        st.markdown("**💬 Feedback od klienta:**")
        st.info(feedback)
        
        st.markdown("---")
        
        # Szczegóły kontraktu
        # Karta 1: Opis sytuacji - Header
        st.markdown("""
        <div style='background: linear-gradient(135deg, #8b5cf615 0%, #6d28d915 100%); 
                    border-left: 4px solid #8b5cf6; 
                    border-radius: 12px 12px 0 0; 
                    padding: 12px 20px 8px 20px; 
                    margin-bottom: 0;'>
            <div style='color: #8b5cf6; 
                        font-size: 11px; 
                        text-transform: uppercase; 
                        letter-spacing: 1px; 
                        font-weight: 600;'>
                📄 OPIS SYTUACJI
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Content
        st.markdown("""
        <div style='background: linear-gradient(135deg, #8b5cf615 0%, #6d28d915 100%); 
                    border-left: 4px solid #8b5cf6; 
                    border-radius: 0 0 12px 12px; 
                    padding: 8px 20px 16px 20px; 
                    margin: 0 0 16px 0;'>
        """, unsafe_allow_html=True)
        
        st.markdown(contract['opis'])
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Karta 2: Zadanie - Header
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f59e0b15 0%, #d9770615 100%); 
                    border-left: 4px solid #f59e0b; 
                    border-radius: 12px 12px 0 0; 
                    padding: 12px 20px 8px 20px; 
                    margin-bottom: 0;'>
            <div style='color: #f59e0b; 
                        font-size: 11px; 
                        text-transform: uppercase; 
                        letter-spacing: 1px; 
                        font-weight: 600;'>
                🎯 ZADANIE
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Content
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f59e0b15 0%, #d9770615 100%); 
                    border-left: 4px solid #f59e0b; 
                    border-radius: 0 0 12px 12px; 
                    padding: 8px 20px 16px 20px; 
                    margin: 0 0 16px 0;'>
        """, unsafe_allow_html=True)
        
        st.markdown(contract['zadanie'])
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Karta 3: Twoje rozwiązanie - Header
        st.markdown("""
        <div style='background: linear-gradient(135deg, #06b6d415 0%, #0891b215 100%); 
                    border-left: 4px solid #06b6d4; 
                    border-radius: 12px 12px 0 0; 
                    padding: 12px 20px 8px 20px; 
                    margin-bottom: 0;'>
            <div style='color: #06b6d4; 
                        font-size: 11px; 
                        text-transform: uppercase; 
                        letter-spacing: 1px; 
                        font-weight: 600;'>
                ✍️ TWOJE ROZWIĄZANIE
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Content
        solution = contract.get("solution", "Brak zapisanego rozwiązania")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #06b6d415 0%, #0891b215 100%); 
                    border-left: 4px solid #06b6d4; 
                    border-radius: 0 0 12px 12px; 
                    padding: 8px 20px 16px 20px; 
                    margin: 0 0 0 0;'>
        """, unsafe_allow_html=True)
        
        st.markdown(f"```\n{solution}\n```")
        
        st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# WYDARZENIA (HELPER FUNCTIONS)
# =============================================================================

def show_events_tab(username, user_data, industry_id="consulting"):
    """Zakładka Wydarzenia - losowe zdarzenia"""
    bg_data = get_game_data(user_data, industry_id)
    
    # BACKWARD COMPATIBILITY: Zainicjalizuj events jeśli nie istnieje
    if "events" not in bg_data:
        bg_data["events"] = {
            "history": [],
            "last_roll": None,
            "active_effects": []
        }
        save_game_data(user_data, bg_data, industry_id)
        save_user_data(username, user_data)
    
    st.subheader("🎲 Wydarzenia Losowe")
    
    # Info
    st.info("""
    📰 **Jak działają wydarzenia?**
    - Co 24h możesz wylosować nowe zdarzenie (20% szansa)
    - Zdarzenia mogą być **pozytywne** 🎉, **neutralne** ⚖️ lub **negatywne** 💥
    - Niektóre wymagają od Ciebie decyzji!
    - Historia ostatnich wydarzeń poniżej
    """)
    
    st.markdown("---")
    
    # Sekcja losowania
    from utils.business_game_events import should_trigger_event, get_random_event, apply_event_effects
    from datetime import datetime, timedelta
    
    # Sprawdź cooldown
    last_roll = bg_data.get("events", {}).get("last_roll")
    can_roll = True
    hours_left = 0
    minutes_left = 0
    
    if last_roll:
        last_dt = datetime.strptime(last_roll, "%Y-%m-%d %H:%M:%S")
        next_roll = last_dt + timedelta(hours=24)
        now = datetime.now()
        
        if now < next_roll:
            can_roll = False
            time_until_next = next_roll - now
            hours_left = int(time_until_next.total_seconds() / 3600)
            minutes_left = int((time_until_next.total_seconds() % 3600) / 60)
    
    st.markdown("### 🎰 Losowanie Zdarzenia")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if can_roll:
            st.success("✅ **Możesz wylosować zdarzenie!**")
            st.caption("Szansa: 20% na zdarzenie, 80% na brak")
        else:
            st.warning(f"⏰ **Następne losowanie za: {hours_left}h {minutes_left}min**")
            st.caption("Zdarzenia można losować raz na 24 godziny")
    
    with col2:
        if st.button("🎲 LOSUJ!", disabled=not can_roll, type="primary", key="roll_event"):
            # Losuj zdarzenie
            event_result = get_random_event(bg_data, user_data.get("degencoins", 0))
            
            if event_result:
                event_id, event_data = event_result
                
                # Sprawdź czy wymaga wyboru
                if event_data["type"] == "neutral" and "choices" in event_data:
                    # Zapisz zdarzenie tymczasowo w session_state
                    st.session_state["pending_event"] = (event_id, event_data)
                    st.rerun()
                else:
                    # Bezpośrednio aplikuj
                    user_data = apply_event_effects(event_id, event_data, None, user_data, industry_id)
                    save_user_data(username, user_data)
                    st.success(f"{event_data['emoji']} **{event_data['title']}**")
                    st.balloons() if event_data["type"] == "positive" else None
                    st.rerun()
            else:
                # Brak zdarzenia (80% przypadków)
                bg_data.setdefault("events", {})["last_roll"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_game_data(user_data, bg_data, industry_id)
                save_user_data(username, user_data)
                st.info("😐 Tym razem nic się nie wydarzyło. Spokojny dzień!")
                st.rerun()
    
    # Pending event (jeśli neutralne wymaga wyboru)
    if "pending_event" in st.session_state:
        event_id, event_data = st.session_state["pending_event"]
        render_event_choice_modal(event_id, event_data, username, user_data, context="events")
    
    st.markdown("---")
    
    # Historia wydarzeń
    st.markdown("### 📜 Historia Wydarzeń")
    
    if "events" not in bg_data or not bg_data["events"].get("history"):
        st.info("Brak wydarzeń w historii. Wylosuj pierwsze zdarzenie powyżej!")
    else:
        history = bg_data["events"]["history"]
        # Filtruj elementy bez timestamp przed sortowaniem
        history_with_timestamp = [h for h in history if "timestamp" in h]
        history_sorted = sorted(history_with_timestamp, key=lambda x: x["timestamp"], reverse=True)
        
        # Pokazuj tylko ostatnie 10
        for event in history_sorted[:10]:
            render_event_history_card(event)


