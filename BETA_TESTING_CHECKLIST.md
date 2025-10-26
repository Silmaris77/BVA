# 🚀 CHECKLIST - BETA TESTY BrainventureAcademy

**Data przygotowania:** 25 października 2025  
**Wersja:** 1.1.0  
**Status:** GOTOWE DO BETA TESTÓW ✅

---

## ✅ PRZED URUCHOMIENIEM

### 1. **Konfiguracja**
- [x] `DEVELOPMENT_MODE = False` (zapisy do plików włączone)
- [x] Klucze API skonfigurowane (Gemini, ElevenLabs)
- [x] `.gitignore` zabezpiecza secrets
- [x] `secrets.toml` w `.streamlit/` (nie w repozytorium!)

### 2. **Dane startowe**
- [ ] `users_data.json` - backup przed testami
- [ ] Konta testowe utworzone lub pusty start?
- [ ] Dane lekcji (`data/lessons/`) kompletne

### 3. **Funkcjonalności kluczowe**
- [x] Logowanie/Rejestracja działa
- [x] Dashboard wyświetla się poprawnie
- [x] Lekcje ładują się i zapisują postęp
- [x] System XP i poziomów działa
- [x] Testy diagnostyczne (Kolb, Neuroleader, MI) działają
- [x] Business Games - kontrakty i zakończenie działają
- [x] AI Conversation - feedback i zakończenie działa
- [x] ElevenLabs TTS - naturalne głosy z emocjami (jeśli klucz API)

---

## 🧪 TESTY DO WYKONANIA

### **TEST 1: Pierwszy użytkownik**
- [ ] Zarejestruj nowe konto
- [ ] Zaloguj się
- [ ] Sprawdź dashboard (statystyki, misje)
- [ ] Wykonaj jedną lekcję
- [ ] Zdobądź XP i monety
- [ ] Wyloguj i zaloguj ponownie - dane zapisane?

### **TEST 2: Testy diagnostyczne**
- [ ] Wykonaj Test Kolba (styl uczenia)
- [ ] Wykonaj Test Neuroleadera (typ przywódcy)
- [ ] Wykonaj Test MI (inteligencje wielorakie)
- [ ] Sprawdź profil - wyniki widoczne?
- [ ] Dashboard pokazuje pełny profil (3/3)?

### **TEST 3: Business Games - AI Conversation**
- [ ] Wejdź w Business Games → 💬 Rozmowa
- [ ] Rozpocznij kontrakt "Spóźniający się Talent"
- [ ] Wyślij 2-3 wiadomości
- [ ] Sprawdź czy pokazuje feedback (punkty, metryki)
- [ ] Kliknij "🏁 Zakończ" - kontrakt przechodzi do zakończonych?
- [ ] Sprawdź czy otrzymałeś monety i XP
- [ ] Posłuchaj głosu Marka (ElevenLabs) - naturalny?

### **TEST 4: Business Games - Decision Tree**
- [ ] Wejdź w inny kontrakt (np. Kryzys Zespołu)
- [ ] Przejdź przez scenariusz decyzyjny
- [ ] Zakończ kontrakt - sprawdź zakończenie

### **TEST 5: Wielokrotne logowania**
- [ ] Zaloguj się 3 razy z rzędu
- [ ] Sprawdź szybkość logowania (powinno być ~1-2 sekundy)
- [ ] Dane zachowane między sesjami?

### **TEST 6: Mobile/Tablet**
- [ ] Otwórz na telefonie
- [ ] Dashboard wyświetla się poprawnie?
- [ ] Przyciski klikalne?
- [ ] Nawigacja działa?

---

## 🐛 ZNANE PROBLEMY

### **Naprawione przed beta:**
- ✅ Kontrakty AI Conversation nie zamykały się (FIXED)
- ✅ Brak feedbacku po wiadomościach (FIXED)
- ✅ Przycisk "Zakończ" nie działał (FIXED)
- ✅ Duplicate key errors w event modals (FIXED)
- ✅ Wolne logowanie - 4x zapisy do JSON (FIXED - zoptymalizowane do 1x)
- ✅ Robotyczne głosy TTS (FIXED - ElevenLabs z emocjami)

### **Do sprawdzenia w beta:**
- ⚠️ ElevenLabs - klucz API może potrzebować uprawnień `text_to_speech`
- ⚠️ Fallback na gTTS jeśli ElevenLabs nie działa
- ⚠️ Performance przy wielu użytkownikach jednocześnie
- ⚠️ Wielkość pliku `users_data.json` przy 10+ użytkownikach

---

## 📊 METRYKI DO ŚLEDZENIA

