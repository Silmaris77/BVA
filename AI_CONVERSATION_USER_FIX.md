# FIX: AI Conversation - separacja sesji per użytkownik + Speech-to-Text

## 🐛 **Problem #1: Współdzielony stan sesji**
Różni użytkownicy współdzielili ten sam stan konwersacji AI. 
Gdy użytkownik "Max" założył firmę i wybrał kontrakt "Spóźniający się talent", zobaczył stan z poprzedniej gry (innego użytkownika).

### 🔍 **Przyczyna:**
Klucz session_state był: `ai_conv_{contract_id}` - **BEZ username**!

To oznaczało, że wszyscy użytkownicy mieli wspólny stan dla tego samego kontraktu.

### ✅ **Rozwiązanie:**
Zmieniono klucz na: `ai_conv_{username}_{contract_id}`

## 🎤 **Ulepszenie #2: Speech-to-Text**
Zamieniono niestabilny Web Speech API (custom HTML/JS) na **natywny komponent Streamlit**.

### **Stare rozwiązanie (usunięte):**
- Custom HTML/JS z Web Speech API
- Tylko Chrome/Edge
- Problemy z iframe communication
- Plik: `utils/speech_to_text.py` (usunięty)

### **Nowe rozwiązanie:**
- `st.audio_input()` - natywny komponent Streamlit
- **Google Speech Recognition** (offline processing)
- **Gemini post-processing** - automatyczne dodanie interpunkcji
- Działa tak samo jak w "Feedback dla nowego pracownika"

**Kod:**
```python
audio_data = st.audio_input("🎤 Nagrywanie...", key=f"audio_input_ai_conv_{contract_id}")

if audio_data is not None:
    # 1. Konwersja audio (pydub)
    # 2. Rozpoznanie mowy (SpeechRecognition + Google)
    # 3. Post-processing (Gemini - interpunkcja)
    # 4. Dopisanie do text_area
```

**Wymagane biblioteki:**
- `SpeechRecognition>=3.10.0` ✅ (już w requirements.txt)
- `pydub>=0.25.1` ✅ (już w requirements.txt)

---

## 📋 **Zmodyfikowane pliki:**

#### **1. utils/ai_conversation_engine.py**
Wszystkie funkcje teraz przyjmują `username` jako parametr:

```python
def initialize_ai_conversation(contract_id: str, npc_config: Dict, scenario_context: str, username: Optional[str] = None):
    if username is None:
        username = st.session_state.get("username", "default_user")
    conv_key = f"ai_conv_{username}_{contract_id}"  # ← USERNAME DODANY!
```

**Zmienione funkcje:**
- `initialize_ai_conversation()` - dodano `username` param
- `get_conversation_state()` - dodano `username` param
- `process_player_message()` - dodano `username` param
- `calculate_final_conversation_score()` - dodano `username` param
- `reset_conversation()` - dodano `username` param

#### **2. views/business_games.py**
Wszystkie wywołania teraz przekazują `username`:

```python
# PRZED:
conversation = get_conversation_state(contract_id)
initialize_ai_conversation(contract_id, npc_config, scenario_context)

# PO:
conversation = get_conversation_state(contract_id, username)
initialize_ai_conversation(contract_id, npc_config, scenario_context, username)
```

**Zmienione wywołania:**
- Linia 2234-2237: `get_conversation_state()`, `initialize_ai_conversation()`
- Linia 2258: `calculate_final_conversation_score()`
- Linia 2363: `reset_conversation()`
- Linia 2379: `calculate_final_conversation_score()` (w zakończeniu)
- Linia 2653-2657: `process_player_message()`
- Linia 2671: Klucz przycisku "Zakończ" zmieniony na `ai_conv_{username}_{contract_id}`

**Zmieniony Speech-to-Text (linie 2595-2690):**
- Usunięto import `utils.speech_to_text`
- Dodano `st.audio_input()` z przetwarzaniem przez:
  - `SpeechRecognition` (Google API)
  - `pydub` (konwersja audio)
  - `Gemini` (post-processing - interpunkcja)

#### **3. utils/speech_to_text.py**
**USUNIĘTY** - zastąpiony przez `st.audio_input()`

## 🧪 **Test:**

### **Scenariusz testowy:**

1. **Użytkownik "Alice":**
   - Zakłada firmę
   - Wybiera "Spóźniający się talent"
   - Rozmawia z Markiem (2 tury)
   - **NIE kończy** kontraktu

2. **Użytkownik "Max":**
   - Zakłada firmę
   - Wybiera TEN SAM kontrakt "Spóźniający się talent"
   - Powinien zobaczyć: **NOWĄ rozmowę** (nie konwersację Alice)

### **Oczekiwany wynik:**
✅ Max widzi czystą rozmowę (tura 1)  
✅ Alice może kontynuować swoją rozmowę (tura 3)  
✅ Każdy użytkownik ma własny stan

### **Przed fixem:**
❌ Max widział rozmowę Alice (tura 3)  
❌ Wspólny stan dla wszystkich użytkowników

## 📊 **Wpływ na inne funkcje:**

- **Session state:** Klucze teraz zawierają username - każdy user ma izolowany stan
- **Backward compatibility:** Stare sesje (bez username w kluczu) zostaną zignorowane - użytkownicy zaczną od nowa
- **Performance:** Brak wpływu - tylko zmiana nazwy klucza

## 🚀 **Deploy:**

```powershell
# Zrestartuj Streamlit:
streamlit run main.py
```

**Uwaga:** Użytkownicy z aktywną rozmową zobaczą ją jako "niezainicjowaną" i rozpoczną od początku (bo klucz się zmienił).

---

**Fix gotowy! Każdy użytkownik ma teraz własną konwersację AI! 🎯**
