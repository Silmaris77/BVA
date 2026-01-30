# 🗑️ Analiza plików do usunięcia - BVA Application

**Data analizy:** 27 października 2025  
**Cel:** Identyfikacja niepotrzebnych plików, które można bezpiecznie usunąć

---

## 📊 Podsumowanie

| Kategoria | Liczba plików | Rozmiar (szacunkowy) | Priorytet usunięcia |
|-----------|---------------|---------------------|---------------------|
| Backupy JSON (stare) | 6 plików | ~10-50 MB | 🟢 WYSOKI |
| Pliki .bak (temp) | 10 plików | ~2-5 MB | 🟢 WYSOKI |
| Skrypty fix_* (jednorazowe) | 18 plików | ~500 KB | 🟡 ŚREDNI |
| Pliki test_* (rozwojowe) | 19 plików | ~1 MB | 🟡 ŚREDNI |
| Pliki temp/ (tymczasowe) | 8 plików | ~2 MB | 🟢 WYSOKI |
| Logi debug (.log) | 5 plików | ~100-500 KB | 🟢 WYSOKI |
| Pliki HTML (prototypy) | 4 pliki | ~500 KB | 🟡 ŚREDNI |
| Inne (MD, scripts) | ~5 plików | ~100 KB | 🔴 NISKI |

**Łącznie:** ~60-70 plików, ~15-60 MB

---

## 🟢 PRIORYTET WYSOKI - Usuń natychmiast

### 1. Backupy JSON użytkowników (stare)

**Lokalizacja:** Root folder  
**Status:** ✅ Bezpieczne do usunięcia (mamy najnowszy + backupy w `backups/`)

```
users_data_backup_20251019_014517.json          # 8 dni temu
users_data_backup_20251025_175412.json          # 2 dni temu
users_data_backup_20251027_230904.json          # dzisiaj (wcześniejszy)
users_data_backup_emergency_20251027_230946.json # dzisiaj (awaryjny)
users_data_backup_fix_20251027_231033.json      # dzisiaj (fix)
users_data_backup_beta_20251025_150832.json     # beta test
```

**Zalecenie:** Zachowaj TYLKO najnowszy (users_data_backup_fix_20251027_231033.json), resztę usuń.

---

### 2. Pliki backup .bak w temp/import_backups/

**Lokalizacja:** `temp/import_backups/`  
**Status:** ✅ Bezpieczne do usunięcia (stare backupy z 24 października)

```
temp/import_backups/main.py.20251024_193037.bak
temp/import_backups/main.py.20251024_193011.bak
temp/import_backups/dashboard.py.20251024_193037.bak
temp/import_backups/dashboard.py.20251024_193011.bak
temp/import_backups/business_games.py.20251024_193037.bak
temp/import_backups/business_games.py.20251024_193011.bak
temp/import_backups/admin.py.20251024_193037.bak
temp/import_backups/admin.py.20251024_193011.bak
temp/import_backups/activity_tracker.py.20251024_193037.bak
temp/import_backups/activity_tracker.py.20251024_193011.bak
```

**Zalecenie:** Usuń wszystkie (mamy nowsze w .git)

---

### 3. Pliki tymczasowe w temp/

**Lokalizacja:** `temp/`  
**Status:** ✅ Bezpieczne do usunięcia

```
temp/npc_audio_1761399253.34533.mp3           # Tymczasowe audio (ElevenLabs)
temp/npc_audio_1761399826.743076.mp3          # Tymczasowe audio
temp/npc_audio_1761400048.684071.mp3          # Tymczasowe audio
temp/Kolb_Raport_Max_20251016_180829.html     # Stary raport testowy
temp/Kolb_Raport_Max_20251016_180904.html     # Stary raport testowy
temp/business_games_layout_prototype.html      # Prototyp (już zaimplementowany)
temp/cheatsheet.png                            # ?
temp/dzwieki_timer.html                        # Prototyp HTML
```

**Zalecenie:** Usuń wszystkie pliki MP3 i HTML (prototypy już w produkcji)

---

### 4. Logi debug (.log)

**Lokalizacja:** Root folder  
**Status:** ✅ Bezpieczne do usunięcia (development logs)

```
business_games_debug.log
button_click_debug.log
save_debug.log
save_method_entry.log
save_single_user_debug.log
```

**Zalecenie:** Usuń wszystkie (można je zawsze odtworzyć)

