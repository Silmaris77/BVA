# ✅ FIX: Duplikowanie transkrypcji przy wielokrotnym nagrywaniu

## 🐛 **Problem zgłoszony:**
> "jak dodaję kolejną część audio, to w oknie odpowiedzi pojawi mi się kopia poprzedniej odpowiedzi i nowa odpowiedź"

**Przykład:**
```
Pierwsze nagranie: "Witaj Marku"
Drugie nagranie: "Co słychać?"

Wynik w polu tekstowym:
Witaj Marku

Witaj Marku        ← DUPLIKAT!

Co słychać?
```

## 🔍 **Przyczyna:**

Były **DWA** problemy:

### **1. Klucz `audio_input` był stały**
```python
# PRZED:
audio_data = st.audio_input("🎤", key=f"audio_input_ai_conv_{contract_id}")
```

Streamlit **nie czyści** komponentu `st.audio_input` między turami rozmowy, więc:
- Użytkownik nagrywa → przetwarza
- Wysyła wiadomość → `st.rerun()`
- **Audio z poprzedniego nagrania WCIĄŻ JEST w komponencie!**
- Przetwarza się ponownie → duplikat

### **2. Logika dopisywania zamiast zastępowania**
```python
# PRZED (skopiowane z "Feedback"):
existing_text = st.session_state.get(transcription_key, "")
if existing_text.strip():
    st.session_state[transcription_key] = existing_text + "\n\n" + transcription  # DOPISUJE!
```

Ta logika ma sens w "Feedback dla nowego pracownika", gdzie:
- Użytkownik nagrywa **wiele fragmentów**
- Na końcu wysyła **całość jako jedno rozwiązanie**

Ale w **AI Conversation**:
- Każda tura to **osobna wiadomość**
- Po wysłaniu pole **powinno się wyczyścić**
- Nowe nagranie to **nowa odpowiedź**, nie kontynuacja!

## ✅ **Rozwiązanie:**

### **1. Dynamiczny klucz `audio_input` z numerem tury**
```python
# PO:
audio_data = st.audio_input(
    "🎤 Nagrywanie...",
    key=f"audio_input_ai_conv_{contract_id}_turn{current_turn}"  # ← DODANY current_turn!
)
```

**Efekt:**
- Każda tura (turn 1, 2, 3...) ma **własny** komponent audio
- Po `st.rerun()` Streamlit tworzy **nowy** audio_input (dla nowej tury)
- Stare nagranie **nie przetwarza się ponownie**

### **2. Zastępowanie zamiast dopisywania**
```python
# PO:
# W AI Conversation: ZASTĄP tekst (nie dopisuj)
# Bo każde nagranie to nowa próba odpowiedzi w tej samej turze
st.session_state[transcription_key] = transcription  # ZASTĘPUJE!
```

**Efekt:**
- Jeśli użytkownik nagra dwa razy **w tej samej turze**, zobaczą tylko **ostatnie** nagranie
- Po wysłaniu wiadomości pole się **czyści** (bo `transcription_key = ""`)
- Nowa tura = nowy komponent audio = czyste pole tekstowe

## 📝 **Zmienione linie w `views/business_games.py`:**

### **Linia 2610:**
```python
# PRZED:
key=f"audio_input_ai_conv_{contract_id}"

# PO:
key=f"audio_input_ai_conv_{contract_id}_turn{current_turn}"
```

### **Linie 2667-2676:**
```python
# PRZED (10 linii z logiką dopisywania):
existing_text = st.session_state.get(transcription_key, "")
if existing_text.strip():
    st.session_state[transcription_key] = existing_text.rstrip() + "\n\n" + transcription
else:
    st.session_state[transcription_key] = transcription

# PO (2 linie - proste zastępowanie):
# W AI Conversation: ZASTĄP tekst (nie dopisuj)
st.session_state[transcription_key] = transcription
```

## 🎯 **Rezultat:**

### **Scenariusz 1: Wielokrotne nagrywanie W TEJ SAMEJ TURZE**
```
Tura 1:
1. Nagraj: "Witaj" → pole: "Witaj."
2. Nagraj ponownie: "Witaj Marku" → pole: "Witaj Marku." (zastąpione!)
3. Wyślij → NPC odpowiada
```

### **Scenariusz 2: Nowa tura po wysłaniu**
```
Tura 1: Nagraj "Witaj" → Wyślij
Tura 2: Pole tekstowe CZYSTE ✅
        Komponent audio CZYSTY ✅
        Nagraj "Jak sprawy?" → pole: "Jak sprawy?"
        (bez duplikatu poprzedniej wiadomości!)
```

## 🧪 **Test:**

1. Login → Business Games → 💬 Spóźniający się Talent
2. **Tura 1:**
   - Nagraj: _"witaj marku"_
   - Sprawdź pole: `Witaj Marku.` ✅
   - Kliknij **📤 Wyślij**
3. **Tura 2:**
   - Sprawdź pole: **(puste)** ✅
   - Nagraj: _"co słychać"_
   - Sprawdź pole: `Co słychać?` ✅ (bez "Witaj Marku")
   - Kliknij **📤 Wyślij**
4. **Tura 3:**
   - Sprawdź pole: **(puste)** ✅
   - **BEZ duplikatów!** ✅

---

## 📊 **Porównanie: "Feedback" vs "AI Conversation"**

| Aspekt | Feedback dla nowego pracownika | AI Conversation |
|--------|-------------------------------|----------------|
| **Klucz audio_input** | `audio_input_{contract_id}` | `audio_input_{contract_id}_turn{turn}` |
| **Wielokrotne nagrania** | Dopisywanie (`\n\n`) | Zastępowanie |
| **Wysłanie** | Na końcu (całość) | Po każdej turze |
| **Czyszczenie** | Nigdy (do końca) | Po każdym wysłaniu |
| **Cel** | Długi feedback (akapity) | Krótkie odpowiedzi (dialog) |

---

**Teraz działa poprawnie - bez duplikatów! 🎉**
