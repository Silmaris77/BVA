"""
FMCG Implementation - Plan Wykonania OPTION C
Data rozpoczęcia: 28 października 2025

=============================================================================
FAZA 1: MIGRACJA CONSULTING → SQL (Dzień 1-2)
=============================================================================

CHECKLIST:

DZIEŃ 1: PRZYGOTOWANIE + TEST MIGRATION
----------------------------------------
[✅] 1. Backup users_data.json
    Plik: users_data_backup_before_sql_migration_20251028.json
    
[✅] 2. Test dry-run migration (Max - consulting)
    Status: consulting OK (1 completed contract)
           fmcg SKIP (niepełna struktura - nowa implementacja w SQL)
    
[✅] 3. Live migration test (Max - tylko consulting)
    python scripts/migration/migrate_business_games.py Max --migrate
    Result: ✅ SUKCES! Consulting zmigrowany do SQL
    
[✅] 4. Verification SQL data
    python scripts/migration/test_sql_read.py Max
    Result: ✅ User found, data w SQL
    
[🔄] 5. Manual QA (Max account)
    NEXT STEP: Otworzyć aplikację, sprawdzić Business Games
    - Otwórz Business Games
    - Sprawdź czy consulting wyświetla się
    - Sprawdź completed contracts
    - Sprawdź historię transakcji
    - Sprawdź statystyki
    
[ ] 6. Rollback test (jeśli coś nie działa)
    cp users_data_backup_before_sql_migration_20251028.json users_data.json

DZIEŃ 2: BATCH MIGRATION (WSZYSCY UŻYTKOWNICY)
-----------------------------------------------
[ ] 7. Analiza użytkowników z business_games
    python -c "import json; ..."
    
[ ] 8. Batch migration Phase 1 (5 użytkowników)
    Wybierz użytkowników z consulting (nie FMCG!)
    
[ ] 9. Verification Phase 1
    
[ ] 10. Batch migration Phase 2 (15 użytkowników)
    
[ ] 11. Verification Phase 2
    
[ ] 12. Batch migration Phase 3 (reszta)
    
[ ] 13. Final verification
    python scripts/migration/final_stats.py
    
[ ] 14. Switch backend to SQL
    config/settings.py: DATABASE_BACKEND = "sql"
    
[ ] 15. Restart aplikacji + smoke test
    Otwórz kilka kont użytkowników, sprawdź business games


=============================================================================
FAZA 2: REFACTORING DATA STRUCTURE (Dzień 3)
=============================================================================

[ ] 16. Cleanup money/coins redundancja
    - Usuń bg_data["money"] (deprecated)
    - Usuń bg_data["firm"]["coins"] (stare)
    - Używaj tylko user_data["degencoins"]
    
[ ] 17. Update utils/business_game.py
    - Zmień wszystkie money references
    - Update docstringi
    
[ ] 18. Update views/business_games.py
    - get_game_data() → zawsze user_data["degencoins"]
    
[ ] 19. Tests
    - Manual QA
    - Check console errors
    - Verify coin balance calculations
    
[ ] 20. Documentation update
    - README.md - nowa struktura
    - FMCG_PRE_IMPLEMENTATION_AUDIT.md - mark as done


=============================================================================
FAZA 3: FMCG IMPLEMENTATION START (Dzień 4+)
=============================================================================

[ ] 21. Create FMCG module structure
    views/business_games_refactored/industries/fmcg/
        __init__.py
        data_models.py (Client, Contract schemas)
        game_logic.py (visit, task logic)
        ui_components.py (cards, forms)
    
[ ] 22. FMCG Game Initialization
    - initialize_fmcg_game(username)
    - Territory: Piaseczno (mapa Folium)
    - Starting clients: 5 PROSPECT
    
[ ] 23. Client Management
    - Client Card UI
    - Client lifecycle (PROSPECT/ACTIVE/LOST)
    - Per-client reputation
    
[ ] 24. AI Conversation System
    - Gemini 2.0 Flash integration
    - Conversation UI
    - Rating system (1-5⭐)
    - Outcome matrix implementation
    
[ ] 25. Task System
    - 5 task types (regular, operational, sales, emergency, admin)
    - Task completion effects
    - Calendar/schedule view
    
[ ] 26. Trade Marketing Tools
    - 5 tools (Gratis, Rabat, POS, Promocja, Darmowa dostawa)
    - Budget tracking (2000 PLN/m)
    - Cooldowns & diminishing returns
    
[ ] 27. Energy System
    - 100%/day
    - Distance-based costs
    - Visit planning
    
[ ] 28. Dashboard & Reports
    - Main dashboard
    - Weekly report
    - Charts (reputation, revenue)
    
[ ] 29. Progression System
    - Level up (Junior → Mid → Senior)
    - Unlock new features
    - Achievements
    
[ ] 30. Testing & Polish
    - Full playthrough test
    - Balance tuning
    - Bug fixes
    - UI polish


=============================================================================
NOTATKI
=============================================================================

UWAGI Z DRY-RUN:
- Max ma consulting (1 completed contract) - gotowe do migracji
- Max ma fmcg (niepełna struktura) - SKIP, nowa implementacja w SQL
- Inne scenariusze mogą mieć podobny mix

STRATEGIA MIGRACJI:
- Migrujemy TYLKO consulting (pełna struktura)
- FMCG pomijamy (będzie tworzone od nowa w SQL)
- Jeśli user ma tylko FMCG → SKIP (później dostanie nowy FMCG)

SQL MODELS READY:
✅ BusinessGame
✅ BusinessGameContract (z extra_data dla FMCG!)
✅ BusinessGameEmployee
✅ BusinessGameTransaction
✅ BusinessGameStats

REPOSITORY READY:
✅ BusinessGameRepository(backend="sql")
✅ UserRepository(backend="sql")

NEXT STEPS AFTER PHASE 1:
1. Switch backend to "sql"
2. Refactor money/coins
3. Start FMCG implementation with clean slate!

