# 🎤 Przewodnik po nagrywaniu audio w BVA FMCG Simulator

## Jak działa nagrywanie odpowiedzi?

W panelu wizyt możesz teraz nagrywać swoje wypowiedzi **bezpośrednio przez przeglądarkę** używając mikrofonu komputera.

# � Przewodnik po nagrywaniu audio w BVA FMCG Simulator

## Jak działa nagrywanie odpowiedzi?

W panelu wizyt możesz teraz **nagrywać swoje wypowiedzi jednym kliknięciem** używając mikrofonu komputera.

### � Jak nagrać odpowiedź (SUPER PROSTE!)

#### Metoda 1: Nagrywanie jednym przyciskiem ⭐ NAJŁATWIEJSZE

1. **Kliknij ikonę mikrofonu** 🎤 na panelu nagrywania
2. **Przeglądarka zapyta o dostęp** do mikrofonu - kliknij **"Zezwól"**
3. **Mów swoją odpowiedź** - przycisk zmieni kolor na czerwony (nagrywanie aktywne)
4. **Kliknij ponownie** ikonę mikrofonu aby **zatrzymać nagrywanie**
5. Nagranie zostanie **automatycznie przetworzone i transkrybowane** 🎯

**To wszystko! Jedna ikona, dwa kliknięcia!** ✨

#### Metoda 2: Wgrywanie gotowego pliku audio

1. Nagraj plik na telefonie/komputerze (Dyktafon, Voice Recorder, etc.)
2. Kliknij "Browse files" w sekcji alternatywnej
3. Wybierz plik (WAV, MP3, M4A, OGG, WEBM)
4. Plik zostanie przetworzony

### 🔧 Wymagania techniczne

#### Przeglądarka
- **Chrome/Edge** - pełne wsparcie ✅
- **Firefox** - pełne wsparcie ✅
- **Safari** - pełne wsparcie ✅

#### Mikrofon
- Wbudowany mikrofon laptopa ✅
- Zewnętrzny mikrofon USB ✅
- Słuchawki z mikrofonem ✅
- Mikrofon w kamerze internetowej ✅

### 🎯 Jak uzyskać najlepszą jakość transkrypcji?

1. **Mów wyraźnie** - nie śpiesz się, artykułuj
2. **Unikaj hałasu** - zamknij okna, wyłącz muzykę
3. **Trzymaj mikrofon blisko** - optymalna odległość: 15-30 cm
4. **Używaj odpowiedniego sprzętu** - słuchawki z mikrofonem dają lepsze rezultaty niż mikrofon laptopa
5. **Mów naturalnie** - używaj pełnych zdań, unikaj "eee", "mmm"

### 🤖 Proces przetwarzania

```
Nagranie → Konwersja do WAV → Google Speech Recognition → 
Gemini AI (dodawanie interpunkcji) → Gotowa transkrypcja
```

1. **Nagranie audio** - HTML5 MediaRecorder API
2. **Konwersja formatu** - pydub (AudioSegment)
3. **Rozpoznawanie mowy** - Google Speech Recognition (pl-PL)
4. **Post-processing** - Gemini 2.0 Flash dodaje interpunkcję
5. **Wynik** - gotowa transkrypcja w polu tekstowym

### ⚠️ Rozwiązywanie problemów

#### Przeglądarka nie prosi o dostęp do mikrofonu
- Sprawdź czy strona używa HTTPS (localhost jest OK)
- W ustawieniach przeglądarki sprawdź uprawnienia dla mikrofonu
- Odśwież stronę (F5)

#### Transkrypcja jest niedokładna
- Powtórz nagranie mówiąc wolniej i wyraźniej
- Sprawdź czy mikrofon działa (przetestuj w innej aplikacji)
- Spróbuj użyć słuchawek z mikrofonem zamiast mikrofonu laptopa

#### Błąd "Nie udało się rozpoznać mowy"
- Sprawdź połączenie internetowe (potrzebne do Google Speech API)
- Upewnij się że mówiłeś wystarczająco długo (minimum 1-2 sekundy)
- Sprawdź czy nagranie nie jest puste

#### Nagranie się nie pojawia
- Sprawdź czy kliknąłeś "Zatrzymaj nagrywanie"
- Odczekaj kilka sekund - przetwarzanie może potrwać
- Sprawdź konsolę błędów w przeglądarce (F12)

### 📝 Edycja transkrypcji

Po automatycznej transkrypcji możesz:
- ✏️ **Edytować tekst** bezpośrednio w polu tekstowym
- ➕ **Dodać więcej** - nagraj kolejną część, zostanie dopisana
- 🔄 **Zacząć od nowa** - wyczyść pole tekstowe i nagraj ponownie

### 🎓 Wskazówki dla trenerów

1. **Demonstracja** - pokaż użytkownikom jak nagrywać przed pierwszą wizytą
2. **Test mikrofonu** - poproś o krótkie testowe nagranie "Cześć, jestem [imię]"
3. **Feedback** - zachęcaj do słuchania własnych nagrań przed wysłaniem
4. **Praktyka** - pierwsze nagrania mogą być niezręczne, to normalne

### 🔐 Bezpieczeństwo i prywatność

- Nagrania NIE są zapisywane na serwerze
- Audio jest przetwarzane tylko w celu transkrypcji
- Po transkrypcji plik audio jest kasowany
- Tylko tekst transkrypcji zostaje w sesji użytkownika

### 💡 Alternatywne opcje

Jeśli nagrywanie nie działa:
1. **Pisz bezpośrednio** - użyj pola tekstowego bez nagrywania
2. **Wgraj plik** - nagraj na telefonie, prześlij plik
3. **Dyktuj do asystenta** - użyj asystenta głosowego systemu, skopiuj tekst

## 🚀 Gotowe!

Teraz możesz swobodnie rozmawiać z AI klientami w Twoim FMCG Simulatorze!

**Powodzenia w Twojej karierze sprzedawcy! 🎯**
