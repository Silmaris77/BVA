"""
Speech-to-Text Component dla Streamlit
Używa Web Speech API (Chrome/Edge) do rozpoznawania mowy
"""

import streamlit as st
import streamlit.components.v1 as components

def render_speech_to_text_button(key: str = "stt", language: str = "pl-PL"):
    """
    Renderuje przycisk mikrofonu do rozpoznawania mowy.
    Transkrybowany tekst zostanie zapisany w st.session_state[f"{key}_transcript"]
    
    Args:
        key: Unikalny klucz komponentu
        language: Język rozpoznawania (domyślnie polski)
    """
    
    # Inicjalizuj session state dla transkrypcji
    if f"{key}_transcript" not in st.session_state:
        st.session_state[f"{key}_transcript"] = ""
    
    # HTML/JS komponent z Web Speech API
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
        <div style="display: flex; align-items: center; gap: 10px;">
            <button id="mic-btn" 
                    style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        border: none;
                        border-radius: 50%;
                        width: 50px;
                        height: 50px;
                        font-size: 24px;
                        cursor: pointer;
                        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                        transition: all 0.3s ease;
                    "
                    onmouseover="this.style.transform='scale(1.1)'"
                    onmouseout="this.style.transform='scale(1)'"
                    title="Kliknij aby nagrać (wymaga Chrome/Edge)">
                🎤
            </button>
            <span id="status" style="font-size: 14px; color: #666;"></span>
        </div>
        
        <script>
        (function() {{
            const button = document.getElementById('mic-btn');
            const status = document.getElementById('status');
            let recognition = null;
            let isRecording = false;
            
            // Sprawdź dostępność Web Speech API
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
                status.textContent = '❌ Brak wsparcia (użyj Chrome/Edge)';
                button.disabled = true;
                button.style.opacity = '0.5';
                button.style.cursor = 'not-allowed';
                return;
            }}
            
            // Inicjalizuj Speech Recognition
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            recognition = new SpeechRecognition();
            recognition.lang = '{language}';
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            
            button.onclick = function() {{
                if (isRecording) {{
                    recognition.stop();
                    return;
                }}
                
                try {{
                    recognition.start();
                    isRecording = true;
                    button.style.background = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
                    button.textContent = '⏺️';
                    status.textContent = '🎙️ Nagrywanie...';
                }} catch (e) {{
                    console.error('Error:', e);
                    status.textContent = '❌ ' + e.message;
                }}
            }};
            
            recognition.onresult = function(event) {{
                const transcript = event.results[0][0].transcript;
                const confidence = event.results[0][0].confidence;
                
                // Komunikacja z Streamlit przez query params
                const url = new URL(window.location.href);
                url.searchParams.set('{key}_text', transcript);
                window.parent.location.href = url.toString();
                
                status.textContent = `✅ "${{transcript}}" (${{(confidence * 100).toFixed(0)}}%)`;
            }};
            
            recognition.onerror = function(event) {{
                let msg = '';
                switch(event.error) {{
                    case 'no-speech': msg = 'Nie wykryto mowy'; break;
                    case 'audio-capture': msg = 'Brak mikrofonu'; break;
                    case 'not-allowed': msg = 'Brak uprawnień'; break;
                    case 'network': msg = 'Brak internetu'; break;
                    default: msg = event.error;
                }}
                status.textContent = '❌ ' + msg;
                resetButton();
            }};
            
            recognition.onend = function() {{
                resetButton();
            }};
            
            function resetButton() {{
                button.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                button.textContent = '🎤';
                isRecording = false;
            }}
        }})();
        </script>
    </body>
    </html>
    """
    
    # Renderuj komponent
    components.html(html_code, height=70)
    
    # Sprawdź czy jest nowy tekst w query params
    params = st.query_params
    if f"{key}_text" in params:
        transcript = params[f"{key}_text"]
        st.session_state[f"{key}_transcript"] = transcript
        # Wyczyść param
        del params[f"{key}_text"]


def get_speech_transcript(key: str = "stt") -> str:
    """
    Pobiera ostatnią transkrypcję z session_state i ją czyści.
    
    Returns:
        Transkrybowany tekst lub pusty string
    """
    transcript_key = f"{key}_transcript"
    if transcript_key in st.session_state:
        transcript = st.session_state[transcript_key]
        st.session_state[transcript_key] = ""  # Wyczyść po pobraniu
        return transcript
    return ""
