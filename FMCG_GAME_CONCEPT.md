# 🛒 FMCG Sales Simulator - Koncept Gry

## 📋 Przegląd

**FMCG Sales Simulator** to interaktywna symulacja biznesowa, w której gracz wciela się w rolę Junior Sales Representative w firmie FreshLife Poland. Celem gry jest rozwijanie umiejętności sprzedażowych poprzez realistyczne scenariusze wizyt handlowych w kanale detalicznym (sklepy osiedlowe, kioski).

## 🎯 Cele Edukacyjne

1. **Techniki sprzedaży B2B** - budowanie relacji, identyfikacja potrzeb, prezentacja wartości
2. **Zarządzanie czasem i energią** - optymalizacja tras, priorytetyzacja klientów
3. **Trade marketing** - wykorzystanie narzędzi POS, promocji, gratisów
4. **Zarządzanie portfolio** - optymalizacja mix produktów, wypychanie konkurencji z półki
5. **Rozwój kariery** - uczenie się przez feedback menedżerski (coaching on-the-job)

## 🏢 Świat Gry

### FreshLife Poland
- **Branża:** FMCG (Fast-Moving Consumer Goods)
- **Model biznesowy:** Producent własnych produktów (100% portfolio)
- **Portfolio:** 12 produktów w 5 kategoriach (Personal Care, Food, Home Care, Snacks, Beverages)
  - **Marża:** 25-45% - standardowa dla producenta
  - **Popularność:** Średnia - budująca się marka (wymaga aktywnej sprzedaży)
  - **Wyzwanie:** Walka o shelf space z dużymi korporacjami (Unilever, P&G, Nestlé)
- **Konkurencja (NIE sprzedawana przez FreshLife):** Znane marki już obecne w sklepach (Dove, Danone, Fa, Kotlin, etc.)

### Terytorium: Piaseczno
- **Typ klientów:** Sklepy osiedlowe, kioski, małe markety
- **Liczba klientów:** 12 lokalizacji
- **Charakterystyka:** Różne osobowości właścicieli, różne potrzeby, różny poziom trudności

## 🎮 Mechaniki Gry

### 1. System Energii
- **Energia początkowa:** 100% każdego dnia
- **Koszt wizyty:** Zależny od odległości i czasu trwania wizyty
- **Regeneracja:** Pełna regeneracja po zakończeniu dnia
- **Strategia:** Gracz musi planować trasę i liczbę wizyt

### 2. Status Klientów
- **PROSPECT** 🔓 - Potencjalny klient (nie kupuje jeszcze)
- **ACTIVE** ✅ - Aktywny klient (regularnie kupuje)
- **LOST** ❌ - Utracony klient (przestał kupować)

**Przejścia statusów:**
- PROSPECT → ACTIVE: Po udanej pierwszej sprzedaży
- ACTIVE → LOST: Brak wizyt przez >30 dni lub bardzo słabe wizyty
- LOST → ACTIVE: Możliwy powrót po odbudowaniu relacji

### 3. System Reputacji
- **Skala:** 0-100 punktów na klienta
- **Czynniki wpływające:**
  - Jakość rozmowy (AI evaluation)
  - Regularne wizyty
  - Dotrzymywanie obietnic
  - Wartość dodana (narzędzia trade marketing)
- **Decay:** -2 pkt/dzień po 7 dniach bez wizyty

### 4. Rozmowy AI (Gemini 2.0 Flash)
- **Osobowości klientów:** Każdy właściciel sklepu ma unikalną osobowość, priorytety, obawy
- **Pamięć kontekstowa:** AI pamięta:
  - Poprzednie wizyty i ustalenia
  - Zamówione produkty i ich ilości
  - Użyte narzędzia trade marketing (ulotki, promocje, etc.)
  - Obietnice złożone przez gracza
- **Ocena rozmowy:** AI ocenia jakość (1-5⭐), prawdopodobieństwo zamówienia, wpływ na reputację

### 5. 🔍 Client Discovery System (Odkrywanie Klienta)

#### Koncepcja
Wiedza o kliencie **nie jest dana** od początku - gracz musi ją **odkryć** poprzez pytania i aktywne słuchanie podczas wizyt. To realistyczny element sprzedaży B2B, gdzie budowanie profilu klienta jest kluczowe.

