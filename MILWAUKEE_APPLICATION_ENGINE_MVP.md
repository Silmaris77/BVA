# Milwaukee Application First™ Tool - MVP Documentation

**Status:** MVP Ready for Testing  
**Data:** 28 grudnia 2025  
**Wersja:** 1.0

---

## 📋 Podsumowanie wykonanej pracy

### ✅ Zrealizowane komponenty

#### 1. Struktura danych (3 pliki JSON)

**`data/milwaukee/applications.json`**
- 3 pełne aplikacje z realnymi danymi:
  - **Hydraulik - instalacje wewnętrzne**: Ciasne przestrzenie, beton/cegła, M12 platforma
  - **Warsztat samochodowy**: Zastąpienie pneumatyki, M18 klucze udarowe, wysoka powtarzalność
  - **Serwis mobilny / UR**: Różnorodność, PACKOUT, uniwersalność M18
- Każda aplikacja zawiera:
  - Kontekst (4 zmienne: typ klienta, typ pracy, materiały, skala)
  - Charakterystyka pracy
  - Pytania pogłębiające (discovery questions)
  - Rekomendowany ekosystem (narzędzia + baterie + akcesoria + PACKOUT + PPE)
  - Skrypt perswazyjny (problem → konsekwencja → rozwiązanie → korzyści → proof → obiekcje → CTA)
  - Kalkulator ROI
  - Case studies

**`data/milwaukee/products_ecosystem.json`**
- **26 produktów** z pełnymi danymi:
  - 8 narzędzi (M12 CH, M12 FPD, M12 FID, M18 FHIWF12, M18 FPD, M18 FID, M18 FMT, M12 FIR)
  - 4 baterie (M12 2.0Ah, M12 4.0Ah, M18 5.0Ah, M18 8.0Ah HIGH OUTPUT)
  - 6 akcesoriów (wiertła SDS+, bity SHOCKWAVE, nasadki udarowe, przedłużki, brzeszczoty multitool, wiertła metal)
  - 5 organizacja PACKOUT (skrzynka, organizer nasadki, torba, organizer drobnicowy)
  - 2 PPE (okulary, rękawice)
- Każdy produkt:
  - SKU, pełna nazwa, kategoria, platforma
  - Cena PLN
  - Cechy kluczowe (key_features)
  - Korzyści (benefits)
  - Aplikacje (mapping do applications)
- **3 gotowe bundle** (pakiety promocyjne z oszczędnościami)

**`data/milwaukee/discovery_questions.json`**
- Pytania kontekstowe (4 zmienne):
  - Typ klienta (6 opcji: hydraulik, warsztat, serwis mobilny, elektryk, stolarstwo, budowa)
  - Typ pracy (ciągła, projektowa, serwisowa, awaryjna)
  - Materiały/środowisko (multi-select: beton, metal, drewno, wilgoć, ciasne przestrzenie, wysokość)
  - Skala (solo, 2-3, 5-10, 10+)
- Pytania pogłębiające per typ klienta:
  - **Hydraulik**: 4 pytania z scoring (M12 vs M18, pojemność baterii, częstotliwość)
  - **Warsztat**: 4 pytania (koła/dzień, pneumatyka, zapieczenia, liczba mechaników)
  - **Serwis mobilny**: 4 pytania (koszt przestoju, powroty po sprzęt, najczęstsze zadania, organizacja)
- System scoring:
  - Każda odpowiedź → punkty dla konkretnych produktów
  - Automatyczne dostosowanie rekomendacji na podstawie odpowiedzi
- Obiekcje + odpowiedzi:
  - "To jest drogie" → ROI calculation
  - "Mam już Bosch/Makita" → Pain point identification + test
  - "Czy M12 wystarczy?" → Technical match
  - "Baterie się rozładują" → Battery sizing

#### 2. Logika aplikacji

**`utils/milwaukee_recommender.py`** (380 linii)
- Klasa `MilwaukeeRecommender`:
  - `match_application(context)` - dopasowanie aplikacji do kontekstu klienta (scoring 0-100%)
  - `get_discovery_questions(typ_klienta)` - pobierz pytania dla typu klienta
  - `calculate_product_scores(answers)` - scoring produktów na podstawie odpowiedzi
  - `build_recommendation_package(app_id)` - zbuduj pełny pakiet (narzędzia + baterie + akcesoria + organizacja + PPE)
  - `get_persuasion_script(app_id)` - skrypt sprzedażowy
  - `get_roi_calculator(app_id)` - dane ROI
  - `get_case_studies(app_id)` - prawdziwe przykłady
  - `get_bundle_for_application(app_id)` - gotowe pakiety promocyjne
- Singleton pattern - jedna instancja w całej aplikacji
- Załadowanie wszystkich danych przy starcie

#### 3. Interfejs użytkownika

