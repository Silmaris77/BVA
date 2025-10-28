# Szybka instalacja ElevenLabs TTS 🚀

## Krok po kroku (5 minut)

### 1. Zainstaluj bibliotekę
Otwórz PowerShell w folderze projektu i uruchom:
```powershell
pip install elevenlabs
```

### 2. Zdobądź darmowy klucz API
1. Idź na **https://elevenlabs.io/**
2. Kliknij **Sign Up** (niebieski przycisk w prawym górnym rogu)
3. Zarejestruj się przez email lub Google
4. Po zalogowaniu, kliknij **ikonę kółka zębatego** (Settings) u dołu po lewej
5. W menu po lewej wybierz **API Keys**
6. Kliknij **+ Create**
7. Nazwij klucz (np. "BVA App") i kliknij **Create**
8. **SKOPIUJ** wygenerowany klucz (zaczyna się od `sk_...`)

### 3. Dodaj klucz do projektu
Otwórz plik: `.streamlit\secrets.toml`

Znajdź sekcję:
```toml
[API_KEYS]
gemini = "AIzaSy..."
elevenlabs = "twój_klucz_elevenlabs_tutaj"  # ⬅️ TU!
```

Zamień `twój_klucz_elevenlabs_tutaj` na skopiowany klucz:
```toml
elevenlabs = "sk_1234567890abcdef..."  # ⬅️ Twój prawdziwy klucz
```

**ZAPISZ PLIK!**

### 4. Uruchom ponownie Streamlit
W terminalu gdzie uruchomiłeś aplikację:
1. Naciśnij **Ctrl+C** (zatrzymaj)
2. Uruchom ponownie: `streamlit run main.py`

### 5. Przetestuj!
1. Wejdź w **Business Games**
2. Zaakceptuj kontrakt **💬 Rozmowa: Spóźniający się Talent**
3. Wyślij pierwszą wiadomość
4. **Posłuchaj odpowiedzi NPC** 🎧

Jeśli wszystko działa, w terminalu zobaczysz:
```
✅ ElevenLabs audio [anxious] wygenerowane dla: Mark siedzi przy biurku...
```

---

## Weryfikacja

### ✅ Działa - jak poznać?
- W terminalu widzisz: `✅ ElevenLabs audio [emotion]...`
- Głos brzmi **bardzo naturalnie** (jak prawdziwa osoba)
- Słychać **emocje** w głosie (niepokój, radość, smutek)

### ❌ Nie działa - co robić?

**Problem 1: Nie ma dźwięku**
- Sprawdź czy klucz API jest **poprawnie wklejony** w secrets.toml
- Sprawdź czy plik jest **zapisany**
- **Uruchom ponownie** Streamlit (Ctrl+C → `streamlit run main.py`)

**Problem 2: Błąd "401 Unauthorized"**
- Klucz API jest **nieprawidłowy**
- Wejdź ponownie na https://elevenlabs.io/ i **wygeneruj nowy klucz**

**Problem 3: Błąd "429 Too Many Requests"**
- Przekroczyłeś **limit 10,000 znaków/miesiąc**
- System automatycznie przełączy się na **gTTS** (podstawowy głos)
- Poczekaj do następnego miesiąca lub kup **płatny plan**

**Problem 4: Słyszę podstawowy głos (robotyczny)**
- ElevenLabs nie działa - sprawdź terminal
- Jeśli widzisz `ℹ️ Brak klucza ElevenLabs, używam gTTS...`
- Sprawdź **krok 3** - czy klucz jest dodany?

---

## Co dalej?

🎉 **Gotowe!** Teraz każda rozmowa z NPC będzie miała naturalny głos z emocjami!

📖 **Więcej informacji**: Zobacz `ELEVENLABS_SETUP.md`

🔧 **Zmiana głosu**: Edytuj `utils/ai_conversation_engine.py` → `voice_id`

💰 **Sprawdź zużycie**: https://elevenlabs.io/ → Usage (pasek u góry)
