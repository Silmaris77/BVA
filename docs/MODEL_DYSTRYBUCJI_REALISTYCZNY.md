# 📊 FMCG Simulator - Model Dystrybucji (Wersja Realistyczna)

## 🎯 Cel Dokumentu
Ten dokument opisuje **model dystrybucji** zastosowany w FMCG Sales Simulator - wersja **realistyczna**, odzwierciedlająca rzeczywisty rynek polski.

---

## 🏭 Model 2-Poziomowy (Przez Hurtownię)

### Schemat Przepływu
```
┌──────────────────────────┐
│ FreshLife (Producent)    │
│ - Produkuje 12 produktów │
│ - Marża: 25%             │
└──────────┬───────────────┘
           │ Sprzedaż hurtowa
           │ Cena: 7.50 zł
           ↓
┌──────────────────────────────┐
│ Eurocash / Makro / FMCG24    │
│ (Hurtownia)                  │
│ - Marża: 30-40%              │
└──────────┬───────────────────┘
           │ Sklep zamawia
           │ Cena: 10.50 zł
           ↓
┌──────────────────────────────┐
│ Sklep Osiedlowy              │
│ (Detal)                      │
│ - Marża: 18-25%              │
└──────────┬───────────────────┘
           │ Sprzedaż detaliczna
           │ Cena: 12.99 zł
           ↓
┌──────────────────────────────┐
│ Klient Końcowy               │
└──────────────────────────────┘
```

---

## 💰 Przykład Cenowy: BodyWash Natural

| Poziom | Cena | Marża | Marża PLN |
|--------|------|-------|-----------|
| **COGS** (koszt produkcji) | 6.00 zł | - | - |
| **FreshLife → Hurtownia** | 7.50 zł | 25% | 1.50 zł |
| **Hurtownia → Sklep** | 10.50 zł | 40% | 3.00 zł |
| **Sklep → Klient** | 12.99 zł | 19% | 2.49 zł |

**Końcowy efekt:**
- Klient płaci: **12.99 zł**
- Sklep zarabia: **2.49 zł/szt** (przy zamówieniu z Eurocash)
- Hurtownia zarabia: **3.00 zł/szt**
- FreshLife zarabia: **1.50 zł/szt**

---

## 👔 Rola Handlowca FreshLife (Pull Strategy)

### ✅ Co ROBI handlowiec:

1. **Prezentacja produktów** w sklepach
   - Pokazuje produkty FreshLife
   - Edukuje o zaletach (cena, marża, rotacja)
   - Demonstracje, testery

2. **Budowanie "pull" (popytu)**
   - Przekonuje właściciela sklepu
   - Pokazuje konkretną ekonomikę (PLN zarobione/mies)
   - Porównuje z konkurencją

3. **Informuje o dostępności w hurtowni**
   - "Produkt dostępny w Eurocash pod kodem FL-PC001-250"
   - "Może Pan zamówić przez swoje konto online"

4. **Oferuje testowe zamówienie**
   - Małe zamówienie bezpośrednio od FreshLife (6-10 szt)
   - Redukcja ryzyka dla sklepu
   - Jeśli się sprawdzi → sklep zamawia przez Eurocash

5. **Merchandising i POS**
   - Układa produkty na półce
   - Dostarcza wobblery, shelf stripy, testery
   - Sprawdza dostępność (facing, rotacja)

### ❌ Czego NIE ROBI handlowiec:

1. ❌ **NIE bierze zamówienia** (w standardowym modelu)
   - Sklep zamawia **SAM** przez Eurocash

2. ❌ **NIE organizuje dostawy**
   - Hurtownia dostarcza do sklepu

3. ❌ **NIE rozlicza płatności**
   - Sklep płaci hurtowni (nie FreshLife)

4. ❌ **NIE zna marż konkurencji**
   - Sklep nie dzieli się danymi
   - FreshLife nie ma dostępu do umów konkurentów

### Jak sklep zamawia produkty FreshLife?

```
Krok 1: Handlowiec przekonał właściciela
        ↓
Krok 2: Właściciel loguje się do konta Eurocash
        (online lub dzwoni do przedstawiciela)
        ↓
Krok 3: Zamawia FL-PC001-250 (BodyWash Natural)
        Ilość: dowolna (MOQ = 1 szt w Eurocash)
        ↓
Krok 4: Eurocash dostarcza następnego dnia
        ↓
Krok 5: Sklep płaci Eurocash (przelew 7-14 dni)
```

**Rola handlowca:** Wraca za tydzień, sprawdza czy produkt jest na półce, pomaga w merchandisingu.

---

## 📦 Ekonomika Sklepu - Kluczowe Koncepty

