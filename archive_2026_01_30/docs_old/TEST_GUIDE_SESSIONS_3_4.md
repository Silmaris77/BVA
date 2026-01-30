# 🎮 Przewodnik Testowy - Sessions 3 & 4
## Visit Recording + Contract Signing

### 📋 Przygotowanie (2 min)

1. **Uruchom aplikację** (jeśli nie działa):
   ```
   streamlit run main.py
   ```

2. **Zaloguj się jako Basia**

3. **Przejdź do Business Games → FMCG Simulator**

---

### 🎯 Test Scenariusz - Od PROSPECT do ACTIVE

#### **Krok 1: Wybierz klienta PROSPECT** (1 min)

1. Kliknij tab **"👥 Klienci"**
2. Rozwiń expander **"🎯 Potencjalni (5)"**
3. Znajdź klienta z niską reputacją (np. "Sklep 'U Danusi'" z -75)
4. Kliknij **"📋 SZCZEGÓŁY"**
5. **Sprawdź:**
   - Status badge: 🎯 PROSPECT (niebieski)
   - Reputacja: 💀 LOST (-75) z czerwonym paskiem
   - Wizyty: "Brak historii wizyt"
   - Portfolio: "Brak produktów - podpisz pierwszy kontrakt!"

#### **Krok 2: Przeprowadź rozmowę AI** (5 min)

1. Wróć do listy (przycisk ⬅️)
2. Kliknij tab **"💬 Rozmowa"**
3. Wybierz tego samego klienta z listy
4. Sprawdź koszty wizyty (dojazd, energia)
5. Kliknij **"🚀 Rozpocznij rozmowę"**
6. **Prowadź rozmowę:**
   - Przywitaj się i przedstaw
   - Zapytaj o potrzeby sklepu
   - Zaproponuj produkty FreshLife (np. cola, energy drink, chipsy)
   - Odpowiedz na pytania klienta
   - Zakończ profesjonalnie
7. Kliknij **"✅ Zakończ rozmowę"**

#### **Krok 3: Sprawdź ocenę (Session 3)** (2 min)

**Powinno się pokazać:**
- 📊 Ocena rozmowy:
  - Jakość: ⭐⭐⭐⭐ lub ⭐⭐⭐⭐⭐ (4-5 gwiazdek)
  - Zamówienie: wartość + status
  - Reputacja: 📈 +5 lub +10

- 📊 Podsumowanie wizyty:
  - Jakość rozmowy: ⭐⭐⭐⭐ (4/5)
  - Łączna liczba wizyt: 1
  - Aktualna reputacja: np. -70 lub -65 (wzrost!)

**✅ Session 3 TEST:**
- [ ] Wizyta zapisana do historii
- [ ] Reputacja wzrosła
- [ ] Licznik wizyt: 1

#### **Krok 4: Podpisz kontrakt (Session 4)** (3 min)

**Jeśli jakość >= 4, powinien pokazać się:**

```
🎉 Świetna rozmowa! Klient gotowy do podpisania kontraktu!

📝 Podpisz kontrakt - wybierz produkty do portfolio
```

1. Rozwiń expander z produktami
2. **Wybierz 3-4 produkty** (zaznacz checkboxy):
   - Np. FreshLife Cola 250ml
   - FreshLife Energy Drink 250ml
   - FreshLife Chipsy Paprykowe
   - FreshLife Woda Gazowana 500ml

3. Kliknij **"✍️ PODPISZ KONTRAKT"**

**Powinno się pokazać:**
- 🎈 Balloons animation
- ✅ Komunikaty:
  - "Kontrakt podpisany! Status: PROSPECT → ACTIVE"
  - "Bonus reputacji: +20 (nowa: np. -50)"
  - "Produkty w portfolio: 4"
- Auto-refresh po 3 sekundach

**✅ Session 4 TEST:**
- [ ] Status zmieniony na ACTIVE
- [ ] Reputacja wzrosła o +20
- [ ] Produkty dodane do portfolio

