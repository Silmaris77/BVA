# 🚀 Business Games - System Oceny - Quick Start

## 📋 Co zostało dodane?

System oceny kontraktów Business Games z **3 trybami**:
- ⚡ **Heurystyka** - automatyczna, szybka (domyślnie aktywna)
- 🤖 **AI** - ocena przez Google Gemini
- 👨‍💼 **Mistrz Gry** - ręczna ocena przez Admina

---

## 🎯 Dla Użytkownika (Gracza)

### Jak to wygląda od strony gracza?

1. **Przejście do Business Games**
2. **Wybór kontraktu** z rynku
3. **Napisanie rozwiązania** (minimum słów)
4. **Przesłanie** - kliknięcie "Prześlij rozwiązanie"

### Co się dzieje po przesłaniu?

To zależy od trybu wybranego przez Admina:

| Tryb | Co się dzieje | Jak długo czekać |
|------|---------------|------------------|
| ⚡ Heurystyka | Natychmiastowa ocena 1-5⭐ + monety | 0 sekund |
| 🤖 AI | Ocena przez GPT + szczegółowy feedback | 5-10 sekund |
| 👨‍💼 Mistrz Gry | Trafia do kolejki → Admin oceni | 1-48 godzin |

**W trybie Mistrza Gry:**
- Zobaczysz komunikat: "✅ Rozwiązanie przesłane! Oczekuje na ocenę"
- Kontrakt pozostaje aktywny
- Gdy Admin oceni → dostaniesz powiadomienie
- Wtedy otrzymasz monety i feedback

---

## 👨‍💼 Dla Admina

### Jak zmienić tryb oceny?

1. **Zaloguj się jako Admin**
2. **Panel Administratora** (sidebar)
3. **Zakładka "Business Games"**
4. **Tab "🎯 Ustawienia Oceny"**
5. **Wybierz tryb** z dropdown
6. **Zapisz ustawienia**

### ⚡ Tryb 1: Heurystyka (domyślny)

**Kiedy używać:**
- Testy systemu
- MVP / prototyp
- Duża liczba graczy (>50)
- Brak budżetu na API
- Potrzeba natychmiastowego feedbacku

**Jak działa:**
- Automatyczna ocena oparta na długości tekstu
- Losowość ±1 gwiazdka
- Brak kosztów
- Zero opóźnień

**Konfiguracja:**
- Nie wymaga konfiguracji
- Działa out-of-the-box

---

### 🤖 Tryb 2: AI (Google Gemini)

**Kiedy używać:**
- Potrzebujesz merytorycznej oceny
- Chcesz szczegółowego feedbacku dla graczy
- Masz budżet na API (~$0.03 per ocena)
- Średnia liczba graczy (10-50)

**Jak działa:**
- Wysyła kontrakt + rozwiązanie do Gemini
- AI ocenia według 5 kryteriów
- Zwraca ocenę 1-5⭐ + feedback tekstowy
- Czas: 5-10 sekund per ocena

**Konfiguracja:**

1. **Uzyskaj klucz API Google Gemini:**
   - Wejdź na: https://platform.Google Gemini.com/api-keys
   - Zaloguj się / zarejestruj
   - Kliknij "Create new secret key"
   - Skopiuj klucz (zaczyna się od `AIza...`)

2. **Dodaj klucz w panelu admina:**
   - Business Games → Ustawienia Oceny
   - Wybierz tryb "AI"
   - Wpisz klucz API
   - Kliknij "Zapisz klucz API"

3. **Zapisz tryb:**
   - Kliknij "Zapisz ustawienia"
   - System przełączy się na tryb AI

4. **Test:**
   - Zaloguj się jako zwykły użytkownik
   - Prześlij kontrakt
   - Powinieneś zobaczyć szczegółową ocenę AI

**Koszt:**
- Model: `Geminio-mini` (najt��ńszy)
- Średnio: $0.01-0.05 per ocena
- Dla 100 kontraktów: ~$3-5

**Troubleshooting:**
- Jeśli AI nie działa → system automatycznie przełączy się na heurystykę
- Sprawdź czy klucz API jest prawidłowy
- Sprawdź limit API na koncie Google Gemini

---

### 👨‍💼 Tryb 3: Mistrz Gry

**Kiedy używać:**
- Mała grupa (do 20 osób)
- Potrzebujesz NAJWYŻSZEJ jakości
- Chcesz spersonalizowanego feedbacku
- Masz czas na ręczną ocenę
- Kurs premium / VIP uczestnicy

**Jak działa:**
1. Gracz przesyła rozwiązanie
2. Trafia do kolejki oczekujących
3. Admin loguje się do panelu
4. Przegląda rozwiązania jedno po drugim
5. Ocenia (1-5⭐) + pisze komentarz
6. Zatwierdza → gracz dostaje monety + feedback