### 1. Marża × Rotacja = Zarobek/mies

**To NAJWAŻNIEJSZY argument w kanale tradycyjnym!**

Sklep woli produkt który:
- Szybko rotuje (3-4x/mies)
- Zajmuje mało miejsca
- Nie zamraża kapitału

**Przykład:**

| Produkt | Marża/szt | Rotacja/mies | Shelf Space | Zarobek/mies |
|---------|-----------|--------------|-------------|--------------|
| **FreshLife BodyWash** | 2.49 zł | 3x | 15 cm | **7.47 zł** |
| **Dove Natural** | 2.88 zł | 1x | 15 cm | **2.88 zł** |

**Wniosek:** FreshLife lepszy mimo niższej marży jednostkowej!

### 2. MOQ (Minimum Order Quantity)

**Dlaczego to ważne?**
- Mały sklep ma ograniczony kapitał (5,000-20,000 zł/mies)
- Każda złotówka zamrożona w towarze = brak elastyczności

**Porównanie:**
- FreshLife BodyWash: **6 szt** (testowo bezpośrednio) lub **1 szt** (Eurocash)
- Dove Natural: **24 szt** (typowe MOQ dla korporacji)

**Argument:**
> "Może Pan zacząć od 6 sztuk - to tylko 63 zł. Dove wymaga zamówienia 24 sztuk za 336 zł. Nie zamraża Pan kapitału."

### 3. Shelf Space (Miejsce na Półce)

**Problem:** Sklep ma ograniczoną przestrzeń. Każdy nowy produkt = coś musi zejść.

**Argument:**
> "Nasz produkt zajmuje 15 cm półki, podobnie jak Dove. Może go zastąpić 1:1, a Pan zarobi więcej miesięcznie."

### 4. Kapitał Obrotowy

Mały sklep żyje z przepływu gotówki. Wolno rotujące produkty = zamrożony kapitał = problem.

**Argument:**
> "Nasz produkt sprzedaje się w 7-10 dni. Kupi Pan 10 sztuk za 105 zł, sprzeda Pan w 10 dni za 130 zł. To 25 zł zysku w tydzień, 100 zł/mies."

---

## 🎯 Kluczowe Argumenty Sprzedażowe (Pull Strategy)

### Argument #1: Dostępność w hurtowni
```
"Nasz produkt jest dostępny w Eurocash pod kodem FL-PC001-250. 
Może Pan zamówić przez swoje konto online lub zadzwonić do 
przedstawiciela. Cena 10.50 zł, sprzeda Pan za 12.99 - to 2.49 zł 
na sztuce."
```

**Dlaczego to działa:**
- Sklep już ma konto w Eurocash → łatwy zakup
- Nie musi płacić od razu (kredyt 14 dni)
- Może zamówić nawet 1 szt (test)

---

### Argument #2: Rotacja i ekonomika
```
"Kluczowa sprawa: nasz produkt rotuje w 7-10 dni, Dove w 30. 
To oznacza że zarobi Pan WIĘCEJ mimo niższej marży jednostkowej: 
3 rotacje/mies x 2.49 zł = 7.47 zł vs 1 rotacja Dove x 2.88 zł = 2.88 zł."
```

**Dlaczego to działa:**
- Konkretne liczby (PLN, nie %)
- Porównanie z znaną marką
- Kontekst ekonomiczny (zarobek/mies)

---

### Argument #3: Testowe zamówienie
```
"Może Pan zacząć testowo - zamówię bezpośrednio 6 sztuk. 
Jeśli się sprawdzi (a zazwyczaj tak jest), będzie Pan zamawiał 
przez Eurocash. Małe ryzyko, duży potencjał."
```

**Dlaczego to działa:**
- Redukcja ryzyka (tylko 6 szt)
- Elastyczność (test przed commitment)
- Wsparcie handlowca (nie jest sam)

---

### Argument #4: Cena dla konsumenta
```
"Klienci szukają oszczędności: 12.99 zł zamiast 15.99 za Dove 
to argument, który działa. Szczególnie w małych sklepach, gdzie 
klient liczy każdą złotówkę."
```

**Dlaczego to działa:**
- Kanał tradycyjny = klienci wrażliwi na cenę
- 3 zł oszczędności = znacząca kwota
- Sklep przyciąga klientów niższą ceną

---

### Argument #5: Trend/USP
```
"Naturalny skład i ekologiczne opakowanie - to trend! 
Młodsi klienci (25-40 lat) coraz częściej patrzą na skład 
i pochodzenie opakowania."
```

**Dlaczego to działa:**
- Social proof (trend rynkowy)
- Differentiation (97% naturalnych składników)
- Target grupa (świadomi konsumenci)

