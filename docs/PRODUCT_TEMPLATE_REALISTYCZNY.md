# 📦 Szablon Produktu - Model Realistyczny (Dystrybucja przez Hurtownię)

## 🎯 Wprowadzenie

Ten szablon opisuje strukturę produktu FreshLife w **modelu realistycznym** dystrybucji przez hurtownie (Eurocash, Makro, FMCG24).

**Kluczowe zmiany vs model bezpośredni:**
- ❌ Brak marż konkurencji (sklep ich nie zna!)
- ✅ Dostępność w hurtowniach (SKU, MOQ)
- ✅ Rotacja jako kluczowy argument (marża × rotacja)
- ✅ Argumenty dostosowane do "pull strategy"
- ✅ Kontekst ekonomiczny (PLN zarobione/mies)

---

## ✅ Status Produktów

### Personal Care (3)
- [x] **pc_001** - BodyWash Natural ✅ GOTOWE (wzorzec)
- [ ] **pc_002** - SilkHair (szampony)
- [ ] **pc_003** - DeoActive (dezodoranty)

### Food (2)
- [ ] **food_001** - MorningJoy (płatki śniadaniowe)
- [ ] **food_002** - NutriBar (batony proteinowe)

### Home Care (3)
- [ ] **hc_001** - CleanWave (płyn do naczyń)
- [ ] **hc_002** - FreshAir (odświeżacz powietrza)
- [ ] **hc_003** - SparkleFloor (płyn do podłóg)

### Snacks (2)
- [ ] **snacks_001** - CrunchyNuts (orzeszki)
- [ ] **snacks_002** - ChipsNatural (chipsy ziemniaczane)

### Beverages (2)
- [ ] **bev_001** - FruitSplash (napój owocowy)
- [ ] **bev_002** - EnergyBoost (napój energetyczny)

---

## 📋 Kompletna Struktura