### **Podczas beta testów:**
1. **Średni czas logowania** - powinno być <2 sekundy
2. **Ukończone lekcje** - ile użytkowników kończy przynajmniej 1 lekcję?
3. **Testy diagnostyczne** - % użytkowników wykonujących wszystkie 3
4. **Business Games** - średnia liczba ukończonych kontraktów
5. **Błędy** - loguj wszystkie błędy w konsoli
6. **Feedback** - notatki od testerów

### **Pytania dla testerów:**
1. Czy interfejs jest intuicyjny?
2. Czy instrukcje są jasne?
3. Czy napotkałeś błędy? Jakie?
4. Co chciałbyś zmienić/ulepszyć?
5. Czy system XP i monet jest motywujący?
6. Jak oceniasz głosy AI (ElevenLabs vs gTTS)?
7. Czy testy diagnostyczne dały wartościowe wyniki?

---

## 🔧 KONFIGURACJA DLA TESTERÓW

### **Wymagania:**
- Python 3.8+
- Przeglądarka (Chrome, Firefox, Edge)
- Stabilne połączenie internetowe (API Gemini/ElevenLabs)

### **Uruchomienie:**
```bash
# 1. Zainstaluj zależności
pip install -r requirements.txt

# 2. Uruchom aplikację
streamlit run main.py

# 3. Otwórz w przeglądarce
http://localhost:8501
```

### **Klucze API (dla Ciebie):**
- **Gemini:** `AIzaSyCDRzwz8c8EE8Mb1suxrF6kWHaBQNDqB3I` (w secrets.toml)
- **ElevenLabs:** `sk_2c76b82443ac4b1a7724b1f988c2e8a368c8a737ddbfcb10` (w secrets.toml)

⚠️ **NIE UDOSTĘPNIAJ KLUCZY PUBLICZNIE!**

---

## 🚀 DEPLOYMENT OPTIONS

### **OPCJA 1: Streamlit Cloud (Zalecane dla beta)**
1. Push kod na GitHub (bez secrets!)
2. Połącz z Streamlit Cloud: https://share.streamlit.io/
3. Dodaj secrets w panelu Streamlit Cloud
4. Share link z testerami: `https://twoja-app.streamlit.app`

**Zalety:**
- ✅ Darmowe
- ✅ Automatyczne deploymenty (push = update)
- ✅ HTTPS z certyfikatem
- ✅ Nie wymaga własnego serwera

**Limity:**
- ⚠️ 1GB RAM (wystarczy dla 5-10 użytkowników jednocześnie)
- ⚠️ Hibernacja po 7 dniach nieaktywności
- ⚠️ Public repo lub private (limit)

### **OPCJA 2: Localhost + ngrok (Szybki test)**
```bash
# Terminal 1 - uruchom Streamlit
streamlit run main.py

# Terminal 2 - udostępnij przez ngrok
ngrok http 8501
```
Share link: `https://xyz123.ngrok.io` (tymczasowy, max 2h)

### **OPCJA 3: Własny serwer (VPS)**
- Wymaga: VPS (DigitalOcean, AWS, Azure)
- Konfiguracja: Docker + Nginx + SSL
- Koszt: $5-20/miesiąc

---

## 📝 NOTATKI PO TESTACH

### **Tester 1:**
- Imię:
- Data testu:
- Feedback:
- Znalezione błędy:
- Ocena 1-10:

### **Tester 2:**
- Imię:
- Data testu:
- Feedback:
- Znalezione błędy:
- Ocena 1-10:

### **Tester 3:**
- Imię:
- Data testu:
- Feedback:
- Znalezione błędy:
- Ocena 1-10:

---

## ✅ FINAL CHECKLIST PRZED PUBLIKACJĄ

- [ ] Wszystkie testy przeszły pomyślnie
- [ ] Brak krytycznych błędów
- [ ] Performance akceptowalny
- [ ] Feedback testerów pozytywny (>7/10)
- [ ] Dokumentacja README.md aktualna
- [ ] Secrets zabezpieczone (.gitignore)
- [ ] Backup danych przed publikacją
- [ ] Plan reakcji na błędy (hotfix strategy)

---

## 🎯 KOLEJNE KROKI PO BETA

1. **Analiza feedbacku** - co zmienić?
2. **Poprawki błędów** - priorytet: krytyczne → high → medium
3. **Optymalizacje** - performance, UX
4. **Dokumentacja** - tutorial dla nowych użytkowników
5. **Marketing** - landing page, social media
6. **Skalowanie** - baza danych zamiast JSON?

---

**Powodzenia w beta testach! 🚀**