---

## ❌ Czego NIE Mówić (Nierealistyczne)

### 1. NIE podawaj marż konkurencji
**Złe:** "Dove ma marżę 18%, my 19%"  
**Dobre:** "Na naszym produkcie zarobi Pan 2.49 zł, na Dove ~2.88 zł, ALE my rotujemy 3x szybciej"

**Dlaczego?** Sklep nie zna dokładnych marż konkurencji. Handlowiec FreshLife też nie.

---

### 2. NIE mów tylko o marży %
**Złe:** "Mamy świetną marżę 19%"  
**Dobre:** "Zarobi Pan 2.49 zł na sztuce, przy 10 sztkach tygodniowo to 100 zł/mies"

**Dlaczego?** Sklep myśli w PLN, nie w %. Konkretne kwoty są bardziej przekonujące.

---

### 3. NIE obiecuj dostawy (jeśli model przez hurtownię)
**Złe:** "Dostarczę Panu towar w czwartek"  
**Dobre:** "Może Pan zamówić dziś przez Eurocash, dostawa jutro. Wrócę w piątek pomóc z wystawieniem"

**Dlaczego?** W modelu przez hurtownię handlowiec nie organizuje dostaw.

---

## 📚 Materiały Edukacyjne

### Dla graczy:
- **Artykuł:** `docs/TRADYCYJNY_KANAL_DYSTRYBUCJI.md` (pełny przewodnik)
- **Tab: Inspiracje** w grze (dostęp do artykułów)
- **Szczegóły produktów** w Tab: Produkty (argumenty gotowe do użycia)

### Dla deweloperów:
- **Template produktu:** `docs/PRODUCT_TEMPLATE_REALISTYCZNY.md`
- **Struktura danych:** `data/industries/fmcg_data_schema.py`
- **Wzorcowy produkt:** `pc_001` w `fmcg_products.py`

---

## 🎮 Jak To Działa w Grze?

### 1. Gracz wybiera klienta do wizyty
UI pokazuje:
- Dystans (koszt energii)
- Status (PROSPECT/ACTIVE/LOST)
- Reputacja (0-100)
- Poziom znajomości (⭐⭐⭐☆☆)

### 2. Przed wizytą - przygotowanie
- Przegląda profil klienta (odkryte informacje)
- Sprawdza produkty (szczegóły, argumenty)
- Planuje strategię

### 3. Podczas wizyty - rozmowa AI
- Konwersacja z AI (Gemini 2.0 Flash)
- AI gra rolę właściciela (osobowość, priorytety)
- Gracz prezentuje produkty, używa argumentów
- AI pamięta kontekst, historię wizyt

### 4. Zamówienie (lub nie)
- **Model przez hurtownię:** Gracz NIE bierze zamówienia
- Ale może zaproponować testowe zamówienie bezpośrednie (6-10 szt)
- Lub przekonuje właściciela do zamówienia przez Eurocash

### 5. Po wizycie - feedback
- AI ocenia rozmowę (1-5⭐)
- Ekstrakcja odkrytych informacji (Client Discovery)
- Popup "Nowe odkrycia!" jeśli coś odkryto
- Aktualizacja poziomu znajomości
- Opcjonalnie: Feedback FUKO od menedżera

---

## 🎯 Korzyści Modelu Realistycznego

### Dla edukacji (studenci BVA):
✅ Uczy **prawdziwego** modelu dystrybucji w Polsce  
✅ Pokazuje różnicę między pull strategy (hurtownia) a direct sales  
✅ Trenuje argumenty ekonomiczne (rotacja, MOQ, kapitał)  
✅ Buduje zrozumienie całego łańcucha wartości  

### Dla partnerów biznesowych (testerzy):
✅ Realistyczny model → większa wiarygodność  
✅ Możliwość testowania własnych produktów w grze  
✅ Symulacja prawdziwych wyzwań kanału tradycyjnego  

### Dla rozgrywki:
✅ Większa głębia strategiczna  
✅ Różnorodność argumentów (nie tylko cena/marża)  
✅ Realistyczne wyzwania (shelf space, kapitał obrotowy)  

---

**Autor:** BVA Educational Materials  
**Data:** 2025-10-30  
**Wersja:** 1.0 (Model Realistyczny - Przez Hurtownię)  
**Powiązane dokumenty:**
- `FMCG_GAME_CONCEPT.md` - główny koncept gry
- `TRADYCYJNY_KANAL_DYSTRYBUCJI.md` - artykuł edukacyjny
- `PRODUCT_TEMPLATE_REALISTYCZNY.md` - szablon produktów
