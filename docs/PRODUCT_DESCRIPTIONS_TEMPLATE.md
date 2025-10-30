# Template Opisu Produktu FreshLife

## Struktura Rozszerzonego Opisu

Każdy z 12 produktów FreshLife powinien zawierać:

### 1. Podstawowe Dane (istniejące)
```python
"id": "pc_001",
"name": "Nazwa Produktu",
"brand": "FreshLife",
"category": "Personal Care",  # lub Food, Home Care, Snacks, Beverages
"subcategory": "Kategoria szczegółowa",
"emoji": "🧴",  # NOWE - emoji dla kategorii
"price_retail": 12.99,
"price_wholesale": 8.44,
"margin_percent": 35,
"margin_pln": 4.55,  # NOWE - marża w PLN
"moq": 6,
"popularity": 72,
```

### 2. Storytelling (NOWE)
```python
"description": "Pełny opis produktu - skład, korzyści, USP. 2-3 zdania.",
"target_customer": "Dla kogo ten produkt - demografia, potrzeby, styl życia",
"rotation_speed": "Szybka/Średnia/Wolna (X dni przy Y szt)",
"suggested_initial_order": "6-10 szt",
```

### 3. Przewagi nad Konkurencją (NOWE)
```python
"competitors": [
    {
        "brand": "Nazwa Marki Konkurencji",
        "price": 15.99,
        "margin_percent": 18,
        "advantages": [
            "Tańszy o X zł",
            "Lepsza marża: X% vs Y%",
            "Dodatkowa przewaga (skład/opakowanie/rozmiar)"
        ]
    },
    # 2-3 głównych konkurentów
],
```

### 4. Argumenty Sprzedażowe (NOWE)
```python
"sales_arguments": [
    "Gotowe zdanie #1 - porównanie z konkurencją (cena + marża)",
    "Gotowe zdanie #2 - korzyść dla klienta końcowego",
    "Gotowe zdanie #3 - unikalny benefit (trend/ekologia/jakość)"
],
```

## Przykład - BodyWash Natural

Zobacz `fmcg_products.py` - produkt `pc_001` jako wzorzec.

## Lista 12 Produktów FreshLife do Uzupełnienia

### Personal Care (3)
1. ✅ `pc_001` - BodyWash Natural - **GOTOWE**
2. ⏳ `pc_002` - Szampon (do aktualizacji)
3. ⏳ `pc_003` - Dezodorant (do aktualizacji)

### Food (2)
4. ⏳ `food_001` - Płatki śniadaniowe (do aktualizacji)
5. ⏳ `food_002` - Zupa instant (do aktualizacji)

### Home Care (3)
6. ⏳ `hc_001` - Płyn do mycia naczyń (do aktualizacji)
7. ⏳ `hc_002` - Uniwersalny środek czystości (do aktualizacji)
8. ⏳ `hc_003` - Proszek do prania (do aktualizacji)

### Snacks (2)
9. ⏳ `snacks_001` - Chipsy (do aktualizacji)
10. ⏳ `snacks_002` - Batony zbożowe (do aktualizacji)

### Beverages (2)
11. ⏳ `bev_001` - Sok owocowy (do aktualizacji)
12. ⏳ `bev_002` - Napój gazowany (do aktualizacji)

## Wskazówki przy Tworzeniu Opisów

### Konkurencja do porównania
- **Personal Care:** Dove, Fa, Palmolive, Nivea
- **Food:** Nestlé, Danone, Knorr, Winiary
- **Home Care:** Ludwik, Domestos, Persil, Ariel
- **Snacks:** Lay's, Grześki, Prince Polo, Corny
- **Beverages:** Tymbark, Kubuś, Coca-Cola, Pepsi

### Typowe przewagi FreshLife:
- Cena niższa o 10-20% od lidera rynku
- Marża wyższa o 10-20 punktów procentowych
- Naturalniejszy skład / mniej chemii
- Ekologiczne opakowanie
- Polski producent (lokalność)
- Wsparcie POS (materiały, promocje)

### Marże typowe dla kategorii:
- **Personal Care:** 30-40%
- **Food:** 25-35%
- **Home Care:** 28-38%
- **Snacks:** 30-40%
- **Beverages:** 25-35%

## Implementacja w UI

Po uzupełnieniu wszystkich 12 produktów, UI pokaże:

**Tab: Produkty**
- Przycisk "ℹ️ Szczegóły" na każdej karcie produktu
- Modal z:
  - Pełny opis + target customer
  - Tabela porównawcza z konkurencją
  - Lista gotowych argumentów sprzedażowych
  - Przycisk "📋 Kopiuj argumenty"

**Tab: Rozmowa**
- Quick reference panel z produktami
- Sugestie AI: "Klient wspomniał o X - pokaż produkt Y"
- Możliwość podglądnięcia argumentów bez opuszczania czatu

---

**Status:** Produkt pc_001 (BodyWash Natural) gotowy jako wzorzec.
**Następny krok:** Aktualizacja pozostałych 11 produktów według tego template.
