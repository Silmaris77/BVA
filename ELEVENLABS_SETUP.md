# ElevenLabs TTS - Naturalne głosy z emocjami 🎧

## Dlaczego ElevenLabs?
- ✅ **Bardzo naturalne głosy** - brzmią jak prawdziwi ludzie
- ✅ **Emocje w głosie** - radość, smutek, złość są słyszalne
- ✅ **Polskie głosy** wysokiej jakości
- ✅ **10,000 znaków/miesiąc za darmo**
- ✅ **Automatyczne dostosowanie do emocji NPC**

## Szybka instalacja (3 kroki)

### 1️⃣ Zainstaluj bibliotekę
```powershell
pip install elevenlabs
```

### 2️⃣ Zdobądź klucz API (DARMOWY)
1. Idź na: **https://elevenlabs.io/**
2. Kliknij **"Sign Up"** i zarejestruj się (email + hasło)
3. Po zalogowaniu, idź do **Settings** (ikonka koła zębatego)
4. Kliknij **"API Keys"** w menu po lewej
5. Kliknij **"Create API Key"**
6. **Skopiuj** wygenerowany klucz

### 3️⃣ Dodaj klucz do secrets.toml
Otwórz plik `.streamlit/secrets.toml` i zmień linię:

```toml
[API_KEYS]
elevenlabs = "twój_klucz_elevenlabs_tutaj"  # ⬅️ Wklej tutaj swój klucz!
```

### ✅ Gotowe! 
System automatycznie wykryje klucz i zacznie używać ElevenLabs.
Jeśli klucza brak lub wystąpi błąd, system automatycznie przełączy się na gTTS (podstawowy TTS).

---

## Jak to działa

System **automatycznie**:
1. Wykrywa emocję z odpowiedzi AI (happy, angry, sad, anxious, etc.)
2. Dostosowuje parametry głosu do emocji:
   - **Stability** (stabilność) - wyższa dla spokojnych emocji
   - **Similarity Boost** - jak blisko oryginalnego głosu
   - **Style** - jak mocno emocja wpływa na ton
3. Generuje naturalny głos z odpowiednią intonacją

### Przykładowe mapowanie emocji:
- 😊 **Happy**: Niska stabilność (0.4), wysoki boost (0.8), style (0.6)
- 😤 **Angry**: Średnia stabilność (0.6), średni boost (0.75), style (0.5)
- 😢 **Sad**: Wysoka stabilność (0.7), niski boost (0.6), style (0.3)
- 😰 **Anxious**: Niska stabilność (0.4), średni boost (0.7), style (0.5)

---

## Dostępne głosy polskie

Obecnie używany głos: **Adam** (pNInz6obpgDQGcFmaJgB)
- Męski, ciepły, profesjonalny
- Świetny dla rozmów biznesowych

### Inne dostępne polskie głosy:
Możesz zmienić w `utils/ai_conversation_engine.py` → `generate_npc_audio_elevenlabs()`:

```python
voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam (domyślny)
# voice_id = "..."  # Antoni - energiczny, młody
# voice_id = "..."  # Arnold - głęboki, autorytatywny
```

Pełna lista: https://elevenlabs.io/voice-library (filtruj: Polish)

---

## Koszty i limity

| Plan | Znaków/miesiąc | Cena |
|------|----------------|------|
| **Free** | 10,000 | $0 |
| Starter | 30,000 | $5/mo |
| Creator | 100,000 | $22/mo |
| Pro | 500,000 | $99/mo |

### Ile to jest 10,000 znaków?
- 1 odpowiedź NPC (~50 słów) ≈ **250-300 znaków**
- 1 pełna rozmowa (~10 odpowiedzi) ≈ **2,500-3,000 znaków**
- **Free tier wystarczy na ~3-4 pełne rozmowy/miesiąc**

### Jak sprawdzić zużycie?
W ElevenLabs dashboard → **Usage** (pasek u góry)

---

## Rozwiązywanie problemów

### "⚠️ ElevenLabs niedostępne"
```powershell
pip install elevenlabs
```

### "⚠️ Brak klucza API ElevenLabs"
Sprawdź `.streamlit/secrets.toml` - czy klucz jest wpisany?

### "❌ ElevenLabs TTS Error: 401 Unauthorized"
Klucz API jest nieprawidłowy lub wygasł. Wygeneruj nowy w https://elevenlabs.io/

### "❌ ElevenLabs TTS Error: 429 Too Many Requests"
Przekroczyłeś limit 10,000 znaków/miesiąc. System automatycznie przełączy się na gTTS.

### Głos brzmi sztucznie mimo ElevenLabs
Sprawdź terminal - czy widzisz:
```
✅ ElevenLabs audio [emotion] wygenerowane dla: ...
```

Jeśli nie, to ElevenLabs nie działa. Sprawdź:
1. Czy klucz API jest poprawny
2. Czy masz dostęp do internetu
3. Czy nie przekroczyłeś limitu

---

## Przełączanie na gTTS (fallback)

System automatycznie używa gTTS jeśli:
- Brak klucza ElevenLabs
- Błąd API (401, 429, 500)
- Brak połączenia z internetem
- Biblioteka `elevenlabs` nie jest zainstalowana

Nie musisz nic robić - fallback działa automatycznie! ✅

---

## Chcesz więcej?

Możesz rozszerzyć o:
- **Różne głosy dla różnych NPC** (CEO = głęboki głos, junior = młody głos)
- **Voice cloning** - sklonuj własny głos! (Pro plan)
- **Sound effects** - dodaj szum w tle, echo, etc.

Zobacz dokumentację ElevenLabs: https://docs.elevenlabs.io/