```python
"product_id": {
    # === PODSTAWOWE DANE ===
    "id": "product_id",
    "name": "Nazwa Produktu",
    "brand": "FreshLife",
    "category": "Personal Care",  # lub Food, Home Care, Snacks, Beverages
    "subcategory": "Szczegółowa kategoria",
    "emoji": "🧴",  # Wybierz unikalne emoji
    "variants": ["Wariant 1", "Wariant 2", "Wariant 3"],
    "base_variant": "Główny wariant z gramaturaą (np. Aloe & Green Tea 250ml)",
    
    # === PRICING - MODEL PRZEZ HURTOWNIĘ ===
    "price_retail": 12.99,  # Cena w sklepie dla klienta końcowego
    "price_wholesale_eurocash": 10.50,  # Cena hurtowni (Eurocash) dla sklepu
    "price_freshlife_to_eurocash": 7.50,  # Cena FreshLife dla hurtowni
    
    "margin_shop_percent": 19,  # Marża sklepu (kupuje od Eurocash, sprzedaje klientowi)
    "margin_shop_pln": 2.49,  # Ile zarabia sklep na 1 sztuce w PLN
    "margin_eurocash_percent": 40,  # Marża hurtowni
    "margin_freshlife_percent": 25,  # Marża producenta (COGS: 6.00 zł → sprzedaż: 7.50 zł)
    
    # === MODEL DYSTRYBUCJI ===
    "distribution_model": "wholesale",  # "wholesale" dla modelu realistycznego
    "available_at": ["Eurocash", "Makro Cash & Carry", "FMCG24"],
    "eurocash_sku": "FL-PC001-250",  # Kod produktu w systemie Eurocash
    
    # === ZAMAWIANIE ===
    "moq_freshlife": 6,  # MOQ bezpośrednio od FreshLife (dla testów)
    "moq_eurocash": 1,  # MOQ w Eurocash (sklepy mogą kupić nawet 1 szt)
    "payment_terms_eurocash": "Przelew 14 dni",
    "payment_terms_direct": "Przelew 14 dni lub gotówka",
    "delivery_free_threshold": 300,  # Darmowa dostawa bezpośrednia od X PLN
    
    # === LOGISTYKA I SHELF SPACE ===
    "shelf_space_cm": 15,  # Ile cm zajmuje na półce (ważne dla zastępowania)
    "case_size": 12,  # Ile sztuk w kartonie
    "cases_per_pallet": 80,
    "popularity": 72,  # 0-100 (symulacja popytu)
    "shelf_life_days": 1080,  # 3 lata
    "packaging": "Butelka PET z recyclingu 250ml, pompka",
    
    # === STORYTELLING ===
    "description": """
    2-4 zdania opisujące produkt:
    - Główne składniki/charakterystyka
    - Korzyści dla użytkownika
    - Co wyróżnia od konkurencji (skład, opakowanie, certyfikaty)
    - Dla kogo jest przeznaczony (krótko)
    
    Przykład: "Naturalny żel pod prysznic z ekstraktami z aloesu i zielonej herbaty. 
    Bez parabenów, SLS i barwników. Idealny dla skóry wrażliwej. 
    Piękne, ekologiczne opakowanie z recyclingu."
    """,
    
    "target_customer": """
    Szczegółowy profil klienta końcowego:
    - Demografia (wiek, płeć, status rodzinny)
    - Psychografia (wartości, styl życia, zachowania)
    - Potrzeby (problemy które rozwiązuje produkt)
    
    Przykład: "Kobiety 25-45 lat świadome składu, rodzice szukający bezpiecznych 
    produktów, osoby z wrażliwą skórą, ekologiczni konsumenci"
    """,
    
    "rotation_speed": "Szybka/Średnia/Wolna (X-Y dni przy Z szt) = N rotacji/mies",
    # Przykład: "Szybka (7-10 dni przy 10 szt) = 3-4 rotacje/mies"
    
    "rotation_speed_context": """
    Konkretne wyliczenie ekonomiczne pokazujące przewagę szybkiej rotacji:
    
    "Przy rotacji 3x/mies i marży 2.49 zł = 7.47 zł zysku/mies z 15 cm półki. 
    Dove rotuje 1x/mies przy marży 2.88 zł = 2.88 zł/mies."
    
    To pokazuje że MIMO niższej marży jednostkowej, szybsza rotacja = więcej zarobku!
    """,
    
    "suggested_initial_order": """
    "6-10 szt (pierwsze zamówienie testowe bezpośrednio od FreshLife), 
    potem przez Eurocash"
    
    Zawsze proponuj małe, testowe zamówienie bezpośrednie → redukcja ryzyka.
    """,
    
    # === KONKURENCJA (BEZ ICH MARŻ!) ===
    "competitors": [
        {
            "brand": "Nazwa Konkurenta #1",
            "price_retail": 15.99,  # Cena w sklepie (możemy sprawdzić)
            "price_wholesale_estimated": 13.11,  # Szacowana (nie znamy dokładnie!)
            "moq_estimated": 24,  # Szacowane MOQ (nie znamy dokładnie)
            "shelf_space_cm": 15,
            "rotation_estimated": "Wolna (30 dni)",  # Na podstawie obserwacji rynku
            "advantages": [
                "💰 Cena - ZAWSZE konkretna kwota: 'Tańszy dla klienta: 12.99 zł vs 15.99 zł (oszczędność 3 zł)'",
                "💵 Marża × Rotacja - kluczowy argument: 'Lepsza marża + 3x szybsza rotacja = 2.6x więcej zarobku miesięcznie'",
                "📦 MOQ - przewaga logistyczna: 'Może Pan zacząć od 6 szt (u nas) vs 24 szt Dove'",
                "♻️ Jakość/Skład - konkretne fakty: '97% naturalnych składników vs 85%'",
                "🌱 Trend - społeczny kontekst: 'Opakowanie z recyclingu - przyciąga ekologicznych klientów'"
            ]
        },
        {
            "brand": "Nazwa Konkurenta #2",
            "price_retail": 13.99,
            "price_wholesale_estimated": 11.19,
            "moq_estimated": 12,
            "shelf_space_cm": 15,
            "rotation_estimated": "Średnia (20 dni)",
            "advantages": [
                # Podobna struktura jak wyżej
                # Minimum 3-4 advantages z emoji
            ]
        }
    ],
    
    # === ARGUMENTY SPRZEDAŻOWE (Pull Strategy - przez hurtownię) ===
    "sales_arguments": [
        """
        📦 ARGUMENT #1 - Dostępność w hurtowni:
        
        "Nasz produkt jest dostępny w Eurocash pod kodem FL-PC001-250. 
        Może Pan zamówić przez swoje konto online lub zadzwonić do przedstawiciela. 
        Cena 10.50 zł, sprzeda Pan za 12.99 - to 2.49 zł na sztuce."
        
        Struktura:
        - Gdzie dostępny (hurtownia + SKU)
        - Jak zamówić (konto online/telefon)
        - Ekonomika (cena zakupu → cena sprzedaży → marża)
        """,
        
        """
        🔄 ARGUMENT #2 - Rotacja i ekonomika (NAJWAŻNIEJSZY!):
        
        "Kluczowa sprawa: nasz produkt rotuje w 7-10 dni, Dove w 30. 
        To oznacza że zarobi Pan WIĘCEJ mimo niższej marży jednostkowej: 
        3 rotacje/mies x 2.49 zł = 7.47 zł vs 1 rotacja Dove x 2.88 zł = 2.88 zł."
        
        Struktura:
        - Porównanie rotacji (nasze X dni vs konkurent Y dni)
        - Konkretne wyliczenie (rotacje × marża = zarobek/mies)
        - Wniosek (więcej mimo niższej marży jednostkowej)
        """,
        
        """
        💡 ARGUMENT #3 - Testowe zamówienie (redukcja ryzyka):
        
        "Może Pan zacząć testowo - zamówię bezpośrednio 6 sztuk. 
        Jeśli się sprawdzi (a zazwyczaj tak jest), będzie Pan zamawiał przez Eurocash. 
        Małe ryzyko, duży potencjał."
        
        Struktura:
        - Propozycja małego zamówienia (6-10 szt bezpośrednio)
        - Jeśli się sprawdzi → potem Eurocash
        - Frame: małe ryzyko, duży potencjał
        """,
        
        """
        🛒 ARGUMENT #4 - Cena dla konsumenta:
        
        "Klienci szukają oszczędności: 12.99 zł zamiast 15.99 za Dove to argument, który działa. 
        Szczególnie w małych sklepach, gdzie klient liczy każdą złotówkę."
        
        Struktura:
        - Konkretna oszczędność dla klienta końcowego
        - Kontekst (małe sklepy = klienci wrażliwi na cenę)
        - Korzyść dla sklepu (przyciąga klientów)
        """,
        
        """
        ♻️ ARGUMENT #5 - Trend/USP:
        
        "Naturalny skład i ekologiczne opakowanie - to trend! 
        Młodsi klienci (25-40 lat) coraz częściej patrzą na skład i pochodzenie opakowania."
        
        Struktura:
        - Unikalna cecha produktu (naturalność, ekologia, certyfikat)
        - Social proof / trend rynkowy
        - Grupa docelowa która to docenia
        """
    ],
    
    # === PODSUMOWANIE ===
    "usp": "1 zdanie - główna przewaga konkurencyjna",
    "awards": [],  # Lista nagród lub pusta
    "promo_support": True,
    "pos_materials": ["Wobbler", "Shelf strip", "Tester", "Ulotka składnikowa"],
}
```

