# 🎛️ Interaktywny Panel Kontrolny Mapy Myśli

## 📋 Przegląd funkcjonalności

Panel kontrolny umożliwia użytkownikom personalizację i eksport map myśli bezpośrednio z interfejsu aplikacji. Dostępny w sekcji "4. Podsumowanie" każdej lekcji.

## 🎨 Opcje personalizacji

### Kolumna 1: Rozmiary
- **Rozmiar węzłów** (0.5x - 2.0x)
  - Skaluje wielkość wszystkich węzłów na mapie
  - Domyślnie: 1.0x (oryginalny rozmiar)
  - Użyj mniejszych wartości dla kompaktowego widoku
  - Użyj większych wartości dla prezentacji

- **Rozmiar czcionki** (0.7x - 1.5x)
  - Skaluje tekst w węzłach
  - Domyślnie: 1.0x
  - Przydatne dla poprawy czytelności

### Kolumna 2: Układ
- **Fizyka włączona** (checkbox)
  - Włącza/wyłącza dynamiczny układ z symulacją fizyczną
  - Gdy włączona: węzły poruszają się i układają automatycznie
  - Gdy wyłączona: statyczny układ

- **Układ hierarchiczny** (checkbox)
  - Organizuje węzły w strukturze hierarchicznej
  - Przydatne dla map o jasnej strukturze poziomów

- **Szerokość mapy** (600px - 1400px)
  - Dostosuj szerokość obszaru mapy
  - Domyślnie: 900px

- **Wysokość mapy** (400px - 1000px)
  - Dostosuj wysokość obszaru mapy
  - Domyślnie: 600px

### Kolumna 3: Eksport
- **Zrzut ekranu** (instrukcje dla różnych platform)
- **Eksport do JSON** (przycisk pobierania)

## 📸 Jak zrobić zrzut ekranu mapy

### Windows
- **Win + Shift + S**: Narzędzie Wycinanie
- **Alt + PrtScn**: Zrzut aktywnego okna
- **Win + PrtScn**: Pełny ekran (zapisuje do Obrazy)

### macOS
- **Cmd + Shift + 4**: Wybierz obszar
- **Cmd + Shift + 3**: Pełny ekran
- **Cmd + Shift + 4 + Spacja**: Zrzut okna

### Przeglądarki
- **Firefox**: Narzędzia Przeglądarki → Zrzut strony
- **Chrome/Edge**: DevTools (F12) → ... → Capture screenshot

## 💾 Eksport do JSON

Przycisk "📥 Pobierz mapę (JSON)" pozwala:
- Zapisać strukturę mapy w formacie JSON
- Użyć danych w innych narzędziach
- Zachować backup konfiguracji mapy

## 🎯 Przykładowe konfiguracje

### Widok rozszerzony (prezentacja)
- Rozmiar węzłów: 1.5x
- Rozmiar czcionki: 1.2x
- Szerokość: 1200px
- Wysokość: 800px
- Fizyka: włączona

### Widok kompaktowy (przegląd)
- Rozmiar węzłów: 0.7x
- Rozmiar czcionki: 0.8x
- Szerokość: 700px
- Wysokość: 500px
- Fizyka: wyłączona

### Widok do druku
- Rozmiar węzłów: 1.0x
- Rozmiar czcionki: 1.0x
- Szerokość: 1000px
- Wysokość: 700px
- Fizyka: wyłączona (dla stabilnego układu)

## 🔧 Szczegóły techniczne

### Renderowanie
- Biblioteka: streamlit-agraph
- Format węzłów: Node objects z customizowanymi właściwościami
- Format krawędzi: Edge objects z kierunkiem i etykietami

### Interaktywność
- Przybliżanie/oddalanie: scroll myszy
- Przeciąganie węzłów: kliknij i przeciągnij
- Panoramowanie: przeciągnij tło mapy

---

*Uwaga: Panel kontrolny jest dostępny w trybie rozszerzonym (expander) i nie wpływa na wydajność aplikacji gdy jest zwinięty.*