#### **Krok 5: Weryfikacja na karcie klienta** (2 min)

1. Po odświeżeniu kliknij tab **"👥 Klienci"**
2. Znajdź klienta teraz w **"✅ Aktywni (1)"** (przeniósł się!)
3. Kliknij **"📋 SZCZEGÓŁY"**

**Sprawdź kartę klienta:**

- **Header:**
  - Status badge: ✅ ACTIVE (zielony gradient)
  - Nazwa i lokalizacja

- **Reputacja:**
  - Emoji i status: np. ⚠️ AT RISK lub 😐 NEUTRAL
  - Pasek kolorowy: pomarańczowy/żółty (nie czerwony!)
  - Wartość: np. -50 (było -75, +5 wizyta +20 kontrakt)

- **Wizyty:**
  - "Ostatnia wizyta: Dzisiaj (2025-10-29)"
  - "✅ Wizyta na czas!"

- **Portfolio Produktów:**
  - Tabela z 3-4 produktami
  - Każdy: 50 szt/mies
  - Przycisk "+ Dodaj produkt" (cross-sell)

- **Historia Wydarzeń:**
  - Timeline z 5-7 wpisami:
    - 📝 Kontrakt podpisany (+20 rep)
    - 🌟 Dodano produkty (+15 rep każdy)
    - 🎯 Pierwsza wizyta (0 rep)
    - Wizyta regularna (+5 rep)

**✅ FINAL CHECK:**
- [ ] Klient widoczny w "Aktywni"
- [ ] Reputacja wzrosła łącznie o ~+80 (-75 → ok. -50 do 0)
- [ ] Portfolio zawiera wybrane produkty
- [ ] Timeline pokazuje wszystkie wydarzenia
- [ ] Daty wizyt i kontraktu prawidłowe

---

### 🎉 SUCCESS CRITERIA

**Session 3 - Visit Recording:**
✅ Wizyta zapisana w `visits_history`
✅ Wydarzenia w `events_timeline`
✅ Reputacja zaktualizowana
✅ UI pokazuje podsumowanie

**Session 4 - Contract Signing:**
✅ Status: PROSPECT → ACTIVE
✅ Bonus +20 reputacji
✅ Produkty w portfolio (3-4 szt)
✅ Daty kontraktu ustawione
✅ Event `contract_signed` w timeline

**Integracja:**
✅ Pełny flow: wizyta → ocena → kontrakt → aktywacja
✅ Dane spójne na karcie klienta
✅ UI responsywny i czytelny

---

### 🐛 Co sprawdzić jeśli coś nie działa:

**Problem:** Nie pokazuje się opcja podpisania kontraktu
- Sprawdź jakość rozmowy (musi być >= 4)
- Sprawdź status klienta (musi być PROSPECT)

**Problem:** Produkty mają 0 volume
- Bug naprawiony - powinno być 50 szt/mies

**Problem:** Reputacja nie wzrosła
- Sprawdź `events_timeline` - czy są wydarzenia
- Każde dodanie produktu daje +15, kontrakt +20

**Problem:** Klient nie przeniósł się do "Aktywni"
- Sprawdź czy status faktycznie zmienił się na "active"
- Odśwież stronę (F5)

---

### 📸 Screenshot Checklist

Jeśli chcesz pokazać wyniki, zrób screeny:
1. Karta klienta PRZED (PROSPECT, -75 rep, brak portfolio)
2. Ocena rozmowy (4-5 gwiazdek)
3. Opcja podpisania kontraktu (expander z produktami)
4. Komunikat sukcesu (balloons + status change)
5. Karta klienta PO (ACTIVE, wyższa rep, portfolio z produktami)
6. Timeline wydarzeń (wszystkie eventy)

---

**READY TO TEST!** 🚀

Powodzenia! Jeśli wszystko działa - będziemy mieli w pełni funkcjonalny system zarządzania klientami!