---

### 5. Backup config

```
config/settings.py.bak
```

**Zalecenie:** Usuń (mamy w .git)

---

## 🟡 PRIORYTET ŚREDNI - Rozważ usunięcie

### 6. Jednorazowe skrypty fix_*

**Lokalizacja:** Root folder  
**Status:** ⚠️ Skrypty naprawcze już wykonane, ale mogą być przydatne jako przykłady

```
fix_comm_analyzer_emoji.py
fix_emoji.py
fix_encoding.py
fix_html.py
fix_json_error.py               # ✅ Właśnie utworzony (dzisiaj)
fix_json_newline.py             # ✅ Właśnie utworzony (dzisiaj)
fix_json_precise.py             # ✅ Właśnie utworzony (dzisiaj)
fix_lesson_emoji.py
fix_lesson_remaining.py
fix_plotly_chart.py
fix_remaining.py
fix_sections_emoji.py
fix_simulator.py
fix_tabs_order.py
fix_tools_all_emoji.py
fix_tools_emoji_part2.py
fix_use_container_width.py
fix_users_json.py
```

**Zalecenie:**
- **ZACHOWAJ:** `fix_json_error.py`, `fix_json_newline.py`, `fix_json_precise.py` (nowe, mogą się przydać)
- **USUŃ:** Reszta (stare, jednorazowe naprawy)

---

### 7. Skrypty testowe test_*

**Lokalizacja:** Root folder  
**Status:** ⚠️ Testy rozwojowe, niektóre mogą być przydatne

```
test_ai_conversation_flow.py
test_ai_evaluation.py
test_anti_cheat.py
test_backward_compatibility.py
test_business_games.py
test_dev_mode.py
test_elevenlabs.py
test_engagement_v2.py
test_evaluation_mode.py
test_evaluation_system.py
test_gemini_api_key.py
test_lesson_coins.py
test_mi_implementation.py
test_mi_profiles.py
test_new_charts.py
test_radar_chart.py
test_simulator_import.py
test_split.py
test_weasyprint.py
test_who_am_i_report.py
test_xhtml2pdf.py
```

**Zalecenie:**
- **PRZENIEŚ DO:** `tests/` folder (uporządkowanie)
- **ZACHOWAJ:** Testy kluczowych funkcji (test_business_games.py, test_backward_compatibility.py)
- **USUŃ:** Jednorazowe testy (test_gemini_api_key.py, test_new_charts.py)

---

### 8. Inne skrypty pomocnicze

```
apply_refactoring.py           # ⚠️ Czy już użyty?
check_contracts.py
cleanup_business_games.py      # ✅ Już wykonany (dzisiaj)
debug_ai_contracts.py
delete_mick.py                 # ✅ Już wykonany (usunięcie użytkownika)
extract_fmcg.py                # ✅ Już wykonany (dzisiaj)
find_fstrings.py
find_singles.py
list_gemini_models.py
migrate_contract_types.py
remove_functions_utf8.py
remove_old_functions.py
set_ai_mode.py
```

**Zalecenie:**
- **ZACHOWAJ:** `list_gemini_models.py`, `set_ai_mode.py` (mogą być przydatne)
- **PRZENIEŚ DO:** `scripts/maintenance/` - `cleanup_business_games.py`, `extract_fmcg.py`
- **USUŃ:** `delete_mick.py`, `apply_refactoring.py` (jeśli już wykonane)

---

### 9. Pliki HTML (testowe/prototypy)

```
Kolb_Raport_admin_20251016_103417.html  # Stary raport testowy (root)
test_html_report.html                    # Test HTML
test_plotly_offline.html                 # Test wykresu
visualization_samples.html               # Próbki wizualizacji
README.html                              # Duplikat README.md
```

**Zalecenie:**
- **USUŃ:** Wszystkie testy HTML (są w temp/ lub nieaktualne)
- **ZACHOWAJ:** README.html tylko jeśli jest używany

---

### 10. Pliki PowerShell .ps1

```
fix_kolb_visualization.ps1
replace_kolb_cards.ps1
```

**Zalecenie:** Usuń (jednorazowe naprawy)

---

## 🔴 PRIORYTET NISKI - Zachowaj lub rozważ archiwizację

### 11. Pliki dokumentacji MD

