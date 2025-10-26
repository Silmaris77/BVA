# 🎤 Instrukcja: Nagrywanie głosowe w AI Conversation

## Jak używać mikrofonu?

### 1️⃣ **Rozpocznij rozmowę AI**
W Business Games wybierz kontrakt: **💬 Spóźniający się Talent**

### 2️⃣ **Nagraj odpowiedź**
1. Kliknij **"🎤 Nagrywanie..."**
2. Zezwól na dostęp do mikrofonu (jeśli pytanie się pojawi)
3. **Mów wyraźnie po polsku**
4. Zakończ nagranie (automatycznie po zatrzymaniu)

### 3️⃣ **Poczekaj na rozpoznanie**
- Zobaczysz spinner: "🤖 Rozpoznaję mowę..."
- System:
  1. Konwertuje audio
  2. Rozpoznaje słowa (Google Speech Recognition)
  3. Dodaje interpunkcję i wielkie litery (Gemini AI)

### 4️⃣ **Sprawdź i wyślij**
- Rozpoznany tekst pojawi się w polu tekstowym
- Możesz go **edytować** przed wysłaniem
- Możesz **nagrać kolejne fragmenty** - dodadzą się do poprzedniego tekstu
- Kliknij **"📤 Wyślij wiadomość"**

---

## ✅ **Zalety tego rozwiązania:**

- ✨ **Automatyczna interpunkcja** - Gemini poprawia składnię
- 🎯 **Wiele nagrań** - możesz nagrywać wielokrotnie
- ✏️ **Edycja przed wysłaniem** - pełna kontrola
- 🌐 **Dowolna przeglądarka** - nie tylko Chrome/Edge
- 🔒 **Bezpieczeństwo** - audio przetwarzane lokalnie

---

## ⚠️ **Wymagania:**

- **Mikrofon** (wbudowany lub zewnętrzny)
- **Połączenie internetowe** (dla Google Speech Recognition)
- **Klucz Gemini API** (skonfigurowany w `.streamlit/secrets.toml`)

---

## 🐛 **Problemy?**

### **"❌ Nie rozpoznano mowy"**
- Mów **wyraźnie i wolno**
- Sprawdź czy mikrofon działa (test w systemie)
- Spróbuj nagrać ponownie

### **"❌ Błąd połączenia z usługą rozpoznawania mowy"**
- Sprawdź połączenie internetowe
- Odczekaj chwilę i spróbuj ponownie

### **"❌ Błąd przetwarzania audio"**
- Sprawdź czy biblioteki są zainstalowane:
  ```bash
  pip install SpeechRecognition pydub
  ```
- Upewnij się że masz zainstalowany `ffmpeg` (dla pydub)

---

## 🎓 **Wskazówki:**

1. **Mów naturalnie** - Gemini poprawi interpunkcję
2. **Nagraj fragmentami** - łatwiej edytować
3. **Sprawdź tekst** przed wysłaniem - AI czasem się myli
4. **Możesz pisać i nagrywać** - oba sposoby działają równocześnie

---

**Ten sam system działa w kontrakcie "Feedback dla nowego pracownika"! 🚀**
