# 🎤 UPGRADE: Speech-to-Text w AI Conversation

## Data: 2025-10-25

## 🔄 **Co się zmieniło?**

### **USUNIĘTO:** Web Speech API (custom HTML/JS)
- ❌ Plik: `utils/speech_to_text.py` (156 linii)
- ❌ Custom HTML component z iframe
- ❌ Query params communication
- ❌ Tylko Chrome/Edge
- ❌ Problemy z stabilnością

### **DODANO:** Natywny `st.audio_input()` (jak w "Feedback")
- ✅ Streamlit native component
- ✅ **Google Speech Recognition** (offline processing)
- ✅ **Gemini post-processing** (interpunkcja + wielkie litery)
- ✅ Dowolna przeglądarka
- ✅ Stabilne rozwiązanie

---

## 📝 **Zmiany w kodzie:**

### **views/business_games.py** (linie 2595-2690)

#### **PRZED:**
```python
from utils.speech_to_text import render_speech_to_text_button, get_speech_transcript

col_mic, col_info = st.columns([1, 5])
with col_mic:
    render_speech_to_text_button(key=f"stt_{contract_id}", language="pl-PL")
    
transcript = get_speech_transcript(key=f"stt_{contract_id}")
if transcript:
    st.session_state[f"text_area_{contract_id}"] += " " + transcript
```

#### **PO:**
```python
audio_data = st.audio_input("🎤 Nagrywanie...", key=f"audio_input_ai_conv_{contract_id}")

if audio_data is not None:
    # 1. Konwersja audio (pydub)
    audio = AudioSegment.from_file(tmp_path)
    
    # 2. Rozpoznanie mowy (SpeechRecognition)
    recognizer = sr.Recognizer()
    transcription = recognizer.recognize_google(audio_data_sr, language="pl-PL")
    
    # 3. Post-processing (Gemini - interpunkcja)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Dodaj interpunkcję: {transcription}")
    
    # 4. Dopisz do text_area
    st.session_state[f"text_area_{contract_id}"] += " " + transcription
```

---

## ✨ **Korzyści:**

| Aspekt | Web Speech API | st.audio_input() |
|--------|----------------|------------------|
| **Stabilność** | ⚠️ Problemy z iframe | ✅ Natywne Streamlit |
| **Przeglądarki** | ❌ Tylko Chrome/Edge | ✅ Wszystkie |
| **Interpunkcja** | ❌ Brak | ✅ Gemini AI |
| **Wielokrotne nagrania** | ⚠️ Trudne | ✅ Łatwe |
| **Edycja przed wysłaniem** | ✅ Tak | ✅ Tak |
| **Kod** | 156 linii custom | ~70 linii natywnych |

---

## 🧪 **Test:**

1. Login → Business Games → **💬 Spóźniający się Talent**
2. Kliknij **"🎤 Nagrywanie..."**
3. Powiedz: _"Witaj Marku rozumiem że masz problem z punktualnością"_
4. Poczekaj na rozpoznanie
5. Sprawdź pole tekstowe - powinno być:
   ```
   Witaj Marku, rozumiem, że masz problem z punktualnością.
   ```
   (z przecinkami i kropką dodanymi przez Gemini)

---

## 📚 **Dokumentacja:**

- **Instrukcja dla użytkowników:** `docs/AUDIO_INPUT_GUIDE.md`
- **Fix session isolation:** `AI_CONVERSATION_USER_FIX.md`

---

## ⚠️ **Wymagania:**

Sprawdź `requirements.txt`:
```txt
SpeechRecognition>=3.10.0  ✅
pydub>=0.25.1              ✅
```

Opcjonalnie (dla lepszej konwersji audio):
```bash
# Windows (przez Chocolatey)
choco install ffmpeg

# Lub ręcznie z: https://ffmpeg.org/download.html
```

---

## 🎯 **Podsumowanie:**

- ✅ **Usunięto:** `utils/speech_to_text.py` + `STT_GUIDE.md`
- ✅ **Dodano:** Natywny `st.audio_input()` w `views/business_games.py`
- ✅ **Bonus:** Gemini dodaje interpunkcję automatycznie
- ✅ **Kompatybilność:** Taki sam system jak w "Feedback dla nowego pracownika"

**Gotowe do testowania! 🚀**
