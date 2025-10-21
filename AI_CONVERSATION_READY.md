# 🎮 AI Conversation Contracts - Gotowe!

## ✅ Co zostało zaimplementowane

### 1. **Backend (Engine)**
- `utils/ai_conversation_engine.py` - 7 funkcji do zarządzania rozmowami AI:
  - `initialize_ai_conversation()` - start rozmowy
  - `get_conversation_state()` - odczyt stanu
  - `evaluate_player_response()` - Gemini ocenia odpowiedź gracza
  - `generate_npc_reaction()` - Gemini generuje reakcję NPC
  - `process_player_message()` - orkiestruje całość
  - `calculate_final_conversation_score()` - końcowy wynik (1-5★)
  - `reset_conversation()` - replay

### 2. **Integracja z systemem nagród**
- `utils/business_game.py`:
  - `submit_contract_ai_conversation()` - finalizuje kontrakt
  - Nalicza nagrody (interpolacja liniowa base → 5star)
  - Aktualizuje degencoins, reputację, statystyki
  - Przenosi kontrakt do completed

### 3. **UI (Streamlit)**
- `views/business_games.py`:
  - `render_ai_conversation_contract()` - kompletny interfejs chat
  - Historia rozmowy (player + NPC messages z emotikonami)
  - Sidebar z metrykami na żywo (empathy, assertiveness, etc.)
  - Input gracza + przycisk wysyłki
  - AI feedback po każdej turze
  - Ekran podsumowania z gwiazdkami i metrykami
  - Przyciski: "Zagraj ponownie" i "Zakończ kontrakt"

### 4. **Kontrakty**
Gotowe w `data/business_data.py`:

**CIQ-AI-001: "💬 Rozmowa: Spóźniający się Talent"**
- NPC: Mark (Senior Developer)
- Scenariusz: Spóźnienia pracownika, ukryty problem rodzinny
- Wymaga: Empatia + GROW Model
- Nagrody: 600-1100 coins, +40 rep
- **Wymagany poziom: 1** (dostępny od startu)

**CIQ-AI-002: "💬 Rozmowa: Trudne Negocjacje"**
- NPC: Michael (CEO TechVentures)
- Scenariusz: Klient żąda 40% zniżki lub odchodzi
- Wymiar: Negocjacje + komunikacja wartości
- Nagrody: 800-1400 coins, +50 rep
- **Wymagany poziom: 1** (dostępny od startu)

---

## 🚀 Jak uruchomić i przetestować

### Krok 1: Uruchom aplikację Streamlit
```powershell
streamlit run main.py
```

### Krok 2: Przejdź do Business Games
1. Zaloguj się / wybierz profil
2. Kliknij **Business Games**
3. Jeśli nowa gra: wybierz branżę (np. Consulting)

### Krok 3: Znajdź kontrakty AI Conversation
1. Zakładka **"Rynek Kontraktów"**
2. **WAŻNE:** Jeśli nie widzisz kontraktów z 💬, kliknij przycisk **"🔄 Wymuś odświeżenie"** (odświeży pulę kontraktów)
3. Poszukaj kontraktów z ikoną 💬:
   - "💬 Rozmowa: Spóźniający się Talent"
   - "💬 Rozmowa: Trudne Negocjacje"
4. Kliknij **"Przyjmij"**

### Krok 4: Przeprowadź rozmowę
1. Po przyjęciu kontrakt pojawi się w **"Aktywne Kontrakty"**
2. Kliknij na kontrakt aby otworzyć chat
3. Przeczytaj scenariusz (expander "📖 Kontekst sytuacji")
4. **Sidebar** pokaże metryki na żywo
5. **Wpisz odpowiedź** w pole tekstowe (np. "Dzień dobry Mark, chciałbym z Tobą porozmawiać...")
6. Kliknij **"📤 Wyślij wiadomość"**
7. **AI oceni** Twoją odpowiedź i wygeneruje reakcję NPC
8. Kontynuuj rozmowę (AI reaguje dynamicznie!)
9. Gdy uznasz że zakończyłeś rozmówę, kliknij **"🏁 Zakończ"**

### Krok 5: Zobacz wyniki
1. Ekran podsumowania pokaże:
   - ⭐ Gwiazdki (1-5)
   - 🎯 Punkty
   - 📊 Metryki (empatia, asertywność, profesjonalizm, rozwiązania)
   - 💬 Pełna historia rozmowy (expander)
2. Możesz:
   - **"🔄 Zagraj ponownie"** - reset rozmowy
   - **"✅ Zakończ kontrakt"** - zapisz wynik, otrzymaj nagrody

---

## 🧪 Co przetestować