**`views/milwaukee_application_engine.py`** (600+ linii)
- **4-poziomowy wizard**:
  
  **POZIOM 1: Kontekst klienta**
  - 4 zmienne (selectbox + multiselect)
  - Real-time implications dla wybranych materiałów
  - Walidacja (musi wybrać przynajmniej 1 materiał)
  
  **POZIOM 2: Wybór aplikacji**
  - Automatyczne dopasowanie aplikacji do kontekstu
  - Karty aplikacji z scoring dopasowania
  - Pokaż 3 pierwsze charakterystyki
  - Przycisk "Wybierz" dla każdej aplikacji
  
  **POZIOM 3: Pytania pogłębiające**
  - Dynamiczne ładowanie pytań dla typu klienta
  - 4 typy pytań: scale, choice, multi_choice, yes_no, number
  - Tooltips z "purpose" (dlaczego pytamy)
  - Real-time scoring produktów
  
  **POZIOM 4: Rekomendacja + Skrypt**
  - 4 taby:
    - **📦 Pakiet produktów**: Narzędzia, baterie, akcesoria, PACKOUT, PPE z cenami i uzasadnieniem
    - **💬 Skrypt perswazyjny**: Problem → Konsekwencja → Rozwiązanie → Korzyści → Proof → Obiekcje → CTA
    - **💰 Kalkulator ROI**: Interaktywny kalkulator z custom wartościami
    - **🏆 Case Studies**: Prawdziwe przykłady z rynku
  
- **Progress bar** (4 kroki) z wizualną indykacją
- **Navigation buttons**: Wstecz, Restart
- **Akcje końcowe**:
  - 📋 After Visit (feedback po wizycie)
  - 📄 Eksportuj PDF (w przygotowaniu)
  - 📧 Wyślij email (w przygotowaniu)
  - 💾 Zapisz wizytę (JSON do `data/milwaukee/visits/`)

**`views/milwaukee_after_visit.py`** (400+ linii)
- **After Visit Mode** - feedback loop:
  
  **9 sekcji feedback**:
  1. Czy wizyta się odbyła? (data, czas trwania)
  2. Czy kontekst był trafny? (weryfikacja założeń)
  3. Czy aplikacja była trafiona? (inna była lepsza?)
  4. Ocena pytań discovery (które zadałeś, które dało najwięcej)
  5. Produkty (co zaprezentowałeś, czego brakowało, co niepotrzebne)
  6. Skuteczność przekazu (czy użyłeś skryptu, jak skuteczny 1-10)
  7. Obiekcje klienta (wybór z listy + własne)
  8. Rezultat (sprzedaż, oferta, follow-up, brak zainteresowania)
  9. Samoocena (rating 1-10, co poszło dobrze, co poprawić)
  
  **🤖 Auto-sugestie**:
  - Analiza odpowiedzi → konkretne sugestie doskonalenia
  - Np. "Rozważ dodatkowe pytania pre-wizyta aby lepiej zrozumieć kontekst"
  - Np. "Spróbuj konkretnego CTA zamiast ogólnej oferty"
  
  **Zapis feedback**: JSON do `data/milwaukee/feedback/` z timestamp i metadatą

#### 4. Integracja z systemem

**Lokalizacja**: Tab w zakładce Narzędzia (`views/tools.py`):
- **Tab 9**: 🔴 Milwaukee Application Engine
- Automatyczne sprawdzanie uprawnień (resource_tags)
- Jeśli użytkownik nie ma dostępu → komunikat o braku uprawnień

**Permissions** (`config/resource_tags.json`):
```json
"tools_menu": {
  "milwaukee_app_engine": ["Milwaukee"]
}
```
- Application Engine widoczny TYLKO dla użytkowników Milwaukee
- Użytkownicy innych firm widzą komunikat: "Ta funkcja jest dostępna tylko dla użytkowników Milwaukee"

**Przekierowanie z Dashboard**:
```python
st.session_state.tools_tab = 'milwaukee'
st.session_state.page = 'tools'
```
- Możliwość dodania szybkiego dostępu z Dashboardu (jak dla Autodiagnozy)

---

## 🎯 Kluczowe cechy MVP

### Strategiczne
1. **Application First™ filozofia** - nie zaczynamy od produktu, tylko od zrozumienia pracy klienta
2. **4-zmienne kontekstu** zamiast prostych checkboxów - filtruje 80% szumu przed SKU
3. **Inteligentne pytania pogłębiające** - budują eksperckość, nie tylko zbierają dane
4. **Skrypt perswazyjny** - gotowy coaching w kieszeni (problem → ROI → proof → CTA)
5. **Tryb After Visit** - zamyka pętlę uczenia (audyt → narzędzie → feedback → doskonalenie)

### Operacyjne
1. **Automatyczne dopasowanie aplikacji** - scoring 0-100% na podstawie kontekstu
2. **Dynamiczny scoring produktów** - odpowiedzi zmieniają rekomendacje
3. **Pełny ekosystem** - nie tylko narzędzie, ale baterie + akcesoria + PACKOUT + PPE
4. **Kalkulator ROI** - konkretne liczby zamiast ogólników
5. **Case studies** - prawdziwe przykłady do użycia w rozmowie