#### Poziomy Znajomości Klienta
- **⭐☆☆☆☆ Nieznajomy** (0-2 wizyty) - Podstawowe dane, większość "Do ustalenia"
- **⭐⭐☆☆☆ Powierzchowny** (3-4 wizyty) - Kilka odkrytych informacji
- **⭐⭐⭐☆☆ Dobry** (5-7 wizyt) - Większość profilu odkryta
- **⭐⭐⭐⭐☆ Bardzo dobry** (8-10 wizyt) - Niemal pełny profil
- **⭐⭐⭐⭐⭐ Ekspert** (10+ wizyt) - Wszystko odkryte, pełne zrozumienie

#### Pola Profilu Klienta
**Dane podstawowe (zawsze widoczne):**
- Nazwa sklepu, lokalizacja, dystans od bazy
- Status (PROSPECT/ACTIVE/LOST)
- Reputacja (0-100)

**Dane do odkrycia (początkowo "Do ustalenia"):**
- 👤 **Charakterystyka właściciela** - osobowość, styl podejmowania decyzji
- 🎯 **Główni klienci sklepu** - demografia, potrzeby
- 🛒 **Obecnie sprzedawane marki** - co jest na półce (konkurencja)
- 💡 **Potrzeby/Bolesności** - problemy do rozwiązania
- 💰 **Potencjał zamówienia** - typowa wartość zamówienia
- 📅 **Preferowana częstotliwość** - jak często zamawia
- ⚖️ **Priorytet decyzyjny** - co jest najważniejsze (cena/jakość/wsparcie)

#### AI Ekstrakcja Informacji
Po każdej wizycie **Gemini 2.0 Flash** analizuje transkrypt rozmowy:

**Input:** Pełna treść rozmowy gracz ↔ klient

**Output:** JSON z odkrytymi informacjami:
```json
{
  "charakterystyka": "Konserwatywny, niechętny zmianom, liczy każdą złotówkę",
  "glowni_klienci": "Seniorzy z osiedla (60+ lat)",
  "obecne_marki": ["Dove", "Fa", "Danone", "Bakoma"],
  "potrzeby": ["Wysokie ceny od hurtowni", "Brak wsparcia marketingowego"],
  "potencjal": "300-500 zł",
  "czestotliwosc": "Co 2 tygodnie",
  "priorytet": "Cena > Jakość",
  "notatka": "Klient wspomniał, że jego klienci szukają tanich produktów"
}
```

**Wyświetlanie:**
- 🎉 **Po wizycie:** "Odkryłeś nowe informacje o kliencie!"
- Lista co się zmieniło (diff)
- Aktualizacja poziomu znajomości

#### Korzyści z Odkrywania
✅ **Im więcej wiesz → lepsze dopasowanie oferty**
- Gracz może dostosować argumenty sprzedażowe
- Wyższe prawdopodobieństwo zamówienia

✅ **Klienci doceniają pamięć**
- Bonus do reputacji za wykorzystanie wiedzy: "Pamięta Pan, że wspominał Pan o..."
- AI ocenia czy gracz używa odkrytych informacji

✅ **Progresja i gamifikacja**
- **Achievement:** "🔍 Detektyw" - odkryj wszystkie pola u 5 klientów
- **Achievement:** "⚡ Speed Learner" - odkryj 80% profilu w 2 wizytach
- **Achievement:** "📚 Ekspert Relacji" - osiągnij poziom 5⭐ z 3 klientami

#### Implementacja w UI
**Tab: Klienci**
- Poziom znajomości (⭐⭐⭐☆☆) obok nazwy klienta
- Expander "📋 Profil klienta" z podziałem:
  - ✅ Odkryte informacje (pogrubione)
  - ❓ Do ustalenia (szare, placeholdery)

**Tab: Rozmowa (przed wizytą)**
- Przypomnienie profilu klienta (sidebar)
- Podpowiedzi jakie pytania zadać (jeśli poziom <3⭐)

**Tab: Rozmowa (po wizycie)**
- 🎉 Popup: "Nowe odkrycia!" z listą co się zmieniło
- Aktualizacja poziomu znajomości

### 6. 📦 Katalog Produktów (Szczegółowy)

#### Struktura Opisu Produktu
Każdy z 12 produktów FreshLife ma **pełny storytelling** dostępny od początku gry:

