# ⏱️ Narzędzie do Zarządzania Szkoleniem

## 📋 Opis

Kompleksowe narzędzie do prowadzenia szkoleń z funkcjami:
- **Timer** - odliczanie czasu na ćwiczenia
- **Licytacja** - śledzenie ofert zespołów
- **Rankingi** - monitoring postępów i efektywności
- **Wykresy** - wizualizacja wzrostu dochodów i efektywności

## 🚀 Funkcjonalności

### ⏱️ Timer
- Ustawienie czasu w minutach (1-180 min)
- Duży, czytelny wyświetlacz odliczający
- Progress bar pokazujący postęp
- Efekt wizualny i dźwiękowy po zakończeniu
- Możliwość zatrzymania i resetu

### 💰 Licytacja
- Śledzenie ofert wszystkich zespołów
- Ranking zespołów po kwotach
- Medalki dla TOP 3
- Łatwa aktualizacja ofert
- Reset wszystkich ofert jednym kliknięciem

### 📊 Rankingi & Postępy
- **Dochód** - tracking przychodów w kolejnych rundach
- **Efektywność** - monitoring wydajności zespołów
- Tabele podsumowujące z historią
- **Wykresy interaktywne** (Plotly):
  - Wzrost dochodów w czasie
  - Wzrost efektywności w czasie
- Kontrola rund (start, następna, reset)

### ⚙️ Ustawienia
- **Zarządzanie zespołami**:
  - Edycja nazw zespołów
  - Dodawanie nowych zespołów
  - Usuwanie zespołów (min. 2)
- **Reset globalny** - przywrócenie ustawień fabrycznych

## 📖 Jak używać

### 1. Uruchom aplikację
Narzędzie znajduje się w zakładce **🔧 Narzędzia → ⏱️ Zarządzanie Szkoleniem**

### 2. Przygotuj zespoły
W zakładce **⚙️ Ustawienia**:
- Zmień nazwy domyślnych zespołów
- Dodaj więcej zespołów jeśli potrzeba
- Usuń zbędne zespoły

### 3. Prowadź szkolenie

**Timer:**
1. Ustaw czas na ćwiczenie (np. 30 minut)
2. Kliknij **START**
3. Timer będzie odliczał i pokazywał postęp
4. Po zakończeniu pojawi się komunikat "CZAS MINĄŁ!"

**Licytacja:**
1. Każdy zespół podaje swoją ofertę
2. Prowadzący aktualizuje kwoty w systemie
3. Ranking aktualizuje się automatycznie
4. Zespoły widzą swoją pozycję (medalki)

**Postępy:**
1. Po każdej rundzie wprowadź:
   - Dochód zespołu w tej rundzie
   - Efektywność zespołu (0-20)
2. Kliknij **Następna runda**
3. Zobacz wykresy i trendy
4. Exportuj dane (opcjonalnie)

## 💡 Wskazówki

- **Auto-refresh**: Timer odświeża się automatycznie co sekundę
- **Persistent data**: Dane zachowują się w session (do przeładowania strony)
- **Wizualizacje**: Wykresy są interaktywne - możesz zoomować, exportować jako PNG
- **Kolory**: Każdy zespół ma swój dedykowany kolor na wykresach

## 🔧 Techniczne

### Stack
- **Frontend**: Streamlit
- **Wykresy**: Plotly
- **Dane**: Pandas, session_state
- **Timer**: datetime, time.sleep + auto-rerun

### Session State Keys
- `training_teams` - lista zespołów z danymi
- `training_timer_end` - czas zakończenia timera
- `training_current_round` - numer aktualnej rundy

## 📝 Przykładowa struktura danych zespołu

```python
{
    "name": "Zespół 1",
    "bid": 500,  # Kwota licytacji
    "revenue": [100, 2500, 3000],  # Dochód w rundach
    "efficiency": [9, 10, 11]  # Efektywność w rundach
}
```

## 🎯 Use Cases

1. **Szkolenia biznesowe** - symulacje rynkowe
2. **Warsztaty zespołowe** - konkursy i wyzwania
3. **Gamifikacja** - śledzenie postępów
4. **Debriefing** - analiza wyników na wykresach

## 📧 Wsparcie

Pytania? Problemy? Skontaktuj się z zespołem BrainVenture Academy!