---

## 🎓 Kluczowe Zasady Modelu Realistycznego

### 1. ❌ NIE podajemy marż konkurencji
**Dlaczego?** Sklep ich nie zna! Handlowiec FreshLife też nie zna dokładnych umów konkurencji z hurtowniami.

**Co MOŻEMY podać:**
- ✅ Cena detaliczna (widzimy w sklepie)
- ✅ Szacowana cena hurtowa (można wywnioskować z marży ~20-25% dla sklepów)
- ✅ Szacowane MOQ (obserwacje rynku, doświadczenie)
- ✅ Szacowana rotacja (obserwacje, dane Nielsen)

### 2. 🔄 Rotacja jako główny argument
W kanale tradycyjnym **rotacja ważniejsza niż marża %**.

**Dlaczego?** 
- Sklep ma ograniczony kapitał (5,000-20,000 zł/mies)
- Shelf space ograniczone (każdy cm się liczy)
- Wolne produkty zamrażają kapitał

**Jak pokazać:**
```
Marża × Rotacje/mies = Zarobek miesięczny z X cm półki

Przykład:
- Produkt A: 2.49 zł × 3 rotacje = 7.47 zł/mies (15 cm)
- Produkt B: 2.88 zł × 1 rotacja = 2.88 zł/mies (15 cm)

→ Produkt A lepszy! (mimo niższej marży jednostkowej)
```

