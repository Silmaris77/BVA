# 🚀 Plan Refaktoryzacji Business Games

## 📊 Stan obecny
- **Główny plik**: `views/business_games.py` - **7,960 linii** (za duży!)
- **Problem**: Trudne utrzymanie, debugowanie, testowanie
- **Cel**: Podział na logiczne moduły po ~300-500 linii każdy

## 📁 Nowa struktura katalogów

```
views/
  business_games/
    __init__.py                 # Główny export (show_business_games)
    helpers.py                  # ✅ UTWORZONY - Funkcje pomocnicze
    main.py                     # Główny widok i routing
    
    # === TABS - Główne zakładki ===
    tabs/
      __init__.py
      dashboard.py              # Dashboard tab (show_dashboard_tab)
      contracts.py              # Kontrakty tab (show_contracts_tab)
      management.py             # Zarządzanie tab (wszystkie pod-taby)
      settings.py               # Ustawienia tab
    
    # === COMPONENTS - Komponenty UI ===
    components/
      __init__.py
      contract_card.py          # Karty kontraktów (aktywne, dostępne, ukończone)
      employee_card.py          # Karty pracowników
      event_card.py             # Karty wydarzeń
      charts.py                 # Wykresy (finansowe, KPI)
      headers.py                # Nagłówki firm (render_header, render_fmcg_header)
    
    # === FMCG - Specyficzne dla branży FMCG ===
    fmcg/
      __init__.py
      onboarding.py             # FMCG onboarding
      dashboard.py              # FMCG dashboard
      customers.py              # FMCG customers tab
      tasks.py                  # FMCG tasks tab
      company_info.py           # FMCG company info
    
    # === MANAGEMENT - Pod-zakładki zarządzania ===
    management/
      __init__.py
      office.py                 # Zakładka Biuro
      employees.py              # Zakładka Pracownicy
      financial_reports.py      # Zakładka Raporty Finansowe
      history.py                # Zakładka Historia & Wydarzenia
```

## 🎯 Fazy refaktoryzacji

### ✅ **FAZA 1: Przygotowanie** (UKOŃCZONA)
- [x] Stworzono katalog `views/business_games/`
- [x] Stworzono `__init__.py`
- [x] Stworzono `helpers.py` z funkcjami utility

### 🔄 **FAZA 2: Komponenty UI** (W TRAKCIE)
- [ ] `components/charts.py` - Wykresy (create_financial_chart, etc.)
- [ ] `components/headers.py` - Nagłówki (render_header, render_fmcg_header)
- [ ] `components/contract_card.py` - Karty kontraktów
  - render_active_contract_card
  - render_contract_card
  - render_completed_contract_card
  - render_decision_tree_contract
  - render_conversation_contract
  - render_speed_challenge_contract
- [ ] `components/employee_card.py` - Karty pracowników
  - render_employee_card
  - render_hire_card
- [ ] `components/event_card.py` - Wydarzenia
  - show_active_event_card
  - render_latest_event_card
  - render_active_effects_badge

### ⏳ **FAZA 3: Główne zakładki**
- [ ] `tabs/dashboard.py` - show_dashboard_tab
- [ ] `tabs/contracts.py` - show_contracts_tab
- [ ] `tabs/management.py` - Zarządzanie (router do pod-tabów)
- [ ] `tabs/settings.py` - show_firm_settings_tab, show_game_management_tab

### ⏳ **FAZA 4: FMCG moduł**
- [ ] `fmcg/onboarding.py` - show_fmcg_onboarding
- [ ] `fmcg/dashboard.py` - show_fmcg_dashboard_tab
- [ ] `fmcg/customers.py` - show_fmcg_customers_tab, render_fmcg_customer_conversation
- [ ] `fmcg/tasks.py` - show_fmcg_tasks_tab
- [ ] `fmcg/company_info.py` - show_fmcg_company_info_tab

### ⏳ **FAZA 5: Management pod-zakładki**
- [ ] `management/office.py` - show_office_tab
- [ ] `management/employees.py` - show_employees_tab
- [ ] `management/financial_reports.py` - show_financial_reports_tab + wszystkie analizy
- [ ] `management/history.py` - show_history_tab, show_events_tab

### ⏳ **FAZA 6: Główny router**
- [ ] `main.py` - show_business_games, show_industry_game, routing, CSS
- [ ] Aktualizacja importów w całym projekcie

### ⏳ **FAZA 7: Testy i czyszczenie**
- [ ] Testy importów
- [ ] Testy funkcjonalności
- [ ] Usunięcie starego `business_games.py`
- [ ] Aktualizacja dokumentacji

## 📈 Metryki sukcesu

**Przed:**
- 1 plik: 7,960 linii
- Trudne utrzymanie
- Brak separacji odpowiedzialności

**Po:**
- ~25 plików po 200-400 linii
- Klarowna struktura
- Łatwe testowanie i rozwijanie
- Gotowość do dalszej skalowalności

## 🚧 Następne kroki

1. **Teraz**: Wydzielić komponenty UI (charts, headers, cards)
2. **Potem**: Wydzielić zakładki (dashboard, contracts, management)
3. **Na koniec**: Główny router i testy

## ⚠️ Ważne uwagi

- **Backward compatibility**: Wszystkie istniejące importy będą działać (`from views.business_games import show_business_games`)
- **Stopniowa migracja**: Stary plik pozostaje dopóki nie przeniesiemy wszystkiego
- **Zero downtime**: Aplikacja działa cały czas podczas refaktoryzacji
- **Testy**: Po każdej fazie testujemy czy wszystko działa

---
**Status**: 🟢 FAZA 1 ukończona | 🔄 FAZA 2 w trakcie
**Ostatnia aktualizacja**: 2025-10-27