**Dane podstawowe:**
- Nazwa, kategoria, emoji
- Cena detaliczna, marża (% i PLN)
- Popularność (pasek 0-100%)

**Rozszerzony opis (modal/expander):**
- 📖 **O produkcie** - opis, USP, skład, opakowanie
- ✅ **Przewagi nad konkurencją** - porównanie z 2-3 markami
- 🎯 **Dla kogo** - target demographic
- 💬 **Argumenty sprzedażowe** - gotowe zdania do użycia w rozmowie
- 📊 **Rotacja** - jak szybko produkt się sprzedaje (szybka/średnia/wolna)

**Przykład - FreshLife BodyWash Natural:**
```
🧴 FreshLife BodyWash Natural
━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Cena: 12.99 zł | Marża: 35% (4.55 zł)
📦 Opakowanie: 250ml, z pompką
🌿 Kategoria: Personal Care > Żele pod prysznic

📖 O produkcie:
Naturalny żel pod prysznic z ekstraktami z aloesu 
i zielonej herbaty. Bez parabenów, SLS i barwników. 
Idealny dla skóry wrażliwej. Piękne, ekologiczne 
opakowanie z recyclingu.

✅ Przewagi nad konkurencją:
• vs Dove Natural (15.99 zł): 
  - Tańszy o 3 zł (-19%)
  - Lepsza marża: 35% vs 18%
• vs Fa Natural (13.99 zł):
  - Bardziej naturalny skład (97% vs 85%)
  - Podobna cena, lepsza marża: 35% vs 20%

🎯 Dla kogo:
• Kobiety 25-45 lat świadome składu
• Rodzice szukający bezpiecznych produktów
• Osoby z wrażliwą skórą
• Ekologiczni konsumenci

💬 Argumenty sprzedażowe:
"Widzę że ma Pan/Pani Dove Natural za 15.99. Nasz 
BodyWash ma podobną jakość i naturalny skład, ale 
jest tańszy dla klienta końcowego (12.99) i Pan/Pani 
zarabia więcej (35% vs 18%). To idealna opcja dla 
klientów szukających oszczędności bez kompromisów 
w jakości."

📊 Rotacja: Średnia (7-10 dni przy 10 szt)
🏷️ Sugerowane zamówienie początkowe: 6-10 szt
```

#### UI dla Produktów
**Tab: Produkty**
- Karta produktu (grid 3 kolumny)
- Przycisk **"ℹ️ Szczegóły"** → modal z pełnym opisem
- Przycisk **"📋 Kopiuj argumenty"** → kopiuje do schowka

**Tab: Rozmowa (podczas wizyty)**
- Quick reference panel "📦 Produkty"
- Możliwość podglądnięcia argumentów bez opuszczania czatu
- Sugestie AI: "Klient wspomniał o wysokich cenach - pokaż FreshLife BodyWash (tańszy od Dove)"

### 7. System Zamówień
- **Katalog produktów:** 12 produktów FreshLife (5 kategorii)
- **Interfejs:** Grupowanie po kategoriach, szczegółowe opisy dostępne na klik
- **Kalkulator:** Automatyczne liczenie:
  - Wartości zamówienia
  - Marży całkowitej (w PLN)
  - Średniej marży (w %)
- **Historia:** Szczegółowe zapisy wszystkich zamówień per klient
- **Shelf space battle:** Informacja o produktach konkurencji już obecnych u klienta (odkrywane stopniowo)

### 8. 👔 Coaching On-the-Job (FUKO Feedback)

#### Koncepcja
Gracz może poprosić swojego menedżera o wspólną wizytę rozwojową. Menedżer **obserwuje** rozmowę (nie uczestniczy) i po zakończeniu wizyty udziela feedbacku w profesjonalnej formule FUKO.

#### Dostępność
- **Tydzień 1:** Maksymalnie 2 wizyty rozwojowe
- **Późniejsze tygodnie:** Feature do rozbudowy (np. 1x/miesiąc, tylko do trudnych klientów)

#### Rola Menedżera
✅ **Obserwuje** rozmowę  
✅ **Analizuje** zachowania handlowca  
✅ **Udziela feedbacku** po wizycie  
❌ **NIE uczestniczy** w rozmowie  
❌ **NIE pomaga** graczowi podczas rozmowy

