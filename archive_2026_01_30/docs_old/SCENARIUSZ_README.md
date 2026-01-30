# 🎯 Prosty Scenariusz Wizyty Handlowej - Heinz

## 📋 Opis

Najprostszy możliwy scenariusz symulacji rozmowy handlowej w food service.

### Cel
Przekonaj właściciela bistro "U Michała" do testowego zamówienia **Heinz Ketchup Premium 5kg**.

## 🎮 Jak używać

### 1. Uruchom aplikację
```bash
streamlit run app.py
```

### 2. Przejdź do gry FMCG
- Wybierz **Business Games → FMCG**

### 3. Otwórz tab "Scenariusz"
- Kliknij **🎮 Scenariusz** w górnym menu

### 4. Rozpocznij wizytę
- Przeczytaj informacje o kliencie
- Kliknij **🚀 Rozpocznij rozmowę**

### 5. Prowadź dialog
- AI wciela się w Michała Kowalskiego (właściciela bistro)
- Wpisuj co chcesz powiedzieć
- Klient naturalnie odpowiada

### 6. Zakończ i otrzymaj feedback
- Kliknij **🏁 Zakończ wizytę**
- AI oceni Twoją rozmowę (0-100 pkt)
- Otrzymasz szczegółowy feedback w formacie FUKO

## 👨‍🍳 Profil klienta

**Michał Kowalski** - właściciel Bistro U Michała
- **Typ:** Pragmatyczny, oszczędny
- **Obecny dostawca:** Pudliszki (zadowolenie 7/10)
- **Zużycie:** ~8 kg ketchupu miesięcznie
- **Problem:** Klienci pytają o Heinz
- **Budżet:** ~500 PLN na testy

### Co go przekonuje:
✅ Konkretna korzyść finansowa (marża)  
✅ Dowód że klienci preferują Heinz  
✅ Gwarancja jakości  
✅ Łatwa dostępność/dostawa  

## 📊 Kryteria oceny

Rozmowa jest oceniana w 4 obszarach (każdy 0-25 pkt):

1. **Budowanie Relacji** (0-25)
   - Czy budowałeś rapport i zaufanie?
   - Czy byłeś profesjonalny i uprzejmy?

2. **Odkrywanie Potrzeb** (0-25)
   - Czy zadawałeś pytania odkrywające?
   - Czy słuchałeś odpowiedzi klienta?

3. **Dopasowanie Argumentów** (0-25)
   - Czy argumenty trafiały w potrzeby klienta?
   - Czy odwoływałeś się do jego sytuacji?

4. **Zamknięcie** (0-25)
   - Czy próbowałeś doprowadzić do decyzji?
   - Czy ustalono kolejne kroki?

## 🎓 Tips

### ✅ Dobre praktyki:
- Zacznij od pytań (odkrywaj potrzeby)
- Słuchaj co mówi klient
- Dopasuj argumenty do jego sytuacji
- Bądź konkretny (liczby, fakty)
- Proponuj konkretne rozwiązanie

### ❌ Częste błędy:
- Gadanie bez pytania
- Ogólnikowe argumenty ("dobra jakość")
- Ignorowanie obiekcji klienta
- Brak próby zamknięcia sprzedaży
- Agresywna sprzedaż

## 🔧 Struktura plików

```
BVA/
├── scenarios/
│   ├── __init__.py
│   └── heinz_simple_visit.py          # Logika scenariusza
│
├── views/scenarios/
│   ├── __init__.py
│   └── simple_visit_panel.py          # UI panelu
│
└── views/business_games_refactored/industries/
    └── fmcg_playable.py               # Integracja (tab "Scenariusz")
```

## 📝 Przykładowa rozmowa

```
👨‍🍳 Michał: Dzień dobry. Słucham Pana?

🎮 Ty: Dzień dobry! Jestem z Heinz. Czy mogę poświęcić Panu 5 minut?

👨‍🍳 Michał: Heinz? No dobra, pięć minut to mogę.

🎮 Ty: Dziękuję! Powiedz mi, jaki ketchup obecnie Pan używa?

👨‍🍳 Michał: Mam Pudliszki. Sprzedaje się normalnie, nie narzekam.

🎮 Ty: Rozumiem. A czy zdarza się że klienci pytają o inne marki?

👨‍🍳 Michał: No właśnie... czasem pytają o Heinz. Ale Pudliszki są tańsze.

🎮 Ty: Faktycznie, Heinz jest droższy w zakupie. Ale marża na Heinzu to 35%, 
     a na Pudliszkach? Około 25%?

👨‍🍳 Michał: Hmm... no tak mniej więcej. A ile to kosztuje?

... itd.
```

## 🚀 Rozwój scenariusza

Ten scenariusz jest bazą do dalszego rozwoju:

### Planowane rozszerzenia:
- [ ] Więcej klientów (różne osobowości)
- [ ] Różne produkty Heinz
- [ ] Wizyty wieloetapowe
- [ ] System reputacji
- [ ] Leaderboard
- [ ] Nagrania audio (voice AI)

## 🆘 Troubleshooting

### Problem: "System oceny niedostępny"
**Rozwiązanie:** Sprawdź czy masz klucz API Gemini w `config/gemini_api_key.txt`

### Problem: "Import error" przy uruchomieniu
**Rozwiązanie:** Sprawdź czy masz wszystkie foldery:
- `scenarios/`
- `views/scenarios/`

### Problem: Scenariusz się nie pokazuje
**Rozwiązanie:** Odśwież stronę (F5) lub zrestartuj Streamlit

## 📞 Kontakt

Pytania? Problemy? Sugestie?  
Zgłoś issue lub skontaktuj się z autorem.

---

**Wersja:** 1.0  
**Data:** 2025-11-09  
**Status:** ✅ Gotowy do użycia