**Konfiguracja:**

1. **Włącz tryb:**
   - Business Games → Ustawienia Oceny
   - Wybierz "👨‍💼 Mistrz Gry"
   - Zapisz ustawienia

2. **Przeglądaj kolejkę:**
   - Business Games → Tab "👨‍💼 Kolejka Mistrza Gry"
   - Zobaczysz listę oczekujących

3. **Oceń rozwiązanie:**
   - Rozwiń expandera z rozwiązaniem
   - Przeczytaj kontrakt i rozwiązanie gracza
   - Przesuń slider: 1-5⭐
   - Napisz komentarz (opcjonalnie)
   - Kliknij "✅ Zatwierdź ocenę"

4. **Co się dzieje po zatwierdzeniu:**
   - Gracz dostaje monety (zależy od gwiazdek)
   - Firma gracza dostaje reputację
   - Kontrakt przenosi się do "completed"
   - Gracz widzi Twój feedback

**Best Practices:**
- Sprawdzaj kolejkę codziennie (SLA: 48h)
- Pilne (>24h oczekiwania) są oznaczone 🔴
- Używaj komentarzy aby uczyć graczy
- Format feedbacku:
  ```
  Mocne strony:
  - ...
  - ...
  
  Do poprawy:
  - ...
  - ...
  
  Podsumowanie:
  ...
  ```

**Statystyki:**
- Tab "📊 Statystyki" pokazuje:
  - Ile ocen w kolejce
  - Ile oceniłeś
  - Średnia ocena

---

## 📊 Porównanie trybów

| Cecha | Heurystyka | AI | Mistrz Gry |
|-------|-----------|-----|------------|
| **Jakość** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Czas** | Instant | 5-10s | 1-48h |
| **Koszt** | Darmowe | ~$0.03/ocena | Czas Admina |
| **Feedback** | Brak | Szczegółowy | Spersonalizowany |
| **Skalowalność** | ∞ | ∞ | ~20 osób |
| **Setup** | Zero | API key | Regularna praca |

---

## 🔄 Migracja między trybami

**Można zmieniać tryby w dowolnym momencie!**

- Kontrakty już ocenione → pozostają ocenione
- Kontrakty aktywne → będą ocenione nowym trybem
- Kontrakty w kolejce GM → pozostaną tam (zmień tryb z powrotem aby je ocenić)

**Przykład:**
1. Zaczynasz od Heurystyki (testy)
2. Dodajesz API key → przełączasz na AI (produkcja)
3. VIP kurs → przełączasz na Mistrza Gry (premium)

---

## ❓ FAQ

**Q: Czy gracze widzą jaki tryb jest aktywny?**
A: Nie, system jest transparentny. Widzą tylko ocenę i feedback.

**Q: Co jeśli zmienię tryb w trakcie kursu?**
A: Nowe kontrakty będą oceniane nowym trybem. Stare pozostają.

**Q: Czy mogę używać AI tylko dla niektórych kontraktów?**
A: Nie, tryb jest globalny. Ale możesz przełączać w dowolnym momencie.

**Q: Co jeśli zapomnę ocenić w trybie Mistrza Gry?**
A: Kontrakty pozostaną w kolejce. Gracz czeka. System przypomina o pilnych (>24h).

**Q: Czy mogę mieć wielu Mistrzów Gry?**
A: Obecnie nie, ale można to dodać w przyszłości.

**Q: Ile kosztuje API Google Gemini?**
A: Model `Geminio-mini`: ~$0.02 per 1000 tokenów. Średnio $0.01-0.05 per ocena kontraktu.

---

## 🐛 Troubleshooting

**Problem: Nie widzę zakładki Business Games w panelu admina**
- Sprawdź czy jesteś zalogowany jako admin
- Lista adminów: `views/admin.py` → `admin_users`

**Problem: AI nie działa**
- Sprawdź klucz API (czy zaczyna się od `AIza`)
- Sprawdź saldo na koncie Google Gemini
- System automatycznie przełączy się na heurystykę

**Problem: Kolejka Mistrza Gry pusta mimo przesłanych kontraktów**
- Sprawdź czy tryb jest ustawiony na "Mistrz Gry"
- Sprawdź plik `game_master_queue.json`

**Problem: Błąd przy zatwierdzaniu oceny GM**
- Sprawdź czy użytkownik istnieje w bazie
- Sprawdź czy kontrakt jest w `active` (nie `completed`)

---

## 📝 Changelog

**v1.0 - 19 października 2025**
- ✅ Implementacja 3 trybów oceny
- ✅ Panel admina z ustawieniami
- ✅ Kolejka Mistrza Gry
- ✅ Integracja z Google Gemini API
- ✅ Testy jednostkowe
- ✅ Dokumentacja

---

**🎉 System gotowy do użycia! Powodzenia!**