### Techniczne
1. **Modularna architektura** - łatwe dodawanie nowych aplikacji
2. **JSON data store** - nie wymaga bazy danych, łatwa edycja
3. **Singleton recommender** - performance (ładowanie danych raz)
4. **Session state management** - pełna nawigacja wstecz/restart
5. **Resource tagging** - integracja z company permission system

---

## 📊 Statystyki MVP

- **Aplikacje**: 3 (hydraulik, warsztat, serwis mobilny)
- **Produkty**: 26 (8 narzędzi, 4 baterie, 6 akcesoriów, 5 PACKOUT, 2 PPE, 3 bundle)
- **Pytania discovery**: 12 (4 per typ klienta)
- **Skrypty perswazyjne**: 3 pełne (problem → CTA)
- **Case studies**: 3 (po 1 na aplikację)
- **Linie kodu**: ~1500 (recommender + views)
- **Pliki JSON**: 3 (applications, products, questions)

---

## 🚀 Jak używać (Quick Start)

### Dla użytkownika Milwaukee:

1. **Login** jako użytkownik z company="Milwaukee"
2. **Menu** → �️ Narzędzia
3. **Tabs** → Przejdź do ostatniego taba: **🔴 Milwaukee**
4. **Krok 1**: Wybierz kontekst klienta (4 zmienne)
5. **Krok 2**: Zobacz dopasowane aplikacje → Wybierz jedną
6. **Krok 3**: Odpowiedz na pytania pogłębiające
7. **Krok 4**: Zobacz rekomendację:
   - Tab "Pakiet produktów" - co zaproponować
   - Tab "Skrypt perswazyjny" - jak sprzedać
   - Tab "Kalkulator ROI" - konkretne liczby
   - Tab "Case Studies" - prawdziwe przykłady
8. **Zapisz wizytę** (opcjonalnie)
9. **After Visit** - wypełnij po spotkaniu z klientem

### Dla admina:

1. **Dodawanie nowych aplikacji**: Edytuj `data/milwaukee/applications.json`
2. **Dodawanie produktów**: Edytuj `data/milwaukee/products_ecosystem.json`
3. **Dodawanie pytań**: Edytuj `data/milwaukee/discovery_questions.json`
4. **Analiza feedback**: Sprawdź `data/milwaukee/feedback/*.json`
5. **Analiza wizyt**: Sprawdź `data/milwaukee/visits/*.json`

---

## 🔄 Następne kroki (Roadmap)

### FAZA 2: Intelligence (sugerowane na weekend)
- [ ] AI Practice Mode - symulacja rozmowy z klientem (jak Business Games)
- [ ] Integracja z Google Generative AI - auto-generowanie skryptów
- [ ] OCR scoring - analiza odpowiedzi i ocena jakości discovery

### FAZA 3: PRO Features (przyszły tydzień)
- [ ] PDF export - gotowy dokument ofertowy
- [ ] Email integration - wysyłka oferty do klienta
- [ ] Analytics dashboard - statystyki użycia, top aplikacje, conversion rate
- [ ] Leaderboard - ranking najlepszych użytkowników (gamification)

### FAZA 4: Integracja biznesowa
- [ ] Synchronizacja z CRM
- [ ] Import danych klientów
- [ ] Automatyczne follow-up (reminders)
- [ ] Raportowanie dla managementu

---

## 🐛 Znane ograniczenia MVP

1. **Tylko 3 aplikacje** - docelowo 10-15
2. **Brak AI conversation** - planowane w FAZA 2
3. **Brak PDF export** - planowane w FAZA 3
4. **Brak synchronizacji z CRM** - planowane w FAZA 4
5. **Statyczne pytania discovery** - brak dynamicznego dostosowania

---

## 📝 Uwagi techniczne

### Wymagania:
- Python 3.8+
- Streamlit
- Permissions: company="Milwaukee" w user_data

### Struktura plików:
```
data/milwaukee/
├── applications.json          # 3 aplikacje
├── products_ecosystem.json    # 26 produktów
├── discovery_questions.json   # 12 pytań
├── visits/                    # Zapisane wizyty
└── feedback/                  # After visit feedback

utils/
└── milwaukee_recommender.py   # Logika dopasowania

views/
├── milwaukee_application_engine.py  # Main view
└── milwaukee_after_visit.py        # Feedback loop

config/
└── resource_tags.json         # tools_menu: milwaukee_app_engine
```

---

## ✅ MVP GOTOWE DO TESTOWANIA

**Status:** ✅ Wszystkie komponenty zaimplementowane i zintegrowane  
**Test:** Aplikacja uruchomiona na http://localhost:8502  
**Dostęp:** Tylko użytkownicy Milwaukee (resource tagging)  

**Potrzebne do testów produkcyjnych:**
1. Użytkownik testowy z company="Milwaukee"
2. 2-3 prawdziwe scenariusze klientów
3. Feedback od team Milwaukee po pierwszych wizytach

---

**Stworzył:** GitHub Copilot  
**Data:** 28 grudnia 2025  
**Wersja:** 1.0 MVP
