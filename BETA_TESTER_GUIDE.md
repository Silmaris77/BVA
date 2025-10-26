# 🧪 Instrukcja dla Testerów Beta - BrainventureAcademy

Witaj w zespole beta testerów! Twoim zadaniem jest przetestowanie aplikacji i zgłoszenie uwag.

---

## 🎯 CO TESTUJEMY?

**BrainventureAcademy** to interaktywna platforma edukacyjna o zarządzaniu i neurobiologii, która:
- 🧠 Pomaga odkryć Twój styl uczenia się i typ przywódcy
- 📚 Oferuje lekcje z gamifikacją (XP, poziomy, monety)
- 🎮 Zawiera Business Games z AI (rozmowy, decyzje)
- 🤖 Wykorzystuje AI (Google Gemini) do generowania feedbacku
- 🎤 Ma naturalne głosy AI (ElevenLabs) z emocjami

---

## 🚀 JAK ROZPOCZĄĆ?

### **OPCJA A: Link do aplikacji (jeśli hostowana)**
1. Otwórz link: `[LINK ZOSTANIE UDOSTĘPNIONY]`
2. Zarejestruj się (wymyśl nazwę użytkownika i hasło)
3. Zaloguj się i eksploruj!

### **OPCJA B: Lokalne uruchomienie**
```bash
# 1. Sklonuj repozytorium (jeśli masz dostęp)
git clone [REPO_URL]
cd BVA

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Uruchom aplikację
streamlit run main.py

# 4. Otwórz w przeglądarce
http://localhost:8501
```

---

## 📋 CO PRZETESTOWAĆ?

### **1️⃣ REJESTRACJA I LOGOWANIE (5 min)**
- [ ] Zarejestruj nowe konto
- [ ] Wyloguj się
- [ ] Zaloguj ponownie - **działa?**
- [ ] **Pytanie:** Czy logowanie jest szybkie (<2 sekundy)?

---

### **2️⃣ DASHBOARD (5 min)**
- [ ] Sprawdź statystyki (XP, monety, poziom)
- [ ] Zobacz dostępne lekcje
- [ ] **Pytanie:** Czy wszystko wyświetla się poprawnie?
- [ ] **Pytanie:** Czy coś jest niejasne?

---

### **3️⃣ TESTY DIAGNOSTYCZNE (15-20 min)**
Idź do: **🧰 Narzędzia → Autodiagnoza**

- [ ] Wykonaj **Test Kolba** (styl uczenia się) - 10 pytań
- [ ] Wykonaj **Test Neuroleadera** (typ przywódcy) - 12 pytań  
- [ ] Wykonaj **Test MI** (inteligencje wielorakie) - 24 pytania
- [ ] Sprawdź wyniki w **Profil → Mój Profil**
- [ ] **Pytania:**
  - Czy wyniki są zrozumiałe?
  - Czy uważasz je za trafne?
  - Czy wizualizacje (wykresy) są czytelne?

---

### **4️⃣ LEKCJE (10 min)**
Idź do: **📚 Lekcje**

- [ ] Wybierz jedną lekcję (np. "Wprowadzenie do neurobiologii")
- [ ] Przejdź przez całą lekcję
- [ ] Zakończ lekcję - **otrzymałeś XP i monety?**
- [ ] Sprawdź Dashboard - **XP się zwiększyło?**
- [ ] **Pytania:**
  - Czy treść lekcji była ciekawa?
  - Czy długość lekcji jest OK?
  - Czy chciałbyś więcej interakcji?

---

### **5️⃣ BUSINESS GAMES - AI CONVERSATION (15 min)** ⭐ PRIORYTET
Idź do: **🎮 Business Games → 💬 Rozmowa: Spóźniający się Talent**

- [ ] Przeczytaj briefing
- [ ] Wyślij 2-3 wiadomości do "Marka" (NPC)
- [ ] **Pytania:**
  - Czy otrzymałeś odpowiedź od AI?
  - Czy odpowiedź była sensowna?
  - Czy widzisz **feedback** (punkty, metryki) po każdej wiadomości?
  - Czy **głos Marka** (jeśli słyszalny) brzmi naturalnie?