### 3. 📦 Pull Strategy (budowanie popytu)
Handlowiec FreshLife **nie bierze zamówienia bezpośrednio** (w modelu przez hurtownię).

**Rola handlowca:**
1. Prezentuje produkt w sklepie
2. Przekonuje właściciela o zaletach
3. Informuje o dostępności w Eurocash (SKU)
4. Oferuje małe zamówienie testowe (bezpośrednio od FreshLife)
5. Wspiera merchandisingiem i POS

**Sklep zamawia sam** przez Eurocash (online/telefon).

### 4. 💰 Mów o PLN, nie o %
**Złe:** "Marża 19%"  
**Dobre:** "Zarobi Pan 2.49 zł na sztuce"

**Złe:** "Rotacja 3x/mies"  
**Dobre:** "W miesiącu zarobi Pan 7.47 zł z 15 cm półki"

### 5. 🎯 Kontekst ekonomiczny
Każdy argument powinien mieć **konkretne liczby** i **kontekst**.

**Przykłady:**
- "3 zł oszczędności" (nie "19% taniej")
- "6 sztuk vs 24 sztuki Dove" (nie "niższe MOQ")
- "7.47 zł/mies vs 2.88 zł/mies" (nie "lepsza rotacja")

---

## 🛠️ Implementacja Krok po Kroku

### Krok 1: Wybierz produkt
Np. `pc_002` - SilkHair (szampon)

### Krok 2: Ustal pricing (model przez hurtownię)
```python
# Załóżmy COGS = 8.00 zł
"price_freshlife_to_eurocash": 10.00,  # Margin 25%
"price_wholesale_eurocash": 14.00,     # Margin Eurocash 40%
"price_retail": 18.00,                  # Margin sklepu 22%
"margin_shop_pln": 4.00,
"margin_shop_percent": 22,
```

### Krok 3: Zidentyfikuj 2-3 głównych konkurentów
**Dla szamponu:**
- Dove Intensive Repair (~19.99 zł)
- Pantene Pro-V (~16.99 zł)
- Head & Shoulders (~15.99 zł)

### Krok 4: Szacuj ich parametry
```python
"competitors": [
    {
        "brand": "Dove Intensive Repair",
        "price_retail": 19.99,
        "price_wholesale_estimated": 15.99,  # ~20% margin sklepu
        "moq_estimated": 24,
        "shelf_space_cm": 12,
        "rotation_estimated": "Średnia (20 dni)",
        "advantages": [...]
    }
]
```

### Krok 5: Stwórz storytelling
- **Description:** Skład, korzyści, dla kogo
- **Target customer:** Demografia + psychografia
- **Rotation speed:** Konkretne dni + liczba rotacji
- **Rotation context:** Ekonomika (PLN/mies)

### Krok 6: Napisz 5 argumentów sprzedażowych
Według szablonu wyżej:
1. Dostępność w hurtowni
2. Rotacja i ekonomika
3. Testowe zamówienie
4. Cena dla konsumenta
5. Trend/USP

### Krok 7: Sprawdź kompletność
- [ ] Wszystkie pola wypełnione
- [ ] 2-3 konkurentów z advantages
- [ ] 5 sales arguments
- [ ] Konkretne liczby (PLN, dni, %)
- [ ] Emoji i USP

---

## 📚 Dodatkowe Zasoby

- **Artykuł edukacyjny:** `docs/TRADYCYJNY_KANAL_DYSTRYBUCJI.md`
- **Wzorzec produktu:** `fmcg_products.py` → `pc_001`
- **Game concept:** `FMCG_GAME_CONCEPT.md`

---

**Autor:** BVA Educational Materials  
**Data:** 2025-10-30  
**Wersja:** 1.0 (Model Realistyczny)