### Testy funkcjonalne
- [ ] Kontrakt pojawia się na rynku (badge 💬)
- [ ] Przyjęcie kontraktu działa
- [ ] Chat UI się otwiera, widać wiadomość powitalną NPC
- [ ] Wysyłka wiadomości wywołuje AI (spinner "🤖 AI analizuje...")
- [ ] NPC odpowiada realistycznie (sprawdź różne style odpowiedzi)
- [ ] Metryki aktualizują się po każdej turze
- [ ] Relationship health się zmienia (bar w sidebar)
- [ ] Zakończenie rozmowy pokazuje podsumowanie
- [ ] "Zagraj ponownie" resetuje stan
- [ ] "Zakończ kontrakt" przenosi do completed + daje nagrody

### Testy AI Quality
**CIQ-AI-001 (Mark):**
- [ ] Podejście konfrontacyjne → Mark defensywny, nie otwiera się
- [ ] Podejście empatyczne → Mark stopniowo ujawnia problem z matką
- [ ] Pytania GROW → AI rozpoznaje technikę, wyższe punkty
- [ ] Rozwiązanie (flex hours) → SUCCESS ending

**CIQ-AI-002 (Michael):**
- [ ] Natychmiastowa 40% zniżka → WORST ending (20 pkt)
- [ ] Sztywne odmowa → BAD ending (klient odchodzi)
- [ ] Pokazanie ROI z ostatniego roku → GREAT ending
- [ ] Kreatywny custom package → BEST ending + achievement

### Testy balansu
- [ ] 1-2★ = czy faktycznie osiągalne przy słabych odpowiedziach?
- [ ] 4-5★ = czy osiągalne przy dobrych (bez bycia ekspertem)?
- [ ] Nagrody proporcjonalne do trudności?
- [ ] Relationship health logicznie reaguje na styl komunikacji?

---

## 🐛 Known Issues (możliwe do napotkania)

1. **Kontrakty nie pojawiają się na rynku**
   - Objaw: Nie widzisz 💬 kontraktów mimo że są w CONTRACTS_POOL
   - Przyczyna: `wymagany_poziom` > poziom firmy
   - Fix: ✅ **NAPRAWIONE** - oba kontrakty mają teraz `wymagany_poziom: 1`
   - Jeśli nadal nie widać: sprawdź czy `refresh_contract_pool` się wykonał (poczekaj 24h lub force refresh)

2. **Brak klucza Gemini API**
   - Objaw: Błąd "❌ Brak klucza API Gemini"
   - Fix: Dodaj klucz w `.streamlit/secrets.toml`:
     ```toml
     [API_KEYS]
     gemini = "AIza..."
     ```

2. **Limit API Gemini**
   - Objaw: Error 429 (Too Many Requests)
   - Fix: Poczekaj minutę lub użyj innego klucza

3. **AI nie rozpoznaje subtelnych technik**
   - Normalnie - model jest dobry ale nie idealny
   - Można ulepszyć prompty w `ai_conversation_engine.py`

4. **Streamlit warnings w testach offline**
   - Normalne - ignoruj lub użyj `2>$null` (PowerShell)

---

## 📝 Następne kroki (TODO)

### Krótkoterminowe (przed release)
- [ ] **Przetestować oba kontrakty end-to-end**
- [ ] Sprawdzić czy scoring jest fair (nie za łatwo/trudno)
- [ ] Zweryfikować czy NPC personalities są wyraziste
- [ ] Test anti-cheat (czy można oszukać kopiując odpowiedzi?)

### Średnioterminowe (enhancement)
- [ ] **Speed Challenge contracts** (timer-based)
- [ ] Więcej AI Conversation scenarios (3-5 dodatkowych)
- [ ] Achievement system dla najlepszych zakończeń
- [ ] Leaderboard dla AI conversations (najwyższe avg ratings)

### Długoterminowe (advanced)
- [ ] Multi-NPC conversations (np. negocjacje 3-stronne)
- [ ] Voice input (Whisper API)
- [ ] Persistent NPC memory (Redis/vector DB)
- [ ] Adaptacyjna trudność (AI dopasowuje się do poziomu gracza)

---

## 💡 Tips dla gracza

### Jak osiągnąć 5★?
1. **Czytaj scenariusz** - ukryte konteksty są kluczem
2. **Zadawaj pytania** zamiast od razu dawać rady
3. **Używaj technik** z lekcji (GROW, CNV, active listening)
4. **Empatia + asertywność** - balans jest ważny
5. **Eksperymentuj** - replay pozwala próbować różne ścieżki

### Czerwone flagi (niskie punkty)
- ❌ Natychmiastowe osądzanie
- ❌ Ignorowanie emocji rozmówcy
- ❌ Sztywne procedury bez kontekstu
- ❌ Brak follow-up questions
- ❌ Szybkie "rozwiązanie" bez diagnozy

---

**Status: ✅ GOTOWE DO TESTOWANIA**

Wszelkie bugi/feedback proszę zgłaszać!