- [ ] Kliknij **"🏁 Zakończ"** po kilku wiadomościach
- [ ] Sprawdź **"🏁 Zakończone"** - **kontrakt tam jest?**
- [ ] **Otrzymałeś monety i XP?**

---

### **6️⃣ BUSINESS GAMES - DECISION TREE (10 min)**
Idź do: **🎮 Business Games → 🌳 Kryzys Zespołu** (lub inny kontrakt)

- [ ] Przejdź przez scenariusz decyzyjny
- [ ] Dokonaj kilku wyborów
- [ ] Zakończ kontrakt
- [ ] **Pytanie:** Czy scenariusz był angażujący?

---

### **7️⃣ MOBILE/TABLET (opcjonalnie, 5 min)**
- [ ] Otwórz aplikację na telefonie/tablecie
- [ ] **Pytania:**
  - Czy wszystko wyświetla się poprawnie?
  - Czy przyciski są klikalne?
  - Czy tekst jest czytelny?

---

## 🐛 ZGŁASZANIE BŁĘDÓW

### **Jeśli coś nie działa:**
1. **Zrób screenshot** (Win+Shift+S lub PrtScr)
2. **Zanotuj:**
   - Co robiłeś przed błędem?
   - Co się stało (błąd, crash, brak reakcji)?
   - Jaki masz system (Windows/Mac/Linux)?
   - Jaka przeglądarka (Chrome/Firefox/Edge)?
3. **Wyślij do mnie:**
   - Email: [TWÓJ_EMAIL]
   - Slack/Discord: [LINK]
   - Formularz: [GOOGLE_FORM_LINK]

### **Przykład zgłoszenia:**
```
BŁĄD: Nie mogę zakończyć kontraktu AI Conversation
KROKI:
1. Business Games → 💬 Rozmowa
2. Napisałem 3 wiadomości
3. Kliknąłem "🏁 Zakończ"
4. Nic się nie stało, kontrakt wciąż w "Aktywne"

SYSTEM: Windows 11, Chrome 118
SCREENSHOT: [załączony]
```

---

## 💬 FEEDBACK

Po zakończeniu testów, odpowiedz na te pytania:

### **OGÓLNE WRAŻENIA (1-10):**
1. Jak oceniasz **intuicyjność** interfejsu? __/10
2. Jak oceniasz **atrakcyjność wizualną**? __/10
3. Jak oceniasz **wartość edukacyjną**? __/10
4. Czy **poleciłbyś** aplikację znajomym? __/10

### **PYTANIA OTWARTE:**
1. **Co Ci się najbardziej podobało?**
   - 

2. **Co chciałbyś zmienić/ulepszyć?**
   - 

3. **Czy napotkałeś błędy? Jakie?**
   - 

4. **Jakie funkcje dodałbyś?**
   - 

5. **Czy testy diagnostyczne dały wartościowe wyniki?**
   - 

6. **Czy system XP/monet Cię motywuje?**
   - 

7. **Jak oceniasz głosy AI (jeśli słyszałeś)?**
   - 

8. **Inne uwagi:**
   - 

---

## ⏱️ CZAS TRWANIA TESTÓW

**Przewidywany czas:** 60-90 minut  
**Termin:** Do [DATA] (elastyczny, to beta!)

---

## 🎁 NAGRODA ZA TESTY

- ✅ Wczesny dostęp do pełnej wersji
- ✅ Twoje imię w credits (jeśli chcesz)
- ✅ [OPCJONALNIE: gadżet, rabat, itp.]

---

## 📞 KONTAKT

Masz pytania? Pisz:
- **Email:** [TWÓJ_EMAIL]
- **Phone/WhatsApp:** [NUMER]
- **Discord/Slack:** [LINK]

---

**Dziękuję za pomoc w rozwoju BrainventureAcademy! 🚀**

Twój feedback jest bezcenny i pomoże stworzyć lepszy produkt.

**Powodzenia w testach!** 🧪