```
AI_CONVERSATION_CLEANUP.md
AI_CONVERSATION_READY.md
AI_CONVERSATION_USER_FIX.md
AUDIO_DUPLICATION_FIX.md
AUDIO_DYNAMIC_RERENDER_FIX.md
AUDIO_INPUT_UPGRADE.md
BETA_READY_SUMMARY.md
BETA_TESTER_GUIDE.md
BETA_TESTING_CHECKLIST.md
BUSINESS_GAMES_COACHING_SPLIT.md
BUSINESS_GAMES_GUIDE.md
CHANGELOG_2025_10_27.md
ELEVENLABS_QUICKSTART.md
ELEVENLABS_SETUP.md
FMCG_IMPLEMENTATION_STATUS.md
GEMINI_COST_ANALYSIS.md
GOOGLE_FORMS_TEMPLATE.md
MATERIALY_PROMOCYJNE.md
MECHANIKA_VS_CONTENT_DECISION.md
MIND_MAP_CONTROLS.md
MVP_MONETIZATION_STRATEGY.md
NEXT_STEPS.md
PERFORMANCE_REPORT.md
PRICING_STRATEGY.md
PRIORYTET_1_PROGRESS_REPORT.md
REFACTORING_PLAN.md
REFACTORING_STATUS.md
SALES_PITCH_DECK.md
SALES_SCRIPT.md
SALES_SCRIPT_B2B_FOCUS.md
SECRETS_SETUP.md
URGENT_KEY_ROTATION.md
```

**Zalecenie:**
- **PRZENIEŚ DO:** `docs/archive/` - stare statusy i raporty
- **ZACHOWAJ w ROOT:** Kluczowe MD (README.md, CHANGELOG_*, SECRETS_SETUP.md)
- **ZACHOWAJ w docs/:** Guides, procedury (BETA_TESTER_GUIDE.md, ELEVENLABS_SETUP.md)

---

### 12. Inne pliki

```
11b. Licytacja, rankingi, timer.xlsm  # Excel - co to?
Key.docx                               # ???
start.bat                              # Batch starter (Windows)
```

**Zalecenie:** Sprawdź co zawierają, rozważ przeniesienie do docs/ lub usunięcie

---

## 📋 Skrypt do automatycznego czyszczenia

Mogę utworzyć skrypt PowerShell, który:
1. Utworzy backup przed czyszczeniem
2. Usunie pliki z PRIORYTET WYSOKI
3. Przeniesie pliki do odpowiednich folderów
4. Wygeneruje raport

**Czy chcesz, żebym to zrobił?**

---

## 🎯 Rekomendowana akcja

### Krok 1: Bezpieczne usunięcie (PRIORYTET WYSOKI)
```powershell
# Usuń stare backupy JSON (zachowaj najnowszy)
# Usuń pliki .bak
# Usuń logi .log
# Wyczyść temp/
```

### Krok 2: Reorganizacja (PRIORYTET ŚREDNI)
```powershell
# Przenieś testy do tests/
# Przenieś skrypty do scripts/maintenance/
# Przenieś stare MD do docs/archive/
```

### Krok 3: Weryfikacja
```powershell
# Sprawdź czy aplikacja działa
# Commit do git
```

---

## 💾 Szacowane odzyskanie miejsca

- **Natychmiastowe (Priorytet Wysoki):** ~15-25 MB
- **Po reorganizacji (Priorytet Średni):** ~5-10 MB dodatkowych
- **Łącznie:** ~20-35 MB

---

## ⚠️ Ostrzeżenia

1. **NIE USUWAJ:**
   - `users_data.json` (aktywne dane!)
   - Pliki w `backups/` (główne backupy)
   - Pliki w `.git/` (historia)
   - Pliki w `data/` (dane aplikacji)

2. **PRZED USUNIĘCIEM:**
   - Zrób commit do git
   - Sprawdź czy aplikacja działa
   - Opcjonalnie: pełny backup foldera

3. **Testuj po czyszczeniu:**
   - `streamlit run main.py`
   - Sprawdź wszystkie kluczowe funkcje

---

## 🤖 Następne kroki

Mogę dla Ciebie:
1. ✅ Utworzyć skrypt czyszczący (PowerShell)
2. ✅ Wykonać czyszczenie krok po kroku
3. ✅ Zarchiwizować stare pliki zamiast usuwać
4. ✅ Wygenerować raport po czyszczeniu

**Co wybierasz?**