#### Feedback w Formule FUKO

**FUKO** to framework używany w korporacjach do udzielania konstruktywnego feedbacku:

**F - Fakty**  
Opisz konkretne zachowania zaobserwowane podczas wizyty (cytuj fragmenty rozmowy)

**U - Ustosunkowanie**  
Wyraź swoją ocenę - co było dobre, co wymaga poprawy

**K - Konsekwencje**  
Opisz skutki zaobserwowanych zachowań (dla sprzedaży, relacji z klientem, rozwoju)

**O - Oczekiwania**  
Określ konkretne zachowania i techniki, których oczekujesz w przyszłości

#### Obszary Feedbacku

AI Menedżer wybiera **2 najważniejsze** obszary z listy:

1. **Nawiązanie kontaktu** - pierwsze wrażenie, small talk, budowanie relacji
2. **Identyfikacja potrzeb** - pytania odkrywające, aktywne słuchanie
3. **Prezentacja wartości** - przedstawienie rozwiązania dopasowanego do potrzeb
4. **Obsługa obiekcji** - reakcja na wątpliwości klienta
5. **Zamykanie sprzedaży** - techniki closing, call-to-action
6. **Budowanie współpracy** - perspektywa długoterminowa, follow-up

#### Przykład Feedbacku

```
📋 Obszar 1: Identyfikacja potrzeb klienta

F - Fakty:
Podczas rozmowy zauważyłem, że przeszedłeś szybko do prezentacji produktów. 
Zadałeś tylko jedno pytanie: "Co Pan sądzi o naszych produktach?" zanim 
zacząłeś prezentować TomatoRed.

U - Ustosunkowanie:
Pozytywnie oceniam Twoją energię i entuzjazm dla produktów. Jednak rozmowa 
była zbyt zorientowana na produkt, a za mało na klienta. Brakowało pytań 
odkrywających rzeczywiste potrzeby sklepu.

K - Konsekwencje:
Klient może czuć się przytłoczony informacjami o produkcie, którego być może 
wcale nie potrzebuje. Zmniejsza to prawdopodobieństwo zamówienia i budowania 
długoterminowej relacji opartej na zaufaniu.

O - Oczekiwania:
W następnych wizytach zacznij od 3-4 pytań odkrywających:
- "Jakie kategorie produktów najlepiej się sprzedają w Pana sklepie?"
- "Z jakimi wyzwaniami boryka się Pan w zarządzaniu asortymentem?"
- "Co jest dla Pana najważniejsze przy wyborze dostawcy?"
Dopiero po zidentyfikowaniu potrzeb przechodź do prezentacji rozwiązania.
```

#### Implementacja Techniczna
- **Checkbox:** "🎓 Wizyta rozwojowa z menedżerem" przed rozpoczęciem rozmowy
- **Informacja:** Banner podczas rozmowy: "👔 Menedżer obserwuje wizytę..."
- **AI Generator:** Gemini 2.0 Flash analizuje transkrypt rozmowy i ocenę
- **Wyświetlanie:** Po ocenie wizyty, przed finalizacją zamówienia
- **Zapis:** Feedback zapisany w `visit_history` z flagą `manager_feedback`
- **Historia:** Możliwość przeglądania feedbacku z poprzednich wizyt rozwojowych

#### Korzyści dla Gracza
✅ **Uczenie się przez feedback** - konkretne wskazówki rozwojowe  
✅ **Realizm symulacji** - odwzorowuje prawdziwe praktyki korporacyjne  
✅ **Bezpieczne środowisko** - można eksperymentować z technikami sprzedaży  
✅ **Progresja** - śledzenie rozwoju w różnych obszarach  
✅ **Motywacja** - widzialne rezultaty nauki i poprawy

### 9. Narzędzia Trade Marketing
- **🎁 Gratis/próbki** - bezpłatne produkty dla klienta
- **💰 Rabat** - obniżka ceny
- **📄 Materiały POS** - ulotki, plakaty, wobblery
- **🎯 Promocja** - akcja promocyjna (np. 2+1 gratis)
- **🚚 Darmowa dostawa** - free shipping

**Wpływ:** Zwiększają szansę na zamówienie, budują relację

### 10. System Tygodniowy
- **5 dni roboczych:** Poniedziałek - Piątek
- **Cele tygodniowe:** Wartość sprzedaży, liczba wizyt
- **Reset:** W poniedziałek resetuje się licznik wizyt i energia
- **Progresja:** Zwiększająca się trudność w kolejnych tygodniach

## 📊 Interfejs Użytkownika

### Tab: Dashboard
- Metryki: Energia, liczba klientów (Prospect/Active/Lost), sprzedaż miesięczna
- Dzień/Tydzień: Aktualny dzień tygodnia, numer tygodnia
- Statusy klientów: Podsumowanie w kartkach
- Cele: Postęp względem celów tygodniowych/miesięcznych

### Tab: Klienci
- **Mapa interaktywna** (Folium): Wizualizacja lokalizacji klientów
- **Kolory pinezek:**
  - 🔵 Niebieski - PROSPECT
  - 🟢 Zielony - ACTIVE
  - 🔴 Czerwony - LOST
- **Popup:** Nazwa, typ, status, dystans od bazy

### Tab: Produkty
- **Filtry:**
  - Kategoria: Personal Care, Food, Home Care, Snacks, Beverages
  - Wyszukiwarka: Po nazwie produktu
- **Karty produktów (Grid 3 kolumny):**
  - Emoji kategorii (🧴🥛🧽🍪🥤)
  - Nazwa produktu FreshLife
  - Cena detaliczna
  - Marża (% i PLN)
  - Pasek popularności
- **Informacja o konkurencji:** Panel "Co sprzedaje konkurencja?" (edukacyjny)

### Tab: Rozmowa
1. **Wybór klienta** - dropdown z listą klientów (nazwa, status, dystans)
2. **Preview kosztu** - czas dojazdu, czas wizyty, koszt energii
3. **Checkbox coaching** - Opcja wizyty rozwojowej z menedżerem (jeśli dostępna)
4. **Historia wizyt** - Expander z 3 ostatnimi wizytami:
   - Data, jakość, wartość zamówienia
   - Podsumowanie AI
   - Zamówione produkty
   - Użyte narzędzia trade marketing
   - Feedback menedżerski (FUKO) - jeśli była wizyta rozwojowa
5. **Rozmowa AI:**
   - Chat interface (gracz ↔ klient)
   - Pamięć kontekstowa
   - Ocena jakości rozmowy (1-5⭐)
   - Feedback menedżerski (jeśli wybrano coaching)
6. **System zamówień:**
   - Produkty FreshLife pogrupowane po kategoriach
   - Selektor ilości dla każdego produktu
   - Kalkulator: wartość, marża, średnia %
   - Szczegóły zamówienia (expander)
   - Info: Jakie produkty konkurencji klient już ma
7. **Finalizacja:**
   - Wartość zamówienia (auto-wyliczona lub ręczna)
   - Narzędzia trade marketing (multiselect)
   - Liczba zadań wykonanych
   - Przycisk "Zapisz wizytę"

### Poza tabami: Koniec Dnia
- **Pilne wizyty** - Warning o klientach wymagających wizyty
- **Przycisk "Zakończ dzień"** - Przejście do następnego dnia
- **Debug info** - Collapsible panel z danymi technicznymi

## 🔄 Progresja

### Krótkoterminowa (Dzień)
- Planowanie tras (optymalizacja energii)
- Prowadzenie wizyt
- Finalizacja zamówień
- Analiza feedbacku menedżerskiego

### Średnioterminowa (Tydzień)
- Osiąganie celów tygodniowych
- Budowanie relacji z klientami
- Wypychanie konkurencji z półek (zwiększanie share of shelf)
- Wykorzystanie wizyt rozwojowych (coaching)

### Długoterminowa (Miesiąc/Gra)
- Zmiana statusów klientów (PROSPECT → ACTIVE)
- Wzrost reputacji
- Awans (Junior → Mid → Senior Sales Rep)
- Odblokowanie trudniejszych terytoriów
- Rozwój kompetencji (tracking obszarów feedbacku)

## 🎓 Elementy Edukacyjne

### Koncepcje Biznesowe
- **Share of Shelf** - Walka o miejsce na półce z dużymi markami
- **Customer Lifetime Value** - Wartość długoterminowej relacji
- **Territory Management** - Optymalizacja tras i priorytetyzacji
- **Trade Marketing ROI** - Kiedy używać których narzędzi?
- **Relationship Selling** - Budowanie zaufania zamiast transakcji jednorazowych
- **Competitive Displacement** - Strategia wypierania konkurencji

### Soft Skills
- **Aktywne słuchanie** - Identyfikacja potrzeb przez pytania
- **Komunikacja perswacyjna** - Prezentacja wartości
- **Obsługa obiekcji** - Radzenie sobie z wątpliwościami
- **Negocjacje** - Znajdowanie win-win
- **Time management** - Priorytetyzacja działań
- **Przyjmowanie feedbacku** - Uczenie się z FUKO i rozwój

### Rozwój przez Coaching
- **Samoświadomość** - Rozpoznawanie własnych słabych punktów przez feedback
- **Deliberate Practice** - Świadome doskonalenie konkretnych technik
- **Progresja kompetencji** - Tracking rozwoju w 6 obszarach sprzedaży
- **Profesjonalny feedback** - Nauka struktury FUKO do stosowania w przyszłości

## 🚀 Plany Rozwoju

### Faza 1 (MVP) ✅
- [x] System tabów (Dashboard, Klienci, Produkty, Rozmowa)
- [x] Rozmowy AI z pamięcią
- [x] System zamówień z kalkulatorem
- [x] Historia wizyt ze szczegółami
- [x] Coaching on-the-job z feedbackiem FUKO

### Faza 2 (Rozbudowa Coachingu)
- [ ] Wybór obszaru feedbacku przez gracza
- [ ] Różne style menedżerskie (supportive/demanding/analityczny)
- [ ] Menedżer uczestniczy w rozmowie (demo/wsparcie)
- [ ] Tracking progresji w obszarach (wizualizacja rozwoju)
- [ ] Achievement: "Samodzielny handlowiec" (10 wizyt bez coachingu z sukcesem 4+)

### Faza 3 (Zaawansowane Mechaniki)
- [ ] Dashboard z wykresami (Plotly)
- [ ] Top 5 produktów/klientów
- [ ] System poziomów (Junior → Mid → Senior → Key Account Manager)
- [ ] Odblokowywanie trudniejszych klientów
- [ ] Konkurencja (inni handlowcy walczą o tych samych klientów)
- [ ] Sezonowość (różne produkty w różnych porach roku)

### Faza 4 (Multiplayer/Social)
- [ ] Ranking graczy
- [ ] Współpraca zespołowa (przekazywanie klientów)
- [ ] Wyzwania tygodniowe
- [ ] Mentoring (doświadczeni gracze pomagają juniorom)

## 💡 Inspiracje

- **Reality:** Prawdziwe praktyki firm FMCG (P&G, Unilever, Nestlé)
- **Coaching:** Struktury feedbacku z korporacji (FUKO, GROW, STAR)
- **Gameplay:** Symulatory biznesowe (Sim City, Game Dev Tycoon)
- **AI:** Realistyczne rozmowy (Character.AI, Replika)

## 📚 Wartość Edukacyjna dla BVA

### Dla Studentów
- Praktyczne przećwiczenie teorii sprzedaży B2B
- Bezpieczne środowisko do eksperymentowania
- Natychmiastowy feedback (AI + menedżer)
- Budowanie portfolio kompetencji

### Dla Wykładowców
- Narzędzie do demonstracji konceptów
- Dane o postępach studentów
- Możliwość tworzenia scenariuszy/case studies
- Integration z curriculum (FMCG module)

### Dla Firm Partnerskich
- Ocena kompetencji kandydatów
- Pre-onboarding training
- Assessment center tool
- Employer branding (nowoczesne narzędzia)

---

## 🎯 Kluczowe Różnicujące Cechy

1. **AI z pamięcią** - Nie tylko chatbot, ale prawdziwa symulacja relacji biznesowej
2. **Realistyczny model producenta** - Tylko własne produkty, walka z konkurencją o shelf space
3. **Coaching FUKO** - Profesjonalny rozwój przez strukturalny feedback
4. **Trade marketing** - Narzędzia jak w prawdziwej pracy handlowca
5. **Progresja wielopoziomowa** - Od dnia przez tydzień do kariery

**Status projektu:** 🚧 W rozwoju (Faza 1 - MVP ukończona)  
**Ostatnia aktualizacja:** 2025-10-29
